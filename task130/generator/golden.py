#!/usr/bin/env python3
"""Golden deliverables for task130, the 2027 designation of census sections.

Reads only the shipped files under <task>/target and writes the three files the prompt names into
<task>/golden: designation_brief_2027.pdf, designation_annex_2027.csv and section_bridge_2027.png.
Prints the figures the critical components carry.

    python3 -I golden.py [/path/to/task130]
"""
import csv
import datetime as dt
import os
import subprocess
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import verify as V  # noqa: E402  the pack's parsing and conformance, which read target/ only

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

TASK = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE))
OUT = os.path.join(TASK, "golden")

QUARTER, LODGED_BY = "2026T2", "2026-08-31"        # the 30 June returns, as the bulletin takes them
SNAPSHOT, EXTRACT_CUT, PROGRAMME_DAY = "2026-06-30", "2026-09-30", "2027-01-01"
LINE = Decimal(25)                                  # Article 4 of the order
BRIEF_DATE = "30 October 2026"
PDF_MADE = b"D:20261030103412+01'00'"
INVARIANT_PDF_DATE = b"D:20000101000000+00'00'"
MONTHS = ["July", "August", "September", "October", "November", "December"]


def place(P):
    """Municipality and district per section, from the 2026 annex."""
    return {str(r["Secció censal"]): (r["Municipi"], r["Districte"]) for _, r in P.annex.iterrows()}


def compute():
    P = V.Pack(TASK)
    W = P.watch
    june = V.picture(P, QUARTER, LODGED_BY, 2)
    june_n = V.tally(june, P, W)
    # control: the conformed 30 June picture is the bulletin's, section for section
    bull = V.bulletin_figures(P.bull_text, W)
    assert all(bull[s] == (P.N[s], june_n[s]) for s in W), "30 June picture does not tie to the bulletin"

    tk = V.commitments(P, 120)
    rolled = V.roll(P, june, SNAPSHOT, EXTRACT_CUT, PROGRAMME_DAY, "R5", tk)
    # holders inscribed after 30 June with no return yet: what the deeds show they hold (Article 2.1, 2.4)
    extra, late = V.late_registrants(P, EXTRACT_CUT)
    assert not set(extra) & set(rolled), "a registrant dwelling already on the roll"
    own = dict(rolled, **extra)
    lh = V.per_section(P, own, W)
    reg_sec = {}
    for k, h in extra.items():
        reg_sec.setdefault(h, {}).setdefault(P.sec[k], 0)
        reg_sec[h][P.sec[k]] += 1
    reg_info = sorted(((P.name[h], P.tit.loc[P.tit["nif"] == h, "data_inscripcio"].iloc[0], v) for h, v in reg_sec.items()),
                      key=lambda x: -sum(x[2].values()))
    share = {s: V.pct(lh[s], P.N[s]) for s in W}
    designated = sorted(s for s in W if share[s] >= LINE)
    under = sorted(s for s in W if share[s] < LINE)
    near_in = min(designated, key=lambda s: share[s])
    near_out = max(under, key=lambda s: share[s])

    # last year's build: every notified sale carried to its agreed buyer and date
    last_year = V.chosen(P, V.per_section(P, V.roll(P, june, SNAPSHOT, EXTRACT_CUT, PROGRAMME_DAY, "R3"), W), W)

    group = V.biggest(P, own, W, V.members(P, PROGRAMME_DAY))
    occ = V.occupied(P)
    empty = {s: sum(1 for k in own if P.sec.get(k) == s and k not in occ) for s in W}

    bridges = {}
    for s in (near_out, near_in):
        prev, steps = june_n[s], []
        for m in range(7, 13):
            end = dt.date(2026, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(2026, 12, 31)
            cut = min(end.isoformat(), EXTRACT_CUT)
            c = V.per_section(P, V.roll(P, june, SNAPSHOT, cut, end.isoformat(), "R5", tk), W)[s]
            steps.append(c - prev)
            prev = c
        assert not any(P.sec[k] == s for k in extra), f"registrant dwellings in bridge section {s}"
        assert june_n[s] + sum(steps) == lh[s], f"bridge for {s} does not close"
        bridges[s] = (june_n[s], steps, lh[s])

    settled = []
    for ref, (c, _, _) in tk.items():
        later = P.deeds[(P.deeds["referencia_cadastral"] == ref) & (P.deeds["data_atorgament"] > c.isoformat())]
        if len(later):
            settled.append((dt.date.fromisoformat(later.iloc[0]["data_atorgament"]) - c).days)
    assert settled and set(settled) == {120}, "settled first-offer purchases off the 120-day interval"
    early = 0
    for ref, (c, _, planned) in tk.items():
        later = P.deeds[(P.deeds["referencia_cadastral"] == ref) & (P.deeds["data_atorgament"] > c.isoformat())]
        if len(later) and planned > dt.date.fromisoformat(later.iloc[0]["data_atorgament"]):
            early += 1
    assert early == 4, early

    return dict(P=P, W=W, N=P.N, place=place(P), june=june_n, lh=lh, share=share, designated=designated,
                near_in=near_in, near_out=near_out, last_year=last_year, group=group, empty=empty,
                bridges=bridges, settled=len(settled), early=early, annex26=P.annex, june_items=june,
                late=late, reg_info=reg_info, rolled_n=V.per_section(P, rolled, W))


def d1(x):
    return str(V.one_dec(x))


# ------------------------------------------------------------------------------ the annex
ANNEX_COLS = ["seccio_censal", "municipi", "districte", "habitatges_grans_tenidors", "percentatge_grans_tenidors",
              "grup_o_titular_amb_mes_habitatges", "habitatges_del_grup_o_titular",
              "habitatges_grans_tenidors_sense_empadronats"]


def write_annex(F, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(ANNEX_COLS)
        for s in F["W"]:                       # the order's own annex order, by section code
            mun, dis = F["place"][s]
            name, n, _ = F["group"][s]
            w.writerow([s, mun, dis, F["lh"][s], d1(F["share"][s]), name, n, F["empty"][s]])


# ------------------------------------------------------------------------------ the bridge chart
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
TOTAL, DOWN, UP, LINE_C = "#3d5a80", "#eb6834", "#2a78d6", "#0b0b0b"


def level_at(start, steps, m):
    """Running level before month m (1 = July)."""
    return start + sum(steps[:m - 1])


def write_bridge(F, path):
    plt.rcParams.update({"font.family": "Carlito", "font.size": 10, "axes.edgecolor": MUTED,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "svg.hashsalt": "task130"})
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.9), dpi=150, sharey=False)
    labels = ["30 Jun\n2026"] + [m[:3] for m in MONTHS] + ["1 Jan\n2027"]
    for ax, s in zip(axes, (F["near_out"], F["near_in"])):
        start, steps, end = F["bridges"][s]
        line = F["N"][s] * LINE / 100
        lo = min(start, end, float(line)) - 14
        hi = max(start, end, float(line)) + 9
        x = range(8)
        ax.bar(0, start - lo, bottom=lo, width=0.62, color=TOTAL, zorder=2)
        ax.bar(7, end - lo, bottom=lo, width=0.62, color=TOTAL, zorder=2)
        level = start
        for i, d in enumerate(steps, 1):
            if d:
                ax.bar(i, abs(d), bottom=min(level, level + d), width=0.62, color=DOWN if d < 0 else UP, zorder=2)
            else:
                ax.plot([i - 0.31, i + 0.31], [level, level], color=MUTED, lw=1.2, zorder=2)
            ax.plot([i - 0.69, i - 0.31], [level, level], color=MUTED, lw=0.7, zorder=1)
            ax.text(i, max(level, level + d) + 0.9, f"{d:+d}" if d else "0", ha="center", va="bottom",
                    fontsize=9.5, color=INK)
            level += d
        ax.plot([6.31, 6.69], [level, level], color=MUTED, lw=0.7, zorder=1)
        ax.text(0, start + 0.9, f"{start}", ha="center", va="bottom", fontsize=10, color=INK, weight="bold")
        ax.text(7, end + 0.9, f"{end}", ha="center", va="bottom", fontsize=10, color=INK, weight="bold")
        ax.axhline(float(line), color=LINE_C, lw=1.1, ls=(0, (4, 3)), zorder=3)
        ax.text(1.5, float(line) + 0.5, f"25% line: {line:.2f}".rstrip("0").rstrip(".") + " dwellings",
                ha="center", va="bottom", fontsize=9, color=INK)
        n_tk, _, done, _, _ = takeovers(F, s)
        if done[-1].year == 2026:
            m = done[-1].month - 6
            ax.annotate(f"agency completes its\n{n_tk}-dwelling purchase\non {day(done[-1])}", xy=(m - 0.33, float(line) + 4),
                        xytext=(m - 1.3, float(line) + 6), ha="center", va="center", fontsize=8.5,
                        color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))
        else:
            ax.text(4.0, float(line) - 5, f"{n_tk} sales the agency took over\ncomplete {span(done)} 2027",
                    ha="center", va="center", fontsize=8.5, color=INK2)
        mun, dis = F["place"][s]
        status = "designated" if s in F["designated"] else "not designated"
        ax.set_title(f"{s}  {mun}, {dis}\n{d1(F['share'][s])}% on 1 January 2027, {status}",
                     loc="left", fontsize=10.5, color=INK)
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylim(lo, hi)
        ax.set_xlim(-0.6, 7.6)
        ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_ylabel("Large-holder dwellings")
    n = len(F["designated"])
    fig.suptitle(f"2027 order: {n} sections designated. The two sections closest to the 25% line, "
                 "30 June 2026 to 1 January 2027", x=0.01, ha="left", fontsize=12.5, color=INK, weight="bold")
    fig.text(0.01, 0.015, "Monthly bars: net change in large-holder dwellings, deeds by execution date. "
             "30 June figure as published in Butlletí del Parc Residencial 2026/2. Axis does not start at zero.",
             fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 0.965))
    fig.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(fig)


# ------------------------------------------------------------------------------ the brief
def takeovers(F, s):
    """The notified sales of section s that the agency took over: (dwellings, commitment dates, completion dates,
    agreed dates, agreed buyer on the register)."""
    tk = V.commitments(F["P"], 120)
    rows = [(tk[k][0], tk[k][1], dt.date.fromisoformat(sch[0]), sch[1] in F["P"].reg)
            for k, _, sec, sch in F["june_items"] if sec == s and sch and k in tk]
    return (len(rows), sorted({r[0] for r in rows}), sorted({r[1] for r in rows}), sorted({r[2] for r in rows}),
            {r[3] for r in rows})


WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}


def day(d):
    return f"{d.day} {d.strftime('%B')}"


def span(ds):
    if len(ds) == 1:
        return f"on {day(ds[0])}"
    if ds[0].month == ds[-1].month:
        return f"between {ds[0].day} and {day(ds[-1])}"
    return f"between {day(ds[0])} and {day(ds[-1])}"


def write_brief(F, path):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13.2, alignment=TA_LEFT, spaceAfter=6)
    small = ParagraphStyle("small", parent=body, fontSize=7.8, leading=10, spaceAfter=3, textColor=colors.HexColor("#3a3936"))
    head = ParagraphStyle("head", parent=body, fontName="Helvetica-Bold", fontSize=10.2, spaceBefore=6, spaceAfter=4)
    title = ParagraphStyle("title", parent=body, fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=8)
    org = ParagraphStyle("org", parent=body, fontName="Helvetica-Bold", fontSize=8.4, leading=11,
                         textColor=colors.HexColor("#3d5a80"), spaceAfter=2)

    W, sh, pl = F["W"], F["share"], F["place"]
    des = F["designated"]
    nin, nout = F["near_in"], F["near_out"]

    def where(s):
        return f"{pl[s][0]}, {pl[s][1]}"

    def listing(codes):
        return codes[0] if len(codes) == 1 else ", ".join(codes[:-1]) + " and " + codes[-1]

    ann26 = {str(r["Secció censal"]): r["Designada"] == "Sí" for _, r in F["annex26"].iterrows()}
    leave = sorted(s for s in W if ann26[s] and s not in des)
    join = sorted(s for s in W if s in des and not ann26[s])
    ly = F["last_year"]
    ly_in = sorted(s for s in ly if s not in des)
    ly_out = sorted(s for s in des if s not in ly)
    tko = {c: takeovers(F, c) for c in ly_in + ly_out}
    s = []
    s.append(Paragraph("OBSERVATORI DEL PARC RESIDENCIAL", org))
    meta = [["To", "Amaro Peláez, Director General for Housing"],
            ["From", "Aurora Roig, Head of the Observatori del Parc Residencial"],
            ["Date", BRIEF_DATE],
            ["Subject", "Proposal for the 2027 designation order (Article 6) and its annex"]]
    mt = Table(meta, colWidths=[20 * mm, 140 * mm], hAlign="LEFT")
    mt.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.8), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.8),
                            ("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.HexColor("#52514e"))]))
    s += [mt, Spacer(1, 9)]
    s.append(Paragraph(f"The 2027 order designates {WORDS[len(des)]} sections", title))
    s.append(Paragraph(
        f"Large holders will hold 25 per cent or more of the dwellings on 1 January 2027 in {WORDS[len(des)]} of "
        f"the fourteen watch-list sections, and the order designates those {WORDS[len(des)]}: {listing(des)}.", body))

    rows = [["Section", "Municipality, district", "Share on 1 Jan 2027"]]
    for c in sorted(des, key=lambda c: -sh[c]):
        rows.append([c, where(c), f"{d1(sh[c])}%"])
    t = Table(rows, colWidths=[28 * mm, 62 * mm, 34 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.8),
                           ("ALIGN", (2, 0), (2, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#52514e"))]))
    s += [t, Spacer(1, 8)]
    s.append(Paragraph(
        f"The designated section closest to the line is <b>{nin}</b> ({where(nin)}), at <b>{d1(sh[nin])}%</b>, "
        f"<b>{d1(sh[nin] - LINE)} points</b> above it. The undesignated section closest to the line is "
        f"<b>{nout}</b> ({where(nout)}), at <b>{d1(sh[nout])}%</b>, <b>{d1(LINE - sh[nout])} points</b> below it. "
        "Both are walked month by month in the attached chart.", body))
    s.append(Paragraph(
        f"Against the 2026 order, {listing(leave)} leave the list and {listing(join)} joins it.", body))

    s.append(Paragraph("How the list was built, and where it differs from last year's method", head))
    s.append(Paragraph(
        "Article 4 counts the dwellings large holders hold on 1 January of the programme year, so the list rests on "
        "holdings on a day that has not come yet. We started from the 30 June 2026 quarterly returns, conformed to "
        "the dwelling, which tie to Butlletí del Parc Residencial 2026/2 in all fourteen sections, and rolled every "
        "dwelling forward with the deeds executed and registered up to 30 September 2026. Sales notified in the "
        "returns and not yet executed were carried to their agreed buyer on their agreed date.", body))
    s.append(Paragraph(
        "The exception is the sales the Ens Públic de Patrimoni Residencial has taken over under its first-offer "
        "right. Its budget execution to 30 September records each commitment under programme PPO, and every "
        f"first-offer purchase it has completed so far ({F['settled']}) was executed 120 days after the commitment, never "
        f"on the date the parties had notified, and {WORDS[F['early']]} of them came before that date. We therefore treat each committed sale as passing to the agency 120 days after "
        "its commitment, and the agency, as a public body, is not a large holder (Article 2.1).", body))
    def held(v):
        parts = [f"{n} {'dwellings ' if i == 0 else ''}in {c}" for i, (c, n) in enumerate(sorted(v.items(), key=lambda kv: -kv[1]))]
        return " and ".join(parts)
    named = [f"{nm} (inscribed {day(dt.date.fromisoformat(d))}) holds {held(v)}" for nm, d, v in F["reg_info"]]
    rest = len(F["late"]) - len(F["reg_info"])
    s.append(Paragraph(
        f"The register also lists {WORDS[len(F['late'])]} holders inscribed after 30 June that have lodged no return "
        "yet; their first is due with the third quarter. From inscription they are large holders under Article 2.1, "
        "and the deed extract shows what they own: " + "; ".join(named) + ", all bought from private owners before "
        f"30 June. The other {WORDS[rest]} hold nothing in the watch list. A roll that starts from the returns "
        "alone leaves these dwellings out.", body))
    s.append(Paragraph(
        f"This is where the list departs from the 2026 method, which Celestina Gallart's notes describe and which "
        f"reproduces the 2026 annex exactly. Built that way, the 2027 list would carry {WORDS[len(ly)]} sections: "
        f"{listing(ly_in)} would stay on it and {listing(ly_out)} would drop off.", body))
    why = []
    for c in ly_in:
        n, com, done, agreed, lh_buyer = tko[c]
        assert lh_buyer == {True} and done[-1] < dt.date(2027, 1, 1)
        why.append(f"In {c} the agency committed {span(com)} to {n} dwellings sold between large holders, so it "
                   f"holds them from {day(done[-1])}, before the year ends.")
    for c in ly_out:
        n, com, done, agreed, lh_buyer = tko[c]
        assert lh_buyer == {False} and done[0] > dt.date(2027, 1, 1) and {a.month for a in agreed} == {agreed[0].month}
        why.append(f"In {c} it committed {span(com)} to {n} sales to private buyers agreed for "
                   f"{agreed[0].strftime('%B')}; those complete {span(done)} 2027, so the seller still holds the "
                   "dwellings on 1 January.")
    for c in des:
        if V.pct(F["rolled_n"][c], F["N"][c]) < LINE:
            n, com, done, agreed, lh_buyer = takeovers(F, c)
            who = [nm for nm, d, v in F["reg_info"] if c in v]
            why.append(f"In {c} the agency also takes {n} dwellings sold between large holders, {span(done)}, but the "
                       f"{F['lh'][c] - F['rolled_n'][c]} that {who[0]} holds keep the section over the line at "
                       f"{d1(sh[c])}%.")
    s.append(Paragraph(" ".join(why), body))
    s.append(Paragraph("The annex", head))
    s.append(Paragraph(
        "designation_annex_2027.csv carries one row per watch-list section in the order's annex order, with the "
        "contents Article 5 requires.", body))

    full = [["Section", "Municipality, district", "30 Jun 2026", "1 Jan 2027", ""]]
    order = sorted(W, key=lambda c: -sh[c])
    for c in order:
        full.append([c, where(c), f"{d1(V.pct(F['june'][c], F['N'][c]))}%", f"{d1(sh[c])}%",
                     "designated" if c in des else ""])
    ft = Table(full, colWidths=[28 * mm, 62 * mm, 24 * mm, 24 * mm, 24 * mm], hAlign="LEFT")
    cut = 1 + len(des)
    ft.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                            ("ALIGN", (2, 0), (3, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 0.8),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 0.8), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                            ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#52514e")),
                            ("LINEBELOW", (0, cut - 1), (-1, cut - 1), 0.9, colors.HexColor("#0b0b0b"))]))
    cap = Paragraph("Large-holder share of each section's dwellings; the rule marks the 25 per cent line. "
                       "30 June 2026 as published in the bulletin. Source: quarterly returns 2024T3 to 2026T2, "
                       "cadastre extract of 28 September 2026, deeds registered to 30 September 2026, Ens Públic de "
                       "Patrimoni Residencial budget execution to 30 September 2026.", small)
    s.append(KeepTogether([Spacer(1, 2), ft, Spacer(1, 3), cap]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Notes", ParagraphStyle("nh", parent=small, fontName="Helvetica-Bold")))
    for note in (
            "1. Shares are large-holder dwellings over the section's residential cadastral units (Article 2.3), "
            "rounded once to one decimal; the distance to the line is taken from the unrounded share.",
            "2. The largest group or holder is read from the register's group links in force on 1 January 2027, "
            "by declarant and effective date, under the name the register gives it.",
            "3. Dwellings with nobody registered are read from the latest municipal delivery for each district: "
            "September 2026, and June 2026 for València districts 11 and 12 and Alacant district 2, which the "
            "September delivery does not include. Registrations past their two-year renewal date count as lapsed."):
        s.append(Paragraph(note, small))

    def foot(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#52514e"))
        canvas.drawString(20 * mm, 11 * mm, "Observatori del Parc Residencial  |  Designation 2027, proposal to the "
                                            "Direcció General d'Habitatge")
        canvas.drawRightString(190 * mm, 11 * mm, f"page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=18 * mm, title="Designation 2027: proposal and annex",
                            author="Aurora Roig", subject="2027 designation of census sections",
                            creator="Observatori del Parc Residencial", producer="Observatori del Parc Residencial",
                            invariant=1)
    doc.build(s, onFirstPage=foot, onLaterPages=foot)
    b = open(path, "rb").read()
    assert b.count(INVARIANT_PDF_DATE) == 2 and len(PDF_MADE) == len(INVARIANT_PDF_DATE)
    with open(path, "wb") as f:
        f.write(b.replace(INVARIANT_PDF_DATE, PDF_MADE))


# ------------------------------------------------------------------------------ main
def main():
    F = compute()
    os.makedirs(OUT, exist_ok=True)
    write_annex(F, os.path.join(OUT, "designation_annex_2027.csv"))
    write_bridge(F, os.path.join(OUT, "section_bridge_2027.png"))
    write_brief(F, os.path.join(OUT, "designation_brief_2027.pdf"))
    scrub = os.path.join(os.path.dirname(TASK.rstrip("/")) or "..", ".claude/skills/reduce-house-fixes/scripts/"
                         "scrub_producer_metadata.py")
    subprocess.run([sys.executable, scrub, OUT, "--apply", "--producer", "Observatori del Parc Residencial",
                    "--stamp", "2026-10-30"], check=True, stdout=subprocess.DEVNULL)
    for name, hhmm in (("designation_annex_2027.csv", (9, 52)), ("section_bridge_2027.png", (10, 18)),
                       ("designation_brief_2027.pdf", (10, 34))):
        ts = dt.datetime(2026, 10, 30, *hhmm, tzinfo=dt.timezone(dt.timedelta(hours=1))).timestamp()
        os.utime(os.path.join(OUT, name), (ts, ts))
    sh = F["share"]
    print(f"designated ({len(F['designated'])}): {', '.join(F['designated'])}")
    print(f"last year's method would file ({len(F['last_year'])}): {', '.join(F['last_year'])}")
    print(f"settled first-offer purchases at 120 days: {F['settled']}")
    for s in F["W"]:
        name, n, _ = F["group"][s]
        print(f"  {s}  {F['lh'][s]:>4} of {F['N'][s]:>4}  {d1(sh[s]):>5}%  {name} ({n})  empty {F['empty'][s]}")
    print(f"nearest designated {F['near_in']} {d1(sh[F['near_in']])}% (+{d1(sh[F['near_in']] - LINE)} points); "
          f"nearest undesignated {F['near_out']} {d1(sh[F['near_out']])}% (-{d1(LINE - sh[F['near_out']])} points)")
    for s, (a, steps, b) in F["bridges"].items():
        print(f"bridge {s}: {a} " + " ".join(f"{m[:3]} {d:+d}" for m, d in zip(MONTHS, steps)) + f" -> {b}; "
              f"line {F['N'][s] * LINE / 100} dwellings")


if __name__ == "__main__":
    main()
