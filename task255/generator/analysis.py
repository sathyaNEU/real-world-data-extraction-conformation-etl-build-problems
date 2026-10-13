"""The golden analysis and every rung, on the records as the pool holds them. The severity curve is fitted by
maximum likelihood at 2027 cost to the closed occurrences of accident years 2014 to 2021; the golden's likelihood
carries each occurrence's deductible as left truncation and the retention as right censoring for the occurrences
that reached it, both brought to 2027 cost with the same index as the occurrence."""
import datetime as dt
import math
import re
from collections import Counter

import numpy as np
from scipy import optimize, stats

import world as W

STARTS = ([10.0, 1.5], [11.5, 1.0], [9.0, 2.2], [12.0, 0.8], [8.0, 2.8])


def fit_rows(rec):
    """The record rows the curve is fitted to: closed occurrences of the policy's accident years, with the
    recorded ground-up cost (deductible plus the pool's payments), the deductible and the retention."""
    out = []
    for r in rec:
        if r["ay"] in W.FIT_YEARS and r["status"] == "closed":
            g = round(r["ded"] + r["paid_ind"] + r["paid_def"], 2)
            out.append({"ay": r["ay"], "f": W.factor(r["ay"]), "ded": r["ded"], "ret": r["ret"], "cost": g,
                        "capped": g >= r["ret"] - 0.005})
    return out


def mle(rows, trunc=True, cens=True, trend_thresholds=True, scale=None):
    """Maximum likelihood lognormal (mu, sigma of the log of dollars at 2027 cost)."""
    f = np.array([r["f"] for r in rows])
    lx = np.log(np.array([r["cost"] for r in rows]) * f)
    ld = np.log(np.array([r["ded"] for r in rows]) * (f if trend_thresholds else 1.0))
    c = np.array([r["capped"] for r in rows]) & cens

    def nll(p):
        m, s = p[0], abs(p[1])
        z = (lx - m) / s
        ll = np.where(c, stats.norm.logsf(z), stats.norm.logpdf(z) - math.log(s) - lx)
        if trunc:
            ll = ll - stats.norm.logsf((ld - m) / s)
        return -ll.sum()

    best = None
    for st in STARTS:
        res = optimize.minimize(nll, st, method="Nelder-Mead",
                                options=dict(xatol=1e-11, fatol=1e-11, maxiter=60000, maxfev=60000))
        if best is None or res.fun < best.fun:
            best = res
    return float(best.x[0]), float(abs(best.x[1])), float(best.fun)


def mle_accident_year_dollars(rows):
    """The same likelihood written in each accident year's own dollars, the curve's log mean moving with the index:
    the thresholds are then the nominal deductible and retention. It must land on the 2027-cost fit."""
    f = np.array([r["f"] for r in rows])
    lx = np.log(np.array([r["cost"] for r in rows]))
    ld = np.log(np.array([r["ded"] for r in rows], dtype=float))
    lf = np.log(f)
    c = np.array([r["capped"] for r in rows])

    def nll(p):
        m, s = p[0] - lf, abs(p[1])
        z = (lx - m) / s
        ll = np.where(c, stats.norm.logsf(z), stats.norm.logpdf(z) - math.log(s) - lx)
        return -(ll - stats.norm.logsf((ld - m) / s)).sum()

    best = None
    for st in STARTS:
        res = optimize.minimize(nll, st, method="Nelder-Mead",
                                options=dict(xatol=1e-11, fatol=1e-11, maxiter=60000, maxfev=60000))
        if best is None or res.fun < best.fun:
            best = res
    return float(best.x[0]), float(abs(best.x[1]))


def tail_ratio(mu, sigma, amount):
    return math.exp(stats.norm.logsf((math.log(amount) - mu) / sigma)
                    - stats.norm.logsf((math.log(W.ANCHOR) - mu) / sigma))


def counts(mu, sigma, lam=None):
    lam = W.COUNT_25K if lam is None else lam
    return {a: lam * tail_ratio(mu, sigma, a) for a in W.OPTIONS}


def pick(cnt):
    for a in W.OPTIONS:
        if cnt[a] <= W.BAR:
            return a
    return None


def crossing(mu, sigma):
    g = lambda la: math.log(W.COUNT_25K) + math.log(tail_ratio(mu, sigma, math.exp(la)))
    return math.exp(optimize.brentq(g, math.log(3e4), math.log(1e10)))


RUNGS = {
    "R0": dict(trunc=False, cens=False),            # the recorded costs as a complete sample
    "R1": dict(trunc=False, cens=True),             # the capped occurrences censored, the deductible ignored
    "R2": dict(trunc=True, cens=False),             # the deductible as truncation, the capped costs read as exact
    "R3": dict(trunc=True, cens=True, trend_thresholds=False),   # both, thresholds left in each year's dollars
    "G": dict(),
}


def ladder(rows):
    out = {}
    for k, kw in RUNGS.items():
        mu, sg, _ = mle(rows, **kw)
        c = counts(mu, sg)
        out[k] = {"mu": mu, "sigma": sg, "counts": c, "pick": pick(c), "crossing": crossing(mu, sg)}
    return out


# ---------------------------------------------------------------- the asks: the rated exposure and the premiums
def norm_id(s):
    return re.sub(r"[\s\-]", "", (s or "")).upper()


def unit_key(vin, serial):
    v = norm_id(vin)
    return ("VIN", v) if len(v) == 17 else ("SERIAL", norm_id(serial))


def scheduled_units(log, at=None):
    """Units on the schedule at the rating date, one per vehicle: a vehicle's status is that of the latest unit
    number added for it (by its VIN, or its serial where it has none), so the consortium's numbers replace the
    pool's for the vehicles loaded in March 2025."""
    at = at or W.RATING_DATE
    add, gone, ident = {}, set(), {}
    for r in log:
        k = (r["member"], r["unit_no"])
        if r["type"] == "ADD" and r["effective"] <= at:
            add[k] = (r["effective"], r["entered"])
            ident[k] = unit_key(r["vin"], r["serial"])
        elif r["type"] == "DELETE" and r["effective"] <= at:
            gone.add(k)
    latest = {}
    for k, stamp in add.items():
        kk = (k[0], ident[k])
        if kk not in latest or stamp > latest[kk][0]:
            latest[kk] = (stamp, k)
    return Counter(kk[0] for kk, (_, k) in latest.items() if k not in gone)


def units_naive(log, at=None, mode="raw"):
    at = at or W.RATING_DATE
    add, gone, ident = {}, set(), {}
    for r in log:
        k = (r["member"], r["unit_no"])
        if r["type"] == "ADD" and r["effective"] <= at:
            add[k] = True
            ident[k] = (r["vin"], r["serial"])
        elif r["type"] == "DELETE" and r["effective"] <= at:
            gone.add(k)
    live = [k for k in add if k not in gone]
    if mode == "raw":
        return Counter(k[0] for k in live)
    if mode == "dedup_live":
        return Counter(m for m, _ in {(k[0], unit_key(*ident[k])) for k in live})
    if mode == "raw_vin":
        return Counter(m for m, _ in {(k[0], ident[k][0] if ident[k][0] else ("unit", k[1])) for k in live})
    if mode == "vin_only":
        return Counter(m for m, _ in {(k[0], norm_id(ident[k][0])) for k in live})
    raise ValueError(mode)


def premium(toe, units, attachment):
    gl, al = W.QUOTES[attachment]
    return gl * toe / 1000.0 + al * units


def by_class(per_member, kind_of):
    out = Counter()
    for m, v in per_member.items():
        out[kind_of[m]] += v
    return out


# ---------------------------------------------------------------- the whole world and the figures the write-up states
def world_state():
    mem, occ = W.world()
    W.member_details(W.stream(3), mem)
    rec = W.development(W.stream(4), mem, occ)
    units = W.fleets(W.stream(5), mem)
    dec = W.declarations(W.stream(6), mem)
    log = W.schedule_log(W.stream(7), mem, units)
    return {"mem": mem, "occ": occ, "rec": rec, "units": units, "dec": dec, "log": log}


def figures(st):
    mem, rec, dec, log = st["mem"], st["rec"], st["dec"], st["log"]
    rows = fit_rows(rec)
    mu, sg, _ = mle(rows)
    cnt = counts(mu, sg)
    call = pick(cnt)
    i = W.OPTIONS.index(call)
    runner = W.OPTIONS[i - 1]
    kind = {m["no"]: m["kind"] for m in mem}
    toe = {d["member"]: d["toe"] for d in dec}
    units = scheduled_units(log)
    T, U = sum(toe.values()), sum(units.values())
    prem = {str(a): round(premium(T, U, a)) for a in W.OPTIONS}
    by = {}
    for k in sorted(set(kind[m] for m in toe)):
        ms = [m for m in toe if kind[m] == k]
        by[k] = {"members": len(ms), "toe_000": round(sum(toe[m] for m in ms) / 1000),
                 "units": sum(units.get(m, 0) for m in ms)}
    lad = ladder(rows)
    return {
        "call": {"attachment": call, "runner_up": runner, "count": round(cnt[call], 2),
                 "runner_up_count": round(cnt[runner], 2),
                 "flip_count_25k_runner_passes": round(W.COUNT_25K / cnt[runner], 1),
                 "flip_count_25k_call_fails": round(W.COUNT_25K / cnt[call], 1)},
        "counts": {str(a): cnt[a] for a in W.OPTIONS},
        "counts_2dp": {str(a): round(cnt[a], 2) for a in W.OPTIONS},
        "curve": {"mu": mu, "sigma": sg, "mu_2dp": round(mu, 2), "sigma_2dp": round(sg, 2)},
        "fit": {"n": len(rows), "capped": sum(r["capped"] for r in rows),
                "capped_250k": sum(1 for r in rows if r["capped"] and r["ret"] == 250_000),
                "capped_500k": sum(1 for r in rows if r["capped"] and r["ret"] == 500_000)},
        "premiums": prem,
        "exposure": {"toe": T, "toe_000": round(T / 1000), "units": U, "members": len(toe)},
        "by_class": by,
        "rungs": {k: {"mu": v["mu"], "sigma": v["sigma"], "pick": v["pick"],
                      "count_3m": v["counts"][3_000_000], "count_4m": v["counts"][4_000_000]} for k, v in lad.items()},
        "count_25k": W.COUNT_25K,
        "anchor": W.ANCHOR,
        "retentions": sorted(set(W.RETENTION.values())),
        "fit_sources": {"legacy": sum(1 for r in rec if r["ay"] in W.FIT_YEARS and r["system"] == "legacy"),
                        "current": sum(1 for r in rec if r["ay"] in W.FIT_YEARS and r["system"] == "current")},
        "attachments": list(W.OPTIONS),
        "attachments_millions": ["%.1f million" % (a / 1e6) for a in W.OPTIONS],
    }
