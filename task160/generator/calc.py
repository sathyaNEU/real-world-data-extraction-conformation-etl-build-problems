"""Every figure the design note, the checks and the write-up quote, computed forward from the clean truth: the golden
block, each rung of the ladder, the convergence family, the out-of-sample record and the asks. verify.py recomputes
the graded figures from the shipped bundle on its own code path."""
from __future__ import annotations

import datetime as dt
import statistics as st

import numpy as np

import common as C
import world as W

D = dt.date


def r50(x):
    return int(50 * round(x / 50.0))


class Truth:
    def __init__(self):
        self.hs, self.wp, self.truth = W.simulate()
        self.H = {h["facility_id"]: h for h in self.hs}
        self.decl = W.declarations(self.hs, self.truth)
        self.iv = {h["facility_id"]: W.active_intervals(self.decl, h["facility_id"]) for h in self.hs}
        self.shifts = W.agency_shifts(self.hs, self.truth, self.decl)

    # ---------------------------------------------------------------------------------------------- census reads
    def nights(self, fid, a, b):
        return [r for r in self.truth[fid] if a <= r["date"] <= b]

    def draw_grid(self, fid, a, b):
        """Surge nights in [a, b] priced at the register's agency staffing per level."""
        g = self.H[fid]["grid"]
        return sum(g[r["level"] - 1] for r in self.nights(fid, a, b) if r["level"])

    def draw_shifts(self, fid, a, b):
        """The same draw counted shift by shift at the level in force when each shift starts (declaration times)."""
        g = self.H[fid]["grid"]
        n = 0
        for d in C.daterange(a, b):
            for hh in (7, 19):
                lv = W.level_at(self.iv[fid], dt.datetime.combine(d, dt.time(hh)))
                if lv:
                    n += g[lv - 1] // 2
        return n

    def region(self, reg):
        return [h for h in self.hs if h["region"] == reg]

    def south(self):
        return [h for h in self.hs if h["region"] != "NO"]

    def season_draw(self, hs, w, how="grid"):
        a, b = C.season_bounds(w)
        f = self.draw_grid if how == "grid" else self.draw_shifts
        return sum(f(h["facility_id"], a, b) for h in hs)

    def block_draw(self, hs, w, how="grid"):
        a, b = C.block_weeks(w) if w < 2027 else C.BLOCK_2027
        f = self.draw_grid if how == "grid" else self.draw_shifts
        return sum(f(h["facility_id"], a, b) for h in hs)

    # ---------------------------------------------------------------------------------------------- timing
    def spell(self, fid, w):
        a, b = C.season_bounds(w)
        sp = W.spells(self.nights(fid, a, b))
        assert len(sp) == 1, (fid, w, sp)
        return sp[0]

    def mid(self, fid, w):
        a, b, _, _ = self.spell(fid, w)
        return a.toordinal() + (b - a).days / 2.0

    def region_mid(self, reg, w, upto=None):
        return float(np.median([self.mid(h["facility_id"], w) for h in self.region(reg)]))

    def lags(self, up="WC"):
        """The North's wave centre behind an upstream region's, each closed winter."""
        return {w: self.region_mid("NO", w) - self.region_mid(up, w) for w in C.CLOSED}

    def first(self, reg, w, upto=None):
        a, b = C.season_bounds(w)
        b = min(b, upto) if upto else b
        return min(r["date"] for h in self.region(reg) for r in self.truth[h["facility_id"]]
                   if a <= r["date"] <= b and r["level"]).toordinal()

    # ---------------------------------------------------------------------------------------------- the golden
    def north_waves(self, how="grid"):
        return [self.season_draw(self.region("NO"), w, how) for w in C.CLOSED]

    def golden(self):
        return st.mean(self.north_waves())


if __name__ == "__main__":
    T = Truth()
    nw = T.north_waves()
    print("North per-wave draws", nw, "mean %.1f" % st.mean(nw))
    print("North per-wave (shift by shift)", T.north_waves("shifts"))
    print("lags", {w: round(v, 1) for w, v in T.lags().items()})
    print("block draws", {w: T.block_draw(T.hs, w) for w in C.WINTERS})


# -------------------------------------------------------------------------------------------------- the rungs
def rungs(T):
    """Every route the ladder names, computed on the clean truth at the register's staffing (grid basis)."""
    out = {}
    south, north = T.south(), T.region("NO")
    jan = {w: T.block_draw(T.hs, w) for w in C.CLOSED}
    jan_s = {w: T.block_draw(south, w) for w in C.CLOSED}
    jan_n = {w: T.block_draw(north, w) for w in C.CLOSED}
    out["R0"] = st.mean(jan.values())                                  # the calendar: closed Januaries averaged
    out["R0_south"] = st.mean(jan_s.values())
    out["R0_north"] = st.mean(jan_n.values())
    out["R0b"] = jan[2026]                                              # last January
    b = np.polyfit(np.array(C.CLOSED, float), np.array([jan[w] for w in C.CLOSED], float), 1)
    out["R0c"] = float(np.polyval(b, 2027))                             # the January draws trended
    # the pool's own post-peak profile: the sixteen southern members' daily draw aligned on each closed winter's
    # Southeast centre, read over this winter's block weeks; the North at the same draw per staffed bed
    se27 = T.region_mid("SE", 2027)
    a27, b27 = C.BLOCK_2027
    offs = (a27.toordinal() - se27, b27.toordinal() - se27)
    prof = []
    for w in C.CLOSED:
        c = T.region_mid("SE", w)
        a = D.fromordinal(int(round(c + offs[0])))
        bb = D.fromordinal(int(round(c + offs[1])))
        prof.append(sum(T.draw_grid(h["facility_id"], a, bb) for h in south))
    beds_s = sum(h["beds"] for h in south)
    beds_n = sum(h["beds"] for h in north)
    out["R1"] = st.mean(prof) * (1 + beds_n / beds_s)
    out["R1_south"] = st.mean(prof)
    # the same post-peak profile for the south with the North at its own calendar January
    out["R1b"] = st.mean(prof) + out["R0_north"]
    # the closest closed winter by the Southeast's timing (2022-23) taken whole
    out["R2c"] = jan[2023]
    # one month later: the four weeks from the first Monday in February, every member at its staffing
    def feb(w):
        d = D(w, 2, 1)
        while d.weekday() != 0:
            d += dt.timedelta(days=1)
        return d, d + dt.timedelta(days=27)
    out["R2d"] = st.mean([sum(T.draw_grid(h["facility_id"], *feb(w)) for h in T.hs) for w in C.CLOSED])
    # a fit of the January draw on the Southeast's timing, extrapolated to this winter
    x = np.array([T.region_mid("SE", w) - D(w - 1, 12, 1).toordinal() for w in C.CLOSED])
    y = np.array([jan[w] for w in C.CLOSED], float)
    b2 = np.polyfit(x, y, 1)
    out["R2e"] = float(np.polyval(b2, se27 - D(2026, 12, 1).toordinal()))
    # the season's usual total less what the season has drawn: to the as-of, and with December's tail
    seas = [T.season_draw(T.hs, w) for w in C.CLOSED]
    sofar = sum(T.draw_grid(h["facility_id"], C.season_bounds(2027)[0], C.CENSUS_END) for h in T.hs)
    todec = sum(T.draw_grid(h["facility_id"], C.season_bounds(2027)[0], D(2026, 12, 31)) for h in T.hs)
    out["R2f"] = st.mean(seas) - sofar
    out["R2f_dec"] = st.mean(seas) - todec
    # the golden and its convergence family
    nw = T.north_waves()
    nws = T.north_waves("shifts")
    out["R3"] = st.mean(nw)
    srt = sorted(nw)
    fam = {
        "mean of five waves (staffing per night)": st.mean(nw),
        "mean of five waves (shift by shift)": st.mean(nws),
        "median of five waves": st.median(nw),
        "last three waves": st.mean(nw[-3:]),
        "middle three waves": st.mean(srt[1:4]),
        "hospital by hospital medians": sum(st.median([T.season_draw([h], w) for w in C.CLOSED]) for h in north),
        "scaled by this winter's southern draw": st.mean(nw) * T.season_draw(south, 2027) / st.mean([T.season_draw(south, w) for w in C.CLOSED]),
        "every member aligned on West and Central's centre": aligned(T, "WC"),
        "the North placed by West and Central's first surge night": placed(T, "WC", onset=True),
    }
    out["family"] = fam
    out["north_waves"] = nw
    out["lags"] = T.lags()
    out["lags_se"] = T.lags("SE")
    out["jan"] = jan
    # timing the North from the Southeast instead of West and Central: the North placed by the Southeast's centre or
    # first surge night and the closed winters' mean lag, and the whole state aligned on the Southeast
    out["R1c"] = placed(T, "SE")
    out["R1c_onset"] = placed(T, "SE", onset=True)
    out["R1d"] = aligned(T, "SE")
    return out


def _window(T, fids, w, delta):
    a, b = C.BLOCK_2027
    return sum(T.draw_grid(f, a - dt.timedelta(days=delta), b - dt.timedelta(days=delta)) for f in fids)


def _anchor(T, reg, w, onset=False, upto=None):
    if onset:
        return T.first(reg, w, upto)
    if w == 2027:
        a, _ = C.season_bounds(2027)
        mids = []
        for h in T.region(reg):
            sp = W.spells([r for r in T.truth[h["facility_id"]] if a <= r["date"] <= upto])
            mids.append(sp[0][0].toordinal() + (sp[0][1] - sp[0][0]).days / 2.0)
        return float(np.median(mids))
    return T.region_mid(reg, w)


def aligned(T, reg, onset=False):
    """Every member's closed-winter census moved so the anchor region's wave sits where it sits this winter (its
    centre, or its first surge night, as the census shows it at the pull), read over the block weeks and averaged."""
    a27 = _anchor(T, reg, 2027, onset, C.CENSUS_END)
    fids = [h["facility_id"] for h in T.hs]
    return st.mean(_window(T, fids, w, int(round(a27 - _anchor(T, reg, w, onset)))) for w in C.CLOSED)


def placed(T, up, onset=False):
    """The North's closed-winter waves placed this winter by an upstream region's centre (or first surge night) and the
    closed winters' mean lag, read over the block weeks and averaged."""
    north = [h["facility_id"] for h in T.region("NO")]
    lags = [_anchor(T, "NO", w, onset) - _anchor(T, up, w, onset) for w in C.CLOSED]
    pred = _anchor(T, up, 2027, onset, C.CENSUS_END) + st.mean(lags)
    return st.mean(_window(T, north, w, int(round(pred - _anchor(T, "NO", w, onset)))) for w in C.CLOSED)


if __name__ == "__main__":
    T = Truth()
    R = rungs(T)
    for k, v in R.items():
        print(k, v if not isinstance(v, float) else round(v, 1))


# -------------------------------------------------------------------------------------------------- out of sample
def out_of_sample(T):
    """Each closed January forecast from the winter before it by the calendar (last January carried); the North's
    per-wave draw and its lag behind West and Central (and, for the rival, behind the Southeast) each left out one
    winter at a time and forecast from the other four."""
    jan = {w: T.block_draw(T.hs, w) for w in C.CLOSED}
    carry = {w: (jan[w - 1] - jan[w]) / jan[w] for w in C.CLOSED[1:]}
    loo = {}
    nw = dict(zip(C.CLOSED, T.north_waves()))
    for w in C.CLOSED:
        others = [nw[v] for v in C.CLOSED if v != w]
        loo[w] = (st.mean(others) - nw[w]) / nw[w]
    lag = T.lags()
    lag_err = {w: lag[w] - st.mean([lag[v] for v in C.CLOSED if v != w]) for w in C.CLOSED}
    lse = T.lags("SE")
    lag_err_se = {w: lse[w] - st.mean([lse[v] for v in C.CLOSED if v != w]) for w in C.CLOSED}
    return {"carry": carry, "north_loo": loo, "lag_loo": lag_err, "lag_loo_se": lag_err_se, "jan": jan}


def timing_2027(T):
    """This winter's timing as the generator realised it (never shipped): the south's last surge night, the North's
    spells against the block weeks."""
    a, b = C.season_bounds(2027)
    south_last = max(T.spell(h["facility_id"], 2027)[1] for h in T.south())
    north = [T.spell(h["facility_id"], 2027) for h in T.region("NO")]
    return {"south_last": south_last, "north_first": min(s[0] for s in north), "north_last": max(s[1] for s in north),
            "realised_north": T.block_draw(T.region("NO"), 2027), "realised_all": T.block_draw(T.hs, 2027)}
