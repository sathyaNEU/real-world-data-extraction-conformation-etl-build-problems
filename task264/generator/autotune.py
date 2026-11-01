"""Design-time: move each provider's effect and each site's invitation miss rate (free parameters of the
world) so the outcome and the 2025-26 participation sit inside their bins; writes them back into the
generator. Never shipped."""
import re, importlib
import common, world, truth

TARGET = {40117: 15.10, 40152: 15.93, 40188: 12.88, 41206: 15.14, 41231: 17.10, 41274: 13.92, 41309: 13.06,
          41355: 15.18, 41388: 13.95, 41402: 12.94}
PART = {40117: 83.8, 40152: 84.8, 40188: 83.8, 41206: 80.8, 41231: 80.2, 41274: 81.2, 41309: 83.8, 41355: 81.2,
        41388: 80.2, 41402: 80.8}


def scores():
    ws = open("world.py").read()
    ws = re.sub(r"NOT_INVITED = \{[^}]*\}", "NOT_INVITED = {" + ", ".join("%d: %.4f" % (k, NI[k]) for k in sorted(NI)) + "}", ws)
    open("world.py", "w").write(ws)
    importlib.reload(world)
    A = world.build_all()
    g, _, _ = truth.golden_truth(A)
    return g, truth.participation_truth(A)


NI = dict(world.NOT_INVITED)
for it in range(4):
    g, pt = scores()
    for p in common.PROVIDERS:
        p["u"] = round(p["u"] + (TARGET[p["key"]] - g[p["key"]]), 2)
        NI[p["key"]] = round(max(0.0, NI[p["key"]] + (pt[p["key"]] - PART[p["key"]]) / 100.0 / 0.9), 4)
    print(it, {k: round(g[k], 2) for k in g}, {k: round(pt[k], 2) for k in pt})
src = open("common.py").read()
for p in common.PROVIDERS:
    src = re.sub(r'(dict\(key=%d,.*?u=)(-?[0-9.]+)' % p["key"], lambda m: m.group(1) + ("%.2f" % p["u"]), src, flags=re.S)
open("common.py", "w").write(src)
ws = open("world.py").read()
ni = "NOT_INVITED = {" + ", ".join("%d: %.4f" % (k, NI[k]) for k in sorted(NI)) + "}"
ws = re.sub(r"NOT_INVITED = \{[^}]*\}", ni, ws)
open("world.py", "w").write(ws)
print(ni)
