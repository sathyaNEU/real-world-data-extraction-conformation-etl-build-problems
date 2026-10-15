"""Build task262: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task262/generator/build.py              everything
    python3 task262/generator/build.py --out DIR    the pack only, into DIR
    python3 task262/generator/build.py --golden     the pack and the goldens, no checks"""
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
import bridges as BR       # noqa: E402
import common as K         # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
DISTRACTORS = (K.INDICATORS, K.SURVEY)
CALL_FILES = (K.COHORT, K.EARN, K.HIST, K.RECODE, K.CPI_FILE, K.GUIDE, K.DICT, K.BRIEF)
ASK_FILES = (K.PART, K.LEDGER, K.OFFICES, K.GUIDELINES, K.CLOSEOUT)


def world():
    regions = R.identify(W.province())
    P = BR.people()
    rows = BR.records(P)
    lines = BR.ledger(P)
    return dict(regions=regions, P=P, rows=rows, lines=lines)


def closeout_figures(S):
    by_year = {}
    for d, cc, acct, amt, jn, desc in S["lines"]:
        by_year[d.year] = by_year.get(d.year, 0.0) + amt
    r = K.rng("follow-up")
    ended = [p for p in S["P"] if p["outcome"] in ("Completed", "Withdrawn")]
    answered = [p for p in ended if r.random() < (0.62 if p["outcome"] == "Completed" else 0.31)]
    working = sum(1 for p in answered if r.random() < (0.81 if p["outcome"] == "Completed" else 0.52))
    return by_year, len(answered), int(round(100.0 * working / len(answered)))


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    S = world()
    regs = S["regions"]
    counts = {K.COHORT: R.write_cohort(p(K.COHORT), regs), K.EARN: R.write_earnings(p(K.EARN), regs),
              K.HIST: R.write_history(p(K.HIST), regs), K.RECODE: R.write_recode(p(K.RECODE)),
              K.CPI_FILE: R.write_cpi(p(K.CPI_FILE)), K.PART: R.write_participants(p(K.PART), S["rows"]),
              K.LEDGER: R.write_ledger(p(K.LEDGER), S["lines"]), K.OFFICES: R.write_offices(p(K.OFFICES))}
    n_children = sum(len(x["fam_of"]) for x in regs)
    n_families = sum(x["nfam"] for x in regs)
    n_history = sum(int(x["files"].sum()) for x in regs)
    D.write_user_guide(p(K.GUIDE), n_children, n_families, n_history)
    D.write_dictionary(p(K.DICT))
    D.write_brief(p(K.BRIEF))
    D.write_guidelines(p(K.GUIDELINES))
    by_year, answered, working = closeout_figures(S)
    D.write_closeout(p(K.CLOSEOUT), by_year, answered, working)
    D.write_indicators(p(K.INDICATORS))
    D.write_survey(p(K.SURVEY))
    PP.COMPANY = K.CENTRE
    PP.normalize_ooxml(p(K.DICT), K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-05-28T14:20:37Z",
                       "2026-06-19T18:02:51Z", excel=True)
    PP.normalize_pdf(p(K.GUIDE), b"D:20260619140913-04'00'", b"D:20260622091442-04'00'")
    PP.COMPANY = K.FOUNDATION
    PP.normalize_ooxml(p(K.BRIEF), K.PEOPLE["director"], K.PEOPLE["director"], "2026-11-04T19:31:00Z",
                       "2026-11-06T14:12:00Z")
    PP.normalize_ooxml(p(K.INDICATORS), "Research and Evaluation", "Research and Evaluation", "2023-03-09T15:44:18Z",
                       "2023-03-21T20:07:33Z", excel=True)
    PP.normalize_pdf(p(K.GUIDELINES), b"D:20181211163250-05'00'", b"D:20181211163250-05'00'")
    PP.normalize_pdf(p(K.CLOSEOUT), b"D:20240418102716-04'00'", b"D:20240419150833-04'00'")
    PP.normalize_pdf(p(K.SURVEY), b"D:20230914113105-04'00'", b"D:20230914113105-04'00'")
    stamp = dt.datetime(2026, 11, 6, 10, 22, tzinfo=dt.timezone(dt.timedelta(hours=-5))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return dict(counts=counts, S=S, closeout=(by_year, answered, working))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2026, 11, 6, 10, 23, 14)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def write_metadata(path):
    meta = {"task": "task262", "distractor_files": list(DISTRACTORS),
            "deliverables": list(K.DELIVERABLES), "call_files": list(CALL_FILES), "ask_files": list(ASK_FILES),
            "provenance": "Constructed records (declared): the fictional Provincial Research Data Centre's linked "
                          "intergenerational income extract (cohort file, children's earnings, parents' income history, "
                          "region recode, price index, user guide, data dictionary) and the fictional Wrenmore Foundation's "
                          "brief, Bridges participant export, program ledger, office list, guidelines, close-out summary, "
                          "regional economic indicators and youth aspirations survey, all generated by task262/generator "
                          "from a simulated province and a simulated program; no third-party data; every organisation, "
                          "place and person is invented."}
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
    chart = os.path.join(gold, K.DELIVERABLES[2])
    G.write_chart(chart, res)
    G.write_memo(os.path.join(gold, K.DELIVERABLES[0]), res, chart)
    G.write_xlsx(os.path.join(gold, K.DELIVERABLES[1]), res)
    PP.COMPANY = K.FOUNDATION
    PP.normalize_pdf(os.path.join(gold, K.DELIVERABLES[0]), b"D:20261117151208-05'00'", b"D:20261118092645-05'00'")
    PP.normalize_ooxml(os.path.join(gold, K.DELIVERABLES[1]), "Research and Evaluation", "Research and Evaluation",
                       "2026-11-12T16:40:22Z", "2026-11-18T14:21:07Z", excel=True)
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
