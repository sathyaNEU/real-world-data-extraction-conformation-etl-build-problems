"""Build task481: the pack into <task>/target, the golden files into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task481/generator/build.py              everything
    python3 task481/generator/build.py --out DIR    the pack only, into DIR
    python3 task481/generator/build.py --fast       one build with the checks, no second build or zip
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
LOCAL = dt.timezone(dt.timedelta(hours=-5))

PDF_STAMPS = {
    "dictionary": (b"D:20261005084410-05'00'", b"D:20261005091236-05'00'"),
    "cert": (b"D:20250122101503-06'00'", b"D:20250122101503-06'00'"),
    "state_table": (b"D:20260914131022-05'00'", b"D:20260915090418-05'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company, excel
    "ra_2021": ("Records Division", "Records Division", "2021-02-03T15:12:00Z", "2022-01-21T19:44:31Z", W.DEPT, True),
    "ra_2022": ("Records Division", "Records Division", "2022-02-02T14:55:00Z", "2023-01-19T21:03:12Z", W.DEPT, True),
    "ra_2023": ("Records Division", "Records Division", "2023-02-06T16:20:00Z", "2024-01-23T15:41:08Z", W.DEPT, True),
    "ra_2024": ("Records Division", "Records Division", "2024-02-05T15:02:00Z", "2025-01-28T20:17:55Z", W.DEPT, True),
    "method": (W.PEOPLE["lab"], W.PEOPLE["lab"], "2026-08-27T14:30:00Z", "2026-09-29T21:08:42Z",
               "University of Ellsmere", False),
}
AS_OF = {
    "extract": "2026-10-05", "dictionary": "2026-10-05", "ra_2021": "2022-01-21", "ra_2022": "2023-01-19",
    "ra_2023": "2024-01-23", "ra_2024": "2025-01-28", "dvu": "2026-10-02", "dvu_notes": "2026-10-02",
    "method": "2026-09-29", "cert": "2025-01-22", "state_table": "2026-09-15", "state_repo": "2026-09-18",
    "gvr": "2026-10-01", "me": "2026-10-06", "population": "2026-06-26", "cad": "2026-01-12",
}


def everything_data(seed=W.SEED):
    import asks as A
    import bundle as B
    b = B.Bundle(seed)
    return {"b": b, "sh": A.Shootings(b), "sf": A.StateFreeze(b), "seed": seed}


def cert_rows(x):
    import methods as M
    b = x["b"]
    ra = b.return_a()
    rows = x["extract"]
    tot, to13a = M.dual_tables(rows)
    n13 = M.nibrs_13a(rows)
    agg = sum(ra[ym][l][2] for ym in M.DUAL for l in M.AGG)
    e4 = sum(ra[ym]["4E"][2] for ym in M.DUAL)
    rob = sum(ra[ym][l][2] for ym in M.DUAL for l in M.ROB)
    cnt = lambda codes: sum(1 for r in rows if M.local_month(r[M.E["report_datetime_utc"]]) in M.DUAL
                            and r[M.E["offense_code"]] in codes)
    rob_n = len({r[M.E["incident_number"]] for r in rows if M.local_month(r[M.E["report_datetime_utc"]]) in M.DUAL
                 and r[M.E["offense_code"]] == "120"})
    return [("Aggravated assault", "{:,}".format(agg), "{:,}".format(sum(n13[ym] for ym in M.DUAL))),
            ("Other assaults / simple assault and intimidation", "{:,}".format(e4), "{:,}".format(cnt(("13B", "13C")))),
            ("Robbery (incidents)", "{:,}".format(rob), "{:,}".format(rob_n))]


def state_table_rows(x):
    import numpy as np
    b = x["b"]
    ra = b.return_a()
    pub24 = sum(ra[(2024, m)][l][2] for m in range(1, 13) for l in ("4A", "4B", "4C", "4D"))
    r = np.random.default_rng(x["seed"] * 43 + 5)
    others = [("Ashcombe Police Department", "NIBRS"), ("Brayley Police Department", "NIBRS"),
              ("Carrow City Police Department", "NIBRS"), ("Dunmore Police Department", "SRS to 2024, NIBRS from 2025"),
              ("Fenwick Police Department", "NIBRS"), ("Galloway Police Department", "NIBRS"),
              ("Halsted Police Department", "NIBRS from July 2024"), ("Ivers Police Department", "NIBRS"),
              ("Kettering Falls Police Department", "NIBRS"), ("Linden Police Department", "NIBRS")]
    rows = []
    for name, rep in others:
        a = int(r.integers(380, 2600))
        rows.append((name, "{:,}".format(a), "{:,}".format(int(a * r.uniform(0.9, 1.12))), rep))
    rows.append(("Ellsmere Police Department", "{:,}".format(pub24), "{:,}".format(x["sf"].published),
                 "SRS to 2024, NIBRS from 2025"))
    rows.sort(key=lambda t: t[0])
    return rows


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or everything_data()
    b = x["b"]
    n = {}
    rows = P.extract_rows(b)
    x["extract"] = rows
    n["extract"] = P.write_csv(f("extract"), P.EXTRACT_COLS, rows)
    dvu = P.dvu_rows(b)
    x["dvu"] = dvu
    n["dvu"] = P.write_csv(f("dvu"), P.DVU_COLS, dvu)
    n["state_repo"] = P.write_csv(f("state_repo"), P.STATE_COLS, P.state_rows(x["sf"]))
    n["gvr"] = P.write_csv(f("gvr"), P.GVR_COLS, P.gvr_rows(x["sh"], x["seed"]))
    n["me"] = P.write_csv(f("me"), P.ME_COLS, P.me_rows(x["sh"]))
    n["population"] = P.write_csv(f("population"), P.POP_COLS, P.population_rows())
    n["cad"] = P.write_csv(f("cad"), P.CAD_COLS, P.cad_rows(b))
    ra = b.return_a()
    x["ra"] = ra
    for y in (2021, 2022, 2023, 2024):
        DC.write_return_a(f("ra_%d" % y), y, ra, old_layout=(y == 2021))
    DC.write_dictionary(f("dictionary"), n["extract"])
    DC.write_dvu_notes(f("dvu_notes"))
    DC.write_methods(f("method"))
    DC.write_cert(f("cert"), cert_rows(x))
    DC.write_state_table(f("state_table"), state_table_rows(x))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co, xl) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=xl, company=co)
    for i, k in enumerate(P.FILES):
        y, m, d = (int(v) for v in AS_OF[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=LOCAL).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), LOCAL)
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
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"), sorted(os.listdir(gdir)), n)
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
    good &= bool(V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden")))
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
