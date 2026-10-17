"""Build task469: the pack into <task>/target, the golden workbook into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task469/generator/build.py              everything
    python3 task469/generator/build.py --out DIR    the pack only, into DIR
    python3 task469/generator/build.py --fast       one build with the checks, no second build or zip
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
EASTERN = dt.timezone(dt.timedelta(hours=-4))
STAMP = dt.datetime(2026, 10, 29, 16, 40, tzinfo=EASTERN)      # the folder as the analyst assembled it

PDF_STAMPS = {
    "guideline": b"D:20250814103322-04'00'",
    "ssim_layout": b"D:20250311141907-04'00'",
}
AS_OF = {   # each file's date as its source dated it
    "aodb": "2026-10-02", "pellmont": "2026-10-06", "sable": "2026-10-07", "grayling": "2026-10-05",
    "ssim26": "2026-03-02", "ssim27": "2026-10-09", "ssim_layout": "2025-03-11", "guideline": "2025-08-14",
    "filings": "2026-10-09", "affiliates": "2026-07-15", "aircraft": "2026-09-30", "fleet27": "2026-10-08",
    "delay_codes": "2025-08-14", "stations": "2026-03-02", "otp": "2026-10-13", "staffing": "2026-10-01",
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or P.everything()
    n = {}
    n["aodb"] = P.write_csv(f("aodb"), P.AODB_COLS, P.aodb_rows(x))
    n["pellmont"] = P.write_csv(f("pellmont"), P.PELLMONT_COLS, P.pellmont_rows(x))
    sable = P.sable_rows(x)
    DC.write_sable(f("sable"), sable)
    n["sable"] = len(sable)
    n["grayling"] = P.write_csv(f("grayling"), P.GRAYLING_COLS, P.grayling_rows(x))
    n["ssim26"] = P.write_ssim26(f("ssim26"), x)
    n["ssim27"] = P.write_ssim27(f("ssim27"), x)
    n["filings"] = P.write_csv(f("filings"), P.FILING_COLS, P.filing_rows())
    n["aircraft"] = P.write_csv(f("aircraft"), P.AIRCRAFT_COLS, P.aircraft_rows(x))
    n["fleet27"] = P.write_csv(f("fleet27"), P.FLEET_COLS, P.fleet_rows(x))
    n["delay_codes"] = P.write_csv(f("delay_codes"), P.DELAY_COLS, P.delay_rows())
    n["stations"] = P.write_csv(f("stations"), P.STATION_COLS, P.station_rows())
    n["staffing"] = P.write_csv(f("staffing"), P.STAFF_COLS, P.staffing_rows())
    DC.write_affiliates(f("affiliates"))
    DC.write_punctuality(f("otp"), x)
    DC.write_guideline(f("guideline"))
    DC.write_layout(f("ssim_layout"))
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    PP.normalize_ooxml(f("affiliates"), "Gate Planning", "Gate Planning", "2019-02-11T15:20:00Z",
                       "2026-07-15T13:44:51Z", excel=True, company=W.AUTHORITY)
    PP.normalize_ooxml(f("sable"), "Sable Coast Air OCC", "Sable Coast Air OCC", "2026-10-07T11:02:00Z",
                       "2026-10-07T11:06:37Z", excel=True, company="Sable Coast Air")
    PP.normalize_ooxml(f("otp"), "Airside Performance", "Airside Performance", "2026-10-13T14:10:00Z",
                       "2026-10-13T14:31:18Z", excel=True, company=W.AUTHORITY)
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=EASTERN).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), EASTERN)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import golden as GO
    import metadata as MD
    import postprocess as PP
    import writeup as WU
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][0],
                       "2026-10-26T13:05:00Z", "2026-10-29T20:31:00Z", excel=True, company=W.AUTHORITY)
    ts = dt.datetime(2026, 10, 29, 16, 31, tzinfo=EASTERN).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
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
