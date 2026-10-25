"""The asks from the pack. Ask A: the condominium class on Rule 18-7 (sales, level, COD, PRD). Ask B: what the Board of
Review took off the 2025 roll in each market area (parcels reduced, value taken off). Each has the golden handling
and the stops a competent response reaches on the way."""
import numpy as np
import pandas as pd

import common as K
from analysis import AS_OF

CERT_2025 = pd.Timestamp(K.CERT_2025)


def _study_stats(d):
    r = (d["av26"] / d["price_jan26"]).to_numpy()
    m = float(np.median(r))
    cod = 100.0 * float(np.mean(np.abs(r - m))) / m
    agg = float(d["av26"].sum() / d["price_jan26"].sum())
    prd = float(np.mean(r)) / agg
    return dict(n=int(len(r)), level=m, cod=cod, prd=prd, agg=agg)


def ask_a(pk, mode="golden"):
    """mode: golden (a deed or a permit dated before a renumbering or combination took effect is read through the
    change log, a sale set aside where the unit was combined, or its permit work finaled, after the deed); noperm (the
    golden reading of the deeds, no permit set aside); rawperm (the golden reading of the deeds, each permit's number
    read as a 2026 identifier); raw (every number read as a 2026 identifier); every (the change log applied to every
    number it lists, whatever the date)."""
    r26 = pk.roll26.set_index("parcel_id")
    q = pk.deeds[pk.deeds["validation_code"] == "Q"].copy()
    ch = pk.changes[pk.changes["change_type"].isin(["RENUMBER", "COMBINE"])]
    ch = ch[ch["old_parcel_no"].map(lambda p: p[:3] >= "200")]
    m_new = dict(zip(ch["old_parcel_no"], ch["new_parcel_id"]))
    m_eff = dict(zip(ch["old_parcel_no"], ch["effective_date"]))
    m_type = dict(zip(ch["old_parcel_no"], ch["change_type"]))
    dated = mode in ("golden", "noperm", "rawperm")

    def read(p, when, raw):
        if p in m_new and not raw and (mode == "every" or (dated and when < m_eff[p])):
            return m_new[p], m_type[p] == "COMBINE"
        return p.replace("-", "") + "0", False

    pid, drop = [], []
    for _, d in q.iterrows():
        target, comb = read(d["parcel_no"], d["deed_date"], mode == "raw")
        pid.append(target)
        drop.append(comb and dated)
    q["pid_a"] = pid
    q["drop"] = drop
    q = q[~q["drop"]]
    q = q[q["pid_a"].map(lambda x: x in r26.index and r26.at[x, "class_code"] == "R2")].copy()
    if mode != "noperm":
        fin = pk.permits.dropna(subset=["final_inspection_date"])
        fin = fin[fin["parcel_no"].map(lambda p: p[:3] >= "200")]
        raw = mode in ("raw", "rawperm")
        last = {}
        for _, p in fin.iterrows():
            t, _ = read(p["parcel_no"], p["issued_date"], raw)
            last[t] = max(last.get(t, p["final_inspection_date"]), p["final_inspection_date"])
        after = q["pid_a"].map(last)
        q = q[~(after.notna() & (after > q["deed_date"]) & (after < AS_OF))].copy()
    q["price_jan26"] = q["consideration"] * pk.index_carry(q["deed_date"])
    q["av26"] = q["pid_a"].map(r26["total_assessed_value"])
    return _study_stats(q)


def ask_b(pk, mode="golden"):
    """mode: golden (appeals of the 2025 roll: heard after the roll was certified and appealed from its certified
    value; each parcel's last decision in its case); parcel (the same, each parcel's last decision whatever its case);
    case (the 2025 roll's appeals at each case's last decision, a petition's parcels taken as one); all (every hearing in
    the 2025 log, each parcel's last decision in its case); allcase (every hearing, each case's last decision); rows (the
    2025 roll's appeals, every REDUCED row summed); first (the 2025 roll's appeals at each parcel's first decision)."""
    b = pk.bor.copy()
    r25 = pk.roll25.set_index("Parcel No.")
    b["cert_value"] = b["parcel_no"].map(r25["Total Assessed"])
    b["area"] = b["parcel_no"].map(r25["market_area"])
    if mode not in ("all", "allcase"):
        b = b[(b["hearing_date"] >= CERT_2025) & (b["value_before"] == b["cert_value"])]
    heard = b[b["hearing_date"].notna()].sort_values(["case_no", "hearing_date", "parcel_no"], kind="mergesort")
    if mode == "rows":
        last = heard
    elif mode == "first":
        last = heard.groupby(["case_no", "parcel_no"]).head(1)
    elif mode in ("case", "allcase"):
        last = heard.groupby("case_no").tail(1)
    elif mode == "parcel":
        last = heard.sort_values(["parcel_no", "hearing_date"], kind="mergesort").groupby("parcel_no").tail(1)
    else:
        last = heard.groupby(["case_no", "parcel_no"]).tail(1)
    red = last[last["decision"] == "REDUCED"].copy()
    red["off"] = red["value_before"] - red["value_after"]
    out = {}
    for a, _ in K.AREAS:
        x = red[red["area"] == a]
        out[a] = dict(parcels=int(x["parcel_no"].nunique()), off=int(x["off"].sum()))
    return out
