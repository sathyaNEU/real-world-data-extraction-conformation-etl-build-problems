"""The analysis: the estimand executed literally, the ladder's rungs, and the three asks' answers.

The golden is `group_figure`: for each trading unit, the per-posting rate at which its postings trip the
monitoring ruleset, recovered from the voucher-level indicator by maximum likelihood on that unit's own
entries, times that unit's postings; summed to the group. Unit figures round to the nearest hundred and the
group figure to the nearest thousand, each from its own unrounded value.
"""
import datetime as dt

import numpy as np

import asks as A
import estimate as E
import ledger as L
import world as W

UBIN, GBIN = 100, 1_000
QUARTER = {p: (p - 1) // 3 + 1 for p in range(1, 13)}


# ---------------------------------------------------------------- the call

def unit_figures(sim):
    """Per unit: postings, entries, flagged entries, the recovered figure and its graded rounding."""
    out = {}
    for code, _o, _n, _k, _c in W.UNITS:
        d = sim["FY26"]["by_unit"][code]
        k, f = d["k"], d["flag"]
        T = int(k.sum())
        lic = E.licensed(k, f)
        out[code] = dict(postings=T, entries=int(len(k)), flagged=int(f.sum()),
                         trips=int(d["trips"].sum()), raw=lic["mle"],
                         graded=int(round(lic["mle"] / UBIN) * UBIN), licensed=lic)
    return out


def group_figure(sim):
    """The golden: the sum of the unrounded unit figures, graded to the nearest thousand."""
    u = unit_figures(sim)
    raw = sum(v["raw"] for v in u.values())
    return dict(raw=raw, graded=int(round(raw / GBIN) * GBIN),
                max_items=int(max(int(sim["FY26"]["by_unit"][c]["k"].max())
                                  for c in sim["FY26"]["by_unit"])),
                postings=sum(v["postings"] for v in u.values()),
                entries=sum(v["entries"] for v in u.values()),
                flagged=sum(v["flagged"] for v in u.values()),
                trips=sum(v["trips"] for v in u.values()),
                units=u)


def rungs(sim):
    """Every route a competent analyst takes, as a figure on the graded quantity."""
    g = group_figure(sim)
    k = np.concatenate([sim["FY26"]["by_unit"][c]["k"] for c in sim["FY26"]["by_unit"]])
    f = np.concatenate([sim["FY26"]["by_unit"][c]["flag"] for c in sim["FY26"]["by_unit"]])
    n, T, flags = len(k), int(k.sum()), int(f.sum())
    kbar = T / n
    p = flags / n
    r_agg = 1.0 - (1.0 - p) ** (1.0 / kbar)
    pooled = E.licensed(k, f)
    return {
        "rung0_flagged_entries": float(flags),
        "rung1_entry_rate_grossed_up": flags / n * T,
        "rung2_inversion_on_mean_entry_size": r_agg * T,
        "rung3_golden": g["raw"],
        "postings_on_flagged_vouchers": float(int(k[f == 1].sum())),
        "pooled_one_group_rate": pooled["mle"],
        "pooled_mom": pooled["mom"],
        "pooled_cloglog": pooled["cloglog"],
    }


def per_line_reading(sim, table):
    """SF1: reading `posting` as a ledger line. It is ruled out by the dictionary, not by convergence:
    the figure it gives is about half the golden and rounds to a different bin."""
    lines_by = {}
    for r in table:
        lines_by.setdefault(r["unit_now"], []).append(r["lines"])
    total = 0.0
    for code, _o, _n, _k, _c in W.UNITS:
        d = sim["FY26"]["by_unit"][code]
        lines = np.array(lines_by[code], dtype=np.int64)
        total += E.recover_unit(lines, d["flag"]) * lines.sum()
    return total


# ---------------------------------------------------------------- ask 1

def ask1(accr, control):
    """Per unit: the subledger's closing accrual, the ledger control account, the difference and what
    makes it up."""
    sub = A.accrual_balance(accr, by="unit_code")
    led = A.accrual_balance(accr, by="posted_to")
    grni = {u: g for u, _a, g, _t in control}
    ctl = {u: t for u, _a, _g, t in control}
    rows = {}
    for code, _o, _n, _k, _c in W.UNITS:
        s_, l_ = sub.get(code, 0.0), led.get(code, 0.0)
        rows[code] = dict(subledger=round(s_, 2), control=round(ctl[code], 2),
                          difference=round(ctl[code] - s_, 2),
                          grni=round(grni[code], 2), misposted=round(l_ - s_, 2))
    rows["GROUP"] = dict(
        subledger=round(sum(v["subledger"] for k, v in rows.items() if k != "GROUP"), 2),
        control=round(sum(v["control"] for k, v in rows.items() if k != "GROUP"), 2),
        difference=round(sum(v["difference"] for k, v in rows.items() if k != "GROUP"), 2),
        grni=round(sum(v["grni"] for k, v in rows.items() if k != "GROUP"), 2),
        misposted=round(sum(v["misposted"] for k, v in rows.items() if k != "GROUP"), 2))
    return rows


def ask1_stops(accr, control):
    """The routes a cracker and a mirror take. Each returns {unit: subledger balance}."""
    naive, roots, period_only = {}, {}, {}
    for r in accr:
        naive[r["unit_code"]] = naive.get(r["unit_code"], 0.0) + r["amount"]
        if not r["restates"]:
            # the natural wrong repair: read the restatement as the duplicate and keep the original
            roots[r["unit_code"]] = roots.get(r["unit_code"], 0.0) + r["amount"]
        if r["period"] == 12:
            period_only[r["unit_code"]] = period_only.get(r["unit_code"], 0.0) + r["amount"]
    return {"cracker": {k: round(v, 2) for k, v in naive.items()},
            "mirror": {k: round(v, 2) for k, v in roots.items()},
            "period_only": {k: round(v, 2) for k, v in period_only.items()},
            "answer": A.accrual_balance(accr, by="unit_code")}


# ---------------------------------------------------------------- ask 2

def ask2(till_rows, control_rows):
    """Per branch and FY25 quarter: takings by trading date, the sales control account, and the gap."""
    takings = {}
    for u, _t, b, _up, _n, v in till_rows:
        q = QUARTER[W.period_of(dt.date.fromisoformat(b), W.FY25_PERIODS)]
        key = (W.resolve_unit(u), q)
        takings[key] = takings.get(key, 0.0) + float(v)
    posted = {}
    for u, p, v in control_rows:
        key = (W.resolve_unit(u), QUARTER[int(p)])
        posted[key] = posted.get(key, 0.0) + float(v)
    out = {}
    for u in W.BRANCHES:
        for q in (1, 2, 3, 4):
            t_, p_ = takings.get((u, q), 0.0), posted.get((u, q), 0.0)
            out["%s-Q%d" % (u, q)] = dict(takings=round(t_, 2), posted=round(p_, 2),
                                          gap=round(t_ - p_, 2))
    return out


def ask2_stops(till_rows, control_rows):
    """cracker: attribute takings by the ledger upload date, which makes every gap zero."""
    by_upload = {}
    for u, _t, _b, up, _n, v in till_rows:
        p = W.period_of(dt.date.fromisoformat(up), W.FY25_PERIODS)
        if p is None:                 # uploaded after the FY25 close, so it posts into FY26
            continue
        key = (W.resolve_unit(u), QUARTER[p])
        by_upload[key] = by_upload.get(key, 0.0) + float(v)
    posted = {}
    for u, p, v in control_rows:
        key = (W.resolve_unit(u), QUARTER[int(p)])
        posted[key] = posted.get(key, 0.0) + float(v)
    cracker, mirror = {}, {}
    ans = ask2(till_rows, control_rows)
    for u in W.BRANCHES:
        for q in (1, 2, 3, 4):
            key = "%s-Q%d" % (u, q)
            cracker[key] = dict(takings=round(by_upload.get((u, q), 0.0), 2),
                                posted=round(posted.get((u, q), 0.0), 2),
                                gap=round(by_upload.get((u, q), 0.0) - posted.get((u, q), 0.0), 2))
            # the mirror gets the unaffected quarters right and the boundary ones wrong
            mirror[key] = ans[key] if q == 2 else cracker[key]
    return {"cracker": cracker, "mirror": mirror, "answer": ans}


# ---------------------------------------------------------------- ask 3

def _in_scope(summary_rows):
    """Entries the ruleset covers, per current unit code and period. The FY25 summary carries the former
    codes, so the unit register's mapping has to be applied before anything joins."""
    out = {}
    for u, p, iface, entries, _post, _val in summary_rows:
        if iface in A.MONITORED:
            key = (W.resolve_unit(u), int(p))
            out[key] = out.get(key, 0) + int(entries)
    return out


def ask3(summary_rows, log_rows):
    """Per unit and FY25 period: entries in scope of the ruleset that were never evaluated."""
    scope = _in_scope(summary_rows)
    ev = {(W.resolve_unit(u), int(p)): int(e) for u, p, _r, e, _c, _v, _h in log_rows}
    out = {}
    for code, _o, _n, _k, _c in W.UNITS:
        for p in range(1, 13):
            out["%s-P%02d" % (code, p)] = max(scope.get((code, p), 0) - ev.get((code, p), 0), 0)
    return out


def ask3_stops(summary_rows, log_rows):
    """cracker: every entry counted as in scope, so the gap is inflated by the unmonitored interfaces."""
    allscope = {}
    for u, p, _iface, entries, _post, _val in summary_rows:
        key = (W.resolve_unit(u), int(p))
        allscope[key] = allscope.get(key, 0) + int(entries)
    ev = {(W.resolve_unit(u), int(p)): int(e) for u, p, _r, e, _c, _v, _h in log_rows}
    cracker, mirror = {}, {}
    ans = ask3(summary_rows, log_rows)
    for code, _o, _n, _k, _c in W.UNITS:
        for p in range(1, 13):
            key = "%s-P%02d" % (code, p)
            cracker[key] = max(allscope.get((code, p), 0) - ev.get((code, p), 0), 0)
            # the mirror believes the completion flag, so it reports nothing unevaluated anywhere
            mirror[key] = 0
    return {"cracker": cracker, "mirror": mirror, "answer": ans}


def window_reading(sim, table, start, end):
    """The golden recomputed over an arbitrary date window, for the window and boundary closures.

    Returns (group unrounded, group graded, {unit: graded}).
    """
    tot = 0.0
    units = {}
    for code, _o, _n, _k, _c in W.UNITS:
        rows = [r for r in table if r["unit_now"] == code and start <= r["day"] <= end]
        k = np.array([r["items"] for r in rows], dtype=np.int64)
        f = np.array([r["flag"] for r in rows], dtype=np.int64)
        v = E.recover_unit(k, f) * k.sum()
        units[code] = int(round(v / UBIN) * UBIN)
        tot += v
    return tot, int(round(tot / GBIN) * GBIN), units
