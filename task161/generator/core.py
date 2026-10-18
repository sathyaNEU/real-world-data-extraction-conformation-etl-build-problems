"""task161 core: one call that builds the whole world in memory (truth, records, notices, ports).

pack.py writes target/ from this; golden.py, verify.py and cracker.py read target/ back. Before the
pack is cut, cracker.py can run on this directly.
"""
import datetime as dt
import numpy as np
import world as W
import sim
import records
import asks

ONE = dt.timedelta(days=1)


def tune_ports(receipts, manifest, la, lb):
    """The ports' figures are constructed: where the book's share (per cent, graded to three decimals) would
    sit within 0.00026 of a cell edge, or in a cell ending in zero (a share that reads as round), that month's
    Long Beach loaded inbound is moved (by well under one per cent) so the share sits between 0.00004 and
    0.00021 from the centre of its own cell, or of the next cell up when its own ends in zero. The book's TEU
    is computed first and never moved here."""
    LA = {k: la[i] for i, k in enumerate(asks.MONTHS_2026)}
    LB = {k: lb[i] for i, k in enumerate(asks.MONTHS_2026)}
    teu, share = asks.a2_golden(receipts, manifest, LA, LB, records.utc_to_pacific_date)
    rng = np.random.default_rng([W.SEED, 7006])
    for k in asks.MONTHS_2026:
        v = share[k]
        cell = round(v, 3)
        u = float(rng.uniform(0.00004, 0.00021))
        if round(cell * 1000) % 10 == 0:
            cell = round(cell + 0.001, 3)
            target = cell - u
        elif abs(v - cell) <= 0.00024:
            continue
        else:
            target = cell + (u if v > cell else -u)
        LB[k] = int(round(100.0 * teu[k] / target - LA[k]))
    return LA, LB


def fix_half_teu(receipts, manifest):
    """A month whose golden TEU ends in exactly .5 cannot be graded to the whole TEU: re-type one of that
    month's 45ft boxes as a 40ft high cube in the record (the box's pallets do not move). A month whose TEU
    rounds to a whole hundred reads as round: re-type four of its 40ft high cubes as 45ft boxes (one TEU)."""
    LA = {k: 1 for k in asks.MONTHS_2026}
    LB = {k: 1 for k in asks.MONTHS_2026}
    for _ in range(6):
        teu, _ = asks.a2_golden(receipts, manifest, LA, LB, records.utc_to_pacific_date)
        half = [k for k in asks.MONTHS_2026 if abs((teu[k] % 1.0) - 0.5) < 1e-9]
        round100 = [k for k in asks.MONTHS_2026 if int(round(teu[k])) % 100 == 0]
        if not half and not round100:
            return
        for k in half:
            for r in receipts:
                d = records.utc_to_pacific_date(r["received_at"])
                if (d.year, d.month) == k and r["type"] == "L5G1" and r.get("part") is None:
                    r["type"] = "45G1"
                    r["size"] = "40HC"
                    break
        for k in round100:
            n = 0
            for r in receipts:
                d = records.utc_to_pacific_date(r["received_at"])
                if (d.year, d.month) == k and r["type"] == "45G1" and r.get("part") is None:
                    r["type"] = "L5G1"
                    r["size"] = "45"
                    n += 1
                    if n == 4:
                        break


def build_world():
    T = sim.simulate()
    receipts, manifest = records.build_receipts(T)
    records.receipt_times(receipts, np.random.default_rng([W.SEED, 7003]))
    fix_half_teu(receipts, manifest)
    notices = records.notices(T, np.random.default_rng([W.SEED, 7005]))
    la, lb = records.port_statistics(None, np.random.default_rng([W.SEED, 7004]))
    rec_window = [r for r in receipts if r["day"] >= dt.date(2022, 9, 12)]
    LA, LB = tune_ports(rec_window, manifest, la, lb)
    split_asof = records.site_split(T, W.LAST_CLOSE)
    lpn = records.lpn_snapshot(T, receipts, {c: split_asof[c] for c in W.CURRENT},
                               np.random.default_rng([W.SEED, 7002]))
    return {"truth": T, "receipts": receipts, "manifest": manifest, "notices": notices, "LA": LA, "LB": LB,
            "split_asof": split_asof, "lpn": lpn}
