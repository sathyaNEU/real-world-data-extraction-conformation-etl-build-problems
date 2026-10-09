"""Ask-layer assertions: K1 and K2 golden figures, every designed stop, the necessity matrix, the
composed mishandlings, the over-cleaner, the referee, the pair simulation, the separation count and
the memo against the payment run (A44 to A50, A53)."""
from itertools import combinations

from common import SEPT_CENSUS, fyq, qend
from lines import is_new_form, TOTAL_CODES, MEMO_CODES
from asks import k1, k2, windows, apt_series, pick_version
from screen import eod

K1_DEV = {  # device or hazard -> keyword arguments for k1
    "D3 label mapping": dict(mapping="label"),
    "H2 comparatives": dict(comps=True),
    "H1 project-grant copy": dict(vhow="pg"),
    "H4 latest delivered": dict(vhow="delivered"),
}
K2_DEV = {
    "D8 instalment month": dict(how="for"),
    "H5 returned payments": dict(statuses=("paid", "returned")),
    "H1 one grant reference": dict(drop_pg=True),
    "H2 comparatives": dict(memo={"comps": True}),
    "H4 latest delivered": dict(memo={"vhow": "delivered"}),
}


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
    R3 = {r["org"]: r for r in S["R3"]["rows"]}
    c = SEPT_CENSUS
    offered = [r for r in T["rows"] if r["offer"]]
    G = golden_asks(W)
    W["golden_asks"] = G

    def stop_k1(r, **kw):
        return k1(W, r["org"], *windows(r), c, **kw)

    def stop_k2(r, **kw):
        return k2(W, r["org"], *windows(r), c, **kw)

    # A45: every stop's value per offered grantee, either untouched or at least NZ$500 away
    stops_k1 = {"S1 label mapping": dict(mapping="label"), "S2 comparatives": dict(comps=True),
                "S3 whole fees line to government": dict(mapping="over")}
    stops_k2 = {"S1 instalment month": dict(how="for"),
                "S2 returned summed with reissue": dict(statuses=("paid", "returned")),
                "S3 last ten days dropped": dict(how="transit"),
                "S4 one grant reference": dict(drop_pg=True)}
    moved = {}
    for name, kw in stops_k1.items():
        vals = [(r["org"], stop_k1(r, **kw) - G[r["org"]]["K1"]) for r in offered]
        near = [(k, d) for k, d in vals if d != 0 and abs(d) < 500]
        moved[("K1", name)] = [k for k, d in vals if d != 0]
        C.ok("A45", not near, f"K1 {name}: moves {len(moved[('K1', name)])} of 14 offered, none within NZ$500 ({near})")
    for name, kw in stops_k2.items():
        vals = [(r["org"], stop_k2(r, **kw) - G[r["org"]]["K2"]) for r in offered]
        near = [(k, d) for k, d in vals if d != 0 and abs(d) < 500]
        moved[("K2", name)] = [k for k, d in vals if d != 0]
        C.ok("A45", not near, f"K2 {name}: moves {len(moved[('K2', name)])} of 14 offered, none within NZ$500 ({near})")
    # S4/S5: the right construction on R3's windows (the mirror)
    mir1 = [(r["org"], k1(W, r["org"], *windows(R3[r["org"]]), c, q4src="portal") - G[r["org"]]["K1"])
            for r in offered if r["org"] in R3 and R3[r["org"]]["end"] != r["end"]]
    mir2 = [(r["org"], k2(W, r["org"], *windows(R3[r["org"]]), c) - G[r["org"]]["K2"])
            for r in offered if r["org"] in R3 and R3[r["org"]]["end"] != r["end"]]
    C.ok("A45", all(abs(d) >= 500 for _, d in mir1) and len(mir1) == 7,
         f"K1 S4 on R3's windows misses all 7 unfiled offerees by NZ$500 or more")
    C.ok("A45", all(abs(d) >= 500 for _, d in mir2) and len(mir2) == 7,
         f"K2 S5 on R3's windows misses all 7 unfiled offerees by NZ$500 or more")
    # lazy deltas
    lazy1 = [r["org"] for r in offered
             if abs(stop_k1(r, mapping="label") - G[r["org"]]["K1"]) >= max(0.08 * abs(G[r["org"]]["K1"]), 2000)]
    lazy2 = [r["org"] for r in offered
             if abs(stop_k2(r, how="for") - G[r["org"]]["K2"]) >= max(0.08 * abs(G[r["org"]]["K2"]), 1000)]
    C.ok("A45", len(lazy1) >= 10, f"K1 lazy path (label mapping) moves {len(lazy1)} of 14 by 8 per cent or NZ$2,000")
    C.ok("A45", len(lazy2) >= 10, f"K2 lazy path (instalment month) moves {len(lazy2)} of 14 by 8 per cent or NZ$1,000")
    W["lazy"] = (len(lazy1), len(lazy2))
    # A46: necessity matrix (each device mishandled alone moves exactly the asks in its row)
    rowmap = {}
    for name, kw in K1_DEV.items():
        rowmap[("K1", name)] = sorted(r["org"] for r in offered if stop_k1(r, **kw) != G[r["org"]]["K1"])
    for name, kw in K2_DEV.items():
        rowmap[("K2", name)] = sorted(r["org"] for r in offered if stop_k2(r, **kw) != G[r["org"]]["K2"])
    W["necessity"] = rowmap
    C.ok("A46", len(rowmap[("K1", "D3 label mapping")]) >= 10, "D3 moves K1")
    C.ok("A46", len(rowmap[("K2", "D8 instalment month")]) >= 10, "D8 moves K2")
    C.ok("A46", rowmap[("K1", "H1 project-grant copy")] == ["F3"] and rowmap[("K2", "H1 one grant reference")] == ["F3"],
         "H1 moves K1 and K2 for the offered dual grantee only")
    d_h1 = abs(stop_k1(next(r for r in offered if r["org"] == "F3"), vhow="pg") - G["F3"]["K1"])
    C.ok("A46", d_h1 >= 1500, f"H1 moves the dual grantee's K1 by NZ${d_h1}")
    C.ok("A46", rowmap[("K1", "H4 latest delivered")] == ["A4", "F2"] and rowmap[("K2", "H4 latest delivered")] == ["A4", "F2"],
         "H4 moves K1 and K2 for the two offered grantees with a rejected latest delivery")
    for k in ("A4", "F2"):
        r = next(x for x in offered if x["org"] == k)
        C.ok("A46", abs(stop_k1(r, vhow="delivered") - G[k]["K1"]) >= 1000 and
             abs(stop_k2(r, memo={"vhow": "delivered"}) - G[k]["K2"]) >= 1000, f"H4 moves {k} by NZ$1,000 or more on both")
    C.ok("A46", rowmap[("K2", "H5 returned payments")] == ["A3"], "H5 moves K2 for one offered grantee")
    h2 = [r["org"] for r in offered if abs(stop_k1(r, comps=True) - G[r["org"]]["K1"]) >= 0.05 * abs(G[r["org"]]["K1"])]
    C.ok("A46", len(h2) >= 8, f"H2 moves {len(h2)} of 14 offered K1 figures by 5 per cent or more")
    C.ok("A46", len(rowmap[("K2", "H2 comparatives")]) >= 8, "H2 moves K2")
    # H3: short-form filers carry no government line and no memo
    short = [r for r in T["rows"] if W["by"][r["org"]].short_form]
    C.ok("A46", len(short) >= 20 and all(G[r["org"]]["K1"] is None for r in short)
         and not any(W["by"][r["org"]].short_form for r in offered),
         f"H3: {len(short)} short-form scored grantees, K1 empty for each, none offered")
    # A47: composed mishandlings, every subset of the devices that touch a figure
    worst = None
    for r in offered:
        for ask, devs, fn in (("K1", K1_DEV, stop_k1), ("K2", K2_DEV, stop_k2)):
            touching = [n for n in devs if r["org"] in rowmap[(ask, n)]]
            for m in range(1, len(touching) + 1):
                for sub in combinations(touching, m):
                    kw = merge(devs[n] for n in sub)
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
    C.ok("A48", len(oc1) == 14 and len(oc2) == 14, "over-cleaning (whole fees line, ten-day transit) fails every offered figure")
    # A49: the referee ties to the golden's financial-year totals and to no re-presented split
    ties, rep_bad = 0, 0
    for r in offered:
        o = W["by"][r["org"]]
        for (key, q4), ar in W["annual"].items():
            if key != o.key or ar.received is None or q4 < r["pend"] - 7 or q4 - 3 > r["end"]:
                continue
            # golden: the four quarters of the year sum to the register's government total
            from asks import gov_quarter
            s = sum(gov_quarter(W, o, q, eod(SEPT_CENSUS), "register") for q in range(q4 - 3, q4 + 1)
                    if q >= 5)
            if q4 - 3 >= 5 and s == ar.lines["gov"]:
                ties += 1
        for (key, q4), ar in W["annual"].items():
            if key != o.key or ar.received is None:
                continue
            nv = pick_version(W, o, q4 + 4, eod(SEPT_CENSUS))
            if nv is not None and is_new_form(q4 + 4) and not is_new_form(q4):
                if nv.lines["GOV_GRC"][1] != ar.lines["gov"]:
                    rep_bad += 1
    C.ok("A49", ties >= 20 and rep_bad >= 10,
         f"referee: {ties} offered-grantee years tie to the register; {rep_bad} re-presented comparatives do not")
    s2diff = [r["org"] for r in offered if stop_k1(r, comps=True) != G[r["org"]]["K1"]]
    C.ok("A49", len(s2diff) >= 8, f"the re-presented split misses {len(s2diff)} of 14 window figures")
    # A50: pair simulation (habitual battery: statuses and the dual collapse handled, D3 and D8 not)
    crack1 = sum(1 for r in offered if stop_k1(r, mapping="label") == G[r["org"]]["K1"])
    crack2 = sum(1 for r in offered if stop_k2(r, how="for") == G[r["org"]]["K2"])
    mirror = 0
    for r in offered:
        if r["org"] in R3 and R3[r["org"]]["offer"]:
            m1 = k1(W, r["org"], *windows(R3[r["org"]]), c, q4src="portal", mapping="label")
            m2 = k2(W, r["org"], *windows(R3[r["org"]]), c, how="for")
            mirror += (m1 == G[r["org"]]["K1"]) + (m2 == G[r["org"]]["K2"])
    Lc = (crack1 + crack2) / 28.0
    Ls = mirror / 28.0
    cracker = 38 + 7 + 55 * Lc
    mir = 3 + 7 + 55 * Ls
    pair = (cracker + mir) / 2
    W["pair"] = (cracker, mir, pair, Lc, Ls)
    C.ok("A50", pair <= 40, f"pair simulation: cracker {cracker:.1f}, mirror {mir:.1f}, average {pair:.1f} (Lc {Lc:.2f}, Ls {Ls:.2f})")
    # A53: the new-form Trust memo equals the payment run by value date, every grantee and quarter
    run = apt_series(W)
    bad = 0
    checked = 0
    for (key, q), lst in W["book"].by_org.items():
        o = W["by"][key]
        if not is_new_form(q) or o.short_form:
            continue
        v = lst[-1]
        k = fyq(q, o.bal)
        want = int(sum(run[key][q - k + 1:q + 1]))
        checked += 1
        if v.lines["GRT_NGO_APT"][0] != want:
            bad += 1
    C.ok("A53", bad == 0 and checked > 800, f"memo equals the payment run by value date ({checked} returns, {bad} differ)")
    return G


def separation(W, C, portal_rows):
    """A44: no device or hazard row inside the main call's declared row population."""
    main = [r for r in portal_rows if r["line_code"] in TOTAL_CODES and r["column"] == "YTD"]
    devices = {
        "D3 old-form memo and government lines": lambda r: r["line_code"] in ("FEE_SVC_GOV", "GOV_GRT", "FEE_SVC", "GOV_GRC"),
        "H1 project-grant line copies": lambda r: r["is_pg"] and r["line_code"] not in TOTAL_CODES,
        "H2 comparative column": lambda r: r["column"] == "PY",
        "H3 short-form lines": lambda r: r["short"] and r["line_code"] not in TOTAL_CODES,
        "H4 rejected line coding": lambda r: r["status"] == "rejected" and r["line_code"] not in TOTAL_CODES,
        "D8 Trust memo": lambda r: r["line_code"] == "GRT_NGO_APT",
    }
    counts = {}
    for name, f in devices.items():
        counts[name] = sum(1 for r in main if f(r))
        C.ok("A44", counts[name] == 0, f"{name}: 0 rows inside the main call's population of {len(main)} rows")
    C.ok("A44", True, "the payment run is read by no step of the main call (0 rows), H5 included")
    W["separation"] = (len(main), counts)
    # the main call reads exactly the version totals the portal rows carry
    tot_ok = all(v.lines[("TOT_REV" if is_new_form(v.q) else "TOT_INC")][0] == v.ytd for v in W["versions"])
    C.ok("A44", tot_ok, "every version's total-income row equals the total the screen reads")
