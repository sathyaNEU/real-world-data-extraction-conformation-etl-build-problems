"""Writes target/ from the clean truth: the exports the airport's systems produce, with their own conventions.

Every file here is something a real system or person would hand over; none describes the others.
"""
import datetime as dt
import json
import os
from collections import defaultdict

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import docs
import io_util as IO
import params as P

FILES = {
    "tip": "tip_events_20250701_20261130.csv",
    "library": "tip_library_catalogue_r1.xlsx",
    "logins": "ct_operator_logins.csv",
    "register": "screening_officer_register.xlsx",
    "standard": "SCS-04_screening_officer_competency_standard_rev6.pdf",
    "roster": "lane_roster_20251201_20261130.csv",
    "leave": "hr_leave_taken_20251201_20261130.csv",
    "throughput": "ct_unit_bag_counts_hourly_utc.csv",
    "units": "ct_unit_register.csv",
    "queues": "checkpoint_queue_times_daily_2026.csv",
    "cbt": "xray_cbt_sessions_2026.csv",
    "tipcfg": "tip_projection_settings.json",
}
DISTRACTORS = ["queues", "cbt", "tipcfg"]
CAT_NAME = {c[0]: c[2] for c in P.CATS}
CAT_CODE = {c[0]: c[1] for c in P.CATS}


def local_dt(d, minute):
    naive = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=minute)
    return naive.replace(tzinfo=P.TZ)


def to_utc(d, minute):
    return local_dt(d, minute).astimezone(P.UTC)


def hhmm(minute):
    minute = int(round(minute))
    return "%02d:%02d" % (minute // 60, minute % 60)


class Identities:
    """Names, staff numbers, payroll numbers and CT logins, all drawn from one stream."""

    def __init__(self, world):
        r = np.random.default_rng(P.SEED + 11)
        assert len(P.OFFICER_NAMES) >= len(world.off)
        perm = np.random.default_rng(P.SEED + 1).permutation(len(P.OFFICER_NAMES))
        self.name = {o["idx"]: tuple(P.OFFICER_NAMES[perm[k]].split(" ", 1)) for k, o in enumerate(world.off)}
        n = world.n_off
        self.staff = {o["idx"]: "SC%05d" % v for o, v in zip(world.off, r.choice(np.arange(10200, 48900), n, replace=False))}
        self.payroll = {o["idx"]: "%07d" % v for o, v in zip(world.off, r.choice(np.arange(3100000, 3999999), n, replace=False))}
        self.dom = {o["idx"]: "OP1%04d" % v for o, v in zip(world.off, r.choice(np.arange(1000, 9999), n, replace=False))}
        self.intl = {o["idx"]: "OP7%04d" % v for o, v in zip(world.off, r.choice(np.arange(1000, 9999), n, replace=False))}


def unit_on(lane, d):
    """The CT unit standing on a lane on a local date (the truth the unit register does not keep)."""
    for ln, day in P.RETROFIT:
        if ln == lane and day <= d <= day + dt.timedelta(days=1):
            return "KX6-0416"
    if lane == "D2":
        return P.NEW_D2 if d >= P.D2_NEW else "KX6-0413"
    if lane == "D5":
        return "KX6-0413" if d >= P.D5_SWAP else "KX6-0416"
    return P.SCANNERS0[lane]


def retrofitted(serial, d):
    if serial == "KX6-0416":
        return d >= dt.date(2026, 6, 2)
    own = {unit_on(ln, dt.date(2026, 11, 30)): day for ln, day in P.RETROFIT}
    day = own.get(serial)
    return day is not None and d >= day + dt.timedelta(days=2)


def build(world, target):
    os.makedirs(target, exist_ok=True)
    ids = Identities(world)
    rng = np.random.default_rng(P.SEED + 29)
    n = {}

    # ---------------------------------------------------------------- TIP events (spine)
    rows = []
    for (op, d, ln, minute, f, hit, k, kf, rt, q) in world.tips:
        t = to_utc(d, minute)
        intl_server = ln in P.INTL and d < P.SERVER_MERGE
        login = ids.intl[op] if intl_server else ids.dom[op]
        num = int(world.fti_num[f])
        image = str(num) if intl_server else "%06d" % num
        cat = CAT_CODE[world.obj_cat[world.fti_obj[f]]]
        rows.append((t, ln, login, image, cat, "HIT" if hit else "MISS", rt, d))
    rows.sort(key=lambda x: (x[0], x[1]))
    out = []
    for t, ln, login, image, cat, res, rt, d in rows:
        rec = (t.strftime("%Y-%m-%dT%H:%M:%S") + "Z", ln, login, image, cat, res, rt)
        out.append(rec)
        if ln == "D3" and d == P.RESEND_DAY:
            pass
    # the re-sent day: D3's records for one day appear a second time, appended where the resend landed
    resend = [x for x, r0 in zip(out, rows) if r0[1] == "D3" and r0[7] == P.RESEND_DAY]
    cut = next(i for i, r0 in enumerate(rows) if r0[7] >= P.RESEND_DAY + dt.timedelta(days=1)) + 37
    out = out[:cut] + resend + out[cut:]
    n["tip"] = IO.write_csv(os.path.join(target, FILES["tip"]),
                            ["event_utc", "lane", "operator_login", "image_no", "threat_category", "result",
                             "decision_ms"], out, newline="\n")

    # ---------------------------------------------------------------- library catalogue
    wb = Workbook()
    ws = wb.active
    ws.title = "Objects"
    ws.append(["Kestrine 3D TIP library, release 1.0, object catalogue"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Exported 1 December 2026 from the TIP library manager"])
    ws.append([])
    ws.append(["object_code", "category", "description", "images"])
    desc = docs.object_descriptions(world, rng)
    order = rng.permutation(P.N_OBJ)
    for i in order:
        ws.append([world.obj_code[i], CAT_NAME[world.obj_cat[i]], desc[i], P.VIEWS])
    ws2 = wb.create_sheet("Images")
    ws2.append(["Kestrine 3D TIP library, release 1.0, image list"])
    ws2["A1"].font = Font(bold=True)
    ws2.append([])
    ws2.append(["image_no", "object_code", "view", "release"])
    views = {1: "orientation A", 2: "orientation B", 3: "orientation C"}
    forder = np.argsort(world.fti_num)
    for f in forder:
        ws2.append(["%06d" % int(world.fti_num[f]), world.obj_code[world.fti_obj[f]], views[int(world.fti_view[f])], "1.0"])
    for wsx, widths in ((ws, (22, 40, 52, 8)), (ws2, (10, 22, 16, 8))):
        for col, wd in zip("ABCD", widths):
            wsx.column_dimensions[col].width = wd
    path = os.path.join(target, FILES["library"])
    wb.save(path)
    IO.repack_ooxml(path, "Keith Keller", "Keith Keller", "2025-06-18T23:05:00Z", "2026-12-01T21:40:00Z",
                    "Kestrine 3D TIP library catalogue", "Silverwattle Coast Airport")
    n["library"] = P.N_OBJ * P.VIEWS

    # ---------------------------------------------------------------- logins
    lrows = []
    worked_intl = set(op for (op, d, ln, *_r) in world.tips if ln in P.INTL and d < P.SERVER_MERGE)
    for o in sorted(world.off, key=lambda o: ids.dom[o["idx"]]):
        i = o["idx"]
        issued = max(P.DAY0, o["endorsed"])
        revoked = (o["left"] + dt.timedelta(days=1)).isoformat() if o["left"] else ""
        lrows.append((ids.dom[i], ids.staff[i], "DOM", issued.isoformat(), revoked))
        if i in worked_intl:
            issued_i = max(P.INTL_CT, o["endorsed"])
            lrows.append((ids.intl[i], ids.staff[i], "INTL", issued_i.isoformat(), "2026-02-28"))
    lrows.sort(key=lambda x: (x[2], x[3], x[0]))
    n["logins"] = IO.write_csv(os.path.join(target, FILES["logins"]),
                               ["login", "staff_no", "server", "issued", "revoked"], lrows)

    # ---------------------------------------------------------------- officer register
    wb = Workbook()
    ws = wb.active
    ws.title = "Officers"
    ws.append(["staff_no", "payroll_no", "surname", "given_name", "employment", "home_checkpoint",
               "xray_endorsed", "endorsement_30_nov_2026", "left"])
    emp = {"FT": "Full-time", "PT": "Part-time", "CA": "Casual"}
    for o in sorted(world.off, key=lambda o: (ids.name[o["idx"]][1], ids.name[o["idx"]][0])):
        i = o["idx"]
        g, s = ids.name[i]
        ws.append([ids.staff[i], ids.payroll[i], s, g, emp[o["kind"]],
                   "Domestic" if o["home"] == "D" else "International", o["endorsed"],
                   "Lapsed" if o["left"] else "Current", o["left"] if o["left"] else None])
    for row in ws.iter_rows(min_row=2, min_col=7, max_col=9):
        for c in row:
            if c.value is not None and c.column in (7, 9):
                c.number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFGHI", (10, 11, 16, 14, 11, 15, 13, 22, 11)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, FILES["register"])
    wb.save(path)
    IO.repack_ooxml(path, "Teresa Malone", "Teresa Malone", "2024-02-06T00:20:00Z", "2026-12-01T22:05:00Z",
                    "Screening officer register", "Silverwattle Coast Airport")
    n["register"] = world.n_off

    # ---------------------------------------------------------------- roster (window)
    rrows = []
    for (i, d, ln, s, e, sick) in world.roster:
        if P.WIN0 <= d <= P.WIN1:
            rrows.append((ids.staff[i], d.isoformat(), ln, hhmm(s), hhmm(e)))
    rrows.sort(key=lambda x: (x[1], x[3], x[2], x[0]))
    n["roster"] = IO.write_csv(os.path.join(target, FILES["roster"]),
                               ["staff_no", "roster_date", "lane", "start", "finish"], rrows)

    # ---------------------------------------------------------------- leave (window)
    lv = []
    for o in world.off:
        i = o["idx"]
        hrs = {"FT": "7.60", "PT": "6.00", "CA": "6.00"}[o["kind"]]
        for d in sorted(world.annual[i]):
            if P.WIN0 <= d <= P.WIN1 and d.weekday() in o["days"]:
                lv.append((ids.payroll[i], "%s, %s" % (ids.name[i][1].upper(), ids.name[i][0]), d.isoformat(),
                           "Annual leave", hrs))
        for d in sorted(world.sick[i]):
            if P.WIN0 <= d <= P.WIN1:
                lv.append((ids.payroll[i], "%s, %s" % (ids.name[i][1].upper(), ids.name[i][0]), d.isoformat(),
                           "Personal leave", hrs))
    lv.sort(key=lambda x: (x[2], x[0]))
    n["leave"] = IO.write_csv(os.path.join(target, FILES["leave"]),
                              ["payroll_no", "employee", "leave_date", "leave_type", "hours"], lv)

    # ---------------------------------------------------------------- CT unit hourly counts (UTC)
    counts = defaultdict(int)
    lo = dt.datetime(2025, 11, 30, 0, tzinfo=P.UTC)
    hi = dt.datetime(2026, 11, 30, 23, tzinfo=P.UTC)
    for (d, ln, s, length, bags, op) in world.slots:
        if ln in P.INTL and d < P.INTL_CT:
            continue
        t = to_utc(d, s)
        if not (lo <= t <= hi + dt.timedelta(minutes=59)):
            continue
        hour = t.replace(minute=0, second=0)
        counts[(hour, unit_on(ln, d))] += bags
    # performance-test images counted by retrofitted units before the lane's first rostered officer starts
    first_rostered = {}
    for (i, dd, ln, s, e, sick) in world.roster:
        first_rostered[(dd, ln)] = min(first_rostered.get((dd, ln), 9999), s)
    d = P.WIN0 - dt.timedelta(days=1)
    while d <= P.WIN1 + dt.timedelta(days=1):
        for ln in P.LANES:
            fo = first_rostered.get((d, ln))
            serial = unit_on(ln, d)
            if fo is None or not retrofitted(serial, d):
                continue
            minute = fo - 60 + int(rng.integers(5, 25))
            t = to_utc(d, minute)
            if lo <= t <= hi + dt.timedelta(minutes=59):
                counts[(t.replace(minute=0, second=0), serial)] += int(rng.integers(P.TEST_IMAGES[0], P.TEST_IMAGES[1] + 1))
        d += dt.timedelta(days=1)
    trows = [(h.strftime("%Y-%m-%d %H:00"), s, c) for (h, s), c in sorted(counts.items()) if c > 0]
    n["throughput"] = IO.write_csv(os.path.join(target, FILES["throughput"]),
                                   ["hour_start_utc", "unit_serial", "bags_imaged"], trows)

    # ---------------------------------------------------------------- unit register (current state only)
    urows = [("KX6-0412", "Kestrine CTX-6", "D1", "2025-07-01", "6.4.2"),
             ("KX6-0413", "Kestrine CTX-6", "D5", "2025-07-01", "6.4.2"),
             ("KX6-0414", "Kestrine CTX-6", "D3", "2025-07-01", "6.4.2"),
             ("KX6-0415", "Kestrine CTX-6", "D4", "2025-07-01", "6.4.2"),
             ("KX6-0416", "Kestrine CTX-6", "Spare (CT store)", "2025-07-01", "6.4.2"),
             ("KX6-0471", "Kestrine CTX-6", "I1", "2025-09-01", "6.4.2"),
             ("KX6-0472", "Kestrine CTX-6", "I2", "2025-09-01", "6.4.2"),
             ("KX6-0590", "Kestrine CTX-6", "D2", "2026-03-05", "6.4.2")]
    n["units"] = IO.write_csv(os.path.join(target, FILES["units"]),
                              ["unit_serial", "model", "location", "commissioned", "firmware"], urows)

    # ---------------------------------------------------------------- distractors
    q = []
    day_bags = defaultdict(int)
    for (d, ln, s, length, bags, op) in world.slots:
        day_bags[(d, "Domestic" if ln in P.DOM else "International")] += bags
    d = dt.date(2026, 1, 1)
    while d <= P.WIN1:
        for cp in ("Domestic", "International"):
            b = day_bags.get((d, cp), 0)
            pax = int(b / rng.uniform(1.42, 1.58))
            p95 = round(float(np.clip(rng.normal(9.5 if cp == "Domestic" else 13.0, 3.2), 2.5, 31.0)), 1)
            q.append((d.isoformat(), cp, pax, p95))
        d += dt.timedelta(days=1)
    n["queues"] = IO.write_csv(os.path.join(target, FILES["queues"]),
                               ["date", "checkpoint", "passengers_screened", "p95_queue_minutes"], q)
    cb = []
    mods = ["CT image interpretation 1", "CT image interpretation 2", "IED components refresher",
            "Liquids, aerosols and gels", "Concealment in electronics", "Firearm parts recognition"]
    for o in world.off:
        if o["left"]:
            continue
        i = o["idx"]
        for _ in range(int(rng.integers(3, 11))):
            day = dt.date(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 320)))
            cb.append((ids.staff[i], day.isoformat(), mods[int(rng.integers(len(mods)))],
                       int(np.clip(rng.normal(82, 9), 48, 100))))
    cb.sort(key=lambda x: (x[1], x[0]))
    n["cbt"] = IO.write_csv(os.path.join(target, FILES["cbt"]),
                            ["staff_no", "session_date", "module", "score_pct"], cb)
    cfg = {"system": "Kestrine TIP manager 3.2", "exported": "2026-12-01T21:12:44Z",
           "library_release": "1.0",
           "lanes": [{"lane": ln, "projection_probability": 0.013,
                      "categories": [CAT_CODE[c[0]] for c in P.CATS]} for ln in P.LANES]}
    with open(os.path.join(target, FILES["tipcfg"]), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(cfg, indent=2) + "\n")
    n["tipcfg"] = len(P.LANES)

    # ---------------------------------------------------------------- governing document
    docs.standard(os.path.join(target, FILES["standard"]))
    n["standard"] = 1
    return ids, n
