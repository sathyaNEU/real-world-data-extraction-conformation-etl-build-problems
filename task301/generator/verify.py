"""Independent verifier: reads only the shipped files under target/ and the golden deliverables, on its own code path
(pandas for the CSVs, its own XLSX, DOCX and PDF readers, vectorised microsimulation), and recomputes every graded
figure and the call against generator/figures.json and the golden workbook. Each reader is first proved on a
positive control. Exit 1 on any mismatch."""
import base64
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
T = os.path.join(TASK_DIR, "target")
GOLD = os.path.join(TASK_DIR, "golden")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


# ---------------------------------------------------------------- readers
def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    return [s.get("name") for s in wb.find("m:sheets", NS)]


def xlsx_rows(path, sheet_name):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rid = [s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
           for s in wb.find("m:sheets", NS) if s.get("name") == sheet_name][0]
    tgt = [r.get("Target") for r in rels if r.get("Id") == rid][0].lstrip("/")
    if not tgt.startswith("xl/"):
        tgt = "xl/" + tgt
    rows = []
    for row in ET.fromstring(z.read(tgt)).iter("{%s}row" % NS["m"]):
        vals = {}
        for c in row.findall("m:c", NS):
            col = 0
            for ch in re.match(r"([A-Z]+)", c.get("r")).group(1):
                col = col * 26 + ord(ch) - 64
            t, v = c.get("t"), c.find("m:v", NS)
            if t == "s":
                val = shared[int(v.text)]
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif v is None:
                val = None
            else:
                val = float(v.text)
            vals[col] = val
        if vals:
            rows.append([vals.get(i) for i in range(1, max(vals) + 1)])
    return rows


def docx_text(path):
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    return "\n".join("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras)


def pdf_text(path):
    data = open(path, "rb").read()
    chunks = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2])
            raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", raw):
            s = re.sub(rb"\\([0-7]{3})", lambda q: bytes([int(q.group(1), 8)]), s)
            s = s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(b"\\\\", b"\\")
            chunks.append(s.decode("cp1252", "replace"))
    return re.sub(r"\s+", " ", " ".join(chunks))


def num(s):
    return float(str(s).replace(",", ""))


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    fn = {k: os.path.join(T, v) for k, v in {
        "hh": "ecvv2026_households.csv", "pe": "ecvv2026_persons.csv", "fw": "ecvv2026_fieldwork_cases.csv",
        "reg": "cfv_register_extract_20261102.csv", "inc": "cfv_incidents_2025.xlsx", "codes": "territorial_codes.csv",
        "guid": "appraisal_guidance_child_poverty_2027.docx", "prop": "child_poverty_proposals_2027.pdf",
        "rules": "complemento_familiar_rules_2026.pdf", "cov": "complemento_familiar_coverage_2025.pdf",
        "res": "ecvv2026_main_results.pdf"}.items()}

    # ---------------------------------------------------------------- positive controls on every reader
    g = docx_text(fn["guid"])
    pr, ru, cv, rs = pdf_text(fn["prop"]), pdf_text(fn["rules"]), pdf_text(fn["cov"]), pdf_text(fn["res"])
    ok("C1 DOCX reader: the guidance's title and its section 3.5 read back",
       "Appraisal of the 2027 child poverty measures" in g and "receives during 2027" in g)
    ok("C2 PDF reader: proposals, rules, coverage and results read back with their euro signs",
       "Prestación Infancia Directa" in pr and "€" in ru and "per cent of entitled families" in cv
       and "at-risk-of-poverty" in rs)
    ok("C3 XLSX reader: the incident workbook's four quarterly sheets", xlsx_sheets(fn["inc"]) ==
       ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"])
    hh = pd.read_csv(fn["hh"], sep=";", decimal=",", dtype={"household_id": str, "province": str})
    pe = pd.read_csv(fn["pe"], sep=";", decimal=",", dtype={"household_id": str})
    ok("C4 CSV reader: Spanish-locale household and person files", len(hh) > 10000 and len(pe) >= 25000
       and hh["household_weight"].dtype.kind == "f")

    # ---------------------------------------------------------------- the filed definitions
    line = num(re.search(r"poverty line for 2027 is €([\d,]+)", g).group(1))
    up = 1 + float(re.search(r"increased by ([\d.]+) per cent", g).group(1)) / 100
    born = int(re.search(r"born in (\d{4}) or later", g).group(1))
    base_year = int(re.search(r"taken as (\d{4}) less", g).group(1))
    seg = {k: pr[pr.index(a):pr.index(b) if b else pr.index("Notes on the measures")] for k, a, b in (
        ("A", "A. Prestación", "B. Ayuda"), ("B", "B. Ayuda", "C. Complemento"), ("C", "C. Complemento", "D. Suplemento"),
        ("D", "D. Suplemento", "E. Complemento"), ("E", "E. Complemento", None))}
    a_rate = num(re.search(r"€(\d+) a month per child", seg["A"]).group(1))
    a_lim = num(re.search(r"below €([\d,]+)", seg["A"]).group(1))
    b_rate = num(re.search(r"€(\d+) a month per child", seg["B"]).group(1))
    c_lo, c_hi = [num(x) for x in re.search(r"from €([\d,]+) to €([\d,]+)", seg["C"]).groups()]
    d_rate = num(re.search(r"€(\d+) a month per child", seg["D"]).group(1))
    e_rate = num(re.search(r"€(\d+) a month more", seg["E"]).group(1))
    cfv = num(re.search(r"€(\d+) a month for each child", ru).group(1))
    old_lim = num(re.search(r"limit of €([\d,]+)", ru).group(1))
    take = float(re.search(r"reached ([\d.]+) per cent", cv).group(1)) / 100

    # ---------------------------------------------------------------- the survey, vectorised
    pe["age"] = base_year - pe["birth_year"]
    grp = pe.groupby("household_id")
    big = grp["age"].apply(lambda a: int((a >= 14).sum()))
    small = grp["age"].apply(lambda a: int((a < 14).sum()))
    kids = grp["birth_year"].apply(lambda b: int((b >= born).sum()))
    hh = hh.set_index("household_id")
    hh["eq"] = np.where(big[hh.index] > 0, 1 + 0.5 * (big[hh.index] - 1) + 0.3 * small[hh.index],
                        1 + 0.3 * (small[hh.index] - 1))
    hh["kids"] = kids[hh.index].values
    hh["cfv25"] = hh["complemento_familiar_2025"].fillna(0.0)
    hh["base"] = hh["disposable_income_2025"] * up
    hh["comp"] = (hh["disposable_income_2025"] - hh["cfv25"]) / hh["eq"]
    hh["below"] = hh["base"] / hh["eq"] < line
    k = hh[hh["kids"] > 0].copy()
    annual = {
        "A": np.where((k["irpf_return_2025"] == 1) & (k["irpf_gross_income_2025"] < a_lim), 12 * a_rate * k["kids"], 0),
        "B": np.where(k["comp"] < line, 12 * b_rate * k["kids"], 0),
        "C": np.where((k["comp"] >= c_lo) & (k["comp"] < c_hi) & (k["complemento_familiar_now"] != 1),
                      12 * cfv * k["kids"], 0),
        "D": np.where(k["tenure"].str.startswith("rented") & (k["comp"] < line), 12 * d_rate * k["kids"], 0),
        "E": np.where(k["complemento_familiar_now"] == 1, 12 * e_rate * k["kids"], 0)}
    wk = (k["household_weight"] * k["kids"]).values
    below = k["below"].values
    basepe = (k["base"] / k["eq"]).values
    eqv = k["eq"].values

    def lifted(pay):
        return below & (basepe + pay / eqv >= line) & (pay > 0)
    static = {m: float(wk[lifted(annual[m])].sum()) for m in annual}
    a_prov = {pc: float(wk[lifted(annual["A"]) & (k["province"].values == pc)].sum()) for pc in ("81", "82", "83")}

    # ---------------------------------------------------------------- the register's claiming curves and lag
    reg = pd.read_csv(fn["reg"], sep="|", dtype=str, keep_default_na=False)

    def pdate(s):
        return pd.to_datetime(s, format="%d/%m/%Y") if "/" in s else pd.to_datetime(s, format="%Y-%m-%d")

    def pmon(s):
        if not s:
            return None
        y, m = (s.split("/")[1], s.split("/")[0]) if "/" in s else s.split("-")
        return int(y) * 12 + int(m) - 1
    reg["claim"] = reg["claim_date"].map(pdate)
    reg["dec"] = reg["decision_date"].map(lambda s: pdate(s) if s else pd.NaT)
    reg["inc"] = reg["computable_income_per_eq_adult"].map(lambda s: float(s.replace(",", ".")) if s else np.nan)
    reg["first"] = reg["first_month_paid"].map(pmon)
    reg["last"] = reg["last_month_paid"].map(pmon)
    fin = reg[reg["dec"].notna()].sort_values(["case_number", "dec"]).groupby("case_number").tail(1)
    gi = fin[(fin["claim_type"] == "INITIAL") & (fin["decision"] == "GRANTED")]
    cm = gi["claim"].dt.year * 12 + gi["claim"].dt.month - 1

    def curve(mask, start, n):
        rel = (cm[mask] - start + 1)
        rel = rel[(rel >= 1) & (rel <= n)]
        c = np.cumsum(np.bincount(rel, minlength=n + 1)[1:])
        return c / c[-1]
    widen = curve((gi["inc"] >= old_lim) & (gi["inc"] < c_lo) & (gi["claim"] >= "2024-04-01"), 2024 * 12 + 3, 31)
    launch = curve((gi["claim"] < "2024-04-01") & (gi["inc"] < old_lim), 2022 * 12 + 9, 18)
    nrows = reg["case_number"].value_counts()
    one = gi[gi["case_number"].map(nrows) == 1]
    lag = (one["first"] - (one["claim"].dt.year * 12 + one["claim"].dt.month - 1)).value_counts(normalize=True)

    def months_dist(cur):
        d = {}
        prev = 0.0
        for mo in range(1, 13):
            sh = cur[mo - 1] - prev
            prev = cur[mo - 1]
            for kk, pk in lag.items():
                n_ = max(0, 13 - mo - int(kk))
                d[n_] = d.get(n_, 0.0) + sh * pk
        return d

    def year27(m, cur):
        d = months_dist(cur)
        tot = 0.0
        for n_, q in d.items():
            if n_:
                tot += q * wk[lifted(annual[m] / 12.0 * n_)].sum()
        return take * tot
    y27 = {"A": static["A"], "E": static["E"], "B": year27("B", launch), "C": year27("C", widen),
           "D": year27("D", launch)}
    call = max(y27, key=y27.get)
    ok("V1 the call is measure A", call == "A", " > ".join("%s %.0f" % (m, y27[m]) for m in sorted(y27, key=lambda m: -y27[m])))
    ok("V2 the default path (full year at the coverage rate) files C", max(
        {m: (take * static[m] if m in "BCD" else static[m]) for m in static}.items(), key=lambda x: x[1])[0] == "C")
    r100 = lambda x: "{:,}".format(int(100 * round(x / 100.0)))
    ok("V3 A's region and province figures recompute and sit in figures.json",
       r100(static["A"]) in figs and all(r100(v) in figs for v in a_prov.values()),
       "%s %s" % (r100(static["A"]), {p: r100(v) for p, v in a_prov.items()}))
    ok("V4 C's full-year figure, the rivals' bound and E recompute",
       r100(static["C"]) in figs and max(y27["B"], y27["C"], y27["D"]) < 3000 and r100(static["E"]) in figs)

    # ---------------------------------------------------------------- ask 1
    codes = pd.read_csv(fn["codes"], dtype=str).set_index("municipality_code")["province_code"].to_dict()
    moves = []
    for sh in xlsx_sheets(fn["inc"]):
        rows = xlsx_rows(fn["inc"], sh)
        hi = [i for i, r in enumerate(rows) if r and r[0] == "Date"][0]
        for r in rows[hi + 1:]:
            if r and len(r) >= 5 and r[3] == "Change of address":
                day = pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(r[0]))
                moves.append((r[1], day.year * 12 + day.month - 1 + 1, str(r[4])))
    mv = {}
    for fam, eff, new in sorted(moves, key=lambda x: x[1]):
        mv.setdefault(fam, []).append((eff, new))
    revocation_dates = reg[reg["claim_type"] == "REVOCATION"].groupby("case_number")["dec"].min()
    awards = reg[(reg["claim_type"] != "REVOCATION") & reg["first"].notna() & reg["dec"].notna()
                 & (reg["dec"] <= "2025-12-31")].copy()
    stood = (awards["decision"] == "GRANTED") | ((awards["decision"] == "REVOKED") & (
        awards["case_number"].map(revocation_dates) > pd.Timestamp("2025-12-31")))
    awards = awards[stood]
    golden_wb = xlsx_rows(os.path.join(GOLD, "appraisal_annex_2027.xlsx"), "Complemento 2025")
    gw = {r[0]: r[1:5] for r in golden_wb if r and r[0] in ("Valdemora", "Las Cuencas", "Sierra del Alba")}
    names = {"81": "Valdemora", "82": "Las Cuencas", "83": "Sierra del Alba"}
    all_ok = True
    for j, (y, mth) in enumerate(((2025, 3), (2025, 6), (2025, 9), (2025, 12))):
        t = y * 12 + mth - 1
        cov = awards[(awards["first"] <= t) & (awards["last"].isna() | (awards["last"] >= t))]
        cov = cov.sort_values("dec").groupby("family_number").tail(1)
        cnt = {}
        for fam, muni in zip(cov["family_number"], cov["municipality"]):
            for eff, new in mv.get(fam, []):
                if eff <= t:
                    muni = new
            cnt[codes[muni]] = cnt.get(codes[muni], 0) + 1
        for pc, name in names.items():
            if int(gw[name][j]) != cnt[pc] or "{:,}".format(cnt[pc]) not in figs:
                all_ok = False
    ok("V5 ask 1: all 12 family counts recompute and match the golden workbook and figures.json", all_ok)

    # ---------------------------------------------------------------- ask 2
    fw = pd.read_csv(fn["fw"], dtype=str)
    parts = fw["dwelling"].str.split("-", expand=True)
    fw["key"] = parts[0] + ":" + parts[2]
    fw["issue"] = fw["issue"].astype(int)
    lastc = fw.sort_values("issue").groupby("key").tail(1)
    lastc = lastc.assign(prov=lastc["key"].str[:5].map(codes))
    elig = lastc[~lastc["result"].isin(["empty dwelling", "not a dwelling", "address not found"])]
    gf = {r[0]: r[1:4] for r in xlsx_rows(os.path.join(GOLD, "appraisal_annex_2027.xlsx"), "ECVV 2026 fieldwork")
          if r and r[0] in names.values()}
    ok2 = True
    for pc, name in names.items():
        e = elig[elig["prov"] == pc]
        n_el, n_co = len(e), int((e["result"] == "complete interview").sum())
        rate = round(100.0 * n_co / n_el, 1)
        if (int(gf[name][0]), int(gf[name][1]), round(gf[name][2], 1)) != (n_el, n_co, rate) or "%.1f" % rate not in figs:
            ok2 = False
    ok("V6 ask 2: eligible dwellings, complete interviews and response rates recompute and match", ok2)

    # ---------------------------------------------------------------- the golden note
    note = pdf_text(os.path.join(GOLD, "cabinet_note_child_poverty_2027.pdf"))
    ok("V7 the note recommends measure A with the region and province figures",
       "Fund measure A" in note and r100(static["A"]) in note and all(r100(v) in note for v in a_prov.values()))
    nb = open(os.path.join(GOLD, "cabinet_note_child_poverty_2027.pdf"), "rb").read()
    ok("V8 the note is no more than two pages and carries its chart", len(re.findall(rb"/Type\s*/Page[^s]", nb)) <= 2
       and b"/Subtype /Image" in nb)

    bad = [o for o in OUT if not o[1]]
    for label, good, detail in OUT:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("%d checks, %d failed" % (len(OUT), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
