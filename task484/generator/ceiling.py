"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1).

    python3 task484/generator/ceiling.py

The cracker lands the call, runs the hygiene battery and executes every filed rule: it counts the registry's
appliances in place in the 2014 season on the 2020 boundaries following each re-registration's predecessor id, and
builds each county's remainder from the tool's named ACS release with each block group's housing units outside the
areas. The mirror stops at the default rung (the survey's class means carried back) and does everything else as the
cracker does. A naive handling (every registry row counted, the latest ACS release, whole block groups) is printed
beside them. Each graded ask figure in submission.md's Deliverable Answers is scored against figures.json."""
import collections
import csv
import json
import os
import re

from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")


def rows(name):
    with open(os.path.join(T, name), newline="") as f:
        return list(csv.DictReader(f))


def ask_a(chain):
    scc = {x["registry_device_type"]: x["scc"] for x in rows("scc_crosswalk_rwc.csv")}
    area20 = {x["parcel_number"]: x["area_2020_boundary"] for x in rows("parcel_area_crosswalk.csv")}
    n = collections.Counter()
    for x in rows("wood_device_registry_2026-06-30.csv"):
        if chain and x["predecessor_id"]:
            continue
        if int(x["year_installed"]) <= 2014 and not x["replaces_device_id"] and area20.get(x["parcel_number"]):
            n[area20[x["parcel_number"]], scc[x["device_type"]]] += 1
    return n


def ask_b(rule, split):
    text = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "state_rwc_tool_method_note.pdf")).pages)
    text = text.replace("\n", " ")
    sec = float(re.search(r"secondary heat source are ([\d.]+) times", text).group(1))
    sccs = {x["description"].replace("Woodstove: ", ""): x["scc"] for x in rows("scc_crosswalk_rwc.csv")}
    ef = {x["scc"]: float(x["factor"]) for x in rows("emission_factors_rwc_2023.csv") if x["pollutant"] == "PM2.5"}
    pel = [s for d, s in sccs.items() if d.startswith("pellet")][0]
    tool = {}
    for name, s in sccs.items():
        m = re.search(re.escape(name) + r" (\d\.\d\d) (\d\.\d\d) (\d+\.\d) (\d+\.\d)", text)
        tool[s] = tuple(float(v) for v in m.groups())
    acs = rows("acs_b25040_blockgroups_2019_2023.csv" if rule else "acs_b25040_blockgroups_2020_2024.csv")
    hu = collections.defaultdict(lambda: [0, 0])
    for x in rows("assessor_housing_units_by_block_group_2025.csv"):
        hu[x["block_group"]][0 if x["maintenance_area_2020"] else 1] += int(x["housing_units"])
    out = collections.Counter()
    for x in acs:
        g = x["GEO_ID"][-12:]
        county = re.search(r", (\w+) County", x["NAME"]).group(1)
        inside, outside = hu[g]
        share = outside / (inside + outside) if split else (1.0 if outside > inside else 0.0)
        main = int(x["B25040_008E"]) * share
        for s, (sp, ss, up, us) in tool.items():
            use = main * sp * up + main * sec * ss * us
            wood = use if s == pel else use * 1.163
            out[county, s] += wood * ef[s] / 2000
    return out


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ga = {k: v["registry"] for k, v in figs["ask_a"].items()}
    gb = {k: v["pm"] for k, v in figs["ask_b"].items()}

    def score(a, b):
        ka = sum(1 for k, v in ga.items() if a.get(tuple(k.split(".")), -1) == v)
        kb = sum(1 for k, v in gb.items() if abs(round(b.get(tuple(k.split(".")), -99) + 1e-9, 1) - v) < 0.05)
        return ka, kb

    total = len(ga) + len(gb)
    ck = score(ask_a(True), ask_b(True, True))
    nk = score(ask_a(False), ask_b(False, False))
    lc = sum(ck) / total
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * lc            # the mirror misses the call and handles the asks as the cracker does
    print("ask figures: %d registry counts (ask A), %d remainder cells (ask B), %d in all" % (len(ga), len(gb), total))
    print("cracker keeps ask A %d, ask B %d: %.1f per cent of ask weight; scores %.1f" % (ck + (100 * lc, C)))
    print("mirror (default rung) keeps the same: %.1f per cent; scores %.1f" % (100 * lc, S))
    print("naive handling keeps ask A %d, ask B %d" % nk)
    print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % ((C + S) / 2, 100 * lc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
