"""task179 ask layer against the careful solver's routes, on the cut pack.

    python3 task179/generator/ceiling.py [target]

Every route a careful reader takes on each ask, figure by figure, against figures.json: the cracker (lands the call,
runs the hygiene battery, executes every filed rule) takes the most reflexive routes below, and the mirror is the best
response off the call. Pair ceiling on the generated rubric's weights (38 recommendation and components, 7
instruction following, 55 asks; a wrong call keeps about 5)."""
from __future__ import annotations

import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc     # noqa: E402
import common as C   # noqa: E402

FAC_ARC = calc.FAC_ARC


def groups_by(tt, cols):
    act = tt[tt["Class Status"] == "Active"]
    cls = act.drop_duplicates("Class Code")[["Class Code", "Owning Faculty", "Enrolled at Census"]]
    if cols is None:
        g = cls.assign(grp=cls["Class Code"])
    else:
        meet = act[["Class Code"] + cols].drop_duplicates()
        key = meet[cols].astype(str).agg("|".join, axis=1)
        parent = {c: c for c in cls["Class Code"]}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for _, gg in meet.assign(k=key).groupby("k"):
            cs = sorted(gg["Class Code"].unique())
            for c in cs[1:]:
                ra, rb = find(cs[0]), find(c)
                if ra != rb:
                    parent[rb] = ra
        g = cls.assign(grp=cls["Class Code"].map(find))
    grp = g.groupby("grp").agg(fac=("Owning Faculty", "first"), n=("Enrolled at Census", "sum"))
    out = {}
    for f, code in FAC_ARC.items():
        gg = grp[grp["fac"] == f]
        out["ask_groups_s1_2026_%s" % code.lower()] = int(len(gg))
        out["ask_groups_over30_s1_2026_%s" % code.lower()] = int((gg["n"] > 30).sum())
    return out


def continuing_by(d, rule):
    cz = d["census"].copy()
    cz["Y"] = cz["CENSUS_DATE"].map(calc.census_year)
    c6 = cz[(cz["Y"] == 2026) & (cz["STATUS"] == "Enrolled") & (cz["YEAR_OF_STUDY"] >= 2)]
    cat = d["cat"]
    combos = {}
    for _, r in cat[cat["TYPE"] == "Conjoint"].iterrows():
        a, b = r["COMPONENTS"].split(";")
        combos[frozenset((a, b))] = a
    pfac = {r["CODE"]: FAC_ARC[r["OWNING_FACULTY"]] for _, r in cat[cat["TYPE"] == "Programme"].iterrows()}
    out = {}

    def add(f, y):
        k = "ask_continuing_2026_%s_y%d" % (f.lower(), min(y, 4))
        out[k] = out.get(k, 0) + 1
    for sid, g in c6.groupby("STUDENT_ID"):
        g = g.sort_values("ATTEMPT_SEQ")
        progs = list(g["PROGRAMME"])
        y = int(g["YEAR_OF_STUDY"].iloc[0])
        if rule == "attempts":
            for p in progs:
                add(pfac[p], y)
            continue
        if len(progs) == 1:
            add(pfac[progs[0]], y)
        elif rule == "first":
            add(pfac[progs[0]], y)
        elif rule == "latest":
            add(pfac[progs[-1]], y)
        elif rule == "catalogue_latest":
            add(pfac[combos[frozenset(progs)]] if frozenset(progs) in combos else pfac[progs[-1]], y)
        elif rule == "catalogue_first":
            add(pfac[combos[frozenset(progs)]] if frozenset(progs) in combos else pfac[progs[0]], y)
        elif rule == "faculty_field_first":
            add(FAC_ARC[g["FACULTY"].iloc[0]], y)
    return out


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    asks = sorted(k for k in figs if k.startswith("ask_"))
    d = calc.load(target)
    routes = {
        "A class codes": groups_by(d["tt"], None),
        "A room, day, start, teacher": groups_by(d["tt"], ["Room", "Day", "Start", "Teacher"]),
        "A room, day, start": groups_by(d["tt"], ["Room", "Day", "Start"]),
        "A room, day, start, weeks, teacher": groups_by(d["tt"], ["Room", "Day", "Start", "Teaching Weeks", "Teacher"]),
        "B first attempt": continuing_by(d, "first"),
        "B every attempt": continuing_by(d, "attempts"),
        "B latest attempt": continuing_by(d, "latest"),
        "B catalogue, else latest": continuing_by(d, "catalogue_latest"),
        "B catalogue, else first": continuing_by(d, "catalogue_first"),
    }
    print("%-40s %s" % ("route", "figures kept"))
    kept = {}
    for name, r in routes.items():
        ks = [k for k in asks if k in r]
        hit = [k for k in ks if r[k] == figs[k]]
        kept[name] = (len(hit), len(ks))
        print("%-40s %d of %d%s" % (name, len(hit), len(ks), (": " + ", ".join(hit)) if hit else ""))
    # the cracker takes the most each ask allows among the reflexive routes; the mirror is off the call
    bestA = max(v[0] for k, v in kept.items() if k.startswith("A"))
    bestB = max(v[0] for k, v in kept.items() if k.startswith("B"))
    L = (bestA + bestB) / float(len(asks))
    crack = 38 + 7 + 55 * L
    mirror = 5 + 7 + 55 * L
    print("asks %d; worst route keeps A %d, B %d; cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f"
          % (len(asks), bestA, bestB, crack, mirror, (crack + mirror) / 2, 100 * L))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
