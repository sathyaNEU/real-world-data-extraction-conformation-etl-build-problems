"""The golden deliverables, computed from the shipped files only: kvr_2027_pitch_markets.csv (each candidate market's
2026 trips and passengers) and kvr_2027_route_pitch_brief.docx (the three markets, the first left out and the gap, the
chart of every candidate's trips); and figures.json, every figure the write-up states."""
import csv
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B      # noqa: E402
import methods as M     # noqa: E402
import world as W       # noqa: E402

BLUE = "#1f4e79"
GREY = "#b7bec6"
AMBER = "#b8742a"


def fmt(n):
    return "{:,}".format(int(n))


def compute(target):
    P = B.Pack(target)
    trips = M.estimate(P)
    pax = M.estimate(P, unit="passengers")
    rungs = {name: M.estimate(P, **kw) for name, _, kw in M.RUNGS}
    return dict(P=P, trips=trips, pax=pax, rungs=rungs)


def figures(X):
    P = X["P"]
    cand = P.candidates
    order = [m for m, _ in M.ranking(X["trips"], cand)]
    three, fourth = order[:3], order[3]
    name = lambda m: P.market_name[m]
    t, p = X["trips"], X["pax"]
    E = P.quarter_entries()
    r0 = M.top3(X["rungs"]["R0"], cand)
    return dict(
        three=[dict(code=m, name=name(m), trips=fmt(B.r100(t[m])), passengers=fmt(B.r100(p[m]))) for m in three],
        first_left_out=dict(code=fourth, name=name(fourth), trips=fmt(B.r100(t[fourth])),
                            passengers=fmt(B.r100(p[fourth]))),
        gap=fmt(B.r100(t[three[2]] - t[fourth])),
        markets=[dict(code=m, name=name(m), trips=fmt(B.r100(t[m])), passengers=fmt(B.r100(p[m])),
                      pitched=m in three) for m in order],
        candidates=len(cand),
        served=[name(m) for m in P.served],
        served_shortlisted=[name(m) for m in P.served if m in P.shortlist],
        served_other=[name(m) for m in P.served if m not in P.shortlist],
        entries={"Q%d" % q: fmt(E[q]) for q in (1, 2, 3, 4)},
        default_three=[name(m) for m in r0],
        dup_rows=str(P.dup_rows),
        dup_batch=P.dup_batch,
        stated=dict(clauses=["standard 2.1", "standard 2.4", "standard 3.1", "standard 4.1"]),
        close_day=str(sorted(set(P.close_day.values()))[0]),
    )


def write_csv(F, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["market_code", "city_market", "trips_2026", "passengers_2026", "in_2027_pitch"])
        for r in F["markets"]:
            wr.writerow([r["code"], r["name"], r["trips"].replace(",", ""), r["passengers"].replace(",", ""),
                         "Y" if r["pitched"] else "N"])


def chart_png(X, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = F["markets"][::-1]
    vals = [B.r100(X["trips"][r["code"]]) for r in rows]
    cols = [BLUE if r["pitched"] else (AMBER if r["code"] == F["first_left_out"]["code"] else GREY) for r in rows]
    fig, ax = plt.subplots(figsize=(6.6, 4.3), dpi=150)
    ax.barh(range(len(rows)), vals, color=cols, height=0.66)
    for i, (r, v) in enumerate(zip(rows, vals)):
        ax.text(v + 60, i, fmt(v), va="center", ha="left", fontsize=7.2, color="#2b2b2b")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r["name"] for r in rows], fontsize=7.8)
    ax.set_xlabel("Trips parked at Brennick International from the Kessick Valley service area, 2026", fontsize=7.6)
    ax.set_xlim(0, max(vals) * 1.13)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: fmt(v)))
    ax.tick_params(axis="x", labelsize=7.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=BLUE, label="In the 2027 pitch"), Patch(color=AMBER, label="First market left out"),
                       Patch(color=GREY, label="Other candidates")], fontsize=7, frameon=False, loc="lower right")
    ax.set_title("%s, %s and %s lead the %d candidate markets" % (
        F["three"][0]["name"], F["three"][1]["name"], F["three"][2]["name"], F["candidates"]), fontsize=9,
        loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _page_field(paragraph):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = paragraph.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write_docx(X, F, path):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt, RGBColor
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Inches(0.9)
        sec.top_margin = sec.bottom_margin = Inches(0.8)
    h = doc.add_paragraph()
    run = h.add_run("%s, %s  |  Air Service Development" % (W.STATE_AGENCY, W.BUREAU))
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x5C, 0x5C, 0x5C)
    foot = doc.sections[0].footer.paragraphs[0]
    fr = foot.add_run("Kessick Valley Regional 2027 route pitch  |  Page ")
    fr.font.size = Pt(8)
    fr.font.color.rgb = RGBColor(0x5C, 0x5C, 0x5C)
    _page_field(foot)
    three = F["three"]
    fo = F["first_left_out"]
    t = doc.add_paragraph()
    rt = t.add_run("%s, %s and %s go in Kessick Valley's 2027 nonstop pitch" % (three[0]["name"], three[1]["name"],
                                                                                 three[2]["name"]))
    rt.bold = True
    rt.font.size = Pt(14)
    rt.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    meta = doc.add_paragraph()
    meta.add_run("To: Director, %s\nFrom: %s, Air Service Development Manager\nDate: 29 January 2027\n"
                 "Subject: Markets for the 2027 pitch for new nonstop service from %s (spring route development "
                 "conference, March 2027)" % (W.BUREAU, W.PEOPLE["asd"], W.REGIONAL)).font.size = Pt(9.5)
    p = doc.add_paragraph()
    r1 = p.add_run("The 2027 pitch carries %s, %s and %s. " % (three[0]["name"], three[1]["name"], three[2]["name"]))
    r1.bold = True
    p.add_run("In 2026 the Kessick Valley service area drove to Brennick International and parked in the long-stay lots "
              "to fly to %s on %s trips, to %s on %s and to %s on %s, the three largest of the %d candidate markets "
              "under the pitch standard (section 4.1). %s is the first market left out, at %s trips, %s below %s." % (
                  three[0]["name"], three[0]["trips"], three[1]["name"], three[1]["trips"], three[2]["name"],
                  three[2]["trips"], F["candidates"], fo["name"], fo["trips"], F["gap"], three[2]["name"]))
    doc.add_paragraph(
        "The trips are Brennick's long-stay transient entries for each quarter of 2026, split by the parking card "
        "survey's four waves. A card comes back only when its car leaves, and each wave's drop boxes were taken in two "
        "days after its last handout day, so a card handed in a wave's last week could come back only from a short "
        "stay, and a card from a three-week stay only if it was handed in the first nine days. Each returned card "
        "is therefore weighted by the wave's cards handed over the cards handed on the days that left room for its "
        "stay to end before the boxes came in. Counted card for card, the replies would have put %s in the pitch: "
        "they lose most of the two- to four-week winter stays that make up much of the Phoenix and Tampa trips, "
        "while the valley's two- and three-night business trips come back from nearly every handout day."
        % _join(F["default_three"]))
    doc.add_picture(io.BytesIO(chart_png(X, F)), width=Inches(6.3))
    cap = doc.add_paragraph()
    rc = cap.add_run("Trips parked by the Kessick Valley service area at Brennick International, 2026, by candidate "
                     "market, nearest hundred. Every candidate's trips and passengers are in %s." % W.GOLDEN["csv"])
    rc.italic = True
    rc.font.size = Pt(8)
    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = "Light List Accent 1"
    for c, txt in zip(tbl.rows[0].cells, ("Market", "Trips, 2026", "Passengers, 2026")):
        c.text = txt
    for r in three + [fo]:
        row = tbl.add_row().cells
        row[0].text = r["name"] + ("" if r is not fo else " (first left out)")
        row[1].text, row[2].text = r["trips"], r["passengers"]
    for rw in tbl.rows:
        for c in rw.cells[1:]:
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    doc.add_paragraph()
    doc.add_paragraph(
        "The candidates are the market review's shortlist less %s, which Sunstream Air serves at Sanford from 11 "
        "February to 25 April 2027 (standard section 3.1). Kessick Valley's year-round flights go to %s, none of them "
        "on the shortlist." % (_join(F["served_shortlisted"]), _join(F["served_other"])))
    src = doc.add_paragraph()
    rs = src.add_run("Sources: Brennick parking revenue control system, daily entries by lot, 2026 (extracts of 6 "
                     "January 2027); %s, long-stay parking survey 2026, cards, verbatims and handout log (delivered 15 "
                     "December 2026); Kessick Valley Regional nonstop schedule 2027 (20 January 2027); Air Service "
                     "Pitch Standard, 2027 pitch." % W.CONTRACTOR)
    rs.italic = True
    rs.font.size = Pt(8)
    notes = doc.add_paragraph()
    rn = notes.add_run(
        "Notes. A trip is one car's stay in Economy C, Economy D or Long-Term, counted once whatever its party; "
        "passengers count the party in full as the traveller wrote it on the card (a card reading 2 adults 2 kids is "
        "four). The garage and permit entries are outside the basis. Each wave stands for its quarter. Figures are "
        "rounded to the nearest hundred from unrounded totals; the gap is taken before rounding.")
    rn.font.size = Pt(8.5)
    rn.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
    doc.save(path)


def main(target, golden, figures_path):
    import postprocess as PP
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    F = figures(X)
    write_csv(F, os.path.join(golden, W.GOLDEN["csv"]))
    write_docx(X, F, os.path.join(golden, W.GOLDEN["brief"]))
    PP.normalize_ooxml(os.path.join(golden, W.GOLDEN["brief"]), W.PEOPLE["asd"], W.PEOPLE["asd"],
                       "2027-01-27T15:12:00Z", "2027-01-29T21:41:00Z",
                       company="%s, %s" % (W.STATE_AGENCY, W.BUREAU))
    stamp = 1801429260.0
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (stamp, stamp))
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return X
