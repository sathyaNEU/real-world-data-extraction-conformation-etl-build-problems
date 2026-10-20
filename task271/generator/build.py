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

import numpy as np   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK          # noqa: E402
import common as K         # noqa: E402
import core as C           # noqa: E402
import docs as DC          # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())

CONTENTS = [
    ("criteria", "Community Engagement Support track 2027: criteria for the regions (Programs and Quality Committee, "
                 "16 September 2026)."),
    ("guide", "Analytics and Reporting: data guide for the 2027 Community Engagement Support figures."),
    ("methods", "Kestrelby Survey Research: 2026 Member Work and Income Survey, methods report (30 June 2026)."),
    ("sample", "MWIS 2026 sample file (Kestrelby sample management system)."),
    ("dialer", "Kestrelby dialer export, MWIS project, all calls to 29 May 2026."),
    ("crm", "Member Services Center CRM export: activity on the MWIS sample, 13 April to 29 May 2026."),
    ("interviews", "MWIS 2026 interview file (Kestrelby)."),
    ("regions", "Apple Health regions and their counties."),
    ("roster", "Expansion adult roster, active members, exported 19 October 2026."),
    ("changes", "Enrollment change log, 1 to 19 October 2026."),
    ("cases", "HCA household composition extract, 15 October 2026."),
    ("pilot", "Kestrelby: MWIS pilot memo (27 February 2026)."),
    ("cahps", "CAHPS 2025 adult Medicaid results by region (Quality Improvement)."),
]


def frame_counts(A, seed):
    """Each region's members on 1 March 2026: the October files' members enrolled then, aged 19 to 64, and the
    members who left the plan between March and October (about one in seven)."""
    r = np.random.default_rng(seed + 111)
    n = {c: 0 for c in K.CODES}
    for m in A["members"] + A["retro"]:
        if m["begin"] <= K.FRAME_DATE and 19 <= AK.age_on(m["born"], K.FRAME_DATE) <= 64:
            n[AK.REGION_OF[m["county1"]]] += 1
    return {c: int(round(n[c] / r.uniform(0.85, 0.87))) for c in K.CODES}


def fieldwork(w):
    out = {c: dict(msc=0, passed=0, complete=0, declined=0, noncontact=0) for c in K.CODES}
    centres = {}
    for row in w["calls"]:
        centres.setdefault(int(row[0]), set()).add(int(row[2]))
    for c in w["cases"]:
        f = out[K.CODES[int(c[1])]]
        cid = int(c[0])
        if int(c[8]):
            f["msc"] += 1
            if 1 in centres[cid]:
                f["passed"] += 1
        f[{1: "complete", 2: "declined", 0: "noncontact"}[int(c[5])]] += 1
    return out


def build(out, seed=C.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    w = W.world(seed)
    A = AK.build(C.ASK_SEED)
    H = AK.households(A, C.ASK_SEED)
    linked = AK.link_sample(w, A, C.ASK_SEED)
    rows = R.call_rows(w)
    n = {}
    n["sample"] = R.write_sample(p("sample"), w)
    n["dialer"] = R.write_dialer(p("dialer"), w, rows, seed)
    n["crm"] = R.write_crm(p("crm"), w, rows, seed)
    n["interviews"] = R.write_interviews(p("interviews"), w, rows)
    n["regions"] = R.write_regions(p("regions"))
    n["cahps"] = R.write_cahps(p("cahps"), seed)
    n["roster"] = AK.write_roster(p("roster"), A)
    n["changes"] = AK.write_changes(p("changes"), A, C.ASK_SEED)
    n["cases"] = AK.write_households(p("cases"), H)
    DC.write_criteria(p("criteria"))
    DC.write_methods(p("methods"), fieldwork(w), frame_counts(A, seed))
    DC.write_pilot(p("pilot"))
    DC.write_guide(p("guide"))
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(w=w if keep else None, A=A if keep else None, H=H if keep else None, counts=n, linked=linked)


DOC_DATES = {
    "criteria": ("D:20260916171500-07'00'", "D:20260917090500-07'00'"),
    "guide": ("D:20261020101000-07'00'", "D:20261020143000-07'00'"),
    "methods": ("D:20260629161000-05'00'", "D:20260630112000-05'00'"),
    "pilot": ("D:20260226153000-05'00'", "D:20260227094500-05'00'"),
}
OOXML = {
    "crm": ("Trevanna CRM Reporting", "Trevanna CRM Reporting", "2026-10-20T16:02:00Z", "2026-10-20T16:02:00Z",
            "MWIS activity export", K.PLAN),
    "regions": ("Trevanna Analytics", "Trevanna Analytics", "2024-02-05T18:20:00Z", "2026-01-12T22:41:00Z",
                "Apple Health regions", K.PLAN),
    "cahps": ("Trevanna Quality Improvement", "Trevanna Quality Improvement", "2025-08-11T20:15:00Z",
              "2025-08-14T15:52:00Z", "CAHPS 2025 regions", K.PLAN),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in DOC_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    for k, (cr, lb, c, m, title, company) in OOXML.items():
        PP.COMPANY = company
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=True)
    PP.COMPANY = K.PLAN
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.PLAN
    PP.normalize_ooxml(os.path.join(golden, K.DELIVERABLES[0]), K.PEOPLE["requester"], K.PEOPLE["requester"],
                       "2026-10-21T16:02:00Z", "2026-10-23T22:47:00Z", title="Community Engagement Support regions 2027",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    return {
        "task": "task271",
        "title": "%s: the four regions for the 2027 %s" % (K.PLAN, K.TRACK),
        "domain": "Survey Research & Official Statistics (nonresponse, calibration and measurement error adjustment)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["pilot"], K.FILES["cahps"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); %s, %s, every member, case and "
                                        "person are fictional; the Apple Health regions and their counties are "
                                        "Washington's" % (K.PLAN, K.VENDOR),
                              "date": "2026-10-20", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "Regions for 2027: %s" % ", ".join(fig["call"]["regions"]),
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
    h = {}
    for f in sorted(os.listdir(folder)):
        h[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return h


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
