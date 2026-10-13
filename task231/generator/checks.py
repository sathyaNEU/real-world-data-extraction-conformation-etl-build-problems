"""task231 checks, run on every build: the three rules (R1 to R3c) on the clean truth, the ladder, the settled corridor,
every semantic fork row (SF1 to SF13), the asks' devices and their separation from the main population, the input
gates and the realism sweep. Every assertion is labelled; make.py prints the count."""
import csv
import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone

import estim
import params as P
import records
import sim
import verify as V
import world as W

LINES = (55.0, 58.0)


def margin(x):
    return min(abs(x - 55.0), abs(x - 58.0))


def bands(d):
    return {g: V.band(x) for g, x in d.items()}


def run(target, golden_dir, pan, rec, res):
    out = []

    def ok(label, cond, detail=""):
        assert cond, (label, detail)
        out.append(label)

    pk = res["pack"]
    lad = res["ladder"]
    call = V.call_from(lad)
    gold = {g: lad[g]["golden"] for g in lad}
    sim_res, sim_sh = estim.routes(pan)
    regs = estim.REGS

    # ------------------------------------------------------------------------------- generator and files agree
    ok("G1 golden rates: simulation and shipped files agree", all(abs(sim_res[g]["golden"] - gold[g]) < 1e-9 for g in regs))
    ok("G2 default and call-centre rungs agree", all(abs(sim_res[g]["R1"] - lad[g]["R1"]) < 1e-9
                                                    and abs(sim_res[g]["casro"] - lad[g]["casro"]) < 1e-9
                                                    and abs(sim_res[g]["unob"] - lad[g]["unob"]) < 1e-9 for g in regs))
    ok("G3 settled share agrees", abs(sim_sh["settled"] - res["shares"]["settled"]) < 1e-12)
    by_close_files = {}
    for q, rows_ in pk.out.items():
        rnd = pk.by_quarter[q]
        reach = pk.reach_times(q, True)
        for r in rows_:
            by_close_files[(rnd["frame"], int(r["panel_id"]))] = reach.get(int(r["panel_id"])) is not None and \
                reach[int(r["panel_id"])] <= rnd["close_utc"]
    mism = sum(1 for o in pan.outcomes if o["frame"] < P.CURRENT and
               by_close_files[(o["frame"], rec.pid[o["fid"]])] != o["by_close"])
    ok("G4 every return's on-time status in the files matches the simulation", mism == 0, mism)

    # ------------------------------------------------------------------------------- the call and the ladder
    ok("L1 golden: Capital and Harbour red, Islands and Western Uplands amber, the rest green",
       call["extension"] == ["R01", "R02"] and call["email"] == ["R04", "R06"] and len(call["neither"]) == 8)
    red = lambda key: {g for g in regs if V.band(lad[g][key]) == "red"}
    amber = lambda key: {g for g in regs if V.band(lad[g][key]) == "amber"}
    ok("L2 default (register as it stands): five red, seven amber", red("R1") == {"R01", "R02", "R04", "R05", "R06"}
       and amber("R1") == set(regs) - red("R1"))
    ok("L3 call-centre e: four red, Border amber", red("casro") == {"R01", "R02", "R04", "R06"} and "R05" in amber("casro"))
    ok("L4 call-centre e counting staff answers as alive, or reading outbound records only: same levels",
       bands({g: lad[g]["casro_any"] for g in regs}) == bands({g: lad[g]["casro"] for g in regs}) ==
       bands({g: lad[g]["casro_out"] for g in regs}))
    for key in ("recent", "allr", "unob"):
        ok("L5 %s: four red, Border amber" % key, red(key) == {"R01", "R02", "R04", "R06"} and "R05" in amber(key))
    ok("L6 R3 and R4 with telephone returns read at the database load time: same levels",
       bands({g: lad[g]["recent_nat"] for g in regs}) == bands({g: lad[g]["recent"] for g in regs}) and
       bands({g: lad[g]["allr_nat"] for g in regs}) == bands({g: lad[g]["allr"] for g in regs}))
    ok("L7 over-correction (every unresolved non-returner closed): all green", red("over") | amber("over") == set())
    ok("L8 truth lands the golden's levels with margin", all(V.band(sim_res[g]["truth"]) == call["levels"][g]
                                                          and margin(sim_res[g]["truth"]) >= 0.3 for g in regs))
    ok("L9 every rung sits clear of the lines", min(margin(lad[g][k]) for g in regs
                                                   for k in ("R1", "casro", "recent", "allr", "unob", "golden")) >= 0.15)
    ok("L10 only the settled share files the golden call",
       all(bands({g: lad[g][k] for g in regs}) != call["levels"] for k in ("R1", "casro", "recent", "allr", "unob", "over")))
    ok("L11 shares: settled above all rounds above the last two years", res["shares"]["settled"] > res["shares"]["all"] >
       res["shares"]["recent"])

    # ------------------------------------------------------------------------------- the corridor (SF7 to SF10)
    for g in regs:
        for name, x in sim_res[g]["corridor"].items():
            ok("C1 simulation corridor %s %s" % (g, name), V.band(x) == call["levels"][g] and margin(x) >= 0.25, x)
    for g, row in res["corridor"].items():
        for name, x in row.items():
            ok("C2 file corridor %s %s" % (g, name), V.band(x) == call["levels"][g] and margin(x) >= 0.25, x)
    last = estim.months_before(P.EXTRACT, P.SETTLED_MONTHS)
    s_call, _ = estim.settled_share(pan, last, key=lambda f, o: o["call"], first_frame=date(2022, 3, 1))
    cur = estim.current(pan)
    for g in regs:
        c = cur[g]
        x = 100.0 * c["R"] / (c["R"] + sum(1 - s_call.get(o["call"], 0.0) for f, o in c["nr"]))
        ok("C3 settled share by call outcome (2022 rounds) %s" % g, V.band(x) == call["levels"][g], x)

    # ------------------------------------------------------------------------------- semantic fork table
    inv = pk.inv
    holders = pk.holders
    ok("SF1 every invited firm's region matches its panel register record",
       all(any(h["region"] == inv[pid]["region"] for h in holders[pid]) for pid in inv))
    active = set()
    for pid, hs in holders.items():
        for h in hs:
            if h["left"] is None and h["recruited"] <= V.FRAME:
                active.add(pid)
    ok("SF2 the active panel and the invitation list hold the same firms", active == set(inv), len(active ^ set(inv)))
    last_ret = max(t for v in pk.sep.values() for t, m in v)
    ok("SF3 no September return after 15:00 UTC on 25 September", last_ret <= datetime(2026, 9, 25, 15, 0, tzinfo=timezone.utc))
    frames = set(records.FRAMES)
    ok("SF4 no shipped closure ceased on a round's frame date", all(c[0] not in frames for c in pk.clos.values()))
    ok("SF5 the September 2026 frame date is 1 September", pk.rounds["2026-09"]["frame"] == date(2026, 9, 1))
    raw = {g: 100.0 * lad[g]["R"] / lad[g]["inv"] for g in regs}
    ok("SF6 returns over every invited firm: a wrong call", bands(raw) != call["levels"])
    ok("SF7 every settled estimate at least 0.25 points from both lines",
       min(margin(x) for row in res["corridor"].values() for x in row.values()) >= 0.25)
    ok("SF8 status at the round's end lands the same levels", all(V.band(row["end"]) == call["levels"][g]
                                                                  for g, row in res["corridor"].items()))
    ok("SF9 windows from 36 to 72 months land the same levels",
       all(V.band(row["w%d" % w]) == call["levels"][g] for g, row in res["corridor"].items() for w in (36, 42, 48, 54, 60, 72)))
    ok("SF10 by region, rounds silent and size band land the same levels",
       all(V.band(row[k]) == call["levels"][g] for g, row in res["corridor"].items() for k in ("region", "k", "size")))
    dup = {pid: v for pid, v in pk.sep.items() if len(v) > 1}
    close = pk.rounds["2026-09"]["close_utc"]
    ok("SF11 every September firm with two returns has both before the close",
       len(dup) > 0 and all(t <= close for v in dup.values() for t, m in v))
    rows_count = {}
    sepv = pk.september()
    for g in regs:
        extra = sum(len(pk.sep[pid]) - 1 for pid in dup if inv[pid]["region"] == g)
        R, n = sepv[g]["R"] + extra, len(sepv[g]["nr"])
        rows_count[g] = 100.0 * R / (R + n * (1 - res["shares"]["settled"]))
    ok("SF11b counting return rows instead of firms leaves every level", bands(rows_count) == call["levels"])
    exact = {r["company_number"] for r in csv.DictReader(open(os.path.join(target, "brevland_business_register_closures.csv")))}
    ok("SF12 main files carry the check-digit form only: an exact join and a core join agree",
       all(re.fullmatch(r"\d{6}-\d", r["company_number"]) for r in inv.values()) and
       {pid for pid, r in inv.items() if r["company_number"] in exact} ==
       {pid for pid, r in inv.items() if V.core(r["company_number"]) in pk.clos})
    import pypdf
    std = " ".join(pg.extract_text() for pg in pypdf.PdfReader(os.path.join(target, "BCS_fieldwork_quality_standard_v3.pdf")).pages)
    std = re.sub(r"\s+", " ", std)
    ok("SF13 the standard's alert table: red under 55 goes into the extension, amber gets one extra email",
       "under 55 per cent The region goes into the reminder-call extension" in std and "one extra email reminder" in std, std[:200])
    ok("SF4b the standard files the scope sentence once", std.count("whether or not the Brevland Business Register yet records") == 1)

    # ------------------------------------------------------------------------------- the three rules
    hdrs = {}
    for f in os.listdir(target):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                hdrs[f] = next(csv.reader(fh))
    banned = re.compile(r"scope|eligib|trading_at|status_at|share|rate|alive|dead|imput|weight", re.I)
    ok("R1a no shipped column holds the deciding quantity", not any(banned.search(h) for v in hdrs.values() for h in v),
       hdrs)
    ok("R1b the decisive computation reads the round outcomes and the register's two dates",
       abs(pk.settled_share()[0]["all"] - sim_sh["settled"]) < 1e-12 and "registered" in hdrs[
           "brevland_business_register_closures.csv"] and "ceased_trading" in hdrs["brevland_business_register_closures.csv"])
    # R2: every Layer 1 item, mishandled, leaves the call
    settled_rows = [(q, r) for q, rows_ in pk.out.items() for r in rows_ if pk.by_quarter[q]["frame"] <= V.SETTLED_LAST]
    ok("R2a postal keying lag: every settled-round row has recorded_at equal to received_at",
       all(r["recorded_at"] == r["received_at"] for q, r in settled_rows))
    settled_out = [o for o in pan.outcomes if o["frame"] <= V.SETTLED_LAST and o["ret_day"] is not None]
    ok("R2b overnight telephone transfer: every settled-round return carries its true reach time",
       all(rec.ret[id(o)]["received"] == rec.ret[id(o)]["reach"] for o in settled_out))
    late_close = 0
    for q, r in settled_rows:
        if not r["received_at"]:
            continue
        t = V.ts(r["received_at"])
        rnd = pk.by_quarter[q]
        if rnd["close_utc"] < t <= datetime.combine(rnd["close"], datetime.min.time(), timezone.utc) + timedelta(hours=17):
            late_close += 1
    ok("R2c UTC read as Brevland time: no settled return falls between the two readings of the close", late_close == 0)
    ok("R2d regional review: the settled share needs no region (blanking every region code leaves it)",
       abs(pk.settled_share(key=lambda r, h, rnd: "all")[0]["all"] - res["shares"]["settled"]) < 1e-12)
    ok("R2e reissued panel IDs: no settled-round panel ID has two holders",
       all(len(holders[int(r["panel_id"])]) == 1 for q, r in settled_rows))
    ok("R2f reissued panel IDs: every invited firm has one holder on the panel now",
       all(sum(1 for h in holders[pid] if h["left"] is None) == 1 for pid in inv))
    ok("R2g the settled share is the same with telephone returns timed from the call records or the database",
       abs(pk.settled_share(phone_from_calls=False)[0]["all"] - res["shares"]["settled"]) < 1e-12)
    quarters = set(pk.out)
    ok("R2h round labels: every outcomes quarter maps to one calendar round",
       all(sum(1 for v in pk.rounds.values() if v["quarter"] == q) == 1 for q in quarters))
    ok("R3a analyst test: the register as it stands, every filed rule applied, files five red and seven amber",
       bands({g: sim_res[g]["R1"] for g in regs}) != call["levels"] and len([g for g in regs if V.band(sim_res[g]["R1"]) ==
                                                                            "red"]) == 5)
    ok("R3b the decisive step alone (settled share) files the golden; each lower correction does not",
       bands({g: sim_res[g]["golden"] for g in regs}) == call["levels"] and
       all(bands({g: sim_res[g][k] for g in regs}) != call["levels"] for k in ("casro", "recent", "allr", "unob")))
    per_round = defaultdict(Counter)
    for q, rows_ in pk.out.items():
        for r in rows_:
            per_round[q][r["mode"] or "none"] += 1
    sig = [tuple(sorted(v.items())) for v in per_round.values()]
    ok("R3c no copied block: no two rounds share a return profile", len(sig) == len(set(sig)))

    # ------------------------------------------------------------------------------- the asks
    A_, B_, C_ = res["A"], res["B"], res["C"]
    st = A_["stops"]
    ok("A1 calls placed: counting rows misses every region", all(st["calls_rows"][g] != A_["calls"][g] for g in regs))
    ok("A2 calls placed: one call per firm a day misses every region", all(st["calls_firmday"][g] != A_["calls"][g] for g in regs))
    ok("A3 calls placed: dropping the reloaded records but keeping transfer legs misses most regions",
       sum(st["calls_noid"][g] != A_["calls"][g] for g in regs) >= 9)
    ok("A3b calls placed: every outbound record counted misses every region",
       all(st["calls_outbound_rows"][g] != A_["calls"][g] for g in regs))
    ok("A3c firms reached: outbound records only miss every region",
       all(st["reached_outbound"][g] != A_["reached"][g] for g in regs))
    ok("A4 firms reached: respondent codes only miss every region", all(st["reached_resp"][g] != A_["reached"][g] for g in regs))
    ok("A5 firms reached: the bank's own records only miss every region",
       all(st["reached_bcb"][g] != A_["reached"][g] for g in regs))
    fields = ("team", "direction", "panel_id", "company_number", "region", "agent", "started_at", "duration_s", "outcome")
    seprec = [r for r in pk.calls if r["round"] == "2026-09"]
    keyc = Counter(tuple(r[f] for f in fields) for r in seprec)
    dups = {k: n for k, n in keyc.items() if n > 1}
    ok("A6 every reloaded record duplicates a 22 September contractor record, and nothing else duplicates",
       len(dups) == rec.replay_n and all(n == 2 and k[0] == "OVF" and V.local_date(V.ts(k[6])) == records.REPLAY_DAY
                                         for k, n in dups.items()))
    ok("A7 the reload reaches every region", len({inv[pk.inv_by_core[V.core(k[3])]]["region"] for k in dups}) == 12)
    inb = [r for r in seprec if r["direction"] == "in"]
    ok("A8 inbound calls: all at the bank's own desk, none on the close day", all(r["team"] == "BCB" for r in inb) and
       all(V.local_date(V.ts(r["started_at"])) != date(2026, 9, 25) for r in inb) and len(inb) > 0)
    ok("B1 late returns: received_at as loaded misses every region",
       all(B_["stops"]["late_received_at"][g] != B_["late"][g] for g in regs))
    ok("B2 late returns: recorded_at misses every region", all(B_["stops"]["late_recorded_at"][g] != B_["late"][g] for g in regs))
    ie = pk.interview_ends("2026-06")
    june_phone = [r for r in pk.out["2026Q2"] if r["mode"] == "phone"]
    ok("B3 every June telephone return has its interview in the call records, ending before its database load",
       all(int(r["panel_id"]) in ie and ie[int(r["panel_id"])] < V.ts(r["received_at"]) for r in june_phone))
    ok("B4 late shares sit clear of a rounding edge", all(abs((100.0 * B_["late"][g] / B_["returns"][g] * 10) % 1 - 0.5) > 0.02
                                                          for g in regs))
    groups = [g for g, _ in W.GROUPS]
    ok("C4 recruited: reading Rev. 2.1 sections as survey groups misses J, M and N",
       all(C_["stops"]["recruited_letters"][g] != C_["recruited"][g] for g in ("J", "M", "N")))
    ok("C5 recruited: counting from the invitation lists misses most groups",
       sum(C_["stops"]["recruited_invited"][g] != C_["recruited"][g] for g in groups) >= 7)
    ok("C5b recruited: counting register rows misses most groups",
       sum(C_["stops"]["recruited_rows"][g] != C_["recruited"][g] for g in groups) >= 5)
    ok("C5c recruited: dropping every withdrawal before the first round misses most groups",
       sum(C_["stops"]["recruited_kept"][g] != C_["recruited"][g] for g in groups) >= 7)
    ok("C5d every duplicate recruitment record shares its company with another 2026 recruit and left before March",
       all(d_["core"] == d_["duplicate_of"]["core"] and d_["left"] < date(2026, 3, 1) for d_ in rec.dups
           if d_["joined"] == records.REFRESH_2026))
    ok("C6 returned at least once: leaving out September misses every group",
       all(C_["stops"]["returned_no_september"][g] != C_["returned"][g] for g in groups))
    ok("C7 returned at least once: any return under the panel ID misses most groups",
       sum(C_["stops"]["returned_any_id"][g] != C_["returned"][g] for g in groups) >= 7)
    reissued = [pid for pid, hs in holders.items() if len(hs) > 1]
    ok("C8 every reissued ID's earlier holder came from the 2024 expansion and left before July 2025",
       all(min(holders[p], key=lambda h: h["recruited"])["wave"] == "2024 expansion" and
           min(holders[p], key=lambda h: h["recruited"])["left"] < date(2025, 7, 1) for p in reissued))
    # separation: the September receipts carry true reach times
    sep_phone = [(pid, t) for pid, v in pk.sep.items() for t, m in v if m == "phone"]
    ie9 = pk.interview_ends("2026-09")
    ok("D3 September telephone returns carry the interview end", all(ie9.get(pid) == t for pid, t in sep_phone), len(sep_phone))

    # ------------------------------------------------------------------------------- input gates and distractors
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok("IG1 ten or more files, three or more formats", len(files) >= 10 and len(fmts) >= 3, (len(files), fmts))
    ok("IG2 a file of 25,000 rows or more", big >= 25000, big)
    ok("IG3 two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]))
    tmp = tempfile.mkdtemp()
    try:
        t2 = os.path.join(tmp, "t")
        shutil.copytree(target, t2)
        for f in meta["distractor_files"]:
            os.remove(os.path.join(t2, f))
        r2 = V.compute(t2)
        same = (V.call_from(r2["ladder"]) == call and r2["A"]["calls"] == A_["calls"] and r2["A"]["reached"] == A_["reached"]
                and r2["B"]["late"] == B_["late"] and r2["C"]["returned"] == C_["returned"] and
                r2["C"]["recruited"] == C_["recruited"])
    finally:
        shutil.rmtree(tmp)
    ok("IG4 deleting the distractors changes no answer", same)
    from openpyxl import load_workbook
    dwb = load_workbook(os.path.join(target, "BCS_data_dictionary.xlsx"), read_only=True)
    listed = {r[0] for r in dwb["Files"].iter_rows(min_row=2, values_only=True) if r[0]}
    ok("IG6 the dictionary names every other shipped file", listed == set(files) - {"BCS_data_dictionary.xlsx"},
       listed ^ (set(files) - {"BCS_data_dictionary.xlsx"}))
    late_clos = [pid for pid, r in inv.items() if V.core(r["company_number"]) in pk.clos
                 and pk.clos[V.core(r["company_number"])][0] > V.FRAME]
    ok("SF4c no invited firm's register closure has it trading on the frame date", not late_clos, late_clos)
    man = json.load(open(os.path.join(target, "export_manifest.json")))
    ok("IG5 the manifest names every other shipped file", {x["file"] for x in man["files"]} == set(files) - {"export_manifest.json"})

    # ------------------------------------------------------------------------------- realism sweep
    inv_n = Counter(r["region"] for r in inv.values())
    ok("RS1 no two regions invite the same number of firms", len(set(inv_n.values())) == 12)
    ok("RS2 no round headline totals", sum(inv_n.values()) % 100 != 0 and round(res["shares"]["settled"] * 1000) % 10 != 0)
    ok("RS3 no two regions have the same late-return count and share",
       len({(B_["late"][g], B_["share"][g]) for g in regs}) == 12)
    allowed = {"BCS_round_calendar.xlsx"}
    limit = datetime(2026, 9, 25, 23, 59, tzinfo=timezone.utc)
    future = set()
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            for m in re.findall(r"\d{4}-\d\d-\d\d(?:T\d\d:\d\d:\d\dZ)?", txt):
                tt = datetime.fromisoformat(m.replace("Z", "+00:00")) if "T" in m else \
                    datetime.combine(date.fromisoformat(m), datetime.min.time(), timezone.utc)
                if tt > limit:
                    future.add(f)
                    break
    ok("RS4 no record dated after the extract outside the calendar", future <= allowed, future)
    dash = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith((".csv", ".json")):
            if "\u2014" in open(p, encoding="utf-8").read() or "\u2013" in open(p, encoding="utf-8").read():
                dash.append(f)
        elif f.endswith((".xlsx", ".pptx")):
            with zipfile.ZipFile(p) as z:
                if any("\u2014".encode() in z.read(n) or "\u2013".encode() in z.read(n) for n in z.namelist()):
                    dash.append(f)
    for f in os.listdir(golden_dir):
        with zipfile.ZipFile(os.path.join(golden_dir, f)) as z:
            if any("\u2014".encode() in z.read(n) or "\u2013".encode() in z.read(n) for n in z.namelist()):
                dash.append(f)
    ok("RS5 no em or en dash in any shipped or golden file", not dash, dash)
    import postprocess
    sc = postprocess._scrubber()
    bad = []
    for d_ in (target, golden_dir):
        for f in os.listdir(d_):
            if f.endswith((".xlsx", ".pdf", ".pptx")):
                names, out_band = sc.audit(os.path.join(d_, f), postprocess.FLOOR, postprocess.CEILING)
                if names or out_band:
                    bad.append((f, names, out_band))
    ok("RS6 no writer signature or out-of-band stamp in any document", not bad, bad)
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(target)), ".claude", "skills", "fingerprint", "cards",
                                       "task231.json")))
    ok("RS7 every persona comes from the card", set(W.PEOPLE.values()) <= set(card["world"]["people"]))
    ok("RS8 no artifact states a response rate, closure share or alert level for the round",
       not any(re.search(r"response.?rate|alert", h, re.I) for v in hdrs.values() for h in v))
    return out
