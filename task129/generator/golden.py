"""task129 generator: every rung, rival read and graded figure, computed from the files as written
under target/. The generator asserts on these; verify.py recomputes them on its own code path."""
import json
import os
import re

import numpy as np
import pandas as pd

import params as P

F = dict(
    spine="rum_mobile_views_2026.parquet", release="release_train_log_2026.csv",
    rollout="boelge_rollout_log.csv", changes="change_register_2026.xlsx",
    registry="device_registry_2026-09.csv", subs="subscription_register_extract_2026-09-05.csv",
    editions="edition_register.csv", sla="page_delivery_service_level_v3.pdf",
    paywall="paywall_terms_subscriber_layout_2026.pdf",
    closeout="digital_ops_q3_service_closeout.xlsx", cdn="image_cdn_delivery_2026.csv",
    cdnapp="image_cdn_vendor_appendix.pdf", guide="rum_export_field_guide.md",
    thread="service_review_prep_thread.txt", manifest="export_manifest.csv",
    desktop="desktop_field_summary_2026.csv", amp="amp_landing_views_2026.csv",
    news="newsletter_sends_2026.csv",
)
DISTRACTORS = ["desktop", "amp", "news"]
LETTER = {v[0]: k for k, v in P.CHG.items()}
WIN = pd.Timedelta(days=28)


def _utc(s):
    return pd.to_datetime(s, utc=True).dt.tz_localize(None)


def load(tgt, spine_cols=None):
    L = {}
    L["spine"] = pd.read_parquet(os.path.join(tgt, F["spine"]), columns=spine_cols)
    for k in ["release", "rollout", "registry", "subs", "editions", "cdn"]:
        L[k] = pd.read_csv(os.path.join(tgt, F[k]), keep_default_na=False, dtype=str)
    L["closeout"] = pd.read_excel(os.path.join(tgt, F["closeout"]), sheet_name="By title", header=3)
    return L


# ------------------------------------------------------------------ the view frame
def deploy_utc(L):
    r = L["release"]
    return np.sort(_utc(r.deployed_at).values)


def switch_times(L):
    ro = L["rollout"]
    ads = ro[ro.layout == "ad-supported"]
    sw = {row.template_groups: _utc(pd.Series([row.switched_on])).iloc[0] for row in ads.itertuples()}
    r = L["release"]
    t = {}
    af = ro[ro.layout != "ad-supported"]
    assert len(af) == 1
    t["SUB"] = _utc(af.switched_on).iloc[0]
    for letter in "EBD":
        m = r.notes.str.contains(P.CHG[letter][0])
        assert m.sum() == 1
        t[letter] = _utc(r.deployed_at[m]).iloc[0]
    m = r.notes.str.contains(P.CHG["A"][0]) & r.notes.str.contains("spil", case=False)
    assert m.sum() == 1
    t["PUZ"] = _utc(r.deployed_at[m]).iloc[0]
    return sw, t


REPEAT_S = 600


def repeated_beacons(s):
    """Rows that repeat an earlier beacon of the same device for the same page view under another
    page-view key: same page and the same three timings, within ten minutes (the local-edition
    container's older library sent such a second beacon under its own key and send time)."""
    x = s[s.lcp_ms.notna()]
    t = x.ts_utc.dt.tz_convert(None) if x.ts_utc.dt.tz is not None else x.ts_utc
    k = pd.DataFrame({"d": x.device_key.values, "u": x.url_path.values, "l": x.lcp_ms.values,
                      "b": x.ttfb_ms.values, "c": x.cls.values, "t": t.values, "p": x.pv_id.values},
                     index=x.index)
    k = k.sort_values(["d", "u", "l", "b", "c", "t", "p"], kind="stable")
    same = ((k.d.values[1:] == k.d.values[:-1]) & (k.u.values[1:] == k.u.values[:-1])
            & (k.l.values[1:] == k.l.values[:-1]) & (k.b.values[1:] == k.b.values[:-1])
            & (k.c.values[1:] == k.c.values[:-1]) & (k.p.values[1:] != k.p.values[:-1]))
    gap = (k.t.values[1:] - k.t.values[:-1]) / np.timedelta64(1, "s")
    rep = np.r_[False, same & (gap <= REPEAT_S)]
    return pd.Index(k.index[rep])


def views(L, dedup=True, phones=True, repeats=True):
    s = L["spine"]
    if dedup:
        s = s.sort_values("beacon_id", kind="stable").drop_duplicates("pv_id", keep="first")
    if repeats:
        s = s.drop(index=repeated_beacons(s))
    reg = L["registry"].set_index("device_model")
    ff = reg.form_factor.reindex(s.device_model.values).values
    v = pd.DataFrame({
        "ts": s.ts_utc.dt.tz_localize(None).values if s.ts_utc.dt.tz is not None else s.ts_utc.values,
        "device_key": s.device_key.values, "account_key": s.account_key.values,
        "title": s.title.values, "template": s.template.values, "url_path": s.url_path.values,
        "ff": ff, "pclass": reg.perf_band.reindex(s.device_model.values).values,
        "lcp": s.lcp_ms.values, "w": s.sample_weight.values.astype(float),
        "nav": s.navigation_type.values, "ref": s.referrer_class.values,
        "ect": s.effective_connection_type.values, "browser": s.browser.values,
        "pv_id": s.pv_id.values,
    })
    if phones:
        v = v[v.ff == "phone"].reset_index(drop=True)
    loc = pd.DatetimeIndex(v.ts).tz_localize("UTC").tz_convert(P.TZ).tz_localize(None)
    v["local"] = loc
    v["month"] = loc.month
    v["day"] = loc.normalize()
    v["scored"] = ~pd.isna(v.lcp)
    v["over"] = v.lcp.fillna(0).values > 4000
    # local-edition pages and the masthead they are reported under today
    ed = v.url_path.str.extract(r"^/lokal/([a-z\-]+)/")[0]
    v["edition"] = ed.fillna("").values
    er = L["editions"]
    cur = er[er.valid_to == ""].set_index("edition_slug").masthead
    v["title_cur"] = np.where(v.edition != "", cur.reindex(v.edition.values).values, v.title.values)
    # release-train state: first view of the device since the latest deploy
    du = deploy_utc(L)
    v = v.sort_values(["device_key", "ts"], kind="stable").reset_index(drop=True)
    k = np.searchsorted(du, v.ts.values, side="right") - 1
    d = v.device_key.values
    v["state"] = np.where(np.r_[True, d[1:] != d[:-1]] | np.r_[True, k[1:] != k[:-1]], "F", "K")
    v["landing_proxy"] = landing_proxy(v)
    # subscriber at view time (subscription register)
    sb = L["subs"]
    sb = sb[sb.account_key != ""]
    st = pd.to_datetime(sb.start_date)
    en = pd.to_datetime(sb.end_date.replace("", "2100-01-01"))
    act = np.zeros(len(v), bool)
    acc = v.account_key.fillna("").values
    m = acc != ""
    if m.any():
        tab = pd.DataFrame({"account_key": sb.account_key.values, "st": st.values, "en": en.values})
        q = pd.DataFrame({"i": np.flatnonzero(m), "account_key": acc[m], "day": v.day.values[m]})
        j = q.merge(tab, on="account_key", how="inner")
        j = j[(j.day >= j.st) & (j.day <= j.en)]
        act[j.i.unique()] = True
    v["sub"] = act
    tpl = v.template.values
    coh = np.isin(tpl, P.COHORTS)
    g = np.full(len(v), "legacy", dtype=object)
    g[coh & act] = "sub"
    g[coh & ~act] = "base"
    g[(tpl == "spil") & act] = "subpuz"
    g[(tpl == "spil") & ~act] = "puz"
    v["group"] = g
    return v


def landing_proxy(v):
    """First view of a 30-minute visit (a partial-correction rival, never the golden)."""
    d = v.device_key.values
    gap = np.r_[np.inf, (v.ts.values[1:] - v.ts.values[:-1]) / np.timedelta64(1, "m")]
    return np.where(np.r_[True, d[1:] != d[:-1]] | (gap > 30), "F", "K")


# ------------------------------------------------------------------ main call
def share(df):
    s = df[df.scored]
    return (s.w * s.over).sum() / s.w.sum()


def _cells(df, by):
    s = df[df.scored]
    if not by:
        return pd.Series({(): (s.w * s.over).sum() / s.w.sum()})
    g = s.assign(wo=s.w * s.over).groupby(by)
    return g.wo.sum() / g.w.sum()


def windows(v, group, sw, t, win=WIN):
    d = v[v.group == group]
    pre, post = [], []
    if group in ("puz", "sub"):
        k = "PUZ" if group == "puz" else "SUB"
        pre.append(d[(d.ts >= t[k] - win) & (d.ts < t[k])])
        post.append(d[(d.ts >= t[k]) & (d.ts < t[k] + win)])
    else:
        for c in P.COHORTS:
            x = d[d.template == c]
            pre.append(x[(x.ts >= sw[c] - win) & (x.ts < sw[c])])
            post.append(x[(x.ts >= sw[c]) & (x.ts < sw[c] + win)])
    return pd.concat(pre), pd.concat(post)


def effects(v, group, sw, t, by, win=WIN):
    pre, post = windows(v, group, sw, t, win)
    return _cells(post, by) - _cells(pre, by)


def august(v):
    return v[(v.month == 8) & v.scored]


def apply(aug, eff, by, fill=None):
    if not by:
        return float(aug.w.sum() * eff.iloc[0])
    w = aug.groupby(by).w.sum()
    e = eff.reindex(w.index)
    if fill is not None and e.isna().any():
        e = e.fillna(pd.Series(fill.reindex(w.index.get_level_values(0)).values, index=w.index))
    assert not e.isna().any(), "cell without an effect"
    return float((w * e).sum())


def main_call(v, L, by_state="state", win=WIN):
    sw, t = switch_times(L)
    a = august(v)
    base, sub, puz = a[a.group == "base"], a[a.group == "sub"], a[a.group == "puz"]
    out = {}
    for name, by in (("raw", []), ("phone", ["pclass"]), ("state", ["pclass", by_state])):
        eA = effects(v, "puz", sw, t, by, win)
        eC = effects(v, "sub", sw, t, by, win)
        if name == "raw":
            A = apply(base, eA, []) + apply(puz, eA, [])
            C = apply(base, eC, []) + apply(sub, eC, [])
        else:
            fA = fC = None
            if name == "state":
                fA = effects(v, "puz", sw, t, ["pclass"], win)
                fC = effects(v, "sub", sw, t, ["pclass"], win)
            A = apply(base, eA, by, fA) + apply(puz, eA, by, fA)
            C = apply(base, eC, by, fC) + apply(sub, eC, by, fC)
        out[name] = {"A": A, "C": C, "eA": eA, "eC": eC, "fA": fA if name != "raw" else None,
                     "fC": fC if name != "raw" else None}
    by = ["pclass", by_state]
    eA, eC = out["state"]["eA"], out["state"]["eC"]
    fA, fC = out["state"]["fA"], out["state"]["fC"]
    grid = {}
    for c in P.COHORTS:
        grid[c] = {"A": apply(base[base.template == c], eA, by, fA),
                   "C": apply(base[base.template == c], eC, by, fC)
                   + apply(sub[sub.template == c], eC, by, fC)}
    out["grid"] = grid
    out["A_puz"] = apply(puz, eA, by, fA)
    out["C_sub"] = apply(sub, eC, by, fC)
    # joint ramp on the base (phone mix of the base), and its residual against the raw split
    eJ = effects(v, "base", sw, t, ["pclass"], win)
    out["joint"] = apply(base, eJ, ["pclass"])
    eJs = effects(v, "base", sw, t, [], win)
    out["joint_pts"] = float(eJs.iloc[0]) * 100
    out["raw_pts"] = float(out["raw"]["eA"].iloc[0] + out["raw"]["eC"].iloc[0]) * 100
    return out


# ------------------------------------------------------------------ the dated changes (T ask, rung 2)
def page_class(v):
    return np.where(v.edition.values != "", "local", "other")


def dated(v, L, letter, title_col="title_cur", strata=True, weighted=True, win=WIN):
    """Views a month each title gets back from fixing a dated change: the step read on the 28
    days either side of its release, inside each page class, valued on August scored views."""
    _, t = switch_times(L)
    t0 = t[letter]
    x = v[v.scored]
    if letter == "B":
        x = x[x.template.isin(sorted(P.HERO))]
    x = x.assign(pcls=page_class(x))
    aug = x[x.month == 8]
    xs = x if weighted else x.assign(w=1.0)
    pre = xs[(xs.ts >= t0 - win) & (xs.ts < t0)]
    post = xs[(xs.ts >= t0) & (xs.ts < t0 + win)]
    by = ["pcls"] if strata else []
    out = {}
    for ti in P.TITLES:
        e = _cells(post[post[title_col] == ti], by) - _cells(pre[pre[title_col] == ti], by)
        out[ti] = apply(aug[aug.title_cur == ti], e, by)
    return out


def dated_restricted(v, L, letter):
    """Second correct handling of the tag gap: the window kept to days every edition reports."""
    _, t = switch_times(L)
    t0 = t[letter]
    x = v[v.scored]
    if letter == "B":
        x = x[x.template.isin(sorted(P.HERO))]
    gap = (x.day >= pd.Timestamp(P.TAG_GAP[0])) & (x.day <= pd.Timestamp(P.TAG_GAP[1]))
    x = x[~gap]
    pre = x[(x.ts >= t0 - WIN) & (x.ts < t0)]
    post = x[(x.ts >= t0) & (x.ts < t0 + WIN)]
    aug = x[x.month == 8]
    return {ti: float(aug[aug.title_cur == ti].w.sum()
                      * (share(post[post.title_cur == ti]) - share(pre[pre.title_cur == ti])))
            for ti in P.TITLES}


def puzzles_step(v, L):
    sw, t = switch_times(L)
    pre, post = windows(v, "puz", sw, t)
    a = august(v)
    return float(a[a.group == "puz"].w.sum() * (share(post) - share(pre)))


# ------------------------------------------------------------------ image delivery (I ask)
NATIVE = ("CFNetwork", "okhttp")


def view_months(v, by="local", scored=False):
    x = v[v.scored] if scored else v
    if by == "local":
        key = pd.DatetimeIndex(x.local).strftime("%Y-%m")
    else:
        key = pd.DatetimeIndex(x.ts).strftime("%Y-%m")
    return x.groupby(key).w.sum()


def image_delivery(L, v, native=False, hits_only=False, kb_fix=True, scored=False, by="local"):
    """Image requests and kilobytes the CDN served to mobile page views, per mobile page view, by
    month: smartphone rows of browser and app-webview clients over the month's mobile page views."""
    cdn = L["cdn"].copy()
    for col in ["edge_hits", "origin_fills", "bytes_served"]:
        cdn[col] = cdn[col].astype(np.int64)
    cdn = cdn[cdn.device_class == "smartphone"]
    if not native:
        cdn = cdn[~cdn.ua_family.isin(NATIVE)]
    cdn["m"] = cdn.log_date.str[:7]
    req = cdn.edge_hits + (0 if hits_only else cdn.origin_fills)
    b = cdn.bytes_served.astype(float)
    if kb_fix:
        b = np.where(cdn.vendor == "fallback", b * 1000.0, b)
    cdn = cdn.assign(req=req, b=b)
    vm = view_months(v, by, scored)
    out = {}
    for m in range(3, 9):
        name = "2026-%02d" % m
        x = cdn[cdn.m == name]
        out[name] = (float(x.req.sum() / vm[name]), float(x.b.sum() / 1000.0 / vm[name]))
    return out
