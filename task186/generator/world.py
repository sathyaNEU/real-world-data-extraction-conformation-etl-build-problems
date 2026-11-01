"""The clean truth for task186: the CT lanes' operation, the roster, every threat image projection and its outcome.

Nothing here is written to target/. pack.py turns this into the exports the airport's systems produce.
"""
import datetime as dt
from collections import defaultdict

import numpy as np

import params as P

MIN_DAY = 1440


def days():
    d = P.DAY0
    while d <= P.WIN1:
        yield d
        d += dt.timedelta(days=1)


def lg(p):
    return np.log(p / (1.0 - p))


def blocks_for(lane, d):
    """Roster blocks for a lane on a local date: (period, start_min, end_min)."""
    if lane in P.INTL and d < P.INTL_CT:
        return []
    if lane == "D2" and P.D2_FAULT <= d < P.D2_NEW:
        return []
    wk = d.weekday() < 5
    spans = P.HOURS[lane]["wk" if wk else "we"]
    out = []
    for i, (a, b) in enumerate(spans):
        if len(spans) == 1:
            # one long interval: two early blocks, two late blocks
            m = (a + b) // 2
            m = m - m % 15
            q1 = (a + m) // 2
            q1 -= q1 % 15
            q3 = (m + b) // 2
            q3 -= q3 % 15
            out += [("E", a, q1), ("E", q1, m), ("L", m, q3), ("L", q3, b)]
        else:
            per = "E" if a < 750 else "L"
            m = (a + b) // 2
            m -= m % 15
            out += [(per, a, m), (per, m, b)]
    return out


class World:
    def __init__(self, seed=P.SEED):
        self.rng = np.random.default_rng(seed)
        self._library()
        self._officers()
        self._leave()
        self._operate()

    # ------------------------------------------------------------------ library
    def _library(self):
        r = self.rng
        cats = [c[0] for c in P.CATS]
        shares = np.array([c[4] for c in P.CATS])
        self.obj_cat = r.choice(cats, size=P.N_OBJ, p=shares / shares.sum())
        self.obj_diff = r.normal(0.0, 0.55, P.N_OBJ)
        ceff = {c[0]: c[3] for c in P.CATS}
        nf = P.N_OBJ * P.VIEWS
        self.fti_obj = np.repeat(np.arange(P.N_OBJ), P.VIEWS)
        self.fti_view = np.tile(np.arange(1, P.VIEWS + 1), P.N_OBJ)
        self.fti_eff = np.array([ceff[self.obj_cat[o]] for o in self.fti_obj]) + self.obj_diff[self.fti_obj] \
            + r.normal(0.0, 0.25, nf)
        # image numbers: issued in batches by the vendor, not in object order
        nums = r.choice(np.arange(10000, 99999), size=nf, replace=False)
        self.fti_num = np.sort(nums)[r.permutation(nf)]
        # object codes
        ocodes = r.choice(np.arange(1000, 9999), size=P.N_OBJ, replace=False)
        self.obj_code = ["KTL-%s-%04d" % (self.obj_cat[i], ocodes[i]) for i in range(P.N_OBJ)]

    def theta_for(self, target):
        lo, hi = -6.0, 9.0
        for _ in range(70):
            m = (lo + hi) / 2
            if (1.0 / (1.0 + np.exp(-(m + self.fti_eff)))).mean() < target:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2

    # ------------------------------------------------------------------ officers
    def _officers(self):
        r = self.rng
        offs = []

        def add(home, kind, target, endorsed, left=None, deficient=False):
            offs.append(dict(idx=len(offs), home=home, kind=kind, target=float(target), endorsed=endorsed,
                             left=left, deficient=deficient))

        vet = lambda: dt.date(2019, 1, 1) + dt.timedelta(days=int(r.integers(0, 2200)))
        # six full-time veterans whose detection of an unseen item is below standard
        for _ in range(6):
            add("D", "FT", r.uniform(P.DEF_FT[0], P.DEF_FT[1]), vet(), deficient=True)
        # four part-time officers endorsed after the domestic CT lanes opened, below standard
        for d in (dt.date(2025, 8, 11), dt.date(2025, 8, 25), dt.date(2025, 9, 15), dt.date(2025, 10, 6)):
            add("D", "CA", r.uniform(P.DEF_PT[0], P.DEF_PT[1]), d, deficient=True)
        for _ in range(28):
            add("D", "FT", r.uniform(0.87, 0.94), vet())
        for d in (dt.date(2025, 9, 1), dt.date(2025, 10, 13), dt.date(2025, 11, 3)):
            add("D", "FT", r.uniform(0.88, 0.93), d)
        for _ in range(16):
            add("D", "PT", r.uniform(0.87, 0.94), vet())
        for _ in range(P.N_CA_D):
            add("D", "CA", r.uniform(P.CA_T[0], P.CA_T[1]), vet())
        for _ in range(12):
            add("I", "FT", r.uniform(0.87, 0.94), vet())
        for _ in range(8):
            add("I", "PT", r.uniform(0.87, 0.94), vet())
        for _ in range(P.N_CA_I):
            add("I", "CA", r.uniform(P.CA_T[0], P.CA_T[1]), vet())
        # two full-time officers who leave during the screening year (no longer endorsed at 30 November)
        add("D", "FT", r.uniform(0.87, 0.93), vet(), left=dt.date(2026, 4, 17))
        add("I", "FT", r.uniform(0.87, 0.93), vet(), left=dt.date(2026, 8, 28))
        order = r.permutation(len(offs))
        self.off = [offs[i] for i in order]
        for i, o in enumerate(self.off):
            o["idx"] = i
            o["theta"] = self.theta_for(o["target"])
            o["week_early"] = int(r.integers(0, 2))
            o["days"] = set(r.choice(7, size={"FT": 5, "PT": 3, "CA": 2}[o["kind"]], replace=False).tolist())
        self.n_off = len(self.off)

    # ------------------------------------------------------------------ leave
    def _leave(self):
        r = self.rng
        self.annual = defaultdict(set)      # idx -> dates on annual leave (not rostered)
        for o in self.off:
            if o["kind"] == "CA":
                continue
            n = 2 if o["kind"] == "FT" else 1
            for _ in range(n):
                start = P.DAY0 + dt.timedelta(days=int(r.integers(10, 500)))
                length = int(r.choice([7, 10, 14, 14, 21]))
                for k in range(length):
                    self.annual[o["idx"]].add(start + dt.timedelta(days=k))

    # ------------------------------------------------------------------ operation
    def lam(self, lane, d, minute):
        h = minute / 60.0
        shape = 0.55 + 0.45 * np.exp(-((h - 7.5) / 2.2) ** 2) + 0.38 * np.exp(-((h - 17.0) / 2.4) ** 2)
        if lane in P.INTL:
            shape = 0.6 + 0.4 * np.exp(-((h - 9.5) / 2.5) ** 2) + 0.45 * np.exp(-((h - 21.0) / 1.8) ** 2)
        dow = [1.06, 0.97, 0.95, 1.0, 1.12, 0.9, 1.02][d.weekday()]
        season = {1: 1.12, 2: 0.94, 3: 1.0, 4: 1.08, 5: 0.95, 6: 0.97, 7: 1.1, 8: 0.96, 9: 1.03, 10: 1.07,
                  11: 1.0, 12: 1.15}[d.month]
        return P.LANE_BASE[lane] * shape * dow * season / 1.15

    def _operate(self):
        r = self.rng
        roster = []        # (idx, date, lane, start_min, end_min, sick)
        day_roster = []
        slots_out = []     # (date, lane, slot_start_min, bags, operator idx or -1)
        tips = []          # (idx, date, lane, minute, fti, hit, k_obj, k_fti, rt_ms)
        seen = [defaultdict(int) for _ in range(self.n_off)]
        seenf = [defaultdict(int) for _ in range(self.n_off)]
        self.sick = defaultdict(set)
        for d in days():
            # who can work today
            avail = {"D": [], "I": []}
            week = (d - P.DAY0).days // 7
            for o in self.off:
                if o["endorsed"] > d or (o["left"] and d > o["left"]):
                    continue
                if d in self.annual[o["idx"]]:
                    continue
                if d.weekday() not in o["days"]:
                    if not (o["kind"] == "CA" and r.random() < 0.05):
                        continue
                home = o["home"]
                if r.random() < 0.06:
                    home = "I" if home == "D" else "D"
                avail[home].append(o["idx"])
            # positions per lane and period
            lanes_today = {ln: blocks_for(ln, d) for ln in P.LANES}
            for cp, lanes in (("D", P.DOM), ("I", P.INTL)):
                pool = list(r.permutation(avail[cp])) if avail[cp] else []
                per_of = {}
                for i in pool:
                    o = self.off[i]
                    per_of[i] = ("E" if (week + o["week_early"]) % 2 == 0 else "L") if o["kind"] == "FT" \
                        else ("E" if r.random() < 0.5 else "L")
                for per in ("E", "L"):
                    people = [i for i in pool if per_of[i] == per]
                    lane_order = [ln for ln in r.permutation(lanes) if any(b[0] == per for b in lanes_today[ln])]
                    need = {}
                    for ln in lane_order:
                        bl = [b for b in lanes_today[ln] if b[0] == per]
                        need[ln] = []
                        for b in bl:
                            lm = np.mean([self.lam(ln, d, m) for m in range(b[1], b[2], 30)])
                            need[ln].append(2 if lm < 95 else (3 if lm < 165 else 4))
                    # core team per lane = min team over its blocks, extras for the larger blocks
                    assign = defaultdict(list)
                    pi = 0
                    for ln in lane_order:
                        core = min(need[ln])
                        for _ in range(core):
                            if pi < len(people):
                                assign[ln].append(("both", people[pi]))
                                pi += 1
                    for ln in lane_order:
                        for bi, t in enumerate(need[ln]):
                            for _ in range(t - min(need[ln])):
                                if pi < len(people):
                                    assign[ln].append((bi, people[pi]))
                                    pi += 1
                    # spare people: top up the busiest lanes' second block
                    while pi < len(people) and lane_order:
                        ln = lane_order[pi % len(lane_order)]
                        assign[ln].append((len(need[ln]) - 1, people[pi]))
                        pi += 1
                    for ln in lane_order:
                        bl = [b for b in lanes_today[ln] if b[0] == per]
                        for which, i in assign[ln]:
                            sick = r.random() < 0.035
                            if sick:
                                self.sick[i].add(d)
                            for bi, b in enumerate(bl):
                                if which != "both" and which != bi:
                                    continue
                                s, e = b[1], b[2]
                                if which == "both" and bi == 0 and r.random() < 0.10:
                                    s = s + 60
                                if which == "both" and bi == len(bl) - 1 and r.random() < 0.08:
                                    e = e - 60
                                if e - s >= 40:
                                    day_roster.append((i, d, ln, s, e, sick))
            # slots: who is at the screen, bags, projections
            roster += day_roster
            todays = day_roster
            day_roster = []
            by_lane = defaultdict(list)
            for x in todays:
                by_lane[x[2]].append(x)
            day_tips = []
            for ln in P.LANES:
                for (per, a, b) in lanes_today[ln]:
                    team = [x for x in by_lane[ln] if x[3] < b and x[4] > a]
                    order = list(r.permutation(len(team))) if team else []
                    rot = 0
                    for s in range(a, b, P.SLOT_MIN):
                        e = min(b, s + P.SLOT_MIN)
                        present = [team[j] for j in order if team[j][3] <= s and team[j][4] >= e and not team[j][5]]
                        lamb = self.lam(ln, d, s) * (e - s) / 60.0
                        bags = int(r.poisson(lamb))
                        op = -1
                        if present:
                            op = present[rot % len(present)][0]
                            rot += 1
                        slots_out.append((d, ln, s, e - s, bags, op))
                        ct = not (ln in P.INTL and d < P.INTL_CT)
                        if ct and op >= 0 and bags > 0:
                            n = int(r.binomial(bags, P.TIP_RATE))
                            for _ in range(n):
                                minute = s + r.random() * (e - s)
                                day_tips.append((minute, op, ln, int(r.integers(len(self.fti_obj)))))
            day_tips.sort()
            for minute, op, ln, f in day_tips:
                o = self.off[op]
                ob = int(self.fti_obj[f])
                k = seen[op][ob]
                kf = seenf[op][f]
                base = o["theta"] + self.fti_eff[f]
                since = (d - o["endorsed"]).days
                if 0 <= since < 120:
                    base -= 0.9 * np.exp(-since / 25.0)
                q = 1.0 / (1.0 + np.exp(-base))
                ph = 1.0 - (1.0 - q) * (P.MEMORY ** k)
                hit = bool(r.random() < ph)
                rt = int(np.exp(r.normal(8.45 if hit else 8.9, 0.42)))
                tips.append((op, d, ln, minute, f, hit, k, kf, rt, q))
                seen[op][ob] += 1
                seenf[op][f] += 1
        self.roster = roster
        self.slots = slots_out
        self.tips = tips
