"""The pair ceiling, measured on the cut pack: every response row scored figure by figure against the golden at the
prompt's rounding, on the arithmetic 38 (call and components) + 7 (instruction) + 55 (asks).

    python3 task276/generator/ceiling.py            (solves target/ and prints the sheet)
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV

F1 = lambda v: "%.1f" % round(v + 1e-12, 1)


def ask_rows(S):
    """each ask figure under each route: (ask, crossing) -> {route: printed figure}"""
    out = {}
    for n in S["names"]:
        out[("fault", n)] = {r: F1(S["fault"][r][n]) for r in ("lazy", "careful", "full_short_f3", "golden", "long10")}
        out[("hgv", n)] = {r: F1(S["hgv"][r][n]) for r in ("lazy", "f4", "golden")}
    return out


# the routes each response takes on each ask; the cracker and the mirror both take the careful solver's route
RESPONSES = {
    "cracker (lands the call; careful routes)": dict(call=True, fault="careful", hgv="lazy"),
    "mirror (closure model, Station Road; careful routes)": dict(call=False, fault="careful", hgv="lazy"),
    "lazy reader on the call": dict(call=True, fault="lazy", hgv="lazy"),
    "full includer short of F3 and F5": dict(call=True, fault="full_short_f3", hgv="f4"),
}
FINDINGS = {"F1": ("fault", "careful", "full_short_f3"), "F3": ("fault", "full_short_f3", "golden"),
            "F4": ("hgv", "lazy", "f4"), "F5": ("hgv", "f4", "golden")}


def kept(S, rows, fault_route, hgv_route):
    hit = 0
    for (ask, n), v in rows.items():
        route = fault_route if ask == "fault" else hgv_route
        hit += v[route] == v["golden"]
    return hit / float(len(rows))


def lift(S, rows, finding):
    """the ask weight one finding adds to the careful route, the other findings left unmade"""
    ask, base, more = FINDINGS[finding]
    before = after = 0
    for (a, n), v in rows.items():
        if a != ask:
            continue
        if finding == "F3":   # F3 is made on top of F1, F5 on top of F4: the lift of the second finding alone
            before += v["full_short_f3"] == v["golden"]
            after += v["golden"] == v["golden"]
        elif finding == "F5":
            before += v["f4"] == v["golden"]
            after += v["golden"] == v["golden"]
        else:
            before += v[base] == v["golden"]
            after += v[more] == v["golden"]
    return (after - before) / float(len(rows))


def sheet(S, target):
    rows = ask_rows(S)
    out = []
    for name, R in RESPONSES.items():
        L = kept(S, rows, R["fault"], R["hgv"])
        score = (38 if R["call"] else 5) + 7 + 55 * L
        out.append((name, L, score))
    pair = (out[0][2] + out[1][2]) / 2.0
    full_pair = (out[3][2] + out[1][2]) / 2.0
    lifts = {f: lift(S, rows, f) for f in FINDINGS}
    dig = hashlib.sha256()
    for root, _, files in sorted(os.walk(target)):
        for f in sorted(files):
            dig.update(open(os.path.join(root, f), "rb").read())
    return dict(rows=out, pair=pair, full_pair=full_pair, mirror_leak=100 * out[1][1], lifts=lifts,
                digest=dig.hexdigest()[:12], askrows=rows)


def main():
    target = os.path.join(os.path.dirname(HERE), "target")
    S = SV.solve(target)
    C = sheet(S, target)
    print("pack digest", C["digest"])
    for name, L, score in C["rows"]:
        print("  %-55s ask kept %5.1f%%  score %5.1f" % (name, 100 * L, score))
    print("pair ceiling (cracker and mirror) %.1f; with the full includer on the call %.1f" % (C["pair"], C["full_pair"]))
    print("mirror leakage %.1f%% of ask weight" % C["mirror_leak"])
    for f, v in C["lifts"].items():
        print("  lift of %s alone: %.1f%% of ask weight" % (f, 100 * v))
    assert C["pair"] <= 60 and C["mirror_leak"] < 50
    assert max(C["lifts"].values()) <= 1 / 3.0 + 1e-9, C["lifts"]
    return C


if __name__ == "__main__":
    main()
