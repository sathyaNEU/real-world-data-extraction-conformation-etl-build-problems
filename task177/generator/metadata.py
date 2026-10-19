"""Write task177/metadata.json from the built pack: what every file is and where it comes from, what is constructed,
the distractors, the input gates."""
from __future__ import annotations

import csv
import json
import os

from openpyxl import load_workbook

import common as C

ORIGIN = "Constructed for this task (seeded, deterministic): "
SOURCES = {
    C.F_LEGS: ("Prairie Works Manitoba (fictional), contact-centre platform interaction-leg export, both lines, in the "
               "layout of a cloud contact-centre platform's leg export with a legacy platform's history loaded at "
               "cutover", "2027-01-04"),
    C.F_CONV: ("Riverlot Dialogue Inc. (fictional assistant vendor), session export for the Prairie Works tenant",
               "2027-01-04"),
    C.F_CLAIMS: ("Prairie Works Manitoba case system, claims register", "2027-01-04"),
    C.F_XWALK: ("Prairie Works Manitoba case system, contact details with history", "2027-01-04"),
    C.F_CODES: ("Prairie Works Manitoba Contact Centre Systems, cutover code list", "2026-07-08"),
    C.F_OVERFLOW: ("Prairie Works Manitoba workforce team, overflow log", "2027-01-04"),
    C.F_PLAN: ("Prairie Works Manitoba Digital Channels, Ask Prairie Works 4.0 rollout plan version 1.4", "2026-12-16"),
    C.F_ACCEPT: ("Riverlot Dialogue Inc., acceptance test summary for release 4.0", "2026-12-01"),
    C.F_ORDER: ("Riverlot Dialogue Inc., usage tier order form for January to April 2027", "2026-12-14"),
    C.F_INVOICES: ("Prairie Works Manitoba accounts payable, the vendor's 2026 invoices", "2027-01-04"),
    C.F_DICT: ("Prairie Works Manitoba Digital Channels, field descriptions for the pull", "2027-01-04"),
    C.F_SURVEY: ("Prairie Works Manitoba survey platform, post-contact survey export", "2027-01-04"),
    C.F_MANIFEST: ("Prairie Works Manitoba Digital Channels, export manifest", "2027-01-04"),
}
TITLE = ("The share of their own contacts a provincial employment service's jobseekers will start in its digital "
         "assistant in March and April 2027, after eight weeks in which the upgraded assistant answers every call")


def _rows(path):
    ext = path.rsplit(".", 1)[-1]
    if ext == "csv":
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in csv.reader(fh)) - 1
    if ext == "jsonl":
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh)
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
        dict(file=C.F_OVERFLOW, wrong_basis=False,
             why_relevant="the workforce team's record of when the claimant queue was in overflow, the episodes the "
                          "transfers came from",
             why_unused="the legs export marks every transfer on the call itself and the voice session gives its "
                        "outcome; the log adds nothing a figure reads",
             ruled_out_by="the legs export's leg_result and transfer_to"),
        dict(file=C.F_SURVEY, wrong_basis=False,
             why_relevant="jobseekers' satisfaction with each channel, which looks like a driver of channel choice",
             why_unused="a 6 per cent sample with about three in ten answering; the choices and outcomes themselves are "
                        "in the exports; no figure reads it",
             ruled_out_by="its own coverage (a sample of contacts)"),
    ]
    meta = dict(
        task="task177", title=TITLE,
        domain="Psychology & Behavioral Science", client_domain="psychology-behavioral-science",
        subdomain="decision-making and computational behavioural modelling (a reinforcement-learning model of "
                  "jobseekers' contact-by-contact channel choices, with the learning from contacts they did not choose "
                  "estimated from overflow transfers and carried through eight weeks of such contacts)",
        objective="Forecasting & Predictive Modeling",
        prompt_shape="one forecast share to the whole per cent for an eight-week window; employers' conversations and "
                     "the service's own staff and test conversations in each month of 2026",
        as_of="2027-01-04",
        deliverables=["assistant_share_forecast_mar_apr_2027.xlsx", "assistant_first_aftermath_note.docx"],
        distractor_files=[d["file"] for d in distractors],
        distractors=distractors,
        stated_inputs=["2,041 of 2,400", "14 days", "3 January 2027", "4 January to 28 February 2027",
                       "1 March to 25 April 2027"],
        field_terms=[],
        input_gates=dict(files=len(files), formats=sorted(set(x["format"] for x in files)), largest_file=big,
                         largest_file_rows=big_rows),
        sources=[dict(files="all files under target/",
                      origin="constructed for this task by task177/generator/build.py (seeded, deterministic) around a "
                             "fictional provincial employment and income assistance service in Manitoba (Prairie Works "
                             "Manitoba), its fictional digital assistant (Ask Prairie Works) and assistant vendor "
                             "(Riverlot Dialogue Inc.). Jobseekers and employers are identified by number only. No real "
                             "organisation's records or person is depicted.",
                      date="2027-01-04", license="CC0-1.0 (original work)")],
        created="2026-10-19", generator="task177/generator/build.py", files=files)
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
