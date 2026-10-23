"""Write task178/metadata.json from the built pack: what every file is, where it comes from, the distractors and the
input gates."""
from __future__ import annotations

import json
import os

from openpyxl import load_workbook

import common as C

ORIGIN = "Constructed for this task (seeded, deterministic): "
SOURCES = {
    C.F_PEAKS: ("Callender Paper Company (fictional), Sauer mill, TUM-02 annual peak stage register, water years 1980 to 2015", "2016-03-02"),
    C.F_STAGE: ("Callender Paper Company, Sauer mill, TUM-02 15-minute stage, hydrologic database export, water years 2016 to 2025", "2026-01-20"),
    C.F_MEAS_OLD: ("Callender Paper Company, Sauer mill, TUM-02 discharge measurement notes transcribed from the field forms, 1980 to 2004", "2016-03-02"),
    C.F_MEAS_NEW: ("Callender Paper Company, Sauer mill, TUM-02 discharge measurements, measurement database export, water years 2005 to 2025", "2026-01-20"),
    C.F_STATION: ("Callender Paper Company, Sauer mill, TUM-02 station description, revised 2024-03-18", "2024-03-18"),
    C.F_LEVELS: ("Callender Paper Company, Sauer mill, TUM-02 levels log", "2025-08-27"),
    C.F_VISITS: ("Callender Paper Company, Sauer mill, TUM-02 site visit log, water years 2016 to 2025", "2026-01-20"),
    C.F_STANDARD: ("Callender Paper Company, Sauer mill, Engineering Standard section 4 (hydrology), issue 3", "2021-04-26"),
    C.F_STUDY: ("Crandell Hyde Engineering (fictional) for Callender, Sauer pipe bridge waterway alternatives study, draft", "2025-12-12"),
    C.F_SCADA: ("Callender Paper Company, Sauer mill, SCADA historian export, Sauer crossing tags", "2026-01-12"),
    C.F_WO: ("Callender Paper Company, Sauer mill, maintenance management system work orders, Sauer crossing assets", "2026-01-20"),
    C.F_RAIN: ("Callender Paper Company, Sauer mill, wastewater plant rain gage, daily totals", "2026-01-20"),
    C.F_KESSEL: ("Callender Paper Company, Sauer mill, MRT-01 Marten Creek annual peaks", "2026-01-20"),
    C.F_DICT: ("Callender Paper Company, Sauer mill, data dictionary for the TUM-02 exports", "2025-11-04"),
}
TITLE = ("The waterway alternative for a paper mill's replacement raw-water pipe bridge, the smallest that passes the river's "
         "1 per cent annual chance flood at the company's own stage gauge")


def _rows(path):
    ext = path.rsplit(".", 1)[-1]
    if ext == "csv":
        with open(path, encoding="utf-8") as fh:
            return sum(1 for line in fh if not line.startswith("#")) - 1
    if ext == "xlsx":
        wb = load_workbook(path, read_only=True)
        return sum(max(0, ws.max_row - 1) for ws in wb.worksheets)
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    files = []
    big, big_rows = None, 0
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        rows = _rows(p)
        if rows and rows > big_rows:
            big, big_rows = f, rows
        src, date = SOURCES[f]
        files.append(dict(path=f, format=f.rsplit(".", 1)[-1], bytes=os.path.getsize(p), rows=rows,
                          source=ORIGIN + src, date=date, license="CC0-1.0 (original work, constructed for this task)"))
    distractors = [
        dict(file=C.F_RAIN, wrong_basis=False,
             why_relevant="the rain at the mill in the same valley drives the floods the design flow is about",
             why_unused="the design flood comes from the gage's own annual peaks; no figure reads the rain record",
             ruled_out_by="the alternatives study section 3 and Engineering Standard 4.2.2 (the gage's annual peak series)"),
        dict(file=C.F_KESSEL, wrong_basis=False,
             why_relevant="the mill's other gage in the valley, with annual peak discharges from a stable rating",
             why_unused="the generalized skew is set by the standard and the design flood is at TUM-02; no figure reads it",
             ruled_out_by="Engineering Standard 4.2.2 and 4.2.4 (the structure's own gage, the filed generalized skew)"),
    ]
    meta = dict(
        task="task178", title=TITLE,
        domain="Physical & Environmental Sciences", client_domain="Physical & Environmental Sciences",
        subdomain="hydrology and flood frequency (the 1 per cent annual chance peak discharge at a stage-only gauge, "
                  "from its annual peak stages and its field discharge measurements)",
        objective="Forecasting & Predictive Modeling",
        prompt_shape="one dial (seven waterway alternatives by capacity) against the 1 per cent design discharge; ten "
                     "work windows' highest stages with dates; six water years' pipe-bridge levels and falls at the "
                     "gauge's crest; a frequency-curve chart",
        as_of="2026-01-20",
        deliverables=[C.G_BOOK, C.G_CHART],
        distractor_files=[d["file"] for d in distractors],
        distractors=distractors,
        stated_inputs=["{:,}".format(c) for _, c in C.ALTERNATIVES] + ["15 July to 15 September", "2016 to 2025", "2020 to 2025",
                                                                       "%.2f" % C.REG_SKEW, "%.3f" % C.REG_SKEW_MSE],
        field_terms=["stage", "gage height", "annual exceedance probability", "log-Pearson Type III", "water year"],
        input_gates=dict(files=len(files), formats=sorted(set(x["format"] for x in files)), largest_file=big,
                         largest_file_rows=big_rows),
        sources=[dict(files="all files under target/",
                      origin="constructed for this task by task178/generator/build.py (seeded, deterministic) around a "
                             "fictional western Washington pulp and paper mill (the Callender Paper Company Sauer mill), its river gage TUM-02 "
                             "on the fictional Tumwick River and its engineering consultant. No real organisation's "
                             "records or person is depicted.",
                      date="2026-01-20", license="CC0-1.0 (original work)")],
        created="2026-10-23", generator="task178/generator/build.py", files=files)
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
