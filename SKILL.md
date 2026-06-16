---
name: a-share-research-skill
description: Market-specific financial research skill for mainland China A-share analysis. Use when Codex needs to parse A-share filings, earnings reports, broker research, industry notes, announcements, market data, factor hypotheses, valuation work, catalyst tracking, or market-structure narratives with source-traced evidence and China-market conventions.
---

# A-share Research Skill

## Operating Rule

Keep the market boundary first. Treat report parsing, factor engineering, and philosophical analysis as output modes inside A-share research, not separate top-level skills.

Preserve source-project capability before optimizing. When adapting a workflow, check `references/source-map.md` and `references/capability-matrix.md` so the result remains traceable to pinned upstream snapshots.

## Output Modes

Choose one mode explicitly when the user has not specified the expected output:

- `report_parsing`: extract, normalize, and explain content from filings, announcements, broker reports, earnings material, news, papers, or datasets.
- `factor_engineering`: turn structured research evidence into factor candidates with evidence, calculation logic, economic hypothesis, and validation status.
- `philosophical_analysis`: apply explicit thinking models to examine assumptions, causality, uncertainty, failure modes, and market narratives.

## Workflow

1. Identify the research market as A-share and reject crypto-style assumptions unless the user is comparing markets.
2. Select the output mode and load only the relevant reference files.
3. Run `scripts/source_doctor.py` when live data sources are needed or when prior source health is unknown.
4. Gather or inspect source evidence before forming conclusions.
5. Run the Source Health Loop: detect failed, stale, partial, or suspicious sources and surface diagnostic events before conclusions.
6. Apply the QuantMind Layer pattern: convert raw or semi-structured material into structured research evidence.
7. If producing factor work, output factor candidates with the required factor contract.
8. If applying thinking models, use progressive disclosure: start with the smallest relevant model subset and expand only when the question requires it.
9. State data freshness, source limitations, fallback sources, repair candidates, and validation status.

## Factor Candidate Contract

Every factor candidate must include:

- `factor_name`
- `market`
- `asset_universe`
- `source_evidence`
- `calculation_logic`
- `economic_hypothesis`
- `validation_status`

Do not present a candidate factor as a final trading signal without validation evidence.

## References

- `references/source-map.md`: pinned upstream source repositories and capability provenance.
- `references/capability-matrix.md`: source parity, market adaptation, and quality upgrade checklist.
- `references/data-source-policy.md`: A-share data-source tiers, fallback rules, and freshness handling.
- `references/source-health-loop.md`: diagnostic events, user warnings, fallback handling, and self-repair candidates for data-source problems.
- `references/quantmind-layer.md`: structured evidence extraction contract inspired by QuantMind.
- `references/research-output-modes.md`: output mode definitions and selection rules.
- `references/thinking-model-adapter.md`: progressive disclosure rules for thinking models.
- `scripts/source_doctor.py`: executable OpenCLI source health checker that emits diagnostic events and repair candidates.
