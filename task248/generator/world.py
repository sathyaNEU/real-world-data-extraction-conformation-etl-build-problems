"""Simulate Highbank Marinas' 2026: the true tanks, dock sales, deliveries, temperatures, gauge readings,
leak tests and the systems' own events. Returns a dict of plain lists; pack.py writes the files."""
import datetime as dt
import math
import numpy as np
from zoneinfo import ZoneInfo
import params as P

CHI = ZoneInfo(P.TZ)
UTC = dt.timezone.utc


def vol(h, D, L):
    R = D / 2.0
    h = np.clip(np.asarray(h, dtype=float), 0.0, D)
    a = R * R * np.arccos((R - h) / R) - (R - h) * np.sqrt(np.maximum(2 * R * h - h * h, 0.0))
    return a * L / P.GAL_IN3


class Tank:
    def __init__(self, tid, rng):
        m, prod, cap, delta, eps, meter, nh = P.TANKS[tid]
        self.id, self.marina, self.product, self.cap = tid, m, prod, cap
        self.D, self.L0 = P.GEOM[cap]
        self.Lt = self.L0 * (1.0 - eps)          # chart overstates every gallon by about eps
        self.delta, self.eps, self.meter = delta, eps, meter
        self.beta = P.BETA[prod]
        self.chart_no = "HC%d-%02dK" % (int(self.D), cap // 1000)
        # hose meters: tank-level bias plus small spread
        self.hose_err = [meter + rng.normal(0, 0.0003) for _ in range(nh)]
        self.reorder_h = float(round(P.REORDER_FRAC * self.D))
        self.half_h = float(round(self.D / 2.0))
        self.fill_h = float(round(P.FILL_FRAC * self.D))
        grid = np.linspace(0, self.D, 20001)
        self._gv = vol(grid, self.D, self.Lt)
        self._gh = grid

    def h_of_gross(self, g):
        return float(np.interp(g, self._gv, self._gh))

    def chart_gal(self, h):
        """the console's chart: the nominal-dimension table at quarter-inch steps, linearly interpolated"""
        q = np.arange(0, self.D + 1e-9, 0.25)
        tab = np.round(vol(q, self.D, self.L0), 1)
        return float(np.interp(h, q, tab))

    def chart_table(self):
        q = np.arange(0, self.D + 1e-9, 0.25)
        return q, np.round(vol(q, self.D, self.L0), 1)


def local(d, hour=0.0):
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=hour)


def to_utc(naive_local):
    return naive_local.replace(tzinfo=CHI).astimezone(UTC).replace(tzinfo=None)


def season_factor(d):
    doy = d.timetuple().tm_yday
    if d < dt.date(2026, 3, 14) or d > dt.date(2026, 11, 22):
        return 0.0
    # shoulder ramps, July peak
    peak = math.exp(-((doy - 196) / 62.0) ** 2)
    return 0.12 + 0.95 * peak


def ground_temp(t_local):
    doy = t_local.timetuple().tm_yday + t_local.hour / 24.0
    return 59.6 + 1.3 * math.sin(2 * math.pi * (doy - 120) / 365.0)


def simulate(seed=P.SEED):
    rng = np.random.default_rng(seed)
    tanks = {tid: Tank(tid, rng) for tid in P.TANKS}
    days = [dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range(365)]
    out = {"tanks": tanks, "sales": [], "readings": [], "deliveries": [], "bols": [], "tests": [],
           "outages": {}, "probe_faults": [], "resets": {}, "true_closing": {}}

    # ---- dock sales, per marina, per day ----
    hose_ids = {}
    for tid, t in tanks.items():
        disp = {"AH": 2, "BP": 3, "CF": 2, "DH": 2, "EB": 3, "FL": 3, "GC": 3, "HS": 2}[t.marina]
        hose_ids[tid] = []
        for k in range(len(t.hose_err)):
            hose_ids[tid].append("%d%s" % (1 + (k % disp), "ABCD"[k // disp + (1 if t.product == "DSL" else 0)]))
    by_marina = {}
    for tid, t in tanks.items():
        by_marina.setdefault(t.marina, []).append(tid)
    txn = 0
    sales_by_tank = {tid: [] for tid in tanks}
    for d in days:
        sf = season_factor(d)
        wk = 1.45 if d.weekday() >= 5 else 0.85
        hol = 1.5 if d in (dt.date(2026, 5, 25), dt.date(2026, 7, 4), dt.date(2026, 9, 7)) else 1.0
        for m, tids in by_marina.items():
            open_winter = P.MARINAS[m][2]
            lev = P.MARINA_LEVEL[m]
            if sf == 0.0:
                if not open_winter:
                    continue
                base = 0.05
            else:
                base = sf
            for tid in tids:
                t = tanks[tid]
                share = P.PRODUCT_SHARE[t.product]
                if m == "DH" and t.product == "REC90":
                    share = 0.62 if tid == "DH-1" else 0.48
                mean_gal_day = 520.0 * base * wk * hol * lev * share * rng.uniform(0.85, 1.15)
                avg = 85.0 if t.product == "DSL" else 33.0
                n = rng.poisson(max(mean_gal_day / avg, 0.0))
                for _ in range(n):
                    if sf == 0.0:
                        hr = rng.uniform(9.0, 16.5)
                    elif rng.random() < 0.035 and m in ("BP", "DH", "FL"):
                        hr = rng.uniform(20.5, 30.0)     # 24-hour card pumps
                    else:
                        hr = float(np.clip(rng.normal(13.0, 3.0), 7.03, 19.96))
                    g = float(np.clip(rng.lognormal(math.log(avg) - 0.18, 0.6), 3.0, 260.0))
                    k = int(rng.integers(len(t.hose_err)))
                    when = local(d, hr).replace(microsecond=0)
                    if when.minute == 0 and when.second < 20:
                        when = when + dt.timedelta(seconds=int(rng.integers(25, 300)))
                    sales_by_tank[tid].append((when, g, k))
    for tid in tanks:
        sales_by_tank[tid].sort()

    # ---- modem outages per marina (lost beyond the 48 h buffer) ----
    for m in P.MARINAS:
        outs = []
        for _ in range(int(rng.integers(3, 7))):
            start = local(dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(5, 355))), float(rng.uniform(0, 24)))
            dur_h = float(rng.choice([6, 14, 30, 60, 90, 120, 150])) + float(rng.uniform(0, 10))
            outs.append((start, start + dt.timedelta(hours=dur_h)))
        out["outages"][m] = sorted(outs)

    # probe faults (tank-specific: no readings from the probe)
    faults = [("DH-2", local(dt.date(2026, 1, 9), 3.5), local(dt.date(2026, 1, 14), 15.0)),
              ("EB-3", local(dt.date(2026, 8, 18), 11.0), local(dt.date(2026, 8, 19), 19.0)),
              ("GC-2", local(dt.date(2026, 3, 2), 8.0), local(dt.date(2026, 3, 5), 10.5))]
    out["probe_faults"] = faults

    # ---- per tank time loop (one time-ordered event queue) ----
    import heapq
    for tid, t in tanks.items():
        m = t.marina
        net = float(vol(0.62 * t.D, t.D, t.Lt))
        T = ground_temp(local(days[0]))
        seq = int(rng.integers(40000, 90000))
        t_cur = local(days[0], 0.0)
        tau_h = 70.0
        q = []
        for i in range(365 * 12):
            heapq.heappush(q, (local(days[0], 0.0) + dt.timedelta(hours=2 * i), 2, "R", None))
        for (when, g, k) in sales_by_tank[tid]:
            heapq.heappush(q, (when, 1, "S", (g, k)))
        pending = False
        dstate = None
        while q:
            when, _, kind, payload = heapq.heappop(q)
            dt_h = max((when - t_cur).total_seconds() / 3600.0, 0.0)
            Tg = ground_temp(when)
            T = Tg + (T - Tg) * math.exp(-dt_h / tau_h)
            t_cur = when
            if kind == "S":
                g_true, k = payload
                min_net = float(vol(0.06 * t.D, t.D, t.Lt))
                g_true = min(g_true, max((net - min_net) / (1 - t.beta * (T - 60.0)), 0.0))
                if g_true <= 0.5:
                    continue
                net -= g_true * (1 - t.beta * (T - 60.0))
                reg = round(g_true * (1 + t.hose_err[k]), 3)
                out["sales"].append({"tank": tid, "marina": m, "local": when, "hose": hose_ids[tid][k],
                                     "product": t.product, "gal_true": g_true, "gal_reg": reg})
            elif kind == "DS":
                gross_now = net * (1 + t.beta * (T - 60.0))
                h0 = t.h_of_gross(gross_now)
                h_to = float(rng.uniform(*P.DELIVER_TO)) * t.D
                target_net = float(vol(h_to, t.D, t.Lt)) * (1 - t.beta * (T - 60.0))
                del_net = max(round((target_net - net) / 50.0) * 50.0, 1500.0)
                Tdel = float(ground_temp(when) + rng.normal(0.8, 1.2))
                true_net = del_net * (1 + rng.normal(0, 0.0007))
                dur = float(rng.uniform(0.40, 0.85))
                T_meas0 = T + rng.normal(0, 0.06)
                hread0 = h0 + t.delta + rng.normal(0, 0.004)
                gr0 = t.chart_gal(hread0)
                V_old = net
                net += true_net
                T = (V_old * T + true_net * Tdel) / (V_old + true_net)
                dstate = {"tank": tid, "marina": m, "start": when, "h0": round(hread0, 3), "g0": round(gr0, 1),
                          "n0": round(gr0 * (1 - t.beta * (T_meas0 - 60.0)), 1), "T0": round(T_meas0, 1)}
                out["bols"].append({"tank": tid, "marina": m, "local": when - dt.timedelta(minutes=int(rng.integers(8, 25))),
                                    "product": t.product, "net": int(round(del_net)),
                                    "gross": int(round(del_net * (1 + t.beta * (Tdel - 60.0)))),
                                    "temp": round(Tdel, 1), "true_net": true_net})
                heapq.heappush(q, (when + dt.timedelta(hours=dur), 0, "DE", None))
            elif kind == "DE":
                gross_end = net * (1 + t.beta * (T - 60.0))
                h1 = t.h_of_gross(gross_end)
                T_meas1 = T + rng.normal(0, 0.06)
                hread1 = h1 + t.delta + rng.normal(0, 0.004)
                gr1 = t.chart_gal(hread1)
                dstate.update({"end": when, "h1": round(hread1, 3), "g1": round(gr1, 1),
                               "n1": round(gr1 * (1 - t.beta * (T_meas1 - 60.0)), 1), "T1": round(T_meas1, 1)})
                out["deliveries"].append(dstate)
                dstate = None
                pending = False
            else:   # reading
                gross_true = net * (1 + t.beta * (T - 60.0))
                h_true = t.h_of_gross(gross_true)
                T_meas = T + rng.normal(0, 0.05)
                hread = h_true + t.delta + rng.normal(0, 0.004)
                gr = t.chart_gal(hread)
                netc = gr * (1 - t.beta * (T_meas - 60.0))
                seq += 1
                wmean = 0.55 if tid in ("CF-1", "GC-3") else 0.18
                out["readings"].append({"tank": tid, "marina": m, "local": when, "seq": seq, "h": round(hread, 3),
                                        "T": round(T_meas, 1), "gross": round(gr, 1), "tc": round(netc, 1),
                                        "water": round(max(0.0, rng.normal(wmean, 0.05)), 2),
                                        "net_true": net, "h_true": h_true, "T_true": T})
                if when.hour == 6 and not pending and when < local(dt.date(2026, 12, 29), 0):
                    reorder_net = t.chart_gal(t.reorder_h)
                    if netc < reorder_net + float(rng.uniform(-60, 160)):
                        lag = 1 if when.weekday() < 4 else (7 - when.weekday())
                        dd = when.date() + dt.timedelta(days=lag)
                        heapq.heappush(q, (local(dd, float(rng.uniform(8.3, 13.2))), 0, "DS", None))
                        pending = True
        out["true_closing"][tid] = net
    out["hose_ids"] = hose_ids
    return out
