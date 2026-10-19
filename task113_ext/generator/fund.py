"""Ledgerpoint's point-in-time quarterly fundamentals and its earnings calendar.

A period reaches the file several times, each row stamped with the date it became known: the press release (the
income statement and per-share figures, a balance sheet in some), the 10-Q or 10-K (the full statements), and for a
few periods a later amendment that restates them. Income statement items are for the quarter; cash flow items are
year to date, as the filings present them; the 10-K row carries the fiscal year, so a fourth quarter's own figures
appear only in its press release. Money is in thousands for most companies and in millions for the larger ones, as
each reports; shares are in thousands throughout; per-share figures are as reported at the time, before any later
split. The calendar logs each announcement's projected and confirmed date and time in UTC."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

import history as H
import universe as U
import world as W

NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")


def lp_ids(secs):
    rng = U.rng_for(9)
    ids = rng.choice(np.arange(100200, 989900), len(secs), replace=False)
    return {s["k"]: "LP%06d" % int(ids[i]) for i, s in enumerate(secs)}


def _S_at(p, d):
    """The cumulative split factor in force on date d (1 before the store begins)."""
    i = U.day_on_or_after(d)
    if i >= U.T:
        i = U.T - 1
    if i < p.i0:
        return 1.0
    if i > p.i1:
        return float(p.S[-1])
    return float(p.S[p.j(i)])


def _econ_shares(s, b, p, d):
    """Economic shares on date d, from the vendor's share counts."""
    i = U.day_on_or_after(d)
    if i < b["i0"]:
        return float(b["shares"][0] / b["S"][0])
    i = min(i, b["i1"])
    j = i - b["i0"]
    return float(b["shares"][j] / b["S"][j])


def build(secs, sched, paths, bars, hist):
    rng = U.rng_for(10)
    ids = lp_ids(secs)
    rows = []
    for s in secs:
        k = s["k"]
        sc = sched[k]
        p, b = paths[k], bars[k]
        per = sc["periods"]
        if not per:
            continue
        pb0 = float(np.exp(rng.normal(np.log(2.1), 0.45)))
        bvps = s["price0"] / pb0
        lev = {6: rng.uniform(8.5, 11.5), 10: rng.uniform(2.0, 2.6), 9: rng.uniform(2.9, 3.5)}.get(
            s["sector"], rng.uniform(1.5, 2.5))
        cash_r = float(rng.uniform(0.04, 0.18))
        debt_r = float(rng.uniform(0.3, 0.62))
        capex_r = float(rng.uniform(0.015, 0.08))
        big = None
        ytd_ocf, ytd_capex, cur_fy = 0.0, 0.0, None
        fy_acc = {}
        for r in per:
            sh = _econ_shares(s, b, p, r["pe"])
            S_k = _S_at(p, r["ann"])
            dil = sh * float(rng.uniform(1.0, 1.025))
            rev = r["rev"] * sh
            ni = r["eps"] * dil
            opi = r["opi"] * sh
            divq = sum(dv["amount"] * float(p.S[p.j(dv["ex"])]) for dv in p.divs
                       if r["pe"] - dt.timedelta(days=92) < U.DAYS[dv["ex"]] <= r["pe"])
            bvps = bvps + r["eps"] - divq
            eq = bvps * sh
            assets = eq * lev * float(np.exp(rng.normal(0, 0.02)))
            if eq <= 0:
                assets = abs(eq) * 1.8 + rev
            liab = assets - eq
            if big is None:
                big = rev * 4 > 2.0e9
            if cur_fy != r["fy"]:
                ytd_ocf, ytd_capex, cur_fy = 0.0, 0.0, r["fy"]
            ytd_ocf += ni * float(rng.uniform(1.05, 1.6)) + rev * float(rng.normal(0, 0.02))
            ytd_capex += -rev * capex_r * float(np.exp(rng.normal(0, 0.15)))
            vals = dict(revenue=rev, operating_income=opi, net_income=ni, total_assets=assets,
                        total_liabilities=liab, total_equity=eq, cash_and_equivalents=assets * cash_r,
                        total_debt=liab * debt_r, operating_cash_flow_ytd=ytd_ocf, capex_ytd=ytd_capex)
            fy_acc.setdefault(r["fy"], []).append((r, vals, dil, S_k))
            ident = _ident(hist, s, r["ann"])
            base = dict(lp_id=ids[k], ticker=ident["ticker"], cusip=ident["cusip"], company_name=ident["name"],
                        fiscal_year=r["fy"], fiscal_quarter=r["q"], period_end=r["pe"], currency="USD",
                        units="millions" if big else "thousands")
            # press release
            pr = dict(base, period_type="Q", source="PRESS_RELEASE", knowledge_date=r["ann"])
            pr.update(_money(vals, big, keep=("revenue", "operating_income", "net_income")))
            if rng.random() < 0.6:
                pr.update(_money(vals, big, keep=("total_assets", "total_liabilities", "total_equity",
                                                  "cash_and_equivalents")))
            pr["eps_diluted"] = round(r["eps"] / S_k, 2)
            pr["shares_diluted"] = int(round(dil * S_k / 1000))
            rows.append(pr)
            # the filing
            fv = dict(vals)
            if rng.random() < 0.04:
                fv["net_income"] = vals["net_income"] * float(rng.uniform(0.98, 1.02))
            ident_f = _ident(hist, s, r["filed"])
            if r["filed"] > W.FUND_PULLED:
                continue
            if r["q"] != 4:
                fq = dict(base, ticker=ident_f["ticker"], cusip=ident_f["cusip"], company_name=ident_f["name"],
                          period_type="Q", source="10-Q", knowledge_date=r["filed"])
                fq.update(_money(fv, big))
                S_f = _S_at(p, r["filed"])
                fq["eps_diluted"] = round(fv["net_income"] / dil / S_f, 2)
                fq["shares_diluted"] = int(round(dil * S_f / 1000))
                rows.append(fq)
                _maybe_restate(rows, fq, fv, dil, p, rng, big)
            else:
                q4 = fy_acc[r["fy"]]
                if len(q4) == 4:
                    S_f = _S_at(p, r["filed"])
                    annual = {kk: sum(v[kk] for _, v, _, _ in q4) for kk in ("revenue", "operating_income",
                                                                           "net_income")}
                    annual.update({kk: fv[kk] for kk in ("total_assets", "total_liabilities", "total_equity",
                                                           "cash_and_equivalents", "total_debt",
                                                           "operating_cash_flow_ytd", "capex_ytd")})
                    annual["net_income"] += fv["net_income"] - vals["net_income"]
                    wsh = float(np.mean([dl for _, _, dl, _ in q4]))
                    fk = dict(base, ticker=ident_f["ticker"], cusip=ident_f["cusip"], company_name=ident_f["name"],
                              fiscal_quarter=None, period_type="FY", source="10-K", knowledge_date=r["filed"])
                    fk.update(_money(annual, big))
                    fk["eps_diluted"] = round(annual["net_income"] / wsh / S_f, 2)
                    fk["shares_diluted"] = int(round(wsh * S_f / 1000))
                    rows.append(fk)
                    _maybe_restate(rows, fk, annual, wsh, p, rng, big)
    for r in rows:
        for kk in ("period_end", "knowledge_date"):
            r[kk] = r[kk].isoformat()
    rows.sort(key=lambda r: (r["knowledge_date"], r["lp_id"], r["period_end"], r["source"]))
    return rows, ids


def _ident(hist, s, d):
    i = U.day_on_or_after(d)
    i = max(i, s["first"])
    if s["last"] is not None:
        i = min(i, s["last"])
    i = min(i, U.T - 1)
    return H.on(hist, s["k"], i)


MONEY = ("revenue", "operating_income", "net_income", "total_assets", "total_liabilities", "total_equity",
         "cash_and_equivalents", "total_debt", "operating_cash_flow_ytd", "capex_ytd")


def _money(vals, big, keep=MONEY):
    out = {}
    for kk in keep:
        v = vals[kk]
        out[kk] = round(v / 1e6, 1) if big else int(round(v / 1e3))
    return out


def _maybe_restate(rows, filed, fv, dil, p, rng, big):
    if rng.random() >= 0.025:
        return
    kd = dt.date.fromisoformat(filed["knowledge_date"]) if isinstance(filed["knowledge_date"], str) else \
        filed["knowledge_date"]
    later = kd + dt.timedelta(days=int(rng.integers(120, 400)))
    if later > W.FUND_PULLED:
        return
    while later.weekday() >= 5:
        later += dt.timedelta(days=1)
    rv = dict(fv)
    rv["revenue"] = fv["revenue"] * float(rng.uniform(0.96, 1.03))
    dn = fv["net_income"] * float(rng.uniform(0.85, 1.08)) - fv["net_income"]
    rv["net_income"] = fv["net_income"] + dn
    rv["total_equity"] = fv["total_equity"] + dn
    rv["total_liabilities"] = fv["total_assets"] - rv["total_equity"]
    a = dict(filed, source=filed["source"] + "/A", knowledge_date=later)
    a.update(_money(rv, big, keep=tuple(k for k in MONEY if filed.get(k) is not None)))
    S_l = _S_at(p, later)
    a["eps_diluted"] = round(rv["net_income"] / dil / S_l, 2)
    a["shares_diluted"] = int(round(dil * S_l / 1000))
    rows.append(a)


def calendar(secs, sched, hist, ids):
    """The earnings calendar's log: a projected date some weeks ahead for most periods, then the confirmed date and
    time; a few confirmed dates moved; the next quarter's dates for companies still listed at the pull."""
    rng = U.rng_for(11)
    out = []
    for s in secs:
        sc = sched[s["k"]]
        for r in sc["periods"]:
            ann_et = dt.datetime.combine(r["ann"], r["time"], tzinfo=NY)
            label = "%dQ%d" % (r["fy"], r["q"])
            ident = _ident(hist, s, r["ann"])
            base = dict(lp_id=ids[s["k"]], ticker=ident["ticker"], company=ident["name"], fiscal_period=label,
                        period_end=r["pe"].isoformat())
            if rng.random() < 0.65:
                guess = r["ann"] + dt.timedelta(days=int(rng.integers(-6, 7)))
                while guess.weekday() >= 5:
                    guess += dt.timedelta(days=1)
                upd = r["ann"] - dt.timedelta(days=int(rng.integers(35, 60)))
                out.append(dict(base, event_utc=_utc(dt.datetime.combine(guess, dt.time(0, 0), tzinfo=NY)),
                                time_code="UNK", status="PROJECTED", updated_utc=_stamp(upd, rng)))
            conf = r["ann"] - dt.timedelta(days=int(rng.integers(8, 26)))
            if rng.random() < 0.02:
                # confirmed for another date first, then moved: the move is the later record
                moved = r["ann"] + dt.timedelta(days=int(rng.choice([-1, 1])) * int(rng.integers(2, 8)))
                while moved.weekday() >= 5:
                    moved += dt.timedelta(days=1)
                out.append(dict(base, event_utc=_utc(dt.datetime.combine(moved, r["time"], tzinfo=NY)),
                                time_code=r["code"], status="CONFIRMED", updated_utc=_stamp(conf, rng)))
                conf = conf + dt.timedelta(days=int(rng.integers(2, 6)))
            out.append(dict(base, event_utc=_utc(ann_et), time_code=r["code"], status="CONFIRMED",
                            updated_utc=_stamp(conf, rng)))
        # the next quarter, for companies listed at the pull
        if s["last"] is None and sc["periods"]:
            last = sc["periods"][-1]
            nxt_pe = (last["pe"] + dt.timedelta(days=100)).replace(day=1) - dt.timedelta(days=1)
            ann = last["ann"] + dt.timedelta(days=91)
            while ann.weekday() >= 5:
                ann += dt.timedelta(days=1)
            if ann > W.FUND_PULLED:
                q = last["q"] % 4 + 1
                fy = last["fy"] + (1 if last["q"] == 4 else 0)
                ident = _ident(hist, s, W.END)
                base = dict(lp_id=ids[s["k"]], ticker=ident["ticker"], company=ident["name"],
                            fiscal_period="%dQ%d" % (fy, q), period_end=nxt_pe.isoformat())
                if rng.random() < 0.45:
                    out.append(dict(base, event_utc=_utc(dt.datetime.combine(ann, last["time"], tzinfo=NY)),
                                    time_code=last["code"], status="CONFIRMED",
                                    updated_utc=_stamp(W.FUND_PULLED - dt.timedelta(days=int(rng.integers(1, 12))),
                                                       rng)))
                else:
                    out.append(dict(base, event_utc=_utc(dt.datetime.combine(ann, dt.time(0, 0), tzinfo=NY)),
                                    time_code="UNK", status="PROJECTED",
                                    updated_utc=_stamp(W.FUND_PULLED - dt.timedelta(days=int(rng.integers(5, 30))),
                                                       rng)))
    out.sort(key=lambda r: (r["updated_utc"], r["lp_id"], r["fiscal_period"]))
    return out


def _utc(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp(d, rng):
    return dt.datetime(d.year, d.month, d.day, int(rng.integers(9, 23)), int(rng.integers(0, 60)),
                       int(rng.integers(0, 60))).strftime("%Y-%m-%dT%H:%M:%SZ")
