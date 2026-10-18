"""The golden deliverables, computed from the shipped files only: corrisan_2026_field_piston_lead.csv (each of the 24
fields without a tower, its 2026 lead) and cvaqd_2027_unleaded_grant_qualification.docx (the memo to the Governing
Board: the qualifying fields, the chart against the round's line, the towered fields' operations and lead); and
figures.json, every figure the write-up states."""
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

GREEN = "#2f6b4a"
GREY = "#a9b1ad"


def fmt(n):
    return "{:,}".format(int(n))


def kg(v):
    return int(round(v))


def r100(v):
    return int(round(v / 100.0)) * 100


def compute(target):
    P = B.Pack(target)
    inv = P.inventory()
    rungs, sets, par = M.rungs(P, inv)
    names = {lid: P.dir[lid]["Facility Name"] for lid in B.FIELDS}
    counties = {lid: P.dir[lid]["County"] for lid in B.FIELDS}
    return dict(P=P, inv=inv, rungs=rungs, sets=sets, par=par, names=names, counties=counties)


def order(X):
    lead = X["inv"]["lead"]
    return sorted(W.UNTOWERED, key=lambda l: (-lead[l], l))


def figures(X):
    inv, names = X["inv"], X["names"]
    lead = inv["lead"]
    q = B.qualifying(lead)
    qo = [l for l in order(X) if l in q]
    below = [l for l in order(X) if l not in q]
    C = W.COUNTED
    unrec_c = sum(inv["unrec"][l] for l in C)
    nd_c = sum(inv["nd"][l] for l in C)
    est = [l for l in order(X) if l not in W.STUDIED]
    r0 = X["sets"]["R0 one capture rate"]
    caps = {l: (inv["tower"][l]["heard_in_hours"] / inv["tower"][l]["civil"]) if l in W.TOWERED else
            inv["heard"].loc[l, "ops"] / X["P"].study[l] for l in C}
    lo, hi = min(caps, key=caps.get), max(caps, key=caps.get)
    r1 = X["sets"]["R1 capture by flight training"]
    return dict(
        count=len(q),
        count_word={6: "Six", 7: "Seven", 8: "Eight"}[len(q)],
        qualifying=[dict(lid=l, name=names[l], lead_kg=kg(lead[l])) for l in qo],
        first_below=dict(lid=below[0], name=names[below[0]], lead_kg=kg(lead[below[0]])),
        threshold_kg=str(W.THRESHOLD_KG),
        fields=[dict(lid=l, name=names[l], county=X["counties"][l], lead_kg=kg(lead[l])) for l in order(X)],
        counted=dict(unrecorded=fmt(unrec_c), never_recorded=str(nd_c), per_airplane="%.1f" % (unrec_c / nd_c)),
        never_recorded={l: str(inv["nd"][l]) for l in est},
        towers=[dict(lid=l, name=names[l], ops=fmt(r100(inv["ops"][l])), lead_kg=kg(lead[l])) for l in W.TOWERED],
        rivals=dict(
            capture_pct=str(int(round(100 * X["par"]["r"]))),
            capture_set=[names[l] for l in r0],
            capture_in=[names[l] for l in r0 if l not in q],
            capture_out=[names[l] for l in q if l not in r0],
            training_set_count=len(r1),
            training_in=[names[l] for l in r1 if l not in q],
            school_pct=str(int(round(100 * X["par"]["r_school"]))),
            other_pct=str(int(round(100 * X["par"]["r_other"]))),
        ),
        unrecorded_g=str(W.LEAD_UNRECORDED),
        stated=dict(clauses=["method 2.1", "method 3.2", "method 4.2", "method 4.3", "method 4.4", "guidelines 2.2"],
                    year="2026", round="2027"),
        capture_low=dict(name=names[lo], pct=str(int(round(100 * caps[lo])))),
        capture_high=dict(name=names[hi], pct=str(int(round(100 * caps[hi])))),
    )


def write_csv(X, F, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["loc_id", "field", "county", "lead_2026_kg"])
        for r in F["fields"]:
            wr.writerow([r["lid"], r["name"], r["county"], r["lead_kg"]])


def chart_png(X, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    lead = X["inv"]["lead"]
    q = {r["lid"] for r in F["qualifying"]}
    ls = order(X)
    vals = [lead[l] for l in ls]
    fig, ax = plt.subplots(figsize=(6.6, 3.5), dpi=150)
    cols = [GREEN if l in q else GREY for l in ls]
    ax.bar(range(len(ls)), vals, color=cols, width=0.68)
    ax.axhline(W.THRESHOLD_KG, color="#7a2e2e", linewidth=1.0, linestyle=(0, (4, 2)))
    ax.text(len(ls) - 0.6, W.THRESHOLD_KG + 0.35, "Round threshold, %.1f kg" % W.THRESHOLD_KG, ha="right",
            va="bottom", fontsize=7.4, color="#7a2e2e")
    for i, (l, v) in enumerate(zip(ls, vals)):
        ax.text(i, v + 0.25, str(kg(v)), ha="center", va="bottom", fontsize=6.4, color="#2b2b2b")
    ax.set_xticks(range(len(ls)))
    ax.set_xticklabels(ls, rotation=90, fontsize=7)
    ax.set_ylabel("2026 lead from piston-engine aircraft (kg)", fontsize=7.8)
    ax.set_title("%s of the 24 fields without a tower reach the %.1f kg line" % (F["count_word"], W.THRESHOLD_KG),
                 fontsize=9, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.set_ylim(0, max(vals) * 1.12)
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
    from docx.shared import Inches, Pt, RGBColor
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Inches(0.9)
        sec.top_margin = sec.bottom_margin = Inches(0.8)
    h = doc.add_paragraph()
    run = h.add_run("%s  |  Planning and Air Toxics" % W.DISTRICT)
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x5C, 0x5C, 0x5C)
    foot = doc.sections[0].footer.paragraphs[0]
    fr = foot.add_run("%s  |  2027 Unleaded Avgas Transition Grants: qualifying fields  |  Page " % W.DISTRICT_SHORT)
    fr.font.size = Pt(8)
    fr.font.color.rgb = RGBColor(0x5C, 0x5C, 0x5C)
    _page_field(foot)
    t = doc.add_paragraph()
    rt = t.add_run("%s fields without a tower qualify for the 2027 unleaded avgas round" % F["count_word"])
    rt.bold = True
    rt.font.size = Pt(14)
    rt.font.color.rgb = RGBColor(0x2F, 0x6B, 0x4A)
    meta = doc.add_paragraph()
    meta.add_run("To: Governing Board, meeting of 10 March 2027\n"
                 "From: %s, %s\nCopy: %s, %s\nDate: 12 February 2027\n"
                 "Subject: 2027 Unleaded Avgas Transition Grants, qualifying fields on the 2026 aircraft lead "
                 "inventory" % (W.PEOPLE["planner"][0], W.PEOPLE["planner"][1], W.PEOPLE["grants"][0],
                                W.PEOPLE["grants"][1])).font.size = Pt(9.5)
    qn_ = ["%s (%s, %d kg)" % (r["name"], r["lid"], r["lead_kg"]) for r in F["qualifying"]]
    p = doc.add_paragraph()
    r1 = p.add_run("%s of the 24 public-use fields without a control tower qualify for the 2027 round: " %
                   F["count_word"])
    r1.bold = True
    p.add_run("%s. Each emitted %.1f kg or more of lead from piston-engine aircraft in 2026 under method %s, "
              "Revision 3, which the round's guidelines (section 2.2) make the test. The highest field below the "
              "line is %s at %d kg." % (_join(qn_), W.THRESHOLD_KG, W.METHOD_ID, F["first_below"]["name"],
                                       F["first_below"]["lead_kg"]))
    doc.add_paragraph(
        "How the operations the network missed were placed. The receiver network records every operation of an "
        "aircraft that broadcasts ADS-B Out and none of one that does not. At the ten fields with a count (the six "
        "towers and the four fields the District had counted through 2026) the counts exceed what the network "
        "recorded by %s operations, and those fields have %s based piston airplanes that the network never "
        "recorded anywhere in 2026: %s operations a year for each. The fields without a count were completed the "
        "same way, %s operations for each based piston airplane the network never recorded there, at %s g each "
        "(method section 3.2). The airplanes that never broadcast are not spread evenly: the vintage fields "
        "keep most of them and the flight-school fields almost none, so the network hears %s per cent of the "
        "counted fields' operations overall, %s per cent at %s and %s per cent at %s." % (
            F["counted"]["unrecorded"], F["counted"]["never_recorded"], F["counted"]["per_airplane"],
            F["counted"]["per_airplane"], F["unrecorded_g"], F["rivals"]["capture_pct"],
            F["capture_low"]["pct"], F["capture_low"]["name"], F["capture_high"]["pct"], F["capture_high"]["name"]))
    doc.add_paragraph(
        "Scaling every field's recorded operations by that %s per cent instead would have qualified %s and "
        "left out %s." % (F["rivals"]["capture_pct"], _join(F["rivals"]["capture_in"]),
                          _join(F["rivals"]["capture_out"])))
    doc.add_picture(io.BytesIO(chart_png(X, F)), width=Inches(6.3))
    cap = doc.add_paragraph()
    rc = cap.add_run("Lead by field, 2026, kilograms. Qualifying fields in green. Field figures in "
                     "%s." % W.GOLDEN["csv"])
    rc.italic = True
    rc.font.size = Pt(8)
    doc.add_paragraph("The towered fields. They are outside the round but complete the 2026 inventory; their "
                      "operations are the network's recorded piston operations, each assigned to the aircraft that "
                      "flew it, and the towers' counts beyond what the network recorded. Where an owner moved an "
                      "N-number to a turbine in 2026, the piston airplane kept flying on its old address until the "
                      "turbine arrived, weeks after the Registry's date, and those operations are counted as its own.")
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = "Light List Accent 1"
    for c, txt in zip(tbl.rows[0].cells, ("Field", "LocID", "Piston operations, 2026", "Lead, 2026 (kg)")):
        c.text = txt
    for r in F["towers"]:
        row = tbl.add_row().cells
        row[0].text, row[1].text, row[2].text, row[3].text = r["name"], r["lid"], r["ops"], str(r["lead_kg"])
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    for rw in tbl.rows:
        for c in rw.cells[2:]:
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = doc.add_paragraph()
    rs = src.add_run("Sources: ADS-B field events export of 8 January 2027; FAA register extract of 1 February "
                     "2027; tower daily counts; the 2026 count studies; the state's 2027 based aircraft "
                     "validation.")
    rs.italic = True
    rs.font.size = Pt(8)
    notes = doc.add_paragraph()
    rn = notes.add_run(
        "Notes. Operations as a tower counts them: a takeoff or a landing is one, a touch-and-go two (method "
        "section 2.1). The year is 2026 in Pacific time. Lead is rounded to the whole kilogram and operations to "
        "the nearest hundred from unrounded totals; qualification is judged on the unrounded lead. An airplane "
        "that changed its N-number during 2026 is counted as recorded when the network heard either address.")
    rn.font.size = Pt(8.5)
    rn.font.color.rgb = RGBColor(0x40, 0x40, 0x40)
    doc.save(path)


def main(target, golden, figures_path):
    import postprocess as PP
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    F = figures(X)
    write_csv(X, F, os.path.join(golden, W.GOLDEN["csv"]))
    write_docx(X, F, os.path.join(golden, W.GOLDEN["memo"]))
    PP.normalize_ooxml(os.path.join(golden, W.GOLDEN["memo"]), W.PEOPLE["planner"][0], W.PEOPLE["planner"][0],
                       "2027-02-09T17:12:00Z", "2027-02-12T22:41:00Z", company=W.DISTRICT)
    stamp = 1802565660.0
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (stamp, stamp))
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return X
