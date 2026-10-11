"""Build the pack, the goldens and metadata.json, run every check and the verifier, build a second
time into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task445/generator/make.py
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks as C
import deliver as DL
import docs as D
import golden as G
import pack as P
import sim as S
import verify as V

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2023, 2, 4, 6, 12, 0)

DISTRACTORS = [D.SHORTS, D.LIST13F]


def build(target, golden_dir):
    shutil.rmtree(target, ignore_errors=True)
    shutil.rmtree(golden_dir, ignore_errors=True)
    wd = S.build()
    counts = P.write_all(wd, target)
    g = G.compute(target)
    DL.write(g, golden_dir)
    return wd, g, counts


def describe(target):
    desc = {
        "form13f_2022q3/SUBMISSION.tsv": "SEC Form 13F data set, filings submitted 1 Jul to 30 Sep 2022: submissions",
        "form13f_2022q3/COVERPAGE.tsv": "SEC Form 13F data set, filings submitted 1 Jul to 30 Sep 2022: cover pages",
        "form13f_2022q3/INFOTABLE.tsv": "SEC Form 13F data set, filings submitted 1 Jul to 30 Sep 2022: information tables",
        "form13f_2022q4/SUBMISSION.tsv": "SEC Form 13F data set, filings submitted 1 Oct to 31 Dec 2022: submissions",
        "form13f_2022q4/COVERPAGE.tsv": "SEC Form 13F data set, filings submitted 1 Oct to 31 Dec 2022: cover pages",
        "form13f_2022q4/INFOTABLE.tsv": "SEC Form 13F data set, filings submitted 1 Oct to 31 Dec 2022: information tables",
        "edgar13f_daily_20230103_20230203/SUBMISSION.tsv": "Nightly EDGAR 13F build, filings accepted 3 Jan to 3 Feb 2023: submissions",
        "edgar13f_daily_20230103_20230203/COVERPAGE.tsv": "Nightly EDGAR 13F build, filings accepted 3 Jan to 3 Feb 2023: cover pages",
        "edgar13f_daily_20230103_20230203/INFOTABLE.tsv": "Nightly EDGAR 13F build, filings accepted 3 Jan to 3 Feb 2023: information tables",
        "fsds_cover_extract/sub.txt": "Cover-page extract in the financial statement data sets layout: submissions",
        "fsds_cover_extract/num.txt": "Cover-page extract in the financial statement data sets layout: dei cover tags",
        "manager_register.csv": "Ownership desk register of 13F filing managers",
        D.WATCHLIST: "Client watchlist, crowding monitor",
        D.LAYOUT: "Client flag file layout v3",
        D.METHOD_PDF: "Ownership methodology note OM-4",
        D.README: "Readme for the Form 13F data sets (tables, fields)",
        D.SOURCES: "Data sources note for the ownership desk",
        D.SHORTS: "Exchange short interest for the watchlist, settlement 30 Dec 2022",
        D.LIST13F: "Official list of Section 13(f) securities, fourth quarter 2022, rows for covered issuers",
    }
    files = []
    for rel in sorted(desc):
        p = os.path.join(target, rel)
        ext = os.path.splitext(rel)[1].lstrip(".")
        rows = None
        if ext in ("tsv", "csv") or rel.endswith(("sub.txt", "num.txt")):
            rows = sum(1 for _ in open(p, encoding="utf-8")) - 1
        files.append({"path": rel, "format": ext, "bytes": os.path.getsize(p), "rows": rows,
                      "source": ("Constructed: " if not rel.endswith("readme.htm") else "Constructed on the SEC readme's structure: ") + desc[rel],
                      "date": "2023-02-04", "license": "CC0-1.0 (original work, constructed for this task)"})
    return files


def metadata(target, counts):
    files = describe(target)
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task445",
        "title": "Which watchlist names carry the crowded-ownership flag for the December 2022 13F quarter",
        "domain": "Quantitative Finance",
        "subdomain": "other: institutional ownership analytics from Form 13F holdings filings",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "03 (bridge between two totals): the September bridge from the SEC information-table lines to conformed institutional shares, inside a twelve-row client flag file with ownership, flag, share counts and top holder per name for two periods",
        "as_of": "2023-02-06",
        "deliverables": ["crowded_flags_2022q4.csv", "sep_quarter_bridge.png"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task445/generator/make.py (seeded, deterministic) in the "
                               "layout of the SEC Form 13F data sets and the SEC financial statement data sets; every "
                               "manager, issuer, CIK, CUSIP and figure is invented and no real filer or security is depicted",
                     "date": "2023-02-04", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task445/generator/make.py",
        "files": files,
    }


def stamp_tree(root):
    import time
    t = time.mktime(STAMP + (0, 0, -1))
    for dp, dns, fns in os.walk(root):
        for fn in fns:
            os.utime(os.path.join(dp, fn), (t, t))


def zip_target(target, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dns, fns in sorted(os.walk(target)):
            dns.sort()
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                rel = os.path.relpath(p, target)
                zi = zipfile.ZipInfo(rel, date_time=STAMP)
                zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, open(p, "rb").read())


def main():
    wd, g, counts = build(TARGET, GOLDEN)
    meta = metadata(TARGET, counts)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    n = C.run(wd, g, TARGET, GOLDEN, meta)
    out, br = V.run(TARGET, GOLDEN)
    assert br["conformed"] == g["bridge"]["conformed"] and br["superseded"] == g["bridge"]["superseded"] \
        and br["options"] == g["bridge"]["options"] and br["cusip_repaired"] == g["bridge"]["cusip_repaired"], (br, g["bridge"])
    with open(os.path.join(HERE, "golden_figures.json"), "w", encoding="utf-8") as fh:
        json.dump({k: g[k] for k in ("bridge", "c_count", "c_value", "c_value_june", "thousands_after_switch")}
                  | {"rungs": {k: {c: round(v, 3) for c, v in g[k].items()} for k in ("R0", "R1", "R2", "R3", "R3w", "R4dev", "dec_io", "sep_io")},
                     "backtest": g["backtest"], "sep_wrong": g["sep_wrong"], "top": g["top"], "top_wrong": g["top_wrong"],
                     "dec_onfile_shares": g["dec_onfile_shares"], "dec_carried_shares": g["dec_carried_shares"],
                     "pending_count": len(g["pending_ciks"])}, fh, indent=1, default=str)
    # second build, byte-identical
    tmp = tempfile.mkdtemp()
    t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    build(t2, g2)
    for a, b in ((TARGET, t2), (GOLDEN, g2)):
        for dp, _, fns in os.walk(a):
            for fn in fns:
                p = os.path.join(dp, fn)
                q = os.path.join(b, os.path.relpath(p, a))
                assert filecmp.cmp(p, q, shallow=False), f"not byte-identical: {p}"
    shutil.rmtree(tmp)
    stamp_tree(TARGET)
    zip_target(TARGET, os.path.join(TASK, "target.zip"))
    print(f"checks {n} green; verifier ok; two builds byte-identical; files {meta['input_gates']}")


if __name__ == "__main__":
    main()
