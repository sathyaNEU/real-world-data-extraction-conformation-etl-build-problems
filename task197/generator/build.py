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
    ("VKF-OOS", dt.date(2026, 9, 23), "05:12", 38, "droop controller alarm, reserve withdrawn", "ALM-DRP", "local", False),
    ("VKF-HGZ", dt.date(2026, 9, 30), "20:35", 74, "engine 3 trip, reserve capacity reduced", "ENG-TRP", "local", False),
    ("VKF-NWV", dt.date(2026, 10, 3), "06:22", 29, "communications loss to control platform", "COM-LOS", "local", False),
    ("VKF-MPD", dt.date(2026, 9, 22), "06:35", 44, "engine 1 lube oil alarm", "ENG-LUB", "local", False),
    ("VKF-ZWT", dt.date(2026, 10, 1), "10:20", 52, "state of charge outside reserve band", "SOC-OUT", "local", False),
    ("VKF-TRB", dt.date(2026, 9, 25), "09:30", 41, "process load locked out of reserve", "LOA-LCK", "local", False),
    ("VKF-DLK", dt.date(2026, 9, 27), "01:30", 63, "inverter bank 2 isolated", "INV-ISO", "local", False),
    ("VKF-OOS", dt.date(2026, 10, 7), "13:40", 47, "inverter bank 1 derated on cooling fault", "INV-DER", "local", False),
    ("VKF-KPV", dt.date(2026, 10, 5), "17:25", 36, "cell string isolated on insulation alarm", "ISO-INS", "local", False),
    ("VKF-RDL", dt.date(2026, 9, 23), "18:10", 55, "gas train isolation valve fault", "GAS-VLV", "local", False),
    # the operator-interface handler's rows
    ("VKF-HGZ", dt.date(2026, 10, 7), "20:40", 58, "engine 2 governor hunting", "ENG-GOV", "utc", True),
    ("VKF-KPV", dt.date(2026, 9, 28), "16:35", 42, "inverter bank 2 fan failure", "INV-FAN", "utc", True),
    ("VKF-ZWT", dt.date(2026, 10, 9), "08:30", 49, "transformer cooling alarm", "TRF-COO", "utc", True),
    ("VKF-NWV", dt.date(2026, 9, 26), "04:35", 33, "control platform link degraded", "COM-DEG", "utc", True),
    ("VKF-TRB", dt.date(2026, 10, 2), "08:50", 37, "process line interlock raised", "LOA-INT", "utc", True),
    ("VKF-DLK", dt.date(2026, 10, 8), "16:20", 51, "inverter bank 3 isolated", "INV-IS3", "utc", True),
    ("VKF-RDL", dt.date(2026, 9, 30), "16:45", 44, "engine 2 knock sensor fault", "ENG-KNK", "utc", True),
    ("VKF-OOS", dt.date(2026, 10, 8), "12:30", 39, "state of charge outside reserve band", "SOC-OUT", "utc", True),
    ("VKF-DLK", dt.date(2026, 10, 9), "01:10", 46, "inverter bank 1 isolated", "INV-IS1", "utc", False),
    # three entries a later correction row cancels: the window was logged against a site that had
    # not in fact been withdrawn
    ("VKF-OOS", dt.date(2026, 9, 28), "13:20", 56, "reserve withdrawn, pending investigation", "ALM-DRP", "local", False),
    ("VKF-HGZ", dt.date(2026, 10, 2), "21:10", 68, "reserve withdrawn, pending investigation", "ENG-TRP", "local", False),
    ("VKF-NWV", dt.date(2026, 10, 10), "09:05", 33, "reserve withdrawn, pending investigation", "COM-LOS", "local", False),
]
SUPERSEDED = {19, 20, 21}       # indexes into UNAVAIL whose event a correction row cancels
STAMP_SHIFT = 7200              # seconds the operator-interface handler's rows read early

# The operator's minute summary ran on the SCADA chain's own one-minute average for a few short
# spans in which the one-second feed was not available to the summariser, so those rows carry that
# single value in all three columns. The deviation extracts were published afterwards from the
# quality-metering archive and carry the seconds. Each span is given as (local date, first local
# minute, minutes); none may hold a second at or below 49.920 Hz.
SUMMARY_HELD = [
    (dt.date(2026, 9, 21), 616, 4),
    (dt.date(2026, 9, 23), 1171, 5),
    (dt.date(2026, 9, 29), 721, 4),
    (dt.date(2026, 10, 2), 676, 4),
    (dt.date(2026, 10, 6), 1246, 5),
    (dt.date(2026, 10, 10), 1186, 4),
]

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


def place_outage(site, d, hhmm, minutes, stamp, want_over):
    key = (site["id"], d, hhmm, minutes, stamp, want_over)
    if key not in _PLACE_CACHE:
        _PLACE_CACHE[key] = _place_outage(site, d, hhmm, minutes, stamp, want_over)
    return _PLACE_CACHE[key]


def _place_outage(site, d, hhmm, minutes, stamp, want_over):
    """The start second of the logged window, searched outward from the stated time. Every
    candidate must sit wholly inside a contracted block, and neither the true window nor its
    two-hour-early reading may come within two minutes of a qualifying under-frequency episode:
    that is the separation between the ask devices and the main call. A row the operator-interface
    handler wrote must also cross a block boundary when read two hours early, or the device moves
    no block figure, and must cover an over-frequency obligation at its true place and none at the
    place it reads."""
    under = _mask(d, "under")
    need = minutes * 60
    shift = STAMP_SHIFT if stamp == "utc" else 0
    h, m = [int(x) for x in hhmm.split(":")]
    pref = h * 3600 + m * 60
    cand = sorted(range(0, sim.DAY - need, 60), key=lambda t: (abs(t - pref), t))
    for t in cand:
        if t - 60 < 0 or t + need + 60 >= sim.DAY:
            continue
        if not sim.contracted(site, np.arange(t, t + need), d).all():
            continue
        if under[t - 60:t + need + 60].any():
            continue
        st0, st1 = t - shift, t + need - shift
        if shift:
            if st0 - 60 < 0:
                continue
            if under[st0 - 60:st1 + 60].any():
                continue
            if st0 // 14400 == t // 14400:          # the shifted row must change delivery block
                continue
        n_true = len(_over_hits(site, d, t, t + need))
        n_stamp = len(_over_hits(site, d, st0, st1)) if shift else n_true
        if want_over:
            if n_true < 1 or n_stamp != 0:
                continue
        else:
            if n_true != 0 or n_stamp != 0:
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
    for i, (sid, d, hhmm, mins, reason, code, stamp, want_over) in enumerate(UNAVAIL):
        t0 = place_outage(sim.SITE_BY_ID[sid], d, hhmm, mins, stamp, want_over)
        if t0 is None:
            raise AssertionError("no placement for %s %s %s" % (sid, d, hhmm))
        out.append(dict(idx=i, site=sid, date=d, start=t0, minutes=mins, reason=reason,
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


def held_minutes():
    """Every (local date, local minute) the operator's minute summary carries the SCADA chain's
    one-minute average in all three columns."""
    out = set()
    for (d, m0, n) in SUMMARY_HELD:
        for k in range(n):
            out.add((d, m0 + k))
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
    recs = core.recordings(W)
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
        if dup_src is None and trig == "frequency_excursion" and sid == "VKF-HGZ" \
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
                # the summariser fell back to the SCADA chain's own one-minute average, so all
                # three columns carry that single value
                v = round(float(seg.mean()), 4)
                mins.append((utc(d, m * 60), v, v, v))
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
    av = pack2.availability(W, placed)
    met = pack2.metered_totals(W)
    name = {s["id"]: s["name"] for s in sim.SITES}
    cap = {s["id"]: s["cap"] for s in sim.SITES}
    order = [sid for sid, _ in core.ranked(su, "traj")]
    sc = [dict(site=sid, name=name[sid], cap=round(cap[sid], 2),
               contract_gain=round(cap[sid] / sim.SPAN, 2), gain_pct=round(su[sid]["traj"], 1),
               episodes=su[sid]["n"], under=round(su[sid]["traj"], 1) < core.TOLERANCE_PCT)
          for sid in order]
    call, runner = order[0], order[1]
    down = [dict(site=sid, name=name[sid],
                 gain_pct=(round(so[sid]["traj"], 1) if sid in so else None),
                 episodes=(so[sid]["n"] if sid in so else 0)) for sid in sorted(name)]
    dn_low = min([d for d in down if d["gain_pct"] is not None], key=lambda d: d["gain_pct"])
    dn_none = [d for d in down if d["gain_pct"] is None]
    blocks = [dict(block=b + 1, hours="%02d:00-%02d:00" % sim.BLOCK_HOURS[b],
                   committed=round(av["committed"][b], 1), available=round(av["available"][b], 1),
                   shortfall=round(av["lost"][b], 1)) for b in range(6)]
    rec = [dict(site=sid, name=name[sid], metered=round(met[sid], 1),
                settled=round(st["statement"][sid], 1),
                difference=round(st["statement"][sid] - met[sid], 1)) for sid in sorted(name)]
    rung0_site = core.ranked(su, "pre")[0][0]
    F = dict(window_from=sim.WINDOW_START.isoformat(), window_to=sim.WINDOW_END.isoformat(),
             as_of=AS_OF.isoformat(), filing_due=FILING_DUE.isoformat(),
             delivery_month=DELIVERY_MONTH, delivery_start="2026-11-01", tso=TSO, org=ORG,
             tolerance=core.TOLERANCE_PCT, scorecard=sc, down=down, availability=blocks,
             reconciliation=rec, call_site=call, call_name=name[call],
             call_gain=round(su[call]["traj"], 1), runner_site=runner, runner_name=name[runner],
             runner_gain=round(su[runner]["traj"], 1),
             gap_pp=round(round(su[runner]["traj"], 1) - round(su[call]["traj"], 1), 1),
             call_episodes=su[call]["n"],
             down_low_name=dn_low["name"], down_low_gain=dn_low["gain_pct"],
             down_none_name=(dn_none[0]["name"] if dn_none else "none"),
             avail_committed_total=round(sum(b["committed"] for b in blocks), 1),
             avail_available_total=round(sum(b["available"] for b in blocks), 1),
             avail_shortfall_total=round(sum(b["shortfall"] for b in blocks), 1),
             rec_metered_total=round(sum(r["metered"] for r in rec), 1),
             rec_settled_total=round(sum(r["settled"] for r in rec), 1),
             rec_difference_total=round(sum(r["difference"] for r in rec), 1),
             rung0_site=rung0_site, rung0_name=name[rung0_site],
             rung0_pre=round(su[rung0_site]["pre"], 1), rung0_traj=round(su[rung0_site]["traj"], 1),
             ladder={k: {sid: round(v[k], 4) for sid, v in su.items()} for k in ("traj", "pre", "sp", "lin")},
             ladder_names={k: core.ranked(su, k)[0][0] for k in ("traj", "pre", "sp", "lin")},
             exact={sid: round(v["traj"], 6) for sid, v in su.items()},
             exact_down={sid: round(v["traj"], 6) for sid, v in so.items()},
             forcing=dict(ean_lost_mwh=round(st["ean_lost_mwh"], 1),
                          prelim_gap_mwh=round(st["prelim_gap_mwh"], 3),
                          superseded_mwh=round(sum(av["lost_with_superseded"][b] - av["lost"][b]
                                                   for b in range(6)), 1),
                          kwh_site=KWH_SITE),
             counts=counts)
    print("[stage] dictionary and goldens", flush=True)
    counts["dictionary"] = pack2.dictionary(TGT, counts)
    blk = [("Block %d (%02d:00-%02d:00)" % (b + 1, sim.BLOCK_HOURS[b][0], sim.BLOCK_HOURS[b][1]),
            av["committed"][b] / (4.0 * 30), 99.14 - 0.37 * b + 0.11 * (b % 3)) for b in range(6)]
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
