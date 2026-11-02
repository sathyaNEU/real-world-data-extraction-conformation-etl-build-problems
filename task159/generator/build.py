"""Builds task159 end to end: the pack twice (asserted byte-identical), target/, the analysis, figures.json, the golden
deliverables, submission.md, metadata.json and target.zip.

    python3 build.py
"""
import filecmp
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import params as P          # noqa: E402
import pack                 # noqa: E402
import analysis as A        # noqa: E402
import golden               # noqa: E402
import writeup              # noqa: E402

ZIP_DT = (2026, 11, 13, 9, 30, 0)
TROY = 31.1034768


def rnd(v, u):
    return int(round(v / u)) * u


def digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def figures(t):
    r = A.compute(t)
    m = r["main"]
    F = dict(
        budget_oz=rnd(m["golden"], 10000), budget_oz_raw=round(m["golden"], 1),
        ore_mt_1dp=round(m["golden_t"] / 1e6, 1), ore_t_raw=round(m["golden_t"]), ore_t_100k=rnd(m["golden_t"], 100000),
        ore_grade_1dp=round(m["golden"] * TROY / m["golden_t"], 1),
        ore_grade_raw=round(m["golden"] * TROY / m["golden_t"], 3),
        plan_oz_100=rnd(m["plan_oz"], 100), plan_oz_raw=round(m["plan_oz"], 1),
        plan_mt_2dp=round(m["plan_t"] / 1e6, 2), plan_t_raw=round(m["plan_t"]), plan_t_10k=rnd(m["plan_t"], 10000),
        plan_grade_2dp=round(m["plan_oz"] * TROY / m["plan_t"], 2),
        f05_2dp=round(m["f05"], 2), f05_raw=round(m["f05"], 4), f09_1dp=round(m["f09"], 1), f09_raw=round(m["f09"], 4),
        n_pairs=m["n_pairs"],
        default_R1=rnd(m["R1"], 10000), default_R1_raw=round(m["R1"], 1), R0=rnd(m["R0"], 10000),
        family=dict(A=round(m["A"]), B05=round(m["B05"]), B10=round(m["B10"]), B20=round(m["B20"]), C=round(m["C"]),
                    D=round(m["D"])),
    )
    labels = {"2023": "31 December 2023", "2024": "31 December 2024", "2025": "31 December 2025",
              "2026-10": "31 October 2026"}
    F["stock_rows"] = [(labels[k], rnd(v[0], 1000), rnd(v[1], 100)) for k, v in r["stockpile"].items()]
    F["stock_raw"] = {k: [round(v[0], 1), round(v[1], 2)] for k, v in r["stockpile"].items()}
    F["hours_rows"] = [(k, rnd(v, 1)) for k, v in r["hours"].items()]
    F["hours_raw"] = {k: round(v, 3) for k, v in r["hours"].items()}
    F["fine_rows"] = [(k, rnd(v, 100)) for k, v in r["fine"].items()]
    F["fine_raw"] = {k: round(v, 2) for k, v in r["fine"].items()}
    return F, r


def metadata(target):
    files = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                files[f] = sum(1 for l in fh if not l.startswith("#")) - 1
        else:
            files[f] = ""
    big = max((k for k in files if isinstance(files[k], int)), key=lambda k: files[k])
    return {
        "task": "task159",
        "domain": "General Statistics & Data Science",
        "client_domain": "general-statistics-data-science",
        "subdomain": "regression-classification-model-diagnostics",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-11-13",
        "question": "the gold an Ontario open-pit mine budgets for the ore it mines in 2027 under a higher ore cut-off, "
                    "with the low-grade stockpile at four dates, the ball mill's running hours by quarter and the fine "
                    "gold poured by quarter",
        "deliverables": [golden.BOOK, golden.CHART],
        "distractor_files": [
            {"file": pack.F_EXPL, "why_relevant": "the resource drilling's assays are the data the block model was "
                                                  "estimated from", "why_unused": "no graded figure reads a drill "
                                                  "hole interval"},
            {"file": pack.F_GEOT, "why_relevant": "the Phase 5 and 6 walls bound the 2027 pit", "why_unused":
                "the 2027 schedule already carries the wall design; no graded figure reads a slope angle"},
            {"file": pack.F_PRICE, "why_relevant": "the budget's revenue and costs are priced from this deck",
             "why_unused": "every graded figure is in ounces, tonnes, hours or grams per tonne"}],
        "input_gates": {"files": len(files), "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
                        "largest_file": big, "largest_file_rows": files[big]},
        "files": files,
        "sources": [
            {"files": "all files under target/", "origin": "constructed for this task by task159/generator/build.py "
                                                           "(seeded and deterministic, seed %d)" % P.SEED,
             "license": "CC BY 4.0 (constructed data)", "date": "2026-11-13"},
            {"files": "NAD83(CSRS) UTM zone 17N, CGVD2013 heights, troy ounce (31.1034768 g)",
             "origin": "public geodetic and measurement standards", "license": "public", "date": "2026-11-13"}],
        "notes": "Synthetic pack. Aubreth Gold Corporation, the Kessock Lake mine, its refinery counterparty and "
                 "every person are invented; the northeastern Ontario setting, Canadian geodetic frames and the "
                 "laboratory and refinery conventions are real.",
    }


def zip_target(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=ZIP_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


def main():
    tmp = tempfile.mkdtemp(prefix="t159_")
    a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
    pack.build(a)
    pack.build(b)
    names = sorted(os.listdir(a))
    assert names == sorted(os.listdir(b))
    _, mism, err = filecmp.cmpfiles(a, b, names, shallow=False)
    assert not mism and not err, ("rebuild differs", mism, err)
    target = os.path.join(TASK, "target")
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(a, target)
    for f in os.listdir(target):
        st = os.stat(os.path.join(a, f))
        os.utime(os.path.join(target, f), (st.st_atime, st.st_mtime))
    F, r = figures(target)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    gdir = os.path.join(TASK, "golden")
    shutil.rmtree(gdir, ignore_errors=True)
    golden.build(gdir, F)
    writeup.emit(os.path.join(TASK, "submission.md"), F)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(target), f, indent=1)
    zpath = os.path.join(TASK, "target.zip")
    zip_target(target, zpath)
    shutil.rmtree(tmp)
    sha = hashlib.sha256(open(zpath, "rb").read()).hexdigest()
    print("byte-identical rebuild: %d files" % len(names))
    print("target digest %s" % digest(target)[:16])
    print("target.zip sha256 %s" % sha)
    print("budget gold %s oz (raw %.0f), default %s, plan %s" % (format(F["budget_oz"], ","), F["budget_oz_raw"],
                                                                 format(F["default_R1"], ","), format(F["plan_oz_100"], ",")))


if __name__ == "__main__":
    main()
