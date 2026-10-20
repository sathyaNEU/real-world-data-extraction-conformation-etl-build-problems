"""Build task471 (architecture 5): the pack into <task>/target, the golden files into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task471/generator/build.py              everything
    python3 task471/generator/build.py --out DIR    the pack only, into DIR
    python3 task471/generator/build.py --fast       one build with the checks, no second build or zip
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
LOCAL = dt.timezone(dt.timedelta(hours=12))

PDF_STAMPS = {
    "pes_report": (b"D:20250926143012+12'00'", b"D:20250926151840+12'00'"),
    "series_notes": (b"D:20250414101530+12'00'", b"D:20250414101530+12'00'"),
    "migration": (b"D:20250909092245+12'00'", b"D:20250909114402+12'00'"),
    "field_ops": (b"D:20250721160530+12'00'", b"D:20250722083911+12'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company, excel
    "plan": (W.PEOPLE["commission"], W.PEOPLE["commission"], "2026-09-08T21:14:00Z", "2026-09-21T23:02:51Z",
             W.COMMISSION, False),
    "spec": (W.PEOPLE["estimates"], W.PEOPLE["estimates"], "2026-09-23T22:40:00Z", "2026-09-29T20:17:09Z", W.OFFICE, True),
    "dictionary": ("Data Services", "Data Services", "2025-09-08T23:05:00Z", "2026-09-30T21:31:47Z", W.COMMISSION, True),
    "census": ("Census Outputs", "Census Outputs", "2025-11-12T21:00:00Z", "2025-11-17T19:44:12Z", W.OFFICE, True),
    "deaths_hist": ("Vital Statistics", "Vital Statistics", "2019-05-02T22:10:00Z", "2025-04-13T21:58:30Z", W.OFFICE, True),
}
AS_OF = {   # each file's date as its source dated it
    "census": "2025-11-18", "pes_people": "2025-09-26", "pes_records": "2025-09-26", "pes_meshblocks": "2025-09-26",
    "pes_report": "2025-09-26", "roll": "2026-09-17", "electorates": "2024-11-30", "births": "2025-04-14",
    "deaths_hist": "2025-04-14", "deaths": "2025-04-14", "movements": "2025-04-14", "series_notes": "2025-04-14",
    "plan": "2026-09-22", "spec": "2026-09-30", "log": "2026-10-01", "dictionary": "2026-10-01",
    "migration": "2025-09-09", "estimates_2024": "2024-10-30", "field_ops": "2025-07-22", "roll_2023": "2023-11-09",
}


def field_rows(x):
    import numpy as np
    r = np.random.default_rng(x["seed"] * 1000 + 15)
    out = []
    for c in W.CODES:
        people = sum(int(x["reg"]["pop"][c][s].sum()) for s in ("M", "F"))
        dw = int(round(people / r.uniform(2.45, 2.75) / 10.0)) * 10
        online = r.uniform(0.66, 0.79)
        field = r.uniform(0.07, 0.13)
        paper = 1 - online - field
        out.append((W.NAME[c], "{:,}".format(dw), "%.1f%%" % (100 * online), "%.1f%%" % (100 * paper),
                    "%.1f%%" % (100 * field), "%.1f%%" % (100 * x["cov"]["imputed"][c] * 0.92)))
    return out


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    x = x or P.everything()
    n = {}
    n["pes_people"] = P.write_csv(f("pes_people"), P.PEOPLE_COLS, x["ids"]["people"])
    n["pes_records"] = P.write_csv(f("pes_records"), P.RECORD_COLS, x["ids"]["records"])
    n["pes_meshblocks"] = P.write_csv(f("pes_meshblocks"), P.MB_COLS, P.meshblock_rows(x))
    n["roll"] = P.write_csv(f("roll"), P.ROLL_COLS, x["snapshot"])
    n["electorates"] = P.write_csv(f("electorates"), P.ELECTORATE_COLS, P.electorate_rows())
    n["roll_2023"] = P.write_csv(f("roll_2023"), P.GE_COLS, P.ge_rows(x))
    n["births"] = P.write_csv(f("births"), P.BIRTH_COLS, P.birth_rows(x), lineterminator="\n")
    n["deaths"] = P.write_csv(f("deaths"), P.DEATH_COLS, P.death_rows(x), lineterminator="\n")
    n["movements"] = P.write_csv(f("movements"), P.MOVE_COLS, P.movement_rows(x), lineterminator="\n")
    n["log"] = P.write_csv(f("log"), P.LOG_COLS, P.log_rows(x))
    n["estimates_2024"] = P.write_csv(f("estimates_2024"), P.EST_COLS, P.estimate_rows(x))
    DC.write_census_workbook(f("census"), P.census_table(x))
    DC.write_deaths_history(f("deaths_hist"), P.death_wide(x))
    DC.write_pes_report(f("pes_report"), sum(len(v) for v in x["cnt"]["sampled_mb"].values()), n["pes_people"],
                        n["pes_records"])
    DC.write_series_notes(f("series_notes"))
    DC.write_plan(f("plan"))
    DC.write_spec(f("spec"))
    DC.write_dictionary(f("dictionary"))
    DC.write_migration(f("migration"))
    DC.write_field_ops(f("field_ops"), field_rows(x))
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
