"""The golden figures, computed from target/ alone, and the golden deliverables written from them."""
import datetime as dt
import json
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import analysis as A
import common as C
import world as W

QNAME = {1: "Q1 2026", 2: "Q2 2026", 3: "Q3 2026", 4: "Q4 2026"}


def r1000(x):
    return int(round(x / 1000.0)) * 1000


def r25000(x):
    return int(round(x / 25000.0)) * 25000


def rungs(df, cdd):
    out = {}
    exp0 = cdd.loc[df.index, "anticipated_monthly_cash_deposits_cad"].astype(float) * 12
    out["R0_declared"], _ = A.designate(df, exp0)
    band = cdd.loc[df.index, "anticipated_annual_turnover_band"]
    exp1 = df.cash.groupby([df.trade, band.values]).transform("mean")
    out["R1_peer_mean"], _ = A.designate(df, exp1)
    sh = df.cash / df.credits
    out["R2_turnover_share"], _ = A.designate(df, sh.groupby(df.trade).transform("median") * df.credits)
    out["R2b_noncash"], _ = A.designate(df, A.produced(df, df.noncash, "median"))
    out["R3_all_settlements"], _ = A.designate(df, A.produced(df, df.card + df.platform, "median"))
    return out


def compute(target):
    p, mem, acc = A.load(target)
    df = A.member_year(p, mem)
    cdd = A.read_cdd(target)
    g = A.golden_call(df)
    fam = {}
    for how in A.FAMILY:
        e = A.produced(df, df.card, how)
        s, x = A.designate(df, e)
        fam[how] = (s, x, e)
    rg = rungs(df, cdd)
    lreq, windows = A.lctr_required(p, mem)
    lfiled, llate = A.lctr_filed(target, mem, acc, p)
    bc = A.branch_cash(target, p)
    return {"p": p, "mem": mem, "acc": acc, "df": df, "cdd": cdd, "golden": g, "family": fam, "rungs": rg,
            "lctr": (lreq, lfiled, llate), "windows": windows, "branch": bc}


def figures_of(res):
    df, g = res["df"], res["golden"]
    ratio = (df.cash / df.card).groupby(df.trade).median()
    out = {"call": {"referred": [], "near_miss": {}}, "deliverables": [
        "fiu_referral_slate_2027q1.docx", "member_cash_review_2026.xlsx", "cash_review_2026.png"]}
    for i in g["referred"]:
        out["call"]["referred"].append({
            "member_number": int(i), "name": df.name[i], "business_type": W.TRADE[df.trade[i]][1],
            "cash_paid_in": r1000(df.cash[i]), "produced": r25000(g["expected"][i]),
            "excess": r25000(g["excess"][i]),
            "cash_paid_in_exact": round(float(df.cash[i]), 2),
            "card_settlements_2026": round(float(df.card[i]), 2),
            "card_settlements_2026_whole": int(round(float(df.card[i]))),
            "trade_cash_to_card": round(float(ratio[df.trade[i]]), 4),
            "times_produced": round(float(g["excess"][i] / g["expected"][i]), 2),
        })
    n = g["near"]
    out["call"]["near_miss"] = {"member_number": int(n), "name": df.name[n], "business_type": W.TRADE[df.trade[n]][1],
                                "cash_paid_in": r1000(df.cash[n]), "produced": r25000(g["expected"][n]),
                                "excess": r25000(g["excess"][n]),
                                "times_produced": round(float(g["excess"][n] / g["expected"][n]), 2)}
    lreq, lfiled, llate = res["lctr"]
    out["lctr"] = {QNAME[q]: {"required": int(lreq[q]), "filed": int(lfiled[q]), "late": int(llate[q])} for q in (1, 2, 3, 4)}
    names = {b[0]: b[1] for b in W.BRANCHES}
    out["branch_cash"] = {b: {"name": names[b], "atm": r1000(v["atm"]), "night": r1000(v["night"])}
                          for b, v in res["branch"].items()}
    out["segment"] = {"members_assessed": int(len(df)), "trade_cash_to_card": {k: round(float(v), 4) for k, v in ratio.items()}}
    # the workbook's graded cells are the ones every estimator of produced cash prints alike: every member's cash
    # paid in (a sum of shipped rows), the test column and the referred members' three figures; the other members'
    # produced cash and excess are the review's working, shown and not asked for
    out["workbook"] = {"sheet": "Members 2026", "members": int(len(df)),
                       "graded": ["cash paid in, every member", "meets the s.7.3 test, every member",
                                  "produced cash and excess, the members referred"],
                       "working": "produced cash and excess of the members not referred"}
    out["rungs"] = {k: [df.name[i] for i in v] for k, v in res["rungs"].items()}
    out["test"] = {"threshold_cad": A.THRESHOLD_CAD, "times_produced": A.TIMES_PRODUCED, "lctr_cash_cad": A.LCTR_CASH,
                   "report_due_days": 15, "window_hours": 24}
    out["transits"] = sorted(res["branch"]) + ["19004"]
    out["programme_sections"] = ["5", "6.2", "7.3"]
    return out


# --- deliverables -----------------------------------------------------------------------------------------

THIN = Side(style="thin", color="B7C0C9")
HDR_FILL = PatternFill("solid", fgColor="1F3B57")
HDR_FONT = Font(bold=True, color="FFFFFF")
REF_FILL = PatternFill("solid", fgColor="FCE4D6")


def _hdr(ws, row, values, widths=None):
    for j, v in enumerate(values, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = Border(bottom=THIN)
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w


def workbook(res, figs, path):
    df, g = res["df"], res["golden"]
    ratio = (df.cash / df.card).groupby(df.trade).median()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Members 2026"
    ws["A1"] = "Cash-intensive business segment, January review of calendar 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Programme v6.1 s.7.3. Cash paid in on the business date of each credit, nearest CAD 1,000. Produced "
                "cash: the member's 2026 card acquirer settlements times its business type's median ratio of cash paid "
                "in to card settlements across the segment; produced cash and excess to the nearest CAD 25,000, the "
                "ratio column from unrounded figures. Sorted by excess. Business Services, 15 January 2027.")
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:J2")
    ws.row_dimensions[2].height = 42
    _hdr(ws, 4, ["Member", "Operating name", "Business type", "Cash paid in 2026 (CAD)", "Card settlements 2026 (CAD)",
                 "Produced cash (CAD)", "Excess (CAD)", "Excess / produced", "Meets s.7.3 test", "Note"],
         [11, 34, 30, 16, 16, 15, 15, 11, 11, 30])
    order = g["excess"].sort_values(ascending=False).index
    row = 5
    for i in order:
        meets = i in g["referred"]
        note = "Refer, Q1 2027" if meets else ("Largest excess not meeting the test" if i == g["near"] else "")
        vals = [int(i), df.name[i], W.TRADE[df.trade[i]][1], r1000(df.cash[i]), int(round(float(df.card[i]))),
                r25000(g["expected"][i]), r25000(g["excess"][i]),
                round(float(g["excess"][i] / g["expected"][i]), 2), "Yes" if meets else "No", note]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=row, column=j, value=v)
            if j in (4, 5, 6, 7):
                c.number_format = "#,##0"
            if j == 8:
                c.number_format = "0.00"
            if meets:
                c.fill = REF_FILL
        row += 1
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:J%d" % (row - 1)
    # trade relation
    wt = wb.create_sheet("Business type ratios")
    _hdr(wt, 1, ["Business type", "Members", "Median cash paid in per dollar of card settlements"], [32, 10, 22])
    for k, (t, v) in enumerate(sorted(ratio.items()), 2):
        wt.cell(row=k, column=1, value=W.TRADE[t][1])
        wt.cell(row=k, column=2, value=int((df.trade == t).sum()))
        c = wt.cell(row=k, column=3, value=round(float(v), 4))
        c.number_format = "0.0000"
    # LCTR
    wl = wb.create_sheet("LCTR 2026")
    _hdr(wl, 1, ["Quarter", "Reports required (24-hour windows)", "Reports filed", "Filed late (over 15 days)"], [12, 22, 14, 18])
    for k, q in enumerate((1, 2, 3, 4), 2):
        d = figs["lctr"][QNAME[q]]
        for j, v in enumerate([QNAME[q], d["required"], d["filed"], d["late"]], 1):
            wl.cell(row=k, column=j, value=v)
    wl.cell(row=7, column=1, value="Segment accounts only. Required: the 24-hour windows of programme s.6.2. Filed: each report "
                                   "reference once, in the quarter of its transaction date. Late: submitted more than 15 days after "
                                   "the day the first cash it reports was received.")
    # branch cash
    wbx = wb.create_sheet("Branch cash 2026")
    _hdr(wbx, 1, ["Transit", "Branch name", "Deposit ATMs (CAD)", "Night depository (CAD)", "After hours (CAD)"], [9, 26, 17, 19, 16])
    for k, (b, v) in enumerate(figs["branch_cash"].items(), 2):
        tot = v["atm"] + v["night"]
        for j, x in enumerate([b, v["name"], v["atm"], v["night"], tot], 1):
            c = wbx.cell(row=k, column=j, value=x)
            if j >= 3:
                c.number_format = "#,##0"
    wbx.cell(row=len(figs["branch_cash"]) + 3, column=1,
             value="Segment cash, nearest thousand. Night deposits counted at Regional Cash Services are placed at the depository the bag was collected from.")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    C.freeze_zip(path, "Microsoft Excel", stamp_iso="2027-01-15T22:14:00Z", app_version="16.0300")


def chart(res, figs, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    df, g = res["df"], res["golden"]
    x = g["expected"] / 1000.0
    y = df.cash / 1000.0
    fig, ax = plt.subplots(figsize=(8.6, 6.0), dpi=110)
    others = [i for i in df.index if i not in g["referred"]]
    ax.scatter(x[others], y[others], s=11, color="#8C99A6", alpha=0.75, label="Other segment members", linewidths=0)
    ax.scatter(x[g["referred"]], y[g["referred"]], s=42, color="#C0392B", label="Meets the s.7.3 test", zorder=3)
    xs = np.geomspace(8.0, float(x.max()) * 1.15, 300)
    edge = np.maximum(xs + A.THRESHOLD_CAD / 1000.0, (1 + A.TIMES_PRODUCED) * xs)
    ax.plot(xs, edge, color="#1F3B57", lw=1.1, ls="--", label="Test line: excess of CAD 100k and twice produced")
    ax.plot(xs, xs, color="#B7C0C9", lw=0.9, label="Cash paid in equals produced cash")
    offsets = {0: (-12, 16), 1: (-12, -26)}
    for k, i in enumerate(g["referred"]):
        ax.annotate("%s\nCAD %s paid in, %s produced" % (df.name[i], "{:,}".format(r1000(df.cash[i])),
                                                         "{:,}".format(r25000(g["expected"][i]))),
                    (x[i], y[i]), xytext=offsets.get(k, (-12, 12)), textcoords="offset points", fontsize=7.6,
                    color="#7B241C", ha="right", arrowprops=dict(arrowstyle="-", color="#C0392B", lw=0.6))
    n = g["near"]
    ax.annotate(df.name[n], (x[n], y[n]), xytext=(-8, 8), textcoords="offset points", fontsize=7.2, color="#34495E",
                ha="right")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ticks = [10, 30, 100, 300, 1000, 3000]
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(["{:,}".format(t) for t in ticks])
    ax.set_yticklabels(["{:,}".format(t) for t in ticks])
    ax.minorticks_off()
    ax.set_xlim(8, float(x.max()) * 1.3)
    ax.set_ylim(8, float(max(y.max(), edge.max())) * 1.1)
    ax.set_xlabel("Cash its trade produced in 2026, CAD thousands (card settlements times the business type's ratio)")
    ax.set_ylabel("Cash paid in during 2026, CAD thousands")
    ax.set_title("Two members paid in about four times the cash their counter trade produced", fontsize=10.5)
    ax.grid(True, which="both", color="#E5E8EB", lw=0.5)
    ax.legend(fontsize=7.5, loc="upper left", frameon=False)
    fig.text(0.01, 0.01, "Harlow Reach Credit Union Business Services, January review of the cash-intensive business segment. Log scales.",
             fontsize=6.5, color="#5D6D7E")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def memo(res, figs, path):
    import docx
    from docx.shared import Pt
    df, g = res["df"], res["golden"]
    d = docx.Document()
    d.styles["Normal"].font.name = "Calibri"
    d.styles["Normal"].font.size = Pt(10)
    d.add_heading("Two cash-intensive members referred for enhanced investigation, Q1 2027", level=1)
    d.add_paragraph("To: AML Compliance Committee, meeting of 20 January 2027\nCc: FIU Lead\nFrom: Business "
                    "Services\nDate: 15 January 2027\nRef: BS/EDD/2027-01\nRe: January review of the cash-intensive "
                    "business segment, calendar 2026 (programme v6.1, s.7.2 and s.7.3)")
    ref = g["referred"]
    words = {1: "One member meets", 2: "Two members meet", 3: "Three members meet"}
    d.add_paragraph("%s the case acceptance test of s.7.3: cash paid in during 2026 that exceeds the cash the "
                    "member's trade produced by CAD 100,000 or more and by at least twice that cash. Business Services refers "
                    "%s to the Financial Intelligence Unit and asks the Committee to approve the investigations in the "
                    "order below, within the Unit's capacity of four new investigations a quarter." % (words.get(len(ref), "%d members meet" % len(ref)),
                                                                         "both" if len(ref) == 2 else "each"))
    t = d.add_table(rows=1, cols=6)
    t.style = "Light Grid Accent 1"
    for j, h in enumerate(["Member", "Operating name", "Business type", "Cash paid in 2026", "Cash its trade produced",
                           "Excess"]):
        t.rows[0].cells[j].text = h
    for i in ref:
        c = t.add_row().cells
        vals = [str(int(i)), df.name[i], W.TRADE[df.trade[i]][1], "CAD {:,}".format(r1000(df.cash[i])),
                "CAD {:,}".format(r25000(g["expected"][i])), "CAD {:,}".format(r25000(g["excess"][i]))]
        for j, v in enumerate(vals):
            c[j].text = v
    n = g["near"]
    d.add_paragraph("")
    d.add_paragraph("The largest excess among members that do not meet the test is %s (member %d, %s): CAD {:,} paid "
                    "in against about CAD {:,} produced, an excess of about CAD {:,}. It clears CAD 100,000 but is "
                    "less than twice its produced cash, so it is not referred.".format(
                        r1000(df.cash[n]), r25000(g["expected"][n]), r25000(g["excess"][n]))
                    % (df.name[n], int(n), W.TRADE[df.trade[n]][1].lower()))
    d.add_heading("How produced cash was measured", level=2)
    d.add_paragraph("A member's cash comes from its walk-in customers, and the same customers' card payments reach the "
                    "account as its card acquirer's daily settlements. Produced cash is the member's 2026 card "
                    "settlements times its business type's median ratio of cash paid in to card settlements across "
                    "the segment. The declared anticipated cash in the CDD profiles, the account's other credits and "
                    "delivery-platform payouts were not used: the profiles are the members' own statements, some "
                    "years old; business-to-business receipts and loans carry no cash; and platform orders are paid "
                    "online. Measured this way, %s paid in %.1f times and %s %.1f times the cash their counter trade "
                    "produced." % (df.name[ref[0]], float(df.cash[ref[0]] / g["expected"][ref[0]]),
                                   df.name[ref[1]], float(df.cash[ref[1]] / g["expected"][ref[1]])))
    d.add_heading("Large cash transaction reporting, 2026", level=2)
    t2 = d.add_table(rows=1, cols=4)
    t2.style = "Light Grid Accent 1"
    for j, h in enumerate(["Quarter", "Reports required", "Reports filed", "Filed late"]):
        t2.rows[0].cells[j].text = h
    for q in (1, 2, 3, 4):
        v = figs["lctr"][QNAME[q]]
        c = t2.add_row().cells
        for j, x in enumerate([QNAME[q], v["required"], v["filed"], v["late"]]):
            c[j].text = str(x)
    d.add_paragraph("Required reports are the 24-hour windows of s.6.2 across each member's accounts and channels; "
                    "the old reporting module filed per account and business date, so some windows went unreported "
                    "and some were reported twice.")
    d.add_heading("Segment cash after hours by branch, 2026", level=2)
    t3 = d.add_table(rows=1, cols=3)
    t3.style = "Light Grid Accent 1"
    for j, h in enumerate(["Branch (transit)", "Deposit ATMs", "Night depository"]):
        t3.rows[0].cells[j].text = h
    for b, v in figs["branch_cash"].items():
        c = t3.add_row().cells
        for j, x in enumerate(["%s (%s)" % (v["name"], b), "{:,}".format(v["atm"]), "{:,}".format(v["night"])]):
            c[j].text = x
    d.add_paragraph("CAD, nearest thousand. Langley City closed on 26 June 2026 and Willowbrook opened on 29 June 2026.")
    foot = d.sections[0].footer.paragraphs[0]
    foot.text = "Harlow Reach Credit Union, Business Services. Internal: AML Compliance Committee only."
    cp = d.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    cp.title = ""
    cp.created = dt.datetime(2027, 1, 15, 21, 40)
    cp.modified = dt.datetime(2027, 1, 15, 22, 6)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d.save(path)
    C.freeze_zip(path, "Microsoft Office Word", stamp_iso="2027-01-15T22:06:00Z", app_version="16.0000")


def run(target, task, members=None, by_role=None, verbose=True):
    res = compute(target)
    figs = figures_of(res)
    gold = os.path.join(task, "golden")
    workbook(res, figs, os.path.join(gold, "member_cash_review_2026.xlsx"))
    chart(res, figs, os.path.join(gold, "cash_review_2026.png"))
    memo(res, figs, os.path.join(gold, "fiu_referral_slate_2027q1.docx"))
    with open(os.path.join(task, "generator", "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    if verbose:
        for r in figs["call"]["referred"]:
            print("referred", r["name"], r["cash_paid_in"], r["produced"], r["excess"], r["times_produced"])
        print("near", figs["call"]["near_miss"])
        print("rungs", figs["rungs"])
        print("lctr", figs["lctr"])
    return res, figs
