"""Build task471: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

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
EASTERN = dt.timezone(dt.timedelta(hours=-5))

PDF_STAMPS = {
    "methods": (b"D:20261215142207-05'00'", b"D:20261215142207-05'00'"),
    "handout": (b"D:20261211093416-05'00'", b"D:20261215141950-05'00'"),
    "standard": (b"D:20260914103502-04'00'", b"D:20260914103502-04'00'"),
    "schedule": (b"D:20270120081245-05'00'", b"D:20270120081245-05'00'"),
    "rates": (b"D:20251208160433-05'00'", b"D:20251208160433-05'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company
    "access": ("Aviation Planning", "Aviation Planning", "2025-11-18T14:02:00Z", "2026-01-09T16:37:21Z",
               "%s, %s" % (W.STATE_AGENCY, W.BUREAU)),
}
AS_OF = {   # each file's date as its source dated it
    "cards": "2026-12-15", "verbatims": "2026-12-15", "handout": "2026-12-15", "methods": "2026-12-15",
    "q1": "2027-01-06", "q2": "2027-01-06", "q3": "2027-01-06", "q4": "2027-01-06", "zips": "2026-07-22",
    "markets": "2026-07-22", "schedule": "2027-01-20", "standard": "2026-09-14", "rates": "2025-12-08",
    "tickets": "2026-12-18", "t100": "2027-01-14", "access": "2026-01-09",
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
    n["cards"] = P.write_csv(f("cards"), P.CARD_COLS, P.card_rows(x))
    n["verbatims"] = P.write_csv(f("verbatims"), P.VERBATIM_COLS, P.verbatim_rows(x))
    for q in (1, 2, 3, 4):
        cols, rows = P.register_rows(x, q)
        n["q%d" % q] = P.write_csv(f("q%d" % q), cols, rows, crlf=q <= 2)
    n["zips"] = P.write_csv(f("zips"), P.ZIP_COLS, P.zip_rows())
    n["markets"] = P.write_csv(f("markets"), P.MARKET_COLS, P.market_rows())
    n["tickets"] = P.write_csv(f("tickets"), P.TICKET_COLS, P.ticket_rows())
    n["t100"] = P.write_csv(f("t100"), P.T100_COLS, P.t100_rows())
    DC.write_methods(f("methods"), x)
    DC.write_handout(f("handout"), x)
    DC.write_standard(f("standard"))
    DC.write_schedule(f("schedule"))
    DC.write_rates(f("rates"))
    DC.write_access(f("access"))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=EASTERN).timestamp()
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
    good = V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden")) and good
    if fast:
        if not good:
            raise SystemExit("checks or verifier failed")
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
