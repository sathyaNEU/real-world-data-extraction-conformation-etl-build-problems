"""Ask B's records: the maintenance management system's defect reports (MMS export), from the clean truth.

Operators write a defect card when they pull a car in; the card names the car and the block. The yard clerk keys the
cards into the MMS on the next business morning (now and then a day later), so each card's record carries only the
time it was entered. Mechanics' inspection findings are entered the day they are found and name no block. Ask B counts
the operator cards on the service day they were written, which only the card's car and block against the cars that ran
each block that day recover (a recorded date for the event date): the yard's block sheets name each block's pull-out
car or cars, and on a Foundry block whose car was bad-ordered in service the spare that took the block over is on no
sheet, only in the AVL log (the true key elsewhere).

Every car that ran a block writes cards at the same rates: the pull-out car, a two-car block's trailing car, and on a
swapped block both the bad-ordered car (until it pulled in) and the spare (after it pulled out). A card is written only
where its car and block date it uniquely: its car ran its block on no other day in the week before the card was keyed
and not on the keying day itself, and its car carries no other card for the same defect that day.

defect_reports(T, Rr, seed) -> (mms, truth, release_wos): the export rows, one truth row per operator card (service
day, line, group, weekday service), and the work-order numbers of the depot's bad-order repairs (in the swaps' order).
Its own random streams, drawn after every other record, so the main call's records and ask A's are unchanged by it.
"""
import numpy as np
import pandas as pd
import world as W
import simulate as S

GROUPS = {
    "Brakes": (0.052, ["Brakes grabbing", "Friction brake slow to release", "Sander inoperative", "Track brake fault light",
                       "Brake cylinder pressure low", "Parking brake not releasing"]),
    "Doors": (0.070, ["Door slow to close", "Door obstruction alarm", "Door chime inoperative", "Sensitive edge fault",
                      "Door will not lock out", "Bridge plate fault"]),
    "Propulsion": (0.030, ["Traction cut-out", "Jerky acceleration", "Propulsion fault light"]),
    "HVAC": (0.038, ["AC not cooling", "Heater inoperative", "Cab fan inoperative"]),
    "Lights and horn": (0.036, ["Headlight out", "Gong weak", "Marker light out", "Interior lights flickering"]),
    "Body and interior": (0.030, ["Seat damaged", "Window cracked", "Stanchion loose", "Graffiti"]),
    "Communications": (0.042, ["PA inaudible", "Radio static", "Destination sign blank", "Stop announcement wrong"]),
}
INSPECT_P = 0.035          # inspection findings per car per business day
LATE_P = 0.07              # cards keyed a business day late
EXPORTED = "2026-11-02 11:00"   # the MMS extract was run on the morning of 2 November
UNIQUE_DAYS = 7            # a card's car ran its block on exactly one service day in the week before keying


def _business_days(start, end):
    hol = {pd.Timestamp(h) for h in W.OBS_HOLIDAYS}
    return [d for d in pd.date_range(start, end) if d.weekday() < 5 and d not in hol]


def operating(T, Rr):
    """Every (service day, block, car) the cars actually ran: each block's pull-out car or cars from the yard's sheets,
    and on a swapped Foundry block the spare that took it over (the bad-ordered car is the sheet's pull-out car)."""
    C = T["consists"].copy()
    C["date"] = pd.to_datetime(C["date"])
    rows = []
    for r in C.itertuples():
        rows.append((r.date, r.block, int(r.lead_car), "pull-out"))
        if not pd.isna(r.trail_car):
            rows.append((r.date, r.block, int(r.trail_car), "trailing"))
    for s in Rr["swaps"].itertuples():
        rows.append((pd.Timestamp(s.date), s.block, int(s.spare), "spare"))
    return pd.DataFrame(rows, columns=["sday", "block", "car", "role"])


def defect_reports(T, Rr, seed=W.SEED):
    rng = np.random.default_rng(seed + 29)
    SW = Rr["swaps"]
    Y = operating(T, Rr)
    seen = {k: set(g["sday"]) for k, g in Y.groupby(["car", "block"])}    # the cars that ran each block, by day

    bdays = _business_days(W.OBS_START, "2026-11-30")
    bidx = pd.DatetimeIndex(bdays)
    dtype = {d: S.day_type(d, W.OBS_HOLIDAYS) for d in pd.date_range(W.OBS_START, W.OBS_END)}

    cards = []
    written = set()
    for r in Y.itertuples():
        summer = 1.8 if r.sday.month in (6, 7, 8) else 1.0
        for grp, (lam, texts) in GROUPS.items():
            n = rng.poisson(lam * (summer if grp == "HVAC" else 1.0))
            for _ in range(n):
                k = int(np.searchsorted(bidx, r.sday, side="right"))
                if rng.random() < LATE_P:
                    k += 1
                keyed_day = bidx[k]
                t = keyed_day + pd.Timedelta(minutes=int(rng.integers(6 * 60 + 35, 9 * 60 + 40)))
                text = str(rng.choice(texts))
                lo = keyed_day - pd.Timedelta(days=UNIQUE_DAYS)
                days = seen[(r.car, r.block)]
                hits = [d for d in days if lo <= d < keyed_day]
                if len(hits) != 1 or keyed_day in days:
                    continue      # only a card its car and block date uniquely is kept, never on its keying day (C1)
                if (r.car, r.sday, text) in written:
                    continue      # one card per defect per car per day (the day's later report of it is not keyed)
                written.add((r.car, r.sday, text))
                cards.append(dict(created=t, source="Operator card", car=r.car, block=r.block, group=grp, defect=text,
                                  sday=r.sday, weekday=dtype[r.sday] == "weekday", role=r.role))
    K = pd.DataFrame(cards)
    K = K[K["created"] < pd.Timestamp(EXPORTED)].reset_index(drop=True)     # cards keyed after the export are not in it

    # mechanics' inspection findings, keyed the day they are found
    ins = []
    cars = W.CARS["J"] + W.CARS["F"]
    for d in _business_days(W.OBS_START, W.OBS_END):
        for c in cars:
            if rng.random() < INSPECT_P:
                grp = str(rng.choice(list(GROUPS)))
                ins.append(dict(created=d + pd.Timedelta(minutes=int(rng.integers(10 * 60, 15 * 60 + 30))), source="Inspection",
                                car=c, block="", group=grp, defect=str(rng.choice(GROUPS[grp][1]))))
    I = pd.DataFrame(ins)
    M = pd.concat([K.drop(columns=["sday", "weekday", "role"]), I], ignore_index=True)
    M = M.sort_values(["created", "car"], kind="mergesort").reset_index(drop=True)
    # one work-order series for the whole agency (the buses, the facilities and the streetcar's other work take the
    # numbers between), the Foundry depot's bad-order repairs included, numbered in the order each was opened; its own
    # random stream, so nothing above moves
    opened = pd.to_datetime(SW["t_first"]) - pd.Timedelta(minutes=17)
    seq = pd.DataFrame({"t": list(M["created"]) + list(opened), "kind": ["m"] * len(M) + ["r"] * len(SW),
                        "i": list(range(len(M))) + list(range(len(SW)))})
    seq = seq.sort_values(["t", "kind", "i"], kind="mergesort").reset_index(drop=True)
    num = 712040 + np.cumsum(1 + np.random.default_rng(seed + 31).poisson(3.4, len(seq)))
    wo_m = dict(zip(seq.loc[seq["kind"] == "m", "i"], num[(seq["kind"] == "m").values]))
    wo_r = dict(zip(seq.loc[seq["kind"] == "r", "i"], num[(seq["kind"] == "r").values]))
    M["wo_no"] = ["WO-%06d" % wo_m[i] for i in range(len(M))]
    M["reported"] = M["created"].dt.normalize()
    truth = K.copy()
    truth["line"] = np.where(truth["car"] < 120, "Juniper", "Foundry")
    truth["bucket"] = np.where(truth["group"].isin(["Brakes", "Doors"]), truth["group"], "All other")
    return M, truth, ["WO-%06d" % wo_r[i] for i in range(len(SW))]


def ask_b_truth(truth):
    t = truth[truth["weekday"] & (truth["sday"] >= pd.Timestamp(W.OBS_START)) & (truth["sday"] <= pd.Timestamp(W.OBS_END))]
    c = t.groupby(["line", "bucket"]).size()
    return {ln: {b: int(c.get((ln, b), 0)) for b in ("Brakes", "Doors", "All other")} for ln in ("Juniper", "Foundry")}
