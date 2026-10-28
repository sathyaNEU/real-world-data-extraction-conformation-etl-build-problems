"""task464 architecture 8: the ask layer's ceiling, measured on the cut pack.

The cracker (supplemental-stumping Part 1.1) lands the call, runs the hygiene battery and executes every filed
rule it points at. It reads the asking sentence, so it works on the learner-course unit the sentence names,
keyed the way the extract keys it (the learner number and the course reference), keeps the five centres the
site directory lists, and takes each learner-course's planned hours ONCE, from the catalogue. That is the
strongest reading of the asks a response can take without reconstructing the cutover. Modelling it weaker
flatters the ceiling (Part 7), so the weaker reading, summing the hours the rows carry, is printed beside it
and never gated.

  C = 38 + 7 + 55 * Lc     the landed call's score
  S = 5  + 7 + 55 * Ls     the best response off the call
  pair = (C + S) / 2       the ceiling precut.py reads

The asks consume nothing the call's construction produces (checks.py, the separation block), so the response
off the call takes the same ask path as the cracker and Ls equals Lc by construction, not by a second count.
"""
import csv, json, os, sys
import world as W
import answers

_p = answers._p


def naive(sum_rows=False):
    coded, mod, enr, sites = answers.load()
    cat = {c["course_ref"]: c for c in csv.DictReader(open(_p("course_catalogue_2025_26.csv"), encoding="utf-8"))}
    in_scope = {x["site_code"] for x in sites}
    rows = [e for e in enr if e["site_code"] in in_scope]
    tcodes = [t["code"] for t in W.TERMS]
    lc = {}
    for e in rows:
        k = (e["uln"], e["course_ref"])
        d = lc.setdefault(k, {"sites": [], "status": set(), "hrs": []})
        d["sites"].append((e["term_code"], e["site_code"]))
        d["status"].add(e["status"])
        d["hrs"].append(int(e["guided_hours_planned"]))
    a1 = {}
    for area in W.CURRICULUM:
        ks = [k for k in lc if cat[k[1]]["curriculum_area"] == area]
        a1[area] = (sum(sum(lc[k]["hrs"]) for k in ks) if sum_rows
                    else sum(int(cat[k[1]]["planned_guided_hours"]) for k in ks))
    st, cp = {}, {}
    for x in sites:
        started = [k for k, d in lc.items()
                   if min(d["sites"], key=lambda p: tcodes.index(p[0]))[1] == x["site_code"]]
        done = [k for k in started if "completed" in lc[k]["status"]]
        st[x["site_name"]] = len(started)
        cp[x["site_name"]] = round(100.0 * len(done) / len(started), 1)
    return {"hours": a1, "started": st, "completed": cp}


def compare(sum_rows=False):
    g = answers.figures()
    n = naive(sum_rows)
    out = []
    for area in W.CURRICULUM:
        out.append(("ask1 planned guided hours, %s" % area, g["ask1_planned_hours"][area], n["hours"][area], 0.5))
    for k in sorted(g["ask2_started"]):
        out.append(("ask2 learner-courses started, %s" % k, g["ask2_started"][k], n["started"][k], 0.5))
    for k in sorted(g["ask2_completed_pct"]):
        out.append(("ask2 completed share, %s" % k, g["ask2_completed_pct"][k], n["completed"][k], 0.05))
    return [(name, gv, nv, abs(gv - nv) <= tol) for name, gv, nv, tol in out]


def pair_of(rows):
    kept = sum(1 for r in rows if r[3])
    Lc = kept / len(rows)
    Ls = Lc
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    return kept, Lc, Ls, (C + S) / 2


def main():
    rows = compare()
    kept, Lc, Ls, pair = pair_of(rows)
    print("%-48s %10s %10s %s" % ("ask figure", "golden", "cracker", "cracker"))
    for name, gv, nv, hit in rows:
        print("%-48s %10s %10s %s" % (name, gv, nv, "KEEP" if hit else "miss"))
    print()
    print("ask figures: %d, cracker keeps %d" % (len(rows), kept))
    print("Lc %.3f   Ls %.3f (same ask path, asks decoupled)   PAIR CEILING %.1f   (precut allows 60, built to 51)"
          % (Lc, Ls, pair))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Ls))
    weak = compare(sum_rows=True)
    print("weaker reading (hours summed off the rows), not gated: keeps %d of %d, pair %.1f"
          % (pair_of(weak)[0], len(weak), pair_of(weak)[3]))
    json.dump({"ask_figures": len(rows), "cracker_keeps": kept, "Lc": round(Lc, 4),
               "pair_ceiling": round(pair, 2), "mirror_leakage_pct": round(100 * Ls, 2)},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ceiling.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
