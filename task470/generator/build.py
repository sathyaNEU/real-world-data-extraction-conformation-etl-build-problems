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

import numpy as np       # noqa: E402

import pack as P         # noqa: E402
import sim               # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
OSLO = dt.timezone(dt.timedelta(hours=1))

PDF_STAMPS = {"regulation": (b"D:20261014113207+02'00'", b"D:20261014113207+02'00'")}
AS_OF = {   # each file's date as its source dated it
    "regulation": "2026-10-14", "assignment": "2026-12-01", "cadastre": "2027-01-04", "municipalities": "2026-01-02",
    "meterpoints": "2027-01-04", "hourly": "2026-12-14", "register": "2027-01-05", "events": "2027-01-05",
    "titles": "2027-01-05", "transfers": "2027-01-05", "entities": "2027-01-05", "shareholders": "2026-05-29",
    "prices": "2026-11-23", "outages": "2026-12-03",
}


def build(out, w=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    if w is None:
        w = sim.build()
        P.prepare(w)
    rng = np.random.default_rng(W.SEED + 1)
    n = {}
    n["cadastre"] = P.write_cadastre(w, f("cadastre"))
    n["municipalities"] = P.write_municipalities(f("municipalities"))
    n["meterpoints"] = P.write_meterpoints(w, f("meterpoints"), rng)
    n["hourly"] = P.write_hourly(w, f("hourly"), rng)
    n["register"] = P.write_register(w, f("register"))
    n["events"] = P.write_events(w, f("events"), rng)
    n["titles"] = P.write_titles(w, f("titles"))
    n["transfers"] = P.write_transfers(w, f("transfers"))
    n["entities"] = P.write_entities(w, f("entities"))
    n["shareholders"] = P.write_shareholders(w, f("shareholders"))
    n["prices"] = P.write_prices(w, f("prices"))
    n["outages"] = P.write_outages(w, f("outages"))
    DC.write_regulation(f("regulation"))
    DC.write_assignment(f("assignment"))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    PP.normalize_ooxml(f("outages"), "Driftssentralen", "Driftssentralen", "2026-12-02T13:05:00Z",
                       "2026-12-03T08:41:27Z", excel=True, company="Hvitfjell Nett AS")
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 8 + (i * 5) % 9, (i * 13) % 60, tzinfo=OSLO).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(W.FILES), W.FILES[big], n[big]))
    return n, w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), OSLO)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, w=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n, w = build(os.path.join(root, "target"), w=w, quiet=quiet)
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
    return w


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    w = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), w=w,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    vgood = V.main(os.path.join(TASK, "target"), os.path.join(HERE, "figures.json"))
    if fast:
        if not (good and vgood):
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
    if not (good and vgood):
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
