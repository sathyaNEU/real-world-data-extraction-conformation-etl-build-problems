"""Builds task259 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
submission.md, metadata.json, generator/figures.json and target.zip.

    python3 task259/generator/build.py
"""
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
import analysis  # noqa: E402
import common  # noqa: E402
import docs  # noqa: E402
import golden  # noqa: E402
import pack  # noqa: E402
import world  # noqa: E402
import writeup  # noqa: E402

AS_OF = "2026-10-23"
LIC = "synthetic, CC0"
FILES = {
    "HES_PERSON_2025Q1_2026Q3.csv": ("evidence", "Tamarack Household Employment Survey person-level estimation "
                                     "extract, 2025Q1 to 2026Q3; synthetic, built for this task"),
    "HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv": ("evidence", "HES field operations disposition extract from the "
                                                     "CAPI v3 and CAPI 2026 systems; synthetic"),
    "HES_CASEID_CROSSWALK_CAPI2026.csv": ("evidence", "HES case number crosswalk written at the CAPI 2026 migration; "
                                          "synthetic"),
    "HES_FRAME_MAINTENANCE_2024-07_2026-09.csv": ("evidence", "Tamarack master address file maintenance log; "
                                                  "synthetic"),
    "HES_DISPOSITION_CODES.csv": ("evidence", "HES disposition code list for both CAPI systems; synthetic"),
    "HES_PERSON_CODES.csv": ("evidence", "HES person file code list as published with the public-use files; synthetic"),
    "HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx": ("evidence", "HES final person weights by quarter, with the 2026Q3 "
                                             "reissue; synthetic"),
    "TDLI_WORKFORCE_AREAS_2026.xlsx": ("evidence", "TDLI workforce development area designations, 2026; synthetic"),
    docs.RULE_FILE: ("evidence", "Tamarack Administrative Rules, portable benefits pilot chapter; synthetic"),
    docs.NOTE_FILE: ("evidence", "HES technical note, September 2026; synthetic"),
    docs.RELEASE_FILE: ("evidence", "HES quarterly release, third quarter 2026, preliminary; synthetic"),
    "QCEW_WDA_SECTOR_2025.csv": ("distractor", "Quarterly census of employment and wages, 2025 annual averages by "
                                 "workforce area and sector; synthetic"),
    "LAUS_WDA_MONTHLY_2025-07_2026-09.csv": ("distractor", "Local area unemployment statistics by workforce area, "
                                             "monthly; synthetic"),
}


def metadata(rows):
    return {
        "task": "task259", "architecture": 2, "as_of": AS_OF,
        "decision": "which workforce development areas the Tamarack Department of Labor and Industry certifies for "
                    "its 2027 portable benefits pilot under its pilot-area rule",
        "deliverables": [golden.WB, golden.MEMO],
        "files": {f: {"role": r, "source": s, "date": AS_OF, "license": LIC} for f, (r, s) in sorted(FILES.items())},
        "distractor_files": sorted(f for f, (r, s) in FILES.items() if r == "distractor"),
        "largest_file": {"name": "HES_PERSON_2025Q1_2026Q3.csv", "rows": rows["HES_PERSON_2025Q1_2026Q3.csv"]},
        "row_counts": rows,
    }


def build_once(out):
    W = world.build_world()
    tdir = os.path.join(out, "target")
    pack.write_target(W, tdir)
    L = analysis.load(tdir)
    F, M = analysis.figures(L)
    golden.write_goldens(F, os.path.join(out, "golden"))
    writeup.write(F, M, os.path.join(out, "submission.md"), os.path.join(out, "figures.json"))
    rows = {f: sum(1 for _ in open(os.path.join(tdir, f), encoding="utf-8")) - 1
            for f in sorted(os.listdir(tdir)) if f.endswith(".csv")}
    with open(os.path.join(out, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(rows), f, indent=1, sort_keys=True)
        f.write("\n")
    make_zip(tdir, os.path.join(out, "target.zip"))
    common.set_mtime(out)
    return W, F, M


def make_zip(tdir, path):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(tdir)):
            zi = zipfile.ZipInfo(fn, date_time=common.EXPORT_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tdir, fn), "rb").read())


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def main():
    a, b = tempfile.mkdtemp(prefix="t259a_"), tempfile.mkdtemp(prefix="t259b_")
    try:
        build_once(a)
        build_once(b)
        da, db = digest(a), digest(b)
        diff = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        if diff:
            print("BUILDS DIFFER:", diff)
            return 1
        print("two builds byte-identical: %d files" % len(da))
        for sub in ("target", "golden"):
            dst = os.path.join(TASK, sub)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(os.path.join(a, sub), dst)
        shutil.copy2(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
        shutil.copy2(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
        shutil.copy2(os.path.join(a, "figures.json"), os.path.join(HERE, "figures.json"))
        shutil.copy2(os.path.join(a, "target.zip"), os.path.join(TASK, "target.zip"))
        common.set_mtime(os.path.join(TASK, "target"))
        print("target.zip sha256 %s" % hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
        return 0
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
