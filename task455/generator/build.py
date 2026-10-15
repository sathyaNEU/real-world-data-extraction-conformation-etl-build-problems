"""Build task455: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task455/generator/build.py              everything
    python3 task455/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import deaths as DE        # noqa: E402
import ems as EM           # noqa: E402
import pack as P           # noqa: E402
import review as RV        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = dt.timezone(dt.timedelta(hours=-7))
STAMP = dt.datetime(2027, 5, 11, 16, 42, tzinfo=LOCAL)       # the folder as the department assembled it


def world():
    recs, final = DE.records()
    DE.number(recs)
    encs, reps, ems_rows = EM.build()
    return {"recs": recs, "final": final, "encs": encs, "reps": reps, "ems_rows": ems_rows}


def build(out, quiet=False, docs=True):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    w = world()
    n = {}
    rows, receipts = DE.death_rows(w["recs"])
    n["deaths"] = P.write_deaths(rows, f("deaths"))
    n["receipts"] = P.write_receipts(receipts, f("receipts"))
    n["status"] = P.write_status(f("status"))
    w["review_rows"] = RV.rows(w["final"])
    n["review"] = P.write_review(w["review_rows"], f("review"))
    n["ems"] = P.write_ems(w["ems_rows"], f("ems"))
    n["pop"] = P.write_population(f("pop"))
    n["naloxone"] = P.write_naloxone(f("naloxone"))
    if docs:
        import docs as DC
        import postprocess as PP
        DC.write_agreement(f("agreement"))
        n["dict"] = P.write_dictionary(f("dict"))
        P.write_manifest(f("manifest"), n)
        PP.normalize_ooxml(f("review"), W.OME, W.PEOPLE["pathologist"], "2027-01-28T15:12:00Z", "2027-02-12T21:47:33Z",
                           excel=True, company=W.OME)
        PP.normalize_ooxml(f("dict"), W.PEOPLE["manager"], W.PEOPLE["manager"], "2025-03-04T16:20:00Z",
                           "2027-05-11T22:31:08Z", excel=True, company=W.ORG)
        PP.normalize_pdf(f("agreement"), b"D:20240119153012-07'00'", b"D:20240122101547-07'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %s" % kv for kv in n.items())))
    w["counts"] = n
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 5, 11, 16, 42, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False):
    import golden as G
    import metadata as MD
    import postprocess as PP
    w = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    os.makedirs(os.path.join(root, "generator"), exist_ok=True)
    w["golden"] = G.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                         os.path.join(root, "generator", "figures.json"))
    PP.normalize_ooxml(os.path.join(root, "golden", G.WORKBOOK), W.PEOPLE["manager"], W.PEOPLE["manager"],
                       "2027-05-12T15:05:00Z", "2027-06-01T23:18:27Z", excel=True, company=W.ORG)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    if root == TASK:
        import writeup as WU
        WU.main()
    stamp = dt.datetime(2027, 6, 2, 9, 30, tzinfo=LOCAL).timestamp()
    for name in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", name), (stamp, stamp))
    return w


def main():
    import checks as CK
    import verify as V
    w = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=w,
                meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode() +
                          open(os.path.join(TASK, "metadata.json"), "rb").read() +
                          open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))), allh[:16]))
    import zipfile
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))
    if not ok:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--nodocs", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out, docs=not a.nodocs)
    else:
        main()
