# Ballot.py
from typing import List, NamedTuple

class Ballot:

    __slots__ = ('userid', 'votename', 'ranking')

    def __init__(self, userid: str, votename: str, ranking: List[int]):
        self.userid = userid
        self.votename = votename
        self.ranking = ranking

    @property
    def full_ranking(self):
        rv = [0] * 5
        for i, e in enumerate(self.ranking):
            rv[i] = e
        return rv

    @classmethod
    def from_database(cls, data):
        return cls(votename=data[0], userid=data[1], ranking=data[2:])

class CountedBallot(NamedTuple):
    ballot: Ballot
    count: int