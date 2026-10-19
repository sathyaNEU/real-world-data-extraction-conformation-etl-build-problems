"""Build task270: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import books as BK         # noqa: E402
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("basis", "Pricing Committee paper PC/26/09: the definitions of the 2027 private car rating basis."),
    ("scale", "The no-claims step scale, private car, 2024 revision, with Step Protection."),
    ("guide", "Management Information: guide to the claims and policy extracts of 30 September 2026."),
    ("pol_legacy", "Legacy policy system: private car policy years incepting 1 January 2023 to 30 June 2025."),
    ("pol_platform", "Policy platform: private car policy years incepting 1 July 2025 to 30 September 2026."),
    ("crosswalk", "Legacy policy numbers and the platform numbers they renewed under."),
    ("mta", "Data warehouse: mid-term adjustments on both policy systems, 2023 to September 2026."),
    ("clm_legacy", "Legacy claims system: claims notified 1 January 2023 to 30 June 2025, as at 30 September 2026."),
    ("clm_platform", "Claims platform: claims notified 1 July 2025 to 30 September 2026."),
    ("glass", "%s: job file, jobs booked in 2025." % K.PARTNER),
    ("salvage", "%s: sale statements, 2025 and 2026 to September." % K.SALVAGE),
    ("regions", "The rating region map: postcode districts and regions, with effective dates."),
    ("industry", "Private Motor Statistics Service: national private car claims statistics, 2021 to 2025."),
    ("complaints", "Customer Relations: complaints received in 2025."),
]


def build(out, seed=W.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.world(seed)
    bk = BK.books(w, seed)
    n = {}
    n["pol_legacy"] = R.write_policy_legacy(p("pol_legacy"), bk)
    n["pol_platform"] = R.write_policy_platform(p("pol_platform"), bk)
    n["crosswalk"] = R.write_crosswalk(p("crosswalk"), bk)
    n["mta"] = R.write_mtas(p("mta"), bk)
    lines = R.glass_jobs(bk)
    n["glass"] = R.write_glass(p("glass"), lines)
    n["clm_legacy"] = R.write_claims_legacy(p("clm_legacy"), bk)
    n["clm_platform"] = R.write_claims_platform(p("clm_platform"), bk)
    n["salvage"] = R.write_salvage(p("salvage"), bk, w, seed)
    n["regions"] = R.write_region_map(p("regions"))
    n["industry"] = R.write_industry(p("industry"), seed)
    n["complaints"] = R.write_complaints(p("complaints"), bk, seed)
    DC.write_scale(p("scale"))
    DC.write_basis(p("basis"))
    DC.write_guide(p("guide"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w if keep else None, bk=bk if keep else None, counts=n)


DOC_DATES = {
    "scale": ("D:20231012143000+01'00'", "D:20231012143000+01'00'"),
    "basis": ("D:20260916101500+01'00'", "D:20260922164000+01'00'"),
    "guide": ("D:20261002111200+01'00'", "D:20261005152500+01'00'"),
}
OOXML = {
    "salvage": (K.SALVAGE, K.SALVAGE, "2025-01-31T17:05:00Z", "2026-09-30T16:48:00Z", "Sale statements"),
    "industry": ("Private Motor Statistics Service", "Private Motor Statistics Service", "2026-05-11T09:30:00Z",
                 "2026-05-14T08:02:00Z", "Private car claims statistics 2025"),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in DOC_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    for k, (cr, lb, c, m, title) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=True)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def metadata(fig, counts):
    return {
        "task": "task270",
        "title": "%s: the three rating regions in band C of the 2027 private car rating basis" % K.SOCIETY,
        "domain": "Actuarial Science & Insurance (claims frequency and severity)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["industry"], K.FILES["complaints"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); %s, %s, %s, the Private Motor "
                                        "Statistics Service and every person are fictional; postcode districts are "
                                        "real district codes used as labels only" % (K.SOCIETY, K.PARTNER, K.SALVAGE),
                              "date": "2026-10-05", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Band C: %s" % ", ".join(fig["call"]["band_names"]),
    }


def main_build(target, golden):
    import deliver as DV
    b = build(target, keep=True)
    finish(target)
    fig, res = DV.write(target, golden)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
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
    a = ap.parse_args()
    if a.out:
        build(a.out)
        finish(a.out)
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
