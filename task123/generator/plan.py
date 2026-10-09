"""The amendment plan: every designed version beyond a return's original filing.

plan[(org, q)] = {
    "mgmt_exact": bool,            fourth quarters only
    "v1_error": {"op": int, "pg": int},   total-income error carried by the original filing
    "v1_shift": {"op": {line: amount}, "pg": {...}},   line misclassification on the original
    "events": [ {date, kind, refs ('both'|'op'|'pg'), error_after, shift, review_days} ],
}
kinds: correction (total changes), linesplit (lines only), coding (rejected, lines only),
withdrawn (same figures, never accepted).
"""
import datetime as dt

import numpy as np

from common import SEED, MARCH_CENSUSES, qend, fyq
from roster import Q


def add(plan, key, **kw):
    p = plan.setdefault(key, {})
    for k, v in kw.items():
        if k == "events":
            p.setdefault("events", []).extend(v)
        elif k in ("v1_error", "v1_shift"):
            p.setdefault(k, {}).update(v)
        else:
            p[k] = v
    return p


def residue_plan(plan):
    # D1: the 31 December grantee that files each May (residue in all six rounds)
    for fy, exact in [(2018, True), (2019, False), (2020, True), (2021, True), (2022, False),
                      (2023, True), (2024, False), (2025, True)]:
        add(plan, ("D1", Q(fy, 12)), mgmt_exact=exact)
    for fy, exact in [(2020, True), (2021, True), (2022, False), (2023, False), (2024, True),
                      (2025, False)]:
        add(plan, ("D2", Q(fy, 12)), mgmt_exact=exact)
    add(plan, ("J1", Q(2022, 6)), mgmt_exact=True)
    add(plan, ("J2", Q(2023, 6)), mgmt_exact=False)
    add(plan, ("J3", Q(2022, 6)), mgmt_exact=True)
    add(plan, ("J4", Q(2025, 6)), mgmt_exact=True)


def october_exact(plan, orgs):
    for o in orgs:
        if o.bal == 3 and o.sept_status == "oct":
            add(plan, (o.key, Q(2026, 3)), mgmt_exact=True)


def twin_plan(plan, x):
    add(plan, ("TA", Q(2024, 12)), v1_error={"op": x},
        events=[{"date": dt.date(2025, 4, 23), "kind": "correction", "refs": "both",
                 "error_after": 0}])


def g_r2_plan(plan, x):
    add(plan, ("G_R2", Q(2026, 6)), v1_error={"op": x},
        events=[{"date": dt.date(2026, 10, 5), "kind": "correction", "refs": "both",
                 "error_after": 0, "review_days": 0}])


def l_dual_plan(plan, x):
    # both references filed low on 3-4 August; corrected under the operating grant only
    add(plan, ("L_dual", Q(2026, 6)), v1_error={"op": -x, "pg": -x},
        events=[{"date": dt.date(2026, 8, 25), "kind": "correction", "refs": "op",
                 "error_after": 0}])


def du2_plan(plan, e):
    # March 2023: the project-grant copy was corrected before the census, the operating one after
    add(plan, ("DU2", Q(2022, 12)), v1_error={"op": e, "pg": e},
        events=[{"date": dt.date(2023, 3, 9), "kind": "correction", "refs": "pg", "error_after": 0,
                 "review_days": 1},
                {"date": dt.date(2023, 4, 18), "kind": "correction", "refs": "op", "error_after": 0}])


def post_census_corrections(plan, orgs, tot, picks):
    """Corrections accepted after a March census to the last quarter of that census's window.

    picks: list of (org_key, round_year, error_fraction_of_quarter, correction_date)."""
    for key, ry, frac, d in picks:
        q = Q(ry - 1, 12)
        e = int(round(tot[key][q] * frac))
        add(plan, (key, q), v1_error={"op": e, "pg": e},
            events=[{"date": d, "kind": "correction", "refs": "both", "error_after": 0}])


def v3_linesplits(plan, picks):
    """Fourth-quarter returns re-amended after a census with a new line split, total unchanged.

    picks: (org_key, round_year, date, shift)"""
    for key, ry, d, shift in picks:
        q = Q(ry - 1, 3)
        add(plan, (key, q), events=[{"date": d, "kind": "linesplit", "refs": "both",
                                     "shift": shift}])
