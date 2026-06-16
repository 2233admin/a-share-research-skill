# Data Source Policy

Use source tiers to make A-share evidence auditable and to avoid silently mixing paid, public, and stale data.

## Source Tiers

| Tier | Source | Use for | Notes |
|---|---|---|---|
| Tier-0 | Wind | Full-market professional data across A-shares, funds, macro, indices, bonds, funds, broker research, and announcements when credentials are available. | Requires `WIND_API_KEY` or equivalent configured access. |
| Tier-1 | iFind | A-share fundamentals, market data, funds, bonds, macro, indices, and sector data when credentials are available. | Requires `IFIND_AUTH_TOKEN` or equivalent configured access. |
| Tier-2 | AkShare | Public/open fallback for stocks, funds, industries, indices, and public market datasets. | Prefer when paid credentials are unavailable or when an open-source reproduction path is needed. |
| Tier-3 | Public announcements and financial news | Exchange announcements, company filings, regulator releases, financial media, and public research context. | Use to verify events and narratives; mark source and timestamp. |

## Fallback Rules

1. Prefer the highest tier that is available, relevant, and fresh enough for the task.
2. If a paid source is unavailable, say so, emit a diagnostic event using `source-health-loop.md`, and use the best open fallback.
3. Do not hide provider differences; note when two sources disagree and emit a source-disagreement diagnostic.
4. Do not treat broker research or news as fact without distinguishing source fact from analyst interpretation.
5. Never include user secrets or API keys in outputs, examples, or committed files.

## Freshness Notes

For market data, include observation date or timestamp. For financial statements, include report period and filing date. For catalyst work, include event date and source publication date when available.
