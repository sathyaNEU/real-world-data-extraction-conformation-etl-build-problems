"""The graded figures at their asked rounding, computed once from target/ and shared by the goldens, the write-up,
figures.json and the checks."""
import analysis as A

SITES = ["Fend Spit", "Wenning Deep"]
QUARTERS = {1: "October to December 2025", 2: "January to March 2026", 3: "April to June 2026", 4: "July to September 2026"}
METALS = ["Cadmium", "Mercury", "Lead", "Copper"]
PARTS = A.REACH_NAMES + ["Berth pockets"]


def nearest(v, unit):
    return int(round(v / unit)) * unit


def r2(v):
    return round(v + 1e-12, 2)


def compute(tdir):
    g = A.call(tdir)
    rg, info = A.rungs(tdir)
    a, monthly = A.ask_a(tdir)
    b = A.ask_b(tdir)
    out = dict(raw=dict(call=g, rungs=rg, info=info, a=a, monthly=monthly, b=b))
    out["total"] = nearest(g["total"], 50000)
    out["parts"] = {p: nearest(v, 20000) for p, v in g["parts"].items()}
    out["a"] = {(s, q): nearest(v, 1000) for (s, q), v in a.items()}
    out["b"] = {k: r2(v) for k, v in b.items()}
    out["monthly"] = {k: nearest(v, 1000) for k, v in monthly.items()}
    return out


def fmt(n):
    return "{:,}".format(int(n))
