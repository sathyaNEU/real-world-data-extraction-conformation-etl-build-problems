"""Build task402: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then a second full cut compared byte for byte, and target.zip from the final build.

    python3 task402/generator/build.py              everything
    python3 task402/generator/build.py --out DIR    the pack only, into DIR
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

import numpy as np  # noqa: E402
import docs as DC  # noqa: E402
import golden as GD  # noqa: E402
import harness as H  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = 1778490000  # 2026-05-11 09:00 UTC, the pack's export date


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def cut(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = W.simulate()
    pk = PK.build(out, w)
    m = H.measure(w)
    DC.plan_docx(out)
    DC.kpi_pdf(out, m, w, np.random.default_rng(40222))
    for fn in os.listdir(out):
        os.utime(os.path.join(out, fn), (STAMP, STAMP))
    return w, m, pk


def zip_target(target, dest):
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=(2026, 5, 11, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


METADATA = {
    "task": "task402",
    "decision": "Which change on an NHS Talking Therapies service's 2025-26 improvement list gets the commissioner's "
                "2026-27 improvement fund, with the recoveries it cost, a monthly chart of recoveries, and evidence "
                "tables for the list's other lines.",
    "deliverables": ["improvement_case_2026-27.pptx", "review_evidence_2025-26.xlsx"],
    "distractor_files": ["target/quillfern_module_completions_2025-04_to_2025-06.csv",
                         "target/stress_management_groups_schedule_2024-04_to_2025-08.csv"],
    "licence": "CC BY 4.0 (synthetic records generated for this task; the service, the provider, the integrated care "
               "board, the agencies, the digital vendors and every person are fictional)",
    "files": {
        "referrals_received_2023-10_to_2026-03.csv": "Clinical system referral extract, refreshed 6 May 2026. Synthetic.",
        "care_contacts_2023-10-02_to_2025-10-12.csv": "Previous clinical system appointment export to its close on 12 October 2025. Synthetic.",
        "outcome_measures_items_2023-10-02_to_2025-10-12.csv": "Previous clinical system questionnaire item export. Synthetic.",
        "appointments_2025-10-13_to_2026-05-06.parquet": "Clinical system appointment export from 13 October 2025. Synthetic.",
        "clinical_system_users_2026-05-06.xlsx": "Clinical system user list, 6 May 2026. Synthetic.",
        "agency_bookings_psychological_therapies_2025-26.xlsx": "People team agency booking register export, 5 May 2026. Synthetic.",
        "agency_timesheets_2025-04_to_2026-03.csv": "Agency timesheet portal export, 2025-26. Synthetic.",
        "step3_waiting_list_month_end_2025-04_to_2025-09.csv": "Waiting list module month-end snapshots, previous system. Synthetic.",
        "step3_waiting_list_month_end_2025-10_to_2026-03.csv": "Waiting list module month-end snapshots, current system. Synthetic.",
        "steadyway_activity_export_2025-07_to_2026-05.json": "Digital CBT vendor activity export, 6 May 2026. Synthetic.",
        "quillfern_module_completions_2025-04_to_2025-06.csv": "Previous digital CBT vendor's final completions export. Synthetic.",
        "stress_management_groups_schedule_2024-04_to_2025-08.csv": "Group programme schedule. Synthetic.",
        "improvement_plan_2026-27.docx": "Integrated care board improvement plan for the contract, version 2.0. Constructed.",
        "monthly_performance_report_2026-03_provisional.pdf": "Provider's provisional monthly performance report, March 2026. Constructed.",
    },
    "dates": {"pack_export": "2026-05-11", "refreshed_extract": "2026-05-06"},
}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.out:
        cut(a.out)
        return 0
    target = os.path.join(TASK, "target")
    w, m, pk = cut(target)
    f = GD.figures(w, m, pk)
    json.dump(f, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=False)
    gdir = os.path.join(TASK, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    GD.deliverables(gdir, f)
    WU.write(os.path.join(TASK, "submission.md"), f)
    json.dump(METADATA, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    d1 = digest(target)
    tmp = tempfile.mkdtemp()
    cut(os.path.join(tmp, "target"))
    d2 = digest(os.path.join(tmp, "target"))
    shutil.rmtree(tmp)
    print("digest 1", d1)
    print("digest 2", d2)
    assert d1 == d2, "the two cuts differ"
    zip_target(target, os.path.join(TASK, "target.zip"))
    print("target.zip", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
