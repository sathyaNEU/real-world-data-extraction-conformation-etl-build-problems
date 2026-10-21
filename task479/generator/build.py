"""Build task479: the pack into <task>/target, the golden deliverable into <task>/golden, metadata.json,
submission.md and generator/figures.json; then the checks and the independent verifier, a second full build into a
scratch folder inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task479/generator/build.py              everything
    python3 task479/generator/build.py --out DIR    the pack only, into DIR
    python3 task479/generator/build.py --fast       one build with the checks, no second build or zip
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
LOCAL = dt.timezone(dt.timedelta(hours=-5))
AS_OF = {"legacy": "2022-04-04 10:12", "current": "2026-10-02 06:41", "register": "2026-10-02 06:44",
         "xwalk": "2022-04-01 16:20", "rates": "2026-07-01 09:05", "visitor": "2025-11-18 14:30",
         "method": "2026-02-12 11:48", "program": "2026-09-17 09:41", "dictionary": "2026-10-02 11:02",
         "manifest": "2026-10-02 11:06"}
for _y, (_a, _b, _c) in P.DOR_ISSUED.items():
    AS_OF["dor%d" % _y] = "%d-%02d-%02d 10:00" % (_a, _b, _c)


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or W.build()
    P.names(x)
    n = {}
    n["legacy"] = P.write_csv(f("legacy"), P.LEGACY_COLS, P.legacy_rows(x))
    n["current"] = P.write_csv(f("current"), P.CURRENT_COLS, P.current_rows(x))
    n["register"] = P.write_csv(f("register"), P.REGISTER_COLS, P.register_rows(x))
    n["xwalk"] = P.write_csv(f("xwalk"), P.XWALK_COLS, P.xwalk_rows(x))
    n["rates"] = P.write_csv(f("rates"), P.RATES_COLS, P.rates_rows())
    n["visitor"] = P.write_csv(f("visitor"), P.VISITOR_COLS, P.visitor_rows(x))
    for y in W.BENCH:
        DC.write_dor(f("dor%d" % y), x, y)
        iy, im, iday = P.DOR_ISSUED[y]
        PP.normalize_pdf(f("dor%d" % y), ("D:%d%02d%02d093000-05'00'" % (iy, im, iday - 1)).encode(),
                         ("D:%d%02d%02d100000-05'00'" % (iy, im, iday)).encode())
    DC.write_method(f("method"))
    PP.normalize_pdf(f("method"), b"D:20260211160412-05'00'", b"D:20260212114802-05'00'")
    DC.write_program(f("program"))
    PP.normalize_ooxml(f("program"), "Samantha Walter", "Samantha Walter", "2026-09-16T20:02:00Z",
                       "2026-09-17T14:41:00Z", excel=False, company=P.COMPANY)
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
