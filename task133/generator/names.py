"""Business and personal names for the Orari Bank world: South Island places, NZ surnames, activity words."""
import re
from faker import Faker

PLACES = [
    "Orari", "Opihi", "Temuka", "Geraldine", "Pleasant Point", "Fairlie", "Tekapo", "Twizel", "Waimate",
    "Oamaru", "Kurow", "Omarama", "Palmerston", "Waikouaiti", "Mosgiel", "Taieri", "Milton", "Balclutha",
    "Clutha", "Gore", "Mataura", "Winton", "Riverton", "Te Anau", "Lumsden", "Alexandra", "Clyde", "Cromwell",
    "Roxburgh", "Ranfurly", "Wanaka", "Hawea", "Arrowtown", "Frankton", "Glenorchy", "Ashburton", "Methven",
    "Rakaia", "Tinwald", "Hinds", "Rangitata", "Darfield", "Kaiapoi", "Rangiora", "Amberley", "Oxford",
    "Akaroa", "Lincoln", "Rolleston", "Prebbleton", "Halswell", "Sumner", "Lyttelton", "Hornby", "Papanui",
    "Riccarton", "Woolston", "Sydenham", "Burnside", "Mornington", "Caversham", "St Kilda", "Invercargill",
    "Bluff", "Otatara", "Waihao", "Makikihi", "Hakataramea", "Maheno", "Herbert", "Hampden", "Dunback",
    "Middlemarch", "Outram", "Owaka", "Tapanui", "Heriot", "Waikaka", "Edendale", "Wyndham", "Tuatapere",
    "Ohai", "Nightcaps", "Mossburn", "Garston", "Kingston", "Luggate", "Tarras", "Bannockburn", "Pisa",
    "Ophir", "Naseby", "Patearoa", "Hyde", "Macraes", "Moeraki", "Kakanui", "Ngapara", "Duntroon",
    "Waitaki", "Ahuriri", "Pukaki", "Benmore", "Ben Ohau", "Mount Somers", "Mayfield", "Staveley", "Alford",
    "Coldstream", "Seadown", "Washdyke", "Gleniti", "Highfield", "Marchwiel", "Kingsdown", "Claremont",
    "Southern Alps", "Canterbury Plains", "Otago", "Southland", "Mackenzie", "Catlins", "Central Otago",
]
WORDS = ["Alpine", "Southern", "Summit", "Kea", "Tui", "Totara", "Kowhai", "Matai", "Rimu", "Tussock",
         "Plains", "Valley", "Lakes", "High Country", "Braided River", "Gorge", "Ridgeline", "Coastal",
         "Bluestone", "Schist", "Kahu", "Pukeko", "Weka", "Harrier", "Kereru", "Manuka", "Kanuka", "Southerly",
         "Nor'west", "Frontier", "Cornerstone", "Keystone", "Ironbark", "Silverpeak", "Clearwater", "Riverstone"]

ACT = {  # activity words by BIC code prefix (class)
    "C1111": ["Meats", "Meat Processors", "Butchery Wholesale"], "C1131": ["Dairy", "Milk Company"],
    "C1174": ["Bakery", "Bakehouse", "Pies"], "C1214": ["Wines", "Vineyards", "Winery"],
    "C1199": ["Foods", "Kitchen", "Preserves", "Specialty Foods"],
    "C1491": ["Homes Manufacturing", "Transportable Homes", "Prefab Buildings"],
    "C1499": ["Joinery", "Kitchens & Joinery", "Cabinetry"], "C2034": ["Concrete Products", "Precast", "Concrete"],
    "C2221": ["Steel Fabrication", "Engineering & Steel", "Steel"], "C2229": ["Aluminium", "Windows & Doors", "Glass & Aluminium"],
    "C2462": ["Agricultural Engineering", "Farm Machinery", "Ag Engineering"], "C2499": ["Engineering", "Machinery", "Fabrication"],
    "C2319": ["Trailers", "Trailer Manufacturing", "Caravans"], "C1611": ["Print", "Printing", "Print & Design"],
    "C1912": ["Plastics", "Mouldings", "Packaging"],
    "A0160": ["Dairy Farm", "Dairies", "Farming"], "A0144": ["Station", "Farming", "Pastoral"],
    "A0141": ["Farming", "Station", "Merinos"], "A0131": ["Vineyards", "Wines", "Estate"],
    "A0529": ["Contracting", "Ag Contracting", "Agricultural Services"], "A0301": ["Forestry", "Forest Management", "Logging"],
    "B0911": ["Quarries", "Aggregates", "Gravel"], "B0600": ["Coal", "Mining"],
    "D2612": ["Power", "Energy", "Hydro"], "D2811": ["Water", "Water Services"], "D2921": ["Waste", "Bins", "Waste Services"],
    "E3011": ["Builders", "Homes", "Building", "Construction"], "E3019": ["Construction", "Builders", "Developments"],
    "E3020": ["Construction", "Commercial Builders", "Contractors"], "E3101": ["Civil", "Roading", "Civil Contracting"],
    "E3109": ["Civil", "Earthworks", "Contracting", "Infrastructure"], "E3221": ["Concrete", "Concreting", "Concrete Placers"],
    "E3223": ["Roofing", "Roofing Solutions", "Spouting & Roofing"], "E3231": ["Plumbing", "Plumbing & Gas", "Plumbers"],
    "E3232": ["Electrical", "Electrical Services", "Sparkies"], "E3242": ["Carpentry", "Builders", "Joinery & Building"],
    "E3243": ["Flooring", "Tiling", "Carpets"], "E3244": ["Painters", "Decorators", "Painting"],
    "E3291": ["Landscapes", "Landscaping", "Gardens"],
    "F3331": ["Timber", "Timber Supplies", "Sawmilling"], "F3332": ["Plumbing Supplies", "Bathroom Supplies"],
    "F3339": ["Building Supplies", "Building Products", "Trade Supplies"], "F3601": ["Foodservice", "Food Distributors", "Wholesale Foods"],
    "F3602": ["Meat Supplies", "Smallgoods", "Meat Distributors"], "F3604": ["Fresh Produce", "Produce", "Fruit & Vege"],
    "F3319": ["Rural Supplies", "Farm Supplies", "Agri Supplies"], "F3411": ["Tractors", "Machinery", "Agri Machinery"],
    "F3499": ["Distributors", "Trading", "Imports"], "F3712": ["Paper", "Packaging Supplies", "Office Supplies"],
    "G4110": ["Supermarket", "Foodmarket", "Grocer"], "G4121": ["Butchery", "Meats", "Quality Meats"],
    "G4214": ["Furniture", "Furnishings", "Beds & Furniture"], "G4231": ["Hardware", "Home & Hardware", "Mitre"],
    "G4251": ["Clothing", "Menswear", "Outfitters", "Boutique"], "G4271": ["Pharmacy", "Chemist", "Health Pharmacy"],
    "G4000": ["Fuels", "Service Station", "Fuel Stop"], "G3911": ["Motors", "Cars", "Motor Group"],
    "G4241": ["Outdoors", "Sports", "Ski & Bike"],
    "H4400": ["Lodge", "Hotel", "Resort", "Holiday Park", "Retreat"], "H4400_": ["Motel", "Motor Lodge", "Motor Inn"],
    "H4511": ["Cafe", "Espresso", "Eatery", "Kitchen", "Bistro", "Restaurant"], "H4512": ["Takeaways", "Fish & Chips", "Burgers"],
    "H4513": ["Catering", "Events Catering"], "H4520": ["Tavern", "Hotel", "Bar", "Brewery Bar"],
    "I4610": ["Transport", "Freight", "Haulage", "Carriers", "Logistics"], "I4621": ["Buses", "Coachlines", "Shuttles"],
    "I4622": ["Tours", "Coach Tours", "Scenic Tours"], "I4820": ["Cruises", "Jetboats", "Boat Tours"],
    "I4900": ["Scenic Flights", "Helicopters", "Air"], "I5102": ["Couriers", "Express", "Delivery"],
    "I5309": ["Storage", "Warehousing", "Coolstores"],
    "J5411": ["News", "Publishing", "Media"], "J5802": ["Telecom", "Networks", "Communications"],
    "K6322": ["Insurance", "Mutual Insurance"], "K6330": ["Compensation"], "K6419": ["Payments", "Merchant Services"],
    "K6240": ["Investments", "Capital"],
    "L6631": ["Hire", "Plant Hire", "Scaffolding", "Equipment Hire"], "L6632": ["Rentals", "Vehicle Hire", "Truck Rentals"],
    "L6711": ["Properties", "Holdings"], "L6712": ["Property", "Properties", "Investments"],
    "L6720": ["Realty", "Real Estate", "Property Brokers"],
    "M6921": ["Architects", "Design", "Architecture"], "M6922": ["Surveyors", "Surveying", "Land Surveys"],
    "M6923": ["Engineering", "Consulting Engineers", "Engineers"], "M6931": ["Law", "Lawyers", "Legal"],
    "M6932": ["Chartered Accountants", "Accountants", "Accounting"], "M7000": ["Technology", "IT", "Software", "Digital"],
    "M6940": ["Advertising", "Marketing", "Creative"], "M6970": ["Vets", "Veterinary Services", "Vet Clinic"],
    "N7311": ["Cleaning", "Cleaning Services", "Commercial Cleaners"], "N7212": ["Staffing", "Recruitment", "Labour Hire", "Workforce"],
    "N7712": ["Security", "Guards", "Patrols"], "N7220": ["Travel", "Tours & Travel", "Tour Bookings"],
    "N7291": ["Admin Services", "Business Services"],
    "O7530": ["District Council"], "O7510": ["Ministry"], "O7713": ["Fire & Emergency"],
    "P8010": ["Kindergarten", "Early Learning", "Childcare"], "P8219": ["Training", "Academy", "Learning Centre"],
    "P8021": ["School"],
    "Q8531": ["Dental", "Dentists", "Dental Care"], "Q8533": ["Physiotherapy", "Physio", "Sports Physio"],
    "Q8601": ["Rest Home", "Care Home", "Retirement Care"], "Q8511": ["Medical Centre", "Health Centre", "Doctors"],
    "Q8401": ["Hospital", "Surgical Hospital"],
    "R9113": ["Fitness", "Gym", "Sports Centre"], "R9139": ["Adventures", "Activities", "Ski Area", "Golf Club"],
    "R9001": ["Theatre", "Productions", "Events"], "R8910": ["Museum", "Heritage Centre"],
    "S9412": ["Panelbeaters", "Collision Repairs", "Auto Body"], "S9419": ["Automotive", "Motors", "Auto Services", "Mechanical"],
    "S9511": ["Hair", "Hair Studio", "Barbers"], "S9511_": ["Beauty", "Beauty Therapy", "Skin Clinic"],
    "S9531": ["Laundry", "Linen Services", "Drycleaners"],
}


def act_words(bic):
    key = bic[:5]
    if bic in ("H440020",):
        key = "H4400_"
    if bic in ("S951120",):
        key = "S9511_"
    return ACT.get(key, ["Services"])


class Namer:
    def __init__(self, rng, seed):
        self.rng = rng
        self.fk = Faker("en_NZ")
        self.fk.seed_instance(seed)
        self.used = set()

    def surname(self):
        return self.fk.last_name()

    def person(self):
        return self.fk.first_name(), self.fk.last_name()

    def business(self, bic):
        r = self.rng
        a = act_words(bic)
        for _ in range(200):
            act = a[r.integers(len(a))]
            shape = r.choice(8, p=[.30, .22, .08, .10, .08, .08, .07, .07])
            if shape == 0:
                core = f"{PLACES[r.integers(len(PLACES))]} {act}"
            elif shape == 1:
                core = f"{self.surname()} {act}"
            elif shape == 2:
                core = f"{self.surname()} & {self.surname()}"
            elif shape == 3:
                core = f"{WORDS[r.integers(len(WORDS))]} {act}"
            elif shape == 4:
                core = f"{self.surname()} {act} ({r.integers(1998, 2024)})"
            elif shape == 5:
                core = f"{PLACES[r.integers(len(PLACES))]} {act} ({r.integers(1998, 2024)})"
            elif shape == 6:
                core = f"{self.surname()} Group"
            else:
                core = f"{self.surname()} Holdings"
            name = core + " Limited"
            if name not in self.used:
                self.used.add(name)
                return name
        raise RuntimeError("name space exhausted for " + bic)


def bank_party(name):
    """How a payer's name arrives on an Orari Bank statement: upper case, Limited shortened, 20 characters."""
    s = name.upper().replace(" LIMITED", " LTD").replace("&", "AND")
    s = re.sub(r"[^A-Z0-9 ()']", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:20].rstrip()
