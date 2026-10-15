"""The estimators, on plain records (the generator's or the ones parsed back from the pack): the detection curve fitted
to the controlled releases, plume attribution, and each producer's methane emitted under the golden method and under
every rung of the ladder."""
import datetime as dt
import math

import numpy as np

import world as W

M_LAT = 111_000.0
M_LON = 111_000.0 * math.cos(math.radians(36.6))


def fit_pod(releases, link="logit", wind=False):
    """Maximum likelihood fit of detected (0/1) on ln(metered rate) (and ln wind), logit or probit, by Newton steps."""
    from math import erf
    q = np.array([r["rate"] for r in releases])
    y = np.array([1.0 if r["detected"] else 0.0 for r in releases])
    cols = [np.ones(len(q)), np.log(q)] + ([np.log([r["wind"] for r in releases])] if wind else [])
    X = np.column_stack(cols)
    b = np.zeros(X.shape[1])
    for _ in range(100):
        z = X @ b
        if link == "logit":
            p = 1 / (1 + np.exp(-z))
            g = X.T @ (y - p)
            H = X.T @ (X * (p * (1 - p))[:, None])
        else:
            from scipy.stats import norm
            p = np.clip(norm.cdf(z), 1e-9, 1 - 1e-9)
            d = norm.pdf(z)
            w = d * d / (p * (1 - p))
            g = X.T @ ((y - p) * d / (p * (1 - p)))
            H = X.T @ (X * w[:, None])
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-12:
            break

    def f(rate, wind_ms=None):
        x = [1.0, math.log(rate)] + ([math.log(wind_ms)] if wind else [])
        z = float(np.dot(b, x))
        if link == "logit":
            return 1 / (1 + math.exp(-z))
        from scipy.stats import norm
        return float(norm.cdf(z))
    f.b = b
    return f


def attribute(plumes, sites, radius=W.ATTRIB_M):
    """The register site nearest each plume within the radius (or None), and the distance."""
    la = np.array([s["lat"] for s in sites])
    lo = np.array([s["lon"] for s in sites])
    out = []
    for p in plumes:
        d = np.hypot((p["lat"] - la) * M_LAT, (p["lon"] - lo) * M_LON)
        i = int(np.argmin(d))
        out.append((sites[i]["site_id"], float(d[i])) if d[i] <= radius else (None, None))
    return out


def operator_on(site, day):
    who = site["ops"][0][1]
    for eff, p in site["ops"]:
        if day >= eff:
            who = p
    return who


def tenures(site):
    out = []
    ops = site["ops"]
    for i, (eff, p) in enumerate(ops):
        end = ops[i + 1][0] if i + 1 < len(ops) else W.RATING_END + dt.timedelta(days=1)
        out.append((p, max(eff, W.RATING_START), end))
    return out


def site_campaign_values(passes, plumes, weight, floor=W.FLOOR, first_pass_only=False, sum_passes=False):
    """For each (site, campaign) imaged: the mean over its imaged passes of the weighted plume rates attributed to the
    site on that pass (plumes at or above the floor). Returns {(site, campaign): (value, day)}."""
    by_pass = {}
    for pl in plumes:
        if pl["site"] is None or pl["rate"] < floor:
            continue
        by_pass.setdefault((pl["site"], pl["campaign"], pl["line"]), []).append(pl)
    seen = {}
    for ps in passes:
        if not ps["imaged"]:
            continue
        seen.setdefault((ps["site"], ps["campaign"]), []).append(ps)
    out = {}
    for (site, camp), lst in seen.items():
        lst = sorted(lst, key=lambda z: (z["time"], z["line"]))
        if first_pass_only:
            lst = lst[:1]
        vals = [sum(weight(pl) for pl in by_pass.get((site, camp, ps["line"]), [])) for ps in lst]
        v = sum(vals) if sum_passes else sum(vals) / len(vals)
        out[(site, camp)] = (v, lst[0]["time"].date())
    return out


def campaign_hours(scheme):
    """The hours each campaign stands for: a quarter of the year each, or the days from the midpoint with the campaign
    before to the midpoint with the one after, inside the rating year."""
    if scheme == "quarter":
        return {c: W.HOURS / 4.0 for c, _, _ in W.CAMPAIGNS}
    mids = [d0 + (d1 - d0) / 2 for (_, d0, _), (_, d1, _) in zip(W.CAMPAIGNS[:-1], W.CAMPAIGNS[1:])]
    edges = [W.RATING_START] + mids + [W.RATING_END + dt.timedelta(days=1)]
    return {c: (edges[i + 1] - edges[i]).days * 24.0 for i, (c, _, _) in enumerate(W.CAMPAIGNS)}


def emitted(sites, passes, plumes, weight, coverage_zero=False, by_current_operator=False, hours="tenure", **kw):
    """Each producer's methane emitted over the rating year, tonnes: for each site and each producer that operated it,
    the mean over the campaigns imaged in that tenure of the site's campaign value (kg/h), times the tenure's hours.
    hours="quarter" or "interval" instead gives each imaged campaign its own share of the year (campaign_hours), the
    site's unimaged campaigns at the mean of its imaged ones."""
    vals = site_campaign_values(passes, plumes, weight, **kw)
    out = {p: 0.0 for p in W.NAMES}
    ch = campaign_hours(hours) if hours != "tenure" else None
    for s in sites:
        ten = tenures(s)
        if by_current_operator:
            ten = [(ten[-1][0], W.RATING_START, W.RATING_END + dt.timedelta(days=1))]
        if ch is not None:
            seen = [vals[(s["site_id"], c)][0] for c, _, _ in W.CAMPAIGNS if (s["site_id"], c) in vals]
            fill = float(np.mean(seen)) if seen else 0.0
            for c, d0, _ in W.CAMPAIGNS:
                p = operator_on(s, d0) if not by_current_operator else ten[-1][0]
                v = vals[(s["site_id"], c)][0] if (s["site_id"], c) in vals else fill
                out[p] += v * ch[c] / 1000.0
            continue
        for p, a, b in ten:
            v = []
            for c, d0, d1 in W.CAMPAIGNS:
                if not (a <= d0 < b):
                    continue
                if (s["site_id"], c) in vals:
                    v.append(vals[(s["site_id"], c)][0])
                elif coverage_zero:
                    v.append(0.0)
            if v:
                out[p] += np.mean(v) * (b - a).days * 24 / 1000.0
    return out


def carried_sources(sites, passes, plumes, duty=False, floor=W.FLOOR, join_m=40.0, weight=None):
    """The source list: each site's plumes over the four campaigns grouped by location (within 40 m), each group one
    source at its mean detected rate, carried through the producer's tenure (duty=False) or scaled by the share of
    imaged campaigns it was detected in (duty=True)."""
    site = {s["site_id"]: s for s in sites}
    imaged = {}
    for ps in passes:
        if ps["imaged"]:
            imaged.setdefault(ps["site"], set()).add(ps["campaign"])
    groups = {}
    for pl in sorted(plumes, key=lambda z: (z["site"] or "", z["campaign"], z["n"])):
        if pl["site"] is None or pl["rate"] < floor:
            continue
        gs = groups.setdefault(pl["site"], [])
        for g in gs:
            if math.hypot((pl["lat"] - g["lat"]) * M_LAT, (pl["lon"] - g["lon"]) * M_LON) <= join_m:
                g["rates"].append(pl["rate"])
                g["camps"].add(pl["campaign"])
                break
        else:
            gs.append(dict(lat=pl["lat"], lon=pl["lon"], rates=[pl["rate"]], camps={pl["campaign"]}))
    out = {p: 0.0 for p in W.NAMES}
    for sid, gs in groups.items():
        for p, a, b in tenures(site[sid]):
            for g in gs:
                r = float(np.mean([weight(dict(rate=q)) for q in g["rates"]] if weight else g["rates"]))
                f = len(g["camps"]) / max(1, len(imaged.get(sid, ()))) if duty else 1.0
                out[p] += r * f * (b - a).days * 24 / 1000.0
    return out


def intensity(em, prod):
    return {p: 100.0 * em[p] / prod[p] for p in W.NAMES}


def rated(inten, limit=W.LIMIT):
    return [p for p in W.NAMES if inten[p] <= limit]


# ------------------------------------------------------------------------------------------- on the shipped records
RATING_MONTHS = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]


def attribute_by_facility(plumes, sites):
    """Talmora's own attribution: the reported nearest facility number mapped through the register, the nearest of the
    sites sharing a number where a permit covers two."""
    by_fac = {}
    for s in sites:
        for f in s["fac"]:
            by_fac.setdefault(f, []).append(s)
    out = []
    for p in plumes:
        cand = by_fac.get(p["nf"]) if p["nf"] else None
        if not cand:
            out.append(None)
            continue
        best = min(cand, key=lambda s: math.hypot((p["lat"] - s["lat"]) * M_LAT, (p["lon"] - s["lon"]) * M_LON))
        out.append(best["site_id"])
    return out


def binned_pod(releases, edges=(0.8, 2.0, 5.0, 10.0, 20.0, 40.0, 80.0)):
    """The releases' detected share in rate bins, read as a step curve."""
    shares = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        grp = [r for r in releases if lo <= r["rate"] < hi or (hi == edges[-1] and r["rate"] == hi)]
        shares.append(sum(r["detected"] for r in grp) / len(grp))

    def f(rate, wind_ms=None):
        for (lo, hi), sh in zip(zip(edges[:-1], edges[1:]), shares):
            if rate < hi:
                return max(sh, 1e-6)
        return shares[-1]
    f.shares = shares
    return f


def produced(rows, comp, latest_only=True, convert=True, year=None, current_operator=False):
    """Tonnes of methane each producer's wells produced over the rating year: the latest report for each well and
    month, the operator of record that month, gas converted from the commission's 14.65 psia to 14.73, times the
    field's methane share in its latest composite and 19.2 kg per Mcf."""
    latest = {}
    last = {}
    for r in rows:
        if current_operator and ((r["y"], r["m"]) > last.get(r["api"], ((0, 0), None))[0]):
            last[r["api"]] = ((r["y"], r["m"]), r["op"])
        if (r["y"], r["m"]) not in RATING_MONTHS:
            continue
        k = (r["api"], r["y"], r["m"]) + (() if latest_only else (r["kind"], r["filed"]))
        if k not in latest or r["filed"] > latest[k]["filed"]:
            latest[k] = r
    out = {p: 0.0 for p in W.NAMES}
    for r in latest.values():
        op = last[r["api"]][1] if current_operator else r["op"]
        if op not in out:
            continue
        share = comp[r["field"]][year or max(comp[r["field"]])]
        mcf = r["gas"] * (W.STATE_PSIA / W.STD_PSIA if convert else 1.0)
        out[op] += mcf * share * W.KG_PER_MCF / 1000.0
    return out


def inventory(ghgrp, year=2025):
    out = {p: 0.0 for p in W.NAMES}
    for r in ghgrp:
        if r["year"] != year:
            continue
        p = [n for n in W.NAMES if r["parent"].startswith(n)][0]
        out[p] += r["ch4"]
    return out


def delivered(statements, stations, heating, by="production", revisions="latest", energy="convert"):
    """Gas each rated producer delivered to the plant over the rating year, MMcf at 14.73 psia. by: the production month
    in each line's reference, or the statement's accounting month; revisions: the latest of each statement, or all;
    energy: an energy-only line converted at the station's heating value for the month, read as Mcf, or left out."""
    rows = statements
    if revisions == "latest":
        top = {}
        for ln in rows:
            top[(ln["sy"], ln["sm"])] = max(top.get((ln["sy"], ln["sm"]), 0), ln["rev"])
        rows = [ln for ln in rows if ln["rev"] == top[(ln["sy"], ln["sm"])]]
    out = {p: 0.0 for p in W.NAMES}
    for ln in rows:
        op = stations[ln["station"]]["op"]
        if op not in out:
            continue
        ym = (ln["py"], ln["pm"]) if by == "production" else (ln["sy"], ln["sm"])
        if ym not in RATING_MONTHS:
            continue
        if ln["mcf"] is None:
            v = {"convert": lambda: ln["mmbtu"] * 1000.0 / heating[(ln["station"], ln["py"], ln["pm"])],
                 "as_mcf": lambda: ln["mmbtu"], "drop": lambda: 0.0}[energy]()
        else:
            v = ln["mcf"]
        out[op] += v / 1000.0
    return out


def lease_operator(hist, y, m, at_end=False):
    if at_end:
        return hist[-1][1]
    who = hist[0][1]
    for eff, p in hist:
        if dt.date(y, m, 1) >= eff:
            who = p
    return who


def latest_flaring(reports):
    top = {}
    for r in reports:
        k = (r["lease"], r["y"], r["m"], r["code"])
        if k not in top or r["filed"] > top[k]["filed"]:
            top[k] = r
    return list(top.values())


def flared(reports, leases, codes=("FL", "FR"), versions="latest", at_end=False):
    """Gas each rated producer flared over the rating year, MMcf: the latest report for each lease, month and code,
    each lease to its operator of record that month."""
    reps = latest_flaring(reports) if versions == "latest" else reports
    out = {p: 0.0 for p in W.NAMES}
    for r in reps:
        if (r["y"], r["m"]) not in RATING_MONTHS or r["code"] not in codes:
            continue
        op = lease_operator(leases[r["lease"]], r["y"], r["m"], at_end)
        if op in out:
            out[op] += r["mcf"] / 1000.0
    return out
