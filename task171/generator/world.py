"""The clean truth for task171: the Marrowfield Turnpike's toll-by-mail book from the night the cash booths first
closed (3 March 2025) to the records' date (31 October 2026), and the commercial MarrowPass postings of January to
September 2026. Everything the pack prints is cut from what this module returns; the mess lives in pack.py.

Truth, in brief:
- cash users seen overnight in the booth lanes (invoice type TBM) and express-lane violators (type VIO), each plate
  with a home-state or out-of-state registration;
- an invoice per plate, type and crossing month, issued on the 8th of the next month (next weekday);
- unpaid at 60 days, a home-state plate goes on a registration hold and pays when it renews its two-year
  registration (renewals fall in the 45 days before expiry, and a hold placed after the owner has renewed waits for
  the next expiry); an out-of-state plate, or a home-state plate the MVD has no record of, goes to the agency at 90
  days, which collects or returns it 360 days after the invoice;
- the violation agency works a plate's whole account: when it collects, one remittance names the oldest invoice it
  holds for the plate and covers every invoice it holds for that plate;
- an express-lane vehicle that straddles the two lanes is read twice; a truck whose classifier splits it bills its
  trailer (or a towed car) as a second vehicle with no tag, a phantom violation."""
from __future__ import annotations

import calendar
import datetime as dt

import numpy as np
import pandas as pd

import common as C

D = dt.date
TD = dt.timedelta


def bday(d):
    while d.weekday() >= 5:
        d += TD(days=1)
    return d


def issue_date(y, m):
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    return bday(D(ny, nm, 8))


def month_end(y, m):
    return D(y, m, calendar.monthrange(y, m)[1])


def next_expiry(after, m, parity):
    for y in range(after.year - 1, after.year + 5):
        if y % 2 == parity:
            e = month_end(y, m)
            if e > after:
                return e
    raise ValueError


class Plates:
    """Registered plates: string, state, owner kind, behaviour."""
    LET = "ABCDEFGHJKLMNPRSTUVWXYZ"

    def __init__(self, rng):
        self.rng = rng
        self.used = set()

    def make(self, state):
        r = self.rng
        while True:
            L = "".join(r.choice(list(self.LET), 3))
            n = int(r.integers(0, 10000))
            if state == C.HOME:
                s = "%s%04d" % (L, n) if r.random() < 0.82 else "%04d%s" % (n, L[:2])
            elif state in ("ON", "QC"):
                s = "%s%s %03d" % (L, r.choice(list(self.LET)), n % 1000)
            elif state in ("PA", "NY", "NC"):
                s = "%s%04d" % (L, n)
            elif state in ("OH", "IN", "IL"):
                s = "%s%s%03d" % (L[:2], r.choice(list("0123456789")), n % 1000)
            else:
                s = "%s%s%02d" % (L, r.choice(list("0123456789")), n % 100)
            if (s, state) not in self.used:
                self.used.add((s, state))
                return s


def draw_states(rng, n, home_share):
    home = rng.random(n) < home_share
    st = np.where(home, C.HOME, rng.choice(C.OUT_STATES, n, p=np.array(C.OUT_P) / sum(C.OUT_P)))
    return st


def build(seed=C.SEED):
    rng = np.random.default_rng(seed)
    PL = Plates(rng)
    days = pd.date_range(C.CLOSE_START, C.LAST_CROSS, freq="D")
    nd = len(days)
    plates = []

    # ---------------------------------------------------------------- the people
    def population(kind, n, home_share, chronic_share):
        st = draw_states(rng, n, home_share)
        chronic = rng.random(n) < chronic_share
        home = st == C.HOME
        # crossings per 30 days in the channel, and the span of days the plate is around
        if kind == "TBM":
            rate = np.where(home, rng.lognormal(np.log(1.0), 1.0, n), rng.lognormal(np.log(0.9), 0.8, n))
            span = np.where(home, rng.integers(60, nd + 1, n), rng.integers(20, 260, n))
        else:
            rate = np.where(home, rng.lognormal(np.log(0.65), 1.0, n), rng.lognormal(np.log(0.5), 0.9, n))
            rate = np.where(chronic, rate * 3.0, rate)
            span = np.where(home, rng.integers(20, nd + 1, n), rng.integers(1, 90, n))
        start = np.array([int(rng.integers(-s + 1, nd)) for s in span])
        ax = rng.choice([2, 3, 4, 5, 6], n, p=[0.90, 0.03, 0.01, 0.05, 0.01] if kind == "TBM" else [0.93, 0.03, 0.01, 0.025, 0.005])
        match = np.where(home, rng.random(n) < 0.965, False)
        exp_m = rng.integers(1, 13, n); exp_par = rng.integers(0, 2, n)
        for i in range(n):
            plates.append(dict(plate=PL.make(st[i]), state=st[i], kind=kind, chronic=bool(chronic[i]), rate=float(rate[i]),
                               start=int(start[i]), span=int(span[i]), axles=int(ax[i]), match=bool(match[i]),
                               exp_m=int(exp_m[i]), exp_par=int(exp_par[i]), phantom=False))

    population("TBM", 27000, 0.56, 0.0)
    population("VIO", 30500, 0.58, 0.12)
    P = pd.DataFrame(plates)

    # ---------------------------------------------------------------- the crossings
    lo = np.maximum(P.start.values, 0); hi = np.minimum(nd, P.start.values + P.span.values)
    hi = np.maximum(hi, lo)
    n = rng.poisson(P.rate.values * (hi - lo) / 30.4)
    pi = np.repeat(np.arange(len(P)), n)
    di = (lo[pi] + np.floor(rng.random(len(pi)) * (hi[pi] - lo[pi]))).astype(int)
    tbm = (P.kind.values[pi] == "TBM")
    base = days.values[di]
    sec_tbm = 23 * 3600 + rng.integers(0, 6 * 3600, len(pi))
    sec_vio = rng.choice(24, len(pi), p=HOUR_W) * 3600 + rng.integers(0, 3600, len(pi))
    ms = np.where(tbm, sec_tbm, sec_vio) * 1000 + rng.integers(0, 1000, len(pi))
    t0 = (pd.to_datetime(base) + pd.to_timedelta(ms, "ms")).values.astype("datetime64[ns]")
    X = explode(rng, pi, t0, tbm, P.axles.values[pi])
    # an overnight crossing outside 11 p.m. to 5 a.m. met an open booth and paid cash: not billed
    hh = X.ts.dt.hour
    X = X[~(X.lane.isin(C.BOOTH_LANES)) | (hh >= 23) | (hh < 5)]
    X = X[X.ts.dt.date <= C.LAST_CROSS].reset_index(drop=True)

    # commercial MarrowPass postings, 2026, ordinary violators following trucks closely, and the phantoms
    T, phantom_rows, P = commercial(rng, P, PL, X)
    # straddles: an express-lane vehicle read in both lanes a fraction of a second apart
    X["gid"] = np.arange(len(X))
    v = X[(X.lane.isin(C.ETC_LANES))].sample(frac=0.011, random_state=int(rng.integers(1 << 30)))
    st_ = v.copy()
    st_["lane"] = np.where(st_.lane == "E1", "E2", "E1")
    st_["ts"] = st_.ts + pd.to_timedelta(rng.integers(40, 380, len(st_)), "ms")
    st_["origin"] = "straddle"
    fol = phantom_rows[phantom_rows.origin == "follower"].assign(origin="real")
    fol["gid"] = np.arange(len(fol)) + 10_000_000
    X = pd.concat([X, st_, fol], ignore_index=True)
    X = headway(rng, X, T)
    X = pd.concat([X, phantom_rows[phantom_rows.origin == "phantom"]], ignore_index=True)
    X = X.sort_values(["ts", "plaza", "lane"], kind="mergesort").reset_index(drop=True)
    X["kind"] = P.kind.values[X.pi.values]
    yr = X.ts.dt.year.values
    X["toll"] = [round(C.CASH[y][p] * C.MULT[a], 2) for y, p, a in zip(yr, X.plaza.values, X.axles.values)]
    X["ym"] = list(zip(X.ts.dt.year, X.ts.dt.month))

    # ---------------------------------------------------------------- invoices
    inv = X.groupby(["pi", "kind", "ym"], sort=True).agg(toll=("toll", "sum"), n=("toll", "size")).reset_index()
    inv["issue"] = [issue_date(y, m) for (y, m) in inv.ym]
    inv = inv.sort_values(["issue", "pi"], kind="mergesort").reset_index(drop=True)
    inv["inv_no"] = ["%s%s%06d" % ("T" if k == "TBM" else "V", d.strftime("%y%m"), j)
                     for j, (k, d) in enumerate(zip(inv.kind, inv.issue))]
    # owed toll: a straddle's second read and a phantom owe nothing
    owed = X[X.origin == "real"].groupby(["pi", "kind", "ym"]).toll.sum()
    inv["owed"] = [owed.get((a, b, c), 0.0) for a, b, c in zip(inv.pi, inv.kind, inv.ym)]
    inv["fee"] = np.where(inv.kind == "TBM", C.INVOICE_FEE, C.VIOLATION_FEE)

    pay, holds, agy, settle, late = collect(rng, P, inv)
    inv["late"] = late
    return dict(P=P, X=X, inv=inv, pay=pay, holds=holds, agy=agy, settle=settle, T=T, days=days)


HOUR_W = np.array([.8, .5, .4, .4, .6, 1.4, 3.6, 6.2, 6.4, 5.0, 4.6, 4.8, 5.0, 5.0, 5.3, 6.0, 6.9, 7.1, 5.9, 4.4, 3.4, 2.6, 1.9, 1.3])
HOUR_W = HOUR_W / HOUR_W.sum()


ORDER = {"SB": ["VEL", "BRN", "OST"], "NB": ["OST", "BRN", "VEL"]}


def explode(rng, owner, t0, booth, axles):
    """Trips to plaza crossings: a trip runs one direction through one to three consecutive plazas at its own speed;
    a plate's trips never overlap (a later one that would is dropped)."""
    n = len(owner)
    order = np.lexsort((t0, owner))
    owner, t0, booth, axles = owner[order], t0[order], booth[order], axles[order]
    dirn = np.array(C.DIRS)[rng.integers(0, 2, n)]
    k = rng.choice([1, 2, 3], n, p=[0.50, 0.32, 0.18])
    s0 = (rng.random(n) * (4 - k)).astype(int)
    speed = rng.uniform(52, 72, n)
    span_s = np.array([abs(C.MILEPOST[ORDER[d][a + kk - 1]] - C.MILEPOST[ORDER[d][a]]) for d, a, kk in zip(dirn, s0, k)]) / speed * 3600
    end = t0 + (span_s * 1e9).astype("timedelta64[ns]")
    keep = np.ones(n, bool)
    last_o, last_end = -1, None
    for i in range(n):
        if owner[i] == last_o and t0[i] < last_end + np.timedelta64(40, "m"):
            keep[i] = False
            continue
        last_o, last_end = owner[i], end[i]
    rows = []
    for j in range(3):
        sel = keep & (k > j)
        pz = np.array([ORDER[d][a + j] for d, a in zip(dirn[sel], s0[sel])])
        start = np.array([ORDER[d][a] for d, a in zip(dirn[sel], s0[sel])])
        dist = np.abs(np.array([C.MILEPOST[p] for p in pz]) - np.array([C.MILEPOST[p] for p in start]))
        ts = t0[sel] + (dist / speed[sel] * 3600 * 1e9).astype("timedelta64[ns]")
        lane = np.where(booth[sel], np.array(C.BOOTH_LANES)[rng.integers(0, 4, sel.sum())], np.array(C.ETC_LANES)[rng.integers(0, 2, sel.sum())])
        rows.append(pd.DataFrame(dict(pi=owner[sel], ts=ts, plaza=pz, dir=dirn[sel], lane=lane, axles=axles[sel], origin="real")))
    X = pd.concat(rows, ignore_index=True)
    X["ts"] = X.ts.astype("datetime64[ns]")
    return X.sort_values(["ts", "pi"], kind="mergesort").reset_index(drop=True)


def headway(rng, X, T):
    """Two vehicles cannot pass one express lane less than 0.9 s apart: move any ordinary read (with its straddle
    partner) that sits that close to a commercial posting to 1.0 to 1.6 s from it."""
    key = ["plaza", "dir", "lane"]
    t = T[key + ["ts"]].rename(columns={"ts": "tts"}).sort_values("tts")
    for _ in range(4):
        e = X[X.lane.isin(C.ETC_LANES) & (X.ts >= pd.Timestamp("2025-12-31"))].reset_index().sort_values("ts")
        b = pd.merge_asof(e, t, left_on="ts", right_on="tts", by=key, direction="backward")
        f = pd.merge_asof(e, t, left_on="ts", right_on="tts", by=key, direction="forward")
        gb = (b.ts - b.tts).dt.total_seconds(); gf = (f.tts - f.ts).dt.total_seconds()
        badb = b[gb < 0.9]; badf = f[gf < 0.9]
        if not len(badb) and not len(badf):
            break
        shift = {}
        for r, gsec in zip(badb.itertuples(), gb[gb < 0.9]):
            shift[X.at[r.index, "gid"]] = 1.0 + rng.random() * 0.6 - gsec
        for r, gsec in zip(badf.itertuples(), gf[gf < 0.9]):
            shift.setdefault(X.at[r.index, "gid"], -(1.0 + rng.random() * 0.6 - gsec))
        sh = X.gid.map(shift)
        m = sh.notna()
        X.loc[m, "ts"] = X.loc[m, "ts"] + pd.to_timedelta((sh[m] * 1000).round().astype(int), "ms")
    # whatever still sits too close after the passes is dropped with its straddle partner
    e = X[X.lane.isin(C.ETC_LANES) & (X.ts >= pd.Timestamp("2025-12-31"))].reset_index().sort_values("ts")
    b = pd.merge_asof(e, t, left_on="ts", right_on="tts", by=key, direction="backward")
    f = pd.merge_asof(e, t, left_on="ts", right_on="tts", by=key, direction="forward")
    gone = set(X.loc[b["index"][(b.ts - b.tts).dt.total_seconds() < 0.9].values, "gid"]) | set(X.loc[f["index"][(f.tts - f.ts).dt.total_seconds() < 0.9].values, "gid"])
    return X[~X.gid.isin(gone)].reset_index(drop=True)


def commercial(rng, P, PL, X):
    """MarrowPass commercial postings in the express lanes, January to September 2026, with the classifier splits."""
    days = pd.date_range("2026-01-01", "2026-09-30", freq="D")
    fleet = 2600
    f_ax = rng.choice([3, 4, 5, 6], fleet, p=[0.18, 0.10, 0.62, 0.10])
    f_tow = rng.random(fleet) < 0.035
    f_ax = np.where(f_tow, 3, f_ax)
    f_rate = rng.lognormal(np.log(0.32), 0.7, fleet)
    f_state = draw_states(rng, fleet, 0.55)
    f_plate = [PL.make(s) for s in f_state]
    acct = rng.integers(40_000, 41_200, fleet)
    n = rng.poisson(f_rate * len(days))
    fi = np.repeat(np.arange(fleet), n)
    di = rng.integers(0, len(days), len(fi))
    ms = rng.choice(24, len(fi), p=HOUR_W) * 3_600_000 + rng.integers(0, 3_600_000, len(fi))
    t0 = (pd.to_datetime(days.values[di]) + pd.to_timedelta(ms, "ms")).values.astype("datetime64[ns]")
    Tx = explode(rng, fi, t0, np.zeros(len(fi), bool), f_ax[fi])
    T = pd.DataFrame(dict(fi=Tx.pi.values, ts=Tx.ts.values, plaza=Tx.plaza.values, dir=Tx.dir.values, lane=Tx.lane.values,
                          axles_true=Tx.axles.values))
    T = T[T.ts < pd.Timestamp("2026-10-01")]
    # two trucks cannot pass one lane less than 1.5 s apart: push the later one back
    T = T.sort_values(["plaza", "dir", "lane", "ts"], kind="mergesort").reset_index(drop=True)
    for _ in range(6):
        same = T.plaza.eq(T.plaza.shift()) & T.dir.eq(T.dir.shift()) & T.lane.eq(T.lane.shift())
        gap = (T.ts - T.ts.shift()).dt.total_seconds()
        bad = same & (gap < 1.5)
        if not bad.any():
            break
        T.loc[bad, "ts"] = T.ts.shift()[bad] + pd.to_timedelta(rng.integers(1500, 3000, int(bad.sum())), "ms")
        T = T.sort_values(["plaza", "dir", "lane", "ts"], kind="mergesort").reset_index(drop=True)
    T = T.sort_values(["ts", "fi"], kind="mergesort").reset_index(drop=True)
    T["plate"] = [f_plate[i] for i in T.fi]; T["state"] = [f_state[i] for i in T.fi]; T["account"] = acct[T.fi.values]
    T["tow"] = f_tow[T.fi.values]
    # classifier splits: a five- or six-axle combination counted as a three-axle tractor and a separate two- or
    # three-axle unit; a tow truck's towed car counted as a second vehicle
    split = ((T.axles_true >= 5) & (rng.random(len(T)) < 0.0042)) | (T.tow & (rng.random(len(T)) < 0.08))
    T["axles"] = np.where(split & ~T.tow, 3, T.axles_true)
    T["split"] = split
    # trailers and towed cars: their own plates
    trailers_state = draw_states(rng, 900, 0.30)
    trailer_plates = [PL.make(s) for s in trailers_state]
    new = []
    sp = T[T.split]
    phantom_pi = {}
    base = len(P)
    add = []
    for r in sp.itertuples():
        if r.tow:
            s = draw_states(rng, 1, 0.62)[0]; pl = PL.make(s); ax = 2
        else:
            j = int(rng.integers(0, len(trailer_plates))); pl, s = trailer_plates[j], trailers_state[j]; ax = int(r.axles_true - 3)
        key = (pl, s)
        if key not in phantom_pi:
            phantom_pi[key] = base + len(add)
            add.append(dict(plate=pl, state=s, kind="VIO", chronic=False, rate=0.0, start=0, span=0, axles=ax,
                            match=bool(s == C.HOME and rng.random() < 0.98), exp_m=int(rng.integers(1, 13)),
                            exp_par=int(rng.integers(0, 2)), phantom=True))
        dt_ = pd.Timedelta(milliseconds=int(rng.integers(100, 300)))
        new.append((phantom_pi[key], r.ts + dt_, r.plaza, r.dir, r.lane, ax, "phantom"))
    P = pd.concat([P, pd.DataFrame(add)], ignore_index=True)
    ph = pd.DataFrame(new, columns=["pi", "ts", "plaza", "dir", "lane", "axles", "origin"])
    # ordinary violators a second or two behind a truck in the same lane: occasional drivers without a tag
    tk = T[T.ts >= pd.Timestamp("2026-01-01")].sample(frac=0.012, random_state=int(rng.integers(1 << 30)))
    fol_add, fol_rows = [], []
    for r in tk.itertuples():
        s_ = draw_states(rng, 1, 0.55)[0]
        fol_rows.append((len(P) + len(fol_add), r.ts + pd.Timedelta(milliseconds=int(rng.integers(900, 2400))),
                         r.plaza, r.dir, r.lane, 2, "real"))
        fol_add.append(dict(plate=PL.make(s_), state=s_, kind="VIO", chronic=False, rate=0.0, start=0, span=0, axles=2,
                            match=bool(s_ == C.HOME and rng.random() < 0.965), exp_m=int(rng.integers(1, 13)),
                            exp_par=int(rng.integers(0, 2)), phantom=False))
    P = pd.concat([P, pd.DataFrame(fol_add)], ignore_index=True)
    ph = pd.concat([ph, pd.DataFrame(fol_rows, columns=ph.columns).assign(origin="follower")], ignore_index=True)
    T["class_toll"] = [round(C.CASH[2026][p] * C.MULT[a] * 0.8, 2) for p, a in zip(T.plaza, T.axles)]
    return T, ph, P


def collect(rng, P, inv):
    """The enforcement cycle, invoice by invoice: payments, holds, agency placements, settlements."""
    home = (P.state.values == C.HOME)
    pay, holds, agy = [], [], []
    vio_place = {}
    bal_info = {}
    Pr = list(P.itertuples(index=False))
    late_flag = np.zeros(len(inv))
    for j, r in enumerate(inv.itertuples()):
        p = Pr[r.pi]
        is_home = p.state == C.HOME
        I = r.issue
        billed = r.toll + r.fee
        if p.phantom:
            pe = 0.55
        elif r.kind == "TBM":
            pe = 0.61 if is_home else 0.45
        else:
            pe = (0.07 if p.chronic else 0.55) if is_home else (0.03 if p.chronic else 0.38)
        early = rng.random() < pe
        state = dict(inv=r.inv_no, I=I, toll=r.toll, fee=r.fee, late=0.0, coll=0.0)
        start_unpaid = I
        if early:
            day = int(rng.integers(3, 31)) if rng.random() < 0.6 else int(rng.integers(36, 61))
            d = I + TD(days=day)
            amt = billed + (C.LATE_FEE if day > 35 else 0.0)
            ch = rng.choice(["WEB", "IVR", "MAIL", "WALKIN"], p=[0.52, 0.18, 0.22, 0.08])
            pay.append([r.inv_no, d, ch, round(amt, 2), ""])
            late_flag[j] = C.LATE_FEE if day > 35 else 0.0
            if ch in ("WEB", "IVR") and rng.random() < 0.005:
                rv = d + TD(days=int(rng.integers(6, 26)))
                pay.append([r.inv_no, rv, "REVERSAL", -round(amt, 2), "RETURNED PAYMENT"])
                start_unpaid = rv
            else:
                continue
        # unpaid: late fee at 35 days, then the hold or the agency
        late = C.LATE_FEE
        late_flag[j] = late
        hold_day = max(I + TD(days=61), start_unpaid + TD(days=1))
        if is_home and p.match:
            hd = bday(hold_day)
            e = next_expiry(hd, int(p.exp_m), int(p.exp_par))
            renew_day = e - TD(days=int(rng.integers(0, 46)))
            if renew_day < hd:
                e = next_expiry(e, int(p.exp_m), int(p.exp_par))
                renew_day = e - TD(days=int(rng.integers(0, 46)))
            holds.append([r.inv_no, p.plate, hd, "HOLD PLACED", e, None, ""])
            bal = r.toll + r.fee + late
            if rng.random() < 0.05:
                vd = hd + TD(days=int(rng.integers(5, 400)))
                if vd < renew_day:
                    pay.append([r.inv_no, vd, rng.choice(["WEB", "IVR", "MAIL"]), round(bal, 2), ""])
                    holds[-1][5] = vd; holds[-1][6] = "PAID"
                    continue
            renew_p = 0.50 if p.chronic else (0.90 if p.phantom else 0.86)
            if rng.random() < renew_p:
                pay.append([r.inv_no, renew_day, "DMV", round(bal, 2), "DMV RENEWAL"])
                holds[-1][5] = renew_day; holds[-1][6] = "PAID AT RENEWAL"
            continue
        if is_home:
            holds.append([r.inv_no, p.plate, bday(hold_day), "NO RECORD", None, None, ""])
        placed = bday(max(I + TD(days=90), start_unpaid + TD(days=30)))
        bal = (r.toll + r.fee + late) * (1 + C.AGENCY_PCT)
        if p.phantom:
            ap = 0.25
        elif r.kind == "TBM":
            ap = 0.26 if not is_home else 0.30
        else:
            ap = 0.06 if p.chronic else (0.20 if not is_home else 0.22)
        close = placed + TD(days=270)
        if r.kind == "VIO":
            # the violation agency works the whole account: one collection takes every invoice it holds for the plate
            vio_place.setdefault(r.pi, []).append([placed, r.inv_no, round(bal, 2), ap, None])
            continue
        if rng.random() < ap:
            d = placed + TD(days=int(rng.integers(20, 270)))
            pay.append([r.inv_no, d, "AGENCY", round(bal, 2), "CMR REMITTANCE"])
            agy.append([r.inv_no, placed, "COLLECTED", d, "Corrigan Mott Recovery"])
        else:
            agy.append([r.inv_no, placed, "RETURNED UNCOLLECTED", close, "Corrigan Mott Recovery"])
    for pi in sorted(vio_place):
        L = sorted(vio_place[pi])
        ev = []
        for k, x in enumerate(L):
            if rng.random() < x[3]:
                ev.append((x[0] + TD(days=int(rng.integers(20, 270))), k))
        for d, k in sorted(ev):
            if L[k][4] is not None:
                continue
            cov = [j for j, y in enumerate(L) if y[4] is None and y[0] <= d < y[0] + TD(days=270)]
            if not cov:
                continue
            for j in cov:
                L[j][4] = d
            pay.append([L[cov[0]][1], d, "AGENCY", round(sum(L[j][2] for j in cov), 2), "BENBOW REMITTANCE"])
        for y in L:
            if y[4] is not None:
                agy.append([y[1], y[0], "COLLECTED", y[4], "Benbow Associates"])
            else:
                agy.append([y[1], y[0], "RETURNED UNCOLLECTED", y[0] + TD(days=270), "Benbow Associates"])
    settle = []
    pay = pd.DataFrame(pay, columns=["inv_no", "posted", "channel", "amount", "reference"])
    holds = pd.DataFrame(holds, columns=["inv_no", "plate", "requested", "response", "reg_expires", "released", "release_reason"])
    agy = pd.DataFrame(agy, columns=["inv_no", "placed", "status", "closed", "agency"])
    return pay, holds, agy, settle, late_flag
