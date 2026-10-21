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
    "notes": (b"D:20230612142210-05'00'", b"D:20240214101533-06'00'"),
    "instructions": (b"D:20260813160455-05'00'", b"D:20260814091207-05'00'"),
}
OOXML = {   # creator, last modified by, created, modified, company, excel
    "policy": (W.PEOPLE["aging"], W.PEOPLE["aging"], "2023-08-30T15:20:00Z", "2023-09-21T20:41:16Z", W.OFFICE, False),
    "facilities": ("Licensing and Certification", W.PEOPLE["planning"], "2026-09-02T13:10:00Z", "2026-09-08T19:22:47Z",
                   W.OFFICE, True),
    "providers": (W.PEOPLE["aging"], W.PEOPLE["aging"], "2023-07-05T14:02:00Z", "2026-10-09T15:31:02Z", W.OFFICE, True),
}


def received():
    import docs as DC
    by_name = {r[0]: r[4] for r in DC.INVENTORY}
    out = {}
    for k, name in P.FILES.items():
        out[k] = by_name.get(name, "2026-10-09")
    return out


def build(out, b=None, quiet=False):
    import docs as DC
    import postprocess as PP
    from bundle import Bundle
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    b = b or Bundle()
    n = {}
    p12_cols = ["GEO_ID", "NAME"] + P.P12_CODES
    p12_labs = ["Geography", "Geographic Area Name"] + P.p12_labels()
    n["blocks"] = P.write_csv(f("blocks"), P.BLOCK_COLS, P.blocks_long(b))
    n["bgs"] = P.write_csv(f("bgs"), p12_cols, P.bg_rows(b), extra_header=p12_labs)
    n["tracts"] = P.write_csv(f("tracts"), p12_cols, P.tract_rows(b), extra_header=p12_labs)
    n["hu"] = P.write_csv(f("hu"), ["GEO_ID", "NAME", "H1_001N"], P.hu_rows(b),
                          extra_header=["Geography", "Geographic Area Name", " !!Total"])
    n["colmeta"] = P.write_csv(f("colmeta"), P.COLMETA_COLS, P.colmeta_rows())
    n["assign"] = P.write_csv(f("assign"), P.ASSIGN_COLS, P.assign_rows(b))
    n["points"] = P.write_csv(f("points"), P.POINTS_COLS, P.points_rows(b, W.SEED))
    acols, alabs = P.acs_header()
    n["acs"] = P.write_csv(f("acs"), acols, P.acs_rows(b, W.SEED), extra_header=alabs)
    n["roster"] = P.write_csv(f("roster"), P.ROSTER_COLS, P.roster_rows(b))
    n["episodes"] = P.write_csv(f("episodes"), P.EPISODE_COLS, P.episode_rows(b, W.SEED))
    n["log"] = P.write_csv(f("log"), P.LOG_COLS, P.log_rows(b))
    n["items"] = P.write_csv(f("items"), P.ITEM_COLS, P.item_rows())
    n["deaths"] = P.write_csv(f("deaths"), P.DEATH_COLS, P.death_rows(b, W.SEED))
    n["links"] = P.write_csv(f("links"), P.LINK_COLS, P.link_rows(b, W.SEED))
    DC.write_inventory(f("inventory"))
    n["inventory"] = len(DC.INVENTORY)
    DC.write_guide(f("guide"))
    DC.write_notes(f("notes"))
    DC.write_instructions(f("instructions"))
    DC.write_policy(f("policy"))
    DC.write_facilities(f("facilities"), b, P.geoid_block)
    DC.write_providers(f("providers"))
    for k, (c, m) in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), c, m)
    for k, (cr, lb, c0, m0, co, xl) in OOXML.items():
        PP.normalize_ooxml(f(k), cr, lb, c0, m0, excel=xl, company=co)
    rec = received()
    for i, k in enumerate(P.FILES):
        y, m, d = (int(v) for v in rec[k].split("-"))
        ts = dt.datetime(y, m, d, 8 + (i * 5) % 9, (i * 13) % 60, tzinfo=LOCAL).timestamp()
        os.utime(f(k), (ts, ts))
    if not quiet:
        big = max(n, key=lambda k: n[k])
        print("pack: %d files, largest %s (%d rows)" % (len(P.FILES), P.FILES[big], n[big]))
    return n, b


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


def everything(root, b=None, quiet=False):
    import golden as GO
    import metadata as MD
    import writeup as WU
    n, b = build(os.path.join(root, "target"), b=b, quiet=quiet)
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
    return n, b


def main(fast=False):
    import tempfile
    import zipfile
    import checks as CK
    import verify as V
    n, b = everything(TASK)
    good = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), b=b,
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
