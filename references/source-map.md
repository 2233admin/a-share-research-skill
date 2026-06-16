# Source Map

This skill follows source-faithful adaptation. Source snapshots are pinned in `C:\c\Users\Administrator\projects\financial-skill-sources\SOURCE_SNAPSHOTS.md`.

## Pinned Sources

| Source | Commit | Role in this skill |
|---|---|---|
| `anthropics/financial-services` | `4bbabc7cd1a474c1667fa05a2bfe58e411dcf9c1` | Reference plugin architecture, financial research workflows, modeling/reporting capability parity. |
| `jwangkun/claude-for-financial-services-cn` | `59e97ee6683391a05ce6c69502a0fd16bbce4690` | A-share market localization, China data-source priorities, CN financial terminology and research conventions. |
| `LLMQuant/quant-mind` | `8e218884a6cec3122ba42f9fa2277d593b907361` | QuantMind Layer pattern for interpreting source material into structured research evidence. |
| `tjboudreaux/cc-thinking-skills` | `0313ee0d476bf9db2c38ad8bd11d9933a61350d4` | Thinking Model Adapter pattern and progressive disclosure for explicit reasoning models. |

## Adaptation Rules

- Preserve useful source capability before simplifying the skill.
- Cite the source row when adding or changing a capability derived from an upstream project.
- Record deliberate omissions in `references/capability-matrix.md`; do not leave omissions implicit.
- Prefer adapted instructions over large verbatim copied passages.

## Capability Trace

| Local capability | Primary source | Adaptation note |
|---|---|---|
| Research output modes | `anthropics/financial-services` | Consolidates equity research, financial analysis, and report-writing capabilities into market-local modes. |
| Earnings analysis and preview | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Keep original earnings workflows, adapt for A-share calendar, disclosure style, China financial statements, and local broker-note conventions. |
| Initiating coverage | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve staged research/modeling/valuation/report assembly workflow, adapt peers, valuation norms, and market language for A-share. |
| Model update | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve estimate refresh and model-change flagging, adapt to A-share announcements, guidance scarcity, and China statement formats. |
| Sector overview and thematic research | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve sector landscape workflow, adapt to domestic industry chains, policy cycles, and local classification systems. |
| Thesis tracker and catalyst calendar | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve thesis/catalyst monitoring, adapt catalysts to earnings dates, regulatory events, policy releases, conferences, and product launches. |
| Comparable company analysis | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve comps methodology, adapt to domestic peer selection and A-share multiples such as PE, PB, PS, and sector valuation bands. |
| DCF and 3-statement modeling | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve model-building flow, adapt CAS/China GAAP conventions, local financial statement formats, and China government bond rate inputs. |
| Excel/model audit and data cleaning | `anthropics/financial-services`, `jwangkun/claude-for-financial-services-cn` | Preserve audit/clean-data workflows, adapt to Chinese financial labels, statement formats, and A-share data quirks. |
| Market data access policy | `jwangkun/claude-for-financial-services-cn` | Use Wind, iFind, AkShare, and China news/public announcements as explicit tiers with fallback and credential handling. |
| Structured evidence extraction | `LLMQuant/quant-mind` | Use source/parser/workflow/structured knowledge concepts to turn reports and data into evidence units before analysis. |
| Thinking model routing | `tjboudreaux/cc-thinking-skills` | Use selected thinking frameworks as progressive-disclosure checks, not as accuracy guarantees. |
