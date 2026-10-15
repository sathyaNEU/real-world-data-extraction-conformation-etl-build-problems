"""Build task458: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task458/generator/build.py              everything
    python3 task458/generator/build.py --out DIR    the pack only, into DIR
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

import claims as CL         # noqa: E402
import members as M         # noqa: E402
import pack as P            # noqa: E402
import providers as PV      # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
PACIFIC = dt.timezone(dt.timedelta(hours=-8))
STAMP = dt.datetime(2026, 11, 12, 15, 26, tzinfo=PACIFIC)       # the folder as Network Analytics assembled it


def world():
    CL.CHARGE.clear()
    persons = M.population()
    M.member_numbers(persons)
    clins, orgs = PV.build()
    lines, bk = CL.build(persons, clins, orgs)
    recs = P.nppes_records(clins, orgs)
    return {"persons": persons, "clins": clins, "orgs": orgs, "lines": lines, "recs": recs}


def build(out, quiet=False, docs=True):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    w = world()
    n = {}
    n["claims"] = P.write_claims(P.claim_rows(w["lines"]), f("claims"))
    n["spans"] = P.write_spans(P.span_rows(w["persons"]), f("spans"))
    monthly, weeks = P.monthly_and_weeks(w["recs"])
    n["nppes"] = P.write_nppes(monthly, f("nppes"))
    for k, rows in zip(P.WEEK_KEYS, weeks):
        n[k] = P.write_nppes(rows, f(k))
    n["deact"] = P.write_deactivations(w["recs"], f("deact"))
    n["zipcty"] = P.write_zip_county(f("zipcty"))
    n["nucc"] = P.write_nucc(f("nucc"))
    n["fees"] = P.write_fees(f("fees"))
    n["adequacy"] = P.write_adequacy(f("adequacy"), w["persons"])
    n["ofm"] = P.write_ofm(f("ofm"))
    if docs:
        import docs as DC
        import postprocess as PP
        n["dict"] = P.write_dictionary(f("dict"))
        n["manifest"] = P.write_manifest(f("manifest"), {k: v for k, v in n.items() if k not in ("dict",)})
        DC.write_policy(f("policy"))
        PP.normalize_ooxml(f("deact"), "CMS", "CMS", "2026-11-10T14:02:00Z", "2026-11-10T14:02:00Z", excel=True,
                           company="CMS")
        PP.normalize_ooxml(f("zipcty"), "HUD PD&R", "HUD PD&R", "2026-09-17T13:41:00Z", "2026-09-17T13:55:12Z",
                           excel=True, company="HUD")
        PP.normalize_ooxml(f("adequacy"), W.PEOPLE["director"], W.PEOPLE["director"], "2026-08-12T16:20:00Z",
                           "2026-08-14T18:03:51Z", excel=True, company=W.ORG)
        PP.normalize_ooxml(f("dict"), W.PEOPLE["analyst"], W.PEOPLE["analyst"], "2025-09-03T17:12:00Z",
                           "2026-11-12T22:41:09Z", excel=True, company=W.ORG)
        PP.normalize_pdf(f("policy"), b"D:20260519141205-07'00'", b"D:20260521093344-07'00'")
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
    stamp = (2026, 11, 12, 15, 26, 0)
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
    PP.normalize_ooxml(os.path.join(root, "golden", G.SCORECARD), W.PEOPLE["analyst"], W.PEOPLE["director"],
                       "2026-11-13T17:05:00Z", "2026-11-16T23:48:27Z", excel=True, company=W.ORG)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    stamp = dt.datetime(2026, 11, 16, 15, 48, tzinfo=PACIFIC).timestamp()
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
