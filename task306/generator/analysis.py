"""The golden analysis, run on the cut pack (target/) only: each review's protocol executed on the practices'
extracts at 31 December 2026, who started each eligible patient's medicine rebuilt from the trusts' letters, the
pilot's six-month take-off split the same way and carried patient by patient, the harms weighted at each patient's
age, the call; then the two asks. Every routine takes the handling it applies as an argument, so the checks and the
ceiling script can run the routes a solver might take through the same code."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

AS_OF = pd.Timestamp("2026-12-31")
WIN0 = pd.Timestamp("2026-07-01")
CV = "Clun Valley PCN"
NETWORKS = ["Clun Valley PCN", "Wrekinside Central PCN", "Wrekinside North PCN", "Teme Valley PCN",
            "Severn Gorge PCN"]
REVIEWS = ["AP", "BZ", "GB"]
LABEL = {"Antipsychotics 65+": "AP", "Benzodiazepines and Z-drugs 65+": "BZ", "Gabapentinoid with opioid": "GB"}
GENERIC = {"AP": ["risperidone", "quetiapine", "haloperidol", "olanzapine"],
           "BZ": ["diazepam", "temazepam", "lorazepam", "zopiclone", "zolpidem", "clobazam"],
           "GB": ["pregabalin", "gabapentin"],
           "OP": ["codeine", "co-codamol", "tramadol", "morphine", "oxycodone", "buprenorphine"]}
HARM = {"AP": {"65 to 74": 6.7, "75 to 84": 9.3, "85 and over": 12.2},
        "BZ": {"65 to 74": 2.7, "75 to 84": 4.2, "85 and over": 6.3},
        "GB": {"18 to 64": 1.8, "65 to 74": 2.7, "75 to 84": 3.7, "85 and over": 4.5}}
EXCLUDE = {"AP": {"69322001", "58214004", "13746004", "1129481000000101"},
           "BZ": {"1129481000000101"},
           "GB": {"84757009", "1129481000000101"}}
MIN_ISSUES = {"AP": 2, "BZ": 3, "GB": 2, "OP": 2}
MIN_AGE = {"AP": 65, "BZ": 65, "GB": 18}
GP_WINDOW = 21   # days after a letter within which its GP Connect receipt is sought (ask A)


def band(a):
    if a < 65:
        return "18 to 64"
    if a < 75:
        return "65 to 74"
    if a < 85:
        return "75 to 84"
    return "85 and over"


def class_of(medicine):
    m = medicine.lower()
    for cls, names in GENERIC.items():
        if any(m.startswith(n) for n in names):
            return cls
    return None


def load(target):
    f = lambda n: os.path.join(target, n)
    D = {}
    D["reg"] = pd.read_csv(f("member_practice_register_2026.csv"), dtype=str)
    R = pd.read_parquet(f("patient_registrations_2020-2026.parquet"))
    for c in ("date_of_death", "registration_start", "registration_end"):
        R[c] = pd.to_datetime(R[c])
    D["regs"] = R
    D["courses"] = pd.read_csv(f("repeat_medication_courses_2026-12-31.csv"), dtype=str)
    D["issues"] = pd.read_parquet(f("prescribing_issues_2025-07_2026-12.parquet"))
    D["problems"] = pd.read_csv(f("problem_list_extract_2026-12-31.csv"), dtype=str)
    D["letters"] = pd.read_csv(f("trust_medicine_letters_feed_2019-2026.csv"), dtype=str, keep_default_na=False)
    D["lookup"] = pd.read_csv(f("trust_hospital_number_lookup.csv"), dtype=str)
    D["workflow"] = pd.read_csv(f("practice_document_workflow_2026.csv"), dtype=str)
    D["hub"] = pd.read_csv(f("pharmacist_hub_appointments_2026.csv"), dtype=str, keep_default_na=False)
    D["groups"] = pd.read_excel(f("hub_group_session_register_2026.xlsx"), sheet_name="Register", dtype=str)
    D["activity"] = pd.read_csv(f("clinical_system_pharmacist_activity_2026.csv"), dtype=str)
    D["lists"] = pd.read_csv(f("registered_list_sizes_2026.csv"), dtype={"practice_code": str})
    D["pilot"] = pd.read_csv(f("deprescribing_pilot_outcome_log_2026.csv"), dtype=str)
    return D


def network_of(D):
    reg = D["reg"]
    m = dict(zip(reg["ods_code"], reg["primary_care_network"]))
    return m


# --------------------------------------------------------------------------------------------------------------------
# The main call
# --------------------------------------------------------------------------------------------------------------------
def registered_at(D, when):
    R = D["regs"]
    t = pd.Timestamp(when)
    m = (R["registration_start"] <= t) & (R["registration_end"].isna() | (R["registration_end"] > t))
    m &= R["date_of_death"].isna() | (R["date_of_death"] > t)
    return R.loc[m, ["patient_pseudonym", "practice_code", "birth_month", "sex"]].drop_duplicates("patient_pseudonym")


def eligible(D, when=AS_OF, win=(WIN0, AS_OF), outside_cv=True, window_override=None):
    """Each review's protocol on the search date: registered at a member practice (outside the pilot network), the
    age, the issues in the six months to the search date, and the exclusions."""
    net = network_of(D)
    pts = registered_at(D, when)
    pts = pts[pts["practice_code"].isin(net)].copy()
    pts["network"] = pts["practice_code"].map(net)
    if outside_cv:
        pts = pts[pts["network"] != CV]
    by = pts["birth_month"].str[:4].astype(int)
    bm = pts["birth_month"].str[5:7].astype(int)
    w = pd.Timestamp(when)
    pts["age"] = w.year - by - (w.month < bm).astype(int)
    I = D["issues"].copy()
    I["cls"] = I["medicine"].map(class_of)
    I["issue_date"] = pd.to_datetime(I["issue_date"])
    lo, hi = window_override or win
    Iw = I[(I["issue_date"] >= lo) & (I["issue_date"] <= hi)]
    Iw = Iw[~Iw["medicine"].str.lower().str.startswith("clobazam")]
    cnt = Iw.groupby(["patient_pseudonym", "cls"]).size().unstack(fill_value=0)
    prob = D["problems"]
    prob = prob[pd.to_datetime(prob["recorded_date"]) <= w]
    out = {}
    for cls in REVIEWS:
        ok = cnt.index[cnt.get(cls, pd.Series(0, index=cnt.index)) >= MIN_ISSUES[cls]]
        if cls == "GB":
            ok = [p for p in ok if cnt.loc[p].get("OP", 0) >= MIN_ISSUES["OP"]]
        e = pts[pts["patient_pseudonym"].isin(set(ok)) & (pts["age"] >= MIN_AGE[cls])]
        ex = set(prob.loc[prob["snomed_code"].isin(EXCLUDE[cls]), "patient_pseudonym"])
        e = e[~e["patient_pseudonym"].isin(ex)].copy()
        e["band"] = e["age"].map(band)
        out[cls] = e.sort_values("patient_pseudonym").reset_index(drop=True)
    return out


def _letter_dates(L):
    d = L["letter_date"]
    iso = d.str.match(r"^\d{4}-\d\d-\d\d$")
    out = pd.Series(pd.NaT, index=L.index, dtype="datetime64[ns]")
    out[iso] = pd.to_datetime(d[iso], format="%Y-%m-%d")
    out[~iso] = pd.to_datetime(d[~iso], format="%d/%m/%Y")
    return out


def resolved_letters(D, drop_hn_only=False):
    """Letter lines with the patient resolved: the pseudonym where the feed carries it, else the trust's hospital
    number through the lookup."""
    L = D["letters"].copy()
    L["date"] = _letter_dates(L)
    enc = L["encounter_date"]
    iso = enc.str.match(r"^\d{4}-\d\d-\d\d$")
    L["enc"] = pd.NaT
    L.loc[iso, "enc"] = pd.to_datetime(enc[iso], format="%Y-%m-%d")
    L.loc[~iso, "enc"] = pd.to_datetime(enc[~iso], format="%d/%m/%Y")
    lk = D["lookup"].set_index(["trust", "hospital_number"])["patient_pseudonym"]
    blank = L["patient_pseudonym"] == ""
    if drop_hn_only:
        L = L[~blank].copy()
    else:
        keys = list(zip(L.loc[blank, "sender"], L.loc[blank, "hospital_number"]))
        L.loc[blank, "patient_pseudonym"] = [lk.get(k, "") for k in keys]
    L["cls"] = L["medicine_line"].map(_class_in_text)
    return L


_PAT = {cls: re.compile(r"\b(" + "|".join(names) + r")\b", re.I) for cls, names in GENERIC.items()}


def _class_in_text(t):
    for cls in ("AP", "BZ", "GB"):
        if _PAT[cls].search(t):
            return cls
    return None


def first_issue(D, cls):
    C = D["courses"].copy()
    C["cls"] = C["medicine"].map(class_of)
    C = C[C["cls"] == cls]
    if cls == "BZ":
        C = C[~C["medicine"].str.lower().str.startswith("clobazam")]
    C["first"] = pd.to_datetime(C["first_issue_date"])
    return C.groupby("patient_pseudonym")["first"].min()


def provenance(D, cls, patients, window=60, basis="letter", any_time=False, drop_hn_only=False, L=None,
               start_only=False):
    """specialist when a letter naming a medicine of the class is dated in the `window` days before the first issue of
    the patient's earliest course of the class; else practice."""
    if L is None:
        L = resolved_letters(D, drop_hn_only)
    Lc = L[L["cls"] == cls]
    if start_only:
        Lc = Lc[Lc["recommendation"] == "Start"]
    if basis == "received":
        W_ = D["workflow"]
        rec = dict(zip(W_["sender_reference"], pd.to_datetime(W_["received"]).dt.normalize()))
        dts = Lc["letter_reference"].map(rec)
        Lc = Lc.assign(date=dts.where(dts.notna(), Lc["date"]))
    fi = first_issue(D, cls)
    by_p = Lc.groupby("patient_pseudonym")["date"].apply(list).to_dict()
    out = {}
    for p in patients:
        f = fi.get(p)
        ds = by_p.get(p, [])
        if any_time:
            out[p] = "specialist" if ds else "practice"
            continue
        hit = f is not None and any((f - pd.Timedelta(days=window)) <= d < f for d in ds)
        out[p] = "specialist" if hit else "practice"
    return out


def pilot_table(D):
    P = D["pilot"]
    six = P[P["record_type"] == "Six-month follow-up"].copy()
    six["cls"] = six["review"].map(LABEL)
    six["off"] = (six["outcome"] == "Off medicine").astype(int)
    return six


def pilot_rates(D, prov_kw=None, by=None, L=None):
    """The pilot's six-month take-off, by review and provenance (and optionally one more attribute)."""
    six = pilot_table(D)
    prov_kw = prov_kw or {}
    rows = []
    for cls in REVIEWS:
        s = six[six["cls"] == cls].copy()
        pr = provenance(D, cls, s["patient_pseudonym"], L=L, **prov_kw)
        s["prov"] = s["patient_pseudonym"].map(pr)
        rows.append(s)
    six = pd.concat(rows)
    regs = D["regs"].drop_duplicates("patient_pseudonym").set_index("patient_pseudonym")
    six["age"] = 2026 - six["patient_pseudonym"].map(regs["birth_month"]).str[:4].astype(int)
    six["band"] = six["age"].map(band)
    six["sex"] = six["patient_pseudonym"].map(regs["sex"])
    return six


def carry(D, E, six, how="provenance", prov=None, pooled_specialist=False):
    """Each eligible patient's chance of being off six months after review, from the pilot."""
    out = {}
    for cls in REVIEWS:
        e = E[cls].copy()
        s = six[six["cls"] == cls]
        if how == "pooled":
            e["chance"] = s["off"].mean()
        elif how == "provenance":
            e["prov"] = e["patient_pseudonym"].map(prov[cls])
            r = s.groupby("prov")["off"].mean().to_dict()
            if pooled_specialist:
                sp = six[six["prov"] == "specialist"]
                r["specialist"] = sp["off"].mean()
            e["chance"] = e["prov"].map(r)
        elif how.startswith("provenance+"):
            k = how.split("+")[1]
            e["prov"] = e["patient_pseudonym"].map(prov[cls])
            r = s.groupby(["prov", k])["off"].mean().to_dict()
            r0 = s.groupby("prov")["off"].mean().to_dict()
            e["chance"] = [r.get((pv, kv), r0[pv]) for pv, kv in zip(e["prov"], e[k])]
        elif how.startswith("pooled+"):
            k = how.split("+")[1]
            r = s.groupby(k)["off"].mean().to_dict()
            e["chance"] = e[k].map(r).fillna(s["off"].mean())
        e["harm"] = e["band"].map(HARM[cls]) / 100.0
        e["harms"] = e["chance"] * e["harm"]
        out[cls] = e
    return out


def summarise(res):
    s = {}
    for cls in REVIEWS:
        e = res[cls]
        s[cls] = dict(eligible=int(len(e)), off=float(e["chance"].sum()), harms=float(e["harms"].sum()))
    order = sorted(REVIEWS, key=lambda c: -s[c]["harms"])
    return s, order


def main_call(D, prov_kw=None, how="provenance", E=None, L=None, pooled_specialist=False):
    E = E if E is not None else eligible(D)
    prov_kw = prov_kw or {}
    if L is None:
        L = resolved_letters(D, prov_kw.get("drop_hn_only", False))
    kw = {k: v for k, v in prov_kw.items() if k != "drop_hn_only"}
    six = pilot_rates(D, kw, L=L)
    prov = {cls: provenance(D, cls, E[cls]["patient_pseudonym"], L=L, **kw) for cls in REVIEWS}
    if how.startswith("provenance+sex") or how.startswith("pooled+sex"):
        regs = D["regs"].drop_duplicates("patient_pseudonym").set_index("patient_pseudonym")["sex"]
        for cls in REVIEWS:
            E[cls] = E[cls].assign(sex=E[cls]["patient_pseudonym"].map(regs))
    res = carry(D, E, six, how, prov, pooled_specialist)
    s, order = summarise(res)
    return dict(summary=s, order=order, res=res, six=six, prov=prov, E=E)


def figures_main(M):
    s = M["summary"]
    fig = {}
    for cls in REVIEWS:
        fig[cls] = dict(eligible=s[cls]["eligible"], off=s[cls]["off"], harms=s[cls]["harms"],
                        off_10=int(round(s[cls]["off"] / 10.0)) * 10, harms_1=int(round(s[cls]["harms"])))
    o = M["order"]
    fig["call"], fig["runner_up"], fig["third"] = o[0], o[1], o[2]
    fig["gap"] = fig[o[0]]["harms_1"] - fig[o[1]]["harms_1"]
    return fig


# --------------------------------------------------------------------------------------------------------------------
# Ask A: hospital medicine letters received by each network's practices, by half of 2026
# --------------------------------------------------------------------------------------------------------------------
def letters_received(D, basis="received", dedupe_resend=True, gpconnect="match", resend_mode="content",
                     network_by="receiving", L=None, gp_window=None):
    """Each network's medicine letters by the half in which its practices received them. Handling switches:
    basis 'received' or 'letter'; dedupe_resend; gpconnect 'match' (patient, sender and document date), 'drop' or
    'letter_date'; resend_mode 'content' (a 7 April copy of an earlier letter) or 'batch' (every 7 April letter);
    network_by 'receiving' (the practice that received it) or 'addressed' (the feed's practice field)."""
    net = network_of(D)
    gp_window = GP_WINDOW if gp_window is None else gp_window
    if L is None:
        L = resolved_letters(D)
    lines = L.sort_values(["letter_reference", "line"])
    lt = lines.groupby("letter_reference").agg(sender=("sender", "first"), service=("service", "first"),
                                               date=("date", "first"), enc=("enc", "first"),
                                               p=("patient_pseudonym", "first"),
                                               addressed=("gp_practice_code", "first"),
                                               content=("medicine_line", lambda x: "|".join(x)))
    lt = lt.reset_index()
    W_ = D["workflow"].copy()
    W_["received"] = pd.to_datetime(W_["received"])
    W_["document_date"] = pd.to_datetime(W_["document_date"])
    by_ref = W_.set_index("sender_reference")
    lt["recv"] = lt["letter_reference"].map(by_ref["received"])
    lt["recv_prac"] = lt["letter_reference"].map(by_ref["practice_code"])
    gp = W_[~W_["sender_reference"].isin(set(lt["letter_reference"])) & W_["sender"].str.startswith("Wrekinside")]
    if gpconnect in ("match", "exact", "exact_fallback"):
        un = lt[lt["recv"].isna() & lt["sender"].str.startswith("Wrekinside")].sort_values(["date", "letter_reference"])
        gps = gp.sort_values(["received", "document_id"])
        pools = {}
        exact = gpconnect != "match"
        for k1, k2, k3, rv, pr in zip(gps["patient_pseudonym"], gps["sender"], gps["document_date"], gps["received"],
                                      gps["practice_code"]):
            pools.setdefault((k1, k2, k3) if exact else (k1, k2), []).append((rv, pr))
        rv_new, pr_new = {}, {}
        for i, k1, k2, k3 in zip(un.index, un["p"], un["sender"], un["date"]):
            q = pools.get((k1, k2, k3) if exact else (k1, k2))
            if not q:
                continue
            if exact:
                rv, pr = q.pop(0)
            else:
                cand = [j for j, (rv, pr) in enumerate(q) if k3 <= rv.normalize() <= k3 + pd.Timedelta(days=gp_window)]
                if not cand:
                    continue
                rv, pr = q.pop(cand[0])
            rv_new[i], pr_new[i] = rv, pr
        if rv_new:
            ix = list(rv_new)
            lt.loc[ix, "recv"] = [rv_new[i] for i in ix]
            lt.loc[ix, "recv_prac"] = [pr_new[i] for i in ix]
        if gpconnect == "exact_fallback":
            un2 = lt["recv"].isna() & lt["sender"].str.startswith("Wrekinside") & (lt["date"] >= "2026-09-20")
            lt.loc[un2, "recv"] = lt.loc[un2, "date"]
            lt.loc[un2, "recv_prac"] = lt.loc[un2, "addressed"]
    elif gpconnect == "letter_date":
        un = lt["recv"].isna() & lt["sender"].str.startswith("Wrekinside") & (lt["date"] >= "2026-09-20")
        lt.loc[un, "recv"] = lt.loc[un, "date"]
        lt.loc[un, "recv_prac"] = lt.loc[un, "addressed"]
    # the 7 April re-sends: the same letter as an earlier one
    lt["group"] = lt["letter_reference"]
    mmh = lt["sender"].str.startswith("Marches")
    apr7 = mmh & (lt["date"] == pd.Timestamp("2026-04-07"))
    if dedupe_resend:
        if resend_mode == "content":
            early = lt[mmh & (lt["date"] < pd.Timestamp("2026-04-07"))]
            key = dict(zip(zip(early["p"], early["service"], early["enc"], early["content"]),
                           early["letter_reference"]))
            sub = lt[apr7]
            grp = [key.get(k, ref) for k, ref in zip(zip(sub["p"], sub["service"], sub["enc"], sub["content"]),
                                                    sub["letter_reference"])]
            lt.loc[sub.index, "group"] = grp
        elif resend_mode == "batch":
            lt = lt[~apr7].copy()
    if basis == "letter":
        lt["when"] = lt["date"]
    else:
        lt["when"] = lt["recv"]
    g = lt.dropna(subset=["when"]).sort_values("when").groupby("group").first().reset_index()
    if network_by == "receiving":
        g["prac"] = g["recv_prac"].where(g["recv_prac"].notna(), g["addressed"])
    else:
        g["prac"] = g["addressed"]
    succ = dict(zip(D["reg"]["ods_code"], D["reg"]["successor_ods_code"].fillna("")))
    g["prac"] = [succ.get(p_) or p_ for p_ in g["prac"]]
    g["network"] = g["prac"].map(net)
    g = g[g["when"].between(pd.Timestamp("2026-01-01"), pd.Timestamp("2026-12-31 23:59:59"))]
    g["half"] = np.where(g["when"] < pd.Timestamp("2026-07-01"), "H1", "H2")
    counts = g.groupby(["network", "half"]).size()
    lists = D["lists"].copy()
    lists["network"] = lists["practice_code"].map(net)
    den = lists.groupby(["network", "extract_date"])["registered_patients"].sum()
    out = {}
    for n_ in NETWORKS:
        for h, d0 in (("H1", "2026-01-01"), ("H2", "2026-07-01")):
            c = int(counts.get((n_, h), 0))
            out[(n_, h)] = dict(letters=c, patients=int(den[(n_, d0)]), rate=1000.0 * c / den[(n_, d0)])
    return out


# --------------------------------------------------------------------------------------------------------------------
# Ask B: patient consultations with the pharmacist team, by network and quarter
# --------------------------------------------------------------------------------------------------------------------
def _local(ts):
    t = pd.to_datetime(ts.str.replace("Z", "", regex=False))
    bst = (t >= pd.Timestamp("2026-03-29 01:00")) & (t < pd.Timestamp("2026-10-25 01:00"))
    return t + pd.to_timedelta(np.where(bst, 1, 0), unit="h")


def _next_working(d, holidays):
    d = d + pd.Timedelta(days=1)
    while d.weekday() >= 5 or d in holidays:
        d = d + pd.Timedelta(days=1)
    return d


HOLIDAYS = {pd.Timestamp(x) for x in ("2026-01-01", "2026-04-03", "2026-04-06", "2026-05-04", "2026-05-25",
                                      "2026-08-31", "2026-12-25", "2026-12-28")}


def consultations(D, dedupe="writeup", window_days=None, groups="attendees", network_by="registration",
                  use=("hub", "activity", "groups"), utc="convert"):
    """Each network's patient consultations with the team by quarter. Handling switches: dedupe 'writeup' (a hub
    appointment and the same pharmacist's record of that patient on the same or next working day are one
    consultation), 'same_day' (same patient and local date), 'exact' (same patient and local date and time) or
    'none'; groups 'attendees' (each patient who attended), 'session' (one per session) or 'booked'; utc 'convert'
    or 'ignore'."""
    net = network_of(D)
    H = D["hub"].copy()
    H["local"] = _local(H["slot_start_utc"]) if utc == "convert" else pd.to_datetime(
        H["slot_start_utc"].str.replace("Z", "", regex=False))
    H["date"] = H["local"].dt.normalize()
    one = H[(H["patient_pseudonym"] != "") & (H["outcome"] == "Attended")].copy()
    A = D["activity"].copy()
    A["date"] = pd.to_datetime(A["consultation_date"])
    A["dt"] = pd.to_datetime(A["consultation_date"] + " " + A["consultation_time"])
    A["writeup"] = False
    if dedupe == "writeup":
        idx = A.groupby(["patient_pseudonym", "clinician"]).groups
        for row in one.itertuples(index=False):
            k = (row.patient_pseudonym, row.pharmacist)
            if k not in idx:
                continue
            hi = _next_working(row.date, HOLIDAYS) if window_days is None else row.date + pd.Timedelta(days=window_days)
            for j in idx[k]:
                if row.date <= A.at[j, "date"] <= hi and not A.at[j, "writeup"]:
                    A.at[j, "writeup"] = True
                    break
    elif dedupe == "same_day":
        keys = set(zip(one["patient_pseudonym"], one["date"]))
        A["writeup"] = [(p, d) in keys for p, d in zip(A["patient_pseudonym"], A["date"])]
    elif dedupe == "exact":
        keys = set(zip(one["patient_pseudonym"], one["local"]))
        A["writeup"] = [(p, d) in keys for p, d in zip(A["patient_pseudonym"], A["dt"])]
    rows = []
    if "activity" in use:
        a = A[~A["writeup"]]
        rows.append(pd.DataFrame({"p": a["patient_pseudonym"], "date": a["date"], "prac": a["practice_code"]}))
    if "hub" in use:
        rows.append(pd.DataFrame({"p": one["patient_pseudonym"], "date": one["date"], "prac": None}))
    if "groups" in use:
        G = D["groups"].copy()
        G["date"] = pd.to_datetime(G["Date"])
        if groups == "attendees":
            g = G[G["Attended"] == "Yes"]
            rows.append(pd.DataFrame({"p": g["Patient"], "date": g["date"], "prac": None}))
        elif groups == "booked":
            rows.append(pd.DataFrame({"p": G["Patient"], "date": G["date"], "prac": None}))
        elif groups == "session":
            s = H[(H["appointment_type"] == "Group medicines review")]
            for row in s.itertuples(index=False):
                g = G[G["Session"] == row.appointment_id]
                p0 = g["Patient"].iloc[0] if len(g) else None
                rows.append(pd.DataFrame({"p": [p0], "date": [row.date], "prac": [None]}))
    X = pd.concat(rows, ignore_index=True)
    # the patient's registered practice on the day, where the record does not carry it
    R = D["regs"]
    R = R[R["practice_code"].isin(net)]
    succ = dict(zip(D["reg"]["ods_code"], D["reg"]["successor_ods_code"].fillna("")))
    sp = {}
    for p_, a_, b_, c_ in zip(R["patient_pseudonym"], R["registration_start"], R["registration_end"],
                              R["practice_code"]):
        sp.setdefault(p_, []).append((a_, b_, c_))

    def prac_on(p_, d_):
        for a_, b_, c_ in sp.get(p_, []):
            if a_ <= d_ and (pd.isna(b_) or d_ < b_):
                return (succ.get(c_) or c_) if d_ >= pd.Timestamp("2025-04-01") else c_
        return None
    need = X["prac"].isna()
    X.loc[need, "prac"] = [prac_on(p_, d_) for p_, d_ in zip(X.loc[need, "p"], X.loc[need, "date"])]
    X["network"] = X["prac"].map(net)
    X["q"] = "Q" + X["date"].dt.quarter.astype(str)
    counts = X.groupby(["network", "q"]).size()
    lists = D["lists"].copy()
    lists["network"] = lists["practice_code"].map(net)
    den = lists.groupby(["network", "extract_date"])["registered_patients"].sum()
    out = {}
    for n_ in NETWORKS:
        for q, d0 in (("Q1", "2026-01-01"), ("Q2", "2026-04-01"), ("Q3", "2026-07-01"), ("Q4", "2026-10-01")):
            c = int(counts.get((n_, q), 0))
            out[(n_, q)] = dict(consultations=c, patients=int(den[(n_, d0)]), rate=1000.0 * c / den[(n_, d0)])
    return out


def r1(x):
    return float(np.floor(x * 10 + 0.5) / 10)
