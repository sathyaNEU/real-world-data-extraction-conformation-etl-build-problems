"""Independent recomputation of every graded figure from target.zip (or a target folder), by code that shares nothing
with solve.py, against figures.json and submission.md.   python3 verify.py [target.zip|target]"""
import io
import json
import os
import re
import sys
import zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FAILS = []


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def unpack(src):
    if os.path.isdir(src):
        return {f: open(os.path.join(src, f), "rb").read() for f in os.listdir(src)}
    with zipfile.ZipFile(src) as z:
        return {n.split("/", 1)[1]: z.read(n) for n in z.namelist() if not n.endswith("/")}


def the_call(F):
    X = pd.read_parquet(io.BytesIO(F["web_sessions_2028q4.parquet"]))
    X = X[(~X["is_bot"]) & (X["ip_prefix"] != "85.214.110.0")].drop_duplicates()
    X["edition"] = X["content_group"].where(X["content_group"] != "HKR", "HOL")
    berlin = X["session_start"].dt.tz_convert("Europe/Berlin")
    X["month"] = berlin.dt.month
    X = X[X["month"] >= 10]
    X["webkit"] = X["os"].eq("iOS") | (X["os"].eq("Macintosh") & X["browser"].eq("Safari"))
    reg = pd.read_csv(io.BytesIO(F["signin_device_register_2028q4.csv"]), dtype=str)
    acc = pd.read_csv(io.BytesIO(F["reader_accounts.csv"]), dtype=str)
    printed_accounts = set(acc.loc[acc["origin"] == "print subscription", "account_no"])
    reg["print"] = reg["account_no"].isin(printed_accounts)
    device = dict(zip(reg["client_id"], reg["device_id"]))
    prn = set(reg.loc[reg["print"], "client_id"])
    # replayed identifiers: per client, sessions in time order, a new one after a gap of more than seven days
    X = X.sort_values(["client_id", "session_start"])
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    t0 = (X["session_start"] - epoch).dt.total_seconds()
    t1 = (X["session_end"] - epoch).dt.total_seconds()
    newc = X["client_id"].ne(X["client_id"].shift())
    gap = t0 - t1.shift()
    X["ident"] = (newc | (gap > 7 * 24 * 3600)).cumsum()
    est = {}
    for (e, m), g in X.groupby(["edition", "month"]):
        total = 0.0
        for d, gd in g.groupby("device_category"):
            other = gd[~gd["webkit"]]
            wk = gd[gd["webkit"]]
            comp = other[~other["client_id"].isin(prn)]
            per = comp.groupby("client_id")["ident"].nunique().mean()
            total += other["client_id"].nunique()
            total += wk.loc[wk["client_id"].isin(prn), "client_id"].map(device).nunique()
            total += wk.loc[~wk["client_id"].isin(prn), "client_id"].nunique() / per
        est[(e, m)] = (g["client_id"].nunique(), total)
    over = {}
    for e in sorted({k[0] for k in est}):
        rep = np.mean([est[(e, m)][0] for m in (10, 11, 12)])
        br = np.mean([est[(e, m)][1] for m in (10, 11, 12)])
        over[e] = 100 * (rep / br - 1)
    return over


def newsletter(F):
    C = pd.read_csv(io.BytesIO(F["newsletter_contacts_2029-01-15.csv"]))
    E = pd.read_csv(io.BytesIO(F["newsletter_activity_log.csv"]), keep_default_na=False)
    Gc = pd.read_csv(io.BytesIO(F["newsletter_group_changes.csv"]))
    ED = pd.read_csv(io.BytesIO(F["editions.csv"]))
    trans = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", " ": "-"})
    code = {n.lower().translate(trans): c for c, n in zip(ED["edition"], ED["name"])}
    cut = "2028-12-31 23:00:00"
    st = dict(zip(C["contact_id"], C["status"]))
    gr = {c: set(g.split("|")) if isinstance(g, str) else set() for c, g in zip(C["contact_id"], C["groups"])}
    implied = {"subscribed": None, "confirmed": "pending", "unsubscribed": "subscribed", "cleaned": "subscribed",
               "resubscribed": "unsubscribed"}
    later = E[(E["at_utc"] >= cut) & (E["event"] != "clicked")].sort_values("at_utc", kind="mergesort")
    seen = set()
    for c, ev in zip(later["contact_id"], later["event"]):
        if c not in seen:
            seen.add(c)
            st[c] = implied[ev]
    # every change to a contact's groups after midnight, undone newest first: the preference centre's (the groups before)
    # and the newsletters' one-click additions
    undo = {}
    for c, t, before in zip(Gc["contact_id"], Gc["changed_utc"], Gc["groups_before"]):
        if t >= cut:
            undo.setdefault(c, []).append((t, 0, before))
    k = E[(E["event"] == "clicked") & (E["at_utc"] >= cut) & E["link"].str.contains("/newsletter/ausgabe-hinzufuegen?", regex=False)]
    for c, t, link in zip(k["contact_id"], k["at_utc"], k["link"]):
        undo.setdefault(c, []).append((t, 1, code[link.rsplit("=", 1)[1]]))
    for c, items in undo.items():
        g = set(gr.get(c, set()))
        for t, kind, x in sorted(items, reverse=True):
            if kind == 0:
                g = set(x.split("|"))
            else:
                g.discard(x)
        gr[c] = g
    out = {}
    for c, s_ in st.items():
        if s_ == "subscribed":
            for g in gr[c]:
                out[g] = out.get(g, 0) + 1
    return out


def copies(F):
    S = pd.read_csv(io.BytesIO(F["circulation_subscriptions_2028q4.csv"]))
    # numbers are issued in order of entry: a start later than any start numbered above it was not the first delivery
    S = S.sort_values("sub_no", ascending=False).reset_index(drop=True)
    st = pd.to_datetime(S["start_date"])
    S["start_date"] = np.where(st > st.cummin().shift(1), "2028-09-30", S["start_date"])
    U = pd.read_csv(io.BytesIO(F["circulation_suspensions_2028q4.csv"]))
    A = pd.read_csv(io.BytesIO(F["epaper_accesses_2028q4.csv"]))
    X = pd.read_csv(io.BytesIO(F["single_copy_sales_2028q4.csv"]))
    T = pd.read_csv(io.BytesIO(F["retail_points.csv"]))
    ED = pd.read_csv(io.BytesIO(F["editions.csv"]))
    days = pd.date_range("2028-10-01", "2028-12-31")
    idx = {d: i for i, d in enumerate(days)}
    out = {}
    for _, e in ED.iterrows():
        hol = {"2028-10-03", "2028-12-25", "2028-12-26"} | ({"2028-11-01"} if e["state"] == "RP" else set())
        pub = np.array([d.weekday() < 6 and d.strftime("%Y-%m-%d") not in hol for d in days])
        sat = np.array([d.weekday() == 5 for d in days])
        n = np.zeros(len(days))
        s = S[(S["edition"] == e["edition"]) & (S["product"] != "TRIAL")]
        for sn, prod, cp, a, b in zip(s["sub_no"], s["product"], s["copies"], s["start_date"], s["end_date"].fillna("2099-12-31")):
            on = (days >= a) & (days <= b)
            if prod == "SATURDAY":
                on &= sat
            n += cp * on
        p = U[(U["kind"] == "pause") & U["sub_no"].isin(s["sub_no"])].merge(s[["sub_no", "product", "copies", "start_date", "end_date"]], on="sub_no")
        for prod, cp, f, t, a, b in zip(p["product"], p["copies"], p["from_date"], p["to_date"], p["start_date"], p["end_date"].fillna("2099-12-31")):
            off = (days >= f) & (days <= t) & (days >= a) & (days <= b)
            if prod == "SATURDAY":
                off &= sat
            n -= cp * off
        a_ = A[(A["edition"] == e["edition"]) & ~A["plan"].isin(["Digital Plus", "Trial 14 days"])]
        for a, b in zip(a_["start_date"], a_["end_date"].fillna("2099-12-31")):
            n += (days >= a) & (days <= b)
        x = X.merge(T, on="retail_point")
        x = x[x["edition"] == e["edition"]]
        total = n[pub].sum() + (x["delivered"] - x["returned"]).sum()
        out[e["edition"]] = total / pub.sum()
    return out


def main(src):
    F = unpack(src)
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    over = the_call(F)
    noted = sorted(e for e, v in over.items() if v > 25.0)
    check(noted == sorted(fig["call"]["noted"]), "the noted set %s" % noted)
    check(len(noted) == fig["call"]["n_noted"], "the count %d" % len(noted))
    check(min(over[e] for e in noted) > fig["components"]["noted_floor_pct"], "noted floor")
    check(max(v for e, v in over.items() if e not in noted) < fig["components"]["kept_ceiling_pct"], "kept ceiling")
    nl = newsletter(F)
    for c, v in fig["asks"]["newsletter_subscribers_2028_12_31"].items():
        check(nl.get(c) == v, "newsletter %s %s = %s" % (c, nl.get(c), v))
        check(("%s: %s" % (c, "{:,}".format(v))) in sub, "newsletter %s in submission" % c)
    cp = copies(F)
    for c, v in fig["asks"]["sold_copies_per_publication_day_q4"].items():
        check(int(round(cp[c])) == v, "copies %s %.2f -> %d" % (c, cp[c], v))
        check(("%s: %s" % (c, "{:,}".format(v))) in sub, "copies %s in submission" % c)
    print("%d FAIL" % len(FAILS))
    return FAILS


if __name__ == "__main__":
    f = main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target.zip"))
    sys.exit(1 if f else 0)
