"""Build task181: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task181/generator/build.py              everything
    python3 task181/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import sim as S            # noqa: E402
import traffic as T        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "fdps": R.FDPS, "occ": R.OCC, "codes": R.CODES, "plan": R.PLAN, "register": R.REGISTER, "slots": R.SLOTS,
    "regs": R.REGS, "clog": R.CLOG, "ctab": R.CTAB, "plan_doc": D.PLAN_DOC, "closeout": D.CLOSEOUT, "om": D.OM,
    "notes": D.NOTES, "roster": R.ROSTER, "met": R.MET,
}
DISTRACTORS = ("roster", "met")


def closeout_table(w):
    """Summer 2025 and 2026 ATM-related losses and flight hours by sector, from the record as the pack carries it."""
    occ = w["occ_rows"]
    t = w["t"]
    tab = {}
    for k, s in enumerate(W.SECTORS):
        r = {}
        for y, key in ((2025, "25"), (2026, "26")):
            a, b = W.season(y)
            lo, hi = a.strftime("%Y-%m-%d %H:%M"), b.strftime("%Y-%m-%d %H:%M")
            r["l" + key] = sum(1 for o in occ if o["occurrence_type"] == "SMI" and o["atm_contribution"] in ("D", "I")
                               and o["sector"] == W.NAME[s] and lo <= o["occurrence_date"] + " " + o["time_utc"] < hi)
            m = (t["sec"] == k) & (t["t0"] >= T.secs(a)) & (t["t0"] < T.secs(b))
            r["fh" + key] = float((t["t1"][m] - t["t0"][m]).sum()) / 3600.0
        tab[s] = r
    a, b = W.season(2026)
    lo, hi = a.strftime("%Y-%m-%d %H:%M"), b.strftime("%Y-%m-%d %H:%M")
    s26 = [o for o in occ if o["occurrence_type"] == "SMI" and lo <= o["occurrence_date"] + " " + o["time_utc"] < hi]
    tab["sev"] = {c: sum(1 for o in s26 if o["atm_contribution"] in ("D", "I") and o["severity"] == c) for c in "ABC"}
    tab["non26"] = sum(1 for o in s26 if o["atm_contribution"] == "N")
    a25, b25 = W.season(2025)
    lo25, hi25 = a25.strftime("%Y-%m-%d %H:%M"), b25.strftime("%Y-%m-%d %H:%M")
    s25 = [o for o in occ if lo25 <= o["occurrence_date"] + " " + o["time_utc"] < hi25]
    tab["sev25"] = {c: sum(1 for o in s25 if o["occurrence_type"] == "SMI" and o["atm_contribution"] in ("D", "I")
                           and o["severity"] == c) for c in "ABC"}
    all26 = [o for o in occ if lo <= o["occurrence_date"] + " " + o["time_utc"] < hi]
    tab["other25"] = {k: sum(1 for o in s25 if o["occurrence_type"] == k) for k in ("LB", "PLOC", "DEV", "ATMT", "AI", "WTE")}
    tab["other26"] = {k: sum(1 for o in all26 if o["occurrence_type"] == k) for k in ("LB", "PLOC", "DEV", "ATMT", "AI", "WTE")}
    return tab


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = world or S.simulate()
    w["occ_rows"] = R.occurrence_table(w["occ"])
    counts = {}
    counts["fdps"] = R.write_fdps(p("fdps"), w["f"], w["t"], w["ids"])
    counts["occ"] = R.write_csv(p("occ"), w["occ_rows"], R.OCC_COLS)
    counts["codes"] = R.write_codes(p("codes"))
    counts["plan"] = R.write_plan(p("plan"), w["fp"], w["tp"])
    R.write_register(p("register"))
    counts["slots"] = R.write_slots(p("slots"), w["slots"])
    counts["regs"] = R.write_regs(p("regs"), w["regs"])
    counts["clog"] = R.write_clog(p("clog"), w["log"])
    counts["ctab"] = R.write_ctab(p("ctab"))
    counts["met"] = R.write_met(p("met"))
    R.write_roster(p("roster"))
    D.write_plan(p("plan_doc"))
    w["closeout"] = closeout_table(w)
    D.write_closeout(p("closeout"), w["closeout"])
    D.write_om(p("om"))
    D.write_notes(p("notes"))
    PP.normalize_ooxml(p("roster"), "Kenny Lassen", "Kenny Lassen", "2026-05-18T07:41:12Z", "2026-09-02T13:05:47Z",
                       excel=True)
    PP.normalize_pdf(p("plan_doc"), b"D:20260210151203+01'00'", b"D:20260212094418+01'00'")
    PP.normalize_pdf(p("closeout"), b"D:20261005163021+02'00'", b"D:20261006110734+02'00'")
    PP.normalize_pdf(p("om"), b"D:20260324100512+01'00'", b"D:20260326081940+01'00'")
    stamp = dt.datetime(2026, 10, 12, 16, 20, tzinfo=W.LOCAL).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 12, 16, 22, 4)
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
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
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
