"""The call and its routes, on trip records (from the world or read back from the pack):
seg, ground, hours, nhauls, observed, half, land_mk, land_bms (declared), self_dis (declared discards) and on observed
trips obs_mk, obs_bms, obs_dis (the observer's sampled hauls raised to the trip), obs_hours_s, obs_unw_s, obs_mk_s
(the sampled hauls themselves).

The golden: a segment's 2025 discards are its observed trips' discards plus, on its unobserved trips, the unwanted
catch (BMS and lawful discards) per hour fished that its observed trips show on each ground, times the unobserved
hours on that ground, less the BMS the unobserved trips declared; its catch is every trip's declared landings plus
those discards."""
from __future__ import annotations

import itertools

import common as K

THR = K.THRESHOLD


def _aux(t, aux, observed):
    if aux == "hours":
        return t["hours"]
    if aux == "hauls":
        return t["nhauls"]
    if aux == "trips":
        return 1.0
    if aux == "mk":
        return t["land_mk"]
    raise ValueError(aux)


def _key(t, strata):
    if strata == "ground":
        return t["ground"]
    if strata == "ground_half":
        return (t["ground"], t["half"])
    return 0


def golden(T, strata="ground", aux="hours", net=True, landed="decl", haul_level=False):
    """each segment's discard share (per cent); None when a stratum with unobserved effort has no observed trip"""
    parts = golden_parts(T, strata, aux, net, landed, haul_level)
    return None if parts is None else {s: 100 * d / c for s, (d, c) in parts.items()}


def golden_parts(T, strata="ground", aux="hours", net=True, landed="decl", haul_level=False):
    """each segment's (discards, catch) in kg live weight"""
    out = {}
    for s in K.SEG:
        X = [t for t in T if t["seg"] == s]
        O = [t for t in X if t["observed"]]
        N = [t for t in X if not t["observed"]]
        disc = sum(t["obs_dis"] for t in O)
        if landed == "decl":
            catch = sum(t["land_mk"] + t["land_bms"] + t["obs_dis"] for t in O)
        else:
            catch = sum(t["obs_mk"] + t["obs_bms"] + t["obs_dis"] for t in O)
        for k in sorted({_key(t, strata) for t in N}, key=str):
            Ok = [t for t in O if _key(t, strata) == k]
            Nk = [t for t in N if _key(t, strata) == k]
            if not Ok:
                return None
            if haul_level and aux == "hours":
                u = sum(t["obs_unw_s"] for t in Ok) / sum(t["obs_hours_s"] for t in Ok)
            else:
                u = sum(t["obs_bms"] + t["obs_dis"] for t in Ok) / sum(_aux(t, aux, True) for t in Ok)
            U = u * sum(_aux(t, aux, False) for t in Nk)
            disc += U - (sum(t["land_bms"] for t in Nk) if net else 0.0)
            catch += sum(t["land_mk"] for t in Nk) + U
        out[s] = (disc, catch)
    return out


def family(T):
    """the golden's licensed members: every raising variable, ground or ground by half-year, declared or observer
    landings for the observed trips, trip-level or haul-level rates"""
    fam = {}
    for strata, aux, landed, hl in itertools.product(("ground", "ground_half"), ("hours", "hauls", "trips", "mk"),
                                                     ("decl", "obs"), (False, True)):
        if hl and aux != "hours":
            continue
        g = golden(T, strata=strata, aux=aux, landed=landed, haul_level=hl)
        if g is not None:
            fam["%s/%s/%s%s" % (strata, aux, landed, "/haul" if hl else "")] = g
    return fam


def routes(T):
    """the wrong routes, each segment's share"""
    out = {}
    out["R0 the logbooks' declared discards"] = {
        s: 100 * sum(t.get("self_dis", 0.0) for t in T if t["seg"] == s) /
        sum(t["land_mk"] + t["land_bms"] + t.get("self_dis", 0.0) for t in T if t["seg"] == s) for s in K.SEG}
    out["R1 the observed trips' discard share"] = {
        s: 100 * sum(t["obs_dis"] for t in T if t["seg"] == s and t["observed"]) /
        sum(t["obs_mk"] + t["obs_bms"] + t["obs_dis"] for t in T if t["seg"] == s and t["observed"]) for s in K.SEG}
    r2 = {}
    for s in K.SEG:
        X = [t for t in T if t["seg"] == s]
        D = 0.0
        for g in K.GR:
            Og = [t for t in X if t["observed"] and t["ground"] == g]
            Xg = [t for t in X if t["ground"] == g]
            if Og:
                D += sum(t["obs_dis"] for t in Og) / sum(t["hours"] for t in Og) * sum(t["hours"] for t in Xg)
        land = sum(t["land_mk"] + t["land_bms"] for t in X)
        r2[s] = 100 * D / (land + D)
    out["R2 the observed discards per hour by ground, raised (default path)"] = r2
    out["R3 the observed trips' unwanted share"] = {
        s: 100 * sum(t["obs_bms"] + t["obs_dis"] for t in T if t["seg"] == s and t["observed"]) /
        sum(t["obs_mk"] + t["obs_bms"] + t["obs_dis"] for t in T if t["seg"] == s and t["observed"]) for s in K.SEG}
    out["R4 unwanted catch per hour, grounds pooled"] = golden(T, strata="none")
    out["R5 unwanted catch per hour by ground, declared BMS not netted"] = golden(T, net=False)
    return out


def designated(shares):
    return tuple(s for s in K.SEG if shares[s] > THR)


def margin(fam):
    return min(abs(v - THR) for g in fam.values() for v in g.values())


def ratio_to_landings(T):
    """the default path's other form: observed discards over observed trips' declared landings, by ground, raised
    by every trip's declared landings"""
    out = {}
    for s in K.SEG:
        X = [t for t in T if t["seg"] == s]
        D = 0.0
        for g in K.GR:
            Og = [t for t in X if t["observed"] and t["ground"] == g]
            Xg = [t for t in X if t["ground"] == g]
            if Og:
                D += sum(t["obs_dis"] for t in Og) / sum(t["land_mk"] + t["land_bms"] for t in Og) * \
                    sum(t["land_mk"] + t["land_bms"] for t in Xg)
        land = sum(t["land_mk"] + t["land_bms"] for t in X)
        out[s] = 100 * D / (land + D)
    return out


def bms_rates(T):
    """BMS declared per hour fished, observed against unobserved trips, by segment and ground (kg an hour)"""
    out = {}
    for s in K.SEG:
        for g in K.GR:
            X = [t for t in T if t["seg"] == s and t["ground"] == g]
            O = [t for t in X if t["observed"]]
            N = [t for t in X if not t["observed"]]
            if O and N:
                out[(s, g)] = (sum(t["land_bms"] for t in O) / sum(t["hours"] for t in O),
                               sum(t["land_bms"] for t in N) / sum(t["hours"] for t in N), len(O), len(N))
    return out


def nursery_share(T):
    """the share of hours fished on each ground, observed against unobserved trips, by segment"""
    out = {}
    for s in K.SEG:
        X = [t for t in T if t["seg"] == s]
        for flag in (True, False):
            Y = [t for t in X if t["observed"] == flag]
            h = sum(t["hours"] for t in Y)
            out[(s, flag)] = {g: sum(t["hours"] for t in Y if t["ground"] == g) / h for g in K.GR}
    return out
