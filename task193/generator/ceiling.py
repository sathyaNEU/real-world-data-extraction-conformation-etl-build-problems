"""The cracker and mirror sheets, run on the cut pack: each ask figure scored for the careful solver who lands the
call and runs the hygiene battery (the cracker), for the solver who stops at the plan's limits on every background
result (the mirror), and for the full includer who handles every device but the second. Scores on 38, 7 and 55 so
builds compare. Prints the pack's digest so a figure is tied to the pack it was measured on."""
import csv
import datetime as dt
import hashlib
import os
import sys

import world as W


def _rows(tgt, purge_file):
    rows = []
    for r in csv.DictReader(open(os.path.join(tgt, purge_file), encoding="utf-8")):
        r["t"] = dt.datetime.strptime(r["entry_utc"], "%Y-%m-%dT%H:%M:%SZ")
        rows.append(r)
    return rows


def routes(tgt, purge_file):
    days = {d.strftime("%Y-%m-%d") for d in W.EVENTS[W.EVAL]["days"]}
    rows = sorted([r for r in _rows(tgt, purge_file) if r["visit_date"] in days], key=lambda r: r["t"])
    first, spc_log, spc_inc, pur_crack, pur_inc = {}, {}, {}, {}, {}
    mark, day_seen = 0.0, None
    for r in rows:
        if r["visit_date"] != day_seen:
            day_seen, mark = r["visit_date"], 0.0
        if r["remark"] in ("decon rinse", "bottles filled, pump off"):
            mark = float(r["controller_l"])
            continue
        w = r["location"]
        if w not in first:
            first[w] = (float(r["controller_l"]), mark)
        if r["remark"] == "sample collected":
            c = float(r["spc_us_cm"])
            spc_log[w] = round(c)
            if r["meter_sn"] == W.RENTAL_UNCOMP:
                spc_inc[w] = round(c / (1 + W.TEMP_COEF * (float(r["temperature_c"]) - 25)))
            else:
                spc_inc[w] = round(c)
            end = float(r["controller_l"])
            pur_crack[w] = round((end - first[w][0]) / W.L_PER_GAL, 1)
            pur_inc[w] = round((end - first[w][1]) / W.L_PER_GAL, 1)
    return {"cracker": (spc_log, pur_crack), "mirror": (spc_log, pur_crack), "full": (spc_inc, pur_inc)}


def measure(tgt, g, purge_file=None):
    import pack as PK
    purge_file = purge_file or PK.FILES["purge"]
    R = routes(tgt, purge_file)
    gs = {w: int(round(v)) for w, v in g["spc"].items()}
    gp = {w: round(v, 1) for w, v in g["purge"].items()}
    out = {}
    tot = len(gs) + len(gp)
    keep = {}
    for name, (s, p) in R.items():
        a1 = sum(1 for w in gs if s.get(w) == gs[w])
        a2 = sum(1 for w in gp if abs(p.get(w, -9) - gp[w]) < 1e-9)
        keep[name] = (a1, a2)
    out["A1"] = {"figures": len(gs), "cracker": keep["cracker"][0], "mirror": keep["mirror"][0], "full": keep["full"][0]}
    out["A2"] = {"figures": len(gp), "cracker": keep["cracker"][1], "mirror": keep["mirror"][1], "full": keep["full"][1]}
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
    import golden as GD
    import pack as PK
    tgt = os.path.join(os.path.dirname(here), "target")
    g = GD.compute(tgt, PK.FILES)
    m = measure(tgt, g)
    for k, v in m.items():
        print(k, v)
