"""Build task256: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task256/generator/build.py              everything
    python3 task256/generator/build.py --out DIR    the pack only, into DIR"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
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
    "roster": R.ROSTER, "ostrander": R.OSTRANDER, "fernhill": R.FERNHILL, "fleet": R.FLEET, "disposals": R.DISPOSALS,
    "retrofits": R.RETROFITS, "work_orders": R.WORK_ORDERS, "comfort": R.COMFORT, "claims": R.CLAIMS,
    "standard": D.STANDARD, "fit": D.FIT_REPORT, "survey": D.SURVEY, "fm": D.FM_PROCEDURE, "trial": R.TRIAL,
}
DISTRACTORS = ("comfort", "claims")
CALL_FILES = ("standard", "fit", "survey", "roster", "ostrander", "fernhill", "trial")
ASK_FILES = ("fleet", "disposals", "retrofits", "work_orders", "fm")


def build(out, quiet=False, st=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    st = st or AN.world_state()
    counts = {}
    nums = R.ostrander_numbers(st["enc"])
    counts["roster"] = R.write_roster(p("roster"), st["people"])
    counts["ostrander"] = R.write_ostrander(p("ostrander"), st["enc"], nums)
    counts["fernhill"] = R.write_fernhill(p("fernhill"), st["enc"], nums)
    counts["fleet"] = R.write_fleet(p("fleet"), st["buses"])
    counts["disposals"] = R.write_disposals(p("disposals"), st["buses"])
    counts["retrofits"] = R.write_retrofits(p("retrofits"), st["buses"])
    counts["work_orders"] = R.write_work_orders(p("work_orders"), st["wos"])
    counts["comfort"] = R.write_comfort(p("comfort"), st["comfort"])
    counts["claims"] = R.write_claims(p("claims"), st["claims"])
    counts["trial"] = R.write_trial(p("trial"), st["trial"])
    D.write_standard(p("standard"))
    D.write_fit_report(p("fit"))
    D.write_survey(p("survey"))
    D.write_fm_procedure(p("fm"))
    PP.normalize_ooxml(p("roster"), "HRIS Export", "HRIS Export", "2026-10-01T13:06:41Z", "2026-10-01T13:06:41Z",
                       excel=True)
    PP.normalize_ooxml(p("comfort"), W.PEOPLE["fleet"][0], W.PEOPLE["fleet"][0], "2023-05-30T15:42:10Z",
                       "2023-06-02T20:11:37Z", excel=True)
    PP.normalize_pdf(p("standard"), b"D:20240314094410-07'00'", b"D:20240314095203-07'00'")
    PP.normalize_pdf(p("fit"), b"D:20260828153318-05'00'", b"D:20260828160942-05'00'")
    PP.normalize_pdf(p("survey"), b"D:20130520101507-04'00'", b"D:20130520101507-04'00'")
    PP.normalize_pdf(p("fm"), b"D:20230109081530-07'00'", b"D:20230109082204-07'00'")
    stamp = dt.datetime(2026, 10, 1, 8, 47, tzinfo=dt.timezone(dt.timedelta(hours=-7))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    st["counts"] = counts
    st["bm"] = {o: W.option_months(st["buses"], o) for o in W.OPTION_ORDER}
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return st


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 1, 8, 48, 6)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def write_metadata(path):
    meta = {"task": "task256", "distractor_files": [FILES[k] for k in DISTRACTORS],
            "deliverables": ["workstation_configurations_2027.xlsx", "operator_accommodation_2027.svg"],
            "stated_inputs": ["{:,}".format(p) for _, _, p in W.CONFIGS if p],
            "forward_dated": {FILES["fernhill"]: "cert_expires: the expiry of medical certificates issued up to "
                                                  "30 September 2026"},
            "provenance": "Constructed records of a fictional transit authority, its builder and a fictional survey "
                          "institute (declared): rosters, examinations, fleet records, work orders and documents "
                          "generated by task256/generator; no third-party data."}
    with open(path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def everything(root, quiet=False):
    import golden as G
    st = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    fig = AN.figures(st)
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    G.write_workbook(os.path.join(gold, G.WORKBOOK), fig)
    PP.normalize_ooxml(os.path.join(gold, G.WORKBOOK), W.PEOPLE["fleet"][0], W.PEOPLE["fleet"][0],
                       "2026-10-14T16:20:05Z", "2026-11-03T22:48:31Z", excel=True)
    G.write_chart(os.path.join(gold, G.CHART), fig)
    PP.normalize_svg(os.path.join(gold, G.CHART))
    write_metadata(os.path.join(root, "metadata.json"))
    st["fig"] = fig
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
            dt_, dg_ = digest(os.path.join(TASK, "target")), digest(os.path.join(tmp, "target"))
            gt_, gg_ = digest(os.path.join(TASK, "golden")), digest(os.path.join(tmp, "golden"))
            keep = os.environ.get("KEEP_DIFF")
            if keep:
                shutil.copytree(tmp, keep, dirs_exist_ok=True)
            raise SystemExit("second build differs: target %s, golden %s, %s; files %s" % (
                same_t, same_g, same, [f for f in dt_ if dt_[f] != dg_.get(f)] + [f for f in gt_ if gt_[f] != gg_.get(f)]))
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
