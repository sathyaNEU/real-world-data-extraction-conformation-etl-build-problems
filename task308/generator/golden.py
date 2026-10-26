"""The two deliverables: the board paper (cat_layer_placement_2027.pdf) and its workbook (cat_layer_workbook_2027.xlsx).
Every figure comes from solve.py on the cut pack and figures.json; nothing is typed."""
import io
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer

import docs as D
import params as P
import postprocess as PP

PDF = "cat_layer_placement_2027.pdf"
XLSX = "cat_layer_workbook_2027.xlsx"
PAPER_DATE = "2026-11-27"
REF = "B/26/41"
ORDER = ["Pennine", "Severn Vale", "Coastal North", "Fenland"]
INK, MUTED, ACCENT, GREY = "#1F2A36", "#5B6670", "#1D6E8C", "#8E979F"


def m1(x):
    return "%.1f" % (round(x + 1e-9, 1) + 0.0)


def m2(x):
    return "%.2f" % (round(x + 1e-9, 2) + 0.0)


def gbp(x):
    return "{:,.2f}".format(round(x + 1e-9, 2))


def facts(target, mc, fig):
    """the figures both deliverables print, computed once"""
    import solve as S
    O = mc["O"].copy()
    O["rec"] = (O.G - P.RETENTION / 1e6).clip(lower=0).clip(upper=P.LIMIT / 1e6)
    O["rec_idx"] = (O.L_loss - P.RETENTION / 1e6).clip(lower=0).clip(upper=P.LIMIT / 1e6)
    c, ex, I, I27, PLAN = S.load(target)
    pol = ex.groupby(["year", "region"]).policies_in_force_mid_year.sum()
    A = S.ask_a(target)
    Bq = S.ask_b(target)
    Dd = pd.read_csv(os.path.join(target, P.FILES["direct"]))
    direct = {r: float(Dd[Dd.region == r].buildings_sums_insured_gbp.sum()) / 1e6 for r in P.REGIONS}
    panel = c[c.repair_contractor != ""].groupby([c.date_of_loss.dt.year, "region"])["repair_contractor"].nunique()
    fz = O[(O.region == "Pennine") & (O.peril == "freeze") & (O.year < 2021)].sort_values("start")
    return dict(O=O, pol=pol, A=A, B=Bq, direct=direct, panel=panel, fz=fz, I27=I27)


def chart(mc, fig):
    """each book's value: recorded costs carried by the index alone (open) and at the 2027 scale (filled)"""
    gold = {r: mc["gold"][r]["value"] for r in P.REGIONS}
    dflt = {r: mc["default"][r]["value"] for r in P.REGIONS}
    order = sorted(P.REGIONS, key=lambda r: gold[r])
    fg, ax = plt.subplots(figsize=(6.6, 2.7), dpi=200)
    for i, r in enumerate(order):
        col = ACCENT if r == fig["call"]["region"] else GREY
        ax.plot([dflt[r], gold[r]], [i, i], color=col, lw=2, solid_capstyle="round", zorder=1)
        ax.scatter([dflt[r]], [i], s=46, facecolor="white", edgecolor=col, linewidth=1.6, zorder=2)
        ax.scatter([gold[r]], [i], s=58, color=col, edgecolor="white", linewidth=1.2, zorder=3)
        ax.annotate("GBP %s m" % m1(gold[r]), (max(gold[r], dflt[r]), i), xytext=(9, -3), textcoords="offset points",
                    fontsize=8, color=INK, fontweight="bold" if r == fig["call"]["region"] else "normal")
    ax.axvline(0, color=INK, lw=0.9, zorder=0)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=8.5, color=INK)
    ax.set_xlim(-1.0, 0.45)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xticks([-1.0, -0.75, -0.5, -0.25, 0.0, 0.25])
    ax.set_xticklabels(["-1.00", "-0.75", "-0.50", "-0.25", "0", "0.25"], fontsize=7.5, color=MUTED)
    ax.set_xlabel("Value of the layer, GBP million a year", fontsize=7.8, color=MUTED)
    ax.grid(axis="x", color="#E3E6E8", lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#B5BCC2")
    ax.tick_params(axis="y", length=0)
    ax.scatter([], [], s=46, facecolor="white", edgecolor=GREY, linewidth=1.6, label="Recorded costs carried by the index")
    ax.scatter([], [], s=58, color=GREY, label="Repairs priced at the 2027 scale")
    ax.legend(loc="lower right", fontsize=7, frameon=False)
    fg.tight_layout()
    buf = io.BytesIO()
    fg.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fg)
    buf.seek(0)
    return buf


def paper(path, target, mc, fig, f):
    body, h1, h2, small = D._styles()
    gold = mc["gold"]
    call = fig["call"]["region"]
    fz = f["fz"]
    s = [Paragraph("%s | Board of Directors, 9 December 2026 | Paper %s | For decision" % (P.ORG, REF), small),
         Paragraph("Place the 2027 catastrophe layer on the %s book, where it is worth GBP %s million a year"
                   % (call, m1(gold[call]["value"])), h1),
         Paragraph("From Donna Phillips, Head of Reinsurance. Reviewed by Anne Shah, Chief Actuary. 27 November 2026.",
                   small), Spacer(1, 5),
         Paragraph("1. Recommendation", h2),
         Paragraph("The quotations %s gave us on 18 November for the 2027 regional catastrophe layer, GBP 15 million "
                   "excess of GBP 10 million each loss occurrence with one reinstatement at 100 per cent, are firm until "
                   "15 December, and the order has to be signed with the lead reinsurer before then for cover from "
                   "1 January. The 2027 plan provides for one regional layer. Valued under policy RC-07, the layer is "
                   "worth GBP %s million a year on %s and less on each of the other three books. We recommend that the "
                   "Board place it on %s, led by %s."
                   % (P.BROKER, m1(gold[call]["value"]), call, call, P.LEAD[call]), body)]
    rows = [["Region", "Expected recoveries", "Expected reinstatement premium", "Quoted premium", "Value"]]
    for r in sorted(P.REGIONS, key=lambda q: -gold[q]["value"]):
        g = gold[r]
        rows.append([r, m2(g["recoveries"]), m2(g["rip"]), "%.3f" % (P.PREMIUM[r] / 1e6), m1(g["value"])])
    s += [D._table(rows, [34, 34, 46, 30, 22], align_right=(1, 2, 3, 4)),
          Paragraph("GBP million a year. Sixteen-year averages, 2010 to 2025, at the 2027 book and 2027 repair costs "
                    "(RC-07); premiums as quoted on 18 November 2026.", small), Spacer(1, 6),
          Image(chart(mc, fig), width=166 * mm, height=68 * mm),
          Paragraph("Figure 1. The layer's value on each book with recorded repair costs carried forward by the rebuild "
                    "cost index (open) and with repairs priced at the claims each panel firm would carry in 2027 "
                    "(filled).", small)]
    O = f["O"]
    pan = f["panel"]
    s += [Paragraph("2. Why %s" % call, h2),
          Paragraph("Pennine's book doubled on 1 January 2021, when the %s policies moved onto our platforms in eight "
                    "of its districts. Its repair panel did not grow with it: %d firms in 2010 and %d in 2025. A "
                    "catastrophe's repairs cost more the more claims each panel firm has to take on at once, as firms "
                    "subcontract and materials run short. Across the %d loss occurrences of %d claims or more since 2010, "
                    "the cost of a claim at 2027 prices rises by about %s per cent for each claim a firm above %s."
                    % (P.TRANSFEROR, pan[(2010, "Pennine")], pan[(2025, "Pennine")],
                       fig["steps"]["fit_occurrences"], fig["steps"]["fit_min_claims"],
                       fig["steps"]["fit_slope_pct"], fig["steps"]["fit_threshold"]), body),
          Paragraph("Pennine's four freezes before the transfer put %s to %s claims on each of its firms. Struck on the "
                    "2027 book, the same freezes would put %s to %s claims on each of today's firms, and each would cost "
                    "more than GBP 25 million: every one exhausts the layer, and Pennine recovers GBP %s million a year "
                    "against a premium of GBP %s million and an expected reinstatement premium of GBP %s million. "
                    "Carried forward by the rebuild cost index alone, the same freezes recover %s to %s each and the "
                    "layer would be worth GBP %s million on Pennine, behind Severn Vale. On the other three books the "
                    "panel grew with the book, and the 2027 scale moves no value by more than GBP %s million."
                    % (m1(fz.u_all.min()), m1(fz.u_all.max()), m1(fz.u27_all.min()), m1(fz.u27_all.max()),
                       m2(gold["Pennine"]["recoveries"]), m2(P.PREMIUM["Pennine"] / 1e6), m2(gold["Pennine"]["rip"]),
                       m1(fz.rec_idx.min()), m1(fz.rec_idx.max()), m1(mc["default"]["Pennine"]["value"]),
                       "%.2f" % (math.ceil(100 * max(abs(gold[r]["value"] - mc["default"][r]["value"])
                                                    for r in P.REGIONS if r != call)) / 100)), body)]
    rows = [["Freeze", "Claims", "Claims a firm, then", "Claims a firm, 2027", "Loss, index alone",
             "Loss, 2027 scale", "Recovery"]]
    for r in fz.itertuples():
        rows.append([pd.Timestamp(r.start).strftime("%-d %B %Y"), "{:,}".format(r.n), m1(r.u_all), m1(r.u27_all),
                     m1(r.L_loss), m1(r.G), m1(r.rec)])
    s += [D._table(rows, [30, 16, 26, 26, 24, 24, 20], align_right=(1, 2, 3, 4, 5, 6)),
          Paragraph("Losses and recoveries in GBP million at the 2027 book. Claims from the claims extract at 31 October "
                    "2026; panel firms counted from the firms named on the claims each year; 2027 at the plan's policies "
                    "and the 2025 panel.", small)]
    s += [Paragraph("3. How the value is built", h2),
          Paragraph("As RC-07 sets out. Each region's windstorm, flood and freeze claims since 2010 are grouped into loss "
                    "occurrences under the event definitions: %d hours for a windstorm and %d for a flood or a freeze, "
                    "one period from each catastrophe's first loss. Each claim is brought to its district's 2027 "
                    "policies and to 2027 repair costs: the rebuild cost index carries it from its month of loss to the "
                    "plan's 2027 level of %s, and the cost of a claim against claims per firm carries each catastrophe "
                    "from its own claims per firm to its 2027 claims per firm. The layer's terms apply to each "
                    "occurrence, each year is capped at GBP %d million, and the sixteen-year average is taken less the "
                    "quoted premium and the expected reinstatement premium."
                    % (P.HOURS["windstorm"], P.HOURS["flood"], fig["steps"]["index_2027"], P.ANNUAL // 1000000), body)]
    rows = [["Region", "2023", "2024", "2025"]]
    for r in ORDER:
        rows.append([r] + [gbp(f["A"]["%s|%d" % (r, y)]) for y in (2023, 2024, 2025)])
    rows2 = [["Region", "Direct book", "Lowther and Pike", "Total"]]
    for r in ORDER:
        rows2.append([r, "{:,.1f}".format(f["direct"][r]), "{:,.1f}".format(f["B"][r]["si_m"] - f["direct"][r]),
                      "{:,.1f}".format(round(f["B"][r]["si_m"] + 1e-9, 1))])
    s += [KeepTogether([Paragraph("4. For the reinsurers' submission", h2),
                        Paragraph("The brokers have asked for each book's recent claims experience and its buildings "
                                  "exposure at the last year end.", body),
                        Paragraph("Incurred per policy in force on escape of water, accidental damage, theft, fire and "
                                  "subsidence claims taken together, GBP", small),
                        D._table(rows, [40, 30, 30, 30], align_right=(1, 2, 3)),
                        Paragraph("Incurred at 31 October 2026, paid plus outstanding, by year of loss (note 1); "
                                  "policies in force at mid-year from the exposure extract.", small), Spacer(1, 5)]),
          KeepTogether([Paragraph("Buildings sums insured on 31 December 2025, GBP million", small),
                        D._table(rows2, [40, 30, 34, 30], align_right=(1, 2, 3)),
                        Paragraph("The direct book from the platform's year-end table; Lowther and Pike homes from %s's "
                                  "bordereaux, October 2025 to February 2026 (note 2). Totals from unrounded figures."
                                  % P.COVERHOLDER, small)]),
          Spacer(1, 6),
          Paragraph("Note 1. Claims the Major Loss Unit holds are at the unit's figures: a reopened case is added to its "
                    "claim, and a claim sits in the year of the date of loss the unit's adjusters set. A claim the unit "
                    "sent back to the home claims team is at the platform's figure.", small),
          Paragraph("Note 2. A Lowther and Pike term cancelled for a missed payment and then reinstated is in force; a "
                    "term still listed in the month its cancellation took effect is out from that day; a rewrite onto "
                    "fuller cover counts at its new sum insured; cancellations and endorsements count from their "
                    "effective dates.", small)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="2027 catastrophe layer: placement", author="Donna Phillips",
                            creator=P.ORG, subject="Board paper %s" % REF, invariant=1)
    foot = D._footer("%s | Board paper %s | 2027 catastrophe layer" % (P.ORG, REF))
    doc.build(s, onFirstPage=foot, onLaterPages=foot)
    PP.scrub(path, P.ORG, PAPER_DATE)


def _head(ws, row, n):
    D._xl_head(ws, row, n)


def _widths(ws, widths):
    for k, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(k)].width = w


def workbook(path, target, mc, fig, f):
    gold = mc["gold"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(["2027 catastrophe layer, GBP 15m xs 10m with one reinstatement: value by region under RC-07"])
    ws["A1"].font = Font(bold=True, size=12, color="1F3A5F")
    ws.append(["GBP million a year. Recommended: %s." % fig["call"]["region"]])
    ws.append([])
    ws.append(["Region", "Expected recoveries", "Expected reinstatement premium", "Quoted premium", "Value", "Rank"])
    _head(ws, 4, 6)
    for k, r in enumerate(sorted(P.REGIONS, key=lambda q: -gold[q]["value"]), start=1):
        g = gold[r]
        ws.append([r, round(g["recoveries"], 2), round(g["rip"], 2), P.PREMIUM[r] / 1e6, round(g["value"] + 1e-9, 1), k])
        n = ws.max_row
        for c, fmt in (("B", "0.00"), ("C", "0.00"), ("D", "0.000"), ("E", "0.0")):
            ws["%s%d" % (c, n)].number_format = fmt
    ws.append([])
    ws.append(["Sixteen-year averages, 2010 to 2025, at the 2027 book (the plan's policies) and 2027 repair costs. Value is "
               "expected recoveries less the quoted premium and the expected reinstatement premium, rounded once."])
    ws.freeze_panes = "A5"
    _widths(ws, [16, 20, 30, 16, 10, 8])

    wo = wb.create_sheet("Occurrences")
    wo.append(["Region", "Peril", "First day", "Claims", "Claims a firm, then", "Claims a firm, 2027",
               "Loss at the index alone", "Loss at the 2027 scale", "Recovery before the annual cap"])
    _head(wo, 1, 9)
    O = f["O"].sort_values(["region", "start", "peril"])
    for r in O.itertuples():
        wo.append([r.region, r.peril.capitalize(), pd.Timestamp(r.start).to_pydatetime(), int(r.n), round(r.u_all, 2),
                   round(r.u27_all, 2), round(r.L_loss, 3), round(r.G, 3), round(r.rec, 3)])
        n = wo.max_row
        wo["C%d" % n].number_format = "dd/mm/yyyy"
        wo["D%d" % n].number_format = "#,##0"
        for c in ("E", "F"):
            wo["%s%d" % (c, n)].number_format = "0.0"
        for c in ("G", "H", "I"):
            wo["%s%d" % (c, n)].number_format = "0.000"
    wo.freeze_panes = "A2"
    wo.auto_filter.ref = "A1:I%d" % wo.max_row
    _widths(wo, [15, 12, 12, 9, 12, 12, 14, 14, 16])

    wf = wb.create_sheet("Repair cost")
    wf.append(["Cost of a claim against claims per panel firm: loss occurrences of %d claims or more since 2010"
               % fig["steps"]["fit_min_claims"]])
    wf["A1"].font = Font(bold=True, size=11, color="1F3A5F")
    wf.append(["Log cost per claim at 2027 prices, weighted by claims, a level for each peril; above %s claims a firm "
               "the cost rises %s per cent a claim a firm." % (fig["steps"]["fit_threshold"], fig["steps"]["fit_slope_pct"])])
    wf.append([])
    wf.append(["Region", "Peril", "First day", "Claims", "Claims a firm", "Cost per claim, 2027 prices",
               "Multiplier to the 2027 scale"])
    _head(wf, 4, 7)
    E = O[O.n >= 150].sort_values("u_all")
    for r in E.itertuples():
        wf.append([r.region, r.peril.capitalize(), pd.Timestamp(r.start).to_pydatetime(), int(r.n), round(r.u_all, 2),
                   round(r.sev_loss, 2), round(r.f, 4)])
        n = wf.max_row
        wf["C%d" % n].number_format = "dd/mm/yyyy"
        wf["D%d" % n].number_format = "#,##0"
        wf["E%d" % n].number_format = "0.0"
        wf["F%d" % n].number_format = "#,##0"
        wf["G%d" % n].number_format = "0.000"
    wf.freeze_panes = "A5"
    _widths(wf, [15, 12, 12, 9, 13, 18, 18])

    wa = wb.create_sheet("Incurred per policy")
    wa.append(["Region", "Year of loss", "Incurred at 31 October 2026", "Policies in force, mid-year", "Incurred per policy"])
    _head(wa, 1, 5)
    for r in ORDER:
        for y in (2023, 2024, 2025):
            v = f["A"]["%s|%d" % (r, y)]
            p = int(f["pol"][(y, r)])
            wa.append([r, y, round(v * p, 2), p, round(v + 1e-9, 2)])
            n = wa.max_row
            wa["C%d" % n].number_format = "#,##0"
            wa["D%d" % n].number_format = "#,##0"
            wa["E%d" % n].number_format = "#,##0.00"
    wa.append([])
    wa.append(["Escape of water, accidental damage, theft, fire and subsidence claims taken together, GBP. Claims the "
               "Major Loss Unit holds are at the unit's figures, a reopened case added to its claim, in the year of the "
               "date of loss the unit's adjusters set; a claim sent back to the home claims team is at the platform's "
               "figure."])
    wa.freeze_panes = "A2"
    _widths(wa, [15, 11, 24, 22, 18])

    wbk = wb.create_sheet("Sums insured")
    wbk.append(["Region", "Direct book", "Lowther and Pike", "Total"])
    _head(wbk, 1, 4)
    for r in ORDER:
        tot = f["B"][r]["si_m"]
        wbk.append([r, round(f["direct"][r], 1), round(tot - f["direct"][r], 1), round(tot + 1e-9, 1)])
        n = wbk.max_row
        for c in ("B", "C", "D"):
            wbk["%s%d" % (c, n)].number_format = "#,##0.0"
    wbk.append([])
    wbk.append(["Buildings sums insured on 31 December 2025, GBP million; totals from unrounded figures. Lowther and Pike "
                "homes from %s's bordereaux, October 2025 to February 2026: a term cancelled for a missed payment and "
                "then reinstated is in force; a term still listed in the month its cancellation took effect is out "
                "from that day; a rewrite onto fuller cover counts at its new sum insured; cancellations and "
                "endorsements count from their effective dates." % P.COVERHOLDER])
    wbk.freeze_panes = "A2"
    _widths(wbk, [15, 14, 16, 14])

    wn = wb.create_sheet("Notes")
    for line in [["Notes"],
                 ["Basis", "Board policy RC-07 (catastrophe_layer_valuation_basis.pdf); occurrences under the catastrophe "
                           "event definitions, version 3."],
                 ["Claims", "Home claims extract at 31 October 2026, incurred as paid plus outstanding."],
                 ["Book", "2027 policies from the business plan, spread across districts by the mid-2025 mix."],
                 ["Costs", "Rebuild cost index for the month of loss, to the plan's 2027 level of %s; repairs at the "
                           "2027 claims per panel firm on the 2025 panel." % fig["steps"]["index_2027"]],
                 ["Layer", "GBP 15m xs 10m each loss occurrence, one reinstatement at 100 per cent pro rata as to "
                           "amount, GBP %d million a year at most." % (P.ANNUAL // 1000000)],
                 ["Prepared", "Donna Phillips, Head of Reinsurance, 27 November 2026, for the Board of 9 December 2026."]]:
        wn.append(line)
    wn["A1"].font = Font(bold=True, size=11, color="1F3A5F")
    for row in wn.iter_rows(min_row=2):
        row[0].font = Font(bold=True)
        if len(row) > 1:
            row[1].alignment = Alignment(wrap_text=True, vertical="top")
    _widths(wn, [12, 100])
    for w in wb.worksheets:
        w.sheet_view.showGridLines = w.title in ("Occurrences", "Repair cost")
    wb.save(path)
    PP.scrub(path, P.ORG, PAPER_DATE)
    PP.finish_office(path, "2026-11-24T09:12:00Z", "2026-11-27T16:41:00Z", P.ORG, person="Donna Phillips")
