"""task157 architecture 3: the independent verifier. Reads only the files under target/ (every format: the AVL
CSV, the TransXChange XML, the duty schedule and returns workbooks, the PDFs, the logs and the ticket machine
extract), rebuilds every graded figure with its own code, and compares it with generator/figures.json.

    python3 verify.py [target_dir]
"""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
NS = {"t": "http://www.transxchange.org.uk/"}
ASSIGN = {}


def pdf(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True,
                                              text=True).stdout)


def find(target, pat):
    return os.path.join(target, next(f for f in sorted(os.listdir(target)) if re.search(pat, f)))


def hm(s):
    h, m = s.split(":")[:2]
    return int(h) * 60 + int(m)


def hms(s):
    h, m, x = s.split(":")
    return int(h) * 60 + int(m) + int(x) / 60.0


# ------------------------------------------------------------------ the documents
def rules(target):
    s7 = pdf(find(target, r"schedule7"))
    tmp = pdf(find(target, r"tmp"))
    early = 60 if "no more than one minute before" in s7 else None
    late = 5 * 60 + 59 if "five minutes fifty-nine seconds after" in s7 else None
    floor = float(re.search(r"Punctuality Floor is (\d+) per cent", s7).group(1))
    peaks = re.findall(r"(\d\d):(\d\d) to (\d\d):(\d\d)", tmp)[:2]
    pk = [(int(a) * 60 + int(b), int(c) * 60 + int(d)) for a, b, c, d in peaks]
    m = re.search(r"Additional running time.*?(\d+) minutes\s+(\d+) minutes\s+(\d+) minutes", tmp)
    assert m.group(1) == m.group(2), "the two peaks carry one figure"
    div_pk, div_off = int(m.group(1)), int(m.group(3))
    cor = int(re.search(r"about (\d+) minutes longer in the weekday peaks", tmp).group(1))
    unserved = re.search(r"stops at (.+?) are not served", tmp).group(1)
    unserved = [x.strip() for x in re.split(r",| and ", unserved) if x.strip()]
    return dict(early=early, late=late, floor=floor, peaks=pk, div_pk=div_pk, div_off=div_off, cor=cor,
                unserved=unserved)


# ------------------------------------------------------------------ the timetable
def timetable(target):
    from lxml import etree
    root = etree.parse(find(target, r"txc\.xml$")).getroot()
    names = {e.findtext("t:StopPointRef", namespaces=NS): e.findtext("t:CommonName", namespaces=NS)
             for e in root.iterfind(".//t:AnnotatedStopPointRef", NS)}
    dist = {}
    for rl in root.iterfind(".//t:RouteLink", NS):
        dist[rl.get("id")] = int(rl.findtext("t:Distance", namespaces=NS))
    jps = {}
    for s in root.iterfind(".//t:JourneyPatternSection", NS):
        links = []
        for ln in s.iterfind("t:JourneyPatternTimingLink", NS):
            a = ln.findtext("t:From/t:StopPointRef", namespaces=NS)
            b = ln.findtext("t:To/t:StopPointRef", namespaces=NS)
            rt = int(re.match(r"PT(\d+)M", ln.findtext("t:RunTime", namespaces=NS)).group(1))
            links.append((a, b, rt, dist[ln.findtext("t:RouteLinkRef", namespaces=NS)]))
        jps[s.get("id")] = links
    jp = {}
    for p in root.iterfind(".//t:JourneyPattern", NS):
        jp[p.get("id")] = (p.findtext("t:Direction", namespaces=NS), jps[p.findtext("t:JourneyPatternSectionRefs",
                                                                                   namespaces=NS)])
    terms = [(date.fromisoformat(r.findtext("t:StartDate", namespaces=NS)), date.fromisoformat(r.findtext("t:EndDate",
                                                                                                          namespaces=NS)))
             for r in root.iterfind(".//t:ServicedOrganisation/t:WorkingDays/t:DateRange", NS)]
    js = {}
    for v in root.iterfind(".//t:VehicleJourney", NS):
        code = v.findtext("t:VehicleJourneyCode", namespaces=NS)
        dirn, links = jp[v.findtext("t:JourneyPatternRef", namespaces=NS)]
        dep = hms(v.findtext("t:DepartureTime", namespaces=NS))
        stops = [links[0][0]] + [l[1] for l in links]
        times = [dep]
        for l in links:
            times.append(times[-1] + l[2])
        prof = v.find("t:OperatingProfile", NS)
        dow = prof.find("t:RegularDayType/t:DaysOfWeek", NS)
        day = etree.QName(dow[0]).localname
        school = prof.find("t:ServicedOrganisationDayType", NS) is not None
        js[code] = dict(code=code, service=v.findtext("t:LineRef", namespaces=NS)[1:], dir=dirn, stops=stops,
                        times=times, km=[l[3] / 1000.0 for l in links], block=v.findtext(".//t:BlockNumber", namespaces=NS),
                        day={"MondayToFriday": "MF", "Saturday": "SA", "Sunday": "SU"}[day], school=school)
    return js, names, terms


def day_type(d, bank):
    if d in bank or d.weekday() == 6:
        return "SU"
    return "SA" if d.weekday() == 5 else "MF"


# ------------------------------------------------------------------ the AVL
def avl(target, js):
    """Records keyed (day, journey): stop index -> (event, local minutes). Re-sent messages once."""
    seen = set()
    rec = defaultdict(dict)
    veh = {}
    with open(find(target, r"^avl_"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            k = (r["operating_day"], r["journey_ref"], r["stop_ref"], r["event_type"])
            if k in seen:
                continue
            seen.add(k)
            t = datetime.strptime(r["recorded_at_utc"], "%Y-%m-%dT%H:%M:%SZ")
            # British Summer Time ended at 01:00 UTC on 25 October 2026
            if t < datetime(2026, 10, 25, 1, 0, 0):
                t += timedelta(hours=1)
            d = date.fromisoformat(r["operating_day"])
            m = (t - datetime(d.year, d.month, d.day)).total_seconds() / 60.0
            j = js[r["journey_ref"]]
            i = int(r["stop_seq"]) - 1
            assert j["stops"][i] == r["stop_ref"]
            rec[(d, r["journey_ref"])][i] = (r["event_type"], m)
            veh[(d, r["journey_ref"])] = r["vehicle_ref"]
    return rec, veh


# ------------------------------------------------------------------ the duty schedule
def duties(target, js):
    from openpyxl import load_workbook
    wb = load_workbook(find(target, r"duty_schedule"), read_only=True)
    rows = []
    hdr = None
    for r in wb["Pieces"].iter_rows(values_only=True):
        if hdr is None:
            if r and r[0] == "Duty":
                hdr = r
            continue
        if r[0] is None:
            continue
        rows.append(r)
    blocks = defaultdict(list)
    for j in js.values():
        blocks[(j["day"], j["block"])].append(j)
    for k in blocks:
        blocks[k].sort(key=lambda j: j["times"][0])
    dmap = {"Mon-Fri": "MF", "Sat": "SA", "Sun": "SU"}
    pieces = defaultdict(list)
    for duty, days, k, board, svc, on, on_at, off, off_at in rows:
        dt = dmap[days.split(" ")[0]]
        blk = board.replace("/", "")
        b = blocks[(dt, blk)]
        t_on, t_off = hm(on), hm(off)
        if t_off < t_on:
            t_off += 1440
        inside = [j for j in b if j["times"][0] >= t_on - 0.01 and j["times"][-1] <= t_off + 0.01]
        pieces[(dt, duty)].append(dict(k=k, board=board, first=inside[0]["code"], last=inside[-1]["code"],
                                       on=t_on, off=t_off, on_at=on_at, off_at=off_at, journeys=[j["code"] for j in inside]))
    links = {}
    for (dt, duty), ps in pieces.items():
        ps.sort(key=lambda p: p["k"])
        for a, b in zip(ps, ps[1:]):
            links[b["first"]] = (a["last"], b["on"] - a["off"])
    return links, pieces


# ------------------------------------------------------------------ the main call
def punct(js, rec, R, closure=None):
    n, ok = Counter(), Counter()
    for (d, code), ev in rec.items():
        j = js[code]
        for i, (e, m) in ev.items():
            if e != "DEP":
                continue
            if closure is not None and code in closure["drop"] and i in closure["drop"][code]:
                continue
            add = closure["add"].get((d, code), [0] * len(j["stops"]))[i] if closure else 0.0
            late = int(round((m + add - j["times"][i]) * 60))
            n[j["service"]] += 1
            ok[j["service"]] += -R["early"] <= late <= R["late"]
    return {s: 100.0 * ok[s] / n[s] for s in n}


def replay(js, rec, links, R, names, bank):
    """Added minutes per journey and stop: route 41's diversion, the Ring Road crossing's peak delay, passed on to
    the bus's next journey beyond its recorded stand over one minute and to a relieved driver's next piece (joins
    under 30 minutes) beyond the recorded slack."""
    stop_of = {v: k for k, v in names.items()}
    inv = {nm: code for code, nm in names.items()}

    def peak(d, m):
        return d.weekday() < 5 and d not in bank and any(a <= m < b for a, b in R["peaks"])
    add = {}
    drop = defaultdict(set)
    by_day = defaultdict(list)
    for (d, code) in rec:
        by_day[d].append(code)
    for d, codes in sorted(by_day.items()):
        codes.sort(key=lambda c: (js[c]["times"][0], js[c]["block"]))
        added_arr, rec_arr, last_on_block = {}, {}, {}
        for c in codes:
            j = js[c]
            ev = rec[(d, c)]
            n = len(j["stops"])
            a = [0.0] * n
            nm = [names[s] for s in j["stops"]]
            if j["service"] == "41":
                start = "Tenter Street" if j["dir"] == "outbound" else "Ravensholme Road"
                k = nm.index(start)
                mins = R["div_pk"] if peak(d, j["times"][k]) else R["div_off"]
                for i in range(k + 1, n):
                    a[i] = mins
                for i, s in enumerate(nm):
                    if s in R["unserved"]:
                        drop[c].add(i)
            if j["service"] in ("6", "12"):
                acc = 0.0
                for i in range(1, n):
                    pair = {nm[i - 1], nm[i]}
                    if pair in ({"Ring Road, Junction 4", "Saltmeadow Lane"}, {"Ring Road, Junction 4", "Ring Road, Junction 5"}):
                        if peak(d, j["times"][i - 1]):
                            acc += R["cor"]
                    a[i] = acc
            # recorded departure (first event, carried to the first stop) and arrival (last event)
            idx = sorted(ev)
            fi = idx[0]
            dep = ev[fi][1] - (j["times"][fi] - j["times"][0])
            arr_i = max(i for i in idx if ev[i][0] == "ARR") if any(ev[i][0] == "ARR" for i in idx) else idx[-1]
            last_i = arr_i
            arr = ev[last_i][1]
            delta = 0.0
            blk = (j["day"], j["block"])
            if blk in last_on_block:
                p = last_on_block[blk]
                if rec_arr.get(p) is not None:
                    delta = max(delta, added_arr[p] - max(0.0, dep - rec_arr[p] - 1.0))
            lk = links.get(c)
            if lk is not None and lk[1] < 30 and lk[0] in added_arr and rec_arr.get(lk[0]) is not None:
                delta = max(delta, added_arr[lk[0]] - max(0.0, dep - rec_arr[lk[0]]))
            delta = max(delta, 0.0)
            tot = [delta + x for x in a]
            add[(d, c)] = tot
            added_arr[c] = tot[last_i]
            rec_arr[c] = arr
            last_on_block[blk] = c
    return dict(add=add, drop=drop)


# ------------------------------------------------------------------ ask A
def ask_a(target, js, rec, pieces, terms, bank, first, last):
    log = []
    with open(find(target, r"control_room_log"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            log.append(r)
    s7 = pdf(find(target, r"schedule7"))
    excused = {"PC", "RW", "WX", "BD"}           # 7.5.1 (a) to (d): police, works, weather, another vehicle
    from openpyxl import load_workbook
    wb = load_workbook(find(target, r"daily_returns"), read_only=True)
    ret = []
    hdr = None
    for r in wb["Returns"].iter_rows(values_only=True):
        if hdr is None:
            if r and r[0] == "Date":
                hdr = r
            continue
        if r[0]:
            ret.append(dict(zip(hdr, r)))
    seen_run = {(d, c) for (d, c) in rec}
    spans = defaultdict(set)
    cause = {}
    for e in log:
        if e["log_event"] not in ("LOST", "PART LOST"):
            continue
        t = datetime.strptime(e["log_time"], "%d/%m/%Y %H:%M")
        code = e["journey_ref"]
        j = js[code]
        # the operating day: a journey logged after midnight belongs to the day it ran
        d = t.date()
        if t.hour < 3 and j["times"][0] > 20 * 60:
            d -= timedelta(days=1)
        if e["log_event"] == "LOST":
            ls = range(len(j["km"]))
        else:
            a = j["stops"].index(e["lost_from_stop"])
            z = j["stops"].index(e["lost_to_stop"])
            ls = range(a, z)
        for l in ls:
            spans[(d, code)].add(l)
            cause.setdefault(((d, code), l), e["cause"])
    dmap = {"Mon-Fri": "MF", "Sat": "SA", "Sun": "SU"}
    for e in ret:
        if e["Status"] not in ("UNCOVERED", "PART COVERED"):
            continue
        d = datetime.strptime(e["Date"], "%d/%m/%Y").date()
        dt = day_type(d, bank)
        p = next(p for p in pieces[(dt, e["Duty"])] if p["k"] == e["Piece"])
        cf = hm(e["Covered from"]) if e["Covered from"] else None
        for code in p["journeys"]:
            if cf is not None and js[code]["times"][0] >= cf:
                continue
            if (d, code) in seen_run:
                continue                     # the AVL saw it run
            for l in range(len(js[code]["km"])):
                spans[(d, code)].add(l)
                cause.setdefault(((d, code), l), "SS")
    km = Counter()
    for (d, code), ls in spans.items():
        if not (first <= d <= last):
            continue
        j = js[code]
        for l in ls:
            if cause[((d, code), l)] not in excused:
                km[j["service"]] += j["km"][l]
    sched = Counter()
    d = first
    while d <= last:
        dt = day_type(d, bank)
        school = d.weekday() < 5 and d not in bank and any(a <= d <= b for a, b in terms)
        for j in js.values():
            if j["day"] == dt and (school or not j["school"]):
                sched[j["service"]] += sum(j["km"])
        d += timedelta(days=1)
    rel = {s: 100.0 * (sched[s] - km[s]) / sched[s] for s in sched}
    return km, rel, sched


# ------------------------------------------------------------------ ask B
def ask_b(target, js, rec, veh, names, R, detect_clock=True):
    fl = {}
    with open(find(target, r"fleet_register"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            fl[r["etm_unit"]] = r["registration"].replace(" ", "")
    stages = defaultdict(list)
    with open(find(target, r"fare_stages"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            stages[int(r["fare_stage"])].append(r["stop_name"])
    want = sorted(s for s, stops in stages.items() if all(x in R["unserved"] for x in stops))
    # each vehicle's journeys and their spans (local minutes), and its times at the timing points
    spans = defaultdict(list)
    tp_times = defaultdict(list)
    for (d, code), ev in rec.items():
        if js[code]["service"] != "41":
            continue
        v = veh[(d, code)]
        ms = [m for e, m in ev.values()]
        spans[(v, d)].append((min(ms), max(ms), js[code]["dir"]))
        for i, (e, m) in ev.items():
            nm = names[js[code]["stops"][i]]
            if nm in ("Thornsby Road", "Thornsby Quay"):
                tp_times[(v, d)].append(m)
    txns = []
    seen = set()
    with open(find(target, r"etm_transactions"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            k = (r["etm_unit"], r["txn_seq"], r["txn_time"], r["fare_stage"])
            if k in seen:
                continue
            seen.add(k)
            txns.append(r)
    # each machine's clock against its bus's AVL at the bridge stops, before and after the clock change: the offset
    # that puts the bridge-stop sales on the bus's own passages there
    groups = defaultdict(list)
    for r in txns:
        if int(r["fare_stage"]) not in (3, 4):
            continue
        t = datetime.strptime(r["txn_time"], "%Y-%m-%d %H:%M:%S")
        d = (t - timedelta(hours=3)).date()          # a sale after midnight belongs to the day's last journeys
        m = (t - datetime(d.year, d.month, d.day)).total_seconds() / 60.0
        tt = tp_times.get((fl[r["etm_unit"]], d))
        if tt:
            groups[(r["etm_unit"], d >= date(2026, 10, 25))].append((m, tt))
    shift = {}
    for (u, after), xs in groups.items():
        score = {}
        for o in (-60, 0, 60):
            score[o] = sum(1 for m, tt in xs if min(abs(m - o - x) for x in tt) <= 3) / len(xs)
        best = max(score, key=score.get)
        if detect_clock and best != 0 and after and score[best] > 2 * score[0]:
            shift[u] = float(best)
    boards = defaultdict(list)
    for j in js.values():
        if j["service"] == "41" and j["day"] == "MF":
            boards[j["block"]].append(j)
    cnt = Counter()
    days = set()
    for r in txns:
        t = datetime.strptime(r["txn_time"], "%Y-%m-%d %H:%M:%S")
        if r["etm_unit"] in shift and (t - timedelta(hours=3)).date() >= date(2026, 10, 25):
            t -= timedelta(minutes=shift[r["etm_unit"]])
        d = (t - timedelta(hours=3)).date()
        if d.weekday() >= 5:
            continue
        days.add(d)
        if int(r["fare_stage"]) not in want:
            continue
        m = (t - datetime(d.year, d.month, d.day)).total_seconds() / 60.0
        sp = spans.get((fl[r["etm_unit"]], d), [])
        dirn = None
        for a, z, dd in sp:
            if a - 2 <= m <= z + 2:
                dirn = dd
                break
        if dirn is None:
            # no AVL for the bus that day: the running board's journey timetabled through the stop at that time
            blk = r["running_board"].replace("/", "")
            cand = [j for j in boards[blk] if j["times"][0] - 2 <= m <= j["times"][-1] + 15] or boards[blk]
            dirn = min(cand, key=lambda j: abs(m - j["times"][1]))["dir"]
        band = "AM peak" if R["peaks"][0][0] <= m < R["peaks"][0][1] else (
            "PM peak" if R["peaks"][1][0] <= m < R["peaks"][1][1] else "Other times")
        cnt[("I" if dirn == "inbound" else "O", band)] += 1
        ASSIGN[(r["etm_unit"], r["txn_seq"], r["txn_time"])] = ("I" if dirn == "inbound" else "O", band)
    n = len(days)
    return {k: v / n for k, v in cnt.items()}, n, want, sorted(shift)


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    R = rules(target)
    js, names, terms = timetable(target)
    bank = {date(2026, 8, 31), date(2026, 12, 25), date(2026, 12, 28), date(2027, 1, 1), date(2027, 3, 26)}
    rec, veh = avl(target, js)
    links, pieces = duties(target, js)
    fails = []

    def check(name, got, want):
        good = got == want
        print("%s  %-46s verify %-16s figures %s" % ("PASS" if good else "FAIL", name, got, want))
        if not good:
            fails.append(name)
    au = punct(js, rec, R)
    for s in sorted(au, key=int):
        check("autumn punctuality, route %s" % s, round(au[s], 1), fig["autumn"][s])
    cl = replay(js, rec, links, R, names, bank)
    fc = punct(js, rec, R, closure=cl)
    named = sorted([s for s, v in fc.items() if v < R["floor"]], key=int)
    check("the notice's routes", named, fig["call"]["routes"])
    for s in sorted(fc, key=int):
        check("closure forecast below the floor, route %s" % s, fc[s] < R["floor"], fig["below_floor"][s])
    km, rel, sched = ask_a(target, js, rec, pieces, terms, bank, date(2026, 9, 1), date(2026, 12, 6))
    for s in sorted(km, key=int):
        check("lost km not excused, route %s" % s, round(km[s]), fig["ask_a"]["op_km"][s])
        check("reliability, route %s" % s, round(rel[s], 2), fig["ask_a"]["reliability"][s])
    check("lost km not excused, Lot 2", round(sum(km.values())), fig["ask_a"]["op_km_total"])
    check("reliability, Lot 2", round(100.0 * (sum(sched.values()) - sum(km.values())) / sum(sched.values()), 2),
          fig["ask_a"]["reliability_lot"])
    cells, n, want, slow = ask_b(target, js, rec, veh, names, R)
    print("      fare stages %s, %d weekdays, machines kept on summer time: %s" % (want, n, slow))
    for d in ("I", "O"):
        for b in ("AM peak", "PM peak", "Other times"):
            check("boardings %s %s" % (d, b), round(cells.get((d, b), 0.0)), fig["ask_b"]["cells"]["%s|%s" % (d, b)])
    check("boardings, all", round(sum(cells.values())), fig["ask_b"]["total"])
    print("\n%d failed" % len(fails))
    return not fails


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(0 if main(t) else 1)
