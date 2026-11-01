"""R3a measured honestly on the clean truth (11-01 re-check): python3 task307/generator/analyst_test.py.
Guidance 2.1 takes the build network's vehicle-hours from the current regional model on the coded network, and
documentation 6.1 files that model's assignment (user equilibrium, relative gap below 0.000001). The fixed-volume
route holds the no-build loads on each build network; this tests those loads against 6.1's own condition, then
prints the two routes. Not part of make.py: it changes no file in the pack."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import net  # noqa: E402
import params as P  # noqa: E402
import rungs  # noqa: E402
import solve  # noqa: E402

o = solve.run()
links, cap, t0, al, be, tabs = o["links"], o["cap"], o["t0"], o["al"], o["be"], o["tabs"]
asg = net.Assign(links)


def gap(v, c2, od):
    t = t0 * (1 + al * (v / c2) ** be)
    y = asg.aon(t, solve.aggregate(od))
    tot = float(v @ t)
    return (tot - float(y @ t)) / tot


for pr in P.PROJECTS:
    c2 = solve.project_caps(links, cap, pr)
    g = [gap(o["nobuild"][per]["v"], c2, od) for per, od in tabs.items()]
    print("fixed-volume route, %s %s: no-build loads on the build network, relative gap AM %.4f PM %.4f (6.1 files < 0.000001)"
          % (pr["code"], pr["name"] if "name" in pr else "", g[0], g[1]))
R = rungs.routes(o)
for k in ("fixed no-build volumes", "equilibrium (golden)"):
    r = R[k]
    print("%-24s -> %s  %s" % (k, max(r, key=r.get), "  ".join("%s %.0f" % (c, v) for c, v in r.items())))
print("every filed rule executed (2.1 on the coded network, 6.1 user equilibrium, 2.2, 3.1) is the equilibrium route: R3a fails")
