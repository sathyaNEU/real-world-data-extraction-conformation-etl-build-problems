"""task304 architecture 4: build the pack twice, assert the two builds are byte-identical, then install target/,
golden/, generator/figures.json, metadata.json, submission.md and target.zip."""
import filecmp
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

import golden  # noqa: E402
import pack  # noqa: E402
import results  # noqa: E402
import writeup  # noqa: E402

ZIP_TIME = (2026, 11, 16, 9, 0, 0)

PROVENANCE = {
    "wcs_operator_sessions_export_20261116.csv": ("Brolga Parcel Network sorter control system (WCS), operator session export pulled 16 November 2026", "induct station log-ons and log-offs at six hubs, 28 September to 8 November 2026, UTC"),
    "badge_register_20261113.xlsx": ("Brolga site security access-control register, export 13 November 2026", "badges issued to employees, labour-hire operatives and contractors, with issue and cancel dates"),
    "hr_employee_list_20261113.csv": ("Brolga HR system, employee list 13 November 2026", "employees by site, position title and roster team"),
    "ta_shift_records_20260928_20261108.csv": ("Brolga time and attendance system", "employees' rostered shifts and their status, 28 September to 8 November 2026"),
    "labour_hire_timesheets_oct_nov_2026.xlsx": ("Tasman Workforce and Meridian Labour Hire client timesheets", "labour-hire operatives' shifts at Brolga hubs, 28 September to 8 November 2026"),
    "induct_station_register.xlsx": ("Brolga engineering asset register (sorters)", "induct stations by site and their commissioning"),
    "noise_survey_report_2026.pdf": ("Kestrel Acoustics report KA-2611-R1, 30 September 2026", "area noise levels at the six hubs, August and September 2026"),
    "induct_enclosure_design_report_rev2.pdf": ("Quellmark Acoustic Engineering project QAE-0927 revision 2, 22 October 2026", "the induct-line enclosure design: predicted levels and prices by hub"),
    "noise_enforceable_undertaking_schedule_2027.pdf": ("Brolga Parcel Network, noise enforceable undertaking, Schedules 2 and 3, 6 November 2026", "the 2027 engineering control's placement and the audiometric testing terms"),
    "boundary_noise_complaints_2026.csv": ("Brolga community relations complaint log", "neighbours' noise complaints at hub boundaries, 2026"),
    "sort_volumes_daily_2026.csv": ("Brolga network operations daily volumes", "parcels sorted and peak hourly rate by hub, July to November 2026"),
    "ppe_vending_transactions_2026q3.json": ("SafeStock Cloud vend transaction export, 6 October 2026", "PPE vending machine transactions at Brolga hubs, 29 June to 2 October 2026, UTC"),
    "ppe_vending_service_visits_2026q3.csv": ("SafeStock service and restock visit log", "restock, range change and commissioning visits by machine and site, July to September 2026"),
    "ppe_vending_asset_list_20260930.xlsx": ("SafeStock asset list as at 30 September 2026", "machines on the Brolga account and the product list"),
    "audiometry_results_2025_2026.csv": ("ClearTone Occupational Audiology test export", "hearing test thresholds at 2, 3 and 4 kHz for enrolled workers, baselines and 2025 to 2026 tests"),
    "audiometry_clients_20261106.xlsx": ("ClearTone Occupational Audiology client list, 6 November 2026", "enrolled workers with their employee numbers and reference tests"),
    "hr_site_transfers_2026.csv": ("Brolga HR system, site transfers 2026", "employees who moved between hubs in 2026 and the effective dates"),
}


def build_into(out):
    pk = pack.build(out)
    return pk


def tree_equal(a, b):
    names_a, names_b = sorted(os.listdir(a)), sorted(os.listdir(b))
    if names_a != names_b:
        return False, "file lists differ"
    for n in names_a:
        if not filecmp.cmp(os.path.join(a, n), os.path.join(b, n), shallow=False):
            return False, n
    return True, ""


def metadata(target):
    files = []
    for n in sorted(os.listdir(target)):
        src, cov = PROVENANCE[n]
        files.append({"path": "target/" + n, "source": src, "covers": cov, "made": "constructed by the task's seeded generator in the source system's export format",
                      "licence": "synthetic, released with the task under CC BY 4.0", "date": "2026-11-16"})
    return {
        "task": "task304",
        "decision": "which sortation hub receives the 2027 induct-line enclosure under the noise undertaking's schedule, and the workers it brings below the 85 dB(A) exposure standard at each hub",
        "deliverables": ["induct_enclosure_2027.pptx", "hearing_program_2026.csv"],
        "distractor_files": ["target/boundary_noise_complaints_2026.csv", "target/sort_volumes_daily_2026.csv"],
        "as_of": "2026-11-27",
        "files": files,
    }


def zip_target(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, n), "rb").read())


def main():
    tmp = tempfile.mkdtemp(prefix="t304b_")
    a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
    build_into(a)
    build_into(b)
    ok, why = tree_equal(a, b)
    if not ok:
        print("BUILD NOT BYTE-IDENTICAL:", why)
        sys.exit(1)
    target = os.path.join(TASK, "target")
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(a, target)
    for n in os.listdir(target):
        st = os.stat(os.path.join(a, n))
        os.utime(os.path.join(target, n), (st.st_mtime, st.st_mtime))
    F = results.write(target, os.path.join(HERE, "figures.json"))
    gdir = os.path.join(TASK, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    golden.write(gdir, F)
    writeup.write(os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    json.dump(metadata(target), open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8"), indent=1)
    zip_target(target, os.path.join(TASK, "target.zip"))
    h = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    # a second zip from the second build must match
    zip_target(b, os.path.join(tmp, "b.zip"))
    h2 = hashlib.sha256(open(os.path.join(tmp, "b.zip"), "rb").read()).hexdigest()
    shutil.rmtree(tmp)
    if h != h2:
        print("ZIPS DIFFER")
        sys.exit(1)
    print("built: two byte-identical builds; target.zip sha256 %s" % h[:16])
    print("call: %s %d brought below (runner-up %s %d)" % (F["call_hub"], F["call_below"], F["runner_up"], F["runner_up_below"]))


if __name__ == "__main__":
    main()
