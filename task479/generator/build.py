"""Build task479: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

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
CENTRAL = dt.timezone(dt.timedelta(hours=-5))
PDF_STAMPS = {"guidelines": (b"D:20260813162210-05'00'", b"D:20260814091544-05'00'"),
              "closeout": (b"D:20260219103128-06'00'", b"D:20260902151907-05'00'")}
OOXML = {   # creator, last modified by, created, modified, company
    "register": ("TSRFA Grants", "TSRFA Grants", "2026-09-30T22:04:00Z", "2026-09-30T22:04:00Z", P.COMPANY_NAME),
}
AS_OF = {"policies": "2026-10-02 06:12", "claims1": "2026-10-02 06:31", "claims2": "2026-10-02 06:40",
         "register": "2026-09-30 17:04", "crosswalk": "2026-09-30 17:20", "offsets": "2013-04-22 14:05",
         "members": "2026-10-02 10:48", "crs": "2026-10-01 09:12", "firm": "2026-09-30 16:31",
         "guidelines": "2026-08-14 09:15", "closeout": "2026-09-02 15:19", "dictionary": "2026-10-02 11:36",
         "manifest": "2026-10-02 11:41"}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or W.build()
    P.property_ids(x)
    n = {}
    n["policies"] = P.write_csv(f("policies"), P.POLICY_COLS, P.policy_rows(x))
    n["claims1"] = P.write_csv(f("claims1"), P.CLAIM1_COLS, P.claim_rows(x, 1))
    n["claims2"] = P.write_csv(f("claims2"), P.CLAIM2_COLS, P.claim_rows(x, 2))
    props, insp = P.register_rows(x)
    pr = P.project_rows(x)
    n["register"] = P.write_xlsx(f("register"), [("Projects", P.PROJECT_COLS, pr, (6, 7), (9, 10)),
                                                ("Properties", P.PROPERTY_COLS, props, (8,), (5, 6)),
                                                ("Inspections", P.INSPECTION_COLS, insp, (3,), ())])
    n["crosswalk"] = P.write_csv(f("crosswalk"), P.CROSS_COLS, P.crosswalk_rows(x))
    n["offsets"] = P.write_csv(f("offsets"), P.OFFSET_COLS, P.offset_rows())
    n["members"] = P.write_csv(f("members"), P.MEMBER_COLS, P.member_rows())
    n["crs"] = P.write_csv(f("crs"), P.CRS_COLS, P.crs_rows())
    n["firm"] = P.write_csv(f("firm"), P.FIRM_COLS, P.firm_rows())
    DC.write_guidelines(f("guidelines"))
    DC.write_closeout(f("closeout"), x)
    DC.write_dictionary(f("dictionary"))
    n["manifest"] = P.write_csv(f("manifest"), DC.MANIFEST_COLS, DC.manifest_rows(n))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for k in P.FILES:
        t = dt.datetime.strptime(AS_OF[k], "%Y-%m-%d %H:%M").replace(tzinfo=CENTRAL).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), CENTRAL)
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
