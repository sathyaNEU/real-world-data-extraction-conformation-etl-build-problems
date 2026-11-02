"""Builds task484 twice, asserts the two builds byte-identical, and installs target/, golden/, figures.json,
metadata.json, submission.md and target.zip.

    python3 task484/generator/build.py
"""
import datetime as dt
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

import common as C      # noqa: E402
import golden           # noqa: E402
import pack             # noqa: E402
import world            # noqa: E402
import writeup          # noqa: E402

TASK = C.TASK
STAMP = dt.datetime(2026, 3, 23, 16, 0, tzinfo=dt.timezone.utc).timestamp()
PRODUCERS = {
    "utc_asset_register_2025.xlsx": ("Wrenford Borough Council", "2026-01-12"),
    "count_points_2025.xlsx": ("Wrenford Borough Council", "2026-01-15"),
    "expansion_factor_review_2025.xlsx": ("Wrenford Borough Council", "2026-02-10"),
    "network_operations_log_2025.docx": ("Wrenford Borough Council", "2026-01-09"),
    "traffic_estimate_terms_2025.pdf": ("Wrenford Borough Council", "2026-02-03"),
    "noise_mapping_2026_scope.pdf": ("Wrenford Borough Council", "2026-01-26"),
    "traffic_network_2025.xlsx": ("Wrenford Borough Council", "2026-03-23"),
}


def scrub(d):
    sys.path.insert(0, os.path.join(TASK, "..", ".claude", "skills", "reduce-house-fixes", "scripts"))
    import scrub_producer_metadata as S
    for fn in sorted(os.listdir(d)):
        if fn in PRODUCERS:
            prod, stamp = PRODUCERS[fn]
            f = S.scrub_pdf if fn.endswith(".pdf") else S.scrub_ooxml
            f(os.path.join(d, fn), prod, stamp, floor="2025-01-01", ceiling="2026-03-24")


def one_build(root):
    W = world.build()
    tgt, gld = os.path.join(root, "target"), os.path.join(root, "golden")
    pack.write_pack(W, tgt)
    G = golden.write_golden(tgt, gld)
    scrub(tgt)
    scrub(gld)
    for d in (tgt, gld):
        for fn in os.listdir(d):
            os.utime(os.path.join(d, fn), (STAMP, STAMP))
    return W, G


def same_tree(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    assert fa == fb, (fa, fb)
    for fn in fa:
        assert filecmp.cmp(os.path.join(a, fn), os.path.join(b, fn), shallow=False), "differs: %s" % fn
    return len(fa)


PROV = {
    "utc_detector_daily_2025.csv": "the urban traffic control system's daily detector summaries for 2025, exported in two half-year parts",
    "utc_asset_register_2025.xlsx": "the urban traffic control asset register: signalised junctions and their detector channels",
    "atc_daily_2025.csv": "the permanent automatic counters' daily export for 2025, all motor vehicles and output channels",
    "atc_sites_2025.csv": "the permanent counter site list with each site's current equipment",
    "classifier_schemes.csv": "the vehicle class tables of the two classifier models the counters have carried",
    "manual_counts_2025.csv": "the 2025 manual classified counts, keyed from the count sheets, by hour and direction",
    "count_points_2025.xlsx": "the Council's count point register",
    "traffic_estimate_terms_2025.pdf": "the Council's note on traffic estimate terms and the counting programme, edition 2025.2",
    "noise_mapping_2026_scope.pdf": "Environmental Protection's scope note for the 2026 noise mapping contract",
    "network_operations_log_2025.docx": "the transport data team's operations log for its counters and signal assets, 2025",
    "expansion_factor_review_2025.xlsx": "the team's annual review of its counter groups against the counters' own annual flows",
    "streetworks_permits_2025.csv": "the street works permits granted on the borough's roads in 2025",
    "school_term_dates.csv": "the local authority's school term dates, 2024-25 and autumn 2025",
}


def metadata(files):
    out = {
        "task": "task484",
        "title": "Wrenford: road sections over three million vehicles in 2025",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "Survey Research & Official Statistics",
        "decision": "which road sections the Council counted in 2025 carried more than three million vehicle passages, fixing the noise mapping contract's scope, with each counted section's 2025 traffic, the counters' heavy goods vehicles and the two renewed junctions' recorded approach totals",
        "deliverables": ["noise_round_sections_2025.csv", "section_traffic_2025.png", "traffic_network_2025.xlsx"],
        "distractor_files": ["target/streetworks_permits_2025.csv", "target/school_term_dates.csv"],
        "distractor_reasons": {
            "target/streetworks_permits_2025.csv": "works on the borough's streets in 2025; no works were on a counted section within two days of its count, and the sections' annual traffic is read from records that already carry whatever the works did",
            "target/school_term_dates.csv": "the term calendar; the counting programme already keeps counts out of school holidays, and a section's own year is read from the records rather than built from a calendar",
        },
        "as_of": C.AS_OF.isoformat(),
        "files": [],
    }
    for fn in sorted(files):
        out["files"].append({"path": "target/" + fn, "content": PROV[fn],
                             "source": "synthetic: constructed by the task generator (fixed seed) in the layout of the named system's export",
                             "date": "2026-03-23", "licence": "CC0 1.0 (constructed for this task)"})
    return out


def make_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=C.ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, fn), "rb") as f:
                z.writestr(zi, f.read())


def main():
    tmp = tempfile.mkdtemp(prefix="t484_")
    try:
        a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
        os.makedirs(a)
        os.makedirs(b)
        one_build(a)
        one_build(b)
        n1 = same_tree(os.path.join(a, "target"), os.path.join(b, "target"))
        n2 = same_tree(os.path.join(a, "golden"), os.path.join(b, "golden"))
        print("two builds byte-identical: %d target files, %d golden files" % (n1, n2))
        for d in ("target", "golden"):
            dst = os.path.join(TASK, d)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(os.path.join(a, d), dst)
            for fn in os.listdir(dst):
                os.utime(os.path.join(dst, fn), (STAMP, STAMP))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tgt = os.path.join(TASK, "target")
    G = golden.compute(tgt)
    figs = golden.figures(G)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(os.listdir(tgt)), f, indent=1)
    writeup.write(G, os.path.join(TASK, "submission.md"))
    make_zip(tgt, os.path.join(TASK, "target.zip"))
    print("target.zip md5", hashlib.md5(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
