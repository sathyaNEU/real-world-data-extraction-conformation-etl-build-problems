"""Assemble task502_ext/target from the Project STAR deposit on Harvard Dataverse.

Source: C.M. Achilles et al., 2008, "Tennessee's Student Teacher Achievement Ratio (STAR)
project", Harvard Dataverse, V1, doi:10.7910/DVN/SIWH9F, released under CC0 1.0.

Downloads the four student and school tables as Dataverse serves them (tab-delimited, codes
as stored), the variable-level DDI codebook for each table (it carries the value labels the
tab export drops), the HEROS user's guide and reports, the overview page and the dataset's
own metadata record. Nothing is edited. The checks at the end confirm every downloaded
document matches the MD5 Dataverse publishes, every value-label frequency in the DDI
reproduces from the tables, and the counts the user's guide states reproduce as well.

Run: python3 task502_ext/generator/build_pack.py
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import zipfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(ROOT, "target")
UA = {"User-Agent": "Mozilla/5.0"}

DV = "https://dataverse.harvard.edu/api/"
DOI = "doi:10.7910/DVN/SIWH9F"
PULL_DATE = (2026, 10, 13, 9, 0, 0)

# Dataverse file id -> name in the pack. Tables keep the name Dataverse lists them under.
TABLES = {
    666716: "STAR_Students.tab",
    666717: "STAR_K-3_Schools.tab",
    666718: "STAR_High_Schools.tab",
    666719: "Comparison_Students.tab",
}
DOCS = {
    666705: "starUsersGuide.pdf",
    666702: "Project STAR K-3 summary report.pdf",
    666715: "STAR follow-up Studies (1996-1997) Report newstar.pdf",
    666704: "star-college.pdf",
    666710: "Overview of Public Data Files.htm",
}
METADATA = "dataverse_SIWH9F_dataset_metadata.json"


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
        return r.read()


def write_bytes(name, data):
    with open(os.path.join(TARGET, name), "wb") as f:
        f.write(data)


def ddi_name(table):
    return table.replace(".tab", "-ddi.xml")


def main():
    os.makedirs(TARGET, exist_ok=True)
    for name in os.listdir(TARGET):
        os.remove(os.path.join(TARGET, name))

    for fid, name in TABLES.items():
        write_bytes(name, fetch(f"{DV}access/datafile/{fid}"))
        write_bytes(ddi_name(name), fetch(f"{DV}access/datafile/{fid}/metadata/ddi"))
    for fid, name in DOCS.items():
        write_bytes(name, fetch(f"{DV}access/datafile/{fid}"))
    meta = fetch(f"{DV}datasets/export?exporter=dataverse_json&persistentId={DOI}")
    write_bytes(METADATA, json.dumps(json.loads(meta), indent=2, ensure_ascii=False).encode() + b"\n")

    with open(os.path.join(HERE, "provenance.md"), "rb") as f:
        write_bytes("provenance.md", f.read())

    verify()
    stamp_and_zip()


def ddi_vars(path):
    """(name, label, [(code, freq), ...]) for every variable in a Dataverse DDI file."""
    text = open(path, encoding="utf-8").read()
    out = []
    for name, body in re.findall(r'<var ID="[^"]*" name="([^"]+)"[^>]*>(.*?)</var>', text, re.S):
        label = re.search(r'<labl level="variable">([^<]*)</labl>', body)
        cats = re.findall(r'<catgry[^>]*><catValu>([^<]*)</catValu>.*?'
                          r'<catStat type="freq">(\d+)</catStat></catgry>', body, re.S)
        out.append((name, label.group(1) if label else "", [(c, int(n)) for c, n in cats]))
    return out


def verify():
    t = lambda n: os.path.join(TARGET, n)
    meta = json.load(open(t(METADATA)))
    md5 = {f["dataFile"]["id"]: f["dataFile"]["md5"] for f in meta["datasetVersion"]["files"]}
    tabs = {n: pd.read_csv(t(n), sep="\t", low_memory=False) for n in TABLES.values()}
    s, k3, cmp_ = tabs["STAR_Students.tab"], tabs["STAR_K-3_Schools.tab"], tabs["Comparison_Students.tab"]

    checks = [
        ("licence is CC0 1.0", meta["datasetVersion"]["license"]["name"] == "CC0 1.0"),
    ]
    for fid, name in DOCS.items():
        got = hashlib.md5(open(t(name), "rb").read()).hexdigest()
        checks.append((f"{name} matches the Dataverse MD5", got == md5[fid]))

    # Every value-label frequency Dataverse computed at ingest reproduces from the tab export,
    # and every table's columns are exactly the variables its codebook lists, in order.
    n_cats = 0
    for name, df in tabs.items():
        vs = ddi_vars(t(ddi_name(name)))
        checks.append((f"{name} columns match its DDI variables", [v[0] for v in vs] == list(df.columns)))
        bad = 0
        for var, _, cats in vs:
            col = pd.to_numeric(df[var], errors="coerce")
            for code, freq in cats:
                n_cats += 1
                bad += int((col == float(code)).sum() != freq)
        checks.append((f"{name} value-label frequencies reproduce ({sum(len(v[2]) for v in vs)})", bad == 0))

    sch = set(k3["schid"])
    in_star = lambda g: s[f"{g}classtype"].notna()
    checks += [
        ("student file over 10,000 rows", len(s) > 10_000),
        ("student file has the 11,601 students the guide states", len(s) == 11_601),
        ("comparison file has the 1,780 students the guide states", len(cmp_) == 1_780),
        ("K-3 school file has 80 schools, ids unique", len(k3) == 80 and k3["schid"].is_unique),
        ("student ids unique", s["stdntid"].is_unique and cmp_["stdntid"].is_unique),
        ("STAR and comparison student ids do not overlap", not set(s["stdntid"]) & set(cmp_["stdntid"])),
        ("class type codes are 1, 2 or 3 wherever present",
         all(set(s[f"{g}classtype"].dropna()) <= {1, 2, 3} for g in ("gk", "g1", "g2", "g3"))),
        ("every K-3 school id in the student file is in the school file",
         all(set(s[f"{g}schid"].dropna()) <= sch for g in ("gk", "g1", "g2", "g3"))),
        ("a school id is present exactly when a class type is",
         all((s[f"{g}schid"].notna() == in_star(g)).all() for g in ("gk", "g1", "g2", "g3"))),
        ("teacher ids nest within school ids wherever a teacher id is present",
         all((s.loc[s[f"{g}tchid"].notna(), f"{g}tchid"] // 100
              == s.loc[s[f"{g}tchid"].notna(), f"{g}schid"]).all() for g in ("gk", "g1", "g2", "g3"))),
        ("one grade-3 record has a class type but no teacher id, and no other grade has one",
         [int((in_star(g) & s[f"{g}tchid"].isna()).sum()) for g in ("gk", "g1", "g2", "g3")] == [0, 0, 0, 1]),
        ("kindergarten ran in 79 schools", s.loc[in_star("gk"), "gkschid"].nunique() == 79),
        ("kindergarten arms are 1,900 small, 2,194 regular, 2,231 regular with aide",
         s["gkclasstype"].value_counts().to_dict() == {3: 2231, 2: 2194, 1: 1900}),
        ("26.6% of students were in STAR all four years, as the guide states",
         round(100 * (s["yearsstar"] == 4).mean(), 1) == 26.6),
        ("grade 1 to 3 arms are as the codebooks count them",
         [s[f"{g}classtype"].value_counts().sort_index().tolist() for g in ("g1", "g2", "g3")]
         == [[1925, 2584, 2320], [2016, 2329, 2495], [2174, 2085, 2543]]),
    ]

    files = sorted(f for f in os.listdir(TARGET) if not f.startswith("."))
    formats = sorted({f.rsplit(".", 1)[1] for f in files})
    checks += [("10 or more files", len(files) >= 10), ("3 or more formats", len(formats) >= 3)]

    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    print(f"{len(files)} files, formats {formats}, {n_cats} value-label frequencies checked")
    print(", ".join(f"{n} {len(df):,} rows" for n, df in tabs.items()))
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
