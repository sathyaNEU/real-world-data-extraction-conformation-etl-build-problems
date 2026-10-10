"""task129 generator: assemble the beacon export (the spine) and keep the truth beside it."""
import hashlib

import numpy as np
import pandas as pd

import params as P
import traffic as T
import beacons as B


def build(rng):
    dev = T.devices(rng)
    ses = T.sessions(rng, dev)
    V = T.views(rng, dev, ses)
    dep = B.deploy_table(rng)
    ct = B.change_times(dep)
    V = B.annotate(rng, dev, V, dep)
    V = B.groups(V, ct)
    keep, w, gap_rows = B.export(dev, V, ct)
    n_gap = int(gap_rows.sum())
    X = V[keep].reset_index(drop=True)
    X["weight"] = w[keep]
    X = B.context(rng, X)
    scored = X.navigation_type.values != "back_forward"
    over, p = B.allocate(X, scored)
    X["over"] = over
    X["p"] = p
    lcp, ttfb, cls = B.timings(rng, X, over, scored)
    X["lcp_ms"], X["ttfb_ms"], X["cls"] = lcp, ttfb, cls
    # identifiers
    n = len(X)
    alpha = np.array(list("abcdefghijkmnpqrstuvwxyz23456789"))
    raw = rng.integers(0, 32, (n, 10))
    pv = np.array(["".join(r) for r in alpha[raw]], dtype=object)
    assert len(set(pv)) == n
    X["pv_id"] = pv
    # August cached-load views kept by audience and template (tuning knob, hash of the key)
    if P.KEEP_AUG:
        h = np.array([int(hashlib.sha256(k.encode()).hexdigest()[:8], 16) / 2 ** 32 for k in pv])
        drop = np.zeros(n, bool)
        aug = (X.local_day.values >= np.datetime64("2026-08-01")) & (X.state.values == "K")
        for key, keep in P.KEEP_AUG.items():
            grp, tpl = key.split("|")
            m = aug & (X.group.values == grp) & (X.template.values == tpl)
            drop |= m & (h >= keep)
        X = X[~drop].reset_index(drop=True)
        n = len(X)
    # collector v1 forwarded Sønderå Tidende app-webview beacons twice from 16 March to 7 May
    day = X.local_day.values
    dup = (X.app.values & (X.title.values == "ST") & (day >= np.datetime64(P.DUP_WINDOW[0]))
           & (day <= np.datetime64(P.DUP_WINDOW[1])))
    D = X[dup].copy()
    D["ingest_delay"] = rng.integers(40, 900, len(D))
    X["ingest_delay"] = rng.integers(1, 30, n)
    X["is_dup"] = False
    D["is_dup"] = True
    S = pd.concat([X, D], ignore_index=True)
    ing = S.ts.values + S.ingest_delay.values.astype("timedelta64[s]")
    o = np.lexsort((S.pv_id.values, ing))
    bid = np.empty(len(S), np.int64)
    gaps = rng.integers(1, 4, len(S))
    bid[o] = 41_000_000 + np.cumsum(gaps)
    S["beacon_id"] = bid
    S = S.sort_values(["ts", "beacon_id"], kind="stable").reset_index(drop=True)
    return dict(dev=dev, dep=dep, ct=ct, V=V, X=X, S=S, n_gap=n_gap)
