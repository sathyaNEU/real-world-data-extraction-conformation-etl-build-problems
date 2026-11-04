"""task211 world: Nordvig Marine's five North Sea sites, the hourly sea-state record and the vessels' shelter cycle.

The clean truth lives here: the regional fronts, each site's hourly significant wave height, every floating vessel's
shelter cycle replayed jointly (who holds the heavy-lift berth at a port, who goes on to storm moorings), the past
campaigns as they ran, and the forward campaign under each jack-up placement. Everything is computed forward from
seeded draws; nothing is fitted to a target.
"""
import numpy as np

SEED = 2230                  # the record stream for task211 (tie-free at the Bramso berth, every graded figure mid-bin)
WINTERS = list(range(2008, 2026))            # winter starting year: 2008 means 1 Nov 2008 to 28 Feb 2009
H = 24 * 120                                 # campaign hours, 1 Nov 00:00 to 28 Feb 24:00 Danish time
PAD = 96                                     # hours of record kept after the window for look-ahead
LW, LS, TC = 1.8, 3.2, 10                    # working limit, station-keeping limit (Hs, m), critical lift hours

SITES = ["SKG", "LVB", "OSR", "MOF", "FJH"]
SITE_NAME = {"SKG": "Skarvgrund", "LVB": "Lillevig Banke", "OSR": "Osterrev", "MOF": "Molleflak", "FJH": "Fjernhav"}
# lag of the regional front at the site (h), exposure scale, exposure to northerly fronts
SITE_CLIMATE = {
    "SKG": dict(lag=0.0, scale=1.02, north=0.55),
    "LVB": dict(lag=9.0, scale=0.84, north=1.00),
    "OSR": dict(lag=3.0, scale=1.14, north=1.00),
    "MOF": dict(lag=5.0, scale=0.92, north=0.85),
    "FJH": dict(lag=11.0, scale=0.97, north=0.80),
}
# ports: heavy-lift berths; passage hours from each site at the class's service speed
PORTS = {
    "BRA": dict(name="Bramso Havn", heavy_lift_berths=1),
    "KAL": dict(name="Kalvholm", heavy_lift_berths=0),
    "SAN": dict(name="Sandvig", heavy_lift_berths=1),
    "TRV": dict(name="Tranevig", heavy_lift_berths=2),
    "HJB": dict(name="Hjortby Havn", heavy_lift_berths=1),
}
PASSAGE = {   # hours, site -> port
    "SKG": {"BRA": 12, "KAL": 27, "SAN": 12, "TRV": 19, "HJB": 22},
    "LVB": {"BRA": 9, "KAL": 25, "SAN": 10, "TRV": 16, "HJB": 20},
    "OSR": {"BRA": 18, "KAL": 21, "SAN": 17, "TRV": 4, "HJB": 15},
    "MOF": {"BRA": 15, "KAL": 19, "SAN": 14, "TRV": 5, "HJB": 13},
    "FJH": {"BRA": 23, "KAL": 28, "SAN": 22, "TRV": 14, "HJB": 13},
}
STATIONS = {  # station id, the old export's buoy name, position, water depth (m)
    "SKG": ("NVB-0412", "SKARVGRUND WR", 55.512, 6.284, 31),
    "LVB": ("NVB-0587", "LILLEVIG BNK WR", 55.776, 7.418, 24),
    "OSR": ("NVB-0233", "OSTERREV OUTER", 56.104, 6.751, 38),
    "MOF": ("NVB-0319", "MOLLEFLAK WR", 55.329, 7.602, 19),
    "FJH": ("NVB-0761", "FJERNHAV DW", 56.448, 5.937, 44),
}
SHELTER = {"SKG": "BRA", "LVB": "BRA", "OSR": "TRV", "MOF": "TRV", "FJH": "HJB"}
STORM_MOORINGS = "KAL"     # where a vessel finding its shelter berth taken goes, as the past records show
PORT_PASSAGE = {          # hours between ports at the class's service speed
    "BRA": {"KAL": 16, "SAN": 2, "TRV": 14, "HJB": 17},
    "TRV": {"BRA": 14, "KAL": 19, "SAN": 13, "HJB": 9},
    "HJB": {"BRA": 17, "KAL": 21, "SAN": 16, "TRV": 9},
    "SAN": {"BRA": 2, "KAL": 15, "TRV": 13, "HJB": 16},
    "KAL": {"BRA": 16, "SAN": 15, "TRV": 19, "HJB": 21},
}


def hindcast(rng):
    """Hourly Hs per site for every winter: regional fronts (clustered arrivals, a peak, a duration and a
    direction) reaching each site with its lag, scaled by its exposure, plus local AR(1) sea. Returns
    {site: array (n_winters, H + PAD)} and the fronts per winter."""
    n = len(WINTERS)
    out = {s: np.zeros((n, H + PAD)) for s in SITES}
    fronts = []
    L = H + PAD + 48
    for w in range(n):
        base = np.full(L, 1.0)
        fl = []
        t = 0.0
        while True:
            t += rng.exponential(30.0) if rng.random() < 0.50 else rng.exponential(120.0)
            if t >= L:
                break
            peak = rng.gamma(4.0, 0.55) + 0.8
            dur = rng.gamma(3.2, 6.5) + 6.0
            north = rng.random() < 0.30
            speed = rng.normal(1.0, 0.04)
            fl.append((t, peak, dur, north, speed))
        fronts.append(fl)
        for s in SITES:
            c = SITE_CLIMATE[s]
            sig = np.full(H + PAD, 1.0)
            idx = np.arange(H + PAD)
            for (t0, peak, dur, north, speed) in fl:
                tc = t0 + c["lag"] * speed - 48
                lo, hi = int(max(0, tc - dur * 0.2)), int(min(H + PAD, tc + dur * 2.6))
                if hi <= lo:
                    continue
                x = (idx[lo:hi] - tc) / dur
                amp = peak * c["scale"] * (c["north"] if north else 1.0)
                sig[lo:hi] = np.maximum(sig[lo:hi], 0.95 + amp * np.exp(-((x - 0.5) ** 2) / 0.12))
            z = rng.normal(0.0, 0.09, H + PAD)
            e = np.empty(H + PAD); e[0] = 0.0
            for h in range(1, H + PAD):
                e[h] = 0.92 * e[h - 1] + z[h]
            out[s][w] = np.round(np.maximum(0.25, sig * (1.0 + 0.10 * e) + 0.35 * e), 2)
    return out, fronts


def runlen_below(x, lim):
    n = len(x); r = np.zeros(n + 1, dtype=np.int32)
    for h in range(n - 1, -1, -1):
        r[h] = r[h + 1] + 1 if x[h] <= lim else 0
    return r[:n]


def replay(hs, sites, conflict="moorings", margin=0, tc=TC, ls=LS, lw=LW, horizon=H, start=0, log=False,
           active=None, trace=False):
    """Replay the floating vessels at `sites` jointly over one winter's record `hs` ({site: array}), hour by hour,
    in the order `sites` lists them. The weather procedure: a vessel at its site leaves for its shelter port at the
    latest hour that brings it alongside by the start of the first hour in which Hs at the site is above the
    station-keeping limit (passage hours P: it leaves at hour h when an hour in h..h+P is above the limit); it works
    in every hour at the site with Hs at or below the working limit; in shelter it sails back at the first hour h
    from which the passage (hours h..a-1, a = h + P) and a critical lift of `tc` hours from its arrival (hours
    a..a+tc-1) can be made with Hs at the site at or below the working limit through the lift and at or below the
    station-keeping limit from h to a. On arrival it lies at a free heavy-lift berth, first come first served; when
    every heavy-lift berth there is taken, `conflict` decides what it does:
      'moorings'  - goes on to the storm moorings (the practice the past records show)
      'ignore'    - berths anyway (the berth count read as no limit)
      'anchorage' - waits off the port until a berth frees
      'nearest'   - goes on to the nearest other port with a free heavy-lift berth (else waits off the port)
    Downtime is every hour in the vessel's window from the hour it leaves the site to the last hour before it is back
    at the site, and every hour at the site with Hs above the working limit. `active` = {site: (first, end)} hours
    limits each vessel's window (a vessel leaves any berth it holds when its window ends). Returns downtime hours per
    site, the event list (site, kind, hour, place) with log=True, and per-hour (state, place) with trace=True."""
    rl = {s: runlen_below(hs[s], lw) for s in sites}
    st = {s: None for s in sites}; until = {s: 0 for s in sites}; where = {s: None for s in sites}
    held = {p: [] for p in PORTS}
    down = {s: 0 for s in sites}; ev = []
    tr = {s: [None] * (start + horizon) for s in sites} if trace else None

    def at_site(s, h):
        home = SHELTER[s]
        if hs[s][h: h + PASSAGE[s][home] + 1 + margin].max() > ls:
            st[s] = "out"; until[s] = h + PASSAGE[s][home]; where[s] = home
            if log:
                ev.append((s, "depart", h, home))
            return ("TRN", home)
        if hs[s][h] > lw:
            return ("WOW", s)
        return ("INST", s)

    for h in range(start, start + horizon):
        # first, vessels that sail from shelter this hour leave their berths (a berth left at the start of an hour is
        # free to a vessel arriving in that hour, whatever order the sites are taken in)
        for s in sites:
            a0, a1 = active[s] if active else (start, start + horizon)
            if a0 <= h < a1 and st[s] == "port":
                port = where[s].split("@")[0]
                a = h + PASSAGE[s][port]
                if a + tc <= len(hs[s]) and rl[s][a] >= tc and hs[s][h: a + 1].max() <= ls:
                    if s in held[port]:
                        held[port].remove(s)
                    st[s] = "back"; until[s] = a
                    if log:
                        ev.append((s, "sail", h, port))
        for s in sites:
            a0, a1 = active[s] if active else (start, start + horizon)
            if h < a0 or h >= a1:
                if st[s] is not None and h >= a1:
                    for p in held:
                        if s in held[p]:
                            held[p].remove(s)
                    st[s] = None
                continue
            if st[s] is None:
                st[s] = "site"
            home = SHELTER[s]
            if st[s] == "back" and h >= until[s]:
                st[s] = "site"
                if log:
                    ev.append((s, "on_station", h, None))
            if st[s] == "site":
                rec = at_site(s, h)
            elif st[s] == "out":
                rec = ("TRN", home)
                if h >= until[s]:
                    cap = PORTS[home]["heavy_lift_berths"]
                    if conflict == "ignore" or len(held[home]) < cap:
                        held[home].append(s); st[s] = "port"; where[s] = home; kind = "berth"; rec = ("SHEL", home)
                    elif conflict == "moorings":
                        st[s] = "cont"; until[s] = h + PORT_PASSAGE[home][STORM_MOORINGS]; where[s] = STORM_MOORINGS
                        kind = "continue"; rec = ("TRN", STORM_MOORINGS)
                    elif conflict == "anchorage":
                        st[s] = "port"; where[s] = home + "@anch"; kind = "anchor"; rec = ("SHEL", home)
                    else:
                        opts = sorted((PORT_PASSAGE[home][p], p) for p in PORTS
                                      if p != home and PORTS[p]["heavy_lift_berths"] > len(held[p]))
                        if opts:
                            where[s] = opts[0][1]; held[where[s]].append(s); st[s] = "cont"
                            until[s] = h + PORT_PASSAGE[home][where[s]]; kind = "continue"; rec = ("TRN", where[s])
                        else:
                            st[s] = "port"; where[s] = home + "@anch"; kind = "anchor"; rec = ("SHEL", home)
                    if log:
                        ev.append((s, "arrive_" + kind, h, where[s]))
            elif st[s] == "cont":
                rec = ("TRN", where[s])
                if h >= until[s]:
                    st[s] = "port"; rec = ("SHEL", where[s])
                    if log:
                        ev.append((s, "arrive_onward", h, where[s]))
            elif st[s] == "port":
                if where[s].endswith("@anch") and len(held[home]) < PORTS[home]["heavy_lift_berths"]:
                    held[home].append(s); where[s] = home
                    if log:
                        ev.append((s, "berth_from_anchorage", h, home))
                rec = ("SHEL", where[s].split("@")[0])
            else:   # back, under way to the site
                rec = ("TRN", s)
            if rec[0] != "INST":
                down[s] += 1
            if trace:
                tr[s][h] = rec
    return down, ev, tr


def campaign(hs, floating, conflict="moorings", **kw):
    """Downtime hours per floating site for one winter, every floating vessel replayed jointly."""
    d, _, _ = replay(hs, floating, conflict=conflict, **kw)
    return d


def avoided_by_placement(hcw, conflict="moorings", winters=None, **kw):
    """Mean over winters of the campaign's floating-vessel downtime avoided by the jack-up at each site:
    all five floating, less the four floating with the jack-up at the site. Days."""
    idx = range(len(WINTERS)) if winters is None else winters
    tot = {s: [] for s in SITES}; own = {s: [] for s in SITES}
    for w in idx:
        hs = {s: hcw[s][w] for s in SITES}
        allf = campaign(hs, SITES, conflict, **kw)
        A = sum(allf.values())
        for s in SITES:
            rest = [x for x in SITES if x != s]
            d = campaign(hs, rest, conflict, **kw)
            tot[s].append(A - sum(d.values()))
            own[s].append(allf[s])
    return ({s: float(np.mean(v)) / 24 for s, v in tot.items()},
            {s: float(np.mean(v)) / 24 for s, v in own.items()})


# ---------------------------------------------------------------- the past campaigns, as they ran
# winter -> {"floating": {site: (vessel, first_hour, end_hour)}, "jackup": (site, first_hour, end_hour)}
D = 24
PAST = {
    2023: {"floating": {"SKG": ("NM Havorn", 0, H), "LVB": ("NM Terne", 0, H), "OSR": ("NM Lomvie", 12 * D + 6, H)},
           "jackup": ("MOF", 0, H)},
    2024: {"floating": {"SKG": ("NM Terne", 0, 110 * D + 18), "LVB": ("NM Mallemuk", 0, H), "MOF": ("NM Lomvie", 0, H),
                        "FJH": ("NM Havorn", 3 * D + 14, H)},
           "jackup": ("OSR", 0, H)},
    2025: {"floating": {"SKG": ("NM Havorn", 0, H), "LVB": ("NM Terne", 5 * D + 9, H), "OSR": ("NM Mallemuk", 0, H),
                        "FJH": ("NM Lomvie", 0, 94 * D + 12)},
           "jackup": ("MOF", 0, 106 * D + 20)},
}
FLEET_2026 = {"SKG": "NM Havorn", "LVB": "NM Terne", "OSR": "NM Lomvie", "MOF": "NM Mallemuk", "FJH": "NM Ederfugl"}


def past_traces(hcw):
    """Each past winter replayed as it ran (the 'moorings' practice): {winter: (traces, events, downtime)}."""
    out = {}
    for y, cfg in PAST.items():
        w = WINTERS.index(y)
        hs = {s: hcw[s][w] for s in SITES}
        fl = cfg["floating"]
        sites = [s for s in SITES if s in fl]
        active = {s: (fl[s][1], fl[s][2]) for s in sites}
        d, ev, tr = replay(hs, sites, "moorings", log=True, active=active, trace=True)
        out[y] = (tr, ev, d)
    return out


def per_site_alone(hcw, winters=None, **kw):
    idx = range(len(WINTERS)) if winters is None else winters
    out = {s: [] for s in SITES}
    for w in idx:
        hs = {s: hcw[s][w] for s in SITES}
        for s in SITES:
            out[s].append(campaign(hs, [s], **kw)[s])
    return {s: float(np.mean(v)) / 24 for s, v in out.items()}
