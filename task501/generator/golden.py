"""Builds the golden board paper (python-docx) from the deliverable script's run against target/, and checks the
script's printed figures against golden_figures.json. Run after build.py."""
import json
import os
import shutil
import subprocess
import sys
import time

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm, Inches

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
T = os.path.join(ROOT, "target")
D = os.path.join(ROOT, "deliverables")
G = json.load(open(os.path.join(HERE, "golden_figures.json")))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
K = lambda x: f"{round(x / 1000):,}"
PCT = lambda x: f"{x * 100:.1f}"
LABEL = {"band": "age band", "strategy_band": "strategy and band", "fund_own": "manager's own"}


def run_script():
    scratch = os.path.join(HERE, "_run")
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    shutil.copytree(T, scratch)
    shutil.copy(os.path.join(D, "standby_facility_2027.py"), scratch)
    out = subprocess.run([sys.executable, "standby_facility_2027.py"], cwd=scratch, capture_output=True, text=True)
    if out.returncode != 0:
        print(out.stderr)
        raise SystemExit("deliverable script failed")
    shutil.move(os.path.join(scratch, "standby_facility_2027_chart.png"), os.path.join(D, "standby_facility_2027_chart.png"))
    shutil.rmtree(scratch)
    return out.stdout


def check_output(text):
    missing = []
    for m in G["months"]:
        for k in ("calls", "dists", "credited", "net", "cum"):
            if K(m[k]) not in text:
                missing.append(f"month {m['month']} {k} {K(m[k])}")
    V = G["validation"]
    for a in V["actual"]:
        if K(a) not in text:
            missing.append(f"actual {K(a)}")
    for c, d in V["candidates"].items():
        for F in d["forecasts"]:
            if K(F) not in text:
                missing.append(f"{c} forecast {K(F)}")
        if f"{PCT(d['mape'])}%" not in text:
            missing.append(f"{c} error {PCT(d['mape'])}")
        if K(d["buffer"]) not in text:
            missing.append(f"{c} furthest ahead {K(d['buffer'])}")
    for s, d in G["bridge"].items():
        for k, v in d.items():
            if K(v) not in text:
                missing.append(f"bridge {s} {k}")
    for m, d in G["cash"].items():
        for k, v in d.items():
            if K(v) not in text:
                missing.append(f"cash {m} {k}")
    for s in (f"CHF {G['tranche']}m", K(G["uncovered_below"]), K(G["peak"]), K(G["buffer"]), f"{G['fee_sel']:,.0f}", f"selected basis: {LABEL[V['winner']]}", "agrees to 180 of 180"):
        if s not in text:
            missing.append(s)
    if missing:
        print("SCRIPT OUTPUT MISSING:", missing)
        raise SystemExit(1)


def table(doc, header, rows, widths, bold_last=False):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        c.text = ""
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        if i > 0:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            r = p.add_run(str(v))
            r.font.size = Pt(8.5)
            if bold_last and ri == len(rows) - 1:
                r.bold = True
            if i > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for i, w in enumerate(widths):
        for row in t.rows:
            row.cells[i].width = Cm(w)
    return t


def source(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(8)


def build_paper():
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = Cm(1.8)
        s.bottom_margin = Cm(1.8)
        s.footer.paragraphs[0].text = "Pensionskasse Werdinsel · Treasury & Liquidity · Stiftungsrat 19.11.2026, Traktandum 4 · internal"
        s.footer.paragraphs[0].runs[0].font.size = Pt(7.5)
    tranche, below = G["tranche"], G["below"]
    req, peak, unc, buf = G["required"], G["peak"], G["uncovered_below"], G["buffer"]
    fp = G["first_past_below"][1]
    pm = G["peak_month"]
    V = G["validation"]
    w = V["winner"]
    p = doc.add_paragraph()
    p.add_run("Pensionskasse Werdinsel").bold = True
    doc.add_paragraph("To: Stiftungsrat, for the sitting of 19 November 2026 (Traktandum 4, Resolution 2026-41)\n"
                      "From: Serena Sidler, Treasury & Liquidity\nDate: 6 November 2026\nRef: TL-2026-27, standby facility 2027")
    h = doc.add_paragraph()
    r = h.add_run(f"Elect the CHF {tranche} million standby tranche for 2027")
    r.bold = True
    r.font.size = Pt(13)
    doc.add_paragraph(
        f"The 2027 plan under RL-PM-04 puts the programme's cumulative net outflow at CHF {K(peak)} thousand by {MONTHS[pm - 1]} 2027. The directive adds "
        f"the buffer the walk-forward test sets, CHF {K(buf)} thousand, the most that realised calls ran ahead of the selected basis's forecast at any point in a test "
        f"horizon (the first half of each year, when the managers close most deals, runs well ahead of an even spread; read at the end of the horizons alone the "
        f"gap is only CHF {K(G['buffer_total'])} thousand), and nets the CHF 75 million reserve: CHF {K(req)} thousand. The smallest tranche "
        f"Lindenhof offers that covers it is CHF {tranche} million. The CHF {below} million tranche would leave CHF {K(unc)} thousand uncovered in {MONTHS[pm - 1]}, "
        f"and the buffered need first runs past it in {MONTHS[fp - 1]} 2027. Commitment and arrangement fees for the year under the term sheet come to "
        f"CHF {G['fee_sel']:,.0f} at CHF {tranche} million and CHF {G['fee_below']:,.0f} at CHF {below} million.")
    doc.add_paragraph(
        f"The basis is the {LABEL[w]} basis. Section 5.3 of the directive selects it on the walk-forward test below: at each of the twelve quarter-ends from "
        f"December 2022 to September 2025, each candidate was estimated on the record up to that quarter-end only and set against what the funds then on the "
        f"register actually called over the following twelve months. The age-band basis carries a test error of {PCT(V['candidates']['band']['mape'])} per cent, "
        f"the strategy-and-band basis {PCT(V['candidates']['strategy_band']['mape'])} per cent and the manager's-own basis {PCT(V['candidates']['fund_own']['mape'])} per cent. "
        f"The manager's-own basis, which the CIO favours, fits the past closely when it is estimated on everything on file, including the years it is then scored "
        f"on; estimated honestly at each origin it is the weakest of the three, because a fund's own record says little about the band it has not yet entered.")
    doc.add_paragraph(
        "Unfunded commitments are carried from the notice ledger under section 6.1, with the recycling clause of each fund applied; the ledger basis agrees to "
        "all 180 audited capital accounts on file. The schedule follows section 5: the selected basis on commitment, capped at each fund's unfunded "
        "commitment, distributions on the audited 31 December 2025 values at the pooled strategy-and-band rates and credited at one quarter, everything at the "
        "30 September rate.")
    p = doc.add_paragraph()
    p.add_run("Walk-forward test, CHF thousand").bold = True
    rows = []
    for (y, m), a, i in zip(V["origins"], V["actual"], range(12)):
        rows.append([f"{MONTHS[m - 1][:3]} {y}", K(a), K(V["candidates"]["band"]["forecasts"][i]), K(V["candidates"]["strategy_band"]["forecasts"][i]), K(V["candidates"]["fund_own"]["forecasts"][i])])
    rows.append(["Test error", "", f"{PCT(V['candidates']['band']['mape'])}%", f"{PCT(V['candidates']['strategy_band']['mape'])}%", f"{PCT(V['candidates']['fund_own']['mape'])}%"])
    rows.append(["Furthest ahead in a horizon", "", K(V["candidates"]["band"]["buffer"]), K(V["candidates"]["strategy_band"]["buffer"]), K(V["candidates"]["fund_own"]["buffer"])])
    table(doc, ["Origin", "Realised, next 12 months", "Age band", "Strategy and band", "Manager's own"], rows, [2.4, 3.4, 2.8, 3.2, 2.8], bold_last=True)
    source(doc, f"Source: notice ledger, register and custodian rate file; RL-PM-04 section 5.3. Each forecast uses the record to the origin only, the funds on the register at the origin, "
                f"and their unfunded commitments at the origin; realised calls cover the same funds. Selected: {LABEL[w]} basis. The last row is the most realised cumulative calls exceeded the forecast's cumulative calls at any month-end of a horizon, at the origin's rate (section 5.6).")
    doc.add_picture(os.path.join(D, "standby_facility_2027_chart.png"), width=Inches(6.4))
    source(doc, "Figure 1. Cumulative net outflow of the 2027 plan, with and without the buffer, against the two tranches plus reserve. Source: standby_facility_2027.py.")
    p = doc.add_paragraph()
    p.add_run("2027 plan, CHF thousand").bold = True
    rows = [[MONTHS[m["month"] - 1], K(m["calls"]), K(m["dists"]), K(m["credited"]), K(m["net"]), K(m["cum"])] for m in G["months"]]
    table(doc, ["Month", "Expected calls", "Expected distributions", "Credited (one quarter)", "Net outflow", "Cumulative"], rows, [2.6, 2.6, 3.0, 2.8, 2.4, 2.4])
    source(doc, "Source: notice ledger, register, audited capital accounts and the custodian rate file as at 30 September 2026; RL-PM-04 section 5. October to December 2026 are "
                "scheduled first and reduce unfunded commitments before the facility year; they are not counted in the cumulative figure (section 4). Rates are carried unrounded and rounded to the nearest thousand after translation.")
    doc.add_page_break()
    p = doc.add_paragraph()
    p.add_run("Appendix A. Programme NAV bridge, 31 December 2025 to 30 June 2026, CHF thousand").bold = True
    SL = {"BO": "Buyout", "GR": "Growth", "PC": "Private credit", "IN": "Infrastructure", "TOTAL": "Programme"}
    rows = [[SL[s], K(G["bridge"][s]["opening"]), K(G["bridge"][s]["calls"]), K(G["bridge"][s]["dists"]), K(G["bridge"][s]["valuation_fx"]), K(G["bridge"][s]["closing"])] for s in ("BO", "GR", "PC", "IN", "TOTAL")]
    table(doc, ["Strategy", "NAV 31.12.2025", "Capital called", "Distributions", "Valuation and currency", "NAV 30.06.2026"], rows, [3.0, 2.8, 2.6, 2.6, 3.0, 2.8], bold_last=True)
    source(doc, "Source: NAV register and notice ledger, conventions of RL-PM-04 section 7. Rosenthal II, Ebersol IV and Juno II had not delivered a 30 June statement at the extract date; "
                "their closing values are the 31 March statements adjusted for calls and distributions with a value date in the second quarter (section 7.3). The Gossamer III distribution in specie of August falls outside the period.")
    p = doc.add_paragraph()
    p.add_run("Appendix B. Cash paid and received, January to September 2026, CHF thousand").bold = True
    rows = [[MONTHS[m - 1], K(G["cash"][str(m)]["calls"]), K(G["cash"][str(m)]["dists"]), K(G["cash"][str(m)]["net"])] for m in range(1, 10)]
    table(doc, ["Month", "Calls paid", "Distributions received", "Net"], rows, [3.0, 3.0, 3.4, 3.0])
    source(doc, "Source: notice ledger by value date at the custodian rate of the value date; the three notices the managers withdrew this year are excluded, as is the Gossamer III "
                "distribution in specie of 24 August, which settled in shares. Net is calls less distributions; negative is cash into the programme account.")
    doc.core_properties.author = "Treasury & Liquidity"
    doc.core_properties.title = "Standby facility 2027"
    doc.save(os.path.join(D, "standby_facility_2027_board_paper.docx"))


if __name__ == "__main__":
    text = run_script()
    check_output(text)
    build_paper()
    scrub = os.path.join(os.path.dirname(ROOT), ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    subprocess.run([sys.executable, scrub, D, "--apply", "--producer", "Pensionskasse Werdinsel", "--stamp", "2026-11-06", "--floor", "2026-10-01", "--ceiling", "2026-11-20"], check=False, capture_output=True)
    sys.path.insert(0, HERE)
    import pack as _pack
    _pack.fix_zip_times(os.path.join(D, "standby_facility_2027_board_paper.docx"), (2026, 11, 6, 9, 0, 0))
    stamp = time.mktime((2026, 11, 6, 9, 0, 0, 0, 0, -1))
    for f in os.listdir(D):
        os.utime(os.path.join(D, f), (stamp, stamp))
    print("golden built")
