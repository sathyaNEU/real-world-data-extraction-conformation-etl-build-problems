"""Build task476 (architecture 4): the pack into <task>/target, the golden into <task>/golden, metadata.json and
generator/figures.json; then the checks and the verifier, a second build compared byte for byte, and target.zip.

    python3 task476/generator/build.py            everything
    python3 task476/generator/build.py --fast     one build with the checks, no second build or zip
"""
import argparse
import hashlib
import os
import shutil
import sys
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P    # noqa: E402
import sim as S     # noqa: E402

TASK = os.path.dirname(HERE)
ZIP_STAMP = (2026, 10, 1, 9, 0, 0)


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def cut(task_dir, fig_path):
    x = S.simulate()
    n = P.build_pack(os.path.join(task_dir, "target"), x)
    import golden as GD
    import metadata as MD
    import postprocess as PP
    g = GD.build(os.path.join(task_dir, "target"), os.path.join(task_dir, "golden"), fig_path)
    pdf = os.path.join(task_dir, "golden", "salvage_marking_2027.pdf")
    PP.normalize_pdf(pdf, b"D:20261104081512-08'00'", b"D:20261104081512-08'00'")
    MD.write(os.path.join(task_dir, "metadata.json"), n)
    return x, n, g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    x, n, g = cut(TASK, os.path.join(HERE, "figures.json"))
    tgt = os.path.join(TASK, "target")
    files = sorted(digest(tgt))
    print("pack: %d files, largest table %d rows" % (len(files), max(n.values())))
    import checks as C
    ok = C.main(tgt, os.path.join(TASK, "golden"), x)
    import verify as V
    ok = V.main(tgt, os.path.join(TASK, "golden")) and ok
    if a.fast:
        return 0 if ok else 1
    scratch = os.path.join(TASK, ".rebuild")
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    cut(scratch, os.path.join(scratch, "figures.json"))
    same = digest(tgt) == digest(os.path.join(scratch, "target")) and \
        digest(os.path.join(TASK, "golden")) == digest(os.path.join(scratch, "golden")) and \
        open(os.path.join(TASK, "metadata.json"), "rb").read() == open(os.path.join(scratch, "metadata.json"), "rb").read() and \
        open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(scratch, "figures.json"), "rb").read()
    shutil.rmtree(scratch)
    print("two builds byte-identical: %s" % same)
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in files:
            zi = zipfile.ZipInfo(rel, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(tgt, rel), "rb").read())
    print("target.zip cut from this build: %d files (sha256 %s)" % (
        len(files), hashlib.sha256(open(zp, "rb").read()).hexdigest()))
    return 0 if ok and same else 1


if __name__ == "__main__":
    sys.exit(main())
