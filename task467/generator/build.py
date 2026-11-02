"""Build task467 (architecture 2): the pack into <task>/target, the goldens into <task>/golden, metadata.json,
submission.md and generator/figures.json; then the checks and the independent verifier, a second full build into a
scratch folder inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task467/generator/build.py              everything
    python3 task467/generator/build.py --out DIR    the pack only, into DIR
    python3 task467/generator/build.py --fast       one build with the checks, no second build or zip
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
UK = dt.timezone(dt.timedelta(hours=0))

PDF_STAMPS = {
    "assurance": (b"D:20261009111408+01'00'", b"D:20261009152231+01'00'"),
    "review": (b"D:20260211093522+00'00'", b"D:20260211160944+00'00'"),
}


def review_monthly(x):
    p = x["parcels"]
    out = {(2025, m): [0, 0, 0] for m in range(1, 13)}
    for s in p["deliv"]:
        d = S.day_of(s)
        if d.year == 2025:
            out[(2025, d.month)][0] += 1
    for t, i in x["opened"]:
        d = S.day_of(t)
        if d.year == 2025:
            out[(2025, d.month)][1] += 1
    for i in range(len(p["deliv"])):
        d = p["made_day"][i]
        if d is not None and d.year == 2025 and p["outcome"][i] == "REFUND":
            out[(2025, d.month)][2] += 1
    return {k: tuple(v) for k, v in out.items()}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or S.everything()
    n = {}
    n["goods2025"], n["goods2026"] = P.write_goods(x, f("goods2025"), f("goods2026"))
    n["processing"] = P.write_processing(x, f("processing"))
    n["refunds"] = P.write_refunds(x, f("refunds"))
    n["orders"] = P.write_orders(x, f("orders"))
    n["vouchers"] = P.write_vouchers(x, f("vouchers"))
    n["redemptions"] = P.write_redemptions(x, f("redemptions"))
    n["cases"] = P.write_cases(x, f("cases"))
    n["rota"] = P.write_csv(f("rota"), ["shift_date", "shift", "employees_rostered", "agency_rostered"], P.rota_rows(x))
    DC.write_assurance(f("assurance"))
    DC.write_review(f("review"), review_monthly(x))
    DC.write_dailyops(f("dailyops"), P.daily_ops(x))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    PP.normalize_ooxml(f("dailyops"), "Cotterby Supervisors", W.PEOPLE["centre"], "2024-12-02T07:41:00Z",
                       "2026-10-29T17:58:12Z", excel=True, company=W.RETAILER_LTD)
    asof = {k: d for k, src, d, desc in DC.PROVENANCE}
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in asof[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=UK).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), UK)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    import bundle as BU
    BU._C.clear()
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    import ladder as LD
    GO.main(os.path.join(root, "target"), gdir, fig, extra=LD.ladder(os.path.join(root, "target")))
    import postprocess as PP
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["note"]), b"D:20261112100417+00'00'", b"D:20261112143908+00'00'")
    ts = dt.datetime(2026, 11, 12, 14, 39, tzinfo=UK).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
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
    print("target.zip cut from this build: %d files, each identical to target/ (md5 %s)" % (
        len(inside), hashlib.md5(open(zp, "rb").read()).hexdigest()))
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
