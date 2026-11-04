"""Build task462: the pack into <task>/target, the goldens into <task>/golden, metadata.json, generator/figures.json and
submission.md; then the checks, the independent verifier, a second full build in a scratch folder compared byte for
byte, and target.zip cut last.

    python3 task462/generator/build.py              everything
    python3 task462/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import hashlib
import os
import shutil
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import ops as O      # noqa: E402
import pack as PK    # noqa: E402
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = W.STAMP


def build(out, x=None):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or O.simulate()
    n = PK.write_data(out, x)
    DC.write_procedure(f("procedure"))
    DC.write_accounting(f("accounting"))
    DC.write_control(f("control"))
    DC.write_plan(f("plan"))
    PP.normalize_ooxml(f("plan"), W.FUEL_MANAGER, W.FUEL_MANAGER, "2026-11-30T13:05:00Z", "2026-12-09T14:22:00Z",
                       excel=True, company=W.ORG)
    PP.normalize_pdf(f("procedure"), b"D:20260311101500+02'00'", b"D:20260311101500+02'00'")
    PP.normalize_pdf(f("accounting"), b"D:20250120094000+02'00'", b"D:20250120094000+02'00'")
    PP.normalize_pdf(f("control"), b"D:20260703150500+03'00'", b"D:20260703150500+03'00'")
    import time
    ts = time.mktime(STAMP + (0, 0, -1))
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    import writeup as WU
    n, x = build(os.path.join(root, "target"))
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    DL.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x, n


def main():
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x, n = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x, n=n,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {f: open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
                for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
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
