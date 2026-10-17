"""Build task464: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task464/generator/build.py              everything
    python3 task464/generator/build.py --out DIR    the pack only, into DIR
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
STAMP = dt.datetime(2026, 11, 20, 14, 25, tzinfo=EASTERN)      # the folder as the programme office assembled it


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or S.everything()
    n = {}
    n["glra"] = P.write_csv(f("glra"), P.GLRA_COLS, P.glra_rows(x))
    n["crosswalk"] = P.write_csv(f("crosswalk"), P.XWALK_COLS, P.xwalk_rows(x))
    n["slm"] = P.write_csv(f("slm"), P.SLM_COLS, P.slm_rows(x))
    n["bridge"] = P.write_csv(f("bridge"), P.BRIDGE_COLS, P.bridge_rows(x))
    n["enrollment"] = P.write_csv(f("enrollment"), P.ENROL_COLS, P.enrol_rows(x))
    n["nonpublic"] = P.write_csv(f("nonpublic"), P.NONPUBLIC_COLS, P.nonpublic_rows())
    n["finance"] = P.write_csv(f("finance"), P.FIN_COLS, P.finance_rows(x))
    n["gradrate"] = P.write_csv(f("gradrate"), P.GRAD_COLS, P.grad_rows(x))
    n["directory"] = DC.write_directory(f("directory"), x)
    DC.write_rules(f("rules"))
    DC.write_glra_guide(f("glra_guide"))
    DC.write_slm_summary(f("slm_report"), x)
    DC.write_bridge_memo(f("bridge_memo"), x)
    DC.write_resolution(f("resolution"))
    n["dict"] = DC.write_dictionary(f("dict"))
    n["register"] = DC.write_register(f("register"), {k: v for k, v in n.items() if k != "directory"})
    PP.normalize_ooxml(f("directory"), "Office of Data Management", "Office of Data Management", "2026-09-22T13:05:00Z",
                       "2026-10-01T19:47:31Z", excel=True, company=W.STATE_AGENCY)
    PP.normalize_pdf(f("rules"), b"D:20261016101500-04'00'", b"D:20261016101500-04'00'")
    PP.normalize_pdf(f("glra_guide"), b"D:20250815093000-04'00'", b"D:20250815093000-04'00'")
    PP.normalize_pdf(f("slm_report"), b"D:20260626153000-04'00'", b"D:20260626153000-04'00'")
    PP.normalize_pdf(f("bridge_memo"), b"D:20260821111500-04'00'", b"D:20260821111500-04'00'")
    PP.normalize_pdf(f("resolution"), b"D:20260813164500-04'00'", b"D:20260813164500-04'00'")
    asof = {k: d for k, src, desc, d in DC.REGISTER}
    for i, k in enumerate(W.FILES):
        if k in asof and k != "dict":
            y, m, d = (int(v) for v in asof[k].split("-"))
            ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=EASTERN).timestamp()
        else:
            ts = STAMP.timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max((k for k in n if k != "directory"), key=lambda k: n[k])
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
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["director"], W.PEOPLE["director"],
                       "2026-11-20T15:10:00Z", "2026-11-23T21:42:16Z", excel=False, company=W.STATE_AGENCY)
    ts = dt.datetime(2026, 11, 23, 16, 42, tzinfo=EASTERN).timestamp()
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
