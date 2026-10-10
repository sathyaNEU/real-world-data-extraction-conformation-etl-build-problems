"""task129 generator: devices, sessions and page views (the truth behind the beacon export).

Every sampled device is simulated from a January warm-up to 31 August, whether or not the
collector of the day exported it, so the per-view state (first load after a release-train
deploy, or a reload of the cached bundle) is the device's real history."""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

import params as P
import world as Wd

GTYPES = ["anon", "free", "sub", "puz", "tablet"]


def _choice(rng, keys, probs, n):
    p = np.asarray(probs, float)
    return np.asarray(keys)[rng.choice(len(keys), size=n, p=p / p.sum())]


def devices(rng):
    mbc = Wd.models_by_class()
    frames = []
    for g in GTYPES:
        n = P.N_DEV[g]
        title = _choice(rng, P.TITLES, [P.TITLE_SHARE[t] for t in P.TITLES], n)
        if g == "tablet":
            pc = np.array(["tablet"] * n, dtype=object)
        else:
            mix = P.MIX["base" if g in ("anon", "free") else g]
            pc = _choice(rng, ["low", "mid", "high"], mix, n)
        model = np.empty(n, dtype=object)
        for c in np.unique(pc):
            ix = np.flatnonzero(pc == c)
            model[ix] = _choice(rng, mbc[c], np.ones(len(mbc[c])), len(ix))
        edition = np.array([""] * n, dtype=object)
        if g != "puz":
            loc = rng.random(n) < P.LOCAL_READER
            for t in P.TITLES:
                eds = [s for s, v in P.EDITIONS.items() if v[1] == t]
                ix = np.flatnonzero(loc & (title == t))
                edition[ix] = _choice(rng, eds, np.ones(len(eds)), len(ix))
        app = np.zeros(n, bool)
        if g in P.APP_SHARE_ST:
            app = (title == "ST") & (rng.random(n) < P.APP_SHARE_ST[g])
        shape, mean = P.RATE[g]
        rate = rng.gamma(shape, mean / shape, n)
        # collector subsets: every k-th device in an order that balances title, phone class,
        # edition, app and activity, so the two collectors see the same audience mix
        order = np.lexsort((rate, app, edition.astype(str), pc.astype(str), title.astype(str)))
        rank = np.empty(n, int)
        rank[order] = np.arange(n)
        k1 = int(round(1 / P.V1_SHARE[g]))
        v1 = (rank % k1) == 0
        if g == "anon":
            v2 = (rank % P.V2_ANON_KEEP) == 0
        elif g == "tablet":
            v2 = np.zeros(n, bool)
        else:
            v2 = np.ones(n, bool)
        span = len(pd.date_range(P.SIM_START, P.EXTRACT_END))
        start = np.zeros(n, int)
        end = np.full(n, span - 1)
        frames.append(pd.DataFrame({"gtype": g, "home": title, "pclass": pc, "model": model,
                                    "edition": edition, "app": app, "v1": v1, "v2": v2,
                                    "rate": rate, "start": start, "end": end}))
    dev = pd.concat(frames, ignore_index=True)
    n = len(dev)
    keys = set()
    out = []
    while len(out) < n:
        k = "".join(rng.choice(list("0123456789abcdef"), 12))
        if k not in keys:
            keys.add(k)
            out.append(k)
    dev["device_key"] = out
    # accounts: signed-in devices; subscribers, and free accounts (a share of them lapsed subscribers)
    acc = np.array([""] * n, dtype=object)
    signed = dev.gtype.isin(["free", "sub"]).to_numpy()
    ids = rng.choice(np.arange(10_000_000, 99_999_999), size=signed.sum(), replace=False)
    acc[signed] = ["A" + str(x) for x in ids]
    dev["account_key"] = acc
    # subscription start for a few subscriber devices inside the extract (before the main windows)
    sub_start = np.full(n, np.datetime64("NaT"), dtype="datetime64[ns]")
    six = np.flatnonzero(dev.gtype.to_numpy() == "sub")
    lateix = six[:0]
    offs = rng.integers(5, 84, len(lateix))
    sub_start[lateix] = (np.datetime64("2026-02-01") + offs.astype("timedelta64[D]")).astype(
        "datetime64[ns]")
    dev["sub_start_in_window"] = sub_start
    return dev


HOUR_NEWS = np.array([0.6, 0.35, 0.25, 0.2, 0.3, 0.9, 2.6, 4.6, 5.2, 4.3, 3.8, 3.9, 4.6, 4.2,
                      3.8, 3.9, 4.1, 4.4, 4.8, 5.3, 5.9, 5.8, 4.2, 1.9])
HOUR_LOYAL = np.array([0.7, 0.4, 0.3, 0.25, 0.35, 1.2, 4.2, 6.4, 5.6, 4.0, 3.3, 3.3, 4.1, 3.6,
                       3.2, 3.3, 3.6, 4.1, 4.6, 5.0, 5.6, 5.9, 4.5, 2.1])


def sessions(rng, dev):
    days = pd.date_range(P.SIM_START, P.EXTRACT_END)
    nd, n = len(days), len(dev)
    gt = dev.gtype.to_numpy()
    loyal = np.isin(gt, ["sub", "puz"])
    season = np.array([P.SEASON[d.month] for d in days])
    dow_n = np.array([P.DOW_NEWS[d.weekday()] for d in days])
    dow_l = np.array([P.DOW_LOYAL[d.weekday()] for d in days])
    rate = dev.rate.to_numpy()
    start, end = dev.start.to_numpy(), dev.end.to_numpy()
    tablet = gt == "tablet"
    dev_ix, day_ix = [], []
    for j in range(nd):
        lam = rate * season[j] * np.where(loyal, dow_l[j], dow_n[j])
        lam = np.where((j >= start) & (j <= end), lam, 0.0)
        if days[j].date() >= P.FORWARDER_FIX.date():
            lam = np.where(tablet, 0.0, lam)
        k = rng.poisson(lam)
        ix = np.flatnonzero(k)
        dev_ix.append(np.repeat(ix, k[ix]))
        day_ix.append(np.full(k[ix].sum(), j))
    s_dev = np.concatenate(dev_ix)
    s_day = np.concatenate(day_ix)
    ns = len(s_dev)
    prof = np.where(loyal[s_dev], 1, 0)
    hours = np.empty(ns, int)
    for v, h in ((0, HOUR_NEWS), (1, HOUR_LOYAL)):
        ix = np.flatnonzero(prof == v)
        hours[ix] = rng.choice(24, size=len(ix), p=h / h.sum())
    secs = hours * 3600 + rng.integers(0, 3600, ns)
    base = days.values.astype("datetime64[s]")[s_day]
    t_local = base + secs.astype("timedelta64[s]")
    order = np.lexsort((t_local, s_dev))
    return pd.DataFrame({"dev": s_dev[order], "t_local": t_local[order]})


def views(rng, dev, ses):
    """Expand sessions to page views with template, page, title and context columns."""
    gt = dev.gtype.to_numpy()
    s_dev = ses.dev.to_numpy()
    ns = len(s_dev)
    g_s = gt[s_dev]
    m_extra = np.array([P.EXTRA_VIEWS[g] for g in g_s])
    n_main = rng.geometric(1.0 / (1.0 + m_extra))
    side = {}
    is_sub = g_s == "sub"
    for tpl, r in P.SUB_SIDE_VIEWS.items():
        side[tpl] = np.where(is_sub, rng.poisson(r * n_main), 0)
    n_side = sum(side.values())
    n_tot = n_main + n_side
    v_ses = np.repeat(np.arange(ns), n_tot)
    pos = np.arange(len(v_ses)) - np.repeat(np.cumsum(n_tot) - n_tot, n_tot)
    nv = len(v_ses)
    # side views sit after the landing view: mark the last n_side positions, then shuffle them
    # into positions 1.. of their session
    kind = np.empty(nv, dtype=object)
    is_main = pos < np.repeat(n_main, n_tot)
    kind[is_main] = "main"
    lab_ses = np.concatenate([np.repeat(np.arange(ns), side[t]) for t in P.SUB_SIDE_VIEWS])
    lab_tpl = np.concatenate([np.full(side[t].sum(), t, dtype=object) for t in P.SUB_SIDE_VIEWS])
    o = np.argsort(lab_ses, kind="stable")
    kind[~is_main] = lab_tpl[o]
    # random order of positions 1.. within sessions that carry side views
    key = rng.random(nv)
    key[pos == 0] = -1.0
    order = np.lexsort((key, v_ses))
    kind = kind[order]
    v_dev = s_dev[v_ses]
    g_v = gt[v_dev]
    landing = pos == 0
    # templates
    tpl = np.empty(nv, dtype=object)
    for grp, keyg in (("anon", "anon"), ("free", "anon"), ("tablet", "anon"), ("sub", "sub")):
        m = (g_v == grp) & (kind == "main")
        for lab, dist in ((True, P.LAND[keyg]), (False, P.BROWSE[keyg])):
            ix = np.flatnonzero(m & (landing == lab))
            tpl[ix] = _choice(rng, list(dist), list(dist.values()), len(ix))
    tpl[g_v == "puz"] = P.PUZZLE_T
    side_ix = np.flatnonzero(kind != "main")
    tpl[side_ix] = kind[side_ix]
    # times: session start plus cumulative gaps
    gaps = (15 + rng.exponential(85, nv)).astype(int)
    gaps[landing] = 0
    cum = np.cumsum(gaps)
    cum0 = cum - np.repeat(cum[np.cumsum(n_tot) - n_tot], n_tot)
    t_local = ses.t_local.to_numpy()[v_ses] + cum0.astype("timedelta64[s]")
    V = pd.DataFrame({"dev": v_dev, "ses": v_ses, "pos": pos, "landing": landing,
                      "template": tpl, "t_local": t_local})
    # session thinning by audience and landing template, on its own stream
    u = np.random.default_rng([P.SEED, 77]).random(ns)
    aud = np.where(np.isin(g_s, ["anon", "free", "tablet"]), "base", g_s)
    land_tpl = tpl[landing]
    land_ses = v_ses[landing]
    keep_p = np.ones(ns)
    for a_, d_ in P.KEEP.items():
        for t_, k_ in d_.items():
            m = (aud[land_ses] == a_) & (land_tpl == t_)
            keep_p[land_ses[m]] = k_
    keep_s = u < keep_p
    return V[keep_s[v_ses]].reset_index(drop=True)
