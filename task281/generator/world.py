"""The clean truth: lots, luminaires, poles, every driver's life, every exit, every outage and its reports.

Nothing here is shipped as it stands; records.py writes the files the utility, its installer and the luminaire maker
keep, each in its own form. Times are in days from 2021-01-01 unless a date is named."""
import datetime as dt

import numpy as np

import params as P

EPOCH = dt.date(2021, 1, 1)


def d2i(d):
    return (d - EPOCH).days


def i2d(i):
    return EPOCH + dt.timedelta(days=int(i))


def workdays(a, b):
    out, d = [], a
    while d <= b:
        if d.weekday() < 5 and not (d.month == 12 and d.day >= 22) and not (d.month == 1 and d.day <= 2) \
                and not (d.month == 7 and d.day == 4) and not (d.month == 11 and 22 <= d.day <= 28 and d.weekday() == 3):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


class World:
    def __init__(self, seed=P.SEED):
        # one stream per part of the world, so that a change to the reports or the asks never moves a life
        self.seed = seed
        ss = np.random.SeedSequence(seed).spawn(9)
        self.rngs = [np.random.default_rng(s) for s in ss]
        self.rng = self.rngs[0]
        self.make_lots_and_luminaires()
        self.rng = self.rngs[1]
        self.make_lives()
        self.rng = self.rngs[2]
        self.make_reprog()
        self.rng = self.rngs[5]
        self.make_noncon_poles()
        self.rng = self.rngs[7]
        self.make_circuits()
        self.rng = self.rngs[3]
        lum_out = self.make_outages()
        self.rng = self.rngs[6]
        nc_out = self.make_noncon_outages()
        self.rng = self.rngs[8]
        lum_out += self.make_shields()
        self.rng = self.rngs[7]
        ck_out = self.make_circuit_outages(lum_out)
        # the last outage that darkened each pole, for the residents who report again after a repair
        self._last = {}
        for o in sorted(lum_out + nc_out + ck_out, key=lambda o: o["day"]):
            for p in o["poles"]:
                self._last[p] = id(o)
        self.rng = self.rngs[4]
        rep_l = self.make_reports_2026(lum_out)
        self.rng = self.rngs[6]
        rep_n = self.make_reports_2026(nc_out)
        self.rng = self.rngs[7]
        rep_c = self.make_reports_2026(ck_out)
        rep_x = self.make_foreign_reports()
        self.outages = sorted(lum_out + nc_out + ck_out, key=lambda o: (o["day"], o["pole"], o["kind"]))
        # report numbers run in the order the reports were received, one series since the portal opened; the
        # reports before December 2025 are known here only by the work orders created from them
        pre = sorted([o for o in self.outages if "reported" in o], key=lambda o: (o["reported"], o["pole"]))
        rid = 61204
        for o in pre:
            rid += int(self.rng.integers(1, 4))
            o["pre_id"] = rid
        self.reports = sorted(rep_l + rep_n + rep_c + rep_x, key=lambda x: (x[1]["t"], x[1]["pole"] or 0))
        # the customer system numbers every contact it logs (billing, power outages, streetlights) in one series
        idg = np.random.default_rng(np.random.SeedSequence(seed + 23))
        for o, r in self.reports:
            rid += int(idg.integers(1, 9))
            r["id"] = rid

    # ------------------------------------------------------------------ lots and luminaires
    def make_lots_and_luminaires(self):
        rng = self.rng
        lots, lum = [], []
        pole_ids = rng.permutation(np.arange(400100, 400100 + 60000))
        pole_k = 0
        streets = {t: ["%s %s" % (s, k) for s in rng.choice(STREET_STEMS, 120, replace=False)
                       for k in [rng.choice(["St", "Ave", "Rd", "Dr", "Ln", "Pike", "Way", "Ct"])]]
                   for t in P.TOWN_CODES}
        lot_seq = {}
        for pc, a, b, n, sA, towns in P.PHASES:
            d0, d1 = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
            days = workdays(d0, d1)
            # lots for the phase: catalog by the wattage mix, driver source by lot so the A share lands on sA
            sizes = []
            while sum(sizes) < n:
                sizes.append(int(rng.integers(*P.LOT_SIZE)))
            sizes[-1] -= sum(sizes) - n
            if sizes[-1] < 60:
                sizes[-2] += sizes[-1]
                sizes.pop()
            m = len(sizes)
            watts = rng.choice([40, 70, 110], m, p=[P.WATT_MIX[w] for w in (40, 70, 110)])
            # choose the A lots greedily in a random order until their luminaires reach sA * n
            order = rng.permutation(m)
            src = np.array(["B"] * m, dtype=object)
            acc = 0
            for j in order:
                if acc + sizes[j] / 2 <= sA * n:
                    src[j] = "A"
                    acc += sizes[j]
            # ship dates: lots arrive in install order, two to nine weeks ahead of their first install
            per_day = n / len(days)
            cum = np.cumsum([0] + sizes[:-1])
            for j in range(m):
                first_day = days[min(len(days) - 1, int(cum[j] / per_day))]
                ship = first_day - dt.timedelta(days=int(rng.integers(14, 63)))
                ym = ship.strftime("%y%m")
                lot_seq[ym] = lot_seq.get(ym, 0) + 1
                lot_no = "HL%s-%02d" % (ym, lot_seq[ym])
                rng.choice(["B1", "B2", "B3"]) if src[j] == "A" else rng.choice(["02", "03"])   # (kept: the stream)
                part = P.DRV_PART[src[j]] + "-" + P.DRV_REV[src[j]]
                lots.append(dict(lot=lot_no, phase=pc, ship=ship, watts=int(watts[j]), src=src[j], qty=sizes[j],
                                 drv_part=part, first=first_day))
            # luminaires: installed in order across the phase's workdays, lots consumed in order with a little
            # interleaving (two lots open on the trucks at once)
            phase_lots = lots[-m:]
            seq = []
            for j, L in enumerate(phase_lots):
                seq += [j] * L["qty"]
            seq = np.array(seq)
            # interleave: swap a share of neighbours within a window of about half a lot
            idx = np.arange(n) + rng.normal(0, 90, n)
            seq = seq[np.argsort(idx, kind="stable")]
            day_of = np.sort(rng.integers(0, len(days), n))
            tw = list(towns)
            tp = np.array([towns[t] for t in tw])
            town_of = rng.choice(tw, n, p=tp / tp.sum())
            serial_k = {}
            for i in range(n):
                L = phase_lots[seq[i]]
                serial_k[L["lot"]] = serial_k.get(L["lot"], 0) + 1
                t = town_of[i]
                hps = P.HPS_FOR[L["watts"]]
                hw = int(rng.choice([h for h, _ in hps], p=[q for _, q in hps]))
                lum.append(dict(phase=pc, install=days[day_of[i]], lot=L["lot"], src=L["src"], watts=L["watts"],
                                serial="%s-%04d" % (L["lot"].replace("HL", "HRX"), serial_k[L["lot"]]),
                                pole=int(pole_ids[pole_k]), town=t,
                                street=str(rng.choice(streets[t])), hps_w=hw,
                                crew="B%02d" % int(rng.integers(1, 9))))
                pole_k += 1
        self.lots = lots
        self.lum = lum
        self.streets = streets
        self.pole_ids_left = pole_ids[pole_k:]

    # ------------------------------------------------------------------ lives
    def make_lives(self):
        rng = self.rng
        n = len(self.lum)
        end = d2i(P.RECORD_END)
        for i, L in enumerate(self.lum):
            t0 = d2i(L["install"])
            if L["src"] == "A":
                life = P.LAM_A * rng.weibull(P.K_A)
            else:
                life = rng.exponential(1 / P.RATE_B)
            L["drv_fail"] = t0 + int(round(life * P.YEAR_D)) + 1
            ex = {k: t0 + int(round(rng.exponential(1 / r) * P.YEAR_D)) + 2 for k, r in P.EXIT.items()}
            k = min(ex, key=ex.get)
            L["exit"], L["exit_type"] = ex[k], k
            L["end"] = end
            # after a driver failure the luminaire carries a service driver, which can fail too (drawn whatever
            # happens, so that no luminaire's draws move another's)
            e2 = rng.exponential(1.0)
            L["drv2_fail"] = None
            if L["drv_fail"] < min(L["exit"], end):
                L["drv2_fail"] = L["drv_fail"] + int(round(e2 / P.RATE_B * P.YEAR_D)) + 1

    def make_reprog(self):
        """Some 110 W luminaires were reprogrammed to 70 W after glare complaints, in 2025 and 2026."""
        rng = self.rng
        for L in self.lum:
            t0 = d2i(L["install"])
            L["reprog"] = None
            u = rng.random()
            day = None
            if L["watts"] == 110 and u < P.REPROG_2026 + P.REPROG_2025:
                yr = 2026 if u < P.REPROG_2026 else 2025
                day = d2i(dt.date(yr, 1, 1)) + int(rng.integers(5, 355))
            if day is not None and t0 + 120 < day < min(L["exit"], d2i(P.RECORD_END)) and not (
                    L["exit_type"] == "pole_removed" and L["exit"] <= d2i(P.RECORD_END)):
                L["reprog"] = day

    # ------------------------------------------------------------------ outages (every year) for the work orders
    HARD = ("driver", "knockdown", "luminaire", "pole_removed", "reprogram", "glare_shield")
    PLANNED = ("reprogram", "pole_removed", "glare_shield")

    @staticmethod
    def _one_visit(out, key):
        """A fault within 20 days of another outage on the same light is the same visit's work: keep one."""
        by = {}
        for o in sorted(out, key=lambda o: (o[key], o["day"], o["kind"])):
            by.setdefault(o[key], []).append(o)
        kept = []
        for _, os_ in by.items():
            fixed = [o for o in os_ if o["kind"] in World.HARD]
            for o in os_:
                if o["kind"] in World.HARD:
                    kept.append(o)
                    continue
                if any(abs(q["day"] - o["day"]) <= 20 for q in fixed):
                    continue
                fixed.append(o)
                kept.append(o)
        return kept

    KIND_ID = {"driver": 1, "photocontrol": 2, "wiring": 3, "fuse": 4, "lamp": 5, "ballast": 6, "knockdown": 7,
               "luminaire": 8, "pole_removed": 9, "reprogram": 10, "glare_shield": 11, "ug_cable": 12}

    def _g(self, o, salt):
        """A generator for one outage's draws, so that no other outage's existence moves them."""
        return np.random.default_rng([self.seed, salt, o["pole"], o["day"] + 50000, World.KIND_ID[o["kind"]],
                                      int(o.get("second", False))])

    def _times(self, out):
        """The light goes out in the evening of its day; a report (portal or phone) or a patrol finds it; dispatch
        picks up a report; the crew repairs it some days later."""
        for o in out:
            rng = self._g(o, 1)
            o["dark"] = o["day"] + 0.80                                    # about 7 pm
            o["patrol"] = rng.random() < (0.16 if o["kind"] not in World.PLANNED else 1.0)
            delay = rng.exponential(1.4) + 0.05
            o["found"] = o["dark"] + delay
            o["repair_lag"] = 0.35 + rng.gamma(1.6, 1.15)               # days from dispatch to completion
            if o["kind"] in ("knockdown", "pole_removed"):
                o["repair_lag"] = 0.6 + rng.gamma(2.0, 1.6)

    def make_outages(self):
        rng = self.rng
        end = d2i(P.RECORD_END)
        out = []
        for i, L in enumerate(self.lum):
            t0 = d2i(L["install"])
            stop = min(L["exit"], end)
            u = dict(lum=i, pole=L["pole"], town=L["town"], poles=(L["pole"],))
            # the original driver's failure
            if L["drv_fail"] <= stop:
                out.append(dict(u, kind="driver", day=L["drv_fail"]))
            if L["drv2_fail"] is not None and L["drv2_fail"] <= stop:
                out.append(dict(u, kind="driver", day=L["drv2_fail"], second=True))
            for kind, r in P.OTHER.items():
                t = t0
                while True:
                    t += int(round(rng.exponential(1 / r) * P.YEAR_D)) + 1
                    if t > stop:
                        break
                    out.append(dict(u, kind=kind, day=t))
            if L["exit"] <= end:
                out.append(dict(u, kind=L["exit_type"], day=L["exit"]))
            if L["reprog"] is not None and L["reprog"] <= stop:
                out.append(dict(u, kind="reprogram", day=L["reprog"]))
        self._times(out)
        return self._one_visit(out, "pole")

    def make_circuits(self):
        """Some streets are fed underground: their lights hang on one circuit fed from a riser pole. The GIS records
        each pole's feed."""
        rng = self.rng
        by_street = {}
        for i, L in enumerate(self.lum):
            by_street.setdefault((L["town"], L["street"]), []).append(i)
        self.circuit_of, self.circuits, self.riser = {}, {}, {}
        k = {t: 0 for t in P.TOWN_CODES}
        for (town, street), idx in sorted(by_street.items()):
            if len(idx) < 4 or rng.random() > P.UG_SHARE:
                continue
            idx = sorted(idx, key=lambda i: self.lum[i]["pole"])
            chunks, j = [], 0
            while j < len(idx):
                m = int(rng.integers(4, 10))
                chunks.append(idx[j:j + m])
                j += m
            if len(chunks) > 1 and len(chunks[-1]) < 4:
                tail = chunks.pop()
                chunks[-1] = chunks[-1] + tail
            end = d2i(P.RECORD_END)
            for ch in chunks:
                k[town] += 1
                cid = "UG-%s-%03d" % (town, k[town])
                self.circuits[cid] = ch
                # the riser is a pole that stands to the end of the record
                stand = [i for i in ch if not (self.lum[i]["exit_type"] == "pole_removed" and self.lum[i]["exit"] <= end)]
                self.riser[cid] = self.lum[(stand or ch)[0]]["pole"]
                for i in ch:
                    self.circuit_of[self.lum[i]["pole"]] = cid

    def make_shields(self):
        """A glare complaint is answered with a house-side shield when the light's output can stay as it is."""
        rng = self.rng
        out = []
        end = d2i(P.RECORD_END)
        for i, L in enumerate(self.lum):
            u, yr, dd = rng.random(), rng.random(), int(rng.integers(5, 355))
            if L["reprog"] is not None or L["watts"] == 40 or u > P.SHIELD_RATE:
                continue
            day = d2i(dt.date(2026 if yr < 0.75 else 2025, 1, 1)) + dd
            if d2i(L["install"]) + 120 < day < min(L["exit"], end):
                out.append(dict(lum=i, pole=L["pole"], town=L["town"], poles=(L["pole"],), kind="glare_shield",
                                day=day))
        self._times(out)
        return out

    def make_circuit_outages(self, pole_out):
        """Underground cable faults: each darkens its whole circuit until the cable is spliced. A fault within 30
        days of an outage on one of the circuit's lights is left out (the record would not tell them apart)."""
        rng = self.rng
        end = d2i(P.RECORD_END)
        days_by_pole = {}
        for o in pole_out:
            days_by_pole.setdefault(o["pole"], []).append(o["day"])
        out = []
        for cid, idx in sorted(self.circuits.items()):
            poles = tuple(self.lum[i]["pole"] for i in idx)
            t = -int(rng.integers(0, 365))
            while True:
                t += int(round(rng.exponential(1 / P.UG_FAULT_RATE) * P.YEAR_D)) + 1
                if t > end:
                    break
                if t < 0:
                    continue
                live = tuple(self.lum[i]["pole"] for i in idx if self.lum[i]["exit"] > t + 30 and not (
                    self.lum[i]["exit_type"] == "pole_removed" and self.lum[i]["exit"] <= end))
                if self.riser[cid] not in live or len(live) < 3:
                    continue
                if any(abs(d - t) <= 30 for p in poles for d in days_by_pole.get(p, [])):
                    continue
                if out and out[-1]["circuit"] == cid and t - out[-1]["day"] <= 30:
                    continue
                ri = next(i for i in idx if self.lum[i]["pole"] == self.riser[cid])
                out.append(dict(lum=None, circuit=cid, riser_i=ri, pole=self.riser[cid],
                                town=self.lum[idx[0]]["town"], poles=live, kind="ug_cable", day=t))
        for o in out:
            g = self._g(o, 1)
            o["dark"] = o["day"] + 0.80
            o["patrol"] = g.random() < 0.05
            o["found"] = o["dark"] + g.exponential(0.6) + 0.05
            o["repair_lag"] = 0.8 + g.gamma(2.0, 0.9)
        return out

    def make_noncon_outages(self):
        """The sodium and metal halide lights the conversion did not reach fail too: lamps, ballasts, photocontrols."""
        rng = self.rng
        end = d2i(P.RECORD_END)
        out = []
        for j, N in enumerate(self.noncon):
            u = dict(lum=None, nc=j, pole=N["pole"], town=N["town"], poles=(N["pole"],))
            for kind, r in P.OTHER_HPS.items():
                t = -int(rng.integers(0, 365))
                while True:
                    t += int(round(rng.exponential(1 / r) * P.YEAR_D)) + 1
                    if t > end:
                        break
                    if t >= 0:
                        out.append(dict(u, kind=kind, day=t))
        self._times(out)
        return self._one_visit(out, "pole")

    # ------------------------------------------------------------------ 2026 reports and dispatch
    def make_reports_2026(self, outages):
        """Each outage from December 2025 gets its customer reports and its work order's anchor. Residents report
        through the portal (time stamped in UTC) or by phone (local time), each about the light in front of them.
        Dispatch creates the work order from the report it picks up: usually the first, but a portal report can sit
        in the unassigned queue until a phone report about the same light is taken, and the work order then carries
        the phone report's time. An underground cable fault darkens every light on its circuit: residents report
        whichever light they see, and the work order is the trouble crew's, raised on the circuit's riser pole once
        it has found the fault."""
        lo, hi = d2i(dt.date(2025, 12, 1)), d2i(P.RECORD_END)
        reps = []
        for o in sorted(outages, key=lambda o: (o["day"], o["pole"], o["kind"])):
            rng = self._g(o, 2)
            circuit = o["kind"] == "ug_cable"
            if not (lo <= o["day"] <= hi) or o["kind"] in World.PLANNED:
                o["reports"] = []
                continue
            rs = []
            k = 1 + rng.poisson(1.6 if circuit else 0.55)
            t = o["found"]
            for j in range(k):
                ch = "PORTAL" if rng.random() < 0.58 else "PHONE"
                p = o["poles"][int(rng.integers(0, len(o["poles"])))]
                if not o["patrol"]:
                    rs.append(dict(t=t, ch=ch, pole=p))
                t += rng.exponential(0.8 if circuit else 1.6) + 0.02
            q, sw, dl = rng.random(), rng.exponential(1.2), rng.exponential(0.05)
            anchor = None
            if circuit:
                # the trouble crew sent to the first report finds the cable fault and raises the circuit's order
                created = (rs[0]["t"] + 0.5 + rng.exponential(0.8)) if rs else o["found"]
            elif rs:
                anchor = 0
                if rs[0]["ch"] == "PORTAL" and q < 0.34:
                    later_phone = [j for j in range(1, len(rs)) if rs[j]["ch"] == "PHONE"]
                    if later_phone:
                        anchor = later_phone[0]
                    else:
                        # nobody phoned: the portal report is picked up when the queue is swept
                        rs[0]["swept"] = rs[0]["t"] + 1.5 + sw
                created = rs[anchor].get("swept", rs[anchor]["t"]) + 0.02 + dl
            else:
                created = o["found"]
            o["created"] = created
            o["completed"] = created + o["repair_lag"]
            self._clear_tie(o, rs[0]["t"] if rs else o["found"])
            # once the light is back on nobody reports it out (the re-reports below are the exception)
            rs = [r for r in rs if r["t"] < o["completed"] - 0.01]
            if anchor is not None:
                anchor = min(anchor, len(rs) - 1)
            # residents sometimes report again after the repair (a light flickering back on, or a neighbour's
            # light), only where nothing else darkens that light afterwards in the record
            ra, ta, ca = rng.random(), rng.uniform(0.3, 6.0), rng.random()
            if rs and ra < 0.05 and self._last.get(rs[-1]["pole"]) == id(o):
                rs.append(dict(t=o["completed"] + ta, ch="PORTAL" if ca < .6 else "PHONE", pole=rs[-1]["pole"],
                               after=True))
            for j, r in enumerate(rs):
                r["anchor"] = (j == anchor)
            o["reports"] = rs
            reps += [(o, r) for r in rs]
        # outages before December 2025: a customer's report or a crew's find, then dispatch and the repair
        for o in sorted(outages, key=lambda o: (o["day"], o["pole"], o["kind"])):
            rng = self._g(o, 3)
            if "created" not in o:
                if not o["patrol"] and o["kind"] not in World.PLANNED:
                    o["reported"] = o["found"]
                    o["created"] = o["found"] + (0.5 + rng.exponential(0.8) if o["kind"] == "ug_cable"
                                                 else 0.02 + rng.exponential(0.05))
                else:
                    o["created"] = o["found"]
                o["completed"] = o["created"] + o["repair_lag"]
        return reps

    def make_foreign_reports(self):
        """Residents also report lights the Company does not own (park and parking-lot lights, municipal
        decorative poles): the call centre logs the address, and no work order follows."""
        rng = self.rng
        out = []
        d0, d1 = d2i(dt.date(2025, 12, 1)), d2i(P.RECORD_END)
        n = int(rng.poisson(0.35 * (d1 - d0 + 1)))
        for _ in range(n):
            town = str(rng.choice(P.TOWN_CODES))
            t = d0 + rng.uniform(0, d1 - d0 + 1)
            fake = dict(kind="foreign", town=town, pole=None, lum=None, poles=())
            out.append((fake, dict(t=t, ch="PHONE" if rng.random() < 0.7 else "PORTAL", pole=None, anchor=False,
                                   street=str(rng.choice(self.streets[town])), foreign=True,
                                   house=int(rng.integers(1, 99)) * 20 + 19)))
        return out

    @staticmethod
    def _offset(x):
        """UTC offset in hours of local time x (days from EPOCH): US Eastern, 2 am second Sunday of March to 2 am
        first Sunday of November."""
        t = dt.datetime(EPOCH.year, EPOCH.month, EPOCH.day) + dt.timedelta(minutes=int(round(x * 1440)))
        mar = dt.datetime(t.year, 3, 8)
        while mar.weekday() != 6:
            mar += dt.timedelta(days=1)
        nov = dt.datetime(t.year, 11, 1)
        while nov.weekday() != 6:
            nov += dt.timedelta(days=1)
        return 4 if mar + dt.timedelta(hours=2) <= t < nov + dt.timedelta(hours=2) else 5

    def _clear_tie(self, o, first):
        """A crew's completion stamp is never on the 72-hour mark to the minute, on the wall clock or in elapsed time
        across a clock change."""
        for _ in range(4):
            naive = int(round(o["completed"] * 1440)) - int(round(first * 1440))
            elapsed = naive + 60 * (self._offset(o["completed"]) - self._offset(first))
            lo, hi = min(naive, elapsed), max(naive, elapsed)
            if hi < 4320 - 2 or lo > 4320 + 2:
                return
            if naive >= 4320:
                o["completed"] += (4320 + 7 - lo) / 1440.0
            else:
                o["completed"] -= (hi - 4320 + 7) / 1440.0

    # ------------------------------------------------------------------ poles outside the program
    def make_noncon_poles(self):
        rng = self.rng
        n = 1460
        ids = self.pole_ids_left[:n]
        self.noncon = []
        for i in range(n):
            town = str(rng.choice(P.TOWN_CODES))
            self.noncon.append(dict(pole=int(ids[i]), town=town, street=str(rng.choice(self.streets[town])),
                                    kind=str(rng.choice(["HPS 100 W post-top", "HPS 150 W acorn", "MH 175 W shoebox"],
                                                        p=[.5, .3, .2])),
                                    set_year=int(rng.integers(1978, 2012))))


STREET_STEMS = [
    "Abbott", "Alder", "Ash", "Aspen", "Bancroft", "Barlow", "Beech", "Birch", "Bramble", "Brook", "Calder", "Canal",
    "Cedar", "Chapel", "Cherry", "Church", "Clay", "Clover", "Colfax", "Copper", "Cottage", "Crane", "Cross", "Dale",
    "Delta", "Depot", "Dover", "Eastman", "Elm", "Ember", "Fairview", "Fern", "Field", "Finch", "Forest", "Foster",
    "Garden", "Garfield", "Glen", "Grange", "Granite", "Grove", "Hadley", "Hale", "Harbor", "Hawthorn", "Hazel",
    "Hickory", "High", "Hill", "Holly", "Hollis", "Holt", "Hudson", "Iron", "Ivy", "Juniper", "Kendall", "Kingston",
    "Lake", "Larch", "Laurel", "Linden", "Locust", "Lyle", "Main", "Maple", "Market", "Meadow", "Mercer", "Mill",
    "Milton", "Mulberry", "Myrtle", "North", "Oak", "Orchard", "Osage", "Park", "Pearl", "Pine", "Pleasant", "Poplar",
    "Prospect", "Quarry", "Railroad", "Raven", "Ridge", "River", "Rowan", "Sawmill", "School", "Seneca", "Shady",
    "Spring", "Spruce", "State", "Station", "Stone", "Summit", "Sumner", "Sycamore", "Tanner", "Thorn", "Tower",
    "Union", "Valley", "Vine", "Walnut", "Warren", "Water", "Wayne", "Willow", "Windsor", "Wood", "Wren", "York",
    "Zane", "Alcott", "Baird", "Corwin", "Dunmore", "Ellery", "Fenwick", "Galway", "Harlan", "Ingram", "Jessup",
]
