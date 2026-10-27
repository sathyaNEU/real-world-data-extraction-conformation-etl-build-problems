"""Cut the task307 pack."""
import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import net
import params as P
import records as R
import solve
import world

F = P.FILES
PACK = list(F)
DISTRACTORS = ("crash", "transit", "probe", "segs", "cmp")
CONTEXT = ("guidance", "modeldoc", "tip")

SPONSOR = {"A": "State DOT, District 4", "B": "City of Merrimont", "C": "City of Merrimont",
           "D": "Ashkettle County Public Works"}
DESC = {"A": "Add a third lane in each direction on Route 9 through Millbrook, between Lakeview Road and Quarry Lane.",
        "B": "Widen the Ferry Street exit from Route 9 into downtown from two lanes to three, with a third lane on the "
             "matching on-ramp.",
        "C": "Replace the Center Street Bridge deck and restripe from one lane each way to two lanes each way.",
        "D": "Adaptive signals and protected turn lanes on the Southport Bridge and Southport Avenue to downtown; "
             "the corridor's per-lane capacity rises from 850 to 980 vehicles an hour."}


def coding(links):
    recs = R.link_records(links)
    rows = []
    for pr in P.PROJECTS:
        for r in recs:
            l = links[r["_k"]]
            if pr["change"] == "lanes" and l["name"] == pr["street"] and (pr.get("segment") is None or l["bottleneck"]):
                rows.append([pr["tip_id"], r["LINK_ID"], r["A_NODE"], r["B_NODE"], "AB_LANES and BA_LANES",
                             r["AB_LANES"], pr["new_lanes"]])
            if pr["change"] == "lane_capacity" and l["name"] in pr["streets"]:
                rows.append([pr["tip_id"], r["LINK_ID"], r["A_NODE"], r["B_NODE"],
                             "capacity per lane, both directions (vph)", net.LANE_CAP[l["ftype"]], pr["new_lane_cap"]])
    summary = [(p, SPONSOR[p["code"]], DESC[p["code"]]) for p in P.PROJECTS]
    return {"rows": rows, "summary": summary}


def inventory_rows():
    rows = []
    for st, loc, _, dab, dba in R.STATIONS:
        status, note, since = "Active", "", "2016-05-01"
        if st == R.REPLACED[0]:
            status = "Retired"
            note = ("Loops lifted 2025-07-14 for the deck joint repair; station replaced at the same location by "
                    "%s on 2025-07-15." % R.REPLACED[1])
        rows.append([st, loc, "%s / %s" % (dab, dba), "Inductive loop", since, status, note])
    st, loc, _, dab, dba = R.STATIONS[2]
    rows.insert(3, [R.REPLACED[1], loc, "%s / %s" % (dab, dba), "Inductive loop", "2025-07-15", "Active",
                    "Replaces %s at the same location." % R.REPLACED[0]])
    return rows


MAINT_BENIGN = [
    ("S-0101", "2025-01-22", "Quarterly cabinet inspection; no faults found."),
    ("S-0101", "2025-08-12", "Cellular modem replaced; logger memory intact."),
    ("S-0102", "2025-03-11", "Loop 1 EB resistance high on the annual test; within tolerance, no action."),
    ("S-0102", "2025-06-17", "Quarterly cabinet inspection; no faults found."),
    ("S-0103", "2025-02-04", "Quarterly cabinet inspection; no faults found."),
    ("S-0103R", "2025-11-18", "Count accuracy check against video, 2 hours each direction: within 2 per cent."),
    ("S-0104", "2025-05-28", "Firmware updated to 4.11.2."),
    ("S-0104", "2025-10-01", "Count accuracy check against video, 2 hours each direction: within 2 per cent."),
    ("S-0105", "2025-01-15", "Quarterly cabinet inspection; no faults found."),
    ("S-0105", "2025-09-09", "Loop 2 SB lead-in splice resealed; counting checked."),
    ("S-0106", "2025-04-03", "Firmware updated to 4.11.2."),
    ("S-0106", "2025-12-02", "Quarterly cabinet inspection; no faults found."),
    ("S-0107", "2025-03-25", "Count accuracy check against video, 2 hours each direction: within 2 per cent."),
    ("S-0107", "2025-07-08", "Cabinet fan replaced."),
    ("S-0108", "2025-06-10", "Quarterly cabinet inspection; no faults found."),
    ("S-0108", "2025-10-21", "Loop 1 EB resistance high on the annual test; within tolerance, no action."),
]


def _wo(day):
    """work orders are numbered in the order they are raised across every crew, so a station's are sparse"""
    start = dt.date(day.year, 1, 1)
    n = int(round((day - start).days * 3.37)) + 17 + (day.toordinal() * 7919) % 5
    return "WO %s-%04d" % (day.strftime("%y"), n)


def maintenance_rows():
    rows = []
    for st, (d, f0, f1, fac, lane, kind) in R.FAULTS.items():
        sid = st
        if st == R.REPLACED[0] and f1.date() >= R.REPLACED[2]:
            sid = R.REPLACED[1]
        if kind == "open":
            txt = "Loop %d %s open circuit; loop sawcut and replaced, counting checked." % (lane, d)
        else:
            txt = "%s detector card replaced (crosstalk with the adjacent channel); counting checked." % d
        rows.append([sid, f1.date().isoformat(), _wo(f1.date()), txt])
    for sid, d, txt in MAINT_BENIGN:
        day = dt.date.fromisoformat(d)
        rows.append([sid, d, _wo(day), txt])
    rows.append([R.REPLACED[0], "2025-07-14", _wo(dt.date(2025, 7, 14)), "Loops lifted for the bridge deck joint repair; station "
                 "decommissioned."])
    rows.append([R.REPLACED[1], "2025-07-15", _wo(dt.date(2025, 7, 15)), "New loops and cabinet at the same location; station "
                 "commissioned as %s." % R.REPLACED[1]])
    return sorted(rows, key=lambda r: (r[1], r[0]))


def _parquet(df, path):
    tb = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tb, path, compression="snappy", store_schema=False)


def build(target):
    os.makedirs(target, exist_ok=True)
    p = lambda k: os.path.join(target, F[k])
    o = solve.run()
    links = o["links"]
    recs = pd.DataFrame(R.link_records(links)).drop(columns="_k")
    recs.to_csv(p("links"), index=False)
    R.nodes_table(links).to_csv(p("nodes"), index=False)
    R.trips_table(o["tabs"]).to_csv(p("trips"), index=False)
    R.loaded_table(o).to_csv(p("loaded"), index=False)
    blinks, base = R.base_assignment()
    R.validation_table(blinks, base).to_csv(p("valid"), index=False)
    atr, _ = R.atr_records(blinks, base)
    atr.to_csv(p("atr"), index=False)
    cap, t0, al, be = net.link_arrays(blinks)
    bt = {per: t0 * (1 + al * (base[per] / cap) ** be) for per in base}
    seg, probe = R.probe_records(blinks, bt, t0)
    seg.drop(columns="_k").to_csv(p("segs"), index=False)
    _parquet(probe, p("probe"))
    R.transit_table().to_csv(p("transit"), index=False)
    docs.model_doc(p("modeldoc"))
    docs.guidance(p("guidance"))
    docs.count_manual(p("countman"))
    docs.cmp_doc(p("cmp"))
    docs.tip_workbook(p("tip"), coding(links))
    docs.station_inventory(p("stations"), inventory_rows(), maintenance_rows())
    docs.crash_workbook(p("crash"), R.crash_table())
    return o


TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def metadata():
    files = []
    for k in PACK:
        files.append(dict(file=F[k], source="synthetic (task307 generator)", date=P.AS_OF,
                          license="generated for this task", distractor=k in DISTRACTORS))
    meta = dict(task="task307", title="Merrimont Area MPO: the FY2028 TIP congestion-relief slot", files=files,
                distractors=[F[k] for k in DISTRACTORS],
                license="All files are synthetic, generated for this task by task307/generator; no third-party data.",
                source_note="The Merrimont subarea network, trip tables, count stations, probe travel times and "
                            "documents are invented; the methods (BPR volume-delay functions, user-equilibrium "
                            "assignment, the AASHTO AADT method, the planning time index) are standard practice.")
    import json
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
    metadata()
