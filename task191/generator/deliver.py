"""The goldens: the paper for the executive risk meeting (with its chart) and the alert figures workbook."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
from docx import Document         # noqa: E402
from docx.shared import Cm, Pt    # noqa: E402
import openpyxl                   # noqa: E402
from openpyxl.styles import Font  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402

DOCX = "tuning_scenarios_2027.docx"
XLSX = "tm_alert_figures_2026.xlsx"
QUARTERS = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
MONTHS = ["2026-%02d" % m for m in range(1, 11)]
MONTH_NAME = {"2026-%02d" % m: n for m, n in zip(range(1, 11), ["January", "February", "March", "April", "May", "June",
                                                                  "July", "August", "September", "October"])}


def label(code):
    return code + " / XB-HRJ2" if code in C.REPLACEMENT else code


def chart(fig, path):
    order = sorted(C.CODES, key=lambda c: fig["productivity"][c])
    f, ax = plt.subplots(figsize=(7.4, 3.9), dpi=150)
    cols = ["#b03a2e" if c in fig["call"]["tuning"] else "#5d6d7e" for c in order]
    ax.bar(range(len(order)), [fig["productivity"][c] for c in order], color=cols, width=0.62)
    ax.axhline(C.FLOOR, color="#1b2631", lw=1.1, ls="--")
    ax.text(len(order) - 0.4, C.FLOOR + 0.12, "Floor, 3 per cent", ha="right", fontsize=7.5, color="#1b2631")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([label(c) for c in order], rotation=55, ha="right", fontsize=7)
    ax.set_ylabel("Alerts ending in a SAR, per cent", fontsize=8)
    ax.set_title("Productivity, alerts raised 1 October 2025 to 30 September 2026 (red: into the 2027 tuning)",
                 fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=8)
    f.tight_layout()
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def paper(fig, path):
    import datetime as dt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
    tun, traps, c = fig["call"]["tuning"], fig["traps"], fig["counts"]
    p = doc.add_paragraph()
    r = p.add_run("Executive Risk Meeting, 18 November 2026. Paper ERM-26-41. For decision.")
    r.font.size = Pt(9)
    doc.add_heading("Transaction monitoring: the 2027 tuning set", level=1)
    doc.add_paragraph("From: Katherine Cobb, BSA/AML Officer. Prepared with Financial Crimes Analytics (Miguel Swanson) "
                      "on the monitoring tables and the case manager export of 2 November 2026.")
    doc.add_heading("1. Decision sought", level=2)
    doc.add_paragraph("The meeting is asked to approve %s as the scenarios going into the 2027 tuning, and no other "
                      "scenario, so the tuning plan can be in place before the independent AML review opens on "
                      "11 January." % _and(tun))
    doc.add_heading("2. The standard", level=2)
    doc.add_paragraph("As agreed in March, a scenario goes into the year's tuning when fewer than 3 per cent of the alerts "
                      "it raised in the twelve months to 30 September end in a SAR. Every alert raised in those months "
                      "counts, those still under investigation on 2 November by how they will end; the copies raised by "
                      "the 11 March re-run are not counted, and XB-HRJ is read with XB-HRJ2, which replaced it on "
                      "1 April.")
    doc.add_heading("3. Each scenario against the floor", level=2)
    tab = doc.add_table(rows=1, cols=6)
    tab.style = "Light Grid Accent 1"
    for k, h in enumerate(["Scenario", "Alerts raised", "Ended in a SAR so far", "Undecided on 2 November",
                           "Productivity, %", "2027 tuning"]):
        tab.rows[0].cells[k].text = h
    for code in sorted(C.CODES, key=lambda x: fig["productivity"][x]):
        row = tab.add_row().cells
        row[0].text = label(code)
        row[1].text = "{:,}".format(c[code]["alerts"])
        row[2].text = "{:,}".format(c[code]["sar_decided"])
        row[3].text = "{:,}".format(c[code]["undecided"])
        row[4].text = "%.1f" % fig["productivity"][code]
        row[5].text = "Yes" if code in tun else "No"
    png = os.path.join(C.GOLDEN, "_chart.png")
    chart(fig, png)
    doc.add_paragraph("")
    doc.add_picture(png, width=Cm(16.0))
    os.remove(png)
    doc.add_heading("4. The scenarios close to the floor on the decided alerts", level=2)
    doc.add_paragraph(
        "%s are not in the set, although the SARs they have produced so far are under 3 per cent of their decided "
        "alerts. Their investigations run the longest of any scenario: on 2 November %s of their alerts from the "
        "year were still under investigation, and of their alerts from before the year that were still undecided "
        "two months after the alert, most went on to a SAR. Read with the open alerts by how they will end, each "
        "is above the floor." % (_and(traps), _and("{:,}".format(c[t]["undecided_in_investigation"]) for t in traps)))
    doc.add_heading("5. How the figures were read", level=2)
    doc.add_paragraph("Each alert is dated by the business date of its run. An alert ends in a SAR when the "
                      "investigation it was escalated into, or added to, files one. An alert still undecided on "
                      "2 November is counted at the share of the scenario's alerts raised at least 330 days earlier, "
                      "undecided at the same age, that went on to end in a SAR.")
    doc.add_heading("6. Next steps", level=2)
    doc.add_paragraph("On approval, Financial Crimes Analytics will draw up the threshold work for each scenario in the "
                      "set with the scenario owners and bring the tuning plan to the Model governance forum in December.")
    cp = doc.core_properties
    cp.author = "Katherine Cobb"
    cp.title = "Transaction monitoring: the 2027 tuning set"
    cp.created = dt.datetime(2026, 11, 3, 14, 5)
    cp.modified = dt.datetime(2026, 11, 5, 18, 40)
    cp.last_modified_by = "Miguel Swanson"
    doc.save(path)
    C.normalise_zip(path, "2026-11-03T14:05:00Z", "2026-11-05T18:40:00Z", app="Microsoft Office Word",
                    author="Katherine Cobb", editor="Miguel Swanson")


def workbook(fig, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Investigations by quarter"
    ws.append(["Scenario"] + QUARTERS)
    for code in C.CODES:
        ws.append([label(code)] + [fig["ask_investigations"][code][q] for q in QUARTERS])
    ws2 = wb.create_sheet("SARs filed 2026")
    ws2.append(["Month", "Initial", "Continuing activity"])
    for m in MONTHS:
        ws2.append([MONTH_NAME[m] + " 2026", fig["ask_sars"][m]["initial"], fig["ask_sars"][m]["continuing"]])
    for w in (ws, ws2):
        for cell in w[1]:
            cell.font = Font(bold=True)
        w.column_dimensions["A"].width = 22
    wb.save(path)
    C.normalise_zip(path, "2026-11-03T13:30:00Z", "2026-11-05T17:55:00Z")


def make(fig=None):
    if fig is None:
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    os.makedirs(C.GOLDEN, exist_ok=True)
    for x in os.listdir(C.GOLDEN):
        os.remove(os.path.join(C.GOLDEN, x))
    paper(fig, os.path.join(C.GOLDEN, DOCX))
    workbook(fig, os.path.join(C.GOLDEN, XLSX))
    import writeup
    writeup.write(os.path.join(C.TASK, "submission.md"), fig)


if __name__ == "__main__":
    make()
