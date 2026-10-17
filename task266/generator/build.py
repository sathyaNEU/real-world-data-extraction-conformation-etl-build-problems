"""Build task266: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task266/generator/build.py              everything
    python3 task266/generator/build.py --out DIR    the pack only, into DIR
    python3 task266/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as D           # noqa: E402
import population as PO    # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import term26 as T26       # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2027, 5, 28, 16, 42)               # the registrar's extracts for the June 2027 review, EDT
MTIME = calendar.timegm((EXPORT + dt.timedelta(hours=4)).timetuple())


def world(seed=W.SEED):
    T = PO.build(seed)
    PO.stamp(T, seed)
    T26.build(T, seed)
    return T


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = world(seed)
    n = {}
    n["cohorts"] = R.write_cohorts(p("cohorts"), T)
    n["admissions"] = R.write_admissions(p("admissions"), T)
    n["conferrals"] = R.write_conferrals(p("conferrals"), T)
    n["idmap"] = R.write_idmap(p("idmap"), T)
    n["terms"] = R.write_terms(p("terms"))
    n["history"] = R.write_history(p("history"), T)
    n["registrations"] = R.write_registrations(p("registrations"), T)
    n["schedule"] = R.write_schedule(p("schedule"), T)
    n["register"] = R.write_register(p("register"))
    n["success"] = R.write_success(p("success"))
    n["outlook"] = R.write_outlook(p("outlook"))
    D.write_policy(p("policy"))
    D.write_notes(p("notes"))
    from pypdf import PdfReader
    for k in ("policy", "notes"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    D.write_manifest(p("manifest"), manifest(n))
    PP.COMPANY = K.COLLEGE
    PP.normalize_ooxml(p("cohorts"), K.PEOPLE["ir"], K.PEOPLE["ir"], "2023-09-21T14:12:07Z", "2025-09-19T19:03:44Z",
                       excel=True)
    PP.normalize_ooxml(p("terms"), "Office of the Registrar", "Office of the Registrar", "2019-03-04T15:20:11Z",
                       "2026-11-30T16:48:02Z", excel=True)
    PP.normalize_ooxml(p("schedule"), "Office of the Registrar", "Office of the Registrar", "2027-05-28T20:31:45Z",
                       "2027-05-28T20:31:45Z", excel=True)
    PP.normalize_ooxml(p("register"), "Academic Affairs", "Academic Affairs", "2019-06-03T13:40:28Z",
                       "2026-08-14T18:22:51Z", excel=True)
    PP.normalize_ooxml(p("success"), K.PEOPLE["ir"], K.PEOPLE["ir"], "2022-06-27T15:02:39Z", "2026-06-12T13:55:20Z",
                       excel=True)
    PP.normalize_pdf(p("policy"), b"D:20250610143115-04'00'", b"D:20250611090412-04'00'")
    PP.normalize_pdf(p("notes"), b"D:20270527153840-04'00'", b"D:20270528162209-04'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["n"] = n
    return T


def manifest(n):
    F = K.FILES
    reg, ir = "Office of the Registrar", "Office of Institutional Research"
    return [
        (F["policy"], "Board Policy 3.12, Academic Program Review, revised 10 June 2025", "Academic Affairs",
         "2025-06-11", "%d pages" % n["policy_pages"]),
        (F["notes"], "Notes on the registrar's extracts for the June 2027 review", reg, "2027-05-28",
         "%d pages" % n["notes_pages"]),
        (F["cohorts"], "Fall entering-student files, fall 2023, fall 2024 and fall 2025, each frozen at its census", ir,
         "2025-09-19", "%d rows, 3 sheets" % n["cohorts"]),
        (F["admissions"], "Admissions with an admit term from fall 2023 to spring 2027, with exits", reg, "2027-05-28",
         "%d rows" % n["admissions"]),
        (F["conferrals"], "Associate degrees conferred, December 2023 to May 2027", reg, "2027-05-28",
         "%d rows" % n["conferrals"]),
        (F["idmap"], "Student-number map from the 2024 conversion (pipe-delimited)", reg, "2024-07-13",
         "%d rows" % n["idmap"]),
        (F["terms"], "Term calendar with current and legacy term codes", reg, "2026-11-30", "%d rows" % n["terms"]),
        (F["registrations"], "Fall 2026 registrations, every status", reg, "2027-05-28", "%d rows" % n["registrations"]),
        (F["history"], "Program-of-record history, periods in effect from fall 2023 to spring 2027", reg, "2027-05-28",
         "%d rows" % n["history"]),
        (F["schedule"], "Fall 2026 section schedule", reg, "2027-05-28", "%d rows" % n["schedule"]),
        (F["register"], "Program register, 2026-27, with the course subjects each program owns", "Academic Affairs",
         "2026-08-14", "%d programs, 2 sheets" % n["register"]),
        (F["success"], "Course success rates by subject, fall 2021 to spring 2026", ir, "2026-06-12",
         "%d rows" % n["success"]),
        (F["outlook"], "Occupational outlook for the college's service area, 2024 to 2034 (Workforce Development "
         "planning extract)", "Workforce Development", "2026-02-20", "%d rows" % n["outlook"]),
    ]


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=W.SEED)
    a = ap.parse_args()
    if a.out:
        build(a.out, a.seed)
        return
    target = os.path.join(TASK, "target")
    T = build(target)
    print("pack:", T["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
