"""What the network's instruments and people recorded of the true levels: manual dips (with the field team's
habits), hourly unvented logger pressures in UTC, the site barometric logger. Returns rows and a private truth
table (which dips were pumped or keyed twice, the measuring point used) that only checks.py reads."""
import datetime as dt
import math

import numpy as np

import sim as S
import world as W

PUMPED_REMARKS = ["pump on", "Pump running", "PUMP ON", "pump running, landholder could not turn off",
                  "stock pump going", "pumping when we arrived", "solar pump running", "pumped level",
                  "pump on - couldn't isolate", "Pump going, level drawn down"]
# The dips stream draws one index into a list of this length for every plain remark; the draw is kept so that every
# later draw on the stream (noise, pumped dips, keyed duplicates) stays where it was, and the remark itself is chosen
# on its own stream from what the officer could actually see that day (plain_remark()).
N_PLAIN_DRAW = 25
DOWNLOAD_REMARKS = ["logger downloaded, check dip", "LL download + check dip", "logger dl ok, check dip",
                    "downloaded logger, manual check"]
# Pumped remarks that fit the bore's headworks; every one names the pump, so the remark and the outlier rule still
# agree on every pumped dip.
PUMPED_FOR = {"windmill": ["mill pumping, could not stop it", "pumping, mill in gear", "pumped level",
                           "Pump going, level drawn down"],
              "solar submersible": ["solar pump running", "pump on", "Pump running", "pumping when we arrived",
                                    "pumped level", "pump on - couldn't isolate"],
              "electric submersible": ["pump on", "Pump running", "PUMP ON", "pump running, landholder could not turn off",
                                       "stock pump going", "pumping when we arrived", "pumped level",
                                       "pump on - couldn't isolate", "Pump going, level drawn down"]}
# Plain remarks. None mentions the pump or reads as a dry or doubtful reading.
HEADWORKS_REMARKS = {"windmill": ["bees in mill stand", "mill stand ladder loose", "tail chain broken on mill"],
                     "solar submersible": ["solar panels dusty", "panel frame loose", "controller box lid missing"],
                     "electric submersible": ["switchboard door broken", "green ants in switchboard"]}
LANDHOLDER_REMARKS = ["cattle at trough", "cap rusted, used shifter", "wasps in headworks", "new padlock fitted",
                      "grass long around headworks", "green ants on cap", "snake under bore slab"]
REFERENCE_REMARKS = {"road reserve": ["grader working on road", "road reserve fence down", "marker post replaced"],
                     "stock route": ["stock on route, waited", "marker post replaced", "cattle camped at bore"]}
MINE_REMARKS = ["via pit perimeter road", "waited for blast clearance", "haul road crossing closed, went round",
                "bollard knocked over, reported", "cap padlock replaced"]
EIS_REMARKS = ["TOC N side", "ft dipper", "SWL, TOC N", "access OK", "cattle in yard", "gate locked, rang owner"]
# A few bores have a note the officers write again and again
HABIT = {"CM2": "dogs tied up", "CM4": "via dam paddock gate", "A6": "access via north gate",
         "A8": "waterhole track rough", "B3": "gate locked, key from homestead", "B4": "ridge track, 4WD"}
BASELINE_REMARK = "MG-02 baseline assessment, pump off since previous evening"
# Pumped dips in the assessment month (September 2026): which bores and which run
SEP_PUMPED = {"CM4": 2, "A5": 1, "B1": 3}
PUMP_DRAW = {"alluvium": (1.7, 2.8), "basalt": (2.8, 5.2), "coal": (3.4, 7.5)}


def mp_on(label, day):
    """Measuring point elevation in force on a date."""
    b = W.BY_LABEL[label]
    mp0 = round(b["gl"] + W.MP_STICKUP[label], 3)
    if label in W.MP_RESURVEY and day >= W.MP_RESURVEY[label][0]:
        return round(b["gl"] + W.MP_RESURVEY[label][1], 3)
    return mp0


def weekday_on_or_after(day):
    while day.weekday() >= 5:
        day += dt.timedelta(days=1)
    return day


def run_days(start, n):
    out, d = [], weekday_on_or_after(start)
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


ROUTE = ["MC1", "MC2", "MC3", "MC4", "MA1", "MA2", "CM1", "CM3", "CM4", "CM2", "A1", "A2", "A5", "A3", "A4",
         "A6", "A7", "A8", "A9", "RA2", "CM5", "B3", "B2", "B1", "B4", "RA1", "RB1"]


def schedule():
    """Every visit: (label, local datetime, purpose)."""
    r = W.rng("schedule")
    visits = []

    def campaign(days, sites, purpose, t0=(8, 5)):
        per = math.ceil(len(sites) / len(days))
        for i, lab in enumerate(sites):
            day = days[min(i // per, len(days) - 1)]
            k = i % per
            minutes = t0[0] * 60 + t0[1] + k * int(r.integers(38, 62)) + int(r.integers(0, 12))
            visits.append((lab, dt.datetime.combine(day, dt.time(min(minutes // 60, 17), minutes % 60)), purpose))

    for y, m in W.EIS_ROUNDS:
        campaign(run_days(dt.date(y, m, int(r.integers(8, 15))), 4), ROUTE, "eis")
    m = W.MONTHLY_FROM
    while m <= dt.date(2026, 9, 1):
        if (m.year, m.month) == (2026, 9):
            start = dt.date(2026, 9, 1)
        elif (m.year, m.month) == (2026, 8):
            start = dt.date(2026, 8, 4)
        else:
            start = dt.date(m.year, m.month, int(r.integers(2, 11)))
        days = run_days(start, 3)
        sites = [s for s in ROUTE if not (r.random() < 0.035 and not (m.year == 2026 and m.month >= 8)
                                           and not (m.year == 2022 and m.month in (4, 5, 6)))]
        download = m.month in (1, 4, 7, 10) and m >= dt.date(2015, 7, 1)
        campaign(days, sites, "monthly-dl" if download else "monthly", t0=(7, 40))
        m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    lh = [s for s in ROUTE if W.BY_LABEL[s]["kind"] == "landholder"]
    for start in (dt.date(2026, 8, 18), dt.date(2026, 9, 15), dt.date(2026, 9, 28)):
        campaign(run_days(start, 3 if start.day != 28 else 2), lh, "fortnightly", t0=(7, 50))
    for lab in lh:
        b = W.BY_LABEL[lab]
        visits.append((lab, dt.datetime.combine(b["base"], dt.time(9 + int(r.integers(0, 5)), int(r.integers(0, 6)) * 10)),
                       "baseline"))
    logged = [s for s in ROUTE if W.BY_LABEL[s]["logged"]]
    campaign(run_days(W.DOWNLOAD_FINAL[0], 4), logged, "final-download", t0=(8, 20))
    visits.sort(key=lambda v: (v[1], ROUTE.index(v[0])))
    return visits


def sep_run(when):
    """Which of the three September 2026 runs a visit belongs to (0 if none)."""
    d = when.date()
    if d.year != 2026 or d.month != 9:
        return 0
    return 1 if d.day <= 10 else (2 if d.day <= 20 else 3)


def site_as_recorded(label, purpose, r):
    b = W.BY_LABEL[label]
    code = b["code"]
    if purpose == "eis":
        return ("RN " + b["rn"]) if r.random() < 0.55 else b["rn"]
    u = r.random()
    if u < 0.07:
        return code.replace("-", "")
    if u < 0.11:
        return code.split("-", 1)[1]
    if u < 0.135:
        return code.replace("-", " ", 1)
    if u < 0.15:
        return code.lower()
    return code


def officer(when, purpose):
    if purpose == "eis":
        return "IVH"
    if purpose == "baseline":
        return "RQ"
    d = when.date()
    if d < dt.date(2019, 1, 1):
        return "JH"
    return "NC" if (d.toordinal() // 30) % 11 else "EM"


def weather(clim, when):
    """What the officer could see of the weather at a visit, from the gridded climate (rainfall is the 24 hours to
    9 am on the date, so rain during a visit after 9 am is in the next day's total)."""
    i = S.idx(when.date())
    rain = clim["rain"]
    now = rain[i] if when.hour < 9 else rain[i + 1]
    out = []
    if now >= 20:
        out.append("heavy rain")
    elif now >= 5:
        out += ["showers", "rain during visit"]
    elif now >= 0.4:
        out += ["light rain", "drizzle"]
    prev3 = rain[i] + rain[i - 1] + rain[i - 2]
    if prev3 >= 10 and now < 20:
        out += ["road wet, 4WD", "tracks boggy, 4WD"]
    if clim["tmax"][i] >= 37.5 and when.hour >= 11:
        out += ["hot", "very hot"]
    if clim["tmin"][i] <= 2.0 and when.hour < 9:
        out.append("frost on the flat")
    if rain[i - 30:i + 1].sum() < 1.0 and when.month in (8, 9, 10, 11):
        out += ["dust about", "dust on the road"]
    return out, prev3


def plain_remark(lab, when, purpose, clim, rr, first_eis):
    """A plain remark, or none, for a static dip: access, the headworks, stock or the weather that day."""
    b = W.BY_LABEL[lab]
    seen, prev3 = weather(clim, when)
    if purpose == "eis":
        if first_eis:
            return "MP marked TOC N side"
        if seen and rr.random() < 0.35:
            return seen[int(rr.integers(0, len(seen)))]
        return EIS_REMARKS[int(rr.integers(0, len(EIS_REMARKS)))] if rr.random() < 0.22 else ""
    if seen and rr.random() < 0.4:
        text = seen[int(rr.integers(0, len(seen)))]
    elif (b["kind"] == "landholder" and b["unit"] == "alluvium" and prev3 >= 40 and rr.random() < 0.6):
        text = "creek up at crossing, went round"
    elif lab in HABIT and rr.random() < 0.3:
        text = HABIT[lab]
    elif rr.random() < 0.16:
        if b["kind"] == "mine":
            pool = MINE_REMARKS
        elif b["kind"] == "reference":
            pool = REFERENCE_REMARKS[b["prop"]]
        else:
            who = "owner present" if b["owner"] in W.PEOPLE.values() else "manager present"
            pool = LANDHOLDER_REMARKS + HEADWORKS_REMARKS.get(b["pump"], []) + [who]
        text = pool[int(rr.integers(0, len(pool)))]
    else:
        text = ""
    if text and officer(when, purpose) == "EM":
        text = text[0].upper() + text[1:]
    return text


def pumped_remark(lab, idx, rr):
    """The pumped remark the dips stream drew, or one that fits the bore's headworks in its place."""
    text = PUMPED_REMARKS[idx]
    fits = PUMPED_FOR[W.BY_LABEL[lab]["pump"]]
    return text if text in fits else fits[int(rr.integers(0, len(fits)))]


def mine_logger_events():
    """The two mine-bore loggers' own history (never in the landholder or reference records). KV-MB01's sensor drifts
    and is re-hung at some downloads, its battery went flat in 2018 and it was out for a headworks repair in 2023;
    KV-MB03's was re-hung high at the October 2019 download and put back at the January 2020 one, stopped in
    September 2016 and was out for road works in June 2024. None of it touches April to June 2022 or September
    2026, the windows the evidence on the mine's bores reads. Returns {serial: dict(drift, steps, gaps)} with UTC
    datetimes, and the remarks the officers wrote at those visits {(label, local datetime): remark}."""
    rr = W.rng("mine-loggers")
    utc = lambda s: dt.datetime.fromisoformat(s).replace(tzinfo=W.AEST).astimezone(W.UTC)
    vis = schedule()
    dl = {lab: [v[1] for v in vis if v[0] == lab and v[2] in ("monthly-dl", "final-download")] for lab in ("MA1", "MC1")}
    first_after = lambda lab, s: min(x for x in dl[lab] if x > dt.datetime.fromisoformat(s))
    remarks = {}
    # KV-MB01
    steps = []
    for when in dl["MA1"]:
        if dt.date(2016, 1, 1) <= when.date() <= dt.date(2026, 8, 31) and rr.random() < 0.28:
            steps.append((utc(when.isoformat(sep=" ")), float(rr.normal(0, 0.11))))
            remarks[("MA1", when)] = "logger re-hung after download"
    flat = "2018-08-27 15:00"
    back = first_after("MA1", flat)
    remarks[("MA1", back)] = "logger flat, new battery, restarted"
    out_from, out_to = "2023-05-09 08:40", "2023-05-22 10:15"
    steps.append((utc(out_to), 0.17))
    ma1 = dict(drift=(0.061, 0.0023), steps=steps,
               gaps=[(utc(flat), utc(back.isoformat(sep=" "))), (utc(out_from), utc(out_to))],
               start=utc("2015-05-12 15:20"))
    # KV-MB03
    snag = first_after("MC1", "2019-10-01 00:00")
    reset = first_after("MC1", "2020-01-01 00:00")
    remarks[("MC1", reset)] = "logger cable caught on cap, re-hung"
    stop = "2016-09-14 03:00"
    restart = first_after("MC1", stop)
    remarks[("MC1", restart)] = "logger stopped 14/09, restarted"
    mc1 = dict(drift=(0.0, 0.0), steps=[(utc(snag.isoformat(sep=" ")), -0.44), (utc(reset.isoformat(sep=" ")), 0.44)],
               gaps=[(utc(stop), utc(restart.isoformat(sep=" "))), (utc("2024-06-11 09:30"), utc("2024-06-20 14:10"))],
               start=utc("2015-05-12 16:10"))
    return {"2041956": ma1, "2041964": mc1}, remarks


def dips(hd, clim):
    """Manual dip rows as keyed from the field sheets, and the private truth for each row."""
    r = W.rng("dips")
    rr = W.rng("remarks")
    _, event_remarks = mine_logger_events()
    eis_seen = set()
    rows, truth = [], []
    entry = 1000
    vis = schedule()
    batches = {}
    for lab, when, purpose in vis:
        key = (when.date().year, when.date().month, purpose == "baseline")
        batches.setdefault(key, []).append((lab, when, purpose))
    for key in sorted(batches):
        batch = batches[key]
        dup_pick = []
        for lab, when, purpose in batch:
            b = W.BY_LABEL[lab]
            day = when.date()
            h = hd[lab]["h"][S.idx(day)] + r.normal(0, 0.004)
            mp = mp_on(lab, day)
            pumped = False
            run = sep_run(when)
            if b["kind"] == "landholder" and not b["logged"] and b["pump"] != "none" and purpose != "baseline":
                if run:
                    pumped = SEP_PUMPED.get(lab) == run
                else:
                    pumped = r.random() < (0.05 if day.year < 2023 else 0.07)
            if pumped:
                lo, hi = PUMP_DRAW[b["unit"]]
                h -= r.uniform(lo, hi)
            depth_m = mp - h
            if purpose == "eis":
                value, units = round(depth_m / W.FT, 2), "ft"
            else:
                value, units = round(depth_m, 2), "m"
            first_eis = purpose == "eis" and lab not in eis_seen
            if purpose == "eis":
                eis_seen.add(lab)
            if pumped:
                remark = pumped_remark(lab, int(r.integers(0, len(PUMPED_REMARKS))), rr)
            elif purpose == "baseline":
                remark = BASELINE_REMARK
            elif purpose in ("monthly-dl", "final-download") and b["logged"]:
                remark = DOWNLOAD_REMARKS[int(r.integers(0, len(DOWNLOAD_REMARKS)))]
                remark = event_remarks.get((lab, when), remark)
            else:
                r.integers(0, N_PLAIN_DRAW)
                remark = plain_remark(lab, when, purpose, clim, rr, first_eis)
            row = dict(entry_no=entry, reading_date=day.isoformat(), reading_time=when.strftime("%H:%M"),
                       site=site_as_recorded(lab, purpose, r), dtw=value, units=units, remarks=remark,
                       officer=officer(when, purpose))
            rows.append(row)
            truth.append(dict(entry_no=entry, label=lab, day=day, pumped=pumped, dup=False, mp=mp, purpose=purpose,
                              depth_m=value * (W.FT if units == "ft" else 1.0), run=run, raw_m=depth_m))
            entry += 1
            if (not pumped and purpose in ("monthly", "eis") and not (day.year == 2026 and day.month == 9)
                    and r.random() < 0.007):
                dup_pick.append(len(rows) - 1)
        for i in dup_pick:
            row = dict(rows[i])
            row["entry_no"] = entry
            rows.append(row)
            t = dict(truth[i])
            t["entry_no"], t["dup"] = entry, True
            truth.append(t)
            entry += 1
    return rows, truth


# ------------------------------------------------------------------ the loggers

def utc_hours(start_local, end_local):
    a = dt.datetime.fromisoformat(start_local).replace(tzinfo=W.AEST).astimezone(W.UTC)
    b = dt.datetime.fromisoformat(end_local).replace(tzinfo=W.AEST).astimezone(W.UTC)
    a = (a + dt.timedelta(minutes=59)).replace(minute=0, second=0, microsecond=0)
    n = int((b - a).total_seconds() // 3600) + 1
    return a, n


def baro():
    """Site barometric logger: hourly absolute pressure (kPa) on the hour, UTC."""
    r = W.rng("baro")
    a, n = utc_hours(W.BARO_FROM, "2026-10-06 16:00")
    hours = np.arange(n)
    t = np.array([a + dt.timedelta(hours=int(h)) for h in hours])
    doy = np.array([x.timetuple().tm_yday for x in t])
    seasonal = 0.35 * np.cos(2 * np.pi * (doy - 196) / 365.25)
    z = r.normal(0, 0.6 * math.sqrt(1 - 0.996 ** 2), n)
    syn = np.empty(n)
    syn[0] = 0.0
    for i in range(1, n):
        syn[i] = 0.996 * syn[i - 1] + z[i]
    utc_h = np.array([x.hour for x in t])
    local_h = (utc_h + 10) % 24
    tide = 0.11 * np.cos(2 * np.pi * (local_h - 10) / 12.0) + 0.04 * np.cos(2 * np.pi * (local_h - 4) / 24.0)
    p = np.round(98.07 + seasonal + syn + tide + r.normal(0, 0.006, n), 3)
    temp = np.round(26.5 + 7.5 * np.cos(2 * np.pi * (doy - 15) / 365.25) + 5.0 * np.cos(2 * np.pi * (local_h - 15) / 24.0)
                    + r.normal(0, 0.6, n), 1)
    keep = np.ones(n, bool)
    for g0, g1 in W.BARO_GAPS:
        g0 = dt.datetime.fromisoformat(g0).replace(tzinfo=W.UTC)
        g1 = dt.datetime.fromisoformat(g1).replace(tzinfo=W.UTC)
        keep &= ~np.array([(g0 <= x <= g1) for x in t])
    return t[keep], p[keep], temp[keep], dict(zip(t, p))


def loggers(hd, baro_map):
    """Hourly rows per installation: (serial, label, utc datetimes, kPa, deg C) and the installation table."""
    r = W.rng("loggers")
    events, _ = mine_logger_events()
    out, installs = [], []
    final = {}
    vis = [v for v in schedule() if v[2] == "final-download"]
    for lab, when, _ in vis:
        final[lab] = when
    for lab in W.LOGGED:
        for k, (serial, inst, removed, sensor) in enumerate(W.LOGGER_INSTALLS[lab]):
            end = removed or final[lab].strftime("%Y-%m-%d %H:%M")
            a, n = utc_hours(inst, end)
            if removed is None:
                n -= 1
            t = np.array([a + dt.timedelta(hours=int(i)) for i in range(n)])
            keep = np.array([x in baro_map for x in t])
            for g0, g1 in W.LOGGER_GAPS.get(lab, []):
                g0 = dt.datetime.fromisoformat(g0).replace(tzinfo=W.UTC)
                g1 = dt.datetime.fromisoformat(g1).replace(tzinfo=W.UTC)
                keep &= ~np.array([(g0 <= x <= g1) for x in t])
            t = t[keep]
            local = [x.astimezone(W.AEST) for x in t]
            # true level at the hour: daily values set at local midday, linear between them
            fd = np.array([(x.date() - S.T0).days + (x.hour + x.minute / 60.0 - 12.0) / 24.0 for x in local])
            h = np.interp(fd, np.arange(S.N), hd[lab]["h"]) + r.normal(0, 0.003, len(t))
            mp = np.array([mp_on(lab, x.date()) for x in local])
            column = h - (mp - sensor)
            p = np.array([baro_map[x] for x in t]) + W.KPA_PER_M * column + r.normal(0, 0.006, len(t))
            r.normal(0, 0.03, len(t))       # the stream's old temperature draw, kept so later loggers' draws stay put
            temp = logger_temperature(serial, lab, t, sensor)
            if serial in events:
                eff, keep = instrument(events[serial], t)
                p = p + eff
                t, p, temp = t[keep], p[keep], temp[keep]
            out.append((serial, lab, t, np.round(p, 3), temp))
            installs.append(dict(serial=serial, label=lab, installed=inst, removed=removed or "", sensor=sensor, n=len(t)))
    return out, installs


def logger_temperature(serial, lab, t, sensor):
    """Water temperature at the sensor (deg C): the ground's temperature at that depth (about 2.8 degrees per 100 m
    below a shallow 23.6), the bore's own departure from it, a small annual swing at the shallow sensors, the
    sensor's offset and slow drift, and the first hours after installation while the logger cooled from the air."""
    rt = W.rng("temperature-" + serial)
    z = sensor - W.MP_STICKUP[lab]
    ground = 23.6 + 0.028 * z + W.rng("ground-temperature-" + lab).normal(0, 0.22)
    secs = np.array([(x - t[0]).total_seconds() for x in t])
    years = secs / (365.25 * 86400)
    doy = np.array([x.timetuple().tm_yday for x in t])
    swing = 0.55 * math.exp(-z / 6.5) * np.cos(2 * np.pi * (doy - 40) / 365.25 - z / 6.5)
    offset = rt.normal(0, 0.06)
    drift = rt.uniform(-0.004, 0.011) * years
    air, tau = rt.uniform(26.5, 31.0), rt.uniform(0.6, 1.4)
    settle = (air - ground) * np.exp(-(secs / 3600.0 + 0.5) / tau)
    temp = ground + offset + swing + drift + settle + rt.normal(0, 0.004, len(t))
    return np.round(temp, 3 if serial in ("2190446", "2213378") else 2)


def instrument(ev, t):
    """A mine-bore logger's drift and re-hang steps (kPa, added to the reading) and the hours it did not record."""
    secs = np.array([(x - ev["start"]).total_seconds() for x in t])
    years = secs / (365.25 * 86400)
    a, b = ev["drift"]
    eff = a * years + b * years ** 2
    for when, kpa in ev["steps"]:
        eff = eff + np.where(np.array([x >= when for x in t]), kpa, 0.0)
    keep = np.ones(len(t), bool)
    for g0, g1 in ev["gaps"]:
        keep &= ~np.array([(g0 <= x < g1) for x in t])
    return eff, keep
