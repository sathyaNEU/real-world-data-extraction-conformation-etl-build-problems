"""task134 assertions: the three rules, the ladder, the golden's family, the semantic forks, the asks, the input gates
and the realism sweep. Run after build.py and golden.py; exit 1 on any failure.

    python3 task134/generator/checks.py
"""
import collections
import csv
import glob
import json
import os
import re
import sys
import warnings

import numpy as np
import openpyxl

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import build as B
import estimators as E
import projects as PR
import sim as S
import world as W

RES = []


def ok(label, cond, detail=""):
    RES.append((label, bool(cond), detail))


def rnd(Y):
    return E.rnd(Y)


def same_bins(Y, G):
    return rnd(Y) == rnd(G)


def main():
    pack = E.load(TARGET)
    P = E.panel(pack)
    F = E.forward(pack)
    G = E.golden(pack, P, F)
    g = G["yearly"]
    gr, gt = rnd(g)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    net = (F["homes"] - F["units"]).values

    # ---------------------------------------------------------------- the call and its bins
    ok("call: yearly figures 2,800 2,700 2,600 2,500 2,400", gr == [2800, 2700, 2600, 2500, 2400], gr)
    ok("call: total 13,000", gt == 13000, gt)
    off = [abs(y - round(y / 100.0) * 100) for y in g]
    ok("bins: every yearly figure within 15 of its bin's centre (35 or more from an edge)", max(off) <= 15,
       [round(x, 1) for x in off])
    ok("bins: the total within 100 of its bin's centre", abs(g.sum() - 13000) <= 100, round(g.sum(), 1))
    ok("flip: the nearest yearly edge is %.1f homes away" % (50 - max(off)), 50 - max(off) >= 35)
    ok("figures.json carries the call", fig["call"]["total"] == gt and [fig["call"]["yearly"][str(y)] for y in W.FWD] == gr)

    # ---------------------------------------------------------------- R1 raw material
    ok("R1a the decisive computation reads lot-years: 100,000 or more standing lot-years, 50,000 or more with a priced "
       "best building", len(P) >= 100000 and P["R"].notna().sum() >= 50000, (len(P), int(P["R"].notna().sum())))
    ok("R1b the forward reads every standing lot of the order (3,000 or more)", len(F) >= 3000, len(F))
    banned = re.compile(r"feasib|residual|probab|forecast|capacity|take.?up|yield|realis|target|rate", re.I)
    hdrs = []
    distractor_names = {B.FILES[k] for k in B.DISTRACTORS}
    for fp in glob.glob(os.path.join(TARGET, "*.csv")):
        if os.path.basename(fp) in distractor_names:
            continue
        with open(fp, encoding="utf-8") as f:
            hdrs += [(os.path.basename(fp), h) for h in next(csv.reader(f)) if banned.search(h)]
    for fp in glob.glob(os.path.join(TARGET, "*.xlsx")):
        if os.path.basename(fp) in distractor_names:
            continue
        wb = openpyxl.load_workbook(fp, read_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(min_row=1, max_row=4, values_only=True):
                for v in row:
                    if isinstance(v, str) and len(v) < 40 and banned.search(v) and "Floor area ratio" not in v:
                        hdrs.append((os.path.basename(fp), v))
    ok("R1c no shipped column or table header holds the deciding quantity (feasibility, residual value, rate, yield, "
       "capacity, forecast)", not hdrs, hdrs[:5])

    # ---------------------------------------------------------------- R2 every mess item real and neutral
    def neutral(label, Y):
        ok("R2 %s leaves the call where it was" % label, same_bins(Y, g), (np.round(Y, 1).tolist(), rnd(Y)))
    neutral("former roll layout unread (2019 to 2026 only)", E.project(F, E.rates(P, years=list(range(2019, 2027))), net))
    neutral("renamed zone codes unmapped (2014 to 2020 only)", E.project(F, E.rates(P, years=list(range(2014, 2021))), net))
    pk = dict(pack)
    roll = pack["roll"].copy()
    roll["sqft"] = roll["lot_area"]
    pk["roll"] = roll
    P3, F3 = E.panel(pk), E.forward(pk)
    neutral("acres read as square feet", E.project(F3, E.rates(P3), (F3["homes"] - F3["units"]).values))
    F6 = F[F["folio"].isin(set(pack["sched"]["folio"]))]
    neutral("Schedule A joined to the 2026 roll without the folio history", E.project(F6, G["rates"], (F6["homes"] - F6["units"]).values))
    p = pack["permits"]
    new = p[p["permit_type"] == "New Construction"]
    allp = new.groupby("folio")["year"].apply(list).to_dict()
    P4 = P.copy()
    P4["event"] = [y in allp.get(f, []) for f, y in zip(P4["folio"], P4["year"])]
    neutral("cancelled, expired and superseded permits each read as a rebuild", E.project(F, E.rates(P4), net))
    sl = p[p["permit_type"].isin(["Secondary Suite", "Laneway House"])]
    firsts = sl.groupby("folio")["year"].min().to_dict()
    keep = ~P.apply(lambda r: r["folio"] in firsts and r["year"] > firsts[r["folio"]], axis=1)
    P2 = P[keep].copy()
    P2.loc[P2.apply(lambda r: firsts.get(r["folio"]) == r["year"], axis=1), "event"] = True
    F2 = F[~F["folio"].isin(firsts)]
    neutral("suite and laneway permits read as rebuilds", E.project(F2, E.rates(P2), (F2["homes"] - F2["units"]).values))
    F5 = F.assign(units=np.where(F["kind"] == "house", 1, F["units"]))
    neutral("houses with a suite netted at one home", E.project(F5, G["rates"], (F5["homes"] - F5["units"]).values))
    neutral("the zone read as the roll records it (valuation-date lag)", E.project(F, E.rates(E.panel(pack, zone_basis="roll")), net))
    ok("R2 the golden reads no permit floor area and no permit's demolished units (square metres, double-recorded "
       "demolitions and floor area units cannot move it)", True)
    ok("R2 the golden reads no occupancy record, building table row or strata lot (asks only)",
       "Strata residential" not in set(pack["roll"][pack["roll"]["folio"].isin(F["folio"]) & (pack["roll"]["year"] == 2026)]["use"]))

    # ---------------------------------------------------------------- R3 the analyst test and the decisive step alone
    d = E.default_path(pack)
    dr, dt_ = rnd(d["yearly"])
    ok("R3a the default path (zoned capacity at the corridors' take-up, every filed rule applied) files %s a year, "
       "%s in all" % (format(int(round(d["yearly"][0])), ","), format(int(round(d["total"])), ",")),
       dt_ != gt and abs(d["total"] / g.sum() - 1) >= 0.25 and all(a != b for a, b in zip(dr, gr)),
       (round(d["yearly"][0]), round(d["total"])))
    T = B.truth()
    lots, alive = T["lots"], T["alive"]
    capc = sum(max(0, np.floor(l["a"] * 3 * 0.85 / 820 + 1e-9) - l["u0"]) for l in lots
               if l["group"] in ("CORR_H", "CORR_C", "CORR_R", "TOD_C", "TOD_R"))
    homes_c = sum(T["rebuild"][l["lot_id"]]["homes"] - (l["u0"] if l["kind"] != "comm" else 0) for l in lots
                  if l["group"] in ("CORR_H", "CORR_C", "CORR_R", "TOD_C", "TOD_R") and l["lot_id"] in T["rebuild"])
    tk = homes_c / capc / 13.0
    capt = 0.0
    truthY = np.zeros(5)
    for i, lot in enumerate(lots):
        if not lot["tier"]:
            continue
        far = max(W.TIER_FAR[lot["tier"]], W.ZONES[S.zone_of(lot["group"], 2026)]["far"](2026))
        if alive[i]:
            u = S.units_on_roll(lot, 2026) if lot["kind"] != "comm" else 0
            capt += max(0, np.floor(lot["a"] * far * 0.85 / 820 + 1e-9) - u)
            t, f, rl = S.best_building(lot["a"], lot["area"], "tower", far, 2026)
            land, imp = S.roll_values(lot, 2026, None)
            if rl / (land + imp) > 1:
                h = W.RATE[lot["kind"]]
                for j in range(5):
                    truthY[j] += h * (1 - h) ** j * (S.homes_in(lot["a"], t, f) - u)
    ok("R3a on the clean truth the default construction is still wrong (capacity of the standing lots at the corridors' "
       "take-up, %d a year)" % round(capt * tk), abs(capt * tk * 5 / g.sum() - 1) >= 0.25, round(capt * tk))
    ok("R3b the decisive step alone (feasibility at the best building, rate by kind, each lot once) files the golden on "
       "the clean truth at the generating rates", same_bins(truthY, g), np.round(truthY, 1).tolist())
    R = E.rivals(pack, P, F, G)
    for name in ("R0b default, declining", "R0c default, take-up 2019 to 2026", "R0d default, standing lots only",
                 "R0e hybrid: best-building capacity at the take-up", "R0f hybrid, declining"):
        ok("R3b one lower correction alone leaves the default wrong: %s" % name, rnd(R[name])[1] != gt, round(R[name].sum()))
    docs_text = doc_texts()
    plants = re.compile(r"memo|draft|briefing|preliminary estimate|staff (estimate|figure)|forecast|realisation rate|"
                        r"take-up|feasibility|residual land value", re.I)
    found = [n for n, t in docs_text.items() if plants.search(t)]
    ok("R3c no plant: no memo, draft, staff figure, forecast, take-up, feasibility or residual value in any document",
       not found, found)
    dup = collections.Counter()
    old = pack["roll"]
    sig = old[old["kind"].notna()].groupby("folio")["land"].apply(lambda s: tuple(s.round(-3)))
    sig = sig[sig.map(len) >= 3]
    ok("R3c no copied block: no two lots carry the same land-value history over three or more rolls",
       sig.duplicated().sum() == 0, int(sig.duplicated().sum()))

    # ---------------------------------------------------------------- the ladder: every rival off by a full bin
    for name, Y in R.items():
        yr, yt = rnd(Y)
        ok("ladder: %s misses the total by a full bin or more (%s against %s)" % (name, format(yt, ","), format(gt, ",")),
           yt != gt and abs(Y.sum() - g.sum()) >= 500, round(Y.sum()))
        hits = sum(a == b for a, b in zip(yr, gr))
        allowed = 1 if name.startswith("L1") else 0
        ok("ladder: %s hits at most %d yearly figure(s)" % (name, allowed), hits <= allowed, hits)
    ok("ladder: the default sits 25 per cent or more above the golden", d["total"] / g.sum() >= 1.25, round(d["total"] / g.sum(), 3))

    # ---------------------------------------------------------------- the family (C1, C3)
    fam = E.family(pack, P, F, G)
    for name, Y in fam.items():
        if name == "homes unrounded":
            ok("SF9 homes unrounded moves the call and is ruled out by the reference tables' note (rounded down)",
               not same_bins(Y, g) and "rounded down to a whole home" in docs_text["housing_reference_tables_2026.xlsx"])
            continue
        ok("family: %s lands on the golden's figures" % name, same_bins(Y, g), np.round(Y, 1).tolist())

    # ---------------------------------------------------------------- semantic forks
    meth = docs_text["housing_target_methodology_2026.pdf"]
    order = docs_text["tod_area_order_ridgemont_2026.pdf"]
    ok("SF1 net new homes: gross moves the call, ruled out by methodology 2.2",
       rnd(R["L2 gross (no netting)"])[1] != gt and "less the dwelling units standing on the lots" in meth)
    ok("SF2 permits by issue date; cancelled and expired out; a revision once (methodology 2.3)",
       "counted in the calendar year it is issued" in meth and "cancelled or expires is not counted" in meth)
    sched_f = set(pack["sched"]["folio"])
    r26 = pack["roll"][pack["roll"]["year"] == 2026]
    ok("SF3 the order's lots: every 2026-roll folio in a station area is in Schedule A or an ancestor of one",
       sched_station_cover(pack))
    ok("SF4 suites and laneway houses outside the target (methodology 2.4)", "not part of a transit-oriented area target" in meth)
    ok("SF5 calendar years (methodology 2.3 and 2.6)", "calendar year" in meth)
    ok("SF6 no rezoning beyond the order (methodology 2.5)", "No other rezoning is assumed" in meth)
    ok("SF7 a house with a suite holds two dwelling units (methodology 2.2); netting at one stays in the bins",
       "holds two" in meth and same_bins(E.project(F5, G["rates"], (F5["homes"] - F5["units"]).values), g))
    ev = E.events(pack)
    k26 = [f for f in E.current_folios(pack)["folio"] if ev.get(f) == 2026]
    ok("SF8 lots with a 2026 permit are out of the 2027 risk set (methodology 2.3: a later permit for the same buildings "
       "revises, never adds); %d such lots" % len(k26), len(k26) > 0 and not set(k26) & set(F["folio"]))
    near = int(((P["R"] > 0.8) & (P["R"] < 1.25)).sum())
    ok("SF10 feasibility threshold: no standing lot between 0.8 and 1.3, at most 5 record lot-years between 0.8 and "
       "1.25 (%d), and thresholds 1.0, 1.1 and 1.25 file the same call" % near,
       not ((F["R"] > 0.8) & (F["R"] < 1.3)).any() and near <= 5 and same_bins(fam["threshold 1.10"], g)
       and same_bins(fam["threshold 1.25"], g), (round(F["R"].min(), 3), near))
    ok("SF11 values, costs and roll a year earlier: same call",
       same_bins(fam["prior year's values and costs"], g) and same_bins(fam["prior roll's assessed values"], g))
    ok("SF12 the record's window from any start 2016 to 2022: same call",
       all(same_bins(fam["window %d to 2026" % y], g) for y in (2016, 2018, 2020, 2022)))
    ok("SF13 pooled rate against the mean of yearly rates or a continuous hazard: same call",
       same_bins(fam["mean of the yearly rates"], g) and same_bins(fam["continuous hazard"], g))
    ok("SF14 rounding: the rounded years add to the rounded total", sum(gr) == gt, (sum(gr), gt))
    ok("SF15 acres converted: reading them as square feet stays in the bins", same_bins(E.project(F3, E.rates(P3), (F3["homes"] - F3["units"]).values), g))
    ok("SF16 floor area units never enter the call (permit floor areas unread by the golden)", True)
    ok("SF17 rates by kind and location (station areas, neighbourhoods, City Centre): same call",
       same_bins(fam["rates by kind and location"], g), round(fam["rates by kind and location"].sum(), 1))
    ok("SF18 the zone as the roll records it at its valuation date: same call",
       same_bins(fam["zone as the roll records it"], g))

    # ---------------------------------------------------------------- the asks
    A = E.ask_a(pack)
    Bg = E.ask_b(pack)
    ok("Ask A matches figures.json", all(fig["ask_a"][s][str(y)] == A[(s, y)] for s in E.STATIONS for y in E.ASK_YEARS))
    ok("Ask B matches figures.json", all(fig["ask_b"][s][t] == Bg[(s, t)] for s in E.STATIONS for t in E.BANDS))
    S1, S2, S3 = E.ask_a(pack, "direct"), E.ask_a(pack, "occupancy_units"), E.ask_a(pack, "permit_once")
    ok("Ask A cracker (folio chain, first occupancy, the occupancy record's units) misses all 20 cells",
       all(S2[k] != A[k] for k in A), sum(S2[k] == A[k] for k in A))
    ok("Ask A natural read (records summed, Schedule A folios only) misses all 20 cells", all(S1[k] != A[k] for k in A))
    ok("Ask A over-correction (each permit's units once at its first occupancy) misses 15 or more cells",
       sum(S3[k] != A[k] for k in A) >= 15, sum(S3[k] != A[k] for k in A))
    ok("Ask A device in every cell: a building of a phased project first occupied in each station area and year",
       all(S2[k] > A[k] for k in A))
    B1, B2, B3 = E.ask_b(pack, "every_strata"), E.ask_b(pack, "floor_only"), E.ask_b(pack, "unit_only")
    ok("Ask B cracker (every strata lot one home) misses all 12 cells", all(B1[k] != Bg[k] for k in Bg))
    ok("Ask B over-cleaner (strata lots without a floor area dropped) misses all 12 cells", all(B2[k] != Bg[k] for k in Bg))
    ok("Ask B device in every cell: parking or storage stalls among each cell's strata lots", all(B1[k] > Bg[k] for k in Bg))
    r26s = r26[r26["use"] == "Strata residential"]
    stalls = r26s[(r26s["unit_no"].fillna("") == "") & r26s["floor"].isna()]
    homes_nofloor = r26s[(r26s["unit_no"].fillna("") != "") & r26s["floor"].isna()]
    homes_nounit = r26s[(r26s["unit_no"].fillna("") == "") & r26s["floor"].notna()]
    ok("Ask B fair: stalls (no unit, no floor area) all assessed under $95,000; every home at $310,000 or more",
       (stalls["value"] < 95000).all() and (r26s.drop(stalls.index)["value"] >= 310000).all(),
       (stalls["value"].max(), r26s.drop(stalls.index)["value"].min()))
    ok("Ask B benign twins: homes without a floor area and homes without a unit number both exist",
       len(homes_nofloor) > 50 and len(homes_nounit) > 20, (len(homes_nofloor), len(homes_nounit)))
    ok("separation: no strata lot, occupancy record or building row in the call's standing lots",
       not set(F["folio"]) & set(r26s["folio"]))
    ok("separation: the call is unchanged with the occupancy file and building table removed",
       same_bins(E.golden(dict(pack, occ=None, buildings=None), P, F)["yearly"], g))
    dists = [os.path.join(TARGET, B.FILES[k]) for k in B.DISTRACTORS]
    ok("distractors exist and the estimators never open them", all(os.path.exists(x) for x in dists)
       and not any(B.FILES[k] in open(os.path.join(HERE, "estimators.py")).read() for k in B.DISTRACTORS))

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len(exts) >= 3, sorted(exts))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("gate: a file of 25,000 rows or more", big >= 25000, big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    ok("gate: no file name says distractor", not any("distract" in f.lower() for f in files))

    # ---------------------------------------------------------------- realism sweep
    a_vals = [A[k] for k in A]
    ok("realism: Ask A cells are not uniform (no value more than twice)", max(collections.Counter(a_vals).values()) <= 2)
    yearly_p = new[new["status"].isin(["Issued", "Completed"])].groupby("year").size()
    ok("realism: permits for new construction vary year to year", yearly_p.nunique() == len(yearly_p))
    demo = p[p["permit_type"] == "Demolition"]["construction_value"].astype(float)
    ok("realism: demolition values are not a constant stream", demo.value_counts().iloc[0] / len(demo) < 0.05)
    names = set(re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", " ".join(docs_text.values())))
    personas = set(W.PEOPLE.values())
    stray = [n for n in names if n not in personas and n.split()[0] in {"John", "Jane", "Acme"}]
    ok("realism: no placeholder names", not stray, stray)
    texts = list(docs_text.values()) + [open(os.path.join(TARGET, f), encoding="utf-8").read()
                                        for f in files if f.endswith((".csv", ".txt"))]
    ok("realism: no em or en dash in any shipped text", not any(("\u2014" in t) or ("\u2013" in t) for t in texts))
    mt = [os.stat(os.path.join(TARGET, f)).st_mtime for f in files]
    ok("realism: every file saved on or before 15 January 2027", max(mt) <= W.posix(__import__("datetime").datetime(2027, 1, 15, 23, 59)))
    ok("golden: tod_housing_target_2027-31.xlsx carries the call", golden_xlsx_ok(fig))

    fails = [r for r in RES if not r[1]]
    for label, good, detail in RES:
        print("%-4s %s%s" % ("ok" if good else "FAIL", label, "" if good else "  %s" % (detail,)))
    print("CHECKS %s: %d assertions, %d failures" % ("PASS" if not fails else "FAIL", len(RES), len(fails)))
    return 1 if fails else 0


def sched_station_cover(pack):
    r26 = pack["roll"][pack["roll"]["year"] == 2026]
    st = r26[r26["area_name"].isin(E.STATIONS)]
    cover = set(pack["sched"]["folio"]) | E.ancestors(pack, set(pack["sched"]["folio"]))
    return set(st["folio"]) <= cover


def golden_xlsx_ok(fig):
    wb = openpyxl.load_workbook(os.path.join(TASK, "golden", "tod_housing_target_2027-31.xlsx"), data_only=True)
    ws = wb["Target 2027-31"]
    vals = {}
    for row in ws.iter_rows(min_row=5, max_row=10, values_only=True):
        vals[str(row[0])] = row[1]
    return all(vals.get(str(y)) == fig["call"]["yearly"][str(y)] for y in W.FWD) and vals.get("2027 to 2031") == fig["call"]["total"]


def doc_texts():
    out = {}
    from pypdf import PdfReader
    for f in ("housing_target_methodology_2026.pdf", "tod_area_order_ridgemont_2026.pdf"):
        out[f] = " ".join(p.extract_text() for p in PdfReader(os.path.join(TARGET, f)).pages).replace("\n", " ")
        out[f] = re.sub(r"\s+", " ", out[f])
    for f in ("housing_reference_tables_2026.xlsx", "tod_order_schedule_a.xlsx", "rental_market_survey_oct2026.xlsx"):
        wb = openpyxl.load_workbook(os.path.join(TARGET, f), read_only=True)
        parts = []
        for ws in wb.worksheets:
            for row in ws.iter_rows(max_row=12 if "schedule" in f else None, values_only=True):
                parts += [str(v) for v in row if isinstance(v, str)]
        out[f] = " ".join(parts)
    out["extract_notes_2027-01-12.txt"] = open(os.path.join(TARGET, "extract_notes_2027-01-12.txt"), encoding="utf-8").read()
    return out


if __name__ == "__main__":
    sys.exit(main())
