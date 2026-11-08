"""task184 world: Fosdyke Poultry, a broiler integrator in south Lincolnshire and the Norfolk fens.

Everything here is fixed (names, farms, houses, calendar, the mortality course the simulation draws from).
sim.py draws the records from it; nothing in this module is shipped as data."""
import datetime as dt

SEED = 18411
D = dt.date

ORG = "Fosdyke Poultry Ltd"
ORG_SHORT = "Fosdyke Poultry"
HATCHERY = "Fosdyke Poultry hatchery, Kirton Holme"
PLANT = "Fosdyke Poultry, Riverside plant, Boston"
CONTRACT_HATCHERY = "Broederij Lindewaard B.V."
CATCHER = "Wash Catching Services Ltd"
PEOPLE = {"head_flock_health": "Annette Begum", "area_manager": "Eileen Porter"}

# calendar
FIRST_PLACEMENT = D(2024, 11, 4)
WINDOW = [D(2027, 2, 10) + dt.timedelta(days=i) for i in range(5)]       # Wednesday 10 to Sunday 14 February
AS_OF = D(2027, 2, 15)                                                    # Monday's round
COURSE_FROM, COURSE_TO = D(2025, 1, 1), D(2026, 12, 31)                   # crops cleared in 2025 and 2026
APP_FROM = D(2025, 6, 2)                                                  # first farm on the growers' app
APP_TO = D(2025, 8, 25)                                                   # last farm on the app
CONTRACT_FROM, CONTRACT_TO = D(2026, 12, 1), D(2026, 12, 24)              # hatchery refit: chicks bought in
INTAKE_SWITCH = D(2027, 1, 18)                                            # plant intake software upgrade
CLOSEOUT_FROM, CLOSEOUT_TO = D(2027, 1, 18), D(2027, 1, 31)               # January close-out catch nights
NO_CATCH = {D(2026, 12, 24), D(2026, 12, 25), D(2026, 12, 26), D(2026, 12, 31), D(2027, 1, 1), D(2027, 1, 2),
            D(2027, 1, 3), D(2027, 1, 17), D(2027, 1, 31)}
APP_OUTAGE = [D(2027, 1, 18), D(2027, 1, 19), D(2027, 1, 20)]
INF_TUNE = {}   # per-house infection size, set so every graded figure sits mid-bin (tune.py)
LINE = 150   # FP-AI-03: swab where the infection killed more than this many birds on the farm in the five days

# the ordinary course: birds found dead per 1,000 alive on the n-th morning after placement (unthinned)
_EARLY = {1: 5.2, 2: 4.6, 3: 3.6, 4: 2.7, 5: 2.0, 6: 1.5, 7: 1.15, 8: 0.95, 9: 0.82, 10: 0.73, 11: 0.67,
          12: 0.62, 13: 0.58, 14: 0.55}


def course(a):
    if a in _EARLY:
        return _EARLY[a]
    if a <= 27:
        return 0.53 - 0.004 * (a - 15)
    if a <= 31:
        return 0.48 + 0.045 * (a - 27)
    return 0.66 + 0.086 * (a - 31)


THINNED_FACTOR = 0.66          # remaining birds after a thin, from the first morning after the thin night


def cull_rate(a):              # birds culled per 1,000 alive (legs, runts); no thinning or infection term
    if a <= 7:
        return 0.30
    if a <= 21:
        return 0.08
    return 0.08 + 0.012 * (a - 21)


# farms: (code, name, grower, parish/area, houses as the grower names them)
FARMS = [
    ("FP104", "Gedney Drove End Farm", "R. & S. Leverton", "Gedney Drove End", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP117", "Holbeach St Marks Poultry Unit", "Marsh Lane Farms Ltd", "Holbeach St Marks", ["No.1", "No.2", "No.3"]),
    ("FP123", "Fleet Hargate Farm", "D. Plowright", "Fleet Hargate", ["Shed A", "Shed B"]),
    ("FP131", "Whaplode Drove Broiler Site", "Ashby Poultry Partnership", "Whaplode Drove", ["1", "2", "3", "4", "5"]),
    ("FP138", "Tydd Gote Farm", "J. W. Sharpe & Son", "Tydd Gote", ["Shed 1", "Shed 2", "Shed 3", "Shed 4", "Shed 5", "Shed 6"]),
    ("FP142", "Moulton Seas End Farm", "K. Bettinson", "Moulton Seas End", ["North", "South"]),
    ("FP149", "Quadring Eaudyke Farm", "A. Hessle", "Quadring Eaudyke", ["House 1", "House 2", "House 3", "House 4"]),
    ("FP155", "Surfleet Seas End Poultry Unit", "Glenside Farming Ltd", "Surfleet Seas End", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP160", "Wigtoft Marsh Farm", "P. & L. Crosby", "Wigtoft", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP168", "Swineshead Bridge Farm", "T. Rylatt", "Swineshead Bridge", ["Shed 1"]),
    ("FP171", "Amber Hill Farm", "Northlands Poultry Ltd", "Amber Hill", ["No.1 House", "No.2 House", "No.3 House"]),
    ("FP179", "Langrick Poultry Unit", "S. Wass", "Langrick", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP183", "Frithville Farm", "M. Cammack", "Frithville", ["Shed A", "Shed B", "Shed C"]),
    ("FP186", "Sibsey Northlands Farm", "Sibsey Northlands Farm Ltd", "Sibsey Northlands", ["1", "2"]),
    ("FP194", "Stickford Broiler Site", "H. Coupland", "Stickford", ["Shed 1", "Shed 2", "Shed 3", "Shed 4", "Shed 5"]),
    ("FP201", "Midville Farm", "J. & E. Tunnard", "Midville", ["Shed 1", "Shed 2"]),
    ("FP207", "Friskney Eaudyke Poultry Unit", "Eaudyke Farms Ltd", "Friskney Eaudyke", ["No.1", "No.2", "No.3", "No.4"]),
    ("FP212", "Wrangle Common Farm", "G. Pickwell", "Wrangle Common", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP218", "Leake Commonside Farm", "B. Fountain", "Leake Commonside", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP223", "Benington Sea End Farm", "C. Elvidge", "Benington Sea End", ["North shed", "South shed"]),
    ("FP229", "Butterwick Poultry Unit", "Butterwick Growers Ltd", "Butterwick", ["Shed 1", "Shed 2", "Shed 3", "Shed 4", "Shed 5"]),
    ("FP236", "Fishtoft Drove Farm", "R. Bontoft", "Fishtoft Drove", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP241", "Algarkirk Fen Farm", "W. Mowbray", "Algarkirk", ["Shed 1", "Shed 2"]),
    ("FP247", "Sutterton Dowdyke Farm", "Dowdyke Poultry LLP", "Sutterton Dowdyke", ["House A", "House B", "House C", "House D"]),
    ("FP253", "Donington Eaudyke Farm", "N. Gostelow", "Donington Eaudyke", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP258", "Bicker Gauntlet Farm", "F. Dring", "Bicker", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP264", "Helpringham Fen Broiler Site", "Fen Edge Farming Ltd", "Helpringham Fen", ["1", "2", "3", "4", "5", "6"]),
    ("FP270", "Billinghay Dales Farm", "S. & K. Kirk", "Billinghay Dales", ["Shed 1", "Shed 2"]),
    ("FP276", "Walcott Dales Farm", "D. Cawthorne", "Walcott Dales", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP281", "Tattershall Thorpe Poultry Unit", "Thorpe Poultry Ltd", "Tattershall Thorpe", ["No.1", "No.2", "No.3", "No.4"]),
    ("FP287", "Coningsby Moor Farm", "A. Ostler", "Coningsby Moor", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP293", "Dogdyke Farm", "L. Grummitt", "Dogdyke", ["Shed 1"]),
    ("FP298", "Revesby Bridge Farm", "E. Neave", "Revesby Bridge", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP305", "Holland Fen Farm", "P. Brackenbury", "Holland Fen", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP311", "Sutton Bridge Marsh Farm", "Cross Keys Poultry Ltd", "Sutton Bridge", ["Shed 1", "Shed 2", "Shed 3", "Shed 4", "Shed 5"]),
    ("FP317", "Long Sutton Poultry Unit", "G. & M. Wakefield", "Long Sutton", ["Shed 1", "Shed 2"]),
    ("FP322", "Tydd St Mary Farm", "Hall Farm Partnership", "Tydd St Mary", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP328", "Gosberton Risegate Farm", "I. Skelton", "Gosberton Risegate", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP334", "Kirton Holme Farm", "V. Blades", "Kirton Holme", ["Shed 1", "Shed 2"]),
    ("FP339", "Freiston Shore Farm", "Shore Road Farms Ltd", "Freiston Shore", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
    ("FP345", "Eastville Poultry Unit", "R. Marris", "Eastville", ["Shed 1", "Shed 2", "Shed 3"]),
    ("FP352", "Stixwould Fen Farm", "Stixwould Growers LLP", "Stixwould Fen", ["Shed 1", "Shed 2", "Shed 3", "Shed 4"]),
]

# the window, designed farm by farm: placement date of the crop on site in week 7 and how the crop runs.
# I1 week-old infected, I2 mid-crop infected, I3 thinned late infected, U1 and U2 unthinned late uninfected.
DESIGN = {
    "FP149": dict(role="I1", place=D(2027, 2, 5), thin=None, inf=(D(2027, 2, 9), 0.36, 1.36)),
    "FP328": dict(role="I2", place=D(2027, 1, 22), thin=None, inf=(D(2027, 2, 9), 0.24, 1.36)),
    "FP218": dict(role="I3", place=D(2027, 1, 6), thin=32, inf=(D(2027, 2, 9), 0.30, 1.36)),
    "FP138": dict(role="U1", place=D(2027, 1, 4), thin=None, inf=None),
    "FP264": dict(role="U2", place=D(2027, 1, 7), thin=None, inf=None),
    "FP160": dict(role="T1", place=D(2027, 1, 5), thin=32, inf=None),
    "FP104": dict(role="T2", place=D(2027, 1, 3), thin=33, inf=None),
    "FP352": dict(role="T3", place=D(2027, 1, 4), thin=31, inf=None),
}
