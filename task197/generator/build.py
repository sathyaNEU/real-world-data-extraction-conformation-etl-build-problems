"""task197 pack builder. Writes target/, golden/ and figures.json from core.py's arrays."""
import sys, os, json, csv, sqlite3, shutil, datetime as dt
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim, core
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
    ("VKF-ZWT", dt.date(2026, 9, 26), "10:41", 52, "state of charge outside reserve band", "SOC-OUT"),
    ("VKF-HGZ", dt.date(2026, 9, 30), "20:35", 74, "engine 3 trip, reserve capacity reduced", "ENG-TRP"),
    ("VKF-TRB", dt.date(2026, 10, 1), "09:14", 41, "process load locked out of reserve", "LOA-LCK"),
    ("VKF-NWV", dt.date(2026, 10, 3), "06:22", 29, "communications loss to control platform", "COM-LOS"),
    ("VKF-DLK", dt.date(2026, 10, 5), "17:48", 63, "inverter bank 2 isolated", "INV-ISO"),
    ("VKF-RDL", dt.date(2026, 10, 7), "18:05", 47, "gas supply pressure low", "GAS-LOW"),
    ("VKF-KPV", dt.date(2026, 10, 9), "16:08", 35, "auxiliary transformer inspection", "AUX-INS"),
    ("VKF-MPD", dt.date(2026, 9, 22), "06:35", 44, "engine 1 lube oil alarm", "ENG-LUB"),
    # three entries a later correction row supersedes (the outage was logged against the wrong site
    # or cancelled); a naive sum of outage minutes counts them twice
    ("VKF-OOS", dt.date(2026, 9, 28), "13:20", 56, "reserve withdrawn, pending investigation", "ALM-DRP"),
    ("VKF-HGZ", dt.date(2026, 10, 2), "21:10", 68, "reserve withdrawn, pending investigation", "ENG-TRP"),
    ("VKF-NWV", dt.date(2026, 10, 10), "09:05", 33, "reserve withdrawn, pending investigation", "COM-LOS"),
]
SUPERSEDED = {9, 10, 11}        # indexes into UNAVAIL whose event a correction row cancels

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

def unavail_windows(site_id):
    out = []
    for i, (sid, d, hhmm, mins, reason, code) in enumerate(UNAVAIL):
        if sid != site_id or i in SUPERSEDED:
            continue
        h, m = [int(x) for x in hhmm.split(":")]
        s0 = h * 3600 + m * 60
        out.append((d, s0, s0 + mins * 60))
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
    W = core.window()
    recs = core.recordings(W)
    cache = core.power_cache(W, recs)

    # ---------- the 1 Hz archive -------------------------------------------------------------
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
        if dup_src is None and trig == "frequency_excursion" and sid == "VKF-HGZ" \
                and d == dt.date(2026, 10, 4) and any(a <= lo <= b for (a, b, _, _) in W[d]["over"]):
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
    json.dump(counts, open(os.path.join(HERE, "_counts.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(counts, indent=1, sort_keys=True))
    return W, recs, cache, archive_index


if __name__ == "__main__":
    main()
