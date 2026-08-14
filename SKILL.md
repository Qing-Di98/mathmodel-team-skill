---
name: mathmodel-team
description: 数学建模团队工作流（融合版）。当用户要求数学建模、建模竞赛、建模分析、代码求解、结果可视化或生成数学建模论文时使用。融合 math-modeling-skill v1.2.0（三角色规范 + M1/P1/P2/W1/W2 五道 Subagent 门禁 + 六件工具）与 MathModelAgent（六阶段细分 + math_modeling_norms 领域知识库 + 17 竞赛论文模板 + 11 科研图模板 + Typst 参考库）。支持单人全流程，以及按子问题分工的双解题手并行模式（共享契约冻结 → 并行求解 + 独立质检 → 结果锚点对账 → 集中合稿 → 终检）。
---

# 数学建模（团队融合版）

本 Skill 是两套体系的有机融合：**MathModelAgent 六阶段细分**提供阶段边界与领域知识库，**math-modeling-skill v1.2.0** 提供三角色细化规范与五道独立 Subagent 门禁。同质内容按"科学准确、全面及时"择优，两套都不可替代的资产全部保留。生成的论文仅供用户参考，不作为可直接提交的作品。论文结构与格式必须以目标竞赛当届官方规则和官方模板为准，不能用往届经验替代官方要求。

## 融合来源与择优原则

| 领域 | 采用（融合后唯一入口） | 未采用/降级（理由） |
|---|---|---|
| 赛题分析与建模设计 | `stages/2analysis-modeling`（每问：目标/变量/约束/求解法 + 代码任务清单的报告结构） | — |
| 建模理论参考 | `stages/_references/math_modeling_norms.md`（20+ 小节题型/规范知识库，最全面）；`references/算法索引.md` + `assets/*.md`（算法深读） | `references/roles/建模手/references/常见模式.md` 降级为速查（与 norms 五大题型指南同质） |
| 建模前置确认 | `references/roles/建模手/references/前置合同.md`（建模前与用户确认输入/约束/目标） | — |
| 假设管理 | 建模手假设敏感性预检 + `M1` 门禁"假设依据"审查 | — |
| 编程实现 | `stages/3coding-visual`（骨架→逐子问题→结果报告）；`references/roles/编程手/references/工作流程.md`（环境诊断先行） | `MATLAB规范.md` 降级为按需（本队用 Python，保留给 MATLAB 场景） |
| 数据可视化 | `tools/figure`（Nature 图表契约 + 数据剖析选图 + 三层自检 + 18 避坑清单）为**唯一契约**；`stages/mathmodel-figure-templates` 提供 11 个可复用高端模板 | `3coding-visual` 的绘图规则并入 figure 契约，不另立 |
| 非数据图 | `stages/4drawio`（路线图/流程图/架构图，自检清单 + PDF 导出） | — |
| 论文写作 | `stages/5writing`（Typst/LaTeX 双引擎 + 14 中 3 英竞赛模板）；`stages/typst-author`（Typst 参考库）；`references/roles/论文手/`（写作规范/章节模板/自审框架）；`tools/docx`（OMML 公式）、`tools/latex`（哈希绑定）、`tools/pdf` | — |
| 学术检索 | `tools/paper_search`（OpenAlex + AnySearch 双引擎） | — |
| 阶段质检 | `M1/P1/P2/W1/W2` 独立 Subagent 门禁（`references/Subagent调度.md`）+ `stages/6verity` 脚本化终检（writing_check.sh、PDF 逐页视觉） | — |
| 环境检查 | `stages/doctor` | — |
| 官方规则核验/附件盘点/文献调研/原型/对照实现 | `references/Subagent调度.md` 可选协作，默认关闭 | — |
| 影印版/图片题面识别 | `tools/pdf-ocr`（四引擎 OCR，中英文），挂载于 `stages/2analysis-modeling` | — |
| 官方内置 skills（英文写作/润色/检索/引用核验等） | `stages/5writing/SKILL.md`"官方内置 Skills 调用登记"按需调用（nature-*、ml-paper-writing、dataviz 等），仓库自足工具优先 | 平台/开发工具（claude-api、update-config、keybindings 等）与数模领域无关，不纳入 |

## 课件优先（最高优先级学习资源）

**模型使用及论文写作的学习资源，优先参考 `<SKILL_ROOT>/references/课件/`（源：`E:\数模\课件\`）中的资料。** 不同资料的模型术语、模型步骤等若有冲突，**一律以课件为准**——用户学习的就是这份课件，对其有学习记忆和依赖。课件未覆盖的内容才用其他资料补齐，且术语与步骤格式沿用课件风格。课件目录索引与按任务加载表见 `references/课件/README.md`；每个 docx 均有同名 `.md` 提取版，建模与写作前直接检索。

## 强制执行协议

用户明确点名本 Skill 或任务命中本 Skill 时，严格执行以下协议；不要把它降级为建议：

1. 在首次进度更新中回显：已激活本 Skill、`SKILL_ROOT`、`PROJECT_ROOT`、运行模式（单人/双解题手）、目标竞赛与届次、计划读取的模块和工具入口。未确认的官方规则明确标为待核验。
9. **用户全程参与知情（禁止黑箱推进）**：建模（`2analysis-modeling`）与代码（`3coding-visual`）的**每一个关键 Step 结束即按 `references/交互知情机制.md` 向用户汇报**（【Step 结果】【含义】【下一步】三行式，3-5 句，留思考空间）；模型选取、假设取舍、数据口径、参数确定、结果异常处理等关键决策点须用 `决策确认机制.md` 选项（1.是/2.否/3.其他）等用户明确选择后再执行。禁止连续推进多个 Step 后一次性汇报。
10. **云端算力提醒义务**：`3coding-visual` Step 1.5 按 `references/云端算力建议.md` 评估代码阶段工作量；预估运行 ≥30 分钟、需 GPU/大内存、本地环境不满足依赖、数据量大或需并行时，**必须主动提醒用户可在 AutoDL 上跑**并给出公共镜像选择建议（框架→CUDA→Python→预装环境四要素），经用户决策（1.用 AutoDL / 2.本地跑 / 3.其他）后继续。
11. **本仓库修改纪律（评测回归）**：修改本 Skill 仓库的 `SKILL.md`、阶段模块、脚本、模板或 `tests/` 后，必须运行 `tests/` 回归（`python -m unittest discover tests`），全部通过才算修改完成；新增行为须先补充对应评测用例（评测驱动、失败优先），评测未通过时优先简化修改而非叠加规则。
2. 开始每个阶段前，实际读取该阶段的 `SKILL.md`（`stages/` 下各模块或 `references/roles/` 下各角色）；使用 PDF、Excel、论文搜索、DOCX 或 LaTeX 时，再实际读取对应工具的 `SKILL.md`。知道文件路径不等于已经执行。
3. 严格调用模块提供的脚本和模板。已有初始化、转换、编译或校验工具时，禁止为了省时手写替代实现。
4. 把任何校验预警视为未完成。只有当届官方规则或用户明确要求允许偏离时，才能记录"规则来源、偏离项、理由"后继续；不得自行降低篇幅、图表、公式、引用或编译质量目标。
5. 环境缺少引擎、搜索源、渲染器或依赖时，报告阻塞并继续完成仍可验证的部分；禁止静默换工具、跳过验证或用较差产物冒充完成。
6. 运行环境支持 Subagent 且任务会生成或修改固定交付物时，按 `references/Subagent调度.md` 派发独立质检。单人模式按 M1/P1/P2/W1/W2 顺序；双解题手模式的阶段质检与单人模式一致，由**未参与编写的独立质检 Subagent 承担**（线下协作中解题手互不熟悉对方工作，解题手间互审省略），合稿与终检仍按 W1/W2 派发 Subagent。禁止等全流程结束后才首次派发，作者自检不能替代独立验收。除固定质检外，不主动派发其他 Subagent；仅在用户明确启用具体协作任务时按所选范围执行。
7. 交付前运行当前阶段规定的全部完成门禁。任一命令未运行、退出码非零、独立验收未通过、仍有未处理问题或产物在门禁后发生变化时，不得声称"已完成"。
8. 最终回复列出实际读取的入口、实际运行的关键命令、退出码、门禁状态、核心质量指标和仍存在的阻塞；不得只说"已检查"。

## 根目录契约

- `SKILL_ROOT`：本文件所在目录，只读。阶段模块、角色说明、算法资料、脚本和模板都从这里读取。
- `PROJECT_ROOT`：用户题目和项目所在目录，所有新产物只能写入这里。
- 两个根目录必须不同；默认禁止覆盖 `SKILL_ROOT` 内任何文件。
- 输入附件只读。确需修改模板时，先复制到 `PROJECT_ROOT` 再处理。

## 运行模式

由用户在首次对话中确认（默认**双解题手模式**，即本队分工方式）：

- **双解题手模式**：两人按子问题分工（如 A=Q3/Q4、B=Q1/Q2），共享契约冻结后各自独立完成建模→编程→出图，由独立质检 Subagent 验收，锚点对账后集中合稿。适合两解题手（不同于传统建模手/代码手/论文手三角色）。
- **单人模式**：一人按六阶段顺序全流程，五道门禁由独立 Subagent 承担（即 math-modeling-skill 原协议）。

## 双解题手模式工作流（核心）

```
阶段0 统一契约（两解题手共同）
      ├─ 读取题面/附件（tools/pdf、tools/xlsx）
      ├─ 完整读题后给出分工建议（references/分工建议.md）：依赖结构判定（基础问数量 0/1/多个）→ 选择协同/独立模式（完全独立 / 协同+独立混合 / 协同为主）→ 按实力分配（一强一弱）→ 经用户确认
      ├─ 子问题按题号分配（A/B 各认领，边界不重叠；存在基础问时二人共同实现、强者主导，无基础问则完全独立并行）
      ├─ 共同产出并冻结：题目分析报告、术语表格、假设清单、符号表、数据口径（假设与模型选取等关键决策先经用户确认，见 references/决策确认机制.md）
      ├─ 产出：00_契约/（共享，冻结后只读）
      └─ 门禁：M1（独立质检 Subagent 建模终检）
阶段1 并行求解（解题手 A 与 B 独立工作区，物理隔离）
      ├─ 各自：stages/2analysis-modeling（仅自己子问题）
      │        → stages/3coding-visual（代码/结果/数据图，tools/figure 契约）
      │        → stages/4drawio（按需非数据图）
      ├─ 产出：01_<子问题组>_解题手A/、02_<子问题组>_解题手B/
      └─ 门禁：P1、P2 由独立质检 Subagent 承担（只读 + 证据回执，未参与产物编写）
               —— 线下协作中解题手互不熟悉对方工作，解题手间互审省略
阶段2 结果锚点对账（共同）
      ├─ 从两份 RESULTS_REPORT/复现清单提取关键数值 → 结果锚点表（references/共享契约/结果锚点表.md）
      ├─ 交叉核对数值一致性、符号口径、跨题耦合参数（如共享经济参数、λ 等）
      └─ 冲突项由双方协商裁决并记录到契约
阶段3 集中合稿（主笔人）
      ├─ stages/5writing：证据大纲（W1 门禁）→ 正文 → 排版（Word 默认 / LaTeX 按需）
      ├─ 论文手规范：references/roles/论文手/
      └─ 门禁：W1 证据大纲、W2 论文终检
阶段4 终检（stages/6verity）→ VERIFY_REPORT.md
```

### 并行边界（必须遵守）

- 并行窗口**仅限阶段 1**：契约冻结后至锚点对账前。阶段 0/2/3/4 均为单人执行。
- 两解题手在阶段 1 只写**自己工作区**内的文件（代码/结果/图/报告），禁止同时修改任何共享文件。
- 两解题手的思路文档、代码、结果与求解报告对论文手（合稿方）**全程开放**，合稿可读取两份工作区全部产物；基础问的两种独立实现均保留，合稿时择优或合并表述。
- 共享契约文件（`00_契约/`）冻结后默认只读；确需修改必须双方在场并记录变更，且相关 `PASS` 立即失效复验。
- 独立质检只读：质检 Subagent 只看产物、返回证据回执，不修改任一工作区文件；`FAIL` 由被审方修正后复验。
- 不按章节多人并写论文，不分别生成互不共享正文的 Word 与 LaTeX（合稿必须集中）。
- 模型取舍、假设与阈值裁决、跨题耦合、用户授权和最终交付范围不交给任何 Subagent，由两人共同裁决；其中**假设的提出与取舍、模型选取等关键决策须先经用户确认**（`references/决策确认机制.md`：AI 提出方案 + 选项 1.是 / 2.否 / 3.其他），契约冻结以用户确认为前提。

### 双解题手目录骨架

```text
PROJECT_ROOT/
├── 00_契约/
│   ├── 题目分析报告.md          # 阶段0 冻结
│   ├── 术语表格.md              # 阶段0 冻结
│   ├── 假设清单.md              # 阶段0 冻结（含敏感性预检结论）
│   ├── 符号表.md                # 阶段0 冻结（统一符号，防合稿冲突）
│   └── 数据口径.md              # 阶段0 冻结（数据来源/清洗口径/单位）
├── 01_<子问题组>_解题手A/       # 阶段1A：code/ results/ figures/ 复现清单.json、求解报告_qN.md
├── 02_<子问题组>_解题手B/       # 阶段1B：同上
├── 03_合稿/
│   ├── 结果锚点表.md            # 阶段2：两工作区关键数值对账
│   └── paper/                   # 阶段3-4：论文源码 + 编译产物 + VERIFY_REPORT.md
```

## 单人模式工作流

按 MathModelAgent 六阶段顺序执行（各阶段模块不变）：

`stages/1start-mathmodel`（询问偏好/plan.md/todo.md）→ `stages/2analysis-modeling` → `stages/3coding-visual` → `stages/4drawio`（按需）→ `stages/5writing` → `stages/6verity`。

门禁顺序：M1 建模终检 → P1 最小可运行结果 → P2 编程终检 → W1 证据大纲 → W2 论文终检。`P1` 通过后才能全量计算与正式出图，`P2` 通过后进入论文规划，`W1` 通过后才开始长篇正文。`FAIL` 按证据回到对应阶段修正并复验；被审产物发生实质变化时，相关 `PASS` 立即失效。环境不支持 Subagent 时，只能标记为 `BLOCKED` 或受限交付，不得把主 Agent 自检描述为独立通过。

## 路由

| 用户意图 | 加载入口 | 是否要求前一阶段已完成 |
|---|---|---|
| 完整建模（双解题手） | 本 SKILL.md 双解题手模式 → 阶段0 契约 → 阶段1 并行（各自读 `stages/2analysis-modeling` 等） | 按流程 |
| 完整建模（单人） | `stages/1start-mathmodel` → 按六阶段顺序 | 按顺序执行 |
| 只做题目分析、选模型 | `stages/2analysis-modeling` + `references/roles/建模手/SKILL.md`（前置合同/建模设计理论） | 否 |
| 只写代码、跑结果、出图 | `stages/3coding-visual` + `references/roles/编程手/SKILL.md` + `tools/figure/SKILL.md` | 需要题目和可执行的模型说明；缺失时先补齐必要分析 |
| 画流程图 | `stages/4drawio` | 需要建模与结果报告 |
| 只写或修改论文 | `stages/5writing` + `references/roles/论文手/SKILL.md` + `stages/typst-author` | 需要题目、模型、真实运行结果和图表；缺失时回退到对应阶段 |
| 检查论文 | `stages/6verity` | 需要论文产物 |
| 检查建模环境依赖 | `stages/doctor` | 否 |
| 检索文献 | `tools/paper_search/SKILL.md` | 否 |
| 单阶段任务 | 只运行对应门禁，不强制执行完整流程 | — |

## 模块导航

- **阶段模块**（`stages/`）：`1start-mathmodel` 总控、`2analysis-modeling` 分析建模、`3coding-visual` 编程出图、`4drawio` 非数据图、`5writing` 论文（含 `templates/` 17 竞赛模板）、`6verity` 验收（含 `scripts/` 门禁脚本）、`doctor` 环境、`mathmodel-figure-templates` 科研图模板、`typst-author` Typst 参考、`_references/math_modeling_norms.md` 领域知识库。
- **角色规范**（`references/roles/`）：`建模手/`（工作流程/建模设计理论/前置合同/质检清单）、`编程手/`（工作流程/MATLAB规范/质检清单）、`论文手/`（工作流程/章节模板/论文格式规范/LaTeX格式规范/写作规范/英文化工作流/自审框架/论文模板.docx）。
- **共享契约**（`references/共享契约/`）：双解题手模式专用模板（假设清单/术语表/符号表/结果锚点表），阶段 0 使用。
- **调度**：`references/Subagent调度.md`（门禁/可选协作/不委派边界）、`references/算法索引.md`、`references/README.md`（完整导航）。
- **工具**（`tools/`）：`figure`、`docx`、`latex`、`pdf`、`paper_search`、`xlsx`（各含 SKILL.md）。
- **算法资料**（`assets/`）：按需深读。

## 渐进式加载

先读当前阶段的 `SKILL.md`，再按其中"何时加载"表读取所需参考，禁止一次性加载全部资料。

| 当前任务 | 额外读取 |
|---|---|
| 选模型或查算法 | `references/算法索引.md`，再读取相关 `assets/*.md` |
| 搜索论文 | `tools/paper_search/SKILL.md` |
| 读取题目 PDF | `tools/pdf/SKILL.md` |
| 处理 Excel | `tools/xlsx/SKILL.md` |
| 画数据图 | `tools/figure/SKILL.md`（唯一契约）；高端模板查 `stages/mathmodel-figure-templates` |
| 画流程图 | `stages/4drawio/SKILL.md` |
| 生成 Word 论文 | `tools/docx/SKILL.md` |
| 生成 LaTeX 论文 | `tools/latex/SKILL.md` |
| 派发 Subagent 或阶段质检 | `references/Subagent调度.md` |
| 共享契约模板 | `references/共享契约/` |

## 固定交付物

- **双解题手模式**：`00_契约/`（4 件冻结文档）、两工作区各含（代码、结果表、三类图每类≥3 张合计≥9 张且覆盖该解题手全部子问题、`复现清单.json`）、`03_合稿/结果锚点表.md`、论文（Word 默认；LaTeX 仅在用户显式要求时生成；**PDF 仅在用户明确确认终稿后生成**，写作与修改期间不生成 PDF）。
- **单人模式**：按 `stages/` 各阶段 SKILL.md 的固定交付物执行；论文至少 8 幅正式图（当届官方规则或用户明确要求冲突时以其为准并记录依据）；PDF 生成同双解题手模式（终稿确认后）。
- 论文默认至少 8 幅正式图；全部计算结论来自实际运行结果，禁止编造。

## 完成判定

- 先满足"强制执行协议"，并提供可复核的门禁结果。
- 声称完整完成时，当前任务涉及的独立门禁均为 `PASS`（双解题手模式下含独立质检回执），且通过后产物未发生未经复验的实质变化；缺少 Subagent 能力时只能报告 `BLOCKED` 或受限交付。
- 所有计算结论来自实际运行结果；公式、表格和图表与代码结果一致；双解题手模式下共享参数在两工作区数值一致（结果锚点表核对通过）。
- 引用可由 OpenAlex、AnySearch 或原始出版页面追溯。
- 论文已按目标竞赛当届官方规则配置，篇幅目标已经确认，公式/非空图表数量与全部子问题图覆盖经过检查，图表编号与正文引用连续，参考文献与正文引用双向对应。Word 分支还须通过原生 OMML、DOCX 结构、转换警告门禁和渲染页数检查；LaTeX 分支还须通过环境诊断、真实编译、日志、权威资源—源码—PDF 哈希绑定、正文与附录页数、空白页、页面尺寸、字体嵌入和图片 DPI 检查。
- 所有产物位于 `PROJECT_ROOT`，`SKILL_ROOT` 未被改写。
