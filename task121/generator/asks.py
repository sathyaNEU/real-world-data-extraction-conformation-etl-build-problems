"""The asks under the golden handling and under each mishandling: the complaints about odors noticed in
each month from inside the district (January to September) and the station's usable and calm hours (May to
September); the cracker's and the mirror's sheets."""
import collections
import datetime as dt

import analysis as AN
import core


def months_received(rows, poly, district=True):
    c = collections.Counter()
    for r in rows:
        if district and not AN.P.point_in(r["lat"], r["lon"], poly):
            continue
        t = r["received_t"]
        if core.YEAR0 <= t.date() <= core.LAST:
            c[t.month] += 1
    return [c[m] for m in range(1, 10)]


def months_exported(rows, poly, district=True, exact_dups=False):
    c = collections.Counter()
    seen = set()
    for r in rows:
        if district and not AN.P.point_in(r["lat"], r["lon"], poly):
            continue
        if exact_dups:
            k = tuple(v for kk, v in r.items() if kk not in ("complaint_no", "received", "received_t", "noticed_t",
                                                                "lat", "lon"))
            if k in seen:
                continue
            seen.add(k)
        t = r["noticed_t"]
        if core.YEAR0 <= t.date() <= core.LAST:
            c[t.month] += 1
    return [c[m] for m in range(1, 10)]


def ask_a(F):
    rows, ocs, poly = F["rows"], F["ocs"], F["poly"]
    gold = AN.months_noticed(AN.clean(rows, ocs, poly))
    stops = {
        "received month, every row": months_received(rows, poly, district=False),
        "received month, inside the district": months_received(rows, poly),
        "noticed as exported, inside the district": months_exported(rows, poly),
        "noticed, exact duplicates dropped (the battery)": months_exported(rows, poly, exact_dups=True),
        "one report once by household and time noticed, as exported": AN.months_noticed(
            AN.clean(rows, ocs, poly, utc=False, imported=False, key="household")),
        "one report once by household and time noticed, carry-over and UTC handled": AN.months_noticed(
            AN.clean(rows, ocs, poly, key="household")),
        "one report once by contact and time noticed, carry-over and UTC handled": AN.months_noticed(
            AN.clean(rows, ocs, poly, key="contact")),
        "resends dropped only": AN.months_noticed(AN.clean(rows, ocs, poly, utc=False, imported=False)),
        "resends and import": AN.months_noticed(AN.clean(rows, ocs, poly, utc=False)),
        "resends and UTC": AN.months_noticed(AN.clean(rows, ocs, poly, imported=False)),
        "over-cleaner (one per household and hour)": AN.months_noticed(AN.clean(rows, ocs, poly, pairs_over=True)),
        "golden without the boundary": AN.months_noticed(AN.clean(rows, ocs, poly, district=False)),
    }
    return gold, stops


def ask_c(F):
    met, held = F["met"], F["held"]
    gold = AN.station_hours(met, held)
    stops = {
        "held-vane records read as wind (the V flag trusted)": AN.station_hours(met, held, use_held=False),
        "standard-time months": AN.station_hours(met, held, local=False),
        "scalar average": AN.station_hours(met, held, method="scalar"),
        "held-vane trusted, standard-time months": AN.station_hours(met, held, local=False, use_held=False),
    }
    return gold, stops


def months_contact_dedup(rows, poly):
    """A stronger battery: one row per contact and time noticed, inside the boundary, by the noticed month."""
    c = collections.Counter()
    seen = set()
    for r in rows:
        if not AN.P.point_in(r["lat"], r["lon"], poly):
            continue
        k = (r["contact_id"], r["noticed"])
        if k in seen:
            continue
        seen.add(k)
        t = r["noticed_t"]
        if core.YEAR0 <= t.date() <= core.LAST:
            c[t.month] += 1
    return [c[m] for m in range(1, 10)]


def cracker(F):
    """The cracker landed the call, ran the battery (exact duplicates, key checks) and executed every filed rule:
    noticed month, inside the boundary, one report once (found on the household and the time noticed), vector
    averages, nine-of-twelve records, the V flag as the record's validity."""
    a = AN.months_noticed(AN.clean(F["rows"], F["ocs"], F["poly"], utc=False, imported=False, key="household"))
    c = AN.station_hours(F["met"], F["held"], use_held=False)
    return dict(A=a, C_usable=c[0], C_calm=c[1])


def kept(gold, sheet):
    """Cells of each ask the sheet files at the golden's value (exact counts)."""
    out = {}
    out["A"] = sum(int(x == y) for x, y in zip(gold["A"], sheet["A"]))
    out["C_usable"] = sum(int(x == y) for x, y in zip(gold["C_usable"], sheet["C_usable"]))
    out["C_calm"] = sum(int(x == y) for x, y in zip(gold["C_calm"], sheet["C_calm"]))
    return out
