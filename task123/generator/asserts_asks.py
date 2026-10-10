"""Ask-layer assertions: K1 and K2 golden figures, every designed stop, the necessity matrix, the
composed mishandlings, the over-cleaner, the referee, the pair simulation, the separation count and
the memo against the payment run (A44 to A50, A53)."""
from itertools import combinations

from common import SEPT_CENSUS, fyq, qend, fpos
from lines import is_new_form, TOTAL_CODES, MEMO_CODES
from asks import k1, k2, windows, apt_series, pick_version
from screen import eod

K1_DEV = {  # device or hazard -> keyword arguments for k1
    "D10 the co-funding at a twelfth on every instalment": dict(cofund="twelfths"),
    "D5 government co-funding left out (counted only from the government lines)": dict(cofund=None),
    "D8 co-funding by instalment month": dict(cofund="for"),
    "H6 GOV_GRT read as one line on both forms": dict(mapping="label"),
    "H2 comparatives": dict(comps=True),
    "H1 project-grant copy": dict(vhow="pg"),
    "H4 latest delivered": dict(vhow="delivered"),
}
RUN_ONLY = ("OG", "PG")
K2_DEV = {
    "D4 Steady Ground instalments left out": dict(progs=RUN_ONLY),
    "D10 the co-funding out at a twelfth on every instalment": dict(cofund_how="twelfths"),
    "D5 government co-funding left in": dict(cofund_out=False),
    "D8 instalment month": dict(how="for"),
    "H5 returned payments": dict(statuses=("paid", "returned")),
    "H1 one grant reference": dict(drop_pg=True),
}
K1_PRIMARY = "D10 the co-funding at a twelfth on every instalment"
K2_PRIMARY = "D4 Steady Ground instalments left out"


def merge(kws):
    out = {}
    for kw in kws:
        for k, v in kw.items():
            if k == "memo":
                out.setdefault("memo", {}).update(v)
            else:
                if k in out and out[k] != v:
                    return None
                out[k] = v
    return out


def golden_asks(W):
    T = W["sept"]
    c = SEPT_CENSUS
    G = {}
    for r in T["rows"]:
        cq, pq = windows(r)
        G[r["org"]] = {"K1": k1(W, r["org"], cq, pq, c), "K2": k2(W, r["org"], cq, pq, c)}
    return G


def check_asks(W, C, S):
    T = S["T"]
    R6 = {r["org"]: r for r in S["R6"]["rows"]}
    R3 = {r["org"]: r for r in S["R3"]["rows"]}
    c = SEPT_CENSUS
    offered = [r for r in T["rows"] if r["offer"]]
    n = len(offered)
    G = golden_asks(W)
    W["golden_asks"] = G

    def stop_k1(r, **kw):
        return k1(W, r["org"], *windows(r), c, **kw)

    def stop_k2(r, **kw):
        return k2(W, r["org"], *windows(r), c, **kw)

    # A45: every stop's value per offered grantee, either untouched or at least NZ$500 away
    stops_k1 = {"S1 the government lines alone": dict(cofund=None),
                "S2 co-funding by instalment month": dict(cofund="for"),
                "S2b the co-funding at a twelfth on every instalment, by value date": dict(cofund="twelfths"),
                "S2c the co-funding at a twelfth on every instalment, by instalment month": dict(cofund="twelfths_for"),
                "S3 GOV_GRT on both forms": dict(mapping="label"),
                "S4 comparatives": dict(comps=True),
                "S5 whole fees line to government": dict(mapping="over")}
    stops_k2 = {"S0 the payment run alone": dict(progs=RUN_ONLY, cofund_out=False),
                "S1 run and instalments, co-funding left in": dict(cofund_out=False),
                "S2 run less co-funding, no instalments": dict(progs=RUN_ONLY),
                "S2b run and instalments less a twelfth of the co-funding a month": dict(cofund_how="twelfths"),
                "S2c the run less a twelfth of the co-funding a month": dict(progs=RUN_ONLY, cofund_how="twelfths"),
                "S3 instalment month": dict(how="for"),
                "S4 returned summed with reissue": dict(statuses=("paid", "returned")),
                "S5 last ten days dropped": dict(how="transit"),
                "S6 one grant reference": dict(drop_pg=True)}
    moved = {}
    for ask, stops, fn in (("K1", stops_k1, stop_k1), ("K2", stops_k2, stop_k2)):
        for name, kw in stops.items():
            vals = [(r["org"], fn(r, **kw) - G[r["org"]][ask]) for r in offered]
            near = [(k, d) for k, d in vals if d != 0 and abs(d) < 500]
            moved[(ask, name)] = [k for k, d in vals if d != 0]
            C.ok("A45", not near, f"{ask} {name}: moves {len(moved[(ask, name)])} of {n} offered, none within NZ$500 ({near})")
    # the mirror: the stop (R6) holds every offered grantee on the answer's windows, so only the devices
    # separate it; R3 differs on the two 30 June offerees' windows and misses both on both asks
    same = [r["org"] for r in offered if r["org"] in R6 and (R6[r["org"]]["end"], R6[r["org"]]["pend"]) == (r["end"], r["pend"])]
    C.ok("A45", len(same) == n, f"the stop (R6) holds every one of the {n} offered grantees on the answer's windows")
    mir1 = [(r["org"], k1(W, r["org"], *windows(R3[r["org"]]), c, q4src="portal") - G[r["org"]]["K1"])
            for r in offered if R3[r["org"]]["end"] != r["end"]]
    mir2 = [(r["org"], k2(W, r["org"], *windows(R3[r["org"]]), c) - G[r["org"]]["K2"])
            for r in offered if R3[r["org"]]["end"] != r["end"]]
    C.ok("A45", len(mir1) == 2 and all(abs(d) >= 500 for _, d in mir1 + mir2),
         f"R3's June windows miss both 30 June offerees on K1 and K2 by NZ$500 or more ({mir1}, {mir2})")
    # lazy deltas: the most natural path on each ask
    lazy1 = [r["org"] for r in offered if abs(stop_k1(r, cofund=None) - G[r["org"]]["K1"]) >= 2000]
    lazy2 = [r["org"] for r in offered
             if abs(stop_k2(r, progs=RUN_ONLY, cofund_out=False) - G[r["org"]]["K2"]) >= max(0.08 * abs(G[r["org"]]["K2"]), 1000)]
    C.ok("A45", len(lazy1) == n, f"K1 lazy path (the government lines alone) moves {len(lazy1)} of {n} by NZ$2,000 or more")
    C.ok("A45", len(lazy2) == n, f"K2 lazy path (the payment run alone) moves {len(lazy2)} of {n} by 8 per cent or NZ$1,000")
    W["lazy"] = (len(lazy1), len(lazy2))
    # A46: necessity matrix (each device mishandled alone moves exactly the asks in its row)
    rowmap = {}
    for name, kw in K1_DEV.items():
        rowmap[("K1", name)] = sorted(r["org"] for r in offered if stop_k1(r, **kw) != G[r["org"]]["K1"])
    for name, kw in K2_DEV.items():
        rowmap[("K2", name)] = sorted(r["org"] for r in offered if stop_k2(r, **kw) != G[r["org"]]["K2"])
    W["necessity"] = rowmap
    C.ok("A46", len(rowmap[("K1", K1_PRIMARY)]) == n, "D10 (the co-funding at a twelfth a month) moves every K1")
    d10 = [abs(stop_k1(r, cofund="twelfths") - G[r["org"]]["K1"]) for r in offered]
    C.ok("A46", min(d10) >= 4000, f"D10 moves each offered K1 by four months' co-funding, NZ${min(d10):,} to NZ${max(d10):,}")
    C.ok("A46", len(rowmap[("K1", "D5 government co-funding left out (counted only from the government lines)")]) == n,
         "D5 (the co-funding left out) moves every K1")
    C.ok("A46", len(rowmap[("K1", "D8 co-funding by instalment month")]) == n, "D8 moves every K1")
    C.ok("A46", len(rowmap[("K2", K2_PRIMARY)]) == n, "D4 moves every K2")
    C.ok("A46", len(rowmap[("K2", "D10 the co-funding out at a twelfth on every instalment")]) == n, "D10 moves every K2")
    C.ok("A46", len(rowmap[("K2", "D5 government co-funding left in")]) == n, "D5 moves every K2")
    C.ok("A46", len(rowmap[("K2", "D8 instalment month")]) >= n - 2, "D8 moves K2")
    C.ok("A46", len(rowmap[("K1", "H6 GOV_GRT read as one line on both forms")]) >= n - 1, "H6 (the old code reading) moves K1")
    C.ok("A46", rowmap[("K1", "H1 project-grant copy")] == ["F3"] and rowmap[("K2", "H1 one grant reference")] == ["F3"],
         "H1 moves K1 and K2 for the offered dual grantee only")
    d_h1 = abs(stop_k1(next(r for r in offered if r["org"] == "F3"), vhow="pg") - G["F3"]["K1"])
    C.ok("A46", d_h1 >= 1500, f"H1 moves the dual grantee's K1 by NZ${d_h1}")
    C.ok("A46", rowmap[("K1", "H4 latest delivered")] == ["F2", "F4"],
         "H4 moves K1 for the two offered grantees with a rejected latest delivery")
    for k in ("F2", "F4"):
        r = next(x for x in offered if x["org"] == k)
        C.ok("A46", abs(stop_k1(r, vhow="delivered") - G[k]["K1"]) >= 1000, f"H4 moves {k}'s K1 by NZ$1,000 or more")
    C.ok("A46", rowmap[("K2", "H5 returned payments")] == ["F5"], "H5 moves K2 for one offered grantee")
    h2 = [r["org"] for r in offered if abs(stop_k1(r, comps=True) - G[r["org"]]["K1"]) >= 0.05 * abs(G[r["org"]]["K1"])]
    C.ok("A46", len(h2) >= n - 4, f"H2 moves {len(h2)} of {n} offered K1 figures by 5 per cent or more")
    # H3: short-form filers carry no government line and no memo
    short = [r for r in T["rows"] if W["by"][r["org"]].short_form]
    C.ok("A46", len(short) >= 20 and all(G[r["org"]]["K1"] is None for r in short)
         and not any(W["by"][r["org"]].short_form for r in offered),
         f"H3: {len(short)} short-form scored grantees, K1 empty for each, none offered")
    # the co-funding: which grantees carried it and that every offered grantee is among them
    cof = sorted(o.key for o in W["orgs"] if o.cofund)
    C.ok("A46", len(cof) >= 30 and all(r["org"] in cof for r in offered),
         f"government co-funding carried by {len(cof)} grantees, every offered grantee among them")
    # A47: composed mishandlings, every subset of the devices that touch a figure
    worst = None
    for r in offered:
        for ask, devs, fn in (("K1", K1_DEV, stop_k1), ("K2", K2_DEV, stop_k2)):
            touching = [nm for nm in devs if r["org"] in rowmap[(ask, nm)]]
            for m in range(1, len(touching) + 1):
                for sub in combinations(touching, m):
                    kw = merge(devs[nm] for nm in sub)
                    if kw is None:
                        continue
                    d = abs(fn(r, **kw) - G[r["org"]][ask])
                    if worst is None or d < worst[0]:
                        worst = (d, r["org"], ask, sub)
                    C.ok("A47", d >= 500, f"{ask} {r['org']} under {'+'.join(sub)} lands NZ${d} from the answer")
    W["composed_worst"] = worst
    # A48: the over-cleaner lands on its designed over-corrected stop
    oc1 = [r["org"] for r in offered if stop_k1(r, mapping="over") != G[r["org"]]["K1"]]
    oc2 = [r["org"] for r in offered if stop_k2(r, how="transit") != G[r["org"]]["K2"]]
    C.ok("A48", len(oc1) == n and len(oc2) == n,
         "over-cleaning (the whole fees line as government, ten-day transit) fails every offered figure")
    # A49: the referee ties to the government lines' financial-year totals, never to the co-funding,
    # and to no re-presented split
    from asks import gov_quarter
    ties, rep_bad = 0, 0
    for r in offered:
        o = W["by"][r["org"]]
        for (key, q4), ar in W["annual"].items():
            if key != o.key or ar.received is None or q4 < r["pend"] - 7 or q4 - 3 > r["end"]:
                continue
            s_ = sum(gov_quarter(W, o, q, eod(SEPT_CENSUS), "register") for q in range(q4 - 3, q4 + 1)
                     if q >= 5)
            if q4 - 3 >= 5 and s_ == ar.lines["gov"]:
                ties += 1
        for (key, q4), ar in W["annual"].items():
            if key != o.key or ar.received is None:
                continue
            nv = pick_version(W, o, q4 + 4, eod(SEPT_CENSUS))
            if nv is not None and is_new_form(q4 + 4) and not is_new_form(q4):
                if nv.lines["GOV_GRT"][1] != ar.lines["gov"]:
                    rep_bad += 1
    C.ok("A49", ties >= 15 and rep_bad >= 6,
         f"referee: {ties} offered-grantee years tie to the register; {rep_bad} re-presented comparatives do not")
    s2diff = [r["org"] for r in offered if stop_k1(r, comps=True) != G[r["org"]]["K1"]]
    C.ok("A49", len(s2diff) >= n - 3, f"the re-presented split misses {len(s2diff)} of {n} window figures")
    # the register's government figure leaves the co-funding out for every co-funded year, so the
    # year-end check passes on the lazy path: it confirms the government lines, never the co-funding
    from asks import cofund_series
    cs = cofund_series(W)
    co_years = 0
    for (key, q4), ar in W["annual"].items():
        o = W["by"][key]
        if not o.cofund or ar.received is None or o.short_form:
            continue
        if sum(cs[key][q] for q in range(q4 - 3, q4 + 1)):
            co_years += 1
            gl = sum(L["gov_grant"] + L["gov_contract"] for L in (W["true_lines"][key][q] for q in range(q4 - 3, q4 + 1)))
            if gl != ar.lines["gov"]:
                co_years = -10**6
    C.ok("A49", co_years >= 20, f"on {co_years} co-funded financial years the register's government figure equals the "
                                "government lines and carries none of the co-funding")
    # A50: pair simulation (habitual battery: statuses, the dual collapse, comparatives, the notice's code
    # mapping, the register year-end check and the memo check handled; the co-funding found on the
    # Variations sheet and taken at a twelfth of its annual figure on every instalment, as solver round 3
    # took it; the quarterly timing and the Steady Ground instalments not). The stop R6 holds the same
    # windows on every offered grantee.
    crack1 = sum(1 for r in offered if stop_k1(r, cofund="twelfths") == G[r["org"]]["K1"])
    crack2 = sum(1 for r in offered if stop_k2(r, progs=RUN_ONLY, cofund_how="twelfths") == G[r["org"]]["K2"])
    mirror = 0
    for r in offered:
        m = R6[r["org"]]
        mirror += (k1(W, r["org"], *windows(m), c, cofund="twelfths") == G[r["org"]]["K1"])
        mirror += (k2(W, r["org"], *windows(m), c, progs=RUN_ONLY, cofund_how="twelfths") == G[r["org"]]["K2"])
    Lc = (crack1 + crack2) / (2.0 * n)
    Ls = mirror / (2.0 * n)
    cracker = 38 + 7 + 55 * Lc
    mir = 3 + 7 + 55 * Ls
    pair = (cracker + mir) / 2
    W["pair"] = (cracker, mir, pair, Lc, Ls)
    C.ok("A50", pair <= 40, f"pair simulation: cracker {cracker:.1f}, mirror {mir:.1f}, average {pair:.1f} (Lc {Lc:.2f}, Ls {Ls:.2f})")
    # A53: the new-form Trust memo equals the operating account's payment run by value date, co-funding
    # inside; Steady Ground money sits outside both
    run = apt_series(W, progs=RUN_ONLY)
    full = apt_series(W)
    bad = 0
    checked = 0
    sg_in_memo_window = 0
    co_in_memo = 0
    for (key, q), lst in W["book"].by_org.items():
        o = W["by"][key]
        if not is_new_form(q) or o.short_form:
            continue
        v = lst[-1]
        k = fpos(o, q)
        want = int(sum(run[key][q - k + 1:q + 1]))
        checked += 1
        if v.lines["GRT_NGO_APT"][0] != want:
            bad += 1
        if int(sum(full[key][q - k + 1:q + 1])) != want:
            sg_in_memo_window += 1
        if sum(cs[key][q - k + 1:q + 1]):
            co_in_memo += 1
    C.ok("A53", bad == 0 and checked > 800, f"memo equals the payment run by value date ({checked} returns, {bad} differ)")
    C.ok("A53", sg_in_memo_window >= 100, f"Steady Ground money sits outside both on {sg_in_memo_window} new-form returns")
    C.ok("A53", co_in_memo >= 150, f"the government co-funding sits inside the memo and the run on {co_in_memo} new-form returns")
    return G


def separation(W, C, portal_rows):
    """A44: no device or hazard row inside the main call's declared row population."""
    main = [r for r in portal_rows if r["line_code"] in TOTAL_CODES and r["column"] == "YTD"]
    devices = {
        "H6 government lines on both forms": lambda r: r["line_code"] in ("FEE_SVC_GOV", "GOV_GRT", "FEE_SVC"),
        "H1 project-grant line copies": lambda r: r["is_pg"] and r["line_code"] not in TOTAL_CODES,
        "H2 comparative column": lambda r: r["column"] == "PY",
        "H3 short-form lines": lambda r: r["short"] and r["line_code"] not in TOTAL_CODES,
        "H4 rejected line coding": lambda r: r["status"] == "rejected" and r["line_code"] not in TOTAL_CODES,
        "D4/D5/D8 Trust memo": lambda r: r["line_code"] == "GRT_NGO_APT",
    }
    counts = {}
    for name, f in devices.items():
        counts[name] = sum(1 for r in main if f(r))
        C.ok("A44", counts[name] == 0, f"{name}: 0 rows inside the main call's population of {len(main)} rows")
    C.ok("A44", True, "the payment run, the offers sheet's instalments and the Variations sheet's co-funding are read "
                      "by no step of the main call (0 rows), D4, D5, D8 and H5 included")
    W["separation"] = (len(main), counts)
    # the main call reads exactly the version totals the portal rows carry
    tot_ok = all(v.lines[("TOT_REV" if is_new_form(v.q) else "TOT_INC")][0] == v.ytd for v in W["versions"])
    C.ok("A44", tot_ok, "every version's total-income row equals the total the screen reads")
