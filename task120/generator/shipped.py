"""Shipped frames for the ask files, built from the internal structures in asks.py. Internal
columns (true TINs, device flags) never leave this module."""
import numpy as np
import pandas as pd

from common import stream
from asks import to_utc


def ledger(A):
    pay = A["es_pay"]
    rows = []
    # cash payments as received; TIN as reported
    for i, r in enumerate(pay.itertuples(index=False)):
        rows.append(dict(key=("P", i), account_tin=int(r.reported_tin), tax_year=int(r.tax_year), txn_type="ES",
                         amount=int(r.amount), local=r.local, source_ref=None, channel=r.channel))
    # TY2024 fourth instalments received in January 2025
    for j, (tin, ty, amt, local, chn) in enumerate(A["es_old"]):
        rows.append(dict(key=("O", j), account_tin=tin, tax_year=ty, txn_type="ES", amount=amt, local=local,
                         source_ref=None, channel=chn))
    # transfers of payments keyed to the wrong year: out of 2024, into 2025, citing the payment
    for j, (i, post) in enumerate(A["es_xfer"]):
        p = pay.iloc[i]
        rows.append(dict(key=("XO", j), account_tin=int(p.tin), tax_year=2024, txn_type="TRF", amount=-int(p.amount),
                         local=post, source_ref=("P", i), channel=None))
        rows.append(dict(key=("XI", j), account_tin=int(p.tin), tax_year=2025, txn_type="TRF", amount=int(p.amount),
                         local=post + pd.Timedelta(seconds=1), source_ref=("P", i), channel=None))
    # overpayments credited from TY2024 returns, citing the return
    for j, (rid, amt, tin, post) in enumerate(A["es_credits"]):
        rows.append(dict(key=("C", j), account_tin=tin, tax_year=2025, txn_type="TRF", amount=int(amt), local=post,
                         source_ref=("R", rid), channel=None))
    df = pd.DataFrame(rows)
    df["utc"] = to_utc(df.local).to_numpy()
    rng = stream("txn_ids")
    df = df.sort_values(["utc", "account_tin", "amount"], kind="stable").reset_index(drop=True)
    df["txn_id"] = 25_000_000_000 + 1_204_117 + np.cumsum(rng.integers(1, 7, len(df)))
    idmap = dict(zip(df.key, df.txn_id))

    def ref(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return ""
        if x[0] == "R":
            return str(int(x[1]))
        return str(int(idmap[x]))
    df["source_ref"] = [ref(x) for x in df.source_ref]
    df["channel"] = df.channel.fillna("")
    out = pd.DataFrame({
        "txn_id": df.txn_id.astype(np.int64),
        "account_tin": df.account_tin.astype(np.int64),
        "tax_year": df.tax_year.astype(np.int16),
        "txn_type": df.txn_type,
        "amount": df.amount.astype(np.int64),
        "txn_utc": pd.to_datetime(df.utc).dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_ref": df.source_ref,
        "channel": df.channel,
    })
    pay_txn = {i: idmap[("P", i)] for i in range(len(pay))}
    return out, pay_txn


def returned_items(A, pay_txn):
    rng = stream("ret_ids")
    rows = []
    for (i, code, rdate, rep_date, rep_res) in A["es_returned"]:
        rows.append((pay_txn[i], code, rdate.date(), rep_date.date() if rep_date is not None else None, rep_res or ""))
    df = pd.DataFrame(rows, columns=["txn_id", "return_reason", "returned_date", "represented_date", "represented_result"])
    df = df.sort_values(["returned_date", "txn_id"], kind="stable").reset_index(drop=True)
    df.insert(0, "item_id", 88_100_000 + np.cumsum(rng.integers(1, 5, len(df))))
    return df


def register(A):
    reg = A["register"]
    rng = stream("reg_ids")
    df = reg.sort_values(["opened_date", "reported_tin"], kind="stable").reset_index(drop=True)
    out = pd.DataFrame({
        "case_id": 30_400_000 + np.cumsum(rng.integers(1, 9, len(df))),
        "reported_tin": df.reported_tin.astype(np.int64),
        "reported_on": np.where(df.source == "W2", "WAGE_STATEMENT", "PAYMENT"),
        "opened_date": df.opened_date.dt.date,
        "case_status": df.status,
        "resolved_tin": df.resolved_tin.astype(np.int64),
        "closed_date": df.closed_date.dt.date,
    })
    return out


def w2_efile(A):
    ef = A["w2_efile"]
    return pd.DataFrame({
        "statement_id": ef.statement_id.astype(np.int64),
        "submission_id": ef.submission_id.astype(np.int64),
        "employer_ein": ef.ein.astype(np.int64),
        "employee_tin": ef.reported_tin.astype(np.int64),
        "tax_year": np.full(len(ef), 2025, np.int16),
        "state_wages": ef.wages.astype(np.int64),
        "state_tax_withheld": ef.withheld.astype(np.int64),
        "received_date": ef.received_date,
    })


def w2_paper_lines(A):
    pp = A["w2_paper"]
    rng = stream("keyers")
    keyer = rng.choice(["K2", "K4", "K5", "K7", "K9", "KA"], len(pp))
    lines = []
    for b, s, ein, tin, w, wh, d, k in zip(pp.batch, pp.seq, pp.ein, pp.reported_tin, pp.wages, pp.withheld,
                                           pd.to_datetime(pp.keyed_date), keyer):
        lines.append(f"{int(b):06d}{int(s):04d}{int(ein):09d}{int(tin):09d}2025{int(w):011d}{int(wh):010d}{d:%Y%m%d}{k}")
    return lines


def recon_summary(A):
    ef = A["w2_efile"]
    pp = A["w2_paper"]
    rows = []
    for lab, d in (("Electronic (platform)", ef), ("Paper (capture vendor)", pp)):
        rows.append((lab, int(d.ein.nunique()), int(len(d)), int(d.wages.sum()), int(d.withheld.sum())))
    distinct = int(pd.concat([ef.ein, pp.ein]).nunique())
    return rows, distinct


def schd_extract(A):
    x = A["schd_extract"]
    return pd.DataFrame({"return_id": x.return_id.astype(np.int64), "tax_year": 2025,
                         "amendment_seq": x.amendment_seq.astype(np.int64),
                         "received_date": pd.to_datetime(x.received_date).dt.date,
                         "net_gain_loss": x.net_gain_loss.astype(np.int64),
                         "amount_in_agi": x.amount_in_agi.astype(np.int64)})


def amended_log(A):
    v = A["versions"].sort_values(["return_id", "amendment_seq"], kind="stable")
    out = pd.DataFrame({
        "return_id": v.return_id.astype(np.int64),
        "amendment_seq": v.amendment_seq.astype(np.int64),
        "received_date": pd.to_datetime(v.received_date).dt.date,
        "disposition": v.disposition,
        "disposition_date": pd.to_datetime(v.disposition_date).dt.date,
        "federal_agi": v.federal_agi.astype(np.int64),
        "net_gain_loss": v.net_gain_loss.where(v.has_schd).astype("Int64"),
        "amount_in_agi": v.amount_in_agi.where(v.has_schd).astype("Int64"),
    })
    return out.reset_index(drop=True)


def apply_credit_elections(R24, A):
    """The TY2024 return's overpayment credit election equals the transfer that cites it."""
    m = {rid: amt for rid, amt, _, _ in A["es_credits"]}
    v = R24.return_id.map(m)
    R24 = R24.copy()
    R24["overpayment_credit_elect"] = v.fillna(0).astype(np.int64).to_numpy()
    return R24
