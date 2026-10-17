"""Build task154: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the pack.

    python3 task154/generator/build.py              everything
    python3 task154/generator/build.py --out DIR    the pack only, into DIR"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
# the desk's folder as it stood when the call was made, and the goldens as sent
EXPORT_STAMP = dt.datetime(2026, 7, 29, 17, 30, 0)
GOLDEN_STAMP = dt.datetime(2026, 7, 29, 18, 0, 0)
# who saved each workbook, when (UTC)
OFFICE = {
    R.F_ANNUAL: ("Statistics Office", "Statistics Office", "2026-07-20T21:02:00Z", "2026-07-20T22:31:00Z",
                 "Annual national accounts 2025", "Statistics Office"),
    R.F_PRICES: ("Statistics Office", "Statistics Office", "2026-07-15T20:40:00Z", "2026-07-15T22:05:00Z",
                 "Price indexes, June 2026", "Statistics Office"),
    R.F_TRACKER: ("Jodie Ford", "Jodie Ford", "2026-04-30T23:18:00Z", "2026-07-27T19:52:00Z",
                  "GDP tracker, June quarter 2026", "Tarbert Bank"),
}


class Built:
    pass


def build(out, quiet=False):
    import docs as D
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    W = R.prepare()
    counts = R.write_all(out, W)
    D.write_all(out, W)
    for f, (cr, by, c0, c1, title, company) in OFFICE.items():
        PP.normalize_ooxml(os.path.join(out, f), cr, by, c0, c1, title=title, excel=True, company=company)
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    B = Built()
    B.W, B.counts = W, counts
    B.bundle = R.bundle(out, W)
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
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
    import submission as SUB
    Bt = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    os.makedirs(gdir)
    os.makedirs(os.path.join(root, "generator"), exist_ok=True)
    res, figs = DL.write_all(gdir, os.path.join(root, "generator"), Bt.bundle)
    stamp = GOLDEN_STAMP.timestamp()
    for f in os.listdir(gdir):
        os.utime(os.path.join(gdir, f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    SUB.write(os.path.join(root, "submission.md"), Bt.bundle, res, figs)
    Bt.res, Bt.figs = res, figs
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
          "target.zip (sha256 %s; target.zip sha256 %s)" % (
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
