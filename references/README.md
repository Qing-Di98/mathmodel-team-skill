# 参考资料导航

本目录采用渐进式加载。先确定当前阶段，只读取对应角色入口；遇到具体任务再读取一份或少量参考文件。

## 根目录

- `SKILL_ROOT`：本仓库根目录，只读。
- `PROJECT_ROOT`：用户项目目录，所有产物写入这里。

任何参考文档中的相对路径均以其所属 `SKILL.md` 目录为基准。角色文档通过 `../../..` 回到 `SKILL_ROOT`。

## 三角色

| 阶段 | 入口 | 固定交付物 |
|---|---|---|
| 建模分析 | `roles/建模手/SKILL.md` | `题目分析报告.md`、`术语表格.md` |
| 代码实现 | `roles/编程手/SKILL.md` | Python/MATLAB 代码、结果表格、三类各至少 3 张且覆盖全部子问题的候选图、复现清单 |
| 论文撰写 | `roles/论文手/SKILL.md` | 默认交付 `完整论文.docx`；用户显式要求时同时交付 LaTeX 源码项目与编译 PDF |

## 按任务加载

| 任务 | 读取 |
|---|---|
| 竞赛要求（弹性需求/格式/支撑材料构成） | `竞赛要求.md` |
| 当届官方论文格式（2026 修订稿，电子版务必严格遵守） | `论文格式规范2026.md` |
| 关键决策与用户确认（1.是/2.否/3.其他） | `决策确认机制.md` |
| 解题手分工（依赖判定/基础问共同实现/实力分配） | `分工建议.md` |
| 论文写作团队标准（摘要五要素/结构黄金模板/篇幅/写作要点） | `课件/论文写作.md` |
| 摘要写作规范（标题/开头段/中间段/总结/关键词 + 国一实例逐条印证） | `摘要写作规范.md` |
| 流程图规范（排版/配色/美观度要素 + 模板图 flow_2~6 + 反例对照） | `流程图/流程图学习笔记.md` |
| 选模型 | `roles/建模手/references/建模设计理论.md` |
| 查具体算法 | `算法索引.md`，再读取一个匹配的 `../assets/*.md` |
| Python/MATLAB 实现 | `roles/编程手/references/工作流程.md` |
| 写求解报告（问题/意图/通俗讲解） | `求解报告模板.md` |
| MATLAB 工具箱与出图 | `roles/编程手/references/MATLAB规范.md` |
| 可视化 | `../tools/figure/SKILL.md` |
| 图型选择与科研绘图避坑 | `../tools/figure/references/chart-types/chart_selection.md` |
| Subagent 调度与阶段质检 | `Subagent调度.md` |
| 论文结构 | `roles/论文手/references/章节模板.md` |
| Word 格式 | `roles/论文手/references/论文格式规范.md` |
| LaTeX 格式 | `roles/论文手/references/LaTeX格式规范.md` |

## 课件资料

本队备赛课件（源文件：`E:\数模\课件\`），建模与写作时按需阅读：

- `课件/论文写作.md`：论文写作团队标准（摘要 300-400 字五要素、结构黄金模板与篇幅分配、模型阐述与结果展示要点），**论文写作阶段必读**。
- `课件/数学建模竞赛备赛教案.docx`：教案全文（含国一/省一论文差异分析）。
- `课件/数学建模新手备赛指南.docx`、`课件/数模第一节课补充.docx`、`课件/建模思维与流程.docx`：入门与流程。
- `课件/CUMCM国赛案例与建模步骤.docx`、`课件/优化模型 + 评价模型.docx`：赛题案例与模型分类。
- `课件/AHP.docx`、`课件/TOPSIS.docx`、`课件/bigM.docx`、`课件/PuLP代码.docx`：具体算法与代码。

## 工具

| 工具 | 入口 |
|---|---|
| 科研可视化 | `../tools/figure/SKILL.md` |
| 影印版/图片题面 OCR（四引擎，中英文） | `../tools/pdf-ocr/SKILL.md` |
| 双引擎论文搜索 | `../tools/paper_search/SKILL.md` |
| PDF | `../tools/pdf/SKILL.md` |
| Excel | `../tools/xlsx/SKILL.md` |
| DOCX | `../tools/docx/SKILL.md` |
| LaTeX | `../tools/latex/SKILL.md` |

外部论文只在确有需要时搜索和读取，并保留来源。
