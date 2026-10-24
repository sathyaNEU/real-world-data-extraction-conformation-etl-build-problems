"""Voltwerk's line from January 2025 to July 2026, driven by the Voltwerk fittings in the Netherlands the world produces:
each fitting is a refurbished pack the line shipped a few days before, built on a work order from a core received
earlier; the failed pack the garage sends back is the next core. Cores are graded at one of two docks, modules come
from stores in supplier lots, every pack runs end-of-line test on one of four benches, and rejected or scrapped cores
go to the recycler. Everything here is read by the asks alone."""
import datetime as dt
from collections import defaultdict, deque

import numpy as np

import params as P
import world as Wd

L0 = dt.date(2025, 1, 1)
L1 = dt.date(2026, 7, 31)
EXPORT = dt.date(2026, 7, 1)          # the morning the exports were pulled
GO_LIVE = dt.date(2025, 1, 6)         # the bench system's first day
WO_FROM = dt.date(2024, 12, 1)        # the MES exports start with the work orders opened in December 2024
PART = {"Volta hatch": "MOD-VLT-12A", "Kestrel SUV": "CAR-KST-2X", "Plover saloon": "MOD-PLV-14S",
        "Mira city car": "MOD-MRA-8C", "Tern van": "MOD-TRN-18P"}
SUPPLIER = {"Volta hatch": "Lucanor Cells GmbH", "Kestrel SUV": "Hanseatic Module Supply",
            "Plover saloon": "Lucanor Cells GmbH", "Mira city car": "Celeste Batteries S.r.l.",
            "Tern van": "Hanseatic Module Supply"}
LOT_SIZE = {"Volta hatch": 600, "Kestrel SUV": 160, "Plover saloon": 300, "Mira city car": 1200, "Tern van": 40}
BMS_PRE = {"Volta hatch": "VLT", "Kestrel SUV": "KSB", "Plover saloon": "PLV", "Mira city car": "MRA",
           "Tern van": "TRN"}
SCRAP_TEARDOWN = ["mechanische schade", "vochtinslag koelcircuit", "thermisch incident", "behuizing gescheurd"]
SCRAP_EOL = ["vochtinslag koelcircuit", "thermisch incident"]
KG = {"Volta hatch": 318, "Kestrel SUV": 486, "Plover saloon": 431, "Mira city car": 214, "Tern van": 512}


def _workday(d, back=True):
    while d.weekday() >= 5:
        d += dt.timedelta(days=-1 if back else 1)
    return d


def _bdays(d, n):
    """n working days after (n > 0) or before (n < 0) d"""
    step = 1 if n > 0 else -1
    k = 0
    while k < abs(n):
        d += dt.timedelta(days=step)
        if d.weekday() < 5:
            k += 1
    return d


def fittings(W, ev):
    """Voltwerk packs fitted in the Netherlands, from the world up to the register's date and at June 2026's rate after
    it (those fittings are after every record in the pack)"""
    rs = np.random.default_rng([P.SEED_FITS, 1])
    alive_then = ev.d.values <= np.minimum(W["exit_d"][ev.i.values], Wd.SNAP)
    e = ev[(ev.cover.values > 0) & (ev.d.values >= W["nl"][ev.i.values]) & alive_then]
    e = e[(e.d >= Wd.day(L0)) & (e.d <= Wd.SNAP)]
    out = [(Wd.date(d), P.NAMES[W["plat"][i]]) for i, d in zip(e.i.values, e.d.values)]
    june = defaultdict(int)
    for d, n in out:
        if d >= dt.date(2026, 6, 1):
            june[n] += 1
    for n in P.NAMES:
        for _ in range(rs.poisson(june[n] * 46 / 30.0)):
            out.append((dt.date(2026, 7, 1) + dt.timedelta(days=int(rs.integers(0, 46))), n))
    out.sort()
    return out


class Line:
    def __init__(self, W, ev, seed=P.SEED_LINE):
        self.rs = np.random.default_rng([seed, 2])
        self.fits = fittings(W, ev)
        self.wo, self.reqs, self.receipts, self.runreq, self.bms, self.ships = [], [], [], [], [], []
        self.intake, self.quarantine = [], []
        self.n = defaultdict(int)

    def _next(self, k):
        self.n[k] += 1
        return self.n[k]

    def _bms(self, name):
        r = self.rs
        return "%s%s%07d" % (BMS_PRE[name], "ABCDEFGH"[int(r.integers(0, 8))], int(r.integers(0, 10 ** 7)))

    # ---- the line -------------------------------------------------------------------------------------------
    def build(self):
        r = self.rs
        cores = {n: deque() for n in P.NAMES}
        for n in P.NAMES:
            weekly = sum(1 for d, x in self.fits if x == n and d < dt.date(2025, 4, 1)) / 13.0
            for _ in range(int(weekly * 4) + 3):
                cores[n].append("K%06d" % (204000 + self._next("core")))
        arrivals = sorted((d + dt.timedelta(days=int(r.integers(4, 22))), P.NAMES.index(n), "garage")
                          for d, n in self.fits)
        jobs = []
        for d, n in self.fits:
            s = _workday(d - dt.timedelta(days=int(r.integers(1, 7))))
            jobs.append((_bdays(s, -int(r.integers(8, 19))), s, n, "ship"))
            u = r.random()
            if u < 0.03:      # torn down and found beyond repair
                jobs.append((_bdays(_workday(d - dt.timedelta(days=int(r.integers(5, 20)))), -int(r.integers(3, 9))),
                             None, n, "teardown"))
            elif u < 0.042:   # failing test twice
                jobs.append((_bdays(_workday(d - dt.timedelta(days=int(r.integers(5, 20)))), -int(r.integers(6, 14))),
                             None, n, "eolscrap"))
        jobs.sort(key=lambda x: (x[0], P.NAMES.index(x[2])))
        ai = 0
        for o, s, n, kind in jobs:
            while ai < len(arrivals) and arrivals[ai][0] <= o:
                self._intake(cores, arrivals[ai][0], P.NAMES[arrivals[ai][1]], "garage")
                ai += 1
            while len(cores[n]) < 3:
                self._intake(cores, _bdays(o, -int(r.integers(1, 4))), n, "inkoop")
            wo = "WO%s-%05d" % (o.strftime("%y"), self._next("wo"))
            self.wo.append(dict(werkorder=wo, geopend=o, platform=n, kerncode=cores[n].popleft(), kind=kind, ship=s))
        while ai < len(arrivals):
            self._intake(cores, arrivals[ai][0], P.NAMES[arrivals[ai][1]], "garage")
            ai += 1
        for rec in self.wo:
            self._work(rec)
        self._holds()
        self._lots()
        self._ensure()
        self._picks()
        self._name_lots()
        self._benches()
        self._close()
        self._recycler()
        self._grades()
        return self

    def _intake(self, cores, d, n, src):
        r = self.rs
        d = _workday(d, back=False)
        tag = "K%06d" % (204000 + self._next("core"))
        dock = 2 if (src == "garage" and r.random() < 0.42) else 1
        rej = r.random() < P.REJECT[n]
        t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=int(r.integers(0, 9 * 60)))
        reason = ""
        if rej:
            reason = ["mechanische schade", "vochtinslag koelcircuit", "thermisch incident", "BMS ontbreekt",
                      "behuizing gescheurd"][int(r.choice(5, p=[0.34, 0.24, 0.12, 0.14, 0.16]))]
        grade = "AFGEKEURD" if rej else ("A" if r.random() < 0.63 else "B")
        self.intake.append(dict(kerncode=tag, ontvangen=t, dock=dock, platform=n, herkomst=src, keuring=grade,
                                reden=reason, scanned=True))
        if rej:
            self.quarantine.append(dict(kerncode=tag, datum=d, platform=n, bron="inname"))
        else:
            cores[n].append(tag)

    def _issue(self, n, d, wo, qty, kind="UITGIFTE", pick=None, lot=None, first=False):
        r = self.rs
        t = dt.datetime.combine(d, dt.time(6, 0)) + dt.timedelta(minutes=int(r.integers(0, 15 * 60)))
        self.reqs.append(dict(t=t, soort=kind, artikel=PART[n], partij=lot, aantal=qty, werkorder=wo, pick=pick,
                              platform=n, true_qty=qty, first=first, hold=None))
        return self.reqs[-1]

    def _work(self, rec):
        r = self.rs
        n, o, kind, wo = rec["platform"], rec["geopend"], rec["kind"], rec["werkorder"]
        if kind == "teardown":
            rec["status"], rec["afgesloten"] = "AFGEKEURD", _bdays(o, int(r.integers(1, 3)))
            self.quarantine.append(dict(kerncode=rec["kerncode"], datum=rec["afgesloten"], platform=n, bron="demontage"))
            return
        units = int(min(P.BOM[n] // P.PER_UNIT[n] - 1, 1 + r.poisson(P.UNITS_MEAN[n] - 1)))
        pday = _bdays(o, int(r.integers(1, 4)))
        self._issue(n, pday, wo, units, first=True)
        if r.random() < 0.10:
            self._issue(n, _bdays(pday, int(r.integers(1, 3))), wo, 1)
        if units >= 2 and r.random() < 0.06:
            self._issue(n, _bdays(pday, int(r.integers(1, 4))), wo, -1, kind="RETOUR")
        pack = self._bms(n)
        asm = dt.datetime.combine(_bdays(pday, 1), dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(0, 420)))
        self.bms.append(dict(werkorder=wo, bms=pack, t=asm, soort="MONTAGE"))
        if r.random() < 0.04:
            pack = self._bms(n)
            self.bms.append(dict(werkorder=wo, bms=pack, t=asm + dt.timedelta(hours=int(r.integers(2, 30))),
                                 soort="VERVANGING"))
        s = rec["ship"]
        d = _bdays(s, -int(r.integers(1, 4))) if s else _bdays(pday, int(r.integers(2, 5)))
        d = max(d, _bdays(asm.date(), 1))
        fails = 0
        while True:
            want = dt.datetime.combine(d, dt.time(int(r.integers(6, 21)), int(r.integers(0, 60))))
            if r.random() < 0.025:
                self._runreq(n, want, pack, "ABORT", wo)
                want = want + dt.timedelta(hours=P.EOL_HOURS[n] * 0.7 + float(r.uniform(0.5, 3.0)))
            if kind == "eolscrap":
                ok = False
            else:
                ok = r.random() < (P.FPY[n] if fails == 0 else P.RETEST_PASS)
            end = self._runreq(n, want, pack, "PASS" if ok else "FAIL", wo)
            if ok:
                break
            fails += 1
            if kind == "eolscrap" and fails == 2:
                rec["status"], rec["afgesloten"] = "AFGEKEURD", _bdays(end.date(), 1)
                self.quarantine.append(dict(kerncode=rec["kerncode"], datum=rec["afgesloten"], platform=n,
                                            bron="eindtest"))
                rec["pack"] = pack
                return
            rw = _workday(end.date(), back=False) if end.date().weekday() >= 5 else end.date()
            self._issue(n, rw, wo, int(r.integers(1, 3)))
            if r.random() < P.BMS_SWAP:
                pack = self._bms(n)
                self.bms.append(dict(werkorder=wo, bms=pack, soort="VERVANGING",
                                     t=dt.datetime.combine(rw, dt.time(10, 0)) + dt.timedelta(minutes=int(r.integers(0, 300)))))
            d = _bdays(rw, 1)
        rec["pack"] = pack
        rec["status"], rec["afgesloten"] = "VERZONDEN", s

    def _runreq(self, n, want, pack, result, wo):
        r = self.rs
        dur = P.EOL_HOURS[n] * float(r.uniform(0.86, 1.14))
        if result == "ABORT":
            dur *= float(r.uniform(0.1, 0.7))
        self.runreq.append(dict(want=want, dur=dur, pakket=pack, resultaat=result, wo=wo, platform=n))
        return want + dt.timedelta(hours=dur)

    def _holds(self):
        """supplier-lot holds: packs that passed test are held back, the lot's units replaced from a replacement lot the
        supplier sends, and the packs run again; stores book the replacement pick once for the batch, and the export
        writes the batch's quantity against every work order on it"""
        r = self.rs
        runs = defaultdict(list)
        for x in self.runreq:
            runs[x["wo"]].append(x)
        asm = {b["werkorder"]: b["t"] for b in self.bms if b["soort"] == "MONTAGE"}
        used = set()
        self.hold_groups = []
        for h_i, (n, k, m) in enumerate(P.HOLDS):
            ok = [w for w in self.wo if w["kind"] == "ship" and w["platform"] == n and w["werkorder"] not in used
                  and P.FY0 + dt.timedelta(days=20) <= w["ship"] <= dt.date(2026, 6, 15)
                  and [x["resultaat"] for x in runs[w["werkorder"]]] == ["PASS"]]
            ok.sort(key=lambda w: w["ship"])
            lo = (h_i * 37 + 11) % max(1, len(ok) - k * 3)
            grp = []
            for a in list(range(lo, len(ok))) + list(range(0, lo)):
                grp = [w for w in ok[a:] if (w["ship"] - ok[a]["ship"]).days <= 10][:k]
                if len(grp) == k:
                    break
            assert len(grp) == k, (n, k, len(ok))
            hold = _bdays(min(w["ship"] for w in grp), -3)
            ready = max(asm[w["werkorder"]] for w in grp)
            if _bdays(ready.date(), 2) > hold:
                continue_ok = False
                for a in range(len(ok)):
                    g2 = [w for w in ok[a:] if (w["ship"] - ok[a]["ship"]).days <= 10][:k]
                    if len(g2) == k:
                        h2 = _bdays(min(w["ship"] for w in g2), -3)
                        if _bdays(max(asm[w["werkorder"]] for w in g2).date(), 2) <= h2:
                            grp, hold, continue_ok = g2, h2, True
                            break
                assert continue_ok, ("no hold group", n)
            lot = self._lot(n, _bdays(hold, -1), k * m + int(r.integers(0, 3)), special=True)
            pick = "hold%d" % h_i
            for w in grp:
                used.add(w["werkorder"])
                x = runs[w["werkorder"]][0]          # its one run moves before the hold
                x["want"] = max(dt.datetime.combine(_bdays(hold, -int(r.integers(1, 3))), dt.time(int(r.integers(6, 15)), 0)),
                                dt.datetime.combine(_bdays(asm[w["werkorder"]].date(), 1), dt.time(6, 0)))
                q = self._issue(n, hold, w["werkorder"], k * m, pick=pick, lot=lot)
                q["t"] = dt.datetime.combine(hold, dt.time(7, 5)) + dt.timedelta(minutes=grp.index(w))
                q["true_qty"] = m
                q["hold"] = h_i
                self._runreq(n, dt.datetime.combine(_bdays(hold, 1), dt.time(int(r.integers(6, 18)), 0)),
                             w["pack"], "PASS", w["werkorder"])
            spare = self.receipts[-1]["aantal"] - k * m
            later = [w for w in self.wo if w["platform"] == n and w["geopend"] > hold and w["kind"] != "teardown"]
            for w in later[:spare]:
                self._issue(n, _bdays(w["geopend"], 2), w["werkorder"], 1, lot=lot)
            self.hold_groups.append(dict(platform=n, k=k, m=m, lot=lot, pick=pick, hold=hold,
                                         wos=[w["werkorder"] for w in grp]))

    def _picks(self):
        """first picks of the same platform on the same day often go out on one shared pick list; every list is
        numbered in the order it was printed"""
        r = self.rs
        by = defaultdict(list)
        for q in self.reqs:
            if q["soort"] == "RETOUR":
                q["pick"] = ""
            elif q["pick"] is None and q["first"] and q.get("with") is None:
                by[(q["t"].date(), q["platform"])].append(q)
        group = {}
        for key in sorted(by, key=lambda x: (x[0], P.NAMES.index(x[1]))):
            qs = sorted(by[key], key=lambda q: q["t"])
            cur, size = None, 0
            for q in qs:
                if cur is None or size >= 3 or r.random() < 0.62:
                    cur, size, t0 = "g%d" % len(group), 0, q["t"]
                    group[cur] = t0
                q["pick"] = cur
                q["t"] = t0 + dt.timedelta(minutes=size)
                size += 1
        for q in self.reqs:
            if q.get("with") is not None:
                q["pick"] = q["with"]["pick"]
                q["t"] = q["with"]["t"] + dt.timedelta(minutes=1)
        for q in self.reqs:
            if q["pick"] is None:
                q["pick"] = "s%d" % self._next("single")
        first = {}
        for q in self.reqs:
            if q["pick"]:
                first[q["pick"]] = min(first.get(q["pick"], q["t"]), q["t"])
        names = {}
        for i, (g, t) in enumerate(sorted(first.items(), key=lambda x: (x[1], x[0])), 1):
            names[g] = "PL%s%05d" % (t.strftime("%y"), 1200 + i)
        for q in self.reqs:
            if q["pick"]:
                q["pick"] = names[q["pick"]]
        for h in self.hold_groups:
            h["pick"] = names[h["pick"]]

    def _ensure(self):
        """every platform's year carries a reject at dock 2 and a shared pick list with two equal quantities"""
        r = self.rs
        fy = lambda d: P.FY0 <= d <= P.FY1
        for n in P.NAMES:
            if not any(x["platform"] == n and x["dock"] == 2 and x["keuring"] == "AFGEKEURD" and fy(x["ontvangen"].date())
                       for x in self.intake):
                d = _bdays(P.FY0, int(r.integers(20, 230)))
                tag = "K%06d" % (204000 + self._next("core"))
                t = dt.datetime.combine(d, dt.time(8, 0)) + dt.timedelta(minutes=int(r.integers(0, 400)))
                self.intake.append(dict(kerncode=tag, ontvangen=t, dock=2, platform=n, herkomst="garage",
                                        keuring="AFGEKEURD", reden="behuizing gescheurd", scanned=True))
                self.quarantine.append(dict(kerncode=tag, datum=d, platform=n, bron="inname"))
            firsts = [q for q in self.reqs if q["platform"] == n and q["first"] and fy(q["t"].date())]
            firsts.sort(key=lambda q: q["t"])
            same = defaultdict(list)
            for q in firsts:
                same[(q["t"].date(), q["partij"])].append(q["aantal"])
            if any(len(v) >= 2 and len(set(v)) < len(v) for v in same.values()):
                continue
            opened = {w["werkorder"]: w["geopend"] for w in self.wo}
            for a, b in zip(firsts[len(firsts) // 3:], firsts[len(firsts) // 3 + 1:]):
                if a["partij"] == b["partij"] and opened[b["werkorder"]] <= a["t"].date():
                    lo = min(a["aantal"], b["aantal"])
                    a["aantal"] = a["true_qty"] = lo
                    b["aantal"] = b["true_qty"] = lo
                    b["with"] = a
                    b["t"] = a["t"] + dt.timedelta(minutes=1)
                    break
            else:
                raise AssertionError("no pair to share a pick list on " + n)

    def _lot(self, n, d, qty, special=False):
        lot = "tmp%05d" % self._next("lot")
        self.receipts.append(dict(datum=d, artikel=PART[n], partij=lot, aantal=qty, leverancier=SUPPLIER[n],
                                  special=special, platform=n))
        return lot

    def _name_lots(self):
        """lots numbered per platform in the order they arrived, delivery notes in date order"""
        names, k = {}, defaultdict(int)
        self.receipts.sort(key=lambda x: (x["datum"], x["partij"]))
        for i, x in enumerate(self.receipts, 1):
            n = x["platform"]
            k[n] += 1
            names[x["partij"]] = "%s%s-%02d" % (P.CODE[n], x["datum"].strftime("%y%m"), k[n])
            x["partij"] = names[x["partij"]]
            x["pakbon"] = "PB%07d" % (5530000 + 7 * i + int(self.rs.integers(0, 7)))
        for q in self.reqs:
            q["partij"] = names[q["partij"]]
        for h in self.hold_groups:
            h["lot"] = names[h["lot"]]

    def _lots(self):
        """supplier lots drawn first in, first out; a new lot arrives two working days before the stock runs out"""
        left, cur, of_wo = defaultdict(int), {}, {}
        for q in sorted(self.reqs, key=lambda q: q["t"]):
            n = q["platform"]
            if q["partij"] is not None:
                of_wo.setdefault(q["werkorder"], q["partij"])
                continue
            if q["soort"] == "RETOUR":
                q["partij"] = of_wo[q["werkorder"]]
                if q["partij"] == cur.get(n):
                    left[n] += 1
                continue
            if left[n] < q["aantal"]:
                cur[n] = self._lot(n, _bdays(q["t"].date(), -2), LOT_SIZE[n])
                left[n] = LOT_SIZE[n]
            q["partij"] = cur[n]
            of_wo.setdefault(q["werkorder"], cur[n])
            left[n] -= q["aantal"]

    def _benches(self):
        """four benches, each running one pack at a time: a run starts when it is wanted or when a bench frees up"""
        # the benches came on line one after another on the go-live morning
        free = {"T1": dt.datetime(2025, 1, 6, 6, 10), "T2": dt.datetime(2025, 1, 6, 6, 55),
                "T3": dt.datetime(2025, 1, 6, 8, 20), "T4": dt.datetime(2025, 1, 6, 10, 5)}
        self.runs = []
        last = defaultdict(lambda: dt.datetime(2000, 1, 1))
        for x in sorted(self.runreq, key=lambda x: (x["want"], x["wo"])):
            want = max(x["want"], last[x["pakket"]] + dt.timedelta(minutes=20))
            b = min(free, key=lambda k: (max(free[k], want), k))
            start = max(free[b], want)
            end = start + dt.timedelta(hours=x["dur"])
            free[b] = end + dt.timedelta(minutes=int(self.rs.integers(15, 50)))
            last[x["pakket"]] = end
            n = x["platform"]
            prog = P.PROGRAM[n][0] if (len(P.PROGRAM[n]) == 1 or start.date() < dt.date(2026, 3, 9)) else P.PROGRAM[n][1]
            self.runs.append(dict(bank=b, start=start, einde=end, pakket=x["pakket"], programma=prog,
                                  resultaat=x["resultaat"], wo=x["wo"], platform=n))
        self.runs.sort(key=lambda x: (x["start"], x["bank"]))
        for i, x in enumerate(self.runs, 1):
            x["run"] = "R%07d" % (1180000 + i)

    def _close(self):
        """shipments, and each work order's state on the morning of the export"""
        r = self.rs
        last_run = defaultdict(lambda: None)
        for x in self.runs:
            last_run[x["wo"]] = x["einde"]
        for w in self.wo:
            if w["kind"] == "ship":
                s = w["ship"]
                if last_run[w["werkorder"]] and last_run[w["werkorder"]].date() >= s:
                    s = _bdays(last_run[w["werkorder"]].date(), 1)
                    w["ship"] = s
                w["afgesloten"] = s
                self.ships.append(dict(zending="Z%06d" % (310000 + self._next("ship")), verzonden=s,
                                       werkorder=w["werkorder"], pakket=w["pack"], platform=w["platform"],
                                       garage=int(r.integers(1, 214))))
            if w["afgesloten"] is None or w["afgesloten"] >= EXPORT:
                w["status_export"] = "IN BEWERKING"
            else:
                w["status_export"] = w["status"]

    def _grades(self):
        """each core's grade on the morning of the export: a pack scrapped on the line takes its core's grade with it,
        with the reason the line recorded"""
        r = np.random.default_rng([P.SEED_LINE, 11])
        scrapped = {w["kerncode"]: w for w in self.wo if w.get("status_export") == "AFGEKEURD"}
        for x in sorted(self.intake, key=lambda x: (x["ontvangen"], x["kerncode"])):
            x["keuring_export"], x["reden_export"] = x["keuring"], x["reden"]
            w = scrapped.get(x["kerncode"])
            if w is not None:
                pool = SCRAP_TEARDOWN if w["kind"] == "teardown" else SCRAP_EOL
                x["keuring_export"], x["reden_export"] = "AFGEKEURD", pool[int(r.integers(0, len(pool)))]

    def _recycler(self):
        """the recycler collects on Wednesdays everything set aside before that day"""
        r = self.rs
        q = sorted(self.quarantine, key=lambda x: (x["datum"], x["kerncode"]))
        rows, note, i = [], 0, 0
        d = dt.date(2025, 1, 1)
        while d <= L1:
            if d.weekday() == 2:
                batch = []
                while i < len(q) and q[i]["datum"] < d:
                    batch.append(q[i]); i += 1
                if batch:
                    note += 1
                    for j, x in enumerate(batch, 1):
                        rows.append(dict(note="BGB-%06d" % (88000 + note), ophaal=d, regel=j, platform=x["platform"],
                                         kg=int(KG[x["platform"]] + r.integers(-12, 13)), kerncode=x["kerncode"],
                                         quarantaine=x["datum"], bron=x["bron"]))
            d += dt.timedelta(days=1)
        self.recycled = rows
