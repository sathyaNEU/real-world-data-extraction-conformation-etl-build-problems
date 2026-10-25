"""Write the bundle under target/: the main call's records, the ask files, the distractors and the documents."""
import os

import numpy as np
import pandas as pd

import asks as A
import docs as DC
import params as P
import postprocess
import records as RC

FILES = {
    "extract": "active_patients_2026-09-30.csv",
    "history": "smoking_status_history_2012-2026.parquet",
    "practices": "practices.csv",
    "log": "quit_outreach_calls_eastern_shore_2025.csv",
    "plan": "quit_outreach_plan_2027.docx",
    "dictionary": "data_dictionary_2026.docx",
    "quitline": "quitline_referrals_2023-2025.csv",
    "dialler": "dialler_legs_2025.csv",
    "profiles": "sub_region_profiles_2025.csv",
    "workforce": "gp_workforce_2025.xlsx",
    "medicines": "quit_medicines_dispensed_2025.csv",
}
PACK = list(FILES)
DISTRACTORS = ["profiles", "workforce", "medicines"]
CONTEXT = ["plan"]


def world():
    R = RC.build()
    log, *_ = RC.pilot(R)
    R["log"] = log
    rng = np.random.default_rng(P.SEED_ASK)
    names, qln = A.practice_names(R["pr"], rng, entered_2023=A.moved_practices(R["pr"], R["ext"]))
    R["practices"].insert(1, "practice_name", R["practices"].practice_id.map(names))
    R["quitline"] = A.quitline(R["pr"], R["ext"], qln, rng)
    # the dialler draws from its own stream: the first whose figures sit clear of their rounding edges
    for k in range(60):
        dl = A.dialler(log, np.random.default_rng(P.SEED_ASK + 500 + k))
        if dialler_ok(dl):
            break
    R["dialler"] = dl
    R["moved"] = A.moved_practices(R["pr"], R["ext"])
    return R


def dialler_ok(dl):
    """Every member-month's minutes per patient reached at least 0.0025 inside its printed cell, and every weekday's
    calls and patients reached from 5 pm moved by reading the record time as the start."""
    st = pd.to_datetime(dl._start)
    end = pd.to_datetime(dl.date_time)
    calls = dl._kind == "call"
    ans = calls & (dl.result == "Answered")
    for ag in ("QO-C1", "QO-C2", "QO-N1"):
        a = dl[ans & (dl.agent_id == ag)]
        m = st[a.index].dt.month
        v = a.groupby(m)._staff_s.sum() / 60.0 / a.groupby(m).patient_key.nunique()
        if len(v) != 10 or (0.05 - (v - v.round(1)).abs()).min() < 0.0025:
            return False
    day = st.dt.day_name()
    for t in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
        g = calls & (st.dt.hour >= 17) & (day == t)
        n = calls & (end.dt.hour >= 17) & (end.dt.day_name() == t)
        if g.sum() == n.sum() or dl[g & ans].patient_key.nunique() == dl[n & ans].patient_key.nunique():
            return False
    return True


def distractors(R, rng):
    ext = R["ext"]
    adults = ext.groupby("sub_region").size()
    prof = pd.DataFrame({"sub_region": [P.NAME[g] for g in P.REG],
                         "residents_18_plus_2025": [int(adults[P.NAME[g]] * rng.uniform(1.22, 1.38)) for g in P.REG],
                         "remoteness": ["Major city", "Inner regional", "Major city", "Inner regional", "Outer regional"],
                         "irsd_median_decile": [6, 7, 2, 5, 4]})
    # GP workforce by practice: full-time equivalent GPs and practice nurses, and new-patient availability
    pr = R["practices"]
    wf = pd.DataFrame({"practice_id": pr.practice_id, "sub_region": pr.sub_region,
                       "gp_fte": [round(max(1.0, n / 1700.0 * rng.uniform(0.75, 1.25)), 1) for n in pr.active_patients_18_plus],
                       "practice_nurse_fte": [round(max(0.4, n / 3200.0 * rng.uniform(0.6, 1.4)), 1)
                                              for n in pr.active_patients_18_plus],
                       "taking_new_patients": rng.choice(["Yes", "No", "Limited"], len(pr), p=[0.55, 0.15, 0.30])})
    med = []
    for g in P.REG:
        for m in pd.period_range("2025-01", "2025-12", freq="M"):
            base = adults[P.NAME[g]] / 1000.0
            med.append((P.NAME[g], str(m), "Varenicline", int(rng.poisson(base * 0.55))))
            med.append((P.NAME[g], str(m), "Nicotine replacement therapy", int(rng.poisson(base * 0.90))))
    medicines = pd.DataFrame(med, columns=["sub_region", "month", "medicine", "dispensings"])
    return prof, wf, medicines


def build(target, R=None):
    os.makedirs(target, exist_ok=True)
    if R is None:
        R = world()
    f = lambda k: os.path.join(target, FILES[k])
    R["ext"].to_csv(f("extract"), index=False)
    R["hist"].to_parquet(f("history"), index=False)
    R["practices"].to_csv(f("practices"), index=False)
    R["log"].to_csv(f("log"), index=False)
    R["quitline"].to_csv(f("quitline"), index=False)
    R["dialler"].drop(columns=["_start", "_staff_s", "_kind"]).to_csv(f("dialler"), index=False)
    rng = np.random.default_rng(P.SEED_DOCS)
    prof, wf, medicines = distractors(R, rng)
    prof.to_csv(f("profiles"), index=False)
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Workforce June 2026"
    ws.append(list(wf.columns))
    for row in wf.itertuples(index=False):
        ws.append(list(row))
    ns = wb.create_sheet("Notes")
    ns.append(["Notes"])
    ns.append(["Full-time equivalents at 30 June 2026 from the practices' workforce returns to the PHN."])
    ns.append(["Taking new patients is as each practice reported it to the PHN's practice support team in June 2026."])
    wb.properties.creator = "Practice Support"
    wb.save(f("workforce"))
    postprocess.scrub(f("workforce"), P.ORG, "2026-07-21")
    postprocess.finish_office(f("workforce"), "2026-07-08T00:20:00Z", "2026-07-21T04:05:00Z", P.ORG,
                              person="Practice Support")
    medicines.to_csv(f("medicines"), index=False)
    DC.plan(f("plan"))
    DC.dictionary(f("dictionary"))
    return R
