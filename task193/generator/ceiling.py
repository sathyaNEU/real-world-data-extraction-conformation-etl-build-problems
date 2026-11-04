"""The cracker and mirror sheets, run on the cut pack: each ask figure scored for the careful solver who lands the
call, runs the hygiene battery and executes every filed rule (the cracker), for the solver who stops at the plan's
limits on every background result and handles the field entries the same way (the mirror), and for the full includer
who handles every device. Scores on 38, 7 and 55 so builds compare, with the ask ladders' other stops printed beside
them. Prints the pack's digest so a figure is tied to the pack it was measured on.

The careful route reads the calibration entries (FS-03 section 4 points there), carries the day's serial across the
unpaired sets (FS-03 section 3) and converts what a meter logged at the sample's temperature, so the meter is no longer
what A1 turns on. What it does not do is reconstruct when each sample was collected: the field app marks no sample, it
keeps logging the flow cell while the bottles fill, and the collection minute exists only on the chain of custody in
the laboratory's deliverable, in local time against the app's UTC. No sentence joins the two systems, so the careful
route reads a visit's sample set as its last set before the pump stopped. A2 holds on its own device as well: the
purge starts at the counter of the day's last pump stop, which no filed sentence states."""
import csv
import datetime as dt
import hashlib
import os
import sys

import golden as GD
import world as W


def _rows(tgt, purge_file):
    rows = []
    for r in csv.DictReader(open(os.path.join(tgt, purge_file), encoding="utf-8")):
        r["t"] = dt.datetime.strptime(r["entry_utc"], "%Y-%m-%dT%H:%M:%SZ")
        rows.append(r)
    return rows


def routes(tgt, files):
    days = {d.strftime("%Y-%m-%d") for d in W.EVENTS[W.EVAL]["days"]}
    mode = GD.read_calib(tgt, files)
    coc = GD.read_coc(tgt, files, W.EVENTS[W.EVAL]["days"])
    rows = sorted([r for r in _rows(tgt, files["purge"]) if r["visit_date"] in days], key=lambda r: r["t"])
    first, last_set, at_sample = {}, {}, {}
    mark, day_seen, meter = 0.0, None, ""
    for r in rows:
        if r["visit_date"] != day_seen:
            day_seen, mark, meter = r["visit_date"], 0.0, ""
        if r["remark"] in ("decon rinse", "bottles filled, pump off"):
            mark = float(r["controller_l"])
            continue
        meter = r["meter_sn"] or meter
        r["carried"] = meter
        w = r["location"]
        if w not in first:
            first[w] = (float(r["controller_l"]), mark)
        last_set[w] = r                      # the visit's last set before the pump stopped
        if r["t"] <= coc[w]:
            at_sample[w] = r                 # the set the sample was collected immediately after

    def spc_of(r, how):
        c, T = float(r["spc_us_cm"]), float(r["temperature_c"])
        fix = c / (1 + W.TEMP_COEF * (T - 25))
        if how == "as_logged":
            return round(c)
        if how == "own_serial":
            own = (r["visit_date"], r["meter_sn"])
            return round(fix) if own in mode and not mode[own] else round(c)
        return round(fix) if not mode[(r["visit_date"], r["carried"])] else round(c)

    spc = {"last_set_as_logged": {w: spc_of(r, "as_logged") for w, r in last_set.items()},
           "last_set_carried": {w: spc_of(r, "carried") for w, r in last_set.items()},
           "sample_set_as_logged": {w: spc_of(r, "as_logged") for w, r in at_sample.items()},
           "sample_set_own_serial": {w: spc_of(r, "own_serial") for w, r in at_sample.items()},
           "sample_set_carried": {w: spc_of(r, "carried") for w, r in at_sample.items()}}

    def vol(r, w, base):
        return round((float(r["controller_l"]) - first[w][base]) / W.L_PER_GAL, 1)

    pur = {"last_set_first_set": {w: vol(r, w, 0) for w, r in last_set.items()},
           "last_set_pump_stop": {w: vol(r, w, 1) for w, r in last_set.items()},
           "sample_set_first_set": {w: vol(r, w, 0) for w, r in at_sample.items()},
           "sample_set_pump_stop": {w: vol(r, w, 1) for w, r in at_sample.items()}}
    return spc, pur


def measure(tgt, g, files=None):
    import pack as PK
    files = files or PK.FILES
    spc, pur = routes(tgt, files)
    gs = {w: int(round(v)) for w, v in g["spc"].items()}
    gp = {w: round(v, 1) for w, v in g["purge"].items()}

    def hits_s(route):
        return sum(1 for w in gs if spc[route].get(w) == gs[w])

    def hits_p(route):
        return sum(1 for w in gp if abs(pur[route].get(w, -9) - gp[w]) < 1e-9)

    sheet = {"cracker": ("last_set_carried", "last_set_first_set"),
             "mirror": ("last_set_carried", "last_set_first_set"),
             "full": ("sample_set_carried", "sample_set_pump_stop")}
    keep = {name: (hits_s(s), hits_p(p)) for name, (s, p) in sheet.items()}
    tot = len(gs) + len(gp)
    out = {"A1": {"figures": len(gs), "cracker": keep["cracker"][0], "mirror": keep["mirror"][0], "full": keep["full"][0],
                  "stops": {k: hits_s(k) for k in spc}},
           "A2": {"figures": len(gp), "cracker": keep["cracker"][1], "mirror": keep["mirror"][1], "full": keep["full"][1],
                  "stops": {k: hits_p(k) for k in pur}}}
    Lc = sum(keep["cracker"]) / tot
    Lm = sum(keep["mirror"]) / tot
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    out["cracker_score"] = round(C, 1)
    out["mirror_score"] = round(S, 1)
    out["pair"] = round((C + S) / 2, 1)
    out["mirror_leakage"] = round(100 * Lm, 1)
    out["cracker_keep"] = round(100 * Lc, 1)
    out["full_keep"] = round(100 * sum(keep["full"]) / tot, 1)
    h = hashlib.sha256()
    for fn in sorted(os.listdir(tgt)):
        h.update(open(os.path.join(tgt, fn), "rb").read())
    out["pack_digest"] = h.hexdigest()[:16]
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import pack as PK
    tgt = os.path.join(os.path.dirname(here), "target")
    g = GD.compute(tgt, PK.FILES)
    m = measure(tgt, g)
    for k, v in m.items():
        print(k, v)
