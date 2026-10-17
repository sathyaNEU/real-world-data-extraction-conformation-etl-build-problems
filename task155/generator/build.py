"""Build task155: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
compared byte for byte, then target.zip cut from the pack.

    python3 task155/generator/build.py              everything
    python3 task155/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 11, 12, 18, 52, 0)      # the extract folder as Workforce Systems sent it
GOLDEN_STAMP = dt.datetime(2026, 11, 13, 16, 20, 0)
OFFICE = {
    K.F_XMAS: ("Meredith Stevens", "Meredith Stevens", "2026-11-11T23:05:00Z", "2026-11-12T07:44:00Z",
               "Christmas roster 2026", "Kellaway's"),
    K.F_PLAN: ("Store Operations", "Store Operations", "2026-10-21T03:12:00Z", "2026-10-30T05:47:00Z",
               "Christmas trading plan 2026", "Kellaway's"),
}


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    Wd = R.prepare()
    counts = R.write_all(out, Wd)
    for f, (cr, by, c0, c1, title, company) in OFFICE.items():
        PP.normalize_ooxml(os.path.join(out, f), cr, by, c0, c1, title=title, excel=True, company=company)
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return Wd, counts


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--pack-only", action="store_true")
    ap.add_argument("--goldens", action="store_true", help="goldens, figures, submission, checks and verifier on the "
                                                           "existing target, no rebuild")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return 0
    target = os.path.join(TASK, "target")
    if not a.goldens:
        build(target)
    if a.pack_only:
        return 0
    import deliver as DL
    import metadata as MD
    import submission as SB
    figs = DL.write_goldens(TASK, target)
    MD.write(TASK, target)
    SB.write(TASK)
    import checks
    rc = checks.main(TASK, figs)
    import verify
    rv = verify.main(target, os.path.join(HERE, "figures.json"))
    if a.goldens:
        return 0 if (rc == 0 and rv == 0) else 1
    second = os.path.join(TASK, "_rebuild")
    build(second, quiet=True)
    d1, d2 = digest(target), digest(second)
    shutil.rmtree(second)
    same = d1 == d2
    print("rebuild byte-identical: %s (%d files)" % (same, len(d1)))
    if not same:
        print("differ:", [f for f in d1 if d1.get(f) != d2.get(f)])
    zp = cut_zip(TASK)
    print("zip:", zp)
    return 0 if (rc == 0 and rv == 0 and same) else 1


if __name__ == "__main__":
    sys.exit(main())
