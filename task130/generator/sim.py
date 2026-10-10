"""Simulates the borough's homelessness cases, the move-on queue and the temporary-accommodation
placements from April 2018 to the extract cut. Returns plain DataFrames holding the full truth;
extracts.py censors them at the cut and writes the shipped files."""
import numpy as np
import pandas as pd

import world as W


def _days(rng, lo, hi, n=None):
    return pd.to_timedelta(rng.integers(lo, hi + 1, n), unit="D")


def cases(rng):
    rows = []
    months = pd.date_range(W.SIM_START, W.ASOF, freq="MS")
    for i, m in enumerate(months):
        lam = 92 + 34 * i / len(months)
        if pd.Timestamp("2023-08-01") <= m <= pd.Timestamp("2024-01-01"):
            lam *= 1.35                                  # the autumn 2023 rise in approaches
        n_ta = rng.poisson(lam)
        n_home = rng.poisson(7.5)
        dim = m.days_in_month
        for _ in range(n_ta):
            app = m + pd.Timedelta(days=int(rng.integers(0, dim)))
            rows.append(dict(app=app, placed=True))
        for _ in range(n_home):
            app = m + pd.Timedelta(days=int(rng.integers(0, dim)))
            rows.append(dict(app=app, placed=False))
    df = pd.DataFrame(rows).sort_values("app", kind="mergesort").reset_index(drop=True)
    n = len(df)
    df["need"] = rng.choice(W.SIZES, n, p=W.NEED_MIX)
    df["ta_start"] = df["app"].where(df["placed"])
    lag = rng.integers(21, 76, n)
    slow = rng.random(n) < 0.22                      # inquiries, reviews and late evidence
    lag = np.where(slow, rng.integers(110, 330, n), lag)
    lag_home = rng.integers(30, 71, n)
    df["decision"] = df["app"] + pd.to_timedelta(np.where(df["placed"], lag, lag_home), unit="D")
    df["main"] = np.where(df["placed"], rng.random(n) < 0.52, True)
    # households not owed the main duty leave at the decision
    df["exit"] = pd.NaT
    df["exit_reason"] = None
    nm = ~df["main"]
    df.loc[nm, "exit"] = df.loc[nm, "decision"] + _days(rng, 0, 14, nm.sum())
    df.loc[nm, "exit_reason"] = rng.choice(
        ["Relief duty ended: accommodation secured", "Main duty not owed", "Contact lost"],
        nm.sum(), p=[0.55, 0.35, 0.10])
    df["duty"] = df["decision"].where(df["main"])
    # early other exits, inside the first 120 days of the main duty only
    oth = df["main"] & (rng.random(n) < 0.12)
    df.loc[oth, "exit"] = df.loc[oth, "duty"] + _days(rng, 5, 120, oth.sum())
    df.loc[oth, "exit_reason"] = rng.choice(
        ["Own arrangements", "Moved out of the area", "Contact lost"], oth.sum(), p=[0.5, 0.3, 0.2])
    # bedroom need reassessed upward (a birth, a child joining the household)
    re = df["main"] & (rng.random(n) < 0.06)
    df["reassess"] = pd.NaT
    df.loc[re, "reassess"] = df.loc[re, "duty"] + _days(rng, 60, 900, re.sum())
    df["need_after"] = np.minimum(df["need"] + 1, 4)
    # application years number the case references
    df["case_ref"] = [
        "HPR/%02d/%05d" % (a.year % 100, k + 1)
        for k, a in zip(df.groupby(df["app"].dt.year).cumcount(), df["app"])
    ]
    df["hh"] = ["H%06d" % (100000 + i * 7 % 900000) for i in range(n)]
    return df


def need_at(df, t):
    """bedroom need of every case on day t"""
    after = df["reassess"].notna() & (df["reassess"] <= t)
    return np.where(after, df["need_after"], df["need"])


def allocate(df, rng, end):
    """Move-on lets from April 2018 to `end`, each given to the household at the front of its
    size's list: main duty accepted, still owed, current need equal to the let's size, earliest
    duty date first, then case reference."""
    lets = []
    months = pd.date_range(W.SIM_START, end, freq="MS")
    duty = df["duty"].values.astype("datetime64[D]")
    ref = df["case_ref"].values
    order_key = np.lexsort((ref, duty))            # duty date, then case reference
    rank = np.empty(len(df), int)
    rank[order_key] = np.arange(len(df))
    exit_ = df["exit"].values.astype("datetime64[D]")
    has_exit = ~pd.isna(df["exit"]).values
    main = df["main"].values
    for m in months:
        for s in W.SIZES:
            k = rng.poisson(W.supply(m, s))
            for _ in range(k):
                d = m + pd.Timedelta(days=int(rng.integers(0, m.days_in_month)))
                lets.append((d, s))
    lets.sort()
    let_case = []
    taken = np.zeros(len(df), bool)
    for d, s in lets:
        t = np.datetime64(d.date())
        nd = need_at(df, d)
        ok = main & (duty <= t) & ~taken & (nd == s) & (~has_exit | (exit_ > t))
        if not ok.any():
            let_case.append(None)
            continue
        idx = np.flatnonzero(ok)
        j = idx[np.argmin(rank[idx])]
        taken[j] = True
        exit_[j] = t
        has_exit[j] = True
        let_case.append(j)
    lt = pd.DataFrame({"tenancy_start": [d for d, _ in lets], "size": [s for _, s in lets], "row": let_case})
    lt = lt.dropna(subset=["row"]).astype({"row": int}).reset_index(drop=True)
    df = df.copy()
    df.loc[lt["row"].values, "exit"] = lt["tenancy_start"].values
    kind = np.where(rng.random(len(lt)) < 0.76, "Settled: social housing let", "Settled: private let (Larkmoor Lettings)")
    df.loc[lt["row"].values, "exit_reason"] = kind
    lt["kind"] = kind
    lt["offer_date"] = lt["tenancy_start"] - _days(rng, 9, 24, len(lt))
    return df, lt


def hash_pick(uid, f):
    import zlib
    return zlib.crc32(("%s|%s" % (uid, f.date())).encode())


def _tenter_house(df, rows, far):
    """Tenter House flats are let, from the day the block opened until the owner's notice, to the
    household that has been in a nightly-paid flat longest under the main duty (earliest duty date,
    then case reference) among those whose bedroom need matches the flat; the move takes place a
    week after the flat falls vacant (the opening let ran over eight weeks)."""
    import heapq
    units = [(W.TH_OPEN + pd.Timedelta(days=int(k * 56 / sum(W.TH_UNITS.values()))), s, "TH-%d%02d" % (s, q + 1))
             for k, (s, q) in enumerate((s, q) for s in W.SIZES for q in range(W.TH_UNITS[s]))]
    heapq.heapify(units)
    np_idx = [j for j, r in enumerate(rows) if r[1] == "Nightly-paid self-contained"]
    hh = np.array([rows[j][0] for j in np_idx])
    st = np.array([rows[j][3] for j in np_idx], dtype="datetime64[ns]")
    en = np.array([rows[j][4] for j in np_idx], dtype="datetime64[ns]")
    duty = df["duty"].values.astype("datetime64[ns]")[hh]
    order = np.lexsort((df["case_ref"].values[hh], duty))
    rank = np.empty(len(hh), int)
    rank[order] = np.arange(len(hh))
    need0 = df["need"].values[hh]
    need1 = df["need_after"].values[hh]
    rea = df["reassess"].values.astype("datetime64[ns]")[hh]
    avail = np.ones(len(hh), bool)
    while units:
        f, s, uid = heapq.heappop(units)
        if f + pd.Timedelta(days=7) >= W.NOTICE:
            continue
        t = np.datetime64(f)
        nd = np.where(~np.isnat(rea) & (rea <= t), need1, need0)
        ok = avail & (st < t) & (en > t + np.timedelta64(45, "D")) & (nd == s)
        if not ok.any():
            heapq.heappush(units, (f + pd.Timedelta(days=14), s, uid))
            continue
        cand = np.flatnonzero(ok)
        if f >= W.TH_RULE:
            c = cand[np.argmin(rank[cand])]
        else:
            # before the rule, flats went by school and support ties: no order by waiting time
            c = cand[(hash_pick(uid, f) % len(cand))]
        j = np_idx[c]
        avail[hh == hh[c]] = False
        i_, typ, unit, st_, en_, kind = rows[j]
        mv = f + pd.Timedelta(days=7)
        rows[j] = (i_, typ, unit, st_, mv, "move")
        rows.append((i_, "Tenter House", uid, mv, en_, kind))
        if en_ < far:
            heapq.heappush(units, (en_ + pd.Timedelta(days=4), s, uid))


def placements(df, rng):
    """Every temporary-accommodation placement, start and end. A household starts in bed and
    breakfast or a hostel; once the main duty is accepted it moves to self-contained
    accommodation, Tenter House when a flat of its bedroom need is free (flats filled in order of
    the move date), otherwise a private sector lease or a nightly-paid flat."""
    rows = []
    far = pd.Timestamp("2099-12-31")
    th_free = {s: [pd.Timestamp("1900-01-01")] * W.TH_UNITS[s] for s in W.SIZES}
    th_ids = {s: ["TH-%d%02d" % (s, k + 1) for k in range(W.TH_UNITS[s])] for s in W.SIZES}
    placed = df[df["placed"]]
    fl = rng.integers(14, 71, len(placed))
    ft = rng.choice(["Bed and breakfast", "Hostel"], len(placed), p=[0.6, 0.4])
    wait = rng.integers(3, 31, len(placed))
    u_away = rng.random(len(placed))
    u_away_t = rng.random(len(placed))
    u_np = rng.random(len(placed))
    u_np_move = rng.random(len(placed))
    u_np_t = rng.random(len(placed))
    u_th_out = rng.random(len(placed))
    u_th_t = rng.random(len(placed))
    seq = []
    for k, (i, r) in enumerate(placed.iterrows()):
        end = r["exit"] if pd.notna(r["exit"]) else far
        if not r["main"]:
            rows.append((i, ft[k], None, r["ta_start"], end, "left"))
            continue
        d2 = max(r["ta_start"] + pd.Timedelta(days=int(fl[k])), r["duty"] + pd.Timedelta(days=int(wait[k])))
        if end <= d2:
            rows.append((i, ft[k], None, r["ta_start"], end, "left"))
            continue
        rows.append((i, ft[k], None, r["ta_start"], d2, "move"))
        seq.append((d2, i, k, end))
    seq.sort(key=lambda x: (x[0], x[1]))
    opened = False
    for d2, i, k, end in seq:
        span = (min(end, W.ASOF + pd.Timedelta(days=400)) - d2).days
        away = None
        if u_away[k] < 0.05 and span > 150:
            away = d2 + pd.Timedelta(days=int(60 + u_away_t[k] * (span - 90)))
        stop = away if away is not None else end
        last = "away" if away is not None else "left"
        s = int(need_at(df.loc[[i]], d2)[0])
        t2 = "Private sector lease" if u_np[k] < 0.45 else "Nightly-paid self-contained"
        if t2 == "Nightly-paid self-contained" and u_np_move[k] < 0.25 and (stop - d2).days > 240:
            d3 = d2 + pd.Timedelta(days=int(90 + u_np_t[k] * ((min(stop, far) - d2).days - 150)))
            rows.append((i, t2, None, d2, d3, "move"))
            rows.append((i, "Private sector lease", None, d3, stop, last))
        else:
            rows.append((i, t2, None, d2, stop, last))
    _tenter_house(df, rows, far)
    # emergency stays are often split: a first bed and breakfast, then a hostel room or another hotel
    out = []
    split_u = rng.random(len(rows))
    split_t = rng.random(len(rows))
    for k, r in enumerate(rows):
        i, typ, unit, st, en, kind = r
        span = (min(en, W.ASOF + pd.Timedelta(days=60)) - st).days
        if typ in ("Bed and breakfast", "Hostel") and split_u[k] < 0.55 and span >= 12:
            mid = st + pd.Timedelta(days=int(4 + split_t[k] * (span - 8)))
            other = "Hostel" if (typ == "Bed and breakfast" and split_t[k] < 0.5) else "Bed and breakfast"
            out.append((i, typ, None, st, mid, "move"))
            out.append((i, other, None, mid, en, kind))
        else:
            out.append(r)
    pl = pd.DataFrame(out, columns=["row", "type", "unit", "start", "end", "end_kind"])
    pl = pl.sort_values(["start", "row"], kind="mergesort").reset_index(drop=True)
    return pl
