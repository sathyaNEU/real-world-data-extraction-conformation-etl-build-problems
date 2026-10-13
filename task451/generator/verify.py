"""Independent verifier for task451: reads only target/ (and figures.json to compare), imports nothing from the
generator, and recomputes the call (received-date completion), the default path's call (paid-date chain ladder over all
development), each partner's pharmacy spending and its share of professional spending outside the group."""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CUT = dt.date(2027, 1, 29)
FAILS = []


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def mk(s):
    d = pd.to_datetime(s)
    return (d.dt.year * 12 + d.dt.month - 1).to_numpy()


def main(target, golden=None):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, "accountable_care_partner_agreement_schedule_b.pdf")).pages)
    rows = re.findall(r"\b([A-Z]{3})\s+(\d{10})\s+([\d,]+\.\d\d)", txt)
    tg = {c: float(v.replace(",", "")) for c, _, v in rows}
    gn = {c: n for c, n, _ in rows}
    check(len(tg) == 12, "Exhibit 1 lists twelve partners")
    cl = pd.read_csv(os.path.join(target, "medical_claims_extract_2025-01_2027-01.csv"), dtype=str)
    for col in ("paid_amount", "payment_amount"):
        cl[col] = cl[col].astype(float)
    cl["claim_version"] = cl["claim_version"].astype(int)
    last = cl.sort_values(["claim_number", "claim_version"]).groupby("claim_number").tail(1).set_index("claim_number")
    first = cl[cl["claim_version"] == 1].set_index("claim_number")
    last["received_date"] = first["received_date"]
    fc = last.reset_index()
    el = pd.read_csv(os.path.join(target, "eligibility_spans_2025-2027.csv"), dtype=str)
    el["span_version"] = el["span_version"].astype(int)
    lv = el.sort_values(["span_id", "span_version"]).groupby("span_id").tail(1)
    covered = set()
    for r in lv.itertuples():
        a = dt.date.fromisoformat(r.coverage_start)
        b = dt.date.fromisoformat(r.coverage_end) if isinstance(r.coverage_end, str) and r.coverage_end else dt.date(2027, 1, 31)
        if b < a:
            continue
        for k in range(a.year * 12 + a.month - 1, b.year * 12 + b.month):
            covered.add((r.member_id, k))
    ro = pd.read_csv(os.path.join(target, "attribution_roster_2026.csv"), dtype=str)
    ro["k"] = mk(ro["roster_month"])
    att = {(m, k): p for m, k, p in zip(ro["member_id"], ro["k"], ro["partner_code"])}
    mm = {}
    for (m, k), p in att.items():
        if (m, k) in covered:
            mm[p] = mm.get(p, 0) + 1
    check(all(mm[c] == F["member_months"][c] for c in tg), "attributed member months match figures.json for every partner")
    fc["k"] = mk(fc["service_from_date"])
    d = fc[(fc["k"] >= 2026 * 12) & (fc["k"] < 2027 * 12)].copy()
    d["p"] = [att.get((m, k)) for m, k in zip(d["member_id"], d["k"])]
    tot = d.groupby("member_id")["paid_amount"].sum()
    exc = {c: 0.0 for c in tg}
    for mid, t in tot[tot > 200000].items():
        for p, a in d[(d["member_id"] == mid) & d["p"].notna()].groupby("p")["paid_amount"].sum().items():
            exc[p] += (t - 200000) * a / t
    s0, cm = 2025 * 12, 2027 * 12
    n = cm - s0 + 1

    def tri(df, col, datecol):
        T = np.zeros((n, n))
        s = mk(df["service_from_date"]) - s0
        L = mk(df[datecol]) - mk(df["service_from_date"])
        for i, l_, v in zip(s, L, df[col]):
            if 0 <= i < n and 0 <= l_ < n:
                T[i, l_] += v
        return np.cumsum(T, axis=1)

    def cf(T, keep=None):
        f = np.ones(n)
        for L in range(n - 1):
            num = den = 0.0
            for i in range(n - L - 1):
                if keep is not None and not keep(s0 + i + L + 1):
                    continue
                num += T[i, L + 1]
                den += T[i, L]
            f[L] = num / den if den else 1.0
        return np.array([np.prod(f[n - 1 - i:n - 1]) if n - 1 - i < n - 1 else 1.0 for i in range(n)])

    Tr = tri(fc, "paid_amount", "received_date")
    Tp = tri(cl, "payment_amount", "paid_date")
    amt = {c: np.zeros(12) for c in tg}
    for (p, k), v in d[d["p"].notna()].groupby(["p", "k"])["paid_amount"].sum().items():
        amt[p][k - 2026 * 12] += v
    i0 = 2026 * 12 - s0

    def owe(c_):
        pm = {c: (float(np.dot(c_[i0:i0 + 12], amt[c])) - exc[c]) / mm[c] for c in tg}
        return sorted(c for c in tg if pm[c] > tg[c] * 1.02), pm

    gold, pm = owe(cf(Tr))
    check(gold == sorted(F["call_codes"]), "received-date completion names %s (figures.json %s)" % (gold, sorted(F["call_codes"])))
    check(all(abs(pm[c] - F["golden_tcoc_pmpm"][c]) < 0.01 for c in tg), "every partner's golden TCOC PMPM recomputes to the cent")
    post, pm3 = owe(cf(Tp, lambda m: m > 2026 * 12 + 9))
    check(post == gold, "the paid-date chain ladder on the payments after the go-live month names the same partners")
    g2, pm2 = owe(cf(Tr, lambda m: m > cm - 12))
    Tf = tri(fc, "paid_amount", "paid_date")
    g5, _ = owe(cf(Tf, lambda m: m > 2026 * 12 + 9))
    check(g5 == gold, "the paid-date chain ladder on latest versions, payments after the go-live month, names the same partners")
    check(g2 == gold, "the received-date chain ladder on the latest twelve receipt months names the same partners")
    # by claim type: professional, outpatient (UB-04 0131), inpatient (UB-04 0111)
    kinds = {"P": lambda f: f["claim_form"] == "CMS1500", "O": lambda f: (f["claim_form"] == "UB04") & (f["bill_type"] == "0131"),
             "I": lambda f: (f["claim_form"] == "UB04") & (f["bill_type"] == "0111")}
    pm4 = {c: 0.0 for c in tg}
    for t, sel in kinds.items():
        ct = cf(tri(fc[sel(fc)], "paid_amount", "received_date"))
        sub = d[sel(d) & d["p"].notna()]
        for (p, k), v in sub.groupby(["p", "k"])["paid_amount"].sum().items():
            pm4[p] += ct[i0 + k - 2026 * 12] * v
    pm4 = {c: (pm4[c] - exc[c]) / mm[c] for c in tg}
    check(sorted(c for c in tg if pm4[c] > tg[c] * 1.02) == gold, "the received-date chain ladder by claim type names the same partners")
    for c in gold:
        v = [100 * x[c] / tg[c] for x in (pm, pm2, pm4)]
        check(["%.1f" % min(v), "%.1f" % max(v)] == F["received_ratio_range_pct"][c],
              "%s share of target %.1f%% to %.1f%% across the three received-date completions (figures.json %s)" % (c, min(v), max(v), F["received_ratio_range_pct"][c]))
    dflt, _ = owe(cf(Tp))
    check(dflt == sorted(F["routes"]["R0 paid, all development"]) and dflt != gold,
          "the paid-date chain ladder over all development names %s" % dflt)
    raw, _ = owe(np.ones(n))
    check(raw == sorted(F["routes"]["R1 paid as extracted"]), "paid as extracted names %s" % raw)
    # pharmacy: the patient matched to the member by cardholder, birth date and sex; fills in the member's attributed
    # member months (on the roster for the fill month and eligible in it)
    rx = pd.read_csv(os.path.join(target, "corvane_pharmacy_claims_2026.csv"), dtype=str)
    rx["plan_paid"] = rx["plan_paid"].astype(float)
    sign = rx["transaction_code"].map({"B1": 1.0, "B3": 1.0, "B2": -1.0})
    who = {}
    for r in lv.itertuples():
        who[(r.subscriber_id, r.birth_date, r.gender)] = r.member_id
    rx["m"] = [who.get((a, b, g)) for a, b, g in zip(rx["cardholder_id"], rx["patient_birth_date"], rx["patient_gender"])]
    rx["k"] = mk(rx["fill_date"])
    rx["p"] = [att.get((m, k)) if (m, k) in covered else None for m, k in zip(rx["m"], rx["k"])]
    ph = (rx["plan_paid"] * sign).groupby(rx["p"]).sum()
    check(all(int(round(ph[c] / 1000.0)) * 1000 == F["pharmacy_stated"][c] for c in tg), "every partner's pharmacy spending recomputes to the thousand")
    # professional spending outside the group: the claim's billing group
    pr = d[(d["claim_form"] == "CMS1500") & d["p"].notna()]
    out = {}
    for p, g in pr.groupby("p"):
        out[p] = g.loc[g["billing_npi"] != gn[p], "paid_amount"].sum() / g["paid_amount"].sum() * 100
    check(all("%.1f" % out[c] == F["outside_share_stated"][c] for c in tg), "every partner's outside share recomputes to one decimal")
    print("verify: %d failed" % len(FAILS))
    return not FAILS


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")) else 1)
