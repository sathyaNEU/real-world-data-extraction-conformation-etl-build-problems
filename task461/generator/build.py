"""Build task461: the pack into <task>/target, the goldens into <task>/golden, metadata.json and generator/figures.json;
then the checks and the independent verifier, a second full build into a scratch folder inside the task compared
byte for byte, and target.zip cut from the final build.

    python3 task461/generator/build.py              everything
    python3 task461/generator/build.py --out DIR    the pack only, into DIR
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

import market as MK     # noqa: E402
import ops as O         # noqa: E402
import pack as P        # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL = dt.timezone(dt.timedelta(hours=-6))
STAMP = dt.datetime(2026, 11, 6, 10, 42, tzinfo=CENTRAL)       # the folder as the analyst assembled it


def world():
    days = O.published_node(MK.simulate())
    dayrec, phys = O.operate(days)
    drops = O.dropouts(dayrec, phys)
    view = O.bms_view(phys, drops)
    lines = O.statements(dayrec, days)
    return dict(days=days, dayrec=dayrec, phys=phys, drops=drops, view=view, lines=lines,
                rt=MK.realtime(days), asp=MK.ancillary(days))


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or world()
    n = {}
    n["hub"] = P.write_csv(f("hub"), P.PRICE_COLS, P.hub_rows(x["days"]))
    n["node"] = P.write_csv(f("node"), P.PRICE_COLS, P.node_rows(x["days"]))
    n["points"] = P.write_csv(f("points"), P.POINT_COLS, P.point_rows())
    n["rt"] = P.write_csv(f("rt"), P.RT_COLS, P.rt_rows(x["rt"]))
    n["as_prices"] = P.write_csv(f("as_prices"), P.AS_COLS, P.as_rows(x["asp"]))
    n["bms"] = P.write_csv(f("bms"), P.BMS_COLS, P.bms_rows(x["view"], P.cell_temp(x["phys"])))
    n["meter"] = P.write_csv(f("meter"), P.METER_COLS, P.meter_rows(x["phys"]))
    n["settle"] = P.write_csv(f("settle"), P.SETTLE_COLS, P.settle_rows(x["lines"]))
    DC.write_policy(f("policy"))
    DC.write_warranty(f("warranty"))
    DC.write_tests(f("tests"), x["dayrec"])
    DC.write_dictionary(f("dict"), n)
    n["manifest"] = DC.write_manifest(f("manifest"), n)
    PP.normalize_ooxml(f("dict"), W.PEOPLE["analyst"], W.PEOPLE["analyst"], "2026-11-04T15:20:00Z",
                       "2026-11-06T16:31:07Z", excel=True, company=W.ORG)
    PP.normalize_pdf(f("policy"), b"D:20260206141500-06'00'", b"D:20260206141500-06'00'")
    PP.normalize_pdf(f("warranty"), b"D:20250627110000-05'00'", b"D:20250627110000-05'00'")
    PP.normalize_pdf(f("tests"), b"D:20260918093000-05'00'", b"D:20260918093000-05'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 11, 6, 10, 42, 0)
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
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["analyst"], W.PEOPLE["analyst"],
                       "2026-11-16T14:05:00Z", "2026-11-20T17:48:22Z", excel=False, company=W.ORG)
    ts = dt.datetime(2026, 11, 20, 11, 48, tzinfo=CENTRAL).timestamp()
    for f in os.listdir(gdir):
        os.utime(os.path.join(gdir, f), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
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
        same = {f: open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
                for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
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
