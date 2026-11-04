"""Everything the golden states, recomputed from the shipped files alone: the patrol call, the asks and the rungs
of the ladder. Nothing here imports the generator's world or its simulation."""
import bisect
import collections
import csv
import datetime as dt
import json
import math
import os
import re
from zoneinfo import ZoneInfo

import openpyxl
from pypdf import PdfReader

CT = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
F = {
    "relay": "protection/feeder_relay_events_2025_2026.csv",
    "recloser": "protection/recloser_control_events_2025_2026.csv",
    "soe": "scada/soe_breakers_reclosers_2025_2026.csv",
    "oms": "oms/oms_outage_history_2025_2026.xlsx",
    "feeders": "assets/feeder_register.xlsx",
    "devices": "assets/protective_device_register.csv",
    "transformers": "assets/distribution_transformers.csv",
    "sps": "customers/service_points_2026-10-31.csv",
    "strokes": "weather/lightning_strokes_2025_2026.csv",
    "asos": "weather/airport_hourly_obs_2025_2026.csv",
    "subs": "gis/substations.geojson",
    "procedure": "procedures/DRP-04_distribution_reliability_procedure_rev6.pdf",
}
FIVE = 5 * 60 * 1000
CEMI_N = 2
MIN = 60 * 1000
REP0, REP1 = dt.date(2026, 1, 1), dt.date(2026, 10, 31)
WIN0, WIN1 = dt.date(2026, 8, 1), dt.date(2026, 10, 31)
BASE0, BASE1 = dt.date(2025, 8, 1), dt.date(2025, 10, 31)


def P(T, k):
    return os.path.join(T, F[k])


def rows(T, k):
    with open(P(T, k), newline="") as fh:
        return list(csv.DictReader(fh))


def ms(d):
    return int(d.timestamp() * 1000)


def utc_iso(s):
    s = s.replace("Z", "+00:00")
    return ms(dt.datetime.fromisoformat(s))


def from_wall(s, fmt):
    return ms(dt.datetime.strptime(s, fmt).replace(tzinfo=CT))


def scada_t(s):
    body, zone = s.rsplit(" ", 1)
    off = {"CDT": -5, "CST": -6}[zone]
    return ms(dt.datetime.strptime(body, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=dt.timezone(dt.timedelta(hours=off))))


def cst_t(s):
    return ms(dt.datetime.strptime(s, "%m/%d/%Y %H:%M:%S").replace(tzinfo=dt.timezone(dt.timedelta(hours=-6))))


def local(t):
    return dt.datetime.fromtimestamp(t / 1000, UTC).astimezone(CT)


def lday(t):
    return local(t).date()


def floor_min(t):
    return t - t % MIN


# --------------------------------------------------------------------------- the register and the customers
class Net:
    def __init__(self, T):
        wb = openpyxl.load_workbook(P(T, "feeders"), read_only=True)
        ws = wb["Feeders"]
        it = ws.iter_rows(values_only=True)
        hdr = next(it)
        self.feeders = {}
        for r in it:
            if r[0]:
                self.feeders[r[0]] = dict(zip(hdr, r))
        ws2 = wb[wb.sheetnames[1]]
        it = ws2.iter_rows(values_only=True)
        next(it)
        self.old_feeder, self.old_breaker, self.old_point = {}, {}, {}
        for r in it:
            if r[0]:
                self.old_feeder[r[0]] = r[1]
                self.old_breaker[r[2]] = r[3]
                self.old_point[r[4]] = r[5]
        wb.close()
        self.rows = collections.defaultdict(list)
        self.point = {}
        bounds = set()
        for r in rows(T, "devices"):
            dev = self.nb(r["device_id"])
            a = dt.date.fromisoformat(r["in_service_from"])
            b = dt.date.fromisoformat(r["in_service_to"]) if r["in_service_to"] else dt.date(2099, 1, 1)
            self.rows[dev].append(dict(type=r["device_type"], feeder=self.nf(r["feeder"]), pole=r["pole"],
                                       up=self.nb(r["upstream_device"]) if r["upstream_device"] else None, a=a, b=b,
                                       scada=r["scada_point"], shots=r["shots_to_lockout"],
                                       phasing=r["terminal_phasing"]))
            if r["scada_point"]:
                self.point[r["scada_point"]] = dev
            for x in (a, b + dt.timedelta(days=1)):
                if dt.date(2025, 1, 1) < x <= dt.date(2026, 10, 31):
                    bounds.add(x)
        for old, new in self.old_point.items():
            self.point[old] = self.nb(self.point.get(new, new))
        self.bounds = sorted(bounds)
        self.trans = {}
        for r in rows(T, "transformers"):
            self.trans[r["transformer_id"]] = dict(feeder=r["feeder"], dev=self.nb(r["protective_device"]),
                                                   phase=r["phase"])
        self.sp = {}
        self.sp_by_t = collections.defaultdict(list)
        for r in rows(T, "sps"):
            v = dict(t=r["transformer_id"], feeder=r["feeder"], con=dt.date.fromisoformat(r["service_connected"]),
                     dis=dt.date.fromisoformat(r["service_disconnected"]) if r["service_disconnected"] else None)
            self.sp[r["service_point"]] = v
            self.sp_by_t[r["transformer_id"]].append(r["service_point"])
        self._down = {}

    def nb(self, d):
        return self.old_breaker.get(d, d)

    def nf(self, f):
        return self.old_feeder.get(f, f)

    def row(self, dev, day):
        for r in self.rows.get(dev, []):
            if r["a"] <= day <= r["b"]:
                return r
        return None

    def up(self, dev, day):
        r = self.row(dev, day)
        return r["up"] if r else None

    def feeder(self, dev, day):
        if dev in self.sp:
            return self.feeder(self.trans[self.sp[dev]["t"]]["dev"], day)
        if dev in self.trans:
            return self.feeder(self.trans[dev]["dev"], day)
        r = self.row(dev, day)
        return r["feeder"] if r else None

    def chain(self, dev, day):
        out = []
        while dev:
            out.append(dev)
            dev = self.up(dev, day)
        return out

    def regime(self, day):
        return bisect.bisect_right(self.bounds, day)

    def down_transformers(self, dev, day):
        if dev in self.trans:
            return [dev]
        k = self.regime(day)
        if k not in self._down:
            dd = collections.defaultdict(list)
            for tid in sorted(self.trans):
                for x in self.chain(self.trans[tid]["dev"], day):
                    dd[x].append(tid)
            self._down[k] = dd
        return self._down[k].get(dev, [])

    def active(self, sp, day):
        v = self.sp[sp]
        return v["con"] <= day and (v["dis"] is None or v["dis"] > day)

    def customers(self, dev, day):
        if dev in self.sp:
            return {dev} if self.active(dev, day) else set()
        out = set()
        for tid in self.down_transformers(dev, day):
            for sp in self.sp_by_t[tid]:
                if self.active(sp, day):
                    out.add(sp)
        return out


def procedure_constants(T):
    text = " ".join((p.extract_text() or "") for p in PdfReader(P(T, "procedure")).pages)
    text = re.sub(r"\s+", " ", text)
    tmed = float(re.search(r"is ([\d.]+) minutes of daily system SAIDI", text).group(1))
    nsys = int(re.search(r"divided by ([\d,]+), the customers served by the system", text).group(1).replace(",", ""))
    return tmed, nsys, text


# --------------------------------------------------------------------------- operations
def soe(T, net):
    by = collections.defaultdict(list)
    for r in rows(T, "soe"):
        by[net.point[r["point"]]].append((scada_t(r["time"]), r["state"]))
    for k in by:
        by[k].sort()
    return by


def open_intervals(seq):
    out, t_open = [], None
    for t, s in seq:
        if s == "OPEN" and t_open is None:
            t_open = t
        elif s == "CLOSED" and t_open is not None:
            out.append((t_open, t))
            t_open = None
    return out


def recloser_log(T):
    by = collections.defaultdict(list)
    for r in rows(T, "recloser"):
        by[r["control"]].append(dict(t=cst_t(r["time_cst"]), ev=r["event"], term=r["fault_terminals"],
                                     ka=float(r["fault_ka"]) if r["fault_ka"] else None))
    for k in by:
        by[k].sort(key=lambda x: x["t"])
    return by


def device_events(T, net, S=None, L=None):
    """Momentary interruption events of each breaker (from SCADA) and recloser (from its control's log): the
    operations within five minutes of the first, the device closed again inside those five minutes."""
    S = S or soe(T, net)
    L = L or recloser_log(T)
    ev = []
    for dev, seq in S.items():
        if net.rows[dev][0]["type"] != "BREAKER":
            continue
        opens = [(t, s) for t, s in seq]
        i = 0
        while i < len(opens):
            t, s = opens[i]
            if s != "OPEN":
                i += 1
                continue
            first = t
            j = i
            last_close = None
            n_open = 0
            closed_all = True
            while j < len(opens) and opens[j][0] <= first + FIVE:
                if opens[j][1] == "OPEN":
                    n_open += 1
                    if j + 1 >= len(opens) or opens[j + 1][1] != "CLOSED" or opens[j + 1][0] > first + FIVE:
                        closed_all = False
                else:
                    last_close = opens[j][0]
                j += 1
            if closed_all and n_open:
                ev.append(dict(device=dev, t=first, end=last_close, day=lday(first), ops=n_open, src="SCADA"))
            # skip to the end of this group
            k = j
            while k < len(opens) and not (opens[k][1] == "OPEN" and opens[k][0] > first + FIVE):
                k += 1
            i = k
    for dev, seq in L.items():
        i = 0
        while i < len(seq):
            if seq[i]["ev"] != "TRIP":
                i += 1
                continue
            first = seq[i]["t"]
            grp = []
            j = i
            while j < len(seq) and seq[j]["t"] <= first + FIVE:
                grp.append(seq[j])
                j += 1
            lock = [g for g in grp if g["ev"] == "LOCKOUT"]
            close_after = [g for g in grp if g["ev"] == "CLOSE"]
            if not lock or close_after:
                ev.append(dict(device=dev, t=first, end=grp[-1]["t"], day=lday(first),
                               ops=sum(1 for g in grp if g["ev"] == "TRIP"), src="LOG",
                               trip=grp[0]))
            k = j
            while k < len(seq) and not (seq[k]["ev"] == "TRIP" and seq[k]["t"] > first + FIVE):
                k += 1
            i = k
    ev.sort(key=lambda e: e["t"])
    for e in ev:
        e["feeder"] = net.feeder(e["device"], e["day"])
    return ev


# --------------------------------------------------------------------------- sustained interruptions
def oms(T, net):
    wb = openpyxl.load_workbook(P(T, "oms"), read_only=True)
    leg = list(wb["Legacy tickets"].iter_rows(values_only=True))
    inc = list(wb["Incidents"].iter_rows(values_only=True))
    stp = list(wb["Restoration Steps"].iter_rows(values_only=True))
    wb.close()
    out = []
    kids = collections.defaultdict(list)
    for r in leg[1:]:
        if r[1]:
            kids[r[1]].append(r)
    for r in leg[1:]:
        if r[1] or not r[0]:
            continue
        start = from_wall(r[5], "%m/%d/%Y %H:%M")
        rest = from_wall(r[6], "%m/%d/%Y %H:%M")
        steps = [(from_wall(k[6], "%m/%d/%Y %H:%M"), int(k[7])) for k in sorted(kids[r[0]], key=lambda k: k[0])]
        if steps:
            steps.append((rest, int(r[7]) - sum(n for _, n in steps)))
        out.append(dict(id=r[0], src="legacy", device=net.nb(r[3]), dtype=r[4], start=start, restore=rest,
                        oms_customers=int(r[7]), steps=steps, cause=r[8], circuit=net.nf(r[2])))
    st = collections.defaultdict(list)
    for r in stp[1:]:
        if r[0]:
            st[r[0]].append((int(r[1]), utc_iso(r[2]), int(r[3])))
    for r in inc[1:]:
        if not r[0]:
            continue
        steps = [(t, n) for _, t, n in sorted(st.get(r[0], []))]
        out.append(dict(id=r[0], src="incident", device=r[2], dtype=r[3], start=utc_iso(r[4]), restore=utc_iso(r[5]),
                        oms_customers=int(r[6]), steps=steps, cause=r[7], circuit=r[1]))
    return out


def interruptions(T, net, S=None):
    """Every sustained interruption: the OMS's tickets and incidents, and the breaker and recloser openings that
    SCADA holds for more than five minutes with no ticket behind them."""
    S = S or soe(T, net)
    items = oms(T, net)
    by_dev = collections.defaultdict(list)
    for o in items:
        by_dev[o["device"]].append(o["start"])
    for dev, seq in S.items():
        for a, b in open_intervals(seq):
            if b - a <= FIVE:
                continue
            if any(abs(s - a) <= 2 * MIN for s in by_dev.get(dev, [])):
                continue
            items.append(dict(id="SCADA %s %d" % (dev, a), src="scada", device=dev,
                              dtype=net.rows[dev][0]["type"], start=a, restore=b, oms_customers=None, steps=[],
                              cause=None, circuit=None))
    items.sort(key=lambda o: o["start"])
    for o in items:
        o["day"] = lday(o["start"])
        o["feeder"] = net.feeder(o["device"], o["day"])
        o["reach"] = net.customers(o["device"], o["day"])
    # a service ticket opened at the minute the device above it closed is that customer's interruption carrying on
    by_restore = collections.defaultdict(list)
    for o in items:
        by_restore[o["restore"]].append(o)
    for o in items:
        o["continues"] = None
        if o["dtype"] != "SERVICE":
            continue
        for p in by_restore.get(o["start"], []):
            if p is not o and o["device"] in p["reach"]:
                o["continues"] = p
                break
    for o in items:
        p = o
        while p["continues"] is not None:
            p = p["continues"]
        o["began"] = p["start"]
        o["day"] = lday(p["start"])
    # customers already without supply when an interruption begins are not interrupted by it
    starts = [o["start"] for o in items]
    for i, o in enumerate(items):
        already = set()
        lo = bisect.bisect_left(starts, o["start"] - 40 * 86400 * 1000)
        for p in items[lo:i]:
            if p["start"] < o["start"] < p["restore"] and p["device"] != o["device"]:
                already |= o["reach"] & p["reach"]
        o["hit"] = o["reach"] - already if o["continues"] is None else set()
        o["dark"] = o["reach"] if o["continues"] is not None else o["hit"]
        if o["continues"] is not None:
            o["cmi"] = len(o["reach"]) * (o["restore"] - o["start"]) / MIN
        elif o["steps"]:
            o["cmi"] = sum(n * (t - o["start"]) / MIN for t, n in o["steps"])
        else:
            o["cmi"] = len(o["hit"]) * (o["restore"] - o["start"]) / MIN
    return items


def major_event_days(items, tmed, nsys):
    daily = collections.defaultdict(float)
    for o in items:
        daily[o["day"]] += o["cmi"]
    saidi = {d: v / nsys for d, v in daily.items()}
    return sorted(d for d, v in saidi.items() if d.year == 2026 and v > tmed), saidi


# --------------------------------------------------------------------------- the asks
def indices(T, net, items, ev, meds):
    medset = set(meds)
    inwin = lambda d: REP0 <= d <= REP1 and d not in medset
    nt = collections.Counter()
    end_feeder = {}
    for sp, v in net.sp.items():
        if net.active(sp, REP1):
            f = net.feeder(sp, REP1)
            end_feeder[sp] = f
            nt[f] += 1
    ci, cmi, mom = collections.Counter(), collections.Counter(), collections.Counter()
    per_sp = collections.Counter()
    for o in items:
        if not inwin(o["day"]):
            continue
        ci[o["feeder"]] += len(o["hit"])
        cmi[o["feeder"]] += o["cmi"]
        for sp in o["hit"]:
            per_sp[sp] += 1
    starts = [o["start"] for o in items]
    for e in ev:
        reach = net.customers(e["device"], e["day"])
        em = floor_min(e["t"])
        lo = bisect.bisect_left(starts, e["t"] - 40 * 86400 * 1000)
        hi = bisect.bisect_right(starts, e["t"] + FIVE)
        out_now, absorbed = set(), set()
        for o in items[lo:hi]:
            if o["start"] < em and e["t"] < o["restore"]:
                out_now |= reach & o["dark"]
            elif em <= o["start"] <= e["t"] + FIVE:
                absorbed |= reach & o["dark"]
        e["reached"] = reach - out_now - absorbed
        e["n_reach"], e["n_out"], e["n_abs"] = len(reach), len(out_now), len(absorbed - out_now)
    # DRP-04 2.5 counts a customer's momentary interruptions within five minutes of the first as one event, so a
    # second device opening on the same customers inside those five minutes adds nothing for them
    opened = {}
    for e in ev:
        n = 0
        for c in e["reached"]:
            t0 = opened.get(c)
            if t0 is None or e["t"] - t0 > FIVE:
                opened[c] = e["t"]
                n += 1
        e["n"] = n
        e["n_merged"] = len(e["reached"]) - n
        del e["reached"]
        if inwin(e["day"]):
            mom[e["feeder"]] += e["n"]
    cemi = collections.Counter()
    for sp, f in end_feeder.items():
        if per_sp[sp] > CEMI_N:
            cemi[f] += 1
    out = {}
    for f in sorted(nt):
        out[f] = dict(nt=nt[f], saifi=ci[f] / nt[f], saidi=cmi[f] / nt[f], maifi=mom[f] / nt[f], cemi=cemi[f])
    return out, per_sp


# --------------------------------------------------------------------------- the call
PH = {"A": "A", "B": "B", "C": "C"}


def fault_records(T, net, ev):
    """The faulted phase and the fault current each momentary event's first operation recorded: the feeder
    relays' event records for breakers, the controls' logs for reclosers."""
    rel = collections.defaultdict(list)
    for r in rows(T, "relay"):
        rel[net.nb(r["relay"])].append((utc_iso(r["utc_time"]), r))
    for k in rel:
        rel[k].sort(key=lambda x: x[0])
    keys = {k: [x[0] for x in v] for k, v in rel.items()}
    out = []
    for e in ev:
        if e["src"] == "SCADA":
            lst = rel.get(e["device"], [])
            ks = keys.get(e["device"], [])
            i = bisect.bisect_left(ks, e["t"] - 2000)
            if i >= len(ks) or ks[i] > e["t"] + 2000:
                continue
            r = lst[i][1]
            ph = r["event_type"].split()[0].replace("G", "") if r["event_type"].split()[0] != "ABC" else "ABC"
            cur = max(int(r["i%s_a" % p.lower()]) for p in ph)
            out.append(dict(e, phases=ph, current=cur, ig=int(r["ig_a"])))
        else:
            tr = e["trip"]
            row = net.rows[e["device"]][0]
            order = row["phasing"].split("-")
            tt = tr["term"]
            terms = [int(x) for x in tt.replace("-G", "").split("-")]
            ph = "".join(sorted(order[k - 1] for k in terms))
            out.append(dict(e, phases=ph, current=int(round(tr["ka"] * 1000)), ig=None))
    return out


def largest_group(recs, band=1.04, days=True):
    """Each feeder's largest set of momentary faults recorded by one device on one phase whose recorded currents
    lie within a band, counted on separate days."""
    by = collections.defaultdict(list)
    for r in recs:
        by[(r["feeder"], r["device"], r["phases"])].append(r)
    best = {}
    for (f, dev, ph), xs in by.items():
        xs.sort(key=lambda r: r["current"])
        for i in range(len(xs)):
            g = [x for x in xs[i:] if x["current"] <= xs[i]["current"] * band]
            n = len({x["day"] for x in g}) if days else len(g)
            if n > best.get(f, (0,))[0]:
                best[f] = (n, dev, ph, g)
    return best


def zone(net, dev, day):
    """A protective device's zone: the reclosers next beyond it on the main line."""
    beyond = []
    for d, rs in net.rows.items():
        r = net.row(d, day)
        if r and r["type"] == "RECLOSER" and r["up"] == dev:
            beyond.append((d, r["pole"]))
    return sorted(beyond)


def compute(T):
    net = Net(T)
    tmed, nsys, text = procedure_constants(T)
    S = soe(T, net)
    L = recloser_log(T)
    ev = device_events(T, net, S, L)
    items = interruptions(T, net, S)
    meds, daily = major_event_days(items, tmed, nsys)
    idx, per_sp = indices(T, net, items, ev, meds)
    win = [e for e in ev if WIN0 <= e["day"] <= WIN1]
    recs = fault_records(T, net, win)
    best = largest_group(recs)
    order = sorted(best, key=lambda f: -best[f][0])
    call, ru = order[0], order[1]
    sep = {}
    for f in (call, ru):
        n, dev, ph, g = best[f]
        cs = sorted(x["current"] for x in g)
        sep[f] = dict(n=n, device=dev, phase=ph, lo=cs[0], hi=cs[-1], first=min(x["day"] for x in g),
                      last=max(x["day"] for x in g), behind=len(net.customers(dev, REP1)),
                      zone_to=zone(net, dev, REP1), pole=net.row(dev, REP1)["pole"],
                      dates=sorted({x["day"] for x in g}))
    return dict(net=net, tmed=tmed, nsys=nsys, ev=ev, items=items, meds=meds, daily=daily, idx=idx, per_sp=per_sp,
                recs=recs, best=best, order=order, call=call, runner_up=ru, sep=sep, soe=S, log=L)


# --------------------------------------------------------------------------- the ladder's cheap rungs
def storm_days(T):
    subs = json.load(open(P(T, "subs")))
    pts = {f["properties"]["substation"]: f["geometry"]["coordinates"] for f in subs["features"]}
    days = {s: set() for s in pts}
    for r in rows(T, "strokes"):
        if r["type"] != "CG":
            continue
        la, lo = float(r["latitude"]), float(r["longitude"])
        d = lday(utc_iso(r["utc_time"]))
        for s, (slo, sla) in pts.items():
            if haversine_mi(la, lo, sla, slo) <= 5.0:
                days[s].add(d)
    gust = set()
    for r in rows(T, "asos"):
        if r["gust"] not in ("M", "") and float(r["gust"]) * 1.15078 >= 40.0:
            gust.add(lday(utc_iso(r["valid"].replace(" ", "T") + ":00Z")))
    return days, gust


def damp_days(T):
    out = set()
    for r in rows(T, "asos"):
        t = utc_iso(r["valid"].replace(" ", "T") + ":00Z")
        l = local(t)
        if 4.0 <= l.hour + l.minute / 60 < 9.5 and r["relh"] != "M" and float(r["relh"]) >= 97:
            out.add(l.date())
    return out


def haversine_mi(la1, lo1, la2, lo2):
    R = 3958.8
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def ladder(T, res):
    """The field's patrol screen and its variants, each feeder's figure on each."""
    net, ev = res["net"], res["ev"]
    sd, gust = storm_days(T)
    damp = damp_days(T)
    sub_of = {}
    for f, v in net.feeders.items():
        sub_of[f] = {"Bluffview": "BLV", "Cotter Road": "CTR", "Millrace": "MLR", "North Yard": "NYD",
                     "Sycamore": "SYC"}[v["Substation"]]
    R = {}
    for f in net.feeders:
        oh = float(net.feeders[f]["Overhead miles"])
        storm = sd[sub_of[f]] | gust
        e26 = [e for e in ev if e["feeder"] == f and WIN0 <= e["day"] <= WIN1]
        e25 = [e for e in ev if e["feeder"] == f and BASE0 <= e["day"] <= BASE1]
        n26 = [e for e in e26 if e["day"] not in storm]
        n25 = [e for e in e25 if e["day"] not in storm]
        recs = [r for r in res["recs"] if r["feeder"] == f]
        sp = [r["phases"] for r in recs if len(r["phases"]) == 1]
        cnt = [sp.count(p) for p in "ABC"]
        n = len(sp)
        R[f] = dict(raw=len(e26), raw25=len(e25), chg=len(e26) - len(e25), ns=len(n26), ns25=len(n25),
                    nsmi=len(n26) / oh, dflt=(len(n26) - len(n25)) / oh, nsd=len(n26) - len(n25),
                    damp=sum(1 for e in n26 if e["day"] in damp), oh=oh,
                    chi=(sum((c - n / 3) ** 2 / (n / 3) for c in cnt) if n >= 6 else 0.0),
                    share=(max(cnt) / n if n >= 6 else 0.0), n1=n,
                    per_cust=(len(n26) - len(n25)) / res["idx"][f]["nt"] * 1000)
    return R
