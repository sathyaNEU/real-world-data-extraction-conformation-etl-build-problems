"""Build task187: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task187/generator/build.py              everything
    python3 task187/generator/build.py --out DIR    the pack only, into DIR
    python3 task187/generator/build.py --no-checks  the pack, goldens and figures only"""
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
import ops as OP           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import wind as WD          # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "scada": R.SCADA, "mast": R.MAST, "anm": R.ANM, "states": R.STATES, "lifts": R.LIFTS, "layout": R.LAYOUT,
    "register": R.REGISTER, "counters": R.COUNTERS, "orders": R.WORKORDERS, "standard": D.STANDARD,
    "schedule": D.SCHEDULE, "notes": D.NOTES, "meter": R.METER, "prior": R.PRIOR,
}
DISTRACTORS = ("meter", "prior")


def world():
    m = WD.mast()
    T = WD.turbines(m)
    curve = WD.warranted()
    AN.set_curve(curve)
    ops = OP.simulate(m, T)
    return dict(mast=m, turb=T, curve=curve, ops=ops)


def build(out, quiet=False, sim=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    sim = sim or world()
    m, T, ops = sim["mast"], sim["turb"], sim["ops"]
    counts = {}
    table, _, _ = R.scada_table(m, T, ops)
    counts["scada"] = R.write_scada(p("scada"), table)
    counts["mast"] = R.write_mast(p("mast"), R.mast_rows(m))
    counts["anm"] = R.write_anm(p("anm"), R.anm_rows(ops["anm"]))
    R.write_states(p("states"))
    R.write_lifts(p("lifts"))
    counts["layout"] = R.write_layout(p("layout"))
    R.write_register(p("register"))
    counts["counters"] = R.write_counters(p("counters"), R.counters(ops))
    counts["orders"] = R.write_work_orders(p("orders"), R.work_order_rows(ops, m))
    counts["meter"] = R.write_meter(p("meter"), R.meter_rows(ops))
    R.write_prior(p("prior"), R.prior_year())
    D.write_standard(p("standard"))
    D.write_schedule(p("schedule"), sim["curve"])
    D.write_notes(p("notes"), {k: FILES[k] for k in ("scada", "mast", "anm", "states", "lifts", "layout", "register",
                                                       "counters", "orders", "meter", "prior")} |
                  {"orders": FILES["orders"]})
    am = W.PEOPLE["asset_manager"][0]
    PP.normalize_ooxml(p("states"), "Hallvard Wind Systems", am, "2019-02-14T10:12:07Z", "2025-11-03T15:40:22Z", excel=True)
    PP.normalize_ooxml(p("lifts"), W.PEOPLE["lifts"][0], am, "2026-04-20T06:58:31Z", "2026-07-16T17:02:48Z", excel=True)
    PP.normalize_ooxml(p("register"), am, am, "2015-01-19T09:31:44Z", "2025-06-30T16:18:05Z", excel=True)
    PP.normalize_ooxml(p("prior"), am, am, "2025-10-14T08:52:10Z", "2025-11-06T17:25:39Z", excel=True)
    PP.normalize_pdf(p("standard"), b"D:20260512143018+01'00'", b"D:20260515091142+01'00'")
    PP.normalize_pdf(p("schedule"), b"D:20140226110405+00'00'", b"D:20140226110405+00'00'")
    stamp = dt.datetime(2026, 10, 9, 10, 40, tzinfo=W.LONDON).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    sim["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return sim


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 9, 10, 44, 26)
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
    sim = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    fig = DL.figures(os.path.join(root, "target"))
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    DL.write_paper(os.path.join(gold, DL.PAPER), fig, DL.chart_png(fig))
    DL.write_workbook(os.path.join(gold, DL.WORKBOOK), fig)
    am = W.PEOPLE["asset_manager"][0]
    PP.normalize_pdf(os.path.join(gold, DL.PAPER), b"D:20261014152208+01'00'", b"D:20261014163951+01'00'")
    PP.normalize_ooxml(os.path.join(gold, DL.WORKBOOK), am, am, "2026-10-12T08:41:16Z", "2026-10-14T15:37:02Z",
                       excel=True)
    stamp = dt.datetime(2026, 10, 14, 16, 42, tzinfo=W.LONDON).timestamp()
    for f in os.listdir(gold):
        os.utime(os.path.join(gold, f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    sim["fig"] = fig
    return sim


def main():
    import checks as CK
    import verify as V
    sim = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), sim, os.path.join(TASK, "metadata.json"))
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
    ap.add_argument("--no-checks", action="store_true", help="build the pack, goldens and figures only")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    elif a.no_checks:
        everything(TASK)
    else:
        main()
