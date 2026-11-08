"""The world before any mess or document: thirty hubs, their legacy RC50 and Korrant HX150 units, every power-down,
hang, fault, visit, supply interruption and comms drop from 1 January 2023 to 31 October 2026, the 2027 regime, and
the January to October 2026 charges. Times are integer seconds from 2023-01-01 00:00 UTC."""
import datetime as dt
import math
from zoneinfo import ZoneInfo

import numpy as np

SEED = 156
UTC = dt.timezone.utc
IE = ZoneInfo("Europe/Dublin")
T0 = dt.datetime(2023, 1, 1, tzinfo=UTC)
DAY = 86400


def ts(dtm):
    return int((dtm - T0).total_seconds())


HIST_END = ts(dt.datetime(2026, 11, 1, tzinfo=UTC))      # 31 October 2026 24:00, Irish time and UTC alike
MIGRATION = ts(dt.datetime(2025, 6, 10, 2, 30, tzinfo=UTC))
CONTRACT_B = ts(dt.datetime(2024, 4, 1, tzinfo=UTC))
Y27_START = ts(dt.datetime(2027, 1, 1, tzinfo=UTC))
Y27_END = ts(dt.datetime(2028, 1, 1, tzinfo=UTC))
S26_START = ts(dt.datetime(2026, 1, 1, tzinfo=UTC))

# the HX150 controller hang: none before 75 days without a power-up, rising to 0.12 a day at 90 days
H0, H1, HMAX = 75.0, 90.0, 0.12
HB = 300            # heartbeat interval, seconds; the back office writes Offline after three missed heartbeats
EXCL_TAIL = 1800    # Schedule 4: the half hour after a visit window or a supply interruption is excluded too
CARD_TARIFF, PREAUTH = 0.59, 40.0
CAP_WH = int(PREAUTH / CARD_TARIFF * 1000)


def utc(t):
    return T0 + dt.timedelta(seconds=int(t))


def local(t):
    return utc(t).astimezone(IE)


def from_local(y, m, d, hh=0, mm=0):
    return ts(dt.datetime(y, m, d, hh, mm, tzinfo=IE).astimezone(UTC))


def hang_tau(E):
    """Days after a power-up at which the hang comes, for a unit exponential draw E (inverse cumulative hazard)."""
    ramp = HMAX * (H1 - H0) / 2.0
    if E < ramp:
        return H0 + math.sqrt(2.0 * (H1 - H0) * E / HMAX)
    return H1 + (E - ramp) / HMAX


# ------------------------------------------------------------------------------------------------------------ hubs
# code, name, county, site type, kind, programme, own pillar, HX150 commissioning dates, supply interruptions a
# year, callout attendance (days, mean), ordinary faults a unit-year, HX150 charges a day, RC50 charges a day,
# visit months
HUBS = [
    ("NM112", "Carrigvane Services", "Westmeath", "Motorway service area", "M", True, False, ["2021-05-18", "2021-05-18"], 0.6, 0.98, 0.42, 8.3, 2.1, (1, 3, 5, 7, 9, 11)),
    ("NM127", "Lismoy Services", "Longford", "Motorway service area", "M", True, False, ["2021-08-24", "2022-03-09"], 0.5, 1.03, 0.38, 7.6, 1.9, (2, 4, 6, 8, 10, 12)),
    ("NM104", "Ardcree Services", "Roscommon", "Motorway service area", "M", True, False, ["2021-03-02", "2021-03-02", "2022-11-15"], 0.7, 0.95, 0.44, 8.8, 2.3, (1, 3, 5, 7, 9, 11)),
    ("NM141", "Knockvane Services", "Westmeath", "Motorway service area", "M", False, False, ["2021-10-12", "2021-10-12"], 0.5, 1.01, 0.4, 7.9, 2.0, (2, 4, 6, 8, 10, 12)),
    ("NM133", "Drumtane Services", "Cavan", "Motorway service area", "M", False, False, ["2021-06-29", "2021-06-29", "2023-04-18"], 0.6, 0.97, 0.43, 8.1, 2.2, (1, 3, 5, 7, 9, 11)),
    ("NM158", "Monaleen Services", "Longford", "Motorway service area", "M", False, False, ["2022-02-01", "2022-02-01"], 0.4, 1.04, 0.37, 7.2, 1.8, (2, 4, 6, 8, 10, 12)),
    ("NM109", "Kilbeg Retail Park", "Westmeath", "Retail park", "P", True, False, ["2021-07-06"], 0.6, 2.55, 0.41, 5.6, 1.7, (3, 9)),
    ("NM121", "Tullymore Market Square", "Cavan", "Town centre car park", "P", True, False, ["2021-09-14", "2022-06-21"], 0.7, 2.61, 0.39, 5.1, 1.6, (4, 10)),
    ("NM117", "Clonlea Leisure Centre", "Roscommon", "Leisure centre", "P", True, False, ["2021-11-30", "2021-11-30"], 0.5, 2.52, 0.4, 4.7, 1.5, (3, 9)),
    ("NM146", "Rathmoy Station Road", "Longford", "Railway station car park", "P", True, False, ["2022-04-26"], 0.8, 2.58, 0.43, 5.3, 1.8, (5, 11)),
    ("NM103", "Glenfad Shopping Centre", "Sligo", "Shopping centre", "P", True, False, ["2021-04-13", "2022-09-06"], 0.6, 2.63, 0.38, 5.9, 1.9, (2, 8)),
    ("NM138", "Ballinkeel Main Street", "Leitrim", "Town centre car park", "P", True, False, ["2022-01-18", "2022-01-18"], 0.7, 2.56, 0.42, 4.4, 1.4, (4, 10)),
    ("NM150", "Derrylane Park and Ride", "Cavan", "Park and ride", "P", True, False, ["2022-07-12"], 0.6, 2.53, 0.4, 4.9, 1.6, (5, 11)),
    ("NM125", "Annagh Cross", "Roscommon", "Rural crossroads", "R", True, False, ["2022-05-10", "2022-05-10"], 6.3, 1.06, 0.41, 3.1, 1.2, (3, 9)),
    ("NM162", "Cloonfin Crossroads", "Longford", "Rural crossroads", "R", True, False, ["2021-12-07", "2021-12-07", "2023-02-21"], 6.9, 1.02, 0.39, 2.9, 1.1, (4, 10)),
    ("NM119", "Bunacurry Pier", "Mayo", "Harbour", "C", False, True, ["2022-03-22", "2022-03-22"], 1.1, 2.12, 1.18, 3.4, 1.3, (5, 11)),
    ("NM144", "Rossnabeg Harbour", "Donegal", "Harbour", "C", False, True, ["2021-06-08", "2022-10-04"], 0.9, 2.08, 1.24, 3.7, 1.4, (3, 9)),
    ("NM131", "Portavaddy Seafront", "Sligo", "Seafront car park", "C", False, True, ["2021-08-03", "2021-08-03", "2022-12-13"], 1.0, 2.1, 1.21, 3.9, 1.5, (4, 10)),
    ("NM155", "Carrowkeel Business Park", "Sligo", "Business park", "S", False, True, ["2022-08-30", "2022-08-30"], 0.6, 2.16, 0.41, 4.1, 1.5, (2, 8)),
    ("NM166", "Tobernalt Road", "Leitrim", "Town centre car park", "S", False, True, ["2022-10-25", "2023-03-14"], 0.7, 2.14, 0.4, 3.8, 1.4, (5, 11)),
    ("NM106", "Ballyroe Town Park", "Mayo", "Town park", "O", False, False, ["2021-05-25", "2021-05-25"], 0.6, 1.42, 0.4, 4.6, 1.6, (3, 9)),
    ("NM129", "Corrabeg Business Park", "Cavan", "Business park", "O", False, False, ["2022-02-15"], 0.5, 1.31, 0.41, 4.2, 1.5, (4, 10)),
    ("NM114", "Dromkeen Square", "Leitrim", "Town centre car park", "O", False, False, ["2021-10-05", "2022-08-16"], 0.7, 1.55, 0.39, 4.0, 1.4, (2, 8)),
    ("NM137", "Eskerbrook Shopping Centre", "Westmeath", "Shopping centre", "O", False, False, ["2021-03-16", "2021-03-16", "2022-05-24"], 0.4, 1.24, 0.42, 6.2, 2.0, (5, 11)),
    ("NM148", "Gortnaclay Leisure Park", "Roscommon", "Leisure centre", "O", False, False, ["2022-06-07"], 0.6, 1.47, 0.38, 4.4, 1.5, (3, 9)),
    ("NM122", "Kilmeedy Church Street", "Longford", "Town centre car park", "O", False, False, ["2021-12-14", "2021-12-14"], 0.8, 1.36, 0.4, 3.9, 1.3, (4, 10)),
    ("NM152", "Lisduff Retail Park", "Westmeath", "Retail park", "O", False, False, ["2022-03-01", "2023-05-09"], 0.5, 1.28, 0.43, 5.4, 1.8, (2, 8)),
    ("NM135", "Moyvalley Station", "Westmeath", "Railway station car park", "O", False, False, ["2022-09-20"], 0.6, 1.51, 0.41, 4.3, 1.4, (5, 11)),
    ("NM118", "Shanbally Community Centre", "Sligo", "Community centre", "O", False, False, ["2021-07-27", "2021-07-27"], 0.7, 1.44, 0.39, 3.6, 1.2, (3, 9)),
    ("NM160", "Templederry Green", "Mayo", "Village green", "O", False, False, ["2022-11-08"], 0.5, 1.39, 0.4, 3.3, 1.1, (4, 10)),
]
NEW_UNIT_KINDS = ("M", "P")          # the programme puts a new HX150 at its motorway and standard hubs
WORKS = {  # the programme's works at each hub (Irish dates): RC50 out, new unit in, the pillar isolated for both
    "NM112": "2026-12-01", "NM127": "2026-12-03", "NM104": "2026-12-08", "NM109": "2026-11-30", "NM121": "2026-12-02",
    "NM117": "2026-12-04", "NM146": "2026-12-09", "NM103": "2026-12-10", "NM138": "2026-12-14", "NM150": "2026-12-15",
    "NM125": "2026-12-16", "NM162": "2026-12-17"}


def hub_table():
    out = []
    for i, h in enumerate(HUBS):
        code, name, county, site, kind, prog, own, comm, dso, att, frate, hxc, rcc, months = h
        out.append(dict(i=i, code=code, name=name, county=county, site=site, kind=kind, prog=prog, own=own,
                        comm=comm, dso=dso, att=att, frate=frate, hx_charges=hxc, rc_charges=rcc, months=months))
    return out


def works_time(code):
    y, m, d = map(int, WORKS[code].split("-"))
    return from_local(y, m, d, 9, 30)


# ---------------------------------------------------------------------------------------------------------- units
def unit_table(hubs, rng):
    """Every unit: an RC50 per hub (2017-2019) and the HX150 units; previous IDs from the 2017 back office, new IDs
    from the June 2025 migration, serials as the makers stamp them."""
    units = []
    for k, h in enumerate(hubs):
        y = 2017 + int(rng.integers(0, 3))
        dd = dt.date(y, int(rng.integers(2, 12)), int(rng.integers(1, 28)))
        units.append(dict(uid="RC%02d" % k, hub=h["code"], model="RC50", make="Tavrin", kw=50, connectors=2,
                          commissioned=dd.isoformat(), bay=1))
        for j, c in enumerate(h["comm"]):
            units.append(dict(uid="HX%02d%d" % (k, j), hub=h["code"], model="HX150", make="Korrant", kw=150,
                              connectors=2, commissioned=c, bay=j + 2))
    old_no = 1000 + int(rng.integers(20, 60))
    for u in sorted(units, key=lambda u: (u["commissioned"], u["uid"])):
        old_no += int(rng.integers(1, 5))
        u["old_id"] = "AV%04d" % old_no
    for u in units:
        u["new_id"] = "IE-ARV-%s%02d" % (u["hub"][2:], u["bay"] * 3 + int(rng.integers(0, 3)))
        yy = u["commissioned"][2:4]
        if u["model"] == "HX150":
            u["serial"] = "KX15-%s%s-%05d" % (yy, "ABCDEFGHJK"[int(rng.integers(0, 10))], int(rng.integers(10000, 99999)))
        else:
            u["serial"] = "TRC50/%s/%04d" % (yy, int(rng.integers(1000, 9999)))
    return units


def commissioned_t(u):
    d = dt.date.fromisoformat(u["commissioned"])
    return max(0, from_local(d.year, d.month, d.day, 11, 0))


# ------------------------------------------------------------------------------------------------- hub event plans
def visit_dates(h, year, rng):
    """Planned visits (Irish dates) in a year: two a year, two-monthly at the motorway hubs, on a weekday."""
    out = []
    for m in h["months"]:
        d = dt.date(year, m, int(rng.integers(3, 25)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        out.append(d)
    return out


def visit_event(d, rng, notified=None):
    ws = from_local(d.year, d.month, d.day, 8, 30)
    we = from_local(d.year, d.month, d.day, 14, 30)
    arrive = ws + int(rng.integers(15, 75)) * 60
    s = arrive + int(rng.integers(12, 35)) * 60
    return dict(kind="visit", s=s, e=s + int(rng.integers(55, 150)) * 60, arrive=arrive, ws=ws, we=we, date=d,
                notified=notified)


def plan_hub(h, rng, start, end, years=(2023, 2024, 2025, 2026)):
    """Every pillar power-down and job at a hub between start and end (seconds): visits (both pillars), supply
    interruptions (both pillars), the RC50's monthly cabinet service and its cabinet repairs (its own pillar), and
    the RC50's other jobs (no isolation)."""
    ev = []
    for y in years:
        for d in visit_dates(h, y, rng):
            e = visit_event(d, rng, notified=d - dt.timedelta(days=int(rng.integers(14, 40))))
            if start <= e["ws"] < end:
                ev.append(e)
    t = start
    rate = h["dso"] / 365.0 / DAY
    while True:
        t += int(rng.exponential(1.0 / rate))
        if t >= end:
            break
        med = 130 if h["kind"] == "R" else 80
        dur = int(min(9 * 3600, max(22 * 60, rng.lognormal(math.log(med * 60), 0.6))))
        planned = rng.random() < 0.12
        s = t
        if planned:
            lt = local(t)
            s = from_local(lt.year, lt.month, lt.day, 9, 0) + int(rng.integers(0, 60)) * 60
            dur = int(rng.integers(180, 330)) * 60
            if s < start or s >= end:
                continue
        ev.append(dict(kind="dso", s=s, e=s + dur, planned=planned))
    wk = int(rng.integers(0, 3))
    first = local(start)
    y, m = first.year, first.month
    while True:
        d = dt.date(y, m, 1) + dt.timedelta(days=7 * wk + int(rng.integers(0, 7)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        s = from_local(d.year, d.month, d.day, 10, 0) + int(rng.integers(0, 270)) * 60
        if s >= end:
            break
        if s >= start and rng.random() > 0.03:
            ev.append(dict(kind="service", s=s, e=s + int(rng.integers(25, 46)) * 60,
                           arrive=s - int(rng.integers(5, 20)) * 60))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    worn = h["kind"] in ("C", "S")     # the coastal RC50s and the two 2017 units at the inland pair need more work
    for kind, per_year in (("repair", 6.8 if worn else 3.5), ("other", 14.5 if worn else 10.0)):
        t = start
        while True:
            t += int(rng.exponential(365.0 * DAY / per_year))
            if t >= end:
                break
            arrive = t + max(3 * 3600, int(rng.gamma(3.0, h["att"] * DAY / 3.0)))
            dur = int(rng.integers(40, 71)) * 60 if kind == "repair" else int(rng.integers(30, 95)) * 60
            s = arrive + int(rng.integers(5, 15)) * 60
            ev.append(dict(kind=kind, fault=t, s=s, e=s + dur, arrive=arrive))
    ev.sort(key=lambda e: (e["s"], e["kind"]))
    return ev


def powerdowns_for(h, ev, model):
    """The isolations that cut a unit's supply: visits, interruptions and the programme works always; the RC50's
    service and cabinet repairs for the RC50 itself, and for the HX150 units only where they share its pillar."""
    out = []
    for e in ev:
        if e["kind"] in ("visit", "dso", "works"):
            out.append((e["s"], e["e"], e["kind"]))
        elif e["kind"] in ("service", "repair"):
            if model == "RC50" or not h["own"]:
                out.append((e["s"], e["e"], e["kind"]))
    return sorted(out)


# ------------------------------------------------------------------------------------------------ the HX150 engine
def run_hx(rng, start, end, pds, t_up, att_days, frate_yr, tau_fn=hang_tau, comms_rate=0.04, comms_min=(16, 61)):
    """One HX150 from start to end under the pillar power-downs pds [(s, e, kind)]. Returns its non-Available
    intervals [(a, b, status, cause)] with the back office's lag applied, its power-ups, its hangs
    [(t, restart, by, arrive)] and its faults [(t, arrive, done)]."""
    frate = frate_yr / 365.0 / DAY
    iv, ups, hangs, faults = [], [], [], []
    t = max(start, t_up)
    k = 0
    E = rng.exponential()
    t_hang = t_up + int(tau_fn(E) * DAY)
    while True:
        while k < len(pds) and pds[k][0] < t:
            k += 1
        pd = pds[k] if k < len(pds) else (end + 400 * DAY, end + 400 * DAY, "end")
        t_fault = t + int(rng.exponential(1.0 / frate)) if frate > 0 else end + 400 * DAY
        nxt = min(pd[0], t_fault, t_hang)
        if nxt >= end:
            break
        lag = 600 + int(rng.integers(0, HB))
        boot = int(rng.integers(150, 361))
        if nxt == pd[0]:
            if pd[2] == "visit":
                iv.append((pd[0] - int(rng.integers(5, 21)) * 60, pd[0] + lag, "Unavailable", "visit"))
            iv.append((pd[0] + lag, pd[1] + boot, "Offline", pd[2]))
            t_up = pd[1]
            k += 1
        elif nxt == t_hang:
            arrive = t_hang + max(3 * 3600, int(rng.gamma(3.0, att_days * DAY / 3.0)))
            restart, by = arrive + int(rng.integers(6, 25)) * 60, "technician"
            while k < len(pds) and pds[k][1] <= t_hang:
                k += 1
            if k < len(pds) and t_hang < pds[k][0] < arrive:
                restart, by = pds[k][1], pds[k][2]
                k += 1
            iv.append((t_hang + lag, restart + boot, "Offline", "hang"))
            hangs.append((t_hang, restart, by, arrive))
            t_up = restart
        else:
            arrive = t_fault + max(2 * 3600, int(rng.gamma(3.0, att_days * DAY / 3.0)))
            iso = arrive + int(rng.integers(3, 12)) * 60
            done = iso + int(rng.integers(30, 151)) * 60
            iv.append((t_fault, iso + lag, "Faulted", "fault"))
            iv.append((iso + lag, done + boot, "Offline", "repair"))
            faults.append((t_fault, arrive, done))
            t_up = done
        ups.append(t_up)
        t = t_up + boot
        E = rng.exponential()
        t_hang = t_up + int(tau_fn(E) * DAY)
    if comms_rate:
        busy = sorted((a - 1200, b + 600) for a, b, _, _ in iv)
        tt = start
        while True:
            tt += int(rng.exponential(DAY / comms_rate))
            if tt >= end:
                break
            b = tt + int(rng.integers(*comms_min)) * 60
            lag = 600 + int(rng.integers(0, HB))
            if any(x < b and tt < y for x, y in busy) or tt + lag >= b:
                continue
            iv.append((tt + lag, b + int(rng.integers(5, 61)), "Offline", "comms"))
    iv.sort()
    return iv, ups, hangs, faults


def run_rc(rng, start, end, ev):
    """The RC50's own non-Available time: its service, repairs, other jobs, the pillar power-downs and comms."""
    iv = []
    for e in ev:
        lag = 600 + int(rng.integers(0, HB))
        if e["kind"] in ("visit", "dso"):
            if e["kind"] == "visit":
                iv.append((e["s"] - int(rng.integers(5, 21)) * 60, e["s"] + lag, "Unavailable", "visit"))
            iv.append((e["s"] + lag, e["e"] + int(rng.integers(150, 361)), "Offline", e["kind"]))
        elif e["kind"] == "service":
            iv.append((e["arrive"], e["s"] + lag, "Unavailable", "service"))
            iv.append((e["s"] + lag, e["e"] + int(rng.integers(300, 900)), "Offline", "service"))
        elif e["kind"] == "repair":
            iv.append((e["fault"], e["s"] + lag, "Faulted", "repair"))
            iv.append((e["s"] + lag, e["e"] + int(rng.integers(150, 361)), "Offline", "repair"))
        elif e["kind"] == "other":
            iv.append((e["fault"], e["e"], "Faulted", "other"))
    busy = sorted((a - 1200, b + 600) for a, b, _, _ in iv)
    tt = start
    while True:
        tt += int(rng.exponential(DAY / 0.04))
        if tt >= end:
            break
        b = tt + int(rng.integers(16, 61)) * 60
        lag = 600 + int(rng.integers(0, HB))
        if any(x < b and tt < y for x, y in busy) or tt + lag >= b:
            continue
        iv.append((tt + lag, b + int(rng.integers(5, 61)), "Offline", "comms"))
    iv.sort()
    return iv


# --------------------------------------------------------------------------------------------------- the history
def history(seed=SEED):
    """The clean truth from 1 January 2023 to 31 October 2026."""
    hubs = hub_table()
    units = unit_table(hubs, np.random.default_rng(seed + 7))
    plans, runs = {}, {}
    for h in hubs:
        ev = plan_hub(h, np.random.default_rng([seed, h["i"], 1]), 0, HIST_END)
        plans[h["code"]] = ev
        for u in [u for u in units if u["hub"] == h["code"]]:
            ur = np.random.default_rng([seed, h["i"], 2, u["bay"]])
            start = commissioned_t(u)
            if u["model"] == "HX150":
                pds = [p for p in powerdowns_for(h, ev, "HX150") if p[1] > start]
                if start == 0:
                    t_up = -int(ur.integers(0, 70 if h["own"] else 28)) * DAY - int(ur.integers(0, DAY))
                else:
                    t_up = start
                iv, ups, hangs, faults = run_hx(ur, start, HIST_END, pds, t_up, h["att"], h["frate"])
                runs[u["uid"]] = dict(start=start, t_up0=t_up, iv=iv, ups=ups, hangs=hangs, faults=faults)
            else:
                iv = run_rc(ur, start, HIST_END, [e for e in ev if e["s"] >= start])
                runs[u["uid"]] = dict(start=start, iv=iv, ups=[], hangs=[], faults=[])
    return dict(hubs=hubs, units=units, plans=plans, runs=runs, seed=seed)


# ------------------------------------------------------------------------------------------------------ 2027 truth
def plan_2027(h, seed=SEED):
    """The 2027 visit plan (Irish dates), the schedule's own sheet."""
    return visit_dates(h, 2027, np.random.default_rng([seed, h["i"], 27]))


def year27_events(h, rng, plan27):
    """Power-downs from 1 November 2026 to 31 December 2027: the 2027 visit plan, supply interruptions, the RC50's
    service and repairs where it stays, and at a programme hub the works that take it out."""
    ev = [e for e in plan_hub(h, rng, HIST_END, Y27_END, years=(2026,))]
    for d in plan27:
        ev.append(visit_event(d, rng))
    if h["prog"]:
        s = works_time(h["code"])
        ev = [e for e in ev if not (e["kind"] in ("service", "repair", "other") and e["s"] > s - 3 * DAY)]
        ev.append(dict(kind="works", s=s, e=s + 5 * 3600))
    ev.sort(key=lambda e: (e["s"], e["kind"]))
    return ev


def merge(lst, a, b):
    out = []
    for x, y in sorted(lst):
        x, y = max(x, a), min(y, b)
        if y > x:
            if out and x <= out[-1][1]:
                out[-1][1] = max(out[-1][1], y)
            else:
                out.append([x, y])
    return out


def schedule4(iv, excl, a, b):
    """Availability over [a, b): non-Available time outside the excluded windows over the time outside them."""
    ex = merge(excl, a, b)
    dn = merge([(x, y) for x, y, *_ in iv], a, b)
    inter = 0
    for x, y in dn:
        for p, q in ex:
            lo, hi = max(x, p), min(y, q)
            if hi > lo:
                inter += hi - lo
    down = sum(y - x for x, y in dn) - inter
    return 1.0 - down / float((b - a) - sum(y - x for x, y in ex))


def excluded(ev):
    out = []
    for e in ev:
        if e["kind"] == "visit":
            out.append((e["ws"], e["we"] + EXCL_TAIL))
        elif e["kind"] in ("dso", "works"):
            out.append((e["s"], e["e"] + EXCL_TAIL))
    return out


def units_2027(H, h):
    hx = [u for u in H["units"] if u["hub"] == h["code"] and u["model"] == "HX150"]
    return hx, len(hx) + (1 if (h["prog"] and h["kind"] in NEW_UNIT_KINDS) else 0)


def truth_2027(H, reps=300, seed=SEED):
    """Each HX150's expected 2027 availability under the true mechanism, averaged over simulated years."""
    res = {}
    for h in H["hubs"]:
        plan27 = plan_2027(h, seed)
        hx, n27 = units_2027(H, h)
        acc = np.zeros(n27)
        for r in range(reps):
            rr = np.random.default_rng([seed, h["i"], 2700, r])
            ev = year27_events(h, rr, plan27)
            pds = [p for p in powerdowns_for(h, ev, "HX150") if p[1] > HIST_END]
            ex = excluded(ev)
            for j in range(n27):
                if j < len(hx):
                    run = H["runs"][hx[j]["uid"]]
                    t_up = run["ups"][-1] if run["ups"] else run["t_up0"]
                else:
                    t_up = works_time(h["code"]) + 5 * 3600
                iv, _, _, _ = run_hx(rr, HIST_END, Y27_END, pds, t_up, h["att"], h["frate"])
                acc[j] += schedule4(iv, ex, Y27_START, Y27_END)
        res[h["code"]] = acc / reps
    return res


# ------------------------------------------------------------------------------------------------ 2026 charges
def charges_2026(H, seed=SEED, salt=None):
    """Every charge begun at every unit from 1 January to 31 October 2026, as connections, each with the records
    the back office makes of it: a record closed when it hears nothing from the unit for five minutes and resumed
    without a token, and a card charge closed at its pre-authorisation and continued under a new one."""
    out = []
    tok_rng = np.random.default_rng([seed, 9001])
    pool = ["%08X" % int(x) for x in tok_rng.integers(0x10000000, 0xFFFFFFFF, 26000)]
    weights = 1.0 / np.arange(1, len(pool) + 1) ** 0.85
    weights /= weights.sum()
    prof = np.array([0.15, 0.1, 0.08, 0.08, 0.1, 0.2, 0.45, 0.8, 1.0, 1.05, 1.1, 1.15, 1.2, 1.15, 1.1, 1.15, 1.25,
                     1.35, 1.3, 1.1, 0.85, 0.6, 0.4, 0.25])
    prof = prof / prof.mean()
    for h in H["hubs"]:
        for u in [u for u in H["units"] if u["hub"] == h["code"]]:
            rng = np.random.default_rng([seed, h["i"], 26, u["bay"], (salt or {}).get(h["code"], 0)])
            hx = u["model"] == "HX150"
            rate = (h["hx_charges"] if hx else h["rc_charges"]) / DAY
            down = sorted((a, b) for a, b, st, cause in H["runs"][u["uid"]]["iv"]
                          if cause != "comms" and b > S26_START - DAY and a < HIST_END)
            age_years = (S26_START - commissioned_t(u)) / (365.0 * DAY) if commissioned_t(u) > 0 else \
                (dt.date(2026, 1, 1) - dt.date.fromisoformat(u["commissioned"])).days / 365.0
            reg = [int(rng.uniform(0.8, 1.2) * age_years * (h["hx_charges"] if hx else h["rc_charges"]) * 0.5 * 365 *
                       (28000 if hx else 18000)) + int(rng.integers(0, 999)) for _ in range(2)]
            busy = [S26_START, S26_START]
            drops = []
            if hx:
                tt = S26_START
                while True:
                    tt += int(rng.exponential(DAY / 2.5))
                    if tt >= HIST_END:
                        break
                    drops.append((tt, tt + int(rng.integers(6 * 60, 18 * 60))))
            di = 0
            t = S26_START
            pmax = prof.max()
            while True:
                t += int(rng.exponential(1.0 / (rate * pmax)))
                if t >= HIST_END - 3 * 3600:
                    break
                if rng.random() > prof[local(t).hour] / pmax:
                    continue
                if any(a <= t < b for a, b in down):
                    continue
                free = [c for c in (0, 1) if busy[c] <= t]
                if not free:
                    continue
                c = free[0] if len(free) == 1 else int(rng.integers(0, 2))
                failed = rng.random() < 0.04
                if failed:
                    E, dur = 0, int(rng.integers(20, 151))
                else:
                    E = float(np.clip(rng.lognormal(math.log(28.0 if hx else 18.0), 0.55 if hx else 0.5), 3, 95 if hx else 60))
                    P = rng.uniform(45, 115) if hx else rng.uniform(22, 44)
                    dur = int(E / P * 3600) + int(rng.integers(60, 241))
                end = t + dur
                for a, b in down:
                    if a < end and t < a:
                        if not failed:
                            E = E * (a - t) / float(dur)
                        end = a
                        break
                Ewh = int(round(E * 1000))
                if Ewh <= 0 and not failed:
                    continue
                r = rng.random()
                auth = "app" if r < 0.52 else "rfid" if r < 0.72 else "roaming" if r < 0.85 else "card"
                token = "" if auth == "card" else pool[int(rng.choice(len(pool), p=weights))]
                t0, m0 = t, reg[c]
                reg[c] += Ewh
                # cut points: the card's pre-authorisation, and every drop the unit makes while charging
                cuts = []
                if hx and auth == "card" and Ewh > CAP_WH + 2000:
                    tc = t0 + int((end - t0) * CAP_WH / float(Ewh))
                    cuts.append(("card", tc, tc + int(rng.integers(1, 5)), m0 + CAP_WH))
                while di < len(drops) and drops[di][1] < t0:
                    di += 1
                j = di
                while hx and j < len(drops) and drops[j][0] < end:
                    a, b = drops[j]
                    if a > t0 + 120 and b + 120 < end:
                        last = a - int(rng.integers(0, 61))
                        first = b + int(rng.integers(0, 61))
                        cuts.append(("drop", last, first, None))
                    j += 1
                cuts.sort(key=lambda x: x[1])
                recs, s, ms, tok = [], t0, m0, token
                ok = True
                for kind, cs, ce, mcut in cuts:
                    if cs <= s + 60 or ce >= end - 60:
                        continue
                    stop_m = m0 + int(round(Ewh * (cs - t0) / float(end - t0))) if mcut is None else mcut
                    next_m = m0 + int(round(Ewh * (ce - t0) / float(end - t0))) if kind == "drop" else stop_m
                    if stop_m <= ms or next_m < stop_m:
                        ok = False
                        break
                    recs.append(dict(start=s, stop=cs, m0=ms, m1=stop_m, token=tok))
                    s, ms, tok = ce, next_m, ""
                if not ok:
                    recs, s, ms, tok = [], t0, m0, token
                recs.append(dict(start=s, stop=end, m0=ms, m1=m0 + Ewh, token=tok))
                out.append(dict(uid=u["uid"], hub=h["code"], model=u["model"], connector=c + 1, start=t0, stop=end,
                                m0=m0, m1=m0 + Ewh, auth=auth, failed=failed, recs=recs))
                busy[c] = end + int(rng.integers(150, 420))
    out.sort(key=lambda x: (x["start"], x["uid"], x["connector"]))
    return out
