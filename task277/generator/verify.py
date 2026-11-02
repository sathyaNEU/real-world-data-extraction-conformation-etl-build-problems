"""Independent verifier: reads only the shipped folder (target/) and recomputes every graded figure on its own code
path, then compares with generator/figures.json. Exit 1 on any difference.

    python3 task277/generator/verify.py [--target DIR]
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import sys
from functools import reduce

import numpy as np
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
RANGES = {"Daily": "DLY", "Hair": "HAI", "Skin": "SKN", "Kids": "KID", "Men": "MEN", "Sun": "SUN"}
GOOD = {"SHORT", "OVER", "WRONG_ITEM"}


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def read_lines(target):
    old = pd.read_csv(find(target, r"^wms_pick_confirmations_2026-01-01.*\.csv$"), sep=";", dtype={"GEBRUIKER": str})
    old["ts"] = pd.to_datetime(old["DATUM"] + " " + old["TIJD"], format="%d-%m-%Y %H:%M:%S")
    o = pd.DataFrame({"order_no": old["ORDERNR"], "line_no": old["REGELNR"], "sku": old["ARTIKELNR"],
                      "qty": old["AANTAL"], "ts_local": old["ts"],
                      "channel": old["KANAAL"].map({"B2B": "T", "B2C": "W"}), "src": "old", "container": ""})
    new = pd.read_parquet(find(target, r"^wms_pick_confirmations_2026-06-15.*\.parquet$"))
    loc = new["confirmed_at"].dt.tz_convert("Europe/Amsterdam").dt.tz_localize(None)
    n = pd.DataFrame({"order_no": new["order_id"], "line_no": new["line_no"], "sku": new["sku"],
                      "qty": new["qty_confirmed"], "ts_local": loc,
                      "channel": new["channel"].map({"RETAIL": "T", "ECOM": "W"}), "src": "new",
                      "container": new["container"]})
    rows = pd.concat([o, n], ignore_index=True)
    assert rows["channel"].notna().all()
    lines = rows.groupby(["order_no", "line_no"], sort=True).agg(
        sku=("sku", "first"), qty=("qty", "sum"), ts=("ts_local", "min"), channel=("channel", "first")).reset_index()
    lines["day"] = lines["ts"].dt.date
    lines = lines[lines["qty"] > 0].copy()
    return lines, rows, new


def read_items(target):
    it = pd.read_excel(find(target, r"item_master.*\.xlsx$"), sheet_name=0)
    it["valid_from"] = [d.date() for d in pd.to_datetime(it["valid_from"])]
    it["valid_to"] = [None if pd.isna(d) else d.date() for d in pd.to_datetime(it["valid_to"])]
    return it


def inner_on(it, skus, days):
    """The inner pack in force for each (sku, day): the item master row whose validity covers the day."""
    by = {}
    for r in it.itertuples():
        by.setdefault(r.sku, []).append((r.valid_from, r.valid_to if isinstance(r.valid_to, dt.date) else dt.date(2099, 1, 1), r.inner_qty))
    out = np.zeros(len(skus), int)
    for i, (s, d) in enumerate(zip(skus, days)):
        hit = [q for f, t, q in by[s] if f <= d <= t]
        assert len(hit) == 1, (s, d, hit)
        out[i] = hit[0]
    return out


def kind(q, inner):
    q, inner = np.asarray(q), np.asarray(inner)
    return np.where(q % inner == 0, "whole", np.where(q < inner, "loose", "mixed"))


def main_call(target):
    lines, rows, new = read_lines(target)
    exc = pd.read_csv(find(target, r"^packout_exceptions"))
    exc = exc[exc["code"].isin(GOOD)]
    exc["order_no"] = exc["order_ref"].str.replace("SIE", "", regex=False).astype(int)
    bad = set(zip(exc["order_no"], exc["line"]))
    lines["fail"] = [(o, l) in bad for o, l in zip(lines["order_no"], lines["line_no"])]
    assert lines["fail"].sum() == len(bad), "every failing line is a picked line"
    it = read_items(target)
    rng = it.drop_duplicates("sku").set_index("sku")["range"]
    lines["range"] = lines["sku"].map(rng)
    # the 2026 record: inner in force on each pick date, through a per-sku table (fast path, checked on a sample)
    first = {}
    for r in it.itertuples():
        first.setdefault(r.sku, []).append(r)
    lines["inner"] = [min((x for x in first[s] if x.valid_from <= d), key=lambda x: (d - x.valid_from)).inner_qty
                      for s, d in zip(lines["sku"], lines["day"])]
    smp = lines.sample(2000, random_state=1)
    assert (inner_on(it, smp["sku"].values, smp["day"].values) == smp["inner"].values).all()
    lines["kind"] = kind(lines["qty"], lines["inner"])
    lines["month"] = [d.month for d in lines["day"]]
    hist = lines.groupby("month").agg(n=("fail", "size"), f=("fail", "sum"))
    hist["acc"] = 100 * (1 - hist["f"] / hist["n"])
    hep = lines.groupby("kind")["fail"].mean().to_dict()
    # the plan
    pl = pd.read_excel(find(target, r"volume_plan.*\.xlsx$"), header=None)
    hdr = pl.index[pl.iloc[:, 0].astype(str).str.strip() == "Range"][0]
    plan = pl.iloc[hdr + 1:, :5].dropna(how="all")
    plan.columns = ["range", "channel", "Jan", "Feb", "Mar"]
    plan["range"] = plan["range"].map(RANGES)
    plan["channel"] = plan["channel"].map({"Retail": "T", "E-commerce": "W"})
    # each article's configuration on 1 February 2027: the latest row dated on or before it (an article delisted in
    # 2026 keeps its last configuration, carried in the 2026 mix the plan repeats)
    inner27 = {}
    for r in sorted(it.itertuples(), key=lambda x: (x.sku, x.valid_from)):
        if r.valid_from <= dt.date(2027, 2, 1):
            inner27[r.sku] = r.inner_qty
    new_daily = {r.inner_qty for r in it.itertuples() if r.range == "DLY" and r.valid_from >= dt.date(2027, 1, 1)}
    assert len(new_daily) == 1, new_daily
    for r in it.itertuples():
        if r.range == "DLY":
            inner27[r.sku] = min(new_daily)    # PCN-2026-11: the Daily range, all articles
    out = {}
    for m, col in ((2, "Feb"), (3, "Mar")):
        ref = lines[lines["month"] == m].copy()
        ref["k27"] = kind(ref["qty"], ref["sku"].map(inner27).values)
        tot, n = 0.0, 0
        for r in plan.itertuples():
            cell = ref[(ref["channel"] == r.channel) & (ref["range"] == r.range)]
            tot += int(getattr(r, col)) * cell["k27"].map(hep).mean()
            n += int(getattr(r, col))
        out[m] = dict(fail=tot, n=n, acc=100 * (1 - tot / n))
    return out, hist, hep, lines, rows, new, it


def store_packs(lines):
    """Each article's store order unit: the common divisor of the quantities its retail lines carry, leaving out the
    odd quantity a stock-out left on a line."""
    t = lines[lines["channel"] == "T"]
    out = {}
    for sku, s in t.groupby("sku")["qty"]:
        vc = s.astype(int).value_counts()
        keep = vc[vc >= max(2, 0.01 * len(s))].index.tolist() or vc.index.tolist()
        out[sku] = reduce(math.gcd, keep)
    return out


def claims(target, lines, rows, new, it):
    reg = pd.read_csv(find(target, r"store_claims.*\.csv$"), sep=";", dtype=str)
    reg["received"] = pd.to_datetime(reg["ontvangen"], format="%d-%m-%Y").dt.date
    reg["aantal"] = reg["aantal"].astype(int)
    dl = pd.read_csv(find(target, r"^dispatch_deliveries"), dtype=str)
    dl["delivery_date"] = pd.to_datetime(dl["delivery_date"]).dt.date
    by_note = dl.set_index("delivery_note")
    by_po = dl[dl["store_po"].notna()].set_index("store_po")
    sku_of_ean = it.drop_duplicates("sku").set_index("ean")["sku"].astype(int).to_dict()
    sku_of_art = it.drop_duplicates("sku").set_index("article_no")["sku"].astype(int).to_dict()
    packs = store_packs(lines)
    line_of = {(o, s): l for o, s, l in zip(lines["order_no"], lines["sku"], lines["line_no"])}
    # the portal release: where portal copies of EDI claims stop counting store packs
    edi = reg[reg["kanaal"] == "EDI"]
    por = reg[reg["kanaal"] == "PORTAL"]
    switch_hi, switch_lo = None, None
    for r in por.itertuples():
        if not r.artikel or (isinstance(r.artikel, float)):
            continue
    ratio = []
    for r in por.itertuples():
        if not isinstance(r.artikel, str) or not r.artikel:
            continue
        sku = sku_of_art.get(int(r.artikel))
        if sku is None:
            continue
        cand = edi[(edi["filiaal"] == r.filiaal) & (edi["artikel"].map(lambda e: sku_of_ean.get(int(e)) if isinstance(e, str) and e else None) == sku)]
        for c in cand.itertuples():
            if c.received <= r.received and (r.received - c.received).days <= 7 and packs[sku] > 1:
                ratio.append((r.received, c.aantal / r.aantal, packs[sku]))
    # portal copies of EDI claims count store packs up to one date and units after another; the portal's entries break
    # once between the two (its release), and that break divides the portal rows
    pack_d = max(d for d, q, m in ratio if abs(q - m) < 1e-9)
    unit_d = min(d for d, q, m in ratio if abs(q - 1) < 1e-9)
    assert pack_d < unit_d and all(abs(q - m) < 1e-9 for d, q, m in ratio if d <= pack_d) and \
        all(abs(q - 1) < 1e-9 for d, q, m in ratio if d >= unit_d), "one regime change"
    days = sorted(d for d in por["received"].unique() if pack_d <= d <= unit_d)
    gaps = [((b_ - a_).days, a_, b_) for a_, b_ in zip(days, days[1:])]
    big = [g for g in gaps if g[0] >= 5]
    assert len(big) == 1, ("one break inside the bracket", big)
    last_pack, first_unit = big[0][1], big[0][2]
    between = por[(por["received"] > last_pack) & (por["received"] < first_unit)]
    out_rows = []
    for r in reg[(reg["status"] == "Geaccepteerd") & reg["reden"].isin(["Tekort", "Teveel", "Verkeerd artikel"])].itertuples():
        ref = r.referentie
        if ref in by_note.index:
            d = by_note.loc[ref]
        elif ref in by_po.index:
            d = by_po.loc[ref]
        else:
            continue
        order_no = int(d["order_no"])
        q = (d["delivery_date"].month - 1) // 3 + 1
        if d["delivery_date"].year != 2026:
            continue
        if isinstance(r.sscc, str) and r.sscc:
            out_rows.append((d["customer"], q, ("cage", r.sscc), None))
            continue
        sku = sku_of_ean[int(r.artikel)] if r.kanaal == "EDI" else sku_of_art[int(r.artikel)]
        if r.kanaal == "PORTAL" and r.received <= last_pack:
            units = r.aantal * packs[sku]
        elif r.kanaal == "PORTAL":
            assert r.received >= first_unit
            units = r.aantal
        else:
            units = r.aantal
        out_rows.append((d["customer"], q, ("line", order_no, line_of[(order_no, sku)]), units))
    # cage contents: the dispatch module to the cut-over, the new WMS's container after it
    col = pd.read_csv(find(target, r"^dispatch_colli"), dtype={"sscc": str})
    cage_units = col.groupby("sscc")["qty"].sum().to_dict()
    nw = new[(new["container"] != "") & (new["channel"] == "RETAIL")].groupby("container")["qty_confirmed"].sum().to_dict()
    for k, v in nw.items():
        assert k not in cage_units
        cage_units[k] = v
    seen = {}
    for cust, q, key, units in out_rows:
        if key[0] == "cage":
            units = int(cage_units[key[1]])
        if key in seen:
            assert seen[key][2] == units, ("a line claimed twice must agree", key, seen[key], units)
            continue
        seen[key] = (cust, q, units)
    res = {}
    for cust, q, units in seen.values():
        res[(cust, q)] = res.get((cust, q), 0) + units
    return res, (last_pack, first_unit, len(between))


def closeout(target):
    with pdfplumber.open(find(target, r"closeout.*\.pdf$")) as pdf:
        text = "\n".join(p.extract_text() for p in pdf.pages)
    acc = {}
    names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
    for k, nm in enumerate(names, 1):
        m = re.search(r"^%s\s+([\d,]+)\s+([\d.]+)%%" % nm, text, re.M)
        acc[k] = (int(m.group(1).replace(",", "")), float(m.group(2)))
    return acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(TASK, "target"))
    args = ap.parse_args()
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    fc, hist, hep, lines, rows, new, it = main_call(args.target)
    for m, key in ((2, "feb"), (3, "mar")):
        r5 = int(10 * math.floor(fc[m]["fail"] / 10 + 0.5))
        acc = "%.1f" % (fc[m]["acc"] + 1e-12)
        if r5 != fig["%s_failing_lines" % key]:
            bad.append(("%s failing lines" % key, r5, fig["%s_failing_lines" % key]))
        if acc != fig["%s_accuracy" % key]:
            bad.append(("%s accuracy" % key, acc, fig["%s_accuracy" % key]))
        if fc[m]["n"] != fig["%s_plan_lines" % key]:
            bad.append(("%s plan" % key, fc[m]["n"], fig["%s_plan_lines" % key]))
    for k in range(1, 13):
        if "%.2f" % hist.loc[k, "acc"] != fig["history"][str(k)]:
            bad.append(("history %d" % k, "%.2f" % hist.loc[k, "acc"], fig["history"][str(k)]))
    for s in ("whole", "loose", "mixed"):
        if "%.3f" % (100 * hep[s]) != fig["hep_%s_pct" % s]:
            bad.append(("hep " + s, "%.3f" % (100 * hep[s]), fig["hep_%s_pct" % s]))
    co = closeout(args.target)
    for k in range(1, 13):
        if co[k][0] != int(hist.loc[k, "n"]) or abs(co[k][1] - round(hist.loc[k, "acc"], 2)) > 1e-9:
            bad.append(("closeout %d" % k, co[k], (int(hist.loc[k, "n"]), round(hist.loc[k, "acc"], 2))))
    cl, sw = claims(args.target, lines, rows, new, it)
    for key, v in fig["claims"].items():
        g, q = key.split("_Q")
        if cl.get((g, int(q)), 0) != v:
            bad.append(("claims " + key, cl.get((g, int(q)), 0), v))
    print("verify: forecast Feb %.2f lines %.3f%%, Mar %.2f lines %.3f%%; portal switch between %s and %s (%d rows between)"
          % (fc[2]["fail"], fc[2]["acc"], fc[3]["fail"], fc[3]["acc"], sw[0], sw[1], sw[2]))
    if bad:
        for b in bad:
            print("MISMATCH", b)
        sys.exit(1)
    print("verify: PASS, every graded figure recomputed from target/ alone")


if __name__ == "__main__":
    main()
