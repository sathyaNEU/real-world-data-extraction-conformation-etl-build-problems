"""The clean truth: every parcel Kurier Warta collected from 30 September to 30 October 2026, the hub that sorted it
(its plan's hub, or Strykow's manual line on a night Pruszkow overflowed), whether that hub's sort was recorded, the
trailer it came off at its delivery depot and the morning burst it was scanned in, its delivery, the couriers' handheld
events with the re-sends, and the shippers' pre-advices. Nothing here is a file: pack.py cuts the feeds from it."""
import datetime as dt
import math

import numpy as np

import params as P

HUB_BASE = {h[0]: h[3] for h in P.HUBS}
DEPOT = {d[0]: d for d in P.DEPOTS}
DEPOTS = [d[0] for d in P.DEPOTS]
HUB_ARRIVE = {"HPOZ": 252, "HWRO": 246, "HKTW": 258, "HKRK": 255, "HLDZ": 249, "HWAW": 262}   # minutes after midnight
OLD_FLEET = ("D-POZ2", "D-WRO2", "D-KTW2", "D-KRK2", "D-LDZ2", "D-WAW2")   # couriers still on the TC51 handheld
MARKET_DEPOTS = ("D-POZ1", "D-WRO1", "D-KTW1", "D-KRK1", "D-LDZ1", "D-WAW1")  # marketplace sellers collected here
B2B_DEPOTS = OLD_FLEET                                                        # contract B2B shippers collected here


def check_digit(body):
    """the carrier's check digit on a twelve-digit body: weights 3 and 1 from the right, mod 10"""
    s = 0
    for i, ch in enumerate(reversed(body)):
        s += int(ch) * (3 if i % 2 == 0 else 1)
    return str((10 - s % 10) % 10)


def tracking(serial):
    body = "62" + "%010d" % serial
    return body + check_digit(body)


def pickup_days():
    d, out = P.FIRST_PICKUP, []
    while d <= P.LAST_PICKUP:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def unload_day(pick):
    return pick + dt.timedelta(days=1)


def plan_hub(dest, night):
    if dest == "D-WRO2" and night >= P.OPOLE_REHOME:
        return "HKTW"
    return DEPOT[dest][2]


def depot_code(dest, day):
    if dest == "D-KRK1" and day >= P.KRK_MOVE:
        return P.KRK_NEW[0]
    return dest


def waw_miss(util):
    x = min(1.0, max(0.0, (util - P.WAW_U0) / (1.0 - P.WAW_U0)))
    return P.WAW_P_FLOOR + P.WAW_P_RISE * x ** 2


def shippers(rng):
    """shipper accounts by home depot: api (prints labels, pre-advises the number), marketplace (label printed at
    collection, pre-advises its order reference), b2b (master number, pieces), legacy (the KW contract range)"""
    out = []
    acct = 400113
    for d in DEPOTS:
        n = int(rng.integers(17, 25))
        for i in range(n):
            acct += int(rng.integers(3, 41))
            r = rng.random()
            if d in MARKET_DEPOTS and r < 0.30:
                kind = "marketplace"
            elif d in B2B_DEPOTS and r < 0.34:
                kind = "b2b"
            elif r > 0.92:
                kind = "legacy"
            else:
                kind = "api"
            out.append({"account": "K%06d" % acct, "depot": d, "kind": kind,
                        "weight": float(rng.lognormal(0, 0.9)), "slot": float(rng.uniform(9.2, 16.9) * 60),
                        "serial": int(rng.integers(10 ** 8, 9 * 10 ** 8)) * 10})
    return out


def world(seed=P.SEED):
    rng = np.random.default_rng(seed)
    shp = shippers(np.random.default_rng([seed, 0, 9]))
    by_depot = {d: [s for s in shp if s["depot"] == d] for d in DEPOTS}
    days = pickup_days()
    o_w = np.array([DEPOT[d][4] for d in DEPOTS]); o_w = o_w / o_w.sum()
    d_w = np.array([DEPOT[d][3] for d in DEPOTS]); d_w = d_w / d_w.sum()
    legacy_serial = [int(np.random.default_rng([seed, 0, 8]).integers(10 ** 7, 9 * 10 ** 7))]
    market_stock = {d: int(np.random.default_rng([seed, i, 7]).integers(10 ** 8, 9 * 10 ** 8)) * 10
                    for i, d in enumerate(DEPOTS)}
    parcels, shipments = [], []
    pid = sid = 0
    for k, day in enumerate(days):
        g = np.random.default_rng([seed, k, 1])
        vol = P.BASE_DAILY * P.WEEKDAY[day.weekday()] * (1 + P.RAMP_PER_DAY * k) * g.lognormal(0, 0.035)
        for oi, o in enumerate(DEPOTS):
            target = int(round(vol * o_w[oi]))
            ss = by_depot[o]
            sw = np.array([s["weight"] for s in ss]); sw = sw / sw.sum()
            made = 0
            while made < target:
                s = ss[int(g.choice(len(ss), p=sw))]
                n = 1
                if s["kind"] == "b2b" and g.random() < 0.46:
                    n = int(min(6, 2 + g.geometric(0.55) - 1))
                dst = DEPOTS[int(g.choice(len(DEPOTS), p=d_w))]
                while dst == o:
                    dst = DEPOTS[int(g.choice(len(DEPOTS), p=d_w))]
                t = float(np.clip(s["slot"] + g.normal(0, 22), 8.5 * 60, 17.95 * 60))
                if s["kind"] in ("api", "b2b"):
                    s["serial"] += int(g.integers(1, 4))
                    master = tracking(s["serial"])
                elif s["kind"] == "legacy":
                    legacy_serial[0] += int(g.integers(1, 30))
                    master = "KW%09dPL" % legacy_serial[0]
                else:
                    market_stock[o] += int(g.integers(1, 3))
                    master = tracking(market_stock[o])
                labels = [master + "%03d" % (i + 1) for i in range(n)] if s["kind"] == "b2b" else [master]
                ref = _ref(g, s) if s["kind"] == "marketplace" else ""
                sh = {"sid": sid, "shipper": s["account"], "kind": s["kind"], "origin": o, "dest": dst,
                      "day": day, "master": master, "pieces": n, "ref": ref, "collected": n, "pick_min": t}
                shipments.append(sh)
                sid += 1
                for lab in labels:
                    parcels.append({"pid": pid, "sid": sh["sid"], "label": lab, "night": day, "origin": o,
                                    "dest": dst, "pick_min": t + g.uniform(0, 2.5), "shipper": s["account"],
                                    "kind": s["kind"], "ref": ref})
                    pid += 1
                made += n
    _route(seed, parcels)
    _unload(seed, parcels)
    _deliver(seed, parcels)
    _trailer_collections(seed, shipments, parcels, shp)
    pre = _preadvice(seed, shipments, shp, days)
    _order_refs(seed, shipments, parcels, pre, shp)
    events = _courier(seed, parcels, shp, pre)
    return {"parcels": parcels, "nights": NIGHTS, "days": days, "shippers": shp, "shipments": shipments,
            "courier": events, "preadvice": pre}


MARKETS = ("ALG", "OLX", "EMP", "SHP", "VNT")


def market_ref(mk, acct, day, seq):
    """a marketplace order number as the marketplace writes it"""
    if mk == "ALG":
        return "ALG-%s-%s%05d" % (acct[-4:], day.strftime("%Y%m%d"), seq % 100000)
    if mk == "SHP":
        return "SHP-%s-%s-%04d" % (acct[-4:], day.strftime("%Y%m%d"), seq % 10000)
    if mk == "EMP":
        return "EMP/%s/%06d" % (day.strftime("%y%m%d"), seq % 1000000)
    if mk == "OLX":
        return "OLX%09d" % (seq % 10 ** 9)
    return "VNT%s" % seq


def _order_refs(seed, shipments, parcels, pre, shp):
    """each marketplace seller's order numbers for a day, collected and uncollected orders numbered together"""
    g = np.random.default_rng([seed, 0, 11])
    mk, seq = {}, {}
    for s in shp:
        if s["kind"] != "marketplace":
            continue
        mk[s["account"]] = MARKETS[int(g.choice(5, p=[0.38, 0.17, 0.12, 0.23, 0.10]))]
        seq[s["account"]] = int(g.integers(1000, 60000))
    glob = {"OLX": int(g.integers(4 * 10 ** 8, 5 * 10 ** 8)), "EMP": int(g.integers(30000, 90000))}  # one numbering per marketplace
    alnum = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
    items = {}
    for sh in shipments:
        if sh["kind"] == "marketplace":
            items.setdefault((sh["shipper"], sh["day"]), []).append(("s", sh))
    for ln in pre:
        if ln["kind"] == "marketplace" and not ln["collected"]:
            items.setdefault((ln["shipper"], ln["date"]), []).append(("p", ln))
    for (acct, day), v in sorted(items.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        order = list(range(len(v)))
        g.shuffle(order)
        for i in order:
            m = mk[acct]
            if m in ("ALG", "SHP"):
                seq[acct] += int(g.integers(1, 4))
                ref = market_ref(m, acct, day, seq[acct])
            elif m in glob:
                glob[m] += int(g.integers(1, 40))
                ref = market_ref(m, acct, day, glob[m])
            else:
                ref = market_ref("VNT", acct, day, "".join(alnum[int(g.integers(0, 33))] for _ in range(16)))
            v[i][1]["ref"] = ref
    by_sid = {sh["sid"]: sh["ref"] for sh in shipments if sh["kind"] == "marketplace"}
    for p in parcels:
        if p["kind"] == "marketplace":
            p["ref"] = by_sid[p["sid"]]
    for ln in pre:
        if ln["kind"] == "marketplace" and ln["collected"]:
            ln["ref"] = by_sid[ln["sid"]]
    for s in shp:
        s["market"] = mk.get(s["account"])


def _trailer_collections(seed, shipments, parcels, shp):
    """the largest label-printing shippers at each depot load a trailer on some days: the trailer goes to the hub and
    the parcels are never scanned at collection"""
    g = np.random.default_rng([seed, 0, 10])
    bulk_days = {}
    for d in DEPOTS:
        cand = sorted([s for s in shp if s["depot"] == d and s["kind"] in ("api", "b2b")],
                      key=lambda s: (-s["weight"], s["account"]))[:2]
        for s in cand:
            s["trailer"] = True
            bulk_days[s["account"]] = float(g.uniform(0.22, 0.45))
    flag = {}
    for sh in sorted(shipments, key=lambda x: x["sid"]):
        key = (sh["shipper"], sh["day"])
        if sh["shipper"] in bulk_days and key not in flag:
            flag[key] = bool(g.random() < bulk_days[sh["shipper"]])
        sh["bulk"] = flag.get(key, False)
    by_sid = {sh["sid"]: sh["bulk"] for sh in shipments}
    for p in parcels:
        p["bulk"] = by_sid[p["sid"]]


def _ref(g, s):
    n = int(g.integers(16, 27))
    head = "%s-%s-" % (["ALG", "OLX", "EMP", "SHP", "VNT"][int(g.integers(0, 5))], s["account"][-4:])
    body = "".join("0123456789ABCDEFGHJKLMNPRSTUVWXYZ"[int(g.integers(0, 33))] for _ in range(max(4, n - len(head))))
    return (head + body)[:n]


NIGHTS = {}


def _route(seed, parcels):
    by_night = {}
    for p in parcels:
        by_night.setdefault(p["night"], []).append(p)
    NIGHTS.clear()
    for k, (night, ps) in enumerate(sorted(by_night.items())):
        g = np.random.default_rng([seed, k, 2])
        for p in ps:
            p["plan_hub"] = plan_hub(p["dest"], night)
            p["hub"] = p["plan_hub"]
            p["flex"] = False
        waw = [p for p in ps if p["plan_hub"] == "HWAW"]
        over = len(waw) - P.WAW_CAPACITY
        flex_n = 0
        if over > 0:
            over = int(math.ceil(over / P.CAGE) * P.CAGE)   # linehaul control moves the overflow in whole roll cages
            movable = [p for p in waw if p["origin"] not in P.FLEX_ORIGINS_EXCLUDE]
            by_o = {}
            for p in movable:
                by_o.setdefault(p["origin"], []).append(p)
            tot = len(movable)
            shares = {o: over * len(v) / tot for o, v in by_o.items()}
            alloc = {o: int(math.floor(s)) for o, s in shares.items()}
            rest = over - sum(alloc.values())
            for o in sorted(shares, key=lambda o: (-(shares[o] - alloc[o]), o))[:rest]:
                alloc[o] += 1
            for o, v in sorted(by_o.items()):
                v = sorted(v, key=lambda p: (p["pick_min"], p["pid"]))
                for p in v[len(v) - alloc[o]:]:
                    p["hub"] = "HLDZ"
                    p["flex"] = True
                    flex_n += 1
        util = min(1.0, (len(waw) - flex_n) / P.WAW_CAPACITY)
        rate = {h: HUB_BASE[h] * g.uniform(0.86, 1.14) for h in HUB_BASE}
        rate["HWAW"] = waw_miss(util) * g.uniform(0.92, 1.08)
        manual = P.MANUAL_MISS * g.uniform(0.9, 1.1)
        for p in ps:
            q = manual if p["flex"] else rate[p["hub"]]
            p["scanned"] = bool(g.random() >= q)
            p["recirc"] = bool(p["scanned"] and not p["flex"] and g.random() < 0.019)
            base = 22.2 * 60 if p["hub"] != "HLDZ" or not p["flex"] else 22.9 * 60
            p["sort_min"] = float(base + g.uniform(0, 250))       # minutes after the night's midnight-minus-24h
        NIGHTS[night] = {"waw_planned": len(waw), "flex": flex_n, "util": util, "waw_rate": rate["HWAW"],
                         "manual_rate": manual, "rates": rate}


def _unload(seed, parcels):
    by_night = {}
    for p in parcels:
        by_night.setdefault(p["night"], []).append(p)
    for k, (night, ps) in enumerate(sorted(by_night.items())):
        g = np.random.default_rng([seed, k, 3])
        day = unload_day(night)
        by_d = {}
        for p in ps:
            by_d.setdefault(p["dest"], []).append(p)
        for dest in DEPOTS:
            v = by_d.get(dest, [])
            code = depot_code(dest, day)
            door_main = ["B1", "B2"][int(g.integers(0, 2))]
            main = [p for p in v if not p["flex"]]
            flex = [p for p in v if p["flex"]]
            hub = plan_hub(dest, night)
            t0 = HUB_ARRIVE[hub] + g.normal(0, 7)
            end = _burst(g, main, day, code, door_main, t0, "%s/%s/%s" % (night.isoformat(), dest, hub))
            if flex:
                t1 = max(6 * 60 + 5, end + 32) + g.uniform(0, 11)
                door_flex = "B2" if door_main == "B1" else "B1"
                _burst(g, flex, day, code, door_flex, t1, "%s/%s/HLDZ" % (night.isoformat(), dest))


def _burst(g, ps, day, code, door, t0, trailer):
    if not ps:
        return t0
    order = sorted(ps, key=lambda p: p["pid"])
    g.shuffle(order)
    t = t0 + g.uniform(4, 9)
    mean_gap = g.uniform(3.6, 5.4)
    for p in order:
        t += (1.5 + min(40.0, g.exponential(mean_gap))) / 60.0
        p["arr_day"] = day
        p["arr_min"] = t
        p["depot_code"] = code
        p["door"] = "%s-%s" % (code, door)
        p["trailer"] = trailer
    return t


def next_delivery_day(day):
    d = day + dt.timedelta(days=1)
    while d.weekday() in (6, 0):
        d += dt.timedelta(days=1)
    return d


AFTERNOON_WAVE = ("D-POZ1", "D-WRO1", "D-KTW1", "D-KRK1", "D-LDZ1", "D-WAW1", "D-WAW2")   # depots running a second wave


def _deliver(seed, parcels):
    by_night = {}
    for p in parcels:
        by_night.setdefault(p["night"], []).append(p)
    for k, (night, ps) in enumerate(sorted(by_night.items())):
        g = np.random.default_rng([seed, k, 4])
        h = np.random.default_rng([seed, k, 14])
        for p in ps:
            day = p["arr_day"]
            p["fail_first"] = bool(g.random() < 0.036)
            p["ofd_min"] = float(g.uniform(7.3 * 60, 8.7 * 60))
            p["try_min"] = float(np.clip(g.normal(12.6 * 60, 130), 9.0 * 60, 18.4 * 60))
            p["deliv_day"] = next_delivery_day(day) if p["fail_first"] else day
            p["ofd2_min"] = float(g.uniform(7.3 * 60, 8.7 * 60))
            p["deliv_min"] = float(np.clip(g.normal(12.8 * 60, 130), 9.0 * 60, 18.6 * 60))
            # a parcel taken off the first loop and loaded again on the courier's second loop that morning
            p["reload_min"] = None
            if h.random() < 0.021:
                p["reload_min"] = p["ofd_min"] + float(h.uniform(48, 175))
                first = p["try_min"] if p["fail_first"] else p["deliv_min"]
                if first < p["reload_min"] + 15:
                    shift = p["reload_min"] + float(h.uniform(15, 80)) - first
                    if p["fail_first"]:
                        p["try_min"] += shift
                    else:
                        p["deliv_min"] = min(18.9 * 60, p["deliv_min"] + shift)
            # a failed morning attempt taken out again on the afternoon wave the same day
            p["same_day"] = bool(p["fail_first"] and p["dest"] in AFTERNOON_WAVE and p["try_min"] < 12.4 * 60
                                 and h.random() < 0.55)
            if p["same_day"]:
                p["deliv_day"] = day
                p["ofd2_min"] = max(p["try_min"] + float(h.uniform(35, 95)), 12.9 * 60 + float(h.uniform(0, 40)))
                p["deliv_min"] = p["ofd2_min"] + float(h.uniform(22, 150))


def _courier(seed, parcels, shp, pre):
    """the couriers' handheld events, each with its true local time; a re-send copies an event the platform had
    already received, stamped as the app's queue holds it (TC52: local time cut to the minute; TC51: UTC cut to the
    minute), with the sync it went out on"""
    g = np.random.default_rng([seed, 0, 5])
    couriers = {}
    serials = set()
    for d in DEPOTS:
        n = int(g.integers(14, 23))
        old = float(g.uniform(0.55, 0.75) if d in OLD_FLEET else g.uniform(0.15, 0.32))
        models = ["TC51" if g.random() < old else "TC52" for _ in range(n)]
        models[0], models[1], models[2], models[3] = "TC51", "TC51", "TC52", "TC52"   # every depot runs both
        cs = []
        for i, model in enumerate(models):
            sn = int(g.integers(10000, 99999))
            while sn in serials:
                sn = int(g.integers(10000, 99999))
            serials.add(sn)
            cs.append({"courier": "%s-K%02d" % (d[2:].replace("-", ""), i + 1),
                       "device": "%s%05d" % ("51" if model == "TC51" else "52", sn), "model": model})
        perm = list(range(n))
        g.shuffle(perm)
        couriers[d] = [cs[i] for i in perm]
    resend = {d: float(g.uniform(0.008, 0.026)) for d in DEPOTS}
    ev = []
    for p in sorted(parcels, key=lambda p: p["pid"]):
        o = p["origin"]
        c = couriers[o][p["pid"] % len(couriers[o])]
        if not p["bulk"]:
            ev.append(_ev(p, "PICKUP", p["night"], p["pick_min"], o, c))
        dd = p["dest"]
        c2 = couriers[dd][(p["pid"] * 7) % len(couriers[dd])]
        ev.append(_ev(p, "OUT_FOR_DELIVERY", p["arr_day"], p["ofd_min"], dd, c2))
        if p["reload_min"] is not None:
            ev.append(_ev(p, "OUT_FOR_DELIVERY", p["arr_day"], p["reload_min"], dd, c2))
        if p["fail_first"]:
            ev.append(_ev(p, "ATTEMPT", p["arr_day"], p["try_min"], dd, c2))
            ev.append(_ev(p, "OUT_FOR_DELIVERY", p["deliv_day"], p["ofd2_min"], dd, c2))
        ev.append(_ev(p, "DELIVERED", p["deliv_day"], p["deliv_min"], dd, c2))
    # a courier who called for a pre-advised consignment and found nothing ready records the failed collection
    # against the number on the pickup list
    h = np.random.default_rng([seed, 0, 12])
    slot = {s["account"]: s["slot"] for s in shp}
    for ln in pre:
        if ln["collected"] or not ln["master"] or h.random() >= 0.36:
            continue
        o = ln["depot"]
        c = couriers[o][int(h.integers(0, len(couriers[o])))]
        minute = float(np.clip(slot[ln["shipper"]] + h.normal(0, 25), 8.5 * 60, 18.2 * 60))
        ev.append({"label": ln["master"], "type": "PICKUP_FAILED", "day": ln["date"], "min": minute, "depot": o,
                   "courier": c["courier"], "device": c["device"], "model": c["model"], "ref": "", "pid": None})
    copies = []
    for e in ev:
        if g.random() < resend[e["depot"]]:
            lag = float(g.uniform(9, 150))
            copies.append(dict(e, copy=True, sync_lag=lag))
    for e in ev:
        e["copy"] = False
        e["sync_lag"] = float(g.exponential(0.6))
    return {"events": ev + copies, "couriers": couriers}


def _ev(p, kind, day, minute, depot, c):
    return {"label": p["label"], "type": kind, "day": day, "min": minute, "depot": depot,
            "courier": c["courier"], "device": c["device"], "model": c["model"],
            "ref": p["ref"] if kind == "PICKUP" else "", "pid": p["pid"]}


def _preadvice(seed, shipments, shp, days):
    """the shippers' EDI pre-advices: one line per consignment as each shipper's system sends it, a later version
    where a shipper corrected one, and the consignments pre-advised that the depot never collected"""
    g = np.random.default_rng([seed, 0, 6])
    kind = {s["account"]: s for s in shp}
    lines = []
    cons = 7700000 + int(g.integers(0, 90000))
    for sh in shipments:
        if sh["kind"] == "legacy" and g.random() < 0.5:
            continue                                   # half the legacy range still arrives without a pre-advice
        if sh["kind"] == "api" and g.random() < 0.028:
            continue                                   # labels printed in the web panel, never pre-advised
        cons += int(g.integers(1, 9))
        n = sh["pieces"]
        short = 0
        if sh["kind"] == "b2b" and n >= 2 and g.random() < 0.13:
            short = int(min(n - 1, 1 + (g.random() < 0.3)))
        lines.append({"cons": "C%08d" % cons, "shipper": sh["shipper"], "kind": sh["kind"], "depot": sh["origin"],
                      "date": sh["day"], "master": sh["master"] if sh["kind"] != "marketplace" else "",
                      "pieces": n + short, "short": short, "ref": sh["ref"], "collected": True, "sid": sh["sid"]})
    # consignments pre-advised that never came to the courier
    accts = [s for s in shp]
    for day in days:
        for s in accts:
            lam = 0.22 * s["weight"]
            for _ in range(int(g.poisson(lam))):
                cons += int(g.integers(1, 9))
                n = 1
                if s["kind"] == "b2b" and g.random() < 0.4:
                    n = int(min(6, 2 + g.geometric(0.55) - 1))
                if s["kind"] in ("api", "b2b"):
                    s["serial"] += int(g.integers(1, 4))
                    master = tracking(s["serial"])
                elif s["kind"] == "legacy":
                    master = "KW%09dPL" % int(g.integers(10 ** 8, 9 * 10 ** 8))
                else:
                    master = ""
                ref = ""                                   # marketplace order numbers come from _order_refs
                lines.append({"cons": "C%08d" % cons, "shipper": s["account"], "kind": s["kind"],
                              "depot": s["depot"], "date": day, "master": master, "pieces": n, "short": n,
                              "ref": ref, "collected": False, "sid": None})
    return lines
