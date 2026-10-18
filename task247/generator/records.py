"""task247 records: every data file of the pack, built from the simulator's sea, cloud and analyses, the loggers and
the 2023 survey.

Layer 1, as the station's systems produce it: the near-real-time extract keeps every issue of a day (a day re-issued
when a late pass arrives appears twice), its observation flag changed coding with version 3.2 on 15 July 2027, the
provider issued no analysis for 17 June 2027, the reprocessed record is in kelvin, both satellite files are keyed by
pixel, and the bulletins are dated by the station's local Tuesday while they report the UTC day before."""
import datetime as dt

import numpy as np
import pandas as pd

import estim as E
import insitu
import params as P
import sim
import survey

MISSING_DAY = dt.date(2027, 6, 17)
V31 = dt.date(2021, 4, 1)               # version 3.1 from this issue date
V32 = dt.date(2027, 7, 15)              # version 3.2 from this issue date (flag recoded)
BULLETIN_FIRST = dt.date(2027, 5, 4)    # Tuesdays to the as-of
LOCAL = dt.timedelta(hours=-5)


def version(issued):
    d = issued.date()
    return "3.2" if d >= V32 else ("3.1" if d >= V31 else "3.0")


def flag(observed, ver):
    if ver == "3.2":
        return 2 if observed else 1
    return 1 if observed else 0


def level(x):
    return "Alert Level 2" if x >= P.AL2 else ("Alert Level 1" if x >= P.AL1 else "No alert")


class Records:
    def __init__(self, W=None):
        self.W = W if W is not None else sim.make(P.SIM_SEED)
        W = self.W
        self.rng = np.random.default_rng(P.SEED + 101)
        self.D = W["D"]
        self.mmm = np.round(W["mmm"], 2)
        self.X = insitu.make(W)
        self.S = survey.make(W)
        self._issues()

    # ------------------------------------------------------------ the near-real-time issues
    def _issues(self):
        """every issue of every day: (site, day index, value, observed, issued UTC)"""
        W, rng = self.W, self.rng
        out = []
        for i, day in enumerate(self.D):
            if day == MISSING_DAY:
                continue
            for s in range(P.NSITE):
                first = dt.datetime.combine(day + dt.timedelta(days=1), dt.time(8, 30)) + \
                    dt.timedelta(minutes=int(rng.integers(0, 55)), seconds=int(rng.integers(0, 60)))
                out.append((s, i, float(W["nrt"][s, i]), not bool(W["cloud"][s, i]), first))
                if W["late"][s, i]:
                    again = dt.datetime.combine(day + dt.timedelta(days=int(rng.integers(2, 4))), dt.time(8, 30)) + \
                        dt.timedelta(minutes=int(rng.integers(0, 55)), seconds=int(rng.integers(0, 60)))
                    out.append((s, i, float(W["obsv"][s, i]), True, again))
        self.issues = out

    def nrt(self):
        rows = []
        for s, i, v, obs, issued in self.issues:
            ver = version(issued)
            rows.append((P.SITES[s][3], self.D[i].isoformat(), "%.2f" % v, flag(obs, ver), ver,
                         issued.strftime("%Y-%m-%dT%H:%M:%SZ"), i, s, issued))
        rows.sort(key=lambda r: (r[6], r[7], r[8]))
        return pd.DataFrame([r[:6] for r in rows], columns=["pixel_id", "date", "sst_c", "obs_flag",
                                                             "product_version", "issued_utc"])

    def final_series(self):
        """the latest issue of each day as a site by day array (NaN for the day never issued), and its observed mask"""
        T = len(self.D)
        val = np.full((P.NSITE, T), np.nan)
        obs = np.zeros((P.NSITE, T), bool)
        when = np.full((P.NSITE, T), None, dtype=object)
        for s, i, v, o, issued in self.issues:
            if when[s, i] is None or issued > when[s, i]:
                val[s, i] = round(v, 2)
                obs[s, i] = o
                when[s, i] = issued
        return val, obs

    # ------------------------------------------------------------ the reprocessed record
    def reprocessed(self):
        W = self.W
        rows = []
        for i, day in enumerate(self.D):
            if day > P.LAST_REP_DAY:
                break
            for s in range(P.NSITE):
                rows.append((P.SITES[s][3], day.isoformat(), "%.2f" % (W["rep"][s, i] + 273.15)))
        return pd.DataFrame(rows, columns=["pixel_id", "time", "analysed_sst_k"])

    # ------------------------------------------------------------ the register and the climatology
    def sites(self):
        rng = np.random.default_rng(P.SEED + 11)
        rows = []
        lat, lon = 19.93, -87.418
        for s, (code, name, region, pixel) in enumerate(P.SITES):
            rows.append((code, name, region, pixel, "%.4f" % lat, "%.4f" % lon, P.SITE_DEPTH[s], "%.2f" % self.mmm[s]))
            lat -= rng.uniform(0.035, 0.065)
            lon -= rng.uniform(0.004, 0.018)
        return pd.DataFrame(rows, columns=["site_code", "site_name", "region", "pixel_id", "latitude", "longitude",
                                           "survey_depth_m", "mmm_c"])

    def climatology(self):
        W = self.W
        rows = []
        y19 = {d: i for i, d in enumerate(self.D) if d.year == 2019}
        y20 = {d: i for i, d in enumerate(self.D) if d.year == 2020}
        for s in range(P.NSITE):
            for m in range(1, 13):
                for d in range(1, 32):
                    try:
                        day = dt.date(2020, m, d)
                    except ValueError:
                        continue
                    i = y20[day]
                    rows.append((P.SITES[s][3], m, d, "%.2f" % W["clim"][s, i]))
        return pd.DataFrame(rows, columns=["pixel_id", "month", "day", "clim_sst_c"])

    # ------------------------------------------------------------ the bulletins
    def bulletins(self):
        """each Tuesday's bulletin, from the issues available at 09:00 local (14:00 UTC): each site's SST, HotSpot and
        degree heating weeks for the Monday (UTC day) before, and the alert level"""
        rows = []
        idx = {d: i for i, d in enumerate(self.D)}
        by_site = [[] for _ in range(P.NSITE)]
        for s, i, v, o, issued in self.issues:
            by_site[s].append((issued, i, v))
        for s in range(P.NSITE):
            by_site[s].sort()
        tue = BULLETIN_FIRST
        no = 1
        while tue <= P.ASOF:
            cut = dt.datetime.combine(tue, dt.time(14, 0))
            mon = tue - dt.timedelta(days=1)
            j = idx[mon]
            for s in range(P.NSITE):
                cur = {}
                for issued, i, v in by_site[s]:
                    if issued > cut:
                        break
                    cur[i] = v
                hs = 0.0
                for i in range(j - P.WINDOW + 1, j + 1):
                    if i in cur:
                        h = round(cur[i], 2) - self.mmm[s]
                        hs += h if h >= P.HS_MIN else 0.0
                dhw = hs / 7.0
                hot = round(cur[j], 2) - self.mmm[s]
                rows.append(dict(bulletin=no, issued=tue.isoformat(), analysis_day=mon.isoformat(),
                                 site_code=P.SITES[s][0], site_name=P.SITES[s][1], sst_c=round(cur[j], 2),
                                 hotspot_c=round(max(hot, 0.0), 2), dhw=round(dhw, 1), alert_level=level(dhw),
                                 _dhw=dhw))
            tue += dt.timedelta(days=7)
            no += 1
        return pd.DataFrame(rows)

    # ------------------------------------------------------------ the 2023 survey
    def survey_colonies(self):
        rows = []
        for r in self.S["rows"]:
            rows.append((P.SITES[r["site"]][0], r["date"].isoformat(), r["transect"], r["sheet"], r["observer"],
                         "%.1f" % r["depth"], r["segment"], r["line"], r["genus"], r["dia"], r["cond"]))
        rows.sort(key=lambda x: (x[1], x[0], x[3] != "S", x[2], x[7]))
        return pd.DataFrame(rows, columns=["site_code", "date", "transect", "sheet", "observer", "depth_m", "metre",
                                           "line", "genus", "max_diameter_cm", "condition"])

    # ------------------------------------------------------------ the loggers
    def logger_deployments(self):
        rows = []
        for d in sorted(self.X["deps"], key=lambda d: (d["deployed"], d["site"])):
            dep = insitu.logged(d["deployed"], d["deployed_utc"])
            ret = insitu.logged(d["retrieved"], d["retrieved_utc"]) if d["retrieved"] else None
            notes = ""
            if d["retrieved"] is None:
                notes = "in the water"
            elif d["retrieved_boat"] == "Cozumel II" and d["retrieved"].month == 8 and d["retrieved"].year == 2025:
                notes = "retrieved only; new loggers went in from the Ixchel on 18 to 21 August"
            if d["model"] == "MX2203" and d["deployed"].date() < dt.date(2025, 9, 1):
                notes = notes or "first MX2203 at the site"
            rows.append((P.SITES[d["site"]][0], d["serial"], d["model"], P.SITE_DEPTH[d["site"]],
                         dep.strftime("%Y-%m-%d %H:%M"), d["deployed_boat"],
                         ret.strftime("%Y-%m-%d %H:%M") if ret else "", d["retrieved_boat"], notes))
        return pd.DataFrame(rows, columns=["site_code", "serial", "model", "depth_m", "deployed", "deployed_from",
                                           "retrieved", "retrieved_from", "notes"])

    def logger_readings(self):
        rows = [(serial, t.strftime("%Y-%m-%d %H:%M"), "%.2f" % v) for serial, t, v in self.X["readings"]
                if t >= insitu.FIRST_EXPORT]
        rows.sort(key=lambda r: (r[0], r[1]))
        return pd.DataFrame(rows, columns=["serial", "datetime_local", "temperature_c"])

    # ------------------------------------------------------------ distractors
    def kd490(self):
        rng = np.random.default_rng(P.SEED + 31)
        rows = []
        base = rng.uniform(0.045, 0.075, P.NSITE)
        for y in (2024, 2025, 2026, 2027):
            for m in range(1, 13):
                if dt.date(y, m, 1) > dt.date(2027, 10, 1):
                    break
                for s in range(P.NSITE):
                    v = base[s] * (1 + 0.18 * np.cos(2 * np.pi * (m - 1) / 12)) * np.exp(rng.normal(0, 0.08))
                    rows.append((P.SITES[s][3], "%d-%02d" % (y, m), "%.3f" % v))
        return pd.DataFrame(rows, columns=["pixel_id", "month", "kd490_per_m"])

    def tide(self):
        rng = np.random.default_rng(P.SEED + 37)
        rows = []
        t = dt.datetime(2027, 1, 1, 0, 0)
        k = 0
        while t <= dt.datetime(2027, 10, 31, 23, 0):
            h = k
            v = (0.11 * np.cos(2 * np.pi * h / 12.42 + 0.7) + 0.06 * np.cos(2 * np.pi * h / 23.93 + 1.9)
                 + 0.04 * np.cos(2 * np.pi * h / 12.0) + 0.05 * np.sin(2 * np.pi * h / (24 * 182.6)) + rng.normal(0, 0.01))
            rows.append((t.strftime("%Y-%m-%d %H:%M"), "%.3f" % v))
            t += dt.timedelta(hours=1)
            k += 1
        return pd.DataFrame(rows, columns=["datetime_local", "sea_level_m"])
