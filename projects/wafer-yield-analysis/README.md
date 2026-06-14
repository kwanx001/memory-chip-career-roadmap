# 晶圆良率分析项目

本项目生成一批模拟晶圆测试数据，并完成：

- wafer map。
- pass/fail 与 bin 分布。
- 阈值电压直方图。
- 均值、标准差、CPK。
- 边缘失效和局部异常簇识别。
- Markdown 分析报告。

## 运行

需要 Python 3.10 或更高版本。

当前电脑的 `python` 是 Windows 商店占位符。正式学习前应从
[Python 官网](https://www.python.org/downloads/windows/)安装 64 位版本，并在安装时勾选
`Add python.exe to PATH`。安装完成后重新打开 PowerShell，确认：

```powershell
python --version
python -m pip --version
```

然后在本目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python analyze.py
```

运行后生成：

```text
output/
  simulated_wafer.csv
  wafer_map.png
  vth_histogram.png
  bin_distribution.png
  report.md
```

## 面试时如何讲

1. 先说明数据是模拟数据，不冒充真实产线数据。
2. 解释规格限、pass/fail 和 CPK 的定义。
3. 指出空间分布比单一总良率提供了更多根因线索。
4. 说明边缘失效可能与涂胶、曝光、刻蚀、薄膜均匀性或测量接触有关，但不能只凭图下结论。
5. 给出下一步验证：按设备、批次、时间和工艺参数分层，并检查量测系统。

## 扩展任务

- 增加 10 片晶圆和 lot 维度。
- 添加 Xbar-R 或 I-MR 控制图。
- 将结果存入 SQLite，再用 SQL 查询异常 bin。
- 改变模拟缺陷模式，比较随机、边缘、中心和划痕缺陷。
