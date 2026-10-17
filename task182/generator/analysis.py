"""Every route through the survey: the golden and each rung, computed from the minute series.

The functions here take the series `sim.build()` produced and the same column values the pack ships, so the
golden and the rungs are the same arithmetic the solver would run.
"""
import datetime as dt
import math

import numpy as np

import sim as SM
import world as W


def eavg(db):
    db = np.asarray(db, dtype=float)
    return float(10.0 * math.log10(np.mean(np.power(10.0, db / 10.0)))) if len(db) else float("nan")


def esub(a, b):
    ea, eb = 10.0 ** (a / 10.0), 10.0 ** (b / 10.0)
    return float(10.0 * math.log10(ea - eb)) if ea > eb else float("nan")


def stop_mask(stamps):
    """Minutes inside an interval in which every plant source is recorded down."""
    out = np.zeros(len(stamps), dtype=bool)
    if not len(stamps):
        return out
    for start, end in SM.all_down():
        out |= np.array([(s >= start) and (s < end) for s in stamps])
    return out


def planned_mask(stamps):
    out = np.zeros(len(stamps), dtype=bool)
    if not len(stamps):
        return out
    for start, mins, _ in W.PLANNED_STOPS:
        end = start + dt.timedelta(minutes=mins)
        out |= np.array([(s >= start) and (s < end) for s in stamps])
    return out


def position_frames(series, adjust=True, drop_invalid=True, keep_dup=False, dup_rows=None):
    """Per position: the adjusted minute levels over its deployments, with the masks the routes need."""
    out = {}
    for sid, s in series.items():
        code = s["dep"]["code"]
        dev = SM.dep_dev(s["dep"])
        adj = SM.dep_correction(s["dep"]) if adjust else 0.0
        # the shipped columns, with the deployment's no-data minutes left as the file carries them: every
        # route below reads them through a mask that drops those minutes
        laeq = np.where(s["nd"], W.NODATA_VALUE, np.round(s["laeq"] + dev, 1) - adj)
        la90 = np.where(s["nd"], W.NODATA_VALUE, np.round(s["la90"] + dev, 1) - adj)
        st = stop_mask(s["stamps"])
        pl = planned_mask(s["stamps"])
        keep = s["am"].copy()
        if drop_invalid:
            keep &= s["vm"]
        d = out.setdefault(code, {"laeq": [], "la90": [], "keep": [], "stop": [], "planned": [],
                                  "am": [], "vm": [], "valid": [], "stamps": []})
        d["laeq"].append(laeq)
        d["la90"].append(la90)
        d["keep"].append(keep)
        d["valid"].append(s["vm"] if drop_invalid else np.ones(len(keep), dtype=bool))
        d["stop"].append(st)
        d["planned"].append(pl)
        d["am"].append(s["am"])
        d["vm"].append(s["vm"])
        d["stamps"].append(np.array(s["stamps"], dtype=object))
    for code, d in out.items():
        for k in list(d):
            d[k] = np.concatenate(d[k])
    if keep_dup and dup_rows is not None:
        code, laeq, la90, keep, stop, planned, valid = dup_rows
        d = out[code]
        d["laeq"] = np.concatenate([d["laeq"], laeq])
        d["la90"] = np.concatenate([d["la90"], la90])
        d["keep"] = np.concatenate([d["keep"], keep])
        d["stop"] = np.concatenate([d["stop"], stop])
        d["planned"] = np.concatenate([d["planned"], planned])
        d["valid"] = np.concatenate([d["valid"], valid])
    return out


def routes(frames):
    """The golden and every rung, per position."""
    r = {}
    for code, d in frames.items():
        on = d["keep"] & ~d["stop"]
        off = d["valid"] & d["stop"]
        off_planned = d["valid"] & d["planned"]
        total = eavg(d["laeq"][d["keep"]])            # plan 3.1: every valid assessment minute
        total_running = total
        resid = eavg(d["laeq"][off])
        resid_planned = eavg(d["laeq"][off_planned])
        p10 = float(np.percentile(d["laeq"][on], 10.0))
        la90mean = eavg(d["la90"][on])
        # quietest contiguous quarter hour of the position's own record
        x = d["laeq"][on]
        e = np.power(10.0, x / 10.0)
        if len(e) >= 15:
            c = np.convolve(e, np.ones(15) / 15.0, mode="valid")
            min15 = float(10.0 * math.log10(c.min()))
        else:
            min15 = float(x.min())
        arith = float(np.mean(x))
        arith90 = float(np.mean(d["la90"][on]))
        r[code] = {
            "total": total, "total_running": total_running, "resid": resid,
            "resid_planned": resid_planned, "minutes_valid": int(on.sum()),
            "minutes_excluded": int((d["am"] & ~d["vm"]).sum()) if "am" in d else 0,
            "minutes_stop": int(off.sum()),
            "specific": esub(total, resid),
            "specific_planned": esub(total, resid_planned),
            "specific_running_total": esub(total_running, resid),
            "rung1_total": total,
            "rung2_p10": esub(total, p10),
            "rung2_la90": esub(total, la90mean),
            "rung2b_min15": esub(total, min15),
            "rung2c_arith": esub(arith, arith90),
            "p10": p10, "la90mean": la90mean, "min15": min15,
        }
    return r


def slate(values, n=5):
    """The n positions with the highest value, and the margin from the nth to the next."""
    items = sorted(values.items(), key=lambda kv: -kv[1])
    picked = [k for k, _ in items[:n]]
    margin = items[n - 1][1] - items[n][1]
    return sorted(picked), round(margin, 3), items[n][0]


def all_slates(r):
    keys = ["specific", "rung1_total", "rung2_p10", "rung2_la90", "rung2b_min15", "rung2c_arith"]
    out = {}
    for k in keys:
        out[k] = slate({c: v[k] for c, v in r.items()})
    out["rung0_complaints"] = slate({c: float(W.COMPLAINTS[c]) + 0.001 * (14 - W.CODES.index(c))
                                     for c in W.CODES})
    return out
