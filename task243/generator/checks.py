"""task243 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF16), the rungs, the corridor of readings and the call under every death distribution method carrying the movement
(C1, C4), the Layer 1 slips, the ask devices and their stops, the separation of the call from the devices, the
documents' pins, the input gates and the realism sweep."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

import build as B
import estim as E
import ggb as G
import params as P
import sim

N = [0]
GOLD = ["KLW-02", "KLW-03", "KLW-07", "KLW-08", "KLW-09"]
EASY = ["KLW-02", "KLW-03", "KLW-04", "KLW-05", "KLW-06", "KLW-07", "KLW-08", "KLW-09"]
FARM = ["KLW-04", "KLW-05", "KLW-06"]
NG = len(G.AGES)


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def _docx_text(path):
    import docx
    d = docx.Document(path)
    return " ".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells])


def _xlsx_text(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    return " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row if c is not None)


def _text(path):
    if path.endswith(".pdf"):
        return _pdf_text(path)
    if path.endswith(".docx"):
        return _docx_text(path)
    if path.endswith(".xlsx"):
        return _xlsx_text(path)
    return open(path, encoding="utf-8").read()


def fl(v):
    return [c for c in E.CODES if v[c] < E.ALERT]


def grp(a):
    return np.minimum((np.asarray(a) // 5).astype(int), NG - 1)


def shift(v):
    s = 0.5 * v
    s[:-1] += 0.5 * v[1:]
    return s


# ------------------------------------------------------------------ the clean truth
def truth(W, R):
    """each LGU's household population by five-year group at both census dates as it was (everyone counted), its deaths
    in the interval by group at death and residence at death (all of them, and those registered by the extract, each
    once), and its net movement by group from every survivor's residence on 1 May 2015"""
    p = {}
    for k, cd in ((1, P.CENSUS1), (2, P.CENSUS2)):
        idx, lg, sx, ag = W.census[cd]
        p[k] = {c: np.bincount(grp(ag[lg == i]), minlength=NG).astype(float) for i, c in enumerate(P.CODES)}
    d0, d1 = sim.days(P.CENSUS1), sim.days(P.CENSUS2)
    alld = {c: np.zeros(NG) for c in P.CODES}
    for p_, dd, l_ in W.deaths:
        if d0 <= dd < d1 and l_ < 12:
            alld[P.CODES[l_]][grp((dd - W.birth[p_]) / 365.2425)] += 1
    df = R.deaths()
    x = df[(df["CERT_TYPE"] == "DEATH") & (df["_person"] >= 0) & (~df["_dup"].astype(bool))].drop_duplicates("_person")
    x = x[(x["DATE_OF_DEATH"] >= P.CENSUS1.isoformat()) & (x["DATE_OF_DEATH"] < P.CENSUS2.isoformat())]
    reg = {c: np.zeros(NG) for c in P.CODES}
    for p_, c, dod in zip(x["_person"], x["_l"], x["DATE_OF_DEATH"]):
        reg[c][grp((sim.days(dt.date.fromisoformat(dod)) - W.birth[p_]) / 365.2425)] += 1
    idx, lg, sx, ag = W.census[P.CENSUS2]
    r15 = W.res2015[idx]
    nm = {}
    for i, c in enumerate(P.CODES):
        inn = (lg == i) & (r15 != i) & (ag >= 5)
        out = (lg != i) & (r15 == i) & (ag >= 5)
        nm[c] = (np.bincount(grp(ag[inn]), minlength=NG) - np.bincount(grp(ag[out]), minlength=NG)).astype(float)
    t = (P.CENSUS2 - P.CENSUS1).days / 365.25
    return dict(p1=p[1], p2=p[2], all=alld, reg=reg, nm=nm, t=t)


# ------------------------------------------------------------------ the call from a deaths frame of its own
def groups(d, spread=True, age=None):
    a = E.age_years(d) if age is None else age
    out = {}
    for c in E.CODES:
        m = (d["lgu"] == c).values
        aa = a[m]
        known = aa[~np.isnan(aa)]
        g = np.bincount(grp(known), minlength=NG).astype(float)
        unk = np.isnan(aa).sum()
        if spread and g.sum() > 0:
            g = g * (1 + unk / g.sum())
        out[c] = g
    return out


def variant(D, exact=True, dedupe=True, place="residence", on="DATE_OF_DEATH", end=E.C2, fetal=False):
    d = D["deaths"].copy()
    if not fetal:
        d = d[d["CERT_TYPE"] == "DEATH"]
    if exact:
        d = d.drop_duplicates()
    if place == "residence":
        d = d[d["RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN"]
        d["lgu"] = d["RES_CITY_MUN"].map(E.norm_place)
    elif place == "office":
        d["lgu"] = d["LCRO_NAME"].str.replace("LCRO ", "", regex=False).map(E.norm_place)
    else:
        d["lgu"] = d["PLACE_OF_DEATH_CITY_MUN"].map(E.norm_place)
    d = d[d["lgu"].notna()]
    if dedupe:
        d = d.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"], kind="mergesort")
        d = d.drop_duplicates(["LAST_NAME", "FIRST_NAME", "MIDDLE_NAME", "SEX", "DATE_OF_DEATH", "DATE_OF_BIRTH"])
    return d[(d[on] >= E.C1.isoformat()) & (d[on] < end.isoformat())]


def call_from(D, dd, t=E.T):
    nm = E.net_movers(D, "shift")
    p1, p2 = E.census_arrays(D)
    return {c: G.completeness(p1[c], p2[c], dd[c], t, nm[c], 15, 65)[0] for c in E.CODES}


def other_methods(D):
    """the synthetic extinct generations method carrying the movement over the usual ranges, with either placement of
    the movers' ages, and the hybrid (the census of lower coverage raised by the balance's relative coverage first)"""
    p1, p2 = E.census_arrays(D)
    dd = E.dg(D)
    out = {c: [] for c in E.CODES}
    for conv in ("shift", "census"):
        nm = E.net_movers(D, conv)
        for c in E.CODES:
            for lo, hi in ((10, 65), (15, 60), (15, 65), (20, 65), (25, 70), (30, 70)):
                out[c].append(G.seg(p1[c], p2[c], dd[c], E.T, nm[c], lo, hi))
            icpt = G.completeness(p1[c], p2[c], dd[c], E.T, nm[c], 15, 65)[1]
            for lo, hi in ((15, 65), (20, 65), (25, 70)):
                out[c].append(G.seg(p1[c], p2[c] * np.exp(icpt * E.T), dd[c], E.T, nm[c], lo, hi))
    return out


def edge(v, k=0.02):
    return abs(abs(v * 10 - round(v * 10)) - 0.5) > k


def run(target, golden, o, X, A):
    W, R = o["W"], o["R"]
    D = X["D"]
    F = B.FILES
    g = X["call"]
    ok([c for c in E.CODES if g[c]["alert"]] == GOLD, "golden: the five offices below the alert")

    # ---------------------------------------------------------------- the truth behind the golden
    T = truth(W, R)
    tc = {c: T["reg"][c][3:].sum() / T["all"][c][3:].sum() for c in E.CODES}
    ok(fl(tc) == GOLD, "truth: the five register fewer than 80 per cent of their residents' adult deaths")
    ok(max(tc[c] for c in GOLD) < 0.66 and min(tc[c] for c in E.CODES if c not in GOLD) > 0.84,
       "truth margins: the five under 0.66, the rest over 0.84 (%.3f, %.3f)"
       % (max(tc[c] for c in GOLD), min(tc[c] for c in E.CODES if c not in GOLD)))
    ok(all(abs(g[c]["c"] - tc[c]) < 0.05 for c in E.CODES), "the golden completeness sits within 5 points of the truth "
       "for every office (max %.3f)" % max(abs(g[c]["c"] - tc[c]) for c in E.CODES))
    ok(all(abs(g[c]["c"] - tc[c]) < 0.035 for c in FARM), "the golden completeness of the three farming municipalities "
       "sits within 3.5 points of the truth")

    # ---------------------------------------------------------------- R1: the field's raw material ships, nothing derived
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols = pd.read_csv(os.path.join(target, f), nrows=1).columns
            ok(not any(re.search(r"complet|expected|estimat|migra|mover|net_|adjust|coverage|growth|balance", c, re.I)
                       for c in cols), "R1 %s carries no derived column (%s)" % (f, list(cols)))

    # ---------------------------------------------------------------- R2: the default path on the cut pack
    for r in ("closed", "closed_trimmed", "seg", "in_province"):
        ok(fl(X["rungs"][r]) == EASY, "R2 rung %s files the eight (%s)" % (r, fl(X["rungs"][r])))
    ok(fl(X["rungs"]["brass"]) != GOLD, "R2 Brass's one-census balance files another set (%s)" % fl(X["rungs"]["brass"]))
    cr = X["closed_readings"]
    ok(all(max(cr[c]) < 0.79 for c in FARM), "R2 the closed balance flags the three farming municipalities over every "
       "fitting range and fit (max %.3f)" % max(max(cr[c]) for c in FARM))
    ok(all(max(cr[c]) < 1.0 for c in E.CODES), "R2 no closed reading passes 100 per cent anywhere (max %.3f)"
       % max(max(cr[c]) for c in E.CODES))
    pts = {c: G.ggb_points(D["c2015"][c], D["c2020"][c], E.dg(D)[c], E.T) for c in FARM}
    for c in FARM:
        slope, icpt, res = G.fit(pts[c], 15, 65)
        ok(res < 0.0015, "R2 the closed balance for %s is a straight line (largest residual %.5f)" % (c, res))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    easy = {c: G.completeness(T["p1"][c], T["p2"][c], T["reg"][c], T["t"], None, 15, 65)[0] for c in E.CODES}
    ok(fl(easy) == EASY, "R3a the easy route on the clean truth (every resident counted, every registered death once, "
       "the balance taken as closed) files the eight (%s)" % fl(easy))
    ok(max(easy[c] for c in FARM) < 0.78, "R3a it puts the three farming municipalities under 0.78 (%.3f)"
       % max(easy[c] for c in FARM))
    dec = {c: G.completeness(T["p1"][c], T["p2"][c], T["reg"][c], T["t"], shift(T["nm"][c]) * T["t"] / 5, 15, 65)[0]
           for c in E.CODES}
    ok(fl(dec) == GOLD, "R3b the decisive step alone (the survivors' net movement from their residence on 1 May 2015 in "
       "the balance) gives the five on the clean truth (%s)" % fl(dec))
    ok(min(dec[c] for c in FARM) > 0.86, "R3b and puts the three farming municipalities over 0.86 (%.3f)"
       % min(dec[c] for c in FARM))

    # ---------------------------------------------------------------- R3c: no plant, no method filed
    for k in ("request", "tor", "cover", "readme", "dict"):
        txt = _text(os.path.join(target, F[k]))
        ok(not re.search(r"growth balance|death distribution|migra|net mov|movers|closed population|synthetic extinct|"
                         r"Brass|Bennett|Horiuchi|Hill|Preston|Coale|adjust", txt, re.I),
           "R3c %s names no method and no movement adjustment" % F[k])
    tor = _text(os.path.join(target, F["tor"]))
    ok("The deaths of the city's or municipality's usual residents aged 15 years and over that occurred from 1 August "
       "2015" in tor and "as a share of all deaths of those residents in that interval" in tor,
       "R3c the terms of reference file D1's estimand (population, outcome, window, comparison)")
    ok("D1 below 80 per cent. The office goes into the first round of CRIP 2024." in tor, "R3c the alert is filed")
    for k in F:
        if k.startswith("deliv_"):
            continue
        txt = _text(os.path.join(target, F[k]))
        ok(not re.search(r"completeness (?:of|is|was) \d|\d+ per cent complete", txt, re.I),
           "R3c %s states no completeness figure for any office" % F[k])

    # ---------------------------------------------------------------- the corridor of readings (C1) and the margins (C4)
    rd = X["readings"]
    ok(all(max(rd[c]) < E.ALERT for c in GOLD) and all(min(rd[c]) >= E.ALERT for c in E.CODES if c not in GOLD),
       "C1 every reading of the balance with the movement puts the same five below 80 per cent (%d readings an office)"
       % len(rd["KLW-01"]))
    ok(max(max(rd[c]) for c in GOLD) < 0.70 and min(min(rd[c]) for c in E.CODES if c not in GOLD) > 0.81,
       "C4 the readings keep 10 points under the alert and 1 over it (%.3f, %.3f)"
       % (max(max(rd[c]) for c in GOLD), min(min(rd[c]) for c in E.CODES if c not in GOLD)))
    g15 = {c: E.completeness(D, c, E.net_movers(D, "shift"), 15, 65) for c in E.CODES}
    ok(all(abs(g15[c] - g[c]["c"]) < 1e-12 for c in E.CODES), "C1 the golden reading is the 15+ to 65+ balance with the "
       "geometric means, the movers split with the next younger group, carried to the interval")
    om = other_methods(D)
    ok(all(max(om[c]) < E.ALERT for c in GOLD) and all(min(om[c]) >= E.ALERT for c in E.CODES if c not in GOLD),
       "C4 synthetic extinct generations and the hybrid, both carrying the movement, put the same five below 80 per cent")
    ok(max(max(om[c]) for c in GOLD) < 0.78 and min(min(om[c]) for c in E.CODES if c not in GOLD) > 0.84,
       "C4 and keep 2 points either side of it (%.3f, %.3f)"
       % (max(max(om[c]) for c in GOLD), min(min(om[c]) for c in E.CODES if c not in GOLD)))
    iv = X["interval"]
    ok(all(iv[c][0] <= round(100 * g[c]["c"]) <= iv[c][1] for c in E.CODES), "C1 each golden completeness inside its "
       "accepted interval")
    ok(all(not (iv[c][0] <= round(100 * X["rungs"]["closed"][c]) <= iv[c][1]) for c in FARM),
       "C1 the closed balance lands outside the accepted interval for the three farming municipalities")
    ok(max(iv[c][1] for c in GOLD) < 80 and min(iv[c][0] for c in E.CODES if c not in GOLD) > 80,
       "C1 no accepted interval reaches the alert")

    # ---------------------------------------------------------------- semantic fork rows
    base = call_from(D, groups(variant(D)))
    ok(all(abs(base[c] - g[c]["c"]) < 1e-9 for c in E.CODES), "SF0 the checks' own route reproduces the golden")
    for pl in ("office", "occurrence"):
        v = call_from(D, groups(variant(D, place=pl)))
        ok(fl(v) != GOLD and v["KLW-01"] > 1.5, "SF1 deaths placed by the %s: another set, Kalinawan City at %.2f" % (pl, v["KLW-01"]))
    ok("A death belongs to the city or municipality of the deceased's usual residence at death." in tor and
       "wherever in the country the event was registered" in tor, "SF1 ruled out by the terms of reference")
    ok(fl(call_from(D, groups(variant(D), spread=False))) == GOLD, "SF2 deaths with no age stated dropped: same call")
    d = variant(D)
    dob = pd.to_datetime(d["DATE_OF_BIRTH"], errors="coerce")
    dod = pd.to_datetime(d["DATE_OF_DEATH"])
    a2 = np.where(dob.notna(), ((dod - dob).dt.days / 365.2425).values, E.age_years(d))
    ok(fl(call_from(D, groups(d, age=a2))) == GOLD, "SF3 age at death from the date of birth where stated: same call")
    ok(fl(call_from(D, groups(variant(D, end=dt.date(2020, 5, 2))))) == GOLD, "SF4 deaths on 1 May 2020 included: same call")
    ok(fl(call_from(D, groups(variant(D, on="DATE_REGISTERED")))) == GOLD, "SF5 the window read on the registration date: "
       "same call")
    ok(D["deaths"]["DATE_REGISTERED"].max() <= "2023-03-31", "SF6 every row was registered by 31 March 2023 (converge)")
    ok(fl(call_from(D, groups(variant(D, dedupe=False)))) == GOLD, "SF7 a death registered at two offices counted twice: "
       "same call")
    ok(fl(call_from(D, groups(variant(D, exact=False)))) == GOLD, "SF8 rows sent twice counted twice: same call")
    ok(fl(call_from(D, groups(variant(D, fetal=True)))) == GOLD, "SF9 fetal deaths read as deaths of unstated age: same call")
    dd = D["deaths"]
    nr = dd[dd["RES_PROVINCE"].str.upper().str.strip() != "KALINAWAN"]
    ok(int(nr["RES_CITY_MUN"].map(E.norm_place).notna().sum()) == 0, "SF10 no other province's resident maps to an office "
       "(converge)")
    ok(X["counts"]["unmapped"] == 0, "SF11 every resident's residence as written maps to one city or municipality, Santa "
       "Cruz's records before its charter included (converge)")
    for t in (4.75, (E.C2 - E.C1).days / 365.2425):
        ok(fl(call_from(D, groups(variant(D)), t)) == GOLD, "SF12 the interval as %.4f years: same call" % t)
    ok(all(min(rd[c]) <= g[c]["c"] <= max(rd[c]) for c in E.CODES), "SF13 completeness relative to either census inside "
       "the readings: same call")
    ok(all(abs(v - E.ALERT) > 0.01 for c in E.CODES for v in rd[c]), "SF14 below 80 or at most 80: no reading within a "
       "point of the line (nearest %.3f)" % min((abs(v - E.ALERT), v) for c in E.CODES for v in rd[c])[1])
    ok(all(iv[c][0] < round(100 * g[c]["c"]) < iv[c][1] or iv[c][1] - iv[c][0] <= 4 for c in E.CODES),
       "SF15 whole per cent: each golden figure inside its interval")
    for k in ("cen2015", "cen2020"):
        ok("Household Population" in _text(os.path.join(target, F[k])), "SF16 %s is the household population" % F[k])
    ok("Persons in institutional households are not included." in _text(os.path.join(target, F["cover"])),
       "SF16 the tabulation of residence is on the same household basis (converge)")
    am = {c: E.completeness(D, c, E.net_movers(D, "shift"), nx_mean="arithmetic") for c in E.CODES}
    ok(fl(am) == GOLD and all(iv[c][0] <= round(100 * am[c]) <= iv[c][1] for c in E.CODES),
       "SF18 the persons reaching each age from the arithmetic mean of the two groups: same call, inside every interval")
    for lab, w0, w1 in (("the interval", "2015-08-01", "2020-05-01"), ("2022", "2022-01-01", "2023-01-01")):
        x = D["deaths"].drop_duplicates()
        x = x[(x["CERT_TYPE"] == "DEATH") & (x["RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN")]
        x = x[(x["DATE_OF_DEATH"] >= w0) & (x["DATE_OF_DEATH"] < w1)]
        key = ["LAST_NAME", "FIRST_NAME", "MIDDLE_NAME", "SEX", "DATE_OF_DEATH"]
        pairs = x[x.duplicated(key + ["DATE_OF_BIRTH"], keep=False)]
        ok(len(pairs) > 0 and (pairs["DATE_OF_BIRTH"] != "").all() and
           int(x.duplicated(key + ["DATE_OF_BIRTH"]).sum()) == int(x[x["DATE_OF_BIRTH"] != ""].duplicated(key + ["DATE_OF_BIRTH"]).sum()),
           "SF19 every death registered at two offices in %s carries its date of birth, so a blank date of birth matched "
           "or not gives the same deaths (converge)" % lab)
    bs = by_sex(D, target)
    ok(fl(bs) == GOLD and all(iv[c][0] <= round(100 * bs[c]) <= iv[c][1] for c in E.CODES),
       "SF17 the balance by sex, the two combined over their registered deaths: same call, inside every interval")

    # ---------------------------------------------------------------- Layer 1: loud when mishandled
    up = {n: c for c, n in zip(E.CODES, E.NAMES)}
    d0 = D["deaths"]
    d1 = d0[(d0["CERT_TYPE"] == "DEATH") & (d0["RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN")].drop_duplicates()
    ok(d1["RES_CITY_MUN"].map(lambda s: up.get(s)).isna().mean() > 0.10, "L1 residence spellings: over a tenth of "
       "residents' rows are not written as the census names them")
    ok(int((d0["CERT_TYPE"] == "FETAL DEATH").sum()) > 1000 and int(d0.duplicated().sum()) > 50, "L1 fetal deaths and rows "
       "sent twice are in the extract")
    ok(X["counts"]["window_double"] > 10 and X["counts"]["window_unstated_age"] > 100, "L1 double registrations and "
       "unstated ages in the interval")

    # ---------------------------------------------------------------- separation: the asks sit outside the call
    blank = D["deaths"].copy()
    for col in ("CERTIFIED_BY", "CERTIFIER_TITLE", "ATTENDANT", "PLACE_OF_DEATH", "PLACE_OF_DEATH_CITY_MUN",
                "CIVIL_STATUS", "LATE_REGISTRATION", "RES_BARANGAY"):
        blank[col] = ""
    Db = {k: v for k, v in D.items() if k != "_dg"}
    Db["deaths"] = blank
    Db["births"] = D["births"].iloc[:0]
    Db["roster"] = D["roster"].iloc[:0]
    v = E.call(Db)
    ok(all(abs(v[c]["c"] - g[c]["c"]) < 1e-12 for c in E.CODES), "separation: the call reads no certifier, attendant or "
       "place-of-death column, no birth and no roster row")
    w = E.resident_deaths(D)
    ok(int((w["DATE_OF_DEATH"] >= "2021-01-01").sum()) == 0, "separation: no 2022 death is in the call's population")
    ok(min(P.VACANT[c][0] for c in P.VACANT) > E.C2, "separation: every vacancy the certification ask rides on is after "
       "the interval")

    # ---------------------------------------------------------------- ask A: births registered within 30 days
    a = X["ask_a"]
    ok(all(edge(a[c]) for c in E.CODES), "ask A: no share within 0.002 of a rounding edge")
    stops = {"per certificate": E.ask_a(D, "none"), "mother and day": E.ask_a(D, "mother_day"),
             "registered in 2022": ask_a_registered(D), "by registering office": ask_a_office(D)}
    for k, s in stops.items():
        miss = sum(round(s[c], 1) != round(a[c], 1) for c in E.CODES)
        need = 9 if k == "mother and day" else 12
        ok(miss >= need, "ask A stop %s misses %d of 12 (need %d)" % (k, miss, need))
    b = D["births"].drop_duplicates()
    b = b[(b["DATE_OF_BIRTH"] >= "2022-01-01") & (b["DATE_OF_BIRTH"] <= "2022-12-31")]
    b = b[b["MOTHER_RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN"].copy()
    b["lgu"] = b["MOTHER_RES_CITY_MUN"].map(E.norm_place)
    key = ["CHILD_FIRST_NAME", "CHILD_MIDDLE_NAME", "CHILD_LAST_NAME", "SEX", "DATE_OF_BIRTH", "MOTHER_FIRST_NAME",
           "MOTHER_MAIDEN_LAST_NAME"]
    dbl = b[b.duplicated(key, keep=False)]
    ok(dbl["lgu"].nunique() >= 10 and len(dbl) > 500, "ask A: births registered twice under new registry numbers in "
       "%d offices' records" % dbl["lgu"].nunique())
    ok(not dbl.duplicated(["REGISTRY_NO", "LCRO_CODE"]).any(), "ask A: no double registration shares a registry number "
       "(no exact-duplicate sweep finds it)")
    tw = b[b["TYPE_OF_BIRTH"] == "TWIN"]
    ok(tw["lgu"].nunique() == 12, "ask A: twins in every office's births")

    # ---------------------------------------------------------------- ask B: deaths certified by a licensed physician
    cb = X["ask_b"]
    ok(all(edge(cb[c]) for c in E.CODES), "ask B: no share within 0.002 of a rounding edge")
    for k, s in X["ask_b_paths"].items():
        miss = sum(round(s[c], 1) != round(cb[c], 1) for c in E.CODES)
        ok(miss == 12, "ask B stop %s misses every office (%d of 12)" % (k, miss))
    d22 = E.deaths_2022(D)
    office = d22[d22["CERTIFIER_TITLE"].isin(["MHO", "CHO"])]
    terms = E.officers(D)
    phys_names = {(c, n) for c, n, a_, b_, isp in terms if isp}
    staff = office[[(l, n.strip().upper()) not in phys_names for l, n in zip(office["lgu"], office["CERTIFIED_BY"])]]
    ok(staff["lgu"].nunique() == 12, "ask B: certificates made in the health office's name and signed by a nurse or "
       "midwife in every office")
    found = [any(c == l and n == who.strip().upper() and a_ <= day <= b_ for c, n, a_, b_, isp in terms)
             for l, who, day in zip(office["lgu"], office["CERTIFIED_BY"], office["DATE_OF_DEATH"])]
    ok(all(found), "ask B: every certificate in the health office's name has its signer in the roster on the date of "
       "death (%d certificates; none left to assume)" % len(found))
    bb = D["births"]
    late = (pd.to_datetime(bb["DATE_REGISTERED"]) - pd.to_datetime(bb["DATE_OF_BIRTH"])).dt.days > 30
    gap = (pd.to_datetime(bb["DATE_REGISTERED"]) - pd.to_datetime(bb["DATE_OF_BIRTH"])).dt.days
    ok(((bb["LATE_REGISTRATION"] == "Y") == late).all() and int((gap == 30).sum()) == 0, "ask A: the extract's late flag "
       "is more than 30 days after the birth, as the dictionary says, and no birth was registered on the 30th day, so "
       "within 30 days and under 30 days converge")
    rost = D["roster"]
    ok(set(rost["POSITION"]) >= {"Nurse II", "Rural Health Midwife"} and
       int(rost["POSITION"].str.contains("officer-in-charge").sum()) == len(P.VACANT),
       "ask B: the roster carries each signer's post, %d nurses in charge" % len(P.VACANT))

    # ---------------------------------------------------------------- the pack's own registers (H9)
    readme = _text(os.path.join(target, F["readme"]))
    ok(all(f in readme for f in os.listdir(target) if f != F["readme"]), "the README names every other shipped file")
    dic = _text(os.path.join(target, F["dict"]))
    ok(all(F[k] in dic for k in F if F[k].endswith((".csv", ".xlsx")) and not k.startswith("deliv_")),
       "the dictionary names every data file")

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(target))
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv"))
    ok(big - 1 >= 25000, "input gates: a table of 25,000 rows or more (%d)" % (big - 1))
    for k in B.DISTRACTORS:
        ok(os.path.exists(os.path.join(target, F[k])), "distractor %s ships" % F[k])
    src = open(os.path.join(os.path.dirname(__file__), "estim.py")).read()
    ok(not any(F[k] in src or ('"%s"' % k) in src for k in B.DISTRACTORS), "no estimator reads a distractor")
    for f in files:
        p = os.path.join(target, f)
        txt = _text(p) if f.rsplit(".", 1)[1] in ("pdf", "docx", "xlsx") else open(p, encoding="utf-8").read()
        ok("—" not in txt and "–" not in txt, "no em or en dash in %s" % f)
        ok(not re.search(r"\b(leverage|robust|comprehensive|seamless|delve|furthermore)\b", txt, re.I),
           "no LLM tell in %s" % f)
    for f in os.listdir(golden):
        txt = _text(os.path.join(golden, f))
        ok("—" not in txt and "–" not in txt, "no em or en dash in golden %s" % f)
    return N[0]


def by_sex(D, target):
    """the balance with the movement for each sex from the census tables' male and female columns, the two combined as
    the registered deaths over the deaths each estimates"""
    def sheet(path, col):
        raw = pd.read_excel(path, header=None, dtype=object)
        out, cur = {}, None
        for _, r in raw.iterrows():
            a = r[0]
            if isinstance(a, str) and E.norm_place(a) and (not isinstance(r[1], (int, float)) or pd.isna(r[1])):
                cur = E.norm_place(a)
                out[cur] = np.zeros(NG)
            elif cur and isinstance(a, str) and a.strip()[:1].isdigit():
                out[cur][min(int(a.split()[0]) // 5, NG - 1)] = float(r[col])
        return out
    est, reg = {c: 0.0 for c in E.CODES}, {c: 0.0 for c in E.CODES}
    for sex, col in (("MALE", 2), ("FEMALE", 3)):
        p1 = sheet(os.path.join(target, B.FILES["cen2015"]), col)
        p2 = sheet(os.path.join(target, B.FILES["cen2020"]), col)
        d = E.resident_deaths(D)
        dd = groups(d[d["SEX"] == sex])
        nm = E.net_movers(dict(D, restab=D["restab"][D["restab"]["SEX"] == sex]), "shift")
        for c in E.CODES:
            v = G.completeness(p1[c], p2[c], dd[c], E.T, nm[c], 15, 65)[0]
            reg[c] += dd[c][3:].sum()
            est[c] += dd[c][3:].sum() / v
    return {c: reg[c] / est[c] for c in E.CODES}


def ask_a_registered(D):
    """the share among births registered in 2022 (the registration year in place of the year of birth)"""
    b = D["births"].drop_duplicates()
    b = b[b["MOTHER_RES_PROVINCE"].str.upper().str.strip() == "KALINAWAN"].copy()
    b["lgu"] = b["MOTHER_RES_CITY_MUN"].map(E.norm_place)
    b = b[b["lgu"].notna() & (b["DATE_REGISTERED"] >= "2022-01-01") & (b["DATE_REGISTERED"] <= "2022-12-31")]
    b = b.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"], kind="mergesort")
    b = b.drop_duplicates(["CHILD_FIRST_NAME", "CHILD_MIDDLE_NAME", "CHILD_LAST_NAME", "SEX", "DATE_OF_BIRTH",
                           "MOTHER_FIRST_NAME", "MOTHER_MAIDEN_LAST_NAME"])
    days = (pd.to_datetime(b["DATE_REGISTERED"]) - pd.to_datetime(b["DATE_OF_BIRTH"])).dt.days
    b["timely"] = days <= 30
    return {c: 100.0 * b.loc[b["lgu"] == c, "timely"].mean() for c in E.CODES}


def ask_a_office(D):
    """the share by the registering office in place of the mother's residence"""
    b = D["births"].drop_duplicates()
    b = b[(b["DATE_OF_BIRTH"] >= "2022-01-01") & (b["DATE_OF_BIRTH"] <= "2022-12-31")].copy()
    b["lgu"] = b["LCRO_NAME"].str.replace("LCRO ", "", regex=False).map(E.norm_place)
    b = b[b["lgu"].notna()]
    days = (pd.to_datetime(b["DATE_REGISTERED"]) - pd.to_datetime(b["DATE_OF_BIRTH"])).dt.days
    b["timely"] = days <= 30
    return {c: 100.0 * b.loc[b["lgu"] == c, "timely"].mean() for c in E.CODES}
