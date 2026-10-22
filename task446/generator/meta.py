"""Write task446/metadata.json from the cut pack, and cut target.zip last.

    python3 task446/generator/meta.py          metadata.json
    python3 task446/generator/meta.py --zip    target.zip (flat, sorted, fixed member times) and its receipt
"""
import hashlib
import json
import os
import sys
import zipfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make import DISTRACTORS, FILES  # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
DESC = {
    FILES["signals"]: "Early-warning engine month-end publications, one row per covered entity per month-end, "
                      "September 2022 to September 2026",
    FILES["lei"]: "GLEIF LEI-CDF 3.1 level 1 records for the Bank's entities and the engine's coverage list, GLEIF "
                  "concatenated file of 30 Sep 2026",
    FILES["rr"]: "GLEIF RR-CDF 2.1 level 2 relationship records, GLEIF concatenated file of 30 Sep 2026",
    FILES["repex"]: "GLEIF level 2 reporting exceptions, GLEIF concatenated file of 30 Sep 2026",
    FILES["obligors"]: "Credit system obligor master: customer, LEI, Companies House number, obligor group, booking entity",
    FILES["register"]: "Credit system obligor group register with relationship dates, ultimate parent LEI and sector",
    FILES["watchlist"]: "Watch-list cases opened since January 2020: placement, level, removal and reason",
    FILES["facilities"]: "Facility and obligor extract from the Halstow Bank plc and Halstow Bank Ireland DAC loan "
                         "ledgers, run 01:15 on 1 Oct 2026",
    FILES["limits"]: "Committed limit history for every facility, one row per version, to 7 Oct 2026",
    FILES["fx"]: "Group Treasury closing FX rates at 30 Sep 2026",
    FILES["triggers"]: "Early-warning trigger code list with feed and default signal",
    FILES["standard"]: "Early-Warning and Watch-List Monitoring Standard CRM-07 v3.1",
    FILES["close"]: "Credit Risk Monitoring year-end close timetable for the year to 30 Sep 2026",
    FILES["fieldref"]: "Reference Data field reference for the quarter-end credit extracts (data dictionary)",
    FILES["log"]: "Reference Data quarter-end extract log: jobs, run times, row counts and the control check "
                  "(provenance)",
    FILES["ratings"]: "Internal rating master scale and group ratings at 30 Sep 2026",
    FILES["outlook"]: "Group Economics UK outlook, October 2026: central, downside and severe downside paths",
}


def rows(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(ws.max_row for ws in wb.worksheets)
    return None


def main():
    shipped = sorted(os.listdir(TARGET))
    assert set(shipped) == set(DESC), set(shipped) ^ set(DESC)
    files = []
    for f in shipped:
        p = os.path.join(TARGET, f)
        files.append(dict(path=f, format=f.rsplit(".", 1)[1], bytes=os.path.getsize(p), rows=rows(p),
                          source="Constructed: " + DESC[f], date="2026-10-08",
                          license="CC0-1.0 (original work, constructed for this task)"))
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task446",
        "title": "How many obligor groups from the monitored book will reach the watch list in the year to "
                 "30 September 2027",
        "domain": "Banking, Credit & Financial Risk",
        "subdomain": "credit-scoring-pd-modeling (early-warning and watch-list monitoring of corporate obligor groups)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "05 (allocation to a fixed total): the caseload allocated over the five exposure bands, each band "
                        "with the groups it holds, their committed exposure, the groups the September early-warning run "
                        "flagged, the expected arrivals and the committed exposure they are expected to bring, with a "
                        "total row",
        "as_of": "2026-10-08",
        "deliverables": ["watchlist_inflow_2027.xlsx", "watchlist_inflow_2027.svg"],
        "distractor_files": list(DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task446/generator/make.py (seeded, deterministic) around "
                               "a fictional UK bank (Halstow Bank plc, with Halstow Bank Ireland DAC) and fictional "
                               "borrowers, on GLEIF's published concatenated-file CSV schemas (LEI-CDF 3.1, RR-CDF 2.1, "
                               "reporting exceptions) with valid ISO 17442 LEI check digits; managing LOU identifiers "
                               "are real LOU LEIs; no real borrower, bank exposure or GLEIF record is depicted",
                     "date": "2026-10-08", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task446/generator/make.py",
        "files": files,
    }
    assert meta["input_gates"]["files"] >= 10 and len(meta["input_gates"]["formats"]) >= 3
    assert big["rows"] >= 25000 and len(meta["distractor_files"]) >= 2
    with open(os.path.join(HERE, "..", "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(meta["input_gates"]), meta["distractor_files"])


def cut_zip():
    out = os.path.join(HERE, "..", "target.zip")
    names = sorted(os.listdir(TARGET))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=(2026, 10, 8, 17, 42, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, n), "rb") as fh:
                z.writestr(zi, fh.read())
    with zipfile.ZipFile(out) as z:
        members = z.namelist()
        assert members == names and all("/" not in m for m in members)
        for n in names:
            with open(os.path.join(TARGET, n), "rb") as fh:
                assert z.read(n) == fh.read(), n
    digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("target.zip %d bytes, %d members, sha256 %s" % (os.path.getsize(out), len(members), digest))


if __name__ == "__main__":
    if "--zip" in sys.argv:
        cut_zip()
    else:
        main()
