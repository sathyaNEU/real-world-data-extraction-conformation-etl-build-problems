"""Build task261: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task261/generator/build.py              everything
    python3 task261/generator/build.py --out DIR    the pack only, into DIR
    python3 task261/generator/build.py --golden     the pack and the goldens, no checks"""
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
import insurer as I        # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
DISTRACTORS = (K.BULLETIN, K.RESEARCH)
CALL_FILES = (K.SUMMARY, K.PERSONS, K.REPW, K.GUIDE, K.BRIEF)
ASK_FILES = (K.CRM, K.RIA, K.NOMS, K.ANN, K.DICT, K.PDS, K.FACTS)


def world():
    d = W.survey()
    B = I.build()
    I.events(B)
    I.new_business(B)
    I.register(B)
    return dict(d=d, B=B)


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda f: os.path.join(out, f)
    S = world()
    d, B = S["d"], S["B"]
    counts = {K.SUMMARY: R.write_summary(p(K.SUMMARY), d), K.PERSONS: R.write_persons(p(K.PERSONS), d),
              K.REPW: R.write_repweights(p(K.REPW), d), K.CRM: R.write_crm(p(K.CRM), B), K.RIA: R.write_ria(p(K.RIA), B),
              K.NOMS: R.write_nominations(p(K.NOMS), B), K.ANN: R.write_annuities(p(K.ANN), B)}
    fig = D.bulletin_figures(d)
    D.write_user_guide(p(K.GUIDE), d, fig)
    D.write_bulletin(p(K.BULLETIN), d, fig)
    D.write_brief(p(K.BRIEF))
    D.write_pds(p(K.PDS))
    D.write_key_facts(p(K.FACTS))
    D.write_dictionary(p(K.DICT))
    D.write_research(p(K.RESEARCH))
    PP.COMPANY = K.CENTRE
    PP.normalize_ooxml(p(K.BULLETIN), K.CENTRE, K.CENTRE, "2026-09-08T03:12:44Z", "2026-09-14T00:31:09Z", excel=True)
    PP.COMPANY = K.INSURER
    PP.normalize_ooxml(p(K.DICT), "Insights and Analytics", "Insights and Analytics", "2025-03-04T22:41:16Z",
                       "2027-01-12T05:08:51Z", excel=True)
    PP.normalize_ooxml(p(K.BRIEF), K.PEOPLE["head"], K.PEOPLE["head"], "2027-01-12T23:05:00Z", "2027-01-13T02:47:00Z")
    PP.normalize_pdf(p(K.GUIDE), b"D:20260911161408+10'00'", b"D:20260914093015+10'00'")
    PP.normalize_pdf(p(K.PDS), b"D:20260616112035+10'00'", b"D:20260616112035+10'00'")
    PP.normalize_pdf(p(K.FACTS), b"D:20261027150322+11'00'", b"D:20261027150322+11'00'")
    PP.normalize_pdf(p(K.RESEARCH), b"D:20260909104517+10'00'", b"D:20260909104517+10'00'")
    stamp = dt.datetime(2027, 1, 13, 16, 40, tzinfo=dt.timezone(dt.timedelta(hours=11))).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return dict(counts=counts, S=S, fig=fig)


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 1, 13, 16, 41, 2)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def write_metadata(path):
    meta = {"task": "task261", "distractor_files": list(DISTRACTORS),
            "wrong_basis_distractor": {"file": K.BULLETIN,
                                       "basis": "median household net worth by the age of the household reference "
                                                "person, not by the older of the reference person and partner",
                                       "ruled_out_by": "%s: a household is placed by the age of the older of its "
                                                       "reference person and partner" % K.BRIEF},
            "deliverables": list(K.DELIVERABLES), "call_files": list(CALL_FILES), "ask_files": list(ASK_FILES),
            "provenance": "Constructed records (declared): the public-use release of the fictional National Household "
                          "Wealth Survey 2025 (household summary extract, person file, replicate weights, user guide, "
                          "results bulletin) and the fictional Kelvane Life's client register, pension and nomination "
                          "extracts, annuity valuation listing, data dictionary, PDS, key facts sheet, customer research "
                          "summary and brief, all generated by task261/generator from a simulated survey and a simulated "
                          "retirement book; no third-party data; every organisation and person is invented."}
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
    PP.COMPANY = K.INSURER
    PP.normalize_ooxml(os.path.join(gold, K.DELIVERABLES[0]), "Insights and Analytics", "Insights and Analytics",
                       "2027-01-15T22:12:31Z", "2027-01-20T05:44:02Z")
    PP.normalize_ooxml(os.path.join(gold, K.DELIVERABLES[1]), "Insights and Analytics", "Insights and Analytics",
                       "2027-01-14T23:02:47Z", "2027-01-20T05:39:18Z", excel=True)
    PP.normalize_svg(os.path.join(gold, K.DELIVERABLES[2]))
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
