"""task177 goldens: the forecast workbook, the note for the executive team, generator/figures.json and submission.md,
every figure computed once from the shipped files (calc.py) and carried."""
from __future__ import annotations

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K           # noqa: E402
import common as C         # noqa: E402
import postprocess as PP   # noqa: E402

F_BOOK = "retention_offer_forecast_2027.xlsx"
F_NOTE = "january_offer_note.docx"


def figures(target):
    P, c, a, b, ly, ty = K.figures(target)
    by_day = []
    for d in range(1, 29):
        g = ly[ly.d == d]
        by_day.append(dict(d=d, n=int(len(g)), offer=round(100 * g.Y[g["T"] == 1].mean(), 1),
                           hold=round(100 * g.Y[g["T"] == 0].mean(), 1), diff=round(K.diff(g), 1)))
    F = dict(
        call_share=C.pct5(c["share"] / 100),
        share_unrounded=round(c["share"], 2),
        n_ty=c["n_ty"],
        ty_next="1 February 2027",
        ty_days=int(c["ty_days"][0]) if len(c["ty_days"]) == 1 else None,
        fortnight_kept=C.pct5(c["fortnight"] / 100),
        later_kept=C.pct5(c["rest"] / 100),
        whole_list=C.pct5(c["pooled"] / 100),
        n_ly=c["n_ly"],
        n_fort=c["n_fort"],
        window_days=K.FORTNIGHT[1],
        lead_days=[int(ly.d.min()), int(ly.d.max())],
        by_day=by_day,
        disc={"%s %s" % (C.MONTH_NAME[m], pl): C.hundred(a[("disc", m, pl)]) for m in (2, 3) for pl in C.PLANS},
        takers={pl: a[("takers", pl)] for pl in C.PLANS},
        billed={"%s %d %s" % (C.MONTH_NAME[m], y, pl): C.hundred(b[("billed", y, m, pl)])
                for (y, m) in C.ASK_B_MONTHS for pl in C.PLANS},
        raw=dict(disc={"%s %s" % (C.MONTH_NAME[m], pl): a[("disc", m, pl)] for m in (2, 3) for pl in C.PLANS},
                 billed={"%s %d %s" % (C.MONTH_NAME[m], y, pl): b[("billed", y, m, pl)]
                         for (y, m) in C.ASK_B_MONTHS for pl in C.PLANS},
                 fortnight=round(c["fortnight"], 3), rest=round(c["rest"], 3), pooled=round(c["pooled"], 3)),
    )
    return F


def _money(v):
    return "GBP {:,}".format(int(v))


# --------------------------------------------------------------------------------------------------- the workbook
def write_workbook(path, F):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    head = PatternFill("solid", fgColor="E7E2DC")
    bold = Font(bold=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast"
    w = F["window_days"]
    rows = [
        ("The January offer should keep %d per cent of the list to 31 March 2027" % F["call_share"], None),
        ("Subscriber Retention, Audience Revenue. Prepared 25 January 2027, before the 26 January send.", None),
        (None, None),
        ("Share of the list kept to 31 March 2027 by the offer (per cent, nearest 5)", F["call_share"]),
        ("Subscriptions on the 26 January list", F["n_ty"]),
        ("Their next bill", "%s, %d days after the send" % (F["ty_next"], F["ty_days"])),
        (None, None),
        ("Last January's test: sent 31 January 2026 to a random half of the list", None),
        ("Kept to 31 March 2026 by the offer, next bill within %d days of the send (per cent, nearest 5)" % w,
         F["fortnight_kept"]),
        ("Kept to 31 March 2026 by the offer, next bill %d to %d days after the send (per cent, nearest 5)"
         % (w + 1, F["lead_days"][1]), F["later_kept"]),
        ("Kept to 31 March 2026 by the offer, whole list (per cent, nearest 5)", F["whole_list"]),
        ("Test subscriptions", F["n_ly"]),
        ("of which next bill within %d days of the send" % w, F["n_fort"]),
    ]
    for i, (a, b) in enumerate(rows, 1):
        if a is not None:
            ws.cell(row=i, column=1, value=a)
        if b is not None:
            c = ws.cell(row=i, column=2, value=b)
            c.alignment = Alignment(horizontal="right")
            if isinstance(b, int) and b > 1000:
                c.number_format = "#,##0"
    ws.cell(row=1, column=1).font = Font(bold=True, size=13)
    ws.cell(row=2, column=1).font = Font(italic=True, size=9, color="5F6670")
    ws.cell(row=4, column=1).font = bold
    ws.cell(row=4, column=2).font = Font(bold=True, size=13)
    ws.cell(row=8, column=1).font = bold
    ws.cell(row=13, column=1).alignment = Alignment(indent=2)
    ws.column_dimensions["A"].width = 84
    ws.column_dimensions["B"].width = 36
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    ws2 = wb.create_sheet("Test by days to bill")
    hdr = ("Days from the send to the next bill", "Subscriptions", "Offer: subscribed 31 March (per cent)",
           "Held back: subscribed 31 March (per cent)", "Kept by the offer (points)")
    for j, h in enumerate(hdr, 1):
        c = ws2.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(F["by_day"], 2):
        for j, k in enumerate(("d", "n", "offer", "hold", "diff"), 1):
            c = ws2.cell(row=i, column=j, value=r[k])
            if k == "n":
                c.number_format = "#,##0"
            elif k != "d":
                c.number_format = "0.0"
    ws2.cell(row=31, column=1, value="Bills on the 29th to 31st fell on 28 February 2026, 28 days after the send.")
    ws2.cell(row=32, column=1, value="Source: campaign tool list RET-2026-01 (arms); subscription events to 31 March "
                                     "2026; legacy billing, each subscription's January 2026 bill.")
    for r_ in (31, 32):
        ws2.cell(row=r_, column=1).font = Font(italic=True, size=9, color="5F6670")
    ws2.print_title_rows = "1:1"
    for col, w_ in zip("ABCDE", (22, 14, 20, 20, 16)):
        ws2.column_dimensions[col].width = w_
    ws2.freeze_panes = "A2"

    ws3 = wb.create_sheet("Offer discounts 2026")
    for j, h in enumerate(("Plan", "February 2026 bills (GBP)", "March 2026 bills (GBP)", "Subscriptions that took the offer"), 1):
        c = ws3.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, pl in enumerate(C.PLANS, 2):
        ws3.cell(row=i, column=1, value=pl)
        ws3.cell(row=i, column=2, value=F["disc"]["February %s" % pl]).number_format = "#,##0"
        ws3.cell(row=i, column=3, value=F["disc"]["March %s" % pl]).number_format = "#,##0"
        ws3.cell(row=i, column=4, value=F["takers"][pl]).number_format = "#,##0"
    ws3.cell(row=6, column=1, value="Half-price discounts on the bills of subscriptions that took last January's offer, "
                                    "in the email, on the web or in the app, by the month the bill was raised; pounds "
                                    "to the nearest hundred. Discount lines and the credits posted against an "
                                    "acceptance once a bill had been raised are both the offer; app acceptances the "
                                    "offers engine did not apply were billed at the app's half-price rate with no "
                                    "discount line, and are counted. The save desk's own half price is not the offer.")
    ws3.merge_cells("A6:D6")
    ws3.cell(row=6, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws3.cell(row=6, column=1).font = Font(italic=True, size=9, color="5F6670")
    ws3.row_dimensions[6].height = 48
    for col, w_ in zip("ABCD", (16, 22, 22, 22)):
        ws3.column_dimensions[col].width = w_

    ws4 = wb.create_sheet("List billing")
    months = [("October", 2026), ("November", 2026), ("December", 2026), ("January", 2027)]
    for j, h in enumerate(["Plan"] + ["%s %d (GBP)" % m for m in months], 1):
        c = ws4.cell(row=1, column=j, value=h)
        c.font = bold
        c.fill = head
    for i, pl in enumerate(C.PLANS, 2):
        ws4.cell(row=i, column=1, value=pl)
        for j, (mn, y) in enumerate(months, 2):
            ws4.cell(row=i, column=j, value=F["billed"]["%s %d %s" % (mn, y, pl)]).number_format = "#,##0"
    ws4.cell(row=6, column=1, value="What the subscriptions on this year's list were billed for their plans, net of "
                                    "credit notes and the goodwill credits on its invoices, by the UK date each bill "
                                    "was raised; pounds to the nearest hundred. Each subscription's own invoice lines, "
                                    "on whichever account's invoice they sit, one unit of each (a line of qty 2 also "
                                    "bills the household's other subscription); the Puzzles add-ons and other plans on "
                                    "the same invoices are not the list's plans.")
    ws4.merge_cells("A6:E6")
    ws4.cell(row=6, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.cell(row=6, column=1).font = Font(italic=True, size=9, color="5F6670")
    ws4.row_dimensions[6].height = 48
    for col, w_ in zip("ABCDE", (16, 20, 20, 20, 20)):
        ws4.column_dimensions[col].width = w_

    ws5 = wb.create_sheet("Notes")
    notes = [
        ("As of", "Extracts pulled 25 January 2027."),
        ("Subscribed", "A subscription is subscribed on a day if its paid period covers that day; it ends at "
                       "access_ended (data dictionary). A subscription that restarted before 31 March counts."),
        ("The test", "%s: offer against holdout, as randomised." % C.F_ASSIGN),
        ("Days to the bill", "Each test subscription's billing day from its January 2026 bill (%s); the next bill is "
                             "February's, days 29 to 31 on 28 February." % C.F_LBS),
        ("This year", "Every subscription on the list was last billed on 1 January 2027 for January; the next bill is "
                      "1 February 2027 (%s; %s 1.2)." % (C.F_SPINV, C.F_NOTE)),
        ("Rounding", "Shares to the nearest 5 per cent; pounds to the nearest hundred; counts whole."),
    ]
    for i, (a, b) in enumerate(notes, 1):
        ws5.cell(row=i, column=1, value=a).font = bold
        ws5.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    ws5.column_dimensions["A"].width = 18
    ws5.column_dimensions["B"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, "Natalie Taylor", "Natalie Taylor", "2027-01-25T19:02:00Z", "2027-01-25T22:31:00Z",
                       excel=True, company=C.ORG)


# ------------------------------------------------------------------------------------------------------- the note
def chart_png(F):
    """last January's points kept by the offer, by days from the send to the next bill: the days inside the window
    in the accent, the rest in the de-emphasis grey, this year's day marked"""
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task177"
    import matplotlib.pyplot as plt
    ACCENT, REST, INK, INK2, MUTED, GRID, AXIS = ("#2a78d6", "#898781", "#0b0b0b", "#52514e", "#898781", "#e1e0d9",
                                                  "#c3c2b7")
    w = F["window_days"]
    d = [r["d"] for r in F["by_day"]]
    v = [r["diff"] for r in F["by_day"]]
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    ax.bar(d, v, color=[ACCENT if x <= w else REST for x in d], width=0.78, zorder=2)
    top = max(v) + 6
    ax.set_ylim(min(min(v) - 1.5, -3), top)
    ax.axvline(F["ty_days"], color=INK, linewidth=1.1, linestyle=(0, (4, 3)), zorder=3)
    ax.text(F["ty_days"] + 0.35, top - 0.8, "This year every bill falls on 1 February,\n%d days after the send"
            % F["ty_days"], fontsize=7.8, color=INK, va="top")
    ax.text((w + 1 + F["lead_days"][1]) / 2, max(v[w:]) + 2.2, "Bill %d to %d days after the send"
            % (w + 1, F["lead_days"][1]), fontsize=7.8, color=INK2, ha="center")
    ax.axhline(0, color=AXIS, linewidth=0.8, zorder=1)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.set_xlabel("Days from the 31 January 2026 send to the subscription's next bill", fontsize=8.2, color=INK2)
    ax.set_ylabel("Kept to 31 March by the offer\n(points, offer minus held back)", fontsize=8.2, color=INK2)
    ax.set_title("Last January the offer kept subscribers only when it reached them in the fortnight before their bill",
                 fontsize=9.2, loc="left", color=INK)
    ax.set_xticks([1, 7, 14, 21, 28])
    ax.tick_params(labelsize=7.8, colors=MUTED, length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None}, facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()


def note_sections(F):
    w = F["window_days"]
    case = [
        "Of the %s subscriptions on the 26 January list, %d in 100 will still be subscribed on 31 March 2027 because "
        "they were sent the offer, subscriptions that would otherwise have gone. That is the rate last January's test "
        "measured on the subscribers whose next bill fell within %d days of the send, and every bill on this year's "
        "list falls on %s, %d days after it."
        % ("{:,}".format(F["n_ty"]), F["call_share"], w, F["ty_next"], F["ty_days"]),
        "Last January's headline figure is lower. Across the whole test list the offer kept about %d in 100, but that "
        "average mixes the subscribers whose bill came up within two weeks of the send, where it kept about %d in "
        "100, with those billed later in February, where it kept almost none: an offer that arrives weeks before the "
        "bill has been forgotten by the time the subscriber decides whether to pay it. Last year each subscription "
        "billed on its own day of the month; since November every monthly plan bills on the 1st, so this year the "
        "whole list hears from us in the week before its bill."
        % (F["whole_list"], F["fortnight_kept"]),
    ]
    disc = F["disc"]
    cost = ("On February 2026 bills last January's offer gave %s, %s and %s on the Digital, Digital Plus and Family "
            "plans, and on March bills %s, %s and %s; %s, %s and %s subscriptions took it."
            % (_money(disc["February Digital"]), _money(disc["February Digital Plus"]), _money(disc["February Family"]),
               _money(disc["March Digital"]), _money(disc["March Digital Plus"]), _money(disc["March Family"]),
               "{:,}".format(F["takers"]["Digital"]), "{:,}".format(F["takers"]["Digital Plus"]),
               "{:,}".format(F["takers"]["Family"])))
    brings = ("In January this list was billed %s for Digital, %s for Digital Plus and %s for Family, after credits; "
              "the workbook has October to January by plan."
              % (_money(F["billed"]["January 2027 Digital"]), _money(F["billed"]["January 2027 Digital Plus"]),
                 _money(F["billed"]["January 2027 Family"])))
    notes = ["Subscribed means the paid period covers 31 March: a subscription's access ends on its last paid day, and "
             "one that restarted by then counts.",
             "The save desk's own half price uses the same billing code as the offer and is not counted as the offer.",
             "App acceptances the offers engine did not apply were billed at the app's half-price rate, with no "
             "discount line; they are counted as takers and their discounts in the cost."]
    return case, cost, brings, notes


def write_note(path, F):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
    GREY = RGBColor(0x5F, 0x66, 0x70)
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    for label, value in (("To", "Executive team"), ("From", "Natalie Taylor, Subscriber Retention, Audience Revenue"),
                         ("Date", "25 January 2027"), ("Subject", "January retention offer: what it will keep")):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run("%s: " % label)
        r1.bold = True
        r1.font.size = Pt(9.5)
        r2 = p.add_run(value)
        r2.font.size = Pt(9.5)
    doc.add_paragraph()
    t = doc.add_paragraph()
    r = t.add_run("The January offer should keep %d per cent of the list to 31 March" % F["call_share"])
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0x7A, 0x2E, 0x1F)
    case, cost, brings, notes = note_sections(F)
    for para in case:
        doc.add_paragraph(para)
    doc.add_picture(io.BytesIO(chart_png(F)), width=Inches(6.3))
    cap = doc.add_paragraph("Source: retention test RET-2026-01 (%s subscriptions, a random half sent the offer); "
                            "subscription events to 31 March 2026; legacy billing, January 2026 bills."
                            % "{:,}".format(F["n_ly"]))
    cap.runs[0].font.size = Pt(8.5)
    cap.runs[0].font.color.rgb = GREY
    for head, body in (("What last January's offer cost", cost), ("What the list brings in", brings)):
        p = doc.add_paragraph()
        p.add_run(head).bold = True
        doc.add_paragraph(body)
    p = doc.add_paragraph()
    rr = p.add_run("Notes")
    rr.font.size = Pt(8.5)
    rr.bold = True
    for i, n_ in enumerate(notes, 1):
        q = doc.add_paragraph("%d. %s" % (i, n_))
        q.runs[0].font.size = Pt(8.5)
        q.runs[0].font.color.rgb = GREY
    foot = doc.sections[0].footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fr = foot.add_run("Daily Lantern Media. Subscriber Retention. Internal. Page ")
    fr.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    rn = OxmlElement("w:r")
    tx = OxmlElement("w:t")
    tx.text = "1"
    rn.append(tx)
    fld.append(rn)
    foot._p.append(fld)
    doc.save(path)
    PP.normalize_docx(path, "Natalie Taylor", "Natalie Taylor", "2027-01-25T17:40:00Z", "2027-01-25T22:48:00Z",
                      revision=9, total_time=126, seed="note2027", title="January retention offer: what it will keep",
                      company=C.ORG)


# ---------------------------------------------------------------------------------------------- figures and write-up
FIG_KEYS = (("call_share", "call_share"), ("call_share_unrounded", "share_unrounded"), ("call_n_ty", "n_ty"),
            ("call_ty_next", "ty_next"), ("call_ty_days", "ty_days"), ("call_fortnight_kept", "fortnight_kept"),
            ("call_later_kept", "later_kept"), ("call_whole_list", "whole_list"), ("call_n_ly", "n_ly"),
            ("call_n_fort", "n_fort"), ("call_window_days", "window_days"), ("call_lead_days", "lead_days"),
            ("ask_a_discount", "disc"), ("ask_a_takers", "takers"),
            ("ask_b_billed", "billed"))


def write_figures(path, F):
    """the call's figures under call_ keys, each ask's under its ask's key, as the write-up states them"""
    flat = {k: F[f] for k, f in FIG_KEYS}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(flat, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


def write_submission(path, F):
    disc, tk, bl = F["disc"], F["takers"], F["billed"]
    w, lo, hi = F["window_days"], F["lead_days"][0], F["lead_days"][1]
    L = []
    L += ["## Tags", "",
          "**Domain:** Product Analytics, churn propensity and uplift modelling.",
          "**Analytical objective:** Forecasting and predictive modelling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**%d per cent of the %s subscriptions on the 26 January 2027 list will still be subscribed on 31 March 2027 "
          "because they are sent the offer.**" % (F["call_share"], "{:,}".format(F["n_ty"])),
          "Last January the offer kept %d per cent of the test's subscriptions whose next bill fell within %d days of "
          "the send, and every bill on this year's list falls %d days after it. Not the test's whole-list %d per cent, "
          "which averages in subscriptions billed later in the month, where the offer kept almost none."
          % (F["fortnight_kept"], w, F["ty_days"], F["whole_list"]), ""]
    L += ["## 2. Critical Components", "",
          "1. Every subscription on this year's list bills next on **%s**, **%d days** after the 26 January send "
          "(**%s** of %s)." % (F["ty_next"], F["ty_days"], "{:,}".format(F["n_ty"]), "{:,}".format(F["n_ty"])),
          "2. Last January the offer kept **%d per cent** of the test's subscriptions whose next bill fell within %d "
          "days of the send, and almost none of those billed later." % (F["fortnight_kept"], w),
          ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Joined %s to %s: a test subscription is subscribed on 31 March 2026 unless its access ended before then "
          "and it did not restart by then (data dictionary, access_ended); offer against holdout as randomised."
          % (C.F_ASSIGN, C.F_EVENTS),
          "2. Took each test subscription's billing day from its January 2026 SUB line in %s and its next bill in "
          "February (on the month's last day where the billing day is past it): %d to %d days after the send."
          % (C.F_LBS, lo, hi),
          "3. Compared the arms by those days: within %d days of the send the offer kept %d per cent, later %d per "
          "cent, the whole list %d per cent (nearest 5)." % (w, F["fortnight_kept"], F["later_kept"], F["whole_list"]),
          "4. Took this year's next bill from the lines of %s: every list subscription's last bill covers January "
          "2027, so all %s bill next on %s, %d days after the send, as the 1st-of-month calendar in %s has it."
          % (C.F_SPINV, "{:,}".format(F["n_ty"]), F["ty_next"], F["ty_days"], C.F_NOTE),
          "5. Carried the rate within %d days of the bill to the whole list: %d per cent." % (w, F["call_share"]),
          "6. Took last January's offer discounts from %s: the DISC lines and the CRED lines (credits posted once the "
          "bill had been raised) whose applied_ref is an acceptance in %s, the save desk's STAY50 cases not being the "
          "offer, and the February and March bills of the app acceptances the engine never applied, which charge the "
          "plan at the app's half-price rate (%s), each such discount the subscription's January charge less the "
          "rate; by the month the bill was raised and the plan in %s, the subscriptions with any of them took it."
          % (C.F_LBS, C.F_OFFERS, ", ".join(C.RATE_CODE[p] for p in C.PLANS), C.F_PROFILE),
          "7. Took each list subscription's own lines from the lines column of %s by their subscription_id, one unit "
          "of each (an account's invoice also carries its add-ons and any other plan it pays for, some list "
          "subscriptions are billed on another account's invoice, and a line of qty 2 bills the list subscription "
          "and the household's other subscription on that plan), by the UK date each bill was raised (times are "
          "UTC), goodwill credit lines netted, added its legacy 1 October bill through %s and took off each bill a "
          "credit note covers at that bill's own amount, as %s has it." % (C.F_SPINV, C.F_XWALK, C.F_NOTE),
          "8. Recommendation: %d per cent of the list kept to 31 March 2027 by the offer." % F["call_share"], ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % F_BOOK, "",
          "1. Share of the 26 January 2027 list still subscribed on 31 March 2027 because of the offer: %d per cent."
          % F["call_share"],
          "2. Discount last January's offer gave, pounds to the nearest hundred:"]
    for m in ("February", "March"):
        for pl in C.PLANS:
            L.append("   - %s 2026 bills, %s: %s" % (m, pl, _money(disc["%s %s" % (m, pl)])))
    L.append("3. Subscriptions that took last January's offer:")
    for pl in C.PLANS:
        L.append("   - %s: %s" % (pl, "{:,}".format(tk[pl])))
    L.append("4. Billed to this year's list for its plans after credits, pounds to the nearest hundred:")
    for (y, m) in C.ASK_B_MONTHS:
        for pl in C.PLANS:
            L.append("   - %s %d, %s: %s" % (C.MONTH_NAME[m], y, pl, _money(bl["%s %d %s" % (C.MONTH_NAME[m], y, pl)])))
    L += ["", "### %s" % F_NOTE, "",
          "1. The case: %d per cent of the list kept to 31 March 2027, from last January's rate within %d days of the "
          "bill, with every bill this year %d days after the send." % (F["call_share"], w, F["ty_days"]),
          "2. Bar chart of the share last January's offer kept by days from the send to the next bill, the days "
          "within %d of the bill highlighted and this year's %d marked." % (w, F["ty_days"]), ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(target, golden, figures_path, submission):
    os.makedirs(golden, exist_ok=True)
    F = figures(target)
    write_workbook(os.path.join(golden, F_BOOK), F)
    write_note(os.path.join(golden, F_NOTE), F)
    write_figures(figures_path, F)
    write_submission(submission, F)
    return F
