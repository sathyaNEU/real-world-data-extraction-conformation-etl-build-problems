"""task229 generator: build the evidence pack.

    python3 task229/generator/build.py [--out DIR]

Writes DIR/target/ and DIR/metadata.json (DIR defaults to the task folder)."""
import argparse
import json
import os
import shutil
import sys
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import params as P     # noqa: E402
import world as W      # noqa: E402
import truth as T      # noqa: E402
import records as R    # noqa: E402
import docs            # noqa: E402
import ship            # noqa: E402

F = {
    "standard": "hydrometric_data_standard_ed2.pdf",
    "plan": "data_plan_2027.docx",
    "register": "station_register.xlsx",
    "ratings": "rating_book_issue2_2026.pdf",
    "daily": "daily_records_wy2023_wy2026.csv",
    "gaugings": "gaugings_2016_2026.csv",
    "outlook": "water_supply_outlook_2027.xlsx",
    "ops": "corriston_hydro_operating_plan_2027.pdf",
    "migration": "telemetry_migration_2026.xlsx",
    "visits": "field_visits_wy2026.csv",
    "dictionary": "data_dictionary.csv",
    "flood": "flood_frequency_update_2025.pdf",
    "quality": "water_quality_grab_samples_2026.csv",
    "manifest": "export_manifest.csv",
}
DISTRACTORS = ["flood", "quality", "visits"]
DESC = {
    F["standard"]: ("the network's hydrometric data standard, edition 2 (March 2025)", "hydrometric section"),
    F["plan"]: ("the network's 2027 data plan for the water licence inspector", "data quality manager"),
    F["register"]: ("the station register, every station including closed ones", "data quality manager"),
    F["ratings"]: ("the rating book, issue 2: the ratings in force and their gauged ranges", "hydrometric section"),
    F["daily"]: ("daily water level and discharge, every row the data system holds, 1 October 2022 to 30 September 2026", "hydrometric database export"),
    F["gaugings"]: ("field discharge measurements, water years 2017 to 2026", "gauging software export"),
    F["outlook"]: ("the 2027 water supply outlook, monthly flows by station", "hydrologist"),
    F["ops"]: ("Corriston Hydro Ltd.'s 2027 operating plan for the Corriston and Merrin systems", "Corriston Hydro Ltd."),
    F["migration"]: ("the 2026 telemetry migration tracker", "data quality manager"),
    F["visits"]: ("field visits, water year 2026", "field crews"),
    F["dictionary"]: ("column definitions for the exports", "hydrometric section"),
    F["flood"]: ("flood frequency update, 2025", "hydrometric section"),
    F["quality"]: ("monthly water quality grab samples, water year 2026", "environmental monitoring"),
    F["manifest"]: ("this list", "hydrometric section"),
}
MTIME = {
    "standard": "2025-03-14 10:12", "plan": "2026-11-05 14:15", "register": "2026-10-02 09:05",
    "ratings": "2026-06-30 15:40", "daily": "2026-11-06 07:31", "gaugings": "2026-11-06 07:34",
    "outlook": "2026-11-02 09:35", "ops": "2026-10-19 13:02", "migration": "2026-09-29 14:10",
    "visits": "2026-11-06 07:36", "dictionary": "2026-11-06 07:38", "flood": "2025-12-09 11:20",
    "quality": "2026-10-28 16:44", "manifest": "2026-11-06 07:40",
}


def flood_peaks(TR):
    out = []
    for no in W.CURRENT:
        if no in W.PLANT_OF or no in W.SPRING or no in ("C122",):
            continue
        s = TR["S"][no].reshape(T.NDAY, T.SPD).max(axis=1)
        yrs = []
        for wy in range(2017, 2026):
            a, b = (date(wy - 1, 10, 1) - T.T0).days, (date(wy, 9, 30) - T.T0).days
            yrs.append(s[a:b + 1].max())
        yrs = np.array(yrs)
        m, sd = yrs.mean(), yrs.std(ddof=1)
        q2 = m - 0.164 * sd
        n_years = 2025 - max(W.ESTABLISHED[no], 1975)
        out.append((no, W.ST[no]["name"], n_years, q2, q2 + 1.30 * sd, q2 + 2.43 * sd, q2 + 3.42 * sd))
    return out


def write_pack(out):
    tgt = os.path.join(out, "target")
    if os.path.isdir(tgt):
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    p = lambda k: os.path.join(tgt, F[k])
    TR = T.build_truth()
    DR = R.daily_record(TR)
    G = R.gaugings(TR)
    GR = R.gauged_ranges(G)
    docs.standard(p("standard"))
    docs.data_plan(p("plan"))
    docs.rating_book(p("ratings"), GR)
    docs.operating_plan(p("ops"))
    docs.flood_frequency(p("flood"), flood_peaks(TR))
    ship.daily_record(DR, p("daily"))
    ship.gaugings(G, p("gaugings"))
    ship.register(p("register"))
    ship.outlook(p("outlook"))
    ship.migration(p("migration"))
    ship.visit_log(R.visit_rows(G, DR), p("visits"))
    ship.dictionary(p("dictionary"))
    ship.water_quality(np.random.default_rng([P.SEED, 900]), TR, p("quality"))
    ship.manifest(p("manifest"), [F[k] for k in F], DESC, {F[k]: MTIME[k][:10] for k in F})
    return tgt, {"TR": TR, "DR": DR, "G": G, "GR": GR}


def set_mtimes(tgt):
    for k, when in MTIME.items():
        ts = pd.Timestamp(when).tz_localize(P.TZ).timestamp()
        os.utime(os.path.join(tgt, F[k]), (ts, ts))


def metadata(out, tgt):
    files, fmts = [], set()
    biggest, rows = None, 0
    for name in sorted(os.listdir(tgt)):
        ext = name.rsplit(".", 1)[1]
        fmts.add(ext)
        path = os.path.join(tgt, name)
        n = None
        if ext == "csv":
            n = sum(1 for _ in open(path, encoding="utf-8")) - 1
        if n and n > rows:
            biggest, rows = name, n
        files.append({"path": name, "format": ext, "bytes": os.path.getsize(path), "rows": n,
                      "source": "Constructed for this task: the fictional Corriston Basin Hydrometric Cooperative's "
                                "network and Corriston Hydro Ltd.; no third-party data",
                      "date": "2026-11-06", "license": "CC0-1.0 (original work)"})
    meta = {
        "task": "task229",
        "title": "From which month of 2027 each hydrometric station's published daily discharge carries the below-grade-B flag",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "sensor-calibration-measurement",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "13 (scenarios and the flip point)",
        "as_of": P.AS_OF.isoformat(),
        "deliverables": ["discharge_grades_2027.png", "record_review_wy2026.xlsx"],
        "distractor_files": [F[k] for k in DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted(fmts), "largest_file": biggest, "largest_file_rows": rows},
        "files": files,
    }
    with open(os.path.join(out, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.abspath(os.path.join(HERE, "..")))
    a = ap.parse_args()
    tgt, B = write_pack(a.out)
    meta = metadata(a.out, tgt)
    set_mtimes(tgt)
    print("build ok:", tgt, meta["input_gates"])


if __name__ == "__main__":
    main()
