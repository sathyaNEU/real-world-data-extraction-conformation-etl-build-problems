"""task197 pack builder. Writes target/, golden/ and figures.json from core.py's arrays."""
import sys, os, json, csv, sqlite3, shutil, datetime as dt
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim, core, time
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")

AS_OF = sim.AS_OF
FILING_DUE = dt.date(2026, 10, 23)
DELIVERY_MONTH = "November 2026"
ORG = "Veerkracht Flex"
TSO = "Rijksnet"

# Mid-block reserve unavailability the control platform logged, as
# (site, local date, preferred local start HH:MM, minutes, reason, code, stamp, want_over).
#   stamp "local": start_local carries the local wall clock, 90 s before logged_utc, as the alarm
#                  handler writes it.
#   stamp "utc":   the operator-interface handler stamped the field from the UTC clock and the
#                  export appended the house offset, so the field reads two hours early. The file's
#                  own logged_utc is 90 s after the start on every row the alarm handler wrote and
#                  7,290 s after it on these.
#   want_over:     the placed window must cover the extreme second of at least one qualifying
#                  over-frequency episode the site was contracted for, and the two-hour-early
#                  reading of the same row must cover none.
# No window, read either way, may hold a qualifying under-frequency second: that is what keeps
# every ask device out of the main call's population, and checks.py asserts the count is zero.
UNAVAIL = [
    # (site, local date, delivery block, preferred local start, minutes, reason, code,
    #  stamp, want_over, cross)
    # --- rows the alarm handler wrote: start_local is the local wall clock ---------------------
    ("VKF-OOS", dt.date(2026, 9, 23), 2, "05:12", 38, "droop controller alarm, reserve withdrawn", "ALM-DRP", "local", False, False),
    ("VKF-HGZ", dt.date(2026, 9, 30), 6, "20:35", 74, "engine 3 trip, reserve capacity reduced", "ENG-TRP", "local", False, False),
    ("VKF-NWV", dt.date(2026, 10, 3), 2, "06:22", 29, "communications loss to control platform", "COM-LOS", "local", False, False),
    ("VKF-MPD", dt.date(2026, 9, 22), 2, "06:35", 45, "engine 1 lube oil alarm", "ENG-LUB", "local", False, False),
    ("VKF-ZWT", dt.date(2026, 10, 1), 3, "10:20", 45, "state of charge outside reserve band", "SOC-OUT", "local", False, False),
    ("VKF-TRB", dt.date(2026, 9, 25), 3, "09:30", 42, "process load locked out of reserve", "LOA-LCK", "local", False, False),
    ("VKF-DLK", dt.date(2026, 9, 27), 1, "01:30", 63, "inverter bank 2 isolated", "INV-ISO", "local", False, False),
    ("VKF-OOS", dt.date(2026, 10, 7), 4, "13:40", 47, "inverter bank 1 derated on cooling fault", "INV-DER", "local", False, False),
    ("VKF-KPV", dt.date(2026, 10, 5), 5, "17:25", 36, "cell string isolated on insulation alarm", "ISO-INS", "local", False, False),
    ("VKF-RDL", dt.date(2026, 9, 28), 5, "18:10", 48, "gas train isolation valve fault", "GAS-VLV", "local", False, False),
    # --- rows the operator interface wrote: start_local carries the UTC instant ---------------
    ("VKF-HGZ", dt.date(2026, 9, 26), 6, "20:00", 26, "engine 2 governor hunting", "ENG-GOV", "utc", True, True),
    ("VKF-OOS", dt.date(2026, 10, 2), 4, "12:00", 24, "state of charge outside reserve band", "SOC-OUT", "utc", True, True),
    ("VKF-ZWT", dt.date(2026, 10, 8), 3, "09:35", 15, "transformer cooling alarm", "TRF-COO", "utc", True, True),
    ("VKF-TRB", dt.date(2026, 10, 9), 3, "09:04", 28, "process line interlock raised", "LOA-INT", "utc", True, True),
    ("VKF-KPV", dt.date(2026, 10, 3), 5, "19:20", 30, "inverter bank 2 fan failure", "INV-FAN", "utc", True, False),
    ("VKF-NWV", dt.date(2026, 9, 24), 2, "04:00", 28, "control platform link degraded", "COM-DEG", "utc", False, True),
    ("VKF-DLK", dt.date(2026, 9, 30), 1, "00:01", 45, "inverter bank 1 isolated", "INV-IS1", "utc", False, True),
    ("VKF-RDL", dt.date(2026, 9, 23), 5, "16:00", 36, "engine 2 knock sensor fault", "ENG-KNK", "utc", False, True),
    ("VKF-DLK", dt.date(2026, 9, 22), 5, "16:05", 45, "inverter bank 3 isolated", "INV-IS3", "utc", False, True),
    # --- further alarm-handler rows: the operator interface wrote nine of the file's withdrawal
    # --- rows and the alarm handler the rest, so the mis-stamped clock is a minority of them -----
    ("VKF-NWV", dt.date(2026, 9, 27), 3, "10:40", 37, "inverter string 4 isolated", "INV-IS4", "local", False, False),
    ("VKF-TRB", dt.date(2026, 10, 6), 3, "10:10", 34, "process load recalled from reserve", "LOA-RCL", "local", False, False),
    ("VKF-ZWT", dt.date(2026, 9, 26), 3, "09:50", 30, "state of charge outside reserve band", "SOC-OUT", "local", False, False),
    ("VKF-KPV", dt.date(2026, 9, 30), 5, "17:10", 42, "cell string temperature derate", "CEL-DER", "local", False, False),
    ("VKF-DLK", dt.date(2026, 10, 4), 5, "17:40", 39, "inverter bank 4 isolated", "INV-IS4", "local", False, False),
    ("VKF-MPD", dt.date(2026, 10, 2), 2, "05:40", 51, "engine 2 coolant alarm", "ENG-COL", "local", False, False),
    ("VKF-OOS", dt.date(2026, 9, 25), 2, "06:10", 43, "droop controller restart", "ALM-DRP", "local", False, False),
    ("VKF-HGZ", dt.date(2026, 10, 8), 6, "21:40", 56, "engine 1 exhaust alarm", "ENG-EXH", "local", False, False),
    # --- three windows a later correction row cancels: the reserve was not withdrawn ----------
    ("VKF-OOS", dt.date(2026, 9, 28), 4, "13:20", 56, "reserve withdrawn, pending investigation", "ALM-DRP", "local", False, False),
    ("VKF-HGZ", dt.date(2026, 10, 2), 6, "21:10", 68, "reserve withdrawn, pending investigation", "ENG-TRP", "local", False, False),
    ("VKF-NWV", dt.date(2026, 10, 10), 3, "09:05", 33, "reserve withdrawn, pending investigation", "COM-LOS", "local", False, False),
]
SUPERSEDED = {27, 28, 29}       # indexes into UNAVAIL whose event a correction row cancels
STAMP_SHIFT = 7200              # seconds the operator-interface handler's rows read early

# The operator's minute summary ran on the SCADA chain's own one-minute average for a few short
# spans in which the one-second feed was not available to the summariser, so those rows carry that
# single value in all three columns. The deviation extracts were published afterwards from the
# quality-metering archive and carry the seconds, so for those minutes the extract reaches above
# the summary's own stated maximum. Each span is (local date, delivery block, minutes); it opens
# two minutes before the first qualifying over-frequency episode of that block on that date, and
# the last three spans fall in blocks holding no such episode, where the fallback cost nothing.
SUMMARY_HELD = [
    (dt.date(2026, 9, 23), 3, 5),
    (dt.date(2026, 9, 30), 5, 4),
    (dt.date(2026, 10, 2), 3, 4),
    (dt.date(2026, 10, 5), 5, 5),
    (dt.date(2026, 10, 4), 6, 4),
    (dt.date(2026, 9, 25), 1, 4),
    (dt.date(2026, 9, 27), 2, 3),
    (dt.date(2026, 10, 7), 1, 3),
]

# The settlement metering point in force for each site: (code, replacement code, effective date).
METER_EAN = {"VKF-OOS": ("871687140000312447", "871687140000398201", dt.date(2026, 10, 1)),
             "VKF-ZWT": ("871687140000207718", None, None), "VKF-HGZ": ("871687140000255143", None, None),
             "VKF-KPV": ("871687140000266509", None, None), "VKF-MPD": ("871687140000271882", None, None),
             "VKF-NWV": ("871687140000289064", None, None), "VKF-TRB": ("871687140000294337", None, None),
             "VKF-DLK": ("871687140000301776", None, None), "VKF-RDL": ("871687140000318095", None, None)}
KWH_SITE = "VKF-DLK"            # this meter reports in kWh, as its unit column says


def utc(d, sec):
    return core.local_to_utc(d, sec).strftime("%Y-%m-%dT%H:%M:%SZ")

def loc(d, sec):
    base = dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(sec))
    return base.strftime("%Y-%m-%dT%H:%M:%S+02:00")

def norm(d, sec):
    """A (local date, second of day) pair for a second count that may fall outside the day."""
    sec = int(sec)
    while sec < 0:
        d, sec = d - dt.timedelta(days=1), sec + sim.DAY
    while sec >= sim.DAY:
        d, sec = d + dt.timedelta(days=1), sec - sim.DAY
    return d, sec

_PLACED = {}
_PLACE_CACHE = {}
_WIN_CACHE = {}


def _mask(d, kind):
    """Seconds inside a qualifying episode of one sign on local date d, padded by two minutes."""
    key = (d, kind)
    if key not in _PLACED:
        f = sim.frequency_day(d)
        marked = np.zeros(sim.DAY, dtype=bool)
        eps = sim.qualifying_episodes(d, f) if kind == "under" else core.over_episodes(f)
        for (t0, t1, tstar, fx) in eps:
            marked[max(0, t0 - 120):min(sim.DAY, t1 + 121)] = True
        _PLACED[key] = marked
    return _PLACED[key]


def _over_extremes(d):
    """(extreme second, peak) of every qualifying over-frequency episode published on date d."""
    if ("over_ext", d) not in _PLACED:
        f = sim.frequency_day(d)
        out = []
        for (a, b) in core.extract_windows(f):
            seg = np.full(len(f), 50.0)
            seg[a:b + 1] = f[a:b + 1]
            for (t0, t1, tstar, fx) in core.over_episodes(seg):
                if a <= tstar <= b:
                    out.append((tstar, fx))
        _PLACED[("over_ext", d)] = sorted(set(out))
    return _PLACED[("over_ext", d)]


def _over_hits(site, d, lo, hi):
    """Qualifying over-frequency episodes the site was contracted for whose extreme second falls in
    [lo, hi): the obligations a withdrawal over that window removes."""
    out = []
    for (tstar, fx) in _over_extremes(d):
        if lo <= tstar < hi and sim.contracted(site, np.array([float(tstar)]), d)[0]:
            out.append(tstar)
    return out


def place_outage(site, d, block, hhmm, minutes, stamp, want_over, cross):
    key = (site["id"], d, block, hhmm, minutes, stamp, want_over, cross)
    if key not in _PLACE_CACHE:
        _PLACE_CACHE[key] = _place_outage(site, d, block, hhmm, minutes, stamp, want_over, cross)
    return _PLACE_CACHE[key]


def _under_clear(d, lo, hi):
    """True when no second of [lo - 60, hi + 60) lies in a qualifying under-frequency episode,
    rolling across local dates. This is the separation between the ask devices and the main call:
    neither a window's true place nor the place its own row reads may touch the call's population."""
    lo, hi = lo - 60, hi + 60
    while lo < hi:
        dd, ss = norm(d, lo)
        n = min(hi - lo, sim.DAY - ss)
        if sim.WINDOW_START <= dd <= sim.WINDOW_END and _mask(dd, "under")[ss:ss + n].any():
            return False
        lo += n
    return True


def _place_outage(site, d, block, hhmm, minutes, stamp, want_over, cross):
    """The start second of the logged window, searched inside the stated delivery block outward
    from the stated time. A row the operator interface wrote must change delivery block when it is
    read two hours early, or the device moves no block figure, and a row that carries an
    over-frequency obligation must cover one at its true place and none at the place it reads."""
    need = minutes * 60
    shift = STAMP_SHIFT if stamp == "utc" else 0
    lo_b, hi_b = sim.BLOCK_HOURS[block - 1]
    h, m = [int(x) for x in hhmm.split(":")]
    pref = h * 3600 + m * 60
    cand = sorted(range(lo_b * 3600, hi_b * 3600 - need + 1, 60), key=lambda t: (abs(t - pref), t))
    for t in cand:
        if t - 60 < 0 or t + need + 60 >= sim.DAY:
            continue
        if not sim.contracted(site, np.arange(t, t + need), d).all():
            continue
        if not _under_clear(d, t, t + need):
            continue
        st0 = t - shift
        if shift:
            if not _under_clear(d, st0, st0 + need):
                continue
            if cross and st0 >= 0 and st0 // 14400 == t // 14400:
                continue
            sd, ss = norm(d, st0)
            n_stamp = len(_over_hits(site, sd, ss, ss + need))
        else:
            n_stamp = None
        n_true = len(_over_hits(site, d, t, t + need))
        if want_over:
            if n_true < 1 or n_stamp != 0:
                continue
        else:
            if n_true != 0 or (shift and n_stamp != 0):
                continue
        return t
    return None


def unavail_windows(site_id):
    """The windows that actually removed the obligation: the live events at their true place."""
    if site_id in _WIN_CACHE:
        return _WIN_CACHE[site_id]
    out = []
    for r in unavail_rows():
        if r["site"] != site_id or r["superseded"]:
            continue
        out.append((r["date"], r["start"], r["start"] + r["minutes"] * 60))
    _WIN_CACHE[site_id] = out
    return out


def unavail_rows():
    """Every logged reserve-unavailability event, placed, including the superseded ones. `start` is
    the true start second; `stamp_start` is the second the row's start_local field reads as."""
    if "rows" in _WIN_CACHE:
        return _WIN_CACHE["rows"]
    out = []
    for i, (sid, d0, blk, hhmm, mins, reason, code, stamp, want_over, cross) in enumerate(UNAVAIL):
        # the stated delivery date, then the nearest dates either side: the window has to sit in a
        # block the site is committed to and clear of the call's population, which not every date
        # allows. The order is fixed, so the pack rebuilds byte for byte.
        d, t0 = None, None
        for k in [0] + [v for j in range(1, 11) for v in (j, -j)]:
            cd = d0 + dt.timedelta(days=k)
            if not (sim.WINDOW_START <= cd <= sim.WINDOW_END):
                continue
            t = place_outage(sim.SITE_BY_ID[sid], cd, blk, hhmm, mins, stamp, want_over, cross)
            if t is not None:
                d, t0 = cd, t
                break
        if t0 is None:
            raise AssertionError("no placement for %s %s block %d %s" % (sid, d0, blk, hhmm))
        out.append(dict(idx=i, site=sid, date=d, block=blk, start=t0, minutes=mins, reason=reason,
                        code=code, stamp=stamp, want_over=want_over,
                        stamp_start=t0 - (STAMP_SHIFT if stamp == "utc" else 0),
                        superseded=(i in SUPERSEDED)))
    _WIN_CACHE["rows"] = out
    return out


def fcr_active(site, d, t):
    """Contracted and not withdrawn from reserve: the seconds the site owed a response."""
    ok = sim.contracted(site, t, d)
    for (dd, a, b) in unavail_windows(site["id"]):
        if dd == d:
            ok = ok & ~((np.asarray(t) >= a) & (np.asarray(t) < b))
    return ok


def scope_gate(site, d, tstar):
    """clause 2's scope: the parts of a delivery block the site was withdrawn from reserve for."""
    return bool(fcr_active(site, d, np.array([float(tstar)]))[0])


def stamp_scope_gate(site, d, tstar):
    """clause 2's scope as a response reading start_local at face value would apply it: the window
    of every live event placed where its own row says, not where the platform's log clock puts it."""
    for r in unavail_rows():
        if r["site"] != site["id"] or r["superseded"]:
            continue
        sd, ss = norm(r["date"], r["stamp_start"])
        if sd == d and ss <= tstar < ss + r["minutes"] * 60:
            return False
    return True


def capture_events():
    """(site, local date, local second, trigger) for every logged event the platform took a high
    resolution capture around: the alarms and reserve withdrawals, and the mode changes and manual
    overrides. Read from the same event list the control platform's log is written from, so the two
    files agree on when each event happened. Events before the archive's window are dropped."""
    import pack2
    kind = {"alarm": "ALARM", "mode": "MODE", "setpoint": "MODE"}
    out = []
    for (logged, site, typ, code, detail) in pack2.BENCH:
        if typ not in kind:
            continue
        t = dt.datetime.strptime(logged, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=2)
        d = t.date()
        if not (sim.WINDOW_START <= d <= sim.WINDOW_END):
            continue
        out.append((site, d, (t - dt.datetime(d.year, d.month, d.day)).seconds, kind[typ]))
    for r in unavail_rows():
        out.append((r["site"], r["date"], r["start"], "ALARM"))
    out.sort(key=lambda x: (x[1], x[0], x[2]))
    return out


def held_minutes():
    """Every (local date, local minute) the operator's minute summary carries the SCADA chain's
    one-minute average in all three columns. A span opens two minutes before the first qualifying
    over-frequency episode of its delivery block on that date, and half an hour into the block
    where there is none."""
    out = set()
    for (d, blk, n) in SUMMARY_HELD:
        lo_h, hi_h = sim.BLOCK_HOURS[blk - 1]
        first = None
        for (tstar, fx) in _over_extremes(d):
            if lo_h * 3600 <= tstar < hi_h * 3600:
                first = tstar // 60
                break
        m0 = (first - 2) if first is not None else lo_h * 60 + 30
        for k in range(n):
            m = m0 + k
            if 0 <= m < 1440:
                out.add((d, m))
    return out


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def main():
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    if os.path.isdir(GOLD):
        shutil.rmtree(GOLD)
    os.makedirs(TGT); os.makedirs(GOLD)
    counts = {}

    # patch sim's FCR gate so unavailability removes the obligation, before anything is computed,
    # and clause 2's scope gate so a withdrawn part of a block is out of the measured population
    sim._fcr_gate = fcr_active
    core._scope_gate = scope_gate
    print("[stage] window", flush=True)
    W = core.window()
    print("[stage] recordings", flush=True)
    recs = core.recordings(W, capture_events())
    print("[stage] power cache", flush=True)
    cache = core.power_cache(W, recs)

    # ---------- the 1 Hz archive -------------------------------------------------------------
    print("[stage] archive", flush=True)
    dbp = os.path.join(TGT, "platform", "vkf_highres_archive.sqlite")
    os.makedirs(os.path.dirname(dbp), exist_ok=True)
    con = sqlite3.connect(dbp)
    con.execute("PRAGMA page_size=4096")
    con.execute("""CREATE TABLE recording (recording_id INTEGER PRIMARY KEY, site_id TEXT NOT NULL,
        trigger TEXT NOT NULL, start_utc TEXT NOT NULL, end_utc TEXT NOT NULL, samples INTEGER NOT NULL)""")
    con.execute("""CREATE TABLE power_1s (recording_id INTEGER NOT NULL, ts_utc TEXT NOT NULL,
        p_mw REAL NOT NULL, quality TEXT NOT NULL)""")
    rid, rows_written, dup_src = 0, 0, None
    archive_index = {}
    for (d, sid, trig, lo, hi) in recs:
        rid += 1
        P = cache[(d, sid, lo)]
        archive_index[(d, sid, lo)] = rid
        samples = []
        rq = sim._rng("qual", sid, d.isoformat(), lo)
        for i, t in enumerate(range(lo, hi)):
            q = "M"
            if rq.random_sample() < 0.004:
                q = "E"
            samples.append((rid, utc(d, t), round(float(P[i]), 3), q))
        con.execute("INSERT INTO recording VALUES (?,?,?,?,?,?)",
                    (rid, sid, trig, utc(d, lo), utc(d, hi - 1), len(samples)))
        con.executemany("INSERT INTO power_1s VALUES (?,?,?,?)", samples)
        rows_written += len(samples)
        # the replayed recording: one over-frequency extract restored twice under a fresh id
        # the storage-fault restore of 2026-10-04 put one over-frequency recording back under a
        # fresh id; it holds no qualifying under-frequency episode, so the main call cannot see it
        if dup_src is None and trig == "FREQ-DEV" and sid == "VKF-HGZ" \
                and d == dt.date(2026, 10, 4) \
                and any(lo <= x < hi for (_, _, x, _) in W[d]["over"]) \
                and not any(lo <= x < hi for (_, _, x, _) in W[d]["under"]):
            dup_src = (rid, sid, trig, lo, hi, d, samples)
    if dup_src:
        (src_id, sid, trig, lo, hi, d, samples) = dup_src
        rid += 1
        con.execute("INSERT INTO recording VALUES (?,?,?,?,?,?)",
                    (rid, sid, trig, utc(d, lo), utc(d, hi - 1), len(samples)))
        con.executemany("INSERT INTO power_1s VALUES (?,?,?,?)",
                        [(rid, s[1], s[2], s[3]) for s in samples])
        rows_written += len(samples)
    con.commit()
    con.execute("VACUUM")
    con.close()
    counts["archive_recordings"] = rid
    counts["archive_rows"] = rows_written

    # ---------- the operator's frequency files ----------------------------------------------
    print("[stage] frequency files", flush=True)
    rows, mins = [], []
    for d in sim.dates():
        f = W[d]["f"]
        for k, (a, b) in enumerate(W[d]["exc"], start=1):
            eid = "%s-%02d" % (d.strftime("%Y%m%d"), k)
            for t in range(a, b + 1):
                rows.append((eid, utc(d, t), round(float(f[t]), 4)))
        held = held_minutes()
        for m in range(1440):
            seg = f[m * 60:(m + 1) * 60]
            if (d, m) in held:
                # the summariser fell back to the SCADA chain's own one-minute average for these
                # minutes, so the row carries the mean and nothing else: one sample a minute has
                # no minimum or maximum to publish and both columns go out empty
                mins.append((utc(d, m * 60), "", round(float(seg.mean()), 4), ""))
            else:
                mins.append((utc(d, m * 60), round(float(seg.min()), 4), round(float(seg.mean()), 4),
                             round(float(seg.max()), 4)))
    counts["freq_1s"] = write_csv(os.path.join(TGT, "operator", "system_frequency_1s_extracts.csv"),
                                  ["extract_id", "ts_utc", "frequency_hz"], rows)
    counts["freq_min"] = write_csv(os.path.join(TGT, "operator", "system_frequency_minute_summary.csv"),
                                   ["minute_utc", "frequency_min_hz", "frequency_mean_hz", "frequency_max_hz"], mins)

    # ---------- programme, commitments, metered volumes --------------------------------------
    print("[stage] programme and metered", flush=True)
    prog_rows, met_rows, com_rows = [], [], []
    for d in sim.dates():
        for s in sim.SITES:
            prog = W[d]["prog"][s["id"]]
            for p in range(96):
                prog_rows.append((s["id"], loc(d, p * 900), p + 1, round(float(prog[p]), 3)))
            mw = core.metered(W, d, s["id"])
            unit = "kWh" if s["id"] == KWH_SITE else "MWh"
            scale = 1000.0 if unit == "kWh" else 1.0
            ean = METER_EAN[s["id"]]
            # The meter data platform stamps each interval with the instant it closes and derives
            # the period index from that instant, so the row carrying the interval 00:00 to 00:15
            # is stamped 00:15 and indexed 2. The export covers the intervals that closed inside
            # the window, which is the window's 2,016 intervals per metering point, no more.
            for p in range(96):
                dd, ss = norm(d, (p + 1) * 900)
                if dd > sim.WINDOW_END + dt.timedelta(days=1):
                    continue
                code = ean[0]
                if ean[1] and core.local_to_utc(d, p * 900).date() >= ean[2]:
                    code = ean[1]
                met_rows.append((code, loc(dd, ss), ss // 900 + 1,
                                 round(float(mw[p]) * scale, 4), unit))
            for b in sim.commitments(s, d):
                lo_h, hi_h = sim.BLOCK_HOURS[b]
                com_rows.append((d.isoformat(), b + 1, "%02d:00" % lo_h, "%02d:00" % hi_h, s["id"],
                                 round(s["cap"], 2)))
    com_rows.sort(key=lambda r: (r[0], r[1], r[4]))
    met_rows.sort(key=lambda r: (r[0], r[1]))
    counts["programme"] = write_csv(os.path.join(TGT, "platform", "site_programme_15min.csv"),
                                    ["site_id", "period_start_local", "settlement_period", "programme_mw"], prog_rows)
    counts["metered"] = write_csv(os.path.join(TGT, "settlement", "metered_volumes_15min.csv"),
                                  ["metering_point", "interval_ts_local", "settlement_period", "net_volume", "unit"], met_rows)
    counts["commitments"] = write_csv(os.path.join(TGT, "platform", "fcr_block_commitments.csv"),
                                      ["delivery_date", "block", "block_start_local", "block_end_local",
                                       "site_id", "committed_mw"], com_rows)
    # ---------- documents, register, settlement, distractors --------------------------------
    print("[stage] documents", flush=True)
    import docs, pack2, goldens
    placed = unavail_rows()
    counts["event_log"] = pack2.event_log(os.path.join(TGT, "platform", "control_platform_event_log.csv"), placed)
    pack2.register(os.path.join(TGT, "register", "asset_register.xlsx"))
    docs.technical_conditions(os.path.join(TGT, "operator", "fcr_technical_conditions_2026.pdf"), TSO)
    docs.performance_standard(os.path.join(TGT, "standards", "reserve_performance_standard_v4.pdf"),
                              ORG, core.TOLERANCE_PCT, sim.WINDOW_START, sim.WINDOW_END, AS_OF)
    st = pack2.settlement_files(TGT, W)
    counts["settlement_statements"] = sum(st["rows"])
    counts["imbalance_prices"], counts["auction_results"] = pack2.distractors(TGT)
    counts["prequalification"] = pack2.prequal(TGT)

    # ---------- the figures -------------------------------------------------------------------
    print("[stage] figures", flush=True)
    under = core.episode_table(W, recs, cache, "under")
    over = core.episode_table(W, recs, cache, "over")
    su, so = core.site_scores(under), core.site_scores(over)
    # the same over-frequency table as a response reading start_local at face value builds it, and
    # as a response that also stopped at the undisturbed level reads it: both are ask-layer
    # measurements, printed into figures.json so ceiling.py scores two real readings
    _g = core._scope_gate
    try:
        core._scope_gate = stamp_scope_gate
        so_stamp = core.site_scores(core.episode_table(W, recs, cache, "over"))
    finally:
        core._scope_gate = _g
    av = pack2.availability(W, placed, "golden")
    av_c = pack2.availability(W, placed, "cracker")
    av_m = pack2.availability(W, placed, "mirror")
    adh = pack2.adherence(W, "golden")
    adh_n = pack2.adherence(W, "natural")
    name = {s["id"]: s["name"] for s in sim.SITES}
    cap = {s["id"]: s["cap"] for s in sim.SITES}
    order = [sid for sid, _ in core.ranked(su, "traj")]
    sc = [dict(site=sid, name=name[sid], cap=round(cap[sid], 2),
               contract_gain=round(cap[sid] / sim.SPAN, 2), gain_pct=round(su[sid]["traj"]),
               episodes=su[sid]["n"], under=round(su[sid]["traj"]) < core.TOLERANCE_PCT)
          for sid in order]
    call, runner = order[0], order[1]
    down = [dict(site=sid, name=name[sid],
                 gain_pct=(round(so[sid]["traj"]) if sid in so else None),
                 episodes=(so[sid]["n"] if sid in so else 0)) for sid in sorted(name)]
    dn_low = min([d for d in down if d["gain_pct"] is not None], key=lambda d: d["gain_pct"])
    dn_none = [d for d in down if d["gain_pct"] is None]
    blocks = [dict(block=b, hours="%02d:00-%02d:00" % sim.BLOCK_HOURS[b - 1],
                   committed=round(av["committed"][b], 1), available=round(av["available"][b], 1),
                   shortfall=round(av["lost"][b], 1)) for b in range(1, 7)]
    exposure = [dict(site=sid, name=name[sid], above=round(adh["above"][sid], 1),
                     below=round(adh["below"][sid], 1)) for sid in sorted(name)]
    rung0_site = core.ranked(su, "pre")[0][0]
    F = dict(window_from=sim.WINDOW_START.isoformat(), window_to=sim.WINDOW_END.isoformat(),
             as_of=AS_OF.isoformat(), filing_due=FILING_DUE.isoformat(),
             delivery_month=DELIVERY_MONTH, delivery_start="2026-11-01", tso=TSO, org=ORG,
             tolerance=core.TOLERANCE_PCT, scorecard=sc, down=down, availability=blocks,
             exposure=exposure, call_site=call, call_name=name[call],
             call_gain=round(su[call]["traj"]), runner_site=runner, runner_name=name[runner],
             runner_gain=round(su[runner]["traj"]),
             gap_pp=round(su[runner]["traj"]) - round(su[call]["traj"]),
             call_episodes=su[call]["n"],
             down_low_name=dn_low["name"], down_low_gain=dn_low["gain_pct"],
             down_none_name=(dn_none[0]["name"] if dn_none else "none"),
             exposure_above_total=round(adh["above_total"], 1),
             exposure_below_total=round(adh["below_total"], 1),
             rung0_site=rung0_site, rung0_name=name[rung0_site],
             rung0_pre=round(su[rung0_site]["pre"], 1), rung0_traj=round(su[rung0_site]["traj"]),
             ladder={k: {sid: round(v[k], 4) for sid, v in su.items()} for k in ("traj", "pre", "sp", "lin")},
             ladder_names={k: core.ranked(su, k)[0][0] for k in ("traj", "pre", "sp", "lin")},
             exact={sid: round(v["traj"], 6) for sid, v in su.items()},
             exact_down={sid: round(v["traj"], 6) for sid, v in so.items()},
             forcing=dict(
                 # ask B, the clock device: the block shortfall the natural read misplaces
                 clock_blocks={b: round(av["lost"][b] - av_c["lost"][b], 1) for b in range(1, 7)},
                 clock_moved_mwh=round(sum(abs(av["lost"][b] - av_c["lost"][b])
                                           for b in range(1, 7)), 1),
                 clock_rows=sum(1 for r in placed if r["stamp"] == "utc"),
                 # ask C, the interval-index device
                 adh_above_natural=round(adh_n["above_total"], 1),
                 adh_below_natural=round(adh_n["below_total"], 1),
                 adh_natural_site={sid: [round(adh_n["above"][sid], 1), round(adh_n["below"][sid], 1)]
                                   for sid in sorted(name)},
                 # ask A, the held summary rows and the over-frequency obligations withdrawn
                 held_minutes=len(held_minutes()),
                 over_withdrawn=sum(1 for r in placed if r["want_over"]),
                 # the documented mess that moves the mirror and not the cracker
                 superseded_mwh=round(sum(av_m["lost"][b] - av_c["lost"][b]
                                          for b in range(1, 7)), 1),
                 ean_lost_mwh=round(st["ean_lost_mwh"], 1),
                 prelim_gap_mwh=round(st["prelim_gap_mwh"], 3),
                 kwh_site=KWH_SITE,
                 # ask A read with the start_local field at face value, and on rung 0's baseline
                 down_gain_stamped={sid: round(v["traj"]) for sid, v in so_stamp.items()},
                 down_episodes_stamped={sid: v["n"] for sid, v in so_stamp.items()},
                 down_gain_rung0={sid: round(v["pre"]) for sid, v in so.items()
                                  if v.get("pre") == v.get("pre")}),
             counts=counts)
    print("[stage] dictionary and goldens", flush=True)
    counts["dictionary"] = pack2.dictionary(TGT, counts)
    # September's own contracted mean per block. These are NOT derived from the review window: the
    # window's commitments averaged over a notional 30 days gave a column that included eleven October
    # dates and omitted 1 to 20 September, and a reader recovered the arithmetic exactly from the
    # shipped commitments file (140/30 = 4.67 and so on). The pack ships only the review window, so a
    # September statement legitimately carries figures this pack cannot reconstruct.
    SEP_MEAN_MW = {1: 5.12, 2: 9.08, 3: 12.41, 4: 3.47, 5: 12.95, 6: 2.63}
    blk = [("Block %d (%02d:00-%02d:00)" % (b, sim.BLOCK_HOURS[b - 1][0], sim.BLOCK_HOURS[b - 1][1]),
            SEP_MEAN_MW[b], 99.14 - 0.37 * (b - 1) + 0.11 * ((b - 1) % 3))
           for b in range(1, 7)]
    docs.availability_report(os.path.join(TGT, "operator", "fcr_group_availability_2026-09.pdf"),
                             TSO, ORG, "2026-09", blk, "RPG-0417")
    goldens.workbook(os.path.join(GOLD, "site_response_scorecard.xlsx"), F)
    goldens.memo(os.path.join(GOLD, "response_determination.md"), F)
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(counts, open(os.path.join(HERE, "_counts.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: counts[k] for k in sorted(counts)}, indent=1))
    print("call %s %.1f | runner %s %.1f | gap %.1f" % (F["call_name"], F["call_gain"],
                                                        F["runner_name"], F["runner_gain"], F["gap_pp"]))
    print("rungs:", F["ladder_names"])
    return W, recs, cache, archive_index


if __name__ == "__main__":
    main()
