"""Build task168: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json,
generator/figures.json and submission.md, then the checks and the independent verifier, then a second full build
into a scratch folder compared byte for byte, then target.zip cut from the pack.

    python3 task168/generator/build.py              everything
    python3 task168/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import calendar
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
PACK_DONE = (2025, 12, 12, 9, 0, 0)                          # the pack assembled, Rome time
MTIME = calendar.timegm((2025, 12, 12, 8, 0, 0, 0, 0, 0))    # the same moment, UTC

FILES = {
    "rm": "rm_booking_build_s25.csv",
    "ym3": "ym3_leg_history_s24.sqlite",
    "dcs": "dcs_flight_close_s25.csv",
    "ref": "booking_engine_refusals_s25.csv",
    "cap": "summer2026_capacity_plan_v3.xlsx",
    "basis": "planning_basis_NP-PB-26S_issue2.pdf",
    "log": "schedule_change_log.xlsx",
    "fleet": "fleet_register.csv",
    "routes": "route_master.csv",
    "close": "summer_closeout_IS24_IS25.pdf",
    "dict": "data_dictionary_rev5.pdf",
    "fares": "fare_report_IS25.xlsx",
    "comp": "competitor_seats_IS25_IS26.csv",
    "manifest": "export_manifest.csv",
}

MANIFEST = [
    ("rm_booking_build_s25.csv", "Revenue Management Systems", "RM", "2025-12-01",
     "summer 2025 departures, every route", "extract of 1 December 2025, 04:38 UTC"),
    ("ym3_leg_history_s24.sqlite", "Revenue Management Systems", "YM3 archive", "2024-11-18",
     "summer 2024 legs, every route", "archive frozen at the migration; read only"),
    ("dcs_flight_close_s25.csv", "Airport Operations", "DCS", "2025-11-03",
     "summer 2025 operated departures, every route", "flight close-out as finalised"),
    ("booking_engine_refusals_s25.csv", "Digital Sales", "booking engines", "2025-12-03",
     "requests for summer 2025 departures, logged {span}", ""),
    ("summer2026_capacity_plan_v3.xlsx", "Network Planning", "", "2025-11-21", "summer 2026 against summer 2025",
     "version 3"),
    ("planning_basis_NP-PB-26S_issue2.pdf", "Network Planning", "", "2025-11-28", "the nine Linate routes",
     "issue 2"),
    ("schedule_change_log.xlsx", "Network Planning", "", "2025-11-21", "IS24 to IS26", ""),
    ("fleet_register.csv", "Fleet Management", "", "2025-11-30", "registrations in service, retired and on order",
     ""),
    ("route_master.csv", "Network Planning", "", "2025-11-21", "routes flown in IS25", ""),
    ("summer_closeout_IS24_IS25.pdf", "Revenue Management reporting", "", "2025-11-14", "IS24 and IS25 by route",
     ""),
    ("data_dictionary_rev5.pdf", "Revenue Management Systems", "", "2025-12-02", "the four analytics extracts",
     "revision 5"),
    ("fare_report_IS25.xlsx", "Revenue Management", "", "2025-11-10", "IS25 average net fares by route and month",
     ""),
    ("competitor_seats_IS25_IS26.csv", "Network Planning", "filed schedules", "2025-11-24",
     "weekly seats by airport pair, IS25 and IS26", "typical week in July"),
]


def build_pack(out):
    import pack as PK
    import docs as DC
    import sim
    from records import Seasons
    os.makedirs(out, exist_ok=True)
    S = Seasons()
    regs = PK.tails_for(S)
    n = {}
    n[FILES["rm"]] = PK.rm_build_s25(S, os.path.join(out, FILES["rm"]))
    legs, bkg = PK.ym3_archive_s24(S, os.path.join(out, FILES["ym3"]))
    n[FILES["ym3"]] = bkg
    n[FILES["dcs"]] = PK.dcs_close_s25(S, os.path.join(out, FILES["dcs"]), regs)
    nref, _, ev = PK.refusals_log(S, os.path.join(out, FILES["ref"]))
    n[FILES["ref"]] = nref
    first = min(e[0] for e in ev).astimezone(sim.ROME).date()
    last = max(e[0] for e in ev).astimezone(sim.ROME).date()
    span = "%d %s %d to %d %s %d" % (first.day, first.strftime("%B"), first.year, last.day, last.strftime("%B"),
                                      last.year)
    DC.capacity_plan(S, os.path.join(out, FILES["cap"]))
    DC.planning_basis(os.path.join(out, FILES["basis"]))
    DC.change_log(S, os.path.join(out, FILES["log"]))
    DC.fleet_register(os.path.join(out, FILES["fleet"]), regs)
    DC.route_master(S, os.path.join(out, FILES["routes"]))
    DC.closeout(S, os.path.join(out, FILES["close"]))
    DC.dictionary(os.path.join(out, FILES["dict"]), span)
    DC.fare_report(S, os.path.join(out, FILES["fares"]))
    DC.competitor_seats(S, os.path.join(out, FILES["comp"]))
    DC.export_manifest(os.path.join(out, FILES["manifest"]),
                       [tuple(c.format(span=span) for c in row) for row in MANIFEST])
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    return n


def digest(folder):
    h = {}
    for f in sorted(os.listdir(folder)):
        h[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return h


def cut_zip(root):
    target = os.path.join(root, "target")
    zpath = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo(f, date_time=PACK_DONE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    return zpath


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--pack-only", action="store_true")
    ap.add_argument("--rebuild-dir")
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args()
    if a.out:
        n = build_pack(a.out)
        for f in sorted(os.listdir(a.out)):
            print("  %-40s %10d bytes %s" % (f, os.path.getsize(os.path.join(a.out, f)),
                                              ("%d rows" % n[f]) if f in n else ""))
        return
    target = os.path.join(TASK, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n = build_pack(target)
    for f in sorted(os.listdir(target)):
        print("  %-40s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)),
                                          ("%d rows" % n[f]) if f in n else ""))
    if a.pack_only:
        return
    import deliver
    import metadata
    deliver.main(target, os.path.join(TASK, "golden"), os.path.join(HERE, "figures.json"),
                 os.path.join(TASK, "submission.md"))
    metadata.write(TASK, n)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target])
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target])
    if r1.returncode or r2.returncode:
        sys.exit("checks or verify failed")
    if a.rebuild_dir:
        if os.path.isdir(a.rebuild_dir):
            shutil.rmtree(a.rebuild_dir)
        build_pack(a.rebuild_dir)
        d1, d2 = digest(target), digest(a.rebuild_dir)
        shutil.rmtree(a.rebuild_dir)
        bad = [f for f in d1 if d1.get(f) != d2.get(f)] + [f for f in d2 if f not in d1]
        print("rebuild byte-identical:", not bad, bad)
        if bad:
            sys.exit("rebuild differs")
    if a.zip:
        print("cut", cut_zip(TASK))


if __name__ == "__main__":
    main()
