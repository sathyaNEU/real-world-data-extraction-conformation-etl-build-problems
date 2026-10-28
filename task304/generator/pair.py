"""The ask layer measured on the cut pack: every careful path's keep of the ten confirmed-cure counts, the cracker
(lands the call, runs the hygiene battery, executes every filed rule) and the mirror (stops at the most attractive
wrong rung), and the pair on Part 0's weights (38 for the recommendation, 7 for instruction-following, 55 for asks).

    python3 task304/generator/pair.py [target]"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV  # noqa: E402


def dispensing_date_only(target):
    """a reader who takes the last pack's dispensing date itself as the last dose"""
    cs = SV.courses(target)
    for c in cs:
        c["last"] = c["last"] - dt.timedelta(days=27)
    t = SV.rna(target)
    out = {}
    for c in cs:
        for h, (a, b) in (("H1", SV.H1), ("H2", SV.H2)):
            if a <= c["last"] <= b and SV.cured(c, t):
                out["%s_%s" % (c["clinic"], h)] = out.get("%s_%s" % (c["clinic"], h), 0) + 1
    return {"%s_%s" % (k, h): out.get("%s_%s" % (k, h), 0) for k in SV.P.CLINICS for h in ("H1", "H2")}


def main(target):
    g = SV.cures(target)
    paths = {
        "cracker: the register's end date as the last dose, migrated courses joined, the pathway's not-detected rule":
            SV.cures(target, last_dose="register"),
        "mirror: the register's end date, every register row a course, a result below 12 IU/mL read as a cure":
            SV.cures(target, last_dose="register", merge=False, cure_words=("Not detected", "Detected <12 IU/mL")),
        "the last pack's dispensing date read as the last dose":
            dispensing_date_only(target),
        "the dispensing route with the go-live's old rows as courses of their own":
            SV.cures(target, merge=False),
        "the dispensing route with a result below 12 IU/mL read as a cure":
            SV.cures(target, cure_words=("Not detected", "Detected <12 IU/mL")),
        "golden": g,
    }
    keep = {}
    for name, d in paths.items():
        keep[name] = sum(d[k] == g[k] for k in g)
        print("%-110s keeps %2d of %d  %s" % (name, keep[name], len(g), " ".join("%d" % d[k] for k in g)))
    names = list(paths)
    Lc, Ls = keep[names[0]] / len(g), keep[names[1]] / len(g)
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    print("cracker on the call %.1f, mirror off the call %.1f: pair ceiling %.1f; mirror leakage %.1f per cent"
          % (C, S, (C + S) / 2, 100 * Ls))
    both = 38 + 7 + 55 * Lc
    print("both responses on the call: pair %.1f" % ((both + 38 + 7 + 55 * Ls) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
