"""task127 generator: the pilot's money trail (installer invoices, the fund's payment ledger, the bank's
returned-payment notices) and the pilot log's own columns that the two asks read.

Devices (ask ledger in the design note): A1 version of record (latest version the fund accepted); HZ1 one
firm's export repeats a multi-zone system's price on every indoor-head line; HZ2 returned bank transfers that
live only in the bank's notices, reissued by cheque under a new payment id; B1 the bank's UTC clearing clock
against the fund's Central-time month end. Over-cleaning halves: two genuine identical electrical lines on
some jobs; assigned rebates paid in two legs.
"""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import params as P

CT = ZoneInfo("America/Chicago")
INSTALLERS = {
    "NWC": ("Northwoods Comfort Systems", ["NS", "LA"]),
    "RHA": ("Range Heating & Air", ["NS"]),
    "CMC": ("Coulee Mechanical", ["VA", "RB"]),
    "RVH": ("River Valley HVAC", ["VA", "RB"]),
    "LSM": ("Lakeshore Mechanical", ["LA"]),
    "PAS": ("Prairie Air Services", ["UP"]),
    "TCH": ("Tri-County Heat Pump Co.", ["UP", "PW"]),
    "PCH": ("Pine Country Heating", ["PW"]),
    "BMS": ("Boreal Mini-Split", ["NS", "LA", "RB", "PW"]),
}
INSTALLER_NO = {"NWC": "IN-1042", "RHA": "IN-1057", "CMC": "IN-1061", "RVH": "IN-1078", "LSM": "IN-1083",
                "PAS": "IN-1090", "TCH": "IN-1104", "PCH": "IN-1112", "BMS": "IN-1126"}
REBATE = {"D": 3600, "E": 4200, "H": 5400}
TOPUP = 1000                      # household income 35,000 to 74,999
REPEATER = "BMS"
MONTH_END = date(2026, 11, 30)


def rebate_amount(sys, inc):
    return REBATE[sys] + (TOPUP if inc == P.IN_BAND[0] else 0)


def pilot_columns(pi):
    """System type, indoor heads and installer for each pilot install."""
    g = P.rng("pilot-kit")
    st, heads, inst = [], [], []
    for r in pi.itertuples():
        if r.sys == "D":
            t, h = "ducted", 1
        elif r.sys == "E":
            t = "ductless multi-zone" if g.random() < 0.45 else "ductless single-zone"
            h = int(g.choice([2, 3, 4], p=[.5, .35, .15])) if t.endswith("multi-zone") else 1
        else:
            t = "ductless multi-zone" if g.random() < 0.7 else "ductless single-zone"
            h = int(g.choice([2, 3, 4], p=[.45, .4, .15])) if t.endswith("multi-zone") else 1
        firms = [k for k, v in INSTALLERS.items() if r.coop in v[1]]
        if t == "ducted":
            firms = [f for f in firms if f != REPEATER]
            f = firms[int(g.integers(0, len(firms)))]
        else:
            f = REPEATER if (REPEATER in firms and g.random() < 0.55) else \
                [x for x in firms if x != REPEATER][int(g.integers(0, len([x for x in firms if x != REPEATER])))]
        st.append(t); heads.append(h); inst.append(f)
    pi = pi.copy()
    pi["system_type"] = st
    pi["indoor_heads"] = heads
    pi["installer"] = inst
    pi["rebate_usd"] = [rebate_amount(s, i) for s, i in zip(pi.sys, pi.income_band)]
    return pi


# ------------------------------------------------------------------ invoices

def _ct(d, hh, mm):
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=CT)


def _mid(x, step, edge):
    """Distance of x from the nearest rounding edge for a grid of `step` (edges at k*step + edge)."""
    r = (x - edge) % step
    return min(r, step - r)


def invoices(pi):
    """Every invoice version installers delivered for pilot jobs, one row per line."""
    g = P.rng("invoices")
    jobs = []
    kinds_by_k = {}
    for c in P.COOPS:
        idx = np.flatnonzero(pi.coop.to_numpy() == c)
        m = max(3, int(round(len(idx) * 0.09)))
        early = np.array([k for k in idx if pi.install_date.iloc[k] <= date(2026, 10, 31)])
        pick = g.permutation(early)[:m]
        for j, k in enumerate(pick):
            kinds_by_k[int(k)] = ["rejected_resend", "change_order", "correction"][j] if j < 3 else \
                str(g.choice(["rejected_resend", "change_order", "correction"], p=[.35, .4, .25]))
    for k, r in enumerate(pi.itertuples()):
        sys_price = {"ducted": g.uniform(11200, 15400), "ductless single-zone": g.uniform(5600, 7900),
                     "ductless multi-zone": g.uniform(7600, 9400) + 1900 * (r.indoor_heads - 1)}[r.system_type]
        lines = [["heat pump system, supplied and installed", round(sys_price / 5) * 5]]
        circuits = 2 if (r.system_type == "ducted" and g.random() < 0.12) else 1
        elec = round(g.uniform(820, 1380) / 5) * 5
        lines += [["electrical: 240 V circuit and disconnect", elec] for _ in range(circuits)]
        lines.append(["heat-pump rate meter base and wiring", round(g.uniform(340, 610) / 5) * 5])
        lines.append(["line set, pad and condensate", round(g.uniform(380, 920) / 5) * 5])
        if r.sys in ("D", "H"):
            lines.append(["removal of existing propane equipment", round(g.uniform(320, 780) / 5) * 5])
        if r.system_type == "ducted" and g.random() < 0.55:
            lines.append(["ductwork modifications", round(g.uniform(600, 2400) / 5) * 5])
        lines.append(["permit and inspection", round(g.uniform(150, 290) / 5) * 5])
        heads = [f"ID{g.integers(10**6, 10**7)}" for _ in range(r.indoor_heads)]
        kind = kinds_by_k.get(k, "single")
        delta = {"rejected_resend": round(g.uniform(450, 1600) / 5) * 5, "change_order": round(g.uniform(700, 2200) / 5) * 5,
                 "correction": round(g.uniform(300, 900) / 5) * 5, "single": 0}[kind]
        t0 = _ct(r.install_date + timedelta(days=int(g.integers(1, 6))), int(g.integers(8, 17)), int(g.integers(0, 60)))
        gaps = [int(g.integers(4, 15)), int(g.integers(0, 300)), int(g.integers(1, 5)), int(g.integers(0, 6)),
                int(g.integers(0, 300)), int(g.integers(1, 5)), int(g.integers(0, 6)), int(g.integers(3, 58)),
                int(g.integers(3, 58))]
        jobs.append(dict(r=r, lines=lines, heads=heads, kind=kind, delta=delta, t0=t0, gaps=gaps))

    def record_total(j):
        base = sum(a for _, a in j["lines"])
        return base + (j["delta"] if j["kind"] == "change_order" else 0)

    # centre each co-op's average cost and rebate share in their rounding bins (whole dollars; one decimal)
    tuned = {}
    for c in P.COOPS:
        js = [j for j in jobs if j["r"].coop == c]
        tune = next(j for j in js if j["kind"] == "single" and j["r"].installer != REPEATER)
        reb = sum(j["r"].rebate_usd for j in js)
        for step in sorted(range(-900, 905, 5), key=lambda x: (abs(x), x)):
            tune["lines"][0][1] += step
            tot = sum(record_total(j) for j in js)
            avg, share = tot / len(js), reb / tot * 100
            if _mid(avg, 1, 0.5) >= 0.2 and _mid(share, 0.1, 0.05) >= 0.02:
                tuned[c] = step
                break
            tune["lines"][0][1] -= step
        assert c in tuned, c
    rows, truth, kinds = [], {}, {}
    for inv_seq, j in enumerate(jobs, start=1):
        r, lines, kind, delta = j["r"], [tuple(x) for x in j["lines"]], j["kind"], j["delta"]
        if kind == "rejected_resend":
            versions = [(lines, True), ([(lines[0][0], lines[0][1] + delta)] + lines[1:], False)]
        elif kind == "change_order":
            versions = [(lines, True), (lines + [("change order: additional work approved", delta)], True)]
        elif kind == "correction":
            versions = [([(lines[0][0], lines[0][1] + delta)] + lines[1:], True), (lines, True)]
        else:
            versions = [(lines, True)]
        truth[r.rebate_id] = record_total(j)
        kinds[r.rebate_id] = kind
        inv_no = f"{INSTALLER_NO[r.installer][3:]}-{2600 + inv_seq * 3}"
        gp = j["gaps"]
        for v, (ls, accepted) in enumerate(versions, start=1):
            dt = j["t0"] + (timedelta(days=gp[0], minutes=gp[1]) if v == 2 else timedelta(0))
            acc = dt + timedelta(days=gp[2 if v == 1 else 5], hours=gp[3 if v == 1 else 6],
                                 minutes=gp[7 if v == 1 else 8]) if accepted else None
            out = []
            for desc, amt in ls:
                if desc.startswith("heat pump system") and r.system_type == "ductless multi-zone":
                    if r.installer == REPEATER:
                        for h, sn in enumerate(j["heads"], start=1):
                            out.append((f"multi-zone heat pump system, indoor head {h}", amt, sn))
                    else:
                        out.append((desc, amt, ";".join(j["heads"])))
                elif desc.startswith("heat pump system"):
                    out.append((desc, amt, j["heads"][0] if r.system_type != "ducted" else ""))
                else:
                    out.append((desc, amt, ""))
            for ln, (desc, amt, sn) in enumerate(out, start=1):
                rows.append(dict(invoice_no=inv_no, version=v, installer_id=INSTALLER_NO[r.installer],
                                 premises_id=r.premises_id, delivered_at=dt.strftime("%Y-%m-%d %H:%M"),
                                 accepted_at=acc.strftime("%Y-%m-%d %H:%M") if acc else "",
                                 line_no=ln, description=desc, unit_serial=sn, amount_usd=f"{amt:.2f}"))
    df = pd.DataFrame(rows)
    df = df.sort_values(["delivered_at", "invoice_no", "version", "line_no"], kind="stable").reset_index(drop=True)
    return df, truth, kinds


# ------------------------------------------------------------------ payments

def _runs(d0, d1):
    out, d = [], d0
    while d <= d1:
        if d.weekday() in (0, 3):
            out.append(d)
        d += timedelta(days=1)
    return out


RUNS = _runs(date(2026, 4, 1), date(2026, 12, 31))


def payments(pi):
    """The fund's payment ledger and the bank's notices, re-drawn with a different forced return in any co-op
    where two mishandlings would cancel back onto the right dollars."""
    shift = {c: 0 for c in P.COOPS}
    for _ in range(12):
        L, N = _payments(pi, shift)
        bad = _cancelling(L, N, pi)
        if not bad:
            return L, N
        for c in bad:
            shift[c] += 1
    raise AssertionError("payments: cancelling stops remain")


def _cancelling(L, N, pi):
    coop = dict(zip(pi.rebate_id, pi.coop))
    ret = set(N.payment_id)
    cut = date(2026, 11, 30)
    ok = L[[isinstance(c, datetime) for c in L.cleared_utc]]
    cen = [c.astimezone(CT).date() <= cut for c in ok.cleared_utc]
    utc = [c.date() <= cut for c in ok.cleared_utc]
    rel = list(L.released_on <= cut)
    bad = set()
    for c in P.COOPS:
        def tot(mask_rows, frame, drop):
            f = frame[mask_rows]
            f = f[[coop[r] == c for r in f.rebate_id]]
            if drop:
                f = f[~f.payment_id.isin(ret)]
            return f.amount_usd.sum()
        gold = tot(cen, ok, True)
        stops = [tot(utc, ok, False), tot(utc, ok, True), tot(cen, ok, False), tot(rel, L, True)]
        if any(abs(x - gold) < 0.5 for x in stops):
            bad.add(c)
    return bad


def _payments(pi, shift):
    g = P.rng("payments")
    led, notices = [], []
    pay_seq = [30410]

    def pid():
        pay_seq[0] += int(g.integers(1, 4))
        return f"CHF-{pay_seq[0]:06d}"

    pi = pi.sort_values(["meter_set_date", "rebate_id"]).reset_index(drop=True)
    assigned = g.random(len(pi)) < 0.45
    run_of = [next(x for x in RUNS if x >= d + timedelta(days=10)) for d in pi.meter_set_date]
    late_cheque = set()
    for c in P.COOPS:     # in each co-op, one member without an account on file paid in a late-November run
        k = next(k for k in range(len(pi)) if pi.coop[k] == c and date(2026, 11, 16) <= run_of[k] <= date(2026, 11, 26))
        late_cheque.add(k)
        assigned[k] = False
    forced_return = set()
    for c in P.COOPS:     # and one member whose account had closed, paid in a summer or autumn run
        cands = [k for k in range(len(pi)) if pi.coop[k] == c and k not in late_cheque
                 and date(2026, 7, 1) <= run_of[k] <= date(2026, 10, 15)]
        k = cands[shift[c] % len(cands)]
        forced_return.add(k)
        assigned[k] = False
    for k, r in enumerate(pi.itertuples()):
        run = run_of[k]
        rel = _ct(run, 18, int(g.integers(28, 56)))
        amt = r.rebate_usd
        if k in late_cheque:
            led.append(dict(payment_id=pid(), rebate_id=r.rebate_id, payee_type="member", method="cheque",
                            amount_usd=amt, released_on=run,
                            cleared=_ct(date(2026, 12, 1) + timedelta(days=int(g.integers(1, 8))),
                                        int(g.integers(9, 17)), int(g.integers(0, 60))), memo=""))
            continue
        if assigned[k]:
            if g.random() < 0.4:
                legs = [("installer", amt / 2), ("member", amt / 2)]
            else:
                legs = [("installer", amt - 500), ("member", 500)]
            for who, a in legs:
                led.append(dict(payment_id=pid(), rebate_id=r.rebate_id, payee_type=who, method="ACH",
                                amount_usd=a, released_on=run, cleared=rel + timedelta(minutes=int(g.integers(2, 9))),
                                memo="assigned rebate"))
            continue
        if g.random() < 0.10 and k not in forced_return:
            led.append(dict(payment_id=pid(), rebate_id=r.rebate_id, payee_type="member", method="cheque",
                            amount_usd=amt, released_on=run,
                            cleared=_ct(run + timedelta(days=int(g.integers(4, 21))), int(g.integers(9, 17)),
                                        int(g.integers(0, 60))), memo=""))
            continue
        p0 = pid()
        led.append(dict(payment_id=p0, rebate_id=r.rebate_id, payee_type="member", method="ACH", amount_usd=amt,
                        released_on=run, cleared=rel + timedelta(minutes=int(g.integers(2, 9))), memo=""))
        if g.random() < 0.11 or k in forced_return:
            ret = rel + timedelta(days=int(g.choice([2, 3, 4])), hours=int(g.integers(-3, 3)))
            notices.append(dict(payment_id=p0, returned=ret, amount=amt))
            run2 = next(x for x in RUNS if x >= ret.date() + timedelta(days=5))
            led.append(dict(payment_id=pid(), rebate_id=r.rebate_id, payee_type="member", method="cheque",
                            amount_usd=amt, released_on=run2,
                            cleared=_ct(run2 + timedelta(days=int(g.integers(3, 19))), int(g.integers(9, 17)),
                                        int(g.integers(0, 60))), memo="reissue"))
    L = pd.DataFrame(led)
    pull = datetime(2026, 12, 11, 6, 0, tzinfo=CT)
    L = L[L.released_on <= date(2026, 12, 10)].copy()
    L["cleared_utc"] = pd.Series([c.astimezone(timezone.utc) if c <= pull else None for c in L.cleared], index=L.index, dtype=object)
    N = pd.DataFrame(notices)
    N = N[N.returned <= pull].copy()
    return L, N


def ledger_frame(L):
    df = pd.DataFrame({
        "payment_id": L.payment_id, "rebate_id": L.rebate_id, "payee_type": L.payee_type, "method": L.method,
        "amount_usd": [f"{a:.2f}" for a in L.amount_usd], "released_on": [d.isoformat() for d in L.released_on],
        "cleared_at": [c.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(c, datetime) else "" for c in L.cleared_utc],
        "memo": L.memo})
    return df.sort_values(["released_on", "payment_id"], kind="stable").reset_index(drop=True)


def notices_doc(N, L):
    acct = {p: f"****{int(abs(hash_s(p)) % 9000 + 1000)}" for p in N.payment_id}
    items = []
    for i, r in enumerate(N.sort_values("returned").itertuples(), start=1):
        items.append({"notice_id": f"RTN-26-{40310 + 17 * i}", "type": "ACH_RETURN",
                      "original_payment_reference": r.payment_id,
                      "returned_at": r.returned.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "return_code": "R02", "return_reason": "Account closed",
                      "amount": {"value": f"{r.amount:.2f}", "currency": "USD"},
                      "receiver_account": acct[r.payment_id]})
    return {"originator": P.FUND, "originator_id": "1841203377", "report": "ACH returns",
            "period": {"from": "2026-04-01T00:00:00Z", "to": "2026-12-11T12:00:00Z"},
            "count": len(items), "notices": items}


def hash_s(s):
    h = 0
    for ch in s:
        h = (h * 31 + ord(ch)) % 1000003
    return h
