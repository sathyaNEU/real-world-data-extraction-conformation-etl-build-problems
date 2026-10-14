"""The world of task230: the Office of the Registrar General of Aldmere and its 2026 Census of Population and Housing.
The classification (ISCO-08 and the national extension), the occupation mix, the vague write-ins, the regions and
enumeration districts, the clerical coding teams and the follow-up enumerators."""
import numpy as np

import isco08
import params as P
import titles as T

OFFICE = "Office of the Registrar General"
COUNTRY = "Aldmere"
CENSUS = "2026 Census of Population and Housing"

SUB = dict(isco08.sub_major())
GROUPS = [g for g, _ in isco08.sub_major()]
UNIT_TITLE = dict(isco08.units())
TITLES = T.titles()

# sub-major group shares of persons in employment (per cent), Aldmere 2026
SHARE = dict(zip(GROUPS, [1.3, 3.1, 2.4, 2.1, 4.4, 5.0, 5.8, 5.6, 2.6, 2.3, 3.3, 2.9, 6.0, 1.9, 1.4, 4.6, 2.5, 2.9, 1.1,
                          4.1, 6.4, 4.6, 1.7, 2.6, 0.5, 0.05, 4.4, 3.7, 0.6, 2.3, 1.5, 1.7, 1.8, 4.1, 3.1, 1.0, 2.2, 0.8,
                          0.2, 1.0]))

# the national extension (Aldmere Occupational Classification 2026): ISCO-08 unit group plus a fifth digit; a unit group
# without national detail takes 0
NATIONAL = {
    "1420": [("1", "Retail managers"), ("2", "Wholesale managers")],
    "2221": [("1", "Registered general nurses"), ("2", "Registered psychiatric nurses"),
             ("3", "Registered children's nurses"), ("4", "Public health nurses")],
    "2330": [("1", "Secondary teachers, languages and humanities"), ("2", "Secondary teachers, mathematics and sciences"),
             ("3", "Secondary teachers, technical and practical subjects")],
    "2411": [("1", "Chartered and certified accountants"), ("2", "Management accountants"), ("3", "Tax advisers")],
    "2512": [("1", "Software developers"), ("2", "Games developers")],
    "3322": [("1", "Sales representatives, wholesale"), ("2", "Sales representatives, technical goods")],
    "4110": [("1", "General office clerks, public service"), ("2", "General office clerks, other")],
    "4311": [("1", "Bookkeepers"), ("2", "Accounts clerks")],
    "5120": [("1", "Cooks, hotels and restaurants"), ("2", "Cooks, institutions")],
    "5223": [("1", "Shop sales assistants, food"), ("2", "Shop sales assistants, non-food")],
    "5321": [("1", "Care assistants, hospitals"), ("2", "Care assistants, nursing homes")],
    "6121": [("1", "Dairy farmers"), ("2", "Cattle farmers"), ("3", "Sheep farmers")],
    "7231": [("1", "Motor mechanics"), ("2", "Auto electricians")],
    "8322": [("1", "Taxi and hackney drivers"), ("2", "Van drivers"), ("3", "Chauffeurs")],
    "9112": [("1", "Office cleaners"), ("2", "Hotel and hospital cleaners")],
    "9329": [("1", "Food factory operatives"), ("2", "Other manufacturing labourers")],
}


def national_codes(unit):
    if unit in NATIONAL:
        return [unit + d for d, _ in NATIONAL[unit]]
    return [unit + "0"]


# vague write-ins: the default unit group the autocoder suggests and the forms people write, by who writes them
VAGUE_TEXT = {
    "office": (["Office", "office work", "Works in an office", "Office job", "Office staff"],
               ["works in an office", "office job I think", "in an office in town", "office work"]),
    "business": (["Business", "Own business", "Self employed - business", "Business"],
                 ["has his own business", "business", "something in business", "runs a business"]),
    "accounts": (["Accounts", "Accounts dept", "Works in accounts"],
                 ["does the accounts", "accounts", "works in accounts somewhere", "accounts for a company"]),
    "computers": (["Computers", "Computer work", "Works with computers"],
                  ["something with computers", "computers", "computer work"]),
    "IT": (["IT", "I.T.", "IT dept", "Works in IT"],
           ["IT", "works in IT", "in IT I think", "IT company"]),
    "engineer": (["Engineer", "Engineering", "Engineer"],
                 ["engineer", "some kind of engineer", "engineering", "an engineer at the plant"]),
    "labourer": (["Labourer", "General labourer", "Labouring"],
                 ["labourer", "labouring", "building sites", "works on the buildings"]),
    "factory": (["Factory work", "Factory", "Works in factory"],
                ["works in the factory", "factory", "at the factory", "factory worker"]),
    "hospital": (["Hospital", "Hospital work", "Works at the hospital"],
                 ["works at the hospital", "hospital", "something at the hospital", "hospital worker"]),
    "shop": (["Shop", "Shop work", "Works in a shop"],
             ["works in a shop", "shop", "in the shop in the village", "shop work"]),
    "farm": (["Farm", "Farming", "Farm work"],
             ["farming", "on the farm", "farm", "works the farm"]),
    "driver": (["Driver", "Driving", "Drives for a living"],
               ["drives a van", "driver", "driving", "drives for a company"]),
}

REGIONS = [("PA", "Port Aldmere", 0.24), ("AV", "Ardvale", 0.13), ("BM", "Brackenmoor", 0.11), ("KM", "Kilmarran", 0.12),
           ("FH", "Fernholt", 0.10), ("RC", "Rathcolm", 0.11), ("SM", "Strathmoyle", 0.10), ("GW", "Glenwarren", 0.09)]

TEAMS = ["Coding Team 1", "Coding Team 2", "Coding Team 3", "Coding Team 4", "Coding Team 5"]


def unit_mix():
    """per sub-major group: the unit groups people hold and their weights"""
    mix = {}
    for g in GROUPS:
        us = sorted(u for u in TITLES if u[:2] == g)
        w = np.array([TITLES[u][0] for u in us], float)
        mix[g] = (us, w / w.sum())
    return mix


def eds(rng):
    """enumeration districts: code, region, households expected"""
    out = []
    n_tot = P.N_EDS
    for code, name, sh in REGIONS:
        n = int(round(n_tot * sh))
        for i in range(n):
            out.append(("%s%03d" % (code, 101 + i), code))
    return out
