"""The real-name check (reduce-house-fixes H21) for the firm and the partner chains' banners: each banner's
distinctive word sits at least three edits from every Australian locality, statistical-area, local-government and
electorate name in ref/au_place_names.txt (derived from the public Australian postcode and locality table) and from
the grocery banners, retailers, market-data firms and brands listed below, and neither contains nor sits inside one."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
GENERIC = {"north", "south", "east", "west", "upper", "lower", "mount", "mt", "port", "point", "creek", "river",
           "bay", "beach", "hill", "hills", "heights", "park", "vale", "valley", "plains", "plain", "flat",
           "flats", "junction", "lake", "lakes", "springs", "island", "head", "heads", "bridge", "gully", "the",
           "of", "st", "saint", "new", "old", "central", "city", "council", "shire", "regional", "region",
           "and", "-", "outer", "inner", "greater", "rural", "surrounds", "district", "town", "village",
           "fresh", "supermarkets", "foods", "discount", "warehouse", "local", "grocers", "stop", "online", "direct",
           "retail", "data", "fulfilment"}
BRANDS = """coles woolworths aldi iga foodworks supa spar drakes romeos foodland costco seven eleven nightowl ampol
harris farm spudshed ritchies supabarn friendly grocer metro express milkrun amazon tesco sainsbury asda morrisons
waitrose lidl kroger safeway walmart target kmart bunnings wesfarmers metcash bigw nielsen circana quantium
dunnhumby kantar ibisworld morgan nestle arnotts kelloggs sanitarium bega devondale pauls jalna chobani danone
heinz cadbury mars smiths doritos pepsi coca schweppes bundaberg nescafe moccona lavazza vittoria bushells lipton
twinings ingham steggles lilydale sunrice barilla maggi continental streets peters bulla connoisseur mission
pringles kettle thins cheezels twisties shapes""".split()


def lev(a, b, cap=3):
    if abs(len(a) - len(b)) >= cap:
        return cap
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        if min(cur) >= cap:
            return cap
        prev = cur
    return min(prev[-1], cap)


def remainder(name):
    s = re.sub(r"[^a-z ]", " ", name.lower().replace("'", ""))
    return " ".join(w for w in s.split() if w not in GENERIC)


def reference():
    with open(os.path.join(HERE, "ref", "au_place_names.txt")) as f:
        names = [remainder(x) for x in f.read().splitlines() if x.strip()]
    return sorted(set(n for n in names if n)) + BRANDS


def clashes(name, ref):
    r = remainder(name)
    if not r:
        return []
    out = []
    for x in ref:
        if len(x) >= 4 and (x in r or (len(r) >= 4 and r in x)):
            out.append(x)
        elif abs(len(x) - len(r)) < 3 and lev(r, x) < 3:
            out.append(x)
    return out
