"""The reliability figures on the clean truth: who each interruption reached, its customer minutes, the major
event days, and each feeder's indices for the reporting window. The golden recomputes all of it from the pack."""
import collections
import datetime as dt

import world as W
import sim

FIVE_MIN = 5 * sim.MS_MIN
CEMI_N = 2


class Reach:
    """Service points downstream of a device on a date, through the register's history."""

    def __init__(self, net):
        self.net = net
        self.cache = {}
        self.sp_by_t = collections.defaultdict(list)
        for sp, v in net["sps"].items():
            self.sp_by_t[v["transformer"]].append(sp)
        for k in self.sp_by_t:
            self.sp_by_t[k].sort()
        self.moves = sorted({L["moved"]["date"] for L in net["laterals"].values() if L["moved"]})

    def regime(self, day):
        return tuple(m <= day for m in self.moves)

    def _down(self, key, day):
        if key not in self.cache:
            net = self.net
            down = collections.defaultdict(list)
            for tid in sorted(net["transformers"]):
                for dvc in W.chain(net, net["transformers"][tid]["device"], day):
                    down[dvc].append(tid)
            self.cache[key] = down
        return self.cache[key]

    def transformers(self, dev, day):
        if dev in self.net["transformers"]:
            return [dev]
        return self._down(self.regime(day), day).get(dev, [])

    def sps(self, dev, day):
        """Active service points downstream of a device (or a transformer, or one service point) on a date."""
        net = self.net
        if dev in net["sps"]:
            v = net["sps"][dev]
            return [dev] if active(v, day) else []
        out = []
        for tid in self.transformers(dev, day):
            for sp in self.sp_by_t[tid]:
                if active(net["sps"][sp], day):
                    out.append(sp)
        return out


def active(v, day):
    return v["connected"] <= day and (v["disconnected"] is None or v["disconnected"] > day)


def sp_feeder(net, sp, day):
    T = net["transformers"][net["sps"][sp]["transformer"]]
    return W.device_feeder(net, T["device"], day)


def outage_feeder(net, o):
    dev = o["device"]
    if dev in net["sps"]:
        return sp_feeder(net, dev, o["day"])
    if dev in net["transformers"]:
        return W.device_feeder(net, net["transformers"][dev]["device"], o["day"])
    return W.device_feeder(net, dev, o["day"])


def step_counts(o, n):
    """Customers restored at each step of a stepped restoration: integers summing to n."""
    if not o["steps"]:
        return [(o["restore"], n)]
    out, left = [], n
    for t, frac in o["steps"]:
        k = int(round(frac * left))
        out.append((t, k))
        left -= k
    out.append((o["restore"], left))
    return out


def begun(o):
    """When a customer's interruption began: a continuation began with the outage it carries on."""
    while o.get("continues"):
        o = o["continues"]
    return o["start"]


def compute(net, S):
    R = Reach(net)
    outs = S["outages"]
    # who each sustained interruption reached, net of customers already without supply
    reach = []
    for i, o in enumerate(outs):
        sps = set(R.sps(o["device"], o["day"]))
        already = set()
        for j, p in enumerate(outs):
            if j == i or not (p["start"] < o["start"] < p["restore"]):
                continue
            if p["device"] == o["device"]:
                continue
            already |= sps & set(R.sps(p["device"], p["day"]))
        hit = sps - already
        reach.append(dict(all=len(sps), hit=hit, already=len(already)))
    for i, o in enumerate(outs):
        if o.get("continues"):
            reach[i]["hit"] = set()
    for i, o in enumerate(outs):
        n_all = reach[i]["all"]
        steps = step_counts(o, n_all)
        o["step_counts"] = steps
        n_hit = len(reach[i]["hit"])
        if o["steps"]:
            assert n_hit == n_all, ("a stepped restoration reached customers already out", i)
            cmi = sum(k * (t - o["start"]) / sim.MS_MIN for t, k in steps)
        elif o.get("continues"):
            cmi = n_all * (o["restore"] - o["start"]) / sim.MS_MIN
        else:
            cmi = n_hit * (o["restore"] - o["start"]) / sim.MS_MIN
        o["n_all"], o["n_hit"], o["cmi"] = n_all, n_hit, cmi
        o["feeder"] = outage_feeder(net, o)
    n_sys = sum(1 for v in net["sps"].values() if active(v, dt.date(2025, 12, 31)))
    daily = collections.defaultdict(float)
    for o in outs:
        daily[sim.local_day(begun(o))] += o["cmi"]
    saidi_day = {d: v / n_sys for d, v in daily.items()}
    meds = sorted(d for d, v in saidi_day.items() if d.year == 2026 and v > W.T_MED_2026)
    # momentary interruption events: each device's operations within five minutes of the first are one event
    ev = []
    by_dev = collections.defaultdict(list)
    for op in S["ops"]:
        by_dev[op["device"]].append(op)
    for dev, ops in by_dev.items():
        ops.sort(key=lambda o: o["t"])
        k = 0
        while k < len(ops):
            first = ops[k]
            grp = [first]
            k += 1
            while k < len(ops) and ops[k]["t"] - first["t"] <= FIVE_MIN:
                grp.append(ops[k])
                k += 1
            locked = [g for g in grp if g["lockout"]]
            if locked and not (locked[-1].get("test_close") and locked[-1]["test_close"] - first["t"] <= FIVE_MIN):
                continue
            ev.append(dict(device=dev, t=first["t"], day=first["day"], ops=grp, feeder=first["feeder"]))
    ev.sort(key=lambda e: e["t"])
    starts = sorted((o["start"], i) for i, o in enumerate(outs))
    dark = [set(R.sps(o["device"], o["day"])) if o.get("continues") else reach[i]["hit"] for i, o in enumerate(outs)]
    import bisect
    keys = [s for s, _ in starts]
    for e in ev:
        sps = set(R.sps(e["device"], e["day"]))
        out_now = set()
        absorbed = set()
        lo = bisect.bisect_left(keys, e["t"] - 40 * sim.MS_DAY)
        hi = bisect.bisect_right(keys, e["t"] + FIVE_MIN)
        em = sim.minute_floor(e["t"])
        for s, i in starts[lo:hi]:
            o = outs[i]
            if o["start"] < em and e["t"] < o["restore"]:
                out_now |= sps & dark[i]
            elif em <= o["start"] <= e["t"] + FIVE_MIN:
                absorbed |= sps & dark[i]
        e["n_all"] = len(sps)
        e["n_out"] = len(out_now)
        e["n_abs"] = len(absorbed - out_now)
        e["set"] = sps - out_now - absorbed
    # a customer's momentary interruptions within five minutes of the first are one event, whichever devices
    opened = {}
    for e in ev:
        n = 0
        for c in e["set"]:
            t0 = opened.get(c)
            if t0 is None or e["t"] - t0 > FIVE_MIN:
                opened[c] = e["t"]
                n += 1
        e["n"] = n
        e["n_merged"] = len(e["set"]) - n
        del e["set"]
    # the reporting window and the indices
    end = W.REP1
    nt = collections.Counter()
    for sp, v in net["sps"].items():
        if active(v, end):
            nt[sp_feeder(net, sp, end)] += 1
    medset = set(meds)

    def counted(day):
        return W.REP0 <= day <= W.REP1 and day not in medset

    ci = collections.Counter()
    cmi = collections.Counter()
    per_sp = collections.Counter()
    for i, o in enumerate(outs):
        d = sim.local_day(begun(o))
        if not counted(d):
            continue
        ci[o["feeder"]] += o["n_hit"]
        cmi[o["feeder"]] += o["cmi"]
        for sp in reach[i]["hit"]:
            per_sp[sp] += 1
    mom = collections.Counter()
    for e in ev:
        if counted(sim.local_day(e["t"])):
            mom[e["feeder"]] += e["n"]
    cemi = collections.Counter()
    for sp, v in net["sps"].items():
        if active(v, end) and per_sp[sp] > CEMI_N:
            cemi[sp_feeder(net, sp, end)] += 1
    idx = {}
    for f in W.FID:
        idx[f] = dict(nt=nt[f], saifi=ci[f] / nt[f], saidi=cmi[f] / nt[f], maifi=mom[f] / nt[f], cemi=cemi[f],
                      ci=ci[f], cmi=cmi[f], mom=mom[f])
    return dict(outages=outs, reach=reach, events=ev, saidi_day=saidi_day, meds=meds, n_sys=n_sys, idx=idx,
                per_sp=per_sp, nt=nt)
