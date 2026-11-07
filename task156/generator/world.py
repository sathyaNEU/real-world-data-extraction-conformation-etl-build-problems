"""task156 architecture 3: the world. A Victorian union branch covering council workers (the Local Services Union,
Victoria Branch), the councils it bargains with, their worksites, the branch's elected worksite delegates by term,
its online votes, the protected action ballot rounds the ballot agent declared, and the 2027 bargaining round.

Everything is constructed for this build; no real dataset, council, union or ballot agent is used. Council names are
invented and checked against Victoria's 79 local government areas."""
import datetime as dt

SEED = 156
UNION = "Local Services Union, Victoria Branch"
UNION_SHORT = "LSU Victoria"
AGENT = "Tallyhouse Ballot Services Pty Ltd"
BUREAU = "Western Shires Payroll Services"
PEOPLE = {"research": "Samantha Taylor", "secretary": "Dennis Kim", "organising": "Eric Goodwin"}

# The forecast is struck on this extract of the membership register; the ballots open on BALLOT_OPEN.
EXTRACT = dt.date(2026, 11, 2)
BALLOT_OPEN = dt.date(2027, 3, 1)
BALLOT_CLOSE = dt.date(2027, 3, 15)

# Delegate terms: elected each even July for two years.
TERMS = [2018, 2020, 2022, 2024, 2026]


def term_of(d):
    """The delegate term in force on date d (terms start 1 July of an even year)."""
    y = d.year if d.month >= 7 else d.year - 1
    return y - (y % 2)


# Online votes: (id, title, open local, close local, utc offset hours during the window)
VOTES = [
    ("V2203", "2022 log of claims endorsement", dt.datetime(2022, 3, 16, 9, 0), dt.datetime(2022, 3, 25, 17, 0), 11),
    ("V2308", "2023 model agreement consultation", dt.datetime(2023, 8, 8, 9, 0), dt.datetime(2023, 8, 18, 17, 0), 10),
    ("V2409", "2024 rules amendment vote", dt.datetime(2024, 9, 10, 9, 0), dt.datetime(2024, 9, 20, 17, 0), 10),
    ("V2510", "2026-27 bargaining claims endorsement", dt.datetime(2025, 10, 14, 9, 0),
     dt.datetime(2025, 10, 24, 17, 0), 11),
]
# Logit level of each online vote (the vote's own salience).
VOTE_ALPHA = {"V2203": -1.10, "V2308": -1.00, "V2409": -1.15, "V2510": -0.95}
# Logit level of a protected action ballot (postal and online, run by the agent); the same in every round.
PAB_ALPHA = 0.00
GAMMA = 1.25          # logit lift of an active delegate at the member's worksite
U_SD = 0.90           # sd of each member's own propensity

# Councils: code, name, candidate in 2027, members on the extract (target), sites, delegate coverage of members by
# term (2020, 2022, 2024, 2026), the 2027 turnout a ballot would show on the 2024-26 delegates (target), past ballots.
# Coverage in 2018 equals 2020.
COUNCILS = [
    # code, name, cand, n, sites, cov20, cov22, cov24, cov26, base27, hist
    ("ARD", "Ardeen Shire Council", True, 420, 12, .70, .71, .70, .72, .63, "24"),
    ("BEL", "Bellcourt City Council", True, 1480, 28, .76, .78, .78, .23, .57, "21 24"),
    ("BRK", "Brackley Ranges Shire Council", True, 260, 9, .55, .54, .55, .52, .41, ""),
    ("COP", "Copeland Downs Shire Council", True, 610, 14, .31, .30, .30, .80, .445, "24"),
    ("COR", "Corrigan Valley Shire Council", True, 890, 18, .80, .82, .82, .44, .70, "21 24"),
    ("DAR", "Darnley Plains Shire Council", True, 330, 10, .80, .81, .80, .82, .38, "21"),
    ("ELM", "Elmhurst Bay City Council", True, 1210, 24, .71, .72, .72, .24, .57, "24"),
    ("FAI", "Fairholme Shire Council", True, 180, 7, .36, .35, .35, .38, .66, ""),
    ("GLE", "Glenvale Hills Shire Council", True, 450, 13, .26, .25, .25, .60, .33, "21"),
    ("HAL", "Halston City Council", True, 1620, 30, .67, .68, .68, .70, .59, "21 24"),
    ("JER", "Jerrick Rural City Council", True, 520, 13, .84, .85, .85, .36, .58, "21"),
    ("KEL", "Kelvale Shire Council", True, 210, 8, .45, .46, .45, .45, .44, ""),
    ("LIN", "Lindale City Council", True, 1340, 26, .74, .75, .75, .42, .67, "24"),
    ("MAR", "Marlow Coast Shire Council", True, 690, 15, .79, .80, .82, .30, .58, "24"),
    ("NOR", "Northvale City Council", True, 950, 20, .60, .61, .60, .63, .72, "21 24"),
    ("OAK", "Oakmere Shire Council", True, 390, 11, .61, .62, .62, .60, .33, "21"),
    ("PEL", "Pellham City Council", True, 1050, 22, .29, .28, .28, .76, .45, "21 24"),
    ("QUA", "Quarrington Shire Council", True, 300, 9, .21, .20, .20, .44, .36, ""),
    ("ROS", "Rosedene City Council", True, 860, 18, .75, .76, .76, .22, .585, "24"),
    ("STA", "Stanwick Shire Council", True, 470, 12, .50, .50, .50, .48, .61, "24"),
    ("TAL", "Tallis Creek Shire Council", True, 580, 14, .81, .82, .82, .32, .57, "21 24"),
    ("UND", "Underhill Rural City Council", True, 240, 8, .52, .53, .53, .70, .38, "21"),
    ("VAL", "Valmont City Council", True, 1180, 24, .69, .70, .70, .36, .66, "24"),
    ("WES", "Westhaven Shire Council", True, 640, 15, .41, .40, .40, .42, .68, ""),
    # councils outside the 2027 round (agreements run to 2028 or later)
    ("ASH", "Ashby Shire Council", False, 380, 11, .58, .60, .59, .60, .55, "21"),
    ("BUR", "Burnleigh City Council", False, 1100, 22, .66, .65, .67, .66, .58, "21 24"),
    ("CAR", "Carrow Shire Council", False, 290, 9, .40, .42, .41, .43, .50, "21"),
    ("DEN", "Denholm City Council", False, 820, 18, .72, .70, .71, .70, .62, "24"),
    ("EAS", "Eastbourne Rural City Council", False, 350, 10, .50, .52, .50, .51, .47, "24"),
    ("GRE", "Greystone Shire Council", False, 560, 14, .62, .61, .62, .60, .53, "24"),
]
CODES = [c[0] for c in COUNCILS]
NAME = {c[0]: c[1] for c in COUNCILS}
CANDIDATES = [c[0] for c in COUNCILS if c[2]]
BUREAU_CLIENTS = ["BRK", "KEL", "QUA"]          # pay through the shared payroll bureau

# Protected action ballot rounds: (round, close dates spread over the window)
PAB_ROUNDS = {"21": (dt.date(2021, 3, 22), dt.date(2021, 6, 25)),
              "24": (dt.date(2023, 10, 16), dt.date(2024, 3, 22))}

# Site kinds with relative size
SITE_KINDS = [("Civic Centre", 3.0), ("Operations Depot", 2.6), ("Library", 0.9), ("Aquatic and Leisure Centre", 1.2),
              ("Maternal and Child Health Centre", 0.6), ("Customer Service Centre", 0.8), ("Transfer Station", 0.5),
              ("Works Depot", 1.8), ("Community Care Office", 1.0), ("Parks Depot", 1.1), ("Arts Centre", 0.5),
              ("Early Learning Centre", 0.9), ("Local Laws Office", 0.5), ("Waste Services Depot", 1.0),
              ("Youth Services Hub", 0.4), ("Visitor Information Centre", 0.3)]
TOWNS = ["North", "South", "East", "West", "Central", "Riverside", "Hillside", "Lakeside", "Station Street",
         "Market Street", "Mill Road", "Bridge Street"]
