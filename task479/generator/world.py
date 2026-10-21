"""The world of task479 (architecture 3): Marlowe Benefit Administrators, a third-party administrator of sixteen
self-funded employer health plans, each with specific stop-loss from Arbor Ridge Specialty Insurance Company at a
$250,000 attachment that the 2027 policies keep.

A group's retained claims are its members' claims, each member's year kept below the attachment. Medical trend acts on
claims, so a member already over the attachment costs the plan the attachment in 2027 whatever the trend: the groups
whose 2025 experience carries several members at or near the attachment retain less in 2027 than their 2025 retained
claims trended.

    x = build()    the truth: groups, members, enrollment, 2025 and 2026 claims, the carrier's records, the rates"""
import calendar
import datetime as dt

import numpy as np

SEED = 4793
ATTACH = 250_000
TREND = 0.075
F = (1 + TREND) ** 2              # 2025 to 2027
ADVISORY = 125_000                # the carrier's 50 per cent advisory threshold

# group no, employer, industry, members, ordinary claims scale, members over the attachment (2025 claims), members
# just under it, the 2027 claims funding rate's place: "both" over on the golden and the default, "default" over on
# the default only, "partial" over only when the crossers are left uncapped, "neither"
GROUPS = [
    ("G1041", "Halsted Tool & Die", "manufacturing", 640, 1.00, [312, 488], [231], "neither"),
    ("G1052", "Ferris Valley Credit Union", "finance", 410, 0.92, [], [], "both"),
    ("G1063", "Oakmont Senior Living", "health care", 620, 1.10, [276, 351, 402, 655, 298, 510], [228, 244], "default"),
    ("G1074", "Grafton Freight Lines", "transportation", 480, 1.06, [298, 541, 1220, 330], [236], "default"),
    ("G1085", "Kittredge Foods", "food processing", 1520, 0.98, [263, 330], [219], "neither"),
    ("G1096", "Ashbury Engineering Group", "professional services", 330, 0.88, [702, 265, 410], [240], "default"),
    ("G1107", "Linden Park Schools Foundation", "education", 520, 0.95, [], [241], "neither"),
    ("G1118", "Pemberton Hardware Cooperative", "retail", 940, 1.02, [287], [], "both"),
    ("G1129", "Sorrel Creek Dental Partners", "health care", 270, 0.90, [], [], "neither"),
    ("G1130", "Northfield Paperboard", "manufacturing", 760, 1.08, [305, 377, 468, 590, 812, 290, 355], [227, 239, 246], "default"),
    ("G1141", "Calloway & Reese LLP", "professional services", 380, 0.86, [356], [], "neither"),
    ("G1152", "Brightwell Plumbing & Heating", "construction", 450, 1.04, [], [233, 247, 238, 229, 244], "partial"),
    ("G1163", "Tamarack Hotel Group", "hospitality", 990, 1.00, [258, 449], [], "both"),
    ("G1174", "Wexford County Mutual", "insurance", 420, 0.94, [520, 610, 280, 330], [222], "default"),
    ("G1185", "Delacorte Printing", "manufacturing", 300, 1.05, [], [], "neither"),
    ("G1196", "Quarry Hill Builders", "construction", 580, 1.07, [383], [230, 243], "neither"),
]
NAMES = [g[0] for g in GROUPS]
MONTHS25 = [(2025, m) for m in range(1, 13)]
MONTHS26 = [(2026, m) for m in range(1, 9)]


def build():
    rng = np.random.default_rng(SEED)
    members, mm = [], {}
    nid = 0
    for gno, emp, ind, n, scale, over, near, place in GROUPS:
        g_members = []
        seen = set()
        # subscribers and dependants: about 1.9 members per subscriber
        sub = 0
        while len(g_members) < n:
            sub += 1
            fam = 1 + int(rng.choice([0, 0, 1, 1, 2, 3], p=[0.32, 0.12, 0.2, 0.12, 0.14, 0.10]))
            byear = int(rng.integers(1961, 2003))
            for k in range(fam):
                nid += 1
                rel = "EE" if k == 0 else ("SP" if k == 1 else "CH")
                by = byear if k == 0 else (byear + int(rng.integers(-4, 5)) if rel == "SP" else int(rng.integers(2005, 2025)))
                while True:
                    bd = dt.date(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
                    sx = "F" if rng.random() < 0.5 else "M"
                    if (bd, sx, rel) not in seen:
                        seen.add((bd, sx, rel))
                        break
                g_members.append({"k": nid, "group": gno, "sub": sub, "rel": rel, "birth": bd, "sex": sx})
        # enrollment: most members all year; some add or term in 2025 and 2026
        for m in g_members:
            start = (2025, 1) if rng.random() < 0.9 else (2025, int(rng.integers(2, 13)))
            end = (2026, 8) if rng.random() < 0.88 else ((2025, int(rng.integers(3, 13))) if rng.random() < 0.5
                                                          else (2026, int(rng.integers(1, 9))))
            if end < start:
                end = (2026, 8)
            m["start"], m["end"] = start, end
        members += g_members
    # 2025 claims per member: ordinary members from a heavy-tailed draw, the designed large claimants placed on
    # members enrolled all of 2025
    for gno, emp, ind, n, scale, over, near, place in GROUPS:
        gm = [m for m in members if m["group"] == gno]
        for m in gm:
            months = sum(1 for ym in MONTHS25 if m["start"] <= ym <= m["end"])
            base = float(rng.lognormal(7.75, 1.42)) * scale * months / 12
            if rng.random() < 0.13:
                base = 0.0
            m["c25"] = min(base, 92_000.0)
            m["c26"] = min(float(rng.lognormal(7.75, 1.42)) * scale * 8 / 12 * 1.075, 92_000.0)
        full = [m for m in gm if m["start"] == (2025, 1) and m["end"] == (2026, 8)]
        pick = rng.permutation(len(full))
        j = 0
        for amt in over + near:
            mbr = full[pick[j]]
            j += 1
            mbr["c25"] = amt * 1000 + float(rng.integers(0, 999))
        # a few members between $100,000 and the near band, who stay under the attachment after trend
        for _ in range(int(rng.integers(1, 4))):
            mbr = full[pick[j]]
            j += 1
            mbr["c25"] = float(rng.integers(101_000, 190_000))
        # 2026 large claims to date (the carrier's advisories)
        for _ in range(int(rng.integers(2, 5))):
            mbr = full[pick[j]]
            j += 1
            mbr["c26"] = float(rng.integers(126_000, 420_000))
    for m in members:
        m["rx25"] = round(m["c25"] * float(rng.uniform(0.08, 0.35)), 2) if m["c25"] else 0.0
        m["med25"] = round(m["c25"] - m["rx25"], 2)
        m["c25"] = round(m["med25"] + m["rx25"], 2)
    x = {"members": members}
    _rates(x, rng)
    return x


def member_months(members, gno, months):
    return sum(1 for m in members if m["group"] == gno for ym in months if m["start"] <= ym <= m["end"])


def group_figures(x):
    """Per group: 2025 member months, gross, reimbursed (excess over the attachment), retained; and the 2027 PMPM
    under the golden (each member trended, then capped), the default (retained trended), the partial fix (members
    already over the attachment held at it, the rest trended uncapped) and gross trended."""
    out = {}
    for gno, *_ in GROUPS:
        gm = [m for m in x["members"] if m["group"] == gno]
        mm = member_months(x["members"], gno, MONTHS25)
        c = np.array([m["c25"] for m in gm])
        gross = c.sum()
        reimb = np.maximum(c - ATTACH, 0).sum()
        ret = gross - reimb
        golden = np.minimum(c * F, ATTACH).sum()
        partial = np.where(c >= ATTACH, ATTACH, c * F).sum()
        out[gno] = {"mm": mm, "gross": gross, "reimb": reimb, "ret": ret, "pm_ret25": ret / mm,
                    "golden": golden / mm, "default": F * ret / mm, "partial": partial / mm, "gross27": F * gross / mm}
    return out


def _rates(x, rng):
    """The 2027 claims funding rates the employers elected in September, placed against the estimates so each group
    sits where GROUPS puts it, at least 1.2 per cent from every route it must clear and short of."""
    fig = group_figures(x)
    rates = {}
    for gno, emp, ind, n, scale, over, near, place in GROUPS:
        f = fig[gno]
        g, d, p = f["golden"], f["default"], f["partial"]
        if place == "both":
            r = g / float(rng.uniform(1.025, 1.04))
        elif place == "default":
            lo, hi = g * 1.012, d / 1.012
            assert lo < hi, (gno, g, d)
            r = lo + (hi - lo) * float(rng.uniform(0.35, 0.65))
        elif place == "partial":
            lo, hi = g * 1.006, p / 1.006
            assert lo < hi, (gno, g, p)
            r = (lo + hi) / 2
        else:
            r = d * float(rng.uniform(1.03, 1.06))
        rates[gno] = round(r, 2)
    x["rates"] = rates


def month_end(y, m):
    return dt.date(y, m, calendar.monthrange(y, m)[1])
