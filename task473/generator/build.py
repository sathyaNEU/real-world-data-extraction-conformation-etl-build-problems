"""Build task473: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task473/generator/build.py              everything
    python3 task473/generator/build.py --out DIR    the pack only, into DIR
    python3 task473/generator/build.py --fast       one build with the checks, no second build or zip
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import pack as P         # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL_STD = dt.timezone(dt.timedelta(hours=-6))
CENTRAL_DST = dt.timezone(dt.timedelta(hours=-5))

PDF_STAMPS = {
    "guidelines": (b"D:20270209100512-06'00'", b"D:20270209100512-06'00'"),
    "manual": (b"D:20240314162207-05'00'", b"D:20240315091130-05'00'"),
    "crs_notes": (b"D:20270308141844-06'00'", b"D:20270308141844-06'00'"),
    "lab_annual": (b"D:20270305113027-06'00'", b"D:20270306082419-06'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company
    "agencies": (W.CENTER_SHORT, "Eduardo Chapman", "2024-01-08T15:12:00Z", "2027-01-04T16:40:27Z", W.UNIVERSITY),
    "vmt": ("Transportation Planning", "Transportation Planning", "2027-01-27T19:05:00Z", "2027-01-30T14:22:51Z",
            W.DOT),
    "licensed": ("MVD Statistics", "MVD Statistics", "2026-01-14T15:30:00Z", "2026-01-15T17:02:16Z",
                 "Department of Revenue"),
}
AS_OF = {   # each file's date as its source dated it
    "guidelines": "2027-02-09", "manual": "2024-03-15", "crash23": "2025-02-27", "person23": "2025-02-27",
    "crash2425": "2027-02-25", "person2425": "2027-02-25", "agencies": "2027-01-04", "vmt": "2027-01-30",
    "lab": "2027-03-12", "lab_notes": "2027-03-12", "sites": "2027-03-12", "reports": "2027-03-08",
    "units": "2027-03-08", "crs_notes": "2027-03-08", "lab_annual": "2027-03-06", "licensed": "2026-01-15",
    "prelim26": "2027-03-01", "index": "2027-03-18",
}


def build(out, x=None, quiet=False):
    import census as C
    import crs as R
    import docs as DC
    import lab as L
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or P.everything()
    n = {}
    c23, p23 = x["census23"]
    c25, p25 = x["census25"]
    n["crash23"] = P.write_csv(f("crash23"), C.CRASH23_COLS, c23)
    n["person23"] = P.write_csv(f("person23"), C.PERSON23_COLS, p23)
    n["crash2425"] = P.write_csv(f("crash2425"), C.CRASH25_COLS, c25)
    n["person2425"] = P.write_csv(f("person2425"), C.PERSON25_COLS, p25)
    n["lab"] = P.write_csv(f("lab"), L.COLS, x["lab_rows"], crlf=True)
    n["sites"] = P.write_csv(f("sites"), P.SITE_COLS, P.site_rows(), crlf=True)
    n["reports"] = P.write_csv(f("reports"), R.REPORT_COLS, x["rep_rows"])
    n["units"] = P.write_csv(f("units"), R.UNIT_COLS, x["unit_rows"])
    n["prelim26"] = P.write_csv(f("prelim26"), C.PRELIM_COLS, x["prelim"])
    n["index"] = P.write_csv(f("index"), P.INDEX_COLS, P.index_rows(), crlf=True)
    DC.write_lab_notes(f("lab_notes"), n["lab"])
    DC.write_guidelines(f("guidelines"))
    DC.write_manual(f("manual"))
    DC.write_crs_notes(f("crs_notes"), n["reports"], n["units"])
    DC.write_lab_annual(f("lab_annual"), x["kits"])
    DC.write_directory(f("agencies"))
    DC.write_dvmt(f("vmt"), x["tab"])
    DC.write_licensed(f("licensed"), x["vmt"])
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        tz = CENTRAL_DST if (3, 14) <= (m, d) <= (11, 1) else CENTRAL_STD
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=tz).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(W.FILES), W.FILES[big], n[big]))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), CENTRAL_STD)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig, x)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    if fast:
        if not good:
            raise SystemExit("checks failed")
        return
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {fn: open(os.path.join(TASK, fn), "rb").read() == open(os.path.join(tmp, fn), "rb").read()
                for fn in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            bad = [k for k, v in digest(os.path.join(TASK, "target")).items()
                   if digest(os.path.join(tmp, "target")).get(k) != v]
            badg = [k for k, v in digest(os.path.join(TASK, "golden")).items()
                    if digest(os.path.join(tmp, "golden")).get(k) != v]
            raise SystemExit("second build differs: target %s %s, golden %s %s, %s" % (same_t, bad, same_g, badg, same))
    finally:
        shutil.rmtree(tmp)
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, submission.md, figures.json" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not good:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--fast", action="store_true")
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main(fast=args.fast)
