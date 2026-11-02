"""Place and shop names for the fictional country (localities invented; shop surnames drawn from
faker's en_NZ index with a fixed seed)."""
from faker import Faker

LOCALITIES = {
    "CR01": ["Kings Wharf", "Market Hill", "Albion Square"],
    "CR02": ["Northgate", "Ellerby", "Fernside", "Upper Harrow"],
    "CR03": ["Southmead", "Clayton Park", "Riverside East"],
    "CR04": ["Eastwick", "Pellin Bay", "Sandhaven"],
    "CR05": ["Belmont", "Oakridge", "Linton Falls"],
    "CR06": ["Wexcombe", "Ashgrove", "Dunmore"],
    "CR07": ["Tamsin", "Port Avery", "Kelso Point"],
    "CR08": ["Greywater", "Ashcott", "Millbrook"],
    "CR09": ["Ardmore", "Glenhallow", "Crickwood"],
    "CR10": ["Fenwick", "Stanbury", "Lowfield"],
    "CR11": ["Corran", "Maddox Heads", "Saltford"],
    "CR12": ["Westholm", "Brindle", "Carrow Vale"],
    "CR13": ["Rookby", "Hatherley", "Gorse Hill"],
    "CR14": ["Northreach", "Tallow Creek", "Ivydale"],
}

STREETS = ["Main Street", "High Street", "Victoria Road", "Station Road", "Church Street", "Queen Street",
           "Harbour Road", "Mill Lane", "Park Road", "Bridge Street", "Market Street", "King Street",
           "Hillside Road", "Beach Road", "North Road", "South Road", "Elm Avenue", "Union Street"]

# surnames for independent shop names, from faker's en_NZ index with a fixed seed; words that read as
# adjectives in a shop name are passed over
_ADJECTIVES = {"Small", "Little", "Long", "Short", "Young", "Best", "Rich", "Good", "Fair", "Sharp", "Sweet",
               "Strong", "Wise", "Gay", "Hardy", "Bright", "Moody", "Love", "Hope", "Bacon", "Lamb", "Baker",
               "Butcher", "Cook", "Fish", "Fry", "Taylor", "Draper", "Chemist"}
_fake = Faker("en_NZ")
_fake.seed_instance(233)
_surnames = []
while len(_surnames) < 160:
    s = _fake.last_name()
    if s not in _surnames and s not in _ADJECTIVES and " " not in s:
        _surnames.append(s)
SURNAMES = _surnames

# how an independent outlet of each kind is named ({s} a surname, {loc} the outlet's locality)
KIND_NAMES = {
    "greengrocer": ["{s} Fruit and Vege", "{loc} Fresh Produce", "{s} Fruiterers", "{s} Greengrocers"],
    "butcher": ["{s} Butchery", "{loc} Meat Co", "{s} and Sons Butchers", "{s} Quality Meats"],
    "bakery": ["{s} Bakery", "{loc} Bakehouse", "{s} Hot Bread Shop"],
    "convenience": ["{s} Superette", "{loc} Dairy", "{s} Corner Store", "{s} Family Store"],
    "pharmacy": ["{s} Pharmacy", "{loc} Chemist", "{s} Chemist"],
    "boutique": ["{s} Clothing", "{loc} Outfitters", "{s} Drapers", "{s} Menswear"],
    "hardware": ["{s} Hardware", "{loc} Home and Garden", "{s} Building Supplies"],
}

# the size of the shop-name list the outlet draw permutes (kept so every later draw in that stream holds)
SHOP_NAME_DRAW = 47
