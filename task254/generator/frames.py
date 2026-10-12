"""The safety tables as they leave the systems: string DataFrames, exactly as written to the files."""
import datetime as dt

import pandas as pd

import cases as K
import core as C
import world as W

TD = dt.timedelta
LOCK, EXPORT = W.LOCK, W.EXPORT
LISTING_COLS = ["case_no", "version_no", "version_receipt_date", "initial_receipt_date", "report_type", "primary_source",
                "country", "sex", "age_years", "therapy_start_date", "therapy_stop_date", "reaction_pt", "onset_date",
                "serious", "seriousness_criteria", "outcome", "outcome_date", "action_taken"]


def _d(v):
    return "" if v is None else v.isoformat()


def _start_str(case):
    s = case["rec"]["lines"][0]["start"]
    return "%04d-%02d" % (s.year, s.month) if case["start_partial"] else s.isoformat()


def listing(cases):
    rows = []
    for case in cases:
        lines = case["rec"]["lines"]
        nv = len(case["versions"])
        for vi, vr in enumerate(case["versions"]):
            stop = lines[-1]["stop"]
            stop_s = _d(stop) if (stop is not None and stop <= vr) else ""
            oc, od = K.outcome_at(case, vi)
            ser, crit = case["serious"], case["criteria"]
            if case.get("ser_upgrade") and vi == 0:
                ser, crit = "N", ""
            for i, rx in enumerate(case["rx"]):
                if rx["added"] > vi:
                    continue
                if case.get("rx_from", {}).get(i, 0) > vi:
                    continue
                main = rx.get("risk") is not None or i == 0
                rows.append([case["case_no"], str(vi + 1), vr.isoformat(), case["versions"][0].isoformat(),
                             case["report_type"], str(case["qual"]), case["market"], case["sex"],
                             "" if case["age"] is None else str(case["age"]), _start_str(case), stop_s, rx["pt"],
                             K.onset_string(case, i, vi), ser if main else "N", crit if main else "",
                             oc if main else ("RECOVERED" if oc == "RECOVERED" else oc), od if main else "",
                             case["rec"].get("action", "UNKNOWN")])
    df = pd.DataFrame(rows, columns=LISTING_COLS)
    return df.sort_values(["case_no", "version_no", "reaction_pt"], key=lambda s: s.astype(int) if s.name == "version_no" else s,
                          kind="mergesort").reset_index(drop=True)


def dosage(cases):
    rows = []
    for case in cases:
        rec = case["rec"]
        for j, ln in enumerate(rec["lines"]):
            st = ln["start"]
            st_s = ("%04d-%02d" % (st.year, st.month)) if (case["start_partial"] and j == 0) else st.isoformat()
            tab = case["qual"] == 5 or (case["report_type"] == "SO" and case["qual"] == 3 and j % 2 == 1)
            rows.append([case["case_no"], str(j + 1), st_s, _d(ln["stop"]), "1" if tab else str(ln["dose"]),
                         "tablet" if tab else "mg", str(ln["dose"]), ln["end"]])
    return pd.DataFrame(rows, columns=["case_no", "line_no", "start_date", "stop_date", "daily_dose", "dose_unit",
                                       "strength_mg", "line_end"])


def feed(cases):
    rows = []
    for case in cases:
        for (date, an, val, unit, lab) in case.get("samples", []):
            rows.append([case["psp_ref"], case["case_no"], date.isoformat(), an, val, unit, lab])
    df = pd.DataFrame(rows, columns=["psp_patient_ref", "case_no", "sample_date", "analyte", "value", "unit", "lab_code"])
    return df.sort_values(["psp_patient_ref", "sample_date", "analyte"], kind="mergesort").reset_index(drop=True)


def lab_register():
    rows = []
    for code, (name, ctry, _, alt_u, um, uf, n_u, fac, lln) in C.LABS.items():
        rows.append([code, name, ctry, "ALT", alt_u, "", _num(um), _num(uf), "2023-01-01"])
        nh = 7.5 * fac if fac != 1.0 else 7.5
        rows.append([code, name, ctry, "NEUT", n_u, _num(lln), _num(nh), _num(nh), "2023-01-01"])
        rows.append([code, name, ctry, "LYMPH", n_u, _num(1.0 * fac if fac != 1.0 else 1.0), _num(4.0 * fac if fac != 1.0 else 4.0),
                     _num(4.0 * fac if fac != 1.0 else 4.0), "2023-01-01"])
    return pd.DataFrame(rows, columns=["lab_code", "laboratory", "country", "analyte", "unit", "lln", "uln_male",
                                       "uln_female", "valid_from"])


def _num(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return ("%.2f" % v) if isinstance(v, float) else str(v)


def dup_register(dups):
    rows = []
    for d in dups:
        rows.append([d["master"]["case_no"], d["case_no"], d["linked_on"].isoformat(), d["link_reason"], "PV case processing"])
    df = pd.DataFrame(rows, columns=["master_case_no", "duplicate_case_no", "linked_on", "link_reason", "linked_by"])
    return df.sort_values(["linked_on", "master_case_no"], kind="mergesort").reset_index(drop=True)


SOC = {"ild": "Respiratory, thoracic and mediastinal disorders", "zoster": "Infections and infestations",
       "infection": "Infections and infestations", "vte": "Vascular disorders", "hepatic": "Hepatobiliary disorders",
       "neutropenia": "Blood and lymphatic system disorders"}
SOC_OVERRIDE = {"Alanine aminotransferase increased": "Investigations", "Aspartate aminotransferase increased": "Investigations",
                "Transaminases increased": "Investigations", "Hepatic enzyme increased": "Investigations",
                "Neutrophil count decreased": "Investigations", "Pulmonary embolism": "Respiratory, thoracic and mediastinal disorders",
                "Retinal vein occlusion": "Eye disorders", "Febrile neutropenia": "Blood and lymphatic system disorders"}
EXTRA_TERMS = {
    "ild": ["Lung infiltration", "Pulmonary toxicity", "Idiopathic interstitial pneumonia", "Pneumonitis chemical"],
    "zoster": ["Herpes zoster infection neurological", "Herpes zoster pharyngitis", "Herpes zoster reactivation"],
    "infection": ["Abscess limb", "Bacteraemia", "Endocarditis", "Meningitis", "Peritonitis", "Septic arthritis",
                  "Pneumonia viral", "Infective exacerbation of chronic obstructive airways disease", "Empyema",
                  "Post procedural infection", "Wound infection", "Pneumonia klebsiella", "Pneumonia pneumococcal",
                  "Staphylococcal bacteraemia", "Clostridium difficile colitis", "Infection", "Lung abscess"],
    "vte": ["Venous thrombosis", "Pelvic venous thrombosis", "Subclavian vein thrombosis", "Mesenteric vein thrombosis",
            "Pulmonary thrombosis", "Thrombophlebitis"],
    "hepatic": ["Liver injury", "Hepatic failure", "Hypertransaminasaemia", "Liver function test increased",
                "Hepatitis acute", "Cholestatic liver injury", "Jaundice"],
    "neutropenia": ["Neutropenic sepsis", "Granulocytopenia", "Neutropenic infection"],
}
POT_CONCERN = {"mace": "Major adverse cardiovascular events", "malig": "Malignancies excluding non-melanoma skin cancer",
               "nmsc": "Non-melanoma skin cancer", "tb": "Tuberculosis"}
POT_EXTRA = {"mace": ["Cardiac arrest", "Cardiac death", "Haemorrhagic stroke", "Stroke", "Myocardial ischaemia"],
             "malig": ["Pancreatic carcinoma", "Malignant melanoma", "Gastric cancer", "Renal cell carcinoma",
                       "Hepatocellular carcinoma", "Bladder cancer", "Ovarian cancer", "Plasma cell myeloma", "Leukaemia"],
             "nmsc": ["Bowen's disease", "Keratoacanthoma"], "tb": ["Tuberculosis", "Extrapulmonary tuberculosis",
                                                                     "Lymph node tuberculosis"]}
POT_SOC = {"mace": "Cardiac disorders", "malig": "Neoplasms benign, malignant and unspecified (incl cysts and polyps)",
           "nmsc": "Neoplasms benign, malignant and unspecified (incl cysts and polyps)", "tb": "Infections and infestations"}
NERVOUS = {"Ischaemic stroke", "Cerebrovascular accident", "Haemorrhagic stroke", "Stroke"}


def term_list():
    rows = []
    for r in W.RISKS:
        pts = [t for t, _ in C.TERMS[r]] + [t for t, _ in C.LAB_TERMS.get(r, [])] + EXTRA_TERMS[r]
        pts += [a for a, _ in C.V4_ADDED.get(r, [])]
        if r == "hepatic":
            pts.append("Aspartate aminotransferase increased")
        for t in sorted(set(pts)):
            rows.append([t, SOC_OVERRIDE.get(t, SOC[r]), W.RISK_LABEL[r], "Important identified risk"])
    for k, label in POT_CONCERN.items():
        pts = [p for p, kk, _ in K.POTENTIAL if kk == k] + POT_EXTRA[k]
        for t in sorted(set(pts)):
            soc = "Nervous system disorders" if t in NERVOUS else POT_SOC[k]
            rows.append([t, soc, label, "Important potential risk"])
    df = pd.DataFrame(rows, columns=["preferred_term", "meddra_soc", "safety_concern", "risk_category"])
    return df


def change_log():
    rows = []
    n = 1
    for r in ("zoster", "infection"):
        for t, parent in C.V4_ADDED[r]:
            rows.append(["C%02d" % n, t, W.RISK_LABEL[r], "Added", "2025-11-14",
                         "MedDRA %s coded beside %s in case processing; added so that the concern is retrieved by every "
                         "PT in use" % ("PT", parent)])
            n += 1
    rows.append(["C%02d" % n, "Squamous cell carcinoma of skin", POT_CONCERN["nmsc"], "Added", "2025-11-14",
                 "Aligned with the PRAC assessment of the PSUR 5 signal on skin cancer"])
    n += 1
    rows.append(["C%02d" % n, "Tuberculosis", POT_CONCERN["tb"], "Added", "2025-11-14",
                 "Non-specific PT added after the MedDRA 28.1 upgrade"])
    return pd.DataFrame(rows, columns=["change_no", "preferred_term", "safety_concern", "change", "effective_from", "rationale"])
