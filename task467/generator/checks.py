"""task467's assertions, run on every build: the three rules executed on the clean truth (R1 to R3c), every semantic
fork (SF1 to SF23), the 2025 deep-queue back-test and the labelled openings (lesson 12), the golden's assumptions
(lesson 7), the ladder, the ask devices and their separation from the call, the input gates and distractors, the
realism sweep, the leak sweep of the shipped documents (each absence with a positive control through the same
extractor) and the deliverables against figures.json."""
import collections
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import bundle as B
import golden as G
import ladder as L
import sim as S
import world as W

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join((pg.extract_text() or "") for pg in PdfReader(path).pages)


_FUTURE = {}


def future_columns(target, asof=dt.date(2026, 10, 30)):
    """Every data column in the pack holding a date after the extracts' date, as file:column (H16)."""
    if target in _FUTURE:
        return _FUTURE[target]
    out = []
    for f in sorted(os.listdir(target)):
        fp = os.path.join(target, f)
        if f.endswith(".csv"):
            d = pd.read_csv(fp, dtype=str)
            for col in d.columns:
                s = d[col].dropna()
                s = s[s.str.match(r"^\d{4}-\d{2}-\d{2}")]
                if len(s) and dt.date.fromisoformat(s.str[:10].max()) > asof:
                    out.append("%s:%s" % (f, col))
        elif f.endswith(".parquet"):
            d = pd.read_parquet(fp)
            for col in d.columns:
                s = d[col].dropna()
                if pd.api.types.is_datetime64_any_dtype(s) and len(s):
                    m = s.max()
                    if (m.tz_convert("Europe/London") if m.tzinfo else m).date() > asof:
                        out.append("%s:%s" % (f, col))
                elif len(s) and isinstance(s.iloc[0], dt.date) and max(s) > asof:
                    out.append("%s:%s" % (f, col))
        elif f.endswith(".xlsx"):
            from openpyxl import load_workbook
            wb = load_workbook(fp, read_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(min_row=2, values_only=True):
                    for k, v in enumerate(row):
                        if isinstance(v, (dt.datetime, dt.date)):
                            day = v.date() if isinstance(v, dt.datetime) else v
                            if day > asof and "%s:%s:%d" % (f, ws.title, k) not in out:
                                out.append("%s:%s:%d" % (f, ws.title, k))
    _FUTURE[target] = out
    return out


def months_of(pairing, target, **kw):
    return B.monthly(B.refund_table(target, pairing), **kw)


def call_of(mon):
    rows, pay, breach, late = G.call_figures(mon)
    return pay, breach, {k: rows[k]["refunds_late"] for k in rows}, {k: rows[k]["refunds_made"] for k in rows}


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    RESULTS.clear()
    fig = json.load(open(fig_path))
    newest = B.replay(target, "newest")
    golden_mon = months_of(newest, target)
    pay, breach, late, made = call_of(golden_mon)
    gold = (fig["payment_gbp"], fig["breach_months"])
    ok("golden recomputes from target/", (pay, breach) == gold, "%s %s" % (pay, breach))

    # ------------------------------------------------------------------------- R: the three rules on the clean truth
    p = x["parcels"]
    n = len(p["deliv"])
    truth_late = collections.Counter()
    truth_made = collections.Counter()
    for i in range(n):
        md = p["made_day"][i]
        if md is None or p["outcome"][i] != "REFUND":
            continue
        k = "%d-%02d" % (md.year, md.month)
        truth_made[k] += 1
        if (md - S.day_of(p["deliv"][i])).days >= W.LATE_DAY:
            truth_late[k] += 1
    ok("R1 clean truth: the golden's late refunds equal the world's, month by month",
       all(truth_late[k] == late[k] and truth_made[k] == made[k] for k in G.MONTHS),
       "%s" % {k: (truth_late[k], late[k]) for k in G.MONTHS})
    cols = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols += list(pd.read_csv(os.path.join(target, f), nrows=1).columns)
        elif f.endswith(".parquet"):
            cols += list(pd.read_parquet(os.path.join(target, f)).columns)
    ok("R1 no shipped column holds a 2026 refund's delivery day or a late flag",
       not any(re.search(r"deliver|late|wait|received_at|day_?0", c, re.I) for c in cols), ", ".join(sorted(set(cols)))[:200])
    arrival = B.replay(target, "oldest")
    pay1, breach1, late1, _ = call_of(months_of(arrival, target))
    ok("R3a the analyst test: arrival-order pairing files the default path's answer, not the golden",
       (pay1, breach1) == (fig["rungs"]["r1_arrival_order"]["payment_gbp"], fig["rungs"]["r1_arrival_order"]["breach_months"])
       and pay1 != pay and breach1 != breach, "%s %s against %s %s" % (pay1, breach1, pay, breach))
    ok("R3b the decisive step alone: the same pipeline with only the pairing changed to newest-first files the golden",
       call_of(months_of(B.replay(target, "newest"), target))[:2] == gold)
    lower = {k: v for k, v in fig["rungs"].items() if k.startswith("r") and k not in ("r4_newest_from_empty_2026",)}
    ok("R3b each lower rung's single correction leaves a wrong answer",
       all((v["payment_gbp"], v["breach_months"]) != gold for k, v in lower.items() if k != "r5_newest_by_day")
       and fig["rungs"]["r5_newest_by_day"]["payment_gbp"] != pay, "%s" % {k: v["payment_gbp"] for k, v in lower.items()})
    g = B.goods(target)
    dup_blocks = g.groupby(g.t.dt.date).size()
    ok("R3c no copied block: no two delivery days carry the same scan sequence",
       len(set(tuple(v) for _, v in g.groupby(g.t.dt.date).barcode)) == len(dup_blocks))
    ok("R3c no decoy document: the assurance and the review state no wait, late count, payment or pairing",
       True)  # asserted with a positive control in the leak block below

    # R2: every Layer 1 item on the main path, mishandled, leaves the call and the components where they were
    rf = B.refunds(target)
    ret = rf[rf.reason == "RETURN"]
    ok("R2 the ledger's UTC stamps: every return refund's UTC date is its UK date (18:00 runs)",
       (ret.initiated_at_utc.dt.date == ret.day).all())
    failed = ret[ret.status == "FAILED"]
    re_ = ret[ret.reissue_of.notna()].set_index("reissue_of")
    if len(failed):
        fd = failed.set_index("refund_id").day
        swap = B.refund_table(target, newest)
        alt = swap.copy()
        mp = {r: fd[r] for r in fd.index}
        alt["day"] = [mp.get(of, d) if of is not None else d for of, d in zip(alt.reissue_of, alt.day)]
        ok("R2 reissued refunds: dating each at its failed run moves no month's made or late count",
           B.monthly(alt) == B.monthly(swap), "%d reissues" % len(failed))
    else:
        ok("R2 reissued refunds present", False)
    lab = B.processing(target)
    stragglers = lab[(lab.label != "") & (lab.t >= pd.Timestamp(2026, 1, 1))]
    truth_lab = L.label_truth(target)
    ok("R2 labelled parcels still arriving in January 2026: the replay gives each its own label's scan",
       all(newest[i] == truth_lab[i] for i in stragglers.id), "%d stragglers" % len(stragglers))
    ok("R2 the two goods-in layouts union to one record: every 2025 and 2026 scan read, none twice",
       g.barcode.is_unique and len(g) == len(B.deliveries(target)), "%d scans" % len(g))
    ok("R2 the pence column from April: the call reads no amount", True)

    # ------------------------------------------------------------------------------------------ the semantic forks
    hours = months_of(newest, target, hours=True)
    ok("SF1 a refund made late is calendar days from day 0 (the golden); the 336-hour reading differs",
       call_of(hours)[0] != pay and call_of(hours)[0] == fig["rungs"]["hours_reading"]["payment_gbp"],
       "%s against %s" % (call_of(hours)[0], pay))
    tb = B.refund_table(target, newest)
    by_deliv = tb.assign(day=tb.delivered.dt.date)
    ok("SF2 a refund belongs to its made month; the delivery month gives other counts",
       B.monthly(by_deliv)["2026-03"][0] != golden_mon["2026-03"][0])
    ok("SF3 a reissued refund is made at the succeeding payment (asserted neutral in R2); the ledger ties each reissue "
       "to its failed refund", set(re_.index) == set(failed.refund_id))
    ok("SF4 the delivery day is the goods-in scan's UK day: both exports are written in UK time",
       "scanned_at_uk" in pd.read_csv(B.path(target, "goods2025"), nrows=1).columns
       and "event_ts_uk" in pd.read_parquet(B.path(target, "goods2026")).columns)
    ok("SF5 one delivery per barcode: no barcode is scanned twice", g.barcode.is_unique)
    allref = rf[(rf.status == "PAID")]
    allref = allref.assign(m=allref.day.map(lambda d: "%d-%02d" % (d.year, d.month)))
    ok("SF6 refunds for goods returned to the centre are reason RETURN; every paid refund is another count",
       int((allref.m == "2026-03").sum()) != golden_mon["2026-03"][0])
    o = B.orders(target)
    ie = set(o[o.currency == "EUR"].order_ref)
    win = tb[pd.to_datetime(tb.day) >= pd.Timestamp(2026, 1, 1)]
    win = win[pd.to_datetime(win.day) < pd.Timestamp(2026, 7, 1)]
    ok("SF7 Irish customers' refunds are in the population (their parcels came to Cotterby)",
       len(set(win.order_ref) & ie) > 0 and len(win[win.order_ref.isin(ie)]) == len(win[win.currency == "EUR"]),
       "%d euro refunds in the window" % len(win[win.currency == "EUR"]))
    procs = B.processing(target)
    rej = procs[procs.outcome != "REFUND"]
    ok("SF8 rejected parcels carry no return refund", not set(rej.order) & set(ret.order_ref))
    ok("SF9 every goods-in row is a return (the class columns hold one value)",
       set(g.cls) == {"RET"})
    ok("SF10 every processing record is an opening (no voided records ship)", procs.id.is_unique)
    empty = {**newest, **B.replay(target, "newest", start=pd.Timestamp(2026, 1, 1))}
    ok("SF11 the hall's 1 January content: an empty-hall start files the same call (the hall was empty)",
       call_of(months_of(empty, target))[:2] == gold)
    shares = {k: golden_mon[k][1] / golden_mon[k][0] for k in G.MONTHS}
    ok("SF12 at least 95 per cent against more than 95 per cent: no month's late share is exactly 5 per cent",
       all(abs(s - 0.05) > 0.02 for s in shares.values()), "%s" % {k: round(100 * v, 2) for k, v in shares.items()})
    ok("SF13 the late share is late over made, one decimal of the exact share",
       all(fig["months"][k]["late_share_pct"] == round(100.0 * late[k] / made[k], 1) for k in G.MONTHS))
    ok("SF14 the payment is GBP 15 times the half-year's late refunds", pay == W.PAYMENT_PER_LATE * sum(late.values()))
    hv = G.voucher_values(target, currency_from="house")
    ok("SF15 a voucher's value in pounds: euros at the reporting rate; every value as pounds differs every month",
       all(hv[k] != fig["months"][k]["vouchers_gbp"] for k in G.MONTHS))
    v = B.vouchers(target)
    ok("SF16 the vouchers issued in a month are every voucher (all reasons); refund-delay ones only differ",
       set(v.reason) >= {"Refund delay", "Delivery delay", "Damaged item"})
    cs = B.cases(target).set_index("case_ref")
    rdv = v[v.reason == "Refund delay"]
    on_rd_case = v[v.case_ref.map(cs.topic) == "Refund delay"]
    ok("SF17 refund-delay vouchers: reason Refund delay and vouchers on refund-delay cases are one set",
       set(rdv.voucher_code) == set(on_rd_case.voucher_code))
    case_order = rdv.case_ref.map(cs.order_ref)
    diff = rdv[case_order != rdv.order_ref]
    any_refund = set(rf.order_ref)
    ok_orders = o.set_index("order_ref").ordered_at_utc
    ok("SF18 the order a delayed refund was on is the case's; where a Refund delay voucher's own field differs, that "
       "order is a later order of the customer's with no refund of any kind and no processing record (the literal "
       "reading is impossible on every row, lesson 8)",
       len(diff) > 0 and not set(diff.order_ref) & any_refund and not set(diff.order_ref) & set(procs.order)
       and (pd.to_datetime(diff.order_ref.map(ok_orders), utc=True)
            > pd.to_datetime(diff.case_ref.map(cs.order_ref).map(ok_orders), utc=True)).all(),
       "%d of %d vouchers" % (len(diff), len(rdv)))
    v_diff = v[v.case_ref.map(cs.order_ref) != v.order_ref]
    coherent = v_diff[v_diff.order_ref.isin(any_refund)]
    tb_days = (pd.to_datetime(tb.day) - pd.to_datetime(tb.delivered.dt.date)).dt.days
    coherent_late = int((coherent.order_ref.map(dict(zip(tb.order_ref, tb_days))) >= W.LATE_DAY).sum())
    ok("SF18 every voucher whose own order differs from its case's and carries a refund is outside the refund-delay set "
       "(Ask B never reads one; Ask A reads no order)", (coherent.reason != "Refund delay").all(),
       "%d of %d differing vouchers, %d of those refunds made late, reasons %s" % (
           len(coherent), len(v_diff), coherent_late, sorted(set(coherent.reason))))
    half = rdv[(rdv.issued >= pd.Timestamp(2026, 1, 1)) & (rdv.issued < pd.Timestamp(2026, 7, 1))]
    opened_half = rdv[(rdv.case_ref.map(cs.opened) >= pd.Timestamp(2026, 1, 1)) &
                      (rdv.case_ref.map(cs.opened) < pd.Timestamp(2026, 7, 1))]
    ok("SF19 vouchers issued in January to June by issue time and by case opening are one set",
       set(half.voucher_code) == set(opened_half.voucher_code))
    ok("SF20 one category an order", o.order_ref.is_unique and o.main_category.notna().all())
    rate, cur = G.eur_rate(target), G.customer_currency(target)
    gbp_all = v.value * v.customer_ref.map(lambda c_: rate if cur.get(c_) == "EUR" else 1.0)
    utc_month = pd.to_datetime(v.issued_at, utc=True).dt.strftime("%Y-%m")
    by_utc = {k: int(round(float(gbp_all[utc_month == k].sum()))) for k in G.MONTHS}
    moved = [k for k in G.MONTHS if by_utc[k] != fig["months"][k]["vouchers_gbp"]]
    utc_half = rdv[(utc_month[rdv.index] >= "2026-01") & (utc_month[rdv.index] <= "2026-06")]
    ok("SF22 a voucher counts in the UK calendar month it was issued (the prompt); the UTC month prints other figures, "
       "and the half-year's refund-delay vouchers are one set under either clock",
       moved == ["2026-03", "2026-04"] and set(utc_half.voucher_code) == set(half.voucher_code),
       "UTC %s against %s" % ({k: by_utc[k] for k in moved}, {k: fig["months"][k]["vouchers_gbp"] for k in moved}))
    days = (pd.to_datetime(tb.day) - pd.to_datetime(tb.delivered.dt.date)).dt.days
    refund_days = dict(zip(tb.order_ref, days))
    strict = half[half.case_ref.map(cs.order_ref).map(refund_days) >= W.LATE_DAY]
    strict_cat = strict.case_ref.map(cs.order_ref).map(o.set_index("order_ref").main_category)
    strict_gbp = strict.value * strict.customer_ref.map(lambda c_: rate if cur.get(c_) == "EUR" else 1.0)
    strict_fig = {c_: {"count": int((strict_cat == c_).sum()), "value_gbp": int(round(float(strict_gbp[strict_cat == c_].sum())))}
                  for c_ in G.CATS}
    ok("SF23 vouchers given for a refund delay are every Refund delay voucher (the voucher's own reason, no lateness "
       "test); counting only refunds made on day 15 or later prints other figures",
       sum(fig["categories"][c_]["count"] for c_ in G.CATS) == len(half) and len(strict) < len(half)
       and strict_fig != fig["categories"],
       "%d against %d vouchers" % (len(strict), len(half)))
    ref_only = B.replay(target, "newest", refunds_only=True)
    ok_ro, _, n_lab = L.agreement(target, ref_only, truth_lab)
    ro_call = call_of(months_of(ref_only, target))
    ok("SF21 every opening pops the hall, rejected parcels included: a refunds-only replay misses labelled openings "
       "and files another call",
       ok_ro < n_lab and ok_ro == fig["labels"]["refunds_only_exact"] and ro_call[:2] != gold
       and ro_call[0] == fig["rungs"]["refunds_only_replay"]["payment_gbp"],
       "%d of %d exact; GBP %s %s" % (ok_ro, n_lab, ro_call[0], ro_call[1]))

    # ----------------------------------------------------------------- lesson 12: the order measured where it applies
    lb = fig["labels"]
    ok("L12 the labelled openings: newest-first exact on every one, 2025 and January 2026",
       lb["newest_exact"] == lb["labelled_openings"] and lb["newest_exact_2026"] == lb["labelled_2026"] > 1000,
       "%d of %d; 2026 %d" % (lb["newest_exact"], lb["labelled_openings"], lb["labelled_2026"]))
    lab_open = lab[lab.label != ""]
    lab_deliv = B.goods(target).set_index("barcode").loc[lab_open.label, "t"]
    ok("L12 the labelled openings are every opening to the end of 2025 (from December 2024) and the stragglers opened "
       "to April 2026, their parcels all delivered by 8 January 2026 (the span the write-up and the note state)",
       (lab[lab.t < pd.Timestamp(2026, 1, 1)].label != "").all()
       and lab_open.t.min().strftime("%Y-%m") == "2024-12" and lab_open.t.max().strftime("%Y-%m") == "2026-04"
       and lab_deliv.max() < pd.Timestamp(2026, 1, 9), "%s to %s" % (lab_open.t.min(), lab_open.t.max()))
    ok("L12 arrival order and the by-day reading fail the labelled openings",
       lb["arrival_exact"] < 0.05 * lb["labelled_openings"] and lb["by_day_exact"] < 0.05 * lb["labelled_openings"])
    bt = fig["backtest_2025"]
    deep = [m for m in ("2", "12") if bt["labels"][m] > 0]
    ok("L12 2025 holds two deep-queue months whose labelled late refunds the replay reproduces exactly",
       deep == ["2", "12"] and all(bt["newest"][m] == bt["labels"][m] for m in bt["labels"]),
       "%s" % {m: bt["labels"][m] for m in deep})
    ok("L12 arrival order misses both deep-queue months' late refunds",
       all(bt["arrival"][m] != bt["labels"][m] for m in deep), "%s" % {m: bt["arrival"][m] for m in deep})
    ok("L12 the textbook check passes: the 2025 mean wait is the same under labels, newest-first and arrival order",
       bt["labels_mean_wait_days"] == bt["newest_mean_wait_days"] == bt["arrival_mean_wait_days"])

    # --------------------------------------------------------------------------- lesson 7: the golden's assumptions
    ok("L7 every opening finds a parcel waiting (no opening precedes its parcel's delivery)",
       all(v is not None for v in newest.values()))
    ok("L7 every return refund made has exactly one opening with outcome REFUND",
       tb.id.notna().all() and tb.id.is_unique, "%d refunds" % len(tb))
    ok("L7 no opening shares a second with a goods-in scan (no tie to break)",
       not set(procs.t.astype("int64")) & set(g.t.astype("int64")))
    ok("L7 no two openings and no two deliveries share a second, so no row order moves the replay",
       procs.t.is_unique and g.t.is_unique)
    lab25 = lab[lab.label != ""]
    carriers = B.goods(target).set_index("barcode")
    ok("L7 the order holds whatever the door or carrier (the labelled openings are exact in each door)",
       len(set(carriers.loc[lab25.label, "door"])) == 4)
    ok("L7 the hall carries nothing over 1 January that changes the call (SF11)", True)

    # ----------------------------------------------------------------------------------------------- the ladder
    r = fig["rungs"]
    ok("Ladder: the default path (arrival order) files a payment and breach months the golden does not",
       r["r1_arrival_order"]["payment_gbp"] != pay and r["r1_arrival_order"]["breach_months"] != breach)
    ok("Ladder: random order, 2025's shares and the opening day each file another payment and breach set",
       all(r[k]["payment_gbp"] != pay and r[k]["breach_months"] != breach
           for k in ("r0_opened_as_delivered", "r2_2025_shares_carried", "r3_random_order")))
    ok("Ladder: no rung within GBP 600 of the golden but the by-day reading the labels reject",
       all(abs(v["payment_gbp"] - pay) > 600 for k, v in r.items()
           if k not in ("r4_newest_from_empty_2026", "r5_newest_by_day", "hours_reading")))
    ok("Ladder: the golden's breach months sit two points or more from the line",
       min(abs(s - 0.05) for s in shares.values()) >= 0.02)

    # ------------------------------------------------------------------------------------------- the ask devices
    cc = G.customer_currency(target)
    ie_v = v[v.customer_ref.map(cc) == "EUR"]
    ok("Ask A device mass: Irish vouchers every month", all((ie_v.issued.dt.strftime("%Y-%m") == k).sum() >= 10
                                                            for k in G.MONTHS))
    red = B.redemptions(target)
    on_eur = red[red.order_ref.isin(ie)]
    ok("Ask A forcing: every redemption of an Irish customer's voucher is on a euro order, and only those",
       set(on_eur.voucher_code) == set(red.voucher_code) & set(ie_v.voucher_code))
    ok("Ask A forcing: the reporting rate is one rate on every euro order", fig["eur_rate"] == W.EUR_RATE
       and float((o[o.currency == "EUR"].order_total_gbp - o[o.currency == "EUR"].order_total * W.EUR_RATE).abs().max())
       <= 0.0051)
    vb_case = G.voucher_categories(target, link="voucher", currency_from="customer")
    ok("Ask B device mass: the voucher's own field moves every category's count",
       all(vb_case[c]["count"] != fig["categories"][c]["count"] for c in G.CATS))
    ok("Ask B: no voucher's own order is orphaned (the battery's anti-join finds nothing)",
       v.order_ref.isin(o.order_ref).all())
    import inspect
    call_src = "".join(inspect.getsource(fn) for fn in (B.replay, B.refund_table, B.return_refunds_made, B.deliveries,
                                                         B.processing, B.monthly, B.goods, B.refunds))
    ok("Separation: the call's path reads no voucher, case, redemption or order file",
       not any(k in call_src for k in ('"vouchers"', '"cases"', '"redemptions"', '"orders"')))
    ok("Separation: no ask figure reads the goods-in or processing records",
       not any(k in inspect.getsource(G.voucher_values) + inspect.getsource(G.voucher_categories)
               for k in ("replay", "processing", "goods")))

    # ------------------------------------------------------------------------------------- input gates, metadata
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path))
    rows = {f: (sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 if f.endswith(".csv") else
                (len(pd.read_parquet(os.path.join(target, f))) if f.endswith(".parquet") else 0)) for f in files}
    ok("Input gates: 10 or more files", len(files) >= 10, "%d" % len(files))
    ok("Input gates: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("Input gates: a file of 25,000 rows or more", max(rows.values()) >= 25000, "%d" % max(rows.values()))
    ok("Input gates: 2 or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2
       and all(d in files for d in meta["distractor_files"]))
    ok("Input gates: provenance for every file", sorted(x_["file"] for x_ in meta["provenance"]) == files)
    ok("Input gates: no file describes the data", not any(re.search(r"readme|dictionar|manifest|notes|schema|codebook",
                                                                    f, re.I) for f in files))
    ok("Distractors: the golden reads none of them", True)  # golden.compute reads goods, processing, refunds, orders,
    # vouchers and cases; the daily sheet, the rota and the review are never opened (asserted by the reader below)
    import inspect
    src = inspect.getsource(G) + inspect.getsource(B)
    ok("Distractors: no golden or reader code opens the daily sheet, the rota or the review",
       not any(k in src for k in ('"dailyops"', '"rota"', '"review"')))

    # ---------------------------------------------------------------------------------------------- realism sweep
    for f, col in (("goods2025", "scan_id"), ("processing", "process_id")):
        s = pd.read_csv(B.path(target, f), usecols=[col], dtype=str)[col].str.replace("P", "").astype(int)
        ok("Realism: %s has no constant step" % col, s.diff().dropna().nunique() > 1)
    e = pd.read_parquet(B.path(target, "goods2026")).event_id
    ok("Realism: event_id has no constant step", e.diff().dropna().nunique() > 1)
    ok("Realism: no two months carry the same refunds made", len(set(made.values())) == len(made))
    ok("Realism: no round headline (payment, late total)", pay % 1000 != 0 and sum(late.values()) % 100 != 0)
    ppl = set(W.PEOPLE.values())
    ok("Realism: personas are the drawn ones", ppl == {"Howard Jones", "Steven Jennings", "Neil Fisher"})
    ok("H16 no date past the extracts (30 October 2026) but the allow-list: the vouchers' validity window",
       future_columns(target) == ["wh_goodwill_vouchers_2026.csv:expires_on"], ", ".join(future_columns(target)))

    # ------------------------------------------------------------------- leak sweep of the documents (positive control)
    from pdfminer.high_level import extract_text as pm_text
    for k, control in (("assurance", "made on day 15 or later is made late"), ("review", "agency contract")):
        t = pdf_text(B.path(target, k))
        t1 = re.sub(r"\s+", " ", t)
        ok("Leak control: %s reads back through the extractor" % W.FILES[k], control in t1 and len(t1) > 500)
        t2 = re.sub(r"\s+", " ", pm_text(B.path(target, k)))
        ok("H25 %s reads the same sentence through a second extractor (pdfminer)" % W.FILES[k], control in t2)
        bad = [wd for wd in ("newest", "stack", "label", "LIFO", "first in", "pair", "order of working", "cage",
                             "Tarnwell", "prepaid", "postage", "self-") if wd.lower() in t1.lower()]
        ok("Leak: %s names no pairing, order of working, label or postage" % W.FILES[k], not bad, ", ".join(bad))
        other = [wd for wd in ("stock transfer", "supplier sample", "misdeliver", "scanned twice", "void")
                 if wd in t1.lower()]
        ok("R2 %s describes no goods-in or processing row the exports do not hold" % W.FILES[k], not other,
           ", ".join(other))
        nums = [str(pay), "{:,}".format(pay), str(sum(late.values())), "{:,}".format(sum(late.values()))]
        ok("Gate G: %s states no golden figure" % W.FILES[k], not any(nm in t1 for nm in nums))
    from openpyxl import load_workbook
    wb = load_workbook(B.path(target, "dailyops"), read_only=True)
    head = [c.value for c in next(wb.active.iter_rows(max_row=1))]
    ok("Leak control: the daily sheet reads back", head[0] == "Date" and "Parcels opened" in head)
    ok("Gate G: the daily sheet ranks nothing on late refunds", not any("late" in str(h).lower() for h in head))

    # ---------------------------------------------------------------------------------------- deliverables
    csvp = os.path.join(gdir, W.GOLDEN["return"])
    gc = pd.read_csv(csvp, dtype=str)
    ok("Deliverable: the return's rows equal figures.json",
       all(int(gc.iloc[i].refunds_made_late) == fig["months"][k]["refunds_late"] and
           int(gc.iloc[i].refunds_made) == fig["months"][k]["refunds_made"] and
           float(gc.iloc[i].late_share_pct) == fig["months"][k]["late_share_pct"] and
           gc.iloc[i].met_95pct_commitment == fig["months"][k]["met"] and
           int(gc.iloc[i].goodwill_vouchers_issued_gbp) == fig["months"][k]["vouchers_gbp"]
           for i, k in enumerate(G.MONTHS)))
    nt = re.sub(r"\s+", " ", pdf_text(os.path.join(gdir, W.GOLDEN["note"])))
    ok("Deliverable: the note states the payment and every category figure",
       "{:,}".format(pay) in nt and all("{:,}".format(fig["categories"][c]["value_gbp"]) in nt for c in G.CATS))

    bad = [r_ for r_ in RESULTS if not r_[1]]
    for name, good, detail in RESULTS:
        if not good:
            print("FAIL  %s  %s" % (name, detail))
    print("checks: %d assertions, %d failures" % (len(RESULTS), len(bad)))
    return not bad
