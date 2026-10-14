"""The maturity book the asks read: the holdings view of every term deposit and investment certificate the core holds
on 2 November 2026 that matures from January to June 2027 (one row per holder of each account), the legacy investment
platform's final certificate register (30 June 2026) and the migration batches that moved certificates to the core."""
from __future__ import annotations

import datetime as dt

import sim as S
import world as W

H1_FROM, H1_TO = dt.date(2027, 1, 1), dt.date(2027, 6, 30)

# Cohorts maturing April to June 2027 that the window simulation did not create, by term.
REST_2027Q2 = {1: 1600, 2: 2200, 3: 1450, 4: 1200, 5: 1150}


def rest_of_book(Wd):
    r = W.rng("book-2027q2")
    for term, n in REST_2027Q2.items():
        oq = W.q_add("2027Q2", -4 * term)
        for _ in range(n):
            pr = S._principal(r)
            rate = S._locked(r, oq, term, None, pr)
            h = S._holder(Wd, r, term, False, "2027Q2")
            S.new_deposit(Wd, r, h, term, rate, pr, S._open_day(r, oq), "rest",
                          "PAY" if r.random() < 0.07 else None)


def certificates(Wd):
    """Kaimai Investment Certificates: a fixed-term product sold until 2023 on the legacy platform, interest paid on
    each anniversary of issue. The register lists every certificate open at 30 June 2026. No two certificates share an
    issue date, a term and a rate (the platform's issue runs were sparse)."""
    r = W.rng("kip")
    out = []
    no = 1002417
    mem = 30411
    members = []
    used = set()
    for _ in range(3400):
        term = int(r.choice([1, 2, 3, 4, 5], p=[.12, .18, .26, .2, .24]))
        prem = float(r.choice([0.10, 0.15, 0.20, 0.25]))
        # issued 2021 to mid-2023 (sales ended June 2023), or reinvested on the platform up to June 2026
        while True:
            issue = dt.date(2021, 7, 1) + dt.timedelta(days=int(r.integers(0, 1800)))
            mat = S.add_years(issue, term)
            rate = round(W.card(W.q_of(issue), term) + prem, 2)
            if issue <= dt.date(2026, 6, 26) and mat > W.KIP_FROZEN and W.business_day(issue) and \
                    (issue, term, rate) not in used:
                break
        used.add((issue, term, rate))
        if members and r.random() < 0.18:
            m = members[int(r.integers(0, len(members)))]
        else:
            mem += int(r.integers(2, 29))
            m = "M%06d" % mem
            members.append(m)
        pr = S._principal(r)
        no += int(r.integers(3, 61))
        out.append(dict(cert="KIC-%07d" % no, member=m, principal=pr, rate=rate, issue=issue, maturity=mat,
                        term=term))
    return out


def accrued(c, on):
    """Interest accrued on a certificate from its last anniversary of issue to the day it moved to the core."""
    last = c["issue"]
    k = 1
    while S.add_years(c["issue"], k) <= on:
        last = S.add_years(c["issue"], k)
        k += 1
    return round(c["principal"] * c["rate"] / 100.0 * (on - last).days / 365.0, 2)


def _edge_gap(x, unit=1000.0):
    """How far x sits from the nearest rounding edge when rounded to the nearest unit."""
    f = x % unit
    return abs(f - unit / 2.0)


def nudge_off_edges(Wd, certs, moved, migrated, clear=150.0):
    """Keep each month's maturing principal, and the quarter's part off the list, clear of a thousand-dollar rounding
    edge: while a figure sits within NZ$150 of an edge, one sole-held deposit maturing in that month (for the quarter's
    part, in March) that is on no list and in no extract but the holdings view takes the smallest shift in its
    principal (a multiple of NZ$50) that clears both the month and the quarter's part."""
    listed = {d["acct"] for d in Wd.campaigns[W.FWD]["listed"]}
    seen = {s["acct"] for q in W.PAST for s in Wd.campaigns[q]["listed"]} | set(Wd.tracked)

    def span(m):
        return dt.date(2027, m, 1), dt.date(2027, m + 1, 1) - dt.timedelta(days=1)

    def totals():
        tot, lst = {}, 0.0
        for m in (1, 2, 3):
            lo, hi = span(m)
            td = [d for d in Wd.deposits.values() if d["status"] == "open" and lo <= d["maturity"] <= hi]
            tot[m] = sum(d["principal"] for d in td) + \
                sum(c["core_principal"] for c in migrated if lo <= c["maturity"] <= hi) + \
                sum(c["principal"] for c in certs if lo <= c["maturity"] <= hi and c["cert"] not in moved)
            lst += sum(d["principal"] for d in td if d["acct"] in listed)
        return tot, sum(tot.values()) - lst
    for _ in range(4):
        tot, off = totals()
        bad = [m for m in (1, 2, 3) if _edge_gap(tot[m]) < clear]
        if not bad and _edge_gap(off) >= clear:
            return
        m = bad[0] if bad else 3
        lo, hi = span(m)
        pick = sorted((d for d in Wd.deposits.values() if d["status"] == "open" and lo <= d["maturity"] <= hi and
                       d["acct"] not in listed and d["acct"] not in seen and not d.get("joint") and
                       d["principal"] >= 5000), key=lambda d: d["acct"])[0]
        for step in sorted(range(-400, 401, 50), key=lambda x: (abs(x), x)):
            if _edge_gap(tot[m] + step) >= clear and _edge_gap(off + step) >= clear:
                pick["principal"] = round(pick["principal"] + step, 2)
                break
        else:
            raise AssertionError("no shift clears month %d" % m)
    tot, off = totals()
    assert all(_edge_gap(v) >= clear for v in tot.values()) and _edge_gap(off) >= clear, (tot, off)


def build_book(Wd):
    rest_of_book(Wd)
    r = W.rng("holdings")
    certs = certificates(Wd)
    # migration: six batches from July to October 2026; most certificates move, some are deferred, the rest wait
    batch_dates = [dt.date(2026, 7, 13), dt.date(2026, 7, 27), dt.date(2026, 8, 17), dt.date(2026, 9, 7),
                   dt.date(2026, 9, 28), dt.date(2026, 10, 19)]
    batches = []
    member_cust = {}
    body = 700113
    migrated = []
    hand_days = [d for d in (dt.date(2026, 7, 1) + dt.timedelta(days=k) for k in range(0, 112)) if W.business_day(d)]

    def move(c, on, logged, k=None):
        if c["member"] not in member_cust:
            member_cust[c["member"]] = Wd.next_cust
            Wd.next_cust += int(r.integers(3, 41))
        nonlocal_body[0] += int(r.integers(5, 71))
        acct = W.acct_plain(nonlocal_body[0], W.KIC_SUFFIX)
        if logged:
            batches.append(["KIP-MIG-%02d" % (k + 1), batch_dates[k].isoformat(), c["cert"], acct, "MIGRATED"])
        migrated.append(dict(c, acct=acct, cust=member_cust[c["member"]], moved=on, logged=logged,
                             core_principal=round(c["principal"] + accrued(c, on), 2)))
    nonlocal_body = [body]
    for c in sorted(certs, key=lambda c: c["cert"]):
        u = float(r.random())
        if c["maturity"] <= dt.date(2026, 10, 19):
            continue        # matured on the platform before its batch came round
        if u < 0.84:
            if r.random() < 0.12:
                # moved by the operations team outside the batches (certificates the batch loader rejected)
                move(c, hand_days[int(r.integers(0, len(hand_days)))], False)
            else:
                k = int(r.integers(0, len(batch_dates)))
                move(c, batch_dates[k], True, k)
        elif u < 0.89:
            k = int(r.integers(0, len(batch_dates) - 1))
            batches.append(["KIP-MIG-%02d" % (k + 1), batch_dates[k].isoformat(), c["cert"], "", "DEFERRED"])
            if r.random() < 0.4:
                # held back from one batch and moved in a later one
                k2 = int(r.integers(k + 1, len(batch_dates)))
                move(c, batch_dates[k2], True, k2)
    batches.sort(key=lambda b: (b[1], b[2]))
    moved = {c["cert"] for c in migrated}
    nudge_off_edges(Wd, certs, moved, migrated)
    kip = []
    for c in sorted(certs, key=lambda c: c["cert"]):
        kip.append([c["cert"], c["member"], "%.2f" % c["principal"], "%.2f" % c["rate"], c["issue"].isoformat(),
                    c["maturity"].isoformat(), c["term"] * 12, "ACTIVE"])
    # the holdings view: every open account maturing January to June 2027, one row per holder
    rows = []
    for d in Wd.deposits.values():
        if d["status"] != "open" or not (H1_FROM <= d["maturity"] <= H1_TO):
            continue
        holders = [d["holder"]]
        if d.get("joint"):
            if d["joint"] == "pending":
                d["joint"] = Wd.next_cust
                Wd.next_cust += int(r.integers(3, 41))
            holders.append(d["joint"])
        for h in holders:
            rows.append([h, d["acct"], "TD", "%.2f" % d["principal"], "%.4f" % (d["rate"] / 100.0), d["term"] * 12,
                         d["opened"].isoformat(), d["maturity"].isoformat()])
    for c in migrated:
        if not (H1_FROM <= c["maturity"] <= H1_TO):
            continue
        holders = [c["cust"]]
        if r.random() < 0.21:
            holders.append(Wd.next_cust)
            Wd.next_cust += int(r.integers(3, 41))
        for h in holders:
            rows.append([h, c["acct"], "KIC", "%.2f" % c["core_principal"], "%.4f" % (c["rate"] / 100.0), c["term"] * 12,
                         c["issue"].isoformat(), c["maturity"].isoformat()])
    rows.sort(key=lambda x: (x[0], x[1]))
    return dict(rows=rows, kip=kip, batches=batches, certs=certs, migrated=migrated)
