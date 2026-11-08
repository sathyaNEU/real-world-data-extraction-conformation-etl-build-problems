"""Every route through the availability record, on one representation R that the clean truth (from_truth) and the
cut pack (parse.read_pack) both produce: status changes per unit, the visit windows, the supply interruptions, the
work orders, the programme and the 2027 visit plan. Routes: the default path and its cheap family, the two wrong
clocks, and the restart-clock constructions that make the standing family."""
import bisect
import math
import warnings

import numpy as np

import world as W

DAY = W.DAY
YEAR_S = 365.0 * DAY
PRIO = {"Offline": 3, "Faulted": 2, "Unavailable": 1}


# ------------------------------------------------------------------------------------------------ representation
def rows_from_intervals(iv, start):
    """Status changes from possibly overlapping non-Available intervals, by priority Offline > Faulted >
    Unavailable > Available, starting Available at the unit's first report (a sweep over the boundaries)."""
    evs = []
    for a, b, st, *_ in iv:
        if b > a:
            evs.append((a, 1, st))
            evs.append((b, -1, st))
    evs.sort(key=lambda e: (e[0], e[1]))
    live = {"Offline": 0, "Faulted": 0, "Unavailable": 0}
    rows, cur = [(start, "Available")], "Available"
    i = 0
    while i < len(evs):
        t = evs[i][0]
        while i < len(evs) and evs[i][0] == t:
            live[evs[i][2]] += evs[i][1]
            i += 1
        best = "Offline" if live["Offline"] > 0 else "Faulted" if live["Faulted"] > 0 else \
            "Unavailable" if live["Unavailable"] > 0 else "Available"
        if t < start:
            rows[0] = (start, best)
            cur = best
            continue
        if best != cur:
            if rows and rows[-1][0] == t:
                rows[-1] = (t, best)
            else:
                rows.append((t, best))
            cur = best
    out = []
    for t, st in rows:
        if out and out[-1][1] == st:
            continue
        out.append((t, st))
    return out


def from_truth(H, charges=None):
    """R from the clean truth: every row as the units and back office produced it, no re-sends, every key final."""
    R = dict(hubs=[], units={}, rows={}, visits={}, visits27={}, dso={}, wo=[], programme={}, cpd={}, end=W.HIST_END)
    for h in H["hubs"]:
        R["hubs"].append(dict(code=h["code"], name=h["name"], site=h["site"], county=h["county"]))
        ev = H["plans"][h["code"]]
        R["visits"][h["code"]] = [(e["ws"], e["we"]) for e in ev if e["kind"] == "visit"]
        R["dso"][h["code"]] = [(e["s"], e["e"]) for e in ev if e["kind"] == "dso"]
        R["visits27"][h["code"]] = [(W.from_local(d.year, d.month, d.day, *W.visit_window(h, d)[:2]),
                                     W.from_local(d.year, d.month, d.day, *W.visit_window(h, d)[2:])) for d in W.plan_2027(h)]
        if h["prog"]:
            R["programme"][h["code"]] = dict(works=W.works_time(h["code"]), new_unit=h["kind"] in W.NEW_UNIT_KINDS)
    for u in H["units"]:
        run = H["runs"][u["uid"]]
        R["units"][u["new_id"]] = dict(hub=u["hub"], model=u["model"], start=run["start"])
        R["rows"][u["new_id"]] = rows_from_intervals(run["iv"], run["start"])
    umap = {u["uid"]: u for u in H["units"]}
    for j in H["jobs"]:
        R["wo"].append(dict(hub=j["hub"], key=umap[j["uid"]]["new_id"] if j["uid"] else None,
                            kind={"rc_other": "rc_repair"}.get(j["kind"], j["kind"]), logged=j["logged"], arrive=j["arrive"],
                            done=j["done"], full=j.get("full", True)))
    if charges is not None:
        n = {}
        for c in charges:
            if c["model"] == "HX150" and not c["failed"] and c["auth"] != "test":
                n[c["uid"]] = n.get(c["uid"], 0) + 1
        days = (W.HIST_END - W.S26_START) / float(DAY)
        for u in H["units"]:
            if u["model"] == "HX150":
                R["cpd"][u["new_id"]] = n.get(u["uid"], 0) / days
    return R


def hx_keys(R, hub=None):
    return sorted(k for k, u in R["units"].items() if u["model"] == "HX150" and (hub is None or u["hub"] == hub))


def hub_keys(R, hub):
    return sorted(k for k, u in R["units"].items() if u["hub"] == hub)


def hubinfo(R):
    return {h["code"]: h for h in R["hubs"]}


def site_flags(site):
    return (1.0 if site == "Motorway service area" else 0.0, 1.0 if site in ("Harbour", "Seafront car park") else 0.0,
            1.0 if site == "Rural crossroads" else 0.0)


# ------------------------------------------------------------------------------------------------------ the record
def spells(rows, end):
    out = []
    for k, (t, st) in enumerate(rows):
        b = rows[k + 1][0] if k + 1 < len(rows) else end
        if st != "Available":
            out.append((t, b, st))
    return out


def excl_windows(R, hub, visits_key="visits"):
    out = [(a, b + W.EXCL_TAIL) for a, b in R[visits_key][hub]]
    out += [(a, b + W.EXCL_TAIL) for a, b in R["dso"][hub]]
    return out


def availability(R, key, a, b):
    hub = R["units"][key]["hub"]
    iv = [(x, y, st) for x, y, st in spells(R["rows"][key], R["end"])]
    a = max(a, R["units"][key]["start"])
    return W.schedule4(iv, excl_windows(R, hub), a, b)


def down_at(sp, starts, t):
    """Whether a unit was Offline or Faulted at t (a spell begun before t and not yet ended)."""
    i = bisect.bisect_left(starts, t) - 1
    return i >= 0 and sp[i][1] > t and sp[i][2] in ("Offline", "Faulted")


def comms_jobs(R):
    out = {}
    for w in R["wo"]:
        if w["kind"] == "comms" and w["key"]:
            out.setdefault(w["key"], []).append(w["logged"])
    return out


def classify(R, window=360, comms_as_hangs=False):
    """Per hub, the clusters of Offline rows in which every unit online at the time went Offline (a pillar power-down
    of the whole hub); per HX150, each Offline spell as pillar, repair, hang or comms, its power-ups and its hangs."""
    C = dict(clusters={}, units={})
    cj = comms_jobs(R)
    for h in R["hubs"]:
        keys = hub_keys(R, h["code"])
        sp = {k: spells(R["rows"][k], R["end"]) for k in keys}
        starts = {k: [a for a, _, _ in sp[k]] for k in keys}
        offs = sorted((a, k) for k in keys for a, b, st in sp[k] if st == "Offline")
        clusters, i = [], 0
        while i < len(offs):
            j = i
            while j + 1 < len(offs) and offs[j + 1][0] - offs[i][0] <= window:
                j += 1
            members = set(k for _, k in offs[i:j + 1])
            t0 = offs[i][0]
            if len(members) >= 2:
                online = set(k for k in keys if R["units"][k]["start"] <= t0 and not down_at(sp[k], starts[k], t0 - 60))
                if online <= members:
                    clusters.append((t0, offs[j][0], members))
            i = j + 1
        C["clusters"][h["code"]] = clusters
        cl_starts = [(c[0], c[1]) for c in clusters]
        cl0 = [c[0] for c in cl_starts]
        for k in keys:
            if R["units"][k]["model"] != "HX150":
                continue
            ups, hangs, faults, kinds = [], [], [], []
            prev = None
            for a, b, st in sp[k]:
                if st == "Faulted":
                    faults.append((a, b))
                elif st == "Offline":
                    ci = bisect.bisect_right(cl0, a + 5) - 1
                    pillar = ci >= 0 and cl_starts[ci][0] - 5 <= a <= cl_starts[ci][1] + 5
                    if prev is not None and prev[2] == "Faulted" and abs(prev[1] - a) <= 1:
                        kind = "repair"
                    elif pillar:
                        kind = "pillar"
                    elif b >= R["end"]:
                        kind = "open"           # still Offline when the record ends: its outcome is not on record
                    elif not comms_as_hangs and b - a >= 3 * 3600 and any(a - 900 <= x <= b for x in cj.get(k, [])):
                        kind = "comms_repair"
                    elif b - a >= 3 * 3600 or (bisect.bisect_left(cl0, b) > bisect.bisect_right(cl0, a + 1800)):
                        kind = "hang"
                    else:
                        kind = "comms"
                    kinds.append((a, b, kind))
                    if kind == "hang":
                        hangs.append((a - 750, b))
                    if kind in ("pillar", "repair", "hang", "comms_repair") and b < R["end"]:
                        ups.append(b)
                prev = (a, b, st)
            C["units"][k] = dict(ups=sorted(ups), hangs=hangs, faults=faults, kinds=kinds)
    return C


# ------------------------------------------------------------------------------------------------------ the clock
def life_table(R, C, ups_fn=None, kmax=400):
    """Exposure and hangs by day since power-up, every HX150 spell from a power-up to the next power-up, a hang or
    the end of the record."""
    expo = np.zeros(kmax + 1)
    ev = np.zeros(kmax + 1)
    for k in hx_keys(R):
        u = C["units"][k]
        ups = ups_fn(k) if ups_fn else u["ups"]
        start = R["units"][k]["start"]
        marks = sorted([(t, "up") for t in ups] + [(t, "hang") for t, _ in u["hangs"]] + [(a, "fault") for a, _ in u["faults"]])
        last = None
        for t, kind in marks:
            if last is not None:
                tau = (t - last) / float(DAY)
                n = int(min(tau, kmax))
                expo[:n] += 1.0
                if n < kmax:
                    expo[n] += tau - n
                if kind == "hang":
                    ev[min(n, kmax)] += 1
                last = None
            if kind == "up":
                last = t
        if last is not None:
            tau = (R["end"] - last) / float(DAY)
            n = int(min(tau, kmax))
            expo[:n] += 1.0
            if n < kmax:
                expo[n] += tau - n
        del start
    return expo, ev


def hazard_binned(expo, ev, width=5, plateau=90):
    """A life table read in bins of width days below the plateau and as one pooled rate from it on."""
    kmax = len(expo) - 1
    h = np.zeros(kmax + 1)
    for b0 in range(0, plateau, width):
        e, x = ev[b0:b0 + width].sum(), expo[b0:b0 + width].sum()
        h[b0:b0 + width] = e / x if x > 0 else 0.0
    e, x = ev[plateau:].sum(), expo[plateau:].sum()
    h[plateau:] = e / x if x > 0 else 0.0
    return h


def hazard_daily(expo, ev, plateau=90):
    h = np.where(expo > 0, ev / np.maximum(expo, 1e-9), 0.0)
    e, x = ev[plateau:].sum(), expo[plateau:].sum()
    h[plateau:] = e / x if x > 0 else 0.0
    return h


def hazard_onset(expo, ev):
    """A fitted onset: nothing before a, rising linearly to c at b, flat after; a and b by grid, c in closed form."""
    kmax = len(expo) - 1
    tau = np.arange(kmax + 1) + 0.5
    best = None
    n = ev.sum()
    for a in range(55, 90):
        for b in range(a + 2, a + 35):
            g = np.clip((tau - a) / float(b - a), 0.0, 1.0)
            G = (g * expo).sum()
            if G <= 0 or (ev[g <= 0]).sum() > 0:
                continue
            c = n / G
            ll = (ev[g > 0] * np.log(c * g[g > 0])).sum() - c * G
            if best is None or ll > best[0]:
                best = (ll, a, b, c)
    _, a, b, c = best
    return c * np.clip((tau - a) / float(b - a), 0.0, 1.0), (a, b, c)


def tau_from_hazard(h):
    """The inverse cumulative of a daily hazard array, for the simulation engine."""
    H = np.concatenate([[0.0], np.cumsum(h)])

    def f(E):
        i = int(np.searchsorted(H, E))
        if i >= len(H):
            return len(h) + (E - H[-1]) / max(h[-1], 1e-9)
        i = max(i, 1)
        rate = h[i - 1]
        return (i - 1) + ((E - H[i - 1]) / rate if rate > 0 else 0.0)
    return f


# --------------------------------------------------------------------------------------------- per-hub estimates
def estimates(R, C):
    """What the record says about each hub and unit: callout attendance, fault rates and repair time, comms
    downtime, supply interruptions, the visits' isolation timing, the other pillar power-downs, hang downtime."""
    yrs = {k: (R["end"] - R["units"][k]["start"]) / YEAR_S for k in R["units"]}
    E = dict(att={}, frate={}, rep={}, comms={}, dso_rate={}, dso_dur={}, visit_off={}, other_pd={}, hang_dt={},
             iso_dt={}, unit_frate={})
    all_f, all_rep, all_comms = [], [], []
    for h in R["hubs"]:
        code = h["code"]
        keys = hub_keys(R, code)
        calls = [(w["arrive"] - w["logged"]) / float(DAY) for w in R["wo"]
                 if w["hub"] == code and w["arrive"] is not None and w["kind"] in ("fault", "comms", "hang", "rc_repair")]
        hangs = [(b - a) / float(DAY) for k in hx_keys(R, code) for a, b in C["units"][k]["hangs"]]
        E["att"][code] = float(np.mean(calls)) if calls else 1.5
        E["hang_dt"][code] = float(np.mean(hangs)) if hangs else E["att"][code]
        nf, ty, reps = 0, 0.0, []
        for k in hx_keys(R, code):
            u = C["units"][k]
            nf += len(u["faults"])
            ty += yrs[k]
            E["unit_frate"][k] = len(u["faults"]) / max(yrs[k], 0.2)
            for (a, b) in u["faults"]:
                rep = [y - x for x, y, kd in u["kinds"] if kd == "repair" and abs(x - b) <= 1]
                reps.append((b - a + (rep[0] if rep else 0)) / float(DAY))
            co = [(y - x) for x, y, kd in u["kinds"] if kd == "comms"]
            E["comms"][k] = (len(co) / max(yrs[k], 0.2), float(np.mean(co)) if co else 1800.0)
            all_comms.append(E["comms"][k])
        E["frate"][code] = nf / max(ty, 0.2)
        E["rep"][code] = float(np.mean(reps)) if reps else None
        all_f.append((nf, ty))
        all_rep += reps
        hy = (R["end"] - 0) / YEAR_S
        E["dso_rate"][code] = len(R["dso"][code]) / hy
        E["dso_dur"][code] = [b - a for a, b in R["dso"][code]] or [3600]
        offs, durs = [], []
        for c0, c1, m in C["clusters"][code]:
            for a, b in R["visits"][code]:
                if a <= c0 <= b + 3600:
                    offs.append(c0 - a)
        E["visit_off"][code] = float(np.median(offs)) if offs else 5400.0
        vis = []
        for k in hx_keys(R, code):
            for x, y, kd in C["units"][k]["kinds"]:
                if kd == "pillar" and any(a <= x <= b + 3600 for a, b in R["visits"][code]):
                    vis.append(y - x)
        E["visit_dur"] = E.get("visit_dur", {})
        E["visit_dur"][code] = float(np.median(vis)) if vis else 5400.0
        other = []
        for c0, c1, m in C["clusters"][code]:
            if any(a <= c0 <= b + 3600 for a, b in R["visits"][code]):
                continue
            if any(a - 600 <= c0 <= b + 1800 for a, b in R["dso"][code]):
                continue
            other.append(c0)
        iso = []
        for k in hx_keys(R, code):
            for x, y, kd in C["units"][k]["kinds"]:
                if kd == "pillar" and any(abs(x - c0) <= 600 for c0 in other):
                    iso.append(y - x)
        E["other_pd"][code] = (len(other) / hy, float(np.mean(iso)) if iso else 0.0)
    cf, cfd = 0, []
    for k in hx_keys(R):
        sp = [(x, y) for x, y, kd in C["units"][k]["kinds"] if kd == "comms_repair"]
        cf += len(sp)
        cfd += [(y - x) / float(DAY) for x, y in sp]
    E["fleet_cf"] = cf / sum(yrs[k] for k in hx_keys(R))
    E["cf_dt"] = float(np.mean(cfd)) if cfd else 0.0
    E["fleet_frate"] = sum(n for n, _ in all_f) / sum(t for _, t in all_f)
    E["fleet_rep"] = float(np.mean(all_rep))
    E["fleet_comms"] = (float(np.mean([r for r, _ in all_comms])), float(np.mean([d for _, d in all_comms])))
    for code in E["rep"]:
        if E["rep"][code] is None:
            E["rep"][code] = E["fleet_rep"]
    return E


def units27(R):
    """The 2027 asset base: every HX150 on record and a new unit at each programme hub the programme names."""
    out = []
    for h in R["hubs"]:
        for k in hx_keys(R, h["code"]):
            out.append((h["code"], k, False))
        p = R["programme"].get(h["code"])
        if p and p["new_unit"]:
            out.append((h["code"], "NEW-" + h["code"], True))
    return out


def excl27_days(R, E, code):
    ex = sum((b - a + W.EXCL_TAIL) for a, b in R["visits27"][code]) / float(DAY)
    ex += E["dso_rate"][code] * (np.mean(E["dso_dur"][code]) + W.EXCL_TAIL) / float(DAY)
    return ex


# ------------------------------------------------------------------------------------------- the default path
def unit_rates(R, C, keys, a=0, b=None):
    b = R["end"] if b is None else b
    out = {}
    for k in keys:
        u = C["units"][k]
        s = max(a, R["units"][k]["start"])
        yrs = max((b - s) / YEAR_S, 0.05)
        nh = sum(1 for t, _ in u["hangs"] if s <= t < b)
        nf = sum(1 for t, _ in u["faults"] if s <= t < b)
        hdt = [(y - x) / float(DAY) for x, y in u["hangs"] if s <= x < b]
        out[k] = dict(h=nh / yrs, f=nf / yrs, hdt=float(np.mean(hdt)) if hdt else None, yrs=yrs)
    return out


def pillar_downtime(R, C, k, a, b):
    """Non-excluded pillar Offline time a year that is not a visit or an interruption (the RC50's isolations)."""
    hub = R["units"][k]["hub"]
    ex = excl_windows(R, hub)
    iv = [(x, y, "Offline") for x, y, kd in C["units"][k]["kinds"] if kd == "pillar" and a <= x < b]
    s = max(a, R["units"][k]["start"])
    av = W.schedule4(iv, ex, s, b)
    return (1 - av) * (b - s) / float(DAY) / ((b - s) / YEAR_S)


def avail27(R, E, code, hang_rate, hang_dt, frate, rep, comms, iso_days):
    down = hang_rate * hang_dt + frate * rep + comms[0] * comms[1] / float(DAY) + iso_days + E["fleet_cf"] * E["cf_dt"]
    return 1.0 - down / (365.0 - excl27_days(R, E, code))


def route_rates(R, C, E, rates=None, a=0, b=None, mode="unit"):
    """Rung 0: each unit's hang and fault rates carried into 2027 with their downtime; the RC50's own isolation
    minutes dropped where the programme takes it out; new units at fleet rates."""
    b = R["end"] if b is None else b
    keys = hx_keys(R)
    ur = unit_rates(R, C, keys, a, b) if rates is None else rates
    tot_h = sum(ur[k]["h"] * ur[k]["yrs"] for k in keys) / sum(ur[k]["yrs"] for k in keys)
    out = {}
    for code, k, new in units27(R):
        if new:
            hr, fr, cm = tot_h, E["fleet_frate"], E["fleet_comms"]
        else:
            hr, fr, cm = ur[k]["h"], (ur[k]["f"] if mode == "unit" else E["frate"][code]), E["comms"][k]
        hdt = (ur[k]["hdt"] if (not new and ur[k]["hdt"]) else E["hang_dt"][code])
        iso = 0.0 if code in R["programme"] else (pillar_downtime(R, C, k, a, b) if not new else 0.0)
        out.setdefault(code, []).append(avail27(R, E, code, hr, hdt, fr, E["rep"][code], cm, iso))
    return out


def side_set(av, line=0.99):
    return sorted(c for c, v in av.items() if min(v) < line)


def backtests(R, C, E):
    """The rate route's validation: 2025 from 2023-24 and January to October 2026 from 2023-25 for every unit, and
    each unit left out (its hub's other units, else the fleet). Mean absolute error in points and sides kept."""
    keys = [k for k in hx_keys(R) if R["units"][k]["start"] < W.ts(W.dt.datetime(2024, 1, 1, tzinfo=W.UTC))]
    out = {}
    for label, fit_b, a, b in (("2025", W.ts(W.dt.datetime(2025, 1, 1, tzinfo=W.UTC)), W.ts(W.dt.datetime(2025, 1, 1, tzinfo=W.UTC)),
                                W.ts(W.dt.datetime(2026, 1, 1, tzinfo=W.UTC))),
                               ("2026", W.ts(W.dt.datetime(2026, 1, 1, tzinfo=W.UTC)), W.ts(W.dt.datetime(2026, 1, 1, tzinfo=W.UTC)), R["end"])):
        ur = unit_rates(R, C, keys, 0, fit_b)
        errs, sides = [], 0
        for k in keys:
            code = R["units"][k]["hub"]
            act = availability(R, k, a, b)
            hdt = ur[k]["hdt"] or E["hang_dt"][code]
            down = ur[k]["h"] * hdt + ur[k]["f"] * E["rep"][code] + E["comms"][k][0] * E["comms"][k][1] / float(DAY) + \
                pillar_downtime(R, C, k, 0, fit_b) + E["fleet_cf"] * E["cf_dt"]
            pred = 1.0 - down / 365.0
            errs.append(abs(pred - act) * 100)
            sides += (pred < 0.99) == (act < 0.99)
        out[label] = (float(np.mean(errs)), sides, len(keys))
    errs, sides = [], 0
    for k in keys:
        code = R["units"][k]["hub"]
        mates = [m for m in hx_keys(R, code) if m != k] or [m for m in keys if m != k]
        ur = unit_rates(R, C, mates)
        hr = sum(ur[m]["h"] * ur[m]["yrs"] for m in mates) / sum(ur[m]["yrs"] for m in mates)
        act = availability(R, k, R["units"][k]["start"], R["end"])
        down = hr * E["hang_dt"][code] + E["frate"][code] * E["rep"][code] + E["comms"][k][0] * E["comms"][k][1] / float(DAY) + \
            pillar_downtime(R, C, k, 0, R["end"]) + E["fleet_cf"] * E["cf_dt"]
        pred = 1.0 - down / 365.0
        errs.append(abs(pred - act) * 100)
        sides += (pred < 0.99) == (act < 0.99)
    out["loo"] = (float(np.mean(errs)), sides, len(keys))
    return out


# --------------------------------------------------------------------------------------------- the cheap family
def unit_years(R, C, E, rc_jobs=None):
    """One row per HX150 and calendar year: hangs, exposure and every covariate the pack holds."""
    hi = hubinfo(R)
    rows = []
    for k in hx_keys(R):
        code = R["units"][k]["hub"]
        mw, co, ru = site_flags(hi[code]["site"])
        for y in (2023, 2024, 2025, 2026):
            a = W.ts(W.dt.datetime(y, 1, 1, tzinfo=W.UTC))
            b = min(W.ts(W.dt.datetime(y + 1, 1, 1, tzinfo=W.UTC)), R["end"])
            s = max(a, R["units"][k]["start"])
            if b - s < 30 * DAY:
                continue
            nh = sum(1 for t, _ in C["units"][k]["hangs"] if s <= t < b)
            nvis = sum(1 for x, _ in R["visits"][code] if a <= x < b) * YEAR_S / (b - a)
            ndso = sum(1 for x, _ in R["dso"][code] if a <= x < b) * YEAR_S / (b - a)
            nrc = sum(1 for w in R["wo"] if w["hub"] == code and w["kind"].startswith("rc_") and a <= w["logged"] < b) * YEAR_S / (b - a)
            nhx = sum(1 for m in hx_keys(R, code) if R["units"][m]["start"] < b)
            comm = W.utc(R["units"][k]["start"]).year if R["units"][k]["start"] > 0 else 2022
            rows.append(dict(key=k, hub=code, y=y, n=nh, expo=(b - s) / YEAR_S,
                             x=[mw, co, ru, nhx, comm - 2021, R["cpd"].get(k, 0.0), nvis, ndso, nrc]))
    return rows


def x27(R, E, code, key, new, rows):
    hi = hubinfo(R)
    mw, co, ru = site_flags(hi[code]["site"])
    hub_rows = [r for r in rows if r["hub"] == code]
    nhx = len([1 for c, k, n in units27(R) if c == code])
    cpd = R["cpd"].get(key, 0.0) if not new else float(np.mean([R["cpd"].get(k, 0.0) for k in hx_keys(R, code)]))
    nrc = 0.0 if code in R["programme"] else float(np.mean([r["x"][8] for r in hub_rows]))
    comm = 5 if new else ((W.utc(R["units"][key]["start"]).year if R["units"][key]["start"] > 0 else 2022) - 2021)
    return [mw, co, ru, nhx, comm, cpd, float(len(R["visits27"][code])), E["dso_rate"][code], nrc]


def route_glm(R, C, E, cols=None):
    import statsmodels.api as sm
    rows = unit_years(R, C, E)
    cols = list(range(9)) if cols is None else cols
    X = np.array([[r["x"][c] for c in cols] for r in rows])
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xs = sm.add_constant((X - mu) / sd, has_constant="add")
    Y = np.array([r["n"] for r in rows])
    off = np.log(np.array([r["expo"] for r in rows]))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = sm.GLM(Y, Xs, family=sm.families.Poisson(), offset=off).fit_regularized(alpha=0.002, L1_wt=0.0, maxiter=300)
    beta = np.asarray(m.params)
    out = {}
    for code, k, new in units27(R):
        xv = (np.array([x27(R, E, code, k, new, rows)[c] for c in cols]) - mu) / sd
        rate = float(np.exp(beta[0] + xv @ beta[1:]))
        cm = E["fleet_comms"] if new else E["comms"][k]
        fr = E["fleet_frate"] if new else E["unit_frate"][k]
        iso = 0.0 if (code in R["programme"] or new) else pillar_downtime(R, C, k, 0, R["end"])
        out.setdefault(code, []).append(avail27(R, E, code, rate, E["hang_dt"][code], fr, E["rep"][code], cm, iso))
    return out, beta


def _tree(rows, depth, min_expo=8.0):
    n = sum(r["n"] for r in rows)
    ex = sum(r["expo"] for r in rows)
    lam = n / ex if ex else 0.0
    def dev(rs):
        nn = sum(r["n"] for r in rs); ee = sum(r["expo"] for r in rs)
        l = nn / ee if ee else 0.0
        return sum((r["n"] * math.log(r["n"] / (l * r["expo"])) if r["n"] > 0 else 0.0) - (r["n"] - l * r["expo"]) for r in rs)
    if depth == 0 or ex < 2 * min_expo:
        return ("leaf", lam)
    base = dev(rows)
    best = None
    for c in range(len(rows[0]["x"])):
        vals = sorted(set(r["x"][c] for r in rows))
        for v0, v1 in zip(vals[:-1], vals[1:]):
            thr = (v0 + v1) / 2.0
            L = [r for r in rows if r["x"][c] <= thr]
            Rr = [r for r in rows if r["x"][c] > thr]
            if sum(r["expo"] for r in L) < min_expo or sum(r["expo"] for r in Rr) < min_expo:
                continue
            g = base - dev(L) - dev(Rr)
            if best is None or g > best[0]:
                best = (g, c, thr, L, Rr)
    if best is None or best[0] <= 1e-6:
        return ("leaf", lam)
    return ("split", best[1], best[2], _tree(best[3], depth - 1, min_expo), _tree(best[4], depth - 1, min_expo))


def _predict(t, x):
    while t[0] == "split":
        t = t[3] if x[t[1]] <= t[2] else t[4]
    return t[1]


def route_tree(R, C, E):
    rows = unit_years(R, C, E)
    t = _tree(rows, 3)
    out = {}
    for code, k, new in units27(R):
        rate = _predict(t, x27(R, E, code, k, new, rows))
        cm = E["fleet_comms"] if new else E["comms"][k]
        fr = E["fleet_frate"] if new else E["unit_frate"][k]
        iso = 0.0 if (code in R["programme"] or new) else pillar_downtime(R, C, k, 0, R["end"])
        out.setdefault(code, []).append(avail27(R, E, code, rate, E["hang_dt"][code], fr, E["rep"][code], cm, iso))
    return out, t


def route_daily(R, C, E, only_full=False):
    """A daily model of the hangs on the RC50's work in the last 60 days and the days since its last job, beside the
    coast: each unit-day a row, collapsed to its cells, carried at the programme's no-RC50 values."""
    import statsmodels.api as sm
    hi = hubinfo(R)
    cells = {}
    for code in [h["code"] for h in R["hubs"]]:
        jobs = sorted((w["arrive"] or w["logged"]) for w in R["wo"] if w["hub"] == code and w["kind"].startswith("rc_")
                      and (not only_full or (w["kind"] == "rc_service" and w.get("full", True))))
        co = site_flags(hi[code]["site"])[1]
        for k in hx_keys(R, code):
            hdays = set(int(t // DAY) for t, _ in C["units"][k]["hangs"])
            d0 = int(max(0, R["units"][k]["start"]) // DAY)
            ji = 0
            for d in range(d0, int(R["end"] // DAY)):
                t = d * DAY
                while ji < len(jobs) and jobs[ji] < t:
                    ji += 1
                recent = sum(1 for j in jobs[max(0, ji - 12):ji] if j >= t - 60 * DAY)
                since = min(60, int((t - jobs[ji - 1]) // DAY)) if ji > 0 else 60
                key = (co, recent, since // 10)
                n, x = cells.get(key, (0, 0))
                cells[key] = (n + (1 if d in hdays else 0), x + 1)
    keys = sorted(cells)
    X = sm.add_constant(np.array([[c[0], c[1], c[2]] for c in keys], float), has_constant="add")
    Y = np.array([cells[c][0] for c in keys], float)
    off = np.log(np.array([cells[c][1] for c in keys], float))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = sm.GLM(Y, X, family=sm.families.Poisson(), offset=off).fit_regularized(alpha=0.002, L1_wt=0.0, maxiter=300)
    beta = np.asarray(m.params)
    out = {}
    for code, k, new in units27(R):
        co = site_flags(hi[code]["site"])[1]
        if code in R["programme"]:
            x = [1.0, co, 0.0, 6.0]
        else:
            x = [1.0, co, 2.0, 1.5]
        rate = float(np.exp(np.array(x) @ beta)) * 365.0
        cm = E["fleet_comms"] if new else E["comms"][k]
        fr = E["fleet_frate"] if new else E["unit_frate"][k]
        iso = 0.0 if (code in R["programme"] or new) else pillar_downtime(R, C, k, 0, R["end"])
        out.setdefault(code, []).append(avail27(R, E, code, rate, E["hang_dt"][code], fr, E["rep"][code], cm, iso))
    return out, beta


def route_hier(R, C, E):
    """Hang rates shrunk unit to hub to fleet by gamma-Poisson empirical Bayes."""
    keys = hx_keys(R)
    ur = unit_rates(R, C, keys)
    n = np.array([ur[k]["h"] * ur[k]["yrs"] for k in keys])
    t = np.array([ur[k]["yrs"] for k in keys])
    lam = n.sum() / t.sum()
    var = max(np.var(n / t) - lam / t.mean(), 1e-6)
    a_f = lam ** 2 / var
    hub_rate = {}
    for h in R["hubs"]:
        ks = hx_keys(R, h["code"])
        nn = sum(ur[k]["h"] * ur[k]["yrs"] for k in ks)
        tt = sum(ur[k]["yrs"] for k in ks)
        hub_rate[h["code"]] = (nn + a_f) / (tt + a_f / lam)
    shr = {}
    for k in keys:
        code = R["units"][k]["hub"]
        b = 4.0
        shr[k] = dict(ur[k])
        shr[k]["h"] = (ur[k]["h"] * ur[k]["yrs"] + b * hub_rate[code]) / (ur[k]["yrs"] + b)
    return route_rates(R, C, E, rates=shr)


def route_last(R, C, E):
    a = W.S26_START
    out = {}
    for code, k, new in units27(R):
        if new:
            out.setdefault(code, []).append(float(np.mean([availability(R, m, a, R["end"]) for m in hx_keys(R, code)])))
        else:
            out.setdefault(code, []).append(availability(R, k, a, R["end"]))
    return out


def route_smooth(R, C, E, alpha=0.3):
    out = {}
    months = []
    for y in (2023, 2024, 2025, 2026):
        for m in range(1, 13):
            if y == 2026 and m > 10:
                break
            a = W.ts(W.dt.datetime(y, m, 1, tzinfo=W.UTC))
            b = W.ts(W.dt.datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=W.UTC))
            months.append((a, b))
    for code, k, new in units27(R):
        ks = hx_keys(R, code) if new else [k]
        lev = []
        for kk in ks:
            level = None
            for a, b in months:
                if b <= R["units"][kk]["start"]:
                    continue
                v = availability(R, kk, a, b)
                level = v if level is None else alpha * v + (1 - alpha) * level
            lev.append(level)
        out.setdefault(code, []).append(float(np.mean(lev)))
    return out


# ------------------------------------------------------------------------------------------ the restart clock
def rc_calendar(R, C, E, code):
    """The RC50's own calendar on the record at a hub where it shares the HX150s' pillar: the share of months whose
    monthly job opened the cabinet (not an external inspection, not skipped), the days of the month and the minutes
    of the day it did, and the rate of the other isolations (cabinet repairs) the status history shows beside them."""
    cache = E.setdefault("rc_cal", {})
    if code in cache:
        return cache[code]
    months = {}
    for w in R["wo"]:
        if w["hub"] == code and w["kind"] == "rc_service" and w["arrive"] is not None:
            lt = W.local(w["arrive"])
            months.setdefault((lt.year, lt.month), []).append((w.get("full", True), lt.day, lt.hour * 60 + lt.minute))
    first, last = W.local(0), W.local(R["end"] - 1)
    n_months = (last.year - first.year) * 12 + last.month - first.month + 1
    full = [(d, m) for v in months.values() for f, d, m in v if f]
    p_full = len(set(k for k, v in months.items() if any(f for f, _, _ in v))) / float(n_months)
    serv = [w["arrive"] for w in R["wo"] if w["hub"] == code and w["kind"] == "rc_service" and w.get("full", True) and w["arrive"]]
    other = 0
    for c0, c1, m in C["clusters"][code]:
        if any(a <= c0 <= b + 3600 for a, b in R["visits"][code]) or any(a - 600 <= c0 <= b + 1800 for a, b in R["dso"][code]):
            continue
        if any(abs(c0 - t) <= 6 * 3600 for t in serv):
            continue
        other += 1
    cache[code] = dict(p_full=p_full, days=[d for d, _ in full] or [10], mins=[m for _, m in full] or [600],
                       other_rate=other / ((R["end"] - 0) / YEAR_S))
    return cache[code]


def regime27(R, E, code, rng, no_resets=False, calendar=None):
    """2027 power-downs a hub's record supports: the plan's visits at the record's isolation timing, supply
    interruptions at the hub's rate, the other pillar power-downs where the RC50 stays, the programme works."""
    pds = []
    if not no_resets:
        for ws, we in R["visits27"][code]:
            s = ws + int(E["visit_off"][code])
            pds.append((s, s + int(E["visit_dur"][code]), "visit"))
        rate = E["dso_rate"][code] / YEAR_S
        t = W.HIST_END
        while rate > 0:
            t += int(rng.exponential(1.0 / rate))
            if t >= W.Y27_END:
                break
            d = E["dso_dur"][code][int(rng.integers(0, len(E["dso_dur"][code])))]
            pds.append((t, t + int(d), "dso"))
    p = R["programme"].get(code)
    orate, odur = E["other_pd"][code]
    if orate > 0 and odur > 0 and calendar is not None:
        stop = p["works"] if p else W.Y27_END
        y, m = 2026, 11
        while (y, m) <= (2027, 12):
            if rng.random() < calendar["p_full"]:
                d = int(calendar["days"][int(rng.integers(0, len(calendar["days"])))])
                mins = int(calendar["mins"][int(rng.integers(0, len(calendar["mins"])))])
                last_day = (W.dt.date(y + (m == 12), m % 12 + 1, 1) - W.dt.timedelta(days=1)).day
                t = W.from_local(y, m, min(d, last_day), 0, 0) + mins * 60 + 15 * 60
                if W.HIST_END <= t < stop:
                    pds.append((t, t + int(odur), "service"))
            m += 1
            if m == 13:
                y, m = y + 1, 1
        t = W.HIST_END
        while calendar["other_rate"] > 0:
            t += int(rng.exponential(YEAR_S / calendar["other_rate"]))
            if t >= stop:
                break
            pds.append((t, t + int(odur), "service"))
    elif orate > 0 and odur > 0:
        t = W.HIST_END
        stop = p["works"] if p else W.Y27_END
        while True:
            t += int(rng.exponential(YEAR_S / orate))
            if t >= stop:
                break
            pds.append((t, t + int(odur), "service"))
    if p:
        pds.append((p["works"], p["works"] + 5 * 3600, "works"))
    return sorted(pds)


def excl27(R, E, code):
    return [(a, b + W.EXCL_TAIL) for a, b in R["visits27"][code]]


def last_up(R, C, k):
    ups = C["units"][k]["ups"]
    return ups[-1] if ups else R["units"][k]["start"]


def sim27(R, C, E, h, reps=200, seed=W.SEED, no_resets=False, unit_fault=False, stat="mean", new_start=None, exclude=True,
          hang_pool=None, calendar=False, hubs=None):
    """Each 2027 unit's expected availability: the record's hang rate by day since power-up run through the hub's
    2027 power-downs, its attendance, fault rate, repair time and comms, averaged over simulated years. stat "reps"
    returns every simulated year (years by units); hang_pool draws each hang's downtime from recorded hang spells in
    place of the hub's attendance; calendar draws the RC50's isolations from the record's own calendar."""
    tau_fn = tau_from_hazard(h)
    out = {}
    by_hub = {}
    for code, k, new in units27(R):
        by_hub.setdefault(code, []).append((k, new))
    for i, (code, lst) in enumerate(sorted(by_hub.items())):
        if hubs is not None and code not in hubs:
            continue
        acc = np.zeros((reps, len(lst)))
        hacc = np.zeros((reps, len(lst)))
        for r in range(reps):
            rng = np.random.default_rng([seed, 777, i, r])
            cal = rc_calendar(R, C, E, code) if (calendar and not R["programme"].get(code)) else None
            pds = regime27(R, E, code, rng, no_resets=no_resets, calendar=cal)
            dso_ex = [(s, e + W.EXCL_TAIL) for s, e, kd in pds if kd == "dso"]
            ex = (excl27(R, E, code) + dso_ex) if exclude else []
            for j, (k, new) in enumerate(lst):
                t_up = ((R["programme"][code]["works"] + 5 * 3600) if new_start is None else new_start) if new else last_up(R, C, k)
                cm = E["fleet_comms"] if new else E["comms"][k]
                fr = (E["frate"][code] or E["fleet_frate"]) if (new or not unit_fault) else E["unit_frate"][k]
                iv, _, hg, _ = W.run_hx(rng, W.HIST_END, W.Y27_END, pds, t_up, E["att"][code], fr, tau_fn=tau_fn,
                                      comms_rate=cm[0] / 365.0, comms_min=(max(16, int(cm[1] / 60 * 0.5)), max(17, int(cm[1] / 60 * 1.5))),
                                      cfrate_yr=E["fleet_cf"], hang_dt=hang_pool)
                acc[r, j] = W.schedule4(iv, ex, W.Y27_START, W.Y27_END)
                hacc[r, j] = sum(1 for x in hg if W.Y27_START <= x[0] < W.Y27_END)
        if stat == "hangs":
            out[code] = list(hacc.mean(axis=0))
        elif stat == "reps":
            out[code] = acc
        else:
            out[code] = list(np.median(acc, axis=0) if stat == "median" else acc.mean(axis=0))
    return out


def hub_readings(reps_out, line=0.99):
    """From every simulated year: each unit's expected availability (the golden's reading, the lowest of them), the
    hub's expected lowest unit (the mean over years of its worst unit) and the event (the share of years in which
    some unit falls below the line)."""
    out = {}
    for code, acc in reps_out.items():
        worst = acc.min(axis=1)
        out[code] = dict(unit=float(acc.mean(axis=0).min()), lowest=float(worst.mean()), event=float((worst < line).mean()))
    return out


def hang_spells(R, C):
    """Every recorded hang's downtime (seconds), pooled over the fleet."""
    return [b - a for k in hx_keys(R) for a, b in C["units"][k]["hangs"] if b < R["end"]]


def clock_spells(R, C):
    """Every HX150 spell on the days-since-power-up clock: (days, hang) from a power-up to the next hang, power-up,
    fault or the end of the record, as the life table reads them."""
    out = []
    for k in hx_keys(R):
        u = C["units"][k]
        marks = sorted([(t, "up") for t in u["ups"]] + [(t, "hang") for t, _ in u["hangs"]] + [(a, "fault") for a, _ in u["faults"]])
        last = None
        for t, kind in marks:
            if last is not None:
                out.append(((t - last) / float(DAY), kind == "hang"))
                last = None
            if kind == "up":
                last = t
        if last is not None:
            out.append(((R["end"] - last) / float(DAY), False))
    return out


def weibull_fit(R, C):
    """A two-parameter Weibull on the days-since-power-up clock, each spell censored at its next power-up, fault or
    the record's end; its log-likelihood beside the fitted onset's on the same spells, and its daily hazard."""
    from scipy.optimize import minimize
    sp = clock_spells(R, C)
    t = np.array([x for x, _ in sp]) + 1e-6
    d = np.array([e for _, e in sp], float)

    def nll(th):
        k, lam = np.exp(th)
        z = t / lam
        return -((d * (np.log(k) - np.log(lam) + (k - 1) * np.log(z))).sum() - (z ** k).sum())
    best = min((minimize(nll, x0, method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-8, fatol=1e-8))
                for x0 in ([np.log(2.0), np.log(150.0)], [np.log(5.0), np.log(100.0)], [np.log(10.0), np.log(90.0)])),
               key=lambda m: m.fun)
    k, lam = np.exp(best.x)
    ll_w = -best.fun
    expo, ev = life_table(R, C)
    _, (a, b, c) = hazard_onset(expo, ev)

    def onset_cum(x):
        x = np.asarray(x, float)
        ramp = np.clip(x - a, 0, b - a)
        return c * (ramp ** 2 / (2.0 * (b - a)) + np.clip(x - b, 0, None))

    def onset_h(x):
        return c * np.clip((np.asarray(x, float) - a) / float(b - a), 0.0, 1.0)
    he = onset_h(t[d > 0])
    ll_o = float(np.log(np.maximum(he, 1e-300)).sum() - onset_cum(t).sum()) if (he > 0).all() else -np.inf
    days = np.arange(len(expo))
    S = np.exp(-(days / lam) ** k)
    S1 = np.exp(-((days + 1) / lam) ** k)
    hw = 1.0 - S1 / np.maximum(S, 1e-300)
    return dict(k=float(k), lam=float(lam), ll_weibull=float(ll_w), ll_onset=ll_o, aic_weibull=4 - 2 * float(ll_w),
                aic_onset=6 - 2 * ll_o, onset=(a, b, c), h=hw, n_spells=len(sp), n_hangs=int(d.sum()))


def dp27(R, C, E, h, unit_fault=False):
    """The same forecast by day-step arithmetic instead of simulation: the distribution of days since power-up and
    of days hung, carried day by day through the hub's 2027 visits, its daily interruption and fault chances."""
    kmax = len(h) - 1
    att_j = 60
    out = {}
    from scipy.stats import gamma as G
    from scipy.integrate import quad
    for code, k, new in units27(R):
        att = E["att"][code]
        # a hang's downtime: the callout (gamma(3) about the hub's attendance, three hours at least) and a restart of
        # about a quarter of an hour; a hang falls at mid-day on average, so a hang of age a days at the start of a day
        # has been down a - 0.5 days, and the day holds the part of its downtime between a - 0.5 and a + 0.5
        lag = 15 * 60 / float(DAY)

        def sf_t(t, att=att):
            t = t - lag
            return 1.0 if t < 0.125 else float(G.sf(t, 3, scale=att / 3.0))
        a = np.arange(att_j) + 1.0
        s_start = np.array([sf_t(x - 0.5) for x in a])
        s_end = np.array([sf_t(x + 0.5) for x in a])
        rel = np.where(s_start > 1e-12, 1 - s_end / np.maximum(s_start, 1e-12), 1.0)
        day_dt = np.array([quad(sf_t, x - 0.5, x + 0.5, points=[0.125 + lag], limit=80)[0] for x in a])
        day_dt = np.where(s_start > 1e-12, day_dt / np.maximum(s_start, 1e-12), 0.0)
        rel0 = 1 - sf_t(0.5)
        dt0 = quad(sf_t, 0.0, 0.5, points=[0.125 + lag], limit=80)[0]
        fr = (E["frate"][code] or E["fleet_frate"]) if (new or not unit_fault) else E["unit_frate"][k]
        f = (fr + E["fleet_cf"]) / 365.0
        q = E["dso_rate"][code] / 365.0
        p = R["programme"].get(code)
        orate, odur = E["other_pd"][code]
        qo = (orate / 365.0) if not p else 0.0
        t_up = (p["works"] + 5 * 3600) if new else last_up(R, C, k)
        k0 = int(min(kmax, max(0, (W.HIST_END - t_up) // DAY)))
        pu = np.zeros(kmax + 1)
        pu[k0] = 1.0
        ph = np.zeros(att_j)
        visit_days = set(int((s - W.HIST_END) // DAY) for s, _ in R["visits27"][code])
        works_day = int((p["works"] - W.HIST_END) // DAY) if p else None
        hung = 0.0
        ndays = int((W.Y27_END - W.HIST_END) // DAY)
        y27 = int((W.Y27_START - W.HIST_END) // DAY)
        for d in range(ndays):
            if d in visit_days or d == works_day:
                pu = np.concatenate([[pu.sum() + ph.sum()], np.zeros(kmax)])
                ph = np.zeros(att_j)
            else:
                qq = q + ((orate / 365.0) if (works_day is None or d < works_day) else 0.0)
                m = qq * (pu.sum() + ph.sum())
                pu *= (1 - qq)
                ph *= (1 - qq)
                pu[0] += m
            fm = f * pu.sum()
            pu *= (1 - f)
            pu[0] += fm
            nh = (pu * h).sum()
            pu = pu * (1 - h)
            pu = np.concatenate([[0.0], pu[:-1]]) + np.concatenate([np.zeros(kmax), [pu[-1]]])
            if d >= y27:
                hung += (ph * day_dt).sum() + nh * dt0
            released = (ph * rel).sum() + nh * rel0
            ph = np.concatenate([[nh * (1 - rel0)], (ph * (1 - rel))[:-1]])
            pu[0] += released
        cm = E["fleet_comms"] if new else E["comms"][k]
        iso = 0.0 if (p or new) else (E["other_pd"][code][0] * E["other_pd"][code][1] / float(DAY))
        down = hung + fr * E["rep"][code] + cm[0] * cm[1] / float(DAY) + iso + E["fleet_cf"] * E["cf_dt"]
        out.setdefault(code, []).append(1.0 - down / (365.0 - excl27_days(R, E, code)))
    return out


def golden(R, C=None, E=None, reps=200, seed=W.SEED):
    C = classify(R) if C is None else C
    E = estimates(R, C) if E is None else E
    expo, ev = life_table(R, C)
    h5 = hazard_binned(expo, ev, 5)
    av = sim27(R, C, E, h5, reps=reps, seed=seed)
    return dict(av=av, set=side_set(av), C=C, E=E, expo=expo, ev=ev, h=h5)


def standing(R, C, E, reps=200):
    expo, ev = life_table(R, C)
    hs = {"5-day life table": hazard_binned(expo, ev, 5), "1-day life table": hazard_daily(expo, ev),
          "fitted onset": hazard_onset(expo, ev)[0]}
    out = {}
    for name, h in hs.items():
        out[name + ", simulated"] = sim27(R, C, E, h, reps=reps)
        out[name + ", day-step"] = dp27(R, C, E, h)
    return out


def rung_workorder_clock(R, C, E, reps=150):
    """The restart clock built from the work orders alone: every RC50 job a power-up for every unit at its hub,
    beside the visits, the interruptions and the unit's own restarts."""
    jobs = {}
    for w in R["wo"]:
        if w["kind"].startswith("rc_"):
            if w["done"] is not None:
                jobs.setdefault(w["hub"], []).append(w["done"])

    def ups_fn(k):
        code = R["units"][k]["hub"]
        own = [b for x, b, kd in C["units"][k]["kinds"] if kd in ("repair", "hang")]
        vis = [b for _, b in R["visits"][code]]
        dso = [b for _, b in R["dso"][code]]
        return sorted(t for t in own + vis + dso + jobs.get(code, []) if t >= R["units"][k]["start"])
    expo, ev = life_table(R, C, ups_fn=ups_fn)
    h = hazard_binned(expo, ev, 5)
    return sim27(R, C, E, h, reps=reps)


def rung_no_resets(R, C, E, reps=150):
    expo, ev = life_table(R, C)
    return sim27(R, C, E, hazard_binned(expo, ev, 5), reps=reps, no_resets=True)
