"""Build task399: the pack into <task>/target, generator/figures.json, the goldens into <task>/golden,
metadata.json and submission.md; then the checks, the independent verifier, a second full build compared byte for
byte, and target.zip cut from the final build.

    python3 task399/generator/build.py              everything
    python3 task399/generator/build.py --pack-only  the pack and figures.json only
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G  # noqa: E402
import pack as P    # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def cut(out, full=True):
    if os.path.isdir(out):
        shutil.rmtree(out)
    w = W.build_world()
    P.build_pack(w, out)
    figs = G.write_figures(w)
    if full:
        import deliver as DL
        DL.build_all(w, figs, TASK)
    return w, figs


def zip_target():
    z = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 11, 2, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    names = zipfile.ZipFile(z).namelist()
    assert names == sorted(os.listdir(TARGET)) and not any("/" in n for n in names), "H4 archive members"
    return hashlib.sha256(open(z, "rb").read()).hexdigest()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args(argv[1:])
    cut(TARGET, full=not a.pack_only)
    if a.pack_only:
        print("pack cut, digest", digest(TARGET)[:16])
        return 0
    d1 = digest(TARGET) + digest(os.path.join(TASK, "golden"))
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rv = subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    cut(TARGET, full=True)
    d2 = digest(TARGET) + digest(os.path.join(TASK, "golden"))
    same = d1 == d2
    print("two builds byte-identical:", same)
    zd = zip_target()
    print("target.zip sha256", zd[:16])
    return 0 if (rc == 0 and rv == 0 and same) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
