"""Keep every graded ask figure clear of its rounding edge, and identical on every rounding path, by nudging
records that sit off the main call's path. Runs on the written pack and rewrites it until the bins hold."""
import math

import golden_calc as G
import roles
from world import RATE, annual_value, price_year, MINIMUM


def frac_ok(x, edge=0.10):
    f = x - math.floor(x)
    return abs(f - 0.5) >= edge


def bad_book(cells):
    return [k for k, v in cells.items() if v["revenue"] and not frac_ok_sum(k, v)]


def frac_ok_sum(k, v):
    return True


def check_pilot(res):
    bad = []
    for k, v in res.items():
        f, c, n = v["fee"], v["credit"], v["net"]
        if not (frac_ok(f) and frac_ok(c) and frac_ok(n) and round(f) - round(c) == round(n)):
            bad.append(k)
    return bad


def check_usage(res):
    return [k for k, v in res.items() if v is not None and not frac_ok(v * 10, 0.08)]


def book_revenue_exact(sch):
    out = {}
    for t in G.TYPES:
        for b in G.BANDS:
            s = sch[(sch["type"] == t) & (sch["band"] == b)]
            out[(t, b)] = float(s["revenue"].sum())
    return out


def nudge_value(x, d):
    py = price_year(x["current_term_start"])
    x["pupils_billed"] += d
    x["annual_value_gbp"] = annual_value(x["price_band"], x["current_term_start"], x["pupils_billed"])


def settle(T, reg, A, write, max_rounds=40):
    """`write` rewrites the pack from A; returns the number of rounds used."""
    for rnd in range(max_rounds):
        d = G.load(T)
        sch = G.schools_on_tallybridge(d)
        exact = book_revenue_exact(sch)
        bad_a = [k for k, v in exact.items() if v and not frac_ok(v)]
        bad_b = check_pilot(G.ask_pilot(d))
        bad_c = check_usage(G.ask_usage(d, sch))
        if not (bad_a or bad_b or bad_c):
            return rnd
        main = A.main_uids
        for (t, b) in bad_a:
            pool = [x for x in A.rows if x["billing_basis"] == "Per pupil" and x["status"] == "In force"
                    and not x.get("copy_of") and x.get("site") is None and x.get("uid") not in main
                    and x.get("tag") in ("la", "sat", "special", "single")
                    and reg.info[x["urn_current"]]["EstablishmentTypeGroup (name)"] == t and x["price_band"] == b
                    and x["annual_value_gbp"] > MINIMUM[price_year(x["current_term_start"])] + 10]
            pool.sort(key=lambda z: (z["urn"], z["agreement_start"]))
            x = pool[rnd % len(pool)]
            nudge_value(x, 1)
        for trust in bad_b:
            uid = int(A.uid_of[trust])
            reps = sorted([x for x in A.rows if x.get("uid") == uid and x["status"] == "Replaced by Trust Licence"
                           and x["current_term_end"] > __import__("datetime").date(2026, 8, 31)],
                          key=lambda z: (z["urn"], z["agreement_start"]))
            x = reps[rnd % len(reps)]
            nudge_value(x, 1)
            for L in A.licences:
                if L["uid"] == uid:
                    subs = [z for z in A.rows if z.get("uid") == uid and z["billing_basis"] == "Per pupil"]
                    L["replaced_value"] = round(sum(z["annual_value_gbp"] for z in subs), 2)
                    L["net"] = round(L["licence_value"] - L["replaced_value"], 2)
        for key in bad_c:
            A.usage_tweak[key] = A.usage_tweak.get(key, 0) + 3
        write()
    raise AssertionError("bins would not settle in %d rounds" % max_rounds)
