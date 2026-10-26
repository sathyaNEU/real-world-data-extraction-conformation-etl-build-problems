"""Independent verifier: unzip target.zip into a scratch folder and recompute every graded figure from the bundle with
code that shares nothing with solve.py, then compare with figures.json and the write-up.

    python3 task304/generator/verify.py [target.zip]
"""
import json
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
BOOKS = ["First-time buyer 2019-21", "High LTV 2022-24", "Shared ownership", "Buy to let"]
SH = {"First-time buyer 2019-21": "FTB", "High LTV 2022-24": "HLTV", "Shared ownership": "SO", "Buy to let": "BTL"}


def month(s):
    return int(s[:4]) * 12 + int(s[5:7]) - 1


def chain(T, use_term=True):
    h = pd.read_parquet(os.path.join(T, "mortgage_payment_history_2019-01_to_2026-09.parquet")).drop_duplicates()
    h["m"] = h.period.map(month)
    h = h.sort_values(["account_number", "m"]).reset_index(drop=True)
    acct = h.account_number.to_numpy()
    new = np.r_[True, acct[1:] != acct[:-1]]
    pay = h.contractual_payment.to_numpy()
    arr = h.arrears_balance.to_numpy()
    state = np.where(pay > 0, np.floor(arr / np.where(pay > 0, pay, 1) + 1e-9), 0).clip(0, 2).astype(int)
    rem = h.remaining_term_months.to_numpy()
    code = h.product_code.str.replace("-", "", regex=False).to_numpy()
    m = h.m.to_numpy()
    n = len(h)
    # the last switch's payment rise and the month of the last term increase, carried forward per account
    chg = np.r_[False, code[1:] != code[:-1]] & ~new
    r = np.full(n, np.nan)
    r[chg] = pay[chg] / np.maximum(np.r_[1.0, pay[:-1]][chg], 1) - 1
    r[new] = 0.0
    rise = pd.Series(r).ffill().to_numpy()
    up = np.r_[False, rem[1:] > rem[:-1]] & ~new
    last = np.full(n, np.nan)
    last[up] = m[up]
    last[new & ~up] = -10 ** 6
    inc = pd.Series(last).ffill().to_numpy()
    live = (h.account_status == "Live").to_numpy()
    nxt = np.r_[~new[1:], False]
    nstate = np.r_[state[1:], 0]
    rb = np.digitize(rise, [0.05, 0.2, 0.4])
    book = h.book.to_numpy()

    def band(mm, last):
        since = mm - last
        return np.where(last < -10 ** 5, -1, np.digitize(since, [8, 16])) if use_term else np.zeros(len(mm), int)
    fit = (m >= 2024 * 12) & (m < 2026 * 12 + 8) & live & nxt & np.r_[live[1:], False]
    key = pd.DataFrame({"b": book[fit], "r": rb[fit], "e": band(m[fit], inc[fit]), "s": state[fit], "t": nstate[fit]})
    moves = {}
    for s0, s1 in ((0, 1), (0, 2), (1, 2), (1, 0), (2, 0), (2, 1)):
        x = key[key.s == s0]
        y = (x.t >= 2) if s1 == 2 else (x.t == s1)
        cell = y.groupby([x.b, x.r, x.e]).agg(["sum", "count"])
        moves[(s0, s1)] = (cell, y.groupby(x.b).mean())
    snap = (m == 2026 * 12 + 8) & live
    bk = pd.read_parquet(os.path.join(T, "mortgage_book_2026-09-30.parquet"))
    keep = set(bk.account_number[bk.recovery_stage == "None"])
    sel = snap & np.isin(acct, list(keep))
    b0, r0, l0, s0 = book[sel], rb[sel], inc[sel], state[sel]
    p = np.zeros((sel.sum(), 3))
    p[np.arange(sel.sum()), s0] = 1
    got = np.zeros(sel.sum())

    def rate(s0_, s1_, mm):
        cell, base = moves[(s0_, s1_)]
        idx = pd.MultiIndex.from_arrays([b0, r0, band(np.full(len(b0), mm), l0)])
        s_ = cell["sum"].reindex(idx).fillna(0).to_numpy()
        c_ = cell["count"].reindex(idx).fillna(0).to_numpy()
        return (s_ + 20 * base.reindex(b0).to_numpy()) / (c_ + 20)
    for mm in range(2026 * 12 + 9, 2027 * 12 + 12):
        q = {k: rate(k[0], k[1], mm) for k in moves}
        enter = p[:, 0] * q[(0, 2)] + p[:, 1] * q[(1, 2)]
        z0 = p[:, 0] * (1 - q[(0, 1)] - q[(0, 2)]) + p[:, 1] * q[(1, 0)] + p[:, 2] * q[(2, 0)]
        z1 = p[:, 0] * q[(0, 1)] + p[:, 1] * (1 - q[(1, 2)] - q[(1, 0)]) + p[:, 2] * q[(2, 1)]
        z2 = p[:, 2] * (1 - q[(2, 0)] - q[(2, 1)]) + enter
        if mm >= 2027 * 12:
            got += enter
            z2 = z2 - enter
        p = np.stack([z0, z1, z2], axis=1)
    return pd.Series(got).groupby(b0).sum()


def rates(T):
    from pypdf import PdfReader
    txt = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(
        os.path.join(T, "financial_support_team_2027_plan_paper.pdf")).pages))
    return {b: float(re.search(re.escape(b) + r" (\d+\.\d) per cent", txt).group(1)) / 100 for b in BOOKS}


def effect(T):
    """the share of the chance of possession the team removes, as the plan paper files it"""
    from pypdf import PdfReader
    txt = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(
        os.path.join(T, "financial_support_team_2027_plan_paper.pdf")).pages))
    return int(re.search(r"cuts that chance by (\d+) per cent", txt).group(1)) / 100


def ext(T):
    """the term increases the paper and the write-up state, from the history and the book alone"""
    h = pd.read_parquet(os.path.join(T, "mortgage_payment_history_2019-01_to_2026-09.parquet"),
                        columns=["account_number", "book", "period", "product_code", "remaining_term_months",
                                 "contractual_payment", "arrears_balance"]).drop_duplicates()
    h["m"] = h.period.map(month)
    h = h.sort_values(["account_number", "m"]).reset_index(drop=True)
    bk = pd.read_parquet(os.path.join(T, "mortgage_book_2026-09-30.parquet"), columns=["account_number", "book"])
    g = h.groupby("account_number")
    prev_rem, prev_pay = g.remaining_term_months.shift(), g.contractual_payment.shift()
    code = h.product_code.str.replace("-", "", regex=False)
    prev_code = code.groupby(h.account_number).shift()
    rose = prev_rem.notna() & (h.remaining_term_months > prev_rem)
    switch = prev_code.notna() & (code != prev_code)
    ftb = "First-time buyer 2019-21"
    f26 = (h.book == ftb) & (h.m >= 2026 * 12) & h.account_number.isin(set(bk.account_number))
    rise = h.contractual_payment / prev_pay.clip(lower=1) - 1
    pia = np.floor(h.arrears_balance / h.contractual_payment.where(h.contractual_payment > 0) + 1e-9).fillna(0)
    r24 = h[rose & (h.m >= 2024 * 12) & (h.m < 2025 * 12)][["account_number", "m"]]
    j = r24.merge(h[pia >= 2][["account_number", "m"]], on="account_number", suffixes=("", "_b"))
    j = j[j.m_b > j.m]
    return {"ftb_raised_2026": int(h[rose & f26].account_number.nunique()),
            "ftb_on_book": int((bk.book == ftb).sum()),
            "years_added_median": int(round(np.median((h.remaining_term_months - prev_rem + 1)[rose & f26]) / 12)),
            "pay_rise_extended": int(round(rise[switch & f26 & rose].median() * 100)),
            "pay_rise_kept": int(round(rise[switch & f26 & ~rose].median() * 100)),
            "raised_2024": int(r24.account_number.nunique()),
            "behind_8m": int(j[j.m_b <= j.m + 8].account_number.nunique()),
            "behind_by_asof": int(j[j.m_b <= 2026 * 12 + 8].account_number.nunique())}


def pilot(T):
    """the pilot report's table from the history, the litigation actions and the receiver appointments"""
    h = pd.read_parquet(os.path.join(T, "mortgage_payment_history_2019-01_to_2026-09.parquet"),
                        columns=["account_number", "period", "contractual_payment", "arrears_balance",
                                 "account_status"]).drop_duplicates()
    h["m"] = h.period.map(month)
    h = h.sort_values(["account_number", "m"]).reset_index(drop=True)
    pay = h.contractual_payment.to_numpy()
    h["p"] = np.where(pay > 0, np.floor(h.arrears_balance.to_numpy() / np.where(pay > 0, pay, 1) + 1e-9), 0)
    h["prev"] = h.groupby("account_number").p.shift().fillna(0)
    e = h[(h.p >= 2) & (h.prev < 2) & (h.account_status == "Live") & (h.m >= 2024 * 12) & (h.m <= 2024 * 12 + 11)]
    e = e.groupby("account_number").m.min()
    lit = pd.read_csv(os.path.join(T, "litigation_actions_2023-01_to_2026-09.csv"), dtype=str)
    lit = lit[lit.action == "Claim issued"]
    lit["c"] = lit.action_date.str[:7].map(month)
    rv = pd.read_csv(os.path.join(T, "lpa_receiver_appointments_2019-2026.csv"), dtype=str)
    rv["r"] = rv.date_appointed.map(lambda s: int(s[6:10]) * 12 + int(s[3:5]) - 1)
    first = pd.concat([lit.groupby("account_number").c.min(), rv.groupby("account_number").r.min()]).groupby(level=0).min()
    e = e[~(e.index.map(first).to_numpy() <= e.to_numpy())]
    four = h[h.p >= 4].groupby("account_number").m.apply(list)
    issued = lit.groupby("account_number").c.apply(list)
    res = {}
    for name, par in (("team", 0), ("usual", 1)):
        g = e[e.index.str[-1].astype(int) % 2 == par]
        res[name] = [len(g), sum(any(m0 < x <= m0 + 12 for x in four.get(a, [])) for a, m0 in g.items()),
                     sum(any(m0 <= x <= m0 + 12 for x in issued.get(a, [])) for a, m0 in g.items())]
    return res


def ask_a(T, books):
    """orders made or varied at hearings dated October 2025 to September 2026 (a repeat of the claim's last order on
    the same terms with no hearing between is the order sent again), how many suspended, and the claims open"""
    lit = pd.read_csv(os.path.join(T, "litigation_actions_2023-01_to_2026-09.csv"), dtype=str)
    lit = lit[lit.defendant == "1"].sort_values(["claim_number", "action_date"], kind="stable")
    reg = pd.read_csv(os.path.join(T, "possession_register_2019-01_to_2026-09.csv"), dtype=str)
    reg["d"] = pd.to_datetime(reg.possession_date, format="%d/%m/%Y")
    taken = reg.groupby("account_number").d.max()
    res = {b: [0, 0, 0] for b in BOOKS[:3]}
    for cn, g in lit.groupby("claim_number"):
        a = g.account_number.iloc[0]
        b = books.get(a)
        if b not in res:
            continue
        prev, heard = None, False
        for d, act, det in zip(g.action_date, g.action, g.detail.fillna("")):
            if act.startswith("Hearing"):
                heard = True
            elif act.startswith("Possession order"):
                if not (prev == det and not heard) and "2025-10-01" <= d <= "2026-09-30":
                    res[b][0] += 1
                    res[b][1] += int(det == "Suspended on terms")
                prev, heard = det, False
        if set(g.action) & {"Claim withdrawn", "Order discharged", "Eviction carried out"}:
            continue
        if a in taken.index and taken[a] >= pd.Timestamp(g.action_date.min()):
            continue
        res[b][2] += 1
    return res


def ask_b(T, books):
    """one possession sold per account and completion date; the debt every register row's for the account"""
    s = pd.read_csv(os.path.join(T, "possession_sales_completed_2019-2026.csv"), dtype=str)
    s["statement"] = s.statement.astype(int)
    s = s.sort_values("statement").groupby("sale_ref").tail(1)
    rv = pd.read_csv(os.path.join(T, "lpa_receiver_appointments_2019-2026.csv"), dtype=str)
    s["a"] = s.account_number.where(s.account_number.notna(), s.receiver_ref.map(dict(zip(rv.receiver_ref, rv.account_number))))
    s = s[(s.completion_date >= "2025-10-01") & (s.completion_date <= "2026-09-30")]
    s = s.drop_duplicates(["a", "completion_date"])
    reg = pd.read_csv(os.path.join(T, "possession_register_2019-01_to_2026-09.csv"), dtype=str)
    debt = reg.assign(x=reg.debt_at_possession.astype(float)).groupby("account_number").x.sum()
    loss = (s.a.map(debt) - s.sale_price.astype(float) + s.selling_costs.astype(float)).clip(lower=0)
    bk = s.a.map(books)
    out = {}
    for b in BOOKS[:3]:
        x = loss[bk == b]
        out[b] = [int(len(x)), int((x > 0).sum()), int(round(x.mean() / 100.0) * 100)]
    return out


def main(zp=None):
    zp = zp or os.path.join(TASK, "target.zip")
    T = tempfile.mkdtemp()
    with zipfile.ZipFile(zp) as z:
        z.extractall(T)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    bad = []
    rt = rates(T)
    ent = chain(T)
    cut = effect(T)
    av = {b: cut * ent.get(b, 0) * rt[b] for b in BOOKS}
    best = max(av, key=av.get)
    if best != fig["call"]["book"]:
        bad.append(("call", best))
    for b in BOOKS:
        if round(av[b], 1) != fig["call"]["avoided"][SH[b]]:
            bad.append(("avoided", b, round(av[b], 1), fig["call"]["avoided"][SH[b]]))
    easy = chain(T, use_term=False)
    ea = {b: cut * easy.get(b, 0) * rt[b] for b in BOOKS}
    if max(ea, key=ea.get) != "High LTV 2022-24":
        bad.append(("easy route", max(ea, key=ea.get)))
    h = pd.read_parquet(os.path.join(T, "mortgage_payment_history_2019-01_to_2026-09.parquet"), columns=["account_number", "book"])
    books = dict(zip(h.account_number, h.book))
    a = ask_a(T, books)
    for b in BOOKS[:3]:
        want = [fig["askA"][SH[b]][k] for k in ("orders", "suspended", "open")]
        if a[b] != want:
            bad.append(("askA", b, a[b], want))
    bb = ask_b(T, books)
    for b in BOOKS[:3]:
        want = [fig["askB"][SH[b]][k] for k in ("sold", "at_loss", "avg_loss")]
        if bb[b] != want:
            bad.append(("askB", b, bb[b], want))
    from pypdf import PdfReader
    ptxt = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(
        os.path.join(T, "financial_support_team_pilot_2024_report.pdf")).pages))
    mm = re.search(r"Support team \(even\) (\d+) (\d+) \([\d.]+%\) (\d+) \([\d.]+%\) Usual collections \(odd\) (\d+) (\d+) "
                   r"\([\d.]+%\) (\d+)", ptxt)
    pv = pilot(T)
    if mm is None or [int(x) for x in mm.groups()] != pv["team"] + pv["usual"]:
        bad.append(("pilot table", pv, mm.groups() if mm else None))
    ex = ext(T)
    for k, v in ex.items():
        if fig["ext"][k] != v:
            bad.append(("ext", k, v, fig["ext"][k]))
    # the write-up states each graded figure as figures.json holds it
    for b in BOOKS[:3]:
        line = "%s: %d, %d, %d" % (b, *a[b])
        if line not in sub:
            bad.append(("submission askA", line))
        line = "%s: %d, %d, £%s" % (b, bb[b][0], bb[b][1], "{:,}".format(bb[b][2]))
        if line not in sub:
            bad.append(("submission askB", line))
    for b, word in (("First-time buyer 2019-21", "about %d" % (int(round(av["First-time buyer 2019-21"] / 10.0)) * 10)),
                    ("High LTV 2022-24", "about %d" % (int(round(av["High LTV 2022-24"] / 10.0)) * 10))):
        if word not in sub:
            bad.append(("submission call", word))
    # the data dictionary lists every field of every data file, in the file's own order
    dic = pd.read_csv(os.path.join(T, "data_dictionary.csv"))
    for f in sorted(os.listdir(T)):
        if f.endswith(".parquet"):
            cols = pq.read_schema(os.path.join(T, f)).names
        elif f.endswith(".csv") and f != "data_dictionary.csv":
            cols = pd.read_csv(os.path.join(T, f), nrows=1).columns.tolist()
        else:
            continue
        if dic[dic.file == f].field.tolist() != cols:
            bad.append(("dictionary", f))
    print("verify: %d mismatches" % len(bad))
    for x in bad:
        print("  ", x)
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
