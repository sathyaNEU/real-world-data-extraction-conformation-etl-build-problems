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
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import docs as D            # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_STAMP = dt.datetime(2026, 10, 5, 15, 20, 0)      # the water resources lead's pull of the records
GOLDEN_STAMP = dt.datetime(2026, 11, 13, 16, 14, 0)
# who saved each workbook and when (UTC); the PDFs' issue dates
OWNERS = {
    R.F_TEST: ("Hollybush Hydro Consultants", "Hollybush Hydro Consultants", "2014-06-14T16:02:00Z",
               "2014-06-16T09:41:00Z", "BH2 constant rate test June 2014"),
    R.F_TICKETS: ("Teme Valley Bulk Liquids", "Teme Valley Bulk Liquids", "2026-05-01T07:52:00Z",
                  "2026-10-05T07:58:00Z", "Bulk load statements"),
    R.F_SKU: ("SAP export", K.PEOPLE["lead"], "2026-10-02T10:12:00Z", "2026-10-02T10:12:00Z", "Material master"),
}
PDF_DATES = {
    D.F_LETTER: (b"D:20260922113000+01'00'", b"D:20260922113000+01'00'"),
    D.F_LICENCE: (b"D:20150326100000+00'00'", b"D:20150326100000+00'00'"),
    D.F_GEOLOGY: (b"D:20260930141500+01'00'", b"D:20260930141500+01'00'"),
    D.F_RETURNS: (b"D:20260422090500+01'00'", b"D:20260422090500+01'00'"),
}


class Built:
    pass


def build(out, quiet=False):
    import calc as C
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    O = C.ops_cached()
    counts = R.write_all(out, O)
    D.write_all(out, O)
    for f, (cr, by, c0, c1, title) in OWNERS.items():
        PP.normalize_ooxml(os.path.join(out, f), cr, by, c0, c1, title=title, excel=True,
                           company=cr if "Teme" in cr or "Hollybush" in cr else K.COMPANY)
    for f, (c0, c1) in PDF_DATES.items():
        PP.normalize_pdf(os.path.join(out, f), c0, c1)
    PP.normalize_docx(os.path.join(out, D.F_BRIEF), K.PEOPLE["lead"], K.PEOPLE["lead"], "2026-09-02T08:40:00Z",
                      "2026-09-08T15:22:00Z", 4, 96, K.SEED, title="Line 5 project brief", company=K.COMPANY)
    stamp = EXPORT_STAMP.timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    B = Built()
    B.counts = counts
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
    import calc as C
    import deliver as DL
    import metadata as MD
    import submission as SUB
    Bt = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    os.makedirs(gdir)
    os.makedirs(os.path.join(root, "generator"), exist_ok=True)
    Bt.bundle = C.bundle(os.path.join(root, "target"))
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
          "target.zip (sha256 %s; target.zip md5 %s)" % (
              len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
              allh.hexdigest()[:16], hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
