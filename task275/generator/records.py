"""task275 records: the simulated fleet written out as the PO's files.

Nothing here changes a simulated catch. Identities, clock times, species splits, observer weighings, sales, VMS tracks
and terminals come from the records layer's own random streams, so the world the seed search chose is the world the
files describe."""
from __future__ import annotations

import csv
import datetime as dt
import math

import numpy as np

import common as K
import world as W

DAYBOAT = ("TR2", "NEP", "SN", "GN", "LL", "POT")
TOWED = ("TR1", "TR2", "NEP", "BT", "SN")
GEAR = {"TR1": "OTB", "TR2": "OTB", "NEP": "OTB", "BT": "TBB", "SN": "SDN", "GN": "GNS", "LL": "LLS", "POT": "FPO"}
MESH = {"TR1": (100, 120), "TR2": (100, 120), "NEP": (80, 99), "BT": (80, 80), "SN": (100, 110), "GN": (100, 120),
        "LL": (0, 0), "POT": (0, 0)}
STEAM_KN = 9.0
YARD = (55.32, -10.05)        # the slipway the refit passages go to, outside the region
EXTRACT = dt.datetime(2026, 2, 6, 9, 15)


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(head)
        wr.writerows(rows)


def rng(seed, k):
    return np.random.default_rng([seed, k])


def nm(a, b):
    """distance in nautical miles between two (lat, lon) points (equirectangular)"""
    la = math.radians((a[0] + b[0]) / 2)
    dx = (b[1] - a[1]) * 60 * math.cos(la)
    dy = (b[0] - a[0]) * 60
    return math.hypot(dx, dy)


def lerp(a, b, f):
    return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)


def fmt_dt(t):
    return t.strftime("%Y-%m-%d %H:%M")


def kg(x, nd=1):
    return round(float(x), nd)


class Records:
    def __init__(self, seed=K.SEED, w=None):
        self.seed = seed
        self.w = w if w is not None else W.simulate(seed)
        self.V = self.w["V"]
        self.T = self.w["T"]
        self._identities()
        self._times()
        self._landings()
        self._observer()

    # ------------------------------------------------------------------ vessels
    def _identities(self):
        r = rng(self.seed, 101)
        names = list(K.VESSEL_NAMES)
        r.shuffle(names)
        used = set()
        for i, v in enumerate(self.V):
            port = v["port"]
            v["home"] = port[0]
            while True:
                n = int(r.integers(12, 399))
                pln = "%s %d" % (port[1], n)
                if pln not in used:
                    used.add(pln)
                    break
            v["pln"] = pln
            v["name"] = names[i].upper()
            v["rss"] = "C1%04d" % int(r.integers(1000, 9999))
            while v["rss"] in {u.get("rss") for u in self.V[:i]}:
                v["rss"] = "C1%04d" % int(r.integers(1000, 9999))
            base = {"TR1": 26.0, "TR2": 21.0, "NEP": 19.0, "BT": 24.0, "SN": 20.0, "GN": 14.0, "LL": 13.0,
                    "POT": 12.0}[v["seg"]]
            v["kw"] = int(round(base * v["length"] * r.lognormal(0, 0.12)))
            v["built"] = int(r.integers(1978, 2020))
            v["member_since"] = dt.date(int(r.integers(1996, 2021)), int(r.integers(1, 13)), int(r.integers(1, 28)))
            lo, hi = MESH[v["seg"]]
            v["mesh"] = int(lo + 5 * int(r.integers(0, (hi - lo) // 5 + 1))) if hi else 0
        self.by_pln = {v["pln"]: v for v in self.V}

    # ------------------------------------------------------------------ trip clocks
    def _times(self):
        """local departure and return for every trip, then UTC; the landing port and the steaming legs"""
        r = rng(self.seed, 102)
        last = {}
        for t in sorted(self.T, key=lambda t: (t["v"], t["dep"])):
            v = self.V[t["v"]]
            d0 = dt.datetime.combine(t["dep"].date(), dt.time(0))
            g = K.GROUNDS[t["ground"]]
            t["dep_port"] = last.get(t["v"], v["home"])
            home = K.PORT[t["dep_port"]]
            land = v["home"] if r.random() < 0.88 else K.PORTS[int(r.integers(0, len(K.PORTS)))][0]
            t["land_port"] = land
            last[t["v"]] = land
            fish_pt = (g[5][0] + r.uniform(-.6, .6) * g[6][0], g[5][1] + r.uniform(-.6, .6) * g[6][1])
            t["fish_pt"] = fish_pt
            out_h = nm(home[3], fish_pt) / STEAM_KN
            back_h = nm(fish_pt, K.PORT[land][3]) / STEAM_KN
            if v["seg"] in DAYBOAT:
                if r.random() < 0.30 and t["dep"].timetuple().tm_yday > 1:
                    off = r.uniform(-1.0, 1.0)
                else:
                    off = r.uniform(1.0, 6.0)
                dep = d0 + dt.timedelta(hours=float(off))
                span = t["hours"] + 0.35 * (len(t["hauls"]) - 1)
                if t["dur"] == 2:
                    span += 9.0
                ret = dep + dt.timedelta(hours=float(out_h + span + back_h + r.uniform(0.3, 1.2)))
            else:
                dep = d0 + dt.timedelta(hours=float(r.uniform(-5.0, 9.0) if t["dep"].timetuple().tm_yday > 1
                                                    else r.uniform(1.0, 9.0)))
                ret = d0 + dt.timedelta(days=t["dur"] - 1, hours=float(r.uniform(9.0, 21.0)))
                need = out_h + t["hours"] * 1.05 + back_h + 2.0
                if (ret - dep).total_seconds() / 3600 < need:
                    ret = dep + dt.timedelta(hours=float(need))
            end = dt.datetime(K.YEAR, 12, 31, 23, 15)
            if ret > end:
                # the year's last trips are home before midnight
                ret = end - dt.timedelta(minutes=t["id"] % 75)
            t["dep_local"], t["ret_local"] = dep, ret
            t["dep_utc"], t["ret_utc"] = K.to_utc(dep), K.to_utc(ret)
            t["out_h"], t["back_h"] = out_h, back_h
        # the logbook's trip numbers, in order of departure
        order = sorted(self.T, key=lambda t: (t["dep_utc"], t["v"]))
        for i, t in enumerate(order):
            t["trip_id"] = "WC25%06d" % (101 + 7 * i + int(r.integers(0, 6)))

    # ------------------------------------------------------------------ landings by species
    def _landings(self):
        r = rng(self.seed, 103)
        for t in self.T:
            p = W.SPEC[t["seg"]]
            sp = list(p["mix"])
            a = np.array([p["mix"][s] for s in sp]) * 60
            sh = r.dirichlet(a)
            mk = {s: t["mk"] * f for s, f in zip(sp, sh)}
            quota = [s for s in sp if K.SPECIES[s][1] and not K.SPECIES[s][3]]
            if quota:
                qa = np.array([p["mix"][s] for s in quota]) * 40
                bsh = dict(zip(quota, r.dirichlet(qa)))
            else:
                bsh = {}
            lsp = list(p["lmix"])
            lsh = dict(zip(lsp, r.dirichlet(np.array([p["lmix"][s] for s in lsp]) * 40)))
            t["mk_sp"], t["bms_sh"], t["legal_sh"] = mk, bsh, lsh
            lines = []
            for s in sp:
                if mk[s] < 2.0:
                    continue
                f = K.SPECIES[s][4]
                pres = K.SPECIES[s][5]
                prod = int(round(mk[s] * r.lognormal(0, 0.02) / f))
                if prod < 1:
                    continue
                lines.append((s, pres, "Above MCRS", prod, f, kg(prod * f)))
            if t["landed_bms"] > 0.5 and bsh:
                for s in quota:
                    w_ = t["landed_bms"] * bsh[s] * r.lognormal(0, 0.03)
                    prod = int(round(w_))
                    if prod >= 1:
                        lines.append((s, "WHL", "BMS", prod, 1.0, kg(prod)))
            t["lines"] = lines
            t["decl_mk"] = sum(l[5] for l in lines if l[2] == "Above MCRS")
            t["decl_bms"] = sum(l[5] for l in lines if l[2] == "BMS")
            # the skipper's logbook declares discards of the exempted catch only when above 50 kg
            ex = sum(t["legal"] * lsh.get(s, 0) for s in ("NEP", "CRE", "LBE"))
            t["self_dis"] = int(round(ex * r.uniform(0.25, 0.45) / 10.0) * 10) if ex > 50 else 0

    # ------------------------------------------------------------------ observer
    def _observer(self):
        r = rng(self.seed, 104)
        drawn = sorted([t for t in self.T if t["drawn"]], key=lambda t: t["dep_utc"])
        n_obs = 0
        observers = ["OB%02d" % i for i in (2, 3, 5, 6, 8, 9, 11, 12, 14)]
        for i, t in enumerate(drawn):
            t["notified"] = t["dep_local"] + dt.timedelta(hours=float(r.uniform(-1.5, 1.5)))
            if t["observed"]:
                n_obs += 1
                t["obs_ref"] = "WCO25-T%04d" % (100 + n_obs)
                t["observer"] = observers[int(r.integers(0, len(observers)))]
        self.drawn = drawn
        # weighings: every haul the observer attends, every species in each fraction, live weight raised to the haul
        r2 = rng(self.seed, 105)
        r3 = rng(self.seed, 113)
        for t in self.T:
            if not t["observed"]:
                continue
            attend = r3.random(len(t["hauls"])) < 0.985
            if not attend.any():
                attend[int(r3.integers(0, len(t["hauls"])))] = True
            f_ret, f_bms = float(r3.lognormal(0, 0.05)), float(r3.lognormal(0, 0.06))
            g = K.GROUNDS[t["ground"]]
            hl = []
            clock = t["dep_local"] + dt.timedelta(hours=t["out_h"])
            day0 = t["dep_local"].date()
            for j, h in enumerate(t["hauls"]):
                if t["seg"] not in DAYBOAT:
                    # multi-day trips fish through the day and lie to at night
                    day_end = dt.datetime.combine(clock.date(), dt.time(22, 0))
                    if clock + dt.timedelta(hours=h["hours"]) > day_end:
                        clock = dt.datetime.combine(clock.date() + dt.timedelta(days=1), dt.time(4, 0)) + \
                            dt.timedelta(minutes=int(r2.integers(0, 50)))
                shot = clock
                haul = shot + dt.timedelta(hours=h["hours"])
                pos = (g[5][0] + r2.uniform(-.9, .9) * g[6][0], g[5][1] + r2.uniform(-.9, .9) * g[6][1])
                lo, hi = [int(x) for x in g[2].replace(" m", "").split("-")]
                rows = []
                for s, w_ in t["mk_sp"].items():
                    x = w_ * h["mk"] / t["mk"] * r2.lognormal(0, 0.05) * f_ret
                    if x >= 0.1:
                        rows.append((s, "RET", kg(x)))
                for s, f in t["bms_sh"].items():
                    x = h["bms"] * f * r2.lognormal(0, 0.05) * f_bms
                    if x >= 0.1:
                        rows.append((s, "BMS", kg(x)))
                for s, f in t["legal_sh"].items():
                    x = h["legal"] * f * r2.lognormal(0, 0.05)
                    if x >= 0.1:
                        rows.append((s, "DIS", kg(x)))
                hl.append(dict(no=j + 1, shot=shot, haul=haul, pos=pos, depth=int(r2.integers(lo, hi + 1)),
                               rows=rows, hours=h["hours"], attended=bool(attend[j])))
                clock = haul + dt.timedelta(minutes=int(r2.integers(15, 45)))
            t["obs_hauls"] = hl
            del day0

    # ------------------------------------------------------------------ the files
    def register_rows(self):
        head = ["rss_no", "vessel_pln", "vessel_name", "segment", "gear", "overall_length_m", "engine_kw", "year_built",
                "home_port", "member_since"]
        rows = []
        for v in sorted(self.V, key=lambda v: (K.SEG.index(v["seg"]), v["pln"])):
            rows.append([v["rss"], v["pln"], v["name"], v["seg"], GEAR[v["seg"]], "%.2f" % v["length"], v["kw"],
                         v["built"], K.PORT[v["home"]][2], v["member_since"].isoformat()])
        return head, rows

    def trip_rows(self):
        head = ["trip_id", "vessel_pln", "rss_no", "departure_utc", "departure_port", "return_utc", "return_port",
                "gear", "mesh_mm", "po_ground", "hauls", "fishing_hours", "discards_declared_kg"]
        rows = []
        for t in sorted(self.T, key=lambda t: t["trip_id"]):
            v = self.V[t["v"]]
            rows.append([t["trip_id"], v["pln"], v["rss"], fmt_dt(t["dep_utc"]), K.PORT[t["dep_port"]][2],
                         fmt_dt(t["ret_utc"]), K.PORT[t["land_port"]][2], GEAR[v["seg"]],
                         v["mesh"] if v["mesh"] else "", K.GR[t["ground"]], len(t["hauls"]),
                         "%.1f" % t["hours"], t["self_dis"]])
        return head, rows

    def landing_rows(self):
        head = ["trip_id", "vessel_pln", "landing_date", "landing_port", "species", "presentation", "mcrs_status",
                "live_weight_kg"]
        rows = []
        for t in sorted(self.T, key=lambda t: t["trip_id"]):
            v = self.V[t["v"]]
            for s, pres, st, prod, f, live in t["lines"]:
                rows.append([t["trip_id"], v["pln"], t["ret_local"].date().isoformat(), K.PORT[t["land_port"]][2], s,
                             pres, st, "%.1f" % live])
        return head, rows

    def deployment_rows(self):
        """the coordinator's log: every drawn trip, typed by the coordinator from the skipper's notification"""
        r = rng(self.seed, 106)
        head = ["deployment_ref", "notified_departure", "vessel_pln", "vessel_name", "outcome", "observer",
                "observer_trip_ref", "hauls_sampled"]
        recs = []
        for t in self.drawn:
            v = self.V[t["v"]]
            u = r.random()
            pln = v["pln"] if u < 0.72 else (v["pln"].replace(" ", "") if u < 0.93 else v["pln"].replace(" ", "-"))
            name = v["name"] if r.random() < 0.8 else v["name"].title()
            if t["observed"]:
                recs.append((t["notified"], [pln, name, "Observed", t["observer"], t["obs_ref"],
                                             sum(h["attended"] for h in t["obs_hauls"])]))
            else:
                recs.append((t["notified"], [pln, name, "No observer available", "", "", ""]))
        # notified trips that were drawn and did not sail
        for v in self.V:
            if r.random() < 0.18:
                own = sorted(t["dep_local"] for t in self.T if t["v"] == v["idx"])
                for _ in range(int(r.integers(1, 3))):
                    day = W.START + dt.timedelta(days=int(r.integers(5, 360)))
                    if any(abs((x.date() - day).days) <= 1 for x in own):
                        continue
                    when = dt.datetime.combine(day, dt.time(int(r.integers(1, 7)), int(r.integers(0, 60))))
                    recs.append((when, [v["pln"], v["name"], "Trip cancelled", "", "", ""]))
        recs.sort(key=lambda x: x[0])
        rows = []
        for i, (when, rest) in enumerate(recs):
            rows.append(["D25-%04d" % (i + 1), fmt_dt(when)] + rest)
        return head, rows

    def haul_rows(self):
        head = ["observer_trip_ref", "haul_no", "shot_local", "hauled_local", "shot_lat", "shot_lon", "depth_m",
                "species", "fraction", "weight_kg"]
        rows = []
        for t in sorted([t for t in self.T if t["observed"]], key=lambda t: t["obs_ref"]):
            for h in t["obs_hauls"]:
                if not h["attended"]:
                    continue
                for s, frac, x in h["rows"]:
                    rows.append([t["obs_ref"], h["no"], fmt_dt(h["shot"]), fmt_dt(h["haul"]), "%.4f" % h["pos"][0],
                                 "%.4f" % h["pos"][1], h["depth"], s, frac, "%.1f" % x])
        return head, rows

    def ground_rows(self):
        head = ["po_ground", "ground_name", "depth_band", "sediment", "distance_offshore_nm", "lat_min", "lat_max",
                "lon_min", "lon_max"]
        rows = []
        for code, name, depth, sed, dist, c, hs in K.GROUNDS:
            rows.append([code, name, depth, sed, dist, "%.2f" % (c[0] - hs[0]), "%.2f" % (c[0] + hs[0]),
                         "%.2f" % (c[1] - hs[1]), "%.2f" % (c[1] + hs[1])])
        return head, rows

    def species_rows(self):
        head = ["species_code", "common_name", "scientific_name", "landing_obligation", "mcrs_cm",
                "survivability_exemption", "usual_presentation", "conversion_factor"]
        rows = []
        for s, (name, quota, mcrs, ex, f, pres, _) in K.SPECIES.items():
            rows.append([s, name, K.SCIENTIFIC[s], "Y" if quota else "N", mcrs if mcrs else "",
                         "Y" if ex else "N", pres, "%.2f" % f])
        return head, rows

    def port_rows(self):
        head = ["port_code", "port_name", "harbour_lat", "harbour_lon", "port_limit_radius_nm", "fish_market"]
        return head, [[c, n, "%.3f" % ll[0], "%.3f" % ll[1], "%.1f" % rad, "Y" if auc else "N"]
                      for c, _, n, ll, rad, auc in K.PORTS]

    # ------------------------------------------------------------------ sales notes
    GRADE = {1: 1.25, 2: 1.0, 3: 0.82, 4: 0.68}
    SHELL = ("NEP", "CRE", "LBE", "WHE")
    CLOSED = {dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 12, 25),
              dt.date(2025, 12, 26), dt.date(2026, 1, 1)}

    def _market_day(self, d, landed_at):
        """the fish markets sell from 06:00 Monday to Saturday: fish landed after 05:00 goes to the next sale"""
        day = d.date() + dt.timedelta(days=1) if landed_at.hour >= 5 else d.date()
        while day.weekday() == 6 or day in self.CLOSED:
            day += dt.timedelta(days=1)
        return day

    def _grades(self, r, s, w):
        if s in ("LBE", "WHE"):
            return [(1, 1.0)]
        n = 1 if w < 120 else (2 if w < 600 else (3 if s in ("NEP", "CRE") else int(r.integers(3, 5))))
        n = min(n, 2) if s == "CRE" else n
        sh = r.dirichlet(np.ones(n) * 6)
        start = 1 if n >= 3 or r.random() < 0.5 else 2
        return [(start + i if start + i <= 4 else 4, float(sh[i])) for i in range(n)]

    def sales(self):
        """every first sale of the members' landings, with the copies one merchant filed of its market purchases"""
        if hasattr(self, "_sales_cache"):
            return self._sales_cache
        r = rng(self.seed, 107)
        phase = {s: float(r.uniform(0, 12)) for s in K.SPECIES}
        mkt = {}

        def market(port, day):
            k = (port, day)
            if k not in mkt:
                mkt[k] = float(r.lognormal(0, 0.05))
            return mkt[k]

        def price(s, grade, day, port, auction):
            base = K.SPECIES[s][6] * self.GRADE[grade]
            season = 1 + 0.12 * math.sin(2 * math.pi * (day.month - phase[s]) / 12)
            p = base * season * market(port, day) * r.lognormal(0, 0.06) * (1.03 if auction else 1.0)
            return round(p, 2)

        landings = []
        for t in self.T:
            prod = {}
            for s, pres, st, pw, f, live in t["lines"]:
                if st == "Above MCRS":
                    prod[s] = (pw, pres)
            landings.append(dict(v=t["v"], when=t["ret_local"], port=t["land_port"], prod=prod, trip=t["trip_id"]))
        # landings either side of the year, from the same vessels, for the notes the extract window takes in
        for v in self.V:
            own = [t for t in self.T if t["v"] == v["idx"]]
            rate = len(own) / 365.0 * 0.8
            days = [dt.date(2024, 12, 27) + dt.timedelta(days=i) for i in range(5)] + \
                   [dt.date(2026, 1, 2) + dt.timedelta(days=i) for i in range(23)]
            for d in days:
                if d.weekday() == 6 or r.random() > rate:
                    continue
                src = own[int(r.integers(0, len(own)))]
                f = float(r.uniform(0.6, 1.15))
                prod = {}
                for s, pres, st, pw, cf, live in src["lines"]:
                    if st == "Above MCRS":
                        x = int(round(pw * f))
                        if x >= 1:
                            prod[s] = (x, pres)
                when = dt.datetime.combine(d, dt.time(int(r.integers(9, 20)), int(r.integers(0, 60))))
                landings.append(dict(v=v["idx"], when=when, port=v["home"], prod=prod, trip=None))
        landings.sort(key=lambda x: (x["when"], x["v"]))
        seq = {b[0]: int(r.integers(1000, 4000)) for b in K.BUYERS}
        notes = []          # (note_no, buyer, sale_day, landing, lines[(s, pres, grade, w, p, v)], submitted_local)
        copies = []
        buyers = {b[0]: b for b in K.BUYERS}
        for L in landings:
            port = L["port"]
            auction = K.PORT[port][5]
            if auction:
                day = self._market_day(L["when"], L["when"])
                lines, quay = [], []
                for s, (pw, pres) in sorted(L["prod"].items()):
                    for grade, share in self._grades(r, s, pw):
                        whole = pw * share
                        if whole >= 40 and r.random() < 0.06:
                            # part of the grade sold on the quay by private treaty before the sale
                            f = float(r.uniform(0.2, 0.4))
                            qw = round(whole * f * r.lognormal(0, 0.015), 1)
                            qp = round(price(s, grade, L["when"].date(), port, False) * r.lognormal(0, 0.04), 2)
                            quay.append((s, pres, grade, qw, qp, round(qw * qp, 2)))
                            whole *= 1 - f
                        w = round(whole * (1 - r.uniform(0.005, 0.06)), 1)
                        if w < 0.5:
                            continue
                        pr = price(s, grade, day, port, True)
                        lines.append((s, pres, grade, w, pr, round(w * pr, 2)))
                # the quay's scale never lands within 5 per cent of one of the market's lots of the species, whatever
                # its grade, so a lot is told from a private sale without the grade
                for k, (s, pres, grade, qw, qp, qv) in enumerate(quay):
                    lots_s = [l[3] for l in lines if l[0] == s]
                    f = 1.0
                    while any(abs(qw * f - m) <= 0.05 * m for m in lots_s):
                        f *= 0.93
                    if f != 1.0:
                        nw = round(qw * f, 1)
                        quay[k] = (s, pres, grade, nw, qp, round(nw * qp, 2))
                if not lines:
                    continue
                bcode = "RB0412" if port == "KMH" else "RB0437"
                seq[bcode] += 1
                sub = dt.datetime.combine(day, dt.time(int(r.integers(13, 18)), int(r.integers(0, 60))))
                notes.append(dict(no="%s/25/%05d" % ("KHFM" if port == "KMH" else "BFM", seq[bcode]), buyer=bcode,
                                  day=day, L=L, lines=lines, sub=sub, copy=False))
                if quay:
                    qb = ("RB1186", "RB1203", "RB1311")[int(r.integers(0, 3))]
                    seq[qb] += 1
                    qday = L["when"].date()
                    qsub = dt.datetime.combine(qday, dt.time(int(r.integers(15, 23)), int(r.integers(0, 60))))
                    notes.append(dict(no="%s-%06d" % (qb[2:], seq[qb]), buyer=qb, day=qday, L=L, lines=quay,
                                      sub=qsub, copy=False))
                if day >= K.DEVICE_FROM and len(lines) > 1 and r.random() < 0.30:
                    # the merchant buys one of the smaller lots, and its new invoicing system files the purchase
                    # as a sales note: its own weighing and the price it paid with the market's buyer's commission
                    med = sorted(l[3] for l in lines)[len(lines) // 2]
                    small = [l for l in lines if l[3] < med] or lines
                    s_, pres_, g_, w_, p_, v_ = small[int(r.integers(0, len(small)))]
                    cw = round(w_ * r.uniform(0.985, 1.015), 1)
                    cp = round(p_ * r.uniform(1.03, 1.06), 2)
                    copies.append((day, L, [(s_, pres_, g_, cw, cp, round(cw * cp, 2))]))
            else:
                fish = {s: x for s, x in L["prod"].items() if s not in self.SHELL}
                shell = {s: x for s, x in L["prod"].items() if s in self.SHELL}
                day = L["when"].date() if L["when"].hour < 20 else L["when"].date() + dt.timedelta(days=1)
                for group, kind in ((fish, "merchant"), (shell, "shellfish")):
                    if not group:
                        continue
                    cands = [b[0] for b in K.BUYERS if b[2] == kind and port in b[3]]
                    if r.random() < 0.22 and len(cands) > 1 and len(group) > 1:
                        pick = [str(x) for x in r.choice(cands, size=2, replace=False)]
                        split = {s: pick[int(r.integers(0, 2))] for s in group}
                    else:
                        b0 = cands[int(r.integers(0, len(cands)))]
                        split = {s: b0 for s in group}
                    for bcode in sorted(set(split.values())):
                        lines = []
                        for s in sorted(s for s in group if split[s] == bcode):
                            pw, pres = group[s]
                            for grade, share in self._grades(r, s, pw):
                                w = round(pw * share * r.lognormal(0, 0.015), 1)
                                if w < 0.5:
                                    continue
                                pr = price(s, grade, day, port, False)
                                lines.append((s, pres, grade, w, pr, round(w * pr, 2)))
                        if not lines:
                            continue
                        seq[bcode] += 1
                        sub = dt.datetime.combine(day, dt.time(int(r.integers(15, 23)), int(r.integers(0, 60)))) + \
                            dt.timedelta(days=int(r.integers(0, 2)))
                        notes.append(dict(no="%s-%06d" % (bcode[2:], seq[bcode]), buyer=bcode, day=day, L=L,
                                          lines=lines, sub=sub, copy=False))
        # the merchant's own notes for what it bought on the markets, from its new invoicing system
        for day, L, mine in copies:
            seq[K.DEVICE_BUYER] += 1
            sub = dt.datetime.combine(day + dt.timedelta(days=int(r.integers(1, 3))),
                                      dt.time(int(r.integers(8, 19)), int(r.integers(0, 60))))
            notes.append(dict(no="%s-%06d" % (K.DEVICE_BUYER[2:], seq[K.DEVICE_BUYER]), buyer=K.DEVICE_BUYER, day=day,
                              L=L, lines=list(mine), sub=sub, copy=True))
        lo, hi = dt.date(2025, 1, 1), dt.date(2026, 1, 31)
        notes = [n for n in notes if lo <= n["day"] <= hi]
        notes.sort(key=lambda n: (n["sub"], n["no"]))
        del buyers
        self._sales_cache = notes
        return notes

    def sales_rows(self):
        head = ["sales_note_no", "buyer_reg_no", "buyer_name", "sale_date", "landing_date", "port_of_landing",
                "vessel_pln", "vessel_name", "species", "presentation", "size_grade", "weight_kg", "price_gbp_per_kg",
                "value_gbp", "submitted_utc"]
        bname = {b[0]: b[1] for b in K.BUYERS}
        rows = []
        for n in self.sales():
            v = self.V[n["L"]["v"]]
            name = v["name"] if n["buyer"] in ("RB0412", "RB0437", "RB2040") else v["name"].title()
            for s, pres, grade, w, pr, val in n["lines"]:
                rows.append([n["no"], n["buyer"], bname[n["buyer"]], n["day"].isoformat(),
                             n["L"]["when"].date().isoformat(), K.PORT[n["L"]["port"]][2], v["pln"], name, s, pres,
                             grade, "%.1f" % w, "%.2f" % pr, "%.2f" % val, fmt_dt(K.to_utc(n["sub"]))])
        return head, rows

    # ------------------------------------------------------------------ VMS terminals, passages and positions
    MODELS = ("Seatrack ST-30", "Seatrack ST-41", "Oceanlink OL-7")

    def _at_sea_days(self, vi):
        out = set()
        for t in self.T:
            if t["v"] == vi:
                d = t["dep_local"].date()
                while d <= t["ret_local"].date():
                    out.add(d)
                    d += dt.timedelta(days=1)
        for a, b, _, _ in self.V[vi].get("passages", []):
            d = K.to_local(a).date()
            while d <= K.to_local(b).date():
                out.add(d)
                d += dt.timedelta(days=1)
        return out

    def _passages(self):
        """refit passages to the slipway outside the region: no fishing, so no logbook trip"""
        r = rng(self.seed, 108)
        for v in self.V:
            v["passages"] = []
            if r.random() > 0.32:
                continue
            own = sorted((t["dep_local"], t["ret_local"]) for t in self.T if t["v"] == v["idx"])
            gaps = [(own[i][1], own[i + 1][0]) for i in range(len(own) - 1)
                    if (own[i + 1][0] - own[i][1]).days >= 6]
            if not gaps:
                continue
            a, b = gaps[int(r.integers(0, len(gaps)))]
            leg = nm(K.PORT[v["home"]][3], YARD) / STEAM_KN
            start = a + dt.timedelta(days=1, hours=float(r.uniform(-4, 6)))
            arrive = start + dt.timedelta(hours=leg)
            stay = int(r.integers(1, max(2, (b - a).days - 4)))
            leave = arrive + dt.timedelta(days=stay, hours=float(r.uniform(-6, 6)))
            back = leave + dt.timedelta(hours=leg)
            if back > b - dt.timedelta(hours=20):
                continue
            v["passages"].append((K.to_utc(start), K.to_utc(back), K.to_utc(arrive), K.to_utc(leave)))

    def terminals(self):
        """every terminal installation: one terminal a vessel, and the faulty terminals swapped during the year, the
        refurbished ones later fitted to another vessel"""
        if hasattr(self, "_term"):
            return self._term
        self._passages()
        r = rng(self.seed, 109)
        used = set()

        def unit():
            while True:
                u = "ST%06d" % int(r.integers(100000, 999999))
                if u not in used:
                    used.add(u)
                    return u
        inst = []
        cur = {}
        for v in self.V:
            u = unit()
            start = dt.date(int(r.integers(2016, 2025)), int(r.integers(1, 13)), int(r.integers(1, 28)))
            inst.append(dict(unit=u, model=self.MODELS[int(r.integers(0, 2))], v=v["idx"], start=start, end=None))
            cur[v["idx"]] = inst[-1]
        busy = {v["idx"]: self._at_sea_days(v["idx"]) for v in self.V}
        by_seg = {s: [v["idx"] for v in self.V if v["seg"] == s] for s in K.SEG}
        for s in by_seg:
            r.shuffle(by_seg[s])
        taken = set()
        self.moves = []
        for k in range(14):
            ps, qs = K.SEG[k % 8], K.SEG[(k + 3 + k // 8) % 8]
            P = next(x for x in by_seg[ps] if x not in taken)
            Q = next(x for x in by_seg[qs] if x not in taken)
            taken.update((P, Q))
            for _ in range(400):
                d1 = dt.date(2025, 2, 20) + dt.timedelta(days=int(r.integers(0, 200)))
                if d1 not in busy[P]:
                    break
            for _ in range(400):
                d2 = d1 + dt.timedelta(days=int(r.integers(21, 70)))
                if d2 not in busy[Q] and d2 < dt.date(2025, 12, 12):
                    break
            X = cur[P]
            X["end"] = d1
            Y = dict(unit=unit(), model=self.MODELS[int(r.integers(0, 3))], v=P, start=d1, end=None)
            Z = cur[Q]
            Z["end"] = d2
            X2 = dict(unit=X["unit"], model=X["model"], v=Q, start=d2, end=None)
            inst += [Y, X2]
            cur[P], cur[Q] = Y, X2
            self.moves.append(dict(P=P, Q=Q, d1=d1, d2=d2, unit=X["unit"]))
        # a few terminals simply replaced, the old one scrapped
        for v in self.V:
            if v["idx"] in taken or r.random() > 0.08:
                continue
            for _ in range(400):
                d = dt.date(2025, 1, 15) + dt.timedelta(days=int(r.integers(0, 320)))
                if d not in busy[v["idx"]]:
                    break
            cur[v["idx"]]["end"] = d
            Y = dict(unit=unit(), model=self.MODELS[int(r.integers(0, 3))], v=v["idx"], start=d, end=None)
            inst.append(Y)
            cur[v["idx"]] = Y
        self._term = inst
        return inst

    def label(self):
        """the vessel each terminal is assigned to in the provider's system at the extract"""
        lab = {}
        for i in sorted(self.terminals(), key=lambda i: (i["start"], i["end"] or dt.date(2100, 1, 1))):
            lab[i["unit"]] = i["v"]
        return lab

    def _legs(self, vi):
        """the vessel's at-sea legs in UTC with a position function each"""
        legs = []
        for t in self.T:
            if t["v"] != vi:
                continue
            legs.append(("trip", t["dep_utc"], t["ret_utc"], t))
        for a, b, arr, lv in self.V[vi]["passages"]:
            legs.append(("out", a, arr, None))
            legs.append(("back", lv, b, None))
        legs.sort(key=lambda x: x[1])
        return legs

    def _pos(self, r, leg, when):
        kind, a, b, t = leg
        v = self.V[t["v"]] if t is not None else None
        h = (when - a).total_seconds() / 3600
        tot = (b - a).total_seconds() / 3600
        if kind != "trip":
            return None
        if h < t["out_h"]:
            p = lerp(K.PORT[t["dep_port"]][3], t["fish_pt"], h / t["out_h"])
            return p, r.uniform(8.3, 9.8)
        if h > tot - t["back_h"]:
            f = (h - (tot - t["back_h"])) / t["back_h"]
            return lerp(t["fish_pt"], K.PORT[t["land_port"]][3], f), r.uniform(8.3, 9.8)
        g = K.GROUNDS[t["ground"]]
        p = (g[5][0] + r.uniform(-.9, .9) * g[6][0], g[5][1] + r.uniform(-.9, .9) * g[6][1])
        sp = r.uniform(2.4, 3.9) if v["seg"] in TOWED else r.uniform(0.0, 2.2)
        return p, sp

    def pings(self):
        """every position report in 2025 UTC: (unit, utc, lat, lon, speed, course, true vessel)"""
        if hasattr(self, "_pings"):
            return self._pings
        inst = self.terminals()
        r = rng(self.seed, 110)
        port_on = {v["idx"]: r.random() < 0.22 for v in self.V}
        phase = {}
        out = []
        y0 = dt.datetime(2025, 1, 1)
        y1 = dt.datetime(2026, 1, 1)
        for i in sorted(inst, key=lambda i: (i["v"], i["start"])):
            if i["unit"] not in phase:
                phase[i["unit"]] = int(r.integers(0, 120))
            vi = i["v"]
            v = self.V[vi]
            a = max(y0, K.to_utc(dt.datetime.combine(i["start"], dt.time(12))))
            b = min(y1, K.to_utc(dt.datetime.combine(i["end"], dt.time(12)))) if i["end"] else y1
            if b <= a:
                continue
            legs = self._legs(vi)
            # passages' positions along the coast to the slipway
            k0 = int(math.ceil(((a - y0).total_seconds() / 60 - phase[i["unit"]]) / 120.0))
            when = y0 + dt.timedelta(minutes=phase[i["unit"]] + 120 * k0)
            li = 0
            berth = None
            while when < b:
                while li < len(legs) and legs[li][2] < when:
                    li += 1
                leg = legs[li] if li < len(legs) and legs[li][1] <= when <= legs[li][2] else None
                if leg is not None:
                    if leg[0] == "trip":
                        p, sp = self._pos(r, leg, when)
                    else:
                        f = (when - leg[1]).total_seconds() / max(1.0, (leg[2] - leg[1]).total_seconds())
                        home = K.PORT[v["home"]][3]
                        p = lerp(home, YARD, f) if leg[0] == "out" else lerp(YARD, home, f)
                        sp = r.uniform(8.0, 9.6)
                    out.append((i["unit"], when, p[0], p[1], sp, vi))
                else:
                    nxt = legs[li] if li < len(legs) else None
                    prev = legs[li - 1] if li > 0 else None
                    in_yard = prev is not None and prev[0] == "out"
                    if port_on[vi] and not in_yard and ((when - y0).total_seconds() // 7200) % 2 == 0:
                        pt = K.PORT[prev[3]["land_port"]][3] if prev is not None and prev[0] == "trip" else \
                            K.PORT[v["home"]][3]
                        out.append((i["unit"], when, pt[0] + r.uniform(-.0015, .0015),
                                    pt[1] + r.uniform(-.0025, .0025), 0.0, vi))
                    elif nxt is not None and nxt[0] == "trip" and 0 < (nxt[1] - when).total_seconds() <= 3600 * 2 \
                            and r.random() < 0.55:
                        pt = K.PORT[nxt[3]["dep_port"]][3]
                        out.append((i["unit"], nxt[1] - dt.timedelta(minutes=int(r.integers(4, 40))),
                                    pt[0] + r.uniform(-.0015, .0015), pt[1] + r.uniform(-.0025, .0025), 0.0, vi))
                when += dt.timedelta(minutes=120)
        # no report sits within a few hundred metres of a port limit, where the distance formula would decide
        moved = []
        for u, when, la, lo, sp, vi in out:
            for c, _, _, ll, rad, _ in K.PORTS:
                d = nm((la, lo), ll)
                if abs(d - rad) < 0.06 and d > 0:
                    f = (rad + 0.08) / d
                    la, lo = ll[0] + (la - ll[0]) * f, ll[1] + (lo - ll[1]) * f
            moved.append((u, when, la, lo, sp, vi))
        out = moved
        out.sort(key=lambda x: (x[1], x[0]))
        # course from each unit's previous report
        prevp = {}
        res = []
        for u, when, la, lo, sp, vi in out:
            if u in prevp and sp > 0.5:
                pla, plo = prevp[u]
                crs = (math.degrees(math.atan2((lo - plo) * math.cos(math.radians(la)), la - pla)) + 360) % 360
            else:
                crs = float(r.integers(0, 360)) if sp > 0.5 else 0.0
            prevp[u] = (la, lo)
            res.append((u, when, la, lo, sp, crs, vi))
        self._pings = res
        return res

    def record(self):
        """the PO's equipment record at the end of the year: each vessel's terminal and the one it carried before,
        that one either taken off during 2025 or, for about half the rest, a unit replaced in an earlier year"""
        if hasattr(self, "_rec"):
            return self._rec
        inst = self.terminals()
        used = {i["unit"] for i in inst}
        r = rng(self.seed, 114)
        rec = {}
        for v in self.V:
            mine = sorted((i for i in inst if i["v"] == v["idx"]), key=lambda i: i["start"])
            cur = mine[-1]
            prev = mine[-2]["unit"] if len(mine) > 1 else ""
            if not prev and cur["start"].year >= 2018 and r.random() < 0.62:
                while True:
                    prev = "ST%06d" % int(r.integers(100000, 999999))
                    if prev not in used:
                        used.add(prev)
                        break
            rec[v["idx"]] = (cur["unit"], cur["model"], prev)
        self._rec = rec
        return rec

    def transponder_rows(self):
        head = ["vessel_pln", "rss_no", "terminal_id", "terminal_model", "previous_terminal_id"]
        rows = []
        rec = self.record()
        for v in sorted(self.V, key=lambda v: v["pln"]):
            u, model, prev = rec[v["idx"]]
            rows.append([v["pln"], v["rss"], u, model, prev])
        return head, rows

    def vms_rows(self):
        head = ["terminal_id", "vessel_pln", "vessel_name", "position_utc", "latitude", "longitude", "speed_kn",
                "course_deg"]
        lab = self.label()
        rows = []
        for u, when, la, lo, sp, crs, vi in self.pings():
            v = self.V[lab[u]]
            rows.append([u, v["pln"], v["name"], when.strftime("%Y-%m-%d %H:%M"), "%.4f" % la, "%.4f" % lo,
                         "%.1f" % sp, "%d" % round(crs) if sp > 0.5 else "0"])
        return head, rows

    # ------------------------------------------------------------------ the two files the analysis does not need
    def gear_rows(self):
        r = rng(self.seed, 111)
        head = ["vessel_pln", "gear", "mesh_mm", "panel_or_grid", "panel_mesh_mm", "gear_size",
                "declared"]
        rows = []
        for v in sorted(self.V, key=lambda v: v["pln"]):
            s = v["seg"]
            decl = [dt.date(2025, 1, int(r.integers(2, 29)))]
            if r.random() < 0.15:
                decl.append(dt.date(2025, int(r.integers(4, 11)), int(r.integers(1, 28))))
            for k, d in enumerate(decl):
                mesh = v["mesh"] if v["mesh"] else ""
                if s in ("TR1", "TR2", "NEP"):
                    dev = "square-mesh panel" if r.random() < (0.35 + 0.3 * k) else "none"
                    dmesh = (120 if s != "NEP" else 100) if dev != "none" else ""
                    size = "headline %d m" % int(r.integers(24, 41) if s == "TR1" else r.integers(16, 31))
                elif s == "BT":
                    dev = "benthic release panel" if r.random() < 0.2 + 0.3 * k else "none"
                    dmesh = 200 if dev != "none" else ""
                    size = "2 x %d m beams" % int(r.integers(8, 13))
                elif s == "SN":
                    dev, dmesh = "none", ""
                    size = "%d coils of rope" % int(r.integers(14, 23))
                elif s == "GN":
                    dev, dmesh = "none", ""
                    size = "%s m of net" % format(int(r.integers(12, 41)) * 100, ",")
                elif s == "LL":
                    dev, dmesh = "none", ""
                    size = "%s hooks" % format(int(r.integers(8, 31)) * 100, ",")
                else:
                    dev, dmesh = "escape gaps" if r.random() < 0.8 else "none", ""
                    size = "%d pots" % int(r.integers(18, 61) * 10)
                rows.append([v["pln"], GEAR[s], mesh, dev, dmesh, size, d.isoformat()])
        return head, rows

    def quota_rows(self):
        r = rng(self.seed, 112)
        mon = {s: [0.0] * 12 for s in K.QUOTA}
        for t in self.T:
            m = t["ret_local"].month - 1
            for s, pres, st, prod, f, live in t["lines"]:
                if s in mon:
                    mon[s][m] += live / 1000.0
        out = []
        for s in K.QUOTA:
            tot = sum(mon[s])
            alloc = round(tot / r.uniform(0.72, 0.97) * 1.0, 1)
            tin = round(alloc * r.uniform(0, 0.08), 1) if r.random() < 0.6 else 0.0
            tout = round(alloc * r.uniform(0, 0.06), 1) if r.random() < 0.5 else 0.0
            out.append(("%s (WC)" % K.SPECIES[s][0], alloc, tin, tout, mon[s]))
        return out
