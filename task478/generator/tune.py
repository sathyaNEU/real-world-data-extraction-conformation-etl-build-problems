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


def recorded_march(no, segs, looks, off, groups, tb):
    """As recorded(), counting only potholes some unit saw on a pass in March, district local time."""
    ps = W.section_potholes(no, segs, looks, off, veh_group=groups)
    return sum(1 for d in ps if not tb[d["seg"]] and any(W.local(p["enter"]).month == 3 for u in d["seen"]
                                                          for p in d["seen"][u]))


def ok(no, rate):
    whole = W.SEC[no]["whole"]
    return abs(rate - whole) <= 0.30 and abs(rate - W.LINE) >= 0.75


def search(segs, looks, vehicles, span=400):
    tb = {s["seg"]: s["turnback"] for s in segs}
    lm = lane_miles(segs)
    groups = {v["unit"]: v["group"] for v in vehicles}
    pick, counts = {}, set()
    for no in W.ORDER:
        for off in range(span):
            n = recorded(no, segs, looks, off, groups, tb)
            if ok(no, n / (lm[no] / 10.0)) and recorded_march(no, segs, looks, off, groups, tb) not in counts:
                pick[no] = off
                counts.add(recorded_march(no, segs, looks, off, groups, tb))
                break
        assert no in pick, (no, "no stream in range")
    return pick


# the latency draws: the first stream whose patrol phones in Fenwick Gap, Grisholt and Oxbrae run long, the design's
# need (the single-distance and fleet-latency rungs end off the golden at every distance, checks.py)
LONG = {402: 1.55, 404: 1.65, 410: 1.60}


def lat_stream(segs):
    for k in range(40000):
        W.LAT_STREAM = k
        veh = W.fleet(segs)
        lat = {v["home"]: v["lat"] for v in veh if v["group"] == "PATROL"}
        if all(lat[no] >= x for no, x in LONG.items()):
            return k
    raise AssertionError("no latency stream")


def main():
    segs, seg25, _ = W.network()
    k = lat_stream(segs)
    W.LAT_STREAM = k
    veh = W.fleet(segs)
    trav, ign = W.driving(segs, veh)
    looks = W.looks_of(veh, trav)
    pick = search(segs, looks, veh, span=1500)
    out = {str(n): v for n, v in pick.items()}
    out["lat_stream"] = k
    json.dump(out, open(os.path.join(HERE, "tune.json"), "w"), indent=1, sort_keys=True)
    print(out)


if __name__ == "__main__":
    main()
