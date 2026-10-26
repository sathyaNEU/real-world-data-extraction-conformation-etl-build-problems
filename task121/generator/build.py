"""Build task121: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

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
import records as R        # noqa: E402
import world as WD         # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("definitions", "Quality assurance program: measures and definitions (effective 1 July 2025)."),
    ("release", "Systems team: protocol software release 13.3, go-live note."),
    ("reference", "Centre reference: trunk groups, ambulances, protocols and positions."),
    ("takers", "Scheduling system: call-takers, with their CAD logins."),
    ("roster", "Scheduling system: the shifts each call-taker worked, 18 August 2025 to 31 August 2026."),
    ("calls", "CAD: medical calls answered, 1 September 2025 to 31 August 2026."),
    ("epcr", "ePCR: the crews' patient care records for those calls."),
    ("units", "CAD: ambulance assignments for those calls."),
    ("che", "911 call handling equipment: call detail, every call on the centre's trunks."),
    ("tcpr", "QA review log: cardiac arrest call reviews."),
    ("casereview", "QA review log: protocol compliance case reviews."),
    ("unithours", "EMS operations: ambulance staffed hours by day."),
    ("dictionary", "Data dictionary for the files above."),
]


def build(out, seed=K.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = WD.World(seed)
    rc = R.Records(w, seed)
    n = {}
    for key, fn in (("takers", rc.taker_rows), ("roster", rc.roster_rows), ("calls", rc.call_rows),
                    ("epcr", rc.epcr_rows), ("units", rc.unit_rows), ("che", rc.che_rows), ("tcpr", rc.tcpr_rows),
                    ("casereview", rc.case_rows), ("unithours", rc.unit_hour_rows)):
        head, rows = fn()
        R.write_csv(p(key), head, rows)
        n[key] = len(rows)
    DC.write_definitions(p("definitions"))
    DC.write_release(p("release"))
    DC.write_reference(p("reference"))
    DC.write_dictionary(p("dictionary"))
    DC.write_index(p("index"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(world=w if keep else None, counts=n)


PDF_DATES = {"definitions": ("D:20250618101500-05'00'", "D:20250626153000-05'00'"),
             "release": ("D:20260219164000-06'00'", "D:20260220091200-06'00'")}
OOXML = {"reference": (K.PEOPLE["qa"], K.PEOPLE["qa"], "2023-01-09T15:12:00Z", "2026-11-03T21:47:00Z",
                       "Centre reference", True)}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the folder's assembly."""
    import postprocess as PP
    for k, (c, m) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.CENTRE
    for k, (cr, lb, c, m, title, excel) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=excel)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.CENTRE
    PP.normalize_ooxml(os.path.join(golden, K.GOLDEN), K.REQUESTER, K.REQUESTER, "2026-11-12T16:05:00Z",
                       "2026-11-24T22:18:00Z", title="Under-triage cause 2026", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    src = ("constructed by the task generator (seeded); %s, its centre, call-takers, patients and people are fictional; "
           "the records follow the forms of a US county 911 centre's CAD, scheduling system, 911 call handling "
           "equipment and quality review logs, and an ambulance service's patient care records" % K.COUNTY)
    return {
        "task": "task121",
        "title": "%s: what caused the rise in under-triaged medical calls from March 2026" % K.CENTRE,
        "domain": "Human Factors & Ergonomics (workload, fatigue and shift analysis)",
        "objective": "Root-Cause Analysis",
        "distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS],
        "deliverables": list(K.DELIVERABLES),
        "provenance": {name: {"source": src, "date": "2026-10-26", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in sorted(counts.items())},
        "answer": fig["call"]["cause"],
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
    h = {}
    for f in sorted(os.listdir(folder)):
        with open(os.path.join(folder, f), "rb") as fh:
            h[f] = hashlib.md5(fh.read()).hexdigest()
    return h


def cut_zip(target, path):
    import zipfile
    if os.path.exists(path):
        os.remove(path)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            info = zipfile.ZipInfo(f, date_time=K.ASSEMBLED.timetuple()[:6])
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(os.path.join(target, f), "rb") as fh:
                z.writestr(info, fh.read())
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        finish(a.out)
        return 0
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        return 0
    import checks as CK
    import verify as VF
    rc = CK.run(TASK, b["world"], res)
    rv = VF.main(TASK)
    scratch = os.path.join(TASK, ".rebuild_check")
    build(scratch)
    finish(scratch)
    same = digest(scratch) == digest(target)
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    md5 = cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", md5)
    return 0 if (rc == 0 and rv == 0 and same) else 1


if __name__ == "__main__":
    sys.exit(main())
