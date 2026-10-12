"""The shipped tables as DataFrames, in the column order and row order of the extracts."""
import numpy as np
import pandas as pd

import observe as OB
import world as W


def placements_df(O):
    rows = O.placements + O.short
    df = pd.DataFrame(rows)
    df = df.sort_values(["_st", "client_id", "placement_type"], kind="stable").reset_index(drop=True)
    rng = np.random.default_rng(W.SEED + 1111)
    ids = 3100000 + np.cumsum(rng.integers(1, 6, len(df)))
    df.insert(0, "placement_id", ["%07d" % v for v in ids])
    return df


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
    rng = np.random.default_rng(W.SEED + 2222)
    df.insert(0, "assessment_no", ["FA%06d" % v for v in 210000 + np.cumsum(rng.integers(1, 4, len(df)))])
    return df


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
