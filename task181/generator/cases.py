"""The fraud desk's case workbook and the chargeback log.

A claim is what a member reports; the workbook carries one row per disputed transaction under the
claim's case number. Refunds post on business days. A claim closed for want of the member's signed
declaration and re-opened when the member calls back gets a new case number and repeats its
transactions. Chargebacks are raised on the disputed transactions where the network allows it; a
credit lost at pre-arbitration is taken back as a later, negative row.
"""
import datetime as dt

import numpy as np
import pandas as pd

import world as W
import sim as S
import fraud as F
import messages as M

DAY = S.DAY
LAST_BD = dt.date(2026, 10, 2)          # last business day before the extract


def is_bd(d):
    return d.weekday() < 5 and d not in W.HOLIDAY_SET


def next_bd(d):
    while not is_bd(d):
        d += dt.timedelta(1)
    return d


def add_bd(d, k):
    x, n = d, 0
    while n < k:
        x += dt.timedelta(1)
        if is_bd(x):
            n += 1
    return x


def bd_between(a, b):
    n, x = 0, a
    while x < b:
        x += dt.timedelta(1)
        if is_bd(x):
            n += 1
    return n


def local_date(t):
    return S.date_of(int(t) // DAY)


def descriptor(m):
    town = m["town"].upper()
    return "%s %s %s" % (m["name"].upper()[:23].strip(), town, m["prov"])


def build(fr):
    rng = np.random.default_rng(W.SEED + 83)
    cat, ev, toks = fr.cat, fr.ev, fr.tokens
    tag_of = {"Counterfeit": F.T_CF, "Card not present": F.T_CNPF, "Lost or stolen": F.T_LSF}
    fe = ev[ev.tag.isin([F.T_CF, F.T_CNPF, F.T_LSF]) & (ev.resp == 0) & (ev.kind != S.K_BAL)]
    by_slot = {s: g for s, g in fe.groupby("slot", sort=True)}
    claims = []
    for s, rep in sorted(fr.reports.items(), key=lambda kv: (kv[1], kv[0])):
        kind = fr.kinds[s]
        g = by_slot.get(s)
        if g is None:
            continue
        g = g[(g.tag == tag_of[kind]) & (g.t < rep)]
        if not len(g):
            continue
        tok = int(g.tok.iat[0])
        claims.append({"slot": s, "kind": kind, "report_t": int(rep), "tok": tok,
                       "card_type": toks.card_type.iat[tok], "rows": g.index.tolist()})
    # refund timing --------------------------------------------------------------------------------
    waits = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    pw = np.array([.07, .13, .15, .15, .13, .10, .08, .06, .05, .04, .025, .015])
    for c in claims:
        rd = local_date(c["report_t"])
        c["day0"] = next_bd(rd)
        c["k"] = int(rng.choice(waits, p=pw / pw.sum()))
        c["evening"] = (c["report_t"] % DAY) >= 20 * 3600
        c["role"] = None
    cf = [c for c in claims if c["kind"] == "Counterfeit"]

    def pick(pool, n, role):
        idx = [i for i in rng.permutation(len(pool))][:n]
        out = [pool[i] for i in idx]
        for c in out:
            c["role"] = role
        return out

    sep7 = dt.date(2026, 9, 7)
    for ctype, n_re, n_utc, n_hol in (("Debit", 6, 4, 4), ("Credit", 3, 2, 2)):
        pool = [c for c in cf if c["card_type"] == ctype and c["role"] is None]
        # re-opened claims, one evening report per card type to carry the longest wait
        ev_pool = [c for c in pool if c["evening"] and is_bd(local_date(c["report_t"])) and
                   c["day0"] <= dt.date(2026, 8, 31)]
        lead = pick(ev_pool, 1, "reopen_lead")
        pool = [c for c in pool if c["role"] is None]
        early = [c for c in pool if c["day0"] <= dt.date(2026, 9, 3)]
        pick(early, n_re - 1, "reopen")
        pool = [c for c in pool if c["role"] is None]
        utc_pool = [c for c in pool if c["evening"] and is_bd(local_date(c["report_t"])) and
                    add_bd(c["day0"], 11) <= LAST_BD]
        for c in pick(utc_pool, n_utc, "utc"):
            c["k"] = 11
        pool = [c for c in pool if c["role"] is None]
        hol_pool = [c for c in pool if c["day0"] < sep7 <= add_bd(c["day0"], 10) and not c["evening"]]
        for c in pick(hol_pool, n_hol, "holiday"):
            c["k"] = 10
        # nobody else lands on the edge the stops are built around
        for c in cf:
            if c["card_type"] == ctype and c["role"] is None:
                if c["evening"] and c["k"] == 11:
                    c["k"] = 12
                if c["day0"] < sep7 <= add_bd(c["day0"], c["k"]) and c["k"] == 10:
                    c["k"] = 9
    rows, cases = [], []
    seq = 41_210
    for c in claims:
        c["refund"] = add_bd(c["day0"], c["k"])
        c["refunded"] = c["refund"] <= LAST_BD
        if c["role"] in ("reopen", "reopen_lead"):
            closed = add_bd(c["day0"], 13 if c["role"] == "reopen_lead" else int(rng.integers(10, 13)))
            back = closed + dt.timedelta(int(rng.integers(3, 6)) if c["role"] == "reopen_lead" else int(rng.integers(1, 4)))
            t_back = S.day_of(back) * DAY + int((9 + 8 * rng.random()) * 3600)
            day0b = next_bd(back)
            refund = add_bd(day0b, 5 if c["role"] == "reopen_lead" else int(rng.integers(2, 5)))
            assert refund <= LAST_BD, (c["slot"], refund)
            c["refund"], c["refunded"], c["reopen_t"] = refund, True, t_back
            cases.append({"claim": c, "opened_t": c["report_t"], "refunded_on": None, "status": "Closed"})
            cases.append({"claim": c, "opened_t": t_back, "refunded_on": refund, "status": "Refunded"})
        else:
            st = "Refunded" if c["refunded"] else "Open"
            ref = c["refund"] if c["refunded"] else None
            if c["kind"] != "Counterfeit" and rng.random() < 0.03:
                st, ref = "Closed", None
            cases.append({"claim": c, "opened_t": c["report_t"], "refunded_on": ref, "status": st})
    cases.sort(key=lambda x: (x["opened_t"], x["claim"]["slot"]))
    for cs in cases:
        seq += int(rng.integers(1, 9))
        cs["case_number"] = "FC26-%05d" % seq
    m_by = cat.merchants
    for cs in cases:
        c = cs["claim"]
        for i in c["rows"]:
            e = ev.loc[i]
            m = m_by[int(e.merch)]
            rows.append({"case_number": cs["case_number"], "card_token": toks.token.iat[c["tok"]],
                         "member_id": toks.member_id.iat[c["tok"]], "fraud_type": c["kind"],
                         "txn_date": local_date(e.t), "merchant_as_on_statement": descriptor(m),
                         "amount": round(float(e.amount), 2), "retrieval_ref": e.rrn,
                         "case_opened": cs["opened_t"], "refunded_on": cs["refunded_on"], "status": cs["status"],
                         "_ev": i})
    wb = pd.DataFrame(rows)
    wb["case_opened"] = [(dt.datetime.combine(W.SIM_START, dt.time()) +
                          dt.timedelta(seconds=int(t) + W.UTC_OFFSET_H * 3600)).strftime("%Y-%m-%dT%H:%M:%SZ")
                         for t in wb.case_opened]
    wb = wb.sort_values(["case_opened", "case_number", "txn_date", "retrieval_ref"]).reset_index(drop=True)
    fr.claims, fr.case_rows = claims, wb
    cb = chargebacks(fr, rng, wb)
    return wb, cb


def chargebacks(fr, rng, wb):
    cat, ev = fr.cat, fr.ev
    fx = M.fx_path()
    rows = []
    seq = 7_310
    uniq = wb.drop_duplicates("retrieval_ref").rename(columns={"_ev": "ev_row"})
    opened = {}
    for r in wb.itertuples():
        opened.setdefault(r.retrieval_ref, r.case_opened)
    pre_arb = {"Debit": 4, "Credit": 2}
    cand_rev = []
    for r in uniq.sort_values(["case_opened", "retrieval_ref"]).itertuples(index=False):
        e = ev.loc[int(getattr(r, "ev_row"))]
        m = cat.merchants[int(e.merch)]
        us = m["country"] == "US"
        ctype = fr.tokens.card_type.iat[int(e.tok)]
        if r.fraud_type == "Counterfeit":
            p = 0.9 if us else (0.7 if m["cat"] != "atm" else 0.35)
            reason = "Counterfeit transaction"
        elif r.fraud_type == "Card not present":
            p, reason = 0.62, "Fraud, card not present"
        else:
            continue
        if rng.random() > p:
            continue
        op = dt.datetime.strptime(opened[r.retrieval_ref], "%Y-%m-%dT%H:%M:%SZ").date()
        filed = next_bd(op + dt.timedelta(int(rng.integers(2, 7))))
        seq += int(rng.integers(1, 4))
        ref = "CB%05d" % seq
        if filed <= LAST_BD:          # not yet raised when the extract was taken otherwise
            rows.append([ref, r.retrieval_ref, r.card_token, reason, filed, "Filed", None])
        credit_d = next_bd(filed + dt.timedelta(int(rng.integers(9, 22))))
        if credit_d > LAST_BD:
            continue
        rate = fx[S.day_of(credit_d)] if us else 1.0
        amt = round(float(e.amount) * rate, 2)
        rows.append([ref, r.retrieval_ref, r.card_token, reason, credit_d, "Credited", amt])
        if r.fraud_type == "Counterfeit" and credit_d <= dt.date(2026, 9, 18):
            cand_rev.append((ctype, len(rows) - 1, credit_d))
    # credits taken back at pre-arbitration
    for ctype, k in pre_arb.items():
        pool = sorted([(d, i) for t, i, d in cand_rev if t == ctype])[:3 * k]
        assert len(pool) >= k, (ctype, len(pool))
        for j in sorted(rng.choice(len(pool), size=k, replace=False).tolist()):
            i = pool[j][1]
            ref, rrn, tok, reason, d, _, amt = rows[i]
            back = next_bd(d + dt.timedelta(int(rng.integers(9, 13))))
            assert back <= LAST_BD
            rows.append([ref, rrn, tok, reason, back, "Pre-arbitration debit", -amt])
    # merchant disputes on ordinary purchases share the log
    normal = ev[(ev.tag == F.T_NORMAL) & (ev.resp == 0) & ev.kind.isin([S.K_PUR, S.K_CNP]) &
                (ev.amount > 40) & (ev.t >= S.day_of(dt.date(2026, 7, 20)) * DAY)]
    pick = normal.iloc[sorted(rng.choice(len(normal), size=38, replace=False).tolist())]
    for e in pick.itertuples():
        d = next_bd(S.date_of(int(e.t) // DAY) + dt.timedelta(int(rng.integers(12, 30))))
        if d > LAST_BD:
            continue
        seq += int(rng.integers(1, 4))
        ref = "CB%05d" % seq
        reason = "Goods or services not provided" if e.kind == S.K_CNP else "Duplicate processing"
        tok = fr.tokens.token.iat[int(e.tok)]
        rows.append([ref, e.rrn, tok, reason, d, "Filed", None])
        d2 = next_bd(d + dt.timedelta(int(rng.integers(8, 20))))
        if d2 <= LAST_BD and rng.random() < 0.7:
            rate = fx[S.day_of(d2)] if cat.merchants[int(e.merch)]["country"] == "US" else 1.0
            rows.append([ref, e.rrn, tok, reason, d2, "Credited", round(float(e.amount) * rate, 2)])
    cb = pd.DataFrame(rows, columns=["chargeback_ref", "retrieval_ref", "card_token", "reason", "event_date",
                                     "event", "amount_cad"])
    cb = cb.sort_values(["event_date", "chargeback_ref", "event"], kind="mergesort").reset_index(drop=True)
    return cb
