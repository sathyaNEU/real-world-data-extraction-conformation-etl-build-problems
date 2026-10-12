"""Assemble task112/target from Census Bureau public files (2023 ACS 1-year PUMS, Oregon).

Downloads every source, extracts or filters it, derives the one lookup table, and checks
that the pack reproduces the Census Bureau's own PUMS verification estimates. Nothing in
the spine is edited: column names, codes, blanks and weights are as published.

Run: python3 task112/generator/build_pack.py
"""
import csv
import io
import os
import sys
import urllib.request
import zipfile
from collections import defaultdict

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
UA = {"User-Agent": "Mozilla/5.0"}

PUMS = "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/"
DOCS = "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/"
GEO = "https://www2.census.gov/geo/docs/"

SRC = {
    "person_zip": PUMS + "csv_por.zip",
    "housing_zip": PUMS + "csv_hor.zip",
    "dictionary": DOCS + "data_dict/PUMS_Data_Dictionary_2023.csv",
    "accuracy": DOCS + "accuracy/2023AccuracyPUMS.pdf",
    "estimates": DOCS + "estimates/pums_estimates_23.csv",
    "tract_puma": GEO + "maps-data/data/rel2020/2020_Census_Tract_to_2020_PUMA.txt",
    "counties": GEO + "reference/codes2020/national_county2020.txt",
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        return r.read()


def write_bytes(name, data):
    with open(os.path.join(TARGET, name), "wb") as f:
        f.write(data)


def main():
    os.makedirs(TARGET, exist_ok=True)

    # Spine: person and housing records, extracted unchanged with the publisher's README.
    for key, member in (("person_zip", "psam_p41.csv"), ("housing_zip", "psam_h41.csv")):
        z = zipfile.ZipFile(io.BytesIO(fetch(SRC[key])))
        write_bytes(member, z.read(member))
        if key == "person_zip":
            write_bytes("ACS2023_PUMS_README.pdf", z.read("ACS2023_PUMS_README.pdf"))

    write_bytes("PUMS_Data_Dictionary_2023.csv", fetch(SRC["dictionary"]))
    write_bytes("2023AccuracyPUMS.pdf", fetch(SRC["accuracy"]))

    # National files filtered to Oregon (state FIPS 41), header kept, rows otherwise untouched.
    est = fetch(SRC["estimates"]).decode("utf-8-sig").splitlines()
    write_bytes("pums_estimates_23_oregon.csv",
                ("\n".join([est[0]] + [l for l in est[1:] if l.startswith("41,")]) + "\n").encode())

    tract = fetch(SRC["tract_puma"]).decode("utf-8-sig").splitlines()
    write_bytes("2020_Census_Tract_to_2020_PUMA_oregon.txt",
                ("\n".join([tract[0]] + [l for l in tract[1:] if l.startswith("41,")]) + "\n").encode())

    cty = fetch(SRC["counties"]).decode("utf-8-sig").splitlines()
    write_bytes("national_county2020_oregon.txt",
                ("\n".join([cty[0]] + [l for l in cty[1:] if l.startswith("OR|")]) + "\n").encode())

    # Derived: one row per PUMA x county, with tract counts, from the two geography files.
    names = {}
    for row in csv.DictReader(io.StringIO("\n".join(cty)), delimiter="|"):
        if row["STATEFP"] == "41":
            names[row["COUNTYFP"]] = row["COUNTYNAME"]
    tracts = defaultdict(int)
    for row in csv.DictReader(io.StringIO("\n".join(tract))):
        if row["STATEFP"] == "41":
            tracts[(row["PUMA5CE"], row["COUNTYFP"])] += 1
    puma_total = defaultdict(int)
    for (p, _), n in tracts.items():
        puma_total[p] += n
    with open(os.path.join(TARGET, "puma_county_lookup.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["STATEFP", "PUMA", "COUNTYFP", "COUNTYNAME", "tracts_in_puma_county",
                    "tracts_in_puma", "share_of_puma_tracts"])
        for (p, c) in sorted(tracts):
            n = tracts[(p, c)]
            w.writerow(["41", p, c, names[c], n, puma_total[p], f"{n / puma_total[p]:.4f}"])

    verify()


def verify():
    p = pd.read_csv(os.path.join(TARGET, "psam_p41.csv"), dtype={"SERIALNO": str, "PUMA": str})
    h = pd.read_csv(os.path.join(TARGET, "psam_h41.csv"), dtype={"SERIALNO": str, "PUMA": str})
    est = pd.read_csv(os.path.join(TARGET, "pums_estimates_23_oregon.csv"))
    lk = pd.read_csv(os.path.join(TARGET, "puma_county_lookup.csv"), dtype=str)
    ev = dict(zip(est["CHARACTERISTIC"], est["PUMS_EST_23"]))
    se = dict(zip(est["CHARACTERISTIC"], est["PUMS_SE_23"]))
    rep = [f"PWGTP{i}" for i in range(1, 81)]

    def rse(df):
        full = df["PWGTP"].sum()
        return (4 / 80 * ((df[rep].sum() - full) ** 2).sum()) ** 0.5

    checks = [
        ("person rows over 10,000", len(p) > 10_000),
        ("person keys unique", not p.duplicated(["SERIALNO", "SPORDER"]).any()),
        ("housing keys unique", h["SERIALNO"].is_unique),
        ("every person joins to a housing record", p["SERIALNO"].isin(h["SERIALNO"]).all()),
        ("all records are Oregon", (p["STATE"] == 41).all() and (h["STATE"] == 41).all()),
        ("every PUMA in the spine is in the lookup", set(p["PUMA"]) <= set(lk["PUMA"])),
        ("total population reproduces", p["PWGTP"].sum() == ev["Total population"]),
        ("males reproduce", p.loc[p.SEX == 1, "PWGTP"].sum() == ev["Total males (SEX=1)"]),
        ("males SE reproduces", round(rse(p[p.SEX == 1])) == se["Total males (SEX=1)"]),
        ("age 25-34 reproduces",
         p.loc[p.AGEP.between(25, 34), "PWGTP"].sum() == ev["Age 25-34"]),
        ("age 25-34 SE reproduces", round(rse(p[p.AGEP.between(25, 34)])) == se["Age 25-34"]),
        ("occupied units reproduce",
         h.loc[h.TEN.notna() & (h.TYPEHUGQ == 1), "WGTP"].sum() == ev["Total occupied units"]),
    ]
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    print(f"{len(files)} files, formats {sorted({f.rsplit('.', 1)[1] for f in files})}")
    print(f"person rows {len(p):,}, housing rows {len(h):,}")
    if not all(ok for _, ok in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
