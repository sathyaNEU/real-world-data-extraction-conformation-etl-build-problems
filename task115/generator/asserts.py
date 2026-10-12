"""task115 assertion regime. Run after build.py; reads target/ and re-simulates the world in memory.

    python3 asserts.py

Sections: the golden against the simulation, the answer, the rungs, the rival sweep, estimator variants,
bin margins, crossing margins and L1, Appendix B, the ask devices and their separation from the main call,
the claims audit, the clean-data and lens-swap tests, the input gates."""
import datetime as dt
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import build
import golden as GD
import simulate as SIM
import stores as ST
import tune
import world as W

TARGET = Path(__file__).resolve().parent.parent / "target"
FAILS = []
NAMES = {"third": "Save a third", "forty": "Save 40%", "half": "Half price", "off240": "€2.40 off"}
ORDER = ["third", "off240", "forty", "half"]          # cheapest first, by funding (asserted below)


def check(ok, what, info=""):
    print(("ok   " if ok else "FAIL ") + what + (("  " + str(info)) if info != "" else ""))
    if not ok:
        FAILS.append(what)


def rbin(x, step):
    return math.floor(x / step + 0.5)


def edge(x, step):
    return tune.edge_dist(x, step) / step


def pick(chain):
    """Cheapest menu deal whose chain multiple clears the floor, else sit out."""
    for k in ORDER:
        if chain[k] >= GD.FLOOR:
            return k
    return "sit out"


# ------------------------------------------------------------------ worlds
stores = ST.build(W.SEED)
rows, means, truth = SIM.simulate(stores, W.SEED)
df = tune.frame(rows)
appb = set(build.APPENDIX_B)
pure, share = tune.estimators(df)
G = tune.figures(df, stores, appb, pure, share)
F = GD.golden(TARGET)
GOLD = tune.cells(G)

# ------------------------------------------------------------------ 1. golden from the files = simulation path
print("\n1. golden recomputed from target/ against the in-memory path")
fmap = {"third": "Save a third", "forty": "Save 40%", "half": "Half price", "off240": "€2.40 off"}
short = {W.REGIONS[i]: r for i, r in enumerate(tune.REGS)}
diff = 0.0
for k in ORDER:
    diff = max(diff, abs(F["chain"][fmap[k]] - G["chain"][k]))
    for reg in W.REGIONS:
        diff = max(diff, abs(F["region"][reg][fmap[k]] - G["region"][short[reg]][k]))
for reg in W.REGIONS:
    diff = max(diff, abs(F["base_region"][reg] - G["base_region"][short[reg]]) / 1000,
               abs(F["packs_region"][reg] - G["packs_region"][short[reg]]) / 10000)
diff = max(diff, abs(F["base_chain"] - G["base_chain"]) / 1000, abs(F["packs_Save 40%"] - G["packs_forty"]) / 10000)
check(diff < 1e-9, "every graded figure identical on both paths", "max diff %.2e" % diff)
check(abs(F["share"] - share) < 1e-12, "switch share identical", round(share, 5))
check(len(F["stores"]) == 169, "participating scanning stores", len(F["stores"]))

# ------------------------------------------------------------------ 2. the answer
print("\n2. the answer")
chain = G["chain"]
check(pick(chain) == "forty", "cheapest clearing deal is Save 40%", {k: round(v, 4) for k, v in chain.items()})
check(rbin(chain["forty"], 0.1) == 27, "Save 40% chain multiple rounds to 2.7", round(chain["forty"], 4))
check(chain["forty"] >= GD.FLOOR * 1.06, "Save 40% clears the floor by at least 6 per cent",
      "%.1f%%" % (100 * (chain["forty"] / GD.FLOOR - 1)))
check(chain["off240"] < GD.FLOOR * 0.75 and chain["third"] < GD.FLOOR * 0.75,
      "Save a third and EUR 2.40 off at least 25 per cent short", (round(chain["third"], 4), round(chain["off240"], 4)))
fund = {}
for k in ORDER:
    fund[k] = 3 * sum((r["reg"] - r[fmap[k]][1]) * r[fmap[k]][0] for r in F["fc"].values())
check(fund["third"] < fund["off240"] < fund["forty"] < fund["half"], "funding order third < 2.40 off < 40% < half",
      {k: round(v) for k, v in fund.items()})
check(fund["half"] > 1.5 * fund["forty"], "half price funds at least half as much again as Save 40%",
      round(fund["half"] / fund["forty"], 2))
check(rbin(G["packs_forty"], 1000) == 36, "chain packs to the nearest thousand: 36,000", round(G["packs_forty"], 1))

# ------------------------------------------------------------------ 3. the rungs
print("\n3. the rungs")
rec = build.recap_rows(rows, W.EVENTS, first=dt.date(2025, 1, 1))
own = [r for r in rec if W.LINE[r["item"]]["supplier"] == "Delahunt Tea"]
check(all(r["label"] in ("Save 20%", "Save 25%") for r in own), "Delahunt's own cycles are all Save 20% or Save 25%",
      [(r["code"], r["label"]) for r in own])
pts = defaultdict(list)
for r in own:
    pts[0.20 if r["label"] == "Save 20%" else 0.25].append(r["mult"] - 1)
l20, l25 = np.mean(pts[0.20]), np.mean(pts[0.25])
cur = {}
last = df.week.max()
cdf = df[df.week == last].set_index(["store", "item"]).reg
part = list(F["stores"])
regp = {s: float(cdf[(s, W.DEL160)]) for s in part}
bases = {s: F["fc"][s]["base"] for s in part}
Bsum = sum(bases.values())


def chain_from_curve(f):
    out = {}
    for k, kind, val, label in W.MENU:
        out[k] = sum(bases[s] * (1 + f(W.depth(regp[s], kind, val))) for s in part) / Bsum
    return out


curves = {
    "linear through 20% and 25%": lambda d: l20 + (l25 - l20) / 0.05 * (d - 0.20),
    "proportional through origin": lambda d: d * (0.20 * l20 + 0.25 * l25) / (0.04 + 0.0625),
    "power through both": lambda d: l20 * (d / 0.20) ** (math.log(l25 / l20) / math.log(1.25)),
    "exponential through both": lambda d: l20 * math.exp(math.log(l25 / l20) / 0.05 * (d - 0.20)),
    "quadratic through origin": lambda d: np.polyval(np.polyfit([0, 0.20, 0.25], [0, l20, l25], 2), d),
}
r0picks = {}
for name, f in curves.items():
    c = chain_from_curve(f)
    r0picks[name] = pick(c)
    check(r0picks[name] != "forty", "R0 %s does not name Save 40%%" % name,
          "%s %s" % (r0picks[name], {k: round(v, 2) for k, v in c.items()}))
check(r0picks["linear through 20% and 25%"] == "sit out", "R0 linear extrapolation sits out")
by = defaultdict(list)
for r in rec:
    by[r["label"]].append(r["mult"])
r1 = {}
for stat, fn in (("mean", np.mean), ("median", np.median)):
    c = {"third": fn(by["Save a third"]), "forty": fn(by["Save 40%"]), "half": fn(by["Half price"]),
         "off240": 0.0}
    r1[stat] = pick(c)
    check(r1[stat] == "third", "R1 recap %s by mechanic names Save a third" % stat,
          {k: round(float(v), 3) for k, v in c.items() if k != "off240"})
c160 = {k: np.mean([r["mult"] for r in rec if r["label"] == NAMES[k] and W.LINE[r["item"]]["bags"] == 160] or [0])
        for k in ("third", "forty", "half")}
c160["off240"] = 0.0
check(pick(c160) == "third", "R1 on 160s cycles only names Save a third", {k: round(float(v), 3) for k, v in c160.items()})
lines = GD.load_lines(TARGET)
fdf = GD.load_feed(TARGET)
avg_ol = float(df[(df.week == last) & (df.item == W.OL160)].reg.mean())
for label, ref in (("RRP 3.79", 3.79), ("chain-average own-label price %.2f" % avg_ol, avg_ol)):
    fc2 = GD.forecast(fdf, lines, F["pure"], F["share"], F["stores"], test="rrp", rrp=ref)
    B2 = sum(r["base"] for r in fc2.values())
    c2 = {k: sum(r[fmap[k]][0] for r in fc2.values()) / B2 for k in ORDER}
    f2 = {k: 3 * sum((r["reg"] - r[fmap[k]][1]) * r[fmap[k]][0] for r in fc2.values()) for k in ORDER}
    check(pick(c2) == "off240" and f2["off240"] < f2["forty"],
          "R2 crossing tested at the %s names EUR 2.40 off" % label,
          "%s, funding 2.40 off %.0f < 40%% %.0f" % ({k: round(v, 3) for k, v in c2.items()}, f2["off240"],
                                                    f2["forty"]))
    check(c2["off240"] >= GD.FLOOR * 1.03, "R2 at the %s: EUR 2.40 off clears by at least 3 per cent" % label,
          round(c2["off240"], 4))

g_loss = tune.figures(df, stores, appb, *tune.estimators(df, side="loss"))
check(pick(g_loss["chain"]) == "half" and g_loss["chain"]["forty"] <= GD.FLOOR * 0.92,
      "R3 switch read off the own-label loss, credited one for one, names half price (Save 40% short)",
      {k: round(v, 4) for k, v in g_loss["chain"].items()})
# corpus direction: under one-for-one transfer every crossing cycle in the recap is under-predicted, under the
# deal-line measure each is reproduced
pl_, sl_ = tune.estimators(df, side="loss")
key_reg = df.set_index(["store", "week", "item"]).reg
under, fit = {}, {}
for code, start, item, kind, val, label in W.EVENTS:
    pair = W.OWN.get(W.LINE[item]["bags"])
    if not pair:
        continue
    weeks = [start + dt.timedelta(days=7 * k) for k in range(3)]
    pre = [start - dt.timedelta(days=7 * k) for k in range(1, 14)]
    bse = df[(df.item == item) & df.week.isin(pre) & df.dp.isna()].groupby("store").units.mean()
    obs = df[(df.item == pair) & df.week.isin(pre) & df.dp.isna()].groupby("store").units.mean()
    ev = df[(df.item == item) & df.week.isin(weeks) & (df.ref == code)]
    ev = ev[ev.store.isin(bse.index) & ev.store.isin(obs.index)]
    olp_ = key_reg.reindex(list(zip(ev.store, ev.week, [pair] * len(ev)))).values
    crs = ev.dp.values <= olp_ + 1e-9
    if not crs.any() or not crs.all():
        continue
    dep = [W.depth(r, kind, val) for r in ev.reg]
    pure_part = sum(b * (1 + tune.lift_at(pure, d)) for b, d in zip(bse.reindex(ev.store).values, dep))
    ol_part = float(obs.reindex(ev.store).values.sum())
    actual = float(ev.units.sum())
    under[code] = (pure_part + sl_ * ol_part) / actual
    fit[code] = (pure_part + share * ol_part) / actual
check(len(under) >= 4 and max(under.values()) <= 0.85 and all(abs(x - 1) < 0.03 for x in fit.values()),
      "corpus direction: one-for-one under-predicts every all-crossing cycle by 15%+, the deal-line measure fits",
      {c: (round(under[c], 3), round(fit[c], 3)) for c in under})

# ------------------------------------------------------------------ 4. rival sweep
print("\n4. rival sweep")
rivals = {}
rath = {k: np.mean([r["mult"] for r in rec if r["item"] == "214770" and r["label"] == NAMES[k]] or [0])
        for k in ("third", "forty")}
rivals["Rathmore as the closest analog"] = pick({"third": rath["third"], "forty": rath["forty"], "half": 0, "off240": 0})
dep = []
for r in rec:
    e = next(e for e in W.EVENTS if e[0] == r["code"])
    regs = [W.price(r["item"], pf, e[1]) for pf in "PCV"]
    dep.append((np.mean([W.depth(x, e[3], e[4]) for x in regs]), r["mult"]))
b1, b0 = np.polyfit([d for d, m in dep], [m for d, m in dep], 1)
creg = chain_from_curve(lambda d: b0 + b1 * d - 1)
rivals["depth regression over the recap"] = pick(creg)
lo = chain_from_curve(lambda d: tune.lift_at(F["pure"], d))
rivals["pure lift only (no switch)"] = pick(lo)
# chain-level crossing ratio regression: multiple on (mean deal price / mean own-label price) over the recap
xs, ys = [], []
for r in rec:
    e = next(e for e in W.EVENTS if e[0] == r["code"])
    pair = W.OWN.get(W.LINE[r["item"]]["bags"])
    if not pair:
        continue
    dp = np.mean([W.deal_price(W.price(r["item"], pf, e[1]), e[3], e[4]) for pf in "PCV"])
    op = np.mean([W.price(pair, pf, e[1]) for pf in "PCV"])
    xs.append(dp / op)
    ys.append(r["mult"])
c1, c0 = np.polyfit(xs, ys, 1)
olp = {s: float(cdf[(s, W.OL160)]) for s in part}
cr = {}
mean_ol = np.mean([olp[s] for s in part])
for k, kind, val, label in W.MENU:
    mdp = np.mean([W.deal_price(regp[s], kind, val) for s in part])
    cr[k] = c0 + c1 * mdp / mean_ol
rivals["chain-level regression on deal price over own-label price"] = pick(cr)
nob = tune.figures(df, stores, set(), pure, share)
rivals["store-level crossing ignoring Appendix B"] = pick(nob["chain"])
rivals["crossing tested per region (floor per region)"] = next(
    (k for k in ORDER if all(G["region"][r][k] >= GD.FLOOR for r in tune.REGS)), "sit out")
for name, p in rivals.items():
    extra = ""
    if name == "store-level crossing ignoring Appendix B":
        ok = p == "forty" and rbin(nob["chain"]["forty"], 0.1) == 27
        check(ok, "C1 converges: %s" % name, "%s %.4f" % (p, nob["chain"]["forty"]))
        continue
    check(p != "forty", "rival does not name Save 40%%: %s" % name, p)
check(rivals["crossing tested per region (floor per region)"] == "half",
      "the per-region reading of the floor names half price (the brief pins chain-wide)")

# ------------------------------------------------------------------ 5. estimator variants
print("\n5. estimator variants (required set keeps every graded cell in its bin)")
bat = tune.battery(df, stores, appb)
worst = tune.report(bat, show=False)
for v in tune.REQUIRED:
    c = tune.cells(bat[v])
    moved = [k for k, x in GOLD.items() if rbin(c[k], 1000.0 if k[1] == "packs" else 0.1) !=
             rbin(x, 1000.0 if k[1] == "packs" else 0.1)]
    check(not moved and pick(bat[v]["chain"]) == "forty", "variant %s: pick and every cell unchanged" % v,
          "share %.4f" % bat[v]["share"])
c26 = tune.cells(bat["p26"])
moved26 = [k for k, x in GOLD.items() if rbin(c26[k], 1000.0 if k[1] == "packs" else 0.1) !=
           rbin(x, 1000.0 if k[1] == "packs" else 0.1)]
check(pick(bat["p26"]["chain"]) == "forty" and all(k[1] == "half" for k in moved26),
      "26-week window (reads the previous crossing cycle's own-label weeks into the base): pick held, moves "
      "half-price cells only", moved26)

# ------------------------------------------------------------------ 6. bin margins and receipts
print("\n6. bin margins")
mins = defaultdict(lambda: 1.0)
for k, (x, off, m, _) in worst.items():
    mins[k[1]] = min(mins[k[1]], m)
check(min(mins[k] for k in ORDER) >= 0.05, "multiples: worst margin over required variants >= 0.005",
      {k: round(mins[k] * 0.1, 4) for k in ORDER})
check(mins["packs"] >= 0.10, "packs: worst margin over required variants >= 100 packs", round(mins["packs"] * 1000))
near = [k for k, (x, off, m, _) in worst.items() if k[1] in ("forty", "half", "off240") and abs(off) < 0.05]
check(not near, "no Save 40%, half or 2.40 off cell within 0.005 of its round value", near)
packs_near = [k for k, (x, off, m, _) in worst.items() if k[1] == "packs" and abs(off) < 0.04]
check(not packs_near, "no packs figure within 40 of a round thousand", packs_near)
bmin = min([edge(G["base_chain"], 1.0)] + [edge(G["base_region"][r], 1.0) for r in tune.REGS])
check(bmin >= 0.15, "bases: every whole-pack figure at least 0.15 from its rounding edge", round(bmin, 3))
check(sum(round(G["base_region"][r]) for r in tune.REGS) == round(G["base_chain"]),
      "regional bases in whole packs add to the total in whole packs",
      (sum(round(G["base_region"][r]) for r in tune.REGS), round(G["base_chain"])))
check(sum(rbin(G["packs_region"][r], 1000) for r in tune.REGS) == rbin(G["packs_forty"], 1000),
      "regional packs to the thousand add to the chain figure to the thousand")
for code, (inv, sup, dif) in F["claims"].items():     # sums of whole cents, so no float path can move them
    for nm, x in (("invoiced", inv), ("supported", sup), ("difference", dif)):
        check(edge(x, 1.0) >= 0.05, "claims %s %s at least 0.05 from its whole-euro edge" % (code, nm), x)
    check(round(inv) - round(sup) == round(dif), "claims %s: whole-euro invoiced less supported is the difference"
          % code, (round(inv), round(sup), round(dif)))

# ------------------------------------------------------------------ 7. crossing margins and L1
print("\n7. crossing margins and L1")
key = df.set_index(["store", "week", "item"]).reg
gaps = []
l1 = []
l1_160 = []
for code, start, item, kind, val, label in W.EVENTS:
    pair = W.OWN.get(W.LINE[item]["bags"])
    if not pair:
        continue
    ev = df[(df.item == item) & df.dp.notna() & (df.ref == code)]
    op = key.reindex(list(zip(ev.store, ev.week, [pair] * len(ev)))).values
    gaps.extend(list(np.abs(ev.dp.values - op)))
    if W.LINE[item]["supplier"] == "Delahunt Tea":
        l1.extend(list(ev.dp.values - op))
        if item == W.DEL160:
            l1_160.extend(list(ev.dp.values - op))
check(min(gaps) >= 0.10 - 1e-9, "no history store-week within EUR 0.10 of the own-label price", round(min(gaps), 2))
check(min(l1) >= 0.45 - 1e-9 and min(l1_160) >= 0.80 - 1e-9,
      "L1: every Delahunt deal sat above its own-label pair (80s by EUR 0.45, 160s by EUR 0.80 at least)",
      (round(min(l1), 2), round(min(l1_160), 2)))
mg = []
for s in part:
    for k, kind, val, label in W.MENU:
        mg.append(abs(W.deal_price(regp[s], kind, val) - olp[s]))
check(min(mg) >= 0.10 - 1e-9, "no March store within EUR 0.10 of the boundary for any deal", round(min(mg), 2))
crossing_ev = {}
for code, start, item, kind, val, label in W.EVENTS:
    pair = W.OWN.get(W.LINE[item]["bags"])
    if not pair:
        continue
    weeks = [start + dt.timedelta(days=7 * k) for k in range(3)]
    pre = [start - dt.timedelta(days=7 * k) for k in range(1, 14)]
    ev = df[(df.item == item) & df.dp.notna() & (df.ref == code)]
    op = key.reindex(list(zip(ev.store, ev.week, [pair] * len(ev)))).values
    cr_st = set(ev[ev.dp.values <= op + 1e-9].store)
    ob = df[(df.item == pair) & df.week.isin(pre)].groupby("store").units.mean()
    oe = df[(df.item == pair) & df.week.isin(weeks)].groupby("store").units.sum() / 3
    inside = [s for s in oe.index if s in cr_st and s in ob.index]
    outside = [s for s in oe.index if s not in cr_st and s in ob.index and s in set(ev.store)]
    if inside:
        crossing_ev[code] = (oe[inside].sum() / ob[inside].sum(),
                             oe[outside].sum() / ob[outside].sum() if outside else None)
ok = all(abs(a - (1 - W.SWITCH_LOSS)) < 0.02 and (b is None or abs(b - 1.0) < 0.03) for a, b in crossing_ev.values())
check(ok, "own label at 0.65 of normal where the deal crossed and at normal where it did not, every event",
      {c: (round(a, 3), None if b is None else round(b, 3)) for c, (a, b) in crossing_ev.items()})
pl, sl = tune.estimators(df, side="loss")
check(abs(share - 0.70) < 0.015 and abs(sl - 0.35) < 0.01 and 1.9 < share / sl < 2.1,
      "the deal line gains twice the packs own label loses (gain-side share and loss-side share)",
      (round(share, 4), round(sl, 4)))

# ------------------------------------------------------------------ 8. Appendix B
print("\n8. Appendix B")
check(all(rbin(nob["chain"][k], 0.1) == rbin(G["chain"][k], 0.1) for k in ORDER),
      "chain multiples identical to one decimal with or without Appendix B",
      {k: round(nob["chain"][k] - G["chain"][k], 4) for k in ORDER})
check(rbin(nob["packs_forty"], 1000) != rbin(G["packs_forty"], 1000) and
      all(round(nob["base_region"][r]) != round(G["base_region"][r]) for r in tune.REGS),
      "ignoring Appendix B moves the chain packs and every regional base",
      (round(nob["packs_forty"]), {r: round(nob["base_region"][r], 1) for r in tune.REGS}))


# ------------------------------------------------------------------ 9. ask devices bite, main call inert
print("\n9. ask devices: bite on the asks, inert on the main call")


def moved_cells(g2, keys=None):
    c2 = tune.cells(g2)
    out = [k for k, x in GOLD.items() if rbin(c2[k], 1000.0 if k[1] == "packs" else 0.1) !=
           rbin(x, 1000.0 if k[1] == "packs" else 0.1)]
    bases = [r for r in tune.REGS if round(g2["base_region"][r]) != round(G["base_region"][r])]
    if round(g2["base_chain"]) != round(G["base_chain"]):
        bases.append("chain")
    return out, bases


dev = {
    "D2 region vintage: January list only": tune.figures(df, stores, appb, pure, share, regmode="jan"),
    "D2 region vintage: May 2027 moves applied": tune.figures(df, stores, appb, pure, share, regmode="may27"),
    "D4 missing store-weeks read as zero": tune.figures(df, stores, appb, pure, share, zero_fill=True),
}
need = {"D2 region vintage: January list only": (6, 4), "D2 region vintage: May 2027 moves applied": (4, 2),
        "D4 missing store-weeks read as zero": (0, 3)}
for name, g2 in dev.items():
    cm, bm = moved_cells(g2)
    check(len(cm) >= need[name][0] and len(bm) >= need[name][1], "%s bites" % name,
          "%d cells, bases %s" % (len(cm), bm))
    check(pick(g2["chain"]) == "forty" and rbin(g2["chain"]["forty"], 0.1) == 27,
          "%s inert on the main call" % name)
# H1: the renumbered Phibsborough store dropped (0388 matches no January store)
g_h1 = tune.figures(df, [s for s in stores], appb | {"0388"}, pure, share)
cm, bm = moved_cells(g_h1)
check("DNE" in bm and pick(g_h1["chain"]) == "forty" and rbin(g_h1["chain"]["forty"], 0.1) == 27,
      "H1 dropping 0388 moves the Dublin base and leaves the main call", bm)
# H2: the reissued 0119 read as Ballinrobe (West & North West); read alone it moves two bases
b_sw = float(df[(df.store == "0119") & df.week.isin(W.BASE_WEEKS) & df.dp.isna() & (df.item == W.DEL160)].units.mean())
check(round(G["base_region"]["DNE"] - b_sw) != round(G["base_region"]["DNE"]) and
      round(G["base_region"]["WNW"] + b_sw) != round(G["base_region"]["WNW"]),
      "H2 reading 0119 as Ballinrobe moves the Dublin and West bases", round(b_sw, 2))
# zero-counts: the main call's row population (scan rows of participating stores) holds no device rows
main_rows = df[df.store.isin(set(part))]
check(len(main_rows[main_rows.store.isin({"0412", "0415"})]) == 0, "no manual-return store in the main rows")
check(len(main_rows[main_rows.store.isin(appb)]) == 0, "no Appendix B store in the main rows")
check(all(s in set(df.store) for s in part), "every participating store is in the feed")

# ------------------------------------------------------------------ 10. the claims audit
print("\n10. claims audit")
inv = {c: v[0] for c, v in F["claims"].items()}
sup = {c: v[1] for c, v in F["claims"].items()}
dif = {c: v[2] for c, v in F["claims"].items()}
check(round(dif["BD26-04"]) == 217 and round(dif["BD26-13"]) == 4670, "differences 217 and 4,670",
      F["claims"])
wb = load_workbook(TARGET / GD.DN_F, read_only=True)
dn = [dict(zip([c for c in next(wb.active.iter_rows(values_only=True))], r))
      for r in list(wb.active.iter_rows(values_only=True))[1:]]
re_net = sum(d["Net (EUR)"] for d in dn if d["Debit note"] == "DN-26-1022")
fl = pd.read_csv(TARGET / GD.CLAIMS_F, dtype={"store_no": str})
ret = pd.read_csv(TARGET / GD.RETURNS_F, dtype={"store_no": str, "item_no": str})
retv = {c: float(((ret.regular_price_eur - ret.deal_price_eur) * ret.deal_units)[(ret.deal_ref == c) &
                                                                                   (ret.item_no == W.DEL160)].sum())
        for c in inv}
ri = fl[fl.debit_note == "DN-26-1022"]
covered = set(zip(ri.store_no, ri.week_commencing))
orig = fl[fl.debit_note == "DN-26-0947"]
replaced = float(orig[[(s, w) in covered for s, w in zip(orig.store_no, orig.week_commencing)]].line_amount_eur.sum())
wrong = {
    "re-issue assumed credited against the original": round((inv["BD26-13"] - replaced) - sup["BD26-13"]),
    "only the original debit note counted": round((inv["BD26-13"] - re_net) - sup["BD26-13"]),
    "manual returns left out of supported": round(inv["BD26-13"] - (sup["BD26-13"] - retv["BD26-13"])),
    "gross of VAT": round(inv["BD26-13"] * 1.23 - sup["BD26-13"]),
    "Finglas left in the March support": round(inv["BD26-04"] - (sup["BD26-04"] + dif["BD26-04"])),
}
for name, x in wrong.items():
    target_dif = round(dif["BD26-04"]) if "Finglas" in name else round(dif["BD26-13"])
    check(x != target_dif, "claims wrong path differs: %s" % name, x)
check(retv["BD26-04"] > 0 and retv["BD26-13"] > 0, "manual returns carry deal funding in both cycles",
      {c: round(v, 2) for c, v in retv.items()})

# ------------------------------------------------------------------ 11. clean-data and lens-swap tests
print("\n11. clean-data and lens-swap tests")
gaps_saved = SIM.GAPS
SIM.GAPS = set()
rows_c, _, _ = SIM.simulate(stores, W.SEED)
SIM.GAPS = gaps_saved
df_c = tune.frame(rows_c)
pu_c, sh_c = tune.estimators(df_c)
g_c = tune.figures(df_c, stores, appb, pu_c, sh_c)


def naive(rws, dfx, gg):
    """R0 on a world: Delahunt's own recap cycles, linear in depth, carried to the menu on that world's bases."""
    rc = build.recap_rows(rws, W.EVENTS, first=dt.date(2025, 1, 1))
    p = defaultdict(list)
    for r in rc:
        if W.LINE[r["item"]]["supplier"] == "Delahunt Tea":
            p[0.20 if r["label"] == "Save 20%" else 0.25].append(r["mult"] - 1)
    a20, a25 = np.mean(p[0.20]), np.mean(p[0.25])
    sub = dfx[dfx.week.isin(W.BASE_WEEKS) & dfx.dp.isna() & (dfx.item == W.DEL160)]
    bb = sub.groupby("store").units.mean()
    bb = bb[[s not in appb for s in bb.index]]
    lw = dfx[dfx.week == dfx.week.max()].set_index(["store", "item"]).reg
    out = {}
    for k, kind, val, label in W.MENU:
        out[k] = sum(bb[s] * (1 + a20 + (a25 - a20) / 0.05 * (W.depth(float(lw[(s, W.DEL160)]), kind, val) - 0.20))
                     for s in bb.index) / bb.sum()
    return pick(out)


check(pick(g_c["chain"]) == pick(G["chain"]) == "forty" and rbin(g_c["chain"]["forty"], 0.1) == 27,
      "feed repaired (no missing files): answer unchanged", round(g_c["chain"]["forty"], 4))
n_c, n_s = naive(rows_c, df_c, g_c), naive(rows, df, G)
check(n_c == n_s == "sit out" and pick(G["chain"]) != n_s,
      "feed repaired: naive answer unchanged and different from the answer", (n_c, n_s))
check(pick(lo) != "forty", "lens-swap: the answer needs the own-label line, not a relabelling of Delahunt's series",
      pick(lo))

# ------------------------------------------------------------------ 12. input gates
print("\n12. input gates")
files = [p for p in TARGET.iterdir() if p.is_file()]
fmts = {p.suffix.lower() for p in files}
check(len(files) >= 10, "10 or more files", len(files))
check(len(fmts) >= 3, "3 or more formats", sorted(fmts))
check(len(fdf) >= 25000, "a file of 25,000 or more rows", len(fdf))

# ------------------------------------------------------------------ 12b. island stores read into the packs
print("\n12b. island stores (monthly returns) added to the pack totals")
import calendar
rt = pd.read_csv(TARGET / GD.RETURNS_F, dtype={"store_no": str, "item_no": str})


def weekly(store, item, months):
    u = days = 0
    for m in months:
        r = rt[(rt.store_no == store) & (rt.item_no == item) & (rt.month == m)].iloc[0]
        y, mo = map(int, m.split("-"))
        u += int(r.units) - int(r.deal_units)
        days += calendar.monthrange(y, mo)[1] - (21 if int(r.deal_units) else 0)
    return u / (days / 7)


isl = []
for months in (("2026-07", "2026-08"), ("2026-06", "2026-07", "2026-08"), ("2026-07", "2026-08", "2026-09")):
    isl.append(sum(3 * (weekly(s, W.DEL160, months) * (1 + tune.lift_at(pure, 0.40)) +
                        share * weekly(s, W.OL160, months)) for s in ("0412", "0415")))
check(all(rbin(G["packs_forty"] + x, 1000) == rbin(G["packs_forty"], 1000) and
          rbin(G["packs_region"]["WNW"] + x, 1000) == rbin(G["packs_region"]["WNW"], 1000) for x in isl),
      "C1: adding the island stores' Save 40% packs leaves the chain and West & North West packs in their bins",
      "adds %.0f to %.0f; West & North West margin %.0f" % (min(isl), max(isl),
                                                          6500 - G["packs_region"]["WNW"] - max(isl)))

# ------------------------------------------------------------------ 13. two builds byte-identical
print("\n13. rebuild")
import hashlib
import deliver


def digest():
    out = {}
    for folder in (TARGET, TARGET.parent / "golden"):
        for p in sorted(folder.iterdir()):
            out[p.name] = (hashlib.sha256(p.read_bytes()).hexdigest(), int(p.stat().st_mtime))
    return out


first = digest()
build.main()
deliver.main()
second = digest()
moved = [k for k in first if first[k] != second.get(k)]
check(not moved and set(first) == set(second), "two consecutive builds byte-identical, file times included",
      moved or len(first))

print("\n%d failures" % len(FAILS))
for f in FAILS:
    print("  FAIL", f)
sys.exit(1 if FAILS else 0)
