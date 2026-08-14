# mathmodel-team-skill · 数学建模团队工作流（融合版）

> 当前版本：**v1.0.3**（2026-08-14）

融合 **math-modeling-skill v1.2.0**（[XiaoMaColtAI/math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill)）与 **MathModelAgent**（skills 子目录）两套 Claude Code 数学建模技能，按"同质内容优先科学准确、全面及时"择优合并。

## 一、融合了什么

| 来源 | 贡献 |
|---|---|
| **math-modeling-skill v1.2.0** | 三角色细化规范（建模手/编程手/论文手）、M1/P1/P2/W1/W2 五道独立 Subagent 门禁、主张-证据链与复现清单机制、六件工具（figure/docx/latex/pdf/paper_search/xlsx）、Subagent 调度与可选协作 |
| **MathModelAgent** | 六阶段细分（分析建模→编程→drawio→写作→验收）、`math_modeling_norms.md` 领域知识库（20+ 小节）、17 个竞赛论文模板（14 中 + 3 英）、11 个科研图模板、Typst 完整参考库、doctor 环境检查 |

**融合新增**：
- `references/共享契约/`——双解题手并行模式的唯一事实源（题目分析/术语/假设/符号/数据口径/结果锚点六件模板）；
- 融合入口 `SKILL.md` 的双解题手并行工作流；
- 本队机制（v1.0.1 起）：`references/竞赛要求.md`（国赛弹性需求 + 硬性要求）、`references/决策确认机制.md`（关键决策 1.是/2.否/3.其他 用户确认）、`references/分工建议.md`（依赖判定 → 协同/独立模式 → 实力分配）、`references/求解报告模板.md`（每问求解后的辅助报告）；
- 本队资料（v1.0.2+）：`references/课件/`（备赛课件全量同步并 md 化，**模型使用及论文写作第一优先参考、冲突以课件为准**；含 `数据处理与预测模型/`、`优化模型与评价模型/` 分类与 `README.md` 索引）、`tools/pdf-ocr/`（四引擎 OCR，影印版题面）、`stages/5writing` 官方内置 Skills 调用登记（nature-*/ml-paper-writing/dataviz 等，仓库自足工具优先）；
- 本队资料（v1.0.3）：`references/论文格式规范2026.md`（当届官方格式全文，电子版硬性要求）、`references/摘要写作规范.md`（国一实例逐条印证）、`references/流程图/`（流程图模板规范 + 模板图）、`references/竞赛要求.md` 排版硬性细节（公式大括号/下标规范/图表标题）；`CHANGELOG_UPSTREAM.md` 保存上游历史，`CHANGELOG.md` 只记本队条目。

## 二、为什么融合

两套体系各有强项，同质部分存在重叠：

- **可视化**：tools/figure 的 Nature 图表契约 + 数据剖析选图 + 三层自检，远强于 3coding-visual 的简单绘图规则 → 契约以 tools/figure 为唯一入口，3coding 负责流程与产物结构。
- **知识库**：math_modeling_norms.md（20+ 小节）覆盖且更新于建模手"常见模式" → 后者降级为速查。
- **论文**：5writing 双引擎 + 17 竞赛模板 + typst-author 参考库，叠加论文手的中文科技写作规范/自审框架。
- **质检**：五道 Subagent 门禁 + 6verity 脚本化终检互补叠加。

原两套目录原样保留（未改写），内部相对引用不受影响，可随时回退。

## 三、两种运行模式

### 1. 双解题手模式（默认，本队分工）

两人按**子问题**分工（如 A=Q3/Q4、B=Q1/Q2），不同于传统建模手/代码手/论文手三角色：

```
阶段0 统一契约（共同冻结，只读；M1 独立质检）
阶段1 并行求解（各自工作区；P1/P2 由独立质检 Subagent 验收——线下协作互不熟悉对方工作，互审省略）
阶段2 结果锚点对账（数值交叉核对）
阶段3 集中合稿（W1 证据大纲 → 正文 → W2）
阶段4 终检（6verity）
```

### 2. 单人模式

按六阶段顺序全流程：1start → 2analysis-modeling → 3coding-visual → 4drawio → 5writing → 6verity，五道门禁由独立 Subagent 承担。

## 四、安装

```bash
# 方式一：直接复制到 Claude Code skills 目录
cp -r mathmodel-team-skill <skills目录>/mathmodel-team

# 方式二：作为 Git 子目录使用（推荐，便于更新）
git clone <本仓库地址>
```

激活方式：对话中提及"数学建模/建模竞赛"或直接点名 `mathmodel-team`。

## 五、目录结构

```text
mathmodel-team-skill/
├── SKILL.md                  # 融合入口（唯一入口，含双解题手编排与择优映射）
├── stages/                   # MathModelAgent 六阶段（原样搬入，内部引用不变）
│   ├── 1start-mathmodel ~ 6verity / doctor / typst-author
│   ├── mathmodel-figure-templates   # 11 个科研图模板
│   └── _references/math_modeling_norms.md
├── tools/                    # figure / docx / latex / pdf / pdf-ocr / paper_search / xlsx
├── references/
│   ├── roles/                # 建模手 / 编程手 / 论文手 三角色规范（上游遗留，仅参考）
│   ├── 共享契约/             # 双解题手并行模板（本仓库新增）
│   ├── 课件/                 # 本队备赛课件（第一优先学习资源，冲突以课件为准；含 README 索引与按任务加载表，docx 全量 md 化）
│   │   ├── 数据处理与预测模型/  # 数据预处理/插值/回归/灰色预测 + ARIMA&SARIMA
│   │   └── 优化模型与评价模型/  # 优化三要素/LP/IP/MILP + AHP/TOPSIS/bigM/PuLP
│   ├── 竞赛要求.md / 决策确认机制.md / 分工建议.md / 求解报告模板.md
│   ├── Subagent调度.md / 算法索引.md / README.md
├── assets/ tests/ imgs/ docs/
└── README.md / CHANGELOG.md（本队条目）/ CHANGELOG_UPSTREAM.md（上游历史）/ VERSION
```

## 六、与上游的关系

- 本仓库是两套上游的**只读整合**：`stages/`、`tools/`、`references/roles/` 均未改写正文，仅在 3 处同质文档头部加"融合注记"（常见模式/MATLAB规范/3coding-visual）。
- 上游更新时，可用 `diff` 或直接重新复制对应目录，融合注记与共享契约为本仓库独有内容。

## 七、许可证与致谢

- math-modeling-skill：见上游仓库
- MathModelAgent：见上游仓库
