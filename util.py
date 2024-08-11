import time
from contextlib import contextmanager
from enum import Enum, auto


@contextmanager
def timing(message: str = None) -> int:
    start = time.perf_counter_ns()
    if message:
        print(f"[......] {message}", end='')
    try:
        yield start
    finally:
        end = time.perf_counter_ns()
        dur = end - start
        print(f"\r\033[2K[{dur//1000:6d}] {message}")


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()
