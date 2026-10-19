"""The benchmark (Northcote US Small Cap Select: its June reconstitutions, interim changes and daily levels), the
exchanges' semi-monthly short interest, the custodian's sweep rate, and the live book's orders and executions."""
import datetime as dt
import math
from zoneinfo import ZoneInfo

import numpy as np

import calendar_us as C
import history as H
import universe as U
import world as W

NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
N_INDEX = 80


def _alive(s, i):
    return s["first"] <= i and (s["last"] is None or i <= s["last"])


def _fourth_friday_june(y):
    d = C.nth_weekday(y, 6, 4, 4)
    while d not in U.DIDX:
        d -= dt.timedelta(days=1)
    return U.DIDX[d]


def _last_trading_day(y, m):
    d = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    while d not in U.DIDX:
        d -= dt.timedelta(days=1)
    return U.DIDX[d]


def _third_friday(y, m):
    d = C.nth_weekday(y, m, 4, 3)
    while d not in U.DIDX:
        d -= dt.timedelta(days=1)
    return U.DIDX[d]


# ------------------------------------------------------------------------------------------------ the benchmark
def index(secs, bars, hist):
    """Constituents: the 80 largest eligible companies with a total capitalisation between $300 million and $7.5
    billion on the last trading day of May, effective after the close of the fourth Friday of June. Index shares are
    float shares scaled so no constituent weighs more than 4 per cent at the reconstitution, and stay fixed until
    the next one except for splits; IPOs join at the quarterly addition dates, a constituent's spin-off joins on its
    ex-day, and a constituent leaves after its last trade."""
    rng = U.rng_for(12)
    ff = {s["k"]: s["float_factor"] for s in secs}
    LO, HI, CAP = 3.0e8, 7.5e9, 0.04

    def px(k, i):
        b = bars[k]
        return float(b["close"][i - b["i0"]])

    def cap(k, i):
        b = bars[k]
        j = i - b["i0"]
        return float(b["close"][j]) * float(b["shares"][j])

    def float_shares(k, i):
        b = bars[k]
        return float(b["shares"][i - b["i0"]]) * ff[k]

    def capped(ks, i):
        q = {k: float_shares(k, i) for k in ks}
        for _ in range(20):
            mv = {k: q[k] * px(k, i) for k in ks}
            tot = sum(mv.values())
            over = [k for k in ks if mv[k] / tot > CAP + 1e-9]
            if not over:
                break
            for k in over:
                q[k] *= CAP * tot / mv[k] * 0.999
        return q

    def select(i, rank_i):
        elig = [s for s in secs if _alive(s, rank_i) and _alive(s, i) and
                (s["first"] <= rank_i - 60 or s["kind"] == "initial") and
                px(s["k"], rank_i) >= 1.0 and LO <= cap(s["k"], rank_i) <= HI]
        return [s["k"] for s in sorted(elig, key=lambda s: -cap(s["k"], rank_i))[:80]]

    base = select(0, 0)
    q = {k: float(round(v)) for k, v in capped(base, 0).items()}
    cfac = {k: q[k] / float_shares(k, 0) for k in base}
    recons = [dict(label="Jun2017", eff=None, rank=None, day=0, q=dict(q), cfac=dict(cfac))]
    changes = []
    recon_days = {_fourth_friday_june(y): y for y in range(2018, 2027)}
    rank_days = {y: _last_trading_day(y, 5) for y in range(2018, 2027)}
    ipo_days = {_third_friday(y, m) for y in range(2018, 2027) for m in (3, 9, 12) if _third_friday(y, m) < U.T}
    levels = []
    lvl_pr, lvl_tr = 1873.42, 2311.07
    for i in range(U.T):
        if i > 0:
            num_p = num_t = den = 0.0
            for k, qk in list(q.items()):
                b = bars[k]
                j = i - b["i0"]
                prev = float(b["close"][j - 1])
                den += qk * prev
                num_p += qk * prev * ((b["close"][j] * b["F"][j] + b["V"][j]) / prev)
                num_t += qk * prev * (1 + float(b["ret"][j]))
                if b["F"][j] != 1.0:
                    q[k] = qk * float(b["F"][j])
            lvl_pr *= num_p / den
            lvl_tr *= num_t / den
        for k in sorted(q):
            s = secs[k]
            if s["last"] is not None and s["last"] == i:
                del q[k]
                sp = H.on(hist, k, i)
                changes.append(dict(date=U.DAYS[i], action="DELETE", k=k, name=sp["name"], ticker=sp["ticker"],
                                    cusip=sp["cusip"], reason={"cause": "Delisted", "cash": "Acquired",
                                                                "stock": "Acquired", "private": "Acquired"}[s["fate"]]))
        for s in secs:
            if s["kind"] == "spin" and s["first"] == i and s["parent"] in q:
                q[s["k"]] = float(round(float_shares(s["k"], i)))
                sp = H.on(hist, s["k"], i)
                changes.append(dict(date=U.DAYS[i], action="ADD", k=s["k"], name=sp["name"], ticker=sp["ticker"],
                                    cusip=sp["cusip"], reason="Spin-off of a constituent", shares=int(q[s["k"]])))
        if i in ipo_days and q:
            for s in secs:
                k = s["k"]
                if s["kind"] == "ipo" and k not in q and _alive(s, i) and s["first"] + 20 <= i and \
                        s["first"] > i - 70 and LO <= cap(k, i) <= HI:
                    q[k] = float(round(float_shares(k, i)))
                    sp = H.on(hist, k, i)
                    changes.append(dict(date=U.DAYS[i], action="ADD", k=k, name=sp["name"], ticker=sp["ticker"],
                                        cusip=sp["cusip"], reason="IPO addition", shares=int(q[k])))
        if i in recon_days:
            y = recon_days[i]
            rd = rank_days[y]
            for k in ff:
                ff[k] = float(np.clip(ff[k] + rng.normal(0, 0.015), 0.5, 1.0))
            ks = select(i, rd)
            q = {k: float(round(v)) for k, v in capped(ks, i).items()}
            cfac = {k: q[k] / float_shares(k, i) for k in ks}
            recons.append(dict(label="Jun%d" % y, eff=U.DAYS[i], rank=U.DAYS[rd], day=i, q=dict(q), cfac=dict(cfac)))
        mcap = sum(qk * px(k, i) for k, qk in q.items())
        levels.append(dict(date=U.DAYS[i], pr=round(float(lvl_pr), 2), tr=round(float(lvl_tr), 2), n=len(q),
                           mcap=round(mcap / 1e6, 1)))
    recon_rows = []
    for rc in recons:
        i = rc["day"]
        tot = sum(qk * px(k, i) for k, qk in rc["q"].items())
        rows = []
        for k, qk in rc["q"].items():
            sp = H.on(hist, k, i)
            rows.append(dict(name=sp["name"], ticker=sp["ticker"], cusip=sp["cusip"],
                             sector=W.SECTORS[sp["sector"]][1], close=px(k, i), shares_in_index=int(round(qk)),
                             float_factor=round(ff[k], 3), capping_factor=round(rc["cfac"][k], 6),
                             mcap=round(qk * px(k, i), 0), weight=round(100 * qk * px(k, i) / tot, 4)))
        rows.sort(key=lambda r: -r["weight"])
        recon_rows.append(dict(rc, rows=rows))
    return recon_rows, changes, levels


# ------------------------------------------------------------------------------------------------ short interest
def settlement_days():
    out = []
    for y in range(2018, 2027):
        for m in range(1, 13):
            d = dt.date(y, m, 15)
            while d not in U.DIDX and d >= W.START:
                d -= dt.timedelta(days=1)
            if W.START <= d <= W.END:
                out.append(U.DIDX[d])
            e = _last_trading_day(y, m) if dt.date(y, m, 1) <= W.END else None
            if e is not None and e < U.T and U.DAYS[e] <= W.END:
                out.append(e)
    return sorted(set(out))


def short_interest(secs, bars, hist):
    rng = U.rng_for(13)
    days = settlement_days()
    level = {}
    prev = {}
    rows = []
    mean = {s["k"]: float(np.clip(np.exp(rng.normal(np.log(0.045), 0.6)), 0.006, 0.22)) for s in secs}
    pubs = {}
    for n, i in enumerate(days):
        pub_i = i + 7
        pub = U.DAYS[pub_i] if pub_i < U.T else _add_bdays(U.DAYS[-1], pub_i - U.T + 1)
        if pub > W.SI_LAST_PUB:
            break
        pubs[i] = pub
        for s in secs:
            if not _alive(s, i):
                continue
            k = s["k"]
            b = bars[k]
            j = i - b["i0"]
            m = mean[k] * (3.0 if s.get("distress") and i >= s["distress"]["start"] else 1.0)
            if s.get("deal") and s["deal"]["announce"] <= i:
                m *= 0.4
            x = level.get(k, math.log(m))
            x = x + 0.25 * (math.log(m) - x) + rng.normal(0, 0.11)
            level[k] = x
            short = int(round(float(b["shares"][j]) * min(math.exp(x), 0.45) / 10) * 10)
            lo = max(0, j - 9)
            adv = int(round(float(np.mean(b["volume"][lo:j + 1]))))
            sp = H.on(hist, k, i)
            p0 = prev.get(k)
            rows.append(dict(settlement=U.DAYS[i], symbol=sp["ticker"], issue=_issue_name(sp["name"]),
                             market={"N": "NYSE", "A": "NYSE AMER", "Q": "NASDAQ"}[sp["exch"]], short=short,
                             previous=p0, adv=adv, revised="", published=pub))
            prev[k] = short
    # a few rows republished as revised with the next publication
    out = []
    for r in rows:
        out.append(r)
        if rng.random() < 0.006:
            nxt = [d for d in pubs.values() if d > r["published"]]
            if nxt:
                rr = dict(r, short=int(round(r["short"] * float(rng.uniform(0.92, 1.08)) / 10) * 10), revised="R",
                          published=min(nxt))
                out.append(rr)
    out.sort(key=lambda r: (r["published"], r["settlement"], r["symbol"], r["revised"]))
    return out


def _issue_name(name):
    t = name.upper().replace(",", "").replace(".", "")
    return t[:30].strip()


def _add_bdays(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


# ------------------------------------------------------------------------------------------------ the sweep rate
POLICY = [("2017-12-14", 1.375), ("2018-03-22", 1.625), ("2018-06-14", 1.875), ("2018-09-27", 2.125),
          ("2018-12-20", 2.375), ("2019-08-01", 2.125), ("2019-09-19", 1.875), ("2019-10-31", 1.625),
          ("2020-03-04", 1.125), ("2020-03-16", 0.125), ("2022-03-17", 0.375), ("2022-05-05", 0.875),
          ("2022-06-16", 1.625), ("2022-07-28", 2.375), ("2022-09-22", 3.125), ("2022-11-03", 3.875),
          ("2022-12-15", 4.375), ("2023-02-02", 4.625), ("2023-03-23", 4.875), ("2023-05-04", 5.125),
          ("2023-07-27", 5.375), ("2024-09-19", 4.875), ("2024-11-08", 4.625), ("2024-12-19", 4.375),
          ("2025-09-18", 4.125), ("2025-10-30", 3.875), ("2025-12-11", 3.625), ("2026-03-19", 3.375)]


def sweep():
    rng = U.rng_for(14)
    out = []
    d = dt.date(2018, 1, 1)
    pol = [(dt.date.fromisoformat(a), v) for a, v in POLICY]
    last = None
    while d <= W.SWEEP_LAST:
        if last is None or (d.weekday() < 5 and (d in U.DIDX or d > W.END)):
            mid = [v for a, v in pol if a <= d][-1]
            ref = mid - 0.05 + rng.normal(0, 0.006)
            if d.month != (d + dt.timedelta(days=1)).month:
                ref += abs(rng.normal(0.02, 0.01))
            spread = 0.25 if d < W.SWEEP_SWITCH else 0.20
            last = (round(ref, 4), round(max(0.01, ref - spread), 4),
                    "FEDFUNDS-EFF" if d < W.SWEEP_SWITCH else "OBFR", spread)
        out.append(dict(date=d, reference=last[2], reference_rate=last[0], spread=last[3], sweep_rate=last[1],
                        accrual_basis="ACT/360"))
        d += dt.timedelta(days=1)
    return out


# ------------------------------------------------------------------------------------------------ the live book
def book(secs, paths, bars, hist, fund_rows, ids):
    """Monthly rebalances from July 2023: fifty names, equal weight, chosen on twelve-to-one-month momentum and the
    trailing earnings yield known at the time; parent orders from the OMS (stamped in UTC) and the broker's child
    executions (stamped in New York time), with busts and corrections as the broker sends them."""
    rng = U.rng_for(15)
    reb = []
    for y in range(2023, 2027):
        for m in range(1, 13):
            i = U.day_on_or_after(dt.date(y, m, 1))
            if i < U.T and U.DAYS[i] >= W.LIVE_FROM:
                reb.append(i)
    eps_by = _ttm_eps(fund_rows, ids, secs)
    nav = 150_000_000.0
    flows = {U.day_on_or_after(dt.date(2024, 4, 1)): 40_000_000.0, U.day_on_or_after(dt.date(2025, 1, 2)): 30_000_000.0}
    pos = {}
    orders, fills = [], []
    seq = 0
    exec_seq = 0
    last_i = reb[0]
    for i in reb:
        # mark to market and corporate actions since the last rebalance
        for t in range(last_i + 1, i + 1):
            for k in list(pos):
                s = secs[k]
                b = bars[k]
                if t > b["i1"]:
                    if s["fate"] == "stock":
                        acq = s["deal"]["acquirer"]
                        pos[acq] = pos.get(acq, 0) + int(pos[k] * paths[k].deal_K)
                    del pos[k]
                    continue
                j = t - b["i0"]
                if b["F"][j] != 1.0:
                    pos[k] = int(round(pos[k] * b["F"][j]))
        nav += flows.get(i, 0.0)
        cands = []
        for s in secs:
            k = s["k"]
            if not _alive(s, i) or s["first"] > i - 260 or (s.get("deal") and s["deal"]["announce"] < i and
                                                               (s["deal"].get("close") or U.T) > i):
                continue
            b = bars[k]
            j = i - 1 - b["i0"]
            px = float(b["close"][j])
            adv = float(np.mean(b["volume"][max(0, j - 19):j + 1])) * px
            if px < 5 or adv < 1.5e6:
                continue
            j12, j1 = j - 252, j - 21
            if j12 < 1:
                continue
            mom = float(np.prod(1 + np.nan_to_num(b["ret"][j12 + 1:j1 + 1])) - 1)
            e = eps_by(k, U.DAYS[i - 1])
            if e is None:
                continue
            ey = e / px
            cands.append((k, mom, ey))
        if len(cands) < 60:
            last_i = i
            continue
        mr = _rank([c[1] for c in cands])
        er = _rank([c[2] for c in cands])
        score = sorted(zip(cands, mr + er), key=lambda z: -z[1])
        keep = set(z[0][0] for z in score[:50])
        # value the book at the rebalance day's open
        val = nav
        target = {}
        for k in keep:
            b = bars[k]
            o = float(b["open"][i - b["i0"]])
            if math.isnan(o):
                o = float(b["close"][i - 1 - b["i0"]])
            target[k] = int(val * 0.02 / o // 100 * 100)
        for k in sorted(set(pos) | keep):
            b = bars[k]
            if b["ctype"][i - b["i0"]] != "T":
                continue                  # no trade in the name that day: the order waits for the next rebalance
            want = target.get(k, 0)
            have = pos.get(k, 0)
            q = want - have
            if abs(q) < 100 and want != 0:
                continue
            if q == 0:
                continue
            seq += 1
            side = "BUY" if q > 0 else "SELL"
            o_id = "PBK%s-%04d" % (U.DAYS[i].strftime("%y%m%d"), seq % 10000)
            res = _execute(secs[k], bars[k], i, abs(q), side, rng, o_id, exec_seq, hist)
            exec_seq = res["exec_seq"]
            filled = res["filled"]
            pos[k] = have + (filled if side == "BUY" else -filled)
            if pos[k] == 0:
                del pos[k]
            sp = H.on(hist, k, i)
            created = dt.datetime.combine(U.DAYS[i], dt.time(9, int(rng.integers(5, 26)), int(rng.integers(0, 60))),
                                          tzinfo=NY).astimezone(UTC)
            orders.append(dict(order_id=o_id, created_utc=created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                               rebalance_date=U.DAYS[i], account="PBK-SMID-01", symbol=sp["ticker"],
                               cusip=sp["cusip"], side=side, order_qty=abs(q), order_type="MKT", algo="VWAP",
                               tif="DAY", status=res["status"], filled_qty=filled, avg_price=res["avg"],
                               arrival_price=res["arrival"]))
            fills.extend(res["fills"])
        # the book's value moves with its holdings until the next rebalance
        last_i = i
        nav = _nav_next(pos, bars, i, reb, nav)
    return orders, fills


def _nav_next(pos, bars, i, reb, nav):
    nxt = [r for r in reb if r > i]
    if not nxt:
        return nav
    n = nxt[0]
    tot0 = tot1 = 0.0
    for k, q in pos.items():
        b = bars[k]
        j0 = i - b["i0"]
        j1 = min(n - 1, b["i1"]) - b["i0"]
        if j0 < 0 or j1 < j0:
            continue
        growth = float(np.prod(1 + np.nan_to_num(b["ret"][j0 + 1:j1 + 1])))
        v0 = q * float(b["close"][j0])
        tot0 += v0
        tot1 += v0 * growth
    return nav + (tot1 - tot0)


def _rank(xs):
    order = np.argsort(np.argsort(xs))
    return list(order / max(1, len(xs) - 1))


def _ttm_eps(rows, ids, secs):
    """Trailing four quarters' diluted EPS from the press releases and filings known by a date."""
    inv = {v: k for k, v in ids.items()}
    by = {}
    for r in rows:
        if r["period_type"] != "Q" or r["eps_diluted"] is None:
            continue
        k = inv[r["lp_id"]]
        by.setdefault(k, []).append((r["knowledge_date"], r["period_end"], float(r["eps_diluted"])))
    for k in by:
        by[k].sort()

    def f(k, d):
        ds = d.isoformat()
        known = {}
        for kd, pe, e in by.get(k, []):
            if kd <= ds:
                known[pe] = e
        if len(known) < 4:
            return None
        last4 = [known[pe] for pe in sorted(known)[-4:]]
        return float(sum(last4))
    return f


VENUES = [("XNAS", 0.22), ("XNYS", 0.16), ("ARCX", 0.11), ("BATS", 0.1), ("EDGX", 0.08), ("IEXG", 0.05),
          ("XBOS", 0.02), ("KLWX", 0.14), ("EDGA", 0.04), ("MEMX", 0.08)]


def _execute(s, b, i, qty, side, rng, o_id, exec_seq, hist):
    j = i - b["i0"]
    o, h, lo, c = (float(b[x][j]) for x in ("open", "high", "low", "close"))
    if math.isnan(o):
        o = h = lo = c
    adv = float(np.mean(b["volume"][max(0, j - 20):j])) if j > 0 else float(b["volume"][j])
    nch = int(np.clip(qty / max(200.0, adv * 0.004), 3, 40))
    partial = rng.random() < 0.03
    total = qty if not partial else int(qty * rng.uniform(0.6, 0.95)) // 100 * 100
    total = max(total, 100) if qty >= 100 else qty
    cuts = np.sort(rng.choice(np.arange(1, max(2, total // 100)), size=min(nch - 1, max(0, total // 100 - 1)),
                              replace=False)) * 100 if total >= 200 else np.array([], dtype=int)
    sizes = np.diff(np.concatenate([[0], cuts, [total]])).astype(int)
    early = U.DAYS[i] in C.early_closes(U.DAYS[i].year)
    close_t = 13 * 3600 if early else 16 * 3600
    secs_ = np.sort(rng.uniform(9.5 * 3600 + 5, close_t - 30, len(sizes)))
    # an intraday path pinned to the open and the close, kept inside the day's range
    span = (secs_ - 9.5 * 3600) / (close_t - 9.5 * 3600)
    w = np.cumsum(rng.normal(0, 1, len(sizes)))
    w = (w - span * (w[-1] if len(w) else 0)) * (math.log(h / lo) / 4 if lo > 0 else 0)
    path = np.exp(np.log(o) + span * (math.log(c) - math.log(o)) + w * 0.5)
    tick = 0.01 if c >= 1 else 0.0001
    pxs = np.clip(np.round(path / tick) * tick, lo, h)
    td = U.DAYS[i]
    settle = C.settle_date(td, 1 if td >= dt.date(2024, 5, 28) else 2)
    rate = 0.015 if td < W.FEE_CHANGE else 0.010
    sp = H.on(hist, s["k"], i)
    out = []
    for n_, (qq, px, tt) in enumerate(zip(sizes, pxs, secs_)):
        exec_seq += 1
        hh, mm, ss = int(tt // 3600), int(tt % 3600 // 60), tt % 60
        stamp = "%s %02d:%02d:%06.3f" % (td.strftime("%m/%d/%Y"), hh, mm, ss)
        venue = VENUES[int(rng.choice(len(VENUES), p=[v[1] for v in VENUES]))][0]
        e_id = "K%s%07d" % (td.strftime("%y%m%d"), exec_seq)
        row = dict(exec_id=e_id, exec_type="F", ref_exec_id="", client_order_id=o_id,
                   broker_order_id="KS-" + o_id[3:], symbol=sp["ticker"], side="B" if side == "BUY" else "S",
                   exec_time=stamp, qty=int(qq), price=round(float(px), 4), venue=venue,
                   liquidity=str(rng.choice(["A", "R"], p=[0.45, 0.55])) if venue != "KLWX" else "X",
                   commission=round(int(qq) * rate + 1e-9, 2), clearing_fee=round(int(qq) * 0.00025 + 1e-9, 2),
                   trade_date=td, settle_date=settle)
        out.append(row)
        if rng.random() < 0.0015:
            exec_seq += 1
            out.append(dict(row, exec_id="K%s%07d" % (td.strftime("%y%m%d"), exec_seq), exec_type="X",
                            ref_exec_id=e_id, exec_time=_later(stamp, rng)))
            exec_seq += 1
            corr = round(float(px) + float(rng.choice([-1, 1])) * tick * int(rng.integers(1, 4)), 4)
            out.append(dict(row, exec_id="K%s%07d" % (td.strftime("%y%m%d"), exec_seq), exec_type="C",
                            ref_exec_id=e_id, exec_time=_later(stamp, rng), price=corr))
    live = _net(out)
    filled = sum(r["qty"] for r in live)
    avg = round(sum(r["qty"] * r["price"] for r in live) / filled, 4) if filled else None
    status = "FILLED" if filled == qty else ("PARTIAL" if filled else "CANCELLED")
    return dict(fills=out, filled=filled, avg=avg, status=status, arrival=round(o, 4), exec_seq=exec_seq)


def _net(rows):
    """The executions standing after busts and corrections."""
    dead = {r["ref_exec_id"] for r in rows if r["exec_type"] in ("X", "C")}
    return [r for r in rows if r["exec_type"] in ("F", "C") and r["exec_id"] not in dead]


def _later(stamp, rng):
    d, t = stamp.split(" ")
    hh, mm, ss = t.split(":")
    tot = int(hh) * 3600 + int(mm) * 60 + float(ss) + float(rng.uniform(60, 1800))
    tot = min(tot, 16 * 3600 + 1800)
    return "%s %02d:%02d:%06.3f" % (d, int(tot // 3600), int(tot % 3600 // 60), tot % 60)
