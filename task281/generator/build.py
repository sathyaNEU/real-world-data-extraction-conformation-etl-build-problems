"""Builds the pack twice from the fixed seed, asserts the two builds byte-identical and every generator check,
then installs target/, golden/, metadata.json, generator/figures.json and submission.md and writes target.zip."""
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
import admin
import analysis as AN
import checks
import golden
import pack
import params as P
import world
import writeup

STAMP = (2026, 10, 31, 9, 12, 0)
LIC = "Constructed for this task; no third-party records; CC BY 4.0"
PROV = "synthetic, constructed by the task author to behave as the named system's export"
SOURCES = {
    "holds": ("Shelfmark Lend institutional holds export for Ardmuir University, 1 September 2025 to the October "
              "2026 download", "2026-10-31"),
    "loans": ("Shelfmark Lend institutional checkouts export for Ardmuir University, same period", "2026-10-31"),
    "terms": ("Ardmuir University Court paper UC/26/114, Course Texts Fund 2027 terms", "2026-10-15"),
    "lending": ("Shelfmark Lend lending and licence terms for institutional customers, version 2025.2", "2025-08-01"),
    "procedures": ("Ardmuir University Library collections procedures for course texts, version 3", "2026-08-24"),
    "register": ("The Library's electronic resource management licence register (title licences and packages)",
                 "2026-10-31"),
    "status": ("Shelfmark Lend licence status report for 40-loan licences in force", "2025-09-01"),
    "lists": ("Reading-list system export of list items, 2025-26 and 2026-27", "2026-10-29"),
    "courses": ("Registry course catalogue, 2025-26 and 2026-27", "2026-10-01"),
    "catalogue": ("Library catalogue records for course texts (print and electronic)", "2026-10-30"),
    "invoices": ("Finance system invoice lines charged to course texts funds, 1 January to 31 October 2026",
                 "2026-10-31"),
    "rates": ("Finance Office monthly exchange rates", "2026-10-01"),
    "survey": ("Students' Association textbook access survey, spring 2026", "2026-05-29"),
    "usage": ("Shelfmark Lend title usage report, 2025-26", "2026-09-02"),
}


def metadata(target):
    files = []
    names = dict(pack.FILES)
    for k, fn in sorted(names.items(), key=lambda kv: kv[1]):
        src, date = SOURCES[k]
        files.append(dict(file=fn, source=src, date=date, rows=_rows(os.path.join(target, fn)), license=LIC,
                          provenance=PROV))
    for pname, fn in sorted(pack.KBART.items(), key=lambda kv: kv[1]):
        files.append(dict(file=fn, source="Publisher KBART title list for the package %s" % pname,
                          date="2026-01-05", rows=_rows(os.path.join(target, fn)), license=LIC, provenance=PROV))
    return {"task": "task281", "architecture": 4, "as_of": "2026-11-02",
            "world": "Ardmuir University Library (fictional), Scotland; Shelfmark Lend (fictional) lending platform",
            "files": files,
            "distractors": [
                {"file": pack.FILES["survey"], "why_relevant": "students' own account of e-textbook access by faculty "
                 "in the same semester, which the Court's terms do not use to divide the fund"},
                {"file": pack.FILES["usage"], "why_relevant": "the platform's monthly checkouts and turnaways by "
                 "title, a demand signal at the wrong grain that the terms do not use"}],
            "deliverables": ["course_texts_fund_2027.csv", "course_texts_fund_2027.xlsx"],
            "stated_inputs": ["180,000"]}


def _rows(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8") as f:
            return sum(1 for _ in f) - 1
    return None


def digest(folder):
    h = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def one_build(base, run_checks):
    target, gold, gen = (os.path.join(base, x) for x in ("target", "golden", "gen"))
    os.makedirs(gen, exist_ok=True)
    W = world.build(P.SEED)
    A = admin.build(W, P.SEED)
    pack.write(W, A, target)
    AN._CACHE.clear()
    F = golden.write_all(target, gold)
    writeup.write(F, os.path.join(base, "submission.md"), os.path.join(gen, "figures.json"))
    json.dump(metadata(target), open(os.path.join(base, "metadata.json"), "w"), indent=1, sort_keys=True)
    if run_checks:
        rows = checks.run(W, A, target, gold)
        if checks.report(rows):
            sys.exit(1)
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
    try:
        install(a, b)
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def install(a, b):
    da = one_build(a, True)
    db = one_build(b, False)
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
    for sub in ("target", "golden"):
        for fn in os.listdir(os.path.join(TASK, sub)):
            os.utime(os.path.join(TASK, sub, fn), (1793440320, 1793440320))
    cut_zip(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("target.zip", z[:8])


if __name__ == "__main__":
    main()
