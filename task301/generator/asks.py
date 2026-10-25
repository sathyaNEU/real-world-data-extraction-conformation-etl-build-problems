"""The two asks' records.

Ask A: each farm's plane-of-array pyranometer in 2025. The logger integrates the sensor's voltage into millivolt-hours a
day; irradiation is that signal over the sensitivity of the sensor in the mast that day, as the certificate in force
gives it. Every farm's sensor went to the laboratory once in 2025 and a calibrated spare took its place. The logger's
sensor setting was not changed at the swap, so the station file names the sensor that left all year; the register (as at
31 December 2025) names the sensor in the mast now and the day it went in; the sensor that left was recalibrated after it
left, and the laboratory's certificate says which mast it came from. Days the logger did not record are not in the file.

Ask B: the O&M contractor's response to inverter fault alarms in 2025. The SCADA alarm log stamps alarms in UTC; the CMMS
stamps work orders in UK time, raised a few minutes after the alarm; the van tracker's portal exports site visits in UK
time. A technician's tablet stamps "attended" when the job is opened on site, and where the site has no mobile signal the
stamp is the moment the tablet next syncs, after the technician has left; the van tracker has the arrival either way."""
import datetime as dt
import zoneinfo

import numpy as np

import params as P

UK = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc


class AskTruth:
    pass


def _local(t_utc):
    return t_utc.astimezone(UK).replace(tzinfo=None)


# ---------------------------------------------------------------- ask A: pyranometers
def _off_centre(rng, v, unit):
    """a value inside the printed cell of v at unit, a little off its centre, never on it or near an edge"""
    c = round(v / unit) * unit
    return c + unit * float(rng.uniform(0.10, 0.25)) * (1 if rng.uniform() < 0.5 else -1)


def pyranometers(W):
    rng = np.random.default_rng(P.SEED_MET)
    days = [d.date() for d in W.days]
    i25 = [i for i, d in enumerate(days) if d.year == P.Y_ASK]
    farms = P.OPERATING
    nf = len(farms)
    # the sensor pool: one sensor in each mast at the start of 2025, a calibrated spare for each, and two more spares
    serials = sorted(set(int(x) for x in rng.choice(np.arange(140000, 189999), size=nf * 2 + 2, replace=False)))
    rng.shuffle(serials)
    base = 9.62
    sens = {s: base * float(rng.lognormal(0, 0.025)) for s in serials}      # sensitivity at its first certificate
    drift = {s: float(rng.uniform(0.006, 0.014)) for s in serials}           # loss of sensitivity a year
    in_mast = {f: serials[k] for k, f in enumerate(farms)}
    spares = serials[nf:]
    certs = []      # (serial, date, sensitivity, uncertainty, lab, sent from)
    first_cert = {}
    labs = ["Kipp Calibration Services (Delft)", "Solaris Metrology Ltd (Didcot)"]
    for s in serials:
        d0 = dt.date(2022, 1, 10) + dt.timedelta(days=int(rng.integers(0, 820)))
        if s in spares:
            d0 = dt.date(2024, 3, 1) + dt.timedelta(days=int(rng.integers(0, 300)))
        first_cert[s] = d0
        certs.append([s, d0, sens[s], 1.2 if rng.uniform() < 0.7 else 1.4, labs[int(rng.integers(0, 2))], "Stores"])

    def true_sens(s, d):
        return sens[s] * (1 - drift[s] * (d - first_cert[s]).days / 365.25)

    swap = {}
    order = list(farms)
    rng.shuffle(order)
    swap_days = sorted(int(x) for x in rng.choice(np.arange(70, 291), size=nf, replace=False))
    for f, sd in zip(order, swap_days):
        swap[f] = dt.date(2025, 1, 1) + dt.timedelta(days=sd)
    out_sensor, new_sensor = {}, {}
    pool = [(p, first_cert[p] + dt.timedelta(days=7)) for p in spares]      # (serial, on the shelf from)
    rng.shuffle(pool)
    for f in sorted(farms, key=lambda x: swap[x]):
        old = in_mast[f]
        so = true_sens(old, swap[f])
        shelf = [p for p, avail in pool if avail <= swap[f]]
        # stores send the first spare on the shelf whose sensitivity is not within 1.5 per cent of the outgoing one's
        pick = next((p for p in shelf if abs(true_sens(p, swap[f]) / so - 1) >= 0.015), None)
        if pick is None:
            pick = max(shelf, key=lambda p: abs(true_sens(p, swap[f]) / so - 1))
        pool = [(p, a_) for p, a_ in pool if p != pick]
        new = pick
        out_sensor[f], new_sensor[f] = old, new
        if (swap[f] - max(c[1] for c in certs if c[0] == new)).days > 365:
            cd = swap[f] - dt.timedelta(days=int(rng.integers(12, 40)))
            certs.append([new, cd, true_sens(new, cd) * float(rng.normal(1, 0.002)), 1.2, labs[int(rng.integers(0, 2))],
                          "Stores"])
        cd = swap[f] + dt.timedelta(days=int(rng.integers(21, 50)))
        certs.append([old, cd, true_sens(old, cd) * float(rng.normal(1, 0.002)), 1.2, labs[int(rng.integers(0, 2))],
                      "%s MET1" % f])
        pool.append((old, cd + dt.timedelta(days=int(rng.integers(5, 16)))))
    certs.sort(key=lambda c: (c[1], c[0]))
    cert_rows = []
    for k, (s, d, v, u, lab, frm) in enumerate(certs):
        cert_rows.append(["%s-%d-%04d" % ("KCS" if lab.startswith("Kipp") else "SML", d.year, 311 + 7 * k),
                          "SMP10-%d" % s, "SMP10", d, round(v, 2), u, lab, frm])
    by_serial = {}
    for c in cert_rows:
        by_serial.setdefault(c[1], []).append((c[3], c[4]))

    def valid(serial, d):
        cs = [x for x in by_serial[serial] if x[0] <= d]
        return max(cs)[1]

    def latest(serial):
        return max(by_serial[serial])[1]

    reg_sens = {f: valid("SMP10-%d" % new_sensor[f], dt.date(2025, 12, 31)) for f in farms}
    rows = []
    truth = {}
    for f in farms:
        S = W.site[f]
        bad = set(int(x) for x in rng.choice(i25, size=int(rng.integers(3, 11)), replace=False))
        noise = rng.normal(1, 0.002, len(i25))
        label = "SMP10-%d" % out_sensor[f]       # the logger's sensor setting, not changed at the swap

        def ratios(m):
            out, g, n_, la, ll, sat = [], 0.0, 0.0, 0.0, 0.0, 0.0
            for k, i in enumerate(i25):
                d = days[i]
                if i in bad or d == swap[f]:
                    continue
                s = out_sensor[f] if d < swap[f] else new_sensor[f]
                serial = "SMP10-%d" % s
                sig = round(S["poa"][i] * m * true_sens(s, d) * float(noise[k]), 3)
                out.append([d, f, "MET1", label, sig])
                g += sig / valid(serial, d)
                n_ += sig / reg_sens[f]
                la += sig / valid(label, d)
                ll += sig / latest(label)
                sat += round(float(S["poa_sat"][i]), 3)
            return out, g / sat, n_ / sat, la / sat, ll / sat
        # the 2012 to 2014 farms' arrays, and their met masts, stand at 30 degrees, a little over the weather file's 25
        # degree plane; each mast's own small tilt and shading leave its sensor a fraction of a per cent off the plane
        tilt = 1.011 if S["mod"] == "A" else 1.0
        _, r0, _, _, _ = ratios(tilt)
        m = tilt * _off_centre(rng, r0, 0.001) / r0
        out, r, rn, rla, rll = ratios(m)
        rows += out
        truth[f] = dict(swap=swap[f], old="SMP10-%d" % out_sensor[f], new="SMP10-%d" % new_sensor[f], ratio=r,
                        register=rn, label_asof=rla, label_latest=rll, days=len(out))
    reg = []
    for f in farms:
        s = "SMP10-%d" % new_sensor[f]
        reg.append([f, "MET1", s, "SMP10", "POA, %d degrees, due south" % (30 if W.site[f]["mod"] == "A" else 25),
                    reg_sens[f], swap[f]])
    return rows, reg, cert_rows, truth


# ---------------------------------------------------------------- ask B: alarm response
REGIONS = {"South West": ["Ashcombe", "Bramble Hill", "Wexcombe", "Furzedown"],
           "Wessex": ["Coldharbour", "Brindle Moor", "Hartsfield", "Fairoak", "Knowle Park"],
           "Thames and Chilterns": ["Greystoke Barns", "Jessop's Farm"],
           "East Anglia": ["Dunsford Lane", "Elmstead", "Ivy Cross"]}
TECHS = {"South West": ["T104", "T117"], "Wessex": ["T102", "T109", "T121"], "Thames and Chilterns": ["T111"],
         "East Anglia": ["T106", "T114"]}
CODES = [("F023", "Grid fault"), ("F101", "Insulation fault"), ("F045", "Overtemperature"), ("F310", "DC overcurrent"),
         ("F078", "Fan failure"), ("F152", "IGBT desaturation"), ("F207", "AC contactor fault")]
AUTO = [("W011", "Grid voltage out of range"), ("W014", "Grid frequency out of range"), ("W030", "Derating, temperature")]


def _plate(rng):
    L = "ABCDEFGHJKLMNOPRSTUVWXYZ"
    return "%s%s%d %s%s%s" % (L[int(rng.integers(0, 24))], L[int(rng.integers(0, 24))], int(rng.integers(19, 25)),
                              L[int(rng.integers(0, 24))], L[int(rng.integers(0, 24))], L[int(rng.integers(0, 24))])


def response(W):
    rng = np.random.default_rng(P.SEED_OM)
    region_of = {f: r for r, fs in REGIONS.items() for f in fs}
    offline = {f: float(rng.uniform(0.35, 0.80)) for f in P.OPERATING}     # share of visits with no signal on site
    travel = {f: float(rng.uniform(0.6, 2.4)) for f in P.OPERATING}         # hours from the depot
    techs = [t for r in TECHS for t in TECHS[r]]
    plates = []
    while len(plates) < len(techs) + 3:
        p = _plate(rng)
        if p not in plates:
            plates.append(p)
    van = {t: plates[k] for k, t in enumerate(techs)}
    # two technicians changed vans during the year, and one took a pool van while their own was in for service
    swaps = {"T109": (dt.date(2025, 5, 12), plates[len(techs)]), "T106": (dt.date(2025, 8, 4), plates[len(techs) + 1])}
    roster = []
    for t in techs:
        if t in swaps:
            d, newp = swaps[t]
            roster.append([t, van[t], dt.date(2025, 1, 1), d - dt.timedelta(days=1)])
            roster.append([t, newp, d, None])
        else:
            roster.append([t, van[t], dt.date(2025, 1, 1), None])
    roster.append(["T121", van["T109"], dt.date(2025, 6, 9), dt.date(2025, 6, 20)])

    def van_on(t, d):
        cur = [r for r in roster if r[0] == t and r[2] <= d and (r[3] is None or d <= r[3])]
        cur.sort(key=lambda r: r[2])
        return cur[-1][1]

    def working_morning(t):
        d = t.date() + dt.timedelta(days=1)
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        return dt.datetime.combine(d, dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(0, 50)))

    alarms, wos, corrective, other = [], [], [], []
    truth = {}
    wo_no = 250413
    al_no = 7_100_000
    windows = []      # (vehicle, site, raised utc, arrival utc) for every attended alarm
    for f in P.OPERATING:
        nb = len(W.site[f]["blocks"])
        older = W.site[f]["mod"] == "A"
        n = int(rng.integers(13, 26)) if older else int(rng.integers(7, 18))
        doy = sorted(int(x) for x in rng.choice(np.arange(5, 357), size=n, replace=False))
        tlist = TECHS[region_of[f]]
        resp = []
        jobs = []
        last_arrival = {}
        for dd in doy:
            day = dt.date(2025, 1, 1) + dt.timedelta(days=dd)
            loc = dt.datetime.combine(day, dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(0, 600)))
            raised_utc = loc.replace(tzinfo=UK).astimezone(UTC)
            inv = "INV%02d" % int(rng.integers(1, nb + 1))
            code = CODES[int(rng.integers(0, len(CODES)))]
            t = tlist[int(rng.integers(0, len(tlist)))]
            if loc.weekday() < 5 and loc.time() < dt.time(14, 30):
                leave = loc + dt.timedelta(minutes=int(rng.integers(20, 150)))
            else:
                leave = working_morning(loc)
            arrive = leave + dt.timedelta(hours=travel[f] * float(rng.uniform(0.85, 1.2)))
            arrive = arrive.replace(second=0, microsecond=0)
            repair = dt.timedelta(minutes=int(rng.integers(35, 230)))
            leave_site = arrive + repair + dt.timedelta(minutes=int(rng.integers(8, 25)))
            cleared = arrive + repair
            arrive_utc = arrive.replace(tzinfo=UK).astimezone(UTC)
            v = van_on(t, arrive.date())
            # an alarm raised while an earlier one at this farm still waits for this van would be attended on the
            # same visit: the contractor logs one alarm a visit, so such days are not drawn; nor is an alarm whose
            # technician changed vans between the alarm and the visit
            if v in last_arrival and raised_utc <= last_arrival[v]:
                continue
            if van_on(t, loc.date()) != v:
                continue
            # nor one whose wait spans a change of the clocks (the last Sundays of March and October)
            if (loc.replace(tzinfo=UK).utcoffset() != arrive.replace(tzinfo=UK).utcoffset()
                    or any(loc.date() <= dt.date(2025, mo, dd) <= arrive.date() for mo, dd in ((3, 30), (10, 26)))):
                continue
            last_arrival[v] = leave_site.replace(tzinfo=UK).astimezone(UTC)
            al_no += int(rng.integers(3, 40))
            off = rng.uniform() < offline[f]
            sync = leave_site + dt.timedelta(minutes=int(rng.integers(25, 140)))
            wo_no += int(rng.integers(1, 9))
            # the control room raises the work order a few minutes after the alarm comes in
            wo_raised = loc + dt.timedelta(minutes=int(rng.integers(4, 41)))
            jobs.append(dict(al=al_no, wo=wo_no, inv=inv, code=code, t=t, v=v, loc=loc, raised_utc=raised_utc,
                             wo_raised=wo_raised, arrive=arrive, repair=repair, leave_site=leave_site, off=off, sync=sync))
        # the contractor's dispatch log rounds the van's arrival to the minute; one job's travel is taken from the
        # tracker as it stood, so the farm's mean lands where the minutes put it
        hrs = [((j["arrive"].replace(tzinfo=UK).astimezone(UTC) - j["raised_utc"]).total_seconds() / 3600.0) for j in jobs]
        mean = float(np.mean(hrs))
        k = int(round((_off_centre(rng, mean, 0.1) - mean) * len(jobs) * 60))
        big = int(np.argmax(hrs))
        if k:
            j = jobs[big]
            dtk = dt.timedelta(minutes=k)
            j["arrive"] += dtk
            j["leave_site"] += dtk
            j["sync"] += dtk
        for j in jobs:
            arrive_utc = j["arrive"].replace(tzinfo=UK).astimezone(UTC)
            cleared = j["arrive"] + j["repair"]
            alarms.append([j["al"], f, j["inv"], j["code"][0], j["code"][1], j["raised_utc"],
                           cleared.replace(tzinfo=UK).astimezone(UTC)])
            if j["off"]:
                attended, completed = j["sync"], j["sync"] + dt.timedelta(minutes=1)
            else:
                attended, completed = j["arrive"], j["leave_site"]
            wos.append([j["wo"], f, j["inv"], j["al"], j["wo_raised"], j["t"], attended, completed, j["code"][1]])
            corrective.append([j["v"], f, arrive_utc, j["leave_site"].replace(tzinfo=UK).astimezone(UTC)])
            windows.append((j["v"], f, j["raised_utc"], arrive_utc))
            resp.append((arrive_utc - j["raised_utc"]).total_seconds() / 3600.0)
        for k in range(int(rng.integers(20, 70))):
            day = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(2, 362)))
            loc = dt.datetime.combine(day, dt.time(7, 30)) + dt.timedelta(minutes=int(rng.integers(0, 720)))
            code = AUTO[int(rng.integers(0, len(AUTO)))]
            al_no += int(rng.integers(1, 15))
            r_utc = loc.replace(tzinfo=UK).astimezone(UTC)
            alarms.append([al_no, f, "INV%02d" % int(rng.integers(1, nb + 1)), code[0], code[1], r_utc,
                           r_utc + dt.timedelta(minutes=int(rng.integers(3, 50)))])
        for q in range(6):
            day = dt.date(2025, 1 + 2 * q, 1) + dt.timedelta(days=int(rng.integers(3, 55)))
            while day.weekday() >= 5:
                day += dt.timedelta(days=1)
            t = tlist[int(rng.integers(0, len(tlist)))]
            a = dt.datetime.combine(day, dt.time(9, 0)) + dt.timedelta(minutes=int(rng.integers(0, 90)))
            other.append([van_on(t, day), f, a.replace(tzinfo=UK).astimezone(UTC),
                          (a + dt.timedelta(hours=float(rng.uniform(4.5, 7.5)))).replace(tzinfo=UK).astimezone(UTC)])
        truth[f] = dict(n=len(resp), mean=float(np.mean(resp)), resp=resp)
    # vans call in on their way past: a stop for parts or a word with the landowner, a few minutes on site
    for k in range(240):
        f = P.OPERATING[int(rng.integers(0, len(P.OPERATING)))]
        t = TECHS[region_of[f]][int(rng.integers(0, len(TECHS[region_of[f]])))]
        day = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(3, 360)))
        a = dt.datetime.combine(day, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 540)))
        other.append([van_on(t, day), f, a.replace(tzinfo=UK).astimezone(UTC),
                      (a + dt.timedelta(minutes=int(rng.integers(4, 18)))).replace(tzinfo=UK).astimezone(UTC)])
    # no preventive visit or pass by the attending van falls between an alarm and that van's arrival for it
    keep = [o for o in other if not any(o[0] == v and o[1] == f and r <= o[2] < a for v, f, r, a in windows)]
    visits = keep + corrective
    alarms.sort(key=lambda r: (r[5], r[0]))
    wos.sort(key=lambda r: r[0])
    visits.sort(key=lambda r: (r[2], r[0]))
    return alarms, wos, visits, roster, truth


def write(W, F, csvw):
    rows, reg, certs, ta = pyranometers(W)
    csvw(F["met"], ["date", "site", "station", "sensor_serial", "poa_signal_mvh"],
         [[d.isoformat(), f, st, s, "%.3f" % v] for d, f, st, s, v in rows])
    csvw(F["pyrreg"], ["site", "station", "sensor_serial", "model", "mounting", "sensitivity_uv_per_w_m2",
                       "installed"], [[a, b, c, m, mo, "%.2f" % s, d.isoformat()] for a, b, c, m, mo, s, d in reg])
    import docs
    docs.certificates(F["certs"], certs)
    alarms, wos, visits, roster, tb = response(W)
    fmt = lambda t: t.strftime("%Y-%m-%d %H:%M")
    csvw(F["alarms"], ["alarm_id", "site", "inverter", "code", "text", "raised_utc", "cleared_utc"],
         [[a, f, i, c, x, fmt(r), fmt(cl)] for a, f, i, c, x, r, cl in alarms])
    csvw(F["workorders"], ["work_order", "site", "asset", "alarm_ref", "raised", "assigned_to", "attended", "completed",
                           "fault"], [[w, f, a, ar, fmt(r), t, fmt(at), fmt(c), x] for w, f, a, ar, r, t, at, c, x in wos])
    # the van tracker's portal exports in UK time
    csvw(F["geofence"], ["vehicle", "site", "entered", "left"], [[v, f, fmt(_local(a)), fmt(_local(b))]
                                                               for v, f, a, b in visits])
    csvw(F["vans"], ["technician", "vehicle", "from", "to"],
         [[t, v, a.isoformat(), b.isoformat() if b else ""] for t, v, a, b in roster])
    W.ask_a, W.ask_b = ta, tb
