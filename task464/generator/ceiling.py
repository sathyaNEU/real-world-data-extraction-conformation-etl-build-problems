"""task464 architecture 8: the ask layer's ceiling, measured on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every filed rule it points at. For each ask
figure this script computes the figure the cracker's reflex produces and compares it with the golden at the
rounding the asking sentence states. A figure the reflex reproduces is kept; a figure it misses is not.

  C = 38 + 7 + 55 * Lc     the landed call's score
  S = 5  + 7 + 55 * Ls     the best response off the call
  pair = (C + S) / 2       the ceiling precut.py reads
"""
import csv, json, os, sys
import world as W
import answers

_p = answers._p


def naive():
    coded, mod, enr, sites = answers.load()
    cat = {c["course_ref"]: c for c in csv.DictReader(open(_p("course_catalogue_2025_26.csv"), encoding="utf-8"))}
    in_scope = {x["site_code"] for x in sites}
    rows = [e for e in enr if e["site_code"] in in_scope]
    tcodes = [t["code"] for t in W.TERMS]
    out = {}
    # The cracker reads the asking sentence, so it works on the learner-course unit the sentence names. It
    # is modelled at that strength deliberately: a cracker modelled as careless flatters the ceiling, which
    # is the failure supplemental-stumping Part 7 records.
    lc = {}
    for e in rows:
        k = (e["uln"], e["course_ref"])
        d = lc.setdefault(k, {"terms": set(), "sites": [], "status": set(),
                              "area": e["curriculum_area"], "hrs": []})
        d["terms"].add(e["term_code"])
        d["sites"].append((e["term_code"], e["site_code"]))
        d["status"].add(e["status"])
        d["hrs"].append(int(e["guided_hours_planned"]))
    a1 = {}
    for area in W.CURRICULUM:
        ks = [k for k, d in lc.items() if d["area"] == area]
        # the count is right once it is deduped; the hours are taken from the rows, where a two-term course
        # carries the whole course's hours on each of its two rows
        a1[area] = {"learner_courses": len(ks),
                    "planned_hours": sum(sum(lc[k]["hrs"]) for k in ks)}
    out["ask1_curriculum"] = a1
    a2 = {}
    for x in sites:
        started = [k for k, d in lc.items()
                   if min(d["sites"], key=lambda p: tcodes.index(p[0]))[1] == x["site_code"]]
        done = [k for k in started if "completed" in lc[k]["status"]]
        a2[x["site_name"]] = round(100.0 * len(done) / len(started), 1) if started else 0.0
    out["ask2_started_and_completed_pct"] = a2
    a3 = {}
    for i, t in enumerate(W.TERMS[:-1]):
        nxt = tcodes[i + 1]
        a3[t["code"]] = sum(1 for d in lc.values() if t["code"] in d["terms"] and nxt in d["terms"])
    out["ask3_carried_over"] = a3
    return out


def compare():
    g = answers.figures()
    n = naive()
    rowsout = []
    for area in W.CURRICULUM:
        for key, lab, tol in (("planned_hours", "planned guided hours", 0.5),
                              ("learner_courses", "learner-courses", 0.5)):
            gv = g["ask1_curriculum"][area][key]
            nv = n["ask1_curriculum"][area][key]
            rowsout.append(("ask1 %s, %s" % (lab, area), gv, nv, abs(gv - nv) <= tol))
    for k, gv in g["ask2_started_and_completed_pct"].items():
        nv = n["ask2_started_and_completed_pct"][k]
        rowsout.append(("ask2 started and completed, %s" % k, gv, nv, abs(gv - nv) <= 0.05))
    for k, gv in g["ask3_carried_over"].items():
        nv = n["ask3_carried_over"][k]
        rowsout.append(("ask3 carried over, %s" % k, gv, nv, abs(gv - nv) <= 0.5))
    return rowsout


def main():
    rows = compare()
    kept = sum(1 for _, _, _, hit in rows if hit)
    Lc = kept / len(rows)
    Ls = Lc                      # the mirror reads the asks the same way; it differs only on the call
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    pair = (C + S) / 2
    print("%-46s %12s %12s %s" % ("ask figure", "golden", "cracker", "cracker hits"))
    for name, gv, nv, hit in rows:
        print("%-46s %12s %12s %s" % (name, gv, nv, "KEEP" if hit else "miss"))
    print()
    print("ask figures: %d, cracker keeps %d" % (len(rows), kept))
    print("Lc %.3f   C %.1f   S %.1f   PAIR CEILING %.1f   (precut allows 40)" % (Lc, C, S, pair))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Ls))
    json.dump({"ask_figures": len(rows), "cracker_keeps": kept, "Lc": round(Lc, 4),
               "pair_ceiling": round(pair, 2), "mirror_leakage_pct": round(100 * Ls, 2)},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ceiling.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
