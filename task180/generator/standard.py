"""ES-DGA-02 condition coding, parameterised so the grid and the rungs can be run on the same rows.

rows: list of dicts with transformer_id, sampled (datetime), date (analysis date), sample_id, issue
and the gas columns as reported strings ("<0.5", "12.4", "3810").
"""
import datetime as dt
import statistics

import world as W

DAY = dt.timedelta(days=1)


def value(s, bdl="half"):
    if s is None or s == "":
        return None
    s = str(s)
    if s.startswith("<"):
        lim = float(s[1:])
        return {"zero": 0.0, "half": lim / 2, "limit": lim}[bdl]
    return float(s)


def record_of_issue(rows):
    """The report of record is the latest issue for a sample ID."""
    best = {}
    for r in rows:
        k = r["sample_id"]
        if k not in best or int(r["issue"]) > int(best[k]["issue"]):
            best[k] = r
    return list(best.values())


def by_unit(rows, when="sampled"):
    out = {}
    for r in rows:
        out.setdefault(r["transformer_id"], []).append(r)
    for k in out:
        out[k].sort(key=lambda r: (r[when], r["sample_id"]))
    return out


def as_day(x):
    return x.date() if isinstance(x, dt.datetime) else x


def preservation(samples, mode="latest"):
    def ratio(r):
        return float(r["O2"]) / float(r["N2"])
    if mode == "latest":
        x = ratio(samples[-1])
    else:
        x = statistics.median(ratio(r) for r in samples)
    return "SL" if x <= W.O2N2_SEALED_MAX else "FB"


def base_sample(samples, gap=W.BASE_GAP_DAYS, when="sampled"):
    latest = samples[-1]
    t1 = as_day(latest[when])
    cands = [r for r in samples[:-1] if (t1 - as_day(r[when])).days >= gap]
    return cands[-1] if cands else None


def increases(samples, bdl="half", gap=W.BASE_GAP_DAYS, when="sampled"):
    latest = samples[-1]
    base = base_sample(samples, gap, when)
    days = (as_day(latest[when]) - as_day(base[when])).days
    inc = {}
    for g in W.GASES:
        inc[g] = (value(latest[g], bdl) - value(base[g], bdl)) * 365.0 / days
    return inc, base, days


def code_unit(tid, samples, exclude=(), bdl="half", gap=W.BASE_GAP_DAYS, cls_mode="latest",
              when="sampled"):
    """Returns (code, severity, gas, detail)."""
    u = W.UNIT[tid]
    cls = preservation(samples, cls_mode)
    band = W.age_band(u)
    bi = W.BANDS.index(band)
    latest = samples[-1]
    inc, base, days = increases(samples, bdl, gap, when)
    c3, c2 = [], []
    ratios = {}
    for g in W.GASES:
        if g in exclude:
            continue
        lvl = value(latest[g], bdl)
        lim = W.A3[cls][g]
        ratios[g] = max(0.0, inc[g]) / lim
        over95 = lvl > W.A2[cls][g][bi]
        over90 = lvl > W.A1[cls][g][bi]
        rate = inc[g] > lim
        if over95 and rate:
            c3.append(g)
        if over90 or rate:
            c2.append(g)
    code = 3 if c3 else (2 if c2 else 1)
    gas = max(ratios, key=lambda g: ratios[g])
    return code, ratios[gas], gas, {"class": cls, "band": band, "base": base, "days": days,
                                    "inc": inc, "ratios": ratios, "c3": c3, "c2": c2}


def fleet(rows, excl=None, **kw):
    excl = excl or {}
    units = by_unit(record_of_issue(rows), kw.get("when", "sampled"))
    out = {}
    for tid in W.IDS:
        out[tid] = code_unit(tid, units[tid], exclude=excl.get(tid, ()), **kw)
    return out


def slate(coded, n=3):
    c3 = [t for t in coded if coded[t][0] == 3]
    c3.sort(key=lambda t: (-coded[t][1], t))
    return c3[:n], c3
