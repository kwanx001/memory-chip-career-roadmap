# 存储芯片入行学习仓库

这是一套面向零基础专科背景、暂不提升学历的 3 至 5 年行动方案。目标不是直接竞争
DRAM/NAND 核心器件研发，而是先获得半导体设备、制造、测试或失效分析岗位所需的能力，
再向测试、产品、良率、失效分析或助理工艺岗位发展。

## 从这里开始

0. 打开 [可视化学习网页](web/index.html)，直观查看路线并记录每周进度。
1. 阅读 [3 至 5 年路线](docs/roadmap.md)。
2. 按 [前 12 周计划](docs/first-12-weeks.md) 执行，每周投入 10 至 12 小时。
3. 每月底更新 [技能检查表](docs/skills-checklist.md)。
4. 从第 9 周开始运行 [晶圆良率分析项目](projects/wafer-yield-analysis/README.md)。
5. 基础稳定后完成 [DRAM 保持时间仿真](projects/dram-retention-ltspice/README.md) 和
   [8D 失效分析案例](projects/failure-analysis-8d/README.md)。

## 仓库结构

```text
docs/
  roadmap.md                 3 至 5 年阶段路线与验收标准
  first-12-weeks.md          零基础启动日程
  skills-checklist.md        月度能力检查表
  job-search.md              岗位筛选、简历和面试准备
  vocabulary.csv             首批半导体英文词汇
projects/
  wafer-yield-analysis/      可运行的 Python 良率分析作品
  dram-retention-ltspice/    LTspice 仿真项目
  failure-analysis-8d/       NAND 与 MLCC 的 8D 案例模板
progress/
  weekly-log-template.md     每周复盘模板
```

## 每周固定节奏

- 4 小时：数学、物理和电路基础。
- 3 小时：半导体器件、工艺和存储器。
- 2 小时：Excel、Python、SQL 或统计质量工具。
- 2 小时：实验、项目和技术文档。
- 1 小时：英文词汇、岗位信息与复盘。

学习顺序遵守一个原则：先能解释，再能计算，最后能用数据或实验验证。

## 阶段目标

| 时间 | 可验证结果 |
| --- | --- |
| 3 个月 | 解释基本电路和 MOS 管；用 Python 读取 CSV、统计并绘图 |
| 1 年 | 解释 DRAM/NAND 基本结构；掌握常见工艺、仪器和统计概念 |
| 2 年 | 独立完成良率分析、基础故障诊断和规范化技术报告 |
| 3 年 | 具备设备、制造、封测、测试或 FA 初级岗位的作品与面试能力 |
| 3 至 5 年 | 通过现场经验转向测试、产品、良率、FA 或助理工艺岗位 |

## 重要说明

证书不能代替可验证能力。每学一个主题，至少留下一个结果：计算题、实验记录、脚本、
图表、仿真文件、8D 报告或故障复盘。
