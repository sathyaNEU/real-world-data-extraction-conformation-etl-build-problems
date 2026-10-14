"""An independent read of the shipped pack: nothing from the generator but the file names. Recomputes the carried
figure, the claimant-feature counts and the ledger quarters from target/ and checks them against the goldens."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

CT = ZoneInfo("America/Chicago")
NQ = 40


def _q(ts):
    return ((ts.dt.year - 2017) * 4 + (ts.dt.month - 1) // 3).to_numpy()


def _local(s):
    return pd.to_datetime(s, utc=True, errors="coerce").dt.tz_convert(CT).dt.tz_localize(None)


def read(target):
    f = lambda n: os.path.join(target, n)
    arch = pd.read_csv(f("legacy_bi_claims_archive.csv"), dtype=str)
    arch["key"] = arch.CLM_NO + "-" + arch.FEAT_NO
    for c in ("LOSS_DT", "RPT_DT", "CLS_DT"):
        arch[c] = pd.to_datetime(arch[c], format="%m/%d/%Y")
    lpay = pd.read_csv(f("legacy_bi_payments_2017-2024.csv"), dtype=str)
    lpay["key"] = lpay.CLM_NO + "-" + lpay.FEAT_NO
    lpay["t"] = pd.to_datetime(lpay.TRANS_DT, format="%m/%d/%Y") + pd.Timedelta(hours=12)
    lpay["acc"] = pd.to_datetime(lpay.LOSS_DT, format="%m/%d/%Y")
    lpay["amt"] = lpay.AMOUNT.astype(float)
    reg = pd.read_csv(f("platform_bi_features_2027-01-06.csv"), dtype=str, keep_default_na=False)
    reg["acc"] = pd.to_datetime(reg.accident_date)
    reg["rep"] = pd.to_datetime(reg.reported_date)
    ev = pd.read_csv(f("platform_feature_events_2027-01-06.csv"), dtype=str, keep_default_na=False)
    ev["t"] = _local(ev.event_at)
    pay = pd.read_csv(f("platform_bi_payments_2024-2027.csv"), dtype=str, keep_default_na=False)
    pay["amt"] = pay.amount_cents.astype(int) / 100.0
    pay["t"] = _local(pay.issued_at)
    pay["tv"] = _local(pay.voided_at.replace("", None))
    gl = pd.read_csv(f("gl_5311_bi_paid_loss_2026.csv"), dtype=str)
    gl["d"] = pd.to_datetime(gl.posting_date)
    gl["amt"] = gl.amount.astype(float)
    import openpyxl
    ws = openpyxl.load_workbook(f("year_end_2026_preliminary_reserves.xlsx"), data_only=True).active
    booked = [r[3] for r in ws.iter_rows(min_row=5, values_only=True) if r[1] == "Bodily injury" and r[2] == "Loss"][0]
    return arch, lpay, reg, ev, pay, gl, float(booked) * 1000.0


def universe(arch, reg):
    """Claimant features: the archive less CV and XD, the register less DUPLICATE, a legacy feature re-entered on the
    platform (its legacy_ref on a closed archive row) once, under its legacy number."""
    cv = set(arch.key[arch.DISP == "CV"])
    closed_arch = arch[~arch.DISP.isin(["CV", "XD"])]
    live = reg[reg.disposition != "DUPLICATE"]
    reentered = set(live.legacy_ref) & set(closed_arch.key)
    ident = {fid: (ref if ref in reentered else fid) for fid, ref in zip(live.feature_id, live.legacy_ref)}
    for ref in cv:
        hit = live.feature_id[live.legacy_ref == ref]
        if len(hit):
            ident[ref] = hit.iloc[0]
    rows = [(k, a, r) for k, a, r in zip(closed_arch.key, closed_arch.LOSS_DT, closed_arch.RPT_DT)]
    rows += [(fid, a, r) for fid, a, r, ref in zip(live.feature_id, live.acc, live.rep, live.legacy_ref)
             if ref not in reentered]
    u = pd.DataFrame(rows, columns=["id", "acc", "rep"])
    return u, ident, reentered, closed_arch, live


def closed_at_ends(u, ident, closed_arch, live, ev):
    """For each feature, closed (True) at the end of each calendar quarter 0..39."""
    ends = [pd.Timestamp(2017 + (k + 1) // 4, ((k + 1) % 4) * 3 + 1, 1) for k in range(NQ)]
    hist = {}
    for k, c in zip(closed_arch.key, closed_arch.CLS_DT):
        hist.setdefault(k, []).append((c + pd.Timedelta(hours=12), 1))
    e = ev[ev.event.isin(["CLOSED", "REOPENED"]) & ev.feature_id.isin(set(live.feature_id))]
    for fid, kind, t in zip(e.feature_id, e.event, e.t):
        hist.setdefault(ident.get(fid, fid), []).append((t, 1 if kind == "CLOSED" else -1))
    out = np.zeros((len(u), NQ), bool)
    for n, i in enumerate(u.id):
        h = sorted(hist.get(i, []))
        for q, end in enumerate(ends):
            out[n, q] = sum(d for t, d in h if t < end) > 0
    return out


def paid_by_feature(lpay, pay, ident, arch, reg, upto):
    """Net paid through `upto`, by feature id in the universe's terms (a duplicate's payment on its claim's one real
    feature)."""
    m = dict(ident)
    claim = arch.key.str.rsplit("-", n=1).str[0]
    real = arch[arch.DISP != "XD"].groupby(claim[arch.DISP != "XD"]).key.agg(list)
    for k, cl in zip(arch.key[arch.DISP == "XD"], claim[arch.DISP == "XD"]):
        if len(real.get(cl, [])) == 1:
            m[k] = m.get(real[cl][0], real[cl][0])
    realp = reg[reg.disposition != "DUPLICATE"].groupby("claim_number").feature_id.agg(list)
    for fid, cn in zip(reg.feature_id[reg.disposition == "DUPLICATE"], reg.claim_number[reg.disposition == "DUPLICATE"]):
        if len(realp.get(cn, [])) == 1:
            m[fid] = m.get(realp[cn][0], realp[cn][0])
    rows = [(m.get(k, k), a) for k, a, t in zip(lpay.key, lpay.amt, lpay.t) if t < upto]
    rows += [(m.get(k, k), a) for k, a, t in zip(pay.feature_id, pay.amt, pay.t) if t < upto]
    rows += [(m.get(k, k), -a) for k, a, t in zip(pay.feature_id, pay.amt, pay.tv) if pd.notna(t) and t < upto]
    return pd.DataFrame(rows, columns=["id", "a"]).groupby("id").a.sum()


def carried(arch, lpay, reg, ev, pay):
    u, ident, reentered, closed_arch, live = universe(arch, reg)
    u["aq"] = _q(u.acc)
    u["rq"] = _q(u.rep)
    accf = dict(zip(reg.feature_id, reg.acc))
    tx = pd.concat([pd.DataFrame({"acc": lpay.acc, "t": lpay.t, "a": lpay.amt}),
                    pd.DataFrame({"acc": pay.feature_id.map(accf), "t": pay.t, "a": pay.amt}),
                    pd.DataFrame({"acc": pay.feature_id.map(accf)[pay.tv.notna()], "t": pay.tv[pay.tv.notna()],
                                  "a": -pay.amt[pay.tv.notna()]})], ignore_index=True)
    tx["aq"], tx["tq"] = _q(tx.acc), _q(tx.t)
    P = np.full((NQ, NQ), np.nan)
    Rr, C = P.copy(), P.copy()
    cl = closed_at_ends(u, ident, closed_arch, live, ev)
    for i in range(NQ):
        ti = tx[tx.aq == i]
        ui = u.aq.to_numpy() == i
        for j in range(NQ - i):
            P[i, j] = ti.a[ti.tq <= i + j].sum()
            Rr[i, j] = int((u.rq.to_numpy()[ui] <= i + j).sum())
            C[i, j] = int(cl[ui, i + j].sum())
    last = [NQ - 1 - i for i in range(NQ)]

    def fac(T):
        return [np.nansum([T[i, j + 1] for i in range(NQ - j - 1)]) / np.nansum([T[i, j] for i in range(NQ - j - 1)])
                for j in range(NQ - 1)]

    def proj(T, f):
        return np.array([T[i, last[i]] * np.prod(f[last[i]:]) for i in range(NQ)])
    n_ult = proj(Rr, fac(Rr))
    D = C / n_ult[:, None]
    tgt = [D[NQ - 1 - j, j] for j in range(NQ)]
    Rs = P.copy()
    for i in range(NQ):
        xs = [0.0] + [D[i, j] for j in range(last[i] + 1)]
        ys = [0.0] + [P[i, j] for j in range(last[i] + 1)]
        for j in range(last[i]):
            x = tgt[j]
            k = 1
            while k < len(xs) - 1 and xs[k] < x:
                k += 1
            x0, x1, y0, y1 = xs[k - 1], xs[k], ys[k - 1], ys[k]
            Rs[i, j] = y1 if x1 <= x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    lat = np.array([P[i, last[i]] for i in range(NQ)])
    unpaid = proj(P, fac(Rs)) - lat
    plain = proj(P, fac(P)) - lat
    return float(unpaid.sum()), float(plain.sum())


def counts(arch, lpay, reg, ev, pay):
    u, ident, reentered, closed_arch, live = universe(arch, reg)
    end = pd.Timestamp(2027, 1, 1)
    cl = closed_at_ends(u, ident, closed_arch, live, ev)[:, NQ - 1]
    paid = u.id.map(paid_by_feature(lpay, pay, ident, arch, reg, end)).fillna(0.0).to_numpy()
    rep_ok = (u.rep < end).to_numpy()
    ay = u.acc.dt.year.to_numpy()
    return {y: (int(((ay == y) & rep_ok & cl & (paid > 0.005)).sum()),
                int(((ay == y) & rep_ok & cl & (paid <= 0.005)).sum())) for y in range(2017, 2027)}


def ledger(gl, pay, reg):
    """Each 2026 quarter of account 5311: claims payments issued in an earlier quarter, and lines no claims payment
    accounts for (checks by the Central day before the feed's posting, a day's checks once; wires by the month of
    their bank value date, released after 15:00 counted to the next business day)."""
    st = dict(zip(reg.feature_id, reg.state))
    pay = pay.assign(state=pay.feature_id.map(st))
    chk = pay[pay.method == "CHECK"]
    net = {}
    for d, s, a in zip(chk.t.dt.date, chk.state, chk.amt):
        net[(d, s)] = net.get((d, s), 0.0) + a
    for d, s, a in zip(chk.tv.dt.date, chk.state, chk.amt):
        if not pd.isna(d):
            net[(d, s)] = net.get((d, s), 0.0) - a
    hol = set()
    for y in (2025, 2026, 2027):
        for m_, d_ in ((1, 1), (7, 4), (12, 25)):
            x = dt.date(y, m_, d_)
            hol.add(x - dt.timedelta(days=1) if x.weekday() == 5 else x + dt.timedelta(days=1) if x.weekday() == 6 else x)

    def nxt(d):
        d += dt.timedelta(days=1)
        while d.weekday() >= 5 or d in hol or _special(d):
            d += dt.timedelta(days=1)
        return d

    def _special(d):
        mem = max(dt.date(d.year, 5, k) for k in range(25, 32) if dt.date(d.year, 5, k).weekday() == 0)
        lab = min(dt.date(d.year, 9, k) for k in range(1, 8) if dt.date(d.year, 9, k).weekday() == 0)
        thx = [dt.date(d.year, 11, k) for k in range(1, 31) if dt.date(d.year, 11, k).weekday() == 3][3]
        return d in (mem, lab, thx, thx + dt.timedelta(days=1))
    wires = pay[pay.method == "WIRE"]
    wv = [(t.date() if t.hour < 15 else nxt(t.date()), t.date(), s, a) for t, s, a in zip(wires.t, wires.state, wires.amt)]
    out = {}
    seen = set()
    for q in range(4):
        lo = dt.date(2026, 3 * q + 1, 1)
        hi = dt.date(2026, 3 * q + 4, 1) if q < 3 else dt.date(2027, 1, 1)
        g = gl[(gl.d.dt.date >= lo) & (gl.d.dt.date < hi)]
        earlier = other = 0.0
        for (d, ref), lines in g.groupby([g.d, g.batch_ref], sort=True):
            src = lines.source.iloc[0]
            amts = dict(zip(lines.state, lines.amt))
            if src == "CLAIMS FEED":
                day = None
                for k in range(1, 6):
                    c = (d - pd.Timedelta(days=k)).date()
                    if all(abs(round(net.get((c, s), 0.0), 2) - a) < 0.005 and (c, s) not in seen
                           for s, a in amts.items()):
                        day = c
                        break
                if day is None:
                    other += sum(amts.values())
                else:
                    seen.update((day, s) for s in amts)
                    if day < lo:
                        earlier += sum(amts.values())
            elif src == "TREASURY":
                prev = d - pd.DateOffset(months=1)
                for s, a in amts.items():
                    mine = [(i_, a_) for v_, i_, s_, a_ in wv if s_ == s and (v_.year, v_.month) == (prev.year, prev.month)]
                    earlier += sum(a_ for i_, a_ in mine if i_ < lo)
                    other += a - sum(a_ for _, a_ in mine)
            else:
                for s, a in amts.items():
                    hit = None
                    for k in range(1, 6):
                        c = (d - pd.Timedelta(days=k)).date()
                        if (c, s) not in seen and abs(a) > 0.005 and abs(round(net.get((c, s), 0.0), 2) - a) < 0.005:
                            hit = c
                            break
                    if hit is None:
                        other += a
                    else:
                        seen.add((hit, s))
                        if hit < lo:
                            earlier += a
        out[q + 1] = (round(earlier, 2), round(other, 2))
    return out


def main(target, golden):
    arch, lpay, reg, ev, pay, gl, booked = read(target)
    unpaid, plain = carried(arch, lpay, reg, ev, pay)
    carry = int(np.floor(unpaid / 25e6 + 0.5) * 25)
    memo = open(os.path.join(golden, "bi_reserve_ye2026.md"), encoding="utf-8").read()
    want = re.search(r"Carry \$(\d+) million", memo).group(1)
    assert int(want) == carry, (want, carry, unpaid)
    assert "$%.1f million" % (unpaid / 1e6) in memo, unpaid
    assert "$%.1f million" % (plain / 1e6) in memo, plain
    assert "$%.1f million more than the $%.1f million" % (carry - booked / 1e6, booked / 1e6) in memo
    cnt = counts(arch, lpay, reg, ev, pay)
    rows = open(os.path.join(golden, "bi_claim_counts_ye2026.csv"), encoding="utf-8").read().strip().splitlines()[1:]
    for r in rows:
        y, a, b = map(int, r.split(","))
        assert cnt[y] == (a, b), (y, cnt[y], a, b)
    led = ledger(gl, pay, reg)
    for q, (e, o) in led.items():
        line = "| Q%d 2026 | " % q
        row = [ln for ln in memo.splitlines() if ln.startswith(line)][0]
        cells = [c.strip().replace(",", "") for c in row.split("|")[2:5]]
        assert abs(float(cells[1]) - e) < 0.005 and abs(float(cells[2]) - o) < 0.005, (q, e, o, cells)
    print("verify: carried $%d million (indicated %.1f, chain ladder %.1f), 20 count cells and 8 ledger cells "
          "recomputed from target/ alone" % (carry, unpaid / 1e6, plain / 1e6))


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(here, "target"), os.path.join(here, "golden"))
