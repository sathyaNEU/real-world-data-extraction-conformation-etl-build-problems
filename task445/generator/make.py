"""Build the pack, the goldens and metadata.json, run every check and the verifier, build a second time into a
scratch folder and require byte-identical output, then cut target.zip.

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
import checks as C  # noqa: E402
import deliver as DL  # noqa: E402
import pack as PK  # noqa: E402
import sim  # noqa: E402
import solve as SV  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

TASK = W.TASK
STAMP = (2026, 10, 9, 17, 40, 0)

DESC = {
    PK.REG: "Death registrations of Ellesmoor residents from 1 January 2021, entries to 9 October 2026 (primary care "
            "mortality extract layout)",
    PK.NORTH: "North Ellesmoor Medical Examiner Office scrutiny log, 9 September 2024 to 9 October 2026",
    PK.SOUTH: "South Ellesmoor Medical Examiner Office case export (JSON), 9 September 2024 to 9 October 2026",
    PK.LOOKUP: "Postcode to place lookup for the six Ellesmoor places, live and terminated postcodes",
    PK.DISTRICTS: "Registration districts and their codes before and after 3 April 2023",
    PK.POPULATION: "Mid-2025 population estimates by place and age band",
    PK.TEMPERATURE: "Daily maximum temperatures at two Ellesmoor stations, June to September 2026",
    PK.ALERTS: "Heat-health alerts for the north of England, summer 2026",
    PK.TERMS: "Heat Resilience Fund 2027 allocation terms, board paper B/26/41, with Table 1",
    PK.CARE: "The board's commissioning list of care homes in the six places, October 2026",
}


def build(target, golden_dir):
    shutil.rmtree(target, ignore_errors=True)
    shutil.rmtree(golden_dir, ignore_errors=True)
    T = sim.build()
    counts = PK.write_all(T, target)
    S = SV.solve(target)
    DL.write(S, golden_dir)
    return T, S, counts


def describe(target, counts):
    files = []
    for rel in sorted(DESC):
        p = os.path.join(target, rel)
        ext = os.path.splitext(rel)[1].lstrip(".")
        rows = None
        if ext == "csv":
            rows = sum(1 for _ in open(p, encoding="utf-8")) - 1
        elif rel in counts:
            rows = counts[rel]
        files.append({"path": rel, "format": ext, "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed: " + DESC[rel], "date": "2026-10-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    return files


def metadata(target, counts):
    files = describe(target, counts)
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task445",
        "title": "Which Ellesmoor places qualify for the 2027 heat resilience grants",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10 (scorecard against thresholds): each place's summer 2026 deaths, expected deaths, excess "
                        "and qualification against the fund's line, with the medical examiner offices' quarters and "
                        "the registration shares by place and quarter",
        "as_of": "2026-10-14",
        "deliverables": [DL.XLSX, DL.CSV],
        "distractor_files": PK.DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task445/generator/make.py (seeded, deterministic) in the "
                               "layouts of an English primary care mortality extract, two medical examiner offices' "
                               "case systems and an integrated care board paper; every place, person, postcode, "
                               "organisation and figure is invented",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-31",
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


def figures(S):
    r1 = SV.r1
    tot = sum(S["counts"].values())
    texp = sum(S["expected"].values())
    return {
        "call": {p: {"deaths": S["counts"][p], "expected": S["expected"][p], "excess": r1(S["excess"][p]),
                     "qualifies": "Yes" if p in S["qualifying"] else "No",
                     "grant": "{:,}".format(W.GRANT if p in S["qualifying"] else W.STANDARD),
                     "not_registered": S["added"].get(p, 0), "registered": S["rungs"]["registered"][p],
                     "pooled_excess": r1(S["rung_excess"]["pooled"][p]),
                     "registered_excess": r1(S["rung_excess"]["registered"][p])} for p in W.NAMES},
        "total": {"deaths": "{:,}".format(tot), "expected": "{:,}".format(texp),
                  "excess": r1(100.0 * (tot - texp) / texp), "not_registered": sum(S["added"].values()),
                  "grants": "{:,}".format(sum(W.GRANT if p in S["qualifying"] else W.STANDARD for p in W.NAMES))},
        "line": "10.0", "grant": "300,000", "standard": "60,000",
        "completeness": r1(100 * S["completeness"][("all", 0)]),
        "months": {"%s %d" % (p, m): S["months"][(p, m)] for p in W.NAMES for m in (6, 7, 8)},
        "ask_b": {"%s Q%d" % k: "{:,}".format(v) for k, v in S["ask_b"].items()},
        "ask_b_year": {o: "{:,}".format(sum(S["ask_b"][(o, q)] for q in (1, 2, 3, 4))) for o in ("North", "South")},
        "ask_c": {"%s Q%d" % k: r1(v) for k, v in S["ask_c"].items()},
    }


def main():
    T, S, counts = build(W.TARGET, W.GOLDEN)
    meta = metadata(W.TARGET, counts)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    n = C.run(T, S, W.TARGET, W.GOLDEN, meta)
    vx = V.run(W.TARGET)
    assert vx["counts"] == S["counts"], (vx["counts"], S["counts"])
    assert vx["qualifying"] == S["qualifying"], vx["qualifying"]
    assert vx["expected"] == S["expected"]
    assert vx["ask_b"] == S["ask_b"], (vx["ask_b"], S["ask_b"])
    assert all(abs(vx["ask_c"][k] - S["ask_c"][k]) < 1e-9 for k in S["ask_c"]), "verifier ask C"
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(figures(S), fh, indent=1)
        fh.write("\n")
    tmp = tempfile.mkdtemp()
    t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    build(t2, g2)
    for a, b in ((W.TARGET, t2), (W.GOLDEN, g2)):
        for dp, _, fns in os.walk(a):
            for fn in fns:
                p = os.path.join(dp, fn)
                q = os.path.join(b, os.path.relpath(p, a))
                assert filecmp.cmp(p, q, shallow=False), "not byte-identical: %s" % p
    shutil.rmtree(tmp)
    stamp_tree(W.TARGET)
    zip_target(W.TARGET, os.path.join(TASK, "target.zip"))
    print("checks %d green; verifier ok; two builds byte-identical; files %s" % (n, meta["input_gates"]))
    print("golden %s; rungs %s" % (S["qualifying"], C.LOG["rungs"]))


if __name__ == "__main__":
    main()
