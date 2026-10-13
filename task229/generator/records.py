"""task229 generator: the network's exports from the truth. The daily record (two telemetry generations, the GOES
ingest's held messages, cellular backfills, provisional and approved rows, the relocation), the gaugings (field
times in UTC, litres at the spring creeks, braided sections by channel, the rating column rewritten at the move),
the gauged ranges the rating book prints, the visit log and the migration tracker."""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import params as P
import truth as T
import world as W

CLOCK = ZoneInfo(P.TZ)
UTC = timezone.utc
LST = timezone(timedelta(hours=P.LST_OFFSET_H))


def rng(*k):
    return np.random.default_rng([P.SEED, 500, *k])


def sig4(x):
    return W.sig(x, 4)


def rating_in_force(no, d):
    """(parameters, rating number) in force at a site on a local standard date"""
    if no == "C122":
        return W.RATING[no], W.RATING_NO[no]
    if d < P.MOVE:
        return W.OLD_RATING[no], W.OLD_RATING_NO[no]
    return W.RATING[no], W.RATING_NO[no]


def active(no, d):
    if no == "C110":
        return d <= P.RELOC_END
    if no == "C122":
        return d >= P.RELOC_START
    return True


GOES_LOSS = {"C107": 0.050, "C116": 0.050, "C120": 0.055, "C108": 0.040, "C114": 0.045, "C111": 0.040,
             "C115": 0.045}                         # the oldest platforms
GOES_LOSS_DEFAULT = 0.022
CELL_MISS = 0.014
NEVER = 0.0012


def iso(dt):
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def daily_record(TR):
    """the daily records export, WY2023 to WY2026"""
    rows = []
    D = TR["D"]
    days = [d for d in T.DAYS if P.RECORD_START <= d <= P.RECORD_END]
    import knobs as KN
    for k, no in enumerate(sorted(W.ST)):
        st = W.ST[no]
        r = rng(1, k, KN.DAILY_SALT)
        res = st["res"]
        last = None                         # last GOES row (for the ingest's hold)
        miss_prev = False
        cut = st["cutover"]
        slot_h, slot_m = (int(x) for x in st["slot"].split(":")) if st["slot"] else (0, 0)
        for d in days:
            if not active(no, d):
                continue
            i = T.DAYS.index(d) if False else (d - T.T0).days
            par, rno = rating_in_force(no, d)
            out = []
            # GOES row for the UTC day d (until the cut-over day, inclusive)
            if no != "C122" and d <= cut:
                loss = GOES_LOSS.get(no, GOES_LOSS_DEFAULT)
                missed = r.random() < (0.30 if miss_prev else loss)
                miss_prev = missed
                if missed and last is not None:
                    held = dict(last)
                    held["date"] = d
                    out.append(held)                     # the ingest holds the platform's last message
                elif not missed:
                    wl = round(round(D[no]["utc"][i] / res) * res, 3)
                    q = sig4(W.q_of_h(par, wl))
                    rec = datetime(d.year, d.month, d.day, slot_h, slot_m, tzinfo=UTC) + timedelta(days=1, seconds=int(r.integers(4, 58)))
                    row = {"station": no, "date": d, "water_level_m": wl, "discharge_m3s": q, "platform": "GOES",
                           "received_utc": iso(rec)}
                    out.append(row)
                    last = row
            # new-platform row for the local standard day d (from the cut-over day)
            if d >= cut:
                wl = round(round(D[no]["local"][i] / res) * res, 3)
                q = sig4(W.q_of_h(par, wl))
                plat = st["new_platform"]
                base = datetime(d.year, d.month, d.day, tzinfo=LST) + timedelta(days=1, minutes=int(r.integers(4, 26)), seconds=int(r.integers(0, 60)))
                u = r.random()
                if u < NEVER:
                    pass                                   # never arrived: a gap
                else:
                    if u < CELL_MISS:
                        base = base + timedelta(days=int(r.integers(2, 10)), hours=int(r.integers(1, 9)))
                    out.append({"station": no, "date": d, "water_level_m": wl, "discharge_m3s": q,
                                "platform": plat, "received_utc": iso(base)})
            for row in out:
                wy26 = P.WY_START <= d <= P.WY_END
                if wy26 and d <= P.REVIEWED_TO:
                    rows.append(dict(row, status="provisional"))
                    rows.append(dict(row, status="approved"))
                elif wy26:
                    rows.append(dict(row, status="provisional"))
                else:
                    rows.append(dict(row, status="approved"))
    df = pd.DataFrame(rows, columns=["station", "date", "water_level_m", "discharge_m3s", "status", "platform", "received_utc"])
    df = df.sort_values(["station", "date", "received_utc", "status"], kind="mergesort").reset_index(drop=True)
    return df


# ---------------------------------------------------------------- gaugings

def local_dt(d, hour_float):
    h = int(hour_float)
    m = int(round((hour_float - h) * 60))
    if m == 60:
        h, m = h + 1, 0
    return datetime(d.year, d.month, d.day, h, m, tzinfo=CLOCK)


def truth_at(TR, no, dt):
    """true flow and water level at a clock instant (nearest 5-minute step)"""
    lst = dt.astimezone(LST)
    day = lst.date()
    i = (day - T.T0).days
    step = int((lst.hour * 60 + lst.minute) // P.STEP_MIN)
    j = i * T.SPD + step
    return float(TR["S"][no][j]), float(TR["H"][no][j])


def plan_dates(r, wy, n, regulated, first=None, last=None):
    """n visit dates spread over a water year"""
    start = date(wy - 1, 10, 1) if first is None else first
    end = date(wy, 9, 30) if last is None else last
    span = (end - start).days
    edges = np.linspace(0, span, n + 1)
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        d = start + timedelta(days=int(r.integers(int(a) + 2, max(int(a) + 3, int(b) - 2))))
        out.append(d)
    return out


def station_gaugings(TR, no, salt=0):
    """one station's gaugings, water years 2017 to 2026 (as rows before numbering)"""
    import knobs as KN
    k = sorted(W.ST).index(no)
    r = rng(2, k, salt)
    reg = no in ("C104", "C105")
    est = W.ESTABLISHED[no]
    rows = []
    for wy in range(P.GAUGING_FROM + 1, 2027):
        first, last = None, None
        if no == "C110":
            if wy == 2026:
                last = P.RELOC_START - timedelta(days=1)
        if no == "C122":
            if wy != 2026:
                continue
            first = P.RELOC_START
        if est >= wy and no != "C122":
            continue
        n = int(r.integers(6, 10))
        if no == "C110" and wy == 2026:
            n = 6
        if no == "C122":
            dates = [date(2026, 6, 9), date(2026, 6, 23)] + plan_dates(r, wy, 3, reg, date(2026, 7, 1), last)
        else:
            dates = plan_dates(r, wy, n, reg, first, last)
        for d in dates:
            if reg and d.month not in W.CONTINUOUS_MONTHS:
                hr = float(r.uniform(10.75, 15.25))
                note = "between generating periods, plant at minimum release"
            elif reg:
                hr = float(r.uniform(8.5, 16.0))
                note = "plant on continuous generation"
            else:
                hr = float(r.uniform(8.5, 16.5))
                note = ""
            dt = local_dt(d, hr)
            if no in WADE_LIMIT:
                tries = 0
                while truth_at(TR, no, dt)[0] > WADE_LIMIT[no] and tries < 40:
                    dt = dt + timedelta(days=3)
                    tries += 1
                if truth_at(TR, no, dt)[0] > WADE_LIMIT[no]:
                    continue
                note = "wading"
            rows.append(_one(TR, r, no, dt, note))
    if no == "C116":
        # the evening gauging at Cawdell Creek on 31 March 2026, the last stop of a long field day
        rows.append(_one(TR, rng(3, 0), "C116", datetime(2026, 3, 31, 17, 40, tzinfo=CLOCK), "last stop of the day"))
    out = []
    for x in rows:
        out.extend(x)
    return out


def number(rows):
    df = pd.DataFrame(rows)
    df = df.sort_values(["measured_utc", "station", "notes"], kind="mergesort").reset_index(drop=True)
    # gauging numbers: year-month of the local date and a network-wide sequence; channel rows share one
    df["ym"] = [pd.Timestamp(u).tz_convert(P.TZ).strftime("%y%m") for u in df.measured_utc]
    seq, nos, cur = {}, [], {}
    for key, ym in zip(df.key, df.ym):
        if key not in cur:
            seq[ym] = seq.get(ym, 0) + 1
            cur[key] = "%s-%03d" % (ym, seq[ym])
        nos.append(cur[key])
    df["gauging_no"] = nos
    return df.drop(columns=["ym", "key"])


def gaugings(TR):
    import knobs as KN
    rows = []
    for no in sorted(W.ST):
        rows.extend(station_gaugings(TR, no, KN.GAUGE_SALT.get(no, 0)))
    return number(rows)


SPLIT_Q = {"C108": 28.0, "C119": 24.0}
WADE_LIMIT = {"C107": 4.2}          # Sable Creek: no bridge or cableway, gauged only where it can be waded


def _one(TR, r, no, dt, note):
    q, h = truth_at(TR, no, dt)
    eps = float(np.clip(r.normal(0, 0.014), -0.026, 0.026))
    qm = q * (1 + eps)
    gh = round(h, 3)
    unit = W.ST[no]["unit"]
    fac = 1000.0 if unit == "L/s" else 1.0
    method = "volumetric" if q < 0.1 else ("current meter" if q < 6 else "ADCP")
    rno = W.RATING_NO[no]
    crew = "F%d" % (1 + (int(no[1:]) + dt.month) % 3)
    base = {"station": no, "measured_utc": iso(dt), "gh_m": gh, "unit": unit, "method": method, "rating": rno,
            "crew": crew, "key": "%s|%s" % (no, iso(dt))}
    if no in SPLIT_Q and q > SPLIT_Q[no]:
        s = float(r.uniform(0.38, 0.62))
        out = []
        for part, side in ((s, "east channel"), (1 - s, "west channel")):
            out.append(dict(base, discharge=W.sig(qm * part * fac, 3), notes=side))
        return out
    return [dict(base, discharge=W.sig(qm * fac, 3), notes=note)]


def gauged_ranges(G):
    """the top and bottom of each station's gauged range as the rating book prints it: gaugings to 31 March 2026
    (C122: its gaugings to 30 June 2026), channel rows summed, litres converted"""
    g = G.copy()
    g["q"] = np.where(g.unit == "L/s", g.discharge / 1000.0, g.discharge)
    g["d"] = [pd.Timestamp(u).tz_convert("Etc/GMT+8").date() for u in g.measured_utc]
    tot = g.groupby(["gauging_no", "station"], as_index=False).agg(q=("q", "sum"), d=("d", "first"))
    out = {}
    for no in sorted(W.ST):
        lim = date(2026, 6, 30) if no == "C122" else date(2026, 3, 31)
        sel = tot[(tot.station == no) & (tot.d <= lim)]
        if no == "C110":
            sel = tot[(tot.station == no) & (tot.d <= date(2026, 3, 31))]
        lo, hi = sel.loc[sel.q.idxmin()], sel.loc[sel.q.idxmax()]
        out[no] = {"low": float(lo.q), "low_date": lo.d, "high": float(hi.q), "high_date": hi.d, "n": int(len(sel))}
    return out


if __name__ == "__main__":
    import time
    t = time.time()
    TR = T.build_truth()
    DR = daily_record(TR)
    G = gaugings(TR)
    print("built in %.1fs; daily rows %d; gauging rows %d" % (time.time() - t, len(DR), len(G)))
    print(DR.head(3).to_string())
    print(G.head(3).to_string())
    GR = gauged_ranges(G)
    print({k: (round(v["high"], 3), v["n"]) for k, v in GR.items()})


def visit_rows(G, DR):
    """the WY2026 field visit log: gaugings, cut-overs, the relocation, Lake Ashlin's stop logs, routine checks and the
    modem resets after which a cellular logger sent the days it had missed"""
    rows = []
    g = G.copy()
    g["d"] = [pd.Timestamp(u).tz_convert(P.TZ).date() for u in g.measured_utc]
    g = g[(g.d >= P.WY_START) & (g.d <= P.WY_END)].drop_duplicates(["gauging_no"])
    for _, x in g.iterrows():
        rows.append((x.d, x.station, x.crew, "gauging; staff gauge read"))
    for no in sorted(W.ST):
        st = W.ST[no]
        if no == "C122":
            rows.append((P.RELOC_START, "C122", "F2", "new section commissioned; cellular logger installed; levels run to benchmark"))
            continue
        cut = st["cutover"]
        rows.append((cut - timedelta(days=W.install_lead(no, cut)), no, "F%d" % (1 + int(no[1:]) % 3), "%s platform installed" % st["new_platform"]))
        rows.append((cut + timedelta(days=1), no, "F%d" % (1 + int(no[1:]) % 3), "GOES platform removed"))
    rows.append((P.RELOC_END + timedelta(days=1), "C110", "F2", "old site dismantled; logger and staff gauge recovered"))
    rows.append((date(2025, 10, 14), "C102", "F1", "stop logs pulled for the winter level"))
    rows.append((date(2026, 6, 2), "C102", "F1", "stop logs set for the summer level"))
    r = rng(9, 0)
    for no in sorted(W.ST):
        if no in ("C110", "C122"):
            continue
        for mth in (11, 2, 5, 8):
            y = 2025 if mth >= 10 else 2026
            rows.append((date(y, mth, int(r.integers(3, 27))), no, "F%d" % (1 + int(r.integers(0, 3))), "routine check; battery and desiccant"))
    late = DR[(DR.platform == "cellular")].copy()
    late["rd"] = [pd.Timestamp(u).tz_convert("Etc/GMT+8").date() for u in late.received_utc]
    late["lag"] = [(a - b).days for a, b in zip(late.rd, late.date)]
    late = late[(late.lag >= 2) & (late.date >= P.WY_START) & (late.date <= P.WY_END)].drop_duplicates(["station", "rd"])
    for _, x in late.iterrows():
        if r.random() < 0.5:
            rows.append((x.rd, x.station, "F%d" % (1 + int(r.integers(0, 3))), "modem reset; logger resent stored days"))
    return [x for x in rows if P.WY_START <= x[0] <= P.WY_END]
