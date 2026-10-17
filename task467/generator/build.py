"""Build task467: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task467/generator/build.py              everything
    python3 task467/generator/build.py --out DIR    the pack only, into DIR
    python3 task467/generator/build.py --fast       one build with the checks, no second build or zip
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
import sim as S          # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-4))
STAMP = dt.datetime(2026, 10, 16, 15, 20, tzinfo=EASTERN)      # the folder as the finance manager assembled it

PDF_STAMPS = {
    "dictionary": b"D:20260209104237-05'00'",
    "bylaw": b"D:20260102091514-05'00'",
    "policy": b"D:20230614153052-04'00'",
    "notice": b"D:20260814112009-04'00'",
    "bulletin": b"D:20241021080341-04'00'",
    "survey": b"D:20240226141128-05'00'",
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or S.everything()
    n = {}
    n["trips2024"] = P.write_annual(f("trips2024"), P.file_2024(x), P.V2)
    n["trips2025"] = P.write_annual(f("trips2025"), P.file_2025(x), P.V3)
    for m in range(1, 9):
        n["drop%02d" % m] = P.write_drop(f("drop%02d" % m), P.drop_2026(x, m), m)
    n["archive"] = P.write_csv(f("archive"), P.ARCHIVE_COLS, P.archive_rows(x))
    n["zones"] = P.write_csv(f("zones"), P.ZONE_COLS, P.zone_rows())
    n["brokerages"] = P.write_csv(f("brokerages"), P.BROKERAGE_COLS, P.brokerage_rows())
    n["affiliations"] = P.write_csv(f("affiliations"), P.AFFIL_COLS, P.affiliation_rows(x))
    DC.write_dictionary(f("dictionary"))
    DC.write_bylaw(f("bylaw"))
    DC.write_policy(f("policy"))
    DC.write_notice(f("notice"))
    DC.write_bulletin(f("bulletin"))
    DC.write_survey(f("survey"))
    DC.write_budget(f("budget"))
    DC.write_passengers(f("passengers"))
    n["passengers"] = len(DC.passenger_rows())
    DC.write_index(f("index"), n)
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    PP.normalize_ooxml(f("budget"), W.PEOPLE["finance"], W.PEOPLE["finance"], "2026-09-08T14:12:00Z",
                       "2026-10-14T19:41:27Z", excel=True, company=W.AUTHORITY)
    PP.normalize_ooxml(f("passengers"), "Airport Operations", "Airport Operations", "2023-02-06T13:05:00Z",
                       "2026-09-22T15:18:09Z", excel=True, company=W.AUTHORITY)
    asof = {k: d for k, src, d, desc in __import__("docs").INDEX}
    for i, k in enumerate(W.FILES):
        if k in asof:
            y, m, d = (int(v) for v in asof[k].split("-"))
            ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=EASTERN).timestamp()
        else:
            ts = STAMP.timestamp()
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
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["memo"]), W.PEOPLE["finance"], W.PEOPLE["finance"],
                       "2026-10-09T13:02:00Z", "2026-10-16T19:48:00Z", title="2027 taxi pickup fee", company=W.AUTHORITY)
    ts = dt.datetime(2026, 10, 16, 15, 48, tzinfo=EASTERN).timestamp()
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
