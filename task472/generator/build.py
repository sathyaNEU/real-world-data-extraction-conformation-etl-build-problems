"""Build task472: the pack into <task>/target, the golden deliverables into <task>/golden, metadata.json, submission.md
and generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task472/generator/build.py              everything
    python3 task472/generator/build.py --out DIR    the pack only, into DIR
    python3 task472/generator/build.py --fast       one build with the checks, no second build or zip
"""
import argparse
import datetime as dt
import hashlib
import json
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
EASTERN = dt.timezone(dt.timedelta(hours=-4))
PDF_STAMPS = {"rules": (b"D:20260609141207-04'00'", b"D:20260609141207-04'00'"),
              "directions": (b"D:20250424101533-04'00'", b"D:20250424101533-04'00'")}
OOXML = {   # creator, last modified by, created, modified, company
    "rvt": ("Salt River Terminals", "jwood", "2024-06-03T13:12:00Z", "2026-10-05T11:41:37Z", "Ternmouth Port Authority"),
    "jobs": ("Salt River Terminals", "jwood", "2024-06-03T13:20:00Z", "2026-10-05T11:44:09Z", "Ternmouth Port Authority"),
    "oem": ("Allison Mcbride", "Allison Mcbride", "2025-07-08T14:02:00Z", "2026-10-05T12:20:51Z",
            "Ternmouth Port Authority"),
}
AS_OF = {"tos": "2026-10-05 06:22", "visits": "2026-10-05 06:24", "rvt": "2026-10-05 07:41",
         "pilot": "2026-10-02 10:15", "tides": "2025-05-12 09:00", "vessels": "2026-10-05 06:10",
         "register": "2026-10-05 06:58", "wo": "2026-10-05 06:51", "status": "2026-10-05 06:53",
         "labor": "2026-10-05 06:56", "oem": "2026-10-05 08:20", "jobs": "2026-10-05 07:44",
         "ais": "2026-10-06 08:15", "yard": "2026-10-05 06:55", "windows": "2026-10-01 16:30",
         "rules": "2026-06-09 14:12", "directions": "2025-04-24 10:15", "dictionary": "2026-10-06 09:02",
         "manifest": "2026-10-06 09:05"}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or W.build()
    n = {}
    auth, rvt = P.tos_rows(x)
    n["tos"] = P.write_csv(f("tos"), P.TOS_COLS, P.tos_csv_rows(auth))
    n["visits"] = P.write_csv(f("visits"), P.VISIT_COLS, P.visit_rows(x))
    calls = P.rvt_calls(x)
    qc = [[v, q, P.unaive(h), mv, P.unaive(a), P.unaive(b), "%02d-%02d" % (b0, b1)]
          for h, term, v, q, mv, a, b, b0, b1 in rvt]
    P.write_xlsx(f("rvt"), [("Calls", ["CALL_REF", "BERTH", "VESSEL", "LLOYDS", "CALLSIGN", "OPERATOR", "SERVICE",
                                       "VOY", "ETA_UTC"], calls, [8]),
                            ("QC Hours", ["CALL_REF", "QC", "HOUR_UTC", "LIFTS", "FIRST_LIFT_UTC", "LAST_LIFT_UTC",
                                          "BAYS"], qc, [2, 4, 5])])
    n["rvt"] = len(calls) + len(qc)
    n["pilot"] = P.write_csv(f("pilot"), P.PILOT_COLS, P.pilot_rows(x))
    txt = P.tides_txt(x)
    with open(f("tides"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(txt)
    n["tides"] = sum(1 for line in txt.splitlines() if line[:2] in ("20",))
    vj = P.vessel_json(x)
    with open(f("vessels"), "w", encoding="utf-8") as fh:
        json.dump(vj, fh, indent=1)
        fh.write("\n")
    n["vessels"] = len(vj["vessels"])
    n["register"] = P.write_csv(f("register"), P.REG_COLS, P.register_rows())
    sts, status, yrows = P.order_book(x)
    n["wo"] = P.write_csv(f("wo"), P.WO_COLS, sts)
    n["status"] = P.write_csv(f("status"), P.STATUS_COLS, status)
    n["yard"] = P.write_csv(f("yard"), P.WO_COLS, yrows)
    jobs = P.job_rows(x)
    P.write_xlsx(f("jobs"), [("Jobs", P.JOB_COLS, jobs, [5, 6, 7])])
    n["jobs"] = len(jobs)
    yard = [y for y in P.yard_orders(__import__("numpy").random.default_rng(W.SEED + 405))]
    # the yard orders carry the numbers order_book gave them
    ywon = {(r[1], r[9]): r[0] for r in yrows}
    for y in yard:
        k = (y["asset"], P.lstr(y["start"], False))
        if k in ywon:
            y["wonum"] = ywon[k]
    n["labor"] = P.write_csv(f("labor"), P.LABOR_COLS, P.labor_rows(x, yard))
    oem = P.oem_rows(x)
    P.write_xlsx(f("oem"), [("Timesheets", P.OEM_COLS, oem, [])])
    n["oem"] = len(oem)
    n["ais"] = P.write_csv(f("ais"), P.AIS_COLS, P.ais_rows(x))
    n["windows"] = P.write_csv(f("windows"), P.WINDOW_COLS, P.window_rows())
    DC.write_rules(f("rules"))
    DC.write_directions(f("directions"))
    DC.write_dictionary(f("dictionary"))
    n["manifest"] = P.write_csv(f("manifest"), DC.MANIFEST_COLS, DC.manifest_rows(n))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=True, company=co)
    for k in P.FILES:
        t = dt.datetime.strptime(AS_OF[k], "%Y-%m-%d %H:%M").replace(tzinfo=EASTERN).timestamp()
        os.utime(f(k), (t, t))
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), EASTERN)
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
