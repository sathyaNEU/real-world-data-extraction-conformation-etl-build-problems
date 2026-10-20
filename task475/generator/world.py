"""The Corran Valley world before any file is written: a state's credit claimants on the tax-year 2022 and 2023
schedules, placed in ZIP codes whose residential addresses straddle county lines; the IRS's ZIP-code publication and
the Department of Revenue's statewide statistics cut from them; the council's fourteen member counties; and the
program's 2023 to 2026 weatherization jobs, their status history and the grants ledger that paid for them."""
import datetime as dt

import numpy as np

SEED = 4750
FUND = 20_000_000
CAP = 0.12
TAX_YEAR = 2023
STATE_FIPS = "57"

# federal earned income credit, by number of qualifying children: phase-in rate, maximum credit, phase-out start
# (single, joint), phase-out rate (Rev. Proc. 2021-45 for 2022, Rev. Proc. 2022-38 for 2023)
SCHED = {2022: {0: (0.0765, 560, 9160, 15290, 0.0765), 1: (0.34, 3733, 20130, 26260, 0.1598),
                2: (0.40, 6164, 20130, 26260, 0.2106), 3: (0.45, 6935, 20130, 26260, 0.2106)},
         2023: {0: (0.0765, 600, 9800, 16370, 0.0765), 1: (0.34, 3995, 21560, 28120, 0.1598),
                2: (0.40, 6604, 21560, 28120, 0.2106), 3: (0.45, 7430, 21560, 28120, 0.2106)}}
AGI_EDGES = [1, 25000, 50000, 75000, 100000, 200000]          # IRS ZIP-code classes 1 to 6
DOR_EDGES = [0, 10000, 20000, 25000, 50000, 75000]             # the Department's classes 1 to 6

# member counties: FIPS, name, the agency serving it, the county's profile (credit claims, childless share among
# claimants drawn, income scale, joint share of families)
MEMBERS = [
    ("57005", "Tallis", "THCA", 14587, 0.615, 0.955, 0.23),
    ("57011", "Hesketh", "THCA", 5483, 0.318, 1.015, 0.39),
    ("57013", "Brenmoor", "NCCS", 7926, 0.296, 0.982, 0.41),
    ("57019", "Quarrow", "NCCS", 4163, 0.344, 1.046, 0.36),
    ("57023", "Varden", "NCCS", 6151, 0.287, 0.968, 0.44),
    ("57029", "Fennick", "UCAP", 8238, 0.372, 0.993, 0.33),
    ("57031", "Kerrow", "UCAP", 3644, 0.268, 1.034, 0.42),
    ("57037", "Stanwick", "UCAP", 5953, 0.351, 0.951, 0.35),
    ("57041", "Wexley", "EHCA", 6879, 0.305, 1.058, 0.38),
    ("57043", "Hollin", "EHCA", 4967, 0.383, 0.977, 0.31),
    ("57047", "Esker", "EHCA", 3274, 0.276, 1.009, 0.45),
    ("57053", "Ardley", "SCCA", 7406, 0.329, 0.963, 0.37),
    ("57059", "Silbury", "SCCA", 4589, 0.362, 1.024, 0.34),
    ("57061", "Ravell", "SCCA", 3836, 0.291, 0.988, 0.43),
]
FIPS = [m[0] for m in MEMBERS]
NAME = {m[0]: m[1] for m in MEMBERS}
SEAT = "57005"


def credit(year, agi, kids, mfj):
    P = np.array([SCHED[year][k] for k in range(4)], float)
    r, mx, s1, s2, pr = (P[kids, j] for j in range(5))
    start = np.where(mfj, s2, s1)
    full = np.minimum(r * agi, mx)
    return np.maximum(0.0, np.minimum(full, mx - pr * np.maximum(agi - start, 0.0))).round(0)


def agi_class(a):
    return np.searchsorted(AGI_EDGES, a, side="right")


def dor_class(a):
    return np.searchsorted(DOR_EDGES, a, side="right")


# ---------------------------------------------------------------------------------------------- geography
def counties(rng):
    """Every county of the state: the fourteen members and the rest, each with returns and a credit profile."""
    used = set(FIPS)
    others = [("57%03d" % k) for k in range(1, 120, 2) if ("57%03d" % k) not in used][:46]
    out = []
    for f, nm, ag, claims, cl, sc, mj in MEMBERS:
        rate = 0.226 if f == SEAT else float(rng.uniform(0.17, 0.215))
        out.append(dict(fips=f, member=True, claims=claims, childless=cl, scale=sc, mfj=mj,
                        returns=int(round(claims / rate)), mix=rng.dirichlet([6, 5, 3])))
    for f in others:
        claims = int(rng.integers(1500, 12500))
        rate = float(rng.uniform(0.15, 0.23))
        out.append(dict(fips=f, member=False, claims=claims, childless=float(rng.uniform(0.27, 0.41)),
                        scale=float(rng.uniform(0.93, 1.07)), mfj=float(rng.uniform(0.3, 0.46)),
                        returns=int(round(claims / rate)), mix=rng.dirichlet([6, 5, 3])))
    return out


def zip_codes(rng, cty):
    """ZIP codes and their parts: each county holds its own ZIP codes, some of which reach into a neighbouring
    county; a few P.O. Box ZIP codes serve a town's box holders; a few ZIP codes hold too few returns to publish."""
    zips, parts = [], []
    code = 58010
    order = sorted(cty, key=lambda c: c["fips"])
    for ci, c in enumerate(order):
        nz = 26 if c["fips"] == SEAT else int(rng.integers(7, 15))
        w = rng.dirichlet(np.ones(nz) * 1.6)
        for j in range(nz):
            code += int(rng.integers(1, 9))
            z = dict(zip="%05d" % code, home=c["fips"], kind="standard")
            zips.append(z)
            parts.append(dict(zip=z["zip"], fips=c["fips"], w=float(w[j]), home=True))
    # straddling ZIP codes: a part in a neighbouring county (neighbours by FIPS order), residents of that county
    for zi in rng.choice(len(zips), 70, replace=False):
        z = zips[zi]
        k = [c["fips"] for c in order].index(z["home"])
        nb = order[(k + (1 if rng.random() < 0.5 else -1)) % len(order)]["fips"]
        parts.append(dict(zip=z["zip"], fips=nb, w=float(rng.uniform(0.02, 0.09)), home=False))
    # P.O. Box ZIP codes: a town's boxes, held by residents of the county and of its neighbour
    for fips in (FIPS[3], FIPS[9], order[20]["fips"], order[41]["fips"]):
        code += int(rng.integers(1, 9))
        zips.append(dict(zip="%05d" % code, home=fips, kind="pobox"))
        parts.append(dict(zip="%05d" % code, fips=fips, w=0.035, home=True))
    # ZIP codes with fewer than a hundred returns
    for fips in (FIPS[6], FIPS[12], order[30]["fips"], order[50]["fips"], order[55]["fips"], order[17]["fips"]):
        code += int(rng.integers(1, 9))
        zips.append(dict(zip="%05d" % code, home=fips, kind="small"))
        parts.append(dict(zip="%05d" % code, fips=fips, w=0.0, home=True, fixed=int(rng.integers(55, 96))))
    return zips, parts


# ---------------------------------------------------------------------------------------------- the tax world
def claimants(rng, year, c, n):
    """n credit claimants of one county on one year's schedule: kind, filing status, AGI and credit."""
    out = []
    got = 0
    while got < n:
        m = 6000
        kids = np.where(rng.random(m) < c["childless"], 0, rng.choice([1, 2, 3], m, p=c["mix"]))
        mfj = rng.random(m) < np.where(kids == 0, 0.07, c["mfj"])
        base = np.where(kids == 0, rng.gamma(2.3, 4100 * c["scale"], m), rng.gamma(2.7, 9600 * c["scale"], m))
        agi = np.maximum(np.round(base, 0), 400.0)
        cr = credit(year, agi, kids, mfj)
        keep = cr > 0
        out.append(np.column_stack([kids[keep], mfj[keep], agi[keep], cr[keep]]))
        got += int(keep.sum())
    return np.vstack(out)[:n]


def other_returns(rng, c, n):
    """AGI of the county's returns that claim no credit."""
    med = 52000 * c["scale"]
    return np.maximum(np.round(rng.lognormal(np.log(med), 0.85, n), 0), 1.0)


def tax_year(rng, year, cty, zips, parts, shrink=1.0):
    """Every return of the year placed in a ZIP-code part: credit claimants as rows (zip, fips, kids, mfj, agi,
    credit) and the rest as AGI only; the IRS's ZIP x class cells cut from them."""
    by_fips = {}
    for p in parts:
        by_fips.setdefault(p["fips"], []).append(p)
    cl_rows, ot_rows = [], []
    for c in cty:
        n = int(round(c["claims"] * shrink))
        no = int(round((c["returns"] - c["claims"]) * shrink))
        ps = [p for p in by_fips[c["fips"]] if not p.get("fixed")]
        w = np.array([p["w"] for p in ps]); w = w / w.sum()
        # the county's ZIP parts carry slightly different mixes of claimants
        tilt = rng.normal(0, 0.025, len(ps))
        cc = dict(c)
        rows = []
        idx = rng.choice(len(ps), n, p=w)
        for j, p in enumerate(ps):
            k = int((idx == j).sum())
            if not k:
                continue
            cc["childless"] = float(np.clip(c["childless"] + tilt[j], 0.12, 0.88))
            r = claimants(rng, year, cc, k)
            rows.append((p["zip"], c["fips"], r))
        for z, f, r in rows:
            for kids, mfj, agi, cr in r:
                cl_rows.append((z, f, int(kids), int(mfj), float(agi), float(cr)))
        oi = rng.choice(len(ps), no, p=w)
        oa = other_returns(rng, c, no)
        for j, p in enumerate(ps):
            for a in oa[oi == j]:
                ot_rows.append((p["zip"], c["fips"], float(a)))
        # the county's share of each small ZIP code: a fixed handful of returns
        for p in by_fips[c["fips"]]:
            if p.get("fixed"):
                k = int(round(p["fixed"] * shrink))
                kc = max(6, int(round(k * c["claims"] / c["returns"])))
                r = claimants(rng, year, c, kc)
                for kids, mfj, agi, cr in r:
                    cl_rows.append((p["zip"], c["fips"], int(kids), int(mfj), float(agi), float(cr)))
                for a in other_returns(rng, c, k - kc):
                    ot_rows.append((p["zip"], c["fips"], float(a)))
    cl = np.array(cl_rows, dtype=object)
    return dict(year=year, claim=cl, other=ot_rows)


def irs_cells(ty):
    """The IRS publication of one tax year: for each ZIP code with a hundred returns or more, six AGI classes of
    returns, AGI ($ thousands), credit claims and credit amount ($ thousands); the other ZIP codes summed into
    99999; the state into 00000."""
    cl, ot = ty["claim"], ty["other"]
    n1, agi, ec, ea = {}, {}, {}, {}
    for z, f, kids, mfj, a, cr in cl:
        k = (z, int(agi_class(a)))
        n1[k] = n1.get(k, 0) + 1
        agi[k] = agi.get(k, 0.0) + a
        ec[k] = ec.get(k, 0) + 1
        ea[k] = ea.get(k, 0.0) + cr
    for z, f, a in ot:
        k = (z, int(agi_class(a)))
        n1[k] = n1.get(k, 0) + 1
        agi[k] = agi.get(k, 0.0) + a
    zips = sorted({z for z, _ in n1})
    tot = {z: sum(n1.get((z, s), 0) for s in range(1, 7)) for z in zips}
    pub = {}
    other = {s: [0, 0.0, 0, 0.0] for s in range(1, 7)}
    state = {s: [0, 0.0, 0, 0.0] for s in range(1, 7)}
    for z in zips:
        for s in range(1, 7):
            v = [n1.get((z, s), 0), agi.get((z, s), 0.0), ec.get((z, s), 0), ea.get((z, s), 0.0)]
            for i in range(4):
                state[s][i] += v[i]
            if tot[z] < 100:
                for i in range(4):
                    other[s][i] += v[i]
            else:
                pub[(z, s)] = v
    def fmt(v):
        return (int(v[0]), int(round(v[1] / 1000.0)), int(v[2]), int(round(v[3] / 1000.0)))
    out = {k: fmt(v) for k, v in pub.items()}
    for s in range(1, 7):
        out[("99999", s)] = fmt(other[s])
        out[("00000", s)] = fmt(state[s])
    return out


def dor_table(ty):
    """The Department's statewide statistics: credit claims and amount ($ thousands) by the Department's AGI class
    and number of qualifying children (0, 1, 2, 3 or more)."""
    out = {}
    for z, f, kids, mfj, a, cr in ty["claim"]:
        k = (int(dor_class(a)), int(kids))
        n, s = out.get(k, (0, 0.0))
        out[k] = (n + 1, s + cr)
    return {k: (n, int(round(s / 1000.0))) for k, (n, s) in out.items()}


# ---------------------------------------------------------------------------------------------- the relationship file
def relationship(rng, zips, parts, ty):
    """Residential, business and other (P.O. Box) addresses of each ZIP code in each county, 2023 fourth quarter,
    and the ratios the relationship file prints."""
    returns = {}
    for z, f, kids, mfj, a, cr in ty["claim"]:
        returns[(z, f)] = returns.get((z, f), 0) + 1
    for z, f, a in ty["other"]:
        returns[(z, f)] = returns.get((z, f), 0) + 1
    kind = {z["zip"]: z["kind"] for z in zips}
    addr = {}
    for (z, f), n in sorted(returns.items()):
        if kind[z] == "pobox":
            addr[(z, f)] = [0, 0, 0]
            continue
        res = int(round(n * rng.uniform(1.04, 1.22)))
        bus = int(round(res * rng.uniform(0.03, 0.11)))
        oth = int(round(res * rng.uniform(0.0, 0.05)))
        addr[(z, f)] = [res, bus, oth]
    for z in zips:
        if z["kind"] == "pobox":
            boxes = int(rng.integers(380, 1400))
            addr[(z["zip"], z["home"])] = [0, 0, boxes]
    rows = []
    for zc in sorted({z for z, _ in addr}):
        ks = sorted(f for z, f in addr if z == zc)
        tot = [sum(addr[(zc, f)][i] for f in ks) for i in range(3)]
        for f in ks:
            a = addr[(zc, f)]
            ratio = [round(a[i] / tot[i], 6) if tot[i] else 0.0 for i in range(3)]
            all_ = round(sum(a) / sum(tot), 6) if sum(tot) else 0.0
            rows.append(dict(zip=zc, fips=f, res=ratio[0], bus=ratio[1], oth=ratio[2], tot=all_, addr=a))
    return rows


# ---------------------------------------------------------------------------------------------- routes to the families
def residence_shares(rel, ratio="res"):
    """ZIP code -> {county: share}: the policy's residential ratio, a ZIP code with no residential addresses by its
    total ratio."""
    out = {}
    for r in rel:
        out.setdefault(r["zip"], {})[r["fips"]] = r
    sh = {}
    for z, d in out.items():
        res_tot = sum(v["res"] for v in d.values())
        key = ratio if (ratio != "res" or res_tot > 0) else "tot"
        sh[z] = {f: v[key] for f, v in d.items() if v[key] > 0}
    return sh


def averages(dor):
    """The first IRS class's childless and family average credit, from the Department's table: its classes 1 to 3
    are the IRS's class 1."""
    n0 = sum(dor.get((c, 0), (0, 0))[0] for c in (1, 2, 3))
    s0 = sum(dor.get((c, 0), (0, 0))[1] for c in (1, 2, 3)) * 1000.0
    n1 = sum(dor.get((c, k), (0, 0))[0] for c in (1, 2, 3) for k in (1, 2, 3))
    s1 = sum(dor.get((c, k), (0, 0))[1] for c in (1, 2, 3) for k in (1, 2, 3)) * 1000.0
    return s0 / n0, s1 / n1, n1 / (n0 + n1)


def pooled_family_average(dor):
    n = sum(v[0] for (c, k), v in dor.items() if k > 0)
    s = sum(v[1] for (c, k), v in dor.items() if k > 0) * 1000.0
    return s / n


def families(cells, dor, sh, route="gold"):
    """Each member county's tax-year returns with qualifying children, by route:
    R0 every claim; R1 the Department's statewide share of families in the first class; R1b the decomposition with
    the family average pooled over every class; gold the decomposition by the first class's childless and family
    averages; every class above the first is all families (the Department's table shows no childless claim there)."""
    a0, a1, share = averages(dor)
    pa1 = pooled_family_average(dor)
    out = {f: 0.0 for f in FIPS}
    for (z, s), (n1, agi, ec, ea) in cells.items():
        if z in ("00000", "99999") or z not in sh:
            continue
        for f, w in sh[z].items():
            if f not in out:
                continue
            if s > 1 or route == "R0":
                out[f] += w * ec
            elif route == "R1":
                out[f] += w * ec * share
            elif route == "gold":
                out[f] += w * (ea * 1000.0 - a0 * ec) / (a1 - a0)
            elif route == "R1b":
                out[f] += w * (ea * 1000.0 - a0 * ec) / (pa1 - a0)
    return out


def allocate(counts, fund=FUND, cap=CAP):
    """The policy's allocation: shares of the fourteen counties' total; a county above the cap is held at it and the
    excess shared in proportion among the rest, repeated until none is above it; unrounded."""
    v = np.array([counts[f] for f in FIPS], float)
    out = np.zeros(len(v))
    fixed = np.zeros(len(v), bool)
    while True:
        rest = fund - out[fixed].sum()
        free = ~fixed
        out[free] = rest * v[free] / v[free].sum()
        over = free & (out > cap * fund + 1e-9)
        if not over.any():
            break
        out[over] = cap * fund
        fixed |= over
    return {f: float(x) for f, x in zip(FIPS, out)}


def capped(al, fund=FUND, cap=CAP):
    return sorted(NAME[f] for f, x in al.items() if abs(x - cap * fund) < 1e-6) or ["none"]


# ---------------------------------------------------------------------------------------------- aggregates and tuning
def raw_cells(ty):
    """Unrounded ZIP x class aggregates [returns, AGI, claims, credit] and the Department's [claims, credit] by its
    class and children, kept beside the claimant rows so a claimant's change updates both."""
    cells, dor = {}, {}
    for i, (z, f, kids, mfj, a, cr) in enumerate(ty["claim"]):
        k = (z, int(agi_class(a)))
        v = cells.setdefault(k, [0, 0.0, 0, 0.0])
        v[0] += 1; v[1] += a; v[2] += 1; v[3] += cr
        d = dor.setdefault((int(dor_class(a)), int(kids)), [0, 0.0])
        d[0] += 1; d[1] += cr
    for z, f, a in ty["other"]:
        v = cells.setdefault((z, int(agi_class(a))), [0, 0.0, 0, 0.0])
        v[0] += 1; v[1] += a
    ty["raw"], ty["raw_dor"] = cells, dor


def publish(ty):
    """The IRS cells and the Department's table from the unrounded aggregates."""
    cells = ty["raw"]
    tot = {}
    for (z, s), v in cells.items():
        tot[z] = tot.get(z, 0) + v[0]
    out = {}
    other = {s: [0, 0.0, 0, 0.0] for s in range(1, 7)}
    state = {s: [0, 0.0, 0, 0.0] for s in range(1, 7)}
    for (z, s), v in cells.items():
        for i in range(4):
            state[s][i] += v[i]
            if tot[z] < 100:
                other[s][i] += v[i]
        if tot[z] >= 100:
            out[(z, s)] = v
    for z in {z for z, _ in out}:
        for s in range(1, 7):
            out.setdefault((z, s), [0, 0.0, 0, 0.0])
    fmt = lambda v: (int(v[0]), int(round(v[1] / 1000.0)), int(v[2]), int(round(v[3] / 1000.0)))
    pub = {k: fmt(v) for k, v in out.items()}
    for s in range(1, 7):
        pub[("99999", s)] = fmt(other[s])
        pub[("00000", s)] = fmt(state[s])
    dor = {k: (int(v[0]), int(round(v[1] / 1000.0))) for k, v in ty["raw_dor"].items()}
    return pub, dor


def edge(v, unit, need):
    """Whether v sits at least need (a share of the unit) from the rounding edge of its printed cell."""
    x = v / unit
    return abs(x - np.floor(x) - 0.5) >= need


def figures_ok(fam, need_f=0.15, need_s=0.15, need_a=0.2):
    tot = sum(fam.values())
    al = allocate(fam)
    bad = []
    for f in FIPS:
        sh = 100.0 * fam[f] / tot
        if not (edge(fam[f], 0.1, need_f) and edge(sh, 0.01, need_s) and edge(al[f], 100.0, need_a)):
            bad.append(f)
    return bad


def lever(ty, rel, f, k):
    """Move the published first-class credit amount of the county's largest ZIP code wholly inside it by k thousand
    dollars, by changing the income of phase-in family claimants there (their credit is the phase-in rate times
    income), with the cell's unrounded total left at least 300 dollars from a rounding edge."""
    whole = {}
    for r in rel:
        whole.setdefault(r["zip"], []).append(r)
    inside = [z for z, rs in whole.items() if len(rs) == 1 and rs[0]["fips"] == f and rs[0]["res"] > 0]
    cells = ty["raw"]
    cand = sorted((cells[(z, 1)][2], z) for z in inside if (z, 1) in cells)
    z = cand[-1][1]
    v = cells[(z, 1)]
    target = (round(v[3] / 1000.0) + k) * 1000.0 + 0.0
    delta = target - v[3]
    cl = ty["claim"]
    rows = ty.setdefault("rows_by_zip", {})
    if not rows:
        for i in range(len(cl)):
            if cl[i][2] > 0 and agi_class(cl[i][4]) == 1:
                rows.setdefault(cl[i][0], []).append(i)
    sch = SCHED[ty["year"]]
    undo = []
    for i in rows.get(z, []):
        if abs(delta) < 1.0:
            break
        kids, mfj, a, cr = int(cl[i][2]), int(cl[i][3]), float(cl[i][4]), float(cl[i][5])
        r_, mx = sch[kids][0], sch[kids][1]
        top = mx / r_
        if a >= top - 50 or a <= 600:
            continue
        lo, hi = 600.0, top - 50.0
        new_a = float(np.clip(a + delta / r_, lo, hi))
        new_a = float(round(new_a))
        new_c = float(credit(ty["year"], np.array([new_a]), np.array([kids]), np.array([bool(mfj)]))[0])
        dc = new_c - cr
        if dc == 0:
            continue
        undo.append((i, z, a, cr))
        set_claim(ty, i, z, new_a, new_c)
        delta -= dc
    return abs(delta) < 1.0, undo


def set_claim(ty, i, z, new_a, new_c):
    """Change one claimant's income and credit, keeping the ZIP cell and the Department's cell in step."""
    cl = ty["claim"]
    kids, a, cr = int(cl[i][2]), float(cl[i][4]), float(cl[i][5])
    assert agi_class(a) == agi_class(new_a) == 1
    v = ty["raw"][(z, 1)]
    cl[i][4], cl[i][5] = new_a, new_c
    v[1] += new_a - a
    v[3] += new_c - cr
    d0 = ty["raw_dor"][(int(dor_class(a)), kids)]
    d0[0] -= 1; d0[1] -= cr
    d1 = ty["raw_dor"].setdefault((int(dor_class(new_a)), kids), [0, 0.0])
    d1[0] += 1; d1[1] += new_c


def unlever(ty, undo):
    for i, z, a, cr in reversed(undo):
        set_claim(ty, i, z, a, cr)


# ---------------------------------------------------------------------------------------------- the weatherization program
AGENCIES = {
    "THCA": ("Tallis-Hesketh Community Action", ["57005", "57011"]),
    "NCCS": ("North Corran Community Services", ["57013", "57019", "57023"]),
    "UCAP": ("Upper Corran Action Program", ["57029", "57031", "57037"]),
    "EHCA": ("Esker-Hollin Community Action", ["57041", "57043", "57047"]),
    "SCCA": ("South Corran Community Action", ["57053", "57059", "57061"]),
}
AGENCY_OF = {f: a for a, (_, fs) in AGENCIES.items() for f in fs}
START = dt.date(2023, 7, 1)
PULL = dt.date(2026, 9, 30)
MOVE = dt.date(2025, 7, 14)          # the agencies' move to the WX job system
PY = {y: (dt.date(y, 1, 1), dt.date(y, 12, 31)) for y in (2024, 2025, 2026, 2027)}   # calendar program years
ASK_YEAR = 2025
LEGACY_FIRST, NEW_FIRST = 18640, 18001
FUNDS = [("DOE-WAP", 0.52), ("STATE-WX", 0.24), ("DOE-WAP;STATE-WX", 0.09), ("UTIL-LIW", 0.09),
         ("DOE-WAP;UTIL-LIW", 0.06)]
FUEL = ["Natural gas", "Propane", "Electric", "Fuel oil", "Wood"]


def day(d, n):
    return d + dt.timedelta(days=int(n))


def tracts(rng):
    out = {}
    for f in FIPS:
        n = 31 if f == SEAT else int(rng.integers(6, 15))
        codes = sorted(rng.choice(np.arange(100, 9800), n, replace=False))
        out[f] = ["%s%06d" % (f, int(c) * (1 if c % 4 else 1)) for c in codes]
    return out


def jobs(rng):
    """Every job the agencies opened from July 2023 to the pull: the dwelling's county and tract, the building, the
    funding, and the dated life of the job (audit, start, first completion, callbacks, deferral or cancellation)."""
    tr = tracts(rng)
    rate = {f: (m[3] ** 0.82) / 15.0 for f, m in zip(FIPS, MEMBERS)}
    out = []
    d = START
    while d <= dt.date(2026, 9, 12):
        for f in FIPS:
            season = 1.0 + 0.18 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 300) / 365.0)
            n = rng.poisson(rate[f] * season / 365.0 * 7)
            for _ in range(n):
                out.append(dict(fips=f, created=day(d, rng.integers(0, 7))))
        d = day(d, 7)
    out.sort(key=lambda j: (j["created"], j["fips"]))
    for j in out:
        f = j["fips"]
        j["agency"] = AGENCY_OF[f]
        j["tract"] = tr[f][int(rng.integers(len(tr[f])))]
        u = rng.random()
        mf_bias = 0.10 if f == SEAT else 0.0
        if u < 0.66 - mf_bias:
            j["btype"], j["units"] = "SF", 1
        elif u < 0.84 - mf_bias:
            j["btype"], j["units"] = "MH", 1
        elif u < 0.94 - mf_bias / 2:
            j["btype"], j["units"] = "MF2-4", int(rng.integers(2, 5))
        else:
            j["btype"], j["units"] = "MF5+", int(rng.integers(5, 25))
        j["funding"] = FUNDS[int(rng.choice(len(FUNDS), p=[p for _, p in FUNDS]))][0]
        j["fuel"] = FUEL[int(rng.choice(5, p=[0.46, 0.21, 0.19, 0.09, 0.05]))]
        j["audit"] = day(j["created"], rng.integers(2, 24))
        u = rng.random()
        j["deferred"] = j["cancelled"] = None
        j["completions"], j["reopens"] = [], []
        if u < 0.07:
            j["deferred"] = day(j["audit"], rng.integers(1, 18))
        elif u < 0.10:
            j["cancelled"] = day(j["audit"], rng.integers(5, 60))
        else:
            mf = j["units"] > 1
            j["start"] = day(j["audit"], rng.integers(9, 62))
            done = day(j["start"], rng.integers(2, 12) + (rng.integers(10, 40) if mf else 0))
            j["completions"].append(done)
            if rng.random() < 0.085:
                ro = day(done, rng.integers(18, 115))
                j["reopens"].append(ro)
                j["completions"].append(day(ro, rng.integers(2, 26)))
        j["start"] = j.get("start")
        if j["audit"] > PULL:
            # opened in the last weeks: the audit is still to come at the pull
            j["audit"] = j["start"] = j["deferred"] = j["cancelled"] = None
            j["completions"], j["reopens"] = [], []
            continue
        last = max([x for x in [j["audit"], j["deferred"], j["cancelled"]] + j["completions"] + j["reopens"] if x])
        if last > PULL:
            # the job is still open at the pull: drop the events after it
            j["completions"] = [x for x in j["completions"] if x <= PULL]
            j["reopens"] = [x for x in j["reopens"] if x <= PULL]
            if j["start"] and j["start"] > PULL:
                j["start"] = None
            if j["deferred"] and j["deferred"] > PULL:
                j["deferred"] = None
            if j["cancelled"] and j["cancelled"] > PULL:
                j["cancelled"] = None
    # job numbers: the old system numbered every job as it was opened; the conversion loaded the old jobs in that
    # order under the new system's numbers, which then numbered new jobs in turn
    old = [j for j in out if j["created"] < MOVE]
    for k, j in enumerate(old):
        j["legacy"] = LEGACY_FIRST + k
        j["no"] = NEW_FIRST + k
    n = NEW_FIRST + len(old)
    for j in out:
        if j["created"] >= MOVE:
            j["legacy"] = None
            j["no"] = n
            n += 1
    return out, tr


def status_now(j):
    """The job's status at the pull and the date it was last marked complete."""
    if j["cancelled"]:
        return "CANCELLED", None
    if j["deferred"]:
        return "DEFERRED", None
    if j["completions"]:
        if len(j["reopens"]) > len(j["completions"]) - 1 and j["reopens"][-1] > j["completions"][-1]:
            return "REOPENED", j["completions"][-1]
        return "COMPLETED", j["completions"][-1]
    if j["start"]:
        return "IN PROGRESS", None
    if not j["audit"]:
        return "AUDIT SCHEDULED", None
    return "AUDITED", None


def program_job(j):
    return "DOE-WAP" in j["funding"] or "STATE-WX" in j["funding"]


def crossing_callbacks(rng, js):
    """Every member county needs at least one callback carrying a completion across the program year's end, as any
    county's agencies see in a year: a November or December 2025 dwelling reopened in the new year."""
    py0, py1 = PY[ASK_YEAR]
    for f in FIPS:
        def moved(j):
            if not j["completions"] or not program_job(j) or not j["reopens"]:
                return 0
            st, last = status_now(j)
            first_in = py0 <= j["completions"][0] <= py1
            last_in = st == "COMPLETED" and py0 <= last <= py1
            return int(first_in) - int(last_in)
        net = sum(moved(j) * j["units"] for j in js if j["fips"] == f)
        if net != 0:
            continue
        pool = [j for j in js if j["fips"] == f and program_job(j) and not j["reopens"] and j["completions"]
                and dt.date(2025, 11, 10) <= j["completions"][0] <= dt.date(2025, 12, 22) and j["units"] == 1]
        pool.sort(key=lambda j: j["no"])
        j = pool[int(rng.integers(len(pool)))]
        ro = day(j["completions"][0], rng.integers(24, 60))
        j["reopens"].append(ro)
        j["completions"].append(day(ro, rng.integers(3, 15)))


ACCT_TEXT = {
    "AUDIT": ["Energy audit and blower-door test", "Energy audit, combustion safety test", "Audit and testing"],
    "MATERIALS": ["Attic insulation", "Air sealing materials", "Wall insulation, dense-pack", "Duct sealing",
                  "Window repair materials", "Floor insulation", "Door weatherstripping", "Smoke and CO alarms"],
    "LABOR": ["Crew labor", "Crew labor, air sealing", "Crew labor, insulation", "Crew labor, final work"],
    "SUBCONTRACT": ["Furnace tune and repair", "Water heater replacement", "Electrical repair", "HVAC replacement"],
    "HEALTH-SAFETY": ["Health and safety repair", "Moisture repair", "Ventilation fan install"],
    "CALLBACK": ["Crew labor, return visit", "Crew labor, warranty visit"],
}


def ledger(rng, js):
    """The grants ledger: every expenditure line the council posted for its agencies' monthly invoices, July 2024
    to the pull, with the job number each invoice gave (the old system's before the move, the new system's after)
    and the agencies' administration, vehicle, training and insurance lines, which carry no job."""
    lines = []
    def add(j, acct, d, amt, fund):
        lines.append(dict(job=j, acct=acct, service=d, amount=round(float(amt), 2), fund=fund, agency=j["agency"]))
    for j in js:
        if not program_job(j):
            continue
        funds = [x for x in j["funding"].split(";") if x != "UTIL-LIW"]
        pick = lambda: funds[int(rng.integers(len(funds)))]
        u = j["units"]
        scale = u ** 0.85
        if not j["audit"]:
            continue
        add(j, "AUDIT", j["audit"], rng.uniform(380, 620) + (90 * u if u > 1 else 0), pick())
        if j["deferred"]:
            if rng.random() < 0.4:
                add(j, "HEALTH-SAFETY", j["deferred"], rng.uniform(150, 600), pick())
            continue
        if j["cancelled"] or not j["start"]:
            continue
        end = j["completions"][0] if j["completions"] else PULL
        span = max(1, (end - j["start"]).days)
        for _ in range(int(rng.integers(1, 4))):
            add(j, "MATERIALS", day(j["start"], rng.integers(0, span + 1)), rng.uniform(500, 1600) * scale, pick())
        for _ in range(int(rng.integers(2, 5))):
            add(j, "LABOR", day(j["start"], rng.integers(0, span + 1)), rng.uniform(450, 1400) * scale, pick())
        for _ in range(int(rng.choice([0, 0, 1, 1, 2]))):
            add(j, "SUBCONTRACT", day(j["start"], rng.integers(0, span + 1)), rng.uniform(600, 3200), pick())
        if rng.random() < 0.35:
            add(j, "HEALTH-SAFETY", day(j["start"], rng.integers(0, span + 1)), rng.uniform(200, 1600), pick())
        for ro, co in zip(j["reopens"], j["completions"][1:] + [None]):
            add(j, "CALLBACK", co or ro, rng.uniform(120, 950), pick())
    # the agencies' own lines
    for a in AGENCIES:
        m = dt.date(2024, 6, 1)
        while m <= dt.date(2026, 8, 1):
            fake = dict(agency=a, no=None, legacy=None)
            k = len(AGENCIES[a][1])
            for acct, lo, hi, p in (("ADMIN", 4000, 12000, 1.0), ("VEHICLE", 500, 2400, 1.0),
                                    ("TRAINING", 300, 2500, 0.35), ("INSURANCE", 900, 3100, 0.34)):
                if rng.random() < p:
                    lines.append(dict(job=fake, acct=acct, service=day(m, rng.integers(0, 27)),
                                      amount=round(float(rng.uniform(lo, hi) * (0.7 + 0.3 * k)), 2),
                                      fund="DOE-WAP" if rng.random() < 0.7 else "STATE-WX", agency=a))
            m = (m.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
    # monthly invoices: one per agency and service month, posted 12 to 38 days after the month ends
    posted = {}
    out = []
    for ln in lines:
        mon = ln["service"].replace(day=1)
        key = (ln["agency"], mon)
        if key not in posted:
            nxt = (mon.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
            posted[key] = day(nxt, rng.integers(11, 38))
        ln["posted"] = posted[key]
        ln["invoice"] = "%s-%s" % (ln["agency"], mon.strftime("%y%m"))
        if dt.date(2024, 7, 1) <= ln["posted"] <= PULL:
            # the agency prepares the month's invoice on the second of the next month, from the system it is on
            prepared = day((mon.replace(day=28) + dt.timedelta(days=5)).replace(day=1), 1)
            j = ln["job"]
            ln["job_no"] = (j["legacy"] if prepared < MOVE else j["no"]) if j.get("no") else None
            out.append(ln)
    out.sort(key=lambda r: (r["posted"], r["agency"], r["invoice"], r["service"], r["acct"]))
    return out


# ---------------------------------------------------------------------------------------------- truths for the asks
def a_truth(js, year=ASK_YEAR):
    """Dwellings the program weatherized in each member county in the program year: units of DOE or state funded
    jobs first completed in the year, placed by the dwelling's tract."""
    p0, p1 = PY[year]
    out = {f: 0 for f in FIPS}
    for j in js:
        if program_job(j) and j["completions"] and p0 <= j["completions"][0] <= p1:
            out[j["tract"][:5]] += j["units"]
    return out


def b_truth(gl, year=ASK_YEAR):
    """The program's spending on dwellings in each member county in the program year: lines posted in the year that
    carry a job, placed by the job's tract."""
    p0, p1 = PY[year]
    out = {f: 0.0 for f in FIPS}
    for ln in gl:
        if ln["job_no"] and p0 <= ln["posted"] <= p1:
            out[ln["job"]["tract"][:5]] += ln["amount"]
    return out


def tune_spending(rng, gl, need=0.15):
    """Each county's spending off the edge of its whole-dollar cell: one of its 2025 material lines is a few
    cents different."""
    for f in FIPS:
        v = b_truth(gl)[f]
        if edge(v, 1.0, need):
            continue
        frac = v - np.floor(v)
        shift = round((0.12 - frac) if frac < 0.5 else (0.88 - frac), 2)
        cand = [ln for ln in gl if ln["job_no"] and ln["job"]["tract"][:5] == f and ln["acct"] == "MATERIALS"
                and PY[ASK_YEAR][0] <= ln["posted"] <= dt.date(2025, 12, 20)]
        cand.sort(key=lambda ln: (ln["posted"], ln["amount"]))
        cand[0]["amount"] = round(cand[0]["amount"] + shift, 2)
        assert edge(b_truth(gl)[f], 1.0, need), (f, b_truth(gl)[f])


def tune_dwellings(js):
    """No two member counties weatherize the same number of dwellings in the year: a tied county's small
    multifamily job, one never reopened, covers one more unit."""
    for _ in range(20):
        a = a_truth(js)
        seen, tie = {}, None
        for f in FIPS:
            if a[f] in seen:
                tie = f
                break
            seen[a[f]] = f
        if tie is None:
            return
        p0, p1 = PY[ASK_YEAR]
        cand = [j for j in js if j["tract"][:5] == tie and program_job(j) and j["btype"] == "MF2-4" and j["units"] < 4
                and not j["reopens"] and j["completions"] and p0 <= j["completions"][0] <= p1]
        cand.sort(key=lambda j: j["no"])
        cand[0]["units"] += 1
    raise AssertionError("dwelling ties not cleared")


def labels(rng, js):
    """The funding code each job record shows. The old system held one code per job: a job the grant shared with the
    State fund shows the grant, and a job the grant shared with the utility's program shows whichever code the
    intake worker entered, often the utility's, which had referred the household. The WX job system lists every
    source of the jobs opened in it."""
    for j in sorted(js, key=lambda j: j["no"]):
        f = j["funding"]
        if j["legacy"] and f == "DOE-WAP;UTIL-LIW":
            j["label"] = "UTIL-LIW" if rng.random() < 0.6 else "DOE-WAP"
        elif j["legacy"] and f == "DOE-WAP;STATE-WX":
            j["label"] = "DOE-WAP"
        else:
            j["label"] = f


def hidden_program_jobs(js):
    """Every member county has at least one dwelling the program paid for, first completed in the year, whose old
    record shows only the utility's code."""
    p0, p1 = PY[ASK_YEAR]
    for f in FIPS:
        def mine(j):
            return (j["tract"][:5] == f and j["legacy"] and j["completions"] and p0 <= j["completions"][0] <= p1)
        if any(mine(j) and program_job(j) and j["label"] == "UTIL-LIW" for j in js):
            continue
        cand = sorted((j for j in js if mine(j) and j["funding"] == "DOE-WAP" and j["units"] == 1
                       and not j["reopens"]), key=lambda j: j["no"])
        j = cand[len(cand) // 2]
        j["funding"], j["label"] = "DOE-WAP;UTIL-LIW", "UTIL-LIW"


# ---------------------------------------------------------------------------------------------- the whole world
def build(seed=SEED):
    rng = np.random.default_rng(seed)
    cty = counties(rng)
    zips, parts = zip_codes(rng, cty)
    ty = tax_year(rng, 2023, cty, zips, parts)
    ty22 = tax_year(rng, 2022, cty, zips, parts, shrink=0.972)
    rel = relationship(rng, zips, parts, ty)
    raw_cells(ty)
    raw_cells(ty22)
    sh = residence_shares(rel)
    # edges: move each failing county's published first-class amount by whole thousands
    trng = np.random.default_rng(seed + 31)
    for it in range(40):
        pub, dor = publish(ty)
        bad = figures_ok(families(pub, dor, sh, "gold"))
        if not bad:
            break
        f = bad[int(trng.integers(len(bad)))]
        best = None
        for k in range(-8, 9):
            if k == 0:
                continue
            ok, undo = lever(ty, rel, f, k)
            if ok:
                pub, dor = publish(ty)
                still = figures_ok(families(pub, dor, sh, "gold"))
                score = (f in still, len(still), abs(k))
                if best is None or score < best[0]:
                    best = (score, k)
            unlever(ty, undo)
        if best:
            lever(ty, rel, f, best[1])
    assert not figures_ok(families(*publish(ty), sh, "gold")), "edges not cleared"
    pub, dor = publish(ty)
    pub22, dor22 = publish(ty22)
    orng = np.random.default_rng(seed + 900)
    js, tr = jobs(orng)
    crossing_callbacks(orng, js)
    tune_dwellings(js)
    labels(np.random.default_rng(seed + 905), js)
    hidden_program_jobs(js)
    gl = ledger(np.random.default_rng(seed + 901), js)
    tune_spending(np.random.default_rng(seed + 902), gl)
    return dict(cty=cty, zips=zips, parts=parts, ty=ty, ty22=ty22, rel=rel, sh=sh, pub=pub, dor=dor, pub22=pub22,
                dor22=dor22, jobs=js, tracts=tr, ledger=gl)
