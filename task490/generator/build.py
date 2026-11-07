"""task490 pack builder: writes target/, golden/, generator/figures.json, metadata.json and target.zip.
Deterministic: two runs give byte-identical outputs."""
import json
import os
import shutil
import zipfile
from datetime import datetime

import world as W
import sim
import records as R
import docs as D
import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
EXPORT_TIME = (2026, 11, 6, 8, 41, 0)
EXPORT_TS = datetime(*EXPORT_TIME).timestamp()


def build_world():
    boats, fleet, cycles = sim.season_traffic()
    scheds = {name: sim.release_schedule(name) for name in W.RESERVOIRS}
    meters = {lic["ref"]: sim.meter_truth(lic) for lic in W.LICENCES}
    return boats, fleet, cycles, scheds, meters


def write_metadata():
    files = {
        R.F_MOVES: ("LockCount Mk3 counter network, season movement export for the six summit locks", "2026-11-03"),
        R.F_SITES: ("LockCount Mk3 counter network, site configuration export", "2026-11-03"),
        R.F_KEEP: ("Tilsey summit volunteer lock-keepers' log, typed up from the paper log, April to September",
                   "2026-11-04"),
        R.F_NOTICES: ("the trust's navigation notices for the three summit lines, 2026", "2026-11-02"),
        R.F_LOCKS: ("the trust's lock chamber survey 2025 and the transcribed 1951 schedule of locks", "2026-01-19"),
        R.F_RET: ("daily returns from the three valve-operated supply reservoirs", "2026-11-02"),
        R.F_COLD: ("Coldmere Reservoir outlet gauging weir telemetry, 15-minute means", "2026-11-02"),
        R.F_LIC: ("water abstraction agreements on the summit pounds", "2026-10-12"),
        R.F_READ: ("abstraction meter month-end readings, March to October 2026", "2026-11-02"),
        R.F_WO: ("the trust's field works orders, January to October 2026", "2026-11-02"),
        R.F_BOATS: ("boat licence register extract, licensed craft of the region", "2026-11-01"),
        R.F_STORE: ("weekly reservoir storage, the trust's published reservoir watch figures", "2026-11-02"),
        D.F_PROG: ("Water Management, back-pumping programme 2027/28: scope and siting, version 1.1", "2026-09-21"),
        D.F_RESREG: ("Reservoir Safety and Engineering, reservoir register extract", "2026-07-07"),
    }
    meta = {
        "task": "task490",
        "decision": "which summit the Coldmere Canals Trust's 2027/28 back-pumping scheme serves",
        "deliverables": ["summit_lockage_return_2026.csv", "summit_water_2026.xlsx", "backpumping_site_2027.docx"],
        "distractor_files": ["target/" + R.F_BOATS, "target/" + R.F_STORE],
        "files": {("target/" + k): {"source": "constructed for this task (an invented waterways charity, its "
                                              "canals, reservoirs, counters and records)",
                                    "covers": v[0], "date": v[1], "licence": "CC BY 4.0 (constructed for this task)"}
                  for k, v in sorted(files.items())},
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
        f.write("\n")
    return sorted(files)


def cut_zip():
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=EXPORT_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, fn), "rb").read())
    os.utime(path, (EXPORT_TS, EXPORT_TS))


def main():
    for folder in (TARGET, GOLDEN):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    boats, fleet, cycles, scheds, meters = build_world()
    events = R.camera_events(cycles, boats)
    n_rows = R.write_moves(TARGET, events)
    R.write_sites(TARGET)
    R.write_keepers(TARGET, R.keeper_entries(cycles))
    R.write_notices(TARGET)
    R.write_lock_register(TARGET)
    R.write_returns(TARGET, scheds)
    R.write_coldmere(TARGET, R.coldmere_series(scheds["Coldmere Reservoir"]))
    R.write_abstraction(TARGET, meters)
    R.write_works(TARGET, meters)
    R.write_boats(TARGET, boats, fleet)
    R.write_storage(TARGET, scheds)
    D.write_all(TARGET)
    figs = G.write_golden(GOLDEN, TARGET)
    figs["movement_rows"] = n_rows
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
        f.write("\n")
    names = write_metadata()
    for folder in (TARGET, GOLDEN):
        for fn in os.listdir(folder):
            os.utime(os.path.join(folder, fn), (EXPORT_TS, EXPORT_TS))
    assert sorted(os.listdir(TARGET)) == names, (sorted(os.listdir(TARGET)), names)
    cut_zip()
    print("built %d files, %d movement rows; call %s %.1f Ml, runner-up %s %.1f Ml" % (
        len(names), n_rows, figs["call"], figs["lockage_ml"][figs["call"]], figs["runner_up"],
        figs["lockage_ml"][figs["runner_up"]]))


if __name__ == "__main__":
    main()
