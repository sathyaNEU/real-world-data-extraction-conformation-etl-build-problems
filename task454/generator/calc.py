"""The golden's construction and every rung, route and ask computed on the generator's clean truth."""
from collections import defaultdict
from world import *

Q = {m: (m - 1) // 3 + 1 for m in range(1, 13)}


def routine_pair(months, days, min_months=6, min_days=30):
    return months >= min_months and days >= min_days


def routine(c, r, min_months=6, min_days=30):
    """A region is part of a card holder's usual environment when the card is there routinely: in many months and on
    many days of the year. Any threshold inside the gap the data leave gives the same classes (asserted in checks)."""
    return routine_pair(len(c.months_in(r)), c.days_in(r), min_months, min_days)


def spend_by(cards, weight, is_visitor):
    q = {r: [0.0, 0.0, 0.0, 0.0] for r in ELIGIBLE}
    for c in cards:
        w = weight[c.stratum]
        for (r, m), v in c.rows.items():
            if r in q and is_visitor(c, r, m):
                q[r][Q[m] - 1] += w * v[0]
    return q


def per_resident(q, rpop):
    return {r: sum(q[r]) / rpop[r] for r in q}


def ranking(pr):
    order = sorted(pr, key=lambda r: (-pr[r], ERP26[r]))
    return order


def summary(q, rpop):
    pr = per_resident(q, rpop)
    o = ranking(pr)
    return {"per_resident": pr, "order": o, "set": o[:N_FUNDED], "fifth": o[N_FUNDED - 1], "sixth": o[N_FUNDED],
            "margin": pr[o[N_FUNDED - 1]] / pr[o[N_FUNDED]], "gap": pr[o[N_FUNDED - 1]] - pr[o[N_FUNDED]], "q": q}


def golden(cards, weight, rpop, mm=6, md=30):
    return summary(spend_by(cards, weight, lambda c, r, m: not routine(c, r, mm, md)), rpop)


def statement_region(sa2, sa2_region, shared_split):
    """The region a statement SA2 lies in (shared SA2s: the region holding the larger share)."""
    if sa2 in shared_split:
        return max(shared_split[sa2], key=shared_split[sa2].get)
    return sa2_region.get(sa2, "IS")


def default(cards, weight, rpop, sa2_region, shared_split, by="month"):
    def home(c, m):
        if by == "stratum":
            return c.stratum
        sa2 = c.sa2_change[1] if (c.sa2_change and m >= c.sa2_change[0]) else c.sa2
        return statement_region(sa2, sa2_region, shared_split)
    return summary(spend_by(cards, weight, lambda c, r, m: home(c, m) != r), rpop)


def default_split(cards, weight, rpop, sa2_region, shared_split):
    """Statement-based with a shared statement SA2 split between its regions by the schedule's shares."""
    q = {r: [0.0, 0.0, 0.0, 0.0] for r in ELIGIBLE}
    for c in cards:
        w = weight[c.stratum]
        for (r, m), v in c.rows.items():
            if r not in q:
                continue
            sa2 = c.sa2_change[1] if (c.sa2_change and m >= c.sa2_change[0]) else c.sa2
            if sa2 in shared_split:
                local = shared_split[sa2].get(r, 0.0)
            else:
                local = 1.0 if sa2_region.get(sa2, "IS") == r else 0.0
            q[r][Q[m] - 1] += w * v[0] * (1 - local)
    return summary(q, rpop)


def adjacency(cards, weight, rpop, sa2_region, shared_split):
    adj = lambda a, b: (a, b) in ADJ or (b, a) in ADJ
    def vis(c, r, m):
        sa2 = c.sa2_change[1] if (c.sa2_change and m >= c.sa2_change[0]) else c.sa2
        h = statement_region(sa2, sa2_region, shared_split)
        return h != r and not (h in CODES and adj(h, r))
    return summary(spend_by(cards, weight, vis), rpop)


def modal_home(cards, weight, rpop):
    home = {}
    for c in cards:
        dd = defaultdict(int)
        for (r, m), v in c.rows.items():
            dd[r] += v[2]
        home[c.cid] = max(sorted(dd), key=lambda r: dd[r]) if dd else None
    return summary(spend_by(cards, weight, lambda c, r, m: home[c.cid] != r), rpop)


def asks(agreements, claims, payments, receipts):
    """Ask A: what remains of each region's open agreements at 31 December 2026 (approved less paid). Ask B: unspent
    money each region's councils returned in 2026. The round's total and each funded region's grant."""
    A = defaultdict(float); B = defaultdict(float)
    paid = defaultdict(float)
    for c in claims:
        if c["paid"]:
            paid[c["agreement"]] += c["approved_amt"]
    for a in agreements:
        if a["status"] == "Open":
            A[a["region"]] += a["approved"] - a["paid_before"] - paid[a["agreement"]]
    reg = {c[0]: c[1] for c in COUNCILS}
    for r in receipts:
        for kind, ref, amt in r["parts"]:
            if kind == "unspent":
                B[reg[r["payer"]]] += amt
    A = {r: round(A[r], 2) for r in ELIGIBLE}
    B = {r: round(B[r], 2) for r in ELIGIBLE}
    total = ROUND_BUDGET + sum(B.values()) - sum(A.values())
    return A, B, round(total, 2), round(total / N_FUNDED, 2)


def asks_cracker(agreements, claims, payments, receipts):
    """The careful solver's route on the clean truth: the 20 March repeats dropped as duplicates; each transfer paired
    to the claims it equals where one claim or one agreement's claims equal it, otherwise booked to the agreement it
    quotes; a receipt equal to a repeat paired off with it and every other receipt read as unspent money."""
    R = ask_routes(agreements, claims, payments, receipts)
    A, B = R["cracker"]
    total = ROUND_BUDGET + sum(B.values()) - sum(A.values())
    return A, B, round(total, 2), round(total / N_FUNDED, 2)


def ask_routes(agreements, claims, payments, receipts):
    """Every complete pipeline a careful solver could file for the two asks, on the clean truth: route -> (A, B)."""
    import datetime as dt
    reg = {c[0]: c[1] for c in COUNCILS}
    ag = {a["agreement"]: a for a in agreements}
    cl = {c["claim"]: c for c in claims}

    def remaining(paid):
        A = defaultdict(float)
        for a in agreements:
            if a["status"] == "Open":
                A[a["region"]] += a["approved"] - a["paid_before"] - paid[a["agreement"]]
        return {r: round(A[r], 2) for r in ELIGIBLE}

    live = [p for p in payments if not p.get("repeat_of")]
    # the transfer as booked: a single claim, or one agreement's claims, that it equals; else the agreement it quotes
    quoted = defaultdict(float)
    for p in live:
        cs = [cl[k] for k in p["claims"]]
        one = {c["agreement"] for c in cs}
        quoted[cs[0]["agreement"] if len(one) == 1 else p["ref"]] += p["amount"]
    # claims taken as paid: every 2026 claim; the claims a transfer equals one for one; claims approved four days or
    # more before the year's last run
    allc, matched, timing, split = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float)
    last = max(p["paid_on"] for p in live)
    for c in claims:
        allc[c["agreement"]] += c["approved_amt"]
        if c["approved_on"] <= last - dt.timedelta(days=4):
            timing[c["agreement"]] += c["approved_amt"]
        if c["paid"]:
            split[c["agreement"]] += c["approved_amt"]
    for p in live:
        if len(p["claims"]) == 1:
            matched[cl[p["claims"][0]]["agreement"]] += p["amount"]
    # receipts
    reps = defaultdict(list)
    for p in payments:
        if p.get("repeat_of"):
            reps[p["payee"]].append(round(p["amount"], 2))
    whole, paired, golden = defaultdict(float), defaultdict(float), defaultdict(float)
    for r in receipts:
        whole[reg[r["payer"]]] += r["amount"]
        if not (round(r["amount"], 2) in reps[r["payer"]] or abs(r["amount"] - sum(reps[r["payer"]])) < 0.005):
            paired[reg[r["payer"]]] += r["amount"]
        golden[reg[r["payer"]]] += sum(x for k, _, x in r["parts"] if k == "unspent")
    # the register's view: what an agreement closed under budget left unspent (paid less final cost)
    paid26 = defaultdict(float)
    for c in claims:
        if c["paid"]:
            paid26[c["agreement"]] += c["approved_amt"]
    rr_all, rr_2026 = defaultdict(float), defaultdict(float)
    for a in agreements:
        if a["status"] != "Open" and a["final_cost"] is not None:
            u = a["paid_before"] + paid26[a["agreement"]] - a["final_cost"]
            if u > 0.005:
                rr_all[a["region"]] += u
                if a["acquitted"].year == 2026:
                    rr_2026[a["region"]] += u
    fix = lambda d: {r: round(d[r], 2) for r in ELIGIBLE}
    return {"golden": (remaining(split), fix(golden)),
            "cracker": (remaining(quoted), fix(paired)),
            "every receipt": (remaining(quoted), fix(whole)),
            "claims all paid": (remaining(allc), fix(paired)),
            "claims a transfer equals": (remaining(matched), fix(paired)),
            "claims by payment timing": (remaining(timing), fix(paired)),
            "register, closed in 2026": (remaining(quoted), fix(rr_2026)),
            "register, every closure": (remaining(quoted), fix(rr_all))}
