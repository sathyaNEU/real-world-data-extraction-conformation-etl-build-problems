"""task197 physics core: system frequency, site programmes, site power, qualifying episodes.

Everything here is deterministic given SEED. The shipped pack is cut from these series and the
graded figures are computed from the same arrays, so target/, golden/ and figures.json agree by
construction.
"""
import numpy as np, datetime as dt, hashlib

SEED = 1970417
WINDOW_START = dt.date(2026, 9, 21)
WINDOW_END = dt.date(2026, 10, 11)          # inclusive, 21 days
AS_OF = dt.date(2026, 10, 13)
LOCAL_OFFSET_H = 2                          # CEST all window (DST ends 2026-10-25)
DEADBAND = 0.010                            # Hz
FULL_ACT = 0.200                            # Hz
SPAN = FULL_ACT - DEADBAND                  # 0.190 Hz
QUALIFY_HZ = 49.920                         # f at or below this
QUALIFY_SECS = 15                           # for at least this many consecutive seconds
DAY = 86400

# --- sites -------------------------------------------------------------------------------------
# pts: coarse daily anchors (local hour, MW) of the programme, net export at the grid connection
# (negative = import). stair: (h_from, h_to, MW per quarter hour, h_reset) the cumulative trim the
# site's own intraday position adds through that span, held until h_reset. ramp_s: the realised ramp
# duration of the site's controller; no shipped document states it.
SITES = [
    dict(id="VKF-OOS", name="Oosterhout", kind="battery", pmax=12.0, cap=6.0, gain=0.982386, gain_dn=0.987837,
         tau=4.0, ramp_s=85, blocks=[1, 3],
         pts=[(0, 0), (5.0, 0), (5.5, 4.8), (9.5, 4.8), (9.75, 0), (10.5, -6.4), (14.5, -6.4),
              (15.5, 0), (17.0, 8.4), (19.5, 8.4), (20.5, 0), (24, 0)],
         stair=[(5.5, 7.75, -0.46, 9.75)]),
    dict(id="VKF-ZWT", name="Zwartewater", kind="battery", pmax=20.0, cap=8.0, gain=1.008993, gain_dn=0.957413,
         tau=3.0, ramp_s=80, blocks=[2],
         pts=[(0, 0), (5.25, 0), (5.75, 13.2), (11.25, 13.2), (11.5, -9.6), (15.0, -9.6),
              (16.0, 0), (17.5, 14.0), (20.0, 14.0), (21.0, 0), (24, 0)],
         stair=[(8.0, 11.25, -1.52, 11.5)]),
    dict(id="VKF-HGZ", name="Hoogezand", kind="gas_engine", pmax=9.0, cap=3.0, gain=0.919577, gain_dn=0.910017,
         tau=6.0, ramp_s=185, blocks=[4, 5],
         pts=[(0, 1.2), (6.0, 1.2), (6.75, 6.4), (9.5, 6.4), (10.25, 1.2), (11.0, 4.2),
              (13.75, 4.2), (14.0, 1.2), (16.25, 1.2), (17.0, 3.6), (21.75, 3.6), (22.0, 1.2),
              (24, 1.2)],
         stair=[(17.0, 19.75, 0.20, 22.0)]),
    dict(id="VKF-KPV", name="Kampvliet", kind="battery", pmax=10.0, cap=5.0, gain=0.737286, gain_dn=0.750940,
         tau=4.0, ramp_s=90, blocks=[4],
         pts=[(0, 0), (6.75, 0), (7.25, 4.4), (9.25, 4.4), (10.0, 0), (11.0, -5.2), (14.0, -5.2),
              (15.0, 0), (16.0, 0.6), (20.0, 0.6), (20.75, 0), (24, 0)],
         stair=[(16.0, 18.75, 0.76, 20.75)]),
    dict(id="VKF-MPD", name="Meppelerdiep", kind="gas_engine", pmax=6.0, cap=2.0, gain=1.022230, gain_dn=1.001239,
         tau=7.0, ramp_s=200, blocks=[1],
         pts=[(0, 0.8), (5.5, 0.8), (6.25, 3.2), (10.0, 3.2), (10.75, 0.8), (11.5, 3.4),
              (14.0, 3.4), (14.25, 0.8), (17.0, 0.8), (17.75, 5.1), (21.5, 5.1), (22.25, 0.8),
              (24, 0.8)],
         stair=[(6.25, 7.75, 0.34, 10.75)]),
    dict(id="VKF-NWV", name="Nieuwveen", kind="battery", pmax=15.0, cap=6.0, gain=0.930253, gain_dn=0.909233,
         tau=3.5, ramp_s=95, blocks=[1, 2],
         pts=[(0, 0), (1.0, -4.8), (4.0, -4.8), (5.0, 0), (6.0, 5.4), (9.5, 5.4), (10.0, 0),
              (11.5, -7.2), (14.5, -7.2), (15.5, 0), (17.5, 9.6), (20.0, 9.6), (21.0, 0), (24, 0)],
         stair=[(6.0, 9.25, -0.11, 10.0)]),
    dict(id="VKF-TRB", name="Terborgh", kind="industrial_load", pmax=8.0, cap=3.0, gain=1.047016, gain_dn=1.013484,
         tau=5.0, ramp_s=300, blocks=[2],
         pts=[(0, -2.1), (5.75, -2.1), (6.0, -7.4), (13.75, -7.4), (14.0, -4.6), (21.75, -4.6),
              (22.0, -2.1), (24, -2.1)],
         stair=[(8.0, 10.0, 0.63, 13.75)]),
    dict(id="VKF-DLK", name="Dollardkust", kind="battery", pmax=25.0, cap=10.0, gain=0.945685, gain_dn=0.937169,
         tau=3.0, ramp_s=100, blocks=[4, 0],
         pts=[(0, 0), (0.5, -12.0), (4.5, -12.0), (5.5, 0), (7.0, 9.0), (9.0, 9.0), (10.0, 0),
              (11.0, -14.0), (15.0, -14.0), (16.0, 2.5), (20.0, 2.5), (21.0, 0), (24, 0)],
         stair=[(16.0, 19.75, 0.34, 21.0)]),
    dict(id="VKF-RDL", name="Reiderland", kind="gas_engine", pmax=7.0, cap=2.5, gain=0.871397, gain_dn=0.855481,
         tau=6.5, ramp_s=190, blocks=[4],
         pts=[(0, 1.0), (6.25, 1.0), (7.0, 5.1), (9.75, 5.1), (10.5, 1.0), (11.25, 4.0),
              (14.25, 4.0), (14.5, 0.8), (16.0, 0.8), (21.25, 0.8), (22.25, 0.8), (24, 1.0)],
         stair=[(16.5, 19.0, 0.70, 22.25)]),
]
SITE_BY_ID = {s["id"]: s for s in SITES}
BLOCK_HOURS = [(0, 4), (4, 8), (8, 12), (12, 16), (16, 20), (20, 24)]   # local, FCR blocks 1..6

# Days a site is out of the reserve market, with the reason the platform event log carries.
OUT_OF_MARKET = {
    "VKF-KPV": [dt.date(2026, 9, 24), dt.date(2026, 9, 25)],
    "VKF-MPD": [dt.date(2026, 10, 6)],
    "VKF-DLK": [dt.date(2026, 9, 29)],
}
# Cover taken by another site while one is out, and the weekend reshuffle.
COVER = {(dt.date(2026, 9, 24), 4): "VKF-DLK", (dt.date(2026, 9, 25), 4): "VKF-DLK",
         (dt.date(2026, 10, 6), 1): "VKF-NWV", (dt.date(2026, 9, 29), 4): "VKF-HGZ"}


def commitments(site, d):
    """The FCR blocks the site is contracted for on local date d."""
    blocks = list(site["blocks"])
    if d in OUT_OF_MARKET.get(site["id"], []):
        return []
    if d.weekday() >= 5:                      # the weekend portfolio runs two blocks fewer
        blocks = [b for b in blocks if b not in (0, 3)]
    for (cd, cb), sid in COVER.items():
        if cd == d and sid == site["id"] and cb not in blocks:
            blocks.append(cb)
    return sorted(blocks)

# --- system net-load ramp by local quarter hour -------------------------------------------------
def netload_ramp_profile():
    """Signed net-load change per quarter hour (normalised units): positive = net load rising, which
    leaves the stepped programmes short just after the boundary and pulls the frequency down."""
    prof = np.zeros(96)
    for p in range(96):
        h = p / 4.0
        v = 0.0
        if h < 4.5:             v = -0.52 - 0.18 * np.sin(np.pi * h / 4.5)
        elif 4.5 <= h < 5.0:    v = 0.0
        elif 5.0 <= h < 7.0:    v = 0.45 + 0.25 * (h - 5.0) / 2.0
        elif 7.0 <= h < 9.25:   v = 0.80 + 0.45 * np.sin(np.pi * (h - 7.0) / 2.25)
        elif 9.25 <= h < 13.0:  v = -0.72 - 0.26 * np.sin(np.pi * (h - 9.25) / 3.75)
        elif 13.0 <= h < 15.5:  v = -0.10
        elif 15.5 <= h < 19.0:  v = 0.70 + 0.55 * np.sin(np.pi * (h - 15.5) / 3.5)
        elif 19.0 <= h < 23.0:  v = -0.78 - 0.30 * np.sin(np.pi * (h - 19.0) / 4.0)
        prof[p] = v
    return prof

NETLOAD = netload_ramp_profile()
DFD_K = 0.086        # Hz per unit of normalised ramp
DFD_PEAK_S = 80      # seconds after the boundary at which the deviation peaks
DFD_LEN_S = 160

def _stable(*key):
    """A hash that does not move between processes, so the pack rebuilds byte for byte."""
    raw = "|".join(str(k) for k in key).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(raw, digest_size=8).digest(), "big")


def _rng(*key):
    return np.random.RandomState((SEED + _stable(*key)) % (2**32 - 1))

def dates():
    d, out = WINDOW_START, []
    while d <= WINDOW_END:
        out.append(d)
        d += dt.timedelta(days=1)
    return out

INCIDENTS = {           # unplanned infeed losses: date -> (local hour decimal, depth Hz, decay s)
    dt.date(2026, 9, 24): (13.60, 0.138, 420),
    dt.date(2026, 10, 2): (22.35, 0.126, 360),
    dt.date(2026, 10, 8): (11.15, 0.151, 480),
}

def frequency_day(d):
    """1 Hz system frequency for one local day, as a numpy array of 86400 samples (index = second
    of the local day). Deterministic in (SEED, date)."""
    r = _rng("freq", d.isoformat())
    n = DAY
    # mean-reverting background
    noise = np.zeros(n)
    phi, sd = np.exp(-1.0 / 45.0), 0.0040
    e = r.normal(0, sd * np.sqrt(1 - phi**2), n)
    v = 0.0
    for i in range(n):
        v = phi * v + e[i]
        noise[i] = v
    f = 50.0 + noise
    # deterministic deviations at each quarter-hour boundary
    wk = 1.0 if d.weekday() < 5 else 0.82
    shape = np.sin(np.pi * np.arange(DFD_LEN_S) / (2.0 * DFD_PEAK_S)) ** 2
    for p in range(96):
        T = p * 900
        amp = DFD_K * NETLOAD[p] * wk * (1.0 + r.normal(0, 0.16))
        seg = slice(T, min(T + DFD_LEN_S, n))
        f[seg] -= amp * shape[: seg.stop - seg.start]
    if d in INCIDENTS:
        h, depth, decay = INCIDENTS[d]
        t0 = int(round(h * 3600))
        k = np.arange(n - t0)
        bump = depth * np.minimum(1.0, k / 8.0) * np.exp(-k / decay)
        f[t0:] -= bump
    return f

# --- programmes --------------------------------------------------------------------------------
def programme(site, d):
    """The site's market programme: 96 quarter-hour setpoints in MW, net export."""
    r = _rng("prog", site["id"], d.isoformat())
    pts = site["pts"]
    out = np.zeros(96)
    for p in range(96):
        h = p / 4.0
        lvl = pts[-1][1]
        for (h0, v0), (h1, v1) in zip(pts, pts[1:]):
            if h0 <= h < h1:
                lvl = v0 + (v1 - v0) * ((h - h0) / (h1 - h0)) if (h1 - h0) <= 1.01 else v0
                break
        out[p] = lvl
    for st in site.get("stair", []):
        h0, h1, stp, hr = st
        k, kmax = 0, 0
        for p in range(96):
            h = p / 4.0
            if h0 <= h <= h1:
                out[p] += stp * k
                k += 1
                kmax = k - 1
            elif h1 < h < hr:
                out[p] += stp * kmax
    wk = 0.9 if d.weekday() >= 5 else 1.0
    out = out * wk + r.normal(0, 0.035, 96) * np.maximum(0.3, np.abs(out))
    return np.round(np.clip(out, -site["pmax"], site["pmax"]), 3)

def traj(site, prog, t):
    """The programme trajectory in MW at local second t: linear ramp of length ramp_s from the
    boundary. Vectorised over t."""
    t = np.asarray(t, dtype=float)
    p = np.minimum(95, (t // 900).astype(int))
    prev = np.where(p > 0, prog[np.maximum(p - 1, 0)], prog[0])
    cur = prog[p]
    frac = np.clip((t - p * 900) / float(site["ramp_s"]), 0.0, 1.0)
    return prev + (cur - prev) * frac

def required(site, f):
    """Required FCR response in MW at frequency f (positive = increase export for under-frequency)."""
    dev = 50.0 - np.asarray(f, dtype=float)
    mag = np.clip((np.abs(dev) - DEADBAND) / SPAN, 0.0, 1.0) * site["cap"]
    return np.sign(dev) * mag

def contracted(site, t_local_s, d=None):
    """True where the site is inside one of its contracted FCR blocks at local second t. With no
    date the site's standing pattern is used; with a date, that day's commitments."""
    h = (np.asarray(t_local_s, dtype=float) / 3600.0) % 24.0
    out = np.zeros(np.shape(h), dtype=bool)
    for b in (site["blocks"] if d is None else commitments(site, d)):
        lo, hi = BLOCK_HOURS[b]
        out |= (h >= lo) & (h < hi)
    return out

_fcr_gate = None            # build.py installs the reserve-availability gate here


def site_power(site, d, f, prog, lo, hi):
    """Net active power in MW for local seconds [lo, hi), from the trajectory, the lagged FCR
    response and telemetry noise."""
    t = np.arange(lo, hi)
    base = traj(site, prog, t)
    gate = _fcr_gate(site, d, t) if _fcr_gate else contracted(site, t, d)
    req = required(site, f[lo:hi]) * gate
    gu, gd = site["gain"], site.get("gain_dn", site["gain"])
    a = np.exp(-1.0 / site["tau"])
    resp = np.zeros(len(t))
    # warm start: run the lag from 400 s before the window so the state is right
    pre_lo = max(0, lo - 400)
    tp = np.arange(pre_lo, lo)
    gate_pre = _fcr_gate(site, d, tp) if _fcr_gate else contracted(site, tp, d)
    req_pre = required(site, f[pre_lo:lo]) * gate_pre
    v = 0.0
    for x in req_pre:
        v = a * v + (1 - a) * (gu if x >= 0 else gd) * x
    for i, x in enumerate(req):
        v = a * v + (1 - a) * (gu if x >= 0 else gd) * x
        resp[i] = v
    r = _rng("tel", site["id"], d.isoformat(), int(lo))
    noise = r.normal(0, 0.013, len(t)) + 0.004 * np.sin(t / 17.0 + _stable(site["id"]) % 7)
    return base + resp + noise

# --- episodes ----------------------------------------------------------------------------------
def qualifying_episodes(d, f):
    """Every qualifying under-frequency episode in one local day: f <= QUALIFY_HZ for at least
    QUALIFY_SECS consecutive seconds. Returns (start_s, end_s, deepest_s, min_f)."""
    below = f <= QUALIFY_HZ
    out, i, n = [], 0, len(f)
    while i < n:
        if not below[i]:
            i += 1
            continue
        j = i
        while j < n and below[j]:
            j += 1
        if j - i >= QUALIFY_SECS:
            seg = f[i:j]
            k = int(np.argmin(seg))
            out.append((i, j - 1, i + k, float(seg[k])))
        i = j
    return out

def excursions(f, thresh=0.040, min_secs=20):
    """Maximal runs where |f - 50| >= thresh, used for the operator's 1 Hz extract windows."""
    out, i, n = [], 0, len(f)
    bad = np.abs(f - 50.0) >= thresh
    while i < n:
        if not bad[i]:
            i += 1
            continue
        j = i
        while j < n and bad[j]:
            j += 1
        if j - i >= min_secs:
            out.append((i, j - 1))
        i = j
    return out
