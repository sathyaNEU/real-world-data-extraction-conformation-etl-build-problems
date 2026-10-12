"""Build the pack, the golden page, figures.json, submission.md and metadata.json; run every check and the
independent verifier; build a second time into a scratch folder and require byte-identical output; cut
target.zip.

    python3 task229/generator/make.py
"""
import filecmp
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import checks as C
import estimate as E
import asks as A
import golden as G
import verify as V
import world as W

TASK = B.TASK
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

SOURCES = {
    "counts": "Corderoy WMS count history for Thornacre pick faces, all eight centres, 1 June to 7 December 2026",
    "locations": "Corderoy WMS location master, Thornacre client, effective-dated",
    "centres": "Corderoy centre register with Thornacre depot codes",
    "snapshot": "Corderoy WMS stock by location at 06:00 on 7 December 2026",
    "batches": "Corderoy WMS batch register at 06:00 on 7 December 2026",
    "linemaster": "Thornacre line master export with case-size history",
    "costbase": "Thornacre cost price list extracted 28 November 2026",
    "costp10": "Thornacre period 10 cost change file",
    "forecast": "Thornacre store replenishment forecast, run of 23 November 2026",
    "servicing": "Thornacre store-to-depot servicing map with validity dates",
    "calendar": "Thornacre store trading calendar, Christmas and New Year 2026/27",
    "stores": "Thornacre store list from the estate service",
    "categories": "Thornacre forecast category table",
    "labour": "Corderoy peak labour plan, agency hours and headcount",
    "goodsin": "Corderoy goods-in booking summary over the freeze",
    "standard": "Thornacre SCS-07 peak stock-record standard, version 3",
    "programme": "Corderoy CP-THN-04 perpetual count programme, version 7",
    "notes": "Corderoy BI extract notes for the pull of 7 December 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        return sum(1 for _ in open(path, encoding="utf-8")) - 1
    if path.endswith(".json"):
        return len(json.load(open(path))["stores"])
    return None


def metadata():
    files = []
    for k, f in B.ALL_FILES.items():
        p = os.path.join(TARGET, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-12-07",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task229",
        "title": "Which distribution centres meet the client's peak stock-record standard at the freeze stand-down",
        "domain": "General Statistics & Data Science",
        "subdomain": "missing-data-censoring-measurement-error",
        "setting": "a third-party logistics operator's peak gate on its pick-face stock records for a grocery client",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10 (scorecard against thresholds): eight centres, each with record accuracy against the line and a verdict, plus the stock value on the gate's faces and the forecast cases over the freeze, charted",
        "as_of": "2026-12-07",
        "deliverables": [G.GOLDEN_FILE],
        "distractor_files": [A.FILES[k] for k in A.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task229/generator/make.py (seeded, deterministic) around a "
                               "fictional 3PL (Corderoy Logistics) and a fictional grocer (Thornacre); real UK place names "
                               "and postcode districts; no real company, store, product or person is depicted.",
                     "date": "2026-12-07", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task229/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 12, 7, 7, 20, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp, hashlib.sha256(open(zp, "rb").read()).hexdigest()


def deliver(target, golden):
    est = E.everything(target)
    ga, gb = A.ask_a(target), A.ask_b(target)
    return G.main(target, golden, est, ga, gb, sum(est[n]["in_scope_faces"] for n in W.NAMES))


def main():
    world = B.build(TARGET)
    deliver(TARGET, GOLDEN)
    metadata()
    n, _ = C.run(TARGET, world, os.path.join(TASK, "metadata.json"))
    print("checks.py: %d assertions green" % n)
    V.main(TARGET, GOLDEN)
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "target")
    B.build(t2, quiet=True)
    d1, d2 = digest(TARGET), digest(t2)
    bad = [f for f in d1 if d1[f] != d2.get(f)]
    shutil.rmtree(tmp)
    if bad:
        raise SystemExit("second build differs: %s" % bad)
    print("two builds byte-identical (%d target files)" % len(d1))
    zp, sha = cut_zip()
    house_fixes(zp)
    print("zip:", zp, sha)


def house_fixes(zp):
    """reduce-house-fixes H7, H8, H9 and H11, asserted on the final cut."""
    import re
    with zipfile.ZipFile(zp) as z:
        members = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    assert members == digest(TARGET), "H7: target.zip disagrees with target/"
    assert not any("/" in m or m.startswith(".") for m in members), "H7: archive members must sit at the root"
    sub = open(os.path.join(TASK, "submission.md")).read()
    page = open(os.path.join(GOLDEN, G.GOLDEN_FILE)).read()
    for f in set(re.findall(r"[\w-]+\.(?:csv|xlsx|json|pdf|docx|txt)", sub + page)):
        assert f in members, "H8: the write-up or golden cites a file the pack does not carry: %s" % f
    notes = open(os.path.join(TARGET, B.ALL_FILES["notes"])).read()
    listed = {f for f in members if f in notes}
    assert listed == set(members) - {B.ALL_FILES["notes"]}, "H9: the extract notes miss %s" % (set(members) - listed)
    names = [os.path.join(dp, f) for dp, _, fs in os.walk(TASK) for f in fs]
    assert sum(1 for p in names if os.path.basename(p) == "submission.md") == 1, "H11: one submission.md"
    assert sum(1 for p in names if os.path.basename(p) == "prompt.txt") == 1 and not any(
        os.path.basename(p) == "prompt.md" for p in names), "H11: one prompt.txt and no prompt.md"
    print("house fixes H7, H8, H9, H11 green")


if __name__ == "__main__":
    main()
