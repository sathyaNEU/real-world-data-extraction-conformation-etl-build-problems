"""Every rung, rival and grid cell of the main call, computed from the world at shipped precision."""
from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np
import pandas as pd

from common import (BOOKS, EXTRACT, HEDGES, NC, PEAKS, SUMMERS, continuous_split, lot_margins, lots, p90,
                    round_half_up, water_level)
from world import CENTRE_TOTAL_KW


def _active(prem, d, dedup=True):
    a = prem[(prem["start"] <= d) & prem["end"].map(lambda e: e is None or e >= d)]
    return a[a["record_type"] == "NEW"] if dedup else a


class Analysis:
    def __init__(self, w):
        self.w = w
        p = w.prem
        st = w.settled.set_index(["book", "date", "he"])["mwh"]
        self.st = st
        self.peak_load = {b: {y: float(st[(b, PEAKS[y][0], PEAKS[y][1])]) for y in SUMMERS} for b in BOOKS}
        self.md_peak = {b: {} for b in BOOKS}
        self.ref_peak = {b: {} for b in BOOKS}
        for y in SUMMERS:
            a = _active(p, PEAKS[y][0])
            g = a.groupby("book")["md_kw"].sum()
            r = a[a["comp"] == "ref"].groupby("book")["md_kw"].sum()
            for b in BOOKS:
                self.md_peak[b][y] = float(g.get(b, 0.0))
                self.ref_peak[b][y] = float(r.get(b, 0.0))
        rows = _active(p, EXTRACT, dedup=False)
        ded = rows[rows["record_type"] == "NEW"]
        self.rows27 = rows.groupby("book")["md_kw"].sum().reindex(BOOKS).fillna(0).to_dict()
        self.ded27 = ded.groupby("book")["md_kw"].sum().reindex(BOOKS).fillna(0).to_dict()
        self.centres = float(ded.loc[ded["comp"] == "centre", "md_kw"].sum())
        pk26 = PEAKS[2026][0]
        newgen = ded[(ded["book"] == NC) & (ded["comp"] != "centre") & (ded["start"] > pk26)]
        self.new_general_nc = float(newgen["md_kw"].sum())
        self.ref27 = ded[ded["comp"] == "ref"].groupby("book")["md_kw"].sum().reindex(BOOKS).fillna(0).to_dict()
        self.amend_kw = float(rows.loc[rows["record_type"] == "AMEND", "md_kw"].sum())
        self.amend_rows = int((rows["record_type"] == "AMEND").sum())
        # the fourteen at the closed peaks, and uncalled
        mem = p[(p["comp"] == "ref") & (p["record_type"] == "NEW")].set_index("esi_id")
        self.mem = mem
        mr = w.mreads.copy()
        mr["y"] = [d.year for d in mr["date"]]
        mr["md"] = mr["esi_id"].map(mem["md_kw"])
        mr["called"] = [d in set(w.calls[d.year]) for d in mr["date"]]
        mr["pkh"] = mr["y"].map(lambda y: PEAKS[y][1])
        self.mr = mr
        atpk = mr[[(d == PEAKS[y][0]) and h == PEAKS[y][1] for d, y, h in zip(mr["date"], mr["y"], mr["he"])]]
        self.class_by_summer = {y: float(g["kwh"].sum() / g["md"].sum()) for y, g in atpk.groupby("y")}
        self.class_factor = float(atpk["kwh"].sum() / atpk["md"].sum())
        self.site_called = (atpk["kwh"] / atpk["md"]).to_numpy()
        self.u_star = w.u_star
        # the programme's own baseline at each closed peak hour (ten most recent uncalled business days), MD-weighted
        base = w.base_at_peak
        self.baseline = float(sum(base.values()) / sum(mem.at[e, "md_kw"] for (_, e) in base))
        t = w.temps.set_index(["date", "book"])["tmax"]
        mr["tmax"] = [t[(d, b)] for d, b in zip(mr["date"], mr["esi_id"].map(mem["book"]))]
        self.tmax = t

    # -------------------------------------------------------------- replay arithmetic
    def pooled(self, b, y):
        return self.peak_load[b][y] / (self.md_peak[b][y] / 1000.0)

    def replay(self, b, md_kw):
        return [self.pooled(b, y) * md_kw / 1000.0 for y in SUMMERS]

    def exposures(self, kind, centre_factor=None, method="linear", members_uncalled=False, newgen_factor=None):
        E = {}
        for b in BOOKS:
            if kind == "settled":
                L = p90([self.peak_load[b][y] for y in SUMMERS], method)
            elif kind == "rows":
                base = self.rows27[b] - (self.centres if (b == NC and centre_factor is not None) else 0.0)
                L = p90(self.replay(b, base), method)
            else:  # dedup
                base = self.ded27[b] - (self.centres if (b == NC and centre_factor is not None) else 0.0)
                if b == NC and newgen_factor is not None:
                    base -= self.new_general_nc
                L = p90(self.replay(b, base), method)
            if b == NC and centre_factor is not None:
                L += centre_factor * self.centres / 1000.0
            if b == NC and newgen_factor is not None:
                L += newgen_factor * self.new_general_nc / 1000.0
            if members_uncalled:
                L += (self.u_star - self.class_factor) * self.ref27[b] / 1000.0
            E[b] = L - HEDGES[b]
        return E

    def rungs(self):
        R = {
            "R0": self.exposures("settled"),
            "R1": self.exposures("rows"),
            "R2": self.exposures("dedup"),
            "R3": self.exposures("dedup", centre_factor=self.class_factor),
            "R4": self.exposures("dedup", centre_factor=self.baseline),
            "R5": self.exposures("dedup", centre_factor=self.u_star),
        }
        return R

    def loads_answer(self):
        E = self.exposures("dedup", centre_factor=self.u_star)
        return {b: E[b] + HEDGES[b] for b in BOOKS}

    def grid(self, lo=None, hi=None):
        cf, u, bl = self.class_factor, self.u_star, self.baseline
        g = {
            "rows, pooled (rung 1)": self.exposures("rows"),
            "rows, class factor on the centres": self.exposures("rows", centre_factor=cf),
            "rows, programme baseline on the centres": self.exposures("rows", centre_factor=bl),
            "rows, peak-heat draw on the centres": self.exposures("rows", centre_factor=u),
            "premises, pooled (rung 2)": self.exposures("dedup"),
            "premises, class factor (rung 3)": self.exposures("dedup", centre_factor=cf),
            "premises, programme baseline (rung 4)": self.exposures("dedup", centre_factor=bl),
            "premises, peak-heat draw (answer)": self.exposures("dedup", centre_factor=u),
            "partial: class factor on every new North Central premise": self.exposures("dedup", centre_factor=cf, newgen_factor=cf),
            "partial: peak-heat draw on every new North Central premise": self.exposures("dedup", centre_factor=u, newgen_factor=u),
            "partial: programme baseline on every new North Central premise": self.exposures("dedup", centre_factor=bl, newgen_factor=bl),
            "members uncalled in 2027 too": self.exposures("dedup", centre_factor=u, members_uncalled=True),
            "centres at their full maximum demand (1.00)": self.exposures("dedup", centre_factor=1.0),
            "P90 nearest rank": self.exposures("dedup", centre_factor=u, method="inverted_cdf"),
            "P90 exclusive (Excel PERCENTILE.EXC)": self.exclusive(),
            "settled loads, own book (rung 0)": self.exposures("settled"),
        }
        if lo is not None:
            g[f"centres at {lo:.3f}"] = self.exposures("dedup", centre_factor=lo)
            g[f"centres at {hi:.3f}"] = self.exposures("dedup", centre_factor=hi)
        return g

    def exclusive(self):
        E = {}
        for b in BOOKS:
            base = self.ded27[b] - (self.centres if b == NC else 0.0)
            x = sorted(self.replay(b, base))
            r = 0.9 * (len(x) + 1)  # 9.9
            lo = int(math.floor(r)) - 1
            L = x[lo] + (r - math.floor(r)) * (x[lo + 1] - x[lo])
            if b == NC:
                L += self.u_star * self.centres / 1000.0
            E[b] = L - HEDGES[b]
        return E

    def class_replay_full(self):
        """Each summer: the general premises at the general factor (settled less members, over MD less members' MD),
        the members at their own measured draw, applied to the 2027 classes; the centres at the uncalled draw."""
        E = {}
        for b in BOOKS:
            xs = []
            for y in SUMMERS:
                ref_load = self._ref_load(b, y)
                fg = (self.peak_load[b][y] - ref_load) / ((self.md_peak[b][y] - self.ref_peak[b][y]) / 1000.0)
                fr = ref_load / (self.ref_peak[b][y] / 1000.0) if self.ref_peak[b][y] else self.class_factor
                gen27 = self.ded27[b] - self.ref27[b] - (self.centres if b == NC else 0.0)
                xs.append(fg * gen27 / 1000.0 + fr * self.ref27[b] / 1000.0)
            L = p90(xs) + (self.u_star * self.centres / 1000.0 if b == NC else 0.0)
            E[b] = L - HEDGES[b]
        return E

    def _ref_load(self, b, y):
        m = self.mr
        sel = m[(m["date"] == PEAKS[y][0]) & (m["he"] == PEAKS[y][1])]
        sel = sel[sel["esi_id"].map(self.mem["book"]) == b]
        return float(sel["kwh"].sum()) / 1000.0

    def naics_replay(self):
        """IDR premises by NAICS code at their own summer's draw, the profiled remainder at its own, members at theirs."""
        p, w = self.w.prem, self.w
        ir = w.ireads
        E = {}
        ded = _active(p, EXTRACT)
        for b in BOOKS:
            xs = []
            gen27 = ded[(ded["book"] == b) & (ded["comp"] == "idr")]
            prof27 = float(ded.loc[(ded["book"] == b) & (ded["comp"] == "prof"), "md_kw"].sum())
            for y in SUMMERS:
                d, h = PEAKS[y][0], PEAKS[y][1]
                a = _active(p, d)
                ga = a[(a["book"] == b) & (a["comp"] == "idr")]
                r = ir[(ir["date"] == d) & (ir["he"] == h)].set_index("esi_id")["kwh"]
                ga = ga.assign(kwh=ga["esi_id"].map(r))
                fac = (ga.groupby("naics")["kwh"].sum() / ga.groupby("naics")["md_kw"].sum()).to_dict()
                gall = ga["kwh"].sum() / ga["md_kw"].sum()
                ref_load = self._ref_load(b, y) * 1000.0
                profl = self.peak_load[b][y] * 1000.0 - ga["kwh"].sum() - ref_load
                profmd = self.md_peak[b][y] - ga["md_kw"].sum() - self.ref_peak[b][y]
                fp = profl / profmd
                fr = ref_load / self.ref_peak[b][y] if self.ref_peak[b][y] else self.class_factor
                x = sum(fac.get(n, gall) * k for n, k in gen27.groupby("naics")["md_kw"].sum().items())
                xs.append((x + fp * prof27 + fr * self.ref27[b]) / 1000.0)
            L = p90(xs) + (self.u_star * self.centres / 1000.0 if b == NC else 0.0)
            E[b] = L - HEDGES[b]
        return E

    # -------------------------------------------------------------- the replay table and its rivals
    def md_on(self, d):
        a = _active(self.w.prem, d)
        return a.groupby("book")["md_kw"].sum().reindex(BOOKS).fillna(0).to_dict()

    def replay_table(self):
        return {(b, y): self.pooled(b, y) * self.md_peak[b][2026] / 1000.0 for b in BOOKS for y in SUMMERS}

    def replay_rivals(self):
        tab = self.replay_table()
        out = {}
        out["settled loads unscaled"] = {(b, y): self.peak_load[b][y] for b in BOOKS for y in SUMMERS}
        ye = {y: self.md_on(date(y, 12, 31)) for y in SUMMERS}
        j1 = {y: self.md_on(date(y, 6, 1)) for y in SUMMERS}
        out["divisor at year end"] = {(b, y): self.peak_load[b][y] / ye[y][b] * self.md_peak[b][2026] for b in BOOKS for y in SUMMERS}
        out["divisor at 1 June"] = {(b, y): self.peak_load[b][y] / j1[y][b] * self.md_peak[b][2026] for b in BOOKS for y in SUMMERS}
        avg = {}
        for y in SUMMERS:
            ds = [date(y, 6, 1) + timedelta(days=k) for k in range(0, 122, 7)]
            ms = [self.md_on(d) for d in ds]
            avg[y] = {b: float(np.mean([m[b] for m in ms])) for b in BOOKS}
        out["summer average enrolled MD (weekly)"] = {(b, y): self.peak_load[b][y] / avg[y][b] * self.md_peak[b][2026] for b in BOOKS for y in SUMMERS}
        own = {}
        s = self.w.settled
        for (b, y), g in s.assign(y=[d.year for d in s["date"]]).groupby(["book", "y"]):
            i = g["mwh"].idxmax()
            own[(b, y)] = (float(g.at[i, "mwh"]), g.at[i, "date"])
        mdo = {}
        for (b, y), (v, d) in own.items():
            mdo[(b, y)] = v / self.md_on(d)[b] * self.md_peak[b][2026]
        out["zone's own peak hour"] = mdo
        res = {}
        for k, t in out.items():
            hits = sum(1 for c in tab if round_half_up(t[c]) == round_half_up(tab[c]))
            worst = max(abs(t[c] - tab[c]) / tab[c] for c in tab)
            res[k] = (hits, worst)
        return res

    # -------------------------------------------------------------- the uncalled draw: two families of estimators
    def _unc(self):
        m = self.mr[(self.mr["he"] == self.mr["pkh"]) & ~self.mr["called"]].copy()
        m["s"] = m["kwh"] / m["md"]
        return m

    def estimators(self):
        """The draw on ordinary uncalled weekdays, every way a solver could average it, and the programme baseline."""
        m = self._unc()
        per_y = {y: g["kwh"].sum() / g["md"].sum() for y, g in m.groupby("y")}
        per_site = m.groupby("esi_id")["s"].mean()
        mds = self.mem["md_kw"]
        base = self.w.base_at_peak
        allb = self.all_call_baseline()
        return {
            "pooled, MD-weighted": float(m["kwh"].sum() / m["md"].sum()),
            "pooled, mean of site ratios": float(m["s"].mean()),
            "pooled, median of site ratios": float(m["s"].median()),
            "summer by summer, mean": float(np.mean(list(per_y.values()))),
            "summer by summer, median": float(np.median(list(per_y.values()))),
            "summer by summer, maximum": float(max(per_y.values())),
            "summer by summer, minimum": float(min(per_y.values())),
            "site by site, MD-weighted": float((per_site * mds[per_site.index]).sum() / mds[per_site.index].sum()),
            "site by site, mean": float(per_site.mean()),
            "2026 only": float(per_y[2026]),
            "programme baseline at each closed peak hour": float(self.baseline),
            "programme baseline at the peak hour, every called day": allb,
        }

    def all_call_baseline(self):
        """The terms' baseline at the summer's peak hour for every called day, MD-weighted over member-days."""
        from common import billing_holidays, summer_weekdays
        r = self.mr.set_index(["esi_id", "date", "he"])["kwh"]
        num = den = 0.0
        for y in SUMMERS:
            he = PEAKS[y][1]
            cs = set(self.w.calls[y])
            bd = [d for d in summer_weekdays(y) if d not in billing_holidays(y)]
            for d in self.w.calls[y]:
                prior = [x for x in bd if x < d and x not in cs]
                for esi, mm in self.mem.iterrows():
                    if mm["start"] > d:
                        continue
                    pr = [x for x in prior if x >= mm["start"]][-10:]
                    if not pr:
                        continue
                    num += float(np.mean([r[(esi, x, he)] for x in pr]))
                    den += mm["md_kw"]
        return num / den

    def peak_estimators(self):
        """What an uncalled cold store draws in the system peak hour, every way a solver could condition on heat."""
        m = self._unc()
        cut = self.w.temp_cut
        bk = m["esi_id"].map(self.mem["book"])
        W = lambda g: float(g["kwh"].sum() / g["md"].sum())  # noqa: E731
        hot = self.hot_uncalled()
        med = {b: float(np.median([self.tmax[(PEAKS[y][0], b)] for y in SUMMERS])) for b in BOOKS}
        q90 = m.groupby(["esi_id", "y"])["tmax"].transform(lambda x: x.quantile(0.9))
        return {
            "zone at least as hot as its coolest closed peak day (golden)": W(m[m["tmax"] >= bk.map(cut)]),
            "zone at least as hot as its median closed peak day": W(m[m["tmax"] >= bk.map(med)]),
            "hottest-decile weekdays (book-wide settled load), uncalled": W(m[[d in hot for d in m["date"]]]),
            "hottest tenth of each site-summer's uncalled weekdays by zone maximum": W(m[m["tmax"] >= q90]),
            "each site-summer's highest uncalled peak-hour draw": float(m.groupby(["esi_id", "y"])["s"].max().mean()),
            "each site's highest uncalled peak-hour draw over ten summers": float(m.groupby("esi_id")["s"].max().mean()),
        }

    def middle_estimators(self):
        """Readings that condition on heat but not on peak-day heat: neither the ordinary nor the peak-day draw."""
        m = self._unc()
        W = lambda g: float(g["kwh"].sum() / g["md"].sum())  # noqa: E731
        q80 = m.groupby(["esi_id", "y"])["tmax"].transform(lambda x: x.quantile(0.8))
        X = np.c_[np.ones(len(m)), m["tmax"].to_numpy(float)]
        b0, b1 = np.linalg.lstsq(X, m["s"].to_numpy(), rcond=None)[0]
        bk = m["esi_id"].map(self.mem["book"])
        pk = np.mean([self.tmax[(PEAKS[y][0], b)] for y in SUMMERS for b in set(bk)])
        return {"hottest fifth of each site-summer's uncalled weekdays": W(m[m["tmax"] >= q80]),
                "straight line on zone maximum, read at the mean peak-day maximum": float(min(1.0, b0 + b1 * pk))}

    def hot_uncalled(self):
        """Weekdays in each summer's hottest decile (by the book-wide settled daily maximum) without a call."""
        s = self.w.settled
        tot = s.groupby(["date", "he"])["mwh"].sum().groupby(level=0).max()
        out = set()
        self.hot_counts = {}
        for y in SUMMERS:
            t = tot[[d.year == y and d.weekday() < 5 for d in tot.index]]
            n10 = math.ceil(0.1 * len(t))
            top = t.sort_values(ascending=False).index[:n10]
            unc = [d for d in top if d not in set(self.w.calls[y])]
            self.hot_counts[y] = len(unc)
            out |= set(unc)
        return out


def lenders_basis(an, outlook_rows):
    """The lenders' zone-share view: book share of the zone's June-September 2026 energy times ERCOT's 90/10 zone
    peak forecast for 2027, less hedges."""
    s = an.w.settled
    e26 = s[[d.year == 2026 for d in s["date"]]].groupby("book")["mwh"].sum()
    E = {}
    for b, pk, e, f50, f90 in outlook_rows:
        share = e26[b] / (e * 1000.0)
        E[b] = share * f90 - HEDGES[b]
    return E
