# Darwin Scorecard

Date: 2026-06-16
Eval mode: `dry_run + opencli_1.8.4_smoke`

This score uses the Darwin Skill 8-dimension rubric. Runtime-neutral red-light scan found no matches in `SKILL.md`.

## Score

| Dimension | Weight | Rating | Weighted |
|---|---:|---:|---:|
| Frontmatter quality | 8 | 8.5 | 6.8 |
| Workflow clarity | 15 | 8.0 | 12.0 |
| Boundary conditions | 10 | 7.5 | 7.5 |
| Checkpoint design | 7 | 6.5 | 4.6 |
| Instruction specificity | 15 | 8.0 | 12.0 |
| Resource integration | 5 | 9.0 | 4.5 |
| Overall architecture | 15 | 8.5 | 12.8 |
| Tested performance | 25 | 8.4 | 21.0 |
| **Total** | **100** |  | **81.2** |

## Read

The A-share skill is structurally sound and testable. It has a good market boundary, source map, capability matrix, data-source policy, source-health loop, executable source doctor, QuantMind evidence contract, and validated OpenCLI paths for quote, financial summary, broker research, retry-aware CNInfo diagnostics, and fallback diagnostics.

## Main Weaknesses

- CNInfo disclosure smoke test still fails in OpenCLI `1.8.4`, but `scripts/source_doctor.py` now records the wide-date retry, detects empty-row anomalies, uses Eastmoney fallback, and emits repair candidates.
- Checkpoint design is light: the skill chooses output mode but does not clearly pause for user confirmation on high-impact decisions such as valuation assumptions or incomplete source coverage.
- Output templates are still sparse; factor candidates have a contract, but report parsing and philosophical analysis need examples.

## Priority Fixes

1. Add fixture tests for source diagnostic events and repair candidates.
2. Add output templates for `report_parsing`, `factor_engineering`, and `philosophical_analysis`.
3. Add checkpoint language for valuation assumptions, source gaps, and publishing-ready outputs.
