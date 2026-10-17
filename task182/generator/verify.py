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
  5.2  a centrifuge run is one start of a centrifuge in the equipment log and the first stop the log
       records for the same machine after it; a start the log does not stop before that machine starts
       again is not a run, and a week's runs are the runs that start in it
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
    """Everything the bundle has to reproduce: the call's own figures and the asks."""
    return _core(target, json.load(open(figures_path, encoding="utf-8")), True)


def call_only(target, fig):
    """The call's figures alone, for the check that they stand with the plant historian deleted."""
    return _core(target, fig, False)


def _core(target, fig, with_asks):
    global OK
    OK = 0

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
        # the field sheets are in local time: the record runs from the minute the meter was set running
        # to the minute it was stopped on the collection round
        spans.setdefault(d["meter_serial"], []).append(
            (dt.datetime.strptime(d["deployed_at"], "%Y-%m-%d %H:%M"),
             dt.datetime.strptime(d["collected_at"], "%Y-%m-%d %H:%M"),
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
    # a start the log does not stop before that machine starts again is not a run (5.2): every open start
    # left when the log ends is one of those, and the log carries exactly one
    unstopped = 0
    seen_start = {}
    for r in ev:
        if not r["equipment"].startswith("CF-"):
            continue
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        if r["event"] == "START":
            if r["equipment"] in seen_start:
                unstopped += 1
            seen_start[r["equipment"]] = t
        else:
            seen_start.pop(r["equipment"], None)
    ok(unstopped == 1, "the log carries %d starts with no stop before the next start" % unstopped)
    by_day = {}
    for j, (ra, rb) in enumerate(cf_runs):
        d0 = ra.date()
        while d0 <= rb.date():
            by_day.setdefault(d0, []).append((ra, rb, j))
            d0 += dt.timedelta(days=1)

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
            if a <= local <= b:
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


    for code in sorted(spec):
        # every printed level clear of its own rounding edge, measured as the distance to the edge
        edge = 0.05 - abs(spec[code] * 10 - round(spec[code] * 10)) * 0.1
        ok(edge >= 0.015, "%s's level sits %.4f dB from a rounding edge" % (code, edge))
    order = sorted(spec, key=lambda c: -spec[c])
    ok(sorted(order[:CAP]) == sorted(fig["slate"]), "the slate is %s" % order[:CAP])
    ok(order[:CAP] == fig["slate_ordered"], "the slate's order is %s" % order[:CAP])
    ok(order[CAP] == fig["sixth"], "the sixth dwelling is %s" % order[CAP])
    mgn = spec[order[CAP - 1]] - spec[order[CAP]]
    ok(round(mgn, 1) == fig["margin_db"], "the margin is %.2f dB" % mgn)
    ok(0.05 - abs(mgn * 10 - round(mgn * 10)) * 0.1 >= 0.015,
       "the margin sits %.4f dB from its rounding edge" % (0.05 - abs(mgn * 10 - round(mgn * 10)) * 0.1))

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
                if a <= t <= b:
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

    # ---- the plant's own records, which the asks run on: the air the blowers delivered off the two
    # meters its three machines discharge through, and the quarter hours the historian holds no reading of
    # its own for, which are the stamps it wrote no row for and the rows that are the quarter hour before
    # them written again while the plant ran on
    if not with_asks:
        return OK
    hist, held, prev = {}, set(), None
    for r in rows(os.path.join(target, "scada_15min_2026.csv")):
        t0 = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        hist[t0] = r
        if prev is not None and all(v == prev[k] for k, v in r.items() if k != "logged_at"):
            # the same row again: no reading of its own where the plant ran on through it, and the
            # works' own stop where the flows read zero, which is a reading
            if float(r["aeration_header_nm3_h"]) > 0.0 or float(r["bl03_discharge_nm3_h"]) > 0.0:
                held.add(t0)
        prev = r
    ok(len(hist) > 7000, "the historian carries %d rows" % len(hist))
    ok(len(held) > 40,
       "%d of them are the quarter hour before them written again while the plant ran on" % len(held))

    def air_at(t0):
        return float(hist[t0]["aeration_header_total_knm3"]) + float(hist[t0]["bl03_discharge_total_knm3"])

    def gone(lo, hi):
        n, cur, longest = 0, 0, 0
        t0 = lo + dt.timedelta(minutes=15)
        while t0 <= hi:
            if t0 not in hist or t0 in held:
                n += 1
                cur += 1
                longest = max(longest, cur)
            else:
                cur = 0
            t0 += dt.timedelta(minutes=15)
        return n, longest

    wins = {}
    for serial, sp in spans.items():
        for a, b, c, _ in sp:
            for k in range((b.date() - a.date()).days + 1):
                day = a.date() + dt.timedelta(days=k)
                if day.weekday() > 4:
                    continue
                lo = dt.datetime(day.year, day.month, day.day, DAY_START)
                hi = dt.datetime(day.year, day.month, day.day, DAY_END)
                if lo >= a and hi <= b:
                    wins.setdefault(c, []).append((lo, hi))
    for code in sorted(wins):
        air, n, longest = 0.0, 0, 0
        for lo, hi in sorted(wins[code]):
            air += air_at(hi) - air_at(lo)
            n2, l2 = gone(lo, hi)
            n += n2
            longest = max(longest, l2)
        ok(round(air, 1) == fig["blower_air_knm3"][code],
           "%s blower air %.1f against %s" % (code, air, fig["blower_air_knm3"][code]))
        ok(n == fig["unrecorded_quarter_hours"][code],
           "%s unrecorded quarter hours %d against %s" % (code, n,
                                                          fig["unrecorded_quarter_hours"][code]))
        ok(longest == fig["longest_unrecorded_run"][code],
           "%s longest unrecorded run %d against %s" % (code, longest,
                                                        fig["longest_unrecorded_run"][code]))
    starts = [dt.date(2026, 8, 31) + dt.timedelta(days=7 * i) for i in range(6)]
    for i, d0 in enumerate(starts):
        a = dt.datetime(d0.year, d0.month, d0.day)
        b = a + dt.timedelta(days=7)
        ok(a in hist and b in hist, "week %d has a reading at both boundaries" % i)
        air = air_at(b) - air_at(a)
        n, longest = gone(a, b)
        w = fig["weekly_plant"][str(i)]
        ok(int(round(air)) == w["blower_air_knm3"],
           "week %d blower air %d against %d" % (i, round(air), w["blower_air_knm3"]))
        ok(0.5 - abs(air - round(air)) >= 0.15,
           "week %d's air (%.1f) sits %.2f from the whole-unit edge" % (i, air, 0.5 - abs(air - round(air))))
        ok(n == w["unrecorded_quarter_hours"],
           "week %d unrecorded quarter hours %d against %d" % (i, n, w["unrecorded_quarter_hours"]))
        ok(longest == w["longest_unrecorded_run"],
           "week %d longest unrecorded run %d against %d" % (i, longest, w["longest_unrecorded_run"]))

    # ---- the goldens carry the same figures
    gold = os.path.join(os.path.dirname(target), "golden", "specific_sound_levels.csv")
    if os.path.exists(gold):
        for r in rows(gold):
            c = r["position_code"]
            ok(float(r["specific_sound_level_db_laeq"]) == fig["specific_level_db"][c],
               "the golden table's level for %s" % c)
            ok(float(r["blower_air_knm3_in_assessment_period"]) == fig["blower_air_knm3"][c],
               "the golden table's blower air for %s" % c)
            ok(int(r["unrecorded_quarter_hours"]) == fig["unrecorded_quarter_hours"][c],
               "the golden table's unrecorded quarter hours for %s" % c)
            ok(int(r["longest_unrecorded_run_quarter_hours"]) == fig["longest_unrecorded_run"][c],
               "the golden table's longest unrecorded run for %s" % c)
    return OK
