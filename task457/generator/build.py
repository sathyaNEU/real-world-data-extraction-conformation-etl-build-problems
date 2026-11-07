"""Build task457: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json; then the checks and the independent verifier, a second full build into a scratch folder
inside the task compared byte for byte, and target.zip cut from the final build.

    python3 task457/generator/build.py              everything
    python3 task457/generator/build.py --out DIR    the pack only, into DIR
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

import disclosures as DS    # noqa: E402
import pack as P            # noqa: E402
import people as PE         # noqa: E402
import register as RG       # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2027, 1, 21, 16, 42, tzinfo=EASTERN)       # the extract as the office assembled it


def world():
    fac, namesakes, mfrs = PE.population()
    recs = RG.records(fac, mfrs, namesakes)
    rows, meta = P.register_rows(recs, mfrs, None)
    P.matcher(rows, fac, namesakes)
    june = P.vintages(rows, meta)
    disc, items, events, ents = DS.build(fac, mfrs)
    return {"fac": fac, "namesakes": namesakes, "mfrs": mfrs, "recs": recs, "rows": rows, "meta": meta, "june": june,
            "disc": disc, "items": items, "events": events, "ents": ents}


def build(out, quiet=False, docs=True):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, P.FILES[k])
    w = world()
    n = {}
    n["register"] = P.write_register(w["rows"], f("register"))
    n["register_june"] = P.write_register(w["june"], f("register_june"))
    n["profiles"] = P.write_profiles(w["fac"], w["namesakes"], f("profiles"))
    n["research"] = P.write_research(w["fac"], w["mfrs"], f("research"))
    n["roster"] = P.write_roster(w["fac"], f("roster"))
    n["depts"] = P.write_depts(f("depts"))
    n["entities"] = P.write_entities(w["ents"], f("entities"))
    n["export"] = P.write_export(w["disc"], w["items"], f("export"))
    n["history"] = P.write_history(w["events"], f("history"))
    n["nih"] = P.write_nih(w["fac"], f("nih"))
    if docs:
        import docs as DC
        import postprocess as PP
        DC.write_policy(f("policy"))
        DC.write_guide(f("guide"))
        PP.normalize_ooxml(f("export"), "COI Disclosure System", "COI Disclosure System", "2027-01-21T21:12:00Z",
                           "2027-01-21T21:14:37Z", excel=True, company=W.ORG)
        PP.normalize_pdf(f("policy"), b"D:20240611101503-04'00'", b"D:20240611103218-04'00'")
        PP.normalize_pdf(f("guide"), b"D:20261102091544-05'00'", b"D:20261102094810-05'00'")
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
    stamp = (2027, 1, 21, 16, 42, 0)
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
    PP.normalize_ooxml(os.path.join(root, "golden", G.DOCKET), W.PEOPLE["director"], W.PEOPLE["director"],
                       "2027-01-26T15:10:00Z", "2027-01-27T14:22:41Z", title="Docket for the meeting of 11 February 2027",
                       company=W.ORG)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    stamp = dt.datetime(2027, 1, 27, 9, 22, tzinfo=EASTERN).timestamp()
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
