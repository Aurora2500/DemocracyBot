# DatabaseManager.py

import _sqlite3
from typing import Set, List

from ballot import Ballot
from vote import Vote

#Name of the database file
database = "Democracy.db"


class RowExistsError(Exception):
    pass


class DBCursor:

    #    A context manager class to access the database more cleanly
    #
    #    You input the database you want to access and it returns the cursor for it, once it is done
    #    it commits if there are no errors and closes the connection

    def __init__(self, database):
        self.conn = _sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.conn.close()


def _row_exists(table, colname, col):
    with DBCursor(database) as c:
        c.execute(f'SELECT EXISTS(SELECT 1 FROM {table} WHERE {colname} = ?)', (col,))
        return bool(c.fetchone()[0])


def user_exists(userid: str):  # Returns True or False depending if a user rxists in the members table
    return _row_exists(table="members", colname="userid", col=userid)


def vote_exists(votename: str):  # Returns True or False depending if a vote exists in the votes table
    return _row_exists(table="votes", colname="votename", col=votename)


def ballot_exists(userid: str, votename: str):  # Returns if there is a ballot sent by a for a vote
    with DBCursor(database) as c:
        c.execute('SELECT EXISTS(SELECT 1 FROM ballots WHERE userid = ? AND votename = ?)', (userid, votename))
        return bool(c.fetchone()[0])


def create_user(userid: str):  # Inserts a row in the members database, use this to register a new user
    if not user_exists(userid):
        with DBCursor(database) as c:
            c.execute("INSERT INTO members VALUES (?, ?)", (userid, ""))
    else:
        raise RowExistsError  # A user may only have one entry


def create_vote(vote: Vote) -> None:  # Creates a new vote with up to 5 options
    if not vote_exists(vote):
        optiontuple = (vote.options + [0] * (5 - len(vote)))
        with DBCursor(database) as c:
            c.execute('INSERT INTO votes VALUES(?, ?, ?, ?, ?, ?)', (vote.name, *optiontuple))
    else:
        raise RowExistsError  # There should only be one vote


def cast_vote(ballot: Ballot):  # Used by the user to cast their ballot on a vote
    with DBCursor(database) as c:
        if ballot_exists(ballot.userid, ballot.votename):  # If a ballot exists it is updated instead of adding a new one
            c.execute('''UPDATE ballots SET rank1 = ?, rank2 = ?, rank3 = ?, rank4 = ?, rank5 = ?
                        WHERE userid = ? AND votename = ?''', (*ballot.full_ranking, ballot.userid, ballot.votename))
        else:
            c.execute('INSERT INTO ballots VALUES(?, ?, ?, ?, ?, ?, ?)', (ballot.votename, ballot.userid, *ballot.full_ranking))


def represent(userid: str, targetid: str):  # Updates
    if user_exists(userid):
        with DBCursor(database) as c:
            c.execute('UPDATE members SET representativeid = ? WHERE userid = ?', (targetid, userid))
    else:
        raise KeyError(0)


def lookup_representative(userid: str):  # 
    with DBCursor(database) as c:
        c.execute('SELECT  representativeid FROM members WHERE userid = ?', (userid,))
        return c.fetchone()[0]


def lookup_ballots_by_vote(votename: str) -> List[Ballot]:
    with DBCursor(database) as c:
        c.execute('SELECT * FROM ballots WHERE votename = ?', (votename,))
        return [
            Ballot.from_database(elem)
            for elem in c.fetchall()
        ]


def lookup_ballots_by_user(userid: str) -> List[Ballot]:
    with DBCursor(database) as c:
        c.execute('SELECT * FROM ballots WHERE userid = ?', (userid,))
        return [Ballot.from_database(elem) for elem in c.fetchall()]


def lookup_votes() -> List[Vote]:
    with DBCursor(database) as c:
        c.execute('SELECT * FROM votes')
        return [Vote.from_database(elem) for elem in c.fetchall()]


def lookup_vote_by_votename(votename: str) -> Vote:
    with DBCursor(database) as c:
        c.execute('SELECT * FROM votes WHERE votename = ?', (votename,))
        return Vote.from_database(c.fetchone())


def lookup_representing(representativeid: str) -> Set[str]:
    with DBCursor(database) as c:
        c.execute('SELECT userid FROM members WHERE representativeid = ?', (representativeid,))
        return set(item[0] for item in c.fetchall())


def lookup_voting_by_votename(votename: str) -> Set[str]:
    with DBCursor(database) as c:
        c.execute('SELECT userid FROM ballots WHERE votename = ?', (votename,))
        return set(item[0] for item in c.fetchall())


def delete_vote(votename: str) -> bool:
    if vote_exists(votename):
        with DBCursor(database) as c:
            c.execute('DELETE FROM ballots WHERE votename = ?', (votename,))
            c.execute('DELETE FROM votes WHERE votename = ?', (votename,))
        return True
    return False


def delete_ballot(userid: int, votename: str):
    if ballot_exists(userid, votename):
        with DBCursor(database) as c:
            c.execute('DELETE FROM ballots WHERE userid = ? AND votename = ?', (userid, votename))

    else:
        raise KeyError


'''
members table
userid str
representativeid str

votes table
votename str
option1 str
option2 str
option3 str
option4 str
option5 str

ballots table
userid str
votename str
rank1 int
rank2 int
rank3 int
rank4 int
rank5 int
'''