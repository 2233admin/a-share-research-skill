# A-share Research Skill

Market-specific agent skill for mainland China A-share research.

This repository packages a source-traced research workflow for A-share filings, announcements, broker research, market data, factor hypotheses, valuation work, catalyst tracking, and narrative analysis.

## What It Does

- Keeps the top-level boundary at the research market: A-share.
- Preserves upstream financial-services capabilities before adapting them.
- Converts raw or semi-structured market material into structured research evidence.
- Supports three output modes: `report_parsing`, `factor_engineering`, and `philosophical_analysis`.
- Emits source-health diagnostics before conclusions when live data is required.
- Treats factors as candidates until validation evidence exists.

## Quick Start

Use the skill root directly from an agent runtime that supports `SKILL.md`.

For local source checks:

```powershell
python scripts\source_doctor.py --symbol 600519 --market sh --limit 3
```

The source doctor returns JSON with:

- `source_health`
- `diagnostic_events`
- fallback source usage
- repair candidates for missing, stale, partial, suspicious, or failed sources

## Current OpenCLI Status

The latest smoke test used OpenCLI `1.8.4`.

- Eastmoney quote, financial summary, broker research, and announcement fallback are usable.
- CNInfo disclosure still returns no data for the tested symbol and is treated as a source or adapter limitation.
- See `OPENCLI_SMOKE_TEST.md` for evidence and score.

## Provenance

This skill is a source-faithful adaptation inspired by:

- Anthropic financial-services skills
- `jwangkun/claude-for-financial-services-cn`
- `LLMQuant/quant-mind`
- `tjboudreaux/cc-thinking-skills`

See `references/source-map.md` and `NOTICE` for pinned source mapping and attribution.

## License

Apache-2.0. See `LICENSE`.
