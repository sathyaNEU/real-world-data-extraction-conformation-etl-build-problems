"""The pack's documents: the federation's 2027 medicines safety programme specification, the deprescribing review
protocols and the Clun Valley pilot's close-out report. Each is a Word document exported by LibreOffice Writer, with
its own issue date; table cells wrap inside the page."""
import datetime as dt
import math
import os

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf as O
import world as W

ORG = "Marches Primary Care Collaborative"
INK = colors.HexColor("#1d2b36")


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13.2, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4f5f6b")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                                spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("cell", parent=base, fontSize=8.6, leading=11, spaceAfter=0),
            "head": ParagraphStyle("head", parent=base, fontName="Helvetica-Bold", fontSize=8.6, leading=11,
                                   spaceAfter=0)}


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, author, subject, blocks, footer, created, modified, widths=None):
    st = _styles()
    story = []
    width = A4[0] - 40 * mm
    k = 0
    for kind, val in blocks:
        if kind == "table":
            ncol = max(len(r) for r in val)
            w = (widths or {}).get(k)
            k += 1
            if w:
                cw = [width * x / sum(w) for x in w]
            else:
                cw = [width / ncol] * ncol
            data = [[Paragraph(_esc(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(val)]
            story += [Table(data, colWidths=cw, hAlign="LEFT"), Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    O.build(path, story, title, author, subject, footer, created, modified, margin_mm=20, top_mm=18, bottom_mm=18)


def _at(y, m, d, hh, mi):
    return dt.datetime(y, m, d, hh, mi, 0, tzinfo=dt.timezone.utc)


# --------------------------------------------------------------------------------------------------------------------
def programme(path):
    h = W.HARM
    blocks = [
        ("t", "Medicines Safety Programme 2027-28"),
        ("s", "Programme specification agreed with NHS Severn Marches Integrated Care Board under the medicines safety "
              "schedule of the 2027-28 primary care contract. Version 1.2, 18 November 2026. Owner: Leigh Bond, "
              "Clinical Director. Programme lead: Colin French, Lead Clinical Pharmacist. ICB contact: Sylvia McDonald, "
              "Medicines Optimisation Pharmacist."),
        ("h", "1. Purpose"),
        ("p", "From April 2027 the federation's clinical pharmacist team will run one structured deprescribing review "
              "across the member practices outside the Clun Valley network. The Clun Valley practices took part in the "
              "2026 pilot of all three candidate reviews and are not in scope for 2027-28. The board will choose the "
              "review at its January 2027 meeting."),
        ("h", "2. Candidate reviews"),
        ("table", [["Review", "Patients", "Protocol"],
                   ["A", "Antipsychotics in people aged 65 and over", "Deprescribing review protocols 2026, protocol A"],
                   ["B", "Benzodiazepines and Z-drugs in people aged 65 and over",
                    "Deprescribing review protocols 2026, protocol B"],
                   ["C", "Gabapentinoids taken with an opioid", "Deprescribing review protocols 2026, protocol C"]]),
        ("h", "3. How the review is chosen"),
        ("p", "3.1 The board will run the review expected to avoid the most serious harm in its first year."),
        ("p", "3.2 For each candidate review, the patients in scope are those registered at a member practice outside "
              "the Clun Valley network who meet the review's protocol on 31 December 2026. The team will review every "
              "patient in scope."),
        ("p", "3.3 For each patient in scope, the harm avoided is the chance that the patient is off the medicine six "
              "months after their review, multiplied by the rate of serious harm attributable to continued use at the "
              "patient's age on 31 December 2026 (table 1). A review's harm avoided is the sum over its patients in "
              "scope, and the patients it takes off their medicine are the sum of those chances."),
        ("p", "3.4 A patient is off the medicine when no medicine in the review's class is issued to them in the 183 "
              "days after their review."),
        ("p", "Table 1. Serious harms attributable to continued use, per 100 patient-years"),
        ("table", [["Age", "A Antipsychotics", "B Benzodiazepines and Z-drugs", "C Gabapentinoids with an opioid"],
                   ["18 to 64", "not in scope", "not in scope", "%.1f" % h["GB"]["18 to 64"]],
                   ["65 to 74", "%.1f" % h["AP"]["65 to 74"], "%.1f" % h["BZ"]["65 to 74"], "%.1f" % h["GB"]["65 to 74"]],
                   ["75 to 84", "%.1f" % h["AP"]["75 to 84"], "%.1f" % h["BZ"]["75 to 84"], "%.1f" % h["GB"]["75 to 84"]],
                   ["85 and over", "%.1f" % h["AP"]["85 and over"], "%.1f" % h["BZ"]["85 and over"],
                    "%.1f" % h["GB"]["85 and over"]]]),
        ("s", "Serious harm: death, stroke, a fracture after a fall, or an emergency admission for a fall, pneumonia, "
              "respiratory depression or over-sedation. Rates are the excess over people of the same age not taking the "
              "medicine, from the ICB medicines safety evidence summary (October 2025), and are applied without further "
              "adjustment."),
        ("h", "4. Activity reporting"),
        ("p", "4.1 The team reports its activity to the ICB each quarter as patient consultations per 1,000 registered "
              "patients for each primary care network. Each patient a pharmacist consults, one to one in person, by "
              "telephone or by video, or as one of the patients at a group medicines review, is one patient consultation. "
              "A patient counts towards the network of the practice they are registered with on the day of the "
              "consultation."),
        ("p", "4.2 Registered patients are the patients registered with the network's member practices on the first day "
              "of the period, as published in the federation's monthly list size extract."),
        ("p", "4.3 Each half-year the team also reports the hospital medicine letters received by each network's "
              "practices, from Wrekinside Teaching Hospitals NHS Trust and Marches Mental Health NHS Trust, per 1,000 "
              "registered patients. A letter counts once, in the half and at the practice of its first receipt."),
        ("h", "5. Governance"),
        ("p", "The board approves the review and the programme lead reports progress to the ICB's medicines "
              "optimisation group each quarter. Changes to this specification are agreed in writing with the ICB."),
    ]
    _pdf(path, "Medicines Safety Programme 2027-28", ORG, "Programme specification for the 2027-28 deprescribing review",
         blocks, "Medicines Safety Programme 2027-28, version 1.2", _at(2026, 11, 18, 10, 41), _at(2026, 11, 18, 15, 7),
         widths={0: [8, 40, 40], 1: [14, 18, 26, 28]})


def protocols(path):
    def prods(cls, skip=()):
        return ", ".join(W.PROD[v]["name"] for v in sorted(W.PROD, key=lambda v: W.PROD[v]["name"])
                         if W.PROD[v]["cls"] == cls and not any(W.PROD[v]["name"].startswith(s) for s in skip))
    blocks = [
        ("t", "Structured deprescribing reviews: search and review protocols"),
        ("s", "Version 2.0, 8 December 2025. Approved by the federation's clinical governance group for the 2026 pilot "
              "and the 2027-28 programme. Owner: Colin French, Lead Clinical Pharmacist."),
        ("h", "Searches"),
        ("p", "Each protocol is run as a search of the practice clinical system on a search date. Issues are counted in "
              "the six months to and including the search date. Ages are on the search date. Codes are SNOMED CT "
              "concepts recorded on or before the search date."),
        ("h", "Protocol A: antipsychotics in people aged 65 and over"),
        ("table", [["Criterion", "Definition"],
                   ["Age", "65 and over"],
                   ["Medicine", "At least two issues of: " + prods("AP")],
                   ["Exclude", "Psychotic disorder (69322001), schizophrenia (58214004) or bipolar disorder (13746004) "
                               "ever recorded; on the palliative care register (1129481000000101)"]]),
        ("h", "Protocol B: benzodiazepines and Z-drugs in people aged 65 and over"),
        ("table", [["Criterion", "Definition"],
                   ["Age", "65 and over"],
                   ["Medicine", "At least three issues of any of: " + prods("BZ", skip=("Clobazam",)) +
                                ". Clobazam is not included."],
                   ["Exclude", "On the palliative care register (1129481000000101)"]]),
        ("h", "Protocol C: gabapentinoids taken with an opioid"),
        ("table", [["Criterion", "Definition"],
                   ["Age", "18 and over"],
                   ["Medicine", "At least two issues of " + prods("GB") + ", and at least two issues of any of: " +
                                prods("OP")],
                   ["Exclude", "Epilepsy (84757009) ever recorded; on the palliative care register (1129481000000101)"]]),
        ("h", "The review"),
        ("p", "1. The practice sends the patient an invitation with the leaflet for their medicine. Patients who lack "
              "capacity are reviewed with their carer or the person holding lasting power of attorney."),
        ("p", "2. A clinical pharmacist holds a structured medication review with the patient, in person or by video, "
              "covering what the medicine is for, how well it works for them, the harms of continuing and the options: "
              "stop, taper, reduce or continue."),
        ("p", "3. The agreed plan is recorded in the patient's record and in the deprescribing outcome log on the day of "
              "the review: Stopped, Taper agreed, Dose reduced, Continued, or Continued, patient declined change."),
        ("p", "4. Tapers follow the federation's tapering guides and use the patient's existing supply where it allows."),
        ("p", "5. Six months after the review the practice pharmacist checks the issue record for the 183 days after the "
              "review and records Off medicine or On medicine in the outcome log."),
        ("h", "Records"),
        ("p", "The outcome log holds one row per review and one per six-month check. A patient who dies or leaves the "
              "practice before the six-month check has no six-month row."),
    ]
    _pdf(path, "Structured deprescribing reviews: protocols", ORG, "Search and review protocols A, B and C", blocks,
         "Deprescribing review protocols, version 2.0", _at(2025, 12, 8, 9, 22), _at(2025, 12, 8, 16, 48),
         widths={0: [16, 70], 1: [16, 70], 2: [16, 70]})


def _chi2_p(table):
    """p-value of the chi-squared test of independence for a two-column table of off and on counts."""
    rows = [r for r in table if sum(r) > 0]
    tot = sum(sum(r) for r in rows)
    col = [sum(r[j] for r in rows) for j in range(2)]
    stat = 0.0
    for r in rows:
        n = sum(r)
        for j in range(2):
            e = n * col[j] / tot
            if e > 0:
                stat += (r[j] - e) ** 2 / e
    df = len(rows) - 1
    from scipy.stats import chi2
    return float(chi2.sf(stat, df)), df


def closeout(path, target):
    P = pd.read_csv(os.path.join(target, "deprescribing_pilot_outcome_log_2026.csv"), dtype=str)
    R = pd.read_parquet(os.path.join(target, "patient_registrations_2020-2026.parquet"))
    R = R.drop_duplicates("patient_pseudonym").set_index("patient_pseudonym")
    reg = pd.read_csv(os.path.join(target, "member_practice_register_2026.csv"), dtype=str).set_index("ods_code")
    labels = ["Antipsychotics 65+", "Benzodiazepines and Z-drugs 65+", "Gabapentinoid with opioid"]
    names = {"Antipsychotics 65+": "A Antipsychotics", "Benzodiazepines and Z-drugs 65+": "B Benzodiazepines and Z-drugs",
             "Gabapentinoid with opioid": "C Gabapentinoids with an opioid"}
    rev = P[P["record_type"] == "Review"]
    six = P[P["record_type"] == "Six-month follow-up"].copy()
    six["off"] = six["outcome"] == "Off medicine"
    six["age"] = 2026 - six["patient_pseudonym"].map(R["birth_month"]).str[:4].astype(int)
    six["band"] = six["age"].map(W.age_band)
    six["sex"] = six["patient_pseudonym"].map(R["sex"])
    t1 = [["Review", "Reviewed", "Stopped", "Taper agreed", "Dose reduced", "Continued", "Declined change"]]
    t1b = [["Review", "Six-month check", "Off medicine", "Off, per cent"]]
    for lab in labels:
        r = rev[rev["review"] == lab]
        s = six[six["review"] == lab]
        vc = r["outcome"].value_counts()
        t1.append([names[lab], len(r), int(vc.get("Stopped", 0)), int(vc.get("Taper agreed", 0)),
                   int(vc.get("Dose reduced", 0)), int(vc.get("Continued", 0)),
                   int(vc.get("Continued, patient declined change", 0))])
        t1b.append([names[lab], len(s), int(s["off"].sum()), "%.1f" % (100 * s["off"].mean())])
    died = len(rev) - len(six)
    stopped = set(rev.loc[rev["outcome"] == "Stopped", "patient_pseudonym"] + "|" + rev.loc[rev["outcome"] == "Stopped", "review"])
    back_on = six[(six["outcome"] == "On medicine") & ((six["patient_pseudonym"] + "|" + six["review"]).isin(stopped))]
    restarted = len(back_on)
    pr = sorted(six["practice_code"].unique())
    t2 = [["", "A Antipsychotics", "B Benzodiazepines", "C Gabapentinoids"]]
    pvals = []
    for title, key, levels in (("Practice", "practice_code", pr),
                               ("Age", "band", ["18 to 64", "65 to 74", "75 to 84", "85 and over"]),
                               ("Sex", "sex", ["F", "M"])):
        for lv in levels:
            row = [("%s %s" % (lv, reg.loc[lv, "practice_name"])) if key == "practice_code" else
                   ({"F": "Women", "M": "Men"}.get(lv, lv))]
            for lab in labels:
                s = six[(six["review"] == lab) & (six[key] == lv)]
                row.append("%d of %d (%.0f%%)" % (s["off"].sum(), len(s), 100 * s["off"].mean()) if len(s) else "none")
            t2.append(row)
        for lab in labels:
            s = six[six["review"] == lab]
            tab = [[int(g["off"].sum()), int((~g["off"]).sum())] for _, g in s.groupby(key)]
            pvals.append(_chi2_p(tab)[0])
    pmin = min(pvals)
    blocks = [
        ("t", "Clun Valley deprescribing pilot 2026: close-out report"),
        ("s", "5 January 2027. Colin French, Lead Clinical Pharmacist. For the federation board and the ICB medicines "
              "optimisation group."),
        ("h", "1. What the pilot did"),
        ("p", "Between 12 January and 26 June 2026 the pharmacist team ran all three candidate reviews in the six Clun "
              "Valley practices. Each practice searched its patients on 12 January 2026 using protocols A, B and C "
              "(version 2.0) and invited every patient the searches found. Reviews were held at the practices and at the "
              "Clun Valley hub. Each patient's six-month status was checked from the issue record for the 183 days after "
              "their review; the last checks were made on 31 December 2026."),
        ("h", "2. Outcomes"),
        ("p", "Outcome recorded at the review:"),
        ("table", t1),
        ("p", "Status at the six-month check:"),
        ("table", t1b),
        ("p", "%d reviewed patients died before their six-month check and have no six-month status. The off rate is the "
              "patients off their medicine at six months as a share of the patients with a six-month check. %d patients "
              "whose medicine was stopped at the review had it issued again within the six months and are counted as on "
              "their medicine." % (died, restarted)),
        ("h", "3. Consistency across practices and patients"),
        ("p", "The share of patients off their medicine at six months, by practice, age and sex (patients with a "
              "six-month check):"),
        ("table", t2),
        ("p", "No practice, age group or sex differed from its review's overall rate by more than chance (chi-squared "
              "tests of each review by practice, by age group and by sex: the smallest p-value was %.2f)." % pmin),
        ("h", "4. Delivery"),
        ("p", "The reviews took a median of 32 minutes of pharmacist time each, plus about 10 minutes of administration. "
              "No serious incidents were reported."),
        ("p", "The outcome log (deprescribing_pilot_outcome_log_2026.csv) holds the review and six-month rows for every "
              "patient. This report does not make a recommendation on the 2027-28 review, which the board will choose "
              "in January 2027."),
    ]
    _pdf(path, "Clun Valley deprescribing pilot 2026: close-out report", ORG, "Close-out of the 2026 deprescribing pilot",
         blocks, "Clun Valley deprescribing pilot 2026, close-out report", _at(2027, 1, 5, 11, 3),
         _at(2027, 1, 5, 14, 26), widths={0: [30, 11, 11, 11, 11, 11, 13], 1: [30, 16, 16, 16], 2: [34, 20, 20, 20]})
    return dict(died=died, pmin=pmin, restarted=restarted)


def write_docs(f, target):
    programme(f("programme"))
    protocols(f("protocols"))
    return closeout(f("closeout"), target)
