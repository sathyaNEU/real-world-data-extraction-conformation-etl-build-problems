"""The world of task479 (architecture 6): the Corbel Ridge Business Health Trust, a chamber of commerce's self-funded
medical and pharmacy plan for eighteen member employers, administered by Hallam Benefit Administrators, with specific
stop-loss from Westerby Specialty Insurance Company at $150,000 a member a contract year.

Each employer's members cost the plan at the employer's own true level, and the employers truly differ by a little;
but most employers are small, and a year's retained claims for a small employer carry the luck of a few members, so its
2023 to 2025 experience spreads far wider than the true levels do. The expected 2027 claims of an employer are its own
experience weighed against the trust's by the share of its spread that is signal (credibility).

    x = build()    the truth: employers, members, enrollment, claims by member and month, the rates"""
import calendar
import datetime as dt

import numpy as np

SEED = 4796
SPECIFIC = 150_000
HCC = 25_000                      # Hallam's high-cost claimant report threshold
TREND = 0.07
YEARS = (2023, 2024, 2025)
TR = {y: (1 + TREND) ** (2027 - y) for y in YEARS}
BASE = 505.0                      # the trust's true 2027 retained PMPM
SD = 0.05
SHIFT = {"CR176": 0.16, "CR181": -0.16}   # two large employers whose true levels sit well off the trust's

# employer id, name, industry, members
EMPLOYERS = [
    ("CR104", "Ashdown Veterinary Clinic", "health care", 34),
    ("CR109", "Brightmere Signs & Graphics", "manufacturing", 41),
    ("CR113", "Calloway Hardware", "retail", 48),
    ("CR118", "Dunleith Title Company", "finance", 56),
    ("CR122", "Emberly Bakery Group", "food service", 63),
    ("CR127", "Fenwright Landscaping", "construction", 72),
    ("CR131", "Glasshouse Dental Partners", "health care", 85),
    ("CR136", "Harrowgate Machine Works", "manufacturing", 98),
    ("CR140", "Inglewell Accounting", "professional services", 112),
    ("CR145", "Juniper Ridge Montessori", "education", 130),
    ("CR149", "Kettering Lane Motors", "retail", 155),
    ("CR154", "Lowfield Logistics", "transportation", 185),
    ("CR158", "Marston Electric Supply", "wholesale", 225),
    ("CR163", "Northcote Engineering", "professional services", 280),
    ("CR167", "Oakhurst Credit Union", "finance", 360),
    ("CR172", "Penrose Senior Living", "health care", 470),
    ("CR176", "Quarrington Foods", "manufacturing", 640),
    ("CR181", "Rushmere County Library District", "public sector", 880),
]
IDS = [e[0] for e in EMPLOYERS]
MONTHS = [(y, m) for y in (2023, 2024, 2025) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]


def draw(rng, m):
    """A member-year's plan-paid claims relative to the plan's mean: a heavy-tailed body and rare large claims."""
    b = rng.lognormal(0.0, 1.35, m)
    big = rng.random(m) < 0.011
    b[big] += rng.lognormal(3.45, 0.55, big.sum())
    zero = rng.random(m) < 0.09
    b[zero] = 0.0
    return b


def build():
    rng = np.random.default_rng(SEED)
    members = []
    nid = 0
    for eid, name, ind, n in EMPLOYERS:
        seen = set()
        fams, sub, size = [], 0, 0
        while size < n:
            sub += 1
            fam = 1 + int(rng.choice([0, 0, 1, 1, 2, 3], p=[0.34, 0.12, 0.2, 0.12, 0.13, 0.09]))
            fams.append((sub, fam))
            size += fam
        for sub, fam in fams:
            spans = [(0, len(MONTHS) - 1)]
            if rng.random() < 0.10:
                t = int(rng.integers(1, len(MONTHS) - 1))
                spans = [(0, t - 1), (t, len(MONTHS) - 1)]
            for j, (a, b) in enumerate(spans):
                s = sub if j == 0 else 10_000 + sub
                f = fam if j == 0 else 1 + int(rng.choice([0, 1, 2, 3], p=[0.45, 0.25, 0.18, 0.12]))
                byear = int(rng.integers(1960, 2002))
                for k in range(f):
                    nid += 1
                    rel = "EE" if k == 0 else ("SP" if k == 1 else "CH")
                    by = byear if k == 0 else (byear + int(rng.integers(-4, 5)) if rel == "SP"
                                               else int(rng.integers(2003, 2025)))
                    while True:
                        bd = dt.date(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
                        sx = "F" if rng.random() < 0.5 else "M"
                        if (bd, sx, rel) not in seen:
                            seen.add((bd, sx, rel))
                            break
                    members.append({"k": nid, "emp": eid, "sub": s, "rel": rel, "birth": bd, "sex": sx,
                                    "start": MONTHS[a], "end": MONTHS[b]})
    x = {"members": members}
    _levels(x, rng)
    _claims(x, rng)
    _advisories(x)
    _rates(x, rng)
    return x


def _levels(x, rng):
    """Each employer's true expected 2027 retained PMPM, and the plan-paid scale that gives it once capped (the cap
    in 2027 dollars taken at the 2025 contract's, the trust's own convention for the truth only)."""
    samp = draw(np.random.default_rng(SEED + 100), 2_000_000)
    x["true"], x["scale"] = {}, {}
    for eid, *_ in EMPLOYERS:
        tl = BASE * float(np.exp(rng.normal(0, SD) - SD * SD / 2))
        if eid in SHIFT:
            tl = BASE * (1 + SHIFT[eid])
        lo, hi = 1000.0, 20000.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if np.minimum(samp * mid, SPECIFIC * TR[2025]).mean() < tl * 12:
                lo = mid
            else:
                hi = mid
        x["true"][eid] = tl
        x["scale"][eid] = (lo + hi) / 2


def _claims(x, rng):
    """Each member's plan-paid claims by month of service: a member-year's claims at the employer's scale in the year's
    dollars, spread over the months enrolled."""
    claims = {}
    for eid, *_ in EMPLOYERS:
        mem = [m for m in x["members"] if m["emp"] == eid]
        for y in YEARS + (2026,):
            months = [ym for ym in MONTHS if ym[0] == y]
            dol = x["scale"][eid] / ((1 + TREND) ** (2027 - y))
            amt = draw(rng, len(mem)) * dol
            for m, a in zip(mem, amt):
                cov = [ym for ym in months if m["start"] <= ym <= m["end"]]
                if not cov or a <= 0:
                    continue
                a = a * len(cov) / 12
                w = rng.dirichlet(np.ones(len(cov)) * 0.5)
                for ym, s in zip(cov, w):
                    claims[(m["k"], ym)] = round(a * s, 2)
    x["claims"] = claims
    by_m = {}
    for (k, ym), v in claims.items():
        by_m[(k, ym[0])] = by_m.get((k, ym[0]), 0.0) + v
    x["member_year"] = by_m


def member_months(x, eid, months):
    ms = set(months)
    return sum(1 for m in x["members"] if m["emp"] == eid for ym in ms if m["start"] <= ym <= m["end"])


def experience(x):
    """Per employer and plan year: member months, plan-paid claims, specific reimbursements (each member's claims in the
    contract year over $150,000), retained claims; and the retained PMPM trended to 2027."""
    emp_of = {m["k"]: m["emp"] for m in x["members"]}
    out = {}
    for eid in IDS:
        for y in YEARS:
            out[(eid, y)] = {"mm": member_months(x, eid, [ym for ym in MONTHS if ym[0] == y]), "paid": 0.0,
                             "reimb": 0.0}
    for (k, y), v in x["member_year"].items():
        if y in YEARS:
            o = out[(emp_of[k], y)]
            o["paid"] += v
            o["reimb"] += max(0.0, v - SPECIFIC)
    for (eid, y), o in out.items():
        o["ret"] = o["paid"] - o["reimb"]
        o["x"] = o["ret"] * TR[y] / o["mm"]
    return out


def credibility(ex, form="buhlmann_straub", n_full=2000, years=YEARS):
    """Each employer's expected 2027 retained PMPM under a credibility form, the trust's level the complement."""
    X = np.array([[ex[(e, y)]["x"] for y in years] for e in IDS])
    W = np.array([[ex[(e, y)]["mm"] for y in years] for e in IDS], float)
    wi = W.sum(1)
    xi = (W * X).sum(1) / wi
    xbar = (wi * xi).sum() / wi.sum()
    r, t = X.shape
    epv = (W * (X - xi[:, None]) ** 2).sum() / (r * (t - 1))
    vhm = ((wi * (xi - xbar) ** 2).sum() - (r - 1) * epv) / (wi.sum() - (wi ** 2).sum() / wi.sum())
    if form == "limited_fluctuation":
        z = np.minimum(1.0, np.sqrt(wi / len(years) / 12 / n_full))
    else:
        z = wi / (wi + epv / vhm)
    if form == "complement_simple_mean":
        xbar = float(xi.mean())
    est = xbar + z * (xi - xbar)
    return ({e: float(v) for e, v in zip(IDS, est)}, {e: float(v) for e, v in zip(IDS, z)}, float(xbar),
            float(epv / vhm))


def forms(ex):
    out = {"buhlmann_straub": credibility(ex)[0], "complement_simple_mean": credibility(ex, "complement_simple_mean")[0]}
    for n in (1000, 2000, 3000):
        out["limited_fluctuation_%d" % n] = credibility(ex, "limited_fluctuation", n)[0]
    return out


def routes(ex):
    """The easy routes: each employer's own 2023 to 2025 experience trended, and its 2025 alone."""
    own, last = {}, {}
    for e in IDS:
        mm = sum(ex[(e, y)]["mm"] for y in YEARS)
        own[e] = sum(ex[(e, y)]["x"] * ex[(e, y)]["mm"] for y in YEARS) / mm
        last[e] = ex[(e, 2025)]["x"]
    return {"own_experience": own, "own_2025": last}


def _rates(x, rng):
    """The claims component of the 2027 contribution each employer elected in September 2026, placed against the
    estimates so each employer sits where it is meant to, at least 2.5 per cent from every value it must clear:
    'golden' over on every credibility form and under on both easy routes, 'default' the reverse; 'credible_over' over
    on every credibility form and the easy routes and under at the trust's level, 'credible_under' the reverse; 'both'
    over on all, 'under' under on all."""
    ex = experience(x)
    fm = forms(ex)
    rt = routes(ex)
    c = credibility(ex)
    z = c[1]
    trust = [c[2], credibility(ex, "complement_simple_mean")[2]]
    rates, place = {}, {}
    for e in IDS:
        s = [fm[f][e] for f in fm]
        d = [rt[r][e] for r in rt]
        slo, shi, dlo, dhi = min(s), max(s), min(d), max(d)
        tlo, thi = min(trust), max(trust)

        def between(lo, hi):
            return lo * 1.025 + (hi / 1.025 - lo * 1.025) * float(rng.uniform(0.35, 0.65))
        if dlo / shi > 1.06:
            p, r = "default", between(shi, dlo)
        elif slo / dhi > 1.06:
            p, r = "golden", between(dhi, slo)
        elif z[e] >= 0.55 and min(slo, dlo) / thi > 1.05:
            p, r = "credible_over", between(thi, min(slo, dlo))
        elif z[e] >= 0.55 and tlo / max(shi, dhi) > 1.05:
            p, r = "credible_under", between(max(shi, dhi), tlo)
        elif z[e] >= 0.55 and rng.random() < 0.35:
            p, r = "both", min(slo, dlo, tlo) / float(rng.uniform(1.035, 1.06))
        else:
            p, r = "under", max(shi, dhi, thi) * float(rng.uniform(1.035, 1.07))
        rates[e], place[e] = round(r, 2), p
    x["rates"], x["place"] = rates, place


def _advisories(x):
    """Members on Hallam's 2026 high-cost claimant report: 2026 claims to date of $25,000 or more, enrolled all of
    2026 to date."""
    tot = {}
    for (k, ym), v in x["claims"].items():
        if ym[0] == 2026:
            tot[k] = tot.get(k, 0.0) + v
    x["big26"] = {}
    for m in x["members"]:
        if tot.get(m["k"], 0.0) >= HCC and m["start"] <= (2026, 1) and m["end"] == (2026, 9):
            x["big26"].setdefault(m["emp"], []).append(m)


def month_end(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])
