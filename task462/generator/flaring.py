"""The commission's flaring and venting reports by lease and month, the lease register (each lease's operator with the
date it took over), and the commission's monthly basin summary. From the January 2026 reports the commission splits
flared gas into FL (emergency or upset) and FR (routine)."""
import datetime as dt

import numpy as np

import production as PR
import world as W


def build(seed, site_list, well_list, rows, other_wells, other_rows):
    rng = np.random.default_rng(seed + W.FLARING_STREAM)
    site = {s["site_id"]: s for s in site_list}
    number = {p[0]: p[1] for p in W.PRODUCERS}
    number.update({o[0]: o[1] for o in W.OTHER_OPERATORS})
    # leases: each rated producer's pads one or two to a lease; other operators' wells by operator and field
    leases, lease_of = [], {}
    seq = 61_000
    pads = sorted({w["site"] for w in well_list})
    i = 0
    while i < len(pads):
        group = pads[i:i + (2 if rng.random() < 0.35 else 1)]
        if len({site[p]["producer"] for p in group}) > 1 or len({tuple(site[p]["ops"]) for p in group}) > 1:
            group = group[:1]
        i += len(group)
        s0 = site[group[0]]
        seq += int(rng.integers(2, 30))
        lid = "L-%06d" % seq
        hist = [(dt.date(2016 + int(rng.integers(0, 8)), int(rng.integers(1, 13)), 1), s0["ops"][0][1])] + \
               [(eff, p) for eff, p in s0["ops"][1:]]
        leases.append(dict(lease=lid, name="%s %s Unit" % (s0["producer"].split()[0], group[0][-4:]), hist=hist,
                           field=None))
        for p in group:
            lease_of[p] = lid
    for w in other_wells:
        key = (w["op"], w["field"])
        if key not in lease_of:
            seq += int(rng.integers(2, 30))
            lid = "L-%06d" % seq
            leases.append(dict(lease=lid, name="%s %s" % (w["op"].split()[0], w["field"]),
                               hist=[(dt.date(2012 + int(rng.integers(0, 10)), int(rng.integers(1, 13)), 1), w["op"])], field=w["field"]))
            lease_of[key] = lid
    by_lease = {}
    latest = {}
    for r in rows + other_rows:
        k = (r["api"], r["y"], r["m"])
        if k not in latest or r["filed"] > latest[k]["filed"]:
            latest[k] = r
    for r in latest.values():
        lid = lease_of[r["site"]] if r["site"] else lease_of[(r["op"], r["field"])]
        by_lease[(lid, r["y"], r["m"])] = by_lease.get((lid, r["y"], r["m"]), 0.0) + r["gas"]
    frac = {p: float(rng.uniform(0.006, 0.026)) for p in list(number)}
    routine = {p: float(rng.uniform(0.60, 0.78)) for p in list(number)}
    vent = {p: float(rng.uniform(0.0015, 0.0055)) for p in list(number)}
    lease_op0 = {L["lease"]: L["hist"][0][1] for L in leases}
    reports = []
    for (lid, y, m), g in sorted(by_lease.items()):
        op = lease_op0[lid]
        f = g * frac[op] * float(np.exp(rng.normal(0, 0.35)))
        if rng.random() < 0.18:
            f = 0.0
        filed = dt.date(y + (m == 12), m % 12 + 1, 1) + dt.timedelta(days=int(rng.integers(20, 45)))
        if (y, m) < W.CODE_SWITCH:
            items = [("FL", f)]
        else:
            r = routine[op] * float(np.clip(rng.normal(1, 0.08), 0.7, 1.3))
            r = min(r, 0.97)
            items = [("FL", f * (1 - r)), ("FR", f * r)]
        items.append(("VT", g * vent[op] * float(np.exp(rng.normal(0, 0.4)))))
        for code, v in items:
            if v < 0.5:
                continue
            rec = dict(lease=lid, y=y, m=m, code=code, mcf=round(v), kind="O", filed=filed)
            reports.append(rec)
            if rng.random() < 0.03:
                a = dict(rec)
                a["mcf"] = round(v * float(rng.uniform(0.85, 1.12)))
                a["kind"] = "A"
                a["filed"] = filed + dt.timedelta(days=int(rng.integers(30, 120)))
                reports.append(a)
    pull = W.PACK_DATE - dt.timedelta(days=3)
    reports = [r for r in reports if r["filed"] <= pull]
    return dict(leases=leases, reports=reports, number=number)


def latest_reports(reports):
    top = {}
    for r in reports:
        k = (r["lease"], r["y"], r["m"], r["code"])
        if k not in top or r["filed"] > top[k]["filed"]:
            top[k] = r
    return list(top.values())


def operator_of(lease, y, m, at_end=False):
    hist = sorted(lease["hist"])
    if at_end:
        return hist[-1][1]
    who = hist[0][1]
    for eff, p in hist:
        if dt.date(y, m, 1) >= eff:
            who = p
    return who


def basin_summary(fl):
    out = {}
    for r in latest_reports(fl["reports"]):
        k = (r["y"], r["m"])
        a = out.setdefault(k, {"flared": 0, "vented": 0, "n": set()})
        if r["code"] in ("FL", "FR"):
            a["flared"] += r["mcf"]
        else:
            a["vented"] += r["mcf"]
        a["n"].add(r["lease"])
    return out


def flared(fl, rating_months, codes=("FL", "FR"), versions="latest", at_end=False):
    """Gas each rated producer flared over the rating year, MMcf."""
    leases = {L["lease"]: L for L in fl["leases"]}
    reps = latest_reports(fl["reports"]) if versions == "latest" else fl["reports"]
    out = {p: 0.0 for p in W.NAMES}
    for r in reps:
        if (r["y"], r["m"]) not in rating_months or r["code"] not in codes:
            continue
        op = operator_of(leases[r["lease"]], r["y"], r["m"], at_end)
        if op in out:
            out[op] += r["mcf"] / 1000.0
    return out
