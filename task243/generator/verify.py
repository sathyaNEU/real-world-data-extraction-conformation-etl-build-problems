"""task243 independent verifier: reads only the shipped bundle (target/), the goldens, figures.json and submission.md;
recomputes the call by its own route (its own residence mapping, its own census reader, the growth balance written
afresh from cumulated age groups), both asks by its own code, reads back every format the pack ships, and requires the
goldens and the write-up to carry the same figures."""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

OFFICES = ["Kalinawan City", "City of Santa Cruz", "San Isidro", "Esperanza", "Magsaysay", "Mabini", "Libertad",
           "San Luis", "Del Carmen", "Quezon", "Rizal", "San Miguel"]


def office(s):
    t = re.sub(r"[^A-Z ]", " ", str(s).upper())
    t = " ".join(t.split())
    t = re.sub(r"^STA ", "SANTA ", t)
    t = re.sub(r"^SN ", "SAN ", t)
    t = re.sub(r"^CITY OF ", "", t)
    t = re.sub(r" CITY$", "", t)
    for o in OFFICES:
        if t == re.sub(r"^CITY OF ", "", o.upper()).replace(" CITY", ""):
            return o
    return None


def pdf_text(p):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(p).pages)


def census(path):
    wb = load_workbook(path, data_only=True)
    ws = wb.worksheets[0]
    out, cur = {}, None
    for row in ws.iter_rows(values_only=True):
        a, b = row[0], row[1]
        if isinstance(a, str) and office(a) and b is None:
            cur = office(a)
            out[cur] = np.zeros(17)
        elif cur and isinstance(a, str) and a.strip()[:1].isdigit() and isinstance(b, (int, float)):
            out[cur][min(int(a.split()[0]) // 5, 16)] = b
    return out


def balance(p1, p2, d, nm, t, lo=15, hi=65):
    """completeness, one over the orthogonal slope of (birthday rate less growth rate plus net movement rate above x)
    against (registered death rate above x), x from lo to hi by five"""
    up = lambda a: np.cumsum(a[::-1])[::-1]
    P1, P2, Dx, Mx = up(p1), up(p2), up(d), up(nm)
    xs, ys = [], []
    for x in range(lo, hi + 1, 5):
        i = x // 5
        pyl = t * math.sqrt(P1[i] * P2[i])
        nx = (p1[i - 1] * p1[i] * p2[i - 1] * p2[i]) ** 0.25 / 5
        xs.append(Dx[i] / pyl)
        ys.append(nx * t / pyl - math.log(P2[i] / P1[i]) / t + Mx[i] / pyl)
    xs, ys = np.array(xs), np.array(ys)
    return float(xs.std() / ys.std())


def main(target, golden, figures, submission):
    fig = json.load(open(figures))
    rd = lambda f, **kw: pd.read_csv(os.path.join(target, f), **kw)
    # every format the pack ships, each carrying what the build leans on
    tor = pdf_text(os.path.join(target, "crvs_review_terms_of_reference_2023.pdf"))
    assert "A death belongs to the city or municipality of the deceased's usual residence at death." in tor, "verify: ToR"
    assert "D1 below 80 per cent." in tor, "verify: the alert"
    cov = pdf_text(os.path.join(target, "cph2020_special_tabulation_cover_note.pdf"))
    assert "ELSEWHERE IN THE PHILIPPINES" in cov, "verify: cover note"
    eml = open(os.path.join(target, "crip2024_review_request.eml"), encoding="utf-8").read()
    assert eml.startswith("From: ") and "Subject: " in eml, "verify: request"
    for f in ("lcro_capacity_survey_jul2023.xlsx", "pho_health_office_clinical_staff_2019_2023.xlsx"):
        assert load_workbook(os.path.join(target, f)).worksheets, "verify: %s" % f
    c15 = census(os.path.join(target, "popcen2015_household_population_age_sex_kalinawan.xlsx"))
    c20 = census(os.path.join(target, "cph2020_household_population_age_sex_kalinawan.xlsx"))
    assert sorted(c15) == sorted(OFFICES) == sorted(c20), "verify: census tables"
    # deaths of residents in the interval, each once
    d = rd("crs_death_records_extract_20230331.csv", dtype=str, keep_default_na=False).drop_duplicates()
    d = d[(d["CERT_TYPE"] == "DEATH") & (d["RES_PROVINCE"].str.strip().str.upper() == "KALINAWAN")].copy()
    d["o"] = d["RES_CITY_MUN"].map(office)
    assert d["o"].notna().all(), "verify: every resident's residence maps"
    d = d.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"]).groupby(
        ["LAST_NAME", "FIRST_NAME", "MIDDLE_NAME", "SEX", "DATE_OF_DEATH", "DATE_OF_BIRTH"], sort=False).head(1)
    w = d[(d["DATE_OF_DEATH"] >= "2015-08-01") & (d["DATE_OF_DEATH"] <= "2020-04-30")].copy()
    w["a"] = np.where(w["AGE_UNIT"] == "YEARS", pd.to_numeric(w["AGE"], errors="coerce"),
                      np.where(w["AGE_UNIT"] == "", np.nan, 0.0))
    t = (pd.Timestamp("2020-05-01") - pd.Timestamp("2015-08-01")).days / 365.25
    # net movement by age group, movers placed half a group younger, carried to the interval
    r = rd("cph2020_special_tabulation_pdpfp_kalinawan.csv", keep_default_na=False)
    gi = {g: int(g.split()[0]) // 5 for g in r["AGE_GROUP"].unique()}
    r["g"] = r["AGE_GROUP"].map(gi)
    up = {o.upper(): o for o in OFFICES}
    done, comp = [], {}
    for o in OFFICES:
        x = w[w["o"] == o]
        known = x["a"].dropna()
        dd = np.bincount(np.minimum((known // 5).astype(int), 16), minlength=17).astype(float)
        dd *= len(x) / len(known)
        here = r[r["CITY_MUN_2020"] == o.upper()]
        mv = np.zeros(17)
        inn = here[~here["RESIDENCE_1MAY2015"].isin(["SAME CITY/MUNICIPALITY", "NOT STATED"])]
        np.add.at(mv, inn["g"].values, inn["PERSONS"].values)
        st = here[here["RESIDENCE_1MAY2015"] != "NOT STATED"].groupby("g")["PERSONS"].sum()
        ns = here[here["RESIDENCE_1MAY2015"] == "NOT STATED"].groupby("g")["PERSONS"].sum()
        im = inn.groupby("g")["PERSONS"].sum()
        for gg in ns.index:
            mv[gg] += ns[gg] * im.get(gg, 0) / st[gg]
        out = r[(r["RESIDENCE_1MAY2015"] == o.upper()) & (r["CITY_MUN_2020"] != o.upper())]
        np.subtract.at(mv, out["g"].values, out["PERSONS"].values)
        sh = 0.5 * mv
        sh[:-1] += 0.5 * mv[1:]
        comp[o] = balance(c15[o], c20[o], dd, sh * t / 5, t)
        if comp[o] < 0.80:
            done.append(o)
    assert done == fig["call"], ("verify: the call", done)
    for o in OFFICES:
        L = fig["lgus"][o]
        assert round(100 * comp[o]) == L["completeness"], ("verify: completeness", o, comp[o])
        assert L["interval"][0] <= round(100 * comp[o]) <= L["interval"][1], ("verify: interval", o)
    # ask A: each 2022 child once, by the mother's residence
    b = rd("crs_birth_records_extract_20230331.csv", dtype=str, keep_default_na=False).drop_duplicates()
    b = b[(b["MOTHER_RES_PROVINCE"].str.strip().str.upper() == "KALINAWAN") & (b["DATE_OF_BIRTH"].str[:4] == "2022")].copy()
    b["o"] = b["MOTHER_RES_CITY_MUN"].map(office)
    b = b.sort_values(["DATE_REGISTERED", "LCRO_CODE", "REGISTRY_NO"]).groupby(
        ["CHILD_FIRST_NAME", "CHILD_MIDDLE_NAME", "CHILD_LAST_NAME", "SEX", "DATE_OF_BIRTH", "MOTHER_FIRST_NAME",
         "MOTHER_MAIDEN_LAST_NAME"], sort=False).head(1)
    b["late"] = (pd.to_datetime(b["DATE_REGISTERED"]) - pd.to_datetime(b["DATE_OF_BIRTH"])).dt.days > 30
    for o in OFFICES:
        x = b[b["o"] == o]
        v = round(100.0 * (~x["late"]).sum() / len(x), 1)
        assert v == fig["lgus"][o]["b1"], ("verify: B1", o, v)
    # ask B: 2022 deaths of residents, each once; a certificate in the health office's name is a physician's only when
    # its signer held a physician's post that day
    ro = pd.read_excel(os.path.join(target, "pho_health_office_clinical_staff_2019_2023.xlsx"), header=3, dtype=str).fillna("")
    posts = [(office(a), n.strip().upper(), f[:10], (u[:10] or "9999"), "physician" in p.lower())
             for a, n, f, u, p in zip(ro["CITY_MUN"], ro["NAME"], ro["FROM"], ro["TO"], ro["POSITION"])]
    y = d[(d["DATE_OF_DEATH"] >= "2022-01-01") & (d["DATE_OF_DEATH"] <= "2022-12-31")]
    for o in OFFICES:
        x = y[y["o"] == o]
        n = 0
        for ttl, who, day in zip(x["CERTIFIER_TITLE"], x["CERTIFIED_BY"], x["DATE_OF_DEATH"]):
            if ttl in ("MD", "ATTENDING PHYSICIAN", "RESIDENT PHYSICIAN"):
                n += 1
            elif ttl in ("MHO", "CHO"):
                hit = [ph for oo, nn, f, u, ph in posts if oo == o and nn == who.strip().upper() and f <= day <= u]
                n += 1 if (not hit or hit[0]) else 0
        v = round(100.0 * n / len(x), 1)
        assert v == fig["lgus"][o]["c1"], ("verify: C1", o, v)
    # the goldens carry the figures
    wb = load_workbook(os.path.join(golden, "lcro_death_registration_completeness_2015_2020.xlsx"), data_only=True)
    ws = wb["Review"]
    got = 0
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] in OFFICES:
            L = fig["lgus"][row[0]]
            assert row[2] == L["completeness"] and row[3] == "%d to %d" % tuple(L["interval"]), ("verify: workbook", row)
            assert (row[4] == "Goes in") == (row[0] in done) and row[5] == L["b1"] and row[6] == L["c1"], ("wb", row)
            got += 1
    assert got == 12, "verify: workbook rows"
    import docx
    note = docx.Document(os.path.join(golden, "crvs_committee_note_2023.docx"))
    txt = " ".join(p.text for p in note.paragraphs)
    title = [p.text for p in note.paragraphs if all(o in p.text for o in done)]
    assert title and not any(o in title[0] for o in OFFICES if o not in done), "verify: note title names the five only"
    assert len(note.inline_shapes) == 1, "verify: one chart"
    sub = open(submission).read()
    for o in OFFICES:
        L = fig["lgus"][o]
        assert re.search(r"- %s: %d \(%d to %d\); %s" % (re.escape(o), L["completeness"], L["interval"][0],
                                                         L["interval"][1], "goes in" if o in done else "stays out"), sub), \
            ("verify: submission row", o)
        assert "%s %.1f" % (o, L["b1"]) in sub and "%s %.1f" % (o, L["c1"]) in sub, ("verify: submission asks", o)
    assert "%d" % fig["lgus"]["Esperanza"]["completeness"] in txt
    print("verify: call (%d offices), every completeness inside its interval, both asks, every format read back, "
          "goldens and write-up agree" % len(done))


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"),
         os.path.join(task, "generator", "figures.json"), os.path.join(task, "submission.md"))
