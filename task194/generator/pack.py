"""Write the bundle under target/ from the clean truth in sim.py."""
import csv
import datetime as dt
import io
import json
import os
import zipfile

import numpy as np
import openpyxl
from openpyxl.styles import Font

import sim
import world as W

FILES = {
    "flows": "historian_inlet_flows_20260801_20261102.csv",
    "pressure": "aznp_pressure_hourly_2026.csv",
    "register": "dma_register_2026-09.xlsx",
    "amr": "amr_large_user_reads_hourly.csv",
    "accounts": "large_user_accounts.xlsx",
    "billing": "billing_account_events_extract.csv",
    "works": "works_orders_aug_oct_2026.xlsx",
    "assets": "mains_asset_list.csv",
    "valves": "gis_boundary_valves.geojson",
    "prv": "prv_setpoint_log_2026.csv",
    "procedure": "LP04_leakage_procedure_rev3.pdf",
    "rain": "raingauge_hv03_daily_2026.csv",
    "contacts": "customer_contacts_aug_oct_2026.csv",
    "findfix": "find_and_fix_outcomes_2025-26.xlsx",
}
DISTRACTORS = ["rain", "contacts", "findfix"]
ZIPTIME = (2026, 11, 3, 6, 12, 0)


MODIFIED = {}
APP_XML = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
           b'<Company>Arnvale Water</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
           b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')


def fixed_zip(path):
    """Re-write an OOXML container with fixed member times and the stamped dates, so builds are byte-identical."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    mod = MODIFIED.get(id(path), None)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == "docProps/app.xml":
                data = APP_XML
            if name == "xl/workbook.xml":
                data = data.replace(b"<workbookProtection/>", b"")
            if name == "docProps/core.xml" and LAST_MOD[0]:
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              rb"\g<1>" + LAST_MOD[0].strftime("%Y-%m-%dT%H:%M:%SZ").encode() + rb"\g<2>", data)
            info = zipfile.ZipInfo(name, ZIPTIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)


LAST_MOD = [None]


def xlsx_props(wb, creator, modifier, created, modified, title=None):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = modifier
    wb.properties.created = created
    wb.properties.modified = modified
    LAST_MOD[0] = modified
    if title:
        wb.properties.title = title


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- flows
def write_flows(target, S, rng):
    rows = []
    ts = S["ts"]
    qrng = np.random.default_rng(W.SEED + 22)   # the historian's quality codes, own stream
    nights = lambda d: W.BASE_NIGHTS[0] <= d <= W.BASE_NIGHTS[1] or W.COMP_NIGHTS[0] <= d <= W.COMP_NIGHTS[1]
    outside = [not nights(sim.local(t).date()) for t in ts]

    def gap_end(tag, prev, t):
        return (tag in ("NR01_FT", "CRK_FM1") and prev == dt.datetime(2026, 8, 13, 8, 45)) or \
               (tag == "HEN_FM2" and prev == dt.datetime(2026, 8, 27, 21, 45))
    for a in W.AREAS:
        code, name, tags = a[0], a[1], a[2]
        q = S["flows"][code]
        if len(tags) == 1:
            parts = [(tags[0][0], q)]
        else:
            w = 0.57 if code == "D4136" else 0.66
            wob = w + rng.normal(0, 0.015, len(q))
            parts = [(tags[0][0], q * wob), (tags[1][0], q * (1 - wob))]
        for tag, v in parts:
            unit = dict(tags)[tag]
            val = v * (1 + rng.normal(0, 0.006, len(v)))
            val = val / 3.6 if unit == "l/s" else val
            dec = 3 if unit == "l/s" else 2
            stuck_from = None
            if tag == "OAK_FM1":
                stuck_from = (dt.datetime(2026, 8, 22, 2, 15), dt.datetime(2026, 8, 22, 11, 30))
            last = None
            u = qrng.random(len(ts))
            qual = np.where(u < 0.0004, "BAD", np.where(u < 0.0019, "UNCERTAIN", "GOOD"))
            for i, t in enumerate(ts):
                if i and outside[i] and gap_end(tag, ts[i - 1], t):
                    qual[i] = "UNCERTAIN"   # first stored reading after a telemetry outage
                if tag in ("NR01_FT", "CRK_FM1") and dt.datetime(2026, 8, 13, 9) <= t < dt.datetime(2026, 8, 13, 16, 30):
                    continue   # telemetry outage, nothing stored
                if tag == "HEN_FM2" and dt.datetime(2026, 8, 27, 22) <= t < dt.datetime(2026, 8, 28, 1, 45):
                    continue
                x = round(float(val[i]), dec)
                if stuck_from and stuck_from[0] <= t < stuck_from[1]:
                    x = last
                last = x
                rows.append((tag, iso(t), ("%." + str(dec) + "f") % x, qual[i] if outside[i] else "GOOD"))
    with open(os.path.join(target, FILES["flows"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["TagName", "TimestampUTC", "Value", "Quality"])
        w.writerows(rows)
    return len(rows)


def write_pressure(target, S, rng):
    bar = {"PL-2290", "PL-2017", "PL-2193"}
    rows = []
    ts = S["ts"]
    for a in W.AREAS:
        code, pl = a[0], a[6]
        p = S["press"][code]
        for i in range(0, len(ts), 4):
            m = float(np.mean(p[i:i + 4])) + float(rng.normal(0, 0.05))
            if pl in bar:
                rows.append((pl, iso(ts[i]), "%.3f" % (m * 0.0980665), "bar"))
            else:
                rows.append((pl, iso(ts[i]), "%.2f" % m, "m"))
    with open(os.path.join(target, FILES["pressure"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["logger_id", "hour_start_utc", "mean_pressure", "unit"])
        w.writerows(rows)


def write_register(target, S):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Areas"
    ws.append(["Arnvale Water - District Metered Area register (Network Operations)", None, None, None,
               None, None, None, None, None])
    ws["A1"].font = Font(bold=True)
    ws.append(["Issue 14, 1 September 2026. Property counts are connected properties at the issue date."])
    ws.append([])
    ws.append(["Area code", "Area name", "Inlet meter tag(s)", "Household properties", "Non-household properties (not logged)",
               "Mains length (km)", "AZNP logger", "Inlet PRV", "Previous code"])
    for a in W.AREAS:
        code, name, tags, hh, nhh, km, pl = a[:7]
        ws.append([code, name, "; ".join(t for t, _ in tags), hh, nhh, km, pl, "Y" if code in ("D4149", "D4136", "D4180") else "N",
                   W.OLD_CODE.get(code, "")])
    for col, wd in zip("ABCDEFGHI", (11, 18, 26, 12, 14, 10, 11, 9, 12)):
        ws.column_dimensions[col].width = wd
    sp = wb.create_sheet("Supply points")
    sp.append(["Supply point", "Area code", "Connection size (mm)", "Revenue meter"])
    rng = np.random.default_rng(W.SEED + 5)
    for u in S["users"]:
        for m in u["meters"]:
            if m.get("sub") or (u["start"] is not None and u["start"] > dt.datetime(2026, 9, 1)):
                continue
            sp.append([m["sp"], m["area"], int(rng.choice([25, 32, 50, 63, 80, 100])), m["serial"]])
    tags = wb.create_sheet("Instrument units")
    tags.append(["Tag", "Engineering unit"])
    for a in W.AREAS:
        for t, u in a[2]:
            tags.append([t, u])
    xlsx_props(wb, "Colin Ward", "Colin Ward", dt.datetime(2024, 2, 12, 9, 3), dt.datetime(2026, 9, 1, 8, 47),
               "DMA register")
    p = os.path.join(target, FILES["register"])
    wb.save(p)
    fixed_zip(p)


# ---------------------------------------------------------------- large users
def write_amr(target, S, rng):
    """Hourly cumulative register reads per meter, as the AMR head-end exports them."""
    rows = []
    ts = S["ts"]
    hours = list(range(0, len(ts), 4))
    exchange = None
    install = []
    for k, u in enumerate(S["users"]):
        for j, m in enumerate(u["meters"]):
            q = m["q"]
            hourly = np.array([q[i:i + 4].mean() for i in hours])     # m3 in each hour
            reg = float(rng.uniform(1200, 88000)) + W.REG_TRIM.get(u["name"], 0.0)
            five = m["serial"].startswith("1") and len(rows) % 3 == 0
            if u["name"].startswith("Stanecroft") or u["name"].startswith("Tollbar"):
                reg, five = 99170.0 + rng.uniform(0, 400), True
            serial = m["serial"]
            started = u["start"] is None
            for n, i in enumerate(hours):
                t = ts[i]
                if not started:
                    if t >= u["start"] - dt.timedelta(hours=1):
                        started, reg = True, 0.0
                    else:
                        continue
                if u["name"].startswith("R. Pennock") and t == dt.datetime(2026, 10, 14, 10):
                    # meter exchange: the old meter's last read, then a reconditioned meter reading from its own register
                    exchange = (serial, "15A%06d" % int(rng.integers(100000, 999999)))
                    rows.append((serial, iso(t), "%.1f" % reg))
                    serial, reg = exchange[1], 31442.6
                    # the fitter's install read on the reconditioned meter, taken as the supply is turned back on
                    install.append((len(rows), (serial, iso(t), "%.1f" % (reg + float(hourly[n + 1])))))
                    continue
                reg += float(hourly[n])
                shown = reg % 100000.0 if five else reg
                rows.append((serial, iso(t), "%.1f" % shown))
            m["final_serial"] = serial
    for pos, row in reversed(install):
        rows.insert(pos, row)
    with open(os.path.join(target, FILES["amr"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["meter_serial", "read_time_utc", "register_m3"])
        w.writerows(rows)
    return exchange


def write_accounts(target, S, exchange):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Large users"
    ws.append(["Account", "Customer", "Area (account)", "Meter serial", "Meter role", "Supply point", "Logged since"])
    for u in S["users"]:
        acc_area = W.OLD_CODE.get(u["area"], u["area"]) if u["name"] in ("Gorsey Bank Hotel",) else u["area"]
        if u["name"].startswith("R. Pennock"):
            acc_area = W.OLD_CODE["D3341"]
        # accounts opened before the April 2025 boundary change keep the area they were opened in
        acc_area = W.ACCOUNT_AREA_2019.get(u["name"], acc_area)
        for m in u["meters"]:
            serial = m["serial"]
            since = "2019-03" if u["start"] is None else u["start"].strftime("%Y-%m")
            role = "Check" if m.get("sub") else "Revenue"
            ws.append([u["uid"], u["name"], acc_area, serial, role, m["sp"], since])
            if exchange and serial == exchange[0]:
                ws.append([u["uid"], u["name"], acc_area, exchange[1], "Revenue", m["sp"], "2026-10"])
    xlsx_props(wb, "Billing Operations", "Kirsty Lloyd", dt.datetime(2023, 6, 1, 14, 20), dt.datetime(2026, 10, 30, 16, 5))
    p = os.path.join(target, FILES["accounts"])
    wb.save(p)
    fixed_zip(p)


# ---------------------------------------------------------------- billing events
def billing(rng):
    """Account events per property; the clean truth of occupancy at 31 October 2026 23:59 local."""
    ev = []
    truth = {}
    pref_no = 410000
    side = np.random.default_rng(W.SEED + 20)   # same-day changes of occupier and earlier occupiers' accounts
    for a in W.AREAS:
        code, hh, nhh = a[0], a[3], a[4]
        nprop = int(hh * rng.uniform(0.985, 1.01)) + nhh
        for k in range(nprop):
            pref_no += int(rng.integers(1, 9))
            pref = "P%07d" % pref_no
            typ = "HH" if k < nprop - nhh else "NHH"
            acc = "%08d" % int(rng.integers(10000000, 99999999))
            occ_from = dt.date(int(rng.integers(2008, 2026)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            posted = dt.datetime.combine(occ_from, dt.time(9)) + dt.timedelta(days=int(rng.integers(0, 20)), hours=int(rng.integers(0, 8)))
            area_at = W.OLD_CODE.get(code, code) if posted < dt.datetime(2025, 4, 1) else code
            occ_row = [pref, acc, "OCC", occ_from, posted, area_at, typ]
            ev.append(occ_row)
            state, cur_type = True, typ
            r = rng.random()
            if r < 0.06:      # vacated, sometimes re-let
                vdate = occ_from + dt.timedelta(days=int(rng.integers(60, 2400)))
                if vdate <= dt.date(2026, 11, 1):
                    vpost = dt.datetime.combine(vdate, dt.time(10)) + dt.timedelta(days=int(rng.integers(0, 45)))
                    if vpost <= dt.datetime(2026, 11, 2, 18):
                        vac_row = [pref, acc, "VAC", vdate, vpost, W.OLD_CODE.get(code, code) if vpost < dt.datetime(2025, 4, 1) else code, cur_type]
                        ev.append(vac_row)
                        state = vdate > dt.date(2026, 10, 31)
                        if rng.random() < 0.55:
                            ndate = vdate + dt.timedelta(days=int(rng.integers(5, 300)))
                            noff = int(rng.integers(0, 12))
                            npost = dt.datetime.combine(ndate, dt.time(11)) + dt.timedelta(days=noff)
                            if vdate <= dt.date(2026, 10, 24) and side.random() < 0.45:
                                # the incoming occupier's account opens on the day the outgoing one closes; the move-in
                                # is keyed at once and the outgoing final bill posts when its closing read is in
                                ndate = vdate
                                npost = dt.datetime.combine(ndate, dt.time(11)) + dt.timedelta(days=noff % 3, minutes=int(side.integers(0, 300)))
                                if vac_row[4] <= npost:
                                    vac_row[4] = npost + dt.timedelta(days=int(side.integers(1, 6)), hours=int(side.integers(1, 7)))
                                    vac_row[5] = W.OLD_CODE.get(code, code) if vac_row[4] < dt.datetime(2025, 4, 1) else code
                            if npost <= dt.datetime(2026, 11, 2, 18):
                                acc2 = "%08d" % int(rng.integers(10000000, 99999999))
                                ev.append([pref, acc2, "OCC", ndate, npost, code if npost >= dt.datetime(2025, 4, 1) else W.OLD_CODE.get(code, code), cur_type])
                                state = state or ndate <= dt.date(2026, 10, 31)
                                if ndate > dt.date(2026, 10, 31) and vdate <= dt.date(2026, 10, 31):
                                    state = False
            elif r < 0.075:   # a landlord account alongside the tenant's
                acc2 = "%08d" % int(rng.integers(10000000, 99999999))
                d2 = occ_from + dt.timedelta(days=int(rng.integers(0, 30)))
                ev.append([pref, acc2, "OCC", d2, dt.datetime.combine(d2, dt.time(15)), code if d2 >= dt.date(2025, 4, 1) else W.OLD_CODE.get(code, code), typ])
            elif r < 0.083 and typ == "HH":   # a house converted to a shop or office
                cdate = dt.date(int(rng.integers(2016, 2027)), int(rng.integers(1, 11)), int(rng.integers(1, 28)))
                if cdate <= dt.date(2026, 10, 31):
                    cpost = dt.datetime.combine(cdate, dt.time(12)) + dt.timedelta(days=int(rng.integers(0, 30)))
                    conv_acc = acc
                    if (cdate, cpost) < (occ_from, posted):
                        # converted under an earlier occupier: the class change sits on that occupier's account and the
                        # present account was opened on the converted class
                        conv_acc = "%08d" % int(side.integers(10000000, 99999999))
                        occ_row[6] = "NHH"
                    ev.append([pref, conv_acc, "CONV", cdate, cpost, code if cpost >= dt.datetime(2025, 4, 1) else W.OLD_CODE.get(code, code), "NHH"])
                    cur_type = "NHH"
            truth[pref] = (code, state, cur_type)
    order = rng.permutation(len(ev))
    ev = [ev[i] for i in order]
    ev.sort(key=lambda e: e[4])
    return ev, truth


def spread_posted(ev):
    """Posting times as the billing system writes them: move-ins and conversions keyed by hand through the day, most
    final bills posted by the overnight billing run, the rest keyed by hand. A property whose events would change
    order within an effective date keeps its keyed times."""
    rng = np.random.default_rng(W.SEED + 21)
    cut = dt.datetime(2026, 11, 2, 18)
    out = []
    for e in ev:
        p = e[4]
        if e[2] == "VAC" and rng.random() < 0.62:
            q = dt.datetime.combine(p.date() + dt.timedelta(days=1), dt.time(1, 20)) + dt.timedelta(minutes=int(rng.integers(0, 75)))
            p = q if q <= cut else p + dt.timedelta(minutes=int(rng.integers(0, 60)))
        else:
            p = p + dt.timedelta(minutes=int(rng.integers(0, 60)))
            if p > cut:
                p = e[4]
        out.append(e[:4] + [p] + e[5:])
    def order(rows):
        by = {}
        for i, r in enumerate(rows):
            by.setdefault(r[0], []).append((r[3], r[4].strftime("%Y-%m-%d %H:%M"), i))
        return {k: [x[2] for x in sorted(v)] for k, v in by.items()}
    o0, o1 = order(ev), order(out)
    keep = {k for k in o0 if o0[k] != o1[k]}
    return [ev[i] if ev[i][0] in keep else out[i] for i in range(len(ev))]


def write_billing(target, ev):
    ev = spread_posted(ev)
    ev = sorted(ev, key=lambda e: e[4])
    with open(os.path.join(target, FILES["billing"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["property_ref", "account_no", "event", "effective_date", "posted", "area_code", "property_class"])
        for e in ev:
            w.writerow([e[0], e[1], e[2], e[3].strftime("%d/%m/%Y"), e[4].strftime("%Y-%m-%d %H:%M"), e[5], e[6]])


# ---------------------------------------------------------------- works orders and assets
def assets(rng):
    out = []
    n = 4100
    for a in W.AREAS:
        for k in range(int(a[5] * 3.2)):
            n += int(rng.integers(1, 12))
            out.append(("WM-%06d" % n, a[0], int(rng.choice([63, 90, 100, 125, 150, 180, 225])),
                        str(rng.choice(["DI", "CI", "PE", "PVC", "AC"])), int(rng.integers(1890, 2021))))
    return out


def works(rng, assets_):
    by_area = {}
    for a in assets_:
        by_area.setdefault(a[1], []).append(a[0])
    jobs = []
    truth = {a[0]: 0 for a in W.AREAS}
    jn = 80312
    start = dt.datetime(2026, 7, 20)
    for d in range(105):
        day = start + dt.timedelta(days=d)
        for _ in range(int(rng.poisson(1.6))):
            code = W.AREAS[int(rng.integers(0, len(W.AREAS)))][0]
            jn += int(rng.integers(3, 40))
            job = "W26-%07d" % jn
            asset = str(rng.choice(by_area[code]))
            kind = rng.random()
            raised = day + dt.timedelta(hours=int(rng.integers(7, 18)), minutes=int(rng.integers(0, 60)))
            tasks = [("LEAK INVESTIGATE", raised + dt.timedelta(hours=int(rng.integers(2, 30))))]
            if kind < 0.5:
                rep = tasks[0][1] + dt.timedelta(days=int(rng.integers(0, 6)), hours=int(rng.integers(1, 9)))
                tasks.append(("REPAIR MAIN", rep))
                tasks.append(("REINSTATE", rep + dt.timedelta(days=int(rng.integers(3, 28)))))
                if dt.datetime(2026, 8, 1) <= rep + dt.timedelta(hours=1) < dt.datetime(2026, 11, 1):
                    truth[code] += 1
            elif kind < 0.85:
                rep = tasks[0][1] + dt.timedelta(days=int(rng.integers(0, 4)))
                tasks.append(("REPAIR SERVICE", rep))
            else:
                tasks.append(("NO LEAK FOUND", tasks[0][1] + dt.timedelta(hours=2)))
            closed = tasks[-1][1] + dt.timedelta(days=int(rng.integers(0, 6)))
            fmt = asset if rng.random() < 0.6 else "%s/WM" % int(asset[3:])
            contractor = kind < 0.5 and rng.random() < 0.45
            for k, (tt, done) in enumerate(tasks):
                if done > dt.datetime(2026, 11, 3, 6, 12):   # not yet done at the export
                    done, closed = None, dt.datetime(2099, 1, 1)
                if contractor and tt == "REPAIR MAIN":
                    # passed to the term contractor: the in-house task stays open, the repair is the contractor's job
                    jobs.append([job, "/%02d" % (k + 1), tt, fmt, raised, None, None])
                    tc = "TC%06d" % int(rng.integers(100000, 999999))
                    extra = int(rng.integers(1, 9))
                    tclose = None if done is None else min(done + dt.timedelta(days=extra), dt.datetime(2026, 11, 2, 16, 40))
                    jobs.append([tc, "/01", "REPAIR MAIN", job, raised + dt.timedelta(hours=3), done,
                                 tclose if tclose is not None and tclose >= done else None])
                    continue
                jobs.append([job, "/%02d" % (k + 1), tt, fmt, raised, done, closed if closed <= dt.datetime(2026, 11, 2, 17) else None])
    # the Calvert Rise PRV job raised from the Calvert Top pressure complaints
    pjob = "W26-0082471"
    passet = by_area["D4149"][5]
    jobs.append([pjob, "/01", "PRESSURE INVESTIGATE", passet, dt.datetime(2026, 9, 18, 9, 41), dt.datetime(2026, 9, 22, 14, 10), dt.datetime(2026, 10, 2, 8, 55)])
    jobs.append([pjob, "/02", "PRV ADJUST", passet, dt.datetime(2026, 9, 18, 9, 41), dt.datetime(2026, 9, 29, 13, 0),
                 dt.datetime(2026, 10, 2, 8, 55)])
    # the Moorend Low valve job
    vjob = "W26-%07d" % (jn + 17)
    t0 = dt.datetime(2026, 10, 6, 10, 15)
    vasset = by_area["D4123"][3]
    jobs.append([vjob, "/01", "PLANNED VALVE REPLACEMENT", vasset, dt.datetime(2026, 9, 21, 11, 2), t0 + dt.timedelta(hours=6), t0 + dt.timedelta(days=2)])
    jobs.append([vjob, "/02", "REINSTATE", vasset, dt.datetime(2026, 9, 21, 11, 2), t0 + dt.timedelta(days=9), t0 + dt.timedelta(days=9, hours=2)])
    return jobs, truth


def write_works(target, jobs):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Export"
    ws.append(["Job", "Task", "Task type", "Asset", "Raised", "Task completed", "Job closed"])
    def lt(t):
        if t is None:
            return None
        return t + dt.timedelta(hours=1) if t < W.BST_END else t
    for j in sorted(jobs, key=lambda r: (r[4], r[0], r[1])):
        ws.append([j[0], j[1], j[2], j[3], lt(j[4]), lt(j[5]), lt(j[6])])
    for row in ws.iter_rows(min_row=2, min_col=5, max_col=7):
        for c in row:
            c.number_format = "dd/mm/yyyy hh:mm"
    xlsx_props(wb, "WMS Reporting", "Sean Gough", dt.datetime(2026, 11, 2, 17, 30), dt.datetime(2026, 11, 2, 17, 31))
    p = os.path.join(target, FILES["works"])
    wb.save(p)
    fixed_zip(p)


def write_assets(target, assets_):
    with open(os.path.join(target, FILES["assets"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["asset_id", "dma", "diameter_mm", "material", "laid_year"])
        w.writerows(assets_)


def write_valves(target, rng):
    feats = []
    for vid, a, b in W.BOUNDARY:
        x = 438000 + int(rng.integers(-6000, 6000))
        y = 452000 + int(rng.integers(-6000, 6000))
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [x, y]},
                      "properties": {"asset_id": vid, "valve_type": "BOUNDARY", "dma_1": a, "dma_2": b, "status": "CLOSED",
                                     "diameter_mm": int(rng.choice([80, 100, 150])),
                                     "last_operated": (dt.date(2021, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1700)))).isoformat()}})
    gj = {"type": "FeatureCollection", "name": "boundary_valves",
          "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::27700"}}, "features": feats}
    with open(os.path.join(target, FILES["valves"]), "w") as f:
        json.dump(gj, f, indent=1)


def write_prv(target):
    rows = [("D4180", "PRV-S1", "2026-01-21 11:35", "43.5", "43.5", "annual check, no change"),
            ("D4149", "PRV-C1", "2026-02-10 10:05", "38.0", "38.0", "annual check, strainer cleaned"),
            ("D4136", "PRV-H2", "2026-03-17 10:20", "41.0", "41.0", "annual check, no change"),
            ("D4149", "PRV-C1", "2026-04-28 13:50", "38.0", "38.0", "pilot diaphragm replaced, set point unchanged"),
            ("D4180", "PRV-S1", "2026-06-02 14:05", "43.5", "42.5", "fixed outlet lowered after pressure complaints review"),
            ("D4136", "PRV-H2", "2026-07-08 09:15", "41.0", "41.0", "outlet logger swapped, set point unchanged"),
            ("D4149", "PRV-C1", "2026-09-29 14:00", "38.0", "47.0", "raised for low pressure complaints, Calvert Top (W26-0082471)"),
            ("D4136", "PRV-H2", "2026-10-20 09:40", "41.0", "41.0", "pilot serviced, set point unchanged")]
    with open(os.path.join(target, FILES["prv"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dma", "prv", "changed_local", "set_point_before_m", "set_point_after_m", "note"])
        w.writerows(rows)


def write_distractors(target, rng):
    with open(os.path.join(target, FILES["rain"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "rain_mm", "qc_code"])
        d = dt.date(2026, 1, 1)
        while d <= dt.date(2026, 11, 2):
            r = 0.0 if rng.random() < 0.45 else float(np.round(rng.gamma(0.9, 4.2), 1))
            w.writerow([d.isoformat(), "%.1f" % r, "" if rng.random() > 0.01 else "E"])
            d += dt.timedelta(days=1)
    reasons = ["Low pressure", "No water", "Discoloured water", "Leak in street", "Leak on property", "Taste/odour", "Noisy pipes"]
    with open(os.path.join(target, FILES["contacts"]), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["contact_ref", "received", "dma", "category", "status"])
        n = 2200400
        calvert_top = {35: ["Low pressure"], 38: ["Low pressure", "Low pressure"], 41: ["Low pressure"], 44: ["Low pressure", "No water"],
                       47: ["Low pressure"], 52: ["Low pressure"], 57: ["Leak on property"], 61: ["Noisy pipes"]}
        for d in range(93):
            day = dt.datetime(2026, 8, 1) + dt.timedelta(days=d)
            for j, cat in enumerate(calvert_top.get(d, [])):
                n += 3 + 5 * j + d % 7
                w.writerow(["C%08d" % n, (day + dt.timedelta(minutes=500 + 97 * j + 13 * (d % 5))).strftime("%d/%m/%Y %H:%M"),
                            "D4149", cat, "Closed"])
            for _ in range(int(rng.poisson(5.5))):
                n += int(rng.integers(1, 30))
                code = W.AREAS[int(rng.integers(0, len(W.AREAS)))][0]
                w.writerow(["C%08d" % n, (day + dt.timedelta(minutes=int(rng.integers(420, 1320)))).strftime("%d/%m/%Y %H:%M"),
                            code, str(rng.choice(reasons, p=[0.18, 0.08, 0.2, 0.24, 0.16, 0.06, 0.08])),
                            str(rng.choice(["Closed", "Closed", "Closed", "Open"]))])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2025-26"
    ws.append(["Week", "DMA", "Leaks found (mains)", "Leaks found (services)", "Customer-side leaks", "Crew days"])
    for wk in range(1, 53):
        for _ in range(int(rng.integers(1, 3))):
            code = W.AREAS[int(rng.integers(0, len(W.AREAS)))][0]
            ws.append([wk, code, int(rng.poisson(1.1)), int(rng.poisson(2.4)), int(rng.poisson(0.7)), int(rng.integers(2, 6))])
    xlsx_props(wb, "Leakage Team", "Colin Ward", dt.datetime(2025, 4, 7, 8, 30), dt.datetime(2026, 4, 2, 12, 11))
    p = os.path.join(target, FILES["findfix"])
    wb.save(p)
    fixed_zip(p)
