"""The fixed world of task255: Fallowmere Intergovernmental Risk Pool, a Washington pool of cities, towns and special
districts that shares its members' liability occurrences above each member's deductible and up to the pool's
per-occurrence retention, and is choosing the attachment of its 2027 excess liability cover from the quotes its
broker gathered. Every other module reads its constants here."""
import datetime as dt
import math

import numpy as np

SEED = 255
SALT = 2
POOL = "Fallowmere Intergovernmental Risk Pool"
POOL_SHORT = "Fallowmere"
AS_OF = dt.date(2026, 9, 30)          # the claims extracts and the actuarial study's evaluation date
STUDY_DATE = dt.date(2026, 10, 9)     # the actuary's 2026 study
QUOTE_DATE = dt.date(2026, 10, 2)     # the broker's indications for 1 January 2027
BOARD_DATE = dt.date(2026, 11, 18)    # the trustees adopt the 2027 budget and the retention
COVER_YEAR = 2027

FIT_YEARS = list(range(2014, 2022))   # the severity curve's accident years, every occurrence now closed
OPEN_YEARS = list(range(2022, 2027))
ALL_YEARS = FIT_YEARS + OPEN_YEARS

# the pool's per-occurrence retention, inclusive of the member's deductible, by accident year
RETENTION = {y: (250_000 if y <= 2017 else 500_000) for y in ALL_YEARS}
DEDUCTIBLES = (10_000, 25_000, 50_000, 100_000)
ANCHOR = 25_000                        # the actuary's frequency is counted above this ground-up amount
OPTIONS = (1_000_000, 1_500_000, 2_000_000, 2_500_000, 3_000_000, 4_000_000, 5_000_000)   # quoted attachments
BAR = 1.0                              # the policy: no layer the pool expects to be reached more than once a year
COUNT_25K = 228.7                      # the actuary's expected 2027 occurrences costing more than $25,000 ground up
# the broker's indications: per attachment, the rate per $1,000 of the members' 2027 operating expenditures and the
# rate per unit on the members' vehicle schedules at 30 September 2026, for $10,000,000 per occurrence above it
QUOTES = {1_000_000: (0.2385, 71.40), 1_500_000: (0.1917, 57.55), 2_000_000: (0.1606, 48.20),
          2_500_000: (0.1378, 41.35), 3_000_000: (0.1201, 36.05), 4_000_000: (0.0941, 28.30),
          5_000_000: (0.0762, 22.90)}
DED_CUTS = (0.15, 0.42, 0.72)          # members ranked by size: the largest carry the $100,000 deductible

# liability claim cost index (accident year average, 2014 = 100.0), the 2027 value the study's projection
INDEX = {2012: 90.1, 2013: 95.2, 2014: 100.0, 2015: 105.3, 2016: 110.9, 2017: 117.4, 2018: 124.6, 2019: 132.1, 2020: 138.8,
         2021: 147.9, 2022: 158.6, 2023: 169.5, 2024: 180.1, 2025: 191.4, 2026: 203.2, 2027: 215.6}

# the ground-up severity of a liability occurrence at 2027 cost (lognormal in dollars)
MU, SIGMA = 9.90, 1.80
# ground-up liability occurrences a year at the 2027 membership, every size (the members never see most of them
# as claims: they are the curve the pool's record is a window on)
GROUND_RATE = 520.0

PEOPLE = {
    "director": ("Laura Williams", "Finance Director"),
    "actuary": ("Larry Hodge", "Consulting Actuary"),
    "broker": ("Matthew Klein", "Account Executive"),
    "claims": ("Caleb Payne", "Claims Manager"),
}


def factor(ay):
    """The multiplier bringing an accident year's dollars to 2027 cost."""
    return INDEX[COVER_YEAR] / INDEX[ay]


# ---------------------------------------------------------------- members
KINDS = [("city", 34), ("fire district", 9), ("water-sewer district", 7), ("port district", 3),
         ("transit authority", 2), ("park and recreation district", 4), ("library district", 3)]
JOINS = {2016: 2, 2019: 3, 2022: 2, 2024: 1}   # members admitted on 1 January of these years
WITHDRAWALS = {2020: 1, 2023: 1}               # members who left on 31 December of the year before


def members(rng):
    out = []
    n = sum(k for _, k in KINDS)
    kinds = [kd for kd, k in KINDS for _ in range(k)]
    order = rng.permutation(n)
    weights = rng.lognormal(0.0, 1.05, n)
    for i, j in enumerate(order):
        out.append({"no": 101 + i, "kind": kinds[j], "w": float(weights[j]), "joined": FIT_YEARS[0], "left": None})
    # admissions and withdrawals
    pool = [m for m in out]
    idx = list(rng.permutation(len(pool)))
    for y in sorted(JOINS):
        for _ in range(JOINS[y]):
            pool[idx.pop()]["joined"] = y
    for y in sorted(WITHDRAWALS):
        for _ in range(WITHDRAWALS[y]):
            m = pool[idx.pop()]
            m["left"] = y - 1
    # deductible elections: larger members carry larger deductibles
    ranked = sorted(out, key=lambda m: -m["w"])
    for r, m in enumerate(ranked):
        q = r / len(ranked)
        base = 3 if q < DED_CUTS[0] else 2 if q < DED_CUTS[1] else 1 if q < DED_CUTS[2] else 0
        m["ded_start"] = base
    for m in out:
        k = m["ded_start"]
        sched = [(dt.date(m["joined"], 1, 1), DEDUCTIBLES[k])]
        for y in range(m["joined"] + 1, 2027):
            if rng.random() < 0.055:
                step = 1 if (k < 3 and (k == 0 or rng.random() < 0.8)) else -1
                k = max(0, min(3, k + step))
                if DEDUCTIBLES[k] != sched[-1][1]:
                    sched.append((dt.date(y, 1, 1), DEDUCTIBLES[k]))
        m["deductibles"] = sched
    return out


def deductible_on(m, d):
    v = None
    for eff, ded in m["deductibles"]:
        if eff <= d:
            v = ded
    return v


def active(m, y):
    return m["joined"] <= y and (m["left"] is None or y <= m["left"])


# ---------------------------------------------------------------- occurrences
def occurrences(rng, mem):
    """Every ground-up liability occurrence of accident years 2014 to 2026 (2026 to the evaluation date), with its
    cost at 2027 cost and in its own year's dollars; the pool's record is the subset above each deductible."""
    out = []
    total_w = {y: sum(m["w"] for m in mem if active(m, y)) for y in ALL_YEARS}
    w27 = sum(m["w"] for m in mem if active(m, 2026))
    for y in ALL_YEARS:
        span = (AS_OF - dt.date(y, 1, 1)).days + 1 if y == AS_OF.year else (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
        days_in_year = (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
        lam = GROUND_RATE * (total_w[y] / w27) ** 0.85 * (span / days_in_year)
        n = int(rng.poisson(lam))
        act = [m for m in mem if active(m, y)]
        p = np.array([m["w"] for m in act]) ** 0.85
        p = p / p.sum()
        who = rng.choice(len(act), n, p=p)
        x27 = rng.lognormal(MU, SIGMA, n)
        day = rng.integers(0, span, n)
        for k in range(n):
            m = act[int(who[k])]
            d = dt.date(y, 1, 1) + dt.timedelta(days=int(day[k]))
            out.append({"ay": y, "date": d, "member": m["no"], "x27": float(x27[k]),
                        "x": float(x27[k]) / factor(y), "ded": deductible_on(m, d), "ret": RETENTION[y]})
    out.sort(key=lambda o: (o["date"], o["member"], o["x27"]))
    return out


def stream(part):
    """One random stream per component, so adding records to one file never moves another."""
    return np.random.default_rng([SEED, SALT, part])


def world():
    mem = members(stream(1))
    occ = occurrences(stream(2), mem)
    return mem, occ


def lognormal_sf(v, mu, sigma):
    return 0.5 * math.erfc((math.log(v) - mu) / (sigma * math.sqrt(2.0)))


# ---------------------------------------------------------------- member details
CLASS_CODE = {"city": "C", "fire district": "FD", "water-sewer district": "WS", "port district": "PT",
              "transit authority": "TR", "park and recreation district": "PR", "library district": "LB"}
DEPARTMENTS = {
    "city": ["General Government", "Police", "Fire", "Public Works", "Parks and Recreation", "Utilities"],
    "fire district": ["Administration", "Operations", "Prevention"],
    "water-sewer district": ["Administration", "Operations and Maintenance"],
    "port district": ["Administration", "Marine Terminals", "Airport"],
    "transit authority": ["Administration", "Operations", "Maintenance"],
    "park and recreation district": ["Administration", "Recreation", "Parks Maintenance"],
    "library district": ["Administration", "Branches"],
}
# operating expenditure per dollar of payroll, and payroll per FTE, by class (2027 budgets)
TOE_PER_PAYROLL = {"city": (2.45, 3.30), "fire district": (1.55, 1.95), "water-sewer district": (3.6, 5.2),
                   "port district": (3.1, 4.6), "transit authority": (2.6, 3.4), "park and recreation district": (2.0, 2.7),
                   "library district": (1.7, 2.2)}
PAY_PER_FTE = {"city": 98_000, "fire district": 112_000, "water-sewer district": 91_000, "port district": 96_000,
               "transit authority": 88_000, "park and recreation district": 71_000, "library district": 74_000}
CONSORTIUM_LOAD = dt.date(2025, 3, 3)        # the fleet consortium's lists loaded into the pool's schedule
CONSORTIUM_EFFECTIVE = dt.date(2025, 3, 1)
SCHEDULE_OPENED = dt.date(2022, 1, 1)        # the pool's current vehicle schedule system went live
LOG_EXTRACT = dt.date(2026, 10, 19)
RATING_DATE = dt.date(2026, 9, 30)           # the quotes rate the units on the schedule at this date


def member_details(rng, mem):
    """Legacy member codes, the departments each 2027 member declared, intake route, fleet consortium."""
    seq = {}
    for m in sorted(mem, key=lambda m: m["no"]):
        c = CLASS_CODE[m["kind"]]
        seq[c] = seq.get(c, 0) + 1
        m["code"] = "%s-%02d" % (c, seq[c])
    live27 = [m for m in mem if m["left"] is None]
    # two members of every class (both transit authorities) run their fleets through the regional consortium
    for kind, _ in KINDS:
        cands = sorted([m for m in live27 if m["kind"] == kind and m["joined"] <= 2024], key=lambda m: m["no"])
        k = 2 if kind != "city" else 4
        pick = rng.choice(len(cands), size=min(k, len(cands)), replace=False)
        for i in sorted(int(x) for x in pick):
            cands[i]["consortium"] = True
    for m in mem:
        m.setdefault("consortium", False)
    # departments declared for 2027 and the intake route (online form or the paper form keyed by staff)
    for m in live27:
        deps = DEPARTMENTS[m["kind"]]
        if m["kind"] == "city":
            n = 3 if m["w"] < 0.35 else 4 if m["w"] < 0.9 else 5 if m["w"] < 2.2 else 6
            keep = ["General Government", "Police", "Public Works"] + [d for d in deps if d not in
                                                                       ("General Government", "Police", "Public Works")]
            deps = [d for d in deps if d in keep[:n]]
        elif len(deps) == 3 and m["w"] < 0.5:
            deps = deps[:2]
        m["departments"] = deps
        m["paper"] = bool(rng.random() < 0.24)
    # every class keeps at least one online member declaring two or more departments
    for kind, _ in KINDS:
        cl = sorted([m for m in live27 if m["kind"] == kind], key=lambda m: m["no"])
        if not any((not m["paper"]) and len(m["departments"]) >= 2 for m in cl):
            cl[0]["paper"] = False
    return mem


# ---------------------------------------------------------------- the claims record
CONVERSION = dt.date(2020, 7, 1)             # the current administrator took over the pool's claims
LEGACY_ADMIN = "Tallowmark Claims Services"
CURRENT_ADMIN = "Brisbrook Risk Services"
PARTS = ("GL", "AL", "LE", "PO", "EP")       # general, auto, law enforcement, public officials, employment practices
PART_MIX = {"city": (0.31, 0.27, 0.24, 0.10, 0.08), "fire district": (0.36, 0.40, 0.0, 0.12, 0.12),
            "water-sewer district": (0.52, 0.28, 0.0, 0.10, 0.10), "port district": (0.50, 0.26, 0.06, 0.10, 0.08),
            "transit authority": (0.30, 0.56, 0.0, 0.06, 0.08), "park and recreation district": (0.62, 0.18, 0.0, 0.10, 0.10),
            "library district": (0.56, 0.10, 0.0, 0.16, 0.18)}


def _cents(v):
    return round(v + 1e-9, 2)


def development(rng, mem, occ):
    """What the pool's two administrators recorded for each occurrence that came to the pool: an occurrence comes
    when its member's payments exhaust the deductible, the pool pays the rest up to its retention, and the excess
    insurer pays above that outside the pool's system. Returns the record rows, each with its truth."""
    byno = {m["no"]: m for m in mem}
    rows = []
    for o in occ:
        if o["x"] <= o["ded"]:
            continue
        m = byno[o["member"]]
        x = _cents(o["x"])
        if x <= o["ded"]:
            continue
        mix = np.array(PART_MIX[m["kind"]])
        part = PARTS[int(rng.choice(5, p=mix / mix.sum()))]
        s = 1.0 if rng.random() < 0.11 else float(rng.beta(2.2, 4.5))      # share of the cost that was defence
        tender = o["date"] + dt.timedelta(days=int(18 + rng.gamma(1.5, 80.0)))
        dur = float(rng.lognormal(math.log(250.0 * (x / 40_000.0) ** 0.25), 0.55))
        close = tender + dt.timedelta(days=int(30 + dur))
        if o["ay"] in FIT_YEARS and close > dt.date(2026, 6, 30):
            close = dt.date(2026, 6, 30) - dt.timedelta(days=int(rng.integers(0, 200)))
            close = max(close, tender + dt.timedelta(days=30))
        cap = o["ret"]
        pool_ult = _cents(min(x, cap) - o["ded"])
        r = {"ay": o["ay"], "date": o["date"], "member": o["member"], "ded": o["ded"], "ret": cap, "x": x,
             "x27": o["x27"], "part": part, "s": s, "tender": tender, "close": close, "pool_ult": pool_ult,
             "capped": x >= cap}
        if tender > AS_OF:
            r["status"] = "untendered"
        elif close <= AS_OF:
            r["status"] = "closed"
        else:
            r["status"] = "open"
        r["system"] = "legacy" if (r["status"] == "closed" and close < CONVERSION) else "current"
        r["converted"] = r["system"] == "current" and tender < CONVERSION
        # paid and reserved at the evaluation date (closed: paid in full; open: part paid, a case reserve beside it)
        if r["status"] == "closed":
            paid = pool_ult
            reserve = 0.0
        elif r["status"] == "open":
            frac = ((AS_OF - tender).days / max(1, (close - tender).days)) ** 1.3
            paid = _cents(pool_ult * min(0.92, frac))
            reserve = _cents(max(0.0, (pool_ult - paid) * float(rng.lognormal(0.0, 0.35))))
            reserve = min(reserve, _cents(cap - o["ded"] - paid))
        else:
            paid = reserve = 0.0
        pi = _cents(paid * (1 - s))
        r.update(paid_ind=pi, paid_def=_cents(paid - pi))
        ri = _cents(reserve * (1 - s))
        r.update(res_ind=ri, res_def=_cents(reserve - ri))
        rows.append(r)
    # claim numbers: the legacy administrator by accident year in tender order; the current one by tender year,
    # converted claims from the conversion block with their legacy numbers kept
    seq = {}
    for r in sorted(rows, key=lambda r: (r["tender"], r["member"], r["x"])):
        if r["status"] == "untendered":
            continue
        if r["tender"] < CONVERSION:
            k = ("L", r["ay"])
            seq[k] = seq.get(k, 0) + 1
            r["legacy_no"] = "FL%02d-%04d" % (r["ay"] % 100, seq[k])
        if r["system"] == "current":
            if r["converted"]:
                k = ("X",)
                seq[k] = seq.get(k, 0) + 1
                r["claim_no"] = "LX-%05d" % (seq[k] + 120)
            else:
                k = ("C", r["tender"].year)
                seq[k] = seq.get(k, 0) + 1
                r["claim_no"] = "L%d-%05d" % (r["tender"].year, seq[k] + 30)
    return rows


# ---------------------------------------------------------------- fleets and the schedule log
UNIT_CLASSES = ("private passenger", "light truck", "heavy truck", "bus", "emergency vehicle", "trailer",
                "mobile equipment")
FLEET_MIX = {"city": (0.34, 0.30, 0.10, 0.0, 0.14, 0.06, 0.06), "fire district": (0.10, 0.20, 0.05, 0.0, 0.55, 0.05, 0.05),
             "water-sewer district": (0.10, 0.45, 0.15, 0.0, 0.0, 0.15, 0.15),
             "port district": (0.10, 0.35, 0.15, 0.0, 0.0, 0.20, 0.20), "transit authority": (0.10, 0.15, 0.05, 0.60, 0.0, 0.0, 0.10),
             "park and recreation district": (0.15, 0.40, 0.0, 0.0, 0.0, 0.20, 0.25),
             "library district": (0.40, 0.40, 0.20, 0.0, 0.0, 0.0, 0.0)}
FLEET_BASE = {"city": (15, 70), "fire district": (8, 22), "water-sewer district": (6, 24), "port district": (10, 30),
              "transit authority": (40, 80), "park and recreation district": (5, 14), "library district": (2, 4)}
MAKES = {"private passenger": [("Ford", "1FM"), ("Chevrolet", "1G1"), ("Toyota", "4T1"), ("Dodge", "2C3")],
         "light truck": [("Ford", "1FT"), ("Chevrolet", "1GC"), ("Ram", "3C6"), ("Toyota", "5TF")],
         "heavy truck": [("Freightliner", "1FV"), ("International", "1HT"), ("Peterbilt", "1NP"), ("Kenworth", "1XK")],
         "bus": [("Gillig", "15G"), ("New Flyer", "5FY"), ("Ford", "1FD")],
         "emergency vehicle": [("Ford", "1FM"), ("Chevrolet", "1GN"), ("Pierce", "4P1"), ("Dodge", "2C3")],
         "trailer": [("Big Tex", "16V"), ("Wells Cargo", "1WC"), ("Felling", "5FT")],
         "mobile equipment": [("John Deere", "1T0"), ("Caterpillar", "CAT"), ("Bobcat", "ALJ"), ("Kubota", "JKU")]}
NO_VIN = ("NONE", "N/A", "", "UNKNOWN", "SEE SERIAL")
YEAR_CODE = {2008: "8", 2009: "9", 2010: "A", 2011: "B", 2012: "C", 2013: "D", 2014: "E", 2015: "F", 2016: "G",
             2017: "H", 2018: "J", 2019: "K", 2020: "L", 2021: "M", 2022: "N", 2023: "P", 2024: "R", 2025: "S", 2026: "T",
             2027: "V"}
VIN_CHARS = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
_TRANS = dict(zip("ABCDEFGHJKLMNPRSTUVWXYZ", (1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 7, 9, 2, 3, 4, 5, 6, 7, 8, 9)))
_WEIGHTS = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)


def vin(rng, wmi, year):
    body = wmi + "".join(VIN_CHARS[int(i)] for i in rng.integers(0, len(VIN_CHARS), 5))
    tail = YEAR_CODE[year] + VIN_CHARS[int(rng.integers(0, 23))] + "%06d" % int(rng.integers(0, 10 ** 6))
    v = body + "0" + tail
    tot = sum((_TRANS[c] if c.isalpha() else int(c)) * w for c, w in zip(v, _WEIGHTS))
    chk = tot % 11
    return body + ("X" if chk == 10 else str(chk)) + tail


def keyed(rng, v):
    """A VIN or serial as the members' staff typed it into the schedule system."""
    u = rng.random()
    if not v or u < 0.85:
        return v
    if u < 0.93:
        return v.lower()
    if u < 0.97:
        return v[:8] + " " + v[8:]
    return v[:3] + "-" + v[3:]


def fleets(rng, mem):
    """Each member's units with their service dates, the schedule log the pool's system keeps, and the truth."""
    units, log = [], []
    unit_seq = [180_000]
    fmc_seq = [4_000]

    def new_unit(m, cls, acquired, model_year):
        make, wmi = MAKES[cls][int(rng.integers(0, len(MAKES[cls])))]
        has_vin = cls not in ("trailer", "mobile equipment") or rng.random() < (0.55 if cls == "trailer" else 0.3)
        v = vin(rng, wmi, model_year) if has_vin else ""
        serial = "" if has_vin else ("%s%07d" % ({"trailer": "TS", "mobile equipment": "SN"}[cls], int(rng.integers(0, 10 ** 7))))
        life = int(rng.integers(6 * 365, 13 * 365))
        unit_seq[0] += int(rng.integers(1, 4))
        u = {"member": m["no"], "unit_no": "%06d" % unit_seq[0], "cls": cls, "make": make, "year": model_year,
             "vin": v, "serial": serial, "acquired": acquired, "disposed": acquired + dt.timedelta(days=life),
             "value": float(round(rng.lognormal(math.log({"private passenger": 31_000, "light truck": 44_000,
                                                          "heavy truck": 148_000, "bus": 520_000,
                                                          "emergency vehicle": 96_000, "trailer": 9_500,
                                                          "mobile equipment": 61_000}[cls]), 0.35), -2)),
             "vin_keyed": keyed(rng, v), "serial_keyed": keyed(rng, serial),
             "placeholder": NO_VIN[int(rng.integers(0, len(NO_VIN)))] if not has_vin else None}
        units.append(u)
        return u

    for m in sorted(mem, key=lambda m: m["no"]):
        start = max(SCHEDULE_OPENED, dt.date(m["joined"], 1, 1))
        end = dt.date(m["left"], 12, 31) if m["left"] is not None else None
        if end is not None and end < SCHEDULE_OPENED:
            continue
        a, b = FLEET_BASE[m["kind"]]
        n0 = int(round(a + b * m["w"] ** 0.85 * float(rng.uniform(0.85, 1.15))))
        mix = np.array(FLEET_MIX[m["kind"]])
        for _ in range(n0):
            cls = UNIT_CLASSES[int(rng.choice(7, p=mix / mix.sum()))]
            age = int(rng.integers(0, 11 * 365))
            acq = start - dt.timedelta(days=age)
            u = new_unit(m, cls, acq, min(2026, max(2008, acq.year + int(rng.integers(0, 2)))))
            while u["disposed"] <= start:
                u["disposed"] = start + dt.timedelta(days=int(rng.integers(30, 3 * 365)))
        # replacements and growth until the log is extracted
        mine = [u for u in units if u["member"] == m["no"]]
        queue = sorted(mine, key=lambda u: u["disposed"])
        while queue:
            u = queue.pop(0)
            if u["disposed"] > LOG_EXTRACT or (end is not None and u["disposed"] > end):
                continue
            acq = u["disposed"] + dt.timedelta(days=int(rng.integers(-20, 60)))
            if acq > LOG_EXTRACT or (end is not None and acq > end):
                continue
            nu = new_unit(m, u["cls"], max(acq, start), max(2008, min(2027, acq.year + int(rng.integers(0, 2)))))
            queue.append(nu)
            queue.sort(key=lambda x: x["disposed"])
            if rng.random() < 0.035:
                cls = UNIT_CLASSES[int(rng.choice(7, p=mix / mix.sum()))]
                g = new_unit(m, cls, max(acq, start) + dt.timedelta(days=int(rng.integers(1, 90))),
                             max(2008, min(2027, acq.year + 1)))
                queue.append(g)
                queue.sort(key=lambda x: x["disposed"])
        if end is not None:
            for u in units:
                if u["member"] == m["no"] and u["disposed"] > end:
                    u["disposed"] = end
    return units


def schedule_log(rng, mem, units):
    """The pool's vehicle schedule as its system logs it: the opening load, members' adds, deletes and changes, the
    renewal revaluations, and on 3 March 2025 the fleet consortium's lists loaded under the consortium's asset
    numbers. The consortium's later disposals reach the pool on its numbers only."""
    byno = {m["no"]: m for m in mem}
    rows = []

    def entered(eff, lo=-25, hi=21):
        return eff + dt.timedelta(days=int(rng.integers(lo, hi)))

    first_entry = {}

    def row(u, unit_no, kind, eff, ent, vin_text, serial_text, value):
        # nothing is keyed before the system's opening load, and nothing about a unit before its add
        ent = max(ent, dt.date(2021, 12, 1))
        if kind == "ADD":
            first_entry[unit_no] = ent
        else:
            ent = max(ent, first_entry[unit_no] + dt.timedelta(days=1))
        rows.append({"member": u["member"], "unit_no": unit_no, "type": kind, "effective": eff, "entered": ent,
                     "vin": vin_text, "serial": serial_text, "year": u["year"], "make": u["make"], "cls": u["cls"],
                     "value": value, "u": u})

    fmc = [7_300]
    for u in units:
        m = byno[u["member"]]
        pool_vin = u["vin_keyed"] if u["vin"] else u["placeholder"]
        first = max(u["acquired"], SCHEDULE_OPENED)
        if u["acquired"] <= SCHEDULE_OPENED:
            ent = dt.date(2021, 12, 1) + dt.timedelta(days=int(rng.integers(0, 28)))
        else:
            ent = entered(first, -10, 18)
        cons = m["consortium"]
        loaded = cons and u["acquired"] <= CONSORTIUM_EFFECTIVE < u["disposed"]
        after = cons and u["acquired"] > CONSORTIUM_EFFECTIVE
        if after:
            fmc[0] += int(rng.integers(1, 3))
            u["fmc"] = "FMC-%05d" % fmc[0]
            row(u, u["fmc"], "ADD", first, entered(first, 0, 18), u["vin"], u["serial"], u["value"])
        else:
            row(u, u["unit_no"], "ADD", first, ent, pool_vin, u["serial_keyed"], u["value"])
        if loaded:
            fmc[0] += int(rng.integers(1, 3))
            u["fmc"] = "FMC-%05d" % fmc[0]
            row(u, u["fmc"], "ADD", CONSORTIUM_EFFECTIVE, CONSORTIUM_LOAD, u["vin"], u["serial"], u["value"])
        # renewal revaluations on 1 January, every unit number the system holds in force
        for y in (2023, 2024, 2025, 2026):
            d = dt.date(y, 1, 1)
            alive_pool = (not after) and first <= d and (u["disposed"] > d or (cons and loaded and
                                                                               u["disposed"] > CONSORTIUM_EFFECTIVE))
            alive_fmc = "fmc" in u and (CONSORTIUM_EFFECTIVE <= d or after) and first <= d < u["disposed"]
            dep = round(u["value"] * (0.9 ** (y - max(2022, u["acquired"].year))), -2)
            ent = dt.date(y - 1, 12, 9) + dt.timedelta(days=int(rng.integers(0, 6)))
            if alive_pool:
                row(u, u["unit_no"], "CHANGE", d, ent, pool_vin, u["serial_keyed"], dep)
            if alive_fmc:
                row(u, u["fmc"], "CHANGE", d, ent, u["vin"], u["serial"], dep)
        # an occasional garaging or value change during the year
        if rng.random() < 0.23:
            d = first + dt.timedelta(days=int(rng.integers(40, 900)))
            if d < min(u["disposed"], LOG_EXTRACT):
                if "fmc" in u and d >= CONSORTIUM_EFFECTIVE:
                    row(u, u["fmc"], "CHANGE", d, entered(d, 0, 20), u["vin"], u["serial"], u["value"])
                elif not after:
                    row(u, u["unit_no"], "CHANGE", d, entered(d, 0, 20), pool_vin, u["serial_keyed"], u["value"])
        # disposal
        if u["disposed"] <= LOG_EXTRACT + dt.timedelta(days=90):
            ent = entered(u["disposed"], -45, 18)
            if ent <= LOG_EXTRACT:
                if "fmc" in u and u["disposed"] >= CONSORTIUM_EFFECTIVE:
                    row(u, u["fmc"], "DELETE", u["disposed"], ent, u["vin"], u["serial"], None)
                else:
                    row(u, u["unit_no"], "DELETE", u["disposed"], ent, pool_vin, u["serial_keyed"], None)
    rows = [r for r in rows if r["entered"] <= LOG_EXTRACT]
    rows.sort(key=lambda r: (r["entered"], r["member"], r["unit_no"], {"ADD": 0, "CHANGE": 1, "DELETE": 2}[r["type"]]))
    for i, r in enumerate(rows):
        r["txn"] = "T%07d" % (2_204_117 + i * 3 + (i * 7919) % 3)
    return rows


def declarations(rng, mem):
    """Each 2027 member's declared departments (FTE and payroll) and its total operating expenditure."""
    out = []
    for m in sorted((m for m in mem if m["left"] is None), key=lambda m: m["no"]):
        scale = {"city": 300, "fire district": 50, "water-sewer district": 30, "port district": 60,
                 "transit authority": 160, "park and recreation district": 30, "library district": 20}[m["kind"]]
        fte_total = 6 + scale * m["w"] ** 0.9 * float(rng.uniform(0.85, 1.15))
        shares = rng.dirichlet(np.full(len(m["departments"]), 3.0))
        lo, hi = TOE_PER_PAYROLL[m["kind"]]
        lines = []
        payroll_total = 0
        for dep, sh in zip(m["departments"], shares):
            fte = round(max(1.0, fte_total * float(sh)), 1)
            pay = int(round(fte * PAY_PER_FTE[m["kind"]] * float(rng.uniform(0.9, 1.12)), -2))
            payroll_total += pay
            lines.append({"department": dep, "fte": fte, "payroll": pay})
        toe = int(round(payroll_total * float(rng.uniform(lo, hi)), 0))
        sub = dt.date(2026, 8, 3) + dt.timedelta(days=int(rng.integers(0, 50)))
        basis = "Adopted" if rng.random() < 0.3 else "Proposed"
        out.append({"member": m["no"], "kind": m["kind"], "lines": lines, "toe": toe, "submitted": sub, "basis": basis,
                    "paper": m["paper"]})
    return out
