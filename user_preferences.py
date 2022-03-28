from enum import Enum
from pickle import POP
from city import CitySize

class UserPreferences:

    def __init__(self, weather = None, size_min = 0, size_max = CitySize.MEGA.value, sort = "ALPHA"):
        self.weather = weather
        self.size_min = size_min
        self.size_max = size_max
        self.sort = sort