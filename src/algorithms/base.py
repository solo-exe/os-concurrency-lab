import abc


class SyncAlgorithm(abc.ABC):
    """
    Abstract base class for mutual exclusion algorithms.
    """

    @abc.abstractmethod
    def acquire(self, thread_id: int):
        """Acquire the lock for the given thread_id."""
        pass

    @abc.abstractmethod
    def release(self, thread_id: int):
        """Release the lock for the given thread_id."""
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the algorithm."""
        pass
