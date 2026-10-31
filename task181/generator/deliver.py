"""figures.json, the golden deliverables, submission.md and metadata.json, every figure from solve.py on target/.

    python3 task181/generator/deliver.py
"""
import io
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
from docx import Document         # noqa: E402
from docx.shared import Cm, Pt    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import solve as S    # noqa: E402
import build as B    # noqa: E402

DOCX = "ssi_review_response_2027.docx"
CSV = "ssi_review_figures_2027.csv"
plt.rcParams["svg.hashsalt"] = "task181"


def figures(R):
    gold, naive = R["gold"], R["naive"]
    rr = R["rr"]
    return {
        "call": {"referred": S.referred(gold), "default_path": S.referred(naive)},
        "repair": R["repair"].strftime("%Y-%m-%d %H:%M"),
        "window_procedures": int(((R["P"]["day"] >= C.WIN0) & (R["P"]["day"] <= C.WIN1)).sum()),
        "exposed_procedures": rr[1],
        "exposed_ratio": round(rr[0], 1),
        "exposed": {"observed": int(rr[2]), "expected": round(float(rr[3]), 1)},
        "unexposed": {"observed": int(rr[4]), "expected": round(float(rr[5]), 1)},
        "naive": {c: {"observed": v["observed"], "expected": round(v["expected"], 1), "limit": v["limit"]}
                  for c, v in naive.items()},
        "traced": {c: {"procedures": v["n"], "observed": v["observed"], "expected": round(v["expected"], 1),
                       "limit": v["limit"]} for c, v in gold.items()},
        "ask_a": R["ask_a"], "ask_b": R["ask_b"],
        "conventions": {"surveillance_days": 30, "implant_days": 90, "limit_centile": 97.5, "link_days": 3,
                        "heavy_container_kg": 10},
    }


def chart(fig, path):
    cs = C.CONSULTANTS
    t = fig["traced"]
    f, ax = plt.subplots(figsize=(7.2, 3.6), dpi=150)
    cols = ["#c0392b" if c in fig["call"]["referred"] else "#7f8c8d" for c in cs]
    ax.bar(range(len(cs)), [t[c]["observed"] for c in cs], color=cols, width=0.6, label="Infections")
    ax.scatter(range(len(cs)), [t[c]["limit"] for c in cs], marker="_", s=420, color="#1f2d3d", zorder=3,
               label="Upper control limit")
    ax.set_xticks(range(len(cs)))
    ax.set_xticklabels(cs, fontsize=8)
    ax.set_ylabel("Infections, April to September 2027", fontsize=8)
    ax.set_title("Infections in each consultant's procedures not reached by the steriliser 3 fault",
                 fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=8)
    f.tight_layout()
    f.savefig(path)
    plt.close(f)


def response_docx(fig, path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("Response to outlier notice HAISC/ON/2027/031", level=1)
    doc.add_paragraph("Kooralong Health, general surgery, procedures from 1 April to 30 September 2027. "
                      "Prepared for the Executive Director of Medical Services, January 2028.")
    ref = fig["call"]["referred"]
    doc.add_heading("Consultants referred to professional practice review", level=2)
    doc.add_paragraph("%s and %s go to professional practice review; no other consultant does." % tuple(ref))
    doc.add_paragraph(
        "From 12 May 2027 operations whose instrument tray had last been sterilised by steriliser 3 carried %.1f "
        "times the infection rate of the department's other operations. Steriliser 3 is the CSSD's one chamber for "
        "instrument containers over 10 kg, so it sterilises the heavy colorectal trays, among them every tray GS-05 "
        "and GS-12 use. Set those operations aside and each consultant's infections stand against the Centre's "
        "expectation for the rest of their procedures."
        % fig["exposed_ratio"])
    doc.add_heading("Each consultant against the upper control limit", level=2)
    tab = doc.add_table(rows=1, cols=6)
    tab.style = "Light Grid Accent 1"
    hdr = ["Consultant", "All procedures: infections", "Limit", "Procedures without a steriliser 3 tray",
           "Infections", "Limit", ]
    for k, h in enumerate(hdr):
        tab.rows[0].cells[k].text = h
    for c in C.CONSULTANTS:
        n, t = fig["naive"][c], fig["traced"][c]
        row = tab.add_row().cells
        row[0].text = c + (" (referred)" if c in ref else "")
        row[1].text = str(n["observed"])
        row[2].text = str(n["limit"])
        row[3].text = str(t["procedures"])
        row[4].text = str(t["observed"])
        row[5].text = str(t["limit"])
    buf = io.BytesIO()
    png = os.path.join(C.GOLDEN, "_chart.png")
    chart(fig, png)
    doc.add_paragraph("")
    doc.add_picture(png, width=Cm(16))
    os.remove(png)
    doc.add_heading("Finding outside the consultants' practice", level=2)
    doc.add_paragraph("Steriliser 3 has been withdrawn from service pending revalidation of its drying stage, and "
                      "the trays it sterilised since its 12 May 2027 repair have been recalled for reprocessing.")
    cp = doc.core_properties
    cp.author = "Kooralong Health, Office of the Executive Director of Medical Services"
    cp.title = "Response to outlier notice HAISC/ON/2027/031"
    import datetime as dt
    cp.created = dt.datetime(2028, 1, 11, 9, 20)
    cp.modified = dt.datetime(2028, 1, 13, 16, 5)
    cp.last_modified_by = cp.author
    doc.save(path)
    C.normalise_zip(path, "2028-01-11T09:20:00Z", "2028-01-13T16:05:00Z", app="Microsoft Office Word")


def figures_csv(fig, path):
    rows = []
    for k, v in fig["ask_a"].items():
        c, y = k.split()
        rows.append(["procedures", c, y, v])
    for k, v in fig["ask_b"].items():
        c, y = k.split()
        rows.append(["infections", c, y, v])
    C.write_csv(path, ["figure", "consultant", "year", "value"], rows)


def metadata(n):
    src = {
        "ops": "a hospital theatre management system's operations export",
        "ssi": "an infection prevention team's surgical site infection surveillance export",
        "scans": "an instrument tracking system's scan export",
        "cycles": "a CSSD's steriliser cycle records",
        "register": "a CSSD's instrument set register",
        "equip": "a CSSD's equipment maintenance log",
        "rates": "a state surveillance centre's published procedure rates",
        "notice": "a state surveillance centre's outlier notice",
        "guide": "a state surveillance centre's outlier response guide",
        "hygiene": "a hospital's ward hand hygiene audit results",
        "air": "a building management system's theatre air sampling export",
    }
    meta = {
        "task": "task181",
        "files": [{"name": B.FILES[k], "source": "synthetic, generated by task181/generator for this task",
                   "format": B.FILES[k].rsplit(".", 1)[1], "license": "CC0-1.0", "created": "2026-10-31"}
                  for k in B.FILES],
        "distractors": [B.FILES[k] for k in B.DISTRACTORS],
        "deliverables": [DOCX, CSV],
        "rows": n,
    }
    with open(os.path.join(C.TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
        f.write("\n")


def make(n=None):
    R = S.solve()
    fig = figures(R)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    os.makedirs(C.GOLDEN, exist_ok=True)
    for x in os.listdir(C.GOLDEN):
        os.remove(os.path.join(C.GOLDEN, x))
    response_docx(fig, os.path.join(C.GOLDEN, DOCX))
    figures_csv(fig, os.path.join(C.GOLDEN, CSV))
    import writeup
    writeup.write(os.path.join(C.TASK, "submission.md"), fig)
    metadata(n or {})
    return fig


if __name__ == "__main__":
    print(make()["call"])
