"""Larkhaven Transit's two GTFS feeds (the winter timetable from 1 January 2026 and the spring timetable from 5 April
2026): the trips each service runs, each trip's departure from its route's designated stop, and the feed files. The
simulator reads its scheduled departures from here, so the record and the feeds agree."""
import csv
import datetime as dt
import io
import zipfile

import numpy as np

import world as W

FEEDS = {"2601": dict(start=dt.date(2026, 1, 1), end=dt.date(2026, 4, 4), file="gtfs_jan", published="20251212"),
         "2604": dict(start=dt.date(2026, 4, 5), end=dt.date(2026, 8, 29), file="gtfs_apr", published="20260313")}
SERVICES = {"2601": {"WKD": "1111100", "SAT": "0000010", "SUN": "0000001", "UNIV": "0000000"},
            "2604": {"MTH": "1111000", "FRI": "0000100", "SAT": "0000010", "SUN": "0000001", "UNIV": "0000000"}}
JITTER = {"2": 2, "4": 1, "17": 3, "3": 0, "6": 2, "9": 1, "11": 0, "14": 2, "22": 1, "12": 0, "31": 2, "40": 3,
          "51": 2, "60": 0}
STREETS = {"2": ["Grand Ave & Northside Loop", "Grand Ave & 22nd St", "Grand Ave & 12th St", "Grand Ave & Pine St",
                 "Grand Ave & Southridge Rd", "Southridge Park & Ride"],
           "4": ["Lincoln Ave & Kellogg Dr", "Lincoln Ave & 18th St", "Lincoln Ave & 7th St", "Lincoln Ave & Ash St",
                 "Lincoln Ave & Hartwell Rd"],
           "17": ["Prairie Rd & Meadowbrook Dr", "Prairie Rd & 30th St", "Prairie Rd & 14th St",
                  "Prairie Rd & Cottonwood Ave", "Prairie Rd & County Line Rd", "Prairie Crossing"],
           "3": ["Westside Dr & Fenwick Ave", "Westside Dr & 9th St", "Westside Dr & Larch St", "Westside Medical Plaza"],
           "6": ["Oak St & Bellamy Rd", "Oak St & 16th St", "Oak St & 3rd St", "Oak St & Riverbend Dr", "Oak Grove Center"],
           "9": ["Riverside Dr & Mill St", "Riverside Dr & 12th St", "Riverside Dr & Tannery Ln", "Riverside Commons"],
           "11": ["Union Station", "College Dr & Pell St", "University Ave & Stadium Dr", "Science Park"],
           "14": ["Union Station", "Elm St & 5th St", "Elm Park Blvd & Holloway Rd", "Elm Park Plaza"],
           "22": ["Union Station", "Fairgrounds Rd & 8th St", "Fairgrounds Rd & Quarry Rd", "Expo Center",
                  "Fairgrounds Rd & Linden Ave"],
           "12": ["Union Station", "Northgate Rd & 19th St", "Northgate Rd & Brookfield Dr", "Northgate Mall"],
           "31": ["Hillview Rd & Summit Ave", "College Dr & Pell St", "College Hill Rd & Ridge St", "College Hill Apartments"],
           "40": ["Westgate Transit Center", "Crosstown Blvd & Sheridan Ave", "Crosstown Blvd & 21st St",
                  "Crosstown Blvd & Ferris Rd", "Eastgate Shopping Center"],
           "51": ["Westgate Transit Center", "Hillcrest Dr & Overlook Rd", "Hillcrest Dr & Canterbury Ln", "Hillcrest Medical"],
           "60": ["Westgate Transit Center", "Mill Creek Rd & Old Post Rd", "Mill Creek Rd & Sawyer Ln", "Mill Creek Village"]}


OPPOSITE = {"A": "Main St & 4th St (Transit Mall, bay D)", "B": "Main St & 9th St (northbound)",
            "C": "Union Station (arrivals)", "D": "University Ave & College Dr (eastbound)",
            "E": "Westgate Transit Center (arrivals)"}


def _offsets():
    rng = np.random.default_rng([W.SEED, 100])
    return {r: float(rng.random()) for r in W.SCHED}


ROUTE_OFFSET = _offsets()


def service_counts(fd, svc, route):
    """Scheduled departures an hour from the designated stop for one service of one feed."""
    base = dict(W.SCHED[route])
    if fd == "2604":
        for (r, h), v in W.APRIL_CHANGES.items():
            if r == route:
                base[h] = v
    if svc in ("WKD", "MTH"):
        return base
    if svc == "FRI":
        for (r, h), v in W.FRIDAY_EXTRA.items():
            if r == route:
                base[h] = base[h] + v
        return base
    if svc in ("SAT", "SUN"):
        share = W.SATURDAY_SHARE if svc == "SAT" else W.SUNDAY_SHARE
        return {h: (max(1, int(round(v * share))) if v else 0) for h, v in base.items()}
    if svc == "UNIV":
        return {h: (W.UNIV_EXTRA.get(h, 0) if route == "31" else 0) for h in base}
    raise KeyError(svc)


def minutes(fd, svc, route):
    """Departure minutes after the service day's midnight at the designated stop (over 1,440 after midnight)."""
    s = service_counts(fd, svc, route)
    out = []
    jit = JITTER[route]
    for h in range(5, 26):
        n = s.get(h, 0)
        if not n:
            continue
        if frequency_window(route, svc) and 6 <= h < 19:
            out.extend(h * 60 + 10 * k for k in range(n))
            continue
        step = 60.0 / n
        base = ROUTE_OFFSET[route] * step if svc != "UNIV" else step / 2 + ROUTE_OFFSET[route] * step / 2
        for k in range(n):
            m = h * 60 + base + k * step + ((jit if k % 2 else -jit) if n > 2 else 0)
            out.append(int(round(min(max(m, h * 60), h * 60 + 59))))
    return sorted(set(out))


def frequency_window(route, svc):
    return route == W.FREQUENCY_BASED and svc in ("WKD", "MTH", "FRI")


def services_on(d):
    """The feed and the service_ids a date runs, by the feeds' calendars and calendar_dates."""
    fd = W.feed(d)
    if fd == "2601":
        if d in W.STATE_HOLIDAYS:
            svc = ["SUN"]
        elif d == W.GOOD_FRIDAY:
            svc = ["SAT"]
        else:
            svc = ["WKD"] if d.weekday() < 5 else (["SAT"] if d.weekday() == 5 else ["SUN"])
    else:
        if d in W.STATE_HOLIDAYS:
            svc = ["SUN"]
        elif d.weekday() < 4:
            svc = ["MTH"]
        elif d.weekday() == 4:
            svc = ["FRI"]
        else:
            svc = ["SAT"] if d.weekday() == 5 else ["SUN"]
    if W.class_day(d) and svc[0] in ("WKD", "MTH", "FRI"):
        svc = svc + ["UNIV"]
    return fd, svc


def operated(d):
    """The services actually run: the snow day ran the Saturday timetable instead of the weekday one."""
    fd, svc = services_on(d)
    if d == W.SNOW_DAY:
        svc = ["SAT"]
    return fd, svc


def trip_id(fd, svc, route, m, direction=0):
    return "%s_%s_%s_%s%04d" % (route, fd, svc, "O" if direction == 0 else "I", (m // 60) * 100 + m % 60)


def departures(d, which=operated):
    """[(route, scheduled minute at the designated stop, trip_id)] for a service day."""
    fd, svc = which(d)
    out = []
    for s in svc:
        for r in W.SCHED:
            for m in minutes(fd, s, r):
                out.append((r, m, trip_id(fd, s, r, m)))
    return sorted(out, key=lambda x: (x[1], x[0]))


# ---------------------------------------------------------------- the feed files
def gtfs_time(m):
    return "%02d:%02d:00" % (m // 60, m % 60)


def gtfs_hms(sec):
    sec = int(sec)
    return "%02d:%02d:%02d" % (sec // 3600, (sec // 60) % 60, sec % 60)


def frequency_blocks(window):
    """The frequency rows for the window's departures (exact times): runs of ten-minute steps that share their seconds
    past the minute, each ending between its last trip and the next step."""
    blocks, run = [], []
    for m in window:
        if run and (m - run[-1] != 10 or W.pub_sec(W.FREQUENCY_BASED, m) != W.pub_sec(W.FREQUENCY_BASED, run[-1])):
            blocks.append(run)
            run = []
        run.append(m)
    if run:
        blocks.append(run)
    out = []
    for k, b in enumerate(blocks):
        p = W.pub_sec(W.FREQUENCY_BASED, b[0])
        start = b[0] * 60 + p
        end = blocks[k + 1][0] * 60 if k + 1 < len(blocks) else b[-1] * 60 + p + 300
        out.append((gtfs_hms(start), gtfs_hms(end)))
    return out


def stop_table():
    """Every stop in the feeds: (key, stop_code, January id, April id, name)."""
    rows = [(k, v[0], v[1], v[2], v[3]) for k, v in W.STOPS.items()]
    for k, nm in OPPOSITE.items():
        c = int(W.STOPS[k][0]) + 1
        rows.append((k + "o", "%04d" % c, "%d" % (int(W.STOPS[k][1]) + 1), "%d" % (int(W.STOPS[k][2]) + 1), nm))
    seen = {v[3] for v in W.STOPS.values()} | set(OPPOSITE.values())
    code = 1100
    for r in sorted(STREETS, key=lambda x: int(x)):
        for nm in STREETS[r]:
            if nm in seen:
                continue
            seen.add(nm)
            code += 37
            rows.append(("x%d" % code, "%04d" % (code % 9000 + 1000), "%d" % (code * 10 + 3), "%d" % (7000 + code % 1000),
                         nm))
    return rows


def pattern_stops(route):
    """The outbound stop pattern: names and minutes from the first stop; the designated stop at OFFSET."""
    names = list(STREETS[route])
    des = W.STOPS[W.STOP_OF[route]][3]
    off = W.OFFSET[route]
    run = W.RUN_MIN[route]
    if off == 0:
        names = [des] + [n for n in names if n != des]
    else:
        names = [n for n in names if n != des]
        names.insert(2, des)
    n = len(names)
    if off == 0:
        mins = [0] + [int(round(run * (i / (n - 1)))) for i in range(1, n)]
    else:
        mins = [0, int(round(off * 0.55)), off] + [off + int(round((run - off) * (i - 2) / (n - 3))) for i in range(3, n)]
    return list(zip(names, mins))


def write_feed(path, fd):
    f = FEEDS[fd]
    stops = stop_table()
    sid = {nm: (rid_jan if fd == "2601" else rid_apr) for _, _, rid_jan, rid_apr, nm in stops}
    files = {}

    def table(name, header, rows):
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
        files[name] = buf.getvalue()

    table("agency.txt", ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang", "agency_phone"],
          [["LKT", W.DEPARTMENT, "https://ride.larkhaventransit.org", "America/Chicago", "en", "(402) 555-0140"]])
    table("feed_info.txt", ["feed_publisher_name", "feed_publisher_url", "feed_lang", "feed_start_date", "feed_end_date",
                            "feed_version"],
          [[W.DEPARTMENT, "https://ride.larkhaventransit.org", "en", f["start"].strftime("%Y%m%d"),
            f["end"].strftime("%Y%m%d"), "%s-%s" % (fd, f["published"])]])
    table("routes.txt", ["route_id", "agency_id", "route_short_name", "route_long_name", "route_type", "route_color",
                         "route_text_color"],
          [[r, "LKT", r, W.ROUTE_NAMES[r], "3", "1F4E79" if r in W.CANDIDATES else "6B6B6B", "FFFFFF"]
           for r in sorted(W.SCHED, key=int)])
    table("stops.txt", ["stop_id", "stop_code", "stop_name", "location_type"],
          [[(j if fd == "2601" else a), c, nm, "0"] for _, c, j, a, nm in stops])
    cal = []
    for s, days in SERVICES[fd].items():
        cal.append([s] + list(days) + [f["start"].strftime("%Y%m%d"), f["end"].strftime("%Y%m%d")])
    table("calendar.txt", ["service_id", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                           "start_date", "end_date"], cal)
    cd = []
    d = f["start"]
    while d <= f["end"]:
        ds = d.strftime("%Y%m%d")
        wkd = "WKD" if fd == "2601" else ("FRI" if d.weekday() == 4 else "MTH")
        if d in W.STATE_HOLIDAYS and d.weekday() < 5:
            cd += [[wkd, ds, "2"], ["SUN", ds, "1"]]
        if d == W.GOOD_FRIDAY:
            cd += [["WKD", ds, "2"], ["SAT", ds, "1"]]
        if W.class_day(d):
            cd.append(["UNIV", ds, "1"])
        d += dt.timedelta(days=1)
    table("calendar_dates.txt", ["service_id", "date", "exception_type"], cd)
    trips, times, freqs = [], [], []
    for r in sorted(W.SCHED, key=int):
        pat = pattern_stops(r)
        off = W.OFFSET[r]
        for s in SERVICES[fd]:
            ms = minutes(fd, s, r)
            if not ms:
                continue
            if frequency_window(r, s):
                window = [m for m in ms if 360 <= m < 1140]
                rest = [m for m in ms if not 360 <= m < 1140]
                if window:
                    t = "%s_%s_%s_F0600" % (r, fd, s)
                    trips.append([r, s, t, W.ROUTE_NAMES[r] + " to " + pat[-1][0], "0"])
                    for i, (nm, mm) in enumerate(pat):
                        tt = gtfs_time(360 + mm)
                        times.append([t, tt, tt, sid[nm], str(i + 1), "1" if i in (0, len(pat) - 1) else "0"])
                    for a_, b_ in frequency_blocks(window):
                        freqs.append([t, a_, b_, "600", "1"])
                ms = rest
            for m in ms:
                t = trip_id(fd, s, r, m)
                trips.append([r, s, t, W.ROUTE_NAMES[r] + " to " + pat[-1][0], "0"])
                start = m - off
                ps = W.pub_sec(r, m)
                for i, (nm, mm) in enumerate(pat):
                    dep = (start + mm) * 60 + (ps if mm >= off else 0)
                    arr = dep
                    if mm == off and off > 0:
                        arr = dep - W.DWELL.get(r, 0) * 60
                    times.append([t, gtfs_hms(arr), gtfs_hms(dep), sid[nm], str(i + 1),
                                  "1" if (i in (0, len(pat) - 1) or mm == off) else "0"])
                # the inbound trip that brings the bus back
                ti = trip_id(fd, s, r, m, 1)
                trips.append([r, s, ti, W.ROUTE_NAMES[r] + " to " + pat[0][0], "1"])
                back = start + W.RUN_MIN[r] + W.LAYOVER.get(r, 7)
                inv = [(OPPOSITE[W.STOP_OF[r]] if nm == W.STOPS[W.STOP_OF[r]][3] else nm, W.RUN_MIN[r] - mm)
                       for nm, mm in reversed(pat)]
                for i, (nm, mm) in enumerate(inv):
                    dep = back + mm
                    times.append([ti, gtfs_time(dep), gtfs_time(dep), sid[nm], str(i + 1),
                                  "1" if i in (0, len(inv) - 1) else "0"])
    table("trips.txt", ["route_id", "service_id", "trip_id", "trip_headsign", "direction_id"], trips)
    table("stop_times.txt", ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "timepoint"], times)
    table("frequencies.txt", ["trip_id", "start_time", "end_time", "headway_secs", "exact_times"], freqs)
    stamp = (int(f["published"][:4]), int(f["published"][4:6]), int(f["published"][6:]), 16, 42, 10)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in ("agency.txt", "feed_info.txt", "routes.txt", "stops.txt", "calendar.txt", "calendar_dates.txt",
                     "trips.txt", "stop_times.txt", "frequencies.txt"):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, files[name])
    return {k: v.count("\n") - 1 for k, v in files.items()}
