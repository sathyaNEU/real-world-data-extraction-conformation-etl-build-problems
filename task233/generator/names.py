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

_fake = Faker("en_NZ")
_fake.seed_instance(233)
_surnames = []
while len(_surnames) < 40:
    s = _fake.last_name()
    if s not in _surnames:
        _surnames.append(s)

_TEMPLATES = [
    "{s} Fruit and Vege", "{s} Butchery", "{s} Bakery", "{s} Superette", "{s} Pharmacy",
    "{s} Clothing", "{s} Hardware", "%(loc)s Fresh Produce", "%(loc)s Meat Co", "%(loc)s Bakehouse",
    "%(loc)s Dairy", "%(loc)s Chemist", "%(loc)s Outfitters", "%(loc)s Home and Garden",
    "{s} Family Store", "{s} and Sons Butchers", "{s} Corner Store", "{s} Drapers",
]

SHOP_NAMES = []
for i, s in enumerate(_surnames):
    SHOP_NAMES.append(_TEMPLATES[i % len(_TEMPLATES)].format(s=s))
for t in _TEMPLATES:
    if "%(loc)s" in t:
        SHOP_NAMES.append(t)
