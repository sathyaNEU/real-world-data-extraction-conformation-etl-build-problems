"""The truth: Kooralong Hospital's general surgery operations 2022 to September 2027, the instrument trays and
sets they used in 2027, the CSSD's steriliser loads, and the site infections that followed.

Generating process (what the pack's records come from):
- each consultant holds two or three elective lists a week, morning (08:15) or afternoon (13:45), three to four
  operations a list, and takes the on-call day in rotation, when emergency operations run at any hour;
- every elective operation opens one of the consultant's four preference trays (rigid containers) and one light
  wrapped set; after the list they go to the CSSD, are washed and packed and go into the next cycle of the steriliser
  that takes them: steriliser 3, the one chamber validated for containers over 10 kg, cycles round the clock;
  steriliser 1 and 2 take wrapped sets and lighter containers by day; steriliser 4 in the theatre suite takes the
  emergency theatre's wrapped trays;
- from the 12 May 2027 repair, steriliser 3's drying stage runs short on heavy containers; every cycle still prints
  a pass, and an operation that opens a tray from such a load carries EXP_RR times the risk;
- infection risk is the Centre's published rate for the procedure and risk index, times the consultant's own
  effect where there is one (PRACTICE), times EXP_RR for an exposed tray.
"""
import datetime as dt
import math

import numpy as np

import common as C

DAY = dt.timedelta(days=1)
MIN = dt.timedelta(minutes=1)

MIX_COLO = {"COLO": 0.36, "SB": 0.10, "XLAP": 0.08, "APPY": 0.12, "CHOL": 0.18, "HER": 0.16}
MIX_GEN = {"COLO": 0.10, "SB": 0.06, "XLAP": 0.06, "APPY": 0.18, "CHOL": 0.32, "HER": 0.28}
EMERG_MIX = {"APPY": 0.42, "XLAP": 0.22, "CHOL": 0.18, "SB": 0.12, "COLO": 0.06}
DUR = {"COLO": (165, 45), "SB": (140, 40), "XLAP": (120, 35), "APPY": (62, 18), "CHOL": (88, 25), "HER": (92, 28)}
WOUND_DIRTY = {"COLO": 0.30, "SB": 0.30, "XLAP": 0.45, "APPY": 0.40, "CHOL": 0.10, "HER": 0.03}
GENERIC = {"COLO": "Bowel set", "SB": "Bowel set", "XLAP": "Major laparotomy set", "APPY": "Laparoscopic general set",
           "CHOL": "Laparoscopic general set", "HER": "Hernia set"}
GENERIC_COPIES = {"Bowel set": 9, "Major laparotomy set": 8, "Laparoscopic general set": 16, "Hernia set": 8}


def _pick(r, mix):
    keys = list(mix)
    p = np.array([mix[k] for k in keys])
    return keys[int(r.choice(len(keys), p=p / p.sum()))]


def schedule():
    """Every operation 2022-01-03 to 2027-09-30, in time order."""
    r = C.rng("schedule")
    ops = []
    # elective templates: each consultant's weekday lists
    tmpl = {}
    for k, c in enumerate(C.CONSULTANTS):
        days = sorted(r.choice(5, size=4, replace=False).tolist())
        tmpl[c] = days
    leave = {(c, y): set(r.choice(52, size=6, replace=False).tolist()) for c in C.CONSULTANTS
             for y in range(2022, 2028)}
    d = C.HIST0
    ur_next = 4_100_000
    oncall_i = 0
    while d <= C.WIN1:
        wk = d.isocalendar()[1] - 1
        if d.weekday() < 5:
            for c in C.CONSULTANTS:
                if d.weekday() not in tmpl[c] or wk in leave[(c, d.year)]:
                    continue
                aft = r.random() < C.AFTERNOON[c]
                t = dt.datetime.combine(d, dt.time(13, 45) if aft else dt.time(8, 15))
                last = dt.datetime.combine(d, dt.time(17, 30) if aft else dt.time(12, 0))
                mix = MIX_COLO if c in C.COLORECTAL else MIX_GEN
                for j in range(6):
                    if j and t > last:
                        break
                    proc = _pick(r, mix)
                    mu, sd = DUR[proc]
                    mins = int(max(25, r.normal(mu, sd)))
                    ur_next += int(r.integers(1, 40))
                    ops.append(dict(consultant=c, start=t, minutes=mins, proc=proc, emergency=False,
                                    list_id="%s-%s-%s" % (c, d.isoformat(), "PM" if aft else "AM"),
                                    asa=int(r.choice([1, 2, 3, 4], p=[0.18, 0.55, 0.23, 0.04])),
                                    wound=int(3 + (r.random() < 0.3)) if r.random() < WOUND_DIRTY[proc]
                                    else int(r.choice([1, 2], p=[0.35, 0.65])),
                                    ur=ur_next, mesh=(proc == "HER" and r.random() < 0.85)))
                    t = t + dt.timedelta(minutes=mins + int(r.integers(20, 40)))
        # emergency operations by the day's on-call consultant
        oc = C.CONSULTANTS[oncall_i % len(C.CONSULTANTS)]
        oncall_i += 1
        for j in range(int(r.poisson(3.4))):
            proc = _pick(r, EMERG_MIX)
            hour = float(r.choice([9, 11, 14, 16, 18, 20, 21, 22, 23, 1, 3],
                                  p=[.06, .08, .10, .12, .14, .14, .11, .09, .07, .05, .04]))
            t = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(hours=hour, minutes=int(r.integers(0, 59)))
            if hour < 7:
                t = t + DAY
            mu, sd = DUR[proc]
            mins = int(max(25, r.normal(mu, sd)))
            ur_next += int(r.integers(1, 40))
            ops.append(dict(consultant=oc, start=t, minutes=mins, proc=proc, emergency=True,
                            list_id="%s-%s-EM" % (oc, d.isoformat()),
                            asa=int(r.choice([1, 2, 3, 4], p=[0.10, 0.42, 0.38, 0.10])),
                            wound=int(3 + (r.random() < 0.4)) if r.random() < WOUND_DIRTY[proc] + 0.15
                            else int(r.choice([1, 2], p=[0.2, 0.8])),
                            ur=ur_next, mesh=False))
        d += DAY
    ops = [o for o in ops if o["start"].date() <= C.WIN1]
    ops.sort(key=lambda o: (o["start"], o["consultant"]))
    for i, o in enumerate(ops):
        o["id"] = i
        o["end"] = o["start"] + dt.timedelta(minutes=o["minutes"])
        o["idx"] = C.risk_index(o["asa"], o["wound"], o["minutes"], o["proc"])
    return ops


class Steriliser:
    """A steriliser's cycle slots; a set joins the first slot at or after it is packed."""

    def __init__(self, name, r):
        self.name = name
        self.r = r
        self.next_no = {"S1": 41_200, "S2": 38_950, "S3": 8_311, "S4": 12_604}[name]
        self.loads = {}          # slot start -> list of set barcodes

    def slot_after(self, t):
        night = self.name == "S3"
        d = t.date()
        while True:
            if night:                                  # the container steriliser cycles round the clock
                base = dt.datetime.combine(d, dt.time(0, 25))
                slots = [base + k * dt.timedelta(minutes=80) for k in range(18)]
            else:
                base = dt.datetime.combine(d, dt.time(7, 40) if self.name != "S4" else dt.time(9, 10))
                n = 9 if self.name != "S4" else 6
                slots = [base + k * dt.timedelta(minutes=70 if self.name != "S4" else 95) for k in range(n)]
            for s in slots:
                if s >= t:
                    return s
            d += DAY


def instruments(ops):
    """2027: each operation's tray and set, their CSSD passes and the steriliser loads (with tests and aborts)."""
    r = C.rng("instruments")
    sts = {n: Steriliser(n, r) for n in C.STERILISERS}
    trays = {}
    for c in C.CONSULTANTS:
        heavy = C.HEAVY_TRAYS.get(c, 0)
        trays[c] = [dict(barcode="KH%05d" % int(r.integers(20000, 99999)), owner=c, kind="tray",
                         name="%s preference tray %s" % (c, "ABCD"[k]), container="Rigid container",
                         kg=round(float(r.uniform(10.6, 12.6) if k < heavy else r.uniform(6.8, 9.6)), 1),
                         ready=dt.datetime(2026, 12, 20), last=None)
                    for k in range(4)]
    trays["EMERGENCY"] = [dict(barcode="KH%05d" % int(r.integers(20000, 99999)), owner="", kind="tray",
                               name="Emergency general tray %d" % (k + 1), container="Wrapped tray",
                               kg=round(float(r.uniform(6.2, 7.8)), 1), ready=dt.datetime(2026, 12, 20), last=None)
                          for k in range(6)]
    sets = {}
    for g, n in GENERIC_COPIES.items():
        sets[g] = [dict(barcode="KH%05d" % int(r.integers(20000, 99999)), owner="", kind="set",
                        name="%s %d" % (g, k + 1), container="Wrapped tray", kg=round(float(r.uniform(2.1, 4.4)), 1),
                        ready=dt.datetime(2026, 12, 20), last=None) for k in range(n)]
    seen = set()
    for pool in list(trays.values()) + list(sets.values()):
        for s in pool:
            while s["barcode"] in seen:
                s["barcode"] = "KH%05d" % int(r.integers(20000, 99999))
            seen.add(s["barcode"])
    uses, passes = [], []
    pending = {}                  # list_id -> [(item, ...)] returned together at the list's end
    ops27 = [o for o in ops if o["start"].date() >= C.TRACK0]
    list_end = {}
    for o in ops27:
        list_end[o["list_id"]] = max(list_end.get(o["list_id"], o["end"]), o["end"])

    def reprocess(item, back):
        recv = back + dt.timedelta(minutes=int(r.integers(20, 55)))
        wash = recv + dt.timedelta(minutes=int(r.integers(55, 85)))
        pack = wash + dt.timedelta(minutes=int(r.integers(18, 40)))
        h = pack.hour
        night = h >= 19 or h < 7
        if item["name"].startswith("Emergency"):
            st = "S4"                                  # the theatre suite's steriliser, round the clock
        elif item["container"] == "Rigid container" and item["kg"] > 10.0:
            st = "S3"                                  # the one chamber validated for containers over 10 kg
        else:
            if night:                                  # wrapped sets wait for the morning's first day load
                pack = dt.datetime.combine(pack.date() + (DAY if h >= 19 else dt.timedelta(0)), dt.time(7, 35))
            st = "S1" if r.random() < 0.5 else "S2"
        slot = sts[st].slot_after(pack)
        sts[st].loads.setdefault(slot, []).append(item["barcode"])
        item["ready"] = slot + dt.timedelta(minutes=int(r.integers(95, 130)))
        passes.append(dict(barcode=item["barcode"], recv=recv, wash=wash, pack=pack, st=st, slot=slot))
        item["last"] = (st, slot)

    for o in ops27:
        owner = "EMERGENCY" if o["emergency"] else o["consultant"]
        tray_pool = [t for t in trays[owner] if t["ready"] <= o["start"] - dt.timedelta(minutes=30)]
        tray = min(tray_pool, key=lambda t: t["ready"]) if tray_pool else min(trays[owner], key=lambda t: t["ready"])
        g = GENERIC[o["proc"]]
        set_pool = [s for s in sets[g] if s["ready"] <= o["start"] - dt.timedelta(minutes=30)]
        gset = min(set_pool, key=lambda s: s["ready"]) if set_pool else min(sets[g], key=lambda s: s["ready"])
        for item in (tray, gset):
            uses.append(dict(op=o["id"], barcode=item["barcode"], kind=item["kind"], last=item["last"],
                             scan=o["start"] - dt.timedelta(minutes=int(r.integers(8, 28)))))
            item["ready"] = dt.datetime(2100, 1, 1)
        back = list_end[o["list_id"]] if not o["emergency"] else o["end"]
        pending.setdefault(o["list_id"], []).append((tray, back))
        pending[o["list_id"]].append((gset, back))
        if o["emergency"] or o["end"] >= list_end[o["list_id"]]:
            for item, b in pending.pop(o["list_id"]):
                reprocess(item, b)
    # cycles: loads, the daily air-removal (Bowie-Dick) test, the weekly leak test, aborts re-run in the next slot
    cycles = []
    for name, s in sts.items():
        slots = sorted(s.loads)
        days = sorted({sl.date() for sl in slots})
        tests = []
        for d in days:
            t0 = dt.datetime.combine(d, dt.time(0, 5) if name == "S3" else dt.time(7, 5))
            tests.append((t0, "Bowie-Dick test"))
            if d.weekday() == 0:
                tests.append((t0 - dt.timedelta(minutes=40), "Vacuum leak test"))
        events = [(sl, "Load") for sl in slots] + tests
        events.sort()
        for t, kind in events:
            if kind == "Load":
                contents = list(s.loads[t])
                if r.random() < 0.015:
                    cycles.append(dict(st=name, no=s.next_no, start=t, end=t + dt.timedelta(minutes=19),
                                       kind=kind, result="Aborted", contents=contents))
                    s.next_no += 1
                    t = t + dt.timedelta(minutes=24)
                cycles.append(dict(st=name, no=s.next_no, start=t, end=t + dt.timedelta(minutes=int(r.integers(54, 63))),
                                   kind=kind, result="Pass", contents=contents))
            else:
                cycles.append(dict(st=name, no=s.next_no, start=t, end=t + dt.timedelta(minutes=17 if
                                   kind.startswith("Bowie") else 26), kind=kind, result="Pass", contents=[]))
            s.next_no += 1
            if name == "S3" and t < C.REPAIR <= t + dt.timedelta(days=1) and s.next_no > 1000:
                pass
    # the controller board fitted at the repair restarts steriliser 3's cycle counter
    cycles.sort(key=lambda c: (c["st"], c["start"]))
    k = 0
    for c in cycles:
        if c["st"] == "S3" and c["start"] >= C.REPAIR:
            k += 1
            c["no"] = k
    return dict(trays=trays, sets=sets, uses=uses, passes=passes, cycles=cycles)


def exposure(ops, inst):
    """The truth: an operation is exposed when its heavy tray came from a steriliser 3 load after the repair."""
    exp = {}
    for u in inst["uses"]:
        if u["kind"] != "tray" or u["last"] is None:
            continue
        st, slot = u["last"]
        if st == "S3" and slot >= C.REPAIR:
            exp[u["op"]] = True
    return exp


def infections(ops, exp):
    r = C.rng("infections")
    out = []
    for o in ops:
        y = o["start"].year
        p = C.expected_rate(o["proc"], o["idx"])
        p *= C.PRACTICE.get(o["consultant"], {}).get(y, 1.0)
        if exp.get(o["id"]):
            p *= C.EXP_RR
        if r.random() >= min(p, 0.6):
            continue
        depth = str(r.choice(["Superficial incisional", "Deep incisional", "Organ/space"],
                             p=[0.46, 0.30, 0.24] if o["proc"] in ("COLO", "SB", "XLAP") else [0.60, 0.28, 0.12]))
        if o["mesh"] and depth != "Superficial incisional" and r.random() < 0.35:
            day = int(r.integers(31, 86))
        else:
            day = int(r.integers(3, 15)) if depth.startswith("Superficial") else int(r.integers(5, 29))
        out.append(dict(op=o["id"], depth=depth, onset=(o["start"] + dt.timedelta(days=day)).date(),
                        post_discharge=bool(r.random() < 0.32)))
    return out


def build_truth():
    ops = schedule()
    inst = instruments(ops)
    exp = exposure(ops, inst)
    inf = infections(ops, exp)
    return dict(ops=ops, inst=inst, exp=exp, inf=inf)


if __name__ == "__main__":
    T = build_truth()
    ops, exp, inf = T["ops"], T["exp"], T["inf"]
    win = [o for o in ops if C.WIN0 <= o["start"].date() <= C.WIN1]
    infd = {i["op"]: i for i in inf}
    print("ops", len(ops), "window", len(win), "infections", len(inf), "cycles", len(T["inst"]["cycles"]),
          "uses", len(T["inst"]["uses"]))
    for c in C.CONSULTANTS:
        w = [o for o in win if o["consultant"] == c]
        E = sum(C.expected_rate(o["proc"], o["idx"]) for o in w)
        O = sum(o["id"] in infd for o in w)
        we = [o for o in w if exp.get(o["id"])]
        wu = [o for o in w if not exp.get(o["id"])]
        Eu = sum(C.expected_rate(o["proc"], o["idx"]) for o in wu)
        Ou = sum(o["id"] in infd for o in wu)
        print("%s n=%d E=%.1f O=%d lim=%d | exposed %d | unexposed E=%.1f O=%d lim=%d" % (
            c, len(w), E, O, C.poisson_upper(E), len(we), Eu, Ou, C.poisson_upper(Eu)))
