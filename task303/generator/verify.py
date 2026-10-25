"""The independent verifier: reads only target.zip and figures.json, recomputes every owed figure by its own code (no
import of the generator's solve, world or records), and checks the archive's members.

    python3 task303/generator/verify.py <target.zip>
"""
import csv
import datetime as dt
import io
import json
import os
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
HERE = os.path.dirname(os.path.abspath(__file__))
CAND = ("F-112", "F-114", "F-205", "F-208", "F-301", "F-303")
SUBS = {"Pell Creek": ("F-112", "F-114", "F-117"), "Sorrel Hill": ("F-205", "F-208", "F-209"),
        "Byers Mill": ("F-301", "F-303", "F-304"), "Hollow Fork": ("F-411", "F-412", "F-415"),
        "Kettle Run": ("F-521", "F-522", "F-525"), "Willow Crossing": ("F-631", "F-632", "F-636")}
CODE = {"PLC": "Pell Creek", "SRH": "Sorrel Hill", "BYM": "Byers Mill", "HLF": "Hollow Fork", "KTR": "Kettle Run",
        "WLC": "Willow Crossing"}
EXPECT = {"oms_interruptions_2019_2022.csv", "oms_interruptions_2023_2025.csv", "storm_crew_status_2023_2025.csv",
          "major_event_days_2019_2025.csv", "feeder_inventory_2026.xlsx", "storm_hardening_plan_2027.docx",
          "oms_export_notes.txt", "mobile_workforce_export_notes.txt", "commission_order_reliability_2024.pdf",
          "vegetation_work_orders_2017_2026.csv", "line_recloser_settings_2026.xlsx"}


def rd(z, name):
    return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8"))))


def r_(x, u):
    return int(round(x / u)) * u if u >= 1 else round(round(x / u) * u, 1)


def main(zp):
    bad = []
    z = zipfile.ZipFile(zp)
    names = set(z.namelist())
    if names != EXPECT:
        bad.append("archive members %s" % sorted(names ^ EXPECT))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meds = {r["event_date"] for r in rd(z, "major_event_days_2019_2025.csv")}
    T = []
    for r in rd(z, "oms_interruptions_2019_2022.csv"):
        raw = r["DUR_MIN"]
        mins = int(raw) if "." not in raw else int(raw.split(".")[0]) * 60 + int(raw.split(".")[1])
        day = dt.datetime.strptime(r["OUT_DT"], "%m/%d/%Y").date()
        # a trouble crew's handheld ticket (hours and minutes after a point) is dated the day the crew closed it
        for k in range(0, 5 if "." in raw else 1):
            st = dt.datetime.strptime((day - dt.timedelta(days=k)).isoformat() + r["OUT_TM"], "%Y-%m-%d%H:%M"
                                      ).replace(tzinfo=ET)
            if "." not in raw or (st.astimezone(UTC) + dt.timedelta(minutes=mins)).astimezone(ET).date() == day:
                break
        else:
            bad.append("handheld ticket %s closes on no day" % r["TKT_NO"])
        T.append(("F-" + r["FDR"], CODE[r["SUB_CD"]], st, mins, int(r["CUST_OUT"]), r["CAUSE_CD"], r["DEV_TYP"], ""))
    cmap = {"Vegetation": "TREE", "Wind": "WIND", "Wildlife": "ANML", "Lightning": "LTNG", "Equipment failure": "EQUP",
            "Vehicle / public": "VEH", "Unknown": "UNK"}
    dmap = {"Feeder breaker": "CB", "Line recloser": "RCL", "Fuse": "FUS", "Transformer": "TX"}
    restored = {}
    est = dt.timezone(dt.timedelta(hours=-5))
    for r in rd(z, "storm_crew_status_2023_2025.csv"):
        if r["status"] == "Restored":
            # the contract crews' devices keep Eastern standard time all year
            zone = est if r["crew_type"] == "Contract line crew" else ET
            restored[r["oms_interruption_id"]] = dt.datetime.strptime(r["status_time_local"], "%Y-%m-%d %H:%M"
                                                                      ).replace(tzinfo=zone)
    for r in rd(z, "oms_interruptions_2023_2025.csv"):
        s = dt.datetime.strptime(r["interruption_start_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        e = dt.datetime.strptime(r["restoration_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        T.append((r["feeder"], r["substation"], s.astimezone(ET), int((e - s).total_seconds() // 60),
                  int(r["customers_interrupted"]), cmap[r["cause_category"]], dmap[r["protective_device_type"]],
                  r["interruption_id"]))
    # the call: every feeder at the substation opening in the same minute is a loss of the substation's supply
    by = defaultdict(set)
    for t in T:
        by[(t[1], t[2])].add(t[0])
    cmi = defaultdict(int)
    for t in T:
        if t[2].date().isoformat() in meds or set(SUBS[t[1]]) <= by[(t[1], t[2])]:
            continue
        if t[6] in ("CB", "RCL") and t[5] in ("TREE", "WIND", "ANML"):
            cmi[t[0]] += t[4] * t[3]
    got = {f: 0.9 * cmi[f] / 7 for f in CAND}
    win = max(CAND, key=lambda f: got[f])
    if win != fig["call"]["feeder"]:
        bad.append("the call: %s against %s" % (win, fig["call"]["feeder"]))
    for f in CAND:
        if r_(got[f], 100) != fig["candidates"][f]["figure"]:
            bad.append("call figure %s %s against %s" % (f, r_(got[f], 100), fig["candidates"][f]["figure"]))
    if r_(got[win] * 2.10, 1000) != fig["call"]["value"]:
        bad.append("value")
    # ask A: storm days 2023 to 2025, each restored at its crew's Restored time
    a, ac = defaultdict(int), defaultdict(int)
    for t in T:
        if t[7] and t[0] in CAND and t[2].date().isoformat() in meds:
            end = restored.get(t[7])
            m = t[3] if end is None else int((end.astimezone(UTC) - t[2].astimezone(UTC)).total_seconds() // 60)
            a[t[0]] += t[4] * m
            ac[t[0]] += t[4]
    for f in CAND:
        if r_(a[f], 1000) != fig["storm"][f]["cmi"] or r_(a[f] / ac[f], 0.1) != fig["storm"][f]["per"]:
            bad.append("storm %s" % f)
    # ask B: the tap fuses outside the major event days, handheld durations in hours and minutes
    b, bc = defaultdict(int), defaultdict(int)
    for t in T:
        if t[0] in CAND and t[6] == "FUS" and t[2].date().isoformat() not in meds:
            b[t[0]] += t[4] * t[3]
            bc[t[0]] += t[4]
    for f in CAND:
        if r_(b[f] / 7, 10) != fig["taps"][f]["year"] or r_(b[f] / bc[f], 0.1) != fig["taps"][f]["per"]:
            bad.append("taps %s" % f)
    for x in bad:
        print("VERIFY FAIL", x)
    print("verify: %d failures (call %s, %d storm crew restores, %d tickets)" % (len(bad), win, len(restored), len(T)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
