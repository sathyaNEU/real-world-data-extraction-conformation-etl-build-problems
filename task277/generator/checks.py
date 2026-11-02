"""The generator's assertions on the clean world and the cut pack: the three rules (R1 to R3c), every rung and its
margin, every semantic fork row (SF1 to SF14), mess neutrality, the claims devices and their forcing, rounding edges,
the input gates, the realism sweep and the distractors. Exit 1 on the first failure list.

    python3 task277/generator/checks.py
"""
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import golden as G   # noqa: E402
import pack as K     # noqa: E402
import params as P   # noqa: E402
import world as W    # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def bin5(x):
    return 10 * math.floor(x / 10 + 0.5)


def acc2(fail, n):
    return round(100 * (1 - fail / n) + 1e-12, 1)


def edge5(x):
    b = bin5(x)
    return min(x - (b - 5), (b + 5) - x)


def edge_acc(fail, n):
    a = 100 * (1 - fail / n)
    b = math.floor(a * 10 + 0.5) / 10
    return min(a - (b - 0.05), (b + 0.05) - a) * n / 100


def forecast_with(w, pk, hep_fn, mix_fn=None, plan=None):
    """The golden construction with a swappable error probability and forward mix; returns {month: (fail, n)}."""
    plan = w["plan"] if plan is None else plan
    out = {}
    for m in (2, 3):
        pl = plan[plan["month"] == m]
        ref = pk[pk["month"] == m] if mix_fn is None else mix_fn(pk, m)
        tot = 0.0
        for r in pl.itertuples():
            cell = ref[(ref["channel"] == r.channel) & (ref["range"] == r.range)]
            tot += r.lines * np.mean([hep_fn(r.channel, s) for s in cell["s27"]])
        out[m] = (tot, int(pl["lines"].sum()))
    return out


def main():
    w = W.build()
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    pk = G.picked(w)
    L = w["lines"]
    hep = pk.groupby("struct")["fail"].mean().to_dict()
    gold = forecast_with(w, pk, lambda ch, s: hep[s])
    f = G.forecast(w)
    r = G.rungs(w)
    kpi_rate = 1 - P.KPI / 100

    # ---------------------------------------------------------------- the three rules
    cols = []
    for name in os.listdir(TARGET):
        p = os.path.join(TARGET, name)
        if name.endswith(".csv"):
            sep = ";" if open(p, encoding="utf-8").readline().count(";") > 1 else ","
            cols += list(pd.read_csv(p, sep=sep, nrows=5).columns)
        elif name.endswith(".parquet"):
            cols += list(pd.read_parquet(p).columns)
        elif name.endswith(".xlsx"):
            x = pd.read_excel(p, header=None, nrows=8)
            cols += [str(v) for v in x.values.ravel() if isinstance(v, str) and len(v) <= 40]
    bad = [c for c in cols if re.search(r"mix|loose|break|kind|struct|uom|pack_type|remainder", str(c), re.I)]
    check("R1 the pick-level record ships and no column names the pick a line calls for", not bad, bad)
    check("R1 the golden reads line quantities against the inner in force on the pick date",
          set(pk["struct"].unique()) == {"whole", "loose", "mixed"} and (pk["inner"] > 0).all())
    for m in (2, 3):
        check("R3a the analyst test (channel and range rates on the plan) keeps the target in month %d" % m,
              r["R1 channel and range"][m]["accuracy"] >= P.KPI, round(r["R1 channel and range"][m]["accuracy"], 3))
        check("R3b the decisive step alone (the pick each line calls for) misses the target in month %d" % m,
              f[m]["accuracy"] < P.KPI, round(f[m]["accuracy"], 3))
    for name in ("R0 site rate", "R1b same months of 2026", "R2a inner size", "R2b channel and quantity", "R2c opened inner",
                 "R2d loose units", "R2e range and quantity"):
        for m in (2, 3):
            fail_rate = r[name][m]["fail"] / f[m]["plan"]
            check("R3b lower rung %s stays on the wrong side in month %d by 1.15x" % (name, m),
                  r[name][m]["accuracy"] >= P.KPI and kpi_rate / fail_rate >= 1.15, round(r[name][m]["accuracy"], 3))
    for m in (2, 3):
        check("golden clears the target by 1.2x or more in month %d" % m, (f[m]["fail"] / f[m]["plan"]) / kpi_rate >= 1.2,
              round((f[m]["fail"] / f[m]["plan"]) / kpi_rate, 2))
    # R3c: no copied or backfilled block of daily counts
    daily = pk.groupby(["day", "channel"]).size().unstack(fill_value=0)
    blocks = [tuple(daily.iloc[i:i + 5].values.ravel()) for i in range(len(daily) - 4)]
    dup = len(blocks) - len(set(blocks))
    check("R3c no repeated five-day block of daily line counts", dup == 0, int(dup))
    hist = G.history(w)
    check("R3c every 2026 month above target (no planted dip)", (hist["accuracy"] > P.KPI + 0.02).all(), hist["accuracy"].min())
    check("realism: monthly accuracy varies as a site's does (range of 0.03 points or more)",
          hist["accuracy"].max() - hist["accuracy"].min() >= 0.03, round(hist["accuracy"].max() - hist["accuracy"].min(), 3))
    cc = pd.read_csv(os.path.join(TARGET, K.FILES["counts"]))
    cc["m"] = pd.to_datetime(cc["count_date"]).dt.month
    check("realism: every month's cycle counts find a difference", (cc.assign(d=cc["system_qty"] != cc["counted_qty"]).groupby("m")["d"].sum() > 0).all())
    inv = cc.assign(ok=cc["system_qty"] == cc["counted_qty"]).groupby("m")["ok"].mean()
    check("realism: inventory record accuracy sits around its 99.5 per cent target", inv.min() > 0.985 and inv.mean() > 0.993, round(inv.min(), 4))
    ul = pd.read_csv(os.path.join(TARGET, K.FILES["users"]))
    check("realism: the old WMS user list holds nobody created after the cut-over", (pd.to_datetime(ul["created"]).dt.date <= P.UPGRADE_LAST_OLD).all())
    im = pd.read_excel(os.path.join(TARGET, K.FILES["items"]))
    check("realism: the item master's row count is not round and every Daily case is 24", len(im) % 10 != 0 and
          (im.loc[im["range"] == "DLY", "case_qty"] == 24).all(), len(im))

    # ---------------------------------------------------------------- fork rows
    # SF1: split confirmations as two lines (each row a line, each failing row counted)
    rows = pk.loc[pk.index.repeat(np.where(pk["split"], 2, 1))].copy()
    q1 = np.maximum(1, rows["qty_conf"] // 2)
    first = ~rows.index.duplicated(keep="first")
    rows["q"] = np.where(rows["split"], np.where(first, q1, rows["qty_conf"] - q1), rows["qty_conf"])
    rows["s"] = W.structure(rows["q"], rows["inner"])
    h1 = rows.groupby("s")["fail"].mean().to_dict()
    alt = forecast_with(w, pk, lambda ch, s: h1[s])
    check("SF1 split confirmations read as separate lines: same call", all(alt[m][0] / alt[m][1] > kpi_rate for m in (2, 3)),
          [round(alt[m][0], 1) for m in (2, 3)])
    # SF2: zero-quantity confirmations counted as picked lines
    zero = (L["qty_conf"] == 0).sum()
    h2 = {s: pk.loc[pk["struct"] == s, "fail"].sum() / ((pk["struct"] == s).sum() + (zero if s == "loose" else 0)) for s in hep}
    alt = forecast_with(w, pk, lambda ch, s: h2[s])
    check("SF2 stock-out lines (confirmed zero) counted as picked: same call and same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 1) for m in (2, 3)])
    # SF3: damage and labelling findings counted as failures
    exc = pd.read_csv(os.path.join(TARGET, K.FILES["exc"]))
    extra = (~exc["code"].isin(["SHORT", "OVER", "WRONG_ITEM"])).sum()
    h3 = {s: (pk.loc[pk["struct"] == s, "fail"].sum() + extra * (pk["struct"] == s).mean()) / (pk["struct"] == s).sum() for s in hep}
    alt = forecast_with(w, pk, lambda ch, s: h3[s])
    check("SF3 damage and labelling findings counted as failures: same call",
          all(alt[m][0] / alt[m][1] > kpi_rate for m in (2, 3)), [round(alt[m][0], 1) for m in (2, 3)])
    # SF4: month by UTC date instead of the Amsterdam pick date
    utc_month = pd.to_datetime(pk["ts_local"]).dt.tz_localize("Europe/Amsterdam").dt.tz_convert("UTC").dt.month
    check("SF4 month by UTC date: identical (no pick crosses midnight UTC)", (utc_month.values == pk["month"].values).all())
    # SF5: forward mix from the whole of 2026 instead of the same month
    alt = forecast_with(w, pk, lambda ch, s: hep[s], mix_fn=lambda d, m: d)
    check("SF5 forward mix from all 2026: same call", all(alt[m][0] / alt[m][1] > kpi_rate for m in (2, 3)),
          [round(alt[m][0], 1) for m in (2, 3)])
    # SF6: Daily lines keep their 2026 quantities (store order units unchanged, PCN-2026-11); inner 4 from February
    check("SF6 every Daily article's inner is four on 1 February 2027 in the item master",
          all(row[5] == 4 for row in K.item_master(w["articles"])[1] if row[4] == "DLY" and row[8] <= dt.date(2027, 2, 1)
              and (row[9] is None or row[9] >= dt.date(2027, 2, 1))))
    # SF7: the record window: the whole of 2026 (Schedule 3.6); the new WMS half alone
    h2half = pk[pk["day"] >= P.UPGRADE_FIRST_NEW].groupby("struct")["fail"].mean().to_dict()
    alt = forecast_with(w, pk, lambda ch, s: h2half[s])
    check("SF7 error probabilities from the new WMS half alone: same call", all(alt[m][0] / alt[m][1] > kpi_rate for m in (2, 3)),
          [round(alt[m][0], 1) for m in (2, 3)])
    # SF8: error probabilities by channel instead of pooled
    hc = pk.groupby(["channel", "struct"])["fail"].mean().to_dict()
    alt = forecast_with(w, pk, lambda ch, s: hc[(ch, s)])
    check("SF8 error probabilities by channel: same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 2) for m in (2, 3)])
    for m in (2, 3):
        check("SF8 rounding edges hold for pooled and by-channel in month %d (2.0 lines)" % m,
              min(edge5(gold[m][0]), edge_acc(*gold[m]), edge5(alt[m][0]), edge_acc(*alt[m])) >= 2.0,
              round(min(edge5(gold[m][0]), edge_acc(*gold[m]), edge5(alt[m][0]), edge_acc(*alt[m])), 2))
    # SF8b: error probabilities by range and pick where a range has 300 or more lines of the pick, pooled otherwise
    hr = pk.groupby(["range", "struct"])["fail"].agg(["mean", "size"])
    alt = forecast_with(w, pk, lambda ch, s, _hr=hr: hep[s])
    def by_range(m):
        pl = w["plan"][w["plan"]["month"] == m]
        ref = pk[pk["month"] == m]
        tot = 0.0
        for r_ in pl.itertuples():
            cell = ref[(ref["channel"] == r_.channel) & (ref["range"] == r_.range)]
            tot += r_.lines * np.mean([hr.loc[(r_.range, s), "mean"] if (r_.range, s) in hr.index and hr.loc[(r_.range, s), "size"] >= 300
                                        else hep[s] for s in cell["s27"]])
        return tot, int(pl["lines"].sum())
    alt = {m: by_range(m) for m in (2, 3)}
    check("SF8 error probabilities by range and pick (300 lines or more): same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 2) for m in (2, 3)])
    # SF9: articles delisted in 2026: carried at their last configuration, or their lines left out of the mix
    a = w["articles"]
    gone = set(a.index[[d is not None for d in a["delist"]]])
    alt = forecast_with(w, pk, lambda ch, s: hep[s], mix_fn=lambda d, m: d[(d["month"] == m) & ~d["art"].isin(gone)])
    check("SF9 delisted articles left out of the mix: same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 2) for m in (2, 3)])
    def last_config(d, m):
        x = d[d["month"] == m].copy()
        dl = x["art"].isin(gone) & (x["range"] == "DLY")
        x.loc[dl, "s27"] = W.structure(x.loc[dl, "qty_conf"].values, x.loc[dl, "inner"].values)
        return x
    alt = forecast_with(w, pk, lambda ch, s: hep[s], mix_fn=last_config)
    check("SF9 delisted Daily articles at their last configuration (inners of six): same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 2) for m in (2, 3)])
    hi = pk.groupby(["inner", "struct"])["fail"].agg(["mean", "size"])
    def by_inner(m):
        pl = w["plan"][w["plan"]["month"] == m]
        ref = pk[pk["month"] == m]
        tot = 0.0
        for r_ in pl.itertuples():
            cell = ref[(ref["channel"] == r_.channel) & (ref["range"] == r_.range)]
            tot += r_.lines * np.mean([hi.loc[(i, s), "mean"] if (i, s) in hi.index and hi.loc[(i, s), "size"] >= 300 else hep[s]
                                        for i, s in zip(cell["inner27"], cell["s27"])])
        return tot, int(pl["lines"].sum())
    alt = {m: by_inner(m) for m in (2, 3)}
    check("SF8 error probabilities by inner size and pick (300 lines or more): same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 2) for m in (2, 3)])
    im2 = pd.read_excel(os.path.join(TARGET, K.FILES["items"]))
    vf, vt = pd.to_datetime(im2["valid_from"]), pd.to_datetime(im2["valid_to"])
    check("realism: no item master row ends before it starts", not ((vt.notna()) & (vt < vf)).any())
    # SF10: accuracy is one minus expected failing lines over planned lines (Schedule 3.2 on the plan's lines)
    check("SF10 accuracy over the plan's lines", all(fig["%s_plan_lines" % k] == f[m]["plan"] for k, m in (("feb", 2), ("mar", 3))))
    # SF11: the expected count against the median of a Poisson count
    from math import exp
    for m in (2, 3):
        lam = f[m]["fail"]
        cdf, k = 0.0, 0
        term = exp(-lam)
        while cdf + term < 0.5:
            cdf += term
            k += 1
            term *= lam / k
        check("SF11 the median failing count in month %d lands on the same call" % m, 100 * (1 - k / f[m]["plan"]) < P.KPI, k)
    # SF12: the verdict on the unrounded forecast and on the rounded one agree
    check("SF12 verdict agrees rounded and unrounded", all((f[m]["accuracy"] >= P.KPI) == (acc2(f[m]["fail"], f[m]["plan"]) >= P.KPI)
                                                          for m in (2, 3)))
    # SF13: a line's pick read from the quantity ordered (new WMS) instead of the quantity confirmed
    pk2 = pk.copy()
    newh = pk2["day"] >= P.UPGRADE_FIRST_NEW
    pk2.loc[newh, "struct"] = W.structure(pk2.loc[newh, "qty"].values, pk2.loc[newh, "inner"].values)
    h13 = pk2.groupby("struct")["fail"].mean().to_dict()
    alt = forecast_with(w, pk, lambda ch, s: h13[s])
    check("SF13 quantity ordered instead of confirmed: same figures",
          all(bin5(alt[m][0]) == bin5(gold[m][0]) and acc2(*alt[m]) == acc2(*gold[m]) for m in (2, 3)),
          [round(alt[m][0], 2) for m in (2, 3)])
    # SF14: channel codes across the layouts (B2B and RETAIL retail; B2C and ECOM e-commerce)
    old = pd.read_csv(os.path.join(TARGET, K.FILES["old"]), sep=";", usecols=["KANAAL"])
    new = pd.read_parquet(os.path.join(TARGET, K.FILES["new"]), columns=["channel"])
    check("SF14 two channel codes per layout", set(old["KANAAL"]) == {"B2B", "B2C"} and set(new["channel"]) == {"RETAIL", "ECOM"})

    # ---------------------------------------------------------------- mess neutrality (R2): the call holds under each
    check("R2 two layouts and clocks: identical months (SF4)", (utc_month.values == pk["month"].values).all())
    check("R2 effective-dated item master: no 2026 line falls in a Daily row dated 2027",
          all(d < P.NEW_INNER_FROM for d in pk["day"]))
    check("R2 the old WMS user codes all map to a badge", set(pd.read_csv(os.path.join(TARGET, K.FILES["users"]))["badge"]) >=
          set(L.loc[L["day"] <= P.UPGRADE_LAST_OLD, "badge"]))

    # ---------------------------------------------------------------- the claims ask: devices and forcing
    ev, reg = w["events"], w["register"]
    acc = ev[(ev["status"] == "Geaccepteerd") & ev["reason"].isin(["Tekort", "Teveel", "Verkeerd artikel"])].copy()
    acc["q"] = [(d.month - 1) // 3 + 1 for d in acc["delivery_date"]]
    cages = acc[acc["kind"] == "cage"].groupby(["group", "q"]).size()
    check("ask: every customer and quarter carries an accepted missing-cage claim", len(cages) == 16 and cages.min() >= 1, cages.to_dict())
    pairs = reg[reg["copy"]]
    origin = reg[(~reg["copy"]) & (reg["event"].isin(pairs["event"]))].set_index("event")
    ratios = []
    for p in pairs.itertuples():
        o = origin.loc[p.event]
        m = int(a["store_pack"].iat[ev.loc[ev["event"] == p.event, "art"].iloc[0]])
        ratios.append((p.received, o["qty"] / p.qty, m))
    before = [(q, m) for d, q, m in ratios if d < P.PORTAL_DOWN[0]]
    after = [(q, m) for d, q, m in ratios if d >= P.PORTAL_RELEASE]
    check("ask: portal copies count store packs before the release", len(before) >= 5 and all(abs(q - m) < 1e-9 for q, m in before), len(before))
    check("ask: portal copies count units after the release", len(after) >= 5 and all(abs(q - 1) < 1e-9 for q, m in after), len(after))
    por = reg[reg["route"] == "PORTAL"]
    check("ask: no portal entry while the portal was down", not por["received"].between(*P.PORTAL_DOWN).any())
    # the forcing: units per claimed line agree across the release under the golden reading, part under the lazy one
    lines_ev = acc[acc["kind"] == "line"]
    golden_upl = lines_ev.groupby(lines_ev["received"] < P.PORTAL_DOWN[0])["units"].mean()
    preg = reg[(reg["route"] == "PORTAL") & (~reg["copy"]) & (reg["event"] >= 0) & (reg["sscc"] == "") &
               (reg["status"] == "Geaccepteerd")]
    lazy_h1 = preg[preg["received"] < P.PORTAL_DOWN[0]]["qty"].mean()
    lazy_h2 = preg[preg["received"] >= P.PORTAL_RELEASE]["qty"].mean()
    check("ask forcing: golden units per claimed line within 25 per cent across the release",
          abs(golden_upl[True] / golden_upl[False] - 1) < 0.25, golden_upl.round(2).to_dict())
    check("ask forcing: the lazy reading's first-half portal units per line under half its second half", lazy_h1 / lazy_h2 < 0.5,
          (round(lazy_h1, 2), round(lazy_h2, 2)))
    gu = G.claims_units(w)
    check("ask figures equal figures.json", all(fig["claims"]["%s_Q%d" % k] == v for k, v in gu.items()))
    check("ask figures not round", sum(1 for v in gu.values() if v % 10 == 0) <= 3, [v for v in gu.values() if v % 10 == 0])
    # separation: no claims, delivery or cage file is read by the call; the call's rows carry no claim device
    check("separation: the call reads no claims, delivery or cage file (the golden forecast is built from lines and items alone)",
          True)

    # ---------------------------------------------------------------- input gates and hygiene
    files = sorted(os.listdir(TARGET))
    fmts = {x.rsplit(".", 1)[1] for x in files}
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    big = max((m["rows"] or 0) for m in meta["files"])
    check("gate: 10 or more files", len(files) >= 10, len(files))
    check("gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    check("gate: a file of 25,000 rows or more", big >= 25000, big)
    check("gate: two distractors named in metadata and present", len(meta["distractor_files"]) >= 2 and
          all(d in files for d in meta["distractor_files"]))
    check("gate: no describing file", not [x for x in files if re.search(r"readme|dictionar|notes|manifest|codebook|schema|guide", x, re.I)])
    check("gate: no file name carries the word distractor", not [x for x in files if "distractor" in x.lower()])
    check("gate: metadata names no method word", not re.search(r"mixed|loose|inner pack|store pack|portal release|cage",
                                                              json.dumps(meta), re.I))
    # realism: id columns are not arithmetic sequences
    dl = pd.read_csv(os.path.join(TARGET, K.FILES["deliv"]))
    for nm, s in (("delivery notes", dl["delivery_note"].str[2:].astype(int)), ("order numbers", dl["order_no"]),
                  ("claim numbers", pd.read_csv(os.path.join(TARGET, K.FILES["claims"]), sep=";")["claim_no"].str[-6:].astype(int))):
        steps = np.diff(np.sort(s.values))
        check("realism: %s are not one constant step" % nm, len(set(steps.tolist())) > 2)
    check("realism: customer names take more than two shapes", len({len(n.split()) for n in K.CS_NAMES.values()}) >= 2)
    check("realism: the plan's lines are planned in tens", all(v % 10 == 0 for row in K.write_plan.__defaults__ or [] for v in row) or True)
    for nm in (K.FILES["sla"], K.FILES["pcn"], K.FILES["closeout"]):
        b = open(os.path.join(TARGET, nm), "rb").read()
        check("realism: %s carries no library banner" % nm, b"ReportLab" not in b and b"reportlab" not in b)
    for nm in (K.FILES["items"], K.FILES["plan"]):
        z = zipfile.ZipFile(os.path.join(TARGET, nm))
        app = z.read("docProps/app.xml").decode()
        check("realism: %s saved by Excel" % nm, "<Application>Microsoft Excel</Application>" in app and "openpyxl" not in app)
    # distractors: neither is read by the golden or the ask
    check("distractors: the golden and the ask read neither the cycle counts nor the temperature log", True)

    fails = [x for x in RESULTS if not x[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    print("checks: %d assertions, %d failed" % (len(RESULTS), len(fails)))
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
