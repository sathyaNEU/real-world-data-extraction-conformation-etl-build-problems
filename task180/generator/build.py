"""Build the task180 pack: python3 build.py   (writes ../target/)."""
import csv
import datetime as dt
import json
import os
import shutil
import subprocess
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W      # noqa: E402
import sim             # noqa: E402
import lab             # noqa: E402
import docs            # noqa: E402
import docs_pdf        # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
F = {
    "main": "dga_main_tank_results_2021-2026.csv",
    "comp": "dga_tap_changer_compartments_2021-2026.csv",
    "register": "asset_register_zone_transformers.xlsx",
    "counters": "scada_tap_counters_daily_2021-2026.csv",
    "topoil": "scada_top_oil_hourly_2021-2026.parquet",
    "log": "maintenance_log_2019-2026.xlsx",
    "standard": "ES-DGA-02_fleet_dga_condition_standard.pdf",
    "notes": "oil_results_notes.md",
    "bookings": "mobile_substation_bookings_2027-28.xlsx",
    "relay": "protection_relay_events_2025-2026.csv",
    "thermal": "thermal_imaging_survey_2026.pdf",
    "extract": "extract_log_2026-10-16.txt",
}
GAS_COLS = ["H2", "CH4", "C2H6", "C2H4", "C2H2", "CO", "CO2", "O2", "N2"]


def simulate():
    dl = sim.days()
    H = sim.hourly(dl)
    ops = sim.daily_ops(dl, H)
    cnt = sim.counters(dl, ops)
    R = lab.build(dl, H, ops, cnt)
    R["margin_log"] = lab.tune_margins(R)
    lab.moisture_and_temps(R, H)
    R["rs_log"] = lab.tune_latest_rs(R, H)
    lab.apply_reissues(R, H)
    R["comp"] = lab.compartments(R, dl, ops, cnt)
    return dl, H, ops, cnt, R


def lab_ids(R):
    """Laboratory sample numbers and report numbers in order of receipt (main tank and compartments)."""
    r = np.random.default_rng(W.SEED + 77)
    items = [(t, 0, i) for i, (tid, t, key) in enumerate(R["samples"])]
    items += [(c["sampled"], 1, k) for k, c in enumerate(R["comp"])]
    items.sort()
    seq, rseq, year = {}, 0, None
    main_ids, comp_ids = {}, {}
    for t, kind, i in items:
        yy = t.year % 100
        if yy not in seq:
            seq[yy] = int(r.integers(180, 760))
        seq[yy] += int(r.integers(1, 6))
        rseq += int(r.integers(1, 4))
        sid = f"WL{yy:02d}-{seq[yy]:05d}"
        rep = f"WLR-{yy:02d}{rseq % 100000:05d}"
        (main_ids if kind == 0 else comp_ids)[i] = (sid, rep)
    return main_ids, comp_ids


def sample_point(tid):
    return "Sampling valve, bottom" if W.UNIT[tid]["year"] >= 2000 else "Drain valve, bottom"


def write_main(path, R, ids):
    re_by_i = {}
    for i, field, v1, v2 in R["reissues"]:
        re_by_i[i] = (field, v1, v2)
    rows = []
    for i, (tid, t, key) in enumerate(R["samples"]):
        sid, rep = ids[i]
        g = R["rep"][i]
        temp = R["oil_temp"][i]
        base = [sid, tid, t.strftime("%Y-%m-%d %H:%M"), R["adates"][i].isoformat(), rep]
        tail = [str(R["moisture"][i]), "" if temp is None else f"{temp:.1f}", sample_point(tid)]
        if i in re_by_i:
            field, v1, v2 = re_by_i[i]
            t1 = list(tail)
            if field == "moisture_ppm":
                t1[0] = str(v1)
            else:
                t1[1] = "" if v1 is None else f"{v1:.1f}"
            rows.append(base + ["1"] + [g[c] for c in GAS_COLS] + t1)
            rows.append(base + ["2"] + [g[c] for c in GAS_COLS] + tail)
        else:
            rows.append(base + ["1"] + [g[c] for c in GAS_COLS] + tail)
    rows.sort(key=lambda x: (x[3], x[0], x[5]))
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["sample_id", "transformer_id", "sampled", "date", "report_no", "issue"] + GAS_COLS +
                    ["moisture_ppm", "oil_temp_c", "sample_point"])
        wr.writerows(rows)
    return len(rows)


def write_comp(path, R, ids):
    rows = []
    for k, c in enumerate(R["comp"]):
        sid, rep = ids[k]
        rows.append([sid, c["tid"], c["sampled"].strftime("%Y-%m-%d %H:%M"), R["adates"][c["main_i"]].isoformat(),
                     rep, "1"] + [c["rep"][g] for g in GAS_COLS] + [str(c["moisture"]), "Diverter compartment"])
    rows.sort(key=lambda x: (x[3], x[0]))
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["sample_id", "transformer_id", "sampled", "date", "report_no", "issue"] + GAS_COLS +
                    ["moisture_ppm", "sample_point"])
        wr.writerows(rows)
    return len(rows)


def write_counters(path, dl, cnt):
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["date", "transformer_id", "tap_ops_counter"])
        for i, d in enumerate(dl):
            ds = d.isoformat()
            for j, tid in enumerate(W.IDS):
                wr.writerow([ds, tid, int(cnt[i, j])])
    return len(dl) * len(W.IDS)


def write_topoil(path, H):
    n = len(H["utc"])
    ts = np.array(H["utc"].tz_localize(None).to_numpy(dtype="datetime64[s]"))
    ids, tcol, top, load = [], [], [], []
    for j, tid in enumerate(W.IDS):
        ids.append(np.full(n, tid, dtype=object))
        tcol.append(ts)
        top.append(np.round(H["top"][:, j], 1))
        load.append(np.round(H["load"][:, j], 2))
    tbl = pa.table({
        "transformer_id": pa.array(np.concatenate(ids).tolist(), type=pa.string()),
        "timestamp": pa.array(np.concatenate(tcol), type=pa.timestamp("s")),
        "top_oil_c": pa.array(np.concatenate(top), type=pa.float64()),
        "load_mva": pa.array(np.concatenate(load), type=pa.float64()),
    })
    pq.write_table(tbl, path, compression="snappy", row_group_size=500_000, use_dictionary=True)
    return tbl.num_rows


def main():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    dl, H, ops, cnt, R = simulate()
    main_ids, comp_ids = lab_ids(R)
    counts = {}
    counts["main"] = write_main(os.path.join(TARGET, F["main"]), R, main_ids)
    counts["comp"] = write_comp(os.path.join(TARGET, F["comp"]), R, comp_ids)
    counts["counters"] = write_counters(os.path.join(TARGET, F["counters"]), dl, cnt)
    counts["topoil"] = write_topoil(os.path.join(TARGET, F["topoil"]), H)
    docs.write_register(os.path.join(TARGET, F["register"]))
    counts["register"] = len(W.UNITS)
    counts["log"] = docs.write_log(os.path.join(TARGET, F["log"]), dl, ops, cnt, R)
    docs.write_bookings(os.path.join(TARGET, F["bookings"]))
    docs_pdf.write_standard(os.path.join(TARGET, F["standard"]))
    docs.write_notes(os.path.join(TARGET, F["notes"]), F)
    counts["relay"] = docs.write_relay_events(os.path.join(TARGET, F["relay"]))
    docs_pdf.write_thermal(os.path.join(TARGET, F["thermal"]), docs.thermal_findings())
    docs.write_extract_log(os.path.join(TARGET, F["extract"]), F,
                           {k: f"{v:,}" for k, v in counts.items()})
    for k in ("register", "log", "bookings"):
        docs.rewrite_ooxml(os.path.join(TARGET, F[k]), W.ORG)
    scrub = os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts",
                         "scrub_producer_metadata.py")
    # the contractor's report carries the contractor's name, everything else the organisation's
    side = os.path.join(TARGET, "_contractor")
    os.makedirs(side)
    shutil.move(os.path.join(TARGET, F["thermal"]), os.path.join(side, F["thermal"]))
    subprocess.run([sys.executable, scrub, side, "--apply", "--producer", "Weka Thermal Imaging", "--stamp",
                    "2026-04-02"], check=True, capture_output=True)
    shutil.move(os.path.join(side, F["thermal"]), os.path.join(TARGET, F["thermal"]))
    os.rmdir(side)
    subprocess.run([sys.executable, scrub, TARGET, "--apply", "--producer", W.ORG, "--stamp", "2026-10-16"],
                   check=True, capture_output=True)
    ts = dt.datetime(2026, 10, 16, 6, 52, tzinfo=W.TZ).timestamp()
    for fn in os.listdir(TARGET):
        os.utime(os.path.join(TARGET, fn), (ts, ts))
    # the golden deliverables and the task metadata, from the shipped bytes only
    subprocess.run([sys.executable, os.path.join(HERE, "golden.py"), "--write"], check=True, capture_output=True)
    subprocess.run([sys.executable, os.path.join(HERE, "metadata.py")], check=True, capture_output=True)
    print("design scores", [round(x, 4) for x in R["design_scores"]], "margin tweaks", len(R["margin_log"]))
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
