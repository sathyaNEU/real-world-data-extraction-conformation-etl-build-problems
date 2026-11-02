"""Build task271: the evidence pack into <task>/target, the goldens into <task>/golden, generator/figures.json,
submission.md and metadata.json, then the checks and the independent verifier, then a second full build into a scratch
folder compared byte for byte, then target.zip cut from the pack.

    python3 task271/generator/build.py              everything
    python3 task271/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D            # noqa: E402
import pack as P            # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = time.mktime((2026, 10, 26, 9, 15, 0, 0, 0, -1))   # the stocking program manager's working morning


def build(out, quiet=False, X=None):
    os.makedirs(out, exist_ok=True)
    X = X or W.simulate()
    n = P.write_all(out, X)
    D.write_all(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-46s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
                                             ("%d rows" % n[f]) if f in n else ""))
    return X, n


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
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 26, 9, 15, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def deliver_into(target, root, figures, submission):
    import deliver
    return deliver.main(target, os.path.join(root, "golden"), figures, submission)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    build(target)
    deliver_into(target, TASK, os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK)
    rc = 0
    if not a.no_checks:
        rc |= subprocess.run([sys.executable, os.path.join(HERE, "checks.py")]).returncode
        rc |= subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target]).returncode
    tmp = tempfile.mkdtemp(prefix="b271_")
    try:
        build(os.path.join(tmp, "target"), quiet=True)
        deliver_into(os.path.join(tmp, "target"), tmp, os.path.join(tmp, "figures.json"),
                     os.path.join(tmp, "submission.md"))
        same = digest(target) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
        same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"), "rb").read()
        print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
    finally:
        shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    if rc or not (same and same_g and same_f and same_s):
        sys.exit(1)


if __name__ == "__main__":
    main()
