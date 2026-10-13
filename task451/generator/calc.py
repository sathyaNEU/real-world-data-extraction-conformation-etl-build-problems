"""Every computation on the shipped files, the way a solver would run it: final claim versions, attributed member
months, the agreement's truncation, the paid-date and received-date lag triangles and each completion route, each
partner's total cost of care per member month against its target; and the two asks (pharmacy spending through
Corvane's cardholder and person code, professional spending outside the partner on the date of service)."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import pack as P
import world as W


def mkey_series(s):
    d = pd.to_datetime(s)
    return d.dt.year * 12 + d.dt.month - 1


def mkey(d):
    return d.year * 12 + d.month - 1


CUTM = mkey(W.CUT)
GOLIVEM = mkey(W.GOLIVE)
S0 = mkey(W.SERVICE_FROM)


# ------------------------------------------------------------------------------------------------------- loading
def load(target):
    f = lambda k: os.path.join(target, P.FILES[k])
    cl = pd.read_csv(f("claims"), dtype={"claim_number": str, "member_id": str, "rendering_npi": str, "billing_npi": str,
                                         "bill_type": str, "place_of_service": str, "claim_frequency_code": str})
    el = pd.read_csv(f("elig"), dtype=str)
    ro = pd.read_csv(f("roster"), dtype=str)
    rx = pd.read_csv(f("rx"), dtype={"cardholder_id": str, "person_code": str, "rx_number": str, "claim_id": str})
    import openpyxl
    ws = openpyxl.load_workbook(f("clinicians"), read_only=True)["Clinicians"]
    rows = []
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0]:
            rows.append(dict(npi=str(r[0]), partner_code=r[1], role=r[3], specialty=r[4],
                             since=r[5].date() if hasattr(r[5], "date") else r[5]))
    di = pd.DataFrame(rows)
    return dict(claims=cl, elig=el, roster=ro, rx=rx, directory=di)


# ------------------------------------------------------------------------------------------------------- claims
def final_claims(cl):
    """the final action claim: each claim's latest version (a void leaves the claim at zero)"""
    last = cl.sort_values(["claim_number", "claim_version"]).groupby("claim_number").tail(1)
    first = cl[cl["claim_version"] == 1].set_index("claim_number")
    out = last.set_index("claim_number")
    out["received_date"] = first["received_date"]
    out["first_paid_date"] = first["paid_date"]
    return out.reset_index()


def eligible_months(el):
    """(member, month) pairs covered on the latest version of every span"""
    last = el.sort_values(["span_id", "span_version"]).groupby("span_id").tail(1)
    pairs = set()
    end_all = mkey(W.SERVICE_TO)
    for r in last.itertuples():
        a = mkey(dt.date.fromisoformat(r.coverage_start))
        if isinstance(r.coverage_end, str) and r.coverage_end:
            e = dt.date.fromisoformat(r.coverage_end)
            if e < dt.date.fromisoformat(r.coverage_start):
                continue
            b = mkey(e)
        else:
            b = end_all
        for k in range(a, b + 1):
            pairs.add((r.member_id, k))
    return pairs


def attribution(ro):
    m = ro.copy()
    m["k"] = mkey_series(m["roster_month"])
    return {(a, b): c for a, b, c in zip(m["member_id"], m["k"], m["partner_code"])}


def member_months(ro, elig_pairs, require_eligible=True):
    att = attribution(ro)
    mm = {c: 0 for c in W.CODES}
    for (mid, k), code in att.items():
        if not require_eligible or (mid, k) in elig_pairs:
            mm[code] += 1
    return mm


def frame2026(fc, att):
    """the 2026 medical claims (first date of service in 2026), each with its service month and partner"""
    d = fc.copy()
    d["k"] = mkey_series(d["service_from_date"])
    d = d[(d["k"] >= YEARM) & (d["k"] < YEARM + 12)].copy()
    d["partner"] = [att.get((m, k)) for m, k in zip(d["member_id"], d["k"])]
    return d


YEARM = W.YEAR * 12


def truncation(d26):
    """each member's 2026 amount above the agreement's $200,000, shared across partners by the member's amounts"""
    tot = d26.groupby("member_id")["paid_amount"].sum()
    over = tot[tot > W.TRUNCATION]
    excess = {c: 0.0 for c in W.CODES}
    detail = []
    for mid, t in over.items():
        sub = d26[(d26["member_id"] == mid) & d26["partner"].notna()].groupby("partner")["paid_amount"].sum()
        for code, a in sub.items():
            excess[code] += (t - W.TRUNCATION) * a / t
        detail.append((mid, float(t)))
    return excess, detail


# ------------------------------------------------------------------------------------------------------ triangles
def triangles(cl, fc):
    """paid-date triangle (each version's payment in the month it was paid), received-date triangle (each claim's
    paid amount at the cut in the month it was received) and the paid-date triangle on latest versions (each claim's
    paid amount at the cut in the month its latest version was paid), by month of first service, cumulative by lag"""
    NL = CUTM - S0 + 1
    p = cl.copy()
    p["s"] = mkey_series(p["service_from_date"])
    p["L"] = mkey_series(p["paid_date"]) - p["s"]
    r = fc.copy()
    r["s"] = mkey_series(r["service_from_date"])
    r["L"] = mkey_series(r["received_date"]) - r["s"]
    q = fc.copy()
    q["s"] = mkey_series(q["service_from_date"])
    q["L"] = mkey_series(q["paid_date"]) - q["s"]
    out = {}
    for nm, df, col in (("paid", p, "payment_amount"), ("received", r, "paid_amount"), ("paid_final", q, "paid_amount")):
        inc = np.zeros((NL, NL))
        g = df.groupby(["s", "L"])[col].sum()
        for (s, L), v in g.items():
            i = s - S0
            if 0 <= i < NL and 0 <= L < NL:
                inc[i, L] += v
        T = np.cumsum(inc, axis=1)
        for i in range(NL):
            T[i, NL - i:] = np.nan
        out[nm] = T
    return out


def by_type_triangles(cl, fc):
    out = {}
    for t, form, bt in (("P", "CMS1500", None), ("O", "UB04", "0131"), ("I", "UB04", "0111")):
        sel_c = cl["claim_form"].eq(form) & (cl["bill_type"].eq(bt) if bt else True)
        sel_f = fc["claim_form"].eq(form) & (fc["bill_type"].eq(bt) if bt else True)
        out[t] = triangles(cl[sel_c], fc[sel_f])
    return out


def factors(T, ok=None):
    """volume-weighted link ratios; ok(m) keeps the cells whose later month m (payment or receipt month) qualifies"""
    NL = T.shape[0]
    f = np.ones(NL)
    for L in range(NL - 1):
        num = den = 0.0
        for i in range(NL - L - 1):
            if ok is not None and not ok(S0 + i + L + 1):
                continue
            num += T[i, L + 1]
            den += T[i, L]
        f[L] = num / den if den > 0 else 1.0
    return f


def completion(f):
    """completion factor for each service month at its lag at the cut"""
    NL = len(f)
    cf = np.ones(NL)
    for i in range(NL):
        L = NL - 1 - i
        cf[i] = float(np.prod(f[L:NL - 1])) if L < NL - 1 else 1.0
    return cf


METHODS = {
    "R0 paid, all development": ("paid", None),
    "paid, latest 12 months": ("paid", lambda m: m > CUTM - 12),
    "paid, latest 6 months": ("paid", lambda m: m > CUTM - 6),
    "paid, latest 4 months": ("paid", lambda m: m > CUTM - 4),
    "G3 paid, after the go-live month": ("paid", lambda m: m > GOLIVEM),
    "G1 received, all development": ("received", None),
    "G2 received, latest 12 months": ("received", lambda m: m > CUTM - 12),
    "G5 paid (latest versions), after the go-live month": ("paid_final", lambda m: m > GOLIVEM),
}
GOLDEN = ("G1 received, all development", "G2 received, latest 12 months", "G3 paid, after the go-live month",
          "G4 received, by claim type", "G5 paid (latest versions), after the go-live month")


def completion_factors(tri, tri_t):
    cf = {}
    for nm, (basis, ok) in METHODS.items():
        cf[nm] = completion(factors(tri[basis], ok))
    cf["R1 paid as extracted"] = np.ones(tri["paid"].shape[0])
    cf["G4 received, by claim type"] = {t: completion(factors(tri_t[t]["received"])) for t in tri_t}
    return cf


def partner_amounts(d26):
    """each partner's paid amount at the cut by service month (index 0 = January 2026), in total and by claim type"""
    tot = {c: np.zeros(12) for c in W.CODES}
    typ = {c: {t: np.zeros(12) for t in "POI"} for c in W.CODES}
    d = d26[d26["partner"].notna()]
    tcol = np.where(d["claim_form"].eq("CMS1500"), "P", np.where(d["bill_type"].eq("0111"), "I", "O"))
    g = d.assign(t=tcol).groupby(["partner", "k", "t"])["paid_amount"].sum()
    for (code, k, t), v in g.items():
        tot[code][k - YEARM] += v
        typ[code][t][k - YEARM] += v
    return tot, typ


def tcoc(cf, amounts, amounts_t, excess, mm):
    """each partner's completed 2026 total cost of care, the truncation excess taken off, per member month"""
    i0 = YEARM - S0
    out = {}
    for code in W.CODES:
        if isinstance(cf, dict):
            comp = sum(float(np.dot(cf[t][i0:i0 + 12], amounts_t[code][t])) for t in "POI")
        else:
            comp = float(np.dot(cf[i0:i0 + 12], amounts[code]))
        out[code] = (comp - excess[code]) / mm[code]
    return out


def compute(target, targets=None):
    L = load(target)
    cl = L["claims"]
    fc = final_claims(cl)
    elig = eligible_months(L["elig"])
    att = attribution(L["roster"])
    mm = member_months(L["roster"], elig)
    d26 = frame2026(fc, att)
    excess, cats = truncation(d26)
    tri = triangles(cl, fc)
    tri_t = by_type_triangles(cl, fc)
    cf = completion_factors(tri, tri_t)
    amt, amt_t = partner_amounts(d26)
    pmpm = {nm: tcoc(c, amt, amt_t, excess, mm) for nm, c in cf.items()}
    out = dict(L=L, fc=fc, elig=elig, att=att, mm=mm, d26=d26, excess=excess, cats=cats, tri=tri, cf=cf, amt=amt,
               amt_t=amt_t, pmpm=pmpm)
    if targets:
        out["flags"] = {nm: sorted(c for c in W.CODES if v[c] > targets[c] * (1 + W.CORRIDOR)) for nm, v in pmpm.items()}
    return out


# ---------------------------------------------------------------------------------------------------------- asks
def rx_members(el):
    """Corvane's patient to the Fund's member: the cardholder is the participant's id; within the family the patient
    is the member with the same birth date and gender"""
    last = el.sort_values(["span_id", "span_version"]).groupby("span_id").tail(1)
    fam = {}
    for r in last.itertuples():
        fam.setdefault((r.subscriber_id, r.birth_date, r.gender), set()).add(r.member_id)
    return fam


def rx_net(rx):
    sign = rx["transaction_code"].map({"B1": 1.0, "B3": 1.0, "B2": -1.0})
    return rx.assign(net=rx["plan_paid"] * sign)


def ask_pharmacy(L, att, how="dob", elig=None):
    """the Fund's net plan paid for 2026 fills in the member's attributed member months with each partner (B.4.1(a):
    on the roster for the fill month and eligible in it, on the latest version of the spans)"""
    rx = rx_net(L["rx"])
    rx = rx[pd.to_datetime(rx["fill_date"]).dt.year == W.YEAR]
    k = mkey_series(rx["fill_date"])
    if how == "dob":
        fam = rx_members(L["elig"])
        mids = [next(iter(fam.get((c, b, g), {None}))) for c, b, g in zip(rx["cardholder_id"], rx["patient_birth_date"], rx["patient_gender"])]
    elif how == "person_code":
        mids = [c + "-" + pc for c, pc in zip(rx["cardholder_id"], rx["person_code"])]
    elif how == "cardholder":
        mids = [c + "-01" for c in rx["cardholder_id"]]
    out = {c: 0.0 for c in W.CODES}
    for mid, kk, v in zip(mids, k, rx["net"]):
        code = att.get((mid, kk))
        if code and (elig is None or (mid, kk) in elig):
            out[code] += v
    return out


def ask_leakage(L, d26, group_npi, how="billing"):
    """the share of each partner's 2026 professional spending (paid through the cut) rendered by clinicians who were
    not with the partner group when the service was given: the claim's billing group (golden), or the January roster
    of clinicians read for the whole year (snapshot), or the roster with its 'with partner since' dates (since)"""
    prof = d26[d26["claim_form"].eq("CMS1500") & d26["partner"].notna()]
    di = L["directory"]
    cur = dict(zip(di["npi"], di["partner_code"]))
    since = dict(zip(di["npi"], di["since"]))
    out = {}
    for code, g in prof.groupby("partner"):
        tot = g["paid_amount"].sum()
        if how == "billing":
            inside = (g["billing_npi"] == group_npi[code]).to_numpy()
        elif how == "snapshot":
            inside = np.array([cur.get(n) == code for n in g["rendering_npi"]])
        else:
            inside = np.array([cur.get(n) == code and dt.date.fromisoformat(d) >= since[n]
                               for n, d in zip(g["rendering_npi"], g["service_from_date"])])
        out[code] = float(g["paid_amount"][~inside].sum() / tot * 100) if tot > 0 else 0.0
    return out
