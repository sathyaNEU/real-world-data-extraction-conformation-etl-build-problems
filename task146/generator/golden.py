"""task146 architecture 3: the golden deliverables and figures.json, every figure from analysis.py on target/."""
import csv
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.shared import Inches, Pt  # noqa: E402

import analysis as A  # noqa: E402
import postprocess as PP  # noqa: E402

DELIV = ("hb231_phase3_dose_recommendation.docx", "hb231_phase2b_tables.csv")
ARM_NAME = {"PBO": "Placebo", "HB25": "HB-231 25 mg", "HB50": "HB-231 50 mg", "HB100": "HB-231 100 mg",
            "HB200": "HB-231 200 mg"}


def compute(target):
    P = A.Pack(target)
    resp = A.composite(P)
    g, (a16, bw) = A.golden(P, resp)
    easy = A.easy_routes(P, resp)
    pasi = A.ask_pasi(P)
    itch = A.ask_itch(P)
    w2 = sum(float(r["weight_kg"]) for r in P.sub.values()) / len(P.sub)
    w3 = sum(c["weight"] for c in P.feas()) / len(P.feas())
    fig = {
        "call": {"dose_mg": A.pick(g)},
        "phase3_expected": {str(d): round(v, 1) for d, v in g.items()},
        "phase3_side": {str(d): ("at or above" if v >= 70 else "below") for d, v in g.items()},
        "phase2b_arm_pasi75": {str(d): round(easy["arm"][d], 1) for d in A.CANDIDATES},
        "weight_exponent": round(-bw, 2),
        "mean_weight_kg": {"phase2b": round(w2, 1), "phase3": round(w3, 1)},
        "ask_pasi": {"%s|%s" % k: v for k, v in pasi.items()},
        "ask_itch": {"%s|%s" % k: v for k, v in itch.items()},
    }
    return P, fig


def chart(fig):
    d = [50, 100, 200]
    f, ax = plt.subplots(figsize=(6.2, 3.4), dpi=150)
    p2 = [fig["phase2b_arm_pasi75"][str(x)] for x in d]
    p3 = [fig["phase3_expected"][str(x)] for x in d]
    x = range(len(d))
    ax.bar([i - 0.19 for i in x], p2, width=0.36, color="#9BB0C8", label="VELA-2 arm (observed)")
    ax.bar([i + 0.19 for i in x], p3, width=0.36, color="#2F5D8A", label="VELA-3 population (expected)")
    ax.axhline(70, color="#B23A2E", lw=1.2, ls="--")
    ax.text(2.45, 71, "CDP bar 70%", color="#B23A2E", fontsize=7.5, ha="right")
    ax.set_xticks(list(x))
    ax.set_xticklabels(["%d mg" % v for v in d])
    ax.set_ylabel("PASI 75 at week 16 (%)")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    buf = io.BytesIO()
    f.tight_layout()
    f.savefig(buf, format="png", metadata={"Software": None})
    plt.close(f)
    buf.seek(0)
    return buf


def docx(fig, path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("HB-231: phase 3 dose recommendation", level=1)
    doc.add_paragraph("To: Villads Kjaer, HB-231 Programme Lead. Cc: Helle Carlsen, Bodil Lauritsen. "
                      "From: Clinical Pharmacology and Biometrics. 30 November 2026. For the Board papers of "
                      "2 December.")
    p = doc.add_paragraph()
    r = p.add_run("Recommendation: take HB-231 200 mg every four weeks into VELA-3A and VELA-3B.")
    r.bold = True
    e = fig["phase3_expected"]
    doc.add_paragraph(
        "Under section 7.2 of the clinical development plan the phase 3 dose is the lowest of 50, 100 and 200 mg "
        "whose expected week-16 PASI 75 response in the phase 3 population is at least 70 per cent. In the "
        "population the VELA-3 sites listed in the feasibility survey we expect %.0f per cent at 50 mg, %.0f per "
        "cent at 100 mg and %.0f per cent at 200 mg, so 100 mg falls short of the bar and 200 mg clears it."
        % (e["50"], e["100"], e["200"]))
    mw = fig["mean_weight_kg"]
    doc.add_paragraph(
        "In VELA-2 the 100 mg arm reached %.1f per cent, but the VELA-2 patients averaged %.1f kg against %.1f kg "
        "for the VELA-3 candidates. HB-231's trough concentrations fall with body weight (clearance rises about "
        "in proportion to weight, exponent %.2f in the population model of the VELA-2 troughs), and response "
        "follows the trough. Carried through the exposure model and the exposure-response fitted on VELA-2, the "
        "heavier phase 3 patients run lower troughs at 100 mg and respond less often."
        % (fig["phase2b_arm_pasi75"]["100"], mw["phase2b"], mw["phase3"], fig["weight_exponent"]))
    doc.add_picture(chart(fig), width=Inches(5.6))
    t = doc.add_table(rows=1, cols=3)
    t.style = "Light Grid Accent 1"
    for c, h in zip(t.rows[0].cells, ["Dose", "VELA-2 arm, PASI 75 (%)", "VELA-3 population, expected (%)"]):
        c.text = h
    for d in ("50", "100", "200"):
        row = t.add_row().cells
        row[0].text = "%s mg" % d
        row[1].text = "%.1f" % fig["phase2b_arm_pasi75"][d]
        row[2].text = "%.0f" % e[d]
    doc.add_paragraph("")
    doc.add_paragraph("Method: PASI 75 as the VELA-2 SAP defines it (composite: rescue therapy and discontinuation "
                      "count as non-response). Population PK model of the week 4 to 16 troughs (log concentration "
                      "per mg on visit and log body weight); logistic exposure-response of the composite on each "
                      "patient's typical week-16 trough; expected response averaged over every feasibility "
                      "candidate, US weights converted from pounds.")
    doc.save(path)
    PP.normalize_docx(path, "Clinical Pharmacology and Biometrics", "2026-11-27T13:05:00Z", "2026-11-30T09:22:00Z",
                      "HB-231 phase 3 dose recommendation")


def tables_csv(fig, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["measure", "arm", "percent"])
        for m in ("PASI 75", "PASI 90"):
            for a in A.ARMS:
                w.writerow(["%s at week 16" % m, ARM_NAME[a], "%.1f" % fig["ask_pasi"]["%s|%s" % (m, a)]])
        for wk in ("Week 12", "Week 16"):
            for a in A.ARMS:
                w.writerow(["Itch NRS responders at %s" % wk.lower(), ARM_NAME[a],
                            "%.1f" % fig["ask_itch"]["%s|%s" % (wk, a)]])


def write_all(target, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    P, fig = compute(target)
    docx(fig, os.path.join(golden_dir, DELIV[0]))
    tables_csv(fig, os.path.join(golden_dir, DELIV[1]))
    return fig
