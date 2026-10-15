"""Build task260: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task260/generator/build.py              everything
    python3 task260/generator/build.py --out DIR    the pack only, into DIR
    python3 task260/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import tempfile      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
NAMES = dict({"export_" + s: f for s, f in K.EXPORTS.items()},
             guide=K.EXPORT_GUIDE, cases=K.CASES, panels=K.PANELS, protocol=K.PROTOCOL, ris=K.RIS, codes=K.CODES,
             locations=K.LOCATIONS, visits=K.VISITS, workforce=K.WORKFORCE, quote_q=K.QUOTES["Ondrix"],
             quote_a=K.QUOTES["Halvic"], quote_v=K.QUOTES["Lumidra"], summaries=K.PRODUCT_SUMMARIES, kpis=K.KPIS,
             qa=K.QA_SCORES)
DISTRACTORS = ("summaries", "kpis", "qa")
CALL_FILES = ("export_S1", "export_S2", "export_S3", "guide", "cases", "protocol")
ASK_FILES = ("ris", "codes", "locations", "visits", "workforce", "quote_q", "quote_a", "quote_v")
NEUTRAL = ("panels",)


def world():
    RD = W.readers()
    PN = W.panels(RD)
    studies = [W.study(S, PN[S["sid"]], K.STUDY_SEEDS[S["sid"]]) for S in K.STUDIES]
    Rr = W.ris()
    V = W.visits(Rr)
    WF, wf_info = W.workforce(RD)
    return dict(RD=RD, PN=PN, studies=studies, ris=Rr, visits=V, workforce=WF, wf_info=wf_info)


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, NAMES[k])
    S = world()
    counts = {}
    for st in S["studies"]:
        counts["export_" + st["S"]["sid"]] = R.write_export(p("export_" + st["S"]["sid"]), st)
    R.write_cases(p("cases"), S["studies"])
    R.write_panels(p("panels"), S["studies"])
    counts["ris"] = R.write_ris(p("ris"), S["ris"])
    R.write_codes(p("codes"))
    R.write_locations(p("locations"))
    R.write_visits(p("visits"), S["visits"])
    R.write_workforce(p("workforce"), S["workforce"])
    R.write_kpis(p("kpis"))
    counts["qa"] = R.write_qa(p("qa"), S["RD"])
    D.write_protocol(p("protocol"))
    D.write_export_guide(p("guide"))
    D.write_quote(p("quote_q"), "Ondrix")
    D.write_quote(p("quote_a"), "Halvic")
    D.write_quote(p("quote_v"), "Lumidra")
    D.write_product_summaries(p("summaries"))
    research = K.PEOPLE["research"]
    PP.normalize_ooxml(p("cases"), research, research, "2026-02-02T10:14:22Z", "2026-07-08T15:41:09Z", excel=True)
    PP.normalize_ooxml(p("panels"), research, research, "2026-01-26T09:02:51Z", "2026-07-09T11:20:36Z", excel=True)
    PP.normalize_ooxml(p("visits"), "Screening Office", "Screening Office", "2025-09-15T08:31:04Z",
                       "2026-10-02T13:55:18Z", excel=True)
    PP.normalize_ooxml(p("workforce"), "Workforce Information", "Workforce Information", "2026-10-09T07:12:40Z",
                       "2026-10-09T07:12:40Z", excel=True)
    PP.normalize_ooxml(p("kpis"), "Screening Office", "Screening Office", "2024-05-20T12:00:31Z",
                       "2026-06-03T09:47:15Z", excel=True)
    PP.normalize_pdf(p("protocol"), b"D:20260112101520+00'00'", b"D:20260112101520+00'00'")
    PP.normalize_pdf(p("guide"), b"D:20260703142208+01'00'", b"D:20260703142208+01'00'")
    PP.normalize_pdf(p("quote_q"), b"D:20260924160213+01'00'", b"D:20260924160213+01'00'")
    PP.normalize_pdf(p("quote_a"), b"D:20260928114751+01'00'", b"D:20260928114751+01'00'")
    PP.normalize_pdf(p("quote_v"), b"D:20260922093340+01'00'", b"D:20260922093340+01'00'")
    PP.normalize_pdf(p("summaries"), b"D:20260120153012+00'00'", b"D:20260120153012+00'00'")
    stamp = dt.datetime(2026, 10, 12, 16, 20, tzinfo=dt.timezone(dt.timedelta(hours=1))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return dict(counts=counts, S=S)


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 10, 12, 16, 21, 4)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def write_metadata(path):
    meta = {"task": "task260", "distractor_files": [NAMES[k] for k in DISTRACTORS],
            "wrong_basis_distractor": {"file": NAMES["summaries"],
                                       "basis": "each tool's standalone area on the vendor's own datasets, not the "
                                                "service's readers' accuracy with the tool",
                                       "ruled_out_by": "ai_evaluation_protocol_v2.pdf, 3.1 and 3.2"},
            "deliverables": list(K.DELIVERABLES),
            "call_files": [NAMES[k] for k in CALL_FILES], "ask_files": [NAMES[k] for k in ASK_FILES],
            "provenance": "Constructed records of a fictional English breast screening service, its fictional reader "
                          "study platform and three fictional AI vendors (declared): the reader study exports, case "
                          "sets, panels, imaging-system records, location table, mobile visit schedule, workforce "
                          "extract, quotes, protocol, KPIs, QA scores and summaries are generated by task260/generator "
                          "from a simulated service; no third-party data; town names are invented."}
    with open(path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def everything(root, quiet=False):
    import deliver as G
    st = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    res = G.compute(os.path.join(root, "target"))
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(res["figures"], fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    G.write_paper(os.path.join(gold, K.DELIVERABLES[0]), res)
    G.write_xlsx(os.path.join(gold, K.DELIVERABLES[1]), res)
    G.write_chart(os.path.join(gold, K.DELIVERABLES[2]), res)
    PP.normalize_pdf(os.path.join(gold, K.DELIVERABLES[0]), b"D:20261110094512+00'00'", b"D:20261110101138+00'00'")
    PP.normalize_ooxml(os.path.join(gold, K.DELIVERABLES[1]), K.PEOPLE["lead"], K.PEOPLE["lead"],
                       "2026-11-06T13:22:05Z", "2026-11-10T09:58:44Z", excel=True)
    write_metadata(os.path.join(root, "metadata.json"))
    st["res"] = res
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
    ap.add_argument("--golden", action="store_true", help="build the pack and the goldens, no checks")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    elif a.golden:
        everything(TASK)
    else:
        main()
