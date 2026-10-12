"""Computes every graded figure of task501 from the shipped files alone (pandas). Shared by the generator's
assertions and by the golden; the independent verifier in ../verify_pack.py shares nothing with this file."""
import os
from datetime import date, timedelta

import pandas as pd
import numpy as np
import openpyxl

T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
PLAN_DATE = date(2026, 9, 30)
FACILITY_MONTHS = [(2027, m) for m in range(1, 13)]
FORWARD_MONTHS = [(2026, 10), (2026, 11), (2026, 12)] + FACILITY_MONTHS
RESERVE = 75_000_000.0
TRANCHES = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300]
BANDS = [(1, 12), (13, 24), (25, 36), (37, 54), (55, 78), (79, 10_000)]
RATE_WINDOW = ((2019, 1), (2026, 9))
DIST_WINDOW = ((2022, 1), (2026, 9))
HAIRCUT = 0.25


def add_months(d, n):
    y, m = d.year, d.month + n
    y += (m - 1) // 12
    m = (m - 1) % 12 + 1
    last = (date(y + (m == 12), 1 if m == 12 else m + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, last))


def band(age):
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= age <= hi:
            return i
    return len(BANDS) - 1


def mi(y, m):
    return y * 12 + m - 1


class Pack:
    def __init__(self, root=T):
        self.root = root
        sp = pd.read_csv(os.path.join(root, "kapitalabrufe_ausschuettungen_2015-2026.csv"), dtype={"investment_ref": str, "remarks": str}, keep_default_na=False)
        sp["notice_date"] = pd.to_datetime(sp["notice_date"]).dt.date
        sp["value_date"] = pd.to_datetime(sp["value_date"]).dt.date
        sp["amount"] = sp["amount"].astype(float)
        sp["currency"] = sp["currency"].str.upper().str.strip()
        self.spine = sp
        self.issued = sp[sp["status"] == "ISSUED"].copy()
        reg = pd.read_excel(os.path.join(root, "fondsregister_2026-09-30.xlsx"), sheet_name="Fonds")
        for c in ("first_close", "final_close", "admission_date", "investment_period_end", "term_end"):
            reg[c] = pd.to_datetime(reg[c]).dt.date
        self.reg = reg.set_index("fund_id")
        inv = pd.read_csv(os.path.join(root, "beteiligungsverzeichnis_2026-09-30.csv"), keep_default_na=False)
        inv["initial_investment_date"] = pd.to_datetime(inv["initial_investment_date"]).dt.date
        inv["realisation_date"] = pd.to_datetime(inv["realisation_date"].replace("", None)).dt.date
        self.inv = inv
        aud = pd.read_excel(os.path.join(root, "kapitalkonten_revidiert_2021-2025.xlsx"), sheet_name="Kapitalkonten")
        aud["fy_end"] = pd.to_datetime(aud["fy_end"]).dt.date
        self.aud = aud
        nav = pd.read_csv(os.path.join(root, "nav_register_quartal.csv"), keep_default_na=False)
        for c in ("period_end", "received_date", "booking_date"):
            nav[c] = pd.to_datetime(nav[c]).dt.date
        self.nav = nav
        fx = pd.read_csv(os.path.join(root, "fx_referenzkurse_tagesende.csv"))
        fx["rate_date"] = pd.to_datetime(fx["rate_date"]).dt.date
        self.fx = fx.set_index("rate_date")
        self.fx_days = sorted(self.fx.index)
        # first call month per fund
        calls = self.issued[self.issued["notice_type"] == "CAPITAL_CALL"]
        self.first_call = calls.groupby("fund_id")["notice_date"].min().to_dict()

    def fx_rate(self, d, ccy):
        if ccy == "CHF":
            return 1.0
        while d not in self.fx.index:
            d -= timedelta(days=1)
        return float(self.fx.loc[d, "USDCHF" if ccy == "USD" else "EURCHF"])

    # ------------------------------------------------------------ building blocks
    def age(self, fund_id, y, m):
        fc = self.first_call.get(fund_id)
        if fc is None:
            fc = date(2026, 10, 1)       # policy: a fund without a first call is aged from October 2026
        return mi(y, m) - mi(fc.year, fc.month) + 1

    def call_rates(self, window=RATE_WINDOW, age_basis="first_call", fx_date=PLAN_DATE):
        """Pooled monthly call rate by strategy and age band: the sum of calls over the sum of commitments across the
        fund-months of the window, both translated at the plan-date rate (the policy's definition)."""
        calls = self.issued[self.issued["notice_type"] == "CAPITAL_CALL"].copy()
        calls["ym"] = calls["notice_date"].map(lambda d: mi(d.year, d.month))
        byfm = calls.groupby(["fund_id", "ym"])["amount"].sum().to_dict()
        lo, hi = mi(*window[0]), mi(*window[1])
        num, den, cnt = {}, {}, {}
        for fid, r in self.reg.iterrows():
            fc = self.first_call.get(fid)
            if fc is None:
                continue
            fxr = self.fx_rate(fx_date, r["currency"])
            start = mi(fc.year, fc.month)
            for ym in range(max(lo, start), hi + 1):
                a = (ym - start + 1) if age_basis == "first_call" else (ym - mi(r["first_close"].year, r["first_close"].month) + 1)
                key = (r["strategy"], band(max(a, 1)))
                num[key] = num.get(key, 0.0) + byfm.get((fid, ym), 0.0) * fxr
                den[key] = den.get(key, 0.0) + r["commitment"] * fxr
                cnt[key] = cnt.get(key, 0) + 1
        return {k: num[k] / den[k] for k in num}, cnt

    def audited_nav(self, fund_id, fy_year):
        a = self.aud[(self.aud["fund_id"] == fund_id) & (self.aud["fy_end"] == date(fy_year, 12, 31))]
        return float(a["nav_fy_end"].iloc[0]) if len(a) else None

    def dist_rates(self, window=DIST_WINDOW, fx_date=PLAN_DATE):
        """Pooled monthly distribution rate by strategy and age band: distributions over the fund's audited NAV at the
        preceding year-end, summed across the fund-months of the window at the plan-date rate."""
        dists = self.issued[self.issued["notice_type"] == "DISTRIBUTION"].copy()
        dists["ym"] = dists["notice_date"].map(lambda d: mi(d.year, d.month))
        byfm = dists.groupby(["fund_id", "ym"])["amount"].sum().to_dict()
        lo, hi = mi(*window[0]), mi(*window[1])
        num, den, cnt = {}, {}, {}
        for fid, r in self.reg.iterrows():
            fc = self.first_call.get(fid)
            if fc is None:
                continue
            fxr = self.fx_rate(fx_date, r["currency"])
            start = mi(fc.year, fc.month)
            for ym in range(max(lo, start), hi + 1):
                y = ym // 12
                nav = self.audited_nav(fid, y - 1)
                if not nav:
                    continue
                key = (r["strategy"], band(ym - start + 1))
                num[key] = num.get(key, 0.0) + byfm.get((fid, ym), 0.0) * fxr
                den[key] = den.get(key, 0.0) + nav * fxr
                cnt[key] = cnt.get(key, 0) + 1
        return {k: num[k] / den[k] for k in num}, cnt

    def calls_to(self, fund_id, upto=PLAN_DATE, since=None):
        c = self.issued[(self.issued["notice_type"] == "CAPITAL_CALL") & (self.issued["fund_id"] == fund_id) & (self.issued["notice_date"] <= upto)]
        if since is not None:
            c = c[c["notice_date"] >= since]
        return float(c["amount"].sum())

    def recallable(self, fund_id, upto=PLAN_DATE, since=None, months=18, lines=("RETURN_OF_CAPITAL",), ip_limb=True, anchor="initial"):
        d = self.issued[(self.issued["notice_type"] == "DISTRIBUTION") & (self.issued["fund_id"] == fund_id) & (self.issued["notice_date"] <= upto) & (self.issued["line_type"].isin(lines))]
        if since is not None:
            d = d[d["notice_date"] >= since]
        if months is None:
            return float(d["amount"].sum())
        inv = self.inv[self.inv["fund_id"] == fund_id].set_index("investment_ref")
        ip_end = self.reg.loc[fund_id, "investment_period_end"]
        if anchor == "last_tranche":
            tr = self.issued[(self.issued["notice_type"] == "CAPITAL_CALL") & (self.issued["fund_id"] == fund_id) & (self.issued["line_type"] == "INVESTMENT")]
            last_tr = tr.groupby("investment_ref")["value_date"].max().to_dict()
        total = 0.0
        for _, row in d.iterrows():
            ref = row["investment_ref"]
            if ref not in inv.index:
                continue
            init = inv.loc[ref, "initial_investment_date"] if anchor == "initial" else last_tr.get(ref, inv.loc[ref, "initial_investment_date"])
            real = inv.loc[ref, "realisation_date"]
            if pd.isna(real):
                continue
            if real <= add_months(init, months) and (not ip_limb or row["notice_date"] <= ip_end):
                total += row["amount"]
        return float(total)

    def unfunded(self, fund_id, construction="true", **kw):
        C = float(self.reg.loc[fund_id, "commitment"])
        if construction == "naive":
            return C - self.calls_to(fund_id)
        if construction == "true":
            return C - self.calls_to(fund_id) + self.recallable(fund_id, **kw)
        if construction == "naive_plus_rule":
            return C - self.calls_to(fund_id) + self.recallable(fund_id, **kw)
        aud = self.aud[(self.aud["fund_id"] == fund_id) & (self.aud["fy_end"] == date(2025, 12, 31))]
        base = float(aud["unfunded_commitment"].iloc[0]) if len(aud) else C
        if construction == "audited_as_is":
            return base
        y26 = date(2026, 1, 1)
        if construction == "audited_rf":
            return base - self.calls_to(fund_id, since=y26)
        if construction == "audited_rf_rule":
            return base - self.calls_to(fund_id, since=y26) + self.recallable(fund_id, since=y26, **kw)
        raise ValueError(construction)

    # ------------------------------------------------------------ the plan
    def plan(self, construction="true", rate_window=RATE_WINDOW, age_basis="first_call", haircut=HAIRCUT, nav_basis="audited",
             cum_from=(2027, 1), fx_date=PLAN_DATE, reserve=RESERVE, **kw):
        cr, _ = self.call_rates(rate_window, age_basis)
        dr, _ = self.dist_rates()
        funds = [fid for fid, r in self.reg.iterrows()]
        U = {}
        for fid in funds:
            if construction in ("true", "audited_rf_rule"):
                U[fid] = max(0.0, self.unfunded(fid, construction, **kw))
            else:
                U[fid] = max(0.0, self.unfunded(fid, construction))
        navs = {}
        for fid in funds:
            if nav_basis == "audited":
                navs[fid] = self.audited_nav(fid, 2025) or 0.0
            else:
                n = self.nav[(self.nav["fund_id"] == fid) & (self.nav["period_end"] == date(2026, 6, 30))]
                navs[fid] = float(n["nav_fund_ccy"].iloc[0]) if len(n) else (self.audited_nav(fid, 2025) or 0.0)
        rows = []
        fund_rows = []
        for (y, m) in FORWARD_MONTHS:
            tc = td = 0.0
            per_strat = {}
            for fid in funds:
                r = self.reg.loc[fid]
                a = self.age(fid, y, m) if age_basis == "first_call" else (mi(y, m) - mi(r["first_close"].year, r["first_close"].month) + 1)
                b = band(max(a, 1))
                rate = cr.get((r["strategy"], b), 0.0)
                call = min(rate * float(r["commitment"]), U[fid])
                U[fid] -= call
                dist = dr.get((r["strategy"], b), 0.0) * navs[fid]
                fxr = self.fx_rate(fx_date, r["currency"])
                tc += call * fxr
                td += dist * fxr
                s = per_strat.setdefault(r["strategy"], [0.0, 0.0])
                s[0] += call * fxr
                s[1] += dist * fxr
                fund_rows.append((y, m, fid, call * fxr, dist * fxr))
            rows.append(dict(year=y, month=m, calls=tc, dists=td, credited=haircut * td, net=tc - haircut * td, by_strategy=per_strat))
        cum = 0.0
        for row in rows:
            if (row["year"], row["month"]) >= cum_from:
                cum += row["net"]
            row["cum"] = cum if (row["year"], row["month"]) >= cum_from else 0.0
        fac = [r for r in rows if (r["year"], r["month"]) in FACILITY_MONTHS]
        peak = max(r["cum"] for r in fac)
        peak_month = max(fac, key=lambda r: r["cum"])
        required = peak - reserve
        tranche = next((t for t in TRANCHES if t * 1e6 >= required), None)
        below = TRANCHES[TRANCHES.index(tranche) - 1] if tranche and TRANCHES.index(tranche) > 0 else None
        first_past_below = next(((r["year"], r["month"]) for r in fac if below is not None and r["cum"] - reserve > below * 1e6), None)
        return dict(rows=rows, facility=fac, peak=peak, peak_month=(peak_month["year"], peak_month["month"]), required=required,
                    tranche=tranche, below=below, uncovered_below=(required - below * 1e6) if below else None,
                    first_past_below=first_past_below, call_rates=cr, dist_rates=dr, unfunded=U, fund_rows=fund_rows)

    # ------------------------------------------------------------ ask B: NAV bridge by strategy
    def nav_bridge(self, start=date(2025, 12, 31), end=date(2026, 6, 30), fx_basis="period_end", absent="adjust", flow_date="value_date"):
        out = {}
        for fid, r in self.reg.iterrows():
            s = r["strategy"]
            d = out.setdefault(s, dict(opening=0.0, calls=0.0, dists=0.0, closing=0.0))
            ccy = r["currency"]
            # opening
            n0 = self.nav[(self.nav["fund_id"] == fid) & (self.nav["period_end"] == start)]
            if len(n0):
                d["opening"] += float(n0["nav_fund_ccy"].iloc[0]) * (self.fx_rate(start, ccy) if fx_basis == "period_end" else 1.0) if fx_basis == "period_end" else float(n0["nav_chf_booked"].iloc[0])
            # flows
            col = flow_date
            fl = self.issued[(self.issued["fund_id"] == fid) & (self.issued[col] > start) & (self.issued[col] <= end)]
            for _, row in fl.iterrows():
                fxr = self.fx_rate(row["value_date"], ccy)
                if row["notice_type"] == "CAPITAL_CALL":
                    d["calls"] += row["amount"] * fxr
                else:
                    d["dists"] += row["amount"] * fxr
            # closing
            n1 = self.nav[(self.nav["fund_id"] == fid) & (self.nav["period_end"] == end)]
            if len(n1):
                d["closing"] += float(n1["nav_fund_ccy"].iloc[0]) * self.fx_rate(end, ccy) if fx_basis == "period_end" else float(n1["nav_chf_booked"].iloc[0])
            else:
                if absent == "skip":
                    continue
                prev = self.nav[(self.nav["fund_id"] == fid) & (self.nav["period_end"] < end)].sort_values("period_end")
                if not len(prev):
                    continue
                pe = prev["period_end"].iloc[-1]
                base = float(prev["nav_fund_ccy"].iloc[-1])
                if absent == "adjust":
                    fl2 = self.issued[(self.issued["fund_id"] == fid) & (self.issued["value_date"] > pe) & (self.issued["value_date"] <= end)]
                    base += float(fl2[fl2["notice_type"] == "CAPITAL_CALL"]["amount"].sum()) - float(fl2[fl2["notice_type"] == "DISTRIBUTION"]["amount"].sum())
                d["closing"] += base * (self.fx_rate(end, ccy) if fx_basis == "period_end" else float(prev["fx_rate_booked"].iloc[-1]))
        for s, d in out.items():
            d["valuation_fx"] = d["closing"] - d["opening"] - d["calls"] + d["dists"]
        tot = dict(opening=sum(d["opening"] for d in out.values()), calls=sum(d["calls"] for d in out.values()), dists=sum(d["dists"] for d in out.values()), closing=sum(d["closing"] for d in out.values()))
        tot["valuation_fx"] = tot["closing"] - tot["opening"] - tot["calls"] + tot["dists"]
        out["TOTAL"] = tot
        return out

    # ------------------------------------------------------------ ask C: 2026 cash by month
    def cash_2026(self, date_col="value_date", fx_col="value_date", cash_only=True, include_cancelled=False):
        sp = self.spine if include_cancelled else self.issued
        sp = sp[(sp[date_col] >= date(2026, 1, 1)) & (sp[date_col] <= date(2026, 9, 30))]
        if cash_only:
            sp = sp[sp["line_type"] != "IN_KIND"]
        out = {m: dict(calls=0.0, dists=0.0) for m in range(1, 10)}
        by_strat = {}
        for _, row in sp.iterrows():
            ccy = self.reg.loc[row["fund_id"], "currency"]
            fxr = self.fx_rate(row[fx_col], ccy)
            m = row[date_col].month
            k = "calls" if row["notice_type"] == "CAPITAL_CALL" else "dists"
            out[m][k] += row["amount"] * fxr
            s = by_strat.setdefault(self.reg.loc[row["fund_id"], "strategy"], dict(calls=0.0, dists=0.0))
            s[k] += row["amount"] * fxr
        for m in out:
            out[m]["net"] = out[m]["calls"] - out[m]["dists"]
        for s in by_strat.values():
            s["net"] = s["calls"] - s["dists"]
        return out, by_strat


# ====================================================================== validation layer (re-root 2026-10-11)
ORIGINS = [(2022, 12), (2023, 3), (2023, 6), (2023, 9), (2023, 12), (2024, 3), (2024, 6), (2024, 9), (2024, 12), (2025, 3), (2025, 6), (2025, 9)]
HORIZON = 12
CANDIDATES = ("band", "strategy_band", "fund_own")


def _ym_to_date_end(ym):
    y, m = divmod(ym, 12)
    m += 1
    nxt = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return nxt - timedelta(days=1)


class Validation:
    """Walk-forward test of the candidate pacing bases, as RL-PM-04 s.5 files it, plus the leaky variants a solver
    takes when it fits once on the whole window."""

    def __init__(self, pack):
        self.p = pack
        p = pack
        calls = p.issued[p.issued["notice_type"] == "CAPITAL_CALL"].copy()
        calls["ym"] = calls["notice_date"].map(lambda d: mi(d.year, d.month))
        self.byfm = calls.groupby(["fund_id", "ym"])["amount"].sum().to_dict()
        self.first = {fid: mi(d.year, d.month) for fid, d in p.first_call.items()}
        self.reg = p.reg
        self._unf_cache = {}

    def unfunded_at(self, fid, origin_ym):
        key = (fid, origin_ym)
        if key not in self._unf_cache:
            d = _ym_to_date_end(origin_ym)
            self._unf_cache[key] = max(0.0, self.p.unfunded(fid, "true", upto=d) if False else self.p.reg.loc[fid, "commitment"] - self.p.calls_to(fid, upto=d) + self.p.recallable(fid, upto=d))
        return self._unf_cache[key]

    def age(self, fid, ym, origin_ym):
        start = self.first.get(fid)
        if start is None or start > origin_ym:
            start = origin_ym + 1               # a fund without a call at the origin is aged from the month after it
        return ym - start + 1

    def fund_rates(self, fit_end):
        """Each fund's own monthly call rate by age band over its fund-months to fit_end (calls over commitment)."""
        out = {}
        for fid, r in self.reg.iterrows():
            start = self.first.get(fid)
            if start is None or start > fit_end:
                continue
            num, cnt = {}, {}
            for ym in range(start, fit_end + 1):
                b = band(ym - start + 1)
                num[b] = num.get(b, 0.0) + self.byfm.get((fid, ym), 0.0) / float(r["commitment"])
                cnt[b] = cnt.get(b, 0) + 1
            out[fid] = {b: num[b] / cnt[b] for b in num}
        return out

    def pooled(self, origin_ym, kind, fit_end=None):
        """Pooled monthly call rates from Jan 2019 to fit_end (default the origin), ratio of sums at the origin rate."""
        fit_end = origin_ym if fit_end is None else fit_end
        fxd = _ym_to_date_end(origin_ym)
        num, den = {}, {}
        lo = mi(2019, 1)
        for fid, r in self.reg.iterrows():
            start = self.first.get(fid)
            if start is None or start > fit_end:
                continue
            f = self.p.fx_rate(fxd, r["currency"])
            for ym in range(max(lo, start), fit_end + 1):
                b = band(ym - start + 1)
                key = (r["strategy"], b) if kind == "strategy_band" else b
                num[key] = num.get(key, 0.0) + self.byfm.get((fid, ym), 0.0) * f
                den[key] = den.get(key, 0.0) + r["commitment"] * f
        return {k: num[k] / den[k] for k in num}

    def forecast(self, origin_ym, kind, rates=None, horizon=HORIZON):
        """Programme calls over the horizon after the origin, CHF at the origin rate, per candidate."""
        fxd = _ym_to_date_end(origin_ym)
        total = 0.0
        monthly = []
        U = {}
        for fid, r in self.reg.iterrows():
            if r["admission_date"] > fxd:
                continue
            U[fid] = self.unfunded_at(fid, origin_ym)
        for k in range(1, horizon + 1):
            ym = origin_ym + k
            tc = 0.0
            for fid in U:
                r = self.reg.loc[fid]
                if kind == "trailing":
                    tr = sum(self.byfm.get((fid, y), 0.0) for y in range(origin_ym - 11, origin_ym + 1)) / 12.0
                    call = min(tr, U[fid])
                elif kind == "fund_own":
                    b = band(max(1, self.age(fid, ym, origin_ym)))
                    own = rates.get(fid)
                    if own:
                        rate = own[b] if b in own else own[max(own)]        # a band not yet reached carries the fund's latest band
                    else:
                        rate = rates["_strategy_band"].get((r["strategy"], b), 0.0)   # a fund with no record carries its strategy band
                    call = min(rate * float(r["commitment"]), U[fid])
                else:
                    b = band(max(1, self.age(fid, ym, origin_ym)))
                    key = (r["strategy"], b) if kind == "strategy_band" else b
                    call = min(rates.get(key, 0.0) * float(r["commitment"]), U[fid])
                U[fid] -= call
                tc += call * self.p.fx_rate(fxd, r["currency"])
            monthly.append(tc)
            total += tc
        return total, monthly

    def realised_monthly(self, origin_ym, horizon=HORIZON):
        fxd = _ym_to_date_end(origin_ym)
        out = [0.0] * horizon
        for fid, r in self.reg.iterrows():
            if r["admission_date"] > fxd:
                continue
            f = self.p.fx_rate(fxd, r["currency"])
            for k in range(1, horizon + 1):
                out[k - 1] += self.byfm.get((fid, origin_ym + k), 0.0) * f
        return out

    def realised(self, origin_ym, horizon=HORIZON):
        """Realised calls of the funds in the register at the origin, the same population the forecast covers."""
        fxd = _ym_to_date_end(origin_ym)
        tot = 0.0
        for fid, r in self.reg.iterrows():
            if r["admission_date"] > fxd:
                continue
            f = self.p.fx_rate(fxd, r["currency"])
            for k in range(1, horizon + 1):
                tot += self.byfm.get((fid, origin_ym + k), 0.0) * f
        return tot

    def run(self, mode="walk_forward"):
        """mode: walk_forward (rates re-estimated at each origin from prior data), full_window (rates fitted once on
        Jan 2019 to Sep 2026 and applied to every origin), in_sample (rates fitted on data to the end of each
        origin's horizon)."""
        out = {c: [] for c in CANDIDATES}
        paths = {c: [] for c in CANDIDATES}
        totals = {c: [] for c in CANDIDATES}
        actual = []
        for (y, m) in ORIGINS:
            o = mi(y, m)
            A = self.realised(o)
            actual.append(A)
            real_m = self.realised_monthly(o)
            fit_end = {"walk_forward": o, "walk_forward_exclusive": o - 1, "full_window": mi(2026, 9), "in_sample": o + HORIZON}[mode]
            for c in CANDIDATES:
                if c == "fund_own":
                    rates = self.fund_rates(fit_end)
                    rates["_strategy_band"] = self.pooled(o, "strategy_band", fit_end=fit_end)
                    F, monthly = self.forecast(o, c, rates)
                else:
                    F, monthly = self.forecast(o, c, self.pooled(o, c, fit_end=fit_end))
                out[c].append(F)
                cf = ca = 0.0
                gaps = []
                for a, fm in zip(real_m, monthly):
                    cf += fm
                    ca += a
                    gaps.append(ca - cf)
                paths[c].append(max(0.0, max(gaps)))
                totals[c].append(max(0.0, gaps[-1]))
        res = {}
        for c in CANDIDATES:
            errs = [abs(F - A) / A for F, A in zip(out[c], actual)]
            res[c] = dict(forecasts=out[c], mape=sum(errs) / len(errs), path_gaps=paths[c], total_gaps=totals[c],
                          buffer=max(paths[c]), buffer_total=max(totals[c]))
        winner = min(CANDIDATES, key=lambda c: (res[c]["mape"], {"trailing": 0, "band": 1, "strategy_band": 2, "fund_own": 3}[c]))
        return dict(actual=actual, candidates=res, winner=winner, mode=mode)


    def plan_calls(self, basis, fit_end=None):
        """Monthly 2026-10 to 2027-12 programme calls (CHF at the plan-date rate) under a candidate basis, rates from the
        record to fit_end (default the plan date)."""
        o = mi(2026, 9)
        fit_end = o if fit_end is None else fit_end
        if basis == "trailing":
            _, monthly = self.forecast(o, basis, horizon=15)
        elif basis == "fund_own":
            rates = self.fund_rates(fit_end)
            rates["_strategy_band"] = self.pooled(o, "strategy_band", fit_end=fit_end)
            _, monthly = self.forecast(o, basis, rates, horizon=15)
        else:
            _, monthly = self.forecast(o, basis, self.pooled(o, basis, fit_end=fit_end), horizon=15)
        return monthly


def facility(pack, val, basis, buffer_amount, reserve=RESERVE, haircut=HAIRCUT):
    """The plan under a basis: calls from the candidate, distributions as RL-PM-04 s.5.3, cumulative from January 2027,
    required = peak + buffer_share x 2027 expected calls - reserve."""
    base = pack.plan("true", haircut=haircut, reserve=reserve)      # distributions and furniture
    calls = val.plan_calls(basis)
    rows = []
    for r, c in zip(base["rows"], calls):
        rows.append(dict(year=r["year"], month=r["month"], calls=c, dists=r["dists"], credited=r["credited"], net=c - r["credited"]))
    cum = 0.0
    for r in rows:
        if r["year"] == 2027:
            cum += r["net"]
        r["cum"] = cum if r["year"] == 2027 else 0.0
    fac = [r for r in rows if r["year"] == 2027]
    peak = max(r["cum"] for r in fac)
    calls27 = sum(r["calls"] for r in fac)
    buffer = float(buffer_amount)
    required = peak + buffer - reserve
    tranche = next((t for t in TRANCHES if t * 1e6 >= required), None)
    below = TRANCHES[TRANCHES.index(tranche) - 1] if tranche else None
    first_past = next(((r["year"], r["month"]) for r in fac if below is not None and r["cum"] + buffer - reserve > below * 1e6), None)
    return dict(rows=rows, facility=fac, peak=peak, calls27=calls27, buffer=buffer, buffer_share=buffer / calls27, required=required,
                tranche=tranche, below=below, uncovered_below=(required - below * 1e6) if below else None, first_past_below=first_past,
                peak_month=max(fac, key=lambda r: r["cum"])["month"])


def main_call(pack, val):
    """The directive's own path: walk-forward selection, the largest miss as buffer, the plan on the selected basis."""
    wf = val.run("walk_forward")
    w = wf["winner"]
    return facility(pack, val, w, wf["candidates"][w]["buffer"]), wf
