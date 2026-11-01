"""Every figure the goldens, the write-up, the checks and the ceiling script use, computed from target/ alone."""
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

import analysis as A
import params as P

QUARTERS = ("Q1", "Q2", "Q3", "Q4")
Q_LABEL = {"Q1": "July to September 2025", "Q2": "October to December 2025", "Q3": "January to March 2026",
           "Q4": "April to June 2026"}


def rhu(x, places=0):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def nearest(x, step):
    return float(Decimal(repr(float(x) / step)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) * step


def compute(tdir):
    pk, res = A.ladder(tdir)
    g = res["golden"]
    rows = []
    pay = defaultdict(list)
    for l in pk.loads:
        u = l["unit"]
        p = pk.payload(l)
        pay[l["grade"]].append(p)
        rows.append(dict(ticket=l["ticket"], date=l["date"], grade=l["grade"], unit=u["Unit"], rego=l["rego"],
                         permit=u["50MAX permit"], tare=float(u["Tare (t)"]), net=l["net"], jas=l["jas"],
                         dens=l["net"] / l["jas"], bunks=pk.cap(u, l["grade"]), new=p))
    a = A.ask_a(tdir, pk)
    b = A.ask_b(tdir)
    F = dict(
        loads=g, total=sum(g.values()), total_500=nearest(sum(g.values()), 500),
        grade_100={k: nearest(v, 100) for k, v in g.items()},
        fy26_loads=len(pk.loads), fy26_tonnes=sum(l["net"] for l in pk.loads),
        fy26_by_grade={k: sum(1 for l in pk.loads if l["grade"] == k) for k in P.GRADE_ORDER},
        plan=dict(pk.plan), plan_total=sum(pk.plan.values()),
        avg_pay={k: sum(v) / len(v) for k, v in pay.items()},
        avg_pay_fy26={k: sum(l["net"] for l in pk.loads if l["grade"] == k) /
                      sum(1 for l in pk.loads if l["grade"] == k) for k in P.GRADE_ORDER},
        permit_share=sum(1 for l in pk.loads if l["unit"]["50MAX permit"] == "Y") / len(pk.loads),
        ladder={k: sum(v.values()) for k, v in res.items()}, ladder_grade=res,
        ask_a=a, ask_a_k={k: rhu(v / 1e3, 0) for k, v in a.items()},
        ask_b=b, ask_b_10={k: nearest(v, 10) for k, v in b.items()},
        rows=rows,
    )
    F["r1_1000"] = nearest(F["ladder"]["R1_permit_units_to_the_new_limit"], 1000)
    F["r2_1000"] = nearest(F["ladder"]["R2_loads_at_the_old_limit_only"], 1000)
    F["r0_1000"] = nearest(F["ladder"]["R0_fleet_average_plus_six"], 1000)
    return F
