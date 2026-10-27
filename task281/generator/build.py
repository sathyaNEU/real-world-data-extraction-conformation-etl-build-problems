"""Build task281: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task281/generator/build.py              everything
    python3 task281/generator/build.py --out DIR    the pack only, into DIR
    python3 task281/generator/build.py --golden     the pack and the goldens, no checks"""
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
import context as CX       # noqa: E402
import docs as DC          # noqa: E402
import payroll as PY       # noqa: E402
import records as R        # noqa: E402
import world as Wd         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())
EARN = [("OT", "Overtime 1.5"), ("OTN", "Shift differential - night"), ("OTR", "Retro pay - overtime"),
        ("CTE", "Comp time earned 1.5"), ("CTS", "Comp time earned 1.0")]


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = Wd.World(seed)
    rc = R.Records(w)
    py = PY.Payroll(w, rc)
    n = {}
    for key, fn in (("rosters", rc.roster_rows), ("employees", rc.employee_rows),
                    ("position", rc.position_control_rows), ("classes", rc.class_rows), ("codes", rc.code_rows),
                    ("payroll", py.payroll_rows), ("offers", py.offer_rows), ("inmates", CX.inmate_rows),
                    ("cad", CX.cad_rows),
                    ("winter", CX.winter_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    R.write_csv(p("earn"), ["earn_code", "description"], [list(r) for r in EARN])
    n["earn"] = len(EARN)
    DC.write_otprog(p("otprog"), CX.otprog_rows())
    DC.write_standard(p("standard"))
    DC.write_memo(p("memo"))
    DC.write_agreement(p("agreement"))
    return dict(w=w if keep else None, rc=rc if keep else None, py=py if keep else None, counts=n)


PDF_DATES = {"standard": ("D:20240814103000-04'00'", "D:20240814103000-04'00'"),
             "memo": ("D:20261009153200-04'00'", "D:20261009153200-04'00'"),
             "agreement": ("D:20260402091500-04'00'", "D:20260402091500-04'00'")}
OOXML = {"otprog": ("Comptroller of Merrimont", "Comptroller of Merrimont", "2026-09-14T13:20:00Z",
                    "2026-09-30T18:05:00Z", "Overtime expenditure FY2026", True)}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.STATE
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.STATE
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), K.PEOPLE["desk"], K.PEOPLE["desk"], "2026-10-26T13:05:00Z",
                       "2026-11-04T20:41:00Z", title="FY2028 relief positions by unit", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); the %s, its agencies, units, people and records are "
           "fictional; the records follow the forms of US state timekeeping roster exports, HR extracts, position "
           "control projections and biweekly payroll earnings lines" % K.STATE)
    return {
        "task": "task281",
        "title": "%s: the FY2028 overtime-relief positions placed across eight round-the-clock units" % K.STATE,
        "domain": "General Statistics & Data Science (exploratory data analysis and distribution assessment)",
        "objective": "Descriptive & Distribution Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-23", "licence": "CC0 1.0 (constructed for this task)"}
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
