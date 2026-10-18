"""task247 golden pipeline, run on the shipped files: each site's 2027 season maximum degree heating weeks as the
reprocessed record will give it, the level and the verdict against the bulletins; the default path's and the other
rungs' figures; the 2023 survey's prevalence and colonies; the loggers' hours at or above the MMM."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import estim as E
import params as P

SEASON = (dt.date(2027, 6, 1), dt.date(2027, 10, 31))
LEVELS = ["No alert", "Alert Level 1", "Alert Level 2"]
STONY = ["OFAV", "OANN", "OFRA", "MCAV", "CNAT", "DLAB", "PSTR", "SSID", "SINT", "AAGA", "PAST", "PPOR", "MMEA",
         "DSTO", "EFAS", "APAL"]
GPS_UTC = ("Cozumel II", dt.date(2026, 6, 1))     # that boat's GPS showed UTC on its trips before this date


def level(x):
    return LEVELS[2] if x >= P.AL2 else (LEVELS[1] if x >= P.AL1 else LEVELS[0])


def verdict(new, old):
    a, b = LEVELS.index(new), LEVELS.index(old)
    return "confirms" if a == b else ("raises" if a > b else "lowers")


class Pack:
    def __init__(self, target, F):
        self.t, self.F = target, F
        rd = lambda k, **kw: pd.read_csv(os.path.join(target, F[k]), **kw)
        self.sites = rd("sites")
        self.clim = rd("clim")
        self.nrt_raw = rd("nrt", dtype={"product_version": str})
        self.rep_raw = rd("rep")
        self.codes = list(self.sites.site_code)
        self.pix = dict(zip(self.sites.pixel_id, self.sites.site_code))
        self.mmm = dict(zip(self.sites.site_code, self.sites.mmm_c))
        self.days = [dt.date(2018, 1, 1) + dt.timedelta(i) for i in range((dt.date(2027, 11, 2) - dt.date(2018, 1, 1)).days + 1)]
        self.di = {d.isoformat(): i for i, d in enumerate(self.days)}
        self._series()

    def _series(self):
        n = self.nrt_raw.sort_values("issued_utc").drop_duplicates(["pixel_id", "date"], keep="last")
        obs_code = np.where(n.product_version == "3.2", 2, 1)
        n = n.assign(observed=(n.obs_flag.values == obs_code))
        S, T = len(self.codes), len(self.days)
        self.nrt = np.full((S, T), np.nan)
        self.obs = np.zeros((S, T), bool)
        si = {c: k for k, c in enumerate(self.codes)}
        for pix, d, v, o in zip(n.pixel_id, n.date, n.sst_c, n.observed):
            k, i = si[self.pix[pix]], self.di[d]
            self.nrt[k, i] = v
            self.obs[k, i] = o
        self.rep = np.full((S, T), np.nan)
        for pix, d, v in zip(self.rep_raw.pixel_id, self.rep_raw.time, self.rep_raw.analysed_sst_k):
            self.rep[si[self.pix[pix]], self.di[d]] = v - 273.15
        cl = {(p, m, d): v for p, m, d, v in zip(self.clim.pixel_id, self.clim.month, self.clim.day, self.clim.clim_sst_c)}
        inv = {c: p for p, c in self.pix.items()}
        self.climd = np.array([[cl[(inv[c], d.month, d.day)] for d in self.days] for c in self.codes])
        self.season = np.array([SEASON[0] <= d <= SEASON[1] for d in self.days])
        self.past = np.array([d.year <= 2026 for d in self.days])
        self.mon = np.array([d.month for d in self.days])

    # ------------------------------------------------------------ the bias and the routes
    def bias(self, mask=None):
        both = self.past & ~np.isnan(self.rep) & ~np.isnan(self.nrt)
        m = both & self.obs if mask is None else both & mask
        return float(np.mean((self.nrt - self.rep)[m]))

    def refilled(self, k, b, mode="anomaly", nrt=None, obs=None):
        nrt = self.nrt[k] if nrt is None else nrt
        obs = self.obs[k] if obs is None else obs
        v = np.where(np.isnan(nrt), 0.0, nrt)
        return E.refill(v, obs, self.climd[k], b, mode)

    def season_max(self, k, sst):
        return E.season_max(np.where(np.isnan(sst), -99.0, sst), self.mmm[self.codes[k]], self.season)

    def golden(self):
        b = self.bias()
        return b, [self.season_max(k, self.refilled(k, b)) for k in range(len(self.codes))]

    def golden_alt(self, first_issue=False, mmm_from_clim=False, missing_zero=False, window_before=False,
                   strict=False, flag_by_date=False):
        """the golden under a convention read another way: the first issue of each day kept, the maximum monthly mean
        recomputed from the climatology file, the day never issued left without a HotSpot, the 84 days before the day
        rather than ending on it, HotSpots strictly above 1.0"""
        nrt, obs = self.nrt, self.obs
        if flag_by_date:
            n = self.nrt_raw.sort_values("issued_utc").drop_duplicates(["pixel_id", "date"], keep="last")
            obs_code = np.where(n.date.values >= "2027-07-15", 2, 1)
            obs = np.zeros_like(self.obs)
            si = {c: k for k, c in enumerate(self.codes)}
            for pix, d, o in zip(n.pixel_id, n.date, n.obs_flag.values == obs_code):
                obs[si[self.pix[pix]], self.di[d]] = o
        if first_issue:
            n = self.nrt_raw.sort_values("issued_utc").drop_duplicates(["pixel_id", "date"], keep="first")
            obs_code = np.where(n.product_version == "3.2", 2, 1)
            nrt = np.full_like(self.nrt, np.nan)
            obs = np.zeros_like(self.obs)
            si = {c: k for k, c in enumerate(self.codes)}
            for pix, d, v, o in zip(n.pixel_id, n.date, n.sst_c, n.obs_flag.values == obs_code):
                nrt[si[self.pix[pix]], self.di[d]] = v
                obs[si[self.pix[pix]], self.di[d]] = o
        both = self.past & ~np.isnan(self.rep) & ~np.isnan(nrt)
        b = float(np.mean((nrt - self.rep)[both & obs]))
        out = []
        for k, c in enumerate(self.codes):
            m = self.mmm[c]
            if mmm_from_clim:
                y = np.array([d.year == 2019 for d in self.days])
                m = round(max(float(np.mean(self.climd[k][y & (self.mon == mm)])) for mm in range(1, 13)), 2)
            x = self.refilled(k, b, nrt=nrt[k], obs=obs[k])
            if missing_zero:
                x = np.where(np.isnan(nrt[k]), -99.0, x)
            hs = x - m
            hs = np.where(hs > P.HS_MIN if strict else hs >= P.HS_MIN, hs, 0.0)
            cs = np.concatenate([[0.0], np.cumsum(hs)])
            n = len(hs)
            if window_before:
                hi = np.arange(n)
                lo = np.maximum(0, hi - P.WINDOW)
            else:
                hi = np.arange(n) + 1
                lo = np.maximum(0, np.arange(n) - (P.WINDOW - 1))
            d = (cs[hi] - cs[lo]) / 7.0
            out.append(float(d[self.season].max()))
        return b, out

    def rungs(self):
        """each rung's season maxima: the record as issued (as the bulletins read it), its pooled mean difference
        taken out, the mean differences of observed and not observed days taken out, the regression of not-observed
        days' anomalies, and the refill without the clear-sky difference"""
        S = len(self.codes)
        both = self.past & ~np.isnan(self.rep) & ~np.isnan(self.nrt)
        b_all = float(np.mean((self.nrt - self.rep)[both]))
        b_obs = float(np.mean((self.nrt - self.rep)[both & self.obs]))
        b_fill = float(np.mean((self.nrt - self.rep)[both & ~self.obs]))
        fa = (self.nrt - self.climd)[both & ~self.obs]
        ra = (self.rep - self.climd)[both & ~self.obs]
        k1, k0 = np.polyfit(fa, ra, 1)
        out = {"as issued": [], "pooled": [], "flag": [], "regression": [], "refill, no difference": []}
        for k in range(S):
            x = self.nrt[k]
            out["as issued"].append(self.season_max(k, x))
            out["pooled"].append(self.season_max(k, x - b_all))
            out["flag"].append(self.season_max(k, x - np.where(self.obs[k], b_obs, b_fill)))
            out["regression"].append(self.season_max(k, np.where(self.obs[k], x - b_obs,
                                                                   self.climd[k] + k0 + k1 * (x - self.climd[k]))))
            out["refill, no difference"].append(self.season_max(k, self.refilled(k, 0.0)))
        return out, dict(b_all=b_all, b_obs=b_obs, b_fill=b_fill, k0=float(k0), k1=float(k1))

    def variants(self, b):
        """the refill's own variants: temperature instead of anomaly, a shape-preserving curve, each site's own or the
        heat seasons' clear-sky difference, the last observed anomaly carried, the nearer observed day"""
        S = len(self.codes)
        both = self.past & ~np.isnan(self.rep) & ~np.isnan(self.nrt)
        heat = both & self.obs & (self.mon >= 6) & (self.mon <= 10)
        b_heat = float(np.mean((self.nrt - self.rep)[heat]))
        out = {}
        for name, f in [("temperature", lambda k: self.refilled(k, b, "temperature")),
                        ("pchip", lambda k: self.refilled(k, b, "pchip")),
                        ("site difference", lambda k: self.refilled(k, float(np.mean((self.nrt[k] - self.rep[k])[both[k] & self.obs[k]])))),
                        ("heat-season difference", lambda k: self.refilled(k, b_heat)),
                        ("carry", lambda k: self.refilled(k, b, "carry")),
                        ("nearest", lambda k: self.refilled(k, b, "nearest"))]:
            out[name] = [self.season_max(k, f(k)) for k in range(S)]
        return out

    def backtest(self, b):
        """past evidence on the days the near-real-time analysis did not observe: each reconstruction's error against
        the reprocessed record, overall and on the hot days (anomaly above 0.6), 2018 to 2026"""
        both = self.past & ~np.isnan(self.rep) & ~np.isnan(self.nrt)
        stats = {}
        rungs, c = self.rungs()
        for name, f in [("as issued", lambda k: self.nrt[k]),
                        ("flag", lambda k: self.nrt[k] - np.where(self.obs[k], c["b_obs"], c["b_fill"])),
                        ("regression", lambda k: np.where(self.obs[k], self.nrt[k] - c["b_obs"],
                                                          self.climd[k] + c["k0"] + c["k1"] * (self.nrt[k] - self.climd[k]))),
                        ("refill", lambda k: self.refilled(k, b)),
                        ("carry", lambda k: self.refilled(k, b, "carry")),
                        ("nearest", lambda k: self.refilled(k, b, "nearest"))]:
            e, h = [], []
            for k in range(len(self.codes)):
                m = both[k] & ~self.obs[k]
                d = (f(k) - self.rep[k])[m]
                e.append(d)
                h.append((f(k) - self.rep[k])[m & ((self.rep[k] - self.climd[k]) > 0.6)])
            e, h = np.concatenate(e), np.concatenate(h)
            stats[name] = (float(np.sqrt(np.mean(e ** 2))), float(np.mean(h)), len(e), len(h))
        return stats

    # ------------------------------------------------------------ the bulletins
    def declared(self):
        wb = pd.read_excel(os.path.join(self.t, self.F["bulletins"]), header=3)
        wb = wb[(wb["Analysis day"] >= SEASON[0].isoformat()) & (wb["Analysis day"] <= SEASON[1].isoformat())]
        out = {}
        for c in self.codes:
            lv = wb[wb["Site"] == c]["Alert level"]
            out[c] = max(lv, key=LEVELS.index)
        return out

    # ------------------------------------------------------------ ask A: the 2023 survey
    def survey(self, collapse=True, filters=True, any_size=False):
        df = pd.read_csv(os.path.join(self.t, self.F["survey"]))
        if filters:
            depth = dict(zip(self.sites.site_code, self.sites.survey_depth_m))
            df = df[(df.sheet == "S") & ((df.depth_m - df.site_code.map(depth)).abs() <= 2.0)
                    & df.genus.isin(STONY) & (df.max_diameter_cm >= 10)]
        n_col, n_bl = {}, {}
        for (site, tr, sh), g in df.groupby(["site_code", "transect", "sheet"]):
            g = g.sort_values(["metre", "line"])
            seen = []
            count = 0
            bleached = 0
            for r in g.itertuples(index=False):
                key = (r.genus, r.max_diameter_cm, r.condition)
                if collapse and (any_size or r.max_diameter_cm >= 100) and any(k == key and m == r.metre - 1
                                                                                for k, m in seen):
                    seen.append((key, r.metre))
                    continue
                seen.append((key, r.metre))
                count += 1
                bleached += r.condition in ("P", "PB", "BL")
            n_col[site] = n_col.get(site, 0) + count
            n_bl[site] = n_bl.get(site, 0) + bleached
        return {c: (100.0 * n_bl[c] / n_col[c], n_col[c]) for c in self.codes}

    # ------------------------------------------------------------ ask B: the loggers
    def logger_hours(self, gps=True, trim=True):
        dep = pd.read_csv(os.path.join(self.t, self.F["deployments"]), dtype={"serial": str})
        rd = pd.read_csv(os.path.join(self.t, self.F["readings"]), dtype={"serial": str})
        rd["t"] = pd.to_datetime(rd.datetime_local)
        out = {c: 0 for c in self.codes}
        for r in dep.itertuples(index=False):
            if not isinstance(r.retrieved, str):
                continue
            a, z = pd.Timestamp(r.deployed), pd.Timestamp(r.retrieved)
            if gps and r.deployed_from == GPS_UTC[0] and a.date() < GPS_UTC[1]:
                a -= pd.Timedelta(hours=5)
            if gps and r.retrieved_from == GPS_UTC[0] and z.date() < GPS_UTC[1]:
                z -= pd.Timedelta(hours=5)
            x = rd[rd.serial == r.serial]
            if trim:
                x = x[(x.t >= a) & (x.t <= z)]
            x = x[x.t.dt.year.isin([2024, 2025, 2026]) & x.t.dt.month.between(6, 10)]
            out[r.site_code] += int((x.temperature_c >= self.mmm[r.site_code]).sum())
        return out


def solve(target, F):
    pk = Pack(target, F)
    b, gold = pk.golden()
    decl = pk.declared()
    rows = []
    for k, c in enumerate(pk.codes):
        lv = level(gold[k])
        rows.append(dict(site=c, name=pk.sites.site_name[k], region=pk.sites.region[k], dhw=gold[k],
                         dhw_round=int(round(gold[k])), level=lv, declared=decl[c], verdict=verdict(lv, decl[c])))
    return pk, b, rows
