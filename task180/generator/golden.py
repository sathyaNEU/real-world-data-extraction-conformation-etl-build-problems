"""The analysis, from the shipped bundle alone (target/): new users under SOP-PV-14, admissions for each event
under its case definition, and every comparison the ladder names, from the spontaneous-report count to the
comparison of each new user's first month with the same person's later time on the medicine.

Conventions of the golden figures (each is one cell of the grid the checks walk):
  new users      a dispensing not returned, with no dispensing of the substance (any of its ATC codes) in the
                 365 days before, resident in Denmark for those 365 days; all such starts in the extract
  events         admissions (LPR3 contacts linked when one starts within 4 hours of the previous one's end; LPR2
                 records linked when one starts on the day the previous one ends), dated by their first contact
  observation    ends at death, at the first emigration after the start or on 30 June 2026 (days inclusive)
  the ratio      days 1 to 30 after each start against days 61 to 180 after the same start (each start its own
                 stratum), conditional Poisson maximum likelihood, 95 per cent Wald interval on the log scale
"""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd

PRESCRIPTIONS = "prescription_registry_2018-2026.parquet"
CONTACTS = "patient_registry_contacts_2018-2026.parquet"
DIAGNOSES = "patient_registry_diagnoses_2018-2026.parquet"
CIVIL = "civil_registration_extract.csv"
MATCHED = "matched_comparators.csv"
ATC = "atc_ddd_index_2026.csv"
POPULATION = "population_and_admissions_2022-2025.csv"
SCREEN = "pv_signal_screen_2026Q3.xlsx"

EPOCH = dt.date(2018, 1, 1)
END_DATE = dt.date(2026, 6, 30)
NEW = ("tasorexant", "corinurad", "velaglutide")
ACTIVE = {"tasorexant": "zopiclone", "corinurad": "allopurinol", "velaglutide": "orlistat"}
EVENT = {"tasorexant": "fall", "corinurad": "aki", "velaglutide": "pancreatitis"}
PT = {"tasorexant": "Fall", "corinurad": "Acute kidney injury", "velaglutide": "Pancreatitis acute"}
BIG = 10 ** 7
MIN_DAY = 1440
Z = 1.959964


def day(d):
    return (d - EPOCH).days


END = day(END_DATE)
Y2022, Y2023, Y2025, Y2026 = day(dt.date(2022, 1, 1)), day(dt.date(2023, 1, 1)), day(dt.date(2025, 1, 1)), \
    day(dt.date(2026, 1, 1))
LAST_START = day(dt.date(2026, 5, 31))
# half-year index h = 2 * year + (1 from July); HALF_START[h - H0] is its first day
HALF = {2 * y + k: day(dt.date(y, 7 if k else 1, 1)) for y in range(2017, 2028) for k in (0, 1)}
H0 = min(HALF)
HALF_START = np.array([HALF[h] for h in range(H0, max(HALF) + 1)], np.int64)

CHARLSON = {
    "mi": ["DI21", "DI22", "DI23"], "chf": ["DI50", "DI110", "DI130", "DI132"],
    "pvd": ["DI70", "DI71", "DI72", "DI73", "DI74", "DI77"],
    "cvd": ["DI6", "DG45", "DG46"], "dementia": ["DF00", "DF01", "DF02", "DF03", "DF051", "DG30"],
    "cpd": ["DJ40", "DJ41", "DJ42", "DJ43", "DJ44", "DJ45", "DJ46", "DJ47", "DJ60", "DJ61", "DJ62", "DJ63", "DJ64",
            "DJ65", "DJ66", "DJ67", "DJ684", "DJ701", "DJ703", "DJ841", "DJ920", "DJ961", "DJ982", "DJ983"],
    "ctd": ["DM05", "DM06", "DM08", "DM09", "DM30", "DM31", "DM32", "DM33", "DM34", "DM35", "DM36", "DD86"],
    "ulcer": ["DK221", "DK25", "DK26", "DK27", "DK28"],
    "mild_liver": ["DB18", "DK700", "DK701", "DK702", "DK703", "DK709", "DK71", "DK73", "DK74", "DK760"],
    "diabetes": ["DE100", "DE101", "DE109", "DE110", "DE111", "DE119"],
    "hemiplegia": ["DG81", "DG82"],
    "renal": ["DI12", "DI13", "DN00", "DN01", "DN02", "DN03", "DN04", "DN05", "DN07", "DN11", "DN14", "DN17",
              "DN18", "DN19", "DQ61"],
    "diabetes_comp": ["DE102", "DE103", "DE104", "DE105", "DE106", "DE107", "DE108", "DE112", "DE113", "DE114",
                      "DE115", "DE116", "DE117", "DE118"],
    "tumour": ["DC0", "DC1", "DC2", "DC3", "DC4", "DC5", "DC6", "DC70", "DC71", "DC72", "DC73", "DC74", "DC75"],
    "leukaemia": ["DC91", "DC92", "DC93", "DC94", "DC95"],
    "lymphoma": ["DC81", "DC82", "DC83", "DC84", "DC85", "DC88", "DC90", "DC96"],
    "severe_liver": ["DB150", "DB160", "DB162", "DB190", "DI85", "DK704", "DK72", "DK766"],
    "metastatic": ["DC76", "DC77", "DC78", "DC79", "DC80"], "aids": ["DB21", "DB22", "DB23", "DB24"],
}


# ------------------------------------------------------------------ loading

class Data:
    pass


def _days(series):
    x = pd.to_datetime(series.replace("", None), errors="coerce")
    out = np.full(len(series), BIG, np.int64)
    ok = x.notna().to_numpy()
    out[ok] = (x[ok].to_numpy().astype("datetime64[D]") - np.datetime64(EPOCH)).astype(np.int64)
    return out


def load(target):
    D = Data()
    civ = pd.read_csv(os.path.join(target, CIVIL), dtype=str, keep_default_na=False)
    D.pnr = civ["pnr"].to_numpy(object)
    D.pid_of = pd.Series(np.arange(len(civ)), index=civ["pnr"])
    D.n = len(civ)
    D.birth_year = civ["foedselsaar"].astype(int).to_numpy()
    D.female = (civ["koen"] == "K").to_numpy()
    D.death, D.emig, D.imm = _days(civ["doedsdato"]), _days(civ["udvandringsdato"]), _days(civ["indvandringsdato"])
    rx = pd.read_parquet(os.path.join(target, PRESCRIPTIONS))
    D.rx = pd.DataFrame({"pid": D.pid_of.reindex(rx["pnr"]).to_numpy(np.int64),
                         "day": (rx["eksd"].to_numpy().astype("datetime64[D]") - np.datetime64(EPOCH)).astype(np.int64),
                         "atc": rx["atc"].to_numpy(object), "vnr": rx["vnr"].to_numpy(object),
                         "apk": rx["apk"].to_numpy(np.int64)})
    atc = pd.read_csv(os.path.join(target, ATC), sep=";", dtype=str, keep_default_na=False)
    D.codes = {s: sorted(g["atc"]) for s, g in atc.groupby("substans")}
    D.current_code = {s: sorted(g[g["gyldig_til"] == ""]["atc"]) for s, g in atc.groupby("substans")}
    c = pd.read_parquet(os.path.join(target, CONTACTS))
    em = np.datetime64(EPOCH, "m")
    endv = c["sluttid"].to_numpy().astype("datetime64[m]")
    nat = np.isnat(endv)
    end = np.full(len(c), -1, np.int64)
    end[~nat] = (endv[~nat] - em).astype(np.int64)
    D.c = pd.DataFrame({
        "pid": D.pid_of.reindex(c["pnr"]).to_numpy(np.int64),
        "kid": c["kontakt_id"].to_numpy(object),
        "lpr2": (c["kilde"] == "LPR2").to_numpy(),
        "pattype": c["pattype"].fillna("").to_numpy(object),
        "acute": (c["prioritet"] == "ATA1").to_numpy(),
        "physical": (c["kontakttype"].fillna("ALCA00") == "ALCA00").to_numpy(),
        "start": (c["starttid"].to_numpy().astype("datetime64[m]") - em).astype(np.int64),
        "end": end,
        "ongoing": nat,
    }).sort_values(["pid", "start", "kid"], kind="stable").reset_index(drop=True)
    dx = pd.read_parquet(os.path.join(target, DIAGNOSES))
    row_of = pd.Series(np.arange(len(D.c)), index=D.c["kid"])
    D.dx = pd.DataFrame({"row": row_of.reindex(dx["kontakt_id"]).to_numpy(np.int64),
                         "code": dx["diagnosekode"].to_numpy(object), "type": dx["diagnosetype"].to_numpy(object)})
    m = pd.read_csv(os.path.join(target, MATCHED), dtype=str)
    D.matched = pd.DataFrame({"set": m["saet_id"].to_numpy(), "substance": m["substans"].to_numpy(),
                              "user": (m["rolle"] == "bruger").to_numpy(),
                              "pid": D.pid_of.reindex(m["pnr"]).to_numpy(np.int64),
                              "day": _days(m["indeksdato"])})
    D.pop = pd.read_csv(os.path.join(target, POPULATION))
    D.screen = read_screen(os.path.join(target, SCREEN))
    D.cache = {}
    return D


def read_screen(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Line listing"]
    hdr, out = None, []
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Case number":
            hdr = list(r)
            continue
        if hdr and r and r[0]:
            out.append(dict(zip(hdr, r)))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ dispensings and new users

def valid_dispensings(D, substance, net=True, current_only=False):
    codes = D.current_code[substance] if current_only else D.codes[substance]
    rx = D.rx[D.rx["atc"].isin(codes)]
    pid, d, v, a = rx["pid"].to_numpy(), rx["day"].to_numpy(), rx["vnr"].astype(np.int64).to_numpy(), \
        rx["apk"].to_numpy()
    pos = np.where(a > 0)[0]
    keep = np.ones(len(pos), bool)
    if net:
        neg = np.where(a < 0)[0]
        kp = (pid[pos] * 10 ** 6 + v[pos]) * 10 ** 5 + d[pos]
        o = np.argsort(kp, kind="stable")
        kps, poss = kp[o], np.arange(len(pos))[o]
        kn = (pid[neg] * 10 ** 6 + v[neg]) * 10 ** 5 + d[neg]
        at = np.searchsorted(kps, kn, side="right") - 1
        ok = at >= 0
        ok[ok] = (kps[at[ok]] // 10 ** 5) == (kn[ok] // 10 ** 5)
        keep[poss[at[ok]]] = False
    p, dd = pid[pos][keep], d[pos][keep]
    o = np.lexsort((dd, p))
    return p[o], dd[o]


def resident_through(D, pid, a, b):
    """True where the person was resident in Denmark on every day of [a, b]."""
    I, U = D.imm[pid], D.emig[pid]
    hasI, hasU = I < BIG, U < BIG
    ok = np.ones(len(pid), bool)
    only_u = ~hasI & hasU
    ok[only_u] = b[only_u] < U[only_u]
    only_i = hasI & ~hasU
    ok[only_i] = a[only_i] >= I[only_i]
    back = hasI & hasU & (I > U)
    ok[back] = (b[back] < U[back]) | (a[back] >= I[back])
    came = hasI & hasU & (I <= U)
    ok[came] = (a[came] >= I[came]) & (b[came] < U[came])
    return ok


def year_of(d):
    return (np.datetime64(EPOCH) + np.asarray(d).astype("timedelta64[D]")).astype("datetime64[Y]").astype(int) + 1970


def new_users(D, substance, washout=365, residence=True, net=True, current_only=False):
    """New-user starts, a DataFrame of pid and day sorted by both. washout: 365 (the rule), 'first' (each person's
    first dispensing only) or 'year' (each person's first dispensing in each calendar year)."""
    key = ("starts", substance, washout, residence, net, current_only)
    if key in D.cache:
        return D.cache[key]
    p, d = valid_dispensings(D, substance, net=net, current_only=current_only)
    same = np.r_[False, p[1:] == p[:-1]]
    gap = np.r_[BIG, np.diff(d)]
    if washout == 365:
        st = ~same | (gap > 365)
    elif washout == "first":
        st = ~same
    else:
        yr = year_of(d)
        st = ~same | np.r_[True, yr[1:] != yr[:-1]]
    p, d = p[st], d[st]
    if residence:
        ok = resident_through(D, p, d - 365, d)
        p, d = p[ok], d[ok]
    out = pd.DataFrame({"pid": p, "day": d})
    D.cache[key] = out
    return out


def obs_end_after(D, pid, s, censor=True):
    """End of observation for a start on day s: death, the first emigration on or after s, or 30 June 2026."""
    if not censor:
        return np.full(len(pid), END, np.int64)
    e = np.minimum(D.death[pid], END)
    U = D.emig[pid]
    return np.where((U < BIG) & (U >= s), np.minimum(e, U), e)


# ------------------------------------------------------------------ admissions and events

def admissions(D, link_hours=4.0, merge=True):
    key = ("adm", link_hours, merge)
    if key in D.cache:
        return D.cache[key]
    c = D.c
    pid, start, end = c["pid"].to_numpy(), c["start"].to_numpy(), c["end"].to_numpy()
    lpr2, pat = c["lpr2"].to_numpy(), c["pattype"].to_numpy()
    acute, phys = c["acute"].to_numpy(), c["physical"].to_numpy()
    staylike = np.where(lpr2, np.isin(pat, ["0", "3"]), phys)
    link = np.zeros(len(c), bool)
    if merge:
        same = np.r_[False, pid[1:] == pid[:-1]]
        pe = np.r_[-1, end[:-1]]
        prev_lpr2 = np.r_[False, lpr2[:-1]]
        prev_stay = np.r_[False, staylike[:-1]]
        g3 = same & ~lpr2 & ~prev_lpr2 & staylike & prev_stay & (pe >= 0) & (start - pe <= link_hours * 60) & \
            (start >= pe)
        g2 = same & lpr2 & prev_lpr2 & staylike & prev_stay & (pe >= 0) & (start // MIN_DAY == pe // MIN_DAY)
        link = g3 | g2
    adm = np.cumsum(~link) - 1
    n = adm[-1] + 1
    a_start, a_pid = start[~link], pid[~link]
    a_end = np.full(n, -1, np.int64)
    np.maximum.at(a_end, adm, np.where(end >= 0, end, -1))
    ongoing = np.zeros(n, bool)
    np.logical_or.at(ongoing, adm, c["ongoing"].to_numpy())
    em = np.zeros(n, bool)
    np.logical_or.at(em, adm, np.where(lpr2, pat == "3", acute & phys))
    inpat2 = np.zeros(n, bool)
    np.logical_or.at(inpat2, adm, lpr2 & (pat == "0"))
    any3 = np.zeros(n, bool)
    np.logical_or.at(any3, adm, ~lpr2 & phys)
    dur = np.where(a_end >= 0, a_end - a_start, BIG)
    inpatient = inpat2 | (any3 & ((dur >= 12 * 60) | ongoing))
    A = dict(adm=adm, pid=a_pid, start=a_start, day=a_start // MIN_DAY, emergency=em, inpatient=inpatient)
    D.cache[key] = A
    return A


def code_flags(D):
    if "flags" in D.cache:
        return D.cache["flags"]
    code = D.dx["code"]
    num = pd.to_numeric(code.str[2:4], errors="coerce").fillna(99).astype(int).to_numpy()
    f = dict(injury=(code.str.startswith("DS") | (code.str.startswith("DT") & (num <= 14))).to_numpy(),
             fall=(code.str.startswith("DW") & (num <= 19)).to_numpy(),
             aki=code.str.startswith("DN17").to_numpy(), pancreatitis=code.str.startswith("DK85").to_numpy(),
             action=(D.dx["type"] == "A").to_numpy())
    D.cache["flags"] = f
    return f


def events(D, kind, link_hours=4.0, merge=True, secondary=False, outpatient=False):
    """Admissions meeting the case definition: (pid, day) sorted, one row per admission. secondary counts secondary
    diagnoses where the definition says action diagnosis; outpatient drops the emergency or inpatient condition."""
    key = ("ev", kind, link_hours, merge, secondary, outpatient)
    if key in D.cache:
        return D.cache[key]
    A = admissions(D, link_hours, merge)
    f = code_flags(D)
    adm = A["adm"][D.dx["row"].to_numpy()]
    act = f["action"] | secondary
    n = len(A["pid"])
    if kind == "fall":
        has_inj = np.zeros(n, bool)
        np.logical_or.at(has_inj, adm, f["injury"] & act)
        has_fall = np.zeros(n, bool)
        np.logical_or.at(has_fall, adm, f["fall"])
        sel = has_inj & has_fall & ((A["emergency"] | A["inpatient"]) | outpatient)
    else:
        has = np.zeros(n, bool)
        np.logical_or.at(has, adm, f[kind] & act)
        sel = has & (A["inpatient"] | outpatient)
    p, d = A["pid"][sel], A["day"][sel]
    o = np.lexsort((d, p))
    out = (p[o].astype(np.int64), d[o].astype(np.int64))
    D.cache[key] = out
    return out


def count_in(ev, pid, lo, hi):
    """Events of each person in [lo, hi] (days, inclusive); zero where hi < lo."""
    key = ev[0] * 10 ** 6 + ev[1]
    a = np.searchsorted(key, pid * 10 ** 6 + lo, side="left")
    b = np.searchsorted(key, pid * 10 ** 6 + hi, side="right")
    return np.where(hi >= lo, b - a, 0)


# ------------------------------------------------------------------ estimators

def cpois(a, b, r, c):
    """Conditional Poisson MLE of the rate ratio, two windows per stratum (a, b events; r, c days); Wald interval."""
    use = (a + b > 0) & (r > 0) & (c > 0)
    a, b, r, c = a[use].astype(float), b[use].astype(float), r[use].astype(float), c[use].astype(float)
    n = a + b
    beta = np.log(max(a.sum(), 0.5) / r.sum() / (max(b.sum(), 0.5) / c.sum()))
    info = 1.0
    for _ in range(100):
        p = r * np.exp(beta) / (r * np.exp(beta) + c)
        score = a.sum() - (n * p).sum()
        info = (n * p * (1 - p)).sum()
        step = score / info
        beta += step
        if abs(step) < 1e-13:
            break
    se = 1 / np.sqrt(info)
    return float(np.exp(beta)), float(np.exp(beta - Z * se)), float(np.exp(beta + Z * se))


def mh(a, b, r, c):
    t = (r + c).astype(float)
    use = t > 0
    return float((a * c / np.where(use, t, 1))[use].sum() / (b * r / np.where(use, t, 1))[use].sum())


def cpois_adjusted(stratum, exposed, age_band, half, days, n_ev):
    """Conditional Poisson with the exposure, age band and half-year, conditioning on the stratum."""
    keep = days > 0
    stratum, exposed, age_band, half, days, n_ev = (x[keep] for x in (stratum, exposed, age_band, half, days, n_ev))
    _, stratum = np.unique(stratum, return_inverse=True)
    N = np.bincount(stratum, weights=n_ev)
    keep = N[stratum] > 0
    stratum, exposed, age_band, half, days, n_ev = (x[keep] for x in (stratum, exposed, age_band, half, days, n_ev))
    _, stratum = np.unique(stratum, return_inverse=True)
    N = np.bincount(stratum, weights=n_ev)
    la = np.unique(age_band, return_inverse=True)[1]
    lp = np.unique(half, return_inverse=True)[1]
    cols = [exposed.astype(float)] + [(la == k).astype(float) for k in range(1, la.max() + 1)] + \
        [(lp == k).astype(float) for k in range(1, lp.max() + 1)]
    X = np.column_stack(cols)
    cnt = np.bincount(stratum, minlength=len(N))
    keepc = [0]
    for j in range(1, X.shape[1]):
        s1 = np.bincount(stratum, weights=X[:, j], minlength=len(N))
        if np.any((s1 > 0) & (s1 < cnt)):
            keepc.append(j)
    X = X[:, keepc]
    logt = np.log(days.astype(float))
    theta = np.zeros(X.shape[1])
    H = np.eye(X.shape[1])
    ridge = np.r_[0.0, np.full(X.shape[1] - 1, 1e-6)]
    for _ in range(200):
        eta = X @ theta + logt
        mx = np.full(len(N), -np.inf)
        np.maximum.at(mx, stratum, eta)
        w = np.exp(eta - mx[stratum])
        p = w / np.bincount(stratum, weights=w)[stratum]
        S1 = np.column_stack([np.bincount(stratum, weights=p * X[:, j], minlength=len(N)) for j in range(X.shape[1])])
        grad = X.T @ n_ev - N @ S1 - ridge * theta
        H = X.T @ (X * (N[stratum] * p)[:, None]) - (S1 * N[:, None]).T @ S1 + np.diag(ridge) + np.eye(len(theta)) * 1e-12
        step = np.linalg.solve(H, grad)
        big = np.abs(step).max()
        if big > 2.0:
            step *= 2.0 / big
        theta += step
        if big < 1e-11:
            break
    se = np.sqrt(np.linalg.inv(H)[0, 0])
    b = theta[0]
    return float(np.exp(b)), float(np.exp(b - Z * se)), float(np.exp(b + Z * se))


# ------------------------------------------------------------------ the self-controlled comparisons

def episodes(D, substance, first_day=None, censor=True, nu=()):
    """Every new-user start (pid, day) and its last observed day (capped the day before the person's next start).
    nu: new-user options as a tuple of (name, value) pairs, for the stops."""
    key = ("episodes", substance, first_day, censor, nu)
    if key in D.cache:
        return D.cache[key]
    allst = new_users(D, substance, **dict(nu))
    ap, ad = allst["pid"].to_numpy(), allst["day"].to_numpy()
    nxt = np.where(np.r_[ap[1:] == ap[:-1], False], np.r_[ad[1:], 0], BIG)
    e = np.minimum(obs_end_after(D, ap, ad, censor), nxt - 1)
    keep = ad >= (first_day if first_day is not None else -BIG)
    out = (ap[keep], ad[keep], e[keep])
    D.cache[key] = out
    return out


def window(ev, pid, s, e, a, b):
    """Events and observed days in [s + a, s + b] (b None runs to e), cut at e."""
    lo = s + a
    hi = np.minimum(s + b, e) if b is not None else e
    return count_in(ev, pid, lo, hi), np.maximum(0, hi - lo + 1), lo, hi


def split_half_years(st, ex, pid, lo, hi, birth_year):
    """Cut labelled segments at half-year boundaries: stratum, exposed, pid, five-year age band, half-year, lo, hi."""
    ok = hi >= lo
    st, ex, pid, lo, hi = st[ok], ex[ok], pid[ok], lo[ok], hi[ok]
    h0 = np.searchsorted(HALF_START, lo, side="right") - 1
    h1 = np.searchsorted(HALF_START, hi, side="right") - 1
    k = h1 - h0 + 1
    rep = np.repeat(np.arange(len(st)), k)
    off = np.arange(len(rep)) - np.repeat(np.cumsum(np.r_[0, k[:-1]]), k)
    h = h0[rep] + off
    plo = np.maximum(lo[rep], HALF_START[h])
    phi = np.minimum(hi[rep], HALF_START[h + 1] - 1)
    band = ((h + H0) // 2 - birth_year[pid[rep]]) // 5
    return st[rep], ex[rep], pid[rep], band, h, plo, phi


def _fit(st, ex, pid, lo, hi, ev, D, adjust, estimator):
    """adjust: False, 'age' (five-year age bands) or 'age+half' (age bands and calendar half-years)."""
    if not adjust:
        n = count_in(ev, pid, lo, hi)
        days = np.maximum(0, hi - lo + 1)
        k = st.max() + 1
        a = np.bincount(st[ex], weights=n[ex], minlength=k)
        r = np.bincount(st[ex], weights=days[ex], minlength=k)
        b = np.bincount(st[~ex], weights=n[~ex], minlength=k)
        c = np.bincount(st[~ex], weights=days[~ex], minlength=k)
        return cpois(a, b, r, c) if estimator == "cpois" else (mh(a, b, r, c), None, None)
    st2, ex2, pid2, band, h, plo, phi = split_half_years(st, ex, pid, lo, hi, D.birth_year)
    if adjust == "age":
        h = np.zeros_like(h)
    n = count_in(ev, pid2, plo, phi)
    days = np.maximum(0, phi - plo + 1)
    if estimator == "cpois":
        return cpois_adjusted(st2, ex2, band, h, days, n)
    key = (st2.astype(np.int64) * 100 + (band - band.min())) * 100 + h
    _, inv = np.unique(key, return_inverse=True)
    k = inv.max() + 1
    a = np.bincount(inv[ex2], weights=n[ex2], minlength=k)
    r = np.bincount(inv[ex2], weights=days[ex2], minlength=k)
    b = np.bincount(inv[~ex2], weights=n[~ex2], minlength=k)
    c = np.bincount(inv[~ex2], weights=days[~ex2], minlength=k)
    return mh(a, b, r, c), None, None


def sccs(D, substance, risk=(1, 30), control=(61, 180), adjust=False, estimator="cpois", first_day=None,
         censor=True, ev=None, subset=None, pre=30, nu=()):
    """The self-controlled comparison. control (a, None) runs to the end of observation (or the next start);
    control 'full' uses all observed time from 1 January 2022 with days -30 to the day before the risk window set
    aside around every start. subset: a mask over the episodes (e.g. no NSAID in days 0 to 30)."""
    if ev is None:
        ev = events(D, EVENT[substance])
    pid, s, e = episodes(D, substance, first_day, censor, nu)
    if subset is not None:
        pid, s, e = pid[subset], s[subset], e[subset]
    if control != "full":
        a, r, rlo, rhi = window(ev, pid, s, e, *risk)
        b, c, clo, chi = window(ev, pid, s, e, *control)
        use = (a + b) > 0
        k = np.arange(use.sum())
        st = np.r_[k, k]
        ex = np.r_[np.ones(len(k), bool), np.zeros(len(k), bool)]
        return _fit(st, ex, np.r_[pid[use], pid[use]], np.r_[rlo[use], clo[use]], np.r_[rhi[use], chi[use]], ev, D,
                    adjust, estimator)
    persons = np.unique(pid)
    I = D.imm[persons]
    lo = np.where(I < BIG, np.maximum(Y2022, I), Y2022).astype(np.int64)
    hi = obs_end_after(D, persons, lo, censor)
    has = count_in(ev, persons, lo, hi) > 0
    persons, lo, hi = persons[has], lo[has], hi[has]
    allst = new_users(D, substance, **dict(nu))
    sp, sd = allst["pid"].to_numpy(), allst["day"].to_numpy()
    m = np.isin(sp, persons)
    sp, sd = sp[m], sd[m]
    q = np.searchsorted(persons, sp)
    r_lo, r_hi, x_lo = sd + risk[0], sd + risk[1], sd - pre
    first = np.r_[True, q[1:] != q[:-1]]
    prev_end = np.where(first, lo[q], np.r_[0, r_hi[:-1]] + 1)
    last = np.r_[q[1:] != q[:-1], True]
    seg_q = np.r_[q, q, q[last]]
    seg_ex = np.r_[np.zeros(len(q), bool), np.ones(len(q), bool), np.zeros(last.sum(), bool)]
    seg_lo = np.r_[np.maximum(prev_end, lo[q]), np.maximum(r_lo, lo[q]), np.maximum(r_hi[last] + 1, lo[q[last]])]
    seg_hi = np.r_[np.minimum(x_lo - 1, hi[q]), np.minimum(r_hi, hi[q]), hi[q[last]]]
    return _fit(seg_q, seg_ex, persons[seg_q], seg_lo, seg_hi, ev, D, adjust, estimator)


RISKS = [(1, 30), (0, 30), (1, 28)]
CONTROLS = [(61, 180), (31, 180), (61, 365), (31, None), "full"]
POPULATIONS = [("all starts", None), ("starts from 2022", Y2022), ("starts from 2023", Y2023)]


def adjustments(control, estimator):
    """The adjustment sets of a cell: none and five-year age bands everywhere; age bands and calendar half-years
    where the observation runs for years (the full-observation design, conditional Poisson)."""
    out = [False, "age"]
    if control == "full" and estimator == "cpois":
        out.append("age+half")
    return out


def sccs_grid(D, substance, censor=True, merge=True, populations=POPULATIONS):
    """Every self-controlled cell: population x risk window x control x adjustment x estimator."""
    ev = events(D, EVENT[substance], merge=merge)
    out = {}
    for plab, fd in populations:
        for risk in RISKS:
            for control in CONTROLS:
                for est in ("cpois", "mh"):
                    for adjust in adjustments(control, est):
                        out[(plab, risk, control, adjust, est)] = sccs(D, substance, risk, control, adjust, est, fd,
                                                                      censor, ev)
    return out


# ------------------------------------------------------------------ the between-person comparisons

def charlson_first(D):
    """The first day each person carries each Charlson group on a hospital contact."""
    if "charlson" in D.cache:
        return D.cache["charlson"]
    code = D.dx["code"]
    rows = D.dx["row"].to_numpy()
    cday = D.c["start"].to_numpy() // MIN_DAY
    cpid = D.c["pid"].to_numpy()
    first = {}
    for g, prefixes in CHARLSON.items():
        m = code.str.startswith(tuple(prefixes)).to_numpy()
        f = np.full(D.n, BIG, np.int64)
        np.minimum.at(f, cpid[rows[m]], cday[rows[m]])
        first[g] = f
    D.cache["charlson"] = first
    return first


def design_matrix(D, pid, s, kind, with_prior, merge=True):
    first = charlson_first(D)
    age = year_of(s) - D.birth_year[pid]
    cols = [((age >= lo) & (age <= hi)).astype(float) for lo, hi in ((50, 59), (60, 69), (70, 79), (80, 200))]
    cols.append(D.female[pid].astype(float))
    for g in CHARLSON:
        x = (first[g][pid] < s).astype(float)
        if 15 <= x.sum() <= len(x) - 15:
            cols.append(x)
    if with_prior:
        ev = events(D, kind, merge=merge)
        cols.append((count_in(ev, pid, s - 365, s - 1) > 0).astype(float))
    return np.column_stack(cols)


def poisson_fit(X, y, t):
    """Poisson regression with a log person-time offset; coefficients, intercept first."""
    Xi = np.column_stack([np.ones(len(y)), X])
    off = np.log(t)
    beta = np.zeros(Xi.shape[1])
    beta[0] = np.log(max(y.sum(), 0.5) / t.sum())
    for _ in range(60):
        eta = Xi @ beta + off
        mu = np.exp(eta)
        z = eta - off + (y - mu) / mu
        WX = Xi * mu[:, None]
        nb = np.linalg.solve(Xi.T @ WX + np.eye(len(beta)) * 1e-9, WX.T @ z)
        done = np.abs(nb - beta).max() < 1e-10
        beta = nb
        if done:
            break
    return beta


def logistic_fit(X, y):
    Xi = np.column_stack([np.ones(len(y)), X])
    beta = np.zeros(Xi.shape[1])
    for _ in range(60):
        p = 1 / (1 + np.exp(-(Xi @ beta)))
        step = np.linalg.solve(Xi.T @ (Xi * (p * (1 - p))[:, None]) + np.eye(len(beta)) * 1e-9, Xi.T @ (y - p))
        beta += step
        if np.abs(step).max() < 1e-10:
            break
    return 1 / (1 + np.exp(-(Xi @ beta)))


def first_month(D, ev, pid, s, censor=True):
    e = obs_end_after(D, pid, s, censor)
    n, t, _, _ = window(ev, pid, s, e, 1, 30)
    return n.astype(float), t.astype(float)


def matched_cohort(D, substance, adjust="none", first_day=Y2022, censor=True, merge=True):
    """New users against the matched non-users drawn at their index day, the month after the index day."""
    m = D.matched[D.matched["substance"] == substance]
    st = new_users(D, substance)
    starts = set(zip(st["pid"].tolist(), st["day"].tolist()))
    u = m[m["user"]]
    keep = np.array([(p, d) in starts for p, d in zip(u["pid"].tolist(), u["day"].tolist())]) & \
        (u["day"] >= first_day).to_numpy() & (u["day"] <= LAST_START).to_numpy()
    mm = m[m["set"].isin(set(u["set"][keep]))]
    pid, s, expo = mm["pid"].to_numpy(), mm["day"].to_numpy(), mm["user"].to_numpy().astype(float)
    ev = events(D, EVENT[substance], merge=merge)
    y, t = first_month(D, ev, pid, s, censor)
    ok = t > 0
    if adjust == "none":
        return float((y[ok & (expo == 1)].sum() / t[ok & (expo == 1)].sum()) /
                     (y[ok & (expo == 0)].sum() / t[ok & (expo == 0)].sum()))
    X = design_matrix(D, pid[ok], s[ok], EVENT[substance], adjust == "charlson_prior", merge)
    return float(np.exp(poisson_fit(np.column_stack([expo[ok], X]), y[ok], t[ok])[1]))


def rate_table(D):
    if "rates" in D.cache:
        return D.cache["rates"]
    col = {"fall": "indlaeggelser_fald", "aki": "indlaeggelser_akut_nyreskade",
           "pancreatitis": "indlaeggelser_akut_pancreatitis"}
    p = D.pop
    lo = p["aldersgruppe"].astype(str).str.extract(r"^(\d+)")[0].astype(int).to_numpy()
    out = {e: dict(year=p["aar"].to_numpy(), lo=lo, sex=p["koen"].to_numpy(),
                   rate=(p[c] / p["folketal_1_januar"]).to_numpy()) for e, c in col.items()}
    D.cache["rates"] = out
    return out


def observed_expected(D, substance, first_day=Y2022, censor=True, merge=True):
    """Admissions in the month after the start against those expected at the national rate for each new user's age
    group, sex and calendar year (2025 rates for 2026 starts)."""
    st = new_users(D, substance)
    st = st[(st["day"] >= first_day) & (st["day"] <= LAST_START)]
    pid, s = st["pid"].to_numpy(), st["day"].to_numpy()
    ev = events(D, EVENT[substance], merge=merge)
    y, t = first_month(D, ev, pid, s, censor)
    R = rate_table(D)[EVENT[substance]]
    yr = np.minimum(year_of(s), 2025)
    age = year_of(s) - D.birth_year[pid]
    bands = np.unique(R["lo"])
    band = bands[np.maximum(0, np.searchsorted(bands, age, side="right") - 1)]
    sex = np.where(D.female[pid], "K", "M")
    lut = {(int(a), int(b), c): r for a, b, c, r in zip(R["year"], R["lo"], R["sex"], R["rate"])}
    rate = np.array([lut[(int(a), int(b), c)] for a, b, c in zip(yr, band, sex)])
    return float(y.sum() / (rate * t / 365.25).sum())


def active_comparator(D, substance, adjust="none", first_day=Y2022, censor=True, merge=True):
    """New users against new users of the established medicine, the month after each start."""
    a = new_users(D, substance)
    b = new_users(D, ACTIVE[substance])
    a = a[(a["day"] >= first_day) & (a["day"] <= LAST_START)]
    b = b[(b["day"] >= first_day) & (b["day"] <= LAST_START)]
    pid = np.r_[a["pid"].to_numpy(), b["pid"].to_numpy()]
    s = np.r_[a["day"].to_numpy(), b["day"].to_numpy()]
    expo = np.r_[np.ones(len(a)), np.zeros(len(b))]
    ev = events(D, EVENT[substance], merge=merge)
    y, t = first_month(D, ev, pid, s, censor)
    ok = t > 0
    pid, s, expo, y, t = pid[ok], s[ok], expo[ok], y[ok], t[ok]
    if adjust == "none":
        return float((y[expo == 1].sum() / t[expo == 1].sum()) / (y[expo == 0].sum() / t[expo == 0].sum()))
    X = design_matrix(D, pid, s, EVENT[substance], True, merge)
    if adjust == "adjusted":
        return float(np.exp(poisson_fit(np.column_stack([expo, X]), y, t)[1]))
    ps = logistic_fit(X, expo)
    if adjust == "ps_att":
        w = np.where(expo == 1, 1.0, ps / (1 - ps))
    else:
        pbar = expo.mean()
        w = np.where(expo == 1, pbar / ps, (1 - pbar) / (1 - ps))
    return float(((w * y)[expo == 1].sum() / (w * t)[expo == 1].sum()) /
                 ((w * y)[expo == 0].sum() / (w * t)[expo == 0].sum()))


NAIVE = [("R1 matched non-users, crude", lambda D, s, **k: matched_cohort(D, s, "none", **k)),
         ("R1 matched non-users, Charlson groups", lambda D, s, **k: matched_cohort(D, s, "charlson", **k)),
         ("R1 matched non-users, Charlson groups and prior admission",
          lambda D, s, **k: matched_cohort(D, s, "charlson_prior", **k)),
         ("R1b observed against expected", lambda D, s, **k: observed_expected(D, s, **k)),
         ("R2 active comparator, crude", lambda D, s, **k: active_comparator(D, s, "none", **k)),
         ("R2 active comparator, adjusted", lambda D, s, **k: active_comparator(D, s, "adjusted", **k)),
         ("R2 active comparator, propensity weighted (IPTW)", lambda D, s, **k: active_comparator(D, s, "ps", **k)),
         ("R2 active comparator, propensity weighted (ATT)",
          lambda D, s, **k: active_comparator(D, s, "ps_att", **k))]


def naive_grid(D, variants=True):
    out = {}
    pops = (("from 2022", Y2022), ("from 2023", Y2023)) if variants else (("from 2022", Y2022),)
    flags = ((True, True), (False, True), (True, False)) if variants else ((True, True),)
    for name, f in NAIVE:
        for plab, fd in pops:
            for censor, merge in flags:
                out[(name, plab, censor, merge)] = {s: f(D, s, first_day=fd, censor=censor, merge=merge) for s in NEW}
    return out


def pre_start_rate(D, substance, who):
    """Admissions for the event per person-year in the 365 days before the start: the new users, their matched
    non-users at the index day, or new users of the established medicine; starts 2022 to May 2026, resident for the
    whole year before."""
    ev = events(D, EVENT[substance])
    if who == "users":
        st = new_users(D, substance)
        pid, s = st["pid"].to_numpy(), st["day"].to_numpy()
    elif who == "active":
        st = new_users(D, ACTIVE[substance])
        pid, s = st["pid"].to_numpy(), st["day"].to_numpy()
    else:
        m = D.matched[(D.matched["substance"] == substance) & ~D.matched["user"]]
        pid, s = m["pid"].to_numpy(), m["day"].to_numpy()
    keep = (s >= Y2022) & (s <= LAST_START)
    pid, s = pid[keep], s[keep]
    ok = resident_through(D, pid, s - 365, s - 1)
    n = count_in(ev, pid[ok], s[ok] - 365, s[ok] - 1)
    return float(n.sum() / (ok.sum() * 365 / 365.25))


# ------------------------------------------------------------------ the call and the asks

def nsaid_free(D, substance, first_day=None, censor=True):
    """A mask over the episodes: no NSAID (M01A) dispensed in days 0 to 30 after the start."""
    pid, s, e = episodes(D, substance, first_day, censor)
    rx = D.rx[D.rx["atc"].str.startswith("M01A") & (D.rx["apk"] > 0)]
    key = np.sort(rx["pid"].to_numpy() * 10 ** 6 + rx["day"].to_numpy())
    a = np.searchsorted(key, pid * 10 ** 6 + s, side="left")
    b = np.searchsorted(key, pid * 10 ** 6 + s + 30, side="right")
    return (b - a) == 0


def reports(D):
    """Rung 0: cases received in the quarter per signal, latest version, the medicine suspected."""
    df = D.screen.sort_values(["Case number", "Version"]).groupby("Case number").tail(1)
    out = {}
    for s in NEW:
        sus = df["Suspect"].fillna("").str.lower().str.contains(s)
        ev = df["Reactions (MedDRA PT)"].fillna("").apply(lambda x: PT[s] in [y.strip() for y in x.split(";")])
        out[s] = int((sus & ev).sum())
    return out


def new_users_by_year(D, **kw):
    out = {}
    for s in NEW:
        st = new_users(D, s, **kw)
        yr = year_of(st["day"].to_numpy())
        for y in (2022, 2023, 2024, 2025):
            out[(s, y)] = int(len(np.unique(st["pid"].to_numpy()[yr == y])))
    return out


def asks(D, substance, ratio, censor=True, merge=True, secondary=False, outpatient=False, **nu):
    """Admissions in days 1 to 30 after a 2025 start, and how many the medicine caused."""
    st = new_users(D, substance, **nu)
    st = st[(st["day"] >= Y2025) & (st["day"] < Y2026)]
    pid, s = st["pid"].to_numpy(), st["day"].to_numpy()
    ev = events(D, EVENT[substance], merge=merge, secondary=secondary, outpatient=outpatient)
    n, _, _, _ = window(ev, pid, s, obs_end_after(D, pid, s, censor), 1, 30)
    k = int(n.sum())
    exact = k * (ratio - 1) / ratio
    return k, exact, int(np.floor(exact + 0.5))


def lead(score):
    order = sorted(score, key=lambda k: -score[k])
    return order[0], order[1], score[order[0]] / score[order[1]]


def solve(target):
    D = load(target)
    g = {"reports": reports(D)}
    g["sccs"] = {s: sccs(D, s) for s in NEW}
    supported = [s for s in NEW if g["sccs"][s][1] > 1.0]
    g["answer"] = max(supported, key=lambda s: g["sccs"][s][0]) if supported else None
    a = g["answer"]
    g["ratio"], g["lower"], g["upper"] = g["sccs"][a]
    g["events_2025"], g["caused_exact"], g["caused"] = asks(D, a, g["ratio"])
    g["new_users"] = new_users_by_year(D)
    g["pre"] = {"tasorexant users": pre_start_rate(D, "tasorexant", "users"),
                "tasorexant matched": pre_start_rate(D, "tasorexant", "matched"),
                "zopiclone users": pre_start_rate(D, "tasorexant", "active"),
                "corinurad users": pre_start_rate(D, "corinurad", "users"),
                "allopurinol users": pre_start_rate(D, "corinurad", "active")}
    nf = nsaid_free(D, "corinurad")
    g["nsaid_free"] = sccs(D, "corinurad", subset=nf)
    g["nsaid_free_share"] = float(nf.mean())
    return D, g
