"""The network manager's side of summer 2026: the regulations on the centre's traffic volumes and on Holmvik
arrivals (1 May to 30 September 2026), and the slot allocation list, one row per flight plan per regulation that
captured it, with the delay that regulation's slot gave the plan.

Plans that never flew stay in the list as allocated: when an operator re-filed after a slot was issued, the
original plan keeps its row (the flight flew on the re-filed plan, with its own smaller delay or none), and a few
flights were cancelled outright after their slot was issued."""
import datetime as dt

import numpy as np

import traffic as T
import world as W

SEED = 18133
REG_FROM = dt.datetime(2026, 5, 1, tzinfo=W.UTC)
REG_TO = dt.datetime(2026, 10, 1, tzinfo=W.UTC)
# how often a sector is regulated on a summer day, and how hard
BUSY = {"TRV": 0.55, "LYS": 0.5, "GRD": 0.42, "MSB": 0.38, "LNM": 0.2, "HAL": 0.24, "KRW": 0.16, "SDV": 0.18}
REASONS = [("C", 0.62), ("S", 0.16), ("W", 0.14), ("M", 0.05), ("T", 0.03)]


def _reason(rng):
    r = rng.random()
    acc = 0.0
    for code, p in REASONS:
        acc += p
        if r < acc:
            return code
    return "C"


def regulations(rng):
    regs = []
    day = REG_FROM.date()
    while day < REG_TO.date():
        mf = W.MONTH[day.month] * W.WEEKDAY[day.weekday()]
        seq = {}
        for s in W.SECTORS:
            n = rng.poisson(BUSY[s] * mf ** 3 * 1.25)
            for _ in range(min(n, 2)):
                h = float(rng.choice([7, 8, 9, 10, 11, 14, 15, 16, 17, 18]))
                start = dt.datetime.combine(day, dt.time(0), tzinfo=W.LOCAL) + dt.timedelta(hours=h, minutes=int(rng.integers(0, 12)) * 5)
                end = start + dt.timedelta(minutes=int(rng.integers(18, 54)) * 5)
                seq[s] = seq.get(s, 0) + 1
                regs.append(dict(id="%s%02d%s" % (W.TV[s][2:], day.day, "ABC"[seq[s] - 1]), tv=W.TV[s], sector=s,
                                 kind="En-route", reason=_reason(rng), start=start.astimezone(W.UTC),
                                 end=end.astimezone(W.UTC), q=float(rng.uniform(0.25, 0.55)),
                                 rate=int(rng.integers(28, 46))))
        if rng.random() < 0.3 * mf:
            start = dt.datetime.combine(day, dt.time(0), tzinfo=W.LOCAL) + dt.timedelta(hours=float(rng.choice([7, 8, 15, 16, 17, 18])))
            end = start + dt.timedelta(minutes=int(rng.integers(30, 60)) * 5)
            regs.append(dict(id="EXHMA%02d" % day.day, tv="EXHMARR", sector=None, kind="Airport",
                             reason="W" if rng.random() < 0.7 else "G", start=start.astimezone(W.UTC),
                             end=end.astimezone(W.UTC), q=float(rng.uniform(0.35, 0.6)), rate=int(rng.integers(20, 30))))
        day += dt.timedelta(days=1)
    regs.sort(key=lambda r: (r["start"], r["id"]))
    return regs


def _delay(rng):
    return int(min(1 + rng.gamma(1.25, 10.5), 118))


class Plans:
    """Unique flight plan ids for plans that never reached the flight data (re-filed originals, cancellations)."""

    def __init__(self, taken, rng):
        self.taken = set(taken)
        self.rng = rng

    def new(self):
        while True:
            pid = "A%s%08d" % ("ABCDEFGHJKLMNPRSTUVWXYZ"[int(self.rng.integers(23))], int(self.rng.integers(10 ** 8)))
            if pid not in self.taken:
                self.taken.add(pid)
                return pid


def ask1(t, rows, regs):
    """En-route ATFM delay per flight by sector, summer 2026 local, from the simulation (the golden's arithmetic):
    each flown flight's most penalising regulation, when en-route, charges its delay to its sector if the flight
    entered that sector in the season; the flights that entered each sector in the season are the denominator."""
    a, b = (T.secs(x) for x in W.season(2026))
    kind = {r["id"]: (r["kind"], r["sector"]) for r in regs}
    m = (t["t0"] >= a) & (t["t0"] < b)
    den = {k: len(set(t["fi"][m & (t["sec"] == k)].tolist())) for k in range(8)}
    entry = {}
    sel = (t["t0"] >= a - 86400 * 40) & (t["t0"] < b + 86400 * 40)
    for fi, sec, t0 in zip(t["fi"][sel], t["sec"][sel], t["t0"][sel]):
        entry[(int(fi), int(sec))] = int(t0)
    top = {}
    for r in rows:
        if r["flew"] and (r["ifplid"] not in top or r["delay"] > top[r["ifplid"]]["delay"]):
            top[r["ifplid"]] = r
    num = {k: 0 for k in range(8)}
    for r in top.values():
        k, s = kind[r["reg"]]
        if k != "En-route":
            continue
        si = W.SECTORS.index(s)
        t0 = entry.get((r["fi"], si))
        if t0 is not None and a <= t0 < b:
            num[si] += r["delay"]
    return {k: num[k] / den[k] for k in range(8)}


def allocations(f, t, ifplid, svcs, regs, seed=SEED):
    """Rows (ifplid, callsign, adep, ades, eobt, regulation, delay) and the truth per row (flew or not)."""
    rng = np.random.default_rng(seed)
    lo, hi = T.secs(REG_FROM), T.secs(REG_TO)
    m = (t["t0"] >= lo - 86400) & (t["t0"] < hi + 86400)
    tt = {k: v[m] for k, v in t.items()}
    by_sec = {s: np.nonzero(tt["sec"] == k)[0] for k, s in enumerate(W.SECTORS)}
    last_exit = {}
    for k in range(len(tt["fi"])):
        fi = int(tt["fi"][k])
        last_exit[fi] = max(last_exit.get(fi, 0), int(tt["t1"][k]))
    captured = {}
    for r in regs:
        a, b = T.secs(r["start"]), T.secs(r["end"])
        if r["kind"] == "En-route":
            idx = by_sec[r["sector"]]
            hit = idx[(tt["t0"][idx] >= a) & (tt["t0"][idx] < b)]
            fis = [int(tt["fi"][k]) for k in hit]
        else:
            fis = [fi for fi, ex in last_exit.items() if f["ades"][fi] == W.HUB and a <= ex + 1200 < b]
        for fi in sorted(set(fis)):
            if rng.random() < r["q"]:
                captured.setdefault(fi, []).append((r["id"], _delay(rng)))
    plans = Plans(ifplid, rng)
    rows = []
    for fi in sorted(captured):
        caps = captured[fi]
        # distinct delays within one plan, so the most penalising regulation is never a tie
        seen = set()
        caps2 = []
        for rid, d in sorted(caps, key=lambda x: -x[1]):
            while d in seen:
                d -= 1
            seen.add(d)
            caps2.append((rid, max(d, 1)))
        base = dict(callsign=f["callsign"][fi], adep=f["adep"][fi], ades=f["ades"][fi], actype=f["actype"][fi])
        top = max(d for _, d in caps2)
        if top >= 20 and rng.random() < 0.16:
            orig = plans.new()
            eobt0 = int(f["eobt"][fi]) - 60 * int(rng.integers(0, 16))
            extra = int(rng.integers(8, 36))
            for rid, d in caps2:
                rows.append(dict(ifplid=orig, eobt=eobt0, reg=rid, delay=d + extra, flew=False, **base))
            if rng.random() < 0.42:
                continue      # the re-filed plan missed every regulation
            for rid, d in caps2:
                rows.append(dict(ifplid=ifplid[fi], eobt=int(f["eobt"][fi]), reg=rid, delay=d, flew=True, fi=fi, **base))
        else:
            for rid, d in caps2:
                rows.append(dict(ifplid=ifplid[fi], eobt=int(f["eobt"][fi]), reg=rid, delay=d, flew=True, fi=fi, **base))
    # flights cancelled outright after their slot was issued: a service that did not operate that day
    flown = {(f["callsign"][fi], int(f["day"][fi])) for fi in range(len(f["callsign"]))}
    allsv = [s for lst in svcs.values() for s in lst if s.flow not in W.NEW_2027]
    for r in regs:
        if r["kind"] != "En-route" or rng.random() > 0.3:
            continue
        a = r["start"].astimezone(W.LOCAL)
        day = a.date()
        cand = [s for s in allsv if any(p[0] == r["sector"] for p in W.FLOWS[s.flow]["path"])
                and (s.callsign, day.toordinal()) not in flown
                and abs(s.minute - (a.hour * 60 + a.minute + 40)) < 90]
        if not cand:
            continue
        s = cand[int(rng.integers(len(cand)))]
        eobt = T.secs(dt.datetime.combine(day, dt.time(0), tzinfo=W.LOCAL) + dt.timedelta(minutes=s.minute - s.offset))
        rows.append(dict(ifplid=plans.new(), eobt=eobt, reg=r["id"], delay=_delay(rng), flew=False,
                         callsign=s.callsign, adep=s.adep, ades=s.ades, actype=s.actype))
    rows.sort(key=lambda x: (x["eobt"], x["callsign"], x["ifplid"], x["reg"]))
    return rows
