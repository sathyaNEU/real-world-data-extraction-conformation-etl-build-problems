"""The clean truth: water levels, the indicator chemistry with the release and the reversed seasons, the October 2026
deciding results placed against the realised limits, and the October field records. No Layer 1 mess here: pack.py
writes the exports the producing systems would write from these values."""
import datetime as dt
import math

import numpy as np

import routes as RT
import world as W

EV = [e["label"] for e in W.EVENTS]


def stream(k):
    return np.random.default_rng(W.SEED * 100 + k)


def sig3(x):
    """three significant figures, as both laboratories report the indicators"""
    if x == 0:
        return 0.0
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    return round(x, d)


def reported(k, v, lab):
    """the value a laboratory reports for an indicator: Tamarack boron in mg/L to three decimals, the rest to three
    significant figures; returned in the golden's units (boron ug/L)"""
    if k == "boron" and lab == "A":
        return round(v / 1000.0, 3) * 1000.0
    return sig3(v)


def lab_of(ei):
    return "A" if ei < W.LAB_SWITCH else "B"


def present(p, ei):
    """MW-5 until its abandonment in May 2022, MW-5R from its installation"""
    d = W.EVENTS[ei]["days"][0]
    if p == "MW-5":
        return d < W.MW5_ABANDONED
    if p == "MW-5R":
        return d > W.MW5_ABANDONED
    return True


# ---------------------------------------------------------------- water levels
def toc_true(p, day):
    """top of casing in NGVD 29 feet on a day (MW-8's riser trimmed in May 2024)"""
    r = W.POINTS[p]
    toc = r[3] + r[4]
    if p == "MW-8" and day >= dt.date(2024, 5, 21):
        toc -= W.MW8_TRIM
    return toc


def heads():
    rng = stream(1)
    out = {}
    for ei, e in enumerate(W.EVENTS):
        lab = e["label"]
        season = 0.85 if e["month"] == 4 else -0.55
        dry = -0.75 if lab in W.DRY else 0.0
        level = W.HEAD_WEST + season + dry + rng.normal(0, 0.22)
        q = W.PUMPING[lab]
        day = e["days"][0]
        for p, r in W.POINTS.items():
            if not present(p, ei):
                continue
            h = level - W.GRADIENT * r[1] - W.DRAW_K[p] * q + rng.normal(0, 0.008)
            dtw = round(toc_true(p, day) - h, 2)
            out[(p, ei)] = {"head_ngvd": round(toc_true(p, day) - dtw, 2), "dtw": dtw, "day": day}
    return out


def reversed_at(hd, w, ei):
    """the truth the decisive step recovers: the background well's head below its boundary piezometer's"""
    return hd[(w, ei)]["head_ngvd"] < hd[(W.BOUNDARY[w], ei)]["head_ngvd"]


# ---------------------------------------------------------------- indicator chemistry
def background(hd):
    rng = stream(2)
    ev_eff = {ei: {k: rng.normal(0, W.EVENT_SD) for k in W.INDICATORS} for ei in range(len(EV))}
    vals, frac = {}, {}
    for ei in range(len(EV)):
        dry = W.DRY_LIFT if EV[ei] in W.DRY else 0.0
        for w in W.BACKGROUND:
            f = 0.0
            if reversed_at(hd, w, ei):
                if w == "MW-1":
                    f = W.F_MW1["strong" if W.PUMPING[EV[ei]] > 1.33 else "moderate"]
                elif w == "MW-2":
                    f = W.F_MW2
                f *= math.exp(rng.normal(0, W.F_SD))
            frac[(w, ei)] = f
            for i, k in enumerate(W.INDICATORS):
                nat = W.NATURAL[w][i] * math.exp(ev_eff[ei][k] + dry + rng.normal(0, W.LOG_SD[k]))
                v = (1 - f) * nat + f * W.LEACHATE[k]
                vals[(w, ei, k)] = reported(k, v, lab_of(ei))
    return vals, frac, ev_eff


def background_window(vals):
    """the plan's background results: April 2018 to April 2026, every routine sample taken and analysed"""
    out = {}
    for (w, ei, k), v in vals.items():
        if ei not in W.BG_EVENTS:
            continue
        if (EV[ei], w) in W.MISSED:
            continue
        if k == "boron" and (EV[ei], w) in W.BORON_NOT_RUN:
            continue
        out[(w, ei, k)] = v
    return out


def compliance(hd, bgwin, rev):
    """compliance wells: natural chemistry, the long-standing release at MW-7 and MW-9, MW-6 newly reached; the October
    2026 results of the plume wells placed against the realised limits."""
    hdiff = {(w, ei): hd[(w, ei)]["head_ngvd"] - hd[(W.BOUNDARY[w], ei)]["head_ngvd"]
             for w in W.BACKGROUND for ei in range(len(EV))}
    lim, _ = RT.background_limits(bgwin, rev, EV, W.DRY, hdiff)
    G = lim[RT.GOLDEN]
    high = {k: min(lim[r][k] for r in RT.CHEAP_HIGH if r in lim) for k in W.INDICATORS}
    low = {k: max(lim[r][k] for r in RT.CHEAP_LOW) for k in W.INDICATORS}
    rng = stream(3)
    ev_eff = {ei: {k: rng.normal(0, W.EVENT_SD) for k in W.INDICATORS} for ei in range(len(EV))}
    noise = {}
    for w in W.COMPLIANCE + ["MW-5"]:
        for ei in range(len(EV)):
            for k in W.INDICATORS:
                noise[(w, ei, k)] = math.exp(ev_eff[ei][k] + (W.DRY_LIFT if EV[ei] in W.DRY else 0.0)
                                             + rng.normal(0, W.LOG_SD[k]))

    def mix(w, ei, f):
        return {k: (1 - f) * W.NATURAL[w][i] * noise[(w, ei, k)] + f * W.LEACHATE[k]
                for i, k in enumerate(W.INDICATORS)}

    # the plume wells' October fractions: each well's leading indicator, the one with the widest window between the
    # golden limit and the lowest high route, placed mid-window in log terms
    plume_oct, lead = {}, {}
    for w in ("MW-9", "MW-7"):
        best = None
        order = sorted(W.INDICATORS, key=lambda k: -(high[k] / G[k]))
        if w == "MW-7" and lead.get("MW-9") == order[0] and high[order[1]] / G[order[1]] > 1.13:
            order = [order[1], order[0]] + order[2:]
        for k0 in order:
            target = math.sqrt(high[k0] / G[k0]) * G[k0]
            for f in np.arange(0.0005, 0.04, 0.00002):
                v = mix(w, W.EVAL, f)
                r = {k: reported(k, v[k], "B") for k in W.INDICATORS}
                if r[k0] >= target:
                    if all(r[k] < 0.94 * high[k] for k in W.INDICATORS) and r[k0] > 1.06 * G[k0]:
                        best = f
                    break
            if best is not None:
                lead[w] = k0
                break
        assert best is not None, (w, "no fraction places")
        plume_oct[w] = best
    # MW-6 well above every route's limit
    k0 = "chloride"
    target = W.PLACE[("MW-6", k0)] * max(lim[r][k0] for r in lim)
    for f in np.arange(0.005, 0.08, 0.0001):
        if reported(k0, mix("MW-6", W.EVAL, f)[k0], "B") >= target:
            plume_oct["MW-6"] = f
            break
    vals, frac = {}, {}
    for ei in range(len(EV)):
        for w in W.COMPLIANCE + ["MW-5"]:
            if not present(w, ei):
                continue
            if w in ("MW-7", "MW-9"):
                f = plume_oct[w] * (0.93 + 0.07 * ei / W.EVAL) * math.exp(rng.normal(0, 0.05)) if ei < W.EVAL else plume_oct[w]
            elif w == "MW-6":
                f = plume_oct["MW-6"] if ei == W.EVAL else W.PLUME_MW6.get(EV[ei], 0.0)
            else:
                f = 0.0
            frac[(w, ei)] = f
            v = mix(w, ei, f)
            for k in W.INDICATORS:
                vals[(w, ei, k)] = reported(k, v[k], lab_of(ei))
    # the road-salt well and the geologic-boron well sit just under the golden limit on their elevated indicators,
    # over the over-cut limits
    for w, ks, r in (("MW-10", ("chloride", "sodium"), 0.885), ("MW-11", ("boron",), 0.88)):
        for k in ks:
            vals[(w, W.EVAL, k)] = reported(k, r * G[k], "B")
    return vals, frac, lim, plume_oct, lead, high, low


# ---------------------------------------------------------------- October 2026 field records (the asks)
def _edge_ok(v, unit, margin):
    """v printed to unit sits at least margin (in the same units) inside its printed cell"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c) >= margin


def _visit(rng, ei, day, w, t, start_counter, meter, octvals, graded):
    """one well visit's reading entries, retried until the visit's graded figures sit inside their printed cells"""
    e = W.EVENTS[ei]
    cl, na = octvals.get(w, (20.0, 12.0))
    base_true = 410 + 5.2 * cl + 4.4 * na + rng.normal(0, 18)
    if ei != W.EVAL:
        base_true *= rng.uniform(0.96, 1.03)
    for attempt in range(200):
        flow = rng.uniform(170, 320)
        lag = rng.uniform(5.5, 9.5)
        nent = int(rng.integers(8, 14))
        temp = rng.uniform(9.2, 12.4) if e["month"] == 10 else rng.uniform(7.6, 9.8)
        spc_true = base_true + attempt * 0.37
        rows = []
        tt = t + dt.timedelta(minutes=lag)
        for j in range(nent):
            minutes = (tt - t).total_seconds() / 60.0
            vol = flow * minutes / 1000.0
            last = j == nent - 1
            drift = (nent - 1 - j) * 0.012
            T = round(temp + rng.normal(0, 0.06) + (nent - 1 - j) * 0.05, 1)
            spc = spc_true * (1 + drift * (1 if j % 2 else -1) * 0.6) if j < nent - 3 else spc_true * (1 + rng.normal(0, 0.004))
            if last:
                spc = spc_true
            recorded = spc * (1 + W.TEMP_COEF * (T - 25)) if meter == W.RENTAL_UNCOMP else spc
            rows.append({"event": ei, "day": day, "time": tt, "location": w, "kind": "reading",
                         "flow_ml_min": int(round(flow + rng.normal(0, 6))), "counter_l": round(start_counter + vol, 2),
                         "temp_c": T, "spc": int(round(recorded)),
                         "ph": round(6.9 + rng.normal(0, 0.05) + (0.1 if w in ("MW-6", "MW-7") else 0), 2),
                         "do": round(max(0.2, rng.normal(1.1, 0.4) + (nent - 1 - j) * 0.15), 2),
                         "orp": int(round(rng.normal(60, 25) - (80 if w in ("MW-6", "MW-7") else 0))),
                         "turb": round(max(0.4, rng.normal(2.0, 0.6) + (nent - 1 - j) * 1.1), 1),
                         "meter": meter, "last": last})
            if not last:
                tt += dt.timedelta(minutes=float(rng.uniform(3.0, 5.0)))
        fin = rows[-1]
        purge_gal = (fin["counter_l"] - round(start_counter, 2)) / W.L_PER_GAL
        comp = fin["spc"] / (1 + W.TEMP_COEF * (fin["temp_c"] - 25)) if meter == W.RENTAL_UNCOMP else float(fin["spc"])
        if not graded or (_edge_ok(purge_gal, 0.1, 0.012) and _edge_ok(comp, 1.0, 0.12)):
            return rows, tt, {"purge_gal": purge_gal, "spc": comp, "meter": meter, "recorded": fin["spc"],
                              "temp": fin["temp_c"], "start_counter": round(start_counter, 2), "sample_time": tt,
                              "end_counter": fin["counter_l"]}
    raise AssertionError(("no mid-bin visit", w))


def field_records(octvals):
    """the sampler's entries for April and October 2026: a reading set every few minutes from the flow-cell meter with
    the pump controller's day counter, the last set at the sample, then a bottles-filled entry when the pump stops.
    The controller counter is zeroed when it is switched on each morning and holds while the pump is off; a decon
    rinse before some wells runs water through it and is logged with the counter after the rinse."""
    rng = stream(5)
    rows, truth = [], {}
    for ei in (W.EVAL - 1, W.EVAL):
        e = W.EVENTS[ei]
        for di, wells in enumerate(W.SAMPLING_ORDER):
            day = e["days"][di]
            counter = 0.0
            t = dt.datetime.combine(day, dt.time(11, 5) if di == 0 else dt.time(8, 10))
            for wi, w in enumerate(wells):
                if wi > 0 and rng.random() < 0.55:
                    counter += rng.uniform(1.4, 2.6)
                    rows.append({"event": ei, "day": day, "time": t - dt.timedelta(minutes=int(rng.integers(9, 15))),
                                 "location": w, "kind": "decon", "counter_l": round(counter, 2)})
                meter = W.OCT_METERS[di] if ei == W.EVAL else W.OWN_METER
                vrows, tend, info = _visit(rng, ei, day, w, t, counter, meter, octvals, ei == W.EVAL)
                rows += vrows
                truth[(ei, w)] = info
                counter = vrows[-1]["counter_l"] + rng.uniform(1.3, 2.4)      # bottles filled with the pump running
                rows.append({"event": ei, "day": day, "time": tend + dt.timedelta(minutes=int(rng.integers(6, 11))),
                             "location": w, "kind": "bottles", "counter_l": round(counter, 2)})
                counter = round(counter, 2)
                t = tend + dt.timedelta(minutes=float(rng.uniform(32, 58)))
    return rows, truth


def _handtyped(ei, day, w):
    return ei == W.EVAL and day == W.EVENTS[W.EVAL]["days"][2] and w in W.METER_UNPAIRED


def sample_minutes(rows, truth):
    """Where each sample sits against the chain of custody. The sample's set is logged a few seconds before a half
    minute and the sample collected in the next minute, so the custody minute begins 31 to 35 s after the set. On the
    October visits the counter carried from the set to the start of that minute, at the set's flow, at the rate of the
    last interval or on the line to the next counter, prints the same tenth of a gallon as the set's own counter: where
    it would not, the pump-stop counter before the visit is raised (a longer decon rinse or bottle fill) or, for a
    day's first well, the last interval's volume trimmed, always inside the printed figure. Its own stream; no graded
    figure moves."""
    rng = stream(7)
    L = W.L_PER_GAL
    index = {}
    for i, x in enumerate(rows):
        if x["kind"] == "reading":
            index.setdefault((x["event"], x["location"]), []).append(i)
    for i, x in enumerate(rows):
        if x["kind"] != "reading" or not x["last"]:
            continue
        ei, w, day = x["event"], x["location"], x["day"]
        sets = index[(ei, w)]
        p = rows[sets[-2]]
        b = rows[i + 1]
        sec = x["time"].second + x["time"].microsecond / 1e6
        target = 25 + float(rng.uniform(0, 4))                   # a few seconds before the half minute
        x["time"] = x["time"] + dt.timedelta(seconds=target - sec)
        assert (x["time"] - p["time"]).total_seconds() > 150, (w, target - sec)
        minute = x["time"].replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
        assert 30 <= (minute - x["time"]).total_seconds() <= 36, (w, minute, x["time"])
        info = truth[(ei, w)]
        info["collect_minute"] = minute
        info["collect_time"] = minute + dt.timedelta(seconds=float(rng.uniform(5, 50)))
        if ei != W.EVAL:
            x["flow_ml_min"] = int(round(1000.0 * (x["counter_l"] - p["counter_l"]) /
                                         ((x["time"] - p["time"]).total_seconds() / 60.0) + rng.normal(0, 2.5)))
            continue
        # the pump-stop entry before the visit: a decon rinse, the previous well's bottles entry, or the morning zero
        j = sets[0] - 1
        start_row = rows[j] if j >= 0 and rows[j]["day"] == day and rows[j]["kind"] in ("decon", "bottles") else None
        for attempt in range(40):
            start = start_row["counter_l"] if start_row else 0.0
            minutes_last = (x["time"] - p["time"]).total_seconds() / 60.0
            f_imp = (x["counter_l"] - p["counter_l"]) / minutes_last
            f_next = f_imp if not _handtyped(ei, day, w) else (b["counter_l"] - x["counter_l"]) / (
                (b["time"] - x["time"]).total_seconds() / 60.0)
            carry = max(f_imp + 0.008, f_next) * (minute - x["time"]).total_seconds() / 60.0
            raw = (x["counter_l"] - start) / L
            fig = round(raw, 1)
            over = raw + carry / L - (fig + 0.05 - 0.004)
            if over <= 0:
                break
            need = round((over + 0.002) * L + 0.005, 2)
            if start_row is not None:
                start_row["counter_l"] = round(start_row["counter_l"] + need, 2)
            else:
                x["counter_l"] = round(x["counter_l"] - need, 2)
            assert round((x["counter_l"] - (start_row["counter_l"] if start_row else 0.0)) / L, 1) == fig, (w, need)
        else:
            raise AssertionError(("no convergence", w))
        raw = (x["counter_l"] - (start_row["counter_l"] if start_row else 0.0)) / L
        assert raw - (round(raw, 1) - 0.05) >= 0.012, (w, raw)
        if start_row is not None:
            nxt = rows[sets[0]]["counter_l"]
            assert start_row["counter_l"] < nxt - 0.2, (w, start_row["counter_l"], nxt)
        x["flow_ml_min"] = int(round(1000.0 * (x["counter_l"] - p["counter_l"]) /
                                     ((x["time"] - p["time"]).total_seconds() / 60.0) + rng.normal(0, 2.5)))
        info["purge_gal"] = raw
    return rows


def bottle_sets(rows, truth):
    """The sample itself: collected in the chain of custody's minute, while the field app goes on logging the flow
    cell every few minutes until the pump stops. Those later sets read water the sample was not taken from: the cell
    warms, takes up air and stirs fines, so they agree with nothing before them. The first of them runs on at the
    sample set's rate. Visits typed by hand (the unpaired meter) log nothing after the sample. Drawn on a stream of
    their own, so every set before the sample, every counter and every graded figure stays as it was."""
    rng = stream(6)
    out = []
    first_counter, start_counter, last_stop = {}, {}, {}
    for x in rows:
        key = (x["event"], x["location"])
        if x["kind"] in ("decon", "bottles"):
            last_stop[x["day"]] = x["counter_l"]
        elif x["kind"] == "reading" and key not in first_counter:
            first_counter[key] = x["counter_l"]
            start_counter[key] = last_stop.get(x["day"], 0.0)
    for i, x in enumerate(rows):
        out.append(x)
        if x["kind"] != "reading" or not x["last"]:
            continue
        ei, w, day = x["event"], x["location"], x["day"]
        b = rows[i + 1]
        assert b["kind"] == "bottles" and b["location"] == w, (w, b["kind"])
        info = truth[(ei, w)]
        t_m = x["time"]
        if _handtyped(ei, day, w):
            continue
        t_c = info["collect_time"]
        p = [r for r in rows[:i] if r["kind"] == "reading" and r["location"] == w and r["event"] == ei][-1]
        f_imp = (x["counter_l"] - p["counter_l"]) / ((t_m - p["time"]).total_seconds() / 60.0)
        golden_gal = round((x["counter_l"] - start_counter[(ei, w)]) / W.L_PER_GAL, 1)
        for attempt in range(200):
            # the last set's counter less the visit's first set must not land the purge volume by coincidence
            times = [t_c + dt.timedelta(seconds=float(rng.uniform(120, 200)))]
            c1 = min(round(x["counter_l"] + f_imp * (times[0] - t_m).total_seconds() / 60.0, 2), b["counter_l"] - 0.15)
            counters = [c1]
            t2 = times[0] + dt.timedelta(seconds=float(rng.uniform(180, 240)))
            if (b["time"] - t2).total_seconds() >= 30:
                c2 = round(c1 + (b["counter_l"] - c1) * (t2 - times[0]).total_seconds() /
                           (b["time"] - times[0]).total_seconds(), 2)
                if (c2 - c1) / ((t2 - times[0]).total_seconds() / 60.0) <= 0.48:
                    times.append(t2)
                    counters.append(c2)
            if ei != W.EVAL or abs(round((counters[-1] - first_counter[(ei, w)]) / W.L_PER_GAL, 1) - golden_gal) >= 0.05:
                break
        else:
            raise AssertionError(("no bottle-set timing", w))
        assert (b["time"] - times[0]).total_seconds() >= 30, w
        comp, prev, unc = info["spc"], x, x["meter"] == W.RENTAL_UNCOMP
        for t, counter in zip(times, counters):
            for attempt in range(80):
                T = round(prev["temp_c"] + rng.uniform(0.15, 0.5), 1)
                spc_k = comp * (1 + rng.uniform(0.006, 0.016) * (1 if rng.random() < 0.5 else -1))
                logged = int(round(spc_k * (1 + W.TEMP_COEF * (T - 25)))) if unc else int(round(spc_k))
                read = logged / (1 + W.TEMP_COEF * (T - 25)) if unc else float(logged)
                if abs(round(read) - round(comp)) >= 2 and abs(read - round(read)) <= 0.38:
                    break
            else:
                raise AssertionError(("no bottle set", w))
            minutes = (t - prev["time"]).total_seconds() / 60.0
            flow = int(round(1000.0 * (counter - prev["counter_l"]) / minutes + rng.normal(0, 4)))
            row = {"event": ei, "day": day, "time": t, "location": w, "kind": "reading", "flow_ml_min": flow,
                   "counter_l": counter, "temp_c": T, "spc": logged, "ph": round(prev["ph"] + rng.normal(0, 0.02), 2),
                   "do": round(max(prev["do"] * rng.uniform(1.25, 1.6), prev["do"] + 0.3), 2),
                   "orp": int(round(prev["orp"] + rng.uniform(10, 30))),
                   "turb": round(prev["turb"] + max(1.2, 0.15 * prev["turb"]) + rng.uniform(0.0, 1.3), 1),
                   "meter": x["meter"], "last": False, "after_sample": True}
            out.append(row)
            prev = row
    return out


def run():
    hd = heads()
    bgv, bgf, _ = background(hd)
    rev = {(w, ei): reversed_at(hd, w, ei) for w in W.BACKGROUND for ei in range(len(EV))}
    win = background_window(bgv)
    cmp_vals, cmp_frac, lim, plume_oct, lead, high, low = compliance(hd, win, rev)
    octvals = {}
    for w in W.COMPLIANCE:
        octvals[w] = (cmp_vals[(w, W.EVAL, "chloride")], cmp_vals[(w, W.EVAL, "sodium")])
    for w in W.BACKGROUND:
        octvals[w] = (bgv[(w, W.EVAL, "chloride")], bgv[(w, W.EVAL, "sodium")])
    frows, ftruth = field_records(octvals)
    frows = bottle_sets(sample_minutes(frows, ftruth), ftruth)
    return {"heads": hd, "bg": bgv, "bg_frac": bgf, "rev": rev, "bgwin": win, "cmp": cmp_vals, "cmp_frac": cmp_frac,
            "limits": lim, "plume_oct": plume_oct, "lead": lead, "high": high, "low": low,
            "field_rows": frows, "field_truth": ftruth}


if __name__ == "__main__":
    S = run()
    lim = S["limits"]
    for r in lim:
        print("%-44s" % r, " ".join("%8.2f" % lim[r][k] for k in W.INDICATORS))
    oc = {(w, k): S["cmp"][(w, W.EVAL, k)] for w in W.COMPLIANCE for k in W.INDICATORS}
    for r in lim:
        print("%-44s" % r, RT.designate(lim[r], oc))
    print("reversed:", sorted((w, EV[e]) for (w, e), v in S["rev"].items() if v and e < W.EVAL))
    print("plume", S["plume_oct"], S["lead"])
    for w in W.COMPLIANCE:
        print(w, [S["cmp"][(w, W.EVAL, k)] for k in W.INDICATORS])
