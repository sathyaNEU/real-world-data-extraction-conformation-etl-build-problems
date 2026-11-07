"""task156: the golden deliverables, figures.json and submission.md, every figure recomputed from the shipped pack."""
import datetime as dt
import json
import os
import sys

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A          # noqa: E402
import estim as E         # noqa: E402
import postprocess as PP  # noqa: E402

XLSX = "pab_2027_turnout_forecast.xlsx"
DOCX = "pab_2027_recommendation_bcom.docx"
DISPLAY_SHORT = {}


def pct(x):
    return "%.0f" % (100 * x)


def compute(target):
    K = E.load(target)
    gold = E.golden(target)
    hist = E.naive_history(target)
    f = E.fit(target, True)
    a = E.pab_level(target, True)
    # the lift in points at the candidates' own rolls: each member with and without an active delegate
    pts = []
    cov_now, cov_then, rolls = {}, {}, {}
    for c in K.candidates:
        roll = [m for m in K.members.values() if m["council"] == c and E.active(m, E.EXTRACT)]
        rolls[c] = len(roll)
        e0 = np.array([E.eta(K, f, m, E.BALLOT_CLOSE, 0.0) for m in roll]) + a
        pts.append(float((1 / (1 + np.exp(-(e0 + f["gamma"]))) - 1 / (1 + np.exp(-e0))).mean()))
        cov_now[c] = float(np.mean([E.D(K, m["site"], E.EXTRACT, 2026) for m in roll]))
        cov_then[c] = float(np.mean([E.D(K, m["site"], E.END24, 2024) for m in roll]))
    bt = E.backtest(target)
    mae = float(np.mean([abs(p - o) for p, o in bt.values()]))
    btd = E.backtest(target, True)
    mae_d = float(np.mean([abs(p - o) for p, o in btd.values()]))
    last = {}
    for r in sorted(K.pab, key=lambda r: r["close"]):
        last[r["council"]] = (r["returned"] / r["roll"], r["close"])
    return dict(K=K, gold=gold, hist=hist, gamma=f["gamma"], se=f["se_gamma"], pts=float(np.mean(pts)),
                cov_now=cov_now, cov_then=cov_then, rolls=rolls, mae=mae, mae_d=mae_d, last=last,
                dues=A.ask_a(target), hours=A.ask_b(target))


def _hdr(ws, row, cols, widths):
    thin = Side(style="thin", color="7F7F7F")
    for j, (c, w) in enumerate(zip(cols, widths), start=1):
        cell = ws.cell(row=row, column=j, value=c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F3864")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=thin)
        ws.column_dimensions[get_column_letter(j)].width = w


def workbook(R, path):
    K = R["K"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast"
    ws["A1"] = "Protected action ballots opening 1 March 2027: expected turnout by council"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Roll: members employed at each council on the 2 November 2026 register extract. Expected turnout: the "
                "share of the roll forecast to return a ballot, from each member's age, years of membership and "
                "employment, the council's level and whether an elected delegate is in post at the member's worksite, "
                "set on the agent's declared 2021 and 2023-24 turnouts.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 48
    cols = ["Council", "Members on the roll", "Expected turnout (%)", "Reaches half the roll", "Apply for an order",
            "Members at a worksite with a delegate in post (%)", "Same, 2024-26 delegates at 30 June 2026 (%)",
            "Last declared turnout (%)"]
    _hdr(ws, 4, cols, [32, 12, 12, 12, 11, 16, 16, 14])
    r = 5
    for c in sorted(K.candidates, key=lambda c: -R["gold"][c]):
        g = R["gold"][c]
        lt = R["last"].get(c)
        ws.append([c, R["rolls"][c], round(100 * g, 1), "Yes" if g >= 0.5 else "No", "Apply" if g >= 0.5 else "Do not apply",
                   round(100 * R["cov_now"][c], 0), round(100 * R["cov_then"][c], 0),
                   ("%.1f (%s)" % (100 * lt[0], lt[1].strftime("%b %Y"))) if lt else "No ballot"])
        if g >= 0.5:
            for j in range(1, 9):
                ws.cell(row=r, column=j).fill = PatternFill("solid", fgColor="E2EFDA")
        r += 1
    ws.cell(row=r + 1, column=1, value="Councils to apply at").font = Font(bold=True)
    ws.cell(row=r + 1, column=2, value=sum(1 for c in K.candidates if R["gold"][c] >= 0.5))
    ws.freeze_panes = "B5"

    ws2 = wb.create_sheet("Delegate effect")
    ws2["A1"] = "Online votes 2022 to 2025: turnout model"
    ws2["A1"].font = Font(bold=True, size=12)
    rows = [("Elected delegate in post at the member's worksite (log odds)", round(R["gamma"], 3)),
            ("Standard error", round(R["se"], 3)),
            ("Same, in points of turnout at the 2027 rolls (average)", round(100 * R["pts"], 1)),
            ("2023-24 ballots reproduced from the online votes, mean absolute error (points), model without the "
             "delegate term", round(100 * R["mae"], 1)),
            ("Same, model with the delegate term", round(100 * R["mae_d"], 1))]
    for i, (k, v) in enumerate(rows, start=3):
        ws2.cell(row=i, column=1, value=k)
        ws2.cell(row=i, column=2, value=v)
    ws2.column_dimensions["A"].width = 78
    ws2.column_dimensions["B"].width = 12
    ws2.cell(row=10, column=1, value=("The 2023-24 round is reproduced as closely with or without the delegate term, "
                                      "because the delegates elected in 2022 and 2024 sat at much the same worksites. "
                                      "The July 2026 elections did not: the forecast runs each member on the delegates "
                                      "of the 2026-28 term still in post on the extract.")).alignment = Alignment(wrap_text=True)
    ws2.row_dimensions[10].height = 46

    ws3 = wb.create_sheet("Dues 2025-26")
    ws3["A1"] = "Dues deducted by each council's payroll, pay periods ending 1 July 2025 to 30 June 2026"
    ws3["A1"].font = Font(bold=True, size=12)
    _hdr(ws3, 3, ["Council", "Dues deducted ($)"], [34, 18])
    for c in sorted(R["dues"]):
        ws3.append([c, A.rnd(R["dues"][c])])
        ws3.cell(row=ws3.max_row, column=2).number_format = "#,##0"
    ws3.append(["Total", sum(A.rnd(v) for v in R["dues"].values())])
    ws3.cell(row=ws3.max_row, column=1).font = Font(bold=True)
    ws3.cell(row=ws3.max_row, column=2).number_format = "#,##0"
    ws3.cell(row=ws3.max_row + 2, column=1, value=("Western Shires Payroll Services' payments split by its statements; "
                                                   "runs on the regional payroll platform from January 2026 placed by "
                                                   "their pay period end (the advice dates them by pay day); the "
                                                   "re-sent March 2026 Lindale advice counted once."))

    ws4 = wb.create_sheet("Organiser hours 2025-26")
    ws4["A1"] = "Organiser hours at each council, 1 July 2025 to 30 June 2026"
    ws4["A1"].font = Font(bold=True, size=12)
    _hdr(ws4, 3, ["Council", "Hours"], [34, 10])
    for c in sorted(R["hours"]):
        ws4.append([c, A.rnd(R["hours"][c])])
    ws4.cell(row=ws4.max_row + 2, column=1, value=("Travel and administration excluded; a rescheduled booking counted "
                                                   "once, at its last update; a visit two organisers made counted for "
                                                   "both; each regional forum's hours shared by the sign-ins from each "
                                                   "council."))
    wb.save(path)
    PP.normalize_ooxml(path, "Samantha Taylor", "Samantha Taylor", "2026-11-03T22:41:00Z", "2026-11-05T05:17:00Z",
                       excel=True, title="Protected action ballots 2027: turnout forecast")


def memo(R, path):
    K = R["K"]
    g = R["gold"]
    yes = sorted([c for c in K.candidates if g[c] >= 0.5])
    no = sorted([c for c in K.candidates if g[c] < 0.5])
    fell = sorted([c for c in K.candidates if g[c] < 0.5 <= R["hist"][c]])
    rose = sorted([c for c in K.candidates if R["hist"][c] < 0.5 <= g[c]])
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    p = doc.add_paragraph()
    r = p.add_run("MEMO")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    for k, v in (("To", "Branch Committee of Management"), ("From", "Samantha Taylor, Research and Bargaining Officer"),
                 ("Date", "5 November 2026"), ("Subject", "Protected action ballot applications for the 2027 round")):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(0)
        q.add_run("%s: " % k).bold = True
        q.add_run(v)
    doc.add_paragraph()
    doc.add_heading("Recommendation", level=2)
    doc.add_paragraph("That the Branch apply to the Fair Work Commission for protected action ballot orders at %d "
                      "councils, for ballots opening on 1 March 2027: %s." % (len(yes), "; ".join(yes)))
    doc.add_paragraph("That the Branch not apply at the other %d councils in the round in this window." % len(no))
    doc.add_heading("Why these councils", level=2)
    doc.add_paragraph(
        "A ballot authorises action only if at least half of the roll votes. I forecast each member's chance of "
        "voting from the Branch's four online votes since 2022, set on the ballot agent's declared turnouts in the "
        "2021 and 2023-24 rounds, and added it up over each council's roll on the 2 November 2026 register.")
    doc.add_paragraph(
        "Whether an elected delegate is in post at a member's worksite moves their vote more than anything else we "
        "hold on them: in our online votes members at such worksites voted at about %s points more than comparable "
        "members elsewhere, and the declared ballots line up with it. The delegates elected in July 2026 sit at "
        "different worksites from those elected in 2022 and 2024. At %s, many worksites that had a delegate in the "
        "last two terms now have none, and those councils, which cleared half in their "
        "last ballots, are now forecast below it. At %s new delegates came forward and the forecast now clears half."
        % (pct(R["pts"]), ", ".join(fell[:-1]) + " and " + fell[-1], " and ".join(rose)))
    doc.add_paragraph(
        "Carried on members' own voting records alone, the forecast reproduces the 2023-24 round within about %.0f "
        "point on average and would put %d councils above half; that record was gathered under the earlier "
        "delegates, so it overstates the councils that lost them and understates those that gained them."
        % (100 * R["mae"], sum(1 for c in K.candidates if R["hist"][c] >= 0.5)))
    doc.add_heading("Forecast by council", level=2)
    t = doc.add_table(rows=1, cols=3)
    t.style = "Light List Accent 1"
    for i, h in enumerate(("Council", "Expected turnout", "Apply")):
        t.rows[0].cells[i].text = h
    for c in sorted(K.candidates, key=lambda c: -g[c]):
        row = t.add_row().cells
        row[0].text = c
        row[1].text = "%s%%" % pct(g[c])
        row[2].text = "Yes" if g[c] >= 0.5 else "No"
        row[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    doc.add_paragraph()
    doc.add_heading("What this means for the six councils", level=2)
    doc.add_paragraph(
        "At the councils that lost delegates the problem is organisational, not support for the claim. I suggest the "
        "organisers prioritise filling the vacant worksites before the next window rather than run ballots now that "
        "the forecast says would fail. The workbook sets out each council's forecast, the dues each council's "
        "payroll deducted in 2025-26 and the organisers' hours at each council in the same year.")
    doc.add_paragraph("Samantha Taylor")
    doc.core_properties.author = "Samantha Taylor"
    doc.save(path)
    PP.normalize_docx(path, "Samantha Taylor", "Samantha Taylor", "2026-11-04T23:12:00Z", "2026-11-05T04:56:00Z", 4,
                      96, 156, title="Protected action ballot applications for the 2027 round")


def submission(R, path):
    K = R["K"]
    g = R["gold"]
    yes = sorted([c for c in K.candidates if g[c] >= 0.5])
    fell = sorted([c for c in K.candidates if g[c] < 0.5 <= R["hist"][c]])
    rose = sorted([c for c in K.candidates if R["hist"][c] < 0.5 <= g[c]])
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Political science and public policy (election and polling forecasting).")
    L.append("**Analytical objective:** Forecasting and predictive modelling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Apply for protected action ballot orders at %d councils: %s.**" % (len(yes), "; ".join(yes)))
    L.append("Not the %d councils members' own voting records put above half: %s fall below half once each member is "
             "read with the delegate in post at their worksite after the July 2026 delegate elections, and %s rise "
             "above it.\n" % (sum(1 for c in K.candidates if R["hist"][c] >= 0.5), ", ".join(fell), " and ".join(rose)))
    L.append("## 2. Critical Components\n")
    L.append("1. Members at a worksite with an elected delegate in post vote markedly more often: about **%s points** "
             "at the 2027 rolls (log odds %.2f)." % (pct(R["pts"]), R["gamma"]))
    L.append("2. Members' voting records alone reproduce the 2023-24 declared turnouts within about **1 point** on "
             "average, because the 2022 and 2024 delegates sat at much the same worksites.")
    L.append("3. Six councils that cleared half at their last ballot fall below it in 2027 (%s), and two that did not "
             "now clear it (%s)." % (", ".join(fell), " and ".join(rose)))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Placed every member of membership_register_extract_2026-11-02.csv at their worksite, moving the codes "
             "used before July 2024 to today's through worksites_2026-11.csv.")
    L.append("2. Marked each member, on each online vote's close and on the extract, as at a worksite with a delegate "
             "of the term in force (delegate_register_2018-2028.xlsx) who was still a member that day.")
    L.append("3. Fitted a logit of voting on online_vote_invitations_2022-2025.csv: vote and council effects, age band, "
             "log years of membership, employment and the delegate mark.")
    L.append("4. Set the ballots' level with one shift returning every ballot the two Tallyhouse declarations report, "
             "each roll the members employed on its roll date.")
    L.append("5. Ran each member of the 2 November 2026 roll at the councils in bargaining_round_2027.xlsx with the "
             "2026-28 delegates in post on the extract and averaged by council.")
    L.append("6. Applied the guide's rule: apply where expected turnout is at least 50 per cent.")
    L.append("7. Dues: one copy of each advice, the bureau's runs split by its statements, each run placed at the "
             "Sunday its pay period ends (FP-04), a Thursday-dated platform advice moved back four days.")
    L.append("8. Organiser hours: travel and administration out, one row per organiser, invitation and day at its last "
             "update (a moved booking keeps its earlier row), each forum's hours shared by all its sign-ins.")
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % XLSX)
    L.append("1. Whether each council's expected turnout reaches half the roll:")
    for c in sorted(K.candidates):
        L.append("   - %s: %s" % (c, "reaches half" if g[c] >= 0.5 else "below half"))
    L.append("2. Dues each council in the round's payroll deducted for the branch, pay periods ending in 2025-26, "
             "whole dollars:")
    for c in sorted(R["dues"]):
        L.append("   - %s: %s" % (c, "{:,}".format(A.rnd(R["dues"][c]))))
    L.append("3. Organiser hours at each council in the round in 2025-26, whole hours:")
    for c in sorted(R["hours"]):
        L.append("   - %s: %d" % (c, A.rnd(R["hours"][c])))
    L.append("")
    L.append("### %s\n" % DOCX)
    L.append("1. Recommendation: apply at %s; do not apply at the other %d councils in the round."
             % ("; ".join(yes), len(K.candidates) - len(yes)))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def figures(R, path):
    K = R["K"]
    out = {"call": sorted(c for c in K.candidates if R["gold"][c] >= 0.5),
           "history_set": sorted(c for c in K.candidates if R["hist"][c] >= 0.5),
           "turnout": {c: round(R["gold"][c], 4) for c in sorted(K.candidates)},
           "turnout_history": {c: round(R["hist"][c], 4) for c in sorted(K.candidates)},
           "turnout_pct": {c: round(100 * R["gold"][c], 2) for c in sorted(K.candidates)},
           "threshold_pct": 50, "points_pct": round(100 * R["pts"], 2),
           "gamma": round(R["gamma"], 4), "points": round(R["pts"], 4), "backtest_mae": round(R["mae"], 4),
           "dues": {c: A.rnd(v) for c, v in sorted(R["dues"].items())},
           "hours": {c: A.rnd(v) for c, v in sorted(R["hours"].items())}}
    json.dump(out, open(path, "w"), indent=1, sort_keys=True)
    open(path, "a").write("\n")


def main(target, golden_dir, fig_path, sub_path):
    os.makedirs(golden_dir, exist_ok=True)
    R = compute(target)
    workbook(R, os.path.join(golden_dir, XLSX))
    memo(R, os.path.join(golden_dir, DOCX))
    figures(R, fig_path)
    submission(R, sub_path)


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"), os.path.join(HERE, "figures.json"),
         os.path.join(T, "submission.md"))
