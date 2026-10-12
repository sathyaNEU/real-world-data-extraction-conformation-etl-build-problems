"""Files that sit beside the PSUR data package and are not part of the analysis: the Medical Information
enquiry log, the weekly literature screening log and the signal tracker."""
import datetime as dt

import numpy as np
import pandas as pd

import pack as P
import world as W

TD = dt.timedelta

SRD = {
    "SRD-LYR-01": "Administration and missed doses", "SRD-LYR-02": "Dose step-up to 30 mg",
    "SRD-LYR-03": "Hepatic and renal impairment", "SRD-LYR-04": "Laboratory monitoring",
    "SRD-LYR-05": "Respiratory symptoms and pulmonary monitoring", "SRD-LYR-06": "Vaccination",
    "SRD-LYR-07": "Herpes zoster", "SRD-LYR-08": "Pregnancy and breastfeeding", "SRD-LYR-09": "Interactions",
    "SRD-LYR-10": "Storage and handling", "SRD-LYR-11": "Switching from another JAK inhibitor",
    "SRD-LYR-12": "Surgery and treatment interruption", "SRD-LYR-13": "Infections during treatment",
    "SRD-LYR-14": "Venous thromboembolism", "SRD-LYR-15": "Patient support programme",
}
QUESTIONS = [
    ("Dosing", "Patient missed two doses, how to restart?", "SRD-LYR-01", 0.08),
    ("Dosing", "When can the dose be stepped up to 30 mg?", "SRD-LYR-02", 0.07),
    ("Dosing", "Dose in moderate hepatic impairment", "SRD-LYR-03", 0.03),
    ("Monitoring", "Which laboratory tests before starting and how often afterwards?", "SRD-LYR-04", 0.09),
    ("Monitoring", "How long should lung function be followed after starting Lyrevo?", "SRD-LYR-05", 0.05),
    ("Monitoring", "Is a baseline HRCT needed in a patient with RA-associated lung disease?", "SRD-LYR-05", 0.03),
    ("Monitoring", "Patient with new cough and breathlessness: stop or continue?", "SRD-LYR-05", 0.03),
    ("Monitoring", "Lipid monitoring after week 12", "SRD-LYR-04", 0.03),
    ("Vaccination", "Can a live zoster vaccine be given during treatment?", "SRD-LYR-06", 0.05),
    ("Vaccination", "Recombinant zoster vaccine before initiation", "SRD-LYR-06", 0.04),
    ("Safety", "Shingles during treatment, can Lyrevo continue?", "SRD-LYR-07", 0.05),
    ("Safety", "Neutrophil count of 1.2, continue treatment?", "SRD-LYR-04", 0.04),
    ("Safety", "Raised ALT at the three-month check", "SRD-LYR-04", 0.04),
    ("Safety", "History of DVT, can Lyrevo be started?", "SRD-LYR-14", 0.03),
    ("Safety", "Serious infection: when to restart?", "SRD-LYR-13", 0.04),
    ("Pregnancy", "Contraception and conception planning", "SRD-LYR-08", 0.04),
    ("Interactions", "Use with clarithromycin or ketoconazole", "SRD-LYR-09", 0.04),
    ("Handling", "Can tablets be split or crushed?", "SRD-LYR-10", 0.04),
    ("Handling", "Tablets left in a hot car", "SRD-LYR-10", 0.02),
    ("Switching", "Washout when switching from another JAK inhibitor", "SRD-LYR-11", 0.04),
    ("Surgery", "Stop before elective surgery?", "SRD-LYR-12", 0.05),
    ("PSP", "Enrolling a patient in the support programme", "SRD-LYR-15", 0.05),
    ("PSP", "Starter pack request", "SRD-LYR-15", 0.04),
]
ENQ = [("Physician", 0.42), ("Pharmacist", 0.22), ("Nurse", 0.14), ("Patient or carer", 0.22)]
CHANNEL = [("Phone", 0.46), ("E-mail", 0.31), ("Web form", 0.18), ("Field team", 0.05)]


def _pick(g, mix):
    u = g.random()
    acc = 0.0
    for v, w in mix:
        acc += w
        if u < acc:
            return v
    return mix[-1][0]


def medinfo(path):
    g = np.random.default_rng([254, 501])
    rows = []
    n = 0
    d = W.LAUNCH
    qmix = [(q, w) for q in QUESTIONS for w in [q[3]]]
    while d <= dt.date(2026, 10, 2):
        months = (d - W.LAUNCH).days / 30.4
        lam = 0.6 + 1.6 * min(1.0, months / 30.0)
        k = g.poisson(lam)
        for _ in range(k):
            n += 1
            q = _pick(g, qmix)
            mk = _pick(g, [(m, W.MARKETS[m][1]) for m in W.MARKET_ORDER if W.MARKETS[m][0] <= d] or [("DK", 1)])
            et = _pick(g, ENQ)
            ae = "Y" if (q[0] == "Safety" and g.random() < 0.55) else "N"
            rows.append(["MI-%d-%05d" % (d.year, 400 + n), d, mk, et, _pick(g, CHANNEL), q[0], q[1], q[2], ae,
                         d + TD(days=int(g.integers(0, 6)))])
        d += TD(days=1)
    rows = [r for r in rows if r[9] <= dt.date(2026, 10, 2)]

    def main(ws):
        P._sheet(ws, ["enquiry_id", "received", "country", "enquirer", "channel", "category", "question",
                      "standard_response", "ae_forwarded_to_pv", "closed"], rows, [13, 11, 8, 16, 10, 13, 66, 16, 10, 11])
        for col in (2, 10):
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for c in row:
                    c.number_format = "yyyy-mm-dd"

    def srd(ws):
        P._sheet(ws, ["standard_response", "title"], [[k, v] for k, v in SRD.items()], [18, 50])
    P._wb("medinfo", path, [("enquiries", main), ("standard responses", srd)])
    return len(rows)


PUB = [("Article", 0.35), ("Review", 0.18), ("Conference abstract", 0.25), ("Case report", 0.08), ("Letter", 0.06),
       ("Pharmacoeconomic", 0.08)]
TOPIC = ["JAK inhibitor class safety", "Efficacy in rheumatoid arthritis", "Efficacy in psoriatic arthritis",
         "Real-world persistence", "Herpes zoster with JAK inhibitors", "Venous thromboembolism with JAK inhibitors",
         "Interstitial lung disease in RA", "Malignancy risk with JAK inhibitors", "Cost-effectiveness",
         "Laboratory changes on JAK inhibitors", "Infections in elderly patients", "Lipid changes"]


def literature(path, li_cases, dup_li):
    """Weekly search hits. Every hit assessed as a valid individual case names a case already in the
    safety database: the literature reports in the export and literature reports linked as duplicates."""
    g = np.random.default_rng([254, 502])
    rows = []
    n = 0
    weeks = []
    d = dt.date(2023, 3, 6)
    while d <= dt.date(2026, 10, 5):
        weeks.append(d)
        d += TD(days=7)
    by_week = {}
    for c, rcpt in li_cases:
        wk = rcpt - TD(days=rcpt.weekday())
        by_week.setdefault(wk, []).append((c, "ICSR: case created"))
    for c, rcpt in dup_li:
        wk = rcpt - TD(days=rcpt.weekday())
        by_week.setdefault(wk, []).append((c, "ICSR: case created, linked as duplicate"))
    for wk in weeks:
        k = g.poisson(4 + 9 * min(1.0, (wk - weeks[0]).days / 900.0))
        for _ in range(k):
            n += 1
            pt = _pick(g, PUB)
            topic = TOPIC[int(g.integers(0, len(TOPIC)))]
            ass = _pick(g, [("Not relevant: no Lyrevo exposure", 0.46), ("No individual case", 0.40),
                            ("Duplicate hit", 0.10), ("Full text reviewed: no case", 0.04)])
            rows.append([wk, "Embase" if g.random() < 0.6 else "MEDLINE", "LIT-%d-%05d" % (wk.year, n), pt, topic, ass, ""])
        for c, ass in by_week.get(wk, []):
            n += 1
            rows.append([wk, "Embase", "LIT-%d-%05d" % (wk.year, n), "Case report", "Adverse reaction during Lyrevo treatment",
                         ass, c])
    df = pd.DataFrame(rows, columns=["search_week", "database", "hit_ref", "publication_type", "topic", "assessment",
                                     "case_no"])
    df["search_week"] = df["search_week"].map(lambda v: v.isoformat())
    P.write_csv(path, df)
    return len(df)


SIGNALS = [
    ("Alopecia", "Spontaneous reports", "2023-11-06", "Validated", "Closed: added to SmPC 4.8 (uncommon)"),
    ("Pancreatitis", "Spontaneous reports", "2024-01-15", "Not validated", "Closed: no new information"),
    ("Herpes zoster ophthalmicus", "Spontaneous reports", "2024-02-26", "Validated", "Closed: covered by identified risk herpes zoster"),
    ("Rhabdomyolysis with CPK increase", "Spontaneous reports", "2024-04-08", "Validated", "Closed: refuted"),
    ("Gastrointestinal perforation", "EudraVigilance eRMR", "2024-05-13", "Validated", "Closed: important potential risk retained"),
    ("Retinal vein occlusion", "Spontaneous reports", "2024-06-24", "Validated", "Closed: covered by identified risk VTE"),
    ("Hearing loss", "Literature", "2024-07-29", "Not validated", "Closed: insufficient evidence"),
    ("Fatal interstitial lung disease", "Spontaneous reports", "2024-09-09", "Validated", "Closed: SmPC 4.4 wording strengthened"),
    ("Tuberculosis reactivation", "EudraVigilance eRMR", "2024-10-21", "Validated", "Closed: screening advice in SmPC 4.4"),
    ("Acne in adolescents", "Spontaneous reports", "2024-11-25", "Not validated", "Closed: labelled"),
    ("Drug-induced liver injury with jaundice", "Spontaneous reports", "2025-01-13", "Validated", "Closed: Hy's law cases reviewed, none confirmed"),
    ("Febrile neutropenia", "Spontaneous reports", "2025-02-17", "Validated", "Closed: covered by identified risk neutropenia"),
    ("Skin squamous cell carcinoma", "PRAC request", "2025-03-24", "Validated", "Closed: term list updated (v4)"),
    ("Myocarditis", "Literature", "2025-04-28", "Not validated", "Closed: no causal association"),
    ("Pulmonary embolism over 65 years", "Spontaneous reports", "2025-06-02", "Validated", "Ongoing: PASS registry analysis"),
    ("Opportunistic infections", "PSUR 5 assessment", "2025-07-07", "Validated", "Closed: merged into serious infections"),
    ("Lymphopenia below 0.5", "Spontaneous reports", "2025-08-18", "Validated", "Ongoing: cumulative review"),
    ("Hypersensitivity", "Spontaneous reports", "2025-09-22", "Not validated", "Closed: labelled"),
    ("Diverticulitis", "EudraVigilance eRMR", "2025-10-27", "Validated", "Ongoing: assessment"),
    ("Pneumocystis pneumonia", "Spontaneous reports", "2025-12-01", "Validated", "Closed: covered by identified risk serious infections"),
    ("Weight increase", "Spontaneous reports", "2026-01-12", "Not validated", "Closed: labelled"),
    ("Interstitial lung disease after dose step-up", "Spontaneous reports", "2026-02-16", "Not validated", "Closed: no dose relationship"),
    ("Kaposi's sarcoma", "Literature", "2026-03-23", "Not validated", "Closed: single case, confounded"),
    ("Hepatitis B reactivation", "EudraVigilance eRMR", "2026-04-27", "Validated", "Ongoing: assessment"),
    ("Erythema multiforme", "Spontaneous reports", "2026-05-25", "Not validated", "Closed: insufficient evidence"),
    ("Herpes zoster disseminated", "Spontaneous reports", "2026-06-29", "Validated", "Ongoing: cumulative review for PSUR 6"),
    ("Arterial thromboembolism", "PRAC request", "2026-07-27", "Validated", "Ongoing: PSUR 6 section 16"),
    ("Neutropenia in patients on methotrexate", "Spontaneous reports", "2026-08-24", "Validated", "Ongoing: assessment"),
    ("Medication error: tablet strength confusion", "Spontaneous reports", "2026-09-14", "Validated", "Ongoing: RMM review"),
]


def signals(path):
    g = np.random.default_rng([254, 503])
    rows = []
    for i, (topic, src, det, val, status) in enumerate(SIGNALS):
        d0 = dt.date.fromisoformat(det)
        vdate = d0 + TD(days=int(g.integers(10, 40)))
        if vdate > dt.date(2026, 9, 30):
            # the tracker was exported on 30 September: a signal still in validation has no outcome yet
            val, vdate, status = "In progress", None, "Ongoing: validation"
        nxt = "" if status.startswith("Closed") else (dt.date(2026, 10, 1) + TD(days=int(g.integers(20, 90)))).isoformat()
        rows.append(["SIG-%d-%03d" % (d0.year, 3 + i * 2), topic, src, d0, val, vdate, status, nxt])

    def main(ws):
        P._sheet(ws, ["signal_id", "topic", "source", "detected", "validation", "validated_on", "status", "next_review"],
                 rows, [14, 44, 22, 11, 13, 12, 52, 12])
        for col in (4, 6):
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for c in row:
                    c.number_format = "yyyy-mm-dd"
    P._wb("signals", path, [("tracker", main)])
    return len(rows)
