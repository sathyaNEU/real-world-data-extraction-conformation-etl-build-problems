"""task241 records: the files the institute's systems write from the world. Each file draws from its own generator
(seed + 1000 onwards), so nothing here moves the simulated ocean or another file."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import seawater as SW
import sim

EPOCH = P.EPOCH
ASCENT_SPEED = 0.092                         # m/s, from the profile's deepest level to the surface
CUTOFF = "2028-01-07T07:00:00Z"              # the morning the pack was drawn
PARTNERS = 1                                 # a partner institute's float the data centre decodes beside the array


def juld(t):
    return (t - EPOCH).total_seconds() / 86400.0


def stamp(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


class Records:
    def __init__(self, W, seed=P.SEED):
        self.W = W
        self.seed = seed
        self._register()
        self._partners()
        self._profiles()
        self._reference()

    def rng(self, k):
        return np.random.default_rng([self.seed, 1000 + k])

    # ---------------------------------------------------------------- the float register
    def _register(self):
        rng = self.rng(1)
        fl = sorted(self.W.floats, key=lambda f: f["deployed"])
        for n, f in enumerate(fl):
            f["wmo"] = "19900%02d" % (n + 1)
            f["model"] = "K" if f["deployed"] < dt.date(2025, 1, 1) else "A"
            f["telecom"] = "Argos" if f["model"] == "K" else "Iridium"
            f["serial"] = "%s%04d" % ("K" if f["model"] == "K" else "A", int(rng.integers(1100, 9800)))
            f["ctd"] = "%d" % int(rng.integers(6100, 9900))
            f["descent"] = False
        for f in rng.choice([f for f in fl if f["model"] == "A"], 3, replace=False):
            f["descent"] = True                                      # set to record on the way down as well
        k = [f for f in fl if f["model"] == "K"]
        for f in rng.choice(k, 1, replace=False):
            f["descent"] = True
        self.array = fl

    def register(self):
        rows = []
        for f in self.array:
            rows.append(dict(wmo=f["wmo"], serial=f["serial"], model=f["model"], telecom=f["telecom"], ctd_serial=f["ctd"],
                             deployed=f["deployed"].isoformat(), deploy_lat=round(f["lat0"], 3),
                             deploy_lon=round(f["lon0"], 3),
                             profiles="ascending and descending" if f["descent"] else "ascending",
                             cycle_days=10, park_dbar=1000, profile_dbar=2000))
        return pd.DataFrame(rows)

    # ---------------------------------------------------------------- the partner institute's floats
    def _partners(self):
        """a partner institute's float, decoded by the data centre beside the array: a clean sensor, the same ocean"""
        rng = self.rng(2)
        out = []
        for j in range(PARTNERS):
            f = dict(wmo="19907%02d" % (31 + j), model="A", telecom="Iridium", descent=False, kind="partner",
                     offset=0.0, drift_start=None, drift_rate=0.0)
            lon, lat = float(rng.uniform(-19, -11)), float(rng.uniform(38, 42))
            t = dt.datetime(2026, 12, 20) + dt.timedelta(hours=float(rng.uniform(0, 240)))
            e, cyc, k = float(rng.normal(0, P.EDDY_SD)), [], int(rng.integers(40, 90))
            while t < dt.datetime(P.YEAR + 1, 1, 1):
                k += 1
                t = t + dt.timedelta(days=10, minutes=float(rng.normal(0, 25)))
                lon = sim.reflect(lon + float(rng.normal(-0.012, 0.09)), P.FLOAT_LON)
                lat = sim.reflect(lat + float(rng.normal(-0.006, 0.07)), P.FLOAT_LAT)
                e = P.EDDY_PHI * e + float(rng.normal(0, P.EDDY_SD * np.sqrt(1 - P.EDDY_PHI ** 2)))
                if dt.datetime(P.YEAR, 1, 1) <= t < dt.datetime(P.YEAR + 1, 1, 1):
                    pmax = float(rng.uniform(1985, 2012))
                    p = sim.float_levels(rng, pmax)
                    th, s = sim.column(p, P.H_2027 + e, lon, t.timetuple().tm_yday)
                    cyc.append(dict(cycle=k, time=t, lon=lon, lat=lat, heave=P.H_2027 + e, delta=0.0,
                                    p=p + rng.normal(0, 0.4, p.size),
                                    t=sim.in_situ(th, s, p) + rng.normal(0, 0.0012, p.size),
                                    s=s + rng.normal(0, 0.0015, p.size)))
            f["cycles"] = cyc
            out.append(f)
        self.partners = out

    # ---------------------------------------------------------------- profiles, levels, technical data, deliveries
    def _profiles(self):
        rng = self.rng(3)
        prof, lev, tech, dlv = [], [], [], []
        pid = 0
        for f in self.array + self.partners:
            restart, prev = None, None
            for k, c in enumerate(f["cycles"]):
                surface = c["time"]
                pmax = float(c["p"].max())
                ascent = dt.timedelta(seconds=pmax / ASCENT_SPEED + float(rng.normal(0, 600)))
                start = surface - ascent
                t_prof = start if f["model"] == "K" else surface
                c["surface"], c["ascent_start"], c["juld"] = surface, start, juld(t_prof)
                # real-time flags: a spike now and then in salinity, the odd bad pressure
                n = c["p"].size
                pq, tq, sq = np.ones(n, int), np.ones(n, int), np.ones(n, int)
                s_rep = c["s"].copy()
                if rng.random() < 0.10:
                    j = int(rng.integers(5, n - 2))
                    s_rep[j] += float(rng.choice([-1, 1]) * rng.uniform(0.15, 0.6))
                    sq[j] = 4
                if rng.random() < 0.03:
                    j = int(rng.integers(n // 2, n))
                    sq[j] = 3
                t_spk = c["t"].copy()
                p_flag = c["p"].copy()
                if rng.random() < 0.04:
                    # a temperature spike, most often in the upper ocean's sharp gradients
                    shallow = np.where(c["p"] < 300)[0]
                    j = int(rng.choice(shallow)) if rng.random() < 0.8 else int(rng.integers(0, n))
                    t_spk[j] += float(rng.choice([-1, 1]) * rng.uniform(0.2, 1.1))
                    tq[j] = 4
                if rng.random() < 0.015:
                    # the deepest sample taken as the float turned: pressure jumps and is flagged
                    p_flag[-1] += float(rng.uniform(4, 15))
                    pq[-1] = 4
                p_rep = np.round(p_flag, 1)
                t_rep = np.round(t_spk, 3)
                s_rep = np.round(s_rep, 4)
                pid += 1
                base = dict(wmo=f["wmo"], cycle=c["cycle"], direction="A", juld=round(c["juld"], 6),
                            latitude=round(c["lat"], 3), longitude=round(c["lon"], 3), position_qc=1)
                # deliveries: Iridium within the hour, Argos as the satellite passes allow
                if f["telecom"] == "Iridium":
                    delay = dt.timedelta(minutes=float(rng.uniform(6, 45)))
                    if rng.random() < 0.04:
                        delay += dt.timedelta(hours=float(rng.uniform(2, 30)))
                else:
                    delay = dt.timedelta(hours=float(rng.uniform(8.0, 26.0)))
                    if rng.random() < 0.05:
                        delay += dt.timedelta(hours=float(rng.uniform(10, 40)))
                complete_at = surface + delay
                resent = rng.random() < 0.05
                if resent:
                    # the first transmission broke off part way up the profile; the full profile came later
                    cut = float(rng.uniform(700, 1800))
                    keep = p_rep <= cut
                    first_at = surface + (dt.timedelta(minutes=float(rng.uniform(5, 40))) if f["telecom"] == "Iridium"
                                          else dt.timedelta(hours=float(rng.uniform(1.0, 8.0))))
                    if f["telecom"] == "Iridium":
                        # sent again with the next profile, at the float's next surfacing
                        nxt = f["cycles"][k + 1]["time"] if k + 1 < len(f["cycles"]) else \
                            surface + dt.timedelta(days=10, minutes=float(rng.normal(0, 25)))
                        complete_at = nxt + dt.timedelta(minutes=float(rng.uniform(6, 45)))
                    else:
                        complete_at = first_at + dt.timedelta(hours=float(rng.uniform(3, 30)))
                    prof.append(dict(profile_id="P%06d" % pid, **base, file_version=1))
                    for a, b, cc, d1, d2, d3 in zip(p_rep[keep], t_rep[keep], s_rep[keep], pq[keep], tq[keep], sq[keep]):
                        lev.append(("P%06d" % pid, a, b, cc, d1, d2, d3))
                    dlv.append(dict(profile_id="P%06d" % pid, wmo=f["wmo"], cycle=c["cycle"], direction="A", file_version=1,
                                    delivered=stamp(first_at), n_levels=int(keep.sum())))
                    pid += 1
                prof.append(dict(profile_id="P%06d" % pid, **base, file_version=2 if resent else 1))
                for a, b, cc, d1, d2, d3 in zip(p_rep, t_rep, s_rep, pq, tq, sq):
                    lev.append(("P%06d" % pid, a, b, cc, d1, d2, d3))
                dlv.append(dict(profile_id="P%06d" % pid, wmo=f["wmo"], cycle=c["cycle"], direction="A",
                                file_version=2 if resent else 1,
                                delivered=stamp(complete_at), n_levels=int(n)))
                c["delivered"] = complete_at
                c["resent"] = resent
                # the descending profile: recorded on the way down to the parking depth at the cycle's start
                if f["descent"]:
                    pid += 1
                    t_down = surface - dt.timedelta(days=9, hours=float(rng.uniform(3, 6)))
                    pd_ = sim.float_levels(rng, 1000.0)
                    th, s = sim.column(pd_, c["heave"], c["lon"], t_down.timetuple().tm_yday)
                    # no fix under water: the position is the last surface fix, the previous cycle's
                    plat, plon = prev if prev is not None else (c["lat"], c["lon"])
                    prof.append(dict(profile_id="P%06d" % pid, wmo=f["wmo"], cycle=c["cycle"], direction="D",
                                     juld=round(juld(t_down), 6), latitude=round(plat, 3),
                                     longitude=round(plon, 3), position_qc=8, file_version=1))
                    for a, b, cc in zip(pd_, sim.in_situ(th, s, pd_), s + c["delta"]):
                        lev.append(("P%06d" % pid, round(float(a + rng.normal(0, 0.4)), 1),
                                    round(float(b + rng.normal(0, 0.0012)), 3), round(float(cc + rng.normal(0, 0.0015)), 4),
                                    1, 1, 1))
                    dlv.append(dict(profile_id="P%06d" % pid, wmo=f["wmo"], cycle=c["cycle"], direction="D", file_version=1,
                                    delivered=stamp(complete_at + dt.timedelta(minutes=1)), n_levels=int(pd_.size)))
                # the cycle's timeline as the float's technical messages report it
                tx = dt.timedelta(hours=float(rng.uniform(5, 9))) if f["telecom"] == "Argos" else \
                    dt.timedelta(minutes=float(rng.uniform(12, 35)))
                if restart is None:
                    tx0 = dt.timedelta(hours=float(rng.uniform(5, 9))) if f["telecom"] == "Argos" else \
                        dt.timedelta(minutes=float(rng.uniform(12, 35)))
                    restart = surface - dt.timedelta(days=10, minutes=float(rng.normal(0, 25))) + tx0
                park_start = restart + dt.timedelta(hours=float(rng.uniform(4.0, 5.5)))
                park_end = start - dt.timedelta(hours=float(rng.uniform(2.6, 3.4)))
                tech.append(dict(wmo=f["wmo"], cycle=c["cycle"], descent_start=stamp(restart), park_start=stamp(park_start),
                                 park_end=stamp(park_end), ascent_start=stamp(start), ascent_end=stamp(surface),
                                 battery_v=round(float(15.32 - 0.0016 * c["cycle"] - (0.05 if f["model"] == "K" else 0.0)
                                                       + rng.normal(0, 0.012)), 2),
                                 vacuum_mbar=int(round(711 + 0.05 * c["cycle"] + float(rng.normal(0, 1.2)))),
                                 pump_s=int(round(float(rng.normal(96 + 0.08 * c["cycle"], 6))))))
                restart = surface + tx
                prev = (c["lat"], c["lon"])
        # the pack was drawn on the morning of the as-of date: files not yet received are not in it
        dlv = pd.DataFrame(dlv)
        dlv = dlv[dlv["delivered"] <= CUTOFF]
        got = set(dlv["profile_id"])
        self.late = sorted(set(p["profile_id"] for p in prof) - got)
        self.prof = pd.DataFrame([p for p in prof if p["profile_id"] in got])
        lev = pd.DataFrame(lev, columns=["profile_id", "pres", "temp", "psal", "pres_qc", "temp_qc", "psal_qc"])
        self.lev = lev[lev["profile_id"].isin(got)].reset_index(drop=True)
        self.tech = pd.DataFrame(tech)
        self.dlv = dlv.drop(columns="profile_id").sort_values(["delivered", "wmo", "cycle"], kind="stable").reset_index(drop=True)

    def profiles(self):
        return self.prof.copy()

    def levels(self):
        return self.lev.copy()

    def technical(self):
        return self.tech.copy()

    def deliveries(self):
        d = self.dlv.copy()
        d.insert(3, "file_name", ["%s%s_%03d%s.nc" % ("R", w, c, "D" if dr == "D" else "") for w, c, dr in
                                  zip(d["wmo"], d["cycle"], d["direction"])])
        return d

    # ---------------------------------------------------------------- the reference data: the institute's archive and
    # an international extract (other institutes' casts, and many of the institute's own under that database's ids)
    def _reference(self):
        W = self.W
        # a station worked twice: the cast repeated a few hours later at the same position (a sensor check, or the
        # bottles re-fired), kept in the archive as the next station
        rng = self.rng(7)
        casts = []
        for c in W.casts:
            casts.append(c)
            if rng.random() < 0.18:
                when = c["when"] + dt.timedelta(minutes=int(rng.integers(180, 361)))
                h = c["heave"] + float(rng.normal(0, 3.0))
                th, s = sim.column(c["p"], h, c["lon"], when.timetuple().tm_yday)
                casts.append(dict(year=c["year"], date=when.date(), when=when, lon=c["lon"] + float(rng.normal(0, 0.001)),
                                  lat=c["lat"] + float(rng.normal(0, 0.001)), p=c["p"].copy(),
                                  theta=th + rng.normal(0, 0.0015, c["p"].size),
                                  s=s + rng.normal(0, 0.0010, c["p"].size), heave=h, repeat=True))
        self.casts = casts
        rng = self.rng(4)
        arch_c, arch_l, intl_c, intl_l = [], [], [], []
        cruise = {}
        for c in casts:
            cr = cruise.setdefault(c["year"], "IOA%02d%02d" % (c["year"] % 100, int(rng.integers(1, 4))))
            stn = sum(1 for x in arch_c if x["cruise"] == cr) + 1
            # most casts went to 2,200 dbar; some stations were planned to 2,100, and slope and seamount stations
            # stopped where the bottom did
            u = rng.random()
            if c.get("repeat") or u < 0.82:
                lim = 2200.0
            elif u < 0.88:
                lim = 2100.0
            else:
                lim = float(10 * int(rng.integers(115, 195)) + 9)
            m = c["p"] <= lim
            c["id"], c["pmax"], c["owner"] = "%s-%03d" % (cr, stn), float(c["p"][m].max()), "IOA"
            scale = "IPTS-68" if c["year"] <= 2016 else "ITS-90"
            t = sim.in_situ(c["theta"], c["s"], c["p"])
            if scale == "IPTS-68":
                t = t * 1.00024
            arch_c.append(dict(cast_id=c["id"], cruise=cr, station=stn, time_utc=c["when"].strftime("%Y-%m-%d %H:%M"),
                               latitude=round(c["lat"], 4), longitude=round(c["lon"], 4), temp_scale=scale,
                               max_pres=c["pmax"]))
            for x, y, z in zip(c["p"][m], t[m], c["s"][m]):
                arch_l.append((c["id"], float(x), round(float(y), 4), round(float(z), 4)))
        # the international extract: about two thirds of the institute's casts, as the institute submitted them, and the
        # casts other institutes submitted
        nid = 81000
        for c in casts:
            if rng.random() < 0.67:
                nid += int(rng.integers(1, 40))
                m = c["p"] <= c["pmax"]
                d = SW.depth_from_pres(c["p"][m], c["lat"])
                t = sim.in_situ(c["theta"], c["s"], c["p"])[m]
                when = c["when"] + dt.timedelta(minutes=int(rng.integers(-3, 4)))
                c["dup"] = "RHD%07d" % nid
                intl_c.append(dict(station_id=c["dup"], platform="RV Mar Atlântico", country="PT",
                                   date=when.strftime("%Y-%m-%d"), time=round(when.hour + when.minute / 60.0, 2),
                                   lat=round(c["lat"], 2), lon=round(c["lon"], 2), max_depth_m=round(float(d.max()), 0)))
                for x, y, z in zip(d, t, c["s"][m]):
                    intl_l.append((c["dup"], round(float(x), 0), round(float(y), 3), round(float(z), 3)))
        others = []
        ships = [("RV Aldegar", "ES", "p5"), ("RV Penmorvan", "FR", "z10"), ("RV Glenbrae", "GB", "p2")]
        for yr in range(2015, 2026):
            for j in range(int(rng.integers(5, 10))):
                lon, lat = float(rng.uniform(-22.0, -9.8)), float(rng.uniform(36.4, 43.6))
                when = dt.datetime(yr, int(rng.integers(1, 13)), int(rng.integers(1, 28))) + \
                    dt.timedelta(minutes=int(rng.integers(0, 1440)))
                ship, country, grid = ships[int(rng.integers(0, 3))]
                band = rng.random()
                if band < 0.35:
                    deepest = float(rng.uniform(1987.0, 1999.0))        # just short of 2,000 m
                elif band < 0.70:
                    deepest = float(rng.uniform(2040.0, 2190.0))
                else:
                    deepest = float(rng.uniform(1450.0, 1960.0))
                if grid == "z10":
                    d = np.arange(5.0, deepest + 0.01, 10.0)
                    p = SW.pres_from_depth(d, lat)
                else:
                    step = 5.0 if grid == "p5" else 2.0
                    p = np.arange(step / 2, 2300.0, step)
                    d = SW.depth_from_pres(p, lat)
                    p, d = p[d <= deepest], d[d <= deepest]
                h = float(rng.normal(0, 10)) + float(rng.normal(0, P.EDDY_SD))
                th, s = sim.column(p, h, lon, when.timetuple().tm_yday)
                th = th + rng.normal(0, 0.0015, p.size)
                s = s + rng.normal(0, 0.0010, p.size)
                nid += int(rng.integers(1, 40))
                sid = "RHD%07d" % nid
                intl_c.append(dict(station_id=sid, platform=ship, country=country, date=when.strftime("%Y-%m-%d"),
                                   time=round(when.hour + when.minute / 60.0, 2), lat=round(lat, 2), lon=round(lon, 2),
                                   max_depth_m=round(float(d.max()), 0)))
                t = sim.in_situ(th, s, p)
                for x, y, z in zip(d, t, s):
                    intl_l.append((sid, round(float(x), 0), round(float(y), 3), round(float(z), 3)))
                others.append(dict(id=sid, year=yr, when=when, lon=lon, lat=lat, theta=th, s=s, p=p, pmax=float(p.max()),
                                   deepest_m=float(d.max())))
        self.others = others
        self.arch_c = pd.DataFrame(arch_c)
        self.arch_l = pd.DataFrame(arch_l, columns=["cast_id", "pres", "temp", "psal"])
        self.intl_c = pd.DataFrame(intl_c).sort_values(["date", "time", "station_id"]).reset_index(drop=True)
        self.intl_l = pd.DataFrame(intl_l, columns=["station_id", "depth_m", "temperature", "salinity"])

    def archive_casts(self):
        return self.arch_c.copy()

    def archive_levels(self):
        return self.arch_l.copy()

    def intl_casts(self):
        return self.intl_c.copy()

    def intl_levels(self):
        return self.intl_l.copy()

    # ---------------------------------------------------------------- distractors
    def recoveries(self):
        """past floats the programme recovered, and what the lab found on their sensors (not this array's floats)"""
        rng = self.rng(5)
        rows = []
        for j in range(9):
            dep = dt.date(2014, 1, 1) + dt.timedelta(days=int(rng.integers(0, 3000)))
            rec = dep + dt.timedelta(days=int(rng.integers(300, 1500)))
            rows.append(dict(wmo="19885%02d" % (j + 3), deployed=dep.isoformat(), recovered=rec.isoformat(),
                             reason=str(rng.choice(["grounded near the coast", "recovered for the sensor study",
                                                    "picked up by a fishing vessel"])),
                             lab_salinity_error=round(float(rng.normal(-0.006, 0.006)), 4),
                             lab_temperature_error=round(float(rng.normal(0, 0.0012)), 4)))
        return pd.DataFrame(rows)

    def oxygen(self):
        rng = self.rng(6)
        rows = []
        withopt = [f for f in self.array if f["model"] == "A"][:6]
        pids = self.prof[(self.prof["direction"] == "A")].drop_duplicates(["wmo", "cycle"], keep="last")
        pid = dict(zip(zip(pids["wmo"], pids["cycle"]), pids["profile_id"]))
        for f in withopt:
            for c in f["cycles"]:
                key = (f["wmo"], c["cycle"])
                for p in c["p"][::2]:
                    o2 = 235 - 70 * np.exp(-((p - 800) / 350.0) ** 2) - 25 * min(p, 1500) / 1500 + rng.normal(0, 1.5)
                    rows.append((pid[key], round(float(p), 1), round(float(o2), 1), 1))
        return pd.DataFrame(rows, columns=["profile_id", "pres", "doxy", "doxy_qc"])
