"""Every figure owed, computed from the cut pack alone (target/): the call and its routes, the standing family, and the
recurring revenue bridge with the handlings a response might take. Nothing here reads the world."""
import csv
import functools
import os

import numpy as np
import pandas as pd

APPS = ["Tracewood", "Taskfold", "Ledgerline", "Formbox", "Notewell"]
RENAMED = {"Leafnote": "Notewell"}
CAP = 2048.0
AT_CAP = 0.99 * CAP                     # an account within one per cent of the allowance has no room for the next file


def _mi(ym):
    y, m = ym.split("-")
    return (int(y) - 2000) * 12 + int(m) - 1


# --- the paper's table -------------------------------------------------------------------------------------------

def paper_table(target):
    """the Plus price and the free-plan revenue per active free account, a month, as section 4 states them"""
    import subprocess
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, "free_plan_limit_paper_2027.pdf"), "-"],
                         capture_output=True, text=True).stdout
    price, free = np.zeros(5), np.zeros(5)
    for i, a in enumerate(APPS):
        for line in txt.splitlines():
            parts = line.split()
            if parts and parts[0] == a and len(parts) >= 3:
                try:
                    price[i], free[i] = float(parts[1]), float(parts[2])
                    break
                except ValueError:
                    continue
    assert price.all(), "paper table not read"
    return price, free


# --- the research panel and the monthly count -------------------------------------------------------------------

MODE = {"rename": True, "drop_merged": False}       # Layer 1 handlings the checks flip one at a time


def panel(target):
    return _panel(target, MODE["rename"], MODE["drop_merged"])


@functools.lru_cache(maxsize=8)
def _panel(target, rename, drop_merged):
    df = pd.read_csv(os.path.join(target, "research_panel_account_months_2023_2026.csv"),
                     dtype={"account_id": str, "app": str, "plan": str})
    if rename:
        df["app"] = df["app"].replace(RENAMED)
    else:
        df = df[df["app"].isin(APPS)]
    if drop_merged:
        reg = pd.read_csv(os.path.join(target, "research_panel_accounts.csv"), dtype=str, keep_default_na=False)
        df = df[~df["account_id"].isin(set(reg.loc[reg["merged_into"] != "", "account_id"]))]
    df["m"] = df["month"].map(_mi)
    acc, ai = np.unique(df["account_id"].values, return_inverse=True)
    m0 = int(df["m"].min())
    M = int(df["m"].max()) - m0 + 1
    A = len(acc)
    ST = np.full((A, M), -1, np.int8)
    K = np.zeros((A, M), np.int16)
    S = np.zeros((A, M))
    j = df["m"].values - m0
    ST[ai, j] = np.where(df["plan"].values == "plus", 1, 0)
    K[ai, j] = df["active_projects"].values
    S[ai, j] = df["storage_mib"].values
    app = np.zeros(A, np.int8)
    app[ai] = [APPS.index(a) for a in df["app"].values]
    return dict(ST=ST, K=K, S=S, app=app, m0=m0, M=M, acc=acc)


@functools.lru_cache(maxsize=4)
def kpi(target):
    """free accounts used in the month, by app and active projects, for the latest month"""
    xl = pd.ExcelFile(os.path.join(target, "free_accounts_by_active_projects_2023_2026.xlsx"))
    last = sorted(xl.sheet_names)[-1]
    d = xl.parse(last)
    d["app"] = d["app"].replace(RENAMED)
    latest = d["month"].max()
    d = d[d["month"] == latest]
    heavy, light = np.zeros(5), np.zeros(5)
    for _, r in d.iterrows():
        i = APPS.index(r["app"])
        if str(r["active_projects"]) in ("1", "2", "3"):
            light[i] += r["free_accounts_active"]
        else:
            heavy[i] += r["free_accounts_active"]
    return heavy, light, latest


def _curves(D, rows, H=12):
    ST = D["ST"]
    a = np.array([r[0] for r in rows if r[1] + H < D["M"]], dtype=int)
    j = np.array([r[1] for r in rows if r[1] + H < D["M"]], dtype=int)
    Pm = np.array([(ST[a, j + h] == 1).mean() for h in range(1, H + 1)])
    Fm = np.array([(ST[a, j + h] == 0).mean() for h in range(1, H + 1)])
    return Pm, Fm, len(a)


def stops(D, thr=AT_CAP, first=True, j_from=0, j_to=None):
    """the account-months at the storage allowance (the first in the panel for each account, by default)"""
    free = D["ST"] == 0
    at = free & (D["S"] >= thr)
    j_to = D["M"] - 13 if j_to is None else j_to
    rows = []
    if first:
        has = at.any(1)
        firstj = np.argmax(at, axis=1)
        for a_ in np.nonzero(has)[0]:
            if j_from <= firstj[a_] <= j_to:
                rows.append((a_, int(firstj[a_])))
    else:
        for a_, j in zip(*np.nonzero(at)):
            if j_from <= j <= j_to:
                rows.append((int(a_), int(j)))
    return rows


def unstopped(D, thr=AT_CAP, heavy=True, j_from=0, j_to=None):
    free = D["ST"] == 0
    c = free & (D["S"] < thr)
    if heavy:
        c &= D["K"] >= 4
    j_to = D["M"] - 13 if j_to is None else j_to
    a_, j = np.nonzero(c)
    keep = (j >= j_from) & (j <= j_to)
    return list(zip(a_[keep].tolist(), j[keep].tolist()))


def crossing(D, j0=None):
    """for free accounts below four active projects at a month, the share first reaching four in each later month"""
    ST, K = D["ST"], D["K"]
    j0 = D["M"] - 13 if j0 is None else j0
    base = np.nonzero((ST[:, j0] == 0) & (K[:, j0] <= 3))[0]
    first = np.full(len(base), -1)
    for h in range(1, 13):
        hit = (ST[base, j0 + h] == 0) & (K[base, j0 + h] >= 4) & (first < 0)
        first[hit] = h
    return np.array([(first == h).sum() for h in range(1, 13)]) / len(base)


def addition(target, dP, dF, fr, heavy=None, light=None):
    """the 2027 revenue the limit adds, by app: the accounts over the limit on 1 January, then the accounts reaching a
    fourth project in each month of the year"""
    price, free = paper_table(target)
    h_, l_, _ = kpi(target)
    heavy = h_ if heavy is None else heavy
    light = l_ if light is None else light
    out = heavy * (dP[:12].sum() * price - dF[:12].sum() * free)
    for h in range(1, 12):
        rem = 12 - h
        out = out + light * fr[h - 1] * (dP[:rem].sum() * price - dF[:rem].sum() * free)
    return out


def golden_call(target, thr=AT_CAP, first=True, ctrl_heavy=True, j_from=0, j_to=None, j_flow=None, keep=None):
    D = panel(target)
    st, un = stops(D, thr, first, j_from, j_to), unstopped(D, thr, ctrl_heavy, j_from, j_to)
    if keep is not None:
        st, un = [r for r in st if keep(D, r)], [r for r in un if keep(D, r)]
    P1, F1, n1 = _curves(D, st)
    P0, F0, n0 = _curves(D, un)
    fr = crossing(D, j_flow)
    return addition(target, P1 - P0, F0 - F1, fr), dict(P1=P1, F1=F1, P0=P0, F0=F0, n1=n1, n0=n0, fr=fr)


def adjusted(target):
    """the constructions the data supports adjusting by: each app read from its own stopped accounts, and only the
    stopped accounts that had four or more active projects at the stop"""
    own = np.zeros(5)
    for i in range(5):
        own[i] = golden_call(target, keep=lambda D, r, i=i: D["app"][r[0]] == i)[0][i]
    four = golden_call(target, keep=lambda D, r: D["K"][r[0], r[1]] >= 4)[0]
    return {"each app read from its own stopped accounts": own,
            "only accounts with four or more active projects": four}


def response(target):
    """the stopped accounts' state the month after the stop: on Plus, still free, gone"""
    D = panel(target)
    rows = [r for r in stops(D) if r[1] + 1 < D["M"]]
    s1 = np.array([D["ST"][a, j + 1] for a, j in rows])
    return (s1 == 1).mean(), (s1 == 0).mean(), (s1 == -1).mean()


def routes(target):
    """the routes a response takes to the call, each app's 2027 addition under it"""
    price, free = paper_table(target)
    heavy, light, _ = kpi(target)
    g, c = golden_call(target)
    up1, fr1, gone1 = response(target)
    U = c["P0"][-1]
    L = 1.0 - c["P0"][-1] - c["F0"][-1]
    surv = c["P1"] / max(c["P1"][0], 1e-9)
    out = {
        "L0 the heavy accounts' own upgrades, nobody leaving": heavy * 12 * U * price,
        "L1 the heavy accounts' own upgrades and own losses": heavy * 12 * (U * price - L * free),
        "L2 the stopped accounts' upgrade share, nobody leaving": heavy * 12 * up1 * price,
        "L3 every account that does not upgrade leaves": heavy * 12 * (up1 * price - (1 - up1) * free),
        "S1 the stopped accounts' response shares for a year": heavy * 12 * (up1 * price - gone1 * free),
        "S2 the stopped accounts' year with nothing set against it": heavy * (c["P1"].sum() * price -
                                                                          (12 - c["F1"].sum() - c["P1"].sum()) * free),
        "G stopped against unstopped": g,
    }
    pd_ = 0.0
    dPb = up1 * (1 - 0.018) ** np.arange(12) + (1 - up1 - gone1) * c["P0"] - c["P0"]
    dFb = c["F0"] - (1 - up1 - gone1) * c["F0"]
    out["S3 the response, then carried as unstopped"] = addition(target, dPb, dFb, c["fr"])
    return out, dict(U=U, L=L, up1=up1, free1=fr1, gone1=gone1, curves=c, pd=pd_)


def standing(target):
    D = panel(target)
    M = D["M"]
    v = {
        "every stop, not the first": golden_call(target, first=False)[0],
        "the allowance read at 2,000 MiB": golden_call(target, thr=2000.0)[0],
        "the allowance read at 1,950 MiB": golden_call(target, thr=1950.0)[0],
        "the allowance read at 2,047 MiB": golden_call(target, thr=2047.0)[0],
        "every unstopped free account as the comparison": golden_call(target, ctrl_heavy=False)[0],
        "stops in 2023 only": golden_call(target, j_to=11)[0],
        "stops in 2024 only": golden_call(target, j_from=12, j_to=23)[0],
        "stops in 2025 only": golden_call(target, j_from=24)[0],
        "crossings over the year to September 2024": golden_call(target, j_flow=M - 25)[0],
    }
    return v


# --- the recurring revenue bridge -----------------------------------------------------------------------------

def _rates(target, year="2026/27"):
    r = {"GBP": 1.0}
    with open(os.path.join(target, "fx_plan_rates.csv")) as fh:
        for row in csv.DictReader(fh):
            if row["plan_year"] == year:
                r[row["currency"]] = float(row["units_per_gbp"])
    return r


def _months(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month) + (b.day - a.day) / 31.0


@functools.lru_cache(maxsize=4)
def _billing(target):
    op = pd.read_csv(os.path.join(target, "billing_subscriptions_20250930.csv"), dtype=str, keep_default_na=False)
    ev = pd.read_csv(os.path.join(target, "billing_subscription_events_20251001_20260930.csv"), dtype=str,
                     keep_default_na=False)
    return op, ev


def bridge(target, key="person", cancel="ended", past_due=True, fx_open="2026/27"):
    """each app's new, expansion, contraction and churned recurring revenue, 30 September 2025 to 30 September 2026,
    pounds a month. key: person (customer records and accounts joined), customer, account, subscription."""
    import datetime as dt
    op, ev = _billing(target)
    r_close = _rates(target, "2026/27")
    r_open = _rates(target, fx_open)

    def value(row, rates, started):
        unit = float(row["unit_amount"]) * int(row["quantity"])
        if row["billing_interval"] == "year":
            unit /= 12.0
        d = row["discount_percent"]
        if d:
            ends = dt.datetime.strptime(row["discount_ends"], "%Y-%m-%d")
            if _months(started, ends) >= 11.99:
                unit *= 1 - float(d) / 100.0
        return unit / rates[row["currency"]]

    def live_ok(status):
        return past_due or status != "past_due"
    started = {}
    open_val = {}
    meta = {}
    for _, r in op.iterrows():
        st = dt.datetime.strptime(r["started_at"], "%Y-%m-%dT%H:%M:%SZ")
        started[r["subscription_id"]] = st
        meta[r["subscription_id"]] = (r["customer_id"], r["account_id"], r["app"])
        if r["status"] in ("active", "past_due") and live_ok(r["status"]):
            open_val[r["subscription_id"]] = value(r, r_open, st)
    state = {sid: r for sid, r in ((r["subscription_id"], r) for _, r in op.iterrows())}
    alive = {sid for sid in state if state[sid]["status"] in ("active", "past_due")}
    for _, e in ev.iterrows():
        sid, kind = e["subscription_id"], e["event_type"].split(".")[1]
        if kind == "created":
            started[sid] = dt.datetime.strptime(e["occurred_at"], "%Y-%m-%dT%H:%M:%SZ")
            alive.add(sid)
        meta.setdefault(sid, (e["customer_id"], e["account_id"], e["app"]))
        if kind in ("created", "updated", "renewed"):
            state[sid] = e
        elif kind == "cancelled" and cancel == "request":
            alive.discard(sid)
        elif kind == "ended":
            alive.discard(sid)
    close_val = {sid: value(state[sid], r_close, started[sid]) for sid in alive if live_ok(state[sid]["status"])}
    # who the customer is
    if key == "person":
        parent = {}

        def find(x):
            while parent.get(x, x) != x:
                parent[x] = parent.get(parent[x], parent[x])
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
        for sid, (c, a, app) in meta.items():
            union(("c", app, c), ("a", app, a))
        who = {sid: find(("c", app, c)) for sid, (c, a, app) in meta.items()}
    elif key == "customer":
        who = {sid: (app, c) for sid, (c, a, app) in meta.items()}
    elif key == "account":
        who = {sid: (app, a) for sid, (c, a, app) in meta.items()}
    else:
        who = {sid: (meta[sid][2], sid) for sid in meta}
    tot = {}
    for sid, v in open_val.items():
        tot.setdefault((meta[sid][2], who[sid]), [0.0, 0.0])[0] += v
    for sid, v in close_val.items():
        tot.setdefault((meta[sid][2], who[sid]), [0.0, 0.0])[1] += v
    out = {}
    for a in APPS:
        n = e_ = c_ = ch = 0.0
        o_sum = cl_sum = 0.0
        for (app, w), (o, cl) in tot.items():
            if app != a:
                continue
            o_sum += o
            cl_sum += cl
            if o <= 1e-9 and cl > 1e-9:
                n += cl
            elif o > 1e-9 and cl <= 1e-9:
                ch += o
            elif cl > o:
                e_ += cl - o
            else:
                c_ += o - cl
        out["%s new" % a] = round(n)
        out["%s expansion" % a] = round(e_)
        out["%s contraction" % a] = round(c_)
        out["%s churned" % a] = round(ch)
        out["%s opening" % a] = round(o_sum)
        out["%s closing" % a] = round(cl_sum)
    return out


ASK_KEYS = ["%s %s" % (a, k) for a in APPS for k in ("new", "expansion", "contraction", "churned")]


def response_by(target):
    """the stopped accounts' next-month shares (on Plus, gone) by app, by active projects at the stop and by years since
    sign-up at the stop"""
    import datetime as dt
    D = panel(target)
    reg = pd.read_csv(os.path.join(target, "research_panel_accounts.csv"), dtype=str, keep_default_na=False)
    born = dict(zip(reg["account_id"], reg["created_utc"]))
    rows = [r for r in stops(D) if r[1] + 1 < D["M"]]
    cut = {"app": {}, "projects": {}, "tenure": {}}
    for a, j in rows:
        s1 = D["ST"][a, j + 1]
        m = D["m0"] + j
        y = (2000 + m // 12) + (m % 12) / 12.0
        c = dt.datetime.strptime(born[D["acc"][a]], "%Y-%m-%dT%H:%M:%SZ")
        age = y - (c.year + (c.month - 1) / 12.0)
        keys = {"app": APPS[D["app"][a]], "projects": "four or more" if D["K"][a, j] >= 4 else "three or fewer",
                "tenure": "under three years" if age < 3 else ("three to six years" if age < 6 else "six years or more")}
        for k, v in keys.items():
            t = cut[k].setdefault(v, [0, 0, 0])
            t[0] += 1
            t[1] += s1 == 1
            t[2] += s1 == -1
    return {k: {v: (n, p / n, g / n) for v, (n, p, g) in d.items()} for k, d in cut.items()}
