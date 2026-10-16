"""The Weighhouse's housekeeping people in summer 2026 and as the systems hold them in June 2027. Every name was drawn
with `guard.py names` (locales en_IE, pl_PL, ro_RO, pt_BR, seeds 147, 1471 and 1477)."""
from __future__ import annotations

import datetime as dt
import unicodedata

D = dt.date


def login_of(name):
    first, last = name.split(" ", 1)
    s = (first[0] + last.replace(" ", "").replace("'", "").replace("-", "")).lower()
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


# the hotel's own room attendants who worked the 2026 season: (name, employee no, start, contract, left, login created)
# logins were created on the day the attendant started, or on 14 January 2019 when the app went live
APP_LIVE = D(2019, 1, 14)
CREW_2026 = [
    ("Suzanne Minihan", "WH1187", D(2011, 4, 4), "Permanent full-time", None),
    ("Ruth Kieran", "WH1342", D(2013, 6, 10), "Permanent full-time", None),
    ("Hayley Heffron", "WH1520", D(2015, 3, 2), "Permanent full-time", None),
    ("Olivia Milne", "WH1588", D(2016, 5, 16), "Permanent part-time", None),
    ("Ailis Williams", "WH1604", D(2016, 9, 5), "Permanent full-time", None),
    ("Aimee Scullion", "WH1671", D(2017, 7, 3), "Permanent full-time", None),
    ("Leonie Tobin", "WH1716", D(2018, 2, 19), "Permanent full-time", D(2027, 2, 12)),
    ("Zara Stapleton", "WH1752", D(2018, 6, 25), "Permanent full-time", None),
    ("Rosemary Fennell", "WH1790", D(2018, 11, 12), "Permanent part-time", None),
    ("Eilis Quirke", "WH1833", D(2019, 4, 8), "Permanent full-time", None),
    ("Angela Gogarty", "WH1869", D(2019, 9, 2), "Permanent full-time", None),
    ("Urszula Garbaciak", "WH1405", D(2014, 4, 22), "Permanent full-time", None),
    ("Nicole Taciak", "WH1636", D(2017, 2, 13), "Permanent full-time", None),
    ("Sylwia Kohut", "WH1702", D(2017, 10, 9), "Permanent full-time", None),
    ("Melania Szarzec", "WH1874", D(2019, 9, 16), "Permanent full-time", None),
    ("Ewelina Nawój", "WH1912", D(2021, 6, 28), "Permanent full-time", None),
    ("Marika Dytko", "WH1948", D(2022, 3, 7), "Permanent full-time", None),
    ("Julita Sporysz", "WH1967", D(2022, 5, 30), "Permanent full-time", D(2027, 4, 9)),
    ("Karina Majsterek", "WH2001", D(2023, 2, 20), "Permanent full-time", None),
    ("Marcin Rakus", "WH2015", D(2023, 4, 17), "Permanent full-time", None),
    ("Isabela Pop", "WH1954", D(2022, 4, 11), "Permanent full-time", None),
    ("Ludmila Barbu", "WH1979", D(2022, 9, 12), "Permanent full-time", None),
    ("Andra Ardelean", "WH2033", D(2023, 8, 28), "Permanent full-time", None),
    ("Margareta Marin", "WH2058", D(2024, 1, 15), "Permanent part-time", None),
    ("Rafael Manole", "WH2076", D(2024, 5, 7), "Permanent full-time", None),
    ("Mariah Souza", "WH2091", D(2024, 9, 23), "Permanent full-time", None),
    ("Sorana Preda", "WH2113", D(2026, 3, 9), "Permanent full-time", None),
    ("Adriana Dobre", "WH2120", D(2026, 5, 11), "Permanent full-time", None),
    ("Lara Correia", "WH2131", D(2026, 7, 6), "Permanent full-time", None),
    ("Katelyn Weldon", "WH2134", D(2026, 7, 20), "Permanent full-time", None),
    # summer contracts, 2026 season only
    ("Melissa Caldeira", "WH2124", D(2026, 6, 15), "Fixed-term (summer)", D(2026, 9, 13)),
    ("Vitória Cunha", "WH2125", D(2026, 6, 15), "Fixed-term (summer)", D(2026, 9, 13)),
    ("Elisa Vasconcelos", "WH2126", D(2026, 6, 15), "Fixed-term (summer)", D(2026, 9, 20)),
    ("Florina Diaconu", "WH2127", D(2026, 6, 22), "Fixed-term (summer)", D(2026, 9, 13)),
    ("Kamila Stachewicz", "WH2128", D(2026, 6, 22), "Fixed-term (summer)", D(2026, 9, 6)),
    ("Leanne Bennet", "WH2129", D(2026, 6, 29), "Fixed-term (summer)", D(2026, 9, 13)),
]

SUPERVISORS = [
    ("Sinead Bohan", "WH1398", D(2014, 2, 3)),     # the morning floor supervisor, floors 1 to 4
    ("Miriam Ahern", "WH1555", D(2015, 10, 19)),   # floors 5 to 8
    ("Inga Trojanek", "WH1802", D(2019, 1, 7)),    # weekends and the afternoon
]
EXEC_HK = ("Fergus Roddy", "WH1290", D(2012, 8, 27))

# Brennock's regular temps of summer 2026 (each with an app login from July 2026); three were later taken on by the
# hotel, their logins moved to the in-house group: (name, Brennock id, login created, hired by the hotel, employee no)
BRENNOCK_REGULARS = [
    ("Anita Dreszer", "BHS-20417", D(2026, 7, 20), D(2026, 10, 12), "WH2152"),
    ("Daniela Costa", "BHS-20488", D(2026, 7, 20), D(2027, 1, 11), "WH2166"),
    ("Gina Mocanu", "BHS-20503", D(2026, 7, 21), D(2027, 3, 8), "WH2179"),
    ("Natasza Mszyca", "BHS-20396", D(2026, 7, 20), None, None),
    ("Bianca Cavalcante", "BHS-20512", D(2026, 7, 21), None, None),
    ("Carina Dinu", "BHS-20530", D(2026, 7, 24), None, None),
]
# the 2026 block, 10 to 16 August (eight a day from ten), on the block's own logins (created for the week)
BLOCK_TEMPS = [
    ("Raquel Borges", "BHS-21044"), ("Malwina Roch", "BHS-21051"), ("Janina Czerwionka", "BHS-21058"),
    ("Flavia Ene", "BHS-21063"), ("Alexandrina Albu", "BHS-21070"), ("Heloísa Rocha", "BHS-21077"),
    ("Marina Alves", "BHS-21082"), ("Krystyna Rosada", "BHS-21089"), ("Luana Campos", "BHS-21095"),
    ("Sânziana Dumitrescu", "BHS-21102"),
]
# Brennock's day temps, sent for single busy days with no app login
DAY_TEMPS = [
    ("Ewa Halik", "BHS-19873"), ("Nela Jachimczyk", "BHS-20118"), ("Apolonia Gozdur", "BHS-20202"),
    ("Gaja Strzelczak", "BHS-20255"), ("Salomea Suciu", "BHS-20311"), ("Lelia Tabacu", "BHS-20347"),
    ("Sophia Cardoso", "BHS-20462"), ("Nina Novais", "BHS-20591"), ("Stella Vargas", "BHS-20644"),
    ("Clarice Peixoto", "BHS-20680"), ("Renan Farias", "BHS-20702"),
]
# room attendants taken on in 2027, after the season
CREW_2027 = [
    ("Kara Cruise", "WH2188", D(2027, 4, 19)), ("Abigail Borland", "WH2193", D(2027, 5, 10)),
    ("Gabriela Pacheco", "WH2197", D(2027, 5, 24)), ("Iancu Stoica", "WH2201", D(2027, 6, 7)),
]
# other app users: front office, engineering and duty managers
OTHER_USERS = [
    ("Georgina Eustace", "Front Office", D(2019, 1, 14)), ("Padraic Reardon", "Duty Managers", D(2020, 9, 7)),
    ("Darren Roache", "Engineering", D(2019, 1, 14)), ("Calum Blake", "Engineering", D(2023, 3, 13)),
    ("Amanda Cullinan", "Front Office", D(2021, 5, 4)), ("Shane Geoghegan", "Front Office", D(2022, 10, 3)),
    ("Roberta Taggart", "Front Office", D(2024, 2, 26)),
]
RECEPTION = ["Amanda Cullinan", "Shane Geoghegan", "Roberta Taggart"]
RES_AGENTS = ["Lauren Courcey", "Keith Dunleavey", "Aoibheann McQueen"]


def first(name):
    return name.split(" ", 1)[0]


def _check():
    allp = ([c[0] for c in CREW_2026] + [s[0] for s in SUPERVISORS] + [b[0] for b in BRENNOCK_REGULARS] +
            [b[0] for b in BLOCK_TEMPS] + [d[0] for d in DAY_TEMPS] + [c[0] for c in CREW_2027] + [EXEC_HK[0]])
    firsts = [first(n) for n in allp]
    assert len(set(firsts)) == len(firsts), sorted(f for f in firsts if firsts.count(f) > 1)
    logins = [login_of(n) for n in allp + [o[0] for o in OTHER_USERS]]
    assert len(set(logins)) == len(logins)
    emp = [c[1] for c in CREW_2026] + [s[1] for s in SUPERVISORS] + [b[4] for b in BRENNOCK_REGULARS if b[4]] + \
          [c[1] for c in CREW_2027] + [EXEC_HK[1]]
    assert len(set(emp)) == len(emp)


_check()
