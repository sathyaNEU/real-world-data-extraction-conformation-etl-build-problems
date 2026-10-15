"""The wells behind the producers' gas: each well pad's wells, their monthly gas, oil and water as the operators reported
them to the State Oil and Gas Commission (amended reports filed later for some months), the operator of record each
month, and each field's gas composition."""
import datetime as dt
import math

import numpy as np

import basin as B
import world as W

MONTHS = [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 10)]          # the extract: July 2025 on
RATING_MONTHS = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]


def mdays(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def wells(rng, site_list):
    """Wells on each pad: API number, the pad, the field, a first-month rate and a decline."""
    fields = {p[0]: p[5] for p in W.PRODUCERS}
    out = []
    county = {"Fenholt Bend": "117", "East Tollaver": "119", "Pinyon Draw": "121", "Brushy Mesa": "117",
              "Lechuza Creek": "125", "Anchell Flats": "121", "Corran Ridge": "119", "Sotol Wash": "125",
              "Sunmere Dome": "123"}
    seq = 10_000
    for s in sorted(site_list, key=lambda z: z["site_id"]):
        if s["kind"] != "well pad":
            continue
        fl = fields[s["producer"]]
        u = rng.random()
        acc = 0.0
        field = fl[-1][0]
        for f, sh in fl:
            acc += sh
            if u < acc:
                field = f
                break
        for j in range(int(rng.integers(2, 9))):
            seq += int(rng.integers(3, 40))
            out.append(dict(api="35-%s-%05d" % (county[field], seq % 100_000), site=s["site_id"], field=field,
                            q0=float(rng.lognormal(math.log(1.0), 0.6)), dec=float(rng.uniform(0.008, 0.03)),
                            oil=float(rng.lognormal(math.log(0.012), 0.5)), water=float(rng.lognormal(math.log(0.03), 0.5)),
                            name="%s %d-%dH" % (s["site_id"][-3:], int(rng.integers(1, 36)), j + 1)))
    return out


def other_wells(seed):
    """Wells of the basin's operators outside the rating, on their own random stream."""
    rng = np.random.default_rng(seed + 12)
    out = []
    flist = sorted(B.FIELD_CH4)
    for name, num, n in W.OTHER_OPERATORS:
        for j in range(n):
            f = flist[int(rng.integers(0, len(flist)))]
            out.append(dict(api="35-%s-%05d" % (("117", "119", "121", "123", "125")[int(rng.integers(0, 5))], int(rng.integers(20_000, 99_999))),
                            site=None, op=name, field=f, q0=float(rng.lognormal(math.log(0.9), 0.6)), dec=float(rng.uniform(0.008, 0.03)),
                            oil=float(rng.lognormal(math.log(0.015), 0.5)), water=float(rng.lognormal(math.log(0.04), 0.5)),
                            name="%s %d-%dH" % (name.split()[0].upper()[:6], int(rng.integers(1, 36)), j + 1)))
    rows = []
    for w in out:
        for k, (y, m) in enumerate(MONTHS):
            days = mdays(y, m)
            down = 0 if rng.random() > 0.1 else int(rng.integers(1, 15))
            gas = w["q0"] * 220 * math.exp(-w["dec"] * k) * (days - down) * math.exp(rng.normal(0, 0.08))
            filed = dt.date(y + (m == 12), m % 12 + 1, 1) + dt.timedelta(days=int(rng.integers(30, 50)))
            rows.append(dict(api=w["api"], name=w["name"], field=w["field"], site=None, y=y, m=m, op=w["op"],
                             gas=round(gas), oil=round(gas * w["oil"]), water=round(gas * w["water"]), days=days - down,
                             kind="O", filed=filed))
    pull = W.PACK_DATE - dt.timedelta(days=3)
    return out, [r for r in rows if r["filed"] <= pull]


def monthly(rng, site_list, well_list):
    """Each well's reported gas (Mcf at the state's 14.65 psia), oil and water by month, scaled so each producer's
    own wells produce its rating-year gas; the operator of record each month; amended reports."""
    site = {s["site_id"]: s for s in site_list}
    raw = {}
    for w in well_list:
        for k, (y, m) in enumerate(MONTHS):
            days = mdays(y, m)
            down = 0 if rng.random() > 0.08 else int(rng.integers(1, 12))
            g = w["q0"] * math.exp(-w["dec"] * k) * (days - down) * math.exp(rng.normal(0, 0.06))
            raw[(w["api"], y, m)] = (g, days - down)
    # scale per producer (by the pad's producer at the start of the rating year) to the rating-year target
    adj = np.random.default_rng(W.SEED + 13).uniform(0.985, 1.015, len(W.PRODUCERS))
    target = {p[0]: p[4] * 1e6 * float(a) for p, a in zip(W.PRODUCERS, adj)}
    have = {p: 0.0 for p in W.NAMES}
    for w in well_list:
        for (y, m) in RATING_MONTHS:
            have[site[w["site"]]["producer"]] += raw[(w["api"], y, m)][0]
    scale = {p: target[p] / have[p] for p in W.NAMES}
    rows = []
    for w in well_list:
        s = site[w["site"]]
        for (y, m) in MONTHS:
            g, d = raw[(w["api"], y, m)]
            gas = g * scale[s["producer"]]
            op = B.operator_on(s, dt.date(y, m, 1))
            filed = dt.date(y + (m == 12), m % 12 + 1, 1) + dt.timedelta(days=int(rng.integers(30, 46)))
            rec = dict(api=w["api"], name=w["name"], field=w["field"], site=w["site"], y=y, m=m, op=op,
                       gas=round(gas), oil=round(gas * w["oil"]), water=round(gas * w["water"]), days=d,
                       kind="O", filed=filed)
            rows.append(rec)
            if rng.random() < 0.035:
                amend = dict(rec)
                amend["gas"] = round(gas * float(rng.uniform(0.90, 1.07)))
                amend["oil"] = round(amend["gas"] * w["oil"])
                amend["kind"] = "A"
                amend["filed"] = filed + dt.timedelta(days=int(rng.integers(40, 150)))
                rows.append(amend)
    pull = W.PACK_DATE - dt.timedelta(days=3)
    return [r for r in rows if r["filed"] <= pull]


def methane_produced(rows, sites=None, by_current_operator=False, latest_only=True, convert=True):
    """Tonnes of methane each producer's wells produced in the rating year: the latest report for each well and month,
    the operator of record that month, gas at 14.73 psia times the field's methane share times 19.2 kg per Mcf."""
    latest = {}
    for r in rows:
        if (r["y"], r["m"]) not in RATING_MONTHS:
            continue
        k = (r["api"], r["y"], r["m"])
        if not latest_only:
            k = k + (r["kind"],)
        if k not in latest or r["filed"] > latest[k]["filed"]:
            latest[k] = r
    cur = {}
    if by_current_operator:
        for s in sites:
            cur[s["site_id"]] = s["ops"][-1][1]
    out = {p: 0.0 for p in W.NAMES}
    for r in latest.values():
        if r["op"] not in out:
            continue
        mcf = r["gas"] * (W.STATE_PSIA / W.STD_PSIA if convert else 1.0)
        op = cur.get(r["site"], r["op"]) if by_current_operator else r["op"]
        out[op] += mcf * B.FIELD_CH4[r["field"]] * W.KG_PER_MCF / 1000.0
    return out
