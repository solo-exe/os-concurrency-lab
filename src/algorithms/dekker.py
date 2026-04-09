import time

from .base import SyncAlgorithm


class Dekker(SyncAlgorithm):
    """
    Implementation of Dekker's Algorithm for 2 threads.
    Thread IDs must be 0 and 1.
    """

    def __init__(self):
        # Flags indicating if a thread wants to enter critical section
        self.wants_to_enter = [False, False]
        # Whose turn it is
        self.turn = 0

    @property
    def name(self) -> str:
        return "Dekker's Algorithm"

    def acquire(self, thread_id: int):
        if thread_id not in (0, 1):
            raise ValueError(
                f"Dekker's algorithm supports only thread IDs 0 and 1. Got: {thread_id}"
            )

        other = 1 - thread_id

        self.wants_to_enter[thread_id] = True

        while self.wants_to_enter[other]:
            if self.turn != thread_id:
                self.wants_to_enter[thread_id] = False
                while self.turn != thread_id:
                    # Busy wait but allow context switch
                    time.sleep(0)
                self.wants_to_enter[thread_id] = True
            else:
                time.sleep(0)

    def release(self, thread_id: int):
        if thread_id not in (0, 1):
            raise ValueError(
                f"Dekker's algorithm supports only thread IDs 0 and 1. Got: {thread_id}"
            )

        other = 1 - thread_id
        self.turn = other
        self.wants_to_enter[thread_id] = False
