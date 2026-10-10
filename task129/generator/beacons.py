"""task129 generator: from simulated views to the beacon export.

Clocks, the release-train state, audience groups, the over-line outcome (allocated
systematically inside each stratum so every contiguous window carries its stratum's share to
within one view), the context columns and the collector rules that decide what was exported."""
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd

import params as P
import world as Wd


def to_utc(local_naive):
    s = pd.DatetimeIndex(local_naive).tz_localize(P.TZ, nonexistent="shift_forward",
                                                  ambiguous="NaT")
    return s.tz_convert("UTC").tz_localize(None).values.astype("datetime64[s]")


def deploy_table(rng):
    dep = Wd.deploys(rng)
    loc = np.array([np.datetime64(t, "s") for t, _ in dep])
    utc = to_utc(loc)
    tags = np.array([g for _, g in dep], dtype=object)
    return pd.DataFrame({"local": loc, "utc": utc, "tag": tags})


def change_times(dep):
    """UTC switch-on time of each dated change and each cohort, read off the deploy table."""
    def at(d):
        m = dep.local.values.astype("datetime64[D]") == np.datetime64(d)
        assert m.sum() == 1, d
        return dep.utc.values[m][0]
    ct = {k: at(d) for k, d in P.DATED.items()}
    ct["PUZ"] = at(P.PUZZLE_AD_SWITCH)
    ct["SUB"] = at(P.SUB_FRONTEND)
    for c, d in P.COHORT_SWITCH.items():
        ct["COH:" + c] = at(d)
    return ct


def annotate(rng, dev, V, dep):
    """Clock, quiet window, state, title, page, context columns."""
    V = V.copy()
    V["ts"] = to_utc(V.t_local.values)
    # no view of any device within ten minutes of a deploy
    du = dep.utc.values
    k = np.searchsorted(du, V.ts.values, side="right") - 1
    prev_gap = V.ts.values - du[np.clip(k, 0, None)]
    nxt = np.clip(k + 1, 0, len(du) - 1)
    next_gap = du[nxt] - V.ts.values
    q = np.timedelta64(P.DEPLOY_QUIET_MIN * 60, "s")
    quiet = ((k >= 0) & (prev_gap < q)) | ((k + 1 < len(du)) & (next_gap < q))
    V = V[~quiet].reset_index(drop=True)
    V = V.sort_values(["dev", "ts"], kind="stable").reset_index(drop=True)
    k = np.searchsorted(du, V.ts.values, side="right") - 1
    d = V.dev.values
    newdev = np.r_[True, d[1:] != d[:-1]]
    newk = np.r_[True, k[1:] != k[:-1]]
    V["deploy_ix"] = k
    V["state"] = np.where(newdev | newk, "F", "K")
    # attributes from the device
    gt = dev.gtype.values[d]
    V["gtype"] = gt
    V["pclass"] = dev.pclass.values[d]
    V["model"] = dev.model.values[d]
    V["home"] = dev.home.values[d]
    V["edition"] = dev.edition.values[d]
    V["app"] = dev.app.values[d]
    V["account_key"] = dev.account_key.values[d]
    V["device_key"] = dev.device_key.values[d]
    loc_day = V.t_local.values.astype("datetime64[D]")
    V["local_day"] = loc_day
    # local-edition pages: article views of edition readers, 60 per cent of them
    tpl = V.template.values
    is_local = (tpl == "artikel") & (V.edition.values != "") & (rng.random(len(V)) < 0.60)
    V["local"] = is_local
    # title: the masthead at view time
    title = V.home.values.copy()
    moved = np.isin(V.edition.values, [s for s, v in P.EDITIONS.items() if v[2]])
    after = loc_day >= np.datetime64(P.EDITION_MOVE.date())
    title[moved & after & is_local] = "KD"
    V["title"] = title
    # subscriber status at view time
    sub_dev = gt == "sub"
    st = dev.sub_start_in_window.values[d]
    active = sub_dev & (np.isnat(st) | (V.t_local.values.astype("datetime64[ns]") >= st))
    V["sub_active"] = active
    return V


def groups(V, ct):
    tpl = V.template.values
    coh = np.isin(tpl, P.COHORTS)
    g = np.full(len(V), "legacy", dtype=object)
    g[coh & V.sub_active.values] = "sub"
    g[coh & ~V.sub_active.values] = "base"
    puz = tpl == P.PUZZLE_T
    g[puz & V.sub_active.values] = "subpuz"
    g[puz & ~V.sub_active.values] = "puz"
    V["group"] = g
    ts = V.ts.values
    sw = np.full(len(V), np.datetime64("2100-01-01"), dtype="datetime64[s]")
    for c in P.COHORTS:
        sw[tpl == c] = ct["COH:" + c]
    on = coh & (ts >= sw)
    V["fx_C"] = (on & (g == "base")) | (coh & (g == "sub") & (ts >= ct["SUB"]))
    V["fx_A"] = (on & (g == "base")) | ((g == "puz") & (ts >= ct["PUZ"]))
    V["fx_E"] = ts >= ct["E"]
    V["fx_B"] = (ts >= ct["B"]) & np.isin(tpl, list(P.HERO))
    V["fx_D"] = ts >= ct["D"]
    return V


def probability(V):
    pc = V.pclass.values
    mult = np.array([P.PHONE_MULT.get(c, 0.0) for c in pc])
    tab = pc == "tablet"
    p = np.array([P.BASE_PHONE[c] for c in pc])
    p += np.where(V.state.values == "F", P.BASE_STATE["F"], 0.0)
    p += np.array([P.BASE_TEMPLATE[t] for t in V.template.values])
    p += np.array([P.BASE_TITLE[t] for t in V.home.values])
    p += np.where(V.local.values, P.BASE_LOCAL, 0.0)
    p += np.where(V.sub_active.values, P.BASE_ADFREE, 0.0)
    p += np.where(V.app.values, P.BASE_APP, 0.0)
    dm = np.where(tab, P.TABLET_STEP_MULT, 1.0)
    cur = np.where(V.local.values, np.array([P.EDITIONS[e][2] or P.EDITIONS[e][1] if e else ""
                                              for e in V.edition.values], dtype=object),
                   V.home.values)
    for c in "EBD":
        st = np.array([P.STEP_T[c][t] for t in cur])
        p += np.where(V["fx_" + c].values, st * dm, 0.0)
    first = V.state.values == "F"
    p += np.where(V.fx_C.values, np.where(first, P.EFF_C["F"], P.EFF_C["K"]) * mult, 0.0)
    p += np.where(V.fx_A.values, np.where(first, P.EFF_A["F"], P.EFF_A["K"]) * mult, 0.0)
    return p / 100.0


def _u(key):
    h = hashlib.sha256(key.encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def allocate(V, scored):
    """Over-line indicator by systematic allocation, time-ordered inside each stratum."""
    p = probability(V)
    weight = V.weight.values
    cur = np.where(V.local.values, np.array([P.EDITIONS[e][2] or P.EDITIONS[e][1] if e else ""
                                              for e in V.edition.values], dtype=object),
                   V.title.values)
    keys = pd.DataFrame({
        "group": V.group.values, "p": np.round(p, 9), "title": cur,
        "local": V.local.values, "pc": V.pclass.values, "st": V.state.values, "w": weight,
    })
    over = np.zeros(len(V), bool)
    idx = np.flatnonzero(scored)
    sub = keys.iloc[idx].reset_index(drop=True)
    cols = list(sub.columns)
    sid = sub.groupby(cols, sort=True).ngroup().values
    first_row = pd.Series(np.arange(len(sid))).groupby(sid).first().values
    labels = sub.iloc[first_row].astype(str).agg("|".join, axis=1).values
    uvals = np.array([_u(s) for s in labels])
    order = np.lexsort((V.ts.values[idx], sid))
    sid_o = sid[order]
    starts = np.r_[0, np.flatnonzero(sid_o[1:] != sid_o[:-1]) + 1]
    ends = np.r_[starts[1:], len(sid_o)]
    pos = np.arange(len(sid_o)) - np.repeat(starts, ends - starts)
    u = uvals[sid_o]
    pp = p[idx][order]
    hit = np.floor(pp * (pos + 1) + u) - np.floor(pp * pos + u)
    over[idx[order]] = hit > 0
    return over, p


def export(dev, V):
    """Collector rules: what each collector version exported, and the weight each row carries."""
    d = V.dev.values
    gt = V.gtype.values
    v2 = V.t_local.values >= np.datetime64(P.COLLECTOR_V2)
    day = V.local_day.values
    inwin = (day >= np.datetime64(P.EXTRACT_START)) & (day <= np.datetime64(P.EXTRACT_END))
    keep_v1 = ~v2 & dev.v1.values[d]
    keep_v2 = v2 & dev.v2.values[d]
    fixed = V.t_local.values >= np.datetime64(P.FORWARDER_FIX)
    keep_v1 = keep_v1 & ~(fixed & (gt == "tablet"))
    keep_v2 = keep_v2 & (gt != "tablet")
    w = np.where(v2, np.where(gt == "anon", P.W_V2_ANON, P.W_V2_SIGNED), P.W_V1)
    gap = (V.local.values & np.isin(V.title.values, ["LA", "KD"])
           & (day >= np.datetime64(P.TAG_GAP[0])) & (day <= np.datetime64(P.TAG_GAP[1])))
    keep = inwin & (keep_v1 | keep_v2) & ~gap
    return keep, w, gap & inwin & (keep_v1 | keep_v2)


REF_LAND = {
    "base": (["search", "social", "direct", "other"], [0.38, 0.22, 0.32, 0.08]),
    "sub": (["direct", "newsletter", "search", "social", "push"], [0.36, 0.28, 0.15, 0.09, 0.12]),
    "puz": (["direct", "newsletter", "search", "social", "push"], [0.36, 0.28, 0.15, 0.09, 0.12]),
}
SECTIONS = ["nyheder", "kultur", "erhverv", "debat", "112"]
SERVICES = ["/tv-guide", "/vejret", "/doedsfald", "/kontakt", "/e-avis"]
PUZZLES = ["krydsord", "sudoku", "ordjagt", "kakuro"]


def context(rng, V):
    n = len(V)
    landing = V.landing.values
    tpl = V.template.values
    nav = np.full(n, "navigate", dtype=object)
    nl = ~landing
    bf = nl & (rng.random(n) < P.BF_SHARE)
    rl = nl & ~bf & (tpl == "liveblog") & (rng.random(n) < 0.35)
    nav[bf] = "back_forward"
    nav[rl] = "reload"
    ref = np.full(n, "internal", dtype=object)
    gt = V.gtype.values
    aud = np.where(np.isin(gt, ["sub"]), "sub", np.where(gt == "puz", "puz", "base"))
    for a, (keys, probs) in REF_LAND.items():
        ix = np.flatnonzero(landing & (aud == a))
        pr = np.asarray(probs) / np.sum(probs)
        ref[ix] = np.asarray(keys, dtype=object)[rng.choice(len(keys), len(ix), p=pr)]
    ref[landing & V.app.values] = "app"
    ect = np.asarray(["4g", "3g", "2g", "slow-2g"], dtype=object)[
        rng.choice(4, n, p=[0.885, 0.09, 0.018, 0.007])]
    model = V.model.values
    ios = np.array([("iPhone" in m) or ("iPad" in m) for m in model])
    samsung = np.array([m.startswith("SM-") for m in model])
    os_ = np.where(ios, "iOS", "Android")
    br = np.where(ios, "Mobile Safari",
                  np.where(samsung & (rng.random(n) < 0.35), "Samsung Internet", "Chrome Mobile"))
    br = np.where(V.app.values, "Sønderå app WebView", br)
    V = V.assign(navigation_type=nav, referrer_class=ref, effective_connection_type=ect,
                 os=os_, browser=br)
    # page paths
    art = rng.integers(5_100_000, 5_380_000, n)
    sec = pd.Series(np.asarray(SECTIONS, dtype=object)[rng.integers(0, len(SECTIONS), n)])
    a = pd.Series(art).astype(str)
    ed = pd.Series(V.edition.values)
    path = pd.Series(np.full(n, "", dtype=object))
    m = {t: tpl == t for t in P.TEMPLATES}
    loc = V.local.values
    path[m["artikel"] & loc] = ("/lokal/" + ed + "/art" + a)[m["artikel"] & loc]
    path[m["artikel"] & ~loc] = ("/" + sec + "/art" + a)[m["artikel"] & ~loc]
    path[m["forside"]] = "/"
    path[m["sektion"]] = ("/" + sec)[m["sektion"]]
    hub = (art % 3) == 0
    path[m["sport"] & ~hub] = ("/sport/art" + a)[m["sport"] & ~hub]
    path[m["sport"] & hub] = "/sport"
    path[m["galleri"]] = ("/galleri/art" + a)[m["galleri"]]
    path[m["liveblog"]] = ("/liveblog/art" + pd.Series(art // 40).astype(str))[m["liveblog"]]
    path[m["arkiv"]] = ("/arkiv/art" + pd.Series(art - 2_900_000).astype(str))[m["arkiv"]]
    path[m["tjenester"]] = pd.Series(np.asarray(SERVICES, dtype=object)[art % len(SERVICES)])[m["tjenester"]]
    path[m["spil"]] = ("/spil/" + pd.Series(np.asarray(PUZZLES, dtype=object)[art % len(PUZZLES)]))[m["spil"]]
    path = path.values
    V["url_path"] = path
    return V


def timings(rng, V, over, scored):
    n = len(V)
    centre = {"low": 2650.0, "mid": 2150.0, "high": 1650.0, "tablet": 1750.0}
    c = np.array([centre[x] for x in V.pclass.values])
    under = np.exp(rng.normal(np.log(c), 0.30))
    under = np.where(under >= 3990, 3990 - rng.integers(0, 900, n), under)
    under = np.clip(under, 420, 3989)
    hi = 4001 + np.exp(rng.normal(np.log(1400), 0.65, n))
    lcp = np.where(over, hi, under).round().astype(np.int64).astype(float)
    lcp[~scored] = np.nan
    ttfb = np.exp(rng.normal(np.log(330), 0.45, n)).round().astype(np.int64)
    cls = np.round(np.abs(rng.normal(0.04, 0.05, n)), 3)
    return lcp, ttfb, cls
