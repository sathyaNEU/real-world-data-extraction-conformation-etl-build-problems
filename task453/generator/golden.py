"""The golden deliverables of task453, computed from the pack in target/ (the survey's published cells are read from
survey.tables, which the report PDFs print; verify.py reads them back off the PDFs):

  designation_certificate_2026.pdf   the trustees' certificate: the 2026 share, the verdict, the designations, a chart
  levy_and_bypass_2026.xlsx          each crematorium's 2026 levy, and each abated crematorium's bypassed cremations

and generator/figures.json, every graded and supporting figure."""
import datetime as dt
import io
import json
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import methods as M
import survey as S
import world as W

ET = ZoneInfo(W.TZ_NAME)
INCLUDED_H = {"BRV-CREM", "BRV-CRMC", "BRV-DIRC", "BRV-CHAP", "BRV-XTND", "BRV-ORGN", "BRV-WEBC", "BRV-MEMB",
              "BRV-SCAT", "BRV-CERT"}
INCLUDED_S = {"Cremation", "Cremation - child", "Direct cremation", "Chapel 40 min", "Chapel 40 min (child)",
              "Chapel extension 20 min", "Organist", "Webcast & recording", "Memorial book entry", "Garden scattering",
              "Certified copy - cremation certificate"}
INCLUDED_F = {"CRM", "DCR", "CHP", "CHX", "ORG", "WEB", "BOR", "SCT", "CRT"}
CODE_OF_SITE = {"HMC": "CM-0417", "OHC": "CM-0738"}
CODE_OF_LOCATION = {"Fenwick Harbour": "CM-1182", "Stannard Bay": "CM-2034", "Port Alder": "CM-1768",
                    "Sorrel Bay": "CM-2409"}


def P(target, key):
    return os.path.join(target, W.FILES[key])


# ---------------------------------------------------------------- readers
def register(target):
    reg = pd.read_excel(P(target, "register"), sheet_name="Members", header=3, dtype={"fund_code": str})
    fac = pd.read_excel(P(target, "register"), sheet_name="Agency facility numbers", dtype=str)
    comm = {r.fund_code: (pd.Timestamp(r.abatement_commissioned).date() if pd.notna(r.abatement_commissioned) else None)
            for r in reg.itertuples()}
    return reg, fac, comm


def cremations_2026(target):
    """The 2026 cremations: (fund code, age in completed years, sex, abated, date)."""
    reg, fac, comm = register(target)
    fmap = {}
    for r in fac.itertuples():
        fmap.setdefault(r.agency_facility_no, []).append((r.fund_code, r.valid_from, r.valid_to))
    pm = pd.read_csv(P(target, "permits"), dtype=str)
    pm = pm[pm.date_of_cremation.str.startswith("2026")]
    out = []
    for r in pm.itertuples():
        d = dt.date.fromisoformat(r.date_of_cremation)
        code = [c for c, f, t in fmap[r.crematorium_facility_no]
                if dt.date.fromisoformat(f[:10]) <= d and (not isinstance(t, str) or d <= dt.date.fromisoformat(t[:10]))]
        assert len(code) == 1
        code = code[0]
        age = int(r.age) if r.age_unit == "Y" else 0
        out.append((code, age, r.sex, comm[code] is not None and d > comm[code], d))
    return out


def call(target, tab=None, form=M.GOLDEN_FORM):
    tab = tab if tab is not None else S.tables(W.SEED)
    idx = {c[0]: i for i, c in enumerate(W.CREMATORIA)}
    cre = [(idx[c], a, s, ab) for c, a, s, ab, d in cremations_2026(target)]
    res = M.designate(cre, tab, form)
    res["n"] = np.bincount([c[0] for c in cre], minlength=len(W.CREMATORIA))
    res["n_ab"] = np.bincount([c[0] for c in cre if c[3]], minlength=len(W.CREMATORIA))
    return res


def ledger_lines(target):
    """The three receivables files as one table: ledger, fund code, document type, posting date, customer, booking,
    service date, whether the item is cremation fee income, account-adjustment flag and net amount in cents."""
    out = []
    h = pd.read_csv(P(target, "ar_halbrook"), dtype=str, keep_default_na=False)
    for r in h.itertuples():
        out.append(("halbrook", CODE_OF_SITE[r.site], r.doc_type, r.posting_date, "H" + r.customer_no, r.booking_ref,
                    r.service_date, r.item_code in INCLUDED_H, r.item_code == "BRV-ADJ",
                    int(round(float(r.net_amount) * 100))))
    s = pd.read_excel(P(target, "ar_shoreline"), sheet_name="Receivables", dtype={"Case No.": str})
    for r in s.itertuples(index=False):
        loc, date, typ, no, cust, case, svc, prod, qty, rate, amt, tax = r
        out.append(("shoreline", CODE_OF_LOCATION[loc], "INV" if typ == "Invoice" else "CRN",
                    pd.Timestamp(date).date().isoformat(), "S" + cust, case if isinstance(case, str) else "",
                    pd.Timestamp(svc).date().isoformat() if pd.notna(svc) else "", prod in INCLUDED_S,
                    prod == "Credit - account", int(round(float(amt) * 100))))
    f = pd.read_csv(P(target, "ar_members"), dtype=str, keep_default_na=False)
    for r in f.itertuples():
        posted = None
        out.append((r.fund_code, r.fund_code, "INV" if r.record == "FEE" else "CRN", r.week_ending, r.fd_account,
                    r.booking_ref, r.service_date, r.fee_code in INCLUDED_F, r.fee_code == "ADJ",
                    int(round(float(r.amount_ex_tax) * 100))))
    cols = ["ledger", "code", "doc", "posted", "cust", "ref", "service", "fee", "adj", "cents"]
    return pd.DataFrame(out, columns=cols)


def _effects(cents, groups, kmax):
    groups = sorted(groups)
    eff = set()

    def rec(start, left, k, acc):
        if left == 0:
            tot = {}
            for a, sig in acc:
                tot[sig] = tot.get(sig, 0) + a
            eff.add(tuple(sorted(tot.items())))
            return
        if k == 0:
            return
        for gi in range(start, len(groups)):
            a, sig, cnt = groups[gi]
            if a > left:
                break
            if sum(1 for x in acc if x == (a, sig)) >= cnt:
                continue
            rec(gi, left - a, k - 1, acc + [(a, sig)])
    rec(0, cents, kmax, [])
    return eff


def levies(target, comm=None):
    """Each crematorium's 2026 levy: fee income for 2026 cremations at the rate their abatement status sets, net of
    credits allowed against those fees. A credit on a booking takes its booking's service date; a credit posted to a
    funeral director's account with no booking takes the service dates of the lines it reverses, the lines on that
    account whose amounts sum to it."""
    if comm is None:
        comm = register(target)[2]
    L = ledger_lines(target)
    abated = lambda code, d: comm.get(code) is not None and d > comm[code]
    base = {}
    matched = []
    inv = L[L.doc == "INV"]
    for r in inv.itertuples():
        if r.fee and r.service.startswith("2026"):
            k = (r.code, abated(r.code, dt.date.fromisoformat(r.service)))
            base[k] = base.get(k, 0) + r.cents
    crn = L[L.doc == "CRN"]
    by_cust = {}
    for r in inv.itertuples():
        by_cust.setdefault((r.ledger, r.cust), []).append(r)
    for r in crn.itertuples():
        if not r.adj:
            if r.fee and r.service.startswith("2026"):
                k = (r.code, abated(r.code, dt.date.fromisoformat(r.service)))
                base[k] = base.get(k, 0) + r.cents                       # a credit's cents are negative
            continue
        posted = dt.date.fromisoformat(r.posted) if r.ledger != r.code else None
        # members' returns carry the week ending, not the posting day: the window runs from the week's end
        end = dt.date.fromisoformat(r.posted)
        win = [x for x in by_cust[(r.ledger, r.cust)] if x.service and
               0 <= (end - dt.date.fromisoformat(x.service)).days <= 200]
        g = {}
        for x in win:
            d = dt.date.fromisoformat(x.service)
            sig = (x.code, d.year, abated(x.code, d), x.fee)
            g[(x.cents, sig)] = g.get((x.cents, sig), 0) + 1
        eff = _effects(-r.cents, [(a, s, c) for (a, s), c in g.items()], 4)
        assert len(eff) == 1, (r.ledger, r.cust, r.posted, r.cents, eff)
        (e,) = eff
        matched.append((r.ledger, r.cust, r.posted, -r.cents, e))
        for (code, y, ab, fee), cts in e:
            if fee and y == 2026:
                base[(code, ab)] = base.get((code, ab), 0) - cts
    out = {}
    for c in W.CREMATORIA:
        un, ab = base.get((c[0], False), 0), base.get((c[0], True), 0)
        out[c[0]] = {"income_unabated": un / 100, "income_abated": ab / 100,
                     "levy": int(np.floor((un * W.LEVY_UNABATED + ab * W.LEVY_ABATED) / 100 + 0.5))}
    return out, matched


def quarter(d):
    return (d.month - 1) // 3 + 1


def bypass_intervals(target):
    """Each abated crematorium's bypass intervals (UTC): a manual bypass from ON to OFF; a differential-pressure alarm
    that is not cleared within five minutes opens the bypass damper, which stays open until the plant is reset."""
    pl = pd.read_parquet(P(target, "plant"))
    ev = pl[pl.record == "EVENT"].sort_values(["fund_code", "logged_utc"])
    out = {}
    for code, g in ev.groupby("fund_code"):
        rows = list(g.itertuples())
        iv = []
        for i, r in enumerate(rows):
            if r.event == "MANUAL BYPASS ON":
                off = next(x for x in rows[i + 1:] if x.event == "MANUAL BYPASS OFF")
                iv.append((r.logged_utc, off.logged_utc, "manual"))
            if r.event == "ALARM" and r.detail.startswith("DP HIGH"):
                clr = next(x for x in rows[i + 1:] if x.event == "ALARM CLEARED" and x.detail == "DP HIGH")
                if (clr.logged_utc - r.logged_utc) > pd.Timedelta(minutes=5):
                    rst = next(x for x in rows[i + 1:] if x.event == "PLANT RESET")
                    iv.append((r.logged_utc + pd.Timedelta(minutes=5), rst.logged_utc, "alarm"))
        out[code] = iv
    return out, pl


def bypassed(target, comm=None):
    if comm is None:
        comm = register(target)[2]
    iv, pl = bypass_intervals(target)
    cy = pd.read_csv(P(target, "cycles"), dtype={"fund_code": str})
    cy = cy[cy.cycle_type == "CREMATION"]
    out = {}
    for code, ivs in sorted(iv.items()):
        c = cy[cy.fund_code == code]
        s_utc = pd.to_datetime(c.charge_et).dt.tz_localize(ET).dt.tz_convert("UTC")
        e_utc = pd.to_datetime(c.end_et).dt.tz_localize(ET).dt.tz_convert("UTC")
        hit = np.zeros(len(c), bool)
        for b0, b1, kind in ivs:
            hit |= ((s_utc <= b1) & (e_utc >= b0)).values
        q = pd.to_datetime(c.charge_et).dt.quarter.values
        cm = comm[code]
        first_q = 1 if cm.year < W.YEAR else quarter(cm)
        out[code] = {"Q%d" % k: int(hit[q == k].sum()) for k in range(first_q, 5)}
    return out


# ---------------------------------------------------------------- the certificate
def _chart_png(res, des, order):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 7.6, "svg.hashsalt": "task453"})
    names = [W.CREMATORIA[i][2] for i in range(len(W.CREMATORIA))]
    hg, ab = res["hg"] / 1000.0, res["ab"] / 1000.0
    idx = sorted(range(len(names)), key=lambda i: hg[i])
    fig, ax = plt.subplots(figsize=(6.6, 4.9), dpi=200)
    y = np.arange(len(idx))
    a = np.array([ab[i] for i in idx])
    u = np.array([hg[i] - ab[i] for i in idx])
    ax.barh(y, a, height=0.62, color="#2a78d6", label="Released in abated cremations")
    ax.barh(y, u, left=a + np.where(a > 0, 0.012, 0), height=0.62, color="#eb6834",
            label="Released in cremations not abated")
    ax.set_yticks(y)
    ax.set_yticklabels([names[i] + ("  (designated)" if i in des else "") for i in idx])
    for t, i in zip(ax.get_yticklabels(), idx):
        if i in des:
            t.set_fontweight("bold")
    for k, i in enumerate(idx):
        ax.text(hg[i] + 0.05, k, "%.1f" % hg[i], va="center", fontsize=6.8, color="#52514e")
    ax.set_xlabel("Mercury released by cremation in 2026, kilograms")
    ax.grid(axis="x", color="#e4e3df", linewidth=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="lower right", frameon=False, fontsize=7.0)
    ax.set_xlim(0, max(hg) * 1.12)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_certificate(res, path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs  # noqa: F401  (registers the fonts)
    ink, grey = colors.HexColor("#1c1e21"), colors.HexColor("#5d6168")
    body = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.4, leading=13.2, textColor=ink, spaceAfter=6)
    h1 = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#2e5e3a"),
                        spaceAfter=2)
    sub = ParagraphStyle("s", fontName="LiberationSans", fontSize=9, leading=12, textColor=grey, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10, leading=13, textColor=ink, spaceBefore=6,
                        spaceAfter=3)
    des, order, steps = res["des"], res["order"], res["steps"]
    names = lambda i: "%s (%s)" % (W.CREMATORIA[i][2], W.CREMATORIA[i][0])
    share = res["share"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Certificate for the 2026 scheme year", author=W.FUND,
                            subject="", creator="", producer="")

    def frame(canvas, d):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(grey)
        canvas.drawString(20 * mm, 10 * mm, "%s  |  Certificate under section 5 of the Crematoria Mercury Regulation, "
                          "2026 scheme year" % W.FUND)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    tot_kg = res["tot"] / 1000
    note = ParagraphStyle("n", fontName="LiberationSans", fontSize=7.6, leading=10, textColor=grey, spaceAfter=3)
    s = [Paragraph("2026 scheme year: abatement share not met, two crematoria designated", h1),
         Paragraph("Certificate CMF-C-2026 of the trustees of the %s, made at their meeting of %s under section 5 "
                   "of the Crematoria Mercury Regulation. To the Minister and the operators of member crematoria." %
                   (W.FUND, W.MEETING.strftime("%-d %B %Y")), sub),
         Paragraph("1. The trustees certify that about %d per cent of the mercury released by cremation in the "
                   "province in 2026 was released in abated cremations. That is less than the 55 per cent section 3 "
                   "requires, so the 2026 scheme year did not meet the Regulation." % int(round(share)), body),
         Paragraph("2. Under section 4 the trustees designate %s and %s. Their operators must connect every "
                   "cremator to a commissioned mercury abatement plant by 31 December 2028. Counting the mercury "
                   "released at %s as abated, the share would have been about %d per cent, still short; counting "
                   "%s as well, about %d per cent. No other crematorium is designated." %
                   (names(des[0]), names(des[1]), W.CREMATORIA[des[0]][2], int(round(steps[1])),
                    W.CREMATORIA[des[1]][2], int(round(steps[2]))), body),
         Paragraph("Basis of the estimate", h2),
         Paragraph("The %s cremations performed in the province in 2026 are those on the Vital Statistics Agency's "
                   "cremation permits with a 2026 date of cremation<super>1</super>; a cremation is abated where its "
                   "crematorium's abatement plant was commissioned before that date, which makes Wexley Regional and "
                   "Hollinsbrook abated from 4 July and 15 September. The mercury of each person cremated is 0.55 grams "
                   "for each tooth restored with amalgam, nil under 18<super>2</super>. The teeth restored with "
                   "amalgam are read from the %s by birth cohort: a person who died at a given age in 2026 was ten "
                   "years younger at the 2016 survey and twenty at the 2006 survey, so each person takes the 2016 mean "
                   "of their sex and cohort, carried to 2026 by that cohort's own change between the 2006 and 2016 "
                   "surveys. The survey's age profile, applied at age at death, would describe the cohorts born ten "
                   "years earlier. In all, %.1f kilograms of mercury were released by cremation in 2026." %
                   ("{:,}".format(int(res["n"].sum())), W.SURVEY, tot_kg), body)]
    png = _chart_png(res, des, order)
    img = Image(io.BytesIO(png), width=158 * mm, height=158 * mm * 4.9 / 6.6)
    s += [Spacer(1, 2), Paragraph("Mercury released by cremation at each crematorium, 2026", h2), img,
          Paragraph("Source: Vital Statistics Agency cremation permits, extract of 8 February 2027; the Fund's member "
                    "register as checked 15 January 2027; %s report tables, 2006 and 2016." % W.SURVEY, note),
          PageBreak()]
    data = [["Crematorium", "Cremations", "Abated cremations", "Mercury, kg", "of which abated"]]
    for i in sorted(range(len(W.CREMATORIA)), key=lambda i: W.CREMATORIA[i][2]):
        data.append([W.CREMATORIA[i][2], "{:,}".format(int(res["n"][i])), "{:,}".format(int(res["n_ab"][i])),
                     "%.1f" % (res["hg"][i] / 1000), "%.1f" % (res["ab"][i] / 1000)])
    data.append(["All crematoria", "{:,}".format(int(res["n"].sum())), "{:,}".format(int(res["n_ab"].sum())),
                 "%.1f" % (res["tot"] / 1000), "%.1f" % (res["ab"].sum() / 1000)])
    t = Table(data, colWidths=[64 * mm, 22 * mm, 28 * mm, 22 * mm, 24 * mm], repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "LiberationSans", 8.0),
                           ("FONT", (0, 0), (-1, 0), "LiberationSans-Bold", 8.0),
                           ("FONT", (0, -1), (-1, -1), "LiberationSans-Bold", 8.0),
                           ("LINEABOVE", (0, 0), (-1, 0), 0.6, ink), ("LINEBELOW", (0, 0), (-1, 0), 0.6, ink),
                           ("LINEABOVE", (0, -1), (-1, -1), 0.4, ink),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, ink), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("ALIGN", (1, 0), (-1, 0), "RIGHT"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    s += [Paragraph("2026 cremations and mercury by crematorium", h2), t,
          Paragraph("Mercury in kilograms to one decimal place; totals from the unrounded figures.", note),
          Spacer(1, 8),
          Paragraph("<super>1</super> Wexley Regional Crematorium's permits for cremations before 2 March 2026 carry "
                    "the agency's former facility number for it, F1984, as the register's facility sheet records.",
                    note),
          Paragraph("<super>2</super> Section 2(2) of the Regulation. The survey examines adults aged 18 and over; "
                    "ages at death under one year are recorded on the permits in months.", note),
          Spacer(1, 18),
          Paragraph("%s, Chair of the trustees&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s, Technical Secretary" %
                    (W.PEOPLE["chair"], W.PEOPLE["secretary"]), body),
          Paragraph("%s" % W.MEETING.strftime("%-d %B %Y"), body)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_book(lev, byp, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Levy 2026"
    ws.append(["Fund code", "Crematorium", "Operator", "Fee income, cremations not abated ($)",
               "Fee income, abated cremations ($)", "Levy ($)"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[1].height = 30
    for c in sorted(W.CREMATORIA, key=lambda x: x[2]):
        v = lev[c[0]]
        ws.append([c[0], c[2], c[3], v["income_unabated"], v["income_abated"], v["levy"]])
    n = len(W.CREMATORIA) + 1
    ws.append([None, "All crematoria", None, round(sum(v["income_unabated"] for v in lev.values()), 2),
               round(sum(v["income_abated"] for v in lev.values()), 2), sum(v["levy"] for v in lev.values())])
    for cell in ws[n + 1]:
        cell.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2):
        for cell in row[3:5]:
            cell.number_format = "#,##0.00"
        row[5].number_format = "#,##0"
    for col, wdt in zip("ABCDEF", [10, 34, 34, 18, 18, 11]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "C2"
    ws.print_title_rows = "1:1"
    ws2 = wb.create_sheet("Bypassed cremations 2026")
    ws2.append(["Fund code", "Crematorium", "Quarter", "Cremations under way while the plant was bypassed"])
    for c in ws2[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws2.row_dimensions[1].height = 30
    for c in sorted(W.CREMATORIA, key=lambda x: x[2]):
        if c[0] not in byp:
            continue
        for q, v in byp[c[0]].items():
            ws2.append([c[0], c[2], "2026 %s" % q, v])
    for col, wdt in zip("ABCD", [10, 34, 10, 22]):
        ws2.column_dimensions[col].width = wdt
    ws2.freeze_panes = "A2"
    ws2.print_title_rows = "1:1"
    ws3 = wb.create_sheet("Notes")
    notes = [
        "Levy 2026",
        "Scheme rules 2.1 to 2.3: 4.5 per cent of cremation fee income from 2026 cremations not abated and 1.5 per cent "
        "from abated ones, net of credits allowed against those fees, excluding sales tax, rounded once per crematorium.",
        "Fee income is taken by the cremation's service date. Urns, keepsakes and the medical referee's fee are left out.",
        "Wexley Regional and Hollinsbrook are split at commissioning: cremations from 4 July and 15 September are abated.",
        "A credit on a booking takes that booking's service date. A credit posted to a funeral director's account without "
        "a booking takes the service dates of the lines on that account whose amounts it equals.",
        "Ledgers: City of Halbrook and Shoreline Memorial Group extracts and the independent crematoria's fee returns, "
        "postings to 19 February 2027.",
        "",
        "Bypassed cremations 2026",
        "A plant is bypassed from a manual bypass to its end, and from a DP HIGH alarm not cleared within five minutes to "
        "the next plant reset (the inlet temperature falls to ambient while cremators fire).",
        "A cremation counts once, in the quarter of its charge (Eastern time), if it was under way at any time while the "
        "plant was bypassed. Quarters are those in which the plant was in service.",
    ]
    for line in notes:
        ws3.append([line or None])
    ws3.column_dimensions["A"].width = 120
    for r in (1, 8):
        ws3.cell(row=r, column=1).font = Font(bold=True)
    for row in ws3.iter_rows():
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def main(target, golden_dir, figures_path):
    import postprocess as PP
    os.makedirs(golden_dir, exist_ok=True)
    tab = S.tables(W.SEED)
    res = call(target, tab)
    comm = register(target)[2]
    lev, matched = levies(target, comm)
    byp = bypassed(target, comm)
    cert = os.path.join(golden_dir, W.GOLDEN["cert"])
    book = os.path.join(golden_dir, W.GOLDEN["book"])
    write_certificate(res, cert)
    write_book(lev, byp, book)
    PP.normalize_pdf(cert, b"D:20270224163012-05'00'", b"D:20270224171905-05'00'")
    PP.normalize_ooxml(book, W.PEOPLE["secretary"], W.PEOPLE["secretary"], "2027-02-18T14:02:00Z",
                       "2027-02-24T21:47:31Z", excel=True, company=W.FUND)
    stamp = dt.datetime(2027, 2, 24, 17, 20, tzinfo=dt.timezone(dt.timedelta(hours=-5))).timestamp()
    for f in os.listdir(golden_dir):
        os.utime(os.path.join(golden_dir, f), (stamp, stamp))
    names = lambda i: W.CREMATORIA[i][2]
    fig = {
        "call": {"met": bool(res["share"] >= W.SHARE_REQUIRED), "designated": [names(i) for i in res["des"]],
                 "designated_codes": [W.CREMATORIA[i][0] for i in res["des"]],
                 "share_pct_whole": int(round(res["share"])), "share_pct": round(float(res["share"]), 2),
                 "steps_pct": [round(float(x), 2) for x in res["steps"]],
                 "order": [names(i) for i in res["order"]],
                 "cremations_2026": int(res["n"].sum()), "mercury_kg_total": round(float(res["tot"]) / 1000, 2)},
        "mercury_kg": {W.CREMATORIA[i][0]: {"total": round(float(res["hg"][i]) / 1000, 3),
                                             "abated": round(float(res["ab"][i]) / 1000, 3),
                                             "cremations": int(res["n"][i])} for i in range(len(W.CREMATORIA))},
        "levy": {k: v["levy"] for k, v in lev.items()},
        "fee_income": {k: [round(v["income_unabated"], 2), round(v["income_abated"], 2)] for k, v in lev.items()},
        "bypass": byp,
        "account_credits_matched": len(matched),
        "filed": {"threshold_pct": W.SHARE_REQUIRED, "factor_g_per_tooth": W.HG_PER_TOOTH_G,
                  "levy_rates_pct": [round(100 * W.LEVY_UNABATED, 1), round(100 * W.LEVY_ABATED, 1)]},
        "share_with_one_designated_pct": {names(i): round(float(100 * (res["ab"].sum() + res["hg"][i]) / res["tot"]), 2)
                                          for i in res["des"]},
        "routes": {},
    }
    idx = {c[0]: i for i, c in enumerate(W.CREMATORIA)}
    cre = [(idx[c], a, s_, ab) for c, a, s_, ab, d in cremations_2026(target)]
    for key, form in (("age_profile_2016_at_death", "age2016"), ("count_of_cremations", "count"),
                      ("cohort_2016_mean_unaged", "cohort_noage")):
        d = M.designate(cre, tab, form)
        fig["routes"][key] = {"share_pct": round(float(d["share"]), 2), "designated": [names(i) for i in d["des"]]}
    with open(figures_path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return {"res": res, "lev": lev, "byp": byp, "matched": matched, "fig": fig}
