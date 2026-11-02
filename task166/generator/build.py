"""Build task166: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte (and deleted), then target.zip cut from the pack.

    python3 task166/generator/build.py              everything
    python3 task166/generator/build.py --out DIR    the pack only, into DIR
    python3 task166/generator/build.py --pack       the pack into target/ only"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
import zipfile

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import postprocess as PP    # noqa: E402
import records as RC        # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
SCRATCH = os.environ.get("TASK166_SCRATCH", os.path.join(TASK, ".scratch"))
PULL_DONE = (2026, 10, 30, 18, 30, 0)                       # the pack assembled, London (GMT)
MTIME = calendar.timegm((2026, 10, 30, 18, 30, 0, 0, 0, 0))  # the same moment, UTC


def normalize(out):
    PP.normalize_ooxml(os.path.join(out, RC.F_TITLES), "Marrowgate Books", "Marrowgate Books", "2026-10-30T17:52:00Z",
                       "2026-10-30T17:52:00Z", excel=True, company=K.COMPANY)
    PP.normalize_ooxml(os.path.join(out, RC.F_REINSPECT), K.PEOPLE["dist_returns"], K.PEOPLE["dist_returns"],
                       "2025-11-03T08:41:00Z", "2026-10-30T16:20:00Z", excel=True, company=K.DISTRIBUTOR)
    PP.normalize_pdf(os.path.join(out, RC.F_TERMS), b"D:20240226113000+00'00'", b"D:20240226113000+00'00'")
    PP.normalize_pdf(os.path.join(out, RC.F_POLICY), b"D:20260915142000+01'00'", b"D:20260915142000+01'00'")


def build(out, quiet=False):
    os.makedirs(out, exist_ok=True)
    W = WD.simulate()
    R = RC.Records(W)
    n = RC.write_all(out, R)
    DOC.write_all(out)
    normalize(out)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    if not quiet:
        for f in sorted(os.listdir(out)):
            print("  %-56s %10d bytes %s" % (f, os.path.getsize(os.path.join(out, f)), ("%d rows" % n[f]) if n.get(f) else ""))
    return W, R, n


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
    ap.add_argument("--pack", action="store_true")
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    W, R, n = build(target)
    if a.pack:
        return
    import deliver
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"))
    import metadata
    metadata.write(TASK, n)
    r1 = r2 = None
    if not a.no_checks:
        r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")])
        r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    same = same_g = same_f = True
    if not a.no_rebuild:
        os.makedirs(SCRATCH, exist_ok=True)
        tmp = tempfile.mkdtemp(prefix="b166_", dir=SCRATCH)
        try:
            build(os.path.join(tmp, "target"), quiet=True)
            deliver.main(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), os.path.join(tmp, "figures.json"))
            same = digest(target) == digest(os.path.join(tmp, "target"))
            same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
            same_f = open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(tmp, "figures.json"), "rb").read()
            print("rebuild byte-identical: target %s, golden %s, figures %s" % (same, same_g, same_f))
        finally:
            shutil.rmtree(tmp)
            if os.path.isdir(SCRATCH) and not os.listdir(SCRATCH):
                os.rmdir(SCRATCH)
    z = cut_zip(TASK)
    print("zip", z, hashlib.sha256(open(z, "rb").read()).hexdigest())
    bad = (r1 is not None and r1.returncode) or (r2 is not None and r2.returncode)
    if bad or not (same and same_g and same_f):
        sys.exit(1)


if __name__ == "__main__":
    main()
