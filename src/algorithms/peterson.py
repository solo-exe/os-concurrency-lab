import time

from .base import SyncAlgorithm


class Peterson(SyncAlgorithm):
    """
    Implementation of Peterson's Algorithm for 2 threads.
    Thread IDs must be 0 and 1.
    """

    def __init__(self):
        # Flags indicating if a thread wants to enter critical section
        self.flag = [False, False]
        # Whose turn it is
        self.turn = 0

    @property
    def name(self) -> str:
        return "Peterson's Algorithm"

    def acquire(self, thread_id: int):
        if thread_id not in (0, 1):
            raise ValueError(
                f"Peterson's algorithm supports only thread IDs 0 and 1. Got: {thread_id}"
            )

        other = 1 - thread_id

        self.flag[thread_id] = True
        self.turn = other

        # Busy wait while the other thread wants to enter AND it's their turn
        while self.flag[other] and self.turn == other:
            time.sleep(0)  # Yield CPU context slightly due to GIL

    def release(self, thread_id: int):
        if thread_id not in (0, 1):
            raise ValueError(
                f"Peterson's algorithm supports only thread IDs 0 and 1. Got: {thread_id}"
            )

        self.flag[thread_id] = False
