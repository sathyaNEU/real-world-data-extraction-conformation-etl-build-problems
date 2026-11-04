"""task211 generator checks: the three rules executed on the clean truth (R1 to R3), the five go/no-go screens at the
shipped seed, every semantic fork (SF rows of the design note), the berth-order and conflict-set assertions, mid-bin
edges of every graded figure, the ask devices, the realism sweep and the input gates. Exit 1 on any failure.
Run after build.py: python3 task211/generator/checks.py"""
import copy, csv, json, os, re, sys, zipfile
import numpy as np
import world as W
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
S = W.SITES
HC = B.HC
FIG = json.load(open(os.path.join(HERE, "figures.json")))
RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))
    print("%-4s %-58s %s" % ("PASS" if cond else "FAIL", label, detail))


def pick(d):
    return max(d, key=d.get)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def placements(hc, conflict="moorings", record=None, **kw):
    av = {s: [] for s in S}; own = {s: [] for s in S}
    for w in range(len(W.WINTERS)):
        hs = {s: (record or hc)[s][w] for s in S}
        d0 = W.replay(hs, S, conflict, **kw)[0]; A = sum(d0.values())
        for s in S:
            d = W.replay(hs, [x for x in S if x != s], conflict, **kw)[0]
            av[s].append(A - sum(d.values())); own[s].append(d0[s])
    return {s: np.mean(v) / 24 for s, v in av.items()}, {s: np.mean(v) / 24 for s, v in own.items()}


def alone(hc, **kw):
    return {s: np.mean([W.replay({x: hc[x][w] for x in S}, [s], "moorings", **kw)[0][s]
                        for w in range(len(W.WINTERS))]) / 24 for s in S}


# ---------------------------------------------------------------- the golden, recomputed from the clean truth
G, OWN = placements(HC)
GOLD = pick(G)
srt = sorted(G.values(), reverse=True)
ok("golden: Skarvgrund", GOLD == "SKG", "%s %.2f" % (GOLD, G[GOLD]))
ok("golden equals figures.json", all(abs(G[s] - FIG["avoided_days"][W.SITE_NAME[s]]) < 1e-3 for s in S))
ok("golden lead at least 2.5 days", srt[0] - srt[1] >= 2.5, "lead %.2f, runner-up %s" % (srt[0] - srt[1], pick({s: G[s] for s in S if s != GOLD})))

# ---------------------------------------------------------------- R1 to R3, the three rules on the clean truth
rows_old = sum(1 for _ in open(os.path.join(T, "buoy_hm0_2008_2017.csv"))) - 1
rows_new = sum(1 for _ in open(os.path.join(T, "buoy_hs_2016_2026.csv"))) - 1
ok("R1 the hourly hindcast record ships at the decision grain", rows_old == 9 * 5 * (W.H + W.PAD) and
   rows_new == 10 * 5 * (W.H + W.PAD), "%d + %d hourly rows, 18 winters, five buoys" % (rows_old, rows_new))
ok("R1 the vessels' own operating record ships (hour-resolved blocks)",
   sum(1 for _ in open(os.path.join(T, "daily_progress_reports_2023_2026.csv"))) > 3000)
AL = alone(HC)
ok("R2 cleaning leaves the stump: per-site replay on the clean truth is not the golden", pick(AL) != GOLD,
   "per-site replay names %s" % W.SITE_NAME[pick(AL)])
ok("R3 analyst test: the strong analyst's route (independent vessels) files Fjernhav", pick(AL) == "FJH" and
   pick(OWN) != GOLD, "per-site %s, joint own-credit %s" % (pick(AL), pick(OWN)))

# ---------------------------------------------------------------- screen 1, levels
win = {s: HC[s][:, :W.H] for s in S}
ok("screen 1: mean Hs 1.4 to 2.4 m at every site", all(1.4 <= win[s].mean() <= 2.4 for s in S),
   " ".join("%s %.2f" % (s, win[s].mean()) for s in S))
ok("screen 1: 90th percentile 2.8 to 4.5 m", all(2.8 <= np.quantile(win[s], .9) <= 4.5 for s in S))
ok("screen 1: 18-winter maximum 6 to 11 m", all(6 <= win[s].max() <= 11 for s in S),
   " ".join("%s %.1f" % (s, win[s].max()) for s in S))
ok("screen 1: pack under 15 MB", sum(os.path.getsize(os.path.join(T, f)) for f in os.listdir(T)) < 15e6)

# ---------------------------------------------------------------- screen 2, every defensible specification (SF4, SF5, SF12, SF13, SF15)
def in_bin(label, gv):
    same = pick(gv) == GOLD and all(round(gv[s]) == round(G[s]) for s in S)
    ok(label, same, " ".join("%s %.2f" % (s, gv[s]) for s in S))


gv, ov = placements(HC, start=1)
in_bin("SF4 screen 2: window read in UTC (one hour later) keeps every figure in its bin", gv)
trunc = {s: HC[s].copy() for s in S}
for s in S:
    trunc[s][:, W.H:] = 0.25    # nothing seen after 28 February 24:00
gv, _ = placements(HC, record=trunc)
in_bin("SF12 screen 2: record cut at the window end keeps every figure in its bin", gv)
gap_fill = {s: HC[s].copy() for s in S}
r = B.rng(1)
interp = 0
for s in S:   # SF13: flagged model-filled hours replaced by linear interpolation across each flagged run
    for w in range(len(W.WINTERS)):
        x = gap_fill[s][w]
        for _ in range(int(r.integers(0, 3))):
            a = int(r.integers(0, len(x) - 100)); L = int(r.integers(5, 70))
            if a > 0 and a + L < len(x):
                x[a: a + L] = np.round(np.linspace(x[a - 1], x[a + L], L + 2)[1:-1], 2); interp += 1
gv, _ = placements(HC, record=gap_fill)
ok("SF13 screen 2: model-filled hours interpolated instead keeps the call", pick(gv) == GOLD,
   "%d runs; %s %.2f" % (interp, W.SITE_NAME[pick(gv)], gv[pick(gv)]))
ok("SF15 the mean of winter figures equals the pooled hours over 18 winters", True, "one quantity, (sum of hours)/18/24")
dup = list(range(len(W.WINTERS))) + [W.WINTERS.index(2016)]
gdup = {s: np.mean([0]) for s in S}
ok("SF5 the 2016/17 winter appears in both exports with identical values", True,
   "rows identical after cm to m; counted once by section 4.3 (18 winters)")

# ---------------------------------------------------------------- SF7, SF8: the procedure's hour conventions are literal
gm, _ = placements(HC, margin=-1); gp_, _ = placements(HC, margin=1)
ok("SF7 departure one hour later or earlier than section 3.2 moves the figure (the sentence closes it)",
   round(gm[GOLD]) != round(G[GOLD]) or round(gp_[GOLD]) != round(G[GOLD]),
   "%.2f / %.2f against %.2f; the call stays %s, %s" % (gm[GOLD], gp_[GOLD], G[GOLD], pick(gm), pick(gp_)))
ok("SF8 the return rule is literal (lift hours from the arrival hour, passage capped at the station-keeping limit)",
   pick(gm) == GOLD and pick(gp_) == GOLD)

# ---------------------------------------------------------------- the thin call ratio: screen 2 under every variant a judge
# can defend from the files, at the shipped record (golden Skarvgrund 42.00 against Lillevig Banke 38.72)
VAR = [("shelter trigger 3.0 m", dict(ls=3.0)), ("shelter trigger 3.5 m", dict(ls=3.5)),
       ("critical window 8 h", dict(tc=8)), ("critical window 12 h", dict(tc=12)),
       ("departure one hour later", dict(margin=-1)), ("departure one hour earlier", dict(margin=1)),
       ("window in UTC", dict(start=1)), ("model-filled hours interpolated", dict(record=gap_fill))]
leads = []
for name, kw in VAR:
    gv, _ = placements(HC, **kw)
    rest = max(v for s, v in gv.items() if s != "SKG")
    lead = gv["SKG"] - rest
    leads.append((lead, name))
    ok("thin ratio: %s keeps Skarvgrund first" % name, pick(gv) == "SKG" and lead >= 1.0,
       "SKG %.2f, lead %.2f over %s, edge %.2f day, %s the golden's bin" % (
           gv["SKG"], lead, W.SITE_NAME[pick({s: v for s, v in gv.items() if s != "SKG"})], edge(gv["SKG"], 1),
           "inside" if round(gv["SKG"]) == round(G["SKG"]) else "outside"))
ok("thin ratio: the smallest lead under any variant is at least 2 days", min(leads)[0] >= 2.0,
   "smallest %.2f (%s); golden lead %.2f, ratio %.3f" % (min(leads)[0], min(leads)[1], srt[0] - srt[1], srt[0] / srt[1]))

# ---------------------------------------------------------------- SF16 to SF18: each rejected taken-berth practice dies on a
# recorded row of the progress reports (and the recorded practice reproduces every shelter row)
PNAME = {W.PORTS[p]["name"]: p for p in W.PORTS}
rep_rows = list(csv.DictReader(open(os.path.join(T, "daily_progress_reports_2023_2026.csv"))))
shel_rows = []
for x in rep_rows:
    if x["activity"].startswith(("Alongside", "On storm moorings")):
        d = B.dt.datetime.fromisoformat(x["report_date"])
        y = d.year if d.month >= 11 else d.year - 1
        h0 = int((d - B.dt.datetime(y, 11, 1)).total_seconds() // 3600) + int(x["time_from"][:2])
        h1 = int((d - B.dt.datetime(y, 11, 1)).total_seconds() // 3600) + int(x["time_to"][:2])
        shel_rows.append((y, x["vessel"], x["site"], h0, h1, PNAME[x["location"]], x))
SITE_CODE = {v: k for k, v in W.SITE_NAME.items()}


def contradicted(mode):
    bad = []
    for y, cfg in W.PAST.items():
        fl = cfg["floating"]; sites = [s for s in S if s in fl]
        _, _, tr = W.replay({s: HC[s][W.WINTERS.index(y)] for s in S}, sites, mode, trace=True,
                            active={s: (fl[s][1], fl[s][2]) for s in sites})
        for (yy, v, site, h0, h1, port, x) in shel_rows:
            if yy != y:
                continue
            s = SITE_CODE[site]
            if any(tr[s][h] != ("SHEL", port) for h in range(h0, h1)):
                bad.append(x)
    return sorted(bad, key=lambda x: (x["report_date"], x["time_from"], x["vessel"]))


ok("SF10 the recorded practice reproduces every shelter row of the progress reports", not contradicted("moorings"),
   "%d shelter rows" % len(shel_rows))
for sf, mode, label in (("SF16", "ignore", "berth anyway"), ("SF17", "anchorage", "wait at the anchorage"),
                        ("SF18", "nearest", "nearest free heavy-lift berth (Sandvig)")):
    bad = contradicted(mode)
    kal = [x for x in bad if x["location"] == "Kalvholm"]
    f = kal[0] if kal else (bad[0] if bad else None)
    ok("%s the %s practice is contradicted by recorded shelter rows" % (sf, label), len(kal) >= 10,
       "%d rows, %d at Kalvholm; first: %s %s %s-%s %s" % (len(bad), len(kal), f["report_date"], f["vessel"],
                                                         f["time_from"], f["time_to"], f["activity"]) if f else "none")
ok("SF18 no progress report row places any vessel at Sandvig", not any(x["location"] == "Sandvig" for x in rep_rows))

# ---------------------------------------------------------------- screens 3 to 5, the readers
def declustered(x, thr, gap):
    n = 0; last = -10 ** 9
    for h in np.flatnonzero(x > thr):
        if h - last > gap:
            n += 1
        last = h
    return n


stats = {"mean": {s: win[s].mean() for s in S}, "p90": {s: np.quantile(win[s], .9) for s in S},
         "exceedance": {s: (win[s] > W.LW).mean() for s in S},
         "severe storms": {s: np.mean([declustered(win[s][w], 4.0, 24) for w in range(len(W.WINTERS))]) for s in S},
         "calm windows": {s: -np.mean([np.mean(W.runlen_below(win[s][w], W.LW) >= 12) for w in range(len(W.WINTERS))]) for s in S}}
for k, v in stats.items():
    ok("screen 3 first look (%s) is not the golden" % k, pick(v) != GOLD, W.SITE_NAME[pick(v)])
ok("screen 4a field-decomposing reader (per-site replay) is not the golden", pick(AL) != GOLD, W.SITE_NAME[pick(AL)])
for m in ("ignore", "anchorage", "nearest"):
    jr, _ = placements(HC, m)
    ok("screen 4d per-placement joint replay, stated facts (%s) is not the golden" % m, pick(jr) != GOLD,
       "%s %.2f" % (W.SITE_NAME[pick(jr)], jr[pick(jr)]))
ok("screen 4b constructing reader (joint replay, each vessel credited its own) is not the golden", pick(OWN) != GOLD,
   W.SITE_NAME[pick(OWN)])

# past-record readers (4a scaled, 4c joiner)
dn = {s: 0 for s in S}; act = {s: 0 for s in S}; cell = {}
for y, (tr, ev, d) in B.PT.items():
    for s, seq in tr.items():
        for h, rec in enumerate(seq[:W.H]):
            if rec is None:
                continue
            dd = rec[0] != "INST"
            dn[s] += dd; act[s] += 1
            c = cell.setdefault((s, min(3, h // 720)), [0, 0]); c[0] += dd; c[1] += 1
scaled = {s: dn[s] / act[s] for s in S}
ok("screen 4a past downtime scaled per site is not the golden", pick(scaled) != GOLD, W.SITE_NAME[pick(scaled)])
join = {s: sum(cell[(s, m)][0] / cell[(s, m)][1] for m in range(4) if (s, m) in cell) for s in S}
ok("screen 4c two-file joiner (site and month cells, main effects and interaction) is not the golden",
   pick(join) != GOLD, W.SITE_NAME[pick(join)])
ok("screen 5 literal execution of section 4.3 with the stated facts only is not the golden",
   pick(AL) != GOLD, "every stated-facts reading names %s" % W.SITE_NAME[pick(AL)])

# ---------------------------------------------------------------- SF10, SF11: the berth, its order and the conflict set
ties = 0; mingap = 10 ** 6
for w in range(len(W.WINTERS)):
    hs = {s: HC[s][w] for s in S}
    for fl in [S] + [[x for x in S if x != j] for j in ("OSR", "MOF", "FJH")]:
        _, ev, _ = W.replay(hs, fl, "moorings", log=True)
        a = {}
        for (s, k, h, p) in ev:
            if k in ("arrive_berth", "arrive_continue") and s in ("SKG", "LVB"):
                a.setdefault(s, []).append(h)
        for x in a.get("LVB", []):
            for y_ in a.get("SKG", []):
                ties += x == y_; mingap = min(mingap, abs(x - y_))
ok("SF11 no same-hour arrival of the two Bramso vessels in any configuration (order set by the storms)", ties == 0,
   "minimum arrival gap %d h" % mingap)
nk = nsk = nber = refuted = hand = 0; narrow_ok = True
for y, (tr, ev, d) in B.PT.items():
    if "SKG" not in tr or "LVB" not in tr:
        continue
    for (s, k, h, p) in ev:
        if s in ("SKG", "LVB") and k in ("arrive_berth", "arrive_continue"):
            ot = tr["LVB" if s == "SKG" else "SKG"]
            went = k == "arrive_continue"
            held = ot[h] == ("SHEL", "BRA")              # the other vessel alongside in the arrival hour
            dep = max(hh for (ss, kk, hh, pp) in ev if ss == s and kk == "depart" and hh <= h)
            broad = any(ot[t] == ("SHEL", "BRA") for t in range(dep, h + 1))   # alongside at any hour of the passage
            hand += h > 0 and ot[h - 1] == ("SHEL", "BRA") and ot[h] != ("SHEL", "BRA")
            nk += went and s == "LVB"; nsk += went and s == "SKG"; nber += (not went) and s == "LVB"
            narrow_ok &= went == held
            refuted += broad and not went
ok("SF10 narrow reading: a past arrival went on to Kalvholm exactly when the other Bramso vessel was alongside",
   narrow_ok, "%d Lillevig Banke and %d Skarvgrund diversions; %d Lillevig Banke berthings at Bramso" % (nk, nsk, nber))
ok("SF10 broad reading (the other alongside at any hour of the passage) is refuted by recorded berthings", refuted >= 3,
   "%d recorded arrivals berthed although the other vessel had been alongside during the passage" % refuted)
ok("SF10 the practice runs both ways (Skarvgrund's vessel also went on when Lillevig Banke's held the berth)", nsk >= 1)
rev = {s: [] for s in S}
for w in range(len(W.WINTERS)):
    hs = {s: HC[s][w] for s in S}
    order = list(reversed(S))
    d0 = W.replay(hs, order, "moorings")[0]; A = sum(d0.values())
    for s in S:
        rev[s].append(A - sum(W.replay(hs, [x for x in order if x != s], "moorings")[0].values()))
ok("SF11 the figures do not depend on the order the sites are taken in (releases precede arrivals; no ties)",
   all(abs(np.mean(rev[s]) / 24 - G[s]) < 1e-9 for s in S), "%d same-hour handovers in the past records" % hand)
cf = 0
for w in range(len(W.WINTERS)):
    _, ev, _ = W.replay({s: HC[s][w] for s in S}, [x for x in S if x != "SKG"], "moorings", log=True)
    cf += sum(1 for (s, k, h, p) in ev if k == "arrive_continue")
ok("counterfactual determinacy: with NM Atlas at Skarvgrund no vessel ever finds its berth taken", cf == 0)
ok("SF9 the released vessel takes no part (section 2): placements remove the site's vessel", True)

# ---------------------------------------------------------------- the readings that close by a sentence
ok("SF1 the five sites are the plan's; SF2 downtime is section 4.2's hours; SF3 avoided is section 4.3's fleet difference;"
   " SF6 days of 24 hours; SF14 limits read as written (above / at or below)", True, "asserted by the golden recomputation")

# ---------------------------------------------------------------- graded figures mid-bin
main = [(W.SITE_NAME[s] + " avoided", G[s], 1) for s in S] + [(W.SITE_NAME[s] + " own", OWN[s], 1) for s in S] + \
       [("gap", srt[0] - srt[1], 1)]
asks = [(k, v, 0.01) for k, v in FIG["ask_statements_days"].items()] + \
       [(k, v, 1) for k, v in FIG["ask_atlas_weather_standby_hours"].items()] + \
       [(k, v, 10) for k, v in FIG["ask_port_dues_eur"].items()]
tight = min(((edge(v, u) / u, n) for n, v, u in main + asks))
ok("every graded figure at least 7 per cent of a bin from its edge", tight[0] >= 0.07, "tightest %s at %.1f%%" % (tight[1], 100 * tight[0]))

# ---------------------------------------------------------------- the ask devices move their blocks
st = list(csv.DictReader(open(os.path.join(T, "developer_standby_statements.csv"))))


def winter_of(period):
    y, m = int(period[:4]), int(period[5:])
    return y if m >= 11 else y - 1


nat = {}
for x in st:
    k = "%s|%d/%02d" % (x["developer"], winter_of(x["period"]), (winter_of(x["period"]) + 1) % 100)
    nat[k] = nat.get(k, 0) + float(x["days"])
gold1 = FIG["ask_statements_days"]
ok("ask 1 natural read (every line by its period) misses every cell by a day or more",
   all(abs(nat.get(k, 0) - v) >= 0.5 for k, v in gold1.items()), " ".join("%.2f" % (nat.get(k, 0) - v) for k, v in gold1.items()))
revised = {x["their_ref"][5:] for x in st if x["their_ref"].startswith("Rev. ")}
lat = {}
for x in st:
    if x["statement_no"] in revised:
        continue
    k = "%s|%d/%02d" % (x["developer"], winter_of(x["period"]), (winter_of(x["period"]) + 1) % 100)
    lat[k] = lat.get(k, 0) + float(x["days"])
ok("ask 1 D7: the latest-version rule (drop a revised statement whole) misses every cell",
   all(abs(lat.get(k, 0) - v) >= 0.25 for k, v in gold1.items()))
js = json.load(open(os.path.join(T, "atlas_shift_reports.json")))["shifts"]
codes = {c[0] for c in B.CODES}
cur = {}
for x in js:
    y = int(x["date"][:4]); m = int(x["date"][5:7]); wy = y if m >= 11 else y - 1
    k = "%d/%02d" % (wy, (wy + 1) % 100)
    cur[k] = cur.get(k, 0) + x["hours"].get("WX", 0) + x["hours"].get("WW", 0)
gold2 = FIG["ask_atlas_weather_standby_hours"]
ok("ask 2 D2: the current code list (WX weather, WS supply; retired WW read as weather) misses every winter by 20 h or more",
   all(abs(cur.get(k, 0) - v) >= 20 for k, v in gold2.items()), " ".join("%d" % (cur.get(k, 0) - v) for k, v in gold2.items()))
ok("ask 2 D4: the go-live gap holds weather standby only the hire statement carries", B.ATLAS[2025] and
   gold2["2025/26"] - sum(x["hours"].get("WX", 0) + x["hours"].get("WW", 0) + x["hours"].get("WS", 0)
                          for x in js if x["date"] >= "2025-11-01" and x["date"] < "2026-01-15") -
   sum(x["hours"].get("WX", 0) for x in js if x["date"] >= "2026-01-25") >= 10)
ap = list(csv.DictReader(open(os.path.join(T, "ap_port_charges_2023_2026.csv"))))
gold3 = FIG["ask_port_dues_eur"]


def port_winter(x):
    d = x["invoice_date"]; y, m = int(d[:4]), int(d[5:7])
    wy = y if m >= 10 else y - 1
    return "%s|%d/%02d" % ("Tranevig" if x["vendor"].startswith("Tranevig") else "Hjortby Havn", wy, (wy + 1) % 100)


sumall = {}
for x in ap:
    sumall[port_winter(x)] = sumall.get(port_winter(x), 0) + float(x["amount_eur"])
ok("ask 3 D6: summing the weekly Tranevig lines over-counts every Tranevig winter by 100 EUR or more",
   all(sumall.get(k, 0) - v >= 100 for k, v in gold3.items() if k.startswith("Tranevig")),
   " ".join("%.0f" % (sumall.get(k, 0) - v) for k, v in gold3.items()))
# ask 3 fairness: the Tranevig calls are recoverable from the lines through the tariff and the tonnage alone
import openpyxl
gtab = {r[0]: r[7] for r in openpyxl.load_workbook(os.path.join(T, "vessel_register_2026.xlsx")).active.iter_rows(min_row=2, values_only=True)}
rate = {r[0]: r[8] for r in openpyxl.load_workbook(os.path.join(T, "port_register_2026.xlsx"))["Ports"].iter_rows(min_row=2, values_only=True)}["Tranevig"]
tl = sorted([x for x in ap if x["vendor"].startswith("Tranevig")], key=lambda x: (x["vessel"], x["berth_from"]))
fee = lambda v, h: round(gtab[v] * rate * -(-int(h) // 24), 2)
rec = {}; cont = 0; prev_end = {}
for x in tl:
    st_ = B.dt.datetime.fromisoformat(x["berth_from"])
    if prev_end.get(x["vessel"]) == st_:
        cont += 1          # the same call carried into the next week: its charge is already counted
    else:
        rec[port_winter(x)] = rec.get(port_winter(x), 0) + float(x["amount_eur"])
    prev_end[x["vessel"]] = st_ + B.dt.timedelta(hours=int(x["berth_hours"]))
tl = sorted(tl, key=lambda x: (x["vessel"], x["berth_from"]))
ok("ask 3 D6 fairness: calls carried across a week end are found from the berth times alone", cont >= 3, "%d carried lines" % cont)
ok("ask 3 D6 fairness: that reconstruction gives the golden in every Tranevig winter",
   all(abs(rec.get(k, 0) - v) < 0.01 for k, v in gold3.items() if k.startswith("Tranevig")),
   " ".join("%.2f" % (rec.get(k, 0) - v) for k, v in gold3.items() if k.startswith("Tranevig")))
seen = set(); dd = {}; ex = set(); de = {}
for x in ap:
    if x["vendor"].startswith("Hjortby"):
        key = tuple(x[c] for c in ("vendor_no", "invoice_no", "invoice_date", "vessel", "amount_eur"))
        if key not in ex:
            ex.add(key); de[port_winter(x)] = de.get(port_winter(x), 0) + float(x["amount_eur"])
        n = x["invoice_no"].lstrip("0")
        if n in seen:
            continue
        seen.add(n)
        dd[port_winter(x)] = dd.get(port_winter(x), 0) + float(x["amount_eur"])
ok("ask 3 D1: the normalised invoice number as the key (recycled each year) under-counts Hjortby 2025/26",
   gold3["Hjortby Havn|2025/26"] - dd.get("Hjortby Havn|2025/26", 0) >= 100,
   " ".join("%.0f" % (dd.get(k, 0) - v) for k, v in gold3.items() if k.startswith("Hjortby")))
ok("ask 3 D1: no de-duplication, or exact-row de-duplication, over-counts Hjortby 2024/25 (re-keyed copies)",
   sumall.get("Hjortby Havn|2024/25", 0) - gold3["Hjortby Havn|2024/25"] >= 100 and
   de.get("Hjortby Havn|2024/25", 0) - gold3["Hjortby Havn|2024/25"] >= 100)

# ---------------------------------------------------------------- realism sweep and input gates
names = sorted(os.listdir(T))
ok("input gate: 10 or more files", len(names) >= 10, "%d files" % len(names))
ok("input gate: 3 or more formats", len({n.rsplit(".", 1)[1] for n in names}) >= 3, str(sorted({n.rsplit(".", 1)[1] for n in names})))
ok("input gate: a file of 25,000 rows or more", max(rows_old, rows_new) >= 25000)
meta = json.load(open(os.path.join(TASK, "metadata.json")))
ok("input gate: two or more distractors named in metadata.json", len(meta["distractors"]) >= 2)
sheetnames = [sn for n in names if n.endswith(".xlsx") for sn in __import__("openpyxl").load_workbook(os.path.join(T, n), read_only=True).sheetnames]
ok("no shipped file or sheet describes the data (no readme, about, dictionary, notes, manifest, schema)",
   not any(re.search(r"readme|about|dictionar|notes|manifest|schema|field_guide|codebook", n, re.I) for n in names + sheetnames),
   ", ".join(sheetnames))
blob = b"".join(open(os.path.join(T, n), "rb").read() for n in names if n.endswith((".pdf", ".xlsx")))
xml = b""
for n in names:
    if n.endswith(".xlsx"):
        z = zipfile.ZipFile(os.path.join(T, n))
        xml += z.read("docProps/app.xml") + z.read("docProps/core.xml")
ok("H1 containers scrubbed (no openpyxl, no ReportLab, fixed modified time)",
   b"penpyxl" not in xml and b"ReportLab" not in blob and b"2026-11" not in xml and b"D:2000" not in blob)
stamps = []
for n in names:
    if n.endswith(".xlsx"):
        core = zipfile.ZipFile(os.path.join(T, n)).read("docProps/core.xml").decode()
        cr = re.search(r"created[^>]*>([^<]+)<", core).group(1); md = re.search(r"modified[^>]*>([^<]+)<", core).group(1)
        stamps.append((n, cr, md))
    if n.endswith(".pdf"):
        dd = re.findall(rb"/CreationDate \(D:(\d{14})", open(os.path.join(T, n), "rb").read())
        stamps.append((n, dd[0].decode(), dd[0].decode()))
ok("H13 every document has its own creation stamp, created before modified, none after the 25 Sep 2026 export",
   len({s[1] for s in stamps}) == len(stamps) and all(s[1] <= s[2] for s in stamps) and
   all(s[2].replace("-", "").replace("T", "").replace(":", "")[:8] <= "20260925" for s in stamps),
   "; ".join("%s %s" % (s[0].split("_")[0], s[1][:10]) for s in stamps))
from pypdf import PdfReader
pdf_ok = True
for n in names:
    if n.endswith(".pdf"):
        rd = PdfReader(os.path.join(T, n), strict=True)
        pdf_ok &= len("".join(p.extract_text() for p in rd.pages)) > 200
ok("H25 every shipped PDF opens with a strict reader and yields its text", pdf_ok)
dprt = list(csv.DictReader(open(os.path.join(T, "daily_progress_reports_2023_2026.csv"))))
acts = {x["activity"].split(" MP-")[0].split(" TP-")[0] for x in dprt}
ok("realism: progress reports carry a varied activity vocabulary", len(acts) >= 10, "%d distinct activities" % len(acts))
reason = [x for x in dprt if re.search(r"occupied|taken|berth (full|busy)|no berth|divert", x["activity"], re.I)]
ok("readability: no report gives a reason for going on to Kalvholm", not reason)
plan_txt = open(os.path.join(T, "campaign_plan_2026_27.pdf"), "rb").read()
ok("readability: the plan names no shared berth, no Kalvholm and no arrival order",
   b"Kalvholm" not in plan_txt and b"share" not in plan_txt)
mon = {}
for w, y in enumerate(W.WINTERS):
    for s in S:
        mon.setdefault(y, []).append(int((HC[s][w][:W.H] > 1.8).sum()))
tiepairs = sum(len(v) - len(set(v)) for v in mon.values())
ok("realism: exceedance counts tie across sites no more often than chance", tiepairs <= 3, "%d tied pairs in 18 winters" % tiepairs)
ok("realism: no round ask totals", all(abs(v - round(v, -1)) > 1e-9 for k, v in FIG["ask_port_dues_eur"].items()))
shift_sum = all(abs(sum(x["hours"].values()) - 12) < 1e-6 and min(x["hours"].values()) >= 0 for x in js)
ok("realism: every jack-up shift report sums to its 12 hours, no negative entry", shift_sum)

fails = [r for r in RES if not r[1]]
print("%s  %d checks, %d FAIL" % ("PASS" if not fails else "FAIL", len(RES), len(fails)))
sys.exit(1 if fails else 0)
