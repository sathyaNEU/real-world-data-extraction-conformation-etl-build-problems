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
    ("rules", "Civil Service Commission: rules for the police officer entry examination, 2023 edition."),
    ("plan", "Personnel Research: the entry examination validation trial plan, approved with the 2023 rules."),
    ("calendar", "Civil Service Commission: police officer examination calendar, autumn 2023 to spring 2026."),
    ("roster", "Civil Service Commission: the 2024 and 2025 eligibility lists as certified, with each listed "
               "candidate's disposition."),
    ("crosswalk", "Civil Service Commission: candidate numbers with the Halvorsen and Pellwyn identifiers."),
    ("written", "Halvorsen Selection Systems: written test results, 2024 and 2025 examinations."),
    ("oral", "Oral board ratings, 2024 and 2025 examinations, one row a rating."),
    ("pat", "Physical ability test timing sheets, 2024 and 2025 examinations, one row a run of the course."),
    ("sjt", "Pellwyn Assessment Partners: situational judgement test trial scores, a sheet an examination."),
    ("inventory", "Halvorsen Selection Systems: work style inventory scale scores, 2024 and 2025 examinations."),
    ("academy", "Police Training Academy: gradebook, classes 24-2 to 26-2."),
    ("handbook", "Police Training Academy: recruit handbook, 2024."),
    ("ats_old", "Human Resources: the former applicant tracking system's export at its retirement on 3 February "
                "2025, police officer postings from January 2024."),
    ("ats_new", "Human Resources: applicant tracking system export, police officer requisitions, February to "
                "September 2025 (times in UTC)."),
    ("ledger", "Finance: general ledger lines on the examination cost centers 4410 to 4415, July 2023 to "
               "September 2026."),
    ("jobs", "Halvorsen Selection Systems: police officer job analysis, 2022."),
    ("campaign", "Recruitment Unit: 2025 recruitment campaign summary."),
]


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.world(seed)
    rows = w["rows"]
    R.numbers(rows, seed)
    n = {}
    n["roster"] = R.write_register(p("roster"), rows, seed)
    n["crosswalk"] = R.write_crosswalk(p("crosswalk"), rows)
    n["written"] = R.write_written(p("written"), rows)
    n["oral"] = R.write_oral(p("oral"), rows, w["panel_of"])
    n["pat"] = R.write_pat(p("pat"), rows, seed)
    n["sjt"] = R.write_sjt(p("sjt"), rows, seed)
    n["inventory"] = R.write_inventory(p("inventory"), rows, seed)
    n["academy"] = R.write_academy(p("academy"), rows, seed)
    n["ats_old"] = R.write_ats_legacy(p("ats_old"), w["legacy"])
    n["ats_new"] = R.write_ats_new(p("ats_new"), w["new"])
    n["ledger"] = R.write_ledger(p("ledger"), w["L"])
    n["calendar"] = R.write_calendar(p("calendar"))
    n["campaign"] = R.write_campaign(p("campaign"), seed)
    DC.write_rules(p("rules"))
    DC.write_plan(p("plan"))
    DC.write_handbook(p("handbook"))
    DC.write_job_analysis(p("jobs"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w, rows=rows, counts=n)


DOC_DATES = {
    "rules": ("D:20231114101500-05'00'", "D:20231114101500-05'00'"),
    "plan": ("D:20231108154200-05'00'", "D:20231114093000-05'00'"),
    "handbook": ("D:20240102083000-05'00'", "D:20240102083000-05'00'"),
    "jobs": ("D:20220318112000-04'00'", "D:20220318112000-04'00'"),
}
OOXML = {
    "sjt": ("Pellwyn Assessment Partners", "Pellwyn Assessment Partners", "2025-11-03T14:12:00Z",
            "2025-11-03T14:12:00Z", None),
    "academy": ("Kessling Police Training Academy", "Kessling Police Training Academy", "2024-07-05T12:40:00Z",
                "2026-09-04T19:22:00Z", "Academy gradebook"),
    "campaign": ("Recruitment Unit", "Recruitment Unit", "2025-01-09T15:02:00Z", "2025-09-12T20:31:00Z",
                 "2025 recruitment campaign"),
}


def finish(out):
    """The containers as the city's systems save them, then every file's modified time set to the pack's assembly."""
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
        "title": "Kessling Division of Police: the two components the 2027 entry examination keeps",
        "domain": "Psychology & Behavioral Science (psychometric measurement and scale validation)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["jobs"], K.FILES["campaign"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); Kessling, its Division of "
                                        "Police, Civil Service Commission and academy, Halvorsen Selection Systems, "
                                        "Pellwyn Assessment Partners and every person are fictional",
                              "date": "2026-10-06", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Keep the %s and the %s" % (fig["call"]["keep"][0].lower(), fig["call"]["keep"][1].lower()),
    }


def main_build(target, golden):
    import deliver as DV
    b = build(target)
    finish(target)
    fig, exact = DV.write(target, golden)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(golden, DV.WB), K.PEOPLE["analyst"], K.PEOPLE["analyst"],
                       "2026-10-05T14:10:00Z", "2026-10-06T19:02:00Z", title="2027 entry examination components",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, exact


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
    b, fig, exact = main_build(target, golden)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, exact)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    b2 = build(os.path.join(scratch, "target"))
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    same = d1 == d2
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
