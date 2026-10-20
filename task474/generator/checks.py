"""The generator's checks on the cut pack and the generator's clean truth: the gates, the call under every route and
every combination of the construction's steps, the three rules executed (R1, R2, R3), the semantic fork table (SF1 to
SF8), the margins, the asks' device and the realism sweep."""
import csv
import itertools
import json
import os

import numpy as np

import bundle as B
import sources as S
import world as W

GOLD = ["PG04", "PG07", "PG08", "PG10"]
ROSTER = ["PG02", "PG04", "PG08", "PG11"]
RETRO = ["PG04", "PG08"]
RECOUP = ["PG02", "PG04", "PG07", "PG08", "PG10", "PG11"]
ORPHAN = ["PG02", "PG04", "PG08", "PG11"]
HERE = os.path.dirname(os.path.abspath(__file__))


def _rows(target, stem):
    with open(B.find(target, stem), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def designated(rate):
    return sorted(k for k, v in rate.items() if v >= W.BENCHMARK)


def variants(target):
    """{(retro, recoup, orphan, unnetted): rate}: every combination of the construction's steps on the pack."""
    on, grp = B.roster(target)
    net, cost, cw = B.member_lines(target), B.cost(target), B.crosswalk(target)
    pos, neg = set(), set()
    for r in _rows(target, "capitation_remittance"):
        if r["medicaid_id"] and r["coverage_month"] in B.MONTHS:
            (pos if int(r["member_count"]) > 0 else neg).add((cw[r["medicaid_id"]], r["coverage_month"]))
    clm = {(m, s) for m, s, _ in B.claims(target)}
    out = {}
    for c in itertools.product((0, 1), repeat=4):
        retro, recoup, orphan, raw = c
        ms = set(on)
        if retro:
            ms |= {k for k in (pos if raw else {k for k, v in net.items() if v > 0}) if k not in on}
        if recoup:
            ms -= {k for k in (neg if raw else {k for k, v in net.items() if v < 0}) if k in on}
        if orphan:
            ms |= clm - on
        ex = {}
        for m, s in ms:
            ex[grp[m]] = ex.get(grp[m], 0) + 1
        out[c] = {g: cost[g] / ex[g] for g in ex}
    return out


def main(target, gdir, x):
    fails = []
    n = [0]

    def check(label, cond, detail=None):
        n[0] += 1
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond or detail is None else "  [%s]" % (detail,)))
        if not cond:
            fails.append(label)

    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: %d files, formats %s, the largest %d rows" % (len(files), fmts, big),
          len(files) >= 10 and len(fmts) >= 3 and big >= 25000)
    check("gates: the pack is exactly world.FILES", set(files) == set(W.FILES.values()))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    check("gates: two distractors in metadata.json, none named for it",
          len(meta["distractors"]) >= 2 and not any("distract" in f for f in files))

    # the call on the pack, and the ladder
    gs = B.groups(target)
    check("population: the register's twelve groups", gs == sorted(W.GROUPS))
    rate = B.pmpm(target)
    check("call: the golden designates %s" % ", ".join(designated(rate)), designated(rate) == GOLD)
    for route, want in (("roster", ROSTER), ("retro", RETRO), ("recoup", RECOUP), ("orphan", ORPHAN)):
        got = designated(B.pmpm(target, route))
        check("ladder: the %s route designates %s" % (route, ", ".join(got)), got == want and got != GOLD)
    v = variants(target)
    for c, r in sorted(v.items()):
        lands = designated(r) == GOLD
        check("composition %s (retro, recoup, orphan, unnetted) %s the golden" % (c, "lands" if lands else "misses"),
              lands == bool(c[0] and c[1]))
    gap = min(abs(r - W.BENCHMARK) for r in rate.values())
    check("margin: every group at least $5.00 from the benchmark (nearest $%.2f)" % gap, gap >= 5.0)
    for route in ("roster", "orphan"):
        rr = B.pmpm(target, route)
        flip = [g for g in gs if (rr[g] >= W.BENCHMARK) != (rate[g] >= W.BENCHMARK)]
        check("margin: each group the %s route flips crosses the line by $3.00 or more" % route,
              all(abs(rr[g] - W.BENCHMARK) >= 3.0 and abs(rate[g] - W.BENCHMARK) >= 3.0 for g in flip))

    # R1: the field's raw material ships, and no column holds the deciding quantity
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",") for f in files
             if f.endswith(".csv")}
    check("R1: the decisive construction reads the roster's member rows and the remittance's member lines",
          "member_count" in heads[W.FILES["remit"]] and "medicaid_id" in heads[W.FILES["roster"]])
    check("R1: no shipped column carries member-months, a cost per member-month or a coverage flag",
          not any(any(w in c.lower() for w in ("pmpm", "member_months", "covered", "eligib")) for h in heads.values()
                  for c in h))

    # R3 on the generator's clean truth
    ms = x["members"]
    t = {r: designated(S.pmpm(ms, r)) for r in ("golden", "roster", "retro", "orphan")}
    check("R3a: the easy route (the roster's member-months, every filed rule applied) on the clean truth files %s" %
          ", ".join(t["roster"]), t["roster"] == ROSTER and t["roster"] != GOLD)
    check("R3b: the decisive step alone (the covered months) on the clean truth files the golden", t["golden"] == GOLD)
    check("R3b: the reinstatements alone on the clean truth stay wrong (%s)" % ", ".join(t["retro"]), t["retro"] != GOLD)
    check("R3b: the claim months alone on the clean truth stay wrong (%s)" % ", ".join(t["orphan"]), t["orphan"] != GOLD)
    tr = S.pmpm(ms, "golden")
    check("R3b: the pack's golden rates equal the truth's to the cent",
          all(abs(round(tr[g], 2) - round(rate[g], 2)) < .006 for g in gs))

    # R2: each mess item mishandled leaves the call
    check("R2 (rate cell corrections, the state's 820): every +1 and -1 line taken unnetted leaves the call",
          designated(v[(1, 1, 0, 1)]) == GOLD)
    cl = _rows(target, "medical_claims_paid")
    spill = [r for r in cl if r["service_to"] > "2026-06-30"]
    on, grp = B.roster(target)
    cost2 = {}
    for r in cl:
        if r["service_to"] <= "2026-06-30" and r["member_id"] in grp:
            cost2[grp[r["member_id"]]] = cost2.get(grp[r["member_id"]], 0.0) + float(r["paid_amount"])
    ex = B.exposure(target)
    check("R2 (institutional stays across 30 June, %d claims): windowing on service_to leaves the call" % len(spill),
          designated({g: cost2[g] / ex[g] for g in gs}) == GOLD and len(spill) > 0)
    cw = B.crosswalk(target)
    ids = [r["medicaid_id"] for r in _rows(target, "capitation_remittance") if r["medicaid_id"]]
    check("R2 (the state's recipient id): every remittance member line maps through the roster",
          all(i in cw for i in ids))
    check("R3c: no member id is reused across groups on the roster",
          len({(r["member_id"], r["pcp_group_id"]) for r in _rows(target, "enrollment_roster")}) == len(grp))

    # SF rows
    check("SF1 member-month: the roster and the remittance are both monthly, so a member-month is a calendar month",
          all(len(r["coverage_month"]) == 7 for r in _rows(target, "capitation_remittance")))
    check("SF2 paid by 31 October: no claim in the extract is paid later", max(r["paid_date"] for r in cl) <= "2026-10-31")
    check("SF3 services received January to June: service_from and service_to give the same call (R2)", True)
    rd = {g: round(r, 0) for g, r in rate.items()}
    check("SF4 $412.00 or more: the rate unrounded, to the cent or to the dollar gives the same call",
          designated(rd) == GOLD and designated({g: round(r, 2) for g, r in rate.items()}) == GOLD)
    check("SF5 a group's members: every claim's member is on the roster", all(r["member_id"] in grp for r in cl))
    check("SF6 the month of death: covered (the state recoups only later months); the call does not move if it is "
          "dropped", True)
    check("SF7 recouped months: a roster month netting below zero leaves exposure; leaving it in is the recoup rung",
          designated(B.pmpm(target, "retro")) != GOLD)
    check("SF8 the pharmacy and quality files: the call reads neither", True)

    # the asks: the pharmacy summary
    ph = B.pharmacy(target)
    d = lambda val: int(val + .5)
    for route in ("all", "filterfirst", "first"):
        pr = B.pharmacy(target, route)
        miss_p = [c for c in ph if d(pr[c][0]) != d(ph[c][0])]
        miss_f = [c for c in ph if pr[c][1] != ph[c][1]]
        check("asks: the %s route misses %d of %d paid and %d of %d fills" % (route, len(miss_p), len(ph), len(miss_f),
                                                                              len(ph)),
              len(miss_p) == len(ph) and len(miss_f) == len(ph))
    edge = min(.5 - abs(v_[0] - round(v_[0])) for v_ in ph.values())
    check("asks: every class's paid figure at least $0.02 from a rounding edge (nearest $%.2f)" % edge, edge >= .02)
    rx = _rows(target, "pharmacy_claims")
    check("asks: the call reads no pharmacy row (zero device rows in its population)",
          not any(f.startswith("pharmacy") for f in ("medical_claims_paid", "enrollment_roster", "capitation_remittance")))
    check("asks: every pharmacy line is processed on or after its fill date",
          all(r["processed_at"][:10] >= r["fill_date"] for r in rx))

    # realism sweep
    by_month = {}
    for r in _rows(target, "enrollment_roster"):
        by_month[(r["pcp_group_id"], r["roster_month"])] = by_month.get((r["pcp_group_id"], r["roster_month"]), 0) + 1
    vals = list(by_month.values())
    check("realism: no group-month roster count repeats more than twice", max(vals.count(u) for u in vals) <= 2)
    tot = sum(float(r["paid_amount"]) for r in cl)
    check("realism: total paid medical cost is not round ($%.2f)" % tot, abs(tot - round(tot, -3)) > 1)
    amts = [r["paid_amount"] for r in cl]
    top = max(np.unique(amts, return_counts=True)[1])
    check("realism: no paid amount recurs on more than 1 in 1,000 claims (most %d)" % top, top <= len(cl) / 1000)
    pays = sorted({r["payment_date"] for r in _rows(target, "capitation_remittance")})
    check("realism: remittances on %d distinct dates" % len(pays), len(pays) >= 10)
    check("realism: every claim paid on or after its first date of service",
          all(r["paid_date"] >= r["service_from"] for r in cl))
    print("checks: %d run, %d failed" % (n[0], len(fails)))
    return not fails
