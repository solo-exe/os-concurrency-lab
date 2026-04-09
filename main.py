import json
import os
import platform

import psutil

from src.algorithms.dekker import Dekker
from src.algorithms.peterson import Peterson
from src.algorithms.semaphore import SemaphoreSync
from src.simulation.engine import SimulationEngine
from src.visualization.charts import (
    plot_cpu_utilization,
    plot_performance_comparison,
    plot_scalability,
    plot_wait_time_analysis,
)
from src.visualization.diagrams import (
    generate_architecture_diagram,
    generate_synchronization_timeline,
)


def collect_host_info() -> dict:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
        "ram_gb": round(psutil.virtual_memory().total / (1024.0**3), 2),
    }


def run_experiments():
    print("=" * 50)
    print("OS Synchronization Algorithms Simulation")
    print("=" * 50)

    env_info = collect_host_info()
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/environment_info.json", "w") as f:
        json.dump(env_info, f, indent=4)
    print(
        f"Environment Info saved. Host OS: {env_info['system']} {env_info['release']}"
    )

    results = []

    iterations_per_thread = 1000

    # 1. Dekker's Algorithm (Strictly 2 threads)
    print("\n[Running Dekker's Algorithm - 2 Threads]")
    dekker = Dekker()
    engine_dekker = SimulationEngine(
        dekker, num_threads=2, iterations=iterations_per_thread
    )
    results.append(engine_dekker.run())

    # 2. Peterson's Algorithm (Strictly 2 threads)
    print("\n[Running Peterson's Algorithm - 2 Threads]")
    peterson = Peterson()
    engine_peterson = SimulationEngine(
        peterson, num_threads=2, iterations=iterations_per_thread
    )
    results.append(engine_peterson.run())

    # 3. Semaphore-based Solution
    # Run with 2 threads for direct comparison
    print("\n[Running Semaphore Solution - 2 Threads]")
    semaphore_2t = SemaphoreSync(value=1)
    engine_sem_2t = SimulationEngine(
        semaphore_2t, num_threads=2, iterations=iterations_per_thread
    )
    results.append(engine_sem_2t.run())

    # Run Semaphore with escalating threads for scalability testing
    for t_count in [4, 8, 16]:
        print(f"\n[Running Semaphore Solution - {t_count} Threads]")
        sem = SemaphoreSync(value=1)
        # Adjust iterations to keep total workload roughly similar or allow it to grow
        # Let's keep iterations_per_thread constant to see true scalability overhead
        engine_sem = SimulationEngine(
            sem, num_threads=t_count, iterations=iterations_per_thread
        )
        results.append(engine_sem.run())

    print("\n" + "=" * 50)
    print("Generating Visualizations...")
    print("=" * 50)

    # Split results for fair comparison (2-threads only)
    results_2t = [r for r in results if r.num_threads == 2]

    # Split results for scalability (Semaphore across different thread counts)
    results_scalability = [r for r in results if r.algorithm_name == "Semaphore-based"]

    plot_performance_comparison(results_2t)
    plot_cpu_utilization(results_2t)
    plot_wait_time_analysis(results_2t)
    plot_scalability(results_scalability)

    print("\nGenerating Diagrams...")
    generate_architecture_diagram()
    generate_synchronization_timeline()

    print("\nSimulations finished. Check the 'outputs' directory for results.")


if __name__ == "__main__":
    run_experiments()
