"""From generated sessions to the settlement ledger: identifiers, versions, batches, re-deliveries,
the legacy gateway export and the quarter-hour readings."""
from __future__ import annotations

from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from common import QH, TZ, lt_date
from world import GATEWAY_B_END, GATEWAY_B_POS, MIGRATION, RESTATED_POS

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
    for i, kind in kinds.items():
        E = float(df.at[i, "energy"])
        if kind == "V":
            vs = [(1, round(E - 0.22, 3), False), (2, E, True), (3, round(E + 0.22, 3), False)]
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

    vers = build_restatements(rng, df)
    # restated versions settle later and are decided by the parking office
    dec_rows = []
    extra_rows = []
    for i, g in vers.groupby("row"):
        s0 = df.at[i, "settled_on"]
        recv2 = s0 + timedelta(days=int(rng.integers(18, 34)))
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
    assert not df.loc[list(restated), "fleet_pre"].any()
    base = df[~df["gateway_b"] & ~df["fleet_pre"]].copy()
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
    led["delivered"] = [delivery_of(s) for s in led["settled_on"]]
    led["redelivered"] = False
    led["in_ledger"] = True
    # sessions from the units on the legacy gateway, and fleet-card charges before the platform move, never
    # reached the settlement extract
    gwb = df[df["gateway_b"] | df["fleet_pre"]].copy()
    gwb["version"] = 1
    gwb["true_row"] = True
    gwb["row"] = gwb.index
    gwb["delivered"] = None
    gwb["redelivered"] = False
    gwb["in_ledger"] = False
    return df, led, gwb, decisions


def add_redeliveries(rng, led: pd.DataFrame, read_dec2025: int, exclude_rows: set):
    """Re-send a subset of rows from three weekly deliveries under new session identifiers.

    October 2025: the delivery holding the October back-test day's D session.
    December 2025: the delivery holding December's D session, and the delivery holding the
    sessions plugged in on 31 December after the panel read."""
    out = []
    dk = led[led["role"] == "D"].sort_values("start")
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
    key = led[led["version"] == 1].set_index("row")["session_id"]
    key = key[~key.index.duplicated(keep="first")]
    m = led["version"] > 1
    led.loc[m, "session_id"] = led.loc[m, "row"].map(key).astype("Int64")
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
