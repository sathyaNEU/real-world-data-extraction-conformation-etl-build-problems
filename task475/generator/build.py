"""Build task475: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task475/generator/build.py              everything
    python3 task475/generator/build.py --out DIR    the pack only, into DIR
    python3 task475/generator/build.py --fast       one build with the checks, no second build or zip
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
PDF_STAMPS = {"dor": (b"D:20260715093814-04'00'", b"D:20260715093814-04'00'"),
              "policy": (b"D:20260514161022-04'00'", b"D:20260518083541-04'00'"),
              "closeout": (b"D:20260224141706-05'00'", b"D:20260224141706-05'00'")}
OOXML = {   # creator, last modified by, created, modified, company
    "rel": ("SGIO Address Programs", "SGIO Address Programs", "2024-03-01T14:20:00Z", "2024-03-05T13:02:44Z",
            "State Geographic Information Office"),
    "rel_rev": ("SGIO Address Programs", "SGIO Address Programs", "2024-03-01T14:31:00Z", "2024-03-05T13:04:09Z",
                "State Geographic Information Office"),
}
AS_OF = {"irs23": "2026-06-22 10:41", "irs22": "2025-04-02 15:12", "rel": "2024-03-05 09:04",
         "rel_rev": "2024-03-05 09:04", "dor": "2026-07-15 09:38", "policy": "2026-05-18 08:35",
         "members": "2026-10-02 11:20", "agencies": "2026-10-02 11:22", "jobs": "2026-09-30 18:05",
         "history": "2026-09-30 18:09", "ledger": "2026-10-01 07:46", "closeout": "2026-02-24 14:17",
         "dictionary": "2026-10-02 11:58", "manifest": "2026-10-02 12:03"}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or W.build()
    n = {}
    n["irs23"] = P.write_csv(f("irs23"), P.IRS23_COLS, P.irs_rows(x["pub"]))
    n["irs22"] = P.write_csv(f("irs22"), P.IRS22_COLS, P.irs_rows(x["pub22"]))
    n["rel"] = P.write_xlsx(f("rel"), "ZIP_COUNTY_2023Q4", P.REL_COLS, P.rel_rows(x["rel"]), ratio_cols=(2, 3, 4, 5))
    n["rel_rev"] = P.write_xlsx(f("rel_rev"), "COUNTY_ZIP_2023Q4", P.REV_COLS, P.rev_rows(x["rel"]),
                                ratio_cols=(2, 3, 4, 5))
    DC.write_dor(f("dor"), x)
    DC.write_policy(f("policy"))
    n["members"] = P.write_csv(f("members"), P.MEMBER_COLS, P.member_rows())
    n["agencies"] = P.write_csv(f("agencies"), P.AGENCY_COLS, P.agency_rows())
    n["jobs"] = P.write_csv(f("jobs"), P.JOB_COLS, P.job_rows(x))
    n["history"] = P.write_csv(f("history"), P.HIST_COLS, P.history_rows(x))
    n["ledger"] = P.write_csv(f("ledger"), P.LEDGER_COLS, P.ledger_rows(x))
    DC.write_closeout(f("closeout"), x)
    DC.write_dictionary(f("dictionary"))
    n["manifest"] = P.write_csv(f("manifest"), DC.MANIFEST_COLS, DC.manifest_rows(n))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for k in P.FILES:
        t = dt.datetime.strptime(AS_OF[k], "%Y-%m-%d %H:%M").replace(tzinfo=EASTERN).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), EASTERN)
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
