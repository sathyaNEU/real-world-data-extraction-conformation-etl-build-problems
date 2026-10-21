"""Build task479: the pack into <task>/target, the golden deliverable into <task>/golden, metadata.json,
submission.md and generator/figures.json; then the checks and the independent verifier, a second full build into a
scratch folder inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task479/generator/build.py              everything
    python3 task479/generator/build.py --out DIR    the pack only, into DIR
    python3 task479/generator/build.py --fast       one build with the checks, no second build or zip
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
LOCAL = dt.timezone(dt.timedelta(hours=-5))
AS_OF = {"enroll": "2026-10-07 05:40", "lag_old": "2026-06-03 06:15", "lag_new": "2026-10-07 06:05",
         "reimb": "2026-07-31 14:20", "hcc": "2026-10-07 06:30", "policy": "2026-09-30 15:45",
         "rates": "2026-09-30 17:10", "memo": "2026-10-06 16:30", "plan": "2026-09-30 10:05",
         "rebates": "2026-05-12 09:00", "roster": "2026-10-01 08:00", "survey": "2026-04-15 12:00",
         "dictionary": "2026-10-07 08:50", "manifest": "2026-10-07 08:55"}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or W.build()
    P.ids(x)
    P.lag_cells(x)
    n = {}
    n["enroll"] = P.write_csv(f("enroll"), P.ENROLL_COLS, P.enroll_rows(x))
    n["lag_old"] = P.write_csv(f("lag_old"), P.LAG_OLD_COLS, P.lag_rows(x, "old"))
    n["lag_new"] = P.write_csv(f("lag_new"), P.LAG_NEW_COLS, P.lag_rows(x, "new"))
    n["reimb"] = P.write_csv(f("reimb"), P.REIMB_COLS, P.reimb_rows(x))
    n["hcc"] = P.write_csv(f("hcc"), P.HCC_COLS, P.hcc_rows(x))
    n["policy"] = P.write_csv(f("policy"), P.POLICY_COLS, P.policy_rows())
    n["rebates"] = P.write_csv(f("rebates"), P.REBATE_COLS, P.rebate_rows(x))
    n["roster"] = P.write_csv(f("roster"), P.ROSTER_COLS, P.roster_rows())
    n["survey"] = P.write_csv(f("survey"), P.SURVEY_COLS, P.survey_rows())
    DC.write_rates(f("rates"), x)
    PP.normalize_ooxml(f("rates"), "Michelle Patrick", "Michelle Patrick", "2026-09-04T15:20:00Z",
                       "2026-09-30T22:10:00Z", excel=True, company=P.COMPANY)
    DC.write_memo(f("memo"))
    PP.normalize_pdf(f("memo"), b"D:20261006152214-05'00'", b"D:20261006163002-05'00'")
    DC.write_plan(f("plan"))
    PP.normalize_pdf(f("plan"), b"D:20260929141907-05'00'", b"D:20260930100511-05'00'")
    n["dictionary"] = P.write_csv(f("dictionary"), DC.DICT_COLS, DC.dictionary_rows())
    n["manifest"] = P.write_csv(f("manifest"), DC.MANIFEST_COLS, DC.manifest_rows(n))
    for k in P.FILES:
        t = dt.datetime.strptime(AS_OF[k], "%Y-%m-%d %H:%M").replace(tzinfo=LOCAL).timestamp()
        os.utime(f(k), (t, t))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(P.FILES), P.FILES[big], n[big]))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), LOCAL)
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
    GO.main(os.path.join(root, "target"), gdir, fig)
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
