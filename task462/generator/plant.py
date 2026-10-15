"""The Tollaver Gas Processing Plant's receipts: the meter stations its shippers deliver through, the monthly
allocation statements (each line booked in the statement's accounting month, prior-period adjustments carrying the
production month they correct in the line's reference), the March 2026 statement re-issued, two stations metering
energy only after a June 2026 upgrade, and each station's monthly heating value."""
import math

import numpy as np

import production as PR
import world as W

PPA_WORDS = ["meter correction", "chart integration", "orifice plate change", "EFM recalibration", "gas quality restatement"]


def _monthly_by_operator(rows):
    """Gas (Mcf at 14.65 psia) each operator's wells produced per production month: latest report, operator of record."""
    latest = {}
    for r in rows:
        k = (r["api"], r["y"], r["m"])
        if k not in latest or r["filed"] > latest[k]["filed"]:
            latest[k] = r
    out = {}
    for r in latest.values():
        out[(r["op"], r["y"], r["m"])] = out.get((r["op"], r["y"], r["m"]), 0.0) + r["gas"]
    return out


def build(seed, rows):
    rng = np.random.default_rng(seed + W.PLANT_STREAM)
    gas = _monthly_by_operator(rows)
    ops = [p[0] for p in W.PRODUCERS] + [o[0] for o in W.OTHER_OPERATORS if o[2] > 0]
    number = {p[0]: p[1] for p in W.PRODUCERS}
    number.update({o[0]: o[1] for o in W.OTHER_OPERATORS})
    stations, k = [], 101
    for op in ops:
        size = sum(v for (o, y, m), v in gas.items() if o == op)
        n = 1 if size < 6e7 else (2 if size < 1.5e8 else 3)
        shares = rng.dirichlet(np.ones(n) * 4.0)
        for j in range(n):
            stations.append(dict(station="M-%d" % k, name="%s %s" % (op.split()[0], ("North", "South", "East")[j] if n > 1 else "Central"),
                                 op=op, share=float(shares[j]), shipper="SH-%03d" % (200 + 7 * k % 600)))
            k += int(rng.integers(1, 4))
    energy_only = [s["station"] for s in rng.choice([s for s in stations if s["op"] in W.NAMES], 2, replace=False)]
    ratio = {op: float(rng.uniform(0.930, 0.968)) for op in ops}
    hv = {}
    for s in stations:
        base = float(rng.uniform(1045, 1185))
        for (y, m) in PR.MONTHS + [(2026, 10)]:
            hv[(s["station"], y, m)] = round(base + float(rng.normal(0, 6)), 1)
    vol = {}                                      # (station, y, m) -> Mcf at the plant's 14.73 psia
    for s in stations:
        for (y, m) in PR.MONTHS:
            g = gas.get((s["op"], y, m), 0.0)
            vol[(s["station"], y, m)] = g * W.STATE_PSIA / W.STD_PSIA * ratio[s["op"]] * s["share"] * math.exp(rng.normal(0, 0.01))
    lines = []

    def prev(y, m, d):
        m -= d
        while m < 1:
            m += 12
            y -= 1
        return y, m

    for (y, m) in W.STATEMENT_MONTHS:
        for s in stations:
            if True:
                v = vol.get((s["station"], y, m))
                if v is None:
                    g = gas.get((s["op"], 2026, 9), 0.0) * 0.985
                    v = g * W.STATE_PSIA / W.STD_PSIA * ratio[s["op"]] * s["share"]
                lines.append(dict(sy=y, sm=m, station=s["station"], shipper=s["shipper"], op=s["op"], py=y, pm=m,
                                  kind="alloc", mcf=v, energy_only=s["station"] in energy_only and (y, m) >= (2026, 7)))
        # prior-period adjustments for the two months before, at about one station in five, and at every rated
        # producer's stations in the statements that straddle the rating year's edges
        edge = (y, m) in [(2025, 10), (2026, 10)]
        for s in stations:
            for d in (1, 2):
                py, pm = prev(y, m, d)
                if (py, pm) < W.EXTRACT_FIRST:
                    continue
                want = {(2025, 10): 1, (2026, 10): 1}.get((y, m))
                force = edge and s["op"] in W.NAMES and d == want \
                    and s["share"] == max(z["share"] for z in stations if z["op"] == s["op"])
                if not (force or rng.random() < 0.10):
                    continue
                base = vol.get((s["station"], py, pm), 0.0)
                adj = base * float(rng.choice([-1, 1]) * rng.uniform(0.012, 0.045))
                lines.append(dict(sy=y, sm=m, station=s["station"], shipper=s["shipper"], op=s["op"], py=py, pm=pm,
                                  kind="ppa", mcf=adj, energy_only=False, word=PPA_WORDS[int(rng.integers(0, len(PPA_WORDS)))]))
    # the March 2026 statement re-issued as revision 2
    out = []
    for ln in lines:
        ln["rev"] = 1
        out.append(ln)
        if (ln["sy"], ln["sm"]) == (2026, 3):
            r2 = dict(ln)
            r2["rev"] = 2
            r2["mcf"] = ln["mcf"] * (1 + float(rng.normal(0, 0.004)))
            out.append(r2)
    for ln in out:
        h = hv[(ln["station"], ln["py"], ln["pm"])]
        ln["hv"] = h
        ln["mmbtu"] = ln["mcf"] * h / 1000.0
    return dict(stations=stations, lines=out, hv=hv, energy_only=energy_only, number=number)


def delivered(plant, rating_months, by="production", revisions="latest", energy="convert"):
    """Gas each rated producer delivered to the plant over the rating year, MMcf. by: production month (the reference)
    or accounting month; revisions: latest or all; energy: convert with the station's heating value, as Mcf, or drop."""
    rows = plant["lines"]
    if revisions == "latest":
        top = {}
        for ln in rows:
            top[(ln["sy"], ln["sm"])] = max(top.get((ln["sy"], ln["sm"]), 0), ln["rev"])
        rows = [ln for ln in rows if ln["rev"] == top[(ln["sy"], ln["sm"])]]
    out = {p: 0.0 for p in W.NAMES}
    for ln in rows:
        if ln["op"] not in out:
            continue
        ym = (ln["py"], ln["pm"]) if by == "production" else (ln["sy"], ln["sm"])
        if ym not in rating_months:
            continue
        if ln["energy_only"]:
            if energy == "convert":
                v = round(ln["mmbtu"], 1) * 1000.0 / ln["hv"]
            elif energy == "as_mcf":
                v = round(ln["mmbtu"], 1)
            else:
                v = 0.0
        else:
            v = round(ln["mcf"], 1)
        out[ln["op"]] += v / 1000.0
    return out
