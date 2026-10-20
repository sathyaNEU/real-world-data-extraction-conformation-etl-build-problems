"""The estimators, on the conformed index frame (one row per index stay: hospital, member, admission date, identifier
class, expected mortality, the death the claims record (in the stay, in the transferred stay or in a later stay inside
the window), the linkage's date of death if it returned one, whether a claim follows that date, and whether a claim
follows day 30): each hospital's 30-day deaths by every route of the ladder, and the golden, the linked deaths
corrected class by class for the linkage's false links and missed links at the rates the record's two control groups
measure."""
import numpy as np
import pandas as pd

import world as W

CLASSES = ("ssn", "simple", "compound")


def rates(f, by="cls", ctrl="all"):
    """The linkage's recall and false-link rate by class: recall on the deaths the claims record (positive controls:
    'all', or 'stay' for deaths in the index stay only), the false-link rate on the members with a claim after day 30
    (negative controls)."""
    out = {}
    for k, g in f.groupby(by):
        pos = g[g["known_death"] & ((g["known_place"] == "stay") if ctrl == "stay" else True)]
        neg = g[g["alive_after"]]
        r = pos["linked"].mean() if len(pos) else np.nan
        fp = neg["linked"].mean() if len(neg) else 0.0
        out[k] = (float(r), float(fp), len(pos), len(neg))
    return out


def deaths(f, how="golden", by="cls", ctrl="all", hosp_rates=False, denom="r_minus_f"):
    """Each hospital's 30-day deaths by route."""
    out = {}
    R = rates(f, by, ctrl)
    for h, g in f.groupby("hosp"):
        known = int(g["known_death"].sum())
        if how == "naive":                      # deaths in the stay and the linked deaths
            out[h] = float((g["in_stay"] | g["linked"]).sum())
            continue
        dead_or_linked = g["known_death"] | g["linked"]
        if how == "union":                      # plus the deaths a later claim records
            out[h] = float(dead_or_linked.sum())
            continue
        if how == "reflex":                     # and less the links a later claim contradicts
            out[h] = float((g["known_death"] | (g["linked"] & ~g["contradicted"])).sum())
            continue
        if how == "refl_u":                     # the golden, with the contradicted links dropped inside U first
            g = g.assign(linked=g["linked"] & ~(g["contradicted"] & ~g["known_death"] & ~g["alive_after"]))
        Rh = rates(g, by, ctrl) if hosp_rates else R
        tot = float(known)
        U = g[~g["known_death"] & ~g["alive_after"]]
        for k, u in U.groupby(by):
            r, fp, npos, nneg = Rh.get(k, R[k])
            if np.isnan(r) or npos < 10:          # a hospital's own control groups too small: the class's pooled rates
                r = R[k][0]
            if nneg < 50:
                fp = R[k][1]
            L, N = float(u["linked"].sum()), float(len(u))
            if how == "fp_only":
                est = L - fp * N
            elif how == "recall_only":
                est = L / r
            else:
                est = (L - fp * N) / ((r - fp) if denom == "r_minus_f" else r)
            tot += max(est, 0.0)
        out[h] = tot
    return out


def ratios(f, d):
    E = f.groupby("hosp")["p"].sum()
    return {h: d[h] / E[h] for h in d}


ROUTES = ("naive", "union", "reflex", "fp_only", "recall_only", "golden")


def losers(rat):
    return sorted(h for h, v in rat.items() if v > W.THRESHOLD)


def frame_from_truth(x):
    """The index frame built straight from the simulation (the clean truth), for calibration and the analyst test."""
    links = {(l["member"], l["adm"]): l for l in x["links"]}
    act = {}
    for m, d in x["activity"]:
        act.setdefault(m, []).append(d)
    known_extra, alive_dates = {}, {}
    for e in x["extra"]:
        if e["status"] == "20":
            known_extra[e["member"]] = e["disch"]
            alive_dates.setdefault(e["member"], []).append(e["adm"])   # admitted alive
        else:                                   # a later stay the member left alive
            alive_dates.setdefault(e["member"], []).extend([e["adm"], e["disch"]])
    rows = []
    for s in x["stays"]:
        m = s["member"]
        lk = links.get((m, s["adm"]))
        in_stay = bool(s["dies"] and s["place"] == "stay")
        kd = None
        if in_stay:
            kd = s["death"]
        elif m in known_extra and known_extra[m] <= s["adm"] + pd.Timedelta(days=W.WINDOW):
            kd = known_extra[m]
        ad = act.get(m, []) + alive_dates.get(m, []) + ([] if s["dies"] and s["place"] == "stay" else [s["disch"]])
        w_end = s["adm"] + pd.Timedelta(days=W.WINDOW)
        rows.append(dict(hosp=s["hosp"], member=m, adm=s["adm"], cls=s["cls"], p=s["p"], in_stay=in_stay,
                         known_death=kd is not None, known_place="stay" if in_stay else ("later" if kd else None),
                         linked=lk is not None, link_date=lk["death"] if lk else None,
                         contradicted=bool(lk is not None and any(d > lk["death"] for d in ad)),
                         alive_after=any(d > w_end for d in ad)))
    return pd.DataFrame(rows)
