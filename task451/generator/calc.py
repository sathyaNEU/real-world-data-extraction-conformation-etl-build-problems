"""The golden and every wrong reading, computed on transaction rows in one shape whether they come from the simulated
world (rows_from_world) or from the shipped files (reader.load). A row is one IATI transaction with its activity's
fields beside it."""
import collections
import datetime as dt

import world as W

D = dt.date
GREF, SREF = W.FUNDS["G"]["ref"], W.FUNDS["S"]["ref"]


# ---------------------------------------------------------------------------------------------- rows
def _row(a, t, source):
    return dict(aid=a["id"], rep=a["reporting"], hierarchy=a.get("hierarchy"), parent=a.get("parent"),
                countries=list(a["countries"]), funding=list(a["funding"]), implementing=list(a["implementing"]),
                dccy=a["ccy"], other_ids=list(a["other_ids"]), title=a["title"], updated=a["updated"],
                ttype=t["type"], tdate=t["date"], value=float(t["value"]),
                ccy=None if a.get("omit_ccy") else t["ccy"], vdate=t["value_date"],
                prov_ref=(t["provider"] or (None, None, None))[0], prov_name=(t["provider"] or (None, None, None))[1],
                prov_act=(t["provider"] or (None, None, None))[2], recv_ref=(t["receiver"] or (None, None, None))[0],
                recv_name=(t["receiver"] or (None, None, None))[1], recv_act=(t["receiver"] or (None, None, None))[2],
                tcountry=t["country"], desc=t["desc"], source=source)


def rows_from_world(w):
    rows = []
    for k in ("member_acts", "fund_acts", "old", "other_acts"):
        for a in w[k]:
            for t in a["tx"]:
                rows.append(_row(a, t, "datastore"))
    for a in w["fund_acts"]:
        for t in a["tx"]:
            rows.append(_row(a, t, "xml"))
    for a in (w["gfund"], w["sfund"]):
        for t in a["tx"]:
            rows.append(_row(a, t, "xml"))
    return rows


def dedup(rows):
    """One copy of each transaction: the funds' grant activities sit in their own files and in the Datastore."""
    seen, out = set(), []
    for r in rows:
        k = (r["aid"], r["ttype"], r["tdate"], round(r["value"], 2), r["vdate"], r["prov_ref"], r["recv_ref"], r["recv_act"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def usd(r, fx):
    ccy = r["ccy"] or r["dccy"]
    d = r["vdate"] or r["tdate"]
    return r["value"] / fx[ccy][d]


def countries_of(r):
    if r["tcountry"]:
        return [(r["tcountry"], 100.0)]
    return [(c, float(p)) for c, p in r["countries"]]


def member_refs(register):
    """Every identifier a member has published under: the register's current and previous identifiers."""
    refs = set()
    for m in register:
        refs.add(m["ref"])
        if m.get("prev"):
            refs.add(m["prev"])
    return refs


# ---------------------------------------------------------------------------------------------- the funds' money
def fund_flows(rows, fx):
    """Each fund's receipts and payments in date order, in US dollars: receipts on its pooled activity, payments
    on the pooled activity (the transfer between the funds) and on its grant activities."""
    out = {}
    for fref in (GREF, SREF):
        rec = [r for r in rows if r["rep"] == fref and r["ttype"] == "1" and r["hierarchy"] == "1"]
        pay = [r for r in rows if r["rep"] == fref and r["ttype"] == "3"]
        out[fref] = (sorted(rec, key=lambda r: (r["tdate"], r["prov_ref"] or "")),
                     sorted(pay, key=lambda r: (r["tdate"], r["recv_act"] or "", r["aid"])))
    return out


def held_when_paid(rows, fx, mrefs, method="pro_rata"):
    """The members' share of each payment the two funds made, from the money each fund held when it paid. The global
    fund first; a receipt from the global fund carries the members' share of the global fund's payment.
    method: pro_rata (every payment draws on the balance in proportion), fifo (the oldest money first) or lifo
    (the newest money first). Returns {(fund ref, payment row id): member share}."""
    flows = fund_flows(rows, fx)
    pay_share = {}
    g_payment_share = {}
    for fref in (GREF, SREF):
        rec, pay = flows[fref]
        events = [(r["tdate"], 0, r) for r in rec] + [(r["tdate"], 1, r) for r in pay]
        events.sort(key=lambda e: (e[0], e[1]))
        lots = []                                # [amount, member amount, day]: a day's receipts are one addition
        for d, kind, r in events:
            amt = usd(r, fx)
            if kind == 0:
                if r["prov_ref"] in mrefs:
                    msh = 1.0
                elif r["prov_ref"] == GREF:
                    msh = g_payment_share[(r["tdate"] - dt.timedelta(2), round(amt, 2))] if (r["tdate"] - dt.timedelta(2), round(amt, 2)) in g_payment_share else \
                        [v for (dd, a), v in g_payment_share.items() if abs(a - round(amt, 2)) < 0.01 and dd <= r["tdate"]][-1]
                else:
                    msh = 0.0
                if lots and lots[-1][2] == r["tdate"]:
                    lots[-1][0] += amt
                    lots[-1][1] += amt * msh
                else:
                    lots.append([amt, amt * msh, r["tdate"]])
            else:
                total = sum(l[0] for l in lots)
                need = amt
                taken_m = 0.0
                if method == "pro_rata":
                    frac = need / total
                    for l in lots:
                        taken_m += l[1] * frac
                        l[0] -= l[0] * frac
                        l[1] -= l[1] * frac
                else:
                    order = lots if method == "fifo" else list(reversed(lots))
                    for l in order:
                        if need <= 1e-9:
                            break
                        take = min(need, l[0])
                        if l[0] > 0:
                            taken_m += l[1] * take / l[0]
                            l[1] -= l[1] * take / l[0]
                        l[0] -= take
                        need -= take
                    lots = [l for l in lots if l[0] > 1e-6]
                share = taken_m / amt
                pay_share[(fref, r["aid"], r["tdate"], round(r["value"], 2))] = share
                if fref == GREF:
                    g_payment_share[(r["tdate"], round(amt, 2))] = share
    return pay_share


def fund_shares_simple(rows, fx, mrefs, years_g, rounds_s, rec=True, g_override=None):
    """A single members' share per fund from contributions in given years (the wrong readings): the global fund's
    share from its receipts dated in years_g; the Sahel fund's from its receipts dated in rounds_s, the global fund's
    part at the global fund's share (rec) or as nobody's (not rec)."""
    flows = fund_flows(rows, fx)
    rec_g, _ = flows[GREF]
    gm = sum(usd(r, fx) for r in rec_g if r["tdate"].year in years_g and r["prov_ref"] in mrefs)
    gt = sum(usd(r, fx) for r in rec_g if r["tdate"].year in years_g)
    sg = gm / gt if g_override is None else g_override
    rec_s, _ = flows[SREF]
    sm = sum(usd(r, fx) for r in rec_s if r["tdate"].year in rounds_s and r["prov_ref"] in mrefs)
    sgp = sum(usd(r, fx) for r in rec_s if r["tdate"].year in rounds_s and r["prov_ref"] == GREF)
    st = sum(usd(r, fx) for r in rec_s if r["tdate"].year in rounds_s)
    ss = (sm + (sgp * sg if rec else 0.0)) / st
    return sg, ss


# ---------------------------------------------------------------------------------------------- the call
def activity_shares(rows, fx, mrefs, fund_share=None, pay_share=None):
    """Members' share of each spending activity's money: a member's activity in full; an activity a fund paid, at the
    fund's share (fund_share: {fund ref: share}) or at the members' share of the fund's payments to it (pay_share)."""
    acts = {}
    for r in rows:
        if r["aid"] not in acts:
            acts[r["aid"]] = r
    paid_to = collections.defaultdict(list)
    if pay_share is not None:
        for (fref, aid, d, v), sh in pay_share.items():
            pass
        for r in rows:
            if r["rep"] in (GREF, SREF) and r["ttype"] == "3" and r["recv_act"]:
                k = (r["rep"], r["aid"], r["tdate"], round(r["value"], 2))
                if k in pay_share:
                    paid_to[r["recv_act"]].append((r["value"], pay_share[k]))
    out = {}
    for aid, r in acts.items():
        if r["rep"] in (GREF, SREF):
            continue
        f = r["funding"][0] if r["funding"] else None
        if f in mrefs:
            out[aid] = 1.0
        elif f in (GREF, SREF):
            if pay_share is not None:
                lst = paid_to.get(aid, [])
                out[aid] = sum(v * s for v, s in lst) / sum(v for v, _ in lst) if lst else 0.0
            else:
                out[aid] = fund_share[f]
        else:
            out[aid] = 0.0
    return out


def spending_by_country(rows, fx, shares, year=W.YEAR, which="exp"):
    """The members' money spent in each country: expenditure in the year by the organisation that spent it, at the
    members' share of the spending activity's money; which="pay" totals the members' own payments instead."""
    tot = collections.defaultdict(float)
    for r in rows:
        if r["tdate"].year != year:
            continue
        if which == "exp":
            if r["ttype"] != "4" or r["rep"] in (GREF, SREF):
                continue
            sh = shares.get(r["aid"], 0.0)
        else:
            if r["ttype"] != "3" or r["rep"] not in shares:
                continue
            sh = 1.0
        if not sh:
            continue
        v = usd(r, fx) * sh
        for iso, pct in countries_of(r):
            tot[W.NAME_OF[iso]] += v * pct / 100.0
    return {c: tot.get(c, 0.0) / 1e6 for c in W.NAMES}


def top3(vals):
    o = sorted(vals, key=lambda c: -vals[c])
    return o[:3], vals[o[2]] / vals[o[3]]


def readings(rows, fx, register):
    """Every reading of the call: name -> (country totals, global fund share, Sahel fund share)."""
    rows = dedup(rows)
    mrefs = member_refs(register)
    out = {}
    ps = held_when_paid(rows, fx, mrefs, "pro_rata")
    sh = activity_shares(rows, fx, mrefs, pay_share=ps)
    gold = spending_by_country(rows, fx, sh)
    g_share = _mean_share(ps, GREF, 2025)
    s_share = _mean_share(ps, SREF, 2025)
    out["golden"] = (gold, g_share, s_share)
    for nm, gy, sy, rec in (("same_year", [2025], [2025], True), ("same_year_one", [2025], [2025], False),
                            ("lifetime", [2023, 2024, 2025], [2024, 2025, 2026], True),
                            ("lifetime_one", [2023, 2024, 2025], [2024, 2025, 2026], False),
                            ("prior_year", [2024], [2024], True), ("golden_one", [2024], [2025], False)):
        g, s = fund_shares_simple(rows, fx, mrefs, gy, sy, rec)
        if nm == "prior_year":
            g2, _ = fund_shares_simple(rows, fx, mrefs, [2023], [2024], True)
            _, s = fund_shares_simple(rows, fx, mrefs, [2023], [2024], True)
        sh2 = activity_shares(rows, fx, mrefs, fund_share={GREF: g, SREF: s})
        out[nm] = (spending_by_country(rows, fx, sh2), g, s)
    # receipts before each payment: a fund's share at a payment is that of every receipt dated before it
    g, s = _cum_before(rows, fx, mrefs)
    out["cum_before_pay"] = (spending_by_country(rows, fx, activity_shares(rows, fx, mrefs, fund_share={GREF: g, SREF: s})), g, s)
    for nm, g, s in (("over", 1.0, 1.0), ("none", 0.0, 0.0)):
        out[nm] = (spending_by_country(rows, fx, activity_shares(rows, fx, mrefs, fund_share={GREF: g, SREF: s})), g, s)
    g, _ = fund_shares_simple(rows, fx, mrefs, [2024], [2025])
    s_full = fund_shares_simple(rows, fx, mrefs, [2024], [2025], True, g_override=1.0)[1]
    out["s_full"] = (spending_by_country(rows, fx, activity_shares(rows, fx, mrefs, fund_share={GREF: g_share, SREF: s_full})), g_share, s_full)
    gm = sum(fund_shares_simple(rows, fx, mrefs, [y], [2025])[0] for y in (2023, 2024, 2025)) / 3
    sm = (fund_shares_simple(rows, fx, mrefs, [2023], [2024], True)[1] + fund_shares_simple(rows, fx, mrefs, [2025], [2025], True, g_override=gm)[1]) / 2
    out["mean_annual"] = (spending_by_country(rows, fx, activity_shares(rows, fx, mrefs, fund_share={GREF: gm, SREF: sm})), gm, sm)
    # the donor view: the members' own 2025 payments by the country on them
    pays = {r["rep"]: 1.0 for r in rows if r["rep"] in mrefs}
    out["pay"] = (spending_by_country(rows, fx, pays, which="pay"), 0.0, 0.0)
    return out


def _mean_share(ps, fref, year):
    num = den = 0.0
    for (f, aid, d, v), s in ps.items():
        if f == fref and d.year == year and aid != f + "-POOL":
            num += v * s
            den += v
    return num / den


def _cum_before(rows, fx, mrefs):
    flows = fund_flows(rows, fx)
    rec_g, pay_g = flows[GREF]
    def share_before(rec, d, gsh_of=None):
        m = t = 0.0
        for r in rec:
            if r["tdate"] >= d:
                continue
            a = usd(r, fx)
            t += a
            if r["prov_ref"] in mrefs:
                m += a
            elif r["prov_ref"] == GREF and gsh_of is not None:
                m += a * gsh_of(r["tdate"])
        return m / t
    p25 = [r for r in pay_g if r["tdate"].year == 2025 and r["aid"] != GREF + "-POOL"]
    g = sum(usd(r, fx) * share_before(rec_g, r["tdate"]) for r in p25) / sum(usd(r, fx) for r in p25)
    rec_s, pay_s = flows[SREF]
    p25s = [r for r in pay_s if r["tdate"].year == 2025]
    s = sum(usd(r, fx) * share_before(rec_s, r["tdate"], lambda d: share_before(rec_g, d)) for r in p25s) / sum(usd(r, fx) for r in p25s)
    return g, s


# ---------------------------------------------------------------------------------------------- the asks
def superseded(rows):
    """Activities another activity names as its previous activity identifier: a publication replaced by a later one."""
    return {ref for r in rows for ref, t in r["other_ids"] if t == "A3"}


def ask_pipeline(rows, fx, register, on=W.PIPELINE_DATE, drop_superseded=True):
    """For each country, the members' commitments to activities there not yet paid at `on`, every amount at that
    day's rate: commitments minus disbursements dated on or before it, activity by activity."""
    rows = dedup(rows)
    mrefs = member_refs(register)
    old = superseded(rows) if drop_superseded else set()
    bal = collections.defaultdict(float)
    acts = {}
    for r in rows:
        if r["rep"] not in mrefs or r["aid"] in old or r["tdate"] > on:
            continue
        if r["ttype"] not in ("2", "3"):
            continue
        if r["recv_ref"] in (GREF, SREF) or not r["countries"]:
            continue
        v = r["value"] / fx[r["ccy"] or r["dccy"]][on]
        bal[r["aid"]] += v if r["ttype"] == "2" else -v
        acts[r["aid"]] = r
    tot = collections.defaultdict(float)
    for aid, b in bal.items():
        for iso, pct in countries_of(acts[aid]):
            tot[W.NAME_OF[iso]] += b * pct / 100.0
    return {c: tot.get(c, 0.0) / 1e6 for c in W.NAMES}


def org_resolver(registry):
    """Union of identifiers that name one organisation: each publisher's identifier with its other identifiers."""
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p in registry:
        for o in p["other"]:
            parent[find(o)] = find(p["ref"])
        find(p["ref"])
    return find


def ask_orgs(rows, register, registry, year=W.YEAR, resolve=True):
    """For each country, how many organisations the members paid directly for work there in the year: the members'
    disbursements on their activities in the country, receivers resolved to organisations through the publisher list."""
    rows = dedup(rows)
    mrefs = member_refs(register)
    find = org_resolver(registry) if resolve else (lambda x: x)
    seen = collections.defaultdict(set)
    for r in rows:
        if r["rep"] not in mrefs or r["ttype"] != "3" or r["tdate"].year != year:
            continue
        if r["recv_ref"] in (GREF, SREF) or not r["countries"]:
            continue
        for iso, _ in countries_of(r):
            seen[W.NAME_OF[iso]].add(find(r["recv_ref"]))
    return {c: len(seen.get(c, ())) for c in W.NAMES}
