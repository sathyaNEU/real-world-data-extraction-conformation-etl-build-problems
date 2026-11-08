"""task197 architecture 2 generator checks. Run after build.py; exit 1 on any failure."""
import os, sys, json, csv, re, glob, zipfile, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import openpyxl
from pypdf import PdfReader
import sim, world, antidotes, docs, pack, askcalc as ac
import analysis as an

TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def edge(v, unit=0.1):
    return unit / 2 - abs(v - round(v / unit) * unit)


def pdf_text(path):
    return " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages)


CODE_OF = {v: k for k, v in world.PRODUCT_CODE.items()}
prod, changes, SER = pack.series(TGT, sim.DAY0)
CAND = {CODE_OF[pc]: (SER[pc], ch) for pc, ch in changes.items()}
D = F["detail"]


def windows(code):
    ck = an.mkey(CAND[code][1])
    return (list(range(an.mkey(sim.EXPORT_FROM), ck)), list(range(ck + 1, ck + 13)), list(range(ck - 12, ck)))


proc_text_raw = pdf_text(os.path.join(TGT, "packaging_review/crp_referral_procedure_issue4.pdf"))
call_text_raw = pdf_text(os.path.join(TGT, "packaging_review/call_for_referrals_2027_review.pdf"))

# ---------------------------------------------------------------- the ladder and the call
gold = {c: D[c]["effect"] for c in D}
order = sorted(gold, key=lambda c: -gold[c])
check("call: the golden names FKJ", order[0] == "FKJ", order[0])
check("call: FKJ reaches the procedure's 1.20 and no other product does",
      gold["FKJ"] >= 1.20 and all(gold[c] < 1.20 for c in gold if c != "FKJ"), str({c: round(v, 3) for c, v in gold.items()}))
check("call: the excess over no change is at least 1.5x the runner-up's, and the printed gap is 0.2 or more",
      (gold["FKJ"] - 1) / (gold[order[1]] - 1) >= 1.5 and F["gap"] >= 0.2,
      "%.2f, gap %s" % ((gold["FKJ"] - 1) / (gold[order[1]] - 1), F["gap"]))
check("call: runner-up is NIC", order[1] == "NIC", order[1])
rungs = {"per_sold": "DOZ", "raw": "NIC", "its": "NIC"}
for m, want in rungs.items():
    o = sorted(D, key=lambda c: -D[c][m])
    check("rung %s: winner %s" % (m, want), o[0] == want, "%s %.3f" % (o[0], D[o[0]][m]))
    check("rung %s: margin at least 1.15x" % m, D[o[0]][m] / D[o[1]][m] >= 1.15, "%.3f" % (D[o[0]][m] / D[o[1]][m]))
    pos = o.index("FKJ") + 1
    check("rung %s: FKJ is not first" % m, pos > 1, str(pos))
    if pos == 2:
        check("rung %s: FKJ second only behind a 1.20x winner" % m, D[o[0]][m] / D["FKJ"][m] >= 1.2,
              "%.3f" % (D[o[0]][m] / D["FKJ"][m]))
o0 = sorted(D, key=lambda c: -D[c]["per_sold"])
check("rung 0 (per pack sold): FKJ fourth or lower", o0.index("FKJ") + 1 >= 4, str(o0.index("FKJ") + 1))
seconds = sum(1 for m in ("per_sold", "raw") if sorted(D, key=lambda c: -D[c][m]).index("FKJ") == 1)
check("ladder: FKJ second on at most one rung", seconds <= 1, str(seconds))
# Gate F: the count of cheap routes reaching the call, every flow-based route a capable analyst could take
CHEAP = {}
for c, (s, ch) in CAND.items():
    pre_all, post, _ = windows(c)
    CHEAP[c] = an.cheap_routes(s, pre_all, post)
route_names = list(CHEAP["FKJ"].keys())
landing = []
for k in route_names:
    o = sorted(CHEAP, key=lambda c: -CHEAP[c][k])
    if o[0] == "FKJ" and CHEAP["FKJ"][k] >= 1.20:
        landing.append(k)
check("Gate F: none of the %d cheap flow-based routes refers FKJ (only the packs-in-use construction does)"
      % len(route_names), not landing, ", ".join(landing))
thin = [k for k in route_names if CHEAP["FKJ"][k] >= 1.20
        and max(CHEAP[c][k] for c in CHEAP if c != "FKJ") < 1.05 * CHEAP["FKJ"][k]]
check("Gate F: where a cheap route puts FKJ at 1.20 or more, another product leads it by 5 per cent or more",
      not thin, ", ".join(thin))
check("Gate F: the routes' referrals are spread over wrong products (DOZ, NIC)",
      {sorted(CHEAP, key=lambda c: -CHEAP[c][k])[0] for k in route_names} == {"DOZ", "NIC"},
      str(sorted({sorted(CHEAP, key=lambda c: -CHEAP[c][k])[0] for k in route_names})))

# ---------------------------------------------------------------- determinism: the licensed family per product
for c in D:
    fam = list(D[c]["family"].values())
    cells = {round(v + 1e-12, 1) for v in fam}
    check("family %s: every licensed member prints %.1f" % (c, round(D[c]["effect"] + 1e-12, 1)), len(cells) == 1,
          "%s" % sorted(round(v, 3) for v in fam))
    check("family %s: every member at least 0.012 from a printed edge" % c, min(edge(v) for v in fam) >= 0.012,
          "%.4f" % min(edge(v) for v in fam))
for c in D:
    want = {"fit", "drain_low", "drain_high", "quarterly"} | ({"gamma"} if D[c]["dnll_gamma"] < 2.0 else set()) \
        | ({"box"} if D[c]["dnll_box"] < 2.0 else set())
    check("family %s: every drain kernel the pre-change record does not refute (within 2 log-likelihood units) is a member"
          % c, set(D[c]["family"]) == want, "%s gamma %.1f box %.1f" % (sorted(D[c]["family"]), D[c]["dnll_gamma"], D[c]["dnll_box"]))
for c in ("FKJ", "NIC", "DOZ", "VAP", "EYE"):
    check("fixed shelf-life kernel refuted for %s (10 dNLL or more)" % c, D[c]["dnll_box"] >= 10, "%.1f" % D[c]["dnll_box"])
check("SF10 gap: the difference of the printed effects equals the unrounded difference printed",
      round(gold["FKJ"] - gold["NIC"] + 1e-12, 1) == F["gap"], "%.3f %s" % (gold["FKJ"] - gold["NIC"], F["gap"]))
for c in D:
    check("SF9 threshold %s: clear of 1.20 by 0.05 or more under every member, so the printed and the unrounded effect agree" % c,
          all(abs(v - 1.20) >= 0.05 for v in D[c]["family"].values()), "")

# ---------------------------------------------------------------- lesson 12: the construction back-tested out of sample
for c in D:
    bt = D[c]["backtest"]
    check("back-test %s: the stock construction predicts the last pre-change year at least as well as per pack sold" % c,
          bt["stock"] <= bt["per_sold"] * 1.05 + 2.0, "%.1f vs %.1f" % (bt["stock"], bt["per_sold"]))
for c in ("FKJ", "EYE", "IBC", "VAP", "CGH", "GUM", "NIC"):
    bt = D[c]["backtest"]
    check("back-test %s: per pack sold is refuted out of sample (deviance 3x or more)" % c,
          bt["per_sold"] >= 3.0 * bt["stock"], "%.1f vs %.1f" % (bt["per_sold"], bt["stock"]))
for c in ("FKJ", "NIC", "DOZ", "GUM", "EYE", "CGH"):
    bt = D[c]["backtest"]
    check("back-test %s: the time series on sales and trend is refuted out of sample (3x or more)" % c,
          bt["its"] >= 3.0 * bt["stock"], "%.1f vs %.1f" % (bt["its"], bt["stock"]))
TRUTH0 = sim.simulate(sim.TRUTH_SEED)
for c in D:
    bt = D[c]["backtest"]
    pre, _, _ = windows(c)
    test = pre[-12:]
    s, _ = CAND[c]
    y = np.array([s.expo.get(k, 0) for k in test], dtype=float)
    mu = np.array([TRUTH0[c]["lam"][sim.MKEY == k].sum() for k in test])
    floor = float(2 * np.sum(np.where(y > 0, y * np.log(y / mu), 0) - (y - mu)))
    check("back-test %s: the stock construction's held-out deviance is within 1.6x of the true expectation's own (the floor)" % c,
          bt["stock"] <= 1.6 * floor + 3.0, "%.1f vs floor %.1f" % (bt["stock"], floor))

# ---------------------------------------------------------------- lesson 7: every assumption the golden makes
for c in ("FKJ", "NIC"):
    s, ch = CAND[c]
    pre, post, _ = windows(c)
    half = len(pre) // 2
    L1, _, n1 = an.fit_drain(s, pre[:half])
    L2, _, n2 = an.fit_drain(s, pre[half:])
    lo, hi = D[c]["L_low"], D[c]["L_high"]
    check("assumption, a constant drain: %s's drain fitted on each half of its pre-change record falls in the full fit's interval" % c,
          lo * 0.8 <= L1 <= hi * 1.25 and lo * 0.8 <= L2 <= hi * 1.25, "%.1f %.1f in %.1f-%.1f" % (L1, L2, lo, hi))
# a seasonal per-pack risk: fit risk x (1 + a cos + b sin) and test it
for c in D:
    s, ch = CAND[c]
    pre, post, _ = windows(c)
    st = s.monthly_stock(D[c]["L"])
    y = np.array([s.expo.get(k, 0) for k in pre], dtype=float)
    x = np.array([st[k] for k in pre])
    m = np.array([k % 12 for k in pre])
    X = np.column_stack([np.ones(len(pre)), np.cos(2 * np.pi * m / 12), np.sin(2 * np.pi * m / 12)])
    off = np.log(x)
    beta = np.array([np.log(y.sum() / x.sum()), 0, 0])
    for _ in range(50):
        mu = np.exp(X @ beta + off)
        beta = beta + np.linalg.solve(X.T @ (mu[:, None] * X), X.T @ (y - mu))
    mu = np.exp(X @ beta + off)
    dev_s = float(2 * np.sum(np.where(y > 0, y * np.log(y / mu), 0) - (y - mu)))
    mu0 = x * y.sum() / x.sum()
    dev_0 = float(2 * np.sum(np.where(y > 0, y * np.log(y / mu0), 0) - (y - mu0)))
    check("assumption, no season in the per-pack risk: %s's seasonal term is not supported (deviance drop under 9.2, 1 per cent on 2 df)" % c,
          dev_0 - dev_s < 9.21, "%.2f" % (dev_0 - dev_s))
# no opening stock: every UPC's first period is at or after its product's first-marketed date
sales_first = {}
with open(os.path.join(TGT, pack.POS_REV), newline="") as fh:
    for r in csv.DictReader(fh):
        sales_first.setdefault(r["upc"], r["period_ending"])
ok = True
for pc, e in prod.items():
    for u in e["upcs"]:
        launch = e["launch"].date() if isinstance(e["launch"], dt.datetime) else e["launch"]
        fp = dt.date.fromisoformat(sales_first[u])
        ok = ok and (fp - launch).days <= 28 and fp >= launch
check("assumption, no opening stock: each UPC's sales begin in the period it was first marketed", ok)
# the drain unchanged by the new packaging: the call holds with FKJ's post-change drain anywhere in its interval and NIC's too
for lo_hi in ("L_low", "L_high"):
    s, ch = CAND["FKJ"]
    pre, post, _ = windows("FKJ")
    hh, _ = an.fit_hazard(s, pre, D["FKJ"]["L"])
    st_fit = s.monthly_stock(D["FKJ"]["L"])
    st_alt = s.monthly_stock(D["FKJ"][lo_hi])
    # the old packs keep the fitted drain; the changed packs drain at the interval's end: bound by the two stocks
    cf_alt = hh * sum(st_alt[k] for k in post) * sum(st_fit[k] for k in pre) / sum(st_alt[k] for k in pre)
    e_alt = D["FKJ"]["obs"] / cf_alt
    check("assumption, the drain unchanged by the changed pack: FKJ still reaches 1.20 and leads with its drain at %s" % lo_hi,
          e_alt >= 1.20 and e_alt / gold["NIC"] >= 1.15, "%.3f" % e_alt)

# ---------------------------------------------------------------- the three rules, on the clean truth
truth = sim.simulate(sim.TRUTH_SEED)
clean = {}
for c in sim.CANDIDATES:
    p = sim.BYCODE[c]
    ck = sim.month_key(p["change"])
    post = [k for k in range(ck + 1, ck + 13)]
    pre12 = list(range(ck - 12, ck))
    mask = lambda ks: np.isin(sim.MKEY, ks)
    lam = truth[c]["lam"]
    buys = truth[c]["buys"]
    clean[c] = dict(per_sold=(lam[mask(post)].sum() / buys[mask(post)].sum()) / (lam[mask(pre12)].sum() / buys[mask(pre12)].sum()),
                    golden=lam[mask(post)].sum() / truth[c]["cf_lam"][mask(post)].sum(),
                    raw=lam[mask(post)].sum() / lam[mask(pre12)].sum())
check("R3a analyst test: per pack sold on the clean truth files DOZ, a wrong answer",
      max(clean, key=lambda c: clean[c]["per_sold"]) == "DOZ", max(clean, key=lambda c: clean[c]["per_sold"]))
check("R3b decisive step alone: the clean-truth counterfactual from the packs in use files FKJ",
      max(clean, key=lambda c: clean[c]["golden"]) == "FKJ", max(clean, key=lambda c: clean[c]["golden"]))
check("R3b lower rung: raw counts on the clean truth file a wrong product",
      max(clean, key=lambda c: clean[c]["raw"]) != "FKJ", max(clean, key=lambda c: clean[c]["raw"]))
check("R1 the field's raw material ships: row-level cases and period sales, no column holding packs in use or an expectation",
      all(h not in open(os.path.join(TGT, pack.CASES)).readline() for h in ("stock", "expected", "in_use", "rate")) and
      all(h not in open(os.path.join(TGT, pack.POS_REV)).readline() for h in ("stock", "in_use", "households")))
# R2: each mess item mishandled leaves the call and every critical figure where they were
def golden_with(month_of):
    out = {}
    for c in D:
        s, ch = CAND[c]
        pre, post, _ = windows(c)
        L, h, _ = an.fit_drain(s, pre)
        out[c] = an.effect_stock(s, pre, post, L, h)[2]
    return out
# local against UTC month: shift each call into UTC by its center's offset and recount
zone_off = {"America/Chicago": 6, "America/Detroit": 5, "America/New_York": 5, "America/Indiana/Indianapolis": 5, "America/Denver": 7}
cz = {c[0]: zone_off[c[3]] for c in world.CENTERS}
moved = 0
utc_counts = {}
with open(os.path.join(TGT, pack.CASES), newline="") as fh:
    for r in csv.DictReader(fh):
        if r["reason"] != "Unintentional - general" or not r["product_code"] or int(r["patient_age_years"]) >= 6:
            continue
        t = dt.datetime.strptime(r["call_received_local"], "%Y-%m-%d %H:%M") + dt.timedelta(hours=cz[r["member_center"]])
        k = t.year * 12 + t.month - 1
        k0 = int(r["call_received_local"][:4]) * 12 + int(r["call_received_local"][5:7]) - 1
        moved += k != k0
        utc_counts.setdefault(r["product_code"], {}).setdefault(k, 0)
        utc_counts[r["product_code"]][k] += 1
utc_eff = {}
for c in D:
    s, ch = CAND[c]
    pc = world.PRODUCT_CODE[c]
    s2 = an.Series(sim.DAY0, s.ndays, [], utc_counts[pc])
    s2.buys = s.buys
    pre, post, _ = windows(c)
    L, h, _ = an.fit_drain(s2, pre)
    utc_eff[c] = an.effect_stock(s2, pre, post, L, h)[2]
check("R2 (SF4) local clock read as UTC: %d calls change month, every effect prints the same" % moved,
      all(round(utc_eff[c] + 1e-12, 1) == round(gold[c] + 1e-12, 1) for c in D), "")
# sales spread over the period's days against booked to the period's end month
end_eff = {}
for c in D:
    s, ch = CAND[c]
    per = pack.period_sales(TGT, {world.PRODUCT_CODE[c]: prod[world.PRODUCT_CODE[c]]["upcs"]})[world.PRODUCT_CODE[c]]
    per2 = [(b - dt.timedelta(days=0), b, u) for a, b, u in per]
    s2 = an.Series(sim.DAY0, s.ndays, per2, s.expo)
    pre, post, _ = windows(c)
    L, h, _ = an.fit_drain(s2, pre)
    end_eff[c] = an.effect_stock(s2, pre, post, L, h)[2]
check("R2 four-week periods booked to their last day instead of spread: every effect prints the same",
      all(round(end_eff[c] + 1e-12, 1) == round(gold[c] + 1e-12, 1) for c in D),
      str({c: round(end_eff[c], 3) for c in D}))
last_window_end = max(sim.key_to_date(windows(c)[1][-1]) for c in D)
with open(os.path.join(TGT, pack.POS_PRE), newline="") as fh:
    pre_first = min(dt.date.fromisoformat(r["period_ending"]) - dt.timedelta(days=27) for r in csv.DictReader(fh))
check("R2 (SF6) preliminary release: no window reaches a preliminary period, so the revision alone sets every effect", pre_first > last_window_end + dt.timedelta(days=31),
      "%s after %s" % (pre_first, last_window_end))
check("R2 second substances carry no product code and so never enter a count",
      all(r["product_code"] == "" for r in csv.DictReader(open(os.path.join(TGT, pack.CASES))) if r["substance_seq"] != "1"))
rows_age = [r for r in csv.DictReader(open(os.path.join(TGT, pack.CASES))) if r["patient_age_months"]]
check("R2 ages in months agree with ages in years for every child under two",
      all(int(r["patient_age_months"]) // 12 == int(r["patient_age_years"]) for r in rows_age), str(len(rows_age)))

# ---------------------------------------------------------------- fork table
def recount(filter_fn):
    out = {}
    with open(os.path.join(TGT, pack.CASES), newline="") as fh:
        for r in csv.DictReader(fh):
            if not filter_fn(r):
                continue
            d = r["call_received_local"][:10]
            out.setdefault(r["product_code"], {}).setdefault(d, 0)
            out[r["product_code"]][d] += 1
    return out


def effect_from_daily(c, daily, window_days=None):
    s, ch = CAND[c]
    pre, post, _ = windows(c)
    monthly = {}
    for d, n in daily.get(world.PRODUCT_CODE[c], {}).items():
        k = int(d[:4]) * 12 + int(d[5:7]) - 1
        monthly[k] = monthly.get(k, 0) + n
    s2 = an.Series(sim.DAY0, s.ndays, [], monthly)
    s2.buys = s.buys
    L, h, _ = an.fit_drain(s2, pre)
    if window_days is None:
        return an.effect_stock(s2, pre, post, L, h)[2]
    a = ch + dt.timedelta(days=1)
    z = ch + dt.timedelta(days=window_days)
    obs = sum(n for d, n in daily[world.PRODUCT_CODE[c]].items() if a <= dt.date.fromisoformat(d) <= z)
    stock = s2.stock(L)
    ia, iz = (a - sim.DAY0).days, (z - sim.DAY0).days
    return obs / (h * stock[ia:iz + 1].sum())


base = lambda r: r["reason"] == "Unintentional - general" and r["product_code"] != "" and int(r["patient_age_years"]) < 6
wide = lambda r: r["reason"].startswith("Unintentional") and r["product_code"] != "" and int(r["patient_age_years"]) < 6
daily_base = recount(base)
daily_wide = recount(wide)
e_wide = {c: effect_from_daily(c, daily_wide) for c in D}
check("SF1 accidental read as every unintentional reason: the call stays FKJ, and procedure 3.2 files unintentional general",
      max(e_wide, key=e_wide.get) == "FKJ" and "recorded as unintentional general" in " ".join(proc_text_raw.split()),
      str({c: round(v, 3) for c, v in e_wide.items()}))
e_days = {c: effect_from_daily(c, daily_base, 365) for c in D}
check("SF3 the window read as 365 days from the first retail sale: the call stays FKJ and every effect prints the same",
      max(e_days, key=e_days.get) == "FKJ" and all(round(e_days[c] + 1e-12, 1) == round(gold[c] + 1e-12, 1) for c in D),
      str({c: round(v, 3) for c, v in e_days.items()}))
check("SF5 notified date against first retail sale: every change inside 1 January 2024 to 30 September 2025 either way",
      all(dt.date(2024, 1, 1) <= world.NOTIFIED[c] <= dt.date(2025, 9, 30) for c in world.NOTIFIED) and
      all(dt.date(2024, 1, 1) <= sim.BYCODE[c]["change"] <= dt.date(2025, 9, 30) for c in world.NOTIFIED))
multi = {}
with open(os.path.join(TGT, pack.CASES), newline="") as fh:
    for r in csv.DictReader(fh):
        if r["product_code"]:
            multi[r["case_id"]] = multi.get(r["case_id"], 0) + 1
older = lambda r: r["reason"] == "Unintentional - general" and r["product_code"] != "" and int(r["patient_age_years"]) <= 6
daily_older = recount(older)
e_older = {c: effect_from_daily(c, daily_older) for c in D}
check("SF2 under six read as six and under: the call stays FKJ and every effect prints the same; procedure 3.2 files "
      "'under six years of age at the time of the call'",
      max(e_older, key=e_older.get) == "FKJ" and all(round(e_older[c] + 1e-12, 1) == round(gold[c] + 1e-12, 1) for c in D)
      and "under six years of age at the time of the call" in " ".join(proc_text_raw.split()),
      str({c: round(v, 3) for c, v in e_older.items()}))
e_notified = {}
for c in D:
    s_, ch_ = CAND[c]
    pre_, _, _ = windows(c)
    kn = an.mkey(world.NOTIFIED[c])
    post_n = list(range(kn + 1, kn + 13))
    pre_n = [k for k in pre_ if k < kn]
    Ln, hn, _ = an.fit_drain(s_, pre_n)
    e_notified[c] = an.effect_stock(s_, pre_n, post_n, Ln, hn)[2]
check("SF5 the twelve months read from the notified date instead: the register's column is headed 'Changed pack first "
      "sold at retail' and procedure 3.3 names that date; read the other way the call is %s"
      % max(e_notified, key=e_notified.get),
      "first sold at retail is the date the network's watched-product register records" in " ".join(proc_text_raw.split()),
      str({c: round(v, 3) for c, v in e_notified.items()}))
second = {nm: sorted(D, key=lambda c: -(D[c]["family"].get(nm, D[c]["effect"])))[1] for nm in D["FKJ"]["family"]}
check("SF8 runner-up read as the product with the next largest effect: NIC under every member of the licensed family",
      set(second.values()) == {"NIC"}, str(second))
check("SF7 no case involves two watched products, so 'counts once for each' never applies", max(multi.values()) == 1)
names = [world.META[c]["name"].split()[0] for c in world.META]
check("R3c no plant: neither governing document names a watched product, ranks anything or states a figure for one",
      not any(n.lower() in (proc_text_raw + call_text_raw).lower() for n in names))

# ---------------------------------------------------------------- asks: devices, exactness, uniqueness
bags = ac.load(TGT)
gold_ask, unexplained = ac.figures_golden(bags)
check("asks: every acetylcysteine bag is accounted for by the regimen reading", unexplained == 0, str(unexplained))
anti = antidotes.simulate(sim.SEED + 303 + 4000)
nac_t, dfo_t = antidotes.ask_truth(anti)
check("asks: the reconstruction from the shipped rows equals the clean truth in every hospital half-year",
      all(gold_ask[k]["nac"] == nac_t[k] and gold_ask[k]["dfo"] == dfo_t[k] for k in gold_ask))
rec = {(a["hospital"], a["half"]): a for a in F["antidote"]}
check("asks: figures.json carries the reconstruction",
      all(rec[k]["acetylcysteine_courses"] == gold_ask[k]["nac"] and rec[k]["deferoxamine_courses"] == gold_ask[k]["dfo"]
          and rec[k]["antidote_courses"] == gold_ask[k]["nac"] + gold_ask[k]["dfo"] for k in gold_ask))
# uniqueness: against the reconstruction's own first bags, every other bag fits exactly one course and no first bag
# fits an earlier course
starts, _ = ac.nac_resolve(bags)
start_set = set(starts)
amb = 0
for h in {b["h"] for b in bags}:
    lst = sorted([b for b in bags if b["drug"] == "NAC" and b["h"] == h], key=lambda x: x["t"])
    firsts = [b for b in lst if (h, b["t"]) in start_set]
    for b in lst:
        fits = 0
        for a in firsts:
            if a is b:
                continue
            hrs = (b["t"] - a["t"]).total_seconds() / 3600
            for load in ac.LOADING:
                w = a["dose"] / load
                if any(lo <= hrs <= hi and abs(b["dose"] / mgkg - w) <= 0.15 for mgkg, lo, hi in ac.FOLLOW[load]):
                    fits += 1
                    break
        is_first = (h, b["t"]) in start_set
        amb += (fits != 0) if is_first else (fits != 1)
check("asks: against the reconstruction's first bags, every bag has exactly one reading", amb == 0, str(amb))
chronic = [b for b in anti["bags"] if b["drug"] == "Deferoxamine" and b["course"][0] == "chronic"]
acute_bags = [b for c in anti["dfo"] for b in c["bags"]]
clash = sum(1 for a in acute_bags for b in chronic if a["hospital"] == b["hospital"] and a["dose"] == b["dose"]
            and 18 <= abs((a["time"] - b["time"]).total_seconds()) / 3600 <= 30)
check("asks: no acute deferoxamine bag has a same-dose transfusion-night bag 18 to 30 hours from it", clash == 0, str(clash))
check("asks: transfusion-night deferoxamine bags in every hospital half-year",
      all(any(b["hospital"] == h and a <= b["time"].date() <= z for b in chronic)
          for h, *_ in world.HOSPITALS for _, a, z in antidotes.ASK_HALVES))
check("asks: two-bag regimen courses exist at the hospitals that switched, three-bag elsewhere",
      any(c["regimen"] == "two-bag" for c in anti["nac"] if c["hospital"] == "H23") and
      not any(c["regimen"] == "two-bag" for c in anti["nac"] if c["hospital"] in ("H11", "H34")))
check("separation: the call reads the case export, the point-of-sale files and the register only; no ask row is in them",
      not any(f.startswith("hospitals/") for f in (pack.CASES, pack.POS_REV, pack.POS_PRE, pack.REGISTER)))

# ---------------------------------------------------------------- leak: no file describes the data, no document names the step
files = []
for root, _, fs in os.walk(TGT):
    for f in fs:
        files.append(os.path.relpath(os.path.join(root, f), TGT))
bad_names = [f for f in files if re.search(r"readme|dictionar|manifest|notes|codebook|definition|schema|field", f, re.I)]
check("leak: no file whose name says it describes the data", not bad_names, str(bad_names))
wb = openpyxl.load_workbook(os.path.join(TGT, pack.REGISTER), read_only=True)
check("leak: the register's sheets are its two tables and nothing else", wb.sheetnames == ["Watched products", "Packaging changes"],
      str(wb.sheetnames))
proc = pdf_text(os.path.join(TGT, "packaging_review/crp_referral_procedure_issue4.pdf"))
call = pdf_text(os.path.join(TGT, "packaging_review/call_for_referrals_2027_review.pdf"))
proc, call = " ".join(proc.split()), " ".join(call.split())
check("leak positive control: the procedure's text is read (its effect clause is found)",
      "the number the product's packs would have produced" in proc.replace("\n", " "), proc[:80])
check("leak positive control: the call letter's text is read", "27 November 2026" in call)
banned = ["in homes", "in the home", "household", "cupboard", "stock", "inventory", "drain", "shelf life", "per pack sold",
          "units sold", "per 100,000", "rate", "in use", "use up", "expiry", "lifetime", "depletion"]
for name, txt in (("procedure", proc), ("call letter", call)):
    hits = [w for w in banned if w in txt.lower()]
    check("leak: the %s names no stock, use, drain, rate or sales basis" % name, not hits, str(hits))
reg_text = " ".join(str(c) for sh in wb.worksheets for row in sh.iter_rows(values_only=True) for c in row if c is not None).lower()
check("leak: the register states no shelf life, usage period or rate", not any(w in reg_text for w in ("shelf", "expiry", "usage", "days of use", "rate", "per day")))
meta = json.load(open(os.path.join(TASK, "metadata.json")))
mtext = json.dumps(meta).lower()
check("leak: metadata.json names no method or mechanism",
      not any(w in mtext for w in ("stump", "stock", "drain", "in homes", "counterfactual", "cupboard", "regimen", "chelation", "transfusion")))

# ---------------------------------------------------------------- Gate G: nothing ranks the candidates
heads = {}
for f in files:
    if f.endswith(".csv"):
        heads[f] = open(os.path.join(TGT, f)).readline().strip()
check("Gate G: no shipped table carries an effect, ratio or ranking column",
      not any(re.search(r"effect|ratio|rank|score|expected", h) for h in heads.values()), str(heads))

# ---------------------------------------------------------------- realism sweep
ids = [r["case_id"] for r in csv.DictReader(open(os.path.join(TGT, pack.CASES))) if r["substance_seq"] == "1"]
LIBS = (b"openpyxl", b"python-docx", b"reportlab", b"matplotlib", b"Openpyxl")
for f in sorted(glob.glob(os.path.join(TGT, "**", "*.xlsx"), recursive=True) + glob.glob(os.path.join(TASK, "golden", "*.xlsx"))
                + glob.glob(os.path.join(TASK, "golden", "*.docx"))):
    with zipfile.ZipFile(f) as z:
        core = z.read("docProps/core.xml")
        app = z.read("docProps/app.xml")
        wbx = z.read("xl/workbook.xml") if "xl/workbook.xml" in z.namelist() else b""
    cr = re.search(rb"<dc:creator[^>]*>([^<]+)</dc:creator>", core)
    lm = re.search(rb"<cp:lastModifiedBy[^>]*>([^<]+)</cp:lastModifiedBy>", core)
    check("container %s: an owner as creator and last modifier, no writer library in its properties" % os.path.relpath(f, TASK),
          cr and lm and not any(l in core or l in app for l in LIBS), "%s / %s" % (cr and cr.group(1), lm and lm.group(1)))
    if wbx:
        check("container %s: no sheet state or default view attribute Excel never writes" % os.path.relpath(f, TASK),
              b'state="visible"' not in wbx and b"<workbookProtection/>" not in wbx and b'visibility="visible"' not in wbx)
check("realism: case IDs are unique per case", len(ids) == len(set(ids)))
steps = set()
by_month = {}
for i in ids:
    if i.startswith("MP"):
        by_month.setdefault(i[2:6], []).append(int(i[6:]))
for m, v in by_month.items():
    steps |= set(np.diff(sorted(v)).tolist())
check("realism: the new system's case numbers do not run on one constant step", len(steps) > 2, str(sorted(steps)[:6]))
monthly = {}
for r in csv.DictReader(open(os.path.join(TGT, pack.CASES))):
    if r["product_code"] == world.PRODUCT_CODE["FKJ"] and r["reason"] == "Unintentional - general" and int(r["patient_age_years"]) < 6:
        monthly[r["call_received_local"][:7]] = monthly.get(r["call_received_local"][:7], 0) + 1
check("realism: monthly counts do not repeat a block", len(set(monthly.values())) > len(monthly) * 0.5)
centers = [c[1] for c in world.CENTERS]
check("realism: member center names take more than two shapes", len({n.split()[-1] for n in centers}) > 2)

# ---------------------------------------------------------------- input gates
fmts = {f.rsplit(".", 1)[1] for f in files}
check("input gates: 10 or more files", len(files) >= 10, str(len(files)))
check("input gates: 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
check("input gates: a file of 25,000 rows or more", sum(1 for _ in open(os.path.join(TGT, pack.CASES))) - 1 >= 25000)
check("input gates: 2 or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
check("input gates: metadata.json lists every file with source, date and licence",
      sorted("target/" + f for f in files) == sorted(x["path"] for x in meta["files"]) and
      all(x.get("source") and x.get("issued_or_extracted") and x.get("licence") for x in meta["files"]))
check("distractors: the golden never reads them", all(d.startswith("target/census") or d.startswith("target/packaging_review/adverse")
                                                       for d in meta["distractor_files"]))

# ---------------------------------------------------------------- document dates
check("dates: no document states a date after the as-of", world.DOC_DATES["call"] < sim.AS_OF and world.DOC_DATES["procedure"] < sim.AS_OF)
check("dates: the call letter follows the procedure it cites", world.DOC_DATES["call"] > world.DOC_DATES["procedure"])

fails = [r for r in RESULTS if not r[1]]
for label, ok, detail in RESULTS:
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [" + detail + "]") if detail and not ok else ""))
print("%d checks, %d failed" % (len(RESULTS), len(fails)))
sys.exit(1 if fails else 0)
