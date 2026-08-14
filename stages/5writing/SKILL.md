---
name: 5writing
description: "数学建模竞赛论文撰写阶段，支持 Typst 和 LaTeX 双引擎。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和 figures/*.pdf 选择比赛模板、排版引擎、组织章节，并在论文正文中按章节直接插入图表。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 竞赛论文撰写（Typst / LaTeX）

本 skill 承接 `3coding-visual` 和 `4drawio`。前序阶段只提供真实数据、图表 PDF 和记录文件；本阶段负责选择比赛模板和排版引擎、组织论文结构，并决定每张图表放入哪个章节。

**Typst 引擎**下可调用 typst-author skill 学习 typst 写法；**LaTeX 引擎**参考本文件末尾的"LaTeX 写作要点"小节。

## 数学建模规范参考

如需领域判断，读取 `../_references/math_modeling_norms.md` 中的“论文写作”“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，论文结构仍按比赛模板和当前赛题内容决定。

**团队课件建议（本队写作标准，课件为第一优先学习资源，冲突以课件为准）**：写作前必读 `<SKILL_ROOT>/references/课件/README.md`（课件索引与按任务加载表）与 `<SKILL_ROOT>/references/课件/论文写作.md`，按其建议执行——摘要 300-400 字且包含问题/方法/创新点/关键结果/结论五要素（第一段约 200 字加粗、结果量化、创新突出）；按"结构黄金模板"组织章节并控制篇幅（问题重述+分析 1-1.5 页、模型假设+符号说明 0.5 页、模型建立与求解 12-15 页、模型检验与评价 2-3 页、推广+参考文献 1 页）；模型阐述符号先行、公式编号、推导完整；结果展示三线表、高清图、对比分析、可视化创新。模型术语与建模步骤引用课件说法（如时序建模的国赛 7 步流程、优化三要素等），与网上资料冲突时以课件为准。其余课件（`references/课件/` 下已按分类整理：`数据处理与预测模型/`、`优化模型与评价模型/`、备赛教案、建模思维与流程、CUMCM 国赛案例等，每个 docx 均有同名 `.md` 提取版）按需阅读。

**当届官方格式（国赛 2026 修订稿，电子版务必严格遵守）**：写作与定稿前必读 `<SKILL_ROOT>/references/论文格式规范2026.md` 与 `references/竞赛要求.md` 硬性要求——纸质版：A4、页边距 ≥2.5cm、承诺书/编号专用页/摘要专用页（摘要 ≤1 页，从摘要页起页码 1 开始）、正文无目录 ≤30 页、附录含支撑材料文件列表与全部可运行源程序、正文不得含身份/学校/赛区信息。**电子版**：参赛论文必须是一个单独文件（PDF 或 Word 之一，建议 PDF），与纸质版内容格式（含附录）完全一致，≤20MB，**不要压缩**，**第一页必须为摘要专用页（不含承诺书和编号专用页）**；支撑材料用 WinRAR 压缩为一个文件（RAR/ZIP，≤20MB），文件列表放入附录，无支撑材料须注明"本论文没有支撑材料"。违反上述要求可能被取消评奖资格。**排版硬性细节（`竞赛要求.md` 新增小节）**：多个公式用大括号括起不铺满一行；符号下标必须用科学下标排版，PDF 中禁止出现 `r_A` 这类带下划线写法；表格标题在表格上方、流程图与数据可视化图标题在图下方，标题字号须小于正文且一律黑色。

## 官方内置 Skills 调用登记（英文论文与写作辅助）

以下为 Claude Code 内置 skills（不落盘、不可拷贝），按需直接调用，**仓库内自足工具优先**：

| 任务 | 调用 skill | 与仓库工具的关系 |
|---|---|---|
| 论文写作方法论（结构/表述通用方法） | `ml-paper-writing` | 方法论补充，不替代课件论文写作.md 本队标准 |
| 英文论文（MCM/ICM）撰写 | `nature-writing` | 与 `5writing` 模板流程互补 |
| 英文润色/改写 | `nature-polishing` | 英文定稿前调用 |
| 审稿视角自检 | `nature-reviewer` | 补充 `6verity` 终检 |
| 文献精读 | `nature-reader` | 按需 |
| 统计表述规范 | `nature-statistics` | 按需 |
| 引用格式核验 | `nature-citation`、`nature-ref-verifier` | 引用仍以当届官方规范为准 |
| 学术检索 | `nature-academic-search` | 与 `tools/paper_search` 双引擎并存，仓库工具优先 |
| 通用可视化规范 | `dataviz` | 仅作 `tools/figure` 契约的参考，figure 契约仍为唯一契约 |
| Word 生成 | `docx` | 仓库 `tools/docx` 优先（哈希/OMML 门禁完整），内置 docx 仅作备选 |
| 画布/协作排版 | `canvas-design`、`doc-coauthoring` | 按需；论文仍集中合稿，不分散多人并写 |

## 模板族

本技能内捆绑的模板位于：

```text
templates/zh/<竞赛>/main.typ         # Typst 模板
templates/zh/<竞赛>-latex/main.tex   # LaTeX 模板
templates/en/<竞赛>/main.typ         # Typst 模板
templates/en/<竞赛>-latex/main.tex   # LaTeX 模板
```

**LaTeX 模板覆盖范围**：所有中文模板和英文模板均已提供 LaTeX 版本（`-latex` 后缀），使用 xelatex 编译。

支持的中文模板（Typst + LaTeX 双版本）：

```text
apmcm, changsanjiao, cumcm, default, diangongbei, dongsansheng,
huashubei, huaweibei, huazhongbei, mathorcup, mcm, shuweibei, stats, wuyibei
```

华为杯、华中杯、五一杯统一使用 `huaweibei`、`huazhongbei`、`wuyibei` 作为模板。

支持的英文模板（Typst + LaTeX 双版本）：

```text
apmcm, default, mcm
```

论文中的所有数值图表结论必须来自 `reports/RESULTS_REPORT.md` 或 `figures/*`。不得编造、估算或使用不同的四舍五入方式。


## 工作流

### 步骤 0：确定排版引擎

**撰写论文前必须让用户选择排版引擎。** 引擎决定后续所有步骤（模板路径、章节文件扩展名、图片插入语法、编译命令），选错会导致整篇论文格式错误。

使用 AskUserQuestion 工具向用户询问："撰写论文使用哪种排版引擎？"

- 选项 1：LaTeX（xelatex 编译，数学建模竞赛主流，模板已全部就绪）— 推荐选项放第一位
- 选项 2：Typst（typst 编译，调用 typst-author skill 辅助写作）

询问前先读取 `plan.md` 的"用户偏好 → 排版引擎"字段作为预选项：
- 若 plan.md 已记录引擎选择，向用户确认："检测到之前选择的引擎是 <LaTeX/Typst>，是否沿用？"
- 若 plan.md 不存在或未记录引擎选择，直接询问用户选择。
- 若用户未明确指定或跳过，**默认使用 LaTeX**。

根据确定的引擎选择对应模板族：

- **Typst 引擎**：使用 `templates/<lang>/<竞赛>/main.typ`，调用 typst-author skill。编译命令 `typst compile main.typ`。
- **LaTeX 引擎**：使用 `templates/<lang>/<竞赛>-latex/main.tex`，xelatex 编译（中文和英文均需跑两遍解决交叉引用）。编译命令 `xelatex -interaction=nonstopmode main.tex`（执行两次）。

**后续步骤中的所有代码示例、文件扩展名、图片插入语法都必须按所选引擎选择对应版本，不要混用。**

### 步骤 1：选择语言和模板


除非用户明确要求中文，否则 MCM/ICM/COMAP 一律使用英文。所有中文竞赛名称使用中文。

模板键示例（Typst 引擎）：

```text
长三角 -> zh/changsanjiao
APMCM 英文版 -> en/apmcm
全国赛/国赛/CUMCM -> zh/cumcm
统计建模 -> zh/stats
MCM/ICM/COMAP -> en/mcm
```

模板键示例（LaTeX 引擎）：

```text
全国赛/国赛/CUMCM -> zh/cumcm-latex
MCM/ICM/COMAP -> en/mcm-latex
```

### 步骤 2：准备模板

用以下命令检查捆绑模板是否可访问（`SKILL_DIR` 为本 skill 所在目录）：

**Typst 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>/main.typ" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：直接将 `templates/zh/<竞赛>/` 整目录复制到 `paper/`。这些模板是自包含入口文件，不依赖额外共享样式文件。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 Typst 框架，并在 `paper/` 内注明"重建自 default 结构"。

存在匹配模板时，绝不从零开始写论文。

**LaTeX 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>-latex/main.tex" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：将 `templates/zh/<竞赛>-latex/` 整目录复制到 `paper/`。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 LaTeX 框架，并在 `paper/` 内注明"重建自 default-latex 结构"。


### 步骤 3：构建图表规划

在写正文各节之前，根据 `figures/*.pdf`、`reports/RESULTS_REPORT.md`，以及 `reports/DRAWIO_REPORT.md`（如果存在）构建图表规划：

```text
图表规划
fig_roadmap.pdf -> 引言/问题重述
fig_flow_q1.pdf -> 问题一模型构建
fig_flow_q2.pdf -> 问题二模型构建
fig_pipeline.pdf -> 数据预处理/方法节
结果图 -> 对应的结果节
```

图片路径相对于写入该图片的文件：写在 `paper/main.typ` 或 `paper/main.tex` 中通常用 `../figures/xxx.pdf`，写在 `paper/sections/*.typ` 或 `paper/sections/*.tex` 中通常用 `../../figures/xxx.pdf`。

**Typst 引擎**图片插入：

```typst
#figure(
  image("../../figures/fig_q1_error_dist.pdf", width: 85%),
  caption: [问题一预测误差分布],
)
```

**LaTeX 引擎**图片插入：

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{../../figures/fig_q1_error_dist.pdf}
  \caption{问题一预测误差分布}
  \label{fig:q1_error}
\end{figure}
```

英文论文使用英文图注。

**流程图（研究思路/模型结构/求解流程）一律按本队模板标准绘制**：绘图前必读 `<SKILL_ROOT>/references/流程图/流程图学习笔记.md`，并对照模板图（`<SKILL_ROOT>/references/流程图/flow_2~6.png`）执行——浅色分区块 + 一个主色相家族 + Problem/Task/Step 编号导航 + 短标签文字 + 三档字号层级；**禁止**纯白底无分区色块的"草稿式"流程图（教训见笔记反例对照节）。

### 步骤 4：撰写各节

**以下章节文件名按所选引擎使用 `.typ`（Typst）或 `.tex`（LaTeX）扩展名。** 例如 Typst 引擎用 `1_restatement.typ`，LaTeX 引擎用 `1_restatement.tex`。文件名主体保持一致。

中文数学建模通用模板各节文件（`changsanjiao`、`diangongbei`、`huashubei`、`mathorcup`、`wuyibei`）：

```text
1_restatement.typ  - 问题重述与分析
2_analysis.typ     - 数据理解与总体思路
3_assumptions.typ  - 模型假设
4_symbols.typ      - 符号说明
5_problem1.typ     - 问题一建模与求解
6_problem2.typ     - 问题二建模与求解
7_problem3.typ     - 问题三建模与求解
...         - 根据题目调整问题数量  
8_evaluation.typ   - 灵敏度分析、模型评价与推广
A_code.typ         - 附录代码
```

国赛/华中杯/华为杯（`cumcm`、`huazhongbei`、`huaweibei`）按以下章节结构：

```text
1_restatement.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...        - 根据题目调整问题数量
8_sensitivity.typ
9_evaluation.typ
A_code.typ
```

东三省模板（`dongsansheng`）额外使用单独摘要文件：

```text
abstract.typ
1_restatement.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...       - 根据题目调整问题数量
8_evaluation.typ
A_code.typ
```

数维杯模板（`shuweibei`）保留原 LaTeX 的示例入口命名：

```text
Abstract.typ
Introduction.typ
2_analysis.typ
3_assumptions.typ
4_symbols.typ
5_problem1.typ
6_problem2.typ
7_problem3.typ
...      - 根据题目调整问题数量
8_evaluation.typ
Appendices1.typ
A_code.typ
```

中文默认模板（`default`）：

```text
1_restatement.typ
2_assumptions.typ
3_symbols.typ
4_problem1.typ
5_problem2.typ
6_problem3.typ
...      - 根据题目调整问题数量
7_sensitivity.typ
8_evaluation.typ
A_code.typ
```

中文统计建模各节文件：

```text
1_introduction.typ
2_method.typ
3_data.typ
4_analysis.typ
5_results.typ
6_conclusion.typ
A_code.typ
```

英文 MCM/APMCM 各节文件（`en/mcm`、`en/apmcm`、`zh/mcm`、`zh/apmcm`）：

```text
1_introduction.typ
2_assumptions.typ
3_model_design.typ
4_solution.typ
5_sensitivity.typ
6_strengths_weaknesses.typ
7_conclusions.typ
A_code.typ
```

**LaTeX 模板章节文件**（对应 `-latex` 后缀模板，结构与 Typst 版本一一对应）：

国赛 LaTeX 模板（`zh/cumcm-latex`，对应 `cumcm` Typst 版本）：

```text
1_restatement.tex
2_analysis.tex
3_assumptions.tex
4_symbols.tex
5_problem1.tex
6_problem2.tex
7_problem3.tex
8_sensitivity.tex
9_evaluation.tex
A_code.tex
```

MCM/ICM LaTeX 模板（`en/mcm-latex`）：

```text
1_introduction.tex
2_assumptions.tex
3_model_design.tex
4_solution.tex
5_sensitivity.tex
6_strengths_weaknesses.tex
7_conclusions.tex
A_code.tex
```

其余 LaTeX 模板（`changsanjiao-latex`、`default-latex`、`huashubei-latex`、`mathorcup-latex`、`wuyibei-latex`、`huazhongbei-latex`、`huaweibei-latex`、`diangongbei-latex`、`dongsansheng-latex`、`shuweibei-latex`、`stats-latex`、`apmcm-latex`、`mcm-latex`、`en/apmcm-latex`、`en/default-latex`）的章节文件命名与上述结构类似，以 `main.tex` 中 `\input{}` 引用的文件名为准。

英文默认模板（`en/default`）：

```text
1_introduction.typ
2_assumptions.typ
3_notations.typ
4_model.typ
5_sensitivity.typ
6_evaluation.typ
7_conclusions.typ
A_code.typ
```

**正文写作应使用连贯的学术段落。避免在最终论文中出现工作流内部名称，如 `reports/`、`figures/` 或 `CLAUDE.md`。**

**写模型假设（`3_assumptions`）与符号说明（`4_symbols`）前必读 `<SKILL_ROOT>/references/模型假设和符号说明.md` 并有意识地逐条执行**（假设：五条为最佳不超过六条、不涉及具体数值/参数/实验过内容、格式 `**假设一**：假设……` 中文序号加粗直接陈述；符号表：汇总成一张三列表"符号/说明/单位"、每项居中、无单位用 `-`、半页纸为宜不超过一页、表标题在表格上方；正文符号一律科学下标排版，禁止 `r_A`、`W*`、`λ_max` 文本写法）。

### 步骤 5：参考文献

只使用真实存在的参考文献。文件名按引擎选择：Typst 用 `paper/references.typ`，LaTeX 用 `paper/references.tex`。

**Typst 引擎**：

```typst
#set enum(numbering: "[1]")
#enum[
  作者. 题名[J]. 期刊名, 年份, 卷(期): 页码.
  Author. "Title." Journal or Conference, year.
]
```

正文上标引用：`相关研究已用于物流网络优化#super("[1]")。`

**LaTeX 引擎**：

```latex
\begin{thebibliography}{99}
  \bibitem{ref1} 作者. 题名[J]. 期刊名, 年份, 卷(期): 页码.
  \bibitem{ref2} Author. "Title." Journal, year.
\end{thebibliography}
```

正文引用用 `\cite{ref1}` 或 `\cite{ref1,ref2}`。

### 步骤 6：最后撰写摘要或总结

在所有章节完成后撰写中文摘要或英文 Summary Sheet。必须包含每个子问题的方法和精确的数值结果。

**写摘要前必读 `<SKILL_ROOT>/references/摘要写作规范.md` 并有意识地逐条执行**（标题"基于XXX的XXX"一行内；开头段背景/做什么/意义三句三五行，第二句最重要；中间段每问"方法→关键处理→求解→精确数值"，每问必有带单位的精确数值、模型算法写全名、交叉验证写相对误差证据、数据外引附录；总结段可选写则"本文创新性在于：一是…二是…"；关键词 4-8 个核心模型词；写完后按执行清单逐条自检）。

### 步骤 7：终稿确认与 PDF 生成（用户明确终稿后才生成 PDF）

论文必然反复修改，**写作与修改期间一律不生成最终 PDF**：

- 工作形态：Word 草稿（docx）或 Typst/LaTeX 源码。所有修改都在源码/草稿上进行，未确认终稿前不执行最终编译。
- **PDF 仅在用户明确声明终稿后生成**（如"这是终稿""定稿，不再修改"等明确表述；仅说"写完了"不算终稿确认）。PDF 生成时须同时满足当届电子版要求（单文件、与纸质版一致、≤20MB、不压缩、第一页为摘要专用页，见 `<SKILL_ROOT>/references/论文格式规范2026.md`）。
- 未确认终稿前，进度汇报只报"草稿完成，待终稿确认"，不得声称论文已完成。
- 终稿确认并生成 PDF 后，进入 `stages/6verity` 终检（含 PDF 逐页视觉检查）。

### 步骤 8：支撑材料打包（先给用户过目清单，确认后再压缩）

按 `<SKILL_ROOT>/references/竞赛要求.md` 与 `<SKILL_ROOT>/references/论文格式规范2026.md` 第十一条生成支撑材料：

1. **主 Agent 盘点候选文件**：全部可运行源程序（含 EXCEL、SPSS 等交互命令）、自主查阅使用的数据资料（赛题提供的原始数据除外）、较大篇幅中间结果的图表等；对应功能缺失时明确说明（如"本队未使用额外数据资料"）。
2. **先列文件清单给用户过目**：按题号/目录列出相对路径与用途，等待用户确认或增删；**用户未过目清单前，不得直接压缩生成支撑材料文件**。
3. 用户确认后使用 WinRAR 压缩为**一个文件**（RAR 或 ZIP，大小不超过 20MB），压缩包文件名不含身份/学校/赛区信息。
4. 校验：压缩包可正常解压、条目数与已确认清单一致、≤20MB、内容与论文相符、无身份信息；文件列表写入论文附录（无支撑材料时附录注明"本论文没有支撑材料"）。

## LaTeX 写作要点

以下要点供 **LaTeX 引擎**使用。Typst 引擎请调用 typst-author skill 获取语法帮助。

### 编译命令

```bash
# 中文模板（xelatex，跑两遍解决交叉引用）
xelatex main.tex && xelatex main.tex

# 英文模板（xelatex，同样跑两遍）
xelatex main.tex && xelatex main.tex
```

> **编译仅限终稿确认后执行**（见步骤 7）：写作与修改期间不编译 PDF，只在用户明确声明终稿后才运行上述命令生成最终 PDF。

### 文档结构

```latex
\documentclass[a4paper,12pt]{article}   % 英文
\documentclass[a4paper,12pt]{ctexart}   % 中文

\usepackage{...}   % 宏包加载
\usepackage{graphicx}   % 图片支持
\usepackage{booktabs}   % 三线表
\usepackage{amsmath,amssymb}   % 数学公式
\usepackage{hyperref}   % 交叉引用（需两遍编译）
```

### 图表插入

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{../../figures/fig_q1.pdf}
  \caption{图注}
  \label{fig:q1}
\end{figure}

% 三线表
\begin{table}[htbp]
  \centering
  \caption{表注}
  \begin{tabular}{ccc}
    \toprule
    \textbf{列1} & \textbf{列2} & \textbf{列3} \\
    \midrule
    数据 & 数据 & 数据 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### 交叉引用

```latex
如图~\ref{fig:q1}所示，...   % 图片引用
式~(\ref{eq:objective}) 给出...   % 公式引用
见第~\pageref{fig:q1} 页   % 页码引用
```

### 数学公式

```latex
行内公式：$f(x) = \sum_{i=1}^n \theta_i \phi_i(x)$

行间公式：
\begin{equation}
  \mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2
  \label{eq:objective}
\end{equation}
```

### 章节和强调

```latex
\section{问题重述}
\subsection{问题背景}
\textbf{问题一：} xxx   % 对应 Typst 的 #strong
```
