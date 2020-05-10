# Vote.py

from typing import List

class Vote:

    __slots__ = ('name', 'options')

    def __init__(self, name: str, options: List[str]):
        self.name = name
        self.options = [elem for elem in options if elem]

    @classmethod
    def from_database(cls, data):
        name = data[0]
        options = [elem for elem in data[1:] if bool(elem)]
        return cls(name, options)

    def __len__(self) -> int:
        return len(self.options)

    def __getitem__(self, rank: int):
        return self.options[rank]