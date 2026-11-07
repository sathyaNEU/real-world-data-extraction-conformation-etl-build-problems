"""task231 architecture 2: build the pack, the goldens, figures.json, submission.md and metadata.json; rebuild into a
scratch folder and require byte-identical output; cut target.zip; then run the checks and the independent verifier.

    python3 task231/generator/make.py
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
import deliver as DL  # noqa: E402
import docs as DC     # noqa: E402
import pack as PK     # noqa: E402
import params as P    # noqa: E402
import world as WD    # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMPS = {P.FILES["feed"]: (2027, 5, 12, 7, 41, 18),
          P.FILES["qc"]: (2027, 5, 4, 16, 2, 50),
          P.FILES["register"]: (2027, 5, 11, 16, 41, 4),
          P.FILES["standard"]: (2026, 8, 28, 15, 41, 0),
          P.FILES["qcconfig"]: (2027, 1, 13, 9, 26, 0),
          P.FILES["sla"]: (2025, 6, 27, 16, 2, 0),
          P.FILES["messages"]: (2027, 5, 3, 6, 14, 36),
          P.FILES["modems"]: (2027, 4, 28, 13, 13, 22),
          P.FILES["outages"]: (2027, 4, 22, 10, 55, 8),
          P.FILES["pavement"]: (2027, 5, 12, 7, 44, 2),
          P.FILES["preseason"]: (2026, 10, 2, 14, 31, 40),
          P.FILES["nwp"]: (2027, 5, 2, 3, 20, 12),
          P.FILES["traffic"]: (2027, 1, 9, 11, 6, 30),
          P.FILES["email"]: (2027, 5, 18, 8, 42, 0)}


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def build(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = WD.build()
    PK.write_all(W, target)
    DC.write_all(target)
    return W


def one(target, golden, extra, here):
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    build(target)
    fig, rows, S = DL.write_all(target, golden, here)
    WU.submission(fig, rows, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"))
    return digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read(), \
        open(os.path.join(here, "figures.json"), "rb").read()


def main():
    t1 = one(TARGET, GOLDEN, TASK, HERE)
    with tempfile.TemporaryDirectory() as tmp:
        t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp, tmp)
    same = t1 == t2
    print("byte-identical rebuild: target %s, golden %s, submission %s, figures %s" % tuple(
        a == b for a, b in zip(t1, t2)))
    if not same:
        sys.exit(1)
    assert sorted(STAMPS) == sorted(os.listdir(TARGET)), sorted(set(STAMPS) ^ set(os.listdir(TARGET)))
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMPS[f])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    if "--no-checks" in sys.argv:
        return
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rc |= subprocess.call([sys.executable, os.path.join(HERE, "verify.py")])
    sys.exit(rc)


if __name__ == "__main__":
    main()
