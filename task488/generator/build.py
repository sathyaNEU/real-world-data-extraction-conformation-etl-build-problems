"""Build task488: the pack into <task>/target, figures.json, the goldens into <task>/golden, submission.md and
metadata.json, then the checks, the verifier, the pair ceiling, a second build compared byte for byte, and
target.zip.

    python3 task488/generator/build.py            everything
    python3 task488/generator/build.py --fast     skip the rivals, the family and the anchor check"""
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
import figures as FG  # noqa: E402
import pack as PK  # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = (2027, 4, 2, 9, 30, 0)
MTIME = calendar.timegm((2027, 4, 2, 14, 30, 0, 0, 0, 0))


def stamp(folder):
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (MTIME, MTIME))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def build_pack(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    tb = PK.tables()
    s = PK.shipped(tb)
    nrows = PK.write(target, s)
    stamp(target)
    return tb, s, nrows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--no-second", action="store_true")
    ap.add_argument("--reuse", action="store_true", help="keep the rivals, family and anchor figures in figures.json")
    a = ap.parse_args()
    target = os.path.join(TASK, "target")
    golden = os.path.join(TASK, "golden")
    tb, s, nrows = build_pack(target)
    for f in sorted(os.listdir(target)):
        print("  %-58s %11d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), nrows.get(f, "")))
    if a.reuse:
        import json
        old = json.load(open(os.path.join(HERE, "figures.json")))
        F, ex = FG.compute(s, tb, full=False)
        for k, v in old.items():
            if k.startswith(("riv_", "fam_", "anchor_", "mess_")):
                F[k] = v
        F["anchor_golden_max_abs"] = round(max(abs(F["anchor_golden_low_%d" % g]) for g in [3, 4, 5, 6, 7, 8]), 1)
        F["anchor_reported_min_abs"] = round(min(-F["anchor_reported_low_%d" % g] for g in [3, 4, 5, 6, 7, 8]), 1)
        F["anchor_reported_max_abs"] = round(max(-F["anchor_reported_low_%d" % g] for g in [3, 4, 5, 6, 7, 8]), 1)
    else:
        F, ex = FG.compute(s, tb, full=not a.fast)
    FG.write(F)
    print("call", F["call"], {g: F["commission_%d" % g] for g in [3, 4, 5, 6, 7, 8]})
    try:
        import deliver as DL
        import writeup as WU
        import checks as CK
    except ImportError as e:
        print("later modules missing:", e)
        return
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    DL.build(F, ex, s, tb, golden)
    WU.write(F, nrows)
    rows, failed = CK.run(s, tb, F, ex, target, golden)
    for label, ok, detail in rows:
        print("  %s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("checks: %d of %d" % (len(rows) - len(failed), len(rows)))
    if failed:
        sys.exit(1)
    if subprocess.run([sys.executable, os.path.join(HERE, "verify.py")]).returncode:
        sys.exit(1)
    subprocess.run([sys.executable, os.path.join(HERE, "ceiling.py")])
    if not a.no_second:
        tmp = tempfile.mkdtemp(prefix="t488b_")
        tb2, s2, _ = build_pack(os.path.join(tmp, "target"))
        F2, ex2 = FG.compute(s2, tb2, full=False)
        DL.build(F2, ex2, s2, tb2, os.path.join(tmp, "golden"))
        same = digest(target) == digest(os.path.join(tmp, "target")) and digest(golden) == digest(os.path.join(tmp, "golden"))
        print("second build byte-identical: %s (%d pack files, %d goldens)" % (same, len(os.listdir(target)), len(os.listdir(golden))))
        shutil.rmtree(tmp)
        if not same:
            sys.exit(1)
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip", hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
