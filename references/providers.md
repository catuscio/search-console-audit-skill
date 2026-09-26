# Provider evidence

- Google: verify owner and sitemap status in Search Console. URL Inspection API reports Google's stored index state, not a live indexing request. Search Analytics reports impressions/clicks/CTR/position, which are distinct from GA visits. Inspect pending/new/changed URLs first. Record exactly which URLs were checked.
- Bing: verify sitemap processing/errors and available index/search metrics. Use the Webmaster API if already configured. A submission response alone does not prove indexing.
- Naver: ownership, sitemap submission, request history and diagnosis are separate observations. The published crawl-request API is for approved partners; do not assume it is available to ordinary accounts.
- Daum: directory/external-blog registration and Webmaster crawling are separate workflows. Preserve accepted applications awaiting review. Confirm the dashboard's connected domain, response code and collection availability. A blank submission input is not proof that a previously accepted sitemap was deleted. Request acceptance is not an indexed URL count.

Official references (verify current capabilities when implementing):
- https://developers.google.com/webmaster-tools/v1/api_reference_index
- https://learn.microsoft.com/en-us/bingwebmaster/
- https://searchadvisor.naver.com/guide/crawl-request-api
- https://webmaster.daum.net/

When the provider is unavailable, record unavailable plus last known state and timestamp. Do not infer an API is supported from undocumented browser network endpoints.
