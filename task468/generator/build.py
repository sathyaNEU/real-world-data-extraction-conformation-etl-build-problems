"""Build task468: the pack into <task>/target, the goldens into <task>/golden, metadata.json, submission.md and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder inside
the task compared byte for byte, and target.zip cut from the final build.

    python3 task468/generator/build.py              everything
    python3 task468/generator/build.py --out DIR    the pack only, into DIR
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

import gtfs as G         # noqa: E402
import pack as P         # noqa: E402
import sim as S          # noqa: E402
import world as W        # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL = dt.timezone(dt.timedelta(hours=-5))

PDF_STAMPS = {
    "guidance": b"D:20260715103012-05'00'",
    "change_note": b"D:20260708144205-05'00'",
    "review_memo": b"D:20260731161833-05'00'",
    "equity": b"D:20260311092741-05'00'",
}


def build(out, x=None, quiet=False):
    import docs as DC
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = x or S.everything()
    n = {}
    n["avl_q1"] = P.write_csv(f("avl_q1"), P.ARBOR_COLS, P.arbor_rows(x))
    if "qrows" not in x:
        x["qrows"] = P.quinnell_rows(x)
    n["avl_q2"] = P.write_csv(f("avl_q2"), P.QUINNELL_COLS, x["qrows"])
    n["review"] = P.write_csv(f("review"), P.REVIEW_COLS, P.review_rows(x))
    n["fleet"] = P.write_csv(f("fleet"), P.FLEET_COLS, P.fleet_rows())
    n["candidates"] = P.write_csv(f("candidates"), P.CANDIDATE_COLS, P.candidate_rows())
    n["amenities"] = P.write_csv(f("amenities"), P.AMENITY_COLS, P.amenity_rows())
    G.write_feed(f("gtfs_jan"), "2601")
    G.write_feed(f("gtfs_apr"), "2604")
    rv = x["review"]
    findings = []
    for m in range(1, 7):
        g = rv[[d.month == m for d in rv["day"]]]
        late = (g["sec"] - g["sched_min"] * 60) / 60.0
        rev = g["revenue"].to_numpy()
        fault = g["fault"].to_numpy()
        assert not (rev & ~fault & (late.to_numpy() <= 0)).any(), "a reviewed bus ran early beyond the window"
        findings.append((int((rev & ~fault).sum()), int((rev & fault).sum()), int((~rev).sum())))
    DC.write_review_memo(f("review_memo"), P.review_frame(x), findings)
    DC.write_guidance(f("guidance"))
    DC.write_change_note(f("change_note"))
    DC.write_equity(f("equity"))
    DC.write_ridership(f("ridership"), P.ridership_table())
    DC.write_farebox(f("farebox"), P.farebox_table())
    DC.write_shelter_wo(f("shelter_wo"))
    for k, stamp in PDF_STAMPS.items():
        PP.normalize_pdf(f(k), stamp, stamp)
    PP.normalize_ooxml(f("ridership"), "Service Planning", "Service Planning", "2026-07-20T15:02:00Z",
                       "2026-07-22T21:14:37Z", excel=True, company=W.DEPARTMENT)
    PP.normalize_ooxml(f("farebox"), "Finance", "Finance", "2026-07-15T13:41:00Z", "2026-07-16T18:22:51Z",
                       excel=True, company=W.DEPARTMENT)
    PP.normalize_ooxml(f("shelter_wo"), "Capital Projects", "Capital Projects", "2025-08-04T14:10:00Z",
                       "2026-07-10T16:48:12Z", excel=True, company=W.DEPARTMENT)
    asof = {k: d for k, src, d, desc in __import__("docs").INDEX}
    for i, k in enumerate(W.FILES):
        y, m, d = (int(v) for v in asof[k].split("-"))
        ts = dt.datetime(y, m, d, 9 + (i * 7) % 8, (i * 13) % 60, tzinfo=CENTRAL).timestamp()
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
            t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder, name)), CENTRAL)
            zi = zipfile.ZipInfo(name, date_time=(t.year, t.month, t.day, t.hour, t.minute, t.second))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, x=None, quiet=False):
    import golden as GO
    import metadata as MD
    import postprocess as PP
    import writeup as WU
    n, x = build(os.path.join(root, "target"), x=x, quiet=quiet)
    gdir = os.path.join(root, "golden")
    if os.path.exists(gdir):
        shutil.rmtree(gdir)
    fig = os.path.join(root, "generator", "figures.json")
    GO.main(os.path.join(root, "target"), gdir, fig)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["planning"], W.PEOPLE["planning"],
                       "2026-10-26T14:10:00Z", "2026-10-30T19:02:00Z", title="FTC nominations FY2027", excel=True,
                       company=W.DEPARTMENT)
    ts = dt.datetime(2026, 10, 30, 14, 2, tzinfo=CENTRAL).timestamp()
    for fn in os.listdir(gdir):
        os.utime(os.path.join(gdir, fn), (ts, ts))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
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
