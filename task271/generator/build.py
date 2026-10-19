"""Build task271: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task271/generator/build.py              everything
    python3 task271/generator/build.py --out DIR    the pack only, into DIR
    python3 task271/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import core as C           # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("criteria", "Corrisbrook Health Cooperative: Pancreatic Surgery Centres, 2027 programme criteria, version 2."),
    ("guide", "Upper Lakes Hospital Data Consortium: hepatobiliary and pancreatic research files, file guide 2026."),
    ("d2016", "ULHDC hepatobiliary and pancreatic discharges, 2016 (fixed width)."),
    ("d2017", "ULHDC hepatobiliary and pancreatic discharges, 2017 (fixed width)."),
    ("d2018", "ULHDC hepatobiliary and pancreatic discharges, 2018 (fixed width)."),
    ("d2019_2022", "ULHDC hepatobiliary and pancreatic discharges, 2019 to 2022."),
    ("d2023_2025", "ULHDC hepatobiliary and pancreatic discharges, 2023 to 2025."),
    ("prelim", "ULHDC 2026 first quarter, preliminary release (15 May 2026)."),
    ("revised", "ULHDC 2026 first and second quarters, revised release (18 September 2026)."),
    ("deaths", "ULHDC death linkage, 2026 run (deaths to 31 August 2026)."),
    ("hospitals", "ULHDC hospital directory, with the numbering and ownership changes."),
    ("codes", "ULHDC procedure classes for the ICD-10-PCS codes in the files."),
    ("claims", "Corrisbrook facility claims for members' pancreatic resection stays, received through 30 September 2026."),
    ("stars", "Public overall hospital star ratings, 2026 release (Wisconsin hospitals in the directory)."),
    ("costs", "Corrisbrook Finance: travel benefit estimates for 2027 budgeting (draft, 12 August 2026)."),
]


def build(out, seed=C.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.world(seed)
    R.assign_ids(w)
    by = R.discharges(w)
    n = {}
    for y in (2016, 2017, 2018):
        n["d%d" % y] = R.write_fixed(p("d%d" % y), by.get(y, []), w, y)
    n["d2019_2022"] = R.write_csv(p("d2019_2022"), sum((by.get(y, []) for y in range(2019, 2023)), []), w, 2)
    n["d2023_2025"] = R.write_csv(p("d2023_2025"), sum((by.get(y, []) for y in range(2023, 2026)), []), w, 3)
    pr, rv = R.releases_2026(w)
    n["prelim"] = R.write_release(p("prelim"), pr, w, "p_no")
    n["revised"] = R.write_release(p("revised"), rv, w, "r_no")
    n["deaths"] = R.write_deaths(p("deaths"), w)
    n["hospitals"] = R.write_hospitals(p("hospitals"))
    n["codes"] = R.write_classes(p("codes"))
    R.plan_claims(w)
    n["claims"] = R.write_claims(p("claims"), w)
    n["stars"] = R.write_stars(p("stars"), w)
    n["costs"] = R.write_travel(p("costs"), w)
    DC.write_criteria(p("criteria"))
    DC.write_guide(p("guide"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w if keep else None, counts=n)


DOC_DATES = {
    "criteria": ("D:20260929162000-05'00'", "D:20260930091500-05'00'"),
    "guide": ("D:20260921110500-05'00'", "D:20260922143000-05'00'"),
}
OOXML = {
    "hospitals": ("ULHDC Data Services", "ULHDC Data Services", "2023-01-09T15:12:00Z", "2026-09-01T13:41:00Z",
                  "ULHDC hospital directory"),
    "costs": ("Corrisbrook Finance", "Corrisbrook Finance", "2026-08-11T19:05:00Z", "2026-08-12T16:20:00Z",
              "Travel benefit estimates 2027"),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in DOC_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    for k, (cr, lb, c, m, title) in OOXML.items():
        PP.COMPANY = K.CONSORTIUM if k == "hospitals" else K.PLAN
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=True)
    PP.COMPANY = K.PLAN
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.PLAN
    PP.normalize_ooxml(os.path.join(golden, "pancreatic_centres_2027.xlsx"), K.PEOPLE["requester"],
                       K.PEOPLE["requester"], "2026-10-09T15:02:00Z", "2026-10-12T21:47:00Z",
                       title="Pancreatic Surgery Centres 2027", excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    return {
        "task": "task271",
        "title": "%s: the three 2027 %s" % (K.PLAN, K.PROGRAMME),
        "domain": "Healthcare Delivery & Health Economics (provider quality and risk adjustment)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["stars"], K.FILES["costs"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); %s, the %s, every hospital and "
                                        "every person are fictional; the NPIs are invented and fail the NPI check digit, "
                                        "so none is a real provider's number" % (K.PLAN, K.CONSORTIUM),
                              "date": "2026-10-09", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Centres for 2027: %s" % ", ".join(fig["call"]["centres"]),
    }


def main_build(target, golden, seed=C.SEED):
    import deliver as DV
    b = build(target, seed, keep=True)
    finish(target)
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
        h[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return h


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
    ap.add_argument("--seed", type=int, default=C.SEED)
    a = ap.parse_args()
    if a.out:
        build(a.out, a.seed)
        finish(a.out)
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
