"""The pack's tables, as the files carry them (dates as dates, before formatting)."""
import datetime as dt

import world as W
import records as R

DIAG_DESC = {
    "C34.90": "Malignant neoplasm of unspecified part of unspecified bronchus or lung",
    "C34.11": "Malignant neoplasm of upper lobe, right bronchus or lung",
    "C50.919": "Malignant neoplasm of unspecified site of unspecified female breast",
    "C61": "Malignant neoplasm of prostate", "C18.9": "Malignant neoplasm of colon, unspecified",
    "C25.9": "Malignant neoplasm of pancreas, unspecified", "C22.0": "Liver cell carcinoma",
    "C71.9": "Malignant neoplasm of brain, unspecified", "C16.9": "Malignant neoplasm of stomach, unspecified",
    "C56.9": "Malignant neoplasm of unspecified ovary", "C67.9": "Malignant neoplasm of bladder, unspecified",
    "C91.10": "Chronic lymphocytic leukemia of B-cell type not having achieved remission",
    "C92.00": "Acute myeloblastic leukemia, not having achieved remission",
    "C80.1": "Malignant (primary) neoplasm, unspecified", "C64.9": "Malignant neoplasm of unspecified kidney, except renal pelvis",
    "C15.9": "Malignant neoplasm of esophagus, unspecified",
    "G30.9": "Alzheimer's disease, unspecified", "G30.1": "Alzheimer's disease with late onset",
    "G31.1": "Senile degeneration of brain, not elsewhere classified", "G31.83": "Neurocognitive disorder with Lewy bodies",
    "G31.09": "Other frontotemporal neurocognitive disorder", "G30.8": "Other Alzheimer's disease",
    "G31.84": "Mild cognitive impairment of uncertain or unknown etiology",
    "I50.9": "Heart failure, unspecified", "I50.22": "Chronic systolic (congestive) heart failure",
    "I50.32": "Chronic diastolic (congestive) heart failure",
    "I50.42": "Chronic combined systolic (congestive) and diastolic (congestive) heart failure",
    "I11.0": "Hypertensive heart disease with heart failure",
    "I13.0": "Hypertensive heart and chronic kidney disease with heart failure and stage 1 through stage 4 chronic kidney disease, or unspecified chronic kidney disease",
    "J44.9": "Chronic obstructive pulmonary disease, unspecified",
    "J44.1": "Chronic obstructive pulmonary disease with (acute) exacerbation",
    "J84.10": "Pulmonary fibrosis, unspecified", "J96.11": "Chronic respiratory failure with hypoxia",
    "I42.9": "Cardiomyopathy, unspecified",
    "I63.9": "Cerebral infarction, unspecified", "N18.6": "End stage renal disease",
    "K74.60": "Unspecified cirrhosis of liver", "G12.21": "Amyotrophic lateral sclerosis",
    "G20.A1": "Parkinson's disease without dyskinesia, without mention of fluctuations", "G35": "Multiple sclerosis",
    "I61.9": "Nontraumatic intracerebral hemorrhage, unspecified", "E43": "Unspecified severe protein-calorie malnutrition",
    "N18.5": "Chronic kidney disease, stage 5", "K72.10": "Chronic hepatic failure without coma",
    "I69.354": "Hemiplegia and hemiparesis following cerebral infarction affecting left non-dominant side",
    "G93.1": "Anoxic brain damage, not elsewhere classified", "J69.0": "Pneumonitis due to inhalation of food and vomit",
}


def extract_rows(people):
    """The benefit periods extract: one row per benefit period per hospice, with the beneficiary's date of death."""
    rows = []
    for b in people:
        dod = W.date_of(b.dod - 1) if (b.dod is not None and b.dod - 1 <= R.LAST_DAY) else None
        for num, prov, lo, hi, days, kind, elect in b.periods:
            if hi is None:
                end = None
            elif kind in ("period", "death"):
                end = W.date_of(hi - 1)
            else:
                end = W.date_of(hi)
            rows.append(dict(mbi=b.mbi, bp=num, elect=W.date_of(elect), ccn=prov, start=W.date_of(lo), end=end,
                             days=days, dod=dod))
    rows.sort(key=lambda r: (r["mbi"], r["bp"], r["start"]))
    return rows


def crosswalk_rows(people, emr, legacy):
    used = {r["medicare_id"] for r in emr} | {r["medicare_no"] for r in legacy}
    out = [dict(hicn=b.hicn, mbi=b.mbi) for b in people if b.hicn in used]
    return sorted(out, key=lambda r: r["hicn"])


def dx_rows():
    out = []
    for g, items in R.DX.items():
        for code, _ in items:
            out.append(dict(code=code, description=DIAG_DESC[code], group=W.GROUP_NAME[g]))
    return sorted(out, key=lambda r: r["code"])


def build(people):
    emr = R.emr_rows(people) + R.other_payer_rows(people)
    emr.sort(key=lambda r: (r["admit_date"], r["provider_number"], r["mrn"]))
    for k, r in enumerate(emr):
        r["episode_id"] = "A%08d" % (10000000 + k * 3)
    legacy = R.legacy_rows(people)
    legacy.sort(key=lambda r: (r["admit"], r["acct"]))
    return dict(extract=extract_rows(people), emr=emr, legacy=legacy,
                crosswalk=crosswalk_rows(people, emr, legacy), dx=dx_rows())
