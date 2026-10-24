"""The placement from the pack: each unit's FY2028 weekly backfill need (FY2026's off-post hours by fiscal week, plus
the position control's vacant lines until their first shift on post and their new holders' off-post hours after it),
cut at its fifth-heaviest week, over the hours a relief position's holder works on post in an average week. The
golden reads that holder as what it will be, an entry-class graduate in the first year on post, from the July 2025
classes' first year; the rungs read it, or the need, otherwise."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import pack as PK

OFF = PK.OFF_POST
GOLDEN = "G"
FAMILY = ("G", "G_unit", "G_class", "G_first", "G_ratios", "G_none", "G_avg")
RUNGS = ("mean", "R1", "R2t", "R2", "R3", "R4", "R5", "R6")
DEFAULT = "R2t"


def q5(x):
    return float(np.sort(x)[::-1][K.K_WEEKS])


def july25(title=None, unit=None):
    def sel(r, e):
        if e is None or not e["academy_class"].endswith(" 2025-1"):
            return False
        if title and e["title_code"] != title:
            return False
        if unit and r["unit_code"] != unit:
            return False
        return True
    return sel


def first_year(title):
    """every holder in the first year on post in FY2026: the July 2025 classes and the mid-year classes"""
    def sel(r, e):
        return (e is not None and e["title_code"] == title and e["academy_class"] != ""
                and e["hire_date"] >= "2025-01-01")
    return sel


def mean_of_ratios(pk, title):
    per = {}
    for r in pk.roster:
        e = pk.emp.get(r["employee_id"]) if r["employee_id"] else None
        if e is None or e["academy_class"] != "%s 2025-1" % title:
            continue
        s, o = per.get(e["employee_id"], (0.0, 0.0))
        h = float(r["scheduled_hours"])
        per[e["employee_id"]] = (s + h, o + (h if r["cat"] in OFF else 0.0))
    return float(np.mean([1 - o / s for s, o in per.values()]))


def components(pk):
    out = {}
    a1t = {t: pk.availability(july25(title=t)) for t in K.TITLE_ORDER}
    a1c = pk.availability(july25())
    a1f = {t: pk.availability(first_year(t)) for t in K.TITLE_ORDER}
    # the title's officers as the HR extract's current rows name them (a reader's dictionary join)
    at = {t: pk.availability(lambda r, e, t=t: e is not None and e["title_code"] == t) for t in K.TITLE_ORDER}
    a1m = {t: mean_of_ratios(pk, t) for t in K.TITLE_ORDER}
    for u in K.UNIT_CODES:
        t = K.UNIT_TITLE[u]
        out[u] = dict(
            A=pk.weekly(u, OFF), V26=pk.weekly(u, ("Vacant line",)),
            a_all=pk.availability(lambda r, e, u=u: r["unit_code"] == u),
            a1=a1t[t], a_title=at[t], a1_unit=pk.availability(july25(unit=u)), a1_class=a1c, a1_first=a1f[t], a1_ratios=a1m[t],
            new=pk.new_lines(u))
    return out


def vacancy(new, after):
    """the FY2028 hours of the position control's vacant lines by fiscal week: every scheduled hour before the first
    shift on post, and after it the new holder's off-post share of the scheduled hours"""
    v = np.zeros(K.WEEKS)
    for _, first, off in new:
        for i in range(K.WEEKS * 7):
            d = K.FY28_START + dt.timedelta(days=i)
            if d.weekday() in off:
                continue
            v[i // 7] += K.SHIFT_H if d < first else K.SHIFT_H * after
    return v


def route(c, name):
    """(weekly need, relief hours on post a week) of one unit on one route"""
    a = c["a_all"]
    a1 = c["a1"]
    if name == "mean":
        return None, None
    if name == "R1":
        return c["A"] + c["V26"], K.WEEK_H * a
    if name == "R2":
        return c["A"] + vacancy(c["new"], 1 - a), K.WEEK_H * a
    if name == "R2t":
        return c["A"] + vacancy(c["new"], 0.0), K.WEEK_H * c["a_title"]
    if name == "R3":
        return c["A"] + c["V26"], K.WEEK_H * a1
    if name == "R4":
        return c["A"].copy(), K.WEEK_H * a1
    if name == "R5":
        return c["A"] + vacancy(c["new"], 0.0), K.WEEK_H
    if name == "R6":
        return c["A"] + c["V26"] + vacancy(c["new"], 1 - a1), K.WEEK_H * a1
    alt = {"G": a1, "G_unit": c["a1_unit"], "G_class": c["a1_class"], "G_first": c["a1_first"],
           "G_ratios": c["a1_ratios"], "G_none": a1, "G_avg": a1}[name]
    after = {"G_none": 0.0, "G_avg": 1 - a}.get(name, 1 - alt)
    return c["A"] + vacancy(c["new"], after), K.WEEK_H * alt


def table(comp):
    """per route: unit -> (ratio, positions)"""
    tab = {}
    for name in FAMILY + RUNGS:
        tab[name] = {}
        for u in K.UNIT_CODES:
            c = comp[u]
            if name == "mean":
                r = float((c["A"] + c["V26"]).mean() / (K.WEEK_H * c["a_all"]))
            else:
                need, h = route(c, name)
                r = q5(need) / h
            tab[name][u] = (r, int(math.ceil(r - 1e-9)))
    return tab


def call(pk):
    comp = components(pk)
    tab = table(comp)
    counts = {k: [tab[k][u][1] for u in K.UNIT_CODES] for k in tab}
    g = counts[GOLDEN]
    need, hours = {}, {}
    for u in K.UNIT_CODES:
        need[u], hours[u] = route(comp[u], GOLDEN)
    return dict(comp=comp, table=tab, counts=counts, golden=dict(zip(K.UNIT_CODES, g)), total=sum(g),
                need=need, hours=hours)
