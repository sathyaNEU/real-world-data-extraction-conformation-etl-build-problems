"""Build task185: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task185/generator/build.py              everything
    python3 task185/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN      # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "daily": R.DAILY, "register": R.REGISTER, "parallel": R.PARALLEL, "district": R.DISTRICT,
    "stations": R.STATIONS, "history": D.HISTORY, "manual": D.MANUAL, "terms27": D.TERMS_27, "terms26": D.TERMS_26,
    "notes": D.NOTES, "schedule": R.SCHEDULE, "blocks": R.BLOCKS, "claims": R.CLAIMS, "ledger": R.LEDGER,
}
DISTRACTORS = ("district", "terms26")


def build(out, quiet=False, st=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    st = st or AN.world_state()
    counts = {}
    counts["daily"] = R.write_daily(p("daily"), st["mf"])
    st["register_days"] = R.write_register(p("register"), st["mf"])
    counts["parallel"] = R.write_parallel(p("parallel"), st["pairs"])
    counts["district"] = R.write_district(p("district"))
    R.write_stations(p("stations"))
    counts["schedule"] = R.write_schedule(p("schedule"), st["members"], st["blocks"])
    R.write_blocks(p("blocks"), st["members"], st["blocks"])
    counts["claims"] = R.write_claims(p("claims"), st["claims"])
    counts["ledger"] = R.write_ledger(p("ledger"), st["ledger"])
    D.write_manual(p("manual"))
    D.write_history(p("history"))
    D.write_terms(p("terms27"), 2027, W.DEDUCTIBLE_DAYS, W.HEAT_RATE, W.SEVERE_RATE, W.CAP,
                  "Quotation terms for the renewal of 1 November 2027.", "25 August 2027")
    d26, h26, s26, c26 = W.TERMS_HISTORY[2026]
    D.write_terms(p("terms26"), 2026, d26, h26, s26, c26, "Bound terms.", "16 October 2026")
    D.write_notes(p("notes"), {k: FILES[k] for k in ("daily", "register", "parallel", "district", "stations",
                                                       "schedule", "blocks", "claims", "ledger")})
    PP.normalize_ooxml(p("register"), "NCS Data Portal", "NCS Data Portal", "2009-06-17T02:41:09Z",
                       "2027-08-27T00:12:48Z", excel=True)
    PP.normalize_ooxml(p("blocks"), W.PEOPLE["coop"][0], W.PEOPLE["coop"][0], "2019-07-08T23:05:31Z",
                       "2027-08-02T06:37:14Z", excel=True)
    PP.normalize_pdf(p("manual"), b"D:20260226151204+10'30'", b"D:20260227092249+10'30'")
    PP.normalize_pdf(p("history"), b"D:20270809103317+09'30'", b"D:20270809103317+09'30'")
    PP.normalize_pdf(p("terms27"), b"D:20270825141506+09'30'", b"D:20270825143922+09'30'")
    PP.normalize_pdf(p("terms26"), b"D:20261016112030+10'30'", b"D:20261016112558+10'30'")
    stamp = dt.datetime(2027, 8, 27, 16, 40, tzinfo=dt.timezone(dt.timedelta(hours=9, minutes=30))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    st["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return st


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 8, 27, 16, 42, 6)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    st = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    mc = AN.main_call(st)
    fig = AN.figures(st)
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    DL.write_quote(os.path.join(gold, DL.QUOTE), fig, mc)
    PP.normalize_pdf(os.path.join(gold, DL.QUOTE), b"D:20270906090412+09'30'", b"D:20270906093851+09'30'")
    DL.write_payouts(os.path.join(gold, DL.PAYOUTS), fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    st["mc"], st["fig"] = mc, fig
    return st


def main():
    import checks as CK
    import verify as V
    st = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), st, os.path.join(TASK, "metadata.json"))
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
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()).hexdigest()
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
