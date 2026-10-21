"""Build task272: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second build into a scratch folder inside
the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task272/generator/build.py              everything
    python3 task272/generator/build.py --out DIR    the pack only, into DIR
    python3 task272/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import hashlib       # noqa: E402
import json          # noqa: E402
import pickle        # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402
import warnings      # noqa: E402

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as DC          # noqa: E402
import ops as O            # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
MTIME = calendar.timegm(K.ASSEMBLED.timetuple())
CACHE = os.path.join(__import__("tempfile").gettempdir(), "task272_world_cache")

CONTENTS = [
    ("criteria", "Vellacott Health Foundation, Program Committee: Decision Coaching Grants FY2027, criteria (approved "
                 "8 December 2026)."),
    ("guide", "Fair Assistance Collaborative: data guide to the 2024 and 2025 extracts."),
    ("puget", "Financial-assistance applications and determinations, 2024 and 2025: the Puget hub's extract."),
    ("willamette", "Financial-assistance applications and determinations, 2024 and 2025: the Willamette hub's extract."),
    ("columbia", "Financial-assistance applications and determinations, 2024 and 2025: the Columbia hub's extract."),
    ("crosswalk", "Lundgren Regional Hospital (H23): counsellor user IDs and guarantor numbers before and after the "
                  "June 2025 billing conversion."),
    ("hospitals", "The collaborative's member hospitals, 2025."),
    ("ledger", "Financial-assistance adjustments posted from 1 January 2025 through 31 March 2026."),
    ("accounts", "Patient accounts those adjustments post to."),
    ("survey", "Patient-experience survey, 2025: would-recommend top-box rates by payer group."),
    ("state", "Charity care as filed with the states, fiscal year 2025."),
]


def make_world(seed=W.SEED):
    """The world and its operations, cached in the system temp folder keyed by the generator's own source."""
    key = hashlib.sha256(b"".join(open(os.path.join(HERE, f), "rb").read()
                                  for f in ("common.py", "models.py", "world.py", "ops.py")) + str(seed).encode()).hexdigest()[:16]
    path = os.path.join(CACHE, "world_%s.pkl" % key)
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))
    hs = W.world(seed)
    doc = W.tune(hs)
    W.decide(hs, doc)
    op = O.build(hs, seed)
    os.makedirs(CACHE, exist_ok=True)
    pickle.dump((hs, op), open(path, "wb"))
    return hs, op


def build(out, seed=W.SEED, keep=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    hs, op = make_world(seed)
    n = {}
    n["puget"] = R.write_puget(p("puget"), op["rows"])
    n["willamette"] = R.write_willamette(p("willamette"), op["rows"])
    n["columbia"] = R.write_columbia(p("columbia"), op["rows"])
    n["crosswalk"] = R.write_crosswalk(p("crosswalk"), op["crosswalk"], op["guarantor_crosswalk"])
    n["hospitals"] = R.write_hospitals(p("hospitals"), hs, seed)
    n["ledger"] = R.write_ledger(p("ledger"), op["ledger"])
    n["accounts"] = R.write_accounts(p("accounts"), op["accounts"], op["ledger"])
    n["survey"] = R.write_survey(p("survey"), seed)
    n["state"] = R.write_state(p("state"), op["ledger"], seed)
    DC.write_criteria(p("criteria"))
    DC.write_guide(p("guide"), n)
    DC.write_contents(p("contents"), [(K.FILES[k], d) for k, d in CONTENTS])
    return dict(hs=hs if keep else None, op=op if keep else None, counts=n)


DOC_DATES = {
    "criteria": ("D:20261208154000-08'00'", "D:20261209101500-08'00'"),
    "guide": ("D:20260414092000-07'00'", "D:20260414161000-07'00'"),
}
OOXML = {
    "crosswalk": ("Puget Hub Billing Conversion", "Puget Hub Billing Conversion", "2025-05-21T17:05:00Z",
                  "2025-06-03T15:42:00Z", "H23 ID crosswalk"),
    "hospitals": ("Fair Assistance Collaborative", "Fair Assistance Collaborative", "2023-01-09T18:30:00Z",
                  "2026-04-10T20:12:00Z", "Member hospitals 2025"),
    "state": ("Vellacott Health Foundation", "Vellacott Health Foundation", "2026-02-02T19:10:00Z",
              "2026-04-13T16:55:00Z", "State charity care filings FY2025"),
}


def finish(out):
    """The containers as their writers save them, then every file's modified time set to the pack's assembly."""
    import postprocess as PP
    for k, (c, m) in DOC_DATES.items():
        PP.normalize_pdf(os.path.join(out, K.FILES[k]), c.encode(), m.encode())
    PP.COMPANY = K.FOUNDATION
    for k, (cr, lb, c, m, title) in OOXML.items():
        PP.normalize_ooxml(os.path.join(out, K.FILES[k]), cr, lb, c, m, title=title, excel=True)
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))


def finish_golden(golden):
    import postprocess as PP
    PP.COMPANY = K.FOUNDATION
    PP.normalize_ooxml(os.path.join(golden, K.DELIVERABLES[0]), K.PEOPLE["requester"], K.PEOPLE["requester"],
                       "2027-01-27T16:02:00Z", "2027-02-02T21:47:00Z", title="Decision Coaching Grants FY2027",
                       excel=True)
    for f in os.listdir(golden):
        os.utime(os.path.join(golden, f), (MTIME, MTIME))


def metadata(fig, counts):
    return {
        "task": "task272",
        "title": "%s: how many FY2027 Decision Coaching Grants" % K.FOUNDATION,
        "domain": "Sociology & Demography (income and poverty measurement)",
        "objective": "Descriptive & Distribution Analysis",
        "distractors": [K.FILES["survey"], K.FILES["state"]],
        "provenance": {name: {"source": "constructed by the task generator (seeded); %s, the %s, its member "
                                        "hospitals, counsellors, patients, applications and accounts are fictional; "
                                        "place names and the federal holiday calendar follow public usage"
                                        % (K.FOUNDATION, K.COLLAB),
                              "date": "2027-01-26", "licence": "CC0 1.0 (constructed for this task)"}
                       for name in sorted(K.FILES.values())},
        "rows": {K.FILES[k]: v for k, v in counts.items()},
        "answer": "%d grants: %s" % (fig["call"]["count"], ", ".join(fig["call"]["qualify"])),
    }


def main_build(target, golden, seed=W.SEED):
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
    ap.add_argument("--seed", type=int, default=W.SEED)
    a = ap.parse_args()
    if a.out:
        build(a.out, a.seed)
        finish(a.out)
        sys.exit(0)
    target, golden = os.path.join(TASK, "target"), os.path.join(TASK, "golden")
    b, fig, res = main_build(target, golden, a.seed)
    print("pack:", b["counts"])
    print("call:", fig["call"]["count"], fig["call"]["qualify"])
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
