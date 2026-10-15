"""The three supplemental asks and the stops a response can halt at. Nothing here ships."""
import datetime as dt

import offences as O
import places as PL
import records as R
import sensors as S
import world as W


def offences_by_class(rows):
    """Ask 1 golden: the quarter's recorded offences of each class, each season. One offence counted once, whichever
    system holds it."""
    out = {}
    for r in rows:
        si = O.season_of(r["from"].date())
        if si is None:
            continue
        out[(r["cls"], si)] = out.get((r["cls"], si), 0) + 1
    return out


def offences_by_class_stops(rows, fr):
    """The stops: both exports unioned as they stand; de-duplicated on the reference; the legacy file left out."""
    rms = R.rms_rows(rows, fr)[1:]
    leg = R.legacy_rows(rows, fr)[1:]
    leg_cls = {v: k for k, v in W.LEGACY_NAMES.items()}
    union, by_ref, rms_only = {}, {}, {}
    for x in rms:
        si = O.season_of(dt.datetime.strptime(x[2], "%Y-%m-%d %H:%M").date())
        if si is None:
            continue
        key = (x[1], si)
        union[key] = union.get(key, 0) + 1
        by_ref[key] = by_ref.get(key, 0) + 1
        rms_only[key] = rms_only.get(key, 0) + 1
    for x in leg:
        si = O.season_of(dt.datetime.strptime(x[2], "%d/%m/%Y").date())
        if si is None:
            continue
        key = (leg_cls[x[1]], si)
        union[key] = union.get(key, 0) + 1
        by_ref[key] = by_ref.get(key, 0) + 1
    return {"union": union, "by_reference": by_ref, "rms_only": rms_only}


def location_shares(rows):
    """Ask 2 golden: the share of the quarter's recorded offences at each of the five locations, each season."""
    tot = {}
    at = {}
    for r in rows:
        si = O.season_of(r["from"].date())
        if si is None:
            continue
        tot[si] = tot.get(si, 0) + 1
        at[(r["loc"], si)] = at.get((r["loc"], si), 0) + 1
    return {k: 100.0 * v / tot[k[1]] for k, v in at.items()}


def location_share_stops(rows, fr):
    """The stops: the raw address string grouped as it stands (two spellings split each street, and Cranstoun's
    Harbourgate Street counts as the quarter's); the gazetteer applied but the out-of-range numbers kept; the rows
    with no location code dropped."""
    allrows = list(rows) + list(fr)
    raw, kept, coded = {}, {}, {}
    for r in allrows:
        si = O.season_of(r["from"].date())
        if si is None:
            continue
        name = r["address"].split(" ", 1)[-1] if r["address"][0].isdigit() else r["address"]
        raw[(name, si)] = raw.get((name, si), 0) + 1
        if r["street"] == R.FRINGE_STREET and r["number"] > 178:
            loc = "Harbourgate Street"          # the gazetteer resolves the spelling, the register's range is
            kept[(loc, si)] = kept.get((loc, si), 0) + 1   # what rules it out, and this stop keeps it
        elif r["loc"]:
            kept[(r["loc"], si)] = kept.get((r["loc"], si), 0) + 1
        if r["coded"] and r["loc"]:
            coded[(r["loc"], si)] = coded.get((r["loc"], si), 0) + 1
    def share(d):
        tot = {}
        for (nm, si), v in d.items():
            tot[si] = tot.get(si, 0) + v
        return {k: 100.0 * v / tot[k[1]] for k, v in d.items()}
    return {"raw_address": share(raw), "range_kept": share(kept), "coded_only": share(coded)}


def footfall(counts):
    """Ask 3 golden: the footfall each sensor's location saw per trading hour, each season. The hours the fault log
    covers are out of both the count and the hours, because the head reported a part of the footfall for them."""
    return S.per_trading_hour(counts)


def footfall_stops(counts):
    """The stops: every hour of the season, closed hours included; the quarter's trading hours with the fault hours
    left in; the fault hours out of the count but still in the hours."""
    faults = {sid: S.fault_hours(sid) for sid in W.SENSORS}
    whole, trading, half = {}, {}, {}
    for sid, stamp, n in counts:
        local = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=1)
        si = 0 if local.date() <= W.SEASONS[0][1] else 1
        whole.setdefault((sid, si), [0, 0])
        whole[(sid, si)][0] += n
        whole[(sid, si)][1] += 1
        if not S.trading_open(local.weekday(), local.hour):
            continue
        trading.setdefault((sid, si), [0, 0])
        trading[(sid, si)][0] += n
        trading[(sid, si)][1] += 1
        half.setdefault((sid, si), [0, 0])
        half[(sid, si)][1] += 1
        if (local.date(), local.hour) not in faults[sid]:
            half[(sid, si)][0] += n
    return {"every_hour": {k: v[0] / v[1] for k, v in whole.items()},
            "faults_left_in": {k: v[0] / v[1] for k, v in trading.items()},
            "faults_out_of_the_count_only": {k: v[0] / v[1] for k, v in half.items()}}
