"""The golden computation, run on the tables the pack ships (as DataFrames, before writing).

Every rung, every grid cell, every ask figure and every device stop is a function of the shipped
tables and a set of reading options; the default options are the golden path."""
import datetime as dt
import re

import numpy as np
import pandas as pd

import params as P

FIX = {"P1": "F1", "P2": "F2", "P3": "F3", "P4": "F4", "P5": "F5"}
POPS = ["P1", "P2", "P3", "P4", "P5"]
GOLD = dict(keep_bots=False, clock_raw=False, cards_current=False, tokens_sep_only=False,
            catalogue_current=False, cohort_current=False, drop_touched=False, identity="union",
            cohort_lastmove=False)
SOCIO = re.compile(r"SOCIO(\d{7})")
WEEK_EDGES = [pd.Timestamp(x) for x in P.WEEK_STARTS] + [pd.Timestamp(P.END)]


def weeks_of(t):
    idx = np.searchsorted(np.array(WEEK_EDGES[:-1], dtype="datetime64[ns]"), t.to_numpy(), side="right") - 1
    return np.array(P.WEEK_NAMES)[idx]


def opts(**kw):
    o = dict(GOLD)
    o.update(kw)
    return o


def enrich(pack, o=GOLD):
    """One row per basket session with every classification the ladder and the asks need."""
    s = pack["sessions"].copy()
    s["t"] = pd.to_datetime(s.started_at).astype("datetime64[ns]")
    s["week"] = weeks_of(s.t)
    s["conv"] = s.order_id.notna()
    bots = set(pack["edge"].session_id)
    s["bot"] = s.session_id.isin(bots)
    if o["drop_touched"]:
        tok_all = s.landing_url.str.extract(r"mpt=([A-Z0-9]+)")[0]
        bt = set(tok_all[s.bot].dropna())
        ba = set(s.account_id[s.bot].dropna())
        s = s[~(tok_all.isin(bt) | s.account_id.isin(ba))].copy()
    elif not o["keep_bots"]:
        s = s[~s.bot].copy()
    s["club"] = s.traffic_source == "club_app"
    s["token"] = s.landing_url.str.extract(r"mpt=([A-Z0-9]+)")[0]
    s["vtype"] = np.where(s.signed_in, "SI", np.where(s.club, "CLUB", np.where(s.new_visitor, "NV", "RG")))
    # the club's token reports joined to loyalty profiles
    tk = pack["tokens_sep"] if o["tokens_sep_only"] else pd.concat([pack["tokens_aug"], pack["tokens_sep"]])
    t2m = dict(zip(tk.token, tk.member_no))
    s["member_no"] = s.token.map(t2m)
    m2a = member_accounts(pack, o["identity"])
    s["chain_account"] = s.member_no.map(lambda m: m2a.get(int(m)) if pd.notna(m) else None)
    s["P4"] = s.club & s.chain_account.notna()
    s["P2"] = s.club & s.chain_account.isna()
    # flag cohort as of the session, and whether the cohort was live
    fl = pack["flags"]
    live = {d["cohort"]: pd.Timestamp(d["enabled_at"][:19]) for d in fl["rollout"]}
    cohort_at = cohort_reader(fl, "current" if o["cohort_current"] else "lastmove" if o["cohort_lastmove"] else "asof")
    coh = []
    for a, t, si in zip(s.account_id, s.t, s.signed_in):
        coh.append(int(cohort_at(a, t)) if si else 0)
    s["cohort"] = coh
    s["live"] = [c > 0 and t >= live[c] for c, t in zip(s.cohort, s.t)]
    # default delivery address as of the session (address book times are UTC)
    ab = pack["address"]
    ab = ab[ab.is_default].copy()
    ab["tl"] = (pd.to_datetime(ab.changed_at) + (pd.Timedelta(0) if o["clock_raw"] else pd.Timedelta(hours=1))
                ).astype("datetime64[ns]")
    ab = ab.sort_values("tl")
    si = s[s.signed_in].sort_values("t")
    m = pd.merge_asof(si[["session_id", "t", "account_id"]], ab[["account_id", "tl", "postcode"]],
                      left_on="t", right_on="tl", by="account_id", direction="backward")
    pc = dict(zip(m.session_id, m.postcode))
    s["postcode"] = s.session_id.map(pc)
    s["cp4"] = s.postcode.fillna("").str.fullmatch(r"\d{4}")
    s["P1"] = s.signed_in & s.live & s.cp4
    # default saved card as of the session
    cards = pack["cards"]
    iss = dict(zip(cards.card_id, cards.issuer))
    dflt = dict(zip(cards.account_id[cards.is_default], cards.card_id[cards.is_default]))
    ch = pack["card_changes"]
    sd = ch[ch.event == "set_default"]
    prev = {a: (pd.Timestamp(at), p) for a, at, p in zip(sd.account_id, sd["at"], sd.previous_default_card_id)}
    card = []
    for a, t, sg in zip(s.account_id, s.t, s.signed_in):
        if not sg:
            card.append(None)
            continue
        c = dflt[a]
        if not o["cards_current"] and a in prev and t < prev[a][0]:
            c = prev[a][1]
        card.append(c)
    s["issuer"] = [iss.get(c) if c else None for c in card]
    s["P3"] = s.signed_in & s.issuer.isin([P.ISSUER_X, P.ISSUER_Y])
    # baskets mixing pre-order and in-stock lines, status as of the session
    cat = pack["catalogue"].copy()
    cat["vf"] = pd.to_datetime(cat.valid_from)
    hist = {k: list(zip(g.vf, g.status)) for k, g in cat.sort_values("vf").groupby("sku")}

    def status(sku, t):
        h = hist[sku]
        if o["catalogue_current"]:
            return h[-1][1]
        st = None
        for vf, x in h:
            if vf <= t:
                st = x
        return st
    mixed = []
    for b, t in zip(s.basket_skus, s.t):
        sts = [status(x, t) for x in b.split(";")]
        mixed.append("pre_order" in sts and "in_stock" in sts)
    s["P5"] = mixed
    return s.reset_index(drop=True)


def cohort_reader(fl, mode="asof"):
    """The flag cohort of an account at a time. asof: the latest move at or before the time, else the
    first move's origin, else the assignment at extract. current: the assignment at extract.
    lastmove: one move kept per account (the last), the reading a dict keyed on the account gives."""
    cur = {d["account_id"]: d["cohort"] for d in fl["assignments"]}
    moves = {}
    for d in fl["assignment_moves"]:
        moves.setdefault(d["account_id"], []).append((pd.Timestamp(d["moved_at"][:19]), d["from_cohort"], d["to_cohort"]))
    for v in moves.values():
        v.sort()

    def at(a, t):
        if mode == "current" or a not in moves:
            return cur[a]
        mv = moves[a]
        if mode == "lastmove":
            return mv[-1][1] if t < mv[-1][0] else cur[a]
        c = mv[0][1]
        for when, _, to in mv:
            if when <= t:
                c = to
        return c
    return at


def member_accounts(pack, identity="union"):
    """Member number to store account. profile: the loyalty profile's club_member_no alone (the visible
    key). union: that, plus last season's members' code (SOCIO and the seven-digit member number)
    redeemed on an account."""
    pr = pack["profiles"].dropna(subset=["club_member_no"])
    m2a = dict(zip(pr.club_member_no.astype(int), pr.account_id))
    if identity == "union":
        pm = pack["promo"].dropna(subset=["account_id"])
        for code, a in zip(pm.promo_code, pm.account_id):
            mt = SOCIO.fullmatch(code)
            if mt:
                m2a.setdefault(int(mt.group(1)), a)
    return m2a


# --------------------------------------------------------------------------- populations and losses

def pop_accounts(s, pop, weeks=P.REVIEW):
    r = s[s.week.isin(weeks) & s[pop]]
    col = "chain_account" if pop == "P4" else "account_id"
    return set(r[col].dropna())


def baselines(s, mode="own", weeks=tuple(P.BASE), acct_weeks=tuple(P.REVIEW)):
    """Each population's pre-fall conversion. mode own: the population's own customers (accounts for
    P1, P3, P4; web new visitors for P2, by the close-outs' convention; mixed baskets for P5)."""
    b = s[s.week.isin(weeks)]
    out = {}
    si = b[b.signed_in]
    for p in ("P1", "P3", "P4"):
        if mode == "signed_in":
            out[p] = si.conv.mean()
        else:
            acc = pop_accounts(s, p, acct_weeks)
            x = si[si.account_id.isin(acc)]
            out[p] = x.conv.mean()
    out["P2"] = b[b.vtype == "NV"].conv.mean()
    out["P5"] = b[b.P5].conv.mean()
    out["store"] = b.conv.mean()
    for v in ("SI", "NV", "RG"):
        out[v] = b[b.vtype == v].conv.mean()
    out["P5_by_type"] = {v: b[b.P5 & (b.vtype == v)].conv.mean() for v in ("SI", "NV", "RG")}
    return out


def losses(s, base, weeks=P.WEEK_NAMES[1:]):
    out = {}
    for p in POPS:
        out[p] = {}
        for w in weeks:
            x = s[(s.week == w) & s[p]]
            out[p][w] = len(x) * base[p] - x.conv.sum()
    return out


def _flags(mode):
    if mode in (None, "golden"):
        return set()
    return {mode} if isinstance(mode, str) else set(mode)


def finance_values(pack, mode="golden"):
    fl = _flags(mode)
    f = pack["finance"].copy()
    f["exp"] = pd.to_datetime(f.exported_at)
    if "pre_correction" in fl:
        first = f.groupby("order_id").exp.transform("min")
        f = f[f.exp == first]
    else:
        last = f.groupby("order_id").exp.transform("max")
        f = f[f.exp == last]
    if "gross_kept" not in fl:
        gross = f.exp < pd.Timestamp(P.FINANCE_NET_FROM)
        f.loc[gross, "order_total_eur"] = f.loc[gross, "order_total_eur"] / (1 + P.VAT)
    if "rows_summed" in fl:
        return f.groupby("order_id").order_total_eur.sum().to_dict()
    return f.groupby("order_id").order_total_eur.first().to_dict()


def aovs(pack, s, mode="golden"):
    fl = _flags(mode)
    val = finance_values(pack, tuple(fl - {"store_wide"}))
    b = s[s.week.isin(P.BASE) & s.conv]
    out = {}
    if "store_wide" in fl:
        v = b.order_id.map(val).mean()
        return {p: v for p in POPS}
    for p in ("P1", "P3", "P4"):
        acc = pop_accounts(s, p)
        out[p] = b[b.signed_in & b.account_id.isin(acc)].order_id.map(val).mean()
    out["P2"] = b[b.vtype == "NV"].order_id.map(val).mean()
    out["P5"] = b[b.P5].order_id.map(val).mean()
    return out


def challenge_shares(pack, s, mode="golden", week="W4"):
    fl = _flags(mode)
    a = pack["auth"]
    sid = {p: set(s.session_id[(s.week == week) & s[p]]) for p in POPS}
    rows = a if "rows" in fl else a.drop_duplicates("attempt_ref")
    ch = ("C",) if "C_only" in fl else ("C", "D")
    out = {}
    for p in POPS:
        x = rows[rows.session_id.isin(sid[p])]
        k = int(x.three_ds_status.isin(ch).sum())
        out[p] = (100.0 * k / len(x), k, len(x))
    return out


def cohort_sheet(s, fold_club=False, pack=None):
    x = s[s.week.isin(P.REVIEW) & s.signed_in][["cohort", "conv"]]
    if fold_club:
        at = cohort_reader(pack["flags"])
        c4 = s[s.week.isin(P.REVIEW) & s.P4].copy()
        c4["cohort"] = [at(a, t) for a, t in zip(c4.chain_account, c4.t)]
        x = pd.concat([x, c4[["cohort", "conv"]]])
    g = x.groupby("cohort").conv.agg(["size", "sum"])
    return {int(c): (int(r["size"]), 100.0 * r["sum"] / r["size"]) for c, r in g.iterrows()}


# --------------------------------------------------------------------------- rungs

STEP_FIX = {"basket": "F2", "contact": "F4", "address": "F1", "delivery": "F5", "payment": "F3"}


def stage_table(s, weeks=P.REVIEW, exclude_club=False):
    x = s[~s.club] if exclude_club else s
    idx = x.furthest_step.map({k: i for i, k in enumerate(P.STEPS)})
    out = {}
    b = x.week.isin(P.BASE)
    r = x.week.isin(weeks)
    for i, st in enumerate(P.STEPS[:5]):
        reach = idx >= i
        ex = idx == i
        rate = ex[b].sum() / reach[b].sum()
        out[STEP_FIX[st]] = float(ex[r].sum() - reach[r].sum() * rate)
    return out


def rank(d):
    return sorted(d, key=lambda k: -d[k])


def rungs(s, base, L):
    """R0 to R4 on the latest complete week (R0 over the four review weeks), by fix."""
    w4 = s[s.week == "W4"]
    R = {}
    R["R0"] = stage_table(s)
    st = base["store"]

    def short(mask, r):
        x = w4[mask]
        return float(len(x) * r - x.conv.sum())
    R["R1"] = {"F1": L["P1"]["W4"], "F2": short(w4.club, st), "F3": short(w4.P3, st),
               "F4": short(w4.vtype == "RG", st), "F5": short(w4.P5, st)}
    f5_type = sum(short(w4.P5 & (w4.vtype == v), base[v]) for v in ("SI", "NV", "RG"))
    R["R2"] = {"F1": L["P1"]["W4"], "F2": short(w4.club, base["NV"]), "F3": short(w4.P3, base["SI"]),
               "F4": short(w4.vtype == "RG", base["RG"]), "F5": f5_type}
    R["R3"] = {"F1": L["P1"]["W4"], "F2": short(w4.club, base["NV"]), "F3": L["P3"]["W4"],
               "F4": short(w4.vtype == "RG", base["RG"]), "F5": L["P5"]["W4"]}
    R["R4"] = {FIX[p]: L[p]["W4"] for p in POPS}
    return R


def by_step_cell(s, base, L):
    """Re-attached club sessions, their lost orders booked to the step where they exceed the
    accounts' signed-in exits (W4)."""
    acc = pop_accounts(s, "P4")
    b = s[s.week.isin(P.BASE) & s.signed_in & s.account_id.isin(acc)]
    w4 = s[(s.week == "W4") & s.P4]
    ib = b.furthest_step.map({k: i for i, k in enumerate(P.STEPS)})
    iw = w4.furthest_step.map({k: i for i, k in enumerate(P.STEPS)})
    exc = {}
    for i, st in enumerate(P.STEPS[:5]):
        rate = (ib == i).sum() / (ib >= i).sum()
        exc[STEP_FIX[st]] = float((iw == i).sum() - (iw >= i).sum() * rate)
    tot = sum(max(v, 0) for v in exc.values())
    share = {k: max(v, 0) / tot for k, v in exc.items()}
    p4 = L["P4"]["W4"]
    out = {"F1": L["P1"]["W4"] + p4 * share["F1"], "F2": L["P2"]["W4"] + p4 * share["F2"],
           "F3": L["P3"]["W4"] + p4 * share["F3"], "F4": p4 * share["F4"], "F5": L["P5"]["W4"] + p4 * share["F5"]}
    return out, share


# --------------------------------------------------------------------------- everything graded

def figures(pk, s, fin_mode="golden", auth_mode="golden", base_mode="own", base_weeks=tuple(P.BASE)):
    base = baselines(s, base_mode, base_weeks)
    L = losses(s, base)
    av = aovs(pk, s, fin_mode)
    sh = challenge_shares(pk, s, auth_mode)
    g = {"base": base, "L": L, "aov": av}
    g["L1"] = {p: sum(L[p][w] for w in P.REVIEW) for p in POPS}
    g["L2"] = {p: L[p]["W1"] for p in POPS}
    g["W4"] = {p: L[p]["W4"] for p in POPS}
    g["L3"] = {p: L[p]["W4"] * av[p] for p in POPS}
    g["L4"] = {p: sh[p][0] for p in POPS}
    g["L4_kn"] = {p: (sh[p][1], sh[p][2]) for p in POPS}
    order = rank({FIX[p]: g["W4"][p] for p in POPS})
    g["call"], g["runner_up"] = order[0], order[1]
    inv = {v: k for k, v in FIX.items()}
    g["call_w4"] = g["W4"][inv[order[0]]]
    g["gap"] = g["W4"][inv[order[0]]] - g["W4"][inv[order[1]]]
    return g
