"""The world of task479 (architecture 5): the Merrin Valley Schools Health Cooperative, sixteen school districts pooling
a self-funded medical and pharmacy plan administered by Tollard Benefit Services, each district on its own benefit
design and contribution rate, the plan year the calendar year.

A member meets the deductible before the plan pays, so a plan year's plan-paid claims are light in January and heavy
by the autumn, and the higher the deductible the more of the year's claims fall late. Four districts moved from the
$500 design to the $3,000 design on 1 January 2026: their own 2025 says how a $500 plan year falls, and the January to
June 2026 claims they have run on the $3,000 design carry less of the year than that.

    x = build()    the truth: districts, members, enrollment, monthly plan-paid claims, the advisories, the rates"""
import calendar
import datetime as dt

import numpy as np

SEED = 4795
DESIGNS = (500, 1500, 3000)
OOP = {500: 2500, 1500: 4000, 3000: 6000}
COINS = 0.20
RX_PMPM = 94.30                   # pharmacy plan paid per member per month, copays only, no deductible
ADVISORY = 125_000                # the carrier's 50 per cent advisory threshold on the $250,000 specific deductible
SPECIFIC = 250_000

# district id, name, 2025 deductible, 2026 deductible, members, 2025 plan-paid PMPM scale, place of the 2026 claims
# component: "both" over on the golden and the own-history route, "golden" over on the golden only, "under" under on
# every route the design names
DISTRICTS = [
    ("MV03", "Alwick School District", 500, 500, 820, 1.02, "both"),
    ("MV07", "Brantmoor Public Schools", 500, 3000, 610, 0.98, "golden"),
    ("MV11", "Carrow Hill School District", 1500, 1500, 1140, 1.00, "under"),
    ("MV14", "Dellacourt Area Schools", 500, 500, 470, 0.95, "under"),
    ("MV18", "Eversley Plains School District", 3000, 3000, 690, 1.04, "under"),
    ("MV21", "Farrowdale Consolidated Schools", 500, 3000, 930, 1.06, "golden"),
    ("MV25", "Gilsby Township Schools", 1500, 1500, 540, 0.97, "both"),
    ("MV28", "Harlow Bend School District", 500, 500, 760, 1.01, "under"),
    ("MV32", "Isenbrook Unified Schools", 500, 3000, 1280, 0.99, "under"),
    ("MV36", "Kestrel Point School District", 3000, 3000, 580, 1.03, "both"),
    ("MV39", "Larchwood Valley Schools", 1500, 1500, 880, 0.96, "under"),
    ("MV43", "Mossgate Community Schools", 500, 500, 650, 1.05, "under"),
    ("MV47", "Northam Vale School District", 500, 3000, 720, 1.00, "golden"),
    ("MV50", "Orrin Creek School District", 1500, 1500, 1010, 1.02, "under"),
    ("MV54", "Pellow Ridge Area Schools", 3000, 3000, 560, 0.98, "under"),
    ("MV58", "Quillon County Schools", 500, 500, 900, 1.00, "under"),
]
IDS = [d[0] for d in DISTRICTS]
MONTHS25 = [(2025, m) for m in range(1, 13)]
MONTHS26 = [(2026, m) for m in range(1, 10)]
H1 = [(2026, m) for m in range(1, 7)]
TREND = 1.062


def patterns():
    """Each design's share of a plan year's plan-paid claims by incurred month, and its plan-paid PMPM relativity,
    from one large simulation of members' allowed claims run through the design (deductible, 20 per cent
    coinsurance, out-of-pocket maximum; pharmacy at copays only)."""
    rng = np.random.default_rng(SEED + 100)
    n = 150_000
    season = np.array([1.06, 1.03, 1.04, 0.99, 0.98, 0.95, 0.93, 0.97, 1.00, 1.02, 1.00, 1.03])
    season /= season.mean()
    ann = rng.lognormal(7.9, 1.45, n)
    ann[rng.random(n) < 0.12] = 0.0
    med = ann[:, None] * rng.dirichlet(season * 0.6, n)
    cum = np.cumsum(med, 1)
    prev = cum - med
    out = {}
    for d in DESIGNS:
        def cost(v):
            return np.minimum(np.minimum(v, d) + COINS * np.maximum(v - d, 0), OOP[d])
        plan = (med - (cost(cum) - cost(prev))).sum(0) + RX_PMPM * n
        out[d] = {"share": plan / plan.sum(), "pmpm": plan.sum() / n / 12}
    return out


def build():
    rng = np.random.default_rng(SEED)
    pat = patterns()
    members = []
    nid = 0
    for did, name, d25, d26, n, scale, place in DISTRICTS:
        seen = set()
        fams = []
        sub = 0
        size = 0
        while size < n:
            sub += 1
            fam = 1 + int(rng.choice([0, 0, 1, 1, 2, 3], p=[0.30, 0.12, 0.2, 0.13, 0.15, 0.10]))
            fams.append((sub, fam))
            size += fam
        # a family on the plan from January 2025, a few leaving during the period and replaced the next month by a
        # family hired into the post
        all_months = MONTHS25 + MONTHS26
        for sub, fam in fams:
            spans = [(0, len(all_months) - 1)]
            if rng.random() < 0.07:
                t = int(rng.integers(1, len(all_months) - 1))
                spans = [(0, t - 1), (t, len(all_months) - 1)]
            for j, (a, b) in enumerate(spans):
                s = sub if j == 0 else 10_000 + sub
                f = fam if j == 0 else 1 + int(rng.choice([0, 1, 2, 3], p=[0.4, 0.25, 0.2, 0.15]))
                byear = int(rng.integers(1962, 2003))
                for k in range(f):
                    nid += 1
                    rel = "EE" if k == 0 else ("SP" if k == 1 else "CH")
                    by = byear if k == 0 else (byear + int(rng.integers(-4, 5)) if rel == "SP"
                                               else int(rng.integers(2004, 2025)))
                    while True:
                        bd = dt.date(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
                        sx = "F" if rng.random() < 0.5 else "M"
                        if (bd, sx, rel) not in seen:
                            seen.add((bd, sx, rel))
                            break
                    members.append({"k": nid, "district": did, "sub": s, "rel": rel, "birth": bd, "sex": sx,
                                    "start": all_months[a], "end": all_months[b]})
    x = {"members": members, "pat": pat}
    _claims(x, rng)
    _advisories(x, rng)
    _rates(x, rng)
    return x


def member_months(x, did, months):
    ms = set(months)
    return sum(1 for m in x["members"] if m["district"] == did for ym in ms if m["start"] <= ym <= m["end"])


def _claims(x, rng):
    """Plan-paid claims by district and incurred month, January 2025 to September 2026 (and October to December 2024
    for the lag report's early paid months): each month the plan year's claims times the design's monthly share, with
    the month's own noise; pharmacy at its flat PMPM, medical the rest."""
    pat = x["pat"]
    paid = {}
    for did, name, d25, d26, n, scale, place in DISTRICTS:
        mm = {ym: member_months(x, did, [ym]) for ym in MONTHS25 + MONTHS26}
        base = 0.97 * scale * pat[500]["pmpm"]                    # the district's 2025 PMPM on the $500 design
        p25 = base * pat[d25]["pmpm"] / pat[500]["pmpm"]
        p26 = base * TREND * pat[d26]["pmpm"] / pat[500]["pmpm"] * float(rng.uniform(0.985, 1.015))
        for (y, m), pp, d in [(ym, p25, d25) for ym in MONTHS25] + [(ym, p26, d26) for ym in MONTHS26]:
            tot = pp * 12 * pat[d]["share"][m - 1] * mm[(y, m)] * (1 + float(rng.normal(0, 0.008)))
            rx = RX_PMPM * mm[(y, m)] * (1 + float(rng.normal(0, 0.01)))
            paid[(did, (y, m), "Medical")] = round(tot - rx, 2)
            paid[(did, (y, m), "Pharmacy")] = round(rx, 2)
        for m in (10, 11, 12):
            tot = p25 / TREND * 12 * pat[d25]["share"][m - 1] * mm[(2025, 1)]
            rx = RX_PMPM * mm[(2025, 1)] * 0.97
            paid[(did, (2024, m), "Medical")] = round(tot - rx, 2)
            paid[(did, (2024, m), "Pharmacy")] = round(rx, 2)
    x["paid"] = paid
    _center(x)


def _sum(x, did, months):
    ms = set(months)
    return sum(v for (d, ym, c), v in x["paid"].items() if d == did and ym in ms)


def factors(x):
    """Per district the plan year 2025 PMPM over its January to June 2025 PMPM."""
    out = {}
    for did, *_ in DISTRICTS:
        fy = _sum(x, did, MONTHS25) / member_months(x, did, MONTHS25)
        h = _sum(x, did, MONTHS25[:6]) / member_months(x, did, MONTHS25[:6])
        out[did] = (fy, h, _sum(x, did, MONTHS25), _sum(x, did, MONTHS25[:6]), member_months(x, did, MONTHS25),
                    member_months(x, did, MONTHS25[:6]))
    return out


def estimates(x):
    """Each district's expected plan year 2026 plan-paid PMPM: its January to June 2026 PMPM completed by the
    ratio of a plan year's PMPM to its first half's, under the routes the design names, and the forms of the golden a
    competent analyst might write (checks.py asserts they round alike)."""
    f = factors(x)
    d25 = {d[0]: d[2] for d in DISTRICTS}
    d26 = {d[0]: d[3] for d in DISTRICTS}

    def pooled(ids):
        return (sum(f[i][2] for i in ids) / sum(f[i][4] for i in ids)) / (sum(f[i][3] for i in ids) /
                                                                          sum(f[i][5] for i in ids))

    def mean_k(ids):
        return float(np.mean([f[i][0] / f[i][1] for i in ids]))

    def paid_share(ids):
        return sum(f[i][2] for i in ids) / sum(f[i][3] for i in ids)
    same = {d: [i for i in IDS if d25[i] == d] for d in DESIGNS}
    k_design = {d: pooled(same[d]) for d in DESIGNS}
    k_all = pooled(IDS)
    out = {}
    for did in IDS:
        mm1 = member_months(x, did, H1)
        p1 = _sum(x, did, H1)
        h1 = p1 / mm1
        d = d26[did]
        own = f[did][0] / f[did][1]
        forms = {"ratio_of_totals": h1 * k_design[d], "mean_of_ratios": h1 * mean_k(same[d]),
                 "paid_share": p1 * paid_share(same[d]) / (2 * mm1)}
        if d25[did] == d:
            forms["own_history"] = h1 * own
        else:
            forms["own_history_relativity"] = h1 * own * k_design[d] / k_design[d25[did]]
        out[did] = {"h1": h1, "golden": forms["ratio_of_totals"], "default": h1 * own, "pooled": h1 * k_all,
                    "annualised": h1, "forms": forms}
    x["k_design"] = k_design
    return out


def _center(x):
    """Scale each district's 2026 claims so every form of its golden estimate falls inside one ten-dollar bin, a
    dollar or more from either edge (every form is proportional to the district's 2026 claims)."""
    rng = np.random.default_rng(SEED + 7)
    est = estimates(x)
    for did in IDS:
        v = list(est[did]["forms"].values())
        lo, hi = min(v), max(v)
        mid, half = (lo + hi) / 2, (hi - lo) / 2
        slack = 5 - 1.0 - half
        assert slack > 0, (did, lo, hi)
        target = 10 * round(mid / 10) + float(rng.uniform(-slack, slack))
        k = target / mid
        for key in list(x["paid"]):
            if key[0] == did and key[1][0] == 2026:
                x["paid"][key] = round(x["paid"][key] * k, 2)


def _rates(x, rng):
    """The claims component of each district's 2026 contribution rate, set by the trustees in October 2025 and placed
    against the estimates so each district sits where DISTRICTS puts it."""
    est = estimates(x)
    rates = {}
    for did, name, d25, d26, n, scale, place in DISTRICTS:
        e = est[did]
        g, d = e["golden"], e["default"]
        if place == "both":
            r = g / float(rng.uniform(1.04, 1.06))
        elif place == "golden":
            lo, hi = d * 1.025, g / 1.025
            assert lo < hi, (did, g, d)
            r = lo + (hi - lo) * float(rng.uniform(0.4, 0.6))
        else:
            r = max(g, d) * float(rng.uniform(1.04, 1.08))
        rates[did] = round(r, 2)
    x["rates"] = rates


def _advisories(x, rng):
    """Members whose 2026 claims reach the carrier's advisory threshold: one to three a district by its size,
    enrolled all of 2026 to date."""
    x["big26"] = {}
    for did, name, d25, d26, n, *_ in DISTRICTS:
        full = [m for m in x["members"] if m["district"] == did and m["start"] <= (2026, 1) and m["end"] == (2026, 9)]
        pick = rng.permutation(len(full))[:int(rng.integers(1, 3)) + (n >= 800)]
        for j in pick:
            full[j]["c26"] = float(rng.integers(205_000, 340_000)) + float(rng.integers(0, 100)) / 100
        x["big26"][did] = [full[j] for j in pick]


def month_end(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])
