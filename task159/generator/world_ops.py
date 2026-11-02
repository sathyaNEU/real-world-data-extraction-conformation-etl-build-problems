"""Operating records of the Kessock Lake world: the laboratory stream, the mill, the gold room and refinery, the haul
fleet and its dispatch loads, the mill DCS and the maintenance system. Clean truth only; pack.py renders it."""
import math
import datetime as dt
import numpy as np
import pandas as pd

import params as P
from world import _rng, month_start

UTC = dt.timezone.utc


def toronto_offset(t):
    """UTC offset of America/Toronto at a naive local time (DST from the second Sunday of March 02:00 to the first
    Sunday of November 02:00)."""
    y = t.year
    mar = dt.datetime(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.datetime(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    start, end = mar.replace(hour=2), nov.replace(hour=2)
    return -4 if start <= t < end else -5


def local_to_utc(t):
    return t - dt.timedelta(hours=toronto_offset(t))


def utc_to_local(t):
    loc = t + dt.timedelta(hours=-5)
    off = toronto_offset(loc + dt.timedelta(hours=1)) if False else None
    # iterate once: offset at the local time
    loc = t + dt.timedelta(hours=toronto_offset(t + dt.timedelta(hours=-5)))
    return loc


# ---------------------------------------------------------------------------------------------------------------
# The laboratory stream: blast holes plus quality-control insertions, batched and reported
# ---------------------------------------------------------------------------------------------------------------

CRMS = [  # certificate, certified Au g/t, 1 SD, legacy site code
    ("KGR-0461", 0.461, 0.019, "STD-L"),
    ("KGR-1587", 1.587, 0.052, "STD-M"),
    ("KGR-4120", 4.120, 0.118, "STD-H"),
]


def lab_stream(hd):
    """Interleave the holes with CRMs, blanks and field duplicates in drilling order, cut batches of 40, date them."""
    rng = _rng("lab")
    rows = []
    n_since_crm, n_since_blk, n_since_dup = 0, 0, 0
    for idx, h in hd.iterrows():
        rows.append(dict(kind="BH", hole=idx, au=h["au"], drilled=h["drilled"], bench=h["bench"],
                         mx=h["mx"], my=h["my"]))
        n_since_crm += 1
        n_since_blk += 1
        n_since_dup += 1
        if n_since_dup >= int(rng.integers(26, 36)):
            rows.append(dict(kind="FD", hole=idx, au=h["au"] * math.exp(rng.normal(0, 0.22) - 0.022 / 2),
                             drilled=h["drilled"], bench=h["bench"], mx=h["mx"], my=h["my"]))
            n_since_dup = 0
        if n_since_crm >= int(rng.integers(20, 30)):
            c = CRMS[int(rng.integers(0, len(CRMS)))]
            rows.append(dict(kind="CRM", hole=-1, au=c[1] * (1 + rng.normal(0.004, c[2] / c[1])), crm=c[0],
                             drilled=h["drilled"], bench=None, mx=None, my=None))
            n_since_crm = 0
        if n_since_blk >= int(rng.integers(44, 56)):
            rows.append(dict(kind="BLK", hole=-1, au=abs(rng.normal(0.0025, 0.0018)), drilled=h["drilled"],
                             bench=None, mx=None, my=None))
            n_since_blk = 0
    lab = pd.DataFrame(rows)
    lab["batch"] = np.arange(len(lab)) // 40
    # receipt and reporting dates per batch
    first = lab.groupby("batch")["drilled"].max()
    rec = {b: d + dt.timedelta(days=int(rng.integers(1, 3))) for b, d in first.items()}
    rep = {b: rec[b] + dt.timedelta(days=int(rng.integers(1, 3))) for b in rec}
    lab["received"] = lab["batch"].map(rec)
    lab["reported"] = lab["batch"].map(rep)
    return lab


# ---------------------------------------------------------------------------------------------------------------
# The mill: monthly feed from grade control's ore, spread over days by the ball mill's running hours
# ---------------------------------------------------------------------------------------------------------------

def mill_months(blocks_hist, gc_by_block):
    """Monthly feed: this month's grade-control ore plus a share of last month's off the ROM pad."""
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
        feed_t = (1 - lag) * t + carry_t
        feed_au = (1 - lag) * au + carry_au
        carry_t, carry_au = lag * t, lag * au
        bias = 1.0 + rng.normal(-0.004, 0.018)
        out.append(dict(month_idx=mi, dry_t=feed_t, head=feed_au / feed_t * bias))
    return pd.DataFrame(out)


def ball_mill_timeline():
    """Ball mill stops 2023-01-01 to 2026-10-31, local time: trips, monthly planned shutdowns and relines."""
    rng = _rng("bmstops")
    stops = []
    t0, t1 = dt.datetime(2023, 1, 1), dt.datetime(2026, 11, 1)
    # planned shutdowns: one a month on a Tuesday, two relines a year
    m = dt.date(2023, 1, 1)
    while m < t1.date():
        d = dt.datetime(m.year, m.month, 9) + dt.timedelta(days=int(rng.integers(0, 12)))
        while d.weekday() != 1:
            d += dt.timedelta(days=1)
        start = d.replace(hour=6) + dt.timedelta(minutes=int(rng.integers(0, 90)))
        reline = m.month in (2, 8)
        hours = rng.uniform(52, 64) if reline else rng.uniform(13, 30)
        stops.append(dict(start=start, end=start + dt.timedelta(hours=float(hours)),
                          kind="RELINE" if reline else "PLANNED"))
        m = month_start((m.year - 2023) * 12 + m.month)
    # trips
    t = t0 + dt.timedelta(hours=float(rng.exponential(170)))
    while t < t1:
        dur = float(np.exp(rng.normal(math.log(1.3), 0.85)))
        stops.append(dict(start=t, end=t + dt.timedelta(hours=dur), kind="TRIP"))
        t += dt.timedelta(hours=float(rng.exponential(170)) + dur)
    s = pd.DataFrame(stops).sort_values("start").reset_index(drop=True)
    # drop overlaps (a trip inside a shutdown never happens)
    keep, last_end = [], t0
    for _, r in s.iterrows():
        if r["start"] <= last_end:
            continue
        keep.append(r)
        last_end = r["end"]
    s = pd.DataFrame(keep).reset_index(drop=True)
    for c in ("start", "end"):
        s[c] = s[c].dt.floor("min") if hasattr(s[c], "dt") else s[c]
    return s


def run_hours_by_day(stops, d0, d1, day_start_hour=0):
    """Hours the mill ran on each day (a day starting at day_start_hour local)."""
    days = []
    d = d0
    while d < d1:
        a = dt.datetime(d.year, d.month, d.day, day_start_hour)
        b = a + dt.timedelta(days=1)
        down = 0.0
        for _, r in stops[(stops["end"] > a) & (stops["start"] < b)].iterrows():
            down += (min(b, r["end"]) - max(a, r["start"])).total_seconds() / 3600.0
        days.append((d, 24.0 - down))
        d += dt.timedelta(days=1)
    return pd.DataFrame(days, columns=["day", "run_h"])


def mill_daily(mm, stops):
    """Daily mill records over mill days (06:00 to 06:00): wet tonnes, moisture, head and tails grade."""
    rng = _rng("milldaily")
    rh = run_hours_by_day(stops, dt.date(2023, 1, 1), dt.date(2026, 11, 1), day_start_hour=6)
    rh["month_idx"] = [(d.year - 2023) * 12 + d.month - 1 for d in rh["day"]]
    out = []
    for mi, g in rh.groupby("month_idx"):
        row = mm[mm["month_idx"] == mi].iloc[0]
        w = g["run_h"].values * (1 + rng.normal(0, 0.035, len(g)))
        w = np.clip(w, 0, None)
        dry = row["dry_t"] * w / w.sum()
        hd = np.exp(rng.normal(0, 0.07, len(g)))
        hd = row["head"] * hd / (np.sum(dry * hd) / dry.sum())
        moist = np.round(rng.uniform(3.2, 5.6, len(g)), 1)
        wet = dry / (1 - moist / 100.0)
        tails = np.clip(rng.normal(0.074, 0.009, len(g)), 0.04, None)
        for (d, rhv), dt_, wt, mo, h, tl in zip(g[["day", "run_h"]].values, dry, wet, moist, hd, tails):
            out.append(dict(day=d, run_h=rhv, dry_t=dt_, wet_t=wt, moist=mo, head=h, tails=tl))
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------------------------------------------
# The gold room and the refinery
# ---------------------------------------------------------------------------------------------------------------

def gold_room(md):
    """Bars poured 2025-01-01 to 2026-10-31 from the mill's recovered gold, with month-end clean-up bars; shipments,
    refinery lots (bars under 300 oz melted with the next bar on the manifest) and settlement dates."""
    rng = _rng("goldroom")
    md = md.copy()
    md["rec_oz"] = md["dry_t"] * np.maximum(md["head"] - md["tails"], 0) / P.TROY
    md = md[(md["day"] >= dt.date(2024, 12, 29))].reset_index(drop=True)
    bars = []
    acc = 0.0
    year_seq = {}
    pending_days = 0
    for i, r in md.iterrows():
        acc += r["rec_oz"] * (1 + rng.normal(0, 0.03))
        pending_days += 1
        d = r["day"]
        nxt = md["day"].iloc[i + 1] if i + 1 < len(md) else None
        month_end = nxt is not None and nxt.month != d.month
        pour = (pending_days >= int(rng.integers(2, 4)) and acc > 1500) or month_end
        if not pour or d < dt.date(2025, 1, 1):
            if d < dt.date(2025, 1, 1) and pour:
                acc = 0.0
                pending_days = 0
            continue
        fine_total = acc
        acc = 0.0
        pending_days = 0
        pieces = []
        if month_end:
            clean = float(rng.uniform(70, 190))           # fine oz in the clean-up bar
            main = fine_total - clean
            if main > 300:
                pieces.append(("REG", main))
            pieces.append(("CLN", clean))
        else:
            pieces.append(("REG", fine_total))
        for kind, fine in pieces:
            fness = rng.uniform(0.835, 0.905) if kind == "REG" else rng.uniform(0.58, 0.74)
            y = d.year
            year_seq[y] = year_seq.get(y, 0) + 1
            hour = int(rng.integers(8, 18)) if kind == "REG" else int(rng.integers(13, 19))
            bars.append(dict(year=y, seq=year_seq[y], pour_day=d, pour_time=dt.time(hour, int(rng.integers(0, 60))),
                             kind=kind, fine=fine, fineness=fness, gross=fine / fness))
    b = pd.DataFrame(bars)
    # shipments every 6 to 9 days, every bar poured since the last
    b["ship"] = -1
    ship_no, last_ship = 0, dt.date(2025, 1, 1)
    ships = []
    d = dt.date(2025, 1, 6)
    while d <= dt.date(2026, 11, 3):
        idx = b.index[(b["pour_day"] < d) & (b["ship"] < 0)]
        if len(idx):
            ship_no += 1
            b.loc[idx, "ship"] = ship_no
            ships.append(dict(ship=ship_no, date=d))
        d += dt.timedelta(days=int(rng.integers(6, 10)))
    b = b[b["ship"] > 0].reset_index(drop=True)
    sh = pd.DataFrame(ships).set_index("ship")
    # refinery lots: bars under 300 oz gross melted with the next bar on the same manifest
    lots, lot_no = [], 0
    b["lot"] = -1
    for s, g in b.groupby("ship"):
        ids = list(g.sort_values(["pour_day", "pour_time"]).index)
        k = 0
        while k < len(ids):
            lot_no += 1
            members = [ids[k]]
            if b.loc[ids[k], "gross"] < 300 and k + 1 < len(ids):
                members.append(ids[k + 1])
                k += 2
            elif b.loc[ids[k], "gross"] < 300 and k > 0 and False:
                k += 1
            else:
                k += 1
            for m_ in members:
                b.loc[m_, "lot"] = lot_no
    # a clean-up bar that is the last on its manifest melts alone (small lot)
    rec_days = {s: sh.loc[s, "date"] + dt.timedelta(days=int(rng.integers(3, 6))) for s in sh.index}
    lot_rows = []
    for lot, g in b.groupby("lot"):
        s = int(g["ship"].iloc[0])
        received = rec_days[s]
        settled = received + dt.timedelta(days=int(rng.integers(7, 15)))
        gross_rec = g["gross"].sum() * (1 - rng.uniform(0.0004, 0.0016))       # refinery's received weight
        fine = g["fine"].sum()
        lot_rows.append(dict(lot=lot, ship=s, received=received, settled=settled, gross_rec=gross_rec,
                             fineness=fine / gross_rec, fine=fine, ag=gross_rec * rng.uniform(0.07, 0.12)))
    lt = pd.DataFrame(lot_rows)
    return b, sh.reset_index(), lt


# ---------------------------------------------------------------------------------------------------------------
# The haul fleet and the low-grade stockpile loads
# ---------------------------------------------------------------------------------------------------------------

FLEET0 = [("T-%02d" % i, "CAT 777G", 90.7) for i in range(1, 13)]
REISSUE = [  # number, old disposal date, new unit in service
    ("T-04", dt.date(2024, 5, 6), dt.date(2024, 5, 21)),
    ("T-09", dt.date(2024, 8, 2), dt.date(2024, 8, 19)),
]
ADDED = [("T-13", dt.date(2025, 2, 10)), ("T-14", dt.date(2025, 2, 24))]
NEW_MODEL, NEW_PAYLOAD = "CAT 785D", 136.1


def fleet_on(day):
    """Trucks in service on a day: (number, model, nominal payload)."""
    out = []
    for no, model, pay in FLEET0:
        re = [r for r in REISSUE if r[0] == no]
        if re:
            disp, new = re[0][1], re[0][2]
            if day < disp:
                out.append((no, model, pay))
            elif day >= new:
                out.append((no, NEW_MODEL, NEW_PAYLOAD))
        else:
            out.append((no, model, pay))
    for no, d in ADDED:
        if day >= d:
            out.append((no, NEW_MODEL, NEW_PAYLOAD))
    return out


def lg_loads(blocks_hist, gc_by_block):
    """Every haul of low-grade material (0.30 to 0.50 g/t on grade control) to the low-grade stockpile, with the
    dispatch system's auto-assigned duplicates added later in pack.py."""
    rng = _rng("dispatch")
    b = blocks_hist.copy()
    b["gc"] = b["ijk"].map(gc_by_block)
    b = b[(b["gc"] >= P.LG_LOW_CUT) & (b["gc"] < P.OLD_ORE_CUT)].sort_values("mined")
    rows = []
    truck_free = {}
    for _, blk in b.iterrows():
        day = blk["mined"]
        trucks = fleet_on(day)
        remaining = blk["tonnes"]
        shift_start = dt.datetime(day.year, day.month, day.day, 7 if rng.random() < 0.55 else 19)
        t = shift_start + dt.timedelta(minutes=float(rng.uniform(20, 300)))
        shovel = "EX-%02d" % int(rng.choice([1, 2, 3], p=[0.45, 0.4, 0.15]))
        poly = "%d-%03d-%02d" % (blk["bench"], blk["i"], blk["j"])
        while remaining > 30:
            no, model, pay = trucks[int(rng.integers(0, len(trucks)))]
            ft = truck_free.get(no)
            if ft is not None and ft > t:
                t = ft
            rows.append(dict(time_local=t, truck=no, payload=pay, model=model, poly=poly, shovel=shovel,
                             grade=round(float(blk["gc"]), 2), block=int(blk["ijk"])))
            truck_free[no] = t + dt.timedelta(minutes=float(rng.uniform(22, 38)))
            remaining -= pay
            t += dt.timedelta(minutes=float(rng.uniform(2.5, 6.0)))
    ld = pd.DataFrame(rows).sort_values("time_local").reset_index(drop=True)
    return ld


# ---------------------------------------------------------------------------------------------------------------
# The mill DCS and the maintenance system (2025-01-01 to 2026-10-31)
# ---------------------------------------------------------------------------------------------------------------

OUTAGES_UTC = [  # historian collector outages: no events stored
    (dt.datetime(2025, 3, 10, 14, 5), dt.datetime(2025, 3, 13, 21, 40)),
    (dt.datetime(2025, 8, 18, 3, 10), dt.datetime(2025, 8, 22, 16, 40)),
    (dt.datetime(2025, 11, 10, 19, 25), dt.datetime(2025, 11, 13, 9, 50)),
    (dt.datetime(2026, 3, 9, 11, 0), dt.datetime(2026, 3, 12, 2, 30)),
]
TAG_SWITCH_UTC = dt.datetime(2026, 5, 12, 14, 0)


def dcs_and_cmms(stops):
    """Ball mill run-state events as the historian stored them, and the work orders the maintenance system holds."""
    rng = _rng("dcs")
    s = stops[(stops["end"] > dt.datetime(2024, 12, 31)) & (stops["start"] < dt.datetime(2026, 11, 1))].copy()
    # move one planned shutdown into each outage window (the outage happened during the shutdown's network work)
    planned = s[s["kind"] != "TRIP"]
    ev = []
    for _, r in s.iterrows():
        su, eu = local_to_utc(r["start"].to_pydatetime() if hasattr(r["start"], "to_pydatetime") else r["start"]), \
            local_to_utc(r["end"].to_pydatetime() if hasattr(r["end"], "to_pydatetime") else r["end"])
        ev.append((su, 0, r["kind"]))
        ev.append((eu, 1, r["kind"]))
    return s, ev
