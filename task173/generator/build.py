"""Build task173: the evidence pack into <task>/target, the golden into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build into a
scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task173/generator/build.py              everything
    python3 task173/generator/build.py --pack-only  the pack, golden and write-up, no checks"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402

ZIP_STAMP = (2026, 10, 16, 15, 20, 0)


def build_into(target, golden, write_docs=True):
    import world, records, pack, deliver, metadata
    W = world.draw()
    ids = records.make_ids(W)
    if os.path.exists(target):
        shutil.rmtree(target)
    pack.write_all(W, ids, target)
    os.makedirs(golden, exist_ok=True)
    P, g, A, Cc, n, e, fig = deliver.compute(target)
    deliver.write_xlsx(os.path.join(golden, C.DELIVERABLE), P, g, A, Cc, n, e, fig)
    if write_docs:
        deliver.write_figures(os.path.join(HERE, "figures.json"), fig, g)
        deliver.write_submission(os.path.join(C.TASK, "submission.md"), P, g, A, Cc, n, e, fig)
        metadata.write(C.TASK)
    return W, ids, g, fig


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=ZIP_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-only", action="store_true")
    a = ap.parse_args()
    build_into(C.TARGET, C.GOLDEN)
    if a.pack_only:
        return 0
    rc = subprocess.call([sys.executable, os.path.join(HERE, "checks.py")])
    rv = subprocess.call([sys.executable, os.path.join(HERE, "verify.py"), C.TARGET])
    tmp = tempfile.mkdtemp(prefix="t173_")
    t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    build_into(t2, g2, write_docs=False)
    d1, d2 = digest(C.TARGET), digest(t2)
    dg1, dg2 = digest(C.GOLDEN), digest(g2)
    same = d1 == d2 and dg1 == dg2
    print("rebuild byte-identical:", same, "(%d pack files, %d golden)" % (len(d1), len(dg1)))
    if not same:
        for k in sorted(set(d1) | set(d2)):
            if d1.get(k) != d2.get(k):
                print("  differs:", k)
    shutil.rmtree(tmp)
    cut_zip(C.TARGET, os.path.join(C.TASK, "target.zip"))
    print("target.zip", hashlib.md5(open(os.path.join(C.TASK, "target.zip"), "rb").read()).hexdigest())
    return 0 if (rc == 0 and rv == 0 and same) else 1


if __name__ == "__main__":
    sys.exit(main())
