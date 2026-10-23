"""Build task486: the pack into <task>/target, the golden workbook into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task486/generator/build.py              everything
    python3 task486/generator/build.py --out DIR    the pack only, into DIR
    python3 task486/generator/build.py --fast       one build with the checks, no second build or zip
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
import sim as S          # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = dt.timezone(dt.timedelta(hours=-7))

PDF_STAMPS = {"note": (b"D:20260603101422-07'00'", b"D:20261009154807-07'00'")}
OOXML = {   # creator, last modified by, created, modified, company, excel
    "dvc": ("hvcs.data", "hvcs.data", "2026-10-06T16:02:00Z", "2026-10-06T16:02:00Z", W.COALITION, True),
    "register": (W.PEOPLE["partnership_data"], W.PEOPLE["partnership_data"], "2024-02-12T17:20:00Z",
                 "2026-10-02T21:41:16Z", W.PARTNERSHIP, True),
    "hic": ("HMIS Team", W.PEOPLE["partnership_data"], "2026-01-29T18:05:00Z", "2026-04-28T22:13:40Z", W.PARTNERSHIP,
            True),
    "policy": (W.PEOPLE["partnership_ed"], W.PEOPLE["partnership_ed"], "2026-08-11T15:30:00Z", "2026-09-16T23:02:51Z",
               W.PARTNERSHIP, False),
}
RECEIVED = {"client": "2026-10-07", "enrollment": "2026-10-07", "exit": "2026-10-07", "services": "2026-10-07",
            "dvc": "2026-10-06", "vsm": "2026-10-06", "hot": "2026-10-05", "pairs": "2026-10-09", "note": "2026-10-09",
            "policy": "2026-09-16", "guide": "2026-10-14", "register": "2026-10-02", "pit": "2026-04-28",
            "hic": "2026-04-28", "inventory": "2026-10-14"}


def run_summary(world):
    received = {s: sum(1 for r in world.records if r["src"] == s) for s in W.SOURCES}
    no_year = {s: sum(1 for r in world.records if r["src"] == s and r["by"] is None) for s in W.SOURCES}
    returned = sum(1 for i, j, sc, c in world.pairs if sc >= 4.0)
    links = sum(1 for i, j, sc, c in world.pairs if sc >= W.THRESHOLD)
    return {"received": received, "no_year": no_year, "returned": returned, "links": links}


def build(out, world=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    w = world or S.World()
    keys = P.Keys(w)
    n = {}
    n["client"] = P.write_csv(f("client"), P.CLIENT_COLS, P.client_rows(w, keys))
    enr, exits, servs = P.enrollment_rows(w, keys)
    n["enrollment"] = P.write_csv(f("enrollment"), P.ENR_COLS, enr)
    n["exit"] = P.write_csv(f("exit"), P.EXIT_COLS, exits)
    n["services"] = P.write_csv(f("services"), P.SERV_COLS, servs)
    n["dvc"] = P.dvc_workbook(f("dvc"), w, keys)
    n["vsm"] = P.write_csv(f("vsm"), P.VSM_COLS, P.vsm_rows(w, keys))
    lines = P.hot_lines(w, keys)
    with open(f("hot"), "w", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(json.dumps(line) + "\n")
    n["hot"] = len(lines)
    n["pairs"] = P.write_csv(f("pairs"), P.PAIR_COLS, P.pair_rows(w, keys))
    DC.write_method_note(f("note"), run_summary(w))
    DC.write_policy(f("policy"))
    DC.write_guide(f("guide"))
    n["register"] = DC.write_register(f("register"), w, P.SITE_NAME, P.SITE_COC)
    n["pit"] = P.write_csv(f("pit"), DC.PIT_COLS, DC.pit_rows(w))
    n["hic"] = DC.write_hic(f("hic"), w)
    n["inventory"] = DC.write_inventory(f("inventory"), P.FILES, n)
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co, xl) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=xl, company=co)
    for i, k in enumerate(P.FILES):
        y, m, d = (int(v) for v in RECEIVED[k].split("-"))
        ts = dt.datetime(y, m, d, 8 + (i * 5) % 9, (i * 13) % 60, tzinfo=LOCAL).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(P.FILES), P.FILES[big], n[big]))
    return n, w


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


def everything(root, world=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n, w = build(os.path.join(root, "target"), world=world, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    MD.write(os.path.join(root, "metadata.json"), n)
    WU.write(fig, os.path.join(root, "submission.md"))
    if not quiet:
        print("built %s: %d pack files, %d golden files" % (root, len(os.listdir(os.path.join(root, "target"))),
                                                           len(os.listdir(gdir))))
    return n, w


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    n, w = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=w,
                  meta_path=os.path.join(TASK, "metadata.json"), fig_path=os.path.join(HERE, "figures.json"))
    good &= V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden")) == 0
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
        mt = {k: os.path.getmtime(os.path.join(TASK, "target", k)) == os.path.getmtime(os.path.join(tmp, "target", k))
              for k in os.listdir(os.path.join(TASK, "target"))}
        if not (same_t and same_g and all(same.values()) and all(mt.values())):
            bad = [k for k, v in digest(os.path.join(TASK, "target")).items()
                   if digest(os.path.join(tmp, "target")).get(k) != v]
            badg = [k for k, v in digest(os.path.join(TASK, "golden")).items()
                    if digest(os.path.join(tmp, "golden")).get(k) != v]
            raise SystemExit("second build differs: target %s %s, golden %s %s, %s, mtimes %s" % (
                same_t, bad, same_g, badg, same, [k for k, v in mt.items() if not v]))
    finally:
        shutil.rmtree(tmp)
    print("two builds byte-identical: %d target files, %d golden files, metadata.json, submission.md, figures.json, "
          "file times" % (len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden")))))
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
