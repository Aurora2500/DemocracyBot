from typing import List

class Ballot:
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