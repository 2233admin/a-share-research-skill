# Capability Matrix

Use this matrix to prevent capability loss while adapting the source projects for A-share research.

## source_parity

| Capability group | Required local coverage |
|---|---|
| Equity research | Earnings analysis, earnings preview, initiating coverage, model update, morning note, sector overview, thesis tracker, catalyst calendar, and idea generation. |
| Financial analysis | Comparable company analysis, DCF, 3-statement model, LBO where relevant, model audit, data cleaning, competitive analysis, deck refresh, xlsx/pptx authoring patterns. |
| China-localized skills | `china-market-data`, `china-comps`, `china-dcf`, `china-3-statement-model`, `china-audit-xls`, `china-clean-data-xls`, `china-earnings-analysis`, `china-earnings-preview`, `china-initiating-coverage`, `china-model-update`, `china-sector-overview`, `china-thesis-tracker`, `china-catalyst-calendar`, `china-morning-note`, `china-idea-generation`. |
| QuantMind layer | Source ingestion, parsing, structured knowledge units, retrieval-ready evidence, batch processing pattern, and natural-language input resolution pattern. |
| Thinking models | Router-style selection, Bayesian update, scientific method, systems thinking, inversion, pre-mortem, second-order thinking, and OODA as the default financial-research subset. |

## market_adaptation

| Adaptation area | Required local behavior |
|---|---|
| Data sources | Follow `references/data-source-policy.md`: Wind first where available, then iFind, AkShare, and public news/announcements as fallback tiers. |
| Market language | Use A-share terminology for boards, tickers, announcements, trading halts, daily price limits, northbound/southbound context, and domestic sector language. |
| Accounting and filings | Treat CAS/China GAAP, Chinese financial statement labels, exchange announcements, and periodic reports as first-class inputs. |
| Valuation | Prefer domestic peer groups, local multiple conventions, China government bond inputs for risk-free rates, and sector valuation bands. |
| Market structure | Consider policy cycles, industry chains, ownership structure, liquidity regime, retail/institutional mix, and event-driven catalysts. |
| Research style | Support China broker-style outputs influenced by CICC, CITIC, Huatai, and local institutional research formats while keeping evidence traceable. |

## quality_upgrade

| Upgrade | Required local behavior |
|---|---|
| Evidence traceability | Every conclusion should point to structured evidence or explicitly state that source support is missing. |
| Source health loop | Every source failure, stale result, partial result, or suspicious output should produce a diagnostic event, user warning, fallback note, and repair candidate. |
| Freshness gate | State data timestamp, report period, filing date, and known data lag when available. |
| Output modes | Support `report_parsing`, `factor_engineering`, and `philosophical_analysis` without treating any one mode as the whole skill. |
| Factor contract | Require the seven-field factor candidate contract before any factor-like output is accepted. |
| Thinking model adapter | Use progressive disclosure and output model labels/checks/risk flags rather than generic long reasoning. |
| Source parity audit | Add omissions to `deliberate_omissions` before removing upstream capability. |

## deliberate_omissions

- None yet. Add a note here before removing any useful upstream capability.
