"""Build task470: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task470/generator/build.py              everything
    python3 task470/generator/build.py --out DIR    the pack only, into DIR
    python3 task470/generator/build.py --fast       one build with the checks, no second build or zip
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
PACIFIC = dt.timezone(dt.timedelta(hours=-8))

PDF_STAMPS = {
    "method": (b"D:20260318101544-07'00'", b"D:20260318101544-07'00'"),
    "grants": (b"D:20261204152210-08'00'", b"D:20261204152210-08'00'"),
    "network": (b"D:20250602094730-07'00'", b"D:20270108161205-08'00'"),
    "reg_notes": (b"D:20270203113918-08'00'", b"D:20270203113918-08'00'"),
    "f37": (b"D:20270122140027-08'00'", b"D:20270122140027-08'00'"),
    "g42": (b"D:20270129083351-08'00'", b"D:20270129083351-08'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company
    "based": (W.STATE_OFFICE, "Aviation Planning", "2026-12-14T17:20:00Z", "2027-01-05T19:02:41Z", W.STATE_OFFICE),
    "directory": (W.STATE_OFFICE, "Aviation Planning", "2026-10-21T16:05:00Z", "2026-11-01T15:47:12Z",
                  W.STATE_OFFICE),
    "l08": ("Pellam Airfield Services", "Pellam Airfield Services", "2027-01-12T18:11:00Z", "2027-01-15T22:30:54Z",
            "Pellam Airfield Services"),
    "d19": ("Ardley Counts LLC", "Ardley Counts LLC", "2027-01-20T17:40:00Z", "2027-01-22T21:03:19Z",
            "Ardley Counts LLC"),
    "m5010": (W.STATE_OFFICE, "Airport Inspections", "2026-09-29T20:13:00Z", "2026-09-30T16:22:08Z", W.STATE_OFFICE),
}
AS_OF = {   # each file's date as its source dated it
    "events": "2027-01-08", "master": "2027-02-01", "dereg": "2027-02-01", "acftref": "2027-02-01",
    "engine": "2027-02-01", "reg_notes": "2027-02-03", "based": "2027-01-05", "atct": "2027-01-12",
    "f37": "2027-01-22", "l08": "2027-01-15", "g42": "2027-01-29", "d19": "2027-01-22", "method": "2026-03-18",
    "grants": "2026-12-04", "network": "2027-01-08", "directory": "2026-11-01", "m5010": "2026-09-30",
    "pbmon": "2027-02-02",
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
    n["events"] = P.write_csv(f("events"), P.EVENT_COLS, P.event_rows(x))
    n["master"] = P.write_padded(f("master"), P.MASTER_COLS, P.master_rows(x))
    n["dereg"] = P.write_padded(f("dereg"), P.DEREG_COLS, P.dereg_rows(x))
    n["acftref"] = P.write_padded(f("acftref"), P.ACFTREF_COLS, P.acftref_rows(x))
    n["engine"] = P.write_padded(f("engine"), P.ENGINE_COLS, P.engine_rows(x))
    n["atct"] = P.write_csv(f("atct"), P.ATCT_COLS, P.atct_rows(x), crlf=True)
    n["pbmon"] = P.write_csv(f("pbmon"), P.PBMON_COLS, P.pbmon_rows(x))
    DC.write_method(f("method"))
    DC.write_grants(f("grants"))
    DC.write_network(f("network"))
    DC.write_reg_notes(f("reg_notes"))
    DC.write_f37(f("f37"), x)
    DC.write_g42(f("g42"), x)
    DC.write_l08(f("l08"), x)
    DC.write_d19(f("d19"), x)
    DC.write_based(f("based"), x)
    DC.write_directory(f("directory"), x)
    DC.write_5010(f("m5010"), x)
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=PACIFIC).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), PACIFIC)
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
