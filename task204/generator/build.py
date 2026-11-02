"""The one entry point: build the pack twice, assert byte-identical, install target/, golden/, figures.json,
metadata.json, target.zip and submission.md."""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis      # noqa: E402
import golden        # noqa: E402
import pack          # noqa: E402
import params as P   # noqa: E402

ZIP_TIME = (2026, 5, 15, 9, 0, 0)


def digest(folder):
    h = hashlib.sha256()
    for root, dirs, files in sorted(os.walk(folder)):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def figures(res):
    teams = golden.team_rows(res)
    covered = sorted({d for t in res["golden"] for d in t["districts"]}, key=lambda s: int(s[1:]))
    sim = max((len(v) for v in res["simultaneous"].values()), default=0)
    f = {
        "n_teams": len(res["golden"]),
        "teams": [{"label": t["label"], "districts": [d[1:] for d in t["districts"]], "n": t["n"]} for t in teams],
        "eastline_trips": len(res["runs"]),
        "simultaneous_evenings": sim,
        "no_series_districts": [d[1:] for d in ["D%d" % k for k in range(1, 11)] if d not in covered],
        "rung0_teams": len(res["rung0"]),
        "rung1_teams": len(res["rung1"]),
        "rung2_teams": len(res["rung2"]),
        "rung2_merged_n": max(t["n"] for t in res["rung2"]),
        "ask_a": {d: res["ask_a"][d] for d in sorted(res["ask_a"], key=lambda s: int(s[1:]))},
        "ask_a_total": sum(sum(v) for v in res["ask_a"].values()),
        "ask_b": res["ask_b"],
        "ask_c": res["ask_c"],
        "review_period": ["2026-02-09", "2026-05-03"],
        "n_group_scope": res["n_group_scope"],
    }
    return f


METADATA_FILES = {
    "rms_occurrence_extract_20260511.csv": ("evidence", "Carvale Police Service records management system, occurrence extract pulled 11 May 2026 (all occurrence types, 2 Feb to 11 May 2025 and 2 Feb to 10 May 2026); synthetic, built for this task"),
    "tpo_occurrence_log_2025_2026.xlsx": ("evidence", "Carvale Transit Security Operations, transit peace officer occurrence log export of 11 May 2026; synthetic"),
    "carvale_transit_codes.xlsx": ("evidence", "Carvale Transit fare systems code list, revision 14 of 30 March 2026; synthetic"),
    "fare_gate_entries_hourly_2026.csv": ("evidence", "Carvale Transit fare system, hourly entries by gate, 2 Feb to 10 May 2026; synthetic"),
    "fare_gate_daily_summary_2025.csv": ("evidence", "Carvale Transit fare system archived daily summary by gate, 3 Feb to 11 May 2025; synthetic"),
    "gtfs/agency.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/routes.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/stops.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/trips.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/stop_times.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/frequencies.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/calendar.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/calendar_dates.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "gtfs/feed_info.txt": ("evidence", "Carvale Transit GTFS feed 2026.03.29-r2; synthetic"),
    "patrol_districts_2026.geojson": ("evidence", "Carvale Police Service patrol district boundaries in force from 1 January 2026; synthetic"),
    "patrol_districts_2025.geojson": ("evidence", "Carvale Police Service patrol district boundaries 2019 to 2025 (archived layout); synthetic"),
    "ops41_series_crime_response_directive.pdf": ("evidence", "Carvale Police Service Operational Directive OPS-41, version 2.1; synthetic"),
    "cau_lrt_station_reference_2026.pdf": ("evidence", "Carvale Police Service Crime Analysis Unit station reference, revised 6 April 2026; synthetic"),
    "summer_deployment_planning_note.docx": ("evidence", "Deputy Chief (Operations) planning note of 4 May 2026; synthetic"),
    "secondhand_dealer_phone_returns_2026q1.csv": ("distractor", "Second-hand dealer bylaw returns for phones bought January to March 2026; synthetic"),
    "cpsd_school_year_calendar_2025_26.pdf": ("distractor", "Carvale Public School Division 2025-2026 school year calendar; synthetic"),
}


def metadata():
    files = {}
    for name, (role, src) in sorted(METADATA_FILES.items()):
        files[name] = {"date": "2026-05-15", "license": "synthetic, CC0", "role": role, "source": src}
    return {"architecture": 2, "as_of": "2026-05-15",
            "decision": "how many OPS-41 series teams the Carvale Police Service summer deployment plan stands up for the "
                        "spring 2026 phone robberies and thefts from the person, and the patrol districts each team covers",
            "deliverables": ["series_assessment_2026.xlsx", "summer_series_deployment_memo.docx"],
            "distractor_files": [n for n, (r, s) in sorted(METADATA_FILES.items()) if r == "distractor"],
            "files": files}


def build_once(root):
    target = os.path.join(root, "target")
    gold = os.path.join(root, "golden")
    w = pack.make_world()
    info = pack.write_pack(w, target)
    res = analysis.run_all(target)
    golden.write_golden(gold, res)
    fig = figures(res)
    return target, gold, fig, info, res, w


def zip_target(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in sorted(os.walk(target)):
            dirs.sort()
            for f in sorted(files):
                p = os.path.join(root, f)
                arc = os.path.join("target", os.path.relpath(p, target))
                zi = zipfile.ZipInfo(arc, date_time=ZIP_TIME)
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, open(p, "rb").read())


def main():
    a = tempfile.mkdtemp(prefix="t204a_")
    b = tempfile.mkdtemp(prefix="t204b_")
    ta, ga, fa, ia, res, w = build_once(a)
    tb, gb, fb, ib, _, _ = build_once(b)
    da, db = digest(ta), digest(tb)
    gda, gdb = digest(ga), digest(gb)
    assert da == db, "target differs between builds"
    assert gda == gdb, "golden differs between builds"
    assert fa == fb, "figures differ between builds"
    for name in ("target", "golden"):
        dst = os.path.join(TASK, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, name), dst)
        for root, dirs, files in os.walk(dst):
            for f in files:
                st = os.stat(os.path.join(a, name, os.path.relpath(os.path.join(root, f), dst)))
                os.utime(os.path.join(root, f), (st.st_mtime, st.st_mtime))
    json.dump(fa, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    zip_target(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    import writeup
    writeup.main()
    zd = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("build ok: target %s golden %s zip %s rms %d tpo %d" % (da[:16], gda[:16], zd[:8], ia["rms_rows"], ia["tpo_rows"]))
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
