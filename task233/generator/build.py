"""Builds task233 twice from nothing, checks the two builds are byte-identical, and installs target/,
golden/, generator/figures.json, metadata.json, target.zip and submission.md.

    python3 task233/generator/build.py
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
import golden as G  # noqa: E402
import pack as PK  # noqa: E402
import writeup as WU  # noqa: E402
from world import World  # noqa: E402

ASOF = "2026-10-16"
SOURCES = {
    "cpi_field_quotes_2025-10_2026-09.csv": ("evidence", "NSO Prices Division, CPI price database extract of field-collected quotes, reference months October 2025 to September 2026, pulled 14 October 2026; synthetic"),
    "handheld_status_codes.csv": ("evidence", "NSO Prices Division, handheld collection status codes before and after the August 2026 software update; synthetic"),
    "cpi_item_list_2026.csv": ("evidence", "NSO Prices Division, CPI 2026 basket item list with COICOP classes; synthetic"),
    "cpi_outlet_register_2026-10.xlsx": ("evidence", "NSO Prices Division, CPI outlet register as at 1 October 2026; synthetic"),
    "fqt_backcheck_register_2026q3.xlsx": ("evidence", "NSO Field Quality Team, back-check register for July to September 2026; synthetic"),
    "tallis_visit_log_2026-07_2026-09.csv": ("evidence", "Tallis Field Research Ltd, handheld visit log export for July to September 2026; synthetic"),
    "tallis_collection_schedule_2026q3.csv": ("evidence", "Tallis Field Research Ltd, quarterly collection schedule agreed 26 June 2026; synthetic"),
    "nso_collection_calendar_2026.csv": ("evidence", "NSO collection calendar, index days and public holidays; synthetic"),
    "commodity_replacement_decisions_2026.xlsx": ("evidence", "NSO Prices Division, commodity analysts' replacement decisions, extract of 14 October 2026; synthetic"),
    "tallis_quarterly_return_2026q3.xlsx": ("context", "Tallis Field Research Ltd, quarterly activity return submitted 9 October 2026; synthetic"),
    "pcqs_price_collection_quality_standard_v3.pdf": ("evidence", "NSO Prices Division, Price Collection Quality Standard version 3.0; synthetic"),
    "pcsa_schedule4_collection_fees.pdf": ("evidence", "Price Collection Services Agreement, Schedule 4 regional collection fees, variation 3; synthetic"),
    "tallis_collector_roster_2026-09.xlsx": ("distractor", "Tallis Field Research Ltd, collector roster and collection test record, 30 September 2026; synthetic"),
    "cpi_regional_indices_2026-06_2026-09.csv": ("distractor", "NSO consumer price index monthly regional indices, released 13 October 2026; synthetic"),
}
DISTRACTORS = {
    "tallis_collector_roster_2026-09.xlsx": "each collector's area, start date and latest collection test; relevant to the contractor's teams, unused by the solution",
    "cpi_regional_indices_2026-06_2026-09.csv": "the published regional index levels for June to September 2026; relevant to the prices collected, unused by the solution",
}


def metadata():
    return {
        "task": "task233", "architecture": 3, "as_of": ASOF,
        "decision": "each collection region's outcome under the national statistics office's Price Collection Quality "
                    "Standard for the field price collection of July to September 2026, and the quarter's service credit",
        "deliverables": ["pcqs_2026q3_assessment.xlsx", "pcqs_2026q3_contractor_letter.pdf"],
        "files": {f: {"source": s, "date": ASOF, "license": "synthetic, CC0", "role": role} for f, (role, s) in SOURCES.items()},
        "distractor_files": sorted(DISTRACTORS),
        "distractor_notes": DISTRACTORS,
        "stated_inputs": ["98.0", "95.5", "4"],
    }


def digest(folder):
    out = {}
    for root, _, files in os.walk(folder):
        for f in sorted(files):
            p = os.path.join(root, f)
            out[os.path.relpath(p, folder)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def one(base):
    tgt, gold, gen = os.path.join(base, "target"), os.path.join(base, "golden"), os.path.join(base, "gen")
    os.makedirs(gen)
    PK.Pack(World(), tgt).write_all()
    res, fig = G.build(tgt, gold, gen)
    return tgt, gold, gen, res, fig


def zip_target(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo(f, date_time=(2026, 10, 15, 8, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(src, f), "rb").read())


def main():
    a, b = tempfile.mkdtemp(prefix="t233a_"), tempfile.mkdtemp(prefix="t233b_")
    ta, ga, gna, res, fig = one(a)
    tb, gb, gnb, _, _ = one(b)
    da = {**{"target/" + k: v for k, v in digest(ta).items()}, **{"golden/" + k: v for k, v in digest(ga).items()},
          **{"gen/" + k: v for k, v in digest(gna).items()}}
    db = {**{"target/" + k: v for k, v in digest(tb).items()}, **{"golden/" + k: v for k, v in digest(gb).items()},
          **{"gen/" + k: v for k, v in digest(gnb).items()}}
    if da != db:
        diff = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        print("NOT byte-identical:", diff)
        return 1
    print("two builds byte-identical over %d files" % len(da))
    for sub in ("target", "golden"):
        dst = os.path.join(TASK, sub)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(a, sub), dst)
    shutil.copy(os.path.join(gna, "figures.json"), os.path.join(HERE, "figures.json"))
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(), f, indent=1, sort_keys=True)
    zip_target(os.path.join(TASK, "target"), os.path.join(TASK, "target.zip"))
    res = G.analysis.run(os.path.join(TASK, "target"))
    WU.write(TASK, res, json.load(open(os.path.join(HERE, "figures.json"))))
    shutil.rmtree(a)
    shutil.rmtree(b)
    print("installed target/, golden/, metadata.json, target.zip, submission.md; target.zip sha256",
          hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
