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
        D.LAYOUT: "Client flag file layout v4",
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
        "prompt_shape": "03 (bridge between two totals): the September bridge from the SEC information-table lines to conformed institutional shares, inside a twelve-row client flag file in layout v4 with December ownership, the flag and September ownership per name",
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
    out, br, vx = V.run(TARGET, GOLDEN)
    assert br["conformed"] == g["bridge"]["conformed"] and br["superseded"] == g["bridge"]["superseded"] \
        and br["options"] == g["bridge"]["options"] and br["cusip_repaired"] == g["bridge"]["cusip_repaired"], (br, g["bridge"])
    assert vx["due"] == len(g["due_ciks"]), vx
    for k, v in g["stops_a"].items():
        assert all(abs(vx["stops_a"][k][c] - v[c]) < 1e-9 for c in g["cusips"]), ("verifier Ask A stop", k)
    for k, v in g["stops_b"].items():
        assert all(vx["stops_b"][k][x] == v[x] for x in vx["stops_b"][k]), ("verifier Ask B stop", k, vx["stops_b"][k], v)
    r3 = lambda d: {c: round(v, 3) for c, v in d.items()}
    with open(os.path.join(HERE, "golden_figures.json"), "w", encoding="utf-8") as fh:
        json.dump({"bridge": g["bridge"], "backtest": C.LOG["backtest"], "dec_io": r3(g["dec_io"]), "sep_io": r3(g["sep_io"]),
                   "jun_io": r3(g["jun_io"]), "rungs": {k: r3(v) for k, v in g["rungs"].items()},
                   "variants": {k: r3(v) for k, v in g["dec_variants"].items()},
                   "type_change": g["type_change"], "type_change_allsec": g["type_change_allsec"],
                   "sponsor_change_name": g["sponsor_change_name"], "sponsor_stake_change": g["sponsor_stake_change"],
                   "grid": {f"{a}|{b}": r3(v) for (a, b), v in g["grid"].items()},
                   "type_change_sep_window": g["type_change3"],
                   "stops_a": {k: r3(v) for k, v in g["stops_a"].items()}, "stops_b": g["stops_b"],
                   "dec_onfile_shares": g["dec_onfile_shares"], "checks": {k: v for k, v in C.LOG.items() if k != "backtest"},
                   "verifier_window_miss": vx["miss"]}, fh, indent=1, default=str)
    # figures.json: every figure submission.md states, as it states it (figures_check.py)
    tk = dict(zip(g["cusips"], g["tickers"]))
    b = g["bridge"]
    fig = {"call": {tk[c]: DL.r1(g["dec_io"][c]) for c in g["cusips"]},
           "due": len(g["due_ciks"]),
           "sponsors_change_pct": {"OTF": f"{100 * (g['sponsor_change_name'][g['cusips'][2]] - 1):.1f}",
                                   "pooled": f"{100 * (g['type_change']['Index and ETF sponsor'] - 1):.1f}"},
           "line": "80.0",
           "type_pooled_OTF": DL.r1(g["rungs"]["type_pooled"][g["cusips"][2]]),
           "backtest": {k: f"{C.LOG['backtest'][k]:.2f}" for k in ("sponsors_per_name", "type_pooled", "flat")},
           "flag_file": {tk[c]: {"dec": DL.r1(g["dec_io"][c]), "flag": "Y" if g["flag"][c] else "N",
                                 "sep": DL.r1(g["sep_io"][c]), "cusip": c} for c in g["cusips"]},
           "bridge": {"start": f"{b['raw']:,}", "options": f"-{b['options']:,}", "superseded": f"-{b['superseded']:,}",
                      "cusips": f"+{b['cusip_repaired']:,}", "end": f"{b['conformed']:,}",
                      "gap_m": f"{(b['raw'] - b['conformed']) / 1e6:.1f}"}}
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
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
