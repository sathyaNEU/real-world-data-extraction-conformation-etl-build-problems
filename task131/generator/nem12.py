"""task131 generator: the meter data agent's NEM12 files, one per month, as the load research team pulled them.

Each file carries every trial premise's registers for the month's days: E1 general supply, E2 controlled-load hot
water where fitted, B1 export where rooftop PV is connected. Reads are kWh per interval, intervals numbered from
midnight AWST, 30-minute meters with 48 values and a few 15-minute meters with 96. Days whose reads were
estimated or substituted when a meter did not communicate arrive again in a later file with actual reads and a
later update time. A meter exchange (a rooftop PV installation, or a fault) starts a new 200 block under the new
serial; the exchange day is read by the old meter up to the exchange and by the new meter after it."""
from datetime import datetime, timedelta

import numpy as np

import params as P
import weather as WX

PULLED = {11: datetime(2025, 12, 5, 8, 14), 12: datetime(2026, 1, 6, 8, 9), 1: datetime(2026, 2, 5, 8, 22),
          2: datetime(2026, 3, 10, 8, 3)}
FILES = {11: "MRP_NEM12_202511.csv", 12: "MRP_NEM12_202512.csv", 1: "MRP_NEM12_202601.csv", 2: "MRP_NEM12_202602.csv"}
HOT = set(WX.HOT_WORKDAYS)


def _fmt(v):
    if v <= 0.0:
        return "0"
    s = "%.3f" % v
    return s


def plan(hh, loads, meta, exch, newp, occ, seed):
    """the meter streams: for every premise key the NMI, the serial by day, the interval length, registers, the
    re-sent days and their estimated stand-ins, and the V days"""
    rng = np.random.default_rng(seed)
    streams = []
    resend = {}
    for key, L in loads.items():
        kind, nmi = key
        m = meta[key]
        i = m["hh"]
        if kind == "occ":
            continue                      # the occupant's reads are spliced onto the trial NMI below
        serial = hh["serial"][i] if m["role"] == "trial" else None
        streams.append({"key": key, "nmi": nmi, "i": i, "role": m["role"], "from": m.get("from", 0),
                        "len": 15 if m["role"] == "new_premise" else 30, "serial": serial})
    # re-sent days: estimated first, actual later; never on a hot workday or the days either side
    avoid = set()
    for d in WX.HOT_WORKDAYS:
        avoid.update({d - timedelta(1), d, d + timedelta(1)})
    days = [d for d in P.DAYS if d not in avoid and d <= P.DATA_TO - timedelta(12)]
    for s in streams:
        if s["role"] != "trial":
            continue
        xd = exch.get(s["i"], {}).get("date")
        k = rng.poisson(0.55)
        for _ in range(k):
            d = days[int(rng.integers(0, len(days)))]
            if d == xd or (s["i"] in occ and d >= occ[s["i"]]["date"]):
                continue
            resend[(s["nmi"], d)] = {"est_factor": float(rng.uniform(0.82, 1.18)), "lag": int(rng.integers(3, 9)),
                                     "partial": bool(rng.random() < 0.35), "a": int(rng.integers(8, 30)),
                                     "b": int(rng.integers(31, 47)), "method": ["E52", "S53", "E56"][int(rng.integers(0, 3))]}
    return streams, resend


def write(path, month, hh, loads, meta, exch, newp, occ, streams, resend, dates_by_month):
    """one month's file: the month's days as first delivered, then every re-send the meter data agent received
    since the previous pull (a February day can come twice in the February file)"""
    pulled = PULLED[month]
    since = {11: datetime(2025, 11, 1), 12: PULLED[11], 1: PULLED[12], 2: PULLED[1]}[month]
    lines = ["100,NEM12,%s,MRPMDP,MRPLR" % pulled.strftime("%Y%m%d%H%M")]
    mdays = dates_by_month[month]
    for s in sorted(streams, key=lambda x: x["nmi"]):
        i = s["i"]
        L = loads[s["key"]]
        regs = [("E1", L["E1"])]
        if L["E2"] is not None:
            regs.append(("E2", L["E2"]))
        if L["B1"] is not None:
            regs.append(("B1", L["B1"]))
        conf = "".join(r for r, _ in regs)
        ex = exch.get(i) if s["role"] == "trial" else None
        for reg, arr in regs:
            for serial, ilen, dlist in _blocks(s, ex, reg, mdays, i, hh, newp, occ):
                if not dlist:
                    continue
                lines.append("200,%s,%s,%s,%s,N%s,%s,KWH,%d," % (s["nmi"], conf, {"E1": 1, "E2": 2, "B1": 3}[reg], reg,
                                                                 {"E1": "1", "E2": "2", "B1": "3"}[reg], serial, ilen))
                for d, part in dlist:
                    lines.extend(_day(s, reg, arr, d, part, ilen, ex, resend, loads, i, occ, pulled, first=True))
        if s["role"] != "trial":
            continue
        for d in [x for x in P.DAYS if x <= mdays[-1]]:
            rs = resend.get((s["nmi"], d))
            if not rs:
                continue
            stamp = datetime(d.year, d.month, d.day) + timedelta(days=rs["lag"], hours=14,
                                                                 minutes=(int(s["nmi"][4:]) * 7 + d.toordinal()) % 271)
            if not (since < stamp <= pulled):
                continue
            serial = _serial_on(s, ex, d, hh)
            lines.append("200,%s,%s,1,E1,N1,%s,KWH,%d," % (s["nmi"], conf, serial, s["len"]))
            lines.extend(_day(s, "E1", L["E1"], d, None, s["len"], ex, None, loads, i, occ, pulled, first=False,
                              stamp=stamp))
    lines.append("900")
    with open(path, "w", newline="") as fh:
        fh.write("\r\n".join(lines) + "\r\n")


def _serial_on(s, ex, d, hh):
    if s["role"] != "trial":
        return s["serial_new"] if s.get("serial_new") else _new_serial(s)
    if ex and d > ex["date"]:
        return _xserial(hh["serial"][s["i"]])
    return hh["serial"][s["i"]]


def _xserial(old):
    return "2118" + old[4:][::-1]


def _new_serial(s):
    return "2117" + s["nmi"][4:]


def _blocks(s, ex, reg, mdays, i, hh, newp, occ):
    """(serial, interval length, [(day, part)]) blocks for one register in one month; part is None for a whole day
    or ('old', cut) / ('new', cut) on an exchange day"""
    if s["role"] == "new_premise":
        start = P.DAYS[s["from"]]
        dl = [(d, None) for d in mdays if d >= start]
        return [(_new_serial(s), s["len"], dl)]
    old = hh["serial"][i]
    ilen = s["len"]
    if not ex:
        return [(old, ilen, [(d, None) for d in mdays])]
    xd = ex["date"]
    new = _xserial(old)
    if reg == "B1" and ex["why"] == "PV":
        return [(new, 30, [(d, None if d > xd else ("new", ex["cut"])) for d in mdays if d >= xd])]
    a = [(d, None if d < xd else ("old", ex["cut"])) for d in mdays if d <= xd]
    b = [(d, None if d > xd else ("new", ex["cut"])) for d in mdays if d >= xd]
    return [(old, ilen, a), (new, 30, b)]


def _vals(arr, j, ilen, rng_key):
    v = arr[j] * 0.5                      # average kW over the half-hour to kWh
    if ilen == 30:
        return v
    r = np.random.default_rng(rng_key)
    sp = np.clip(r.normal(0.5, 0.07, 48), 0.25, 0.75)
    out = np.empty(96)
    out[0::2] = v * sp
    out[1::2] = v * (1 - sp)
    return out


def _validated(nmi, d):
    """when Metering Services validated a day's reads: the meter's read route sets the hour, the night's queue the
    minute"""
    route = int(nmi[-3:]) % 23
    queue = (int(nmi[4:]) * 31 + d.toordinal() * 17) % 11
    return datetime(d.year, d.month, d.day) + timedelta(days=1, hours=1, minutes=10 + 12 * route + queue)


def _day(s, reg, arr, d, part, ilen, ex, resend, loads, i, occ, pulled, first=True, stamp=None):
    j = (d - P.DATA_FROM).days
    # the trial NMI's reads after the household left belong to the new occupant
    use = arr
    if s["role"] == "trial" and i in occ and d >= occ[i]["date"]:
        use = loads[("occ", s["nmi"])][reg] if loads[("occ", s["nmi"])][reg] is not None else arr * 0
    key = int(s["nmi"][4:]) * 1000 + j * 3 + {"E1": 0, "E2": 1, "B1": 2}[reg]
    v = np.array(_vals(use, j, ilen, key), dtype=float)
    nint = 96 if ilen == 15 else 48
    q, recs = "A", []
    rs = resend.get((s["nmi"], d)) if (resend is not None and reg == "E1" and s["role"] == "trial" and part is None) else None
    upd = _validated(s["nmi"], d) if stamp is None else stamp
    if rs is not None and first:
        if rs["partial"]:
            k0, k1 = rs["a"] * (nint // 48), rs["b"] * (nint // 48)
            v[k0:k1] = np.round(v[k0:k1] * rs["est_factor"], 3)
            q = "V"
            recs = ["400,1,%d,A,,," % k0, "400,%d,%d,%s,,," % (k0 + 1, k1, rs["method"]), "400,%d,%d,A,,," % (k1 + 1, nint)]
        else:
            v = np.round(v * rs["est_factor"], 3)
            q = rs["method"]
        upd = _validated(s["nmi"], d)
    if part is not None:
        side, cut = part
        k = cut * (nint // 48)
        if side == "old":
            v[k:] = 0.0
            q = "V"
            recs = ["400,1,%d,A,,," % k, "400,%d,%d,N,,," % (k + 1, nint)]
        else:
            v[:k] = 0.0
            q = "V"
            recs = ["400,1,%d,N,,," % k, "400,%d,%d,A,,," % (k + 1, nint)]
    body = ",".join(_fmt(x) for x in v)
    msats = upd + timedelta(minutes=12 + 7 * (int(s["nmi"][-2:]) % 5))
    line = "300,%s,%s,%s,,,%s,%s" % (d.strftime("%Y%m%d"), body, q, upd.strftime("%Y%m%d%H%M%S"), msats.strftime("%Y%m%d%H%M%S"))
    return [line] + recs
