"""The fixed world: calendar, lines, prices, the Big Deals calendar, the laws, the member stores.

Nothing here is random except the store-level draws, which take the build seed."""
import datetime as dt
import math

import numpy as np

D = dt.date
SEED = 115

# ---------------------------------------------------------------- calendar
FIRST_WEEK = D(2024, 10, 7)            # Monday
N_WEEKS = 104                          # to w/c 28 Sep 2026
WEEKS = [FIRST_WEEK + dt.timedelta(days=7 * k) for k in range(N_WEEKS)]
PRICE_CHANGE = D(2026, 1, 5)           # regular price review
BRIEF_DATE = D(2026, 9, 28)            # March 2027 brief issued
BASE_WEEKS = [w for w in WEEKS if D(2026, 6, 29) <= w <= D(2026, 9, 21)]   # 13 weeks
EVENT_WEEKS = [D(2027, 3, 1), D(2027, 3, 8), D(2027, 3, 15)]
EXTRACT = dt.datetime(2026, 10, 5, 6, 40)
XMAS = {D(2024, 12, 23): 1.03, D(2025, 12, 22): 1.03}


def period(w):
    return 0 if w < PRICE_CHANGE else 1


# ---------------------------------------------------------------- lines
# item, gtin company prefix + item ref, supplier, description, bags, case, express ranged
LINES = [
    ("211401", "539152300401", "Delahunt Tea", "DELAHUNT ORIGINAL 80S", 80, 12, True),
    ("211402", "539152300402", "Delahunt Tea", "DELAHUNT ORIGINAL 160S", 160, 12, True),
    ("211403", "539152300403", "Delahunt Tea", "DELAHUNT ORIGINAL 240S", 240, 6, False),
    ("211404", "539152300411", "Delahunt Tea", "DELAHUNT GOLD BLEND 80S", 80, 12, False),
    ("208115", "539011700080", "Carrow Tea Co", "CARROW TEA 80S", 80, 12, True),
    ("208116", "539011700120", "Carrow Tea Co", "CARROW TEA 120S", 120, 12, False),
    ("208117", "539011700160", "Carrow Tea Co", "CARROW TEA 160S", 160, 12, True),
    ("208118", "539011700240", "Carrow Tea Co", "CARROW TEA 240S", 240, 6, False),
    ("209331", "539184200081", "Carnmore Foods", "CARNMORE BREAKFAST 80S", 80, 12, True),
    ("209332", "539184200161", "Carnmore Foods", "CARNMORE BREAKFAST 160S", 160, 12, True),
    ("214770", "539220600016", "Rathmore Tea Merchants", "RATHMORE RESERVE 160S", 160, 6, True),
    ("214771", "539220600250", "Rathmore Tea Merchants", "RATHMORE RESERVE LOOSE 250G", 0, 6, False),
    ("300812", "539100400812", "Tullan Grocers", "TULLAN IRISH BREAKFAST 80S", 80, 12, True),
    ("300813", "539100400813", "Tullan Grocers", "TULLAN IRISH BREAKFAST 160S", 160, 12, True),
    ("300814", "539100400814", "Tullan Grocers", "TULLAN IRISH BREAKFAST 240S", 240, 6, False),
    ("216050", "506035700020", "Wildmeadow Infusions", "WILDMEADOW PEPPERMINT 20S", 20, 12, True),
    ("216051", "506035700040", "Wildmeadow Infusions", "WILDMEADOW GREEN TEA 40S", 40, 12, True),
    ("216052", "506035700021", "Wildmeadow Infusions", "WILDMEADOW CHAMOMILE 20S", 20, 12, False),
]


def gtin13(body12):
    s = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(body12))
    return body12 + str((10 - s % 10) % 10)


LINE = {l[0]: {"item": l[0], "gtin": gtin13(l[1]), "supplier": l[2], "desc": l[3], "bags": l[4],
               "case": l[5], "express": l[6]} for l in LINES}
OWN = {80: "300812", 160: "300813", 240: "300814"}      # own-label line of each bag count
DEL160 = "211402"
OL160 = OWN[160]

# regular shelf prices by price file (P premium, C core, V value), period 0 / period 1
PRICE = {
    "211401": {"P": (3.69, 3.79), "C": (3.39, 3.49), "V": (3.09, 3.19)},
    "211402": {"P": (6.79, 6.99), "C": (6.29, 6.49), "V": (5.79, 5.99)},
    "211403": {"P": (9.29, 9.49), "C": (8.79, 8.99), "V": (8.29, 8.49)},
    "211404": {"P": (4.49, 4.69), "C": (4.19, 4.39), "V": (3.89, 4.09)},
    "208115": {"P": (3.09, 3.19), "C": (2.79, 2.89), "V": (2.49, 2.59)},
    "208116": {"P": (4.29, 4.39), "C": (3.89, 3.99), "V": (3.59, 3.69)},
    "208117": {"P": (5.39, 5.49), "C": (4.79, 4.89), "V": (4.59, 4.69)},
    "208118": {"P": (7.49, 7.69), "C": (6.99, 7.19), "V": (6.59, 6.79)},
    "209331": {"P": (2.89, 2.99), "C": (2.59, 2.69), "V": (2.39, 2.49)},
    "209332": {"P": (5.19, 5.29), "C": (4.69, 4.79), "V": (4.19, 4.39)},
    "214770": {"P": (7.39, 7.59), "C": (6.69, 6.89), "V": (6.19, 6.39)},
    "214771": {"P": (6.49, 6.79), "C": (6.19, 6.49), "V": (5.99, 6.29)},
    "300812": {"P": (2.29, 2.35), "C": (1.99, 2.05), "V": (1.79, 1.85)},
    "300813": {"P": (4.29, 4.39), "C": (3.69, 3.79), "V": (3.29, 3.39)},
    "300814": {"P": (5.99, 6.15), "C": (5.29, 5.45), "V": (4.79, 4.95)},
    "216050": {"P": (2.79, 2.89), "C": (2.59, 2.69), "V": (2.49, 2.59)},
    "216051": {"P": (3.49, 3.59), "C": (3.29, 3.39), "V": (3.09, 3.19)},
    "216052": {"P": (2.79, 2.89), "C": (2.59, 2.69), "V": (2.49, 2.59)},
}
OWN_RRP = {"300812": (1.99, 2.05), "300813": (3.69, 3.79), "300814": (5.29, 5.45)}   # = Core file


def price(item, pfile, w):
    return PRICE[item][pfile][period(w)]


# ---------------------------------------------------------------- deals
def deal_price(reg, kind, val):
    x = reg * (1 - val) if kind == "pct" else reg - val
    return math.floor(round(x * 100, 6)) / 100


def depth(reg, kind, val):
    return val if kind == "pct" else val / reg


# Big Deals cycles run three weeks on a grid that lands on 1 March 2027.
def cycle_start(k):
    return D(2027, 3, 1) - dt.timedelta(days=21 * k)


# (cycle code, start, item, kind, value, label)
EVENTS = [
    ("BD24-16", D(2024, 11, 11), "211404", "pct", 0.20, "Save 20%"),
    ("BD25-01", D(2025, 1, 13), "208117", "pct", 0.25, "Save 25%"),
    ("BD25-02", D(2025, 2, 3), "216051", "pct", 0.50, "Half price"),
    ("BD25-03", D(2025, 2, 24), "211402", "pct", 0.20, "Save 20%"),
    ("BD25-05", D(2025, 4, 7), "214770", "pct", 1 / 3, "Save a third"),
    ("BD25-07", D(2025, 5, 19), "208117", "pct", 1 / 3, "Save a third"),
    ("BD25-09", D(2025, 6, 30), "211402", "pct", 0.25, "Save 25%"),
    ("BD25-10", D(2025, 7, 21), "216051", "pct", 0.40, "Save 40%"),
    ("BD25-11", D(2025, 8, 11), "214770", "pct", 0.40, "Save 40%"),
    ("BD25-13", D(2025, 9, 22), "209332", "abs", 1.50, "€1.50 off"),
    ("BD25-14", D(2025, 10, 13), "208116", "pct", 0.50, "Half price"),
    ("BD25-15", D(2025, 11, 3), "211401", "pct", 0.25, "Save 25%"),
    ("BD25-16", D(2025, 11, 24), "208115", "pct", 1 / 3, "Save a third"),
    ("BD26-02", D(2026, 1, 26), "209332", "pct", 1 / 3, "Save a third"),
    ("BD26-03", D(2026, 2, 16), "216050", "pct", 1 / 3, "Save a third"),
    ("BD26-04", D(2026, 3, 9), "211402", "pct", 0.20, "Save 20%"),
    ("BD26-06", D(2026, 4, 20), "214770", "pct", 0.40, "Save 40%"),
    ("BD26-08", D(2026, 6, 1), "208117", "pct", 0.50, "Half price"),
    ("BD26-10", D(2026, 7, 13), "216052", "pct", 0.50, "Half price"),
    ("BD26-11", D(2026, 8, 3), "216050", "pct", 0.40, "Save 40%"),
    ("BD26-13", D(2026, 9, 14), "211402", "pct", 0.25, "Save 25%"),
]
for e in EVENTS:
    assert (D(2027, 3, 1) - e[1]).days % 21 == 0, e
MENU = [("third", "pct", 1 / 3, "Save a third"), ("forty", "pct", 0.40, "Save 40%"),
        ("half", "pct", 0.50, "Half price"), ("off240", "abs", 2.40, "€2.40 off")]

# the pure deal lift, common to every tea line, piecewise linear in depth
KNOTS = [(0.0, 0.0), (0.20, 0.40), (0.25, 0.56), (1 / 3, 0.720), (0.40, 0.732), (0.50, 0.86)]


def lift(d):
    for (x0, y0), (x1, y1) in zip(KNOTS, KNOTS[1:]):
        if d <= x1 + 1e-12:
            return y0 + (y1 - y0) * (d - x0) / (x1 - x0)
    return KNOTS[-1][1]


# In a store-week where a branded deal price is at or below the store's regular price for the own-label line of
# the same bag count, own-label units fall by SWITCH_LOSS of normal and the deal line gains SWITCH_GAIN of
# own-label normal: the switching shoppers buy two packs at the deal price for every own-label pack they drop.
SWITCH_LOSS = 0.35
SWITCH_GAIN = 0.70

# ---------------------------------------------------------------- stores
REGIONS = ["Dublin & North East", "South", "West & North West", "Midlands & South East"]
REG_SHORT = {"Dublin & North East": "DNE", "South": "S", "West & North West": "WNW", "Midlands & South East": "MSE"}
# routing key, town, county, region (Jan 2026 structure)
PLACES = [
    ("D01", "Parnell Street", "Dublin", "DNE"), ("D02", "Pearse Street", "Dublin", "DNE"),
    ("D03", "Clontarf", "Dublin", "DNE"), ("D04", "Sandymount", "Dublin", "DNE"),
    ("D05", "Raheny", "Dublin", "DNE"), ("D06", "Rathmines", "Dublin", "DNE"),
    ("D6W", "Terenure", "Dublin", "DNE"), ("D07", "Phibsborough", "Dublin", "DNE"),
    ("D08", "Inchicore", "Dublin", "DNE"), ("D09", "Drumcondra", "Dublin", "DNE"),
    ("D11", "Finglas", "Dublin", "DNE"), ("D12", "Crumlin", "Dublin", "DNE"),
    ("D13", "Baldoyle", "Dublin", "DNE"), ("D14", "Dundrum", "Dublin", "DNE"),
    ("D15", "Blanchardstown", "Dublin", "DNE"), ("D15", "Castleknock", "Dublin", "DNE"),
    ("D16", "Ballinteer", "Dublin", "DNE"), ("D18", "Cabinteely", "Dublin", "DNE"),
    ("D20", "Palmerstown", "Dublin", "DNE"), ("D22", "Clondalkin", "Dublin", "DNE"),
    ("D24", "Tallaght", "Dublin", "DNE"), ("D24", "Firhouse", "Dublin", "DNE"),
    ("K67", "Swords", "Dublin", "DNE"), ("K36", "Malahide", "Dublin", "DNE"),
    ("K32", "Balbriggan", "Dublin", "DNE"), ("K34", "Skerries", "Dublin", "DNE"),
    ("K56", "Rush", "Dublin", "DNE"), ("K45", "Lusk", "Dublin", "DNE"),
    ("K78", "Lucan", "Dublin", "DNE"), ("A94", "Blackrock", "Dublin", "DNE"),
    ("A96", "Glenageary", "Dublin", "DNE"), ("A98", "Bray", "Wicklow", "DNE"),
    ("A63", "Greystones", "Wicklow", "DNE"), ("A67", "Wicklow", "Wicklow", "DNE"),
    ("Y14", "Arklow", "Wicklow", "DNE"), ("C15", "Navan", "Meath", "DNE"),
    ("A82", "Kells", "Meath", "DNE"), ("A84", "Ashbourne", "Meath", "DNE"),
    ("A85", "Dunshaughlin", "Meath", "DNE"), ("A86", "Dunboyne", "Meath", "DNE"),
    ("A83", "Enfield", "Meath", "DNE"), ("A91", "Dundalk", "Louth", "DNE"),
    ("A92", "Drogheda", "Louth", "DNE"), ("A75", "Castleblayney", "Monaghan", "DNE"),
    ("A81", "Carrickmacross", "Monaghan", "DNE"), ("H18", "Monaghan", "Monaghan", "DNE"),
    ("H23", "Clones", "Monaghan", "DNE"), ("H12", "Cavan", "Cavan", "DNE"),
    ("H16", "Cootehill", "Cavan", "DNE"), ("H14", "Belturbet", "Cavan", "DNE"),
    ("T12", "Douglas", "Cork", "S"), ("T12", "Ballinlough", "Cork", "S"),
    ("T23", "Blackpool", "Cork", "S"), ("T45", "Glanmire", "Cork", "S"),
    ("P31", "Ballincollig", "Cork", "S"), ("P43", "Carrigaline", "Cork", "S"),
    ("P24", "Cobh", "Cork", "S"), ("P25", "Midleton", "Cork", "S"),
    ("P36", "Youghal", "Cork", "S"), ("P17", "Kinsale", "Cork", "S"),
    ("P72", "Bandon", "Cork", "S"), ("P85", "Clonakilty", "Cork", "S"),
    ("P81", "Skibbereen", "Cork", "S"), ("P75", "Bantry", "Cork", "S"),
    ("P47", "Dunmanway", "Cork", "S"), ("P12", "Macroom", "Cork", "S"),
    ("P51", "Mallow", "Cork", "S"), ("P61", "Fermoy", "Cork", "S"),
    ("P67", "Mitchelstown", "Cork", "S"), ("P56", "Charleville", "Cork", "S"),
    ("V92", "Tralee", "Kerry", "S"), ("V93", "Killarney", "Kerry", "S"),
    ("V31", "Listowel", "Kerry", "S"), ("V23", "Caherciveen", "Kerry", "S"),
    ("V93", "Kenmare", "Kerry", "S"), ("V92", "Castleisland", "Kerry", "S"),
    ("H91", "Salthill", "Galway", "WNW"), ("H91", "Knocknacarra", "Galway", "WNW"),
    ("H91", "Ballybane", "Galway", "WNW"), ("H65", "Athenry", "Galway", "WNW"),
    ("H62", "Loughrea", "Galway", "WNW"), ("H53", "Ballinasloe", "Galway", "WNW"),
    ("H54", "Tuam", "Galway", "WNW"), ("H71", "Clifden", "Galway", "WNW"),
    ("F23", "Castlebar", "Mayo", "WNW"), ("F28", "Westport", "Mayo", "WNW"),
    ("F26", "Ballina", "Mayo", "WNW"), ("F12", "Claremorris", "Mayo", "WNW"),
    ("F35", "Ballyhaunis", "Mayo", "WNW"), ("F52", "Swinford", "Mayo", "WNW"),
    ("F31", "Ballinrobe", "Mayo", "WNW"), ("F91", "Sligo", "Sligo", "WNW"),
    ("F56", "Ballymote", "Sligo", "WNW"), ("F92", "Letterkenny", "Donegal", "WNW"),
    ("F94", "Donegal Town", "Donegal", "WNW"), ("F93", "Lifford", "Donegal", "WNW"),
    ("F93", "Buncrana", "Donegal", "WNW"), ("F42", "Castlerea", "Roscommon", "WNW"),
    ("F45", "Ballaghaderreen", "Roscommon", "WNW"), ("F42", "Roscommon", "Roscommon", "WNW"),
    ("N41", "Carrick-on-Shannon", "Leitrim", "WNW"), ("V95", "Ennis", "Clare", "WNW"),
    ("V14", "Shannon", "Clare", "WNW"), ("V15", "Kilrush", "Clare", "WNW"),
    ("V95", "Ennistymon", "Clare", "WNW"),
    ("V94", "Castletroy", "Limerick", "MSE"), ("V94", "Dooradoyle", "Limerick", "MSE"),
    ("V94", "Corbally", "Limerick", "MSE"), ("V42", "Newcastle West", "Limerick", "MSE"),
    ("V35", "Kilmallock", "Limerick", "MSE"), ("E91", "Clonmel", "Tipperary", "MSE"),
    ("E25", "Cashel", "Tipperary", "MSE"), ("E21", "Cahir", "Tipperary", "MSE"),
    ("E41", "Thurles", "Tipperary", "MSE"), ("E45", "Nenagh", "Tipperary", "MSE"),
    ("E53", "Roscrea", "Tipperary", "MSE"), ("E34", "Tipperary Town", "Tipperary", "MSE"),
    ("E32", "Carrick-on-Suir", "Tipperary", "MSE"), ("X91", "Waterford City", "Waterford", "MSE"),
    ("X91", "Tramore", "Waterford", "MSE"), ("X35", "Dungarvan", "Waterford", "MSE"),
    ("X42", "Kilmacthomas", "Waterford", "MSE"), ("Y35", "Wexford Town", "Wexford", "MSE"),
    ("Y21", "Enniscorthy", "Wexford", "MSE"), ("Y25", "Gorey", "Wexford", "MSE"),
    ("Y34", "New Ross", "Wexford", "MSE"), ("R95", "Kilkenny", "Kilkenny", "MSE"),
    ("R95", "Callan", "Kilkenny", "MSE"), ("R93", "Carlow", "Carlow", "MSE"),
    ("R21", "Bagenalstown", "Carlow", "MSE"), ("R32", "Portlaoise", "Laois", "MSE"),
    ("R32", "Mountmellick", "Laois", "MSE"), ("R35", "Tullamore", "Offaly", "MSE"),
    ("R42", "Birr", "Offaly", "MSE"), ("R45", "Edenderry", "Offaly", "MSE"),
    ("N37", "Athlone", "Westmeath", "MSE"), ("N91", "Mullingar", "Westmeath", "MSE"),
    ("N39", "Longford", "Longford", "MSE"), ("W91", "Naas", "Kildare", "MSE"),
    ("W12", "Newbridge", "Kildare", "MSE"), ("R51", "Kildare Town", "Kildare", "MSE"),
    ("R14", "Athy", "Kildare", "MSE"), ("W23", "Celbridge", "Kildare", "MSE"),
    ("W23", "Leixlip", "Kildare", "MSE"), ("W23", "Maynooth", "Kildare", "MSE"),
    ("W34", "Monasterevin", "Kildare", "MSE"), ("R56", "Kilcullen", "Kildare", "MSE"),
]
