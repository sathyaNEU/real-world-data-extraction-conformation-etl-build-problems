"""The golden answers, computed from the files in task254/target/ alone."""
import os

import pandas as pd

import analysis as A
import pack as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def read(target):
    f = lambda k: os.path.join(target, P.FILES[k])
    rd = lambda k: pd.read_csv(f(k), dtype=str, keep_default_na=False)
    rx = lambda k, **kw: pd.read_excel(f(k), dtype=str, keep_default_na=False, **kw)
    listing, dosage, feed = rd("listing"), rd("dosage"), rd("feed")
    labreg = rx("labreg", sheet_name="register")
    dupreg = rx("dupreg")
    terms = rx("terms", sheet_name="Term list v4")
    changes = rx("terms", sheet_name="Changes v3 to v4")
    pack = A.Pack(listing, dosage, feed, labreg, dupreg, terms, changes)
    sellin, master = rd("sellin"), rd("master")
    calloff = pd.read_excel(f("calloff"), skiprows=5, dtype={"gtin": str, "qty": int})
    pres = A.read_presentations(open(f("xevmpd")).read())
    sup = A.Supply(sellin, calloff, master, pres)
    return pack, sup


def solve(target=None):
    target = target or os.path.join(TASK, "target")
    pack, sup = read(target)
    g = {"windows": {}, "lb": {}, "rates": {}, "counts": {}}
    for r in A.RISKS:
        t = A.tto(pack, r)
        g["windows"][r] = A.cuts(t, "lb")
        g["lb"][r] = {p: A.lb_detail(t, p) for p in (0.8, 0.95)}
        g["counts"][r] = {w: A.case_counts(pack, r, w) for w in ("launch", "interval")}
    g["py"] = {w: sup.patient_years(window=w) for w in ("launch", "interval")}
    g["py_strength"] = {s: sup.patient_years(window="launch", strength=s) for s in (15, 30)}
    for r in A.RISKS:
        g["rates"][r] = {w: 1000.0 * g["counts"][r][w] / g["py"][w] for w in ("launch", "interval")}
    return pack, sup, g


if __name__ == "__main__":
    _, _, g = solve()
    for r in A.RISKS:
        print(r, g["windows"][r], g["counts"][r], {w: round(v, 2) for w, v in g["rates"][r].items()})
    print("PY", {k: round(v, 1) for k, v in g["py"].items()}, {k: round(v, 1) for k, v in g["py_strength"].items()})
