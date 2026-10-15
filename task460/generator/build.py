"""Build task460: the pack into <task>/target, the goldens into <task>/golden, metadata.json and generator/figures.json;
then the checks and the independent verifier, a second full build into a scratch folder inside the task compared
byte for byte, and target.zip cut from the final build.

    python3 task460/generator/build.py              everything
    python3 task460/generator/build.py --out DIR    the pack only, into DIR
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

import arrays as A      # noqa: E402
import bills as B       # noqa: E402
import grid as G        # noqa: E402
import pack as P        # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-4))
STAMP = dt.datetime(2026, 10, 23, 15, 12, tzinfo=EASTERN)       # the folder as the energy team assembled it


def world():
    w = G.simulate()
    arr = A.model(w)
    series = P.hourly_series(w)
    plants = P.register(w, series)
    lines, meters = B.build()
    return dict(grid=w, arrays=arr, series=series, plants=plants, lines=lines, meters=meters)


def rates_2024(table):
    """The 2024 edition: the same areas a year earlier (weather, fuel prices and a plant's outage moving each figure)."""
    import numpy as np
    rng = np.random.default_rng(W.SEED + 2024)
    out = {}
    for code, t in table.items():
        g = t["gen"] * (1 + rng.normal(-0.012, 0.018))
        f = lambda v: round(v * (1 + rng.normal(0.01, 0.025)), 1) if v is not None else None
        mix = {k: max(v * (1 + rng.normal(0, 0.06)), 0.0) for k, v in t["mix"].items()}
        s = sum(mix.values())
        mix = {k: v / s for k, v in mix.items()}
        avg = f(t["avg"])
        out[code] = dict(gen=round(g), co2_short=round(avg * g / 2000.0), avg=avg, fossil=f(t["fossil"]), coal=f(t["coal"]),
                         gas=f(t["gas"]), oil=f(t["oil"]), nb=f(t["nb"]), mix=mix)
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
    n["hourly"] = P.write_csv(f("hourly"), P.HOURLY_COLS, P.hourly_rows(x["series"]))
    n["arrays"] = P.write_csv(f("arrays"), P.ARRAY_COLS, P.array_rows(x["arrays"]))
    n["plants"] = P.write_csv(f("plants"), P.PLANT_COLS, P.plant_rows(x["plants"]))
    n["sites"] = P.write_csv(f("sites"), P.SITE_COLS, P.site_rows())
    n["codes"] = P.write_csv(f("codes"), P.CODE_COLS, P.code_rows())
    n["utilmap"] = P.write_csv(f("utilmap"), P.UTIL_COLS, P.util_rows())
    n["invoices"] = P.write_csv(f("invoices"), P.INVOICE_COLS, P.invoice_rows(x["lines"]))
    table = P.rates_table(x["plants"])
    DC.write_rates(f("rates"), table, 2025, W.RATES_RELEASE)
    DC.write_rates(f("rates24"), rates_2024(table), 2024, W.RATES_2024_RELEASE)
    DC.write_charter(f("charter"))
    DC.write_label(f("label"))
    DC.write_dictionary(f("dict"), n)
    n["manifest"] = DC.write_manifest(f("manifest"), n)
    PP.normalize_ooxml(f("rates"), "EDC Data Release", "EDC Data Release", "2026-08-27T13:40:00Z", "2026-09-04T18:22:41Z",
                       excel=True, company=W.AGENCY)
    PP.normalize_ooxml(f("rates24"), "EDC Data Release", "EDC Data Release", "2025-09-18T13:52:00Z",
                       "2025-09-29T20:16:45Z", excel=True, company=W.AGENCY)
    PP.normalize_ooxml(f("dict"), W.PEOPLE["analyst"], W.PEOPLE["analyst"], "2026-10-06T16:20:00Z", "2026-10-23T18:58:31Z",
                       excel=True, company=W.ORG)
    PP.normalize_pdf(f("charter"), b"D:20260915103000-04'00'", b"D:20260915103000-04'00'")
    PP.normalize_pdf(f("label"), b"D:20260630091500-05'00'", b"D:20260630091500-05'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, x, table


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 23, 15, 12, 0)
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
    n, x, table = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20261113094500-05'00'", b"D:20261113094500-05'00'")
    ts = dt.datetime(2026, 11, 13, 9, 45, tzinfo=dt.timezone(dt.timedelta(hours=-5))).timestamp()
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
