import os
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.simulation.metrics_tracker import SimulationMetrics


def save_plot(filename: str):
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", filename)
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved chart: {filepath}")


def _prepare_dataframe(results: List[SimulationMetrics]) -> pd.DataFrame:
    data = []
    for r in results:
        data.append(
            {
                "Algorithm": r.algorithm_name,
                "Threads": r.num_threads,
                "Execution Time (s)": r.total_execution_time,
                "Avg CPU Utilization (%)": r.avg_cpu_utilization,
                "Avg Wait Time (s)": r.get_avg_wait_time(),
            }
        )
    return pd.DataFrame(data)


def plot_performance_comparison(results: List[SimulationMetrics]):
    df = _prepare_dataframe(results)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Threads", y="Execution Time (s)", hue="Algorithm")
    plt.title("Performance Comparison: Execution Time vs Thread Count")
    save_plot("performance_comparison.png")


def plot_cpu_utilization(results: List[SimulationMetrics]):
    df = _prepare_dataframe(results)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Threads", y="Avg CPU Utilization (%)", hue="Algorithm")
    plt.title("CPU Utilization Comparison (Busy Waiting vs Blocking)")
    save_plot("cpu_utilization.png")


def plot_wait_time_analysis(results: List[SimulationMetrics]):
    df = _prepare_dataframe(results)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="Threads", y="Avg Wait Time (s)", hue="Algorithm")
    plt.title("Average Wait Time per Thread")
    save_plot("wait_time_analysis.png")


def plot_scalability(results: List[SimulationMetrics]):
    df = _prepare_dataframe(results)

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=df, x="Threads", y="Execution Time (s)", hue="Algorithm", marker="o"
    )
    plt.title("Scalability: Execution Time Growth with Thread Count")
    save_plot("scalability_analysis.png")
