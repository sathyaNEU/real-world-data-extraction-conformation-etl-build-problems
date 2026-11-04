"""The golden from the pack alone: each well's water year 2026 volume (metered wells from their reads, the rest from
each interval's energy at that hour's total head), the ranch against the water available, the purchase, the static
depths and the energy charges; then the two deliverables. Every route checks.py and ceiling.py price runs here too."""
import csv
import datetime as dt
import math
import os

import bundle as B

KWH_AF_FT = 1.0241
MONTHS = [(2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 10)]


def load(target):
    reg = B.register(target)
    return dict(reg=reg, power=B.power(target, reg), log=B.loggers(target), hist=B.site_history(target, reg),
                tests=B.current_tests(target, reg), all_tests=B.tests(target, reg), reads=B.meter_reads(target),
                notice=B.notice(target), tariff=B.tariff(target), letter=B.rate_letter(target),
                dlog=B.download_log(target))


def stick(d, w):
    return float(d["reg"][w]["MP height above ground (ft)"])


def depth_gs(d, w, t_hour, baro_shift=0, swap_aware=True, compensate=True):
    """Depth to water below ground at a Pacific standard hour, from whichever logger sat in the well then."""
    s = B.serial_at(d["hist"], w, t_hour.astimezone(B.LA)) if swap_aware else str(d["reg"][w]["Logger S/N"])
    kind, vals = d["log"][s]
    v = vals.get(t_hour)
    if v is None:
        return None
    if kind == "vented":
        return v - stick(d, w)
    sensor = float(d["reg"][w]["Sensor depth (ft below MP)"])
    baro_s = [k for k, (kk, _) in d["log"].items() if kk == "baro"][0]
    b = d["log"][baro_s][1].get(t_hour + dt.timedelta(hours=baro_shift)) if compensate else 0.0
    if b is None:
        return None
    return sensor - (v - b) - stick(d, w)


# ----------------------------------------------------------------------------------------------- volumes
def meter_volumes(d):
    """Metered wells: months between first-of-month reads, the water year between the reads nearest 1 October."""
    per_af = {"acre-feet": 1.0, "gal x 1000": 325851.0 / 1000.0, "gal x 100": 325851.0 / 100.0}
    out = {}
    by = {}
    for r in d["reads"]:
        by.setdefault(r["Well"], []).append(r)
    for w, rows in by.items():
        rows.sort(key=lambda r: (r["Read date"], r["Read time"]))
        # cumulative acre-feet through the reads, rollovers and the exchange handled
        cum, last, last_sn, acc = [], None, None, 0.0
        for r in rows:
            val, unit, sn = float(r["Totalizer"]), r["Units"], r["Meter S/N"]
            if last is not None and sn == last_sn:
                delta = val - last
                if delta < 0 and unit != "acre-feet":
                    delta += 1_000_000
                acc += delta / per_af[unit]
            last, last_sn = val, sn
            cum.append((r["Read date"], r["Note"], acc))
        firsts = {}
        for day, note, a in cum:
            if day.endswith("-01") and not note:
                firsts[day[:7]] = a
        months = {}
        for y, m in MONTHS:
            k0 = "%d-%02d" % (y, m)
            y1, m1 = (y + (m == 12), m % 12 + 1)
            k1 = "%d-%02d" % (y1, m1)
            months[(y, m)] = firsts[k1] - firsts[k0]
        out[w] = dict(months=months, wy=firsts["2026-10"] - firsts["2025-10"])
    return out


def unmetered_volumes(d, route="golden", pair="mean", clock_shift_h=0, datum=True):
    """Each unmetered well's months and water year by a route:
    golden  each interval's kWh x the test's OPE / (1.0241 x the hour's total head),
            total head = the test's total head + (the hour's depth to water below ground - the test's pumping level)
    R0      kWh / the test's kWh per acre-foot
    R1      running time x the tested flow
    R3      the test's rate scaled by the pumping-level ratio alone
    monthly the golden with each month's mean pumping-hour level."""
    out = {}
    for w, rows in d["power"].items():
        if d["reg"][w]["Flow meter"] != "none":
            continue
        t = d["tests"][w]
        ope = t["ope"] / 100.0
        months = {k: 0.0 for k in MONTHS}
        mean_lvl = {}
        if route == "monthly":
            acc = {}
            for st, mins, kwh in rows:
                if kwh <= 0:
                    continue
                z = depth_gs(d, w, B.quarter_key(st))
                if z is not None:
                    loc = st.astimezone(B.LA)
                    acc.setdefault((loc.year, loc.month), []).append(z)
            mean_lvl = {k: sum(v) / len(v) for k, v in acc.items()}
        for st, mins, kwh in rows:
            loc = st.astimezone(B.LA)
            if not (B.WY0 <= loc < B.WY1) or kwh <= 0:
                continue
            if route == "R0":
                af = kwh / t["kwh_af"]
            elif route == "R1":
                kw = t["kw"]
                af = min(kwh / kw, mins / 60.0) * t["gpm"] * 60.0 / 325851.0
            else:
                q0 = B.quarter_key(st + dt.timedelta(hours=clock_shift_h))
                q1 = q0 + dt.timedelta(minutes=mins)
                if pair == "start":
                    z = depth_gs(d, w, q0)
                elif pair == "end":
                    z = depth_gs(d, w, q1)
                else:      # "mean": every logger reading from the interval's start to its end
                    zs = [depth_gs(d, w, q0 + dt.timedelta(minutes=15 * k)) for k in range(mins // 15 + 1)]
                    zs = [v for v in zs if v is not None]
                    z = sum(zs) / len(zs) if zs else None
                if z is None:
                    z = t["pwl"]
                if route == "monthly":
                    z = mean_lvl.get((loc.year, loc.month), z)
                if not datum:
                    z = z + stick(d, w)
                if route == "R3":
                    af = kwh / t["kwh_af"] * t["pwl"] / z
                else:
                    af = kwh * ope / (KWH_AF_FT * (t["th"] + z - t["pwl"]))
            months[(loc.year, loc.month)] += af
        out[w] = dict(months=months, wy=sum(months.values()))
    return out


def extraction(d, route="golden", **kw):
    met = meter_volumes(d)
    un = unmetered_volumes(d, route=route, **kw)
    vols = dict(met)
    vols.update(un)
    rep = {w: int(round(v["wy"])) for w, v in vols.items()}
    total = sum(rep.values())
    avail = d["notice"]["available"]
    block = d["notice"]["block"]
    excess = total - avail
    purchase = int(math.ceil(excess / block) * block) if excess > 0 else 0
    return dict(vols=vols, reported=rep, total=total, available=avail, excess=excess, purchase=purchase)


# ----------------------------------------------------------------------------------------------- static depths
def running_hours(d, w):
    """Instants (UTC) at which the pump drew energy, from both exports at their own resolution."""
    on = []
    for st, mins, kwh in d["power"][w]:
        if kwh > 0:
            on.append((st, st + dt.timedelta(minutes=mins)))
    return on


def static_depths(d, w, baro_shift=0, swap_aware=True, compensate=True):
    """The first reading in each window at which the pump had been off for at least the preceding 24 hours (off since
    the end of the last interval that drew energy)."""
    import bisect
    runs = sorted(running_hours(d, w))
    starts = [s for s, _ in runs]
    res = {}
    for name, w0, w1 in (("spring", dt.datetime(2026, 2, 1, tzinfo=B.LA), dt.datetime(2026, 4, 1, tzinfo=B.LA)),
                         ("fall", dt.datetime(2026, 10, 1, tzinfo=B.LA), dt.datetime(2026, 11, 1, tzinfo=B.LA))):
        t = B.quarter_key(w0)
        if t < w0:
            t += dt.timedelta(minutes=15)
        found = None
        while t < w1:
            tt = t.astimezone(B.UTC)
            i = bisect.bisect_right(starts, tt) - 1
            running_now = i >= 0 and runs[i][1] > tt
            last_end = runs[i][1] if i >= 0 else None
            if not running_now and (last_end is None or tt - last_end >= dt.timedelta(hours=24)):
                z = depth_gs(d, w, t.astimezone(B.PST), baro_shift=baro_shift, swap_aware=swap_aware,
                             compensate=compensate)
                if z is not None:
                    found = (t, z)
                    break
            t += dt.timedelta(minutes=15)
        res[name] = found
    return res


# ----------------------------------------------------------------------------------------------- energy charges
def energy_charges(d, schedule="letter", clock="aware", hourly=False):
    """April to September 2026 energy charges per well: each interval's kWh at its period's rate on the schedule in
    force (the register's current one, AG-2T before 1 June for the agreements the letter moved)."""
    letter_sas = set(d["letter"]["sas"])
    out = {}
    for w, rows in d["power"].items():
        sa_new = str(d["reg"][w]["Electric SA (from Apr 1, 2026)"])
        cur = d["reg"][w]["Rate schedule"]
        tot = 0.0
        agg = {}
        for st, mins, kwh in rows:
            if st < dt.datetime(2026, 4, 1, 7, tzinfo=B.UTC) or st >= dt.datetime(2026, 10, 1, 7, tzinfo=B.UTC):
                continue
            loc = st.astimezone(B.LA) if clock == "aware" else st.replace(tzinfo=B.LA)
            if hourly:
                key = loc.replace(minute=0)
                agg[key] = agg.get(key, 0.0) + kwh
                continue
            tot += kwh * _rate(d, cur, sa_new, letter_sas, loc, schedule)
        if hourly:
            for loc, kwh in agg.items():
                tot += kwh * _rate(d, cur, sa_new, letter_sas, loc, schedule)
        out[w] = tot
    return out


def _rate(d, cur, sa_new, letter_sas, loc, schedule):
    sch = cur
    if schedule == "letter" and sa_new in letter_sas and loc < d["letter"]["effective"]:
        sch = "AG-2T"
    season, per = B.period(loc)
    return d["tariff"][sch][season][per]


# ----------------------------------------------------------------------------------------------- deliverables
def figures(d):
    ex = extraction(d)
    st = {w: static_depths(d, w) for w in d["reg"]}
    ch = energy_charges(d)
    return dict(ex=ex, static=st, charges=ch)


def write_return(path, d, g):
    head = ["agency_well_id", "state_well_no", "apn", "aquifer", "method"] + \
        ["%s_%d_af" % (dt.date(y, m, 1).strftime("%b").lower(), y) for y, m in MONTHS] + \
        ["wy2026_af", "spring_2026_static_dtw_ft", "fall_2026_static_dtw_ft"]
    rows = []
    for w in sorted(d["reg"], key=lambda k: d["reg"][k]["Agency well ID"]):
        r = d["reg"][w]
        v = g["ex"]["vols"][w]
        meth = "METER" if r["Flow meter"] != "none" else "CALCULATED"
        sp, fa = g["static"][w]["spring"], g["static"][w]["fall"]
        rows.append([r["Agency well ID"], r["State well no."], r["APN"], str(r["Aquifer"]).upper(), meth] +
                    [int(round(v["months"][k])) for k in MONTHS] + [g["ex"]["reported"][w],
                                                                      "%.1f" % sp[1], "%.1f" % fa[1]])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(head)
        wr.writerows(rows)


def write_figures(path, d, g):
    import json
    ex = g["ex"]
    r0 = extraction(d, route="R0")
    r1 = extraction(d, route="R1")
    lower = [w for w in d["reg"] if str(d["reg"][w]["Aquifer"]) == "Lower"]
    sh = [1 - r0["vols"][w]["wy"] / ex["vols"][w]["wy"] for w in lower]
    fig = {
        "purchase_af": ex["purchase"], "ranch_af": ex["total"], "available_af": ex["available"],
        "allocation_af": d["notice"]["allocation"], "carryover_af": d["notice"]["carryover"],
        "excess_af": round(ex["excess"], 1), "excess_af_whole": int(round(ex["excess"])),
        "block_af": d["notice"]["block"], "purchase_usd": ex["purchase"] * 1185,
        "r0_ranch_af": r0["total"], "r0_inside_af": round(-r0["excess"], 1), "r0_inside_af_whole": int(round(-r0["excess"])),
        "r1_ranch_af": r1["total"], "deep_understatement_pct": [int(round(100 * min(sh))), int(round(100 * max(sh)))],
        "wells_af": {w: ex["reported"][w] for w in sorted(d["reg"])},
        "r0_wells_af": {w: r0["reported"][w] for w in sorted(d["reg"])},
        "static_dtw_ft": {w: {k: "%.1f" % v[1] for k, v in g["static"][w].items()} for w in sorted(d["reg"])},
        "energy_charge_usd": {w: int(round(g["charges"][w])) for w in sorted(d["reg"])},
        "energy_charge_total_usd": sum(int(round(v)) for v in g["charges"].values()),
        "tests": {w: {"date": str(t["date"]), "pwl_ft": t["pwl"], "total_head_ft": t["th"], "ope_pct": t["ope"],
                      "kwh_per_af": t["kwh_af"]} for w, t in sorted(d["tests"].items())},
        "acre_foot_gal": 325851, "kwh_af_ft": KWH_AF_FT, "transfer_price_usd": 1185, "uncovered_charge_usd": 1500,
        "metered_af": sum(ex["reported"][w] for w in d["reg"] if d["reg"][w]["Flow meter"] != "none"),
        "unmetered_af": sum(ex["reported"][w] for w in d["reg"] if d["reg"][w]["Flow meter"] == "none"),
        "lower_af": sum(ex["reported"][w] for w in lower), "blocks": ex["purchase"] // d["notice"]["block"],
        "band_pct": {"well": 1, "ranch": 0.5}, "switched_accounts": len(d["letter"]["sas"]),
        "true_up_day": 15, "fall_back_day": 2,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig


def build(target, gdir, figures_path=None):
    import memo as M
    os.makedirs(gdir, exist_ok=True)
    for f in os.listdir(gdir):
        os.remove(os.path.join(gdir, f))
    d = load(target)
    g = figures(d)
    write_return(os.path.join(gdir, "wy2026_extraction_return.csv"), d, g)
    M.write(os.path.join(gdir, "transfer_purchase_memo.docx"), d, g)
    if figures_path:
        write_figures(figures_path, d, g)
    return g
