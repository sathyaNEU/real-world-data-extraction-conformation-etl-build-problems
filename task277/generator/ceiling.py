"""The ask ceiling, measured on the cut pack with code that shares nothing with the generator: each response row reads
target/ the way that response would and is scored against figures.json, a claims figure kept only when it equals the
golden (whole units). Rows: the cracker (lands the call, runs the hygiene battery, executes every rule the asking
sentence and Schedule 3 state), the mirror (stops on the most attractive wrong rung of the call, the same ask path),
and the full includers (each handles one device completely). Pair arithmetic on 38, 7 and 55.

    python3 task277/generator/ceiling.py [--target DIR]
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
from functools import reduce

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CHART_CRITERIA = 4          # 2026 monthly line, the two forecast months, the target line, the values labelled
CHART_KEPT_BY_MIRROR = 3    # everything but the forecast months' values


def one(target, pat):
    f = [x for x in os.listdir(target) if re.search(pat, x)]
    assert len(f) == 1, (pat, f)
    return os.path.join(target, f[0])


def load(target):
    reg = pd.read_csv(one(target, r"claims"), sep=";", dtype=str).fillna("")
    reg["d"] = pd.to_datetime(reg["ontvangen"], dayfirst=True)
    reg["n"] = reg["aantal"].astype(int)
    dl = pd.read_csv(one(target, r"deliveries"), dtype=str).fillna("")
    dl["q"] = pd.to_datetime(dl["delivery_date"]).dt.quarter
    dl["y"] = pd.to_datetime(dl["delivery_date"]).dt.year
    items = pd.read_excel(one(target, r"item_master"))
    ean2sku = dict(zip(items["ean"].astype(str), items["sku"]))
    art2sku = dict(zip(items["article_no"].astype(str), items["sku"]))
    old = pd.read_csv(one(target, r"pick_confirmations.*csv$"), sep=";")
    o = old.groupby(["ORDERNR", "REGELNR"]).agg(sku=("ARTIKELNR", "first"), qty=("AANTAL", "sum"), ch=("KANAAL", "first")).reset_index()
    o.columns = ["order", "line", "sku", "qty", "ch"]
    new = pd.read_parquet(one(target, r"parquet$"))
    n = new.groupby(["order_id", "line_no"]).agg(sku=("sku", "first"), qty=("qty_confirmed", "sum"), ch=("channel", "first")).reset_index()
    n.columns = ["order", "line", "sku", "qty", "ch"]
    lines = pd.concat([o, n])
    retail = lines[lines["ch"].isin(["B2B", "RETAIL"]) & (lines["qty"] > 0)]
    packs = {}
    for sku, s in retail.groupby("sku")["qty"]:
        vc = s.value_counts()
        keep = [int(v) for v in vc[vc >= max(2, 0.01 * len(s))].index] or [int(v) for v in vc.index]
        packs[sku] = reduce(math.gcd, keep)
    colli = pd.read_csv(one(target, r"colli"), dtype={"sscc": str})
    cages = colli.groupby("sscc")["qty"].sum().to_dict()
    cages.update(new[new["channel"] == "RETAIL"].groupby("container")["qty_confirmed"].sum().to_dict())
    return reg, dl, ean2sku, art2sku, packs, cages


def respond(data, portal, cage, dedupe=True):
    """portal: 'all' converts every portal quantity at the store order unit, 'none' reads it as units, 'release' converts
    entries before the portal's release break, 'quarter' converts deliveries of the first half. cage: 'one' counts a
    missing-cage row as the one it records, 'expand' counts the cage's units."""
    reg, dl, ean2sku, art2sku, packs, cages = data
    by_note = dl.set_index("delivery_note")
    by_po = dl[dl["store_po"] != ""].set_index("store_po")
    por_days = sorted(reg.loc[reg["kanaal"] == "PORTAL", "d"].unique())
    gaps = sorted(((b - a).days, a, b) for a, b in zip(por_days, por_days[1:]) if pd.Timestamp("2026-06-01") < a < pd.Timestamp("2026-09-01"))
    release = gaps[-1][2]
    ok = reg[(reg["status"] == "Geaccepteerd") & reg["reden"].isin(["Tekort", "Teveel", "Verkeerd artikel"])]
    out, seen = {}, set()
    for r in ok.itertuples():
        if r.referentie in by_note.index:
            d = by_note.loc[r.referentie]
        elif r.referentie in by_po.index:
            d = by_po.loc[r.referentie]
        else:
            continue
        if int(d["y"]) != 2026:
            continue
        key = (d["customer"], int(d["q"]))
        if r.sscc:
            units = cages[r.sscc] if cage == "expand" else r.n
            ident = ("cage", r.sscc)
        else:
            sku = ean2sku.get(r.artikel) if r.kanaal == "EDI" else art2sku.get(r.artikel)
            units = r.n
            if r.kanaal == "PORTAL":
                conv = {"all": True, "none": False, "release": r.d < release, "quarter": int(d["q"]) <= 2}[portal]
                if conv:
                    units = r.n * packs[sku]
            ident = (d["order_no"], sku)
        if dedupe and ident in seen:
            continue
        seen.add(ident)
        out[key] = out.get(key, 0) + units
    return out


def score(resp, gold):
    return sum(1 for k, v in gold.items() if resp.get(k, 0) == v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(TASK, "target"))
    args = ap.parse_args()
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold = {(k.split("_Q")[0], int(k.split("_Q")[1])): v for k, v in fig["claims"].items()}
    data = load(args.target)
    rows = [
        ("cracker", "lands the call; battery: re-keys store POs to delivery notes, merges each claimed line's EDI and portal rows, "
                    "converts portal quantities at the store order unit once the copies show packs; a missing-cage row as recorded",
         respond(data, "all", "one")),
        ("lazy", "the register read as it stands: portal quantities as units, cage rows as recorded", respond(data, "none", "one")),
        ("full includer, portal", "the release found and portal entries before it converted, lines merged; cage rows as recorded",
         respond(data, "release", "one")),
        ("full includer, cages", "every missing cage counted at the units it carried; the battery's conversion of every portal entry",
         respond(data, "all", "expand")),
        ("full includer, cages and halves", "cages counted; portal entries converted for first-half deliveries",
         respond(data, "quarter", "expand")),
        ("golden path", "cages counted, portal entries before the release converted, lines merged", respond(data, "release", "expand")),
    ]
    n = len(gold)
    digest = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:8] if os.path.exists(
        os.path.join(TASK, "target.zip")) else "unzipped"
    print("pack", digest)
    res = {}
    for name, how, resp in rows:
        k = score(resp, gold)
        res[name] = k
        print("%-34s keeps %2d of %d claims figures  %s" % (name, k, n, "MISS" if k < n else "KEEPS"))
    assert res["golden path"] == n, "the golden path must reproduce every figure"
    total = n + CHART_CRITERIA
    lc = (res["cracker"] + CHART_CRITERIA) / total
    ls = (res["cracker"] + CHART_KEPT_BY_MIRROR) / total
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f; mirror leakage %.1f per cent of ask weight" % (c, s, (c + s) / 2, 100 * ls))
    bad = [r for r in ("cracker", "lazy", "full includer, portal", "full includer, cages", "full includer, cages and halves") if res[r] == n]
    if bad:
        sys.exit("a response row keeps the whole ask: %s" % bad)


if __name__ == "__main__":
    main()
