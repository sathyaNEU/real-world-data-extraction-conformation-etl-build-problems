"""The ask sheet's measurement on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every
filed rule it points at) and the mirror (the strongest response off the call; the asks are decoupled from the call, so
it reads them as the cracker does), each ask figure scored against the golden at half a unit of its rounding.

    python3 task273/generator/cracker.py [target]

Ask A, the people killed or seriously injured in the crashes each use's drivers caused, 2021 to 2025. The cracker
attributes every kind of crash to the at-fault driver's use, checks the persons file's key (crash, unit, person number:
no repeats), takes deaths from the state's 30-day register (the cost note's definition of a fatal crash) and adds the
persons recorded A. It never notices that a person listed again in the same seat of the same unit is one person on a
later report.
Ask B, the cost of those crashes at the Department's unit costs. The cracker costs each crash once at its most severe
injury as the crashes file's CRASH_SEVERITY gives it, raised to K where the register holds a death. It never notices
that the crash-level severity is the first report's while the persons file carries the later ones.
Stops printed beside it: the persons file read row by row, the latest record per seat without the register, the most
severe person row per crash."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN   # noqa: E402
import common as K      # noqa: E402
import pack as P        # noqa: E402


def people_paths(D):
    ps = P.persons(D.target)
    fp, dead = AN.final_persons(D)
    reg = {}
    for (cid, unit, ptype, age, sex) in dead:
        reg[cid] = reg.get(cid, 0) + 1
    count = {
        "rows": lambda cid: sum(1 for p in ps.get(cid, ()) if p["sev"] in ("K", "A")),
        "rows_register": lambda cid: reg.get(cid, 0) + sum(1 for p in ps.get(cid, ()) if p["sev"] == "A"),
        "latest_no_register": lambda cid: sum(1 for p in fp.get(cid, ()) if p["sev"] in ("K", "A")),
        "golden": lambda cid: sum(1 for p in fp.get(cid, ()) if p["final"] in ("K", "A")),
    }
    out = {}
    for name, fn in count.items():
        t = {u: 0 for u in K.CODES}
        for cid, c in D.cr.items():
            uses = AN.caused_by(c)
            if uses:
                n = fn(cid)
                for u in uses:
                    t[u] += n
        out[name] = t
    return out


def cost_paths(D):
    ps = P.persons(D.target)
    fp, dead = AN.final_persons(D)
    cost = P.costs(D.target)
    dead_c = {d[0] for d in dead}
    out = {}
    for name in ("crash_severity", "crash_severity_register", "max_rows", "golden"):
        tot = {u: 0 for u in K.CODES}
        for cid, c in D.cr.items():
            uses = AN.caused_by(c)
            if not uses:
                continue
            if name == "crash_severity":
                sev = c["sev"]
            elif name == "crash_severity_register":
                sev = "K" if cid in dead_c else c["sev"]
            elif name == "max_rows":
                sev = min((p["sev"] for p in ps.get(cid, ())), key="KABCO".index, default="O")
                if cid in dead_c:
                    sev = "K"
            else:
                sev = min((p["final"] for p in fp.get(cid, ())), key="KABCO".index, default="O")
            for u in uses:
                tot[u] += cost[sev]
        out[name] = {u: AN.half_up(v / 1e6, 1) for u, v in tot.items()}
    return out


def score(target):
    D = AN.Data(target)
    pp = people_paths(D)
    cp = cost_paths(D)
    res = {}
    for name, t in pp.items():
        res["A:" + name] = sum(1 for u in K.CODES if t[u] == pp["golden"][u])
    for name, c in cp.items():
        res["B:" + name] = sum(1 for u in K.CODES if abs(c[u] - cp["golden"][u]) <= 0.05)
    hits = res["A:rows_register"] + res["B:crash_severity_register"]
    n = 2 * len(K.CODES)
    lc = hits / n
    return dict(paths=res, people=pp, cost=cp, cracker_hits=hits, n=n, lc=lc,
                pair_ceiling=((38 + 7 + 55 * lc) + (5 + 7 + 55 * lc)) / 2.0, mirror_leakage_pct=100.0 * lc)


if __name__ == "__main__":
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    s = score(T)
    for k, v in s["paths"].items():
        print("%-28s hits %d of 7" % (k, v))
    for name, t in s["people"].items():
        print("A %-26s %s" % (name, [t[u] for u in K.CODES]))
    for name, c in s["cost"].items():
        print("B %-26s %s" % (name, [c[u] for u in K.CODES]))
    print("cracker keeps %d of %d ask figures; pair ceiling %.1f; mirror leakage %.1f per cent (decoupled asks: the "
          "mirror reads them as the cracker does)" % (s["cracker_hits"], s["n"], s["pair_ceiling"],
                                                      s["mirror_leakage_pct"]))
