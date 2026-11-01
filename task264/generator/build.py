"""Builds the pack twice from the fixed seed, asserts the two builds byte-identical, installs target/,
golden/, metadata.json, generator/figures.json and submission.md, and writes target.zip."""
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
from world import build_all
from pack import write_pack, F, DISTRACTORS
import analysis
import goldens
import writeup

STAMP = (2026, 10, 6, 9, 30, 0)
SOURCES = {
    "spells": ("The board's commissioning data warehouse: admitted patient care spells for the lumbar spine cohort "
               "(index operations 2022-23 to 2025-26 and every later spell submitted by 30 September 2026)", "2026-09-30"),
    "proms_old": ("The outcomes supplier's commissioner extract from its first platform, questionnaires completed "
                  "1 April 2022 to 31 March 2025", "2025-04-07"),
    "proms_new": ("The outcomes supplier's commissioner extract from its second platform, questionnaires completed "
                  "1 April 2025 to 30 September 2026", "2026-10-01"),
    "link": ("The supplier's patient references against the board's pseudonymised NHS numbers", "2026-10-01"),
    "deaths": ("Civil registration deaths linked to the cohort by the board's data services", "2026-09-30"),
    "policy": ("The board's contracting policy for the 2027-28 additional lumbar activity", "2026-09-17"),
    "capacity": ("Providers' 2027-28 capacity returns as collected by the planned care contracting team", "2026-09-29"),
    "providers": ("The warehouse's provider reference", "2026-09-30"),
    "codes": ("Code descriptions for the codes the extract carries", "2026-09-30"),
    "ptl": ("Providers' month-end waiting list submissions, January to March 2026", "2026-04-09"),
    "removals": ("Providers' waiting list removals, November 2025 to April 2026", "2026-05-08"),
    "triage": ("The community MSK triage service's referral log", "2026-04-14"),
    "fft": ("Friends and Family Test inpatient responses for the providers' spinal services, 2025-26", "2026-05-12"),
    "cqc": ("Care Quality Commission location ratings for the providers' sites", "2026-09-30"),
}


def metadata(n):
    files = []
    for k, fn in sorted(F.items(), key=lambda kv: kv[1]):
        src, date = SOURCES[k]
        files.append({"file": fn, "source": src, "date": date, "rows": n.get(k),
                      "license": "Constructed for this task; no third-party records; CC BY 4.0",
                      "provenance": "synthetic, constructed by the task author to behave as the named system's export"})
    return {"task": "task264", "architecture": 3, "as_of": "2026-10-06",
            "world": "Quenmoor and Kirkbeck Integrated Care Board (fictional), England",
            "files": files,
            "distractors": [{"file": F[k], "why_relevant": why} for k, why in (
                ("fft", "patient-reported experience at the same providers' spinal services, a quality signal the "
                        "policy does not use"),
                ("cqc", "the regulator's ratings of the same sites, a quality signal the policy does not use"))],
            "deliverables": ["spinal_volume_2027-28.csv", "spinal_volume_board_paper.docx"],
            "stated_inputs": ["1,250", "14.5"]}


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base):
    target, golden, gen = (os.path.join(base, x) for x in ("target", "golden", "gen"))
    os.makedirs(gen, exist_ok=True)
    A = build_all()
    n = write_pack(A, target)
    res = analysis.run(target)
    Fr = goldens.write_all(res, golden, gen)
    writeup.write(Fr, base, os.path.join(gen, "figures.json"))
    os.remove(os.path.join(gen, "waiting_list_2026-03-31.png"))
    json.dump(metadata(n), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    return digest(base)


def cut_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=STAMP)
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
    shutil.copy(os.path.join(a, "submission.md"), os.path.join(TASK, "submission.md"))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])
    shutil.rmtree(a)
    shutil.rmtree(b)


if __name__ == "__main__":
    main()
