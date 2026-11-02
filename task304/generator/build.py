"""task304 architecture 5: build the pack twice, assert the two builds are byte-identical, then install target/,
golden/, generator/figures.json, metadata.json, submission.md and target.zip."""
import filecmp
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

import golden  # noqa: E402
import pack  # noqa: E402
import results  # noqa: E402
import writeup  # noqa: E402

ZIP_TIME = (2026, 11, 27, 9, 0, 0)

PROVENANCE = {
    "collision_records_2016_2025.csv": ("Ardleshire County Council collision system, validated injury collision record, extract 14 October 2026", "police-reported injury collisions in Ardleshire 2016 to 2025, with the county's junction node links"),
    "junction_inventory_2026.xlsx": ("Ardleshire County Council network management, junction inventory 2026", "principal road network junctions: layout, control and traffic estimates by year 2016 to 2026"),
    "road_network_register_2026.csv": ("Ardleshire County Council network register", "classified roads and sections with their highway authority"),
    "junction_safety_fund_guidance_2027.pdf": ("Junction Safety Fund programme team, bid guidance 15 September 2026", "the 2027 fund: eligibility, the benefit, crash modification factors and the supporting tables"),
    "network_screening_2026.pdf": ("Halberd Transport Planning for Ardleshire County Council, junction screening note 9 October 2026", "the junctions listed for treatment study"),
    "police_collisions_2026_jan_may.csv": ("Ardleshire Police collision system (to 31 May 2026), provisional extract", "injury collisions January to May 2026"),
    "police_casualties_2026_jan_may.csv": ("Ardleshire Police collision system (to 31 May 2026), provisional extract", "casualties of those collisions"),
    "police_vehicles_2026_jan_may.csv": ("Ardleshire Police collision system (to 31 May 2026), provisional extract", "vehicles in those collisions"),
    "police_export_2026_jun_sep.json": ("Ardleshire Police collision recording system (from 1 June 2026), export 20 November 2026", "injury collisions from June 2026 and records amended in the new system, with casualties and vehicles"),
    "fatal_casualty_notifications_2026.xlsx": ("Ardleshire Police Fatal Collision Investigation Unit, notifications to the county road safety team", "casualties who died after road collisions in 2026"),
    "skid_resistance_survey_2025.csv": ("Ardleshire County Council skid resistance survey 2025", "sideway-force coefficients and investigatory levels by road section"),
    "community_speedwatch_2026.csv": ("Ardleshire community speedwatch groups, 2026 sessions", "volunteer speed checks by location and session"),
}


def tree_equal(a, b):
    names_a, names_b = sorted(os.listdir(a)), sorted(os.listdir(b))
    if names_a != names_b:
        return False, "file lists differ"
    for n in names_a:
        if not filecmp.cmp(os.path.join(a, n), os.path.join(b, n), shallow=False):
            return False, n
    return True, ""


def metadata(target):
    files = []
    for n in sorted(os.listdir(target)):
        src, cov = PROVENANCE[n]
        files.append({"path": "target/" + n, "source": src, "covers": cov,
                      "made": "constructed by the task's seeded generator in the source system's export format",
                      "licence": "synthetic, released with the task under CC BY 4.0", "date": "2026-11-27"})
    return {
        "task": "task304",
        "decision": "which junction on Ardleshire's 2026 screening list takes the roundabout in the county's 2027 Junction Safety Fund bid, and the injury collisions a year a roundabout would prevent at each listed junction",
        "deliverables": ["junction_bid_2027.docx", "bid_annex_2026.xlsx"],
        "distractor_files": ["target/skid_resistance_survey_2025.csv", "target/community_speedwatch_2026.csv"],
        "as_of": "2026-12-04",
        "files": files,
    }


def zip_target(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, n), "rb").read())


def main():
    tmp = tempfile.mkdtemp(prefix="t304b_")
    a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
    pack.build(a)
    pack.build(b)
    ok, why = tree_equal(a, b)
    assert ok, "builds differ: %s" % why
    target = os.path.join(TASK, "target")
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(a, target)
    F = results.write(target, os.path.join(HERE, "figures.json"))
    gd = os.path.join(TASK, "golden")
    if os.path.exists(gd):
        shutil.rmtree(gd)
    golden.write(gd, F)
    g2 = os.path.join(tmp, "g2")
    golden.write(g2, F)
    ok, why = tree_equal(gd, g2)
    assert ok, "goldens differ: %s" % why
    writeup.write(os.path.join(TASK, "submission.md"), F)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(target), f, indent=1)
        f.write("\n")
    zip_target(target, os.path.join(TASK, "target.zip"))
    zip_target(b, os.path.join(tmp, "b.zip"))
    h = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    h2 = hashlib.sha256(open(os.path.join(tmp, "b.zip"), "rb").read()).hexdigest()
    assert h == h2, "zips differ"
    shutil.rmtree(tmp)
    print("built: two byte-identical builds; target.zip sha256 %s" % h[:16])
    print("call: %s %.1f prevented a year (runner-up %s %.1f)" % (F["call"], F["call_benefit"], F["runner_up"], F["runner_up_benefit"]))


if __name__ == "__main__":
    main()
