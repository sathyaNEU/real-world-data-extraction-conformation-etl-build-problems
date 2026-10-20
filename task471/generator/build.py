"""Build task471: the pack into <task>/target, the golden files into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task471/generator/build.py              everything
    python3 task471/generator/build.py --out DIR    the pack only, into DIR
    python3 task471/generator/build.py --fast       one build with the checks, no second build or zip
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
    "tr2025": (b"D:20250912101544-05'00'", b"D:20250912101544-05'00'"),
    "memo": (b"D:20260209083012-06'00'", b"D:20260209083012-06'00'"),
    "standard": (b"D:20240318141107-05'00'", b"D:20240318141107-05'00'"),
    "framework": (b"D:20240611094521-05'00'", b"D:20240611094521-05'00'"),
    "adminsum": (b"D:20260731161830-05'00'", b"D:20260731161830-05'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company
    "qc26": ("Arcwright Scoring Operations", "Arcwright Scoring Operations", "2026-07-30T14:12:00Z",
             "2026-07-31T19:40:51Z", W.NEW_CO),
    "maps": ("Office of Assessment Research", "Office of Assessment Research", "2026-02-04T15:30:00Z",
             "2026-02-09T13:58:12Z", W.BOARD),
    "completers": ("Educator Preparation and Licensure", "Educator Preparation and Licensure", "2026-07-14T13:05:00Z",
                   "2026-08-04T20:22:37Z", W.BOARD),
}
AS_OF = {   # each file's date as its source dated it
    "tr2025": "2025-09-12", "memo": "2026-02-09", "standard": "2024-03-18", "framework": "2024-06-11",
    "adminsum": "2026-07-31", "maps": "2026-02-09", "conv": "2025-09-12", "scores25": "2025-07-25",
    "scores26": "2026-07-24", "items26": "2026-07-27", "reads26": "2026-07-29", "qc26": "2026-07-31",
    "history": "2026-08-18", "crosswalk": "2026-08-14", "completers": "2026-08-04", "register": "2026-08-18",
    "directory": "2026-01-12",
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or P.everything()
    n = {}
    n["conv"] = P.write_csv(f("conv"), ["RAW_SCORE", "SCALE_SCORE"], P.conversion_rows())
    n["history"] = P.write_csv(f("history"), P.HISTORY_COLS, P.history_rows(x))
    n["register"] = P.write_csv(f("register"), P.REGISTER_COLS, P.register_rows(x))
    n["scores25"] = P.write_csv(f("scores25"), P.SCORES25_COLS, P.scores25_rows(x), crlf=True)
    n["scores26"] = P.write_csv(f("scores26"), P.SCORES26_COLS, P.scores26_rows(x))
    n["items26"] = P.write_csv(f("items26"), P.ITEMS26_COLS, P.items26_rows(x))
    reads = P.reads_rows(x)
    n["reads26"] = P.write_csv(f("reads26"), P.READ_COLS, reads)
    n["crosswalk"] = P.write_csv(f("crosswalk"), P.CROSSWALK_COLS, P.crosswalk_rows(x))
    n["directory"] = P.write_csv(f("directory"), P.DIRECTORY_COLS, P.directory_rows())
    st = DC.stats(x)
    summary, readers = DC.qc_tables(x, reads)
    DC.write_qc(f("qc26"), x, summary, readers)
    DC.write_maps(f("maps"), x)
    DC.write_completers(f("completers"), P.submission_sheets(x))
    DC.write_tr2025(f("tr2025"), x, st)
    DC.write_memo(f("memo"), x)
    DC.write_standard(f("standard"))
    DC.write_framework(f("framework"))
    DC.write_adminsum(f("adminsum"), x, summary)
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(P.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=CENTRAL).timestamp()
        os.utime(f(k), (ts, ts))
    x["qc_summary"] = summary
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
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), sorted(os.listdir(gdir)))
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
    good &= bool(V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden")))
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
