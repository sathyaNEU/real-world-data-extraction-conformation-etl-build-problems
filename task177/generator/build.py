"""Build task177: the evidence pack into <task>/target, figures.json, the goldens into <task>/golden, submission.md
and metadata.json, then the checks, the independent verifier, the pair ceiling, a second full build into a scratch
folder compared byte for byte, and target.zip cut from the pack.

    python3 task177/generator/build.py            everything
    python3 task177/generator/build.py --fast     skip the golden's family (32 constructions) in the checks"""
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
import checks as CK  # noqa: E402
import deliver as DL  # noqa: E402
import figures as FG  # noqa: E402
import pack as PK  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = (2027, 1, 8, 18, 30, 0)                                   # the data room's export, IST
MTIME = calendar.timegm((2027, 1, 8, 13, 0, 0, 0, 0, 0))          # the same moment in UTC


def stamp(folder):
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (MTIME, MTIME))


def digest(folder):
    out = {}
    for f in sorted(os.listdir(folder)):
        out[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return out


def build_pack(target, golden):
    if os.path.isdir(target):
        shutil.rmtree(target)
    shipped, aux = PK.tables()
    nrows = PK.write(target, shipped, aux)
    stamp(target)
    return shipped, aux, nrows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    target = os.path.join(TASK, "target")
    golden = os.path.join(TASK, "golden")
    shipped, aux, nrows = build_pack(target, golden)
    for f in sorted(os.listdir(target)):
        print("  %-58s %11d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), nrows.get(f, "")))
    F, ex = FG.compute(shipped, aux, with_family=not a.fast)
    FG.write(F)
    if os.path.isdir(golden):
        shutil.rmtree(golden)
    DL.build(F, golden)
    WU.write(F, nrows)
    rows, failed = CK.run(shipped, aux, F, ex, target)
    for label, ok, detail in rows:
        print("  %s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    print("checks: %d of %d" % (len(rows) - len(failed), len(rows)))
    if failed:
        sys.exit(1)
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")])
    if r.returncode:
        sys.exit(1)
    subprocess.run([sys.executable, os.path.join(HERE, "ceiling.py")])
    # a second full build into scratch, byte for byte
    tmp = tempfile.mkdtemp(prefix="t177b_")
    s2, a2, _ = build_pack(os.path.join(tmp, "target"), None)
    DL.build(F, os.path.join(tmp, "golden"))
    d1, d2 = digest(target), digest(os.path.join(tmp, "target"))
    g1, g2 = digest(golden), digest(os.path.join(tmp, "golden"))
    same = d1 == d2 and g1 == g2
    print("second build byte-identical: %s (%d pack files, %d goldens)" % (same, len(d1), len(g1)))
    if not same:
        print([k for k in d1 if d1[k] != d2.get(k)] + [k for k in g1 if g1[k] != g2.get(k)])
        sys.exit(1)
    shutil.rmtree(tmp)
    zpath = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip %s" % hashlib.sha256(open(zpath, "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
