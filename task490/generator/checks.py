"""task490 assertions on the clean truth and the cut pack. Exit 1 on any failure."""
import csv
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta

import world as W
import sim
import golden as G
import records as R
import docs as D

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAILS = []
N = [0]


def check(label, ok, detail=""):
    N[0] += 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def replay_dirs(seq, resets=(), times=None):
    st, f = "L", 0
    for i, d in enumerate(seq):
        if times is not None:
            for r_ in resets:
                if i and times[i - 1] < r_ <= times[i]:
                    st = "L"
        if d == "up":
            f += 1
            st = "H"
        else:
            if st == "L":
                f += 1
            st = "L"
    return f


def winner(x):
    o = sorted(x, key=lambda s: -x[s])
    return o[0], x[o[0]] / x[o[1]], o


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


figs = json.load(open(os.path.join(HERE, "figures.json")))
boats, fleet, cyc = sim.season_traffic()

# ------------------------------------------------------------------ the ladder on the clean truth (R3a, R3b)
routes = {k: {s: 0.0 for s in W.SUMMITS} for k in ("gold", "r0", "r1", "r2", "ups", "half")}
for s in W.SUMMITS:
    for a in W.SUMMIT_LOCKS[s]:
        v = W.LOCK[a]["lockful"] / 1000.0
        cs = cyc[a]
        seq = [c["direction"] for c in cs for _ in c["boats"]]
        routes["gold"][s] += sum(c["filled"] for c in cs) * v
        routes["r0"][s] += len(seq) * v
        routes["r1"][s] += replay_dirs(seq) * v
        routes["r2"][s] += len(cs) * v
        routes["ups"][s] += sum(1 for d in seq if d == "up") * v
        routes["half"][s] += 0.5 * len(seq) * v
w0, m0, o0 = winner(routes["r0"])
w1, m1, o1 = winner(routes["r1"])
w2, m2, o2 = winner(routes["r2"])
wg, mg, og = winner(routes["gold"])
check("R3a analyst test, a lockful a boat files Harnock", w0 == "Harnock" and m0 >= 1.15, "%s by %.3f" % (w0, m0))
check("R3a analyst test, the chamber replayed boat by boat files Harnock", w1 == "Harnock" and m1 >= 1.20,
      "%s by %.3f" % (w1, m1))
check("R3a every per-boat shortcut files Harnock (ups only, half a lockful a boat)",
      winner(routes["ups"])[0] == "Harnock" and winner(routes["half"])[0] == "Harnock")
check("R3b the decisive step alone (cycles in place of boats) moves rung 1 to Kelsby", wg == "Kelsby" and mg >= 1.2,
      "%s by %.3f over %s" % (wg, mg, og[1]))
check("R3b pairing without the chamber's state stays wrong", w2 != "Kelsby", "%s by %.3f" % (w2, m2))
check("ladder: Kelsby last on rung 0", o0[-1] == "Kelsby", str(o0))
edge_k = routes["r1"]["Kelsby"] - routes["gold"]["Kelsby"]
edge_h = routes["r1"]["Harnock"] - routes["gold"]["Harnock"]
carried = routes["r1"]["Harnock"] - routes["r1"]["Kelsby"]
check("dominance: the decisive step's edge clears Harnock's carried advantage 1.2 times",
      (edge_h - edge_k) >= 1.2 * carried, "%.1f against %.1f" % (edge_h - edge_k, carried))

# -------------------------------------------------------------------- the pack reproduces the clean truth
for a in W.LOCK:
    nf = sum(c["filled"] for c in cyc[a])
    check("Gate A fillings at %s reproduce from the pack" % a, figs["locks"][a]["fills"] == nf,
          "%d against truth %d" % (figs["locks"][a]["fills"], nf))
check("the call from the pack is Kelsby", figs["call"] == "Kelsby" and figs["runner_up"] == "Tilsey")

# ---------------------------------------------------------------------------- R1: the raw material ships
hdr = open(os.path.join(T, R.F_MOVES)).readline().strip().split(",")
check("R1 the movement export carries one row per detection with time, direction and class",
      hdr == ["site_code", "record_no", "detected_at", "direction", "class", "index_read", "confidence", "firmware"])
check("R1 no shipped column holds a filling, a cycle or a chamber state",
      not any(re.search(r"fill|cycle|chamber|state|lockful|pair|share", h, re.I) for h in hdr))

# -------------------------------------------------- the grouping corridor and the gap structure (SF6, C1)
ev = G.load_moves(T)
kept, dups, unp = G.clean_moves(ev)
keepers = G.load_keepers(T)
merged, n_keep, gap = G.stitch_keepers(kept, keepers)
corr = []
for thr in (1.6, 2.0, 3.0, 5.0, 8.0, 11.0):
    tot = 0
    for a in W.LOCK:
        tot += sum(G.replay(G.cycles_of(merged[a], thr), a))
    corr.append(tot)
check("SF6 one chamber cycle: every grouping threshold from 1.6 to 11 minutes gives the same fillings",
      len(set(corr)) == 1, str(corr))
bad = 0
for a in W.LOCK:
    es = [e for e in merged[a] if not e.get("keeper")]
    for x, y in zip(es, es[1:]):
        g = (y["t"] - x["t"]).total_seconds() / 60
        if x["dir"] == y["dir"] and 1.6 < g < 11.0:
            bad += 1
check("SF6 no two same-direction camera records at a lock fall 1.6 to 11 minutes apart", bad == 0, str(bad))
inn, sep = 0.0, 1e9
for a in W.LOCK:
    es = [e for e in merged[a] if not e.get("keeper")]
    for x, y in zip(es, es[1:]):
        g = (y["t"] - x["t"]).total_seconds() / 60
        if x["dir"] == y["dir"]:
            if g < 5:
                inn = max(inn, g)
            else:
                sep = min(sep, g)
check("H29 the stated bounds hold: pairs within 1.1 minutes, separate same-direction cycles at least 14 minutes apart",
      inn <= 1.1 and sep >= 14.0, "max within %.3f, min apart %.2f" % (inn, sep))
check("SF10 repeat reads of one plate never move a filling (kept, the fillings are the same)",
      sum(sum(G.replay(G.cycles_of(
          sorted([e for e in ev[a] if e["cls"] == "boat"] + ([k for k in merged[a] if k.get("keeper")]),
                 key=lambda e: (e["t"], e["no"]))), a)) for a in W.LOCK) == sum(figs["locks"][a]["fills"] for a in W.LOCK))

# ------------------------------------------------------------------------------------ the fork table rows
lk = figs["lockage_ml"]
check("SF1 the summit locks are the programme's six; no other lock's rows ship in the movement export",
      sorted(ev) == sorted(W.LOCK))
alt = {}
for s in W.SUMMITS:
    alt[s] = 0.0
    for a in W.SUMMIT_LOCKS[s]:
        spec = W.LOCK[a]
        ft = [float(x.split("'")[0]) + float(x.split("'")[1].strip(' "')) / 12 for x in spec["ft"]]
        vol = ft[0] * ft[1] * ft[2] * 0.0283168
        alt[s] += figs["locks"][a]["fills"] * vol / 1000
check("SF2 a lockful from the 1951 schedule's feet and inches gives the same call", winner(alt)[0] == "Kelsby",
      str({k: round(v, 1) for k, v in alt.items()}))
check("SF3 the season window: the export holds 1 April to 31 October only",
      all(W.SEASON_START <= e["t"].date() <= W.SEASON_END for a in ev for e in ev[a]))
check("SF4 water is lockfuls times fillings, in megalitres", all(
    abs(figs["locks"][a]["ml"] - round(figs["locks"][a]["fills"] * W.LOCK[a]["lockful"] / 1000, 1)) < 1e-9
    for a in W.LOCK))
no_vis = {s_: sum(sum(G.replay(G.cycles_of([e for e in merged[a] if not e["idx"].startswith("VP")]), a)) * W.LOCK[a]["lockful"]
              for a in W.SUMMIT_LOCKS[s_]) for s_ in W.SUMMITS}
check("SF5 every boat counts (hire, private, visiting): dropping visitors gives the same call", winner(no_vis)[0] == "Kelsby")
no_reset = {s: sum(sum(G.replay(G.cycles_of(merged[a]), "none")) * W.LOCK[a]["lockful"] for a in W.SUMMIT_LOCKS[s])
            for s in W.SUMMITS}
check("SF7 Steward's Lock left empty on reopening: ignoring it gives the same call", winner(no_reset)[0] == "Kelsby")
from openpyxl import load_workbook
_lw = load_workbook(os.path.join(T, R.F_LOCKS), read_only=True)["Chamber survey 2025"]
falls = [r_[12] for r_ in _lw.iter_rows(values_only=True) if r_ and r_[0] in W.LOCK]
check("SF8 chambers hold water overnight: every summit lock's survey fall in 12 hours is under 25 mm", len(falls) == 6 and max(falls) < 25, str(falls))
with_unp = {s: 0.0 for s in W.SUMMITS}
for a in W.LOCK:
    es = sorted([e for e in ev[a]] + [k for k in merged[a] if k.get("keeper")], key=lambda e: (e["t"], e["no"]))
    with_unp[W.LOCK[a]["summit"]] += sum(G.replay(G.cycles_of(es), a)) * W.LOCK[a]["lockful"]
check("SF9 unpowered craft kept in: the same call", winner(with_unp)[0] == "Kelsby")
no_keep = {s: sum(sum(G.replay(G.cycles_of(kept[a]), a)) * W.LOCK[a]["lockful"] for a in W.SUMMIT_LOCKS[s])
           for s in W.SUMMITS}
check("SF11 the keepers' log left out: the same call", winner(no_keep)[0] == "Kelsby")
check("SF12 no tie: Kelsby leads by more than 200 Ml", figs["gap_ml"] > 200, str(figs["gap_ml"]))
per_boat = {s: lk[s] / sum(figs["locks"][a]["up"] + figs["locks"][a]["down"] for a in W.SUMMIT_LOCKS[s])
            for s in W.SUMMITS}
check("SF13 the most water, not the most per boat: per boat also names Kelsby", winner(per_boat)[0] == "Kelsby")
check("SF14 unrounded and rounded lockage name the same summit", winner(lk)[0] == figs["call"])

# ------------------------------------------------------------------ mess neutrality (R2), call by call
def call_with(events_by_lock):
    x = {s: 0.0 for s in W.SUMMITS}
    for a in W.LOCK:
        x[W.LOCK[a]["summit"]] += sum(G.replay(G.cycles_of(events_by_lock[a]), a)) * W.LOCK[a]["lockful"]
    return winner(x)[0], x


# UTC read as local clock after the firmware change: every later record an hour early
shift = {}
for a in W.LOCK:
    fw = W.LOCK[a]["fw"]
    shift[a] = sorted([dict(e, t=(e["t"] - timedelta(hours=1)) if e["t"] >= fw else e["t"]) for e in merged[a]],
                      key=lambda e: (e["t"], e["no"]))
check("R2 UTC read as local clock: the same call", call_with(shift)[0] == "Kelsby")
flip = {a: [dict(e, dir=("down" if e["dir"] == "up" else "up") if e["t"] >= W.LOCK[a]["fw"] else e["dir"])
            for e in merged[a]] for a in W.LOCK}
check("R2 A>B read as down: the same call", call_with(flip)[0] == "Kelsby")
dbl = dict(merged)
dbl["TC/L08"] = sorted(kept["TC/L08"] + [dict(k, no=-1) for k in keepers if k["asset"] == "TC/L08"
                                         and gap[0] - timedelta(hours=6) <= k["t"] <= gap[1] + timedelta(hours=6)],
                       key=lambda e: (e["t"], e["no"]))
check("R2 the keepers' log added without linking: the same call", call_with(dbl)[0] == "Kelsby")
check("R2 repeat reads kept: the same call", call_with({a: sorted([e for e in ev[a] if e["cls"] == "boat"] +
      [k for k in merged[a] if k.get("keeper")], key=lambda e: (e["t"], e["no"])) for a in W.LOCK})[0] == "Kelsby")

# --------------------------------------------------------------------------------- bins on graded figures
tight = []
for a in W.LOCK:
    v = figs["locks"][a]["fills"] * W.LOCK[a]["lockful"] / 1000.0
    tight.append(edge(v, 0.1))
for s in W.SUMMITS:
    v = sum(figs["locks"][a]["fills"] * W.LOCK[a]["lockful"] for a in W.SUMMIT_LOCKS[s]) / 1000.0
    tight.append(edge(v, 0.1))
rel, recv, split = G.reservoirs(T)
for v in list(rel.values()) + list(recv.values()):
    tight.append(edge(v, 0.1))
check("bins: every megalitre figure sits at least 0.004 Ml inside its bin", min(tight) >= 0.004,
      "tightest %.4f" % min(tight))

# ---------------------------------------------------------------------- the asks' devices, measured as numbers
ret = G.load_returns(T)
raw_lower = sum(l["rel"] for l in ret["Lower Kelsby Reservoir"] if W.SEASON_START <= l["d"] <= W.SEASON_END)
check("ask S Lower Kelsby: summing the Released column over the season's lines misses (releases booked on the day the valve is shut)",
      abs(raw_lower - rel["Lower Kelsby Reservoir"]) > 1.0, "%.1f against %.1f" % (raw_lower, rel["Lower Kelsby Reservoir"]))
cap_lines = sum(1 for l in ret["Lower Kelsby Reservoir"] if l["rel"] > 16.0)
check("ask S Lower Kelsby: lines above the outlet's full-bore 16 Ml/d exist (the tell)", cap_lines > 15, str(cap_lines))
twin_lines = sum(1 for x, y in zip(ret["Tilsey Reservoir"], ret["Tilsey Reservoir"][1:]) if x["rel"] == y["rel"] > 0)
check("ask S Tilsey: consecutive equal day volumes exist (a de-duplication reflex harms them)", twin_lines > 20,
      str(twin_lines))


def uniform_boundary(lines):
    v = 0.0
    for l in lines:
        if l["d"] == W.SEASON_START:
            v += l["rel"] * 9 / 24
        elif l["d"] == W.SEASON_END + timedelta(days=1):
            v += l["rel"] * 15 / 24
        elif W.SEASON_START < l["d"] <= W.SEASON_END:
            v += l["rel"]
    return v


for name in ("Upper Kelsby Reservoir", "Tilsey Reservoir"):
    u = uniform_boundary(ret[name])
    check("ask S %s: the water day split evenly at the season's ends misses" % name, abs(u - rel[name]) > 0.06,
          "%.2f against %.2f" % (u, rel[name]))
stored = 0.0
with open(os.path.join(T, R.F_COLD), newline="") as f:
    for row in csv.DictReader(f):
        t = datetime.strptime(row["period_end_utc"], "%Y-%m-%dT%H:%M:%SZ")
        if datetime(2026, 3, 31, 23, 0) < t <= datetime(2026, 11, 1, 0, 0):
            stored += float(row["flow_ls_mean"]) * 0.9 / 1000.0
check("ask S Coldmere: the outstation's flow column over-reads the plate change", stored - rel["Coldmere Reservoir"] > 50,
      "%.1f against %.1f" % (stored, rel["Coldmere Reservoir"]))
width_h = rel["Coldmere Reservoir"] * 0.5 / 0.85
check("ask S Fox Bridge: a split by notch width misses Harnock by more than 50 Ml", abs(width_h - recv["Harnock"]) > 50,
      "%.1f against %.1f" % (width_h, recv["Harnock"]))
absn, abst = G.abstraction(T)
naive = {}
reads = {}
with open(os.path.join(T, R.F_READ), newline="") as f:
    for row in csv.DictReader(f):
        reads.setdefault(row["point_ref"], []).append(row)
for L in W.LICENCES:
    rs = reads[L["point"]]
    by = {}
    for r_ in rs:
        by.setdefault(r_["meter_serial"], []).append(int(r_["reading_m3"]))
    tot = 0
    for s_, vals in by.items():
        for x, y in zip(vals, vals[1:]):
            tot += (y - x) % (10 ** L["digits"])
    naive[L["ref"]] = tot
miss_ex = [r_ for r_ in W.EXCHANGES if naive[r_] != absn[r_]["take"]]
check("ask A: chaining the exchanged meters without the works orders' readings misses all four",
      len(miss_ex) == 4, str({r_: (naive[r_], absn[r_]["take"]) for r_ in W.EXCHANGES}))
check("ask A: the unexchanged licences are the same either way", all(naive[L["ref"]] == absn[L["ref"]]["take"]
                                                                       for L in W.LICENCES if L["ref"] not in W.EXCHANGES))

# ------------------------------------------------------------------------------------------- input gates
files = sorted(os.listdir(T))
fmts = {f.rsplit(".", 1)[1] for f in files}
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("input gate: 10 or more files", len(files) >= 10, str(len(files)))
check("input gate: 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
check("input gate: a file of 25,000 rows or more", figs["movement_rows"] >= 25000, str(figs["movement_rows"]))
check("input gate: two or more distractors declared", len(meta["distractor_files"]) >= 2)
check("no readme, dictionary, notes or manifest file under target/",
      not any(re.search(r"readme|dictionar|notes|manifest|schema|distractor", f, re.I) for f in files))
src = open(os.path.join(HERE, "golden.py")).read()
check("distractors: the golden never opens either distractor", "F_BOATS" not in src and "F_STORE" not in src)

# --------------------------------------------------------------------------------------- realism sweep
recnos = []
with open(os.path.join(T, R.F_MOVES), newline="") as f:
    for row in csv.DictReader(f):
        recnos.append((row["site_code"], int(row["record_no"])))
steps = Counter(b[1] - a[1] for a, b in zip(recnos, recnos[1:]) if a[0] == b[0])
check("realism: record numbers are not an arithmetic sequence", len(steps) > 3, str(steps.most_common(4)))
daily = Counter()
for a in W.LOCK:
    for e in merged[a]:
        daily[(a, e["t"].date())] += 1
same = sum(1 for d in W.DAYS if len({daily[(a, d)] for a in W.LOCK}) == 1)
check("realism: no day with the same count at every summit lock", same == 0, str(same))
check("realism: lockage figures are not round", all(abs(v - round(v, -1)) > 0.5 for v in lk.values()))
from pypdf import PdfReader
txt = {}
for fn in (D.F_PROG, D.F_RESREG):
    txt[fn] = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, fn)).pages)
check("documents read back (positive control)", "drew the most water from the summit pound" in txt[D.F_PROG].replace("\n", " ")
      and "Fox Bridge division weir" in txt[D.F_RESREG].replace("\n", " "))
words = r"\b(share|shared|sharing|pair|paired|pairs|together|cycle|cycles|set against|per boat|working in turn|in turn|company)\b"
hits = {fn: re.findall(words, t.replace("\n", " "), re.I) for fn, t in txt.items()}
note_hits = [row for row in csv.reader(open(os.path.join(T, R.F_NOTICES))) if re.search(words, " ".join(row), re.I)]
check("R3c no document names the decisive structure (sharing, pairs, cycles, chamber state)",
      not any(hits.values()) and not note_hits, str(hits) + str(note_hits))
people = set(W.PEOPLE.values())
card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task490.json")))
check("personas in the pack are the card's drawn names", people <= set(card["world"]["people"]), str(people))

print("%d checks, %d failed" % (N[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
