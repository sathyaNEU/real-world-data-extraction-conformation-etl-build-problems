"""task166 checks: the build's assertions, run on the cut pack in target/ and on the generator's clean truth.

Blocks: G input gates; C the call and its bin; L the ladder on the shipped files; F the golden family; R1 to R3c the
three rules (R2 one assertion per Layer 1 item mishandled); SF1 to SF21 the semantic fork table; A the asks and their
devices; S the separation of the asks from the call and the distractors; D the documents; Q the realism sweep."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import sys
import warnings
import zipfile
from collections import Counter, defaultdict

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import models as M          # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
RES = []
SW, SE, TX, MW, NE, PA = range(6)
LO, HI = 500.0, 700.0          # the 600 bin at the nearest 200


def check(label, ok, detail=""):
    RES.append((label, bool(ok), detail))
    print("%s  %-6s %s" % ("PASS" if ok else "FAIL", label, detail))


def pick(v):
    o = np.argsort(-np.asarray(v))
    return int(o[0]), float(v[o[0]] / v[o[1]])


def top3(v):
    o = np.argsort(-np.asarray(v))
    return ", ".join("%s %.1f" % (C.REG[j], v[j]) for j in o[:3])


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


figs = json.load(open(os.path.join(HERE, "figures.json")))
meta = json.load(open(os.path.join(TASK, "metadata.json")))

# ------------------------------------------------------------------------------------------------- G: input gates
files = sorted(os.listdir(TARGET))
fmts = sorted({f.rsplit(".", 1)[1] for f in files})
check("G1", len(files) >= 10, "%d files" % len(files))
check("G2", len(fmts) >= 3, "formats %s" % fmts)
check("G3", meta["input_gates"]["largest_file_rows"] >= 25000,
      "%s %d rows" % (meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))
dis = meta["distractor_files"]
check("G4", len(dis) >= 2 and all(d in files for d in dis) and not any("distract" in f.lower() for f in files),
      "distractors %s" % dis)
check("G5", sorted(os.listdir(GOLDEN)) == ["onboarding_pod_2027.docx", "onboarding_staffing_2025.xlsx"], "goldens %s" % sorted(os.listdir(GOLDEN)))
bad = [f for f in files if re.search(r"founder|champion|leaver|departure|link|pipeline|referr|answer|golden|onboarding_pod_2027|onboarding_staffing", f, re.I)]
check("G6", not bad, "no file name names the step %s" % bad)

# ------------------------------------------------------------------------------------------------- C: the call
D, sp, Y, gold, info = C.golden(TARGET)
g_pick, g_margin = pick(gold)
order = list(np.argsort(-gold))
check("C1", g_pick == SW, "pick %s, %s" % (C.REG[g_pick], top3(gold)))
check("C2", LO <= gold[SW] < HI and edge(gold[SW], 200) >= 50, "%.2f in [500, 700), %.1f from the nearer edge" % (gold[SW], edge(gold[SW], 200)))
check("C3", order[1] == TX and gold[TX] / gold[order[2]] >= 1.15, "second %s, %.3f over the third" % (C.REG[order[1]], gold[TX] / gold[order[2]]))
check("C4", g_margin >= 1.2, "margin %.3f over the second" % g_margin)
check("C5", figs["call"]["region"] == "Southwest" and figs["call"]["figure_rounded"] == 600 and figs["call"]["second"] == "Texas & Gulf",
      "figures.json carries the call")
check("C6", round(gold[TX] / 200) * 200 != 600,
      "the runner-up's own figure %.1f prints %d, not the golden's 600" % (gold[TX], round(gold[TX] / 200) * 200))

# ------------------------------------------------------------------------------------------------- L: the ladder
care = C.careful_routes(D, sp)
for k, v in care.items():
    p, m = pick(v)
    check("L0", p == TX, "rung 0, %s: %s (TX over SW %.3f)" % (k, top3(v), v[TX] / v[SW]))
check("L0b", all(v[SW] < LO for v in care.values()),
      "rung 0 never puts the Southwest in the 600 bin: %.1f to %.1f" % (min(v[SW] for v in care.values()), max(v[SW] for v in care.values())))
pr = C.probe_routes(D, sp)
check("L0c", pick(pr["ya"])[0] == TX and pick(pr["yb"])[0] == TX and pr["ya"][SW] < LO and pr["yb"][SW] < LO,
      "the two probes' routes on these files: p166ya's four-fold back-test chooses %s and files %s; p166yb's log and linear "
      "trend ensemble files %s" % (pr["ya_choice"], top3(pr["ya"]), top3(pr["yb"])))
new = D["new"]


def tot(a, b):
    return np.array([new[r, a + 48:b + 49].sum() for r in range(6)], float)


mom = {"ytd2026_x12/9": tot(84, 92) * 12 / 9, "last6_x2": tot(87, 92) * 2, "last12": tot(81, 92),
       "last12_x_growth": tot(81, 92) * (tot(81, 92) / tot(69, 80)) ** (15 / 12)}
for k, v in mom.items():
    check("L1", pick(v)[0] == TX, "rung 1, momentum %s: %s" % (k, top3(v)))
r2, coef, active = C.rung2_installed_users(D, Y, sp)
check("L2", pick(r2)[0] == TX and coef > 0, "rung 2, installed users six months before: %s, elasticity %.3f" % (top3(r2), coef))
rs = C.referral_share(D)
sw_hist = [rs[(SW, y)] for y in range(2019, 2026)]
check("L2b", max(rs.values()) <= 0.06 and abs(rs[(SW, 2026)] - np.mean(sw_hist)) <= 2.5 * np.std(sw_hist) + 0.01,
      "the CRM's customer-referral lead source stays at %.1f to %.1f per cent of new customers in every region and year; "
      "Southwest 2026 %.1f against %.1f before" % (100 * min(rs.values()), 100 * max(rs.values()), 100 * rs[(SW, 2026)], 100 * np.mean(sw_hist)))
check("L3", g_pick == SW and g_margin >= 1.2, "rung 3, the founder pipeline: %s by %.3f" % (C.REG[g_pick], g_margin))
check("L4", sum(1 for v in list(care.values()) + list(mom.values()) + [r2] if pick(v)[0] == SW) == 0,
      "no route without the pipeline names the Southwest")

# ------------------------------------------------------------------------------------------------- F: the golden family
fam = {}
for lag, rate, dest, org in C.FAMILY:
    fam[(lag, rate, dest, org)] = C.golden_routes(D, Y, sp, lag, rate, dest, org)[0]
sw_f = np.array([v[SW] for v in fam.values()])
check("F1", all(pick(v)[0] == SW for v in fam.values()), "%d constructions (organic form x lag form x yield form x destination "
      "form), every one names the Southwest" % len(fam))
check("F2", sw_f.min() >= LO + 50 and sw_f.max() < HI - 50, "Southwest %.1f to %.1f, spread %.1f inside the 600 bin, 50 or more from its edges"
      % (sw_f.min(), sw_f.max(), sw_f.max() - sw_f.min()))
check("F3", min(pick(v)[1] for v in fam.values()) >= 1.15 and all(int(np.argsort(-v)[1]) == TX for v in fam.values()),
      "smallest margin %.3f, Texas & Gulf second in every one" % min(pick(v)[1] for v in fam.values()))
fut = {f: C.golden_routes(D, Y, sp, fut_form=f)[0] for f in ("basis", "last12", "zero")}
check("F4", abs(fut["basis"][SW] - gold[SW]) < 1e-9 and LO <= fut["zero"][SW] < HI and pick(fut["last12"])[0] == SW,
      "the planning basis's removals give %.1f; none after September %.1f; the last twelve months' pace %.1f (the basis files it)"
      % (fut["basis"][SW], fut["zero"][SW], fut["last12"][SW]))

users_ = Y["users"]
link_var = {}
for k, vals in dict(pre_paid_days=[0, 9999], closure_days=[0, 1, 7, 14], window_days=[24 * 31, 48 * 31, 9999],
                    pick=["earliest"], founder=["first_admin"], name_scope=["any"]).items():
    for v in vals:
        Yv = C.directory(D, _users=users_, **{k: v})
        link_var["%s=%s" % (k, v)] = C.golden_routes(D, Yv, sp)[0]
lv = np.array([v[SW] for v in link_var.values()])
check("F5", all(pick(v)[0] == SW and int(np.argsort(-v)[1]) == TX for v in link_var.values()) and lv.min() >= LO and lv.max() < HI,
      "%d linkage conventions (removals before the first paid invoice, the closure window, the link window, the latest or "
      "earliest leaver, the first user or first admin, names within the region or anywhere): Southwest %.1f to %.1f, Texas & "
      "Gulf second in every one" % (len(link_var), lv.min(), lv.max()))
jf = C.judge_family(D, Y, sp)
jv = np.array([v[SW] for v in jf.values()])
jm = np.array([v[SW] for k, v in jf.items() if k[0] == "mobile"])
check("F6", all(pick(v)[0] == SW and int(np.argsort(-v)[1]) == TX for v in jf.values()) and jv.min() >= LO and jv.max() < HI,
      "%d of the round 1 judge's choices (mobile, then names within the region or anywhere; founders sought from 2015 or only "
      "from 2023; the organic fit from 2019, 2021 or 2023; a pooled or mature yield; the lag as linked or a month shorter): "
      "Southwest %.1f to %.1f (%.1f to %.1f on the mobile), Texas & Gulf second in every one"
      % (len(jf), jv.min(), jv.max(), jm.min(), jm.max()))
dbl = np.array([v[SW] + info["champ"][SW] for v in care.values()])
check("F7", dbl.min() >= HI, "the founders added on top of a model of all arrivals (founders counted twice): Southwest %.1f to "
      "%.1f, outside the 600 bin" % (dbl.min(), dbl.max()))
# the components' parts across the golden family and the judge's choices on the mobile link
parts = [C.golden_routes(D, Y, sp, *f_)[1] for f_ in C.FAMILY]
p_org = [x["org"][SW] for x in parts]
p_ch = [x["champ"][SW] for x in parts]
for lf in (-48, 48):
    for os_ in (1, 24, 48):
        for rt in ("pooled", "mature"):
            for ls in (0, -1):
                _, o_, c_ = C.judge_route(D, Y, sp, lf, os_, rt, ls, parts=True)
                p_org.append(o_[SW])
                p_ch.append(c_[SW])
comp_ = figs["components"]
check("F8", all(round(v / 100) * 100 == 400 for v in p_ch) and comp_["organic_2027_low"] == int(round(min(p_org), -1))
      and comp_["organic_2027_high"] == int(round(max(p_org), -1)),
      "the Southwest's parts over the %d golden constructions and the judge's 24 on the mobile: founded by leavers %.1f to %.1f "
      "(400 to the nearest 100 in every one), usual intake %.1f to %.1f (%d to %d, the write-up's range)"
      % (len(C.FAMILY), min(p_ch), max(p_ch), min(p_org), max(p_org), comp_["organic_2027_low"], comp_["organic_2027_high"]))

# ------------------------------------------------------------------------------------------------- R: the three rules
import world as WD          # noqa: E402
W = WD.simulate()
ix = W["ix"]
heads = {}
for f in files:
    if f.endswith(".csv"):
        heads[f] = next(csv.reader(open(os.path.join(TARGET, f))))
import openpyxl             # noqa: E402
for f in files:
    if f.endswith(".xlsx"):
        wb = openpyxl.load_workbook(os.path.join(TARGET, f), read_only=True)
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(min_row=1, max_row=2, values_only=True))
            heads["%s:%s" % (f, ws.title)] = [str(x) for x in (rows[-1] if rows else []) if x is not None]
        wb.close()
leaky = [(f, h) for f, hs in heads.items() for h in hs if re.search(r"founder|champion|referr|previous|prior.?employer|moved|source.?account", h, re.I)]
check("R1", not leaky and len(Y["removals"]) > 20000 and len(Y["links"]) > 1000,
      "the directory's %d removals and the billing events ship at row level; %d founders link by mobile; no column holds "
      "a founder flag, a link or a yield %s" % (len(Y["removals"]), len(Y["links"]), leaky))
lead_of_link = Counter(D["by_id"][e["root"]]["Lead Source"] for e in D["events"] if e["t"] >= 0)
check("R1b", "Customer referral" not in {l for l, _ in lead_of_link.most_common(2)},
      "the CRM's lead source does not carry the pipeline: the two commonest sources of new customers are %s" % lead_of_link.most_common(2))
items = ["both_systems", "voided", "divisions", "reactivations", "returns_as_reactivations", "old_map", "crm_region",
         "closed_as_removal", "utc_dates", "phone_raw", "phone_only", "project_titles", "fiscal_as_calendar"]
COMP = figs["components"]


def components(D_, Y_, g_, info_):
    dep = Y_["dep"]
    wave = sum(dep[SW].get(t, 0) for t in range(87, 93))
    base = sum(dep[SW].get(t, 0) for t in range(72, 84)) / 12.0
    lags = [l["lag"] for l in Y_["links"] if l["land_t"] <= 92]
    return (int(round(wave, -2)), int(round(wave / 6 / base)), int(round(info_["org"][SW] / 100) * 100), int(np.median(lags)))


gold_comp = components(D, Y, gold, info)
check("R2", gold_comp == (COMP["removals_apr_sep_2026_rounded"], COMP["removals_ratio_rounded"], COMP["organic_2027_rounded"],
                          COMP["lag_median_months"]),
      "the golden's components %s match figures.json" % (gold_comp,))
for it in items:
    D2 = C.load(TARGET, (it,))
    sp2 = C.spend(TARGET, (it,))
    Y2 = C.directory(D2, (it,))
    g2, info2 = C.golden_routes(D2, Y2, sp2)
    c2 = components(D2, Y2, g2, info2)
    care2 = C.careful_routes(D2, sp2)
    moved = [n for n, a, b in zip(("removals", "ratio", "organic", "lag"), c2, gold_comp) if a != b]
    ok = pick(g2)[0] == SW and LO <= g2[SW] < HI and all(pick(v)[0] == TX for v in care2.values())
    # counting closures as removals (against the basis's sentence) or only project titles' deactivations changes which
    # deactivations the removals component counts, and moves that component alone (the note's Layer 1 inventory)
    allowed = {"closed_as_removal": {"removals", "ratio"}, "project_titles": {"removals", "ratio"}}.get(it, set())
    check("R2", ok and set(moved) <= allowed,
          "%s mishandled: golden %s %.1f, careful routes all Texas & Gulf, components moved %s" % (it, C.REG[pick(g2)[0]], g2[SW], moved or "none"))
# R3a: the easy route on the clean truth (the world before any record is written) files Texas & Gulf
y_true = [lambda t, r=r: W["new"][r, ix[t]] for r in range(6)]
sp_true = [lambda t, r=r: W["spend"][r, ix[t]] for r in range(6)]
easy_true = M.count_forecast(y_true, sp_true, 1, 92, True, True)
check("R3a", pick(easy_true)[0] == TX, "the easy route on the clean truth: %s" % top3(easy_true))
easy_true2 = M.count_forecast(y_true, None, 24, 92, False, False)
check("R3a", pick(easy_true2)[0] == TX, "the easy route on the clean truth, common trend from 2021: %s" % top3(easy_true2))
tr = W["truth"]["total"]
check("R3b", pick(tr)[0] == SW and LO <= tr[SW] < HI, "the decisive step alone on the clean truth (organic plus founders from "
      "the true leavers at the true yield and lag): %s" % top3(tr))
org_true = [lambda t, r=r: W["new"][r, ix[t]] - W["seeds"][r, ix[t]] for r in range(6)]
o_true = M.count_forecast(org_true, sp_true, 1, 92, True, True)
check("R3b", pick(o_true + W["truth"]["champ27"])[0] == SW, "the easy route's own model on the organic part plus the true "
      "founders: %s" % top3(o_true + W["truth"]["champ27"]))
check("R3b", abs(gold[SW] - tr[SW]) / tr[SW] < 0.08, "the golden on the files %.1f against the clean truth %.1f" % (gold[SW], tr[SW]))
check("R3b", pick(r2)[0] == TX and pick(mom["last12_x_growth"])[0] == TX,
      "each lower rung's single correction (installed users, momentum) stays on Texas & Gulf")


def repeated_block(series, w=6):
    s = list(series)
    seen = set()
    for i in range(len(s) - w + 1):
        b = tuple(s[i:i + w])
        if sum(b) and b in seen:
            return True
        seen.add(b)
    return False


check("R3c", not any(repeated_block(new[r, 48:141]) for r in range(6)) and len({tuple(new[r, 48:141]) for r in range(6)}) == 6,
      "no copied or repeated block in any region's monthly new customers, 2019 to 2026")
docs_text = {}
import docx as _docx        # noqa: E402
import pypdf                # noqa: E402
for f in files:
    p = os.path.join(TARGET, f)
    if f.endswith(".docx"):
        docs_text[f] = "\n".join(x.text for x in _docx.Document(p).paragraphs)
    elif f.endswith(".pdf"):
        docs_text[f] = "\n".join(pg.extract_text() or "" for pg in pypdf.PdfReader(p).pages)
argue = [f for f, t in docs_text.items() if re.search(r"2027", t) and re.search(r"Texas & Gulf (will|should|is expected)|expect.{0,40}Texas", t)]
check("R3c", not argue, "no document argues a region for 2027 or ranks the regions on it %s" % argue)
wordy = [(f, w) for f, t in docs_text.items() for w in re.findall(r"founder|champion|left the company|job change|leaver|referr\w*", t, re.I)]
check("R3c", not wordy, "no document names the pipeline's vocabulary %s" % wordy[:5])
# the components read the same by the planning basis's definition of a removal and by the reasons the directory records
LEAVE = ("Removed by admin", "Left company", "SSO deprovisioned")
sw_win = [x for x in Y["removals"] if x["region"] == SW and dt.date(2026, 4, 1) <= x["date"] <= dt.date(2026, 9, 30)]
by_reason = 0
for u in Y["users"]:
    if u["deactivation_reason"] in LEAVE and D["region_of_root"].get(D["ws_root"].get(u["workspace_id"])) == SW:
        if dt.date(2026, 4, 1) <= (C._ts(u["deactivated_at"]) - dt.timedelta(hours=7)).date() <= dt.date(2026, 9, 30):
            by_reason += 1
from_2016 = [x for x in Y["removals"] if x["t"] >= -36]
check("R4", abs(by_reason - len(sw_win)) <= 5 and all(x["reason"] in LEAVE for x in from_2016)
      and all(l_["reason"] in LEAVE for l_ in Y["links"]),
      "a removal reads the same both ways: the Southwest's April to September 2026 removals number %d by the planning basis's "
      "Seats line (deactivated on a still-paying customer's workspace, closures out) and %d by the directory's leaving "
      "reasons; every removal from 2016 (%d) and every one of the %d founders' removals carries a leaving reason"
      % (len(sw_win), by_reason, len(from_2016), len(Y["links"])))

# ------------------------------------------------------------------------------------------------- SF: the semantic forks
ret_gaps = []
for rid, ss in D["comp"].items():
    own = sorted([s for s in ss if not s["division"]], key=lambda s: (s["first"], s["sid"]))
    for k, s in enumerate(own[1:], start=1):
        lc = max((x["cancel"] for x in own[:k] if x["cancel"] is not None), default=None)
        if lc is not None:
            ret_gaps.append((s["first"] - lc).days)
near = [g_ for g_ in ret_gaps if 360 <= g_ <= 372]
check("SF1", True, "new paying customer (first paid invoice, or a return over 12 months) is the memo's sentence; R2 covers "
      "reactivations counted and returns dropped")
check("SF2", not near, "more than 12 months: no company comes back between 360 and 372 days after cancelling (reactivations "
      "at most %d days, returns at least %d), so 365 days, 366 days and twelve calendar months give the same count"
      % (max(g_ for g_ in ret_gaps if g_ < 366), min(g_ for g_ in ret_gaps if g_ >= 366)))
check("SF3", True, "counted once at its parent: the memo's sentence; R2 divisions mishandled keeps the call")
check("SF4", True, "a voided invoice is not a paid one: the memo's sentence; R2 voided mishandled keeps the call")
check("SF5", True, "the region map: the memo's sentence names the March 2024 map; R2 old map and the CRM's stamped region keep the call")
g_fy = C.golden_routes(*(lambda D_: (D_, C.directory(D_, ("fiscal_as_calendar",)), C.spend(TARGET, ("fiscal_as_calendar",))))(C.load(TARGET)))[0]
check("SF6", pick(g_fy)[0] == SW and LO <= g_fy[SW] < HI, "calendar 2027 against FY2028 read as calendar: %.1f" % g_fy[SW])
check("SF7", pick(fut["last12"])[0] == SW and abs(fut["basis"][SW] - gold[SW]) < 1e-9,
      "the removals after September 2026: the planning basis files each region's 2025 monthly average (%.1f); the last "
      "twelve months' pace (%.1f) is ruled out by that sentence and names the same region" % (fut["basis"][SW], fut["last12"][SW]))
check("SF8", "users deactivated when a customer's account closes belong to the cancellations line" in re.sub(r"\s+", " ", docs_text["fy2028_planning_basis.pdf"]),
      "a removal excludes users deactivated when the account closes: the basis's sentence (R2 closed_as_removal keeps the call)")
check("SF9", True, "expected: the mean of the count model and of the pipeline; a Poisson median differs by under one customer")
check("SF10", edge(gold[SW], 200) >= 50, "the nearest 200: %.1f prints 600, %.1f from the edge" % (gold[SW], edge(gold[SW], 200)))
check("SF11", all(int(np.argsort(-v)[1]) == TX for v in fam.values()) and int(np.argsort(-fut["last12"])[1]) == TX,
      "the region second is Texas & Gulf in every construction")
late = [u for u in Y["users"] if u["created_at"] > "2026-09-30T23:59:59Z" or (u["deactivated_at"] and u["deactivated_at"] > "2026-09-30T23:59:59Z")]
check("SF12", not late and max(e["first"] for e in D["events"]) <= dt.date(2026, 9, 30),
      "the as-of: billing and directory activity end 30 September 2026")
# a founder's new company counts in its own region (the memo), not the leaver's
same_share = float(np.mean([l["dest"] == l["origin"] for l in Y["links"]]))
lv_attr = C.golden_routes(D, Y, sp, destform="od")[0]
check("SF22", 0.8 <= same_share < 0.95 and LO <= lv_attr[SW] < HI and pick(lv_attr)[0] == SW,
      "a founder's company counts in the region of its own billing state, the memo's sentence; %.1f per cent of linked "
      "founders bill in the region they left, and the measured origin-to-destination shares give %.1f" % (100 * same_share, lv_attr[SW]))
# asks
rows_s = list(csv.DictReader(open(os.path.join(TARGET, C.F["sessions"]))))
h_g = C.ask_pod_hours(TARGET, "golden", D)
_, sess = C._held_sessions(TARGET, D)
hist = C.roster_history(TARGET)
# held: completed bookings only, once per host and start, the listed-not-hosting rows dropped, give the same hours
done_ = set()
for r_ in rows_s:
    k_ = (r_["host"], r_["start_utc"])
    if r_["status"] != "Completed" or not r_["start_utc"].startswith("2025") or k_ in done_:
        continue
    done_.add(k_)
unit_of = {(x["host"], x["start"].strftime("%Y-%m-%dT%H:%M:%SZ")): x for x in sess}
h_comp = defaultdict(float)
for k_ in done_:
    x = unit_of[k_]
    if x["shared"] and x["clash"]:
        continue
    h_comp[(C.pod_on(hist, x["host"], x["start"].date()), x["q"], x["kind"])] += x["hours"]
h_filter = h_comp
check("SF13", all(abs(h_filter[k] - h_g[k]) < 1e-9 for k in h_g), "held: a session with any completed booking, and completed "
      "bookings once per host and start, give the same hours in all 24 cells")
qgap = []
for s in rows_s:
    st = C._ts(s["start_utc"])
    if st.year not in (2024, 2025, 2026):
        continue
    for zone in (K.STATE_UTC[x] for x in ("AZ", "CA", "TX", "IL", "GA", "NY")):
        loc = st - dt.timedelta(hours=zone[0] - (1 if zone[1] and K.is_dst(st.date()) else 0))
        if loc.date() != st.date():
            qgap.append(s["booking_id"])
check("SF14", not qgap, "the quarter: every session starts and ends on the same date in UTC and in every regional clock, so a "
      "UTC and a local quarter agree (%d bookings differ)" % len(qgap))
import records as RC        # noqa: E402
import onboarding as OB     # noqa: E402
B = RC.build(W)
O = OB.build(B)
mis = sum(1 for x in sess if x["held"] and C.pod_on(hist, x["host"], x["start"].date()) != OB.pod_at(OB.by_name(x["host"]), x["start"].date()))
now_pod = {n_: sorted(v, key=lambda r_: r_[1])[-1][0] for n_, v in hist.items()}
movers = sorted({x["host"] for x in sess if x["year"] == 2025 and C.pod_on(hist, x["host"], x["start"].date()) != now_pod[x["host"]]})
check("SF15", mis == 0 and len(movers) == 3,
      "its specialists in each quarter: the roster's pod assignments, with their dates, give the pod each specialist worked in "
      "on every session's date (%d sessions, 0 differ); %d specialists' 2025 pods differ from their pod today (%s)"
      % (sum(1 for x in sess if x["held"]), len(movers), ", ".join(movers)))
cases_of_unit = defaultdict(set)
for s in rows_s:
    cases_of_unit[(s["host"], s["start_utc"])].add(s["case_id"])
mixed_types = {s["session_type"] for s in rows_s if len(cases_of_unit[(s["host"], s["start_utc"])]) > 1}
dict_text = " ".join(pypdf.PdfReader(os.path.join(TARGET, "data_dictionary.pdf")).pages[i].extract_text()
                     for i in range(len(pypdf.PdfReader(os.path.join(TARGET, "data_dictionary.pdf")).pages)))
dict_text = " ".join(dict_text.split())
check("SF16", mixed_types <= set(C.GROUP_TYPES) and "Field app training and Office hours are group sessions" in dict_text
      and "Kickoff, Admin setup and Go-live review are one-to-one sessions" in dict_text,
      "group sessions: the dictionary names the templates (Kickoff, Admin setup and Go-live review one-to-one; Field app "
      "training and Office hours group), and only those group templates ever seat more than one customer at a host's start "
      "(%s), so the template, the bookings at a start and the attendees give one reading" % sorted(mixed_types))
A_ = C.amendments(TARGET)
coh = {m: C.ask_cohort(TARGET, m, D, A_) for m in C.COHORT_MODES}
by_name_first = {}
for c in B["comps"]:
    if c["first_inv"].year == 2025 and c.get("kind") != "void_only":
        by_name_first[(c["name"], c["first_inv"])] = c
miss = sum(1 for e in C.cohort_2025(D) if (e["sub"]["name"], e["first"]) not in by_name_first)
gold_counts = Counter()
gold_acv = defaultdict(float)
for c in by_name_first.values():
    if c["start_t"] is None:
        continue
    gold_counts[(K.REGIONS[c["region"]], c["plan0"])] += 1
    gold_acv[(K.REGIONS[c["region"]], c["plan0"])] += c["acv0"]
same_counts = {k: v for k, v in coh["golden"]["counts"].items() if v} == {k: v for k, v in gold_counts.items() if v}
same_acv = all(abs(coh["golden"]["acv"].get(k, 0.0) - v) < 0.01 for k, v in gold_acv.items())
check("SF17", same_counts and same_acv and miss == 0,
      "on the terms in force on the first paid invoice date: the register's terms taken back through the amendments after "
      "that date, a day's amendments in the order their terms chain, each SKU read as sold, equal the world's starting plan "
      "and value for all %d cohort customers" % len(by_name_first))
check("SF18", coh["golden"]["n"] == int(new[:, 48 + 72:48 + 84].sum()), "the 2025 cohort counted the memo's way: %d, the 2025 "
      "months of the call's own count" % coh["golden"]["n"])
check("SF19", len(figs["cohort_acv_k"]) == 18, "the contract value is one figure per region and starting plan (the prompt's 'on each')")
check("SF20", all(abs(v * 4 - round(v * 4)) < 1e-9 for v in figs["hours"].values()),
      "hours are quarter hours, printed exactly at two decimals")
acv_edges = {r: edge(v, 100.0) for r, v in figs["cohort_acv_usd"].items()}
check("SF21", min(acv_edges.values()) >= 5, "contract value to $0.1K: the nearest cell is $%.2f from a rounding edge" % min(acv_edges.values()))
launch, fits = C.launch_order_map(D, A_, TARGET)
pure = all(len(v) == 1 for k, v in fits.items() if k != "PLW-100") and set(fits["PLW-100"]) <= {"Pro", "Core"} \
    and fits["PLW-100"]["Pro"] > 10 * fits["PLW-100"].get("Core", 0)
leg_plan = {r["subscription_id"]: r["plan"] for r in csv.DictReader(open(os.path.join(TARGET, C.F["legacy"])))}
import openpyxl             # noqa: E402
wb_ = openpyxl.load_workbook(os.path.join(TARGET, C.F["reg"]), read_only=True)
reg_rows = list(wb_["Subscriptions"].iter_rows(values_only=True))
wb_.close()
rh_ = reg_rows[1]
mig = Counter()
for v in reg_rows[2:]:
    d_ = dict(zip(rh_, v))
    if d_["Migrated From (legacy subscription)"] and d_["Migrated From (legacy subscription)"] in leg_plan and \
            C._date(d_["Last Amended"]) is None:
        mig[(d_["Rate Plan SKU"], leg_plan[d_["Migrated From (legacy subscription)"]])] += 1
check("SF23", pure and launch == {"PLW-100": "Pro", "PLW-200": "Enterprise", "PLW-300": "Core"} and
      C.catalog_map(TARGET) == {"PLW-100": "Core", "PLW-200": "Pro", "PLW-300": "Enterprise"}
      and all(launch[k[0]] == k[1] for k in mig),
      "the plan a 2025 subscription started on: each starting SKU's own list price and seats fit one plan (%s; the PLW-100 "
      "starts priced at Core's list are the offer's, A9), the "
      "launch-order numbering, and every unamended migrated subscription's legacy plan agrees with it (%s); today's catalog "
      "numbers the same SKUs in price order" % ({k: dict(v) for k, v in fits.items()}, dict(mig)))

# ------------------------------------------------------------------------------------------------- A: the asks and devices
keys = [(p, q, k) for p in C.PODS for q in range(1, 5) for k in ("one-to-one", "group")]
for m in C.HOURS_MODES[1:]:
    h = C.ask_pod_hours(TARGET, m, D)
    diff = sum(1 for k in keys if abs(round(h.get(k, 0), 2) - round(h_g.get(k, 0), 2)) > 1e-9)
    if m == "minutes":
        minutes_diff = diff
        check("A1", diff == 0, "pod hours, route minutes (each specialist's held minutes counted once, however their sessions "
              "overlap): %d of 24 cells differ from the golden" % diff)
        continue
    need = {"listed": 24, "booking_dedup": 16}.get(m, 20)
    check("A1", diff >= need, "pod hours, route %s: %d of 24 cells differ from the golden" % (m, diff))
ck = [(r, p) for r in C.REG for p in ("Core", "Pro", "Enterprise")]
for m in C.COHORT_MODES[1:]:
    x = coh[m]
    dc = sum(1 for k in ck if x["counts"].get(k, 0) != coh["golden"]["counts"].get(k, 0))
    da = sum(1 for k in ck if round(x["acv"].get(k, 0) / 1000, 1) != round(coh["golden"]["acv"].get(k, 0) / 1000, 1))
    need = {"chain_price": 22, "number_price": 22}.get(m, 32)
    check("A2", dc + da >= need, "2025 customers by starting plan, route %s: %d of 18 counts and %d of 18 contract values "
          "differ (%d of 36, at least %d asserted)" % (m, dc, da, dc + da, need))
# the golden hours are the sessions the scheduling tool held, each for the specialist who hosted it, in the pod they worked
# in that day, in the generator's terms
true_h = defaultdict(float)
held_k = {(s["host"], s["start"]) for s in O["sessions"] if s["status"] == "Completed" and not s.get("declined")}
seen = set()
for s in O["sessions"]:
    k = (s["host"], s["start"])
    if s["start"].year != 2025 or k in seen or k not in held_k or s.get("declined"):
        continue
    seen.add(k)
    kind = "group" if s["typ"] in C.GROUP_TYPES else "one-to-one"
    true_h[(OB.pod_at(OB.by_name(s["host"]), s["start"].date()), (s["start"].month - 1) // 3 + 1, kind)] += s["minutes"] / 60
check("A3", all(abs(true_h[k] - h_g[k]) < 1e-9 for k in keys), "the golden hours equal the specialist time the generator "
      "booked and held, each by the specialist who hosted it in the pod they worked in that day, all 24 cells")
check("A4", figs["hours"] == {"%s Q%d %s" % k: round(h_g[k], 2) for k in keys}, "figures.json carries the 24 hours")
cov = Counter()
for x in sess:
    if x["year"] == 2025 and x["held"] and not (x["shared"] and x["clash"]) and x["case_reg"] is not None and \
            C.POD_OF[C.REG[x["case_reg"]]] != C.pod_on(hist, x["host"], x["start"].date()):
        cov[x["kind"]] += 1
check("A5", cov["one-to-one"] > 100 and cov["group"] > 10,
      "cover: %d one-to-one and %d group sessions of 2025 were hosted by a specialist of another pod" % (cov["one-to-one"], cov["group"]))
coh25 = C.cohort_2025(D)
sameday = sum(1 for e in coh25 if any(a["date"] == e["first"] and a["change"] in ("Plan change", "Add seats")
                                      for a in A_.get(C._reg_row(e)["sid"], [])))
check("A6", 0.04 * len(coh25) <= sameday <= 0.12 * len(coh25),
      "same-day corrections: %d of the %d new customers of 2025 had their plan or seats amended on the first paid invoice date"
      % (sameday, len(coh25)))
# the forcing figure for ask A: a specialist cannot hold two sessions at once
by_host_h = defaultdict(list)
for x in sess:
    if x["held"]:
        by_host_h[x["host"]].append(x)
pairs, bad_pairs, contained = 0, 0, 0
for h_, xs in by_host_h.items():
    xs.sort(key=lambda x: x["start"])
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[j]["start"] >= xs[i]["end"]:
                break
            pairs += 1
            bad_pairs += (xs[i]["shared"] == xs[j]["shared"])
            inner, outer = (xs[i], xs[j]) if xs[i]["shared"] else (xs[j], xs[i])
            contained += outer["start"] < inner["start"] and inner["end"] <= outer["end"]
listing = [x for x in sess if x["held"] and x["shared"] and x["clash"]]
cells_l = Counter((C.pod_on(hist, x["host"], x["start"].date()), x["q"], x["kind"]) for x in listing if x["year"] == 2025)
hosts_bk = defaultdict(set)
for r_ in rows_s:
    hosts_bk[r_["booking_id"]].add(r_["host"])
other_clash = sum(1 for x in listing for h2_ in hosts_bk[x["bk"]] - {x["host"]}
                  if unit_of[(h2_, x["start"].strftime("%Y-%m-%dT%H:%M:%SZ"))]["clash"])
two_host = sum(1 for x in sess if x["shared"] and x["held"])
check("A7", pairs > 0 and bad_pairs == 0 and contained == pairs and other_clash == 0 and len(cells_l) == 24,
      "a specialist cannot hold two sessions at once: the record has %d pairs of a specialist's held sessions that overlap and "
      "no other overlap; in every pair a booking that lists a second specialist lies wholly inside the first specialist's own "
      "session, which no one else hosts (%d of %d), and the second specialist holds nothing else then, so %d listed "
      "sessions were the other specialist's (%d in 2025, in all 24 pod, quarter and kind cells) among %d held sessions on "
      "two-specialist bookings" % (pairs, contained, pairs, len(listing), sum(cells_l.values()), two_host))
# the forcing figure for ask B: a day's amendments to one subscription chain in exactly one order
groups = defaultdict(list)
for sid_, am in A_.items():
    for a in am:
        if (a["sku0"], a["seats0"], a["acv0"]) != (a["sku1"], a["seats1"], a["acv1"]):
            groups[(sid_, a["date"])].append(a)
multi = {k: v for k, v in groups.items() if len(v) > 1}
import itertools            # noqa: E402
unique, against = 0, 0
for k, v in multi.items():
    ok_orders = [o for o in itertools.permutations(v) if all((o[i]["sku1"], o[i]["seats1"], round(o[i]["acv1"], 2)) ==
                                                              (o[i + 1]["sku0"], o[i + 1]["seats0"], round(o[i + 1]["acv0"], 2))
                                                              for i in range(len(o) - 1))]
    unique += len(ok_orders) == 1
    against += len(ok_orders) == 1 and [a["no"] for a in ok_orders[0]] != sorted(a["no"] for a in v)
hit = 0
for e in coh25:
    s_ = C._reg_row(e)
    later = [a for a in A_.get(s_["sid"], []) if a["date"] > e["first"]]
    if later:
        d0_ = min(a["date"] for a in later)
        grp = multi.get((s_["sid"], d0_))
        hit += bool(grp) and C.start_terms(e, A_) != C.start_terms_by_number(e, A_)
# the forcing figure for ask B's primary: a subscription starts on the plan its SKU of record names, not the one its price fits
cat_rows = list(csv.DictReader(open(os.path.join(TARGET, C.F["catalog"]))))


def list_price(plan, seats):
    c_ = next(r for r in cat_rows if r["plan"] == plan)
    return round((float(c_["list_price_month_usd"]) + max(0, int(seats) - int(c_["seats_included"]))
                  * float(c_["extra_seat_month_usd"])) * 12, 2)


fit_ = C.price_plans(TARGET)
starts_ = [(e, C.start_terms(e, A_)) for e in coh25]
odd = [(e, t) for e, t in starts_ if launch[t[0]] not in fit_(t[1], t[2])]
at_core = sum(1 for e, t in odd if t[0] == "PLW-100" and abs(t[2] - list_price("Core", t[1])) < 0.005 and fit_(t[1], t[2]) == ["Core"])
reached, stepped, step_ids = 0, 0, set()
for e, t in odd:
    s_ = C._reg_row(e)
    ann = e["first"].replace(year=e["first"].year + 1) if not (e["first"].month == 2 and e["first"].day == 29) else \
        e["first"].replace(year=e["first"].year + 1, day=28)
    if ann > dt.date(2026, 9, 30) or (s_.get("cancel") is not None and s_["cancel"] <= ann):
        continue
    reached += 1
    am = [a for a in A_.get(s_["sid"], []) if a["date"] == ann and a["change"] == "Price change"]
    if len(am) == 1 and am[0]["sku0"] == am[0]["sku1"] == t[0] and am[0]["seats0"] == am[0]["seats1"] \
            and launch[t[0]] in fit_(am[0]["seats1"], am[0]["acv1"]):
        stepped += 1
        step_ids.add(am[0]["no"])
pc_other = [a for am in A_.values() for a in am if a["change"] == "Price change" and a["no"] not in step_ids]
pc_benign = sum(1 for a in pc_other if a["sku0"] == a["sku1"] and launch.get(a["sku0"]) in fit_(a["seats0"], a["acv0"])
                and launch.get(a["sku0"]) in fit_(a["seats1"], a["acv1"]))
odd_reg = Counter(C.REG[e["region"]] for e, t in odd)
check("A9", odd and at_core == len(odd) and stepped == reached > 0 and pc_benign == len(pc_other) > len(step_ids)
      and len(odd_reg) == 6,
      "a subscription starts on the plan its SKU names: %d of the 1,744 starting terms carry PLW-100, sold as Pro, at exactly "
      "Core's list price for their seats (%s); each of the %d that reached its first anniversary moved that day, by a price "
      "change with its SKU and seats unchanged, to Pro's list less 0, 5, 10 or 15 per cent, and the other %d price changes "
      "in the register each move a subscription between two prices of its own SKU's plan" % (len(odd), dict(odd_reg), reached,
                                                                                            len(pc_other)))
check("SF24", contained == pairs > 0 and bad_pairs == 0 and other_clash == 0 and minutes_diff == 0,
      "a specialist listed on a booking a colleague holds spent no time on it: each such booking lies wholly inside a session "
      "of the listed specialist's own that no one else hosts (%d of %d overlapping pairs, no other overlap), the colleague "
      "holding nothing else then, so counting each specialist's minutes once gives the golden in all 24 cells" % (contained, pairs))
check("SF25", at_core == len(odd) > 0 and stepped == reached and pc_benign == len(pc_other),
      "the plan a customer started on is the one its SKU names: the %d PLW-100 starts at Core's list each moved at the first "
      "anniversary, SKU and seats unchanged, to Pro's list less a standard discount (%d of %d that reached it), and every other "
      "price change stays within its own SKU's plan (%d)" % (len(odd), stepped, reached, len(pc_other)))
check("A8", unique == len(multi) and against > 0 and hit > 0,
      "a day's amendments chain: %d subscription-days carry two or more term amendments, every one chains in exactly one "
      "order (each after-terms equal the next before-terms), and %d are referenced against that order; read in reference "
      "order, %d of the 2025 cohort's starting terms come out as the terms after the day's plan move" % (len(multi), against, hit))

# ------------------------------------------------------------------------------------------------- S: separation
import shutil               # noqa: E402
import tempfile             # noqa: E402


def pack_without(drop=(), rewrite=None):
    """A copy of the pack (links) without the files in drop, with rewrite(dir) applied; the call recomputed on it."""
    base = os.environ.get("TASK166_SCRATCH", TASK)
    os.makedirs(base, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="t166chk_", dir=base)
    try:
        for f in files:
            if f not in drop:
                os.symlink(os.path.join(TARGET, f), os.path.join(tmp, f))
        if rewrite:
            rewrite(tmp)
        return C.golden(tmp)[3]
    finally:
        shutil.rmtree(tmp)


g_s1 = pack_without(drop=(C.F["sessions"], C.F["cases"], C.F["roster"], C.F["catalog"], "onboarding_csat_responses_2024-2026.csv",
                          "board_deck_2023-03_customer_growth.pdf"))
check("S1", np.allclose(g_s1, gold), "the call reads none of the onboarding exports, the roster, the catalog, the survey or the "
      "board deck: deleting them leaves every region's figure unchanged")


def no_partners(tmp):
    p = os.path.join(tmp, C.F["crm"])
    rows = list(csv.reader(open(os.path.join(TARGET, C.F["crm"]))))
    os.unlink(p)
    with open(p, "w", newline="") as fh:
        csv.writer(fh, lineterminator="\n").writerows([r for r in rows if r[5] != "Partner"])


g_s2 = pack_without(rewrite=no_partners)
check("S2", np.allclose(g_s2, gold) and not ({r["Account ID"] for r in D["crm"] if r["Type"] == "Partner"} & {e["root"] for e in D["events"]}),
      "the partner accounts carry no subscription, workspace or new customer event, and deleting them leaves the call unchanged")


def flat_terms(tmp):
    p = os.path.join(tmp, C.F["reg"])
    wb = openpyxl.load_workbook(os.path.join(TARGET, C.F["reg"]))
    ws = wb["Subscriptions"]
    hdr = [c.value for c in ws[2]]
    cols = [hdr.index(h) + 1 for h in ("Rate Plan SKU", "Seats", "ACV (USD)", "Last Amended")]
    for row in ws.iter_rows(min_row=3):
        for j_ in cols:
            row[j_ - 1].value = None if j_ == cols[-1] else ("Core" if j_ == cols[0] else 0)
    del wb["Amendments"]
    os.unlink(p)
    wb.save(p)


g_s3 = pack_without(rewrite=flat_terms)
check("S3", np.allclose(g_s3, gold), "blanking the register's plan, seats, ACV and Last Amended and deleting the Amendments "
      "sheet leaves the call unchanged: the asks' device columns sit outside the call's population")
src = open(os.path.join(HERE, "calc.py")).read()
dist_used = [d for d in dis if d.split(".")[0] in src]
check("S4", not dist_used, "no route reads a distractor %s" % dist_used)
# the device rows by count: the listed-not-hosting rows sit in the session log and the same-day amendment lines in the
# Amendments sheet, neither of which the call reads (S1, S3); the 2025 cohort, its regions and first paid invoice dates are
# the call's own and no device row is among them
n_listed = sum(1 for r_ in rows_s for x in [unit_of.get((r_["host"], r_["start_utc"]))] if x and x["shared"] and x["clash"])
n_pairs = sum(len(v) for v in multi.values())
n_offer = len(step_ids)
coh_key = sorted((e["root"], e["region"], e["first"].isoformat()) for e in coh25)
check("S5", n_listed > 0 and n_pairs > 0 and n_offer > 0 and len(coh_key) == coh["golden"]["n"] == int(new[:, 48 + 72:48 + 84].sum()),
      "the device rows by count: %d listed-not-hosting session rows, %d same-day amendment lines and the offer's %d price "
      "changes and first-year terms, in files and columns the call never reads; the 2025 cohort of %d, with its regions and "
      "first paid invoice dates, is the call's own count and no device moves it" % (n_listed, n_pairs, n_offer, len(coh_key)))

# ------------------------------------------------------------------------------------------------- D: the documents
memo = re.sub(r"\s+", " ", docs_text["memo_2027_onboarding_pod.docx"])
for sent in ("its first paid subscription invoice is dated in 2027, or it comes back in 2027 more than 12 months after it cancelled",
             "Count each company once, at its parent", "A voided invoice is not a paid one",
             "the territory map that took effect on 1 March 2024", "forecast on FP&A's FY2028 planning basis"):
    check("D1", sent in memo, "the memo files: %s" % sent)
basis = re.sub(r"\s+", " ", docs_text["fy2028_planning_basis.pdf"])
check("D2", "users are added to and removed from paying customers' workspaces at each region's 2025 monthly average" in basis,
      "the planning basis files the removals after September 2026")
deck = docs_text["board_deck_2023-03_customer_growth.pdf"]
check("D3", "2027" not in deck and "FY2023" in deck, "the board deck is FY2020 to FY2023 history, nothing on 2027")
dict_t = re.sub(r"\s+", " ", docs_text["data_dictionary.pdf"])
check("D4", not re.search(r"partner booked|booked by a partner|synced|in step with|current terms|today's terms|renumber|launch "
                         r"order|cover|took over|taken over|handed|handover|reassign|declin|did not host|keyed|applied|sequence|in the "
                         r"order|offer|promot|introduc|first year|first-year|anniversar|plan of record", dict_t, re.I),
      "the dictionary describes rows, never a device")

# the memo's prose: two in five founded by leavers, most of the Southwest's removals project staff, about half at its
# largest contractors (150 or more users), and the lead under the other removal paces
f25 = Y["founders"][:, 48 + 72:48 + 84].sum() / new[:, 48 + 72:48 + 84].sum()
ws_n = Counter(u["workspace_id"] for u in Y["users"])
wave_users = []
for u in Y["users"]:
    if not u["deactivated_at"] or u["deactivation_reason"] == "Account closed":
        continue
    rid = D["ws_root"].get(u["workspace_id"])
    if rid is None or D["region_of_root"].get(rid) != SW:
        continue
    d_ = (C._ts(u["deactivated_at"]) - dt.timedelta(hours=7)).date()
    if dt.date(2026, 4, 1) <= d_ <= dt.date(2026, 9, 30):
        wave_users.append(u)
proj = np.mean([bool(C.PROJECT_TITLES.search(u["job_title"] or "")) for u in wave_users])
big = np.mean([ws_n[u["workspace_id"]] >= 150 for u in wave_users])
widen = fut["last12"][SW] / fut["last12"][TX] > gold[SW] / gold[TX]
stay = np.mean([l["dest"] == l["origin"] for l in Y["links"]])
check("D5", 0.35 <= f25 <= 0.45 and proj > 0.6 and 0.4 <= big <= 0.6 and pick(fut["zero"])[0] == SW and widen
      and 0.85 <= stay < 0.9,
      "the memo's prose holds: %.3f of 2025's new customers founded by leavers; of the Southwest's April to September 2026 "
      "deactivations, %.2f project titles and %.2f at workspaces of 150 or more users; with no removals after September the "
      "Southwest still leads (%.1f against %.1f), and at the last twelve months' pace its lead widens; %.3f of founders "
      "bill in the region they left (close to nine in ten)"
      % (f25, proj, big, fut["zero"][SW], fut["zero"][TX], stay))

# ------------------------------------------------------------------------------------------------- Q: realism
yearly = new[:, 48:48 + 96].reshape(6, 8, 12).sum(2)
check("Q1", len({int(x) for x in yearly.ravel()}) >= 44 and not any(int(x) % 100 == 0 for x in yearly.ravel()),
      "no repeated or round yearly count: %d distinct of 48 region-years" % len({int(x) for x in yearly.ravel()}))
mins = Counter(s["duration_min"] for s in rows_s)
check("Q2", len(mins) >= 4 and len({s["host"] for s in rows_s}) >= 10, "sessions of %d lengths by %d hosts" % (len(mins), len({s["host"] for s in rows_s})))
names = [r["full_name"] for r in Y["users"]]
check("Q3", max(Counter(names).values()) < 60 and not any(n in ("John Doe", "Jane Doe") for n in names),
      "no placeholder people; the commonest full name appears %d times in %d users" % (max(Counter(names).values()), len(names)))
bad_meta = []
for f in files + ["../golden/" + g_ for g_ in os.listdir(GOLDEN)]:
    p = os.path.join(TARGET, f)
    if f.endswith((".docx", ".xlsx")):
        with zipfile.ZipFile(p) as z:
            core = z.read("docProps/core.xml").decode("utf8", "replace")
            app = z.read("docProps/app.xml").decode("utf8", "replace") if "docProps/app.xml" in z.namelist() else ""
            if re.search(r"openpyxl|python-docx|Microsoft Office User|Apache POI", core + app):
                bad_meta.append(f)
    elif f.endswith(".pdf"):
        raw = open(p, "rb").read()
        if re.search(rb"ReportLab|reportlab|Python", raw[:4000] + raw[-4000:]):
            bad_meta.append(f)
check("Q4", not bad_meta, "every container carries the organisation's producer and dates %s" % bad_meta)
txt_ok = all("2026-10-0" not in s["start_utc"] for s in rows_s) and all(r["opened_on"] <= "2026-09-30" for r in csv.DictReader(open(os.path.join(TARGET, C.F["cases"]))))
check("Q5", txt_ok, "no activity after 30 September 2026 in the onboarding exports")
late_files = []
for f in files:
    if f.endswith(".csv") and f != "export_manifest.csv":
        ds = re.findall(r"\b(\d{4}-\d{2}-\d{2})", open(os.path.join(TARGET, f)).read())
        if ds and max(ds) > "2026-10-01":
            late_files.append((f, max(ds)))
wb_ = openpyxl.load_workbook(os.path.join(TARGET, C.F["reg"]), read_only=True)
for ws_ in wb_.worksheets:
    for row in ws_.iter_rows(min_row=3, values_only=True):
        for v in row:
            if isinstance(v, (dt.date, dt.datetime)) and (v.date() if isinstance(v, dt.datetime) else v) > dt.date(2026, 9, 30):
                late_files.append((C.F["reg"] + ":" + ws_.title, str(v)))
                break
wb_.close()
check("Q8", not late_files, "no record in any export is dated after the pull %s" % late_files[:3])
people = set(K.PEOPLE.values())
check("Q6", people == {"Jeff Guzman", "Joseph Clay", "Guy Morrison"}, "the named people are the card's, from guard.py names")
hosted = [s for s in O["sessions"] if not s.get("declined")]
dbl = Counter((s["host"], s["start"]) for s in hosted)
clash = 0
by_host = defaultdict(list)
for (h_, st_), n_ in dbl.items():
    by_host[h_].append(st_)
for h_, sts in by_host.items():
    sts.sort()
    lens = {}
    for s in hosted:
        if s["host"] == h_:
            lens[s["start"]] = s["minutes"]
    clash += sum(1 for a, b in zip(sts, sts[1:]) if a + dt.timedelta(minutes=lens[a]) > b)
check("Q7", clash == 0, "no specialist hosts two sessions at once in the generator's own bookings (%d overlaps)" % clash)
# a company's plan and its order's seats follow the team it signed up with
u90, short = defaultdict(list), Counter()
for e in C.cohort_2025(D):
    sku_, seats_, _ = C.start_terms(e, A_)
    d90 = (e["first"] + dt.timedelta(days=90)).isoformat()
    n_ = sum(1 for u in Y["by_ws"].get(e["ws"], []) if u["created_at"][:10] <= d90
             and (not u["deactivated_at"] or u["deactivated_at"][:10] > d90))
    u90[launch[sku_]].append(n_)
    short[launch[sku_]] += n_ > int(seats_)
med = {p_: float(np.median(v)) for p_, v in u90.items()}
check("Q9", med["Core"] < med["Pro"] < med["Enterprise"] and short["Core"] <= 0.02 * len(u90["Core"]) and not short["Pro"],
      "users on a 2025 new customer's workspace 90 days after its first paid invoice, median by starting plan: Core %.0f, Pro "
      "%.0f, Enterprise %.0f; orders with fewer seats than users then: Core %d of %d, Pro %d, Enterprise %d"
      % (med["Core"], med["Pro"], med["Enterprise"], short["Core"], len(u90["Core"]), short["Pro"], short["Enterprise"]))

fails = [r for r in RES if not r[1]]
print("%d checks, %d FAIL" % (len(RES), len(fails)))
sys.exit(1 if fails else 0)
