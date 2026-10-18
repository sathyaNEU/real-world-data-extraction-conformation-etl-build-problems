"""Build task164: the clean truth, the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build into
a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task164/generator/build.py                 everything
    python3 task164/generator/build.py --out DIR       the pack only, into DIR (truth built fresh)
    python3 task164/generator/build.py --no-rebuild    skip the second build"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import pickle
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK   # noqa: E402
import truth        # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2027, 4, 5, 16, 52, 0)                          # the pull, Pacific daylight time
MTIME = calendar.timegm((2027, 4, 5, 23, 52, 0, 0, 0, 0))    # the same moment, UTC
SCRATCH = os.environ.get("T164_SCRATCH", "/tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/"
                                         "98ff0d30-fbdb-590b-8f7a-decafc622b0e/scratchpad/b164")


def build(out, quiet=False):
    T = truth.build(verbose=not quiet)
    B = PK.Bundle(T)
    n = PK.build_pack(out, B)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-46s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if f in n else ""))
    return T, B, n


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
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    T, B, n = build(target)
    with open(truth.CACHE, "wb") as fh:        # for checks.py; generator/.truth.pkl is never committed
        pickle.dump(T, fh)
    import deliver
    import metadata
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    metadata.write(TASK)
    env = dict(os.environ, T164_CACHE="1")
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")], env=env)
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = same_g = same_f = same_s = True
    if not a.no_rebuild:
        os.makedirs(SCRATCH, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix="rebuild_", dir=SCRATCH)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"),
                         os.path.join(tmp, "submission.md"))
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
            same_s = open(os.path.join(TASK, "submission.md"), "rb").read() == open(os.path.join(tmp, "submission.md"), "rb").read()
            if not same:
                d1, d2 = digest(target), digest(os.path.join(tmp, "target"))
                print("differs:", sorted(k for k in d1 if d1.get(k) != d2.get(k)))
            print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s" % (same, same_g, same_f, same_s))
        finally:
            shutil.rmtree(tmp)
    z = cut_zip(TASK)
    print("zip", z, os.path.getsize(z), "bytes")
    ok = r1.returncode == 0 and r2.returncode == 0 and same and same_g and same_f and same_s
    print("BUILD %s" % ("GREEN" if ok else "RED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
