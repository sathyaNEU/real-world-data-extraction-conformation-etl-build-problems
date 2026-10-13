"""Build task186: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task186/generator/build.py              everything
    python3 task186/generator/build.py --out DIR    the pack only, into DIR"""
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
import market as M         # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import survey as SV        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "log": R.LOG, "rack": R.RACK, "register": R.REGISTER, "crosswalk": R.CROSSWALK, "survey": R.SURVEY,
    "frame": R.FRAME, "subs": R.SUBMISSIONS, "brands": R.BRANDS, "opslog": R.OPSLOG, "bulletin": R.BULLETIN,
    "complaints": R.COMPLAINTS, "standard": D.STANDARD, "schedule": D.SCHEDULE, "notes": D.NOTES,
}
DISTRACTORS = ("bulletin", "complaints")


def world():
    sim = AN.state(M.simulate())
    sim["log"], sim["log_stats"] = M.log_rows(sim)
    sim["returns"] = SV.returns(sim)
    sim["frame"] = SV.frame(sim)
    sim["subs"] = SV.submissions(sim)
    return sim


def build(out, quiet=False, sim=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    sim = sim or world()
    counts = {}
    counts["log"] = R.write_log(p("log"), sim["log"])
    counts["rack"] = R.write_rack(p("rack"), sim["rack"])
    R.write_register(p("register"), sim)
    counts["crosswalk"] = R.write_crosswalk(p("crosswalk"), sim)
    counts["survey"] = R.write_survey(p("survey"), sim["returns"])
    counts["frame"] = R.write_frame(p("frame"), sim["frame"])
    counts["subs"] = R.write_submissions(p("subs"), sim["subs"])
    R.write_brands(p("brands"))
    R.write_opslog(p("opslog"), sim["log_stats"], sim)
    counts["bulletin"] = R.write_bulletin(p("bulletin"), sim)
    counts["complaints"] = R.write_complaints(p("complaints"), sim)
    D.write_standard(p("standard"))
    D.write_schedule(p("schedule"))
    D.write_notes(p("notes"), {k: FILES[k] for k in ("log", "rack", "register", "crosswalk", "survey", "frame", "subs",
                                                       "brands", "opslog", "bulletin", "complaints")})
    PP.normalize_ooxml(p("register"), "FPM Reporting Platform", "FPM Reporting Platform", "2019-06-24T13:20:41Z",
                       "2026-11-16T11:02:37Z", excel=True)
    PP.normalize_ooxml(p("opslog"), "Platform Operations", W.PEOPLE["analyst"][0], "2023-02-07T15:44:09Z",
                       "2026-11-16T10:31:52Z", excel=True)
    PP.normalize_ooxml(p("bulletin"), W.DIVISION, W.PEOPLE["analyst"][0], "2026-01-12T14:05:16Z",
                       "2026-11-09T15:12:40Z", excel=True)
    PP.normalize_pdf(p("standard"), b"D:20250918103512-04'00'", b"D:20250922141927-04'00'")
    PP.normalize_pdf(p("schedule"), b"D:20261006091544-04'00'", b"D:20261006091544-04'00'")
    stamp = dt.datetime(2026, 11, 16, 10, 48, tzinfo=dt.timezone(dt.timedelta(hours=-5))).timestamp()
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
    stamp = (2026, 11, 16, 10, 52, 18)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False, full=False):
    import deliver as DL
    import metadata as MD
    sim = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    mc = AN.main_call(sim) if full else AN.golden(sim)
    litres = SV.litres_by_brand(sim, sim["returns"])
    priced, _ = SV.priced_itself(sim, sim["subs"])
    fig = DL.figures(mc, litres, priced)
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    DL.write_memo(os.path.join(gold, DL.MEMO), fig, DL.chart_png(fig))
    DL.write_scope(os.path.join(gold, DL.SCOPE), fig)
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    sim["mc"], sim["fig"], sim["litres"], sim["priced"] = mc, fig, litres, priced
    return sim


def main():
    import checks as CK
    import verify as V
    sim = everything(TASK, full=True)
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
        everything(TASK, full=True)
    else:
        main()
