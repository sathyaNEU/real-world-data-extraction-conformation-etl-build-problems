"""metadata.json beside target/: what the task is about, the deliverables, the distractors and each file's
provenance. It names the decision and never the method, the link or the mechanism."""
from __future__ import annotations

import csv
import json
import os

import openpyxl

import common as K
import deliver as DL
import docs as D
import records as R

DISTRACTORS = [R.F_QUALITY, R.F_RAIN]

FILES = {
    R.F_TEST: ("Constructed: Brackenholt Spring Water, constant-rate pumping test of Borehole 2, June 2014, logger "
               "downloads and field sheet", "2014-06-14"),
    R.F_OBS: ("Constructed: Brackenholt Spring Water, observation borehole monthly mean levels under licence "
              "condition 9, as returned to March 2026", "2026-04-22"),
    R.F_RMB: ("Constructed: the licensing authority's regional observation borehole at Windle Cross, daily levels",
              "2026-10-01"),
    R.F_SURVEY: ("Constructed: site survey of boreholes, 2026", "2026-03-11"),
    R.F_TELEM: ("Constructed: Brackenholt Spring Water, site telemetry export, 15-minute meter registers and tank "
                "level", "2026-10-02"),
    R.F_PUMP: ("Constructed: Borehole 2 wellhead pump controller event log", "2026-10-02"),
    R.F_TICKETS: ("Constructed: Teme Valley Bulk Liquids, monthly statements of bulk loads, April to September "
                  "2026", "2026-10-05"),
    R.F_RUNS: ("Constructed: Brackenholt Spring Water, manufacturing execution system order export", "2026-10-02"),
    R.F_SKU: ("Constructed: Brackenholt Spring Water, product master export", "2026-10-02"),
    R.F_QC: ("Constructed: Brackenholt Spring Water, quality control net fill weight samples", "2026-10-02"),
    R.F_QUALITY: ("Constructed: Brackenholt Spring Water, Borehole 2 raw water analyses", "2026-10-02"),
    R.F_RAIN: ("Constructed: Brackenholt site rain gauge, daily totals at 09:00", "2026-10-02"),
    D.F_LETTER: ("Constructed: the licensing authority's pre-application advice for licence MA/28/15/0042",
                 "2026-09-22"),
    D.F_LICENCE: ("Constructed: licence to abstract water MA/28/15/0042, as issued", "2015-03-26"),
    D.F_GEOLOGY: ("Constructed: geological records extract for the Brackenholt district with borehole logs",
                  "2026-09-30"),
    D.F_RETURNS: ("Constructed: Brackenholt Spring Water, annual returns of water abstracted, 2015-16 to 2025-26",
                  "2026-04-22"),
    D.F_BRIEF: ("Constructed: Brackenholt Spring Water, line 5 project brief", "2026-09-08"),
}


def _rows(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in csv.reader(fh)) - 1
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(ws.max_row for ws in wb.worksheets)
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        src, date = FILES[f]
        p = os.path.join(target, f)
        entry = dict(path=f, format=f.rsplit(".", 1)[-1], bytes=os.path.getsize(p), source=src, date=date,
                     license="CC0-1.0 (original work, constructed for this task)")
        r = _rows(p)
        if r is not None:
            entry["rows"] = r
        files.append(entry)
    largest = max((e for e in files if "rows" in e), key=lambda e: e["rows"])
    meta = dict(
        task="task154",
        title="How much water a spring water bottler can apply to take from its borehole at the licence renewal "
              "under the licensing authority's derogation test, with its returns and its bottling line's water use",
        domain="Physical & Environmental Sciences",
        client_domain="Physical & Environmental Sciences",
        subdomain="hydrology-flood-frequency (groundwater abstraction licensing)",
        objective="Forecasting & Predictive Modeling",
        prompt_shape="the largest daily quantity a licence variation can take and whether the quantity needed passes, "
                     "with each protected borehole's predicted drawdown, a chart, a monthly returns check and a "
                     "bottling line's monthly water use",
        as_of=K.EXPORT_DATE.isoformat(),
        deliverables=[DL.G_NOTE, DL.G_CSV],
        distractor_files=DISTRACTORS,
        stated_inputs=["7.53", "10.00", "9.90"],
        input_gates=dict(files=len(files), formats=sorted({e["format"] for e in files}),
                         largest_file=largest["path"], largest_file_rows=largest["rows"]),
        sources=[dict(files="all files under target/",
                      origin="constructed for this task by task154/generator/build.py (seeded, deterministic) around a "
                             "fictional English spring water bottler, its licensing authority, its neighbouring "
                             "licence holders and its bulk haulier, in the layouts of pumping test logger downloads, "
                             "monitoring and telemetry exports, a controller log, a haulier's statements, "
                             "manufacturing and quality exports, a licence, a pre-application letter, a geological "
                             "records extract, abstraction returns and a project brief; no real organisation's "
                             "records or person is depicted.",
                      date=K.EXPORT_DATE.isoformat(), license="CC0-1.0 (original work)")],
        created="2026-11-02",
        generator="task154/generator/build.py",
        files=files,
    )
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return meta
