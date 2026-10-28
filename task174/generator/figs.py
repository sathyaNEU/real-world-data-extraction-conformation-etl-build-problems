"""Every figure the write-up, the goldens and the checks state, computed once from solve.py's output on the pack."""
import json

import params as P

SCHOOL = {s[0]: s for s in P.SCHOOLS}


UNIT_R = 250          # failed checks are stated to the nearest 250


def r100(x, unit=UNIT_R):
    return int(unit * int((x + unit / 2.0) // unit))


def r1(x):
    return float("%.1f" % (int(x * 10 + 0.5) / 10.0))


def compute(out):
    m = out["model"]
    tot, by = out["tot"], out["by_len"]
    N = out["chosen"]
    F = {
        "places": P.PLACES,
        "lengths": list(P.LENGTHS),
        "chosen": N,
        "check": P.CHECK, "pass_at": P.PASS_AT,
        "total_raw": {str(k): round(v, 3) for k, v in tot.items()},
        "total": {str(k): r100(v) for k, v in tot.items()},
        "unit_raw": {sb: round(v, 3) for sb, v in by[N].items()},
        "unit": {sb: r100(v) for sb, v in by[N].items()},
        "unit_all_raw": {str(k): {sb: round(v, 3) for sb, v in by[k].items()} for k in P.LENGTHS},
        "sigma": round(m["sigma"], 4),
        "on_roll": len(out["pack"].on_roll),
        "slopes": {sb: round(float(m["slopes"][0][i]), 4) for sb, i in
                   ((b[0], j) for j, b in enumerate(P.SKILL_BUILDERS))},
        "carry": {sb: round(float(m["slopes"][1][j] / m["slopes"][0][j]), 3) for j, sb in
                  ((j, b[0]) for j, b in enumerate(P.SKILL_BUILDERS))},
        "problems": {code: {sb: int(v) for sb, v in units.items()} for code, units in out["problems"].items()},
        "problems_total": int(sum(sum(u.values()) for u in out["problems"].values())),
        "rounding": UNIT_R,
        "spring_units": [int(sb) for sb in P.SPRING],
        "school_names": {code: SCHOOL[code][1] for code in SCHOOL},
    }
    F["headroom"] = P.PLACES - F["total"][str(N)]
    F["short_by"] = F["total"][str(min(P.LENGTHS))] - P.PLACES
    return F


def write(F, path):
    with open(path, "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True)
        fh.write("\n")
