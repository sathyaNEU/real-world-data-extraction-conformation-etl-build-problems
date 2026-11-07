"""task125 pack writers. Each file is written the way the system that keeps it exports it: the records system's
occurrence versions (legacy codes and day-first dates before its March 2023 migration), the city's street segment
file, the paid-duty office's register (the old system's layout to 2023, the Duty Desk layout from 2024), the
communications centre's 2026 CAD export in UTC, the 2026 patrol roster, and two city files."""
import csv
import datetime as dt
import io

import numpy as np

import sim as S
import world as W

FILES = {
    "rms": "mps_rms_occurrences_2022_2026.csv",
    "crosswalk": "rms_offence_code_crosswalk_2023.csv",
    "segments": "mountjoy_street_segments.csv",
    "register": "mps_paid_duty_register_2022_2027.xlsx",
    "cad": "mps_cad_calls_2026.csv",
    "roster": "mps_patrol_roster_2026.csv",
    "wards": "ward_profiles_2021_census.csv",
    "lights": "streetlight_service_requests_2026.csv",
    "protocol": "hot_spot_patrol_protocol_2027.pdf",
    "directive": "patrol_measures_directive_po14.pdf",
    "request": "turner_request_2027_designation.eml",
}
DISTRACTORS = ("wards", "lights")
EXTRACT = dt.datetime(2027, 1, 6, 5, 40)
LEG_DESC = {l: d for l, d, u in W.LEGACY}

EVENT_MIX = [("1430", 0.35), ("2170", 0.25), ("2142", 0.22), ("1420", 0.09), ("1610", 0.05), ("3370", 0.04)]
BASE_MIX = [("2142", 0.27), ("2170", 0.24), ("2120", 0.19), ("1430", 0.17), ("1610", 0.05), ("1420", 0.06),
            ("3370", 0.02)]
OTHER_MIX = [("2144", 0.30), ("2160", 0.18), ("1627", 0.13), ("3410", 0.11), ("1625", 0.07), ("4140", 0.09),
             ("1371", 0.05), ("2135", 0.07)]
CRIME_HOUR = np.array([5.0, 4.6, 4.0, 3.0, 1.9, 1.2, 1.0, 1.4, 2.0, 2.6, 3.0, 3.3, 3.6, 3.7, 3.8, 4.0, 4.3, 4.6,
                       4.9, 5.1, 5.3, 5.5, 5.6, 5.4])
CRIME_HOUR = CRIME_HOUR / CRIME_HOUR.sum()
FIRST_CODE = {"2142": ["2144", "2170"], "1420": ["1430"], "2120": ["2170", "2144"], "1610": ["2144", "1430"],
              "1430": ["1627", "2170"], "2170": ["2144"], "3370": ["1627"]}
AWAY = {"1430": "1627", "2142": "2144", "2170": "2144", "2120": "2144", "1610": "2144", "1420": "1627",
        "3370": "1627"}


def _pick(r, mix):
    u = r.random()
    acc = 0.0
    for c, p in mix:
        acc += p
        if u < acc:
            return c
    return mix[-1][0]


def _legacy_code(r, ucr):
    opts = W.TO_LEGACY[ucr]
    return opts[int(r.integers(len(opts)))]


def _desc(code):
    return W.PATROL.get(code) or W.OTHER.get(code)


def _fmt(t, legacy):
    if t is None:
        return ""
    return t.strftime("%d/%m/%Y %H:%M") if legacy else t.strftime("%Y-%m-%d %H:%M")


def _block(s):
    return "%d BLOCK %s" % (100 * s["blk"], s["street"].upper())


def _node(s, end):
    return "%s / %s" % (s["street"].upper(), (s["from"] if end == 0 else s["to"]).upper())


def _neighbour(segs_by_key, s):
    o, a, b = s["key"]
    for k in ((o, a, b + 1), (o, a, b - 1)):
        if k in segs_by_key:
            return segs_by_key[k]
    return s


# ----------------------------------------------------------------------------------------------- occurrences
def occurrences(r, segs, crimes, nonp):
    """The records system's occurrences: each true founded patrol crime, the patrol reports later unfounded, the
    reports reclassified out of the patrol codes, the other offences, and the reports outside the five years. Each
    occurrence carries its versions; the truth is the final state."""
    byid = {s["id"]: s for s in segs}
    byk = W.by_key(segs)
    occ = []
    for (sid, d, part) in crimes:
        occ.append({"seg": sid, "date": d, "part": part, "final": _pick(r, EVENT_MIX if part != "base" else BASE_MIX),
                    "kind": "patrol"})
    # patrol-coded reports that end unfounded, and reports reclassified out of the patrol codes
    ids = [s["id"] for s in segs]
    wts = np.array([1.0 + 0.5 * nonp[i] for i in ids])
    wts = wts / wts.sum()
    n_unf = int(0.055 * len(crimes))
    n_away = int(0.03 * len(crimes))
    for kind, n in (("unfounded", n_unf), ("away", n_away)):
        for _ in range(n):
            d = W.DAYS[int(r.integers(len(W.DAYS)))]
            occ.append({"seg": int(ids[int(r.choice(len(ids), p=wts))]), "date": d, "part": "base",
                        "final": _pick(r, BASE_MIX), "kind": kind})
    # other offences
    lam = np.array([nonp[i] for i in ids]) / 365.25
    for d in W.DAYS:
        m = r.poisson(lam)
        for k in np.nonzero(m)[0]:
            for _ in range(int(m[k])):
                occ.append({"seg": int(ids[k]), "date": d, "part": "base", "final": _pick(r, OTHER_MIX),
                            "kind": "other"})
        for _ in range(int(r.poisson(0.95))):
            occ.append({"seg": None, "date": d, "part": "base", "final": "2160", "kind": "other"})
    # reports of 2021 occurrences made in 2022, and of 2027 occurrences made before the extract
    for _ in range(64):
        d = dt.date(2021, 12, 1) + dt.timedelta(int(r.integers(0, 31)))
        occ.append({"seg": int(ids[int(r.choice(len(ids), p=wts))]), "date": d, "part": "base",
                    "final": _pick(r, BASE_MIX), "kind": "outside", "late": int(r.integers(32, 70))})
    for _ in range(140):
        d = dt.date(2027, 1, 1) + dt.timedelta(int(r.integers(0, 5)))
        occ.append({"seg": int(ids[int(r.choice(len(ids), p=wts))]), "date": d, "part": "base",
                    "final": _pick(r, BASE_MIX), "kind": "outside"})
    rows = []
    for o in occ:
        _times(r, o)
    occ = [o for o in occ if o["reported"].date() <= W.AS_OF - dt.timedelta(1)]
    occ.sort(key=lambda o: (o["reported"], o["seg"] or 0, o["final"]))
    seqs = {}
    for o in occ:
        legacy = o["reported"] < W.MIGRATION
        y = o["reported"].year
        key = ("L" if legacy else "N", y)
        seqs[key] = seqs.get(key, 0) + 1 + int(r.random() < 0.55) + int(r.random() < 0.18) * int(r.integers(1, 5))
        o["no"] = ("%d-%06d" % (y, seqs[key])) if legacy else ("MP%02d-%06d" % (y % 100, seqs[key]))
        rows += _versions(r, o, byid, byk, legacy)
    return occ, rows


def _times(r, o):
    d = o["date"]
    code = o["final"]
    if o["part"] != "base":
        h = int(r.integers(18, 24))
        t = dt.datetime(d.year, d.month, d.day, h, int(r.integers(60)))
        o["from"], o["to"] = t, None
        o["reported"] = t + dt.timedelta(minutes=int(r.integers(4, 150)))
        return
    u = r.random()
    if code in ("2120", "2142") and u < 0.6:
        h = int(r.integers(17, 24))
        f = dt.datetime(d.year, d.month, d.day, h, int(r.integers(60)))
        to = f + dt.timedelta(minutes=int(r.integers(120, 780)))
        o["from"], o["to"] = f, to
        o["reported"] = to + dt.timedelta(minutes=int(r.integers(10, 300)))
    elif u < 0.975 or o.get("late") or o["kind"] == "outside":
        h = int(r.choice(24, p=CRIME_HOUR))
        f = dt.datetime(d.year, d.month, d.day, h, int(r.integers(60)))
        o["from"], o["to"] = f, None
        o["reported"] = f + dt.timedelta(minutes=int(r.integers(3, 240)))
    else:
        o["from"], o["to"] = None, None
        o["reported"] = dt.datetime(d.year, d.month, d.day, int(r.integers(8, 20)), int(r.integers(60)))
    if o.get("late"):
        o["reported"] = o["reported"] + dt.timedelta(days=o["late"])


def _versions(r, o, byid, byk, legacy):
    s = byid.get(o["seg"]) if o["seg"] else None
    final = o["final"]
    kind = o["kind"]
    nv = 1 + int(r.random() < 0.30) + int(r.random() < 0.06)
    if kind in ("unfounded", "away"):
        nv = max(nv, 2)
    states = []
    for v in range(nv):
        states.append({"code": final, "seg": s, "status": "OPEN"})
    if nv > 1:
        if kind == "unfounded":
            states[-1]["status"] = "UNFOUNDED"
            if nv == 3 and r.random() < 0.5:
                states[1]["status"] = "OPEN"
        elif kind == "away":
            states[-1]["code"] = AWAY.get(final, "2144")
            for st in states[1:]:
                st["code"] = states[-1]["code"]
        else:
            if r.random() < 0.15 and final in FIRST_CODE:
                opts = FIRST_CODE[final]
                states[0]["code"] = opts[int(r.integers(len(opts)))]
            if s is not None and r.random() < 0.03:
                states[0]["seg"] = _neighbour(byk, s)
            states[-1]["status"] = ["OPEN", "CLEARED BY CHARGE", "CLEARED OTHERWISE"][int(r.integers(3))]
    out = []
    t0 = o["reported"] + dt.timedelta(minutes=int(r.integers(5, 90)))
    times = [t0]
    for v in range(1, len(states)):
        times.append(times[-1] + dt.timedelta(days=int(r.integers(1, 21)), minutes=int(r.integers(0, 600))))
    if times[-1] > EXTRACT and len(times) > 1:
        span = (EXTRACT - t0).total_seconds()
        times = [t0 + dt.timedelta(seconds=span * k / len(times)) for k in range(len(times))]
    for v, st in enumerate(states):
        t = times[v]
        lg = t < W.MIGRATION
        code = st["code"]
        lcode = _legacy_code(r, code) if lg else None
        seg = st["seg"]
        if seg is None:
            loc, sid = "ONLINE / TELEPHONE", ""
        else:
            w = r.random()
            loc = _block(seg) if w < 0.8 else _node(seg, int(r.integers(2)))
            sid = str(seg["id"])
        out.append({"occurrence_no": o["no"], "version": v + 1,
                    "version_entered": t.strftime("%d/%m/%Y %H:%M") if lg else t.strftime("%Y-%m-%d %H:%M:%S"),
                    "reported": _fmt(o["reported"], lg), "occurred_from": _fmt(o["from"], lg),
                    "occurred_to": _fmt(o["to"], lg),
                    "offence_code": lcode if lg else code,
                    "offence": LEG_DESC[lcode] if lg else _desc(code),
                    "location": loc, "segment_id": sid,
                    "status": ({"OPEN": "OPEN", "UNFOUNDED": "UNFOUNDED", "CLEARED BY CHARGE": "CLR-CHG",
                                "CLEARED OTHERWISE": "CLR-OTH"}[st["status"]] if lg else st["status"])})
    return out


RMS_COLS = ["occurrence_no", "version", "version_entered", "reported", "occurred_from", "occurred_to",
            "offence_code", "offence", "location", "segment_id", "status"]


def write_rms(rows, path):
    rows = sorted(rows, key=lambda x: (x["occurrence_no"][:2] != "20", x["occurrence_no"], x["version"]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=RMS_COLS, lineterminator="\n")
        w.writeheader()
        for x in rows:
            w.writerow(x)
    return len(rows)


def write_crosswalk(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["legacy_code", "legacy_description", "ucr2_code", "ucr2_description", "effective"])
        for l, d, u in W.LEGACY:
            w.writerow([l, d, u, _desc(u), "2023-03-01"])


def write_segments(segs, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["segment_id", "street", "from_street", "to_street", "left_from", "left_to", "right_from",
                    "right_to", "ward", "length_m", "x_utm17n", "y_utm17n"])
        for s in sorted(segs, key=lambda x: x["id"]):
            w.writerow([s["id"], s["street"].upper(), s["from"].upper(), s["to"].upper(), s["l_from"], s["l_to"],
                        s["r_from"], s["r_to"], s["ward"], "%.1f" % s["len"], "%.1f" % s["x"], "%.1f" % s["y"]])


# ----------------------------------------------------------------------------------------------- the register
PDS_ABBR = {"MEMORIAL GARDENS, 200 WELLINGTON ST": "MEM GARDENS 200 WELLINGTON",
            "LAKESHORE CENTRE, 2015 HARBOUR RD": "LAKESHORE CTR 2015 HARBOUR"}


def _pds_loc(loc):
    if loc in PDS_ABBR:
        return PDS_ABBR[loc]
    return loc.replace(" / ", "/")


def write_register(bks, path, created, modified):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for y in range(2022, 2028):
        ws = wb.create_sheet(str(y))
        rows = [b for b in bks if b["date"].year == y]
        rows.sort(key=lambda b: (b["date"], b["start"], b["no"]))
        if y <= 2023:
            ws.append(["Booking No", "Duty Date", "Time From", "Time To", "Location", "Client", "Category",
                       "Officers", "Status"])
            for b in rows:
                ws.append([b["no"], b["date"].strftime("%d/%m/%Y"), b["start"], b["end"], _pds_loc(b["loc"]),
                           b["client"], b["category"], b["officers"],
                           {"COMPLETED": "COMP", "CANCELLED": "CANC", "CANCELLED LATE": "CANC-LATE"}[b["status"]]])
        else:
            ws.append(["booking_no", "line", "badge", "duty_date", "booked_start", "booked_end", "actual_start",
                       "actual_end", "location", "client", "category", "status"])
            for b in rows:
                for ln in b["lines"]:
                    ws.append([b["no"], ln["line"], ln["badge"], b["date"].strftime("%Y-%m-%d"), b["start"], b["end"],
                               S.hm(ln["a_start"]) if ln["a_start"] is not None else None,
                               S.hm(ln["a_end"]) if ln["a_end"] is not None else None,
                               b["loc"], b["client"], b["category"], ln["status"]])
        for c in ws[1]:
            c.font = Font(bold=True)
        ws.freeze_panes = "A2"
    wb.properties.creator = "MPS Paid Duty Office"
    wb.properties.lastModifiedBy = "MPS Paid Duty Office"
    wb.properties.created = created
    wb.properties.modified = modified
    wb.properties.title = "Paid duty register"
    import zipnorm
    zipnorm.save(wb, path, "xlsx", created, modified)


# ----------------------------------------------------------------------------------------------- CAD and roster
def _utc(t):
    if t is None:
        return ""
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_cad(r, events, path):
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["event_no", "received_utc", "priority", "call_type", "source", "address", "segment_id",
                    "district", "disposition", "unit", "dispatched_utc", "enroute_utc", "onscene_utc",
                    "cleared_utc"])
        seq = 0
        for ev in events:
            seq += 1 + int(r.random() < 0.08)
            ev["no"] = "E26-%06d" % seq
            head = [ev["no"], _utc(ev["received"]), ev["priority"], ev["type"], ev["source"], ev["address"],
                    ev["segment"], ev["district"], ev["disposition"]]
            if not ev["units"]:
                w.writerow(head + ["", "", "", "", ""])
                n += 1
            for u in sorted(ev["units"], key=lambda x: (x["dispatched"], x["unit"])):
                w.writerow(head + [u["unit"], _utc(u["dispatched"]), _utc(u["enroute"]), _utc(u["onscene"]),
                                   _utc(u["cleared"])])
                n += 1
    return n


def write_roster(rost, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["tour_date", "tour", "unit", "officer_1", "officer_2"])
        for (d, s, u) in sorted(rost, key=lambda k: (k[0], k[1], S.ALL_UNITS.index(k[2]))):
            crew = rost[(d, s, u)]
            w.writerow([d.isoformat(), s, u, crew[0], crew[1] if len(crew) > 1 else ""])


# ----------------------------------------------------------------------------------------------- city files
def write_wards(path):
    rows = [(1, 15210, 7480, 52400, 61.2, 3.9), (2, 14870, 6390, 61800, 44.7, 6.8), (3, 16030, 7110, 58900, 49.3, 5.2),
            (4, 14420, 5920, 71300, 33.8, 9.7), (5, 15960, 6450, 79600, 27.4, 11.3),
            (6, 14980, 6020, 83900, 22.1, 14.6), (7, 15540, 6510, 74200, 30.9, 10.9),
            (8, 13690, 5210, 88700, 18.6, 21.4)]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ward", "population_2021", "private_households_2021", "median_household_income_2020",
                    "pct_households_renting", "land_area_km2"])
        for row in rows:
            w.writerow(row)


def write_lights(r, segs, path):
    issues = ["LIGHT OUT", "LIGHT OUT", "LIGHT OUT", "FLICKERING", "DAY BURNER", "POLE DAMAGED", "WIRE EXPOSED"]
    rows = []
    seq = 26000 + int(r.integers(100, 900))
    d = dt.date(2026, 1, 1)
    while d <= dt.date(2026, 12, 31):
        for _ in range(int(r.poisson(6.4 if d.month in (10, 11, 12, 1, 2) else 4.6))):
            s = segs[int(r.integers(len(segs)))]
            seq += 1 + int(r.random() < 0.4)
            iss = issues[int(r.integers(len(issues)))]
            closed = d + dt.timedelta(int(r.gamma(2.0, 4.0)))
            status = "CLOSED" if closed <= dt.date(2027, 1, 5) else "OPEN"
            rows.append(["SR-%d" % seq, d.isoformat(), s["id"], "%d %s" % (S.address(r, s), s["street"].upper()),
                         iss, status, closed.isoformat() if status == "CLOSED" else ""])
        d += dt.timedelta(1)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["request_no", "received", "segment_id", "address", "issue", "status", "closed"])
        for row in rows:
            w.writerow(row)
    return len(rows)
