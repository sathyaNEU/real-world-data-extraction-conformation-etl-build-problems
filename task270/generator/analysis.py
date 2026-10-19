"""The analysis on the cut pack: each component's correlation with the academy average among the appointees, the
corrections an analyst could apply for how the appointees were chosen, and the golden's correction (the multivariate
correction on the variables the appointments were made on); then the two asks (cost per candidate, the people who
applied and each component's completion rate)."""
import datetime as dt
import itertools

import numpy as np

import common as K
import pack as PK

COMP = K.COMPONENTS


def lawley(Pss, S, s_idx, o_idx):
    """The Pearson-Lawley correction: the pool covariance of the selection variables (Pss) and the selected group's
    covariance of everything (S) give the pool covariance of everything."""
    Sss = S[np.ix_(s_idx, s_idx)]
    Sso = S[np.ix_(s_idx, o_idx)]
    Soo = S[np.ix_(o_idx, o_idx)]
    Si = np.linalg.inv(Sss)
    Pso = Pss @ Si @ Sso
    Poo = Soo - Sso.T @ (Si - Si @ Pss @ Si) @ Sso
    n = len(s_idx) + len(o_idx)
    P = np.zeros((n, n))
    P[np.ix_(s_idx, s_idx)] = Pss
    P[np.ix_(s_idx, o_idx)] = Pso
    P[np.ix_(o_idx, s_idx)] = Pso.T
    P[np.ix_(o_idx, o_idx)] = Poo
    return P


def to_r(P):
    d = np.sqrt(np.diag(P))
    return P / np.outer(d, d)


def arrays(sample):
    X = np.array([[m["s"][c] for c in COMP] for m in sample], float)
    vet = np.array([1.0 if m["vet"] else 0.0 for m in sample])
    a = np.array([m["appointed"] for m in sample])
    Y = np.array([m["y"] if m["y"] is not None else np.nan for m in sample], float)
    fin = np.array([0.6 * m["s"]["written"] + 0.4 * m["s"]["oral"] + 5 * (1 if m["vet"] else 0) for m in sample])
    return X, vet, a, Y, fin


def routes(sample):
    """Every route's five validities, in COMP order."""
    X, vet, a, Y, fin = arrays(sample)
    out = {}
    out["appointees"] = np.array([np.corrcoef(X[a, j], Y[a])[0, 1] for j in range(5)])
    c2 = []
    for j in range(5):
        u = X[:, j].std(ddof=1) / X[a, j].std(ddof=1)
        r = out["appointees"][j]
        c2.append(u * r / np.sqrt(1 + (u * u - 1) * r * r))
    out["case2"] = np.array(c2)
    # the golden: the selection variables are the written test, the oral board, the veteran credit and the physical
    # ability test's points (the list took those who passed it)
    Z = np.column_stack([X[:, 0], X[:, 1], vet, X[:, 2], X[:, 3], X[:, 4], Y])
    P = to_r(lawley(np.cov(Z[:, :4].T), np.cov(Z[a].T), [0, 1, 2, 3], [4, 5, 6]))
    out["golden"] = np.array([P[0, 6], P[1, 6], P[3, 6], P[4, 6], P[5, 6]])
    # every score recorded before appointment as a selection variable
    Za = np.column_stack([X, vet, Y])
    Pa = to_r(lawley(np.cov(Za[:, :6].T), np.cov(Za[a].T), list(range(6)), [6]))
    out["all_recorded"] = Pa[:5, 6]
    # Case III on the final score (with the physical ability test's points, and alone)
    Zf = np.column_stack([fin, X[:, 2], X[:, 0], X[:, 1], X[:, 3], X[:, 4], Y])
    Pf = to_r(lawley(np.cov(Zf[:, :2].T), np.cov(Zf[a].T), [0, 1], [2, 3, 4, 5, 6]))
    out["final_and_pat"] = np.array([Pf[2, 6], Pf[3, 6], Pf[1, 6], Pf[4, 6], Pf[5, 6]])
    Zf1 = np.column_stack([fin, X, Y])
    Pf1 = to_r(lawley(np.atleast_2d(np.var(fin, ddof=1)), np.cov(Zf1[a].T), [0], [1, 2, 3, 4, 5, 6]))
    out["final_only"] = Pf1[1:6, 6]
    # the two ranked components alone
    Zw = np.column_stack([X, Y])
    Pw = to_r(lawley(np.cov(Zw[:, :2].T), np.cov(Zw[a].T), [0, 1], [2, 3, 4, 5]))
    out["ranked_only"] = Pw[:5, 5]
    # Case II on the two ranked components, Case III (final score) on the rest
    mixed = out["case2"].copy()
    mixed[2:] = out["final_only"][2:]
    out["mixed"] = mixed
    return out


LICENSED = ("golden", "all_recorded", "final_and_pat", "final_only", "ranked_only")


def order(v):
    return [COMP[i] for i in np.argsort(-np.asarray(v), kind="stable")]


def call(v):
    o = order(v)
    return dict(keep=sorted(o[:2], key=COMP.index), first_below=o[2], order=o)


def counts(sample):
    X, vet, a, Y, fin = arrays(sample)
    return dict(pool=len(sample), appointees=int(a.sum()))


# ------------------------------------------------------------------------------------------------ Ask A
TRIAL_NAMES = PK.TRIAL_NAMES


def _adm_of(line, cal):
    """The administration a ledger line belongs to: named in its description, or (payroll) the administration whose
    examination days its pay period covers."""
    for nm in PK.ADM_NAMES:
        if nm in line["line_description"]:
            return nm
    if line["line_description"].startswith("Payroll PPE"):
        pe = dt.datetime.strptime(line["line_description"][12:22], "%m/%d/%Y").date()
        for nm, days in cal.items():
            if any(pe - dt.timedelta(days=13) <= d <= pe for d in days):
                return nm
    if line["line_description"].startswith("EMS standby"):
        last = dt.datetime.strptime(line["line_description"].split("-")[1], "%m/%d/%Y").date()
        for nm, days in cal.items():
            if last in days:
                return nm
    return None


def exam_days(target):
    """Every examination day of each administration (written test, oral boards, physical ability test) from the
    Commission's calendar."""
    out = {}
    for r in PK.rows(target, "calendar"):
        days = [dt.date.fromisoformat(r["written_test"])]
        b0, b1 = dt.date.fromisoformat(r["oral_boards_from"]), dt.date.fromisoformat(r["oral_boards_to"])
        d = b0
        while d <= b1:
            days.append(d)
            d += dt.timedelta(days=1)
        days += [dt.date.fromisoformat(r["physical_ability_test_from"]), dt.date.fromisoformat(r["physical_ability_test_to"])]
        out[r["examination"]] = days
    return out


def sat_counts(target):
    S = PK.scores(target)
    return {c: sum(1 for s in S.values() if c in s) for c in COMP}


def cost(target, how="golden"):
    """Ask A on the pack: each component's cost per candidate who sat it over the four administrations.
    how: golden (FY2024 accruals and their reversal out, FY2025 accruals in), every_line (every line kept, the reversal
    shared), accruals_out (every accrual and the reversal out), named_only (the lines naming a trial administration,
    so payroll, retroactive pay and the reversal fall away)."""
    cal = exam_days(target)
    own = {c: 0.0 for c in COMP}
    shared = 0.0
    cc_of = {v: k for k, v in K.CC_OF.items()}
    for l in PK.ledger(target):
        desc = l["line_description"]
        if desc.startswith("Retroactive pay"):
            adm = "retro"
        elif desc.startswith("Reversal of FY2024"):
            adm = "reversal"
        else:
            adm = _adm_of(l, cal)
        if how == "named_only":
            if not any(nm in desc for nm in TRIAL_NAMES):
                continue
        elif adm not in TRIAL_NAMES and adm not in ("retro", "reversal"):
            continue
        accrual = desc.startswith("YE accrual")
        if how == "golden" and ((accrual and l["date"].year == 2024) or adm == "reversal"):
            continue
        if how == "accruals_out" and (accrual or adm == "reversal"):
            continue
        if l["cost_center"] == "4410":
            shared += l["amount"]
        else:
            own[cc_of[l["cost_center"]]] += l["amount"]
    n = sat_counts(target)
    tot = sum(K.MINUTES.values())
    total = {c: own[c] + shared * K.MINUTES[c] / tot for c in COMP}
    return {c: total[c] / n[c] for c in COMP}, total, n


# ------------------------------------------------------------------------------------------------ Ask B
ENTRY = {"Spring 2024": ("PO-24-0116",), "Autumn 2024": ("PO-24-0715",), "Spring 2025": ("PO-25-0121", "REQ-2025-0121"),
         "Autumn 2025": ("REQ-2025-0714",)}


def windows(target):
    out = {}
    for r in PK.rows(target, "calendar"):
        out[r["examination"]] = (dt.datetime.fromisoformat(r["applications_open"] + "T08:00"),
                                 dt.datetime.fromisoformat(r["applications_close"] + "T23:59:59"))
    return out


def _norm(s):
    return " ".join(s.lower().split())


def _digits(p):
    d = "".join(ch for ch in p if ch.isdigit())
    return d[-10:]


def applicants(target, keys=("name_dob", "email", "name_phone"), laterals="officer", window=True):
    """Ask B on the pack: the people who submitted an entry application in each administration's window. Records of
    one person are joined when they share any of the keys named (union of the key graphs)."""
    W = windows(target)
    recs = PK.applications(target)
    out = {}
    for adm, refs in ENTRY.items():
        mine = []
        for r in recs:
            if r["ref"] not in refs or r["submitted"] is None:
                continue
            if laterals == "officer" and (r["officer"] == "Yes" or r["title"] != "Police Officer" and r["officer"] != "No"):
                continue
            if laterals == "title" and r["title"] != "Police Officer":
                continue
            if window and not (W[adm][0] <= r["submitted"] <= W[adm][1]):
                continue
            mine.append(r)
        parent = list(range(len(mine)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for key in keys:
            seen = {}
            for i, r in enumerate(mine):
                if key == "name_dob":
                    v = (_norm(r["first"]), _norm(r["last"]), r["dob"])
                elif key == "email":
                    v = r["email"].strip().lower()
                    if not v:
                        continue
                elif key == "name_phone":
                    v = (_norm(r["first"]), _norm(r["last"]), _digits(r["phone"]))
                elif key == "phone":
                    v = _digits(r["phone"])
                elif key == "name":
                    v = (_norm(r["first"]), _norm(r["last"]))
                if v in seen:
                    parent[find(i)] = find(seen[v])
                else:
                    seen[v] = i
        out[adm] = len({find(i) for i in range(len(mine))})
    return out


def completion(target, appl=None):
    """Each component's completion rate: the candidates who sat it over the people who applied, the four
    administrations together, in per cent."""
    appl = appl or applicants(target)
    n = sat_counts(target)
    tot = sum(appl.values())
    return {c: 100.0 * n[c] / tot for c in COMP}
