"""The paths a solver can take on the credits and complaints asks, computed from the shipped files. Each path is a
complete, internally consistent pipeline; only the golden survives the pack's own rules."""
import datetime as dt
from collections import Counter, defaultdict

import golden as G

D = dt.date


def _accounts(Gd, q3):
    acc = Gd["accounts"]
    props = defaultdict(list)
    for k, v in acc.items():
        if v["bill_payer_account"]:
            props[v["bill_payer_account"]].append(k)
    hh = lambda a: acc[a]["merged_into"] or a
    fam, booked = {}, {}
    for f, a in q3.values():
        k = (hh(a["account_ref"]), a["appointment_date"])
        fam[k] = f
        booked.setdefault((a["account_ref"], a["appointment_date"]), k)
    return acc, props, hh, fam, booked


def credit_paths(Gd, q3, all_misses=None):
    acc, props, hh, fam, booked = _accounts(Gd, q3)
    reg = lambda h, day: bool(acc[h]["priority_register_from"]) and acc[h]["priority_register_from"] <= day
    grp = defaultdict(list)
    for c in Gd["credits"]:
        if c["reason_code"] == "MA" and "2026-07-01" <= c["visit_date"] <= "2026-09-30" and c["account_ref"] in acc:
            grp[(c["account_ref"], c["visit_date"])].append(c)

    def hits(acct, day):
        if acc[acct]["account_type"] == "Landlord":
            return sorted(p for p in props[acct] if (p, day) in fam)
        return [hh(acct)] if (hh(acct), day) in fam else []
    P = {k: Counter() for k in ("golden", "direct", "all_lines", "single_hit", "first_hit", "one_per_acct_day",
                                "first_line", "split", "policy", "runs_q3")}
    for (acct, day), ls in grp.items():
        hs = hits(acct, day)
        if not hs:
            continue
        amts = [int(float(c["amount_gbp"])) for c in ls]
        if len(ls) == len(hs) == 1:
            P["golden"][fam[(hs[0], day)]] += amts[0]
        else:
            pool = list(amts)
            for h in hs:
                r = 50 if reg(h, day) else 30
                pool.remove(r)
                P["golden"][fam[(h, day)]] += r
        for a in amts:
            for h in hs:
                P["all_lines"][fam[(h, day)]] += a
            P["first_hit"][fam[(hs[0], day)]] += a
            if len(hs) == 1:
                P["single_hit"][fam[(hs[0], day)]] += a
        lsr = sorted(ls, key=lambda c: c["credit_ref"])
        keep = int(float(lsr[0]["amount_gbp"]))
        P["one_per_acct_day"][fam[(hs[0], day)]] += keep
        for i, h in enumerate(hs):
            if i < len(lsr):
                P["first_line"][fam[(h, day)]] += int(float(lsr[i]["amount_gbp"]))
        for h in hs:
            P["split"][fam[(h, day)]] += keep / len(hs)
        if (acct, day) in booked:
            P["direct"][fam[booked[(acct, day)]]] += sum(amts)
    import accounts
    for (h, day), f in fam.items():
        run = accounts.run_date_for(D.fromisoformat(day)).isoformat()
        if acc[h]["cancelled_on"] and acc[h]["cancelled_on"] <= run:
            continue
        P["policy"][f] += 50 if reg(h, day) else 30
    # credits posted in the July, August and September runs: June to August visits
    if all_misses is not None:
        _, _, _, famx, _ = _accounts(Gd, all_misses)
        for c in Gd["credits"]:
            if c["reason_code"] != "MA" or not ("2026-07-01" <= c["credit_run_date"] <= "2026-09-30") \
                    or c["account_ref"] not in acc:
                continue
            day = c["visit_date"]
            if acc[c["account_ref"]]["account_type"] == "Landlord":
                hs = sorted(p for p in props[c["account_ref"]] if (p, day) in famx)
            else:
                hs = [hh(c["account_ref"])] if (hh(c["account_ref"]), day) in famx else []
            if hs:
                P["runs_q3"][famx[(hs[0], day)]] += int(float(c["amount_gbp"]))
    return P


def complaint_paths(Gd, q3):
    acc, props, hh, fam, booked = _accounts(Gd, q3)
    first = {}
    for c in Gd["complaints"]:
        r = c["complaint_ref"]
        if r not in first or c["received_at"] < first[r]["received_at"]:
            first[r] = c
    closed = {c["complaint_ref"] for c in Gd["complaints"] if c["status"] == "Closed"}
    canon, seen_k = {}, {}
    for r, c in sorted(first.items(), key=lambda x: (x[1]["received_at"], x[0])):
        canon[r] = seen_k.setdefault((c["account_ref"], c["received_at"], c["about_visit_date"]), r)
    res, direct = [], []
    for c in Gd["complaints"]:
        day = c["about_visit_date"]
        if not day or not ("2026-07-01" <= day <= "2026-09-30") or c["account_ref"] not in acc:
            continue
        a = acc[c["account_ref"]]
        if a["account_type"] == "Landlord":
            hs = [p for p in props[c["account_ref"]] if (p, day) in fam]
            if hs:
                res.append(((hs[0], day), c))
        elif (hh(c["account_ref"]), day) in fam:
            res.append(((hh(c["account_ref"]), day), c))
        if (c["account_ref"], day) in booked:
            direct.append((booked[(c["account_ref"], day)], c))
    lab = lambda c: c["category"] in G.MISSED
    moved = lambda c: first[c["complaint_ref"]]["status"] == "Reopened"
    units = {"refs": lambda c: c["complaint_ref"], "canon": lambda c: canon[c["complaint_ref"]],
             "acctvisit": lambda c: (c["account_ref"], c["about_visit_date"]), "hhday": lambda c: 0}

    def count(rows, keep, unit, drop_moved):
        out, seen = Counter(), defaultdict(set)
        for k, c in rows:
            if not keep(c) or (drop_moved and moved(c)):
                continue
            if unit == "rows":
                out[fam[k]] += 1
            else:
                seen[k].add(units[unit](c))
        for k, v in seen.items():
            out[fam[k]] += len(v)
        return out
    return {"golden": count(res, lab, "canon", True),
            "rows_direct": count(direct, lab, "rows", False),
            "refs_direct": count(direct, lab, "refs", False),
            "rows_resolved": count(res, lab, "rows", False),
            "refs_resolved": count(res, lab, "refs", False),
            "drop_reopened": count(res, lambda c: lab(c) and c["status"] != "Reopened", "refs", False),
            "dedup_copies": count(res, lab, "canon", False),
            "dedup_acct_visit": count(res, lab, "acctvisit", False),
            "closed_only": count(res, lambda c: lab(c) and c["complaint_ref"] in closed, "canon", True),
            "label_only": count(res, lambda c: c["category"] == "Missed appointment", "canon", True),
            "received_q3": count(res, lambda c: lab(c) and first[c["complaint_ref"]]["received_at"] <= "2026-09-30 23:59",
                                 "canon", True),
            "dedup_hhday": count(res, lab, "hhday", True),
            "any_category": count(res, lambda c: True, "canon", True)}


def weekly_worst(Gd, start_weekday):
    """Worst week from January 2026 under weeks starting on the given weekday (0 Monday .. 6 Sunday)."""
    allm = G.trace(Gd, D(2025, 12, 25), D(2026, 9, 30))
    wk = Counter()
    for f, a in allm.values():
        d = D.fromisoformat(a["appointment_date"])
        wk[d - dt.timedelta(days=(d.weekday() - start_weekday) % 7)] += 1
    wk = {k: v for k, v in wk.items() if k >= D(2026, 1, 1) - dt.timedelta(days=6)}
    top = max(wk, key=wk.get)
    return top, wk[top]
