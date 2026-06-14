from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUTPUT_DIR = Path(__file__).resolve().parent / "output"
RNG = np.random.default_rng(20260614)
WAFER_RADIUS = 25
VTH_LSL = 0.42
VTH_USL = 0.58


def generate_wafer() -> pd.DataFrame:
    records: list[dict[str, float | int | str]] = []

    for x in range(-WAFER_RADIUS, WAFER_RADIUS + 1):
        for y in range(-WAFER_RADIUS, WAFER_RADIUS + 1):
            radius = float(np.hypot(x, y))
            if radius > WAFER_RADIUS:
                continue

            vth = float(RNG.normal(0.50, 0.018))
            leakage_na = float(RNG.lognormal(mean=2.25, sigma=0.34))

            edge_risk = radius > WAFER_RADIUS * 0.82 and RNG.random() < 0.22
            cluster_risk = (x - 8) ** 2 + (y + 7) ** 2 < 30 and RNG.random() < 0.60
            random_risk = RNG.random() < 0.018

            if edge_risk:
                vth += float(RNG.normal(0.075, 0.012))
            if cluster_risk:
                leakage_na *= float(RNG.uniform(5.0, 10.0))

            fail_vth = not VTH_LSL <= vth <= VTH_USL
            fail_leakage = leakage_na > 35.0

            if random_risk:
                bin_name = "BIN4_RANDOM"
            elif fail_leakage:
                bin_name = "BIN3_LEAKAGE"
            elif fail_vth:
                bin_name = "BIN2_VTH"
            else:
                bin_name = "BIN1_PASS"

            records.append(
                {
                    "x": x,
                    "y": y,
                    "radius": round(radius, 3),
                    "vth_v": round(vth, 5),
                    "leakage_na": round(leakage_na, 4),
                    "bin": bin_name,
                    "pass": int(bin_name == "BIN1_PASS"),
                }
            )

    return pd.DataFrame.from_records(records)


def calculate_cpk(series: pd.Series, lsl: float, usl: float) -> float:
    mean = float(series.mean())
    sigma = float(series.std(ddof=1))
    if sigma == 0:
        return float("inf")
    cpu = (usl - mean) / (3 * sigma)
    cpl = (mean - lsl) / (3 * sigma)
    return min(cpu, cpl)


def save_wafer_map(df: pd.DataFrame) -> None:
    bin_codes = {
        "BIN1_PASS": 0,
        "BIN2_VTH": 1,
        "BIN3_LEAKAGE": 2,
        "BIN4_RANDOM": 3,
    }
    colors = ["#2ca02c", "#d62728", "#ff7f0e", "#9467bd"]
    labels = ["Pass", "Vth fail", "Leakage fail", "Random fail"]

    fig, ax = plt.subplots(figsize=(8, 7))
    for label, code, color in zip(labels, bin_codes.values(), colors, strict=True):
        subset = df[df["bin"].map(bin_codes) == code]
        ax.scatter(
            subset["x"],
            subset["y"],
            s=22,
            c=color,
            marker="s",
            label=label,
            linewidths=0,
        )

    wafer_edge = plt.Circle((0, 0), WAFER_RADIUS + 0.7, fill=False, color="black")
    ax.add_patch(wafer_edge)
    ax.set_aspect("equal")
    ax.set_title("Simulated Wafer Bin Map")
    ax.set_xlabel("X position")
    ax.set_ylabel("Y position")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "wafer_map.png", dpi=160)
    plt.close(fig)


def save_histogram(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["vth_v"], bins=35, color="#4c78a8", edgecolor="white")
    ax.axvline(VTH_LSL, color="#d62728", linestyle="--", label=f"LSL={VTH_LSL}")
    ax.axvline(VTH_USL, color="#d62728", linestyle="--", label=f"USL={VTH_USL}")
    ax.set_title("Threshold Voltage Distribution")
    ax.set_xlabel("Vth (V)")
    ax.set_ylabel("Die count")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "vth_histogram.png", dpi=160)
    plt.close(fig)


def save_bin_distribution(df: pd.DataFrame) -> None:
    counts = df["bin"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    counts.plot(kind="bar", ax=ax, color=["#2ca02c", "#d62728", "#ff7f0e", "#9467bd"])
    ax.set_title("Bin Distribution")
    ax.set_xlabel("Bin")
    ax.set_ylabel("Die count")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "bin_distribution.png", dpi=160)
    plt.close(fig)


def write_report(df: pd.DataFrame) -> None:
    total = len(df)
    passed = int(df["pass"].sum())
    yield_rate = passed / total
    mean_vth = float(df["vth_v"].mean())
    sigma_vth = float(df["vth_v"].std(ddof=1))
    cpk = calculate_cpk(df["vth_v"], VTH_LSL, VTH_USL)
    edge = df[df["radius"] > WAFER_RADIUS * 0.82]
    center = df[df["radius"] <= WAFER_RADIUS * 0.82]
    edge_yield = float(edge["pass"].mean())
    center_yield = float(center["pass"].mean())
    bin_counts = df["bin"].value_counts().sort_index()

    interpretation = (
        "边缘良率明显低于内部区域，优先检查具有径向非均匀性的工艺或量测因素。"
        if edge_yield + 0.05 < center_yield
        else "未观察到显著的边缘良率下降。"
    )

    bin_lines = "\n".join(f"- {name}: {count}" for name, count in bin_counts.items())
    report = f"""# 模拟晶圆良率报告

## 摘要

- 总 die 数：{total}
- 通过 die 数：{passed}
- 总良率：{yield_rate:.2%}
- 边缘良率：{edge_yield:.2%}
- 内部良率：{center_yield:.2%}

## 阈值电压

- 规格：{VTH_LSL:.2f} V 至 {VTH_USL:.2f} V
- 均值：{mean_vth:.4f} V
- 样本标准差：{sigma_vth:.4f} V
- CPK：{cpk:.3f}

## Bin 统计

{bin_lines}

## 初步判断

{interpretation}

wafer map 中还存在人为注入的局部漏电异常簇。空间相关性只能提供调查方向，不能直接证明
根因。下一步应按设备、批次、时间和工艺参数分层，并先确认量测系统稳定。

## 文件

- `wafer_map.png`：空间失效模式。
- `vth_histogram.png`：阈值电压分布与规格限。
- `bin_distribution.png`：bin 数量分布。
- `simulated_wafer.csv`：可复现分析的数据。
"""
    (OUTPUT_DIR / "report.md").write_text(report, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = generate_wafer()
    df.to_csv(OUTPUT_DIR / "simulated_wafer.csv", index=False)
    save_wafer_map(df)
    save_histogram(df)
    save_bin_distribution(df)
    write_report(df)
    print(f"Analysis complete: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
