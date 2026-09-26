# Consolidated report contract

Use JSON with `schema_version`, `checked_at` (ISO8601 with timezone), `sites`, `public_audit`, `changes`, and `pending`.

Each site has `origin` and `providers`. Each provider observation stores `status`, `observed_at`, `source` (UI/API/public response), and `evidence` (brief exact UI message or structured result). Unknown values are null with a reason. Preserve last-known observations separately; do not date historical values as new.

Provider fields when available: `ownership`, `sitemap`, `requests` (accepted URLs and remaining URLs), `indexing` (checked URL list/status, coverage count and its source), `performance` (window, impressions, clicks, CTR, position), `registration_review`. GA fields: property/stream/measurement IDs, host scope, settings, transport checks and ingestion confirmation. No passwords, PINs, OAuth tokens, cookies or broad account dumps.

Changes store target, before/after, commit or accepted UI evidence, and deployed verification. Pending entries distinguish user access, provider review/quota, unavailable evidence, and implementation work.

Overview: site rows and provider columns, with separate ownership/sitemap/requests/index states. Show freshness and unknown values explicitly. Link per-URL details and source consoles; do not invent an aggregate SEO score.
