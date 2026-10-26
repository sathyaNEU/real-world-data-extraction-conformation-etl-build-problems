"""The golden analysis and every rung, on the records as the pool holds them. Severity is fitted by maximum likelihood
at 2027 cost to every occurrence of accident years 2014 to 2021 in the pool's record, each occurrence's deductible
carried as left truncation and the retention as right censoring for the occurrences that reached it, both brought to
2027 cost with the same index as the occurrence; the golden fits law enforcement liability and the other four coverage
parts apart and carries each group's projected 2027 occurrences above $25,000 by its own curve."""
import datetime as dt
import math
import re
from collections import Counter

import numpy as np
from scipy import optimize, stats

import world as W

STARTS = ([10.0, 1.5], [11.5, 1.0], [9.0, 2.2], [12.0, 0.8], [8.0, 2.8])
GROUPS = {"LE": ("LE",), "OT": ("GL", "AL", "PO", "EP")}


def anchors():
    return {"LE": W.COUNT_LE, "OT": W.COUNT_OT}


def fit_rows(rec, closed_only=False, open_at="incurred"):
    """The record rows severity is fitted to: every occurrence of the policy's accident years in the pool's record,
    with its recorded ground-up cost (the deductible plus what the pool has paid and still reserves), the deductible,
    the retention and the coverage part; closed_only keeps the closed files alone, and open_at="paid" reads an open
    file at its payments to date."""
    out = []
    for r in rec:
        if r["ay"] not in W.FIT_YEARS or r["status"] == "untendered":
            continue
        if closed_only and r["status"] != "closed":
            continue
        g = r["ded"] + r["paid_ind"] + r["paid_def"]
        if r["status"] == "open" and open_at == "incurred":
            g += r["res_ind"] + r["res_def"]
        g = round(g, 2)
        out.append({"ay": r["ay"], "f": W.factor(r["ay"]), "ded": r["ded"], "ret": r["ret"], "cost": g,
                    "capped": g >= r["ret"] - 0.005, "open": r["status"] == "open", "part": r["part"]})
    return out


def _arrays(rows, trend_thresholds=True, trend_retention=True):
    f = np.array([r["f"] for r in rows])
    lx = np.log(np.array([r["cost"] for r in rows]) * f)
    ld = np.log(np.array([r["ded"] for r in rows]) * (f if trend_thresholds else 1.0))
    return f, lx, ld


def mle(rows, trunc=True, cens=True, trend_thresholds=True):
    """Maximum likelihood lognormal (mu, sigma of the log of dollars at 2027 cost) and the minimised negative log
    likelihood."""
    f, lx, ld = _arrays(rows, trend_thresholds)
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


def mle_shift(rows):
    """The rival with one spread: law enforcement's log mean shifted from the other parts', a common sigma."""
    f, lx, ld = _arrays(rows)
    c = np.array([r["capped"] for r in rows])
    le = np.array([r["part"] in GROUPS["LE"] for r in rows])

    def nll(p):
        m = np.where(le, p[0] + p[2], p[0])
        s = abs(p[1])
        z = (lx - m) / s
        ll = np.where(c, stats.norm.logsf(z), stats.norm.logpdf(z) - math.log(s) - lx) - stats.norm.logsf((ld - m) / s)
        return -ll.sum()

    best = None
    for st in STARTS:
        res = optimize.minimize(nll, st + [0.5], method="Nelder-Mead",
                                options=dict(xatol=1e-11, fatol=1e-11, maxiter=80000, maxfev=80000))
        if best is None or res.fun < best.fun:
            best = res
    m0, s, d = best.x
    return {"OT": (float(m0), float(abs(s))), "LE": (float(m0 + d), float(abs(s)))}, float(best.fun)


def mle_accident_year_dollars(rows):
    """The same likelihood written in each accident year's own dollars, the log mean moving with the index: the
    thresholds are then the nominal deductible and retention. It must land on the 2027-cost fit."""
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


def counts_pooled(mu, sigma, lam=None):
    lam = W.COUNT_25K if lam is None else lam
    return {a: lam * tail_ratio(mu, sigma, a) for a in W.OPTIONS}


def counts_groups(curves, anc=None):
    anc = anc or anchors()
    return {a: sum(anc[g] * tail_ratio(*curves[g], a) for g in GROUPS) for a in W.OPTIONS}


LIMIT = 10_000_000     # each quoted layer: $10,000,000 for each occurrence above its attachment


def lev(mu, sigma, d):
    """Limited expected value of a lognormal cost at d, E[min(X, d)]."""
    return (math.exp(mu + sigma * sigma / 2) * stats.norm.cdf((math.log(d) - mu - sigma * sigma) / sigma)
            + d * stats.norm.sf((math.log(d) - mu) / sigma))


def layer_per_anchor(mu, sigma, a):
    """Expected cost a quoted layer pays per occurrence costing more than $25,000."""
    return (lev(mu, sigma, a + LIMIT) - lev(mu, sigma, a)) / W.lognormal_sf(W.ANCHOR, mu, sigma)


def layer_losses(curves, anc=None):
    anc = anc or anchors()
    return {a: sum(anc[g] * layer_per_anchor(*curves[g], a) for g in GROUPS) for a in W.OPTIONS}


def group_fits(rows, **kw):
    out = {}
    for g, parts in GROUPS.items():
        rr = [r for r in rows if r["part"] in parts]
        m, s, n = mle(rr, **kw)
        out[g] = (m, s)
        out[g + "_nll"] = n
        out[g + "_n"] = len(rr)
        out[g + "_capped"] = sum(r["capped"] for r in rr)
    return out


def pick(cnt):
    for a in W.OPTIONS:
        if cnt[a] <= W.BAR:
            return a
    return None


def crossing(cnt_fn):
    g = lambda la: math.log(cnt_fn(math.exp(la)))
    return math.exp(optimize.brentq(g, math.log(3e4), math.log(1e10)))


def golden(rec):
    rows = fit_rows(rec)
    fits = group_fits(rows)
    curves = {g: fits[g] for g in GROUPS}
    return rows, fits, curves, counts_groups(curves)


def ladder(rec):
    """Every rung on the record of 2014 to 2021: one curve over the pooled record under each handling of the floor
    and the ceiling, the one-spread rival, the curve per group on the closed files, with the thresholds nominal, with
    a curve per coverage part, and the golden."""
    rows, closed = fit_rows(rec), fit_rows(rec, closed_only=True)
    out = {}
    for k, kw in (("R0", dict(trunc=False, cens=False)), ("R1", dict(trunc=False)), ("R2", dict(cens=False)),
                  ("R3", dict())):
        m, s, _ = mle(rows, **kw)
        out[k] = {"curves": {"pooled": (m, s)}, "counts": counts_pooled(m, s)}
    sh, _ = mle_shift(rows)
    out["shift"] = {"curves": sh, "counts": counts_groups(sh)}
    for k, rr, kw in (("G_closed", closed, {}), ("G_nominal", rows, dict(trend_thresholds=False))):
        f = group_fits(rr, **kw)
        cv = {g: f[g] for g in GROUPS}
        out[k] = {"curves": cv, "counts": counts_groups(cv)}
    # a curve per coverage part, the other parts weighted by their share of the record's occurrences above $25,000
    parts = {}
    for p in W.PARTS:
        m, s, _ = mle([r for r in rows if r["part"] == p])
        parts[p] = (m, s)
    oth = GROUPS["OT"]
    n25 = {p: sum(1 for r in rows if r["part"] == p and r["cost"] * r["f"] > W.ANCHOR) for p in oth}
    tot = sum(n25.values())
    c5 = {a: W.COUNT_LE * tail_ratio(*parts["LE"], a)
          + sum(W.COUNT_OT * n25[p] / tot * tail_ratio(*parts[p], a) for p in oth) for a in W.OPTIONS}
    out["parts5"] = {"curves": parts, "counts": c5}
    out["parts5"]["layer"] = {a: W.COUNT_LE * layer_per_anchor(*parts["LE"], a)
                              + sum(W.COUNT_OT * n25[p] / tot * layer_per_anchor(*parts[p], a) for p in oth)
                              for a in W.OPTIONS}
    _, _, cv, cg = golden(rec)
    out["G"] = {"curves": cv, "counts": cg}
    for k, v in out.items():
        v["pick"] = pick(v["counts"])
        if "layer" not in v:
            cvs = v["curves"]
            v["layer"] = ({a: W.COUNT_25K * layer_per_anchor(*cvs["pooled"], a) for a in W.OPTIONS} if "pooled" in cvs
                          else layer_losses(cvs))
    return out


# ---------------------------------------------------------------- the asks: the rated exposure and the premiums
def norm_id(s):
    return re.sub(r"[\s\-]", "", (s or "")).upper()


def unit_key(vin, serial):
    v = norm_id(vin)
    return ("VIN", v) if len(v) == 17 else ("SERIAL", norm_id(serial))


def scheduled_units(log, at=None, leaving=()):
    """Units on the schedule at the rating date, one per vehicle: a vehicle's record is the latest unit number added
    for it (by its VIN, or its serial where it has none), so the consortium's numbers replace the pool's for the
    vehicles loaded in March 2024; the vehicle belongs to the member on that number's latest row in effect, so a unit
    another member bought inside the pool counts for its buyer; members leaving before 2027 are not rated."""
    at = at or W.RATING_DATE
    add, gone, ident, owner = {}, set(), {}, {}
    for r in sorted(log, key=lambda r: (r["effective"], r["entered"])):
        if r["effective"] > at:
            continue
        k = r["unit_no"]
        if r["type"] == "ADD":
            add[k] = (r["effective"], r["entered"])
            ident[k] = unit_key(r["vin"], r["serial"])
        elif r["type"] == "DELETE":
            gone.add(k)
        owner[k] = r["member"]
    latest = {}
    for k, stamp in add.items():
        if ident[k] not in latest or stamp > latest[ident[k]][0]:
            latest[ident[k]] = (stamp, k)
    return Counter(owner[k] for _, (_, k) in latest.items() if k not in gone and owner[k] not in leaving)


def units_naive(log, at=None, mode="raw"):
    at = at or W.RATING_DATE
    add, gone, ident, add_stamp = {}, set(), {}, {}
    for r in log:
        k = (r["member"], r["unit_no"])
        if r["type"] == "ADD" and r["effective"] <= at:
            add[k] = True
            add_stamp[k] = (r["effective"], r["entered"])
            ident[k] = (r["vin"], r["serial"])
        elif r["type"] == "DELETE" and r["effective"] <= at:
            gone.add(k)
    live = [k for k in add if k not in gone]
    if mode == "raw":
        return Counter(k[0] for k in live)
    if mode == "add_member":
        # loop 1's reading: a vehicle's latest number added under the member that added it, gone if deleted there
        latest = {}
        for k in add:
            kk = (k[0], unit_key(*ident[k]))
            if kk not in latest or add_stamp[k] > latest[kk][0]:
                latest[kk] = (add_stamp[k], k)
        return Counter(kk[0] for kk, (_, k) in latest.items() if k not in gone)
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
    W.consortium(mem, units)
    dec = W.notices_and_redeclarations(W.stream(8), mem, W.declarations(W.stream(6), mem))
    log = W.schedule_log(W.stream(7), mem, units)
    return {"mem": mem, "occ": occ, "rec": rec, "units": units, "dec": dec, "log": log}


def figures(st):
    mem, rec, dec, log = st["mem"], st["rec"], st["dec"], st["log"]
    rows, fits, curves, cnt = golden(rec)
    call = pick(cnt)
    i = W.OPTIONS.index(call)
    runner = W.OPTIONS[i - 1]
    m0, s0, n0 = mle(rows)
    _, nsh = mle_shift(rows)
    n1 = fits["LE_nll"] + fits["OT_nll"]
    kind = {m["no"]: m["kind"] for m in mem}
    toe = {k: d["toe"] for k, d in W.rated(dec, mem).items()}
    leaving = {m["no"] for m in mem if m.get("withdraws")}
    units = scheduled_units(log, leaving=leaving)
    T, U = sum(toe.values()), sum(units.values())
    prem = {str(a): round(premium(T, U, a)) for a in W.OPTIONS}
    by = {}
    for k in sorted(set(kind[m] for m in toe)):
        ms = [m for m in toe if kind[m] == k]
        by[k] = {"members": len(ms), "toe_000": round(sum(toe[m] for m in ms) / 1000),
                 "units": sum(units.get(m, 0) for m in ms)}
    lad = ladder(rec)
    lay = layer_losses(curves)
    r1, r2 = W.RETENTION[W.FIT_YEARS[0]], W.RETENTION[W.FIT_YEARS[-1]]
    return {
        "call": {"attachment": call, "runner_up": runner, "count": round(cnt[call], 1),
                 "runner_up_count": round(cnt[runner], 1)},
        "counts": {str(a): cnt[a] for a in W.OPTIONS},
        "counts_1dp": {str(a): round(cnt[a], 1) for a in W.OPTIONS},
        "curves": {g: {"mu": curves[g][0], "sigma": curves[g][1], "mu_2dp": round(curves[g][0], 2),
                       "sigma_2dp": round(curves[g][1], 2), "n": fits[g + "_n"], "capped": fits[g + "_capped"]}
                   for g in GROUPS},
        "pooled": {"mu_2dp": round(m0, 2), "sigma_2dp": round(s0, 2), "pick": lad["R3"]["pick"],
                   "count_call": round(lad["R3"]["counts"][lad["R3"]["pick"]], 1)},
        "lr": {"pooled": round(2 * (n0 - n1), 1), "one_spread": round(2 * (nsh - n1), 1)},
        "anchors": {"LE": W.COUNT_LE, "OT": W.COUNT_OT, "all": W.COUNT_25K},
        "fit": {"n": len(rows), "capped": sum(r["capped"] for r in rows),
                "capped_r1": sum(1 for r in rows if r["capped"] and r["ret"] == r1),
                "capped_r2": sum(1 for r in rows if r["capped"] and r["ret"] == r2),
                "open": sum(r["open"] for r in rows), "closed": sum(not r["open"] for r in rows)},
        "premiums": prem,
        "layer_loss": {str(a): lay[a] for a in W.OPTIONS},
        "layer_loss_100k": {str(a): int(round(lay[a] / 1e5) * 100_000) for a in W.OPTIONS},
        "exposure": {"toe": T, "toe_000": round(T / 1000), "units": U, "members": len(toe)},
        "by_class": by,
        "rungs": {k: {"pick": v["pick"], "count_3m": v["counts"][3_000_000], "count_4m": v["counts"][4_000_000]}
                  for k, v in lad.items()},
        "anchor": W.ANCHOR,
        "layer_limit": LIMIT,
        "retentions": sorted(set(W.RETENTION.values())),
        "fit_sources": {"legacy": sum(1 for r in rec if r["ay"] in W.FIT_YEARS and r["system"] == "legacy"),
                        "current": sum(1 for r in rec if r["ay"] in W.FIT_YEARS and r["system"] == "current")},
        "attachments": list(W.OPTIONS),
        "attachments_millions": ["%.1f million" % (a / 1e6) for a in W.OPTIONS],
    }
