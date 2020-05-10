# Election.py

from typing import List, Dict

from ballot import Ballot, CountedBallot
from result import Result
from vote import Vote

"""
All electoral systems must take a list of ballots as an argument
and output a result.
"""

def fptp(ballots: List[CountedBallot], vote: Vote) -> Result:
    result = {i:0 for i, _ in enumerate(vote, start=1)}
    for counted_ballot in ballots:
        ballot = counted_ballot.ballot
        result[ballot.ranking[0]] += counted_ballot.count
    return result


election = {
    "fptp":fptp,
}