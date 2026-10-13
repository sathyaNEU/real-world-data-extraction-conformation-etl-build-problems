"""The world: every page load's paint at Brolga Media's six properties in November 2026 (the beacons a sampled load
sends), the squad's eleven past engagements as the group's RUM saw them, and the ask paths' records. The paint parts
are drawn per load; the playbook's real effect (the image's load delay settles at the CDN connection, its load time
scales with the bytes) is applied only inside the engagements' after windows and never shipped as a figure."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K

DEVICES = ("mobile", "desktop", "tablet")
DEVICE_NET = {"mobile": 1.0, "desktop": 0.80, "tablet": 0.95}   # network-bound parts scale with the device's link
# Sydney hour-of-day weights for page loads (news and sport peak at breakfast and evening)
HOUR_W = np.array([0.9, 0.6, 0.4, 0.35, 0.4, 0.8, 1.9, 3.3, 4.2, 4.0, 3.7, 3.6, 3.9, 3.6, 3.4, 3.4, 3.6, 3.9, 4.3,
                   4.8, 5.2, 4.8, 3.4, 1.9])
HOUR_W = HOUR_W / HOUR_W.sum()
OTHER_KIND = {"news": (0.55, 0.20, 0.15, 0.10), "sport": (0.35, 0.25, 0.15, 0.25), "home": (0.45, 0.30, 0.20, 0.05),
              "personal finance": (0.75, 0.10, 0.15, 0.0), "travel": (0.35, 0.35, 0.20, 0.10),
              "food": (0.40, 0.30, 0.25, 0.05)}   # text, agency image, ad creative, video poster
COLUMNS = ["origin", "page_path", "device", "navigation_type", "fired_at_utc", "lcp_ms", "lcp_element", "lcp_url",
           "ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms"]


def _hours(start=None, end=None):
    out, t = [], start or K.MONTH_START_UTC
    while t < (end or K.MONTH_END_UTC):
        out.append(t)
        t += dt.timedelta(hours=1)
    return out


def edge_hours():
    """The extract's UTC days outside the Sydney month: 31 October before 13:00 UTC and 30 November from 13:00 UTC."""
    return _hours(K.EXTRACT_START_UTC, K.MONTH_START_UTC) + _hours(K.MONTH_END_UTC, K.EXTRACT_END_UTC)


def day_factor(kind: str, t: dt.datetime) -> float:
    """Page loads on the Sydney day of UTC hour t against the November average day, for a property of this kind."""
    w = DOW[kind]
    nov = [w[(dt.date(2026, 11, 1) + dt.timedelta(days=k)).weekday()] for k in range(30)]
    return w[K.sydney(t).date().weekday()] / (sum(nov) / 30.0)


def expected_loads(p, hours) -> np.ndarray:
    """A property's page loads (navigations reporting LCP) expected in each UTC hour."""
    per_day = p["loads"] * 1e6 / 30.0
    return np.array([per_day * HOUR_W[K.sydney(t).hour] * day_factor(p["kind"], t) for t in hours])


SECTIONS = {"news": ("news", "politics", "business", "world", "national", "opinion"),
            "sport": ("afl", "nrl", "cricket", "football", "tennis", "racing"),
            "home": ("renovate", "interiors", "garden", "cleaning"),
            "personal finance": ("super", "tax", "banking", "investing", "property", "budgeting"),
            "travel": ("destinations", "guides", "deals", "flights", "cruises", "getaways"),
            "food": ("recipes", "dinner", "quick-meals", "healthy", "baking", "game-day")}
# sections the group moved between properties on 10 March 2025, pages and images to the receiving property's origin
# and image host: receiving property -> (its section, the property the pages came from, their old section)
MOVED = {"ledger": ("property", "hearth", "real-estate"), "trailhead": ("getaways", "tideline", "travel"),
         "pantry": ("game-day", "matchday", "food")}
MOVE_DATE = dt.date(2025, 3, 10)
PAGES = {"news": 9000, "sport": 6000, "home": 4000, "personal finance": 3000, "travel": 3500, "food": 5000}
# page loads by Sydney day of the week (Monday first), each kind's own week
DOW = {"news": (1.05, 1.04, 1.03, 1.02, 0.99, 0.88, 0.99), "sport": (0.95, 0.93, 0.94, 0.97, 1.02, 1.12, 1.07),
       "home": (0.97, 0.97, 0.98, 0.99, 0.96, 1.05, 1.08), "personal finance": (1.08, 1.07, 1.06, 1.04, 0.98, 0.85, 0.92),
       "travel": (0.99, 0.98, 0.98, 1.00, 1.01, 1.02, 1.02), "food": (0.96, 0.95, 0.96, 0.98, 1.02, 1.04, 1.09)}
# the section already moved to the group image CDN in 2025, and the date before which a property's images went to
# its old media host (the legacy alias)
CDN_SECTION = {"tideline": "opinion", "matchday": "racing", "pantry": "baking"}
ALIAS_BEFORE = {"hearth": dt.date(2023, 7, 1), "trailhead": dt.date(2022, 12, 1)}


_CATALOGUES = {}


def catalogue(p):
    """A property's pages: section, id, publication date and hero (its own image, an agency photo or a video
    poster), each hero's URL as the page serves it. News and sport pages are mostly recent; the others are
    evergreen. Popularity is Zipf-like."""
    if p["code"] in _CATALOGUES:
        return _CATALOGUES[p["code"]]
    r = K.stream("pages", p["code"])
    n = PAGES[p["kind"]]
    secs = SECTIONS[p["kind"]]
    sec = np.array(secs)[r.integers(0, len(secs), n)]
    ids = r.choice(np.arange(100000, 1000000), n, replace=False)
    end = dt.date(2026, 11, 30)
    if p["kind"] in ("news", "sport"):
        age = np.where(r.random(n) < 0.7, r.integers(0, 120, n), r.integers(120, 2900, n))
    else:
        age = r.integers(0, 3200, n)
    pub = np.array([end - dt.timedelta(days=int(a)) for a in age])
    hero = np.array(["own", "agency", "video"])[r.choice(3, n, p=(0.70, 0.22, 0.08))]
    pop = 1.0 / (r.permutation(n) + 12.0) ** 1.05
    host = np.full(n, "own", dtype=object)
    if p["code"] in ALIAS_BEFORE:
        host[pub < ALIAS_BEFORE[p["code"]]] = "alias"
    if p["code"] in CDN_SECTION:
        host[sec == CDN_SECTION[p["code"]]] = "cdn"
    hx = np.char.mod("%08x", r.integers(0, 2**32, n))
    ext = np.array(["jpg", "jpg", "jpg", "png"])[r.integers(0, 4, n)]
    ym = np.array([d.strftime("%Y/%m") for d in pub])
    w, h = p["hero"]
    own_host = np.where(host == "alias", p["alias"][0] if p["alias"] else "", p["img"]).astype(str)
    url_own = np.char.add(np.char.add(np.char.add("https://", own_host), "/i/%dx%d/" % (w, h)),
                          np.char.add(np.char.add(ym, "/"), np.char.add(np.char.add(hx, "."), ext)))
    url_cdn = np.char.add("https://%s/%s/i/%dx%d/" % (K.CDN_HOST, p["code"], w, h),
                          np.char.add(np.char.add(ym, "/"), np.char.add(np.char.add(hx, "."), ext)))
    agency = np.array(K.AGENCY_HOSTS)[np.array([int(v[:2], 16) % len(K.AGENCY_HOSTS) for v in hx])]
    url_ag = np.char.add(np.char.add("https://", agency), np.char.add("/a/", np.char.add(hx, ".jpg")))
    url_vid = np.char.add("https://%s/poster/" % K.VIDEO_HOST, np.char.add(hx, ".jpg"))
    hero_url = np.where(hero == "own", np.where(host == "cdn", url_cdn, url_own),
                        np.where(hero == "agency", url_ag, url_vid))
    path = np.char.add(np.char.add("/", sec), np.char.add("/", ids.astype(str)))
    out = dict(sec=sec, ids=ids, pub=pub, hero=hero, pop=pop, host=host, hx=hx, ext=ext, hero_url=hero_url,
               path=path)
    _CATALOGUES[p["code"]] = out
    return out


def _pick(r, cat, mask, k):
    """k page indices drawn by popularity from the pages where mask holds."""
    idx = np.flatnonzero(mask)
    w = cat["pop"][idx]
    return idx[r.choice(len(idx), k, p=w / w.sum())]


def _property_beacons(p, hours, key):
    """One property's beacons for the given UTC hours: navigations reporting LCP, and back-forward cache restores,
    which report none. Each hour's beacon count is its expected loads times the sampling rate in force (rates change
    on the hour). Prerendered loads are timed from activation."""
    base = np.array([np.datetime64(t, "s") for t in hours])
    r = K.stream(key, p["code"])
    lam = expected_loads(p, hours) * np.array([K.rate_at(p["code"], t) for t in hours])
    n_h, x_h = r.poisson(lam), r.poisson(lam * 0.075)
    n, x = int(n_h.sum()), int(x_h.sum())
    m = n + x
    fired = np.concatenate([np.repeat(base, n_h), np.repeat(base, x_h)]) + \
        r.integers(0, 3600, m).astype("timedelta64[s]")
    restore = np.r_[np.zeros(n, bool), np.ones(x, bool)]
    device = np.array(DEVICES)[r.choice(3, m, p=p["devices"])]
    net = np.where(device == "mobile", 1.0, np.where(device == "desktop", 0.80, 0.95))
    nav = np.array(["navigate", "reload", "prerender"])[r.choice(3, m, p=[0.92, 0.04, 0.04])]
    own = r.random(m) < p["own"]
    (t0, st), (d0, sd), (u0, su), (q0, sq) = p["parts"]
    z = r.normal(0.0, 1.0, (4, m))
    # where the property's own hero image is served from
    u = r.random(m)
    a_share = p["alias"][2] if p["alias"] else 0.0
    how = np.where(u < a_share, "alias", np.where(u < a_share + p["cdn_share"], "cdn", "own"))
    # loads whose largest element is something else: text, an agency or ad image, a video poster
    which = r.choice(4, m, p=OTHER_KIND[p["kind"]])
    total = p["other"][0] * (0.9 + 0.1 * net) * np.exp(p["other"][1] * r.normal(0.0, 1.0, m))
    f_t, f_d, f_u = r.uniform(0.22, 0.38, m), r.uniform(0.12, 0.30, m), r.uniform(0.15, 0.30, m)
    o_ttfb = total * f_t
    o_delay = np.where(which == 0, 0.0, total * f_d)
    o_load = np.where(which == 0, 0.0, total * f_u)
    o_render = np.maximum(total - o_ttfb - o_delay - o_load, 30.0)
    ttfb = np.where(own, t0 * net * np.exp(st * z[0]), o_ttfb)
    delay = np.where(own, d0 * np.exp(sd * z[1]), o_delay)
    load = np.where(own, u0 * net * np.exp(su * z[2]), o_load)
    render = np.where(own, q0 * np.exp(sq * z[3]), o_render)
    # a prerendered page is timed from its activation: the page and its image were fetched beforehand
    pre = (nav == "prerender") & ~restore
    rp = K.stream(key, "prerender", p["code"])
    act = 110.0 * np.exp(0.5 * rp.normal(0.0, 1.0, m))
    ttfb, delay, load = np.where(pre, 0.0, ttfb), np.where(pre, 0.0, delay), np.where(pre, 0.0, load)
    render = np.where(pre, act, render)
    parts = np.rint(np.vstack([ttfb, delay, load, render])).astype(np.int64)
    parts[3] += (parts.sum(0) == K.GOOD_MS)          # nothing sits on the line
    lcp = parts.sum(0)
    # the page each load opened, and the URL of its largest element
    cat = catalogue(p)
    rq = K.stream(key, "pick", p["code"])
    page = np.zeros(m, dtype=np.int64)
    own_hero = cat["hero"] == "own"
    for h in ("own", "alias", "cdn"):
        sel = own & (how == h)
        if sel.any():
            page[sel] = _pick(rq, cat, own_hero & (cat["host"] == h), int(sel.sum()))
    for k, kind in ((1, "agency"), (3, "video")):
        sel = ~own & (which == k)
        if sel.any():
            page[sel] = _pick(rq, cat, cat["hero"] == kind, int(sel.sum()))
    sel = ~own & ((which == 0) | (which == 2))
    if sel.any():
        page[sel] = _pick(rq, cat, np.ones(len(cat["pop"]), bool), int(sel.sum()))
    url = np.where(own, cat["hero_url"][page],
                   np.where(which == 0, "", np.where(which == 2, "", cat["hero_url"][page])))
    creative = np.char.mod("%08x", rq.integers(0, 2**32, m))
    url_ad = np.char.add("https://%s/a/" % K.AD_HOSTS[0], np.char.add(creative, ".jpg"))
    url = np.where(~own & (which == 2), url_ad, url)
    text_el = np.array(["H1", "P", "DIV"])[rq.choice(3, m, p=[0.6, 0.25, 0.15])]
    element = np.where(own, "IMG", np.where(which == 0, text_el, np.where(which == 3, "VIDEO", "IMG")))
    path = cat["path"][page]
    df = pd.DataFrame({
        "origin": p["origin"], "page_path": path,
        "device": device, "navigation_type": np.where(restore, "back_forward", nav),
        "fired_at_utc": pd.to_datetime(fired), "lcp_ms": pd.array(np.where(restore, -1, lcp), dtype="Int64"),
        "lcp_element": np.where(restore, "", element), "lcp_url": np.where(restore, "", url),
        "ttfb_ms": pd.array(np.where(restore, -1, parts[0]), dtype="Int64"),
        "load_delay_ms": pd.array(np.where(restore, -1, parts[1]), dtype="Int64"),
        "load_time_ms": pd.array(np.where(restore, -1, parts[2]), dtype="Int64"),
        "render_delay_ms": pd.array(np.where(restore, -1, parts[3]), dtype="Int64")})
    for c in ("lcp_ms", "ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms"):
        df.loc[restore, c] = pd.NA
    df = df.sort_values(["fired_at_utc", "page_path"], kind="mergesort").reset_index(drop=True)
    ids = [_hexid(key, p["code"], i) for i in range(len(df))]
    df.insert(0, "beacon_id", ids)
    return df


def _hexid(*keys) -> str:
    import hashlib
    return hashlib.blake2b(("%d|" % K.SEED + "|".join(str(k) for k in keys)).encode(), digest_size=8).hexdigest()


def november_beacons(edges=True) -> pd.DataFrame:
    """Every beacon in the extract: the Sydney month's (the world the call is counted on), and with edges the hours
    of the extract's whole UTC days outside it. A small share of beacons reach the collector twice."""
    frames = []
    for p in K.PROPERTIES:
        frames.append(_property_beacons(p, _hours(), "beacons"))
        if edges:
            frames.append(_property_beacons(p, edge_hours(), "edge"))
    out = pd.concat(frames, ignore_index=True)
    if edges:
        r = K.stream("resent")
        twice = out.iloc[np.flatnonzero(r.random(len(out)) < 0.004)]
        out = pd.concat([out, twice], ignore_index=True)
    return out.sort_values(["fired_at_utc", "beacon_id"], kind="mergesort").reset_index(drop=True)


def engagement_windows():
    """Each engagement's before window (28 days to the day before the change shipped) and after window (28 days
    from a week after it). The change ships on the Monday 28 days after the before window opens."""
    out = []
    for e in K.ENGAGEMENTS:
        start = e[3]
        ship = start + dt.timedelta(days=28)
        out.append((e[0], start, ship - dt.timedelta(days=1), ship, ship + dt.timedelta(days=7),
                    ship + dt.timedelta(days=34)))
    return out


def _sydney_offset(day):
    """Hours Sydney runs ahead of UTC on a date: daylight time from the first Sunday of October to the first Sunday
    of April."""
    def first_sunday(y, mth):
        d = dt.date(y, mth, 1)
        return d + dt.timedelta(days=(6 - d.weekday()) % 7)
    on, off = first_sunday(day.year, 10), first_sunday(day.year, 4)
    return 11 if (day >= on or day < off) else 10


def _spread(r, device):
    """Standard normal scores spread evenly over each device's loads (one draw in each of n equal-probability
    strata, in random order), so a window's quantiles follow the part's distribution closely."""
    from scipy.stats import norm
    z = np.empty(len(device))
    for d in DEVICES:
        idx = np.flatnonzero(device == d)
        k = len(idx)
        if k:
            z[idx] = norm.ppf((r.permutation(k) + r.random(k)) / k)
    return z


def engagement_beacons() -> pd.DataFrame:
    """RUM beacons from the engaged article pages in each engagement's review windows, the loads whose LCP element
    was the page's hero image. Before the change the hero sits on the site's own image host; after it, on the group
    image CDN as AVIF at the slot size, preloaded and never lazy-loaded."""
    frames = []
    for (eid, site, origin, start, d_b, u_b, t_b, q_b, lv_off, ratio), (_, b0, b1, ship, a0, a1) in \
            zip(K.ENGAGEMENTS, engagement_windows()):
        r = K.stream("engagement", eid)
        n_pages = 2400
        ids = r.choice(np.arange(100000, 1000000), n_pages, replace=False)
        pub = np.array([start - dt.timedelta(days=int(a)) for a in r.integers(1, 1500, n_pages)])
        hx = np.char.mod("%08x", r.integers(0, 2**32, n_pages))
        pop = 1.0 / (r.permutation(n_pages) + 8.0) ** 1.1
        pop = pop / pop.sum()
        code = origin.split(".")[0]
        n = K.ENGAGEMENT_BEACONS + int(r.integers(-120, 121))
        for window, d0, d1 in (("before", b0, b1), ("after", a0, a1)):
            days = (d1 - d0).days + 1
            k_dev = [int(round(n * 0.24)), int(round(n * 0.04))]
            device = np.array(DEVICES)[r.permutation(np.r_[np.zeros(n - sum(k_dev), int), np.ones(k_dev[0], int),
                                                         np.full(k_dev[1], 2)])]
            net = np.where(device == "mobile", 1.0, np.where(device == "desktop", 0.80, 0.95))
            day = [d0 + dt.timedelta(days=int(k)) for k in r.integers(0, days, n)]
            secs = r.integers(0, 86400, n)
            fired = [dt.datetime.combine(dd, dt.time()) + dt.timedelta(seconds=int(s)) -
                     dt.timedelta(hours=_sydney_offset(dd)) for dd, s in zip(day, secs)]
            page = r.choice(n_pages, n, p=pop)
            ttfb = t_b * net * np.exp(0.40 * r.normal(size=n))
            render = q_b * np.exp(0.45 * r.normal(size=n))
            ym = [pub[k].strftime("%Y/%m") for k in page]
            z_load = _spread(r, device)
            if window == "before":
                delay = d_b * np.exp(0.60 * r.normal(size=n))
                load = u_b * net * np.exp(0.35 * z_load)
                urls = ["https://images.%s/i/1200x675/%s/%s.jpg" % (origin, y, hx[k]) for y, k in zip(ym, page)]
            else:
                delay = K.LEVEL_MS + lv_off + K.LEVEL_SD_MS * _spread(r, device)
                load = u_b * ratio * net * np.exp(0.35 * z_load)
                urls = ["https://%s/%s/i/1200x675/%s/%s.avif" % (K.CDN_HOST, code, y, hx[k]) for y, k in zip(ym, page)]
            parts = np.rint(np.vstack([ttfb, delay, load, render])).astype(np.int64)
            frames.append(pd.DataFrame({
                "origin": origin, "page_path": ["/article/%d" % ids[k] for k in page],
                "device": device, "navigation_type": "navigate", "fired_at_utc": pd.to_datetime(fired),
                "lcp_ms": parts.sum(0), "lcp_element": "IMG", "lcp_url": urls, "ttfb_ms": parts[0],
                "load_delay_ms": parts[1], "load_time_ms": parts[2], "render_delay_ms": parts[3],
                "engagement": eid}))
    df = pd.concat(frames, ignore_index=True).sort_values(["engagement", "fired_at_utc", "page_path"],
                                                          kind="mergesort").reset_index(drop=True)
    df.insert(0, "beacon_id", ["SQ-%06d" % (i + 1) for i in range(len(df))])
    return df


def crux(nov: pd.DataFrame) -> pd.DataFrame:
    """The public Chrome UX Report's November rows for the six origins: the share of LCP in each band and the 75th
    percentile, by form factor. Chrome-only and origin-wide, so it sits near the group's RUM without matching it."""
    r = K.stream("crux")
    rows = []
    month = nov[(nov.fired_at_utc >= K.MONTH_START_UTC) & (nov.fired_at_utc < K.MONTH_END_UTC) &
                nov.lcp_ms.notna()].drop_duplicates("beacon_id")
    for p in K.PROPERTIES:
        g = month[month.origin == p["origin"]]
        for dev, ff in (("mobile", "phone"), ("desktop", "desktop"), ("tablet", "tablet")):
            x = g[g.device == dev].lcp_ms.astype(float).to_numpy()
            good, poor = (x <= 2500).mean(), (x > 4000).mean()
            jg, jp = r.normal(0.012, 0.008), r.normal(-0.006, 0.006)
            good, poor = min(max(good + jg, 0.0), 1.0), min(max(poor + jp, 0.0), 1.0)
            ni = max(1.0 - good - poor, 0.0)
            p75 = float(np.quantile(x, 0.75)) * (1.0 + r.normal(-0.02, 0.015))
            rows.append((202611, "https://" + p["origin"], ff, round(good, 4), round(ni, 4), round(poor, 4),
                         int(round(p75 / 100.0)) * 100))
    return pd.DataFrame(rows, columns=["yyyymm", "origin", "form_factor", "lcp_good", "lcp_ni", "lcp_poor",
                                       "p75_lcp"])


def analytics() -> pd.DataFrame:
    """The analytics suite's daily page views by property and section (Sydney dates): every view the tag records,
    including the virtual views that infinite scroll and photo galleries send."""
    rows = []
    for p in K.PROPERTIES:
        r = K.stream("analytics", p["code"])
        secs = SECTIONS[p["kind"]]
        share = r.dirichlet(np.full(len(secs), 6.0))
        virt = {"news": 0.21, "sport": 0.17, "home": 0.26, "personal finance": 0.06, "travel": 0.31,
                "food": 0.12}[p["kind"]]
        for k in range(30):
            day = dt.date(2026, 11, 1) + dt.timedelta(days=k)
            t = dt.datetime.combine(day, dt.time(12)) - dt.timedelta(hours=K.UTC_OFFSET)
            loads = p["loads"] * 1e6 / 30.0 * day_factor(p["kind"], t) * 1.075
            for s, f in zip(secs, share):
                pv = int(r.poisson(loads * f * (1.0 + virt)))
                rows.append((day.isoformat(), p["name"], s, pv, int(round(pv / (1.9 + 0.4 * r.random())))))
    return pd.DataFrame(rows, columns=["date", "property", "section", "pageviews", "sessions"])


def build():
    return dict(nov=november_beacons(), eng=engagement_beacons())
