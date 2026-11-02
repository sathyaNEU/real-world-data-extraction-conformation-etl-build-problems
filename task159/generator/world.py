"""The clean truth of the Kessock Lake world: the Main Zone's block grades, the resource model's estimates, the
mining sequence, every blast hole and its assay, and the operating records the asks read. Nothing here is written
to target/; pack.py renders it with the systems' own conventions."""
import math
import datetime as dt
import numpy as np
import pandas as pd

import params as P


def _rng(tag):
    """One independent stream per purpose, so a change in one never moves another."""
    h = 0
    for ch in tag:
        h = (h * 131 + ord(ch)) % 2_147_483_647
    return np.random.default_rng([P.SEED, h])


def _grf(rng, shape, ranges, cell):
    kx = np.fft.fftfreq(shape[0], d=cell[0])
    ky = np.fft.fftfreq(shape[1], d=cell[1])
    kz = np.fft.fftfreq(shape[2], d=cell[2])
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
    S = np.exp(-((math.pi * ranges[0] * KX) ** 2 + (math.pi * ranges[1] * KY) ** 2 + (math.pi * ranges[2] * KZ) ** 2))
    w = rng.normal(size=shape)
    f = np.real(np.fft.ifftn(np.fft.fftn(w) * np.sqrt(S)))
    return (f - f.mean()) / f.std()


# ---------------------------------------------------------------------------------------------------------------
# Geometry and grades
# ---------------------------------------------------------------------------------------------------------------

def blocks():
    """Every Main Zone block of the model extent with its estimate and its true grade."""
    ii, jj, kk = np.meshgrid(np.arange(P.NX), np.arange(P.NY), np.arange(P.NZ), indexing="ij")
    xc = P.X0 + (ii + 0.5) * P.BX
    yc = P.Y0 + (jj + 0.5) * P.BY
    zc = P.ZTOP - (kk + 0.5) * P.BZ
    depth = P.ZTOP - zc
    centre = P.Y0 + 236.0 + 0.24 * depth
    half = (52.0 + 14.0 * np.sin((xc - P.X0) / 160.0)) * (1.0 + 0.0062 * depth)
    dom = (np.abs(yc - centre) <= half) & (xc > P.X0 + 40) & (xc < P.X0 + 1080) & (zc > 1150)
    z = _grf(_rng("field"), (P.NX, P.NY, P.NZ), P.FIELD_RANGES, (P.BX, P.BY, P.BZ))
    m = np.exp(math.log(P.MODEL_MEDIAN) + P.MODEL_LOG_SD * z)
    eps = _rng("block").normal(0.0, P.BLOCK_LOG_SD, size=m.shape)
    g = m * np.exp(eps - P.BLOCK_LOG_SD ** 2 / 2.0)
    sel = dom.ravel()
    df = pd.DataFrame({
        "i": ii.ravel()[sel], "j": jj.ravel()[sel], "k": kk.ravel()[sel],
        "xc": xc.ravel()[sel], "yc": yc.ravel()[sel], "zc": zc.ravel()[sel],
        "model": np.round(m.ravel()[sel], 3), "true": g.ravel()[sel],
    })
    df["bench"] = (df["zc"] - P.BZ / 2.0).round().astype(int)        # bench floor, mine RL
    rng = _rng("density")
    df["rock"] = np.where(rng.random(len(df)) < 0.18, "MAF", "FSV")      # mafic volcanics / felsic volcanics
    df["density"] = np.where(df["rock"] == "MAF", 2.84, 2.74)
    df["tonnes"] = df["density"] * P.BLOCK_VOL
    df["model"] = df["model"].clip(lower=0.005)
    df["ijk"] = (df["i"] * 10000 + df["j"] * 100 + df["k"]).astype(int)
    return df.sort_values(["k", "i", "j"]).reset_index(drop=True)


def edge_blocks(df):
    """Waste blocks just outside the Main Zone on the mined benches: grade control samples their holes too."""
    have = set(zip(df.i, df.j, df.k))
    out = set()
    for (i, j, k) in have:
        for dj in (-1, 1):
            q = (i, j + dj, k)
            if q not in have and 0 <= j + dj < P.NY:
                out.add(q)
    rows = [(i, j, k) for (i, j, k) in sorted(out)]
    e = pd.DataFrame(rows, columns=["i", "j", "k"])
    e["xc"] = P.X0 + (e["i"] + 0.5) * P.BX
    e["yc"] = P.Y0 + (e["j"] + 0.5) * P.BY
    e["zc"] = P.ZTOP - (e["k"] + 0.5) * P.BZ
    e["bench"] = (e["zc"] - P.BZ / 2.0).round().astype(int)
    rng = _rng("edge")
    e["true"] = np.exp(math.log(0.035) + 0.95 * rng.normal(size=len(e)))
    return e


# ---------------------------------------------------------------------------------------------------------------
# Mining sequence
# ---------------------------------------------------------------------------------------------------------------

def month_start(n):
    y = P.HIST_START.year + (P.HIST_START.month - 1 + n) // 12
    mo = (P.HIST_START.month - 1 + n) % 12 + 1
    return dt.date(y, mo, 1)


def sequence(df):
    """History blocks get the month the survey depleted them; 2027 blocks the month the plan schedules them."""
    df = df.copy()
    hist_b = P.HIST_BENCH_FLOORS
    plan_b = P.PLAN_BENCH_FLOORS
    df["period"] = np.where(df["bench"].isin(hist_b), "HIST", np.where(df["bench"].isin(plan_b), "PLAN", "LATER"))
    rng = _rng("sequence")
    # history: benches top down, each bench advancing along strike; 46 months over 16 benches
    h = df["period"] == "HIST"
    bidx = df.loc[h, "bench"].map({b: n for n, b in enumerate(hist_b)})
    xfrac = (df.loc[h, "xc"] - P.X0) / (P.NX * P.BX)
    pos = (bidx + xfrac + rng.normal(0, 0.035, h.sum())).clip(0, len(hist_b) - 1e-6)
    df.loc[h, "month_idx"] = np.floor(pos / len(hist_b) * P.HIST_MONTHS).astype(int)
    # day within the month
    days = []
    for mi, r in zip(df.loc[h, "month_idx"].astype(int), rng.random(h.sum())):
        ms = month_start(mi)
        nd = (month_start(mi + 1) - ms).days
        days.append(ms + dt.timedelta(days=int(r * nd)))
    df.loc[h, "mined"] = days
    # 2027: two months a bench, along strike
    p = df["period"] == "PLAN"
    pidx = df.loc[p, "bench"].map({b: n for n, b in enumerate(plan_b)})
    xf = (df.loc[p, "xc"] - P.X0) / (P.NX * P.BX)
    df.loc[p, "plan_month"] = (1 + np.floor((pidx + xf) * 2.0)).clip(1, 12).astype(int)
    return df


# ---------------------------------------------------------------------------------------------------------------
# Blast holes
# ---------------------------------------------------------------------------------------------------------------

def holes(df, edge):
    """Every blast hole drilled on the history benches, with its true assay in g/t."""
    rng = _rng("holes")
    hist = df[df["period"] == "HIST"]
    counts = rng.choice([c for c, _ in P.P_HOLES], p=[p for _, p in P.P_HOLES], size=len(hist))
    rows = []
    for (idx, b), n in zip(hist.iterrows(), counts):
        for h in range(n):
            u, v = rng.uniform(1.0, P.BX - 1.0), rng.uniform(1.0, P.BY - 1.0)
            a = b["true"] * math.exp(rng.normal(0, P.HOLE_LOG_SD) - P.HOLE_LOG_SD ** 2 / 2.0)
            lead = int(rng.integers(4, 24))
            rows.append((int(b["ijk"]), b["bench"], b["xc"] - P.BX / 2 + u, b["yc"] - P.BY / 2 + v, a,
                         b["mined"] - dt.timedelta(days=lead), True))
    # edge waste: one or two holes, drilled with their neighbours
    hb = {}
    for (i_, k_), m_ in zip(zip(hist["i"], hist["k"]), hist["mined"]):
        hb.setdefault((int(i_), int(k_)), m_)
    eh = edge[edge["bench"].isin(P.HIST_BENCH_FLOORS)]
    for _, b in eh.iterrows():
        key = (int(b["i"]), int(b["k"]))
        if key not in hb:
            continue
        mined = hb[key]
        for h in range(int(rng.integers(1, 3))):
            u, v = rng.uniform(1.0, P.BX - 1.0), rng.uniform(1.0, P.BY - 1.0)
            a = b["true"] * math.exp(rng.normal(0, P.HOLE_LOG_SD) - P.HOLE_LOG_SD ** 2 / 2.0)
            rows.append((-1, b["bench"], b["xc"] - P.BX / 2 + u, b["yc"] - P.BY / 2 + v, a,
                         mined - dt.timedelta(days=int(rng.integers(4, 24))), False))
    hd = pd.DataFrame(rows, columns=["ijk", "bench", "mx", "my", "au", "drilled", "in_zone"])
    hd["bench"] = hd["bench"].astype(int)
    hd = hd.sort_values(["drilled", "bench", "mx", "my"]).reset_index(drop=True)
    return hd


def mine_to_utm(mx, my):
    th = math.radians(P.ROT_DEG)
    dx, dy = (np.asarray(mx) - P.X0) * P.SCALE, (np.asarray(my) - P.Y0) * P.SCALE
    e = P.E_ORIGIN + dx * math.cos(th) + dy * math.sin(th)
    n = P.N_ORIGIN - dx * math.sin(th) + dy * math.cos(th)
    return e, n


def utm_to_mine(e, n):
    th = math.radians(P.ROT_DEG)
    de, dn = np.asarray(e) - P.E_ORIGIN, np.asarray(n) - P.N_ORIGIN
    dx = de * math.cos(th) - dn * math.sin(th)
    dy = de * math.sin(th) + dn * math.cos(th)
    return P.X0 + dx / P.SCALE, P.Y0 + dy / P.SCALE
