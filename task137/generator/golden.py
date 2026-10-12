"""The golden deliverables: td_booking_q1_2027.xlsx (the booking by maturity month with its basis, what each closed
campaign kept on term deposit 30 days after maturity, and the quarter's maturing book against the list) and
td_booking_note_q1_2027.docx (the one-page note for the head of deposits, opening with the booking and charting it by
maturity month), plus generator/figures.json and metadata.json. Every figure is computed from the shipped pack
(calc.py for the call, asks.py for the asks)."""
from __future__ import annotations

import io
import json
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import asks as AK
import calc as C
import postprocess as PP
import world as W

BOOK = "td_booking_q1_2027.xlsx"
NOTE = "td_booking_note_q1_2027.docx"
MONTHS = {1: "January", 2: "February", 3: "March"}
CAMPAIGN_LABEL = {q: W.q_label(q) for q in W.PAST}


# ---------------------------------------------------------------------------------------------------------------
def h250(x):
    return int(np.floor(x / 250.0 + 0.5) * 250)


def k1000(x):
    return int(np.floor(x / 1000.0 + 0.5) * 1000)


def n500(x):
    return int(np.floor(x / 500.0 + 0.5) * 500)


def n100(x):
    return int(np.floor(x / 100.0 + 0.5) * 100)


def c(x):
    return "{:,}".format(int(x))


def compute(target):
    L = C.load(target)
    G = C.golden(L)
    Rg = C.rungs(L, G)
    F, cases = G["F"], G["cases"]
    has = (F["cfg"] != "").values
    R = G["R"]
    per_month = {}
    for k in (1, 2, 3):
        sel = (F["month"] == k).values
        per_month[k] = dict(
            deposits=int(sel.sum()), callable=int((sel & has).sum()),
            nr=float((R * G["U"] * has * sel).sum()), conv=float((R * G["C"] * has * sel).sum()),
            ret=float((R * G["C"] * G["p"] * has * sel).sum()), hours=G["months"][k])
    cv = cases[cases["conv"]]
    hi = cv[cv["drop"] >= 2.5]
    lo = cv[cv["drop"] < 0]
    special = (F["term"] == 4) & (F["rate"] == 5.65)
    A = AK.load(target)
    ask_a = AK.ask_a(A, "golden")
    ask_b = AK.ask_b(A, "golden")
    listed = A["lists"].groupby("campaign").size().to_dict()
    return dict(L=L, G=G, Rg=Rg, F=F, cases=cases, per_month=per_month, pooled=float(cv["ret"].mean()),
                n_conv_past=len(cv), share_hi=float(hi["ret"].mean()), n_hi=len(hi), share_neg=float(lo["ret"].mean()),
                special=int(special.sum()), card4=L["cards"][W.FWD][4], no_callable=int((~has).sum()),
                ask_a=ask_a, ask_b=ask_b, listed=listed, A=A)


def figures(c_):
    G, pm, Rg = c_["G"], c_["per_month"], c_["Rg"]
    share = G["ret"] / G["conv"]
    out = {
        "call": {"booking_hours": c(h250(G["total"])),
                 "hours_by_month": {MONTHS[k]: c(h250(pm[k]["hours"])) for k in (1, 2, 3)}},
        "components": {
            "no_callable_number": c(c_["no_callable"]),
            "deposits_at_5_65_four_year": c(c_["special"]),
            "locked_rate_pct": "5.65", "card_four_year_pct": "%.2f" % c_["card4"],
            "drop_points": "%.2f" % (5.65 - c_["card4"]),
            "past_share_at_2_5_or_more_pct": "%d" % int(np.floor(100 * c_["share_hi"] + 0.5)),
            "expected_conversations": c(n500(G["conv"])),
            "retention_share_pct": "%d" % int(np.floor(100 * share + 0.5)),
            "past_pooled_share_pct": "%d" % int(np.floor(100 * c_["pooled"] + 0.5)),
        },
        "steps": {
            "listed_deposits": c(len(c_["F"])),
            "deposits_by_month": {MONTHS[k]: c(pm[k]["deposits"]) for k in (1, 2, 3)},
            "release_share_pct": "%.1f" % (100 * G["R"]),
            "non_reaching_dials": c(n100(G["nr"])),
            "past_conversations": c(c_["n_conv_past"]),
            "past_conversations_at_2_5_or_more": c(c_["n_hi"]),
            "past_share_negative_drop_pct": "%.1f" % (100 * c_["share_neg"]),
            "hours_unrounded": "{:,.1f}".format(G["total"]),
            "hours_by_month_unrounded": {MONTHS[k]: "{:,.1f}".format(pm[k]["hours"]) for k in (1, 2, 3)},
            "band_points": "0.25",
            "drop_threshold_points": "2.5",
        },
        "rules": {"minutes_not_reached": "1.5", "minutes_conversation": "8", "minutes_retention": "22",
                  "release_days_before_maturity": "21", "days_after_maturity": "30", "listing_threshold_nzd": "25,000"},
        "default_path": {
            "pooled_share_hours": c(h250(Rg["R1_pooled"])), "latest_campaign_hours": c(h250(Rg["R2a_latest"])),
            "by_term_hours": c(h250(Rg["R2b_term"])), "by_locked_rate_hours": c(h250(Rg["R2c_locked"])),
            "trend_hours": c(h250(Rg["R2d_trend"])), "latest_hours_per_listed_deposit": c(h250(Rg["R0_latest"])),
            "drop_without_release_share_hours": c(h250(Rg["R3_no_release"]))},
        "ask_a": {q: {"campaign": CAMPAIGN_LABEL[q], "deposits": c(n), "principal_nzd": c(k1000(a))}
                  for q, (n, a) in c_["ask_a"].items()},
        "ask_b": {MONTHS[k]: {"maturing_nzd": c(k1000(t)), "not_on_list_nzd": c(k1000(n))}
                  for k, (t, n) in c_["ask_b"].items()},
    }
    return out


# ---------------------------------------------------------------------------------------------------------------
HEAD = PatternFill("solid", fgColor="DDE5EC")
KEY = PatternFill("solid", fgColor="F4EFE3")
NAVY = "173A5E"


def _head(ws, row, values, height=32):
    for j, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=j, value=v)
        cell.font = Font(bold=True, size=10)
        cell.fill = HEAD
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[row].height = height


def write_book(path, c_, figs):
    G, pm = c_["G"], c_["per_month"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Booking"
    ws["A1"] = "TDR-2027Q1: agent-hours to book with Harbourline Contact Services"
    ws["A1"].font = Font(bold=True, size=13, color=NAVY)
    ws["A2"] = ("List cut 2 November 2026, 18,400 term deposits maturing 1 January to 31 March 2027. Hours at the "
                "SOW HCS-KBS-2025-01 schedule 2 minutes. Block order due 20 November 2026.")
    ws["A2"].font = Font(italic=True, size=9)
    _head(ws, 4, ["Maturity month", "Deposits on the list", "With a callable number", "Expected dials not reaching "
                  "the holder", "Expected conversations", "of which retention offer", "Forecast agent-hours",
                  "Agent-hours to book"])
    r = 5
    for k in (1, 2, 3):
        m = pm[k]
        vals = ["%s 2027" % MONTHS[k], m["deposits"], m["callable"], round(m["nr"]), round(m["conv"]), round(m["ret"]),
                round(m["hours"], 1), h250(m["hours"])]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=j, value=v)
            cell.number_format = "#,##0.0" if j == 7 else "#,##0"
        ws.cell(row=r, column=8).fill = KEY
        r += 1
    tot = ["Quarter", sum(pm[k]["deposits"] for k in pm), sum(pm[k]["callable"] for k in pm), round(G["nr"]),
           round(G["conv"]), round(G["ret"]), round(G["total"], 1), h250(G["total"])]
    for j, v in enumerate(tot, 1):
        cell = ws.cell(row=r, column=j, value=v)
        cell.font = Font(bold=True)
        cell.number_format = "#,##0.0" if j == 7 else "#,##0"
    ws.cell(row=r, column=8).fill = KEY
    r += 2
    ws.cell(row=r, column=1, value="Basis").font = Font(bold=True, color=NAVY)
    basis = [
        ("Do-not-call wash at the cut",
         "%s deposits have no callable number once the holders' numbers are washed against the register as it stood on "
         "2 November 2026; they are not released (procedure 4.3) and carry no hours." % figs["components"][
             "no_callable_number"]),
        ("Release", "%s per cent of listed deposits with a callable number reached release in the seven closed "
                    "campaigns; the rest had given instructions first (procedure 4.2)." % figs["steps"][
                        "release_share_pct"]),
        ("Dialling", "Non-reaching dials and the chance of a conversation per released case, by the mix of callable "
                     "number types, from the release log, dial log and close-outs of the seven closed campaigns."),
        ("Retention offer", "Each deposit's chance that a conversation goes to the retention offer is the share of past "
                            "conversations at the same drop from the locked rate to the reinvestment rate for its term "
                            "(0.25-point bands). The list's drops are read against the January to March 2027 rates in "
                            "the campaign brief: %s four-year deposits at 5.65 per cent meet the %s per cent card, a "
                            "drop of %s points, where %s per cent of past conversations went to the retention offer." % (
                                figs["components"]["deposits_at_5_65_four_year"],
                                figs["components"]["card_four_year_pct"], figs["components"]["drop_points"],
                                figs["components"]["past_share_at_2_5_or_more_pct"])),
        ("Minutes", "1.5 per dial that does not reach the holder, 8 per conversation, 22 per retention-offer "
                    "conversation (schedule 2). Hours to book rounded to the nearest 250 (procedure 6.1)."),
    ]
    for k, v in basis:
        r += 1
        ws.cell(row=r, column=1, value=k).alignment = Alignment(vertical="top")
        cell = ws.cell(row=r, column=2, value=v)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=8)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = 42 if len(v) > 190 else 30
    for j, w in enumerate([22, 13, 13, 15, 14, 13, 13, 13], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Kept at 30 days")
    ws2["A1"] = "Deposits on each closed campaign's list still on term deposit with the Society 30 days after maturity"
    ws2["A1"].font = Font(bold=True, size=12, color=NAVY)
    ws2["A2"] = ("Reinvested on the deposit's own account at maturity, or the maturity proceeds paid that day into a "
                 "term deposit opened with them; either still open 30 days after maturity. Principal kept: the "
                 "deposit's principal, or the proceeds transferred into the new deposit. NZ$, nearest thousand.")
    ws2["A2"].font = Font(italic=True, size=9)
    ws2["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws2.merge_cells("A2:E2")
    ws2.row_dimensions[2].height = 40
    _head(ws2, 4, ["Campaign", "Maturities", "Deposits on the list", "Still on term deposit at 30 days",
                   "Principal still on term deposit (NZ$)"])
    r = 5
    for q in W.PAST:
        n, a = c_["ask_a"][q]
        for j, v in enumerate(["TDR-%s" % q, CAMPAIGN_LABEL[q], int(c_["listed"][q]), n, k1000(a)], 1):
            cell = ws2.cell(row=r, column=j, value=v)
            if j >= 3:
                cell.number_format = "#,##0"
        r += 1
    for j, w in enumerate([14, 24, 16, 18, 22], 1):
        ws2.column_dimensions[get_column_letter(j)].width = w

    ws3 = wb.create_sheet("Maturing Q1 2027")
    ws3["A1"] = "Principal maturing January to March 2027: term deposits and investment certificates, all members"
    ws3["A1"].font = Font(bold=True, size=12, color=NAVY)
    ws3["A2"] = ("Term deposits and certificates held in the core on 2 November 2026, each account once, and the "
                 "certificates still on the investment platform; the part not on the TDR-2027Q1 list. NZ$, nearest "
                 "thousand.")
    ws3["A2"].font = Font(italic=True, size=9)
    ws3["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws3.merge_cells("A2:C2")
    ws3.row_dimensions[2].height = 40
    _head(ws3, 4, ["Maturity month", "Principal maturing (NZ$)", "Not on the list (NZ$)"])
    r = 5
    for k in (1, 2, 3):
        t, n = c_["ask_b"][k]
        for j, v in enumerate(["%s 2027" % MONTHS[k], k1000(t), k1000(n)], 1):
            cell = ws3.cell(row=r, column=j, value=v)
            if j >= 2:
                cell.number_format = "#,##0"
        r += 1
    for j, w in enumerate([18, 24, 22], 1):
        ws3.column_dimensions[get_column_letter(j)].width = w

    ws4 = wb.create_sheet("Notes")
    ws4["A1"] = "Notes"
    ws4["A1"].font = Font(bold=True, size=12, color=NAVY)
    notes = [
        ("As of", "List TDR-2027Q1 cut 2 November 2026 (18,400 term deposits); contact points and the do-not-call "
                  "register as held that day; reinvestment rates for January to March 2027 as approved by ALCO and "
                  "carried in the draft campaign brief of 3 November 2026; Harbourline close-outs to the July to "
                  "September 2026 campaign."),
        ("Agent-hours", "Billed agent-minutes under SOW HCS-KBS-2025-01 schedule 2 (1.5 a dial that does not reach "
                        "the holder, 8 a conversation, 22 a conversation that goes to the retention offer), over 60. "
                        "Not rostered time."),
        ("Retention offer", "Conversations closed RTK or RTW (schedule 3)."),
        ("Drop", "The deposit's rate less the reinvestment rate for its term in the campaign brief for the quarter it "
                 "matures in. Shares of past conversations are taken in 0.25-point bands of drop across all seven "
                 "closed campaigns, as procedure 6.1 has the forecast draw on every closed campaign."),
        ("Not released", "Deposits whose holders have no callable number after the do-not-call wash (procedure "
                         "4.3), and the share of the rest that instruct before release (procedure 4.2)."),
        ("Rounding", "Hours to the nearest 250, each month from its own forecast (procedure 6.1); deposits whole; "
                     "NZ$ to the nearest thousand."),
        ("Kept at 30 days", "Own-account reinvestments, and maturity proceeds paid that day into a new term deposit, "
                            "still open 30 days after maturity; new money added to a new deposit is not counted."),
        ("Maturing Q1 2027", "The core holdings view lists a joint deposit under each holder; counted once per "
                             "account. Certificates still on the investment platform are taken from its register of "
                             "30 June 2026, less those the migration batches moved to the core."),
    ]
    for r, (k, v) in enumerate(notes, 3):
        ws4.cell(row=r, column=1, value=k).font = Font(bold=True)
        ws4.cell(row=r, column=1).alignment = Alignment(vertical="top")
        cell = ws4.cell(row=r, column=2, value=v)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws4.row_dimensions[r].height = 15 * (1 + len(v) // 95)
    ws4.column_dimensions["A"].width = 18
    ws4.column_dimensions["B"].width = 100
    for sh in (ws, ws2, ws3, ws4):
        sh.page_setup.orientation = "landscape"
        sh.page_setup.paperSize = sh.PAPERSIZE_A4
        sh.sheet_properties.pageSetUpPr.fitToPage = True
        sh.page_setup.fitToWidth = 1
        sh.page_setup.fitToHeight = 0
    ws.print_title_rows = "4:4"
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["product"], W.PEOPLE["product"], "2026-11-04T01:05:12Z",
                       "2026-11-05T03:48:30Z", excel=True)


# ---------------------------------------------------------------------------------------------------------------
def chart_png(c_, figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    G, pm = c_["G"], c_["per_month"]
    surface, ink, ink2, muted, grid = "#ffffff", "#1f2428", "#4a535b", "#7d868e", "#e3e6e8"
    cols = ("#b9c7d3", "#6f8fab", "#173a5e")
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.hashsalt": "task137"})
    fig, ax = plt.subplots(figsize=(6.6, 3.15), dpi=200)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    x = np.arange(3)
    dial = np.array([pm[k]["nr"] * W.MIN_NOT_REACHED / 60.0 for k in (1, 2, 3)])
    conv = np.array([pm[k]["conv"] * W.MIN_CONVERSATION / 60.0 for k in (1, 2, 3)])
    ret = np.array([pm[k]["ret"] * (W.MIN_RETENTION - W.MIN_CONVERSATION) / 60.0 for k in (1, 2, 3)])
    w = 0.52
    ax.bar(x, dial, w, color=cols[0], label="Dials that do not reach the holder", zorder=2)
    ax.bar(x, conv, w, bottom=dial, color=cols[1], label="Conversations (first 8 minutes)", zorder=2)
    ax.bar(x, ret, w, bottom=dial + conv, color=cols[2], label="Retention offer (further 14 minutes)", zorder=2)
    for i, k in enumerate((1, 2, 3)):
        top = dial[i] + conv[i] + ret[i]
        ax.annotate("%s hours" % figs["call"]["hours_by_month"][MONTHS[k]], xy=(i, top), xytext=(0, 4),
                    textcoords="offset points", ha="center", va="bottom", fontsize=8.6, color=ink, weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(["%s\n%s deposits" % (MONTHS[k], figs["steps"]["deposits_by_month"][MONTHS[k]])
                        for k in (1, 2, 3)], fontsize=8, color=ink2)
    ax.set_ylim(0, 2400)
    ax.set_yticks(range(0, 2401, 500))
    ax.set_yticklabels(["{:,}".format(v) for v in range(0, 2401, 500)])
    ax.tick_params(axis="y", colors=muted, labelsize=7.5, length=0)
    ax.tick_params(axis="x", length=0, pad=4)
    ax.yaxis.grid(True, color=grid, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#a7b0b8")
    ax.set_ylabel("Agent-hours", color=ink2, fontsize=8)
    ax.legend(loc="upper left", frameon=False, fontsize=7.2, labelcolor=ink2)
    ax.set_title("Seven in ten hours are conversations, most of them retention offers",
                 fontsize=9, color=ink, loc="left", weight="bold")
    fig.subplots_adjust(left=0.11, right=0.985, top=0.9, bottom=0.17)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=surface, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_note(path, c_, figs):
    import docx
    from docx.shared import Mm, Pt, RGBColor
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    sec = d.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.top_margin, sec.bottom_margin = Mm(16), Mm(14)
    fc, fs = figs["components"], figs["steps"]

    def para(text=None, bold=False, size=None, color=None, after=4, italic=False):
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        if text:
            run = p.add_run(text)
            run.bold, run.italic = bold, italic
            if size:
                run.font.size = Pt(size)
            if color:
                run.font.color.rgb = RGBColor.from_string(color)
        return p

    para("Kaimai Building Society  |  Term Deposits", size=9, color="5B6670", after=2)
    para("January to March 2027 maturity calls: book %s agent-hours with Harbourline" % figs["call"]["booking_hours"],
         bold=True, size=14, color=NAVY, after=2)
    para("To the Deposits Committee (chair %s, Head of Deposits), for its meeting on 17 November. From %s, Term "
         "Deposits Product Manager. 5 November 2026." % (W.PEOPLE["head"], W.PEOPLE["product"]), size=9,
         color="5B6670", after=8)
    p = para(after=6)
    p.add_run("Book %s agent-hours with Harbourline for the January to March 2027 list: %s for the deposits maturing "
              "in January, %s for February and %s for March." % (
                  figs["call"]["booking_hours"], figs["call"]["hours_by_month"]["January"],
                  figs["call"]["hours_by_month"]["February"], figs["call"]["hours_by_month"]["March"])).bold = True
    p.add_run(" The block is due with Harbourline on Friday 20 November; it is payable in full, and hours beyond it "
              "cost the block rate plus 35 per cent.")
    d.add_picture(io.BytesIO(chart_png(c_, figs)), width=Mm(168))
    d.paragraphs[-1].paragraph_format.space_after = Pt(1)
    para("Agent-hours to book by maturity month. Source: TDR-2027Q1 list and contact points at 2 November 2026; "
         "Harbourline dial logs and close-outs for the seven campaigns closed since January 2025; SOW HCS-KBS-2025-01 "
         "schedule 2.", size=8, color="5B6670", after=6, italic=True)
    para("Why the block is larger per deposit than any campaign so far", bold=True, size=10.5, color=NAVY, after=2)
    para("%s of the %s deposits on the list are four-year deposits opened at 5.65 per cent in January to March "
         "2023. They reinvest at the %s per cent four-year rate ALCO has approved for the quarter, a drop of %s "
         "points. In every campaign since January 2025, whether a holder Harbourline reached said they meant to move "
         "the money, and so went through the 22-minute retention offer, followed the drop from the deposit's rate to "
         "the rate it rolled onto: %s per cent of conversations where the rate rose, %s per cent at drops of 2.5 "
         "points or more. The four-year deposits we have called so far were opened in 2021 and 2022, when rates were "
         "low, and few of their holders took the offer. On this list about %s per cent of an expected %s "
         "conversations should go to the retention offer, against %s per cent across the seven campaigns." % (
             fc["deposits_at_5_65_four_year"], fs["listed_deposits"], fc["card_four_year_pct"], fc["drop_points"],
             fs["past_share_negative_drop_pct"], fc["past_share_at_2_5_or_more_pct"], fc["retention_share_pct"],
             fc["expected_conversations"], fc["past_pooled_share_pct"]), after=6)
    para("How the hours are built", bold=True, size=10.5, color=NAVY, after=2)
    para("Harbourline bills 1.5 minutes for each dial that does not reach the holder, 8 for each conversation and 22 "
         "for each retention-offer conversation. Dialling per case comes from the seven closed campaigns for each mix "
         "of callable numbers, after washing the list's numbers against the do-not-call register at the cut: %s "
         "deposits have no callable number and will get the maturity letter only. %s per cent of deposits with a "
         "callable number have reached release in past campaigns; the rest gave us instructions first." % (
             fc["no_callable_number"], fs["release_share_pct"]), after=6)
    para("In the workbook", bold=True, size=10.5, color=NAVY, after=2)
    para("td_booking_q1_2027.xlsx carries the booking by month with its basis, what each campaign since January 2025 "
         "kept on term deposit 30 days after maturity, and the principal maturing across the book in each month of "
         "the quarter with the part the list does not cover.", after=8)
    para("Hours are Harbourline's billed agent-minutes under schedule 2, not rostered time. Each month is rounded "
         "from its own forecast to the nearest 250 hours, as procedure v4 rounds the block.", size=8, color="5B6670",
         after=0, italic=True)
    foot = d.sections[0].footer.paragraphs[0]
    run = foot.add_run("Kaimai Building Society  |  Term Deposits  |  Internal")
    run.font.size = Pt(7.5)
    run.font.color.rgb = RGBColor.from_string("5B6670")
    d.core_properties.title = "TDR-2027Q1 Harbourline block"
    d.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["product"], W.PEOPLE["product"], "2026-11-05T02:16:40Z", "2026-11-05T04:02:19Z",
                       title="TDR-2027Q1 Harbourline block")


# ---------------------------------------------------------------------------------------------------------------
SOURCES = {
    W.F_LIST_FWD: "the society's retention list for term deposits maturing January to March 2027, cut 2 November 2026",
    W.F_LISTS_2025: "the retention lists for the four 2025 campaigns, from the pre-upgrade core banking report",
    W.F_LISTS_2026: "the retention lists for the three 2026 campaigns, from the upgraded core",
    W.F_RELEASE: "the society's case release log for the seven closed campaigns",
    W.F_DIALS: "Harbourline's dial log for the seven closed campaigns",
    W.F_CLOSEOUT: "Harbourline's case close-outs for the seven closed campaigns",
    W.F_CONTACTS: "contact points held at the cut for the members on the January to March 2027 list",
    W.F_DNC: "the society's do-not-call register at 2 November 2026",
    W.F_SOW: "statement of work HCS-KBS-2025-01 between the society and Harbourline, with its schedules",
    W.F_PROCEDURE: "the society's term deposit retention procedure, version 4",
    W.F_THREAD: "the block-order email thread between the society and Harbourline, 28 October to 4 November 2026",
    W.F_EVENTS: "term deposit account events, January 2025 to October 2026, for the listed accounts and their holders' "
                "new term deposits",
    W.F_TRANSFERS: "transfers of principal into and out of the accounts in the events extract",
    W.F_HOLDINGS: "the core's term holdings view at 2 November 2026 (term deposits and migrated certificates maturing "
                  "January to June 2027)",
    W.F_KIP: "the legacy investment platform's certificate register at 30 June 2026",
    W.F_BATCHES: "the investment platform to core migration batches, July to October 2026",
    W.F_NOTES: "the deposits analytics team's notes on the extracts",
    W.F_OUTLOOK: "treasury's FY2027 term funding outlook prepared for ALCO",
    W.F_PROPOSAL: "Harbourline's 2027 service and staffing proposal",
}
for _q in W.PAST + [W.FWD]:
    SOURCES[W.brief_name(_q)] = "the campaign brief for TDR-%s, with the quarter's reinvestment rates%s" % (
        _q, " (draft)" if _q == W.FWD else "")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write_metadata(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-10-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task137",
        "title": "How many agent-hours Kaimai Building Society books with Harbourline for its January to March 2027 "
                 "term deposit maturity calls",
        "domain": "Banking, Credit & Financial Risk",
        "subdomain": "deposit-liquidity-behaviour (term deposit retention at maturity on the repricing gap, at a New "
                     "Zealand building society that outsources its maturity calls)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "other: the booking and its three maturity months, the note's chart, what each of seven closed "
                        "campaigns kept on term deposit at 30 days (count and principal), and the quarter's maturing "
                        "principal by month with the part off the list",
        "as_of": "2026-11-04",
        "deliverables": [BOOK, NOTE],
        "distractor_files": list(W.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task137/generator/build.py (seeded, deterministic) around a "
                               "fictional New Zealand building society (Kaimai Building Society), contact centre "
                               "(Harbourline Contact Services) and people; no real organisation, person, account or "
                               "telephone number is depicted.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task137/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


def main(target, golden, figures_path, metadata_path):
    os.makedirs(golden, exist_ok=True)
    c_ = compute(target)
    figs = figures(c_)
    write_book(os.path.join(golden, BOOK), c_, figs)
    write_note(os.path.join(golden, NOTE), c_, figs)
    with open(figures_path, "w", encoding="utf-8") as fh:
        json.dump(figs, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    write_metadata(target, metadata_path)
    return c_, figs
