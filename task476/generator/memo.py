"""The water manager's memo to the partners (docx): the purchase, the ranch against what it had available, each
well's water year volume and its April to September energy charge."""
import datetime as dt

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches

import postprocess as PP

ORDER_NOTE = ("The deep wells' energy is converted interval by interval at the head each pump was lifting against, "
              "read from its logger; their August and September 2025 tests were run near the year's deepest water.")


def _cell(c, text, bold=False, right=False, size=9):
    c.text = ""
    p = c.paragraphs[0]
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if right:
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def write(path, d, g):
    import golden as G
    ex, ch = g["ex"], g["charges"]
    r0 = G.extraction(d, route="R0")
    sh = [1 - r0["vols"][w]["wy"] / ex["vols"][w]["wy"] for w in d["reg"] if str(d["reg"][w]["Aquifer"]) == "Lower"]
    lo, hi = int(round(100 * min(sh))), int(round(100 * max(sh)))
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Inches(0.9)
        s.top_margin = s.bottom_margin = Inches(0.8)
    h = doc.add_paragraph()
    r = h.add_run("Ochre Flats Farming Company")
    r.bold = True
    r.font.size = Pt(13)
    meta = doc.add_paragraph()
    meta.add_run("To: Nicholas Wolf and the partners\nFrom: Melinda Walter, water manager\nDate: November 3, 2026\n"
                 "Re: Buy %d acre-feet of transfer water before the December 15 true-up" % ex["purchase"]).font.size = Pt(10)
    over = ex["total"] - ex["available"]
    p = doc.add_paragraph()
    p.add_run("Recommendation. ").bold = True
    if ex["purchase"] > 0:
        p.add_run("Buy %d acre-feet of transfer water and have it recorded with the Sallow Plains GSA before December "
                  "15. Our wells pumped %s acre-feet in water year 2026 against %s acre-feet available (the %s "
                  "acre-foot allocation plus %d carried over from 2025), %d acre-feet over, and the agency records "
                  "transfers only in whole blocks of %d. At the posted reference price of USD 1,185 an acre-foot the "
                  "purchase is about USD %s; extraction left uncovered is charged USD 1,500 an acre-foot and comes off "
                  "the 2027 allocation."
                  % (ex["purchase"], "{:,}".format(ex["total"]), "{:,.1f}".format(ex["available"]),
                     "{:,.1f}".format(d["notice"]["allocation"]), int(d["notice"]["carryover"]), round(over),
                     d["notice"]["block"], "{:,}".format(ex["purchase"] * 1185)))
    else:
        p.add_run("No transfer is needed: our wells pumped %s acre-feet against %s available."
                  % ("{:,}".format(ex["total"]), "{:,.1f}".format(ex["available"])))
    p = doc.add_paragraph()
    p.add_run("How the volumes were built. ").bold = True
    p.add_run("The four metered upper wells are from their totalizers (the W-03 meter was replaced on June 17). The "
              "other eleven are from the utility's interval data. " + ORDER_NOTE + " Using each test's kWh per "
              "acre-foot for the whole year would have understated the deep wells by %d to %d percent and shown us "
              "inside the allocation." % (lo, hi))
    t = doc.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    for c, txt in zip(t.rows[0].cells, ("Well", "Agency ID", "Aquifer", "WY 2026 (AF)", "Apr-Sep energy (USD)")):
        _cell(c, txt, bold=True)
    for w in sorted(d["reg"]):
        r = d["reg"][w]
        row = t.add_row().cells
        _cell(row[0], "%s %s" % (w, str(r["Ranch name"]).split(" (")[0]))
        _cell(row[1], str(r["Agency well ID"]))
        _cell(row[2], str(r["Aquifer"]))
        _cell(row[3], "{:,}".format(ex["reported"][w]), right=True)
        _cell(row[4], "{:,}".format(int(round(ch[w]))), right=True)
    row = t.add_row().cells
    _cell(row[0], "Ranch", bold=True)
    _cell(row[3], "{:,}".format(ex["total"]), bold=True, right=True)
    _cell(row[4], "{:,}".format(sum(int(round(v)) for v in ch.values())), bold=True, right=True)
    src = doc.add_paragraph()
    sr = src.add_run("Sources: totalizer reads (W-01 to W-04); Valley Rural Power interval data; August and September 2025 "
                     "pump tests; well loggers; VRP schedules AG-2T and AG-3T. Volumes are whole acre-feet per well as the "
                     "agency's return asks, and the ranch total is the sum of the wells' figures (notice section 3).")
    sr.italic = True
    sr.font.size = Pt(8.5)
    p = doc.add_paragraph()
    p.add_run("Energy charges ").bold = True
    stay = [w for w in sorted(d["reg"]) if str(d["reg"][w]["Electric SA (from Apr 1, 2026)"]) not in d["letter"]["sas"]]
    p.add_run("in the table are the season's pumping bill well by well, April through September 2026, the other half of "
              "what this water year's groundwater cost us beside the transfer: energy charges only (no demand or "
              "customer charges), each interval at its time-of-use rate in local time. The %d accounts in Valley Rural "
              "Power's May 14 letter moved from AG-2T to AG-3T on June 1, so their April and May are at AG-2T; %s "
              "stayed on AG-2T." % (len(d["letter"]["sas"]), " and ".join(stay)))
    p = doc.add_paragraph()
    p.add_run("Return. ").bold = True
    p.add_run("The agency return (wy2026_extraction_return.csv) has the monthly volumes and the spring and fall static "
              "depths. I will file it by November 30 once the purchase is approved.")
    doc.core_properties.author = "Melinda Walter"
    doc.save(path)
    PP.normalize_ooxml(path, "Melinda Walter", "Melinda Walter", "2026-11-03T17:12:00Z", "2026-11-03T19:46:24Z",
                       company="Ochre Flats Farming Company")
