"""The two ask systems, cut from their own clean truth.

Claims: the customer-service case export, finance's transfer lines, the card gateway's settlement report, the
tracking history of every parcel with a case, and the flat-rate terms of some business accounts.
Stoppages: the sorter historian's event log and the engineering work orders.

Golden ask figures are computed from the records with the handling the filed WHAT and the records support; the
truth they must equal (claims) or match within the work orders' minute (stoppages) is asserted in checks.py.
"""
import datetime as dt
import numpy as np
import pandas as pd
from world import HUBS, HUB_KEYS, UTC_OFFSET_H

HUB_NO = {h[0]: h[1] for h in HUBS}
CS_HUB = {"ZAZ": "ZARAGOZA", "VLC": "VALENCIA", "SEVILLA": "SEVILLA", "SVQ": "SEVILLA", "MAD": "MADRID",
          "BCN": "BARCELONA", "BIO": "BILBAO"}
CMMS_SITE = {"ZAZ": "ZGZ Plaza", "VLC": "VLC Ribarroja", "SVQ": "SVQ Dos Hermanas", "MAD": "MAD San Fernando",
             "BCN": "BCN El Prat", "BIO": "BIO Basauri"}
PROV_HUB = {8: "BCN", 28: "MAD", 41: "SVQ", 46: "VLC", 48: "BIO", 50: "ZAZ", 3: "VLC", 29: "SVQ", 30: "VLC", 15: "MAD"}
Q3 = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
CUTOFF = dt.date(2026, 10, 20)
EXPORT_DAY = dt.date(2026, 10, 23)
OLD_SORTERS = ("ZAZ", "VLC", "SVQ")      # historian collector on the older control network: link losses
SIS_SORTERS = ("MAD", "BCN", "BIO")      # safety system logs to the historian on its own clock
LABEL_TARIFF = (4.95, 5.90, 6.95, 8.50, 9.90, 12.90)


def weekdays(a, b):
    d, out = a, []
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def night_of(local_ts):
    """The sorting night a local timestamp belongs to: dated by the evening it starts."""
    return (pd.Timestamp(local_ts) - pd.Timedelta(hours=12)).date()


# ------------------------------------------------------------------------------------------------------- claims

CLAIM_LAM = {"ZAZ": 21.0, "VLC": 15.0, "SVQ": 16.5, "MAD": 24.0, "BCN": 19.0, "BIO": 7.5}


def flat_rate_accounts(accounts, seed):
    r = np.random.default_rng(seed + 31)
    acc = accounts[accounts.volume_weight > 0].copy()
    acc["prov"] = acc.account.str[1:3].astype(int)
    acc["home"] = acc.prov.map(PROV_HUB)
    picks, quota = [], {"ZAZ": 1, "VLC": 1, "SVQ": 1, "MAD": 2, "BCN": 2, "BIO": 1}
    for h in HUB_KEYS:
        pool = acc[(acc.home == h) & acc.sector.isin(["home and garden", "electronics", "motor and DIY", "office",
                                                         "sports", "toys", "pet supplies"])].account.tolist()
        pool = sorted(pool)
        for a in r.choice(pool, size=quota[h], replace=False):
            picks.append((a, h))
    rates = [15.0, 18.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.0]
    r.shuffle(rates)
    since = ["2024-03-01", "2025-01-01", "2023-09-15", "2025-06-01", "2024-11-01", "2022-05-01", "2025-02-01", "2024-01-01"]
    return pd.DataFrame([(a, h, rates[i], since[i]) for i, (a, h) in enumerate(picks)],
                        columns=["account", "home_hub", "eur_per_carton", "terms_since"])


def claims(accounts, depots, seed):
    r = np.random.default_rng(seed + 30)
    acc = accounts[accounts.volume_weight > 0].copy()
    acc["home"] = acc.account.str[1:3].astype(int).map(PROV_HUB)
    flat = flat_rate_accounts(accounts, seed)
    flat_by_hub = {h: g.account.tolist() for h, g in flat.groupby("home_hub")}
    rate = flat.set_index("account").eur_per_carton
    reg_by_hub = {h: sorted(set(g.account) - set(flat.account)) for h, g in acc.groupby("home")}
    dep_by_hub = {h: sorted(g.depot_code) for h, g in depots.groupby("hub")}
    nights = weekdays(dt.date(2026, 6, 15), dt.date(2026, 10, 9))
    used, rows = set(), []
    for h in HUB_KEYS:
        for d in nights:
            for _ in range(int(r.poisson(CLAIM_LAM[h]))):
                u = r.random()
                kind = "PARTICULAR" if u < 0.33 else ("FLAT" if u < 0.43 else "EMPRESA")
                if kind == "FLAT":
                    account = str(r.choice(flat_by_hub[h]))
                    k = int(np.clip(1 + r.poisson(1.6), 1, 7))
                    amount = round(k * float(rate[account]), 2)
                elif kind == "EMPRESA":
                    account = str(r.choice(reg_by_hub[h])); k = 1
                    amount = float(np.round(np.clip(r.lognormal(np.log(38), 0.8), 5, 600), 2))
                else:
                    account = ""; k = 1
                    amount = float(np.round(np.clip(r.lognormal(np.log(24), 0.65), 4, 180), 2))
                    while amount in LABEL_TARIFF:
                        amount = round(amount + 0.07, 2)
                while True:
                    bc = "BQ%02d%08d%02d" % (int(r.integers(10, 99)), int(r.integers(0, 10 ** 8)), int(r.integers(0, 100)))
                    if bc not in used:
                        used.add(bc); break
                national = r.random() < 0.38
                dest = h if not national else str(r.choice([x for x in HUB_KEYS if x != h]))
                sort_local = dt.datetime.combine(d, dt.time(21, 5)) + dt.timedelta(seconds=int(r.integers(0, 6.6 * 3600)))
                opened = d + dt.timedelta(days=int(1 + national + r.integers(0, 15)))
                u2 = r.random()
                status = "APPROVED" if u2 < 0.81 else ("REJECTED" if u2 < 0.96 else "WITHDRAWN")
                decided = opened + dt.timedelta(days=int(r.integers(2, 21)))
                rows.append(dict(barcode=bc, sort_hub=h, dest_hub=dest, night=d, sort_local=sort_local, kind=kind,
                                 account=account, k=k, amount=amount, opened=opened, status=status, decided=decided,
                                 origin_depot=str(r.choice(dep_by_hub[h])), dest_depot=str(r.choice(dep_by_hub[dest]))))
    t = pd.DataFrame(rows)
    # private senders' amounts unique among cases decided within ten days of each other (one match per refund)
    priv = t[(t.kind == "PARTICULAR") & (t.status == "APPROVED")].sort_values("decided")
    seen = {}
    for i, row in priv.iterrows():
        a = row.amount
        while any(abs((row.decided - dd).days) <= 10 for dd in seen.get(a, [])) or a in LABEL_TARIFF:
            a = round(a + 0.11, 2)
        t.at[i, "amount"] = a
        seen.setdefault(a, []).append(row.decided)
    # payments
    t["pay_date"] = pd.NaT
    t["reopen"] = (t.kind == "EMPRESA") & (t.status == "APPROVED") & (r.random(len(t)) < 0.07)
    t["top_up"] = np.where(t.reopen, np.round(t.amount * r.uniform(0.25, 1.4, len(t)), 2), 0.0)
    t["ro_opened"] = [d + dt.timedelta(days=int(x)) for d, x in zip(t.decided, r.integers(9, 30, len(t)))]
    t["ro_decided"] = [d + dt.timedelta(days=int(x)) for d, x in zip(t.ro_opened, r.integers(4, 16, len(t)))]
    return t, flat


def _thursday_after(d, lag):
    x = d + dt.timedelta(days=lag)
    while x.weekday() != 3:
        x += dt.timedelta(days=1)
    return x


def claim_records(t, flat, seed):
    """The case export (pulled 23 October), finance's transfer lines, the gateway's refund settlement report and the
    tracking history of every parcel with a case."""
    r = np.random.default_rng(seed + 32)
    t = t.sort_values(["opened", "barcode"]).reset_index(drop=True)
    ref = int(r.integers(7140000, 7190000))
    case_rows, pay_rows, ref_rows = [], [], []
    pref = int(r.integers(5520000, 5560000))
    case_of, paid = {}, {}
    def book(bc, day, amt):
        if day <= CUTOFF:
            paid[bc] = round(paid.get(bc, 0.0) + amt, 2)
    for c in t.itertuples():
        if c.opened > EXPORT_DAY:
            continue
        ref += int(r.integers(1, 6))
        cref = "SIN-%d" % ref
        case_of[c.barcode] = cref
        st = c.status if c.decided <= EXPORT_DAY else "OPEN"
        claimant = "PARTICULAR" if c.kind == "PARTICULAR" else "EMPRESA"
        case_rows.append((cref, c.barcode, claimant, c.account, c.opened.isoformat(), st,
                          c.decided.isoformat() if st != "OPEN" else "", c.amount if st == "APPROVED" else np.nan,
                          CS_HUB[c.dest_hub]))
        if st != "APPROVED":
            continue
        if claimant == "EMPRESA":
            vd = _thursday_after(c.decided, 2)
            if vd <= EXPORT_DAY:
                pref += int(r.integers(1, 13))
                pay_rows.append(("TR%d" % pref, cref, c.account, vd.isoformat(), c.amount))
                book(c.barcode, vd, c.amount)
                if r.random() < 0.025:   # returned by the payee's bank, re-issued on a later run
                    rd = vd + dt.timedelta(days=int(r.integers(3, 6)))
                    pref += int(r.integers(1, 13))
                    pay_rows.append(("TR%d" % pref, cref, c.account, rd.isoformat(), -c.amount))
                    book(c.barcode, rd, -c.amount)
                    ri = _thursday_after(rd, 1)
                    pref += int(r.integers(1, 13))
                    pay_rows.append(("TR%d" % pref, cref, c.account, ri.isoformat(), c.amount))
                    book(c.barcode, ri, c.amount)
        else:
            when = dt.datetime.combine(c.decided + dt.timedelta(days=int(r.integers(0, 3))), dt.time(8, 0)) + \
                dt.timedelta(seconds=int(r.integers(0, 13.5 * 3600)))
            ref_rows.append((when - dt.timedelta(hours=UTC_OFFSET_H), c.amount))
            book(c.barcode, when.date(), c.amount)
        if c.reopen and c.ro_opened <= EXPORT_DAY:
            ref += int(r.integers(1, 6))
            cref2 = "SIN-%d" % ref
            st2 = "APPROVED" if c.ro_decided <= EXPORT_DAY else "OPEN"
            case_rows.append((cref2, c.barcode, "EMPRESA", c.account, c.ro_opened.isoformat(), st2,
                              c.ro_decided.isoformat() if st2 == "APPROVED" else "",
                              round(c.amount + c.top_up, 2) if st2 == "APPROVED" else np.nan, CS_HUB[c.dest_hub]))
            if st2 == "APPROVED":
                vd2 = _thursday_after(c.ro_decided, 2)
                if vd2 <= EXPORT_DAY:
                    pref += int(r.integers(1, 13))
                    pay_rows.append(("TR%d" % pref, cref2, c.account, vd2.isoformat(), c.top_up))
                    book(c.barcode, vd2, c.top_up)
    cases = pd.DataFrame(case_rows, columns=["case_ref", "tracking_no", "claimant", "account", "opened", "status",
                                             "decided", "approved_eur", "hub"])
    cases = cases.sort_values(["opened", "case_ref"]).reset_index(drop=True)
    pays = pd.DataFrame(pay_rows, columns=["payment_ref", "case_ref", "payee", "value_date", "amount_eur"])
    pays = pays.sort_values(["value_date", "payment_ref"]).reset_index(drop=True)
    # label cancellations refunded through the same gateway, at the tariff's prices
    canc = []
    for d in weekdays(dt.date(2026, 7, 1), dt.date(2026, 10, 22)):
        for _ in range(int(r.poisson(9))):
            when = dt.datetime.combine(d, dt.time(8, 0)) + dt.timedelta(seconds=int(r.integers(0, 13.5 * 3600)))
            canc.append((when - dt.timedelta(hours=UTC_OFFSET_H), float(r.choice(LABEL_TARIFF))))
    allr = [(a, b) for a, b in ref_rows + canc if a.date() <= dt.date(2026, 10, 22)]
    allr.sort(key=lambda x: x[0])
    gid = []
    for _ in allr:
        gid.append("re_%s" % "".join(r.choice(list("ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789"), 18)))
    refunds = pd.DataFrame({"id": gid, "type": "refund", "created_utc": [a.strftime("%Y-%m-%d %H:%M:%S") for a, _ in allr],
                            "amount": [b for _, b in allr], "currency": "eur", "status": "succeeded",
                            "card_brand": r.choice(["visa", "mastercard", "visa", "visa", "amex"], len(allr)),
                            "card_last4": ["%04d" % int(x) for x in r.integers(0, 10000, len(allr))]})
    # tracking history of every parcel with a case
    trk = []
    for c in t.itertuples():
        if c.barcode not in case_of:
            continue
        col = dt.datetime.combine(c.night, dt.time(16, 0)) + dt.timedelta(seconds=int(r.integers(0, 4 * 3600)))
        trk.append((c.barcode, "COLLECTED", c.origin_depot, col))
        trk.append((c.barcode, "SORT", "PLAT-%02d" % HUB_NO[c.sort_hub], c.sort_local))
        t2 = c.sort_local
        if c.dest_hub != c.sort_hub:
            t2 = dt.datetime.combine(c.night + dt.timedelta(days=1), dt.time(21, 20)) + \
                dt.timedelta(seconds=int(r.integers(0, 6 * 3600)))
            trk.append((c.barcode, "SORT", "PLAT-%02d" % HUB_NO[c.dest_hub], t2))
        din = dt.datetime.combine(t2.date() + dt.timedelta(days=1 if t2.hour >= 12 else 0), dt.time(6, 0)) + \
            dt.timedelta(seconds=int(r.integers(0, 3600)))
        trk.append((c.barcode, "DEPOT_IN", c.dest_depot, din))
        trk.append((c.barcode, "OUT_FOR_DELIVERY", c.dest_depot, din + dt.timedelta(minutes=int(r.integers(40, 150)))))
        trk.append((c.barcode, "DELIVERED", c.dest_depot, din + dt.timedelta(minutes=int(r.integers(160, 600)))))
    tr = pd.DataFrame(trk, columns=["tracking_no", "event", "location", "ts_local"])
    tr["ts_utc"] = (pd.to_datetime(tr.ts_local) - pd.Timedelta(hours=UTC_OFFSET_H)).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tr = tr.drop(columns=["ts_local"]).sort_values(["ts_utc", "tracking_no"], kind="mergesort").reset_index(drop=True)
    return cases, pays, refunds, tr, paid


def claims_golden(cases, pays, refunds, tracking, terms):
    """Per hub: damaged parcels with a case approved by 20 October (a flat-rate case counts its cartons, the approved
    amount over the account's rate) and the euros paid on them by 20 October (transfers net of returns, plus the card
    refunds each matched to its case by amount after the decision). Hub and night from the parcel's first sort."""
    tr = tracking[tracking.event == "SORT"].sort_values(["tracking_no", "ts_utc"]).drop_duplicates("tracking_no")
    loc_hub = {"PLAT-%02d" % v: k for k, v in HUB_NO.items()}
    sort_hub = tr.set_index("tracking_no").location.map(loc_hub)
    night = (pd.to_datetime(tr.ts_utc.str[:19]) + pd.Timedelta(hours=UTC_OFFSET_H)).map(night_of)
    night = pd.Series(night.values, index=tr.tracking_no.values)
    first = cases.sort_values(["opened", "case_ref"]).drop_duplicates("tracking_no")
    first = first[(first.status == "APPROVED") & (first.decided <= CUTOFF.isoformat())]
    first = first[first.tracking_no.map(night).between(Q3[0], Q3[1])].copy()
    rate = terms.set_index("account").eur_per_carton
    k = (first.approved_eur / first.account.map(rate)).round()
    first["k"] = np.where(first.account.isin(rate.index), k, 1).astype(int)
    first["hub"] = first.tracking_no.map(sort_hub)
    cnt = first.groupby("hub").k.sum().reindex(HUB_KEYS).fillna(0).astype(int)
    keep = set(first.tracking_no)
    case_parcel = cases.set_index("case_ref").tracking_no
    p = pays[pays.value_date <= CUTOFF.isoformat()]
    p = p.assign(parcel=p.case_ref.map(case_parcel))
    p = p[p.parcel.isin(keep)]
    eur = p.assign(hub=p.parcel.map(sort_hub)).groupby("hub").amount_eur.sum()
    m = match_refunds(cases, refunds)
    m = m[(m.parcel.isin(keep)) & (m.created_utc.str[:10] <= CUTOFF.isoformat())]
    eur = eur.add(m.assign(hub=m.parcel.map(sort_hub)).groupby("hub").amount.sum(), fill_value=0)
    return pd.DataFrame({"claims": cnt, "claims_eur": eur.reindex(HUB_KEYS).fillna(0).round(2)}), first


def match_refunds(cases, refunds, days=3, order="earliest"):
    """Each private sender's approved case to the refund of its amount created on or after its decision, within the
    window, one refund per case."""
    pc = cases[(cases.claimant == "PARTICULAR") & (cases.status == "APPROVED")].copy()
    pc = pc.sort_values(["decided", "case_ref"]) if order == "earliest" else pc.sort_values(["decided", "case_ref"], ascending=False)
    rf = refunds.copy()
    rf["d"] = pd.to_datetime(rf.created_utc).dt.date
    taken, out = set(), []
    by_amt = {a: g for a, g in rf.groupby("amount")}
    for c in pc.itertuples():
        g = by_amt.get(round(float(c.approved_eur), 2))
        if g is None:
            continue
        dd = dt.date.fromisoformat(c.decided)
        cand = g[(g.d >= dd) & (g.d <= dd + dt.timedelta(days=days)) & ~g.id.isin(taken)]
        if len(cand):
            x = cand.iloc[0]
            taken.add(x.id)
            out.append((c.case_ref, c.tracking_no, x.id, x.created_utc, float(x.amount)))
    return pd.DataFrame(out, columns=["case_ref", "parcel", "refund_id", "created_utc", "amount"])


def claims_truth(t, paid):
    """The clean truth the golden must equal: every approved parcel's cartons and the money booked on it."""
    x = t[t.night.between(Q3[0], Q3[1]) & (t.status == "APPROVED") & (t.decided <= CUTOFF)].copy()
    x["eur"] = x.barcode.map(paid).fillna(0.0)
    g = x.groupby("sort_hub")
    return pd.DataFrame({"claims": g.k.sum().reindex(HUB_KEYS).fillna(0).astype(int),
                         "claims_eur": g.eur.sum().reindex(HUB_KEYS).fillna(0).round(2)})


# ----------------------------------------------------------------------------------------------------- stoppages

STOP_RATE = {"ZAZ": 2.6, "VLC": 2.9, "SVQ": 3.3, "MAD": 3.8, "BCN": 3.4, "BIO": 2.4}
PLC_REASONS = ["JAM", "JAM", "JAM", "TRAY_FAULT", "OVERLOAD", "MANUAL", "SCANNER"]
SIS_REASONS = ["ESTOP", "LCURTAIN", "GATE"]


def stoppages(seed):
    """Truth: one row per standstill on the sorting nights (20:30 to 05:00 local, dated by the evening)."""
    r = np.random.default_rng(seed + 20)
    nights = weekdays(dt.date(2026, 6, 29), dt.date(2026, 10, 2))
    rows, gaps = [], []
    for h in HUB_KEYS:
        gap_nights = set()
        if h in OLD_SORTERS:
            q3n = [d for d in nights if Q3[0] <= d <= Q3[1]]
            gap_nights = set(q3n[int(i)] for i in r.choice(len(q3n), int(r.integers(4, 6)), replace=False))
        for d in nights:
            open_ = dt.datetime.combine(d, dt.time(20, 30)) + dt.timedelta(seconds=int(r.integers(0, 900)))
            close = dt.datetime.combine(d + dt.timedelta(days=1), dt.time(4, 25)) + dt.timedelta(seconds=int(r.integers(0, 1800)))
            g = None
            if d in gap_nights:
                g0 = open_ + dt.timedelta(seconds=int(r.integers(1800, 4 * 3600)))
                g = (g0, g0 + dt.timedelta(seconds=int(r.integers(70 * 60, 200 * 60))))
                gaps.append((h, d, g[0], g[1]))
            k = int(r.poisson(STOP_RATE[h]))
            starts = np.sort(r.uniform(300, (close - open_).total_seconds() - 1500, k))
            last_end = -1.0
            spells = []
            for s in starts:
                if s < last_end + 150:
                    continue
                dur = float(np.clip(r.lognormal(np.log(420), 0.95), 45, 2.5 * 3600))
                t0 = open_ + dt.timedelta(seconds=int(s)); t1 = t0 + dt.timedelta(seconds=int(dur))
                if t1 >= close - dt.timedelta(minutes=5):
                    continue
                if g is not None and (t0 < g[1] and t1 > g[0]):
                    continue   # placed separately below
                last_end = s + dur
                spells.append((t0, t1))
            if g is not None:   # standstills while the collector was disconnected: one or two, each attended
                n_in = int(r.integers(1, 3))
                span = (g[1] - g[0]).total_seconds()
                cuts = np.sort(r.uniform(0.08, 0.92, n_in))
                for c_ in cuts:
                    t0 = g[0] + dt.timedelta(seconds=int(c_ * span))
                    dur = float(r.uniform(11 * 60, min(48 * 60, 0.4 * span)))
                    t1 = t0 + dt.timedelta(seconds=int(dur))
                    if t1 < g[1] - dt.timedelta(minutes=3) and all(t1 < a or t0 > b for a, b in spells):
                        spells.append((t0, t1))
            for t0, t1 in sorted(spells):
                safety = bool(r.random() < 0.34)
                rows.append(dict(hub=h, night=d, t0=t0, t1=t1, safety=safety, open_=open_, close=close,
                                 in_gap=bool(g is not None and t0 >= g[0] and t1 <= g[1])))
    st = pd.DataFrame(rows)
    st["hours"] = (st.t1 - st.t0).dt.total_seconds() / 3600.0
    gp = pd.DataFrame(gaps, columns=["hub", "night", "g0", "g1"])
    return st, gp


def stoppage_records(st, gp, seed):
    """The historian's event log (UTC; the historian's own ALIVE rows every quarter hour; the sorter PLC's STOP, RUN,
    SORT_START and SORT_END; at the newer sorters the safety system's STOP and RUN on its own clock) and the
    engineering work orders (local, to the minute)."""
    r = np.random.default_rng(seed + 21)
    ev = []
    q3_start = dt.datetime(2026, 7, 1)
    nights = st.drop_duplicates(["hub", "night"])[["hub", "night", "open_", "close"]]
    for n in nights.itertuples():
        ev.append((n.hub, "PLC", "SORT_START", "", n.open_))
        ev.append((n.hub, "PLC", "SORT_END", "", n.close))
        t = dt.datetime.combine(n.night, dt.time(20, 0))
        while t <= dt.datetime.combine(n.night + dt.timedelta(days=1), dt.time(5, 30)):
            ev.append((n.hub, "HIST", "ALIVE", "", t))
            t += dt.timedelta(minutes=15)
    lost = np.zeros(len(st), dtype=bool)
    for i, s in enumerate(st.itertuples()):
        if s.in_gap:
            continue
        reason = "SAFETY" if s.safety else str(r.choice(PLC_REASONS))
        drop = bool(s.safety and s.hub in SIS_SORTERS and r.random() < 0.13)
        lost[i] = drop
        if not drop:
            ev.append((s.hub, "PLC", "STOP", reason, s.t0))
        ev.append((s.hub, "PLC", "RUN", "", s.t1))
        if s.safety and s.hub in SIS_SORTERS:
            days = (s.t0 - q3_start).total_seconds() / 86400.0
            off = dt.timedelta(seconds=int(38 + 4.1 * days + r.integers(0, 6)))
            reset = s.t1 - dt.timedelta(seconds=int(r.integers(6, 45)))
            code = "%s_%02d" % (r.choice(SIS_REASONS), int(r.integers(1, 15)))
            ev.append((s.hub, "SIS", "STOP", code, s.t0 - off))
            ev.append((s.hub, "SIS", "RUN", "", reset - off))
    st["lost_stop"] = lost
    e = pd.DataFrame(ev, columns=["hub", "source", "event", "reason", "ts_local"])
    e["hub_no"] = e.hub.map(HUB_NO)
    e["line"] = "S1"
    e["ts_utc"] = (e.ts_local - pd.Timedelta(hours=UTC_OFFSET_H)).dt.strftime("%Y-%m-%d %H:%M:%S")
    e = e.sort_values(["hub_no", "ts_utc", "source", "event"], kind="mergesort").reset_index(drop=True)
    events = e[["hub_no", "line", "source", "event", "reason", "ts_utc"]]
    # work orders: every standstill of ten minutes or more is attended and gets a corrective order; some shorter ones
    wo, seq = [], int(r.integers(410000, 440000))
    assets = ["induction belt 2", "merge 1", "merge 2", "tilt tray drive", "tray tilt coil", "chute gate",
              "scanner arch", "light curtain", "e-stop circuit", "PLC I/O card", "carrier chain", "sorter loop motor"]
    actions = ["cleared jam and tested", "reset and tested", "replaced proximity sensor", "adjusted belt tension",
               "replaced fuse", "re-seated connector", "replaced tilt coil", "cleaned scanner window",
               "re-aligned photocell", "replaced drive contactor"]
    for s in st.itertuples():
        u = r.random()
        if not (s.in_gap or (s.t1 - s.t0).total_seconds() >= 600 or u < 0.05):
            continue
        seq += int(r.integers(1, 9))
        ms = (s.t0 + dt.timedelta(seconds=30)).replace(second=0)
        mr = (s.t1 + dt.timedelta(seconds=30)).replace(second=0)
        rep = ms + dt.timedelta(minutes=int(r.integers(1, 6)))
        clo = mr + dt.timedelta(minutes=int(r.integers(5, 90)))
        wo.append(("OT-%d" % seq, CMMS_SITE[s.hub], str(r.choice(assets)), "CORRECTIVE", rep, ms, mr, clo,
                   str(r.choice(actions))))
    for h in HUB_KEYS:
        for d in weekdays(dt.date(2026, 6, 29), dt.date(2026, 10, 2)):
            if d.weekday() == 1 or (d.weekday() == 3 and r.random() < 0.5):
                seq += int(r.integers(1, 9))
                t0 = dt.datetime.combine(d, dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(0, 300)))
                wo.append(("OT-%d" % seq, CMMS_SITE[h], str(r.choice(assets)), "PREVENTIVE", t0, pd.NaT, pd.NaT,
                           t0 + dt.timedelta(minutes=int(r.integers(45, 240))), "planned maintenance routine"))
    wos = pd.DataFrame(wo, columns=["work_order", "site", "asset", "order_type", "reported", "machine_stopped",
                                    "machine_running", "closed", "work_done"])
    wos = wos.sort_values(["reported", "work_order"]).reset_index(drop=True)
    return events, wos


def plc_spells(events):
    """The sorter PLC's STOP to RUN spells (local), and the RUNs no STOP precedes."""
    e = events[(events.source == "PLC") & events.event.isin(["STOP", "RUN"])].copy()
    e["ts"] = pd.to_datetime(e.ts_utc) + pd.Timedelta(hours=UTC_OFFSET_H)
    no2key = {v: k for k, v in HUB_NO.items()}
    spells, lone = [], []
    for h, g in e.groupby("hub_no"):
        stop = None
        for x in g.sort_values("ts", kind="mergesort").itertuples():
            if x.event == "STOP":
                stop = (x.ts, x.reason)
            elif stop is not None:
                spells.append((no2key[h], stop[0], x.ts, stop[1])); stop = None
            else:
                lone.append((no2key[h], x.ts))
    return (pd.DataFrame(spells, columns=["hub", "t0", "t1", "reason"]),
            pd.DataFrame(lone, columns=["hub", "t1"]))


def sis_pairs(events, sp, window=12, tol=20):
    """Pair the safety system's STOPs with the PLC's SAFETY stops through the safety clock's own offset: a first
    pass on the unmistakable pairs (the next SAFETY stop within the window whose spell outlasts the safety spell by
    under a minute), a straight line through their offsets, then every safety STOP read against that line."""
    s = events[(events.source == "SIS") & events.event.isin(["STOP", "RUN"])].copy()
    s["ts"] = pd.to_datetime(s.ts_utc) + pd.Timedelta(hours=UTC_OFFSET_H)
    no2key = {v: k for k, v in HUB_NO.items()}
    s["hub"] = s.hub_no.map(no2key)
    rows = []
    for h, g in s.groupby("hub"):
        g = g.sort_values("ts", kind="mergesort")
        stop = None
        for x in g.itertuples():
            if x.event == "STOP":
                stop = x.ts
            elif stop is not None:
                rows.append((h, stop, x.ts)); stop = None
    ss = pd.DataFrame(rows, columns=["hub", "s0", "s1"])
    saf = sp[sp.reason == "SAFETY"]
    out = []
    for h, g in ss.groupby("hub"):
        f = saf[saf.hub == h]
        first = []
        for x in g.itertuples():
            c = f[(f.t0 >= x.s0) & (f.t0 <= x.s0 + pd.Timedelta(minutes=window))]
            c = c[((c.t1 - c.t0) - (x.s1 - x.s0)).dt.total_seconds().between(0, 60)]
            if len(c) == 1:
                first.append(((x.s0 - pd.Timestamp("2026-07-01")).total_seconds() / 86400.0,
                              (c.t0.iloc[0] - x.s0).total_seconds()))
        a = np.array(first)
        slope, icpt = np.polyfit(a[:, 0], a[:, 1], 1)
        for x in g.itertuples():
            d = (x.s0 - pd.Timestamp("2026-07-01")).total_seconds() / 86400.0
            trip = x.s0 + pd.Timedelta(seconds=float(icpt + slope * d))
            hit = f[(f.t0 - trip).abs() <= pd.Timedelta(seconds=tol)]
            out.append((h, x.s0, x.s1, trip, len(hit) > 0))
    return pd.DataFrame(out, columns=["hub", "s0", "s1", "trip", "echo"])


def stoppages_golden(events, wos, tol=20, wo_window=2):
    """Per hub over the July to September sorting nights: the PLC's spells; a safety stop whose PLC STOP the log lost
    starts at the safety system's STOP read on the PLC's clock and ends at the PLC's next RUN; an attended standstill
    the log lost entirely is its corrective order's machine stopped to machine running."""
    sp, lone = plc_spells(events)
    sp["src"] = "plc"
    parts = [sp[["hub", "t0", "t1", "src"]]]
    pr = sis_pairs(events, sp, tol=tol)
    extra = []
    for x in pr[~pr.echo].itertuples():
        nxt = lone[(lone.hub == x.hub) & (lone.t1 > x.trip)].sort_values("t1")
        if len(nxt):
            extra.append((x.hub, x.trip, nxt.t1.iloc[0], "sis"))
    parts.append(pd.DataFrame(extra, columns=["hub", "t0", "t1", "src"]))
    logged = pd.concat(parts, ignore_index=True)
    site2key = {v: k for k, v in CMMS_SITE.items()}
    w = wos[wos.order_type == "CORRECTIVE"].copy()
    w["hub"] = w.site.map(site2key)
    wex = []
    for x in w.itertuples():
        hit = logged[(logged.hub == x.hub) & (logged.t0 <= x.machine_running + pd.Timedelta(minutes=wo_window)) &
                     (logged.t1 >= x.machine_stopped - pd.Timedelta(minutes=wo_window))]
        if len(hit) == 0:
            wex.append((x.hub, x.machine_stopped, x.machine_running, "wo"))
    allsp = pd.concat([logged, pd.DataFrame(wex, columns=["hub", "t0", "t1", "src"])], ignore_index=True)
    allsp["night"] = allsp.t0.map(night_of)
    allsp = allsp[(allsp.night >= Q3[0]) & (allsp.night <= Q3[1])].copy()
    allsp["hours"] = (allsp.t1 - allsp.t0).dt.total_seconds() / 3600.0
    g = allsp.groupby("hub")
    return pd.DataFrame({"stoppages": g.size().reindex(HUB_KEYS).astype(int),
                         "hours_stood": g.hours.sum().reindex(HUB_KEYS).round(4)}), allsp
