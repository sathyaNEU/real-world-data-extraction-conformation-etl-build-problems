"""figures.json and submission.md, both emitted from the golden computed on the shipped pack."""
import json

import numpy as np

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
    x, y = S.pair_points(D, bh, Sr)
    mh, par = S.fit(x, y, "pl")
    e = S.errors(D, bh, mh, Sr)
    return dict(D=D, S=Sr, bh=bh, x=x, y=y, mh=mh, par=par, errors=e, listed=S.listed(e),
                validation=S.validation_errors(D), visits=S.visits(D), failures=S.failures(D))


def figures(target):
    g = golden(target)
    D, e, listed, v = g["D"], g["errors"], g["listed"], g["validation"]
    reg = D["reg"].set_index("station")
    default = S.listed(v)
    fam = S.wide_family(D, g["S"])
    vd = set(zip(D["validation"]["station"], D["validation"]["date"].astype(str).str[:10]))
    h = D["hourly"]
    on_vday = [(s, d) in vd for s, d in zip(h["station"], h["local_start"].str[:10])]
    low = min(min(abs(f[s]) for s in listed) for f in fam.values())
    high = max(max(abs(val) for s, val in f.items() if s not in listed) for f in fam.values())
    loss40 = float(np.ravel(g["mh"](np.array([40.0])))[0])
    assert 0.17 <= min(float(np.ravel(f(np.array([40.0])))[0]) for f in [g["mh"]])
    fig = {
        "call": {"listed": listed, "count": len(listed), "stations": len(e), "stay": len(e) - len(listed),
                 "district": {s: reg.loc[s, "district"] for s in listed},
                 "road": {s: reg.loc[s, "road"] for s in listed},
                 "location": {s: reg.loc[s, "location"] for s in listed},
                 "listed_below_pct": int(np.floor(100 * low)),
                 "unlisted_within_pct": float(np.ceil(200 * high) / 2)},
        "components": {"validation_max_occupancy_pct": round(float(h.loc[on_vday, "occ"].max()), 1),
                       "default_list": default,
                       "default_only": sorted(set(default) - set(listed)),
                       "default_only_validation_pct": {s: _pct(v[s]) for s in sorted(set(default) - set(listed))},
                       "default_missed": sorted(set(listed) - set(default)),
                       "loss_reference_occupancy_pct": 40, "loss_at_reference_share": "one in five"},
        "asks": {"visits": {d: {str(q): int(g["visits"][(d, q)]) for q in (1, 2, 3, 4)} for d in P.DISTRICTS},
                 "failures": {d: {str(q): int(g["failures"][(d, q)]) for q in (1, 2, 3, 4)} for d in P.DISTRICTS}},
    }
    assert 0.17 <= loss40 <= 0.21 and all(
        0.17 <= float(np.ravel(S.fit(*S.pair_points(D, g["bh"], g["S"]), f)[0](np.array([40.0])))[0]) <= 0.21
        for f in S.FAMILY)
    fig["_golden"] = g
    fig["_family"] = fam
    return fig


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def submission(fig):
    c, k, a = fig["call"], fig["components"], fig["asks"]
    F = B.FILES
    drop = k["default_only"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: each "
             "permanent traffic count station's 2027 counting error, a sensitivity and a loss that grows with "
             "occupancy in queued traffic).  ")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Flag %d of the %d stations in the 2027 report and send them to the spring 2028 recalibration: %s; the "
             "other %d meet the standard.** Each listed station counted more than %d per cent fewer vehicles than "
             "passed it in 2027 once the vehicles its loops lose in queued traffic are counted, and no other station "
             "is beyond %s per cent. Not the summer validation list (%s): the filmed days were July and August "
             "weekdays with no hour above %.1f per cent occupancy, so they miss the loss, which the bridges' paired "
             "approaches show reaching about one vehicle in five at %d per cent occupancy; %s, at %s per cent on "
             "their validation days, are inside the band over the year, and %s, inside it on theirs, are beyond it.\n"
             % (c["count"], c["stations"], ", ".join(c["listed"]), c["stay"], c["listed_below_pct"],
                ("%.1f" % c["unlisted_within_pct"]).rstrip("0").rstrip("."), ", ".join(k["default_list"]),
                k["validation_max_occupancy_pct"], k["loss_reference_occupancy_pct"], " and ".join(drop),
                " and ".join("%+d" % k["default_only_validation_pct"][s] for s in drop),
                ", ".join(k["default_missed"][:-1]) + " and " + k["default_missed"][-1]))
    L.append("## 2. Critical Components\n")
    L.append("1. Each station and direction's sensitivity from its filmed day: %s at **%s per cent**, and no hour of "
             "any filmed day above **%.1f per cent** occupancy."
             % (" and ".join(drop), "** and **".join("%+d" % k["default_only_validation_pct"][s] for s in drop),
                k["validation_max_occupancy_pct"]))
    L.append("2. The loops' loss in queued traffic, from each bridge's queued approach against its free one: none in "
             "free flow, about **one vehicle in five** at %d per cent occupancy." % k["loss_reference_occupancy_pct"])
    L.append("3. The margin: every listed station more than **%d per cent** below the vehicles that passed it, every "
             "other station within **%s per cent**.\n"
             % (c["listed_below_pct"], ("%.1f" % c["unlisted_within_pct"]).rstrip("0").rstrip(".")))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read %s with each renumbered station's hours joined to its current number (%s, Code history), "
             "each hour placed in UTC by its offset." % (F["hourly"], F["register"]))
    L.append("2. Took each station and direction's sensitivity as the loops' count over the video count on its filmed "
             "day in %s, sites mapped through the register's validation_site." % F["validation"])
    L.append("3. Paired each bridge's two stations (%s: five bridges, no junction between their stations) and, in each "
             "direction and hour, set one less the queued approach's count over the far approach's, each on its "
             "validated sensitivity, against the queued approach's occupancy: a loss that grows with occupancy above "
             "the free-flow range." % F["network"])
    L.append("4. Divided every hour's count by its sensitivity ratio and by one less the loss at its occupancy, and "
             "took each station's 2027 error as its counted vehicles over the vehicles so estimated, less one, over "
             "the hours it counted (TDP-03 section 5): %d stations beyond 5 per cent." % c["count"])
    L.append("5. Counted the maintenance visits as the days labour was booked to each station in %s (Labour joined to "
             "Orders' stations, one per station and day), less the days at a station then on a TCX-4 (a TCX-2 before "
             "its replacement date) whose cabinet door logged nothing that local day in %s: the controller was reset "
             "from the contractor's office; the counts are item 2 below." % (F["orders"], F["events"]))
    L.append("6. Counted the power failures as each MAINS_FAIL a TCX-4 logged, once (the log repeats some after a lost "
             "poll), and at each TCX-2, which logs nothing and stops, each break in its hourly record, as many as the "
             "COMMS_LOST TrafficVault raised inside the break (a feeder that tripped twice) and at least one, leaving "
             "out the two controller replacements, quarters by local date; the counts are item 3 below.")
    L.append("7. Flag the %d stations and send the list for the spring round; the other %d stay.\n"
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
