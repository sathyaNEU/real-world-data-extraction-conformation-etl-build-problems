"""Build task482: the pack into <task>/target, the golden deliverable into <task>/golden, metadata.json,
submission.md and generator/figures.json; then the checks and the independent verifier, a second full build into a
scratch folder inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task482/generator/build.py              everything
    python3 task482/generator/build.py --out DIR    the pack only, into DIR
    python3 task482/generator/build.py --fast       one build with the checks, no second build or zip
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
AS_OF = {"log_old": "2026-08-03 07:40", "log_new": "2026-10-09 06:15", "open": "2026-10-09 06:20",
         "holidays": "2025-12-01 09:00", "pays": "2026-10-09 05:30", "batches": "2026-10-09 05:35",
         "paper": "2026-10-09 15:30", "staff": "2026-09-30 16:10", "survey": "2026-07-20 12:00",
         "dictionary": "2026-10-09 08:50", "manifest": "2026-10-09 08:55"}
LOCAL = dt.timezone(dt.timedelta(hours=1))


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or W.build()
    P.ids(x)
    n = {}
    n["log_old"] = P.write_csv(f("log_old"), P.OLD_COLS, P.log_rows(x, "old"))
    n["log_new"] = P.write_csv(f("log_new"), P.NEW_COLS, P.log_rows(x, "new"))
    n["open"] = P.write_csv(f("open"), P.OPEN_COLS, P.open_rows(x))
    n["holidays"] = P.write_csv(f("holidays"), P.HOL_COLS, P.holiday_rows())
    n["pays"] = P.write_csv(f("pays"), P.PAY_COLS, P.pay_rows(x))
    n["batches"] = P.write_csv(f("batches"), P.BATCH_COLS, P.batch_rows(x))
    n["survey"] = P.write_csv(f("survey"), P.SURVEY_COLS, P.survey_rows())
    DC.write_staff(f("staff"), x)
    PP.normalize_ooxml(f("staff"), "Jennifer Dyer", "Jennifer Dyer", "2026-09-28T13:20:00Z", "2026-09-30T15:10:00Z",
                       excel=True, company=P.COMPANY)
    DC.write_memo(f("paper"))
    PP.normalize_pdf(f("paper"), b"D:20261009142214+01'00'", b"D:20261009153002+01'00'")
    n["dictionary"] = P.write_csv(f("dictionary"), DC.DICT_COLS, DC.dictionary_rows())
    n["manifest"] = P.write_csv(f("manifest"), DC.MANIFEST_COLS, DC.manifest_rows(n))
    for k in P.FILES:
        t = dt.datetime.strptime(AS_OF[k], "%Y-%m-%d %H:%M").replace(tzinfo=LOCAL).timestamp()
        os.utime(f(k), (t, t))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(P.FILES), P.FILES[big], n[big]))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), LOCAL)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    if fast:
        if not good:
            raise SystemExit("checks failed")
        return
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {fn: open(os.path.join(TASK, fn), "rb").read() == open(os.path.join(tmp, fn), "rb").read()
                for fn in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            bad = [k for k, v in digest(os.path.join(TASK, "target")).items()
                   if digest(os.path.join(tmp, "target")).get(k) != v]
            badg = [k for k, v in digest(os.path.join(TASK, "golden")).items()
                    if digest(os.path.join(tmp, "golden")).get(k) != v]
            raise SystemExit("second build differs: target %s %s, golden %s %s, %s" % (same_t, bad, same_g, badg, same))
    finally:
        shutil.rmtree(tmp)
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, submission.md, figures.json" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not good:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main(fast=args.fast)
