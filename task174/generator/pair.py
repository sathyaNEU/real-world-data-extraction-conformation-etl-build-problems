"""The cracker and mirror sheets for the ask, run on the cut pack (target/), and the pair ceiling.

The cracker lands the call, runs the hygiene battery (account-to-student link, staff accounts out, UTC put on Eastern
time) and executes every filed rule; for the ask it attributes each problem to the school the export's own row
carries. The mirror stops at the homework replay on the call and counts the export's rows by school_code without
the link. A cell is kept when the figure is exact (the ask is in whole problems). The archive route (each problem at
the school the enrollment history shows on the day) is the golden; it is printed as a reachable route, not as the
cracker.

    python3 task174/generator/pair.py [target]
"""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402
import solve as SV  # noqa: E402


def routes(target):
    pk = SV.Pack(target)
    sp = SV.spells(pk)
    crack = {s[0]: {sb: 0 for sb in P.SPRING} for s in P.SCHOOLS}
    mirror = {s[0]: {sb: 0 for sb in P.SPRING} for s in P.SCHOOLS}
    archive = {s[0]: {sb: 0 for sb in P.SPRING} for s in P.SCHOOLS}
    for r in SV.read_csv(pk.f["log_2026"]):
        sb = pk.sb_of_ref[r["assignment_ref"]]
        if sb not in P.SPRING:
            continue
        mirror[r["school_code"]][sb] += 1
        sid = pk.student_of.get(r["student_user_id"])
        if sid is None:
            continue
        crack[r["school_code"]][sb] += 1
        day = dt.datetime.fromisoformat(r["started_utc"].replace("Z", "+00:00")).astimezone(SV.EAST).date()
        at = [c for c, a, b in sp.get(sid, []) if a <= day <= b]
        if at:
            archive[at[0]][sb] += 1
    return crack, mirror, archive


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    crack, mirror, archive = routes(target)
    cells = [(c, sb) for c in sorted(F["problems"]) for sb in P.SPRING]
    kept = lambda R: sum(1 for c, sb in cells if R[c][sb] == F["problems"][c][sb])
    kc, km, ka = kept(crack), kept(mirror), kept(archive)
    Lc, Lm = kc / float(len(cells)), km / float(len(cells))
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    print("cells %d | cracker keeps %d | mirror keeps %d | archive route keeps %d" % (len(cells), kc, km, ka))
    print("Pair ceiling: %.1f  (cracker %.1f on the call, mirror %.1f off it)" % ((C + S) / 2, C, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * Lm))
    print("| School | Cracker (export school_code) | Golden (school attended that day) | Cracker misses |")
    print("|---|---|---|---|")
    for c in sorted(F["problems"]):
        cr = "/".join(str(crack[c][sb]) for sb in P.SPRING)
        go = "/".join(str(F["problems"][c][sb]) for sb in P.SPRING)
        miss = all(crack[c][sb] != F["problems"][c][sb] for sb in P.SPRING)
        print("| %s | %s | %s | %s |" % (c, cr, go, "yes" if miss else "keeps %d" % sum(
            crack[c][sb] == F["problems"][c][sb] for sb in P.SPRING)))
    return (C + S) / 2, 100 * Lm, kc


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
