"""Builds task281 twice from nothing, checks the two builds are byte-identical, and installs target/, golden/,
generator/figures.json, metadata.json, target.zip and submission.md.

    python3 task281/generator/build.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import deliver as GD  # noqa: E402
import make_pack as M  # noqa: E402
import params as P  # noqa: E402

SOURCES = {
    "results": "Kelvory RetinaCheck vendor portal, result export for the network's sites, screenings captured "
               "1 October 2025 to 30 September 2026; synthetic, built for this task",
    "validation": "CVCH Quality department, local validation study record (study CVCH-QI-2025-01); synthetic",
    "protocol": "CVCH Quality department, validation study protocol v1.2; synthetic",
    "assets": "CVCH Biomedical Engineering asset register with location history, exported 30 September 2026; "
              "synthetic",
    "standard": "CVCH Executive Leadership Team, governance standard CAI-03 version 3; synthetic",
    "opspec": "Kelvory Health Systems, RetinaCheck operating points site configuration guide, revision C; synthetic",
    "siteconfig": "Kelvory RetinaCheck portal, site configuration export, 1 October 2026; synthetic",
    "agreement": "Pellam Eye Reading Center, overread services agreement for contract year 2027; synthetic",
    "orders": "CVCH EHR reporting extract, retinal imaging and reading center referral orders, 2025-26; synthetic",
    "directory": "CVCH clinic directory (EHR department, portal site and biomedical location names); synthetic",
    "reads": "Pellam Eye Reading Center case log for the network's 2025-26 referrals; synthetic",
    "registry": "CVCH population health diabetes registry snapshot, 30 September 2026; synthetic",
    "outside": "CVCH Health Information Management, index of outside eye examination reports; synthetic",
    "tickets": "CVCH Biomedical Engineering service tickets, 2025-26; synthetic",
    "dashboard": "Kelvory Customer Success, RetinaCheck site dashboard Q4 2025 to Q3 2026; synthetic",
    "survey": "CVCH patient experience survey, eye screening visits 2026; synthetic",
}


def metadata(n):
    return {
        "task": "task281", "architecture": 3, "as_of": P.ASOF.isoformat(),
        "decision": "the vendor operating point each Corrowan Valley clinic runs Kelvory RetinaCheck at in contract "
                    "year 2027 under the network's clinical AI governance standard",
        "deliverables": [GD.BOOK, GD.BRIEF],
        "files": {P.FILES[k]: {"source": SOURCES[k], "date": P.ASOF.isoformat(), "license": "synthetic, CC0",
                               "role": "distractor" if k in P.DISTRACTORS else "evidence"} for k in P.FILES},
        "distractor_files": [P.FILES[k] for k in P.DISTRACTORS],
        "stated_inputs": ["7,500", "7500", "85"],
        "distractor_notes": {
            P.FILES["dashboard"]: "the vendor's referral and ungradable rates by site and quarter at the Standard "
                                  "point; relevant to the reading center load, unused by the solution",
            P.FILES["survey"]: "patient experience scores for eye screening visits; relevant to the service, "
                               "unused by the solution",
            P.FILES["outside"]: "outside eye examination reports indexed by HIM; relevant to the screening program, "
                                "unused by the solution",
        },
        "largest_file": {"name": P.FILES["results"], "rows": n["results"]},
        "row_counts": {P.FILES[k]: v for k, v in sorted(n.items()) if k in P.FILES},
    }


def digest(folder):
    h = {}
    for root, _d, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = (os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen"))
    w, n = M.build(target)
    GD.write_all(target, golden, gen)
    with open(os.path.join(base, "metadata.json"), "w") as fh:
        json.dump(metadata(n), fh, indent=1, sort_keys=True)
        fh.write("\n")
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=GD.STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, fn), "rb").read())


def main():
    a, b = tempfile.mkdtemp(), tempfile.mkdtemp()
    da, db = one_build(a), one_build(b)
    if da != db:
        bad = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        print("NOT byte-identical:", bad)
        sys.exit(1)
    print("two builds byte-identical over %d files" % len(da))
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(a, "gen", "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(a, "metadata.json"), os.path.join(TASK, "metadata.json"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    import writeup
    writeup.main()
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
