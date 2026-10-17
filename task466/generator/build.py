"""Build task466: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task466/generator/build.py              everything
    python3 task466/generator/build.py --out DIR    the pack only, into DIR
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
EASTERN = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2026, 10, 16, 14, 40, tzinfo=EASTERN)      # the folder as the water department assembled it

# the PDFs' own dates (creation, modification), each on or after the as-of date the folder's index gives it
PDF_STAMPS = {
    "reports": b"D:20190603141200-04'00'",
    "guidance": b"D:20230315100500-04'00'",
    "plan": b"D:20240514163000-04'00'",
    "permit": b"D:20210303112000-05'00'",
    "station": b"D:20251120090500-05'00'",
    "offer": b"D:20261006153500-04'00'",
    "regression": b"D:20190930120000-04'00'",
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
    n["gauge"] = P.write_gauge(f("gauge"), x)
    n["notices"] = P.write_csv(f("notices"), P.NOTICE_COLS, P.notice_rows(x))
    n["scada"] = P.write_csv(f("scada"), P.SCADA_COLS, P.scada_rows(x))
    n["elmhollow"] = P.write_csv(f("elmhollow"), P.EH_COLS, P.elm_rows(x))
    n["welllog"] = P.write_csv(f("welllog"), P.LOG_COLS, P.log_rows(x))
    n["precip"] = P.write_csv(f("precip"), P.PRECIP_COLS, P.precip_rows(x))
    DC.write_reports(f("reports"), x)
    DC.write_guidance(f("guidance"))
    DC.write_plan(f("plan"))
    DC.write_permit(f("permit"))
    DC.write_station(f("station"))
    DC.write_offer(f("offer"))
    DC.write_regression(f("regression"))
    DC.write_meters(f("meters"))
    n["dict"] = DC.write_dictionary(f("dict"))
    DC.write_index(f("index"), n)
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    PP.normalize_ooxml(f("meters"), "Quillfield Water Department", "Quillfield Water Department", "2019-02-11T14:20:00Z",
                       "2026-09-28T18:05:44Z", excel=True, company=PP.COMPANY)
    asof = {k: d for k, src, desc, d in DC.INDEX}
    for i, k in enumerate(W.FILES):
        if k in asof and k != "dict":
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


def everything(root, quiet=False):
    import golden as GO
    import metadata as MD
    import postprocess as PP
    import writeup as WU
    n, x = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20261016161500-04'00'", b"D:20261016161500-04'00'")
    ts = dt.datetime(2026, 10, 16, 16, 15, tzinfo=EASTERN).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return x


def main():
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
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
            raise SystemExit("second build differs: target %s %s, golden %s, %s" % (same_t, bad, same_g, same))
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
    args = ap.parse_args()
    if args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main()
