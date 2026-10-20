"""Build task468: the pack into <task>/target, the golden workbook into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task468/generator/build.py              everything
    python3 task468/generator/build.py --out DIR    the pack only, into DIR
    python3 task468/generator/build.py --fast       one build with the checks, no second build or zip
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

PDF_STAMPS = {
    "spec": (b"D:20250512153204-05'00'", b"D:20250512153204-05'00'"),
    "linknote": (b"D:20261007101512-05'00'", b"D:20261007101512-05'00'"),
    "claimnotes": (b"D:20261005092740-05'00'", b"D:20261005092740-05'00'"),
    "layout": (b"D:20241118143055-06'00'", b"D:20241118143055-06'00'"),
    "profiles": (b"D:20260120111603-06'00'", b"D:20260120111603-06'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company
    "scores": ("Halbrook Analytics", "Halbrook Analytics", "2026-10-02T13:05:00Z", "2026-10-02T14:41:22Z", W.PLAN),
    "readmissions": ("Quality Analytics", "Quality Analytics", "2026-08-31T15:20:00Z", "2026-08-31T19:08:47Z", W.PLAN),
    "disputes": ("Provider Disputes", "Provider Disputes", "2025-01-06T16:02:00Z", "2026-10-01T13:26:51Z", W.PLAN),
}
AS_OF = {   # each file's date as its source dated it
    "claims": "2026-10-05", "encounters": "2026-10-06", "enrollment": "2026-10-05", "activity": "2026-10-05",
    "linkage": "2026-10-07", "scores": "2026-10-02", "roster": "2026-01-15", "spec": "2025-05-12",
    "linknote": "2026-10-07", "claimnotes": "2026-10-05", "layout": "2024-11-18", "readmissions": "2026-08-31",
    "profiles": "2026-01-20", "disputes": "2026-10-01",
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or P.everything()
    n = {}
    n["claims"] = P.write_csv(f("claims"), P.CLAIM_COLS, P.claim_rows(x))
    n["encounters"] = P.write_encounters(f("encounters"), x)
    n["enrollment"] = P.write_csv(f("enrollment"), P.ENROLL_COLS, P.enrollment_rows(x))
    n["activity"] = P.write_csv(f("activity"), P.ACT_COLS, P.activity_rows(x))
    links, n_sent = P.link_rows(x)
    n["linkage"] = P.write_csv(f("linkage"), P.LINK_COLS, links, crlf=True)
    n["roster"] = P.write_csv(f("roster"), P.ROSTER_COLS, P.roster_rows())
    DC.write_scores(f("scores"), P.score_rows(x))
    if P.converge_links(x, out):            # C1: no class at a hospital short of its expected false links
        links, n_sent = P.link_rows(x)
        n["linkage"] = P.write_csv(f("linkage"), P.LINK_COLS, links, crlf=True)
    DC.write_disputes(f("disputes"), P.dispute_rows(x))
    DC.write_spec(f("spec"))
    DC.write_linknote(f("linknote"), n_sent, len(links))
    DC.write_claimnotes(f("claimnotes"))
    DC.write_layout(f("layout"))
    DC.write_readmissions(f("readmissions"), P.readmission_rows(x))
    DC.write_profiles(f("profiles"), P.profile_rows())
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=CENTRAL).timestamp()
        os.utime(f(k), (ts, ts))
    x["n_sent"] = n_sent
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
