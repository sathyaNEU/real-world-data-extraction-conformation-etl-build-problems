"""task304 architecture 4: the clean truth behind the two asks, on their own random streams.

Ask A: the PPE vending supplier's machines at the hubs, July to September 2026 (vends, restocks, a range change that
turned product EP-01 from one pair of earplugs into a pack of five, and two rounds of machine swaps between hubs).
Ask B: the hearing program's audiometry (baseline, annual tests, retests within 30 days, references re-established by
confirmed shifts) and the HR transfer history that places a worker at a hub on a date.
"""
import datetime as dt
from collections import defaultdict

import numpy as np

import params as P


def days(a, b):
    d, out = a, []
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


# ------------------------------------------------------------------ ask A
class Vending:
    def __init__(self, world, seed=None):
        seed = P.VEND_SEED if seed is None else seed
        self.rng = rng = np.random.default_rng(seed)
        self.world = world
        codes = [h["code"] for h in P.HUBS]
        # two machines a hub; machine numbers as the supplier issues them
        ids = sorted(set(int(x) for x in rng.integers(2100, 9800, size=40)))
        rng.shuffle(ids)
        self.machines = []
        k = 0
        for code in codes:
            for slot in ("North", "South"):
                self.machines.append(dict(machine="VM-%04d" % ids[k], hub0=code, location=slot,
                                          model=str(rng.choice(["Vendex P40", "Vendex P40", "SafeStock 360"])),
                                          share=float(rng.uniform(0.38, 0.62))))
                k += 1
        # the site of each machine by date (swaps), with an offline gap in transit
        self.site_on = {}
        self.moves = []
        cur = {m["machine"]: m["hub0"] for m in self.machines}
        by_hub = defaultdict(list)
        for m in self.machines:
            by_hub[m["hub0"]].append(m["machine"])
        timeline = defaultdict(list)    # machine -> [(from_date, hub or None)]
        for m in self.machines:
            timeline[m["machine"]].append((P.VEND_START - dt.timedelta(days=30), m["hub0"]))
        for leave, (a, b) in P.RELOCATIONS:
            ma = [x for x in by_hub[a]][0 if leave.month == 8 else 1]
            mb = [x for x in by_hub[b]][0 if leave.month == 8 else 1]
            gap_a = int(rng.integers(1, 4))      # leaves on a Saturday, commissioned at the new hub one to three days later
            gap_b = int(rng.integers(1, 4))
            for mach, src, dst, gap in ((ma, a, b, gap_a), (mb, b, a, gap_b)):
                arrive = leave + dt.timedelta(days=gap)
                timeline[mach].append((leave, None))
                timeline[mach].append((arrive, dst))
                self.moves.append(dict(machine=mach, src=src, dst=dst, leave=leave, arrive=arrive))
            by_hub[a][by_hub[a].index(ma)] = mb
            by_hub[b][by_hub[b].index(mb)] = ma
        self.timeline = timeline
        self.current = {}
        for mach, tl in timeline.items():
            self.current[mach] = [h for d, h in tl if h][-1]
        self.range_change = {}
        for m in self.machines:
            self.range_change[m["machine"]] = P.RANGE_CHANGE_SUNDAYS[int(rng.integers(0, 2))]
        self.vends = []
        self.visits = []
        self._simulate()

    def site(self, mach, d):
        hub = None
        for start, h in self.timeline[mach]:
            if d >= start:
                hub = h
        return hub

    def _simulate(self):
        rng = self.rng
        W = self.world
        # worker-shifts per hub per weekday from the main world's pattern (its headcount scale)
        heads = defaultdict(int)
        for p in W.people:
            if p["kind"] in ("EMP", "LH"):
                heads[p["hub"]] += 1
        tz_shift = {h["code"]: h for h in P.HUBS}
        slots = {"AM": [5.3, 7.0, 9.4], "PM": [13.2, 15.0, 17.4], "NT": [21.3, 23.0, 25.4]}
        for d in days(P.VEND_START - dt.timedelta(days=2), P.VEND_END + dt.timedelta(days=2)):
            if d.weekday() >= 5:            # the hubs sort Monday to Friday; the Friday night shift ends Saturday 05:00
                continue
            for m in self.machines:
                mach = m["machine"]
                hub = self.site(mach, d)
                if hub is None:
                    continue
                # each hub's demand is split between the machines standing there that day
                standing = [x for x in self.machines if self.site(x["machine"], d) == hub]
                wsum = sum(x["share"] for x in standing)
                frac = m["share"] / wsum
                demand_pairs = heads[hub] * 0.9 * P.PAIRS_PER_WORKER_SHIFT * frac
                after = d >= self.range_change[mach]
                per_vend = P.EP_PACK_AFTER if after else 1
                n_ep = int(rng.poisson(demand_pairs / per_vend))
                n_em = int(rng.poisson(heads[hub] * 0.012 * frac))
                for prod, n in (("EP-01", n_ep), ("EM-01", n_em)):
                    for _ in range(n):
                        sh = str(rng.choice(["AM", "PM", "NT"]))
                        shift_h = float(rng.choice(slots[sh]))
                        minute = shift_h * 60 + float(rng.uniform(0, 80))
                        local = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=minute)
                        self.vends.append(dict(machine=mach, hub=hub, local=local, product=prod, qty=1,
                                               pairs=(per_vend if prod == "EP-01" else 0)))
            # restock and service visits
        for m in self.machines:
            mach = m["machine"]
            for start, hub in self.timeline[mach]:
                pass
            d = P.VEND_START - dt.timedelta(days=int(rng.integers(1, 8)))
            while d <= P.VEND_END + dt.timedelta(days=2):
                hub = self.site(mach, d)
                if hub is not None and d.weekday() < 5:
                    after = d >= self.range_change[mach]
                    self.visits.append(dict(machine=mach, hub=hub, date=d, action="RESTOCK", product="EP-01",
                                            qty=int(rng.integers(180, 420)) if not after else int(rng.integers(40, 90)),
                                            uom="PR" if not after else "PK5"))
                    self.visits.append(dict(machine=mach, hub=hub, date=d, action="RESTOCK", product="EM-01",
                                            qty=int(rng.integers(6, 18)), uom="EA"))
                d += dt.timedelta(days=int(rng.integers(6, 11)))
            rc = self.range_change[mach]
            self.visits.append(dict(machine=mach, hub=self.site(mach, rc), date=rc, action="RANGE CHANGE",
                                    product="EP-01", qty=int(rng.integers(40, 80)), uom="PK5"))
        for mv in self.moves:
            self.visits.append(dict(machine=mv["machine"], hub=mv["dst"], date=mv["arrive"], action="COMMISSION",
                                    product="EP-01", qty=int(rng.integers(40, 80)) if mv["arrive"] >= self.range_change[mv["machine"]] else int(rng.integers(200, 400)),
                                    uom="PK5" if mv["arrive"] >= self.range_change[mv["machine"]] else "PR"))
        self.visits.sort(key=lambda v: (v["date"], v["machine"], v["action"]))

    def truth(self):
        """Earplug pairs issued at each hub in each month (the hub where the machine stood, local time)."""
        out = defaultdict(int)
        for v in self.vends:
            if v["product"] == "EP-01":
                out[(v["hub"], v["local"].month)] += v["pairs"]
        return out


# ------------------------------------------------------------------ ask B
class Audiometry:
    def __init__(self, world, seed=P.SEED + 23):
        self.rng = rng = np.random.default_rng(seed)
        self.world = world
        T = P.TITLES
        enrol = []
        for p in world.people:
            if p["kind"] != "EMP":
                continue
            tt = T[p["hub"]]
            if p["title"] in (tt["induct"], tt["relief"], tt["lead"]):
                enrol.append(p)
        self.enrolled = enrol
        # transfers between hubs in 2026 (effective dates); the main world's hub is the worker's hub after them
        self.transfers = []
        codes = [h["code"] for h in P.HUBS]
        movers = rng.choice(len(enrol), size=24, replace=False)
        self.hub_hist = {}
        for i, p in enumerate(enrol):
            self.hub_hist[p["pid"]] = [(dt.date(2000, 1, 1), p["hub"])]
        for j in movers:
            p = enrol[int(j)]
            src = str(rng.choice([c for c in codes if c != p["hub"]]))
            eff = dt.date(2026, int(rng.integers(3, 10)), int(rng.integers(1, 28)))
            self.hub_hist[p["pid"]] = [(dt.date(2000, 1, 1), src), (eff, p["hub"])]
            self.transfers.append(dict(pid=p["pid"], from_hub=src, to_hub=p["hub"], effective=eff))
        self.tests = []
        self._simulate()

    def hub_at(self, pid, d):
        h = None
        for start, hub in self.hub_hist[pid]:
            if d >= start:
                h = hub
        return h

    def _simulate(self):
        rng = self.rng
        tid = 410000
        for p in self.enrolled:
            pid = p["pid"]
            age = int(rng.integers(21, 63))
            base = []
            for ear in (0, 1):
                b = [max(0.0, 5 * round((rng.normal(8 + 0.35 * max(age - 30, 0), 6)) / 5)) for _ in range(3)]
                base.append(b)
            bdate = dt.date(int(rng.integers(2022, 2025)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            cur = [list(base[0]), list(base[1])]
            tests = [(bdate, "BASELINE", [list(base[0]), list(base[1])])]
            # annual tests in 2025 and 2026, with occasional true shifts
            for yr in (2025, 2026):
                ad = dt.date(yr, int(rng.integers(2, 11)), int(rng.integers(1, 28)))
                if ad <= bdate:
                    continue
                true_shift = rng.random() < (0.09 if yr == 2025 else 0.11)
                if true_shift:
                    ear = int(rng.integers(0, 2))
                    cur[ear] = [cur[ear][0] + float(rng.choice([5, 10])), cur[ear][1] + float(rng.choice([10, 15, 20])),
                                cur[ear][2] + float(rng.choice([15, 20, 25]))]
                meas = [[max(0.0, 5 * round((x + rng.normal(0, 2.5)) / 5)) for x in cur[e]] for e in (0, 1)]
                temp = (not true_shift) and rng.random() < 0.05     # a temporary shift on the day
                if temp:
                    e = int(rng.integers(0, 2))
                    meas[e] = [meas[e][0] + 10, meas[e][1] + 15, meas[e][2] + 15]
                tests.append((ad, "ANNUAL", meas))
                if true_shift or temp:
                    if rng.random() < 0.86:     # retested within 30 days, most of the time
                        rd = ad + dt.timedelta(days=int(rng.integers(9, 29)))
                        rmeas = [[max(0.0, 5 * round((x + rng.normal(0, 2.5)) / 5)) for x in cur[e]] for e in (0, 1)]
                        tests.append((rd, "RETEST", rmeas))
            for d, typ, m in tests:
                tid += int(rng.integers(3, 40))
                self.tests.append(dict(test_id=tid, pid=pid, date=d, type=typ, L=m[0], R=m[1]))

    @staticmethod
    def shift(test, ref):
        out = []
        for e in ("L", "R"):
            out.append(sum(test[e][i] - ref[e][i] for i in range(3)) / 3.0)
        return max(out)

    def truth(self, year=P.AUDIO_YEAR):
        """Workers with a shift confirmed in the year, at their hub on the retest date; and each worker's current
        reference (what the provider holds)."""
        by = defaultdict(list)
        for t in self.tests:
            by[t["pid"]].append(t)
        confirmed = defaultdict(set)
        current_ref = {}
        for pid, ts in by.items():
            ts.sort(key=lambda t: t["date"])
            ref = ts[0]
            i = 1
            while i < len(ts):
                t = ts[i]
                if t["type"] == "ANNUAL" and self.shift(t, ref) >= P.STS_DB:
                    rt = None
                    for u in ts[i + 1:]:
                        if u["type"] == "RETEST" and 0 < (u["date"] - t["date"]).days <= P.RETEST_DAYS:
                            rt = u
                            break
                    if rt is not None and self.shift(rt, ref) >= P.STS_DB:
                        if rt["date"].year == year:
                            confirmed[self.hub_at(pid, rt["date"])].add(pid)
                        ref = rt
                i += 1
            current_ref[pid] = ref
        return confirmed, current_ref
