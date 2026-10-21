"""The operations behind the asks: grid outages at the stations, the maintenance contractor's work, the validation
crew's nights at the cabinets, and what TrafficVault and the contractor record of them.

A grid outage cuts mains power to one to four stations of a district at once. A TCX-4 controller carries a battery and
keeps counting for up to six hours, logging MAINS_FAIL and MAINS_OK; beyond six hours it shuts down, and when power
returns it starts cold with its clock at 1 January 2000 until TrafficVault sets it, so the hours it counted before the
clock was set are lost. A TCX-2 controller has no battery and reports no events: it stops, and its record lacks every
hour from the one the power failed in to the one it returned in (a partial hour is discarded). Each station's modem
runs on mains, so TrafficVault's 15-minute poll raises COMMS_LOST during any outage a poll falls in, and COMMS_OK at the
first poll after it.

The maintenance contractor inspects every station each spring and autumn on district route days, attends faults, and at
TCX-4 stations clears some communications faults by resetting the controller from its office. Every piece of work is
booked as labour against a work order. A TCX-4 cabinet door logs DOOR_OPEN and DOOR_CLOSE; the validation crew opens
every cabinet the night before its filmed day to connect its pulse recorder and the night after to remove it. Two
stations had their TCX-2 replaced by a TCX-4 during the year and took new numbers."""
import datetime as dt
import math

import numpy as np

import params as P
import sim

BATTERY_H = 6.0
POLL_S = 900
BOOT_S = 90
Y2K = dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc)
TECHS = ["D. Okafor", "R. Lindqvist", "S. Brennan", "T. Mahoney", "K. Varga", "P. Duchesne"]


def controller(x, day):
    """TCX-4 or TCX-2 on a day (the renumbered stations ran a TCX-2 until their controller was replaced)"""
    code = x["code"]
    if code in P.RENUMBERED:
        return "TCX-4" if day >= P.RENUMBERED[code][1] else "TCX-2"
    return "TCX-4" if code in P.NEW_CONTROLLERS else "TCX-2"


def utc(local):
    return local.replace(tzinfo=sim.TZ).astimezone(sim.UTC)


def local(t):
    return t.astimezone(sim.TZ).replace(tzinfo=None)


def quarter(day):
    return (day.month - 1) // 3 + 1


def hour_index(t):
    return int((t - sim.START_UTC).total_seconds() // 3600)


def poll_offsets(W):
    rng = np.random.default_rng(W["seed"] + 610)
    return {x["code"]: float(rng.uniform(0, POLL_S)) for x in W["st"]}


def poll_after(off, t):
    """the first of a station's polls after t"""
    s = (t - sim.START_UTC).total_seconds() - off
    k = math.floor(s / POLL_S) + 1
    return sim.START_UTC + dt.timedelta(seconds=round(off + k * POLL_S))


def outages(W, rng):
    """grid outages: a December ice storm long enough to run TCX-4 batteries out, a late evening outage on 30
    September, then one or two in every district and quarter, each cell's set stopping at least one TCX-2"""
    st = W["st"]
    days = W["C"]["days"]
    sx = {x["code"]: x for x in st}
    out = []

    def clear(dist, start, end, hit):
        if end.date() != start.date() or start.time() < dt.time(0, 5) or end.time() > dt.time(23, 55):
            return False
        if start.date() in (dt.date(P.YEAR, 1, 1), dt.date(P.YEAR, 12, 31)):
            return False
        for x in hit:
            if abs((x["vday"] - start.date()).days) <= 1:
                return False
            if x["code"] in P.RENUMBERED and abs((P.RENUMBERED[x["code"]][1] - start.date()).days) <= 2:
                return False
        return not any(o["district"] == dist and abs((o["start"] - start).total_seconds()) < 3 * 86400 for o in out)

    def make(dist, start, hours, hit, parts=None):
        end = start + dt.timedelta(hours=hours)
        out.append(dict(district=dist, start=start, end=end, parts=parts or [(start, end)],
                        stations=[x["code"] for x in hit], lag={x["code"]: float(rng.uniform(0, 40)) for x in hit}))

    def retrip(start):
        """a feeder that recloses and trips again: two losses within the hour"""
        d1 = dt.timedelta(minutes=int(rng.integers(18, 41)), seconds=int(rng.integers(60)))
        up = dt.timedelta(minutes=int(rng.integers(22, 46)), seconds=int(rng.integers(60)))
        d2 = dt.timedelta(minutes=int(rng.integers(18, 71)), seconds=int(rng.integers(60)))
        return [(start, start + d1), (start + d1 + up, start + d1 + up + d2)]

    def members(dist, day, ctl):
        return [x for x in st if x["district"] == dist and controller(x, day) == ctl]

    for _ in range(500):
        dist = P.DISTRICTS[int(rng.integers(3))]
        day = dt.date(P.YEAR, 12, int(rng.integers(6, 21)))
        t4, t2 = members(dist, day, "TCX-4"), members(dist, day, "TCX-2")
        if len(t4) < 2 or not t2:
            continue
        hit = [t4[i] for i in sorted(rng.choice(len(t4), 2, replace=False))] + [t2[int(rng.integers(len(t2)))]]
        start = dt.datetime.combine(day, dt.time(int(rng.integers(2, 11)), int(rng.integers(60)), int(rng.integers(60))))
        hours = float(rng.uniform(7.4, 9.6))
        if clear(dist, start, start + dt.timedelta(hours=hours), hit):
            make(dist, start, hours, hit)
            break
    for _ in range(500):
        dist = P.DISTRICTS[int(rng.integers(3))]
        day = dt.date(P.YEAR, 9, 30)
        t4, t2 = members(dist, day, "TCX-4"), members(dist, day, "TCX-2")
        if not t4 or not t2:
            continue
        hit = [t4[int(rng.integers(len(t4)))], t2[int(rng.integers(len(t2)))]]
        start = dt.datetime.combine(day, dt.time(20, 40)) + dt.timedelta(seconds=int(rng.integers(0, 5400)))
        hours = float(rng.uniform(0.5, 1.3))
        if clear(dist, start, start + dt.timedelta(hours=hours), hit):
            make(dist, start, hours, hit)
            break
    for dist in P.DISTRICTS:
        members_all = [x for x in st if x["district"] == dist]
        for qtr in (1, 2, 3, 4):
            qdays = [d for d in days if quarter(d) == qtr]
            have_t2 = any(o["district"] == dist and quarter(o["start"].date()) == qtr and
                          any(controller(sx[c], o["start"].date()) == "TCX-2" for c in o["stations"]) for o in out)
            n = int(rng.integers(1, 3))
            made = tries = 0
            while made < n and tries < 400:
                tries += 1
                day = qdays[int(rng.integers(len(qdays)))]
                k = int(rng.integers(1, 5))
                hit = [members_all[i] for i in rng.choice(len(members_all), size=min(k, len(members_all)),
                                                          replace=False)]
                if not have_t2 and not any(controller(x, day) == "TCX-2" for x in hit):
                    continue
                start = dt.datetime.combine(day, dt.time(int(rng.integers(0, 24)), int(rng.integers(0, 60)),
                                                         int(rng.integers(0, 60))))
                parts = retrip(start) if rng.random() < 0.4 else None
                hours = (parts[-1][1] - start).total_seconds() / 3600 if parts else \
                    float(np.clip(rng.lognormal(np.log(1.6), 0.9), 0.3, 5.5))
                if not clear(dist, start, start + dt.timedelta(hours=hours), hit):
                    continue
                make(dist, start, hours, hit, parts)
                made += 1
                have_t2 = have_t2 or any(controller(x, day) == "TCX-2" for x in hit)
    return sorted(out, key=lambda o: o["start"])


def power(W, outs, polls):
    """what each outage did at each station it hit: the events, the hours lost from the record, and whether it ran a
    TCX-4 battery out"""
    sx = {x["code"]: x for x in W["st"]}
    recs = []
    for o in outs:
        for c in o["stations"]:
            ctl = controller(sx[c], o["start"].date())
            lag = dt.timedelta(seconds=o["lag"][c])
            ev, lost, drained = [], set(), False
            for a, b in o["parts"]:
                t0, t1 = utc(a) + lag, utc(b) + lag
                p_lost = poll_after(polls[c], t0)
                comms = p_lost < t1 + dt.timedelta(seconds=BOOT_S)
                p_ok = poll_after(polls[c], t1 + dt.timedelta(seconds=BOOT_S))
                if comms:
                    ev.append((p_lost, "TrafficVault", "COMMS_LOST"))
                    ev.append((p_ok, "TrafficVault", "COMMS_OK"))
                if ctl == "TCX-4":
                    ev.append((t0, "controller", "MAINS_FAIL"))
                    if (t1 - t0).total_seconds() > BATTERY_H * 3600:
                        drained = True
                        ev.append((Y2K + dt.timedelta(seconds=4), "controller", "COLD_START"))
                        ev.append((Y2K + dt.timedelta(seconds=5), "controller", "MAINS_OK"))
                        clock = p_ok + dt.timedelta(seconds=9)
                        ev.append((clock, "TrafficVault", "CLOCK_SET"))
                        lost |= set(range(hour_index(t0 + dt.timedelta(hours=BATTERY_H)), hour_index(clock) + 1))
                    else:
                        ev.append((t1, "controller", "MAINS_OK"))
                else:
                    lost |= set(range(hour_index(t0), hour_index(t1 + dt.timedelta(seconds=BOOT_S)) + 1))
            recs.append(dict(code=c, outage=o, controller=ctl, events=ev, lost=lost, drained=drained,
                             window=(utc(o["start"]) + lag, utc(o["end"]) + lag)))
    return recs


def swaps(W, polls, rng):
    """the two controller replacements: the old TCX-2 unplugged mid-morning, the new TCX-4 started cold, its clock set
    at TrafficVault's next poll; the hours between are lost and the station counts under its new number after"""
    out = {}
    for code, (new, day) in sorted(P.RENUMBERED.items()):
        arrive = dt.datetime.combine(day, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 50)))
        unplug = arrive + dt.timedelta(minutes=int(rng.integers(15, 35)))
        boot = unplug + dt.timedelta(minutes=int(rng.integers(120, 190)), seconds=int(rng.integers(60)))
        leave = boot + dt.timedelta(minutes=int(rng.integers(35, 70)))
        tu, tb = utc(unplug), utc(boot)
        p_lost = poll_after(polls[code], tu)
        p_ok = poll_after(polls[code], tb + dt.timedelta(seconds=BOOT_S))
        clock = p_ok + dt.timedelta(seconds=9)
        ev_old = [(p_lost, "TrafficVault", "COMMS_LOST")]
        ev_new = [(Y2K + dt.timedelta(seconds=3), "controller", "COLD_START"),
                  (Y2K + dt.timedelta(seconds=4), "controller", "DOOR_OPEN"),
                  (p_ok, "TrafficVault", "COMMS_OK"), (clock, "TrafficVault", "CLOCK_SET"),
                  (utc(leave), "controller", "DOOR_CLOSE")]
        out[code] = dict(new=new, day=day, arrive=arrive, leave=leave, unplug=tu, boot=tb, clock=clock,
                         lost=set(range(hour_index(tu), hour_index(clock) + 1)), ev_old=ev_old, ev_new=ev_new,
                         first_new=hour_index(clock) + 1)
    return out


def _quarter_hours(rng, lo, hi):
    return float(np.round(rng.uniform(lo, hi) * 4) / 4)


def maintenance(W, outs, sw, polls, rng):
    """the contractor's work, each item an order with its labour lines, the technicians' time on site, the controller
    resets and the communications fault it answered"""
    st = W["st"]
    sx = {x["code"]: x for x in st}
    wdays = [d for d in W["C"]["days"] if d.weekday() < 5 and d not in P.HOLIDAYS]
    work = []
    oid = [24100]

    def next_id():
        oid[0] += int(rng.integers(1, 6))
        return "WO-%d" % oid[0]

    def free(code, day, span=1):
        x = sx[code]
        if abs((x["vday"] - day).days) <= span:
            return False
        if code in P.RENUMBERED and abs((P.RENUMBERED[code][1] - day).days) <= span:
            return False
        if any(code in o["stations"] and abs((o["start"].date() - day).days) <= span for o in outs):
            return False
        return not any(code in w["stations"] and abs((w["opened"] - day).days) <= span and w["category"] == "Fault"
                       for w in work)

    def tech():
        return TECHS[int(rng.integers(len(TECHS)))]

    # routine inspections: spring (April and May) and autumn (October and November), district routes of up to four
    for season, months in (("spring", (4, 5)), ("autumn", (10, 11))):
        for dist in P.DISTRICTS:
            members = [x["code"] for x in st if x["district"] == dist]
            order = list(rng.permutation(members))
            routes = [order[i:i + 4] for i in range(0, len(order), 4)]
            cand = [d for d in wdays if d.month in months]
            for n, r in enumerate(routes, 1):
                for _ in range(200):
                    day = cand[int(rng.integers(len(cand)))]
                    if all(free(c, day, 0) for c in r) and not any(
                            set(r) & set(w["stations"]) and w["opened"] == day for w in work):
                        break
                t = dt.datetime.combine(day, dt.time(7, 45)) + dt.timedelta(minutes=int(rng.integers(0, 30)))
                onsite = []
                for c in r:
                    t += dt.timedelta(minutes=int(rng.integers(15, 45)))
                    stay = dt.timedelta(minutes=int(rng.integers(45, 85)))
                    onsite.append((c, t, t + stay))
                    t += stay
                hours = _quarter_hours(rng, 6.75, 8.0)
                labour = [(day, tech(), hours)]
                if rng.random() < 0.3:
                    labour.append((day, tech(), hours))
                work.append(dict(order=next_id(), category="Inspection", stations=list(r), opened=day, closed=day,
                                 description="%s inspection, %s route %d" % (season.capitalize(), dist, n),
                                 resolution="Inspected; loops tested, cabinet cleaned", labour=_uniq(labour),
                                 onsite=onsite, resets=[], comms=None))
    # faults: communications, cabinet, surge, heater; some communications faults at TCX-4 cleared from the office
    for _ in range(46):
        x = st[int(rng.integers(len(st)))]
        day = wdays[int(rng.integers(len(wdays)))]
        if not free(x["code"], day, 2):
            continue
        ctl = controller(x, day)
        kind = str(rng.choice(["comms", "comms", "comms", "cabinet", "surge", "heater"]))
        remote = ctl == "TCX-4" and kind == "comms" and rng.random() < 0.75
        work.append(_fault(x, day, kind, remote, ctl, rng, next_id, tech, wdays, free))
    # every district and quarter has at least one communications fault cleared from the office
    for dist in P.DISTRICTS:
        for qtr in (1, 2, 3, 4):
            have = sum(1 for w in work if w["resets"] and w["resets"][0][2] == "REMOTE" and
                       sx[w["stations"][0]]["district"] == dist and quarter(w["labour"][0][0]) == qtr)
            for _ in range(2000 if have < 2 else 0):
                if have >= 2:
                    break
                x = st[int(rng.integers(len(st)))]
                day = wdays[int(rng.integers(len(wdays)))]
                if x["district"] == dist and quarter(day) == qtr and controller(x, day) == "TCX-4" and \
                        free(x["code"], day, 2):
                    work.append(_fault(x, day, "comms", True, "TCX-4", rng, next_id, tech, wdays, free))
                    have += 1
    # the two old TCX-2 controllers that were replaced kept losing their communications before the replacement
    for code, (new, swap) in sorted(P.RENUMBERED.items()):
        x = sx[code]
        n = int(rng.integers(2, 4))
        for _ in range(500):
            if n == 0:
                break
            day = wdays[int(rng.integers(len(wdays)))]
            if day < swap - dt.timedelta(days=10) and free(code, day, 3):
                work.append(_fault(x, day, "comms", False, "TCX-2", rng, next_id, tech, wdays, free))
                n -= 1
    # a surge call-out on the evening of 30 June at a TCX-4 station
    for _ in range(500):
        x = st[int(rng.integers(len(st)))]
        day = dt.date(P.YEAR, 6, 30)
        if controller(x, day) == "TCX-4" and free(x["code"], day, 2):
            arrive = dt.datetime.combine(day, dt.time(20, 15)) + dt.timedelta(minutes=int(rng.integers(0, 40)))
            leave = arrive + dt.timedelta(minutes=int(rng.integers(55, 100)))
            work.append(dict(order=next_id(), category="Fault", stations=[x["code"]], opened=day, closed=day,
                             description="Surge damage after storm, detector cards", resolution="Detector card replaced",
                             labour=[(day, tech(), _quarter_hours(rng, 2.0, 3.0))], onsite=[(x["code"], arrive, leave)],
                             resets=[], comms=None))
            break
    # a battery replacement after each outage that ran a TCX-4 battery out
    for o in outs:
        for c in o["stations"]:
            if controller(sx[c], o["start"].date()) == "TCX-4" and \
                    (o["end"] - o["start"]).total_seconds() > BATTERY_H * 3600:
                day = o["end"].date() + dt.timedelta(days=int(rng.integers(1, 4)))
                while day.weekday() >= 5 or day in P.HOLIDAYS:
                    day += dt.timedelta(days=1)
                arrive = dt.datetime.combine(day, dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 300)))
                work.append(dict(order=next_id(), category="Fault", stations=[c], opened=o["end"].date(), closed=day,
                                 description="Controller restarted cold after power failure",
                                 resolution="Battery replaced", labour=[(day, tech(), _quarter_hours(rng, 1.0, 1.75))],
                                 onsite=[(c, arrive, arrive + dt.timedelta(minutes=int(rng.integers(35, 70))))],
                                 resets=[], comms=None))
    # the two controller replacements
    for code, s in sorted(sw.items()):
        t1, t2 = tech(), tech()
        while t2 == t1:
            t2 = tech()
        h = _quarter_hours(rng, 4.5, 6.0)
        work.append(dict(order=next_id(), category="Upgrade", stations=[code], opened=s["day"], closed=s["day"],
                         description="Replace TCX-2 controller with TCX-4",
                         resolution="Controller replaced; station renumbered %s" % s["new"],
                         labour=[(s["day"], t1, h), (s["day"], t2, h)], onsite=[(code, s["arrive"], s["leave"])],
                         resets=[], comms=None))
    return sorted(work, key=lambda w: (w["opened"], w["order"]))


def _uniq(labour):
    seen, out = set(), []
    for d, t, h in labour:
        if (d, t) not in seen:
            seen.add((d, t))
            out.append((d, t, h))
    return out


def _fault(x, day, kind, remote, ctl, rng, next_id, tech, wdays, free):
    code = x["code"]
    tk = tech()
    if kind == "comms":
        back = int(rng.integers(0, 3))
        fault = dt.datetime.combine(day - dt.timedelta(days=back), dt.time(0, 0)) + \
            dt.timedelta(minutes=int(rng.integers(0, 24 * 60 if back else 7 * 60)))
        desc = "No data from controller since %s" % fault.strftime("%H:%M")
        if remote:
            at = dt.datetime.combine(day, dt.time(8, 10)) + dt.timedelta(minutes=int(rng.integers(0, 470)))
            at = max(at, fault + dt.timedelta(minutes=50))
            return dict(order=next_id(), category="Fault", stations=[code], opened=fault.date(), closed=day,
                        description=desc, resolution="Controller reset, data recovered",
                        labour=[(day, tk, _quarter_hours(rng, 0.25, 0.75))], onsite=[],
                        resets=[(code, at, "REMOTE")], comms=(code, fault, at))
        arrive = dt.datetime.combine(day, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 390)))
        arrive = max(arrive, fault + dt.timedelta(minutes=90))
        reset = arrive + dt.timedelta(minutes=int(rng.integers(6, 22)))
        leave = reset + dt.timedelta(minutes=int(rng.integers(15, 60)))
        labour = [(day, tk, _quarter_hours(rng, 0.5, 3.5))]
        if rng.random() < 0.25:
            labour.append((day, tech(), _quarter_hours(rng, 0.5, 3.5)))
        return dict(order=next_id(), category="Fault", stations=[code], opened=fault.date(), closed=day,
                    description=desc, resolution="Controller reset, data recovered", labour=_uniq(labour),
                    onsite=[(code, arrive, leave)], resets=[(code, reset, "KEYPAD")] if ctl == "TCX-4" else [],
                    comms=(code, fault, reset))
    desc, res = dict(cabinet=("Cabinet door or lock damaged", "Lock replaced, door realigned"),
                     surge=("Surge damage after storm", "Detector card and surge protector replaced"),
                     heater=("Cabinet heater not working", "Heater thermostat replaced"))[kind]
    arrive = dt.datetime.combine(day, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 390)))
    leave = arrive + dt.timedelta(minutes=int(rng.integers(30, 150)))
    labour = [(day, tk, _quarter_hours(rng, 1.0, 4.5))]
    onsite = [(code, arrive, leave)]
    if rng.random() < 0.25:
        labour.append((day, tech(), _quarter_hours(rng, 1.0, 4.5)))
    closed = day
    if kind in ("surge", "cabinet") and rng.random() < 0.5:
        d2 = day + dt.timedelta(days=int(rng.integers(1, 9)))
        while d2.weekday() >= 5 or d2 in P.HOLIDAYS:
            d2 += dt.timedelta(days=1)
        if d2.year == P.YEAR and d2 < dt.date(P.YEAR, 12, 31) and free(code, d2, 1):
            a2 = dt.datetime.combine(d2, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 300)))
            labour.append((d2, tk, _quarter_hours(rng, 1.5, 5.0)))
            onsite.append((code, a2, a2 + dt.timedelta(minutes=int(rng.integers(40, 160)))))
            closed = d2
    return dict(order=next_id(), category="Fault", stations=[code], opened=day, closed=closed, description=desc,
                resolution=res, labour=_uniq(labour), onsite=onsite, resets=[], comms=None)


def crew(W, rng):
    """the validation crew at each cabinet: the night before its filmed day to connect the pulse recorder, the night
    after to remove it"""
    out = []
    for x in W["st"]:
        v = x["vday"]
        a = dt.datetime.combine(v - dt.timedelta(days=1), dt.time(21, 30)) + \
            dt.timedelta(minutes=int(rng.integers(0, 110)))
        b = dt.datetime.combine(v + dt.timedelta(days=1), dt.time(0, 10)) + \
            dt.timedelta(minutes=int(rng.integers(0, 90)))
        out.append((x["code"], a, a + dt.timedelta(minutes=int(rng.integers(8, 21)))))
        out.append((x["code"], b, b + dt.timedelta(minutes=int(rng.integers(6, 16)))))
    return out


def region_checks(W, outs, work, rng):
    """the Traffic Data Program's technologist checking loops at TCX-4 cabinets, at least once in every district and
    quarter; no work order, the cabinet door the only trace"""
    st = W["st"]
    wdays = [d for d in W["C"]["days"] if d.weekday() < 5 and d not in P.HOLIDAYS]
    taken = {(c, a.date()) for w in work for c, a, b in w["onsite"]} | \
        {(c, at.date()) for w in work for c, at, how in w["resets"]}
    out = []
    for dist in P.DISTRICTS:
        for qtr in (1, 2, 3, 4):
            n = int(rng.integers(1, 3))
            for _ in range(3000):
                if n == 0:
                    break
                x = st[int(rng.integers(len(st)))]
                day = wdays[int(rng.integers(len(wdays)))]
                if x["district"] != dist or quarter(day) != qtr or controller(x, day) != "TCX-4":
                    continue
                if any(abs((d - day).days) <= 2 for c, d in taken if c == x["code"]) or \
                        abs((x["vday"] - day).days) <= 2 or \
                        any(x["code"] in o["stations"] and abs((o["start"].date() - day).days) <= 1 for o in outs) or \
                        (x["code"] in P.RENUMBERED and abs((P.RENUMBERED[x["code"]][1] - day).days) <= 2):
                    continue
                a = dt.datetime.combine(day, dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 390)))
                out.append((x["code"], a, a + dt.timedelta(minutes=int(rng.integers(20, 75)))))
                taken.add((x["code"], day))
                n -= 1
    return out


def visits_truth(W, work):
    """the maintenance visits: each station and local day a technician was there (two technicians are one visit)"""
    sx = {x["code"]: x for x in W["st"]}
    seen = {(c, a.date()) for w in work for c, a, b in w["onsite"]}
    out = {}
    for code, day in seen:
        k = (sx[code]["district"], quarter(day))
        out[k] = out.get(k, 0) + 1
    return out


def failures_truth(W, outs):
    """the power failures: each station each outage hit, in the district and local quarter it began"""
    sx = {x["code"]: x for x in W["st"]}
    out = {}
    for o in outs:
        for code in o["stations"]:
            k = (sx[code]["district"], quarter(o["start"].date()))
            out[k] = out.get(k, 0) + len(o["parts"])
    return out


def ops(W):
    """the operations of the year, from the world's seed"""
    rng = np.random.default_rng(W["seed"] + 500)
    polls = poll_offsets(W)
    outs = outages(W, rng)
    pw = power(W, outs, polls)
    sw = swaps(W, polls, rng)
    work = maintenance(W, outs, sw, polls, rng)
    cr = crew(W, rng)
    rc = region_checks(W, outs, work, rng)
    lost = {}
    for r in pw:
        lost.setdefault(r["code"], set()).update(r["lost"])
    for code, s in sw.items():
        lost.setdefault(code, set()).update(s["lost"])
    return dict(outs=outs, power=pw, swaps=sw, work=work, crew=cr, region=rc, polls=polls, lost=lost)
