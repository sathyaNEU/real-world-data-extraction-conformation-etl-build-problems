"""Write the golden deliverables: card_reissue_request.pdf (three pages) and common_point_trace.xlsx (one
sheet per page). Every figure comes from golden.solve() on the shipped files."""
import datetime as dt
import io
import os

import numpy as np
import pandas as pd

import golden as G

ACCENT = "#2a78d6"
CONTEXT = "#b9bec6"
INK = "#1d2430"
INK2 = "#52514e"


def fmt_d(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def money(x):
    return "${:,.2f}".format(x)


def short_name(m):
    return m.replace("Ferrier Creek Travel Plaza - ", "Ferrier Creek ")


def screen_rows(sc, names, keep, n=6, floor=10):
    rows = []
    sub = sc[sc.v >= floor].head(n)
    for tid in list(sub.index) + [t for t in keep if t not in sub.index and t in sc.index]:
        r = sc.loc[tid]
        rows.append((tid, names.get(tid, tid), int(r.v), int(r.b), float(r.base), float(r.lift)))
    return rows


def label(name):
    nm, _, town = name.rpartition(", ")
    nm = nm.replace("Ferrier Creek Travel Plaza - ", "Ferrier Creek ").replace("Larchmere Credit Union ATM ",
                                                                             "Larchmere ATM ")
    if town in nm or nm.startswith("Ferrier Creek"):
        return nm
    return "%s, %s" % (nm, town)


def chart_png(pooled_rows, resid_rows, hi):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.95), dpi=200, layout="constrained")
    xmax = max(max(r[5] for r in pooled_rows), max(r[5] for r in resid_rows)) * 1.55
    for ax, rows, title in ((axes[0], pooled_rows, "All 283 counterfeit cards"),
                            (axes[1], resid_rows, "The 78 the pump leaves")):
        rows = rows[::-1]
        vals = [r[5] for r in rows]
        cols = [ACCENT if r[0] in hi else CONTEXT for r in rows]
        bars = ax.barh(range(len(rows)), vals, color=cols, height=0.6)
        for b, r in zip(bars, rows):
            ax.text(b.get_width() + xmax * 0.02, b.get_y() + b.get_height() / 2,
                    "%.1f (%d cards)" % (r[5], r[2]), va="center", fontsize=6.4, color=INK)
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([label(r[1]) for r in rows], fontsize=6.4, color=INK)
        ax.set_title(title, fontsize=7.6, color=INK, loc="left", fontweight="bold")
        ax.set_xlim(0, xmax)
        ax.tick_params(axis="x", labelsize=6.2, colors=INK2)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#e6e8eb", linewidth=0.6)
        ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color("#b8bec7")
    fig.supxlabel("Lift: share of the counterfeit cards the terminal read, over the share of other members' cards "
                  "it read", fontsize=6.4, color=INK2)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def write(s, outdir):
    os.makedirs(outdir, exist_ok=True)
    vic = G.victims()
    a = G.auth()
    md = G.merchants().set_index("merchant_id")
    first_mid = a.dropna(subset=["terminal_id"]).drop_duplicates("terminal_id").set_index("terminal_id").merchant_id
    names = {t: short_name(md.loc[m, "name"]) + ", " + md.loc[m, "town"] for t, m in first_mid.items()}
    opt6, sco2 = s["terminals"]
    f6, fs = s["facts"]
    pooled = s["pooled"]
    pv = G.victims_read_at(vic, opt6)
    r78 = {k: f for k, f in vic.items() if k not in pv}
    sc78 = G.screen(r78)
    plaza = md[md.address == f6["address"]]
    cof_mid = plaza.index[plaza.name.str.contains("Coffee")][0]
    wsh_mid = plaza.index[plaza.name.str.contains("Car Wash")][0]
    cof = a.terminal_id[a.merchant_id == cof_mid].dropna().iloc[0]
    wsh = a.terminal_id[a.merchant_id == wsh_mid].dropna().iloc[0]
    p_rows = screen_rows(pooled, names, [opt6, cof, wsh, sco2], n=6)
    r_rows = screen_rows(sc78, names, [sco2], n=5, floor=3)
    n_open = len(G.open_cards() & set(s["reissue_tokens"]))
    both = len((G.exposed(opt6, vic) & G.open_cards()) & (G.exposed(sco2, vic) & G.open_cards()))
    A, B = s["ask_a"], s["ask_b"]
    s["cities"] = cashout_cities()
    s["open_claims"] = open_claims()
    write_pdf(os.path.join(outdir, "card_reissue_request.pdf"), s, f6, fs, p_rows, r_rows, both, len(pv),
              sc78.loc[sco2], len(r78), A, B)
    write_xlsx(os.path.join(outdir, "common_point_trace.xlsx"), s, f6, fs, p_rows, r_rows, both, A, B, vic)


def cashout_cities():
    """Where the disputed counterfeit transactions were made: transactions and posted CAD by town."""
    w = G.cases()
    cf = w[w.fraud_type == "Counterfeit"].drop_duplicates("retrieval_ref")
    post = G.posted_cad(set(cf.retrieval_ref))
    a = G.auth()
    mid = a[a.retrieval_ref.isin(set(cf.retrieval_ref)) & a.message_type.isin(["0100", "0200"])] \
        .drop_duplicates("retrieval_ref").set_index("retrieval_ref").merchant_id
    md = G.merchants().set_index("merchant_id")
    rows = {}
    for rrn in cf.retrieval_ref:
        m = md.loc[mid[rrn]]
        key = "%s, %s" % (m["town"], m["province_state"])
        n, v = rows.get(key, (0, 0.0))
        rows[key] = (n + 1, v + post[rrn])
    out = sorted(((k, n, round(v, 2)) for k, (n, v) in rows.items()), key=lambda x: (-x[2], x[0]))
    return out


def open_claims():
    ct = G.card_type_of()
    out = {"Debit": 0, "Credit": 0, "since": None}
    for c in G.claims():
        if c["refunded_on"] is None:
            out[ct[c["card_token"]]] += 1
            d = c["first_report_utc"].tz_convert(G.TZ).date()
            out["since"] = d if out["since"] is None else min(out["since"], d)
    return out


# ---------------------------------------------------------------------------------------------------
def write_pdf(path, s, f6, fs, p_rows, r_rows, both, n_pump, s78, n78, A, B):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
                                    KeepTogether)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=5)
    small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=9.6, textColor=colors.HexColor("#4a4f57"))
    title = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=15, leading=18, alignment=0,
                           spaceAfter=6, textColor=colors.HexColor(INK))
    h2 = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15,
                        spaceBefore=4, spaceAfter=6, textColor=colors.HexColor(INK))
    meta = ParagraphStyle("m", parent=body, fontSize=8.6, leading=11.5, textColor=colors.HexColor("#30353d"))
    box = ParagraphStyle("x", parent=body, fontName="Helvetica-Bold", fontSize=10, leading=13.5)

    def tbl(data, widths, align_right_from=1, bold_last=False):
        t = Table(data, colWidths=widths, repeatRows=1)
        st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.6),
              ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6),
              ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor("#30353d")),
              ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#9aa1ab")),
              ("ALIGN", (align_right_from, 0), (-1, -1), "RIGHT"),
              ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
        if bold_last:
            st += [("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 8.6),
                   ("LINEABOVE", (0, -1), (-1, -1), 0.6, colors.HexColor("#30353d"))]
        t.setStyle(TableStyle(st))
        return t

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(colors.HexColor(INK))
        canvas.drawString(54, 760, "Larchmere Credit Union")
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(558, 760, "Board Risk Committee, Thursday 8 October 2026, item 5")
        canvas.setStrokeColor(colors.HexColor("#30353d"))
        canvas.setLineWidth(0.6)
        canvas.line(54, 754, 558, 754)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5a606a"))
        canvas.drawString(54, 34, "Card reissue request under CP-14. Internal: board and management only.")
        canvas.drawRightString(558, 34, "Page %d of 3" % doc.page)
        canvas.restoreState()

    n = s["reissue"]
    story = [
        Paragraph("To: Brenda Figueroa, Chair, and members of the Board Risk Committee<br/>"
                  "From: Laurie Townsend, Fraud and Risk Manager<br/>"
                  "Paper date: 6 October 2026. Card data as at Monday 5 October 2026.", meta),
        Spacer(1, 6),
        Paragraph("Reissue %s member cards read at two compromised terminals" % format(n, ","), title),
        Table([[Paragraph("Decision sought: approve the reissue of %s member cards under CP-14 section 6." %
                          format(n, ","), box)]], colWidths=[504],
              style=TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(ACCENT)),
                                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef4fb")),
                                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])),
        Spacer(1, 8),
        Paragraph(
            "Since 24 August, %d of our members' cards have been used for counterfeit fraud. The common-point screen "
            "in CP-14 section 4 puts the pay-at-pump terminal at the Ferrier Creek Travel Plaza on Highway 416 first: "
            "it read %d of the %d cards by contact in the 60 days before their first counterfeit use. The plaza's coffee "
            "counter and car wash also stand out in that screen, but every counterfeit card either of them read had "
            "been read at the pump while the pump was compromised. They are where the same commuters stopped, not "
            "further sources, and we are not reissuing on them." % (s["victims"], n_pump, s["victims"]), body),
        Paragraph(
            "Screening the %d cards the pump does not account for gives a second source the full screen hides: a "
            "card terminal at Lombard Market in Smiths Falls read %d of them, %.0f per cent, against %.1f per cent of "
            "other members' cards. The %d cards left after both terminals were all used outside Ontario in the weeks "
            "before their fraud, and no terminal stands out among them. Every counterfeit card was itself replaced "
            "the day its holder reported it."
            % (n78, int(s78.v), 100 * s78.share_v, 100 * s78.base, s["unexplained"]), body),
        Spacer(1, 4),
        tbl([["Merchant", "Town", "Terminal ID", "First read", "Last read", "Cards"],
             [short_name(f6["merchant"]), f6["town"], f6["terminal_id"], fmt_d(f6["first_read"]),
              fmt_d(f6["last_read"]), format(f6["cards_read_open"], ",")],
             [fs["merchant"], fs["town"], fs["terminal_id"], fmt_d(fs["first_read"]), fmt_d(fs["last_read"]),
              format(fs["cards_read_open"], ",")],
             ["Cards to reissue, each counted once", "", "", "", "", format(n, ",")]],
            [150, 70, 64, 78, 78, 50], align_right_from=5, bold_last=True),
        Spacer(1, 3),
        Paragraph("First and last read: the first and last time the terminal read, by contact, a card later used in "
                  "counterfeit fraud (Eastern dates). Cards: member cards the terminal read by contact (entry mode 05, "
                  "80 or 90) inside that window and still open on 5 October; %d cards read at both terminals are "
                  "counted once. Neither terminal ID has been used since: the pump's last appears on 31 August and the "
                  "store's on 14 September." % both, small),
        Spacer(1, 6),
        Image(chart_png(p_rows, r_rows, {f6["terminal_id"], fs["terminal_id"]}), width=6.95 * inch,
              height=6.95 * inch * 2.95 / 7.0),
        Paragraph("Common-point screen (CP-14 s4), terminals that read ten or more of the cards on the left and three "
                  "or more on the right. Lift above 1 means the terminal read counterfeit cards more often than it read "
                  "other members' cards over the same weeks.", small),
        PageBreak(),
    ]
    tot = {f: A["Debit"][f] + A["Credit"][f] for f in ("gross", "recovered", "net")}
    story += [
        Paragraph("What the counterfeit wave has cost to 4 October", h2),
        Paragraph(
            "Losses are the Canadian dollar amounts posted to members' accounts for the counterfeit transactions they "
            "disputed, which for the transactions in New York and New Jersey is the converted amount, not the US dollar "
            "figure on the dispute form. A transaction disputed under more than one case number is counted once. "
            "Recovered is the chargeback money received, less the credits the acquirers took back at "
            "pre-arbitration; chargebacks still in progress are not counted.", body),
        Spacer(1, 4),
        tbl([["", "Debit cards", "Credit cards", "All cards"],
             ["Gross loss", money(A["Debit"]["gross"]), money(A["Credit"]["gross"]), money(tot["gross"])],
             ["Recovered through chargebacks", money(A["Debit"]["recovered"]), money(A["Credit"]["recovered"]),
              money(tot["recovered"])],
             ["Net loss", money(A["Debit"]["net"]), money(A["Credit"]["net"]), money(tot["net"])]],
            [190, 105, 105, 104], bold_last=True),
        Spacer(1, 4),
        Paragraph("Source: fraud desk case workbook (counterfeit cases opened to 4 October), authorisation host "
                  "billing amounts, chargeback log to 4 October. CP-14 section 7.", small),
        Spacer(1, 12),
        Paragraph("Where the counterfeit cards were used", ParagraphStyle("h3", parent=h2, fontSize=10.5)),
        tbl([["Town", "Disputed transactions", "Posted (CAD)"]] +
            [[k, str(n), money(v)] for k, n, v in s["cities"]] +
            [["All towns", str(sum(x[1] for x in s["cities"])), money(round(sum(x[2] for x in s["cities"]), 2))]],
            [220, 140, 144], bold_last=True),
        Spacer(1, 4),
        Paragraph("Cash withdrawals at independent ATMs and purchases at electronics shops and a pharmacy, all by "
                  "magnetic stripe (entry mode 90).", small),
        PageBreak(),
        Paragraph("How members were treated: refunds against MS-3", h2),
        Paragraph(
            "MS-3 promises a refund within ten business days of the member's report. Each counterfeit claim is timed "
            "from the day the member first reported it, in Eastern time, to the day the refund posted, counting "
            "business days only (weekends and the MS-3 holidays, Labour Day in this period, excluded). A claim that "
            "was closed and later re-opened under a new case number keeps its first report date. Claims not yet "
            "refunded on 4 October are left out.", body),
        Spacer(1, 4),
        tbl([["", "Debit cards", "Credit cards"],
             ["Counterfeit claims refunded", str(B["Debit"]["refunded"]), str(B["Credit"]["refunded"])],
             ["Refunded within ten business days", str(B["Debit"]["within"]), str(B["Credit"]["within"])],
             ["Longest wait of a refunded member, business days", str(B["Debit"]["longest"]),
              str(B["Credit"]["longest"])]],
            [260, 122, 122]),
        Spacer(1, 4),
        Paragraph("Source: fraud desk case workbook; MS-3 effective 1 January 2026 and its 2026 holiday list.", small),
        Spacer(1, 10),
        Paragraph("Still open on 4 October and not in the table: %d debit and %d credit counterfeit claims, all "
                  "reported on or after %s. The longest waits above are claims that were closed and later re-opened "
                  "under a new case number; MS-3 times them from the member's first report."
                  % (s["open_claims"]["Debit"], s["open_claims"]["Credit"], fmt_d(s["open_claims"]["since"])), body),
    ]
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=72, bottomMargin=54,
                            title="Card reissue request, Board Risk Committee 8 October 2026",
                            author="Larchmere Credit Union", creator="Larchmere Credit Union",
                            producer="Larchmere Credit Union", subject="Card reissue request under CP-14")
    doc.build(story, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------------
def write_xlsx(path, s, f6, fs, p_rows, r_rows, both, A, B, vic):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    bold = Font(bold=True)
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="30353D")
    thin = Border(top=Side(style="thin", color="30353D"))
    wb = Workbook()

    def header(ws, r, cols):
        for j, c in enumerate(cols, 1):
            x = ws.cell(row=r, column=j, value=c)
            x.font, x.fill = head, fill
            x.alignment = Alignment(wrap_text=True, vertical="top")

    def widths(ws, ws_w):
        for j, w in enumerate(ws_w, 1):
            ws.column_dimensions[get_column_letter(j)].width = w

    # sheet 1 ---------------------------------------------------------------------------------------
    ws = wb.active
    ws.title = "1 Reissue"
    ws["A1"] = "Card reissue request, page 1: cards to reissue and where they were compromised"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Board Risk Committee 8 October 2026. Card data as at 5 October 2026. Prepared by Fraud and Risk."
    header(ws, 4, ["Merchant", "Merchant ID", "Town", "Terminal ID", "First read", "Last read",
                   "Open cards read in window"])
    for i, f in enumerate((f6, fs), start=5):
        vals = [f["merchant"], f["merchant_id"], f["town"], f["terminal_id"], f["first_read"], f["last_read"],
                f["cards_read_open"]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            if j in (5, 6):
                c.number_format = "d mmm yyyy"
            if j == 7:
                c.number_format = "#,##0"
    ws.cell(row=7, column=1, value="Cards to reissue (each counted once)").font = bold
    c = ws.cell(row=7, column=7, value=s["reissue"])
    c.font, c.number_format = bold, "#,##0"
    for j in range(1, 8):
        ws.cell(row=7, column=j).border = thin
    ws.cell(row=8, column=1, value="Cards read at both terminals: %d. Read = POS entry mode 05, 80 or 90 (CP-14 s3); "
                                   "open on 5 October per the card history (CP-14 s6)." % both)
    r = 10
    ws.cell(row=r, column=1, value="Common-point screen, all %d counterfeit cards, 60-day lookback (CP-14 s4); "
                                   "terminals reading 10 or more" % s["victims"]).font = bold
    header(ws, r + 1, ["Terminal", "Terminal ID", "Counterfeit cards read", "Other members' cards read",
                       "Member base rate", "Lift"])
    for k, row in enumerate(p_rows, start=r + 2):
        tid, nm, v, b, base, lift = row
        for j, x in enumerate([nm, tid, v, b, base, lift], 1):
            c = ws.cell(row=k, column=j, value=x)
            c.number_format = {3: "#,##0", 4: "#,##0", 5: "0.00%", 6: "0.0"}.get(j, "General")
    r = r + 3 + len(p_rows)
    ws.cell(row=r, column=1, value="Screen of the 78 cards the pump does not account for; terminals reading 3 or "
                                   "more").font = bold
    header(ws, r + 1, ["Terminal", "Terminal ID", "Counterfeit cards read", "Other members' cards read",
                       "Member base rate", "Lift"])
    for k, row in enumerate(r_rows, start=r + 2):
        tid, nm, v, b, base, lift = row
        for j, x in enumerate([nm, tid, v, b, base, lift], 1):
            c = ws.cell(row=k, column=j, value=x)
            c.number_format = {3: "#,##0", 4: "#,##0", 5: "0.00%", 6: "0.0"}.get(j, "General")
    r = r + 3 + len(r_rows)
    ws.cell(row=r, column=1, value="Cards to reissue").font = bold
    header(ws, r + 1, ["Card token", "Member ID", "Card type", "Read at pump", "Read at Lombard Market"])
    c_, _, _ = G.cards()
    ci = c_.set_index("card_token")
    e6 = G.exposed(f6["terminal_id"], vic)
    es = G.exposed(fs["terminal_id"], vic)
    for k, tok in enumerate(sorted(s["reissue_tokens"], key=lambda t: (ci.loc[t, "member_id"], t)), start=r + 2):
        vals = [tok, ci.loc[tok, "member_id"], ci.loc[tok, "card_type"], "yes" if tok in e6 else "",
                "yes" if tok in es else ""]
        for j, v in enumerate(vals, 1):
            ws.cell(row=k, column=j, value=v)
    widths(ws, [44, 18, 15, 17, 15, 12, 14])
    ws.freeze_panes = "A5"

    # sheet 2 ---------------------------------------------------------------------------------------
    ws = wb.create_sheet("2 Losses")
    ws["A1"] = "Card reissue request, page 2: counterfeit losses to 4 October 2026 (CAD)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Gross: amount posted to the member's account (authorisation billing amount), each disputed "
                "transaction once. Recovered: chargeback money received net of pre-arbitration debits.")
    header(ws, 4, ["", "Debit cards", "Credit cards", "All cards"])
    for i, (lab, f) in enumerate((("Gross loss", "gross"), ("Recovered through chargebacks", "recovered"),
                                  ("Net loss", "net")), start=5):
        ws.cell(row=i, column=1, value=lab)
        for j, k in enumerate(("Debit", "Credit"), 2):
            c = ws.cell(row=i, column=j, value=A[k][f])
            c.number_format = "$#,##0.00"
        c = ws.cell(row=i, column=4, value=round(A["Debit"][f] + A["Credit"][f], 2))
        c.number_format = "$#,##0.00"
    for j in range(1, 5):
        ws.cell(row=7, column=j).font = bold
        ws.cell(row=7, column=j).border = thin
    w = G.cases()
    cf = w[w.fraud_type == "Counterfeit"].drop_duplicates("retrieval_ref")
    post = G.posted_cad(set(cf.retrieval_ref))
    cb = G.chargebacks()
    rec = cb[cb.amount_cad.notna()].groupby("retrieval_ref").amount_cad.sum()
    ct = G.card_type_of()
    a = G.auth()
    cur = a[a.retrieval_ref.isin(set(cf.retrieval_ref)) & a.message_type.isin(["0100", "0200"])] \
        .drop_duplicates("retrieval_ref").set_index("retrieval_ref").currency_txn
    ws.cell(row=9, column=1, value="Where the counterfeit cards were used").font = bold
    header(ws, 10, ["Town", "Disputed transactions", "Posted (CAD)"])
    for k, (town, n_, v_) in enumerate(s["cities"], start=11):
        ws.cell(row=k, column=1, value=town)
        ws.cell(row=k, column=2, value=n_)
        ws.cell(row=k, column=3, value=v_).number_format = "$#,##0.00"
    r0 = 11 + len(s["cities"]) + 1
    ws.cell(row=r0, column=1, value="Disputed counterfeit transactions").font = bold
    header(ws, r0 + 1, ["Retrieval reference", "Card type", "Card token", "Transaction date",
                        "Merchant as on statement", "Currency", "Dispute form amount", "Posted (CAD)",
                        "Recovered (CAD)"])
    rows = cf.sort_values(["txn_date", "retrieval_ref"])
    for k, x in enumerate(rows.itertuples(index=False), start=r0 + 2):
        vals = [x.retrieval_ref, ct[x.card_token], x.card_token, x.txn_date, x.merchant_as_on_statement,
                "USD" if cur.get(x.retrieval_ref) == "840" else "CAD", x.amount, post[x.retrieval_ref],
                round(float(rec.get(x.retrieval_ref, 0.0)), 2)]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=k, column=j, value=v)
            if j == 4:
                c.number_format = "yyyy-mm-dd"
            if j in (7, 8, 9):
                c.number_format = "#,##0.00"
    widths(ws, [30, 13, 19, 15, 44, 10, 18, 14, 15])
    ws.freeze_panes = "A5"

    # sheet 3 ---------------------------------------------------------------------------------------
    ws = wb.create_sheet("3 Refunds")
    ws["A1"] = "Card reissue request, page 3: counterfeit claims refunded against MS-3"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Business days from the member's first report (Eastern time; weekend and holiday reports start the "
                "next business day) to the refund; MS-3 holidays excluded; a re-opened claim keeps its first report.")
    header(ws, 4, ["", "Debit cards", "Credit cards"])
    for i, (lab, f) in enumerate((("Counterfeit claims refunded", "refunded"),
                                  ("Refunded within ten business days", "within"),
                                  ("Longest wait of a refunded member (business days)", "longest")), start=5):
        ws.cell(row=i, column=1, value=lab)
        for j, k in enumerate(("Debit", "Credit"), 2):
            ws.cell(row=i, column=j, value=B[k][f])
    ws.cell(row=8, column=1, value="Counterfeit claims still open on 4 October")
    for j, k in enumerate(("Debit", "Credit"), 2):
        ws.cell(row=8, column=j, value=s["open_claims"][k])
    hol = set(G.holidays())
    ws.cell(row=9, column=1, value="Refunded counterfeit claims").font = bold
    header(ws, 10, ["Case number(s)", "Card type", "First report (Eastern)", "Refund posted", "Business days",
                    "Within ten"])
    wc = w[w.fraud_type == "Counterfeit"]
    rows_ = []
    for c_ in G.claims():
        if c_["refunded_on"] is None:
            continue
        rd = c_["first_report_utc"].tz_convert(G.TZ).date()
        d0 = rd
        while not G.is_bd(d0, hol):
            d0 += dt.timedelta(1)
        wait = G.bd_wait(d0, c_["refunded_on"], hol)
        tok = c_["card_token"]
        nums = sorted(set(wc.case_number[wc.card_token == tok]))
        rows_.append([", ".join(nums), ct[tok], rd, c_["refunded_on"], wait, "yes" if wait <= 10 else "no"])
    rows_.sort(key=lambda x: (x[2], x[0]))
    for k, vals in enumerate(rows_, start=11):
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=k, column=j, value=v)
            if j in (3, 4):
                c.number_format = "yyyy-mm-dd"
    widths(ws, [46, 13, 21, 15, 15, 11])
    ws.freeze_panes = "A11"
    wb.properties.creator = "Larchmere Credit Union"
    wb.save(path)
    _pin_zip(path)


def _pin_zip(path):
    import re
    import shutil
    import zipfile
    stamp = (2026, 10, 6, 16, 20, 0)
    iso = "2026-10-06T16:20:00Z"
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                t = data.decode("utf8")
                t = re.sub(r"(<dcterms:created[^>]*>).*?(</dcterms:created>)", r"\g<1>%s\g<2>" % iso, t)
                t = re.sub(r"(<dcterms:modified[^>]*>).*?(</dcterms:modified>)", r"\g<1>%s\g<2>" % iso, t)
                t = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator>Larchmere Credit Union</dc:creator>", t)
                data = t.encode("utf8")
            if item.filename == "docProps/app.xml":
                t = data.decode("utf8")
                t = re.sub(r"<Application>.*?</Application>", "<Application>Microsoft Excel</Application>", t)
                data = t.encode("utf8")
            zi = zipfile.ZipInfo(item.filename, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
    shutil.move(tmp, path)
