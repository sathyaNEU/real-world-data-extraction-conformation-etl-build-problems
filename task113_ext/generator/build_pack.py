"""Assemble task113/target from New York Fed and US Treasury public sources.

US dollar money-market reference rates, the Treasury par yield curve, Treasury auction results
and Fed reverse repo operations, with the publishers' own methodology documents. Every value is
as published; the only derived file is the yield curve, which is Treasury's per-year CSVs stacked
into one table. Ends by checking the pack.

Run: python3 task113/generator/build_pack.py
"""
import csv
import io
import json
import os
import sys
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
UA = {"User-Agent": "Mozilla/5.0"}

START, END = "2000-01-01", "2026-10-06"
YC_YEARS = range(1990, 2027)

NYF_API = "https://markets.newyorkfed.org/api/"
FISCAL = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
          "v1/accounting/od/auctions_query")
YC = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
      "daily-treasury-rates.csv/{y}/all?type=daily_treasury_yield_curve"
      "&field_tdr_date_value={y}&page&_format=csv")

FILES = {
    "nyfed_reference_rates_20000703_20261006.csv":
        NYF_API + f"rates/all/search.csv?startDate={START}&endDate={END}",
    "nyfed_reverse_repo_operations_20130402_20261006.csv":
        NYF_API + f"rp/reverserepo/propositions/search.csv?startDate=2013-01-01&endDate={END}",
    "IOSCO-statement-of-compliance-jul2025.pdf":
        "https://www.newyorkfed.org/medialibrary/media/markets/IOSCO-statement-of-compliance-jul2025",
    "nyfed_additional_information_about_reference_rates.html":
        "https://www.newyorkfed.org/markets/reference-rates/additional-information-about-reference-rates",
    "treasury_yield_curve_methodology.html":
        "https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/"
        "treasury-yield-curve-methodology",
    "treasury_yield_curve_methodology_change_information_sheet.html":
        "https://home.treasury.gov/policy-issues/financing-the-government/"
        "yield-curve-methodology-change-information-sheet",
}
YC_FILE = "treasury_daily_par_yield_curve_1990_2026.csv"
AUC_FILE = "treasury_auctions_query_pulled_20261007.csv"
AUC_DICT = "treasury_auctions_query_dictionary.json"


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def save(name, data):
    with open(os.path.join(TARGET, name), "wb") as f:
        f.write(data)


def main():
    os.makedirs(TARGET, exist_ok=True)
    for name, url in FILES.items():
        save(name, fetch(url))

    # Yield curve: one Treasury CSV per year, stacked oldest first. Columns are the union in
    # Treasury's current order; a tenor Treasury did not publish that year stays blank.
    frames = []
    for y in YC_YEARS:
        frames.append(pd.read_csv(io.BytesIO(fetch(YC.format(y=y))), dtype=str))
    cols = list(frames[-1].columns)
    for f in frames:
        cols += [c for c in f.columns if c not in cols]
    yc = pd.concat(frames, ignore_index=True)[cols]
    yc["_d"] = pd.to_datetime(yc["Date"], format="%m/%d/%Y")
    yc.sort_values("_d").drop(columns="_d").to_csv(
        os.path.join(TARGET, YC_FILE), index=False, quoting=csv.QUOTE_MINIMAL)

    # Auctions: Fiscal Data caps a page at 10,000 rows. The dictionary is the API's own metadata.
    meta, rows = None, []
    page = 1
    while True:
        js = json.loads(fetch(f"{FISCAL}?page[number]={page}&page[size]=10000"))
        meta = js["meta"]
        rows += js["data"]
        if page >= meta["total-pages"]:
            break
        page += 1
    with open(os.path.join(TARGET, AUC_FILE), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(meta["labels"]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(TARGET, AUC_DICT), "w") as f:
        json.dump({"source": FISCAL, "total-count": meta["total-count"],
                   "labels": meta["labels"], "dataTypes": meta["dataTypes"],
                   "dataFormats": meta["dataFormats"]}, f, indent=2)

    verify()


def verify():
    t = lambda n: os.path.join(TARGET, n)
    rr = pd.read_csv(t("nyfed_reference_rates_20000703_20261006.csv"), dtype=str)
    rr["d"] = pd.to_datetime(rr["Effective Date"], format="%m/%d/%Y")
    rrp = pd.read_csv(t("nyfed_reverse_repo_operations_20130402_20261006.csv"), dtype=str)
    yc = pd.read_csv(t(YC_FILE), dtype=str)
    yc["d"] = pd.to_datetime(yc["Date"], format="%m/%d/%Y")
    auc = pd.read_csv(t(AUC_FILE), dtype=str, keep_default_na=False)
    dic = json.load(open(t(AUC_DICT)))
    first = rr.groupby("Rate Type")["d"].min()

    def blank_years(col):
        return sorted(yc.loc[yc[col].isna(), "d"].dt.year.unique())

    checks = [
        ("reference rates over 10,000 rows", len(rr) > 10_000),
        ("reference rates keyed by date and rate type", not rr.duplicated(["d", "Rate Type"]).any()),
        ("repo rates start 2018-04-02",
         all(first[k] == pd.Timestamp("2018-04-02") for k in ("SOFR", "BGCR", "TGCR"))),
        ("EFFR starts 2000-07-03", first["EFFR"] == pd.Timestamp("2000-07-03")),
        ("footnote ids are 1 and 2 only", set(rr["Footnote ID"].dropna()) <= {"1", "2"}),
        ("reverse repo operation ids unique", rrp["Operation Id"].is_unique),
        ("yield curve dates unique", yc["d"].is_unique),
        ("yield curve covers every year 1990-2026", set(yc["d"].dt.year) == set(YC_YEARS)),
        ("30 Yr blank across its 2002-2005 suspension", {2003, 2004, 2005} <= set(blank_years("30 Yr"))),
        ("1 Mo blank before 2001", set(range(1990, 2001)) <= set(blank_years("1 Mo"))),
        ("4 Mo blank before 2022", 2021 in blank_years("4 Mo")),
        ("auction rows equal Fiscal Data total-count", len(auc) == int(dic["total-count"])),
        ("auction columns equal dictionary labels", list(auc.columns) == list(dic["labels"])),
        ("pdf is a pdf", open(t("IOSCO-statement-of-compliance-jul2025.pdf"), "rb").read(5) == b"%PDF-"),
        ("no observation after the 2026-10-07 download",
         max(rr["d"].max(), yc["d"].max(),
             pd.to_datetime(rrp["Operation Date"], format="%m/%d/%Y").max()) < pd.Timestamp("2026-10-07")),
        ("auctions from the download date on are announcements with no results",
         auc.loc[pd.to_datetime(auc["auction_date"]) >= "2026-10-07", "total_accepted"]
            .isin(["null"]).all()),
    ]
    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    checks += [("10 or more files", len(files) >= 10),
               ("3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    print(f"{len(files)} files, formats {sorted({f.rsplit('.', 1)[1] for f in files})}")
    print(f"rates {len(rr):,}  yield curve {len(yc):,}  auctions {len(auc):,}  rrp {len(rrp):,}")
    if not all(ok for _, ok in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
