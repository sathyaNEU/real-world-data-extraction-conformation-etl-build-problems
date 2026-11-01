"""task157 architecture 3: the operating records cut from the simulated autumn, in the form each producing system
writes them. The AVL archive (national stop codes, UTC, registrations, duplicate and dropped messages, a GPS outage),
the timetable export (TransXChange), the depot's duty schedule (operator stop codes), the control room's log, the
depot's daily returns, the route 41 ticket machine extract, the fleet register, the authority's published monthly
punctuality and the lookups."""
from __future__ import annotations

import math
from collections import defaultdict
from datetime import date, datetime, timedelta

import numpy as np

import network as N
import params as P
import simulate as SIM

OPER_CODE = {"MRI-B": "MRB", "MRI-C": "MRC", "MRI-D": "MRD", "MRI-F": "MRF", "MRI-K": "MRK", "GBS-3": "GB3",
             "GBS-5": "GB5", "GBS-7": "GB7", "GBS-9": "GB9", "RBS": "RVB", "DEPOT": "SMD"}
DEAD_RUN = {"41": 7, "6": 16, "12": 18, "14": 19, "19": 21, "22": 24, "27": 23, "33": 25, "58": 24}


def hhmm(m):
    m = int(round(m)) % (24 * 60)
    return "%02d:%02d" % (m // 60, m % 60)


def hhmmss(sec):
    sec = int(sec)
    return "%02d:%02d:%02d" % (sec // 3600, (sec % 3600) // 60, sec % 60)


def local_to_utc(d, minutes):
    t = datetime(d.year, d.month, d.day) + timedelta(minutes=minutes)
    if P.bst(d):
        t -= timedelta(hours=1)
    return t


def atco(route, tp, direction):
    return P.TP_ATCO[(route, tp, direction)]


# ------------------------------------------------------------------ the AVL archive
def avl(recs, seed=P.SEED, protect=()):
    """One row per AVL departure or arrival event. Returns (header, rows, parsed) where parsed is the record list
    a solver rebuilds from the file (integer seconds, dropped events None, duplicates collapsed)."""
    rng = np.random.RandomState(seed + 21)
    fl = {v["reg"]: v for v in SIM.FLEET}
    # the vehicle days on which the AVL unit stopped reporting part way through
    vdays = sorted({(x["date"], x["vehicle"]) for x in recs if (x["date"], x["board"]) not in protect})
    faulty = {}
    for k in rng.choice(len(vdays), size=26, replace=False):
        faulty[vdays[k]] = rng.uniform(9 * 60, 19 * 60)
    outage = (date(2026, 11, 17), 10 * 60 + 40, 12 * 60 + 55)
    rows = []
    parsed = []
    for x in sorted(recs, key=lambda x: (x["date"], x["vehicle"], x["sched"][0])):
        d = x["date"]
        reg = x["vehicle"].replace(" ", "")
        act_sec = []
        for i, a in enumerate(x["actual"]):
            if a is None:
                act_sec.append(None)
                continue
            drop = rng.random_sample() < 0.011
            f = faulty.get((d, x["vehicle"]))
            if f is not None and a >= f:
                drop = True
            if d == outage[0] and outage[1] <= a < outage[2]:
                drop = True
            if drop:
                act_sec.append(None)
                continue
            act_sec.append(int(round(a * 60)))
        n = len(x["tps"])
        last_idx = n - 1
        if x.get("lost") is not None and x["lost"][0] == "part":
            last_idx = x["lost"][2] - 1
        for i in range(n):
            if act_sec[i] is None:
                continue
            ev = "ARR" if i == last_idx else "DEP"
            sched_sec = int(round(x["sched"][i] * 60))
            t = local_to_utc(d, act_sec[i] / 60.0)
            row = (d.isoformat(), x["route"], x["code"], "outbound" if x["dir"] == "O" else "inbound", reg,
                   atco(x["route"], x["tps"][i], x["dir"]), i + 1, ev, hhmmss(sched_sec), t.strftime("%Y-%m-%dT%H:%M:%SZ"))
            rows.append(row)
            if rng.random_sample() < 0.0026:
                rows.append(row)          # the feed re-sent the message
        y = dict(x)
        y["actual"] = [None if s is None else s / 60.0 for s in act_sec]
        y["sched"] = [int(round(s * 60)) / 60.0 for s in x["sched"]]
        y["last_idx"] = last_idx
        parsed.append(y)
    # the archive is written in the order the messages were received: by vehicle, a few out of order
    for k in range(len(rows) - 1):
        if rng.random_sample() < 0.004:
            rows[k], rows[k + 1] = rows[k + 1], rows[k]
    header = ("operating_day", "line_ref", "journey_ref", "direction_ref", "vehicle_ref", "stop_ref", "stop_seq",
              "event_type", "aimed_time", "recorded_at_utc")
    return header, rows, parsed


# ------------------------------------------------------------------ the TransXChange timetable export
def txc(S):
    """A TransXChange 2.4 document for the Lot 2 services: stops, route links with distances, journey patterns
    (one per running-time profile), operating profiles and every vehicle journey with its block number."""
    from xml.sax.saxutils import escape
    L = []
    w = L.append
    w('<?xml version="1.0" encoding="UTF-8"?>')
    w('<TransXChange xmlns="http://www.transxchange.org.uk/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
      'CreationDateTime="2026-08-14T10:22:31" ModificationDateTime="2026-08-21T15:07:44" Modification="revise" '
      'RevisionNumber="4" FileName="GCR_L2_WINTER26_r4.xml" SchemaVersion="2.4" xml:lang="en">')
    w('  <ServicedOrganisations>')
    w('    <ServicedOrganisation>')
    w('      <OrganisationCode>GCC_SCH</OrganisationCode>')
    w('      <Name>Grainford City Council maintained schools</Name>')
    w('      <WorkingDays>')
    for a, b in P.TERMS:
        w('        <DateRange><StartDate>%s</StartDate><EndDate>%s</EndDate></DateRange>' % (a.isoformat(), b.isoformat()))
    w('      </WorkingDays>')
    w('    </ServicedOrganisation>')
    w('  </ServicedOrganisations>')
    w('  <StopPoints>')
    seen = set()
    for r in P.ROUTE_ORDER:
        for d in ("O", "I"):
            for key, name in P.ROUTES[r]["tps"]:
                code = atco(r, key, d)
                if code in seen:
                    continue
                seen.add(code)
                w('    <AnnotatedStopPointRef><StopPointRef>%s</StopPointRef><CommonName>%s</CommonName>'
                  '<LocalityName>Grainford</LocalityName></AnnotatedStopPointRef>' % (code, escape(name)))
    w('  </StopPoints>')
    w('  <RouteSections>')
    for r in P.ROUTE_ORDER:
        R = P.ROUTES[r]
        keys = [k for k, _ in R["tps"]]
        for d in ("O", "I"):
            seq = keys if d == "O" else keys[::-1]
            kms = R["km"] if d == "O" else R["km_in"][::-1]
            w('    <RouteSection id="RS_%s_%s">' % (r, d))
            for i in range(len(seq) - 1):
                w('      <RouteLink id="RL_%s_%s_%d"><From><StopPointRef>%s</StopPointRef></From><To><StopPointRef>%s'
                  '</StopPointRef></To><Distance>%d</Distance></RouteLink>' % (
                      r, d, i + 1, atco(r, seq[i], d), atco(r, seq[i + 1], d), int(round(kms[i] * 1000))))
            w('    </RouteSection>')
    w('  </RouteSections>')
    w('  <Routes>')
    for r in P.ROUTE_ORDER:
        for d in ("O", "I"):
            w('    <Route id="R_%s_%s"><PrivateCode>%s %s</PrivateCode><Description>%s</Description>'
              '<RouteSectionRef>RS_%s_%s</RouteSectionRef></Route>' % (
                  r, d, r, "out" if d == "O" else "in", escape(P.ROUTES[r]["name"]), r, d))
    w('  </Routes>')
    # journey patterns: one per (route, direction, running-time profile)
    jp = {}
    for dt in ("MF", "SA", "SU"):
        for r in P.ROUTE_ORDER:
            for j in S[dt]["journeys"][r]:
                prof = tuple(int(round(b - a)) for a, b in zip(j["times"], j["times"][1:]))
                jp.setdefault((r, j["dir"], prof), "JP_%s_%s_%d" % (r, j["dir"], 1 + sum(1 for k in jp if k[:2] == (r, j["dir"]))))
    w('  <JourneyPatternSections>')
    for (r, d, prof), name in sorted(jp.items(), key=lambda kv: kv[1]):
        R = P.ROUTES[r]
        keys = [k for k, _ in R["tps"]]
        seq = keys if d == "O" else keys[::-1]
        w('    <JourneyPatternSection id="JPS%s">' % name[2:])
        for i in range(len(seq) - 1):
            w('      <JourneyPatternTimingLink id="JPTL%s_%d"><From SequenceNumber="%d"><StopPointRef>%s</StopPointRef>'
              '<TimingStatus>principalTimingPoint</TimingStatus></From><To SequenceNumber="%d"><StopPointRef>%s'
              '</StopPointRef><TimingStatus>principalTimingPoint</TimingStatus></To><RouteLinkRef>RL_%s_%s_%d'
              '</RouteLinkRef><RunTime>PT%dM</RunTime></JourneyPatternTimingLink>' % (
                  name[2:], i + 1, i + 1, atco(r, seq[i], d), i + 2, atco(r, seq[i + 1], d), r, d, i + 1, prof[i]))
        w('    </JourneyPatternSection>')
    w('  </JourneyPatternSections>')
    w('  <Operators>')
    w('    <Operator id="OP1"><NationalOperatorCode>PBGF</NationalOperatorCode><OperatorCode>PB</OperatorCode>'
      '<OperatorShortName>Pellbridge Buses</OperatorShortName><LicenceNumber>PB2041377</LicenceNumber>'
      '<Garages><Garage><GarageCode>SMD</GarageCode><GarageName>Saltmeadow</GarageName></Garage></Garages></Operator>')
    w('  </Operators>')
    w('  <Services>')
    for r in P.ROUTE_ORDER:
        R = P.ROUTES[r]
        w('    <Service>')
        w('      <ServiceCode>GCR_L2_%s</ServiceCode>' % r)
        w('      <Lines><Line id="L%s"><LineName>%s</LineName></Line></Lines>' % (r, r))
        w('      <OperatingPeriod><StartDate>%s</StartDate><EndDate>%s</EndDate></OperatingPeriod>' % (
            P.TT_START.isoformat(), P.TT_END.isoformat()))
        w('      <RegisteredOperatorRef>OP1</RegisteredOperatorRef>')
        a, b = R["name"].split(" - ")[0], R["name"].split(" - ")[-1]
        w('      <StandardService><Origin>%s</Origin><Destination>%s</Destination>' % (escape(a), escape(b)))
        for (rr, d, prof), name in sorted(jp.items(), key=lambda kv: kv[1]):
            if rr != r:
                continue
            w('        <JourneyPattern id="%s"><Direction>%s</Direction><RouteRef>R_%s_%s</RouteRef>'
              '<JourneyPatternSectionRefs>JPS%s</JourneyPatternSectionRefs></JourneyPattern>' % (
                  name, "outbound" if d == "O" else "inbound", r, d, name[2:]))
        w('      </StandardService>')
        w('    </Service>')
    w('  </Services>')
    w('  <VehicleJourneys>')
    days_xml = {"MF": "<MondayToFriday/>", "SA": "<Saturday/>", "SU": "<Sunday/>"}
    for dt in ("MF", "SA", "SU"):
        for b in S[dt]["boards"]:
            for j in b["journeys"]:
                prof = tuple(int(round(y - x)) for x, y in zip(j["times"], j["times"][1:]))
                name = jp[(j["route"], j["dir"], prof)]
                if j["school"]:
                    op = ('<OperatingProfile><RegularDayType><DaysOfWeek><MondayToFriday/></DaysOfWeek></RegularDayType>'
                          '<ServicedOrganisationDayType><DaysOfOperation><WorkingDays><ServicedOrganisationRef>GCC_SCH'
                          '</ServicedOrganisationRef></WorkingDays></DaysOfOperation></ServicedOrganisationDayType>'
                          '<BankHolidayOperation><DaysOfNonOperation><AllBankHolidays/></DaysOfNonOperation>'
                          '</BankHolidayOperation></OperatingProfile>')
                elif dt == "SU":
                    op = ('<OperatingProfile><RegularDayType><DaysOfWeek><Sunday/></DaysOfWeek></RegularDayType>'
                          '<BankHolidayOperation><DaysOfOperation><AllBankHolidays/></DaysOfOperation>'
                          '</BankHolidayOperation></OperatingProfile>')
                else:
                    op = ('<OperatingProfile><RegularDayType><DaysOfWeek>%s</DaysOfWeek></RegularDayType>'
                          '<BankHolidayOperation><DaysOfNonOperation><AllBankHolidays/></DaysOfNonOperation>'
                          '</BankHolidayOperation></OperatingProfile>' % days_xml[dt])
                w('    <VehicleJourney><PrivateCode>%s</PrivateCode><Operational><Block><BlockNumber>%s</BlockNumber>'
                  '</Block></Operational>%s<VehicleJourneyCode>%s</VehicleJourneyCode><ServiceRef>GCR_L2_%s</ServiceRef>'
                  '<LineRef>L%s</LineRef><JourneyPatternRef>%s</JourneyPatternRef><DepartureTime>%s:00</DepartureTime>'
                  '</VehicleJourney>' % (j["code"], b["board"].replace("/", ""), op, j["code"], j["route"], j["route"],
                                          name, hhmm(j["dep"])))
    w('  </VehicleJourneys>')
    w('</TransXChange>')
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ the duty schedule
def duty_numbers(S):
    """Duty numbers as the depot prints them, per day type, in order of sign-on."""
    out = {}
    base = {"MF": 201, "SA": 501, "SU": 701}
    for dt in ("MF", "SA", "SU"):
        s = S[dt]
        order = sorted(range(len(s["duties"])), key=lambda i: s["pieces"][s["duties"][i][0]]["on"])
        for n, i in enumerate(order):
            out[(dt, i)] = base[dt] + n
    return out


def duty_rows(S):
    nums = duty_numbers(S)
    duties, pieces = [], []
    names = {"MF": "Mon-Fri", "SA": "Sat", "SU": "Sun"}
    for dt in ("MF", "SA", "SU"):
        s = S[dt]
        for i, duty in enumerate(s["duties"]):
            ps = [s["pieces"][p] for p in duty]
            num = nums[(dt, i)]
            first, last = ps[0], ps[-1]
            on = first["on"] - (DEAD_RUN[first["route"]] + 12 if first["first"] else (14 if first["on_at"] == "RBS" else 32))
            off = last["off"] + (DEAD_RUN[last["route"]] + 6 if last["last"] else (10 if last["off_at"] == "RBS" else 28))
            plat = sum(p["off"] - p["on"] for p in ps)
            school = any(p.get("school") for p in ps)
            days = names[dt] + (" (school days)" if school else "")
            duties.append((num, days, hhmm(on), "SMD", hhmm(off), "SMD", _hm(off - on), _hm(plat), len(ps)))
            for k, p in enumerate(ps, 1):
                on_at = "SMD" if p["first"] else OPER_CODE.get(p["on_at"], p["on_at"])
                off_at = "SMD" if p["last"] else OPER_CODE.get(p["off_at"], p["off_at"])
                t_on = p["on"] - DEAD_RUN[p["route"]] if p["first"] else p["on"]
                t_off = p["off"] + DEAD_RUN[p["route"]] if p["last"] else p["off"]
                pieces.append((num, days, k, p["board"], p["route"], hhmm(t_on), on_at, hhmm(t_off), off_at))
    return duties, pieces


def _hm(m):
    m = int(round(m))
    return "%d:%02d" % (m // 60, m % 60)


# ------------------------------------------------------------------ the control room log and the depot's returns
REMARK_VD = ["air leak, bus to depot", "door fault, passengers transferred", "engine warning light", "kneeling fault",
             "coolant leak", "brake defect reported by driver", "wheelchair ramp failed", "power steering fault",
             "windscreen damage", "electrical fault, no ticket machine"]
REMARK_SI = ["driver taken ill", "driver unwell, relieved", "driver taken ill at stand", "driver assaulted, police called"]
REMARK_SS = ["no driver", "no driver available", "driver not booked on", "uncovered work"]
REMARK_TR = ["running late, turned short to restore service", "late running, turned at", "heavy traffic, short turned",
             "gap in service, turned short"]
REMARK_PC = ["road closed by police", "police closure", "road closed, turned short", "emergency services on scene"]


def logs(S, lost, meta, recs, seed=P.SEED):
    """The control room's log (journey entries and incidents) and the depot's daily returns (uncovered work)."""
    rng = np.random.RandomState(seed + 31)
    by_code = {}
    for dt in ("MF", "SA", "SU"):
        for b in S[dt]["boards"]:
            for j in b["journeys"]:
                by_code[(dt, j["code"])] = (b, j)
    veh = {(x["date"], x["code"]): x["vehicle"] for x in recs}
    fleet_no = {v["reg"]: v["fleet"] for v in SIM.FLEET}
    nums = duty_numbers(S)
    log = []
    ret = []
    ev, _ = SIM.incidents(None)
    # incidents
    for (ed, er, elinks, es, ee, add, why) in ev:
        log.append(dict(t=datetime(ed.year, ed.month, ed.day) + timedelta(minutes=es + int(rng.randint(2, 9))),
                        service=er, journey="", vehicle="", event="INCIDENT", lost_from="", lost_to="",
                        cause="PC" if ("police" in why or "RTC" in why or "collision" in why) else
                        ("RW" if ("water" in why or "gas" in why or "main" in why or "lights" in why) else
                         ("WX" if "flood" in why else "BD")),
                        remarks="%s, %s to %s, delays on route %s" % (why, hhmm(es), hhmm(ee), er),
                        rk=("INC", why, hhmm(es), hhmm(ee), er)))
    # journey entries
    uncovered_journeys = set()
    for d, m in meta.items():
        dt = P.day_type(d)
        s = S[dt]
        for (di, pn, pid, covered_from, late) in m["uncovered"]:
            p = s["pieces"][pid]
            js = p["journeys"]
            if late is not None:
                lost_js = [j for j in js if j["dep"] < late]
                if rng.random_sample() < 0.5:
                    log.append(dict(t=datetime(d.year, d.month, d.day) + timedelta(minutes=late - rng.uniform(8, 35)),
                                    service=p["route"], journey="", vehicle="", event="NOTE", lost_from="", lost_to="",
                                    cause="", remarks="spare driver on %s from %s" % (p["board"], hhmm(late)),
                                    rk=("SPARE", p["board"], hhmm(late))))
            else:
                lost_js = [j for j in js if covered_from is None or j["dep"] < covered_from]
            for j in lost_js:
                uncovered_journeys.add((d, j["code"]))
            ret.append(dict(date=d, duty=nums[(dt, di)], piece=pn, board=p["board"], service=p["route"],
                            status="PART COVERED" if covered_from is not None else "UNCOVERED",
                            covered_from=hhmm(covered_from) if covered_from is not None else "",
                            reason=str(rng.choice(["No driver", "Sickness", "No driver", "Late book-on", "No driver"]))))
    for x in lost:
        d = x["date"]
        dt = x["dt"]
        kind, cause, i0, i1 = x["lost"]
        tps = x["tps"]
        if cause == "SS" and (d, x["code"]) in uncovered_journeys:
            # the controller logs most, not all, of the journeys the uncovered work loses
            if rng.random_sample() < 0.42:
                continue
        t = datetime(d.year, d.month, d.day) + timedelta(minutes=x["sched"][max(i0 - 1, 0)] + rng.uniform(-6, 2))
        reg = veh.get((d, x["code"]), "")
        if kind == "whole":
            ev_t, lf, lt = "LOST", "", ""
        elif kind == "part":
            ev_t, lf, lt = "PART LOST", atco(x["route"], tps[i0 - 1], x["dir"]), atco(x["route"], tps[-1], x["dir"])
        else:
            ev_t, lf, lt = "PART LOST", atco(x["route"], tps[0], x["dir"]), atco(x["route"], tps[i1 + 1], x["dir"])
        rem = {"VD": REMARK_VD, "SI": REMARK_SI, "SS": REMARK_SS, "TR": REMARK_TR, "PC": REMARK_PC}[cause]
        remark = str(rng.choice(rem))
        rk = ("BASE", remark, fleet_no.get(reg, 0) if (cause == "VD" and reg) else None,
              x["board"] if cause == "SS" else None)
        if cause == "VD" and reg:
            remark = "bus %d %s" % (fleet_no.get(reg, 0), remark)
        if cause == "SS":
            remark = "%s for %s" % (remark, x["board"])
        if kind == "start":
            remark = "started from %s after turning short" % dict(P.ROUTES[x["route"]]["tps"])[tps[i1 + 1]]
            rk = ("START", dict(P.ROUTES[x["route"]]["tps"])[tps[i1 + 1]])
        log.append(dict(t=t, service=x["route"], journey=x["code"], vehicle=str(fleet_no.get(reg, "")) if reg else "",
                        event=ev_t, lost_from=lf, lost_to=lt, cause=cause, remarks=remark, rk=rk))
    # covered work and other notes the depot records
    for d in P.days(P.AVL_FIRST, P.AVL_LAST):
        dt = P.day_type(d)
        s = S[dt]
        for _ in range(int(rng.poisson({"MF": 2.2, "SA": 1.4, "SU": 0.8}[dt]))):
            di = int(rng.randint(len(s["duties"])))
            pn = int(rng.randint(1, len(s["duties"][di]) + 1))
            p = s["pieces"][s["duties"][di][pn - 1]]
            ret.append(dict(date=d, duty=nums[(dt, di)], piece=pn, board=p["board"], service=p["route"],
                            status=str(rng.choice(["COVERED SPARE", "COVERED O/T", "COVERED SPARE"])),
                            covered_from="", reason=str(rng.choice(["Sickness", "Annual leave", "Training",
                                                                     "Sickness", "Medical appointment"]))))
    # a few late-running notes with nothing lost (texture)
    for _ in range(140):
        x = recs[int(rng.randint(len(recs)))]
        lat = [a - s for a, s in zip(x["actual"], x["sched"]) if a is not None]
        if not lat or max(lat) < 9:
            continue
        d = x["date"]
        k = int(np.argmax([(-1e9 if a is None else a - s) for a, s in zip(x["actual"], x["sched"])]))
        log.append(dict(t=datetime(d.year, d.month, d.day) + timedelta(minutes=x["actual"][k]), service=x["route"],
                        journey=x["code"], vehicle=str(fleet_no.get(x["vehicle"], "")), event="LATE", lost_from="",
                        lost_to="", cause="", remarks="running %d late at %s" % (int(max(lat)),
                                                                                 dict(P.ROUTES[x["route"]]["tps"])[x["tps"][k]]),
                        rk=("LATE", int(max(lat)), dict(P.ROUTES[x["route"]]["tps"])[x["tps"][k]])))
    log.sort(key=lambda e: e["t"])
    _controller_hands(log, seed)
    ret.sort(key=lambda e: (e["date"], e["duty"], e["piece"]))
    return log, ret


# the control room's controllers each write the log in their own hand: one in full words, one in capitals and
# depot shorthand, one terse; drawn from a stream of its own so no record moves with the wording
_HAND = {
    "air leak, bus to depot": ("AIR LEAK - RTD", "air leak, to depot"),
    "door fault, passengers transferred": ("DOOR FAULT - PASSENGERS TRANSFERRED", "door fault, pass onto following"),
    "engine warning light": ("ENGINE WARNING LIGHT", "eng light on"),
    "kneeling fault": ("KNEELING FAULT", "kneel u/s"),
    "coolant leak": ("COOLANT LEAK", "coolant leak, recovered"),
    "brake defect reported by driver": ("BRAKE DEFECT - DRV REPORT", "brakes, drv report"),
    "wheelchair ramp failed": ("W/C RAMP FAILED", "ramp u/s"),
    "power steering fault": ("POWER STEERING", "p/steering fault"),
    "windscreen damage": ("WINDSCREEN DAMAGE", "screen cracked"),
    "electrical fault, no ticket machine": ("ELECTRICAL FAULT - NO ETM", "electrics, etm dead"),
    "driver taken ill": ("DRV TAKEN ILL", "drv ill"),
    "driver unwell, relieved": ("DRV UNWELL - RELIEVED", "drv unwell, relieved"),
    "driver taken ill at stand": ("DRV ILL AT STAND", "drv ill on stand"),
    "driver assaulted, police called": ("DRV ASSAULTED - POLICE CALLED", "assault on drv, police called"),
    "no driver": ("NO DRV", "no drv"),
    "no driver available": ("NO DRV AVAILABLE", "no drv avail"),
    "driver not booked on": ("DRV NOT BOOKED ON", "drv not booked on"),
    "uncovered work": ("UNCOVERED", "u/c"),
    "running late, turned short to restore service": ("LATE - T/S TO RESTORE SERVICE", "late, t/s to restore"),
    "late running, turned at": ("LATE RUNNING - T/S", "late running, t/s"),
    "heavy traffic, short turned": ("HEAVY TRAFFIC - T/S", "traffic, t/s"),
    "gap in service, turned short": ("GAP IN SERVICE - T/S", "t/s to fill gap"),
    "road closed by police": ("ROAD CLOSED BY POLICE", "police closed road"),
    "police closure": ("POLICE CLOSURE", "police closure"),
    "road closed, turned short": ("ROAD CLOSED - T/S", "road shut, t/s"),
    "emergency services on scene": ("EMERGENCY SERVICES ON SCENE", "ems on scene"),
}
_FULL = {"late running, turned at": "late running, turned short"}


def _abbr(name):
    for a, b in ((" Road", " Rd"), (" Street", " St"), (" Lane", " Ln"), ("Junction ", "Jct "),
                 (" Interchange", " Int"), (" Bus Station", " BS")):
        name = name.replace(a, b)
    return name


def _hand(rk, h):
    k = rk[0]
    if k == "INC":
        why, a, b, rte = rk[1:]
        return ("%s, %s to %s, delays on route %s" % (why, a, b, rte) if h == 0 else
                ("%s %s-%s, RTE %s DELAYED" % (why, a, b, rte)).upper() if h == 1 else
                "%s %s-%s, rte %s delayed" % (why, a, b, rte))
    if k == "SPARE":
        bd, t = rk[1:]
        return ("spare driver on %s from %s" % (bd, t) if h == 0 else "SPARE ON %s FROM %s" % (bd, t) if h == 1 else
                "spare drv %s @ %s" % (bd, t))
    if k == "LATE":
        m, stop = rk[1:]
        return ("running %d late at %s" % (m, stop) if h == 0 else "%d LATE AT %s" % (m, _abbr(stop).upper())
                if h == 1 else "+%d at %s" % (m, _abbr(stop)))
    if k == "START":
        stop = rk[1]
        return ("started from %s after turning short" % stop if h == 0 else
                "STARTED %s - T/S PREVIOUS TRIP" % _abbr(stop).upper() if h == 1 else
                "started %s, t/s prev trip" % _abbr(stop))
    text, fleet, board = rk[1:]
    body = _FULL.get(text, text) if h == 0 else _HAND[text][h - 1]
    if fleet is not None:
        body = ("bus %d %s" if h == 0 else "VEH %d %s" if h == 1 else "%d %s") % (fleet, body)
    if board is not None:
        body = ("%s for %s" if h == 0 else "%s - %s" if h == 1 else "%s %s") % (body, board)
    return body


def _controller_hands(log, seed):
    hrng = np.random.RandomState(seed + 4441)
    styles = (0, 1, 2, 0, 2)
    rota = {}
    for d in P.days(P.AVL_FIRST - timedelta(days=1), P.AVL_LAST + timedelta(days=1)):
        for shift in ("early", "late", "night"):
            rota[(d, shift)] = styles[int(hrng.randint(len(styles)))]
    for e in log:
        t = e["t"]
        shift = "early" if 5 <= t.hour < 14 else ("late" if 14 <= t.hour < 22 else "night")
        d = t.date() if t.hour >= 5 else t.date() - timedelta(days=1)
        e["remarks"] = _hand(e.pop("rk"), rota[(d, shift)])


# ------------------------------------------------------------------ the ticket machines on route 41
TICKETS = [("ENCTS", 0, 0.29), ("GCR WEEKLY", 0, 0.17), ("ADULT SINGLE", 270, 0.17), ("ADULT DAY", 480, 0.08),
           ("CHILD SINGLE", 130, 0.08), ("CONTACTLESS CAP", 270, 0.13), ("STUDENT WEEKLY", 0, 0.05),
           ("ADULT RETURN", 450, 0.03)]
# boardings per journey by fare stage (stage 1 the interchange ... 6 Ravensholme bus station), by direction and band
RATE = {("I", "AM peak"): [0, 1.6, 4.6, 3.4, 6.2, 8.8], ("I", "PM peak"): [0, 0.9, 1.9, 1.4, 2.4, 3.1],
        ("I", "Other times"): [0, 1.1, 2.3, 1.7, 2.9, 3.8],
        ("O", "AM peak"): [3.2, 1.3, 0.7, 0.5, 0.4, 0], ("O", "PM peak"): [11.4, 4.1, 1.9, 1.3, 0.8, 0],
        ("O", "Other times"): [5.6, 2.2, 1.2, 0.8, 0.6, 0]}
STAGE_TP = {1: "MRI-D", 2: "TNS", 3: "THR", 4: "TQY", 5: "RVR", 6: "RBS"}
ETM_SLOW = set()


def etm(S, recs, seed=P.SEED):
    """Ticket machine transactions on route 41, October and November 2026. A driver who forgets to select his next
    journey at a terminus keeps selling on the previous one. Returns (header, rows, truth) where truth carries every
    transaction's true direction."""
    rng = np.random.RandomState(seed + 41)
    fl = {v["reg"]: v for v in SIM.FLEET}
    nums = duty_numbers(S)
    # the duty driving each journey
    duty_of = {}
    for dt in ("MF", "SA", "SU"):
        s = S[dt]
        for i, duty in enumerate(s["duties"]):
            for pid in duty:
                for j in s["pieces"][pid]["journeys"]:
                    duty_of[(dt, j["code"])] = (nums[(dt, i)], pid)
    habit = {}
    for key in set(duty_of.values()):
        habit[key[0]] = 0.035 if rng.random_sample() < 0.7 else rng.uniform(0.16, 0.34)
    rows = []
    truth = []
    by_day = defaultdict(list)
    for x in recs:
        if x["route"] == "41" and P.ETM_FIRST <= x["date"] <= P.ETM_LAST:
            by_day[x["date"]].append(x)
    seq = defaultdict(int)
    resent = {date(2026, 10, 13), date(2026, 11, 3), date(2026, 11, 24)}
    # two machines on route 41's buses kept summer time after the clock change
    pool41 = sorted(v["etm"] for v in SIM.FLEET if v["route"] == "41")
    slow_clock = {pool41[2], pool41[7]}
    for d in sorted(by_day):
        dt = P.day_type(d)
        dayf = rng.uniform(0.86, 1.12) * ({"MF": 1.0, "SA": 0.82, "SU": 0.55}[dt])
        xs = sorted(by_day[d], key=lambda x: (x["board"], x["k"]))
        prev_sel = {}
        resend_unit = None
        for x in xs:
            dn, pid = duty_of[(dt, x["code"])]
            trip_no = x["k"] + 1
            piece_start = S[dt]["pieces"][pid]["journeys"][0]["code"] == x["code"]
            sel = (trip_no, x["dir"])
            if not piece_start and x["board"] in prev_sel and rng.random_sample() < habit[dn]:
                sel = prev_sel[x["board"]]                  # the journey was not changed at the terminus
            prev_sel[x["board"]] = sel if sel[0] == trip_no else (trip_no, x["dir"])
            v = fl[x["vehicle"]]
            unit = v["etm"]
            for st in range(1, 7):
                tp = STAGE_TP[st]
                if tp not in x["tps"]:
                    continue
                i = x["tps"].index(tp)
                if i == len(x["tps"]) - 1:
                    continue
                a = x["actual"][i]
                if a is None:
                    continue
                # a stage is served only if the journey reached it (part lost journeys stop short)
                bnd = P.band(dt, x["sched"][i])
                lam = RATE[(x["dir"], bnd)][st - 1] * dayf
                n = rng.poisson(lam)
                for _ in range(n):
                    if st in (1, 6) and i == 0:
                        tt = a - rng.uniform(0.05, 4.5)
                    else:
                        tt = a + rng.uniform(-1.3, 0.25)
                    name, fare, _w = TICKETS[int(rng.choice(len(TICKETS), p=[t[2] for t in TICKETS]))]
                    seq[(d, unit)] += 1
                    secs = int(round(tt * 60))
                    if dt == "MF" and secs % 60 == 0 and secs // 60 in (450, 570, 960, 1110):
                        secs += 1                       # the machine stamps the sale, not the band
                    tt = secs / 60.0
                    when = datetime(d.year, d.month, d.day) + timedelta(seconds=secs)
                    if unit in slow_clock and d >= P.CLOCK_CHANGE:
                        when += timedelta(hours=1)
                    row = [unit, "U%s%s" % (d.strftime("%y%m%d"), unit[-3:]), seq[(d, unit)], dn, x["board"], sel[0],
                           "OUT" if sel[1] == "O" else "IN", st, when.strftime("%Y-%m-%d %H:%M:%S"), name, fare]
                    rows.append(row)
                    rec_t = tt + (60 if (unit in slow_clock and d >= P.CLOCK_CHANGE) else 0)
                    truth.append(dict(date=d, dt=dt, stage=st, true_dir=x["dir"], sel_dir=sel[1], band=P.band(dt, tt),
                                      rec_band=P.band(dt, rec_t), code=x["code"], unit=unit, row=len(rows) - 1,
                                      key=(unit, str(seq[(d, unit)]), when.strftime("%Y-%m-%d %H:%M:%S")),
                                      slow=unit in slow_clock and d >= P.CLOCK_CHANGE))
    # three nights the depot's upload failed and the machines sent the day again
    extra = []
    for d in sorted(resent):
        units = sorted({r[0] for r in rows if r[8].startswith(d.isoformat())})
        u = units[int(rng.randint(len(units)))]
        for r in rows:
            if r[0] == u and r[8].startswith(d.isoformat()):
                rr = list(r)
                rr[1] = rr[1] + "R"
                extra.append(rr)
    rows = sorted(rows + extra, key=lambda r: (r[8][:10], r[0], r[1], r[2]))
    ETM_SLOW.clear()
    ETM_SLOW.update(slow_clock)
    header = ("etm_unit", "upload_id", "txn_seq", "waybill_duty", "running_board", "journey_no", "journey_direction",
              "fare_stage", "txn_time", "ticket_type", "fare_pence")
    return header, rows, truth


# ------------------------------------------------------------------ lookups
def fleet_rows():
    bodies = {"Double deck": ["Volvo B5LH / Wright Gemini 3", "ADL Enviro400 MMC", "Volvo B5TL / Wright Gemini 3"],
              "Single deck": ["ADL Enviro200 MMC", "Optare Solo SR", "Wright StreetLite DF"]}
    rng = np.random.RandomState(P.SEED + 51)
    out = []
    for v in SIM.FLEET:
        b = bodies[v["type"]][int(rng.randint(3))]
        seats = int(rng.choice([72, 73, 76])) if v["type"] == "Double deck" else int(rng.choice([38, 39, 41, 33]))
        alloc = "Spare" if v["route"] == "SPARE" else v["route"]
        out.append((v["fleet"], v["reg"], b, v["type"], seats, v["etm"], alloc, "%d-0%d" % (v["year"], 1 + int(rng.randint(8)))))
    return ("fleet_no", "registration", "chassis_body", "type", "seats", "etm_unit", "allocated_service",
            "first_registered"), out


def fare_stage_rows():
    out = []
    for st, name, stops in P.FARE_STAGES_41:
        for k, s in enumerate(stops, 1):
            out.append((41, st, name, k, s))
    return ("line_no", "fare_stage", "stage_name", "stop_order", "stop_name"), out


CAUSES = [("VD", "Vehicle defect"), ("SS", "Staff shortage"), ("SI", "Staff illness / incident"),
          ("TR", "Traffic / late running"), ("PC", "Police or emergency road closure"), ("RW", "Roadworks"),
          ("WX", "Severe weather"), ("BD", "Breakdown of other vehicle"), ("PX", "Passenger incident"),
          ("AV", "AVL / ticket machine fault")]


def cause_rows():
    return ("loss_code", "loss_reason", "code_list_issue"), [(c, d, "Issue 6, April 2025") for c, d in CAUSES]


# ------------------------------------------------------------------ the authority's published monthly punctuality
def published(parsed, seed=P.SEED):
    """Monthly punctuality by route as the authority publishes it: January 2025 to November 2026, computed on the
    AVL for the months the extract covers and taken from the authority's archive before. October 2026 appears as
    the provisional figure released in November and the final one released in December."""
    import analysis as A
    rng = np.random.RandomState(seed + 61)
    by_month = defaultdict(list)
    for x in parsed:
        by_month[(x["date"].year, x["date"].month)].append(x)
    rows = []
    live = {}
    for (y, m), xs in by_month.items():
        n, ok = defaultdict(int), defaultdict(int)
        for x in xs:
            for i in range(x["last_idx"]):
                a = x["actual"][i]
                if a is None:
                    continue
                n[x["route"]] += 1
                ok[x["route"]] += A.on_time(a - x["sched"][i])
        live[(y, m)] = (n, ok)
    autumn = A.punctuality(parsed)
    # the archive's levels: each route near its current level, a mild seasonal swing, the 2025 Marsh Lane
    # closure on route 14 (outbound, 3 March to 13 April 2025)
    season = {1: 0.4, 2: 0.6, 3: 0.2, 4: 0.1, 5: -0.1, 6: -0.3, 7: 0.3, 8: 0.5, 9: -0.3, 10: -0.5, 11: -0.6, 12: -0.2}
    vol = {r: sum(1 for x in parsed if x["route"] == r) for r in P.ROUTE_ORDER}
    months = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 12)]
    drift = {r: rng.normal(0, 0.5) for r in P.ROUTE_ORDER}
    for (y, m) in months:
        for r in P.ROUTE_ORDER:
            if (y, m) in live and (y, m) >= (2026, 9):
                n, ok = live[(y, m)]
                dep, on = n[r], ok[r]
            else:
                base = autumn[r] + drift[r] * (1.0 if y == 2025 else 0.5) + season[m] - np.mean([season[k] for k in (9, 10, 11)])
                if r == "14" and (y, m) in ((2025, 3), (2025, 4)):
                    base -= 13.9 if m == 3 else 6.1
                dep = int(vol[r] / 97 * 30.4 * 4.6 * rng.uniform(0.96, 1.04))
                pct = min(97.5, base + rng.normal(0, 0.55))
                on = int(round(dep * pct / 100))
            pub = date(y + (m == 12), (m % 12) + 1, 4 + int(rng.randint(0, 4)))
            status = "provisional" if (y, m) == (2026, 11) else "final"
            rows.append([r, "%d-%02d" % (y, m), dep, on, round(100.0 * on / dep, 1), status, pub.isoformat()])
            if (y, m) == (2026, 10):
                # the provisional October figure, released before the late AVL uploads were loaded
                dep_p = dep - int(dep * rng.uniform(0.004, 0.011))
                on_p = on - int((on * rng.uniform(0.004, 0.012)))
                rows.append([r, "%d-%02d" % (y, m), dep_p, on_p, round(100.0 * on_p / dep_p, 1), "provisional",
                             date(2026, 11, 5).isoformat()])
    rows.sort(key=lambda r: (int(r[0]), r[1], r[6]))
    header = ("line_no", "period_month", "departures_recorded", "departures_on_time", "punctuality_pct",
              "release_status", "release_date")
    return header, rows


# ------------------------------------------------------------------ distractors
def ring_road_counts(seed=P.SEED):
    """The council's automatic traffic counter on the Ring Road crossing: weekday mean flow by hour and month."""
    rng = np.random.RandomState(seed + 71)
    prof = [60, 38, 30, 34, 70, 260, 820, 1590, 1720, 1240, 1010, 980, 1020, 990, 1060, 1290, 1610, 1680, 1240, 860,
            640, 480, 330, 170]
    rows = []
    for m in range(1, 12):
        for dirn in ("Northbound", "Southbound"):
            f = rng.uniform(0.95, 1.05) * (1.04 if dirn == "Northbound" else 0.97)
            for h in range(24):
                v = prof[h] * f * (1.06 if dirn == "Northbound" and h in (7, 8) else 1.0) * \
                    (1.05 if dirn == "Southbound" and h in (16, 17) else 1.0) * rng.uniform(0.97, 1.03)
                rows.append(["ATC 0412 Ring Road crossing", "2026-%02d" % m, dirn, "%02d:00" % h, int(round(v)),
                             int(rng.randint(18, 23)), v])
    # the counter's own export also carries the seven-day mean and the heavy goods share (a stream of its own)
    xrng = np.random.RandomState(seed + 73)
    for r in rows:
        h = int(r[3][:2])
        wk = 0.62 if h in (7, 8, 16, 17) else (1.12 if h in (0, 1, 2, 3, 22, 23) else 0.84)
        v = r.pop()
        r.append(int(round(v * (5 + 2 * wk * xrng.uniform(0.95, 1.05)) / 7)))
        r.append(round((7.8 if 6 <= h <= 18 else 4.6) * xrng.uniform(0.8, 1.2), 1))
    return ("site", "count_month", "flow_direction", "hour_beginning", "mean_weekday_vehicles", "weekdays_counted",
            "mean_7day_vehicles", "hgv_pct"), rows


def street_works(seed=P.SEED):
    """Street works permits granted for January to March 2027 (none of them touches a Lot 2 timing point while
    buses run: off the network, footway only, or overnight)."""
    rng = np.random.RandomState(seed + 81)
    streets = [("Castle Mount", "footway only", "08:00-16:00"), ("Holm Lane", "overnight lane closure", "00:45-05:15"),
               ("Kirkgate Walk", "lane closure", "09:30-15:30"), ("Barley Street", "road closure", "09:00-15:00"),
               ("Cloth Hall Street", "footway only", "09:30-15:30"), ("Sheepcote Lane", "lane closure", "09:30-15:30"),
               ("Langstrow Road", "overnight road closure", "00:40-05:20"), ("Wrayford Avenue", "footway only",
                                                                            "09:00-15:00"),
               ("Mill Bank", "footway only", "09:30-15:00"), ("Tanyard Close", "road closure", "08:00-17:00"),
               ("Ashgarth Lane", "lane closure", "09:30-15:30"), ("Felbeck Green", "footway only", "09:00-15:30"),
               ("Dyer Street", "overnight lane closure", "00:50-05:10"), ("Coldharrow Road", "footway only",
                                                                         "09:30-15:30"),
               ("Saltmeadow Lane", "overnight lane closure", "00:45-05:00"), ("Oak Street", "footway only",
                                                                              "09:00-15:00"),
               ("Garrow Lane", "footway only", "09:30-15:30"), ("Hollins Way", "road closure", "09:00-16:00"),
               ("Morbeck Drive", "footway only", "09:00-15:00"), ("Tenter Street", "overnight lane closure",
                                                                  "00:40-05:10")]
    promoters = ["Northern Gas Networks", "Yorkshire Water", "Openreach", "Northern Powergrid", "Virgin Media O2",
                 "Grainford City Council Highways", "CityFibre"]
    rows = []
    for k in range(46):
        st, tm, hours = streets[int(rng.randint(len(streets)))]
        start = date(2027, 1, 4) + timedelta(days=int(rng.randint(0, 80)))
        end = start + timedelta(days=int(rng.randint(1, 12)))
        rows.append(["GCC-SW-27-%04d" % (1180 + k * 7 + int(rng.randint(0, 6))), promoters[int(rng.randint(len(promoters)))],
                     st, start.isoformat(), end.isoformat(), hours, tm,
                     str(rng.choice(["service connection", "carriageway reinstatement", "duct repair", "valve replacement",
                                     "pole replacement", "new supply", "leak repair", "chamber rebuild"]))])
    # the permit register's own fields: the street's USRN, the works category and where the permit stands
    # (a stream of its own, so the permits themselves do not move)
    prng = np.random.RandomState(seed + 83)
    usrn = {st: "%d" % (21400000 + 1731 * k + int(prng.randint(0, 900))) for k, (st, _, _) in enumerate(streets)}
    for r in rows:
        days = (date.fromisoformat(r[4]) - date.fromisoformat(r[3])).days
        cat = "Major" if days > 10 else ("Standard" if days > 3 else "Minor")
        status = str(prng.choice(["Granted", "Granted", "Granted", "Granted with conditions", "Granted",
                                  "Granted with conditions", "Cancelled by promoter"]))
        r.insert(3, usrn[r[2]])
        r.append(cat)
        r.append(status)
    rows.sort(key=lambda r: (r[4], r[0]))
    return ("permit_ref", "promoter", "street", "usrn", "start_date", "end_date", "working_hours", "traffic_management",
            "works_description", "works_category", "permit_status"), rows
