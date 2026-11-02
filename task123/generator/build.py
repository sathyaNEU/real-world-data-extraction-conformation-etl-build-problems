"""Builds the pack twice, asserts byte-identical output, runs every check, and installs target/, golden/,
generator/figures.json, submission.md, metadata.json and target.zip."""
import hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile

GEN = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(GEN)
REPO = os.path.dirname(TASK_DIR)
sys.path.insert(0, GEN)
import world, pack, analysis, checks, golden, writeup  # noqa: E402

SCRUB = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
ASOF = "2026-11-20"
PRODUCERS = {
    pack.MSB_NAME: ("Brennand Electrical", "2019-11-18", "2019-01-01"),
    pack.STD_NAME: ("OC1 Tannery Quay", "2026-10-14", "2025-01-01"),
    pack.THERMAL_NAME: ("Ferrier Thermal Services", "2025-06-24", "2025-01-01"),
    pack.REG_NAME: ("Quaylight Energy Services", "2026-10-31", "2025-01-01"),
    pack.LOTS_NAME: ("OC1 manager", "2026-09-30", "2025-01-01"),
    pack.REMARK_NAME: ("OC1 manager", "2025-03-10", "2025-01-01"),
    pack.APPS_NAME: ("OC1 manager", "2026-10-31", "2025-01-01"),
    pack.WORKS_NAME: ("Tannery Quay facilities", "2026-11-06", "2025-01-01"),
    pack.COMMON_NAME: ("Tannery Quay facilities", "2026-08-06", "2025-01-01"),
}
GOLDEN_PRODUCERS = {"riser_capacity_2027.xlsx": ("Kayla Hunt", "2026-11-20", "2025-01-01")}


def scrub(directory, table):
    for name, (prod, stamp, floor) in table.items():
        src = os.path.join(directory, name)
        if not os.path.exists(src):
            continue
        tmp = tempfile.mkdtemp()
        shutil.copy(src, os.path.join(tmp, name))
        r = subprocess.run([sys.executable, SCRUB, tmp, "--apply", "--producer", prod, "--stamp", stamp,
                            "--floor", floor, "--ceiling", ASOF], capture_output=True, text=True)
        if r.returncode != 0 or "LEFT AS WAS" in r.stdout:
            raise SystemExit("scrub failed on %s:\n%s\n%s" % (name, r.stdout, r.stderr))
        shutil.copy(os.path.join(tmp, name), src)
        shutil.rmtree(tmp)


def metadata(path):
    files = {
        pack.NEM12_NAME: "the embedded network operator's NEM12 interval export for the child meters, July 2026, extracted 2 August 2026",
        pack.PQ_NAME: "the embedded network operator's hourly power-quality export (average, minimum and maximum voltage per meter and element), 12 to 20 July 2026 UTC",
        pack.EVENTS_NAME: "the head-end's power-quality event log for July 2026, generated 4 August 2026",
        pack.READS_NAME: "register reads at the start of July and of August 2026",
        pack.EXCH_NAME: "meter exchange log for 2026 with final and initial register reads",
        pack.REG_NAME: "child meter register as at 31 October 2026",
        pack.LOTS_NAME: "owners corporation register extract of lots, units and accessory car spaces, 30 September 2026",
        pack.REMARK_NAME: "basement 2 and 3 car space re-marking schedule, March 2025",
        pack.APPS_NAME: "register of charger applications under the 2024 EV charging by-law, as at 31 October 2026",
        pack.WORKS_NAME: "2027 electrification works schedule (approved chargers and cooktop conversions), issued 6 November 2026",
        pack.MSB_NAME: "rising main schedule from the 2019 main switchboard replacement",
        pack.STD_NAME: "the owners corporation's electrification capacity standard, adopted 14 October 2026",
        pack.PARENT_NAME: "the distributor's parent meter NEM12 export, July 2026",
        pack.COMMON_NAME: "house supply sub-meter daily readings, July 2026",
        pack.THERMAL_NAME: "annual thermographic survey of the switchboards, June 2025",
    }
    meta = {
        "task": "task123",
        "decision": "which apartment rising mains need re-phasing or a larger main before the 2027 chargers and cooktop conversions are connected",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "General Statistics & Data Science",
        "deliverables": ["riser_capacity_2027.xlsx", "riser_phase_loading_2027.svg"],
        "setting_as_of": ASOF,
        "distractor_files": ["target/" + d for d in pack.DISTRACTORS],
        "files": {("target/" + k): {"source": "constructed for this task (synthetic, in the layout of the producing system)",
                                    "covers": v, "licence": "CC BY 4.0 (constructed data)", "date": ASOF}
                  for k, v in files.items()},
        "people": "fictional, drawn with guard.py names",
    }
    with open(path, "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)


def build_once(root):
    W = world.build_all()
    tgt = os.path.join(root, "target")
    pack.write_pack(W, tgt)
    scrub(tgt, PRODUCERS)
    E = analysis.everything(tgt)
    res = checks.run(W, tgt, E)
    gold = os.path.join(root, "golden")
    golden.write(E, gold)
    scrub(gold, GOLDEN_PRODUCERS)
    F = writeup.figures(E)
    with open(os.path.join(root, "figures.json"), "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    writeup.submission(F, os.path.join(root, "submission.md"))
    metadata(os.path.join(root, "metadata.json"))
    return res, F


def digest(root):
    h = {}
    for dp, dn, fn in os.walk(root):
        for n in sorted(fn):
            p = os.path.join(dp, n)
            h[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    res, F = build_once(a)
    build_once(b)
    da, db = digest(a), digest(b)
    diff = [k for k in da if da.get(k) != db.get(k)] + [k for k in db if k not in da]
    for label, okv, detail in res:
        print(("PASS  " if okv else "FAIL  ") + label + ((" (" + detail + ")") if detail else ""))
    fails = [l for l, o, d in res if not o]
    print("\n%d checks, %d failed" % (len(res), len(fails)))
    print("byte-identical rebuild: %s" % ("yes" if not diff else "NO: " + ", ".join(diff)))
    if fails or diff:
        sys.exit(1)
    for sub in ("target", "golden"):
        dst = os.path.join(TASK_DIR, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "figures.json"), os.path.join(GEN, "figures.json"))
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK_DIR, "submission.md"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK_DIR, "metadata.json"))
    zpath = os.path.join(TASK_DIR, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(os.path.join(TASK_DIR, "target"))):
            zi = zipfile.ZipInfo("target/" + n, date_time=(2026, 11, 20, 6, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TASK_DIR, "target", n), "rb").read())
    print("target.zip sha256 %s" % hashlib.sha256(open(zpath, "rb").read()).hexdigest()[:16])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
