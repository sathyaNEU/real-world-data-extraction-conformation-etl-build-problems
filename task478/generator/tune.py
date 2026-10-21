"""Pick each section's pothole stream so the cut pack sits where the design needs it: every section's recorded
potholes per ten lane-miles inside its intended whole-number bin with room to spare (at least a sixth of a unit from
either half), and clear of the program's line. The search reads only the generator's own draws.

    python3 task478/generator/tune.py
"""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def lane_miles(segs):
    out = {}
    for s in segs:
        if not s["turnback"]:
            out[s["sec"]] = out.get(s["sec"], 0.0) + s["length"] * s["lanes"]
    return out


def recorded(no, segs, looks, off, groups, tb):
    """The section's potholes some unit recorded in March, on its roadway as at 31 March."""
    ps = W.section_potholes(no, segs, looks, off, veh_group=groups)
    return sum(1 for d in ps if not tb[d["seg"]] and W.detected(d))


def ok(no, rate):
    whole = W.SEC[no]["whole"]
    return abs(rate - whole) <= 0.30 and abs(rate - W.LINE) >= 0.75


def search(segs, looks, vehicles, span=400):
    tb = {s["seg"]: s["turnback"] for s in segs}
    lm = lane_miles(segs)
    groups = {v["unit"]: v["group"] for v in vehicles}
    pick = {}
    for no in W.ORDER:
        for off in range(span):
            if ok(no, recorded(no, segs, looks, off, groups, tb) / (lm[no] / 10.0)):
                pick[no] = off
                break
        assert no in pick, (no, "no stream in range")
    return pick


def main():
    segs, seg25, _ = W.network()
    veh = W.fleet(segs)
    trav, ign = W.driving(segs, veh)
    looks = W.looks_of(veh, trav)
    pick = search(segs, looks, veh)
    json.dump({str(k): v for k, v in pick.items()}, open(os.path.join(HERE, "tune.json"), "w"), indent=1, sort_keys=True)
    print(pick)


if __name__ == "__main__":
    main()
