"""Build task265: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task265/generator/build.py              everything
    python3 task265/generator/build.py --out DIR    the pack only, into DIR
    python3 task265/generator/build.py --golden     the pack and the goldens, no checks"""
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
import ops as O            # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2027, 1, 27, 14, 6)                # the registry manager's evidence pack for the committee, CST
MTIME = calendar.timegm((EXPORT + dt.timedelta(hours=6)).timetuple())


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = W.world(seed)
    R.registry(T)
    R.revisions(T)
    R.deaths(T)
    O.or_record(T)
    O.choose_devices(T)
    O.other_cases(T)
    O.build_log(T)
    n = {}
    n["prosp"] = R.write_prospective(p("prosp"), T)
    n["legacy"] = R.write_legacy(p("legacy"), T)
    n["revisions"] = R.write_revisions(p("revisions"), T)
    n["deaths"] = R.write_deaths(p("deaths"), T)
    n["status"] = R.write_status(p("status"), T)
    R.write_crosswalk(p("crosswalk"))
    n["visits"] = R.write_visits(p("visits"), T)
    n["implants"] = O.write_log(p("implants"), T)
    n["cases"] = O.write_cases(p("cases"), T)
    n["merges"] = O.write_merges(p("merges"), T)
    D.write_policy(p("policy"))
    D.write_dictionary(p("dictionary"))
    D.write_schedule(p("schedule"))
    D.write_log(p("log"), T)
    from pypdf import PdfReader
    for k in ("policy", "dictionary", "schedule"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    D.write_manifest(p("manifest"), manifest(n))
    PP.COMPANY = K.SYSTEM
    PP.normalize_ooxml(p("legacy"), K.PEOPLE["registry"], K.PEOPLE["registry"], "2018-01-12T15:20:41Z",
                       "2022-01-06T17:02:13Z", excel=True)
    PP.normalize_ooxml(p("crosswalk"), K.PEOPLE["registry"], K.PEOPLE["registry"], "2018-01-03T14:11:09Z",
                       "2025-09-17T19:40:52Z", excel=True)
    PP.normalize_ooxml(p("log"), K.PEOPLE["registry"], K.PEOPLE["registry"], "2018-01-02T16:05:30Z",
                       "2027-01-25T21:48:16Z", excel=True)
    PP.normalize_ooxml(p("cases"), "Perioperative Informatics", "Perioperative Informatics", "2027-01-08T14:31:02Z",
                       "2027-01-08T14:33:47Z", excel=True)
    PP.normalize_pdf(p("policy"), b"D:20250211160418-06'00'", b"D:20250213093102-06'00'")
    PP.normalize_pdf(p("dictionary"), b"D:20270112101507-06'00'", b"D:20270126155921-06'00'")
    PP.normalize_pdf(p("schedule"), b"D:20250623112744-05'00'", b"D:20250701083016-05'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["n"] = n
    return T


def manifest(n):
    F = K.FILES
    return [
        (F["policy"], "Implant Value Analysis Policy VA-07, revision 3", "Supply Chain, Value Analysis", "13 February 2025",
         "%d pages" % n["policy_pages"]),
        (F["dictionary"], "Registry data dictionary for the annual extract, version 4.2", K.REGISTRY, "26 January 2027",
         "%d pages" % n["dictionary_pages"]),
        (F["prosp"], "Registry extract of 31 December 2026: hips captured from 1 January 2018", K.REGISTRY,
         "26 January 2027", n["prosp"]),
        (F["legacy"], "Registry legacy enrolment workbook, 2018 to 2021", K.REGISTRY, "6 January 2022", n["legacy"]),
        (F["revisions"], "Registry extract of 31 December 2026: revisions of registry hips", K.REGISTRY,
         "26 January 2027", n["revisions"]),
        (F["deaths"], "Wisconsin death index linkage for registry patients, deaths to 31 December 2026", K.REGISTRY,
         "22 January 2027", n["deaths"]),
        (F["status"], "Registry patients' residence at 31 December 2026 from the health record's address history",
         K.REGISTRY, "26 January 2027", n["status"]),
        (F["crosswalk"], "Hip component catalogue crosswalk", K.REGISTRY, "17 September 2025", "2 sheets"),
        (F["visits"], "Registry clinic visits, 2018 to 2026", K.REGISTRY, "26 January 2027", n["visits"]),
        (F["log"], "Registry data-management log", K.REGISTRY, "25 January 2027", "1 sheet"),
        (F["cases"], "Orthopaedic and spine cases with implants, 2026, all three hospitals", "Perioperative Informatics",
         "8 January 2027", n["cases"]),
        (F["implants"], "Perioperative implant documentation for 2026 cases, all three hospitals",
         "Perioperative Informatics", "8 January 2027", n["implants"]),
        (F["merges"], "Medical record numbers merged in 2026", "Health Information Management", "5 January 2027",
         n["merges"]),
        (F["schedule"], "Hip agreement 2022 to 2027, Schedule B (pricing), as amended 1 July 2025", "Supply Chain",
         "1 July 2025", "%d pages" % n["schedule_pages"]),
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
