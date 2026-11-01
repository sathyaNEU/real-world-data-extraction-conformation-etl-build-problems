"""Design-time: move each provider's effect (a free parameter of the world) so the full-population
outcome sits mid-bin; writes the effects back into common.py. Never shipped."""
import re, importlib
import common, world, truth

TARGET = {40117: 15.10, 40152: 15.93, 40188: 12.88, 41206: 15.14, 41231: 17.10, 41274: 13.92, 41309: 13.06,
          41355: 15.18, 41388: 13.95, 41402: 12.94}


def scores():
    importlib.reload(world)
    A = world.build_all()
    g, _, _ = truth.golden_truth(A)
    return g


for it in range(3):
    g = scores()
    for p in common.PROVIDERS:
        p["u"] = round(p["u"] + (TARGET[p["key"]] - g[p["key"]]), 2)
    print(it, {k: round(g[k], 3) for k in g})
src = open("common.py").read()
for p in common.PROVIDERS:
    src = re.sub(r'(dict\(key=%d,.*?u=)(-?[0-9.]+)' % p["key"], lambda m: m.group(1) + ("%.2f" % p["u"]), src, flags=re.S)
open("common.py", "w").write(src)
print({p["key"]: p["u"] for p in common.PROVIDERS})
