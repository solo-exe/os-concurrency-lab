import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

import psutil


@dataclass
class ThreadMetrics:
    thread_id: int
    wait_time: float = 0.0
    execution_time: float = 0.0
    cs_entries: int = 0


@dataclass
class SimulationMetrics:
    algorithm_name: str
    num_threads: int
    total_execution_time: float = 0.0
    avg_cpu_utilization: float = 0.0
    thread_metrics: Dict[int, ThreadMetrics] = field(default_factory=dict)

    def get_avg_wait_time(self) -> float:
        if not self.thread_metrics:
            return 0.0
        return sum(m.wait_time for m in self.thread_metrics.values()) / len(
            self.thread_metrics
        )


class MetricsTracker:
    def __init__(self, algorithm_name: str, num_threads: int):
        self.metrics = SimulationMetrics(
            algorithm_name=algorithm_name, num_threads=num_threads
        )
        for i in range(num_threads):
            self.metrics.thread_metrics[i] = ThreadMetrics(thread_id=i)

        self.cpu_samples = []
        self._monitoring = False
        self._monitor_thread = None
        self._start_time = None

    def start_monitoring(self):
        """Starts a background thread to sample CPU utilization."""
        self._start_time = time.time()
        self._monitoring = True

        def monitor_cpu():
            # Initial call to get CPU times, subsequent calls get diffs
            psutil.cpu_percent(interval=None)
            while self._monitoring:
                self.cpu_samples.append(psutil.cpu_percent(interval=0.1))

        self._monitor_thread = threading.Thread(target=monitor_cpu, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        """Stops the monitoring thread and calculates final metrics."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)

        self.metrics.total_execution_time = time.time() - self._start_time
        if self.cpu_samples:
            self.metrics.avg_cpu_utilization = sum(self.cpu_samples) / len(
                self.cpu_samples
            )

    def record_wait_time(self, thread_id: int, wait_time: float):
        self.metrics.thread_metrics[thread_id].wait_time += wait_time

    def record_cs_entry(self, thread_id: int):
        self.metrics.thread_metrics[thread_id].cs_entries += 1
