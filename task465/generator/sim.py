"""The random world of task465: the territory's households by county and income band, the two state surveys' microdata,
Callowmere's 2025 screening pilot, the household estimates as the demographer publishes them, and the centring that
keeps every graded figure mid-bin. Seeded and deterministic."""
import math

import numpy as np

import world as W

SEED = 148
PILOT_DRAW = 1243                             # the pilot's own draw (its two divisions' tables agree within sampling error)
PSI = 3.3                                  # within-band odds ratio between high burden and medical equipment
PB = (0.56, 0.24, 0.09, 0.028)             # high-burden share by band before each division's multiplier
QB = (0.050, 0.036, 0.020, 0.013)          # equipment share by band before each division's multiplier
NA, NB = 9000, 12000                       # completed households in the energy survey and the health survey
PILOT_SAMPLED = 10800                      # addresses mailed in each pilot division
ADULT_SLOPE = 0.10                         # equipment rises gently with the number of adults in the home


def joint(p, q, psi):
    """The share with both traits in a 2x2 table with margins p and q and odds ratio psi."""
    if abs(psi - 1) < 1e-12:
        return p * q
    a = psi - 1
    b = -(1 + (psi - 1) * (p + q))
    c = psi * p * q
    return (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)


def population(rng):
    """County by band cells: households before publication, high-burden share p, equipment share q, joint share j."""
    cells = []
    for name, pm, qm, nk, counties, inc in W.DIVISIONS:
        w = rng.dirichlet(np.ones(len(counties)) * 6)
        for k, c in enumerate(counties):
            for b in range(4):
                n = nk * 1000.0 * w[k] * inc[b]
                p = min(PB[b] * pm * rng.lognormal(0, 0.06), 0.92)
                q = min(QB[b] * qm * rng.lognormal(0, 0.06), 0.5)
                cells.append(dict(county=c, division=W.DIVISION_OF[c], band=b, n=n, p=p, q=q, j=joint(p, q, PSI)))
    for c, pm, qm, nk in W.OUTSIDE:
        for b in range(4):
            n = nk * 1000.0 * W.OUTSIDE_INC[b]
            p = min(PB[b] * pm * rng.lognormal(0, 0.06), 0.92)
            q = min(QB[b] * qm * rng.lognormal(0, 0.06), 0.5)
            cells.append(dict(county=c, division=None, band=b, n=n, p=p, q=q, j=joint(p, q, PSI)))
    return cells


def draw_traits(rng, cells, idx):
    """High burden x and medical equipment y for households drawn from the given cells."""
    p = np.array([cells[i]["p"] for i in idx])
    q = np.array([cells[i]["q"] for i in idx])
    j = np.array([cells[i]["j"] for i in idx])
    u, v = rng.random(len(idx)), rng.random(len(idx))
    x = (u < p).astype(int)
    y = np.where(x == 1, (v < j / p).astype(int), (v < (q - j) / (1 - p)).astype(int))
    return x, y


def sample_counties(rng, cells, n_total, floor):
    """A county-stratified sample: each county's allocation proportional to its households with a floor, households
    drawn at random within the county (so the band mix follows the county's own)."""
    by_c = {}
    for i, c in enumerate(cells):
        by_c.setdefault(c["county"], []).append(i)
    tot = {c: sum(cells[i]["n"] for i in ix) for c, ix in by_c.items()}
    raw = {c: max(floor, n_total * tot[c] / sum(tot.values())) for c in by_c}
    scale = n_total / sum(raw.values())
    alloc = {c: int(round(raw[c] * scale)) for c in sorted(by_c)}
    drift = n_total - sum(alloc.values())
    for c in sorted(alloc, key=lambda c: -tot[c])[:abs(drift)]:
        alloc[c] += 1 if drift > 0 else -1
    idx = []
    for c in sorted(by_c):
        ix = by_c[c]
        pr = np.array([cells[i]["n"] for i in ix])
        idx.extend(rng.choice(ix, size=alloc[c], p=pr / pr.sum()).tolist())
    return np.array(idx), alloc, tot


def incomes(rng, band, n):
    """Household income in dollars inside its band, as respondents give it (to the hundred)."""
    if band == 0:
        v = 7000 + (24900 - 7000) * rng.beta(1.6, 1.3, n)
    elif band == 1:
        v = 25000 + 24900 * rng.beta(1.2, 1.1, n)
    elif band == 2:
        v = 50100 + 24800 * rng.beta(1.1, 1.2, n)
    else:
        v = np.minimum(75000 * np.exp(rng.exponential(0.45, n)), 248000)
    return np.round(v / 100) * 100


# Heating costs run higher where winters are longer (the divisions' own climates; outside counties near the middle).
CLIMATE = {"Northern": 1.24, "Lakeshore": 1.17, "River Valley": 1.10, "High Plains": 1.07, "Central": 1.0,
           "Southern Hills": 0.95, "Southwest": 0.92, "North Metro": 0.90, "South Metro": 0.88}


def climate(county):
    return CLIMATE.get(W.HOME_OF.get(county), 1.0)


def household_costs(rng, band, x, y, clim):
    """Income and annual home energy costs drawn together so each household's burden flag holds: a candidate's income
    from its band and its costs from the territory's cost distribution (higher where winters are longer and where
    someone runs medical equipment), kept when costs over income fall on its side of 6 per cent with a little room."""
    n = len(band)
    inc, cost = np.zeros(n), np.zeros(n)
    todo = np.arange(n)
    while len(todo):
        b = band[todo]
        cand = np.zeros(len(todo))
        for bb in range(4):
            m = b == bb
            cand[m] = incomes(rng, bb, int(m.sum()))
        c = np.exp(rng.normal(np.log(1650 * clim[todo] * (1 + 0.22 * y[todo])), 0.45))
        r = c / cand
        ok = np.where(x[todo] == 1, r > 0.0624, r < 0.0576)
        inc[todo[ok]], cost[todo[ok]] = cand[ok], c[ok]
        todo = todo[~ok]
    return inc, cost


def split_costs(rng, total, n):
    """Electricity, utility gas and other fuels (annual dollars) by the home's main heating fuel."""
    fuel = rng.choice([1, 2, 3, 4, 5, 6], size=n, p=[0.46, 0.31, 0.10, 0.06, 0.04, 0.03])
    elec_share = np.where(fuel == 2, rng.uniform(0.88, 1.0, n),
                          np.where(fuel == 1, rng.uniform(0.48, 0.70, n), rng.uniform(0.40, 0.62, n)))
    elec = total * elec_share
    gas = np.where(fuel == 1, total - elec, 0.0)
    other = np.where(fuel == 1, 0.0, total - elec)
    return fuel, np.round(elec), np.round(gas), np.round(other)


def energy_survey(rng, rc, cells):
    idx, alloc, tot = sample_counties(rng, cells, NA, 70)
    x, y = draw_traits(rng, cells, idx)
    band = np.array([cells[i]["band"] for i in idx])
    county = [cells[i]["county"] for i in idx]
    monthly = rng.random(len(idx)) < 0.08
    mode = rng.choice(["W", "T", "P"], size=len(idx), p=[0.52, 0.21, 0.27])
    tenure = np.where(rng.random(len(idx)) < np.where(band <= 1, 0.48, 0.74), 1, 2)
    adj = {"W": 0.94, "T": 1.11, "P": 1.03}
    base = np.array([tot[c] / alloc[c] * adj[m] for c, m in zip(county, mode)])
    inc, total = household_costs(rc, band, x, y, np.array([climate(c) for c in county]))
    fuel, elec, gas, other = split_costs(rc, total, len(idx))
    elec_amt = np.where(monthly, np.round(elec / 12), elec)
    elec_ann = np.where(monthly, elec_amt * 12, elec_amt)
    chk = ((elec_ann + gas + other) / inc > W.BURDEN).astype(int)
    assert (chk == x).all(), "a rounded cost moved a household across the burden line"
    return dict(idx=idx, x=x, y=y, band=band, income=inc, fuel=fuel, elec_amt=elec_amt, monthly=monthly, gas=gas,
                other=other, mode=mode, tenure=tenure, county=county, base=base)


def health_survey(rng, cells):
    idx, alloc, tot = sample_counties(rng, cells, NB, 90)
    n = len(idx)
    band = np.array([cells[i]["band"] for i in idx])
    adults = rng.choice([1, 2, 3, 4], size=n, p=[0.33, 0.48, 0.13, 0.06])
    f = 1 + ADULT_SLOPE * (adults - 1)
    ef = 1 + ADULT_SLOPE * (np.array([1, 2, 3, 4]) - 1) @ np.array([0.33, 0.48, 0.13, 0.06])
    q = np.array([cells[i]["q"] for i in idx]) * f / ef
    y = (rng.random(n) < q).astype(int)
    cat = np.zeros(n, int)
    for b, (cats, pr) in enumerate([((1, 2, 3), (0.30, 0.25, 0.45)), ((4, 5), (0.42, 0.58)), ((6,), (1.0,)),
                                     ((7, 8), (0.40, 0.60))]):
        m = band == b
        cat[m] = rng.choice(cats, size=int(m.sum()), p=pr)
    u = rng.random(n)
    answer = np.where(u < 0.016, 7, np.where(u < 0.021, 9, np.where(y == 1, 1, 2)))
    children = rng.choice([0, 1, 2, 3], size=n, p=[0.62, 0.17, 0.14, 0.07])
    age = rng.choice([1, 2, 3, 4, 5, 6], size=n, p=[0.07, 0.14, 0.15, 0.16, 0.19, 0.29])
    genhlth = rng.choice([1, 2, 3, 4, 5, 7, 9], size=n, p=[0.17, 0.31, 0.30, 0.14, 0.06, 0.01, 0.01])
    county = [cells[i]["county"] for i in idx]
    base = np.array([tot[c] / alloc[c] for c in county]) * rng.uniform(0.86, 1.16, n)
    return dict(idx=idx, y=y, band=band, cat=cat, answer=answer, adults=adults, children=children, age=age,
                genhlth=genhlth, county=county, base=base)


def pilot(rng, rc, cells):
    """Callowmere's screener mailed to random residential addresses in the two pilot divisions, telephone follow-up to
    non-respondents; the screen ends at an income of $50,000 or more."""
    rows = []
    for d in W.PILOT_DIVISIONS:
        ix = [i for i, c in enumerate(cells) if c["division"] == d]
        pr = np.array([cells[i]["n"] for i in ix])
        idx = rng.choice(ix, size=PILOT_SAMPLED, p=pr / pr.sum())
        resp = rng.random(PILOT_SAMPLED)
        mode = np.where(resp < 0.305, "Mail", np.where(resp < 0.415, "Phone", ""))
        keep = mode != ""
        idx, mode = idx[keep], mode[keep]
        x, y = draw_traits(rng, cells, idx)
        band = np.array([cells[i]["band"] for i in idx])
        u = rng.random(len(idx))
        county = [cells[i]["county"] for i in idx]
        inc, total = household_costs(rc, band, x, y, np.array([climate(c) for c in county]))
        fuel, elec, gas, other = split_costs(rc, total, len(idx))
        for k in range(len(idx)):
            if band[k] >= 2:
                status, equip = "Ended - income", None
            elif u[k] < 0.025:
                status, equip = "Partial", None
            else:
                status = "Complete"
                equip = "Don't know" if u[k] > 0.988 else ("Yes" if y[k] else "No")
            rows.append(dict(division=d, county=county[k], band=int(band[k]), x=int(x[k]), y=int(y[k]),
                             income=float(inc[k]), elec=float(elec[k]), other=float(gas[k] + other[k]),
                             mode=str(mode[k]), status=status, equip=equip))
    return rows


def pilot_tables(P, partial_as_no=False, dk_as_no=False):
    """The pilot's complete screens with a yes or no on the equipment, by band and by division and band: (both,
    burden only, equipment only, neither); the keywords are the natural mishandlings of its screens."""
    tabs, tabs_div = {}, {}
    for r in P:
        if r["status"] == "Ended - income":
            continue
        ans = r["equip"]
        if r["status"] == "Partial":
            if not partial_as_no:
                continue
            ans = "No"
        if ans == "Don't know":
            if not dk_as_no:
                continue
            ans = "No"
        x = int((r["elec"] + r["other"]) / r["income"] > W.BURDEN)
        y = int(ans == "Yes")
        k = 0 if (x and y) else 1 if x else 2 if y else 3
        for key, store in ((r["band"], tabs), ((r["division"], r["band"]), tabs_div)):
            store.setdefault(key, [0, 0, 0, 0])[k] += 1
    return tabs, tabs_div


def eligible_cells(cells, pub):
    """Published households of each territory division and eligible band (the pack's own county rows summed)."""
    out = {}
    for c in cells:
        if c["division"] and c["band"] in W.ELIGIBLE_BANDS:
            out[(c["division"], c["band"])] = out.get((c["division"], c["band"]), 0) + pub[(c["county"], c["band"])]
    return out


def world(seed=SEED):
    """One stream per component, so the asks' files and the costs never move the calibrated survey draws."""
    rngs = [np.random.default_rng([seed, k]) for k in range(8)]
    cells = population(rngs[1])
    A = energy_survey(rngs[2], rngs[3], cells)
    B = health_survey(rngs[4], cells)
    P = pilot(np.random.default_rng([seed, 5, PILOT_DRAW]), np.random.default_rng([seed, 6, PILOT_DRAW]), cells)
    return dict(rng=rngs[7], cells=cells, A=A, B=B, P=P)


def final_weights(base, county, band, pub):
    """Base weights post-stratified to the published households of each county and income band."""
    w = np.zeros(len(base))
    cells = {}
    for i, key in enumerate(zip(county, band)):
        cells.setdefault(key, []).append(i)
    for key, ix in cells.items():
        w[ix] = base[ix] * pub[key] / base[ix].sum()
    return w


def conformed(x, pub, monthly_as_annual=False, dk_as_no=False, base_only=False):
    """Each territory division and eligible band's weighted high-burden share (energy survey) and equipment share (health
    survey), the way the pack is read; the keywords are the natural mishandlings of the mess."""
    A, B = x["A"], x["B"]
    elec = A["elec_amt"] if monthly_as_annual else np.where(A["monthly"], A["elec_amt"] * 12, A["elec_amt"])
    xa = ((elec + A["gas"] + A["other"]) / A["income"] > W.BURDEN).astype(float)
    wa = A["base"] if base_only else final_weights(A["base"], A["county"], A["band"], pub)
    wb = final_weights(B["base"], B["county"], B["band"], pub)
    yb = (B["answer"] == 1).astype(float)
    okb = np.ones(len(yb), bool) if dk_as_no else B["answer"] <= 2
    div_a = np.array([W.DIVISION_OF.get(c) for c in A["county"]])
    div_b = np.array([W.DIVISION_OF.get(c) for c in B["county"]])
    p, q = {}, {}
    for d in W.DIV_NAMES:
        for b in W.ELIGIBLE_BANDS:
            m = (div_a == d) & (A["band"] == b)
            p[(d, b)] = float((wa[m] * xa[m]).sum() / wa[m].sum())
            m = (div_b == d) & (B["band"] == b) & okb
            q[(d, b)] = float((wb[m] * yb[m]).sum() / wb[m].sum())
    return p, q


def publish(x, lo=0.80, hi=1.20, tol=8, gap=90, spread=36, seed=SEED):
    """The demographer's published households: each territory division and eligible band's county figures scaled by one
    factor so the fused eligible households sit within a few households of a hundred in every cell, each division's
    total clear of a caseworker step and off the round thousands, the territory total rounding to the sum of the
    divisions' rounded totals and off the round thousands, and the independence product's totals as clear of a step as
    the grid allows."""
    import methods as M
    raw = {(c["county"], c["band"]): round(c["n"], -1) for c in x["cells"]}
    p, q = conformed(x, raw)
    tabs, tabs_div = pilot_tables(x["P"])
    N = eligible_cells(x["cells"], raw)
    R, _ = M.routes(N, p, q, tabs, tabs_div)
    g, ind = R["golden"], R["independence"]
    fam = [R[m] for m in M.FAMILY]
    pm, _ = conformed(x, raw, monthly_as_annual=True)
    pb, _ = conformed(x, raw, base_only=True)
    _, qd = conformed(x, raw, dk_as_no=True)
    layer1 = [M.routes(N, a, b, t, tabs_div)[0]["golden"] for a, b, t in
              ((pm, q, tabs), (pb, q, tabs), (p, qd, tabs), (p, q, pilot_tables(x["P"], partial_as_no=True)[0]),
               (p, q, pilot_tables(x["P"], dk_as_no=True)[0]))]
    grid = np.arange(lo, hi + 1e-9, 0.0025)

    shown = {n for _, _, v in pilot_counts(pilot_records(np.random.default_rng([seed, 11]), x["P"])) for n in v}

    def mid(k, s):             # the golden near its hundred and every fusion keeping both shares on the same hundred
        h = round(g[k] * s, -2)
        return abs(g[k] * s - h) <= tol and all(abs(f[k] * s - h) <= spread for f in fam) and h not in shown
    options = {}
    for d in W.DIV_NAMES:
        opts = []
        c0 = [s for s in grid if mid((d, 0), s)]
        c1 = [s for s in grid if mid((d, 1), s)]
        for s0 in c0:
            for s1 in c1:
                t = g[(d, 0)] * s0 + g[(d, 1)] * s1
                if min(t % W.CASELOAD, W.CASELOAD - t % W.CASELOAD) < gap or round(t, -2) % 1000 == 0 \
                        or round(t, -2) in shown:          # no staffing figure repeats a count in the pilot report
                    continue
                if any(abs(f[(d, 0)] * s0 + f[(d, 1)] * s1 - round(t, -2)) > 50 - 12 for f in fam):
                    continue
                if any(M.caseworkers(v[(d, 0)] * s0 + v[(d, 1)] * s1) != M.caseworkers(t) for v in layer1):
                    continue           # each mishandling of the mess leaves the division's staffing where it is
                ti = ind[(d, 0)] * s0 + ind[(d, 1)] * s1
                di = min(ti % W.CASELOAD, W.CASELOAD - ti % W.CASELOAD)
                opts.append((abs(s0 - 1) + abs(s1 - 1) - 0.004 * min(di, 60), s0, s1, int(round(t - round(t, -2))),
                             int(round(t, -2))))
        if not opts:
            raise SystemExit("no centring for %s" % d)
        options[d] = sorted(opts)[:30]
    states = {(0, 0): (0.0, [])}       # (summed rounding error, rounded sum mod 1000) -> cheapest choice
    for d in W.DIV_NAMES:
        nxt = {}
        for (err, mod), (cost, picks) in states.items():
            for o in options[d]:
                key, c = (err + o[3], (mod + o[4]) % 1000), cost + o[0]
                if key not in nxt or c < nxt[key][0]:
                    nxt[key] = (c, picks + [o])
        states = nxt
    ok = [(v[0], k) for k, v in states.items() if abs(k[0]) <= 25 and k[1] != 0]
    if not ok:
        raise SystemExit("no centring keeps the territory total on the divisions' rounded sum")
    best = states[min(ok)[1]][1]
    scale = {}
    for d, o in zip(W.DIV_NAMES, best):
        scale[(d, 0)], scale[(d, 1)] = o[1], o[2]
    pub = {}
    noise = np.random.default_rng([seed, 13])
    county_f = {c: noise.lognormal(0, 0.05) for c in W.COUNTIES}
    for c in x["cells"]:
        if c["division"] and c["band"] in W.ELIGIBLE_BANDS:
            s = scale[(c["division"], c["band"])]
        else:                    # the cells the staffing never reads carry their own estimation error
            s = (county_f[c["county"]] if not c["division"] else 1.0) * noise.lognormal(0, 0.035)
        pub[(c["county"], c["band"])] = round(c["n"] * s, -1)
    return pub, scale


# ---------------------------------------------------------------------------------------------------------------------
# Callowmere's own operational records: the medical baseline enrolment extract and the backup battery work orders.
import datetime as _dt

EXTRACT = _dt.date(2026, 11, 3)            # the enrolment and battery extracts were run on 3 November 2026
COUNT_DATE = _dt.date(2026, 10, 31)
HISTORY_FROM = _dt.date(2020, 1, 1)        # the extract holds every spell active on or after 1 January 2020
TAKE_UP = 0.55                             # share of equipment households on the medical baseline rate at a time
EXIT_RATE, MOVE_RATE = 0.11, 0.075         # a year: leaving the rate, and moving home inside the territory
END_REASONS = (("Deceased", 0.34), ("Recertification not received", 0.27), ("Moved", 0.24),
               ("Customer request", 0.15))
EQUIPMENT = (("Oxygen concentrator", 0.31), ("Power wheelchair or scooter", 0.17), ("Home dialysis", 0.07),
             ("Ventilator or BiPAP", 0.12), ("Enteral feeding pump", 0.05), ("Apnea monitor", 0.04),
             ("Electric hospital bed", 0.14), ("Other", 0.10))


def _day(d0, days):
    return d0 + _dt.timedelta(days=int(days))


def _pick(rng, pairs):
    names, pr = zip(*pairs)
    return names[rng.choice(len(names), p=np.array(pr) / sum(pr))]


def enrolment(rng, cells):
    """Medical baseline households, their accounts and spells from 2020 to the extract. A move inside the territory
    opens a new account at the new premise with the rate transferred (the new spell names the old account); the
    customer usually starts service at the new home before stopping it at the old one, so for a few days or weeks
    both accounts are billed at the rate. Moves stay inside the household's division."""
    eq = {}
    for c in cells:
        if c["division"]:
            eq[c["county"]] = eq.get(c["county"], 0) + c["n"] * c["q"]
    households = []
    span = (EXTRACT - HISTORY_FROM).days
    for county in sorted(eq):
        stock = eq[county] * TAKE_UP
        start_stock = int(round(stock * 0.97))
        arrivals = int(rng.poisson(stock * (EXIT_RATE + 0.0045) * span / 365.25))
        tail = 1 - math.exp(-6200 / 1500)             # spells open in 2020 began up to 17 years earlier, fewer the
        starts = [_day(HISTORY_FROM, -1 - int(-1500 * math.log(1 - rng.random() * tail)))   # further back
                  for _ in range(start_stock)]
        starts += [_day(HISTORY_FROM, int(rng.integers(0, span))) for _ in range(arrivals)]
        sib = [c for c in W.DIVISION_OF if W.DIVISION_OF[c] == W.DIVISION_OF[county] and c != county]
        for s0 in starts:
            hh = dict(life_support=bool(rng.random() < 0.31), equipment=_pick(rng, EQUIPMENT), spells=[])
            t, here = s0, county
            exit_at = _day(max(s0, HISTORY_FROM), rng.exponential(365.25 / EXIT_RATE))
            while True:
                move = _day(max(t, HISTORY_FROM), rng.exponential(365.25 / MOVE_RATE))
                if move >= exit_at or move > EXTRACT:
                    end = exit_at if exit_at <= EXTRACT else None
                    hh["spells"].append(dict(start=t, end=end, reason=_pick(rng, END_REASONS) if end else "",
                                             county=here))
                    break
                overlap = 0 if rng.random() < 0.22 else int(min(rng.gamma(1.6, 11.0), 75))
                stop = _day(move, overlap)
                hh["spells"].append(dict(start=t, end=stop if stop <= EXTRACT else None,
                                         reason="Moved" if stop <= EXTRACT else "", county=here))
                t = move
                if sib and rng.random() < 0.18:
                    here = sib[int(rng.integers(len(sib)))]
            if hh["spells"][-1]["end"] is None or hh["spells"][-1]["end"] >= HISTORY_FROM:
                households.append(hh)
    _ensure_overlaps(rng, households)
    _ensure_new_starts(rng, households)
    for hh in households:                        # nothing starts or ends on the count date itself
        for sp in hh["spells"]:
            if sp["start"] == COUNT_DATE:
                sp["start"] = _day(COUNT_DATE, -1)
            if sp["end"] == COUNT_DATE:
                sp["end"] = _day(COUNT_DATE, -1)
    _number(rng, households)
    return households


def open_on(sp, d):
    return sp["start"] <= d and (sp["end"] is None or sp["end"] > d)


def _ensure_overlaps(rng, households, floor=3):
    """Every division holds a few households moving house across the count date (both accounts on the rate)."""
    per = {}
    for hh in households:
        if sum(open_on(sp, COUNT_DATE) for sp in hh["spells"]) > 1:
            d = W.DIVISION_OF[hh["spells"][-1]["county"]]
            per[d] = per.get(d, 0) + 1
    for d in W.DIV_NAMES:
        need = floor - per.get(d, 0)
        pool = [hh for hh in households if len(hh["spells"]) == 1 and hh["spells"][0]["end"] is None
                and W.DIVISION_OF[hh["spells"][0]["county"]] == d and hh["spells"][0]["start"] < _dt.date(2025, 6, 1)]
        for k in range(max(need, 0)):
            hh = pool[int(rng.integers(len(pool)))]
            pool.remove(hh)
            sp = hh["spells"][0]
            move = _day(_dt.date(2026, 10, 9), int(rng.integers(0, 19)))
            stop = _day(_dt.date(2026, 11, 1), int(rng.integers(1, 30)))
            hh["spells"] = [dict(start=sp["start"], end=stop if stop <= EXTRACT else None,
                                 reason="Moved" if stop <= EXTRACT else "", county=sp["county"]),
                            dict(start=move, end=None, reason="", county=sp["county"])]


def _ensure_new_starts(rng, households):
    """Certifications keep arriving after the month closes: where a division's accounts open at the extract would
    still equal its households on the rate on the count date, a household joins the rate on 1 to 3 November."""
    for d in W.DIV_NAMES:
        on = sum(1 for hh in households
                 if any(open_on(sp, COUNT_DATE) and W.DIVISION_OF[sp["county"]] == d for sp in hh["spells"]))
        at = sum(1 for hh in households for sp in hh["spells"] if sp["end"] is None and W.DIVISION_OF[sp["county"]] == d)
        if at == on:
            here = [c for c in W.DIVISION_OF if W.DIVISION_OF[c] == d]
            households.append(dict(life_support=bool(rng.random() < 0.31), equipment=_pick(rng, EQUIPMENT),
                                   spells=[dict(start=_day(COUNT_DATE, int(rng.integers(1, 4))), end=None, reason="",
                                                county=here[int(rng.integers(len(here)))])]))


def _number(rng, households):
    """Accounts numbered in the order they were opened, premises drawn from the territory's premise register, each
    account's division as set up when it was opened."""
    opened = []
    for h, hh in enumerate(households):
        for k, sp in enumerate(hh["spells"]):
            opened.append((sp["start"], h, k))
    opened.sort()
    acct = 6100000000
    premises = rng.choice(np.arange(10000000, 99999999), size=len(opened), replace=False)
    for (d0, h, k), prem in zip(opened, premises):
        acct += int(rng.integers(40, 160))
        sp = households[h]["spells"][k]
        sp["account"] = str(acct)
        sp["premise"] = "P%08d" % prem
        c = sp["county"]
        if c in W.REORG and sp["start"] < _dt.date.fromisoformat(W.REORG[c][2]):
            sp["division_stored"] = W.REORG[c][0]
        else:
            sp["division_stored"] = W.DIVISION_OF[c]
    for hh in households:
        for k, sp in enumerate(hh["spells"]):
            sp["prior"] = hh["spells"][k - 1]["account"] if k else ""


# The backup battery programme: free units for life-support customers on the medical baseline rate, rolled out county
# by county from December 2025; crews' handhelds stamp completion times in UTC, the company works on Central Time.
CENTRAL = None


def central_offset(d):
    """Hours behind UTC on Central Time for a local date (daylight time from 8 March to 1 November 2026)."""
    return 5 if _dt.date(2026, 3, 8) <= d < _dt.date(2026, 11, 1) else 6


def _utc(day, hour, minute):
    local = _dt.datetime(day.year, day.month, day.day, hour, minute)
    return local + _dt.timedelta(hours=central_offset(day))


def batteries(rng, households):
    """Work orders: first placements (some after a no-access or cancelled visit), exchanges of failed units at the same
    account, and re-installs at the new account after a household moves; a few evening completions at the window's
    two ends."""
    counties = sorted(W.DIVISION_OF)
    roll = {}
    for c in counties:
        roll[c] = _day(_dt.date(2025, 12, 1), int(rng.integers(0, 190)))
        if c in W.REORG:
            roll[c] = _day(_dt.date(2026, 8, 3), int(rng.integers(0, 20)))
    orders, serial = [], [251000]

    def unit():
        serial[0] += int(rng.integers(1, 9))
        return "BU-%07d" % serial[0]

    def stamp(day, evening=False):
        if evening:
            h, m = int(rng.integers(19, 21)), int(rng.integers(0, 60))
        else:
            h, m = int(rng.integers(8, 18)), int(rng.integers(0, 60))
        return _utc(day, h, m)

    def spell_on(hh, d):
        for sp in hh["spells"]:
            if open_on(sp, d):
                return sp
        return None

    placed = []
    for h, hh in enumerate(households):
        if not hh["life_support"]:
            continue
        last = hh["spells"][-1]
        c0 = last["county"]
        day = _day(roll[c0], int(rng.integers(0, 150)))
        if day > _day(EXTRACT, -1) or rng.random() > 0.62:
            continue
        sp = spell_on(hh, day)
        if sp is None or sp is not last and len(hh["spells"]) > 1 and sp["end"] and sp["end"] < _day(day, 30):
            continue
        if rng.random() < 0.11:          # a first visit that found nobody home or was called off
            orders.append(dict(h=h, sp=sp, day=_day(day, -int(rng.integers(6, 21))), status=_pick(
                rng, (("No access", 0.65), ("Cancelled", 0.35))), at=None, unit="", removed=""))
        u = unit()
        orders.append(dict(h=h, sp=sp, day=day, status="Completed", at=stamp(day, rng.random() < 0.04), unit=u,
                           removed=""))
        placed.append((h, sp, day, u))
    for o in orders:                     # a crew that ran over finishes a booked visit a day or three later
        if o["status"] == "Completed" and rng.random() < 0.09:
            late = _day(o["day"], int(rng.integers(1, 4)))
            if late < EXTRACT and open_on(o["sp"], late) and not (o["day"] <= COUNT_DATE < late) \
                    and not (o["day"] < _dt.date(2026, 1, 1) <= late):
                o["at"] = stamp(late)
    for h, sp, day, u in placed:
        hh = households[h]
        if day < _dt.date(2026, 1, 1):
            continue                       # nothing more inside the window for a household placed in 2025
        later = [s for s in hh["spells"] if s["start"] > day]
        if later and later[0]["start"] <= _day(COUNT_DATE, -12):
            nxt = later[0]
            d2 = _day(nxt["start"], int(rng.integers(2, 11)))
            orders.append(dict(h=h, sp=nxt, day=d2, status="Completed", at=stamp(d2), unit=u, removed=""))
        elif rng.random() < 0.05:
            d2 = _day(day, int(rng.integers(12, 140)))
            if d2 <= _day(COUNT_DATE, -3) and open_on(sp, d2):
                orders.append(dict(h=h, sp=sp, day=d2, status="Completed", at=stamp(d2), unit=unit(), removed=u))
    _evening_edges(rng, orders)
    _booked_edges(rng, orders)
    orders.sort(key=lambda o: (o["day"], o["at"] or _dt.datetime(o["day"].year, o["day"].month, o["day"].day, 12)))
    return orders


def _evening_edges(rng, orders):
    """Crews finishing late on the window's last day (the Saturday push before winter, every division) and on New
    Year's Eve: single-visit households, their one completed order on that evening."""
    done = {}
    for o in orders:
        if o["status"] == "Completed":
            done.setdefault(o["h"], []).append(o)
    single = [os_[0] for os_ in done.values() if len(os_) == 1]
    quota = {}
    for day, lo, hi, count in ((_dt.date(2025, 12, 31), _dt.date(2025, 12, 1), _dt.date(2025, 12, 31), 3),
                               (COUNT_DATE, _dt.date(2026, 4, 1), COUNT_DATE, 9)):
        pool = [o for o in single if lo <= o["day"] <= hi and open_on(o["sp"], day) and o["day"] != day]
        seen = {}
        for o in sorted(pool, key=lambda o: (o["sp"]["account"])):
            d = W.DIVISION_OF[o["sp"]["county"]]
            want = 1 if day != COUNT_DATE else 1 + quota.get(d, 0)
            if seen.get(d, 0) >= want or (d not in seen and len(seen) == count):
                continue
            seen[d] = seen.get(d, 0) + 1
            if day != COUNT_DATE:
                quota[d] = 1
            o["day"] = day
            hour = 19 if day == COUNT_DATE else 18
            o["at"] = _utc(day, hour + int(rng.integers(0, 2)), int(rng.integers(5, 55)))


def _booked_edges(rng, orders):
    """Visits booked for the last days of a window and finished after it: booked for October 29 to 31 and completed on
    November 2, and booked for December 29 to 31, 2025 and completed in the first days of January."""
    done = {}
    for o in orders:
        if o["status"] == "Completed":
            done.setdefault(o["h"], []).append(o)
    single = [os_[0] for os_ in done.values() if len(os_) == 1 and os_[0]["at"].date() == os_[0]["day"]]
    for lo, hi, finish, count in ((_dt.date(2026, 10, 29), _dt.date(2026, 10, 30), _dt.date(2026, 11, 2), 4),
                                  (_dt.date(2025, 12, 29), _dt.date(2025, 12, 30), _dt.date(2026, 1, 2), 2)):
        pool = [o for o in single if lo <= o["day"] <= hi and open_on(o["sp"], finish)]
        seen = set()
        for o in sorted(pool, key=lambda o: o["sp"]["account"]):
            d = W.DIVISION_OF[o["sp"]["county"]]
            if d in seen or len(seen) == count:
                continue
            seen.add(d)
            o["at"] = _utc(finish, int(rng.integers(9, 16)), int(rng.integers(0, 60)))


def pilot_counts(screens):
    """The pilot report's table: screens returned, ended at the income question, complete and partial, by division and
    mode and in all."""
    sts = ("Ended - income", "Complete", "Partial")
    rows = []
    for d in W.PILOT_DIVISIONS:
        for m in ("Mail", "Phone"):
            rs = [r for r in screens if r["division"] == d and r["mode"] == m]
            rows.append((d, m, [len(rs)] + [sum(r["status"] == st for r in rs) for st in sts]))
    rows.append(("Both", "Both", [len(screens)] + [sum(r["status"] == st for r in screens) for st in sts]))
    return rows


def pilot_records(rng, P):
    """The screening system's records: one per returned screen, an address that answered by mail and then by telephone
    holding two (the same answers, the income sometimes given a little differently), each with its date."""
    keys = set()
    rows = []
    for r in P:
        while True:
            k = "".join(rng.choice(list("ABCDEFGHJKLMNPQRSTUVWXYZ23456789"), size=10))
            if k not in keys:
                keys.add(k)
                break
        first = _day(_dt.date(2025, 3, 10), int(rng.integers(0, 112))) if r["mode"] == "Mail" else \
            _day(_dt.date(2025, 5, 5), int(rng.integers(0, 116)))
        rows.append(dict(r, key=k, received=first))
        if r["status"] == "Complete" and r["mode"] == "Mail" and rng.random() < 0.07:
            inc = r["income"]
            for _ in range(20):
                alt = inc + 100 * int(rng.integers(-3, 4))
                same_band = (alt < 25000) == (inc < 25000) and alt < W.INCOME_LIMIT
                same_flag = ((r["elec"] + r["other"]) / alt > W.BURDEN) == ((r["elec"] + r["other"]) / inc > W.BURDEN)
                if same_band and same_flag and abs((r["elec"] + r["other"]) / alt - W.BURDEN) > 0.0012:
                    break
            else:
                alt = inc
            rows.append(dict(r, key=k, mode="Phone", income=alt, received=_day(_dt.date(2025, 7, 1),
                                                                              int(rng.integers(0, 59)))))
    rows.sort(key=lambda r: (r["received"], r["key"]))
    return rows


def distractor_data(rng, cells):
    """The health department's heat vulnerability index by county and the energy office's energy assistance
    applications by county and month (2025)."""
    n = {}
    low = {}
    for c in cells:
        n[c["county"]] = n.get(c["county"], 0) + c["n"]
        if c["band"] == 0:
            low[c["county"]] = low.get(c["county"], 0) + c["n"] * c["p"]
    hvi = []
    for c in W.COUNTIES:
        old = rng.uniform(14.5, 24.5)
        alone = old * rng.uniform(0.25, 0.36)
        noac = rng.uniform(4.0, 31.0)
        imperv = rng.uniform(1.2, 9.0) if n[c] < 60000 else rng.uniform(9.0, 26.0)
        score = 0.9 * old + 1.1 * alone + 0.6 * noac + 0.8 * imperv + rng.normal(0, 2.5)
        hvi.append(dict(county=c, old=old, alone=alone, noac=noac, imperv=imperv, score=score))
    mu = sum(h["score"] for h in hvi) / len(hvi)
    sd = (sum((h["score"] - mu) ** 2 for h in hvi) / (len(hvi) - 1)) ** 0.5
    for h in hvi:
        h["score"] = 50 + 15 * (h["score"] - mu) / sd
    order = sorted(hvi, key=lambda h: -h["score"])
    for k, h in enumerate(order, start=1):
        h["rank"] = k
    season = [1.9, 1.7, 1.2, 0.8, 0.6, 0.7, 0.9, 0.9, 0.7, 0.8, 1.2, 1.6]
    apps = []
    for c in W.COUNTIES:
        base = low[c] * 0.021
        for m in range(12):
            a = int(rng.poisson(base * season[m]))
            ok = int(rng.binomial(a, 0.81)) if a else 0
            crisis = int(rng.poisson(a * (0.24 if m in (0, 1, 11) else 0.07)))
            benefit = round(float(rng.normal(462 if m in (0, 1, 2, 10, 11) else 338, 22)))
            apps.append(dict(county=c, month="2025-%02d" % (m + 1), received=a, approved=ok, crisis=crisis,
                             benefit=benefit))
    return hvi, apps


def everything(seed=SEED):
    """The whole world: the calibrated surveys and pilot, the published estimates, the operational records and the
    distractors' data."""
    x = world(seed)
    x["pub"], x["scale"] = publish(x, seed=seed)
    rk = np.random.default_rng([seed, 9])
    x["households"] = enrolment(rk, x["cells"])
    x["orders"] = batteries(np.random.default_rng([seed, 10]), x["households"])
    x["screens"] = pilot_records(np.random.default_rng([seed, 11]), x["P"])
    x["hvi"], x["apps"] = distractor_data(np.random.default_rng([seed, 12]), x["cells"])
    return x
