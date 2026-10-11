"""Simulate the fleet, its firmware history, the week's interval reads and the MDM deliveries.

Everything is generated forward from installations, meters and communications events; no figure is
authored. The MDM rows, the head-end history and the register are views of one simulated world.
"""
import datetime as dt
import hashlib

import numpy as np

import world as W


def rng(name):
    h = int(hashlib.sha256(("%d:%s" % (W.SEED, name)).encode()).hexdigest()[:16], 16)
    return np.random.default_rng(h)


def nmi_checksum(nmi):
    """AEMO NMI checksum: double the ASCII value of every second character from the right, sum
    the digits of every value, and take the distance to the next multiple of ten."""
    total, double = 0, True
    for ch in reversed(nmi):
        v = ord(ch) * (2 if double else 1)
        double = not double
        total += sum(int(d) for d in str(v))
    return str((10 - total % 10) % 10)


# ------------------------------------------------------------------ the fleet

class Inst:
    __slots__ = ("nmi", "profile", "group", "build_start", "build_end", "meters", "move", "blocks",
                 "suburb", "postcode", "wave8", "exchange", "rows")

    def __init__(self, nmi, profile, group, b0, b1):
        self.nmi, self.profile, self.group = nmi, profile, group
        self.build_start, self.build_end = b0, b1
        self.meters = []          # [(serial, model, module, installed_local, removed_local)]
        self.move = None          # dict for a Wave 7 move
        self.blocks = []          # [(start_slot, end_slot, cls)] cls 1 precut, 2 post, 3 never
        self.exchange = None
        self.wave8 = None


SUBURBS = [("Penrith", "2750"), ("Blacktown", "2148"), ("Parramatta", "2150"), ("Liverpool", "2170"),
           ("Campbelltown", "2560"), ("Hornsby", "2077"), ("Gosford", "2250"), ("Wyong", "2259"),
           ("Maitland", "2320"), ("Cessnock", "2325"), ("Newcastle West", "2302"), ("Charlestown", "2290"),
           ("Wollongong", "2500"), ("Shellharbour", "2529"), ("Kiama", "2533"), ("Bathurst", "2795"),
           ("Orange", "2800"), ("Dubbo", "2830"), ("Goulburn", "2580"), ("Bowral", "2576"),
           ("Castle Hill", "2154"), ("Rouse Hill", "2155"), ("Kellyville", "2155"), ("Marsden Park", "2765"),
           ("Oran Park", "2570"), ("Camden", "2570"), ("Richmond", "2753"), ("Windsor", "2756"),
           ("Katoomba", "2780"), ("Springwood", "2777"), ("Raymond Terrace", "2324"), ("Port Stephens", "2317")]

MODEL = {"EM3": ["WG-1PH-E3a", "WG-1PH-E3b", "WG-3PH-E3"], "PX5": ["WG-1PH-P5", "WG-3PH-P5", "WG-CT-P5"]}


def make_fleet():
    r = rng("fleet")
    used_nmi, used_serial = set(), set()

    def new_nmi():
        while True:
            pre = "4103" if r.random() < 0.62 else "4310"
            n = pre + "%06d" % r.integers(0, 10 ** 6)
            if n not in used_nmi:
                used_nmi.add(n)
                return n

    def new_serial(module):
        while True:
            if module == "EM3":
                lead = "0" if r.random() < 0.38 else str(r.integers(1, 3))
            else:
                lead = str(r.integers(6, 8))
            s = lead + "%07d" % r.integers(0, 10 ** 7)
            if s not in used_serial:
                used_serial.add(s)
                return s

    insts = []

    def add(profile, group, b0, b1):
        i = Inst(new_nmi(), profile, group, b0, b1)
        sub = SUBURBS[r.integers(0, len(SUBURBS))]
        i.suburb, i.postcode = sub
        module = W.MODULE[b0]
        model = MODEL[module]
        cls = W.PROFILES[profile][2]
        m = model[2] if cls == "SME" else (model[1] if profile in W.HEAVY else model[0])
        y = int(r.integers(2019, 2026)) if module == "EM3" else int(r.integers(2021, 2026))
        inst_dt = dt.datetime(y, int(r.integers(1, 13)), int(r.integers(1, 28)), int(r.integers(8, 16)),
                              int(r.integers(0, 60)))
        i.meters.append([new_serial(module), m, module, inst_dt, None])
        insts.append(i)
        return i

    for b, mix in W.FULL_WEEK.items():
        for prof in sorted(mix):
            for _ in range(mix[prof]):
                add(prof, "full", b, b)
    for frm, to, mix, night in W.WAVE7:
        for prof in sorted(mix):
            for _ in range(mix[prof]):
                i = add(prof, "w7", frm, to)
                i.move = {"night": night}
    # mid-week meter exchanges on EM3.12.0 and EM3.11.4 installations
    for k in range(W.EXCHANGES):
        b0 = "EM3.12.0" if k % 3 else "EM3.11.4"
        prof = ["R30A", "R30B", "R30C", "R5B"][k % 4]
        i = add(prof, "exch", b0, "EM3.12.2")
        day = 3 + (k % 2)                      # Thursday 8 or Friday 9 October, local business hours
        t = dt.datetime(2026, 10, 5 + day, int(r.integers(9, 15)), int(r.integers(0, 60)), tzinfo=W.AEDT)
        i.exchange = t
        i.meters[0][4] = t.replace(tzinfo=None)
        i.meters.append([new_serial("EM3"), i.meters[0][1], "EM3", (t + dt.timedelta(minutes=int(r.integers(35, 80)))).replace(tzinfo=None), None])
    # the Tuesday movers off EM3.12.0 that failed, rolled back and went again on Wednesday
    tue = [i for i in insts if i.group == "w7" and i.move["night"] == "tue"]
    pick = r.choice(len(tue), W.WAVE7_ROLLBACK_RETRY, replace=False)
    for j in sorted(pick):
        tue[j].move["retry"] = True
    order = r.permutation(len(insts))
    return [insts[j] for j in order]


# ------------------------------------------------------------------ the week's communications

def slot_of(t):
    """5-minute slot index in the assessment week (market time) of an aware datetime."""
    return int((t - W.WEEK_START).total_seconds() // 60 // W.SLOT)


def night_window(r, night):
    """A Wave 7 activation time on the given local night, 23:30 to 03:30 AEDT."""
    d = {"tue": 6, "wed": 7}[night]
    start = dt.datetime(2026, 10, d, 23, 30, tzinfo=W.AEDT)
    return start + dt.timedelta(minutes=int(r.integers(0, 240)), seconds=int(r.integers(0, 60)))


# base communications behaviour and per-build departures from it
BASE = dict(gp=0.03, gdur=(20, 120), op=0.012, odur=(240, 2880))
BUILD_FX = {
    "EM3.10.9": dict(gp=0.15, op=0.07),
    "EM3.11.4": dict(gp=0.028, op=0.011),
    "EM3.12.0": dict(gp=0.074, op=0.029),
    "EM3.12.1": dict(light_extra=(0.17, 50, 115)),
    "EM3.12.2": dict(gp=0.025, op=0.009),
    "PX5.2.7": dict(drop=0.026),
    "PX5.3.0": dict(heavy_extra=(0.31, 40, 120)),
    "PX5.3.1": dict(gp=0.025, op=0.0),
}


def _cls(r, kind):
    u = r.random()
    if kind == "gap":
        return 1 if u < 0.12 else (2 if u < 0.50 else 3)
    if kind == "outage":
        return 2 if u < 0.25 else 3
    return 3


def comms_blocks(r, build, profile):
    p = dict(BASE)
    p.update({k: v for k, v in BUILD_FX.get(build, {}).items() if k in BASE})
    fx = BUILD_FX.get(build, {})
    out = []
    for d in range(W.DAYS):
        if r.random() < p["gp"]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(0, W.SLOTS_PER_DAY))
            dur = int(r.integers(p["gdur"][0], p["gdur"][1])) // W.SLOT + 1
            out.append((s, s + dur, _cls(r, "gap")))
        le = fx.get("light_extra")
        if le and profile not in W.HEAVY and r.random() < le[0]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(0, W.SLOTS_PER_DAY))
            out.append((s, s + int(r.integers(le[1], le[2])) // W.SLOT + 1, 3))
        he = fx.get("heavy_extra")
        if he and profile in W.HEAVY and r.random() < he[0]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(0, W.SLOTS_PER_DAY))
            out.append((s, s + int(r.integers(he[1], he[2])) // W.SLOT + 1, 3))
        if fx.get("drop") and r.random() < fx["drop"]:
            s = d * W.SLOTS_PER_DAY + int(r.integers(14 * 12, 18 * 12))
            out.append((s, (d + 1) * W.SLOTS_PER_DAY, 2))
    if r.random() < p["op"]:
        s = int(r.integers(0, W.WEEK_SLOTS))
        dur = int(np.exp(r.uniform(np.log(p["odur"][0]), np.log(p["odur"][1])))) // W.SLOT
        out.append((s, s + dur, _cls(r, "outage")))
    return out


def simulate():
    insts = make_fleet()
    for i in insts:
        salt = W.SALT.get(i.build_end if i.group != "full" else i.build_start, 0)
        r = rng("comms:%s:%d" % (i.nmi, salt))
        ra = rng("act:%s:%d" % (i.nmi, salt))
        if i.group == "full":
            i.blocks = comms_blocks(r, i.build_start, i.profile)
        elif i.group == "w7":
            t = night_window(ra, "wed" if i.move.get("retry") else i.move["night"])
            if i.move.get("retry"):
                t_fail = night_window(ra, "tue")
                i.move["failed_at"] = t_fail
                s = slot_of(t_fail)
                i.blocks.append((s, s + int(ra.integers(2, 4)), 3))
            i.move["at"] = t
            s = slot_of(t)
            pre = comms_blocks(r, i.build_start, i.profile)
            post = comms_blocks(r, i.build_end, i.profile)
            i.blocks += [b for b in pre if b[0] < s] + [b for b in post if b[0] >= s]
            i.blocks.append((s, s + int(ra.integers(150, 300)) // W.SLOT + 1, 3))
        else:  # exchange
            s = slot_of(i.exchange)
            pre = comms_blocks(r, i.build_start, i.profile)
            post = comms_blocks(r, "EM3.12.2", i.profile)
            i.blocks = [b for b in pre if b[0] < s] + [b for b in post if b[0] >= s]
            i.blocks.append((s, s + int(ra.integers(90, 170)) // W.SLOT + 1, 3))
    # the PX5.3.1 pilot site whose cellular modem dropped out for most of the week
    pilot = sorted([i for i in insts if i.group == "full" and i.build_start == "PX5.3.1"], key=lambda x: x.nmi)
    pilot[5].blocks.append((int(2.6 * W.SLOTS_PER_DAY), int(4.9 * W.SLOTS_PER_DAY), 3))
    return insts


def slot_class(inst):
    m = np.zeros(W.WEEK_SLOTS, dtype=np.int8)
    for s, e, c in inst.blocks:
        s, e = max(0, s), min(W.WEEK_SLOTS, e)
        if e > s:
            m[s:e] = np.maximum(m[s:e], c)
    return m


def day_counts(inst):
    """Per market day: (expected, missing precut-recovered, post-recovered, never) per data stream."""
    suff, L, _ = W.PROFILES[inst.profile]
    m = slot_class(inst)
    step = L // W.SLOT
    per = W.SLOTS_PER_DAY // step
    out = []
    for d in range(W.DAYS):
        ends = m[d * W.SLOTS_PER_DAY + step - 1:(d + 1) * W.SLOTS_PER_DAY:step]
        assert len(ends) == per
        out.append((per, int((ends == 1).sum()), int((ends == 2).sum()), int((ends == 3).sum())))
    return out
