"""Build task453: the pack into <task>/target, the goldens into <task>/golden, metadata.json and generator/figures.json;
then the checks and the independent verifier, a second full build into a scratch folder inside the task compared byte
for byte, and target.zip cut from the final build.

    python3 task453/generator/build.py              everything
    python3 task453/generator/build.py --out DIR    the pack only, into DIR
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
import sim                  # noqa: E402
import survey as S          # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
STAMP = dt.datetime(2027, 2, 26, 15, 40, tzinfo=dt.timezone(dt.timedelta(hours=-5)))   # the folder as the Fund assembled it


def simulate():
    rows = sim.decedents()
    cyc = sim.cycles(rows)
    plants = sim.plant_logs(rows, cyc)
    ar = sim.receivables(rows)
    return {"rows": rows, "cyc": cyc, "plants": plants, "ar": ar, "tab": S.tables(W.SEED)}


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or simulate()
    f = lambda k: os.path.join(out, W.FILES[k])
    n = {}
    w["permits"] = P.permits(w["rows"])
    n["permits"] = P.write_permits(w["permits"], f("permits"))
    n["register"] = P.write_register(f("register"))
    lrows = P.ledger_rows(w["ar"])
    w["lrows"] = lrows
    n["ar_halbrook"] = P.write_ar_halbrook(lrows, w["ar"], f("ar_halbrook"))
    n["ar_shoreline"] = P.write_ar_shoreline(lrows, w["ar"], f("ar_shoreline"))
    n["ar_members"] = P.write_ar_members(lrows, w["ar"], f("ar_members"))
    n["cycles"] = P.write_cycles(w["cyc"], f("cycles"))
    n["plant"] = P.write_plant(w["plants"], f("plant"))
    n["deaths"] = P.write_deaths(w["rows"], f("deaths"))
    for y in S.WAVES:
        DC.write_survey(w["tab"], y, f("s%d" % y))
    DC.write_regulation(f("reg"))
    DC.write_rules(f("rules"))
    DC.write_stack(f("stack"))
    PP.normalize_ooxml(f("register"), W.PEOPLE["secretary"], W.PEOPLE["secretary"], "2021-03-09T15:22:00Z",
                       "2027-01-15T19:06:44Z", excel=True, company=W.FUND)
    PP.normalize_ooxml(f("ar_shoreline"), "SMG Finance", "SMG Finance", "2027-02-26T13:51:08Z", "2027-02-26T13:51:08Z",
                       excel=True, company="Shoreline Memorial Group")
    PP.normalize_ooxml(f("deaths"), W.PEOPLE["vitals"], W.PEOPLE["vitals"], "2027-02-12T16:30:00Z",
                       "2027-02-12T16:41:27Z", excel=True, company=W.AGENCY)
    PP.normalize_pdf(f("s1996"), b"D:19970604101544-04'00'", b"D:19970604102231-04'00'")
    PP.normalize_pdf(f("s2006"), b"D:20070612140210-04'00'", b"D:20070612141957-04'00'")
    PP.normalize_pdf(f("s2016"), b"D:20170607093318-04'00'", b"D:20170607095102-04'00'")
    PP.normalize_pdf(f("reg"), b"D:20241230113005-05'00'", b"D:20241230113642-05'00'")
    PP.normalize_pdf(f("rules"), b"D:20251118154820-05'00'", b"D:20251118160233-05'00'")
    PP.normalize_pdf(f("stack"), b"D:20260303084511-05'00'", b"D:20260303085937-05'00'")
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
    stamp = (2027, 2, 26, 15, 40, 0)
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
