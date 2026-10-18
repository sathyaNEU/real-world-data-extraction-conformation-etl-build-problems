"""task243 estimator: reads only the shipped pack and computes every owed figure. The call: each LGU's completeness
of adult death registration between the 2015 and 2020 census reference dates, from Hill's general growth balance with
the net movement above each age from the 2020 census's residence five years earlier (Hill and Queiroz), and the 80 per
cent alert; the rungs (the balance taken as closed over any range, synthetic extinct generations, Brass's one-census
balance, the movement within the province only); the accepted interval for each LGU over the readings the method
admits. The asks: each LGU's share of 2022 live births registered within 30 days, and its share of 2022 resident
deaths certified by a physician."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import ggb as G

CODES = ["KLW-%02d" % i for i in range(1, 13)]
NAMES = ["KALINAWAN CITY", "CITY OF SANTA CRUZ", "SAN ISIDRO", "ESPERANZA", "MAGSAYSAY", "MABINI", "LIBERTAD",
         "SAN LUIS", "DEL CARMEN", "QUEZON", "RIZAL", "SAN MIGUEL"]
SHOW = ["Kalinawan City", "City of Santa Cruz", "San Isidro", "Esperanza", "Magsaysay", "Mabini", "Libertad",
        "San Luis", "Del Carmen", "Quezon", "Rizal", "San Miguel"]
C1, C2 = dt.date(2015, 8, 1), dt.date(2020, 5, 1)
EXTRACT = dt.date(2023, 3, 31)
T = (C2 - C1).days / 365.25
ALERT = 0.80
NG = len(G.AGES)
GOLD_RANGE = (15, 65)
RANGES = [(lo, hi) for lo in (10, 15, 20, 25, 30) for hi in (55, 60, 65, 70, 75)]


def norm_place(s):
    """an LGU code from the residence as written (spelling, abbreviations, the city's two name orders)"""
    if not isinstance(s, str):
        return None
    t = " ".join(s.upper().replace(".", " ").split())
    t = t.replace("STA ", "SANTA ").replace("SN ", "SAN ")
    if t.startswith("CITY OF "):
        t = t[8:]
    if t.endswith(" CITY"):
        t = t[:-5]
    base = {"KALINAWAN": "KLW-01", "SANTA CRUZ": "KLW-02", "SAN ISIDRO": "KLW-03", "ESPERANZA": "KLW-04",
            "MAGSAYSAY": "KLW-05", "MABINI": "KLW-06", "LIBERTAD": "KLW-07", "SAN LUIS": "KLW-08",
            "DEL CARMEN": "KLW-09", "QUEZON": "KLW-10", "RIZAL": "KLW-11", "SAN MIGUEL": "KLW-12"}
    return base.get(t)


def load(target, F):
    p = lambda k: os.path.join(target, F[k])
    D = {}
    D["deaths"] = pd.read_csv(p("deaths"), dtype=str, keep_default_na=False)
    D["births"] = pd.read_csv(p("births"), dtype=str, keep_default_na=False)
    D["restab"] = pd.read_csv(p("restab"), dtype={"PERSONS": int}, keep_default_na=False)
    D["roster"] = pd.read_excel(p("roster"), dtype=str, header=3).fillna("")
    D["c2015"] = census_sheet(p("cen2015"))
    D["c2020"] = census_sheet(p("cen2020"))
    return D


def census_sheet(path):
    """each LGU's household population by five-year age group, from the published table (both sexes); the LGU's
    'All Ages' row is skipped"""
    raw = pd.read_excel(path, header=None, dtype=object)
    out, cur = {}, None
    for _, r in raw.iterrows():
        a = r[0]
        if isinstance(a, str) and norm_place(a) and (not isinstance(r[1], (int, float)) or pd.isna(r[1])):
            cur = norm_place(a)
            out[cur] = np.zeros(NG)
            continue
        if cur is None or not isinstance(a, str):
            continue
        lab = a.strip()
        if lab.lower().startswith("all ages"):
            continue
        if lab[0].isdigit():
            lo = int(lab.split()[0])
            out[cur][min(lo // 5, NG - 1)] = float(r[1])
    return out


# ------------------------------------------------------------------ the deaths the balance reads
def resident_deaths(D, window=(C1, C2), adults_only=False, dedupe=True):
    """registered deaths of the province's usual residents: certificates of death (fetal deaths out), each LGU from the
    residence as written, rows sent twice counted once, a death registered at two offices counted once (its first
    registration), dated in the window"""
    d = D["deaths"].copy()
    d = d[d["CERT_TYPE"] == "DEATH"]
    d = d.drop_duplicates()
    d = d[d["RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN"]
    d["lgu"] = d["RES_CITY_MUN"].map(norm_place)
    d = d[d["lgu"].notna()]
    if dedupe:
        d = d.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"], kind="mergesort")
        d = d.drop_duplicates(["LAST_NAME", "FIRST_NAME", "MIDDLE_NAME", "SEX", "DATE_OF_DEATH", "DATE_OF_BIRTH"])
    a, b = window
    d = d[(d["DATE_OF_DEATH"] >= a.isoformat()) & (d["DATE_OF_DEATH"] < b.isoformat())]
    return d


def age_years(d):
    v = pd.to_numeric(d["AGE"], errors="coerce")
    u = d["AGE_UNIT"]
    return np.where(u == "YEARS", v, np.where(u.isin(["MONTHS", "DAYS", "HOURS"]), 0.0, np.nan))


def deaths_by_group(D, **kw):
    """registered deaths in the window by LGU and five-year age group at death, unstated ages spread over the LGU's
    stated ages in proportion"""
    d = resident_deaths(D, **kw)
    age = age_years(d)
    out = {}
    for c in CODES:
        m = (d["lgu"] == c).values
        a = age[m]
        known = a[~np.isnan(a)]
        g = np.bincount(np.minimum((known // 5).astype(int), NG - 1), minlength=NG).astype(float)
        unk = np.isnan(a).sum()
        if g.sum() > 0:
            g = g * (1 + unk / g.sum())
        out[c] = g
    return out


def net_movers(D, convention="shift", within_province_only=False, scale=True, not_stated="spread"):
    """each LGU's net movement by five-year age group in the five years before the 2020 census: persons in the LGU in
    2020 who lived elsewhere on 1 May 2015, less persons anywhere in the country in 2020 who lived in the LGU then.
    convention: 'census' keeps each mover at the age group of the census; 'shift' places the movers of each group half
    a group younger (they moved, on average, two and a half years before the census). scale: the five years carried to
    the intercensal interval."""
    t = D["restab"]
    gi = {g: i for i, g in enumerate(t["AGE_GROUP"].drop_duplicates().tolist())}
    order = ["5 - 9", "10 - 14", "15 - 19", "20 - 24", "25 - 29", "30 - 34", "35 - 39", "40 - 44", "45 - 49", "50 - 54",
             "55 - 59", "60 - 64", "65 - 69", "70 - 74", "75 - 79", "80 and over"]
    idx = {g: i + 1 for i, g in enumerate(order)}
    nm = {c: np.zeros(NG) for c in CODES}
    stated = {}
    for c, name in zip(CODES, NAMES):
        here = t[t["CITY_MUN_2020"] == name]
        inn = here[~here["RESIDENCE_1MAY2015"].isin(["SAME CITY/MUNICIPALITY", "NOT STATED"])]
        if within_province_only:
            inn = inn[inn["RESIDENCE_1MAY2015"].isin(NAMES)]
        v = np.zeros(NG)
        for g, n in zip(inn["AGE_GROUP"], inn["PERSONS"]):
            v[idx[g]] += n
        if not_stated == "spread":
            ns = here[here["RESIDENCE_1MAY2015"] == "NOT STATED"]
            tot = here[here["RESIDENCE_1MAY2015"] != "NOT STATED"]
            for g in order:
                n_ns = ns.loc[ns["AGE_GROUP"] == g, "PERSONS"].sum()
                n_all = tot.loc[tot["AGE_GROUP"] == g, "PERSONS"].sum()
                n_mv = inn.loc[inn["AGE_GROUP"] == g, "PERSONS"].sum()
                if n_all:
                    v[idx[g]] += n_ns * n_mv / n_all
        out = t[(t["RESIDENCE_1MAY2015"] == name) & (t["CITY_MUN_2020"] != name)]
        if within_province_only:
            out = out[out["CITY_MUN_2020"].isin(NAMES)]
        for g, n in zip(out["AGE_GROUP"], out["PERSONS"]):
            v[idx[g]] -= n
        nm[c] = v
    if convention == "shift":
        for c in CODES:
            v = nm[c]
            s = 0.5 * v
            s[:-1] += 0.5 * v[1:]
            s[-1] += 0.0
            s[-2] += 0.0
            # the open group keeps its own half and gains half of the 75 to 79 group's; nothing above it
            nm[c] = s
    if scale:
        for c in CODES:
            nm[c] = nm[c] * T / 5.0
    return nm


def census_arrays(D):
    return D["c2015"], D["c2020"]


def dg(D):
    if "_dg" not in D:
        D["_dg"] = deaths_by_group(D)
    return D["_dg"]


def completeness(D, c, nm=None, lo=GOLD_RANGE[0], hi=GOLD_RANGE[1], method="orthogonal", deaths=None,
                 nx_mean="geometric"):
    p1, p2 = census_arrays(D)
    dd = deaths if deaths is not None else dg(D)
    return G.completeness(p1[c], p2[c], dd[c], T, None if nm is None else nm[c], lo, hi, method, nx_mean)[0]


def call(D):
    """the golden: the balance carrying the net movement (movers placed at their age when they moved), over 15+ to 65+,
    orthogonal fit"""
    nm = net_movers(D, "shift")
    out = {}
    for c in CODES:
        v = completeness(D, c, nm)
        out[c] = dict(c=v, alert=v < ALERT)
    return out


def readings(D):
    """every reading the method admits: either placement of the movers' ages, the movement scaled to the interval or
    not, any lowest fitted age from 10+ to 30+ with any highest from 55+ to 75+, orthogonal or least-squares fit, the
    persons at each exact age from the geometric or the arithmetic mean of the two groups either side, and completeness
    relative to the two censuses' mean coverage or to either census's (the intercept's relative coverage carried to one
    census)"""
    p1, p2 = census_arrays(D)
    dd = dg(D)
    out = {c: [] for c in CODES}
    for conv in ("shift", "census"):
        for sc in (True, False):
            nm = net_movers(D, conv, scale=sc)
            for lo, hi in RANGES:
                for meth in ("orthogonal", "ols"):
                    for nxm in ("geometric", "arithmetic"):
                        for c in CODES:
                            v, icpt, _ = G.completeness(p1[c], p2[c], dd[c], T, nm[c], lo, hi, meth, nxm)
                            out[c] += [v, v * np.exp(-icpt * T / 2), v * np.exp(icpt * T / 2)]
    return out


def closed_readings(D):
    out = {c: [] for c in CODES}
    for lo, hi in RANGES:
        for meth in ("orthogonal", "ols"):
            for nxm in ("geometric", "arithmetic"):
                for c in CODES:
                    out[c].append(completeness(D, c, None, lo, hi, meth, nx_mean=nxm))
    return out


def rung(D, name):
    """the ladder's readings, each LGU's completeness"""
    if name == "closed":
        return {c: completeness(D, c, None) for c in CODES}
    if name == "closed_trimmed":
        return {c: completeness(D, c, None, 35, 75) for c in CODES}
    if name == "in_province":
        nm = net_movers(D, "shift", within_province_only=True)
        return {c: completeness(D, c, nm) for c in CODES}
    if name == "seg":
        p1, p2 = census_arrays(D)
        dd = dg(D)
        return {c: G.seg(p1[c], p2[c], dd[c], T, None, 15, 65) for c in CODES}
    if name == "brass":
        p1, p2 = census_arrays(D)
        dd = deaths_by_group(D, window=(dt.date(2019, 5, 1), C2))
        return {c: G.brass(p2[c], dd[c], 15, 65)[0] for c in CODES}
    raise KeyError(name)


# ------------------------------------------------------------------ ask A: births registered within 30 days
def births_2022(D, dedupe="child"):
    b = D["births"].copy()
    b = b.drop_duplicates()
    b = b[b["MOTHER_RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN"]
    b["lgu"] = b["MOTHER_RES_CITY_MUN"].map(norm_place)
    b = b[b["lgu"].notna()]
    b = b[(b["DATE_OF_BIRTH"] >= "2022-01-01") & (b["DATE_OF_BIRTH"] <= "2022-12-31")]
    b = b.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"], kind="mergesort")
    if dedupe == "child":
        b = b.drop_duplicates(["CHILD_FIRST_NAME", "CHILD_MIDDLE_NAME", "CHILD_LAST_NAME", "SEX", "DATE_OF_BIRTH",
                               "MOTHER_FIRST_NAME", "MOTHER_MAIDEN_LAST_NAME"])
    elif dedupe == "mother_day":
        b = b.drop_duplicates(["MOTHER_FIRST_NAME", "MOTHER_MAIDEN_LAST_NAME", "DATE_OF_BIRTH", "SEX"])
    days = (pd.to_datetime(b["DATE_REGISTERED"]) - pd.to_datetime(b["DATE_OF_BIRTH"])).dt.days
    b["timely"] = days <= 30
    return b


def ask_a(D, dedupe="child"):
    b = births_2022(D, dedupe)
    return {c: 100.0 * b.loc[b["lgu"] == c, "timely"].mean() for c in CODES}


# ------------------------------------------------------------------ ask B: deaths certified by a physician
def officers(D):
    """the health officers' terms: (LGU, name) to the spans in which the holder was a physician or a nurse in charge"""
    r = D["roster"]
    out = []
    for _, x in r.iterrows():
        c = norm_place(x["CITY_MUN"])
        a = x["FROM"][:10]
        b = x["TO"][:10] if x["TO"] else "2099-12-31"
        out.append((c, x["NAME"].strip().upper(), a, b, "physician" in x["POSITION"].lower()))
    return out


def deaths_2022(D, dedupe=True):
    return resident_deaths(D, window=(dt.date(2022, 1, 1), dt.date(2023, 1, 1)), dedupe=dedupe)


def ask_b(D, roster=True, dedupe=True):
    d = deaths_2022(D, dedupe)
    terms = officers(D)

    def phys(row):
        t = row["CERTIFIER_TITLE"].upper()
        if t in ("MD", "ATTENDING PHYSICIAN", "RESIDENT PHYSICIAN"):
            return True
        if t in ("MHO", "CHO"):
            if not roster:
                return True
            nm = row["CERTIFIED_BY"].strip().upper()
            for c, n, a, b, isphys in terms:
                if c == row["lgu"] and n == nm and a <= row["DATE_OF_DEATH"] <= b:
                    return isphys
            return True
        return False
    d["phys"] = d.apply(phys, axis=1)
    return {c: 100.0 * d.loc[d["lgu"] == c, "phys"].mean() for c in CODES}


# ------------------------------------------------------------------ everything the write-up and the goldens owe
def interval(D):
    """each LGU's accepted completeness in whole per cent: the readings' range rounded outward"""
    import math
    rd = readings(D)
    return {c: (math.floor(100 * min(rd[c])), math.ceil(100 * max(rd[c]))) for c in CODES}


def counts(D):
    d = D["deaths"]
    out = {"death_rows": len(d)}
    out["death_exact_repeats"] = len(d) - len(d.drop_duplicates())
    u = d.drop_duplicates()
    out["fetal"] = int((u["CERT_TYPE"] == "FETAL DEATH").sum())
    dd = u[u["CERT_TYPE"] == "DEATH"]
    res = dd["RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN"
    out["nonresident_deaths"] = int((~res).sum())
    r = dd[res].copy()
    r["lgu"] = r["RES_CITY_MUN"].map(norm_place)
    out["unmapped"] = int(r["lgu"].isna().sum())
    win = r[(r["DATE_OF_DEATH"] >= C1.isoformat()) & (r["DATE_OF_DEATH"] < C2.isoformat())]
    once = win.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"], kind="mergesort").drop_duplicates(
        ["LAST_NAME", "FIRST_NAME", "MIDDLE_NAME", "SEX", "DATE_OF_DEATH", "DATE_OF_BIRTH"])
    out["window_certificates"] = len(win)
    out["window_double"] = len(win) - len(once)
    out["window_deaths"] = len(once)
    age = age_years(once)
    out["window_unstated_age"] = int(np.isnan(age).sum())
    out["window_adult_stated"] = int((age >= 15).sum())
    adults = deaths_by_group(D)
    out["adult_deaths"] = {c: float(adults[c][3:].sum()) for c in CODES}
    p1, p2 = census_arrays(D)
    out["pop2015"] = {c: int(p1[c].sum()) for c in CODES}
    out["pop2020"] = {c: int(p2[c].sum()) for c in CODES}
    t = D["restab"]
    out["restab_rows"] = len(t)
    nm = net_movers(D, "census", scale=False)
    out["net_movers_50plus"] = {c: int(round(nm[c][10:].sum())) for c in CODES}
    out["net_movers_all"] = {c: int(round(nm[c].sum())) for c in CODES}
    # ask A
    b = D["births"]
    out["birth_rows"] = len(b)
    out["birth_exact_repeats"] = len(b) - len(b.drop_duplicates())
    bb = births_2022(D, "none")
    b1 = births_2022(D, "child")
    out["births_2022_certificates"] = len(bb)
    out["births_2022"] = len(b1)
    out["births_2022_double"] = len(bb) - len(b1)
    out["births_2022_twins"] = int((b1["TYPE_OF_BIRTH"] == "TWIN").sum())
    out["births_2022_timely"] = int(b1["timely"].sum())
    # ask B
    d2 = deaths_2022(D, dedupe=False)
    d1 = deaths_2022(D, dedupe=True)
    out["deaths_2022_certificates"] = len(d2)
    out["deaths_2022"] = len(d1)
    out["deaths_2022_double"] = len(d2) - len(d1)
    out["deaths_2022_office_titled"] = int(d1["CERTIFIER_TITLE"].isin(["MHO", "CHO"]).sum())
    return out


def solve(target, F):
    D = load(target, F)
    X = {"D": D}
    X["call"] = call(D)
    X["interval"] = interval(D)
    X["readings"] = readings(D)
    X["closed_readings"] = closed_readings(D)
    X["rungs"] = {k: rung(D, k) for k in ("closed", "closed_trimmed", "seg", "brass", "in_province")}
    X["ask_a"] = ask_a(D)
    X["ask_b"] = ask_b(D)
    X["ask_a_paths"] = {"per_certificate": ask_a(D, "none"), "mother_day": ask_a(D, "mother_day")}
    X["ask_b_paths"] = {"titles": ask_b(D, roster=False, dedupe=False), "titles_once": ask_b(D, roster=False),
                        "roster_every": ask_b(D, roster=True, dedupe=False)}
    X["counts"] = counts(D)
    return X
