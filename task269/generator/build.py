"""Build task269: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task269/generator/build.py              everything
    python3 task269/generator/build.py --out DIR    the pack only, into DIR
    python3 task269/generator/build.py --golden     the pack and the goldens, no checks"""
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
import world as Wd         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = Wd.World(seed)
    rc = R.Records(w)
    n = {}
    for key, fn in (("roll26", rc.roll26_rows), ("crosswalk", rc.crosswalk_rows), ("changes", rc.change_rows),
                    ("deeds", rc.deed_rows), ("index", rc.index_rows), ("permits", rc.permit_rows),
                    ("bor", rc.bor_rows), ("homestead", rc.homestead_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    head, rows = rc.roll25_rows()
    DC.write_roll25(p("roll25"), head, rows)
    n["roll25"] = len(rows)
    DC.write_rule(p("rule"))
    DC.write_memo(p("memo"))
    DC.write_dictionary(p("dictionary"))
    tot = sum(r[8] for r in rows) * 0.83
    taxable = {name: int(round(tot * sh, -3)) for (name, _, _), sh in
               zip(DC.LEVY, (1.0, 1.0, 1.0, 0.71, 0.71, 0.29, 0.38, 0.062, 0.54, 0.83))}
    DC.write_levy(p("levy"), taxable)
    n["levy"] = len(DC.LEVY)
    return dict(w=w if keep else None, rc=rc if keep else None, counts=n)


PDF_DATES = {"rule": ("D:20210311140000-06'00'", "D:20210311140000-06'00'"),
             "memo": ("D:20260914101500-05'00'", "D:20260914101500-05'00'")}
OOXML = {"roll25": ("CAMA Legacy", "CAMA Legacy", "2026-01-08T22:42:00Z", "2026-01-08T22:42:00Z",
                    "2025 certified roll", True),
         "levy": ("Tillford County Auditor", "Tillford County Auditor", "2025-11-03T15:10:00Z",
                  "2025-11-21T19:32:00Z", "FY2026 levies and rates", True)}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.COUNTY
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.COUNTY
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN_BOOK), "Budget and Policy Analysis", "Budget and Policy Analysis",
                       "2026-09-24T14:05:00Z", "2026-10-01T21:12:00Z", title="2026 roll on Rule 18-7", excel=True)
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN_MEMO), "Budget and Policy Analysis", "Budget and Policy Analysis",
                       "2026-09-29T16:20:00Z", "2026-10-01T22:03:00Z",
                       title="The single-family reappraisal offer")
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, its state, offices, people and records are fictional; "
           "the records follow the forms of US county appraisal-system roll exports, recorder deed extracts, "
           "building permit logs and board of review hearing logs" % K.COUNTY)
    return {
        "task": "task269",
        "title": "%s: does the 2026 single-family roll meet the State's ratio study rule, or does the county accept "
                 "its vendor's reappraisal offer" % K.COUNTY,
        "domain": "General Statistics & Data Science (missing data, censoring and measurement error)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-09-18", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
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
    print("call:", fig["call"])
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
