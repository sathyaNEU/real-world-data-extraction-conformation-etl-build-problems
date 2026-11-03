"""The golden figures, computed from the clean truth (world.py). verify.py recomputes them from the shipped files."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

MONTHS = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]


def gap(df):
    r = df.groupby("own")["ric"].mean()
    return 100.0 * (float(r.get(0, np.nan)) - float(r.get(1, np.nan)))


def edge(v, unit):
    """Distance from v to the nearest edge of the cell it prints in, as a fraction of the unit."""
    return (unit / 2.0 - abs(v - round(v / unit) * unit)) / unit


def main_figures(fa):
    f = {}
    for p, lab in (("P1", "2025"), ("P2", "2026")):
        f["region_gap_%s" % lab] = gap(fa[fa.period == p])
        for c in W.COURTS:
            s = fa[(fa.court == c) & (fa.period == p)]
            f["gap_%s_%s" % (c, lab)] = gap(s)
    kb = fa[(fa.court == "KB") & (fa.period == "P2")]
    mag = kb.officer == W.MAGISTRATE
    f["kb_avl_gap"] = gap(kb[kb.during_avl == 1])
    f["kb_other_gap"] = gap(kb[kb.during_avl == 0])
    f["kb_avl_mag_gap"] = gap(kb[(kb.during_avl == 1) & mag])
    f["kb_avl_judges_gap"] = gap(kb[(kb.during_avl == 1) & ~mag])
    f["kb_other_mag_gap"] = gap(kb[(kb.during_avl == 0) & mag])
    f["kb_other_judges_gap"] = gap(kb[(kb.during_avl == 0) & ~mag])
    f["kb_avl_unrepresented"] = int(((kb.during_avl == 1) & (kb.own == 0)).sum())
    f["region_widening"] = f["region_gap_2026"] - f["region_gap_2025"]
    rest = fa[fa.during_avl == 0]
    f["region_widening_rest"] = gap(rest[rest.period == "P2"]) - gap(rest[rest.period == "P1"])
    for c in W.COURTS:
        f["widening_%s" % c] = f["gap_%s_2026" % c] - f["gap_%s_2025" % c]
    kbs = fa[fa.court == "KB"]
    for sess in ("am", "pm"):
        s = kbs[kbs.session == sess]
        f["kb_%s_widening" % sess] = gap(s[s.period == "P2"]) - gap(s[s.period == "P1"])
    f["kb_mag_gap"] = gap(kb[mag])
    f["kb_judges_gap"] = gap(kb[~mag])
    return f


GRADED_MAIN = (["region_gap_2025", "region_gap_2026"] + ["gap_%s_%s" % (c, y) for y in ("2025", "2026")
                                                        for c in W.COURTS]
               + ["kb_avl_gap", "kb_other_gap", "kb_avl_mag_gap", "kb_avl_judges_gap", "kb_other_mag_gap",
                  "kb_other_judges_gap"])


def structure_ok(f):
    others = max(f["widening_%s" % c] for c in ("DN", "AG", "RC"))
    return {
        "kb_leads_court_drill": f["widening_KB"] >= 1.15 * max(others, 0.01),
        "morning_carries_naive_drill": f["kb_am_widening"] >= 1.15 * max(f["kb_pm_widening"], 0.01),
        "magistrate_carries_within_officer": f["kb_mag_gap"] - f["kb_judges_gap"] >= 8.0,
        "avl_split_carries_widening": f["region_widening_rest"] <= 0.25 * f["region_widening"],
        "magistrate_equals_judges_outside": abs(f["kb_other_mag_gap"] - f["kb_other_judges_gap"]) <= 3.0,
        "widening_clear": f["region_widening"] >= 4.0,
        "other_courts_quiet": all(abs(f["widening_%s" % c]) <= 4.5 for c in ("DN", "AG", "RC"))
                              and others <= 0.6 * f["widening_KB"],
    }


def em_month_means(em, kind="golden"):
    """Average days from a District Court's order to the first filing of the report, by the month of the order (the
    standard's section 1 scope: the High Court's orders on cases transferred to it are not the District Courts')."""
    e = em.copy()
    e = e[(e.order_date >= W.P2_START) & (e.order_date <= W.END) & (e.hc == 0)]
    assert (e.filed <= W.EXTRACT).all(), "every District Court order in the year has its report by the extract"
    e["days"] = [(a - b).days for a, b in zip(e["filed"], e["order_date"])]
    e["ym"] = [(d.year, d.month) for d in e["order_date"]]
    return {ym: float(e[e.ym == ym]["days"].mean()) for ym in MONTHS}


def bh_month_nights(place, absn):
    """Occupied nights by month: nights from the first night to the night before leaving, less nights away."""
    nights = {ym: 0 for ym in MONTHS}
    lo, hi = W.P2_START, W.END
    away = set()
    for a in absn.itertuples(index=False):
        for k in range((a.back_date - a.out_date).days):
            away.add((a.placement, a.out_date + dt.timedelta(days=k)))
    for p in place.itertuples(index=False):
        d = p.start
        while d < p.end:
            if lo <= d <= hi and (p.placement, d) not in away:
                nights[(d.year, d.month)] += 1
            d += dt.timedelta(days=1)
    return nights
