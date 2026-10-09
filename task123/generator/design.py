"""Builds the task123 world end to end: roster, true paths (repaired so that only designed movers sit
near the line), the amendment plan, versions, annual returns and the screens. build.py writes the
pack from the object this returns and asserts every property the design note lists."""
import datetime as dt

import numpy as np

from common import (MARCH_CENSUSES, SEPT_CENSUS, POTS, SEPT_POT, natural_end, census_q, LINE_PCT,
                    pct1, qend, fyq)
from roster import build_roster, Q
from identity import assign_identity
from movers import assign_movers, assign_short_form, GENERIC
import plan as P
from world import true_totals, build_annual, q4_plan, build_versions
from screen import Book, screen
from lines import build_payments, apt_by_quarter, true_lines, attach_lines, NONAPT
from world import rng_for

DESIGNED = {"marker", "answer", "common", "decoy", "decoy_soft", "filed_offer", "late_restated",
            "lag_dual", "new_june", "dec_may", "dec_mixed", "dec_feb", "june_late23", "june_late24",
            "june_cday23", "june_cday26", "twin_a", "twin_b", "dual_offer23"}


def scored_at(o, c):
    n = natural_end(c)
    if o.first_q > n - 7:
        return False
    if not (o.og_start <= c <= o.og_end):
        return False
    return True


def nat_fall(tot_o, n):
    cur = int(tot_o[n - 3:n + 1].sum())
    prior = int(tot_o[n - 7:n - 3].sum())
    return 100.0 * (prior - cur) / prior


def sept_t_end(o):
    if o.bal == 6:
        return Q(2026, 3)
    if o.bal == 3 and o.sept_status in ("oct", "later"):
        return Q(2025, 12)
    return Q(2026, 6)


def mover_rounds(o):
    out = set()
    for note in o.notes:
        if note.startswith("corpus mover"):
            out.add(int(note.split()[2]))
    return out


def violations(o, tot_o):
    """Truth-based clearance for organisations outside the designed cast."""
    bad = []
    mr = mover_rounds(o)
    for c in MARCH_CENSUSES:
        if not scored_at(o, c):
            continue
        f = nat_fall(tot_o, natural_end(c))
        if c.year in mr:
            if f < 12.6:
                bad.append(("mover_shallow", c.year, f))
        elif f > 6.6:
            bad.append(("near_line", c.year, f))
    if scored_at(o, SEPT_CENSUS):
        e = sept_t_end(o)
        f = nat_fall(tot_o, e)
        if f > 6.6:
            bad.append(("sept_T", 2026, f))
        f3 = nat_fall(tot_o, natural_end(SEPT_CENSUS))
        if f3 > 6.6:
            bad.append(("sept_R3", 2026, f3))
    return bad


FALL_TARGETS = {
    # key: (window end, target fall per cent, quarters scaled to reach it)
    "TB": (Q(2024, 12), 11.60, [Q(2024, 3), Q(2024, 6), Q(2024, 9), Q(2024, 12)]),
    "Y4": (Q(2025, 12), 7.72, [Q(2025, 3), Q(2025, 6), Q(2025, 9), Q(2025, 12)]),
    "G_R2": (Q(2026, 6), 12.55, [Q(2025, 9), Q(2025, 12), Q(2026, 3), Q(2026, 6)]),
    "L_dual": (Q(2026, 6), 6.35, [Q(2025, 9), Q(2025, 12), Q(2026, 3), Q(2026, 6)]),
}


def hit_target(t, end, pct, quarters):
    """Scale the listed quarters so the trailing-window fall to `end` is pct (to 0.005)."""
    t = t.copy()
    for _ in range(60):
        cur = int(t[end - 3:end + 1].sum())
        prior = int(t[end - 7:end - 3].sum())
        want_cur = prior * (1 - pct / 100.0)
        gap = want_cur - cur
        if abs(100.0 * (prior - cur) / prior - pct) < 0.004:
            break
        in_cur = [q for q in quarters if end - 3 <= q <= end]
        base = sum(int(t[q]) for q in in_cur)
        for q in in_cur:
            t[q] = int(round(t[q] + gap * t[q] / base))
    return t


def repaired_totals(orgs):
    tot = {}
    for o in orgs:
        seed = 0
        t = true_totals(o, seed)
        if o.role in DESIGNED:
            if o.key in FALL_TARGETS:
                t = hit_target(t, *FALL_TARGETS[o.key])
            tot[o.key] = t
            continue
        tries = 0
        while True:
            bad = violations(o, t)
            if not bad:
                break
            tries += 1
            if any(b[0] == "mover_shallow" for b in bad) and tries % 5 == 0:
                for ry in mover_rounds(o):
                    for q in [Q(ry - 1, m) for m in (3, 6, 9, 12)]:
                        o.dips[q] *= 0.98
            if tries % 12 == 0:
                o.sigma *= 0.8
            if tries % 7 == 0 and any(b[0] in ("near_line", "sept_T", "sept_R3") for b in bad):
                o.growth = min(o.growth + 0.01, 0.07)
            seed += 1
            t = true_totals(o, seed)
            if tries > 400:
                raise AssertionError(f"cannot clear {o.key}: {bad}")
        o.eps_seed = seed
        tot[o.key] = t
    by = {o.key: o for o in orgs}
    for o in orgs:
        if o.copy_from:
            a, b = o.copy_span
            tot[o.key][a:b + 1] = tot[o.copy_from][a:b + 1]
    return tot


def build(params=None, nudges=None):
    params = dict(DEFAULT_PARAMS, **(params or {}))
    nudges = nudges or {}
    orgs = build_roster()
    assign_identity(orgs)
    assign_movers(orgs)
    assign_short_form(orgs)
    by = {o.key: o for o in orgs}
    tot = repaired_totals(orgs)
    for (key, q), dlt in sorted(nudges.items()):
        tot[key][q] += dlt
    annual = build_annual(orgs, tot)
    plan = make_plan(orgs, tot, annual, params)
    q4p = q4_plan(orgs, annual, plan)
    versions = build_versions(orgs, tot, annual, plan, q4p)
    book = Book(orgs, versions, annual)
    W = dict(orgs=orgs, by=by, tot=tot, annual=annual, plan=plan, q4p=q4p, versions=versions,
             book=book, params=params, nudges=nudges)
    W["corpus"] = {c: screen(book, c, POTS[c.year]) for c in MARCH_CENSUSES}
    W["sept"] = screen(book, SEPT_CENSUS, SEPT_POT)
    complete(W)
    return W


def complete(W):
    """Payments from the published rounds, then the income lines of every return."""
    orgs, tot, by = W["orgs"], W["tot"], W["by"]
    offers = {c.year: {r["org"]: r["offer"] for r in W["corpus"][c]["rows"] if r["offer"]}
              for c in MARCH_CENSUSES}
    pays, terms, sgf_refs, pg_level = build_payments(orgs, offers, W["params"]["reissues"])
    W.update(payments=pays, terms=terms, sgf_refs=sgf_refs, pg_level=pg_level, offers_by_round=offers)
    refs_of = {o.key: {o.og_ref} | ({o.pg_ref} if o.dual else set()) for o in orgs}
    for (ry, key), ref in sgf_refs.items():
        refs_of[key].add(ref)
    W["refs_of"] = refs_of
    apt = apt_by_quarter(pays, orgs)
    apt_og = apt_by_quarter(pays, orgs, progs=("OG", "PG"))
    W["apt"] = apt
    W["apt_og"] = apt_og
    ref_tot = {}
    for o in orgs:
        ref_tot[o.key] = np.array([int(round(tot[o.key][q] / o.dips.get(q, 1.0)))
                                   for q in range(len(tot[o.key]))], dtype=np.int64)
    W["true_lines"] = true_lines(orgs, tot, apt, ref_tot, apt_og)
    for (key, q4), ar in W["annual"].items():
        L = W["true_lines"][key]
        s = {k: sum(L[q][k] for q in range(q4 - 3, q4 + 1)) for k in L[q4]}
        ar.lines = {"gov": s["gov_grant"] + s["gov_contract"], "donations": s["donations"],
                    "trading": s["trading"], "grants_other": s["other_grants"] + s["apt"] + s["apt_sgf"],
                    "investment": s["investment"], "other": s["other"]}
        assert sum(ar.lines.values()) == ar.total
    attach_lines(W)
    return W


DEFAULT_PARAMS = {
    "twin_a_pct": 5.9,
    "g_r2_held_pct": 5.4,
    "l_dual_pg_pct": 12.7,
    "reissues": [("F5", dt.date(2025, 2, 20)), ("B020", dt.date(2025, 8, 20))],
}


def window_sum(tot_o, end):
    return int(tot_o[end - 3:end + 1].sum()), int(tot_o[end - 7:end - 3].sum())


def pick_post_census(orgs, tot, W_corpus_offered=None):
    """Seven corrections a round to the last quarter of the window, accepted after the census;
    one of them, in four rounds, to an organisation the round offered."""
    rng = np.random.default_rng([12345, 21])
    by = {o.key: o for o in orgs}
    picks = []
    offered_rounds = {2021, 2022, 2024, 2025}
    for c in MARCH_CENSUSES:
        ry = c.year
        pool = sorted([o for o in orgs if o.role in ("steady", "entrant", "deadline_steady", "exit")
                       and scored_at(o, c) and o.bal in (3, 6) and not mover_rounds(o) & {ry}
                       and not o.dual], key=lambda o: o.key)
        idx = rng.permutation(len(pool))[:7]
        for j in idx:
            frac = float(rng.uniform(0.02, 0.06)) * (1 if rng.random() < 0.5 else -1)
            d = dt.date(ry, 4, 7) + dt.timedelta(days=int(rng.integers(0, 200)))
            picks.append((pool[int(j)].key, ry, frac, d))
        if ry in offered_rounds:
            movers = sorted([o for o in orgs if ry in mover_rounds(o) and o.bal in (3, 6)
                             and not o.dual], key=lambda o: o.key)
            o = movers[int(rng.integers(0, len(movers)))]
            d = dt.date(ry, 5, 4) + dt.timedelta(days=int(rng.integers(0, 120)))
            picks.append((o.key, ry, 0.035, d))
    return picks


def make_plan(orgs, tot, annual, params):
    plan = {}
    by = {o.key: o for o in orgs}
    P.residue_plan(plan)
    P.october_exact(plan, orgs)
    # the twin pair: TA's published fall is 5.9 per cent, TB's 11.6
    n25 = natural_end(dt.date(2025, 3, 31))
    cur, prior = window_sum(tot["TB"], n25)
    x = int(round(prior * (100.0 * (prior - cur) / prior - params["twin_a_pct"]) / 100.0))
    P.twin_plan(plan, x)
    # G_R2's June 2026 quarter was first filed high and restated on 5 October 2026
    cur, prior = window_sum(tot["G_R2"], Q(2026, 6))
    true_pct = 100.0 * (prior - cur) / prior
    P.g_r2_plan(plan, int(round(prior * (true_pct - params["g_r2_held_pct"]) / 100.0)))
    # L_dual's June 2026 quarter was filed low under both references; corrected under one
    cur, prior = window_sum(tot["L_dual"], Q(2026, 6))
    true_pct = 100.0 * (prior - cur) / prior
    P.l_dual_plan(plan, int(round(prior * (params["l_dual_pg_pct"] - true_pct) / 100.0)))
    P.du2_plan(plan, int(round(tot["DU2"][Q(2022, 12)] * 0.031)))
    P.post_census_corrections(plan, orgs, tot, pick_post_census(orgs, tot))
    # four on-time filers whose fourth quarter was re-amended (line split only) after a census
    v3 = []
    rng = np.random.default_rng([12345, 22])
    for ry in (2022, 2023, 2025, 2026):
        c = dt.date(ry, 3, 31)
        pool = sorted([o for o in orgs if o.role in ("steady", "deadline_steady") and o.bal == 3
                       and scored_at(o, c) and not o.short_form and not mover_rounds(o)
                       and (o.key, Q(ry - 1, 3)) not in plan], key=lambda o: o.key)
        o = pool[int(rng.integers(0, len(pool)))]
        d = dt.date(ry, 4, 13) + dt.timedelta(days=int(rng.integers(0, 12)))
        v3.append((o.key, ry, d, {"donations": 1, "other": -1}))
    W_v3 = []
    for key, ry, d, sh in v3:
        q = Q(ry - 1, 3)
        amt = int(round(tot[key][q] * 0.04))
        P.add(plan, (key, q), events=[{"date": d, "kind": "linesplit", "refs": "both",
                                       "shift": {"donations": amt, "other": -amt}}])
        W_v3.append((key, ry))
    params["_v3"] = W_v3
    # H4: three returns whose latest delivery was rejected for line coding (same total)
    h4 = [("F2", Q(2025, 6), dt.date(2025, 11, 18)), ("F4", Q(2024, 6), dt.date(2024, 11, 12)),
          ("B031", Q(2025, 9), dt.date(2026, 2, 24))]
    for key, q, d in h4:
        amt = int(round(tot[key][q] * 0.05))
        P.add(plan, (key, q), events=[{"date": d, "kind": "coding", "refs": "both",
                                       "shift": {"gov_contract": -amt, "trading": amt,
                                                 "apt_memo": -int(round(amt * 0.25))}}])
    params["_h4"] = h4
    # H1: the dual grantee's project-grant copy keeps the original line coding
    for q in (Q(2024, 12), Q(2025, 6)):
        amt = int(round(tot["F3"][q] * 0.045))
        P.add(plan, ("F3", q), v1_shift={"op": {"gov_contract": amt, "trading": -amt},
                                         "pg": {"gov_contract": amt, "trading": -amt}},
              events=[{"date": qend(q) + dt.timedelta(days=118), "kind": "linesplit", "refs": "op",
                       "shift": {}}])
    texture(plan, orgs, tot)
    return plan


def texture(plan, orgs, tot):
    """Ordinary portal traffic: quick corrections, withdrawn submissions and line re-coding, none of
    which changes a figure held at any census."""
    rng = np.random.default_rng([12345, 23])
    pool = sorted([o for o in orgs if o.role in ("steady", "entrant", "deadline_steady", "exit",
                                                   "unfiled_steady")], key=lambda o: o.key)
    for n in range(150):
        o = pool[int(rng.integers(0, len(pool)))]
        q = int(rng.integers(max(o.first_q, 5), min(o.last_q, 36) + 1))
        if fyq(q, o.bal) == 4 or (o.key, q) in plan:
            continue
        kind = ["correction", "withdrawn", "linesplit"][int(rng.integers(0, 3))]
        orig_acc = qend(q) + dt.timedelta(days=60)
        d = orig_acc + dt.timedelta(days=int(rng.integers(8, 30)))
        if any(qend(q) <= c <= d + dt.timedelta(days=10) for c in MARCH_CENSUSES + [SEPT_CENSUS]):
            continue
        if kind == "correction":
            e = int(round(tot[o.key][q] * float(rng.uniform(0.01, 0.04)))) * (1 if rng.random() < 0.5 else -1)
            P.add(plan, (o.key, q), v1_error={"op": e, "pg": e},
                  events=[{"date": d, "kind": "correction", "refs": "both", "error_after": 0}])
        elif kind == "withdrawn":
            P.add(plan, (o.key, q), events=[{"date": d, "kind": "withdrawn", "refs": "op"}])
        else:
            amt = int(round(tot[o.key][q] * 0.03))
            P.add(plan, (o.key, q), v1_shift={"op": {"other_grants": -amt, "other": amt}},
                  events=[{"date": d, "kind": "linesplit", "refs": "op", "shift": {}}])
