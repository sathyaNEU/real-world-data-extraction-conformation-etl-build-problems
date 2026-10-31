"""The fixed world of task445 architecture 2: NHS Ellesmoor integrated care board, its six places, two coroner areas,
two medical examiner offices, the calendar and the name lists. Nothing here is random; sim.py draws from it."""
import datetime as dt
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SEED = 44502

START = dt.date(2021, 1, 1)          # first date of death on the extract
ME_START = dt.date(2024, 9, 9)       # the statutory medical examiner system in force
LAST_DEATH = dt.date(2026, 10, 7)    # last date of death any source holds
EXTRACT = dt.date(2026, 10, 9)       # registrations and both logs extracted at the end of this day
W0, W1 = dt.date(2026, 6, 1), dt.date(2026, 8, 31)   # the fund's window, by date of death
HEAT26 = (dt.date(2026, 7, 14), dt.date(2026, 7, 24))
HEAT22 = (dt.date(2022, 7, 17), dt.date(2022, 7, 19))
LINE = 0.10                          # a place qualifies at an excess of at least a tenth of its expected deaths
GRANT, STANDARD = 300_000, 60_000

# name, residence code, mid-2025 population, coroner area, medical examiner office, annual death rate, postcode
# districts, share of deaths at home in an ordinary month, the 2026 summer's designed excess over the expected,
# the summer deaths the coroner still holds at the extract beyond the ordinary inquests (heat wave, found late)
PLACES = [
    ("Hollinsgate", "E08000951", 415_200, "North", "North", 0.00905, range(1, 13), 0.25, 0.076, 12),
    ("Ashwold", "E08000952", 205_400, "North", "North", 0.01310, range(13, 20), 0.27, 0.130, 40),
    ("Thornley Vale", "E07000961", 131_300, "North", "North", 0.01080, range(20, 25), 0.26, 0.136, 2),
    ("Brinmoor", "E07000962", 178_100, "South", "South", 0.00985, range(25, 30), 0.26, 0.068, 0),
    ("Calderholt", "E08000953", 238_600, "South", "South", 0.01010, range(30, 36), 0.25, 0.126, 1),
    ("Moorbridge", "E07000963", 162_400, "South", "South", 0.01030, range(36, 41), 0.26, 0.055, 0),
]
NAMES = [p[0] for p in PLACES]
CODE = {p[0]: p[1] for p in PLACES}
POP = {p[0]: p[2] for p in PLACES}
CORONER = {p[0]: p[3] for p in PLACES}
OFFICE = {p[0]: p[4] for p in PLACES}
RATE = {p[0]: p[5] for p in PLACES}
DISTRICTS = {p[0]: list(p[6]) for p in PLACES}
HOME = {p[0]: p[7] for p in PLACES}
EXCESS = {p[0]: p[8] for p in PLACES}
HELD = {p[0]: p[9] for p in PLACES}

# registration districts (deaths are registered where they occur); the register's codes changed with the 2023
# system replacement on 3 April 2023
REG_DISTRICTS = [
    ("Hollinsgate", "HOL", "E30000801", "North"),
    ("Ashwold and Thornley", "ASH", "E30000802", "North"),
    ("Calderholt", "CAL", "E30000803", "South"),
    ("Brinmoor and Moorbridge", "BRM", "E30000804", "South"),
]
SYSTEM_CHANGE = dt.date(2023, 4, 3)
DISTRICT_OF_PLACE = {"Hollinsgate": "Hollinsgate", "Ashwold": "Ashwold and Thornley",
                     "Thornley Vale": "Ashwold and Thornley", "Calderholt": "Calderholt",
                     "Brinmoor": "Brinmoor and Moorbridge", "Moorbridge": "Brinmoor and Moorbridge"}
HOSPITAL = {"North": "Hollinsgate Royal Infirmary", "South": "Calderholt General Hospital"}
HOSPICE = {"North": "St Wilfrid's Hospice", "South": "Moorbridge Hospice"}
HOSPITAL_PLACE = {"North": "Hollinsgate", "South": "Calderholt"}
HOSPICE_PLACE = {"North": "Ashwold", "South": "Moorbridge"}
OUTSIDE_HOSPITALS = ["Kexley Infirmary", "Warrenby General Hospital", "Northfold University Hospital"]

FORENAMES_F = ["Margaret", "Joan", "Dorothy", "Patricia", "Jean", "Barbara", "Mary", "Betty", "Doreen", "Brenda",
               "Sheila", "Irene", "Eileen", "Joyce", "Pauline", "Ann", "Christine", "Susan", "Elizabeth", "Kathleen",
               "Maureen", "Valerie", "Audrey", "Marjorie", "Edna", "Vera", "Iris", "Gladys", "Winifred", "Hilda",
               "Shirley", "Janet", "Linda", "Carol", "Sandra", "Marion", "Brenda", "June", "Rita", "Evelyn",
               "Frances", "Lesley", "Gwendoline", "Beryl", "Muriel", "Olive", "Phyllis", "Ruth", "Sylvia", "Norma"]
FORENAMES_M = ["John", "David", "William", "Robert", "James", "Peter", "Michael", "Brian", "Kenneth", "Alan",
               "Ronald", "George", "Thomas", "Derek", "Keith", "Raymond", "Anthony", "Dennis", "Roy", "Colin",
               "Geoffrey", "Frank", "Eric", "Barry", "Malcolm", "Stephen", "Terence", "Philip", "Leslie", "Gordon",
               "Harold", "Arthur", "Albert", "Norman", "Donald", "Stanley", "Edward", "Charles", "Walter", "Bernard",
               "Trevor", "Clifford", "Gerald", "Douglas", "Frederick", "Leonard", "Ernest", "Harry", "Jack", "Joseph"]
MIDDLE = ["Ann", "Mary", "Elizabeth", "May", "Rose", "Louise", "Jane", "Margaret", "Edith", "Grace",
          "John", "James", "William", "Edward", "Henry", "George", "Thomas", "Arthur", "Charles", "Frederick"]
SURNAMES = ["Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson", "Davies", "Robinson", "Wright",
            "Thompson", "Evans", "Walker", "White", "Roberts", "Green", "Hall", "Wood", "Clarke", "Hughes",
            "Edwards", "Lewis", "Harris", "Turner", "Martin", "Cooper", "Hill", "Ward", "Morris", "Moore",
            "Clark", "Lee", "King", "Baker", "Harrison", "Morgan", "Allen", "James", "Scott", "Phillips",
            "Watson", "Davis", "Parker", "Price", "Bennett", "Young", "Griffiths", "Mitchell", "Kelly", "Cook",
            "Carter", "Richardson", "Bailey", "Collins", "Bell", "Shaw", "Murphy", "Miller", "Cox", "Richards",
            "Khanom", "Marshall", "Anderson", "Simpson", "Ellis", "Adams", "Singh", "Begum", "Wilkinson", "Foster",
            "Chapman", "Powell", "Webb", "Rogers", "Gray", "Mason", "Ali", "Hunt", "Hussain", "Campbell",
            "Matthews", "Owen", "Palmer", "Holmes", "Mills", "Barnes", "Knight", "Lloyd", "Butler", "Russell",
            "Barker", "Fisher", "Stevens", "Jenkins", "Murray", "Dixon", "Harvey", "Graham", "Pearson", "Ahmed",
            "Fletcher", "Walsh", "Kaur", "Gibson", "Howard", "Andrews", "Stewart", "Elliott", "Reynolds", "Saunders",
            "Payne", "Fox", "Ford", "Pearce", "Day", "Brooks", "West", "Lawrence", "Cole", "Atkinson",
            "Bradley", "Spencer", "Gill", "Dawson", "Ball", "Burton", "O'Brien", "Watts", "Rose", "Booth",
            "Perry", "Ryan", "Grant", "Wells", "Armstrong", "Francis", "Rees", "Hayes", "Hart", "Hudson",
            "Newman", "Barrett", "Kennedy", "Robertson", "Lord", "Holt", "Hargreaves", "Ashworth", "Greenwood",
            "Sutcliffe", "Haigh", "Crowther", "Pickles", "Firth", "Ackroyd", "Holroyd", "Brearley", "Whiteley"]
# forename spellings a medical examiner's first entry carries and the registrar's entry corrects
VARIANT = {"Stephen": "Steven", "Ann": "Anne", "Geoffrey": "Jeffrey", "Philip": "Phillip", "Alan": "Allan",
           "Brian": "Bryan", "Leslie": "Lesley", "Terence": "Terrence", "Marjorie": "Margery", "Sheila": "Shiela",
           "Doreen": "Dorreen", "Frances": "Francis", "Gwendoline": "Gwendolyn", "Clifford": "Cliford",
           "Kathleen": "Kathlene", "Muriel": "Murial", "Winifred": "Winnifred", "Beryl": "Berul"}
OCCUPATIONS = ["Retired", "Retired teacher", "Retired nurse", "Retired engineer", "Retired clerk",
               "Housewife", "Retired textile worker", "Retired driver", "Retired machinist", "Retired shop assistant",
               "Retired electrician", "Retired care assistant", "Retired joiner", "Retired secretary", "Unemployed",
               "Bus driver", "Warehouse operative", "Self-employed builder", "Office manager", "Student"]
MARITAL = ["Married", "Widowed", "Single", "Divorced", "Civil partner"]

PERSONAS = ["Caroline Porter", "Jason Leach", "Graeme Gould", "Jayne Jackson"]


def quarter_fy(d):
    """2025-26 quarter of a date (1 to 4), or 0 outside the year."""
    if dt.date(2025, 4, 1) <= d <= dt.date(2025, 6, 30):
        return 1
    if dt.date(2025, 7, 1) <= d <= dt.date(2025, 9, 30):
        return 2
    if dt.date(2025, 10, 1) <= d <= dt.date(2025, 12, 31):
        return 3
    if dt.date(2026, 1, 1) <= d <= dt.date(2026, 3, 31):
        return 4
    return 0


def summer(y):
    return dt.date(y, 6, 1), dt.date(y, 8, 31)
