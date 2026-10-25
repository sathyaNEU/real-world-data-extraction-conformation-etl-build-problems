"""Build task121: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task121/generator/build.py              everything
    python3 task121/generator/build.py --out DIR    the pack only, into DIR
    python3 task121/generator/build.py --golden     the pack and the goldens, no checks"""
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
import records as RC       # noqa: E402
import trust as T          # noqa: E402
import world as Wd         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())


def build(out, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = Wd.World()
    tr = T.Trust()
    n = {}
    tabs = None
    for key, fn in (("transfer", lambda: RC.transfer(w)), ("register", lambda: RC.register(w)),
                    ("tables", lambda: RC.tables(w)), ("attendance", lambda: RC.attendance(tr)),
                    ("movements", lambda: RC.movements(tr)), ("results25", lambda: RC.results(tr, "June 2025")),
                    ("results26", lambda: RC.results(tr, "June 2026"))):
        head, rows = fn()
        RC.write_csv(p(key), head, rows)
        n[key] = len(rows)
        if key == "tables":
            tabs = rows
    RC.estimates(p("estimates"))
    RC.workforce(p("workforce"), w)
    RC.funding(p("funding"), w)
    DC.write_paper(p("paper"), tabs)
    DC.write_guide(p("guide"))
    DC.write_measures(p("measures"))
    DC.write_attnote(p("attnote"))
    return dict(w=w if keep else None, tr=tr if keep else None, counts=n)


PDF_DATES = {"paper": ("D:20261023141500+01'00'", "D:20261023141500+01'00'"),
             "guide": ("D:20260911093000+01'00'", "D:20260911093000+01'00'"),
             "measures": ("D:20260929110000+01'00'", "D:20260929110000+01'00'"),
             "attnote": ("D:20260922154500+01'00'", "D:20260922154500+01'00'")}
OOXML = {"estimates": ("Department for Education", "Department for Education", "2025-02-06T09:30:00Z",
                       "2025-02-06T09:30:00Z", "Progress 8 estimates", True),
         "workforce": (K.PEOPLE["la"], K.PEOPLE["la"], "2026-06-18T10:02:00Z", "2026-06-18T10:41:00Z",
                       "School workforce, November 2025", True),
         "funding": (K.PEOPLE["la"], K.PEOPLE["la"], "2025-03-27T13:20:00Z", "2025-04-02T08:55:00Z",
                     "School funding 2025-26", True)}


def finish(out):
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.COMPANY = K.COUNCIL if k != "estimates" else "Department for Education"
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.TRUST
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), K.PEOPLE["data"], K.PEOPLE["data"],
                       "2026-10-26T09:05:00Z", "2026-11-04T16:40:00Z", title="Halwick Progress 8 walk", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, %s, the borough of %s, their schools, people and records "
           "are fictional; the records follow the forms of a local authority's key stage 2 to key stage 4 pupil file, "
           "the Department for Education's performance tables and Progress 8 estimates, and a multi-academy trust's "
           "attendance, movements and examination results exports" % (K.TRUST, K.COUNCIL, K.BOROUGH))
    return {
        "task": "task121",
        "title": "%s: whether Halwick Academy's own effect accounts for most of its Progress 8 gap to the trust "
                 "average, 2022 to 2024" % K.TRUST,
        "domain": "Education & Learning Sciences (multilevel school effects research)",
        "objective": "Root-Cause Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-23", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": fig["call"]["sentence"],
    }


def main_build(target, golden):
    import deliver as DV
    b = build(target, keep=True)
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
    a = ap.parse_args()
    if a.out:
        b = build(a.out)
        finish(a.out)
        print(b["counts"])
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"))
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
