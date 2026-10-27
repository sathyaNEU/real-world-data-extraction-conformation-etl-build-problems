"""figures.json and submission.md, both emitted from the golden computed on the shipped pack."""
import json

import numpy as np
import pandas as pd

import build as B
import params as P
import solve as S

QWORD = {1: "first quarter", 2: "second", 3: "third", 4: "fourth"}


def _pct(x):
    return int(round(100 * float(x)))


def golden(target):
    D = S.load(target, B.FILES)
    D = S.load_ops(target, B.FILES, D)
    Sr = S.series(D)
    bh = S.bhat(D)
    cf, cpar = S.cold_fit(*S.cold_points(D, bh, Sr), "knee")
    cday = S.by_day(D, cf)
    x, y = S.pair_points(D, bh, Sr, cday)
    mh, par = S.fit(x, y, "pl")
    e = S.errors(D, bh, mh, cday, Sr)
    return dict(D=D, S=Sr, bh=bh, x=x, y=y, mh=mh, par=par, cf=cf, cpar=cpar, cday=cday, errors=e,
                listed=S.listed(e), validation=S.validation_errors(D), visits=S.visits(D), failures=S.failures(D))


def figures(target):
    g = golden(target)
    D, e, listed, v = g["D"], g["errors"], g["listed"], g["validation"]
    reg = D["reg"].set_index("station")
    default = S.listed(v)
    R = S.routes(D, g["S"])
    queue_only, cold_only = S.listed(R["A"]), S.listed(R["B"])
    fam = S.wide_family(D, g["S"])
    vd = set(zip(D["validation"]["station"], D["validation"]["date"].astype(str).str[:10]))
    h = D["hourly"]
    on_vday = [(s, d) in vd for s, d in zip(h["station"], h["local_start"].str[:10])]
    tm = S.tmean(D)
    vdays = sorted({pd.Timestamp(d).date() for d in D["validation"]["date"]})
    low = min(min(abs(f[s]) for s in listed) for f in fam.values())
    high = max(max(abs(val) for s, val in f.items() if s not in listed) for f in fam.values())
    loss40 = float(np.ravel(g["mh"](np.array([40.0])))[0])
    cold10 = float(np.ravel(g["cf"](np.array([-10.0])))[0])
    bh = g["bh"]
    cv = S.cold_variants(D, bh, g["S"])
    near = sorted(d for d, t in tm.items() if -10.5 <= t <= -9.5)
    spread = [float(np.mean(f(near))) for f in cv.values()]
    assert 0.17 <= loss40 <= 0.20 and all(
        0.17 <= float(np.ravel(S.fit(*S.pair_points(D, bh, g["S"], g["cday"]), f)[0](np.array([40.0])))[0]) <= 0.20
        for f in S.FAMILY), loss40
    assert 0.085 <= cold10 <= 0.12 and all(0.085 <= c <= 0.12 for c in spread), (cold10, spread)
    fig = {
        "call": {"listed": listed, "count": len(listed), "stations": len(e), "stay": len(e) - len(listed),
                 "district": {s: reg.loc[s, "district"] for s in listed},
                 "road": {s: reg.loc[s, "road"] for s in listed},
                 "location": {s: reg.loc[s, "location"] for s in listed},
                 "controller": {s: reg.loc[s, "controller"] for s in listed},
                 "listed_below_pct": int(np.floor(100 * low)),
                 "unlisted_within_pct": float(np.ceil(200 * high) / 2)},
        "components": {"validation_max_occupancy_pct": round(float(h.loc[on_vday, "occ"].max()), 1),
                       "validation_min_mean_temp_c": int(np.floor(min(tm[d] for d in vdays))),
                       "default_list": default,
                       "default_only": sorted(set(default) - set(listed)),
                       "default_missed": sorted(set(listed) - set(default)),
                       "queue_only_list": queue_only,
                       "cold_only_list": cold_only,
                       "loss_reference_occupancy_pct": 40, "loss_at_reference_share": "nearly one in five",
                       "cold_reference_temp_c": -10, "cold_at_reference_share": "about one in ten",
                       "cold_knee_c": 2},
        "asks": {"visits": {d: {str(q): int(g["visits"][(d, q)]) for q in (1, 2, 3, 4)} for d in P.DISTRICTS},
                 "failures": {d: {str(q): int(g["failures"][(d, q)]) for q in (1, 2, 3, 4)} for d in P.DISTRICTS}},
    }
    assert queue_only != listed and cold_only != listed and default != listed
    fig["_golden"] = g
    fig["_family"] = fam
    return fig


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def submission(fig):
    c, k, a = fig["call"], fig["components"], fig["asks"]
    F = B.FILES
    within = ("%.1f" % c["unlisted_within_pct"]).rstrip("0").rstrip(".")
    qmiss = sorted(set(c["listed"]) - set(k["queue_only_list"]))
    cmiss = sorted(set(c["listed"]) - set(k["cold_only_list"]))
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: each "
             "permanent traffic count station's 2027 counting error, a sensitivity, a loss that grows with occupancy "
             "in queued traffic and the older controllers' miss on cold days).  ")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Flag %d of the %d stations in the 2027 report and send them to the spring 2028 recalibration: %s; the "
             "other %d meet the standard.** Each listed station counted more than %d per cent fewer vehicles than "
             "passed it in 2027 once the vehicles its loops lose in queued traffic, and on a TCX-2 controller on cold "
             "days, are counted, and no other station is beyond %s per cent. Not the summer validation list (%s): the "
             "filmed days were July and August weekdays with no hour above %.1f per cent occupancy and no day below "
             "%d degrees. Not the queue loss alone (%s), which leaves %s inside the band; not the cold miss alone (%s), "
             "which leaves %s inside it.\n"
             % (c["count"], c["stations"], _and(c["listed"]), c["stay"], c["listed_below_pct"], within,
                _and(k["default_list"]), k["validation_max_occupancy_pct"], k["validation_min_mean_temp_c"],
                _and(k["queue_only_list"]), _and(qmiss), _and(k["cold_only_list"]), _and(cmiss)))
    L.append("## 2. Critical Components\n")
    L.append("1. Each station and direction's sensitivity from its filmed day, with no hour of any filmed day above "
             "**%.1f per cent** occupancy and no filmed day's mean temperature below **%d degrees**."
             % (k["validation_max_occupancy_pct"], k["validation_min_mean_temp_c"]))
    L.append("2. The loops' loss in queued traffic, from each bridge's queued approach against its free one: none in "
             "free flow, **%s** vehicles at %d per cent occupancy."
             % (k["loss_at_reference_share"], k["loss_reference_occupancy_pct"]))
    L.append("3. The TCX-2 controllers' miss on cold days, from the bridges whose approaches run one controller of "
             "each generation: none above about %d degrees mean temperature, **%s** vehicles at %d degrees; the "
             "TCX-4s miss none (their occupancy per counted vehicle holds flat through the winter while the TCX-2s' "
             "climbs)." % (k["cold_knee_c"], k["cold_at_reference_share"], k["cold_reference_temp_c"]))
    L.append("4. The margin: every listed station more than **%d per cent** below the vehicles that passed it, every "
             "other station within **%s per cent**.\n" % (c["listed_below_pct"], within))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read %s with each renumbered station's hours joined to its current number (%s, Code history), "
             "each hour placed in UTC by its offset, and took each station and direction's sensitivity as the loops' "
             "count over the video count on its filmed day in %s, sites mapped through the register's "
             "validation_site." % (F["hourly"], F["register"], F["validation"]))
    L.append("2. Took each day's controller from the register and its Code history (R08-05 and R19-03 ran a TCX-2 "
             "before their replacement dates) and each day's mean temperature from %s (Mean Temp, a missing day the "
             "mean of the days either side)." % F["weather"])
    L.append("3. Paired each bridge's two stations (%s: five bridges, no junction between their stations) and, on the "
             "three bridges whose approaches run one controller of each generation, set each free-flowing day's TCX-2 "
             "count against the TCX-4 count, each on its validated sensitivity, against the day's mean temperature: "
             "a miss on the TCX-2 that grows below about %d degrees. Read the same miss a second way, off each "
             "station's own occupancy per counted vehicle (occupancy fitted against the counted vehicles over the "
             "station's free-flowing hours and read where the summer's and the month's flows overlap, so the traffic "
             "drops out and only a change in what the controller counts remains): it climbs wherever a TCX-2 was in "
             "service, including the months before each renumbered station's replacement, and holds flat wherever a "
             "TCX-4 was, which puts the miss on the older cards and leaves no room for a drift the two generations "
             "share or for a sensitivity moving inside a regime." % (F["network"], k["cold_knee_c"]))
    L.append("4. With that miss taken out, set in each direction and hour one less the queued approach's count over "
             "the far approach's, each on its validated sensitivity, against the queued approach's occupancy: a loss "
             "that grows with occupancy above the free-flow range, the two approaches of one bridge differing by a "
             "fifth of the upstream count in the most queued hours against under a hundredth in free flow, with "
             "nothing joining or leaving between them, and one function of occupancy fitted at each of the five "
             "bridges on its own.")
    L.append("5. Divided every hour's count by its sensitivity ratio, by one less the loss at its occupancy and, on a "
             "TCX-2, by one less the cold miss at the day's temperature, and took each station's 2027 error as its "
             "counted vehicles over the vehicles so estimated, less one, over the hours it counted (TDP-03 section "
             "5): %d stations beyond 5 per cent, the same %d under the pooled bridge fit, under each station's own "
             "occupancy channel, and with the loss carried to the stations that are on no bridge at any scale from a "
             "half to a third again." % (c["count"], c["count"]))
    L.append("6. Counted the maintenance visits as the station-days a technician attended (TDP-03 section 7): the "
             "days labour was booked to each station in %s (Labour joined to Orders' stations, one per station and "
             "day), less the days at a station then on a TCX-4 whose cabinet door logged nothing that local day in "
             "%s, where the controller was reset over the link from the contractor's own premises, plus the local day "
             "after an attendance the door log shows running past midnight; the counts are item 2 below."
             % (F["orders"], F["events"]))
    L.append("7. Counted the power failures as each loss of mains power at a controller (section 7): each MAINS_FAIL a "
             "controller reported, once (the log repeats some after a lost poll), and each break in a station's "
             "hourly record, which is a loss the controller did not report (a TCX-2 has no standby supply and stops; "
             "a TCX-4 whose battery runs out stops as well and loses what it had logged, leaving the cold start it "
             "raises under an unset clock), with one more for each time the station answered a poll inside the break "
             "and failed again, leaving out the two controller replacements, quarters by local date; the counts are "
             "item 3 below.")
    L.append("8. Flag the %d stations and send the list for the spring round; the other %d stay.\n"
             % (c["count"], c["stay"]))
    L.append("## 4. Deliverable Answers\n")
    L.append("### count_stations_flagged_2027.xlsx\n")
    L.append("1. The stations whose 2027 count is off by more than 5 per cent, %d (station, district):" % c["count"])
    for s in c["listed"]:
        L.append("   - %s, %s" % (s, c["district"][s]))
    L.append("2. Maintenance visits to the stations in 2027, by district and quarter:")
    for d in P.DISTRICTS:
        q = a["visits"][d]
        L.append("   - %s: first quarter %d, second %d, third %d, fourth %d" % (d, q["1"], q["2"], q["3"], q["4"]))
    L.append("3. Power failures at the stations in 2027, by district and quarter:")
    for d in P.DISTRICTS:
        q = a["failures"][d]
        L.append("   - %s: first quarter %d, second %d, third %d, fourth %d" % (d, q["1"], q["2"], q["3"], q["4"]))
    L.append("\n### count_station_errors_2027.png\n")
    L.append("4. Each of the %d stations' 2027 count error against the band from -5 to +5 per cent, the %d listed "
             "stations marked." % (c["stations"], c["count"]))
    return "\n".join(L) + "\n"
