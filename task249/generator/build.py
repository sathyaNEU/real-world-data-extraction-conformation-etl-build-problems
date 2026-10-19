"""Write task249's target folder from the World and its Records."""
import datetime as dt
import os
import numpy as np
import pandas as pd
import params as P
import world as W
import records as R
import docs as D

FILES = {
    "attempts": "mat_r_attempts_2028.parquet",
    "exposure": "mat_r_exposure_2028.parquet",
    "bank": "mat_r_item_bank.csv",
    "register": "candidate_register_2028.csv",
    "shares": "results_shared_2028.csv",
    "shortlists": "shortlists_2028.csv",
    "cases": "integrity_cases_2028.xlsx",
    "study": "mat_v_equivalence_study_2028.csv",
    "report": "mat_v_equivalence_study_report.pdf",
    "standard": "MAL-IS-04_integrity_standard.pdf",
    "manual": "mat_technical_manual_ch4.pdf",
    "plans": "client_plans_2029.xlsx",
    "accounts": "client_accounts.csv",
    "colleges": "colleges.csv",
    "venues": "selection_venues_2029.csv",
    "feedback": "candidate_feedback_2028.csv",
    "dictionary": "DATA_DICTIONARY.md",
    "deliv_xlsx": "verification_bands_2029.xlsx",
    "deliv_pdf": "account_referral_note_2029.pdf",
}
DISTRACTORS = ["selection_venues_2029.csv", "candidate_feedback_2028.csv"]

_CACHE = {}


def world():
    if "w" not in _CACHE:
        w = W.World()
        _CACHE["w"] = w
        _CACHE["r"] = R.Records(w)
    return _CACHE["w"], _CACHE["r"]


def _parquet(df, path):
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.Table.from_pandas(df, preserve_index=False)
    t = t.replace_schema_metadata(None)
    pq.write_table(t, path, compression="zstd", use_dictionary=True, data_page_version="1.0", write_statistics=True)


def study_tables(df):
    d = df.dropna(subset=["mat_v_logit"]).copy()
    t0 = pd.to_datetime(d["mat_r_started_ist"]).dt.normalize()
    t1 = pd.to_datetime(d["mat_v_started_ist"]).dt.normalize()
    d["days"] = (t1 - t0).dt.days
    d["gain"] = d["mat_v_logit"] - d["mat_r_logit"]
    d["ref"] = d["mat_r_logit"] > d["mat_v_logit"] + P.BAND_Z * d["mat_v_se"]
    tab_gain = [[str(k), str(len(g)), "%+.3f" % g["gain"].mean()] for k, g in d.groupby("days")]
    bands = [("1 to 3", 1, 3), ("7 to 14", 4, 14), ("21 to 28", 15, 41), ("42 to 84", 42, 84)]
    tab_ref = []
    for lab, lo, hi in bands:
        g = d[(d["days"] >= lo) & (d["days"] <= hi)]
        tab_ref.append([lab, str(len(g)), str(int(g["ref"].sum())), "%.1f per cent" % (100 * g["ref"].mean())])
    r = float(np.corrcoef(d["mat_r_logit"], d["mat_v_logit"])[0, 1])
    return tab_gain, tab_ref, len(df), len(d), r


def colleges_frame(w):
    recs = [(c["short"], c["aishe"], c["tier"], c["state"], w.test_week[c["cid"]].isoformat(),
             "Y" if c["cid"] in set(w.study["partners"]) else "N") for c in w.colleges]
    return pd.DataFrame(recs, columns=["college_code", "aishe_code", "tier", "state", "test_week_2028", "study_partner"])


def accounts_frame():
    recs = []
    on = {"E": "2024-0%d-1%d", "M": "2023-0%d-2%d", "V": "2022-0%d-0%d"}
    r = np.random.default_rng(P.SEED + 5)
    for code, name, sector, grp, mix, f28, f29, q29 in P.ACCOUNTS:
        d = dt.date(2021 + int(r.integers(0, 6)), int(r.integers(1, 13)), int(r.integers(1, 28)))
        recs.append((code, name, sector, d.isoformat(), "active", ""))
    recs.append(("PGL", P.MERGED["PGL"][0], "lending", "2025-03-11", "merged",
                 "Merged into NVK (Navakar Fintech) on 2 September 2028; campus list moved to NVK"))
    df = pd.DataFrame(recs, columns=["account_code", "client_name", "sector", "onboarded", "status", "note"])
    return df.sort_values("account_code").reset_index(drop=True)


def venues_frame():
    r = np.random.default_rng(P.SEED + 9)
    rows = []
    for city, centres in (("Bengaluru", 3), ("Pune", 2), ("Hyderabad", 2), ("Chennai", 1), ("Gurugram", 1)):
        for k in range(centres):
            d0 = dt.date(2029, 8, 25) + dt.timedelta(days=int(r.integers(0, 21)))
            d1 = dt.date(2029, 12, 5) + dt.timedelta(days=int(r.integers(0, 24)))
            rows.append(("%s-%d" % (city[:3].upper(), k + 1), city, int(r.integers(24, 61)), int(r.choice([2, 3])),
                         d0.isoformat(), d1.isoformat(), str(r.choice(["Y", "Y", "N"]))))
    return pd.DataFrame(rows, columns=["venue_code", "city", "seats_per_session", "sessions_per_day", "available_from",
                                       "available_to", "step_free_access"])


def feedback_frame(rc):
    """the post-sitting survey: a sample of candidates who completed MAT-R; a candidate whose attempt was interrupted
    reports a technical problem more often"""
    r = np.random.default_rng(P.SEED + 13)
    w = rc.w
    first_dev, inter = {}, set()
    for a in rc.att:
        first_dev.setdefault(a["i"], a["dev"])
        if a["status"] == "interrupted":
            inter.add(a["i"])
    sit = np.array(sorted(first_dev))
    pick = r.choice(sit, 6100, replace=False)
    rows = []
    for i in pick:
        hit = i in inter
        tech = r.random() < (0.78 if hit else 0.11)
        if tech:
            pool = (["lost connection"] * 6 + ["slow loading", "timer unclear"]) if hit else \
                (["slow loading"] * 3 + ["timer unclear"] * 2 + ["lost connection"] + (["font small on tablet"] * 3 if first_dev[i] == "tablet" else []))
            theme = str(r.choice(pool))
        else:
            theme = str(r.choice(["", "", "", "", "timer unclear", "practice items too easy"]))
        rating = int(r.choice([1, 2, 3, 4, 5], p=[0.12, 0.2, 0.3, 0.26, 0.12] if tech else [0.03, 0.07, 0.19, 0.43, 0.28]))
        rows.append((rc.cand_id[i], rating, "yes" if tech else "no", theme))
    return pd.DataFrame(rows, columns=["candidate_id", "overall_rating", "technical_problem", "comment_theme"])


def run(target):
    w, rc = world()
    os.makedirs(target, exist_ok=True)
    pj = lambda k: os.path.join(target, FILES[k])
    _parquet(rc.attempts_frame(), pj("attempts"))
    _parquet(rc.exposure_frame(), pj("exposure"))
    rc.bank_frame().to_csv(pj("bank"), index=False)
    rc.register_frame().to_csv(pj("register"), index=False)
    rc.shares_frame().to_csv(pj("shares"), index=False)
    rc.shortlists_frame().to_csv(pj("shortlists"), index=False)
    cases = rc.cases_frame()
    with pd.ExcelWriter(pj("cases"), engine="openpyxl") as xw:
        cases.to_excel(xw, sheet_name="Case log", index=False)
    import postprocess
    postprocess.scrub(pj("cases"), P.FIRM, "2029-01-08T17:45:00")
    postprocess.finish_office(pj("cases"), "2028-07-14T10:00:00Z", "2029-01-08T17:45:00Z", P.FIRM)
    st = rc.study_frame()
    st.to_csv(pj("study"), index=False)
    D.study_report(pj("report"), *study_tables(st))
    D.standard(pj("standard"))
    D.manual(pj("manual"))
    D.plans(pj("plans"), w)
    accounts_frame().to_csv(pj("accounts"), index=False)
    colleges_frame(w).to_csv(pj("colleges"), index=False)
    venues_frame().to_csv(pj("venues"), index=False)
    feedback_frame(rc).to_csv(pj("feedback"), index=False)
    import dictionary
    dictionary.write(pj("dictionary"), FILES)
    return w, rc
