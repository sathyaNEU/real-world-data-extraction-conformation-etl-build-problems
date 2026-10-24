"""The billing system's 2026-27 invoice register as of 20 November 2026, and where each credit goes: the open
2026-27 subscription invoice on the order form's bill-to account with the earliest due date, or a refund by check
when none is open (MSA section 10.1 and the credit memo import layout)."""
import datetime as dt

import numpy as np

import world as W

AS_OF = dt.date(2026, 11, 20)
CREDIT_DATE = dt.date(2026, 11, 30)
NOT_RENEWED = (11, 33, 50)          # district positions without a 2026-27 order form


def term_2627(dd):
    a = dd["term_start"].replace(year=2026)
    return a, dd["term_end"].replace(year=2027)


def build():
    r = np.random.default_rng(W.SEED + 31)
    inv = []
    no = [261000]

    def add(dd, account, when, due, svc, desc, amount, paid):
        no[0] += int(r.integers(3, 29))
        paid_on = None
        if paid:
            paid_on = min(AS_OF - dt.timedelta(days=2), due + dt.timedelta(days=int(r.integers(-25, 40))))
            paid_on = max(paid_on, when + dt.timedelta(days=9))
        inv.append(dict(invoice_number="INV-%d" % no[0], customer_account=account,
                        bill_to=dd["crm_name"] if account == dd["account"] else dd["crm_name"] + " Virtual Academy",
                        partner_id=dd["partner_id"], invoice_date=when, due_date=due,
                        service_start=svc[0] if svc else None, service_end=svc[1] if svc else None,
                        description=desc, amount=round(amount, 2), paid_on=paid_on,
                        balance=0.0 if paid else round(amount, 2), status="Paid" if paid else "Open"))

    for dd in W.DISTRICTS:
        j = dd["j"]
        a, z = term_2627(dd)
        fee = round(dd["seats"] * (1 + float(r.choice([-0.08, 0.0, 0.0, 0.04, 0.08]))) // 50 * 50 *
                    round(dd["seat_price"] * 1.03 * 4) / 4, 2)
        if j not in NOT_RENEWED:
            if dd["billing"] == "Annual":
                add(dd, dd["account"], a, a + dt.timedelta(days=45), (a, z), "Lumenfold subscription 2026-27, annual",
                    fee, r.random() < 0.72)
            else:
                add(dd, dd["account"], a, a + dt.timedelta(days=45), (a, z),
                    "Lumenfold subscription 2026-27, semester 1 instalment", fee / 2, r.random() < 0.75)
                when = dt.date(2026, 11, 16)
                add(dd, dd["account"], when, when + dt.timedelta(days=45), (a, z),
                    "Lumenfold subscription 2026-27, semester 2 instalment", fee / 2, False)
        if "va_account" in dd and j not in NOT_RENEWED:
            add(dd, dd["va_account"], a, a + dt.timedelta(days=45), (a, z),
                "Lumenfold subscription 2026-27, annual", round(fee * r.uniform(0.08, 0.16) / 25) * 25,
                r.random() < 0.3)
    order = r.permutation(len(W.DISTRICTS))
    for j in order[:9]:                       # seat true-ups for the 2025-26 term, invoiced after it closed
        dd = W.DISTRICTS[j]
        when = dt.date(2026, 8, 17)
        extra = int(r.integers(1, 4)) * 25
        add(dd, dd["account"], when, when + dt.timedelta(days=45), (dd["term_start"], dd["term_end"]),
            "Lumenfold subscription seat true-up 2025-26", extra * dd["seat_price"], r.random() < 0.3)
    for j in order[9:16]:                     # professional learning bought for 2026-27
        dd = W.DISTRICTS[j]
        a, z = term_2627(dd)
        when = dt.date(2026, 9, 8)
        add(dd, dd["account"], when, when + dt.timedelta(days=45), (a, z), "Professional learning add-on 2026-27",
            float(r.choice([1500, 2250, 3000])), r.random() < 0.3)
    for j in order[16:22]:                    # lab kits
        dd = W.DISTRICTS[j]
        when = dt.date(2026, 8, 25)
        add(dd, dd["account"], when, when + dt.timedelta(days=45), None, "Lab kit order",
            float(r.choice([640, 960, 1280, 1920])), r.random() < 0.5)
    inv.sort(key=lambda x: (x["invoice_date"], x["invoice_number"]))
    return inv


def target_invoice(dd, inv):
    """The invoice a credit for district dd is applied to, or None for a refund by check."""
    a, _ = term_2627(dd)
    cands = [x for x in inv if x["customer_account"] == dd["account"] and x["status"] == "Open"
             and x["service_start"] == a and x["description"].startswith("Lumenfold subscription 2026-27")]
    if not cands:
        return None
    return min(cands, key=lambda x: (x["due_date"], x["invoice_number"]))
