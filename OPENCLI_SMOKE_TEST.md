# OpenCLI Smoke Test

Date: 2026-06-16
OpenCLI: `1.8.4`

## Commands

```powershell
opencli eastmoney stock-quote --code 600519 --market sh -f json
opencli eastmoney bbsj-summary --code 600519 --limit 3 -f json
opencli eastmoney research --code 600519 --type stock --limit 3 -f json
opencli cninfo disclosure --symbol 600519 --limit 3 -f json
opencli cninfo disclosure --symbol 600519 --startDate 20250101 --endDate 20260616 --limit 3 -f json
python scripts/source_doctor.py --symbol 600519 --market sh --limit 3
```

## Result

| Check | Status | Evidence |
|---|---|---|
| Market quote | Pass | Eastmoney returned Guizhou Moutai quote: price `1291.91`, change `1.01%`, amount `6477910214`. |
| Financial summary | Pass | Eastmoney returned report periods `2026-03-31`, `2025-12-31`, `2025-09-30` with revenue, net profit, and EPS. |
| Broker research | Pass | Eastmoney returned three recent reports with publish date, broker, researcher, rating, title, and PDF URL. |
| CNInfo disclosure | Fail | `cninfo disclosure returned no data` for `600519`; the wide-date retry from `20250101` to `20260616` also returned no rows. |
| CNInfo keyword anomaly | Fail | `--keyword 贵州茅台` returned rows with expected fields present but empty, so this is treated as an adapter/schema anomaly rather than usable evidence. |
| Source doctor | Pass with partial health | Script emitted `status: partial`, identified `CNInfo disclosure` as failed, recorded the wide-date retry in `retry_attempts`, used `Eastmoney announcement` fallback, and proposed repair candidates. |

## Contract Fit

- Can produce `report_parsing` from quote, financial summary, and broker research evidence.
- Can produce `factor_engineering` candidates from EPS/net-profit growth, broker rating dispersion, valuation once valuation data is added, and event/research freshness.
- Must mark CNInfo disclosure failure and empty-row anomalies as source limitations, not silently ignore them.
- `scripts/source_doctor.py` emits this failure as a diagnostic event with retry attempts, fallback, and repair candidates.

## Score

`8.4 / 10`

The skill contract is usable with OpenCLI today for quote, financial summary, broker-research parsing, and source-health diagnostics. It now detects CNInfo retry failure and empty-row anomalies explicitly. It is not production-complete until source-health diagnostics are fixture-tested, valuation/sector enrichment is added, and regression tests are in place.
