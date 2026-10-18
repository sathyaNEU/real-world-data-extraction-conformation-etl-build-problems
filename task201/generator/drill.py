"""task201: every rung of the ladder, computed from the columns the pack ships.

The drill rule is the one filed in procedure PR-07: at each level take the branch, then the district
inside it, then the section class inside that, carrying the largest share of the window's interrupted
customer-hours; the slot is filed against the class the third step names.
"""
import numpy as np, pandas as pd
import params as P

LEVELS = ["oddzial", "rejon", "klasa_odcinka"]


def recorded_hours(ev):
    """Interrupted customer-hours as the dispatch record stands: customers behind the device that
    operated, times the span from the recorded start to restoration."""
    h = (ev.t_zalaczenie - ev.t_poczatek_oms).dt.total_seconds() / 3600.0
    return ev.odbiorcy * h


def observed_delay(ev):
    """On the events a line device timed, the interval between the loss of supply the device
    recorded and the first customer notification. Observable only there."""
    t = ev[ev.telemetrowane]
    return (t.t_zgloszenie - t.t_utrata).dt.total_seconds() / 60.0


def rungs(ev):
    """ev: the cleaned population (restored inside the window, keys joined). Returns a frame of
    per-event customer-hours under each rung."""
    e = ev.reset_index(drop=True).copy()
    e["ch_rec"] = recorded_hours(e)
    need = (~e.telemetrowane).values
    d = observed_delay(e)
    pooled = d.mean()                                   # one interval for every event
    by_cls = d.groupby(e.loc[d.index, "klasa_odcinka"]).mean()
    by_br = d.groupby(e.loc[d.index, "oddzial"]).mean()
    e["ch_r1"] = e.ch_rec
    e["ch_r2"] = e.ch_rec + np.where(need, e.odbiorcy * pooled / 60.0, 0.0)
    e["ch_r3"] = e.ch_rec + np.where(need, e.odbiorcy * e.klasa_odcinka.map(by_cls).values / 60.0, 0.0)
    e["ch_rbr"] = e.ch_rec + np.where(need, e.odbiorcy * e.oddzial.map(by_br).values / 60.0, 0.0)
    return e, dict(pooled=pooled, by_cls=by_cls, by_br=by_br)


def family(ev):
    """Every form of the class-conditional interval a competent analyst would use."""
    e = ev.reset_index(drop=True).copy(); e["ch_rec"] = recorded_hours(e)
    need = (~e.telemetrowane).values
    d = observed_delay(e); cl = e.loc[d.index, "klasa_odcinka"]; cu = e.loc[d.index, "odbiorcy"]
    br = e.loc[d.index, "oddzial"]
    est = {
        "mean": d.groupby(cl).mean(),
        "median": d.groupby(cl).median(),
        "cust_weighted": (d * cu).groupby(cl).sum() / cu.groupby(cl).sum(),
        "trimmed": d.groupby(cl).apply(lambda s: s[(s >= s.quantile(.05)) & (s <= s.quantile(.95))].mean()),
    }
    out = {}
    for k, v in est.items():
        out[k] = e.ch_rec + np.where(need, e.odbiorcy * e.klasa_odcinka.map(v).values / 60.0, 0.0)
    bc = d.groupby([br, cl]).mean()
    key = pd.Series(list(zip(e.oddzial, e.klasa_odcinka)), index=e.index)
    out["branch_x_class"] = e.ch_rec + np.where(
        need, e.odbiorcy * key.map(bc).fillna(est["mean"].mean()).values / 60.0, 0.0)
    return out


def walk(e, col):
    """The filed drill: largest share at each level in turn. Returns the path and every box's share."""
    path, boxes, scope = [], [], e
    for lv in LEVELS:
        tot = scope[col].sum()
        s = scope.groupby(lv)[col].sum().sort_values(ascending=False)
        boxes.append(dict(level=lv, total=tot, shares=(s / tot * 100.0), hours=s))
        path.append(s.index[0])
        scope = scope[scope[lv] == s.index[0]]
    return path, boxes
