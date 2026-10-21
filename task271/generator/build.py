"""Build task271: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task271/generator/build.py              everything
    python3 task271/generator/build.py --out DIR    the pack only, into DIR
    python3 task271/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clinical as CL      # noqa: E402
import common as K         # noqa: E402
import core as C           # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("criteria", "Clinical Programs Committee: Family Outreach Program, criteria for the variant groups, 2027 "
                 "(approved 24 September 2026)."),
    ("guide", "Inherited Cancer Risk Service: data guide to the registry extracts."),
    ("pedigree", "Register pedigree export, every family, cut 30 September 2026."),
    ("labs", "Genetic test results for people on the register, January 2016 to September 2026."),
    ("groups", "The service's variant register: the ten groups and their variants."),
    ("incidence", "Tumor registry: first primary breast cancers and female patient-years by age, 2016 to 2025."),
    ("abstracts", "Tumor registry: breast cancer abstracts for patients on the register, 2016 to 2026."),
    ("surgery", "Surgical procedures on the breast for patients on the register, March 2019 to September 2026."),
    ("imaging", "Breast MRI orders for patients on the register, January 2024 to September 2026."),
    ("empi", "EMPI: hospital record numbers and enterprise IDs for patients on the register."),
    ("merges", "EMPI merge log for patients on the register."),
    ("deaths", "Death linkage for patients on the register, to 30 September 2026."),
    ("capacity", "High-Risk Breast Clinic: breast MRI capacity by hospital, 2026 and the 2027 plan."),
    ("prs", "ICRS polygenic score pilot, 2025: results for the carriers enrolled."),
]


def build(out, seed=C.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.world(seed)
    rec = CL.build(w)
    rec = CL.ensure_contralateral(w, rec, R.positives(w))
    el = CL.eligible(w, rec, R.positives(w))
    rec = CL.imaging(w, rec, el)
    n = {}
    n["pedigree"] = R.write_pedigree(p("pedigree"), w, rec, seed)
    n["labs"] = R.write_labs(p("labs"), w, rec, seed)
    n["groups"] = R.write_register(p("groups"), w)
    n["incidence"] = R.write_incidence(p("incidence"), seed)
    n["abstracts"] = R.write_abstracts(p("abstracts"), w, rec, seed)
    n["surgery"] = R.write_procedures(p("surgery"), w, rec, seed)
    n["imaging"] = R.write_exams(p("imaging"), w, rec, seed)
    n["empi"] = R.write_empi(p("empi"), w, rec, seed)
    n["merges"] = R.write_merges(p("merges"), w, rec, seed)
    n["deaths"] = R.write_deaths(p("deaths"), w, rec, seed)
    n["capacity"] = R.write_capacity(p("capacity"), seed)
    n["prs"] = R.write_prs(p("prs"), w, rec, seed)
    DC.write_criteria(p("criteria"))
    DC.write_guide(p("guide"), n)
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w if keep else None, rec=rec if keep else None, el=el if keep else None, counts=n)


DOC_DATES = {
    "criteria": ("D:20260924160500-06'00'", "D:20260925091200-06'00'"),
    "guide": ("D:20261022101500-06'00'", "D:20261022142000-06'00'"),
}
OOXML = {
    "groups": ("ICRS Registry", "ICRS Registry", "2021-03-08T17:20:00Z", "2026-10-01T15:41:00Z",
               "ICRS variant register"),
    "capacity": ("Ellisford Imaging Services", "Ellisford Imaging Services", "2026-06-02T16:10:00Z",
                 "2026-09-18T21:33:00Z", "High-Risk Breast Clinic MRI capacity"),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in DOC_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.SYSTEM
    for k, (cr, lb, c, m, title) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=True)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.SYSTEM
    PP.normalize_ooxml(os.path.join(golden, K.DELIVERABLES[0]), K.PEOPLE["requester"], K.PEOPLE["requester"],
                       "2026-10-23T16:02:00Z", "2026-10-27T21:47:00Z", title="Family Outreach Program groups 2027",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    return {
        "task": "task271",
        "title": "%s: the variant groups for the 2027 %s" % (K.SYSTEM, K.PROGRAM),
        "domain": "Biomedical & Clinical Research (statistical genomics)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["capacity"], K.FILES["prs"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); %s, its hospitals' patients, every "
                                        "family, person and variant record are fictional; gene names, HGVS conventions "
                                        "and CPT codes follow public usage" % K.SYSTEM,
                              "date": "2026-10-22", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Groups for 2027: %s" % ", ".join(fig["call"]["qualify"]),
    }


def main_build(target, golden, seed=C.SEED):
    import deliver as DV
    b = build(target, seed, keep=True)
    finish(target)
    fig, res = DV.write(target, golden)
    finish_golden(golden)
    DV.write_figures(os.path.join(HERE, "figures.json"), fig)
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(fig, b["counts"]), f, indent=1, sort_keys=True)
        f.write("\n")
    return b, fig, res


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(target, path):
    import zipfile
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=K.ASSEMBLED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    ap.add_argument("--seed", type=int, default=C.SEED)
    a = ap.parse_args()
    if a.out:
        build(a.out, a.seed)
        finish(a.out)
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden, a.seed)
    print("pack:", b["counts"])
    print("call:", fig["call"])
    if a.golden:
        sys.exit(0)
    import checks
    import verify
    rc = checks.run(TASK, b, fig, res)
    rv = verify.run(TASK)
    scratch = os.path.join(TASK, "_rebuild_check")
    build(os.path.join(scratch, "target"), a.seed)
    finish(os.path.join(scratch, "target"))
    import deliver as DV
    DV.write(os.path.join(scratch, "target"), os.path.join(scratch, "golden"))
    finish_golden(os.path.join(scratch, "golden"))
    d1, d2 = digest(target), digest(os.path.join(scratch, "target"))
    g1, g2 = digest(golden), digest(os.path.join(scratch, "golden"))
    same = d1 == d2 and g1 == g2
    for f in sorted(set(d1) | set(g1)):
        if d1.get(f, g1.get(f)) != d2.get(f, g2.get(f)):
            print("  differs on rebuild:", f)
    shutil.rmtree(scratch)
    print("second build byte-identical:", same)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    print("target.zip:", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())
    sys.exit(0 if (rc == 0 and rv == 0 and same) else 1)
