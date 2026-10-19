"""task249's solver: everything is read from the target folder.  The call (which editions' quarter figure carries the
measurement note), the routes a competent analyst might take instead, and the two asks (newsletter subscribers at the
year's end, sold copies per publication day)."""
import datetime as dt
import os
import numpy as np
import pandas as pd

MONTHS = (10, 11, 12)
DEVS = ("mobile", "tablet", "desktop")
CAP = 7 * 86400
NEWSROOM = "85.214.110.0"
YEAR_END_UTC = pd.Timestamp("2028-12-31 23:00:00")
TOL = 25.0


# ------------------------------------------------------------------------------------------- loading
def load(target, files):
    L = {"target": target, "files": files}
    X = pd.read_parquet(os.path.join(target, files["sessions"]))
    X["session_start"] = X["session_start"].dt.tz_convert("UTC").dt.tz_localize(None)
    X["session_end"] = X["session_end"].dt.tz_convert("UTC").dt.tz_localize(None)
    L["raw"] = X
    L["register"] = pd.read_csv(os.path.join(target, files["register"]), dtype={"client_id": str, "device_id": str})
    L["accounts"] = pd.read_csv(os.path.join(target, files["accounts"]))
    L["editions"] = pd.read_csv(os.path.join(target, files["editions"]))
    rep = pd.read_excel(os.path.join(target, files["report"]), header=2)
    L["report"] = rep
    return L


def clean(L, webkit="engine", months_tz="Europe/Berlin", dedupe=True, drop_internal=True, drop_bots=True):
    """the quarter's reader sessions: bots and the newsroom out, the re-sent rows out, Hollerfeld's old code mapped,
    Berlin months, the engine read from os and browser"""
    X = L["raw"]
    if drop_bots:
        X = X[~X["is_bot"]]
    if drop_internal:
        X = X[X["ip_prefix"] != NEWSROOM]
    if dedupe:
        X = X.drop_duplicates()
    X = X.copy()
    old = L["editions"].dropna(subset=["former_content_group"])
    X["edition"] = X["content_group"].replace(dict(zip(old["former_content_group"], old["edition"])))
    loc = X["session_start"].dt.tz_localize("UTC").dt.tz_convert(months_tz) if months_tz else X["session_start"]
    X["month"] = loc.dt.month.values
    X = X[X["month"].isin(MONTHS) & (loc.dt.year.values == 2028)]
    if webkit == "engine":
        X["wk"] = (X["os"] == "iOS") | ((X["os"] == "Macintosh") & (X["browser"] == "Safari"))
    elif webkit == "safari":
        X["wk"] = X["browser"].isin(["Safari", "Safari (in-app)"])
    elif webkit == "safari_only":
        X["wk"] = X["browser"] == "Safari"
    X["dev"] = X["device_category"]
    return X.sort_values(["client_id", "session_start"], kind="mergesort").reset_index(drop=True)


def sign_in(L):
    """client_id -> (device_id, origin) from the sign-in register and the accounts"""
    G = L["register"].merge(L["accounts"][["account_no", "origin"]], on="account_no", how="left")
    cmap = G.drop_duplicates("client_id").set_index("client_id")
    return cmap["device_id"], cmap["origin"]


# ------------------------------------------------------------------------------------------- the replay
def replay_runs(X, per_edition=False):
    """the seven-day rule replayed on each identifier's own sessions (site-wide, or within each edition): for every
    identifier, edition and month, the number of replayed identifiers it would have had"""
    key = ["client_id", "edition"] if per_edition else ["client_id"]
    Y = X.sort_values(key + ["session_start"], kind="mergesort")
    st = Y["session_start"].values.astype("datetime64[s]").astype(np.int64)
    en = Y["session_end"].values.astype("datetime64[s]").astype(np.int64)
    same = np.ones(len(Y), bool)
    for k in key:
        v = Y[k].values
        same[1:] &= v[1:] == v[:-1]
    same[0] = False
    prev_end = np.r_[0, en[:-1]]
    new = ~same | ((st - prev_end) > CAP)
    run = np.cumsum(new)
    Z = pd.DataFrame({"client_id": Y["client_id"].values, "edition": Y["edition"].values, "month": Y["month"].values, "run": run})
    return Z.drop_duplicates().groupby(["client_id", "edition", "month"]).size().rename("runs")


# ------------------------------------------------------------------------------------------- the call
def strata(L, X=None, per_edition_replay=False):
    """per edition, month and device: the counts every route is built from"""
    X = clean(L) if X is None else X
    dev_of, origin_of = sign_in(L)
    A = X[["client_id", "edition", "month", "dev", "wk"]].drop_duplicates()
    A["device_id"] = A["client_id"].map(dev_of)
    A["origin"] = A["client_id"].map(origin_of)
    A["signed"] = A["device_id"].notna()
    A["printed"] = A["origin"] == "print subscription"
    runs = replay_runs(X, per_edition=per_edition_replay)
    A = A.join(runs, on=["client_id", "edition", "month"])
    ses = X.groupby(["client_id", "edition", "month"]).size().rename("sessions")
    A = A.join(ses, on=["client_id", "edition", "month"])
    pv = X.groupby(["client_id", "edition", "month"])["page_views"].sum().rename("pv")
    A = A.join(pv, on=["client_id", "edition", "month"])
    return A


def routes(A):
    """every route's estimate of each edition's browsers per month, averaged over the quarter, against the reported
    average: returns a frame of overstatements in per cent"""
    out = {}
    reported = A.groupby(["edition", "month"])["client_id"].nunique()

    def ratio(df):
        return df["runs"].sum() / len(df) if len(df) else np.nan
    rows = []
    # the replayed identifiers per browser pooled over the quarter's three months, by edition and device class
    q = A[~A["wk"] & ~A["printed"]]
    eq = (q.groupby(["edition", "dev"])["runs"].sum() / q.groupby(["edition", "dev"]).size()).to_dict()
    for (e, m), g in A.groupby(["edition", "month"]):
        est = {k: 0.0 for k in ("golden", "g_q", "g_nodev", "g_vis", "g_vis2", "g_pv", "r2d", "r2", "r3a", "r4", "r4p", "r1a", "r1c", "r6")}
        nwk = g[~g["wk"]]
        wkg = g[g["wk"]]
        # pooled-device quantities
        np_all = nwk[~nwk["printed"]]
        e_np_all = ratio(np_all)
        est["g_nodev"] = nwk["client_id"].nunique() + wkg.loc[wkg["printed"], "device_id"].nunique() + \
            wkg.loc[~wkg["printed"], "client_id"].nunique() / e_np_all
        cnp_all = wkg[~wkg["printed"]]
        est["g_vis2"] = nwk["client_id"].nunique() + wkg.loc[wkg["printed"], "device_id"].nunique() + \
            cnp_all["sessions"].sum() / (np_all["sessions"].sum() / len(np_all))
        e_all = ratio(nwk)
        est["r2"] = nwk["client_id"].nunique() + wkg["client_id"].nunique() / e_all
        s_wk = wkg[wkg["signed"]]
        r1 = s_wk["client_id"].nunique() / max(s_wk["device_id"].nunique(), 1)
        est["r1a"] = nwk["client_id"].nunique() + wkg["client_id"].nunique() / r1
        sg_dev = g[g["signed"]].drop_duplicates("device_id")
        share = sg_dev["wk"].mean()
        est["r6"] = nwk["client_id"].nunique() / (1 - share)
        for d in DEVS:
            gd = g[g["dev"] == d]
            u = gd[~gd["wk"]]; c = gd[gd["wk"]]
            U = u["client_id"].nunique()
            unp = u[~u["printed"]]
            e_np = ratio(unp)
            est["golden"] += U + c.loc[c["printed"], "device_id"].nunique() + c.loc[~c["printed"], "client_id"].nunique() / e_np
            est["g_q"] += U + c.loc[c["printed"], "device_id"].nunique() + c.loc[~c["printed"], "client_id"].nunique() / eq[(e, d)]
            v_np = unp["sessions"].sum() / len(unp)
            cnp = c[~c["printed"]]
            est["g_vis"] += U + c.loc[c["printed"], "device_id"].nunique() + cnp["sessions"].sum() / v_np
            est["g_pv"] += U + c.loc[c["printed"], "device_id"].nunique() + cnp["pv"].sum() / (unp["pv"].sum() / len(unp))
            e_d = ratio(u)
            est["r2d"] += U + c["client_id"].nunique() / e_d
            ua = u[~u["signed"]]
            e_an = ratio(ua)
            cs = c[c["signed"]]; ca = c[~c["signed"]]
            est["r3a"] += U + cs["device_id"].nunique() + ca["client_id"].nunique() / e_an
            est["r4"] += U + cs["device_id"].nunique() + ca["client_id"].nunique() / e_d
            est["r4p"] += U + cs["device_id"].nunique() + ca["client_id"].nunique() / e_np
            r1d = cs["client_id"].nunique() / max(cs["device_id"].nunique(), 1)
            est["r1c"] += U + c["client_id"].nunique() / r1d
        est["reported"] = reported[(e, m)]
        est["edition"], est["month"] = e, m
        rows.append(est)
    M = pd.DataFrame(rows)
    # the pooled-across-editions identifiers per signed-in WebKit device, month by month
    r1b = {}
    for m, g in A[A["wk"] & A["signed"]].groupby("month"):
        r1b[m] = g.drop_duplicates(["edition", "client_id"]).shape[0] / g.drop_duplicates(["edition", "device_id"]).shape[0]
    wk_ids = A[A["wk"]].groupby(["edition", "month"])["client_id"].nunique()
    nwk_ids = A[~A["wk"]].groupby(["edition", "month"])["client_id"].nunique()
    M["r1b"] = [nwk_ids[(e, m)] + wk_ids[(e, m)] / r1b[m] for e, m in zip(M["edition"], M["month"])]
    Q = M.groupby("edition").mean(numeric_only=True)
    res = pd.DataFrame({k: 100 * (Q["reported"] / Q[k] - 1) for k in Q.columns if k not in ("reported", "month")})
    res["reported"] = Q["reported"]
    res["browsers"] = Q["golden"]
    res["r0"] = 0.0
    return res


def main_call(L):
    A = strata(L)
    res = routes(A)
    res["note"] = res["golden"] > TOL
    L["A"] = A
    return res


def golden_set(res, col="golden"):
    return sorted(res.index[res[col] > TOL])


def report_average(L):
    """the platform's reported figure: each edition's users averaged over October, November and December"""
    rep = L["report"].copy()
    rep.columns = ["content_group"] + list(range(1, 13))
    old = L["editions"].dropna(subset=["former_content_group"])
    rep["edition"] = rep["content_group"].replace(dict(zip(old["former_content_group"], old["edition"])))
    q = rep.groupby("edition")[[10, 11, 12]].sum(min_count=1)
    return q.mean(axis=1)


# ------------------------------------------------------------------------------------------- ask: newsletter
def slug(name):
    s = name.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss"), (" ", "-")):
        s = s.replace(a, b)
    return s


ADD_PATH = "/newsletter/ausgabe-hinzufuegen?ausgabe="


def newsletter(target, files, groups_as_of=True, status_as_of=True, cutoff=YEAR_END_UTC, link_adds="after"):
    """confirmed subscribers in each edition's group at the cutoff: the export's status and groups taken back through
    the activity log and the preference centre's changes; link_adds: the groups the newsletters' one-click links added,
    undone after the cutoff ("after"), not at all (None) or every one ever ("all")"""
    C = pd.read_csv(os.path.join(target, files["nl_contacts"]), parse_dates=["first_optin_utc", "last_changed_utc"])
    E = pd.read_csv(os.path.join(target, files["nl_log"]), parse_dates=["at_utc"], keep_default_na=False)
    G = pd.read_csv(os.path.join(target, files["nl_groups"]), parse_dates=["changed_utc"])
    ED = pd.read_csv(os.path.join(target, files["editions"]))
    code_of = {slug(n): c for c, n in zip(ED["edition"], ED["name"])}
    status = C.set_index("contact_id")["status"].copy()
    groups = C.set_index("contact_id")["groups"].copy()
    if status_as_of:
        before = {"subscribed": "none", "confirmed": "pending", "unsubscribed": "subscribed", "cleaned": "subscribed",
                  "resubscribed": "unsubscribed"}
        st = E[(E["at_utc"] >= cutoff) & (E["event"] != "clicked")]
        after = st.sort_values(["contact_id", "at_utc"]).drop_duplicates("contact_id")
        status.loc[after["contact_id"].values] = after["event"].map(before).values
    if groups_as_of:
        ch = G[G["changed_utc"] >= cutoff].rename(columns={"changed_utc": "t"})[["contact_id", "t", "groups_before"]]
        ch = ch.assign(added=None)
        adds = E[(E["event"] == "clicked") & E["link"].str.contains(ADD_PATH, regex=False)]
        adds = adds.assign(added=adds["link"].str.split("ausgabe=").str[1].map(code_of))
        if link_adds == "after":
            late = adds[adds["at_utc"] >= cutoff].rename(columns={"at_utc": "t"})[["contact_id", "t", "added"]]
            ch = pd.concat([ch, late.assign(groups_before=None)], ignore_index=True)
        ch = ch.sort_values(["contact_id", "t"], ascending=[True, False], kind="mergesort")
        for cid, rows in ch.groupby("contact_id", sort=False):
            g = set(groups.get(cid, "").split("|")) - {""}
            for gb, ad in zip(rows["groups_before"].values, rows["added"].values):
                if ad is not None and isinstance(ad, str):
                    g.discard(ad)
                else:
                    g = set(gb.split("|"))
            groups.loc[cid] = "|".join(sorted(g))
        if link_adds == "all":
            for cid, ad in zip(adds["contact_id"].values, adds["added"].values):
                g = set(groups.get(cid, "").split("|")) - {""}
                g.discard(ad)
                groups.loc[cid] = "|".join(sorted(g))
    sub = groups[status == "subscribed"].dropna()
    sub = sub[sub != ""]
    counts = sub.str.split("|").explode().value_counts()
    return counts


# ------------------------------------------------------------------------------------------- ask: sold copies
HOLIDAYS = {"HE": ["2028-10-03", "2028-12-25", "2028-12-26"], "RP": ["2028-10-03", "2028-11-01", "2028-12-25", "2028-12-26"]}


def pub_days(state, holidays=True):
    d = pd.date_range("2028-10-01", "2028-12-31")
    d = d[d.weekday < 6]
    if holidays:
        d = d[~d.isin(pd.to_datetime(HOLIDAYS[state]))]
    return d


RELEASE = (pd.Timestamp("2028-11-06"), pd.Timestamp("2028-12-14"))


def restore_starts(S, how="sequence"):
    """subscription numbers are issued in order of entry, so a start date later than that of a subscription numbered
    after it cannot be the first day of delivery: such a subscription was delivered before the quarter.  how="window"
    takes every start inside the circulation release's weeks as before the quarter instead"""
    S = S.sort_values("sub_no").copy()
    if how == "sequence":
        later_min = S["start_date"].values[::-1]
        later_min = np.minimum.accumulate(later_min)[::-1]
        later_min = np.r_[later_min[1:], np.datetime64("2099-12-31")]
        moved = S["start_date"].values > later_min
    elif how == "window":
        moved = ((S["start_date"] >= RELEASE[0]) & (S["start_date"] < RELEASE[1])).values
    else:
        moved = np.zeros(len(S), bool)
    S.loc[moved, "start_date"] = pd.Timestamp("2028-09-30")
    return S, int(moved.sum())


def sold_copies(target, files, combi_addon=False, pauses=True, saturday=True, trials=False, holidays=True,
                forward_sold=True, restore="sequence"):
    S = pd.read_csv(os.path.join(target, files["subs"]), parse_dates=["start_date", "end_date"])
    S, _ = restore_starts(S, restore)
    U = pd.read_csv(os.path.join(target, files["susp"]), parse_dates=["from_date", "to_date"])
    A = pd.read_csv(os.path.join(target, files["epaper"]), parse_dates=["start_date", "end_date"])
    X = pd.read_csv(os.path.join(target, files["single"]), parse_dates=["issue_date"])
    T = pd.read_csv(os.path.join(target, files["points"]))
    ED = pd.read_csv(os.path.join(target, files["editions"]))
    out = {}
    X = X.merge(T[["retail_point", "edition"]], on="retail_point", how="left")
    X["sold"] = X["delivered"] - X["returned"]
    for _, e in ED.iterrows():
        code = e["edition"]
        days = pub_days(e["state"], holidays)
        far = pd.Timestamp("2099-12-31")
        s = S[S["edition"] == code].copy()
        if not trials:
            s = s[s["product"] != "TRIAL"]
        s["end"] = s["end_date"].fillna(far)
        total = 0.0
        stop = U[U["kind"] == "pause"] if forward_sold else U
        stop = stop[stop["sub_no"].isin(s["sub_no"])]
        a = A[A["edition"] == code].copy()
        if not combi_addon:
            a = a[a["plan"] != "Digital Plus"]
        a = a[a["plan"] != "Trial 14 days"] if not trials else a
        a["end"] = a["end_date"].fillna(far)
        sv, sc, sp = s["start_date"].values, s["end"].values, s["product"].values
        cp = s["copies"].values
        paused = {}
        for sn, f, t in zip(stop["sub_no"], stop["from_date"], stop["to_date"]):
            paused.setdefault(sn, []).append((f, t))
        pidx = np.isin(s["sub_no"].values, list(paused))
        for d in days:
            act = (sv <= np.datetime64(d)) & (sc >= np.datetime64(d))
            if saturday:
                act &= (sp != "SATURDAY") | (d.weekday() == 5)
            n = cp[act].sum()
            if pauses and pidx.any():
                for sn, c in zip(s["sub_no"].values[act & pidx], cp[act & pidx]):
                    if any(f <= d <= t for f, t in paused[sn]):
                        n -= c
            n += ((a["start_date"] <= d) & (a["end"] >= d)).sum()
            total += n
        xs = X[(X["edition"] == code)]
        total += xs["sold"].sum()
        nd = len(days) if holidays else len(pub_days(e["state"], False))
        out[code] = total / nd
    return pd.Series(out)
