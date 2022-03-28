import csv
import argparse
from city import City, CitySize
from user_preferences import UserPreferences

def main():
    citylist = read_csv()
    prefs = get_prefs_from_cli()
    # prefs = get_user_preferences()
    match_city_with_prefs(citylist, prefs)

def get_prefs_from_cli():
    parser = argparse.ArgumentParser(description="Find a city that matches your preferences")
    parser.add_argument("-weather")
    parser.add_argument("-min", metavar='MIN', default=0,type=int,help="The minimum population of the city")
    parser.add_argument("-max", metavar='MAX', default=10_000_000,type=int,help="The maximum population of the city")
    parser.add_argument("-s", metavar='SORT', default="ALPHA",help="The parameter to sort by. Opts=ALPHA,POP,COL,TAX")
    args = parser.parse_args()
    user_prefs = UserPreferences()
    user_prefs.size_min = args.min
    user_prefs.size_max = args.max
    user_prefs.weather = args.weather
    user_prefs.sort = args.s
    return user_prefs

def get_user_preferences():
    user_prefs = UserPreferences()
    print("""Choose your preference for weather/climate:
    1. TROPICAL
    2. COLD/SNOWY
    3. ARID/DESERT
    4. TEMPERATE""")
    weatherPref = int(input())
    if weatherPref == 1:
        user_prefs.weather = "TROPICAL"
    elif weatherPref == 2:
        user_prefs.weather = "COLD/SNOWY"
    elif weatherPref == 3:
        user_prefs.weather = "ARID/DESERT"
    elif weatherPref == 4:
        user_prefs.weather = "TEMPERATE"
    print(user_prefs.weather)
    print("""Choose your preference for city size:
    1. < 250k
    2. 250k - 500k
    3. 500k - 1M
    4. >1M""")
    size_choice = int(input())
    if size_choice == 1:
        user_prefs.size_min = 0
        user_prefs.size_max = CitySize.SMALL
    elif size_choice == 2:
        user_prefs.size_min = CitySize.SMALL
        user_prefs.size_max = CitySize.MEDIUM
    elif size_choice == 3:
        user_prefs.size_min = CitySize.MEDIUM
        user_prefs.size_max = CitySize.LARGE
    elif size_choice == 4:
        user_prefs.size_min = CitySize.LARGE
        user_prefs.size_max = CitySize.MEGA
    return user_prefs

def match_city_with_prefs(cities, prefs):
    filtered = list(filter(lambda city: city.pop >= prefs.size_min and city.pop <= prefs.size_max and city.weather == prefs.weather, cities))
    if prefs.sort == "ALPHA":
        filtered.sort(key=lambda city: city.name)
    elif prefs.sort == "POP":
        filtered.sort(key=lambda city: city.pop, reverse=True)
    elif prefs.sort == "COL":
        filtered.sort(key=lambda city: city.col)
    elif prefs.sort == "TAX":
        filtered.sort(key=lambda city: city.tax_burden)
    for c in filtered:
        print(c)

def read_csv():
    with open('./cities.csv') as f:
        cityreader = csv.reader(f)
        citylist = []
        next(cityreader)
        for city in cityreader:
            cityToInsert = City(city[1],city[2],int(city[3]),city[4],float(city[5]),float(city[6]))
            citylist.append(cityToInsert)
        return citylist

if __name__ == "__main__":
    main()