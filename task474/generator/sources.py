"""The clean truth: every station's and every link's daily traffic by vehicle class over the program year, each
terminal's daily truck visits, and the drayage truck registry. Nothing here knows about files, layouts or mess."""
import datetime as dt

import numpy as np

import world as W

ND = len(W.DAYS)
DOWS = np.array([d.weekday() for d in W.DAYS])
MONTHS = np.array([d.month for d in W.DAYS])
GATE_DOW = np.array([1.04, 1.03, 1.02, 1.01, .99, .38, 0.0])       # gates closed on Sundays


def daily(rng, aadt, su, cu, noise=(.045, .07, .075)):
    """{class: daily volumes over the program year}, each class's mean equal to its share of aadt."""
    shares = {"P": 1 - su - cu, "SU": su, "CU": cu}
    out = {}
    for i, c in enumerate(W.CLASSES):
        dow = np.array(W.DOW[c]) * (1 + rng.normal(0, .025, 7))
        mon = {m: v * (1 + rng.normal(0, .015)) for m, v in W.MON[c].items()}
        v = dow[DOWS] * np.array([mon[m] for m in MONTHS]) * rng.lognormal(0, noise[i], ND)
        for k, d in enumerate(W.DAYS):
            if d in W.HOLIDAYS:
                v[k] *= W.HOLIDAYS[d][0 if c == "P" else 1]
        out[c] = v / v.mean() * aadt * shares[c]
    return out


def gates(rng):
    """{terminal: daily truck visits over the program year}: the weekday pattern, holidays, and the lift each vessel
    call gives the gate on its day and the two after, two services per terminal on their own rotations."""
    out = {}
    for t, (name, base, cycles, lift) in W.TERMINALS.items():
        v = GATE_DOW[DOWS] * np.array([W.PORT_MONTH[m] for m in MONTHS])
        for cyc in cycles:
            phase = int(rng.integers(0, cyc))
            bump = np.zeros(ND)
            for k in range(phase, ND, cyc):
                for j, w in enumerate((1.0, .75, .35)):
                    if k + j < ND:
                        bump[k + j] += lift * w * float(rng.uniform(.75, 1.25))
            v = v * (1 + bump - bump.mean())
        for k, d in enumerate(W.DAYS):
            if d in W.HOLIDAYS:
                v[k] *= .25
        v = v * rng.lognormal(0, .05, ND)
        out[t] = np.round(v * base).astype(int)
    return out


def world(rng, grng):
    st = {s: daily(rng, a, su, cu) for s, (_, _, a, su, cu, _) in W.STATIONS.items()}
    g = gates(grng)
    ln = {}
    for k, (_, _, a, su, cu) in W.LINKS.items():
        ln[k] = daily(rng, a, su, cu)
        if k in W.ACCESS:
            term, share, other = W.ACCESS[k]
            # combination trucks on an access road: the terminal's drays in and out, plus a few others
            extra = daily(rng, other / .1, 0, .1)["CU"]
            ln[k]["CU"] = 2 * share * g[term] + extra
    return dict(stations=st, links=ln, gates=g)


def nox_per_mile(byclass):
    """tonnes of NOx per mile over the program year from {class: AADT}."""
    return sum(byclass[c] * ND * W.EF[c] for c in W.CLASSES) / 1e6


def truth(x):
    return {k: nox_per_mile({c: v[c].mean() for c in W.CLASSES}) for k, v in x["links"].items()}


def registry(rng):
    """The drayage trucks registered with the port over the program year: one record per registration, each truck
    with its VIN, carrier, engine family and model year. Some trucks move to another carrier (a new registration
    under a new truck id; the old one closed, or for a few left open), some trucks leave, new ones join."""
    fams = {}
    for my in range(2004, 2026):
        for _ in range(int(rng.integers(3, 7))):
            maker = "ABCDHMNPVW"[int(rng.integers(0, 10))]
            code = "%s%s%s%s%04.1f%s" % ("456789ABCDEFGHJKLMNPRS"[my - 2004], maker, "XEC"[int(rng.integers(0, 3))],
                                        "HD", float(rng.uniform(10.8, 15.0)), "XAPBGC"[int(rng.integers(0, 6))])
            fams[code] = my
    by_year = {}
    for code, my in fams.items():
        by_year.setdefault(my, []).append(code)
    regs = []
    trucks = []
    tid = 100200
    for i in range(W.N_TRUCKS):
        my = int(rng.choice(np.arange(2004, 2026), p=np.r_[np.full(6, .022), np.full(16, (1 - .132) / 16)]))
        vy = my
        if rng.random() < .045:
            # a glider: a new chassis on a remanufactured pre-2010 engine
            my, vy = int(rng.integers(2004, 2010)), int(rng.integers(2014, 2019))
        vin = ("%s%09d" % ("1XKYDP4X" if rng.random() < .5 else "3AKJHHDR", int(rng.integers(0, 10 ** 9))))[:17]
        car = W.CARRIERS[int(rng.choice(len(W.CARRIERS), p=np.array([18, 15, 14, 12, 11, 11, 10, 9]) / 100))]
        start = W.DAYS[0] if i < int(W.N_TRUCKS * .86) else W.DAYS[int(rng.integers(1, ND))]
        end = None
        if rng.random() < .07:
            end = W.DAYS[int(rng.integers(30, ND))]
            if end <= start:
                end = None
        fam = by_year[my][int(rng.integers(0, len(by_year[my])))]
        trucks.append(dict(vin=vin, my=my, fam=fam))
        tid += int(rng.integers(1, 4))
        legacy = rng.random() < (.62 if my < 2014 else .18)          # registered before the 2024 form change
        regs.append(dict(truck=tid, vin=vin, car=car, start=start, end=end, my=my, vy=vy, fam=fam, legacy=legacy,
                         open_dup=False))
        # a move to another carrier mid-year: a new registration under a new truck id
        if end is None and rng.random() < .09:
            d = W.DAYS[int(rng.integers(20, ND - 10))]
            if d <= start + dt.timedelta(20):
                continue
            new = W.CARRIERS[int(rng.integers(0, len(W.CARRIERS)))]
            if new == car:
                continue
            left_open = rng.random() < .45 and any(ch in "01" for ch in vin)
            if not left_open:
                regs[-1]["end"] = d - dt.timedelta(1)
            regs[-1]["open_dup"] = left_open
            tid += int(rng.integers(1, 4))
            # keyed by hand at the new carrier's registration: a 0 or 1 in the VIN typed as O or I when the old
            # registration was left open
            v2 = vin
            pos = [i for i, ch in enumerate(vin) if ch in "01"]
            if left_open and pos:
                v2 = vin[:pos[-1]] + {"0": "O", "1": "I"}[vin[pos[-1]]] + vin[pos[-1] + 1:]
            regs.append(dict(truck=tid + 50000, vin=v2, car=new, start=d, end=None, my=my, vy=vy, fam=fam,
                             legacy=False, open_dup=False))
    return dict(regs=regs, fams=fams)


def registry_truth(r):
    """{quarter: (trucks registered on the quarter's last day, those of model year 2009 or older)} and
    {carrier: (trucks at 30 September 2026, of which 2009 or older)}: a truck counted once, under its latest
    registration."""
    q_end = {q: dt.date.fromisoformat(b) for q, (a, b) in W.QUARTERS.items()}
    out = {}
    for q, d in q_end.items():
        live = {}
        for g in r["regs"]:
            if g["start"] <= d and (g["end"] is None or d <= g["end"]):
                v = g["vin"].replace("O", "0").replace("I", "1")
                if v not in live or g["start"] > live[v]["start"]:
                    live[v] = g
        out[q] = live
    quarters = {q: (len(v), sum(1 for g in v.values() if g["my"] <= 2009)) for q, v in out.items()}
    carriers = {}
    for g in out[4].values():
        c = carriers.setdefault(g["car"], [0, 0])
        c[0] += 1
        c[1] += g["my"] <= 2009
    return quarters, {k: tuple(v) for k, v in carriers.items()}
