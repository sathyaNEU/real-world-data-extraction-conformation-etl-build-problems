"""Build task157 (architecture 2): the evidence pack into <task>/target, the goldens into <task>/golden,
metadata.json and generator/figures.json, then the checks and the independent verifier, then a second full
build into a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task157/generator/build.py              everything
    python3 task157/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2028, 8, 4, 9, 20, 0)                        # the export's own moment, Arizona local time
MTIME = calendar.timegm((2028, 8, 4, 16, 20, 0, 0, 0, 0))  # the same moment in UTC


class Built:
    pass


def world(seed=K.SEED):
    B = Built()
    B.W = WD.build(seed)
    B.S = R.shape(B.W)
    return B


def build_data(out, B):
    p = lambda f: os.path.join(out, f)
    w, S = B.W, B.S
    n = {}
    n[R.F_RETURNS] = K.write_csv(p(R.F_RETURNS), R.RETURNS_COLS, R.returns_rows(w, S))
    n[R.F_CORR] = K.write_csv(p(R.F_CORR), R.CORR_COLS, R.corr_rows(w, S))
    n[R.F_SNAP_EARLY] = K.write_csv(p(R.F_SNAP_EARLY), R.SNAP_COLS, R.snapshot_rows(w, S, False))
    n[R.F_SNAP_LATE] = K.write_csv(p(R.F_SNAP_LATE), R.SNAP_COLS, R.snapshot_rows(w, S, True))
    n[R.F_SHEETS] = K.write_csv(p(R.F_SHEETS), R.SHEET_COLS, R.sheet_rows(w, S))
    n[R.F_RECEIPT] = K.write_csv(p(R.F_RECEIPT), R.RECEIPT_COLS, R.receipt_rows(w, S))
    n[R.F_MANIFEST] = K.write_csv(p(R.F_MANIFEST), R.MANIFEST_COLS, R.manifest_rows(w, S), crlf=True)
    n[R.F_CIRC] = K.write_csv(p(R.F_CIRC), R.CIRC_COLS, R.circ_rows(w, S))
    n[R.F_MAINT] = K.write_csv(p(R.F_MAINT), R.MAINT_COLS, R.maint_rows(w, S), crlf=True)
    n[R.F_OTHER] = K.write_csv(p(R.F_OTHER), R.OTHER_COLS, R.other_rows(w, S))
    n[R.F_REGSTATS] = K.write_csv(p(R.F_REGSTATS), R.REGSTATS_COLS, R.regstats_rows(w, S))
    return n


def build(out, quiet=False, B=None):
    os.makedirs(out, exist_ok=True)
    B = B or world()
    n = build_data(out, B)
    B.closeout = DOC.write_all(out, B.W, n)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-54s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)),
                                             ("%d rows" % n[f]) if f in n else ""))
    return B, n


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
    ap.add_argument("--no-zip", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    import subprocess
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    B, n = build(target)
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"))
    import metadata
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    tmp = tempfile.mkdtemp(prefix="b157_", dir=TASK)
    try:
        build(os.path.join(tmp, "target"), quiet=True)
        deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"),
                     os.path.join(tmp, "figures.json"), os.path.join(tmp, "submission.md"))
        same = digest(target) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same_f = (open(os.path.join(HERE, "figures.json"), "rb").read()
                  == open(os.path.join(tmp, "figures.json"), "rb").read())
        same_s = (open(os.path.join(TASK, "submission.md"), "rb").read()
                  == open(os.path.join(tmp, "submission.md"), "rb").read())
        print("rebuild byte-identical: target %s, golden %s, figures %s, submission %s"
              % (same, same_g, same_f, same_s))
    finally:
        shutil.rmtree(tmp)
    if not a.no_zip:
        z = cut_zip(TASK)
        print("zip %s sha256 %s" % (z, hashlib.sha256(open(z, "rb").read()).hexdigest()))
    if r1.returncode or r2.returncode or not (same and same_g and same_f and same_s):
        sys.exit(1)


if __name__ == "__main__":
    main()
