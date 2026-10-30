"""Assemble task503_ext/target: US land-border crossings by port, with the national series,
the regulatory record and the northbound mirror beside them.

Sources, all downloaded on the pull date:
  - BTS Border Crossing Entry Data (data.bts.gov keg4-3bc2), the full export and its metadata
  - BTS Monthly Transportation Statistics (data.bts.gov crem-w557), the full export
  - Federal Register: every DHS notice restricting travel at land ports of entry, 2020 to 2023,
    as an API index, plus five of the notices as published (govinfo PDFs)
  - Statistics Canada table 24-10-0002-01, vehicles travelling between Canada and the United
    States, filtered to trucks from January 1996, with the table's own metadata file

Nothing is edited. The one table cut down is the Statistics Canada file (rows only, each kept
byte for byte). The checks at the end confirm the spine is complete against the live API count,
reconciles to the national series where the two measure the same thing, and that the
regulatory index and the Canadian table are internally consistent.

Run: python3 task503_ext/generator/build_pack.py
"""
import csv
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import zipfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(ROOT, "target")
UA = {"User-Agent": "Mozilla/5.0"}
PULL_DATE = (2026, 10, 13, 9, 0, 0)

BTS = "https://data.bts.gov/"
SPINE = "Border_Crossing_Entry_Data.csv"
SPINE_META = "Border_Crossing_Entry_Data_metadata.json"
MTS = "Monthly_Transportation_Statistics.csv"
FR_INDEX = "federal_register_land_port_restrictions_2020-2023.json"
STATCAN_ZIP = "https://www150.statcan.gc.ca/n1/tbl/csv/24100002-eng.zip"
STATCAN = "24100002_trucks_1996-2021.csv"
STATCAN_META = "24100002_MetaData.csv"

FR_QUERY = {
    "conditions[term]": '"land ports of entry" "non-essential travel"',
    "conditions[agencies][]": "homeland-security-department",
    "per_page": "100",
    "order": "oldest",
}
FR_FIELDS = ["document_number", "citation", "publication_date", "effective_on", "dates", "type",
             "title", "abstract", "agencies", "html_url", "pdf_url"]
# Canada and Mexico restrictions as first imposed, the Canada notices that lifted them for
# vaccinated travellers, required vaccination of essential travellers (truck drivers included)
# and ended them.
FR_PDFS = ["2020-06217", "2020-06253", "2021-28063", "2022-01402", "2023-09948"]

SPINE_COLUMNS = ["Port Name", "State", "Port Code", "Border", "Date", "Measure", "Value",
                 "Latitude", "Longitude", "Point"]
MEASURES = {"Bus Passengers", "Buses", "Pedestrians", "Personal Vehicle Passengers",
            "Personal Vehicles", "Train Passengers", "Trains", "Trucks"}
PROVINCES = ["Nova Scotia", "New Brunswick", "Quebec", "Ontario", "Manitoba", "Saskatchewan",
             "Alberta", "British Columbia", "Yukon"]


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
        return r.read()


def write_bytes(name, data):
    with open(os.path.join(TARGET, name), "wb") as f:
        f.write(data)


def main():
    os.makedirs(TARGET, exist_ok=True)
    for name in os.listdir(TARGET):
        os.remove(os.path.join(TARGET, name))

    write_bytes(SPINE, fetch(BTS + "api/views/keg4-3bc2/rows.csv?accessType=DOWNLOAD"))
    meta = json.loads(fetch(BTS + "api/views/keg4-3bc2.json"))
    write_bytes(SPINE_META, json.dumps(meta, indent=2, ensure_ascii=False).encode() + b"\n")
    write_bytes(MTS, fetch(BTS + "api/views/crem-w557/rows.csv?accessType=DOWNLOAD"))

    query = urllib.parse.urlencode(FR_QUERY) + "".join(
        "&" + urllib.parse.urlencode({"fields[]": f}) for f in FR_FIELDS)
    fr = json.loads(fetch("https://www.federalregister.gov/api/v1/documents.json?" + query))
    write_bytes(FR_INDEX, json.dumps(fr, indent=2, ensure_ascii=False).encode() + b"\n")
    pdf_url = {r["document_number"]: r["pdf_url"] for r in fr["results"]}
    for doc in FR_PDFS:
        write_bytes(f"{doc}.pdf", fetch(pdf_url[doc]))

    # Statistics Canada: trucks only, January 1996 on, every kept line exactly as served.
    z = zipfile.ZipFile(io.BytesIO(fetch(STATCAN_ZIP)))
    write_bytes(STATCAN_META, z.read("24100002_MetaData.csv"))
    lines = z.read("24100002.csv").decode("utf-8-sig").splitlines(keepends=True)
    head = next(csv.reader([lines[0]]))
    i_date, i_mode = head.index("REF_DATE"), head.index("Mode of transportation")
    kept = [l for l in lines[1:]
            if (row := next(csv.reader([l])))[i_mode] == "Trucks" and row[i_date] >= "1996-01"]
    write_bytes(STATCAN, ("﻿" + lines[0] + "".join(kept)).encode("utf-8"))

    with open(os.path.join(HERE, "provenance.md"), "rb") as f:
        write_bytes("provenance.md", f.read())

    live_rows = int(json.loads(fetch(BTS + "resource/keg4-3bc2.json?$select=count(*)"))[0]["count"])
    verify(live_rows)
    stamp_and_zip()


def verify(live_rows=None):
    t = lambda n: os.path.join(TARGET, n)
    d = pd.read_csv(t(SPINE))
    d["month"] = pd.to_datetime(d["Date"], format="%b %Y")
    m = pd.read_csv(t(MTS))
    m = pd.concat([m, pd.to_datetime(m["Date"], format="%m/%d/%Y %I:%M:%S %p").rename("month")], axis=1)
    fr = json.load(open(t(FR_INDEX)))["results"]
    sc = pd.read_csv(t(STATCAN), dtype=str, encoding="utf-8-sig")
    sc["v"] = pd.to_numeric(sc["VALUE"])
    sc_meta = open(t(STATCAN_META), encoding="utf-8-sig").read()

    months = d.groupby("Border")["month"].nunique()
    span = d["month"].max().to_period("M") - d["month"].min().to_period("M")
    v = d["Value"].dropna()

    # Where the national series and the spine measure the same thing they should agree: trucks
    # summed over every port on a border, and pedestrians, which is what the national series
    # labelled "Incoming Person Crossings" tracks.
    mts = m.drop_duplicates("month").set_index("month")
    recon = {}
    for border, label in (("US-Canada Border", "U.S.-Canada"), ("US-Mexico Border", "U.S.-Mexico")):
        for measure, col in (("Trucks", "Truck"), ("Pedestrians", "Person")):
            ours = d[(d["Border"] == border) & (d["Measure"] == measure)].groupby("month")["Value"].sum()
            pair = pd.concat([mts[f"{label} Incoming {col} Crossings"].dropna().rename("mts"),
                              ours.rename("spine")], axis=1, join="inner")
            gap = (pair["mts"] - pair["spine"]).abs()
            recon[(label, measure)] = (len(pair), int((gap == 0).sum()), (gap / pair["spine"]).max())

    dup = m[m["month"].duplicated(keep=False)]
    dup_cols = [c for c in m.columns if dup[c].nunique(dropna=False) > 1]

    sct = sc[sc["Mode of transportation"] == "Trucks"]
    prov = sct[sct["GEO"].isin(PROVINCES)].groupby(["REF_DATE", "Trip characteristics"])["v"].sum()
    nat = sct[sct["GEO"] == "Canada"].set_index(["REF_DATE", "Trip characteristics"])["v"]

    checks = [
        ("spine over 10,000 rows", len(d) > 10_000),
        ("spine has the published columns", list(d.columns[:-1]) == SPINE_COLUMNS),
        ("one row per port, measure and month", not d.duplicated(["Port Code", "Measure", "Date"]).any()),
        ("measures are the eight published", set(d["Measure"]) == MEASURES),
        ("two borders, every month present on both, January 1996 on",
         set(d["Border"]) == {"US-Canada Border", "US-Mexico Border"}
         and str(d["month"].min().date()) == "1996-01-01" and (months == span.n + 1).all()),
        ("each port code carries one port name", (d.groupby("Port Code")["Port Name"].nunique() == 1).all()),
        ("values are non-negative whole numbers", (v >= 0).all() and (v % 1 == 0).all()),
        ("national series has every month the spine has",
         set(d["month"]) <= set(mts.index)),
        ("only April 2023 is doubled in the national series, differing only in highway fatalities",
         set(dup["month"].dt.strftime("%Y-%m")) <= {"2023-04"} and set(dup_cols) <= {"Highway Fatalities", "Index"}),
    ]
    if live_rows is not None:
        checks.insert(0, (f"spine row count matches the live API ({live_rows:,})", len(d) == live_rows))
    for (label, measure), (n, exact, worst) in recon.items():
        floor = 0.9 if measure == "Trucks" else 0.8
        checks.append((f"{label} {measure.lower()} match the national series exactly in at least "
                       f"{floor:.0%} of months ({exact} of {n}, worst gap {worst:.2%})", exact / n >= floor))
    checks += [
        ("Federal Register index holds the 48 notices, 24 per border",
         len(fr) == 48 and sum("Canada" in r["title"] for r in fr) == 24
         and sum("Mexico" in r["title"] for r in fr) == 24),
        ("every notice is a CBP rule", all(r["type"] == "Rule" and any(
            a["name"] == "U.S. Customs and Border Protection" for a in r["agencies"]) for r in fr)),
        ("every shipped notice PDF is in the index and is a PDF",
         all(doc in {r["document_number"] for r in fr}
             and open(t(f"{doc}.pdf"), "rb").read(5) == b"%PDF-" for doc in FR_PDFS)),
        ("Statistics Canada extract is trucks, January 1996 to December 2021",
         set(sc["Mode of transportation"]) == {"Trucks"}
         and sc["REF_DATE"].min() == "1996-01" and sc["REF_DATE"].max() == "2021-12"),
        ("Statistics Canada national rows equal the sum of the provinces",
         (pd.concat([nat, prov], axis=1).dropna().nunique(axis=1) == 1).all() and len(nat) == len(prov)),
        ("blank Statistics Canada values are exactly the suppressed (x) cells",
         (sc["v"].isna() == (sc["STATUS"] == "x")).all()),
        ("Statistics Canada metadata marks the table archived", "ARCHIVED" in sc_meta),
    ]

    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    formats = sorted({f.rsplit(".", 1)[1] for f in files})
    checks += [("10 or more files", len(files) >= 10), ("3 or more formats", len(formats) >= 3)]

    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    print(f"{len(files)} files, formats {formats}")
    print(f"spine {len(d):,} rows, {d['Port Code'].nunique()} ports, "
          f"{d['month'].min():%b %Y} to {d['month'].max():%b %Y}, {d['Value'].isna().sum()} blank values; "
          f"national series {len(m):,} rows; Statistics Canada {len(sc):,} rows, "
          f"{sc['GEO'].nunique()} geographies, {int(sc['v'].isna().sum())} suppressed")
    if not all(ok for _, ok in checks):
        sys.exit(1)


def stamp_and_zip():
    """One pull date on every file, then a flat target.zip beside target/."""
    ts = time.mktime(PULL_DATE + (0, 0, -1))
    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    for f in files:
        os.utime(os.path.join(TARGET, f), (ts, ts))
    with zipfile.ZipFile(os.path.join(ROOT, "target.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info = zipfile.ZipInfo(f, date_time=PULL_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, f), "rb") as src:
                z.writestr(info, src.read())


if __name__ == "__main__":
    main()
