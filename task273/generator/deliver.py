"""task273 architecture 4: the golden deliverables. The review workbook and the paper to the Director of Public Health, with
its chart, all from the solved figures."""
from __future__ import annotations

import io
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm   # noqa: E402
import matplotlib.pyplot as plt       # noqa: E402

import params as P                    # noqa: E402

FONT_DIR = next((d for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"),
                              "/Library/Fonts/") if os.path.exists(d + "LiberationSans-Regular.ttf")),
                "/usr/share/fonts/truetype/liberation/")
for f in ("LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"):
    fm.fontManager.addfont(FONT_DIR + f)
plt.rcParams.update({"font.family": "Liberation Sans", "svg.hashsalt": "task273", "pdf.fonttype": 42})

NAVY, TEAL, GREY, AMBER = "#1f4e79", "#2a7f78", "#9aa5b1", "#c26b1a"
COND = {g: c for g, c, on, f, v in P.CONDITIONS}


def chart_png(S):
    order = sorted(S["freq"], key=lambda g: S["freq"][g])
    vals = [S["freq"][g] * 1000 for g in order]
    on = set(S["panel"])
    joining = set(S["joining"])
    colors = [AMBER if g in joining else (NAVY if g in on else GREY) for g in order]
    fig, ax = plt.subplots(figsize=(7.4, 7.6), dpi=160)
    ax.barh(range(len(order)), vals, color=colors, height=0.72)
    ax.axvline(1000 * P.PANEL_LINE, color="#7a1f1f", lw=1.2, ls="--")
    ax.text(1000 * P.PANEL_LINE + 0.4, len(order) - 0.6, "1 in 200 (5 per 1,000)", color="#7a1f1f", fontsize=8.5,
            va="top")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(["%s (%s)" % (COND[g] if len(COND[g]) <= 34 else COND[g][:32] + "...", g) for g in order],
                       fontsize=7.4)
    ax.set_xscale("log")
    ax.set_xlim(0.3, 60)
    ax.set_xticks([0.5, 1, 2, 5, 10, 20, 50])
    ax.set_xticklabels(["0.5", "1", "2", "5", "10", "20", "50"])
    ax.set_xlabel("Carriers per 1,000 members of the Ardvenny Genome Study (log scale)", fontsize=8.6)
    for i, (g, v) in enumerate(zip(order, vals)):
        if g in joining:
            ax.text(v * 1.06, i, "%d, joins" % round(v), va="center", fontsize=7.4, color=AMBER, fontweight="bold")
    ax.set_title("Three founder conditions reach the panel line once each phase's calls are scaled by its\n"
                 "chance of calling a carrier; no condition leaves", fontsize=9.6, loc="left", color="#1c2330")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=NAVY, label="On the 2026/27 panel and stays"),
                       Patch(color=AMBER, label="Joins for 2027/28"), Patch(color=GREY, label="Not on the panel")],
              loc="lower right", fontsize=7.6, frameon=False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_workbook(path, S, F):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Panel 2027-28"
    ws["A1"] = "Couples Carrier Screening Programme: panel review for 2027/28"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Carrier frequency in the reference cohort on the census date, 1 November 2026 (%s members of the %s "
                "with consent in force and a released genotype); panel line at least 1 in 200 (policy 2.1)." %
                (format(S["cohort"], ","), P.STUDY))
    ws["A2"].font = Font(italic=True, size=9)
    head = ["Condition", "Gene", "Carrier frequency (per 1,000 members)", "On the 2026/27 panel",
            "On the 2027/28 panel", "Change"]
    ws.append([])
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for g in sorted(S["freq"], key=lambda g: -S["freq"][g]):
        ws.append([COND[g], g, F["freq_per_1000"][g], "Yes" if g in S["panel_2026"] else "No",
                   "Yes" if g in S["panel"] else "No",
                   "Joins" if g in S["joining"] else ("Leaves" if g in S["leaving"] else None)])
        if g in S["joining"]:
            for c in ws[ws.max_row]:
                c.fill = PatternFill("solid", fgColor="FBE5D0")
    for col, wdt in zip("ABCDEF", (54, 10, 16, 13, 13, 9)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Programme 2025-26")
    ws2["A1"] = "Couples told that one or both partners carry each condition on the 2026/27 panel, 2025/26"
    ws2["A1"].font = Font(bold=True, size=12)
    ws2["A2"] = ("A couple counts in the half in which its report went (every result its screen needed authorised, "
                 "policy 4.2), for each condition a partner was reported to carry at the classification of the day "
                 "the result was authorised (policy 4.3).")
    ws2["A2"].font = Font(italic=True, size=9)
    ws2.append([])
    ws2.append(["Condition", "Gene", "April to September 2025", "October 2025 to March 2026", "Screening year"])
    for c in ws2[4]:
        c.font = Font(bold=True)
    for g in [g for g, *_ in P.CONDITIONS if g in S["panel_2026"]]:
        h1, h2 = F["ask_b"]["H1"][g], F["ask_b"]["H2"][g]
        ws2.append([COND[g], g, h1, h2, h1 + h2])
    for col, wdt in zip("ABCDE", (52, 10, 16, 18, 14)):
        ws2.column_dimensions[col].width = wdt
    ws2.freeze_panes = "A5"

    ws3 = wb.create_sheet("Notes")
    notes = [
        "How the carrier frequencies were estimated",
        "A member counts as a carrier of a condition when a disease-causing variant (pathogenic or likely pathogenic "
        "in the register on 1 November 2026) was called in its gene. A member with no call is not necessarily a "
        "non-carrier: a heterozygote is called only when enough of the reads at the variant carry the alternate "
        "allele to pass that phase's calling rule (phase 1: at least 5 reads and 25 per cent; phase 2: at least 3 "
        "reads and 20 per cent).",
        "For each register variant and phase, each member's chance of being called if a carrier was taken from their "
        "own read count at the variant (the binomial chance of enough alternate reads from a heterozygote), and the "
        "phase's carriers were estimated as its calls divided by the sum of those chances over its members, scaled "
        "to the phase's members. Phase 1 read the founder variants of ARSACS, Joubert syndrome type 2 and diastrophic "
        "dysplasia at 8 to 16 reads, most of them 8 to 11, where its calling rule catches about half of the heterozygotes, and phase 1's "
        "members are the Morvaig Isles and Glenhaskel, where those conditions are common.",
        "Counting calls alone, or counting them over members read at least 10 or 20 times, leaves the three founder "
        "conditions below the line.",
        "Phase 1 call positions are GRCh37 and its variant names the 2019 transcripts; both were matched to the "
        "register through its GRCh37 positions. Members who withdrew consent before 1 November 2026, and samples "
        "withheld after QC, are outside the cohort.",
    ]
    for k, line in enumerate(notes, start=1):
        ws3.cell(row=k * 2 - 1, column=1, value=line).alignment = Alignment(wrap_text=True, vertical="top")
        if k == 1:
            ws3.cell(row=1, column=1).font = Font(bold=True)
    ws3.column_dimensions["A"].width = 120
    wb.properties.creator = P.BOARD
    wb.properties.lastModifiedBy = P.BOARD
    wb.save(path)


def write_paper(path, S, F, png):
    from docx import Document
    from docx.shared import Cm, Pt, RGBColor
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(1.8)
    h = doc.add_paragraph()
    r = h.add_run("Director of Public Health, %s" % P.PAPER.strftime("%d %B %Y").lstrip("0"))
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x5a, 0x64, 0x70)
    t = doc.add_paragraph()
    r = t.add_run("Carrier screening panel for 2027/28: add ARSACS, Joubert syndrome type 2 and diastrophic "
                  "dysplasia; keep the other eleven")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0x1f, 0x4e, 0x79)
    meta = doc.add_paragraph()
    meta.add_run("From: %s, Panel Review Group. Paper DPH/26/41. Decision required." % P.PEOPLE["chair"]).font.size = Pt(9)
    doc.add_heading("Recommendation", level=2)
    names = {g: c for g, c, *_ in P.CONDITIONS}
    jn = ", ".join("%s (%s, %d per 1,000)" % (names[g], g, F["freq_per_1000"][g]) for g in S["joining"])
    doc.add_paragraph(
        "The 2027/28 panel should carry %d conditions from 1 April 2027: the eleven on the current panel, all of which "
        "stay above the policy's line of one carrier in 200, and three that join: %s. No condition leaves. Of the "
        "%d conditions reviewed, the other %d have carrier frequencies between %d and %d per 1,000." %
        (len(S["panel"]), jn, len(S["freq"]), len(S["freq"]) - len(S["panel"]),
         min(F["freq_per_1000"][g] for g in S["freq"] if g not in S["panel"]),
         max(F["freq_per_1000"][g] for g in S["freq"] if g not in S["panel"])))
    doc.add_heading("Why the three founder conditions join", level=2)
    doc.add_paragraph(
        "The reference cohort is %s members of the %s with consent in force and a released genotype on 1 November "
        "2026 (%s from phase 1 in the Morvaig Isles and Glenhaskel, %s from phase 2 on the mainland). The two phases "
        "were sequenced on different capture kits and called with different rules, and phase 1's kit read the founder "
        "variants of the three conditions at only 8 to 16 reads, most of them 8 to 11. At that depth the phase 1 calling rule (at least five "
        "reads carrying the variant, a quarter of the reads) catches about half of the people who carry it, so a member "
        "with no call there is often a carrier who was missed. We therefore estimated each condition's carriers phase by "
        "phase, dividing each phase's calls by the sum of its members' chances of being called given their read count "
        "at the variant. Counted as calls, the three conditions sit at %s per 1,000; corrected, at %s." %
        (format(S["cohort"], ","), P.STUDY, format(S["cohort_by_phase"][1], ","), format(S["cohort_by_phase"][2], ","),
         ", ".join("%.1f" % (S["rungs"]["naive"][g] * 1000) for g in S["joining"]),
         ", ".join("%d" % F["freq_per_1000"][g] for g in S["joining"])))
    doc.add_picture(io.BytesIO(png), width=Cm(15.5))
    cap = doc.add_paragraph("Figure 1. Carrier frequency per 1,000 Study members for the 30 conditions reviewed, "
                            "against the panel line.")
    cap.runs[0].font.size = Pt(8)
    doc.add_heading("The programme's experience in 2025/26", level=2)
    doc.add_paragraph("Couples told that one or both partners carry each condition on the current panel, by the half "
                      "of the screening year in which the couple's report went.")
    tab = doc.add_table(rows=1, cols=4)
    tab.style = "Light List Accent 1"
    for c, txt in zip(tab.rows[0].cells, ("Condition", "Apr to Sep 2025", "Oct 2025 to Mar 2026", "Year")):
        c.text = txt
    for g in [g for g, *_ in P.CONDITIONS if g in S["panel_2026"]]:
        row = tab.add_row().cells
        h1, h2 = F["ask_b"]["H1"][g], F["ask_b"]["H2"][g]
        for c, txt in zip(row, ("%s (%s)" % (names[g], g), str(h1), str(h2), str(h1 + h2))):
            c.text = txt
    doc.add_paragraph()
    n = doc.add_paragraph("Notes. Carrier frequencies use the register's classifications on the census date and count "
                          "a member once per condition (policy 2.3, 2.4). The programme's figures use the "
                          "classification each result was authorised with (policy 4.3).")
    n.runs[0].font.size = Pt(8)
    doc.core_properties.author = P.PEOPLE["chair"]
    doc.core_properties.title = "Carrier screening panel for 2027/28"
    doc.save(path)
