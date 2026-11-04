"""Build task461: the pack into <task>/target, the goldens into <task>/golden, metadata.json and generator/figures.json;
then the checks and the independent verifier, a second full build into a scratch folder inside the task compared
byte for byte, and target.zip cut from the final build.

    python3 task461/generator/build.py              everything
    python3 task461/generator/build.py --out DIR    the pack only, into DIR
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

import numpy as np   # noqa: E402

import books as B    # noqa: E402
import pack as P     # noqa: E402
import sim as S      # noqa: E402
import terminal as T  # noqa: E402
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)
AEDT = dt.timezone(dt.timedelta(hours=11))
STAMP = dt.datetime(2027, 1, 8, 9, 26, tzinfo=AEDT)        # the folder as the terminal manager assembled it


def world():
    x = S.simulate()
    y = T.run(x)
    return x, y


def build(out, xy=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x, y = xy or world()
    rng = np.random.default_rng(W.SEED + 31)
    plate_hist = P.identities(x, rng)
    n = {}
    old, new = P.tms_rows(x, y, rng, plate_hist)
    n["tas_old"] = P.write_csv(f("tas_old"), P.OLD_COLS, old)
    n["tas_new"] = B.write_tms(f("tas_new"), P.NEW_COLS, new)
    n["dockets"] = P.write_csv(f("dockets"), P.DOCKET_COLS, P.docket_rows(x))
    B.write_tankers(f("tankers"), x, plate_hist)
    n["sites"] = P.write_csv(f("sites"), P.SITE_COLS, P.site_rows(x, rng))
    n["vru_cems"] = P.write_csv(f("vru_cems"), P.CEMS_COLS, P.cems_rows(x, y, rng))
    n["vru_plc"] = P.write_csv(f("vru_plc"), P.PLC_COLS, P.plc_rows(x, y, rng))
    n["gauging"] = P.write_csv(f("gauging"), P.GAUGE_COLS, P.gauge_rows(x, y, rng))
    n["outturns"] = len(P.outturn_rows(x, y, np.random.default_rng(W.SEED + 41)))
    B.write_outturns(f("outturns"), P.OUT_COLS, P.outturn_rows(x, y, np.random.default_rng(W.SEED + 41)))
    n["shiftlog"] = P.write_csv(f("shiftlog"), P.LOG_COLS, P.shift_log_rows(x, y, rng))
    n["workorders"] = P.write_csv(f("workorders"), P.WO_COLS, P.work_order_rows(x, rng))
    B.write_tank_register(f("tankreg"))
    n["weather"] = P.write_csv(f("weather"), P.WX_COLS, P.weather_rows(x, rng))
    DC.write_licence(f("licence"))
    DC.write_protocol(f("protocol"))
    DC.write_stack_test(f("stacktest"))
    for k, who, c, m in (("tas_new", "agardner", "2027-01-03T20:12:00Z", "2027-01-03T20:12:00Z"),
                         ("tankers", W.PEOPLE["dispatch"], "2023-02-14T01:05:00Z", "2027-01-06T23:41:00Z"),
                         ("tankreg", W.PEOPLE["manager"], "2019-07-30T04:20:00Z", "2027-01-07T22:18:00Z"),
                         ("outturns", W.PEOPLE["manager"], "2026-01-09T03:00:00Z", "2027-01-05T00:47:00Z")):
        PP.normalize_ooxml(f(k), who, who, c, m, excel=True, company=W.ORG)
    PP.normalize_pdf(f("licence"), b"D:20250303100000+11'00'", b"D:20250303100000+11'00'")
    PP.normalize_pdf(f("protocol"), b"D:20260202093000+11'00'", b"D:20260202093000+11'00'")
    PP.normalize_pdf(f("stacktest"), b"D:20260902141500+10'00'", b"D:20260902141500+10'00'")
    ts = STAMP.timestamp()
    for k in W.FILES:
        os.utime(f(k), (ts, ts))
    return n, (x, y)


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 1, 8, 9, 26, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    import writeup as WU
    n, xy = build(os.path.join(root, "target"), quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    DL.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return xy, n


def main():
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    xy, n = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), xy=xy, n=n,
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
