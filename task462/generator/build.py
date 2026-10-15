"""Build task462: the pack into <task>/target, the goldens into <task>/golden, metadata.json and generator/figures.json;
then the checks and the independent verifier, a second full build into a scratch folder inside the task compared
byte for byte, and target.zip cut from the final build.

    python3 task462/generator/build.py              everything
    python3 task462/generator/build.py --out DIR    the pack only, into DIR
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

import basin as B        # noqa: E402
import distract as D     # noqa: E402
import flaring as FL     # noqa: E402
import pack as P         # noqa: E402
import plant as PL       # noqa: E402
import production as PR  # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL = dt.timezone(dt.timedelta(hours=-6))
STAMP = dt.datetime(2026, 11, 18, 9, 26, tzinfo=CENTRAL)       # the folder as the ratings team assembled it


def world():
    x = B.world(W.SEED)
    rng = np.random.default_rng(W.SEED + 11)
    x["wells"] = PR.wells(rng, x["sites"])
    x["rows"] = PR.monthly(rng, x["sites"], x["wells"])
    x["owells"], x["orows"] = PR.other_wells(W.SEED)
    x["plant"] = PL.build(W.SEED, x["rows"] + x["orows"])
    x["flaring"] = FL.build(W.SEED, x["sites"], x["wells"], x["rows"], x["owells"], x["orows"])
    x["ghgrp"] = D.ghgrp(W.SEED, x["truth"])
    x["satellite"] = D.satellite(W.SEED, sum(x["truth"].values()) * 1.35)
    x["precs"] = P.plume_records(x)
    x["register"] = B.register(W.SEED, x)
    return x


def campaign_summary(x):
    out = []
    for c, d0, d1 in W.CAMPAIGNS:
        lost = len(x["plan"][c]["lost"])
        n = sum(1 for p in x["precs"] if p["campaign"] == c)
        out.append([c, "%s to %s" % (d0.strftime("%d %b %Y").lstrip("0"), d1.strftime("%d %b %Y").lstrip("0")), 18 - lost, lost,
                    format(n, ",")])
    return out


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or world()
    n = {}
    n["plumes"] = P.write_csv(f("plumes"), P.PLUME_COLS, P.plume_rows(x["precs"]))
    n["coverage"] = P.write_csv(f("coverage"), P.COVER_COLS, P.coverage_rows(x))
    n["sites"] = P.write_csv(f("sites"), P.SITE_COLS, P.site_rows(x["register"], x["wells"], W.SEED))
    n["production"] = P.write_csv(f("production"), P.PROD_COLS, P.production_rows(
        [r for r in x["rows"] + x["orows"] if (r["y"], r["m"]) >= (W.RATING_START.year, W.RATING_START.month)]))
    n["operators"] = P.write_csv(f("operators"), P.OPER_COLS, P.operator_rows(W.SEED))
    n["gas"] = P.write_csv(f("gas"), P.GAS_COLS, P.gas_rows(W.SEED))
    n["flaring"] = P.write_csv(f("flaring"), P.FLARE_COLS, P.flaring_rows(x["flaring"]))
    n["leases"] = P.write_csv(f("leases"), P.LEASE_COLS, P.lease_rows(x["flaring"]))
    n["basin"] = P.write_csv(f("basin"), P.BASIN_COLS, P.basin_rows(FL.basin_summary(x["flaring"])))
    n["statements"] = P.write_csv(f("statements"), P.STATEMENT_COLS, P.statement_rows(x["plant"]))
    n["stations"] = P.write_csv(f("stations"), P.STATION_COLS, P.station_rows(x["plant"], W.SEED))
    n["heating"] = P.write_csv(f("heating"), P.HEAT_COLS, P.heating_rows(x["plant"]))
    n["ghgrp"] = P.write_csv(f("ghgrp"), P.GHGRP_COLS, P.ghgrp_rows(x["ghgrp"]))
    with open(f("satellite"), "w") as fh:
        fh.write(D.satellite_json(x["satellite"]))
    DC.write_releases(f("releases"), x["releases"])
    DC.write_standard(f("standard"))
    DC.write_methods(f("methods"), campaign_summary(x))
    DC.write_dictionary(f("dict"), n)
    n["manifest"] = DC.write_manifest(f("manifest"), n)
    PP.normalize_ooxml(f("releases"), W.PEOPLE["provider"], W.PEOPLE["provider"], "2025-11-18T16:05:00Z",
                       "2025-11-20T19:42:13Z", excel=True, company=W.PROVIDER)
    PP.normalize_ooxml(f("dict"), W.PEOPLE["ratings"], W.PEOPLE["ratings"], "2026-11-16T15:10:00Z",
                       "2026-11-18T15:21:44Z", excel=True, company=W.ORG)
    PP.normalize_pdf(f("standard"), b"D:20260902103000-06'00'", b"D:20260902103000-06'00'")
    PP.normalize_pdf(f("methods"), b"D:20261012141500-06'00'", b"D:20261012141500-06'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 11, 18, 9, 26, 0)
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
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["ratings"], W.PEOPLE["ratings"],
                       "2026-11-30T15:05:00Z", "2026-12-03T22:18:40Z", excel=False, company=W.ORG)
    ts = dt.datetime(2026, 12, 3, 16, 18, tzinfo=CENTRAL).timestamp()
    for f in os.listdir(gdir):
        os.utime(os.path.join(gdir, f), (ts, ts))
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
        same = {f: open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
                for f in ("metadata.json", "submission.md", os.path.join("generator", "figures.json"))}
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
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
