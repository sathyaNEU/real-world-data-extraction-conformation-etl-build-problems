"""Indemnity payments issued 1 January to 30 September 2026, the payment register's lines, and the bank's ACH returns.

TTD and TPD are paid in arrears in the Wednesday run after each period (weekly or every two weeks, the claim's own
cadence; the first payment catches up every period accrued by then), PPD as a settlement on its award (an attorney's
fee paid to the attorney) or in two-weekly installments at the PPD rate. The register lists one line for each week a
payment covers and carries the payment's amount on each of its lines. An EFT the claimant's bank returns stays in the
register as issued; the return is in the bank's file and the payment goes out again by check."""
from __future__ import annotations

import datetime as dt
import math

import common as K

RETURN_RATE = 0.012
VOID_RATE = 0.007
REASONS = [("R01", "Insufficient funds"), ("R02", "Account closed"), ("R03", "No account/unable to locate account"),
           ("R04", "Invalid account number"), ("R16", "Account frozen")]


def wednesday_on_or_after(d):
    while d.weekday() != 2:
        d += dt.timedelta(days=1)
    return d


def _chunks(start, ndays, cadence):
    out, s, left = [], start, ndays
    while left > 0:
        k = min(cadence, left)
        out.append((s, s + dt.timedelta(days=k - 1), k))
        s += dt.timedelta(days=k)
        left -= k
    return out


def _schedule(c):
    """Every payment over the claim's life: (issue_date, benefit, payee, period_from, period_to, days, amount)."""
    pays = []
    if c.ttd > 0:
        start = c.dis_began if c.days_off > 14 else c.dis_began + dt.timedelta(days=3)
        ch = _chunks(start, c.ttd_days, c.cadence)
        amts = [round(c.ttd_rate * k / 7, 2) for _, _, k in ch]
        amts[-1] = round(c.ttd - sum(amts[:-1]), 2)
        first = wednesday_on_or_after(c.first_ind)
        pend = []
        for (a, b, k), amt in zip(ch, amts):
            iss = wednesday_on_or_after(b + dt.timedelta(days=1))
            if iss <= first:
                pend.append((a, b, k, amt))
                continue
            if pend:
                pays.append((first, "TTD", "CLAIMANT", pend[0][0], pend[-1][1], sum(x[2] for x in pend),
                             round(sum(x[3] for x in pend), 2)))
                pend = []
            pays.append((iss, "TTD", "CLAIMANT", a, b, k, amt))
        if pend:
            pays.append((first, "TTD", "CLAIMANT", pend[0][0], pend[-1][1], sum(x[2] for x in pend),
                         round(sum(x[3] for x in pend), 2)))
    if c.tpd > 0:
        back = c.dis_began + dt.timedelta(days=c.days_off)
        ch = _chunks(back + dt.timedelta(days=1), 7 * c.tpd_weeks, 14)
        amts = [round(c.tpd_weekly * k / 7, 2) for _, _, k in ch]
        amts[-1] = round(c.tpd - sum(amts[:-1]), 2)
        for (a, b, k), amt in zip(ch, amts):
            pays.append((wednesday_on_or_after(b + dt.timedelta(days=1)), "TPD", "CLAIMANT", a, b, k, amt))
    if c.ppd > 0:
        if c.ppd_lump:
            iss = wednesday_on_or_after(c.ppd_award + dt.timedelta(days=7 + (c.cid % 15)))
            if c.ppd_atty:
                fee = round(c.ppd * 0.25, 2)
                pays.append((iss, "PPD", "CLAIMANT", None, None, 0, round(c.ppd - fee, 2)))
                pays.append((iss, "PPD", "ATTORNEY", None, None, 0, fee))
            else:
                pays.append((iss, "PPD", "CLAIMANT", None, None, 0, c.ppd))
        else:
            weeks = c.ppd / c.ppd_rate
            ndays = int(math.ceil(weeks * 7 - 1e-9))
            ch = _chunks(c.ppd_award, ndays, 14)
            amts = [round(c.ppd_rate * k / 7, 2) for _, _, k in ch]
            amts[-1] = round(c.ppd - sum(amts[:-1]), 2)
            for (a, b, k), amt in zip(ch, amts):
                if amt > 0:
                    pays.append((wednesday_on_or_after(b + dt.timedelta(days=1)), "PPD", "CLAIMANT", a, b, k, amt))
    return pays


def payments(claims, stream=0):
    """The register's payments issued in January to September 2026 (one dict per payment with its lines), and the
    bank's returns of EFT payments made in the window."""
    rg = K.rng("payments", stream)
    issued = []
    for c in claims:
        if c.dup_of >= 0 or not c.ind or c.first_ind is None or c.first_ind > K.PAY_END + dt.timedelta(days=7):
            continue
        for p in _schedule(c):
            if K.PAY_START <= p[0] <= K.PAY_END:
                issued.append((p[0], c.claim_no, p, c))
    issued.sort(key=lambda x: (x[0], x[1], x[2][1], x[2][2], str(x[2][3])))
    out, rets = [], []
    pno, chk, trace = 0, 418204, 0
    reissue_q = []

    def new_payment(iss, c, benefit, payee, a, b, days, amt, method):
        nonlocal pno, chk, trace
        pno += 1
        if method == "CHK":
            chk += 1 + (1 if rg.random() < 0.01 else 0)
            ref = "%06d" % chk
        else:
            trace += 1
            ref = "0710000%08d" % (trace + 41000)
        lines = []
        if a is None:
            lines.append((None, None))
        else:
            for s, e, k in _chunks(a, days, 7):
                lines.append((s, e))
        return dict(pno="P26%07d" % pno, claim_no=c.claim_no, cid=c.cid, seg=c.seg, benefit=benefit, payee=payee,
                    method=method, ref=ref, issue=iss, amount=amt, lines=lines, status="ISSUED", void=None,
                    returned=None)

    for iss, cno, p, c in issued:
        while reissue_q and reissue_q[0][0] <= iss:
            r = reissue_q.pop(0)
            out.append(new_payment(r[0], r[1], r[2]["benefit"], r[2]["payee"], r[3], r[4], r[5], r[2]["amount"], "CHK"))
        benefit, payee, a, b, days, amt = p[1], p[2], p[3], p[4], p[5], p[6]
        method = "EFT" if (c.eft and payee == "CLAIMANT") else "CHK"
        pay = new_payment(iss, c, benefit, payee, a, b, days, amt, method)
        out.append(pay)
        u = rg.random()
        if method == "EFT" and u < RETURN_RATE:
            rdate = K.add_working(iss, int(rg.integers(2, 5)))
            if rdate <= K.PAY_END:
                code, text = REASONS[int(rg.integers(0, len(REASONS)))]
                pay["returned"] = rdate
                rets.append(dict(trace=pay["ref"], amount=amt, settle=K.next_working(iss), rdate=rdate, code=code,
                                 reason=text, name_id=c.claim_no))
                ri = wednesday_on_or_after(rdate + dt.timedelta(days=2))
                if ri <= K.PAY_END:
                    reissue_q.append((ri, c, pay, a, b, days))
                    reissue_q.sort(key=lambda x: (x[0], x[1].claim_no))
        elif method == "CHK" and u < VOID_RATE:
            vd = iss + dt.timedelta(days=int(rg.integers(20, 61)))
            if vd <= K.PAY_END:
                pay["status"] = "VOID"
                pay["void"] = vd
                ri = wednesday_on_or_after(vd + dt.timedelta(days=int(rg.integers(3, 11))))
                if ri <= K.PAY_END:
                    reissue_q.append((ri, c, pay, a, b, days))
                    reissue_q.sort(key=lambda x: (x[0], x[1].claim_no))
    for r in reissue_q:
        if r[0] <= K.PAY_END:
            out.append(new_payment(r[0], r[1], r[2]["benefit"], r[2]["payee"], r[3], r[4], r[5], r[2]["amount"], "CHK"))
    return out, rets


def paid_by_segment(pays):
    """Each programme segment's indemnity paid in the window: each payment once, issued and not returned by the bank."""
    out = {s: 0.0 for s in K.PROG}
    for p in pays:
        if p["status"] == "ISSUED" and p["returned"] is None and p["seg"] in out:
            out[p["seg"]] += p["amount"]
    return out


def clear(pays):
    return all(K.edge_distance(v, 1000) >= 150 for v in paid_by_segment(pays).values())
