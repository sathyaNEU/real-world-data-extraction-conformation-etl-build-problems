"""Build task463: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task463/generator/build.py              everything
    python3 task463/generator/build.py --out DIR    the pack only, into DIR
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

import coverage as CV    # noqa: E402
import feeds as F        # noqa: E402
import pack as P         # noqa: E402
import published as PB   # noqa: E402
import sim as S          # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
KELLESAY = dt.timezone(dt.timedelta(hours=1))
STAMP = dt.datetime(2026, 10, 21, 16, 42, tzinfo=KELLESAY)       # the folder as the prices team assembled it


def world():
    ls = S.world()
    x = {"lines": ls}
    x["wrenfold"] = F.wrenfold(ls, W.STREAM)
    x["gorsedale"] = F.gorsedale(ls, W.STREAM)
    x["calderby"], x["skus"] = F.calderby(ls, W.STREAM)
    x["deliveries"] = F.deliveries(W.STREAM, x["wrenfold"], x["gorsedale"], x["calderby"])
    x["quotes"], x["sample"] = PB.quotes(ls, W.STREAM)
    x["levels"] = PB.published_index(x["quotes"])
    import numpy as np
    rng = np.random.default_rng([W.STREAM, 501])
    x["base"] = {code: round(float(rng.uniform(118, 142)), 1) for code in W.ICODE}
    x["coverage"] = CV.build(W.STREAM)
    return x


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or world()
    n = {}
    n["wrenfold"] = P.write_csv(f("wrenfold"), P.WREN_COLS, x["wrenfold"])
    n["gorsedale"] = P.write_csv(f("gorsedale"), P.GORS_COLS, x["gorsedale"], delimiter="|", lineterminator="\n")
    n["calendar"] = P.write_csv(f("calendar"), P.CAL_COLS, F.calendar_rows())
    n["calderby"] = P.write_calderby(f("calderby"), x["calderby"], x["skus"])
    n["classes"] = P.write_csv(f("classes"), P.CLASS_COLS, P.classification_rows(x["lines"], W.STREAM))
    P.published_workbook(f("published"), x["levels"], x["base"])
    n["deliveries"] = P.write_csv(f("deliveries"), P.DELIV_COLS, x["deliveries"])
    n["quotes"] = P.write_csv(f("quotes"), P.QUOTE_COLS, P.quote_rows(x["quotes"]))
    P.returns_workbook(f("returns"), x["coverage"])
    n["catmap"] = P.write_csv(f("catmap"), P.MAP_COLS, x["coverage"]["map"])
    P.spending_workbook(f("spending"), x["coverage"])
    P.rsi_workbook(f("rsi"), W.STREAM)
    DC.write_plan(f("plan"))
    DC.write_dictionary(f("dict"), n)
    n["manifest"] = DC.write_manifest(f("manifest"), n)
    lawson = W.PEOPLE["prices"]
    PP.normalize_ooxml(f("published"), "Prices Statistics", "Prices Statistics", "2024-02-14T09:12:00Z",
                       "2026-10-15T08:30:04Z", excel=True, company=W.ORG)
    PP.normalize_ooxml(f("returns"), "Business Statistics", "Business Statistics", "2026-02-27T10:05:00Z",
                       "2026-04-30T14:48:31Z", excel=True, company=W.ORG)
    PP.normalize_ooxml(f("spending"), "Household Statistics", lawson, "2026-07-20T13:40:00Z", "2026-07-22T09:02:17Z",
                       excel=True, company=W.ORG)
    PP.normalize_ooxml(f("rsi"), "Business Statistics", "Business Statistics", "2023-03-01T10:00:00Z",
                       "2026-09-18T08:30:41Z", excel=True, company=W.ORG)
    PP.normalize_ooxml(f("dict"), lawson, lawson, "2026-10-19T11:20:00Z", "2026-10-21T15:37:09Z", excel=True,
                       company=W.ORG)
    PP.normalize_pdf(f("plan"), b"D:20260624101500+01'00'", b"D:20260624101500+01'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 21, 16, 42, 0)
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
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["prices"], W.PEOPLE["prices"],
                       "2026-10-22T08:05:00Z", "2026-10-28T16:52:30Z", excel=False, company=W.ORG)
    ts = dt.datetime(2026, 10, 28, 17, 52, tzinfo=KELLESAY).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
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
