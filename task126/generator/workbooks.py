"""The three Excel workbooks: the Saravel acknowledgements, last year's production tables P1 and P2, and the
international pendency comparison (a distractor)."""
import datetime as dt
import math
import random

import params as P
import writers as WR
from analysis import quarter_label

DATE_FMT = "yyyy-mm-dd"


def _d(o):
    return dt.datetime.combine(dt.date.fromordinal(int(o)), dt.time())


def saravel(path, A, T, C, quarters, when):
    """C: analysis.corpus(A); quarters: {label: median days} on the acknowledged decisions."""
    wb = WR.xlsx_book(path, "Work-sharing acknowledgements", "Saravel IPO Work-Sharing Desk",
                      "Saravel Intellectual Property Office", when)
    b = wb.add_format({"bold": True})
    df = wb.add_format({"num_format": DATE_FMT})
    ws = wb.add_worksheet("Acknowledgements")
    ws.write(0, 0, "Saravel Intellectual Property Office | Work-Sharing Programme with the Morvane Patent Office", b)
    ws.write(1, 0, "Acknowledgements of MPO final decisions on programme applications filed 1 October 2018 to "
                   "30 September 2022. Position at 30 September 2026. Prepared 14 October 2026.")
    hdr = ["SIPO file ref", "MPO application no.", "MPO filing date", "Status", "Decision acknowledged",
           "MPO decision date", "Acknowledged on"]
    for j, h in enumerate(hdr):
        ws.write(3, j, h, b)
    R = random.Random(P.SEED + 41)
    label = {"A": "Allowance", "R": "Refusal", "B": "Abandonment"}
    order = sorted(range(len(C["cases"])), key=lambda k: (A.start[C["cases"][k]], T.no[C["cases"][k]]))
    r = 4
    serial = {}
    for k in order:
        i = int(C["cases"][k])
        fy = P.fy_of(A.start[i])
        serial[fy] = serial.get(fy, 0) + 1 + (1 if R.random() < 0.03 else 0)
        ws.write(r, 0, "WS/%02d/%05d" % (fy % 100, serial[fy]))
        ws.write(r, 1, T.no[i])
        ws.write_datetime(r, 2, _d(A.start[i]), df)
        e = int(C["e3"][k])
        lag = R.randint(3, 21)
        if e <= P.EXTRACT:
            ws.write(r, 3, "Decided")
            ws.write(r, 4, label[C["dtype"][k]])
            ws.write_datetime(r, 5, _d(e), df)
            ack = min(e + lag, dt.date(2026, 10, 9).toordinal())
            ws.write_datetime(r, 6, _d(ack), df)
        else:
            ws.write(r, 3, "Open")
        r += 1
    ws.set_column(0, 0, 14)
    ws.set_column(1, 1, 20)
    ws.set_column(2, 6, 18)
    ws.freeze_panes(4, 0)
    q = wb.add_worksheet("Quarterly medians")
    q.write(0, 0, "Median days from MPO filing to the acknowledged MPO decision, by calendar quarter of filing", b)
    q.write(1, 0, "Every programme application filed in the quarter counts; an application with no final decision "
                  "at 30 September 2026 is counted as still waiting.")
    for j, h in enumerate(["Filing quarter", "Applications", "Decided at 30 Sep 2026", "Median days"]):
        q.write(3, j, h, b)
    qlab = [quarter_label(A.start[int(i)]) for i in C["cases"]]
    r = 4
    for lab in sorted(quarters):
        ks = [k for k, x in enumerate(qlab) if x == lab]
        q.write(r, 0, lab)
        q.write_number(r, 1, len(ks))
        q.write_number(r, 2, sum(1 for k in ks if C["e3"][k] <= P.EXTRACT))
        q.write_number(r, 3, quarters[lab])
        r += 1
    q.set_column(0, 0, 16)
    q.set_column(1, 3, 22)
    WR.close_xlsx(wb, path, "Saravel IPO Work-Sharing Desk", when)
    return len(C["cases"])


def annual_tables(path, p1, p2, when):
    wb = WR.xlsx_book(path, "Annual Performance Report 2025: production tables", "Performance Statistics Unit",
                      "Morvane Patent Office", when)
    b = wb.add_format({"bold": True})
    one = wb.add_format({"num_format": "0.0"})
    pct = wb.add_format({"num_format": "0.0"})
    ws = wb.add_worksheet("P1")
    ws.write(0, 0, "Table P1. Examiner docket pendency by docketing year", b)
    ws.write(1, 0, "Months from docketing to docket close (for an allowed docket, the grant), dockets opened in the "
                   "fiscal year. A production measure: it describes dockets, not applications.")
    ws.write(2, 0, "Extract of 30 September 2025. A year is reported once 98 per cent of its dockets have closed.")
    for j, h in enumerate(["Fiscal year docketed", "Dockets opened", "Closed at extract (%)",
                           "Median examiner docket pendency (months)"]):
        ws.write(4, j, h, b)
    r = 5
    for fy in sorted(p1):
        row = p1[fy]
        ws.write(r, 0, "FY%d" % fy)
        ws.write_number(r, 1, row["n"])
        ws.write_number(r, 2, math.floor(row["closed_share"] * 1000 + 0.5) / 10, pct)
        if row["reported"]:
            ws.write_number(r, 3, row["published"], one)
        else:
            ws.write(r, 3, "not yet reported")
        r += 1
    ws.set_column(0, 0, 20)
    ws.set_column(1, 3, 24)
    w2 = wb.add_worksheet("P2")
    w2.write(0, 0, "Table P2. Dockets opened by technology group", b)
    w2.write(1, 0, "Counted by the group code recorded on the docket when it was opened. Not restated.")
    years = list(range(2021, 2026))
    w2.write(3, 0, "Technology group", b)
    for j, fy in enumerate(years):
        w2.write(3, j + 1, "FY%d" % fy, b)
    r = 4
    for g in P.GROUPS:
        w2.write(r, 0, "%s %s" % (g, P.GROUP_NAMES[g]))
        for j, fy in enumerate(years):
            w2.write_number(r, j + 1, p2[(g, fy)])
        r += 1
    w2.write(r, 0, "All groups", b)
    for j, fy in enumerate(years):
        w2.write_number(r, j + 1, sum(p2[(g, fy)] for g in P.GROUPS))
    w2.set_column(0, 0, 46)
    w2.set_column(1, 5, 12)
    WR.close_xlsx(wb, path, "Performance Statistics Unit", when)


INTERNATIONAL = [
    # office, report year, first action pendency (months), total pendency (months), basis note
    ("Saravel Intellectual Property Office", 2024, 13.6, 26.2, "Calendar year; total pendency to grant or final refusal"),
    ("Saravel Intellectual Property Office", 2025, 14.1, 25.7, "Calendar year; total pendency to grant or final refusal"),
    ("Velmora Patent Office", 2024, 17.8, 31.6, "Fiscal year April to March; average, not median"),
    ("Velmora Patent Office", 2025, 18.4, 32.3, "Fiscal year April to March; average, not median"),
    ("Kestria Intellectual Property Agency", 2024, 11.2, 22.4, "Calendar year; excludes divisional applications"),
    ("Kestria Intellectual Property Agency", 2025, 10.9, 21.8, "Calendar year; excludes divisional applications"),
    ("Isteva Patent Bureau", 2024, 20.5, 36.7, "Fiscal year July to June; requests for examination only"),
    ("Isteva Patent Bureau", 2025, 19.7, 35.1, "Fiscal year July to June; requests for examination only"),
]


def international(path, when):
    wb = WR.xlsx_book(path, "International pendency comparison 2025", "International Relations Unit",
                      "Morvane Patent Office", when)
    b = wb.add_format({"bold": True})
    one = wb.add_format({"num_format": "0.0"})
    ws = wb.add_worksheet("Published figures")
    ws.write(0, 0, "Patent pendency published by partner and comparator offices, 2024 and 2025 reports", b)
    ws.write(1, 0, "Each office's own published measure, as printed in its annual report. Definitions differ and the "
                   "figures are not adjusted to a common basis.")
    for j, h in enumerate(["Office", "Report year", "First action pendency (months)", "Total pendency (months)",
                           "Basis as published"]):
        ws.write(3, j, h, b)
    for r, row in enumerate(INTERNATIONAL, start=4):
        ws.write(r, 0, row[0])
        ws.write_number(r, 1, row[1])
        ws.write_number(r, 2, row[2], one)
        ws.write_number(r, 3, row[3], one)
        ws.write(r, 4, row[4])
    ws.set_column(0, 0, 38)
    ws.set_column(1, 3, 16)
    ws.set_column(4, 4, 52)
    WR.close_xlsx(wb, path, "International Relations Unit", when)
