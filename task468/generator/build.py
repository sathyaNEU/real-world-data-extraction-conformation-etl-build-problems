"""Build task468: the pack into <task>/target, the golden workbook into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task468/generator/build.py              everything
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
import sim as S          # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL = dt.timezone(dt.timedelta(hours=-5))
PDF_STAMPS = {"charter": b"D:20260528141205-05'00'", "bulletin": b"D:20251208093310-06'00'",
              "transition": b"D:20260714162544-05'00'", "trend": b"D:20260220110402-06'00'"}


def trend_table(x):
    f = x["fills"]
    out = []
    for c in W.CANDIDATES:
        g = f[(f["cls"] == c)]
        yrs = {}
        for y in (2024, 2025):
            gy = g[[d.year == y for d in g["date"]]]
            paid = (gy["units"] * gy["price"] * W.ORRIN_PRICE_FACTOR[y] + 1.5).sum()
            yrs[y] = (float(paid), int(gy["member"].nunique()))
        out.append((c, yrs[2024][0], yrs[2025][0], yrs[2025][1]))
    return out


def infusion_table():
    return [("Inflammatory conditions (infused biologics)", 412, 3196, 14_208_340),
            ("Multiple sclerosis (infused therapy)", 96, 233, 6_051_772),
            ("Oncology (infused and injected)", 1_183, 9_874, 61_405_218),
            ("Severe asthma (clinic-administered)", 37, 302, 1_247_910),
            ("Osteoporosis (injected)", 655, 1_271, 2_163_486),
            ("Ophthalmology (intravitreal)", 1_048, 6_912, 13_870_455)]


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or S.simulate()
    orrin, tallis = P.claims(x)
    n = {}
    n["orrin"] = P.write_csv(f("orrin"), P.ORRIN_COLS, orrin)
    n["tallis"] = P.write_csv(f("tallis"), P.TALLIS_COLS, tallis)
    n["crosswalk"] = P.write_csv(f("crosswalk"), P.XWALK_COLS, P.crosswalk_rows(x))
    n["drugs"] = P.write_csv(f("drugs"), P.DRUG_COLS, P.drug_rows())
    DC.write_prices(f("prices"), P.price_rows())
    DC.write_rebates(f("rebates"), P.rebate_rows(x))
    DC.write_infusions(f("infusions"), infusion_table())
    DC.write_charter(f("charter"))
    DC.write_bulletin(f("bulletin"))
    DC.write_transition(f("transition"))
    DC.write_trend(f("trend"), trend_table(x))
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    PP.normalize_ooxml(f("prices"), "Network Pricing", "Network Pricing", "2025-12-10T15:02:00Z", "2025-12-15T19:44:21Z",
                       excel=True, company=W.NEW_PBM)
    PP.normalize_ooxml(f("rebates"), "Rebate Operations", "Rebate Operations", "2026-04-15T13:41:00Z",
                       "2026-04-17T18:22:51Z", excel=True, company=W.OLD_PBM)
    PP.normalize_ooxml(f("infusions"), "Medical Economics", "Medical Economics", "2026-03-06T14:10:00Z",
                       "2026-03-09T16:48:12Z", excel=True, company=W.PLAN)
    asof = {k: d for k, src, d, desc in DC.INDEX}
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in asof[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=CENTRAL).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(W.FILES), W.FILES[big], n[big]))
    return n, x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(folder))}


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
    fig = os.path.join(root, "figures.json") if root != TASK else os.path.join(HERE, "figures.json")
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    GO.main(os.path.join(root, "target"), os.path.join(root, "golden"), fig)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(root, "golden", W.GOLDEN["workbook"]), W.PEOPLE["analyst"], W.PEOPLE["analyst"],
                       "2026-07-29T14:05:00Z", "2026-08-03T16:37:42Z", excel=True, company=W.PLAN)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                          len(os.listdir(os.path.join(root, "golden")))))
    return x


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    x = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x)
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    if not ok:
        raise SystemExit("checks failed")
    if fast:
        return
    scratch = tempfile.mkdtemp(prefix=".rebuild_", dir=TASK)
    try:
        everything(scratch, quiet=True)
        for sub in ("target", "golden"):
            assert digest(os.path.join(TASK, sub)) == digest(os.path.join(scratch, sub)), sub
        for fn in ("metadata.json", "submission.md"):
            assert open(os.path.join(TASK, fn), "rb").read() == open(os.path.join(scratch, fn), "rb").read(), fn
        assert open(os.path.join(HERE, "figures.json"), "rb").read() == open(os.path.join(scratch, "figures.json"),
                                                                          "rb").read()
    finally:
        shutil.rmtree(scratch)
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, submission.md, figures.json" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        same = all(z.read(fn) == open(os.path.join(TASK, "target", fn), "rb").read()
                   for fn in os.listdir(os.path.join(TASK, "target")))
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]) if same
          else "target.zip MISMATCH")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    main(fast=a.fast)
