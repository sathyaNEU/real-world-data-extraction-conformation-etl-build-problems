"""Build task465: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task465/generator/build.py              everything
    python3 task465/generator/build.py --out DIR    the pack only, into DIR
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
CENTRAL = dt.timezone(dt.timedelta(hours=-6))
STAMP = dt.datetime(2026, 11, 16, 15, 40, tzinfo=CENTRAL)      # the folder as the programme manager assembled it


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or S.everything()
    n = {}
    n["heas"] = P.write_csv(f("heas"), P.HEAS_COLS, P.heas_rows(x))
    n["shs"] = P.write_csv(f("shs"), P.SHS_COLS, P.shs_rows(x))
    n["pilot"] = P.write_csv(f("pilot"), P.PILOT_COLS, P.pilot_rows(x))
    n["divisions"] = P.write_csv(f("divisions"), P.DIV_COLS, P.division_rows())
    n["baseline"] = P.write_csv(f("baseline"), P.ENROL_COLS, P.enrol_rows(x))
    n["batteries"] = P.write_csv(f("batteries"), P.ORDER_COLS, P.order_rows(x))
    n["hvi"] = P.write_csv(f("hvi"), P.HVI_COLS, P.hvi_rows(x))
    n["liheap"] = P.write_csv(f("liheap"), P.APPS_COLS, P.apps_rows(x))
    P.estimates_workbook(f("estimates"), x)
    DC.write_shs_codebook(f("shs_codebook"))
    DC.write_heas_notes(f("heas_methods"), n["heas"])
    DC.write_pilot_report(f("pilot_report"), x["screens"])
    DC.write_plan(f("plan"))
    n["dict"] = DC.write_dictionary(f("dict"))
    n["register"] = DC.write_register(f("register"), n)
    PP.normalize_ooxml(f("estimates"), "Population Estimates Unit", "Population Estimates Unit", "2026-02-24T15:10:00Z",
                       "2026-03-17T21:42:19Z", excel=True, company=W.DEMOGRAPHER)
    PP.normalize_ooxml(f("shs_codebook"), "Center for Health Statistics", "Center for Health Statistics",
                       "2026-04-02T13:30:00Z", "2026-05-11T19:06:44Z", excel=True, company=W.HEALTH_DEPT)
    PP.normalize_pdf(f("heas_methods"), b"D:20251120093000-06'00'", b"D:20251120093000-06'00'")
    PP.normalize_pdf(f("pilot_report"), b"D:20250926141500-05'00'", b"D:20250926141500-05'00'")
    PP.normalize_pdf(f("plan"), b"D:20261112163000-06'00'", b"D:20261112163000-06'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
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
    stamp = (2026, 11, 16, 15, 40, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
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
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["manager"], W.PEOPLE["manager"],
                       "2026-11-16T15:05:00Z", "2026-11-17T22:31:08Z", excel=False, company=W.ORG)
    ts = dt.datetime(2026, 11, 17, 16, 31, tzinfo=CENTRAL).timestamp()
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
