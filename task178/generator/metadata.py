"""Write task178/metadata.json from the built pack: what every file is, where it comes from, the distractors and the
input gates."""
from __future__ import annotations

import json
import os

from openpyxl import load_workbook

import common as C

ORIGIN = "Constructed for this task (seeded, deterministic): "
SOURCES = {
    C.F_VER: ("City of Port Tessaly DPW (fictional), tide gauge PTG-01 verified 15-minute water level, in the layout "
              "of a municipal data system export", "2026-12-08"),
    C.F_TEL: ("City of Port Tessaly DPW, PTG-01 provisional 6-minute telemetry feed", "2026-12-08"),
    C.F_BOARD: ("City of Port Tessaly harbormaster's office, hourly float tide board log", "2026-12-08"),
    C.F_TABLES: ("City of Port Tessaly harbormaster's office, compiled annual tide tables 1995 to 2027 in three layouts. "
                 "Predictions are computed from fictional harmonic constants with the standard astronomical arguments "
                 "and nodal factors, so their timing follows the real Moon and Sun", "2026-10-01"),
    C.F_LOG: ("City of Port Tessaly DPW, PTG-01 station log", "2026-11-02"),
    C.F_DATUMS: ("City of Port Tessaly DPW, PTG-01 datum sheet revision 2026-06", "2026-06-15"),
    C.F_SLR: ("City of Port Tessaly DPW, Sea Level and Coastal Flooding Guidance 2026 update", "2026-09-03"),
    C.F_BASIS: ("City of Port Tessaly DPW, Granite Wharf trestle design basis revision B", "2026-11-20"),
    C.F_CLOSE: ("City of Port Tessaly DPW, street closure work orders from its two work-order systems", "2026-12-08"),
    C.F_WX: ("Port Tessaly municipal airport daily weather summary", "2026-12-08"),
    C.F_RIVER: ("Pennock River at Tessaly Falls (fictional river gauge), daily mean discharge", "2026-12-08"),
    C.F_DICT: ("City of Port Tessaly DPW, data dictionary for the exports", "2026-11-30"),
    C.F_MANIFEST: ("City of Port Tessaly DPW, export manifest", "2026-12-08"),
}
TITLE = ("The lowest deck elevation for a Maine city's April to May 2027 wharf-rebuild work trestle that high water is "
         "expected to reach on no more than one tide")


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
        dict(file=C.F_WX, wrong_basis=False,
             why_relevant="wind and pressure drive the storm surge on top of the tide",
             why_unused="the surge the forecast needs is measured at the gauge itself; no figure reads the airport record",
             ruled_out_by="the design basis sets every level at the gauge"),
        dict(file=C.F_RIVER, wrong_basis=False,
             why_relevant="the river's April snowmelt peak falls in the work window",
             why_unused="the gauge's readings already carry whatever the river adds at Cutler Wharf; no figure reads it",
             ruled_out_by="the design basis sets every level at the gauge"),
        dict(file=C.F_BOARD, wrong_basis=False,
             why_relevant="the harbormaster's own hourly readings of the water on the same pier",
             why_unused="the design basis and both asks take the gauge's readings; the board is hourly on its own zero",
             ruled_out_by="the design basis section 2 (the gauge's highest 15-minute reading)"),
    ]
    meta = dict(
        task="task178", title=TITLE,
        domain="Physical & Environmental Sciences", client_domain="Physical & Environmental Sciences",
        subdomain="climate and weather extremes (coastal extreme water levels: the expected number of high waters "
                  "reaching each candidate deck elevation over a known April to May 2027 window)",
        objective="Forecasting & Predictive Modeling",
        prompt_shape="one dial (the deck elevation on a nine-step pile schedule) with the expected tides at the chosen "
                     "elevation and the one below; five survival tides with dates and levels; six years of street "
                     "closures with those at the street's flooding level; a bar chart over the schedule",
        as_of="2026-12-08",
        deliverables=[C.G_BOOK, C.G_CHART],
        distractor_files=[d["file"] for d in distractors],
        distractors=distractors,
        stated_inputs=["1 April to 31 May 2027", "11.80 ft MLLW", "three hours", "2017 to 2022"] + ["%.2f" % x for x in C.DECK_SETTINGS],
        field_terms=["MLLW", "high water", "tide"],
        input_gates=dict(files=len(files), formats=sorted(set(x["format"] for x in files)), largest_file=big,
                         largest_file_rows=big_rows),
        sources=[dict(files="all files under target/",
                      origin="constructed for this task by task178/generator/build.py (seeded, deterministic) around a "
                             "fictional Maine coastal city (Port Tessaly), its tide gauge, harbormaster's office and "
                             "public works department. No real organisation's records or person is depicted. The tide "
                             "predictions follow the real astronomy; the storms on the record are placed on the dates of "
                             "real Gulf of Maine storms but their levels are constructed.",
                      date="2026-12-08", license="CC0-1.0 (original work)")],
        created="2026-10-21", generator="task178/generator/build.py", files=files)
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
