"""Turn card events into the issuer's authorisation messages.

One row per message: purchases are financial requests (0200) on debit and authorisation requests (0100)
on credit; pay-at-pump is a pre-authorisation (0100) followed by a completion advice (0220) on the same
retrieval reference; ATM withdrawals are 0200, balance enquiries 0100; reversal advices (0420) carry
the retrieval reference of the message they reverse. Declines stay in the log with their response code.
"""
import datetime as dt

import numpy as np
import pandas as pd

import world as W
import sim as S
import fraud as F

RESP = ["00", "51", "55", "05", "61", "54", "62", "91"]
R00, R51, R55, R05, R61, R54, R62, R91 = range(8)
DAY = S.DAY


def fx_path():
    """USD to CAD by local day, a gentle walk from W.USD_CAD_START (the rate the network applies)."""
    rng = np.random.default_rng(W.SEED + 71)
    r = [W.USD_CAD_START]
    for _ in range(S.ND - 1):
        r.append(r[-1] * (1 + rng.normal(0, 0.0021)))
    return np.round(np.array(r), 4)


def assign_declines(fr, rng):
    """Response codes for ordinary card events; the counterfeit and fraud rows carry their own."""
    ev = fr.ev
    cat = fr.cat
    n = len(ev)
    resp = ev.resp.values.copy()
    normal = ev.tag.values == F.T_NORMAL
    credit = fr.tokens.card_type.values[ev.tok.values] == "Credit"
    kind = ev.kind.values
    u = rng.random(n)
    atm = kind == S.K_ATM
    pur = np.isin(kind, (S.K_PUR, S.K_PUMP, S.K_CNP))
    r = np.zeros(n, np.int8)
    # debit
    d = ~credit
    r[d & pur & (u < 0.016)] = R51
    r[d & pur & (u >= 0.016) & (u < 0.021)] = R55
    r[d & pur & (u >= 0.021) & (u < 0.023)] = R05
    r[d & atm & (u < 0.020)] = R51
    r[d & atm & (u >= 0.020) & (u < 0.028)] = R61
    r[d & atm & (u >= 0.028) & (u < 0.036)] = R55
    # credit
    r[credit & pur & (u < 0.008)] = R05
    r[credit & pur & (u >= 0.008) & (u < 0.014)] = R51
    r[(u > 0.9996)] = R91
    # the two skimmed terminals approve everything in August and September, and nothing ever declines
    # a balance enquiry or a refund
    term = ev.term.values
    day = ev.t.values // DAY
    calm = np.isin(term, [fr.terms["OPT6"], fr.terms["SCO2"]]) & (day >= S.day_of(dt.date(2026, 8, 1))) & \
        (day <= S.day_of(dt.date(2026, 9, 30)))
    r[calm | (kind == S.K_BAL) | (kind == S.K_REF)] = R00
    resp[normal] = r[normal]
    ev["resp"] = resp


def expand(fr):
    rng = np.random.default_rng(W.SEED + 73)
    assign_declines(fr, rng)
    cat = fr.cat
    ev = fr.ev.sort_values(["t", "slot"], kind="mergesort").reset_index(drop=True)
    fr.ev = ev
    toks = fr.tokens
    n = len(ev)
    credit = toks.card_type.values[ev.tok.values] == "Credit"
    acct = np.where(credit, "30", fr.slots.acct.values[ev.slot.values])
    kind = ev.kind.values
    resp = ev.resp.values
    fx = fx_path()
    day = ev.t.values // DAY
    m_cur = np.array([m["currency"] for m in cat.merchants])
    cur = m_cur[ev.merch.values]
    usd = cur == "840"
    amt = ev.amount.values.copy()
    # pre-authorisation holds at the pump
    hold = np.where(credit, 150.0, 100.0)
    pump = kind == S.K_PUMP
    first_amt = np.where(pump, hold, amt)
    bill_rate = np.where(usd, fx[np.clip(day, 0, S.ND - 1)] * (1 + W.FX_MARKUP), 1.0)
    # message rows -------------------------------------------------------------------------------------
    rows_ev = [np.arange(n)]
    rows_mt = [np.where(pump | credit & ~(kind == S.K_ATM) | (kind == S.K_BAL), "0100", "0200")]
    rows_t = [ev.t.values]
    rows_amt = [first_amt]
    rows_seq = [np.zeros(n, np.int8)]
    # completions: approved pre-authorisations at the pump, final amount 2 to 7 minutes on
    comp = np.nonzero(pump & (resp == R00))[0]
    rows_ev.append(comp)
    rows_mt.append(np.full(len(comp), "0220"))
    rows_t.append(ev.t.values[comp] + rng.integers(110, 430, len(comp)))
    rows_amt.append(amt[comp])
    rows_seq.append(np.ones(len(comp), np.int8))
    # reversals: some ATM withdrawals dispense short, some purchases time out
    normal = ev.tag.values == F.T_NORMAL
    ok = resp == R00
    rv_atm = np.nonzero(normal & ok & (kind == S.K_ATM) & (rng.random(n) < 0.0055))[0]
    rv_pos = np.nonzero(normal & ok & (kind == S.K_PUR) & ~credit & (rng.random(n) < 0.0012))[0]
    rv = np.concatenate([rv_atm, rv_pos])
    part = np.where(np.isin(rv, rv_atm), np.round(amt[rv] * rng.choice([0.25, 0.5, 1.0], len(rv)) / 20) * 20, amt[rv])
    part = np.where(part <= 0, amt[rv], part)
    rows_ev.append(rv)
    rows_mt.append(np.full(len(rv), "0420"))
    rows_t.append(ev.t.values[rv] + rng.integers(25, 300, len(rv)))
    rows_amt.append(part)
    rows_seq.append(np.full(len(rv), 2, np.int8))
    ei = np.concatenate(rows_ev)
    msg = pd.DataFrame({"ev": ei, "mt": np.concatenate(rows_mt), "t": np.concatenate(rows_t),
                        "amount_txn": np.round(np.concatenate(rows_amt), 2), "seq": np.concatenate(rows_seq)})
    msg = msg.sort_values(["t", "ev", "seq"], kind="mergesort").reset_index(drop=True)
    e = msg.ev.values
    # identifiers: retrieval reference = year digit, julian day, UTC hour, sequence; one per transaction
    t_utc = ev.t.values + W.UTC_OFFSET_H * 3600
    base = dt.datetime.combine(W.SIM_START, dt.time())
    jday = np.array([(W.SIM_START + dt.timedelta(int(x))).timetuple().tm_yday for x in range(S.ND + 1)])
    ud = t_utc // DAY
    uh = (t_utc % DAY) // 3600
    order = np.argsort(t_utc, kind="mergesort")
    bucket = ud[order] * 100 + uh[order]
    seq = np.zeros(n, np.int64)
    bstart = np.r_[0, np.nonzero(np.diff(bucket))[0] + 1]
    ranks = np.arange(n) - np.repeat(bstart, np.diff(np.r_[bstart, n]))
    offs = rng.integers(100_000, 400_000)
    seq[order] = ranks * 3 + offs % 7 + 104_000
    rrn = np.array(["6%03d%02d%06d" % (jday[a], b, c) for a, b, c in zip(ud, uh, seq)])
    ev["rrn"] = rrn
    msg["retrieval_ref"] = rrn[e]
    msg["stan"] = ["%06d" % ((i * 7 + 18_233) % 999_983) for i in range(len(msg))]
    msg["message_id"] = ["%014d" % (31_870_000_000_000 + i * 11 + int(x) % 7) for i, x in enumerate(e)]
    msg["card_token"] = toks.token.values[ev.tok.values[e]]
    pc_type = np.where(kind == S.K_ATM, "01", np.where(kind == S.K_BAL, "30", np.where(kind == S.K_REF, "20", "00")))
    pc = np.where(kind == S.K_REF, pc_type + "00" + acct, pc_type + acct + "00")
    msg["processing_code"] = pc[e]
    msg["message_type"] = msg.mt
    msg["txn_datetime_utc"] = pd.to_datetime(base) + pd.to_timedelta(msg.t.values + W.UTC_OFFSET_H * 3600, unit="s")
    msg["txn_datetime_utc"] = msg["txn_datetime_utc"].dt.tz_localize("UTC")
    msg["currency_txn"] = cur[e]
    msg["amount_billing_cad"] = np.round(msg.amount_txn.values * bill_rate[e], 2)
    m_id = np.array([m["merchant_id"] for m in cat.merchants])
    msg["merchant_id"] = m_id[ev.merch.values[e]]
    tid = np.full(len(msg), None, dtype=object)
    term = ev.term.values[e]
    dd = day[e]
    base_tid = np.array([t["tid_history"][0][1] for t in cat.terminals], dtype=object)
    cp = term >= 0
    tid[cp] = base_tid[term[cp]]
    for t in cat.terminals:
        h = t["tid_history"]
        if len(h) > 1:
            sel = term == t["idx"]
            for frm, x in h[1:]:
                tid[sel & (dd >= S.day_of(frm))] = x
    msg["terminal_id"] = tid
    m_mcc = np.array([m["mcc"] for m in cat.merchants])
    msg["mcc"] = m_mcc[ev.merch.values[e]]
    msg["pos_entry_mode"] = np.array(S.ENTRY)[ev.entry.values[e]]
    msg["response_code"] = np.array(RESP)[resp[e]]
    msg.loc[msg.mt.isin(["0220", "0420"]), "response_code"] = "00"
    cols = ["message_id", "card_token", "message_type", "processing_code", "txn_datetime_utc", "amount_txn",
            "currency_txn", "amount_billing_cad", "merchant_id", "terminal_id", "mcc", "pos_entry_mode",
            "response_code", "retrieval_ref", "stan"]
    out = msg[cols].copy()
    out.attrs["ev_index"] = e
    fr.msg_ev = e
    return out
