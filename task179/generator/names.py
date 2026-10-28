"""Names in the fiction. People are drawn from Faker's en_US and es_MX weighted name lists (MIT licence) with the
build's own random streams; places (Halverton's streets, the region's towns) are invented here. The documents'
personas are the card's (guard.py names --geo us --seed 179)."""
from __future__ import annotations

import numpy as np
from faker.providers.person.en_US import Provider as US
from faker.providers.person.es_MX import Provider as MX

PERSONAS = {"deputy_director": "Ashlee Evans", "research_lead": "Zachary Wallace"}

TOWNS_DARROW = ["Halverton", "Pell Junction", "Corbin Falls", "Wexley", "Ardmore Station"]
TOWNS_KESWICK = ["Keswick", "Linden Ford", "Marrow Creek", "Tallis", "Branner"]
OTHER_TOWNS = ["Pell Junction", "Corbin Falls", "Wexley", "Keswick", "Linden Ford", "Tallis", "Calder City", "Ostrava Springs"]

HALVERTON_STREETS = [
    "Arbor", "Bellamy", "Birchwood", "Brannock", "Calloway", "Carver", "Cedar Hollow", "Chalmers", "Colfax",
    "Copeland", "Delmont", "Dunmore", "Eastgate", "Elm", "Fairbanks", "Fenwick", "Garland", "Glenhaven", "Grandview",
    "Harmon", "Hawthorne", "Hollis", "Ingram", "Jasper", "Keller", "Kingsley", "Larchmont", "Lattimore", "Linwood",
    "Maple", "Marlow", "Mercer", "Milbrook", "Northfield", "Oakhurst", "Orchard", "Parkline", "Pembury", "Prescott",
    "Quarry", "Radley", "Redfern", "Riverside", "Rosemont", "Saddler", "Sherwood", "Southmoor", "Spruce", "Stanton",
    "Sycamore", "Talbot", "Thornbury", "Tilden", "Union", "Vance", "Walnut", "Waverly", "Westbrook", "Whitcomb",
    "Willow Bend", "Winslow", "Yardley"]
STREET_TYPES = [("Ave", 0.30), ("St", 0.34), ("Dr", 0.10), ("Rd", 0.08), ("Ln", 0.06), ("Ct", 0.05), ("Pl", 0.04),
                ("Blvd", 0.03)]
# Halverton ZIP codes by police district (North, East, Central, South, West)
DISTRICT_ZIPS = {1: ["48711", "48712"], 2: ["48714", "48715"], 3: ["48701", "48703"], 4: ["48720", "48721"],
                 5: ["48724", "48726"]}
DISTRICT_NAMES = {1: "North", 2: "East", 3: "Central", 4: "South", 5: "West"}

NICKNAMES = {"Michael": "Mike", "William": "Bill", "Robert": "Bob", "Richard": "Rick", "James": "Jim",
             "Joseph": "Joe", "Christopher": "Chris", "Anthony": "Tony", "Daniel": "Dan", "Matthew": "Matt",
             "Thomas": "Tom", "Charles": "Charlie", "Nicholas": "Nick", "Jonathan": "Jon", "Timothy": "Tim",
             "Kenneth": "Ken", "Steven": "Steve", "Jeffrey": "Jeff", "Gregory": "Greg", "Benjamin": "Ben"}


def _pool(d):
    names = list(d.keys())
    w = np.array([float(v) for v in d.values()])
    return names, w / w.sum()


def _pool_list(seq):
    names = list(dict.fromkeys(seq))
    return names, np.full(len(names), 1.0 / len(names))


US_M = _pool(US.first_names_male)
US_F = _pool(US.first_names_female)
US_L = _pool(US.last_names)
MX_M = _pool_list(MX.first_names_male)
MX_F = _pool_list(MX.first_names_female)
MX_L = _pool_list(MX.last_names)


def clean(s):
    return s.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o") \
        .replace("ú", "u").replace("ñ", "n").replace("Á", "A").replace("É", "E") \
        .replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Ñ", "N") \
        .replace("ü", "u")


def draw_people(rng, male, hispanic):
    """first, middle, last, suffix for each row; male and hispanic are boolean arrays"""
    male = np.asarray(male, bool)
    hispanic = np.asarray(hispanic, bool)
    n = len(male)
    first = np.empty(n, dtype=object)
    last = np.empty(n, dtype=object)
    middle = np.empty(n, dtype=object)
    for mk in (True, False):
        for hk in (True, False):
            idx = np.where((male == mk) & (hispanic == hk))[0]
            if len(idx) == 0:
                continue
            fp = (MX_M if mk else MX_F) if hk else (US_M if mk else US_F)
            lp = MX_L if hk else US_L
            first[idx] = [clean(fp[0][j]) for j in rng.choice(len(fp[0]), size=len(idx), p=fp[1])]
            last[idx] = [clean(lp[0][j]) for j in rng.choice(len(lp[0]), size=len(idx), p=lp[1])]
            mp = US_M if mk else US_F
            middle[idx] = [clean(mp[0][j]) for j in rng.choice(len(mp[0]), size=len(idx), p=mp[1])]
            second = [clean(lp[0][j]) for j in rng.choice(len(lp[0]), size=len(idx), p=lp[1])]
            u = rng.random(len(idx))
            for k, i in enumerate(idx):
                if hk and u[k] < 0.12:
                    last[i] = last[i] + "-" + second[k]
                elif (not hk) and u[k] < 0.012:
                    last[i] = "O'" + last[i]
    u = rng.random(n)
    letters = np.array(list("ABCDEFGHJKLMNPRSTW"))[rng.integers(0, 18, n)]
    for i in range(n):
        if u[i] < 0.55:
            if middle[i] == first[i]:
                middle[i] = ""
        elif u[i] < 0.80:
            middle[i] = str(letters[i])
        else:
            middle[i] = ""
    w = rng.random(n)
    suffix = np.where(male & (w < 0.035), "JR", np.where(male & (w < 0.042), "III", np.where(male & (w < 0.047), "SR", "")))
    return list(first), list(middle), list(last), [str(x) for x in suffix]


_ST_CDF = np.cumsum([p for _, p in STREET_TYPES])


def street_address(rng):
    u = rng.random(6)
    num = 100 + int(u[0] * 9799)
    st = HALVERTON_STREETS[int(u[1] * len(HALVERTON_STREETS))]
    t = STREET_TYPES[int(np.searchsorted(_ST_CDF, u[2] * _ST_CDF[-1]))][0]
    unit = ""
    if u[3] < 0.28:
        unit = "APT %d" % (1 + int(u[4] * 39)) if u[5] < 0.7 else "UNIT %s" % "ABCDEF"[int(u[4] * 6)]
    return num, st, t, unit
