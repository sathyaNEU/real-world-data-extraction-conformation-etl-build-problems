"""The credit bureau's portfolio review of the pool's borrowers at the cut-off.

One row per account the bureau holds for an inquired borrower, with the bureau's consumer summary repeated on every
row (the number of member codes with an active microfinance account and the total active microfinance balance, as
the bureau computes them). Microfinance accounts are the JLG and MFI-IND account types; gold loans, Kisan credit
cards and consumer-durable loans sit in the same file.

What the records hold that the summary does not know:
- Salandi Microfinance converted into Salandi Small Finance Bank on 1 July 2025; loans made before the conversion stay
  under the old member code and later loans report under the bank's. The member directory records the conversion.
- Gandhamardan Gramya Bank reports the loans its business correspondent originates under a second member code, listed in the
  directory as the bank's BC portfolio.
- Nirmala Small Finance Bank moved its loan accounts to a new core on 14 March 2026 under new account numbers; for
  many accounts the old number was never closed on the bureau, so the old row still shows active at the balance it
  carried then, last reported on 13 March 2026, beside the new row carrying the same loan."""
from __future__ import annotations

import datetime as dt

import numpy as np

import params as P

LENDERS = [
    # member code, name, type, weight on coastal borrowers, weight inland
    ("MFI0447", "Salandi Microfinance Ltd", "NBFC-MFI", 0.30, 0.18),
    ("MFI0518", "Kalinga Sakhi Microfinance Pvt Ltd", "NBFC-MFI", 0.26, 0.16),
    ("SFB0014", "Nirmala Small Finance Bank Ltd", "SFB", 0.42, 0.40),
    ("MFI0590", "Shaktigram Finance Pvt Ltd", "NBFC-MFI", 0.18, 0.14),
    ("NBF0233", "Mahanadi Credit Foundation Ltd", "NBFC", 0.14, 0.18),
    ("MFI0701", "Swarnadeep Microcredit Pvt Ltd", "NBFC-MFI", 0.12, 0.10),
    ("BNK0102", "Gandhamardan Gramya Bank", "Bank", 0.12, 0.14),
    ("SFB0037", "Deepti Small Finance Bank Ltd", "SFB", 0.08, 0.10),
    ("NBF0412", "Parivartan Fincorp Ltd", "NBFC", 0.06, 0.08),
    ("MFI0734", "Udayagiri Microcredit Pvt Ltd", "NBFC-MFI", 0.05, 0.06),
]
SELLER = ("MFI0612", "Prachi Valley Microfinance Pvt Ltd", "NBFC-MFI")
SALANDI_SFB = ("SFB0029", "Salandi Small Finance Bank Ltd", "SFB")
GANDHAMARDAN_BC = ("BNK0115", "Gandhamardan Gramya Bank - BC Portfolio", "Bank")
CONVERSION = dt.date(2025, 7, 1)
NIRMALA_MIGRATION = dt.date(2026, 3, 14)
LAST_REPORT = dt.date(2026, 12, 26)
COASTAL = {"Kendrapara", "Jagatsinghpur", "Bhadrak", "Balasore"}
MF_TYPES = ("JLG", "MFI-IND")
LIMIT_LENDERS = 4
LIMIT_DEBT = 200000
MIN_FLIPS = 3          # each branch carries at least this many borrowers the stale rows push over the debt line
ENTITY = {"MFI0447": "SALANDI", "SFB0029": "SALANDI", "BNK0102": "GANDHAMARDAN", "BNK0115": "GANDHAMARDAN"}


def directory():
    rows = [dict(member_code=SELLER[0], institution=SELLER[1], institution_type=SELLER[2], status="ACTIVE",
                 parent_code="", successor_code="", status_date="")]
    for code, name, typ, _, _ in LENDERS:
        if code == "MFI0447":
            rows.append(dict(member_code=code, institution=name, institution_type=typ, status="CONVERTED",
                             parent_code="", successor_code=SALANDI_SFB[0], status_date=CONVERSION.isoformat()))
        else:
            rows.append(dict(member_code=code, institution=name, institution_type=typ, status="ACTIVE",
                             parent_code="", successor_code="", status_date=""))
    rows.append(dict(member_code=SALANDI_SFB[0], institution=SALANDI_SFB[1], institution_type=SALANDI_SFB[2],
                     status="ACTIVE", parent_code="", successor_code="", status_date=CONVERSION.isoformat()))
    rows.append(dict(member_code=GANDHAMARDAN_BC[0], institution=GANDHAMARDAN_BC[1], institution_type=GANDHAMARDAN_BC[2],
                     status="ACTIVE", parent_code="BNK0102", successor_code="", status_date=""))
    return rows


def _bal(sanc, opened, asof, rng, jitter=0.05):
    frac = 1 - (asof - opened).days / 730.0 + (rng.normal(0, jitter) if jitter else 0.0)
    return int(round(sanc * min(max(frac, 0.08), 1.0)))


def tally(accts):
    live = [a for a in accts if a["type"] in MF_TYPES and a["status"] == "ACTIVE"]
    true = [a for a in live if not a.get("stale")]
    lenders = len({ENTITY.get(a["code"], a["code"]) for a in true})
    debt = sum(a["balance"] for a in true)
    return lenders, debt, sum(a["balance"] for a in live), len({a["code"] for a in live})


def build(pool, seed):
    """pool: list of dicts (member_id, cic_ref, district, branch, principal, sanctioned, disbursed). Returns tradeline
    rows (dicts) and the truth per borrower."""
    rng = np.random.default_rng(seed)
    per = {}
    for m in pool:
        coastal = m["district"] in COASTAL
        accts = [dict(code=SELLER[0], name=SELLER[1], type="JLG", opened=m["disbursed"], sanctioned=m["sanctioned"],
                      balance=m["principal"], reported=LAST_REPORT, closed=None, status="ACTIVE", dpd=0)]
        n_other = int(rng.choice([0, 1, 2, 3, 4], p=([0.22, 0.30, 0.26, 0.15, 0.07] if coastal
                                                     else [0.34, 0.31, 0.22, 0.10, 0.03])))
        w = np.array([(l[3] if coastal else l[4]) for l in LENDERS], dtype=float)
        w /= w.sum()
        picks = list(rng.choice(len(LENDERS), size=n_other, replace=False, p=w)) if n_other else []
        for i in picks:
            code, name, typ, _, _ = LENDERS[i]
            opened = P.CUTOFF - dt.timedelta(days=int(rng.integers(40, 700)))
            sanc = int(rng.integers(35, 91)) * 1000
            bal = _bal(sanc, opened, P.CUTOFF, rng)
            atype = "JLG" if rng.random() < 0.8 else "MFI-IND"
            if code == "MFI0447" and opened >= CONVERSION:
                code, name = SALANDI_SFB[0], SALANDI_SFB[1]
            if code == "BNK0102" and rng.random() < 0.5:
                code, name = GANDHAMARDAN_BC[0], GANDHAMARDAN_BC[1]
            accts.append(dict(code=code, name=name, type=atype, opened=opened, sanctioned=sanc, balance=bal,
                              reported=LAST_REPORT - dt.timedelta(days=int(rng.integers(0, 21))), closed=None,
                              status="ACTIVE", dpd=int(rng.choice([0, 0, 0, 0, 0, 0, 0, 15, 30, 45]))))
            # a Salandi borrower with a pre-conversion loan often took a second one from the bank; a direct Gandhamardan
            # borrower sometimes also holds a loan through its correspondent
            if LENDERS[i][0] == "MFI0447" and opened < CONVERSION and rng.random() < 0.55:
                op2 = CONVERSION + dt.timedelta(days=int(rng.integers(10, (P.CUTOFF - CONVERSION).days - 30)))
                s2 = int(rng.integers(30, 61)) * 1000
                accts.append(dict(code=SALANDI_SFB[0], name=SALANDI_SFB[1], type="JLG", opened=op2, sanctioned=s2,
                                  balance=_bal(s2, op2, P.CUTOFF, rng, 0.0),
                                  reported=LAST_REPORT - dt.timedelta(days=int(rng.integers(0, 14))), closed=None,
                                  status="ACTIVE", dpd=0))
            if LENDERS[i][0] == "BNK0102" and code == "BNK0102" and rng.random() < 0.45:
                op2 = P.CUTOFF - dt.timedelta(days=int(rng.integers(30, 400)))
                s2 = int(rng.integers(30, 61)) * 1000
                accts.append(dict(code=GANDHAMARDAN_BC[0], name=GANDHAMARDAN_BC[1], type="JLG", opened=op2, sanctioned=s2,
                                  balance=_bal(s2, op2, P.CUTOFF, rng, 0.0),
                                  reported=LAST_REPORT - dt.timedelta(days=int(rng.integers(0, 14))), closed=None,
                                  status="ACTIVE", dpd=0))
            if code == "SFB0014" and opened < NIRMALA_MIGRATION and rng.random() < 0.85:
                accts.append(dict(code=code, name=name, type=atype, opened=opened, sanctioned=sanc,
                                  balance=_bal(sanc, opened, NIRMALA_MIGRATION, rng, 0.0),
                                  reported=dt.date(2026, 3, 13), closed=None, status="ACTIVE", dpd=0, stale=True))
        for _ in range(int(rng.choice([0, 1, 1, 2, 3]))):
            code, name, typ, _, _ = LENDERS[int(rng.choice(len(LENDERS), p=w))]
            opened = P.CUTOFF - dt.timedelta(days=int(rng.integers(500, 1600)))
            closed = opened + dt.timedelta(days=int(rng.integers(300, 730)))
            if closed >= P.CUTOFF:
                closed = P.CUTOFF - dt.timedelta(days=int(rng.integers(20, 200)))
            accts.append(dict(code=code, name=name, type="JLG", opened=opened,
                              sanctioned=int(rng.integers(25, 61)) * 1000, balance=0, reported=closed, closed=closed,
                              status="CLOSED", dpd=0))
        if rng.random() < 0.22:
            accts.append(dict(code="BNK0102", name="Gandhamardan Gramya Bank", type=str(rng.choice(["GOLD", "KCC"])),
                              opened=P.CUTOFF - dt.timedelta(days=int(rng.integers(30, 600))),
                              sanctioned=int(rng.integers(20, 151)) * 1000, balance=int(rng.integers(10, 120)) * 1000,
                              reported=LAST_REPORT, closed=None, status="ACTIVE", dpd=0))
        per[m["member_id"]] = accts
    # every branch carries at least MIN_FLIPS borrowers whom the stale rows alone push over the debt line: where a
    # branch has too few, a borrower just under the line with no Nirmala loan is given one, under both numbers
    by_branch = {}
    for m in pool:
        by_branch.setdefault(m["branch"], []).append(m)
    for b in sorted(by_branch):
        ms = by_branch[b]

        def flips():
            n = 0
            for m in ms:
                le, de, ds, _ = tally(per[m["member_id"]])
                if le < LIMIT_LENDERS and de <= LIMIT_DEBT < ds:
                    n += 1
            return n
        # candidates: a borrower just under the debt line, either holding a Nirmala loan opened before the migration
        # with no old-number row yet (its old number is left active), or with room for one more lender
        twin, fresh = [], []
        for m in ms:
            acc = per[m["member_id"]]
            le, de, ds, _ = tally(acc)
            if ds != de or de > LIMIT_DEBT:
                continue
            nir = [a for a in acc if a["code"] == "SFB0014" and a["status"] == "ACTIVE" and a["type"] in MF_TYPES
                   and a["opened"] < NIRMALA_MIGRATION]
            if nir and le < LIMIT_LENDERS:
                a = nir[0]
                old = _bal(a["sanctioned"], a["opened"], NIRMALA_MIGRATION, rng, 0.0)
                if de + old > LIMIT_DEBT:
                    twin.append((m, a, old))
            elif not nir and le < LIMIT_LENDERS - 1 and 120000 < de <= LIMIT_DEBT - 20000:
                fresh.append(m)
        order_t = list(rng.permutation(len(twin)))
        order_f = list(rng.permutation(len(fresh)))
        while flips() < MIN_FLIPS and (order_t or order_f):
            if order_t:
                m, a, old = twin[order_t.pop()]
                per[m["member_id"]].append(dict(a, balance=old, reported=dt.date(2026, 3, 13), stale=True))
                continue
            m = fresh[order_f.pop()]
            le, de, _, _ = tally(per[m["member_id"]])
            now_bal = int(rng.integers(5, (LIMIT_DEBT - de) // 1000)) * 1000
            old_bal = LIMIT_DEBT - de + int(rng.integers(10, 40)) * 1000
            sanc = int(round(max(old_bal, now_bal) * 1.5 / 1000.0)) * 1000
            opened = NIRMALA_MIGRATION - dt.timedelta(days=int(rng.integers(60, 300)))
            base = dict(code="SFB0014", name="Nirmala Small Finance Bank Ltd", type="JLG", opened=opened,
                        sanctioned=sanc, closed=None, status="ACTIVE", dpd=0)
            per[m["member_id"]].append(dict(base, balance=now_bal,
                                            reported=LAST_REPORT - dt.timedelta(days=int(rng.integers(0, 14)))))
            per[m["member_id"]].append(dict(base, balance=max(old_bal, now_bal + 5000), reported=dt.date(2026, 3, 13),
                                            stale=True))
    rows, truth = [], {}
    for m in pool:
        accts = per[m["member_id"]]
        le, de, ds, codes = tally(accts)
        truth[m["member_id"]] = dict(lenders=le, debt=de, breach=(le >= LIMIT_LENDERS or de > LIMIT_DEBT),
                                     codes=codes, debt_with_stale=ds)
        for a in sorted(accts, key=lambda x: (x["code"], x["opened"].isoformat(), x["reported"].isoformat())):
            rows.append(dict(inquiry_ref=m["cic_ref"], member_code=a["code"], member_name=a["name"],
                             account_no="%s%010d" % (a["code"][:3], int(rng.integers(10 ** 9, 10 ** 10 - 1))),
                             account_type=a["type"], date_opened=a["opened"], date_reported=a["reported"],
                             date_closed=a["closed"] or "", sanctioned_amount=a["sanctioned"],
                             current_balance=a["balance"], days_past_due=a["dpd"], account_status=a["status"],
                             summary_active_mfi_lenders=codes, summary_mfi_outstanding=ds))
    return rows, truth
