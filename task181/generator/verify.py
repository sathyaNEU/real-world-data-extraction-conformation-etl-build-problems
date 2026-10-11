"""Independent verifier for task181: reads only ../target/ and shares no code with the generator or golden.py.

It works on pyarrow arrays and numpy with plain dictionaries (no pandas): the counterfeit cards and their
first use from the case workbook, the common-point screen, attribution then re-screening, the two windows and
the reissue count, the losses and the refund record. Every figure is compared with EXPECT.
"""
import csv
import datetime as dt
import os
import sys

import numpy as np
import openpyxl
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target")
EXPECT = {
    "victims": 283, "first_use": "2026-08-24",
    "terminals": ["LT723511", "02417158"],
    "windows": {"LT723511": ["2026-08-05", "2026-08-31"], "02417158": ["2026-08-13", "2026-09-14"]},
    "reissue": 387,
    "ask_a": {"Debit": (246792.17, 78330.45, 168461.72), "Credit": (35217.25, 11845.28, 23371.97)},
    "ask_b": {"Debit": (195, 20), "Credit": (21, 16)},
}
EDT = 4 * 3600   # every timestamp in the extract falls between the 2026 daylight-time changes


def f(prefix):
    return os.path.join(T, next(x for x in sorted(os.listdir(T)) if x.startswith(prefix)))


def sheet(path, name, first):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[name]
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] == first)
    hdr = rows[hi]
    return [dict(zip(hdr, r)) for r in rows[hi + 1:] if r and r[0] is not None]


def as_date(x):
    return x.date() if isinstance(x, dt.datetime) else x


def main():
    ok = True
    # case workbook ------------------------------------------------------------------------------
    cases = sheet(f("fraud_cases"), "Disputed transactions", "case_number")
    cf = [r for r in cases if r["fraud_type"] == "Counterfeit"]
    first = {}
    for r in cf:
        d = as_date(r["txn_date"])
        first[r["card_token"]] = min(first.get(r["card_token"], d), d)
    cards = sheet(f("card_history"), "Cards", "card_token")
    ctype = {r["card_token"]: r["card_type"] for r in cards}
    open_ = {r["card_token"] for r in cards if r["status"] == "Open"}
    print("victims", len(first), min(first.values()))
    ok &= len(first) == EXPECT["victims"] and str(min(first.values())) == EXPECT["first_use"]

    # authorisation log as arrays ------------------------------------------------------------------
    tbl = pq.read_table(f("card_authorisations"), columns=["card_token", "terminal_id", "pos_entry_mode",
                                                           "txn_datetime_utc", "retrieval_ref", "message_type",
                                                           "response_code", "amount_billing_cad"])
    ts = tbl["txn_datetime_utc"].cast(pa.timestamp("s", tz="UTC")).cast("int64").to_numpy()
    assert ts.min() >= int(dt.datetime(2026, 3, 8, 7, tzinfo=dt.timezone.utc).timestamp()) and \
        ts.max() < int(dt.datetime(2026, 11, 1, 6, tzinfo=dt.timezone.utc).timestamp())
    lday = (ts - EDT) // 86400                                     # Eastern day number (epoch days)
    tok_d = pc.dictionary_encode(tbl["card_token"]).combine_chunks()
    tok_code = tok_d.indices.to_numpy()
    tok_names = tok_d.dictionary.to_pylist()
    term_d = pc.dictionary_encode(tbl["terminal_id"]).combine_chunks()
    term_code = term_d.indices.to_numpy(zero_copy_only=False)
    term_code = np.where(np.isnan(term_code.astype(float)), -1, term_code).astype(np.int64)
    term_names = term_d.dictionary.to_pylist()
    mode = tbl["pos_entry_mode"].to_numpy(zero_copy_only=False)
    contact = np.isin(mode, ["05", "80", "90"])
    epoch = dt.date(1970, 1, 1)
    vcode = {tok_names.index(t): (first[t] - epoch).days for t in first}
    is_v = np.zeros(len(tok_names), bool)
    fday = np.full(len(tok_names), -1, np.int64)
    for k, d in vcode.items():
        is_v[k] = True
        fday[k] = d

    def screen(vset, L=60):
        fd = fday[list(vset)]
        span0, span1 = fd.min() - L, fd.max() - 1
        sel_v = np.isin(tok_code, list(vset)) & contact & (term_code >= 0)
        fv = fday[tok_code[sel_v]]
        dv = lday[sel_v]
        keep = (dv >= fv - L) & (dv <= fv - 1)
        pairs = set(zip(term_code[sel_v][keep].tolist(), tok_code[sel_v][keep].tolist()))
        v = {}
        for t, _ in pairs:
            v[t] = v.get(t, 0) + 1
        ins = (lday >= span0) & (lday <= span1)
        nonv = ~is_v[tok_code]
        n_act = len(np.unique(tok_code[ins & nonv]))
        selb = ins & nonv & contact & (term_code >= 0)
        bp = np.unique(term_code[selb] * 100_000 + tok_code[selb])
        bt = bp // 100_000
        tt, cnt = np.unique(bt, return_counts=True)
        b = dict(zip(tt.tolist(), cnt.tolist()))
        out = {}
        for t, x in v.items():
            bb = b.get(t, 0)
            out[t] = (x, bb, (x / len(vset)) / (bb / n_act) if bb else float("inf"))
        return out, pairs

    vall = set(vcode)
    chosen, rem = [], set(vall)
    while len(rem) >= 10:
        sc, pairs = screen(rem)
        cand = sorted(((s[2], s[0], t) for t, s in sc.items() if s[0] >= 10), reverse=True)
        if not cand or not cand[0][0] > 3.0:
            break
        top = cand[0][2]
        chosen.append(top)
        rem -= {k for t, k in pairs if t == top}
    names = [term_names[t] for t in chosen]
    print("terminals", names, "unexplained", len(rem))
    ok &= names == EXPECT["terminals"]

    # windows and the reissue count -----------------------------------------------------------------
    reissue = set()
    for t in chosen:
        at = (term_code == t) & contact
        vrows = at & is_v[tok_code]
        vrows &= lday < fday[tok_code]
        t0, t1 = ts[vrows].min(), ts[vrows].max()
        d0 = (epoch + dt.timedelta(int((t0 - EDT) // 86400))).isoformat()
        d1 = (epoch + dt.timedelta(int((t1 - EDT) // 86400))).isoformat()
        print("window", term_names[t], d0, d1)
        ok &= [d0, d1] == EXPECT["windows"][term_names[t]]
        inside = at & (ts >= t0) & (ts <= t1)
        reissue |= {tok_names[k] for k in np.unique(tok_code[inside]).tolist()}
    n = len(reissue & open_)
    print("reissue", n)
    ok &= n == EXPECT["reissue"]

    # ask A ----------------------------------------------------------------------------------------
    rrns = sorted({r["retrieval_ref"] for r in cf})
    tok_of = {r["retrieval_ref"]: r["card_token"] for r in cf}
    rr = tbl["retrieval_ref"].to_numpy(zero_copy_only=False)
    mt = tbl["message_type"].to_numpy(zero_copy_only=False)
    rc = tbl["response_code"].to_numpy(zero_copy_only=False)
    amt = tbl["amount_billing_cad"].to_numpy()
    idx = np.nonzero(np.isin(rr, rrns))[0]
    posted = {}
    comp = {}
    for i in idx:
        k = rr[i]
        if mt[i] in ("0100", "0200") and rc[i] == "00":
            posted[k] = posted.get(k, 0.0) + amt[i]
        elif mt[i] == "0220":
            comp[k] = comp.get(k, 0.0) + amt[i]
        elif mt[i] == "0420":
            posted[k] = posted.get(k, 0.0) - amt[i]
    for k, v in comp.items():
        posted[k] = v
    gross = {"Debit": 0.0, "Credit": 0.0}
    for k in rrns:
        gross[ctype[tok_of[k]]] += posted[k]
    rec = {"Debit": 0.0, "Credit": 0.0}
    rset = set(rrns)
    with open(f("chargebacks")) as fh:
        for r in csv.DictReader(fh):
            if r["retrieval_ref"] in rset and r["amount_cad"]:
                rec[ctype[r["card_token"]]] += float(r["amount_cad"])
    for k in ("Debit", "Credit"):
        got = (round(gross[k], 2), round(rec[k], 2), round(gross[k] - rec[k], 2))
        print("ask A", k, got)
        ok &= all(abs(x - y) < 0.005 for x, y in zip(got, EXPECT["ask_a"][k]))

    # ask B ----------------------------------------------------------------------------------------
    from docx import Document
    hol = set()
    for row in Document(f("MS-3")).tables[0].rows[1:]:
        hol.add(dt.datetime.strptime(row.cells[0].text.strip(), "%a %d %b %Y").date())
    by_case = {}
    for r in cf:
        by_case.setdefault(r["case_number"], []).append(r)
    parent = {c: c for c in by_case}

    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    seen = {}
    for c in sorted(by_case):
        for r in by_case[c]:
            k = r["retrieval_ref"]
            if k in seen and root(seen[k]) != root(c):
                parent[root(c)] = root(seen[k])
            seen.setdefault(k, c)
    claims = {}
    for c, rows in by_case.items():
        claims.setdefault(root(c), []).extend(rows)
    res = {"Debit": [0, 0], "Credit": [0, 0]}
    for cl, rows in claims.items():
        refunds = [as_date(r["refunded_on"]) for r in rows if r["refunded_on"]]
        if not refunds:
            continue
        t0 = min(dt.datetime.strptime(r["case_opened"], "%Y-%m-%dT%H:%M:%SZ") for r in rows)
        d = (t0 - dt.timedelta(hours=4)).date()
        while d.weekday() >= 5 or d in hol:
            d += dt.timedelta(1)
        refund = max(refunds)
        w, x = 0, d
        while x < refund:
            x += dt.timedelta(1)
            if x.weekday() < 5 and x not in hol:
                w += 1
        k = ctype[rows[0]["card_token"]]
        res[k][0] += int(w <= 10)
        res[k][1] = max(res[k][1], w)
    for k in ("Debit", "Credit"):
        print("ask B", k, tuple(res[k]))
        ok &= tuple(res[k]) == EXPECT["ask_b"][k]
    print("VERIFY", "OK" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
