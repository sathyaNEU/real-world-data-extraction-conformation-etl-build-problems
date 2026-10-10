"""From generated sessions to the settlement ledger: identifiers, versions, batches, re-deliveries,
the legacy gateway export and the quarter-hour readings."""
from __future__ import annotations

from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from common import QH, TZ, lt_date
from world import GATEWAY_B_END, GATEWAY_B_POS, MIGRATION, RESTATED_POS

DECKS = ("CCN", "CCS")
# Curbline's daily settlement run starts at 10:00 local time and reaches each garage at its own step
# (36-second steps, so every cut keeps the readings exact at 0.001 kWh); the run's start drifts by up to two
# steps from day to day. A session still delivering energy when the run reaches its garage is closed there and
# the charge carries on as a new session record under a new authorization code.
RUN_HOUR = 10
RUN_STEP = {"FTG": 1, "MSG": 2, "LIB": 3, "CCN": 4, "CCS": 5, "CSG": 6, "SWG": 7, "ETG": 8}
RUN_SEED = 2026_1000

H = 3600.0
_AUTH = "ACDEFGHJKLMNPQRTUVWXY34679"


def local_date_of(t):
    return datetime.fromtimestamp(int(t), TZ).date()


def assign_station_ids(df: pd.DataFrame, pos: pd.DataFrame) -> pd.Series:
    p = pos.set_index("position")
    out = np.empty(len(df), dtype=np.int64)
    for i, (position, d) in enumerate(zip(df["position"].to_numpy(), df["day"].to_numpy())):
        r = p.loc[position]
        if pd.notna(r["reissued_id"]) and pd.isna(r["old_id"]):
            out[i] = int(r["reissued_id"])
        elif d < MIGRATION:
            out[i] = int(r["old_id"])
        else:
            out[i] = int(r["new_id"])
    return pd.Series(out, index=df.index)


def auth_codes(rng, n):
    seen = set()
    out = []
    alphabet = np.array(list(_AUTH))
    while len(out) < n:
        c = "".join(rng.choice(alphabet, 10))
        if c not in seen:
            seen.add(c)
            out.append(c[:4] + "-" + c[4:])
    return out


def settle_dates(rng, plug_out, cap=date(2027, 1, 10)):
    d = [local_date_of(t) for t in plug_out]
    u = rng.random(len(d))
    delay = np.where(u < 0.86, rng.integers(1, 7, len(d)), rng.integers(7, 16, len(d)))
    out = []
    for dd, k in zip(d, delay):
        s = dd + timedelta(days=int(k))
        if dd.year == 2026 and s > cap:
            s = cap
        out.append(s)
    return out


def delivery_of(settled: date) -> date:
    """Weekly deliveries on the Monday after the settlement week."""
    return settled + timedelta(days=7 - settled.weekday())


def build_restatements(rng, df: pd.DataFrame):
    """Restated sessions at four South units, May to July 2025.

    Returns (versions, decisions): versions holds every non-accepted version's energy keyed by the
    session's row index; the accepted version stays in df. Decisions is the acceptance log."""
    m = (df["position"].isin(RESTATED_POS) & (df["day"] >= date(2025, 5, 1)) & (df["day"] <= date(2025, 7, 31)))
    v = df[m & (df["role"] == "V")]
    loc_end = [(t - lt_date(d)) / H for t, d in zip(df.loc[m, "end_charge"], df.loc[m, "day"])]
    texture = df[m].loc[[i for i, e in zip(df[m].index, loc_end) if e <= 10.9]]
    texture = texture[texture["role"].isin(["bg", "fill"])]
    pick = texture.index[np.sort(rng.choice(len(texture), size=min(21, len(texture)), replace=False))]
    versions = []   # (row index, version, energy, accepted)
    kinds = {}
    for j, i in enumerate(pick):
        kinds[i] = "v2" if j % 7 not in (3, 5) else ("v3" if j % 7 == 3 else "v2only")
    for i in v.index:
        kinds[i] = "V"
    # the 2024 back-test sessions Curbline restated in March 2025: version 2 accepted, after the 2024-based forecast
    for i in df.index[df["role"] == "Q"]:
        kinds[i] = "Q"
    for i, kind in kinds.items():
        E = float(df.at[i, "energy"])
        if kind == "V":
            vs = [(1, round(E - 0.22, 3), False), (2, E, True), (3, round(E + 0.22, 3), False)]
        elif kind == "Q":
            vs = [(1, E, False), (2, round(E + 0.22 * float(df.at[i, "q_sign"]), 3), True)]
        elif kind == "v2":
            a = round(float(rng.uniform(0.15, 0.55)), 3)
            b = round(float(rng.uniform(0.2, 0.7)), 3)
            vs = [(1, round(E - a, 3), False), (2, E, True), (3, round(E + b, 3), False)]
        elif kind == "v3":
            a = round(float(rng.uniform(0.15, 0.55)), 3)
            b = round(float(rng.uniform(0.2, 0.5)), 3)
            vs = [(1, round(E - a - b, 3), False), (2, round(E - b, 3), False), (3, E, True)]
        else:
            a = round(float(rng.uniform(0.15, 0.55)), 3)
            vs = [(1, round(E - a, 3), False), (2, E, True)]
        for ver, energy, acc in vs:
            versions.append({"row": i, "version": ver, "energy": energy, "accepted": acc, "kind": kind})
    return pd.DataFrame(versions)


def build_ledger(rng, df: pd.DataFrame, pos: pd.DataFrame, read_dec2025: int):
    """Returns dict of frames: sessions (the shipped header rows, all versions and re-deliveries),
    legacy (gateway B), decisions, plus helper columns on df."""
    df = df.copy()
    df["station_id"] = assign_station_ids(df, pos)
    df["auth_code"] = auth_codes(rng, len(df))
    df["settled_on"] = settle_dates(rng, df["plug_out"].to_numpy())
    df["gateway_b"] = (df["garage"] == "CCN") & df["position"].isin(GATEWAY_B_POS) & (df["day"] < GATEWAY_B_END)
    # before the April 2025 platform move a fleet card was authorised and settled through the fleet card
    # system, not through Curbline settlement, so those charges never reached the settlement export
    df["fleet_pre"] = (df["acct"] == "FLEET") & (df["day"] < MIGRATION)
    assert not (df["gateway_b"] & df["fleet_pre"]).any(), "a fleet charge on a gateway B unit"
    # charging at the decks on weekends and Schedule 26 holidays is free to permit holders and is not settled:
    # those sessions ship in Curbline's courtesy-session report, not in the settlement export
    # (the legacy gateway's archive keeps every session on its units, so those stay in the gateway B export)
    df["courtesy"] = df["garage"].isin(DECKS) & (df["role"] == "wkend") & ~df["gateway_b"]
    assert not (df["courtesy"] & df["fleet_pre"]).any()

    vers = build_restatements(rng, df)
    # restated versions settle later and are decided by the parking office
    dec_rows = []
    extra_rows = []
    for i, g in vers.groupby("row"):
        s0 = df.at[i, "settled_on"]
        recv2 = s0 + timedelta(days=int(rng.integers(18, 34)))
        if g["kind"].iloc[0] == "Q":
            recv2 = date(2025, 3, 2) + timedelta(days=int(rng.integers(0, 19)))
        recv3 = recv2 + timedelta(days=int(rng.integers(9, 26)))
        for _, r in g.sort_values("version").iterrows():
            ver = int(r["version"])
            if ver == 1:
                set_on = s0
            else:
                set_on = recv2 if ver == 2 else recv3
                dec_rows.append({"row": i, "version": ver, "received": set_on,
                                 "decided": set_on + timedelta(days=int(rng.integers(3, 12))),
                                 "accepted": bool(r["accepted"])})
            extra_rows.append({"row": i, "version": ver, "energy": float(r["energy"]), "settled_on": set_on,
                               "accepted": bool(r["accepted"])})
    extra = pd.DataFrame(extra_rows)
    decisions = pd.DataFrame(dec_rows)

    # the ledger rows: one per session (version 1) unless restated, then one per version
    restated = set(vers["row"])
    assert not df.loc[list(restated), "fleet_pre"].any() and not df.loc[list(restated), "courtesy"].any()
    base = df[~df["gateway_b"] & ~df["fleet_pre"] & ~df["courtesy"]].copy()
    base["version"] = 1
    base["true_row"] = True
    rows = [base[~base.index.isin(restated)].assign(row=lambda x: x.index)]
    for _, r in extra.iterrows():
        i = int(r["row"])
        row = df.loc[[i]].copy()
        row["version"] = int(r["version"])
        row["energy"] = round(r["energy"], 3)
        row["settled_on"] = r["settled_on"]
        row["true_row"] = bool(r["accepted"])
        row["end_charge"] = row["start"] + row["energy"] / row["rate"] * H
        row["row"] = i
        rows.append(row)
    led = pd.concat(rows, ignore_index=True)
    led = split_at_run(led)
    led["delivered"] = [delivery_of(s) for s in led["settled_on"]]
    led["redelivered"] = False
    led["in_ledger"] = True
    # sessions from the units on the legacy gateway, and fleet-card charges before the platform move, never
    # reached the settlement extract
    gwb = df[df["gateway_b"] | df["fleet_pre"] | df["courtesy"]].copy()
    gwb["version"] = 1
    gwb["true_row"] = True
    gwb["row"] = gwb.index
    gwb["frag"] = 0
    gwb["delivered"] = None
    gwb["redelivered"] = False
    gwb["in_ledger"] = False
    return df, led, gwb, decisions


def run_cut(day, garage, jitter) -> int:
    """Instant the settlement run reaches a garage on a local date."""
    return lt_date(day, RUN_HOUR) + 36 * (RUN_STEP[garage] + jitter[day])


def split_at_run(led: pd.DataFrame) -> pd.DataFrame:
    """Close every export record still delivering energy when the day's settlement run reaches its garage, and carry
    the charge on as a new record from that second, at the same station and on the same permit or card, under a new
    authorization code. A restated charge is restated in the record that carries its end. frag: 0 a charge in one
    record, 1 the record the run closed, 2 the record the charge carried on in."""
    rng = np.random.default_rng(RUN_SEED)
    days = sorted(set(led["day"]))
    jitter = {d: int(x) for d, x in zip(days, rng.integers(0, 3, len(days)))}
    cut = np.array([run_cut(d, g, jitter) for d, g in zip(led["day"], led["garage"])], dtype=np.int64)
    st = led["start"].to_numpy(np.int64)
    v1 = led["version"].to_numpy() == 1
    en1 = led["end_charge"].to_numpy(np.float64)
    # whether a charge is cut is decided on its first version (versions differ only in the last quarter-hour)
    first_end = pd.Series(en1[v1], index=led.loc[v1, "row"].to_numpy())
    first_end = first_end[~first_end.index.duplicated()]
    end_v1 = led["row"].map(first_end).to_numpy(np.float64)
    hit = (st < cut) & (end_v1 > cut + 1.0)
    led = led.copy()
    led["frag"] = 0
    keep = led[~hit]
    cutrows = led[hit].copy()
    cutrows["cut"] = cut[hit]
    rate = cutrows["rate"].to_numpy(np.float64)
    e1 = np.round(rate * (cutrows["cut"].to_numpy() - cutrows["start"].to_numpy()) / H, 3)
    cutrows["e1"] = e1
    used = set(led["auth_code"])
    new_codes = {}
    for r in sorted(set(cutrows["row"])):
        while True:
            c = "".join(rng.choice(np.array(list(_AUTH)), 10))
            c = c[:4] + "-" + c[4:]
            if c not in used:
                used.add(c)
                new_codes[r] = c
                break
    f1 = cutrows[cutrows["version"] == 1].copy()
    f1["energy"] = f1["e1"]
    f1["plug_out"] = f1["cut"]
    f1["end_charge"] = f1["cut"].astype(np.float64)
    f1["settled_on"] = f1["day"]
    f1["true_row"] = True
    f1["frag"] = 1
    f2 = cutrows.copy()
    f2["energy"] = np.round(f2["energy"].to_numpy() - f2["e1"].to_numpy(), 3)
    f2["start"] = f2["cut"]
    f2["auth_code"] = f2["row"].map(new_codes)
    f2["frag"] = 2
    assert (f2["energy"] >= 0.001).all() and (f1["energy"] >= 0.066).all()
    out = pd.concat([keep, f1.drop(columns=["cut", "e1"]), f2.drop(columns=["cut", "e1"])], ignore_index=True)
    return out


def add_redeliveries(rng, led: pd.DataFrame, read_dec2025: int, exclude_rows: set):
    """Re-send a subset of rows from three weekly deliveries under new session identifiers.

    October 2025: the delivery holding the October back-test day's D session.
    December 2025: the delivery holding December's D session, and the delivery holding the
    sessions plugged in on 31 December after the panel read."""
    out = []
    dk = led[(led["role"] == "D") & (led["frag"] != 1)].sort_values("start")
    assert len(dk) == 2
    groups = []
    for _, r in dk.iterrows():
        groups.append((r["delivered"], {r.name}))
    after_read = led[(led["garage"].isin(["CCN", "CCS"])) & (led["start"] >= read_dec2025 + 60)
                     & (led["start"] < read_dec2025 + 6 * 3600) & (led["role"].isin(["bg"]))]
    after_read = after_read[[local_date_of(t) == date(2025, 12, 31) for t in after_read["start"]]]
    sel = set()
    for deck in ("CCN", "CCS"):
        a = after_read[after_read["garage"] == deck]
        k = min(len(a), 3)
        sel |= set(a.index[np.sort(rng.choice(len(a), size=k, replace=False))])
    if len(after_read):
        groups.append((led.loc[list(sel)[0], "delivered"] if sel else None, sel))
    dup_idx = set()
    for deliv, must in groups:
        dup_idx |= must
        pool = led[(led["delivered"] == deliv) & (~led["garage"].isin(["CCN", "CCS"])) & (led["version"] == 1)]
        pool = pool[~pool.index.isin(exclude_rows)]
        k = min(len(pool), int(rng.integers(18, 34)))
        dup_idx |= set(pool.index[np.sort(rng.choice(len(pool), size=k, replace=False))])
    dups = led.loc[sorted(dup_idx)].copy()
    dec_cut = date(2025, 11, 1)
    dups["delivered"] = [date(2025, 11, 17) if d < dec_cut else date(2026, 1, 19) for d in dups["delivered"]]
    dups["redelivered"] = True
    dups["true_row"] = False
    return pd.concat([led, dups], ignore_index=True)


def assign_session_ids(rng, led: pd.DataFrame) -> pd.DataFrame:
    led = led.copy()
    first = led[led["version"] == 1].sort_values(["delivered", "settled_on", "start", "garage", "position"])
    sid = 30412000 + int(rng.integers(100, 900))
    ids = {}
    for idx in first.index:
        sid += int(rng.integers(1, 4))
        ids[idx] = sid
    led["session_id"] = pd.Series(ids, dtype="Int64")
    # restated versions share the identifier of their first version
    v1 = led[led["version"] == 1]
    key = dict(zip(zip(v1["row"], v1["frag"]), v1["session_id"]))
    m = led["version"] > 1
    led.loc[m, "session_id"] = pd.Series([key[(r, f)] for r, f in zip(led.loc[m, "row"], led.loc[m, "frag"])],
                                         index=led.index[m], dtype="Int64")
    assert led["session_id"].notna().all()
    return led


def readings(led: pd.DataFrame) -> pd.DataFrame:
    """Quarter-hour readings for every ledger row: plug-in quarter-hour through plug-out quarter-hour."""
    start = led["start"].to_numpy(np.int64)
    end = led["end_charge"].to_numpy(np.float64)
    po = led["plug_out"].to_numpy(np.int64)
    rate = led["rate"].to_numpy(np.float64)
    energy = led["energy"].to_numpy(np.float64)
    q0 = start // QH
    q1 = (po - 1) // QH
    n = (q1 - q0 + 1).astype(np.int64)
    rep = np.repeat(np.arange(len(led)), n)
    off = np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)
    q = q0[rep] + off
    qs = q * QH
    lo = np.maximum(qs, start[rep]).astype(np.float64)
    hi = np.minimum(qs + QH, end[rep])
    kwh = np.where(hi > lo, rate[rep] * (hi - lo) / H, 0.0)
    kwh = np.round(kwh, 3)
    # the last charging quarter-hour takes the remainder so readings sum to the delivered energy exactly
    last_q = (np.ceil(end / QH) - 1).astype(np.int64)
    is_last = q == last_q[rep]
    s = pd.Series(kwh).groupby(rep).sum().to_numpy()
    fix = np.round(energy - s, 3)
    kwh[is_last] = np.round(kwh[is_last] + fix[rep[is_last]], 3)
    out = pd.DataFrame({"lrow": rep, "interval_start": qs, "kwh": kwh})
    return out
