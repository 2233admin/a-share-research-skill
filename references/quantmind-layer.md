# QuantMind Layer

The QuantMind Layer turns raw or semi-structured source material into structured research evidence before report writing, factor construction, or philosophical analysis.

## Inputs

- Company filings and exchange announcements
- Broker reports and industry notes
- Financial statements and market datasets
- News, policy releases, and event calendars
- Academic papers, blogs, and other research material

## Evidence Unit Contract

Use this contract when normalizing source material:

- `source_id`: stable local identifier or URL/path
- `source_type`: filing, announcement, broker_report, dataset, news, paper, note, or other
- `market`: `a-share`
- `entity`: company, sector, index, policy body, or asset universe
- `period_or_timestamp`: report period, filing date, event date, or data timestamp
- `extracted_facts`: facts directly supported by the source
- `interpreted_claims`: analysis derived from facts
- `source_limitations`: known gaps, stale data, provider limitations, or disagreement
- `downstream_uses`: report_parsing, factor_engineering, philosophical_analysis, or multiple

## Use Rules

- Build evidence units before strong conclusions.
- Keep source facts separate from interpreted claims.
- For factor work, transform evidence units into factor candidates only after the calculation logic and economic hypothesis are explicit.
- For report parsing, preserve document structure when it carries meaning, such as management discussion, financial tables, risk factors, and segment disclosures.
- For philosophical analysis, ground assumptions and failure modes in evidence units rather than unsupported narrative.
