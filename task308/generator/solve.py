"""The pack-only solver: reads target/ alone and computes the golden and every rung the ladder names. Nothing here
imports the world."""
import os
import re

import numpy as np
import pandas as pd

import params as P

FORCED = ["U1", "U2", "U3", "SF", "D1", "D2", "D3"]
DERATE = ["D1", "D2", "D3"]


def _f(target, name):
    return os.path.join(target, name)


class Pack:
    def __init__(self, target, files):
        self.t = target
        self.F = files
        self._load()

    # ------------------------------------------------------------------ the planning table on a UTC clock
    def _load(self):
        tb = pd.read_csv(_f(self.t, self.F["table"]), dtype={"hour_ending": str})
        second = tb.hour_ending == "2*"
        he = tb.hour_ending.str.replace("*", "", regex=False).astype(int)
        wall = pd.to_datetime(tb.local_date) + pd.to_timedelta(he - 1, unit="h")
        # the first 01:00 of the autumn change is daylight time, the 2* row standard time
        amb = np.where(second, False, True)
        loc = pd.DatetimeIndex(wall).tz_localize(P.TZ, ambiguous=amb, nonexistent="raise")
        tb["utc"] = loc.tz_convert("UTC")
        kw = tb.load_2027_mw > 50000
        self.kw_years = sorted(tb.weather_year[kw].unique().tolist())
        tb.loc[kw, "load_2027_mw"] = tb.loc[kw, "load_2027_mw"] / 1000.0
        tb = tb.sort_values("utc").reset_index(drop=True)
        self.tb = tb
        self.utc = pd.DatetimeIndex(tb.utc)
        self.n = len(tb)
        fl = pd.read_excel(_f(self.t, self.F["fleet"]), sheet_name="Units")
        fl = fl[fl["Retirement date"].isna() | (pd.to_datetime(fl["Retirement date"]) >= "2027-12-31")]
        self.fleet = fl.reset_index(drop=True)
        self.caps = dict(zip(fl["GADS unit code"], fl["Net winter capability (MW)"].astype(float)))
        self.ct = fl[fl["Technology"] == "Combustion Turbine"]["GADS unit code"].tolist()
        self.ev = pd.read_csv(_f(self.t, self.F["events"]))
        self.ev["start"] = pd.to_datetime(self.ev.start_utc, utc=True)
        self.ev["end"] = pd.to_datetime(self.ev.end_utc, utc=True)
        self.av = self.avail()
        self.tie = self.tie_share()
        pr = pd.read_parquet(_f(self.t, self.F["profiles"]))
        pr["utc"] = pd.to_datetime(pr.hour_beginning_utc).dt.tz_localize("UTC")
        pr = pr.set_index("utc").reindex(self.utc)
        self.wind_new = pr.sandhill_draw_mw_per_mw.values * P.OFFER_MW["Sandhill Draw"]
        self.solar_new = pr.coulee_flats_mw_per_mw.values * P.OFFER_MW["Coulee Flats"]
        self.short = (self.tb.load_2027_mw.values - self.tb.wind_mw.values - self.tb.solar_mw.values
                      - sum(self.av.values()) - P.IMPORT_EX_MW * self.tie)

    def _integrate(self, s, f, lost_per_event, cap=None):
        t0 = self.utc[0]
        nh = self.n
        s = np.asarray(s)
        f = np.asarray(f)
        pts = np.unique(np.clip(np.concatenate([s, f, [0.0, float(nh)]]), 0, nh))
        mid = (pts[:-1] + pts[1:]) / 2
        lost = np.zeros(len(mid))
        for k in range(len(s)):
            on = (mid > s[k]) & (mid < f[k])
            lost = np.where(on, np.maximum(lost, lost_per_event[k]), lost)
        cum = np.concatenate([[0.0], np.cumsum(lost * np.diff(pts))])
        F = np.interp(np.arange(nh + 1, dtype=float), pts, cum)
        return np.diff(F)

    def avail(self, latest=True, forced_only=True, codes=None):
        ev = self.ev
        if latest:
            ev = ev.sort_values("revision").drop_duplicates("event_id", keep="last")
        if forced_only:
            ev = ev[ev.event_type.isin(FORCED)]
        t0 = self.utc[0]
        out = {}
        for code in (codes or list(self.caps)):
            cap = self.caps[code]
            e = ev[ev.unit_code == code]
            if e.empty:
                out[code] = np.full(self.n, cap)
                continue
            s = (e.start - t0).dt.total_seconds().values / 3600.0
            f = (e.end - t0).dt.total_seconds().values / 3600.0
            lost = np.where(e.event_type.isin(DERATE), cap - e.net_available_mw.fillna(0).values, cap)
            out[code] = cap - self._integrate(s, f, lost)
        return out

    def tie_share(self, forced_only=False):
        tl = pd.read_csv(_f(self.t, self.F["tie"]))
        if forced_only:
            tl = tl[tl.kind == "Forced"]

        def parse(x):
            m = re.match(r"(\d\d/\d\d/\d{4} \d\d:\d\d) (CST|CDT)", x)
            off = -6 if m.group(2) == "CST" else -5
            return pd.Timestamp(m.group(1)) - pd.Timedelta(hours=off)
        s = np.array([(parse(x) - self.utc[0].tz_convert(None)).total_seconds() / 3600 for x in tl.out_of_service])
        f = np.array([(parse(x) - self.utc[0].tz_convert(None)).total_seconds() / 3600 for x in tl.returned_to_service])
        return 1.0 - self._integrate(s, f, np.ones(len(s)))

    # ------------------------------------------------------------------ the main call
    def eue(self, add=0.0):
        return float(np.clip(self.short - add, 0, None).sum()) / P.N_YEARS

    def class_share(self):
        return sum(self.av[c] for c in self.ct) / sum(self.caps[c] for c in self.ct)

    def ct_rate(self, exclude_fuel=False):
        """the class's forced outage rate over the ten years, from the replayed hours"""
        if not exclude_fuel:
            return 1.0 - float(self.class_share().mean())
        ev = self.ev.sort_values("revision").drop_duplicates("event_id", keep="last")
        keep = ev[ev.cause_code != 9130]
        saved = self.ev
        self.ev = keep
        av = self.avail(latest=False, codes=self.ct)
        self.ev = saved
        return 1.0 - float(sum(av.values()).sum() / (sum(self.caps[c] for c in self.ct) * self.n))

    def removed(self, route="golden"):
        """EUE removed by each offer under a route for the peaker; the import, wind and solar replay the record"""
        base = self.eue()
        mw = P.OFFER_MW["Ketchum Ridge"]
        if route == "golden":
            ct = mw * self.class_share()
        elif route == "rated":
            ct = mw * (1 - P.CT_RATED_EFORD)
        elif route == "class_avg":
            ct = mw * (1 - self.ct_rate())
        elif route == "class_avg_no_fuel":
            ct = mw * (1 - self.ct_rate(exclude_fuel=True))
        elif route == "nameplate":
            ct = np.full(self.n, mw)
        else:
            raise ValueError(route)
        return {"Ketchum Ridge": base - self.eue(ct),
                "Red Willow import": base - self.eue(P.OFFER_MW["Red Willow import"] * self.tie),
                "Sandhill Draw": base - self.eue(self.wind_new),
                "Coulee Flats": base - self.eue(self.solar_new)}

    def net(self, removed):
        return {o: (removed[o] * P.VOLL - P.annual_payment(o)) / 1e6 for o in P.OFFERS}

    def call(self, route="golden"):
        rem = self.removed(route)
        net = self.net(rem)
        best = max(net, key=net.get)
        return dict(base=self.eue(), removed=rem, net=net, best=best)

    def shortfall_facts(self):
        s = np.clip(self.short, 0, None)
        share = self.class_share()
        allout = share < 0.01
        return dict(hours=int((s > 0).sum()), hours_per_year=(s > 0).sum() / P.N_YEARS,
                    share_in_allout=float(s[allout].sum() / s.sum()),
                    allout_hours=int(((s > 0) & allout).sum()))


# ---------------------------------------------------------------------------------------------- the asks
class Meter:
    def __init__(self, target, files):
        self.t = target
        ex = pd.read_parquet(_f(target, files["meter"]))
        ex["t"] = pd.to_datetime(ex.interval_start, utc=True)
        self.raw = ex
        self.reg = pd.read_excel(_f(target, files["dps"]), sheet_name="Delivery points")
        self.hist = pd.read_excel(_f(target, files["dps"]), sheet_name="Assignment history")
        self.orders = pd.read_csv(_f(target, files["orders"]))

    def latest(self):
        ex = self.raw.sort_values("version").drop_duplicates(["dp_id", "t"], keep="last")
        return ex.sort_values(["dp_id", "t"]).reset_index(drop=True)

    def member_of(self, ex, by_label_time=True, transfer=True):
        h = self.hist.copy()
        h["from"] = pd.to_datetime(h["Effective from"]).dt.tz_localize(P.TZ)
        h["to"] = pd.to_datetime(h["Effective to"]).dt.tz_localize(P.TZ) + pd.Timedelta(days=1)
        mem = pd.Series(index=ex.index, dtype=object)
        if not transfer:
            cur = dict(zip(self.reg["Delivery point"], self.reg["Member (31 Dec 2025)"]))
            return ex.dp_id.map(cur)
        for _, r in h.iterrows():
            on = (ex.dp_id == r["Delivery point"]) & (ex.t >= r["from"])
            if pd.notna(r["to"]):
                on &= ex.t < r["to"]
            mem[on] = r["Member"]
        return mem

    def corrected(self, fix_mult=True, fix_clock=True, net=True, latest=True):
        ex = self.latest() if latest else self.raw.copy()
        ex = ex.copy()
        kwh = ex.kwh_del - (ex.kwh_rec if net else 0.0)
        if fix_mult:
            o = self.orders[self.orders.work_type == "Current transformer replacement"]
            for _, r in o.iterrows():
                m = re.search(r"Meter multiplier (\d+) to (\d+)", r.notes)
                new = float(m.group(2))
                when = pd.Timestamp(r.completed).tz_localize(P.TZ)
                sel = (ex.dp_id == r.dp_id) & (ex.t >= when) & (ex.multiplier != new)
                kwh[sel] = kwh[sel] * new / ex.multiplier[sel]
        ex["kwh"] = kwh
        if fix_clock:
            o = self.orders[self.orders.notes.str.contains("found on standard time", na=False)]
            start = pd.Timestamp("2025-03-09 03:00", tz=P.TZ)
            drop = []
            for _, r in o.iterrows():
                # the meter records on the corrected clock from the first interval after the visit
                reset = pd.Timestamp(r.completed).tz_localize(P.TZ).ceil("h")
                sel = (ex.dp_id == r.dp_id) & (ex.t >= start) & (ex.t < reset - pd.Timedelta(hours=1))
                ex.loc[sel, "t"] = ex.loc[sel, "t"] + pd.Timedelta(hours=1)
                # the MDM's estimate for the stamp the reset skipped now sits on an hour the meter recorded
                drop += ex.index[(ex.dp_id == r.dp_id) & (ex.t == reset - pd.Timedelta(hours=1)) &
                                 (ex.quality == "E")].tolist()
            ex = ex.drop(index=drop)
        return ex

    def energy(self, **kw):
        tr = kw.pop("transfer", True)
        kw.setdefault("fix_clock", False)
        ex = self.corrected(**kw)
        ex["member"] = self.member_of(ex, transfer=tr)
        return (ex.groupby("member").kwh.sum() / 1000.0).reindex(P.MEMBERS)

    def cp12(self, **kw):
        tr = kw.pop("transfer", True)
        ex = self.corrected(**kw)
        ex["member"] = self.member_of(ex, transfer=tr)
        ex["month"] = ex.t.dt.tz_convert(P.TZ).dt.month
        tot = ex.groupby("t").kwh.sum()
        mon = pd.Series(tot.index.tz_convert(P.TZ).month, index=tot.index)
        peaks = tot.groupby(mon).idxmax()
        rows = ex[ex.t.isin(list(peaks))]
        con = rows.groupby(["month", "member"]).kwh.sum().unstack(fill_value=0.0)
        return (con.mean(axis=0) / 1000.0).reindex(P.MEMBERS), peaks
