"""The grantee roster for task123: who the organisations are, their balance dates, grants,
filing habits and the shape of their income. Designed roles are listed explicitly; everyone
else is drawn from the seeded generator. Nothing here is written to the pack directly.
"""
import datetime as dt
from dataclasses import dataclass, field

import numpy as np

from common import SEED, qidx, NQ

PLACES = [
    "Hornby", "Sydenham", "Papanui", "Linwood", "Aranui", "Shirley", "Riccarton", "Halswell",
    "Woolston", "Sumner", "Lyttelton", "New Brighton", "Burwood", "Bryndwr", "Spreydon",
    "Addington", "Wigram", "Belfast", "Rangiora", "Kaiapoi", "Woodend", "Pegasus", "Oxford",
    "Cust", "Amberley", "Waikari", "Hanmer Springs", "Cheviot", "Rolleston", "Lincoln",
    "Prebbleton", "Leeston", "Darfield", "Hororata", "Southbridge", "Akaroa", "Little River",
    "Diamond Harbour", "Ashburton", "Tinwald", "Methven", "Rakaia", "Mayfield", "Geraldine",
    "Temuka", "Pleasant Point", "Fairlie", "Twizel", "Waimate", "Timaru", "Kaikoura", "Culverden",
    "Mount Somers", "Hinds", "Dunsandel", "Springston", "West Melton", "Tai Tapu", "Governors Bay",
    "Heathcote", "Opawa", "St Albans", "Edgeware", "Mairehau", "Parklands", "Avonhead", "Hoon Hay",
    "Bromley", "Phillipstown", "Waltham", "Beckenham", "Cashmere", "Ilam", "Fendalton",
]

KINDS = [
    "Community Rooms Trust", "Household Budgeting Trust", "Youth Collective", "Family Support Trust",
    "Surplus Kai Network", "Older Persons Club", "Arts Trust", "Adult Literacy Project",
    "Learning Centre Trust", "Community Gardens Society", "Play Resource Library Society",
    "Hospital Transport Trust", "Neighbourhood Hub Trust", "Whanau Support Services", "Men's Workshop Collective",
    "Parenting Network", "Newcomers Network", "Disability Recreation Society",
    "Community Transport Trust", "Carer Respite Network", "Te Reo Learning Trust", "Village Hall Society",
    "Sports Education Trust", "Mental Wellbeing Collective", "Tenancy Advocacy Service",
    "Kai Share Cooperative", "Volunteer Exchange Trust", "Day Programme Trust", "Heritage Society",
    "Environmental Restoration Trust", "Music School Trust", "After School Care Society",
]

SECTORS = ["Social services", "Health and disability", "Education and learning", "Arts and culture",
           "Environment", "Community development", "Recreation and sport"]
DISTRICTS = {"Christchurch": 0.55, "Waimakariri": 0.13, "Selwyn": 0.12, "Ashburton": 0.07,
             "Timaru": 0.06, "Hurunui": 0.03, "Banks Peninsula": 0.02, "Kaikoura": 0.02}
PLACE_DISTRICT = {
    **{p: "Christchurch" for p in ["Hornby", "Sydenham", "Papanui", "Linwood", "Aranui", "Shirley",
                                    "Riccarton", "Halswell", "Woolston", "Sumner", "New Brighton",
                                    "Burwood", "Bryndwr", "Spreydon", "Addington", "Wigram", "Belfast",
                                    "Heathcote", "Opawa", "St Albans", "Edgeware", "Mairehau",
                                    "Parklands", "Avonhead", "Hoon Hay", "Bromley", "Phillipstown",
                                    "Waltham", "Beckenham", "Cashmere", "Ilam", "Fendalton"]},
    **{p: "Banks Peninsula" for p in ["Lyttelton", "Akaroa", "Little River", "Diamond Harbour",
                                       "Governors Bay"]},
    **{p: "Waimakariri" for p in ["Rangiora", "Kaiapoi", "Woodend", "Pegasus", "Oxford", "Cust"]},
    **{p: "Hurunui" for p in ["Amberley", "Waikari", "Hanmer Springs", "Cheviot", "Culverden"]},
    **{p: "Selwyn" for p in ["Rolleston", "Lincoln", "Prebbleton", "Leeston", "Darfield", "Hororata",
                              "Southbridge", "Dunsandel", "Springston", "West Melton", "Tai Tapu"]},
    **{p: "Ashburton" for p in ["Ashburton", "Tinwald", "Methven", "Rakaia", "Mayfield",
                                 "Mount Somers", "Hinds"]},
    **{p: "Timaru" for p in ["Geraldine", "Temuka", "Pleasant Point", "Fairlie", "Twizel", "Waimate",
                              "Timaru"]},
    "Kaikoura": "Kaikoura",
}


@dataclass
class Org:
    key: str
    bal: int                       # balance month: 3, 6 or 12
    income: float                  # annual income at the 2024 level, NZ$
    role: str = "steady"
    first_q: int = 5               # first quarterly return, internal index
    last_q: int = 36               # last quarterly return (grant end quarter)
    dual: bool = False
    pg_first_q: int = None         # first project-grant return
    short_form: bool = False
    growth: float = 0.025
    sigma: float = 0.018
    dips: dict = field(default_factory=dict)       # internal quarter -> multiplier
    copy_from: str = None          # twin: copy totals over a span
    copy_span: tuple = None
    # filing habits
    sept_status: str = "filed"     # filed | deadline | oct | later (31 March balance dates only)
    notes: list = field(default_factory=list)
    # identity (filled later)
    cc: str = ""
    name: str = ""
    sector: str = ""
    district: str = ""
    og_ref: str = ""
    pg_ref: str = ""
    og_start: dt.date = None
    og_end: dt.date = None
    pg_start: dt.date = None
    pg_end: dt.date = None


def Q(y, m):
    return qidx(y, m)


def yr_quarters(y):
    """The four calendar quarters of year y."""
    return [Q(y, 3), Q(y, 6), Q(y, 9), Q(y, 12)]


def dip_year(d, y, mult):
    for q in yr_quarters(y):
        d[q] = mult
    return d


def first_q_for_entry(bal, round_year):
    """First return (FY quarter 1) for an entrant first scored at the March round_year census."""
    y = round_year - 3
    return {3: Q(y, 6), 6: Q(y, 9), 12: Q(y + 1, 3)}[bal]


def designed_roles():
    """The organisations whose paths the ladder depends on, with their designed shapes."""
    R = []

    def add(key, bal, income, role, **kw):
        o = Org(key=key, bal=bal, income=income, role=role, **kw)
        o.sigma = kw.get("sigma", 0.006)
        R.append(o)
        return o

    # September answer names and the marker (31 March, unfiled at the census)
    d = {}
    for q in yr_quarters(2025):
        d[q] = 0.78
    d[Q(2026, 3)] = 1.10
    d[Q(2026, 6)] = 1.10
    add("M", 3, 3_250_000, "marker", growth=0.02, dips=d, sept_status="later")

    d = dip_year({}, 2023, 0.855)
    dip_year(d, 2025, 0.765)
    d[Q(2026, 3)] = 1.06
    d[Q(2026, 6)] = 1.06
    add("A2", 3, 1_750_000, "answer", growth=0.02, dips=d, sept_status="oct")

    d = dip_year({}, 2022, 0.85)
    dip_year(d, 2025, 0.775)
    d[Q(2026, 3)] = 1.05
    d[Q(2026, 6)] = 1.05
    add("A3", 3, 1_180_000, "answer", growth=0.02, dips=d, sept_status="later")

    d = dip_year({}, 2024, 0.86)
    dip_year(d, 2025, 0.69)
    d[Q(2026, 3)] = 0.875
    d[Q(2026, 6)] = 0.875
    add("A4", 3, 1_330_000, "answer", growth=0.015, dips=d, sept_status="oct")

    d = dip_year({}, 2024, 0.865)
    d[Q(2025, 3)] = 0.80
    d[Q(2025, 6)] = 0.76
    d[Q(2025, 9)] = 0.70
    d[Q(2025, 12)] = 0.66
    d[Q(2026, 3)] = 0.60
    d[Q(2026, 6)] = 0.58
    add("C1", 3, 1_800_000, "common", growth=0.01, dips=d, sept_status="later")

    # decoys: steady to the end of 2025, hit by the March 2026 government cut
    for key, inc, d1, d2 in [("Y1", 920_000, 0.30, 0.40), ("Y2", 850_000, 0.31, 0.45),
                             ("Y3", 660_000, 0.32, 0.42)]:
        d = {Q(2026, 3): 1 - d1, Q(2026, 6): 1 - d2}
        add(key, 3, inc, "decoy", growth=0.02, dips=d, sept_status="later")
    d = dip_year({}, 2025, 0.918)
    d[Q(2026, 3)] = 0.70
    d[Q(2026, 6)] = 0.62
    add("Y4", 3, 760_000, "decoy_soft", growth=0.0, dips=d, sept_status="later")

    # filed 31 March grantees in steady decline from the second half of 2024
    for key, inc, rate, dual in [("F1", 3_200_000, 0.041, False), ("F2", 1_150_000, 0.041, False),
                                 ("F3", 1_500_000, 0.041, True), ("F4", 950_000, 0.041, False),
                                 ("F5", 750_000, 0.041, False), ("F6", 500_000, 0.041, False),
                                 ("F7", 350_000, 0.041, False)]:
        d = {}
        lvl = 1.0
        for q in range(Q(2024, 9), Q(2026, 6) + 1):
            lvl *= (1 - rate)
            d[q] = lvl
        o = add(key, 3, inc, "filed_offer", growth=0.02, dips=d, dual=dual)
        if dual:
            o.pg_first_q = first_q_for_entry(3, 2025)
            # F3 also fell in 2024 (offered in the March 2025 round)
            for q in yr_quarters(2024):
                o.dips[q] = o.dips.get(q, 1.0) * 0.86
            for q in range(Q(2025, 3), Q(2026, 6) + 1):
                o.dips[q] = o.dips[q] * 0.86

    # 30 June answer names
    d = dip_year({}, 2023, 0.855)
    d[Q(2025, 6)] = 0.55
    d[Q(2025, 9)] = 0.88
    d[Q(2025, 12)] = 0.88
    d[Q(2026, 3)] = 0.90
    d[Q(2026, 6)] = 1.05
    add("A5", 6, 1_400_000, "answer", growth=0.02, dips=d)

    d = dip_year({}, 2022, 0.855)
    d[Q(2025, 6)] = 0.60
    d[Q(2025, 9)] = 0.90
    d[Q(2025, 12)] = 0.90
    d[Q(2026, 3)] = 0.95
    d[Q(2026, 6)] = 1.04
    add("A6", 6, 610_000, "answer", growth=0.02, dips=d)

    # filed grantee whose June 2026 return was restated after the census
    d = {Q(2025, 9): 0.92, Q(2025, 12): 0.88, Q(2026, 3): 0.85, Q(2026, 6): 0.85}
    add("G_R2", 3, 1_800_000, "late_restated", growth=0.0, dips=d)

    # dual grantee whose project-grant return lags one amendment behind
    o = add("L_dual", 3, 540_000, "lag_dual", growth=-0.04, dual=True)
    o.pg_first_q = first_q_for_entry(3, 2023)

    # the new 30 June grantee, first return for the quarter ending September 2024
    add("N", 6, 520_000, "new_june", growth=0.03, first_q=Q(2024, 9), sigma=0.01)

    # 31 December grantees and the 30 June late and census-day filers (all steady)
    add("D1", 12, 560_000, "dec_may", growth=0.004, sigma=0.002)
    add("D2", 12, 430_000, "dec_mixed", growth=0.003, sigma=0.002)
    add("D3", 12, 690_000, "dec_feb", growth=0.02, sigma=0.008)
    add("J1", 6, 380_000, "june_late23", growth=0.004, sigma=0.002)
    add("J2", 6, 450_000, "june_late24", growth=0.003, sigma=0.002)
    add("J3", 6, 520_000, "june_cday23", growth=0.025, sigma=0.008)
    add("J4", 6, 610_000, "june_cday26", growth=0.025, sigma=0.008)

    # the twin pair (March 2025 round); TA copies TB's totals over the round's eight quarters
    d = dip_year({}, 2024, 0.884)
    add("TB", 3, 900_000, "twin_b", growth=0.02, dips=d)
    o = add("TA", 3, 900_000, "twin_a", growth=0.025, dips=dict(d))
    o.copy_from = "TB"
    o.copy_span = (Q(2023, 3), Q(2024, 12))

    # dual grantees
    d = dip_year({}, 2022, 0.83)
    o = add("DU1", 3, 950_000, "dual_offer23", growth=0.02, dips=d, dual=True)
    o.pg_first_q = 5
    for key, inc in [("DU2", 1_050_000), ("DU3", 640_000), ("DU4", 780_000), ("DU5", 520_000)]:
        o = add(key, 3, inc, "dual", growth=0.025, dual=True, sigma=0.012)
        o.pg_first_q = 5
    return R


def build_roster():
    rng = np.random.default_rng([SEED, 1])
    orgs = designed_roles()
    by = {o.key: o for o in orgs}

    # steady 31 March grantees unfiled at the September census (4 file 1 to 7 October, 1 later)
    for k, st in enumerate(["oct", "oct", "oct", "oct", "later"]):
        orgs.append(Org(key=f"U{k+1}", bal=3, income=float(rng.lognormal(np.log(420_000), 0.5)),
                        role="unfiled_steady", sept_status=st, growth=float(rng.normal(0.03, 0.01)),
                        sigma=0.01))
    # 14 steady 31 March grantees whose 2025-26 return reached the register on 30 September 2026
    for k in range(14):
        orgs.append(Org(key=f"S{k+1:02d}", bal=3, income=float(rng.lognormal(np.log(450_000), 0.55)),
                        role="deadline_steady", sept_status="deadline",
                        growth=float(rng.normal(0.03, 0.01)), sigma=0.01))

    # entrants first scored at each March round, and at September
    entrants = {2022: 8, 2023: 9, 2024: 8, 2025: 8, 2026: 5}
    for ry, n in entrants.items():
        for k in range(n):
            bal = 6 if k % 4 == 3 else 3
            o = Org(key=f"E{ry}_{k+1}", bal=bal, income=float(rng.lognormal(np.log(380_000), 0.6)),
                    role="entrant", first_q=first_q_for_entry(bal, ry),
                    growth=float(rng.normal(0.035, 0.02)))
            orgs.append(o)
    for k in range(2):
        orgs.append(Org(key=f"ES_{k+1}", bal=3, income=float(rng.lognormal(np.log(360_000), 0.5)),
                        role="entrant_sept", first_q=Q(2024, 6), growth=float(rng.normal(0.03, 0.01)),
                        sigma=0.012))
    # young grantees with too few quarters to be scored at September
    orgs.append(Org(key="YG1", bal=3, income=300_000, role="young", first_q=Q(2025, 6)))
    orgs.append(Org(key="YG2", bal=3, income=410_000, role="young", first_q=Q(2025, 6)))
    orgs.append(Org(key="YG3", bal=6, income=270_000, role="young", first_q=Q(2025, 9)))

    # exits: grants that ended between censuses
    exits = [(2021, 9), (2021, 12), (2022, 6), (2022, 12), (2023, 6), (2023, 12), (2024, 6),
             (2024, 9), (2024, 12), (2025, 6), (2025, 12), (2026, 6)]
    for k, (y, m) in enumerate(exits):
        bal = 6 if k in (3, 8) else 3
        orgs.append(Org(key=f"X{k+1:02d}", bal=bal, income=float(rng.lognormal(np.log(400_000), 0.6)),
                        role="exit", last_q=Q(y, m), growth=float(rng.normal(0.02, 0.02))))

    # the rest of the book: steady grantees with returns from the start of the extract
    n31 = sum(1 for o in orgs if o.bal == 3 and o.role not in ("exit", "young")
              and o.first_q <= Q(2024, 9))
    n30 = sum(1 for o in orgs if o.bal == 6 and o.role not in ("exit", "young")
              and o.first_q <= Q(2024, 9))
    need31 = 126 - n31
    need30 = 18 - n30
    for k in range(need31):
        orgs.append(Org(key=f"B{k+1:03d}", bal=3, income=float(rng.lognormal(np.log(420_000), 0.7)),
                        role="steady", growth=float(np.clip(rng.normal(0.028, 0.022), -0.03, 0.08))))
    for k in range(need30):
        orgs.append(Org(key=f"BJ{k+1:02d}", bal=6, income=float(rng.lognormal(np.log(420_000), 0.6)),
                        role="steady", growth=float(np.clip(rng.normal(0.028, 0.02), -0.02, 0.07))))
    for o in orgs:
        o.income = float(min(max(o.income, 140_000), 4_800_000))
    return orgs
