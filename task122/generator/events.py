"""task122 generator: adverse events, concomitant medications, vital signs and trough concentrations of
VMK-4410-202, written from the simulated trial."""
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P
import sim as S
from records import STUDY, usubjid, d, sday

HYPERK_VERB = {"Hyperkalaemia": ["Hyperkalaemia", "Hyperkalemia", "HYPERKALAEMIA", "hyperkalaemia", "Hyperkalaemia (mild)",
                                 "Hyperkaliemia"],
               "Blood potassium increased": ["Potassium increased", "Raised serum potassium", "Elevated potassium",
                                             "K+ elevated", "Increased blood potassium"]}
SOC = {"Hyperkalaemia": "Metabolism and nutrition disorders", "Blood potassium increased": "Investigations"}

# other events: preferred term, system organ class, yearly rate, extra per mg of dose, verbatim forms
OTHER = [
    ("Nasopharyngitis", "Infections and infestations", 0.16, 0.0, ["Common cold", "Nasopharyngitis", "Cold", "URTI symptoms"]),
    ("COVID-19", "Infections and infestations", 0.05, 0.0, ["COVID-19", "Covid infection", "SARS-CoV-2 infection"]),
    ("Upper respiratory tract infection", "Infections and infestations", 0.06, 0.0, ["Upper respiratory tract infection", "URTI"]),
    ("Urinary tract infection", "Infections and infestations", 0.06, 0.0, ["Urinary tract infection", "UTI", "Cystitis"]),
    ("Influenza", "Infections and infestations", 0.03, 0.0, ["Influenza", "Flu"]),
    ("Headache", "Nervous system disorders", 0.07, 0.0, ["Headache", "Headaches"]),
    ("Dizziness", "Nervous system disorders", 0.04, 0.0025, ["Dizziness", "Dizzy", "Light-headedness"]),
    ("Hypotension", "Vascular disorders", 0.02, 0.0018, ["Hypotension", "Low blood pressure", "Blood pressure low"]),
    ("Hypertension", "Vascular disorders", 0.04, 0.0, ["Hypertension", "Worsening hypertension", "High blood pressure"]),
    ("Peripheral oedema", "General disorders and administration site conditions", 0.06, 0.0, ["Ankle oedema", "Peripheral oedema", "Leg swelling"]),
    ("Fatigue", "General disorders and administration site conditions", 0.05, 0.0, ["Fatigue", "Tiredness"]),
    ("Diarrhoea", "Gastrointestinal disorders", 0.05, 0.0, ["Diarrhoea", "Diarrhea", "Loose stools"]),
    ("Nausea", "Gastrointestinal disorders", 0.03, 0.0, ["Nausea"]),
    ("Constipation", "Gastrointestinal disorders", 0.03, 0.0, ["Constipation"]),
    ("Back pain", "Musculoskeletal and connective tissue disorders", 0.05, 0.0, ["Back pain", "Low back pain", "Lumbago"]),
    ("Arthralgia", "Musculoskeletal and connective tissue disorders", 0.04, 0.0, ["Arthralgia", "Joint pain", "Knee pain"]),
    ("Muscle spasms", "Musculoskeletal and connective tissue disorders", 0.03, 0.0, ["Muscle cramps", "Cramps in legs"]),
    ("Gout", "Metabolism and nutrition disorders", 0.03, 0.0, ["Gout", "Gout flare", "Acute gout"]),
    ("Hyponatraemia", "Metabolism and nutrition disorders", 0.01, 0.0011, ["Hyponatraemia", "Low sodium"]),
    ("Anaemia", "Blood and lymphatic system disorders", 0.04, 0.0, ["Anaemia", "Anemia", "Renal anaemia"]),
    ("Cough", "Respiratory, thoracic and mediastinal disorders", 0.04, 0.0, ["Cough"]),
    ("Pruritus", "Skin and subcutaneous tissue disorders", 0.02, 0.0, ["Itching", "Pruritus"]),
    ("Glomerular filtration rate decreased", "Investigations", 0.01, 0.0012, ["eGFR decreased", "Decreased eGFR", "GFR decline"]),
    ("Blood creatinine increased", "Investigations", 0.01, 0.0009, ["Creatinine increased", "Raised creatinine"]),
    ("Acute kidney injury", "Renal and urinary disorders", 0.012, 0.0004, ["Acute kidney injury", "AKI"]),
]
HOLD_AE = [("Pneumonia", "Infections and infestations", ["Pneumonia", "Community acquired pneumonia"]),
           ("Gastroenteritis", "Infections and infestations", ["Gastroenteritis", "Stomach flu"]),
           ("Dehydration", "Metabolism and nutrition disorders", ["Dehydration"]),
           ("Acute kidney injury", "Renal and urinary disorders", ["Acute kidney injury", "AKI"]),
           ("Hypotension", "Vascular disorders", ["Hypotension", "Symptomatic hypotension"])]


def _sev(k):
    return "MILD" if k <= 6.0 else ("MODERATE" if k <= 6.5 else "SEVERE")


def adverse_events(rng, Wd, lab_hi):
    """lab_hi: per patient, the on-treatment serum potassium values above 5.5 (date, value) from every laboratory"""
    pats, cs, info = Wd["pats"], Wd["cs"], Wd["info"]
    pi = pats.set_index("SUBJID")
    ev = []                      # (subj, group, rows) with rows [(start, end, sev, acn)]
    hk = {a: [] for a in P.ARMS}
    for s in sorted(cs):
        c = cs[s]
        vals = sorted(lab_hi.get(s, []))
        if not vals:
            continue
        eps, cur = [], [vals[0]]
        for x in vals[1:]:
            if (x[0] - cur[-1][0]).days <= 21:
                cur.append(x)
            else:
                eps.append(cur)
                cur = [x]
        eps.append(cur)
        allk = sorted((r["date"], r["k"]) for r in Wd["krec"][s] if not r["haem"])
        for e in eps:
            mk = max(k for _, k in e)
            prob = 1.0 if mk > 6.0 else (0.6 if mk >= 5.8 else 0.25)
            if rng.random() >= prob:
                continue
            pt = "Hyperkalaemia" if rng.random() < 0.72 else "Blood potassium increased"
            segs = []
            for dt, k in e:
                sv = _sev(k)
                if not segs or segs[-1][2] != sv:
                    segs.append([dt, None, sv, "DOSE NOT CHANGED"])
            later = [dt for dt, k in allk if dt > e[-1][0] and k <= 5.5]
            end = later[0] if later else e[-1][0] + timedelta(days=int(rng.integers(7, 22)))
            for i in range(len(segs)):
                segs[i][1] = segs[i + 1][0] - timedelta(days=1) if i + 1 < len(segs) else end
            if c.dose:
                for i, sg in enumerate(segs):
                    held = [a for a, b in c.off if b is not None and sg[0] <= sday(c, a) <= sg[1] + timedelta(days=1)]
                    stopped = c.stopped_for_good() and info[s]["stop_reason"] == "ADVERSE EVENT (POTASSIUM)" and \
                        sg[0] <= sday(c, c.stop_day()) <= sg[1] + timedelta(days=1)
                    if stopped:
                        sg[3] = "DRUG WITHDRAWN"
                    elif held:
                        sg[3] = "DRUG INTERRUPTED"
            ev.append({"s": s, "pt": pt, "rows": segs, "kind": "hyperk", "mk": mk})
            hk[c.arm].append(ev[-1])
    # an arm with no hyperkalaemia event reported keeps its patient with the highest value as one
    for arm in P.ARMS:
        if hk[arm]:
            continue
        best = max(((max(k for _, k in lab_hi[s]), s) for s in lab_hi if lab_hi[s] and cs[s].arm == arm), default=None)
        if best is None:
            continue
        s = best[1]
        dt0 = min(dt for dt, k in lab_hi[s])
        e = {"s": s, "pt": "Hyperkalaemia", "rows": [[dt0, dt0 + timedelta(days=int(rng.integers(8, 20))), "MILD", "DOSE NOT CHANGED"]],
             "kind": "hyperk", "mk": best[0]}
        ev.append(e)
        hk[arm].append(e)
    # every arm carries an event whose severity the investigator changed, recorded as a second row of the event
    for arm in P.ARMS:
        if not hk[arm] or any(len(e["rows"]) > 1 for e in hk[arm]):
            continue
        e = max(hk[arm], key=lambda x: (x["mk"], x["s"]))
        a, b, sv, acn = e["rows"][0]
        if (b - a).days < 4:
            b = a + timedelta(days=int(rng.integers(6, 14)))
        mid = a + timedelta(days=max(1, (b - a).days // 3))
        nxt = "MODERATE" if sv == "MILD" else "MILD"
        e["rows"] = [[a, mid - timedelta(days=1), sv, acn], [mid, b, nxt, "DOSE NOT CHANGED"]]
    # three events of raised potassium before the first dose (screening period), never treatment-emergent
    pre_ids = []
    for arm in ["Placebo", "VMK-4410 20 mg", "VMK-4410 40 mg"]:
        cand = pats[(pats["ARM"] == arm)].sort_values("K0", ascending=False)["SUBJID"].tolist()
        pre_ids.append(cand[int(rng.integers(0, 6))])
    for s in pre_ids:
        p = pi.loc[s]
        a = p["SCRDT"] + timedelta(days=int(rng.integers(2, 6)))
        b = min(a + timedelta(days=int(rng.integers(3, 8))), p["RANDDT"] - timedelta(days=1))
        ev.append({"s": s, "pt": "Hyperkalaemia", "rows": [[a, b, "MILD", "NOT APPLICABLE"]], "kind": "pre", "mk": 5.6})
    # events behind the temporary holds and the other stops for good
    for s in sorted(cs):
        c = cs[s]
        for a, b in info[s]["holds"]:
            pt, soc, verb = HOLD_AE[int(rng.integers(0, len(HOLD_AE)))]
            st = sday(c, a - 1)
            ev.append({"s": s, "pt": pt, "soc": soc, "verb": verb, "rows": [[st, sday(c, b - 2), "MODERATE", "DRUG INTERRUPTED"]],
                       "kind": "other", "mk": 0})
        if info[s]["stop_reason"] == "ADVERSE EVENT":
            pt, soc, verb = [("Dizziness", "Nervous system disorders", ["Dizziness"]), ("Hypotension", "Vascular disorders", ["Hypotension"]),
                             ("Fatigue", "General disorders and administration site conditions", ["Fatigue"])][int(rng.integers(0, 3))]
            st = sday(c, c.stop_day() - int(rng.integers(1, 5)))
            ev.append({"s": s, "pt": pt, "soc": soc, "verb": verb, "rows": [[st, st + timedelta(days=int(rng.integers(10, 40))), "MODERATE",
                                                                                "DRUG WITHDRAWN"]], "kind": "other", "mk": 0})
    # background events over each patient's time in the study
    for s in sorted(cs):
        c = cs[s]
        p = pi.loc[s]
        t0 = p["SCRDT"]
        t1 = c.vd["WEEK 56 FOLLOW-UP"] if s not in Wd["leave"] else sday(c, Wd["leave"][s])
        yrs = max((t1 - t0).days, 1) / 365.25
        for pt, soc, rate, per_mg, verb in OTHER:
            lam = (rate + per_mg * c.dose) * yrs
            for _ in range(int(rng.poisson(lam))):
                st = t0 + timedelta(days=int(rng.integers(0, max((t1 - t0).days, 1))))
                dur = int(rng.integers(2, 45))
                sv = str(rng.choice(["MILD", "MODERATE", "SEVERE"], p=[0.64, 0.31, 0.05]))
                rows = [[st, st + timedelta(days=dur), sv, "DOSE NOT CHANGED"]]
                if rng.random() < 0.06 and dur > 6:
                    mid = st + timedelta(days=dur // 2)
                    nxt = "MODERATE" if sv == "MILD" else "MILD"
                    rows = [[st, mid - timedelta(days=1), sv, "DOSE NOT CHANGED"], [mid, st + timedelta(days=dur), nxt, "DOSE NOT CHANGED"]]
                ev.append({"s": s, "pt": pt, "soc": soc, "verb": verb, "rows": rows, "kind": "other", "mk": 0})
    return _ae_table(rng, Wd, ev)


def _ae_table(rng, Wd, ev):
    cs = Wd["cs"]
    rows = []
    grp = {}
    for e in sorted(ev, key=lambda x: (x["s"], x["rows"][0][0], x["pt"])):
        s = e["s"]
        c = cs[s]
        grp[s] = grp.get(s, 0) + 1
        g = grp[s]
        if e["kind"] in ("hyperk", "pre"):
            verb = HYPERK_VERB[e["pt"]][int(rng.integers(0, len(HYPERK_VERB[e["pt"]])))]
            soc = SOC[e["pt"]]
        else:
            verb = e["verb"][int(rng.integers(0, len(e["verb"])))]
            soc = e["soc"]
        rel = "RELATED" if (c.dose and rng.random() < 0.55) or (not c.dose and rng.random() < 0.3) else "NOT RELATED"
        if e["kind"] == "other" and rng.random() < 0.7:
            rel = "NOT RELATED"
        if e["kind"] == "pre":
            rel = "NOT APPLICABLE"
        first_dose = c.rand
        last = sday(c, c.last_dose())
        end_study = c.vd["WEEK 56 FOLLOW-UP"] if s not in Wd["leave"] else sday(c, Wd["leave"][s])
        for i, (a, b, sv, acn) in enumerate(e["rows"]):
            if acn == "DOSE NOT CHANGED" and (a < first_dose or a > last):
                acn = "NOT APPLICABLE"
            ser = "Y" if sv == "SEVERE" and rng.random() < 0.5 else "N"
            ongoing = b > end_study
            stc = a.isoformat()
            # a few onset dates recorded to the month only, never in the month of the first or last dose
            if rng.random() < 0.045 and (a.year, a.month) not in ((first_dose.year, first_dose.month), (last.year, last.month)) \
                    and e["kind"] != "pre" and a > first_dose + timedelta(days=40):
                stc = a.strftime("%Y-%m")
            rows.append({"STUDYID": STUDY, "USUBJID": usubjid(s), "AEGRPID": g, "AETERM": verb, "AEDECOD": e["pt"],
                         "AEBODSYS": soc, "AESEV": sv, "AESER": ser, "AEREL": rel, "AEACN": acn,
                         "AEOUT": "NOT RECOVERED/NOT RESOLVED" if ongoing else ("RECOVERING/RESOLVING" if i + 1 < len(e["rows"]) else "RECOVERED/RESOLVED"),
                         "AESTDTC": stc, "AEENDTC": "" if ongoing else b.isoformat(), "_A": a})
    ae = pd.DataFrame(rows).sort_values(["USUBJID", "_A", "AEGRPID"], kind="mergesort").drop(columns="_A").reset_index(drop=True)
    ae.insert(2, "AESEQ", ae.groupby("USUBJID").cumcount() + 1)
    return ae


# ------------------------------------------------------------------------------------------------ medications
LOCAL_NAME = {
    "FUROSEMIDE": {"DK": "Furosemid", "SE": "Furosemid", "DE": "Furosemid", "PL": "Furosemid", "ES": "Furosemida", "GB": "Furosemide"},
    "TORASEMIDE": {"DK": "Torasemid", "SE": "Torasemid", "DE": "Torasemid", "PL": "Torasemid", "ES": "Torasemida", "GB": "Torasemide"},
    "BUMETANIDE": {"DK": "Bumetanid", "SE": "Bumetanid", "DE": "Bumetanid", "PL": "Bumetanid", "ES": "Bumetanida", "GB": "Bumetanide"},
}
LOOP = {"FUROSEMIDE": [20, 40, 40, 80, 80, 120], "TORASEMIDE": [5, 10, 10, 20], "BUMETANIDE": [1, 1, 2]}
ACEI = [("RAMIPRIL", 10, "QD"), ("LISINOPRIL", 20, "QD"), ("ENALAPRIL", 20, "BID"), ("PERINDOPRIL", 8, "QD")]
ARB = [("LOSARTAN", 100, "QD"), ("VALSARTAN", 160, "BID"), ("IRBESARTAN", 300, "QD"), ("CANDESARTAN", 32, "QD"), ("TELMISARTAN", 80, "QD")]
CLAS = {"FUROSEMIDE": ("SULFONAMIDES, PLAIN", "C03CA"), "TORASEMIDE": ("SULFONAMIDES, PLAIN", "C03CA"),
        "BUMETANIDE": ("SULFONAMIDES, PLAIN", "C03CA"), "RAMIPRIL": ("ACE INHIBITORS, PLAIN", "C09AA"),
        "LISINOPRIL": ("ACE INHIBITORS, PLAIN", "C09AA"), "ENALAPRIL": ("ACE INHIBITORS, PLAIN", "C09AA"),
        "PERINDOPRIL": ("ACE INHIBITORS, PLAIN", "C09AA"), "LOSARTAN": ("ANGIOTENSIN II RECEPTOR BLOCKERS (ARBS), PLAIN", "C09CA"),
        "VALSARTAN": ("ANGIOTENSIN II RECEPTOR BLOCKERS (ARBS), PLAIN", "C09CA"), "IRBESARTAN": ("ANGIOTENSIN II RECEPTOR BLOCKERS (ARBS), PLAIN", "C09CA"),
        "CANDESARTAN": ("ANGIOTENSIN II RECEPTOR BLOCKERS (ARBS), PLAIN", "C09CA"), "TELMISARTAN": ("ANGIOTENSIN II RECEPTOR BLOCKERS (ARBS), PLAIN", "C09CA"),
        "DAPAGLIFLOZIN": ("SODIUM-GLUCOSE CO-TRANSPORTER 2 (SGLT2) INHIBITORS", "A10BK"), "EMPAGLIFLOZIN": ("SODIUM-GLUCOSE CO-TRANSPORTER 2 (SGLT2) INHIBITORS", "A10BK"),
        "HYDROCHLOROTHIAZIDE": ("THIAZIDES, PLAIN", "C03AA"), "INDAPAMIDE": ("SULFONAMIDES, PLAIN", "C03BA"),
        "ATORVASTATIN": ("HMG COA REDUCTASE INHIBITORS", "C10AA"), "ROSUVASTATIN": ("HMG COA REDUCTASE INHIBITORS", "C10AA"),
        "SIMVASTATIN": ("HMG COA REDUCTASE INHIBITORS", "C10AA"), "METFORMIN": ("BIGUANIDES", "A10BA"),
        "INSULIN GLARGINE": ("INSULINS AND ANALOGUES FOR INJECTION, LONG-ACTING", "A10AE"),
        "SEMAGLUTIDE": ("GLUCAGON-LIKE PEPTIDE-1 (GLP-1) ANALOGUES", "A10BJ"), "LINAGLIPTIN": ("DIPEPTIDYL PEPTIDASE 4 (DPP-4) INHIBITORS", "A10BH"),
        "AMLODIPINE": ("DIHYDROPYRIDINE DERIVATIVES", "C08CA"), "BISOPROLOL": ("BETA BLOCKING AGENTS, SELECTIVE", "C07AB"),
        "METOPROLOL": ("BETA BLOCKING AGENTS, SELECTIVE", "C07AB"), "ALLOPURINOL": ("PREPARATIONS INHIBITING URIC ACID PRODUCTION", "M04AA"),
        "ACETYLSALICYLIC ACID": ("PLATELET AGGREGATION INHIBITORS EXCL. HEPARIN", "B01AC"), "PANTOPRAZOLE": ("PROTON PUMP INHIBITORS", "A02BC"),
        "OMEPRAZOLE": ("PROTON PUMP INHIBITORS", "A02BC"), "COLECALCIFEROL": ("VITAMIN D AND ANALOGUES", "A11CC"),
        "SODIUM BICARBONATE": ("ALKALIZING AGENTS", "B05XA"), "PATIROMER": ("DRUGS FOR TREATMENT OF HYPERKALEMIA AND HYPERPHOSPHATEMIA", "V03AE"),
        "SODIUM ZIRCONIUM CYCLOSILICATE": ("DRUGS FOR TREATMENT OF HYPERKALEMIA AND HYPERPHOSPHATEMIA", "V03AE"),
        "PARACETAMOL": ("ANILIDES", "N02BE"), "NITROFURANTOIN": ("NITROFURAN DERIVATIVES", "J01XE"), "AMOXICILLIN": ("PENICILLINS WITH EXTENDED SPECTRUM", "J01CA")}
BACKGROUND = [("ATORVASTATIN", 0.40, 40, "mg", "QD", "HYPERCHOLESTEROLAEMIA"), ("ROSUVASTATIN", 0.25, 10, "mg", "QD", "DYSLIPIDAEMIA"),
              ("SIMVASTATIN", 0.08, 40, "mg", "QD", "HYPERCHOLESTEROLAEMIA"), ("AMLODIPINE", 0.45, 5, "mg", "QD", "HYPERTENSION"),
              ("BISOPROLOL", 0.22, 5, "mg", "QD", "HYPERTENSION"), ("METOPROLOL", 0.12, 50, "mg", "QD", "ATRIAL FIBRILLATION"),
              ("ALLOPURINOL", 0.20, 100, "mg", "QD", "GOUT"), ("ACETYLSALICYLIC ACID", 0.35, 75, "mg", "QD", "CARDIOVASCULAR PROPHYLAXIS"),
              ("PANTOPRAZOLE", 0.15, 40, "mg", "QD", "GASTRIC PROTECTION"), ("OMEPRAZOLE", 0.10, 20, "mg", "QD", "REFLUX"),
              ("COLECALCIFEROL", 0.30, 1000, "IU", "QD", "VITAMIN D DEFICIENCY"), ("SODIUM BICARBONATE", 0.10, 500, "mg", "BID", "METABOLIC ACIDOSIS"),
              ("HYDROCHLOROTHIAZIDE", 0.08, 25, "mg", "QD", "HYPERTENSION"), ("INDAPAMIDE", 0.06, 1.5, "mg", "QD", "HYPERTENSION")]
DIAB_MEDS = [("METFORMIN", 0.55, 1000, "mg", "BID", "TYPE 2 DIABETES MELLITUS"), ("INSULIN GLARGINE", 0.35, 24, "IU", "QD", "TYPE 2 DIABETES MELLITUS"),
             ("SEMAGLUTIDE", 0.25, 1, "mg", "QW", "TYPE 2 DIABETES MELLITUS"), ("LINAGLIPTIN", 0.20, 5, "mg", "QD", "TYPE 2 DIABETES MELLITUS")]


def _verbatim(rng, name, cc):
    if name in LOCAL_NAME:
        v = LOCAL_NAME[name][cc]
    else:
        v = name.capitalize() if rng.random() < 0.6 else name
    r = rng.random()
    if r < 0.15:
        v = v.upper()
    elif r < 0.25:
        v = v.lower()
    return v


def _hist_start(rng, consent):
    y = consent.year - int(rng.integers(0, 9))
    r = rng.random()
    if r < 0.35:
        return str(y)
    m = int(rng.integers(1, 13))
    if y == consent.year and m >= consent.month:
        m = max(1, consent.month - 1)
    if r < 0.75:
        return "%d-%02d" % (y, m)
    return date(y, m, int(rng.integers(1, 28))).isoformat()


def medications(rng, Wd, ae, cons):
    pats, cs = Wd["pats"], Wd["cs"]
    rows = []

    def add(s, cc, name, dose, unit, frq, indc, st, en, txt=""):
        cl, cd = CLAS[name]
        rows.append({"STUDYID": STUDY, "USUBJID": usubjid(s), "CMTRT": _verbatim(rng, name, cc), "CMDECOD": name,
                     "CMCLAS": cl, "CMCLASCD": cd, "CMINDC": indc, "CMDOSE": dose if not txt else None, "CMDOSTXT": txt,
                     "CMDOSU": unit if not txt else "", "CMDOSFRQ": frq if not txt else "", "CMROUTE": "ORAL" if unit != "IU" or name == "COLECALCIFEROL" else "SUBCUTANEOUS",
                     "CMSTDTC": st, "CMENDTC": en, "CMENRF": "ONGOING" if en == "" else ""})

    for _, p in pats.iterrows():
        s, cc = p["SUBJID"], p["COUNTRY"]
        c = cs[s]
        con = cons[s]
        # RAS blocker at its maximum tolerated dose, unchanged
        nm, ds, fq = (ACEI if p["RAS"] == "ACEI" else ARB)[int(rng.integers(0, 4 if p["RAS"] == "ACEI" else 5))]
        add(s, cc, nm, ds, "mg", fq, "CHRONIC KIDNEY DISEASE" if rng.random() < 0.6 else "HYPERTENSION", _hist_start(rng, con), "")
        if p["SGLT2"]:
            nm = "DAPAGLIFLOZIN" if rng.random() < 0.55 else "EMPAGLIFLOZIN"
            add(s, cc, nm, 10, "mg", "QD", "CHRONIC KIDNEY DISEASE" if rng.random() < 0.7 else "TYPE 2 DIABETES MELLITUS",
                _hist_start(rng, con), "")
        if p["LOOP"]:
            nm = str(rng.choice(["FUROSEMIDE", "TORASEMIDE", "BUMETANIDE"], p=[0.62, 0.28, 0.10]))
            dose = float(rng.choice(LOOP[nm]))
            indc = str(rng.choice(["OEDEMA", "FLUID RETENTION", "HYPERTENSION"], p=[0.5, 0.3, 0.2]))
            changes = []
            if c.ease_day is not None:
                changes.append((c.ease_day, "down"))
            for dd_, size in c.extra:
                changes.append((dd_, "down" if size > 0 else "up"))
            changes.sort()
            st = _hist_start(rng, con)
            for day_c, way in changes:
                when = sday(c, day_c)
                new = dose / 2.0 if way == "down" else min(dose * 2.0, max(LOOP[nm]) * 2)
                if nm == "FUROSEMIDE" and way == "down" and dose <= 20:
                    new = 0.0
                if nm == "BUMETANIDE" and way == "down" and dose <= 1:
                    new = 0.0
                if nm == "TORASEMIDE" and way == "down" and dose <= 5:
                    new = 0.0
                txt = ""
                if nm == "FUROSEMIDE" and dose in (80, 120) and rng.random() < 0.3:
                    txt = "%d mg morning, %d mg midday" % (dose * 2 // 3, dose - dose * 2 // 3)
                add(s, cc, nm, _fmt_dose(dose), "mg", "QD", indc, st, (when - timedelta(days=1)).isoformat(), txt)
                if new == 0:
                    dose = 0
                    break
                dose = new
                st = when.isoformat()
            if dose:
                txt = ""
                if nm == "FUROSEMIDE" and dose in (80, 120) and rng.random() < 0.3:
                    txt = "%d mg morning, %d mg midday" % (dose * 2 // 3, dose - dose * 2 // 3)
                add(s, cc, nm, _fmt_dose(dose), "mg", "QD", indc, st, "", txt)
        for nm, pr, ds, un, fq, indc in BACKGROUND:
            if rng.random() < pr:
                add(s, cc, nm, ds, un, fq, indc, _hist_start(rng, con), "")
        if p["DIAB"]:
            for nm, pr, ds, un, fq, indc in DIAB_MEDS:
                if rng.random() < pr:
                    add(s, cc, nm, ds, un, fq, indc, _hist_start(rng, con), "")
    # potassium binders started at a hyperkalaemia event, and short courses for other events
    hk = ae[ae["AEDECOD"].isin(["Hyperkalaemia", "Blood potassium increased"])]
    for g, e in hk.groupby(["USUBJID", "AEGRPID"]):
        u = g[0]
        s = u[len(STUDY) + 1:]
        if s not in cs or rng.random() > 0.45:
            continue
        cc = pats.set_index("SUBJID").loc[s, "COUNTRY"]
        a = date.fromisoformat(e["AESTDTC"].iloc[0]) if len(e["AESTDTC"].iloc[0]) == 10 else None
        if a is None:
            continue
        nm = "PATIROMER" if rng.random() < 0.5 else "SODIUM ZIRCONIUM CYCLOSILICATE"
        add(s, cc, nm, 8.4 if nm == "PATIROMER" else 10, "g", "QD", "HYPERKALAEMIA", (a + timedelta(days=int(rng.integers(0, 3)))).isoformat(),
            (a + timedelta(days=int(rng.integers(14, 60)))).isoformat())
    for _, e in ae[ae["AEDECOD"].isin(["Urinary tract infection", "Pneumonia"])].iterrows():
        s = e["USUBJID"][len(STUDY) + 1:]
        if len(e["AESTDTC"]) != 10 or rng.random() > 0.8:
            continue
        cc = pats.set_index("SUBJID").loc[s, "COUNTRY"]
        a = date.fromisoformat(e["AESTDTC"])
        nm = "NITROFURANTOIN" if e["AEDECOD"] == "Urinary tract infection" else "AMOXICILLIN"
        add(s, cc, nm, 50 if nm == "NITROFURANTOIN" else 500, "mg", "QID" if nm == "NITROFURANTOIN" else "TID",
            e["AEDECOD"].upper(), a.isoformat(), (a + timedelta(days=int(rng.integers(5, 8)))).isoformat())
    for _, e in ae[ae["AEDECOD"].isin(["Headache", "Back pain", "Arthralgia"])].iterrows():
        s = e["USUBJID"][len(STUDY) + 1:]
        if len(e["AESTDTC"]) != 10 or rng.random() > 0.5:
            continue
        cc = pats.set_index("SUBJID").loc[s, "COUNTRY"]
        a = date.fromisoformat(e["AESTDTC"])
        add(s, cc, "PARACETAMOL", 1000, "mg", "PRN", e["AEDECOD"].upper(), a.isoformat(), (a + timedelta(days=int(rng.integers(3, 20)))).isoformat())
    cm = pd.DataFrame(rows)
    cm["_K"] = cm["CMSTDTC"].str.pad(10, side="right", fillchar="0")
    cm = cm.sort_values(["USUBJID", "_K", "CMDECOD"], kind="mergesort").drop(columns="_K").reset_index(drop=True)
    cm.insert(2, "CMSEQ", cm.groupby("USUBJID").cumcount() + 1)
    return cm


def _fmt_dose(x):
    return int(x) if float(x).is_integer() else float(x)


# ------------------------------------------------------------------------------------------------ vital signs
BP_EFF = {0: 0.0, 5: 2.2, 10: 3.6, 20: 6.1, 40: 8.4}


def vital_signs(rng, Wd):
    pats, fails, cs = Wd["pats"], Wd["fails"], Wd["cs"]
    rows = []
    for _, p in fails.iterrows():
        h = round(float(rng.normal(176 if p["SEX"] == "M" else 163, 7)), 0)
        w = round(float(np.clip(rng.normal(30.5, 5), 20, 46) * (h / 100) ** 2), 1)
        for cd, val, u in (("SYSBP", int(rng.normal(137, 13)), "mmHg"), ("DIABP", int(rng.normal(78, 9)), "mmHg"),
                           ("PULSE", int(rng.normal(72, 10)), "beats/min"), ("WEIGHT", w, "kg"), ("HEIGHT", int(h), "cm")):
            rows.append((p["SUBJID"], cd, val, u, "SCREENING", 1, p["SCRDT"]))
    for _, p in pats.iterrows():
        s = p["SUBJID"]
        c = cs[s]
        for v in S.attended(Wd["vds"], Wd["leave"], Wd["missed"], s):
            dt = Wd["vds"][s][v]
            day = S.day_of(dt, c.rand)
            st = c.state(day) if c.dose else 0.0
            sbp = p["SBP0"] - BP_EFF[c.dose] * st + rng.normal(0, 8.5)
            dbp = p["DBP0"] - 0.5 * BP_EFF[c.dose] * st + rng.normal(0, 6)
            wt = p["WEIGHT0"] + rng.normal(0, 0.7) + 0.4 * day / 365.25
            if c.dose and p["LOOP"]:
                wt -= (0.3 + 0.025 * c.dose) * st
                if c.ease_day is not None and day > c.ease_day:
                    wt += 0.5 * (1 - np.exp(-((day - c.ease_day) / 7.0) / P.REC_TAU_W))
            vn = [n for vv, n, dd, w in P.VISITS if vv == v][0]
            rows.append((s, "SYSBP", int(round(sbp)), "mmHg", v, vn, dt))
            rows.append((s, "DIABP", int(round(dbp)), "mmHg", v, vn, dt))
            rows.append((s, "PULSE", int(round(rng.normal(71, 9))), "beats/min", v, vn, dt))
            rows.append((s, "WEIGHT", round(float(wt), 1), "kg", v, vn, dt))
            if v == "SCREENING":
                rows.append((s, "HEIGHT", int(p["HEIGHT"]), "cm", v, vn, dt))
    names = {"SYSBP": "Systolic Blood Pressure", "DIABP": "Diastolic Blood Pressure", "PULSE": "Pulse Rate", "WEIGHT": "Weight",
             "HEIGHT": "Height"}
    vs = pd.DataFrame(rows, columns=["SUBJID", "VSTESTCD", "VAL", "VSORRESU", "VISIT", "VISITNUM", "DT"])
    out = pd.DataFrame({"STUDYID": STUDY, "USUBJID": vs["SUBJID"].map(usubjid)})
    out["VSTESTCD"] = vs["VSTESTCD"]
    out["VSTEST"] = vs["VSTESTCD"].map(names)
    out["VSPOS"] = np.where(vs["VSTESTCD"].isin(["SYSBP", "DIABP", "PULSE"]), "SITTING", "")
    out["VSORRES"] = vs["VAL"].astype(str)
    out["VSORRESU"] = vs["VSORRESU"]
    out["VSSTRESN"] = vs["VAL"].astype(float)
    out["VSSTRESU"] = vs["VSORRESU"]
    out["VISITNUM"] = vs["VISITNUM"]
    out["VISIT"] = vs["VISIT"]
    out["VSDTC"] = vs["DT"].map(d)
    out = out.sort_values(["USUBJID", "VSDTC", "VSTESTCD"], kind="mergesort").reset_index(drop=True)
    out.insert(2, "VSSEQ", out.groupby("USUBJID").cumcount() + 1)
    return out


# ------------------------------------------------------------------------------------------------ trough concentrations
def concentrations(rng, Wd):
    pats, cs = Wd["pats"], Wd["cs"]
    rows = []
    for _, p in pats.iterrows():
        s = p["SUBJID"]
        c = cs[s]
        att = S.attended(Wd["vds"], Wd["leave"], Wd["missed"], s)
        for v in ("WEEK 4", "WEEK 12", "WEEK 24", "WEEK 52"):
            if v not in att:
                continue
            dt = Wd["vds"][s][v]
            day = S.day_of(dt, c.rand)
            if not c.on(day - 1) and c.dose:
                continue
            if rng.random() < 0.03:
                rows.append((s, "", "", None, "NOT DONE", v, dt))
                continue
            if c.dose == 0:
                rows.append((s, "<0.50", "ng/mL", None, "", v, dt))
            else:
                conc = 2.1 * c.dose * float(np.exp(rng.normal(0, 0.45)))
                rows.append((s, "%.2f" % conc if conc < 100 else "%.1f" % conc, "ng/mL", round(conc, 2), "", v, dt))
    pc = pd.DataFrame(rows, columns=["SUBJID", "PCORRES", "PCORRESU", "PCSTRESN", "PCSTAT", "VISIT", "DT"])
    out = pd.DataFrame({"STUDYID": STUDY, "USUBJID": pc["SUBJID"].map(usubjid)})
    out["PCTESTCD"] = "VMK4410"
    out["PCTEST"] = "VMK-4410"
    out["PCSPEC"] = "PLASMA"
    out["PCTPT"] = "PRE-DOSE"
    out["PCORRES"] = pc["PCORRES"]
    out["PCORRESU"] = pc["PCORRESU"]
    out["PCSTRESN"] = pc["PCSTRESN"]
    out["PCSTRESU"] = np.where(pc["PCORRES"] != "", "ng/mL", "")
    out["PCLLOQ"] = 0.5
    out["PCSTAT"] = pc["PCSTAT"]
    out["VISIT"] = pc["VISIT"]
    out["PCDTC"] = pc["DT"].map(d)
    out = out.sort_values(["USUBJID", "PCDTC"], kind="mergesort").reset_index(drop=True)
    out.insert(2, "PCSEQ", out.groupby("USUBJID").cumcount() + 1)
    return out
