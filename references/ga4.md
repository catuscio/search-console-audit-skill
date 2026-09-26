# GA4 setup and verification

Inventory existing properties, streams, measurement IDs, installed scripts, deployment variables and historical use before choosing a structure. For related sites whose combined user journeys matter, one property and one web stream with the same G-ID can support host-name comparisons; unrelated products or independent ownership may justify separate properties. Preserve existing history and explain any new destination.

Use the user's timezone and reporting currency. Check enhanced measurement, retention, data filters and referral/domain settings. Do not enable advertising signals, Ads links, User-ID, destructive active filters, paid exports or unrelated integrations without the task requiring them. Keep internal/developer filters in testing until their predicates are validated. Do not guess a user's permanent public IP.

For SPAs choose exactly one page-view mechanism: Google history-based enhanced measurement, or manual route events with the matching automatic behavior disabled. Confirm initial load and client navigation once each. Avoid collecting sensitive query values or form content; inspect actual search and eligibility inputs before enabling form/search features.

Keep configurable public measurement IDs separate from credentials. Public build variables must reach the image build, not just the running container. In Coolify, check whether build-time values are delivered as standard build arguments or BuildKit secret mounts: a Dockerfile ARG alone cannot read a secret mount. If the app needs secret delivery for other variables, support an optional GA-ID mount with an ARG fallback rather than switching all build variables to public arguments. Optional tracking must remain absent when no ID is configured. Never place a maintainer's ID into a reusable open-source template.

Verify three layers independently:
1. Production HTML/JS has the intended G-ID once and no legacy duplicate tag.
2. Browser sends successful collect requests to that ID: initial page view, client navigation, correct page location/title and shared cookie domain where applicable.
3. GA Realtime/DebugView accepts events. If ingestion isn't visible yet, report transport verified and ingestion pending; do not claim full measurement success.

Parse collection requests inside the browser or collector and return only measurement ID, event name, page location/title and response status. Raw collect URLs include user/session identifiers; do not dump or persist them. A cross-origin Resource Timing status of 0 means status is hidden, not success or failure. Use console ingestion evidence or a controller that exposes response status. Wait for DOM readiness and the tag/event, rather than every image or external asset; stop unchanged browser timeouts and use the user-authorized fallback.

Use host name to distinguish sites and source/medium for search traffic. GA sessions are not Search Console clicks; do not add them together. Standard reports can lag; label observation windows.

Official references:
- https://support.google.com/analytics/answer/9679158
- https://support.google.com/analytics/answer/10071811
- https://developers.google.com/analytics/devguides/collection/ga4/single-page-applications
- https://support.google.com/analytics/answer/7667196
