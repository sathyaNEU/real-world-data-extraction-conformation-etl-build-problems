"""Build task400: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then a second full cut compared byte for byte, and target.zip from the final build.

    python3 task400/generator/build.py              everything
    python3 task400/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import deliver as DL  # noqa: E402
import pack as PK     # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def zip_target(target, dest):
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=(2026, 11, 2, 7, 15, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


METADATA = {
    "task": "task400",
    "decision": "Which programme on the Mount Bracken site safety steering committee's list to fund for 2027 against the "
                "rise in vehicle interaction incidents, with the incident counts, a monthly chart, pit gate trips and ramp "
                "overspeed figures.",
    "deliverables": ["vi_programme_paper_2027.docx", "vi_workings_2026.xlsx"],
    "distractor_files": ["haul_road_dust_pm10_2026.csv", "road_maintenance_log_2026.csv"],
    "licence": "CC BY 4.0 (synthetic records generated for this task; the mine, its owner, its contractors, the vendor, "
               "the inspectorate and every person are fictional)",
    "files": {
        "cas_alert_events_2025-01_2026-10.parquet": "Collision avoidance supplier portal alert export, January 2025 to October 2026. Synthetic.",
        "fms_event_windows_2025-2026.parquet": "Fleet management system event window export, January 2025 to October 2026. Synthetic.",
        "dispatch_shift_summary_2025-2026.csv": "Fleet management system shift summaries, January 2025 to October 2026. Synthetic.",
        "pit_gate_reads_2026-07_2026-10.csv": "Pit access gate reader export (number plate and collision avoidance tag reads), July to October 2026. Synthetic.",
        "incident_register_2025-01_2026-10.xlsx": "Site incident register export, January 2025 to October 2026. Synthetic.",
        "cas_device_register_2026-10-31.xlsx": "Collision avoidance supplier portal asset export, 31 October 2026. Synthetic.",
        "site_location_codes.csv": "Site location code list. Synthetic.",
        "light_vehicle_register.csv": "Site light vehicle register. Synthetic.",
        "haul_road_speed_limits.csv": "Haul road speed limit schedule with effective dates. Synthetic.",
        "haul_road_dust_pm10_2026.csv": "Haul road dust monitor hourly PM10, 2026. Synthetic.",
        "road_maintenance_log_2026.csv": "Haul road maintenance task log, 2026. Synthetic.",
        "vi_review_terms_2026.docx": "Site document: vehicle interaction review terms of reference. Constructed.",
        "improvement_notice_IN-2026-0417.pdf": "Inspectorate improvement notice. Constructed.",
        "cas_monthly_report_2026-10.pdf": "Collision avoidance supplier's monthly fleet performance report, October 2026. Constructed.",
    },
    "dates": {"pack_export": "2026-11-02"},
}


def cut(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    return PK.cut(out)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-second", action="store_true")
    a = ap.parse_args(argv)
    if a.out:
        cut(a.out)
        return 0
    target = os.path.join(TASK, "target")
    R = cut(target)
    F, P, resp, rs = DL.figures(target)
    F.update(WU.extra_figures(P, resp))
    golden = os.path.join(TASK, "golden")
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    DL.paper_docx(os.path.join(golden, "vi_programme_paper_2027.docx"), F)
    DL.workings_xlsx(os.path.join(golden, "vi_workings_2026.xlsx"), F)
    json.dump({k: v for k, v in F.items() if k != "monthly"} | {"monthly": [[ym, v] for ym, v in F["monthly"]]},
              open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    open(os.path.join(TASK, "submission.md"), "w").write(WU.submission(F))
    json.dump(METADATA, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    d1 = digest(target)
    if not a.no_second:
        tmp = tempfile.mkdtemp(prefix="t400b_")
        cut(os.path.join(tmp, "target"))
        d2 = digest(os.path.join(tmp, "target"))
        shutil.rmtree(tmp)
        print("rebuild byte-identical:", d1 == d2)
        if d1 != d2:
            return 1
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("target digest", d1[:12], "zip md5", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
