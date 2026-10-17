"""Build task267: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task267/generator/build.py              everything
    python3 task267/generator/build.py --out DIR    the pack only, into DIR
    python3 task267/generator/build.py --golden     the pack and the goldens, no checks"""
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
import askworld as AW      # noqa: E402
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2027, 1, 18, 11, 26)               # the data manager's export for the 2027 rule, Eastern time
MTIME = calendar.timegm((EXPORT + dt.timedelta(hours=5)).timetuple())


def world(seed=W.SEED):
    T = W.build(seed)
    T["assign"] = AW.assignments()
    T["use"] = AW.schedule(T)
    T["runlog"] = AW.runs(T, T["use"], T["assign"])
    T["runlog_db"], T["twice"] = AW.downloads(T["runlog"], T["assign"])
    T["lines"], T["billed"] = AW.billing(T)
    return T


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = world(seed)
    n = {}
    n["encounters"] = R.write_encounters(p("encounters"), T)
    n["ogtt"] = R.write_ogtt(p("ogtt"), T)
    n["rules"] = R.write_rules(p("rules"))
    n["closeout"] = R.write_closeout(p("closeout"), T)
    n["events"] = R.write_events(p("events"), T, T["use"])
    n["runlog"] = R.write_runlog(p("runlog"), T["runlog_db"])
    n["assets"] = R.write_assets(p("assets"), T["assign"])
    n["invoices"] = R.write_invoices(p("invoices"), T["lines"])
    n["feedback"] = R.write_feedback(p("feedback"), T)
    n["profile"] = R.write_profile(p("profile"))
    D.write_protocol(p("protocol"))
    D.write_notes(p("notes"))
    D.write_errors(p("errors"))
    from pypdf import PdfReader
    for k in ("protocol", "notes", "errors"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    D.write_manifest(p("manifest"), manifest(n))
    PP.COMPANY = K.ORG
    PP.normalize_ooxml(p("rules"), K.PEOPLE["data"], K.PEOPLE["data"], "2026-12-02T15:41:08Z", "2027-01-14T21:12:30Z",
                       excel=True)
    PP.normalize_ooxml(p("closeout"), K.PEOPLE["data"], K.PEOPLE["data"], "2027-01-16T14:05:52Z",
                       "2027-01-18T15:58:17Z", excel=True)
    PP.normalize_ooxml(p("assets"), "Biomedical Engineering", K.PEOPLE["data"], "2025-11-03T16:20:44Z",
                       "2026-12-04T19:37:01Z", excel=True)
    PP.normalize_ooxml(p("profile"), "Regional Public Health Office", "Regional Public Health Office",
                       "2025-09-09T13:12:55Z", "2025-09-22T17:44:39Z", excel=True)
    PP.normalize_pdf(p("protocol"), b"D:20260209101544-05'00'", b"D:20260209103012-05'00'")
    PP.normalize_pdf(p("notes"), b"D:20270114160931-05'00'", b"D:20270115092247-05'00'")
    PP.normalize_pdf(p("errors"), b"D:20250318083010-04'00'", b"D:20250318083010-04'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T["n"] = n
    return T


def manifest(n):
    F = K.FILES
    pg = lambda k: "%d page%s" % (n[k + "_pages"], "" if n[k + "_pages"] == 1 else "s")
    prog, lab = K.PROGRAM, K.LAB
    return [
        (F["protocol"], "Screening and referral protocol, 2026-27", "Medical Director, " + prog, "2026-02-09",
         pg("protocol")),
        (F["notes"], "Notes on the 2026 season extracts", "Data manager, " + prog, "2027-01-15", pg("notes")),
        (F["encounters"], "Screening encounters, 2 March to 20 November 2026, as synced from the tablets",
         "Data manager, " + prog, "2027-01-15", "%d rows" % n["encounters"]),
        (F["ogtt"], "OGTT results on program referrals collected by 15 January 2027 (pipe-delimited)", lab,
         "2027-01-15", "%d rows" % n["ogtt"]),
        (F["rules"], "Candidate referral rules for the 2027 season", "Medical Director, " + prog, "2027-01-14",
         "%d rules" % n["rules"]),
        (F["closeout"], "2026 season close-out report", "Data manager, " + prog, "2027-01-18", "3 sheets"),
        (F["events"], "Event calendar, 2026 season", "Program office, " + prog, "2026-11-20", "%d rows" % n["events"]),
        (F["runlog"], "GQ-200 analyzer runs held in the run database, 2026", "Biomedical Engineering",
         "2026-12-04", "%d rows" % n["runlog"]),
        (F["assets"], "Analyzer asset register", "Biomedical Engineering", "2026-12-04", "%d rows" % n["assets"]),
        (F["errors"], "GQ-200 error code quick reference (maker's document GQ-QR-07 rev C)", "Glyquant", "2025-03-18",
         pg("errors")),
        (F["invoices"], "Invoice and credit memo lines on the program's account, April 2026 to January 2027",
         lab + ", billing", "2027-01-06", "%d rows" % n["invoices"]),
        (F["feedback"], "Post-event feedback cards, 2026 season", "Program office, " + prog, "2026-11-30",
         "%d rows" % n["feedback"]),
        (F["profile"], "Community health assessment by service area, adults, 2024", "Regional public health office",
         "2025-09-22", "%d rows" % n["profile"]),
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
