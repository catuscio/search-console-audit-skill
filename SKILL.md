---
name: search-console-audit
description: Audit website search-engine registration, sitemaps, URL indexing and GA4 measurement across Google, Bing, Naver and Daum; compare saved evidence and produce a consolidated status report.
---

# Search Console Audit

Use this skill for search registration follow-up, indexing audits, GA4 setup verification, or a consolidated search-health report. Establish the requested domains from the user or project config. Do not expand to other sites belonging to the account.

## Audit workflow

1. Read the latest saved report, distinguishing historical facts from current observations. Record timestamps and evidence sources. A stale error note must not override newer confirmed success.
2. Run `scripts/audit_public.py --site https://example.com --output /absolute/report.json` for each requested origin (repeat `--site`). It reads robots.txt, sitemaps and their HTML pages without changing the site. Use `--page` for additional search/noindex/404 routes. Resource failures and incomplete inventories must be reported, not interpreted as zero pages.
3. Query official Google/Bing APIs when an existing authorized integration is available. Otherwise inspect owner consoles through the user's preferred browser. For Naver/Daum use the console UI unless a supported integration is available. Follow [provider guidance](references/providers.md). Do not enable APIs or create credentials as part of a read-only audit.
4. Keep ownership, sitemap submission/processing, URL request acceptance, crawl, index status, search performance, and site visits separate. Sitemap discovery counts are not indexed-page counts. Console request-history records are not crawl confirmations. Do not use `site:` search counts as an authoritative inventory.
5. Compare current evidence with prior results. Report confirmed regressions, resolved issues, pending external review, unknown values, and last successful observation. Never replace unavailable data with 0 or success.
6. Save a consolidated JSON report using [the report contract](references/report.md), then a concise site-by-provider summary. Verify fixes in deployed responses and console UI before marking resolved.

## Registration and retry mode

Registration, submissions, code changes and account configuration require authorization in the current task. If authorized, inspect existing registrations before creating duplicates. Only submit public, indexable URLs with successful responses and matching canonical URLs; exclude private, unlisted and search-result pages unless the site's intended indexing policy explicitly says otherwise.

Submit each pending URL once per run. Confirm the accepted UI response. Stop the batch immediately on quota, excessive-call, duplicate/ambiguous rejection, CAPTCHA, or authentication failure; retain the remaining inventory. Do not bypass limits, solve CAPTCHA automatically, or repeatedly poll an unchanged request.

For a PIN/password owned by the user, prepare the URL and ask the user to log in directly. Never read, print, save or include the secret in browser tasks or reports. Do not regenerate site verification codes merely to switch sessions. Daum login is shared between site tabs: verify the connected host before every batch, and only switch through ordinary logout/login when needed.

## GA4 mode

Read [GA4 guidance](references/ga4.md) for setup or measurement checks. Reuse existing properties/streams and avoid duplicate tags. Preserve unrelated analytics accounts and past data. Ask only for essential missing account access or a materially different measurement choice.

## Browser preference

Use the user's preferred browser controller. When Aside is preferred, use `aside` (or `~/.local/bin/aside`): read `aside guide`, prefer `aside exec` with concrete authorized scope, and read `aside guide repl` before direct control. Keep Guard permissions and existing profile/settings. Delegate only the authorized domain/provider scope. Monitor the task, check its saved evidence, and report progress during long runs.

## Completion

Separate completed work from external waiting. Link reports and state the number of checked URLs, submitted requests, freshly confirmed indexed URLs, and unverified URLs. Keep credentials out of skills and reports. Do not promise future checks or schedule tasks unless requested.
