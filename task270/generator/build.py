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
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("paper", "Research Committee paper RC/26/11: recruiting sites for ARV-1102 (for decision, 21 October 2026)."),
    ("questionnaire", "%s: %s site feasibility questionnaire, version 2.0." % (K.SPONSOR, K.TRIAL)),
    ("guide", "Information team: guide to the Memory Assessment Service extracts, 6 October 2026."),
    ("cis_ace", "CIS archive: ACE-III forms, April 2014 to 5 January 2024."),
    ("cis_dx", "CIS archive: diagnoses recorded, April 2014 to 5 January 2024."),
    ("epr_obs", "EPR: ACE-III observations, 8 January 2024 to 2 October 2026."),
    ("epr_dx", "EPR: problem list entries for the Memory Assessment Service's patients."),
    ("episodes", "EPR: Memory Assessment Service episodes open on or after 8 January 2024."),
    ("appts", "EPR: Memory Assessment Service outpatient appointments from 8 January 2024."),
    ("pmi", "Master patient index: hospital patient numbers, NHS numbers, dates of birth and death."),
    ("tracker", "Memory Assessment Service pathway tracker, referrals from 8 January 2024."),
    ("clinics", "Memory Assessment Service clinic register, with the postcode districts each clinic serves."),
    ("audit", "Memory Assessment Service annual audit for the commissioners, 2024-25."),
    ("population", "Planning team: residents aged 65 and over by postcode district, mid-2025."),
]


def build(out, seed=W.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.world(seed)
    R.derive(w)
    n = {}
    n["pmi"] = R.write_pmi(p("pmi"), w)
    n["cis_ace"] = R.write_cis_ace(p("cis_ace"), w)
    n["cis_dx"] = R.write_cis_dx(p("cis_dx"), w)
    n["epr_obs"] = R.write_epr_obs(p("epr_obs"), w)
    n["epr_dx"] = R.write_epr_dx(p("epr_dx"), w)
    n["episodes"] = R.write_episodes(p("episodes"), w)
    n["appts"] = R.write_appointments(p("appts"), w)
    n["tracker"] = R.write_tracker(p("tracker"), w)
    n["clinics"] = R.write_clinics(p("clinics"))
    n["audit"] = R.write_audit(p("audit"), w)
    n["population"] = R.write_population(p("population"), w["seed"])
    DC.write_paper(p("paper"))
    DC.write_questionnaire(p("questionnaire"))
    DC.write_guide(p("guide"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w if keep else None, counts=n)


DOC_DATES = {
    "paper": ("D:20261007154200+01'00'", "D:20261008093500+01'00'"),
    "questionnaire": ("D:20260918110500+01'00'", "D:20260921142000+01'00'"),
    "guide": ("D:20261005160800+01'00'", "D:20261006121500+01'00'"),
}
OOXML = {
    "clinics": ("Information team", "Information team", "2019-04-02T09:12:00Z", "2026-10-02T10:41:00Z",
                "Memory Assessment Service clinic register"),
    "tracker": ("Information team", "Information team", "2024-02-05T08:30:00Z", "2026-10-02T07:05:00Z",
                "MAS pathway tracker"),
    "audit": ("Information team", "Information team", "2025-04-28T13:20:00Z", "2025-05-16T11:02:00Z",
              "MAS annual audit 2024-25"),
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
        "title": "%s: the two memory clinics that recruit for %s" % (K.TRUST, K.TRIAL),
        "domain": "Psychology & Behavioral Science (longitudinal growth curve modelling)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["audit"], K.FILES["population"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); %s, its clinics, %s, %s and every "
                                        "person are fictional; NHS numbers are drawn from a range the NHS does not "
                                        "issue" % (K.TRUST, K.SPONSOR, K.TRIAL),
                              "date": "2026-10-09", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Recruiting sites: %s and %s" % (fig["call"]["sites"][0], fig["call"]["sites"][1]),
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
