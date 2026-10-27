"""task271 world: the stock universe, the central desk's 2026 parent orders and their executions with the mid path
around each, the desk's single orders, and the closing auction executions. Every number here is the generator's
clean truth; records.py writes the systems' own views of it."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

SYL_A = ["Bal", "Cal", "Dar", "Fen", "Gal", "Hal", "Kel", "Lan", "Mar", "Nor", "Pel", "Quen", "Ros", "Sel", "Tal",
         "Ven", "Wel", "Yar", "Bran", "Cor", "Dun", "Esk", "Grav", "Hest", "Ister", "Jor", "Kest", "Lor", "Mel", "Orm",
         "Pran", "Rav", "Stor", "Trel", "Ul", "Vos", "Wint", "Zel"]
SYL_B = ["drake", "worth", "mere", "brook", "vane", "holt", "garth", "stow", "wick", "combe", "lowe", "dene", "fold",
         "ridge", "moor", "thorne", "haven", "bury", "lock", "stead"]
SECTORS = [("Industrials", ["Engineering", "Industries", "Group", "Holdings"]),
           ("Consumer", ["Foods", "Brands", "Retail", "Group"]),
           ("Financials", ["Capital", "Holdings", "Insurance", "Group"]),
           ("Real estate", ["Estates", "Property", "Land"]),
           ("Technology", ["Systems", "Software", "Technologies"]),
           ("Energy", ["Energy", "Resources", "Power"]),
           ("Health care", ["Healthcare", "Pharma", "Medical"]),
           ("Materials", ["Minerals", "Materials", "Chemicals"])]
N_STOCKS = 120
# The master's names and tickers, drawn once from a wider pool and screened against the reference places (H21,
# asserted in checks.py); the universe's random stream is consumed as before, so every price, volume and fill stands.
SHARES = [("Quorent plc", "QRN"), ("WNP Group plc", "WNP"), ("Cleveside Insurance plc", "CLVS"),
          ("Cransroyd Property plc", "CPR"), ("Quorana Group plc", "QRG"), ("Pyrira plc", "PYR"),
          ("Langcote Pharma plc", "LNGC"), ("Trentgate Chemicals plc", "TRN"), ("Sandshaw Industries plc", "SDW"),
          ("Gorsecote Retail plc", "GRSC"), ("Ockside Capital plc", "OCKS"), ("Renello plc", "RNL"),
          ("Hathercote Technologies plc", "HTH"), ("Hazelness Energy plc", "HZL"), ("Birkmead Healthcare plc", "BHR"),
          ("Ostant plc", "OST"), ("Clevegate Industries plc", "CLV"), ("Osberthwaite Brands plc", "OBS"),
          ("Tessova plc", "TSV"), ("Westermead Land plc", "WTRM"), ("Ixura plc", "IXR"), ("Aldshaw Power plc", "ALDS"),
          ("Rainvale Healthcare plc", "RHN"), ("Gorselands Minerals plc", "GRSL"), ("Hambness Holdings plc", "HMBN"),
          ("RPL Group plc", "RPL"), ("Pentgate Group plc", "PNTG"), ("LNH Holdings plc", "LNH"),
          ("PJH Group plc", "PJH"), ("Novura plc", "NVR"), ("Ockshaw Pharma plc", "OPC"),
          ("Pentcote Materials plc", "PNT"), ("Ackroyd Ormerod plc", "ACK"), ("Quardale Group plc", "QRDL"),
          ("Ostira plc", "OTR"), ("Kennside Land plc", "KLN"), ("Inglecote Technologies plc", "IGC"),
          ("Carrcote Resources plc", "CRR"), ("Synaro plc", "SYNR"), ("BJM plc", "BJM"), ("Saxlands Group plc", "SXL"),
          ("Bramness Brands plc", "BRM"), ("FVS plc", "FVS"), ("Hatherling Land plc", "HHR"),
          ("Stanmead Systems plc", "SST"), ("Elstgate Resources plc", "ELS"), ("Fyrex Group plc", "FYRX"),
          ("Sturrmead Chemicals plc", "SCT"), ("Kennling Holdings plc", "KNL"), ("Rookmore Foods plc", "RKM"),
          ("WDR Holdings plc", "WDR"), ("Thornvale Property plc", "TPH"), ("Thornmore Software plc", "TSH"),
          ("Quarshaw Energy plc", "QER"), ("TSD Holdings plc", "TSD"), ("WRN plc", "WRN"),
          ("Draydale Group plc", "DDL"), ("Sturrside Foods plc", "STRS"), ("Pampwood Group plc", "PMP"),
          ("Liddwick Land plc", "LDWC"), ("Voraro Group plc", "VRG"), ("Birkwick Resources plc", "BKW"),
          ("Liddside Pharma plc", "LDSD"), ("Woldvale Minerals plc", "WLDV"), ("Fyrova plc", "FYR"),
          ("Tessica plc", "TSC"), ("Cormwick Holdings plc", "CRMW"), ("Rookgate Property plc", "RKGT"),
          ("Jessop Halliwell plc", "JSP"), ("Merura Group plc", "MRG"), ("Kirtroyd Pharma plc", "KPR"),
          ("Draygate Minerals plc", "DYG"), ("Vantmore Group plc", "VNTM"), ("Vorica Group plc", "VRC"),
          ("Hazelcote Capital plc", "HCZ"), ("Paxica plc", "PXC"), ("Cormdale Software plc", "CMD"),
          ("Fairclough Priestley plc", "FPR"), ("Synum plc", "SYN"), ("Cransling Minerals plc", "CMR"),
          ("Xanura plc", "XNR"), ("Osberdale Retail plc", "ORS"), ("Sheldale Group plc", "SHL"),
          ("Trentmead Land plc", "TRNT"), ("Quarmby & Thewlis plc", "QRM"), ("LCG Holdings plc", "LCG"),
          ("Farnling Medical plc", "FRNL"), ("Pyryx Group plc", "PYRY"), ("Evura Group plc", "EVR"),
          ("Malroyd Group plc", "MLRY"), ("Holroyd & Nuttall plc", "HLR"), ("Paxura plc", "PXR"),
          ("Woldfield Technologies plc", "WTL"), ("RLM Group plc", "RLM"), ("Lumola plc", "LML"),
          ("Wyckwood Materials plc", "WMY"), ("Gillwick Industries plc", "GLW"), ("Yeoroyd Group plc", "YRYD"),
          ("Glenroyd Capital plc", "GLR"), ("Ridroyd Land plc", "RDRY"), ("Hambmore Systems plc", "HSM"),
          ("Bellthwaite Energy plc", "BEL"), ("MBK plc", "MBK"), ("Stanshaw Minerals plc", "SNW"),
          ("Ingleness Engineering plc", "IEN"), ("Bramlands Foods plc", "BML"), ("Shelthwaite Insurance plc", "SHLT"),
          ("Lumera plc", "LMR"), ("Tamthwaite Technologies plc", "TTM"), ("Collness Energy plc", "CLNS"),
          ("Zenant Group plc", "ZNT"), ("Wycklands Chemicals plc", "WYC"), ("Tynvale Industries plc", "TYNV"),
          ("Ibbotson & Oddie plc", "IOB"), ("Vantlow Holdings plc", "VNT"), ("Uppvale Property plc", "UPP"),
          ("Lyndby Technologies plc", "LYN"), ("Myrlands Resources plc", "MYR"), ("Rainlow Pharma plc", "RPN"),
          ("Pampmore Minerals plc", "PPM")]
FORMER_NAME = {88: "Kirtgate Group plc"}    # the name the share traded under until 3 August 2026
CONSOLIDATED_INDEX = 57                  # the FTSE 250 stock that consolidated ten old shares into one on 18 May
CONSOLIDATION_DATE = dt.date(2026, 5, 18)


def _sedol(rg):
    chars = "0123456789BCDFGHJKLMNPQRSTVWXYZ"
    body = "B" + "".join(chars[int(rg.integers(0, len(chars)))] for _ in range(5))
    w = [1, 3, 1, 7, 3, 9]
    s = sum((int(c) if c.isdigit() else ord(c) - 55) * wi for c, wi in zip(body, w))
    return body + str((10 - s % 10) % 10)


def _isin(sedol):
    base = "GB00" + sedol
    digits = "".join(str(int(c)) if c.isdigit() else str(ord(c) - 55) for c in base)
    tot = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            d = d - 9 if d > 9 else d
        tot += d
    return base + str((10 - tot % 10) % 10)


def tick(price):
    return 0.05 if price < 100 else (0.2 if price < 500 else (0.5 if price < 1000 else (1.0 if price < 5000 else 2.0)))


def universe():
    """120 UK equities: names, codes, price, ADV, volatility, spread, index band."""
    rg = K.rng("universe")
    names, seen = [], set()
    while len(names) < N_STOCKS:
        stem = SYL_A[int(rg.integers(0, len(SYL_A)))] + SYL_B[int(rg.integers(0, len(SYL_B)))]
        if stem in seen:
            continue
        seen.add(stem)
        names.append(stem)
    out = []
    for i, stem in enumerate(names):
        sec, words = SECTORS[i % len(SECTORS)]
        rg.integers(0, len(words))           # the draw that once chose a sector word, kept so the stream is unchanged
        nm, tk = SHARES[i]
        sedol = _sedol(rg)
        band = "FTSE 100" if i < 40 else ("FTSE 250" if i < 100 else "Small cap")
        adv = float(np.exp(rg.normal({"FTSE 100": 15.6, "FTSE 250": 14.1, "Small cap": 12.7}[band], 0.45)))
        price = float(np.exp(rg.normal(5.9, 0.75)))
        price = max(40.0, min(price, 9000.0))
        vol = float({"FTSE 100": 95, "FTSE 250": 135, "Small cap": 175}[band] * np.exp(rg.normal(0, 0.18)))
        spread = float({"FTSE 100": 4.0, "FTSE 250": 9.0, "Small cap": 22.0}[band] * np.exp(rg.normal(0, 0.25)))
        out.append(dict(i=i, name=nm, sector=sec, ticker=tk, sedol=sedol, isin=_isin(sedol), band=band,
                        adv=adv, price=price, vol=vol, spread=spread))
    c = out[CONSOLIDATED_INDEX]
    c["price"] = 286.0                   # new shares; the old line traded near 29p
    c["adv"] = c["adv"] * 0.6
    c["old_sedol"] = _sedol(rg)
    c["old_isin"] = _isin(c["old_sedol"])
    return out


def day_prices(stocks, days):
    """Each stock's closing mid on each trading day: a random walk at its daily volatility."""
    rg = K.rng("closes")
    P = {}
    for s in stocks:
        steps = rg.normal(0, s["vol"] / 1e4, len(days))
        lvl = s["price"] * np.exp(np.cumsum(steps) - 0.5 * np.arange(1, len(days) + 1) * (s["vol"] / 1e4) ** 2)
        P[s["i"]] = {d: float(v) for d, v in zip(days, lvl)}
    return P


def g_build(h, tau):
    """Share of a fill's 60-second adverse move built h seconds after it."""
    h = np.minimum(np.maximum(h, 0.0), float(K.HORIZON))
    return (1 - np.exp(-h / tau)) / (1 - math.exp(-K.HORIZON / tau))


class Parent:
    __slots__ = ("pid", "day", "stock", "side", "algo", "style", "qty", "pct", "t0", "t_end", "children", "arrival_mid",
                 "kind", "auction", "order_id", "fund")


def _schedule(style, rg, q_pct, t0):
    """Child times (seconds after the parent's release), shares of the parent, and routing phase per child."""
    times, shares, phase = [], [], []
    if style == "IS":
        nb = int(max(9, round(q_pct * 0.35 / 0.022)))
        tb = np.sort(rg.uniform(0.5, 90.0, nb))
        dur = float(rg.uniform(15, 60) * 60)
        nw = int(max(6, round(q_pct * 0.65 / 0.05)))
        gaps = rg.exponential(dur / nw, nw)
        tw = 90.0 + np.cumsum(gaps)
        times = list(tb) + list(tw)
        shares = [0.35 / nb] * nb + [0.65 / nw] * nw
        phase = ["burst"] * nb + ["work"] * nw
    elif style in ("VWAP", "POV"):
        nb = 4
        tb = np.sort(rg.uniform(0.5, 20.0, nb))
        dur = float(rg.uniform(60, 200) * 60) if style == "VWAP" else float(rg.uniform(20, 80) * 60)
        mean_gap = 95.0 if style == "VWAP" else 70.0
        nw = int(max(6, round(dur / mean_gap)))
        tw = 20.0 + np.cumsum(rg.exponential(dur / nw, nw))
        times = list(tb) + list(tw)
        shares = [0.06 / nb] * nb + [0.94 / nw] * nw
        phase = ["burst"] * nb + ["vwap"] * nw
    elif style == "CLOSE":
        dur = K.CLOSE_S - 60 - t0
        nw = int(max(6, round(dur / 55.0)))
        tw = np.cumsum(rg.exponential(dur / (nw + 1), nw))
        tw = tw[tw < dur]
        times = list(tw)
        shares = [0.65 / max(1, len(tw))] * len(tw)
        phase = ["work"] * len(tw)
    jit = rg.uniform(0.7, 1.3, len(shares))
    shares = list(np.array(shares) * jit / (np.array(shares) * jit).sum() * (0.65 if style == "CLOSE" else 1.0))
    return times, shares, phase


def desk_orders(stocks, days, P):
    """The desk's 2026 algorithmic parents and single orders, with no two of the desk's orders in one stock at once."""
    rg = K.rng("parents")
    busy = {s["i"]: {} for s in stocks}
    weights = np.array([{"FTSE 100": 3.0, "FTSE 250": 1.6, "Small cap": 0.8}[s["band"]] for s in stocks])
    weights = weights / weights.sum()
    algos = K.ALGOS
    ashare = np.array([K.ALGO[a]["share"] for a in algos])
    ashare = ashare / ashare.sum()
    parents = []
    n_par = 2800
    n_single = 2100
    pid = 0
    for kind, n in (("algo", n_par), ("single", n_single)):
        made = 0
        while made < n:
            day = days[int(rg.integers(0, len(days)))]
            s = stocks[int(rg.choice(len(stocks), p=weights))]
            side = "B" if rg.random() < 0.5 else "S"
            p = Parent()
            p.kind = kind
            p.day, p.stock, p.side = day, s, side
            p.auction = None
            if kind == "algo":
                a = algos[int(rg.choice(len(algos), p=ashare))]
                p.algo, p.style = a, K.ALGO[a]["style"]
                pct = float(np.exp(rg.normal(math.log(1.4), 0.55)))
                pct = min(max(pct, 0.25), 7.0)
                if p.style == "CLOSE":
                    t0 = float(rg.uniform(15 * 3600 + 20 * 60, 15 * 3600 + 55 * 60))
                else:
                    t0 = float(rg.uniform(K.OPEN_S + 5 * 60, K.OPEN_S + 6.2 * 3600))
                times, shares, phase = _schedule(p.style, rg, pct, t0)
                t_end = t0 + (max(times) if times else 0.0) + 1.0
                if t_end > K.CLOSE_S - 62:
                    keep = [k for k, t in enumerate(times) if t0 + t <= K.CLOSE_S - 62]
                    if len(keep) < 5:
                        continue
                    times = [times[k] for k in keep]
                    shares = [shares[k] for k in keep]
                    phase = [phase[k] for k in keep]
                    t_end = t0 + max(times) + 1.0
            else:
                p.algo, p.style = "DMA", "SINGLE"
                pct = float(rg.uniform(0.012, 0.06))
                t0 = float(rg.uniform(K.OPEN_S + 10 * 60, K.CLOSE_S - 15 * 60))
                times, shares, phase = [0.0], [1.0], ["single"]
                t_end = t0 + 1.0
            # the desk works one order in a stock at a time, and leaves a gap of five minutes between them
            lo, hi = t0 - 300, t_end + 300 + (K.UNCROSS_S - t_end if p.style == "CLOSE" else 0)
            iv = busy[s["i"]].setdefault(day, [])
            if any(not (hi <= a0 or lo >= b0) for a0, b0 in iv):
                continue
            iv.append((lo, hi))
            p.pid = pid
            pid += 1
            p.pct, p.t0, p.t_end = pct, t0, t_end
            # no two of an order's children print in the same millisecond
            tt = sorted(times)
            for k in range(1, len(tt)):
                if tt[k] - tt[k - 1] < 0.004:
                    tt[k] = tt[k - 1] + 0.004
            order_k = np.argsort(times, kind="stable")
            times = [tt[int(np.where(order_k == k)[0][0])] for k in range(len(times))]
            adv = s["adv"]
            qty_total = max(1, int(round(adv * pct / 100.0)))
            ch = []
            for t, sh, ph in zip(times, shares, phase):
                q = max(1, int(round(qty_total * sh)))
                ch.append([t0 + t, q, ph])
            if p.style == "CLOSE":
                done = sum(c[1] for c in ch)
                p.auction = max(1, int(round(qty_total * 0.35)))
                qty_total = done + p.auction
            p.qty = sum(c[1] for c in ch) + (p.auction or 0)
            p.children = ch
            parents.append(p)
            made += 1
    parents.sort(key=lambda p: (p.day, p.t0, p.pid))
    return parents


def simulate(stocks=None):
    """Executions with their mids: every child order of every desk order filled once at one venue."""
    stocks = stocks or universe()
    days = K.trading_days()
    P = day_prices(stocks, days)
    parents = desk_orders(stocks, days, P)
    rg_v = K.rng("venues")
    rg_n = K.rng("noise")
    rg_p = K.rng("prices")
    execs = []
    for p in parents:
        s = p.stock
        prev = P[s["i"]][p.day]
        sig_d = s["vol"]
        frac = (p.t0 - K.OPEN_S) / (K.CLOSE_S - K.OPEN_S)
        m0 = prev * math.exp(rg_p.normal(0, sig_d / 1e4 * math.sqrt(max(frac, 0.02))))
        side = 1.0 if p.side == "B" else -1.0
        T = int(p.t_end - p.t0 + 302 + (K.UNCROSS_S - p.t_end if p.auction else 0))
        sig_s = sig_d / math.sqrt(8.5 * 3600)
        noise = np.concatenate([[0.0], np.cumsum(rg_n.normal(0, sig_s, T))])
        own_steps = np.zeros(T + 2)
        venues = []
        for t, q, ph in p.children:
            pv = np.array([K.ROUTE[ph][v] for v in K.VENUES])
            v = K.VENUES[int(rg_v.choice(len(K.VENUES), p=pv / pv.sum()))]
            venues.append(v)
            k0 = int(math.floor(t - p.t0))
            if k0 <= T:
                # the desk's own trade moves the market at once, so the mid printed with the fill already carries it
                own_steps[k0] += side * K.LAMBDA * (q / s["adv"] * 100.0)
        path_bp = noise[:T + 1] + np.cumsum(own_steps)[:T + 1]
        tk = tick(m0)

        def mid_at(rel_s, extra_bp=0.0):
            k = int(math.floor(rel_s))
            if k < 0 or k > T:
                return None
            m = m0 * (1 + (path_bp[k] + extra_bp) / 1e4)
            return round(round(m / (tk / 2)) * (tk / 2), 4)

        p.arrival_mid = mid_at(0.0)
        for (t, q, ph), v in zip(p.children, venues):
            rel = t - p.t0
            m_exec = mid_at(rel)
            kind = K.VENUE[v]["kind"]
            half = m_exec * s["spread"] / 2e4
            if kind == "midpoint book":
                px = m_exec
            elif kind == "lit order book":
                aggressive = rg_v.random() < 0.72
                px = m_exec + side * half if aggressive else m_exec - side * half
                px = round(px / tk) * tk
            else:
                px = m_exec + side * half * float(rg_v.uniform(0.1, 0.6))
            marks = {}
            a, tau = K.VENUE[v]["alpha"], K.VENUE[v]["tau"]
            for h in (1, 5, 30, 60, 300):
                tt = t + h
                # the counterparty's information: the move against the order that follows a fill at this venue
                marks[h] = mid_at(rel + h, -side * a * float(g_build(h, tau))) if tt <= K.CLOSE_S else None
            execs.append(dict(pid=p.pid, day=p.day, t=t, stock=s["i"], side=p.side, qty=q, venue=v, price=round(px, 4),
                              mid0=m_exec, marks=marks, phase=ph, session="CONT", algo=p.algo, style=p.style))
        if p.auction:
            m_close = mid_at(K.CLOSE_S - p.t0 - 1) or m0
            px = round(m_close * (1 + rg_p.normal(0, 4.0) / 1e4), 4)
            execs.append(dict(pid=p.pid, day=p.day, t=float(K.UNCROSS_S), stock=s["i"], side=p.side, qty=p.auction,
                              venue="XWEX", price=px, mid0=None, marks={1: None, 5: None, 30: None, 60: None, 300: None},
                              phase="auction", session="AUCT", algo=p.algo, style=p.style))
    return dict(stocks=stocks, days=days, closes=P, parents=parents, execs=execs)


def adverse_bp(e, h=60):
    """The adverse move of an execution at h seconds, positive when the mid moved against the order."""
    m1 = e["marks"].get(h)
    if m1 is None or e["mid0"] is None:
        return None
    sgn = 1.0 if e["side"] == "B" else -1.0
    return -sgn * (m1 - e["mid0"]) / e["mid0"] * 1e4
