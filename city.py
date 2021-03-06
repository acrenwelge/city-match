from enum import Enum

class City:

    def __init__(self,name,state,pop,weather,col):
        self.name = name
        self.state = state
        self.pop = pop
        self.weather = weather
        self.col = col
    
    def __str__(self) -> str:
        return ",".join([self.name,self.state,str(self.pop),self.weather,str(self.col)])

class CitySize(Enum):
    SMALL = 250000
    MEDIUM = 500000
    LARGE = 1000000
    MEGA = 10000000