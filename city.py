from enum import Enum
from os import stat
from typing import List
from state import State

class City:

    def __init__(self,name,state,pop,weather,col):
        self.name = name
        self.state = state # 2 letter abbreviation
        self.pop = pop
        self.weather = weather
        self.col = col
        self.matched_prefs = 0
        self.tax_burden = None
        self.econ_freedom = None
        self.social_freedom = None
    
    def __str__(self) -> str:
        return ",".join([self.name,self.state,str(self.pop),self.weather,str(self.col)])

class CitySize(Enum):
    SMALL = 250000
    MEDIUM = 500000
    LARGE = 1000000
    MEGA = 10000000