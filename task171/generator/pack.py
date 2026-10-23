"""Cut task171's evidence pack (target/) from the clean truth in world.py. One RNG stream for the export layer,
separate from the truth's, so the mess never moves the truth."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import common as C

D = dt.date
EXPORT_TS = dt.datetime(2026, 11, 20, 7, 42, 0)


def read_dates(cycle):
    """read date of each billing month for a billing cycle: the cycle's day, moved off weekends to Monday"""
    out = []
    for (y, m) in [(2023, 2)] + C.MONTHS:
        d = D(y, m, C.CYCLE_DAY[cycle])
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        out.append(d)
    return out          # index 0 is the February 2023 read, index i+1 closes billing month i


def luhn(s):
    tot = 0
    for i, ch in enumerate(reversed(s)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        tot += d
    return str((10 - tot % 10) % 10)


class Ids:
    def __init__(self, W, rng):
        prem, svc = W["prem"], W["svc"]
        dnum = {d: i + 1 for i, d in enumerate(C.DISTRICTS)}
        grid = rng.integers(10, 980, len(prem))
        seq = rng.permutation(len(prem)) % 9000 + 1000
        self.loc = np.array(["%02d-%03d-%04d" % (dnum[d] * 7 + 3, g, s) for d, g, s in zip(prem.district, grid, seq)])
        # service accounts numbered in order of opening, with gaps from non-residential and cancelled accounts
        order = np.lexsort((svc.prem.values, svc.open_i.values))
        base = 30_118_402 + np.cumsum(rng.integers(1, 9, len(svc)))
        acct = np.empty(len(svc), object)
        for k, i in enumerate(order):
            b = str(base[k])
            acct[i] = b + luhn(b)
        self.acct = acct
        mem = 100_000 + rng.permutation(len(svc) + 4000)[:len(svc)] * 3 + rng.integers(0, 3, len(svc))
        self.member = np.array(["%06d" % m for m in mem])
        # members holding two residential services at once (a farm dwelling, a second home): about 2.5 per cent
        alive24 = np.where((svc.open_i.values < C.MIDX[(2024, 1)]) & (svc.close_i.fillna(99).values >= C.MIDX[(2025, 6)]))[0]
        dist = svc.district.values
        town = alive24[np.isin(dist[alive24], ["Brisco Bend", "Sedge Flats"])]
        rural = alive24[np.isin(dist[alive24], ["Kessel Mill", "Pike Ridge", "Tamsey"])]
        a_ = list(rng.choice(town, 900, replace=False))       # the member's home in town
        b_ = list(rng.choice(rural, 900, replace=False))      # a farm dwelling or a second house out of town
        self.second = {}
        for a, b in zip(a_, b_):
            self.member[b] = self.member[a]
            self.second[b] = a
        mtype = rng.random(len(prem)) < 0.62
        self.meter0 = np.array([("31" if t else "52") + "%07d" % rng.integers(0, 10 ** 7) for t in mtype])


def build_pack(W, out, seed=C.SEED + 1):
    rng = np.random.default_rng(seed)
    os.makedirs(out, exist_ok=True)
    prem, svc, use = W["prem"], W["svc"], W["use"]
    nm = len(C.MONTHS)
    ids = Ids(W, rng)
    rdates = {c: read_dates(c) for c in (1, 2, 3, 4)}
    cyc = prem.cycle.values[svc.prem.values]

    # service open and close dates
    open_d, close_d = [], []
    for i, r in enumerate(svc.itertuples()):
        rd = rdates[cyc[i]]
        if r.open_i < 0:
            y = int(rng.integers(1994, 2023)); m = int(rng.integers(1, 13)); day = int(rng.integers(1, 29))
            od = D(y, m, day)
            if od >= D(2023, 2, 1):
                od = D(2022, 11, day)
        else:
            od = rd[r.open_i]
        open_d.append(od)
        close_d.append(rd[int(r.close_i) + 1] if not pd.isna(r.close_i) else None)
    svc = svc.assign(open_d=open_d, close_d=close_d)

    # meters and exchanges (firmware programme in 2025, failed meters at other times)
    meter_of = ids.meter0.copy()
    exch = []
    prog = rng.random(len(prem)) < 0.071
    fail = (~prog) & (rng.random(len(prem)) < 0.012)
    emonth = np.where(prog, rng.integers(C.MIDX[(2025, 2)], C.MIDX[(2025, 11)] + 1, len(prem)),
                      rng.integers(1, nm - 1, len(prem)))
    new_meter = np.array(["58" + "%07d" % rng.integers(0, 10 ** 7) for _ in range(len(prem))])
    for p in np.where(prog | fail)[0]:
        rd = rdates[prem.cycle.iat[p]]
        m = emonth[p]
        a, b = rd[m], rd[m + 1]
        x = a + dt.timedelta(days=int(rng.integers(3, max(4, (b - a).days - 2))))
        exch.append((ids.loc[p], ids.meter0[p], new_meter[p], x, "AMI firmware programme" if prog[p] else
                     rng.choice(["Failed register", "Damaged by storm", "Communication failure"]), m))
    exch_by_prem = {e[0]: e for e in exch}

    # AMI rows
    rows = []
    on_tou = W["on_tou"]
    asof_tou = svc.on_tou_asof.values
    for i in range(len(svc)):
        p = svc.prem.iat[i]
        rd = rdates[cyc[i]]
        o = max(int(svc.open_i.iat[i]), 0)
        c = int(svc.close_i.iat[i]) if not pd.isna(svc.close_i.iat[i]) else nm - 1
        loc = ids.loc[p]
        ex = exch_by_prem.get(loc)
        for m in range(o, c + 1):
            k = use[i, m]
            if k.sum() <= 0:
                continue
            rf = rd[m] if not (m == o and svc.open_i.iat[i] >= 0) else svc.open_d.iat[i]
            rt = rd[m + 1]
            est = rng.random() < 0.014
            if ex is not None and ex[5] == m:
                f = (ex[3] - rf).days / max((rt - rf).days, 1)
                rows.append((ex[1], ids.acct[i], m, rf, ex[3], *(k * f), "EST" if est else "ACT"))
                rows.append((ex[2], ids.acct[i], m, ex[3], rt, *(k * (1 - f)), "ACT"))
                continue
            mt = ex[2] if (ex is not None and m > ex[5]) else ids.meter0[p]
            if est and asof_tou[i] and on_tou[i, m]:
                # a TOU service's estimated month is re-collected from the meter later; both rows stay in the extract
                e = k * rng.lognormal(0, 0.10) * rng.lognormal(0, 0.06, 4)
                rows.append((mt, ids.acct[i], m, rf, rt, *e, "EST"))
                rows.append((mt, ids.acct[i], m, rf, rt, *k, "ACT"))
            else:
                rows.append((mt, ids.acct[i], m, rf, rt, *k, "EST" if est else "ACT"))
    ami = pd.DataFrame(rows, columns=["meter_no", "service_acct", "mi", "read_from", "read_to"] + C.PERIODS + ["read_type"])
    ami.insert(2, "bill_month", ["%04d-%02d" % C.MONTHS[m] for m in ami.mi])
    ami = ami.drop(columns="mi")
    for col in C.PERIODS:
        ami[col] = ami[col].round(1)
    # extract order: by billing month and meter, rows in the order the MDM loaded them (a re-collected read after the
    # estimate it replaces)
    ami["seq"] = np.arange(len(ami))
    ami = ami.sort_values(["bill_month", "meter_no", "seq"], kind="mergesort").drop(columns="seq").reset_index(drop=True)
    tbl = pa.Table.from_pandas(ami, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tbl, os.path.join(out, C.F_AMI), compression="zstd", use_dictionary=True, write_statistics=False)

    # service accounts
    heatname = np.where(svc.heat.values, np.where(rng.random(len(svc)) < 0.7, "Electric - heat pump", "Electric - resistance"),
                        rng.choice(["Natural gas", "Propane", "Wood or other"], len(svc), p=[0.38, 0.47, 0.15]))
    sa = pd.DataFrame(dict(service_acct=ids.acct, membership_no=ids.member, location_no=ids.loc[svc.prem.values],
                           district=svc.district.values, premise_type=svc.ptype.str.replace("multi-unit", "multi-unit (2-8 units)").values,
                           primary_heat=heatname, billing_cycle=cyc,
                           service_start=[d.strftime("%m/%d/%Y") for d in svc.open_d],
                           service_end=[d.strftime("%m/%d/%Y") if d else "" for d in svc.close_d],
                           status=np.where(svc.close_i.isna(), "Active", "Final")))
    sa = sa.sort_values("service_acct").reset_index(drop=True)
    sa.to_csv(os.path.join(out, C.F_SVC), index=False, lineterminator="\n")

    # rate assignments: the CIS writes R-1 rows; the TOU module writes R-TOU rows (re-issued at the 2026 price change,
    # never end-dated by the account-closure batch)
    rr = []
    jan26 = C.MIDX[(2026, 1)]
    for i in range(len(svc)):
        rd = rdates[cyc[i]]
        a = ids.acct[i]
        st = svc.open_d.iat[i]
        ts, te = int(svc.tou_start.iat[i]), int(svc.tou_end.iat[i])
        cl = svc.close_d.iat[i]
        if ts < 0:
            rr.append((a, "R-1", st, cl))
            continue
        on = rd[ts + 1]                   # the read that closes billing month ts
        rr.append((a, "R-1", st, on - dt.timedelta(days=1)))
        off = rd[te] if te >= 0 else None
        segs = [(on, (off - dt.timedelta(days=1)) if off else None)]
        # since the CIS upgrade of June 15, 2025 the TOU module re-writes a member's R-TOU row whenever the account is
        # maintained (budget billing, paperless, a payment-plan change): a new row from the read after the change
        s0, e0 = segs[0]
        lo = max(s0, D(2025, 6, 15))
        hi = min([x for x in (e0, cl, D(2026, 10, 31)) if x is not None])
        if hi > lo and rng.random() < 0.42:
            k = 1 + int(rng.random() < 0.25)
            days = sorted({lo + dt.timedelta(days=int(rng.integers(1, max(2, (hi - lo).days)))) for _ in range(k)})
            cuts = []
            for dd in days:
                rr_ = [x for x in rd if x > dd]
                if rr_ and rr_[0] < hi:
                    cuts.append(rr_[0])
            cuts = sorted(set(cuts))
            if cuts:
                segs = []
                prev = s0
                for cdd in cuts:
                    segs.append((prev, cdd - dt.timedelta(days=1))); prev = cdd
                segs.append((prev, e0))
        for s, e in segs:
            if cl is not None and s > cl:
                continue
            rr.append((a, "R-TOU", s, e))      # open-ended when the service closed on R-TOU
        if off is not None and (cl is None or off <= cl):
            rr.append((a, "R-1", off, cl))
    rate = pd.DataFrame(rr, columns=["service_acct", "rate_code", "eff_from", "eff_to"])
    rate["eff_from"] = [d.isoformat() for d in rate.eff_from]
    rate["eff_to"] = [d.isoformat() if d else "" for d in rate.eff_to]
    rate = rate.sort_values(["service_acct", "eff_from"], kind="mergesort").reset_index(drop=True)
    rate.to_csv(os.path.join(out, C.F_RATE), index=False, lineterminator="\n")

    ex = pd.DataFrame([(e[0], e[1], e[2], e[3].isoformat(), e[4]) for e in exch],
                      columns=["location_no", "removed_meter", "installed_meter", "exchange_date", "reason"])
    ex = ex.sort_values(["exchange_date", "location_no"]).reset_index(drop=True)
    ex.to_csv(os.path.join(out, C.F_EXCH), index=False, lineterminator="\n")
    svc = svc.assign(acct=ids.acct, loc=ids.loc[svc.prem.values], cyc=cyc)
    return dict(svc=svc, ami=ami, rate=rate, exch=ex, sa=sa, rdates=rdates, ids=ids)
