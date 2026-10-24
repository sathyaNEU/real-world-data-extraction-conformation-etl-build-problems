"""The golden settlement: each district's Outcome Share re-estimated from its eligible students' own responses with
the district in the population model, its guarantee result and credit, its live professional learning hours in the
subscription term and any shortfall credit, and the credit memos in the import layout."""
import numpy as np

import world as W
import irt
import billing as BL
import pd as PD


def eligible_view(v):
    el = v["eligible"]
    return {k: (val[el] if isinstance(val, np.ndarray) and len(val) == len(el) else val) for k, val in v.items()}


def golden_shares(v):
    """The district-conditioned latent regression (district, grade, prior band, background) on the eligible students
    who completed the assessment; each district's share is the mean posterior probability of being at or above
    Proficient for the student's grade."""
    ve = eligible_view(v)
    m = np.ones(len(ve["g"]), bool)
    w, gam, s2 = irt.lr_em(ve["L"], irt.X_of(ve, "gold", m))
    return irt.share_post(ve["dist"], ve["g"], w, ve["D"]), w, ve


def settle(v, pd_truth, inv):
    share, w, ve = golden_shares(v)
    n_assessed = np.bincount(ve["dist"], minlength=ve["D"])
    rows, memos = [], []
    for dd in W.DISTRICTS:
        j = dd["j"]
        owed = share[j] < dd["benchmark"]
        og = round(dd["fee"] * dd["credit_pct"] / 100.0, 2) if owed else 0.0
        delivered = PD.half_hours(pd_truth[dd["partner_id"]] / 60.0)
        short = max(0.0, dd["pd_hours"] - delivered)
        pl = round(short * 250.0, 2)
        tgt = BL.target_invoice(dd, inv)
        rows.append(dict(partner_id=dd["partner_id"], name=dd["name"], state=dd["state"], order_form=dd["order_form"],
                         assessed=int(n_assessed[j]), share=float(share[j]), benchmark=dd["benchmark"],
                         result="Not met" if owed else "Met", credit_pct=dd["credit_pct"], fee=dd["fee"], og=og,
                         pd_contract=dd["pd_hours"], pd_delivered=delivered, pd_short=short, pl=pl, total=og + pl,
                         invoice=tgt["invoice_number"] if tgt else "", account=dd["account"]))
        for code, amt in (("OG", og), ("PL", pl)):
            if amt > 0:
                memos.append(dict(memo_reference="%s-2526-%s" % (code, dd["partner_id"][3:]),
                                  customer_account=dd["account"], reason_code=code, credit_amount=amt,
                                  apply_to_invoice=tgt["invoice_number"] if tgt else "",
                                  refund_method="APPLY" if tgt else "CHECK", credit_date=BL.CREDIT_DATE.isoformat(),
                                  partner_id=dd["partner_id"]))
    memos.sort(key=lambda x: x["memo_reference"])
    return rows, memos, share
