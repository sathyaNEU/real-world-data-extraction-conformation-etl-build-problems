"""task211 pack builder: writes target/, generator/figures.json, metadata.json and target.zip, deterministically.
Run from anywhere: python3 task211/generator/build.py"""
import csv, json, os, zipfile, datetime as dt
import numpy as np
import world as W
import docs

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
CET = dt.timedelta(hours=1)
S = W.SITES
NH = W.H + W.PAD


def rng(k):
    return np.random.default_rng([W.SEED, k])


HC, FRONTS = W.hindcast(np.random.default_rng(W.SEED))
PT = W.past_traces(HC)
NAME = W.SITE_NAME
PORTNAME = {p: W.PORTS[p]["name"] for p in W.PORTS}
DEV = {"SKG": "Vestkyst Vind A/S", "LVB": "Vestkyst Vind A/S", "OSR": "Osterhav Energi A/S",
       "MOF": "Osterhav Energi A/S", "FJH": "Fjernhav Offshore ApS"}
DEVS = ["Vestkyst Vind A/S", "Osterhav Energi A/S", "Fjernhav Offshore ApS"]
GT = {"NM Havorn": 41860, "NM Terne": 41860, "NM Lomvie": 38415, "NM Mallemuk": 38415, "NM Ederfugl": 44120}


def t0(y):
    return dt.datetime(y, 11, 1, 0, 0)


def write_csv(name, header, rows):
    with open(os.path.join(TARGET, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)


# ---------------------------------------------------------------- the buoy record (two export layouts)
def buoy_files():
    r = rng(1)
    tp = {}; gaps = {}
    for s in S:
        tp[s] = np.zeros((len(W.WINTERS), NH)); gaps[s] = np.zeros((len(W.WINTERS), NH), dtype=bool)
        for w in range(len(W.WINTERS)):
            z = r.normal(0, 0.35, NH); e = np.zeros(NH)
            for h in range(1, NH):
                e[h] = 0.85 * e[h - 1] + z[h]
            tp[s][w] = np.round(np.clip(2.9 + 3.05 * np.sqrt(HC[s][w]) + 0.6 * e, 3.1, 17.5), 1)
            for _ in range(int(r.integers(0, 3))):
                a = int(r.integers(0, NH - 100)); L = int(r.integers(5, 70))
                gaps[s][w, a: a + L] = True
    old, new = [], []
    for w, y in enumerate(W.WINTERS):
        for s in S:
            sid, oname = W.STATIONS[s][0], W.STATIONS[s][1]
            base = t0(y) - CET
            for h in range(NH):
                t = base + dt.timedelta(hours=h)
                if y <= 2016:
                    old.append((oname, t.strftime("%Y%m%d%H"), int(round(HC[s][w][h] * 100)),
                                int(round(tp[s][w][h] * 10)), "model" if gaps[s][w][h] else "buoy"))
                if y >= 2016:
                    new.append((sid, t.strftime("%Y-%m-%dT%H:%MZ"), "%.2f" % HC[s][w][h], "%.1f" % tp[s][w][h],
                                4 if gaps[s][w][h] else 1))
    write_csv("buoy_hm0_2008_2017.csv", ["buoy_name", "date_hour_utc", "hm0_cm", "tp_ds", "source"], old)
    write_csv("buoy_hs_2016_2026.csv", ["station", "time_utc", "hs_m", "tp_s", "qc"], new)
    write_csv("buoy_stations.csv", ["station", "former_export_name", "site", "lat", "lon", "water_depth_m"],
              [(W.STATIONS[s][0], W.STATIONS[s][1], NAME[s], "%.3f" % W.STATIONS[s][2], "%.3f" % W.STATIONS[s][3],
                W.STATIONS[s][4]) for s in S])
    return len(old), len(new)


# ---------------------------------------------------------------- registers
def registers():
    fleet = [["vessel", "imo", "type", "built", "loa_m", "beam_m", "max_draught_m", "gross_tonnage", "main_crane_swl_t",
              "service_speed_kn", "hs_working_limit_m", "hs_station_keeping_limit_m", "campaign_2026_27_site",
              "shelter_port"]]
    specs = {"NM Havorn": (9784521, 2015, 183.0, 47.0, 8.6, 3000), "NM Terne": (9784533, 2016, 183.0, 47.0, 8.6, 3000),
             "NM Lomvie": (9711205, 2013, 176.5, 44.0, 8.2, 2500), "NM Mallemuk": (9711217, 2014, 176.5, 44.0, 8.2, 2500),
             "NM Ederfugl": (9893140, 2026, 189.0, 49.0, 8.9, 3200)}
    for s in S:
        v = W.FLEET_2026[s]; i, b, loa, beam, dr, crane = specs[v]
        fleet.append([v, i, "Floating heavy-lift vessel (DP2)", b, loa, beam, dr, GT[v], crane, 10.0, W.LW, W.LS,
                      NAME[s], PORTNAME[W.SHELTER[s]]])
    fleet.append(["NM Atlas", 9690117, "Jack-up installation vessel", 2012, 147.0, 50.0, 6.1, 21540, 1600, 9.0, "", "",
                  "", ""])
    ports = [["port", "locode", "heavy_lift_berths", "heavy_lift_quay_m", "depth_alongside_m", "max_loa_m",
              "storm_mooring_buoys", "pilotage", "dues_eur_per_gt_per_24h"]]
    pdat = {"BRA": ("DK BMH", 1, 215, 11.0, 200, 0, "compulsory over 90 m", 0.039),
            "KAL": ("DK KVH", 0, "", "", "", 4, "on request", ""),
            "SAN": ("DK SDV", 1, 205, 10.0, 195, 0, "compulsory over 90 m", 0.044),
            "TRV": ("DK TVG", 2, 460, 12.5, 230, 0, "compulsory over 90 m", 0.042),
            "HJB": ("DK HJB", 1, 225, 11.5, 210, 2, "compulsory over 90 m", 0.051)}
    for p in ["BRA", "HJB", "KAL", "SAN", "TRV"]:
        ports.append([PORTNAME[p]] + list(pdat[p]))
    pas = [["from", "to", "distance_nm", "passage_hours"]]
    for s in S:
        for p in ["BRA", "HJB", "KAL", "SAN", "TRV"]:
            pas.append([NAME[s], PORTNAME[p], W.PASSAGE[s][p] * 10, W.PASSAGE[s][p]])
    for a in ["BRA", "HJB", "KAL", "SAN", "TRV"]:
        for p in ["BRA", "HJB", "KAL", "SAN", "TRV"]:
            if a != p:
                pas.append([PORTNAME[a], PORTNAME[p], W.PORT_PASSAGE[a][p] * 10, W.PORT_PASSAGE[a][p]])
    docs.xlsx(os.path.join(TARGET, "vessel_register_2026.xlsx"), [("Fleet", fleet, None)],
              stamp=dt.datetime(2026, 9, 19, 11, 4), created=dt.datetime(2026, 1, 12, 8, 31))
    docs.xlsx(os.path.join(TARGET, "port_register_2026.xlsx"), [("Ports", ports, None), ("Passage plan", pas, None)],
              stamp=dt.datetime(2026, 9, 3, 9, 22), created=dt.datetime(2025, 10, 2, 13, 47))


# ---------------------------------------------------------------- the governing document
def campaign_plan():
    fnd = {"SKG": 14, "LVB": 12, "OSR": 16, "MOF": 10, "FJH": 13}
    rows = [["Site", "Developer", "Monopile foundations", "Floating vessel (vessel register)"]]
    for s in S:
        rows.append([NAME[s], DEV[s], fnd[s], W.FLEET_2026[s]])
    blocks = [
        ("title", "Winter campaign 2026/27: foundation installation plan"),
        ("small", "Nordvig Marine A/S, Marine Operations. Document NM-MO-CP-2627, revision 3, issued 18 September 2026. "
                  "Owner: A. Jespersen, Marine Operations Manager. Approval: campaign planning panel."),
        ("h", "1. Scope"),
        ("p", "The campaign installs the remaining monopile foundations at five sites between 1 November 2026 00:00 and "
              "28 February 2027 24:00, Danish time."),
        ("t", rows, [34, 48, 34, 58]),
        ("h", "2. Vessels"),
        ("p", "The campaign has the jack-up NM Atlas and the five floating heavy-lift vessels in the vessel register. "
              "NM Atlas stands at one site for the whole campaign and installs that site's foundations. The floating "
              "vessel the register assigns to that site is then released for charter for the season and takes no part "
              "in the campaign. NM Atlas stays elevated at its site through the winter; its survival condition is well "
              "beyond any sea state in the buoy record and it does not leave its site for weather."),
        ("h", "3. Weather procedure for the floating heavy-lift vessels (WP-FHL revision 4)"),
        ("p", "3.1 A vessel works at its site in every hour in which the significant wave height (Hs) at the site is at "
              "or below the vessel's working limit in the vessel register."),
        ("p", "3.2 A vessel leaves its site for its shelter port at the latest hour that brings it alongside by the "
              "start of the first hour in which Hs at the site is above the vessel's station-keeping limit. Passages "
              "take the hours in the port register's passage plan."),
        ("p", "3.3 A vessel in shelter sails for its site at the first hour from which it can make the passage and then "
              "complete a 10-hour critical lift at the site, with Hs at the site at or below the station-keeping limit "
              "in every hour from its departure to its arrival on site and at or below the working limit in every hour "
              "of the lift. It works from the hour it arrives on site."),
        ("p", "3.4 Every vessel is on station at its site at 00:00 on 1 November."),
        ("h", "4. Placement basis"),
        ("p", "4.1 The planning panel places NM Atlas at the site where it avoids the most floating-vessel weather "
              "downtime."),
        ("p", "4.2 A floating vessel's weather downtime is every hour of the campaign from the hour it leaves its site "
              "for shelter up to the hour it is back on site, and every hour at its site in which Hs is above its "
              "working limit."),
        ("p", "4.3 The downtime a placement avoids is the floating fleet's weather downtime over the campaign with every "
              "site worked by its floating vessel, less the fleet's weather downtime with NM Atlas at that site, as the "
              "procedure in section 3 gives it against each of the 18 winters of the buoy record (1 November 2008 to "
              "28 February 2026), averaged over those winters and stated in days of 24 hours. Each winter's record "
              "stands in for the forecast, hour by hour."),
        ("h", "5. Timetable"),
        ("p", "NM Atlas's mobilisation order under its charter must be placed by 9 October 2026 for it to stand at its "
              "site on 1 November. Load-out of the first foundations starts at Tranevig and Bramso Havn on 19 October."),
    ]
    docs.pdf(os.path.join(TARGET, "campaign_plan_2026_27.pdf"), "Winter campaign 2026/27 installation plan",
             "Nordvig Marine A/S", blocks, date="D:20260918101500+02'00'")


# ---------------------------------------------------------------- the past campaigns' daily progress reports
def segments(seq):
    """Consecutive hours with one (state, place): [first, end, state, place]."""
    out = []
    for h, rec in enumerate(seq):
        if rec is None:
            continue
        if out and out[-1][1] == h and (out[-1][2], out[-1][3]) == rec:
            out[-1][1] = h + 1
        else:
            out.append([h, h + 1, rec[0], rec[1]])
    # a passage to a port that runs straight on to the storm moorings is reported as one passage to the moorings
    for i in range(len(out) - 1):
        a, b = out[i], out[i + 1]
        if a[2] == "TRN" and b[2] == "TRN" and a[3] in W.PORTS and b[3] == W.STORM_MOORINGS:
            a[3] = W.STORM_MOORINGS
    merged = []
    for seg in out:
        if merged and merged[-1][1] == seg[0] and merged[-1][2:] == seg[2:]:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg)
    return merged


def dpr():
    r = rng(2)
    rows = []
    steps = [("Positioning and monopile upending {m}", 4, 7), ("Pile driving {m}", 5, 10),
             ("Transition piece installation {t}", 4, 8), ("Bolt tensioning and grouting {t}", 3, 7),
             ("Feeder barge alongside, monopile transfer", 3, 6)]
    wow = ["Waiting on weather", "WOW on location", "Standby on location, Hs above working limit",
           "Waiting on weather, pile in gripper secured"]
    for y, (tr, ev, d) in PT.items():
        fl = W.PAST[y]["floating"]
        for s in S:
            if s not in fl:
                continue
            vessel = fl[s][0]
            k = {"SKG": 3, "LVB": 2, "OSR": 5, "MOF": 2, "FJH": 4}[s] + (y - 2023) * 4
            plan = []
            for h0, h1, state, place in segments(tr[s][:W.H]):
                if state == "INST":
                    pieces = []
                    h = h0
                    while h < h1:
                        if not plan:
                            k += 1
                            m = "MP-%s%02d" % (s[0], k); t = "TP-%s%02d" % (s[0], k)
                            plan = [[txt.format(m=m, t=t), int(r.integers(a, b + 1))] for txt, a, b in steps]
                            if r.random() < 0.55:
                                plan.pop()
                        take = min(plan[0][1], h1 - h)
                        pieces.append((h, h + take, plan[0][0], NAME[s]))
                        plan[0][1] -= take
                        if plan[0][1] == 0:
                            plan.pop(0)
                        h += take
                elif state == "WOW":
                    pieces = [(h0, h1, wow[int(r.integers(0, len(wow)))], NAME[s])]
                elif state == "TRN":
                    pieces = [(h0, h1, "Transit to %s" % (NAME[s] if place == s else PORTNAME[place]), "At sea")]
                else:
                    txt = ("On storm moorings, Kalvholm buoy K%d" % int(r.integers(1, 5)) if place == W.STORM_MOORINGS
                           else "Alongside %s, heavy-lift quay" % PORTNAME[place])
                    pieces = [(h0, h1, txt, PORTNAME[place])]
                for a, b, txt, loc in pieces:
                    while a < b:    # one report a day: split at local midnight
                        day_end = (a // 24 + 1) * 24
                        e = min(b, day_end)
                        ta = t0(y) + dt.timedelta(hours=a)
                        tb = "24:00" if e == day_end else (t0(y) + dt.timedelta(hours=e)).strftime("%H:%M")
                        last = txt.split()[-1]
                        rows.append((ta.strftime("%Y-%m-%d"), vessel, NAME[s], ta.strftime("%H:%M"), tb, txt, loc,
                                     last if last[:3] in ("MP-", "TP-") else ""))
                        a = e
    rows.sort(key=lambda x: (x[0], x[1], x[3]))
    write_csv("daily_progress_reports_2023_2026.csv",
              ["report_date", "vessel", "site", "time_from", "time_to", "activity", "location", "foundation_ref"], rows)
    return rows


# ---------------------------------------------------------------- the metocean monitor (declared wrong-basis distractor)
def monitor():
    rows = [["winter", "site", "station", "mean_hs_m", "p90_hs_m", "max_hs_m", "hours_hs_over_1_8_m",
             "hours_hs_over_3_2_m", "storms_hs_over_4_m"]]
    for w, y in enumerate(W.WINTERS):
        for s in S:
            x = HC[s][w][:W.H]
            n = 0; last = -10 ** 9
            for h in np.flatnonzero(x > 4.0):
                if h - last > 24:
                    n += 1
                last = h
            rows.append(["%d/%02d" % (y, (y + 1) % 100), NAME[s], W.STATIONS[s][0], round(float(x.mean()), 2),
                         round(float(np.quantile(x, 0.9)), 2), round(float(x.max()), 2), int((x > 1.8).sum()),
                         int((x > 3.2).sum()), n])
    info = [["item", "value"],
            ["content", "Sea-state statistics of each site's buoy record, 1 November to 28 February, Danish time"],
            ["not", "a downtime estimate"], ["owner", "S. Schou, metocean"], ["refreshed", "2026-09-22"],
            ["version", "3.2"]]
    docs.xlsx(os.path.join(TARGET, "metocean_monitor_2026.xlsx"), [("Buoy statistics", rows, None), ("Version", info, None)],
              author="Simone Schou", stamp=dt.datetime(2026, 9, 22, 15, 41), created=dt.datetime(2024, 10, 7, 10, 15))


def crew_rotation():
    r = rng(3)
    rows = []
    for v in list(W.FLEET_2026.values()) + ["NM Atlas"]:
        d0 = dt.date(2026, 10, 20) + dt.timedelta(days=int(r.integers(0, 14)))
        while d0 < dt.date(2027, 3, 1):
            rows.append((v, d0.isoformat(), "Tranevig" if v == "NM Atlas" else "Sandvig",
                         "helicopter" if v == "NM Atlas" else "crew transfer vessel", int(r.integers(22, 31)),
                         "T%d" % (1 + (d0.toordinal() // 14) % 2)))
            d0 += dt.timedelta(days=int(r.choice([14, 14, 14, 13, 15])))
    rows.sort()
    write_csv("crew_rotation_2026_27.csv", ["vessel", "crew_change_date", "change_port", "transfer", "persons", "team"],
              rows)


# ---------------------------------------------------------------- ask 1: the developers' standby statements
MONTHS = [(0, 720), (720, 1464), (1464, 2208), (2208, 2880)]   # Nov, Dec, Jan, Feb in campaign hours


def q4(x):
    return round(x * 4) / 4


def statements():
    r = rng(4)
    po = {"Vestkyst Vind A/S": "PO 4500231187", "Osterhav Energi A/S": "PO 4500228840",
          "Fjernhav Offshore ApS": "PO 4500240316"}
    lines = {}   # (dev, y, mi) -> list of [vessel, site, category, days]
    for y, (tr, ev, d) in PT.items():
        for s, (v, a0, a1) in W.PAST[y]["floating"].items():
            for mi, (m0, m1) in enumerate(MONTHS):
                seq = [x for x in tr[s][m0:m1] if x is not None]
                if not seq:
                    continue
                wow = sum(1 for x in seq if x[0] == "WOW"); sh = sum(1 for x in seq if x[0] in ("TRN", "SHEL"))
                L = lines.setdefault((DEV[s], y, mi), [])
                L.append([v, NAME[s], "Weather standby on site", q4(wow / 24)])
                L.append([v, NAME[s], "Shelter and transit", q4(sh / 24)])
    # truth per line: (dev, standby winter) -> days
    truth = {}
    catch = [("Vestkyst Vind A/S", 2023, "SKG"), ("Vestkyst Vind A/S", 2024, "LVB"), ("Osterhav Energi A/S", 2024, "MOF"),
             ("Fjernhav Offshore ApS", 2024, "FJH")]
    extra = {}   # (dev, y+1, 0) -> catch-up lines
    for dev, y, s in catch:
        L = lines[(dev, y, 3)]
        ln = [x for x in L if x[1] == NAME[s] and x[2] == "Shelter and transit"][0]
        disp = q4(ln[3] * float(r.uniform(0.35, 0.6)))
        ln[3] = ln[3] - disp
        extra.setdefault((dev, y + 1, 0), []).append([ln[0], ln[1], "Shelter and transit", disp, y])
    rows = []
    seq = {dev: int(r.integers(118, 140)) for dev in DEVS}
    fmt = {"Vestkyst Vind A/S": "VKV/STB/{:04d}", "Osterhav Energi A/S": "OE-{y}-{:03d}", "Fjernhav Offshore ApS": "FO{:05d}"}
    issued = []
    for (dev, y, mi), L in sorted(lines.items()):
        mstart = (t0(y) + dt.timedelta(hours=MONTHS[mi][0])).date()
        mend = (t0(y) + dt.timedelta(hours=MONTHS[mi][1] - 1)).date()
        iss = mend + dt.timedelta(days=int(r.integers(9, 25)))
        allL = [x + [y] for x in L] + extra.get((dev, y, mi), [])
        issued.append((iss, dev, mstart.strftime("%Y-%m"), allL, y))
    issued.sort(key=lambda x: (x[0], x[1]))
    revs = []
    cells_done = set()
    for iss, dev, period, allL, y in issued:
        seq[dev] += int(r.integers(1, 4))
        no = fmt[dev].format(seq[dev], y=iss.year)
        for v, site, cat, days, wy in allL:
            rows.append([no, dev, period, iss.isoformat(), v, site, cat, "%.2f" % days, po[dev]])
            truth[(dev, wy)] = truth.get((dev, wy), 0.0) + days
        # one revised statement in each developer-winter cell, restating one line of a statement with two or more
        if (dev, y) not in cells_done and period[5:] in ("11", "12", "01") and r.random() < 0.6 and len(allL) >= 2:
            own = [x for x in allL if x[4] == y and x[3] >= 1.0]
            if own:
                cells_done.add((dev, y))
                tgt = own[int(r.integers(0, len(own)))]
                delta = float(r.choice([-1.5, -1.25, -1.0, -0.75, 0.5, 0.75, 1.0, 1.25]))
                revs.append((iss + dt.timedelta(days=int(r.integers(20, 46))), dev, period, no, tgt, max(0.0, tgt[3] + delta)))
    # cells the random pass missed get their revision on their first eligible statement
    for iss, dev, period, allL, y in issued:
        if (dev, y) not in cells_done and len(allL) >= 2:
            own = [x for x in allL if x[4] == y and x[3] >= 1.0]
            no = [rw[0] for rw in rows if rw[1] == dev and rw[2] == period][0]
            if own:
                cells_done.add((dev, y))
                tgt = own[0]
                revs.append((iss + dt.timedelta(days=31), dev, period, no, tgt, max(0.0, tgt[3] + 0.75)))
    for iss, dev, period, orig, tgt, newdays in sorted(revs, key=lambda x: (x[0], x[1])):
        seq[dev] += 1
        no = fmt[dev].format(seq[dev], y=iss.year)
        rows.append([no, dev, period, iss.isoformat(), tgt[0], tgt[1], tgt[2], "%.2f" % newdays, "Rev. " + orig])
        truth[(dev, tgt[4])] += newdays - tgt[3]
    rows.sort(key=lambda x: (x[1], x[3], x[0], x[4], x[6]))
    write_csv("developer_standby_statements.csv",
              ["statement_no", "developer", "period", "issued_on", "vessel", "site", "category", "days", "their_ref"], rows)
    return {"%s|%d/%02d" % (dev, y, (y + 1) % 100): round(v, 2) for (dev, y), v in sorted(truth.items())}


# ---------------------------------------------------------------- ask 2: the jack-up's shift reports
ATLAS = {2023: ("MOF", 7, W.H - 5), 2024: ("OSR", 7, W.H - 5), 2025: ("MOF", 7, 106 * 24 + 19)}
GO_LIVE = dt.datetime(2026, 1, 15, 7, 0)
BACK = dt.datetime(2026, 1, 25, 7, 0)
CODES = [("PD", "Pile driving", "Production"), ("TP", "Transition piece installation", "Production"),
         ("JK", "Jacking, preload and move", "Production"), ("CR", "Crane operations, other", "Production"),
         ("WX", "Weather standby", "Weather"), ("WS", "Waiting on supply barge", "Logistics"),
         ("MT", "Maintenance and repair", "Technical"), ("OT", "Other", "Other")]


def atlas():
    r = rng(5)
    shifts = []; truth = {}; hire = 0
    sid = 3104417
    for y, (s, a0, a1) in ATLAS.items():
        w = W.WINTERS.index(y)
        hs = HC[s][w]
        e1 = np.zeros(W.H); e2 = np.zeros(W.H)
        for h in range(1, W.H):
            e1[h] = 0.9 * e1[h - 1] + r.normal(0, 0.43); e2[h] = 0.6 * e2[h - 1] + r.normal(0, 0.8)
        u = 2.6 + 4.9 * hs[:W.H] ** 0.8 * (1 + 0.12 * e1) + 1.3 * e2
        wx = np.zeros(W.H, dtype=bool); on = False; calm = 0
        for h in range(W.H):
            if not on and u[h] > 15.0:
                on = True; calm = 0
            elif on:
                calm = calm + 1 if u[h] < 13.5 else 0
                if calm >= 3:
                    on = False
            wx[h] = on
        tot = 0
        for h in range(a0, a1, 12):
            start = t0(y) + dt.timedelta(hours=h)
            hrs = range(h, h + 12)
            wtot = int(sum(wx[k] for k in hrs)); tot += wtot
            if start >= GO_LIVE and start < dt.datetime(2026, 2, 15, 20, 0):
                hire += wtot
            if GO_LIVE <= start < BACK:
                continue
            new = start >= BACK
            parts = {}
            if wtot:
                if new:
                    parts["WX"] = float(wtot)
                else:
                    ww = int(sum(1 for k in hrs if wx[k] and hs[k] > 2.3))
                    if ww:
                        parts["WW"] = float(ww)
                    if wtot - ww:
                        parts["WS"] = float(wtot - ww)
            left = 12.0 - wtot
            if left > 0 and r.random() < 0.14:
                x = min(left, float(r.integers(2, 13)) / 2)
                parts["WS" if new else "SB"] = x; left -= x
            if left > 0 and r.random() < 0.05:
                x = min(left, float(r.integers(4, 17)) / 2)
                parts["MT"] = x; left -= x
            if left > 0:
                wts = r.dirichlet([3, 2, 0.6, 0.8])
                cut = [round(left * x * 2) / 2 for x in wts[:3]]
                for c, x in zip(["PD", "TP", "JK"], cut):
                    if x > 0:
                        parts[c] = x
                rest = round(left - sum(cut), 1)
                if rest > 0:
                    parts["CR"] = rest
                elif rest < 0:
                    parts["PD"] = round(parts.get("PD", 0) + rest, 1)
            ident = ("ATL-%s-%s" % (start.strftime("%y%m%d"), "D" if start.hour == 7 else "N")) if not new else str(sid)
            if new:
                sid += int(r.integers(1, 4))
            shifts.append({"id": ident, "date": start.strftime("%Y-%m-%d"), "shift": "D" if start.hour == 7 else "N",
                           "site": NAME[s], "hours": {k: parts[k] for k in sorted(parts)}})
        truth["%d/%02d" % (y, (y + 1) % 100)] = tot
    with open(os.path.join(TARGET, "atlas_shift_reports.json"), "w", encoding="utf-8") as f:
        json.dump({"vessel": "NM Atlas", "system": "OpsLog 5", "exported": "2026-09-24T09:41:07+02:00",
                   "shifts": shifts}, f, indent=1)
        f.write("\n")
    write_csv("atlas_activity_codes.csv", ["code", "description", "group"], CODES)
    day_full, day_red = 172500, 121000
    full_h = (dt.datetime(2026, 2, 15, 19, 0) - GO_LIVE).total_seconds() / 3600 - hire
    blocks = [("title", "Final hire statement"),
              ("small", "Northsea Liftboat Owners AS, Bergen. To: Nordvig Marine A/S, Esbjerg. Charter party NL-ATL-24/26, "
                        "vessel NM Atlas. Statement no. 26-0117, dated 27 February 2026."),
              ("h", "Hire period"),
              ("p", "From 15 January 2026 07:00 to redelivery at 15 February 2026 19:00, Danish time."),
              ("t", [["Item", "Hours", "Rate per day (EUR)", "Amount (EUR)"],
                     ["Hire at full rate", "%d" % full_h, "{:,}".format(day_full), "{:,.2f}".format(full_h * day_full / 24)],
                     ["Hire at reduced rate, weather standby", "%d" % hire, "{:,}".format(day_red),
                      "{:,.2f}".format(hire * day_red / 24)],
                     ["Total", "%d" % (full_h + hire), "", "{:,.2f}".format(full_h * day_full / 24 + hire * day_red / 24)]],
               [70, 22, 36, 40]),
              ("p", "Weather standby hours as agreed with the vessel's master at redelivery. Payment within 30 days to the "
                    "account on file.")]
    docs.pdf(os.path.join(TARGET, "atlas_final_hire_statement.pdf"), "Final hire statement NM Atlas",
             "Northsea Liftboat Owners AS", blocks, date="D:20260227113000+01'00'")
    return truth


# ---------------------------------------------------------------- ask 3: port charges in the payables extract
RATE = {"TRV": 0.042, "HJB": 0.051}


def port_charges():
    r = rng(6)
    calls = []
    for y, (tr, ev, d) in PT.items():
        for s, (v, a0, a1) in W.PAST[y]["floating"].items():
            for h0, h1, state, place in segments(tr[s][:W.H]):
                if state == "SHEL" and place in RATE:
                    hrs = h1 - h0
                    calls.append((place, y, v, t0(y) + dt.timedelta(hours=h0), t0(y) + dt.timedelta(hours=h1), hrs,
                                  round(GT[v] * RATE[place] * -(-hrs // 24), 2)))
    truth = {}
    for p, y, v, a, b, hrs, amt in calls:
        k = "%s|%d/%02d" % (PORTNAME[p], y, (y + 1) % 100)
        truth[k] = round(truth.get(k, 0.0) + amt, 2)
    rows = []
    # Tranevig: a weekly statement, one line per call in each week it touches, the line carrying the call's charge
    weekly = {}
    for p, y, v, a, b, hrs, amt in [c for c in calls if c[0] == "TRV"]:
        t = a
        while t < b:
            wk0 = (t - dt.timedelta(days=t.weekday())).replace(hour=0, minute=0)
            wk1 = wk0 + dt.timedelta(days=7)
            e = min(b, wk1)
            weekly.setdefault(wk0, []).append((v, t, int((e - t).total_seconds() // 3600), amt))
            t = e
    for wk0 in sorted(weekly):
        iso = wk0.isocalendar()
        no = "TVG-%02d%02d" % (iso[0] % 100, iso[1])
        inv = (wk0 + dt.timedelta(days=7)).date()
        tot = round(sum(x[3] for x in weekly[wk0]), 2)
        post = inv + dt.timedelta(days=int(r.integers(2, 6)))
        for v, t, bh, amt in weekly[wk0]:
            rows.append(["40112", "Tranevig Havn", no, inv.isoformat(), post.isoformat(), v, t.strftime("%Y-%m-%d %H:%M"), bh,
                         "%.2f" % amt, "%.2f" % tot])
    # Hjortby Havn: one invoice per call; the sequence restarts each year; invoices open at the ERP change were re-posted
    used = {}
    hj = sorted([c for c in calls if c[0] == "HJB"], key=lambda c: c[3])
    first25 = []
    for p, y, v, a, b, hrs, amt in hj:
        inv = (b + dt.timedelta(days=1)).date()
        yr = inv.year
        if yr == 2026 and first25 and r.random() < 0.6:
            n = first25.pop(0)
        else:
            n = used.get(yr, int(r.integers(3, 9) if inv.month <= 2 else r.integers(380, 420))) + int(r.integers(4, 31))
        used[yr] = max(used.get(yr, 0), n)
        if yr == 2025 and inv.month <= 2:
            first25.append(n)
        post = inv + dt.timedelta(days=int(r.integers(1, 5)))
        rec = ["40177", "Hjortby Havn", "%04d" % n, inv.isoformat(), post.isoformat(), v, a.strftime("%Y-%m-%d %H:%M"), hrs,
               "%.2f" % amt, "%.2f" % amt]
        rows.append(rec)
        if dt.date(2025, 2, 1) <= inv <= dt.date(2025, 6, 30):
            # open at the ERP change on 1 July 2025: re-keyed in the new system, number unpadded, whole euros
            rows.append(["40177", "Hjortby Havn", str(n), inv.isoformat(),
                         dt.date(2025, 7, 1 + int(r.integers(0, 3))).isoformat(), v, a.strftime("%Y-%m-%d %H:%M"), hrs,
                         "%.2f" % round(amt),
                         "%.2f" % round(amt)])
    rows.sort(key=lambda x: (x[4], x[0], x[2], x[5]))
    write_csv("ap_port_charges_2023_2026.csv",
              ["vendor_no", "vendor", "invoice_no", "invoice_date", "posting_date", "vessel", "berth_from", "berth_hours",
               "amount_eur", "invoice_total_eur"], rows)
    return truth, calls


# ---------------------------------------------------------------- the golden figures, provenance and the zip
def main_figures():
    av, own = W.avoided_by_placement(HC)
    order = sorted(S, key=lambda s: -av[s])
    return {"avoided_days": {NAME[s]: round(av[s], 4) for s in S},
            "own_downtime_days_all_floating": {NAME[s]: round(own[s], 4) for s in S},
            "call": NAME[order[0]], "runner_up": NAME[order[1]], "gap_days": round(av[order[0]] - av[order[1]], 4)}


FILES = {
    "buoy_hm0_2008_2017.csv": ("Hourly significant wave height and peak period at the five site buoys, winters 2008/09 to "
                               "2016/17, old metocean database export (heights in cm, periods in tenths of a second)", "spine"),
    "buoy_hs_2016_2026.csv": ("Hourly significant wave height and peak period, winters 2016/17 to 2025/26, current "
                              "platform export", "spine"),
    "buoy_stations.csv": ("Buoy station lookup", "lookup"),
    "vessel_register_2026.xlsx": ("Fleet register with the 2026/27 assignments", "register"),
    "port_register_2026.xlsx": ("Ports, berths, moorings, dues and the passage plan", "register"),
    "campaign_plan_2026_27.pdf": ("The campaign plan: scope, weather procedure, placement basis", "governing document"),
    "daily_progress_reports_2023_2026.csv": ("Floating vessels' daily progress reports, past three winters", "operating extract"),
    "metocean_monitor_2026.xlsx": ("Metocean planner's sea-state statistics by site and winter", "distractor"),
    "crew_rotation_2026_27.csv": ("Crew change plan for the coming campaign", "distractor"),
    "developer_standby_statements.csv": ("Developers' standby statements as received, past three winters", "ask organ"),
    "atlas_shift_reports.json": ("Jack-up shift reports from its reporting system", "ask organ"),
    "atlas_activity_codes.csv": ("The jack-up reporting system's activity code list", "lookup"),
    "atlas_final_hire_statement.pdf": ("The jack-up owner's final hire statement for the 2025/26 charter", "ask organ"),
    "ap_port_charges_2023_2026.csv": ("Accounts payable extract of port charges at Tranevig and Hjortby Havn", "ask organ"),
}


def metadata(nrows):
    meta = {"task": "task211", "seed": W.SEED, "as_of": "2026-09-25",
            "licence": "CC BY 4.0", "source": "Synthetic, generated by task211/generator from a seeded world; every "
                                              "level set from the references below",
            "references": ["DNV-ST-N001 Marine operations and marine warranty (weather-restricted operations, alpha factors "
                           "and planned operation periods)",
                           "Published operating limits of floating heavy-lift installation vessels (working Hs 1.5 to 2.0 m)",
                           "Central and southern North Sea winter wave climatology (mean Hs 1.4 to 2.4 m, 90th percentile "
                           "2.8 to 4.5 m)"],
            "files": [{"name": k, "content": v[0], "role": v[1], "date": "2026-09-25", "licence": "CC BY 4.0",
                       "source": "synthetic, task211 generator"} for k, v in sorted(FILES.items())],
            "row_counts": nrows,
            "distractors": [
                {"file": "metocean_monitor_2026.xlsx", "kind": "declared wrong-basis distractor",
                 "basis": "sea-state statistics at each buoy (exposure), which order the sites with Osterrev first",
                 "ruled_out_by": "campaign_plan_2026_27.pdf section 4.3 files the placement on the floating fleet's weather "
                                 "downtime under the weather procedure, and the monitor's Version sheet states it is not a "
                                 "downtime estimate"},
                {"file": "crew_rotation_2026_27.csv", "kind": "distractor",
                 "basis": "crew changes run by crew transfer vessel from Sandvig and do not touch the shelter cycle"}],
            "generator": "task211/generator/build.py"}
    with open(os.path.join(TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
        f.write("\n")


def cut_zip():
    names = sorted(os.listdir(TARGET))
    with zipfile.ZipFile(os.path.join(TASK, "target.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, docs.ZIPTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, n), "rb") as f:
                z.writestr(zi, f.read())


def build():
    os.makedirs(TARGET, exist_ok=True)
    for n in os.listdir(TARGET):
        os.remove(os.path.join(TARGET, n))
    n_old, n_new = buoy_files()
    registers()
    campaign_plan()
    rows = dpr()
    monitor()
    crew_rotation()
    a1 = statements()
    a2 = atlas()
    a3, calls = port_charges()
    figs = main_figures()
    figs.update({"ask_statements_days": a1, "ask_atlas_weather_standby_hours": a2, "ask_port_dues_eur": a3})
    # every figure as the write-up and the goldens state it
    ndiv = sum(1 for y, (tr, ev, d) in PT.items() for (s_, k, h, p) in ev if k == "arrive_continue")
    figs["stated"] = {
        "avoided_whole_days": {k: int(round(v)) for k, v in figs["avoided_days"].items()},
        "own_whole_days": {k: int(round(v)) for k, v in figs["own_downtime_days_all_floating"].items()},
        "gap_whole_days": int(round(figs["gap_days"])),
        "port_dues_nearest_10": {k: int(round(v, -1)) for k, v in a3.items()},
        "statements_two_decimals": {k: "%.2f" % v for k, v in a1.items()},
        "taken_berth_arrivals_2023_2026": ndiv,
        "limits_m": [W.LW, W.LS], "critical_lift_hours": W.TC}
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
        f.write("\n")
    metadata({"buoy_hm0_2008_2017.csv": n_old, "buoy_hs_2016_2026.csv": n_new,
              "daily_progress_reports_2023_2026.csv": len(rows)})
    cut_zip()
    return figs


if __name__ == "__main__":
    f = build()
    print(json.dumps(f, indent=1, sort_keys=True))
