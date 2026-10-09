"""Golden computations on the generator's own frames: the main call, the ladder, the correction grid,
the calibration corpus, the twin pair and the two audits. build_pack.py asserts on these; the
independent verifier recomputes the same quantities from the shipped bytes alone."""
from __future__ import annotations

import math
from datetime import date, datetime

import numpy as np
import pandas as pd

from common import GRID_T0, QH, TZ, grid_frame, load_curve, nearest5, up5

GROWTH = 1.12
RATIO = 11.5 / 6.6
AS_OF = date(2027, 1, 25)
DECKS = ("CCN", "CCS")


def local_dates(t):
    return pd.to_datetime(np.asarray(t, dtype=np.int64), unit="s", utc=True).tz_convert(TZ)


class Analysis:
    def __init__(self, w):
        self.w = w
        self.gf = grid_frame()
        self.bill = self.gf["billing"].to_numpy()
        self.bill_shift = self.gf["billing_shift"].to_numpy()
        self.year = self.gf["year"].to_numpy()
        self.month = self.gf["month"].to_numpy()
        rows = w.rows
        loc = local_dates(rows["start"])
        rows = rows.assign(ly=loc.year, lm=loc.month)
        self.rows = rows
        true = rows["true_row"] & ~rows["redelivered"]
        self.deck_true = rows[true & rows["garage"].isin(DECKS)]
        self.pop26 = self.deck_true[(self.deck_true["ly"] == 2026) & self.deck_true["in_ledger"]].copy()
        # the car behind each 2026 session on its own date, and the car its permit carries into the contract year
        self.pop26["car"] = self.car_by_join(self.pop26)
        self.pop26["car27"] = self.car_by_join(self.pop26, as_of=AS_OF)
        veh26 = self.vehicles_at(date(2026, 12, 31), date(2026, 1, 1))
        veh27 = self.vehicles_at(AS_OF, AS_OF)
        self.favg = float(np.mean(np.minimum(11.5, veh26["rating"])))
        self.davg = {"CCN": float(np.mean(veh26.loc[veh26["deck"] == "North", "rating"])),
                     "CCS": float(np.mean(np.minimum(11.5, veh26.loc[veh26["deck"] == "South", "rating"])))}
        self.favg27 = float(np.mean(np.minimum(11.5, veh27["rating"])))
        self.davg27 = {"CCN": float(np.mean(veh27.loc[veh27["deck"] == "North", "rating"])),
                       "CCS": float(np.mean(np.minimum(11.5, veh27.loc[veh27["deck"] == "South", "rating"])))}
        self.veh26 = veh26
        self.veh27 = veh27

    # ------------------------------------------------------------------ the car behind a session
    def car_by_join(self, s: pd.DataFrame, as_of: date | None = None) -> pd.Series:
        """Session -> permit -> plate -> checked vehicle -> reference rating (fleet cards via the roster)."""
        if not hasattr(self, "_check_rating"):
            from world import reference_frame
            ref = reference_frame()
            ref = ref.assign(MK=ref["make"].str.upper(), MD=ref["model"].str.upper(), TR=ref["trim"].str.upper())

            def rate(mk, md, tr, yr):
                hit = ref[(ref["MK"] == mk) & (ref["MD"] == md) & (ref["model_year_from"] <= yr)
                          & (ref["model_year_to"] >= yr) & ((ref["TR"] == "") | (ref["TR"] == tr))]
                assert len(hit) == 1, (mk, md, tr, yr, len(hit))
                return float(hit["onboard_charger_kw"].iloc[0])
            ch = self.w.veh["checks"].copy()
            ch["rating"] = [rate(a, b, c, d) for a, b, c, d in zip(ch["make"], ch["model"], ch["trim"], ch["model_year"])]
            ch["checked_on"] = pd.to_datetime(ch["checked_on"])
            self._check_rating = ch.sort_values("checked_on")
            fl = self.w.veh["fleet"]
            self._fleet_rating = {c: rate(mk.upper(), md.upper(), tr.upper(), yr) for c, mk, md, tr, yr in
                                  zip(fl["fleet_card"], fl["make"], fl["model"], fl["trim"], fl["model_year"])}
        out = pd.Series(np.nan, index=s.index)
        perm = s[s["permit_no"] != ""]
        if len(perm):
            q = pd.DataFrame({"permit_no": perm["permit_no"].to_numpy(), "idx": perm.index.to_numpy(),
                              "d": pd.to_datetime([as_of or x for x in perm["day"]])}).sort_values("d")
            m = pd.merge_asof(q, self._check_rating[["permit_no", "checked_on", "rating"]], left_on="d",
                              right_on="checked_on", by="permit_no", direction="backward")
            assert m["rating"].notna().all()
            out.loc[m["idx"].to_numpy()] = m["rating"].to_numpy()
        fl = s[s["fleet_card"] != ""]
        out.loc[fl.index] = fl["fleet_card"].map(self._fleet_rating).astype(float)
        return out

    def vehicles_at(self, last: date, first: date) -> pd.DataFrame:
        """Permit vehicles on the permits active at some point in [first, last] (the latest one per permit)."""
        pv = self.w.veh["pveh"]
        permits = self.w.veh["permits"].set_index("permit_no")
        cur = pv[(pv["from"] <= last) & (pv["to"] >= first)].sort_values("from")
        cur = cur.groupby("permit_no").tail(1).copy() if first == last else cur.copy()
        cur["deck"] = cur["permit_no"].map(permits["deck"])
        return cur

    # ------------------------------------------------------------------ replays
    def load(self, s: pd.DataFrame, rate) -> dict:
        rate = pd.Series(rate, index=s.index) if not isinstance(rate, pd.Series) else rate
        out = {}
        for deck in DECKS:
            m = s["garage"] == deck
            st = s.loc[m, "start"].to_numpy(np.float64)
            r = rate[m].to_numpy(np.float64)
            en = st + s.loc[m, "energy"].to_numpy(np.float64) / r * 3600.0
            out[deck] = load_curve(st, en, r)
        return out

    def monthly(self, load: dict, year=2026, shift=False, decks=DECKS) -> dict:
        mask = self.bill_shift if shift else self.bill
        tot = sum(load[d] for d in decks)
        out = {}
        for m in range(1, 13):
            sel = mask & (self.year == year) & (self.month == m)
            idx = np.flatnonzero(sel)
            j = idx[np.argmax(tot[idx])]
            out[m] = (float(tot[j]), int(GRID_T0 + QH * j))
        return out

    def annual(self, load, year=2026, shift=False, decks=DECKS, allhours=False):
        tot = sum(load[d] for d in decks)
        sel = (self.year == year) if allhours else ((self.bill_shift if shift else self.bill) & (self.year == year))
        idx = np.flatnonzero(sel)
        j = idx[np.argmax(tot[idx])]
        return float(tot[j]), int(GRID_T0 + QH * j)

    def rate_rule(self, rule: str, s: pd.DataFrame) -> pd.Series:
        car26 = s["car"] if "car" in s else self.car_by_join(s)
        car = s["car27"] if "car27" in s else self.car_by_join(s, as_of=AS_OF)
        if rule == "percar":
            return np.minimum(11.5, car)
        if rule == "percar26":
            return np.minimum(11.5, car26)
        if rule == "favg27":
            return pd.Series(self.favg27, index=s.index)
        if rule == "davg27":
            return s["garage"].map(self.davg27).astype(float)
        if rule == "r115":
            return pd.Series(11.5, index=s.index)
        if rule == "r110":
            return pd.Series(11.0, index=s.index)
        if rule == "draw66":
            return pd.Series(6.6, index=s.index)
        if rule == "favg":
            return pd.Series(self.favg, index=s.index)
        if rule == "davg":
            return s["garage"].map(self.davg).astype(float)
        if rule == "N_percar_S_rating":
            return pd.Series(np.where(s["garage"] == "CCN", np.minimum(11.5, car), 11.5), index=s.index)
        if rule == "S_percar_N_rating":
            return pd.Series(np.where(s["garage"] == "CCS", np.minimum(11.5, car), 11.5), index=s.index)
        if rule == "pool_rating":
            pool = s["permit_no"].map(self.w.veh["permits"].set_index("permit_no")["holder_type"]) == "Agency"
            return pd.Series(np.where(pool, 11.5, np.minimum(11.5, car)), index=s.index)
        raise KeyError(rule)

    # ------------------------------------------------------------------ the ladder and the grid
    def ladder(self) -> dict:
        s = self.pop26
        res = {}
        loads = {r: self.load(s, self.rate_rule(r, s)) for r in
                 ("percar", "percar26", "r115", "r110", "draw66", "favg", "davg", "favg27", "davg27",
                  "N_percar_S_rating", "S_percar_N_rating", "pool_rating")}
        self.loads = loads
        for r, ld in loads.items():
            v, t = self.annual(ld)
            res[r] = {"peak": v, "at": t, "filed": GROWTH * v}
        # rung 0: the log's highest month, both registers summed
        log = self.w.log
        l26 = log[(pd.to_datetime(log["read_date"]).dt.year == 2026)]
        by = l26.groupby("read_date")["max_kw"].apply(lambda x: x.max() if len(x) > 2 else x.sum())
        per_month = l26.groupby(["read_date", "panel"])["max_kw"].max().unstack().sum(axis=1)
        res["rung0"] = {"registers": float(per_month.max()), "filed": float(per_month.max()) * GROWTH * RATIO}
        closed = res["draw66"]["peak"]
        res["rung1"] = {"closed": closed, "filed": closed * GROWTH * RATIO}
        res["ratio_favg"] = {"filed": closed * GROWTH * self.favg / 6.6}
        res["monthly_percar"] = self.monthly(loads["percar"])
        res["monthly_percar26"] = self.monthly(loads["percar26"])
        res["monthly_r115"] = self.monthly(loads["r115"])
        res["monthly_r110"] = self.monthly(loads["r110"])
        res["monthly_draw66"] = self.monthly(loads["draw66"])
        res["monthly_percar_shift"] = self.monthly(loads["percar"], shift=True)
        res["allhours"] = {r: self.annual(ld, allhours=True)[0] for r, ld in loads.items()}
        res["deck_own"] = {d: self.annual(loads["percar"], decks=(d,)) for d in DECKS}
        return res

    def answer_from(self, peak):
        return GROWTH * peak


def ks(a, b):
    a, b = np.sort(np.asarray(a, float)), np.sort(np.asarray(b, float))
    allv = np.concatenate([a, b])
    cdf_a = np.searchsorted(a, allv, side="right") / len(a)
    cdf_b = np.searchsorted(b, allv, side="right") / len(b)
    return float(np.max(np.abs(cdf_a - cdf_b)))
