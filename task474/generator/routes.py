"""The ladder's routes, each computed from one person-level table of sittings (the conformed record).

A route picks an old-paper group and a new-paper group it takes to be equivalent; the pass mark it files is the lowest
raw mark that no larger share of the new-paper group reaches than the old-paper group reaches 65 (AP-3 section 3)."""
import datetime as dt
from collections import defaultdict

import numpy as np

import params as P


def mark_for(p_old, new_scores):
    """the lowest raw mark y whose share of new_scores at or above y is no larger than p_old"""
    a = np.asarray(new_scores)
    for y in range(0, P.NEW_ITEMS + 2):
        if (a >= y).mean() <= p_old + 1e-12:
            return y
    return P.NEW_ITEMS + 1


def share_at(p_old_func, new_scores, y):
    return float((np.asarray(new_scores) >= y).mean())


def attempts(people):
    """each person's sat sittings in date order: (date, vendor, score, attempt)"""
    out = {}
    for pid, ss in people.items():
        out[pid] = [s for s in sorted(ss, key=lambda s: s["date"]) if s["status"] == "sat"]
    return out


def first_timers(att, vendor, d0, d1):
    return [ss[0]["score"] for ss in att.values() if ss and ss[0]["vendor"] == vendor and d0 <= ss[0]["date"] <= d1]


def r_same_months(att):
    p = np.mean(np.array(first_timers(att, "old", dt.date(2025, 4, 1), dt.date(2025, 9, 30))) >= P.OLD_PASS)
    return mark_for(p, first_timers(att, "new", P.SWITCH, P.LAST_DAY)), p


def r_adjacent(att):
    p = np.mean(np.array(first_timers(att, "old", dt.date(2025, 10, 1), dt.date(2026, 3, 31))) >= P.OLD_PASS)
    return mark_for(p, first_timers(att, "new", P.SWITCH, P.LAST_DAY)), p


def cross_switch(att, first_only=True):
    """(first old score, new raw) for candidates whose old sittings all failed and who then sat the new paper"""
    out = []
    for ss in att.values():
        old = [s for s in ss if s["vendor"] == "old"]
        new = [s for s in ss if s["vendor"] == "new"]
        if not old or not new:
            continue
        if first_only and len(old) != 1:
            continue
        out.append((old[-1]["score"], new[0]["score"]))
    return out


def history_pairs(att, d0=dt.date(2021, 1, 1), d1=dt.date(2025, 12, 31), first_only=True):
    """(first score, next score) for old-paper fails followed by another old sitting, the fail dated d0 to d1"""
    out = []
    for ss in att.values():
        old = [s for s in ss if s["vendor"] == "old"]
        for i in range(len(old) - 1):
            if first_only and i > 0:
                break
            if d0 <= old[i]["date"] <= d1 and old[i]["score"] < P.OLD_PASS:
                out.append((old[i]["score"], old[i + 1]["score"]))
    return out


def r_matched(att, band=1, d0=dt.date(2021, 1, 1), d1=dt.date(2025, 12, 31), first_only=True):
    cs = cross_switch(att, first_only)
    hist = history_pairs(att, d0, d1, first_only)
    by = defaultdict(list)
    for x1, x2 in hist:
        by[x1 // band].append(x2 >= P.OLD_PASS)
    w, tot = 0.0, 0
    for x1, _ in cs:
        b = by.get(x1 // band)
        if not b:
            continue
        w += np.mean(b)
        tot += 1
    p = w / tot
    return mark_for(p, [y for _, y in cs]), p


def r_unmatched(att):
    cs = cross_switch(att)
    hist = history_pairs(att)
    p = np.mean([x2 >= P.OLD_PASS for _, x2 in hist])
    return mark_for(p, [y for _, y in cs]), p


def r_side_by_side(att):
    cs = cross_switch(att, first_only=False)
    x = np.array([a for a, _ in cs], float)
    y = np.array([b for _, b in cs], float)
    eq = y.mean() + y.std() * (P.OLD_PASS - x.mean()) / x.std()
    return int(np.ceil(eq - 1e-9)), eq


def r_did(att):
    """first-timers a year apart, the cohort's move read off the winter halves both on the old paper"""
    a = np.array(first_timers(att, "old", dt.date(2025, 4, 1), dt.date(2025, 9, 30)), float)
    w0 = np.array(first_timers(att, "old", dt.date(2024, 10, 1), dt.date(2025, 3, 31)), float)
    w1 = np.array(first_timers(att, "old", dt.date(2025, 10, 1), dt.date(2026, 3, 31)), float)
    shifted = a + (w1.mean() - w0.mean())
    p = np.mean(shifted >= P.OLD_PASS - 0.5)
    return mark_for(p, first_timers(att, "new", P.SWITCH, P.LAST_DAY)), p
