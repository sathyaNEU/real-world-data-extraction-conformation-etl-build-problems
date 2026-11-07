"""task165 architecture 2: the whole build. The pack into <task>/target, the goldens into <task>/golden,
metadata.json, generator/figures.json and submission.md; then the checks and the independent verifier; then a second
full build into a scratch folder compared byte for byte (and deleted); then target.zip cut from the pack.

    python3 task165/generator/make.py            everything
    python3 task165/generator/make.py --no-rebuild"""
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
import build as B     # noqa: E402
import deliver        # noqa: E402
import metadata       # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2026, 1, 16, 9, 40, 0)
MTIME = calendar.timegm((2026, 1, 16, 14, 40, 0, 0, 0, 0))


def stamp(folder):
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (MTIME, MTIME))


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            fp = os.path.join(root, f)
            h[os.path.relpath(fp, folder)] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    return h


def cut_zip():
    target = os.path.join(TASK, "target")
    zpath = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=PULL_DONE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def full(root, quiet=False):
    target = os.path.join(root, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n = B.build_pack(target)
    stamp(target)
    deliver.main(target, os.path.join(root, "golden"), os.path.join(root, "figures.json") if root != TASK else
                 os.path.join(HERE, "figures.json"), os.path.join(root, "submission.md"))
    stamp(os.path.join(root, "golden"))
    if not quiet:
        for f in sorted(os.listdir(target)):
            print("  %-52s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)),
                                              ("%d rows" % n[f]) if f in n else ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-rebuild", action="store_true")
    a = ap.parse_args()
    full(TASK)
    metadata.write(TASK)
    target = os.path.join(TASK, "target")
    ok_c = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target]).returncode == 0
    ok_v = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target]).returncode == 0
    same = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="b165_", dir=os.path.dirname(TASK))
        try:
            full(tmp, quiet=True)
            same = (digest(target) == digest(os.path.join(tmp, "target")) and
                    digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden")) and
                    open(os.path.join(HERE, "figures.json"), "rb").read() ==
                    open(os.path.join(tmp, "figures.json"), "rb").read() and
                    open(os.path.join(TASK, "submission.md"), "rb").read() ==
                    open(os.path.join(tmp, "submission.md"), "rb").read())
            print("rebuild byte-identical: %s" % same)
        finally:
            shutil.rmtree(tmp)
    z = cut_zip()
    print("zip %s %d bytes sha256 %s" % (z, os.path.getsize(z), hashlib.sha256(open(z, "rb").read()).hexdigest()[:8]))
    sys.exit(0 if (ok_c and ok_v and same) else 1)


if __name__ == "__main__":
    main()
