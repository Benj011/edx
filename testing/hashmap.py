from collections import defaultdict

city_map = defaultdict(list) # this is the default dictionary way, list is the type if how you are storign the data

# city_map = {}

cities_c = ["Calagary", "Vancouver", "Toronto"]
# city_map["Canada"] = []
city_map["Canada"] += cities_c

cities_a = ["denver", "chicago", "New York"]
city_map["USA"] += cities_a

cities_e = ["london", "paris", "berlin"]
city_map["Europe"] += cities_e

print(city_map.items())
