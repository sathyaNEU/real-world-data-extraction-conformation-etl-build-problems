"""The pack's records: the nodes' export, the register, the regional network's releases and the station's weather."""
import datetime as dt
import unicodedata
import math
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import params as P
import nodes as N
import heads as H
import sim

MAD = ZoneInfo("Europe/Madrid")
CET = dt.timezone(dt.timedelta(hours=1))
_FIELD = None


def field():
    global _FIELD
    if _FIELD is None:
        _FIELD = sim.field(H.sites(), exposure=H.exposure())
    return _FIELD


def utc_of_local(t):
    return t.replace(tzinfo=MAD).astimezone(P.UTC)


EPOCH = dt.datetime(2000, 1, 1, tzinfo=P.UTC)       # a node's clock after a restart, until it is set


def next_weekly(t):
    """the first weekly restart (Sunday 03:00 local time) after t; the node sets its clock from the network then"""
    loc = t.astimezone(MAD)
    d = loc.date()
    while True:
        c = dt.datetime.combine(d, dt.time(3)).replace(tzinfo=MAD)
        if c.weekday() == 6 and c > loc:
            return c.astimezone(P.UTC)
        d += dt.timedelta(days=1)


def stamped(start, episodes):
    """the start the node writes: its own clock, which counts from 2000-01-01 after any restart but the weekly one"""
    for r0, r1 in episodes:
        if r0 <= start < r1:
            return EPOCH + (start - r0)
    return start


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


class World:
    def __init__(self):
        self.true = field()
        self.t = [sim.hour(i) for i in range(sim.HOURS)]
        self.rh = self._humidity()

    # -- weather at Alcorna - Parque (also drives the heads' humidity compensation) --
    def _humidity(self):
        r = np.random.default_rng(77)
        h = np.arange(sim.HOURS)
        doy = (h / 24.0) % 365.25
        loc = (h + 1) % 24
        base = 62 - 22 * np.sin(2 * np.pi * (doy - 105) / 365.25)
        diur = 18 * np.cos(2 * np.pi * (loc - 5) / 24.0)
        e = np.zeros(sim.HOURS)
        z = r.standard_normal(sim.HOURS)
        for i in range(1, sim.HOURS):
            e[i] = 0.97 * e[i - 1] + 0.243 * z[i]
        return np.clip(base + diur + 9 * e, 8, 100)

    def weather(self):
        r = np.random.default_rng(78)
        i0 = sim.index(dt.datetime(2027, 10, 1, tzinfo=P.UTC))
        rows = []
        h = np.arange(sim.HOURS)
        doy = (h / 24.0) % 365.25
        temp = 14 + 10 * np.sin(2 * np.pi * (doy - 110) / 365.25) + 6 * np.sin(2 * np.pi * (((h + 1) % 24) - 9) / 24.0)
        temp = temp + np.convolve(r.standard_normal(sim.HOURS + 48), np.ones(48) / 6.0, "same")[:sim.HOURS]
        ws = np.abs(2.6 + 1.6 * r.standard_normal(sim.HOURS))
        wd = (240 + 70 * r.standard_normal(sim.HOURS)) % 360
        for i in range(i0, sim.HOURS):
            loc = self.t[i].astimezone(CET)
            rows.append((loc.strftime("%d/%m/%Y"), loc.hour + 1, round(float(temp[i]), 1), int(round(self.rh[i])),
                         round(float(ws[i]), 1), int(round(wd[i])) % 360))
        return pd.DataFrame(rows, columns=["fecha", "hora", "temperatura", "humedad", "vel_viento", "dir_viento"])

    # -- the nodes --
    def node_rows(self):
        """One row per record the centre received: node_id, reading_start_utc, o3_ppb, status, received_utc."""
        out = []
        true = self.true
        storm0, storm1 = utc_of_local(dt.datetime(2027, 11, 27, 14)), utc_of_local(dt.datetime(2027, 11, 27, 19))
        cut0, cut1 = utc_of_local(dt.datetime(2027, 12, 12, 8)), utc_of_local(dt.datetime(2027, 12, 14, 2))
        storm_towns = {"Villarejo de Mencia", "Campillo de Mencia", "Peñalba de Alcorna"}
        for i, (code, town, _, _) in enumerate(N.NODES):
            rng = np.random.default_rng(3000 + i)
            half = code in N.MODEL_B
            vals = H.readings(true, code, half=half)
            t0 = H.paths(code)[0]
            fw = utc_of_local(dt.datetime.combine(N.FW_DATES[code], dt.time(10)))
            restarts = [storm1] if town in storm_towns else []
            if code != N.REPLACED[0]:
                restarts.append(fw)                      # the update installs at once and restarts the node
            if code in N.MOVES:
                restarts.append(utc_of_local(dt.datetime.combine(N.MOVES[code][2], dt.time(11))))
            episodes = [(r0, next_weekly(r0)) for r0 in restarts]
            rh_off = rng.normal(0, 4)
            faults = set()
            for _ in range(rng.integers(1, 4)):        # a few heater faults, each a few hours
                a = int(rng.integers(t0 + 24, sim.HOURS - 24))
                faults.update(range(a, a + int(rng.integers(2, 7))))
            lost = set()                                 # link drops too long for the buffer: hours never received
            for _ in range(int(rng.integers(4, 16))):
                a = int(rng.integers(t0 + 24, sim.HOURS - 24))
                lost.update(range(a, a + int(rng.integers(1, 9))))
            if rng.uniform() < 0.25:                     # a router fault: a few days off the network
                a = int(rng.integers(t0 + 24, sim.HOURS - 200))
                lost.update(range(a, a + int(rng.integers(30, 110))))
            lag = rng.uniform(2, 9)                      # minutes from the end of the record to its arrival
            for k in range(t0, sim.HOURS):
                t = self.t[k]
                if code == N.REPLACED[0] and utc_of_local(N.REPLACED[1]) <= t:
                    break                                # the failed unit's last record
                if town in storm_towns and storm0 <= t < storm1:
                    continue
                if k in lost:
                    continue
                if code in N.MOVES and utc_of_local(dt.datetime.combine(N.MOVES[code][2], dt.time(8))) <= t < \
                        utc_of_local(dt.datetime.combine(N.MOVES[code][2], dt.time(11))):
                    continue
                loc = t.astimezone(MAD)
                after_fw = t >= fw
                warm = (loc.weekday() == 6 and loc.hour in (3, 4)) or \
                       (town in storm_towns and storm1 <= t < storm1 + dt.timedelta(hours=2)) or \
                       (code != N.REPLACED[0] and fw <= t < fw + dt.timedelta(hours=2)) or \
                       (code in N.MOVES and utc_of_local(dt.datetime.combine(N.MOVES[code][2], dt.time(11))) <= t <
                        utc_of_local(dt.datetime.combine(N.MOVES[code][2], dt.time(13))))
                humid = after_fw and self.rh[k] + rh_off > 88
                if k in faults:
                    st = 3 if after_fw else 2
                elif warm:
                    st = 2 if after_fw else 1
                elif humid:
                    st = 1
                else:
                    st = 0
                subs = [0, 30] if half else [0]
                for j, m in enumerate(subs):
                    v = vals[j, k] if half else vals[k]
                    if st in ((1,) if not after_fw else (2,)):
                        v = v * 0.82 - 1.5             # a cold head reads low while it warms up
                    if (st == 2 and not after_fw) or (st == 3 and after_fw):
                        val = ""
                    else:
                        val = "%.1f" % max(v, 0.0)
                    start = t + dt.timedelta(minutes=m)
                    end = start + dt.timedelta(minutes=30 if half else 60)
                    rec = end + dt.timedelta(minutes=lag + rng.uniform(0, 1.5))
                    if cut0 <= start < cut1:
                        keep = dt.timedelta(hours=48 if half else 24)
                        if start < cut1 - keep:
                            continue                     # lost: older than the buffer when the link came back
                        rec = cut1 + dt.timedelta(minutes=rng.uniform(4, 40))
                    out.append((code, iso(stamped(start, episodes)), val, st, iso(rec)))
                    if cut0 - dt.timedelta(hours=3) <= start < cut0:
                        # the buffer replayed the last hours before the drop as well
                        out.append((code, iso(stamped(start, episodes)), val, st,
                                    iso(cut1 + dt.timedelta(minutes=rng.uniform(4, 40)))))
        out += self._spare_rows()
        df = pd.DataFrame(out, columns=["node_id", "reading_start_utc", "o3_ppb", "status", "received_utc"])
        # the centre writes records in the order they arrive
        return df.sort_values(["received_utc", "node_id", "reading_start_utc"], kind="mergesort").reset_index(drop=True)

    def _spare_rows(self):
        """The spare unit at OZ19's site: hourly, firmware 4.2, as OZ19B until the register was moved."""
        code, _, up, renamed = N.REPLACED
        i = N.CODES.index(code)
        rng = np.random.default_rng(3100)
        s = H.node_true(self.true, code)
        k0 = sim.index(utc_of_local(up))
        span = 1.0 + (N.SPAN[code] - 1.0) * np.clip((np.arange(sim.HOURS) - k0) / (H.window()[0] + 670 - k0), 0, None)
        vals = span * s + N.ZERO[code] * 0.3 + rng.standard_normal(sim.HOURS) * P.NODE_NOISE
        out = []
        ren = utc_of_local(renamed)
        up_t = utc_of_local(up)
        episodes = [(up_t, next_weekly(up_t))]
        rh_off = rng.normal(0, 4)
        for k in range(k0, sim.HOURS):
            t = self.t[k]
            loc = t.astimezone(MAD)
            warm = (loc.weekday() == 6 and loc.hour in (3, 4)) or k < k0 + 2
            st = 2 if warm else (1 if self.rh[k] + rh_off > 88 else 0)
            v = vals[k] * (0.82 if warm else 1.0)
            rec = t + dt.timedelta(minutes=60 + rng.uniform(2, 9))
            out.append((N.SPARE_ID if t < ren else code, iso(stamped(t, episodes)), "%.1f" % max(v, 0.0), st, iso(rec)))
        return out

    # -- the regional network --
    def analyser_rows(self, validated):
        """fecha (dd/mm/yyyy), hora (1-24, hour ending, UTC+1), estacion, o3_ugm3, validacion, analizador."""
        r = np.random.default_rng(4000 + (1 if validated else 2))
        lo = sim.index(dt.datetime(2025, 12, 31, 23, tzinfo=P.UTC)) if validated else \
            sim.index(dt.datetime(2027, 11, 30, 23, tzinfo=P.UTC))
        hi = sim.index(dt.datetime(2027, 12, 31, 22, tzinfo=P.UTC)) + 1 if validated else sim.HOURS
        serial = {"ES4101A": "TE49i-1187", "ES4102A": "TE49i-1203", "ES4103A": "TE49i-0921", "ES4104A": "T400-1388"}
        swap = (dt.datetime(2027, 7, 4, 9, tzinfo=P.UTC), dt.datetime(2027, 7, 17, 12, tzinfo=P.UTC))
        rows = []
        for a, (code, _, _, _) in enumerate(P.ANALYSERS):
            noise = r.normal(0, 1.1, sim.HOURS)
            gaps = set()
            for _ in range(5):
                g = int(r.integers(lo, hi - 30))
                gaps.update(range(g, g + int(r.integers(3, 30))))
            for k in range(lo, hi):
                t = self.t[k]
                lab = (t + dt.timedelta(hours=1)).astimezone(CET)      # hour ending, UTC+1
                if lab.hour == 0:
                    fecha, hora = (lab - dt.timedelta(days=1)).strftime("%d/%m/%Y"), 24
                else:
                    fecha, hora = lab.strftime("%d/%m/%Y"), lab.hour
                ug = self.true[a, k] * P.PPB_TO_UG + noise[k]
                check = t.astimezone(CET).weekday() == 1 and t.astimezone(CET).hour == 11
                lamp = code == "ES4104A" and dt.datetime(2027, 9, 21, 10, tzinfo=P.UTC) <= t < dt.datetime(2027, 9, 21, 16, tzinfo=P.UTC)
                ser = serial[code]
                if code == "ES4103A" and t >= swap[0]:
                    ser = "TE49i-1342"
                if k in gaps:
                    rows.append((fecha, hora, code, "" if not validated else "", "N", ser))
                elif check or lamp:
                    val = "%d" % round(r.uniform(181, 204) if check else ug * 1.6) if validated else ""
                    rows.append((fecha, hora, code, val, "N", ser))
                else:
                    rows.append((fecha, hora, code, "%d" % round(ug), "V" if validated else "P", ser))
                if validated and code == "ES4103A" and swap[0] <= t < swap[1]:
                    old = ug * 0.86 + r.normal(0, 1.0)           # the old analyser had drifted about 14 per cent low
                    rows.append((fecha, hora, code, "%d" % round(old), "V", "TE49i-0921"))
        return pd.DataFrame(rows, columns=["fecha", "hora", "estacion", "o3_ugm3", "validacion", "analizador"])

    def register(self):
        rows = []
        r = np.random.default_rng(55)
        for i, (code, town, x, y) in enumerate(N.NODES):
            if code in N.MOVES:
                x, y = N.MOVES[code][0], N.MOVES[code][1]
            lat = P.LAT0 + y / 111.0
            lon = P.LON0 + x / (111.0 * math.cos(math.radians(P.LAT0)))
            site = N.SITE_TYPES[int(r.integers(0, len(N.SITE_TYPES)))]
            alt = N.ALT[town] + int(r.integers(-14, 15))
            stem = unicodedata.normalize("NFKD", town[:3]).encode("ascii", "ignore").decode().upper()
            rows.append((code, town, "%s-%02d" % (stem, i + 1), site, round(lat, 5), round(lon, 5), alt,
                         N.install_date(i).isoformat(), "OZN-B" if code in N.MODEL_B else "OZN-A",
                         "H%05d" % int(r.integers(40100, 49900))))
        return pd.DataFrame(rows, columns=["node_id", "municipality", "site_code", "mounting", "lat", "lon",
                                           "altitude_m", "installed", "model", "head_serial"])
