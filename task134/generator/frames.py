"""The shipped tables as DataFrames, in the column order and row order of the extracts."""
import numpy as np
import pandas as pd

import observe as OB
import world as W


def placements_df(O):
    rows = O.placements + O.short
    df = pd.DataFrame(rows)
    df = df.sort_values(["_st", "client_id", "placement_type"], kind="stable").reset_index(drop=True)
    df.insert(0, "placement_id", ["%07d" % v for v in placement_ids(df, O)])
    return df


def placement_ids(df, O):
    """episode numbers as the case system issues them, from one sequence it shares with every other service it records
    (care at home, day care, equipment), so a care home episode's number follows the one before by a gap of one or
    more: the episodes on the old system numbered at the July 2023 migration in start order, later ones in the order
    they were keyed (a conversion when the funding decision was recorded, the April fee episodes by the uprating run on
    1 April, anything else on the day it started or a day or two after). The rows keep the extract's order."""
    rng = np.random.default_rng(W.SEED + 1111)
    n = len(df)
    st = df["_st"].to_numpy(float)
    who = df["_i"].to_numpy(int)
    perm = (df["placement_type"] == "PERM").to_numpy()
    first = np.zeros(n, bool)
    seen = set()
    for k in range(n):                                  # rows are in start order
        if perm[k] and who[k] >= 0 and who[k] not in seen:
            seen.add(who[k])
            first[k] = True
    april = np.array([W.fy_start(W.fy(s)) == s for s in st]) & perm & ~first
    keyed = st + (rng.geometric(0.55, n) - 1)
    keyed[april] = st[april]
    conv = first & (df["route"] == "CONV").to_numpy()
    keyed[conv] = st[conv] + O.ask.lag0[who[conv]]
    live = keyed >= W.GOLIVE
    order = np.lexsort((np.arange(n), np.where(live, keyed, st), live))
    gap = np.where(live[order], rng.geometric(0.30, n), rng.geometric(0.45, n))
    ids = np.empty(n, np.int64)
    ids[order] = 3100000 + np.cumsum(gap)
    return ids


PL_COLS = ["placement_id", "client_id", "service_no", "placement_type", "route", "care_type", "admitted", "start_date",
           "end_date", "end_reason", "weekly_fee", "locality"]
LI_COLS = ["debtor_ref", "service_no", "admitted", "award_start", "period", "period_start", "period_end", "line_type",
           "amount", "award_end", "end_reason"]


def lines_df(O):
    df = O.lines.copy()
    order = {"FPC": 0, "FNC": 1, "HOSP": 2, "ADJ": 3}
    df["_o"] = df["line_type"].map(order)
    df = df.sort_values(["period_start", "debtor_ref", "_o"], kind="stable").reset_index(drop=True)
    return df


def crosswalk_df(O):
    df = pd.DataFrame(O.crosswalk)
    df["_k"] = df["client_id"]
    df = df.sort_values(["_k", "legacy_client_no"], kind="stable").reset_index(drop=True)
    return df


def deaths_df(O):
    df = pd.DataFrame(O.deaths)
    return df.sort_values(["date_of_death", "client_id"], kind="stable").reset_index(drop=True)


def assess_df(O):
    df = pd.DataFrame(O.assess)
    df["completed_s"] = [OB.ds(v) for v in df["completed"]]
    df["effective_s"] = [OB.ds(v) for v in df["effective"]]
    df = df.sort_values(["completed", "_ref", "effective"], kind="stable").reset_index(drop=True)
    df.insert(0, "assessment_no", ["FA%06d" % v for v in assessment_numbers(df)])
    return df


def assessment_numbers(df):
    """assessment numbers as the finance system issues them when an assessment is opened, from one sequence it shares
    with the charging assessments for care at home, a few days to a few weeks before the assessment is completed. The
    rows keep the extract's order (by completion)."""
    rng = np.random.default_rng(W.SEED + 2222)
    n = len(df)
    opened = df["completed"].to_numpy(float) - (rng.geometric(0.16, n) - 1)
    order = np.lexsort((np.arange(n), opened))
    nums = np.empty(n, np.int64)
    nums[order] = 210000 + np.cumsum(rng.geometric(0.40, n))
    return nums


def as_str(df, cols):
    out = df[cols].copy()
    for c in cols:
        out[c] = out[c].map(lambda v: "" if v is None or (isinstance(v, float) and np.isnan(v)) else
                            ("%.2f" % v if isinstance(v, float) else str(v)))
    return out


def register_df(S, O):
    """the Care Inspectorate register of care homes for older people in Strathallan, December 2026: every
    registration, a re-registered home's old registration kept with its cancellation date, and two homes that closed"""
    rows = []
    for k, h in enumerate(S.H):
        if h["ooa"]:
            continue
        reg = [x for x in W.HOMES if x[0] == h["name"]][0][5]
        types = "Care home for older people; nursing care" if h["nursing"] else "Care home for older people"
        if h["name"] in W.REREG:
            prov, rday = W.REREG[h["name"]]
            rows.append(dict(service_no=O.svc[k], service_name=h["name"], provider=h["prov"], postcode=O.home_pc[k],
                             service_type=types, registered_places=h["places"], registered=reg,
                             cancelled=OB.ds(rday - 1), previous_service_no=""))
            rows.append(dict(service_no=O.svc_new[h["name"]], service_name=h["name"], provider=prov,
                             postcode=O.home_pc[k], service_type=types, registered_places=h["places"],
                             registered=OB.ds(rday), cancelled="", previous_service_no=O.svc[k]))
        else:
            rows.append(dict(service_no=O.svc[k], service_name=h["name"], provider=h["prov"], postcode=O.home_pc[k],
                             service_type=types, registered_places=h["places"], registered=reg, cancelled="",
                             previous_service_no=""))
    for name, loc, prov, places, reg, canc, svc in CLOSED:
        pcs = [p for p, l in O.pcs if l == loc]
        rows.append(dict(service_no=svc, service_name=name, provider=prov, postcode=pcs[len(pcs) // 3],
                         service_type="Care home for older people", registered_places=places, registered=reg,
                         cancelled=canc, previous_service_no=""))
    df = pd.DataFrame(rows)
    return df.sort_values(["service_name", "registered"], kind="stable").reset_index(drop=True)


CLOSED = [("Muirton Lodge", "Braeburn", "Muirton Lodge Ltd", 18, "2002-04-01", "2019-06-28", "CS2002317442"),
          ("Gowanbank House", "Dunmorrow", "Gowanbank Care Ltd", 23, "2003-11-17", "2020-09-30", "CS2003341906")]


def lookup_df(O):
    df = pd.DataFrame(O.pcs, columns=["postcode", "locality"])
    return df.sort_values("postcode", kind="stable").reset_index(drop=True)
