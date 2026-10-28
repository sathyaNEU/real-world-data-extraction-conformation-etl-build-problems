"""task275 checks: the build's assertions, run on every build (python3 build.py)."""
from __future__ import annotations

import collections
import copy
import os
import re
import shutil

import analysis as A
import asks as AS
import common as K
import pack as PK
import records as R
import world as W

FAILS = []
GOLDEN_SET = ("TR1", "TR2", "NEP", "BT")


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (": " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def whole(g):
    return {s: int(round(g[s])) for s in K.SEG}


def match_by_date(target, local=True):
    """observed trips matched to the logbook on the vessel as typed (normalised) and the departure date alone"""
    T, _ = PK.trip_records(target, local=local)
    for x in T:
        for k in ("obs_mk", "obs_bms", "obs_dis", "obs_hours_s", "obs_unw_s", "obs_mk_s"):
            x.pop(k, None)
        x["observed"] = False
    obs = {}
    for r in PK.rows(target, "hauls"):
        o = obs.setdefault(r["observer_trip_ref"], dict(RET=0.0, BMS=0.0, DIS=0.0, hours={}))
        o[r["fraction"]] += float(r["weight_kg"])
        o["hours"][r["haul_no"]] = (PK.parse(r["hauled_local"]) - PK.parse(r["shot_local"])).total_seconds() / 3600
    byv = collections.defaultdict(list)
    for x in T:
        byv[x["pln"]].append(x)
    miss = 0
    for r in PK.rows(target, "deploy"):
        if r["outcome"] != "Observed":
            continue
        d = PK.parse(r["notified_departure"]).date()
        c = [x for x in byv[PK.norm_pln(r["vessel_pln"])] if x["dep_local"].date() == d and not x["observed"]]
        if not c:
            miss += 1
            continue
        o = obs[r["observer_trip_ref"]]
        c[0].update(observed=True, obs_mk=o["RET"], obs_bms=o["BMS"], obs_dis=o["DIS"],
                    obs_hours_s=sum(o["hours"].values()), obs_unw_s=o["BMS"] + o["DIS"], obs_mk_s=o["RET"])
    return T, miss


def run(task, b, fig, res):
    del FAILS[:]
    target = os.path.join(task, "target")
    rc = b["rc"]
    w = rc.w
    T = res["T"]
    g = res["shares"]
    des = tuple(fig["call"]["designated"])
    print("== task275 checks")

    # ---------------------------------------------------------------- the call
    check("CALL the golden designates TR1, TR2, NEP and BT", des == GOLDEN_SET, str(des))
    check("CALL every observed deployment matched to a logbook trip", not res["unmatched"],
          "%d unmatched" % len(res["unmatched"]))
    n_obs_world = sum(t["observed"] for t in w["T"])
    check("CALL observed trips read back equal the world's", sum(t["observed"] for t in T) == n_obs_world,
          "%d of %d" % (sum(t["observed"] for t in T), n_obs_world))
    tr = W.truth(w)
    check("TRUTH the world's discard shares name the golden set", A.designated(tr) == des,
          " ".join("%s %.2f" % (s, tr[s]) for s in K.SEG))
    check("TRUTH the golden's whole per cent is the world's within one point",
          all(abs(round(g[s]) - tr[s]) <= 1.0 for s in K.SEG),
          " ".join("%s %d/%.2f" % (s, round(g[s]), tr[s]) for s in K.SEG))

    # ---------------------------------------------------------------- family and margins
    fam = res["fam"]
    sets = {A.designated(x) for x in fam.values()}
    check("FAMILY every licensed construction names the golden set (%d members)" % len(fam), sets == {des},
          str(sets))
    agree = {s: sorted({int(round(x[s])) for x in fam.values()}) for s in K.SEG}
    check("FAMILY every segment's share agrees to the whole per cent across the family",
          all(len(v) == 1 for v in agree.values()), str(agree))
    check("FAMILY the golden's whole per cent is the family's", all(agree[s] == [int(round(g[s]))] for s in K.SEG))
    m = A.margin(fam)
    check("MARGIN every segment in every member at least 1.5 points from the line", m >= 1.5, "%.2f" % m)
    spread = max(max(x[s] for x in fam.values()) - min(x[s] for x in fam.values()) for s in K.SEG)
    check("FAMILY spread under one point on every segment", spread < 1.0, "%.2f" % spread)

    # ---------------------------------------------------------------- the ladder
    Rt = res["routes"]
    want = {"R0 the logbooks' declared discards": (),
            "R1 the observed trips' discard share": ("NEP",),
            "R2 the observed discards per hour by ground, raised (default path)": ("NEP",),
            "R3 the observed trips' unwanted share": ("TR1", "TR2", "NEP", "GN"),
            "R4 unwanted catch per hour, grounds pooled": ("TR1", "TR2", "NEP"),
            "R5 unwanted catch per hour by ground, declared BMS not netted": ("TR1", "TR2", "NEP", "BT", "GN")}
    for k, v in want.items():
        check("LADDER %s files %s" % (k, ",".join(v) or "none"), A.designated(Rt[k]) == v,
              str(A.designated(Rt[k])))
        check("LADDER %s is not the golden set" % k.split(" ")[0], A.designated(Rt[k]) != des)
    check("LADDER R2b observed discards raised by landings files NEP", A.designated(res["r2b"]) == ("NEP",))
    r2 = Rt["R2 the observed discards per hour by ground, raised (default path)"]
    check("LADDER the default path leaves TR1, TR2 and BT 5 points or more under the line",
          all(r2[s] <= 5.0 for s in ("TR1", "TR2", "BT")), " ".join("%s %.1f" % (s, r2[s]) for s in K.SEG))

    # ---------------------------------------------------------------- the three rules on the clean truth
    clean = W.analysis_trips(w)
    cR = A.routes(clean)
    check("R3a ANALYST the easy route (observer discards raised by ground) on the clean truth files NEP alone",
          A.designated(cR["R2 the observed discards per hour by ground, raised (default path)"]) == ("NEP",))
    check("R3a ANALYST raised by landings on the clean truth files NEP alone",
          A.designated(A.ratio_to_landings(clean)) == ("NEP",))
    cg = A.golden(clean)
    check("R3b DECISIVE the easy route with the decisive step alone files the golden set on the clean truth",
          A.designated(cg) == des)
    check("R3b each lower rung's single correction leaves a wrong set (pooled grounds; BMS not netted)",
          A.designated(cR["R4 unwanted catch per hour, grounds pooled"]) != des and
          A.designated(cR["R5 unwanted catch per hour by ground, declared BMS not netted"]) != des)
    shipped_cols = []
    for k, f in K.FILES.items():
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                shipped_cols += [(f, c) for c in fh.readline().strip().split(",")]
    bad = [c for c in shipped_cols if re.search(r"share|rate|ratio|estimate|raised|unobserved", c[1], re.I)]
    check("R1 no shipped column holds a discard share, rate or estimate", not bad, str(bad))
    check("R1 the field's raw material ships: observer hauls by species and fraction, every trip's hours and "
          "ground, every landing declaration", all(os.path.exists(PK.path(target, k))
                                                    for k in ("hauls", "trips", "landings", "deploy")))

    # R2: each Layer 1 item mishandled leaves the call and every whole-per-cent share
    orig = PK.norm_pln
    PK.norm_pln = lambda s: s.strip()
    T1, un1 = PK.trip_records(target)
    PK.norm_pln = orig
    g1 = A.golden(T1)
    check("R2 LAYER1 port letters and numbers as typed (%d observed trips unmatched): same call and shares" % len(un1),
          A.designated(g1) == des and whole(g1) == whole(g), str(whole(g1)))
    T2, m2 = match_by_date(target, local=True)
    g2 = A.golden(T2)
    check("R2 LAYER1 matched on the UK departure date (%d unmatched): same call and shares" % m2,
          A.designated(g2) == des and whole(g2) == whole(g), str(whole(g2)))
    T3, m3 = match_by_date(target, local=False)
    g3 = A.golden(T3)
    check("R2 LAYER1 matched on the logbook's UTC date (%d unmatched): same call and shares" % m3,
          A.designated(g3) == des and whole(g3) == whole(g), str(whole(g3)))
    T5, _ = PK.trip_records(target, raise_hauls=False)
    g5 = A.golden(T5)
    unatt = sum(int(r["hauls_sampled"]) < next(t["nhauls"] for t in T if t.get("obs_ref") == r["observer_trip_ref"])
                for r in PK.rows(target, "deploy") if r["outcome"] == "Observed")
    check("R2 LAYER1 hauls the observer missed (%d observed trips) left unraised: same call and shares" % unatt,
          A.designated(g5) == des and whole(g5) == whole(g), str(whole(g5)))
    byv = collections.defaultdict(list)
    for t in T:
        byv[t["pln"]].append(t["dep_local"])
    canc = [r for r in PK.rows(target, "deploy") if r["outcome"] == "Trip cancelled"]
    near = sum(1 for r in canc if any(abs((d - PK.parse(r["notified_departure"])).total_seconds()) <= 12 * 3600
                                      for d in byv[PK.norm_pln(r["vessel_pln"])]))
    check("R2 LAYER1 no cancelled draw (%d) lies within 12 hours of a logbook departure of its vessel" % len(canc),
          near == 0, str(near))

    # ---------------------------------------------------------------- semantic forks
    # SF1 catch with or without the landed BMS
    parts = A.golden_parts(T)
    alt1 = {s: 100 * parts[s][0] / (parts[s][1] - sum(t["land_bms"] for t in T if t["seg"] == s)) for s in K.SEG}
    check("SF1 catch counts the landed BMS (terms 3.1); leaving it out keeps the call", A.designated(alt1) == des,
          str(A.designated(alt1)))
    dis_all = sum(float(r["weight_kg"]) for r in PK.rows(target, "hauls") if r["fraction"] == "DIS")
    check("SF2 discards are every species returned (terms 3.2): the golden's observed discards are every DIS row",
          abs(sum(t["obs_dis"] for t in T5 if t["observed"]) - dis_all) < 0.5)
    dep_years = collections.Counter((PK.parse(r["departure_utc"]).year, K.to_local(PK.parse(r["departure_utc"])).year)
                                    for r in PK.rows(target, "trips"))
    check("SF3 trips begun in 2025: UTC and UK departure years agree for every trip (same call)",
          set(dep_years) == {(2025, 2025)}, str(dep_years))
    reg = PK.register(target)
    gear_seg = collections.defaultdict(set)
    for r in PK.rows(target, "trips"):
        gear_seg[(r["gear"], reg[r["vessel_pln"]]["segment"])].add(r["vessel_pln"])
    check("SF4 a vessel's segment from the register; every trip's gear agrees with it (same call)",
          all(R.GEAR[seg] == gear for gear, seg in gear_seg))
    check("SF5 observed trips matched by vessel and notified departure, within 12 hours, on the UK date or on the "
          "UTC date: same call", A.designated(g2) == des and A.designated(g3) == des)
    outcomes = collections.Counter(r["outcome"] for r in PK.rows(target, "deploy"))
    check("SF6 drawn trips with no observer and cancelled draws are not observed trips (same call)",
          sum(t["observed"] for t in T) == outcomes["Observed"], str(dict(outcomes)))
    by_aux = {k: A.designated(v) for k, v in fam.items() if k.startswith("ground/") and k.endswith("/decl")}
    check("SF7 raising by hours, hauls, trips or landings: same call", set(by_aux.values()) == {des}, str(by_aux))
    check("SF8 strata by ground or by ground and half-year: same call",
          {A.designated(v) for k, v in fam.items() if k.startswith("ground_half")} == {des})
    check("SF9 observed trips' kept catch from the landing declaration or the observer's RET: same call",
          {A.designated(v) for k, v in fam.items() if "/obs" in k} == {des})
    gb = {gr[0]: gr for gr in K.GROUNDS}
    trip_of = {t["obs_ref"]: t for t in T if t["observed"]}
    outside = 0
    for r in PK.rows(target, "hauls"):
        gr = gb[trip_of[r["observer_trip_ref"]]["ground"]]
        la, lo = float(r["shot_lat"]), float(r["shot_lon"])
        if not (abs(la - gr[5][0]) <= gr[6][0] and abs(lo - gr[5][1]) <= gr[6][1]):
            outside += 1
    check("SF10 the ground from the logbook or from the observer's shot positions: every observed haul lies in its "
          "trip's ground (same call)", outside == 0, "%d haul rows outside" % outside)
    check("SF11 more than 10 per cent or at least 10 per cent: no segment within 1.5 points (same call)", m >= 1.5)
    # SF12 an observed trip's weighings raised from the hauls sampled to its hours fished (the manual's section 3 and
    # the deployment log's hauls_sampled: the haul records hold the hauls sampled)
    Tu, _ = PK.trip_records(target, raise_hauls=False)
    famu = A.family(Tu)
    whole_r = {s: sorted({int(round(g[s])) for g in fam.values()}) for s in K.SEG}
    check("SF12 sampled hauls raised to the trip: every member holds the golden's whole per cent; summed as sampled "
          "the call holds", all(whole_r[s] == [fig["segments"][s]["share"]] for s in K.SEG) and
          {A.designated(g) for g in famu.values()} == {des},
          "as sampled TR1 %.2f to %.2f" % (min(g["TR1"] for g in famu.values()), max(g["TR1"] for g in famu.values())))
    # SF13 the raising variable is one an observer does not change: marketable landings give the golden's whole per
    # cent; total landed weight with the BMS (which the observed trips land twelve times as fast) keeps the call
    mk = fam["ground/mk/decl"]
    for t in T:
        t["landed_all"] = t["land_mk"] + t["land_bms"]
    A_aux = A._aux
    A._aux = lambda t, aux, observed: t["landed_all"] if aux == "all" else A_aux(t, aux, observed)
    try:
        allw = A.golden(T, aux="all")
    finally:
        A._aux = A_aux
    check("SF13 raised by marketable landings, every segment's whole per cent is the golden's; by landed weight with "
          "the BMS, the same call", all(int(round(mk[s])) == fig["segments"][s]["share"] for s in K.SEG) and
          A.designated(allw) == des, " ".join("%s %.2f/%.2f" % (s, mk[s], allw[s]) for s in K.SEG))
    # SF14 the raising basis never moves the call: the observers' discards alone name NEP however they are raised
    r2 = res["routes"]["R2 the observed discards per hour by ground, raised (default path)"]
    check("SF14 the observers' discards raised by hours or by landed weight name NEP alone; the golden's family "
          "names the four by every raising variable", A.designated(r2) == A.designated(res["r2b"]) == ("NEP",) and
          tuple(fig["default_path_by_landed_weight_designated"]) == ("NEP",) and set(by_aux.values()) == {des},
          "by landed weight %s" % " ".join("%s %.2f" % (s, res["r2b"][s]) for s in ("TR1", "TR2", "NEP", "BT")))
    # SF15 a VMS report's vessel is the one carrying its terminal (terms 4.2, its reports); the extract names the
    # last vessel a terminal was fitted to (the dictionary), under which the moved terminals' second vessels report
    # from two terminals at once
    nv, nh, na = AS.two_terminal_hours(target)
    check("SF15 under the extract's names %d vessels report from two terminals in the same UTC hour (%d hours, %d of "
          "them with the nearest pair more than %d nm apart): the moved terminals' second vessels, each terminal one "
          "vessel's previous and another's current in the equipment record" % (nv, nh, na, K.APART_NM),
          nv == len(rc.moves) and na > nh / 2 and fig["vms_two_terminals"] == {
              "vessels": nv, "vessel_hours": nh, "apart_nm": K.APART_NM, "apart_hours": na})
    from pypdf import PdfReader
    pdf = lambda k: " ".join(" ".join(p.extract_text() for p in PdfReader(os.path.join(target, K.FILES[k])).pages).split())
    check("COUNTERPIN the manual says nothing of how the crew sort the catch with an observer aboard",
          "normally" not in pdf("manual") and "takes no part in sorting" in pdf("manual"))

    # ---------------------------------------------------------------- evidence the decisive step rests on
    bms = res["bms"]
    for s in ("TR1", "TR2", "NEP", "BT", "SN"):
        cells = [(k, v) for k, v in bms.items() if k[0] == s and v[0] > 0]
        check("EVIDENCE %s: observed trips declare at least five times the BMS an hour of unobserved trips on every "
              "ground" % s, all(v[0] >= 5 * v[1] for k, v in cells),
              " ".join("%s %.2f/%.2f" % (k[1], v[0], v[1]) for k, v in cells))
    gn = [v for k, v in bms.items() if k[0] == "GN"]
    check("EVIDENCE GN: most gillnetters land their BMS every trip (observed under three times unobserved)",
          all(v[0] < 3 * v[1] for v in gn))
    par = {s: (fig["segments"][s]["marketable_kg_per_hour_observed"], fig["segments"][s]["marketable_kg_per_hour_unobserved"])
           for s in K.SEG}
    check("EVIDENCE every segment's observed and unobserved trips land the same marketable catch an hour (within 7 per "
          "cent), so the hauls bring aboard alike", all(abs(o / u - 1) < 0.07 for o, u in par.values()),
          " ".join("%s %.1f/%.1f" % (s, o, u) for s, (o, u) in par.items()))
    nur = res["grounds"]
    check("EVIDENCE BT: observed beam trawl trips fish WC14 and WC15 less (deployment effect)",
          nur[("BT", True)]["WC14"] + nur[("BT", True)]["WC15"] <
          nur[("BT", False)]["WC14"] + nur[("BT", False)]["WC15"] - 0.15)

    # ---------------------------------------------------------------- separation: the asks' files and devices
    scratch = os.path.join(task, "_sep_check")
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    shutil.copytree(target, scratch)
    for k in ("sales", "vms", "transponders", "ports", "quota", "gear"):
        os.remove(PK.path(scratch, k))
    Ts, _ = PK.trip_records(scratch)
    shutil.rmtree(scratch)
    check("SEPARATION the call is unchanged with the asks' files and the distractors deleted",
          A.golden(Ts) == g)
    cp, over = AS.copies(target)
    n_copy_lines = sum(len(n["lines"]) for n in rc.sales() if n["copy"])
    rows_s = PK.sales(target)
    copy_notes = {n["no"] for n in rc.sales() if n["copy"]}
    found = {rows_s[i]["sales_note_no"] for i in cp}
    check("ASK A DEVICE the lines within 3 per cent of a market lot are exactly the merchant's records of its market "
          "purchases (%d lines)" % n_copy_lines, len(cp) == n_copy_lines and found == copy_notes,
          "%d found, %d filed" % (len(cp), n_copy_lines))
    gaps = []
    mkt = AS.market_buyers(target)
    lots = collections.defaultdict(list)
    for r in rows_s:
        if r["port_of_landing"] in mkt and r["buyer_reg_no"] == mkt[r["port_of_landing"]]:
            lots[AS._lot_key(r)].append(float(r["weight_kg"]))
    for i in over - cp:
        w = float(rows_s[i]["weight_kg"])
        gaps.append(min(abs(w - m) / m for m in lots[AS._lot_key(rows_s[i])]))
    check("ASK A DEVICE the quay's private sales on market lots differ from the lot by 20 per cent or more (%d lines)"
          % len(gaps), gaps and min(gaps) >= 0.2, "closest %.3f" % (min(gaps) if gaps else -1))
    check("ASK A DEVICE no merchant record repeats a market lot exactly", not AS.exact_repeats(target))
    check("ASK A DEVICE the lot key finds the same lines with or without the grade",
          AS.copy_rows(target, grade=False) == cp, "%d without the grade, %d with"
          % (len(AS.copy_rows(target, grade=False)), len(cp)))
    check("SEPARATION the merchant's records sit in the sales notes only, a file the call never opens", True)

    # ---------------------------------------------------------------- asks: golden equals the world's truth
    notes = rc.sales()
    truth_a = collections.Counter()
    for n in notes:
        if n["copy"] or n["L"]["when"].year != 2025:
            continue
        truth_a[rc.V[n["L"]["v"]]["seg"]] += sum(l[5] for l in n["lines"])
    ga = fig["segments"]
    check("ASK A the golden first-sale values are the world's sales of 2025 landings",
          all(abs(ga[s]["first_sale_gbp_thousands"] - round(truth_a[s] / 1000.0, 1)) < 1e-6 for s in K.SEG),
          " ".join("%s %.1f/%.1f" % (s, ga[s]["first_sale_gbp_thousands"], truth_a[s] / 1000.0) for s in K.SEG))
    lim = [(p[3], p[4]) for p in K.PORTS]
    days = collections.defaultdict(set)
    for u, when, la, lo, sp, crs, vi in rc.pings():
        if any(R.nm((la, lo), c) <= rad for c, rad in lim):
            continue
        d = K.to_local(when).date()
        if d.year == K.YEAR:
            days[vi].add(d)
    truth_b = collections.Counter()
    for vi, ds in days.items():
        truth_b[rc.V[vi]["seg"]] += len(ds)
    check("ASK B the golden days at sea are the world's (each report on the vessel that sent it)",
          all(ga[s]["days_at_sea"] == truth_b[s] for s in K.SEG),
          " ".join("%s %d/%d" % (s, ga[s]["days_at_sea"], truth_b[s]) for s in K.SEG))
    ra = AS.ask_a_routes(target)
    for k, v in ra.items():
        check("ASK A route %s misses every segment by 0.1 or more" % k,
              all(abs(round(v[s], 1) - ga[s]["first_sale_gbp_thousands"]) >= 0.1 for s in K.SEG))
    rb = AS.ask_b_routes(target)
    for k, v in rb.items():
        check("ASK B route %s misses every segment" % k, all(v[s] != ga[s]["days_at_sea"] for s in K.SEG))
    moved = {rc.V[mv["P"]]["seg"] for mv in rc.moves} | {rc.V[mv["Q"]]["seg"] for mv in rc.moves}
    check("ASK B the moved terminals touch every segment", moved == set(K.SEG), str(sorted(moved)))
    # the PO's equipment record: the vessel that carried each report's terminal is recovered without a date, and the
    # agreement a solver checks (the named vessel holds the terminal as its own or its previous one) passes every row
    who, between = AS.owners(target)
    hold = AS.holders(target)
    wrong = agree = 0
    pl = {v["idx"]: v["pln"] for v in rc.V}
    by_key = {(u, when.strftime("%Y-%m-%d %H:%M")): vi for u, when, la, lo, sp, crs, vi in rc.pings()}
    for r in PK.vms(target):
        t = PK.parse(r["position_utc"])
        wrong += who(r["terminal_id"], t) != pl[by_key[(r["terminal_id"], r["position_utc"])]]
        agree += r["vessel_pln"] in {p for role, p in hold.get(r["terminal_id"], [])}
    n_vms = len(PK.vms(target))
    check("ASK B DEVICE the equipment record gives every report the vessel that sent it (%d wrong, %d between)"
          % (wrong, between[0]), wrong == 0 and between[0] == 0)
    check("ASK B DEVICE the extract's vessel holds the report's terminal in the record on every row (%d of %d)"
          % (agree, n_vms), agree == n_vms)
    two = [u for u, hs in hold.items() if len(hs) == 2]
    check("ASK B DEVICE the record lists exactly the moved terminals on two vessels (%d)" % len(two),
          sorted(two) == sorted(mv["unit"] for mv in rc.moves))
    seen_u = {r["terminal_id"] for r in PK.vms(target)}
    benign = [r for r in PK.transponders(target) if r["previous_terminal_id"]
              and r["previous_terminal_id"] not in seen_u]
    in_year = [r for r in PK.transponders(target) if r["previous_terminal_id"] in seen_u]
    check("ASK B DEVICE previous terminals are common texture: %d vessels list one that sent no 2025 report, %d one "
          "that did" % (len(benign), len(in_year)), len(benign) >= 30 and len(benign) > len(in_year))

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(target))
    exts = {os.path.splitext(f)[1] for f in files}
    check("GATE 10 or more files", len(files) >= 10, str(len(files)))
    check("GATE 3 or more formats", len(exts) >= 3, str(sorted(exts)))
    big = max(b["counts"].values())
    check("GATE a file of 25,000 rows or more", big >= 25000, str(big))
    check("GATE two or more distractors", len(K.DISTRACTORS) >= 2)
    check("GATE no file named after the trap", not any(re.search(r"observer_effect|bms_gap|unobserved|discard_est", f)
                                                    for f in files))
    per_seg = [fig["segments"][s]["trips"] for s in K.SEG]
    check("REALISM no two segments with the same trip count", len(set(per_seg)) == len(per_seg))
    vals = [fig["segments"][s]["first_sale_gbp_thousands"] for s in K.SEG]
    check("REALISM no round first-sale totals", all(abs(v - round(v, -1)) > 0.05 for v in vals))
    flat = []
    for s in K.SEG:
        rat = []
        for gi in range(5):
            O = [t for t in rc.w["T"] if t["seg"] == s and t["observed"] and t["ground"] == gi]
            if len(O) >= 5:
                rat.append(sum(t["legal"] for t in O) / sum(t["mk"] + t["bms"] for t in O))
        if len(rat) >= 2 and max(rat) / min(rat) < 1.2:
            flat.append("%s %.2f" % (s, max(rat) / min(rat)))
    check("REALISM the observed trips' lawful discards differ across each segment's grounds (1.2 times or more)",
          not flat, " ".join(flat))
    names = [v["name"] for v in rc.V]
    check("REALISM vessel names unique", len(set(names)) == len(names))
    plns = [v["pln"] for v in rc.V]
    check("REALISM port letters and numbers unique", len(set(plns)) == len(plns))
    lines = PK.rows(target, "hauls")
    blocks = collections.Counter(tuple(r[c] for c in ("species", "fraction", "weight_kg")) for r in lines
                                 if float(r["weight_kg"]) >= 5.0)
    top = blocks.most_common(1)[0][1]
    check("REALISM no observer weight of 5 kg or more repeated beyond chance (most common species, fraction and "
          "weight %d times)" % top, top <= 60)
    near = 0
    for r in PK.vms(target):
        la, lo = float(r["latitude"]), float(r["longitude"])
        near += any(abs(R.nm((la, lo), c) - rad) < 0.03 for c, rad in lim)
    check("ASK B no shipped report within 0.03 nm of a port limit", near == 0, str(near))
    text = "".join(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
                   for f in files if f.endswith((".txt", ".csv")) and os.path.getsize(os.path.join(target, f)) < 2e5)
    check("REALISM no em dash in any text file", "—" not in text)
    print("== %d failed" % len(FAILS))
    return 1 if FAILS else 0
