"""Builds task466 twice, asserts the two builds byte-identical, and installs target/, golden/, figures.json,
metadata.json, submission.md and target.zip.

    python3 task466/generator/build.py
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

import golden               # noqa: E402
import pack                 # noqa: E402
import truth                # noqa: E402
import writeup              # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT_TIME = dt.datetime(2027, 1, 14, 9, 0, tzinfo=dt.timezone.utc).timestamp()
ZIP_TIME = (2027, 1, 14, 9, 0, 0)

PRODUCERS = {  # each document's issuing body and its own date
    "DEQ_closed_landfill_methane_rule_extract.pdf": ("Department of Environmental Quality", "2024-11-18"),
    "BH_gas_management_plan_2025.pdf": ("Quarrow Valley RSWA", "2025-03-20"),
    "Leyland_BH_monthly_operating_reports_2026.pdf": ("Leyland Renewable Gas", "2027-01-06"),
    "BH_gas_plant_outage_log_2024-2026.xlsx": ("Leyland Renewable Gas", "2027-01-05"),
    "BH_surface_emissions_monitoring_2026.xlsx": ("Quarrow Valley Regional Solid Waste Authority", "2027-01-12"),
    "BH_site_register_2025.xlsx": ("Quarrow Valley Regional Solid Waste Authority", "2025-02-11"),
    "BH_well_register_2025.xlsx": ("Quarrow Valley Regional Solid Waste Authority", "2025-03-04"),
    "breck_hollow_charge_brief_2026.pdf": ("Quarrow Valley RSWA", "2027-01-15"),
    "breck_hollow_methane_return_2026.xlsx": ("Quarrow Valley Regional Solid Waste Authority", "2027-01-15"),
}


def scrub(d):
    sys.path.insert(0, os.path.join(TASK, "..", ".claude", "skills", "reduce-house-fixes", "scripts"))
    import scrub_producer_metadata as S
    for fn in sorted(os.listdir(d)):
        if fn in PRODUCERS:
            prod, stamp = PRODUCERS[fn]
            f = S.scrub_pdf if fn.endswith(".pdf") else S.scrub_ooxml
            f(os.path.join(d, fn), prod, stamp, floor="2024-01-01", ceiling="2027-01-15")


def one_build(root):
    t = truth.build_truth()
    tgt = os.path.join(root, "target")
    gld = os.path.join(root, "golden")
    pack.write_pack(t, tgt)
    res = golden.write_golden(tgt, gld)
    scrub(tgt)
    scrub(gld)
    for d in (tgt, gld):
        for fn in os.listdir(d):
            os.utime(os.path.join(d, fn), (EXPORT_TIME, EXPORT_TIME))
    return t, res


def same_tree(a, b):
    fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
    assert fa == fb, (fa, fb)
    for fn in fa:
        assert filecmp.cmp(os.path.join(a, fn), os.path.join(b, fn), shallow=False), "differs: %s" % fn
    return len(fa)


PROVENANCE = {
    "BH_gas_plant_hourly_2024-2026.csv": "the gas plant historian's hourly export, January 2024 to the first days of January 2027",
    "BH_gas_plant_outage_log_2024-2026.xlsx": "the gas plant operator's log of blower outages, 2024 to 2026",
    "DEQ_closed_landfill_methane_rule_extract.pdf": "the state's closed landfill methane rule (extract)",
    "BH_engine_plant_events_2026.txt": "the energy plant's control system event log for 2026",
    "Leyland_BH_monthly_operating_reports_2026.pdf": "the engine operator's monthly operating reports to the Authority, 2026",
    "BH_surface_emissions_monitoring_2026.xlsx": "the quarterly surface walkover logger exports and the re-monitoring record, 2026",
    "SEM_analyser_checks_2026.csv": "the walkover analyser's zero and span check sheet, 2026",
    "BH_gas_management_plan_2025.pdf": "the landfill gas management plan, revision 4 (extract)",
    "BH_site_register_2025.xlsx": "the Authority's site register for the landfill",
    "BH_well_register_2025.xlsx": "the Authority's register of gas wells",
    "weather_station_daily_2024-2026.csv": "the site weather station's daily summaries, 2024 to 2026",
    "leachate_pumping_2026.csv": "leachate sump levels, pumping and hauling, 2026",
    "BH_weighbridge_archive_2004-2017.csv": "monthly tonnages received by waste class, 2004 to closure in 2017",
}


def metadata(files):
    out = {
        "task": "task466",
        "title": "Breck Hollow Landfill: the 2026 closed landfill methane charge and return",
        "objective": "Data Extraction & Conformation (ETL)",
        "domain": "Physical & Environmental Sciences",
        "decision": "which tier of the state's closed landfill methane charge the landfill's 2026 return falls in, the charge for the 2027 budget, and the 2026 return's schedules",
        "deliverables": ["breck_hollow_charge_brief_2026.pdf", "breck_hollow_methane_return_2026.xlsx"],
        "distractor_files": ["target/weather_station_daily_2024-2026.csv", "target/leachate_pumping_2026.csv",
                             "target/BH_weighbridge_archive_2004-2017.csv"],
        "distractor_reasons": {
            "target/weather_station_daily_2024-2026.csv": "daily weather at the site; the rule's quantities are measured at the gas plant and no figure is weather-normalised",
            "target/leachate_pumping_2026.csv": "leachate handling at the site's sump, a separate system from the gas plant",
            "target/BH_weighbridge_archive_2004-2017.csv": "tonnages received while the landfill was open; the rule has a closed landfill with a gas system estimate from its capture, and the archive starts thirty years after the first waste",
        },
        "as_of": "2027-01-15",
        "files": [],
    }
    for fn in sorted(files):
        out["files"].append({"path": "target/" + fn, "content": PROVENANCE[fn],
                             "source": "synthetic: constructed by the task generator (fixed seed) in the layout of the named system's export",
                             "date": "2027-01-14", "licence": "CC0 1.0 (constructed for this task)"})
    return out


def make_zip(target, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(fn, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(target, fn), "rb") as f:
                z.writestr(zi, f.read())


def main():
    tmp = tempfile.mkdtemp(prefix="t466_")
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
                os.utime(os.path.join(dst, fn), (EXPORT_TIME, EXPORT_TIME))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tgt = os.path.join(TASK, "target")
    res = golden.compute(tgt)
    figs = golden.figures(res)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata(os.listdir(tgt)), f, indent=1)
    writeup.write(figs, os.path.join(TASK, "submission.md"))
    make_zip(tgt, os.path.join(TASK, "target.zip"))
    print("target.zip sha256", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
