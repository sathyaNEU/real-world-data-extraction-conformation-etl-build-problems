"""Simulate the unit's 2026: every batch, tubing set, dose, weighed check and quarantine sort, with each dose's true
delivered volume. Everything downstream (the pack, the truth the checks assert on) reads this one simulation."""
import datetime as dt
import hashlib
from zoneinfo import ZoneInfo

import numpy as np

import params as P

TZ = ZoneInfo("America/Toronto")
UTC = dt.timezone.utc
_CACHE = {}


def rng(tag):
    h = int(hashlib.sha256(("%d:%s" % (P.SEED, tag)).encode()).hexdigest()[:12], 16)
    return np.random.default_rng(h)


def product(code):
    for p in P.PRODUCTS:
        if p["code"] == code:
            return p
    raise KeyError(code)


def serial_on(station, day):
    for s, a, b in P.STATIONS[station]["serials"]:
        if a <= day and (b is None or day <= b):
            return s
    raise KeyError((station, day))


def open_hours(day):
    if day in P.HOLIDAYS or day.weekday() == 6:
        return None
    if day.weekday() == 5:
        return (dt.time(8, 0), dt.time(16, 0))
    return (dt.time(7, 0), dt.time(23, 0))


def _local(day, t):
    return dt.datetime.combine(day, t, tzinfo=TZ)


def simulate():
    if "w" in _CACHE:
        return _CACHE["w"]
    r = rng("world")
    by_station = {}
    for p in P.PRODUCTS:
        by_station.setdefault(p["station"], []).append(p)
    batches, sets, doses, checks, sorts, events = [], [], [], [], [], []
    day_seq = {}
    set_id = 0
    lot_used = set()

    def new_lot():
        while True:
            lot = "TS%s-%06d" % (r.choice(["2511", "2601", "2604", "2607", "2610"]), int(r.integers(100000, 999999)))
            if lot not in lot_used:
                lot_used.add(lot)
                return lot

    for station in sorted(by_station):
        prods = by_station[station]
        installed = None          # the set on the station: dict with product, set-up time, batches carried
        day = P.FIRST_DAY
        while day <= P.LAST_DAY:
            hrs = open_hours(day)
            if hrs is None:
                day += dt.timedelta(days=1)
                installed = None
                continue
            sat = day.weekday() == 5
            todays = []
            for p in prods:
                rate = p["wk"][1] if sat else p["wk"][0]
                n = int(rate) + (1 if r.random() < rate - int(rate) else 0)
                todays += [p["code"]] * n
            if not todays:
                day += dt.timedelta(days=1)
                installed = None
                continue
            # the product left on the station from yesterday evening runs first; the rest in a shuffled order,
            # each product's batches of the day back to back
            uniq = list(dict.fromkeys(todays))
            r.shuffle(uniq)
            if installed and installed["product"] in uniq:
                uniq.remove(installed["product"])
                uniq.insert(0, installed["product"])
            order = [c for c in uniq for _ in range(todays.count(c))]
            # the day's batches are spread over the station's open hours (cleaning, release and stock waits
            # between them), so the last one runs late in the evening shift on a weekday
            t = _local(day, hrs[0]) + dt.timedelta(minutes=float(r.uniform(8, 40)))
            close = _local(day, hrs[1])
            sizes = [int(r.integers(product(c)["size"][0], product(c)["size"][1] + 1)) for c in order]
            work = sum(sz * float(np.mean(P.SECONDS_PER_DOSE[station])) / 60.0 + 24.0 for sz in sizes)
            room = (close - t).total_seconds() / 60.0 - float(r.uniform(12, 40)) - work
            gaps = list(np.maximum(room, 0.0) * r.dirichlet(np.ones(len(order)))) if len(order) > 1 else [0.0]
            for j, code in enumerate(order):
                p = product(code)
                if j > 0:
                    t += dt.timedelta(minutes=float(gaps[j - 1]))
                if j == len(order) - 1 and not sat:
                    # the evening shift's stock-building batch: the station's last batch starts after 19:00
                    t = max(t, _local(day, dt.time(19, 5)) + dt.timedelta(minutes=float(r.uniform(0, 45))))
                if t > close - dt.timedelta(minutes=30):
                    break
                size = sizes[j]
                key = (day, station)
                day_seq[key] = day_seq.get(key, 0) + 1
                batch_no = "%s%s%02d" % (day.strftime("%y%m%d"), P.LETTER[station], day_seq[key])
                carry = False
                if installed and installed["product"] == code and installed["sid"] is not None:
                    age_h = (t - installed["setup_t"]).total_seconds() / 3600.0
                    nb = installed["batches"]
                    pr = p["carry2"] if nb == 1 else (p["carry3"] if nb == 2 else 0.0)
                    carry = age_h < P.SET_MAX_HOURS and r.random() < pr
                b = dict(batch_no=batch_no, product=code, station=station, serial=serial_on(station, day), size=size,
                         start=t, day=day)
                batches.append(b)

                def set_up(at):
                    nonlocal set_id
                    set_id += 1
                    a0 = float(r.normal(p["a0"], p["a0sd"]))
                    lot = new_lot()
                    s = dict(sid=set_id, product=code, station=station, serial=serial_on(station, at.date()),
                             setup_t=at, a0=a0, k=p["k"], lot=lot, pumped_l=0.0, batches=1, doses=0)
                    sets.append(s)
                    events.append(dict(serial=s["serial"], t=at, event="SET_UP", lot=lot))
                    events.append(dict(serial=s["serial"], t=at + dt.timedelta(seconds=float(r.uniform(150, 420))),
                                       event="CAL_OK", lot=lot))
                    if r.random() < P.RESEAT_RATE:
                        tt = at + dt.timedelta(seconds=float(r.uniform(500, 900)))
                        events.append(dict(serial=s["serial"], t=tt, event="ALARM_OCCLUSION", lot=lot))
                        events.append(dict(serial=s["serial"], t=tt + dt.timedelta(seconds=float(r.uniform(60, 200))),
                                           event="SET_UP", lot=lot))
                    return s

                if carry:
                    cur = installed["set"]
                    cur["batches"] += 1
                    installed["batches"] += 1
                    t += dt.timedelta(minutes=float(r.uniform(4, 9)))
                else:
                    t += dt.timedelta(minutes=float(r.uniform(3, 8)))
                    cur = set_up(t)
                    installed = dict(product=code, sid=cur["sid"], setup_t=cur["setup_t"], batches=1, set=cur)
                    t += dt.timedelta(minutes=float(r.uniform(9, 16)))
                last_good = None
                i = 0
                made = 0
                while made < size:
                    sec = float(r.uniform(*P.SECONDS_PER_DOSE[station]))
                    t += dt.timedelta(seconds=sec)
                    m = cur["a0"] - cur["k"] * cur["pumped_l"]
                    dev = m + float(r.normal(0.0, p["s"]))
                    if r.random() < P.ABORT_RATE:
                        doses.append(dict(batch_no=batch_no, product=code, serial=cur["serial"], t=t, seq=None,
                                          sid=cur["sid"], dev=None, status="ABORTED", vol=p["vol"]))
                        events.append(dict(serial=cur["serial"], t=t, event="ALARM_OCCLUSION", lot=cur["lot"]))
                        cur["pumped_l"] += p["vol"] * float(r.uniform(0.2, 0.8)) / 1000.0
                        continue
                    made += 1
                    i += 1
                    d = dict(batch_no=batch_no, product=code, serial=cur["serial"], t=t, seq=made, sid=cur["sid"],
                             dev=dev, mean=m, status="COMPLETE", vol=p["vol"], pumped_l=cur["pumped_l"])
                    doses.append(d)
                    cur["pumped_l"] += p["vol"] * (1 + dev / 100.0) / 1000.0
                    cur["doses"] += 1
                    weigh = made == 1 or made % P.CHECK_EVERY["bag" if "bag" in p["name"] else "syringe"] == 0
                    if weigh:
                        out = abs(dev) > p["tol"]
                        checks.append(dict(dose=d, out=out, t=t + dt.timedelta(seconds=float(r.uniform(40, 240)))))
                        if out:
                            lo = last_good if last_good is not None else made
                            span = [x for x in doses if x["batch_no"] == batch_no and x["status"] == "COMPLETE"
                                    and lo < x["seq"] <= made]
                            rej = sum(1 for x in span if abs(x["dev"]) > p["tol"])
                            sorts.append(dict(batch_no=batch_no, product=code, t=t, quarantined=len(span),
                                              rejected=rej, station=station))
                            t += dt.timedelta(minutes=float(r.uniform(12, 25)))
                            cur = set_up(t)
                            installed = dict(product=code, sid=cur["sid"], setup_t=cur["setup_t"], batches=1, set=cur)
                            t += dt.timedelta(minutes=float(r.uniform(9, 16)))
                            last_good = None
                        else:
                            last_good = made
                b["end"] = t
                b["made"] = made
                t += dt.timedelta(minutes=float(r.uniform(6, 25)))
            # the evening's set stays on the station overnight (and over a closed day it is taken down)
            nxt = day + dt.timedelta(days=1)
            if open_hours(nxt) is None:
                installed = None
            day = nxt
    w = dict(batches=batches, sets=sets, doses=doses, checks=checks, sorts=sorts, events=events)
    _CACHE["w"] = w
    return w


def truth():
    """Each candidate's out-of-tolerance doses per 100,000 doses made, from the true delivered volumes."""
    w = simulate()
    out = {}
    for c in P.CANDIDATES + [p["code"] for p in P.PRODUCTS if p.get("verified")]:
        p = product(c)
        ds = [d for d in w["doses"] if d["product"] == c and d["status"] == "COMPLETE"]
        n = len(ds)
        bad = sum(1 for d in ds if abs(d["dev"]) > p["tol"])
        out[c] = dict(doses=n, bad=bad, per100k=1e5 * bad / n if n else 0.0)
    return out


if __name__ == "__main__":
    w = simulate()
    print(len(w["batches"]), "batches", len(w["sets"]), "sets", len(w["doses"]), "doses", len(w["checks"]), "checks",
          len(w["sorts"]), "sorts")
    for c, v in truth().items():
        print(c, product(c)["short"], v)
