"""Industry classes (NZ Business Industry Classification codes on ANZSIC 2006 classes) and the business
types the world is built from. A BIC code is the division letter, the four-digit ANZSIC 2006 class and a
two-digit activity suffix."""

# BIC code -> description. The division is the first letter.
BIC = {
    # A
    "A016010": "Dairy cattle farming", "A014410": "Sheep-beef cattle farming", "A014110": "Sheep farming (specialised)",
    "A013110": "Grape growing", "A052910": "Agricultural contracting services", "A030110": "Forestry",
    # B
    "B091110": "Gravel and sand quarrying", "B060010": "Coal mining",
    # C
    "C111110": "Meat processing", "C113110": "Milk and cream processing", "C117420": "Bakery product manufacturing (non-factory based)",
    "C121410": "Wine making", "C119910": "Other food product manufacturing n.e.c.",
    "C149110": "Prefabricated wooden building manufacturing", "C149930": "Joinery manufacturing (timber)",
    "C203410": "Concrete product manufacturing", "C222110": "Structural steel fabricating",
    "C222920": "Aluminium window and door manufacturing", "C246210": "Agricultural machinery manufacturing",
    "C249910": "Machinery and equipment manufacturing n.e.c.", "C161110": "Printing",
    "C191210": "Plastic product manufacturing", "C231910": "Trailer and caravan manufacturing",
    # D
    "D261210": "Hydro-electricity generation", "D281110": "Water supply", "D292110": "Waste collection services",
    # E
    "E301110": "House construction", "E301910": "Residential building construction n.e.c.",
    "E302010": "Non-residential building construction", "E310110": "Road and bridge construction",
    "E310910": "Heavy and civil engineering construction n.e.c.", "E322110": "Concreting services",
    "E322310": "Roofing services", "E323110": "Plumbing services", "E323210": "Electrical services",
    "E324210": "Carpentry services", "E324310": "Tiling and carpeting services",
    "E324410": "Painting and decorating services", "E329110": "Landscape construction services",
    # F
    "F333110": "Timber wholesaling", "F333210": "Plumbing goods wholesaling", "F333910": "Building supplies wholesaling n.e.c.",
    "F360110": "General line grocery wholesaling", "F360210": "Meat and smallgoods wholesaling",
    "F360410": "Fruit and vegetable wholesaling", "F331910": "Rural supplies wholesaling",
    "F341110": "Agricultural machinery wholesaling", "F349910": "Other goods wholesaling n.e.c.",
    "F371210": "Paper product wholesaling",
    # G
    "G411010": "Supermarket and grocery stores", "G412110": "Butcher shop", "G421410": "Furniture retailing",
    "G423110": "Hardware and building supplies retailing", "G425110": "Clothing retailing",
    "G427110": "Pharmacy", "G400010": "Fuel retailing", "G391110": "Car retailing", "G424110": "Sport and camping goods retailing",
    # H
    "H440010": "Accommodation", "H440020": "Motel operation", "H451110": "Cafe operation",
    "H451120": "Restaurant operation", "H451210": "Takeaway food services", "H451310": "Catering services",
    "H452010": "Tavern and bar operation",
    # I
    "I461010": "Road freight transport", "I462110": "Interurban and rural bus transport",
    "I462220": "Tour coach operation", "I482010": "Water passenger transport (tourism)",
    "I510210": "Courier pick-up and delivery services", "I530910": "Warehousing and storage services n.e.c.",
    "I490010": "Air and space transport (scenic flights)",
    # J
    "J541110": "Newspaper publishing", "J580210": "Telecommunications services",
    # K
    "K624010": "Financial asset investing", "K632210": "General insurance", "K641910": "Auxiliary finance services n.e.c.",
    "K641920": "Card payment processing services", "K633010": "Accident compensation insurance",
    # L
    "L663110": "Heavy machinery and scaffolding hiring", "L663210": "Other motor vehicle and transport equipment hiring",
    "L671110": "Residential property operation", "L671210": "Non-residential property operation",
    "L672010": "Real estate agency services",
    # M
    "M692110": "Architectural services", "M692210": "Surveying and mapping services",
    "M692310": "Engineering design and consulting services", "M693110": "Legal services",
    "M693210": "Accounting services", "M700010": "Computer system design services",
    "M694010": "Advertising services", "M697010": "Veterinary services",
    # N
    "N731110": "Building cleaning services", "N721210": "Labour supply services",
    "N771210": "Security services", "N722010": "Travel agency and tour arrangement services",
    "N729110": "Office administrative services",
    # O
    "O753010": "Local government administration", "O751010": "Central government administration",
    "O771310": "Fire protection and emergency services",
    # P
    "P801010": "Early childhood education", "P821910": "Adult and community education n.e.c.",
    "P802110": "Private school education",
    # Q
    "Q853110": "Dental services", "Q853310": "Physiotherapy services", "Q860110": "Aged care residential services",
    "Q851110": "General practice medical services", "Q840110": "Hospitals",
    # R
    "R911310": "Sports and physical recreation venues", "R913910": "Amusement and recreation activities n.e.c.",
    "R900110": "Performing arts operation", "R891010": "Museum operation",
    # S
    "S941210": "Automotive body, paint and interior repair", "S941910": "Automotive repair and maintenance n.e.c.",
    "S951110": "Hairdressing services", "S951120": "Beauty services", "S953110": "Laundry and dry-cleaning services",
}

# The old platform's 1993 codes for a few classes (borrowers migrated in 2019 carry these on the loan file).
ANZSIC93 = {
    "C222110": "C2751", "C149930": "C2323", "C119910": "C2179", "C246210": "C2861", "E323210": "E4232",
    "E301110": "E4111", "F333910": "F4539", "F360110": "F4711", "I461010": "I6110", "L663110": "L7742",
    "M692310": "L7823", "M693210": "L7842", "N731110": "L7866", "N721210": "L7861", "H451120": "H5730",
    "G411010": "G5110", "S941210": "Q9512", "Q853310": "O8635",
}

# Business types of Orari Bank's business banking customers.
# own: BIC codes the type is classed in; n: customers; ead: median exposure (NZD thousand);
# mix: template shares of sales by source: a division letter for business payers, HH for households
# (card settlements, private payers, cash), GOV for government payers (classed O, K or Q in the register).
TYPES = {
    "food_mfr":      dict(own=["C111110", "C117420", "C119910", "C121410"], n=21, ead=900,
                          mix={"G": .45, "H": .30, "F": .20, "HH": .05}),
    "building_mfr":  dict(own=["C149110", "C149930", "C203410", "C222110", "C222920"], n=22, ead=1150,
                          mix={"E": .85, "HH": .15}),
    "machinery_mfr": dict(own=["C246210", "C249910", "C231910"], n=15, ead=1000,
                          mix={"A": .35, "E": .25, "C": .20, "B": .10, "D": .10}),
    "other_mfr":     dict(own=["C161110", "C191210"], n=17, ead=780,
                          mix={"G": .32, "C": .30, "F": .20, "M": .08, "HH": .10}),
    "home_builder":  dict(own=["E301110", "E301910"], n=48, ead=820,
                          mix={"HH": .90, "E": .10}),
    "trades":        dict(own=["E322110", "E322310", "E323110", "E323210", "E324210", "E324310", "E324410", "E329110"],
                          n=50, ead=380, mix={"E": .70, "HH": .25, "GOV": .05}),
    "civil":         dict(own=["E310110", "E310910", "E302010"], n=7, ead=1400,
                          mix={"GOV": .70, "D": .20, "E": .10}),
    "foodservice_wh": dict(own=["F360110", "F360210", "F360410"], n=18, ead=1250,
                           mix={"H": .70, "Q": .15, "G": .15}),
    "building_wh":   dict(own=["F333110", "F333210", "F333910"], n=14, ead=1450,
                          mix={"E": .75, "HH": .25}),
    "rural_wh":      dict(own=["F331910", "F341110"], n=12, ead=1350,
                          mix={"A": .80, "HH": .20}),
    "general_wh":    dict(own=["F349910", "F371210"], n=15, ead=1050,
                          mix={"G": .70, "H": .10, "C": .10, "HH": .10}),
    "retail":        dict(own=["G411010", "G412110", "G421410", "G425110", "G427110", "G400010", "G391110", "G424110"],
                          n=70, ead=540, mix={"HH": .95, "G": .05}),
    "accommodation": dict(own=["H440010", "H440020"], n=34, ead=1850, mix={"HH": 1.0}),
    "food_service":  dict(own=["H451110", "H451120", "H451210", "H452010"], n=47, ead=320,
                          mix={"HH": .95, "M": .05}),
    "freight":       dict(own=["I461010"], n=27, ead=1250,
                          mix={"E": .35, "A": .25, "C": .20, "G": .10, "F": .10}),
    "tour_transport": dict(own=["I462220", "I482010", "I490010", "I462110"], n=15, ead=1100, mix={"HH": 1.0}),
    "courier":       dict(own=["I510210", "I530910"], n=10, ead=650,
                          mix={"G": .40, "F": .30, "C": .30}),
    "plant_hire":    dict(own=["L663110", "L663210"], n=15, ead=1300,
                          mix={"E": .75, "A": .15, "HH": .10}),
    "engineering":   dict(own=["M692310", "M692210", "M692110"], n=27, ead=450,
                          mix={"E": .55, "GOV": .25, "C": .10, "A": .10}),
    "accounting_law": dict(own=["M693110", "M693210"], n=21, ead=380,
                           mix={"HH": .40, "C": .10, "G": .12, "Q": .10, "S": .10, "I": .08, "J": .10}),
    "it_marketing":  dict(own=["M700010", "M694010"], n=14, ead=330,
                          mix={"G": .25, "H": .25, "C": .20, "M": .15, "N": .15}),
    "vet":           dict(own=["M697010"], n=6, ead=520, mix={"A": .60, "HH": .40}),
    "cleaning":      dict(own=["N731110"], n=14, ead=420,
                          mix={"H": .50, "M": .20, "GOV": .15, "Q": .15}),
    "labour_hire":   dict(own=["N721210"], n=14, ead=550,
                          mix={"E": .60, "A": .25, "C": .15}),
    "security":      dict(own=["N771210"], n=9, ead=380,
                          mix={"R": .35, "G": .30, "GOV": .20, "E": .15}),
    "education":     dict(own=["P801010", "P821910"], n=8, ead=650, mix={"HH": .70, "GOV": .30}),
    "health":        dict(own=["Q853110", "Q853310", "Q860110", "Q851110"], n=21, ead=1000,
                          mix={"HH": .50, "GOV": .50}),
    "recreation":    dict(own=["R911310", "R913910", "R900110"], n=17, ead=700, mix={"HH": .90, "H": .10}),
    "auto_repair":   dict(own=["S941210", "S941910"], n=23, ead=420, mix={"HH": .50, "K": .35, "I": .15}),
    "personal":      dict(own=["S951110", "S951120", "S953110"], n=14, ead=170, mix={"HH": 1.0}),
}

# Classes a business payer in each division is drawn from, and how many payer firms the region holds.
PAYER_CLASSES = {
    "A": (["A016010", "A014410", "A014110", "A013110", "A052910", "A030110"], 260),
    "B": (["B091110", "B060010"], 30),
    "C": (["C111110", "C113110", "C117420", "C119910", "C149930", "C203410", "C222110", "C161110", "C191210"], 170),
    "D": (["D261210", "D281110", "D292110"], 25),
    "E": (["E301110", "E301910", "E302010", "E310910", "E322110", "E323210", "E324210"], 300),
    "F": (["F333110", "F333910", "F360110", "F349910", "F331910"], 120),
    "G": (["G411010", "G412110", "G421410", "G423110", "G425110", "G427110", "G400010"], 200),
    "H": (["H440010", "H440020", "H451110", "H451120", "H452010", "H451310"], 260),
    "I": (["I461010", "I462220", "I510210", "I530910"], 80),
    "J": (["J541110", "J580210"], 25),
    "K": (["K632210", "K633010"], 18),
    "L": (["L671210", "L672010", "L663110"], 60),
    "M": (["M692310", "M693110", "M693210", "M700010", "M692110"], 120),
    "N": (["N731110", "N721210", "N729110", "N722010"], 60),
    "O": (["O753010", "O751010", "O771310"], 22),
    "P": (["P801010", "P802110"], 25),
    "Q": (["Q860110", "Q851110", "Q840110", "Q853110"], 60),
    "R": (["R911310", "R900110", "R913910"], 40),
    "S": (["S941910", "S953110"], 40),
}

# Industry sales in the year to September 2026, NZD million (South Island regions), and the year-on-year
# path of the last five years by division (per cent); the series file is built from these.
BASE_SALES = {
    "A": 18450, "B": 1320, "C": 24890, "D": 4210, "E": 15760, "F": 14320, "G": 16980, "H": 7340,
    "I": 6910, "J": 2210, "K": 5180, "L": 6640, "M": 7930, "N": 4120, "O": 6050, "P": 1890,
    "Q": 8460, "R": 1480, "S": 3150,
}
YOY_PATH = {  # year to Sep 2022, 2023, 2024, 2025, 2026
    "A": [9.8, 3.1, -6.2, 4.4, 2.1], "B": [5.2, 7.9, 1.1, -2.4, -3.0], "C": [8.1, 6.4, 0.9, -1.2, -1.0],
    "D": [4.2, 6.8, 5.1, 3.9, 2.6], "E": [14.6, 9.2, 1.8, -4.1, -9.3], "F": [9.4, 5.6, 0.4, 0.2, 0.8],
    "G": [7.9, 4.1, 0.6, 0.9, 1.5], "H": [22.4, 18.6, 7.1, 6.3, 6.1], "I": [11.2, 6.9, 2.2, 1.4, 1.9],
    "J": [2.1, 1.8, 0.4, 0.9, 0.5], "K": [6.1, 4.8, 3.2, 2.7, 2.0], "L": [8.8, 3.9, -2.6, -3.2, -2.5],
    "M": [7.4, 5.2, 2.0, 1.6, 2.4], "N": [9.1, 6.2, 1.4, 1.1, 1.8], "O": [5.6, 6.1, 4.4, 3.1, 3.0],
    "P": [3.2, 4.0, 3.1, 2.4, 2.2], "Q": [6.4, 7.2, 5.9, 4.8, 4.1], "R": [19.8, 12.4, 5.2, 4.9, 6.0],
    "S": [6.2, 4.4, 1.2, 1.0, 1.2],
}
