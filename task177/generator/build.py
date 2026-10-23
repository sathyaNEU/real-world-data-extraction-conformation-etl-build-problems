"""Build task177: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build into
a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task177/generator/build.py              everything
    python3 task177/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2027, 1, 22, 18, 30, 0)                           # the pull assembled, local time
MTIME = calendar.timegm((2027, 1, 22, 23, 30, 0, 0, 0, 0))     # the same moment, UTC (local UTC-5)


def build(out, quiet=False):
    n = PK.build_pack(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-48s %11d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if f in n else ""))
    return n


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip(root):
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=PULL_DONE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def full(root):
    """pack, goldens, figures.json, submission.md and metadata.json under root"""
    import deliver
    import metadata
    target = os.path.join(root, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    build(target, quiet=root != TASK)
    gen = os.path.join(root, "generator") if root != TASK else HERE
    os.makedirs(gen, exist_ok=True)
    deliver.main(target, os.path.join(root, "golden"), os.path.join(gen, "figures.json"), os.path.join(root, "submission.md"))
    metadata.write(root)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--into")
    ap.add_argument("--pack-only", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--no-checks", action="store_true")
    ap.add_argument("--skip-build", action="store_true", help="check, rebuild and zip the build already on disk")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    if a.into:
        full(a.into)
        return
    if not a.skip_build:
        full(TASK)
    target = os.path.join(TASK, "target")
    if a.pack_only:
        return
    if not a.no_checks:
        r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target])
        r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
        if r1.returncode or r2.returncode:
            sys.exit("checks %d verify %d" % (r1.returncode, r2.returncode))
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="t177v3_rebuild_", dir=os.environ.get("REBUILD_DIR"))
        try:
            subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "--into", tmp], check=True)
            mine = {k: v for k, v in digest(TASK).items() if k.split(os.sep)[0] in ("target", "golden")
                    or k in ("submission.md", "metadata.json", os.path.join("generator", "figures.json"))}
            theirs = digest(tmp)
            diff = [k for k in mine if mine[k] != theirs.get(k)]
            print("rebuild: %d files compared, %d differ%s" % (len(mine), len(diff), (": " + ", ".join(diff)) if diff else ""))
            if diff:
                sys.exit(1)
        finally:
            shutil.rmtree(tmp)
    print("zip:", cut_zip(TASK))


if __name__ == "__main__":
    main()
