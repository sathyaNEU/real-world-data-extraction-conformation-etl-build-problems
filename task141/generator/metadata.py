"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import common as K  # noqa: E402

SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
APD = "Okelan County Adult Probation Department"
CLERK = "Clerk of the Okelan County Circuit Court"
SO = "Okelan County Sheriff's Office, Detention Center"
SOURCES = {
    K.CMS1: (APD + ", CMS 1 export of the supervision terms closed from 1 July 2016 to 11 June 2023", "2026-10-02"),
    K.CMS2: (APD + ", CMS 2 export of supervision terms to 30 September 2026", "2026-10-02"),
    K.ORDERS: (CLERK + ", case management system, orders from 1 July 2016 changing a probation term's scheduled "
                       "expiration", "2026-10-02"),
    K.PETITIONS: (CLERK + ", case management system, probation violation petitions filed from 1 July 2016 and their "
                          "dispositions", "2026-10-02"),
    K.BOOKINGS: (SO + ", jail management system export of probation bookings from 1 January 2019", "2026-10-02"),
    K.PERSONS: ("Okelan County Sheriff's Office and Adult Probation Department, person number crosswalk",
                "2026-10-02"),
    K.HEADCOUNT: (SO + ", daily 06:00 count by housing unit", "2026-10-01"),
    K.JAIL_CODES: (SO + ", jail management system code list", "2025-02-04"),
    K.COURT_CODES: (CLERK + ", code table", "2025-01-21"),
    K.OFFICE_CODES: (APD + ", office codes", "2025-06-02"),
    K.ROSTER: (APD + ", personnel system export of probation officer assignments in effect from 1 July 2016",
               "2026-10-02"),
    K.ACT_PDF: ("General Assembly, Senate Bill 26-118 (Felony Probation Term Act), enrolled", "2026-05-14"),
    K.PLAN_PDF: ("State Jail Standards Board, instructions for the 2027 Jail Operations Plans", "2026-07-08"),
    K.REPORT: (APD + ", annual report for fiscal year 2025", "2025-10-15"),
}
DISTRACTORS = ["target/" + K.REPORT, "target/" + K.HEADCOUNT]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task141", title="Okelan County's 2027 felony probation revocation admissions and violator pods "
                                      "under SB 26-118",
                setting="A fictional county in an unnamed state on Central time, whose Adult Probation Department "
                        "supervises felony and misdemeanor probationers and whose Detention Center houses felony "
                        "revocation commitments under the State's 2019 realignment; a statute caps felony supervision "
                        "at 24 months from 1 January 2027. The county, its bodies, its statute and its people are "
                        "fictional, and every record is synthetic.",
                as_of="2026-10-16", deliverables=[K.GOLD_BOOK, K.GOLD_MEMO, K.GOLD_CHART],
                distractor_files=DISTRACTORS,
                stated_inputs=["records to 30 September 2026", "calendar 2027", "whole days"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
