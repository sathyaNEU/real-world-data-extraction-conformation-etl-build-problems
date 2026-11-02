"""Operating records of the Kessock Lake world: the laboratory stream, the mill, the gold room and refinery, the haul
fleet and its dispatch loads, the mill DCS and the maintenance system. Clean truth only; pack.py renders it."""
import math
import datetime as dt
import numpy as np
import pandas as pd

import params as P
from world import _rng, month_start


# ---------------------------------------------------------------------------------------------------------------
# Clocks: the mine runs on Eastern time (America/Toronto)
# ---------------------------------------------------------------------------------------------------------------

def _dst_bounds(y):
    mar = dt.datetime(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.datetime(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return mar.replace(hour=2), nov.replace(hour=2)


def local_offset(loc):
    a, b = _dst_bounds(loc.year)
    return -4 if a <= loc < b else -5


def local_to_utc(loc):
    return loc - dt.timedelta(hours=local_offset(loc))


def utc_to_local(u):
    loc = u - dt.timedelta(hours=5)
    if local_offset(loc) == -4:
        loc = u - dt.timedelta(hours=4)
    return loc


# ---------------------------------------------------------------------------------------------------------------
# The laboratory stream
# ---------------------------------------------------------------------------------------------------------------

CRMS = [  # certificate, certified Au g/t, 1 SD, legacy site code
    ("KGR-0461", 0.461, 0.019, "STD-L"),
    ("KGR-1587", 1.587, 0.052, "STD-M"),
    ("KGR-4120", 4.120, 0.118, "STD-H"),
]


def lab_stream(hd):
    """Holes interleaved with CRMs, blanks and field duplicates in drilling order, batched by 40 and dated."""
    rng = _rng("lab")
    rows = []
    nc, nb, nd = 0, 0, 0
    gap_c, gap_b, gap_d = 24, 50, 30
    for idx, h in hd.iterrows():
        rows.append(dict(kind="BH", hole=idx, au=h["au"], drilled=h["drilled"], bench=h["bench"],
                         mx=h["mx"], my=h["my"], crm=""))
        nc, nb, nd = nc + 1, nb + 1, nd + 1
        if nd >= gap_d:
            rows.append(dict(kind="FD", hole=idx, au=h["au"] * math.exp(rng.normal(0, 0.22) - 0.0242),
                             drilled=h["drilled"], bench=h["bench"], mx=h["mx"], my=h["my"], crm=""))
            nd, gap_d = 0, int(rng.integers(26, 36))
        if nc >= gap_c:
            c = CRMS[int(rng.integers(0, len(CRMS)))]
            rows.append(dict(kind="CRM", hole=-1, au=c[1] * (1 + rng.normal(0.004, c[2] / c[1])),
                             drilled=h["drilled"], bench=None, mx=None, my=None, crm=c[0]))
            nc, gap_c = 0, int(rng.integers(20, 30))
        if nb >= gap_b:
            rows.append(dict(kind="BLK", hole=-1, au=abs(rng.normal(0.0026, 0.0019)), drilled=h["drilled"],
                             bench=None, mx=None, my=None, crm=""))
            nb, gap_b = 0, int(rng.integers(44, 56))
    lab = pd.DataFrame(rows)
    lab["batch"] = np.arange(len(lab)) // 40
    last = lab.groupby("batch")["drilled"].max()
    rec = {b: d + dt.timedelta(days=int(rng.integers(1, 3))) for b, d in last.items()}
    rep = {b: rec[b] + dt.timedelta(days=int(rng.integers(1, 3))) for b in rec}
    lab["received"] = lab["batch"].map(rec)
    lab["reported"] = lab["batch"].map(rep)
    return lab


# ---------------------------------------------------------------------------------------------------------------
# The ball mill's stops, the mill's feed and daily records
# ---------------------------------------------------------------------------------------------------------------

OUTAGE_SHUTDOWNS = [(2025, 3), (2025, 8), (2025, 11), (2026, 3)]   # the planned shutdowns the historian missed
TAG_SWITCH_UTC = dt.datetime(2026, 5, 12, 14, 0)


def ball_mill_stops():
    """Every ball mill stop, local time, 2023-01-01 to 2026-10-31, and the historian outages around four shutdowns."""
    rng = _rng("bmstops")
    planned = []
    for n in range(46):
        m = month_start(n)
        d = dt.datetime(m.year, m.month, 9) + dt.timedelta(days=int(rng.integers(0, 12)))
        while d.weekday() != 1:
            d += dt.timedelta(days=1)
        start = d.replace(hour=6) + dt.timedelta(minutes=int(rng.integers(0, 95)))
        reline = m.month in (2, 8)
        hours = rng.uniform(52, 64) if reline else rng.uniform(13, 31)
        end = (start + dt.timedelta(hours=float(hours))).replace(second=0, microsecond=0)
        planned.append(dict(start=start, end=end, kind="RELINE" if reline else "SHUTDOWN"))
    pl = pd.DataFrame(planned)
    # historian outages: each opens some hours before one planned shutdown and closes some hours after it
    outages = []
    for (y, mo) in OUTAGE_SHUTDOWNS:
        r = pl[(pl["start"].dt.year == y) & (pl["start"].dt.month == mo)].iloc[0]
        a = local_to_utc(r["start"].to_pydatetime()) - dt.timedelta(minutes=int(rng.integers(300, 1700)))
        b = local_to_utc(r["end"].to_pydatetime()) + dt.timedelta(minutes=int(rng.integers(240, 1300)))
        outages.append((a.replace(second=0), b.replace(second=0)))
    trips = []
    t = dt.datetime(2023, 1, 1) + dt.timedelta(hours=float(rng.exponential(160)))
    while t < dt.datetime(2026, 11, 1):
        dur = float(np.exp(rng.normal(math.log(1.25), 0.85)))
        trips.append(dict(start=t.replace(second=0, microsecond=0),
                          end=(t + dt.timedelta(hours=dur)).replace(second=0, microsecond=0), kind="TRIP"))
        t += dt.timedelta(hours=float(rng.exponential(160)) + dur)
    tr = pd.DataFrame(trips)
    s = pd.concat([pl, tr]).sort_values("start").reset_index(drop=True)
    keep, last_end = [], dt.datetime(2022, 12, 31)
    for _, r in s.iterrows():
        a, b = r["start"].to_pydatetime(), r["end"].to_pydatetime()
        if a <= last_end + dt.timedelta(minutes=20):
            if r["kind"] == "TRIP":
                continue
        if r["kind"] == "TRIP" and any(o[0] - dt.timedelta(hours=6) <= local_to_utc(a) <= o[1] + dt.timedelta(hours=6)
                                       for o in outages):
            continue          # no trip falls inside a historian outage
        if b <= a:
            continue
        keep.append(dict(start=a, end=b, kind=r["kind"]))
        last_end = max(last_end, b)
    st = pd.DataFrame(keep).sort_values("start").reset_index(drop=True)
    # guard overlaps once more
    st = st[st["start"] >= st["end"].shift(1).fillna(dt.datetime(2022, 1, 1))].reset_index(drop=True)
    # a breakdown runs on a little longer where a quarter's running time would sit on a half hour
    for _ in range(6):
        moved = False
        for a, b in QUARTERS:
            h = run_hours(st, a, b)
            if 0.30 <= h % 1.0 <= 0.70:
                cand = st[(st["kind"] == "TRIP") & (st["start"] > a + dt.timedelta(days=3)) &
                          (st["end"] < b - dt.timedelta(days=3))]
                if not len(cand):
                    continue
                i = cand.index[-1]
                nxt = st["start"].iloc[i + 1] if i + 1 < len(st) else b
                if st.loc[i, "end"] + dt.timedelta(minutes=50) < nxt:
                    st.loc[i, "end"] = st.loc[i, "end"] + dt.timedelta(minutes=24)
                    moved = True
        if not moved:
            break
    return st, outages


QUARTERS = [(dt.datetime(2025, 1, 1), dt.datetime(2025, 4, 1)), (dt.datetime(2025, 4, 1), dt.datetime(2025, 7, 1)),
            (dt.datetime(2025, 7, 1), dt.datetime(2025, 10, 1)), (dt.datetime(2025, 10, 1), dt.datetime(2026, 1, 1)),
            (dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1)), (dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1)),
            (dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1))]


def run_hours(stops, a, b):
    """Hours the ball mill ran between two local times."""
    down = 0.0
    for _, r in stops[(stops["end"] > a) & (stops["start"] < b)].iterrows():
        down += (min(b, r["end"]) - max(a, r["start"])).total_seconds() / 3600.0
    return (b - a).total_seconds() / 3600.0 - down


def mill_months(blocks_hist, gc_by_block):
    """Monthly feed: this month's grade-control ore and a share of last month's off the ROM pad."""
    b = blocks_hist.copy()
    b["gc"] = b["ijk"].map(gc_by_block)
    b = b[b["gc"] >= P.OLD_ORE_CUT]
    rng = _rng("millmonth")
    out = []
    carry_t, carry_au = 0.0, 0.0
    for mi in range(P.HIST_MONTHS):
        mb = b[b["month_idx"] == mi]
        t, au = mb["tonnes"].sum(), (mb["tonnes"] * mb["gc"]).sum()
        lag = 0.12 + 0.06 * rng.random()
        feed_t, feed_au = (1 - lag) * t + carry_t, (1 - lag) * au + carry_au
        carry_t, carry_au = lag * t, lag * au
        out.append(dict(month_idx=mi, dry_t=feed_t, head=feed_au / feed_t * (1.0 + rng.normal(-0.004, 0.018))))
    return pd.DataFrame(out)


def mill_daily(mm, stops):
    """Mill days (06:00 to 06:00 local): wet tonnes, moisture, head and tails grade."""
    rng = _rng("milldaily")
    rows = []
    d = dt.date(2023, 1, 1)
    while d < dt.date(2026, 11, 1):
        a = dt.datetime(d.year, d.month, d.day, 6)
        rows.append(dict(day=d, run_h=run_hours(stops, a, a + dt.timedelta(days=1))))
        d += dt.timedelta(days=1)
    rh = pd.DataFrame(rows)
    rh["month_idx"] = [(x.year - 2023) * 12 + x.month - 1 for x in rh["day"]]
    out = []
    for mi, g in rh.groupby("month_idx"):
        row = mm[mm["month_idx"] == mi].iloc[0]
        w = np.clip(g["run_h"].values * (1 + rng.normal(0, 0.035, len(g))), 0, None)
        dry = row["dry_t"] * w / w.sum()
        hf = np.exp(rng.normal(0, 0.07, len(g)))
        head = row["head"] * hf / (np.sum(dry * hf) / dry.sum())
        moist = np.round(rng.uniform(3.2, 5.6, len(g)), 1)
        tails = np.clip(rng.normal(0.074, 0.009, len(g)), 0.04, None)
        for (day, rhv), dtt, mo, h, tl in zip(g[["day", "run_h"]].values, dry, moist, head, tails):
            out.append(dict(day=day, run_h=rhv, dry_t=dtt, wet_t=dtt / (1 - mo / 100.0), moist=mo, head=h, tails=tl))
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------------------------------------------
# The gold room and the refinery
# ---------------------------------------------------------------------------------------------------------------

def gold_room(md):
    """Bars poured 2025-01-01 to 2026-10-31, a clean-up bar at each month end; shipments every 6 to 9 days; refinery
    melt lots (a bar under 300 oz gross is melted with the next bar on its manifest); receipt and settlement."""
    rng = _rng("goldroom")
    d = md[md["day"] >= dt.date(2024, 12, 27)].reset_index(drop=True).copy()
    d["rec"] = d["dry_t"] * np.maximum(d["head"] - d["tails"], 0) / P.TROY
    bars, acc, pend, seq = [], 0.0, 0, {}
    days = list(d["day"])
    for i, r in d.iterrows():
        acc += r["rec"] * (1 + rng.normal(0, 0.03))
        pend += 1
        day = r["day"]
        month_end = i + 1 < len(d) and days[i + 1].month != day.month
        pour = month_end or (pend >= int(rng.integers(2, 4)) and acc > 1400)
        if not pour:
            continue
        fine_total, acc, pend = acc, 0.0, 0
        if day < dt.date(2025, 1, 1):
            continue
        pieces = [("REG", fine_total)]
        if month_end:
            cl = float(rng.uniform(70, 185))
            pieces = [("REG", fine_total - cl), ("CLN", cl)] if fine_total - cl > 250 else [("CLN", fine_total)]
        for kind, fine in pieces:
            fness = float(rng.uniform(0.835, 0.905)) if kind == "REG" else float(rng.uniform(0.58, 0.74))
            seq[day.year] = seq.get(day.year, 0) + 1
            hour = int(rng.integers(8, 16)) if kind == "REG" else int(rng.integers(16, 20))
            bars.append(dict(year=day.year, seq=seq[day.year], pour_day=day,
                             pour_time=dt.time(hour, int(rng.integers(0, 60))), kind=kind, fine=fine,
                             fineness=fness, gross=fine / fness))
    b = pd.DataFrame(bars)
    b["ship"] = -1
    ships, no = [], 0
    sd = dt.date(2025, 1, 6)
    while sd <= dt.date(2026, 11, 4):
        idx = b.index[(b["pour_day"] < sd) & (b["ship"] < 0)]
        if len(idx):
            no += 1
            b.loc[idx, "ship"] = no
            ships.append(dict(ship=no, date=sd))
        sd += dt.timedelta(days=int(rng.integers(6, 10)))
    b = b[b["ship"] > 0].reset_index(drop=True)
    sh = pd.DataFrame(ships)
    b["lot"] = -1
    lot = 0
    for s_, g in b.groupby("ship"):
        ids = list(g.sort_values(["pour_day", "pour_time"]).index)
        k = 0
        while k < len(ids):
            lot += 1
            mem = [ids[k]]
            if b.loc[ids[k], "gross"] < 300 and k + 1 < len(ids):
                mem.append(ids[k + 1])
            elif b.loc[ids[k], "gross"] < 300 and k > 0 and len(ids) > 1:
                prev = b.loc[ids[k - 1], "lot"]          # last on the manifest: melted with the bar before it
                b.loc[ids[k], "lot"] = prev
                lot -= 1
                k += 1
                continue
            for m_ in mem:
                b.loc[m_, "lot"] = lot
            k += len(mem)
    # a quarter whose poured fine gold would sit on a 50-ounce line takes its largest single-bar lot a little heavier
    for _ in range(8):
        alloc = quarter_fine(b)
        hit = [q for q, v in alloc.items() if 38 <= v % 100 <= 62]
        if not hit:
            break
        for q in hit:
            a, z = QUARTERS[q]
            solo = b.groupby("lot")["lot"].transform("size") == 1
            c = b[solo & (b["kind"] == "REG") & (b["pour_day"] >= a.date()) & (b["pour_day"] < z.date())]
            i = c["fine"].idxmax()
            b.loc[i, "fine"] += 26.0
            b.loc[i, "gross"] = b.loc[i, "fine"] / b.loc[i, "fineness"]
    ship_date = dict(zip(sh["ship"], sh["date"]))
    rec_day = {s_: ship_date[s_] + dt.timedelta(days=int(rng.integers(3, 6))) for s_ in ship_date}
    lots = []
    for lt, g in b.groupby("lot"):
        s_ = int(g["ship"].iloc[0])
        received = rec_day[s_]
        settled = received + dt.timedelta(days=int(rng.integers(7, 15)))
        gross_rec = g["gross"].sum() * (1 - float(rng.uniform(0.0004, 0.0016)))
        fine = g["fine"].sum()
        lots.append(dict(lot=lt, ship=s_, received=received, settled=settled, gross_rec=gross_rec,
                         fineness=fine / gross_rec, fine=fine, ag=gross_rec * float(rng.uniform(0.07, 0.12))))
    return b, sh, pd.DataFrame(lots)


def quarter_fine(b):
    """Each quarter's poured fine gold: a lot's fine gold shared among its bars by their gross weights, by pour day."""
    lot_fine = b.groupby("lot")["fine"].transform("sum")
    lot_gross = b.groupby("lot")["gross"].transform("sum")
    alloc = lot_fine * b["gross"] / lot_gross
    out = {}
    for q, (a, z) in enumerate(QUARTERS):
        sel = (b["pour_day"] >= a.date()) & (b["pour_day"] < z.date())
        out[q] = float(alloc[sel].sum())
    return out


# ---------------------------------------------------------------------------------------------------------------
# The haul fleet and the low-grade stockpile loads
# ---------------------------------------------------------------------------------------------------------------

FLEET0 = [("T-%02d" % i, "CAT 777G", 90.7) for i in range(1, 13)]
REISSUE = [("T-04", dt.date(2024, 5, 6), dt.date(2024, 5, 21)),
           ("T-09", dt.date(2024, 8, 2), dt.date(2024, 8, 19))]
ADDED = [("T-13", dt.date(2025, 2, 10)), ("T-14", dt.date(2025, 2, 24))]
NEW_MODEL, NEW_PAYLOAD = "CAT 785D", 136.1


def fleet_on(day):
    out = []
    for no, model, pay in FLEET0:
        re = [r for r in REISSUE if r[0] == no]
        if re:
            if day < re[0][1]:
                out.append((no, model, pay))
            elif day >= re[0][2]:
                out.append((no, NEW_MODEL, NEW_PAYLOAD))
        else:
            out.append((no, model, pay))
    for no, d in ADDED:
        if day >= d:
            out.append((no, NEW_MODEL, NEW_PAYLOAD))
    return out


def lg_loads(blocks_hist, gc_by_block):
    """Every haul of low-grade material (0.30 to 0.50 g/t on grade control) to the low-grade stockpile."""
    rng = _rng("dispatch")
    b = blocks_hist.copy()
    b["gc"] = b["ijk"].map(gc_by_block)
    b = b[(b["gc"] >= P.LG_LOW_CUT) & (b["gc"] < P.OLD_ORE_CUT)].sort_values(["mined", "ijk"])
    rows, free = [], {}
    for _, blk in b.iterrows():
        day = blk["mined"]
        trucks = fleet_on(day)
        remaining = blk["tonnes"]
        t = dt.datetime(day.year, day.month, day.day, 7 if rng.random() < 0.55 else 19) + \
            dt.timedelta(minutes=float(rng.uniform(20, 300)))
        shovel = "EX-%02d" % int(rng.choice([1, 2, 3], p=[0.45, 0.4, 0.15]))
        poly = "%d-%03d-%02d" % (blk["bench"], blk["i"], blk["j"])
        while remaining > 30:
            no, model, pay = trucks[int(rng.integers(0, len(trucks)))]
            if free.get(no) is not None and free[no] > t:
                t = free[no]
            rows.append(dict(time_local=t.replace(microsecond=0), truck=no, payload=pay, model=model, poly=poly,
                             shovel=shovel, grade=round(float(blk["gc"]), 2), block=int(blk["ijk"])))
            free[no] = t + dt.timedelta(minutes=float(rng.uniform(22, 38)))
            remaining -= pay
            t += dt.timedelta(minutes=float(rng.uniform(2.5, 6.0)))
    return pd.DataFrame(rows).sort_values(["time_local", "truck"]).reset_index(drop=True)
