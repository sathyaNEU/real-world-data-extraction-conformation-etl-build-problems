"""Scales each link's AADT (world.LINKS) until the golden NOx per mile lands at world.DESIRED, then prints every
route.     python3 tune.py [iterations]"""
import importlib
import re
import sys

import numpy as np

import methods as M
import sources as S
import world as W


def clean_inputs(x):
    """The estimators' inputs from the clean truth: stations' daily totals (every class at the classifying ones) and
    each link's two count days."""
    st = {}
    for s, v in x["stations"].items():
        d = {"ALL": {day: sum(v[c][i] for c in W.CLASSES) for i, day in enumerate(W.DAYS)}}
        if W.STATIONS[s][5]:
            for c in W.CLASSES:
                d[c] = {day: v[c][i] for i, day in enumerate(W.DAYS)}
        st[s] = d
    reg = {s: {"classifies": W.STATIONS[s][5]} for s in W.STATIONS}
    cnt = {}
    for k, v in x["links"].items():
        i = W.DAYS.index(W.COUNT_DAY[k])
        cnt[k] = {c: {W.DAYS[i]: v[c][i], W.DAYS[i + 1]: v[c][i + 1]} for c in W.CLASSES}
    return st, reg, cnt


def main(it):
    for _ in range(it):
        x = S.world(np.random.default_rng(W.SEED))
        g = M.nox(M.estimate(*clean_inputs(x)))
        src = open(W.__file__).read()
        links = {}
        for k, (name, rt, a, su, cu) in W.LINKS.items():
            na = int(round(a * W.DESIRED[k] / g[k], -1))
            links[k] = (name, rt, na, su, cu)
            src = re.sub(r'("%s": \("[^"]+", "%s", )\d+' % (k, rt), r"\g<1>%d" % na, src)
        open(W.__file__, "w").write(src)
        W.LINKS.clear()
        W.LINKS.update(links)
    x = S.world(np.random.default_rng(W.SEED))
    inp = clean_inputs(x)
    r = {"truth": S.truth(x)}
    for route in ("golden", "textbook", "raw", "month"):
        r[route] = M.nox(M.estimate(*inp, route=route))
    for how in ("cell", "sep"):
        for a in ("mean", "aashto"):
            for cf in ("classifying", "all"):
                r["g-%s-%s-%s" % (how, a, cf)] = M.nox(M.estimate(*inp, "golden", how, a, cf))
        r["t-" + how] = M.nox(M.estimate(*inp, "textbook", how))
    for k in W.LINKS:
        print(k, " ".join("%s %.2f" % (n[:10], r[n][k]) for n in ("truth", "golden", "textbook", "g-sep-mean-classifying",
                                                                    "g-sep-aashto-all", "t-sep")))
    for n in r:
        print("%-26s %s" % (n, M.designated(r[n])))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
