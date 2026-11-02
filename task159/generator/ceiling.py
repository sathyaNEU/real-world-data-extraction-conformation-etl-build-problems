"""The cracker and mirror sheets, run on the cut pack (target/). Every ask figure is scored for two responses, a hit
being the same printed value as the golden at the asking sentence's rounding.

cracker: lands the call (the per-block re-cut at 0.90 g/t), then runs the hygiene battery on every ask: near-exact
  duplicate hauls removed, clocks converted to local time, every ball mill tag kept and exact re-sends dropped, each
  refinery line joined to its bar by number and receipt date; it executes what is written and nothing more (each
  truck's payload read from the current fleet sheet, the DCS run state as stored, each line's lot fine gold as the
  bar's).
mirror: stops at the most attractive wrong rung of the call (the reconciliation reports' 0.50 g/t factor on the
  plan's model ounces) and takes each ask to its half-handled stop (dated payloads without the duplicate hauls
  removed; DCS plus the shutdown work orders on a fixed UTC-5 clock; lot fine gold shared by gross weight but
  quartered by statement date).

    python3 ceiling.py <target dir>
"""
import sys

import analysis as A


def rnd(v, u):
    return int(round(v / u)) * u


def asks_sheet(t):
    g = dict(stock=A.stockpile(t), hours=A.mill_hours(t), fine=A.fine_gold(t))
    cr = dict(stock=A.stockpile(t, dedup=True, asof=False), hours=A.mill_hours(t, use_cmms=False),
              fine=A.fine_gold(t, allocate=False))
    mi = dict(stock=A.stockpile(t, dedup=False, asof=True), hours=A.mill_hours(t, local=False),
              fine=A.fine_gold(t, by="stmt"))
    rows = []
    for k in g["stock"]:
        for idx, (lab, u) in enumerate((("t", 1000), ("oz", 100))):
            gv, cv, mv = g["stock"][k][idx], cr["stock"][k][idx], mi["stock"][k][idx]
            rows.append(("stockpile %s %s" % (k, lab), rnd(gv, u), rnd(cv, u), rnd(mv, u)))
    for k in g["hours"]:
        rows.append(("ball mill hours %s" % k, rnd(g["hours"][k], 1), rnd(cr["hours"][k], 1), rnd(mi["hours"][k], 1)))
    for k in g["fine"]:
        rows.append(("fine gold %s" % k, rnd(g["fine"][k], 100), rnd(cr["fine"][k], 100), rnd(mi["fine"][k], 100)))
    return rows


def ceiling(t):
    rows = asks_sheet(t)
    n = len(rows)
    lc = sum(1 for r in rows if r[2] == r[1]) / n
    ls = sum(1 for r in rows if r[3] == r[1]) / n
    m = A.main_call(t)
    call_hit_cracker = rnd(m["golden"], 10000) == rnd(m["D"], 10000)
    call_hit_mirror = rnd(m["R1"], 10000) == rnd(m["golden"], 10000)
    c_score = (38 if call_hit_cracker else 5) + 7 + 55 * lc
    s_score = (38 if call_hit_mirror else 5) + 7 + 55 * ls
    return dict(rows=rows, lc=lc, ls=ls, cracker=c_score, mirror=s_score, pair=(c_score + s_score) / 2,
                mirror_leakage=100 * ls)


if __name__ == "__main__":
    r = ceiling(sys.argv[1])
    print("%-34s %10s %10s %10s %s" % ("ask figure", "golden", "cracker", "mirror", "cracker"))
    for name, g, c, m in r["rows"]:
        print("%-34s %10d %10d %10d %s" % (name, g, c, m, "hit" if c == g else "miss"))
    print("cracker keeps %.1f%% of ask figures, mirror %.1f%%" % (100 * r["lc"], 100 * r["ls"]))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f%%"
          % (r["cracker"], r["mirror"], r["pair"], r["mirror_leakage"]))
