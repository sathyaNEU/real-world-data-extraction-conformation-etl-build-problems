"""Build task270: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task270/generator/build.py              everything
    python3 task270/generator/build.py --out DIR    the pack only, into DIR
    python3 task270/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as WD         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())
FILES = dict(K.FILES, dictionary="data_dictionary.csv")


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = WD.World(seed)
    rc = R.Records(w, seed)
    n = {}
    for key, fn in (("scorecards", rc.scorecard_rows), ("registry", rc.registry_rows), ("holdout", rc.holdout_rows),
                    ("cohorts", rc.cohort_rows), ("calendar", rc.calendar_rows), ("forecast", rc.forecast_rows),
                    ("ratings", rc.ratings_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    DC.write_standard(p("standard"))
    DC.write_guide(p("guide"))
    DC.write_catalogue(p("catalogue"))
    DC.write_dictionary(p("dictionary"))
    DC.write_spend(p("spend"), rc.spend_rows())
    exps = len({r[0] for r in rc.scorecard_rows()[1]})
    DC.write_export_notes(p("export_notes"), dict(experiments=exps, rows="{:,}".format(n["scorecards"])))
    return dict(world=w if keep else None, records=rc if keep else None, counts=n)


PDF_DATES = {"standard": ("D:20261012161500+02'00'", "D:20261012161500+02'00'"),
             "guide": ("D:20240212101000+01'00'", "D:20261005143000+02'00'")}
OOXML = {"spend": ("Renske Mudden", "Renske Mudden", "2026-02-03T08:20:00Z", "2026-10-07T13:42:00Z",
                   "Acquisition spend 2026", True)}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.ORG
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.ORG
    PP.normalize_ooxml(os.path.join(golden, K.BOOK), K.HEAD_EXP, K.HEAD_EXP, "2026-10-26T07:55:00Z",
                       "2026-10-30T15:20:00Z", title="Proxy metric scores 2027", excel=True)
    PP.normalize_ooxml(os.path.join(golden, K.DECK), K.HEAD_EXP, K.HEAD_EXP, "2026-10-27T09:05:00Z",
                       "2026-10-30T15:41:00Z", title="Proxy metric review 2027")
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, its teams, experiments, users and people are fictional; "
           "the records follow the forms of a consumer app's experimentation platform (scorecard export, experiment "
           "registry), its data warehouse, its growth analytics tables and its forecasting tool" % K.ORG)
    return {
        "task": "task270",
        "title": "%s: the 2027 proxy metric for six-month retention" % K.ORG,
        "domain": "Product Analytics (metric definition and measurement science)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-26", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(FILES.values())},
        "rows": {FILES[k]: v for k, v in sorted(counts.items())},
        "answer": fig["call"]["sentence"],
    }


def main_build(target, golden, seed=K.SEED):
    import deliver as DV
    b = build(target, seed, keep=True)
    finish(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    fig, res = DV.write(target, golden)
    finish_golden(golden)
    DV.write_figures(os.path.join(HERE, "figures.json"), fig)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, res


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(target, path):
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=K.SEED)
    a = ap.parse_args()
    if a.out:
        b = build(a.out, a.seed)
        finish(a.out)
        print(b["counts"])
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden, a.seed)
    print("pack:", b["counts"])
    print("call:", fig["call"]["sentence"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"), a.seed)
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    finish_golden(os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    g1, g2 = digest(golden), digest(os.path.join(scratch, "golden"))
    same = d1 == d2 and g1 == g2
    for f in sorted(set(d1) | set(g1)):
        if d1.get(f, g1.get(f)) != d2.get(f, g2.get(f)):
            print("  differs on rebuild:", f)
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
