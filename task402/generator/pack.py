"""Write the pack under target/ from the world. Every key, clock and layout here is the organisation's own."""
import csv, os, json
import numpy as np
import pandas as pd
import pyarrow as pa, pyarrow.parquet as pq
import asks, docs, world
from world import D0, NDAY

DIST = ["North", "Lakes", "Prairie", "River"]
OLD_SUP = ["Halvorsen Electric", "Dunmore Transformer"]
NEW_SUP = "Brekke Power Products"


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def lt_str(m):
    """Local wall-clock minutes to the outage system's text; the hour the clocks skip in March is never shown."""
    ts = asks.local_ts(np.atleast_1d(m)).floor("s")
    idx = pd.DatetimeIndex(ts)
    loc = idx.tz_localize(asks.TZ, ambiguous=False, nonexistent="shift_forward").tz_localize(None)
    return [x.strftime("%Y-%m-%d %H:%M:%S") for x in loc]


def members_served(end_count, seed, growth=0.010):
    """Members served at the end of each local day from 1 October 2020: new services connect on working days, most in
    the building season, a few accounts close, and the count meets the register's on 30 September 2026 (about 1 per
    cent a year, the household growth of the exurban counties north of the Twin Cities)."""
    rng = np.random.default_rng(seed)
    days = pd.date_range(D0, periods=NDAY, freq="D")
    work = (days.dayofweek < 5).astype(float)
    season = np.array([0.7, 0.75, 0.95, 1.1, 1.25, 1.35, 1.3, 1.25, 1.2, 1.1, 0.9, 0.75])[days.month - 1]
    net_year = end_count * growth
    lam = work * season
    adds = rng.poisson(lam / lam.sum() * net_year * NDAY / 365.25 * 1.15)
    drops = rng.poisson(work / work.sum() * net_year * 0.15 * NDAY / 365.25)
    net = adds - drops
    after = np.r_[np.cumsum(net[::-1])[::-1][1:], 0]      # the net change after each day
    return (end_count - after).astype(int)


def scrub_parquet(path, new=b"parquet-mr version 1.13.1 (build db4183109d5b734ec5930d870cdae161e408ddba)"):
    b = open(path, "rb").read()
    flen = int.from_bytes(b[-8:-4], "little")
    foot = b[-8 - flen:-8]
    i = foot.find(b"parquet-cpp-arrow version")
    L = foot[i - 1]
    foot2 = foot[:i - 1] + bytes([len(new)]) + new + foot[i + L:]
    open(path, "wb").write(b[:-8 - flen] + foot2 + len(foot2).to_bytes(4, "little") + b"PAR1")


def ids(W, seed):
    rng = np.random.default_rng(seed)
    S, X, G, Rr = W["S"], W["X"], W["G"], W["Rr"]
    nf = int(S.feeder.max()) + 1
    subs, k, sub = [], 0, 1
    while k < nf:
        n = int(rng.integers(3, 7))
        subs += [(sub, j + 1) for j in range(min(n, nf - k))]
        k += n; sub += 1
    fname = ["F%02d%d" % s for s in subs]
    sid = ["S%05d" % x for x in rng.choice(np.arange(10000, 99999), len(S), replace=False)]
    order = S.groupby("feeder").cumcount() + 1
    old = ["%s-%d" % (fname[f], o) for f, o in zip(S.feeder.values, order.values)]
    dev = []
    nums = rng.choice(np.arange(1000, 9999), len(S), replace=False)
    fz = np.random.default_rng(seed + 29).choice(np.arange(10000, 99999), len(S), replace=False)
    for t, n, z in zip(S.device.values, nums, fz):
        dev.append({"SECT": "SX-%04d" % n, "RCLR": "R%04d" % n, "FUSE": "FU-%05d" % z}[t])
    xid = ["T%06d" % x for x in rng.choice(np.arange(100000, 999999), len(X), replace=False)]
    poles = rng.choice(np.arange(100000, 999999), len(G) + len(Rr), replace=False)
    gp = ["P%06d" % x for x in poles[:len(G)]]
    rp = ["P%06d" % x for x in poles[len(G):]]
    return dict(fname=fname, sid=sid, old=old, dev=dev, xid=xid, gp=gp, rp=rp)


def build(out, W, F, O, R, EMP, seed=4022):
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(seed)
    S, X, G, Rr = W["S"], W["X"], W["G"], W["Rr"]
    K = ids(W, seed + 1)
    members = int(S.members.sum())
    X0m = world.X0 * 1440
    # ------------------------------------------------ steps and customer minutes for every interruption
    n = len(F)
    cmi = np.zeros(n); steps_rows = []
    eid = []
    lgnum = 2100000 + np.cumsum(1 + np.random.default_rng(seed + 13).poisson(0.6, n))
    for i, r in enumerate(F.itertuples()):
        legacy = r.start < world.GIS_DAY * 1440
        eid.append(("LG%07d" % lgnum[i]) if legacy else None)
    newids = world.uuid4s(rng, n)
    eid = [e if e else u for e, u in zip(eid, newids)]
    F = F.assign(event_id=eid)
    for i, r in enumerate(F.itertuples()):
        k = int(r.steps)
        if k > 1:
            gap = (r.end - r.start - r.repair) / (k - 1)
            tk = [r.start + r.repair + j * gap for j in range(k)]
            parts = rng.multinomial(r.ci - k, np.ones(k) / k) + 1
        else:
            tk = [r.end]; parts = [r.ci]
        cmi[i] = sum(p * (t - r.start) for p, t in zip(parts, tk))
        if r.start >= world.day("2024-10-01") * 1440:
            s = int(r.sec)
            dev = K["xid"][int(r.xf)] if r.level == "transformer" else K["dev"][s]
            for j, (p, t) in enumerate(zip(parts, tk)):
                steps_rows.append((i, j + 1, dev, K["sid"][s], t, int(p)))
    F = F.assign(cmi=cmi)
    # ------------------------------------------------ the outage extract, fiscal 2022 to 2026
    E = F[F.start >= X0m].copy()
    E = E[(E.end - E.start) >= 5]
    sec = E.sec.values.astype(int)
    feeder_at = np.where((E.start.values >= world.RESECT * 1440) & (E.kind.values != "transfer"), S.feeder_new.values[sec], S.feeder.values[sec])
    rows = []
    s_l, e_l = lt_str(E.start.values), lt_str(E.end.values)
    wo = rng.choice(np.arange(1000000, 9999999), len(E), replace=False)
    for j, r in enumerate(E.itertuples()):
        s = int(r.sec)
        legacy = r.start < world.GIS_DAY * 1440
        lvl = r.level == "transformer"
        devid = K["xid"][int(r.xf)] if lvl else K["dev"][s]
        dtype = "XFMR" if lvl else S.device.values[s]
        struct = K["gp"][int(r.site)] if r.site >= 0 else (K["rp"][int(r.riser)] if r.riser >= 0 else "")
        rows.append([r.event_id, s_l[j], e_l[j], devid, dtype, K["old"][s] if legacy else K["sid"][s],
                     K["fname"][feeder_at[j]], DIST[S.district.values[s]], int(r.ci), int(round(r.cmi)), r.cause,
                     "Y" if r.planned else "N", struct, K["xid"][int(r.xf)] if lvl else "", "OW%d" % wo[j]])
    write_csv(os.path.join(out, "outage_events_fy2022-fy2026.csv"),
              ["event_id", "start_local", "end_local", "device_id", "device_type", "section_id", "feeder", "district",
               "customers_interrupted", "customer_minutes", "cause_code", "planned", "structure_id", "transformer_id",
               "work_order"], rows)
    E["work_order"] = ["OW%d" % w for w in wo]
    # ------------------------------------------------ the control centre's switching log, restoration steps, fiscal 2025 and 2026
    # orders are numbered through each fiscal year with every other switching job the centre writes (maintenance,
    # tagging, load transfers), so a restoration's number joins to nothing in the outage system: its device and its
    # times do
    rs = np.random.default_rng(seed + 9)
    num, fy_cur, seq = {}, None, 0
    for i in sorted({a for a, *_ in steps_rows}, key=lambda i: F.start.values[i]):
        fy = (D0 + pd.Timedelta(minutes=float(F.start.values[i]))).year + ((D0 + pd.Timedelta(minutes=float(F.start.values[i]))).month >= 10)
        if fy != fy_cur:
            fy_cur, seq = fy, int(rs.integers(3, 30))
        seq += 1 + int(rs.poisson(1.3))
        num[i] = "SW%02d-%05d" % (fy % 100, seq)
    st = [(num[a], b, dv, sc, lt_str([c])[0], d) for a, b, dv, sc, c, d in steps_rows]
    write_csv(os.path.join(out, "restoration_steps_fy2025-fy2026.csv"),
              ["switching_order", "step", "device_id", "section_id", "restored_local", "customers_restored"], st)
    # ------------------------------------------------ recloser operations, fiscal 2026, UTC
    tu = asks.utc(O.t.values)
    dv = [("CB-" + K["fname"][int(i)]) if k == "B" else K["dev"][int(i)] for k, i in zip(O.kind.values, O.id.values)]
    so = [[t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000), d, op] for t, d, op in zip(tu, dv, O.op.values)]
    write_csv(os.path.join(out, "scada_reclosing_operations_fy2026.csv"), ["time_utc", "device_id", "operation"], so)
    # ------------------------------------------------ weather at the headquarters substation, UTC hours
    wx = W["wx"]
    write_csv(os.path.join(out, "hq_substation_temperature_hourly.csv"), ["time_utc", "point", "value"],
              [[t.strftime("%Y-%m-%dT%H:00Z"), "HQ-TMP-01", "%.1f" % v] for t, v in zip(wx.utc, wx.temp_c)])
    # ------------------------------------------------ daily SAIDI, two systems
    U = F[~F.planned]
    dd = (U.start // 1440).astype(int)
    served = members_served(members, seed + 11)
    legacy_served = served.copy()
    for d in range(NDAY):                                 # the retired system took the billing count once a month
        legacy_served[d] = served[(D0 + pd.Timedelta(days=d)).replace(day=1).toordinal() - D0.toordinal()]
    cmi_d = U.cmi.groupby(dd).sum().reindex(range(NDAY), fill_value=0.0).values
    ci_d = U.ci.groupby(dd).sum().reindex(range(NDAY), fill_value=0.0).values
    cut = world.GIS_DAY
    den = np.r_[legacy_served[:cut], served[cut:]]
    daily = pd.Series(cmi_d / den, index=range(NDAY))
    path = os.path.join(out, "daily_reliability_fy2021-fy2026.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        leg = pd.DataFrame({"Date": [(D0 + pd.Timedelta(days=d)).strftime("%-m/%-d/%Y") for d in range(cut)],
                            "Cust Hrs Int": np.round(cmi_d[:cut] / 60.0, 1),
                            "Cust Served": legacy_served[:cut], "SAIDI Hrs": np.round(cmi_d[:cut] / legacy_served[:cut] / 60.0, 5)})
        leg.to_excel(xw, sheet_name="Legacy OMS to Feb 2023", index=False)
        nw = pd.DataFrame({"date": [(D0 + pd.Timedelta(days=d)).date() for d in range(cut, NDAY)],
                           "saidi_min": np.round(cmi_d[cut:] / served[cut:], 4), "saifi": np.round(ci_d[cut:] / served[cut:], 6),
                           "customers_served": served[cut:]})
        nw.to_excel(xw, sheet_name="OMS daily", index=False)
    daily = pd.Series(np.r_[np.round(cmi_d[:cut] / legacy_served[:cut] / 60.0, 5) * 60.0,
                            np.round(cmi_d[cut:] / served[cut:], 4)], index=range(NDAY))
    docs.scrub_xlsx(path, "Kayla Dean", "2023-03-06T14:10:00Z", "2026-10-05T13:41:00Z", (2026, 10, 5, 8, 41, 0))
    # ------------------------------------------------ system register
    path = os.path.join(out, "system_register_2026-09-30.xlsx")
    sec_df = pd.DataFrame({"section_id": K["sid"], "feeder": [K["fname"][f] for f in S.feeder_new.values],
                           "district": [DIST[d] for d in S.district.values], "members": S.members.values,
                           "electric_heat_members": S.eheat_members.values,
                           "construction": np.where(S.urd.values, "UG", "OH"), "protective_device": K["dev"],
                           "device_type": S.device.values, "as_at": pd.Timestamp("2026-09-30").date()})
    cw = pd.DataFrame({"old_section_id": K["old"], "section_id": K["sid"], "effective": "2023-03-01"})
    nf = len(K["fname"])
    relay = {d: ("SEL-351S" if d in (0, 1) else "SEL-351A") for d in range(4)}
    fd = S.groupby("feeder").district.first()
    rc = [["CB-" + K["fname"][f], "BREAKER", K["fname"][f], "", relay[fd[f]]] for f in range(nf)]
    for s in S.index[S.device == "RCLR"]:
        rc.append([K["dev"][s], "LINE RECLOSER", K["fname"][S.feeder_new.values[s]], K["sid"][s], "Form 6"])
    rc_df = pd.DataFrame(rc, columns=["device_id", "type", "feeder", "section_id", "control"])
    rc_df["as_at"] = pd.Timestamp("2026-09-30").date()
    xf_df = pd.DataFrame({"transformer_id": K["xid"], "section_id": [K["sid"][s] for s in X.sec.values],
                          "members_served": X.members.values})
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        sec_df.to_excel(xw, sheet_name="sections", index=False)
        cw.to_excel(xw, sheet_name="gis_crosswalk", index=False)
        rc_df.to_excel(xw, sheet_name="reclosing_devices", index=False)
        xf_df.to_excel(xw, sheet_name="transformers", index=False)
    docs.scrub_xlsx(path, "GIS Services", "2023-03-02T15:00:00Z", "2026-10-01T12:20:00Z", (2026, 10, 1, 7, 20, 0))
    # ------------------------------------------------ heat pump rebates
    rb = []
    hi = X.index[np.isin(X.sec.values, S.index[S.eheat > 0.18])]
    for xf in X.index[X.rebate]:
        for k2 in range(1 + int(rng.random() < 0.3)):
            cday = int(X.conn_day.values[xf]) + (0 if k2 == 0 else int(rng.integers(5, 90)))
            if cday < NDAY:
                rb.append([cday, xf, "waived"])
    for xf in rng.choice(hi, 640, replace=False):
        cday = int(rng.integers(world.day("2023-10-01"), world.R_DAY))
        rb.append([cday, xf, "LS-%02d-%04d" % ((D0 + pd.Timedelta(days=cday)).year % 100, int(rng.integers(1, 9999)))])
    rb = [r for r in rb if r[0] < NDAY]
    rb.sort()
    acct = rng.choice(np.arange(1000000, 9999999), len(rb), replace=False)
    rr_ = np.random.default_rng(seed + 17)
    rnum = np.cumsum(1 + rr_.poisson(0.25, len(rb))) + int(rr_.integers(40, 400))
    mtr = rr_.choice(np.arange(10000000, 99999999), len(rb), replace=False)
    rbd = pd.DataFrame({"rebate_id": ["HPR-%05d" % x for x in rnum], "account": acct,
                        "meter": ["M%08d" % x for x in mtr],
                        "service_transformer": ["T-" + K["xid"][r[1]][1:] for r in rb],
                        "section_id": [K["sid"][X.sec.values[r[1]]] for r in rb],
                        "connected": [(D0 + pd.Timedelta(days=r[0])).date() for r in rb],
                        "tons": rng.choice([2.0, 2.5, 3.0, 3.5, 4.0, 5.0], len(rb), p=[0.12, 0.2, 0.3, 0.18, 0.15, 0.05]),
                        "load_study": [r[2] for r in rb]})
    path = os.path.join(out, "heat_pump_rebates_fy2024-fy2026.xlsx")
    rbd.to_excel(path, sheet_name="rebates", index=False)
    docs.scrub_xlsx(path, "Member Services", "2023-10-02T13:00:00Z", "2026-10-02T14:05:00Z", (2026, 10, 2, 9, 5, 0))
    # ------------------------------------------------ asset programme lists
    ga = G[G.list_year > 0]
    gl = pd.DataFrame({"list_year": ga.list_year.values, "structure_id": [K["gp"][i] for i in ga.site.values],
                       "section_id": [K["sid"][s] for s in ga.sec.values],
                       "fitted": [(D0 + pd.Timedelta(days=int(d))).date() if d < 10 ** 6 else None for d in ga.fit_day.values]})
    ra = Rr[Rr.list_year > 0]
    rl = pd.DataFrame({"list_year": ra.list_year.values, "riser_structure_id": [K["rp"][i] for i in ra.riser.values],
                       "section_id": [K["sid"][s] for s in ra.sec.values],
                       "replaced": [(D0 + pd.Timedelta(days=int(d))).date() if d < 10 ** 6 else None for d in ra.rep_day.values]})
    path = os.path.join(out, "asset_programme_lists_2022-2026.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        gl.sort_values(["list_year", "structure_id"]).to_excel(xw, sheet_name="animal_guards", index=False)
        rl.sort_values(["list_year", "riser_structure_id"]).to_excel(xw, sheet_name="riser_replacements", index=False)
    docs.scrub_xlsx(path, "Operations", "2022-01-03T14:00:00Z", "2026-09-28T19:30:00Z", (2026, 9, 28, 14, 30, 0))
    # ------------------------------------------------ transformer units
    U0 = W["U"]
    serial = rng.choice(np.arange(10 ** 7, 10 ** 8), len(U0) + len(W["NU"]), replace=False)
    un = [(K["xid"][x], "%s%d" % ("HE" if k % 3 else "DT", serial[i]), OLD_SUP[0] if k % 3 else OLD_SUP[1],
           (D0 + pd.Timedelta(days=int(fd_))).date()) for i, (x, fd_, k) in enumerate(zip(U0.xf, U0.fit_day, range(len(U0))))]
    serial2 = rng.choice(np.arange(10 ** 7, 10 ** 8), len(W["OU"]), replace=False)
    for j, (x, fd_) in enumerate(zip(W["OU"].xf, W["OU"].fit_day)):
        un.append((K["xid"][x], "HE%d" % serial2[j], OLD_SUP[0], (D0 + pd.Timedelta(days=int(fd_))).date()))
    for j, (x, fd_) in enumerate(zip(W["NU"].xf, W["NU"].fit_day)):
        un.append((K["xid"][x], "BP%d" % serial[len(U0) + j], NEW_SUP, (D0 + pd.Timedelta(days=int(fd_))).date()))
    un.sort(key=lambda r: (r[0], r[3]))
    tbl = pa.table({"transformer_id": [r[0] for r in un], "unit_serial": [r[1] for r in un], "supplier": [r[2] for r in un],
                    "fitted": pa.array([r[3] for r in un], pa.date32())})
    path = os.path.join(out, "transformer_units.parquet")
    pq.write_table(tbl, path, compression="snappy", store_schema=False)
    scrub_parquet(path)
    # ------------------------------------------------ crew time: restoration callouts, other callouts, scheduled overtime
    ct = crew_rows(R, EMP, E, F, rng)
    write_csv(os.path.join(out, "crew_time_overtime_fy2026.csv"),
              ["entry_id", "employee_id", "job_class", "work_order", "order_type", "pay_code", "start_time", "end_time",
               "hours", "entry_type", "entered_at", "status"], ct)
    # ------------------------------------------------ documents
    docs.policy(out)
    import ladder
    idx = []
    for fy in range(2022, 2027):
        a, b = world.day("%d-10-01" % (fy - 1)), world.day("%d-10-01" % fy)
        _, med = ladder.med_days(daily, start_hist=max(0, a - 5 * 365), end_hist=a)
        m = (U.start >= a * 1440) & (U.start < b * 1440) & ~(U.start // 1440).isin(med)
        ci_, cm_ = U.ci[m].sum(), U.cmi[m].sum()
        avg = float(served[a:b].mean())
        idx.append(["FY%d" % fy, format(int(round(avg)), ","), "%.3f" % (ci_ / avg), "%.1f" % (cm_ / avg), "%.1f" % (cm_ / ci_),
                    str(sum(1 for d in med if a <= d < b))])
    docs.review(out, idx, members)
    docs.rebate_terms(out)
    hols = [("Thanksgiving Day", "27 Nov 2025"), ("Day after Thanksgiving", "28 Nov 2025"), ("Christmas Eve", "24 Dec 2025"),
            ("Christmas Day", "25 Dec 2025"), ("New Year's Day", "1 Jan 2026"), ("Presidents' Day", "16 Feb 2026"),
            ("Memorial Day", "25 May 2026"), ("Independence Day (observed)", "3 Jul 2026"), ("Labor Day", "7 Sep 2026")]
    docs.agreement(out, asks.CLASSES, hols)
    distractors(out, W, F, K, rng)
    return dict(K=K, E=E, F=F, members=members, daily=daily)


def crew_rows(R, EMP, E, F, rng):
    wo = dict(zip(E.index, E.work_order))
    rows = []
    cap = {}
    for r in R.itertuples():
        if r.wo_type == "OUTAGE":
            w = wo.get(r.ev, "OW%d" % (5000000 + r.ev))
        else:
            if r.ev not in cap:
                cap[r.ev] = "CP%06d" % int(rng.integers(100000, 999999))
            w = cap[r.ev]
        rows.append([r.emp, r.cls, r.s, r.e, "CALLOUT", w, r.wo_type])
    busy = {}
    for r in rows:
        busy.setdefault(r[0], []).append((r[2], r[3]))
    def free(emp, s, e):
        return all(e + 300 <= a or s >= b + 300 for a, b in busy.get(emp, []))
    # after-hours callouts that restored nobody: service calls, and a transformer found overheating replaced before it failed
    y0, y1 = asks.Y2 * 1440, asks.YE * 1440
    for kind, nn, dur in (("SERVICE", 70, (50, 150)), ("CAPITAL", 26, (130, 260))):
        k = 0
        while k < nn:
            emp = EMP.sample(1, random_state=int(rng.integers(1 << 30))).iloc[0]
            d = int(rng.integers(asks.Y2, asks.YE))
            s = d * 1440 + int(rng.choice([rng.integers(0, 360), rng.integers(1020, 1380)]))
            e = s + int(rng.integers(*dur))
            if not free(emp.emp, s, e) or (e // 1440) != (s // 1440):
                continue
            w = ("SV%06d" if kind == "SERVICE" else "CP%06d") % int(rng.integers(100000, 999999))
            crew = [emp] if kind == "SERVICE" else [emp] + [x for _, x in EMP[(EMP.district == emp.district) & (EMP.emp != emp.emp)].sample(1, random_state=int(rng.integers(1 << 30))).iterrows()]
            if not all(free(c.emp, s, e) for c in crew):
                continue
            for c in crew:
                rows.append([c.emp, c.cls, s, e, "CALLOUT", w, kind])
                busy.setdefault(c.emp, []).append((s, e))
            k += 1
    # scheduled overtime: planned replacements on Saturdays
    for _ in range(140):
        emp = EMP.sample(1, random_state=int(rng.integers(1 << 30))).iloc[0]
        d = int(rng.integers(asks.Y2, asks.YE))
        while (D0 + pd.Timedelta(days=d)).dayofweek != 5:
            d += 1
        s = d * 1440 + 420 + int(rng.integers(0, 60)); e = s + int(rng.integers(180, 420))
        if not free(emp.emp, s, e) or e >= y1:
            continue
        rows.append([emp.emp, emp.cls, s, e, "OT-SCHED", "CP%06d" % int(rng.integers(100000, 999999)), "CAPITAL"])
        busy.setdefault(emp.emp, []).append((s, e))
    out = []
    ids = world.uuid4s(rng, len(rows) * 2)
    k = 0
    for r in sorted(rows, key=lambda x: (x[2], x[0])):
        emp, cls, s, e, pc, w, ot = r
        # the foreman enters the crew's time each Monday for the week before
        dd = int(e // 1440)
        wd = (D0 + pd.Timedelta(days=dd)).dayofweek
        entered = (dd + (7 - wd)) * 1440 + int(rng.integers(420, 690))
        fix = rng.random() < 0.035
        if fix:     # an entry later corrected: the first entry had the wrong end
            e0 = e + int(rng.choice([-1, 1]) * rng.integers(10, 35))
            out.append(_crow(ids[k], emp, cls, s, e0, pc, w, ot, "ORIGINAL", entered, "APPROVED")); k += 1
            out.append(_crow(ids[k], emp, cls, s, e, pc, w, ot, "CORRECTION", entered + int(rng.integers(600, 4000)), "APPROVED")); k += 1
        else:
            out.append(_crow(ids[k], emp, cls, s, e, pc, w, ot, "ORIGINAL", entered, "APPROVED")); k += 1
        if rng.random() < 0.012:   # keyed twice; the foreman rejected the second
            out.append(_crow(ids[k], emp, cls, s, e, pc, w, ot, "ORIGINAL", entered + int(rng.integers(2, 40)), "REJECTED")); k += 1
    return out


def _crow(i, emp, cls, s, e, pc, w, ot, et, entered, status):
    a, b = lt_str([s])[0], lt_str([e])[0]
    return [i, emp, cls, w, ot, pc, a[11:16], b[11:16], "%.2f" % ((e - s) / 60.0), et, lt_str([entered])[0], status]


def distractors(out, W, F, K, rng):
    # member outage calls to the IVR, fiscal 2026 (the call centre's own log, UTC)
    fy = F[(F.start >= asks.Y2 * 1440) & (F.start < asks.YE * 1440) & ~F.planned]
    calls = []
    S = W["S"]
    for r in fy.itertuples():
        n = rng.binomial(int(r.ci), 0.11 if r.level == "section" else 0.35)
        for _ in range(n):
            t = r.start + rng.exponential(18)
            calls.append((t, int(rng.integers(1000000, 9999999)), DIST[S.district.values[int(r.sec)]],
                          rng.choice(["OUTAGE", "OUTAGE", "OUTAGE", "FLICKER", "WIRE DOWN"], p=[0.5, 0.2, 0.15, 0.1, 0.05])))
    for _ in range(4000):
        t = rng.uniform(asks.Y2 * 1440, asks.YE * 1440)
        calls.append((t, int(rng.integers(1000000, 9999999)), DIST[int(rng.integers(0, 4))], rng.choice(["BILLING", "FLICKER", "OUTAGE"], p=[0.6, 0.25, 0.15])))
    calls.sort()
    tu = asks.utc([c[0] for c in calls])
    ids = world.uuid4s(rng, len(calls))
    write_csv(os.path.join(out, "ivr_calls_fy2026.csv"), ["call_id", "received_utc", "account", "district", "menu_choice"],
              [[i, t.strftime("%Y-%m-%dT%H:%M:%SZ"), c[1], c[2], c[3]] for i, t, c in zip(ids, tu, calls)])
    # wholesale power bills from the generation and transmission cooperative, by month
    mo = pd.period_range("2021-10", "2026-09", freq="M")
    dm = W["dm"]
    rows = []
    for p in mo:
        d0 = (p.start_time - D0).days; d1 = (p.end_time.normalize() - D0).days + 1
        t = dm[d0:d1].mean()
        kwh = 128e6 * (1 + 0.012 * (p.year - 2022)) * (1 + 0.018 * max(10 - t, 0)) * rng.normal(1, 0.02)
        kw = kwh / (24 * len(range(d0, d1))) * (1.55 + 0.01 * max(-t, 0)) * rng.normal(1, 0.015)
        rows.append([str(p), round(kwh), round(kw), round(kwh * 0.0512, 2), round(kw * 14.85, 2)])
    path = os.path.join(out, "wholesale_power_bills_fy2022-fy2026.xlsx")
    pd.DataFrame(rows, columns=["billing_month", "energy_kwh", "coincident_peak_kw", "energy_charge_usd", "demand_charge_usd"]).to_excel(path, sheet_name="bills", index=False)
    docs.scrub_xlsx(path, "Finance", "2021-11-08T15:00:00Z", "2026-10-09T13:00:00Z", (2026, 10, 9, 8, 0, 0))
