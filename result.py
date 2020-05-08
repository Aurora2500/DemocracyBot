# result.py

from typing import Dict

from vote import Vote

class Result:
    def __init__(self, result_dict, vote: Vote):
        self.result_dict = result_dict
        self.vote = vote