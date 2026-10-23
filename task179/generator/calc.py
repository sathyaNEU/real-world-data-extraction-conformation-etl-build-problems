"""task179 golden computation, from the pack alone (target/), the way the Planning Office's analyst works it.

The call: each 2019 to 2025 first-time entrant's enrolment at the next census, modelled on the entrant's attributes,
the week-6 progress ratings and the number of other entrants of the intake the entrant meets in two or more of the
entrant's own Semester 1 classes (repeat classmates, in bands); the model applied to the 2026 intake and summed.
Ask A: Semester 1 2026 teaching groups by owning faculty, and those over 30 students. Ask B: continuing students at
the 2026 census by faculty and year of study."""
from __future__ import annotations

import os

import numpy as np
import pandas as pd
import scipy.sparse as sp

import common as C

FAC_ARC = {"FASS": "ASS", "FBUS": "BUS", "FSCI": "SCI", "FENG": "ENG", "FHLT": "HLT"}
RATE = {"S": 0, "C": 1, "R": 2, "Satisfactory": 0, "Some concern": 1, "At risk": 2}
BANDS = [0, 1, 2, 3, 4, 6, 9, 15, 22, 10 ** 9]


def load(target):
    P = lambda f: os.path.join(target, f)
    d = {}
    d["scls"] = pd.read_csv(P(C.F_SCLS), dtype={"STUDENT_NO": str})
    d["acls"] = pd.read_csv(P(C.F_ACLS), dtype=str)
    d["census"] = pd.read_csv(P(C.F_CENSUS), dtype={"STUDENT_ID": str})
    d["xwalk"] = pd.read_csv(P(C.F_XWALK), dtype=str)
    d["prog"] = pd.read_csv(P(C.F_PROG), dtype={"STUDENT": str, "CLASS": str}, keep_default_na=False)
    d["adm"] = pd.read_excel(P(C.F_ADM), sheet_name=None, dtype={"Student No": str, "Student ID": str})
    d["tt"] = pd.read_excel(P(C.F_TT))
    d["cat"] = pd.read_csv(P(C.F_CAT), dtype=str, keep_default_na=False)
    d["trf"] = pd.read_csv(P(C.F_TRF), dtype=str)
    return d


def census_year(s):
    s = str(s)
    return int(s[-4:]) if "/" in s else int(s[:4])


def enrolled_sets(d):
    """census year -> set of student ids with an enrolled programme attempt (leave is not enrolled)"""
    cz = d["census"].copy()
    cz["Y"] = cz["CENSUS_DATE"].map(census_year)
    en = cz[cz["STATUS"].isin(["EN", "Enrolled"])]
    return {y: set(g["STUDENT_ID"]) for y, g in en.groupby("Y")}


def entrants(d):
    """first-time entrants per intake, one row each, with the admissions attributes"""
    out = []
    for name, df in d["adm"].items():
        y = int(name.split()[0])
        df = df.copy()
        idc = "Student No" if "Student No" in df.columns else "Student ID"
        df = df.rename(columns={idc: "sid", "ASC Points": "asc", "ASC Score": "asc"})
        df["intake"] = y
        out.append(df)
    a = pd.concat(out, ignore_index=True)
    a = a[a["Entry Basis"] == "First-time"].copy()
    a["sid"] = a["sid"].astype(str)
    return a


def ties(pairs):
    """pairs: DataFrame with columns sid, cls. Repeat classmates: other students met in two or more classes."""
    sids = pd.Index(pairs["sid"].unique())
    cls = pd.Index(pairs["cls"].unique())
    r = sids.get_indexer(pairs["sid"])
    c = cls.get_indexer(pairs["cls"])
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(sids), len(cls)))
    M = (A @ A.T).tocsr()
    M.setdiag(0)
    M.eliminate_zeros()
    t2 = np.asarray((M >= 2).sum(1)).ravel()
    return pd.Series(t2, index=sids)


def frame(d):
    a = entrants(d)
    en = enrolled_sets(d)
    xw = dict(zip(d["xwalk"]["SIRIUS_STUDENT_NO"], d["xwalk"]["ARC_ID"]))
    a = a[[sid in en.get(y, set()) for sid, y in zip(a["sid"], a["intake"])]].copy()
    nxt = []
    for sid, y in zip(a["sid"], a["intake"]):
        if y >= 2026:
            nxt.append(np.nan)
        elif y + 1 < 2026:
            nxt.append(0 if sid in en[y + 1] else 1)
        else:
            nxt.append(0 if xw.get(sid) in en[2026] else 1)
    a["gone"] = nxt
    # classes
    s = d["scls"].rename(columns={"STUDENT_NO": "sid"})
    s["cls"] = s["TERM"] + ":" + s["CLASS_NBR"].astype(str)
    s["intake"] = s["COHORT_YR"]
    r = d["acls"].rename(columns={"arc_student_id": "sid"})
    r["cls"] = r["class_code"]
    r["intake"] = 2026
    t = []
    for y, g in pd.concat([s[["sid", "cls", "intake"]], r[["sid", "cls", "intake"]]]).groupby("intake"):
        tt = ties(g)
        t.append(pd.DataFrame({"sid": tt.index, "intake": y, "ties": tt.values}))
    t = pd.concat(t)
    a = a.merge(t, on=["sid", "intake"], how="left")
    a["ties"] = a["ties"].fillna(0)
    # week-6 progress ratings
    pr = d["prog"].copy()
    pr["v"] = pr["RATING"].map(RATE)
    m = pr.groupby(["STUDENT", "YEAR"])["v"].mean().rename("prisk").reset_index()
    m = m.rename(columns={"STUDENT": "sid", "YEAR": "intake"})
    a = a.merge(m, on=["sid", "intake"], how="left")
    a["prisk"] = a["prisk"].fillna(0.5)
    # attributes
    a["fif"] = (a["First in Family"] == "Y").astype(float)
    a["pt"] = (a["Attendance"] == "PT").astype(float)
    a["hard"] = (a["Hardship Grant"] == "Y").astype(float)
    a["lc"] = (a["Living-Learning Community"] == "Y").astype(float)
    a["hall"] = (~a["Accommodation"].isin(["Family home", "Private"])).astype(float)
    dob = pd.to_datetime(a["Date of Birth"])
    a["age"] = a["intake"] - dob.dt.year
    a["mature"] = (a["age"] >= 21).astype(float)
    acc = pd.to_datetime(a["Offer Accepted"])
    a["acc_day"] = (acc - pd.to_datetime(a["intake"].astype(str) + "-01-01")).dt.days
    a["asc"] = a["asc"].astype(float)
    return a


BASE = ["asc", "fif", "pt", "mature", "hard", "prisk", "lc", "hall", "acc_day"]


def design(a, form):
    X = [a[c].values.astype(float) for c in BASE]
    X[0] = (X[0] - 186.0) / 34.0
    X[-1] = X[-1] / 100.0
    for f in ["BUS", "SCI", "ENG", "HLT"]:
        X.append((a["Faculty"] == f).values.astype(float))
    t = a["ties"].values.astype(float)
    if form == "bands":
        e = BANDS
        X += [((t >= lo) & (t < hi)).astype(float) for lo, hi in zip(e[:-1], e[1:])][1:]
    elif form == "bands5":
        e = [0, 1, 3, 6, 10, 10 ** 9]
        X += [((t >= lo) & (t < hi)).astype(float) for lo, hi in zip(e[:-1], e[1:])][1:]
    elif form == "bands4":
        e = [0, 1, 3, 6, 10 ** 9]
        X += [((t >= lo) & (t < hi)).astype(float) for lo, hi in zip(e[:-1], e[1:])][1:]
    elif form.startswith("ge"):
        X.append((t >= int(form[2:])).astype(float))
    elif form == "any":
        X.append((t >= 1).astype(float))
    elif form == "lin":
        X.append(t)
    elif form == "log":
        X.append(np.log1p(t))
    elif form.startswith("sat"):
        X.append(1 - np.exp(-t / float(form[3:])))
    elif form == "none":
        pass
    else:
        raise KeyError(form)
    return np.column_stack([np.ones(len(a))] + X)


def logit_fit(X, y, it=60):
    """Newton-Raphson maximum likelihood for a logistic model; returns coefficients and the log-likelihood"""
    b = np.zeros(X.shape[1])
    for _ in range(it):
        eta = X @ b
        p = 1 / (1 + np.exp(-eta))
        W = p * (1 - p)
        g = X.T @ (y - p)
        H = (X * W[:, None]).T @ X
        step = np.linalg.solve(H + 1e-9 * np.eye(len(b)), g)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    p = 1 / (1 + np.exp(-(X @ b)))
    ll = float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return b, ll


def forecast(a, form="bands", years=None):
    h = a[a["intake"] < 2026]
    if years is not None:
        h = h[h["intake"].isin(years)]
    f = a[a["intake"] == 2026]
    b, ll = logit_fit(design(h, form), h["gone"].values.astype(float))
    p = 1 / (1 + np.exp(-(design(f, form) @ b)))
    return float(p.sum()), ll, b


# ------------------------------------------------------------------ ask A: teaching groups
def teaching_groups(d):
    tt = d["tt"]
    act = tt[tt["Class Status"] == "Active"]
    meet = act[["Class Code", "Day", "Start", "Teaching Weeks", "Room", "Teacher"]].drop_duplicates()
    # classes taught together: the same room, day, start and teaching weeks (the teacher of record is per class)
    key = meet["Day"] + "|" + meet["Start"] + "|" + meet["Teaching Weeks"] + "|" + meet["Room"]
    parent = {c: c for c in act["Class Code"].unique()}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for _, g in meet.assign(k=key).groupby("k"):
        cs = sorted(g["Class Code"].unique())
        for c in cs[1:]:
            ra, rb = find(cs[0]), find(c)
            if ra != rb:
                parent[rb] = ra
    cls = act.drop_duplicates("Class Code")[["Class Code", "Owning Faculty", "Enrolled at Census"]].copy()
    cls["grp"] = cls["Class Code"].map(find)
    grp = cls.groupby("grp").agg(fac=("Owning Faculty", "first"), n=("Enrolled at Census", "sum"),
                                 facs=("Owning Faculty", "nunique"))
    assert (grp["facs"] == 1).all()
    out = {}
    for f in ["FASS", "FBUS", "FSCI", "FENG", "FHLT"]:
        gg = grp[grp["fac"] == f]
        out[FAC_ARC[f]] = (int(len(gg)), int((gg["n"] > 30).sum()))
    return out


# ------------------------------------------------------------------ ask B: continuing students
def continuing(d):
    cz = d["census"].copy()
    cz["Y"] = cz["CENSUS_DATE"].map(census_year)
    c6 = cz[(cz["Y"] == 2026) & (cz["STATUS"] == "Enrolled") & (cz["YEAR_OF_STUDY"] >= 2)]
    cat = d["cat"]
    combos = {}
    for _, r in cat[cat["TYPE"] == "Conjoint"].iterrows():
        a, b = r["COMPONENTS"].split(";")
        combos[frozenset((a, b))] = a
    pfac = {r["CODE"]: FAC_ARC[r["OWNING_FACULTY"]] for _, r in cat[cat["TYPE"] == "Programme"].iterrows()}
    trf = d["trf"]
    moved = {}
    for _, r in trf.iterrows():
        moved.setdefault(r["STUDENT"], []).append((r["APPROVED"], r["FROM_PROGRAMME"], r["TO_PROGRAMME"]))
    out = {}
    n_stale = 0
    for sid, g in c6.groupby("STUDENT_ID"):
        progs = list(g.sort_values("ATTEMPT_SEQ")["PROGRAMME"])
        yos = int(g["YEAR_OF_STUDY"].iloc[0])
        tr = [m for m in moved.get(sid, []) if m[1] in progs and m[2] in progs]
        if len(progs) == 1:
            fac = pfac[progs[0]]
        elif tr:
            # an attempt left enrolled after the student transferred out of it: the student is in the new programme
            fac = pfac[sorted(tr)[-1][2]]
            n_stale += 1
        else:
            fac = pfac[combos[frozenset(progs)]]
        k = (fac, min(yos, 4))
        out[k] = out.get(k, 0) + 1
    return out, n_stale


def compute(target):
    d = load(target)
    a = frame(d)
    res = {"frame": a, "data": d}
    res["n2026"] = int((a["intake"] == 2026).sum())
    res["call"], res["ll"], res["coef"] = forecast(a, "bands")
    res["groups"] = teaching_groups(d)
    res["cont"], res["n_stale"] = continuing(d)
    return res
