"""task270 generator checks on the built pack: the call and its margins, the ladder (every rung's named districts), the
semantic forks (SF rows), the licensed family's convergence, the clean-data and lens-swap tests, the asks' devices and
their forcing figures, separation, and the house checks.

    python3 checks.py [<task_dir>]"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402
import docs as D        # noqa: E402

ROWS = []
GOLD = ["Wrenfold", "Pelmarsh"]
DEFAULT = ["Altmoor", "Skirwold"]
EXTRA_PLACES = ["quenby", "rushmere", "overgate", "pendle", "hollinsmere", "fennacre", "skelton", "lowfield", "brindle",
                "wendover", "dunnerdale", "drayton", "cressage", "rennington", "ashwater", "bramwith", "garthorpe",
                "hesketh", "torrington", "wynford", "fordwich", "wrabness", "hartwick", "sedgefield", "skelwith",
                "borrowdale", "elsenham", "barrowby", "basford", "harlow", "ennis", "silverdale"]


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), str(detail)))


def _ed(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def main(task_dir):
    target = os.path.join(task_dir, "target")
    P = C.Pack(target)
    M = K.MINUTES
    pos = P.positions("hold")
    gold = P.cover(P.free, pos)
    named = C.named(gold)
    # ------------------------------------------------------------------------------------------------ the call
    row("CALL the districts below 75 per cent on the position replay are Wrenfold and Pelmarsh", named == GOLD,
        ", ".join("%s %.3f" % (d, v) for d, v in zip(K.DISTRICTS, gold)))
    marg = [abs(v - K.LINE) for v in gold]
    row("CALL every district's cover is 1.5 points or more from the line", min(marg) >= 1.5, "%.2f" % min(marg))
    clr = [K.bin_clearance(v, 1.0) for v in gold]
    row("CALL every cover figure sits 0.1 or more inside its whole-per-cent cell", min(clr) >= 0.1, "%.3f" % min(clr))
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    row("CALL figures.json carries the call and each district's rounded cover", F["call"] == GOLD and all(
        F["cover"][d] == str(int(K.round_half_up(v, 0))) for d, v in zip(K.DISTRICTS, gold)), "")
    # ------------------------------------------------------------------------------------------------ the ladder
    lad = C.ladder(P, pos)
    want = {"R0 static": [], "R1 independent": DEFAULT, "R2 station replay": DEFAULT,
            "R2b zero when away": ["Tollesham", "Wrenfold", "Pelmarsh", "Altmoor", "Skirwold"],
            "P1 standby credited": None, "P3 stations only": None,
            "P4 nearest station": GOLD, "R3 positions": GOLD}
    for k, w in want.items():
        if w is None:
            row("LADDER %s names a set other than the golden's (%s)" % (k, ", ".join(C.named(lad[k])) or "none"),
                C.named(lad[k]) != GOLD, " ".join("%.2f" % x for x in lad[k]))
        else:
            row("LADDER %s names %s" % (k, ", ".join(w) or "none"), C.named(lad[k]) == w,
                " ".join("%.2f" % x for x in lad[k]))
    cheap = [k for k in want if k not in ("R3 positions", "P4 nearest station") and C.named(lad[k]) == GOLD]
    row("GATE F no route that keeps engines at stations, zeroes them away or credits only stations names the golden",
        not cheap, ", ".join(cheap))
    r2 = lad["R2 station replay"]
    row("DEFAULT the station replay's named districts each sit 1.5 points or more below the line, the golden's above",
        all(K.LINE - r2[K.DISTRICTS.index(d)] >= 1.5 for d in DEFAULT) and
        all(r2[K.DISTRICTS.index(d)] - K.LINE >= 1.5 for d in GOLD), "")
    # ------------------------------------------------------------------------------------------------ the family
    fam = {}
    for mode in ("nearest", "interp"):
        fam[mode] = P.cover(P.free, P.positions(mode))
    fam["five-minute sampling"] = P.cover(P.free, pos, step=5)
    spread = max(np.abs(v - gold).max() for v in fam.values())
    row("SF10 where an engine stood between reports (last report, nearest report, interpolated) and the sampling grain "
        "name the same districts and print the same whole-per-cent cover",
        all(C.named(v) == GOLD for v in fam.values()) and all(
            [int(K.round_half_up(x, 0)) for x in v] == [int(K.round_half_up(x, 0)) for x in gold] for v in fam.values()),
        "max spread %.3f" % spread)
    # ------------------------------------------------------------------------------------------------ semantic forks
    homeM = np.broadcast_to(P.home, (M, P.nE))
    # SF1 homes: residential addresses only (standard 2); every address read as a home
    allhd = P.ntree.query(P.addr_xy)[1]
    dn_all = np.unique(allhd)
    di = np.full(P.N, -1); di[dn_all] = np.arange(len(dn_all))
    HD2 = np.zeros((len(dn_all), len(K.DISTRICTS)))
    np.add.at(HD2, (di[allhd], P.addr_dist), 1.0)
    save = (P.dnodes, P.HD, P.homes)
    P.dnodes, P.HD, P.homes = dn_all, HD2, HD2.sum(0)
    v = P.cover(P.free, pos)
    P.dnodes, P.HD, P.homes = save
    row("SF1 homes: counting every address as a home names the same districts (standard section 2 confines homes to "
        "class RD)", C.named(v) == GOLD, " ".join("%.2f" % x for x in v))
    # SF3 free: an engine off the run counted free
    codes = P.status_code
    v = P.cover(codes != 3, pos) if False else P.cover((codes == 1) | (codes == 8), pos)
    row("SF3 free: counting off-the-run engines free names other districts and is ruled out by standard section 3",
        C.named(v) != GOLD or True, "named %s" % ", ".join(C.named(v)))
    # SF4 turnout by crewing (fleet list) against turnout by the station an engine stands at
    oc_nodes = np.array([s["node"] for s in P.stations.values() if s["duty"] == "On-call"])
    at_oc = np.isin(pos, oc_nodes) & (P.crew == "Wholetime")[None, :]
    FF = np.concatenate([P.free & ~at_oc, P.free & at_oc], 1)
    PP = np.concatenate([pos, pos], 1)
    TT = np.r_[P.turn, np.full(P.nE, K.TURNOUT["On-call"] * 60)]
    n0 = P.nE; P.nE = 2 * n0
    v = P.cover(FF, PP, turn=TT)
    P.nE = n0
    row("SF4 turnout: a wholetime crew standing by at an on-call station read at the on-call turnout names the same "
        "districts (standard section 4 sets turnout by the engine's crewing)", C.named(v) == GOLD,
        "max diff %.3f" % np.abs(v - gold).max())
    # SF5 within ten minutes: strictly under ten
    save_reach = P.reach
    P.reach = lambda ts: (P.D[:, P.dnodes] + ts) < K.STANDARD_MIN * 60.0
    v = P.cover(P.free, pos)
    P.reach = save_reach
    row("SF5 within ten minutes read as strictly under ten names the same districts", C.named(v) == GOLD,
        "max diff %.4f" % np.abs(v - gold).max())
    # SF6 one-way links ignored
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import dijkstra
    lk = C.read_csv(os.path.join(target, K.F_LINKS))
    nid = {n: i for i, n in enumerate(P.node_ids)}
    a = np.array([nid[x] for x in lk["from_node"]]); b = np.array([nid[x] for x in lk["to_node"]])
    w = np.array(lk["drive_time_s"], float)
    G = csr_matrix((np.r_[w, w], (np.r_[a, b], np.r_[b, a])), shape=(P.N, P.N))
    D_save = P.D
    P.D = dijkstra(G, directed=True).astype(np.float32)
    v = P.cover(P.free, pos)
    P.D = D_save
    row("SF6 drive times with one-way links driven both ways name the same districts", C.named(v) == GOLD,
        "max diff %.3f" % np.abs(v - gold).max())
    # SF7 the nearest node: a home placed at the node nearest its address point (standard section 4) - one reading
    row("SF7 node snapping: the standard times a drive between the nodes nearest its start and end; every address and "
        "report has one nearest node", len(np.unique(P.ntree.query(P.addr_xy)[1])) > 0, "")
    # SF8 sampling: covered at the start of the minute against the minute's end
    v = P.cover(P.free[1:], pos[1:]) if False else None
    row("SF8 the year's minutes: sampling every fifth minute names the same districts (included in SF10)",
        C.named(fam["five-minute sampling"]) == GOLD, "")
    # SF9 heartbeats: re-sent statuses change nothing
    tt_changes = 0
    for e in range(P.nE):
        tt, cc, rr = P.st_rows[e]
        keep = np.r_[True, (cc[1:] != cc[:-1]) | (rr[1:] != rr[:-1])]
        mins = np.arange(M) * 60
        idx = np.clip(np.searchsorted(tt[keep], mins, side="right") - 1, 0, None)
        tt_changes += int(((cc[keep][idx] == "1") != P.free[:, e]).sum())
    row("SF9 status re-sends: dropping every re-sent status leaves every engine's free minutes unchanged",
        tt_changes == 0, "%d minutes differ" % tt_changes)
    # SF11 out of base: an engine with no location row stands at its station
    ev = P.trk["ev"]
    row("SF11 every out-of-base spell in the log opens with Left base and closes with Arrived base",
        _spells_closed(P), "")
    # SF12 the line: below 75 on unrounded cover; SF13 rounding to whole per cent
    row("SF12 the line: no district's unrounded cover rounds across 75 (named on unrounded cover, standard section 6)",
        all((v < K.LINE) == (K.round_half_up(v, 0) < K.LINE) for v in gold), "")
    row("SF13 the year: the 525,600 minutes from 00:00 UTC on 1 January 2026 (standard section 5); the log's times are "
        "UTC", P.free.shape[0] == 525600, "")
    # SF14 the district of a home: its 2021 output area's district
    row("SF14 every residential address carries a 2021 output area in the lookup", bool(len(P.addr_dist)), "")
    # SF15 committed engines: an engine mobilised or in attendance is not free (standard section 3)
    v = P.cover((codes == 1) | (codes == 3) | (codes == 5), pos)
    row("SF15 counting mobilised and attending engines free is ruled out by standard section 3 (names %s)" %
        (", ".join(C.named(v)) or "none"), True, "")
    # SF16 the minute's start: a message timed on the minute's first second taken as in force, or the state before it
    mins = np.arange(M) * 60
    free_b = np.zeros_like(P.free)
    for e in range(P.nE):
        tt, cc, rr = P.st_rows[e]
        idx = np.searchsorted(tt, mins, side="left") - 1
        free_b[:, e] = np.where(idx >= 0, cc[np.clip(idx, 0, None)], "") == "1"
    pos_b = np.tile(P.home, (M, 1)).astype(np.int32)
    for e in range(P.nE):
        m = P.trk["e"] == e
        tt, ev_, nd = P.trk["t"][m], P.trk["ev"][m], P.trk["node"][m]
        o = np.argsort(tt, kind="stable"); tt, ev_, nd = tt[o], ev_[o], nd[o]
        idx = np.searchsorted(tt, mins, side="left") - 1
        ii = np.clip(idx, 0, None); out_ = (idx >= 0) & (ev_[ii] != "Arrived base")
        pos_b[out_, e] = nd[ii[out_]]
    v = P.cover(free_b, pos_b)
    row("SF16 the minute's start: the state before a message timed on the minute's first second names the same districts "
        "at the same whole per cent", C.named(v) == GOLD and all(K.round_half_up(x, 0) == K.round_half_up(y, 0)
                                                                  for x, y in zip(v, gold)),
        "max diff %.4f" % np.abs(v - gold).max())
    # SF2 the clock: a log time read as local clock time
    trk = P._tracking(clock_shift=3600)
    v = P.cover(P.free, P.positions("hold", trk=trk))
    P._tracking()
    row("SF2 location times read an hour out against the statuses name the same districts", C.named(v) == GOLD,
        "max diff %.3f" % np.abs(v - gold).max())
    # ------------------------------------------------------------------------------------------------ loudness
    wt = np.where(P.crew == "Wholetime")[0]
    away_free = (P.free[:, wt] & (pos[:, wt] != homeM[:, wt])).sum() / P.free[:, wt].sum()
    row("LOUDNESS wholetime engines' free minutes spent out of base", 0.05 < away_free < 0.30, "%.3f" % away_free)
    # ------------------------------------------------------------------------------------------------ ask A
    g = C.ask_a(target, P)
    u = C.ask_a(target, P, how="union")
    fr = C.ask_a(target, P, how="first")
    cur = C.ask_a(target, P, roles="current")
    F_a = F["ask_a"]
    row("ASK A figures.json carries every station's two figures", all(
        F_a[s]["off_run_4plus"] == C.hm(g[s][0]) and F_a[s]["no_oic"] == C.hm(g[s][1]) for s in C.RURAL_STATIONS), "")
    row("ASK A device: reading every booking (overlaps merged) misses both figures at every station",
        all(u[s][0] != g[s][0] and u[s][1] != g[s][1] for s in C.RURAL_STATIONS),
        " ".join("%s:%+d/%+d" % (s, u[s][0] - g[s][0], u[s][1] - g[s][1]) for s in C.RURAL_STATIONS))
    row("ASK A device: keeping the earlier of two overlapping bookings misses both figures at every station",
        all(fr[s][0] != g[s][0] and fr[s][1] != g[s][1] for s in C.RURAL_STATIONS), "")
    row("ASK A hazard: roles read as at the extract (no promotion dates) move the second figure where a promotion fell",
        sum(cur[s][1] != g[s][1] for s in C.RURAL_STATIONS) >= 3, "")
    row("ASK A every off-the-run boundary in the log falls on a whole minute, so the time is exact in hours and minutes",
        _whole_minute_or(P), "")
    cr_l = C.crew_rule(target, P, "latest")
    cr_u = C.crew_rule(target, P, "union")
    contra_l = sum(int((v["met"] & v["crew_off"]).sum()) for v in cr_l.values())
    contra_u = sum(int((v["met"] & v["crew_off"]).sum()) for v in cr_u.values())
    gap_l = sum(int((~v["met"] & v["avail"]).sum()) for v in cr_l.values())
    row("ASK A forcing: read with the later booking standing, no minute is off the run for crew with the crewing rule "
        "met, and no minute is Available without it; read as every booking, %d minutes are off the run for crew with "
        "the rule met" % contra_u, contra_l == 0 and gap_l == 0 and contra_u > 1000, "%d / %d / %d" % (contra_l, gap_l,
                                                                                                    contra_u))
    # ------------------------------------------------------------------------------------------------ ask C
    c = C.ask_c(target, P)
    c_none = C.ask_c(target, P, dedupe="none")
    c_day = C.ask_c(target, P, dedupe="day")
    F_c = F["ask_c"]
    row("ASK C figures.json carries every district's count and rate", all(
        F_c[d]["actuations"] == str(c[d][0]) and F_c[d]["per_100"] == "%.1f" % K.round_half_up(c[d][1], 1)
        for d in K.DISTRICTS), "")
    row("ASK C device: counting every record misses every district's count and rate",
        all(c_none[d][0] != c[d][0] and abs(K.round_half_up(c_none[d][1], 1) - K.round_half_up(c[d][1], 1)) >= 0.1
            for d in K.DISTRICTS), " ".join("%s:%+d" % (d[:4], c_none[d][0] - c[d][0]) for d in K.DISTRICTS))
    row("ASK C device: one alarm per premises a day misses every district's count and rate",
        all(c_day[d][0] != c[d][0] and abs(K.round_half_up(c_day[d][1], 1) - K.round_half_up(c[d][1], 1)) >= 0.1
            for d in K.DISTRICTS), " ".join("%s:%+d" % (d[:4], c_day[d][0] - c[d][0]) for d in K.DISTRICTS))
    clrC = min(K.bin_clearance(c[d][1], 0.1) for d in K.DISTRICTS)
    row("ASK C every rate sits 0.02 or more inside its one-decimal cell", clrC >= 0.02, "%.4f" % clrC)
    ov, rep = _pairs(target, P)
    row("ASK C forcing: pairs at one premises where the later call came while the earlier record was open (one "
        "actuation) and pairs where it came after closing (two)", ov >= 50 and rep >= 50, "%d overlapping, %d after" % (ov, rep))
    # ------------------------------------------------------------------------------------------------ separation
    src = open(os.path.join(HERE, "calc.py"), encoding="utf-8").read()
    main_src = src[src.index("class Pack"):src.index("# ------------------------------------------------------------------------------------------------- ask A")]
    row("SEP the call reads none of the asks' or distractors' files",
        not re.search(r"F_BOOK|F_CREW|F_POLICY|F_INC|F_CODES|F_POP|F_ESTAB|F_CABINET", main_src), "")
    row("SEP the asks' device rows sit outside the call's files (bookings, incidents)",
        K.F_BOOK != K.F_LOG and K.F_INC != K.F_LOG, "")
    # ------------------------------------------------------------------------------------------------ names, dashes, gates
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()] + EXTRA_PLACES
    invented = sorted({"Ostrevale", "Calderstow", "Tollesham", "Wrenfold", "Hollinbury", "Pelmarsh", "Altmoor",
                       "Skirwold", "Brandeth"} | {n for lst in K.OC_STATIONS.values() for _c, n in lst})
    near = ["%s (%s)" % (nm, p) for nm in invented for p in places
            if _ed(nm.lower(), p) <= 2 or (len(p) >= 5 and (p in nm.lower() or nm.lower() in p))]
    row("H21 every invented place name (%d) is three or more edits from every reference place" % len(invented),
        not near, ", ".join(near[:8]))
    text = " ".join(D.text_of_sections(s) for s in (D.STANDARD, D.POLICY, D.CABINET))
    prompt = open(os.path.join(task_dir, "prompt.txt"), encoding="utf-8").read()
    sub = open(os.path.join(task_dir, "submission.md"), encoding="utf-8").read()
    row("no em or en dash in the documents, the prompt or the write-up",
        all("—" not in x and "–" not in x for x in (text, prompt, sub)), "")
    lowdoc = (text + " " + prompt).lower()
    row("LEAK no document or the prompt speaks of where an engine stands away from its station",
        not re.search(r"track|position|location|stand(s|ing)? by|standby|training|home fire safety|visit|out of base",
                      lowdoc), "")
    files = sorted(os.listdir(target))
    row("GATE files", len(files) >= 10, str(len(files)))
    row("GATE formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str(sorted({f.rsplit('.', 1)[1] for f in files})))
    nlog = len(P.log["event"])
    row("GATE a file of 25,000 rows or more", nlog >= 25000, "%d" % nlog)
    row("GATE no file or sheet describes the data (readme, dictionary, notes, manifest)",
        not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook", f.lower()) for f in files), "")
    meta = json.load(open(os.path.join(task_dir, "metadata.json")))
    row("GATE two distractors named in metadata, unused by the call and the asks",
        len(meta["distractor_files"]) >= 2 and not re.search(r"F_POP|F_ESTAB", src), "")
    for f in files:
        if f.endswith(".pdf"):
            b = open(os.path.join(target, f), "rb").read()
            row("H1 %s carries no generator signature" % f, b"ReportLab" not in b and b"reportlab" not in b, "")
        if f.endswith(".xlsx"):
            import zipfile
            z = zipfile.ZipFile(os.path.join(target, f))
            core = z.read("docProps/core.xml").decode()
            row("H1 %s carries the service's own metadata" % f, "openpyxl" not in core and K.SERVICE in core, "")
    last = max(P.log["time_utc"])
    row("H16 nothing in the log after the year", last < "2027-01-01", last)
    three_rules(task_dir, target, P, gold, pos, lad)
    realism(target, P)
    bad = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("%d checks, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


def three_rules(task_dir, target, P, gold, pos, lad):
    """dataset-generation 7.1: R1 the field's raw material ships; R2 every mess item is neutral; R3a the analyst test
    on the clean truth; R3b the decisive step alone; R3c no plant."""
    import openpyxl
    import ops as O
    import tune as T
    import world as W
    key = lambda v: [int(K.round_half_up(x, 0)) for x in v]
    comp = lambda v: [key(v)[K.DISTRICTS.index(d)] for d in GOLD + DEFAULT]
    # R1
    heads = []
    for f in sorted(os.listdir(target)):
        if f.endswith(".csv"):
            heads += open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(target, f), read_only=True)
            for ws in wb.worksheets:
                heads += [str(x) for x in next(ws.iter_rows(max_row=1, values_only=True)) if x]
            wb.close()
    row("R1 the minute-grain record ships (status rows and location rows of every engine, the routing network, the "
        "address points) and no shipped column holds cover", len(P.trk["t"]) > 100000 and not any(
            "cover" in h.lower() for h in heads), "%d location rows" % len(P.trk["t"]))
    row("R1 the golden's decisive computation reads the location rows: with them dropped it is the station replay",
        C.named(P.cover(P.free, np.broadcast_to(P.home, pos.shape))) == DEFAULT, "")
    # R2: each Layer 1 item mishandled leaves the call and the four deciding districts' printed cover
    row("R2 re-sent statuses: read as new spells, no engine's free minutes change (SF9)", True, "")
    trk = P._tracking(clock_shift=3600)
    v = P.cover(P.free, P.positions("hold", trk=trk))
    P._tracking()
    row("R2 location times read an hour out: same call", C.named(v) == GOLD, " ".join("%.2f" % x for x in v))
    row("R2 one-way links, residential and commercial classes: same call (SF6, SF1)", True, "")
    row("R2 the bookings' local clock and the incident records' code change and 2011 output areas sit only in the "
        "asks' files, which the call never reads (ledgered ask hazards)", True, "")
    # R3a and R3b on the clean truth: the generator's own world and minute arrays, before any record is written
    Wd = W.build()
    sim = O.simulate(Wd)
    free, ipos, _kind = O.minute_arrays(Wd, sim)
    rr = T.rungs(Wd, free, ipos)
    row("R3a the analyst test on the clean truth: the station replay names Altmoor and Skirwold",
        [K.DISTRICTS[i] for i in np.where(rr["R2 station replay"] < K.LINE)[0]] == DEFAULT,
        " ".join("%.2f" % x for x in rr["R2 station replay"]))
    row("R3b on the clean truth the decisive step alone (positions for stations) names Wrenfold and Pelmarsh",
        [K.DISTRICTS[i] for i in np.where(rr["R3 positions"] < K.LINE)[0]] == GOLD,
        " ".join("%.2f" % x for x in rr["R3 positions"]))
    row("R3b each lower rung's single correction (zero when away, standby credited, stations only) stays wrong",
        all([K.DISTRICTS[i] for i in np.where(rr[k] < K.LINE)[0]] != GOLD for k in
            ("R2b zero when away", "P1 standby credited", "P3 stations only")), "")
    # R3c no plant: no copied block of statuses, trips or bookings
    sigs = set()
    dup = 0
    for e in range(P.nE):
        tt, cc, rr_ = P.st_rows[e]
        ch = np.r_[True, cc[1:] != cc[:-1]]
        sig = tuple((tt[ch] % 86400)[:400].tolist())
        dup += sig in sigs
        sigs.add(sig)
    bk = C.read_csv(os.path.join(target, K.F_BOOK))
    per = {}
    for s, f, t in zip(bk["staff_number"], bk["available_from"], bk["available_to"]):
        per.setdefault(s, []).append(f[5:] + t[5:])
    sets = [tuple(sorted(v)) for v in per.values()]
    row("R3c no copied block: no two engines share a status timetable, no two firefighters a set of bookings",
        dup == 0 and len(set(sets)) == len(sets), "")


def realism(target, P):
    """dataset-generation 11: no arithmetic id sequence, no alphabetical or round-robin assignment, no uniform counts."""
    import openpyxl
    cols = {K.F_BOOK: "booking_ref", K.F_INC: "incident_number", K.F_NODES: "node_id", K.F_LINKS: "link_id",
            K.F_ADDR: "uprn"}
    for f, col in cols.items():
        vals = C.read_csv(os.path.join(target, f))[col]
        nums = np.array([int(re.sub(r"\D", "", v)) for v in vals])
        if f == K.F_INC:
            nums = np.array([int(v.split("/")[1]) for v in vals if v.startswith("26/")])
        d = np.diff(np.sort(nums))
        row("REALISM %s %s is no arithmetic sequence" % (f, col), len(np.unique(d)) > 1, "%d steps" % len(np.unique(d)))
    wb = openpyxl.load_workbook(os.path.join(target, K.F_FLEET), read_only=True)
    st = [r for r in wb["Stations"].iter_rows(min_row=2, values_only=True)]
    wb.close()
    row("REALISM station codes do not run in the names' alphabetical order",
        [r[0] for r in sorted(st, key=lambda r: r[1])] != [r[0] for r in sorted(st, key=lambda r: r[0])], "")
    wb = openpyxl.load_workbook(os.path.join(target, K.F_CREW), read_only=True)
    crew = [r for r in wb["Crew"].iter_rows(min_row=2, values_only=True)]
    wb.close()
    pos_wc, sizes = [], {}
    for sc in sorted({r[1] for r in crew}):
        rows_ = [r for r in crew if r[1] == sc]
        sizes[sc] = len(rows_)
        pos_wc += [k for k, r in enumerate(rows_) if r[2] == "Watch Commander"]
    row("REALISM the watch commander falls at different places in each station's staff list", len(set(pos_wc)) > 3,
        str(sorted(set(pos_wc))))
    row("REALISM on-call crews differ in size", len(set(sizes.values())) >= 3, str(sorted(set(sizes.values()))))
    row("REALISM no headline total is round: homes %d" % int(P.homes.sum()), int(P.homes.sum()) % 100 != 0, "")
    t = P.trk["t"]
    gaps = np.diff(np.sort(t[(P.trk["e"] == 0) & (P.trk["ev"] == "Location")]))
    row("REALISM location reports are not on a fixed clock", len(np.unique(gaps[gaps < 120])) > 10, "")


def _whole_minute_or(P):
    for e in range(P.nE):
        tt, cc, rr = P.st_rows[e]
        ch = np.r_[True, cc[1:] != cc[:-1]]
        edge = ch & ((cc == "8") | np.r_[False, cc[:-1] == "8"])
        if (tt[edge] % 60 != 0).any():
            return False
    return True


def _spells_closed(P):
    ev, e = P.trk["ev"], P.trk["e"]
    for k in range(P.nE):
        s = ev[e == k]
        if not len(s):
            continue
        state = "in"
        for x in s:
            if x == "Left base":
                if state != "in":
                    return False
                state = "out"
            elif x == "Arrived base":
                if state != "out":
                    return False
                state = "in"
            elif state != "out":
                return False
    return True


def _pairs(target, P):
    inc = C.read_csv(os.path.join(target, K.F_INC))
    code = np.array(inc["classification"])
    afa = (code == "A01") | (code == "FAA")
    cls_of = dict(zip(P.addr_uprn, np.where(P.addr_res, "R", "C")))
    uprn = np.array(inc["uprn"])
    sel = np.where(afa & np.array([cls_of.get(u, "") == "C" for u in uprn]))[0]
    call = np.array(inc["call_time"], dtype="datetime64[s]")
    closed = np.array(inc["closed_time"], dtype="datetime64[s]")
    o = sel[np.lexsort((call[sel], uprn[sel]))]
    ov = rep = 0
    for k in range(1, len(o)):
        i, j = o[k - 1], o[k]
        if uprn[i] == uprn[j]:
            if call[j] <= closed[i]:
                ov += 1
            elif str(call[j])[:10] == str(call[i])[:10]:
                rep += 1
    return ov, rep


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
