"""task270 calculations from the shipped files only: the cover replay (the golden reads each free engine where the
tracking export last placed it), the ladder's rungs, the licensed family's members, and the asks.

    python3 calc.py <target>"""
from __future__ import annotations

import csv
import datetime as dt
import os
import sys

import numpy as np
import openpyxl
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K       # noqa: E402

M = K.MINUTES
T0 = K.T0


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        r = csv.reader(fh)
        head = next(r)
        cols = {h: [] for h in head}
        for row in r:
            for h, v in zip(head, row):
                cols[h].append(v)
    return cols


def sheet(path, name):
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    return rows[0], rows[1:]


def secs_utc(texts):
    a = np.array(texts, dtype="datetime64[s]")
    return (a - np.datetime64("2026-01-01T00:00:00")).astype(np.int64)


def offset_to_utc_secs(texts):
    """Local clock times written with their UTC offset (2026-07-14T13:05:12+01:00) to seconds from 00:00 UTC on
    1 January 2026."""
    base = np.array([x[:19] for x in texts], dtype="datetime64[s]")
    off = np.array([(1 if x[19] == "+" else -1) * (int(x[20:22]) * 3600 + int(x[23:25]) * 60) for x in texts])
    return (base - np.datetime64("2026-01-01T00:00:00")).astype(np.int64) - off


class Pack:
    def __init__(self, target):
        self.target = target
        J = lambda f: os.path.join(target, f)
        nd = read_csv(J(K.F_NODES))
        self.node_ids = nd["node_id"]
        self.nxy = np.c_[np.array(nd["easting"], float), np.array(nd["northing"], float)]
        nid = {n: i for i, n in enumerate(self.node_ids)}
        lk = read_csv(J(K.F_LINKS))
        a = np.array([nid[x] for x in lk["from_node"]]); b = np.array([nid[x] for x in lk["to_node"]])
        w = np.array(lk["drive_time_s"], float)
        one = np.array([x == "Y" for x in lk["one_way"]])
        self.N = len(self.node_ids)
        G = csr_matrix((np.r_[w, w[~one]], (np.r_[a, b[~one]], np.r_[b, a[~one]])), shape=(self.N, self.N))
        self.D = dijkstra(G, directed=True).astype(np.float32)
        self.ntree = cKDTree(self.nxy)
        # homes: residential addresses, the district of their output area
        ad = read_csv(J(K.F_ADDR))
        cls = np.array(ad["class_code"])
        res = np.char.startswith(cls.astype(str), "RD")
        _, rows = sheet(J(K.F_OALOOK), "OA21 to LAD")
        oa_d = {r[0]: r[2] for r in rows}
        self.addr_xy = np.c_[np.array(ad["easting"], float), np.array(ad["northing"], float)]
        self.addr_res = res
        self.addr_oa = np.array(ad["output_area"])
        self.addr_uprn = np.array(ad["uprn"])
        self.addr_dist = np.array([K.DISTRICTS.index(oa_d[o]) for o in self.addr_oa])
        hn = self.ntree.query(self.addr_xy[res])[1]
        hd = self.addr_dist[res]
        self.dnodes = np.unique(hn)
        di = np.full(self.N, -1); di[self.dnodes] = np.arange(len(self.dnodes))
        self.HD = np.zeros((len(self.dnodes), len(K.DISTRICTS)))
        np.add.at(self.HD, (di[hn], hd), 1.0)
        self.homes = self.HD.sum(0)
        # fleet
        _, st = sheet(J(K.F_FLEET), "Stations")
        self.stations = {r[0]: dict(code=r[0], name=r[1], duty=r[2], district=r[3], xy=np.array([r[4], r[5]], float))
                         for r in st}
        for s in self.stations.values():
            s["node"] = int(self.ntree.query(s["xy"])[1])
        _, ap = sheet(J(K.F_FLEET), "Appliances")
        self.calls = [r[0] for r in ap]
        self.crew = np.array([r[4] for r in ap])
        self.station_of = [r[2] for r in ap]
        self.home = np.array([self.stations[c]["node"] for c in self.station_of])
        self.turn = np.where(self.crew == "Wholetime", K.TURNOUT["Wholetime"] * 60, K.TURNOUT["On-call"] * 60)
        self.nE = len(self.calls)
        self._status()
        self._tracking()

    # ---------------------------------------------------------------------------------------------- status
    def _log(self):
        s = read_csv(os.path.join(self.target, K.F_LOG))
        self.log = s
        return s

    def _status(self):
        s = self._log()
        ev = np.array(s["event"])
        st = ev == "Status"
        t = secs_utc(np.array(s["time_utc"])[st])
        cs = np.array(s["call_sign"])[st]
        code = np.array(s["status_code"])[st]
        reason = np.array(s["off_run_reason"])[st]
        mins = np.arange(M) * 60
        self.free = np.zeros((M, self.nE), bool)
        self.status_code = np.zeros((M, self.nE), np.int8)
        self.st_rows = {}
        for e, c in enumerate(self.calls):
            m = cs == c
            tt, cc, rr = t[m], code[m], reason[m]
            o = np.argsort(tt, kind="stable")
            tt, cc, rr = tt[o], cc[o], rr[o]
            self.st_rows[e] = (tt, cc, rr)
            idx = np.searchsorted(tt, mins, side="right") - 1
            ok = idx >= 0
            cur = np.where(ok, cc[np.clip(idx, 0, None)], "")
            self.free[:, e] = cur == "1"
            self.status_code[:, e] = np.where(ok, cc[np.clip(idx, 0, None)].astype(int), 0)

    def _tracking(self, clock_shift=0):
        s = self.log
        ev = np.array(s["event"])
        m = ev != "Status"
        cs = np.array(s["call_sign"])[m]
        idx = {c: i for i, c in enumerate(self.calls)}
        e_of = np.array([idx[x] for x in cs])
        t = secs_utc(np.array(s["time_utc"])[m]) + clock_shift
        xy = np.c_[np.array(s["easting"], dtype=object)[m].astype(float), np.array(s["northing"], dtype=object)[m].astype(float)]
        node = self.ntree.query(xy)[1]
        self.trk = dict(e=e_of, t=t, ev=ev[m], xy=xy, node=node)
        return self.trk

    def positions(self, mode="hold", trk=None):
        """Node each engine stood at at each minute's start: at its station unless the tracking export has it out of
        base, then where the last report put it (mode hold), the nearest report in time (nearest), or along the line
        between the reports either side (interp)."""
        trk = self.trk if trk is None else trk
        mins = np.arange(M) * 60
        pos = np.tile(self.home, (M, 1)).astype(np.int32)
        for e in range(self.nE):
            m = trk["e"] == e
            if not m.any():
                continue
            tt, ev, nd, xy = trk["t"][m], trk["ev"][m], trk["node"][m], trk["xy"][m]
            o = np.argsort(tt, kind="stable")
            tt, ev, nd, xy = tt[o], ev[o], nd[o], xy[o]
            idx = np.searchsorted(tt, mins, side="right") - 1
            ok = idx >= 0
            ii = np.clip(idx, 0, None)
            out_ = ok & (ev[ii] != "Arrived base")
            if mode == "hold":
                pos[out_, e] = nd[ii[out_]]
            elif mode == "nearest":
                j2 = np.clip(ii + 1, 0, len(tt) - 1)
                closer = (tt[j2] - mins) < (mins - tt[ii])
                pick = np.where(closer & (ev[j2] != "Left base"), j2, ii)
                pos[out_, e] = nd[pick[out_]]
            elif mode == "interp":
                j2 = np.clip(ii + 1, 0, len(tt) - 1)
                span = np.maximum(tt[j2] - tt[ii], 1)
                fr = np.clip((mins - tt[ii]) / span, 0, 1)[:, None]
                p = xy[ii] + fr * (xy[j2] - xy[ii])
                sel = np.where(out_)[0]
                pos[sel, e] = self.ntree.query(p[sel])[1]
        return pos

    # ---------------------------------------------------------------------------------------------- cover
    def reach(self, turn_s):
        return (self.D[:, self.dnodes] + turn_s) <= K.STANDARD_MIN * 60.0

    def cover(self, freem, posm, turn=None, step=1):
        turn = self.turn if turn is None else turn
        R = {ts: self.reach(ts) for ts in np.unique(turn)}
        S = np.where(freem[::step], posm[::step], -1).astype(np.int32)
        u, cnt = np.unique(S, axis=0, return_counts=True)
        out = np.zeros(len(K.DISTRICTS))
        for s0 in range(0, len(u), 3000):
            blk = u[s0:s0 + 3000]
            cov = np.zeros((len(blk), len(self.dnodes)), bool)
            for e in range(self.nE):
                p = blk[:, e]; m = p >= 0
                if m.any():
                    cov[m] |= R[turn[e]][p[m]]
            out += (cnt[s0:s0 + 3000, None] * (cov.astype(np.float32) @ self.HD)).sum(0)
        return out / (M / step) / self.homes * 100.0


def golden(P):
    pos = P.positions("hold")
    return P.cover(P.free, pos), pos


def ladder(P, pos=None):
    if pos is None:
        pos = P.positions("hold")
    homeM = np.broadcast_to(P.home, (M, P.nE))
    snodes = np.unique([s["node"] for s in P.stations.values()])
    at_home = pos == homeM
    at_station = np.isin(pos, snodes)
    res = {}
    res["R0 static"] = P.cover(np.ones_like(P.free), homeM)
    a = P.free.mean(0)
    r1 = []
    for d in range(len(K.DISTRICTS)):
        m = P.HD[:, d] > 0
        pc = np.ones(m.sum())
        for e in range(P.nE):
            reach = (P.D[P.home[e], P.dnodes[m]] + P.turn[e]) <= 600.0
            pc *= np.where(reach, 1 - a[e], 1.0)
        r1.append(((1 - pc) * P.HD[m, d]).sum() / P.homes[d] * 100)
    res["R1 independent"] = np.array(r1)
    res["R2 station replay"] = P.cover(P.free, homeM)
    res["R2b zero when away"] = P.cover(P.free & at_home, homeM)
    res["P1 standby credited"] = P.cover(P.free, np.where(at_station, pos, homeM))
    res["P3 stations only"] = P.cover(P.free & at_station, pos)
    t = cKDTree(P.nxy[snodes])
    snap = snodes[t.query(P.nxy[pos.ravel()])[1]].reshape(pos.shape)
    res["P4 nearest station"] = P.cover(P.free, snap)
    res["R3 positions"] = P.cover(P.free, pos)
    return res


def named(sh):
    return [K.DISTRICTS[i] for i in np.where(np.asarray(sh) < K.LINE)[0]]


def main(target):
    P = Pack(target)
    res = ladder(P)
    print("%-22s" % "district", " ".join("%7s" % d[:7] for d in K.DISTRICTS), " homes", P.homes.astype(int).tolist())
    for k, v in res.items():
        print("%-22s" % k, " ".join("%7.3f" % x for x in v), " named:", ", ".join(named(v)))


if __name__ == "__main__":
    main(sys.argv[1])


# ------------------------------------------------------------------------------------------------- ask A
RURAL_STATIONS = ["61", "62", "63", "64", "71", "72", "73", "74"]
OIC_ROLES = ("Crew Commander", "Watch Commander", "Station Commander")


def local_min(texts):
    """Local clock text (YYYY-MM-DD HH:MM:SS) to UTC minutes from 00:00 UTC on 1 January 2026 (no booking time falls
    in the hour the clocks go back)."""
    t = secs_utc(texts) // 60
    a, b = K.bst_minutes()
    return np.where((t >= a + 60) & (t < b + 60), t - 60, t)


def bookings(target, how="latest"):
    """Each firefighter's booked minutes. how: latest (a booking replaces the earlier ones of the same firefighter it
    overlaps), union (every booking counts), first (an earlier booking stands against a later one)."""
    bk = read_csv(os.path.join(target, K.F_BOOK))
    f = local_min(bk["available_from"]); t = local_min(bk["available_to"]); en = local_min(bk["entered"])
    staff = np.array(bk["staff_number"]); st = np.array(bk["station_code"])
    out = {}
    for s in np.unique(staff):
        idx = np.where(staff == s)[0]
        if how == "union":
            keep = idx
        else:
            o = idx[np.argsort(en[idx] if how == "latest" else -en[idx], kind="stable")]
            keep = []
            for i in o[::-1]:                       # newest first (latest) / oldest first (first)
                if all(t[i] <= f[j] or f[i] >= t[j] for j in keep):
                    keep.append(i)
            keep = np.array(sorted(keep))
        out[s] = (st[keep[0]] if len(keep) else st[idx[0]], f[keep], t[keep])
    return out


def crew_attrs(target):
    _, crew = sheet(os.path.join(target, K.F_CREW), "Crew")
    _, ch = sheet(os.path.join(target, K.F_CREW), "Role changes")
    role_now = {r[0]: r[2] for r in crew}
    hist = {}
    for s, stc, role, eff in ch:
        hist.setdefault(s, []).append((str(eff)[:10], role))
    return role_now, hist


def ask_a(target, P=None, how="latest", roles="dated", sample="minute"):
    """Per rural on-call station: minutes off the run (status 8) while four or more of its firefighters were booked, and
    of those the minutes with no crew commander or above booked."""
    if P is None:
        P = Pack(target)
    bk = bookings(target, how)
    role_now, hist = crew_attrs(target)
    mins = np.arange(M)
    out = {}
    for sc in RURAL_STATIONS:
        e = P.calls.index(sc + "P1")
        n = np.zeros(M, np.int16)
        oic = np.zeros(M, np.int16)
        for s, (st, f, t) in bk.items():
            if st != sc:
                continue
            on = np.zeros(M, bool)
            for a, b in zip(f, t):
                on[max(0, a):min(M, b)] = True
            n += on
            # role by date: the role changes sheet dates a promotion; before it, the earlier role
            if roles == "dated" and s in hist:
                d0, rl = sorted(hist[s])[0]
                m0 = int((np.datetime64(d0) - np.datetime64("2026-01-01")).astype(int)) * 1440
                was_oic = role_now[s] in OIC_ROLES and False
                oic_mask = np.zeros(M, bool)
                if rl in OIC_ROLES:
                    oic_mask[m0:] = True
                oic += on & oic_mask
            elif role_now[s] in OIC_ROLES:
                oic += on
        off = P.status_code[:, e] == 8
        x = off & (n >= 4)
        y = x & (oic == 0)
        out[sc] = (int(x.sum()), int(y.sum()))           # minutes
    return out


def hm(minutes):
    h, m = divmod(int(minutes), 60)
    return "%d %s %d %s" % (h, "hour" if h == 1 else "hours", m, "minute" if m == 1 else "minutes")


# ------------------------------------------------------------------------------------------------- ask C
def ask_c(target, P=None, dedupe="overlap", classify="both"):
    """Per district: false alarms caused by fire alarm apparatus at non-domestic premises (commercial addresses),
    2022 to 2026, each alarm once, and per 100 non-domestic premises."""
    if P is None:
        P = Pack(target)
    inc = read_csv(os.path.join(target, K.F_INC))
    code = np.array(inc["classification"])
    afa = (code == "A01") | (code == "FAA")
    cls_of = dict(zip(P.addr_uprn, np.where(P.addr_res, "R", "C")))
    dist_of = dict(zip(P.addr_uprn, P.addr_dist))
    uprn = np.array(inc["uprn"])
    nondom = np.array([cls_of.get(u, "") == "C" for u in uprn])
    sel = np.where(afa & nondom)[0]
    call = np.array(inc["call_time"], dtype="datetime64[s]")
    closed = np.array(inc["closed_time"], dtype="datetime64[s]")
    keep = np.ones(len(sel), bool)
    if dedupe == "overlap":
        o = np.lexsort((call[sel], uprn[sel]))
        last_closed = {}
        for k in o:
            i = sel[k]
            u = uprn[i]
            if u in last_closed and call[i] <= last_closed[u]:
                keep[k] = False
                last_closed[u] = max(last_closed[u], closed[i])
            else:
                last_closed[u] = closed[i]
    elif dedupe == "day":
        seen = set()
        for k in np.argsort(call[sel], kind="stable"):
            i = sel[k]
            key = (uprn[i], str(call[i])[:10])
            if key in seen:
                keep[k] = False
            seen.add(key)
    alarms = sel[keep]
    prem = np.bincount(P.addr_dist[~P.addr_res], minlength=len(K.DISTRICTS))
    out = {}
    for di, d in enumerate(K.DISTRICTS):
        n = int(sum(1 for i in alarms if dist_of[uprn[i]] == di))
        out[d] = (n, n / prem[di] * 100.0)
    return out


def crew_rule(target, P, how="latest"):
    """Per rural on-call station: minutes the crewing rule (four booked, a crew or watch commander, an LGV driver, two
    BA wearers) is met on the bookings read `how`, and minutes the log shows the engine off the run with reason Crew."""
    bk = bookings(target, how)
    _, crew = sheet(os.path.join(target, K.F_CREW), "Crew")
    _, ch = sheet(os.path.join(target, K.F_CREW), "Role changes")
    ba = {r[0]: r[3] == "Yes" for r in crew}
    drv = {r[0]: (str(r[4])[:10] if r[4] else None) for r in crew}
    role_now = {r[0]: r[2] for r in crew}
    promo = {r[0]: str(r[3])[:10] for r in ch}
    day0 = np.datetime64("2026-01-01")
    out = {}
    for sc in RURAL_STATIONS:
        e = P.calls.index(sc + "P1")
        n = np.zeros(M, np.int16); oic = np.zeros(M, np.int16); dv = np.zeros(M, np.int16); b = np.zeros(M, np.int16)
        for s, (st, f, t) in bk.items():
            if st != sc:
                continue
            on = np.zeros(M, bool)
            for a, z in zip(f, t):
                on[max(0, a):min(M, z)] = True
            n += on
            if ba[s]:
                b += on
            if drv[s]:
                m0 = max(0, int((np.datetime64(drv[s]) - day0).astype(int)) * 1440)
                dm = np.zeros(M, bool); dm[m0:] = True
                dv += on & dm
            om = np.zeros(M, bool)
            if s in promo:
                om[max(0, int((np.datetime64(promo[s]) - day0).astype(int)) * 1440):] = True
            elif role_now[s] in OIC_ROLES:
                om[:] = True
            oic += on & om
        met = (n >= 4) & (oic >= 1) & (dv >= 1) & (b >= 2)
        tt, cc, rr = P.st_rows[e]
        mins = np.arange(M) * 60
        idx = np.clip(np.searchsorted(tt, mins, side="right") - 1, 0, None)
        crew_off = (cc[idx] == "8") & (rr[idx] == "Crew")
        avail = cc[idx] == "1"
        out[sc] = dict(met=met, crew_off=crew_off, avail=avail)
    return out
