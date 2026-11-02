"""Build task483: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task483/generator/build.py              everything
    python3 task483/generator/build.py --out DIR    the pack only, into DIR
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

import pack as P      # noqa: E402
import records as R   # noqa: E402

TASK = os.path.dirname(HERE)
UK = dt.timezone(dt.timedelta(hours=0))
STAMP = dt.datetime(2027, 1, 11, 15, 26, tzinfo=UK)       # the folder as the stewardship lead assembled it


def world():
    return R.build()


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or world()
    n = P.write_all(out, x)
    DC.write_spec(f("spec"))
    PP.normalize_ooxml(f("register"), "Business Office", "Business Office", "2023-04-03T09:20:00Z",
                       "2027-01-08T10:14:52Z", excel=True)
    PP.normalize_ooxml(f("codelists"), "Josephine James", "Josephine James", "2026-10-29T14:02:00Z",
                       "2026-12-03T11:37:09Z", excel=True)
    PP.normalize_ooxml(f("icb"), "Medicines Optimisation", "Medicines Optimisation", "2025-07-09T08:45:00Z",
                       "2026-05-14T07:58:40Z", excel=True, company="Hollinbrook Integrated Care Board")
    PP.normalize_pdf(f("spec"), b"D:20261203113200+00'00'", b"D:20261203113200+00'00'")
    stamps = {"cultures": dt.datetime(2027, 1, 6, 9, 12), "issues": dt.datetime(2027, 1, 7, 16, 41),
              "register": dt.datetime(2027, 1, 8, 10, 14), "codelists": dt.datetime(2026, 12, 3, 11, 37),
              "organisms": dt.datetime(2026, 9, 7, 7, 55), "antimicrobials": dt.datetime(2026, 9, 7, 7, 56),
              "spec": dt.datetime(2026, 12, 3, 11, 32), "icb": dt.datetime(2026, 5, 14, 7, 58),
              "cdiff": dt.datetime(2027, 1, 5, 14, 3), "lists": dt.datetime(2026, 11, 13, 9, 30)}
    for k in P.FILES:
        ts = stamps[k].replace(tzinfo=UK).timestamp()
        os.utime(f(k), (ts, ts))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 1, 11, 15, 26, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import golden as GO
    import metadata as MD
    import postprocess as PP
    import writeup as WU
    n, x = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    PP.normalize_ooxml(os.path.join(gdir, GO.GOLDEN["workbook"]), "Josephine James", "Josephine James",
                       "2027-01-11T09:40:00Z", "2027-01-13T16:22:47Z", excel=False)
    PP.normalize_ooxml(os.path.join(gdir, GO.GOLDEN["note"]), "Josephine James", "Josephine James",
                       "2027-01-12T14:05:00Z", "2027-01-13T16:31:10Z", title="UTI pathway placement 2027-28")
    ts = dt.datetime(2027, 1, 13, 16, 32, tzinfo=UK).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x


def main():
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
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
            raise SystemExit("second build differs: target %s %s, golden %s, %s" % (same_t, bad, same_g, same))
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
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main()
