"""task464 architecture 10: the interruption record the asks read (2023/24 to 2025/26).

Customers by substation and month, the operator's interruption log (control-system HV incidents and work-management LV
incidents in one extract, one row per site per restoration step), the mobile generation log and Ofgem's exceptional
event list. The asks' golden CI and CML come from the clean truth here; the pack writes the records as each system holds
them. Nothing here is read by the losses call.
"""
import datetime as dt
import numpy as np
import world as W
import sim as S

YEARS = [2023, 2024, 2025]          # regulatory years starting 1 April
FY_START = {y: dt.datetime(y, 4, 1) for y in YEARS + [2026]}


def customers_of(c, r):
    cls = c.cls if c.kind == "S" else None
    m = c.mean_kw if c.kind == "S" else 0
    if c.kind == "H":
        return 1
    per = {"dom": 2.2, "domPV": 2.0, "com": 1 / 9.0, "retail": 1 / 20.0, "ind": 1 / 60.0, "agr": 1 / 3.5}[cls]
    return max(3, int(round(m * per * (1 + r.normal(0, 0.04)))))


def month_list():
    out = []
    d = dt.date(2023, 4, 1)
    while d < dt.date(2026, 4, 1):
        out.append(d)
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return out


def customer_counts(conns):
    """Customers connected at each site at the end of each month, 2023-04 to 2026-03."""
    r = S.rng("customers")
    months = month_list()
    out = {}
    for c in conns:
        base = customers_of(c, r)
        drift = r.normal(0.0, 0.0018) * base
        series = []
        for i, mth in enumerate(months):
            if c.name == "Redburn Meadows":
                start = W.REDBURN_MEADOWS_ENERGISED
                k = (mth.year - start.year) * 12 + mth.month - start.month
                v = 0 if mth < dt.date(2025, 10, 1) else min(base, int(round(base * (0.18 + 0.15 * k))))
            else:
                v = int(round(base + drift * (i - 24) + r.normal(0, 0.6)))
            if c.kind == "H":
                v = 1                      # an HV-connected customer is one customer throughout
            series.append(max(0, v))
        out[c.key] = dict(zip(months, series))
    return out


def month_end(counts, key, when):
    m = dt.date(when.year, when.month, 1)
    return counts[key][m]


class Incident:
    def __init__(self, ref, circuit, voltage, category, cause, start, source):
        self.ref, self.circuit, self.voltage, self.category, self.cause, self.start, self.source = (
            ref, circuit, voltage, category, cause, start, source)
        self.steps = []          # (time, site_key, change) change > 0 off, < 0 restored
        self.exceptional = False
        self.dup_of = None


def _beyond(feeder, sections, sec_id):
    """Connection keys beyond a section (those it supplies)."""
    s = [x for x in sections if x.id == sec_id][0]
    return list(s.down)


def simulate(net):
    feeders, sections, conns = net["feeders"], net["sections"], net["conns"]
    counts = customer_counts(conns + net["neigh"])
    r = S.rng("interruptions" + W.REL_SALT)
    refs = iter(sorted(set(int(x) for x in r.choice(np.arange(410000, 999999), 3000, replace=False))))
    wo = iter(sorted(set(int(x) for x in r.choice(np.arange(5100000, 5999999), 3000, replace=False))))
    gen_units = ["MG%03d" % x for x in r.choice(np.arange(100, 400), 14, replace=False)]
    incidents, gens = [], []
    bykey = {c.key: c for c in conns}
    nop_feeders = set(a for a, b, _, _ in W.NOP_LINKS) | set(b for a, b, _, _ in W.NOP_LINKS)

    def t_in_year(y):
        return FY_START[y] + dt.timedelta(minutes=int(r.integers(0, 365 * 24 * 60)))

    def daytime(t):
        return t.replace(hour=int(r.integers(8, 17)), minute=int(r.integers(0, 60)))

    for f in feeders:
        code = f["code"]
        secs = [s for s in sections if s.feeder == code and not getattr(s, "normally_open", False)]
        trunk = [s for s in secs if any(s.to == n for n in f["trunk_nodes"])]
        spurs = [s for s in secs if s not in trunk]
        oh_m = sum(s.metres for s in secs if W.CONDUCTORS[s.code][1] == "OH")
        ug_m = sum(s.metres for s in secs) - oh_m
        sites = [c.key for c in conns if c.feeder == code]
        for y in YEARS:
            lam_hv = 0.12 + 0.11 * oh_m / 1000 + 0.03 * ug_m / 1000
            n_hv = int(r.poisson(lam_hv)) + (1 if y == 2025 else 0)
            for k in range(n_hv):
                ug = r.random() < (0.10 * ug_m) / (0.10 * ug_m + 0.42 * oh_m + 1e-9)
                pool = [s for s in secs if (W.CONDUCTORS[s.code][1] == "UG") == ug] or secs
                wts = np.array([s.metres for s in pool], float)
                sec = pool[int(r.choice(len(pool), p=wts / wts.sum()))]
                if y == 2025 and k == 0 and spurs:
                    good = [s for s in spurs if any(bykey[kk].kind == "S" and month_end(counts, kk, FY_START[2025]) >= 15
                                                    for kk in s.down)]
                    sec = good[int(r.integers(0, len(good)))]          # each feeder sees a long spur fault in the year
                t0 = t_in_year(y)
                inc = Incident("INC%d" % next(refs), f["name"], "HV", "Unplanned",
                               (["Cable fault", "Joint failure", "Third party damage"] if ug else
                                ["Overhead line - vegetation", "Overhead line - wind", "Overhead line - bird",
                                 "Insulator failure", "Lightning"])[int(r.integers(0, 3 if ug else 5))], t0, "ADMS")
                inc.forced_trunk = (y == 2025 and k == 0)
                beyond = _beyond(f, secs, sec.id)
                if sec in trunk:
                    off = sites
                    up = [k2 for k2 in sites if k2 not in beyond]
                else:
                    off = beyond
                    up = []
                for kk in off:
                    inc.steps.append((t0, kk, month_end(counts, kk, t0)))
                t1 = t0 + dt.timedelta(minutes=int(r.integers(9, 38)))
                for kk in up:
                    inc.steps.append((t1, kk, -month_end(counts, kk, t0)))
                rest = [kk for kk in off if kk not in up]
                repair = t0 + dt.timedelta(minutes=int(r.integers(190, 760)))
                forced_spur = (y == 2025 and k == 0 and sec not in trunk)
                if forced_spur:
                    repair = t0 + dt.timedelta(minutes=int(r.integers(330, 720)))
                backfed = sec in trunk and code in nop_feeders and r.random() < 0.85
                if backfed:
                    t2 = t0 + dt.timedelta(minutes=int(r.integers(48, 135)))
                    for kk in rest:
                        inc.steps.append((t2, kk, -month_end(counts, kk, t0)))
                else:
                    long_wait = repair - t0 > dt.timedelta(hours=4)
                    for kk in rest:
                        n = month_end(counts, kk, t0)
                        tg = None
                        if long_wait and n >= 3 and (forced_spur or r.random() < 0.82):
                            tg = t0 + dt.timedelta(minutes=int(r.integers(105, 230)))
                            gens.append(dict(unit=gen_units[int(r.integers(0, len(gen_units)))], site=kk, incident=inc.ref,
                                             connected=tg, disconnected=repair + dt.timedelta(minutes=int(r.integers(6, 40))),
                                             kva=[100, 200, 315, 500][int(r.integers(0, 4))], kind="fault"))
                        inc.steps.append((repair, kk, -n))
                        inc.gen = getattr(inc, "gen", {})
                        if tg is not None:
                            inc.gen[kk] = tg
                incidents.append(inc)
            # transient faults cleared by auto-reclose (short interruptions)
            if oh_m > 2000:
                for _ in range(int(r.poisson(1.5 + oh_m / 4000))):
                    t0 = t_in_year(y)
                    inc = Incident("INC%d" % next(refs), f["name"], "HV", "Unplanned", "Transient - auto-reclose", t0, "ADMS")
                    dur = dt.timedelta(seconds=int(r.integers(20, 170)))
                    for kk in sites:
                        n = month_end(counts, kk, t0)
                        inc.steps.append((t0, kk, n))
                        inc.steps.append((t0 + dur, kk, -n))
                    incidents.append(inc)
            # LV faults at substations: part of a substation's customers off until the fuse or the cable is repaired
            for kk in sites:
                c = bykey[kk]
                if c.kind != "S":
                    continue
                n_all = month_end(counts, kk, FY_START[y])
                if n_all < 15:
                    continue
                for _ in range(int(r.poisson(0.42))):
                    t0 = t_in_year(y)
                    share = float(r.uniform(0.12, 0.45))
                    n = max(2, int(round(month_end(counts, kk, t0) * share)))
                    inc = Incident("WO%d" % next(wo), f["name"], "LV", "Unplanned",
                                   ["LV cable fault", "LV fuse operation", "LV joint failure", "Service cut-out"][int(r.integers(0, 4))],
                                   t0, "WMS")
                    inc.steps.append((t0, kk, n))
                    inc.steps.append((t0 + dt.timedelta(minutes=int(r.integers(70, 330))), kk, -n))
                    incidents.append(inc)
            # pre-arranged outages (planned work). The control system records every site on the switched-out section as
            # off supply for the outage; the sites the generation team kept on supply with a mobile generator appear
            # only in the hire log.
            for j in range(1 + int(r.random() < 0.5)):
                d0 = daytime(t_in_year(y))
                inc = Incident("INC%d" % next(refs), f["name"], "HV", "Pre-arranged", "Planned maintenance", d0, "ADMS")
                cands = [kk for kk in sites if bykey[kk].kind == "S"]
                pick = list(r.choice(cands, min(len(cands), int(r.integers(1, 3))), replace=False))
                end = d0 + dt.timedelta(minutes=int(r.integers(180, 390)))
                inc.kept = set()
                for i_k, kk in enumerate(pick):
                    n = month_end(counts, kk, d0)
                    inc.steps.append((d0, kk, n))
                    inc.steps.append((end, kk, -n))
                    if r.random() < 0.4 or (y == 2025 and j == 0 and i_k == 0):
                        gens.append(dict(unit=gen_units[int(r.integers(0, len(gen_units)))], site=kk, incident=inc.ref,
                                         connected=d0 - dt.timedelta(minutes=int(r.integers(20, 50))),
                                         disconnected=end + dt.timedelta(minutes=int(r.integers(5, 30))),
                                         kva=0, kind="planned"))
                        inc.kept.add(kk)
                if inc.steps:
                    incidents.append(inc)
    # the exceptional event: the 6 to 7 January 2026 windstorm on the overhead feeders
    storm0 = dt.datetime(2026, 1, 6, 15, 10)
    for f in feeders:
        secs = [s for s in sections if s.feeder == f["code"] and not getattr(s, "normally_open", False)]
        oh = [s for s in secs if W.CONDUCTORS[s.code][1] == "OH"]
        if not oh:
            continue
        for j in range(int(r.integers(1, 3))):
            sec = oh[int(r.integers(0, len(oh)))]
            t0 = storm0 + dt.timedelta(minutes=int(r.integers(0, 26 * 60)))
            inc = Incident("INC%d" % next(refs), f["name"], "HV", "Unplanned", "Overhead line - wind", t0, "ADMS")
            inc.exceptional = True
            off = _beyond(f, secs, sec.id)
            rep = t0 + dt.timedelta(minutes=int(r.integers(300, 1300)))
            for kk in off:
                n = month_end(counts, kk, t0)
                inc.steps.append((t0, kk, n))
                inc.steps.append((rep, kk, -n))
            incidents.append(inc)
    # a transmission trip at the grid supply point interrupting the whole primary (excluded from the measures)
    tt = dt.datetime(2025, 8, 19, 6, 41)
    inc = Incident("INC%d" % next(refs), "Copsewell Cross 33kV", "EHV", "Unplanned", "Transmission system (NGET)", tt, "ADMS")
    for c in conns:
        n = month_end(counts, c.key, tt)
        inc.steps.append((tt, c.key, n))
        inc.steps.append((tt + dt.timedelta(minutes=27), c.key, -n))
    incidents.append(inc)
    # duplicates: a work-management record of an LV job at a site whose whole supply was off in an HV incident
    dups = []
    hv25 = [i for i in incidents if i.voltage == "HV" and i.category == "Unplanned" and not i.exceptional
            and i.cause != "Transient - auto-reclose" and FY_START[2025] <= i.start < FY_START[2026]]
    for inc in hv25:
        feeder_sites = {}
        for (tm, kk, ch) in inc.steps:
            if ch > 0:
                feeder_sites[kk] = (tm, ch)
        cand = [kk for kk in feeder_sites if bykey[kk].kind == "S" and feeder_sites[kk][1] >= 15]
        first_trunk = getattr(inc, "forced_trunk", False)
        if not cand or (not first_trunk and r.random() > 0.55):
            continue
        kk = cand[int(r.integers(0, len(cand)))]
        off_t = feeder_sites[kk][0]
        on_t = min(tm for (tm, k2, ch) in inc.steps if k2 == kk and ch < 0)
        if getattr(inc, "gen", {}).get(kk):
            on_t = min(on_t, inc.gen[kk])
        span = (on_t - off_t).total_seconds() / 60
        if span < 40:
            continue
        a = off_t + dt.timedelta(minutes=int(r.integers(10, max(11, int(span * 0.35)))))
        n = feeder_sites[kk][1]
        d = Incident("WO%d" % next(wo), inc.circuit, "LV", "Unplanned",
                     ["LV fuse operation", "Service cut-out", "LV cable fault"][int(r.integers(0, 3))], a, "WMS")
        d.steps.append((a, kk, n))
        d.steps.append((on_t + dt.timedelta(minutes=int(r.integers(2, 26))), kk, -n))   # the job is closed once supply is confirmed
        d.dup_of = inc.ref
        dups.append(d)
    incidents.extend(dups)
    for inc in incidents:          # a site with no customers yet (Redburn Meadows before October 2025) is not interrupted
        inc.steps = [s for s in inc.steps if s[2] != 0]
    incidents = [i for i in incidents if i.steps]
    incidents.sort(key=lambda i: (i.start, i.ref))
    return dict(counts=counts, incidents=incidents, gens=gens, gen_units=gen_units)


def measures(rel, conns, feeders, *, generators=True, dedupe=True, short_rule=True, prearranged_half=True,
             exceptional_rule=True, transmission_rule=True, denominator="march"):
    """CI per 100 customers and CML per customer for 2025/26, each feeder, under the handling flags."""
    counts, incs = rel["counts"], rel["incidents"]
    site_feeder = {c.key: c.feeder for c in conns}
    names = {f["code"]: f["name"] for f in feeders}
    ci = {f["code"]: 0.0 for f in feeders}
    cml = {f["code"]: 0.0 for f in feeders}
    lo, hi = FY_START[2025], FY_START[2026]
    for inc in incs:
        if not (lo <= inc.start < hi):
            continue
        if inc.dup_of and dedupe:
            continue
        if inc.exceptional and exceptional_rule:
            continue
        if inc.voltage == "EHV" and transmission_rule:
            continue
        w = 0.5 if (inc.category == "Pre-arranged" and prearranged_half) else 1.0
        bysite = {}
        for (tm, kk, ch) in inc.steps:
            bysite.setdefault(kk, []).append((tm, ch))
        gmap = getattr(inc, "gen", {}) if generators else {}
        kept = getattr(inc, "kept", set()) if generators else set()
        for kk, ev in bysite.items():
            if kk not in site_feeder or kk in kept:
                continue
            ev.sort()
            off_t, n = ev[0][0], ev[0][1]
            on_t = [tm for tm, ch in ev if ch < 0][0]
            if kk in gmap and gmap[kk] < on_t:
                on_t = gmap[kk]
            mins = (on_t - off_t).total_seconds() / 60.0
            if mins < 3 and short_rule:
                continue
            fcode = site_feeder[kk]
            ci[fcode] += w * n
            cml[fcode] += w * n * mins
    out = {}
    for f in feeders:
        code = f["code"]
        keys = [c.key for c in conns if c.feeder == code]
        if denominator == "march":
            den = sum(counts[k][dt.date(2026, 3, 1)] for k in keys)
        elif denominator == "april":
            den = sum(counts[k][dt.date(2025, 4, 1)] for k in keys)
        else:
            den = np.mean([sum(counts[k][m] for k in keys) for m in month_list()[24:]])
        out[code] = dict(ci=100.0 * ci[code] / den, cml=cml[code] / den, customers=den, name=names[code])
    return out


def on_supply(R, conns):
    """Each connection's share of every UTC half-hour it was on supply from the network, and each substation's share of
    load still connected through its LV faults. A site a generator supplied was still off the network: the generator
    feeds the LV board, the transformer stays dead until the network is restored."""
    import numpy as np
    out = {c.key: np.ones(S.N) for c in conns}
    t0 = S.UTC[0]

    def to_utc(t):
        return t - dt.timedelta(hours=S.uk_offset_hours(t - dt.timedelta(hours=1)))

    def mark(key, a, b, weight):
        ua, ub = to_utc(a), to_utc(b)
        i0 = int((ua - t0).total_seconds() // 1800)
        i1 = int((ub - t0).total_seconds() // 1800)
        for i in range(max(i0, 0), min(i1, S.N - 1) + 1):
            hs = t0 + dt.timedelta(minutes=30 * i)
            he = hs + dt.timedelta(minutes=30)
            ov = (min(he, ub) - max(hs, ua)).total_seconds()
            if ov > 0:
                out[key][i] = max(0.0, out[key][i] - weight * ov / 1800.0)
    for inc in R["incidents"]:
        if inc.dup_of:
            continue
        per = {}
        for (tm, kk, ch) in inc.steps:
            per.setdefault(kk, []).append((tm, ch))
        for kk, ev in per.items():
            if kk not in out:
                continue
            ev.sort()
            a, n = ev[0]
            b = [tm for tm, ch in ev if ch < 0][0]
            if inc.voltage == "LV":
                tot = month_end(R["counts"], kk, a)
                w = min(1.0, n / max(tot, 1))
            else:
                w = 1.0
            mark(kk, a, b, w)
    return out
