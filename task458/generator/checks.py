"""The generator's assertions on the cut pack: input gates, every semantic fork (SF1 to SF23), the three-rules block on
the clean truth (dataset-generation 7.1), every assumption the golden's method makes closed by the data (lesson 7),
the back-test on the year the outlet was oversupplied (lesson 12), the two ask devices (separation, forcing, mass,
over-cleaning half) and the documents (no rate, provision, capacity or answer stated; nothing describes a file)."""
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import bundle as B
import calc as C
from pack import DISTRACTORS, FILES
from world import *

FAILS = []
PASSES = []


def ok(name, cond, detail=""):
    (PASSES if cond else FAILS).append((name, detail))
    if not cond:
        print("FAIL %s %s" % (name, detail))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(path).pages))


def run(target, gdir, x=None, meta_path=None, fig_path=None, quiet=False):
    FAILS.clear()
    PASSES.clear()
    fig = json.load(open(fig_path))
    g = C.compute(target)
    T = C.rnd

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    ok("gate.formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str({f.rsplit(".", 1)[1] for f in files}))
    meta = json.load(open(meta_path))
    big = max((m["rows"] or 0) for m in meta["files"])
    ok("gate.big_file", big >= 25000, "largest %d rows" % big)
    ok("gate.distractors", len(meta["distractors"]) >= 2 and all(FILES[k] in [d["file"] for d in meta["distractors"]]
                                                                for k in DISTRACTORS))
    ok("gate.metadata", all(m["source"] and m["as_of"] and m["licence"] for m in meta["files"]) and
       {m["file"] for m in meta["files"]} == set(files))
    ok("gate.no_data_description", not any(re.search(r"readme|dictionary|codebook|manifest|schema|notes", f, re.I) for f in files))

    # ------------------------------------------------------------ the golden reproduces figures.json
    ok("golden.provision", T(g["provision"], 1000000) / 1e6 == fig["provision_gbp_m"])
    ok("golden.call", g["waiver"] and fig["call"] == "seek a waiver")
    # ------------------------------------------------------------ the semantic forks
    def call_of(**kw):
        return C.compute(target, **kw)["waiver"]

    vh = g["vh_stock"]
    # SF1 Valuehall's year-end stock is the close of the stock system's week cut at 31 December
    w = B.vh_weeks(target)
    last = w[w["week"] == w["week"].max()]
    ok("SF1", (last["week"].iloc[0].isoformat() == "2026-12-28") and int(last["trading_days"].max()) == 4 and
       g["pool"] - vh * (1 - g["r_job"]) > 0 and (g["provision"] - vh * (1 - g["r_job"])) > g["bb"] * 0 and
       (BB_ADVANCE * (g["gross"] - vh - (g["provision"] - vh * (1 - g["r_out"]))) < g["drawn"]),
       "the week of 28 December is cut at the year end; dropping Valuehall's stock entirely leaves the call")
    # SF2 net shipments: despatches less returns; gross despatches (returns ignored) gives the same call
    o = B.orders(target)
    ex = C.excess_lines(target)
    gross_desp = o[(o.year == 2026) & (o.kind == "customer") & (o.qty > 0)].groupby(["sub", "key"])["qty"].sum().to_dict()
    alt = sum(min(q, max(0, q - gross_desp.get((s, k), 0))) * u for s, k, q, u in
              zip(ex["sub"], ex["key"], ex["qty"], ex["unit_gbp"]))
    pool_alt = alt + vh
    prov_alt = pool_alt - (min(pool_alt, g["cap"]) * g["r_out"] + max(0, pool_alt - g["cap"]) * g["r_job"])
    ok("SF2", BB_ADVANCE * (g["gross"] - prov_alt) < g["drawn"], "returns ignored: provision %.0f, still short" % prov_alt)
    # SF3 a line whose 2026 net shipments are negative: excess is the stock held, never more
    neg = ex[ex["net26"] < 0]
    ok("SF3", bool((ex["excess_qty"] <= ex["qty"]).all()), "%d lines with negative net shipments" % len(neg))
    # SF4 AHI's register and 2026 lines in cases carry their pack quantity on the line
    ahi = pd.read_excel(os.path.join(target, FILES["ahi_stock"]), header=4)
    ok("SF4", set(ahi["Unit of Measure Code"]) == {"EA", "CS"} and
       bool((ahi[ahi["Unit of Measure Code"] == "EA"]["Qty. per Unit of Measure"] == 1).all()))
    # SF5 euro stock at the year-end rate; at the 2026 average the call holds
    s = B.stock(target)
    eur = s[s["sub"] != "AHL"]["value_ccy"].sum()
    d_g = eur * (FX_AVG_2026 - FX_CLOSE)
    ok("SF5", BB_ADVANCE * (g["gross"] + d_g - g["provision"] - d_g * 0.3) < g["drawn"], "average-rate shift %.0f" % d_g)
    # SF6 cost is each company's own landed cost: the register values tie to quantity times unit cost
    ok("SF6", abs(s["value_ccy"].sum() - sum(ex["qty"] * ex["unit_gbp"] / ex["fx"])) < 50)
    # SF7 proceeds ex VAT: the outlet's ex VAT column; VAT-inclusive proceeds are ruled out by FIN-07 2.4
    pol = pdf_text(os.path.join(target, FILES["policy"]))
    ok("SF7", "excluding VAT" in pol)
    # SF8 the group's own selling costs are not deducted
    ok("SF8", "are period costs and are not deducted" in pol)
    # SF9 the window: disposal in the year after the balance sheet date
    ok("SF9", "in the year after the balance sheet date" in pol)
    # SF10 Valuehall's own stock with the excess; valued apart at the outlet's rate, the call holds
    p10 = (g["pool"] - vh) - (min(g["pool"] - vh, g["cap"]) * g["r_out"] + max(0, g["pool"] - vh - g["cap"]) * g["r_job"]) \
        + vh * (1 - g["r_out"])
    ok("SF10", BB_ADVANCE * (g["gross"] - p10) < g["drawn"], "Valuehall valued apart: provision %.0f" % p10)
    # SF11 2027 store days from the store plan; at 365 days a store the call holds
    cap11 = g["per_day"] * 365 * 5
    p11 = g["pool"] - (cap11 * g["r_out"] + (g["pool"] - cap11) * g["r_job"])
    plan = pdf_text(os.path.join(target, FILES["vhplan"]))
    ok("SF11", "1801" in plan.replace(",", "") and BB_ADVANCE * (g["gross"] - p11) < g["drawn"], "365 days: %.0f" % p11)
    # SF12 trade recovery: 2026 lots only, or the subsidiaries' lots only: same call
    for yrs in ((2026,), (2025, 2026), (2024, 2025, 2026)):
        ok("SF12.%s" % "-".join(map(str, yrs)), call_of(job_years=yrs))
    # SF13 Valuehall recovery: 2026 only: same call
    ok("SF13", call_of(rec_years=(2026,)) and call_of(rec_years=(2025, 2026)))
    # SF14 the borrowing base counts Valuehall's stock (inventories of the Group); without it the call holds
    fac = pdf_text(os.path.join(target, FILES["facility"]))
    ok("SF14", "62.5 per cent" in fac and "inventories of the Group" in fac and
       BB_ADVANCE * (g["carried"] - vh * g["r_out"]) < g["drawn"])
    # SF15 the drawn balance at close of business on the test date
    r = pd.read_csv(os.path.join(target, FILES["rcf"]))
    ok("SF15", int(r.iloc[-1]["drawn_balance_gbp"]) == g["drawn"] and r.iloc[-1]["value_date"] == "2026-12-31" and
       abs(r["drawn_balance_gbp"].mean() - g["drawn"]) > 0)
    # SF16 exceed: a shortfall, not a tie
    ok("SF16", g["drawn"] - g["bb"] > 300000)
    # SF17 and SF18: every defensible member of the open method files the same four covenant figures, each at the unit
    # the prompt grades it in, with room to spare (the pass-2 probes at 1,390 and 1,400 a day included)
    fam = C.family(target)
    gold = {"provision": g["provision"], "inventories": g["carried"], "bb": g["bb"], "shortfall": -g["headroom"]}
    for j, key in enumerate(("provision", "inventories", "bb", "shortfall")):
        u = C.FAMILY_UNITS[key]
        vals = [r[j] for r in fam]
        bins = {T(v, u) for v in vals}
        centre = T(gold[key], u)
        room = min(min(vals) - (centre - u / 2), (centre + u / 2) - max(vals))
        ok("SF17.%s" % key if key == "provision" else "SF18.%s" % key, len(bins) == 1 and room >= 0.15 * u,
           "%d members %.3fm to %.3fm, one %s bin, %.3fm clear of its edges" % (
               len(vals), min(vals) / 1e6, max(vals) / 1e6, "{:,}".format(u), room / 1e6))
    ok("SF17", all(r[3] > 0 for r in fam), "every member files the waiver")
    ok("SF18", T(gold["shortfall"], 250000) / 1e6 == fig["shortfall_gbp_m"] and
       T(gold["bb"], 500000) / 1e6 == fig["borrowing_base_gbp_m"] and
       T(gold["inventories"], 500000) / 1e6 == fig["inventories_after_provision_gbp_m"])
    # SF19 net realisable value on the stock held at the balance sheet date (later surplus would only raise it)
    ok("SF19", "assessed on the stock held at the balance sheet date" in pol)
    # SF20 superseded group codes in AHB's table resolve to the current code in the same division
    xr = pd.read_csv(os.path.join(target, FILES["ahb_xref"]), sep=";", dtype=str)
    m = B.master(target)
    sup = m[m["Status"] == "Superseded"]
    old_in_xref = set(xr["Groepscode"]) & set(sup["Item Code"])
    div = B.division(target)
    ok("SF20", len(old_in_xref) > 0 and all(div[o_] == div[B.current_code(target)[o_]] for o_ in old_in_xref))
    # SF21 an item's division: the master (one division per code)
    ok("SF21", m["Item Code"].is_unique and set(m["Division"]) == set(DIVISIONS))
    # SF22 2025 units: eaches, customers only (transfers and cancelled lines out), returns netted
    u_t, v_t = C.shipped_2025(target)
    oo = B.orders(target)
    tr25 = oo[(oo.year == 2025) & (oo.kind == "transfer")]
    ok("SF22", len(tr25) > 0 and all(abs(T(u_t[d], 1000) - fig["units_2025_by_division"][d]) == 0 for d in DIVISIONS))
    # SF23 2025 invoiced value: euro at the 2025 average (the rate table's own note)
    fxw = pd.read_excel(os.path.join(target, FILES["fx"]), header=None)
    note = " ".join(str(v) for v in fxw[0].tolist())
    ok("SF23", "Income statement items are translated at the year's average rate" in note and
       all(T(v_t[d], 1000) == fig["sales_2025_gbp_by_division"][d] for d in DIVISIONS))

    # SF24 Lumio's twelve months to the year end hold ten months since its March launch: annualised, the call holds
    lum = set(B.master(target)[B.master(target)["Description"].str.startswith("Lumio")]["Item Code"])
    exl = ex.copy()
    exl["n2"] = [n * (12.0 / 10.0) if c in lum else n for n, c in zip(exl["net26"], exl["code"])]
    alt24 = sum(min(q, max(0, q - max(0, n))) * u for q, n, u in zip(exl["qty"], exl["n2"], exl["unit_gbp"]))
    pool24 = alt24 + vh
    prov24 = pool24 - (min(pool24, g["cap"]) * g["r_out"] + max(0, pool24 - g["cap"]) * g["r_job"])
    ok("SF24", BB_ADVANCE * (g["gross"] - prov24) < g["drawn"] and g["excess"] - alt24 < 300000,
       "Lumio annualised: excess %.0f lower, provision %.0f" % (g["excess"] - alt24, prov24))

    # SF25 the whole surplus is disposed of in 2027: none of it is carried as the stores' working stock into 2028
    work = 3 * 7 * g["per_day"] * len(B.PLAN_DAYS_2027)
    prov25 = g["provision"] - work * (g["r_out"] - g["r_job"])
    ok("SF25", "from its disposal in the year after the balance sheet date" in pol and
       BB_ADVANCE * (g["gross"] - prov25) < g["drawn"],
       "a working stock of %.0f carried into 2028 at Valuehall's rate is ruled out by FIN-07 2.4; call unchanged (%.0f)"
       % (work, prov25))

    # ------------------------------------------------------------ three rules on the clean truth (7.1)
    rung = {k: C.compute(target, capacity=k) for k in ("none", "blended", "fit", "sales2026", "jobber")}
    ok("rules.analyst_test", not rung["none"]["waiver"], "textbook route provision %.0f headroom %.0f" %
       (rung["none"]["provision"], rung["none"]["headroom"]))
    ok("rules.ladder_wrong", not rung["blended"]["waiver"] and not rung["fit"]["waiver"])
    margin_lo = min(g["drawn"] - g["bb"], min(rung[k]["headroom"] for k in ("none", "blended", "fit")))
    ok("rules.margin", margin_lo > 400000, "smallest margin %.0f" % margin_lo)
    ok("rules.cheap_routes", sum(1 for k in ("none", "blended", "fit") if rung[k]["waiver"]) == 0,
       "no route that leaves the outlet unlimited lands the call")

    # ------------------------------------------------------------ lesson 7: the method's assumptions, closed by the data
    wk = C.outlet_weeks(target)
    st = wk[(wk.trading_days == 7) & (wk.available >= C.STOCKED)].copy()
    st["pd"] = st.sales_at_cost / 7
    jan = st[st.promotion == "January sale"]["pd"].mean()
    rest = st[st.promotion != "January sale"]["pd"].mean()
    ok("L7.discount", abs(jan / rest - 1) < 0.015, "January sale %.1f against %.1f a day" % (jan, rest))
    rec_jan = wk[wk.promotion == "January sale"].sales_ex_vat.sum() / wk[wk.promotion == "January sale"].sales_at_cost.sum()
    ok("L7.discount_recovery", rec_jan < g["r_out"] - 0.05, "the January sale recovers %.3f" % rec_jan)
    b1 = np.polyfit(st.available.values, st.pd.values, 1)[0]
    ok("L7.flat_in_stock", abs(b1 * 50000) < 0.01 * rest, "slope %.6f a pound held" % b1)
    thin = wk[(wk.trading_days == 7) & (wk.available < 20000)]
    ok("L7.thin_weeks", len(thin) > 20 and (thin.sales_at_cost / 7).mean() < 0.9 * rest, "%d thin weeks" % len(thin))
    per_store = st.groupby("store")["pd"].mean()
    ok("L7.per_store", (per_store.max() / per_store.min() - 1) < 0.02, str(per_store.round(1).to_dict()))
    per_year = st.groupby(st.week.map(lambda d: d.year))["pd"].mean()
    ok("L7.no_trend", (per_year.max() / per_year.min() - 1) < 0.02, str(per_year.round(1).to_dict()))
    ok("L7.five_stores", "Valuehall will trade from its five existing stores throughout 2027" in plan and
       "deferred" in plan)
    l = B.lots(target)
    l = l.assign(r=l["Price ex VAT (GBP)"] / l["Stock at cost (GBP)"])
    bigl, smalll = l[l["Stock at cost (GBP)"] > 150000], l[l["Stock at cost (GBP)"] <= 150000]
    rb = bigl["Price ex VAT (GBP)"].sum() / bigl["Stock at cost (GBP)"].sum()
    rs = smalll["Price ex VAT (GBP)"].sum() / smalll["Stock at cost (GBP)"].sum()
    slope = np.polyfit(l["Stock at cost (GBP)"].values, l["r"].values, 1)[0]
    ok("L7.trade_not_capped", abs(rb / rs - 1) < 0.05 and abs(slope * 300000) < 0.003 and len(bigl) >= 4,
       "lots over 150,000 recover %.4f, the rest %.4f; slope %.2e a pound of lot" % (rb, rs, slope))
    ok("L7.no_other_source", abs(wk.goods_in_at_cost.sum() - wk.sales_at_cost.sum() - wk.to_trade_buyers_at_cost.sum()
                                 - wk.groupby("store").closing_stock_at_cost.last().sum()) / wk.goods_in_at_cost.sum() < 0.01)

    # ------------------------------------------------------------ lesson 12: the back-test on the oversupplied year
    y23 = wk[wk.week.map(lambda d: d.year) == 2023]
    pred = g["per_day"] * y23.trading_days.sum()
    ok("L12.cap_model", abs(pred / y23.sales_at_cost.sum() - 1) < 0.03, "predicted %.0f sold %.0f" % (pred, y23.sales_at_cost.sum()))
    ok("L12.proportional_refuted", y23.goods_in_at_cost.sum() / y23.sales_at_cost.sum() > 1.5)
    gi = wk.groupby(wk.week.map(lambda d: d.year)).agg(i=("goods_in_at_cost", "sum"), s=("sales_at_cost", "sum"),
                                                      d=("trading_days", "sum"))
    ok("L12.capacity_not_with_stock", (gi.loc[2023, "i"] > gi.loc[2024, "i"]) and (gi.loc[2023, "s"] < gi.loc[2024, "s"]),
       "2023 sent more and sold less than 2024")
    ok("L12.sales_follow_days", float(np.corrcoef(gi["s"], gi["d"])[0, 1]) > 0.99)

    # ------------------------------------------------------------ the ask devices
    arch = pd.read_csv(os.path.join(target, FILES["ahi_arch25"]), dtype={"Stock Code": str})
    arch["date"] = pd.to_datetime(arch["Doc Date"], format="%d/%m/%Y").dt.date
    ok("dev.separation.arch_2025_only", all(d.year == 2025 for d in arch["date"]))
    ok("dev.separation.uom_label", set(arch["UOM"]) == {"EA"})
    cq = B.case_qty(target)
    arch["case"] = arch["Stock Code"].map(cq)
    arch["unit"] = arch["Line Value"] / arch["Qty"]
    cust = arch[~arch["Cust Name"].isin(B.GROUP_COS) & (arch["case"] > 1)]
    pre, post = cust[cust.date < AHI_UOM_SWITCH], cust[cust.date >= AHI_UOM_SWITCH]
    pu = post.groupby(["Stock Code", "Cust Name"])["unit"].median()
    jj = pre.join(pu.rename("post_unit"), on=["Stock Code", "Cust Name"]).dropna()
    ratio = (jj["unit"] / jj["post_unit"] / jj["case"])
    ok("dev.forcing.cases", len(jj) > 500 and float((abs(ratio - 1) < 0.01).mean()) > 0.99,
       "%d pre-switch lines priced at case times each price" % len(jj))
    ok("dev.forcing.whole_cases", bool(((post["Qty"] % post["case"]) == 0).all()))
    ahl = pd.read_csv(os.path.join(target, FILES["ahl_orders"]), dtype={"Item Code": str})
    ahl["date"] = pd.to_datetime(ahl["Despatch Date"], format="%d/%m/%Y").dt.date
    ahl["Order No"] = ahl["Order No"].astype(str)
    pc = ahl[ahl["Doc Type"] == "PRICE"]
    desp = ahl[ahl["Doc Type"] == "DESP"]
    first_day = desp.groupby("Order No")["date"].min()
    ok("dev.separation.price", len(pc) > 300 and all(d.year == 2025 for d in pc["date"]) and bool((pc["Qty"] == 0).all())
       and all(first_day.get(o) is not None and first_day[o] < d for o, d in zip(pc["Order No"], pc["date"])),
       "%d price credits, every one dated in 2025 with no quantity, each under an earlier order of its customer" % len(pc))
    mcodes = set(B.master(target)["Item Code"])
    ok("dev.impossible.no_division", set(pc["Item Code"]) == {"NS001"} and "NS001" not in mcodes,
       "every price credit sits on the non-stock code NS001, which no division carries")
    q1 = desp[desp["date"] < dt.date(2025, 4, 1)].copy()
    q1["unit"] = (q1["Line Value"] / q1["Qty"]).round(2)
    base = q1.groupby(["Customer", "Item Code"])["unit"].min().to_dict()
    q2 = desp[desp["date"] >= dt.date(2025, 4, 1)]
    over = {}
    for l in q2.itertuples(index=False):
        b = base.get((l.Customer, l[6]))
        if b is not None and l.Qty > 0 and round(l[9] - l.Qty * b, 2) > 0.004:
            over.setdefault((l[0], l.Customer), []).append(round(l[9] - l.Qty * b, 2))
    one = 0
    for c in pc.itertuples(index=False):
        if sum(1 for ov in over.get((c[0], c.Customer), []) if abs(ov + c[9]) < 0.006) == 1:
            one += 1
    credited = pc.groupby(["Order No", "Customer"]).size().to_dict()
    lines_over = sum(len(over.get(k, [])) for k in credited)
    ok("dev.forcing.price_identity", one == len(pc) == lines_over,
       "each of %d credits equals, to the penny, the overcharge on exactly one line of its order (the line's quantity "
       "times its excess over the customer's price before 1 April), and the %d orders carry %d such lines" % (
           one, len(credited), lines_over))
    u_l, v_l = C.shipped_2025(target, ahi_cases="label")
    u_a, v_a = C.shipped_2025(target, ahi_cases="all")
    rout = {m: C.shipped_2025(target, price_credits=m) for m in ("spread", "customer", "dropped")}
    for d in DIVISIONS:
        ok("dev.mass.cases.%s" % d, abs(u_l[d] - u_t[d]) >= 5000, "%d units" % (u_l[d] - u_t[d]))
        ok("dev.mass.overclean.%s" % d, abs(u_a[d] - u_t[d]) >= 5000, "%d units" % (u_a[d] - u_t[d]))
        ok("dev.mass.price.%s" % d, abs(rout["spread"][1][d] - v_t[d]) >= 5000,
           "spread over the order %.0f" % (rout["spread"][1][d] - v_t[d]))
        ok("dev.overclean.price.%s" % d, min(abs(rout[m][1][d] - v_t[d]) for m in ("customer", "dropped")) >= 5000,
           "customer mix %.0f, left out %.0f" % (rout["customer"][1][d] - v_t[d], rout["dropped"][1][d] - v_t[d]))
        ok("dev.disjoint.%s" % d, v_l[d] == v_t[d] and all(rout[m][0][d] == u_t[d] for m in rout))
    ok("dev.main_population_clean", g["provision"] == C.compute(target)["provision"] and
       len(arch[arch.date.map(lambda d: d.year) == 2026]) == 0)

    # ------------------------------------------------------------ documents
    texts = {k: pdf_text(os.path.join(target, FILES[k])) for k in ("policy", "facility", "vhplan")}
    banned = re.compile(r"capacity|throughput|store.?week|saturat|recover|per cent of cost|in the pound|budget|forecast|"
                        r"waiver is|waiver will|provision of|provision is|ceiling", re.I)
    for k, t in texts.items():
        hit = banned.findall(t)
        ok("doc.neutral.%s" % k, not hit, str(hit))
    ok("doc.no_rate_in_policy", not re.search(r"\d+(\.\d+)? per cent", texts["policy"]))
    ok("doc.no_file_described", not any(re.search(re.escape(f.rsplit(".", 1)[0]), " ".join(texts.values())) for f in files))

    # ------------------------------------------------------------ goldens
    gfiles = sorted(os.listdir(gdir))
    ok("golden.files", len(gfiles) == 2 and any(f.endswith(".xlsx") for f in gfiles) and any(f.endswith(".pdf") for f in gfiles))

    print("checks: %d passed, %d failed" % (len(PASSES), len(FAILS)))
    return not FAILS


if __name__ == "__main__":
    import sys
    HERE = os.path.dirname(os.path.abspath(__file__))
    TASK = os.path.dirname(HERE)
    good = run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"),
               fig_path=os.path.join(HERE, "figures.json"))
    sys.exit(0 if good else 1)
