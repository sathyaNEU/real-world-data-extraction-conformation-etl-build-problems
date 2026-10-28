"""task464 architecture 8: the rest of the pack.

Two distractors (relevant enough to weigh, unused by the solution, named in metadata.json and never in a file
name), the budget workbook the call feeds, the data dictionary, and the attendance return the asks use.
"""
import csv, os
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import world as W

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")


def _csv(name, rows, fields):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields})
    return name, len(rows)


def write_all():
    rng = np.random.default_rng(W.SEED + 71)
    out = []

    # Distractor one: satisfaction. Relevant to retention, carries no reason composition, unused.
    wb = Workbook()
    ws = wb.active
    ws.title = "By centre"
    ws.append(["Centre", "Responses", "Would recommend (%)", "Teaching (1 to 5)", "Facilities (1 to 5)"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for s in W.SITES:
        ws.append([s["name"], int(rng.integers(380, 1400)), round(float(rng.uniform(74, 93)), 1),
                   round(float(rng.uniform(3.6, 4.6)), 2), round(float(rng.uniform(3.1, 4.4)), 2)])
    ws2 = wb.create_sheet("By curriculum area")
    ws2.append(["Curriculum area", "Responses", "Would recommend (%)", "Teaching (1 to 5)"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for a in W.CURRICULUM:
        ws2.append([a, int(rng.integers(300, 1600)), round(float(rng.uniform(72, 94)), 1),
                    round(float(rng.uniform(3.5, 4.7)), 2)])
    for w in (ws, ws2):
        w.column_dimensions["A"].width = 26
        for col in "BCDE":
            w.column_dimensions[col].width = 20
    wb.properties.creator = "Quality Team"
    wb.properties.lastModifiedBy = "Quality Team"
    wb.save(os.path.join(OUT, "learner_satisfaction_2025_26.xlsx"))
    out.append(("learner_satisfaction_2025_26.xlsx", len(W.SITES) + len(W.CURRICULUM)))

    # Distractor two: attendance. Relevant to withdrawal, not a reason, unused by the solution.
    rows = []
    for a in W.CURRICULUM:
        for t in W.TERMS:
            rows.append({"curriculum_area": a, "term_code": t["code"],
                         "sessions_scheduled": int(rng.integers(220, 980)),
                         "attendance_rate_pct": round(float(rng.uniform(71.5, 92.4)), 1)})
    out.append(_csv("attendance_rates_2025_26.csv", rows,
                    ["curriculum_area", "term_code", "sessions_scheduled", "attendance_rate_pct"]))

    # The budget workbook the call feeds. One line, and its value in GBP thousands.
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 lines"
    ws.append(["Line", "Description", "Value (GBP thousands)", "Status"])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.append(["RET-01", "Retention work against one withdrawal reason", 486, "awaiting the review"])
    ws.append(["RET-02", "Learner support fund (continuing)", 1240, "committed"])
    ws.append(["RET-03", "Outreach and enrolment (continuing)", 702, "committed"])
    ws["C1"].alignment = Alignment(wrap_text=True)
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 48
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 22
    wb.properties.creator = "Finance"
    wb.properties.lastModifiedBy = "Finance"
    wb.save(os.path.join(OUT, "retention_budget_2027_lines.xlsx"))
    out.append(("retention_budget_2027_lines.xlsx", 3))

    return out


if __name__ == "__main__":
    for n, c in write_all():
        print("  %-44s %7d" % (n, c))
