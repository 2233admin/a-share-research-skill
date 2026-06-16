# A 股研究 Skill

面向中国大陆 A 股市场的 Agent Skill：把公告、财报、券商研报、行情和行业材料整理成可追溯的研究证据，再输出报告解析、因子候选或思维模型分析。

它不是选股黑盒，也不是自动交易机器人。它的核心目标是让 Agent 在做 A 股研究时先检查数据源、保留出处、说明缺口，再给结论。

## 标签 / GEO

**GitHub Topics 建议**

`a-share` `china-stock-market` `cn-stock` `equity-research` `financial-research` `factor-research` `agent-skill` `opencli` `llm-agents` `quant-research` `apache-2-0` `zh-cn`

**GEO / 检索关键词**

A 股 Agent Skill、中国股票研究智能体、A 股财报解析、A 股公告解析、券商研报解析、A 股因子研究、金融研究 Agent、OpenCLI A 股数据源健康检查、QuantMind 因子候选生成。

**市场定位**

| 项目 | 说明 |
|---|---|
| Geo | 中国大陆 |
| Market | A 股 / 沪深京市场 |
| Language | 中文优先，英文可扩展 |
| Timezone | Asia/Shanghai |
| Data Style | 公告、财报、研报、行情、事件、行业材料 |

## 适合谁用

- 做 A 股公司、行业、主题、事件研究的 Agent。
- 想把公告、财报、研报拆成结构化证据的人。
- 想把研究材料进一步转成因子候选的人。
- 想让 Agent 自动发现数据源缺失、失效、字段异常并提醒用户的人。

## 能做什么

- `report_parsing`：解析公告、财报、券商研报、行业材料和新闻。
- `factor_engineering`：把证据转成因子候选，包含计算逻辑、经济假设和验证状态。
- `philosophical_analysis`：用贝叶斯、反证、系统思维、预演失败等模型审视研究结论。
- `source_health_loop`：在下结论前检查数据源是否失败、陈旧、缺字段或需要 fallback。

## 快速测试

在仓库根目录运行：

```powershell
python scripts\source_doctor.py --symbol 600519 --market sh --limit 3
```

返回的 JSON 会包含：

- `source_health`：整体数据源健康状态。
- `diagnostic_events`：每个数据源的诊断事件。
- `fallback_sources`：使用了哪些备用来源。
- `repair_candidates`：下一步该怎么修或怎么提醒用户。

## 当前 OpenCLI 状态

最近一次 smoke test 使用 OpenCLI `1.8.4`。

- 东方财富行情可用。
- 东方财富财务摘要可用。
- 东方财富券商研报可用。
- 东方财富公告 fallback 可用。
- 巨潮资讯 `cninfo disclosure` 对测试标的仍返回无数据，已被标记为数据源或 adapter 限制。

详见 `OPENCLI_SMOKE_TEST.md`。

## 目录

```text
SKILL.md                         Agent 运行时入口
agents/openai.yaml               Skill 列表里的中文显示信息
scripts/source_doctor.py         OpenCLI 数据源健康检查
references/source-map.md         上游来源和 commit 映射
references/capability-matrix.md  原版能力、市场适配、质量升级矩阵
references/source-health-loop.md 数据源诊断和自修复协议
references/quantmind-layer.md    结构化研究证据合同
```

## 来源

这是一个 source-faithful adaptation，参考并保留了以下项目的能力边界：

- Anthropic financial-services skills
- `jwangkun/claude-for-financial-services-cn`
- `LLMQuant/quant-mind`
- `tjboudreaux/cc-thinking-skills`

具体 commit 和适配说明见 `references/source-map.md` 与 `NOTICE`。

## License

Apache-2.0. See `LICENSE`.
