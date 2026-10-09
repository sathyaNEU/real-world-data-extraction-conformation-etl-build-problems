#!/usr/bin/env python3
"""Build task121's evidence pack.

    python3 build.py --out <dir> [--record <json>]

Writes <dir>/target/ (the bundle) and <dir>/metadata.json, runs every assertion in checks.py and
exits non-zero on the first failure. Deterministic: two runs write byte-identical files."""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np
import pandas as pd

import analysis as N
import assemble as A
import calib as C
import docs as D
import params as P
import tune as U
import world as W
import writers as WR

F = {
    "sessions": "basket_sessions_2026-07-27_2026-09-27.parquet",
    "edge": "edge_bot_verdicts_2026-07-27_2026-09-27.csv",
    "tokens_aug": "cdm_token_billing_2026-08.csv",
    "tokens_sep": "cdm_token_billing_2026-09.csv",
    "profiles": "loyalty_profiles_2026-09-28.csv",
    "promo": "promo_redemptions_2025-07-01_2026-06-30.csv",
    "address": "address_book_history_2026-09-28.csv",
    "flags": "checkout_flags_export_2026-09-28.json",
    "cards": "saved_cards_2026-09-28.csv",
    "card_changes": "saved_card_events_2026-07-27_2026-09-27.csv",
    "auth": "tagus_3ds_log_2026-08-31_2026-09-27.csv",
    "psp": "tagus_3ds_report_2026-09.pdf",
    "finance": "finance_order_export_2026-07-27_2026-09-27.csv",
    "catalogue": "catalogue_status_history.csv",
    "dashboard": "weekly_trading_dashboard_2026-w39.xlsx",
    "shortlist": "q4_sprint_shortlist.docx",
    "agreement": "cdm_partnership_agreement_2026-27_extract.pdf",
    "closeout_margens": "closeout_festival_margens_app_2025.xlsx",
    "closeout_kaiju": "closeout_kaiju_tuga_link_page_2025.xlsx",
    "release_log": "release_log_2026.xlsx",
    "field_reference": "warehouse_field_reference.md",
    "thread": "inc-0914-checkout-conversion_export.txt",
    "register": "warehouse_extract_register.csv",
    "carrier": "lusolog_cp7_label_notice_2026-07.pdf",
    "stock": "stock_availability_2026-09-25.csv",
}
DISTRACTORS = ["carrier", "stock"]
EXPORT_TIME = dt.datetime(2026, 9, 30, 10, 0)


def dashboard_figures(s):
    weekly, by_source, steps = [], [], []
    for w in P.WEEK_NAMES:
        x = s[s.week == w]
        lab = P.WEEK_STARTS[P.WEEK_NAMES.index(w)].date().isoformat()
        weekly.append(dict(week=lab, sessions=int(len(x)), orders=int(x.conv.sum()),
                           conversion=round(100 * x.conv.mean(), 2)))
        r = {"week": lab}
        for src, g in x.groupby("traffic_source"):
            r[src] = round(100 * g.conv.mean(), 2)
        by_source.append(r)
        idx = x.furthest_step.map({k: i for i, k in enumerate(P.STEPS)})
        reach = [int((idx >= i).sum()) for i in range(6)]
        steps.append(dict(week=lab, reach=reach,
                          completion=[round(100 * reach[i + 1] / reach[i], 1) for i in range(5)]))
    return weekly, by_source, steps


def psp_weekly(auth):
    a = auth.drop_duplicates("attempt_ref").copy()
    a["t"] = pd.to_datetime(a.sent_at)
    a["week"] = N.weeks_of(a.t)
    out = []
    for w in P.REVIEW:
        x = a[a.week == w]
        lab = f"Wk {36 + P.REVIEW.index(w)} ({P.WEEK_STARTS[P.WEEK_NAMES.index(w)].strftime('%d %b')})"
        out.append(dict(label=lab, attempts=len(x), frictionless=int(x.three_ds_status.isin(["Y", "A", "I"]).sum()),
                        challenged=int(x.three_ds_status.isin(["C", "D"]).sum()),
                        failed=int(x.three_ds_status.isin(["N", "U"]).sum())))
    return out


def stock_table(rng, cat):
    rows = []
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    for sku, name in zip(cat.sku, cat.product_name):
        if sku.startswith("GFT") or sku in ("GAM-CE-ORION", "MUS-VBX-LUMEN", "MON-JKT-2627"):
            continue
        sz = sizes if ("shirt" in name or "top" in name or "hoodie" in name or "jacket" in name) else ["one size"]
        for z in sz:
            oh = int(rng.integers(0, 240)) if not sku.startswith("MON-K") else int(rng.integers(0, 90))
            res = int(min(oh, rng.integers(0, 25)))
            nd = (dt.date(2026, 10, 1) + dt.timedelta(days=int(rng.integers(0, 30)))).isoformat() if oh - res < 15 else ""
            rows.append((sku, z, oh, res, oh - res, nd))
    return pd.DataFrame(rows, columns=["sku", "size", "on_hand", "reserved", "available", "next_delivery"])


def register_rows(sizes):
    reg = [
        (F["sessions"], "storefront analytics", "2026-09-28", "2026-07-27", "2026-09-27",
         "Basket sessions only."),
        (F["edge"], "edge bot management", "2026-09-29", "2026-07-27", "2026-09-27", "Weekly verdict file."),
        (F["tokens_aug"], "CD Monteralto (club)", "2026-09-04", "2026-08-31", "2026-08-31",
         "As received with the club's August invoice."),
        (F["tokens_sep"], "CD Monteralto (club)", "2026-09-28", "2026-09-01", "2026-09-27",
         "As received; the club sent the September report early, to 27 September."),
        (F["profiles"], "CRM / loyalty", "2026-09-28", "", "", "Snapshot at extract."),
        (F["promo"], "promotions engine", "2026-09-28", "2025-07-01", "2026-06-30",
         "2025/26 season, every code redeemed at checkout."),
        (F["address"], "customer accounts", "2026-09-28", "2014-01-01", "2026-09-27",
         "Full history of saved addresses. changed_at is UTC."),
        (F["flags"], "feature flag service", "2026-09-28", "", "", "One flag."),
        (F["cards"], "payments vault", "2026-09-28", "", "", "Snapshot at extract, is_default as at extract."),
        (F["card_changes"], "payments vault", "2026-09-28", "2026-07-27", "2026-09-27",
         "Change history over the window; previous_default_card_id is filled on set_default events."),
        (F["auth"], "Tagus Payments", "2026-09-28", "2026-08-31", "2026-09-27",
         "Card payments only. attempt_ref is one payment attempt."),
        (F["psp"], "Tagus Payments", "2026-09-29", "2026-08-31", "2026-09-27", "Provider's monthly report as issued."),
        (F["finance"], "finance (ERP)", "2026-09-28", "2026-07-27", "2026-09-27",
         "Daily exports concatenated, including the 17 August re-export. One row per shipment; order_total_eur "
         "repeats the order total on each shipment row of the order, and the latest export of the order is the one "
         "of record. Amounts are net of VAT on rows exported from the 10 August 2026 finance release and include "
         "VAT at 23% on rows exported before it."),
        (F["catalogue"], "catalogue service", "2026-09-28", "", "", "Status changes for SKUs on sale in 2026."),
        (F["dashboard"], "trading dashboard", "2026-09-28", "2026-07-27", "2026-09-27", "As distributed."),
        (F["shortlist"], "product", "2026-09-28", "", "", ""),
        (F["agreement"], "partnerships", "2026-07-16", "", "", "Extract of the signed agreement."),
        (F["closeout_margens"], "growth", "2025-06-24", "2025-03-31", "2025-06-08", "Close-out as filed."),
        (F["closeout_kaiju"], "growth", "2025-12-16", "2025-10-06", "2025-11-30", "Close-out as filed."),
        (F["release_log"], "checkout squad", "2026-09-01", "2026-01-26", "2026-09-01", "Releases logged to 1 September."),
        (F["field_reference"], "analytics engineering", "2026-09-28", "", "", ""),
        (F["thread"], "team chat", "2026-09-30", "2026-09-28", "2026-09-30", "Channel export."),
        (F["carrier"], "Lusolog Expresso", "2026-07-15", "", "", "Carrier notice as received."),
        (F["stock"], "warehouse management", "2026-09-25", "2026-09-25", "2026-09-25", "Snapshot, 06:00."),
    ]
    return pd.DataFrame([r + (sizes.get(r[0]),) for r in reg],
                        columns=["file", "source_system", "extracted_on", "covers_from", "covers_to", "notes", "rows"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--record")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    tgt = os.path.join(out, "target")
    if os.path.isdir(tgt):
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    T = W.build_truth()
    K, tlog = U.tune(T)
    pk = A.assemble(T, K)
    s = N.enrich(pk)
    rng = np.random.default_rng(P.SEED + 1000)
    p = lambda k: os.path.join(tgt, F[k])
    # data files
    WR.write_parquet(pk["sessions"], p("sessions"))
    for k in ("edge", "tokens_aug", "tokens_sep", "profiles", "promo", "address", "cards", "card_changes", "auth",
              "finance", "catalogue"):
        WR.write_csv(pk[k], p(k))
    with open(p("flags"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(pk["flags"], f, indent=1, ensure_ascii=False)
        f.write("\n")
    # calibration
    crng = np.random.default_rng(P.SEED + 7)
    cos = {k: C.closeout_records(crng, k) for k in C.CLOSEOUTS}
    books = {k: C.closeout_bookings(v) for k, v in cos.items()}
    rels = {k: C.release_records(crng, k) for k in C.RELEASES}
    effs = {k: C.release_effects(v) for k, v in rels.items()}
    D.write_closeout(p("closeout_margens"), "margens", C.CLOSEOUTS["margens"], cos["margens"], books["margens"])
    D.write_closeout(p("closeout_kaiju"), "kaiju", C.CLOSEOUTS["kaiju"], cos["kaiju"], books["kaiju"])
    D.write_release_log(p("release_log"), rels, effs)
    # documents
    # the dashboard as published each Monday, before that week's edge verdicts were applied
    wk, bs, st = dashboard_figures(N.enrich(pk, N.opts(keep_bots=True)))
    D.write_dashboard(p("dashboard"), wk, bs, st)
    D.write_psp_report(p("psp"), psp_weekly(pk["auth"]))
    D.write_shortlist(p("shortlist"))
    D.write_agreement(p("agreement"))
    D.write_carrier_notice(p("carrier"))
    D.write_text(p("field_reference"), D.FIELD_REFERENCE)
    D.write_text(p("thread"), D.THREAD)
    stock = stock_table(rng, T["cat"])
    WR.write_csv(stock, p("stock"))
    sizes = {F[k]: len(pk[k]) for k in ("sessions", "edge", "tokens_aug", "tokens_sep", "profiles", "promo", "address",
                                        "cards", "card_changes", "auth", "finance", "catalogue")}
    sizes[F["stock"]] = len(stock)
    WR.write_csv(register_rows(sizes), p("register"))
    # metadata
    meta = metadata(tgt, sizes)
    with open(os.path.join(out, "metadata.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
        f.write("\n")
    import checks
    ctx = dict(T=T, K=K, pk=pk, s=s, out=out, tgt=tgt, F=F, cos=cos, books=books, rels=rels, effs=effs,
               dash=(wk, bs, st), meta=meta, tlog=tlog, distractors=[F[k] for k in DISTRACTORS])
    rec = checks.run(ctx)
    WR.set_mtime(tgt, EXPORT_TIME)
    print(f"built {len(os.listdir(tgt))} files, {rec['assertions']} assertions passed")
    if a.record:
        with open(a.record, "w") as f:
            json.dump(rec, f, indent=1, default=float)


def metadata(tgt, sizes):
    files = []
    for name in sorted(os.listdir(tgt)):
        fp = os.path.join(tgt, name)
        files.append({"path": name, "format": name.rsplit(".", 1)[1], "bytes": os.path.getsize(fp),
                      "rows": sizes.get(name),
                      "source": "Constructed for this task: fictional store Ventania Merch and club CD Monteralto; "
                                "no third-party data",
                      "date": EXPORT_TIME.date().isoformat(), "license": "CC0-1.0 (original work)"})
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task121",
        "domain": "Product Analytics",
        "subdomain": "onboarding-activation",
        "objective": "Root-Cause Analysis",
        "as_of": "2026-09-28",
        "deliverables": ["q4_sprint_call.html", "checkout_fall_workings.xlsx"],
        "distractor_files": [F[k] for k in DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file_rows": big["rows"], "largest_file": big["path"]},
        "files": files,
    }


if __name__ == "__main__":
    main()
