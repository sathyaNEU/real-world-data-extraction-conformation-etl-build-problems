"""Independent verifier for task465: reads only the shipped folder and the goldens, on its own code path (pandas, pypdf,
zoneinfo), and recomputes the withheld county-years from the district totals, each cover's expected loss, multiple, rate
at which its call changes and call, each cover's 2027 liability and premium, each county's 2016 to 2020 receipts share
and the conformed record, against generator/figures.json, the golden workbook and the golden record. Imports nothing
from the generator.

    python3 task465/generator/verify.py
"""
import json
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
COVERS = ["Ardley", "Corvin", "Elster", "Pallard", "Tresham"]
NI = "SORGHUM, GRAIN, NON-IRRIGATED - "
ALL = "SORGHUM, GRAIN - "
FIELD = {"ACRES HARVESTED": "harvested", "PRODUCTION, MEASURED IN BU": "production", "YIELD, MEASURED IN BU / ACRE": "yield"}


def find(target, stem):
    hit = [f for f in os.listdir(target) if f.startswith(stem)]
    assert len(hit) == 1, (stem, hit)
    return os.path.join(target, hit[0])


def half_up(x, nd):
    return math.floor(x * 10 ** nd + 0.5) / 10 ** nd


def estimates(target, prefix):
    """County and district rows of one sorghum practice, the October 2026 download taking every year it holds."""
    frames = []
    for vint, stem in ((0, "clrs_county_estimates_pull_2024"), (1, "clrs_county_estimates_pull_2026")):
        d = pd.read_csv(find(target, stem), dtype=str, keep_default_na=False)
        d = d[d["Data Item"].str.startswith(prefix) & d["Geo Level"].isin(["COUNTY", "AGRICULTURAL DISTRICT"])].copy()
        d = d[d["Data Item"].str[len(prefix):].isin(FIELD)]
        d["vint"] = vint
        frames.append(d)
    x = pd.concat(frames)
    x["field"] = x["Data Item"].str[len(prefix):].map(FIELD)
    x["year"] = x["Year"].astype(int)
    code = x["Ag District Code"].astype(int)
    x["district"] = code.where(code >= 10, code * 10)
    x["county"] = x["County"].str.title()
    x["value"] = pd.to_numeric(x["Value"].str.replace(",", ""), errors="coerce")
    x = x.sort_values("vint").drop_duplicates(["Geo Level", "district", "county", "year", "field"], keep="last")
    cty = x[x["Geo Level"] == "COUNTY"].pivot_table(index=["county", "year"], columns="field", values="value",
                                                    aggfunc="first", dropna=False)
    dist = x[x["Geo Level"] == "AGRICULTURAL DISTRICT"].pivot_table(index=["district", "year"], columns="field",
                                                                     values="value", aggfunc="first")
    home = x[x["Geo Level"] == "COUNTY"].groupby("county")["district"].agg(lambda s: sorted(set(s)))
    return cty, dist, home


def conformed(target):
    """Each cover county's yield 1991 to 2025: published, or recovered as the district less its other counties."""
    cty, dist, home = estimates(target, NI)
    assert all(len(v) == 1 for v in home), "a county in two districts"
    home = {c: v[0] for c, v in home.items()}
    rows = []
    for c in COVERS:
        d = home[c]
        others = [k for k, v in home.items() if v == d and k != c]
        for y in range(1991, 2026):
            r = cty.loc[(c, y)]
            if not math.isnan(r["yield"]):
                rows.append(dict(county=c, year=y, harvested=r["harvested"], production=r["production"],
                                 yld=r["yield"], recovered=False))
                continue
            o = cty.loc[[(k, y) for k in others]]
            assert o["harvested"].notna().all() and o["production"].notna().all(), (c, y)
            h = dist.loc[(d, y), "harvested"] - o["harvested"].sum()
            p = dist.loc[(d, y), "production"] - o["production"].sum()
            rows.append(dict(county=c, year=y, harvested=h, production=p, yld=half_up(p / h, 1), recovered=True))
    return pd.DataFrame(rows), home


def term_sheet(target):
    import pypdf
    txt = " ".join(p.extract_text() for p in pypdf.PdfReader(find(target, "quillfield_re_area_yield_term_sheet")).pages)
    txt = re.sub(r"\s+", " ", txt)
    table = {}
    for c in COVERS:
        m = re.search(r"%s (\d+\.\d) (\d+\.\d+)" % c, txt)
        table[c] = (float(m.group(1)), float(m.group(2)))
    trig = float(re.search(r"Trigger (\d+) per cent of the expected yield", txt).group(1)) / 100
    cwt = float(re.search(r"\$(\d+\.\d\d) per hundredweight", txt).group(1))
    lb = float(re.search(r"weighs (\d+) pounds", txt).group(1))
    return table, trig, cwt * lb / 100


def quoted(target):
    q = pd.read_excel(find(target, "quillfield_re_quote_schedule"), sheet_name="Dryland grain sorghum", header=3)
    q = q[q["County"].isin(COVERS)]
    return dict(zip(q["County"], 100 * q["Quoted premium rate (per cent of liability)"].astype(float)))


def losses(rec, table, trig):
    el = {}
    for c in COVERS:
        e, b = table[c]
        t = trig * e
        s = rec[rec["county"] == c]
        level = s["yld"] + b * (2027 - s["year"])
        el[c] = 100 * ((t - level) / t).clip(0, 1).mean()
    return el


def acres_enrolled(target):
    e = pd.read_csv(find(target, "apgc_cover_enrolment_2027"), dtype={"acres": float})
    e["t"] = pd.to_datetime(e["submitted_at"], utc=True)
    close = pd.Timestamp("2026-10-30 17:00").tz_localize(ZoneInfo("America/Chicago"))
    e = e[e["t"] < close].sort_values("t").groupby("field_id").tail(1)
    e = e[(e["crop"] == "Grain sorghum") & (e["practice"] == "Non-irrigated")]
    return e.groupby("field_county")["acres"].sum().reindex(COVERS).fillna(0).to_dict()


def receipts(target):
    t = pd.read_csv(find(target, "apgc_scale_tickets"), dtype={"reference": str})
    tr = set(pd.read_csv(find(target, "apgc_site_transfers"), dtype={"transfer_no": str})["transfer_no"])
    t = t[(t["commodity"] == "Sorghum") & ~((t["site"] == "MAIN") & t["reference"].isin(tr))]
    t["bu"] = t["net_lb"] * (100 - t["moisture_pct"]) / 86 / 56
    bu = t.groupby("origin_county")["bu"].sum()
    cty, _, _ = estimates(target, ALL)
    prod = {c: sum(cty.loc[(c, y), "production"] for y in range(2016, 2021)) for c in COVERS}
    return {c: float(bu[c]) for c in COVERS}, prod


def main(target, golden, fig_path=None):
    F = json.load(open(fig_path or os.path.join(HERE, "figures.json")))
    bad = []

    def check(label, cond, detail=""):
        print("%s  verify: %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))
        if not cond:
            bad.append(label)

    rec, home = conformed(target)
    got = {"%s %d" % (r.county, r.year): (int(r.harvested), int(r.production), r.yld) for r in rec.itertuples()
           if r.recovered}
    want = {k: (v["harvested"], v["production"], v["yld"]) for k, v in F["recovered"].items()}
    check("the ten withheld county-years recovered from the district totals", got == want and len(got) == 10, got)
    table, trig, price = term_sheet(target)
    q = quoted(target)
    el = losses(rec, table, trig)
    buy = [c for c in COVERS if q[c] <= 1.4 * el[c]]
    check("each cover's expected loss, two decimals of a per cent", all(
        half_up(el[c], 2) == F["covers"][c]["expected_loss"] for c in COVERS), {c: round(el[c], 4) for c in COVERS})
    check("each cover's quoted rate as a multiple of its expected loss", all(
        half_up(q[c] / el[c], 2) == F["covers"][c]["multiple"] for c in COVERS))
    check("each cover's rate at which the call changes", all(
        half_up(1.4 * el[c], 2) == F["covers"][c]["change_rate"] for c in COVERS))
    check("the call: buy %s" % ", ".join(buy), buy == F["call"]["buy"])
    pub = rec[~rec["recovered"]]
    el0 = losses(pub, table, trig)
    check("the published years alone buy none of the five covers", [c for c in COVERS if q[c] <= 1.4 * el0[c]] == [])
    acres = acres_enrolled(target)
    lia = {c: acres[c] * table[c][0] * trig * price for c in COVERS}
    prem = {c: lia[c] * q[c] / 100 for c in COVERS}
    check("each cover's 2027 liability, nearest hundred dollars", all(
        half_up(lia[c], -2) == F["liability"][c] for c in COVERS), {c: round(lia[c], 2) for c in COVERS})
    check("each cover's 2027 premium, nearest hundred dollars", all(
        half_up(prem[c], -2) == F["premium"][c] for c in COVERS), {c: round(prem[c], 2) for c in COVERS})
    bu, prod = receipts(target)
    share = {c: 100 * bu[c] / prod[c] for c in COVERS}
    check("each county's 2016 to 2020 receipts share, one decimal of a per cent", all(
        half_up(share[c], 1) == F["receipts_share"][c] for c in COVERS), {c: round(share[c], 3) for c in COVERS})

    import csv
    with open(os.path.join(golden, "conformed_county_dryland_sorghum_yields.csv"), encoding="utf-8") as fh:
        g = list(csv.DictReader(fh))
    ok = len(g) == len(rec) == 175
    for r, s in zip(g, rec.itertuples()):
        ok &= (r["county"], int(r["crop_year"])) == (s.county, s.year) and int(r["harvested_acres"]) == int(s.harvested) \
            and int(r["production_bu"]) == int(s.production) and float(r["yield_bu_per_acre"]) == s.yld \
            and int(r["ag_district_code"]) == home[s.county] and r["source"].lower().startswith("recovered") == s.recovered
    check("the golden record: 175 county-years as conformed", ok)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden, "county_area_yield_quotes_2027.xlsx"))
    ws = wb["Covers"]
    rows = {ws.cell(row=i, column=1).value: [ws.cell(row=i, column=j).value for j in range(2, 9)] for i in range(5, 10)}
    check("the golden workbook's Covers sheet", all(
        abs(rows[c][2] * 100 - half_up(el[c], 2)) < 1e-9 and abs(rows[c][3] * 100 - q[c]) < 1e-9
        and abs(rows[c][4] - half_up(q[c] / el[c], 2)) < 1e-9 and abs(rows[c][5] * 100 - half_up(1.4 * el[c], 2)) < 1e-9
        and rows[c][6] == ("Buy" if c in buy else "Decline") for c in COVERS))
    ws = wb["Liability and premium"]
    rows = {ws.cell(row=i, column=1).value: [ws.cell(row=i, column=j).value for j in range(2, 9)] for i in range(5, 10)}
    check("the golden workbook's liability and premium sheet", all(
        rows[c][4] == half_up(lia[c], -2) and rows[c][6] == half_up(prem[c], -2) for c in COVERS))
    ws = wb["Receipts 2016-2020"]
    rows = {ws.cell(row=i, column=1).value: [ws.cell(row=i, column=j).value for j in range(2, 5)] for i in range(5, 10)}
    check("the golden workbook's receipts sheet", all(abs(rows[c][2] * 100 - half_up(share[c], 1)) < 1e-9
                                                      and rows[c][1] == prod[c] for c in COVERS))
    if bad:
        raise SystemExit("verify failed: %s" % bad)
    return el


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
