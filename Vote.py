# Vote.py

from typing import List

class Vote:

    def __init__(self, votename: str, ranking: List[int]):
        self.name = votename
        self.ranking = [elem for elem in ranking if elem]
        pass

    @classmethod
    def from_database(cls, data):
        name = data[0]
        return cls(name, data[1:])

    def __len__(self) -> int:
        return len(self.ranking)

    def __getitem__(self, rank: int):
        return self.ranking[rank]