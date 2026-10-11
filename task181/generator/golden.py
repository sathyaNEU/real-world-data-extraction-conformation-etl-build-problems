"""The golden solve: reads only ../target/ and computes every graded figure.

    python3 golden.py            prints the figures
    python3 golden.py --write    also writes ../golden/card_reissue_request.pdf and common_point_trace.xlsx

Screens, exposure counts and the ask computations are parameterised so checks.py can run every rung, grid
cell and ask stop on the same shipped bytes.
"""
import datetime as dt
import functools
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
GOLDEN = os.path.join(HERE, "..", "golden")
TZ = "America/Toronto"
CONTACT = ("05", "80", "90")
CARD_PRESENT = ("05", "07", "80", "90", "91")
EXTRACT = dt.date(2026, 10, 5)


def tp(prefix):
    return os.path.join(TARGET, next(f for f in sorted(os.listdir(TARGET)) if f.startswith(prefix)))


# loaders ------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def auth():
    df = pd.read_parquet(tp("card_authorisations"))
    df["local"] = df.txn_datetime_utc.dt.tz_convert(TZ)
    df["ldate"] = df["local"].dt.date
    return df


@functools.lru_cache(maxsize=None)
def cards():
    p = tp("card_history")
    c = pd.read_excel(p, sheet_name="Cards", header=3, dtype={"card_token": str, "member_id": str})
    r = pd.read_excel(p, sheet_name="Replacements", header=3, dtype={"old_card_token": str, "new_card_token": str})
    m = pd.read_excel(p, sheet_name="Members", header=3, dtype={"member_id": str})
    return c, r, m


@functools.lru_cache(maxsize=None)
def cases():
    w = pd.read_excel(tp("fraud_cases"), sheet_name="Disputed transactions", header=3,
                      dtype={"card_token": str, "member_id": str, "retrieval_ref": str, "case_number": str})
    w["txn_date"] = pd.to_datetime(w.txn_date).dt.date
    w["refunded_on"] = pd.to_datetime(w.refunded_on).dt.date
    return w


@functools.lru_cache(maxsize=None)
def merchants():
    return pd.read_csv(tp("merchant_directory"), dtype=str)


@functools.lru_cache(maxsize=None)
def chargebacks():
    return pd.read_csv(tp("chargebacks"), dtype={"retrieval_ref": str, "card_token": str})


@functools.lru_cache(maxsize=None)
def holidays():
    from docx import Document
    doc = Document(tp("MS-3"))
    out = set()
    for row in doc.tables[0].rows[1:]:
        out.add(dt.datetime.strptime(row.cells[0].text.strip(), "%a %d %b %Y").date())
    return frozenset(out)


# the counterfeit cards ------------------------------------------------------------------------------
def victims():
    w = cases()
    cf = w[w.fraud_type == "Counterfeit"]
    return cf.groupby("card_token").txn_date.min().to_dict()


# common-point screen ----------------------------------------------------------------------------------
def screen(vic, L=60, base="span", modes="contact"):
    a = auth()
    mset = CONTACT if modes == "contact" else CARD_PRESENT
    f = pd.Series(vic)
    span0 = min(vic.values()) - dt.timedelta(L)
    span1 = max(vic.values()) - dt.timedelta(1)
    isv = a.card_token.isin(f.index)
    rd = a[isv & a.pos_entry_mode.isin(mset) & a.terminal_id.notna()]
    fd = rd.card_token.map(f)
    lo = fd - pd.to_timedelta(L, unit="D")
    ld = pd.to_datetime(rd.ldate)
    inlb = (ld >= pd.to_datetime(lo)) & (ld < pd.to_datetime(fd))
    v = rd[inlb.values].groupby("terminal_id").card_token.nunique()
    if base == "span":
        ins = (a.ldate >= span0) & (a.ldate <= span1)
    else:
        ins = pd.Series(True, index=a.index)
    nv = a[ins & ~isv]
    n_act = nv.card_token.nunique()
    b = nv[nv.pos_entry_mode.isin(mset) & nv.terminal_id.notna()].groupby("terminal_id").card_token.nunique()
    out = pd.DataFrame({"v": v}).join(pd.DataFrame({"b": b}), how="left").fillna({"b": 0})
    out["share_v"] = out.v / len(vic)
    out["base"] = out.b / n_act
    out["lift"] = np.where(out.b > 0, out.share_v / out.base.where(out.base > 0, np.nan), np.inf)
    out.attrs["n_v"], out.attrs["n_act"] = len(vic), n_act
    return out.sort_values(["lift", "v"], ascending=[False, False])


def victims_read_at(vic, tid, L=60, modes="contact"):
    a = auth()
    mset = CONTACT if modes == "contact" else CARD_PRESENT
    r = a[(a.terminal_id == tid) & a.card_token.isin(list(vic)) & a.pos_entry_mode.isin(mset)]
    keep = set()
    for tok, d in zip(r.card_token, r.ldate):
        f = vic[tok]
        if f - dt.timedelta(L) <= d < f:
            keep.add(tok)
    return keep


def sequential(vic, L=60, base="span", modes="contact", floor=10, stop=3.0):
    """Attribute the victims a terminal read to the terminal with the highest lift among those that read at
    least `floor` of the victims still unexplained; screen the rest; stop when nothing stands above `stop`."""
    rem = dict(vic)
    chosen = []
    while len(rem) >= floor:
        sc = screen(rem, L, base, modes)
        cand = sc[sc.v >= floor]
        if not len(cand) or not cand.lift.iloc[0] > stop:
            break
        top = cand.index[0]
        chosen.append(top)
        hit = victims_read_at(rem, top, L, modes)
        rem = {k: v for k, v in rem.items() if k not in hit}
    return chosen, rem


def set_cover(vic, L=60, base="span", modes="contact", floor=10, stop=3.0):
    """Greedy cover: the terminal that explains the most unexplained victims, among terminals whose lift on the
    unexplained victims is above `stop`."""
    rem = dict(vic)
    chosen = []
    while len(rem) >= floor:
        sc = screen(rem, L, base, modes)
        cand = sc[(sc.v >= floor) & (sc.lift > stop)]
        if not len(cand):
            break
        top = cand.sort_values(["v", "lift"], ascending=[False, False]).index[0]
        chosen.append(top)
        hit = victims_read_at(rem, top, L, modes)
        rem = {k: v for k, v in rem.items() if k not in hit}
    return chosen, rem


def logistic(vic, L=60, base="span", modes="contact", floor=10, z_min=4.0, or_min=3.0):
    """Victim status on exposure to every terminal that read at least `floor` victims, fitted jointly;
    terminals whose own effect holds with the others in the model."""
    sc = screen(vic, L, base, modes)
    cand = list(sc[sc.v >= floor].index)
    a = auth()
    mset = CONTACT if modes == "contact" else CARD_PRESENT
    span0 = min(vic.values()) - dt.timedelta(L)
    span1 = max(vic.values()) - dt.timedelta(1)
    ins = (a.ldate >= span0) & (a.ldate <= span1) if base == "span" else pd.Series(True, index=a.index)
    toks = sorted(set(a.card_token[ins & ~a.card_token.isin(list(vic))]) | set(vic))
    idx = {t: i for i, t in enumerate(toks)}
    X = np.zeros((len(toks), len(cand)))
    y = np.array([1.0 if t in vic else 0.0 for t in toks])
    rd = a[a.terminal_id.isin(cand) & a.pos_entry_mode.isin(mset)]
    f = pd.Series(vic)
    for j, tid in enumerate(cand):
        r = rd[rd.terminal_id == tid]
        isv = r.card_token.isin(f.index)
        rv = r[isv]
        fd = rv.card_token.map(f)
        ok_v = (pd.to_datetime(rv.ldate) >= pd.to_datetime(fd) - pd.to_timedelta(L, unit="D")) & \
            (pd.to_datetime(rv.ldate) < pd.to_datetime(fd))
        rn = r[~isv & ((r.ldate >= span0) & (r.ldate <= span1) if base == "span" else True)]
        for t in set(rv.card_token[ok_v.values]) | set(rn.card_token):
            if t in idx:
                X[idx[t], j] = 1.0
    Xd = np.column_stack([np.ones(len(toks)), X])
    lam = 1.0
    pen = lam * np.r_[0.0, np.ones(len(cand))]

    def sig(z):
        return 0.5 * (1 + np.tanh(0.5 * z))

    def obj(bt):
        z = Xd @ bt
        return float(np.sum(y * z - np.logaddexp(0, z)) - 0.5 * np.sum(pen * bt * bt))

    beta = np.zeros(Xd.shape[1])
    beta[0] = np.log(y.mean() / (1 - y.mean()))
    cur = obj(beta)
    for _ in range(100):
        p = sig(Xd @ beta)
        H = Xd.T @ (Xd * (p * (1 - p))[:, None]) + np.diag(pen) + 1e-9 * np.eye(len(beta))
        g = Xd.T @ (y - p) - pen * beta
        step = np.linalg.solve(H, g)
        t = 1.0
        while t > 1e-6:
            nb = beta + t * step
            nv = obj(nb)
            if nv >= cur - 1e-12:
                break
            t *= 0.5
        beta, done = nb, abs(nv - cur) < 1e-10
        cur = nv
        if done:
            break
    p = sig(Xd @ beta)
    H = Xd.T @ (Xd * (p * (1 - p))[:, None]) + np.diag(pen) + 1e-9 * np.eye(len(beta))
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    z = beta / se
    res = pd.DataFrame({"beta": beta[1:], "z": z[1:], "odds_ratio": np.exp(beta[1:])}, index=cand)
    chosen = list(res[(res.z > z_min) & (res.odds_ratio > or_min)].index)
    return chosen, res


# exposure and reissue --------------------------------------------------------------------------------
def window(tid, vic, modes="contact"):
    """First and last read at the terminal of a card later used in counterfeit fraud (reads before the
    card's first counterfeit use), as UTC timestamps."""
    a = auth()
    mset = CONTACT if modes == "contact" else CARD_PRESENT
    r = a[(a.terminal_id == tid) & a.card_token.isin(list(vic)) & a.pos_entry_mode.isin(mset)]
    r = r[[d < vic[t] for t, d in zip(r.card_token, r.ldate)]]
    return r.txn_datetime_utc.min(), r.txn_datetime_utc.max()


def exposed(tid, vic, modes="contact", edge="instant"):
    a = auth()
    mset = CONTACT if modes == "contact" else CARD_PRESENT
    t0, t1 = window(tid, vic, modes)
    r = a[(a.terminal_id == tid) & a.pos_entry_mode.isin(mset)]
    if edge == "instant":
        r = r[(r.txn_datetime_utc >= t0) & (r.txn_datetime_utc <= t1)]
    elif edge == "eastern_dates":
        d0, d1 = t0.tz_convert(TZ).date(), t1.tz_convert(TZ).date()
        r = r[(r.ldate >= d0) & (r.ldate <= d1)]
    elif edge == "utc_dates":
        d0, d1 = t0.date(), t1.date()
        ud = r.txn_datetime_utc.dt.date
        r = r[(ud >= d0) & (ud <= d1)]
    return set(r.card_token)


@functools.lru_cache(maxsize=None)
def all_exposures(modes="contact"):
    """Every terminal's exposed card set: its window from the counterfeit cards it read (before their first
    use), then every card it read inside the window."""
    a = auth()
    vic = victims()
    mset = CONTACT if modes == "contact" else CARD_PRESENT
    r = a[a.pos_entry_mode.isin(mset) & a.terminal_id.notna()][["terminal_id", "card_token", "txn_datetime_utc",
                                                                "ldate"]]
    fv = r.card_token.map(pd.Series(vic))
    vr = r[fv.notna().values]
    vr = vr[(pd.to_datetime(vr.ldate) < pd.to_datetime(vr.card_token.map(pd.Series(vic)))).values]
    win = vr.groupby("terminal_id").txn_datetime_utc.agg(["min", "max"])
    j = r.join(win, on="terminal_id", how="inner")
    j = j[(j.txn_datetime_utc >= j["min"]) & (j.txn_datetime_utc <= j["max"])]
    return {t: frozenset(g.card_token) for t, g in j.groupby("terminal_id")}


def open_cards():
    c, _, _ = cards()
    return set(c.card_token[c.status == "Open"])


def reissue(tids, vic=None, modes="contact", edge="instant", status="open"):
    vic = vic or victims()
    toks = set()
    for t in tids:
        toks |= exposed(t, vic, modes, edge)
    if status == "open":
        toks &= open_cards()
    elif status == "drop_victims":
        toks -= set(vic)
    return len(toks), toks


def terminal_facts(tid, vic):
    a = auth()
    mid = a.merchant_id[a.terminal_id == tid].iloc[0]
    m = merchants().set_index("merchant_id").loc[mid]
    t0, t1 = window(tid, vic)
    return {"terminal_id": tid, "merchant_id": mid, "merchant": m["name"], "town": m["town"],
            "address": m["address"], "first_read": t0.tz_convert(TZ).date(), "last_read": t1.tz_convert(TZ).date(),
            "first_read_ts": t0, "last_read_ts": t1}


# ask A: what the wave has cost ------------------------------------------------------------------------
def card_type_of():
    c, _, _ = cards()
    return dict(zip(c.card_token, c.card_type))


def posted_cad(rrns):
    a = auth()
    r = a[a.retrieval_ref.isin(list(rrns))]
    out = {}
    for rrn, g in r.groupby("retrieval_ref"):
        comp = g[g.message_type == "0220"]
        base = g[g.message_type.isin(["0100", "0200"]) & (g.response_code == "00")]
        amt = comp.amount_billing_cad.sum() if len(comp) else base.amount_billing_cad.sum()
        amt -= g[g.message_type == "0420"].amount_billing_cad.sum()
        out[rrn] = round(float(amt), 2)
    return out


def ask_a(dedup="rrn", currency="posted", recover="net", scope="counterfeit"):
    w = cases()
    cf = w[w.fraud_type == "Counterfeit"] if scope == "counterfeit" else w
    ct = card_type_of()
    if dedup == "rrn":
        rows = cf.drop_duplicates("retrieval_ref")
    elif dedup == "none":
        rows = cf
    elif dedup == "card_merchant_amount_date":
        rows = cf.drop_duplicates(["card_token", "merchant_as_on_statement", "amount", "txn_date"])
    if currency == "posted":
        post = posted_cad(set(rows.retrieval_ref))
        amt = rows.retrieval_ref.map(post)
    else:
        amt = rows.amount
    g = {"Debit": 0.0, "Credit": 0.0}
    for tok, x in zip(rows.card_token, amt):
        g[ct[tok]] += float(x)
    cb = chargebacks()
    cbr = cb[cb.retrieval_ref.isin(set(cf.retrieval_ref))] if scope != "all_chargebacks" else cb
    if recover == "net":
        cbr = cbr[cbr.amount_cad.notna()]
    elif recover == "credits_only":
        cbr = cbr[cbr.amount_cad > 0]
    rec = {"Debit": 0.0, "Credit": 0.0}
    for tok, x in zip(cbr.card_token, cbr.amount_cad):
        rec[ct[tok]] += float(x)
    out = {}
    for k in ("Debit", "Credit"):
        out[k] = {"gross": round(g[k], 2), "recovered": round(rec[k], 2), "net": round(g[k] - rec[k], 2)}
    return out


# ask B: refunds against MS-3 ---------------------------------------------------------------------------
def is_bd(d, hol):
    return d.weekday() < 5 and d not in hol


def bd_wait(day0, refund, hol, calendar=False):
    if calendar:
        return (refund - day0).days
    n, x = 0, day0
    while x < refund:
        x += dt.timedelta(1)
        if is_bd(x, hol):
            n += 1
    return n


def claims(reopen="same_claim"):
    w = cases()
    cf = w[w.fraud_type == "Counterfeit"]
    parent = {c: c for c in cf.case_number.unique()}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    if reopen == "same_claim":
        for _, g in cf.groupby("retrieval_ref"):
            cs = sorted(g.case_number.unique())
            for c in cs[1:]:
                parent[find(c)] = find(cs[0])
    cf = cf.assign(claim=[find(c) for c in cf.case_number])
    out = []
    for cl, g in cf.groupby("claim"):
        opened = pd.to_datetime(g.case_opened, utc=True)
        out.append({"claim": cl, "card_token": g.card_token.iat[0], "first_report_utc": opened.min(),
                    "refunded_on": g.refunded_on.dropna().max() if g.refunded_on.notna().any() else None})
    return out


def ask_b(clock="local", calendar=False, holidays_rule="ms3", reopen="same_claim"):
    hol = set(holidays()) if holidays_rule == "ms3" else set()
    ct = card_type_of()
    res = {"Debit": {"within": 0, "longest": 0, "refunded": 0}, "Credit": {"within": 0, "longest": 0, "refunded": 0}}
    for c in claims(reopen):
        if c["refunded_on"] is None:
            continue
        t = c["first_report_utc"]
        rd = t.tz_convert(TZ).date() if clock == "local" else t.date()
        day0 = rd
        while not is_bd(day0, hol):
            day0 += dt.timedelta(1)
        wait = bd_wait(day0, c["refunded_on"], hol, calendar)
        k = ct[c["card_token"]]
        res[k]["refunded"] += 1
        res[k]["within"] += int(wait <= 10)
        res[k]["longest"] = max(res[k]["longest"], wait)
    return res


# the call ----------------------------------------------------------------------------------------------
def solve():
    vic = victims()
    chosen, rem = sequential(vic)
    n, toks = reissue(chosen, vic)
    facts = [terminal_facts(t, vic) for t in chosen]
    for f in facts:
        f["cards_read_open"] = len(exposed(f["terminal_id"], vic) & open_cards())
    pooled = screen(vic)
    return {"victims": len(vic), "terminals": chosen, "facts": facts, "reissue": n, "reissue_tokens": sorted(toks),
            "unexplained": len(rem), "pooled": pooled, "ask_a": ask_a(), "ask_b": ask_b()}


def printable(s):
    out = {k: v for k, v in s.items() if k not in ("pooled", "reissue_tokens")}
    return json.dumps(out, indent=1, default=str)


if __name__ == "__main__":
    s = solve()
    print(printable(s))
    if "--write" in sys.argv:
        import deliver
        deliver.write(s, GOLDEN)
