"""The listed universe and its lives: who is listed when, what each company is called and trades as on every day,
which exchange it sits on, its CUSIP, and the events that end or reshape it (acquisitions, going private, delisting
for cause, spin-offs, a terminated deal, renamings, ticker and exchange changes, a classification review)."""
import datetime as dt

import numpy as np

import calendar_us as C
import world as W

DAYS = C.trading_days(W.START, W.END)
T = len(DAYS)
DIDX = {d: i for i, d in enumerate(DAYS)}


def rng_for(*keys):
    return np.random.default_rng([W.SEED] + list(keys))


def day_on_or_after(d):
    """The index of the first trading day on or after d; T when d is past the store's last day."""
    if d > DAYS[-1]:
        return T
    while d not in DIDX:
        d += dt.timedelta(days=1)
    return DIDX[d]


def cusip_check(s8):
    total = 0
    for i, ch in enumerate(s8):
        v = int(ch) if ch.isdigit() else ord(ch) - 55
        if i % 2 == 1:
            v *= 2
        total += v // 10 + v % 10
    return str((10 - total % 10) % 10)


def make_cusip(rng, used):
    alnum = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
    while True:
        issuer = "".join(rng.choice(list("0123456789"), 3)) + "".join(rng.choice(list(alnum), 3))
        if issuer not in used:
            used.add(issuer)
            return issuer


def full_cusip(issuer, issue="10"):
    return issuer + issue + cusip_check(issuer + issue)


def _roots(rng):
    roots = []
    for p in W.PREFIX:
        for s in W.SUFFIX:
            r = p + s
            if p[-1] == s[0] or r in W.NAME_BLOCK or len(r) > 11:
                continue
            roots.append(r)
    rng.shuffle(roots)
    return roots


def _ticker(root, exch, taken, rng):
    up = root.upper()
    cons = [c for c in up[1:] if c not in "AEIOU"]
    n = 4 if exch == "Q" else int(rng.choice([2, 3, 3, 3, 4], 1)[0])
    cands = [up[:n], up[0] + "".join(cons[:n - 1]), up[:n - 1] + up[-1], up[0] + "".join(cons[1:n]),
             up[:2] + "".join(cons[-(n - 2):]) if n > 2 else up[0] + up[-1]]
    for c in cands:
        if len(c) == n and c.isalpha() and c not in taken:
            return c
    while True:
        c = up[0] + "".join(rng.choice(list("ABCDEFGHIKLMNOPRSTUVWXY"), n - 1))
        if c not in taken:
            return c


def _legal(rng, desc):
    if desc in ("Realty Trust",):
        return ""
    if desc == "Midstream Partners":
        return "L.P."
    return W.LEGAL[int(rng.integers(len(W.LEGAL)))]


def issuer_name(root, desc, legal):
    """A plain-comma "Inc." on some names and not others, as companies write their own names."""
    base = root if not desc else "%s %s" % (root, desc)
    if not legal:
        return base
    if legal == "Inc." and len(base) % 3 == 0:
        return base + ", Inc."
    return base + " " + legal


def build():
    """Every security with its static traits and its life plan, as a list of dicts keyed by position."""
    rng = rng_for(1)
    roots = _roots(rng)
    n_all = W.N_START + W.N_IPO + W.N_SPIN
    secs = []
    sids = rng.choice(np.arange(10101, 93999), size=n_all, replace=False)
    sids.sort()
    rng.shuffle(sids)
    used_issuers = set()
    taken = set()
    ipo_lo, ipo_hi = day_on_or_after(dt.date(2018, 3, 1)), day_on_or_after(dt.date(2026, 6, 1))
    boom_lo, boom_hi = day_on_or_after(dt.date(2020, 7, 1)), day_on_or_after(dt.date(2021, 11, 30))
    ipo_days = sorted(list(rng.integers(ipo_lo, boom_lo, 6)) + list(rng.integers(boom_lo, boom_hi, 9)) +
                      list(rng.integers(day_on_or_after(dt.date(2023, 3, 1)), ipo_hi, 5)))
    for k in range(n_all):
        kind = "initial" if k < W.N_START else ("ipo" if k < W.N_START + W.N_IPO else "spin")
        si = int(rng.choice(len(W.SECTORS), p=W.SECTOR_WEIGHT))
        code, sname, descs, divp, vm = W.SECTORS[si]
        desc = descs[int(rng.integers(len(descs)))]
        if rng.random() < 0.18 and desc not in ("Bancorp", "Realty Trust", "Midstream Partners"):
            desc = ""
        legal = _legal(rng, desc)
        root = roots[k]
        exch = str(rng.choice(["N", "A", "Q"], p=W.EXCH_SHARE))
        if kind == "ipo":
            exch = str(rng.choice(["N", "Q"], p=[0.3, 0.7]))
        logcap = float(np.clip(rng.normal(9.12, 0.34), 8.35, 9.95))
        if kind != "initial":
            logcap = float(np.clip(rng.normal(9.0, 0.3), 8.5, 9.7))
        price0 = float(np.clip(np.exp(rng.normal(np.log(27.0), 0.55)), 4.0, 140.0))
        tick = _ticker(root, exch, taken, rng)
        taken.add(tick)
        secs.append(dict(
            k=k, sid=int(sids[k]), kind=kind, root=root, sector=si, desc=desc, legal=legal,
            name=issuer_name(root, desc, legal), exch=exch, ticker=tick, logcap=logcap, price0=price0,
            beta=float(np.clip(rng.normal(1.0, 0.22), 0.5, 1.6)),
            ivol=float(np.clip((0.32 - 0.09 * (logcap - 9.1)) * vm * np.exp(rng.normal(0, 0.18)), 0.16, 0.62)),
            payer=bool(rng.random() < divp * (0.75 + 0.25 * (logcap > 9.2))),
            turnover=float(np.exp(rng.normal(np.log(0.0043), 0.45))),
            spread_bp=float(np.clip(18 * np.exp(-(logcap - 9.0) * 1.6) * np.exp(rng.normal(0, 0.3)), 3, 90)),
            float_factor=float(np.clip(rng.normal(0.88, 0.09), 0.55, 1.0)),
            growth=float(rng.normal(0.05, 0.09)),
            issuer=make_cusip(rng, used_issuers),
            first=0 if kind == "initial" else None, last=None, fate="alive", events=[]))
    for s, d in zip([s for s in secs if s["kind"] == "ipo"], ipo_days):
        s["first"] = int(d)
    _plan_lives(secs, rng)
    return secs


def _alive_through(s, a, b):
    return s["first"] is not None and s["first"] <= a and (s["last"] is None or s["last"] >= b)


def _plan_lives(secs, rng):
    by = lambda kind: [s for s in secs if s["kind"] == kind]
    init, ipos, spins = by("initial"), by("ipo"), by("spin")
    free = [s for s in init + ipos]

    def take(pool, n, cond=lambda s: True):
        cand = [s for s in pool if s["fate"] == "alive" and not s["events"] and not s.get("deal") and
                not s.get("distress") and cond(s)]
        idx = rng.choice(len(cand), size=n, replace=False)
        return [cand[i] for i in sorted(idx)]

    # spin-offs: two established non-financial parents
    parents = take(init, 2, lambda s: s["sector"] not in (6, 10) and s["logcap"] > 9.25)
    for p, child, d in zip(parents, spins, (dt.date(2019, 10, 1), dt.date(2022, 7, 5))):
        ex = day_on_or_after(d)
        child["first"] = ex
        child["parent"] = p["k"]
        child["sector"] = p["sector"] if rng.random() < 0.5 else int(rng.choice([2, 7]))
        p["events"].append(("spinoff", ex, child["k"]))
        child["events"].append(("spun", ex, p["k"]))

    def window(lo, hi):
        return int(rng.integers(day_on_or_after(lo), day_on_or_after(hi)))

    # cash and stock acquisitions, going private, one terminated deal
    plans = [("cash", dt.date(2018, 4, 1), dt.date(2026, 6, 15), 12), ("stock", dt.date(2018, 6, 1),
             dt.date(2025, 12, 1), 4), ("private", dt.date(2019, 1, 1), dt.date(2025, 9, 1), 2)]
    for fate, lo, hi, n in plans:
        for s in take(free, n, lambda s: s["sector"] != 10):
            a = window(lo, hi)
            if s["first"] is not None and a < s["first"] + 120:
                a = min(T - 30, s["first"] + 120 + int(rng.integers(0, 200)))
            close = a + int(rng.integers(45, 140))
            s["deal"] = dict(kind=fate, announce=a, close=close, premium=float(rng.uniform(0.18, 0.46)),
                             spread0=float(rng.uniform(0.015, 0.06)))
            if close >= T:          # still pending at the end of the store
                s["deal"]["close"] = None
            else:
                s["fate"] = fate
                s["last"] = close - 1
    # stock deals need an acquirer listed throughout and larger
    for s in [s for s in secs if s.get("deal", {}).get("kind") == "stock"]:
        a, c = s["deal"]["announce"], s["deal"]["close"] or T - 1
        acq = [x for x in init if x is not s and x["fate"] == "alive" and not x.get("deal") and
               x["logcap"] > s["logcap"] + 0.1 and not any(e[0] == "spinoff" for e in x["events"])]
        s["deal"]["acquirer"] = acq[int(rng.integers(len(acq)))]["k"]
    t = take(free, 1, lambda s: s["sector"] != 10 and s["kind"] == "initial")[0]
    a = day_on_or_after(dt.date(2021, 5, 11))
    t["deal"] = dict(kind="terminated", announce=a, close=None, terminate=day_on_or_after(dt.date(2021, 11, 16)),
                     premium=0.31, spread0=0.07)
    t["events"].append(("deal_terminated", t["deal"]["terminate"], None))

    # delisted for cause, three after a reverse split; four survivors of a reverse split
    for i, s in enumerate(take(free, 6, lambda s: s["sector"] in (0, 3, 5, 7, 8) and s["logcap"] < 9.25)):
        lo = max(s["first"] + 260, day_on_or_after(dt.date(2019, 6, 1)))
        end = int(rng.integers(lo, min(T - 20, lo + 1400)))
        start = max(s["first"] + 20, end - int(rng.integers(260, 460)))
        s["distress"] = dict(start=start, end=end, rs=(end - int(rng.integers(90, 170))) if i < 3 else None,
                             target=float(rng.uniform(0.28, 0.75)))
        s["fate"] = "cause"
        s["last"] = end
        s["bankrupt"] = bool(i % 2 == 0)
    for s in take(free, 4, lambda s: s["sector"] in (3, 5, 7) and s["logcap"] < 9.3):
        rs = int(rng.integers(max(s["first"] + 300, day_on_or_after(dt.date(2019, 9, 1))), T - 60))
        s["distress"] = dict(start=max(s["first"] + 10, rs - int(rng.integers(250, 400))), end=None, rs=rs,
                             target=float(rng.uniform(0.62, 0.9)))
    for s in secs:
        if s.get("distress", {}).get("rs"):
            s["events"].append(("reverse_split", s["distress"]["rs"], None))

    # renamings, ticker changes, exchange transfers, the classification review
    def alive_day(s, lo=None, hi=None):
        a = max(s["first"] + 40, day_on_or_after(lo) if lo else 0)
        b = (s["last"] - 40) if s["last"] is not None else T - 10
        if hi:
            b = min(b, day_on_or_after(hi))
        return int(rng.integers(a, b)) if b > a + 5 else None

    for s in take(init + ipos, 10, lambda s: s["fate"] == "alive"):
        d = alive_day(s, dt.date(2018, 6, 1))
        if d:
            s["events"].append(("rename", d, None))
    for s in take(init + ipos, 8):
        d = alive_day(s, dt.date(2018, 3, 1))
        if d:
            s["events"].append(("ticker_change", d, None))
    for s in take(init, 6, lambda s: s["exch"] in ("N", "Q")):
        d = alive_day(s, dt.date(2018, 9, 1))
        if d:
            s["events"].append(("exchange_transfer", d, "Q" if s["exch"] == "N" else "N"))
    review = day_on_or_after(dt.date(2023, 3, 20))
    for s in take(init + ipos, 3, lambda s: s["sector"] in (2, 3, 7) and _alive_through(s, review, review) and
                  s["desc"] in ("", "Industries", "Controls", "Systems", "Leisure")):
        s["events"].append(("reclassify", review, {2: 7, 3: 8, 7: 2}[s["sector"]]))
    for s in secs:
        s["events"].sort(key=lambda e: e[1])
