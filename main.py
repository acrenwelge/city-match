import csv
import argparse
from unittest import result
from city import City, CitySize
from state import State
from user_preferences import UserPreferences
from typing import List
from prettytable import PrettyTable

citylist: List[City] = None
statelist: List[State] = None

def main():
    read_csv_data()
    # uncomment line below to change input to CLI args instead of interactive prompt
    # prefs = get_prefs_from_cli()
    prefs = get_user_preferences()
    results = match_city_with_prefs(citylist, prefs)
    display_prefs(prefs)
    print()
    display_results(results, len(prefs))

def read_csv_data():
    global citylist
    global statelist
    citylist = read_csv_cities()
    statelist = read_csv_states()
    for city in citylist:
        for state in statelist:
            if city.state == state.abbr:
                city.tax_burden = state.tax_burden
                city.social_freedom = state.social_freedom
                city.econ_freedom = state.econ_freedom

def read_csv_cities():
    with open('./cities.csv') as f:
        cityreader = csv.reader(f)
        citylist = []
        next(cityreader)
        for city in cityreader:
            insert_city = City(city[1],city[2],int(city[3]),city[4],float(city[5]))
            citylist.append(insert_city)
        return citylist

def read_csv_states():
    with open('./states.csv') as f:
        statereader = csv.reader(f)
        statelist = []
        next(statereader)
        for st in statereader:
            insert_state = State(st[1],st[2],None,float(st[3]),float(st[4]),float(st[5]))
            statelist.append(insert_state)
        return statelist

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
    user_prefs = []
    print("How many users are you matching preferences for?")
    num_users = int(input())
    if num_users < 1:
        raise RuntimeError('Number of users must be 1 or more')
    user_prefs = [UserPreferences() for x in range(num_users)]
    for idx, user_pref in enumerate(user_prefs):
        print("Enter preferences for user {}".format(idx+1))
        print("""Choose your preference for weather/climate:
        1. TROPICAL
        2. COLD/SNOWY
        3. ARID/DESERT
        4. TEMPERATE""")
        weatherPref = int(input())
        if weatherPref == 1:
            user_pref.weather = "TROPICAL"
        elif weatherPref == 2:
            user_pref.weather = "COLD/SNOWY"
        elif weatherPref == 3:
            user_pref.weather = "ARID/DESERT"
        elif weatherPref == 4:
            user_pref.weather = "TEMPERATE"
        print("""Choose your preference for city size:
        1. < 250k
        2. 250k - 500k
        3. 500k - 1M
        4. >1M""")
        size_choice = int(input())
        if size_choice == 1:
            user_pref.size_min = 0
            user_pref.size_max = CitySize.SMALL.value
        elif size_choice == 2:
            user_pref.size_min = CitySize.SMALL.value
            user_pref.size_max = CitySize.MEDIUM.value
        elif size_choice == 3:
            user_pref.size_min = CitySize.MEDIUM.value
            user_pref.size_max = CitySize.LARGE.value
        elif size_choice == 4:
            user_pref.size_min = CitySize.LARGE.value
            user_pref.size_max = CitySize.MEGA.value
    print("""How would you like the results sorted?
    1. Alphabetically
    2. By Population Size
    3. By Cost of Living
    4. By Tax Burden
    """)
    sort_choice = int(input())
    if sort_choice == 1:
        user_pref.sort = "ALPHA"
    elif sort_choice == 2:
        user_pref.sort = "POP"
    elif sort_choice == 3:
        user_pref.sort = "COL"
    elif sort_choice == 4:
        user_pref.sort = "TAX"
    user_prefs[idx] = user_pref
    return user_prefs

def match_city_with_prefs(cities: List[City], prefs: List[UserPreferences]):
    """Filter and sort the list of cities by the preferences most in common amongst the users.
    The algorithm should consolidate the list of preferences into a single set of preferences by 
    counting how many users' preferences it fulfills. The results should be sorted to prioritize 
    cities that meet ALL user preferences, then ranked by most to least preferences matched.
    """
    if len(prefs) == 1:
        pref = prefs[0]
        filtered = list(filter(lambda city: city.pop >= pref.size_min and city.pop <= pref.size_max and city.weather == pref.weather, cities))
        if pref.sort == "ALPHA":
            filtered.sort(key=lambda city: city.name)
        elif pref.sort == "POP":
            filtered.sort(key=lambda city: city.pop, reverse=True)
        elif pref.sort == "COL":
            filtered.sort(key=lambda city: city.col)
        elif pref.sort == "TAX":
            filtered.sort(key=lambda city: city.tax_burden)
        return filtered
    else:
        for city in cities:
            for pref in prefs:
                if city.pop >= pref.size_min and city.pop <= pref.size_max and city.weather == pref.weather:
                    city.matched_prefs = city.matched_prefs + 1
        filtered = list(filter(lambda c: c.matched_prefs > 0,cities))
        filtered.sort(key=lambda c: c.matched_prefs, reverse=True)
        return filtered

def display_prefs(prefs: List[UserPreferences]):
    pt = PrettyTable()
    pt.field_names = ['User','Weather','Min Size','Max Size']
    for idx, p in enumerate(prefs):
        pt.add_row([f'User {idx+1}',p.weather,p.size_min,p.size_max])
    print("SUMMARY OF PREFERENCES")
    print(pt)

def display_results(cities: List[City], num_users: int):
    pt = PrettyTable()
    if len(cities) == 0:
        print('No cities found that match your criteria')
    else:
        pt.field_names = ['# Matches','City Name','Population','Weather','Cost of Living','Tax Burden','Economic Freedom','Social Freedom']
        for c in cities:
            pt.add_row([str(c.matched_prefs)+'/'+str(num_users),c.name,f"{c.pop:,}",c.weather,c.col,c.tax_burden,c.econ_freedom,c.social_freedom])
        print("CITY RESULTS")
        print(pt)

if __name__ == "__main__":
    main()