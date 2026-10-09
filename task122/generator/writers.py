"""task122 generator: deterministic writers for the data files.

CSV: fixed column order, explicit number formats, "\n" line endings. Parquet: an explicit arrow
schema built from arrays (no pandas metadata), zstd, fixed row-group size. XLSX: xlsxwriter with a
fixed creation date; the container is normalised afterwards (fixed entry times) and its core
properties scrubbed.
"""
import io
import os
import zipfile
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import params as P

EPOCH = datetime(2025, 1, 1)

F_RENDER = "home_carousel_render_log_2026-06-22_2026-09-20.csv"
F_RANKINGS = "home_carousel_served_rankings_2026-06-22_2026-09-20.parquet"
F_ORDERS = "orders_enrolled_buyers_2026-06-01_2026-10-11.parquet"
F_PAYMENTS = "payments_buyer_protection_2026-06-01_2026-10-11.parquet"
F_OFFERS = "offers_accepted_{start}_2026-10-11.csv"


def _iso(seconds):
    s = np.asarray(seconds, np.int64)
    base = np.datetime64("2025-01-01T00:00:00")
    return np.datetime_as_string(base + s.astype("timedelta64[s]"), unit="s")


def _ts_array(seconds):
    s = np.asarray(seconds, np.int64)
    epoch_unix = int((EPOCH - datetime(1970, 1, 1)).total_seconds())
    return pa.array(s + epoch_unix, type=pa.timestamp("s"))


def write_csv(df, path):
    df.to_csv(path, index=False, lineterminator="\n")


def write_parquet(table, path, row_group=200_000):
    pq.write_table(table, path, compression="zstd", compression_level=9, row_group_size=row_group,
                   use_dictionary=True, data_page_version="1.0", write_statistics=True)


def render_log(W, path):
    S = W.S
    N = len(S)
    n = S.n.to_numpy()
    sid = np.repeat(np.arange(N), n)
    seq = np.concatenate([np.arange(1, k + 1) for k in n])
    day0 = np.array([(datetime(d.year, d.month, d.day) - EPOCH).total_seconds() for d in S.date], np.int64)
    t = day0[sid] + S.start_s.to_numpy()[sid] + W.render_offsets[sid, seq - 1]
    ordered = []
    for s in range(N):
        ps = np.flatnonzero(W.ordered[s]) + 1
        ordered.append(" ".join(str(p) for p in ps))
    ordered = np.array(ordered, dtype=object)
    df = pd.DataFrame({
        "session_id": S.session_id.to_numpy()[sid],
        "render_seq": seq,
        "rendered_at": [x.replace("T", " ") for x in _iso(t)],
        "platform": S.platform.to_numpy()[sid],
        "buyer_tenure_days": S.tenure.to_numpy()[sid],
        "pool_id": S.pool_id.to_numpy()[sid],
        "ranker": np.array(P.RANKERS)[S.arm.to_numpy()][sid],
        "propensity": [f"{p:.2f}" for p in P.PI[S.cell.to_numpy(), S.arm.to_numpy()][sid]],
        "ordered_tiles": ordered[sid],
    })
    df = df.iloc[np.lexsort((df.render_seq.to_numpy(), df.session_id.to_numpy(), t))]
    write_csv(df, path)
    return len(df)


def served_rankings(W, path):
    S, WL = W.S, W.WL
    N = len(S)
    day0 = np.array([(datetime(d.year, d.month, d.day) - EPOCH).total_seconds() for d in S.date], np.int64)
    wl = WL.sort_values(["sid", "listing_id"], kind="stable")
    lists = [""] * N
    for sid, g in wl.groupby("sid"):
        lists[sid] = " ".join(str(x) for x in g.listing_id.to_numpy())
    order = np.lexsort((S.session_id.to_numpy(), day0 + S.start_s.to_numpy()))
    cols = {
        "session_id": pa.array(S.session_id.to_numpy()[order], pa.string()),
        "buyer_id": pa.array(S.buyer_id.to_numpy()[order], pa.int64()),
        "started_at": _ts_array((day0 + S.start_s.to_numpy())[order]),
        "ended_at": _ts_array((day0 + S.end_s.to_numpy())[order]),
        "buyer_region": pa.array(S.region.to_numpy()[order], pa.string()),
    }
    for p in range(6):
        cols[f"tile_{p + 1}"] = pa.array(W.tile_ids[order, p], pa.int64())
    for p in range(6):
        cols[f"tile_{p + 1}_age_h"] = pa.array(np.round(W.age[order, p], 1), pa.float64())
    cols["watchlist_at_start"] = pa.array(np.array(lists, dtype=object)[order], pa.string())
    write_parquet(pa.table(cols), path)
    return N


def orders(W, path):
    O = W.O
    cols = {
        "order_id": pa.array(O.order_id.to_numpy(), pa.int64()),
        "buyer_id": pa.array(W.S.buyer_id.to_numpy()[O.sid.to_numpy()], pa.int64()),
        "listing_id": pa.array(O.listing_id.to_numpy(), pa.int64()),
        "ordered_at": _ts_array(O.t.to_numpy()),
        "channel": pa.array(O.channel.to_numpy(), pa.string()),
        "home_session_id": pa.array(O.session_id.to_numpy(), pa.string()),
        "platform": pa.array(O.platform.to_numpy(), pa.string()),
        "category": pa.array(O.category.to_numpy(), pa.string()),
        "asking_price_eur": pa.array(O.asking.to_numpy().astype(float), pa.float64()),
        "delivery": pa.array(O.delivery.to_numpy(), pa.string()),
    }
    write_parquet(pa.table(cols), path)
    return len(O)


def payments(W, path):
    PM = W.PM.sort_values(["captured", "order_id"], kind="stable")
    cols = {
        "payment_id": pa.array(PM.payment_id.to_numpy(), pa.string()),
        "order_id": pa.array(PM.order_id.to_numpy(), pa.int64()),
        "captured_at": _ts_array(PM.captured.to_numpy()),
        "amount_eur": pa.array(PM.amount_cents.to_numpy() / 100.0, pa.float64()),
        "shipping_eur": pa.array(PM.ship_cents.to_numpy() / 100.0, pa.float64()),
        "buyer_protection_fee_eur": pa.array(PM.fee_cents.to_numpy() / 100.0, pa.float64()),
    }
    write_parquet(pa.table(cols), path)
    return len(PM)


def offers(W, tgt):
    F = W.F
    start = (EPOCH + timedelta(seconds=int(F.offered.min()))).date()
    path = os.path.join(tgt, F_OFFERS.format(start=start.isoformat()))
    df = pd.DataFrame({
        "offer_id": F.offer_id.to_numpy(),
        "listing_id": F.listing_id.to_numpy(),
        "buyer_id": W.S.buyer_id.to_numpy()[F.buyer_sid.to_numpy()],
        "offered_at": [x.replace("T", " ") for x in _iso(F.offered.to_numpy())],
        "offer_eur": [f"{v:.2f}" for v in F.offer_eur.to_numpy()],
        "accepted_at": [x.replace("T", " ") for x in _iso(F.accepted.to_numpy())],
        "expires_at": [x.replace("T", " ") for x in _iso(F.expires.to_numpy())],
    })
    write_csv(df, path)
    return os.path.basename(path), len(df)


# ------------------------------------------------------------------ containers

def normalise_zip(path, when=(2026, 10, 14, 9, 0, 0)):
    """Rewrite an OOXML container with fixed entry timestamps and order, contents unchanged."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = [(i.filename, z.read(i.filename)) for i in infos]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for name, blob in data:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            out.writestr(zi, blob)
    with open(path, "wb") as f:
        f.write(buf.getvalue())
