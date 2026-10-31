"""Build the pack, write the goldens, figures.json, submission.md and metadata.json, rebuild into a scratch folder
and require byte-identical output, cut target.zip, then run the checks and the independent verifier.

    python3 task125/generator/make.py
"""
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
import deliver as DL  # noqa: E402
import pack as P      # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 10, 9, 8, 40, 0)


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def one(target, golden, extra):
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    B.build(target)
    fig = DL.write_all(target, golden, TASK)
    WU.submission(fig, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"))
    return digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read()


def main():
    t1 = one(TARGET, GOLDEN, TASK)
    with tempfile.TemporaryDirectory() as tmp:
        t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp)
        # the second build wrote figures.json too; rewrite it from the first
    DL.write_all(TARGET, GOLDEN, TASK)
    same = t1 == t2
    print("byte-identical rebuild: target %s, golden %s, submission %s" % (t1[0] == t2[0], t1[1] == t2[1], t1[2] == t2[2]))
    if not same:
        sys.exit(1)
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    sys.exit(rc)


if __name__ == "__main__":
    main()
