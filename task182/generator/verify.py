"""An independent read of the bundle: nothing is imported from the generator, every figure is rebuilt from
the shipped files and the plan's own clauses, and the result is compared with figures.json.

The rules this file encodes are the ones the shipped noise management plan states:
  2.1  the positions are those in the monitoring position schedule
  3.1  specific sound level = measured sound level less residual sound, combined in energy
  3.2  the assessment period is 07:00 to 19:00 on weekdays, local time
  4.1  a deployment's deviation is the mean of its two field checks less the calibrator's 94.0 dB, and
       where that deviation is more than 0.3 dB from zero it is taken off every level the deployment
       recorded
  4.2  a minute is not valid where the met record for its ten minutes counted rain on the gauge or shows
       wind above 5 m a second, or where the meter recorded no measurement for that minute
  4.3  a tone is prominent where a band exceeds the mean of its two neighbours by 5 dB or more, on the
       unweighted band levels over the assessment period
  5.1  a week's process figure is the counter reading at 00:00 on its Monday taken from the reading at
       00:00 on the Monday after, with the counter's roll-over added back
  5.2  a centrifuge run is one start of a centrifuge in the equipment log
  7.1  the slot takes the dwellings in order of specific sound level, highest first
"""
import csv
import datetime as dt
import json
import math
import os

CAL_REF, CAL_TOL = 94.0, 0.3
DAY_START, DAY_END = 7, 19
WIND_LIMIT = 5.0
TIP_MM = 0.2
NO_DATA = -120.0        # the survey notes: a minute with no measurement carries -120.2 in every column
OFFSET = 1          # the survey notes: the meters stamp UTC, local time was UTC+1 throughout
SWAP = dt.date(2026, 9, 20)      # the survey notes: the replacement anemometer reports km an hour
CAP = 5
OK = 0


def ok(cond, msg):
    global OK
    OK += 1
    if not cond:
        raise AssertionError("verify: " + msg)


def eavg(vals):
    return 10.0 * math.log10(sum(10.0 ** (v / 10.0) for v in vals) / float(len(vals)))


def esub(a, b):
    return 10.0 * math.log10(10.0 ** (a / 10.0) - 10.0 ** (b / 10.0))


def rows(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def run(target, figures_path):
    global OK
    OK = 0
    fig = json.load(open(figures_path, encoding="utf-8"))

    # ---- the paperwork
    deps = rows(os.path.join(target, "meter_deployments_2026.csv"))
    cal = {r["instrument_serial"]: r for r in rows(os.path.join(target, "calibration_records_2026.csv"))}
    ref = {float(r["calibrator_level_db"]) for r in cal.values() if r["calibrator_level_db"]}
    ok(ref == {CAL_REF}, "the certificates give the calibrator's reference level as %s" % sorted(ref))
    adj = {}
    for d in deps:
        mean_dev = (float(d["cal_check_before_db"]) + float(d["cal_check_after_db"])) / 2.0 - CAL_REF
        ok(abs(float(d["cal_check_before_db"]) - float(d["cal_check_after_db"])) <= 1.0,
           "plan 4.1: deployment %s is usable" % d["deployment_ref"])
        adj[d["deployment_ref"]] = mean_dev if abs(mean_dev) > CAL_TOL else 0.0
    spans = {}
    for d in deps:
        spans.setdefault(d["meter_serial"], []).append(
            (dt.date.fromisoformat(d["start_date"]), dt.date.fromisoformat(d["end_date"]),
             d["position_code"], d["deployment_ref"]))

    # ---- the met mast, and the validity rule
    met = rows(os.path.join(target, "weather_10min_2026.csv"))
    wind, rain10, stamps10 = {}, {}, []
    prev_tips, prev_day = None, None
    inc = []
    for r in met:
        t = dt.datetime.strptime(r["measured_at_utc"], "%Y-%m-%d %H:%M")
        v = float(r["wind_speed"])
        eff = round(v / 3.6, 6) if t.date() >= SWAP else v
        wind[t] = eff
        tips = int(r["rain_tips_today"])
        if prev_day is None or t.date() != prev_day:
            step = tips
        else:
            step = tips - prev_tips
        inc.append((t, max(step, 0) * TIP_MM))
        prev_tips, prev_day = tips, t.date()
        stamps10.append(t)
    rained = {t: mm > 0.0 for t, mm in inc}
    ok(len(wind) > 5000, "the met record covers the survey (%d records)" % len(wind))
    ok(sum(1 for v in rained.values() if v) > 40, "the gauge counted rain in the survey")

    def met_key(stamp_utc):
        return stamp_utc - dt.timedelta(minutes=stamp_utc.minute % 10, seconds=0)

    def valid(stamp_utc):
        k = met_key(stamp_utc)
        if k not in wind:
            return True
        return (not rained.get(k, False)) and wind[k] <= WIND_LIMIT

    # ---- the plant's own log: every interval in which all three sources are down
    ev = rows(os.path.join(target, "plant_equipment_events_2026.csv"))
    ev.sort(key=lambda r: (r["logged_at"], r["equipment"]))
    units = sorted({r["equipment"] for r in ev})
    ok(len(units) == 6, "the log carries six units: %s" % units)
    state = {u: True for u in units}
    down_from, downs = None, []
    for r in ev:
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        state[r["equipment"]] = (r["event"] == "START")
        if not any(state.values()) and down_from is None:
            down_from = t
        elif any(state.values()) and down_from is not None:
            downs.append((down_from, t))
            down_from = None
    ok(len(downs) >= 6, "the log shows %d intervals with every unit down" % len(downs))

    def in_down(stamp_local):
        for a, b in downs:
            if a <= stamp_local < b:
                return True
        return False

    # ---- plan 5.2: every centrifuge run the equipment log carries
    cf_open, cf_runs = {}, []
    for r in ev:
        if not r["equipment"].startswith("CF-"):
            continue
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        if r["event"] == "START":
            cf_open[r["equipment"]] = t
        elif r["equipment"] in cf_open:
            cf_runs.append((cf_open.pop(r["equipment"]), t))
    cf_runs.sort()
    ok(len(cf_runs) > 50, "the log carries %d centrifuge runs" % len(cf_runs))

    # ---- the meters
    import pyarrow.parquet as pq
    tbl = pq.read_table(os.path.join(target, "sound_levels_1min_2026.parquet"))
    cols = tbl.to_pydict()
    seen = set()
    acc = {}
    for i in range(tbl.num_rows):
        serial = cols["meter_serial"][i]
        stamp = cols["measured_at_utc"][i]
        key = (serial, stamp)
        if key in seen:
            continue                      # the repeated download: one copy of a minute is one minute
        seen.add(key)
        local = stamp + dt.timedelta(hours=OFFSET)
        code = ref = None
        for a, b, c, dref in spans.get(serial, []):
            if a <= local.date() <= b:
                code, ref = c, dref
                break
        if code is None:
            continue
        raw = float(cols["laeq_db"][i])
        nodata = raw <= NO_DATA
        if nodata:
            ok(float(cols["la90_db"][i]) <= NO_DATA and float(cols["lamax_db"][i]) <= NO_DATA
               and float(cols["lamin_db"][i]) <= NO_DATA,
               "a minute with no measurement carries no statistics (%s %s)" % (serial, stamp))
        else:
            ok(float(cols["lamax_db"][i]) >= raw >= float(cols["la90_db"][i])
               >= float(cols["lamin_db"][i]),
               "the minute's levels order as an instrument reports them (%s %s)" % (serial, stamp))
        laeq = raw - adj[ref]
        la90 = float(cols["la90_db"][i]) - adj[ref]
        d = acc.setdefault(code, {"on": [], "off": [], "excl": 0, "la90": [], "cf": 0, "runs": set()})
        day = local.weekday() <= 4 and DAY_START <= local.hour < DAY_END
        v = valid(stamp) and not nodata
        if in_down(local):
            if v:
                d["off"].append(laeq)
        elif day:
            if v:
                d["on"].append(laeq)
                d["la90"].append(la90)
                for j, (ra, rb) in enumerate(cf_runs):
                    if ra <= local < rb:
                        d["cf"] += 1
                        d["runs"].add(j)
                        break
            else:
                d["excl"] += 1
    ok(len(acc) == 14, "fourteen positions carry minutes: %d" % len(acc))

    spec = {}
    for code, d in sorted(acc.items()):
        total = eavg(d["on"])
        resid = eavg(d["off"])
        spec[code] = esub(total, resid)
        ok(round(spec[code], 1) == fig["specific_level_db"][code],
           "%s specific level %.3f against %s" % (code, spec[code], fig["specific_level_db"][code]))
        ok(round(total, 1) == fig["measured_total_db"][code],
           "%s measured total %.3f against %s" % (code, total, fig["measured_total_db"][code]))
        ok(round(resid, 1) == fig["residual_db"][code],
           "%s residual %.3f against %s" % (code, resid, fig["residual_db"][code]))
        ok(len(d["on"]) == fig["valid_minutes"][code],
           "%s valid minutes %d against %s" % (code, len(d["on"]), fig["valid_minutes"][code]))
        ok(d["excl"] == fig["excluded_minutes"][code],
           "%s excluded minutes %d against %s" % (code, d["excl"], fig["excluded_minutes"][code]))
        ok(len(d["off"]) == fig["stop_minutes"][code],
           "%s stop minutes %d against %s" % (code, len(d["off"]), fig["stop_minutes"][code]))
        ok(d["cf"] == fig["centrifuge_minutes"][code],
           "%s dewatering minutes %d against %s" % (code, d["cf"], fig["centrifuge_minutes"][code]))
        ok(len(d["runs"]) == fig["centrifuge_runs_position"][code],
           "%s runs behind its level %d against %s" % (code, len(d["runs"]),
                                                       fig["centrifuge_runs_position"][code]))

    order = sorted(spec, key=lambda c: -spec[c])
    ok(sorted(order[:CAP]) == sorted(fig["slate"]), "the slate is %s" % order[:CAP])
    ok(order[:CAP] == fig["slate_ordered"], "the slate's order is %s" % order[:CAP])
    ok(order[CAP] == fig["sixth"], "the sixth dwelling is %s" % order[CAP])
    ok(round(spec[order[CAP - 1]] - spec[order[CAP]], 1) == fig["margin_db"],
       "the margin is %.2f dB" % (spec[order[CAP - 1]] - spec[order[CAP]]))

    # the default path, on its own code path: the background from the position's own running record
    naive = {}
    for code, d in acc.items():
        s = sorted(d["on"])
        p10 = s[int(0.10 * (len(s) - 1))]
        frac = 0.10 * (len(s) - 1) - int(0.10 * (len(s) - 1))
        p10 = p10 + frac * (s[min(int(0.10 * (len(s) - 1)) + 1, len(s) - 1)] - p10)
        naive[code] = esub(eavg(d["on"]), p10)
    nslate = sorted(sorted(naive, key=lambda c: -naive[c])[:CAP])
    ok(nslate != sorted(fig["slate"]), "the default path files another slate: %s" % nslate)
    ok(nslate == sorted(fig["rungs"]["rung2_p10"]["slate"]),
       "the default path files %s" % nslate)

    # ---- the bands and the tone test
    with open(os.path.join(target, "third_octave_15min_2026.csv"), encoding="utf-8") as fh:
        rd = csv.reader(fh)
        head = next(rd)
        freqs = [h.replace("lzeq_", "").replace("_hz", "").replace("p", ".") for h in head[2:]]
        band_acc = {}
        ok(head[1] == "measured_at_utc", "the band export is stamped UTC: %s" % head[1])
        for row in rd:
            t = (dt.datetime.strptime(row[1], "%Y-%m-%d %H:%M") + dt.timedelta(hours=OFFSET))
            if t.weekday() > 4 or not (DAY_START <= t.hour < DAY_END):
                continue
            code = None
            for a, b, c, _ in spans.get(row[0], []):
                if a <= t.date() <= b:
                    code = c
                    break
            if code is None:
                continue
            band_acc.setdefault(code, []).append([float(x) for x in row[2:]])
    for code in sorted(acc):
        want_band = fig["highest_band_hz"][code]
        want_tone = fig["tone_prominent"][code]
        if code not in band_acc:
            ok(want_band == "none" and want_tone == "none", "%s has no band rows" % code)
            continue
        n = len(band_acc[code])
        lev = [10.0 * math.log10(sum(10.0 ** (r[j] / 10.0) for r in band_acc[code]) / n)
               for j in range(len(freqs))]
        j = max(range(len(lev)), key=lambda k: lev[k])
        nb = [lev[k] for k in (j - 1, j + 1) if 0 <= k < len(lev)]
        excess = lev[j] - sum(nb) / float(len(nb))        # plan 4.3: the mean of the two band levels
        en = lev[j] - 10.0 * math.log10(sum(10.0 ** (x / 10.0) for x in nb) / len(nb))
        ok((excess >= 5.0) == (en >= 5.0),
           "%s gives the same verdict on either mean of the neighbours (%.2f, %.2f)" % (code, excess, en))
        got_band = freqs[j].rstrip("0").rstrip(".") if "." in freqs[j] else freqs[j]
        ok(str(want_band) == got_band, "%s highest band %s against %s" % (code, got_band, want_band))
        ok(want_tone == ("yes" if excess >= 5.0 else "no"),
           "%s tone %s at %.2f dB excess" % (code, want_tone, excess))

    # ---- the plant's week: the counters at the week boundaries (5.1) and the log's runs (5.2)
    sc = {}
    for r in rows(os.path.join(target, "scada_15min_2026.csv")):
        sc[dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")] = r
    starts = [dt.date(2026, 8, 31) + dt.timedelta(days=7 * i) for i in range(6)]
    log_starts = [dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
                  for r in rows(os.path.join(target, "plant_equipment_events_2026.csv"))
                  if r["equipment"].startswith("CF-") and r["event"] == "START"]
    for i, d0 in enumerate(starts):
        a = dt.datetime(d0.year, d0.month, d0.day)
        b = a + dt.timedelta(days=7)
        ok(a in sc and b in sc, "week %d has a reading at both boundaries" % i)
        gas = float(sc[b]["biogas_meter_m3"]) - float(sc[a]["biogas_meter_m3"])
        while gas < 0:
            gas += 100000.0
        air = float(sc[b]["blower_air_total_knm3"]) - float(sc[a]["blower_air_total_knm3"])
        runs = sum(1 for t in log_starts if a <= t < b)
        inside = sorted((t, float(r["engine_hours_run"])) for t, r in sc.items() if a <= t <= b)
        eng = 0.0
        for j in range(1, len(inside)):
            step = inside[j][1] - inside[j - 1][1]
            eng += inside[j][1] if step < 0 else step     # the counter was changed inside this week
        w = fig["weekly_plant"][str(i)]
        ok(round(eng, 1) == w["engine_hours"],
           "week %d engine hours %.1f against %.1f" % (i, eng, w["engine_hours"]))
        ok(int(round(gas)) == w["biogas_m3"],
           "week %d biogas %d against %d" % (i, round(gas), w["biogas_m3"]))
        ok(int(round(air)) == w["blower_air_knm3"],
           "week %d blower air %d against %d" % (i, round(air), w["blower_air_knm3"]))
        ok(runs == w["centrifuge_runs"],
           "week %d runs %d against %d" % (i, runs, w["centrifuge_runs"]))

    # ---- the goldens carry the same figures
    gold = os.path.join(os.path.dirname(target), "golden", "specific_sound_levels.csv")
    if os.path.exists(gold):
        for r in rows(gold):
            c = r["position_code"]
            ok(float(r["specific_sound_level_db_laeq"]) == fig["specific_level_db"][c],
               "the golden table's level for %s" % c)
            ok(int(r["centrifuge_minutes_in_assessment_period"]) == fig["centrifuge_minutes"][c],
               "the golden table's centrifuge minutes for %s" % c)
            ok(int(r["centrifuge_runs_in_assessment_period"]) == fig["centrifuge_runs_position"][c],
               "the golden table's centrifuge runs for %s" % c)
    return OK


def plant_state(target, fig, spans):
    """Plan 5.2 executed from the equipment log: what ran over each position's assessment period."""
    opens, runs = {}, []
    for r in sorted(rows(os.path.join(target, "plant_equipment_events_2026.csv")),
                    key=lambda x: x["logged_at"]):
        if not r["equipment"].startswith("CF-"):
            continue
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        if r["event"] == "START":
            opens[r["equipment"]] = t
        elif r["equipment"] in opens:
            runs.append((opens.pop(r["equipment"]), t))
    for code in sorted(fig["centrifuge_minutes"]):
        wins = []
        for serial, sp in spans.items():
            for a, b, c, _ in sp:
                if c != code:
                    continue
                for k in range((b - a).days + 1):
                    day = a + dt.timedelta(days=k)
                    if day.weekday() <= 4:
                        wins.append((dt.datetime(day.year, day.month, day.day, DAY_START),
                                     dt.datetime(day.year, day.month, day.day, DAY_END)))
        mins = 0
        for lo, hi in wins:
            iv = sorted((max(a, lo), min(b, hi)) for a, b in runs if a < hi and b > lo)
            cur = None
            for a, b in iv:
                if cur and a <= cur[1]:
                    cur = (cur[0], max(cur[1], b))
                else:
                    if cur:
                        mins += int((cur[1] - cur[0]).total_seconds() // 60)
                    cur = (a, b)
            if cur:
                mins += int((cur[1] - cur[0]).total_seconds() // 60)
        ok(mins == fig["centrifuge_minutes"][code],
           "%s centrifuge minutes %d against %d" % (code, mins, fig["centrifuge_minutes"][code]))
        n = sum(1 for a, b in runs if any(a < hi and b > lo for lo, hi in wins))
        ok(n == fig["centrifuge_runs_position"][code],
           "%s centrifuge runs %d against %d" % (code, n, fig["centrifuge_runs_position"][code]))
