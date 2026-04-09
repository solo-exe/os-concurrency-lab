import threading

from .base import SyncAlgorithm


class SemaphoreSync(SyncAlgorithm):
    """
    Implementation of mutual exclusion using Python's threading.Semaphore.
    Can be used by N threads.
    """

    def __init__(self, value: int = 1):
        self.sem = threading.Semaphore(value)

    @property
    def name(self) -> str:
        return "Semaphore-based"

    def acquire(self, thread_id: int):
        self.sem.acquire()

    def release(self, thread_id: int):
        self.sem.release()
