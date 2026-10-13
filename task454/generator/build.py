"""Build task454: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task454/generator/build.py              everything
    python3 task454/generator/build.py --out DIR    the pack only, into DIR
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

import docs as DC           # noqa: E402
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import sim as S             # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = dt.timezone(dt.timedelta(hours=-4))
STAMP = dt.datetime(2027, 4, 21, 15, 42, tzinfo=LOCAL)      # the extract as the administrator assembled it


def simulate():
    prods = S.coverage(S.catalog())
    rates = S.aac_rates(prods)
    idx = S.index_rates(rates)
    cl = S.claims(prods, idx, W.SCALE)
    return dict(prods=prods, rates=rates, idx=idx, claims=cl, prior=S.prior_year(prods, cl))


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or simulate()
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["claims"] = P.write_claims(w["claims"], f("claims"))
    n["aac"] = P.write_aac(w["rates"], f("aac"))
    n["drugs"] = P.write_drugs(w["prods"], f("drugs"))
    n["classes"] = P.write_classes(w["prods"], f("classes"))
    n["summary"] = P.write_summary(w["prior"], f("summary"))
    n["dict"] = P.write_dictionary(f("dict"))
    n["mco"] = P.write_mco(w["prods"], f("mco"))
    n["pdl"] = P.write_pdl(w["prods"], f("pdl"))
    n["trans"] = P.write_transmittal(f("trans"), n)
    DC.write_terms(f("terms"))
    DC.write_method(f("method"))
    DC.write_request(f("request"))
    PP.normalize_ooxml(f("drugs"), "Drug File Services", "Drug File Services", "2027-04-15T12:02:00Z",
                       "2027-04-15T12:31:44Z", excel=True, company=W.DEPARTMENT)
    PP.normalize_ooxml(f("classes"), W.PEOPLE["director"], W.PEOPLE["director"], "2026-11-18T15:20:00Z",
                       "2026-12-22T21:04:37Z", excel=True, company=W.DEPARTMENT)
    PP.normalize_ooxml(f("trans"), W.PEOPLE["account"], W.PEOPLE["account"], "2027-04-21T13:25:00Z",
                       "2027-04-21T15:38:12Z", title="Data delivery note")
    PP.normalize_ooxml(f("summary"), W.PEOPLE["pricing"], W.PEOPLE["pricing"], "2026-04-23T13:10:00Z",
                       "2026-04-24T19:55:12Z", excel=True)
    PP.normalize_ooxml(f("pdl"), "Pharmacy Program", "Pharmacy Program", "2026-12-10T14:00:00Z",
                       "2026-12-30T16:12:09Z", excel=True, company=W.DEPARTMENT)
    PP.normalize_pdf(f("terms"), b"D:20260618101500-04'00'", b"D:20260618103210-04'00'")
    PP.normalize_pdf(f("method"), b"D:20260112090500-05'00'", b"D:20260112091740-05'00'")
    PP.normalize_pdf(f("request"), b"D:20270308143000-05'00'", b"D:20270308143412-05'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    w["counts"] = n
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 4, 21, 15, 42, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False, world=None):
    import golden as G
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet, world=world)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    world["golden"] = G.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                             os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
                meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
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
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
