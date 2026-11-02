"""Other routes through the asks: the natural reads, the careful solver's (cracker's) route and the
over-cleaning reads.  Used by checks.py (each device moves its figures) and ceiling.py (the pair)."""
from datetime import datetime
import numpy as np
from analysis import parse_unit, WEEK_UTC


def by_riser(D, units, per_unit, scale=1.0):
    out = {r["riser"]: 0.0 for r in D["risers"]}
    for u, v in per_unit.items():
        out[units[u]["riser"]] += v * scale
    return out


# ---------------------------------------------------------------------------------------------------- July use
def a_intervals_all(D, units):
    """Every 300 record of every register summed per NMI (missing days stay missing, substitutes stay)."""
    per = {}
    for u, x in units.items():
        per[u] = sum(r["vals"].sum() for d, recs in D["nem12"][x["nmi"]].items() for r in recs)
    return by_riser(D, units, per, 1 / 1000.0)


def a_dedup(D, units):
    """One record per NMI and day (the last), as if the second record of a day were a repeat."""
    per = {}
    for u, x in units.items():
        per[u] = sum(recs[-1]["vals"].sum() for d, recs in D["nem12"][x["nmi"]].items())
    return by_riser(D, units, per, 1 / 1000.0)


def _register_use(D, x):
    reads = {(r["meter_serial"], r["register"], r["read_local"][:10]): float(r["reading_kwh"]) for r in D["reads"]}
    ex = {e["nmi"]: e for e in D["exchanges"]}
    use = 0.0
    for reg in ("E1", "E2"):
        if x["nmi"] in ex:
            e = ex[x["nmi"]]
            if (e["old_meter_serial"], reg, "2026-07-01") in reads:
                use += float(e["old_final_%s_kwh" % reg]) - reads[(e["old_meter_serial"], reg, "2026-07-01")] + \
                       reads[(e["new_meter_serial"], reg, "2026-08-01")] - float(e["new_initial_%s_kwh" % reg])
        elif (x["serial"], reg, "2026-07-01") in reads:
            use += reads[(x["serial"], reg, "2026-08-01")] - reads[(x["serial"], reg, "2026-07-01")]
    return use


def a_cracker(D, units):
    """The careful route under the filed definition: every register's movement over July from the read file,
    through the exchange log where a meter was changed, each read taken as the file gives it."""
    per = {u: _register_use(D, x) for u, x in units.items()}
    return by_riser(D, units, per, 1 / 1000.0)


def a_impute(D, units):
    """Missing days filled at the meter's own daily mean, substitutes taken as given."""
    per = {}
    for u, x in units.items():
        recs = D["nem12"][x["nmi"]]
        tot = sum(r["vals"].sum() for d in recs for r in recs[d])
        n = len(recs)
        per[u] = tot / n * 31 if n < 31 else tot
    return by_riser(D, units, per, 1 / 1000.0)


# -------------------------------------------------------------------------------------------------- requests
def _space_unit(units):
    m = {}
    for u, x in units.items():
        for s in x["spaces"]:
            m[s] = u
    return m


def b_rows_by_unit(D, units):
    """Application rows counted on the riser of the unit written on them (addresses dropped)."""
    out = {r["riser"]: 0 for r in D["risers"]}
    for a in D["apps"]:
        u = parse_unit(a["Unit or owner address"])
        if u in units:
            out[units[u]["riser"]] += 1
    return out


def b_cracker(D, units):
    """The careful route: one request per car space, a B2 number written before 15 March 2025 carried to its
    re-marked number, each space on the riser of the apartment it is accessory to."""
    su = _space_unit(units)
    spaces = set()
    for a in D["apps"]:
        sp = a["Car space"].strip()
        if sp[:3] in ("B2-", "B3-") and datetime.strptime(a["Lodged"], "%d/%m/%Y") < datetime(2025, 3, 15):
            sp = D["remark"][sp]
        spaces.add(sp)
    out = {r["riser"]: 0 for r in D["risers"]}
    for sp in spaces:
        if sp in su:
            out[units[su[sp]]["riser"]] += 1
    return out


def b_no_remark(D, units):
    """One request per car space as written, on the riser of the apartment the written space belongs to."""
    su = _space_unit(units)
    spaces = {a["Car space"].strip() for a in D["apps"]}
    out = {r["riser"]: 0 for r in D["risers"]}
    for sp in spaces:
        if sp in su:
            out[units[su[sp]]["riser"]] += 1
    return out


# --------------------------------------------------------------------------------------------------- voltage
def _events(D, units):
    su = {x["serial"]: u for u, x in units.items()}
    for e in D["events"]:
        u = su.get(e["meter_serial"])
        if u is None:
            continue
        s = datetime.strptime(e["start_utc"], "%Y-%m-%dT%H:%M:%SZ")
        t = datetime.strptime(e["end_utc"], "%Y-%m-%dT%H:%M:%SZ")
        yield u, e, s, t


def _share(D, units, secs):
    out = {}
    for r in D["risers"]:
        us = [u for u, x in units.items() if x["riser"] == r["riser"]]
        out[r["riser"]] = sum(secs.get(u, 0.0) for u in us) / (len(us) * 7 * 86400.0) * 100.0
    return out


def c_sum_utc(D, units):
    """Durations summed record by record for events starting on UTC dates 13 to 19 July."""
    secs = {}
    for u, e, s, t in _events(D, units):
        if datetime(2026, 7, 13) <= s < datetime(2026, 7, 20):
            secs[u] = secs.get(u, 0.0) + (t - s).total_seconds()
    return _share(D, units, secs)


def c_cracker(D, units):
    """The careful route: near-repeats (same meter and element, start within ten seconds) removed, every record
    clipped to the market-time week, durations summed element by element."""
    seen = {}
    secs = {}
    for u, e, s, t in sorted(_events(D, units), key=lambda z: (z[1]["meter_serial"], z[1]["element"], z[2])):
        key = (e["meter_serial"], e["element"])
        if key in seen and abs((s - seen[key]).total_seconds()) <= 10:
            continue
        seen[key] = s
        s2, t2 = max(s, WEEK_UTC[0]), min(t, WEEK_UTC[1])
        if t2 > s2:
            secs[u] = secs.get(u, 0.0) + (t2 - s2).total_seconds()
    return _share(D, units, secs)


def c_union_utc(D, units):
    """Each apartment's records joined into spans, but on UTC dates 13 to 19 July."""
    iv = {}
    for u, e, s, t in _events(D, units):
        s2, t2 = max(s, datetime(2026, 7, 13)), min(t, datetime(2026, 7, 20))
        if t2 > s2:
            iv.setdefault(u, []).append((s2, t2))
    secs = {}
    for u, lst in iv.items():
        lst.sort()
        tot, (cs, ce) = 0.0, lst[0]
        for s, t in lst[1:]:
            if s <= ce:
                ce = max(ce, t)
            else:
                tot += (ce - cs).total_seconds()
                cs, ce = s, t
        secs[u] = tot + (ce - cs).total_seconds()
    return _share(D, units, secs)
