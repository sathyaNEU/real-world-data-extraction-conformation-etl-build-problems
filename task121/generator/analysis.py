"""The golden analysis, read back from the shipped files only: Halwick's walk from the trust average (attendance,
disadvantage, the academy's own effect, the remainder) on a cross-classified fixed-effects model of the borough's
pupils by secondary and by the school where they sat key stage 2; the default path's model of pupils within
secondaries; Annex A's persistent and severe absence by academy; Annex B's Attainment 8 and EBacc entry by academy."""
import csv
import os

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.sparse.linalg import lsqr

import common as K

TRUST_NAMES = [s[1] for s in K.SECONDARIES if s[2]]
FOCAL_NAME = [s[1] for s in K.SECONDARIES if s[0] == K.FOCAL][0]
HT = ["Autumn 1", "Autumn 2", "Spring 1", "Spring 2", "Summer 1", "Summer 2"]


def read(target, key):
    return pd.read_csv(os.path.join(target, K.FILES[key]), dtype=str, keep_default_na=False)


def load(target):
    return {k: read(target, k) for k in ("transfer", "register", "tables", "attendance", "movements", "results25",
                                         "results26")}


# ------------------------------------------------------------------ the walk
def pupils(D, link=True):
    """The transfer file's pupils with a Progress 8 score, their absence rate and the school where they sat key
    stage 2 (a converted academy read as the school it was, through the register's predecessor URN)."""
    T = D["transfer"]
    E = T[T.p8_score != ""].copy()
    E["p8"] = E.p8_score.astype(float)
    poss = E.y11_sessions_possible.astype(float)
    E["absr"] = 100.0 * (E.y11_sessions_auth_absence.astype(float) + E.y11_sessions_unauth_absence.astype(float)) / poss
    E["dis"] = (E.disadvantaged == "Y").astype(float)
    E["trust"] = E.ks4_school.isin(TRUST_NAMES)
    pred = {}
    if link:
        R = D["register"]
        pred = {r.urn: r.predecessor_urn for r in R.itertuples() if r.predecessor_urn and r.phase == "Primary"}
    E["ks2_school"] = E.ks2_la + ":" + E.ks2_urn.map(lambda u: pred.get(u, u))
    return E


def fit(E, classify=("secondary", "primary"), extra=()):
    """Least squares with a fixed effect for every secondary (and every key stage 2 school), the absence rate and
    the disadvantaged flag as the pupil terms."""
    n = len(E)
    cols = ["absr", "dis"] + list(extra)
    mats = [sp.csr_matrix(np.column_stack([E[c].values.astype(float) for c in cols]))]
    ss = sorted(E.ks4_school.unique())
    si = E.ks4_school.map({s: i for i, s in enumerate(ss)}).values
    mats.append(sp.csr_matrix((np.ones(n), (np.arange(n), si)), shape=(n, len(ss))))
    if "primary" in classify:
        pp = sorted(E.ks2_school.unique())[1:]
        pi = E.ks2_school.map({q: i for i, q in enumerate(pp)}).fillna(-1).astype(int).values
        m = pi >= 0
        mats.append(sp.csr_matrix((np.ones(m.sum()), (np.arange(n)[m], pi[m])), shape=(n, len(pp))))
    A = sp.hstack(mats).tocsr()
    sol = lsqr(A, E.p8.values, atol=1e-14, btol=1e-14, iter_lim=100000)[0]
    k = len(cols)
    return dict(beta=dict(zip(cols, sol[:k])), school=dict(zip(ss, sol[k:k + len(ss)])))


def walk(E, classify=("secondary", "primary"), extra=(), estimation=None):
    """The board's four items: estimation on `estimation` (all the borough's pupils by default), the items on the
    trust's pupils."""
    m = fit(E if estimation is None else estimation, classify, extra)
    T = E[E.trust]
    H = E[E.ks4_school == FOCAL_NAME]
    gap = H.p8.mean() - T.p8.mean()
    att = m["beta"]["absr"] * (H.absr.mean() - T.absr.mean())
    dis = m["beta"]["dis"] * (H.dis.mean() - T.dis.mean())
    own = H.ks4_school.map(m["school"]).mean() - T.ks4_school.map(m["school"]).mean()
    return dict(gap=gap, att=att, dis=dis, own=own, rem=gap - att - dis - own, b_abs=m["beta"]["absr"],
                b_dis=m["beta"]["dis"], n_h=len(H), n_t=len(T),
                abs_h=H.absr.mean(), abs_t=T.absr.mean(), dis_h=H.dis.mean(), dis_t=T.dis.mean())


ITEMS = ["att", "dis", "own", "rem"]
ITEM_NAME = {"att": "attendance", "dis": "disadvantage", "own": "the academy's own effect", "rem": "the remainder"}


def largest(w):
    return min(ITEMS, key=lambda k: w[k])


def feeder_view(E):
    """What lies behind the remainder: each key stage 2 school's pupils' mean Progress 8 at the secondaries other
    than Halwick against the borough's, for the schools that send Halwick most of its pupils."""
    H = E[E.ks4_school == FOCAL_NAME]
    share = H.ks2_school.value_counts() / len(H)
    top = share[share >= 0.04].index.tolist()
    out = []
    for s in top:
        g = E[E.ks2_school == s]
        out.append(dict(school=s, share=float(share[s]), n=len(g), n_elsewhere=int((g.ks4_school != FOCAL_NAME).sum()),
                        p8_halwick=float(g[g.ks4_school == FOCAL_NAME].p8.mean()),
                        p8_elsewhere=float(g[g.ks4_school != FOCAL_NAME].p8.mean())))
    return out


# ------------------------------------------------------------------ Annex A: attendance
def attendance(D, label="true", year="true", y11_rule=True, key="enrolment"):
    """Persistent and severe absence by academy: each half-term row given to the academy whose roll the pupil was
    on (the movements log dates each move between academies), year 11 counted for the autumn and spring terms only
    (the pupil's 2025/26 year group: the extract's year group is the current one for pupils still on roll).

    label "current" groups by the extract's academy column as it stands; year "current" reads the extract's year
    group as it stands; key "upn" merges a pupil's rows within an academy whatever their admission number."""
    A = D["attendance"].copy()
    for c in ("sessions_possible", "sessions_auth_absence", "sessions_unauth_absence"):
        A[c] = A[c].astype(int)
    A["h"] = A.half_term.map({n: i for i, n in enumerate(HT)})
    if year == "true":
        A["yg"] = A.year_group.astype(int) - (A.on_roll == "Y").astype(int)
    else:
        A["yg"] = A.year_group.astype(int)
    if label == "true":
        M = D["movements"]
        moves = {}
        for r in M[M.movement == "Transfer within trust"].itertuples():
            moves[r.upn] = (r.movement_date, r.from_school, r.to_school)
        start = dict(zip(HT, ["2025-09-03", "2025-11-03", "2026-01-05", "2026-02-23", "2026-04-13", "2026-06-08"]))
        acad = []
        for r in A.itertuples():
            mv = moves.get(r.upn)
            acad.append(mv[1] if (mv and start[r.half_term] < mv[0]) else r.academy)
        A["acad"] = acad
    else:
        A["acad"] = A.academy
    if y11_rule:
        A = A[~((A.yg == 11) & (A.h >= 4))]
    out = {}
    for k, g in A.groupby("acad"):
        en = g.groupby(["upn"] if key in ("enrolment", "upn") and label == "true" else
                       (["upn"] if key == "upn" else ["upn", "admission_no"]))[
            ["sessions_possible", "sessions_auth_absence", "sessions_unauth_absence"]].sum()
        r = (en.sessions_auth_absence + en.sessions_unauth_absence) / en.sessions_possible
        out[k] = dict(pa=100.0 * float((r >= 0.10).mean()), sa=100.0 * float((r >= 0.50).mean()), n=len(en))
    return out


# ------------------------------------------------------------------ Annex B: results
EBACC_KINDS = {"English Language": "ENGL", "English Literature": "ENGT", "Mathematics": "MAT",
               "Combined Science": "SCI2", "Biology": "SCI", "Chemistry": "SCI", "Physics": "SCI",
               "Computer Science": "SCI", "History": "EBH", "Geography": "EBH", "French": "EBL", "Spanish": "EBL",
               "Urdu": "EBL", "Polish": "EBL"}
TECH = {"L2D*": 8.5, "L2D": 7.0, "L2M": 5.5, "L2P": 4.0, "L1D*": 3.0, "L1D": 2.0, "L1M": 1.5, "L1P": 1.25, "U": 0.0}


def points(qual, subject, grade):
    if qual == "Technical Award":
        return TECH[grade]
    if subject == "Combined Science":
        a, b = grade.split("-")
        return (int(a) + int(b)) / 2.0
    return 0.0 if grade == "U" else float(grade)


def attainment8(rows):
    """rows: (series order, qualification, subject, discount code, grade) for one pupil."""
    best = {}
    for order, qual, subj, code, grade in sorted(rows):
        kind = EBACC_KINDS.get(subj)
        pts = points(qual, subj, grade)
        cur = best.get(code)
        if cur is None:
            best[code] = (order, qual, subj, pts)
        elif kind is None and pts > cur[3]:
            best[code] = (order, qual, subj, pts)          # outside the EBacc subjects the higher score counts
    q = list(best.values())
    eng = [x for x in q if EBACC_KINDS.get(x[2]) in ("ENGL", "ENGT")]
    mat = [x for x in q if EBACC_KINDS.get(x[2]) == "MAT"]
    total = 2.0 * mat[0][3] if mat else 0.0
    pool = []
    if eng:
        hi = max(eng, key=lambda x: x[3])
        total += (2.0 if len(eng) == 2 else 1.0) * hi[3]
        if len(eng) == 2:
            pool.append(min(eng, key=lambda x: x[3])[3])
    eb = []
    for x in q:
        kind = EBACC_KINDS.get(x[2])
        if kind == "SCI2":
            eb += [x[3], x[3]]
        elif kind in ("SCI", "EBH", "EBL"):
            eb.append(x[3])
    eb.sort(reverse=True)
    total += sum(eb[:3])
    pool += eb[3:]
    pool += [x[3] for x in q if EBACC_KINDS.get(x[2]) is None]
    pool.sort(reverse=True)
    return total + sum(pool[:3])


def ebacc_entered(rows):
    subs = {r[2] for r in rows}
    sci = "Combined Science" in subs or len(subs & {"Biology", "Chemistry", "Physics", "Computer Science"}) >= 2
    return ({"English Language", "English Literature", "Mathematics"} <= subs and sci
            and bool(subs & {"History", "Geography"}) and bool(subs & {"French", "Spanish", "Urdu", "Polish"}))


def results(D, early=True):
    R26 = D["results26"]
    R25 = D["results25"]
    rows = {}
    cohort = {}
    for r in R26.itertuples():
        cohort[r.upn] = r.centre_name
        rows.setdefault(r.upn, []).append((1, r.qualification, r.subject, r.discount_code, r.grade))
    if early:
        for r in R25.itertuples():
            if r.upn in cohort:
                rows[r.upn].append((0, r.qualification, r.subject, r.discount_code, r.grade))
    out = {}
    for k in TRUST_NAMES:
        ups = [u for u, c in cohort.items() if c == k]
        a8 = [attainment8(rows[u]) for u in ups]
        eb = [ebacc_entered(rows[u]) for u in ups]
        out[k] = dict(a8=float(np.mean(a8)), ebacc=100.0 * float(np.mean(eb)), n=len(ups))
    return out
