"""The 2024 ask: each region's 2024 completed interviews, estimate and standard error on the regions as they stand
since the reorganisation, under the golden handling of Northmark's codes and under each careful-path handling.

Handlings of a 2024 case's area code (the code in force in Northmark's system on the day the case was assigned):
  golden        cases assigned before 22 April 2024 carry the pre-2024 code, later cases the new code
  old_if_valid  a code the pre-2024 numbering holds is read as pre-2024, any other as new (the battery's repair)
  split_apr1    cases assigned before 1 April 2024 (the reorganisation's date) read as pre-2024, later as new
  split_apr1_iv the same split on the disposition date
  all_old       every 2024 code read as pre-2024 (the weights file's numbering), codes it lacks dropped
  all_new       every 2024 code read as new
"""
import datetime as dt

import numpy as np

import estim as E
import world as W

HANDLINGS = ["golden", "old_if_valid", "split_apr1", "split_apr1_iv", "all_old", "all_new"]
EFFECTIVE = dt.date(2024, 4, 1)


def maps(world):
    old2area = {a["old_code"]: a for a in world["areas"]}
    new2area = {a["new_code"]: a for a in world["areas"]}
    return old2area, new2area


def resolve(code, assigned, outcome_date, handling, old2area, new2area):
    if handling == "golden":
        return (old2area if assigned < W.NORTHMARK_SWITCH else new2area).get(code)
    if handling == "old_if_valid":
        return old2area.get(code) or new2area.get(code)
    if handling == "split_apr1":
        return (old2area if assigned < EFFECTIVE else new2area).get(code)
    if handling == "split_apr1_iv":
        return (old2area if outcome_date < EFFECTIVE else new2area).get(code)
    if handling == "all_old":
        return old2area.get(code)
    if handling == "all_new":
        return new2area.get(code)
    raise ValueError(handling)


def rows_2024(world, handling, code_of):
    """Per new region, the analysis rows (as estim expects) built from the 2024 cases read under the handling.

    code_of(case) gives the code the case carries in the export."""
    old2area, new2area = maps(world)
    comp = {}
    for c in world["cases"][2024]:
        if c["cls"] not in (W.COMPLETE, W.PROXY):
            continue
        a = resolve(code_of(c), c["assigned"], c["outcome_date"], handling, old2area, new2area)
        if a is None:
            continue
        comp.setdefault(id(a), (a, []))[1].append(c)
    out = {r: [] for r in (1, 2, 3, 4, 5)}
    for key in sorted(comp, key=lambda k: comp[k][0]["new_code"]):
        a, cs = comp[key]
        m_all = len(cs)
        wt = a["design_weight"] * a["occupied"][2024] / m_all
        ys = np.array([c["y"] for c in cs if W.usable(c)], float)
        out[a["new_region"]].append(dict(code=a["new_code"], stratum=a["stratum"], m_all=m_all, w=wt, y=ys))
    return out


def figures_2024(world, handling, code_of):
    rows = rows_2024(world, handling, code_of)
    res = {}
    for r in (1, 2, 3, 4, 5):
        p, v = E.design_var(rows[r])
        res[r] = dict(completes=sum(x["m_all"] for x in rows[r]), est=100 * p, se=100 * np.sqrt(v))
    return res
