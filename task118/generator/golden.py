"""task118 goldens: the capacity note (docx, with its chart) and the 2026 programme audit ledger (csv), both written
from figures.json so every shared figure carries one rounding."""
import csv
import datetime as dt
import io
import os
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Inches, Pt, RGBColor  # noqa: E402

NOTE = "dr_capacity_note_2027.docx"
LEDGER = "dr_programme_audit_2026.csv"
ORDER = ("Home Battery Network", "Peak Time Rewards", "Cool Credit", "Business Demand Partners")
STAMP = dt.datetime(2026, 10, 23, 16, 10, 0)
MONTHS = {"2026-06": "June", "2026-07": "July", "2026-08": "August", "2026-09": "September"}


def chart(fig, path):
    avg = fig["ladder"]["R0 ex post, every event"]
    peak = fig["mw_exact"]
    labels = ["Home Battery\nNetwork", "Peak Time\nRewards", "Cool Credit", "Business Demand\nPartners"]
    x = range(len(ORDER))
    ink, muted = "#1F1F1E", "#5F5E5A"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task118"})
    f, ax = plt.subplots(figsize=(6.4, 3.4), dpi=150)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color="#E4E2DD", linewidth=0.8)
    ax.bar([i - 0.2 for i in x], [avg[p] for p in ORDER], width=0.38, color="#eb6834", edgecolor="white",
           linewidth=1.5, label="Average 2024 to 2026 event at 18:00")
    b = ax.bar([i + 0.2 for i in x], [peak[p] for p in ORDER], width=0.38, color="#2a78d6", edgecolor="white",
               linewidth=1.5, label="2027 system peak hour (fourth weekday called)")
    for rect, p in zip(b, ORDER):
        ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 0.15, "%d MW" % fig["mw"][p],
                ha="center", va="bottom", fontsize=8.5, color=ink, fontweight="bold")
    top = b[0]
    ax.text(top.get_x() + top.get_width() / 2, top.get_height() + 0.95, "Recommended", ha="center", va="bottom",
            fontsize=8, color=muted, style="italic")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, color=ink)
    ax.tick_params(axis="y", colors=muted)
    ax.set_ylabel("MW added by the USD 3.2M expansion", color=muted)
    ax.set_ylim(0, max(avg.values()) * 1.2)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#B8B6B0")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("In the hour the plan counts, the batteries add the most", fontsize=10, loc="left", color=ink)
    f.tight_layout()
    f.savefig(path, format="png", metadata={"Software": None})
    plt.close(f)


def note(fig, path, png):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    cp = d.core_properties
    cp.author = "Corey Cox"
    cp.last_modified_by = "Corey Cox"
    cp.title = "2027 demand response expansion"
    cp.created = STAMP
    cp.modified = STAMP
    cp.revision = 3
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.category = ""
    h = d.add_paragraph()
    r = h.add_run("The 2027 demand response expansion should go to the Home Battery Network")
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0x17, 0x3B, 0x57)
    d.add_paragraph("To: Budget and Rates, for the Council's 2027 budget packet. From: Corey Cox, Resource Planning. "
                    "23 October 2026.")
    p = d.add_paragraph()
    p.add_run("Recommendation: put the USD 3.2 million expansion line into the Home Battery Network. ").bold = True
    p.add_run("Its 2,133 added batteries count for %d MW in the 2027 resource adequacy plan, more than any other "
              "programme the line could buy; Peak Time Rewards is next at %d MW."
              % (fig["mw"]["Home Battery Network"], fig["mw"]["Peak Time Rewards"]))
    d.add_paragraph("Why the batteries, when the thermostats look biggest on an average day", style=None).runs[0].bold = True
    d.add_paragraph("Chapter 4 of the plan counts a programme in the design year's system peak hour, 18:00 on Friday "
                    "23 July 2027. OP-7 calls every programme on each weekday with a forecast high of 110F or more "
                    "(Independence Day and Labor Day excepted), "
                    "and the design week clears that from Tuesday 20 July, so the peak hour is the fourth event day "
                    "in a row. Our three summers of Ridgeway measurement show what that does: the thermostats, the "
                    "rebate customers and the commercial sites each give less on every consecutive event day, and "
                    "on the fourth day Cool Credit's reduction is about a fifth of a first day's. The batteries "
                    "recharge from rooftop solar between events and hold their 3.0 kW setting whatever the run.")
    t = d.add_table(rows=1, cols=3)
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Programme", "Units the USD 3.2M buys", "MW in the 2027 peak hour"
    for prog in ORDER:
        row = t.add_row().cells
        row[0].text = prog
        row[1].text = "{:,} {}".format(fig["units"][prog], {"Home Battery Network": "batteries",
                                                             "Peak Time Rewards": "customers",
                                                             "Cool Credit": "premises",
                                                             "Business Demand Partners": "sites"}[prog])
        row[2].text = "%d" % fig["mw"][prog]
    src = d.add_paragraph("Sources: Ridgeway Analytics measurement files, 2024 to 2026 seasons; Budget and Rates "
                          "cost sheet, 2 October 2026; Resource Adequacy Plan 2027, chapter 4 and Appendix B.")
    src.runs[0].font.size = Pt(8.5)
    d.add_picture(png, width=Inches(6.1))
    cap = d.add_paragraph("Each expansion's megawatts: grey on the record's average event, blue in the hour the plan "
                          "counts.")
    cap.runs[0].italic = True
    cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    d.add_paragraph("The 2026 audit figures the Council asked for (thermostats online on each event day, battery "
                    "incentives owed and Arroyo's nominations) are in dr_programme_audit_2026.csv.")
    fn = d.add_paragraph("Note: the batteries are read on their 2025 and 2026 events only, because Brightwell "
                         "dispatched at 2.0 kW in 2024 and at 3.0 kW from the 2025 season (schedule 2, Amendment 1). "
                         "Megawatts are rounded once, to the whole megawatt.")
    fn.runs[0].font.size = Pt(8.5)
    buf = io.BytesIO()
    d.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            zi = zipfile.ZipInfo(info.filename, date_time=STAMP.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, src.read(info.filename))


def ledger(fig, path):
    rows = [("section", "period", "figure", "unit")]
    for day, v in fig["ask_a"].items():
        rows.append(("Cool Credit enrolled premises with a thermostat online at 16:00", day, v, "premises"))
    for m, v in fig["ask_b_months"].items():
        rows.append(("Home Battery Network incentive owed", m, v, "USD"))
    rows.append(("Home Battery Network premises at the season cap", "2026", fig["ask_b_capped"], "premises"))
    for m, v in fig["ask_c_months_whole"].items():
        rows.append(("Business Demand Partners nominated capacity", m, v, "kW"))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)


def write(folder, fig):
    os.makedirs(folder, exist_ok=True)
    import tempfile
    png = os.path.join(tempfile.mkdtemp(), "chart.png")
    chart(fig, png)
    note(fig, os.path.join(folder, NOTE), png)
    ledger(fig, os.path.join(folder, LEDGER))
