"""Build task474: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task474/generator/build.py              everything
    python3 task474/generator/build.py --out DIR    the pack only, into DIR
    python3 task474/generator/build.py --fast       one build with the checks, no second build or zip
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

import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = {False: dt.timezone(dt.timedelta(hours=-5)), True: dt.timezone(dt.timedelta(hours=-4))}

PDF_STAMPS = {
    "rel2021": b"D:20211209094512-05'00'",
    "rel2022": b"D:20221208093821-05'00'",
    "rel2023": b"D:20231207100233-05'00'",
    "rel2024": b"D:20241212091047-05'00'",
    "methods": b"D:20241120142210-05'00'",
    "rule": b"D:20260915111902-04'00'",
}
OOXML = {   # creator, last modified by, created, modified, company
    "rel2025": (W.PEOPLE["demographer"], W.PEOPLE["demographer"], "2025-12-03T15:12:00Z", "2025-12-10T21:44:31Z",
                W.SDC),
    "fy2026": (W.PEOPLE["grants"], W.PEOPLE["grants"], "2025-09-08T14:20:00Z", "2025-09-12T19:03:12Z", W.OBP),
    "closeout": (W.PEOPLE["grants"], W.PEOPLE["grants"], "2026-07-06T13:40:00Z", "2026-10-02T18:27:45Z", W.OBP),
}
AS_OF = {   # each file's date as its source dated it
    "rel2021": "2021-12-09", "rel2022": "2022-12-08", "rel2023": "2023-12-07", "rel2024": "2024-12-12",
    "rel2025": "2025-12-10", "methods": "2024-11-20", "acs": "2026-01-08", "acs_notes": "2026-01-08",
    "snap": "2026-08-14", "codes": "2026-02-03", "rule": "2026-09-15", "fy2026": "2025-09-12",
    "factors": "2022-06-30", "closeout": "2026-10-02", "extract": "2026-10-01", "audit": "2026-10-01",
    "conversion": "2026-01-02", "layout": "2026-03-10",
}


def _dst(day):
    """Eastern daylight time runs from the second Sunday of March to the first Sunday of November."""
    y = day.year
    mar = dt.date(y, 3, 8) + dt.timedelta(days=(6 - dt.date(y, 3, 8).weekday()) % 7)
    nov = dt.date(y, 11, 1) + dt.timedelta(days=(6 - dt.date(y, 11, 1).weekday()) % 7)
    return mar <= day < nov


def build(out, quiet=False):
    import docs as DC
    import pack as P
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    n["codes"] = P.write_csv(f("codes"), P.CODES_COLS, P.codes_rows())
    n["acs"] = P.write_csv(f("acs"), P.ACS_COLS, P.acs_rows())
    n["snap"] = P.write_csv(f("snap"), P.SNAP_COLS, P.snap_rows(), crlf=True, delimiter="|")
    n["factors"] = P.write_csv(f("factors"), P.FACTOR_COLS, P.factor_rows())
    n["extract"] = P.write_csv(f("extract"), P.EXTRACT_COLS, P.extract_rows(), crlf=True)
    n["audit"] = P.write_csv(f("audit"), P.AUDIT_COLS, P.audit_rows(), crlf=True)
    n["conversion"] = P.write_csv(f("conversion"), P.CONVERSION_COLS, P.conversion_rows(), crlf=True)
    for k in ("rel2021", "rel2022", "rel2023", "rel2024"):
        DC.write_release(f(k), k)
    DC.write_release_2024(f("rel2025"))
    DC.write_methods(f("methods"))
    DC.write_rule(f("rule"))
    DC.write_acs_notes(f("acs_notes"))
    DC.write_fy2026(f("fy2026"))
    DC.write_closeout(f("closeout"))
    DC.write_layout(f("layout"))
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(W.FILES):
        day = dt.date.fromisoformat(AS_OF[k])
        ts = dt.datetime(day.year, day.month, day.day, 9 + (i * 7) % 8, (i * 13) % 60,
                         tzinfo=EASTERN[_dst(day)]).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(W.FILES), W.FILES[big], n[big]))
    return n


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            mt = os.path.getmtime(os.path.join(folder, name))
            day = dt.datetime.fromtimestamp(mt, dt.timezone.utc).date()
            t = dt.datetime.fromtimestamp(mt, EASTERN[_dst(day)])
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return n


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"),
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    vgood = V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"))
    if fast:
        if not (good and vgood):
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
    if not (good and vgood):
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
