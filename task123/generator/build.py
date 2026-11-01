"""Builds task123 end to end: the pack under target/, the golden deliverables under golden/, metadata.json,
generator/figures.json, submission.md and target.zip. `python3 build.py` builds twice into scratch folders,
requires the two to be byte-identical, then installs the first into the task folder."""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import golden  # noqa: E402
import pack  # noqa: E402
import world  # noqa: E402
import writeup  # noqa: E402

ZIP_TIME = (2026, 11, 20, 8, 30, 0)
DESC = {
    pack.F_SURVEY: "Region's monthly guest-movement returns of the accommodation establishments in the Levarna tourist area, July 2025 to September 2026, one row per establishment, month, residence group and submission (extract of 17 November 2026)",
    pack.F_REGISTER: "Regional register of accommodation establishments in the area at 16 November 2026, with the register's dated variations",
    pack.F_CROSSWALK: "Table linking each establishment's regional code (CIR) to its national code (CIN) at the May 2026 change of codes",
    pack.F_CONC: "Provincial collection concessionaire's quarterly summary of tourist-tax declarations, one sheet per comune it collects for, 2025 and 2026",
    pack.F_PLV: "Porto Levarna tax office's quarterly tourist-tax declarations, 2025 and 2026",
    pack.F_SEM: "Sant'Elvira a Mare's quarterly tourist-tax declarations, 2025 and 2026",
    pack.F_LAR: "Lido di Arzena tax office's summary of quarterly tourist-tax declarations, 2025 and 2026",
    pack.F_HILL: "Hill comuni's shared tax office: quarterly tourist-tax declarations of Borgo Sant'Elmo and Castelpieno, 2025 and 2026",
    pack.F_POP: "Resident population of the area's comuni at 1 January 2025 and 1 January 2026 (ISTAT demographic balance layout)",
    pack.F_VAR: "ISTAT extract of 2026 administrative changes for province 112 (the Alvea Salvina merger)",
    pack.F_RATES: "Tourist-tax rates per liable night by comune and category, with the dates each applies from and to",
    pack.F_REG: "The union's regulation for the 2027 peak-month services co-financing (adopted 29 September 2026)",
    pack.F_AIR: "Levarna airport's monthly passenger traffic, January 2025 to September 2026",
    pack.F_PARK: "Daily vehicle entries at five seafront car parks, June to September 2026",
}
DISTRACTORS = [pack.F_AIR, pack.F_PARK]


def zip_dir(src, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(src, fn), "rb").read())


def metadata(target, stats):
    files = []
    for fn in sorted(os.listdir(target)):
        e = {"path": fn, "format": fn.rsplit(".", 1)[1], "bytes": os.path.getsize(os.path.join(target, fn)),
             "description": DESC[fn], "source": "Constructed (seeded generator)", "date": "2026-11-01",
             "license": "CC0-1.0 (original work)"}
        if fn == pack.F_SURVEY:
            e["rows"] = stats["survey_rows"]
        if fn == pack.F_REGISTER:
            e["rows"] = stats["register_rows"]
        if fn == pack.F_CROSSWALK:
            e["rows"] = stats["crosswalk_rows"]
        files.append(e)
    return {
        "task": "task123",
        "title": "Which member comuni of a coastal union of comuni qualify for its 2027 peak-month services "
                 "co-financing on their August 2026 guest nights per resident, with the comuni's January to April 2026 "
                 "guest nights, October 2025 bed-place occupancy by type and the 2025 tourist tax by quarter",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (a monthly accommodation series whose missing "
                     "returns are filled, benchmarked to the quarterly tourist-tax declarations of the same nights)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: every member comune's August 2026 nights per resident set against the 30-night line, "
                        "the qualifying set and the closest comune, with three conformed side tables",
        "as_of": world.AS_OF.isoformat(),
        "deliverables": ["august_2026_guest_nights.xlsx", "peak_cofinancing_2027_note.pdf"],
        "distractor_files": DISTRACTORS,
        "context_artifacts": [],
        "stated_inputs": ["the co-financing line, the residents' date and the definition of guest nights (regulation "
                          "arts. 2 to 4)"],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file": pack.F_SURVEY, "largest_file_rows": stats["survey_rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated by task123/generator/build.py (seeded, deterministic) around a fictional "
                               "Italian coastal union of comuni, its accommodation establishments, the region's monthly "
                               "guest-movement survey, the comuni's tourist-tax declarations and the regional register; "
                               "every comune, organisation, establishment and person is invented, province code 112 is "
                               "not a real province, and no real dataset is reproduced.",
                     "license": "CC0-1.0 (original work)"}],
        "created": "2026-11-01",
        "generator": "task123/generator/build.py",
        "files": files,
    }


SCRUB = os.path.join(TASK_DIR, "..", ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")


PRODUCERS = {
    pack.F_REGISTER: ("Regione - Settore Turismo", "2026-11-16"),
    pack.F_CONC: ("Concessionario tributi", "2026-11-05"),
    pack.F_LAR: ("Comune di Lido di Arzena", "2026-10-31"),
    pack.F_REG: ("Unione Riviera di Levarna", "2026-09-29"),
    pack.F_AIR: ("Aeroporto di Levarna", "2026-10-20"),
    "august_2026_guest_nights.xlsx": ("Ufficio di piano", "2026-11-20"),
    "peak_cofinancing_2027_note.pdf": ("Ufficio di piano", "2026-11-20"),
}


def scrub(folder, producer=None, stamp=None):
    """Repair H1 one file at a time, each with the producer and export date of the system that wrote it."""
    import subprocess
    for fn in sorted(os.listdir(folder)):
        if fn not in PRODUCERS:
            continue
        prod, day = PRODUCERS[fn]
        tmp = tempfile.mkdtemp(prefix="t123_scrub_")
        shutil.copy(os.path.join(folder, fn), os.path.join(tmp, fn))
        r = subprocess.run([sys.executable, SCRUB, tmp, "--apply", "--producer", prod, "--stamp", day,
                            "--floor", "2025-01-01", "--ceiling", "2026-11-20"], capture_output=True, text=True)
        if r.returncode != 0 or "LEFT AS WAS" in r.stdout:
            raise SystemExit("scrub failed on %s: %s %s" % (fn, r.stdout[-600:], r.stderr[-600:]))
        shutil.copy(os.path.join(tmp, fn), os.path.join(folder, fn))
        shutil.rmtree(tmp)


def build_into(root):
    target = os.path.join(root, "target")
    gold = os.path.join(root, "golden")
    scratch = os.path.join(root, "scratch")
    for d in (target, gold, scratch):
        os.makedirs(d, exist_ok=True)
    w, stats = pack.write_pack(target)
    scrub(target, "Regione - Osservatorio turistico regionale", "2026-11-17")
    F = golden.build(target, gold, scratch)
    shutil.rmtree(scratch)
    scrub(gold, "Ufficio di piano dei servizi associati", "2026-11-20")
    json.dump(metadata(target, stats), open(os.path.join(root, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(writeup.figure_values(F), open(os.path.join(root, "figures.json"), "w"), indent=0, ensure_ascii=False)
    writeup.write(F, os.path.join(root, "submission.md"))
    zip_dir(target, os.path.join(root, "target.zip"))
    return F


def digest(root):
    h = {}
    for dp, dn, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            h[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def install(root):
    for d in ("target", "golden"):
        dst = os.path.join(TASK_DIR, d)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(os.path.join(root, d), dst)
    shutil.copy(os.path.join(root, "metadata.json"), os.path.join(TASK_DIR, "metadata.json"))
    shutil.copy(os.path.join(root, "figures.json"), os.path.join(HERE, "figures.json"))
    shutil.copy(os.path.join(root, "submission.md"), os.path.join(TASK_DIR, "submission.md"))
    shutil.copy(os.path.join(root, "target.zip"), os.path.join(TASK_DIR, "target.zip"))


def main():
    base = tempfile.mkdtemp(prefix="t123_build_")
    a, b = os.path.join(base, "a"), os.path.join(base, "b")
    build_into(a)
    build_into(b)
    da, db = digest(a), digest(b)
    diff = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
    if diff:
        print("NOT byte-identical:", diff)
        sys.exit(1)
    print("two builds byte-identical: %d files" % len(da))
    install(a)
    print("target.zip sha256", hashlib.sha256(open(os.path.join(TASK_DIR, "target.zip"), "rb").read()).hexdigest())
    shutil.rmtree(base)


if __name__ == "__main__":
    main()
