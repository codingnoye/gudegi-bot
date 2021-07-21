from typing import List, Set

class User:
    handle: str
    channels: Set[str]
    solved_count: int
    solved_problems: Set[int]
    def __init__(self, handle, channels, solved_count, solved_problems):
        self.handle = handle
        self.channels = channels
        self.solved_count = solved_count
        self.solved_problems = solved_problems