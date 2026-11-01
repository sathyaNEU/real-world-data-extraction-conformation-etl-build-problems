"""Independent verifier for task133: reads every shipped format back with its own code (pandas, python-docx,
openpyxl, a raw PDF stream decoder), takes every parameter from the shipped documents rather than the generator,
recomputes the call and both asks, and compares with generator/figures.json and the goldens.

    python3 task133/generator/verify.py          # exit 1 on any mismatch
"""
import base64
import json
import os
import re
import sys
import zlib
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd
from docx import Document
from openpyxl import load_workbook

GEN = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(GEN)
T = os.path.join(TASK, "target")
FAILS = []


def ok(label, cond, detail=""):
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    if not cond:
        FAILS.append(label)


def r_half_up(x, places=0):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def nearest_half(x):
    return float(Decimal(repr(float(x) * 2)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) / 2


# ---------------------------------------------------------------------- the governing documents, read back
def read_standard():
    d = Document(os.path.join(T, "CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx"))
    text = "\n".join(p.text for p in d.paragraphs)
    tabs = [[[c.text for c in row.cells] for row in t.rows] for t in d.tables]
    pd_tab = tabs[0]
    pdv = {int(g): float(v) / 100 for g, v in zip(pd_tab[0][1:], pd_tab[1][1:])}
    bands = []
    for row in tabs[1][1:]:
        nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", row[0])]
        if row[0].startswith("More than 0"):
            lo, hi = 0.0, nums[-1]
        elif "or more and less than" in row[0]:
            lo, hi = nums[0], nums[1]
        else:
            lo, hi = nums[0], 1e9
        bands.append((lo, hi, float(row[1])))
    lgd = {row[0]: float(row[2]) / 100 for row in tabs[2][1:]}
    seg = {}
    for row in tabs[3][1:]:
        for div in re.findall(r"\b([A-S]) [A-Z]", row[1]):
            seg[div] = row[0]
    return text, pdv, bands, lgd, seg


def read_scenario():
    wb = load_workbook(os.path.join(T, "ICAAP_2026_severe_scenario_board_approved.xlsx"), read_only=True)
    ws = wb["Industry sales"]
    rows = list(ws.iter_rows(values_only=True))
    hdr_i = [i for i, r in enumerate(rows) if r and r[0] == "ANZSIC 2006 division"][0]
    return {r[0]: float(r[3]) for r in rows[hdr_i + 1:] if r and r[0]}, rows[hdr_i]


def pdf_strings(path):
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<(.*?)>>\s*stream\r?\n(.*?)endstream", raw, re.S):
        head, data = m.group(1), m.group(2).strip()
        if b"ASCII85Decode" in head:
            data = base64.a85decode(data[2:-2] if data.startswith(b"<~") else data.rstrip(b"~>").rstrip(), adobe=False) \
                if not data.endswith(b"~>") else base64.a85decode(data[:-2].lstrip(b"<~"))
        if b"FlateDecode" in head:
            try:
                data = zlib.decompress(data)
            except zlib.error:
                continue
        out += [t.decode("latin-1") for t in re.findall(rb"\((.*?)\)\s*Tj", data)]
    return "\n".join(out)


def name_key(s):
    s = s.upper()
    s = s.replace(" LIMITED", " LTD").replace("&", "AND")
    s = re.sub(r"[^A-Z0-9 ()']", "", s)
    s = " ".join(s.split())
    return s[:20].rstrip()


def main():
    figs = json.load(open(os.path.join(GEN, "figures.json")))
    text, pdv, bands, lgd, segmap = read_standard()
    scen, scen_head = read_scenario()
    ok("standard read back: Table 1 has nine grades, Table 2 seven bands, Table 3 five codes",
       len(pdv) == 9 and len(bands) == 7 and len(lgd) == 5, (len(pdv), len(bands), len(lgd)))
    for phrase in ("the fall in the borrower's own sales", "50 per cent of its undrawn limit",
                   "carries an individually assessed provision", "follows its own division on the NZBN register",
                   "recoveries the bank received in the half", "an approved override is in force",
                   "financial year ends on 30 September"):
        ok("positive control: the standard files %r" % phrase, phrase in text)
    ok("scenario read back from its header row: 19 divisions", len(scen) == 19 and "NZD million" in str(scen_head[2]))
    rural = pdf_strings(os.path.join(T, "rural_book_stress_summary_ICAAP_2026.pdf"))
    ok("positive control: the rural PDF decodes (ASCII85 then Flate) and reads", "Rural book total" in rural)
    dep = pd.read_excel(os.path.join(T, "business_deposit_balances_2026-09-30.xlsx"))
    ok("positive control: the deposit listing reads", len(dep) > 500, len(dep))
    ind = pd.read_csv(os.path.join(T, "industry_sales_quarterly_south_island_2021Q4-2026Q3.csv"))
    ok("positive control: the industry series reads", len(ind) > 100, len(ind))

    def mult(fall):
        if fall <= 0:
            return 1.0
        for lo, hi, m in bands:
            if lo <= fall < hi:
                return m
        raise ValueError(fall)

    reg = pd.read_csv(os.path.join(T, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv"), dtype=str).fillna("")
    reg["div"] = reg["bic_code"].str[0]
    book = pd.read_csv(os.path.join(T, "business_lending_book_2026-09-30.csv"), dtype={"customer_no": str, "nzbn": str})
    cred = pd.read_csv(os.path.join(T, "operating_account_credits_2025-10_to_2026-09.csv"),
                       dtype={"customer_no": str}).fillna("")
    perf = book[book["risk_grade"] != "D"].copy()
    perf["div"] = perf["nzbn"].map(dict(zip(reg["nzbn"], reg["div"])))
    revolving = perf["product"].isin(["Business overdraft", "Revolving credit facility"])
    perf["ead"] = perf["drawn_nzd"] + revolving * 0.5 * (perf["limit_nzd"] - perf["drawn_nzd"]).clip(lower=0)
    ok("EAD of the performing book", r_half_up(perf["ead"].sum() / 1e6, 1) == figs["components"]["ead_nzd_m"],
       r_half_up(perf["ead"].sum() / 1e6, 1))
    ok("performing borrowers", perf["customer_no"].nunique() == figs["components"]["performing_borrowers"])

    lookup = {}
    for _, r in reg.iterrows():
        lookup.setdefault(name_key(r["entity_name"]), set()).add(r["div"])
        for tn in [x.strip() for x in r["trading_names"].split(";") if x.strip()]:
            lookup.setdefault(name_key(tn), set()).add(r["div"])
    own_div = perf.drop_duplicates("customer_no").set_index("customer_no")["div"].to_dict()
    names = perf.drop_duplicates("customer_no").set_index("customer_no")["customer_name"].to_dict()
    c = cred[cred["customer_no"].isin(own_div)].copy()
    c = c[~c["tran_type"].isin(["TFR", "INT", "LN"])]
    c = c[~((c["other_party"] == "INLAND REVENUE DEPT") | c["particulars"].str.startswith("GST REFUND")
            | c["particulars"].str.startswith("CLAIM"))]

    def source(row):
        if row["tran_type"] in ("MS", "DEP"):
            return own_div[row["customer_no"]]
        if row["other_party"] == name_key(names[row["customer_no"]].replace(" Ltd", " Limited")):
            return None
        hit = lookup.get(row["other_party"])
        if hit:
            assert len(hit) == 1, row["other_party"]
            return next(iter(hit))
        return own_div[row["customer_no"]]
    c["src"] = c.apply(source, axis=1)
    c = c[c["src"].notna()]
    c["chg"] = c["src"].map(scen) * c["amount_nzd"]
    agg = c.groupby("customer_no").agg(chg=("chg", "sum"), amt=("amount_nzd", "sum"))
    change = (agg["chg"] / agg["amt"]).to_dict()
    other = c[c["src"] != c["customer_no"].map(own_div)]
    other = other[~other["tran_type"].isin(["MS", "DEP"])]
    share = 100 * other["amount_nzd"].sum() / c["amount_nzd"].sum()
    ok("share of trading credits from other divisions", r_half_up(share, 0) == figs["components"]["other_division_share_pct"],
       round(share, 2))
    perf["grade"] = perf["risk_grade"].astype(int)
    perf["chg"] = perf["customer_no"].map(lambda x: change.get(x, scen[own_div[x]]))
    perf["pds"] = [min(1.0, pdv[g] * mult(-ch)) for g, ch in zip(perf["grade"], perf["chg"])]
    perf["loss"] = perf["pds"] * perf["security_code"].map(lgd) * perf["ead"]
    total = perf["loss"].sum()
    perf["seg"] = perf["div"].map(segmap)
    seg = perf.groupby("seg")["loss"].sum()
    ok("the call: book total at the nearest NZD 0.5 million", nearest_half(total / 1e6) ==
       figs["call"]["total_nzd_m_nearest_half"], round(total / 1e6, 4))
    for s, v in figs["segments_nzd_m"].items():
        ok("segment %s" % s, r_half_up(seg[s] / 1e6, 1) == v, round(seg[s] / 1e6, 4))

    # ------------------------------------------------------------------ ask A, read independently
    cm = pd.read_csv(os.path.join(T, "customer_master_extract_2026-10-09.csv"), dtype=str)
    seg_of_c = cm.set_index("customer_no")["nzbn"].map(dict(zip(reg["nzbn"], reg["div"]))).map(segmap).to_dict()
    wo = pd.read_csv(os.path.join(T, "write_offs_2023-10_to_2026-09.csv"), dtype={"customer_no": str})
    wo = wo[wo["portfolio"] == "Business"].copy()
    wo["d"] = pd.to_datetime(wo["posting_date"], format="%d/%m/%Y")
    first = wo.groupby("customer_no")["d"].min().to_dict()

    def halfname(d):
        if pd.Timestamp(2025, 10, 1) <= d <= pd.Timestamp(2026, 3, 31):
            return "H1"
        if pd.Timestamp(2026, 4, 1) <= d <= pd.Timestamp(2026, 9, 30):
            return "H2"
        return None
    wo["h"] = wo["d"].map(halfname)
    wo["seg"] = wo["customer_no"].map(seg_of_c)
    net = wo[wo["h"].notna()].groupby(["seg", "h"])["amount_nzd"].sum().to_dict()
    rc = pd.read_excel(os.path.join(T, "collections_receipts_FY2026.xlsx"), header=2, dtype={"Case No": str})
    cases = pd.read_csv(os.path.join(T, "collections_cases_open_2026-09-30.csv"), dtype=str)
    rc["owner"] = rc["Case No"].map(dict(zip(cases["case_no"], cases["customer_no"])))
    gr = pd.read_csv(os.path.join(T, "guarantees_register_2026-09-30.csv"), dtype=str)
    personal = set(cm.loc[cm["customer_type"] == "Personal", "customer_no"])
    gmap = dict(zip(gr["guarantor_customer_no"], gr["guaranteed_customer_no"]))
    rc["company"] = [gmap.get(o) if o in personal else o for o in rc["owner"]]
    rc = rc[(rc["Receipt Type"] != "Agency collection") & rc["company"].isin(first)].copy()
    rc["d"] = pd.to_datetime(rc["Receipt Date"])
    rc = rc[rc["d"] >= rc["company"].map(first)]
    rc["h"] = rc["d"].map(halfname)
    rc["seg"] = rc["company"].map(seg_of_c)
    for (s, h), v in rc[rc["h"].notna()].groupby(["seg", "h"])["Amount (NZD)"].sum().items():
        net[(s, h)] = net.get((s, h), 0.0) - v
    for key, v in figs["ask_a_net_credit_losses_nzd_k"].items():
        s, h = key.rsplit(" ", 1)
        ok("ask A %s" % key, r_half_up(net[(s, h)] / 1e3, 0) == v, round(net[(s, h)] / 1e3, 3))

    # ------------------------------------------------------------------ ask B, read independently
    snap = pd.read_csv(os.path.join(T, "risk_grade_snapshot_2025-09-30.csv"), dtype=str)
    snap = snap[snap["model_grade"].str.isdigit()].copy()
    grade = dict(zip(snap["customer_no"], snap["model_grade"].astype(int)))
    ov = pd.read_excel(os.path.join(T, "grade_overrides_2024-2026.xlsx"), dtype={"Customer No": str})
    asof = pd.Timestamp(2025, 9, 30)
    for _, o in ov.iterrows():
        if o["Customer No"] in grade and o["Approved"] <= asof and (pd.isna(o["Removed"]) or o["Removed"] > asof):
            grade[o["Customer No"]] = int(o["Override Grade"])
    holder = dict(zip(book["facility_no"], book["customer_no"]))
    mg = pd.read_csv(os.path.join(T, "customer_merge_log_2026-03-14.csv"), dtype=str)
    back = dict(zip(mg["surviving_customer_no"], mg["retired_customer_no"]))
    regs = pd.concat([pd.read_csv(os.path.join(T, f), dtype=str) for f in
                      ("default_register_business_FY2026.csv", "default_register_rural_FY2026.csv")])
    regs["d"] = pd.to_datetime(regs["default_date"], format="%d/%m/%Y")
    regs = regs[(regs["d"] >= pd.Timestamp(2025, 10, 1)) & (regs["d"] <= pd.Timestamp(2026, 9, 30))]
    dflt = {back.get(holder.get(f, c), holder.get(f, c)) for f, c in zip(regs["facility_no"], regs["customer_no"])}
    bands = {"Grades 1 to 3": (1, 3), "Grade 4": (4, 4), "Grade 5": (5, 5), "Grade 6": (6, 6), "Grades 7 to 9": (7, 9)}
    for lab, (lo, hi) in bands.items():
        mem = [c_ for c_, g in grade.items() if lo <= g <= hi]
        k = sum(1 for c_ in mem if c_ in dflt)
        ok("ask B %s defaults" % lab, k == figs["ask_b_defaults"][lab], k)
        ok("ask B %s share" % lab, r_half_up(100.0 * k / len(mem), 1) == figs["ask_b_share_pct"][lab],
           round(100.0 * k / len(mem), 3))

    # ------------------------------------------------------------------ the goldens carry the same figures
    gwb = load_workbook(os.path.join(TASK, "golden", "orari_icaap_business_stress_2027.xlsx"), data_only=True)
    ws = gwb["Summary"]
    ok("golden workbook headline", ws["E4"].value == figs["call"]["total_nzd_m_nearest_half"])
    seg_cells = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=4).value for r in range(7, 13)}
    ok("golden workbook segments", all(seg_cells[s] == v for s, v in figs["segments_nzd_m"].items()))
    ncl = gwb["Net credit losses"]
    cells = {}
    for r in range(5, 11):
        s = ncl.cell(row=r, column=1).value
        cells[s + " H1"], cells[s + " H2"] = ncl.cell(row=r, column=4).value, ncl.cell(row=r, column=7).value
    ok("golden workbook net credit losses", all(cells[k] == v for k, v in figs["ask_a_net_credit_losses_nzd_k"].items()))
    bt = gwb["Default back-test"]
    shares = {bt.cell(row=r, column=1).value: round(bt.cell(row=r, column=4).value * 100, 1) for r in range(5, 10)}
    ok("golden workbook default shares", shares == figs["ask_b_share_pct"], shares)
    paper = Document(os.path.join(TASK, "golden", "board_paper_business_stress_2027.docx"))
    ptxt = "\n".join(p.text for p in paper.paragraphs) + "\n" + "\n".join(
        " | ".join(c.text for c in row.cells) for t in paper.tables for row in t.rows)
    ok("golden paper states the call", "NZD %.1f million" % figs["call"]["total_nzd_m_nearest_half"] in ptxt)
    ok("golden paper carries a chart", len(paper.inline_shapes) == 1)
    ok("no em or en dash in any golden or the write-up", not re.search("[–—]", ptxt + open(
        os.path.join(TASK, "submission.md"), encoding="utf-8").read()))
    print("\n%d checks failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
