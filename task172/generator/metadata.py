"""Write task172/metadata.json from the built pack: what every file is and where it comes from, what is constructed,
the distractors, the input gates."""
from __future__ import annotations

import csv
import json
import os

from openpyxl import load_workbook

import common as C

ORIGIN = "Constructed for this task (seeded, deterministic): "
SOURCES = {
    C.F_NOTICES: ("Marrowby Teale LLP (fictional outside counsel), case-management export of the USCIS notices and "
                  "case-status events logged on Sallowmere Software's work-permit renewal matters, in the layout of a law "
                  "firm's export; not USCIS records", "2026-12-04"),
    C.F_REGISTER: ("Sallowmere Software Global Mobility (fictional), case register, two layouts across its April 2025 "
                   "system change", "2026-12-04"),
    C.F_ACTIONS: ("Sallowmere Software Global Mobility, case-action log", "2026-12-04"),
    C.F_PERMITS: ("Sallowmere Software HR Systems, work permit roster", "2026-12-04"),
    C.F_EMPLOYEES: ("Sallowmere Software HR Systems, Global Mobility program roster (no names)", "2026-12-04"),
    C.F_DEPENDANTS: ("Sallowmere Software Benefits, covered dependants (no names)", "2026-12-04"),
    C.F_TRACKER: ("Sallowmere Software Global Mobility, green-card tracker", "2026-12-03"),
    C.F_DISPATCH: ("Sallowmere Software mailroom, dispatch log from its two dispatch systems", "2026-12-04"),
    C.F_POLICY: ("Sallowmere Software Global Mobility, Work Permit Renewal Standard GM-07 revision 4. It cites two real "
                 "USCIS changes as the company states them: the end of automatic extension for renewals filed on or after "
                 "30 October 2025 (DHS interim final rule) and the 18-month validity of (c)(9) cards approved from "
                 "5 December 2025", "2025-11-12"),
    C.F_THREAD: ("Sallowmere Software Global Mobility mailbox, the December 2026 thread on the portal release", "2026-12-03"),
    C.F_DICT: ("Sallowmere Software Global Mobility, data dictionary and codes", "2026-12-04"),
    C.F_MANIFEST: ("Sallowmere Software Global Mobility, export manifest", "2026-12-04"),
    C.F_POSTED: ("Sallowmere Software Global Mobility, monthly capture of the processing time USCIS posts for Form I-765. "
                 "The figures are constructed and are not USCIS's published processing times", "2026-12-01"),
    C.F_H1B: ("Sallowmere Software immigration team, 2027 H-1B extension calendar", "2026-11-20"),
}
TITLE = ("The wait a software company's benefits portal should quote for the work-permit renewals its global mobility "
         "team files from January to March 2027")


def _rows(path):
    ext = path.rsplit(".", 1)[-1]
    if ext == "csv":
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in csv.reader(fh)) - 1
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
        dict(file=C.F_POSTED, wrong_basis=True,
             why_relevant="the team's record of the processing time USCIS posts for Form I-765, which people quote back",
             why_unused="USCIS's figure covers every filer nationally and the cases it completed in past months, not the "
                        "renewals Global Mobility files in the coming quarter (standard GM-07, 4.1); no figure reads it",
             ruled_out_by="the file's own form lines and offices, and standard GM-07 4.1 to 4.2"),
        dict(file=C.F_H1B, wrong_basis=False,
             why_relevant="H-4 spouses' work permits run to the H-4 end date the principal's H-1B sets",
             why_unused="it lists H-1B extensions to file in 2027, not work permits; no figure reads it",
             ruled_out_by="its own header"),
    ]
    meta = dict(
        task="task172", title=TITLE,
        domain="General Statistics & Data Science", client_domain="General Statistics & Data Science",
        subdomain="regression, classification and model diagnostics (employer immigration operations: a forward 80th "
                  "percentile of a censored wait under the stage model the record supports, each renewal cut at its own "
                  "card's expiry by the team's expedite request)",
        objective="Forecasting & Predictive Modeling",
        prompt_shape="one quoted wait to the nearest half month with its components; permits expiring in each of three "
                     "months by category; lockbox rejections and refilings within 30 days in each of four quarters; a "
                     "labelled bar chart of the permits expiring",
        as_of="2026-12-04",
        deliverables=["q1_2027_renewal_quote.xlsx", "q1_2027_expiring_permits.svg"],
        distractor_files=[d["file"] for d in distractors],
        distractors=distractors,
        stated_inputs=["180", "30.4", "30 October 2025", "5 December 2025", "18-month"],
        field_terms=[],
        input_gates=dict(files=len(files), formats=sorted(set(x["format"] for x in files)), largest_file=big,
                         largest_file_rows=big_rows),
        sources=[dict(files="all files under target/",
                      origin="constructed for this task by task172/generator/build.py (seeded, deterministic) around a "
                             "fictional software company in Bellevue, Washington (Sallowmere Software), its fictional "
                             "outside counsel (Marrowby Teale LLP) and its employees, identified by number only. No "
                             "real organisation's records or person is depicted. USCIS notices, receipt numbers, card "
                             "numbers and processing times are constructed in their real formats and are not USCIS data.",
                      date="2026-12-04", license="CC0-1.0 (original work)")],
        created="2026-10-18", generator="task172/generator/build.py", files=files)
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
