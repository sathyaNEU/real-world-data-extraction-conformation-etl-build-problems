"""Build task488: the pack into <task>/target, the goldens into <task>/golden, metadata.json, generator/figures.json and
submission.md; then the checks, the independent solver, a second full build in a scratch folder compared byte for
byte, and target.zip cut last.

    python3 task488/generator/build.py              everything
    python3 task488/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import hashlib
import os
import shutil
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import names as N   # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = (2026, 10, 14, 7, 30, 0)          # the folder as the Operator's duty supervisor pulled it for the committee
SCADA_COLS = ["timestamp_utc", "pump_station_flow_lpm", "meter_totaliser_m3", "header_pressure_kpa", "pumps_running",
              "tk1_hyd_valve", "tk2_hyd_valve", "tk3_hyd_valve", "tk4_hyd_valve"]
OOXML = {   # file key: (creator, last saved by, created, modified, company)
    "register": (N.OPERATOR, N.OPERATOR, "2019-03-04T16:20:00Z", "2026-06-30T21:05:00Z", N.OPERATOR),
    "maint": (N.OPERATOR, N.OPERATOR, "2026-10-05T13:02:00Z", "2026-10-13T18:41:00Z", N.OPERATOR),
    "ng_tickets": (N.NORTHGARTH, N.NORTHGARTH, "2026-10-14T14:21:00Z", "2026-10-14T14:21:00Z", N.NORTHGARTH),
    "ng_checks": (N.NORTHGARTH, N.NORTHGARTH, "2026-10-14T14:23:00Z", "2026-10-14T14:23:00Z", N.NORTHGARTH),
    "equipment": (N.CORP, N.CORP, "2024-02-12T17:45:00Z", "2026-10-05T15:10:00Z", N.CORP),
    "pits_q3": (N.OPERATOR, N.OPERATOR, "2026-07-06T15:30:00Z", "2026-10-02T19:12:00Z", N.OPERATOR),
}
PDFS = {   # file key: (created, modified) as PDF dates
    "shiftlog": (b"D:20261014072600-07'00'", b"D:20261014072600-07'00'"),
    "recall": (b"D:20261014050500-07'00'", b"D:20261014050500-07'00'"),
    "qm09": (b"D:20260301090000-08'00'", b"D:20260301090000-08'00'"),
    "stock": (b"D:20261005103000-07'00'", b"D:20261005103000-07'00'"),
}


def build(out):
    import docs as DC
    import pack as P
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    W = P.the_world()
    f = lambda k: os.path.join(out, N.FILES[k])
    n = {}
    scada = P.scada_rows(W)
    n["scada"] = P.write_csv(f("scada"), SCADA_COLS, scada)
    P.write_register(f("register"))
    DC.write_shift_log(f("shiftlog"), W)
    P.write_maintenance(f("maint"), W)
    n["corbel_tickets"] = P.write_csv(f("corbel_tickets"), P.CORBEL_COLS, P.corbel_rows(W))
    n["ng_tickets"] = P.write_ng_tickets(f("ng_tickets"), W)
    n["corbel_checks"] = P.write_csv(f("corbel_checks"), P.CORBEL_CHECK_COLS, P.corbel_check_rows(W))
    n["ng_checks"] = P.write_ng_checks(f("ng_checks"), W)
    n["certs"] = P.write_csv(f("certs"), P.CERT_COLS, P.cert_rows())
    n["rack"] = P.write_csv(f("rack"), P.RACK_COLS, P.rack_rows(W))
    P.write_equipment(f("equipment"))
    n["ng_vehicles"] = P.write_csv(f("ng_vehicles"), P.NG_VEHICLE_COLS, P.ng_vehicle_rows(W))
    n["corbel_equipment"] = P.write_csv(f("corbel_equipment"), P.CORBEL_EQUIPMENT_COLS, P.corbel_equipment_rows(W))
    DC.write_recall(f("recall"))
    DC.write_qm09(f("qm09"))
    P.write_pit_inspections(f("pits_q3"), W)
    DC.write_stock(f("stock"), P.september_stock(W, scada))
    for k, (who, last, c, m, co) in OOXML.items():
        PP.normalize_ooxml(f(k), who, last, c, m, excel=True, company=co)
    for k, (c, m) in PDFS.items():
        PP.normalize_pdf(f(k), c, m)
    ts = time.mktime(STAMP + (0, 0, -1))
    for k in N.FILES:
        os.utime(f(k), (ts, ts))
    assert sorted(os.listdir(out)) == sorted(N.FILES.values())
    return n, W


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    folder = os.path.join(root, "target")
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    import writeup as WU
    n, W = build(os.path.join(root, "target"))
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
    return W, n


def main():
    import tempfile
    import checks as CK
    W, n = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), W=W, n=n,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
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
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()))
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
