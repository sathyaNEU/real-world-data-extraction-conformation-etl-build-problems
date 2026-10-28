"""task236 estimators, read only from the pack: the notified series counted under protocol CDB-FLU-03 from the gateway's
results (the person behind each result, the postcode a case's results recorded), each region's change in the share of
its influenza infections notified the golden way (its notified cases read against the sentinel network's
influenza-like-illness consultations attributed to influenza by its protocol swabs), the other ways of building that
index, the routes a solver reaches for instead, the two asks (season-to-date notified cases, the week 36 rate per
100,000 residents) and every careful reading of the asks' rows."""
import datetime as dt
import os
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd

CUTOFF_UTC = "2027-09-12T23:00:00Z"         # 09:00 on Monday 13 September 2027, local time (UTC+10)
CUTOFF_MISREAD = "2027-09-13T09:00:00Z"     # 09:00 read as UTC
REPORT_WEEK = 36
FIRST_WEEK = 14
WINDOW = 4
LINE = 0.25
EPISODE_DAYS = 14
EIGHT = ["FN", "NC", "TB", "CW", "MN", "MS", "MW", "SC"]
UNKNOWN = ("", "0000")


def load(target, files):
    rd = lambda k, **kw: pd.read_csv(os.path.join(target, files[k]), dtype=str, keep_default_na=False, **kw)
    D = dict(res=rd("res"), ret=rd("ret"), sw=rd("sw"), conc=rd("conc"), pop=rd("pop"))
    reg = pd.read_excel(os.path.join(target, files["reg"]), sheet_name="Register")
    reg["effective_date"] = pd.to_datetime(reg.effective_date).dt.date
    D["reg"] = reg
    return D


def iso_week(s):
    return pd.to_datetime(s).dt.isocalendar().week.astype(int)


def round_half(x, places=1):
    q = Decimal(1).scaleb(-places)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


# ------------------------------------------------------------------ the register: the eight changes and their weeks
def changes(D):
    r = D["reg"]
    r = r[r.region_code.isin(EIGHT)]
    return {row.region_code: (row.effective_date, row.effective_date.isocalendar()[1], row.change) for row in r.itertuples()}


def windows(cw):
    return list(range(cw - WINDOW, cw)), list(range(cw, cw + WINDOW))


# ------------------------------------------------------------------ CDB-FLU-03 s.2: notified cases from the results
def is_positive(result):
    t = result.str.lower()
    return ~(t.str.contains("not detected") | t.str.startswith("negative") | t.str.contains("no influenza"))


def concordance_now(D):
    c = D["conc"]
    return c[c.effective_to == ""].set_index("postcode").region_code


def persons(r, identity="person"):
    """the person behind each row. `person`: gateway keys that share a specimen are one person (a specimen is taken
    from one person), and a key whose rows' ages jump by more than a year carries two people (an infant registered
    under its mother's details); an age that rises by one is a birthday. `key`: every gateway key a person. `link`:
    keys joined through their specimens, no key split. `split_age`, `link_split_age`: a key split at every age it
    shows. `split_gap`: a key split where the ages jump, keys not joined."""
    key = r.patient_key
    if identity in ("person", "link", "link_split_age"):
        n = r.groupby("specimen_id").patient_key.nunique()
        shared = r[r.specimen_id.isin(n[n > 1].index)]
        parent = {}

        def find(x):
            while parent.get(x, x) != x:
                x = parent[x]
            return x
        for ks in shared.groupby("specimen_id", sort=True).patient_key.unique():
            ks = sorted(ks)
            for k in ks[1:]:
                a, b = find(ks[0]), find(k)
                if a != b:
                    parent[max(a, b)] = min(a, b)
        if parent:
            sel = key.isin(parent)
            key = key.copy()
            key[sel] = key[sel].map(find)
    if identity in ("split_age", "link_split_age"):
        return key + "|" + r.age_years.astype(str)
    if identity in ("person", "split_gap"):
        age = r.age_years.astype(int)
        ages = pd.DataFrame({"k": key.values, "a": age.values}).groupby("k").a.unique()
        label = {}
        for k, a in ages[ages.map(len) > 1].items():
            a = sorted(a)
            lab, cur = {a[0]: 0}, 0
            for x, y in zip(a, a[1:]):
                cur += int(y - x > 1)
                lab[y] = cur
            label[k] = lab
        if label:
            sel = key.isin(label)
            key = key.copy()
            key[sel] = ["%s|%d" % (k, label[k][a]) for k, a in zip(key[sel], age[sel])]
    return key


def first_reports(r, which):
    """each specimen read off one report: its first (`first`) or its latest final (`final`)"""
    if which == "first":
        return r[r.received_utc == r.groupby("specimen_id").received_utc.transform("min")]
    f = r[r.result_status == "F"]
    return f[f.received_utc == f.groupby("specimen_id").received_utc.transform("max")]


def cases(D, anchor="first", finals_only=False, asof=False, unknown="requester", interstate="exclude",
          identity="person", postcode="recorded", report=None):
    """one row per case: its first positive specimen's collection date and week, when it was notified (the first
    result reporting influenza for it reaching the gateway, UTC) and its region (s.2): the residential postcode its
    results recorded (`postcode="first"` reads the first row's alone), the requesting service's where none did"""
    r = D["res"]
    r = r.assign(person=persons(r, identity))
    if report:
        r = first_reports(r, report)
    p = r[is_positive(r.result)]
    if finals_only:
        p = p[p.result_status == "F"]
    p = p.sort_values(["person", "collection_date", "received_utc"])
    keys = p.person.values
    days = pd.to_datetime(p.collection_date).values.astype("datetime64[D]").astype(np.int64)
    ep = np.empty(len(p), dtype=np.int64)
    n, prev, first, last = -1, None, 0, 0
    for i in range(len(p)):
        k, d = keys[i], days[i]
        if k != prev:
            n += 1; first = last = d; prev = k
        else:
            ref = first if anchor == "first" else last
            if anchor != "person" and d - ref >= EPISODE_DAYS:
                n += 1; first = d
            last = d
        ep[i] = n
    p = p.assign(ep=ep)
    g = p.groupby("ep", sort=True)
    c = pd.DataFrame({"patient_key": g.patient_key.first(), "person": g.person.first(),
                      "first_collection": g.collection_date.min(), "notified_utc": g.received_utc.min(),
                      "postcode": g.residential_postcode.first(), "requester": g.requester_postcode.first()})
    if postcode == "recorded":
        rec = p[~p.residential_postcode.isin(UNKNOWN)].groupby("ep").residential_postcode.first()
        has = c.index.isin(rec.index)
        c.loc[has, "postcode"] = rec.reindex(c.index[has]).values
    now = concordance_now(D)
    unk = c.postcode.isin(UNKNOWN)
    c["region"] = c.postcode.map(now)
    if asof:
        moved = D["conc"][D["conc"].effective_to != ""]
        old = moved.set_index("postcode")
        until = old.effective_to.to_dict()
        sel = c.postcode.isin(until) & (c.first_collection <= c.postcode.map(until).fillna(""))
        c.loc[sel, "region"] = c.loc[sel, "postcode"].map(old.region_code)
    if unknown == "requester":
        c.loc[unk, "region"] = c.loc[unk, "requester"].map(now)
    elif unknown == "blank_only":            # 0000 taken for a postcode outside the state
        c.loc[c.postcode == "", "region"] = c.loc[c.postcode == "", "requester"].map(now)
    if interstate == "requester":            # residents of other states counted where they were tested
        out = c.region.isna() & ~unk
        c.loc[out, "region"] = c.loc[out, "requester"].map(now)
    c["week"] = iso_week(c.first_collection)
    return c[c.region.notna()].reset_index(drop=True)


def series(c, cutoff=CUTOFF_UTC):
    """the notified series as the week 36 report counts them: cases notified by the cut-off, by region and week"""
    d = c if cutoff is None else c[c.notified_utc <= cutoff]
    return d.groupby(["region", "week"]).size()


# ------------------------------------------------------------------ the sentinel network (SGP-2027 s.3 and s.4)
def sentinel(D, denom="list", positivity="pooled"):
    ret = D["ret"]
    r = ret[ret.return_status == "received"].copy()
    for col in ("list_size", "consultations", "ili_consultations"):
        r[col] = r[col].astype(float)
    r["week"] = r.iso_week.astype(int)
    g = r.groupby(["region_code", "week"])
    ili = g.ili_consultations.sum()
    if denom == "list":
        rate = ili / g.list_size.sum() * 1e5
    elif denom == "consultations":
        rate = ili / g.consultations.sum() * 1e3
    else:                                   # ILI consultations as counted, no denominator
        rate = ili
    sw = D["sw"].copy()
    sw = sw[sw.influenza_a != ""]
    region_of = ret.drop_duplicates("practice_code").set_index("practice_code").region_code
    sw["region"] = sw.practice_code.map(region_of)
    sw["week"] = iso_week(sw.collection_date)
    sw["flu"] = (sw.influenza_a == "detected") | (sw.influenza_b == "detected")
    if positivity == "pooled":
        pos = sw.groupby(["region", "week"]).flu.mean()
    else:                                   # the mean of the practices' own positivity
        pos = sw.groupby(["region", "practice_code", "week"]).flu.mean().groupby(["region", "week"]).mean()
    pos.index.names = ["region_code", "week"]
    return rate, pos


def index(rate, pos):
    return (rate * pos).dropna()


# ------------------------------------------------------------------ s.4: the change in the share notified
def window_sum(s, code, weeks):
    return float(sum(s.get((code, w), 0.0) for w in weeks))


def share_change(N, X, ch, how="sums"):
    out = {}
    for code, (_, cw, _) in ch.items():
        b, a = windows(cw)
        if how == "sums":
            out[code] = (window_sum(N, code, a) / window_sum(X, code, a)) / (window_sum(N, code, b) / window_sum(X, code, b))
        else:                                # the mean of the weekly ratios
            m = lambda ws: np.mean([N.get((code, w), 0) / X[(code, w)] for w in ws])
            out[code] = m(a) / m(b)
    return out


def flagged(ratios, line=LINE, down=None):
    lo = 1 - line if down is None else down
    return {c for c, v in ratios.items() if v > 1 + line or v < lo}


# ------------------------------------------------------------------ the routes a solver reaches for instead
def tests_by_region(D):
    r = D["res"]
    now = concordance_now(D)
    s = r.assign(pos=is_positive(r.result)).groupby("specimen_id").agg(
        pos=("pos", "max"), pc=("residential_postcode", "first"), req=("requester_postcode", "first"),
        d=("collection_date", "first"))
    s["region"] = np.where(s.pc.isin(UNKNOWN), s.req.map(now), s.pc.map(now))
    s = s[pd.notna(s.region)]
    s["week"] = iso_week(s.d)
    return s.groupby(["region", "week"]).size(), s.groupby(["region", "week"]).pos.sum()


def rungs(D, N, ch):
    rate, pos = sentinel(D)
    T, TP = tests_by_region(D)
    out = {}
    out["raw"] = {c: window_sum(N, c, windows(cw)[1]) / window_sum(N, c, windows(cw)[0]) for c, (_, cw, _) in ch.items()}
    out["positivity"] = share_change(TP, T, ch)
    out["notified_per_test"] = share_change(N, T, ch)
    out["per_ili_rate"] = share_change(N, rate, ch)
    out["per_swab_positivity"] = share_change(N, pos, ch)
    ref = lambda ws: sum(N.get((c, w), 0) for c in ("SW", "FW") for w in ws)
    out["against_unchanged_regions"] = {c: out["raw"][c] / (ref(windows(cw)[1]) / ref(windows(cw)[0]))
                                        for c, (_, cw, _) in ch.items()}
    return out


def corridor(D, ch):
    """every way of building the index and the series that a careful analyst could take: the flags they give"""
    base = cases(D)
    N = series(base)
    out = {}
    for name, (denom, posn) in {"ili per 100,000 patients, pooled positivity": ("list", "pooled"),
                                "ili per 1,000 consultations": ("consultations", "pooled"),
                                "ili consultations counted": ("count", "pooled"),
                                "practices' own positivity averaged": ("list", "practice")}.items():
        rate, pos = sentinel(D, denom, posn)
        out[name] = share_change(N, index(rate, pos), ch)
    rate, pos = sentinel(D)
    X = index(rate, pos)
    out["mean of the weekly ratios"] = share_change(N, X, ch, how="weekly")
    out["episodes anchored on the previous positive"] = share_change(series(cases(D, anchor="rolling")), X, ch)
    out["final reports only"] = share_change(series(cases(D, finals_only=True)), X, ch)
    out["regions as at collection"] = share_change(series(cases(D, asof=True)), X, ch)
    out["cases without a postcode left out"] = share_change(series(cases(D, unknown="drop")), X, ch)
    out["no cut-off"] = share_change(series(base, None), X, ch)
    return out


# ------------------------------------------------------------------ the asks
def erp_by_region(D, how="now"):
    c, pop = D["conc"], D["pop"].set_index("postcode").erp_30_june_2026.astype(int)
    if how == "now":
        c = c[c.effective_to == ""]
    elif how == "old":
        c = c[c.effective_from == c.effective_from.min()]
    return c.assign(e=c.postcode.map(pop)).groupby("region_code").e.sum()


def season_to_date(c, cutoff=CUTOFF_UTC):
    d = c if cutoff is None else c[c.notified_utc <= cutoff]
    d = d[d.week.between(FIRST_WEEK, REPORT_WEEK)]
    return d.groupby("region").size().reindex(EIGHT).fillna(0).astype(int).to_dict()


def week_rate(c, erp, cutoff=CUTOFF_UTC, raw=False):
    d = c if cutoff is None else c[c.notified_utc <= cutoff]
    n = d[d.week == REPORT_WEEK].groupby("region").size().reindex(EIGHT).fillna(0)
    v = {k: n[k] / erp[k] * 1e5 for k in EIGHT}
    return v if raw else {k: round_half(x, 1) for k, x in v.items()}


def ask_stops(D):
    erp = erp_by_region(D)
    base = cases(D)
    v = {"episodes anchored on the previous positive": cases(D, anchor="rolling"),
         "final reports only": cases(D, finals_only=True),
         "regions as at collection": cases(D, asof=True),
         "cases without a postcode left out": cases(D, unknown="drop"),
         "0000 read as a postcode outside the state": cases(D, unknown="blank_only"),
         "residents of other states counted where tested": cases(D, interstate="requester")}
    A = {k: season_to_date(x) for k, x in v.items()}
    A["no cut-off"] = season_to_date(base, None)
    A["cut-off read as 09:00 UTC"] = season_to_date(base, CUTOFF_MISREAD)
    B = {k: week_rate(x, erp) for k, x in v.items()}
    B["no cut-off"] = week_rate(base, erp, None)
    B["cut-off read as 09:00 UTC"] = week_rate(base, erp, CUTOFF_MISREAD)
    B["every concordance row summed"] = week_rate(base, erp_by_region(D, "all"))
    B["population on the old boundaries"] = week_rate(base, erp_by_region(D, "old"))
    return A, B


def readings(D):
    """the cases under every careful reading in READINGS, the cracker's among them"""
    return {name: cases(D, **kw) for name, kw in READINGS.items()}


# every careful reading of who a person is, which postcode places a case and which report a specimen is read off; the
# golden is the one with `identity="person"`, `postcode="recorded"` and every report read
IDENTITIES = {"key": "every gateway key a person", "link": "keys sharing a specimen joined, no key split",
              "split_age": "each key split at every age it shows", "split_gap": "keys split where ages jump, not joined",
              "link_split_age": "keys joined, then split at every age", "person": "keys joined and split where ages jump"}
POSTCODES = {"first": "the first row's postcode", "recorded": "the postcode any of its results recorded"}
REPORTS = {None: "every report", "first": "each specimen's first report", "final": "each specimen's latest final"}
READINGS = {"%s; %s; %s" % (IDENTITIES[i], POSTCODES[p], REPORTS[u]): dict(identity=i, postcode=p, report=u)
            for i in IDENTITIES for p in POSTCODES for u in REPORTS
            if (i, p, u) != ("person", "recorded", None)}
CRACKER = "%s; %s; %s" % (IDENTITIES["key"], POSTCODES["first"], REPORTS[None])


# ------------------------------------------------------------------ everything the goldens and the write-up owe
def solve(target, files):
    D = load(target, files)
    ch = changes(D)
    c = cases(D)
    N = series(c)
    rate, pos = sentinel(D)
    X = index(rate, pos)
    ratio = share_change(N, X, ch)
    flags = flagged(ratio)
    erp = erp_by_region(D)
    A = season_to_date(c)
    B = week_rate(c, erp)
    Braw = week_rate(c, erp, raw=True)
    weeks = list(range(26, REPORT_WEEK + 1))
    panel = {code: dict(weeks=weeks, notified=[int(N.get((code, w), 0)) for w in weeks],
                        index=[float(X.get((code, w), np.nan)) for w in weeks]) for code in EIGHT}
    win = {}
    for code, (_, cw, _) in ch.items():
        b, a = windows(cw)
        win[code] = dict(before=int(window_sum(N, code, b)), after=int(window_sum(N, code, a)),
                         x_before=window_sum(X, code, b), x_after=window_sum(X, code, a))
    return dict(D=D, changes=ch, cases=c, N=N, X=X, rate=rate, pos=pos, ratio=ratio, flags=flags, erp=erp,
                season=A, rate36=B, rate36_raw=Braw, panel=panel, windows=win)
