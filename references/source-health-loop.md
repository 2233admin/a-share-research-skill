# Source Health Loop

The skill must not silently ignore data-source failures. Every source call should produce evidence or a diagnostic event that the agent can use to warn the user and choose a safe fallback.

## Diagnostic Event Contract

Use this contract when a source is called:

- `source_name`: Wind, iFind, AkShare, Eastmoney, CNInfo, exchange announcement, broker report, or other
- `source_tier`: Tier-0, Tier-1, Tier-2, Tier-3, or unknown
- `command_or_access_path`: command, API, URL, file path, or manual source
- `entity`: ticker, company, sector, index, or universe
- `requested_fields`: requested data fields or document type
- `status`: pass, fail, stale, partial, suspicious
- `observed_at`: local run time or source timestamp
- `data_timestamp`: market timestamp, report period, filing date, or publication date
- `failure_reason`: missing_credentials, no_data, timeout, schema_drift, adapter_error, stale_data, rate_limit, source_disagreement, or none
- `fallback_used`: source name or none
- `user_message`: concise warning or confirmation request to show the user
- `repair_candidates`: list of safe repair actions

## Required Loop

1. Run the highest-priority relevant source from `data-source-policy.md`.
2. Validate that output is non-empty, recent enough, and contains the expected fields.
3. If the source fails or looks suspicious, emit a diagnostic event.
4. Try the next safe fallback source if one exists.
5. Tell the user when a key source failed, when a fallback was used, or when a result is incomplete.
6. Propose repair candidates, but do not perform credential, paid-service, browser-profile, or write-side repairs without confirmation.

## Executable Doctor

Run the source doctor before analysis when live source health is unknown:

```bash
python scripts/source_doctor.py --symbol 600519 --market sh --limit 3
```

The script emits:

- `source_health`: summary status, failed sources, fallback sources, user warning, and repair candidates
- `diagnostic_events`: one event per checked source

If `source_health.status` is `partial` or `fail`, show the user the warning before relying on conclusions.

## A-share Repair Candidates

| Failure | Agent-visible message | Safe repair candidates |
|---|---|---|
| Missing Wind key | Wind is configured as Tier-0 but credentials are unavailable. | Ask user for `WIND_API_KEY`; fall back to iFind/AkShare/public sources. |
| Missing iFind token | iFind is configured as Tier-1 but credentials are unavailable. | Ask user for `IFIND_AUTH_TOKEN`; fall back to AkShare/public sources. |
| CNInfo no data | CNInfo returned no disclosure rows for the requested symbol or window. | Retry with a wider date window; try Eastmoney announcements; ask user for the target disclosure category. |
| Eastmoney schema drift | Eastmoney output is missing expected fields. | Re-run with trace; inspect adapter help; try alternative Eastmoney command; file adapter issue. |
| Stale financials | Latest financial summary is older than expected. | Warn user; fetch announcements; ask whether stale data is acceptable. |
| Source disagreement | Sources disagree on a key figure. | Preserve both values; cite both; ask whether to prefer paid data, exchange filing, or public source. |

## User Warning Template

```json
{
  "source_health": {
    "status": "partial",
    "failed_sources": ["CNInfo disclosure"],
    "fallback_sources": ["Eastmoney announcement"],
    "user_warning": "CNInfo returned no data for 600519 in the requested window, so I used Eastmoney as fallback. Treat disclosure coverage as incomplete.",
    "repair_candidates": ["retry wider date window", "try disclosure category filter", "run adapter trace"]
  }
}
```
