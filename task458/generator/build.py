"""Build task458 (architecture 3): the pack into <task>/target, the goldens into <task>/golden, metadata.json,
submission.md and generator/figures.json; then the checks and the independent verifier, a second full build into a
scratch folder inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task458/generator/build.py              everything
    python3 task458/generator/build.py --out DIR    the pack only, into DIR
    python3 task458/generator/build.py --fast       one build with the checks, no second build or zip
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
    "policy": (b"D:20250314101522+00'00'", b"D:20250314154407+00'00'"),
    "facility": (b"D:20240628091104+01'00'", b"D:20240628172219+01'00'"),
    "vhplan": (b"D:20261120083116+00'00'", b"D:20261120114952+00'00'"),
}
XLSX_STAMPS = {
    "ahi_stock": ("NAV Reporting", "AHI Finance", "2027-01-05T08:12:40Z", "2027-01-05T08:12:40Z", "Ashlund Home Ireland Ltd"),
    "ahi_ship26": ("NAV Reporting", "AHI Finance", "2027-01-05T08:19:02Z", "2027-01-05T08:19:02Z", "Ashlund Home Ireland Ltd"),
    "lots": ("Group Finance", "Group Finance", "2021-02-11T10:02:00Z", "2027-01-08T15:41:27Z", "Ashlund Home Group plc"),
    "fx": ("Group Finance", "Group Finance", "2025-01-06T09:14:00Z", "2027-01-04T09:03:51Z", "Ashlund Home Group plc"),
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or S.everything()
    nums = P.ahb_numbers(x)
    sup = P.superseded(x)
    n = {}
    n["ahl_stock"] = P.write_ahl_stock(x, f("ahl_stock"))
    n["ahi_stock"] = P.write_ahi_stock(x, f("ahi_stock"))
    n["ahb_stock"] = P.write_ahb_stock(x, f("ahb_stock"), nums)
    n["ahb_xref"] = P.write_ahb_xref(x, f("ahb_xref"), nums, sup)
    n["master"] = P.write_master(x, f("master"), sup)
    n["ahl_orders"] = P.write_ahl_orders(x, f("ahl_orders"))
    n["ahi_ship26"] = P.write_ahi_ship26(x, f("ahi_ship26"))
    n["ahi_arch25"] = P.write_ahi_arch25(x, f("ahi_arch25"))
    n["ahb_orders"] = P.write_ahb_orders(x, f("ahb_orders"), nums)
    n["vh_weeks"] = P.write_vh_weeks(x, f("vh_weeks"))
    n["lots"] = P.write_lots(x, f("lots"))
    n["fx"] = P.write_fx(x, f("fx"))
    n["rcf"] = P.write_rcf(x, f("rcf"))
    n["open_po"] = P.write_open_po(x, f("open_po"))
    n["pallets"] = P.write_pallets(x, f("pallets"))
    DC.write_policy(f("policy"))
    DC.write_facility(f("facility"))
    DC.write_vhplan(f("vhplan"))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, last, c0, m0, co) in XLSX_STAMPS.items():
        PP.normalize_ooxml(f(k), cr, last, c0, m0, excel=True, company=co)
    asof = {k: d for k, src, d, desc in DC.PROVENANCE}
    for i, k in enumerate(P.FILES):
        y, m, d = (int(v) for v in asof[k].split("-"))
        ts = dt.datetime(y, m, d, 8 + (i * 5) % 9, (i * 13) % 60, tzinfo=UK).timestamp()
        os.utime(f(k), (ts, ts))
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), UK)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import bundle as BU
    import golden as GO
    import metadata as MD
    import postprocess as PP
    import writeup as WU
    BU._C.clear()
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig_path = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig_path)
    PP.normalize_pdf(os.path.join(gdir, GO.GOLDEN["note"]), b"D:20270122101417+00'00'", b"D:20270122163908+00'00'")
    PP.normalize_ooxml(os.path.join(gdir, GO.GOLDEN["workbook"]), "Group Finance", "Group Finance", "2027-01-19T09:02:11Z",
                       "2027-01-22T16:31:45Z", excel=True, company="Ashlund Home Group plc")
    ts = dt.datetime(2027, 1, 22, 16, 39, tzinfo=UK).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), n)
    WU.write(fig_path, os.path.join(root, "submission.md"))
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
    print("target.zip cut from this build: %d files, each identical to target/ (md5 %s)" % (
        len(inside), hashlib.md5(open(zp, "rb").read()).hexdigest()))
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
