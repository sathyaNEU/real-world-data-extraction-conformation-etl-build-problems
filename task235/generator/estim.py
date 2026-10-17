"""task235 estimators, read only from the pack: purchases and their events under KC-DQ-04, each build's tracking loss
the golden way (a missing event judged against the next session of the phone that made the purchase, the few still
open counted at the build's own share of resolved gaps that stayed missing), the other rates the open purchases could
take, the routes a solver reaches for instead, and the two asks (paying players, gross bookings per paying player)."""
import os
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd

RUN = pd.Timestamp("2026-11-09 07:00")
WIN0, WIN1 = pd.Timestamp("2026-10-12").date(), pd.Timestamp("2026-11-08").date()
IST_END = pd.Timestamp("2026-10-25 01:00")
LINE = 0.02
EXPONENT = {"JPY": 0, "KRW": 0}                         # ISO 4217 minor units; every other currency here has two
ORDER = [("ios", v) for v in ("7.38.2", "7.39.1", "7.40.0", "7.41.0", "7.41.1", "7.42.0")] + \
        [("android", v) for v in ("7.38.1", "7.39.0", "7.40.2", "7.41.0", "7.41.3", "7.42.0")]
NEW = [("android", "7.42.0"), ("ios", "7.42.0")]


def load(target, files):
    rd = lambda k, **kw: pd.read_csv(os.path.join(target, files[k]), **kw)
    D = dict(val=rd("val", dtype=str, keep_default_na=False), evt=rd("evt", dtype=str, keep_default_na=False),
             ses=rd("ses", dtype=str, keep_default_na=False), links=rd("links", dtype=str), rates=rd("rates"))
    D["builds"] = pd.read_excel(os.path.join(target, files["reg"]), sheet_name="Builds", dtype={"build_number": str})
    return D


def utc(s):
    return pd.to_datetime(s.str.replace("Z", "", regex=False))


def irish_date(t, clock="irish"):
    if clock == "utc":
        return t.dt.date
    return (t + pd.to_timedelta(np.where(t < IST_END, 1, 0), unit="h")).dt.date


# ------------------------------------------------------------------ KC-DQ-04 s.2 and s.3
def purchases(D, clock="irish", testers=False, renewals=False):
    v = D["val"]
    m = (v.transaction_kind == "purchase") | (renewals & (v.transaction_kind == "renewal"))
    if not testers:
        m &= (v.environment == "Production") & (v.purchase_type == "standard")
    p = v[m].copy()
    p["t"] = utc(p.purchased_at)
    p["day"] = irish_date(p.t, clock)
    p = p[(p.day >= WIN0) & (p.day <= WIN1)]
    b = D["builds"]
    key = dict(zip(b.build_number.astype(str), zip(b.platform, b.version)))
    p["build"] = [key.get(x, ("", "")) for x in p.app_build]
    p = p.drop_duplicates("store_transaction_id")
    return p.reset_index(drop=True)


def events(D):
    e = D["evt"].copy()
    e["recv"] = utc(e.received_at)
    e = e.sort_values(["store_transaction_id", "recv"]).drop_duplicates("store_transaction_id")
    return e.set_index("store_transaction_id")


def session_starts(D, key="device_id"):
    s = D["ses"]
    t = utc(s.started_at).values
    out = {}
    for k, g in pd.DataFrame({"k": s[key].values, "t": t}).sort_values("t").groupby("k"):
        out[k] = g.t.values
    return out


def next_start(starts, keys, times):
    out = []
    for k, t in zip(keys, times):
        s = starts.get(k)
        if s is None:
            out.append(np.datetime64("NaT", "ns")); continue
        i = np.searchsorted(s, t, side="right")
        out.append(s[i] if i < len(s) else np.datetime64("NaT", "ns"))
    return pd.to_datetime(np.array(out, dtype="datetime64[ns]"))


def conform(D, clock="irish", p=None):
    p = purchases(D, clock) if p is None else p.copy()
    e = events(D)
    p["matched"] = p.store_transaction_id.isin(e.index)
    p["recv"] = p.store_transaction_id.map(e.recv)
    ta = p.t.values
    p["next"] = next_start(session_starts(D), p.device_id, ta)
    p["due"] = p.next.notna()
    p["held"] = p.matched & p.due & (p.recv >= p.next)
    p["next_account"] = next_start(session_starts(D, "account_id"), p.account_id, ta)
    p["due_account"] = p.next_account.notna()
    p["age_d"] = (RUN - p.t).dt.total_seconds() / 86400
    return p


# ------------------------------------------------------------------ each build's tracking loss
def counts(p):
    """per build: purchases, those whose phone has opened the game since (due), their missing events (lost), their
    events that waited for that session (held), and the missing events of purchases whose phone has not (pending)"""
    out = {}
    for b, g in p.groupby("build"):
        out[b] = dict(n=len(g), due=int(g.due.sum()), lost=int((g.due & ~g.matched).sum()), held=int(g.held.sum()),
                      pending=int((~g.due & ~g.matched).sum()))
    return out


def resolved_share(c):
    """of the build's events that were missing until their phone opened the game again, the share that stayed missing"""
    return c["lost"] / (c["lost"] + c["held"]) if c["lost"] + c["held"] else 0.0


def loss(p):
    """the golden: each build's lost events plus its pending ones counted lost at the build's resolved share, over its
    purchases"""
    return {b: (c["lost"] + c["pending"] * resolved_share(c)) / c["n"] for b, c in counts(p).items()}


def loss_at(p, rate):
    """each build's settled losses plus its open purchases at a given resolved share: rate(build, counts) -> share"""
    return {b: (c["lost"] + c["pending"] * rate(b, c)) / c["n"] for b, c in counts(p).items()}


def corridor(p, starts=None):
    """the rates the open purchases could take: the build's own, its platform's and the pooled resolved share, and an
    open purchase counted lost once its phone has been silent longer than the phone's longest earlier gap"""
    C = counts(p)
    pool = lambda bs: sum(C[b]["lost"] for b in bs) / sum(C[b]["lost"] + C[b]["held"] for b in bs)
    plat = {pl: pool([b for b in C if b[0] == pl]) for pl in ("ios", "android")}
    allq = pool(list(C))
    out = {"own": loss_at(p, lambda b, c: resolved_share(c)),
           "platform": loss_at(p, lambda b, c: plat[b[0]]),
           "pooled": loss_at(p, lambda b, c: allq)}
    if starts is not None:
        sil = {}
        for b, g in p[~p.due & ~p.matched].groupby("build"):
            q = resolved_share(C[b])
            tot = 0.0
            for dev, t in zip(g.device_id, g.t):
                s = starts.get(dev)
                gaps = np.diff(s).astype("timedelta64[s]").astype(float) / 86400 if s is not None and len(s) > 1 else []
                longest = max(gaps) if len(gaps) else 17.0
                tot += 1.0 if (RUN - t).total_seconds() / 86400 > longest else q
            sil[b] = tot
        out["silence"] = {b: (c["lost"] + sil.get(b, 0.0)) / c["n"] for b, c in C.items()}
    return out, plat, allq


def flip_share(c):
    """the share of a build's pending events that would have to be lost for it to cross the line"""
    return (LINE * c["n"] - c["lost"]) / c["pending"] if c["pending"] else float("inf")


def loss_due(p):
    """among purchases whose phone has opened the game since, the share whose event is missing"""
    return {b: 1 - g[g.due].matched.mean() for b, g in p.groupby("build")}


def loss_bounds(p):
    """every pending event delivered (low) or lost (high)"""
    c = counts(p)
    return ({b: x["lost"] / x["n"] for b, x in c.items()}, {b: (x["lost"] + x["pending"]) / x["n"] for b, x in c.items()})


def loss_due_account(p):
    """each missing event judged against the next session of the account rather than of the phone"""
    out = {}
    for b, g in p.groupby("build"):
        lost = int((g.due_account & ~g.matched).sum())
        held = int((g.matched & g.due_account & (g.recv >= g.next_account)).sum())
        pend = int((~g.due_account & ~g.matched).sum())
        q = lost / (lost + held) if lost + held else 0.0
        out[b] = (lost + pend * q) / len(g)
    return out


def loss_settled(p, days):
    """a purchase counted as lost when its event is still missing `days` after it"""
    out = {}
    for b, g in p.groupby("build"):
        x = g[g.age_d >= days]
        out[b] = 1 - x.matched.mean() if len(x) else float("nan")
    return out


def loss_settled_all(p, days):
    """the same, the younger purchases kept in the denominator as not yet lost"""
    return {b: float(((g.age_d >= days) & ~g.matched).sum()) / len(g) for b, g in p.groupby("build")}


def loss_curve(p, plateau=21):
    """a pooled arrival curve: the matched share by purchase age over the matched share of purchases old enough to have
    settled, applied to each build's purchases"""
    age = np.floor(p.age_d).astype(int)
    m_inf = p[p.age_d >= plateau].matched.mean()
    F = (p.groupby(age).matched.mean() / m_inf).clip(upper=1.0)
    f = age.map(F).values
    out = {}
    for b, idx in p.groupby("build").groups.items():
        g = p.loc[idx]
        out[b] = 1 - (g.matched.values / f[p.index.get_indexer(idx)]).sum() / len(g)
    return out


def short_windows(p, windows=(0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0)):
    """the 7.42.0 builds judged on their purchases at least `w` days old: window -> {build: (loss, purchases)}"""
    out = {}
    for w in windows:
        r = {}
        for b in NEW:
            g = p[(p.build == b) & (p.age_d >= w)]
            r[b] = (1 - g.matched.mean() if len(g) else float("nan"), len(g))
        out[w] = r
    return out


def age_matched(p):
    """each 7.42.0 build's missing share against the missing share of its platform's other builds' purchases of the
    same age (half-day bins over the 7.42.0 builds' ages)"""
    out = {}
    q = p.assign(bin=np.floor(p.age_d * 2) / 2)
    for b in NEW:
        g = q[q.build == b]
        o = q[(q.build.map(lambda x: x[0]) == b[0]) & ~q.build.isin(NEW) & (q.age_d <= g.age_d.max())]
        ref = 1 - o.groupby("bin").matched.mean()
        out[b] = (1 - g.matched.mean(), float(g.bin.map(ref).mean()))
    return out


def alerted(loss_):
    return {b for b, x in loss_.items() if x == x and x > LINE}


# ------------------------------------------------------------------ ask A: paying players
def resolve(links):
    """each account id to the account its history finally moved to"""
    nxt = dict(zip(links.from_account_id, links.to_account_id))

    def final(a):
        seen = set()
        while a in nxt and a not in seen:
            seen.add(a)
            a = nxt[a]
        return a
    return final


def signed_in_to(D, with_events=False):
    """each guest account to the account its device shows next: the account the guest signed in to, read from the
    purchase service's validations and the session service's starts (and the warehouse's events when asked)"""
    v = D["val"]
    v = v[(v.device_id != "") & (v.account_id != "")]
    s = D["ses"]
    parts = [pd.DataFrame({"device": v.device_id.values, "t": utc(v.purchased_at).values, "acct": v.account_id.values}),
             pd.DataFrame({"device": s.device_id.values, "t": utc(s.started_at).values, "acct": s.account_id.values})]
    if with_events:
        e = D["evt"]
        parts.append(pd.DataFrame({"device": e.device_id.values,
                                   "t": pd.to_datetime(e.client_ts.astype("int64"), unit="ms").values,
                                   "acct": e.account_id.values}))
    x = pd.concat(parts)
    x = x.sort_values(["device", "t"], kind="mergesort").reset_index(drop=True)
    nx = x.groupby("device").acct.shift(-1)
    m = x.acct.str.startswith("gst_") & nx.notna() & ~nx.fillna("gst_").str.startswith("gst_")
    return dict(zip(x.acct[m], nx[m]))


def players(D, devices=True, with_events=False):
    """each account to its player: the account links, and with devices=True each guest account joined to the account
    it signed in to"""
    parent = {}

    def find(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    edges = list(zip(D["links"].from_account_id, D["links"].to_account_id))
    if devices:
        edges += list(signed_in_to(D, with_events).items())
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return find


def paying_players(D, p, how="golden"):
    if how == "account":
        return p.groupby("build").account_id.nunique().to_dict()
    if how == "one_hop":
        nxt = dict(zip(D["links"].from_account_id, D["links"].to_account_id))
        return p.assign(pl=p.account_id.map(lambda a: nxt.get(a, a))).groupby("build").pl.nunique().to_dict()
    find = players(D, devices=(how == "golden"))
    return p.assign(pl=p.account_id.map(find)).groupby("build").pl.nunique().to_dict()


# ------------------------------------------------------------------ ask B: gross bookings in euro
def bookings(D, p, minor="iso", rate="in_force", per_line=True):
    r = D["rates"].copy()
    r["date"] = pd.to_datetime(r.date).dt.date
    price = p.price_minor.astype(float)
    exp = p.currency.map(lambda c: EXPONENT.get(c, 2) if minor == "iso" else 2)
    local = price / (10.0 ** exp)
    days = sorted(r.date.unique())
    tab = r.pivot(index="date", columns="currency", values="rate")
    out = []
    for c, d, x in zip(p.currency, p.day, local):
        if c == "EUR":
            out.append(float(x)); continue
        if rate == "in_force":
            k = [dd for dd in days if dd <= d][-1]
        elif rate == "next":
            k = [dd for dd in days if dd >= d][0] if any(dd >= d for dd in days) else days[-1]
        else:                                   # the date's own rate, or none
            if d not in tab.index:
                out.append(0.0); continue
            k = d
        out.append(x / tab.loc[k, c])
    eur = np.round(np.array(out, dtype=float) + 1e-9, 2) if per_line else np.array(out, dtype=float)
    return p.assign(eur=eur).groupby("build").eur.sum().round(2).to_dict()


def per_player(bk, pl):
    """gross bookings per paying player: the build's total in cents over its paying players, half up to the cent"""
    out = {}
    for b in bk:
        x = Decimal(int(round(bk[b] * 100))) / Decimal(100) / Decimal(int(pl[b]))
        out[b] = float(x.quantize(Decimal("0.01"), ROUND_HALF_UP))
    return out


def per_player_raw(bk, pl):
    return {b: float(Decimal(int(round(bk[b] * 100))) / Decimal(100) / Decimal(int(pl[b]))) for b in bk}


def solve(target, files):
    D = load(target, files)
    p = conform(D)
    C = counts(p)
    gold = loss(p)
    lo, hi = loss_bounds(p)
    routes = {"due": loss_due(p), "account": loss_due_account(p), "curve": loss_curve(p), "lower": lo, "upper": hi}
    for d in (0, 1, 3, 7, 11, 14):
        routes["settle%d" % d] = loss_settled(p, d)
        routes["settle%d_all" % d] = loss_settled_all(p, d)
    cor, plat, allq = corridor(p, session_starts(D))
    v = D["val"]
    refunded = set(v[v.transaction_kind == "refund"].store_transaction_id)
    pt = purchases(D, testers=True)
    pl = {how: paying_players(D, p, how) for how in ("golden", "chain", "one_hop", "account")}
    find = players(D)
    pl["testers_in"] = pt.assign(pl=pt.account_id.map(find)).groupby("build").pl.nunique().to_dict()
    pr = p[~p.store_transaction_id.isin(refunded)]
    pl["refunded_out"] = pr.assign(pl=pr.account_id.map(find)).groupby("build").pl.nunique().to_dict()
    bk = {"golden": bookings(D, p), "all2": bookings(D, p, minor="all2"), "next": bookings(D, p, rate="next"),
          "testers_in": bookings(D, pt), "unrounded": bookings(D, p, per_line=False)}
    net = bookings(D, p[p.store_transaction_id.isin(refunded)])
    bk["refunds_netted"] = {b: round(bk["golden"][b] - net.get(b, 0.0), 2) for b in bk["golden"]}
    pp = {"golden": per_player(bk["golden"], pl["golden"])}
    for how in ("chain", "one_hop", "account", "refunded_out"):
        pp[how] = per_player(bk["golden"], pl[how])
    for how in ("all2", "next", "unrounded", "refunds_netted"):
        pp[how] = per_player(bk[how], pl["golden"])
    pp["testers_in"] = per_player(bk["testers_in"], pl["testers_in"])
    return dict(D=D, p=p, counts=C, gold=gold, esc=alerted(gold), lo=lo, hi=hi, routes=routes, corridor=cor,
                plat_q=plat, pooled_q=allq, short=short_windows(p), matched_age=age_matched(p), players=pl, bookings=bk,
                per_player=pp, per_player_raw=per_player_raw(bk["golden"], pl["golden"]))
