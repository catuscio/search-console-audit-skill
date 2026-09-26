# Search Console Audit

A Codex skill for checking Google, Bing, Naver and Daum registration, sitemap processing, URL indexing and GA4 measurement. Reports separate request acceptance from actual crawling and indexing, preserve observation timestamps, and compare current evidence with previous results.

## Install

Clone this repository into `~/.codex/skills/search-console-audit`, then start a new Codex session. Invoke `$search-console-audit`, or ask to audit your sites' search registration and analytics.

## Public audit helper

Python 3.10+, standard library only:

```sh
python3 scripts/audit_public.py --site https://example.com --output /tmp/search-audit.json
```

Repeat `--site` for related sites. Add `--page` for routes outside the sitemap. The helper reads public endpoints; authenticated provider checks use official APIs or your preferred browser. Quota failures stop submission batches. Credentials and account-specific data do not belong in this repository.
