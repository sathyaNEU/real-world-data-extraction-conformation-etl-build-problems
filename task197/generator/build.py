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

# Mid-block reserve unavailability: (site, local date, start local HH:MM, minutes, reason, code).
# None of these windows may contain a qualifying under-frequency episode for that site; checks.py
# asserts the count is zero.
UNAVAIL = [
    ("VKF-OOS", dt.date(2026, 9, 23), "05:12", 38, "droop controller alarm, reserve withdrawn", "ALM-DRP"),
    ("VKF-HGZ", dt.date(2026, 9, 30), "20:35", 74, "engine 3 trip, reserve capacity reduced", "ENG-TRP"),
    ("VKF-NWV", dt.date(2026, 10, 3), "06:22", 29, "communications loss to control platform", "COM-LOS"),
    ("VKF-MPD", dt.date(2026, 9, 22), "06:35", 44, "engine 1 lube oil alarm", "ENG-LUB"),
    ("VKF-ZWT", dt.date(2026, 10, 1), "10:20", 52, "state of charge outside reserve band", "SOC-OUT"),
    ("VKF-TRB", dt.date(2026, 9, 25), "09:30", 41, "process load locked out of reserve", "LOA-LCK"),
    ("VKF-DLK", dt.date(2026, 9, 27), "01:30", 63, "inverter bank 2 isolated", "INV-ISO"),
    # three entries a later correction row supersedes (the outage was logged against the wrong site
    # or cancelled); a naive sum of outage minutes counts them twice
    ("VKF-OOS", dt.date(2026, 9, 28), "13:20", 56, "reserve withdrawn, pending investigation", "ALM-DRP"),
    ("VKF-HGZ", dt.date(2026, 10, 2), "21:10", 68, "reserve withdrawn, pending investigation", "ENG-TRP"),
    ("VKF-NWV", dt.date(2026, 10, 10), "09:05", 33, "reserve withdrawn, pending investigation", "COM-LOS"),
]
SUPERSEDED = {7, 8, 9}        # indexes into UNAVAIL whose event a correction row cancels

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

_PLACED = {}
_PLACE_CACHE = {}
_WIN_CACHE = {}


def _episode_seconds(d):
    """Every second inside a qualifying episode of either sign on local date d, padded."""
    if d in _PLACED:
        return _PLACED[d]
    f = sim.frequency_day(d)
    marked = np.zeros(sim.DAY, dtype=bool)
    for (t0, t1, tstar, fx) in sim.qualifying_episodes(d, f) + core.over_episodes(f):
        marked[max(0, t0 - 120):min(sim.DAY, t1 + 121)] = True
    _PLACED[d] = marked
    return marked


def place_outage(site, d, hhmm, minutes):
    key = (site["id"], d, hhmm, minutes)
    if key not in _PLACE_CACHE:
        _PLACE_CACHE[key] = _place_outage(site, d, hhmm, minutes)
    return _PLACE_CACHE[key]


def _place_outage(site, d, hhmm, minutes):
    """The start second of the logged outage: the first window of that length inside a contracted
    block of that day holding no qualifying episode of either sign, searched from the stated time.
    Keeping every outage clear of both measured populations is what separates the ask devices from
    the main call; checks.py asserts the overlap count is zero."""
    marked = _episode_seconds(d)
    need = minutes * 60
    h, m = [int(x) for x in hhmm.split(":")]
    pref = h * 3600 + m * 60
    cand = sorted(range(0, sim.DAY - need, 60), key=lambda t: (abs(t - pref), t))
    for t in cand:
        rng = np.arange(t - 60, t + need + 60)
        if rng[0] < 0 or rng[-1] >= sim.DAY:
            continue
        if not sim.contracted(site, np.arange(t, t + need), d).all():
            continue
        if marked[t - 60:t + need + 60].any():
            continue
        return t
    return None


def unavail_windows(site_id):
    if site_id in _WIN_CACHE:
        return _WIN_CACHE[site_id]
    out = []
    for i, (sid, d, hhmm, mins, reason, code) in enumerate(UNAVAIL):
        if sid != site_id or i in SUPERSEDED:
            continue
        t0 = place_outage(sim.SITE_BY_ID[sid], d, hhmm, mins)
        if t0 is None:
            continue
        out.append((d, t0, t0 + mins * 60))
    _WIN_CACHE[site_id] = out
    return out


def unavail_rows():
    """Every logged reserve-unavailability event, placed, including the superseded ones."""
    out = []
    for i, (sid, d, hhmm, mins, reason, code) in enumerate(UNAVAIL):
        t0 = place_outage(sim.SITE_BY_ID[sid], d, hhmm, mins)
        if t0 is None:
            continue
        out.append(dict(idx=i, site=sid, date=d, start=t0, minutes=mins, reason=reason,
                        code=code, superseded=(i in SUPERSEDED)))
    return out

def fcr_active(site, d, t):
    """Contracted and not withdrawn from reserve: the seconds the site owed a response."""
    ok = sim.contracted(site, t, d)
    for (dd, a, b) in unavail_windows(site["id"]):
        if dd == d:
            ok = ok & ~((np.asarray(t) >= a) & (np.asarray(t) < b))
    return ok

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

    # patch sim's FCR gate so unavailability removes the obligation, before anything is computed
    sim._fcr_gate = fcr_active
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
        for m in range(1440):
            seg = f[m * 60:(m + 1) * 60]
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
            for p in range(96):
                code = ean[0]
                if ean[1] and core.local_to_utc(d, p * 900).date() >= ean[2]:
                    code = ean[1]
                met_rows.append((code, loc(d, p * 900), p + 1, round(float(mw[p]) * scale, 4), unit))
            for b in sim.commitments(s, d):
                lo_h, hi_h = sim.BLOCK_HOURS[b]
                com_rows.append((d.isoformat(), b + 1, "%02d:00" % lo_h, "%02d:00" % hi_h, s["id"],
                                 round(s["cap"], 2)))
    com_rows.sort(key=lambda r: (r[0], r[1], r[4]))
    counts["programme"] = write_csv(os.path.join(TGT, "platform", "site_programme_15min.csv"),
                                    ["site_id", "period_start_local", "settlement_period", "programme_mw"], prog_rows)
    counts["metered"] = write_csv(os.path.join(TGT, "settlement", "metered_volumes_15min.csv"),
                                  ["metering_point", "period_start_local", "settlement_period", "net_volume", "unit"], met_rows)
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
