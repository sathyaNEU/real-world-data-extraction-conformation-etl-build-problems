"""Computes every rung, the golden and every ask from the files under target/ alone (no access to the world)."""
import csv
import datetime as dt
import io
import os
import re
from collections import defaultdict

import pandas as pd
from openpyxl import load_workbook

import pack as P

DIM = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
THRESHOLD = 30.0
CATS = ("alberghiero 1-3 stelle", "alberghiero 4-5 stelle", "extralberghiero")


def d_it(s):
    return dt.datetime.strptime(s.strip(), "%d/%m/%Y").date()


class Pack:
    pass


def load(root):
    p = Pack()
    s = pd.read_csv(os.path.join(root, P.F_SURVEY), sep=";", dtype=str, keep_default_na=False)
    for c in ("ANNO", "MESE", "ARRIVI", "PRESENZE", "PROGR_INVIO"):
        s[c] = s[c].astype(int)
    s["SUB"] = pd.to_datetime(s["DATA_INVIO"], format="%d/%m/%Y %H:%M")
    p.survey_all = s
    last = s.groupby(["CODICE_STRUTTURA", "ANNO", "MESE"])["PROGR_INVIO"].transform("max")
    p.survey = s[s["PROGR_INVIO"] == last].copy()
    wb = load_workbook(os.path.join(root, P.F_REGISTER), read_only=True)
    rows = list(wb["STRUTTURE"].iter_rows(values_only=True))
    reg = pd.DataFrame(rows[1:], columns=rows[0])
    reg["CIR"] = reg["CIR"].fillna("")
    p.reg = reg
    rows = list(wb["VARIAZIONI"].iter_rows(values_only=True))
    p.var = pd.DataFrame(rows[1:], columns=rows[0])
    p.xw = pd.read_csv(os.path.join(root, P.F_CROSSWALK), sep=";", dtype=str)
    pop = pd.read_csv(os.path.join(root, P.F_POP), sep=";", dtype={"Codice comune": str})
    p.pop26 = {r["Codice comune"]: int(r["Totale"]) for _, r in pop.iterrows() if r["Data"] == "01/01/2026"}
    p.names = {r["Codice comune"]: r["Comune"] for _, r in pop.iterrows()}
    p.decl = load_declarations(root, p)
    p.rates = pd.read_csv(os.path.join(root, P.F_RATES), sep=";", dtype=str)
    return p


def lar_rows_pdf(path):
    import pdfplumber
    out = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for t in page.extract_tables():
                for r in t:
                    if r and r[0] and r[0].strip().isdigit():
                        out.append(r)
    return out


def load_declarations(root, p):
    """One row per filing: comune ISTAT code, year, quarter, category, total, exempt, liable, filing date."""
    recs = []
    name2code = {v: k for k, v in p.names.items()}
    wb = load_workbook(os.path.join(root, P.F_CONC), read_only=True)
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        code = str(rows[0][3])
        for r in rows[3:]:
            if not r or r[0] is None:
                continue
            q = int(str(r[1])[0])
            recs.append(dict(code=code, y=int(r[0]), q=q, cat=r[2], total=int(r[3]), exempt=int(r[4]),
                             liable=int(r[5]), date=d_it(r[7])))
    plv = pd.read_csv(os.path.join(root, P.F_PLV), sep=";", dtype=str)
    for _, r in plv.iterrows():
        y, q = r["PERIODO"].split("-T")
        recs.append(dict(code=name2code["Porto Levarna"], y=int(y), q=int(q), cat=r["TIPOLOGIA"].lower(),
                         total=int(r["PRESENZE_TOTALI"]), exempt=int(r["PRESENZE_ESENTI"]),
                         liable=int(r["PRESENZE_IMPONIBILI"]), date=d_it(r["DATA_RICEZIONE"])))
    sem = pd.read_csv(os.path.join(root, P.F_SEM), dtype=str)
    for _, r in sem.iterrows():
        recs.append(dict(code=name2code["Sant'Elvira a Mare"], y=int(r["anno"]), q=int(r["trimestre"]),
                         cat=r["categoria"], total=int(r["notti_totali"]), exempt=int(r["notti_esenti"]),
                         liable=int(r["notti_imponibili"]), date=dt.date.fromisoformat(r["data_protocollo"])))
    hill = pd.read_csv(os.path.join(root, P.F_HILL), sep=";", dtype=str)
    qmap = {"gen-mar": 1, "apr-giu": 2, "lug-set": 3, "ott-dic": 4}
    for _, r in hill.iterrows():
        nm = r["Ente"].replace("Comune di ", "")
        per, yy = r["Periodo di riferimento"].split()
        recs.append(dict(code=name2code[nm], y=int(yy), q=qmap[per], cat=r["Tipologia"],
                         total=int(r["Presenze dichiarate"]), exempt=int(r["Presenze esenti"]),
                         liable=int(r["Presenze soggette"]), date=d_it(r["Data"])))
    for r in lar_rows_pdf(os.path.join(root, P.F_LAR)):
        num = lambda x: int(x.replace(".", ""))
        recs.append(dict(code=name2code["Lido di Arzena"], y=int(r[0]), q=int(r[1]), cat=r[2], total=num(r[3]),
                         exempt=num(r[4]), liable=num(r[5]), date=d_it(r[7])))
    d = pd.DataFrame(recs)
    d["cat"] = d["cat"].str.lower()
    return d


def latest_decl(p, mode="resolve"):
    """One row per comune, quarter and category. A later filing far smaller than the first adds the nights the first
    left out; a later filing of about the same size replaces it (the tax office's corrected declaration).
    mode='latest' keeps the last filing whatever it is, mode='sum' adds every filing."""
    d = p.decl.sort_values(["code", "y", "q", "cat", "date"])
    out = []
    for key, g in d.groupby(["code", "y", "q", "cat"], sort=True):
        rows = g.to_dict("records")
        if mode == "latest":
            out.append(rows[-1])
            continue
        if mode == "sum":
            r = dict(rows[0])
            for x in rows[1:]:
                for f in ("total", "exempt", "liable"):
                    r[f] += x[f]
            out.append(r)
            continue
        cur = dict(rows[0])
        for x in rows[1:]:
            if x["total"] < 0.5 * cur["total"]:
                for f in ("total", "exempt", "liable"):
                    cur[f] += x[f]
            else:
                cur = dict(x)
        out.append(cur)
    return pd.DataFrame(out)


def season_days(period, y, m):
    if period == "ANNUALE":
        return DIM[m]
    a, b = period.split("-")
    d1, m1 = int(a[:2]), int(a[3:5])
    d2, m2 = int(b[:2]), int(b[3:5])
    if m < m1 or m > m2:
        return 0
    first = d1 if m == m1 else 1
    last = d2 if m == m2 else DIM[m]
    return last - first + 1


def establishment_table(p):
    reg = p.reg.copy()
    reg["code"] = reg["COD_ISTAT_COMUNE"].astype(str)
    reg["start"] = reg["DATA_INIZIO_ATTIVITA"].map(d_it)
    reg["beds"] = reg["POSTI_LETTO"].astype(int)
    return reg


def survey_by_cin(p, y, m):
    s = p.survey[(p.survey["ANNO"] == y) & (p.survey["MESE"] == m)]
    if (y, m) >= (2026, 5):
        s = s.assign(CIN=s["CODICE_STRUTTURA"])
    else:
        xw = dict(zip(p.xw["CIR"], p.xw["CIN"]))
        s = s.assign(CIN=s["CODICE_STRUTTURA"].map(xw))
    g = s.groupby("CIN").agg(nights=("PRESENZE", "sum"), state=("STATO", "first")).reset_index()
    return g


def main_call(p):
    reg = establishment_table(p)
    out = {}
    aug = survey_by_cin(p, 2026, 8)
    jul = survey_by_cin(p, 2026, 7)
    sep = survey_by_cin(p, 2026, 9)
    a = reg.merge(aug, left_on="CIN", right_on="CIN", how="left")
    a["open_days"] = [season_days(per, 2026, 8) if st <= dt.date(2026, 8, 31) else 0
                      for per, st in zip(a["PERIODO_APERTURA"], a["start"])]
    a["cap"] = a["beds"] * a["open_days"]
    a["reported"] = a["nights"].notna()
    a["missing"] = (~a["reported"]) & (a["open_days"] > 0)
    a["nights"] = a["nights"].fillna(0)
    # stratum occupancies among the establishments that reported August
    rep = a[a["reported"] & (a["cap"] > 0)]
    occ_ct = (rep.groupby(["code", "TIPOLOGIA"])["nights"].sum() / rep.groupby(["code", "TIPOLOGIA"])["cap"].sum()).to_dict()
    occ_t = (rep.groupby("TIPOLOGIA")["nights"].sum() / rep.groupby("TIPOLOGIA")["cap"].sum()).to_dict()
    occ_c = (rep.groupby("code")["nights"].sum() / rep.groupby("code")["cap"].sum()).to_dict()
    # previous-month ratio: own July x the type's August/July among establishments that reported both
    jj = reg.merge(jul, on="CIN", how="left").rename(columns={"nights": "jul"})
    a = a.merge(jj[["CIN", "jul"]], on="CIN", how="left")
    both = a[a["reported"] & a["jul"].notna() & (a["jul"] > 0)]
    ratio_t = (both.groupby("TIPOLOGIA")["nights"].sum() / both.groupby("TIPOLOGIA")["jul"].sum()).to_dict()
    # carry-forward: own August 2025 return (via the crosswalk) x the type's growth among those with both
    a25 = survey_by_cin(p, 2025, 8).rename(columns={"nights": "a25"})
    a = a.merge(a25[["CIN", "a25"]], on="CIN", how="left")
    b2 = a[a["reported"] & a["a25"].notna() & (a["a25"] > 0)]
    grow_t = (b2.groupby("TIPOLOGIA")["nights"].sum() / b2.groupby("TIPOLOGIA")["a25"].sum()).to_dict()

    def fill(row, how):
        if not row["missing"]:
            return row["nights"]
        if how == "ct":
            o = occ_ct.get((row["code"], row["TIPOLOGIA"]), occ_t.get(row["TIPOLOGIA"], 0))
            return row["cap"] * o
        if how == "t":
            return row["cap"] * occ_t.get(row["TIPOLOGIA"], 0)
        if how == "c":
            return row["cap"] * occ_c.get(row["code"], 0)
        if how == "prev":
            if pd.notna(row["jul"]) and row["jul"] > 0:
                return row["jul"] * ratio_t.get(row["TIPOLOGIA"], 1)
            return fill(row, "ct")
        if how == "cf":
            if pd.notna(row["a25"]) and row["a25"] > 0:
                return row["a25"] * grow_t.get(row["TIPOLOGIA"], 1)
            return fill(row, "ct")
        if how == "zero":
            return 0.0
        raise ValueError(how)

    variants = {}
    for how in ("zero", "ct", "t", "c", "prev", "cf"):
        variants[how] = a.assign(v=a.apply(lambda r: fill(r, how), axis=1)).groupby("code")["v"].sum().to_dict()
    jm = reg.merge(jul, on="CIN", how="inner").groupby("code")["nights"].sum().to_dict()
    sm = reg.merge(sep, on="CIN", how="inner").groupby("code")["nights"].sum().to_dict()
    ld = latest_decl(p)
    dq3 = ld[(ld["y"] == 2026) & (ld["q"] == 3)].groupby("code")["total"].sum().to_dict()
    codes = sorted(p.pop26)
    res = {}
    for c in codes:
        r = dict(code=c, name=p.names[c], residents=p.pop26[c], declared_q3=dq3.get(c), jul=jm.get(c, 0),
                 sep=sm.get(c, 0), reported=variants["zero"].get(c, 0))
        for how in variants:
            r["R1_" + how] = variants[how].get(c, 0)
            if c in dq3:
                q3 = r["jul"] + variants[how].get(c, 0) + r["sep"]
                r["R2_" + how] = variants[how].get(c, 0) * dq3[c] / q3
            else:
                r["R2_" + how] = variants[how].get(c, 0)
        r["golden"] = (dq3[c] - r["jul"] - r["sep"]) if c in dq3 else variants["ct"].get(c, 0)
        # golden variant: the quarter's shortfall spread over the filled returns in proportion to their fill
        if c in dq3:
            filled = variants["ct"].get(c, 0) - variants["zero"].get(c, 0)
            r["golden_b"] = variants["ct"].get(c, 0) + (dq3[c] - (r["jul"] + variants["ct"].get(c, 0) + r["sep"])) * (1.0 if filled > 0 else 0)
        else:
            r["golden_b"] = r["golden"]
        r["missing_returns"] = int(a[(a["code"] == c) & a["missing"]].shape[0])
        r["establishments"] = int(a[(a["code"] == c) & (a["open_days"] > 0)].shape[0])
        res[c] = r
    return res


def designation(res, key):
    return sorted(c for c, r in res.items() if r[key] / r["residents"] >= THRESHOLD)


# ---------------------------------------------------------------------------------------------- the asks
def rate_for(p, code, cat, day):
    r = p.rates[(p.rates["COD_ISTAT"] == code) & (p.rates["CATEGORIA"] == cat)]
    for _, x in r.iterrows():
        a = d_it(x["IN_VIGORE_DAL"])
        b = d_it(x["IN_VIGORE_AL"]) if isinstance(x["IN_VIGORE_AL"], str) and x["IN_VIGORE_AL"] else dt.date(2099, 1, 1)
        if a <= day <= b:
            return float(x["EURO_PER_PERNOTTAMENTO"].replace(",", "."))
    return None


def ask_tax_2025(p, mode="resolve", merger=True):
    """The tourist tax the member comuni were due for each quarter of 2025 (liable nights x the rate in force)."""
    d = latest_decl(p, mode)
    if not merger:
        d = d[~d["code"].isin(["112006", "112007"])]
    d = d[d["y"] == 2025]
    out = {}
    for q in (1, 2, 3, 4):
        tot = 0.0
        for _, r in d[d["q"] == q].iterrows():
            rate = rate_for(p, r["code"], r["cat"], dt.date(2025, 3 * q - 1, 15))
            tot += r["liable"] * rate
        out[q] = tot
    return out


def ask_jan_apr(p, via="cir", dedupe=True):
    """Guest nights reported for January to April 2026 by member comune (2026 boundaries). An April return sent again
    under the CIN after the change of codes is the same return as the one under the CIR (one establishment, one month):
    the later submission is kept."""
    s = p.survey[(p.survey["ANNO"] == 2026) & (p.survey["MESE"] <= 4)].copy()
    xw = dict(zip(p.xw["CIR"], p.xw["CIN"]))
    cin2cir = {v: k for k, v in xw.items()}
    s["est"] = s["CODICE_STRUTTURA"].map(lambda c: c if "-" in c else cin2cir.get(c, c))
    if dedupe:
        lastsub = s.groupby(["est", "MESE"])["SUB"].transform("max")
        s = s[s["SUB"] == lastsub]
    merged_from = {"006": "112020", "007": "112020"}
    if via == "cir":
        code = s["est"].map(lambda x: merged_from.get(x[:3], "112" + x[:3]) if "-" in x else None)
    else:  # through the crosswalk to the register
        reg = dict(zip(p.reg["CIN"], p.reg["COD_ISTAT_COMUNE"].astype(str)))
        code = s["CODICE_STRUTTURA"].map(lambda c: reg.get(xw.get(c, c)))
    g = s.assign(code=code).groupby("code")["PRESENZE"].sum().to_dict()
    return {c: g.get(c, 0) for c in sorted(p.pop26)}


def ask_oct_occupancy(p, suspensions=True, changes=True, season=True, corrections=True):
    """Net bed-place occupancy in October 2025 by type: nights over bed-places available on the open days."""
    reg = establishment_table(p)
    s = p.survey[(p.survey["ANNO"] == 2025) & (p.survey["MESE"] == 10)]
    cir_n = s.groupby("CODICE_STRUTTURA")["PRESENZE"].sum().to_dict()
    var = p.var
    susp = set(var[var["TIPO_VARIAZIONE"] == "SOSPENSIONE TEMPORANEA"]["CIN"])
    bc = var[var["TIPO_VARIAZIONE"] == "POSTI LETTO"]
    if not corrections:  # a correction read as a change from its date
        bc = var[var["TIPO_VARIAZIONE"].isin(["POSTI LETTO", "RETTIFICA POSTI LETTO"])]
    num, den = defaultdict(float), defaultdict(float)
    for _, e in reg.iterrows():
        if e["start"] > dt.date(2025, 10, 31) or not e["CIR"]:
            continue
        days = season_days(e["PERIODO_APERTURA"], 2025, 10) if season else (31 if season_days(e["PERIODO_APERTURA"], 2025, 10) else 0)
        if days == 0:
            continue
        if suspensions and e["CIN"] in susp:
            days = 0
        hist = bc[bc["CIN"] == e["CIN"]]
        bd = 0
        for d in range(1, days + 1):
            day = dt.date(2025, 10, d)
            b = e["beds"]
            if changes:
                for _, h in hist.iterrows():
                    when = d_it(h["DATA_DECORRENZA"])
                    if day < when:
                        b = int(h["DA"])
                    else:
                        b = int(h["A"])
                    break
            bd += b
        num[e["TIPOLOGIA"]] += cir_n.get(e["CIR"], 0)
        den[e["TIPOLOGIA"]] += bd
    return {t: 100.0 * num[t] / den[t] for t in sorted(den) if den[t] > 0}


if __name__ == "__main__":
    import sys
    root = sys.argv[1]
    p = load(root)
    res = main_call(p)
    for c, r in res.items():
        R = r["residents"]
        print("%-22s gold %6.2f gb %6.2f R1ct %6.2f R2ct %6.2f R1prev %6.2f R2prev %6.2f R0 %6.2f miss %d/%d" % (
            r["name"][:22], r["golden"] / R, r["golden_b"] / R, r["R1_ct"] / R, r["R2_ct"] / R, r["R1_prev"] / R,
            r["R2_prev"] / R, r["R1_zero"] / R, r["missing_returns"], r["establishments"]))
    for k in ("golden", "R2_ct", "R1_ct", "R2_prev", "R1_zero"):
        print(k, [res[c]["name"] for c in designation(res, k)])
    print("tax", {q: round(v) for q, v in ask_tax_2025(p).items()}, "latest", {q: round(v) for q, v in ask_tax_2025(p, "latest").items()}, "sum", {q: round(v) for q, v in ask_tax_2025(p, "sum").items()})
    print("janapr nodedupe", ask_jan_apr(p, dedupe=False))
    print("occ nocorr", {k: round(v, 1) for k, v in ask_oct_occupancy(p, corrections=False).items()})
    print("janapr", ask_jan_apr(p))
    print("janapr reg", ask_jan_apr(p, "reg"))
    print("occ", {k: round(v, 1) for k, v in ask_oct_occupancy(p).items()})
    print("occ nosusp", {k: round(v, 1) for k, v in ask_oct_occupancy(p, suspensions=False).items()})
    print("occ nochg", {k: round(v, 1) for k, v in ask_oct_occupancy(p, changes=False).items()})
    print("occ noseason", {k: round(v, 1) for k, v in ask_oct_occupancy(p, season=False).items()})
