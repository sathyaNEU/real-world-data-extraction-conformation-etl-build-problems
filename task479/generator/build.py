"""Build task479: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json,
submission.md and generator/figures.json; then the checks and the independent verifier, a second full build into a
scratch folder inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task479/generator/build.py              everything
    python3 task479/generator/build.py --out DIR    the pack only, into DIR
    python3 task479/generator/build.py --fast       one build with the checks, no second build or zip
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
EST = dt.timezone(dt.timedelta(hours=-5))
EDT = dt.timezone(dt.timedelta(hours=-4))
# each file's export or save time, plant local time
AS_OF = {"bw": "2026-07-01 07:42", "orb": "2027-01-05 07:55", "opc": "2026-06-18 10:21", "basis": "2025-03-18 16:05",
         "reg": "2026-08-28 14:33", "dahs": "2027-01-05 08:12", "permit": "2025-03-24 11:02",
         "test": "2025-06-09 15:31", "wms": "2027-01-08 16:47", "ap": "2027-01-29 17:12", "mm": "2027-01-04 09:16",
         "wo": "2027-01-05 10:06", "form": "2023-01-10 09:04", "boiler": "2027-01-06 13:21",
         "gen": "2027-01-06 13:36", "ldar": "2026-11-30 15:02"}


def _zone(d):
    return EDT if dt.datetime(2025, 3, 9, 2) <= d < dt.datetime(2025, 11, 2, 2) or \
        dt.datetime(2026, 3, 8, 2) <= d < dt.datetime(2026, 11, 1, 2) else EST


def _iso_utc(s):
    d = dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
    return d.replace(tzinfo=_zone(d)).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _pdf_date(s):
    d = dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
    off = "-04'00'" if _zone(d) is EDT else "-05'00'"
    return ("D:" + d.strftime("%Y%m%d%H%M%S") + off).encode()


def build(out, w=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    w = w or W.simulate()
    ids = P.batch_ids(w)
    P.purchasing(w)
    n = {}
    n["bw"] = P.write_csv(f("bw"), P.BW_COLS, P.bw_rows(w, ids))
    n["orb"] = P.write_parquet(f("orb"), P.orb_table(w, ids))
    n["opc"] = P.write_csv(f("opc"), ["Op Code", "Description"], P.opcode_rows(), newline="\n")
    n["dahs"] = P.write_csv(f("dahs"), P.DAHS_COLS, P.dahs_rows(w), pre=P.DAHS_PRE)
    n["wms"] = P.write_csv(f("wms"), P.WMS_COLS, P.wms_rows(w))
    n["mm"] = P.write_csv(f("mm"), P.MM_COLS, P.mm_rows())
    n["wo"] = P.write_csv(f("wo"), P.WO_COLS, P.wo_rows(w))
    n["boiler"] = P.write_csv(f("boiler"), ["Month", "Emission Unit", "Equipment", "Natural Gas (therms)",
                                            "Operating Hours", "Heating Degree Days"], P.boiler_rows())
    n["gen"] = P.write_csv(f("gen"), ["Date", "Emission Unit", "Equipment", "Reason", "Run Hours", "Hour Meter"],
                           P.gen_rows())
    n["ldar"] = P.write_csv(f("ldar"), ["Monitoring Date", "Component Tag", "Component Type", "Process Area",
                                        "Reading (ppm)", "Instrument"], P.ldar_rows())
    ap = P.ap_lines(w)
    n["ap"] = len(ap)
    DC.write_ap(f("ap"), ap)
    PP.normalize_ooxml(f("ap"), "AP Reporting", "AP Reporting", _iso_utc("2027-01-29 17:11"),
                       _iso_utc(AS_OF["ap"]), excel=True, company=P.COMPANY)
    DC.write_basis(f("basis"))
    PP.normalize_ooxml(f("basis"), "Dylan Gonzalez", "Alyssa Alexander", _iso_utc("2025-02-11 10:40"),
                       _iso_utc(AS_OF["basis"]), excel=True, company=P.COMPANY)
    DC.write_register(f("reg"))
    PP.normalize_ooxml(f("reg"), "Dylan Gonzalez", "Dylan Gonzalez", _iso_utc("2024-05-02 08:55"),
                       _iso_utc(AS_OF["reg"]), excel=True, company=P.COMPANY)
    DC.write_form(f("form"))
    PP.normalize_ooxml(f("form"), "CCAQD Permits", "CCAQD Permits", _iso_utc("2023-01-09 15:12"),
                       _iso_utc(AS_OF["form"]), excel=True, company="Chalmont County Air Quality District")
    DC.write_permit(f("permit"))
    PP.normalize_pdf(f("permit"), _pdf_date("2025-03-24 10:47"), _pdf_date(AS_OF["permit"]))
    DC.write_test(f("test"))
    PP.normalize_pdf(f("test"), _pdf_date("2025-06-09 14:58"), _pdf_date(AS_OF["test"]))
    for k in P.FILES:
        d = dt.datetime.strptime(AS_OF[k], "%Y-%m-%d %H:%M")
        t = d.replace(tzinfo=_zone(d)).timestamp()
        os.utime(f(k), (t, t))
    if not quiet:
        print("pack: %d files, DAHS %d rows, Orbitas %d rows, Batchwise %d rows" % (len(P.FILES), n["dahs"], n["orb"],
                                                                                      n["bw"]))
    return n, w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            d = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), dt.timezone.utc)
            d = d.astimezone(EST).replace(tzinfo=None)
            d = d + dt.timedelta(hours=1) if _zone(d) is EDT else d
            zi = zipfile.ZipInfo(name, date_time=(d.year, d.month, d.day, d.hour, d.minute, d.second))
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
    GO.main(w, gdir, fig)
    MD.write(os.path.join(root, "metadata.json"), n)
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
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), w,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    ok_v = V.main(os.path.join(TASK, "target"), os.path.join(HERE, "figures.json"))
    if fast:
        if not (good and ok_v):
            raise SystemExit("checks or verify failed")
        return
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        import subprocess
        env = dict(os.environ, PYTHONHASHSEED="20261103")
        subprocess.run([sys.executable, os.path.abspath(__file__), "--into", tmp], check=True, env=env)
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
    print("two builds byte-identical (the second in its own process, another hash seed): %d target files, %d golden files, metadata.json, submission.md, figures.json" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not (good and ok_v):
        raise SystemExit("checks or verify failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--into", help="a second full build into this folder, in its own process")
    args = ap.parse_args()
    if args.into:
        everything(args.into, quiet=True)
    elif args.out:
        build(args.out)
        print("pack written to", args.out)
    else:
        main(fast=args.fast)
