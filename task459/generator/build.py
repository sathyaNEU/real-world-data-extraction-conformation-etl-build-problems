"""Build task459 end to end: the pack twice (asserted byte-identical), then target/, golden/, submission.md,
generator/figures.json, metadata.json and target.zip.

    python3 build.py            full build
    python3 build.py --pack DIR write one pack into DIR (used by the full build, one process per pack)
"""
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

AS_OF = "2026-10-16"


def pack_into(out):
    import pack as P
    import sim as S
    import world as W
    os.makedirs(out, exist_ok=True)
    assert not os.listdir(out), "pack directory must be empty"
    wd = W.build_world()
    P.prepare(wd)
    svcs, fills, visits = S.simulate(wd)
    counts = P.write_pack(out, wd, svcs, fills, visits)
    with open(os.path.join(out, "..", os.path.basename(out) + "_counts.json"), "w") as f:
        json.dump(counts, f)


def digest(d):
    h = hashlib.sha256()
    for name in sorted(os.listdir(d)):
        h.update(name.encode())
        h.update(open(os.path.join(d, name), "rb").read())
    return h.hexdigest()


def metadata(counts):
    import pack as P
    src = {
        "schedule": "Pinyon Valley Health Plan, Senior Choice 2027 In-Home Support Agreement, Schedule B (approved 22 September 2026)",
        "members": "Pinyon Valley Health Plan enrollment system, Senior Choice member extract, year-end snapshot of 2 January 2026",
        "addr": "Pinyon Valley Health Plan enrollment system, member address history, snapshot of 2 January 2026",
        "enroll": "Pinyon Valley Health Plan enrollment system, enrollment spans, snapshot of 2 January 2026",
        "medical": "Pinyon Valley Health Plan claims system, medical claim lines for 2025 dates of service paid through 30 June 2026",
        "pbm": "the plan's pharmacy benefit manager, pharmacy claims file for 2025 fills (pipe-delimited)",
        "visits": "in-home support agencies' claims to the plan for 2025 dates of service",
        "directory": "Pinyon Valley Health Plan provider data management, provider directory extract of 1 October 2026",
        "moves": "Pinyon Valley Health Plan provider data management, practice location change log for 2025",
        "pharmacies": "the plan's pharmacy network listing for 2025",
        "population": "county population estimates, Arizona residents aged 75 and over by county, 1 July 2025",
        "adequacy": "Pinyon Valley Health Plan network management, network adequacy review for the fourth quarter of 2025",
    }
    notes = {
        "population": "county population aged 75 and over; relevant to a regional budget, unused by the solution",
        "adequacy": "time and distance standards and results by county; relevant to the regional network, unused by the solution",
    }
    files = {}
    for k, name in P.FILES.items():
        files[name] = {"date": P.STAMPS[k].strftime("%Y-%m-%d"), "license": "synthetic, CC0",
                       "role": "distractor" if k in P.DISTRACTORS else "evidence", "source": src[k] + "; synthetic",
                       "rows": counts.get(k)}
        if files[name]["rows"] is None:
            del files[name]["rows"]
    return {
        "architecture": 2,
        "as_of": AS_OF,
        "decision": "how Pinyon Valley Health Plan's 2027 in-home support budget is divided among its regional agencies "
                    "under Schedule B of the 2027 agreement, with the 2025 use of members aged 65 to 74",
        "deliverables": ["member_regions_2025.csv", "home_care_allocation_2027.pdf"],
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "distractor_notes": {P.FILES[k]: notes[k] for k in P.DISTRACTORS},
        "files": files,
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "Healthcare Delivery & Health Economics, payment, claims and health plan analytics",
    }


def zip_target(target, path):
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + name, date_time=(2026, 10, 16, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, name), "rb").read())
    os.replace(tmp, path)


def full():
    work = tempfile.mkdtemp(prefix="t459_")
    try:
        a, b = os.path.join(work, "a"), os.path.join(work, "b")
        for d in (a, b):
            subprocess.run([sys.executable, os.path.abspath(__file__), "--pack", d], check=True, cwd=HERE)
        names_a, names_b = sorted(os.listdir(a)), sorted(os.listdir(b))
        assert names_a == names_b, "the two builds wrote different file sets"
        for n in names_a:
            assert filecmp.cmp(os.path.join(a, n), os.path.join(b, n), shallow=False), "not byte-identical: " + n
        da, db = digest(a), digest(b)
        assert da == db
        print("two builds byte-identical:", da[:16])
        counts = json.load(open(os.path.join(work, "a_counts.json")))
        target = os.path.join(TASK, "target")
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(a, target, copy_function=shutil.copy2)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    import golden as G
    import writeup as WU
    gold = os.path.join(TASK, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    res = G.write_goldens(target, gold)
    # the goldens rebuild byte-identically too
    chk = tempfile.mkdtemp(prefix="t459g_")
    try:
        G.write_goldens(target, chk)
        for n in sorted(os.listdir(gold)):
            assert filecmp.cmp(os.path.join(gold, n), os.path.join(chk, n), shallow=False), "golden not byte-identical: " + n
    finally:
        shutil.rmtree(chk, ignore_errors=True)
    WU.write(res, os.path.join(TASK, "submission.md"), os.path.join(HERE, "figures.json"))
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(counts), f, indent=1, sort_keys=True)
        f.write("\n")
    zpath = os.path.join(TASK, "target.zip")
    zip_target(target, zpath)
    z1 = hashlib.md5(open(zpath, "rb").read()).hexdigest()
    zip_target(target, zpath)
    z2 = hashlib.md5(open(zpath, "rb").read()).hexdigest()
    assert z1 == z2
    print("target.zip md5", z1)
    print("allocations", res["alloc"])
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--pack":
        pack_into(sys.argv[2])
        sys.exit(0)
    sys.exit(full())
