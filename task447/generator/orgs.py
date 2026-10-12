"""Organisations, practices, physicians, the ownership register and the NPI-to-TIN history."""
import random
from datetime import date, timedelta

from faker import Faker

import world as W

D = date

# ------------------------------------------------------------------ practices
# key: name, system-at-start or None, county, zip(s), specialty plan
PRACTICES = {
    "BMG": ("Brightwater Medical Group", None, ["54220", "54220", "54241", "54216"]),
    "LMG": ("Ledgestone Medical Group", "LDG", ["54301", "54303", "54911", "54115"]),
    "LPCN": ("Ledgestone Primary Care North", "LDG", ["54313", "54302"]),
    "FRPP": ("Fox River Physician Partners", None, ["54911", "54914"]),
    "BYP": ("Bayside Pediatrics", None, ["54311"]),
    "MFP": ("Mishicot Family Practice", "LDG", ["54228", "54241"]),
    "P1": ("Oak Hollow Family Medicine", None, ["54913"]),
    "P2": ("Baird Creek Gastroenterology", None, ["54311"]),
    "P3": ("Northpoint Orthopedics", None, ["54115"]),
    "P4": ("Harborview Internal Medicine", None, ["54302"]),
    "P5": ("Cedar Ridge Cardiology", None, ["54914"]),
    "HLC": ("Harbor Lakes Clinic", None, ["54304"]),
    "WRMG": ("Wolf River Medical Group", "WRH", ["54901", "54935"]),
    "W1": ("Lakeside Family Physicians", None, ["54904"]),
    "W2": ("Fond du Lac Digestive Health", None, ["54935"]),
    "KPN": ("Kinnickinnic Physician Network", "KNK", ["54220", "54241", "53081", "53083"]),
    "RRF": ("Rapids Road Family Medicine", None, ["54220"]),
    "AFH": ("Algoma Family Health", None, ["54201"]),
    "KAC": ("Kewaunee Area Clinic", None, ["54216", "54217"]),
    "MDC": ("Manitowoc Digestive Care", None, ["54220"]),
    "SOA": ("Shoreline Orthopaedic Associates", None, ["54220", "54241"]),
}
BILLING_ZIP = {"KPN": "53081"}   # the network bills from its Sheboygan business office

TAXON = {"FM": "207Q00000X", "IM": "207R00000X", "PED": "208000000X", "GI": "207RG0100X",
         "ORTH": "207X00000X", "CARD": "207RC0000X", "NP": "363L00000X", "PA": "363A00000X"}
TAXON_NAME = {"207Q00000X": "Family Medicine", "207R00000X": "Internal Medicine", "208000000X": "Pediatrics",
              "207RG0100X": "Internal Medicine, Gastroenterology", "207X00000X": "Orthopaedic Surgery",
              "207RC0000X": "Internal Medicine, Cardiovascular Disease", "363L00000X": "Nurse Practitioner",
              "363A00000X": "Physician Assistant"}

# physicians at the start of their history: practice -> list of specialties
STAFF = {
    "BMG": ["FM"] * 8 + ["IM"] * 4 + ["GI"] * 2 + ["ORTH"] * 2 + ["CARD"] * 2,
    "LMG": ["FM"] * 16 + ["IM"] * 10 + ["PED"] * 4 + ["GI"] * 4 + ["ORTH"] * 6 + ["CARD"] * 5 + ["NP"] * 6 + ["PA"] * 3,
    "LPCN": ["FM"] * 6 + ["IM"] * 3,
    "FRPP": ["FM"] * 4 + ["IM"] * 3,
    "BYP": ["PED"] * 3,
    "MFP": ["FM"] * 3 + ["NP"],
    "P1": ["FM"] * 5,
    "P2": ["GI"] * 3,
    "P3": ["ORTH"] * 4,
    "P4": ["IM"] * 5,
    "P5": ["CARD"] * 3,
    "HLC": ["FM"] * 4 + ["IM"] * 2,
    "WRMG": ["FM"] * 12 + ["IM"] * 8 + ["GI"] * 3 + ["ORTH"] * 4 + ["CARD"] * 4,
    "W1": ["FM"] * 4,
    "W2": ["GI"] * 3,
    "KPN": ["FM"] * 9 + ["IM"] * 5 + ["GI"] * 2 + ["ORTH"] * 3 + ["CARD"] * 2 + ["PA"] * 2,
    "RRF": ["FM"] * 4,
    "AFH": ["FM"] * 3,
    "KAC": ["FM"] * 2 + ["IM"],
    "MDC": ["GI"] * 2,
    "SOA": ["ORTH"] * 3,
}

# ------------------------------------------------------------------ the ownership register
# (org key, parent key, relationship, effective_from, effective_to, source)
REGISTER = [
    ("LMG", "LDG", "owned", D(2009, 7, 1), None, "annual registration 2016"),
    ("LPCN", "LDG", "owned", D(2017, 1, 1), D(2020, 5, 31), "annual registration 2017"),
    ("LPCN", "LMG", "merged into (TIN retired)", D(2020, 6, 1), None, "annual registration 2020"),
    ("MFP", "LDG", "affiliated, controlled", D(2019, 3, 1), None, "notice N19-0027"),
    ("BYP", "FRPP", "owned", D(2018, 4, 1), None, "annual registration 2018"),
    ("FRPP", "LDG", "affiliated, controlled", D(2020, 9, 1), None, "notice N20-0041"),
    ("P1", "LMG", "merged into (TIN retired)", D(2021, 10, 1), None, "notice N21-0058"),
    ("P2", "LDG", "affiliated, controlled", D(2022, 4, 1), None, "notice N22-0016"),
    ("P4", "LMG", "merged into (TIN retired)", D(2023, 3, 1), None, "notice N23-0009"),
    ("P5", "LDG", "affiliated, controlled", D(2023, 8, 1), None, "notice N23-0031"),
    ("HLC", "LDG", "clinically integrated network participant", D(2023, 5, 1), None, "annual registration 2023"),
    ("WRMG", "WRH", "owned", D(2011, 1, 1), None, "annual registration 2016"),
    ("W1", "WRMG", "merged into (TIN retired)", D(2022, 6, 1), None, "notice N22-0029"),
    ("W2", "WRH", "affiliated, controlled", D(2023, 2, 1), None, "notice N22-0047"),
    ("KPN", "KNK", "owned", D(2012, 1, 1), None, "annual registration 2016"),
]
EVENT_DATE = {"P1": D(2021, 10, 1), "P2": D(2022, 4, 1), "P3": D(2022, 10, 3), "P4": D(2023, 3, 1),
              "P5": D(2023, 8, 1), "W1": D(2022, 6, 1), "W2": D(2023, 2, 1)}
ACQUIRER = {"P1": "LDG", "P2": "LDG", "P3": "LDG", "P4": "LDG", "P5": "LDG", "W1": "WRH", "W2": "WRH"}
# practices whose physicians move to the parent's TIN at the event; the others keep their TIN
TIN_RETIRED_INTO = {"LPCN": "LMG", "P1": "LMG", "P4": "LMG", "W1": "WRMG"}


def make_people():
    """Physicians and their billing-TIN history. Returns (people, assignments).

    people: npi -> dict(name, first, last, cred, taxonomy, spec, home)
    assignments: list of (npi, practice, start, end) billing-TIN spans
    """
    fk = Faker("en_US")
    Faker.seed(W.SEED * 10 + 1)
    rnd = random.Random(W.SEED + 11)
    banned_last = {"Abbott", "Murillo", "Prince"}
    # surnames other builds already carry (the fingerprint people check); a physician who draws one
    # takes a surname from a separate stream, so every other draw and every date after it stays put
    corpus_last = {"Johnson"}
    fk_alt = Faker("en_US")
    fk_alt.seed_instance(W.SEED * 10 + 7)
    seen = set()
    people, assign = {}, []

    def new_person(practice, spec, idx):
        while True:
            female = rnd.random() < 0.46
            first = fk.first_name_female() if female else fk.first_name_male()
            last = fk.last_name()
            if last in banned_last or (first, last) in seen:
                continue
            break
        while last in corpus_last or last in banned_last or (first, last) in seen:
            last = fk_alt.last_name()
        seen.add((first, last))
        npi = W.npi_from("%s|%s|%d" % (practice, spec, idx))
        cred = {"NP": "NP", "PA": "PA-C"}.get(spec, "MD" if rnd.random() < 0.82 else "DO")
        people[npi] = {"npi": npi, "first": first, "last": last, "cred": cred, "spec": spec,
                       "taxonomy": TAXON[spec], "home": practice}
        return npi

    roster = {}
    for p, specs in STAFF.items():
        roster[p] = [new_person(p, s, i) for i, s in enumerate(specs)]

    start_default = D(2016, 1, 1)
    for p, npis in roster.items():
        for npi in npis:
            if p in TIN_RETIRED_INTO:
                ev = {"LPCN": D(2020, 6, 1)}.get(p, EVENT_DATE.get(p))
                assign.append((npi, p, start_default, ev - timedelta(days=1)))
                assign.append((npi, TIN_RETIRED_INTO[p], ev, None))
            elif p == "P3":
                pass  # handled below, one by one
            else:
                assign.append((npi, p, start_default, None))

    # Northpoint Orthopedics: physicians reassigned to Ledgestone Medical Group one at a time
    p3_moves = [D(2022, 10, 3), D(2022, 10, 17), D(2022, 11, 1), D(2022, 11, 14)]
    for npi, mv in zip(roster["P3"], p3_moves):
        assign.append((npi, "P3", start_default, mv - timedelta(days=1)))
        assign.append((npi, "LMG", mv, None))

    # organic change at Ledgestone Medical Group: hires and departures (dates clear of 1 January)
    hires = {2020: 3, 2021: 4, 2022: 2, 2023: 5, 2024: 3, 2025: 2}
    leaves = {2020: 2, 2021: 3, 2022: 2, 2023: 2, 2024: 4, 2025: 1}
    lmg = list(roster["LMG"])
    hire_specs = ["FM", "IM", "PED", "GI", "ORTH", "CARD", "NP", "PA"]
    k = 0
    for yr in range(2020, 2026):
        for j in range(hires[yr]):
            spec = hire_specs[(k * 3 + j) % len(hire_specs)]
            k += 1
            npi = new_person("LMG-H%d" % yr, spec, j)
            people[npi]["home"] = "LMG"
            st = D(yr, rnd.choice([3, 4, 6, 7, 8, 9]), rnd.choice([3, 8, 15, 22]))
            if yr == 2025:
                st = D(2025, rnd.choice([2, 3, 4, 5, 6]), rnd.choice([3, 8, 15]))
            assign.append((npi, "LMG", st, None))
            lmg.append(npi)
        # departures among long-standing MDs/DOs and APCs
        cands = [n for n in lmg if people[n]["home"] == "LMG" and n in roster["LMG"]]
        rnd.shuffle(cands)
        for npi in cands[:leaves[yr]]:
            for i, a in enumerate(assign):
                if a[0] == npi and a[1] == "LMG" and a[3] is None:
                    en = D(yr, rnd.choice([2, 5, 6, 9, 10, 11]), rnd.choice([10, 14, 20, 28]))
                    assign[i] = (a[0], a[1], a[2], en)
                    roster["LMG"].remove(npi)
                    break
    # one physician who left Ledgestone in 2021 and came back in 2024 (same NPI)
    back = roster["LMG"][5]
    for i, a in enumerate(assign):
        if a[0] == back and a[1] == "LMG" and a[3] is None:
            assign[i] = (a[0], a[1], a[2], D(2021, 6, 30))
            assign.append((back, "HLC", D(2021, 8, 2), D(2024, 4, 30)))
            assign.append((back, "LMG", D(2024, 5, 20), None))
            break
    # a Brightwater gastroenterologist also reads cases one day a week for Kinnickinnic
    gi_split = [n for n in roster["BMG"] if people[n]["spec"] == "GI"][1]
    assign.append((gi_split, "KPN", D(2023, 2, 6), None))
    return people, assign, roster


def tin_of(practice):
    return W.tin_from(practice)


def org_rows():
    """The register's organisation list (one row per billing entity or system)."""
    rows = []
    for key, name in W.SYSTEMS.items():
        rows.append({"org_key": key, "org_name": name, "org_type": "health system", "tin": "",
                     "zip": {"LDG": "54301", "WRH": "54901", "KNK": "53081"}[key]})
    for key, (name, sysk, zips) in PRACTICES.items():
        rows.append({"org_key": key, "org_name": name, "org_type": "physician practice",
                     "tin": tin_of(key), "zip": BILLING_ZIP.get(key, zips[0])})
    return rows
