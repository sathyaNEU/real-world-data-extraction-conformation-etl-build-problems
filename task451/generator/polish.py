"""Centre the asks' figures in their rounding bins without touching the call: the pharmacy file's amounts (pharmacy is
outside the total cost of care) and, for the professional-services share, which of a partner member's small
professional claims an in-partner clinician rendered rather than an outside one (amounts unchanged, so the total cost of
care does not move). Deterministic: the same rows are chosen on every build."""
import csv
import os

import numpy as np
import pandas as pd

import calc as C
import pack as P
import world as W

RX_EDGE = 150.0          # dollars from a thousand-dollar rounding edge
SHARE_EDGE = 0.025       # percentage points from a one-decimal rounding edge


def _write(path, df):
    df.to_csv(path, index=False, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)


def rx(target):
    L = C.load(target)
    att = C.attribution(L["roster"])
    fam = C.rx_members(L["elig"])
    rx = L["rx"]
    elig = C.eligible_months(L["elig"])
    tot = C.ask_pharmacy(L, att, "dob", elig)
    k = C.mkey_series(rx["fill_date"])
    mids = [next(iter(fam.get((c, b, g), {None}))) for c, b, g in zip(rx["cardholder_id"], rx["patient_birth_date"], rx["patient_gender"])]
    part = np.array([att.get((m, kk)) if (m, kk) in elig else None for m, kk in zip(mids, k)], dtype=object)
    reversed_rx = set(rx.loc[rx["transaction_code"] == "B2", "rx_number"])
    moved = {}
    for code in W.CODES:
        frac = tot[code] / 1000.0 - np.floor(tot[code] / 1000.0)
        dist = min(abs(frac - 0.5), 1.0) * 1000.0
        if dist >= RX_EDGE:
            continue
        shift = 300.0 if frac < 0.5 else -300.0
        rows = rx.index[(part == code) & (rx["transaction_code"] == "B1") & ~rx["rx_number"].isin(reversed_rx)
                        & (rx["plan_paid"] > 60)]
        pick = rows[:6]
        each = round(shift / len(pick), 2)
        for i in pick:
            rx.at[i, "ingredient_cost"] = round(rx.at[i, "ingredient_cost"] + each, 2)
            rx.at[i, "plan_paid"] = round(rx.at[i, "plan_paid"] + each, 2)
        moved[code] = each * len(pick)
    for col in ("ingredient_cost", "dispensing_fee", "patient_pay", "plan_paid"):
        rx[col] = rx[col].map(lambda v: "%.2f" % v)
    rx["quantity"] = rx["quantity"].map(lambda v: "%g" % v)
    _write(os.path.join(target, P.FILES["rx"]), rx)
    return moved


def leakage(target, group_npi, clinicians):
    """for a partner whose share sits within SHARE_EDGE of a rounding edge, small outside professional claims of its
    members become in-partner (rendered by one of its PCPs, billed under its group NPI), or the reverse"""
    L = C.load(target)
    cl = L["claims"]
    fc = C.final_claims(cl)
    att = C.attribution(L["roster"])
    d26 = C.frame2026(fc, att)
    share = C.ask_leakage(L, d26, group_npi, "billing")
    single = set(cl.groupby("claim_number").size().loc[lambda s: s == 1].index)
    movers = set(clinicians["movers"])
    changed = {}
    for code in W.CODES:
        frac = share[code] * 10 - np.floor(share[code] * 10)
        if min(abs(frac - 0.5), 1.0) / 10 >= SHARE_EDGE:
            continue
        prof = d26[d26["claim_form"].eq("CMS1500") & d26["partner"].eq(code)]
        tot = prof["paid_amount"].sum()
        want = (0.05 if frac < 0.5 else -0.05) / 100 * tot        # move the outside amount by about half a bin
        if want > 0:     # more outside: in-partner claims by non-movers become outside
            pool = prof[(prof["billing_npi"] == group_npi[code]) & prof["claim_number"].isin(single) & ~prof["rendering_npi"].isin(movers)]
        else:
            pool = prof[(prof["billing_npi"] != group_npi[code]) & prof["claim_number"].isin(single)]
        pool = pool.sort_values(["paid_amount", "claim_number"])
        acc, pick = 0.0, []
        for r in pool.itertuples():
            if r.paid_amount <= 0:
                continue
            pick.append(r.claim_number)
            acc += r.paid_amount
            if acc >= abs(want):
                break
        pcp = clinicians["pcp"][code][0]
        out_n, out_b = clinicians["outside_example"]
        sel = cl["claim_number"].isin(pick)
        if want > 0:
            cl.loc[sel, "rendering_npi"] = out_n
            cl.loc[sel, "billing_npi"] = out_b
        else:
            cl.loc[sel, "rendering_npi"] = pcp
            cl.loc[sel, "billing_npi"] = group_npi[code]
        changed[code] = len(pick)
    for col in ("billed_amount", "allowed_amount", "paid_amount", "payment_amount"):
        cl[col] = cl[col].map(lambda v: "%.2f" % v)
    for col in ("bill_type", "place_of_service", "admission_date", "rendering_npi", "billing_npi"):
        cl[col] = cl[col].fillna("")
    _write(os.path.join(target, P.FILES["claims"]), cl)
    return changed
