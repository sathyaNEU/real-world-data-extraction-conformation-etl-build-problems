"""Every assertion the build makes, grouped as the design note's assertion plan groups them.
Each check is named; the build fails on the first false one and prints the full list when green."""
from __future__ import annotations

import itertools
import math
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

import meters as M
from analysis import AS_OF, DECKS, GROWTH, RATIO, Analysis, ks, merge_charges
from common import (CITY_HOLIDAYS, GRID_T0, HOLIDAYS, QH, TZ, iso_local, load_curve, lt_date, nearest5, up5)
from world import (BACKFED_POS, BACKFEED, GATEWAY_B_END, GATEWAY_B_POS, MIGRATION, REISSUED_POS, RESTATED_POS)

LOG = []


def ck(name, cond, detail=""):
    LOG.append((name, bool(cond), detail))
    if not cond:
        raise AssertionError(f"{name}: {detail}")


def near(x, y, tol=1e-6):
    return abs(x - y) <= tol


def dist_half(x, step=1.0):
    """Distance of x from the nearest rounding edge of a grid of the given step."""
    f = (x / step) % 1.0
    return abs(f - 0.5) * step


# ====================================================================================== main call
TARGET_MONTHLY = [109.088, 67.872, 97.888, 90.272, 84.896, 79.072, 72.128, 74.816, 87.136, 94.080, 103.264, 129.136]
TARGET_MONTHLY_X = [125.216, 148.512, 114.016, 114.464, 109.088, 103.264, 88.256, 99.008, 119.392, 126.336, 119.392,
                    129.136]


def main_call(a: Analysis, r: dict) -> dict:
    out = {}
    ans = GROWTH * r["percar"]["peak"]
    out["answer"] = ans
    ck("A01 answer 129.136 kW unrounded", near(ans, 129.136, 1e-6), ans)
    ck("A02 files 130 to the nearest 5 kW and 130 rounded up", nearest5(ans) == 130 and up5(ans) == 130,
       (nearest5(ans), up5(ans)))
    ck("A03 1.636 kW above the 127.5 edge, 0.864 below 130", near(ans - 127.5, 1.636, 1e-6) and near(130 - ans, 0.864, 1e-6))
    t = r["percar"]["at"]
    ck("A04 binding quarter-hour 12:00 on 8 December 2026", iso_local(t) == "2026-12-08T12:00:00-08:00", iso_local(t))
    ld = a.loads["percar"]
    j = (t - GRID_T0) // QH
    tot = ld["CCN"] + ld["CCS"]
    ck("A05 the 11:45 quarter-hour equals the binding one and 12:15 is lower",
       near(tot[j - 1], tot[j], 1e-6) and tot[j + 1] < tot[j] - 0.5, (tot[j - 1], tot[j], tot[j + 1]))
    n, s = ld["CCN"][j], ld["CCS"][j]
    out["split_unscaled"] = (n, s)
    out["split"] = (GROWTH * n, GROWTH * s)
    ck("A06 North 74.0 and South 41.3 kW unscaled at the binding quarter-hour", near(n, 74.0, 1e-6) and near(s, 41.3, 1e-6),
       (n, s))
    ck("A07 North over South between 1.7 and 1.9", 1.7 <= n / s <= 1.9, n / s)
    ck("A08 each deck's own per-car maximum falls in the binding quarter-hour",
       all(r["deck_own"][d][1] == t for d in DECKS), {d: iso_local(r["deck_own"][d][1]) for d in DECKS})
    mon = [GROWTH * r["monthly_percar"][m][0] for m in range(1, 13)]
    out["monthly"] = mon
    ck("A09 the twelve monthly per-car figures equal their targets",
       all(near(x, y, 1e-6) for x, y in zip(mon, TARGET_MONTHLY)), mon)
    ck("A10 every monthly figure at least 0.2 kW from a half-kW edge, all distinct at whole kW",
       all(dist_half(x) >= 0.2 for x in mon) and len({round(x) for x in mon}) == 12, [round(dist_half(x), 3) for x in mon])
    ck("A11 runner-up month at most 0.90 x the binding month", sorted(mon)[-2] <= 0.90 * max(mon), sorted(mon)[-2] / max(mon))
    mshift = [GROWTH * r["monthly_percar_shift"][m][0] for m in range(1, 13)]
    ck("A12 stamps read as interval ends return every monthly figure", all(near(x, y, 1e-6) for x, y in zip(mon, mshift)))
    # rungs
    out["rung0"] = r["rung0"]["filed"]
    ck("A13 rung 0: both registers 105.6 in the highest month, 412.16 kW",
       near(r["rung0"]["registers"], 211.2, 1e-9) and near(r["rung0"]["filed"], 412.16, 1e-6), r["rung0"])
    regs = a.w.log["max_kw"].dropna()
    ck("A14 no maximum-demand register ever exceeds 105.6 kW", float(regs.max()) <= 105.6 + 1e-9, float(regs.max()))
    out["rung1"] = r["rung1"]["filed"]
    ck("A15 rung 1: closed billing maximum 158.4 kW, 309.12 filed",
       near(r["rung1"]["closed"], 158.4, 1e-6) and near(r["rung1"]["filed"], 309.12, 1e-6), r["rung1"])
    out["rung2"] = r["r115"]["filed"]
    ck("A16 rung 2: 103.04 kW set on 10 June 2026 by eight sessions at 11.5 kW",
       near(r["r115"]["filed"], 103.04, 1e-6) and iso_local(r["r115"]["at"]).startswith("2026-06-10"),
       (r["r115"], iso_local(r["r115"]["at"])))
    out["rung3"] = r["r110"]["filed"]
    ck("A17 rung 3: 98.56 kW on the same June day", near(r["r110"]["filed"], 98.56, 1e-6)
       and iso_local(r["r110"]["at"]).startswith("2026-06-10"))
    x = GROWTH * r["percar26"]["peak"]
    out["rung4"] = x
    ck("A18 rung 4, each session's car on its own date: 148.512 kW at 12:00 on 17 February 2026, files 150 both ways",
       near(x, 148.512, 1e-6) and iso_local(r["percar26"]["at"]) == "2026-02-17T12:00:00-08:00"
       and nearest5(x) == 150 and up5(x) == 150, (x, iso_local(r["percar26"]["at"])))
    ldx = a.loads["percar26"]
    jx = (r["percar26"]["at"] - GRID_T0) // QH
    out["rung4_split"] = (GROWTH * ldx["CCN"][jx], GROWTH * ldx["CCS"][jx])
    monx = [GROWTH * r["monthly_percar26"][m][0] for m in range(1, 13)]
    out["rung4_monthly"] = monx
    ck("A19 rung 4: North 102.8 and South 29.8 kW unscaled, twelve monthly figures on target",
       near(ldx["CCN"][jx], 102.8, 1e-6) and near(ldx["CCS"][jx], 29.8, 1e-6)
       and all(near(u, v, 1e-6) for u, v in zip(monx, TARGET_MONTHLY_X)), (ldx["CCN"][jx], ldx["CCS"][jx], monx))
    ck("A20 rung 4 differs from the answer at whole kW in eleven of twelve months (December alone agrees)",
       [m + 1 for m in range(12) if round(monx[m]) == round(mon[m])] == [12])
    months = {k: datetime.fromtimestamp(r[k]["at"], TZ).month for k in ("percar", "percar26", "r115", "r110", "draw66")}
    ck("A21 month that sets each rung: answer December, own-date cars and the closed maximum February, rungs 2 and 3 "
       "June", months == {"percar": 12, "percar26": 2, "r115": 6, "r110": 6, "draw66": 2}, months)
    # the natural path replays settlement records: rungs 2 and 3 agree, rungs 4 and 5 do not
    rec = r["records"]
    out["rec"] = {k: v["filed"] for k, v in rec.items()}
    ck("A40 record by record, rungs 2 and 3 are unchanged (103.04 and 98.56): no record the run closed charges into "
       "their binding quarter-hour", near(rec["r115"]["filed"], r["r115"]["filed"], 1e-6)
       and near(rec["r110"]["filed"], r["r110"]["filed"], 1e-6), out["rec"])
    r4, r5 = rec["percar26"]["filed"], rec["percar"]["filed"]
    out["rung4_rec"], out["rung5_rec"] = r4, r5
    out["rung5_rec_at"] = iso_local(rec["percar"]["at"])
    out["rung5_rec_monthly"] = [GROWTH * rec["percar"]["monthly"][m][0] for m in range(1, 13)]
    out["rung4_rec_monthly"] = [GROWTH * rec["percar26"]["monthly"][m][0] for m in range(1, 13)]
    ldr = a.rec_loads["percar"]
    jr = (rec["percar"]["at"] - GRID_T0) // QH
    out["rung5_rec_split"] = (GROWTH * ldr["CCN"][jr], GROWTH * ldr["CCS"][jr])
    ck("A41 rung 5, the contract-year car on every settlement record: at least 15 per cent above the answer, 155 kW to "
       "the nearest 5 kW (160 rounded up), set at 12:00 on 8 December 2026",
       r5 >= 1.15 * ans and nearest5(r5) == 155 and up5(r5) == 160
       and out["rung5_rec_at"] == "2026-12-08T12:00:00-08:00", (r5, out["rung5_rec_at"]))
    ck("A42 rung 5 differs from the answer at whole kW in every contract month",
       all(round(u) != round(v) for u, v in zip(out["rung5_rec_monthly"], mon)), out["rung5_rec_monthly"])
    print("     rung 4 and rung 5 record by record:", round(r4, 3), iso_local(rec["percar26"]["at"]), round(r5, 3),
          out["rung5_rec_at"], [round(x, 1) for x in out["rung5_rec_split"]])
    ck("A43 rung 4 record by record: own-date cars, at least 20 per cent above the answer and filed apart from rung 5",
       r4 >= 1.20 * ans and nearest5(r4) not in (nearest5(r5), 130, 150), (r4, iso_local(rec["percar26"]["at"])))
    ck("A22 rung figures all different when filed (410, 310, 105, 100, rung 4, 155, 130)",
       len({nearest5(v) for v in (out["rung0"], out["rung1"], out["rung2"], out["rung3"], r4, r5, ans)}) == 7
       and [nearest5(v) for v in (out["rung0"], out["rung1"], out["rung2"], out["rung3"], r5, ans)]
       == [410, 310, 105, 100, 155, 130])
    # grid cells
    closed = r["rung1"]["closed"]
    cells = {
        "draw 6.6, billing hours": GROWTH * r["draw66"]["peak"],
        "rating ratio, billing hours": r["rung1"]["filed"],
        "fleet-average ratio, 2026 vehicles": r["ratio_favg"]["filed"],
        "fleet-average ratio, contract-year vehicles": closed * GROWTH * a.favg27 / 6.6,
        "replay at 11.5": r["r115"]["filed"],
        "replay at 11.0": r["r110"]["filed"],
        "replay at the fleet average, 2026 vehicles": GROWTH * r["favg"]["peak"],
        "replay at each deck's average, 2026 vehicles": GROWTH * r["davg"]["peak"],
        "replay at the fleet average, contract-year vehicles": GROWTH * r["favg27"]["peak"],
        "replay at each deck's average, contract-year vehicles": GROWTH * r["davg27"]["peak"],
        "per car, each session's car on its own date": x,
        "per car, growth left off": r["percar"]["peak"],
        "utility planners' sizing": 225.0,
        "per car on North, rating on South": GROWTH * r["N_percar_S_rating"]["peak"],
        "per car on South, rating on North": GROWTH * r["S_percar_N_rating"]["peak"],
        "ratings only for the county pool cars": GROWTH * r["pool_rating"]["peak"],
        "per car, contract-year car, each settlement record replayed": rec["percar"]["filed"],
        "per car, own-date car, each settlement record replayed": rec["percar26"]["filed"],
    }
    for k, v in r["allhours"].items():
        cells[f"all hours, {k}"] = GROWTH * v
    out["cells"] = cells
    ck("A23 draw 6.6 kW cell 177.408", near(cells["draw 6.6, billing hours"], 177.408, 1e-6))
    ck("A24 growth left off 115.3", near(cells["per car, growth left off"], 115.3, 1e-6))
    ck("A25 fleet-average replay on 2026 vehicles at least 40 per cent above the answer",
       cells["replay at the fleet average, 2026 vehicles"] >= 1.4 * ans, cells["replay at the fleet average, 2026 vehicles"])
    ck("A26 deck-average replay on 2026 vehicles at least 10 per cent below",
       cells["replay at each deck's average, 2026 vehicles"] <= 0.90 * ans)
    worst = min(abs(v / ans - 1) for v in cells.values())
    ck("A27 every single-error cell at least 10 per cent from the answer", worst >= 0.10, worst)
    for k in ("per car on North, rating on South", "per car on South, rating on North",
              "ratings only for the county pool cars", "replay at the fleet average, contract-year vehicles",
              "replay at each deck's average, contract-year vehicles"):
        ck(f"A28 partial cell at least 15 per cent away: {k}", abs(cells[k] / ans - 1) >= 0.15, cells[k])
    ck("A29 every all-hours cell at least 40 per cent above", all(v >= 1.4 * ans for k, v in cells.items()
                                                                   if k.startswith("all hours")))
    two = {"own-date cars and growth left off": r["percar26"]["peak"],
           "draw 6.6 and growth left off": r["draw66"]["peak"],
           "deck averages on 2026 vehicles and growth left off": r["davg"]["peak"],
           "fleet average on 2026 vehicles and growth left off": r["favg"]["peak"],
           "replay at 11.5 with the 6.6 kW units' ratio": r["r115"]["peak"] * GROWTH * 6.6 / 11.5,
           "settlement records replayed and growth left off": rec["percar"]["peak"]}
    out["two_error"] = two
    nearest_two = min(two, key=lambda k: abs(two[k] / ans - 1))
    ck("A30 nearest two-error cell: own-date cars with growth left off, 132.6 kW, files 135 not 130, its two "
       "violations opposite in sign", nearest_two == "own-date cars and growth left off"
       and near(two[nearest_two], 132.6, 1e-6) and nearest5(two[nearest_two]) == 135 and up5(two[nearest_two]) == 135
       and x > ans > r["percar"]["peak"], (nearest_two, two[nearest_two]))
    near_pairs = {k: v for k, v in two.items() if abs(v / ans - 1) < 0.10}
    ck("A31 every two-error cell under 10 per cent from the answer is two violations of opposite sign and files "
       "neither 130 nor anything rounding up to it", set(near_pairs) <= {"own-date cars and growth left off",
                                                                         "settlement records replayed and growth left off"}
       and all(nearest5(v) != 130 and up5(v) != 130 for v in near_pairs.values())
       and rec["percar"]["filed"] > ans > r["percar"]["peak"], two)
    ck("A32 the utility planners' figure 225 kW, gap 95 kW", up5(32 * 11.5 * 0.6) == 225 and 225 - nearest5(ans) == 95,
       32 * 11.5 * 0.6)
    # convergent readings
    conv = {}
    conv["decks' own maxima summed"] = GROWTH * (r["deck_own"]["CCN"][0] + r["deck_own"]["CCS"][0])
    full = a.deck_charges.copy()
    full["car27"] = a.car_by_join(full, as_of=AS_OF)
    ld36 = a.load(full, np.minimum(11.5, full["car27"]))
    conv["all 36 months"] = GROWTH * max(a.annual(ld36, year=y)[0] for y in (2024, 2025, 2026))
    for name, asof in (("vehicles on each permit's latest check (energization, 1 April 2027)", date(2027, 4, 1)),
                       ("vehicles as of the council vote (16 February 2027)", date(2027, 2, 16))):
        s2 = a.pop26.copy()
        s2["car27"] = a.car_by_join(s2, as_of=asof)
        conv[name] = GROWTH * a.annual(a.load(s2, np.minimum(11.5, s2["car27"])))[0]
    out["convergent"] = conv
    for k, v in conv.items():
        ck(f"A33 convergent reading: {k}", near(v, ans, 1e-6), v)
    return out


# ====================================================================================== the renewal
def renewal(a: Analysis) -> dict:
    """The January 2027 renewal: what changed, where the record shows it, and that the closed record cannot."""
    w = a.w
    out = {}
    changed = sorted(w.veh["changed_2027"])
    pv = w.veh["pveh"]
    permits = w.veh["permits"].set_index("permit_no")
    new = pv[pv["permit_no"].isin(changed) & (pv["from"] >= date(2027, 1, 1))]
    old = pv[pv["permit_no"].isin(changed) & (pv["to"] < date(2027, 1, 31)) & (pv["to"] >= date(2026, 12, 31))]
    ck("R01 eighteen county permits renewed onto 2023 Bolt EVs (11.0 kW) from 2020 Bolt EVs (7.2 kW)",
       len(changed) == 18 and len(new) == 18 and len(old) == 18
       and set(permits.loc[changed, "holder"]) == {"Larch County Fleet Services"}
       and set(new["year"]) == {2023} and set(new["rating"]) == {11.0} and set(old["year"]) == {2020}
       and set(old["rating"]) == {7.2}, (len(changed), len(new), len(old)))
    ch = w.veh["checks"]
    jan = ch[ch["checked_on"] >= date(2027, 1, 1)]
    ck("R02 every renewal check row is dated 5 to 15 January 2027, before the as-of date, one per active permit",
       jan["checked_on"].between(date(2027, 1, 5), date(2027, 1, 15)).all() and jan["permit_no"].is_unique
       and set(jan["permit_no"]) == set(permits.index[permits["status"] == "ACTIVE"]), (len(jan), jan["checked_on"].max()))
    moved = sorted(set(jan.loc[jan["vin"].isin(new["vin"]), "permit_no"]))
    other = [p for p in jan["permit_no"] if p not in changed]
    prev_vin = {p: ch[(ch["permit_no"] == p) & (ch["checked_on"] < date(2027, 1, 1))].sort_values("checked_on")["vin"].iloc[-1]
                for p in other}
    ck("R03 no other permit changed vehicle at the January 2027 renewal",
       moved == changed and all(jan.set_index("permit_no").loc[p, "vin"] == v for p, v in prev_vin.items()))
    p26 = a.pop26
    diff = p26[p26["car"] != p26["car27"]]
    ck("R04 the session-date and contract-year joins differ exactly on the renewed permits' sessions",
       set(diff["permit_no"]) <= set(changed) and len(diff) == int(p26["permit_no"].isin(changed).sum())
       and (diff["car"] == 7.2).all() and (diff["car27"] == 11.0).all(), len(diff))
    out["sessions_changed"] = len(diff)
    ck("R05 the closed record cannot see the renewal: every 2026 session of a renewed permit was by its 2020 car, "
       "and the renewal is dated after the last 2026 session", (p26.loc[p26["permit_no"].isin(changed), "car"] == 7.2).all()
       and jan["checked_on"].min() > max(p26["day"]))
    bind = {m: d for d, tg in w.cal.items() if tg[0] == "bind" for m in [tg[1]]}
    pooled = {}
    for m, d in sorted(bind.items()):
        day = p26[(p26["day"] == d) & p26["role"].str.startswith("long")]
        pooled[m] = (int(day["permit_no"].isin(changed).sum()), int((day["garage"] == "CCN").sum()))
    out["renewed_long_sessions"] = pooled
    ck("R06 the December binding day carries no renewed car; February's carries ten of its fourteen North long sessions",
       pooled[12][0] == 0 and pooled[2] == (10, 14), pooled)
    v27 = a.veh27
    out["shares27"] = (int((v27["rating"] <= 7.7).sum()), len(v27))
    ck("R07 contract-year fleet: 39 of 73 permit vehicles at 7.2 to 7.7 kW", out["shares27"] == (39, 73), out["shares27"])
    return out


# ====================================================================================== the settlement run's pairs
def charges(a: Analysis) -> dict:
    """A charge still delivering energy when the daily settlement run reaches its garage is closed there and carried on
    as a new record. What links the two, what the closed record cannot see, and what reproduces the statements."""
    w = a.w
    rows = w.rows
    led = rows[rows["in_ledger"] & rows["true_row"] & ~rows["redelivered"]].copy()
    led["who"] = led["permit_no"].where(led["permit_no"] != "", led["fleet_card"])
    f1 = led[led["frag"] == 1].set_index("row")
    f2 = led[led["frag"] == 2].set_index("row")
    out = {"pairs": len(f1), "pairs_deck_2026": int(((f1["garage"].isin(DECKS)) & (f1["day"] >= date(2026, 1, 1))).sum())}
    same = (set(f1.index) == set(f2.index))
    g2 = f2.loc[f1.index]
    ck("S01 every record the run closed pairs with exactly one record the charge carried on in: same station, same permit "
       "or card, the second starting the second the first ends", same and len(f1) > 1000
       and (f1["plug_out"].to_numpy() == g2["start"].to_numpy()).all()
       and (f1["station_id"].to_numpy() == g2["station_id"].to_numpy()).all()
       and (f1["who"].to_numpy() == g2["who"].to_numpy()).all(), out)
    loc = pd.to_datetime(f1["plug_out"], unit="s", utc=True).dt.tz_convert(TZ)
    mins = loc.dt.hour * 60 + loc.dt.minute + loc.dt.second / 60
    inst = f1.groupby(["garage", "day"])["plug_out"].nunique()
    ck("S02 the run closes records between 10:00 and 10:07 local time, at one instant per garage per day",
       bool(mins.between(600.5, 607).all()) and int(inst.max()) == 1, (float(mins.min()), float(mins.max())))
    m = merge_charges(led)
    gen = w.sessions.loc[m["row"].to_numpy()]
    ck("S03 joining every pair end to start reproduces the charges as generated: start, energy and plug-out",
       (m["start"].to_numpy() == gen["start"].to_numpy()).all()
       and np.abs(m["energy"].to_numpy() - gen["energy"].to_numpy()).max() < 0.0005
       and (m["plug_out"].to_numpy() == gen["plug_out"].to_numpy()).all())
    # nothing else at the station touches a pair: no other record ends where the second starts or starts where the first
    # ends, and no record overlaps either
    st = led.sort_values(["station_id", "start"])
    sid, s0, s1, rr = (st["station_id"].to_numpy(), st["start"].to_numpy(np.int64), st["plug_out"].to_numpy(np.int64),
                       st["row"].to_numpy())
    same_st = sid[1:] == sid[:-1]
    touch = same_st & (s0[1:] == s1[:-1])
    overlap = same_st & (s0[1:] < s1[:-1])
    ck("S04 every zero gap at a station is a pair of one charge, and no two records at a station overlap",
       bool((rr[1:][touch] == rr[:-1][touch]).all()) and int(overlap.sum()) == 0 and int(touch.sum()) == len(f1),
       (int(touch.sum()), len(f1), int(overlap.sum())))
    gaps = []
    rep = led[led["frag"] == 0].sort_values("start")
    for (who, sta, d), g in rep[rep["who"] != ""].groupby(["who", "station_id", "day"]):
        if len(g) > 1:
            t0, t1 = g["start"].to_numpy(np.int64), g["plug_out"].to_numpy(np.int64)
            gaps.extend((t0[1:] - t1[:-1]).tolist())
    out["repeat_min_gap_min"] = min(gaps) / 60 if gaps else None
    ck("S05 a genuine unplug and replug never makes a zero gap: the shortest gap between two charges of one permit or "
       "card at one station on one day is 30 minutes or more", bool(gaps) and min(gaps) >= 1800, out["repeat_min_gap_min"])
    # the statements bill per charge: chains reproduce every permit-month, the rivals do not
    p26 = led[led["garage"].isin(DECKS) & (led["acct"] == "PERMIT") & (led["day"] >= date(2026, 1, 1))].copy()
    p26["period"] = [f"{d.year}-{d.month:02d}" for d in p26["day"]]
    billed = p26.groupby(["permit_no", "period"])["row"].nunique()
    rec = p26.groupby(["permit_no", "period"]).size()
    over = p26.groupby(["permit_no", "period"]).apply(lambda g: g.groupby(["station_id", "day"]).ngroups)
    chain = p26.groupby(["permit_no", "period"]).apply(
        lambda g: len(g) - int(g["start"].isin(set(g["plug_out"])).sum()))
    out["statements"] = {"permit_months": len(billed), "records_miss": int((rec != billed).sum()),
                         "overmerge_miss": int((over != billed).sum()), "chains_miss": int((chain != billed).sum())}
    ck("S06 the permit statements' charge counts: zero-gap chains reproduce every permit-month; records as charges miss "
       "most; merging every same-day record at a station misses the months with a genuine replug",
       out["statements"]["chains_miss"] == 0 and out["statements"]["records_miss"] >= 0.5 * len(billed)
       and out["statements"]["overmerge_miss"] >= 10, out["statements"])
    # what the closed record cannot see: at 6.6 kW the pair and the charge give the same readings and the same draw
    ck("S07 the closed record is blind to the pairs: every record's readings follow the constant draw from its own start, "
       "and the closed replay of records equals the closed replay of charges in every quarter-hour",
       np.allclose(sum(a.load(a.rec26, pd.Series(6.6, index=a.rec26.index)).values()),
                   sum(a.load(a.pop26, pd.Series(6.6, index=a.pop26.index)).values()), atol=1e-9))
    bind = [d for d, tg in w.cal.items() if tg[0] == "bind"]
    long26 = a.pop26[a.pop26["day"].isin(bind) & a.pop26["role"].str.startswith("long")]
    out["long_split_share"] = float((long26["n_rec"] == 2).mean())
    ck("S08 the run closes most of the binding days' long sessions (at least 70 per cent are pairs)",
       out["long_split_share"] >= 0.70, out["long_split_share"])
    return out


# ====================================================================================== corpus
def corpus(a: Analysis, r: dict) -> dict:
    out = {}
    w = a.w
    rows = a.deck_true
    cars = a.car_by_join(rows)
    cars27 = a.car_by_join(rows, as_of=AS_OF)
    ck("B01 every deck vehicle 2024-2026, and every contract-year vehicle, listed at 7.2 kW or more (the corpus is blind)",
       float(cars.min()) >= 7.2 and float(cars27.min()) >= 7.2, (float(cars.min()), float(cars27.min())))
    # closed replay under the rated rule and under the per-car rule: identical, reading by reading
    rd = w.rd.set_index("lrow")
    sub = rd.loc[rd.index.isin(rows.index)]
    ratio_rule = np.minimum(6.6, cars.reindex(sub.index).to_numpy())
    ck("B02 rated and per-car rules give the same closed draw on all 72 deck-months (zero differing readings)",
       bool((ratio_rule == 6.6).all()))
    # five-rule family over every closed session with an identified vehicle
    rows_id = w.rows[w.rows["true_row"] & ~w.rows["redelivered"] & w.rows["in_ledger"]
                     & ((w.rows["permit_no"] != "") | (w.rows["fleet_card"] != ""))]
    obs = observed_draw(w, rows_id)
    meas = obs.dropna()
    car_id = a.car_by_join(rows_id.loc[meas.index])
    unit = rows_id.loc[meas.index].apply(lambda x: 11.5 if x["position"] == "L-09" else 6.6, axis=1)
    rules = {"smaller of rating and onboard": np.minimum(unit, car_id), "rating": unit, "onboard": car_id,
             "0.957 x rating": (11.0 / 11.5) * unit, "11.0 on 11.5 kW units": unit.where(unit != 11.5, 11.0)}
    miss = {k: int((np.abs(v - meas) > 0.01).sum()) for k, v in rules.items()}
    out["family"] = {"measurable": len(meas), "misses": miss, "unmeasurable": int(obs.isna().sum())}
    lib = rows_id.loc[meas.index]["position"] == "L-09"
    vans = lib & (car_id == 11.0)
    pick = lib & (car_id == 19.2)
    ck("B03 family of five rules: the composition reproduces every measurable session", miss["smaller of rating and onboard"] == 0)
    ck("B04 rating misses every van session at the 11.5 kW unit", miss["rating"] == int(vans.sum()) and vans.sum() >= 400,
       (miss["rating"], int(vans.sum())))
    ck("B05 onboard rating misses every session on a 6.6 kW unit and the pickup", miss["onboard"] == int((~lib).sum() + pick.sum()))
    ck("B06 the 0.957 derate misses every 6.6 kW session", miss["0.957 x rating"] >= int((~lib).sum()))
    ck("B07 a fixed 11.0 kW on 11.5 kW units misses every pickup session", miss["11.0 on 11.5 kW units"] == int(pick.sum()))
    ck("B08 Library unit: every van at 11.0, every pickup at 11.5, at least ten pickup sessions",
       bool((meas[vans] == 11.0).all()) and bool((meas[pick] == 11.5).all()) and pick.sum() >= 10, int(pick.sum()))
    # twins
    p26 = a.pop26
    cnt = p26.groupby("garage").size()
    ck("B09 twin decks: 2026 session counts within 2 per cent", abs(cnt["CCN"] / cnt["CCS"] - 1) <= 0.02, cnt.to_dict())
    loc = pd.to_datetime(p26["start"], unit="s", utc=True).dt.tz_convert(TZ)
    arr = loc.dt.hour + loc.dt.minute / 60
    dwell = (p26["plug_out"] - p26["start"]) / 3600
    stats = {}
    for name, v in (("arrival", arr), ("dwell", dwell), ("energy", p26["energy"])):
        stats[name] = ks(v[p26["garage"] == "CCN"], v[p26["garage"] == "CCS"])
    out["twins_ks"] = stats
    ck("B10 twin decks: arrival, dwell and energy distributions matched (KS under 0.05)",
       all(x < 0.05 for x in stats.values()), stats)
    ld66 = a.loads["draw66"]
    j = (r["percar"]["at"] - GRID_T0) // QH
    ck("B12 twin decks: closed loads equal at the binding quarter-hour (66.0 kW each), 1.79 to 1 per car",
       near(ld66["CCN"][j], 66.0, 1e-6) and near(ld66["CCS"][j], 66.0, 1e-6))
    # fleet shares
    v26 = a.veh26
    slow = int((v26["rating"] <= 7.7).sum())
    north = v26[v26["deck"] == "North"]
    south = v26[v26["deck"] == "South"]
    pool = int((w.veh["permits"].set_index("permit_no").loc[north["permit_no"], "holder_type"] == "Agency").sum())
    out["shares"] = (slow, len(v26), pool, len(north), int((south["rating"] == 11.0).sum()), len(south))
    ck("B13 fleet shares in 2026: 57 of 73 at 7.2-7.7 kW, 44 of 48 North pool cars, 16 of 25 South at 11.0",
       (slow, len(v26), pool, len(north), int((south["rating"] == 11.0).sum()), len(south)) == (57, 73, 44, 48, 16, 25),
       out["shares"])
    ck("B14 averages: 2026 fleet 8.081, decks 7.242 / 9.692; contract-year fleet 9.018, decks 8.667 / 9.692",
       abs(a.favg - 8.081) < 0.0005 and abs(a.davg["CCN"] - 7.242) < 0.0005 and abs(a.davg["CCS"] - 9.692) < 0.0005
       and abs(a.favg27 - 9.018) < 0.0005 and abs(a.davg27["CCN"] - 8.667) < 0.0005
       and abs(a.davg27["CCS"] - 9.692) < 0.0005, (a.favg27, a.davg27))
    # departure, energy accounting
    slack = (p26["plug_out"] - (p26["start"] + p26["energy"] / 6.6 * 3600)) / 60
    out["departure_min_slack_min"] = float(slack.min())
    ck("B15 every 2026 deck session finished delivery before plug-out (no replay cut short)", float(slack.min()) >= 5)
    sums = w.rd.groupby("lrow")["kwh"].sum()
    diff = (sums - w.rows["energy"].reindex(sums.index)).abs()
    ck("B16 every session's readings sum to its delivered energy (0.001 kWh)", float(diff.max()) < 0.0005 + 1e-9,
       float(diff.max()))
    # peak days
    peak_days = [d for d, tg in w.cal.items() if tg[0] in ("bind", "rung2") and d.year == 2026]
    pd_rows = p26[p26["day"].isin(peak_days)]
    end_day = [datetime.fromtimestamp(int(x), TZ).date() for x in pd_rows["plug_out"]]
    ck("B17 no session on a peak day spans midnight", all(e == d for e, d in zip(end_day, pd_rows["day"])))
    late = 0.0
    for d in peak_days:
        i0 = (lt_date(d, 19) - GRID_T0) // QH
        i1 = (lt_date(d + timedelta(days=1)) - GRID_T0) // QH
        late = max(late, float((a.loads["percar"]["CCN"] + a.loads["percar"]["CCS"])[i0:i1].max()))
    ck("B18 no deck load after 19:00 on any peak day", late < 1e-9, late)
    # permits and vehicles
    pv = w.veh["pveh"]
    act = p26[p26["permit_no"] != ""]
    ok = all(((pv["permit_no"] == p) & (pv["from"] <= d) & (pv["to"] >= d)).any() for p, d in
             zip(act["permit_no"], act["day"]))
    ck("B19 every 2026 deck session's permit is active on its date", ok)
    ch = w.veh["checks"]
    c26 = ch[(ch["checked_on"] >= date(2025, 6, 1)) & (ch["checked_on"] < date(2027, 1, 1))]
    one = c26.groupby("permit_no")["vin"].nunique()
    overlap = any(((g["from"].to_numpy()[1:] <= g["to"].to_numpy()[:-1]).any()) for _, g in
                  pv.sort_values("from").groupby("permit_no"))
    ck("B20 one vehicle per permit at every date, none changed during 2026", int(one.max()) == 1 and not overlap)
    from world import reference_frame
    ref = reference_frame()
    hits = [int(((ref["make"].str.upper() == mk) & (ref["model"].str.upper() == md) & (ref["model_year_from"] <= yr)
                 & (ref["model_year_to"] >= yr) & ((ref["trim"] == "") | (ref["trim"].str.upper() == tr))).sum())
            for mk, md, tr, yr in zip(ch["make"], ch["model"], ch["trim"], ch["model_year"])]
    ck("B21 every checked vehicle resolves to exactly one reference row", set(hits) == {1}, sorted(set(hits)))
    ck("B22 every 2026 session settled by 10 January 2027",
       max(x for x in w.rows.loc[w.rows["in_ledger"], "settled_on"] if x is not None) <= date(2027, 1, 10))
    # tariff holidays
    hol_ok = True
    tot = a.loads["percar"]["CCN"] + a.loads["percar"]["CCS"]
    tot66 = a.loads["draw66"]["CCN"] + a.loads["draw66"]["CCS"]
    for d in sorted(HOLIDAYS):
        if d.year != 2026:
            continue
        i0 = (lt_date(d, 12) - GRID_T0) // QH
        i1 = (lt_date(d, 20) - GRID_T0) // QH
        mpk = r["monthly_percar"][d.month][0]
        hol_ok &= float(tot[i0:i1].max()) <= 0.2 * mpk and float(tot66[i0:i1].max()) <= 0.2 * mpk
    ck("B23 no tariff holiday carries deck load above 20 per cent of its month's peak", hol_ok)
    reg = w.register
    st26 = p26["station_id"].unique()
    raw = reg[reg["station_id"].isin(st26)].groupby("station_id").size()
    ck("B24 every 2026 deck identifier resolves to one register row under the raw and dated joins",
       len(raw) == len(st26) and int(raw.max()) == 1, (len(raw), len(st26)))
    return out


def observed_draw(w, rows):
    """kW of each session from a full quarter-hour of charging (NaN when it never charged a full one)."""
    rd = w.rd[w.rd["lrow"].isin(rows.index)]
    st = rows["start"].reindex(rd["lrow"]).to_numpy()
    en = rows["end_charge"].reindex(rd["lrow"]).to_numpy()
    full = (rd["interval_start"].to_numpy() >= st) & (rd["interval_start"].to_numpy() + QH <= en)
    f = rd[full]
    return (4 * f.groupby("lrow")["kwh"].max()).reindex(rows.index).round(3)


# ====================================================================================== B3
B3_SUBSET_DEVICES = ("F", "U", "Fx", "D7", "H6", "H2", "H3l", "H3f", "H1")


def _skip_b3(subset):
    """Alternatives that cannot be taken together: the first or the latest restated version; the fleet card charges
    left out or added at the processor's stamps read as local time."""
    return ("H3l" in subset and "H3f" in subset) or ("F" in subset and "Fx" in subset) or \
        ("F" in subset and "U" in subset)


def utc_misread(t):
    """The instant a reader gets by taking the fleet card file's UTC stamp as local time."""
    wall = datetime.fromtimestamp(int(t), timezone.utc).replace(tzinfo=None)
    return int(wall.replace(tzinfo=TZ).timestamp())


def b3_values(a: Analysis, sub=()):
    """The standard's 2025 record under a subset of mishandlings: F the fleet-card charges that settled outside the
    export before April 2025 left out, Fx the whole fleet card file added to the export (so the charges the export
    already carries count twice), D7 the raw identifier join, H6 gateway B left out, H2 the 1.09 revision, H3l/H3f
    the latest or first restated version, H1 re-deliveries kept."""
    w = a.w
    rows = w.rows
    base = rows["garage"].isin(DECKS)
    fleet_pre = rows["fleet_pre"].fillna(False).astype(bool)
    gwb = rows["gateway_b"].fillna(False).astype(bool)
    sel = base & rows["true_row"] & ~rows["redelivered"]
    if "H1" in sub:
        sel = sel | (base & rows["redelivered"])
    if "H3l" in sub or "H3f" in sub:
        restated = rows[base & rows["row"].isin(rows.loc[rows["version"] > 1, "row"])]
        pick = restated.groupby("row")["version"].max() if "H3l" in sub else restated.groupby("row")["version"].min()
        keep = restated[restated["version"] == restated["row"].map(pick)].index
        sel = sel & ~rows.index.isin(restated.index)
        sel = sel | rows.index.isin(keep)
    if "H6" in sub:
        sel = sel & ~gwb
    if "F" in sub:
        sel = sel & ~fleet_pre
    if "D7" in sub:
        sel = sel & ~(rows["position"].isin(REISSUED_POS) & (rows["day"] < MIGRATION))
    s = rows[sel]
    if "U" in sub:
        # the charges outside the export, added at the processor's UTC stamps read as local time
        s = s.copy()
        fp = s["fleet_pre"].fillna(False).astype(bool)
        shift = np.array([utc_misread(t) - int(t) for t in s.loc[fp, "start"]], dtype=np.float64)
        s.loc[fp, "start"] = s.loc[fp, "start"].to_numpy(np.float64) + shift
    if "Fx" in sub:
        dup = rows[base & rows["true_row"] & ~rows["redelivered"] & rows["in_ledger"] & (rows["acct"] == "FLEET")]
        if "D7" in sub:
            dup = dup[~(dup["position"].isin(REISSUED_POS) & (dup["day"] < MIGRATION))]
        s = pd.concat([s, dup.set_index(dup.index + 10_000_000)])
    ld = a.load(s, pd.Series(6.6, index=s.index))
    m24 = a.monthly(ld, year=2024)
    m25 = a.monthly(ld, year=2025)
    fac = 1.09 if "H2" in sub else 1.08
    F = {m: fac * m24[m][0] for m in range(1, 13)}
    A = {m: m25[m][0] for m in range(1, 13)}
    # the standard's accuracy record: stated whole-kW forecast less recorded whole-kW demand, over that demand
    NF = {m: int(math.floor(F[m] + 0.5)) for m in F}
    NA = {m: int(math.floor(A[m] + 0.5)) for m in A}
    miss = {m: 100 * (NF[m] - NA[m]) / NA[m] for m in range(1, 13)}
    return F, A, miss


def b3(a: Analysis):
    F, A, miss = b3_values(a)
    out = {"forecast": {m: int(math.floor(F[m] + 0.5)) for m in F}, "miss": {m: round(miss[m], 1) for m in miss},
           "F": F, "A": A, "miss_raw": miss}
    for m in range(1, 13):
        p = a.w.b3[m]
        ck(f"C01 back-test {m:02d}: forecast and actual reproduce the constructed levels",
           near(F[m], p["F"], 1e-6) and near(A[m], p["A"], 1e-6), (F[m], p["F"], A[m], p["A"]))
    vals = list(miss.values())
    ck("C02 golden misses within +-3.0 per cent, at least four each way",
       max(abs(v) for v in vals) <= 3.0 and sum(v > 0 for v in vals) >= 4 and sum(v < 0 for v in vals) >= 4, vals)
    fr = [x - math.floor(x) for x in list(F.values()) + list(A.values())]
    ck("C03 every forecast and every recorded demand sits 0.06 to 0.24 kW from a whole kW (mid-bin, never round)",
       all(0.06 - 1e-9 <= f <= 0.24 + 1e-9 or 0.76 - 1e-9 <= f <= 0.94 + 1e-9 for f in fr), [round(f, 3) for f in fr])
    ck("C04 every miss at least 0.015 inside its one-decimal bin and never an exact one-decimal share",
       all(0.004 <= abs(v - round(v, 1)) <= 0.035 for v in vals), vals)
    rows = a.w.rows
    s = rows[rows["garage"].isin(DECKS) & rows["true_row"] & ~rows["redelivered"]]
    ld = a.load(s, pd.Series(6.6, index=s.index))
    conv = all(near(a.monthly(ld, year=y)[m][0], a.monthly(ld, year=y, decks=("CCN",))[m][0]
                    + a.monthly(ld, year=y, decks=("CCS",))[m][0], 1e-6) for y in (2024, 2025) for m in range(1, 13))
    ck("C12 the decks' billing demand converges: coincident maximum equals the sum of each deck's own, all 24 months", conv)
    fp = rows[rows["fleet_pre"].fillna(False).astype(bool) & rows["garage"].isin(DECKS)]
    topf = fp[fp["role"] == "F"]
    rest = fp[fp["role"] != "F"]
    end_local = pd.to_datetime(rest["end_charge"], unit="s", utc=True).dt.tz_convert(TZ)
    ck("C13 the fleet-card charges at the decks outside the export all fall before 1 April 2025; the back-test top-ups "
       "among them sit on no reissued unit and on no unit while it reported through gateway B; the rest end before noon",
       len(topf) == 15 and (fp["day"] < MIGRATION).all() and not topf["position"].isin(REISSUED_POS).any()
       and not (topf["position"].isin(GATEWAY_B_POS) & (topf["day"] < GATEWAY_B_END)).any()
       and bool((end_local.dt.hour < 12).all()), (len(fp), len(topf)))
    means = []
    moves = {}
    for k in range(1, len(B3_SUBSET_DEVICES) + 1):
        for subset in itertools.combinations(B3_SUBSET_DEVICES, k):
            if _skip_b3(subset):
                continue
            F2, A2, m2 = b3_values(a, subset)
            v2 = list(m2.values())
            means.append(float(np.mean(v2)))
            ck(f"C05 naive misses two-signed under {'+'.join(subset)}", any(v > 0 for v in v2) and any(v < 0 for v in v2))
            if k == 1:
                moves[subset[0]] = ([m for m in F if math.floor(F2[m] + 0.5) != math.floor(F[m] + 0.5)],
                                    [m for m in F if round(m2[m], 1) != round(miss[m], 1)])
    out["subset_mean_range"] = (min(means), max(means))
    ck("C06 naive mean miss inside +-2.0 per cent under every subset of mishandlings",
       max(abs(x) for x in means) <= 2.0, out["subset_mean_range"])
    out["moves"] = moves
    allm = list(range(1, 13))
    ck("C07 the fleet-card charges left out move all twelve forecasts and every miss",
       moves["F"][0] == allm and moves["F"][1] == allm, moves["F"])
    ck("C16 the fleet card file's stamps read as local time put every charge outside the export about eight hours late, "
       "and all 24 figures land where leaving the charges out lands them", moves["U"] == moves["F"]
       and b3_values(a, ("U",))[2] == b3_values(a, ("F",))[2], (moves["U"], moves["F"]))
    ck("C08 the whole fleet card file added to the export moves the April to December misses it double counts",
       moves["Fx"][0] == [] and set(moves["Fx"][1]) <= set(range(4, 13)) and len(moves["Fx"][1]) >= 6, moves["Fx"])
    ck("C09 the reissued identifiers move all twelve forecasts", moves["D7"][0] == allm, moves["D7"])
    ck("C10 the 1.09 factor moves all twelve forecasts", moves["H2"][0] == allm, moves["H2"])
    ck("C11 gateway B moves January to April", moves["H6"] == ([1, 2, 3, 4], [1, 2, 3, 4]), moves["H6"])
    ck("C14 the restated versions move May to July", moves["H3l"][1] == [5, 6, 7] and moves["H3f"][1] == [5, 6, 7])
    ck("C15 the re-delivered batches move October and December", moves["H1"][1] == [10, 12], moves["H1"])
    return out


# ====================================================================================== B1
def b1(a: Analysis):
    w = a.w
    log = w.log
    books = w.books
    reads = sorted(set(log["read_date"]))
    r26 = [d for d in reads if d.year == 2026]
    out = {}

    def instant(d, panel, which="last"):
        rr = log[(log["read_date"] == d) & (log["panel"] == panel)]
        rr = rr.iloc[-1] if which == "last" else rr.iloc[0]
        h, m = map(int, rr["read_time"].split(":"))
        return M.meter_instant(d, h, m), M.civil_misread(d, h, m), float(rr["kwh"])

    gold = {}
    for panel in M.PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(r26, start=1):
            ta, ca, ra = instant(prev, panel)
            tb, cb, rb = instant(d, panel)
            v = (rb - ra) - books.sessions(panel, ta, tb)
            gold[(panel, k)] = v
            prev = d
    out["golden"] = {k: round(v) for k, v in gold.items()}
    out["golden_raw"] = gold
    fr = {k: v - math.floor(v) for k, v in gold.items()}
    ck("D01 B1 golden for all 24 readings, each 0.06 to 0.24 kWh from a whole kWh (mid-bin, never round)",
       all(0.06 <= f <= 0.24 or 0.76 <= f <= 0.94 for f in fr.values()), {k: round(f, 3) for k, f in fr.items()})
    ck("D02 B1 goldens are plausible lighting loads (positive, under 1,500 kWh)", all(0 < v < 1500 for v in gold.values()))
    # devices: each moves its readings by its stated minimum
    clk = {}
    for panel in M.PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(r26, start=1):
            ta, ca, ra = instant(prev, panel)
            tb, cb, rb = instant(d, panel)
            clk[(panel, k)] = (rb - ra) - books.sessions(panel, ca, cb) - gold[(panel, k)]
            prev = d
    moved = sorted(k for k, v in clk.items() if abs(v) >= 2.0)
    out["clock_moves"] = {k: round(v, 1) for k, v in clk.items()}
    ck("D03 the meter clock moves readings 3 to 11 on both panels, each by at least 2 kWh",
       moved == sorted((p, k) for p in M.PANELS for k in range(3, 12)), moved)
    ck("D04 the meter clock leaves readings 1, 2 and 12 alone", all(abs(clk[(p, k)]) < 1e-9 for p in M.PANELS for k in (1, 2, 12)))
    ctm = {}
    for panel in M.PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(r26, start=1):
            ta, _, _ = instant(prev, panel)
            tb, _, _ = instant(d, panel)
            ctm[(panel, k)] = books.sessions(panel, ta, tb) - books.sessions(panel, ta, tb, ct=True)
            prev = d
    out["courtesy_moves"] = {k: round(v, 1) for k, v in ctm.items()}
    ck("D15 the courtesy sessions, which are not in the settlement export, move every 2026 reading on both panels by at "
       "least 20 kWh when left out", all(v >= 20 for v in ctm.values()), min(ctm.values()))
    cr = w.rows[w.rows["courtesy"].fillna(False).astype(bool)]
    cl = a.load(cr, pd.Series(6.6, index=cr.index))
    inwin = float(((cl["CCN"] + cl["CCS"]) * a.bill).max())
    ck("D16 no courtesy session charges in any billing quarter-hour (weekends and Schedule 26 holidays only), and none is "
       "in the settlement export", inwin <= 0.0 and not cr["in_ledger"].any() and len(cr) >= 600,
       (inwin, len(cr)))
    ta, _, ra = instant(date(2025, 12, 31), "CP-N")
    rd_moves = {p: books.sessions(p, instant(date(2025, 12, 31), p)[0], instant(r26[0], p)[0], rdf=True)
                - books.sessions(p, instant(date(2025, 12, 31), p)[0], instant(r26[0], p)[0]) for p in M.PANELS}
    out["redelivery_moves"] = rd_moves
    ck("D05 the re-delivered December 2025 batch moves reading 1 on both panels by at least 5 kWh",
       all(v >= 5 for v in rd_moves.values()), rd_moves)
    bf = {}
    for k in (6, 7):
        d0, d1 = r26[k - 2], r26[k - 1]
        bf[k] = books.sessions("CP-N", instant(d0, "CP-N")[0], instant(d1, "CP-N")[0], bf=True) - \
            books.sessions("CP-N", instant(d0, "CP-N")[0], instant(d1, "CP-N")[0])
    out["backfeed_moves"] = bf
    ck("D06 the back-fed unit moves North readings 6 and 7 by at least 100 kWh in total and each by at least 20",
       sum(bf.values()) >= 100 and min(bf.values()) >= 20, bf)
    first = log[(log["read_date"] == date(2026, 12, 31)) & (log["panel"] == "CP-S")]
    ck("D07 the South panel was read twice on 31 December 2026", len(first) == 2)
    tf, _, rf = instant(date(2026, 12, 31), "CP-S", "first")
    tp, _, rp = instant(r26[10], "CP-S")
    v_first = (rf - rp) - books.sessions("CP-S", tp, tf)
    out["double_read_move"] = v_first - gold[("CP-S", 12)]
    ck("D08 keeping the first 31 December read moves South reading 12 by at least 20 kWh", abs(out["double_read_move"]) >= 20,
       out["double_read_move"])
    # every subset of mishandlings on a different whole kWh (check_reading re-run on the shipped log)
    times = {(d, pn): tuple(map(int, log[(log["read_date"] == d) & (log["panel"] == pn)].iloc[-1]["read_time"].split(":")))
             for d in reads for pn in M.PANELS}
    ck("D14 no read falls on a quarter-hour boundary", all(hm[1] % 15 for hm in times.values())
       and all(int(x.split(":")[1]) % 15 for x in log["read_time"]))
    nearest = 99999.0
    splits = {}
    for panel in M.PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(r26, start=1):
            ok, info = M.check_reading(books, times, prev, d, k, panel)
            ck(f"D09 {panel} reading {k:02d}: every subset of mishandlings lands on a different whole kWh (1.5 kWh away "
               f"unless it carries the pro rata split, 0.76 then)", ok, info)
            nearest = min(nearest, info["nearest_wrong"])
            splits[(panel, k)] = info["splits"]
            prev = d
    out["nearest_wrong"] = nearest
    out["split_moves"] = {k: {x: round(v, 2) for x, v in sp.items()} for k, sp in splits.items()}
    ck("D13 every split of the quarter-hour a read falls inside moves every reading: whole quarter-hours either way "
       "or to the nearest boundary by 1.5 kWh or more, pro rata by 0.76 kWh or more",
       all(abs(sp[x]) >= 1.5 for sp in splits.values() for x in ("qb", "qa", "qn"))
       and all(abs(sp["lin"]) >= 0.76 for sp in splits.values()),
       {x: min(abs(sp[x]) for sp in splits.values()) for x in M.SPLITS})
    # lazy path: calendar months, civil time, deck name, re-deliveries kept, repeats deduped, first read
    lazy = {}
    for panel in M.PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(r26, start=1):
            ta, ca, ra = instant(prev, panel)
            tb, cb, rb = instant(d, panel)
            if panel == "CP-S" and k == 12:
                rb = rf
            a0, a1 = M.month_start(2026, k), M.month_start(2026 + (k == 12), 1 if k == 12 else k + 1)
            lazy[(panel, k)] = (rb - ra) - books.sessions(panel, a0, a1, rdf=True, bf=True, dd=True, ct=True)
            prev = d
    ck("D10 the lazy path lands away from the golden on every reading",
       all(abs(lazy[k] - gold[k]) >= 1.5 for k in gold), min(abs(lazy[k] - gold[k]) for k in gold))
    out["lazy"] = {k: round(v) for k, v in lazy.items()}
    deck = w.rows[w.rows["garage"].isin(DECKS) & w.rows["true_row"] & ~w.rows["redelivered"]]
    pan = M.panel_of(deck)
    whole = {}
    for panel in M.PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(r26, start=1):
            ta, _, ra = instant(prev, panel)
            tb, _, rb = instant(d, panel)
            e = deck[(pan == panel) & (deck["start"] >= ta) & (deck["start"] < tb)]["energy"].sum()
            whole[(panel, k)] = (rb - ra) - e - gold[(panel, k)]
            prev = d
    out["whole_session_moves"] = {k: round(v, 1) for k, v in whole.items()}
    ck("D12 attributing whole sessions by plug-in time lands at least 1.5 kWh from the golden on every reading",
       all(abs(v) >= 1.5 for v in whole.values()), min(abs(v) for v in whole.values()))
    led = w.rows[w.rows["in_ledger"]]
    ck("D11 hygiene battery on the wrong path comes back clean: session_id plus version unique, every station joins",
       not led.duplicated(["session_id", "version"]).any() and led["station_id"].isin(w.register["station_id"]).all())
    return out


# ====================================================================================== separation, Gate G tests
def separation(a: Analysis, r: dict, ans: float):
    w = a.w
    p26 = a.pop26
    counts = {
        "re-delivered rows": int((w.rows["redelivered"] & w.rows["garage"].isin(DECKS)
                                  & (w.rows["day"] >= date(2026, 1, 1))).sum()),
        "restated versions": int(w.rows[(w.rows["version"] > 1) & (w.rows["day"] >= date(2026, 1, 1))].shape[0]),
        "gateway B rows": int(p26["gateway_b"].fillna(False).astype(bool).sum()),
        "fleet-card charges outside the export": int(p26["fleet_pre"].fillna(False).astype(bool).sum()),
        "reissued identifiers": int(p26["station_id"].isin(w.pos["reissued_id"].dropna().astype(int)).sum()),
        "rows outside the decks": int((~p26["garage"].isin(DECKS)).sum()),
        "rows outside the export": int((~p26["in_ledger"]).sum()),
        "courtesy sessions": int(p26["courtesy"].fillna(False).astype(bool).sum()),
    }
    ck("E01 zero device and zero hazard rows inside the main call's population", all(v == 0 for v in counts.values()), counts)

    def three(s):
        s = merge_charges(s)
        s["car"] = a.car_by_join(s)
        s["car27"] = a.car_by_join(s, as_of=AS_OF)
        return (GROWTH * a.annual(a.load(s, np.minimum(11.5, s["car27"])))[0],
                GROWTH * a.annual(a.load(s, np.minimum(11.5, s["car"])))[0],
                GROWTH * a.annual(a.load(s, pd.Series(11.5, index=s.index)))[0])
    ld = a.loads
    base = (GROWTH * a.annual(ld["percar"])[0], GROWTH * a.annual(ld["percar26"])[0], GROWTH * a.annual(ld["r115"])[0])
    repairs = {}
    rows = w.rows
    good = rows["true_row"] & ~rows["redelivered"] & rows["garage"].isin(DECKS)
    variants = {
        "gateway B merged": good,
        "fleet card file merged": good,
        "re-deliveries kept": (rows["true_row"] | rows["redelivered"]) & rows["garage"].isin(DECKS),
        "restated: latest version kept": good | (rows["version"] == 3),
        "identifiers by latest assignment": good & ~(rows["position"].isin(REISSUED_POS) & (rows["day"] < MIGRATION)),
    }
    for name, sel in variants.items():
        s = rows[sel & (rows["day"] >= date(2026, 1, 1)) & rows["in_ledger"]]
        v = three(s)
        repairs[name] = v
        ck(f"E02 clean-data test, {name}: the answer, rung 4 and rung 2 unchanged, all three apart",
           all(near(x, y, 1e-6) for x, y in zip(v, base)) and len({nearest5(x) for x in v}) == 3, v)
    other = rows[rows["in_ledger"] & rows["true_row"] & ~rows["redelivered"]
                 & rows["station_id"].isin(w.pos["reissued_id"].dropna().astype(int)) & (rows["day"] >= date(2026, 1, 1))]
    s = pd.concat([a.pop26.drop(columns=["car", "car27"]), merge_charges(other).assign(garage="CCN")])
    car27 = a.car_by_join(a.pop26, as_of=AS_OF).reindex(s.index).fillna(11.5)
    v_first = GROWTH * a.annual(a.load(s, np.minimum(11.5, car27)))[0]
    ck("E03 identifiers by first assignment leave the answer unchanged", near(v_first, base[0], 1e-6), v_first)
    # lens swap: the closed replay is identical under the rated rule and under both vehicle joins
    s = a.pop26
    closed = [a.load(s, np.minimum(6.6, x)) for x in (pd.Series(11.5, index=s.index), s["car"], s["car27"])]
    ck("E04 lens-swap test: the closed replay is identical under the rated rule and both vehicle joins, so rung 2, rung 4 "
       "and the answer differ only through the forward regime and the forward fleet",
       all(np.allclose(closed[0][d], c[d]) for c in closed[1:] for d in DECKS) and len({nearest5(x) for x in base}) == 3)
    real = a.car_by_join

    def forbidden(*_a, **_k):
        raise RuntimeError("audit touched the vehicle join")
    a.car_by_join = forbidden
    try:
        b3_values(a)
        ok = True
    except RuntimeError:
        ok = False
    finally:
        a.car_by_join = real
    ck("E05 decoupling: the back-test and the panel audit never read a vehicle, so neither vehicle join can move them", ok)
    return counts, repairs


def _instants(log, panel):
    lg = log[log["panel"] == panel]
    out = []
    for d in sorted(set(lg["read_date"])):
        rr = lg[lg["read_date"] == d].iloc[-1]
        out.append((d, M.meter_instant(d, *map(int, rr["read_time"].split(":")))))
    return out


def referee(a: Analysis):
    """Re-deliveries, restatements and the back-feed never touch a panel's all-hours maximum quarter-hour."""
    w = a.w
    books = w.books
    log = w.log
    res = {}
    for panel in M.PANELS:
        inst = _instants(log, panel)
        for which, kw in (("re-deliveries", dict(rdf=True)), ("back-feed", dict(bf=True))):
            naive = np.diff(books.c[(kw.get("rdf", False), kw.get("bf", False), False, False)][panel])
            gold = books.gold_qh[panel]
            light = books.light_raw[panel]
            for (d0, t0), (d1, t1) in zip(inst[:-1], inst[1:]):
                i0, i1 = (t0 - GRID_T0) // QH, (t1 - GRID_T0) // QH
                g = float((4 * (gold[i0:i1] + light[i0:i1])).max())
                nv = float((4 * (naive[i0:i1] + light[i0:i1])).max())
                if abs(g - nv) > 1e-6:
                    res[(panel, which, d1)] = (g, nv)
    ck("F01 re-deliveries and the back-feed never touch a panel's all-hours maximum quarter-hour", not res, res)
    off = []
    for panel in M.PANELS:
        lg = log[log["panel"] == panel].reset_index(drop=True)
        inst = [M.meter_instant(rr.read_date, *map(int, rr.read_time.split(":"))) for rr in lg.itertuples()]
        for i in range(1, len(lg)):
            i0, i1 = (inst[i - 1] - GRID_T0) // QH, (inst[i] - GRID_T0) // QH
            v = round(float((4 * books.gold_qh[panel][i0:i1]).max()) + 1e-9, 1)
            if abs(v - float(lg.loc[i, "max_kw"])) > 1e-9:
                off.append((panel, lg.loc[i, "read_date"], v, lg.loc[i, "max_kw"]))
            for t in (inst[i - 1], inst[i]):
                if not M.straddle_ok(books, panel, t):
                    off.append((panel, "straddle", t))
    ck("F03 every maximum-demand register in the log equals the sessions-only quarter-hour maximum (lights off), and "
       "no read splits a period's maximum quarter-hour", not off, off[:5])
    rows = w.rows
    rest = rows[rows["row"].isin(rows.loc[rows["version"] > 1, "row"]) & (rows["garage"] == "CCS")]
    acc = rest[rest["true_row"]]
    bad = []
    inst = _instants(log, "CP-S")
    for which in ("latest", "first"):
        pick = rest.groupby("row")["version"].max() if which == "latest" else rest.groupby("row")["version"].min()
        alt = rest[rest["version"] == rest["row"].map(pick)]
        delta = np.zeros_like(books.gold_qh["CP-S"])
        for idx, sign in ((alt.index, 1.0), (acc.index, -1.0)):
            rr = w.rd[w.rd["lrow"].isin(idx)]
            np.add.at(delta, ((rr["interval_start"].to_numpy() - GRID_T0) // QH), sign * rr["kwh"].to_numpy())
        for (d0, t0), (d1, t1) in zip(inst[:-1], inst[1:]):
            i0, i1 = (t0 - GRID_T0) // QH, (t1 - GRID_T0) // QH
            g = 4 * (books.gold_qh["CP-S"][i0:i1] + books.light_raw["CP-S"][i0:i1])
            n = g + 4 * delta[i0:i1]
            if abs(float(g.max()) - float(n.max())) > 1e-6:
                bad.append((which, d1, float(g.max()), float(n.max())))
    ck("F02 restated versions never change a South register, whichever version is kept", not bad, bad)
