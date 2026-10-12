"""The three asks from the shipped files, with the cracker's stops: second-pass hours (A), credit at stake (B)
and the third-quarter residual as each client's own audit counted it (C)."""
import datetime as dt
import json
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import analysis as AN
import nov
import world as W

SID2 = AN.SID2
Q3A, Q3B = W.Q3


# ----------------------------------------------------------------------------------------------- A, second-pass hours
def family_rates(target, mode="golden"):
    L = pd.read_csv(os.path.join(target, "second_pass_sessions_2026_09.csv"))
    sr = pd.read_csv(os.path.join(target, "stream_register.csv")).drop_duplicates("stream_code")
    fam = dict(zip(sr.stream_code, sr.form_family))
    L["fam"] = L.stream.map(fam)
    docs = L.groupby("fam").size()
    if mode == "golden":
        mins = L.drop_duplicates(["session_ref", "half_shift"]).groupby("fam").productive_min.sum()
    elif mode == "dedupe":
        mins = L.drop_duplicates(["session_ref"]).groupby("fam").productive_min.sum()
    elif mode == "sum":
        mins = L.groupby("fam").productive_min.sum()
    else:
        raise ValueError(mode)
    return (mins / docs).to_dict()


def nov_docs(sc, one_version=False):
    pl = sc.plan.copy()
    if one_version:
        first = pl.sort_values("day").groupby("code").kfpd.first()
        pl["kfpd"] = pl.code.map(first)
        pl["docs"] = pl.kf / pl.kfpd
    return pl


def hours(target, sc, mode="golden", one_version=False, unrounded=False):
    rate = family_rates(target, mode)
    pl = nov_docs(sc, one_version)
    out = {}
    for c in W.ORDER:
        g = pl[pl.code == c]
        h = g.docs.sum() * rate[W.STREAMS[c]["family"]] / 60
        out[c] = h if unrounded else int(round(h))
    return out


# ----------------------------------------------------------------------------------------------- B, credit at stake
def band_index(client, docs):
    f = W.BANDS[client]["floors"]
    return max(i for i, x in enumerate(f) if docs >= x)


def register_bands(target):
    br = AN._xl(os.path.join(target, "billing_register_oct26.xlsx"), "Accounts")
    out = {}
    for r in br.itertuples(index=False):
        c = SID2[r[2]]
        out[W.STREAMS[c]["client"]] = W.BANDS[W.STREAMS[c]["client"]]["names"].index(r[5])
    return out


def latest_revision_docs(target):
    """the cracker's November documents: each client's latest delivered revision, spread the plan's way"""
    fc = nov.weekly_forecasts()
    rows = []
    for c, g in fc.groupby("client"):
        last = g.sent.max()
        gg = g[g.sent == last]
        for r in gg.itertuples():
            wdays = [r.week_start + dt.timedelta(days=i) for i in range(7)]
            wdays = [d for d in wdays if nov.working(c, d)]
            tot = r.units * (W.HP_BUNDLE if r.code == "D6" else 1)
            for d, n in nov.spread(tot, wdays).items():
                if W.NOV[0] <= d <= W.NOV[1]:
                    rows.append((r.code, d, n))
    return pd.DataFrame(rows, columns=["code", "day", "docs"])


def credit(target, sc, credit_pct, docs=None, bands="november", indexation=True, unrounded=False):
    pl = sc.plan[["code", "day", "docs"]] if docs is None else docs
    pl = pl.assign(client=pl.code.map(lambda c: W.STREAMS[c]["client"]))
    acct = pl.groupby("client").docs.sum()
    stored = register_bands(target) if bands == "register" else None
    out = {}
    for c in W.ORDER:
        cl = W.STREAMS[c]["client"]
        b = W.BANDS[cl]
        bi = band_index(cl, acct[cl]) if bands == "november" else stored[cl]
        base = b["price"][c][bi]
        g = pl[pl.code == c]
        amt = 0.0
        for r in g.itertuples():
            p = base
            if indexation and "index" in b and r.day >= b["index"][0]:
                p = round(base * (1 + b["index"][1] / 100.0), 4)
            amt += r.docs * p
        v = credit_pct[c] / 100.0 * amt
        out[c] = v if unrounded else int(round(v))
    return out


def inr(target_budget, B):
    return {c: B[c] * target_budget[W.CLIENTS[W.STREAMS[c]["client"]]["ccy"]] for c in W.ORDER}


# ----------------------------------------------------------------------------------------------- C, client audits
CAPTURE = {"KBA": {"D01", "D02", "D04"}, "NDS": {"KE", "KT"}, "BMC": {"DE-1", "DE-2"}, "HPB": {"E10", "E11"},
           "WBH": {"CAPT", "KEY"}, "CIP": {"C1"}, "WPC": {"DATA", "TRANS"}, "TCM": {"01", "02"}}


def _i(x, d=0):
    if x is None or x == "" or (isinstance(x, float) and np.isnan(x)):
        return d
    return int(x)


def _s(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return str(x)


def normalized_client_audits(target):
    """one row per finding round (or one row for a clean claim): code, claim, file, delivered (UTC as stamped),
    form version where the client gives it, finding sequence, reason, round, active"""
    f = lambda n: os.path.join(target, n)
    rows = []
    k = pd.read_csv(f("kessington_audit_findings_q3.csv"), dtype=str, keep_default_na=False)
    for r in k.itertuples(index=False):
        rows.append(dict(client="KBA", claim=r[0], file=r[1], delivered=pd.Timestamp(r[2]), seq=_i(r[4], 0),
                         reason=r[5], rnd=_i(r[6], 1)))
    for sheet, c in (("Northgate", "NDS"), ("Brightmoor", "BMC"), ("Harbison", "HPB")):
        d = AN._xl(f("client_audits_us_q3.xlsx"), sheet)
        for r in d.itertuples(index=False):
            if c == "NDS":
                rows.append(dict(client=c, claim=r[0], file=r[1], delivered=pd.Timestamp(r[2]), seq=_i(r[3], 0),
                                 reason=_s(r[4]), rnd=2 if r[5] == "RE-REVIEWED" else 1, status=r[5]))
            elif c == "BMC":
                rows.append(dict(client=c, claim=r[0], file=r[1], delivered=pd.Timestamp(r[2]), seq=_i(r[3], 0),
                                 reason="" if r[4] == "CLEAN" else r[4], rnd=_i(r[5], 1)))
            else:
                rows.append(dict(client=c, claim=r[0], file=r[1], delivered=pd.Timestamp(r[2]), seq=_i(r[3], 0),
                                 reason=_s(r[4]), rnd=_i(r[5], 1)))
    for sheet, c in (("Wattlebird QA", "WBH"), ("Coolabah QA", "CIP")):
        d = AN._xl(f("client_audits_au_q3.xlsx"), sheet)
        for r in d.itertuples(index=False):
            rows.append(dict(client=c, claim=r[0], file=r[2], delivered=pd.Timestamp(r[3]), seq=_i(r[4], 0),
                             reason="" if r[5] == "NIL" else r[5], rnd=2 if r[6] == "Second review" else 1))
    js = json.load(open(f("client_portal_audits_uk_q3.json")))
    for rec in js["records"]:
        c = "WPC" if rec["insurer"].startswith("Whinfell") else "TCM"
        if not rec["findings"]:
            rows.append(dict(client=c, claim=rec["claim_ref"], file=rec["batch"], delivered=pd.Timestamp(rec["delivered_ts"]),
                             seq=0, reason="", rnd=1))
        for fnd in rec["findings"]:
            rows.append(dict(client=c, claim=rec["claim_ref"], file=rec["batch"], delivered=pd.Timestamp(rec["delivered_ts"]),
                             seq=fnd["n"], reason=fnd["code"], rnd=fnd["review"]))
    df = pd.DataFrame(rows)
    df["code"] = df.file.str.split("_").str[1].map(SID2)
    df["shift_day"] = pd.to_datetime(df.file.str.split("_").str[2], format="%Y%m%d").dt.date
    return df


def _final(df):
    """a re-reviewed finding is replaced by its re-review"""
    f = df[df.seq > 0]
    last = f.groupby(["claim", "seq"]).rnd.transform("max")
    return f[f.rnd == last]


def client_audit_rates(df, D=None, clock="local", rereview=True, capture_only=True, vt=None, unrounded=True):
    """per stream: capture findings per 1,000 key fields on sampled claims delivered in Q3 (client's local date)"""
    if "delivered" not in df:
        df = from_sim(df, D)
    df = df.copy()
    tz = {c: ZoneInfo(W.CLIENTS[c]["tz"]) for c in W.CLIENTS}
    if clock == "local":
        loc = [pd.Timestamp(t).tz_localize("UTC").tz_convert(tz[c]).date() for t, c in zip(df.delivered, df.client)]
    elif clock == "utc_as_local":
        loc = [pd.Timestamp(t).date() for t in df.delivered]
    elif clock == "ist":
        loc = [(pd.Timestamp(t) + pd.Timedelta(hours=5, minutes=30)).date() for t in df.delivered]
    elif clock == "shift_day":
        loc = list(df.shift_day)
    df["ldate"] = loc
    df = df[(df.ldate >= Q3A) & (df.ldate <= Q3B)]
    if "kf" not in df or df.kf.isna().any():
        df["kf"] = [W.kfpd(c, d) for c, d in zip(df.code, df.shift_day)]
    claims = df.drop_duplicates("claim")
    den = claims.groupby("code").kf.sum()
    fin = _final(df) if rereview else df[df.seq > 0]
    if capture_only:
        fin = fin[[r in CAPTURE[c] for r, c in zip(fin.reason, fin.client)]]
    else:
        fin = fin[fin.reason != "WD"]
    num = fin.groupby("code").size().reindex(den.index, fill_value=0)
    out = (num / den * 1000).to_dict()
    return out if unrounded else {k: round(v, 1) for k, v in out.items()}


def from_sim(Fd, D):
    import asks_sim as AS
    utc = D.set_index("file").sent_utc
    df = Fd.copy()
    df["delivered"] = [AS.delivered_stamp(utc[f], cl) for f, cl in zip(df.file, df.claim)]
    df["shift_day"] = df.day
    df["claim"] = df.client + df.claim.astype(str)
    return df


def boundary_batches(Fd, D, code):
    """files a stream's cracker counts in the quarter and the golden does not, and the reverse"""
    import asks_sim as AS
    g = D[D.code == code]
    tz = ZoneInfo(W.CLIENTS[W.STREAMS[code]["client"]]["tz"])
    inc_c, inc_g = [], []
    for r in g.itertuples():
        u = pd.Timestamp(AS.delivered_stamp(r.sent_utc, 0))
        a = Q3A <= u.date() <= Q3B
        b = Q3A <= u.tz_localize("UTC").tz_convert(tz).date() <= Q3B
        if a and not b:
            inc_c.append(r.file)
        if b and not a:
            inc_g.append(r.file)
    return inc_c, inc_g


def ten_streams():
    return [c for c in W.ORDER if c != "D6"]


# ----------------------------------------------------------------------------------------------- all asks, stops, pair
def chart_order(B, budget):
    v = inr(budget, B)
    return sorted(W.ORDER, key=lambda c: (-v[c], W.ORDER.index(c)))


def run(target, pk, sc):
    out = {}
    out["A"] = {"golden": hours(target, sc), "dedupe": hours(target, sc, "dedupe"), "sum": hours(target, sc, "sum"),
                "one_version": hours(target, sc, one_version=True)}
    out["A_unrounded"] = hours(target, sc, unrounded=True)
    out["rates"] = {m: family_rates(target, m) for m in ("golden", "dedupe", "sum")}
    cp = pk.credit
    latest = latest_revision_docs(target)
    out["B"] = {"golden": credit(target, sc, cp), "latest_revision": credit(target, sc, cp, docs=latest),
                "register_band": credit(target, sc, cp, bands="register"),
                "cracker": credit(target, sc, cp, docs=latest, bands="register"),
                "no_indexation": credit(target, sc, cp, indexation=False)}
    out["B_unrounded"] = credit(target, sc, cp, unrounded=True)
    df = normalized_client_audits(target)
    out["C_unrounded"] = client_audit_rates(df)
    out["C"] = {"golden": client_audit_rates(df, unrounded=False), "utc_as_local": client_audit_rates(df, clock="utc_as_local", unrounded=False),
                "no_rereview": client_audit_rates(df, rereview=False, unrounded=False),
                "all_codes": client_audit_rates(df, capture_only=False, unrounded=False),
                "ist": client_audit_rates(df, clock="ist", unrounded=False),
                "shift_day": client_audit_rates(df, clock="shift_day", unrounded=False)}
    out["C_cracker_unrounded"] = client_audit_rates(df, clock="utc_as_local")
    out["inr"] = inr(pk.budget, out["B"]["golden"])
    out["order"] = chart_order(out["B"]["golden"], pk.budget)
    out["order_nominal"] = sorted(W.ORDER, key=lambda c: -out["B"]["golden"][c])
    out["cracker_order"] = chart_order(out["B"]["cracker"], pk.budget)
    # the pair simulation: the cracker landed the call, ran the battery and executed every filed rule
    rows = []
    for c in W.ORDER:
        rows.append(("A", c, out["A"]["dedupe"][c] != out["A"]["golden"][c]))
        rows.append(("B", c, abs(out["B"]["cracker"][c] - out["B"]["golden"][c]) >= 1))
    for c in ten_streams():
        rows.append(("C", c, out["C"]["utc_as_local"][c] != out["C"]["golden"][c]))
    rows.append(("chart", "series", all(out["A"]["dedupe"][c] != out["A"]["golden"][c] for c in W.ORDER)))
    rows.append(("chart", "order", out["cracker_order"] != out["order"]))
    rows.append(("chart", "title", out["cracker_order"][0] != out["order"][0]))
    out["cracker_rows"] = rows
    n = len(rows)
    hits = sum(1 for r in rows if not r[2])
    L = hits / n
    r = 6.0
    out["pair_ceiling_measured"] = ((38 + 7 + 55 * L) + (r + 7 + 55 * L)) / 2
    out["pair_ceiling_allowance"] = ((38 + 7 + 55 * max(L, 0.10)) + (r + 7 + 55 * max(L, 0.10))) / 2
    return out
