#!/usr/bin/env python3
"""Read-only public sitemap and HTML metadata audit. Python standard library only."""
import argparse
import concurrent.futures
import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

MAX_BYTES = 8_000_000


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.canonical, self.ld = {}, [], []
        self.title, self.in_title, self.script = '', False, None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property', '')).lower()] = attrs.get('content', '')
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonical.append(attrs.get('href', ''))
        if tag == 'title':
            self.in_title = True
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.script = ''

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.script is not None:
            self.script += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script' and self.script is not None:
            try:
                json.loads(self.script)
                self.ld.append(True)
            except (ValueError, TypeError):
                self.ld.append(False)
            self.script = None


def origin(url):
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username or parts.password:
        raise ValueError('Expected an HTTP(S) URL without credentials')
    return urlunsplit((parts.scheme, parts.netloc, '', '', ''))


def fetch(url):
    record = {'url': url}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; SearchConsoleAudit/1.0)'})
        try:
            response = urllib.request.urlopen(request, timeout=20)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            body = response.read(MAX_BYTES + 1)
            record.update(status=response.code, effective_url=response.geturl(),
                          content_type=response.headers.get('Content-Type', ''),
                          x_robots_tag=response.headers.get('X-Robots-Tag', ''))
            if len(body) > MAX_BYTES:
                record['error'] = 'Response exceeds audit size limit'
                return record, ''
            return record, body.decode(response.headers.get_content_charset() or 'utf-8', errors='replace')
    except (OSError, ValueError) as error:
        record['error'] = str(error)
        return record, ''


def normalized(url):
    return unquote(url).rstrip('/')


def audit(sites, extra_pages, limit):
    resources, pages, urls, inventory_errors = [], [], [], []
    allowed = set(sites)
    for site in sites:
        robot, text = fetch(site + '/robots.txt')
        robot['sitemap_directive_present'] = any(line.lower().startswith('sitemap:') for line in text.splitlines())
        robot['daum_verification_present'] = '#DaumWebMasterTool:' in text
        resources.append(robot)
        if robot.get('status') != 200 or robot.get('error'):
            inventory_errors.append({'url': robot['url'], 'issue': 'robots unavailable'})
        queue, seen = [site + '/sitemap.xml'], set()
        while queue:
            url = queue.pop(0)
            if url in seen:
                continue
            if len(seen) >= 50:
                inventory_errors.append({'url': url, 'issue': 'Sitemap traversal limit reached'})
                break
            seen.add(url)
            record, body = fetch(url)
            resources.append(record)
            if record.get('status') != 200 or record.get('error'):
                inventory_errors.append({'url': url, 'issue': 'Sitemap unavailable'})
                continue
            try:
                root = ET.fromstring(body)
                kind = root.tag.rsplit('}', 1)[-1]
                if kind not in ('sitemapindex', 'urlset'):
                    raise ValueError('Unexpected sitemap root element')
                locations = [(element.text or '').strip() for element in root.findall('.//{*}loc')]
                record.update(xml_valid=True, kind=kind, locations_count=len(locations))
                for loc in locations:
                    if origin(loc) not in allowed:
                        inventory_errors.append({'url': loc, 'issue': 'Outside requested origins; not fetched'})
                    elif kind == 'sitemapindex':
                        queue.append(loc)
                    else:
                        urls.append(loc)
            except (ET.ParseError, ValueError) as error:
                record.update(xml_valid=False, xml_error=str(error))
                inventory_errors.append({'url': url, 'issue': 'Invalid sitemap'})
    urls = list(dict.fromkeys(urls))
    if len(urls) > limit:
        inventory_errors.append({'issue': 'Page limit reached', 'inventory_count': len(urls), 'checked_limit': limit})
    selected = list(dict.fromkeys(urls[:limit] + extra_pages))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for record, body in pool.map(fetch, selected):
            head = Head()
            head.feed(body)
            record.update(title=head.title, description=head.meta.get('description'), canonical=head.canonical,
                          robots=head.meta.get('robots', ''), jsonld_valid=all(head.ld), in_sitemap=record['url'] in urls)
            issues = []
            if record.get('error'):
                issues.append('fetch failed')
            if record['in_sitemap']:
                if record.get('status') != 200:
                    issues.append('sitemap URL not HTTP 200')
                if 'noindex' in (record['robots'] + record.get('x_robots_tag', '')).lower():
                    issues.append('sitemap URL noindex')
                if len(head.canonical) != 1:
                    issues.append('missing or multiple canonical')
                elif normalized(head.canonical[0]) != normalized(record.get('effective_url', '')):
                    issues.append('canonical differs from effective URL')
                if not head.title:
                    issues.append('missing title')
                if not head.meta.get('description'):
                    issues.append('missing description')
            if not all(head.ld):
                issues.append('invalid JSON-LD')
            record['issues'] = issues
            pages.append(record)
    return {'schema_version': 1, 'checked_at': datetime.now(timezone.utc).isoformat(), 'sites': sites,
            'resources': resources, 'pages': pages, 'summary': {'sitemap_pages': len(urls),
            'checked_pages': len(pages), 'inventory_complete': not inventory_errors,
            'inventory_errors': inventory_errors, 'issues': [{'url': p['url'], 'issues': p['issues']} for p in pages if p['issues']]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', action='append', required=True, help='Origin to audit; repeat for multiple sites')
    parser.add_argument('--page', action='append', default=[], help='Additional page to inspect, within a requested origin')
    parser.add_argument('--max-pages', type=int, default=500)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        sites = list(dict.fromkeys(origin(site) for site in args.site))
        if args.max_pages < 1 or any(origin(page) not in sites for page in args.page):
            parser.error('Use a positive max-pages and extra pages within requested origins')
    except ValueError as error:
        parser.error(str(error))
    report = audit(sites, args.page, args.max_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['summary'], ensure_ascii=False))
    return 1 if report['summary']['issues'] or report['summary']['inventory_errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
