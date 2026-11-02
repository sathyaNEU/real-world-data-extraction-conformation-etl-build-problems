"""The clean world: Siersma's assortment, the trade stores and webshop orders the Venlo site picked in 2026, who picked
each line and when, which lines failed pack-out verification, the store deliveries and their cages, the stores'
claims, and the client's plan for the first quarter of 2027. Nothing here is messy; pack.py writes the systems'
exports from it."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P


def rng(tag):
    return np.random.default_rng([P.SEED, sum(ord(c) * (i + 1) for i, c in enumerate(tag))])


def ean13(body12):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(body12))
    return body12 + str((10 - s % 10) % 10)


def gs1_check(body):
    s = sum(int(d) * (3 if (len(body) - i) % 2 else 1) for i, d in enumerate(body))
    return body + str((10 - s % 10) % 10)


def calendar():
    days = pd.date_range("2026-01-01", "2026-12-31", freq="D").date
    trade = [d for d in days if d.weekday() < 5 and d not in P.HOLIDAYS]
    web = [d for d in days if d.weekday() < 6 and d not in P.HOLIDAYS and d != dt.date(2026, 6, 13)]
    return trade, web


NAMES = {
    "DLY": [("Douchegel", ["Citrus", "Lavendel", "Kokos", "Munt", "Amandel", "Granaatappel", "Sensitive", "Oceaan", "Vanille", "Gember"], ["250 ml", "400 ml"]),
            ("Deo roller", ["Fresh", "Sensitive", "Cotton", "Active", "Floral"], ["50 ml"]),
            ("Deo spray", ["Fresh", "Sensitive", "Cotton", "Active", "Floral", "Invisible"], ["150 ml", "200 ml"]),
            ("Bodylotion", ["Shea", "Aloe", "Sensitive", "Kokos", "Amandel"], ["250 ml", "400 ml"]),
            ("Handzeep", ["Citrus", "Lavendel", "Aloe", "Olijf", "Sensitive"], ["300 ml", "500 ml navul"]),
            ("Showerfoam", ["Citrus", "Munt", "Kokos", "Framboos"], ["200 ml"])],
    "HAI": [("Shampoo", ["Volume", "Repair", "Anti-roos", "Kleur", "Krul", "Dagelijks", "Zilver", "Arganolie"], ["250 ml", "500 ml"]),
            ("Conditioner", ["Volume", "Repair", "Kleur", "Krul", "Dagelijks", "Arganolie"], ["200 ml", "400 ml"]),
            ("Haarmasker", ["Repair", "Kleur", "Krul", "Arganolie"], ["200 ml"]),
            ("Styling gel", ["Strong", "Wet look", "Matt"], ["150 ml"]),
            ("Haarspray", ["Strong", "Flexibel", "Volume"], ["300 ml"])],
    "SKN": [("Dagcreme", ["Hydra", "Anti-age", "Sensitive", "SPF 15", "Matt"], ["50 ml"]),
            ("Nachtcreme", ["Hydra", "Anti-age", "Sensitive", "Repair"], ["50 ml"]),
            ("Reinigingsgel", ["Normaal", "Sensitive", "Onzuivere huid"], ["150 ml"]),
            ("Gezichtsmasker", ["Klei", "Hydra", "Peel-off", "Sheet 5 st"], ["75 ml", "5 st"]),
            ("Micellair water", ["Normaal", "Sensitive", "Bi-fase"], ["400 ml"]),
            ("Lippenbalsem", ["Naturel", "Aardbei", "SPF 20"], ["4,8 g"])],
    "KID": [("Kids badschuim", ["Aardbei", "Appel", "Kauwgom", "Banaan"], ["500 ml"]),
            ("Kids shampoo", ["Anti-klit", "Aardbei", "Appel", "Mild"], ["250 ml"]),
            ("Kids douchegel", ["Aardbei", "Appel", "Kauwgom", "Framboos"], ["250 ml"]),
            ("Kids tandpasta", ["Aardbei", "Mint mild"], ["75 ml"])],
    "MEN": [("Men deo spray", ["Sport", "Fresh", "Black", "Sensitive", "Arctic", "Wood"], ["150 ml"]),
            ("Men douchegel", ["Sport", "Fresh", "Black", "3-in-1", "Arctic", "Wood"], ["250 ml", "400 ml"]),
            ("Men scheergel", ["Sensitive", "Fresh", "Comfort"], ["200 ml"]),
            ("Men aftershave balm", ["Sensitive", "Fresh"], ["100 ml"]),
            ("Men face wash", ["Fresh", "Charcoal"], ["150 ml"])],
    "SUN": [("Zonnebrand", ["SPF 15", "SPF 30", "SPF 50", "SPF 50+ Kids", "SPF 30 Sport"], ["200 ml", "100 ml"]),
            ("Zonnespray", ["SPF 30", "SPF 50", "SPF 50+ Kids"], ["200 ml"]),
            ("Aftersun", ["Aloe", "Cooling"], ["200 ml", "400 ml"]),
            ("Zonnestick", ["SPF 50", "SPF 50+ Kids"], ["15 g"])],
}


def articles():
    r = rng("articles")
    rows, used_sku, used_art = [], set(), set()
    for code, name, n, inner, pack, _k, _tw, _ww in P.RANGES:
        variants = [(base, v, s) for base, vs, sizes in NAMES[code] for v in vs for s in sizes]
        r.shuffle(variants)
        variants = variants[:n] if len(variants) >= n else variants + [
            (b, v + " limited", s) for b, v, s in variants[: n - len(variants)]]
        for base, var, size in variants:
            while True:
                sku = int(r.integers(4100000, 4999999))
                if sku not in used_sku:
                    used_sku.add(sku)
                    break
            while True:
                art = int(r.integers(201000, 289999))
                if art not in used_art:
                    used_art.add(art)
                    break
            ean = ean13("8714593" + "%05d" % (art % 100000))
            case = int(r.choice([24, 24, 36, 48])) if inner in (6, 12) else int(r.choice([24, 32, 48]))
            if case % inner:
                case = inner * max(2, case // inner)
            rows.append(dict(sku=sku, article_no=art, ean=ean, description="%s %s %s" % (base, var, size),
                             range=code, inner=inner, store_pack=pack, case_qty=case,
                             pop=float(r.lognormal(0, 0.9))))
    a = pd.DataFrame(rows)
    # a few launches during 2026 and a few delistings, as a real assortment carries
    n = len(a)
    launch = np.full(n, None, object)
    delist = np.full(n, None, object)
    idx = r.choice(n, 22, replace=False)
    for k, i in enumerate(idx):
        if k < 14:
            launch[i] = dt.date(2026, int(r.integers(2, 11)), 1) + dt.timedelta(days=int(r.integers(0, 6)))
        else:
            delist[i] = dt.date(2026, int(r.integers(4, 12)), 1) - dt.timedelta(days=1)
    a["launch"] = launch
    a["delist"] = delist
    return a


def stores():
    r = rng("stores")
    rows = []
    used = set()
    for code, name, n, route, ref in P.GROUPS:
        for _ in range(n):
            while True:
                no = int(r.integers(1001, 1999)) if code != "ZLF" else int(r.integers(5001, 7999))
                if (code, no) not in used:
                    used.add((code, no))
                    break
            days = [int(r.integers(0, 5))]
            if r.random() < 0.3:
                days.append((days[0] + int(r.choice([2, 3]))) % 5)
            rows.append(dict(group=code, store_no=no, days=tuple(sorted(set(days))), size=float(r.uniform(7, 20))))
    return pd.DataFrame(rows)


def _active(a, day):
    return [(l is None or day >= l) and (d is None or day <= d) for l, d in zip(a["launch"], a["delist"])]


def trade_orders(a, st, trade_days):
    r = rng("trade")
    rng_code = {c: i for i, (c, *_rest) in enumerate(P.RANGES)}
    tw = {c: t for c, _n, _a, _i, _p, _k, t, _w in P.RANGES}
    kdist = {c: k for c, _n, _a, _i, _p, k, _t, _w in P.RANGES}
    out = []
    order_no = 31840211
    for day in trade_days:
        act = np.array(_active(a, day))
        sun = P.SUN_SEASON[day.month]
        w = np.array([tw[c] * (sun if c == "SUN" else 1.0) for c in a["range"]]) * a["pop"].values * act
        # normalise within range so range shares follow the trade weights
        for c in rng_code:
            m = (a["range"].values == c) & act
            if m.any():
                w[m] = w[m] / w[m].sum() * tw[c] * (sun if c == "SUN" else 1.0)
        w = w / w.sum()
        todays = st[[day.weekday() in d for d in st["days"]]]
        for s in todays.itertuples():
            n = int(min(4 + r.poisson(s.size), 45))
            idx = r.choice(len(a), n, replace=False, p=w)
            order_no += int(r.integers(1, 9))
            for line, i in enumerate(sorted(idx, key=lambda j: (a["range"].iat[j], a["sku"].iat[j])), start=1):
                vals, pr = kdist[a["range"].iat[i]]
                k = int(r.choice(vals, p=pr))
                out.append((order_no, line, day, "T", s.group, s.store_no, int(i), int(a["store_pack"].iat[i]) * k))
    df = pd.DataFrame(out, columns=["order_no", "line_no", "day", "channel", "group", "store_no", "art", "qty"])
    return df


def web_orders(a, web_days):
    r = rng("web")
    ww = {c: w for c, _n, _a, _i, _p, _k, _t, w in P.RANGES}
    vals, pr = P.WEB_QTY
    rows = []
    order_no = 60412873
    for day in web_days:
        act = np.array(_active(a, day))
        w = np.zeros(len(a))
        for c in ww:
            m = (a["range"].values == c) & act
            pw = a["pop"].values[m] ** 0.8
            w[m] = pw / pw.sum() * ww[c] * (P.SUN_SEASON[day.month] if c == "SUN" else 1.0)
        w = w / w.sum()
        base = {0: 380, 1: 335, 2: 330, 3: 320, 4: 300, 5: 215}[day.weekday()] * P.WEB_SEASON[day.month]
        n_orders = int(r.poisson(base))
        n_lines = 1 + r.poisson(0.85, n_orders)
        n_lines = np.minimum(n_lines, 6)
        tot = int(n_lines.sum())
        arts = r.choice(len(a), tot, p=w)
        qty = r.choice(vals, tot, p=pr)
        gaps = r.integers(1, 4, n_orders)
        onos = order_no + np.cumsum(gaps)
        order_no = int(onos[-1])
        o = np.repeat(onos, n_lines)
        ln = np.concatenate([np.arange(1, k + 1) for k in n_lines])
        part = pd.DataFrame({"order_no": o, "line_no": ln, "art": arts, "qty": qty})
        part = part.drop_duplicates(["order_no", "art"]).copy()
        part["line_no"] = part.groupby("order_no").cumcount() + 1
        part["day"] = day
        rows.append(part)
    df = pd.concat(rows, ignore_index=True)
    df["channel"] = "W"
    df["group"] = None
    df["store_no"] = None
    return df[["order_no", "line_no", "day", "channel", "group", "store_no", "art", "qty"]]


def pickers(trade_days, web_days):
    """The people who picked: permanent staff and agency pickers, each with a badge, an area and a first day."""
    r = rng("pickers")
    people = []
    badge = 10213
    for area, perm, agency_waves in (("T", 13, 30), ("W", 16, 38)):
        for _ in range(perm):
            badge += int(r.integers(3, 40))
            start = dt.date(2019, 1, 1) + dt.timedelta(days=int(r.integers(0, 2000)))
            people.append(dict(badge=badge, area=area, agency=None, first=start, last=None))
        for _ in range(agency_waves):
            badge += int(r.integers(3, 40))
            start = dt.date(2025, 9, 1) + dt.timedelta(days=int(r.integers(0, 470)))
            length = int(r.integers(35, 260))
            last = start + dt.timedelta(days=length)
            people.append(dict(badge=badge, area=area, agency=str(r.choice(["Flexpoint", "Maasland Uitzend", "Werkhuys"])),
                               first=start, last=last))
    return pd.DataFrame(people)


def assign_pickers(lines, ppl, trade_days, web_days):
    r = rng("assign")
    lines = lines.sort_values(["day", "channel", "order_no", "line_no"]).reset_index(drop=True)
    badge = np.zeros(len(lines), int)
    by_day = lines.groupby(["day", "channel"]).indices
    days_worked = {}
    for (day, ch), idx in sorted(by_day.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        pool = ppl[(ppl["area"] == ch) & (ppl["first"] <= day) & (ppl["last"].isna() | (ppl["last"] >= day))]
        b = pool["badge"].values
        if ch == "T":
            orders = lines.loc[idx, "order_no"].values
            uo = np.unique(orders)
            pick = dict(zip(uo, r.choice(b, len(uo))))
            badge[idx] = [pick[o] for o in orders]
        else:
            badge[idx] = r.choice(b, len(idx))
    lines["badge"] = badge
    # tenure: working days on the floor since the person's first pick (people who started before 2026 are never new)
    first = ppl.set_index("badge")["first"].to_dict()
    lines["first_day"] = lines["badge"].map(first)
    worked = lines.groupby(["badge", "day"]).size().reset_index()[["badge", "day"]]
    worked = worked.sort_values(["badge", "day"])
    worked["n"] = worked.groupby("badge").cumcount() + 1
    pre = worked["badge"].map(lambda b: first[b] < dt.date(2026, 1, 1))
    worked["new"] = (~pre) & (worked["n"] <= P.NEW_DAYS)
    lines = lines.merge(worked[["badge", "day", "new"]], on=["badge", "day"], how="left")
    return lines.drop(columns=["first_day"])


def structure(qty, inner):
    qty = np.asarray(qty)
    inner = np.asarray(inner)
    return np.where(qty % inner == 0, "whole", np.where(qty < inner, "loose", "mixed"))


def short_picks(lines):
    """Stock-outs: a few lines confirmed below the quantity ordered, some at zero."""
    r = rng("short")
    conf = lines["qty"].values.copy()
    u = r.random(len(lines))
    zero = u < 0.004
    part = (u >= 0.004) & (u < 0.010) & (conf > 1)
    conf[zero] = 0
    cut = np.maximum(1, (conf[part] * r.uniform(0.3, 0.9, part.sum())).astype(int))
    conf[part] = np.minimum(cut, conf[part] - 1)
    lines["qty_conf"] = conf
    return lines


def failures(lines, a):
    """Which picked lines fail pack-out verification: each line's chance is the error probability of the pick it calls
    for, raised for a picker's first working days; the count in every cell is its expected value, so the realised rate
    of each kind of pick in each channel is the rate the process runs at."""
    r = rng("fail")
    inner = a["inner"].values[lines["art"].values]
    lines["inner"] = inner
    lines["struct"] = structure(np.maximum(lines["qty_conf"].values, 1), inner)
    picked = lines["qty_conf"].values > 0
    p = np.array([P.HEP[s] for s in lines["struct"]]) * np.where(lines["new"].values, P.NEW_PICKER_FACTOR, 1.0)
    p = np.where(picked, p, 0.0)
    lines["p"] = p
    lines["month"] = [d.month for d in lines["day"]]
    lines["range"] = a["range"].values[lines["art"].values]
    fail = np.zeros(len(lines), bool)
    for (ch, rg, s), g in lines[picked].groupby(["channel", "range", "struct"]):
        cells = g.groupby(["month", "new"])
        exp = cells["p"].sum()
        total = int(round(exp.sum()))
        # each channel's and range's year total for this kind of pick is its expected count; the months share it as
        # chance does
        base = r.multinomial(total, exp.values / exp.values.sum())
        for (key, idx), n in zip(cells.indices.items(), base):
            rows = g.index.values[idx]
            if n > 0:
                fail[r.choice(rows, n, replace=False)] = True
    lines["fail"] = fail
    return lines


def times(lines):
    """Pick timestamps in Venlo local time: trade orders one picker after another through the shift, webshop lines
    through the day."""
    r = rng("times")
    ts = np.empty(len(lines), dtype="datetime64[s]")
    for (day, ch), idx in lines.groupby(["day", "channel"]).indices.items():
        base = np.datetime64(day, "s")
        n = len(idx)
        if ch == "T":
            sec = np.sort(r.integers(6 * 3600 + 900, 22 * 3600 + 1800, n))
        else:
            sec = np.sort(r.integers(6 * 3600 + 300, 22 * 3600 + 2700, n))
        ts[idx] = base + sec.astype("timedelta64[s]")
    lines["ts_local"] = ts
    return lines


def splits(lines):
    """Lines the picker completed in two goes (the face ran short and the rest came from a second location)."""
    r = rng("splits")
    m = (lines["qty_conf"].values >= 2) & (r.random(len(lines)) < 0.03)
    lines["split"] = m
    return lines


def deliveries(lines):
    """Store deliveries: one delivery note per trade order, dispatched the evening of the pick and delivered the next
    working day; lines travel in roll cages of about fourteen lines, each with its own SSCC."""
    r = rng("deliv")
    t = lines[lines["channel"] == "T"]
    orders = t.groupby("order_no").agg(day=("day", "first"), group=("group", "first"), store_no=("store_no", "first"),
                                       n=("line_no", "size")).reset_index()
    note = 7700418 + np.cumsum(r.integers(1, 6, len(orders)))
    orders["delivery_note"] = ["KV%d" % x for x in note]
    po = {}
    pos = []
    for g, s in zip(orders["group"], orders["store_no"]):
        po[(g, s)] = po.get((g, s), int(r.integers(10000, 60000))) + int(r.integers(1, 4))
        pos.append("%04d-%06d" % (s, po[(g, s)]) if g == "HGH" else "")
    orders["store_po"] = pos

    def nxt(d):
        d = d + dt.timedelta(days=1)
        while d.weekday() >= 5 or d in P.HOLIDAYS or d == dt.date(2026, 12, 28) and False:
            d = d + dt.timedelta(days=1)
        return d
    orders["delivery_date"] = [nxt(d) for d in orders["day"]]
    orders["dispatch_min"] = np.where(r.random(len(orders)) < 0.006, r.integers(23 * 60 + 2, 23 * 60 + 40, len(orders)),
                                      r.integers(18 * 60 + 40, 22 * 60 + 50, len(orders)))
    # cages
    cage_rows = []
    serial = 412500000
    for o in orders.itertuples():
        ncage = max(1, int(np.ceil(o.n / 14.0)))
        ids = []
        for _ in range(ncage):
            serial += int(r.integers(1, 7))
            ids.append(gs1_check("3" + "8714593" + "%09d" % serial))
        cage_rows.append(ids)
    orders["cages"] = cage_rows
    return orders


def colli(lines, orders):
    t = lines[(lines["channel"] == "T") & (lines["qty_conf"] > 0)].copy()
    cmap = orders.set_index("order_no")["cages"].to_dict()
    sscc = []
    for o, ln, n in zip(t["order_no"], t["line_no"], t.groupby("order_no")["line_no"].transform("size")):
        cs = cmap[o]
        k = min(int((ln - 1) * len(cs) / max(n, 1)), len(cs) - 1)
        sscc.append(cs[k])
    t["sscc"] = sscc
    return t[["order_no", "line_no", "sscc", "qty_conf", "art"]]


def _bday(d, n, r):
    """A store's claim arrives n working days (Monday to Saturday) after the delivery."""
    k = 0
    while k < n:
        d = d + dt.timedelta(days=1)
        if d.weekday() < 6 and d not in P.HOLIDAYS:
            k += 1
    return d


REASONS = (["Tekort", "Teveel", "Verkeerd artikel", "Beschadigd", "THT"], [.70, .08, .10, .09, .03])


def claims(lines, orders, col, a):
    """The stores' claims on 2026 deliveries as Siersma's customer service registered them, one event per claimed line
    (or per missing cage), with the units each claims; and the register rows those events left: a store's EDI message,
    or a portal entry whose quantity field counted store packs until the portal release and units after it."""
    r = rng("claims")
    t = lines[(lines["channel"] == "T") & (lines["qty_conf"] > 0)].copy()
    t = t.merge(orders[["order_no", "delivery_note", "store_po", "delivery_date"]], on="order_no")
    t = t.merge(col[["order_no", "line_no", "sscc"]], on=["order_no", "line_no"])
    t["quarter"] = [(d.month - 1) // 3 + 1 for d in t["delivery_date"]]
    t["store_pack"] = a["store_pack"].values[t["art"].values]
    events = []
    # missing cages: every customer in every quarter of delivery loses one to three
    cage_lines = set()
    for (g, q), sub in t[t["delivery_date"] < dt.date(2026, 12, 24)].groupby(["group", "quarter"]):
        cages = sorted(sub["sscc"].unique())
        n = max(1, min(3, int(r.poisson(1.7))))
        for c in r.choice(cages, n, replace=False):
            cl = sub[sub["sscc"] == c]
            o = cl.iloc[0]
            events.append(dict(kind="cage", group=g, store_no=o["store_no"], delivery_note=o["delivery_note"],
                               store_po=o["store_po"], delivery_date=o["delivery_date"], sscc=c, art=-1,
                               reason="Tekort", units=int(cl["qty_conf"].sum()), store_pack=0))
            cage_lines.update(zip(cl["order_no"], cl["line_no"]))
    keep = np.array([(o, l) not in cage_lines for o, l in zip(t["order_no"], t["line_no"])])
    pr = 0.0042 + 0.0045 * (t["struct"].values == "mixed")
    pick = keep & (r.random(len(t)) < pr)
    vals, w = REASONS
    for row in t[pick].itertuples():
        reason = str(r.choice(vals, p=w))
        m, q = int(row.store_pack), int(row.qty_conf)
        u = r.random()
        if reason == "Tekort":
            units = m if u < .6 else (min(2 * m, q) if u < .7 else int(r.integers(1, max(2, m))))
        elif reason == "Teveel":
            units = m if u < .7 else int(r.integers(1, max(2, m)))
        elif reason == "Verkeerd artikel":
            units = q if u < .6 else m
        elif reason == "Beschadigd":
            units = int(r.integers(1, 4))
        else:
            units = m
        events.append(dict(kind="line", group=row.group, store_no=row.store_no, delivery_note=row.delivery_note,
                           store_po=row.store_po, delivery_date=row.delivery_date, sscc="", art=int(row.art),
                           reason=reason, units=max(1, min(units, q if reason != "Teveel" else 10 * m)), store_pack=m,
                           order_no=row.order_no, line_no=row.line_no))
    ev = pd.DataFrame(events)
    ev["received"] = [_bday(d, int(n), r) for d, n in zip(ev["delivery_date"], r.choice([0, 1, 1, 2, 2, 3, 4, 6], len(ev)))]
    ev.loc[ev["kind"] == "cage", "received"] = [_bday(d, 1, r) for d in ev.loc[ev["kind"] == "cage", "delivery_date"]]
    route = {g: rt for g, _n, _s, rt, _ref in P.GROUPS}
    ev["route"] = [route[g] if (route[g] == "PORTAL" or r.random() > 0.10) else "PORTAL" for g in ev["group"]]
    ev.loc[ev["kind"] == "cage", "route"] = [route[g] for g in ev.loc[ev["kind"] == "cage", "group"]]
    # the portal was offline for its release; claims stores made that week were entered when it came back
    down = (ev["route"] == "PORTAL") & ev["received"].between(*P.PORTAL_DOWN)
    ev.loc[down, "received"] = P.PORTAL_RELEASE
    # a portal entry made before the release could only count whole store packs
    before = (ev["route"] == "PORTAL") & (ev["received"] < P.PORTAL_RELEASE) & (ev["kind"] == "line")
    ev.loc[before, "units"] = [m * max(1, int(round(u / m))) for u, m in zip(ev.loc[before, "units"], ev.loc[before, "store_pack"])]
    st = r.random(len(ev))
    ev["status"] = np.where(st < 0.885, "Geaccepteerd", "Afgewezen")
    ev.loc[ev["kind"] == "cage", "status"] = "Geaccepteerd"
    late = ev["received"] >= dt.date(2026, 12, 23)
    ev.loc[late & (st > 0.80), "status"] = "In behandeling"
    ev = ev[ev["received"] <= P.EXPORT_DATE].reset_index(drop=True)
    ev["event"] = np.arange(len(ev))
    # register rows: the event's own row, plus a portal copy for some EDI claims a store also phoned in
    rows = []
    art_no = a["article_no"].values
    eans = a["ean"].values
    for e in ev.itertuples():
        rows.append(_row(e, e.route, e.received, art_no, eans))
        if e.route == "EDI" and e.kind == "line" and e.units % e.store_pack == 0 and r.random() < 0.16:
            got = _bday(e.received, int(r.integers(1, 4)), r)
            if P.PORTAL_DOWN[0] <= got <= P.PORTAL_DOWN[1]:
                got = P.PORTAL_RELEASE
            rows.append(_row(e, "PORTAL", got, art_no, eans, copy=True))
    reg = pd.DataFrame(rows)
    reg = reg[reg["received"] <= P.EXPORT_DATE]
    # claims on the deliveries Siersma's own warehouse at Hoogeveen made to Vlietmarkt stores (not Kroonvaart's)
    vlm = sorted(t.loc[t["group"] == "VLM", "store_no"].unique())
    extra = []
    for k in range(41):
        d = dt.date(2026, 1, 5) + dt.timedelta(days=int(r.integers(0, 355)))
        while d.weekday() >= 6:
            d += dt.timedelta(days=1)
        i = int(r.choice(np.where(a["range"].values != "SUN")[0]))
        m = int(a["store_pack"].iat[i])
        units = m * int(r.integers(1, 3))
        if P.PORTAL_DOWN[0] <= d <= P.PORTAL_DOWN[1]:
            d = P.PORTAL_RELEASE
        extra.append(dict(event=-1, route="PORTAL", group="VLM", store_no=int(r.choice(vlm)), received=d,
                          reference="HV%06d" % int(r.integers(310000, 389999)), sscc="", article=str(art_no[i]),
                          qty=units // m if d < P.PORTAL_DOWN[0] else units, reason=str(r.choice(["Tekort", "Beschadigd"], p=[.7, .3])),
                          status="Geaccepteerd" if r.random() < 0.9 else "Afgewezen", copy=False))
    reg = pd.concat([reg, pd.DataFrame(extra)], ignore_index=True)
    reg = reg.sort_values(["received", "route", "store_no", "reference", "article"], kind="stable").reset_index(drop=True)
    no = 4100 + np.cumsum(r.integers(1, 4, len(reg)))
    reg["claim_no"] = ["CL-26-%06d" % x for x in no]
    return ev, reg


def _row(e, route, received, art_no, eans, copy=False):
    if e.kind == "cage":
        article, qty = "", 1
    elif route == "EDI":
        article, qty = str(eans[e.art]), int(e.units)
    else:
        article = str(art_no[e.art])
        qty = int(e.units) // int(e.store_pack) if received < P.PORTAL_RELEASE else int(e.units)
    if route == "EDI" and e.group == "HGH":
        ref = e.store_po
    else:
        ref = e.delivery_note
    return dict(event=e.event, route=route, group=e.group, store_no=e.store_no, received=received, reference=ref,
                sscc=e.sscc, article=article, qty=qty, reason=e.reason, status=e.status, copy=copy)


def plan(lines):
    """The client's plan for the first quarter of 2027: order lines per range and channel, each month the same
    month of 2026 grown by the channel's plan growth, in tens."""
    a_range = lines["range"].values
    rows = []
    picked = lines[lines["qty_conf"] > 0]
    for m in (1, 2, 3):
        g = picked[picked["month"] == m].groupby(["channel", "range"]).size()
        for (ch, rg), n in g.items():
            rows.append(dict(month=m, channel=ch, range=rg, lines=int(round(n * P.PLAN_GROWTH[ch] / 10.0) * 10)))
    return pd.DataFrame(rows)


def build():
    a = articles()
    st = stores()
    trade_days, web_days = calendar()
    t = trade_orders(a, st, trade_days)
    w = web_orders(a, web_days)
    lines = pd.concat([t, w], ignore_index=True)
    ppl = pickers(trade_days, web_days)
    lines = assign_pickers(lines, ppl, trade_days, web_days)
    lines["range"] = a["range"].values[lines["art"].values]
    lines = short_picks(lines)
    lines = failures(lines, a)
    lines = times(lines)
    lines = splits(lines)
    orders = deliveries(lines)
    col = colli(lines, orders)
    pl = plan(lines)
    ev, reg = claims(lines, orders, col, a)
    return dict(articles=a, stores=st, lines=lines, people=ppl, orders=orders, colli=col, plan=pl, events=ev, register=reg,
                trade_days=trade_days, web_days=web_days)


if __name__ == "__main__":
    import time
    t0 = time.time()
    W = build()
    L = W["lines"]
    pk = L[L["qty_conf"] > 0]
    print("lines", len(L), "picked", len(pk), "trade", (pk.channel == "T").sum(), "web", (pk.channel == "W").sum())
    print("fail rate %", round(100 * pk["fail"].mean(), 4), "accuracy", round(100 - 100 * pk["fail"].mean(), 3))
    print(pk.groupby("struct")["fail"].agg(["mean", "size"]))
    print(pk.groupby(["channel", "struct"])["fail"].agg(["mean", "size"]))
    print(pk.groupby("month")["fail"].mean().mul(100).round(3).to_dict())
    print("new share", pk["new"].mean())
    print(W["plan"].pivot_table(index=["channel", "range"], columns="month", values="lines"))
    print("secs", round(time.time() - t0, 1))
