"""An independent recomputation of task482's golden from target/ alone, without bundle.py: pandas over the CSVs, openpyxl
over the workbooks, pdfplumber over the PDFs' words. It checks figures.json and the three golden files.

    python3 task482/generator/verify.py
"""
import datetime as dt
import json
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
K = 3.1173e-8
FAIL = []


def say(name, ok):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAIL.append(name)


def half_up(x, nd=0):
    m = 10 ** nd
    return float(np.sign(x) * np.floor(abs(x) * m + 0.5) / m)


def book(fn, sheet, skip=0):
    return pd.read_excel(os.path.join(T, fn), sheet_name=sheet, skiprows=skip, dtype=object)


def words(fn):
    import pdfplumber
    with pdfplumber.open(os.path.join(T, fn)) as pdf:
        return " ".join(" ".join(w["text"] for w in pg.extract_words()) for pg in pdf.pages)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    plants = book("deq_printing_plants_register_2027-02.xlsx", "Plants")
    oxs = book("deq_printing_plants_register_2027-02.xlsx", "Oxidizers")
    capt = book("deq_printing_plants_register_2027-02.xlsx", "Capture")
    name_of = dict(zip(plants["Facility no."].astype(str), plants["Plant"]))
    for fn_, pl in zip(plants["Former name"], plants["Plant"]):
        if isinstance(fn_, str):
            name_of[re.search(r"facility (\d+)", fn_).group(1)] = pl
    cf = dict(zip(plants["Plant"], plants["Carbon content of VOC (lb C per lb VOC)"]))
    ce = dict(zip(capt["Plant"], capt["Capture efficiency (%)"].astype(float) / 100))
    tag_of, rated = {}, {}
    for _, r in oxs.iterrows():
        for t in re.findall(r"[A-Z]{3,4}-RTO\d?", r["Historian tag"]):
            tag_of[t] = r["Plant"]
        rated[r["Plant"]] = float(r["Rated airflow (scfm)"])

    sds = book("safety_data_sheet_master_2027-01.xlsx", "Products").set_index("Product code")
    log = book("safety_data_sheet_master_2027-01.xlsx", "Revision log")

    def lb_per_gal(code, d):
        for _, r in log[log["Product code"] == code].iterrows():
            m = re.search(r"density ([\d.]+) lb/gal and VOC ([\d.]+) per cent", str(r["Change"]))
            if m and d < pd.Timestamp(r["Effective from"]).date():
                return float(m.group(1)) * float(m.group(2)) / 100
        s = sds.loc[code]
        if str(s["VOC basis"]).startswith("%"):
            return float(s["Density (lb/gal)"]) * float(s["VOC"]) / 100
        num = lambda v: 0.0 if pd.isna(v) else float(v)
        return float(s["VOC"]) * (1 - (num(s["Water (vol %)"]) + num(s["Exempt compounds (vol %)"])) / 100)

    # press VOC used, by plant and production day (the day's hours run from its first start to its last end)
    pr = pd.read_csv(os.path.join(T, "press_material_use_2026.csv"), dtype=str)
    pr["plant"] = pr["facility_no"].map(name_of)
    pr["q"] = pr["quantity"].astype(float)
    pr["dens"] = pr["material_code"].map(lambda c: float(sds.loc[c, "Density (lb/gal)"]))
    pr["gal"] = np.where(pr["uom"] == "LB", pr["q"] / pr["dens"], pr["q"])
    vpg = {(c, d): lb_per_gal(c, dt.date.fromisoformat(d)) for c, d in set(zip(pr["material_code"], pr["log_date"]))}
    pr["lb"] = pr["gal"] * [vpg[(c, d)] for c, d in zip(pr["material_code"], pr["log_date"])]
    pr["st"] = pd.to_datetime(pr["start_local"])
    pr["en"] = pd.to_datetime(pr["end_local"])
    day = pr.groupby(["plant", "log_date"]).agg(lb=("lb", "sum"), st=("st", "min"), en=("en", "max")).reset_index()

    # historians on Central time, PROCESS hours into their production day's window
    h = pd.read_csv(os.path.join(T, "oxidizer_historian_hourly_2026.csv"), dtype=str)
    h = h[h["mode"] == "PROCESS"].copy()
    h["plant"] = h["unit_tag"].map(tag_of)
    utc = pd.to_datetime(h["hour_beginning_utc"].str.rstrip("Z"))
    cdt = (utc >= pd.Timestamp("2026-03-08 08:00")) & (utc < pd.Timestamp("2026-11-01 07:00"))
    h["local"] = utc - pd.to_timedelta(np.where(cdt, 5, 6), unit="h")
    h["flow"] = np.where(h["exhaust_flow_scfm"].notna() & (h["exhaust_flow_scfm"] != ""),
                         pd.to_numeric(h["exhaust_flow_scfm"], errors="coerce"),
                         pd.to_numeric(h["fan_speed_pct"], errors="coerce") / 100 * h["plant"].map(rated))
    win = day[day["plant"].isin(rated)]
    hk = []
    for _, r in win.iterrows():
        t = r["st"].floor("h")
        while t < r["en"]:
            hk.append((r["plant"], t, r["log_date"]))
            t += pd.Timedelta(hours=1)
    hk = pd.DataFrame(hk, columns=["plant", "local", "log_date"])
    hh = h.merge(hk, on=["plant", "local"], how="left")
    say("V every PROCESS hour falls in a production day's window", hh["log_date"].notna().all())
    dd = hh.groupby(["plant", "log_date"]).agg(hours=("flow", "size"), flow=("flow", "mean")).reset_index()
    day = day.merge(dd, on=["plant", "log_date"], how="left")

    # the tests: words of the summary, runs on carbon
    txt = words("oxidizer_performance_tests_2017_2026.pdf")
    blocks = re.split(r"(?=\b[A-Z][a-z]+(?: [A-Z][a-z]+)* \(facility \d{4}\), [A-Z]{3,4}-RTO)", txt)
    ci, co = [], []
    n_tests = 0
    for b in blocks:
        if "(facility" not in b or "Test of" not in b:
            continue
        n_tests += 1
        mult = 3.0 if "as propane" in b else 1.0
        for m in re.finditer(r"\b([123]) \d{2}:\d{2} ([\d.]+) ([\d.]+) [\d,]+ [\d,]+ [\d.]+ [\d.]+ [\d.]+", b):
            ci.append(float(m.group(2)) * mult)
            co.append(float(m.group(3)) * mult)
    ci, co = np.array(ci), np.array(co)
    say("V %d tests, %d runs read from the summary" % (n_tests, len(ci)), n_tests == 28 and len(ci) == 84)
    Fv = co[ci < 2000].mean()
    pv = (co[ci > 3000] / ci[ci > 3000]).mean()
    say("V the relation: floor %.2f ppmv as carbon, %.3f per cent above the knee (figures.json %.1f, %.2f)" %
        (Fv, 100 * pv, f["components"]["floor_ppmc"], f["components"]["pass_pct"]),
        round(Fv, 1) == f["components"]["floor_ppmc"] and round(100 * pv, 2) == f["components"]["pass_pct"])

    tons = {}
    for pl in plants["Plant"]:
        dp = day[day["plant"] == pl]
        used = dp["lb"].sum() / 2000
        if pl not in rated:
            tons[pl] = used
            continue
        cap_lb = dp["lb"] * ce[pl]
        inlet = cap_lb / dp["hours"] * cf[pl] / (dp["flow"] * 60 * K)
        out = np.maximum(Fv, pv * inlet)
        ctl = (out * dp["flow"] * 60 * K / cf[pl] * dp["hours"]).sum() / 2000
        tons[pl] = used * (1 - ce[pl]) + ctl
    whole = {pl: int(half_up(v)) for pl, v in tons.items()}
    say("V each plant's 2026 press VOC, whole tons, as figures.json",
        all(whole[pl] == f["plants"][pl]["press_voc_tons"] for pl in whole))
    cov = sorted(pl for pl, v in tons.items() if v >= 25)
    say("V the call: %s" % cov, cov == f["call"]["plants"])
    below = max((v, pl) for pl, v in tons.items() if pl not in cov)
    nb = f["components"]["nearest_below"]
    say("V the nearest below: %s %d, %d short" % (below[1], half_up(below[0]), half_up(25 - below[0])),
        below[1] == nb["name"] and half_up(25 - below[0]) == nb["short_tons"])

    # ask A
    iss = pd.read_csv(os.path.join(T, "stores_cleaning_issues_2026.csv"), dtype=str)
    iss = iss[~iss["issued_to"].str.startswith("PRESS")]
    iss["plant"] = iss["facility_no"].map(name_of)
    iss["lb"] = [float(q) * lb_per_gal(c, dt.date.fromisoformat(d)) for q, c, d in
                 zip(iss["quantity"], iss["material_code"], iss["issue_date"])]
    clean = iss.groupby("plant")["lb"].sum()
    prof = {}
    for m in re.finditer(r"(CB-\d{4}-0\d) .*? (Cleaning|Press operations) ([\d.]+) ", words("cantrell_bend_waste_profiles_2026.pdf")):
        prof[m.group(1)] = (m.group(2), float(m.group(3)))
    man = pd.read_csv(os.path.join(T, "cantrell_bend_manifests_2026.csv"), dtype=str)
    man["plant"] = man["generator_facility_no"].map(name_of)
    man = man[man["waste_profile"].map(lambda p_: prof[p_][0] == "Cleaning")]
    man["lb"] = man["net_weight"].astype(float) * np.where(man["weight_unit"] == "KG", 2.20462, 1.0) * \
        man["waste_profile"].map(lambda p_: prof[p_][1] / 100)
    tk = pd.read_csv(os.path.join(T, "wexcombe_service_tickets_2026.csv"), dtype=str)
    tk["plant"] = tk["facility_no"].map(name_of)
    tk["lb"] = (tk["fresh_added_gal"].astype(float) - tk["spent_removed_gal"].astype(float)) * \
        tk["solvent_product"].map(lambda c: lb_per_gal(c, dt.date(2026, 12, 31)))
    pay = pd.read_csv(os.path.join(T, "solvent_vendor_payments_2026.csv"), dtype=str)
    ex = pay["description"].str.extract(r"fresh ([\d.]+) gal (\S+), spent ([\d.]+) gal recovered").dropna()
    st_lb = pd.Series([(float(a) - float(c)) * lb_per_gal(b, dt.date(2026, 12, 31)) for a, b, c in ex.values],
                      index=ex.index)
    st_pl = pay.loc[ex.index, "facility_no"].map(name_of)
    a_t = {}
    for pl in plants["Plant"]:
        v = clean.get(pl, 0) - man[man["plant"] == pl]["lb"].sum() + tk[tk["plant"] == pl]["lb"].sum() + \
            st_lb[st_pl == pl].sum()
        a_t[pl] = half_up(v / 2000, 1)
    say("V ask A: each plant's cleaning VOC to a tenth of a ton, as figures.json",
        all(abs(a_t[pl] - f["plants"][pl]["cleaning_voc_tons"]) < 1e-9 for pl in a_t))

    # ask B
    cat = pd.read_csv(os.path.join(T, "haldane_catalog_2026-04.csv"), dtype=str).set_index("item_no")
    repl = {r: i for i, r in cat["replaces_item"].dropna().items()}
    hal = book("haldane_statement_2026.xlsx", "Statement detail", skip=1)
    hal["Doc date"] = pd.to_datetime(hal["Doc date"])
    hal["Ship date"] = pd.to_datetime(hal["Ship date"])
    hal = hal[hal["Ship date"].dt.year == 2026].copy()
    hal["item"] = [repl.get(str(i), str(i)) if dd_ < pd.Timestamp("2026-04-01") else str(i)
                   for i, dd_ in zip(hal["Item"], hal["Doc date"])]
    hal["code"] = hal["item"].map(cat["product_code"])
    hal["sold"] = hal["item"].map(cat["sold_by"])
    hal["kind"] = hal["code"].map(sds["Product type"]).str.upper()
    hal = hal[hal["kind"].isin(["INK", "COATING", "ADHESIVE"])]
    hal["gal"] = np.where(hal["sold"] == "LB", hal["Qty"].astype(float) /
                          hal["code"].map(sds["Density (lb/gal)"]).astype(float), hal["Qty"].astype(float))
    pn = {pl.upper(): pl for pl in plants["Plant"]}
    pn["THAMESIDE LAMINATING"] = [pl for pl in plants["Plant"] if pl.startswith("Kelvedon")][0]
    hal["plant"] = hal["Ship to"].map(pn)
    cv = pd.read_csv(os.path.join(T, "corvane_invoice_export_2026.csv"), dtype=str)
    cv = cv[cv["SHIP_DATE"].str.startswith("2026")].copy()
    cv["code"] = "CV-" + cv["ITEM"].str.rsplit("-", n=1).str[0]
    cv = cv[cv["code"].map(sds["Product type"]).str.upper().isin(["INK", "COATING", "ADHESIVE"])]
    cv["plant"] = cv["SHIP_TO"].map(pn)
    cnt = pd.read_csv(os.path.join(T, "stock_counts_2026.csv"), dtype=str)
    cnt["kind"] = cnt["material_code"].map(sds["Product type"]).str.upper()
    cnt = cnt[cnt["kind"].isin(["INK", "COATING", "ADHESIVE"])]
    cnt["gal"] = np.where(cnt["uom"] == "LB", cnt["quantity"].astype(float) /
                          cnt["material_code"].map(sds["Density (lb/gal)"]).astype(float),
                          cnt["quantity"].astype(float))
    cnt["plant"] = cnt["facility_no"].map(name_of)
    cnt["signed"] = np.where(cnt["count_date"] == "2026-01-01", cnt["gal"], -cnt["gal"])
    pk = pr[pr["material_code"].map(sds["Product type"]).str.upper().isin(["INK", "COATING", "ADHESIVE"])]
    b_t = {}
    for pl in plants["Plant"]:
        v = cnt[cnt["plant"] == pl]["signed"].sum() + hal[hal["plant"] == pl]["gal"].sum() + \
            cv[cv["plant"] == pl]["QTY"].astype(float).sum() - pk[pk["plant"] == pl]["gal"].sum()
        b_t[pl] = int(half_up(v))
    say("V ask B: each plant's unaccounted gallons, as figures.json",
        all(b_t[pl] == f["plants"][pl]["unaccounted_gal"] for pl in b_t))

    # the filed sentences, read back through the same extractor
    rule = re.sub(r"\s+", " ", words("deq_rule_18-4_draft_2027-02-19.pdf"))
    letter = re.sub(r"\s+", " ", words("deq_information_request_2027-01-12.pdf"))
    say("V the rule files the applicability (25 tons or more in 2026, used less destroyed) and the cleaning record",
        "VOC emitted from its presses in calendar year 2026 was 25 tons or more" in rule and
        "less the VOC that the plant's capture systems and control devices destroyed" in rule and
        "less the VOC in spent cleaning materials shipped off site" in rule)
    say("V the letter files Central time and Thameside Laminating's records under facility 0117",
        "local (Central) time" in letter and "Thameside Laminating (facility 0117)" in letter)

    # the golden files
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(G, "deq_rule18-4_applicability_2027.xlsx"), data_only=True)
    rows = list(wb["Plants"].iter_rows(min_row=2, values_only=True))
    say("V the workbook's Plants sheet carries every plant's tons, coverage, cleaning VOC and gallons",
        all(r[2] == f["plants"][r[0]]["press_voc_tons"] and (r[3] == "Yes") == f["plants"][r[0]]["covered"] and
            abs(r[4] - f["plants"][r[0]]["cleaning_voc_tons"]) < 1e-9 and r[5] == f["plants"][r[0]]["unaccounted_gal"]
            for r in rows) and len(rows) == 14)
    app = [r[0] for r in wb["Appendix A"].iter_rows(min_row=5, values_only=True) if r[0] and r[1]]
    say("V Appendix A lists the five", app == f["call"]["plants"])
    gc = pd.read_csv(os.path.join(G, "deq_printing_press_voc_2026.csv"), dtype=str)
    say("V the CSV carries the 14 whole tons and the Y/N", all(int(t) == f["plants"][p_]["press_voc_tons"] and
                                                               (y == "Y") == f["plants"][p_]["covered"] for p_, t, y in
                                                               zip(gc["plant"], gc["press_voc_2026_tons"],
                                                                   gc["rule_18_4_from_2027_07_01"])))
    svg = open(os.path.join(G, "deq_printing_press_voc_2026.svg"), encoding="utf-8").read()
    say("V the chart labels every bar with its whole tons and draws the 25-ton line",
        all(">%d<" % f["plants"][p_]["press_voc_tons"] in svg for p_ in f["plants"]) and "25 tons" in svg)
    print("%s  verify: %d failed" % ("PASS" if not FAIL else "FAIL", len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
