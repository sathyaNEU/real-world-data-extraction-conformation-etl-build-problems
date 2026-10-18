"""The ladder, every rung computed from the pack: how the operations the network did not record are completed at a
field without a count. Each rung returns each non-towered field's 2026 lead (kg) and the qualifying set."""
import numpy as np

import bundle as B
import world as W


def _lead(heard, lid, u):
    return (heard.loc[lid, "lead"] + u * W.LEAD_UNRECORDED) / 1000.0


def counted_capture(P, inv, fields=None):
    """The network's share of the counted fields' operations: at a tower, the civil operations it recorded in tower
    hours against the tower's civil count; at a count study, the piston operations it recorded against the count."""
    C = fields or W.COUNTED
    num = den = 0.0
    for lid in C:
        if lid in W.TOWERED:
            t = inv["tower"][lid]
            num += t["heard_in_hours"]
            den += t["civil"]
        else:
            num += inv["heard"].loc[lid, "ops"]
            den += P.study[lid]
    return num / den


def rungs(P, inv=None):
    inv = inv or P.inventory()
    heard = inv["heard"]
    unrec, nd = inv["unrec"], inv["nd"]
    pb = {l: len(v) for l, v in inv["piston_based"].items()}
    out = {}
    est = [l for l in W.UNTOWERED if l not in W.STUDIED]

    def fill(fn):
        lead = {}
        for l in W.UNTOWERED:
            lead[l] = inv["lead"][l] if l in W.STUDIED else _lead(heard, l, fn(l))
        return lead

    r = counted_capture(P, inv)
    out["R0 one capture rate"] = fill(lambda l: heard.loc[l, "ops"] * (1 - r) / r)
    out["R0b one capture rate on the lead"] = {l: (inv["lead"][l] if l in W.STUDIED else
                                                   heard.loc[l, "lead"] / r / 1000.0) for l in W.UNTOWERED}
    sch = [l for l in W.COUNTED if P.dir[l]["Flight Training"] == "Y"]
    oth = [l for l in W.COUNTED if P.dir[l]["Flight Training"] != "Y"]
    rs, ro = counted_capture(P, inv, sch), counted_capture(P, inv, oth)
    out["R1 capture by flight training"] = fill(
        lambda l: heard.loc[l, "ops"] * (1 - (rs if P.dir[l]["Flight Training"] == "Y" else ro)) /
        (rs if P.dir[l]["Flight Training"] == "Y" else ro))
    tot = sum(heard.loc[l, "ops"] + unrec[l] for l in W.COUNTED)
    opba = tot / sum(pb[l] for l in W.COUNTED)
    out["R2 operations per based airplane"] = fill(lambda l: max(0.0, opba * pb[l] - heard.loc[l, "ops"]))
    kb = sum(unrec[l] for l in W.COUNTED) / sum(pb[l] for l in W.COUNTED)
    out["R3 unrecorded per based airplane"] = fill(lambda l: kb * pb[l])
    act = P.based_activity(inv)
    out["R4 never-heard airplanes fly like the heard ones"] = fill(lambda l: act[l] * nd[l])
    out["R4b never-recorded share of based airplanes as the unrecorded share"] = {
        l: (inv["lead"][l] if l in W.STUDIED else heard.loc[l, "lead"] / (1.0 - nd[l] / pb[l]) / 1000.0)
        for l in W.UNTOWERED}
    out["R5 the network's record alone"] = fill(lambda l: 0.0)
    out["G unrecorded per never-heard airplane"] = {l: inv["lead"][l] for l in W.UNTOWERED}
    sets = {k: B.qualifying(v) for k, v in out.items()}
    return out, sets, dict(r=r, r_school=rs, r_other=ro, opba=opba, kb=kb, k=inv["k"])
