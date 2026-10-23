"""Build task170: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build into
a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task170/generator/build.py              everything
    python3 task170/generator/build.py --out DIR    the pack only, into DIR"""
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
PULL_DONE = (2026, 10, 12, 16, 40, 0)                          # the pull's files assembled, local time (UTC+3)
MTIME = calendar.timegm((2026, 10, 12, 13, 40, 0, 0, 0, 0))    # the same moment, UTC


def build(out, quiet=False):
    n, Wd = PK.build_pack(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-48s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%s rows" % n[f]) if f in n else ""))
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    rows = build(target)
    import deliver
    import metadata
    deliver.deliver(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                    os.path.join(TASK, "submission.md"))
    metadata.write(TASK, target, rows)
    ok = True
    if not a.no_checks:
        r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target])
        r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
        ok = r1.returncode == 0 and r2.returncode == 0
    same = same_g = same_f = same_s = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="b170_", dir=TASK)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.deliver(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"),
                            os.path.join(tmp, "submission.md"))
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
            same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"), "rb").read()
            print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
        finally:
            shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, os.path.getsize(z), "bytes")
    sys.exit(0 if (ok and same and same_g and same_f and same_s) else 1)


if __name__ == "__main__":
    main()
