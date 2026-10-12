"""Assemble the world: core draws, names, the three sittings' results, the model fit, then the ask-path
files laid on top (regional boundaries, the 2027 visit plan, the census and the road distances), each drawn
or placed so its figures sit clear of their rounding boundaries."""
import numpy as np

import asks as A
import core
import model as M
import names as NM
import results as R
import world

SEED = 233          # stage 3 seed search, see DESIGN_NOTE.md
SHIFT = 0.47        # the system's level on the scale for this draw (points)


def year5_reading(tables):
    """Participating Year 5 reading results of the three sittings as (school, sitting, score)."""
    import pandas as pd
    out = []
    for j, df in enumerate(tables):
        d = df[(df.year == 5) & (df.test == "RD") & (df.part == "P")]
        out.append(pd.DataFrame({"school": d.school.to_numpy(), "sitting": j, "score": d.score.to_numpy()}))
    return pd.concat(out, ignore_index=True)


def build():
    W = world.build(SEED, SHIFT)
    NM.retitle(W, SEED)
    tables = R.build(W, SEED)
    y5 = year5_reading(tables)
    n, ybar, SSW, N, sq = M.stats(y5)
    f, mean, var, p = M.golden_probs(n, ybar, SSW, N)
    points = (mean < 480).astype(float)
    region, swaps = A.boundary_swaps(W, p, points=points, stu=A.students(W["census"]))
    W["region"] = region
    W["swaps"] = swaps
    stu = A.students(W["census"])
    plan0, near_e, moves = A.plan_hubs(W, p, stu)
    plan, chosen, val = A.choose_moves(W, plan0, moves, p, stu, points=points)
    assert val >= 0.035, val
    W["plan"], W["moves"], W["near_e"] = plan, chosen, near_e
    W["census"], W["census_tune"] = A.tune_census(W, p, plan, region)
    W["road"], W["road_tune"] = A.tune_roads(W, p, plan)
    fitd = {"n": n, "ybar": ybar, "SSW": SSW, "N": N, "sq": sq, "fit": f, "mean": mean, "var": var, "p": p,
            "y5": y5}
    return W, tables, fitd
