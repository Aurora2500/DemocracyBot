# Election.py

from typing import List, Dict

from ballot import Ballot, CountedBallot
from vote import Vote

"""
All electoral systems must take a list of ballots as an argument
and output a dict of the countup.
"""

def fptp(ballots: List[CountedBallot], vote: Vote) -> Dict[int, int]:
    result = {i:0 for i, _ in enumerate(vote, start=1)}
    for counted_ballot in ballots:
        ballot = counted_ballot.ballot
        result[ballot.ranking[0]] += counted_ballot.count
    return result


election = {
    "fptp":fptp,
}