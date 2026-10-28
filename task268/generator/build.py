"""Build task268: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task268/generator/build.py              everything
    python3 task268/generator/build.py --out DIR    the pack only, into DIR
    python3 task268/generator/build.py --golden     the pack and the goldens, no checks"""
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
import docs as DC          # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2026, 4, 14, 16, 42)             # the committee pack, assembled by the outcomes team
MTIME = calendar.timegm(EXPORT.timetuple())


def build(out, seed=W.SEED):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.build(seed)
    n = {}
    n["patients"] = R.write_patients(p("patients"), w)
    n["visits"] = R.write_visits(p("visits"), w)
    n["events"] = R.write_events(p("events"), w)
    n["fl_deaths"] = R.write_fl_deaths(p("fl_deaths"), w)
    n["exchange"] = R.write_exchange(p("exchange"), w)
    n["crosswalk"] = R.write_crosswalk(p("crosswalk"), w)
    n["hospitals"] = R.write_hospitals(p("hospitals"))
    n["lab"] = R.write_lab(p("lab"), w)
    n["echo"] = R.write_echo(p("echo"), w)
    n["clinics"] = R.write_clinics(p("clinics"), w)
    DC.write_charter(p("charter"))
    DC.write_manual(p("manual"))
    from pypdf import PdfReader
    for k in ("charter", "manual"):
        n[k + "_pages"] = len(PdfReader(p(k)).pages)
    DC.write_contents(p("contents"), contents(n))
    PP.COMPANY = K.ORG_INC
    PP.normalize_ooxml(p("fl_deaths"), "Bureau of Vital Statistics", "Bureau of Vital Statistics", "2026-03-06T14:02:51Z",
                       "2026-03-06T14:09:37Z", excel=True)
    PP.normalize_ooxml(p("hospitals"), "Registry team", K.PEOPLE["epi"], "2021-09-14T15:31:08Z", "2024-07-02T13:47:20Z",
                       excel=True)
    PP.normalize_ooxml(p("echo"), "Cardiac imaging", "Cardiac imaging", "2026-01-12T16:20:44Z", "2026-01-12T16:26:03Z",
                       excel=True)
    PP.normalize_pdf(p("charter"), b"D:20260217163314-05'00'", b"D:20260218091127-05'00'")
    PP.normalize_pdf(p("manual"), b"D:20250303104406-05'00'", b"D:20250303112952-05'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    w["n"] = n
    return w


def contents(n):
    F = K.FILES
    pg = lambda k: "%d pages" % n[k + "_pages"] if n[k + "_pages"] != 1 else "1 page"
    rw = lambda k: "{:,} rows".format(n[k])
    return [
        ["File", "What it holds", "Kept by", "As at", "Size"],
        [F["charter"], "Heart Failure Early Diagnosis Programme 2027: charter", "Service line committee", "2026-02-17",
         pg("charter")],
        [F["patients"], "Registry enrolments, January 2022 to March 2026", "HF registry team", "2026-03-31", rw("patients")],
        [F["visits"], "Heart failure clinic visits of enrolled patients", "HF registry team", "2026-03-31", rw("visits")],
        [F["events"], "Relocations and consent withdrawals", "HF registry team", "2026-03-31", rw("events")],
        [F["manual"], "Heart failure registry manual, version 5", "HF registry team", "2025-03-03", pg("manual")],
        [F["fl_deaths"], "Florida death certificate linkage, March 2026 run", "Bureau of Vital Statistics", "2026-03-06",
         rw("fl_deaths")],
        [F["exchange"], "Deaths returned by the Tri-State exchange", "Vital records exchange", "2026-03-12", rw("exchange")],
        [F["crosswalk"], "Legacy to new medical record numbers", "Health information management", "2024-06-01",
         rw("crosswalk")],
        [F["hospitals"], "Hospital and campus codes", "HF registry team", "2024-07-02", "%d codes" % n["hospitals"]],
        [F["lab"], "NT-proBNP results released 1 January 2025 to 6 January 2026", "Laboratory information system",
         "2026-01-07", rw("lab")],
        [F["echo"], "Echocardiography studies by month, 2025", "Cardiac imaging", "2026-01-12", "%d rows" % n["echo"]],
        [F["clinics"], "Heart failure clinic sessions, 2026 timetable", "Clinic operations", "2026-01-05", rw("clinics")],
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
        w = build(a.out, a.seed)
        print("pack:", w["n"])
        return
    target = os.path.join(TASK, "target")
    w = build(target)
    print("pack:", w["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), w)
    if a.golden:
        return
    import checks
    checks.run(target, w)
    r = os.system("python3 %s %s %s" % (os.path.join(HERE, "verify.py"), target, os.path.join(TASK, "golden")))
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
            zi = zipfile.ZipInfo(f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
