import threading
import time

from src.algorithms.base import SyncAlgorithm
from src.simulation.metrics_tracker import MetricsTracker, SimulationMetrics


class SimulationEngine:
    def __init__(self, algorithm: SyncAlgorithm, num_threads: int, iterations: int):
        self.algorithm = algorithm
        self.num_threads = num_threads
        self.iterations = iterations
        self.metrics_tracker = MetricsTracker(algorithm.name, num_threads)

        # Shared resource
        self.shared_counter = 0

    def _worker(self, thread_id: int):
        """Worker thread function that tries to enter the critical section repeatedly."""
        for _ in range(self.iterations):
            # Record wait time
            start_wait = time.time()
            self.algorithm.acquire(thread_id)
            wait_duration = time.time() - start_wait

            self.metrics_tracker.record_wait_time(thread_id, wait_duration)
            self.metrics_tracker.record_cs_entry(thread_id)

            # --- CRITICAL SECTION ---
            # Simulate some work
            local_val = self.shared_counter
            time.sleep(
                0.0001
            )  # Small delay to increase chance of race conditions if faulty
            self.shared_counter = local_val + 1
            # ------------------------

            self.algorithm.release(thread_id)

    def run(self) -> SimulationMetrics:
        """Executes the simulation and returns collected metrics."""
        print(
            f"Starting simulation for {self.algorithm.name} with {self.num_threads} threads, {self.iterations} iterations/thread."
        )

        self.metrics_tracker.start_monitoring()

        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self._worker, args=(i,), daemon=True)
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.metrics_tracker.stop_monitoring()

        expected_counter = self.num_threads * self.iterations
        if self.shared_counter != expected_counter:
            print(
                f"WARNING: Race condition detected! Expected {expected_counter}, got {self.shared_counter}"
            )
        else:
            print(
                f"Success: Mutual exclusion maintained. Final counter: {self.shared_counter}"
            )

        return self.metrics_tracker.metrics
