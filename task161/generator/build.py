"""Build task161: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task161/generator/build.py              everything
    python3 task161/generator/build.py --out DIR    the pack only, into DIR
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile
import time
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core     # noqa: E402
import pack     # noqa: E402

TASK = os.path.dirname(HERE)
# the planner's folder as it stood when the call was made (Monday 7 December 2026), and the goldens as sent
EXPORT_STAMP = dt.datetime(2026, 12, 7, 9, 10, 0)
GOLDEN_STAMP = dt.datetime(2026, 12, 7, 15, 45, 0)


class Built:
    pass


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    t0 = time.time()
    Wd = core.build_world()
    counts = pack.write_all(out, Wd)
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    B = Built()
    B.Wd, B.counts = Wd, counts
    if not quiet:
        print("built %s: %d files in %.0f s; %s" % (out, len(os.listdir(out)), time.time() - t0,
                                                    ", ".join("%s %s" % kv for kv in sorted(counts.items()))))
    return B


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    when = EXPORT_STAMP.timetuple()[:6]
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(folder, f), "rb") as fh:
                z.writestr(zi, fh.read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    Bt = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    os.makedirs(gdir)
    os.makedirs(os.path.join(root, "generator"), exist_ok=True)
    res = DL.write_all(os.path.join(root, "target"), gdir, os.path.join(root, "generator"))
    stamp = GOLDEN_STAMP.timestamp()
    for f in os.listdir(gdir):
        os.utime(os.path.join(gdir, f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    import submission as SUB
    SUB.write(os.path.join(root, "submission.md"), os.path.join(root, "generator", "figures.json"))
    Bt.res = res
    return Bt


def main():
    import checks as CK
    import verify as V
    Bt = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), Bt)
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        same["target.zip"] = open(cut_zip(TASK), "rb").read() == open(cut_zip(tmp), "rb").read()
        if not (same_t and same_g and all(same.values())):
            d1, d2 = digest(os.path.join(TASK, "target")), digest(os.path.join(tmp, "target"))
            g1, g2 = digest(os.path.join(TASK, "golden")), digest(os.path.join(tmp, "golden"))
            raise SystemExit("second build differs: target %s, golden %s, %s; %s" % (
                same_t, same_g, same, [f for f in d1 if d1[f] != d2.get(f)] + [f for f in g1 if g1[f] != g2.get(f)]))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode())
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, figures.json, submission.md and "
          "target.zip "
          "(sha256 %s; target.zip sha256 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
