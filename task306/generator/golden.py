"""The golden deliverables (the board paper and the consultations file), figures.json and submission.md, all from the
golden analysis on the cut pack."""
import csv
import datetime as dt
import os
import shutil
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, PageBreak, Paragraph, Spacer, Table  # noqa: E402

import analysis as A  # noqa: E402
import officepdf as O  # noqa: E402

PAPER = "medicines_safety_review_2027.pdf"
CSV = "pharmacist_consultations_2026.csv"
LETTER = {"AP": "A", "BZ": "B", "GB": "C"}
NAME = {"AP": "antipsychotics in people aged 65 and over",
        "BZ": "benzodiazepines and Z-drugs in people aged 65 and over",
        "GB": "gabapentinoids taken with an opioid"}
SHORT = {"AP": "A Antipsychotics", "BZ": "B Benzodiazepines and Z-drugs", "GB": "C Gabapentinoids with an opioid"}
TITLE = {"AP": "antipsychotic", "BZ": "benzodiazepine and Z-drug", "GB": "gabapentinoid"}
NETS = sorted(A.NETWORKS)
INK = colors.HexColor("#1d2b36")


def compute(target):
    D = A.load(target)
    L = A.resolved_letters(D)
    E = A.eligible(D)
    M = A.main_call(D, E=dict(E), L=L)
    F = A.figures_main(M)
    R1 = A.main_call(D, how="pooled", E=dict(E), L=L)
    six = M["six"]
    fig = {"call": F["call"], "runner_up": F["runner_up"], "third": F["third"], "gap": F["gap"], "reviews": {},
           "pilot": {}, "rung1": {}, "constants": {"window_days": 60, "per": 1000, "off_days": 183}}
    for cls in A.REVIEWS:
        e = M["res"][cls]
        spec = float((e["prov"] == "specialist").mean())
        fig["reviews"][cls] = {"in_scope": F[cls]["eligible"], "off_10": F[cls]["off_10"],
                               "harms_1": F[cls]["harms_1"], "off": round(F[cls]["off"], 3),
                               "harms": round(F[cls]["harms"], 4), "specialist_pct": int(round(100 * spec)),
                               "specialist_share": round(spec, 4)}
        s = six[six["cls"] == cls]
        fig["pilot"][cls] = {}
        for pv in ("practice", "specialist"):
            g = s[s["prov"] == pv]
            fig["pilot"][cls][pv] = {"off": int(g["off"].sum()), "n": int(len(g)),
                                     "pct": int(round(100 * g["off"].mean()))}
        fig["pilot"][cls]["all"] = {"off": int(s["off"].sum()), "n": int(len(s)),
                                    "pct": round(100 * s["off"].mean(), 1)}
        fig["rung1"][cls] = {"harms_1": int(round(R1["summary"][cls]["harms"])),
                             "harms": round(R1["summary"][cls]["harms"], 3)}
    sp = six[six["prov"] == "specialist"]
    pr = six[six["prov"] == "practice"]
    fig["pilot"]["specialist_all"] = {"off": int(sp["off"].sum()), "n": int(len(sp))}
    fig["pilot"]["practice_all"] = {"off": int(pr["off"].sum()), "n": int(len(pr))}
    LA = A.letters_received(D, L=L)
    CB = A.consultations(D)
    fig["letters"] = {n_: {h: {"rate": A.r1(LA[(n_, h)]["rate"]), "letters": LA[(n_, h)]["letters"],
                               "patients": LA[(n_, h)]["patients"]} for h in ("H1", "H2")} for n_ in NETS}
    fig["consultations"] = {n_: {q: {"rate": A.r1(CB[(n_, q)]["rate"]), "consultations": CB[(n_, q)]["consultations"],
                                     "patients": CB[(n_, q)]["patients"]} for q in ("Q1", "Q2", "Q3", "Q4")}
                            for n_ in NETS}
    return fig


def chart(fig, path):
    order = ["AP", "BZ", "GB"]
    labels = [SHORT[c] for c in order][::-1]
    off = [fig["reviews"][c]["off_10"] for c in order][::-1]
    harms = [fig["reviews"][c]["harms_1"] for c in order][::-1]
    col = ["#1f4e79" if c == fig["call"] else "#a9b4bd" for c in order][::-1]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task306"})
    f, axes = plt.subplots(1, 2, figsize=(6.6, 2.3), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, vals, title, fmt in ((axes[0], off, "Patients off their medicine at six months", "about {:,}"),
                                 (axes[1], harms, "Serious harms avoided a year", "{}")):
        ax.barh(range(3), vals, color=col, height=0.56, edgecolor="white", linewidth=1.5)
        for i, v in enumerate(vals):
            ax.text(v + max(vals) * 0.02, i, fmt.format(v), va="center", fontsize=8, color="#1d2b36")
        ax.set_title(title, fontsize=8.8, loc="left", color="#1d2b36")
        ax.set_xlim(0, max(vals) * 1.32)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color("#8a9aa6")
        ax.tick_params(colors="#4f5f6b", length=2)
        ax.grid(axis="x", color="#e3e7ea", linewidth=0.6)
        ax.set_axisbelow(True)
    axes[0].set_yticks(range(3))
    axes[0].set_yticklabels(labels)
    f.savefig(path, dpi=220, bbox_inches="tight", metadata={"Software": None})
    plt.close(f)


def _st():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13.2, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=3),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4f5f6b")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                                spaceBefore=5),
            "p": base,
            "cell": ParagraphStyle("cell", parent=base, fontSize=8.6, leading=11, spaceAfter=0),
            "head": ParagraphStyle("head", parent=base, fontName="Helvetica-Bold", fontSize=8.6, leading=11,
                                   spaceAfter=0)}


def _table(rows, widths, st):
    width = A4[0] - 40 * mm
    cw = [width * x / sum(widths) for x in widths]
    data = [[Paragraph(str(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(rows)]
    return [Table(data, colWidths=cw, hAlign="LEFT"), Spacer(1, 5)]


def paper(fig, path, png):
    st = _st()
    rv, pl = fig["reviews"], fig["pilot"]
    c, r2, r3 = fig["call"], fig["runner_up"], fig["third"]
    head = [["Meeting", "Federation board, 14 January 2027"], ["Agenda item", "6"],
            ["Paper", "Choosing the 2027-28 deprescribing review"],
            ["Prepared by", "Colin French, Lead Clinical Pharmacist"], ["Sponsor", "Leigh Bond, Clinical Director"],
            ["For", "Decision"]]
    t1 = [["Review", "Patients in scope", "Started by a specialist service", "Off their medicine at six months",
           "Serious harms avoided a year"]]
    for k in ("AP", "BZ", "GB"):
        t1.append([SHORT[k], "{:,}".format(rv[k]["in_scope"]), "%d%%" % rv[k]["specialist_pct"],
                   "about {:,}".format(rv[k]["off_10"]), str(rv[k]["harms_1"])])
    t2 = [["Pilot, off at six months", "A Antipsychotics", "B Benzodiazepines and Z-drugs",
           "C Gabapentinoids with an opioid"]]
    for pv, lab in (("practice", "Medicine started by the practice"),
                    ("specialist", "Medicine started by a specialist service")):
        t2.append([lab] + ["%d of %d (%d%%)" % (pl[k][pv]["off"], pl[k][pv]["n"], pl[k][pv]["pct"])
                           for k in ("AP", "BZ", "GB")])
    t2.append(["All reviewed patients"] + ["%d of %d (%.0f%%)" % (pl[k]["all"]["off"], pl[k]["all"]["n"],
                                                                   pl[k]["all"]["pct"]) for k in ("AP", "BZ", "GB")])
    t3 = [["Primary care network", "January to June 2026", "July to December 2026"]]
    for n_ in NETS:
        t3.append([n_, "%.1f" % fig["letters"][n_]["H1"]["rate"], "%.1f" % fig["letters"][n_]["H2"]["rate"]])
    story = []
    story += _table(head, [22, 66], st)
    story += [
        Paragraph("Run the %s review in 2027-28" % TITLE[c], st["t"]),
        Paragraph("Recommendation", st["h"]),
        Paragraph("<b>Run review %s, %s, across the member practices outside the Clun Valley network from April 2027. "
                  "It would take about %s patients off their medicine and avoid about %d serious harms a year, %d more "
                  "than the runner-up, review %s (%s, about %d).</b> Review %s (%s) would avoid about %d."
                  % (LETTER[c], NAME[c], "{:,}".format(rv[c]["off_10"]), rv[c]["harms_1"], fig["gap"], LETTER[r2],
                     NAME[r2], rv[r2]["harms_1"], LETTER[r3], NAME[r3], rv[r3]["harms_1"]), st["p"]),
        Paragraph("The board is asked to approve review %s for the medicines safety schedule of the 2027-28 contract "
                  "with the integrated care board." % LETTER[c], st["p"]),
    ]
    story += _table(t1, [30, 14, 18, 20, 18], st)
    story += [Paragraph("Source: the practices' issue, problem list and registration extracts at 31 December 2026; "
                        "the trusts' medicine letters feed; the pilot outcome log. Patients are rounded to the nearest "
                        "10 and harms to whole numbers.", st["s"]),
              Image(png, width=160 * mm, height=160 * mm * 2.3 / 6.6 * 0.98),
              Paragraph("Figure 1. Review %s avoids the most harm, although review %s would take more patients off "
                        "their medicine." % (LETTER[c], LETTER[r2]), st["s"]),
              Paragraph("How the estimate was made", st["h"]),
              Paragraph("Patients in scope are those registered at a member practice outside the Clun Valley network "
                        "who met the review's protocol on 31 December 2026, as the programme specification sets out "
                        "(section 3). Each patient's chance of being off the medicine six months after review is taken "
                        "from the Clun Valley pilot, and the harm it avoids from table 1 of the specification at their "
                        "age on 31 December 2026.", st["p"]),
              Paragraph("The pilot's results turn on who started the medicine. Where a hospital or mental health trust "
                        "service started it (a trust letter naming a medicine of the review's class in the 60 days "
                        "before the practice first issued it), our pharmacists took %d of %d patients off; where the "
                        "practice started it, %d of %d. The Clun Valley practices are a long way from the memory and "
                        "older adults' mental health services, so most of their antipsychotic patients were started by "
                        "the practice. In the other networks a specialist service started %d%% of the patients in "
                        "scope for review %s, against %d%% for review %s and %d%% for review %s. Each patient in scope "
                        "is therefore given the pilot rate for their review and the way their medicine was started."
                        % (pl["specialist_all"]["off"], pl["specialist_all"]["n"], pl["practice_all"]["off"],
                           pl["practice_all"]["n"], rv["AP"]["specialist_pct"], "A", rv["BZ"]["specialist_pct"], "B",
                           rv["GB"]["specialist_pct"], "C"), st["p"])]
    story += _table(t2, [30, 19, 19, 19], st)
    story += [Paragraph("Source: deprescribing pilot outcome log, six-month checks; the trusts' medicine letters "
                        "feed.", st["s"]),
              Paragraph("Applying each review's overall pilot rate to every patient instead would favour review A, at "
                        "about %d harms a year, because it treats the specialist-started antipsychotic patients as if "
                        "they would come off as readily as the pilot's." % fig["rung1"]["AP"]["harms_1"], st["p"]),
              Paragraph("Note. Following section 3.3 of the specification, a review's patients off their medicine are "
                        "the sum of each patient's chance, an expected number rather than a list of named patients.",
                        st["s"]),
              Paragraph("Hospital medicine letters", st["h"]),
              Paragraph("Medicine letters from Wrekinside Teaching Hospitals and Marches Mental Health received by each "
                        "network's practices, per 1,000 registered patients at the start of each half of 2026. A letter "
                        "the mental health trust re-sent on 7 April 2026 is counted once, when it was first received.",
                        st["p"])]
    story += _table(t3, [40, 24, 24], st)
    story += [Paragraph("Source: the trusts' medicine letters feed and the practices' document workflow log to 6 "
                        "January 2027; registered list sizes on 1 January and 1 July 2026. From October the hospital "
                        "trust's letters arrive through GP Connect and are matched to the workflow log by patient and "
                        "the first receipt after the letter's date; a letter not received by 6 January 2027 is not "
                        "counted.", st["s"]),
              Paragraph("The team's patient consultations by network and quarter of 2026 are in %s." % CSV, st["p"])]
    created = dt.datetime(2027, 1, 12, 16, 5, 0, tzinfo=dt.timezone.utc)
    modified = dt.datetime(2027, 1, 13, 9, 48, 0, tzinfo=dt.timezone.utc)
    assert rv[r2]["off"] > rv[c]["off"], "the caption says the runner-up takes more patients off"
    O.build(path, story, "Run the %s review in 2027-28" % TITLE[c], "Marches Primary Care Collaborative",
            "Board paper: the 2027-28 deprescribing review", "Federation board, 14 January 2027, item 6", created,
            modified, margin_mm=20, top_mm=17, bottom_mm=17)


def consultations_csv(fig, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["primary_care_network", "quarter", "patient_consultations", "registered_patients_at_start",
                    "consultations_per_1000"])
        for n_ in NETS:
            for q in ("Q1", "Q2", "Q3", "Q4"):
                x = fig["consultations"][n_][q]
                w.writerow([n_, "2026 " + q, x["consultations"], x["patients"], "%.1f" % x["rate"]])


def write_all(target, golden, base):
    import writeup as WU
    os.makedirs(golden, exist_ok=True)
    fig = compute(target)
    work = tempfile.mkdtemp(prefix="t306chart-")
    try:
        png = os.path.join(work, "figure1.png")
        chart(fig, png)
        paper(fig, os.path.join(golden, PAPER), png)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    consultations_csv(fig, os.path.join(golden, CSV))
    WU.write(fig, os.path.join(base, "submission.md"))
    return fig
