"""The golden, computed from the bundle alone: each region's accident-year 2025 claim frequency with the claims not yet
notified developed by the notifying route (the representative's firm type from the representatives table), the
Reserving Standard's back-test on accident year 2022 for every development the extract and the register offer, and
the two asks."""
import datetime as dt
import os
from collections import Counter, defaultdict

import pandas as pd
from openpyxl import load_workbook

import common as K

DAMAGE = set(K.DAMAGE)
COVERS = ("COMP", "TPFT", "TPO")


def _local_date(s):
    """the UK calendar date of a notification: the migrated claims carry a date, the new system a UTC timestamp"""
    if "T" not in s:
        return dt.date.fromisoformat(s)
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    return K.to_local(t).date()


class Bundle:
    def __init__(self, target):
        self.t = target
        f = lambda k: os.path.join(target, K.FILES[k])
        self.districts = pd.read_csv(f("districts"), dtype=str)
        d2r = dict(zip(self.districts.postcode_district, self.districts.sales_region))
        reps = pd.read_csv(f("reps"), dtype=str)
        self.reps = reps
        rtype = dict(zip(reps.representative_ref, reps.firm_type))
        c = pd.read_csv(f("claims"), dtype=str, keep_default_na=False)
        c["region"] = c.risk_postcode_district.map(d2r)
        c["acc"] = pd.to_datetime(c.accident_date).dt.date
        c["ay"] = pd.to_datetime(c.accident_date).dt.year
        c["note"] = [_local_date(s) for s in c.notified_at]
        c["firm_type"] = c.representative_ref.map(rtype).fillna("")
        c["route"] = [nb if nb != "Representative" else ("Claims management company" if ft.startswith("Claims") else
                                                         "Solicitor practice")
                      for nb, ft in zip(c.notified_by, c.firm_type)]
        self.claims = c
        wb = load_workbook(f("exposure"), read_only=True)
        rows = list(wb["2025"].iter_rows(values_only=True))
        hdr = rows[0]
        ex = pd.DataFrame(rows[1:], columns=hdr)
        self.cy = ex[ex["product"] == "PC"].groupby("sales_region")["earned_car_years"].sum().to_dict()
        self.inforce = pd.read_csv(f("inforce"), dtype=str, keep_default_na=False)
        self.changes = pd.read_csv(f("changes"), dtype=str, keep_default_na=False)
        self.d2r = d2r


def count_rule(df):
    """the Standard's 2.1: one claimant's claim under one head arising from one accident, counted once. Rows of one
    accident (policy, car, date) and head count as their distinct claimant numbers, or once where none is numbered;
    each kept claim is its claimant's earliest notification."""
    if not len(df):
        return df
    df = df.sort_values(["note", "claim_ref"])
    key = ["policy_ref", "vrm", "accident_date", "head_of_claim"]
    numbered = df.claimant_no != ""
    has_num = numbered.groupby([df[k] for k in key]).transform("any")
    a = df[numbered].drop_duplicates(key + ["claimant_no"])
    b = df[~has_num].drop_duplicates(key)
    return pd.concat([a, b]).sort_index()


class Golden:
    GROUPINGS = ("pooled", "head", "notified_by", "representative", "route", "route_head", "cmc_rest")

    def __init__(self, target):
        self.B = B = Bundle(target)
        c = B.claims
        pc = c[c["product"] == "PC"].copy()
        self.main = pc[pc.ay.isin(list(K.CLOSED) + [K.OPEN_YEAR])].copy()
        self.main_counted = count_rule(self.main)
        self.pc = pc

    @staticmethod
    def key(df, how):
        if how == "pooled":
            return pd.Series(["all"] * len(df), index=df.index)
        if how == "head":
            return df.head_of_claim
        if how == "notified_by":
            return df.notified_by
        if how == "representative":
            return df.representative_ref.where(df.representative_ref != "", df.notified_by)
        if how == "route":
            return df.route
        if how == "route_head":
            return df.route + "|" + df.head_of_claim
        if how == "cmc_rest":
            return (df.route == "Claims management company").map({True: "CMC", False: "rest"})
        if how == "region":
            return df.region
        raise KeyError(how)

    def position(self, ay, asat=None):
        m = self.main_counted
        asat = asat or dt.date(ay + 1, 9, 30)
        return m[(m.ay == ay) & (m.note <= asat)]

    def final(self, ay):
        m = self.main_counted
        return m[m.ay == ay]

    def factors(self, how, years, simple=False):
        num, den, per = Counter(), Counter(), []
        for ay in years:
            fn = Counter(self.key(self.final(ay), how))
            pn = Counter(self.key(self.position(ay), how))
            num.update(fn)
            den.update(pn)
            per.append((fn, pn))
        if simple:
            out = {}
            for k in num:
                rs = [fn[k] / pn[k] for fn, pn in per if pn.get(k)]
                if rs:
                    out[k] = sum(rs) / len(rs)
            return out
        return {k: num[k] / den[k] for k in num if den.get(k)}

    def develop(self, ay, how, years, simple=False):
        f = self.factors(how, years, simple)
        pos = self.position(ay)
        k = self.key(pos, how)
        est = defaultdict(float)
        for reg, kk in zip(pos.region, k):
            est[reg] += f.get(kk, 1.0)
        return {r: est[r] for r in K.REG}

    def notified(self, ay):
        pos = self.position(ay)
        return {r: int((pos.region == r).sum()) for r in K.REG}

    def backtest(self, how, simple=False):
        y = K.BACKTEST_YEAR
        before = [a for a in K.CLOSED if a < y]
        est = self.develop(y, how, before, simple)
        fin = self.final(y)
        out = {}
        for r in K.REG:
            n = int((fin.region == r).sum())
            out[r] = (est[r], n, 100 * (est[r] / n - 1))
        return out

    def frequency(self, how, years=K.CLOSED, simple=False):
        est = self.develop(K.OPEN_YEAR, how, years, simple)
        return {r: 100 * est[r] / self.B.cy[r] for r in K.REG}, est

    def run(self):
        R = {"cy": {r: self.B.cy[r] for r in K.REG}, "notified": self.notified(K.OPEN_YEAR)}
        R["raw"] = {r: 100 * R["notified"][r] / R["cy"][r] for r in K.REG}
        R["bt"], R["freq"], R["est"] = {}, {}, {}
        for how in self.GROUPINGS + ("region",):
            R["bt"][how] = self.backtest(how)
            R["freq"][how], R["est"][how] = self.frequency(how)
        R["freq"]["route_simple"], _ = self.frequency("route", simple=True)
        R["bt"]["route_simple"] = self.backtest("route", simple=True)
        R["passing"] = [h for h in R["bt"] if max(abs(v[2]) for v in R["bt"][h].values()) <= K.TOLERANCE]
        R["factors_route"] = self.factors("route", K.CLOSED)
        g = R["freq"]["route"]
        order = sorted(K.REG, key=lambda r: -g[r])
        R["call"], R["third"] = order[:2], order[2]
        R["order"] = order
        R["gap"] = g[order[1]] - g[order[2]]
        R["final22"] = {r: R["bt"]["route"][r][1] for r in K.REG}
        R["ask_a"] = self.ask_a()
        return R

    # ------------------------------------------------------------------ the ask: cars on cover on 30 September 2026
    def ask_a(self, apply_changes=True, effective_only=True):
        B = self.B
        v = B.inforce
        snap = K.EXTRACT.isoformat()
        on = v[(v["product"] == "PC") & (v.vehicle_on_cover_from <= snap) &
               ((v.vehicle_off_cover_from == "") | (v.vehicle_off_cover_from > snap)) &
               ((v.cancelled_from == "") | (v.cancelled_from > snap))].copy()
        dist = dict(zip(on.policy_ref, on.risk_postcode_district))
        cov = dict(zip(on.policy_ref, on.cover))
        if apply_changes:
            start = dict(zip(on.policy_ref, on.term_start))
            ch = B.changes[B.changes.policy_ref.isin(set(on.policy_ref)) & B.changes.change_type.isin(["ADDRESS", "COVER"])]
            ch = ch.sort_values(["effective_from", "processed_on", "change_ref"])
            for p, t, eff, nd, nc in zip(ch.policy_ref, ch.change_type, ch.effective_from, ch.new_postcode_district,
                                         ch.new_cover):
                if effective_only and not (start[p] <= eff <= snap):
                    continue
                if t == "ADDRESS":
                    dist[p] = nd
                else:
                    cov[p] = nc
        on["region_now"] = on.policy_ref.map(dist).map(B.d2r)
        on["cover_now"] = on.policy_ref.map(cov)
        return {(r, c): int(((on.region_now == r) & (on.cover_now == c)).sum()) for r in K.REG for c in COVERS}
