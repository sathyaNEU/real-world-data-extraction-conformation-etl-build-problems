"""Cut task171's evidence pack (target/) from the clean truth in world.py: the back office's invoice lines, invoices
and payments, the motor vehicle division's hold returns, the agency's placements, the commercial MarrowPass postings,
the lane table, the plaza traffic counts and the image review summary. One RNG stream for the export layer."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import common as C

D = dt.date
TD = dt.timedelta
CLASS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5}


def write_parquet(df, path):
    tbl = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tbl, path, compression="zstd", use_dictionary=True, write_statistics=False)


def build_pack(W, out, seed=C.SEED + 1):
    rng = np.random.default_rng(seed)
    os.makedirs(out, exist_ok=True)
    P, X, inv, pay, holds, agy, settle, T = W["P"], W["X"], W["inv"], W["pay"], W["holds"], W["agy"], W["settle"], W["T"]
    plate = P.plate.values; state = P.state.values
    W["_pay_idx"] = {}
    for k, d, a in zip(pay.inv_no.values, pay.posted.values, pay.amount.values):
        W["_pay_idx"].setdefault(k, []).append((d, a))

    # ---------------------------------------------------------------- invoice lines
    key = inv.set_index(["pi", "kind", "ym"]).inv_no
    X = X.assign(inv_no=[key[(a, b, c)] for a, b, c in zip(X.pi, X.kind, X.ym)])
    L = pd.DataFrame(dict(invoice_no=X.inv_no.values, plate=plate[X.pi.values], plate_state=state[X.pi.values],
                          crossed_at=X.ts.dt.floor("ms").values, plaza=X.plaza.values, direction=X.dir.values,
                          lane=X.lane.values, axles=X.axles.values.astype("int16"),
                          toll_class=np.array([CLASS[a] for a in X.axles.values], dtype="int16"), toll=X.toll.values))
    L = L.sort_values(["invoice_no", "crossed_at"], kind="mergesort").reset_index(drop=True)
    L.insert(0, "line_id", np.arange(5_310_000, 5_310_000 + len(L)))
    write_parquet(L, os.path.join(out, C.F_LINES))

    # ---------------------------------------------------------------- payments as the export carries them
    pay = pay.copy()
    ref = {}
    pay = pay[pay.posted <= C.EXPORT - TD(days=3)]
    pay = pay.sort_values(["posted", "inv_no"], kind="mergesort").reset_index(drop=True)
    pay.insert(0, "payment_id", ["P%07d" % (2_418_000 + i * 3 + int(rng.integers(0, 3))) for i in range(len(pay))])
    pay = pay.rename(columns={"inv_no": "invoice_no", "posted": "posted_on"})
    pay["posted_on"] = [d.isoformat() for d in pay.posted_on]
    pay.to_csv(os.path.join(out, C.F_PAY), index=False, lineterminator="\n")

    # ---------------------------------------------------------------- invoices, status as at 31 October 2026
    asof = C.ASOF
    p_asof = W["pay"][W["pay"].posted <= asof].groupby("inv_no").amount.sum()
    h = holds.set_index("inv_no"); a = agy.set_index("inv_no")
    rows = []
    for r in inv.itertuples():
        I = r.issue
        age = (asof - I).days
        paid = p_asof.get(r.inv_no, 0.0)
        late = r.late if age > 35 else 0.0
        coll = 0.0
        if r.inv_no in a.index and a.at[r.inv_no, "placed"] <= asof:
            coll = round((r.toll + r.fee + late) * C.AGENCY_PCT, 2)
        bal = r.toll + r.fee + late + coll
        if paid >= bal - 0.005 and paid > 0:
            st = "PAID"
        elif r.inv_no in a.index and a.at[r.inv_no, "placed"] <= asof:
            st = "RETURNED" if (a.at[r.inv_no, "status"] == "RETURNED UNCOLLECTED" and a.at[r.inv_no, "closed"] <= asof) else "AT AGENCY"
        elif r.inv_no in h.index and h.at[r.inv_no, "requested"] <= asof and h.at[r.inv_no, "response"] == "HOLD PLACED":
            st = "DMV HOLD"
        else:
            st = "OPEN"
        rows.append([r.inv_no, "TOLL-BY-MAIL" if r.kind == "TBM" else "VIOLATION", plate[r.pi], state[r.pi], I.isoformat(),
                     (I + TD(days=30)).isoformat(), int(r.n), round(r.toll, 2), r.fee, late, coll, st])
    IV = pd.DataFrame(rows, columns=["invoice_no", "invoice_type", "plate", "plate_state", "issued_on", "due_on", "crossings",
                                     "toll_billed", "invoice_fee", "late_fee", "collection_fee", "status"])
    IV.to_csv(os.path.join(out, C.F_INV), index=False, lineterminator="\n")

    # ---------------------------------------------------------------- the division's hold returns
    H = holds[holds.requested <= asof].copy()
    H = H.sort_values(["requested", "inv_no"], kind="mergesort").reset_index(drop=True)
    H.insert(0, "request_id", ["DMV-%s-%05d" % (d.strftime("%y%m%d"), i % 100000) for i, d in enumerate(H.requested)])
    H["reg_expires"] = [e.strftime("%m/%Y") if isinstance(e, D) else "" for e in H.reg_expires]
    rel_ok = [isinstance(x, D) and x <= asof for x in H.released]
    H["released_on"] = [x.isoformat() if ok else "" for x, ok in zip(H.released, rel_ok)]
    H["release_reason"] = [rr if ok else "" for rr, ok in zip(H.release_reason, rel_ok)]
    H["requested_on"] = [d.isoformat() for d in H.requested]
    H = H[["request_id", "inv_no", "plate", "requested_on", "response", "reg_expires", "released_on", "release_reason"]].rename(columns={"inv_no": "invoice_no"})
    H.to_csv(os.path.join(out, C.F_MVD), index=False, lineterminator="\n")

    # ---------------------------------------------------------------- the agency's placements
    A = agy[agy.placed <= asof].copy()
    A["status_"] = [("AT AGENCY" if c > asof else s) for s, c in zip(A.status, A.closed)]
    A["closed_on"] = [c.isoformat() if c <= asof else "" for c in A.closed]
    A["placed_on"] = [d.isoformat() for d in A.placed]
    A = A.sort_values(["placed", "inv_no"], kind="mergesort")
    A = A[["inv_no", "agency", "placed_on", "status_", "closed_on"]].rename(columns={"inv_no": "invoice_no", "status_": "status"})
    A.to_csv(os.path.join(out, C.F_AGY), index=False, lineterminator="\n")

    # ---------------------------------------------------------------- commercial MarrowPass postings
    TT = pd.DataFrame(dict(account_no=T.account.values.astype("int32"), tag_id=["MP%07d" % (3_100_000 + f) for f in T.fi],
                           plate=T.plate.values, plate_state=T.state.values, posted_at=T.ts.dt.floor("ms").values,
                           plaza=T.plaza.values, direction=T.dir.values, lane=T.lane.values,
                           axles_detected=T.axles.values.astype("int16"),
                           toll_class=np.array([CLASS[a] for a in T.axles.values], dtype="int16"), toll=T.class_toll.values))
    TT.insert(0, "posting_id", np.arange(88_000_000, 88_000_000 + len(TT)))
    write_parquet(TT, os.path.join(out, C.F_TAG))
    return dict(L=L, IV=IV, pay=pay, H=H, A=A, TT=TT)


def _paid_by(W, inv_no, day):
    p = W["_pay_idx"].get(inv_no)
    if p is None:
        return False
    return sum(a for d, a in p if d <= day) > 0


def lanes():
    rows = []
    for pz in C.PLAZAS:
        for d in C.DIRS:
            for l in C.ETC_LANES:
                rows.append([pz, C.PLAZA_NAME[pz], C.MILEPOST[pz], d, "%s-%s-%s" % (pz, d, l), l, "EXPRESS", "MarrowPass only, highway speed"])
            for l in C.BOOTH_LANES:
                rows.append([pz, C.PLAZA_NAME[pz], C.MILEPOST[pz], d, "%s-%s-%s" % (pz, d, l), l, "BOOTH",
                             "cash, card or MarrowPass; camera-billed when the booth is closed"])
    return pd.DataFrame(rows, columns=["plaza", "plaza_name", "milepost", "direction", "lane_ref", "lane", "lane_type", "payment"])


def traffic(W, rng):
    """Monthly transactions by plaza, direction, hour of day and payment (a distractor: the traffic team's counts)."""
    rows = []
    months = [(y, m) for y in (2025, 2026) for m in range(1, 13) if D(y, m, 1) <= D(2026, 9, 1)]
    from world import HOUR_W
    for (y, m) in months:
        for pz, base in zip(C.PLAZAS, [21800, 24300, 14600]):
            for d in C.DIRS:
                for hh in range(24):
                    n = base * 30.4 * HOUR_W[hh] * (1 + 0.06 * np.sin((m - 4) / 12 * 2 * np.pi)) * rng.lognormal(0, 0.03)
                    tag = n * (0.79 + 0.004 * (y - 2025) * 12 + rng.normal(0, 0.004))
                    night = (hh >= 23 or hh < 5) and D(y, m, 1) >= D(2025, 3, 1)
                    rest = n - tag
                    cam = rest * 0.97 if night else rest * 0.012
                    cash = rest - cam
                    rows.append(["%04d-%02d" % (y, m), pz, d, hh, int(round(tag)), int(round(cash)), int(round(cam))])
    return pd.DataFrame(rows, columns=["month", "plaza", "direction", "hour", "marrowpass", "cash_or_card", "camera_billed"])


def image_review(W, rng):
    """Captures by month and lane type through image review (a distractor: the call works on invoiceable toll)."""
    X = W["X"]
    g = X.assign(month=X.ts.dt.strftime("%Y-%m"), lt=np.where(X.lane.isin(C.ETC_LANES), "EXPRESS", "BOOTH")).groupby(["month", "lt"]).size()
    rows = []
    for (mo, lt), n in g.items():
        unread = int(round(n * (0.034 if lt == "BOOTH" else 0.046) * rng.lognormal(0, 0.05)))
        noowner = int(round(n * (0.021 if lt == "BOOTH" else 0.029) * rng.lognormal(0, 0.06)))
        rows.append([mo, lt, int(n) + unread + noowner, unread, noowner, int(n)])
    return pd.DataFrame(rows, columns=["capture_month", "lane_type", "captures", "plate_unreadable", "no_owner_found", "invoiced"])
