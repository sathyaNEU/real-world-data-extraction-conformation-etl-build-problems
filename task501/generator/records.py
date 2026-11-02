"""The records the company's systems wrote over the year, cut from the clean truth: the district meters' historian
export, the works outlet meter, the trunk mains register, the control room's valve log, the inlet turbidity monitors,
the flushing contractor's job sheets, the non-household supply points with their monthly settlements and loggers, and
three files the solution never reads (weather, regulatory tap samples, the 2024 condition assessment). Every mess item
is what the producing system writes; none is placed to be caught."""
import datetime as dt
import math

import numpy as np

import net as N
import world as W

R = lambda k: np.random.default_rng(W.SEED + k)


# ------------------------------------------------------------------------------------------------ the truth
def truth():
    dem, users, parts = N.demand(np.random.default_rng(W.SEED))
    dark = N.dark_minutes()
    for h, mn in dark.items():
        for d in ("D06", "D07", "D08", "D09", "D18"):
            frac = (60 - mn) / 60.0
            dem[d][h] *= frac
            for p in parts[d].values():
                p[h] *= frac
        for u, _, _, sup, _ in N.USERS:
            if sup in ("D06", "D07", "D08", "D09", "D18"):
                users[u][h] *= (60 - mn) / 60.0
    tl = N.timeline()
    op, sgn = N.operated_flows(dem, tl, dark)
    static = N.static_flows(dem)
    plan, psgn, pmask = N.plan_flows(dem)
    rel, level, c0 = N.shed(op, static)
    add = N.inlet_turbidity(rel, tl)
    return dict(dem=dem, users=users, parts=parts, tl=tl, op=op, sgn=sgn, static=static, plan=plan, psgn=psgn,
                pmask=pmask, rel=rel, level=level, c0=c0, add=add, dark=dark)


# ------------------------------------------------------------------------------------------------ identifiers
def _codes(rng, n, lo, hi, used=()):
    out = []
    used = set(used)
    while len(out) < n:
        x = int(rng.integers(lo, hi))
        if x not in used:
            used.add(x)
            out.append(x)
    return out


def valves():
    """The trunk register's valves: two per trunk main (upstream and downstream ends), two per interconnector (its
    end valve, normally open, and its boundary valve, normally shut)."""
    rng = R(11)
    nums = _codes(rng, 2 * len(W.MAINS), 10200, 48990)
    out = []
    i = 0
    for k, (mid, name, a, b, dn, *_rest) in W.MAINS.items():
        for end in ("A", "B"):
            if k in W.TRUNK:
                loc = W.NODES[a] if end == "A" else W.NODES[b]
                role = "Upstream end" if end == "A" else "Downstream end"
                normal = "Open"
            else:
                loc = W.NODES[a] if end == "A" else W.NODES[b]
                role = "End valve" if end == "A" else "Boundary valve"
                normal = "Open" if end == "A" else "Shut"
            vtype = "Butterfly" if dn >= 375 else "Sluice"
            turns = int(round(dn / 25.0 * 3.2 + rng.integers(-4, 5))) if vtype == "Sluice" else int(rng.integers(18, 31))
            out.append(dict(key=k, end=end, valve_no="V%05d" % nums[i], main_id=mid, location=loc, role=role,
                            dn=dn if k in W.TRUNK else dn, vtype=vtype, normal=normal, turns=turns))
            i += 1
    return out


def meter_serials():
    rng = R(12)
    nums = _codes(rng, len(W.DISTRICTS) + 2, 30100, 79900)
    ser = {d: "MF%05d" % nums[i] for i, d in enumerate(W.DISTRICTS)}
    swaps = {"D07": (dt.datetime(2026, 3, 11, 9, 0), 2, "MF%05d" % nums[-2]),
             "D15": (dt.datetime(2026, 5, 27, 8, 0), 3, "MF%05d" % nums[-1])}
    return ser, swaps


# ------------------------------------------------------------------------------------------------ district meters
PROTECT = [(dt.datetime(2026, 6, 20), dt.datetime(2026, 7, 30)), (dt.datetime(2026, 4, 10), dt.datetime(2026, 4, 17)),
           (dt.datetime(2026, 8, 15), dt.datetime(2026, 8, 26)), (dt.datetime(2025, 11, 17), dt.datetime(2025, 11, 21)),
           (dt.datetime(2026, 1, 12), dt.datetime(2026, 1, 16)), (dt.datetime(2026, 10, 5), dt.datetime(2026, 10, 9))]


def _protected(t):
    return any(a <= t < b for a, b in PROTECT)


def district_meter_rows(tr):
    """Rows (dma_ref, meter_serial, reading_utc, flow_l_s, quality): hourly means on UTC as the historian exports them,
    a meter change at two inlets, download gaps left blank, one-hour dropouts the historian filled and flagged, and
    one day's download re-sent."""
    rng = R(13)
    ser, swaps = meter_serials()
    bias = {d: 1 + 0.006 * rng.standard_normal() for d in W.DISTRICTS}
    meas = {d: np.round(tr["dem"][d] * bias[d] * (1 + 0.0035 * rng.standard_normal(N.N_HOURS)), 2) for d in W.DISTRICTS}
    quality = {d: np.array(["G"] * N.N_HOURS, dtype=object) for d in W.DISTRICTS}
    blank = {d: np.zeros(N.N_HOURS, bool) for d in W.DISTRICTS}
    # download gaps (blank) and single-hour dropouts the historian filled by interpolation (flagged S)
    dl = list(W.DISTRICTS)
    n_gap = 0
    while n_gap < 23:
        d = dl[int(rng.integers(0, len(dl)))]
        h = int(rng.integers(30, N.N_HOURS - 30))
        L = int(rng.integers(1, 6))
        if any(_protected(N.UTC[h + k]) for k in range(L)) or blank[d][h - 3:h + L + 3].any():
            continue
        blank[d][h:h + L] = True
        quality[d][h:h + L] = "M"
        n_gap += 1
    n_sub = 0
    while n_sub < 17:
        d = dl[int(rng.integers(0, len(dl)))]
        h = int(rng.integers(30, N.N_HOURS - 30))
        if _protected(N.UTC[h]) or blank[d][h - 2:h + 3].any() or quality[d][h] != "G":
            continue
        meas[d][h] = round((meas[d][h - 1] + meas[d][h + 1]) / 2.0, 2)
        quality[d][h] = "S"
        n_sub += 1
    serial = {d: np.array([ser[d]] * N.N_HOURS, dtype=object) for d in W.DISTRICTS}
    for d, (t, L, new) in swaps.items():
        h = N.hour_index(t)
        blank[d][h:h + L] = True
        quality[d][h:h + L] = "M"
        serial[d][h:] = new
    rows = []
    for h in range(N.N_HOURS):
        ts = N.UTC[h].strftime("%Y-%m-%d %H:%M")
        for d in W.DISTRICTS:
            v = "" if blank[d][h] else "%.2f" % meas[d][h]
            rows.append((W.DCODE[d], serial[d][h], ts, v, quality[d][h]))
    # the download for Tannery Yard on 9 February 2026 was sent twice; the second copy sits at the end of the export
    h0 = N.hour_index(dt.datetime(2026, 2, 9))
    dup = [r for r in rows[h0 * len(W.DISTRICTS):(h0 + 24) * len(W.DISTRICTS)] if r[0] == W.DCODE["D12"]]
    rows.extend(dup)
    return rows, dict(meas=meas, blank=blank, quality=quality, bias=bias, serial=serial, swaps=swaps, dup=dup)


def outlet_rows(tr):
    rng = R(14)
    tot = sum(tr["dem"][d] for d in W.DISTRICTS)
    loss = np.zeros(N.N_HOURS)
    a, b, q = W.BURST_LOSS
    t = W.to_utc(a)
    while t < W.to_utc(b):
        loss[N.hour_index(t.replace(minute=0))] += q / 60.0
        t += dt.timedelta(minutes=1)
    out = (tot + 1.6 + loss) * 1.004 * (1 + 0.0025 * rng.standard_normal(N.N_HOURS))
    return [(N.UTC[h].strftime("%Y-%m-%d %H:%M"), "%.1f" % out[h]) for h in range(N.N_HOURS)], out


# ------------------------------------------------------------------------------------------------ valve log
OPERATORS = ["JH", "PM", "SR", "DT", "AB", "KC", "MW", "RL"]
EVENT_REMARKS = {
    "nov_t06": ["Back feed Brook End from Coldharbour for TM105 valve chamber", "Isolate TM105 at Brook End",
                "Isolate TM105 at Eastgate Bar", "TM105 recharged Eastgate Bar end", "TM105 open Brook End",
                "IC02 shut, Brook End normal"],
    "jan_t10": ["Open IC03 to hold Sallowby on Highfield", "TM115 shut Mill Bridge, joint leak Sallowby Rd",
                "TM115 shut Sallowby Gate", "Repair complete, TM115 open Sallowby Gate", "TM115 open Mill Bridge",
                "IC03 shut, Sallowby back on Sallowby Rd"],
    "phase1": ["Relining ph1 - Brook End fed via IC02 for duration", "TM105 isolated Eastgate Bar for relining",
               "TM105 isolated Brook End", "TM105 returned to service after relining, samples clear",
               "TM105 open Brook End", "IC02 shut, relining ph1 complete"],
    "june_t04": ["Open IC03 - Mill Bridge & Sallowby to be fed from Highfield", "TM108 shut Ferrars Corner, valve replacement",
                 "TM108 shut Mill Bridge", "New valve in, TM108 recharged Mill Bridge", "TM108 open Ferrars Corner",
                 "IC03 shut, network normal"],
    "july_t04": ["BURST Mill Rd o/s 41 - TM108 shut Ferrars Corner", "TM108 shut Mill Bridge",
                 "IC08 opened, Mill Bridge supplied from Brook End", "Burst repaired, TM108 recharged Mill Bridge end",
                 "TM108 open Ferrars Corner", "IC08 shut"],
    "oct_t13": ["IC02 open, Coldharbour to be fed from Brook End", "TM112 shut Eastgate Bar, valve replacement",
                "TM112 shut Coldharbour", "TM112 open Eastgate Bar", "TM112 open Coldharbour", "IC02 shut, normal"],
}
DIST_REMARKS = ["Mains repair", "Service pipe leak", "Mains repair - burst", "Hydrant replacement", "New connection",
                "Shut for meter install", "Leak on ferrule", "Mains repair, 4in CI", "Burst 6in CI", "Valve reseated",
                "Flushing", "Air valve repair", "Boundary valve check", "Repair complete", "Supply restored", "Reopen",
                "Customer side leak isolated", "Joint leak", "PRV maintenance", "Washout", ""]


def valve_log_rows(vlist):
    rng = R(15)
    vno = {(v["key"], v["end"]): v["valve_no"] for v in vlist}
    turns = {(v["key"], v["end"]): v["turns"] for v in vlist}
    rows = []
    for ev in W.EVENTS:
        for (ts, m, end, op), rem in zip(ev["seq"], EVENT_REMARKS[ev["key"]]):
            t = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M")
            rows.append(dict(t=t, valve=vno[(m, end)], action=op, turns=turns[(m, end)], job=ev["job"],
                             op=OPERATORS[int(rng.integers(0, len(OPERATORS)))], rem=rem))
    # the exercising programme: every trunk valve worked through at night, twice in the year; boundary valves are
    # cracked a few turns and reshut
    for v in vlist:
        for k in range(2):
            day = W.T0.date() + dt.timedelta(days=int(rng.integers(5, 360)))
            t = dt.datetime.combine(day, dt.time(int(rng.integers(21, 24)), int(rng.integers(0, 60))))
            if v["normal"] == "Shut":
                rem, tn = "Exercised - cracked %d turns and reshut" % int(rng.integers(3, 7)), int(rng.integers(3, 7))
            else:
                tn = v["turns"]
                rem = ["Exercised full cycle, left open", "Exercised, stiff first 10 turns", "Exercised OK",
                       "Exercised full cycle"][int(rng.integers(0, 4))]
            rows.append(dict(t=t, valve=v["valve_no"], action="EXERCISE", turns=tn, job="VX/%02d/%04d" % (
                t.year % 100, int(rng.integers(100, 990))), op=OPERATORS[int(rng.integers(0, len(OPERATORS)))], rem=rem))
    # distribution valves in the districts: shut and reopened for repairs and connections
    used = {int(v["valve_no"][1:]) for v in vlist}
    dvalves = ["V%05d" % x for x in _codes(rng, 520, 10100, 49990, used)]
    n = 0
    while n < 690:
        day = W.T0.date() + dt.timedelta(days=int(rng.integers(0, 365)))
        t = dt.datetime.combine(day, dt.time(int(rng.integers(6, 23)), int(rng.integers(0, 60))))
        dur = dt.timedelta(minutes=int(rng.integers(35, 520)))
        nv = 1 + int(rng.random() < 0.45) + int(rng.random() < 0.15)
        vs = [dvalves[int(rng.integers(0, len(dvalves)))] for _ in range(nv)]
        job = "RW/%02d/%04d" % (t.year % 100, int(rng.integers(1000, 9800)))
        op = OPERATORS[int(rng.integers(0, len(OPERATORS)))]
        rem = DIST_REMARKS[int(rng.integers(0, len(DIST_REMARKS)))]
        for i, vv in enumerate(vs):
            rows.append(dict(t=t + dt.timedelta(minutes=3 * i), valve=vv, action="CLOSE", turns=int(rng.integers(12, 34)),
                             job=job, op=op, rem=rem if i == 0 else ""))
        rem2 = ["Reopen", "Supply restored", "Repair complete", "", "Reopened, flushed hydrant"][int(rng.integers(0, 5))]
        for i, vv in enumerate(vs):
            rows.append(dict(t=t + dur + dt.timedelta(minutes=2 * i), valve=vv, action="OPEN",
                             turns=int(rng.integers(12, 34)), job=job, op=op, rem=rem2 if i == 0 else ""))
        n += 1
    rows = [r for r in rows if W.T0 <= W.to_utc(r["t"]) < W.T1 and not _dst_gap(r["t"])]
    rows.sort(key=lambda r: (r["t"], r["valve"]))
    ref = 26104
    out = []
    for r in rows:
        ref += int(rng.integers(1, 7))
        out.append(("CR%06d" % ref, r["t"].strftime("%d/%m/%Y"), r["t"].strftime("%H:%M"), r["valve"], r["action"],
                    str(r["turns"]), r["job"], r["op"], r["rem"]))
    return out


def _dst_gap(t_local):
    """The control room logs nothing inside a clock change's missing or repeated hour."""
    return t_local.date() in (dt.date(2026, 3, 29), dt.date(2026, 10, 25)) and t_local.hour <= 2


# ------------------------------------------------------------------------------------------------ turbidity
def turbidity_rows(tr):
    """Fifteen-minute turbidity at the monitored district inlets on UTC: each instrument with its own baseline,
    fouling drift between cleaning visits, noise, air-bubble spikes, cleaning windows and communication losses."""
    rng = R(16)
    ids = _codes(rng, len(W.TURB_SITES), 1100, 8900)
    out = []
    n15 = N.N_HOURS * 4
    for si, d in enumerate(W.TURB_SITES):
        r = np.random.default_rng(W.SEED + 300 + si)
        base = 0.055 + 0.07 * r.random()
        add_h = tr["add"][d]
        # spread each hour's release over its quarter hours, smoothed with the next hour's
        add = np.repeat(add_h, 4)
        add = np.convolve(add, np.array([0.15, 0.25, 0.3, 0.2, 0.1]), mode="same")
        # fouling drift reset at cleaning visits every five to seven weeks
        drift = np.zeros(n15)
        visits = []
        t = int(r.integers(4 * 24 * 7, 4 * 24 * 30))
        while t < n15:
            visits.append(t)
            t += int(r.integers(4 * 24 * 35, 4 * 24 * 49))
        last = 0
        rate = (0.0015 + 0.002 * r.random()) / 96.0
        for i in range(n15):
            if visits and i in visits:
                last = i
            drift[i] = rate * (i - last)
        noise = np.exp(0.10 * r.standard_normal(n15))
        val = (base + drift) * noise + add * (1 + 0.06 * r.standard_normal(n15))
        status = np.array(["OK"] * n15, dtype=object)
        blank = np.zeros(n15, bool)
        for v in visits:
            L = int(r.integers(2, 5))
            status[v:v + L] = "MAINT"
            val[v:v + L] = val[v:v + L] + r.uniform(0.3, 1.8, size=len(val[v:v + L]))
        # air bubbles: single readings well above the line
        for _ in range(int(r.integers(9, 16))):
            i = int(r.integers(0, n15))
            val[i] += r.uniform(0.4, 2.2)
        # communication losses: hours with nothing recorded
        for _ in range(int(r.integers(3, 7))):
            i = int(r.integers(0, n15 - 40))
            L = int(r.integers(4, 36))
            if _turb_protected(i, L):
                continue
            blank[i:i + L] = True
            status[i:i + L] = "COMMS"
        site = "TM-%04d" % ids[si]
        for i in range(n15):
            ts = (W.T0 + dt.timedelta(minutes=15 * i)).strftime("%Y-%m-%d %H:%M")
            out.append((site, W.DCODE[d], ts, "" if blank[i] else "%.3f" % val[i], status[i]))
    return out


def _turb_protected(i, L):
    t0 = W.T0 + dt.timedelta(minutes=15 * i)
    t1 = t0 + dt.timedelta(minutes=15 * L)
    keep = [(dt.datetime(2026, 6, 20), dt.datetime(2026, 7, 28)), (dt.datetime(2026, 4, 11), dt.datetime(2026, 4, 16)),
            (dt.datetime(2025, 11, 17), dt.datetime(2025, 11, 21)), (dt.datetime(2026, 1, 12), dt.datetime(2026, 1, 16))]
    return any(t0 < b and t1 > a for a, b in keep)


# ------------------------------------------------------------------------------------------------ ask A: job sheets
STREETS = {
    "D01": ["Copt Hill Road", "Quarry Lane", "Larch Close"], "D02": ["Market Hill", "Sheep Street", "Bridewell Row"],
    "D03": ["Church Lane", "Vicarage Walk", "Tanners Croft"], "D04": ["Ferrars Lane", "Kiln Road", "Orchard Rise"],
    "D05": ["St Anne's Road", "Cooper's Yard", "Prospect Place"], "D06": ["Mill Road", "Wharf Street", "Lock Lane"],
    "D07": ["Weir Lane", "Osier Close", "Ford Street"], "D08": ["Sallowby Road", "Chapel Fold", "Holme Way"],
    "D09": ["Sallowby Park Avenue", "Cedar Drive", "Rowan Way"], "D18": ["Hollow Lane", "Badger Bank", "Pound Lane"],
    "D10": ["Eastgate", "Ropewalk", "Malthouse Lane"], "D11": ["Brook Street", "Water Lane", "Dyers Row"],
    "D12": ["Tannery Yard", "Bark Street", "Hide Lane"], "D13": ["Coldharbour Road", "Gorse Lane", "Furze Hill"],
    "D14": ["North Road", "Lodge Lane", "Spinney Close"], "D15": ["Northfield Road", "Glebe Way", "Hayfield Close"],
    "D16": ["Highfield Road", "Windmill Hill", "Beacon Rise"], "D17": ["Pinfold Lane", "Stocks Hill", "Well Lane"],
}
LEN = {75: (330, 640), 100: (290, 600), 150: (260, 560), 225: (300, 660), 300: (340, 760)}
GAUGE = {75: (4.6, 7.2), 100: (6.8, 10.5), 150: (10.5, 15.5), 225: (14.0, 19.5)}
GAUGE_TWIN = {225: (12.0, 17.0), 300: (15.5, 22.0)}
SHEET_REMARKS = ["Clear", "Clear after 15 min", "Heavy discolouration first 10 min", "Hydrant slow to open", "",
                 "Ran brown then clear", "Clear", "", "Light discolouration", "Clear after 25 min", "Traffic mgmt in place",
                 "Pressure dip reported by resident, recovered", "", "Clear", "Some sediment at start"]


def job_sheet_rows():
    """One row per hydrant used on a section. Crew C14 flushes the smaller mains with one standpipe; from December it
    zeroes the standpipe meter at the start of a night and writes the display after each section. Crew C22 flushes
    the larger mains, zeroing its meters after every section, and flushes the 300 mm mains (and some 225 mm) with a
    standpipe on each of two hydrants run together."""
    rng = R(21)
    nights = []
    d = W.PROGRAMME[0]
    while d <= W.PROGRAMME[1]:
        if not (dt.date(2025, 12, 19) <= d <= dt.date(2026, 1, 4)) and d.weekday() <= 3:
            if rng.random() < 0.62:
                nights.append((d, W.CREW_DIST))
            if rng.random() < 0.34:
                nights.append((d, W.CREW_TRUNK))
        d += dt.timedelta(days=1)
    secrefs = iter(["FS%04d" % x for x in _codes(rng, 900, 1030, 9970)])
    hyds = iter(["H%05d" % x for x in _codes(rng, 1500, 20100, 69900)])
    sheet = 4180
    out = []
    truth = []
    for night, crew in nights:
        dma = list(W.DISTRICTS)[int(rng.integers(0, 18))]
        street = STREETS[dma][int(rng.integers(0, 3))]
        if crew == W.CREW_DIST:
            dn = int(rng.choice([75, 100, 150], p=[0.3, 0.4, 0.3]))
            nsec = int(rng.integers(2, 6))
        else:
            dn = int(rng.choice([100, 150, 225, 300], p=[0.12, 0.26, 0.36, 0.26]))
            nsec = int(rng.integers(1, 4))
        for attempt in range(50):
            secs = []
            for j in range(nsec):
                dnj = dn if rng.random() < 0.8 else (int(rng.choice([75, 100, 150])) if crew == W.CREW_DIST
                                                     else int(rng.choice([100, 150, 225, 300])))
                L = float(int(rng.integers(*LEN[dnj])))
                vp = math.pi * (dnj / 2000.0) ** 2 * L
                k = float(rng.uniform(2.7, 4.2))
                twin = crew == W.CREW_TRUNK and (dnj == 300 or (dnj == 225 and rng.random() < 0.5))
                if twin:
                    g = [float(rng.uniform(*GAUGE_TWIN[dnj])) for _ in range(2)]
                else:
                    g = [float(rng.uniform(*GAUGE[dnj]))]
                r = [float(rng.uniform(0.08, 0.14)) for _ in g]
                vt = k * vp
                Tmin = vt / (sum(gi * (1 - ri) for gi, ri in zip(g, r)) * 0.06)
                secs.append(dict(dn=dnj, L=L, k=k, g=g, r=r, T=Tmin, twin=twin, v=[gi * (1 - ri) * Tmin * 0.06
                                                                                    for gi, ri in zip(g, r)]))
            ok = all(s_["T"] >= 14 for s_ in secs)
            if crew == W.CREW_DIST and night >= W.RUNNING_FROM:
                cum = 0.0
                for j, s_ in enumerate(secs):
                    if j and cum < 0.62 * s_["v"][0]:
                        ok = False
                    cum += s_["v"][0]
            if ok:
                break
        t = dt.datetime.combine(night, dt.time(int(rng.integers(21, 23)), int(rng.integers(0, 60))))
        sheet += int(rng.integers(1, 4))
        disp = 0.0
        for j, s_ in enumerate(secs):
            sref = next(secrefs)
            start = t.replace(second=0)
            fin = start + dt.timedelta(minutes=s_["T"])
            fin_rec = (fin + dt.timedelta(seconds=30)).replace(second=0, microsecond=0)
            st_rec = start
            rem = SHEET_REMARKS[int(rng.integers(0, len(SHEET_REMARKS)))]
            ntu = "%.2f" % float(rng.uniform(0.18, 0.95))
            hy = [next(hyds) for _ in s_["g"]]
            for i, (gi, vi) in enumerate(zip(s_["g"], s_["v"])):
                if crew == W.CREW_DIST and night >= W.RUNNING_FROM:
                    disp += vi
                    booked = disp
                else:
                    booked = vi
                out.append(dict(sheet="FL%d-%05d" % (night.year % 100, sheet), night=night, crew=crew,
                                dma=W.DCODE[dma], street=street, section=sref, dn=s_["dn"], material=(
                                    "CI" if rng.random() < 0.86 else "SI"), length=int(s_["L"]), hydrant=hy[i],
                                start=st_rec, finish=fin_rec, gauge=round(gi, 1), booked=round(booked, 1),
                                ntu=ntu, rem=rem if i == 0 else ""))
            truth.append(dict(section=sref, night=night, crew=crew, dn=s_["dn"], L=s_["L"], v=sum(s_["v"]),
                              twin=s_["twin"], running=crew == W.CREW_DIST and night >= W.RUNNING_FROM, pos=j))
            t = fin + dt.timedelta(minutes=float(rng.uniform(22, 55)))
    _clear_edges(out)
    rows = []
    for r_ in out:
        nd = r_["night"].strftime("%d/%m/%Y") if r_["night"] < dt.date(2026, 1, 1) else r_["night"].isoformat()
        rows.append((r_["sheet"], nd, r_["crew"], r_["dma"], r_["street"], r_["section"], str(r_["dn"]),
                     r_["material"], str(r_["length"]), r_["hydrant"], r_["start"].strftime("%H:%M"),
                     r_["finish"].strftime("%H:%M"), "%.1f" % r_["gauge"], "%.1f" % r_["booked"], r_["ntu"], r_["rem"]))
    # two nights' sheets were sent twice; the copies sit at the end of the export
    resend = []
    for night_pick in (dt.date(2025, 10, 14), dt.date(2026, 2, 10)):
        cand = sorted({r_["night"] for r_ in out if r_["night"] >= night_pick})[0]
        resend.extend(row for row, r_ in zip(rows, out) if r_["night"] == cand and r_["crew"] == (
            W.CREW_DIST if night_pick.month == 10 else W.CREW_TRUNK))
    rows.extend(resend)
    return rows, truth


def _cells(out):
    """Water per 100 m by diameter and year as the sheets will read: a night whose later readings run past their
    flush's gauge flow times minutes is differenced, the hydrants of one section on one night are one flush."""
    by = {}
    for r_ in out:
        by.setdefault((r_["night"], r_["crew"]), []).append(r_)
    w = {}
    for g in by.values():
        cap = lambda r_: r_["gauge"] * ((r_["finish"] - r_["start"]).total_seconds() / 60.0 % 1440) * 0.06
        runs = any(r_["booked"] > 1.2 * cap(r_) for r_ in g[1:])
        prev = 0.0
        for r_ in g:
            w[id(r_)] = r_["booked"] - prev if runs else r_["booked"]
            prev = r_["booked"]
    sec = {}
    for r_ in out:
        k = (r_["night"], r_["section"])
        a, L, dn, yr = sec.get(k, (0.0, r_["length"], r_["dn"], r_["night"].year))
        sec[k] = (a + w[id(r_)], L, dn, yr)
    cell = {}
    for a, L, dn, yr in sec.values():
        x = cell.setdefault((dn, yr), [0.0, 0.0])
        x[0] += a
        x[1] += L
    return {k: v[0] / v[1] * 100 for k, v in cell.items()}


def _clear_edges(out):
    """Keep every diameter-year figure off its one-decimal rounding edge: a section's recorded length is stepped by
    whole metres until the figure clears the edge by 0.006."""
    def edge(x):
        return abs(((x * 10) % 1.0) - 0.5) / 10.0
    for _ in range(60):
        cells = _cells(out)
        bad = [k for k, v in cells.items() if edge(v) < 0.006]
        if not bad:
            return
        dn, yr = bad[0]
        secs = sorted({r_["section"] for r_ in out if r_["dn"] == dn and r_["night"].year == yr})
        pick = secs[len(secs) // 2]
        for r_ in out:
            if r_["section"] == pick:
                r_["length"] += 3
    raise AssertionError("diameter-year figures stay on a rounding edge")


# ------------------------------------------------------------------------------------------------ ask B: customers
SURNAMES = ["Hartley", "Pennick", "Oldroyd", "Spencer", "Garside", "Whitaker", "Lumb", "Barraclough", "Ingham",
            "Crowther", "Haigh", "Sugden", "Mallinson", "Pickles", "Firth", "Dyson", "Holroyd", "Sutcliffe", "Brook",
            "Ackroyd", "Kershaw", "Thewlis", "Ramsden", "Bottomley", "Greenwood", "Midgley", "Shackleton", "Wade"]
TRADES = ["{s} & Sons Ltd", "{s} Motors", "The {n} Inn", "{t} Dental Practice", "{s} Hair Studio", "{t} Pharmacy",
          "{s} Builders Merchants", "{t} Medical Centre", "{s}'s Butchers", "{t} Post Office", "{s} Accountants LLP",
          "{t} Methodist Church", "{s} Vets", "{t} Fish Bar", "{s} Joinery", "{t} Day Nursery", "{s} Car Wash",
          "{t} Social Club", "{s} Engineering Ltd", "{t} Tyres", "{s} Funeral Directors", "{t} Hotel",
          "{s} Print Works", "{t} Community Centre", "Co-op Food {t}", "{t} Library", "{s} Florist", "{t} Garage"]
INNS = ["Black Bull", "Fleece", "Woolpack", "Rose and Crown", "Old Bridge", "Weavers Arms", "Shoulder of Mutton",
        "Golden Lion", "Navigation", "Railway"]


def _pc(rng, sector):
    return "LV%d %d%s" % (sector[0], sector[1], "".join(chr(65 + int(rng.integers(0, 26))) for _ in range(2)).replace(
        "C", "D").replace("I", "J").replace("K", "L").replace("M", "N").replace("O", "P").replace("V", "W"))


SECTORS = {"D01": (3, 1), "D02": (3, 2), "D03": (3, 2), "D04": (4, 1), "D05": (4, 2), "D06": (5, 1), "D07": (5, 2),
           "D08": (6, 1), "D09": (6, 2), "D18": (6, 3), "D10": (2, 1), "D11": (2, 2), "D12": (2, 2), "D13": (2, 3),
           "D14": (7, 1), "D15": (7, 2), "D16": (8, 1), "D17": (8, 2)}


def months(a, b):
    y, m = int(a[:4]), int(a[5:])
    out = []
    while "%04d-%02d" % (y, m) <= b:
        out.append("%04d-%02d" % (y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def customers(tr):
    """Supply points, their monthly settled consumption (April 2025 to October 2026) and the large users' hourly
    loggers on the local clock."""
    rng = R(31)
    spids = iter(_codes(rng, 900, 10000000, 99999999))
    meters = iter(_codes(rng, 900, 100000, 999999))
    loggers = iter(_codes(rng, 40, 2100, 8800))
    sp = []
    mon_all = months("2025-04", "2026-10")
    local_month = np.array([t.strftime("%Y-%m") for t in N.LOCAL])
    in_sim = [m for m in mon_all if m >= "2025-11"]
    # large users
    amr = []
    for key, name, bill, sup, kind in N.USERS:
        q = tr["users"][key]                                  # l/s on the UTC hour
        vol = q * 3.6                                         # m3 in the hour
        lid = "AMR%04d" % next(loggers)
        spid = "30%08dW%02d" % (next(spids), int(rng.integers(10, 99)))
        street = STREETS[bill][int(rng.integers(0, 3))]
        mon = {}
        for m in in_sim:
            mon[m] = float(vol[local_month == m].sum())
        for m in mon_all:
            if m < "2025-11":
                twin = "2026-%s" % m[5:]
                mon[m] = mon[twin] * float(rng.uniform(0.9, 1.04))
        sp.append(dict(spid=spid, name=name, premises="%d %s, %s" % (int(rng.integers(2, 180)), street, W.TOWN),
                       postcode=_pc(rng, SECTORS[bill]), dma=W.DCODE[bill], meter="WM%06d" % next(meters),
                       cycle="Monthly (AMR)", logger=lid, start="2009-06-01" if key != "U10" else "2016-03-14",
                       end="", key=key, sup=sup, bill=bill, mon=mon, basis={m: "L" for m in mon_all}))
        amr.append((lid, vol))
    # small accounts: each district's small non-household draw shared between its supply points
    for d in W.DISTRICTS:
        tot_l_s = W.NH_SMALL[d]
        n = int(round(tot_l_s / 0.031)) + int(rng.integers(-3, 4))
        w = rng.lognormal(0, 0.95, size=n)
        w = w / w.sum()
        nhm = tr["parts"][d]["nh"] * 3.6
        dm = {m: float(nhm[local_month == m].sum()) for m in in_sim}
        for m in mon_all:
            if m < "2025-11":
                dm[m] = dm["2026-%s" % m[5:]] * float(rng.uniform(0.93, 1.03))
        for i in range(n):
            s_ = SURNAMES[int(rng.integers(0, len(SURNAMES)))]
            tmpl = TRADES[int(rng.integers(0, len(TRADES)))]
            name = tmpl.format(s=s_, n=INNS[int(rng.integers(0, len(INNS)))], t=W.DISTRICTS[d][1])
            street = STREETS[d][int(rng.integers(0, 3))]
            start, end = "", ""
            u = rng.random()
            if u < 0.05:
                start = (dt.date(2025, 12, 1) + dt.timedelta(days=int(rng.integers(0, 240)))).isoformat()
            elif u < 0.09:
                end = (dt.date(2025, 5, 1) + dt.timedelta(days=int(rng.integers(0, 180)))).isoformat()
            if not start:
                start = (dt.date(1990, 1, 1) + dt.timedelta(days=int(rng.integers(0, 12000)))).isoformat()
            cyc = "Quarterly" if rng.random() < 0.35 else "Half-yearly"
            mon, basis = {}, {}
            read_m = int(rng.integers(0, 6))
            for k, m in enumerate(mon_all):
                if m < start[:7] or (end and m > end[:7]):
                    continue
                v = w[i] * dm[m] * float(rng.uniform(0.88, 1.12))
                if m == start[:7] or (end and m == end[:7]):
                    v *= float(rng.uniform(0.2, 0.8))
                mon[m] = v
                step = 3 if cyc == "Quarterly" else 6
                basis[m] = "A" if (k - read_m) % step == 0 else "E"
            sp.append(dict(spid="30%08dW%02d" % (next(spids), int(rng.integers(10, 99))), name=name,
                           premises="%d %s, %s" % (int(rng.integers(1, 220)), street, W.TOWN),
                           postcode=_pc(rng, SECTORS[d]), dma=W.DCODE[d], meter="WM%06d" % next(meters), cycle=cyc,
                           logger="", start=start, end=end, key="", sup=d, bill=d, mon=mon, basis=basis))
    order = rng.permutation(len(sp))
    sp = [sp[i] for i in order]
    for s_ in sp:
        s_["mon_m3"] = {m: int(round(v)) for m, v in s_["mon"].items()}
    _clear_b_edges(sp, amr)
    return sp, amr


def _clear_b_edges(sp, amr):
    """Keep each re-routed district's non-household figure inside its one-decimal bin with room below for the autumn
    clock change's repeated hour, should a reader drop it from the loggers: one small supply point's June 2026 settlement
    in the district is stepped by whole cubic metres."""
    win = [m for m in months("2025-11", "2026-10")]
    rep = {}
    t_rep = dt.datetime(2026, 10, 25, 1, 0)                 # UTC hour that reads 01:00 a second time
    h = N.hour_index(t_rep)
    for lid, vol in amr:
        rep[lid] = float(vol[h]) / 1000.0
    for d in W.REROUTED:
        mine = [s_ for s_ in sp if s_["sup"] == d]
        x = sum(sum(s_["mon_m3"].get(m, 0) for m in win) for s_ in mine) / 1000.0
        delta = sum(rep[s_["logger"]] for s_ in mine if s_["logger"])
        r = np.floor(x * 10 + 0.5) / 10.0
        lo, hi = r - 0.05 + delta + 0.006, r + 0.044
        if lo <= x <= hi:
            continue
        target = (lo + hi) / 2.0
        step = int(round((target - x) * 1000))
        small = sorted((s_ for s_ in mine if not s_["logger"] and "2026-06" in s_["mon_m3"]),
                       key=lambda s_: -s_["mon_m3"]["2026-06"])
        small[0]["mon_m3"]["2026-06"] += step
        assert small[0]["mon_m3"]["2026-06"] > 0


def amr_rows(amr):
    """Hourly volume per logger on the local wall clock (the hour beginning): the spring change has no 01:00 and the
    autumn change two."""
    out = []
    for lid, vol in amr:
        for h in range(N.N_HOURS):
            out.append((lid, N.LOCAL[h].strftime("%d/%m/%Y %H:%M"), "%.3f" % vol[h]))
    return out


# ------------------------------------------------------------------------------------------------ distractors
def weather_rows():
    rng = R(41)
    out = []
    d = W.T0.date()
    amp_day = {}
    for d0, d1, amp, pk in W.HEAT:
        half = max((pk - d0).days, (d1 - pk).days) + 1
        x = d0
        while x <= d1:
            amp_day[x] = amp * (1 - abs((x - pk).days) / half) ** 0.35
            x += dt.timedelta(days=1)
    while d < W.T1.date():
        doy = d.timetuple().tm_yday
        base = 12.6 + 8.4 * math.cos(2 * math.pi * (doy - 200) / 365.0)
        tmax = base + 2.3 * rng.standard_normal() + 26 * amp_day.get(d, 0.0)
        tmin = tmax - 7.5 - 2.0 * rng.random() - (2.5 if amp_day.get(d, 0) > 0 else 0)
        rain = 0.0 if rng.random() < (0.55 if amp_day.get(d, 0) == 0 else 0.97) else float(rng.gamma(0.9, 4.2))
        sun = max(0.0, min(15.5, 4.2 + 3.6 * math.cos(2 * math.pi * (doy - 172) / 365.0) + 2.4 * rng.standard_normal()
                           + 30 * amp_day.get(d, 0.0)))
        out.append((d.isoformat(), "%.1f" % tmax, "%.1f" % tmin, "%.1f" % rain, "%.1f" % sun))
        d += dt.timedelta(days=1)
    return out


ZONES = {"Stavenham Central": ["D01", "D02", "D03", "D10"], "Stavenham South": ["D04", "D05", "D06", "D07"],
         "Sallowby": ["D08", "D09", "D18"], "Stavenham East": ["D11", "D12", "D13"],
         "Stavenham North": ["D14", "D15", "D16", "D17"]}


def sample_rows(tr):
    """Regulatory samples at random customer taps, by water supply zone (each zone several districts)."""
    rng = R(42)
    out = []
    ref = 50400
    for zone, ds in ZONES.items():
        n = int(rng.integers(52, 70))
        for _ in range(n):
            day = W.T0.date() + dt.timedelta(days=int(rng.integers(0, 365)))
            if day.weekday() >= 5:
                day -= dt.timedelta(days=2)
            d = ds[int(rng.integers(0, len(ds)))]
            hour = int(rng.integers(9, 15))
            h = N.hour_index(W.to_utc(dt.datetime.combine(day, dt.time(hour, 0))))
            ev = float(tr["add"][d][max(0, h - 6):h + 1].max()) if 0 <= h < N.N_HOURS else 0.0
            fe = float(rng.lognormal(math.log(24), 0.45)) + 95 * ev
            mn = float(rng.lognormal(math.log(2.6), 0.5)) + 9 * ev
            tu = float(rng.lognormal(math.log(0.14), 0.35)) + 0.8 * ev
            col = float(rng.lognormal(math.log(1.6), 0.4)) + 4 * ev
            ref += int(rng.integers(3, 40))
            sec = SECTORS[d]
            out.append(("RS%06d" % ref, day.isoformat(), zone, "LV%d %d" % sec, "%.0f" % fe, "%.1f" % mn, "%.2f" % tu,
                        "%.1f" % col))
    out.sort(key=lambda r: (r[1], r[0]))
    return out


def condition_table():
    """The 2024 condition assessment's findings per trunk main (structure only)."""
    rng = R(43)
    rows = []
    grades = dict(T01=1, T02=1, T03=4, T04=3, T10=3, T05=3, T06=4, T13=2, T08=3, T09=2, X05=2, X02=2, X04=2, X07=3)
    action = dict(T03="Reline 2027 (programme phase 2)", T06="Reline 2026 (programme phase 1)",
                  T04="Reline, programme phase 3 (2029)", T05="Monitor; reassess 2028", T08="Monitor; reassess 2028",
                  T10="Joint survey 2026", T01="None", T02="None", T13="None", T09="None", X05="Exercise valves",
                  X02="None", X04="Exercise valves", X07="Monitor")
    for k, v in W.MAINS.items():
        g = grades[k]
        wall = {1: (96, 100), 2: (85, 94), 3: (72, 84), 4: (58, 70)}[g]
        life = {1: (62, 81), 2: (41, 60), 3: (16, 36), 4: (3, 9)}[g]
        rows.append((v[0], v[1], str(v[4]), v[5], str(v[7]), str(g), "%d" % int(rng.integers(*wall)),
                     ["Sound", "Minor leakage at joints", "Some joints weeping", "Sound"][int(rng.integers(0, 4))]
                     if g >= 3 else "Sound", str(int(rng.integers(*life))), action[k]))
    return rows
