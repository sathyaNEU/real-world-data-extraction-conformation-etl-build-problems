"""Every route a solver might take to the three centres, computed from the cut pack the way the golden reads it: the
ladder's rungs, the golden's model family and the shortcuts. Each returns each hospital's ratio of observed to
expected deaths (or, for the crude and volume routes, the figure the route ranks on)."""
import datetime as dt

import numpy as np
import pandas as pd

import analysis as A
import common as K
import models as M

H = M.H


def frame(P):
    return M.prep(A.frame(P))


def family(d):
    """The golden's family: every form a competent analyst would fit to the patient's condition before surgery with
    the earlier operation on the pancreas or bile ducts in it (logit or probit, an age curve, the harmless earlier
    procedures as their own terms, the conditions as a count, the conditions with no added risk, the diagnosis in
    groups, the earlier operation and a gallbladder removal as one flag)."""
    F = {k: M.ratio(d, cols, link)[0] for k, (cols, link) in M.FAMILY.items()}
    e = d.assign(earlier_op=((d.redo + d.chole) > 0).astype(float))
    F["earlier_op"] = M.ratio(e, M.INDEX + ["earlier_op"])[0]
    g = d.assign(cp=d.pdx.str.startswith("K86.1").astype(float),
                 benign=(~d.pdx.str.startswith("C") & ~d.pdx.str.startswith("K86.1")).astype(float))
    F["dx_groups"] = M.ratio(g, M.GOLDEN + ["cp", "benign"])[0]
    return F


def shortcuts(d):
    """Two forms that keep the earlier operation but leave the filed estimand: comorbidities dropped, and the ratios
    shrunk toward the eight hospitals' mean."""
    return {"golden_min": M.ratio(d, ["age10", "male", "tot", "whip", "urg", "redo"])[0],
            "golden_eb": M.eb(d, M.ratio(d, M.GOLDEN)[0])}


def history_from(P, start):
    """The earlier operations rebuilt only from the files from a given year on."""
    hist = {}
    for rec in P["discharges"]:
        if not rec["key"] or rec["discharge"].year < start:
            continue
        for c, dd in rec["px"]:
            if c in A.EARLIER:
                hist.setdefault(rec["key"], []).append(dd or rec["admit"])
    return hist


def ladder(P):
    d = frame(P)
    R = {}
    R["raw"] = d.groupby("h").dead.mean().reindex(H)
    R["index"] = M.ratio(d, M.INDEX)[0]
    R["index_probit"] = M.ratio(d, M.INDEX, "probit")[0]
    R["index_many"] = M.ratio(d, M.INDEX + ["htn", "lipid", "gerd", "obese", "smoke", "osa", "thyroid", "depress",
                                            "age2"])[0]
    R["index_comp"] = M.ratio(d, M.INDEX + ["comp"])[0]
    R["index_min"] = M.ratio(d, ["age10", "male", "tot", "whip", "urg"])[0]
    R["index_eb"] = M.eb(d, R["index"])
    e = d.assign(any_earlier=((d.redo + d.chole + d.stent) > 0).astype(float))
    R["any_earlier"] = M.ratio(e, M.INDEX + ["any_earlier"])[0]
    R["golden"] = M.ratio(d, M.GOLDEN)[0]
    # the referral centres compared on first operations only
    first = d[d.redo == 0]
    R["first_only"] = M.ratio(first, M.INDEX)[0]
    # the earlier operation rebuilt from the files of 2019 on, or of 2023 on only
    for start in (2019, 2023):
        hist = history_from(P, start)
        adm = {rec["rec_id"]: rec["admit"] for rec in A.operations(P)}
        dd = d.copy()
        dd["redo"] = [float(any(x < adm[r] for x in hist.get(k, []))) for k, r in zip(dd.key, dd.rec_id)]
        R["history_from_%d" % start] = M.ratio(dd, M.GOLDEN)[0]
    # the operation's own record, by discharge date in place of operation date
    R["volume"] = -d.groupby("h").size().reindex(H).astype(float)
    return R


def by_discharge(P):
    """The population read by discharge date (operations of December 2022 discharged in January 2023 in, those of late
    December 2025 discharged in 2026 out): the golden's model."""
    ops = []
    for rec in P["discharges"]:
        if A._res_date(rec) is None or rec["hosp"] not in K.ELIGIBLE or rec["age"] < 18:
            continue
        if K.WINDOW[0] <= rec["discharge"] <= K.WINDOW[1]:
            ops.append(rec)
    return ops


def top3(s):
    return M.top3(s)


def bins(F):
    """Each hospital's range over the family, and whether every member lands in one one-decimal bin."""
    vals = np.array([v.values for v in F.values()])
    lo, hi = vals.min(axis=0), vals.max(axis=0)
    blo, bhi = np.floor(lo / .1 + .5), np.floor(hi / .1 + .5)
    edge = {h: round(float(min(lo[i] - (blo[i] - .5) * .1, (bhi[i] + .5) * .1 - hi[i])), 4) for i, h in enumerate(H)}
    return dict(lo=dict(zip(H, lo)), hi=dict(zip(H, hi)), same=bool((blo == bhi).all()), edge=edge)
