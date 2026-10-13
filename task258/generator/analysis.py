"""Every rung of the main call and both asks, computed from the pack as shipped (load.py). Counts are page loads a
month: each beacon stands for 1 / the sampling rate in force for its origin when its page load started."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K
import load as L

GOOD = K.GOOD_MS
NAMES = [p["name"] for p in K.PROPERTIES]
MONTH = (np.datetime64(K.MONTH_START_UTC), np.datetime64(K.MONTH_END_UTC))


def sydney_dates(ts: pd.Series) -> pd.Series:
    return ts.dt.tz_localize("UTC").dt.tz_convert("Australia/Sydney").dt.date


def page_loads(target, month=MONTH, dedupe=True, weights=None):
    """November's page loads in Sydney time: navigations reporting LCP, one row per beacon id, with the property,
    the weight and whether the LCP element is an image the property serves itself."""
    df = L.beacons(target)
    if dedupe:
        df = df.drop_duplicates("beacon_id")
    t = df.fired_at_utc.to_numpy()
    df = df[(t >= month[0]) & (t < month[1]) & df.lcp_ms.notna()].copy()
    df["prop"] = df.origin.map(L.origins(target))
    df["weight"] = L.weights(df, L.sampling(target)) if weights is None else weights(df)
    df["own"] = own_image(df, L.hosts(target))
    return df


def own_image(df, hosts) -> np.ndarray:
    url = df.lcp_url.fillna("").to_numpy().astype(str)
    el = df.lcp_element.fillna("").to_numpy()
    prop = df.prop.to_numpy()
    out = np.zeros(len(df), bool)
    for name, (own_hosts, prefix) in hosts.items():
        m = prop == name
        hit = np.zeros(m.sum(), bool)
        for h in own_hosts:
            hit |= np.char.startswith(url[m], "https://%s/" % h)
        hit |= np.char.startswith(url[m], "https://%s%s" % (K.CDN_HOST, prefix))
        out[m] = hit
    return out & (el == "IMG")


def engagement_frame(target, clock="sydney"):
    """The review extract with each beacon's window: before (from the before window's first day to its last) or
    after (the after window), by Sydney date (clock='utc' reads the windows on UTC dates, 'ship' splits at the ship
    date and drops the week after it)."""
    e = L.engagement_beacons(target)
    win = L.change_log(target)
    if clock == "sydney":
        day = sydney_dates(e.fired_at_utc)
    else:
        day = e.fired_at_utc.dt.date
    tag = []
    for eid, d in zip(e.engagement, day):
        b0, b1, ship, a0, a1 = win[eid]
        if clock == "ship":
            tag.append("before" if d < ship else "after" if d >= a0 else "")
        else:
            tag.append("before" if b0 <= d <= b1 else "after" if a0 <= d <= a1 else "")
    e["window"] = tag
    return e[e.window != ""]


def effect(e: pd.DataFrame) -> dict:
    """The playbook as the engagements' beacons record it: each part's median before and after, pooled and by
    engagement; the level the image's load delay settled at; the load time's ratio of medians."""
    parts = ("ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms", "lcp_ms")
    pooled = {w: {c: float(e[e.window == w][c].median()) for c in parts} for w in ("before", "after")}
    by = {eid: {w: {c: float(g[g.window == w][c].median()) for c in parts} for w in ("before", "after")}
          for eid, g in e.groupby("engagement")}
    return dict(pooled=pooled, by=by, level=pooled["after"]["load_delay_ms"],
                r_delay=pooled["after"]["load_delay_ms"] / pooled["before"]["load_delay_ms"],
                r_load=pooled["after"]["load_time_ms"] / pooled["before"]["load_time_ms"],
                r_whole=pooled["after"]["lcp_ms"] / pooled["before"]["lcp_ms"],
                shift=pooled["before"]["load_delay_ms"] - pooled["after"]["load_delay_ms"])


def rungs(nov: pd.DataFrame, eff: dict, level=None, r_load=None) -> pd.DataFrame:
    """Page loads a month per property under every rung."""
    lv = eff["level"] if level is None else level
    ru = eff["r_load"] if r_load is None else r_load
    t, d, u, q = nov.ttfb_ms, nov.load_delay_ms, nov.load_time_ms, nov.render_delay_ms
    slow = nov.lcp_ms > GOOD
    reach = slow & nov.own
    cols = {
        "slow_all": slow,
        "R1_reach": reach,
        "R2_parts": reach & (t + eff["r_delay"] * d + ru * u + q <= GOOD),
        "R2_whole": reach & (eff["r_whole"] * nov.lcp_ms <= GOOD),
        "R3_zero": reach & (t + ru * u + q <= GOOD),
        "shift": reach & (t + np.maximum(d - eff["shift"], 0) + ru * u + q <= GOOD),
        "golden": reach & (t + lv + ru * u + q <= GOOD),
        "pushed_out": nov.own & ~slow & (t + lv + ru * u + q > GOOD),
        "good_now": ~slow,
        "loads": pd.Series(True, index=nov.index),
        "own_loads": nov.own,
    }
    out = pd.DataFrame({k: (v * nov.weight).groupby(nov.prop).sum() for k, v in cols.items()})
    return out.reindex(NAMES)


def winner(col: pd.Series):
    s = col.sort_values(ascending=False)
    return s.index[0], float(s.iloc[0]), s.index[1], float(s.iloc[0] / s.iloc[1])


def egress(target, month_utc=True, with_legacy=True, statuses=(200,), hero_only=True):
    """Hero-image requests answered with the image in November (Sydney time) and their egress at the AVIF size of
    the property's hero slot. month_utc=False reads the UTC month; with_legacy=False leaves out the old media
    server's log; statuses=(200, 304) counts revalidations; hero_only=False counts every slot at the hero size."""
    img, leg, av = L.image_logs(target), L.legacy_log(target), L.avif(target)
    hosts = L.hosts(target)
    if month_utc:
        t = img.hour_utc.to_numpy()
        img = img[(t >= MONTH[0]) & (t < MONTH[1])]
        lt = leg.log_hour.dt.tz_convert("UTC").dt.tz_localize(None).to_numpy()
        leg = leg[(lt >= MONTH[0]) & (lt < MONTH[1])]
    else:
        img = img[img.hour_utc.dt.month == 11]
        leg = leg[leg.log_hour.dt.tz_localize(None).dt.month == 11]
    out = {}
    for name in NAMES:
        own_hosts, prefix = hosts[name]
        w, h, size = av[(name, "hero")]
        hero_dir = "/i/%dx%d/" % (w, h)
        m = img.host.isin(own_hosts) & img.status.isin(statuses)
        c = (img.host == K.CDN_HOST) & img.path_prefix.str.startswith(prefix) & img.status.isin(statuses)
        if hero_only:
            m &= img.path_prefix == hero_dir
            c &= img.path_prefix == prefix.rstrip("/") + hero_dir
        req = int(img[m].requests.sum() + img[c].requests.sum())
        if with_legacy:
            lm = leg.vhost.isin(own_hosts) & leg.code.isin(statuses)
            if hero_only:
                lm &= leg.uri_dir == hero_dir
            req += int(leg[lm].hits.sum())
        out[name] = dict(requests=req, gb=req * size / 1e9)
    rate = L.cdn_rate(target)
    for v in out.values():
        v["aud"] = v["gb"] * rate
    return out


def hero_images(target, how="legacy"):
    """Live hero images per property in the DAM export, each on the property whose page carried it at the latest
    crawl. how: 'legacy' folds each library record into the DAM record that names it as legacy_id (the answer);
    'ids' counts distinct asset ids; 'rows' counts rows; 'content' counts distinct file name, pixel size and upload
    time; 'all' ignores the crawl (every asset in the collection); 'property' files each asset under the export's
    property column."""
    d = L.dam(target)
    org = L.origins(target)
    d["on"] = d.last_used_page.str.split("/").str[2].map(org)
    key = "property" if how == "property" else "on"
    if how != "all":
        d = d[d.last_used_on == d.last_used_on.max()]
    if how == "rows":
        return d.groupby(key).size().reindex(NAMES).astype(int).to_dict()
    if how == "content":
        o = d[d.rendition == "original"]
        return o.drop_duplicates([key, "file_name", "width_px", "height_px", "uploaded_utc"]) \
            .groupby(key).size().reindex(NAMES).astype(int).to_dict()
    ids = d.drop_duplicates(["asset_id"])
    if how in ("legacy", "all", "property"):
        ids = ids[~ids.asset_id.isin(set(d.legacy_id.dropna()))]
    return ids.groupby(key).size().reindex(NAMES).astype(int).to_dict()


def round_to(x, unit):
    return int(np.floor(x / unit + 0.5) * unit)
