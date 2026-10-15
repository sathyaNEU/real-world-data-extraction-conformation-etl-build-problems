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

import derive as DV         # noqa: E402
import econ as E            # noqa: E402
import pack as P            # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
CENTRAL = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2027, 5, 14, 16, 42, tzinfo=CENTRAL)       # the folder as the bureau assembled it


def world():
    w, S = E.build()
    d = DV.derive(w, S)
    nums = P.account_numbers(w)
    return {"world": w, "S": S, "d": d, "nums": nums}


def build(out, quiet=False, docs=True):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    x = world()
    w, S, d, nums = x["world"], x["S"], x["d"], x["nums"]
    n = {}
    n["register"] = P.write_csv(f("register"), P.REGISTER_COLS, P.register_rows(w, nums))
    n["qcew"] = P.write_csv(f("qcew"), P.QCEW_COLS, P.qcew_rows(w, d, nums))
    n["wages"] = P.write_wages(f("wages"), w, S, d, nums)
    n["counties"] = P.write_counties(f("counties"))
    n["pop"] = P.write_population(f("pop"))
    n["sos"] = P.write_sos(f("sos"), w, nums)
    n["grants"] = P.write_grants(f("grants"))
    if docs:
        import docs as DC
        import postprocess as PP
        DC.write_guideline(f("guideline"))
        DC.write_dictionary(f("dict"), n)
        n["manifest"] = DC.write_manifest(f("manifest"), n)
        PP.normalize_ooxml(f("dict"), W.PEOPLE["economist"], W.PEOPLE["economist"], "2026-11-18T15:20:00Z",
                           "2027-05-14T21:31:07Z", excel=True, company=W.ORG_LMI.split(", ")[0])
        PP.normalize_ooxml(f("grants"), W.PEOPLE["director"], W.PEOPLE["director"], "2025-07-09T14:02:00Z",
                           "2026-07-22T19:47:33Z", excel=True, company="Department of Commerce")
        PP.normalize_pdf(f("guideline"), b"D:20270201163512-06'00'", b"D:20270202091408-06'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %s" % kv for kv in n.items())))
    x["counts"] = n
    return x


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 5, 14, 16, 42, 0)
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
    x = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    os.makedirs(os.path.join(root, "generator"), exist_ok=True)
    x["golden"] = G.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                         os.path.join(root, "generator", "figures.json"))
    if root == TASK:
        import writeup
        writeup.main()
    PP.normalize_ooxml(os.path.join(root, "golden", G.BOOK), W.PEOPLE["economist"], W.PEOPLE["economist"],
                       "2027-05-17T14:05:00Z", "2027-06-03T22:18:41Z", excel=True, company=W.ORG_LMI.split(", ")[0])
    PP.normalize_pdf(os.path.join(root, "golden", G.MEMO), b"D:20270604101233-05'00'", b"D:20270604101233-05'00'")
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    stamp = dt.datetime(2027, 6, 4, 10, 15, tzinfo=CENTRAL).timestamp()
    for name in os.listdir(os.path.join(root, "golden")):
        os.utime(os.path.join(root, "golden", name), (stamp, stamp))
    return x


def main():
    import checks as CK
    import verify as V
    x = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=x,
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
