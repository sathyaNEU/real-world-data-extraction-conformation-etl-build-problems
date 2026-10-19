"""Read the task249 pack as a solver would and compute the golden, every rung and both asks."""
import datetime as dt
import math
import os
import re
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd

MAD = ZoneInfo("Europe/Madrid")
UTC = dt.timezone.utc
CET = dt.timezone(dt.timedelta(hours=1))
BAND = (0.85, 1.15)
UG = 1.996


def local_utc(y, m, d):
    return pd.Timestamp(dt.datetime(y, m, d, tzinfo=MAD).astimezone(UTC))


class Pack:
    def __init__(self, target, F):
        self.target, self.F = target, F
        p = lambda k: os.path.join(target, F[k])
        self.reg = pd.read_csv(p("register"))
        self.codes = list(self.reg.node_id)
        self.raw = pd.read_csv(p("nodes"), dtype={"o3_ppb": float})
        self.val = pd.read_csv(p("validated"), dtype={"o3_ugm3": float})
        self.prov = pd.read_csv(p("provisional"), dtype={"o3_ugm3": float})
        self.fw = self._firmware(p("log"))
        self._nodes()
        self._analysers()

    # -- the maintenance log: firmware 4.2 dates, and the spare's temporary id --
    def _firmware(self, path):
        from pypdf import PdfReader
        text = " ".join(pg.extract_text() for pg in PdfReader(path).pages)
        out = {}
        for c, d in re.findall(r"(OZ\d\d)\s+(\d\d \w\w\w 2028)", text):
            out[c] = pd.Timestamp(dt.datetime.strptime(d, "%d %b %Y").replace(hour=10, tzinfo=MAD).astimezone(UTC))
        self.spare = re.search(r"reported as (OZ\d\dB)", text).group(1)
        # the replaced node runs 4.2 from the spare's start (the firmware table gives it no date of its own)
        m = re.search(r"(\d{1,2} \w{3} 2028)\s*(OZ\d\d): spare unit.*?up at\s*(\d{1,2}):(\d\d)", text, re.S)
        out[m.group(2)] = pd.Timestamp(dt.datetime.strptime(m.group(1), "%d %b %Y").replace(
            hour=int(m.group(3)), minute=int(m.group(4)), tzinfo=MAD).astimezone(UTC))
        return out

    def _nodes(self, dedup="latest", merge_spare=True, fw_aware=True, retime=True):
        d = self.raw.copy()
        d["start"] = pd.to_datetime(d.reading_start_utc, utc=True)
        d["recv"] = pd.to_datetime(d.received_utc, utc=True)
        if retime:
            # a record stamped in 2000 came from a clock counting from a restart: its received time places it
            old = d.start < pd.Timestamp("2020-01-01", tz=UTC)
            off = d.start[old] - pd.Timestamp("2000-01-01", tz=UTC)
            d.loc[old, "start"] = (d.recv[old] - off - pd.Timedelta(minutes=30)).dt.floor("h") + off
        if merge_spare:
            d["fw42"] = d.node_id == self.spare
            d["node_id"] = d.node_id.replace({self.spare: self.spare[:-1]})
        else:
            d["fw42"] = False
        if dedup == "latest":
            d = d.sort_values(["node_id", "start", "recv"]).drop_duplicates(["node_id", "start"], keep="last")
        elif dedup == "first":
            d = d.sort_values(["node_id", "start", "recv"]).drop_duplicates(["node_id", "start"], keep="first")
        fw = d.node_id.map(self.fw)
        after = d.fw42 | (d.start >= fw)
        if fw_aware:
            d["ok"] = (d.status == 0) | ((d.status == 1) & after)
        else:
            d["ok"] = d.status.isin([0, 1])          # the dictionary's codes read for the whole record
        d["hour"] = d.start.dt.floor("h")
        self.d = d

    def _analysers(self):
        def stamp(df):
            end = pd.to_datetime(df.fecha, format="%d/%m/%Y") + pd.to_timedelta(df.hora, unit="h")
            return (end - pd.Timedelta(hours=1)).dt.tz_localize(CET).dt.tz_convert(UTC)
        self.prov["start"] = stamp(self.prov)
        self.val["start"] = stamp(self.val)

    # -- the main call --
    def window(self):
        return local_utc(2028, 4, 6), local_utc(2028, 6, 1)

    def hourly(self, statuses=None, hours=None):
        """Each node's accepted hourly ozone (ppb) in the window: Series indexed by UTC hour start. hours: (a, b) keeps
        the hours starting a:00 to b:00 local time."""
        w0, w1 = self.window()
        d = self.d[(self.d.hour >= w0) & (self.d.hour < w1)]
        if hours:
            lh = d.hour.dt.tz_convert(MAD).dt.hour
            d = d[(lh >= hours[0]) & (lh < hours[1])]
        ok = d.ok if statuses is None else d.status.isin(statuses)
        d = d[ok & d.o3_ppb.notna()]
        return {c: g.groupby("hour").o3_ppb.mean() for c, g in d.groupby("node_id")}

    def refs(self, factor=UG, hours=None):
        w0, w1 = self.window()
        a = self.prov[(self.prov.start >= w0) & (self.prov.start < w1) & (self.prov.validacion == "P") & self.prov.o3_ugm3.notna()]
        if hours:
            lh = a.start.dt.tz_convert(MAD).dt.hour
            a = a[(lh >= hours[0]) & (lh < hours[1])]
        return {s: g.set_index("start").o3_ugm3 / factor for s, g in a.groupby("estacion")}

    def nearest(self):
        import params as P
        lat0, lon0 = P.LAT0, P.LON0
        out = {}
        st = {code: (P.LAT0 + y / 111.0, P.LON0 + x / (111.0 * math.cos(math.radians(P.LAT0)))) for code, _, x, y in P.ANALYSERS}
        for _, r in self.reg.iterrows():
            dist = {s: math.hypot((r.lat - a) * 111.0, (r.lon - b) * 111.0 * math.cos(math.radians(r.lat))) for s, (a, b) in st.items()}
            out[r.node_id] = min(dist, key=dist.get)
        return out

    def spans(self, method="dm", factor=UG, statuses=None, hours=(12, 18)):
        H = self.hourly(statuses, hours)
        R = self.refs(factor, hours)
        pool = pd.concat(list(R.values()))
        near = self.nearest()
        m4 = pd.concat(R, axis=1).dropna().mean(axis=1)
        out = {}
        for c in self.codes:
            x = H[c]
            r = R[near[c]]
            if method == "dm":
                out[c] = x.std(ddof=0) / pool.std(ddof=0)
            elif method == "dm_near":
                out[c] = x.std(ddof=0) / r.std(ddof=0)
            elif method in ("iqr", "q90"):
                lo, hi = (25, 75) if method == "iqr" else (10, 90)
                out[c] = np.subtract(*np.percentile(x, [hi, lo])) / np.subtract(*np.percentile(pool, [hi, lo]))
            elif method == "qq":
                q = np.linspace(2, 98, 49)
                out[c] = np.polyfit(np.percentile(pool, q), np.percentile(x, q), 1)[0]
            elif method == "dm_daily":
                dx = x.groupby(x.index.tz_convert(MAD).date).mean()
                dp = pd.concat([g.groupby(g.index.tz_convert(MAD).date).mean() for g in R.values()])
                out[c] = dx.std(ddof=0) / dp.std(ddof=0)
            else:
                j = pd.concat([x, r if method != "ols_m4" else m4], axis=1, join="inner").dropna()
                y, z = j.iloc[:, 0].values, j.iloc[:, 1].values
                if method == "ols_h":
                    out[c] = np.polyfit(z, y, 1)[0]
                elif method == "ols_m4":
                    out[c] = np.polyfit(z, y, 1)[0]
                elif method == "ols_d":
                    jj = j.groupby(j.index.tz_convert(MAD).date).mean()
                    out[c] = np.polyfit(jj.iloc[:, 1].values, jj.iloc[:, 0].values, 1)[0]
                elif method == "rom":
                    out[c] = x.mean() / r.mean()
                elif method == "deming":
                    sxx, syy, sxy = z.var(), y.var(), np.cov(z, y, bias=True)[0, 1]
                    out[c] = (syy - sxx + math.sqrt((syy - sxx) ** 2 + 4 * sxy ** 2)) / (2 * sxy)
        return out

    def pulled(self, sp):
        return {c: ("low" if v < BAND[0] else "high") for c, v in sp.items() if not BAND[0] <= v <= BAND[1]}

    # -- ask A: hours with an accepted reading, 1 November 2027 to 31 January 2028, local time --
    def ask_a(self, grid="local", count="hours"):
        d = self.d
        if grid == "local":
            lo, hi = local_utc(2027, 11, 1), local_utc(2028, 2, 1)
        else:
            lo, hi = pd.Timestamp("2027-11-01", tz=UTC), pd.Timestamp("2028-02-01", tz=UTC)
        d = d[(d.hour >= lo) & (d.hour < hi) & d.ok & d.o3_ppb.notna()]
        if count == "rows":
            s = d.groupby("node_id").size()
        else:
            s = d.groupby("node_id").hour.nunique()
        return {c: int(s.get(c, 0)) for c in self.codes}

    # -- ask B: days in 2027 with a maximum daily 8-hour mean above 120 micrograms --
    def ask_b(self, keep_old=False, flags=("V",), shift=0):
        v = self.val[self.val.validacion.isin(flags) & self.val.o3_ugm3.notna()].copy()
        swap = pd.Timestamp(dt.datetime(2027, 7, 4, 9, tzinfo=UTC))
        if not keep_old:
            v = v[~((v.estacion == "ES4103A") & (v.analizador == "TE49i-0921") & (v.start >= swap))]
        out = {}
        for s, g in v.groupby("estacion"):
            h = g.groupby("start").o3_ugm3.mean()
            idx = pd.date_range(pd.Timestamp("2026-12-30 23:00", tz=UTC), pd.Timestamp("2027-12-31 22:00", tz=UTC), freq="h")
            h = h.reindex(idx)
            cnt = h.rolling(8, min_periods=1).count()
            mean8 = h.rolling(8, min_periods=1).mean().where(cnt >= 6)
            end_label = (idx + pd.Timedelta(hours=1 + shift)).tz_convert(CET)        # the hour each mean ends
            day = (end_label - pd.Timedelta(minutes=1)).date
            m = pd.DataFrame({"m": mean8.values, "day": day})
            m = m[(m.day >= dt.date(2027, 1, 1)) & (m.day <= dt.date(2027, 12, 31))]
            agg = m.groupby("day").m.agg(["count", "max"])
            out[s] = int(((agg["count"] >= 18) & (agg["max"] > 120)).sum())
        return out


def solve(target, F):
    pk = Pack(target, F)
    sp = pk.spans("dm")
    return pk, sp, pk.pulled(sp)


def analyser_pairs(pk, hours=None):
    """Each analyser's hourly ozone against each other's over the window: (paired slope, spread ratio)."""
    R = pk.refs(hours=hours)
    out = {}
    for a in sorted(R):
        for b in sorted(R):
            if a < b:
                j = pd.concat([R[a], R[b]], axis=1, join="inner").dropna()
                out[(a, b)] = (np.polyfit(j.iloc[:, 1], j.iloc[:, 0], 1)[0], R[a].std(ddof=0) / R[b].std(ddof=0))
    return out
