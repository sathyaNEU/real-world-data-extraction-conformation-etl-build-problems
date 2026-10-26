"""The Society's records cut from the world: the book at 30 September 2026, the monthly payment history since January
2019, the possession register, the sales completed, the LPA receiver appointments and the panel solicitors' litigation
actions since January 2023."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import world as W

ym = W.ym


def mdate(m, d=None):
    m = np.asarray(m)
    y, mo = m // 12, m % 12 + 1
    if d is None:
        return pd.to_datetime(pd.DataFrame(dict(year=y, month=mo, day=1))) + pd.offsets.MonthEnd(0)
    return pd.to_datetime(pd.DataFrame(dict(year=y, month=mo, day=np.minimum(d, 28))))


def pcode(prod_seq, m_start, fix5, rate):
    kind = "F5" if fix5 else "F2"
    lead = "PT" if prod_seq > 0 else ""
    return f"{lead}{kind}-{(m_start // 12) % 100:02d}{m_start % 12 + 1:02d}-{int(round(rate * 100)):03d}"


def build(seed=P.SEED):
    w = W.World(seed).run()
    rng = np.random.default_rng(seed + 7)
    book = np.array(P.BOOKS)[w.book]
    n = w.n
    base = rng.choice(np.arange(2050000000, 2099999999), n, replace=False) * 2
    acct = np.array([f"{x + (0 if e else 1):010d}" for x, e in zip(base, w.even)])
    pcd = np.array([P.REGION_PC[r][rng.integers(0, 5)] for r in w.region])
    ptype = np.where(rng.random(n) < np.where(book == "SO", 0.55, 0.22), "Flat",
                     np.where(rng.random(n) < 0.5, "Terraced house", "Semi-detached house"))
    day = rng.integers(1, 29, n)

    # ---------- payment history ----------
    parts = []
    for (m, idx, prod, rate, rem, pay, k, bal, st, lit, fe, pipf, capf) in w.hist:
        parts.append(pd.DataFrame(dict(i=idx, m=m, prod=prod, rate=rate, rem=rem, pay=pay, k=k, bal=bal, st=st, fe=fe,
                                       pip=pipf, cap=capf)))
    H = pd.concat(parts, ignore_index=True).sort_values(["i", "m"], kind="stable").reset_index(drop=True)
    same = H.i.eq(H.i.shift())
    newprod = ~same | (H["prod"] != H["prod"].shift())
    H["prod_start"] = np.where(newprod, H.m, np.nan)
    H["prod_start"] = H.groupby("i").prod_start.ffill().astype(int)
    first_prod = H["prod"] == 0
    H.loc[first_prod, "prod_start"] = w.orig_m[H.i[first_prod]]
    H["fix5"] = np.where(first_prod, w.a.fix5.to_numpy()[H.i], (H.fe - H.prod_start) > 30)
    H["code"] = [pcode(p, s, f, r) for p, s, f, r in zip(H["prod"], H.prod_start, H.fix5, H.rate)]
    old = H.m < ym(2022, 7)
    H.loc[old, "code"] = H.loc[old, "code"].str.replace("-", "", regex=False)
    H["arrears"] = (H.k * H.pay).round(2)
    prev_arr = np.where(same, H.arrears.shift(), 0.0)
    H["received"] = np.clip(H.pay + prev_arr - H.arrears, 0, None).round(2)
    # arrears capitalised at a collections term extension move into the balance; the month's payment is all that came in
    H.loc[H.cap, "received"] = H.loc[H.cap, "pay"].round(2)
    # nothing is paid once the property is in possession
    H.loc[H.pip, "received"] = 0.0
    red = H.st == 1
    H.loc[red, "received"] = (H.loc[red, "bal"] + H.loc[red, "arrears"]).round(2)
    # the month an account closes, the redemption or the sale clears its balance and arrears
    shut = H.st > 0
    H.loc[shut, ["arrears", "bal"]] = 0.0
    H.loc[shut, "rem"] = 0
    H["status"] = np.select([H.st == 1, H.st == 2], ["Redeemed", "Possession"], "Live")
    hist = pd.DataFrame({
        "account_number": acct[H.i], "book": [P.BOOKNAME[b] for b in book[H.i]],
        "period": [f"{m // 12}-{m % 12 + 1:02d}" for m in H.m], "product_code": H.code,
        "interest_rate": H.rate.round(2), "remaining_term_months": H.rem.astype(int),
        "contractual_payment": H.pay.round(2), "payment_received": H.received, "arrears_balance": H.arrears,
        "balance": H.bal.round(2), "account_status": H.status})
    dup = hist.sample(frac=0.003, random_state=seed)        # month rows re-sent in a later extract
    hist = pd.concat([hist, dup]).sort_values(["account_number", "period"], kind="stable").reset_index(drop=True)

    # ---------- book at 30 September 2026 ----------
    live = np.where((w.status == 0) & (w.orig_m <= W.SNAP))[0]
    last = H[H.m == W.SNAP].set_index("i")
    bk = pd.DataFrame({
        "account_number": acct[live], "book": [P.BOOKNAME[b] for b in book[live]],
        "completion_date": mdate(w.orig_m[live], day[live]).dt.strftime("%Y-%m-%d"),
        "original_valuation": (np.round(w.value0[live] / 500) * 500).astype(int),
        "original_loan": w.loan0[live].astype(int), "current_balance": w.bal[live].round(2),
        "postcode_district": pcd[live], "property_type": ptype[live],
        "repayment_type": np.where(w.io[live], "Interest only", "Capital and interest"),
        "borrowers": np.where(w.a.joint.to_numpy()[live], 2, 1),
        "product_code": last.code.reindex(live).to_numpy(),
        "product_end_date": mdate(w.fix_end[live] - 1).dt.strftime("%Y-%m-%d"),
        "interest_rate": w.rate[live].round(2), "remaining_term_months": w.rem[live].astype(int),
        "monthly_payment": w.pay[live].round(2), "arrears_balance": (w.k[live] * w.pay[live]).round(2),
        "recovery_stage": np.where(w.lit[live], np.where(book[live] == "BTL", "Receiver appointed", "Litigation"),
                                   "None")}).sort_values("account_number").reset_index(drop=True)

    rec = np.random.default_rng(seed + P.REC_OFFSET)      # the recoveries records draw from their own stream
    dev = np.random.default_rng(seed + P.DEV_OFFSET)      # loan parts and re-sealed orders draw from a third
    poss, sales, recv = possessions(w, acct, book, rec, dev)
    lit = litigation(w, acct, book, rec, dev)
    return dict(w=w, acct=acct, book=book, H=H, hist=hist, bk=bk, rng=rng, pcd=pcd, poss=poss, sales=sales,
                recv=recv, lit=lit)


def possessions(w, acct, book, rng, dev):
    """the possession register, the sales completed and the LPA receiver appointments"""
    ev = pd.DataFrame(w.events, columns=["m", "i", "kind", "bal", "arr"])
    ev = ev[(ev.kind == "possession") & (ev.m >= ym(2019, 1)) & (ev.m <= W.SNAP)].reset_index(drop=True)
    pdate = mdate(ev.m.to_numpy(), w.poss_day[ev.i])
    bk = book[ev.i]
    btl = bk == "BTL"
    legal = np.where(btl, rng.uniform(900, 1800, len(ev)), rng.uniform(2200, 4600, len(ev))).round(2)
    debt = (ev.bal + ev.arr + legal).round(2)
    # the register keeps the book each possession was written under: before the April 2026 re-cut the first-time buyer
    # book held all the Society's lending to first-time buyers, the 2022-24 high loan to value lending and shared
    # ownership included
    label = np.array([P.BOOKNAME[b] for b in bk], dtype=object)
    old = (pdate < pd.Timestamp(P.RECUT)).to_numpy() & np.isin(bk, ["FTB", "HLTV", "SO"])
    label[old] = P.OLD_FTB
    reg = pd.DataFrame({"account_number": acct[ev.i], "book": label,
                        "possession_date": pdate.dt.strftime("%d/%m/%Y"),
                        "route": np.where(btl, "LPA receiver", "Court order"),
                        "debt_at_possession": debt, "_m": ev.m, "_i": ev.i, "_date": pdate,
                        "_book": [P.BOOKNAME[b] for b in bk], "_part": 1})
    # an owner-occupied account with a further advance holds it as a second loan part, and the recoveries system
    # registers each part taken into possession on its own row: the first part carries the legal costs
    two = (~btl) & (dev.random(len(reg)) < P.PART2_SHARE)
    share = dev.uniform(0.08, 0.25, len(reg))
    p2 = reg[two].copy()
    p2["debt_at_possession"] = ((ev.bal + ev.arr).to_numpy()[two] * share[two]).round(2)
    reg.loc[two, "debt_at_possession"] = (reg.debt_at_possession[two] - p2.debt_at_possession).round(2)
    p2["_part"] = 2
    reg = pd.concat([reg, p2]).sort_values(["_date", "account_number", "_part"], kind="stable").reset_index(drop=True)
    # LPA receivers: one appointment for every buy-to-let account that went to recovery since 2019, ended or not;
    # receivers sell and remit under their own reference
    firms = ["Northbank Property Receivers", "Aire & Calder Receiverships"]
    rr = np.random.default_rng(int(rng.integers(0, 2 ** 31)))
    apps = sorted({(int(s), int(i)) for (i, s, e, o, pay) in w.spells if book[i] == "BTL" and s >= ym(2019, 1)})
    recv = pd.DataFrame({"_i": [i for s, i in apps], "_s": [s for s, i in apps]})
    recv["receiver_ref"] = ["RCV-%s-%04d" % (["NPR", "ACR"][j % 2], 1000 + j * 7 + int(rr.integers(0, 6)))
                            for j in range(len(recv))]
    recv["receiver_firm"] = [firms[j % 2] for j in range(len(recv))]
    recv["account_number"] = acct[recv._i.to_numpy()] if len(recv) else []
    recv["date_appointed"] = [mdate(np.array([s]), np.array([rr.integers(1, 29)]))[0].strftime("%d/%m/%Y")
                              for s in recv._s]
    # the appointment a possession belongs to is the account's latest before it
    ref_of = {}
    for i, s, ref in zip(recv._i, recv._s, recv.receiver_ref):
        ref_of.setdefault(int(i), []).append((s, ref))
    recv = recv[["receiver_ref", "receiver_firm", "account_number", "date_appointed"]]
    # sales: the property is sold three to eight months after possession and the account closes that month
    sm = w.sale_m[reg._i]
    sold = (w.status[reg._i] == 2) & (sm >= 0) & (sm <= W.SNAP) & (reg._part == 1).to_numpy()
    sdate = mdate(sm.clip(0), w.sale_day[reg._i])
    val = w.value0[reg._i] * W.hpi(reg._m.to_numpy(), w.region[reg._i]) / W.hpi(w.orig_m[reg._i], w.region[reg._i])
    price = np.round(val * rng.uniform(0.72, 0.90, len(reg)) / 250) * 250
    costs = (price * rng.uniform(0.018, 0.032, len(reg)) + rng.uniform(600, 1400, len(reg))).round(2)
    rows = []
    for j in np.where(sold)[0]:
        is_btl = reg.route.iloc[j] == "LPA receiver"
        mine = [x for x in ref_of.get(int(reg._i.iloc[j]), []) if x[0] <= int(reg._m.iloc[j])]
        # an appointment made before 2019 is not in the extract; its receiver still sells under its own reference
        ref = (max(mine)[1] if mine else "RCV-NPR-0%03d" % (j % 1000)) if is_btl else ""
        # about one buy-to-let sale in five is handed back by the receiver and sold by the Society itself
        by_receiver = is_btl and rng.random() < 0.8
        # a sale completes once, but the Society's own sales issue one completion statement for each loan part
        nparts = int((reg.account_number == reg.account_number.iloc[j]).sum()) if not is_btl else 1
        for _ in range(nparts):
            rows.append({"sale_ref": "", "account_number": "" if by_receiver else reg.account_number.iloc[j],
                         "receiver_ref": ref if by_receiver else "", "completion_date": sdate.iloc[j],
                         "sale_price": float(price[j]), "selling_costs": float(costs[j]), "statement": 1})
    sales = pd.DataFrame(rows).sort_values("completion_date", kind="stable").reset_index(drop=True)
    sales["sale_ref"] = ["SC%05d" % (31000 + k * 3) for k in range(len(sales))]
    # a completion statement corrected after issue is re-sent in full with the corrected figures
    fix = rng.choice(len(sales), max(3, len(sales) // 25), replace=False)
    # a corrected sale is re-sent on every one of its loan parts' statements
    who = sales.account_number.where(sales.account_number != "", sales.receiver_ref) + "|" + sales.completion_date.astype(str)
    factor = pd.Series(rng.uniform(0.85, 1.25, len(fix)), index=who.iloc[fix].to_numpy())
    factor = factor[~factor.index.duplicated()]
    corr = sales[who.isin(factor.index)].copy()
    corr["selling_costs"] = (corr.selling_costs * who[who.isin(factor.index)].map(factor).to_numpy()).round(2)
    corr["statement"] = 2
    sales = pd.concat([sales, corr]).sort_values(["completion_date", "sale_ref", "statement"], kind="stable")
    sales["completion_date"] = pd.to_datetime(sales.completion_date).dt.strftime("%Y-%m-%d")
    sales = sales.reset_index(drop=True)
    return reg, sales, recv


def litigation(w, acct, book, rng, dev):
    """the panel solicitors' actions on every owner-occupied claim open at any time since January 2023"""
    firm_of = {r: P.FIRMS[0] if r in (0, 1, 5) else P.FIRMS[1] for r in range(6)}
    court_of = {0: "Halifax", 1: "Huddersfield", 2: "Leeds", 3: "Bradford", 4: "Wakefield", 5: "Oldham"}
    code_of = {"Halifax": "HX", "Huddersfield": "HD", "Leeds": "LS", "Bradford": "BD", "Wakefield": "WF", "Oldham": "OL"}
    asof = pd.Timestamp(P.ASOF)
    rows = []
    seq = [0]

    def claim_no(court):
        seq[0] += 1
        return "K%d%s%04d" % (6 + seq[0] % 3, code_of[court], 1000 + seq[0] * 7 % 9000)

    def day(m):
        return mdate(np.array([m]), np.array([rng.integers(1, 29)]))[0]

    def days(a, b):
        return pd.Timedelta(days=int(rng.integers(a, b)))

    for (i, start, end, outcome, paying) in sorted(w.spells, key=lambda s: (s[1], s[0])):
        b = book[i]
        if b == "BTL":
            continue
        end_m = W.SNAP if end < 0 else end
        if end_m < ym(2023, 1) and end >= 0:
            continue
        reg = int(w.region[i])
        firm, court = firm_of[reg], court_of[reg]
        joint = bool(w.a.joint.iloc[i])
        claim = claim_no(court)
        ev = []
        t_issue = day(start)
        ev.append((t_issue, "Claim issued", ""))
        t_hear = t_issue + days(75, 125)
        end_t = day(end_m) if end >= 0 else asof + pd.Timedelta(days=1)
        if outcome == "possession":
            end_t = mdate(np.array([end_m]), np.array([w.poss_day[i]]))[0]
        order, t_order = None, None
        if t_hear < end_t:
            ev.append((t_hear - days(20, 40), "Hearing listed", ""))
            if rng.random() < 0.15:
                t_adj = t_hear
                t_hear = t_hear + days(28, 70)
                ev.append((t_adj, "Hearing adjourned", ""))
            if t_hear < end_t:
                order = "suspended" if (paying and outcome != "possession") or (paying and rng.random() < 0.5) else "outright"
                t_order = t_hear
                ev.append((t_hear, "Possession order made", "Suspended on terms" if order == "suspended" else "Outright, 28 days"))
                # the court re-seals an order it has corrected and sends it again; Pennant Moss logs it as made again
                if firm == P.FIRMS[0] and dev.random() < P.RESEAL_SHARE:
                    ev.append((t_hear + pd.Timedelta(days=int(dev.integers(7, 12))), "Possession order made",
                               "Suspended on terms" if order == "suspended" else "Outright, 28 days"))
                # a suspended order the borrower stops keeping to is varied to an outright order at a later hearing
                vary = outcome == "possession" and rng.random() < 0.35 or outcome == "open" and rng.random() < 0.2
                if order == "suspended" and vary:
                    t_var = t_hear + days(40, 120)
                    if t_var < end_t - pd.Timedelta(days=60):
                        ev.append((t_var - days(14, 28), "Hearing listed", ""))
                        ev.append((t_var, "Possession order varied", "Outright, 28 days"))
                        order, t_order = "outright", t_var
                        if firm == P.FIRMS[0] and dev.random() < P.RESEAL_SHARE:
                            ev.append((t_var + pd.Timedelta(days=int(dev.integers(7, 12))), "Possession order varied",
                                       "Outright, 28 days"))
                # a borrower keeping to a suspended order applies to change its terms; the court varies it on new terms
                if order == "suspended" and dev.random() < P.RETERM_SHARE:
                    t_lst = t_order + pd.Timedelta(days=int(dev.integers(40, 200)))
                    t_new = t_lst + pd.Timedelta(days=int(dev.integers(21, 41)))
                    if t_new < min(end_t - pd.Timedelta(days=30), asof):
                        ev.append((t_lst, "Hearing listed", ""))
                        ev.append((t_new, "Possession order varied", "Suspended on terms"))
                # a claim heading for possession soon after the as-of date has its warrant out already
                if outcome == "open" and W.SNAP < w.poss_m[i] <= W.SNAP + 2:
                    t_ev = mdate(np.array([w.poss_m[i]]), np.array([rng.integers(1, 29)]))[0]
                    for back, kind in ((days(45, 70), "Warrant applied"), (days(15, 35), "Warrant issued")):
                        if t_ev - back > t_order:
                            ev.append((t_ev - back, kind, ""))
                # the borrower's own application to vary the terms or suspend is listed and often adjourned
                if outcome == "open" and rng.random() < 0.3:
                    t_app = t_order + days(30, 150)
                    if t_app < asof:
                        ev.append((t_app, "Hearing listed", ""))
                        t_app2 = t_app + days(21, 49)
                        if rng.random() < 0.5 and t_app2 < asof:
                            ev.append((t_app2, "Hearing adjourned", ""))

        if outcome == "possession" and order is not None:
            ev.append((end_t - days(45, 70), "Warrant applied", ""))
            ev.append((end_t - days(15, 35), "Warrant issued", ""))
            if firm == P.FIRMS[0]:
                ev.append((end_t, "Eviction carried out", ""))
        elif outcome == "cured":
            ev.append((end_t, "Order discharged" if order else "Claim withdrawn", "Arrears cleared"))
        elif outcome in ("sold", "bought_back"):
            ev.append((end_t, "Order discharged" if order else "Claim withdrawn",
                       "Redeemed on sale" if outcome == "sold" else "Redeemed on landlord buy-back"))
        ev = sorted([e for e in ev if e[0] <= asof], key=lambda e: e[0])
        # a claim moved to another hearing centre keeps its number
        if rng.random() < 0.08 and len(ev) > 1:
            t_tr = ev[0][0] + days(20, 200)
            new_court = P.COURTS[(P.COURTS.index(court) + 1 + int(rng.integers(0, 4))) % 6]
            if t_tr < ev[-1][0]:
                ev.append((t_tr, "Transferred", "To " + new_court))
                ev = sorted(ev, key=lambda e: e[0])
        here = court
        for (t, kind, note) in ev:
            rows.append((claim, acct[i], firm, here, t, kind, note, joint))
            if kind == "Transferred":
                here = note[3:]
    df = pd.DataFrame(rows, columns=["claim_number", "account_number", "panel_firm", "hearing_centre", "action_date",
                                     "action", "detail", "joint"])
    # Ridley Varga's case system writes one line per defendant
    rv = df[(df.panel_firm == P.FIRMS[1]) & df.joint].copy()
    df["defendant"] = 1
    rv["defendant"] = 2
    df = pd.concat([df, rv]).sort_values(["action_date", "claim_number", "defendant"], kind="stable")
    df["action_date"] = pd.to_datetime(df.action_date).dt.strftime("%Y-%m-%d")
    return df.drop(columns=["joint"]).reset_index(drop=True)
