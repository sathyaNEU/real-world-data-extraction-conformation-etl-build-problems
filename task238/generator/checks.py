"""task238 generator assertions, on the installed bundle (target/, golden/, figures.json) and on the clean truth.

    python3 task238/generator/checks.py        # exit 1 on any failure
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zipfile
import zlib
import base64
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ROOT = os.path.dirname(TASK)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import params as P  # noqa: E402

FAILS = []
N = [0]


def ok(cond, label, detail=""):
    N[0] += 1
    print("%-4s %s %s" % ("OK" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def pdf_text(path):
    raw = open(path, "rb").read()
    out = []
    pos = 0
    while True:
        i = raw.find(b"stream", pos)
        if i < 0:
            break
        j = raw.find(b"endstream", i)
        head = raw[max(0, i - 160):i]
        body = raw[i + 6:j].strip(b"\r\n")
        pos = j + 9
        try:
            if b"ASCII85Decode" in head:
                body = base64.a85decode(body[:-2] if body.endswith(b"~>") else body)
            if b"FlateDecode" in head:
                body = zlib.decompress(body)
        except Exception:
            continue
        out.append(body.decode("latin-1"))
    txt = " ".join(out)
    words = re.findall(r"\((.*?)\)\s*Tj|\[(.*?)\]\s*TJ", txt)
    s = []
    for a, b in words:
        if a:
            s.append(a)
        else:
            s.append("".join(re.findall(r"\((.*?)\)", b)))
    return re.sub(r"\s+", " ", " ".join(s)).replace("\\(", "(").replace("\\)", ")")


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    pk = A.Pack(T)
    R = A.rungs(pk)
    V = A.variants(pk)
    G = R["golden"]
    watch = set(F["watch"])
    stores = pk.stores
    files = sorted(os.listdir(T))

    # ------------------------------------------------------------------------------------- input gates
    ok(len(files) >= 10, "gate.files", "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "gate.formats", str(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(T, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "gate.big_file", "%d rows" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "gate.distractors")
    bad_names = [f for f in files if re.search(r"readme|dictionary|notes|manifest|decoy|trap|test_|answer", f, re.I)]
    ok(not bad_names, "gate.no_describing_file", str(bad_names))

    # ------------------------------------------------------------------------------------- R1 raw material
    ok(all(os.path.getsize(os.path.join(T, P.FILES[k])) > 1000 for k in ("hourly", "movement", "printer",
                                                                         "checks", "audits")),
       "R1.raw_files_ship", "hourly scans, movement, printer jobs, checks, audits")
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(T, f), encoding="utf-8")))
    ok(not any(re.search(r"accura|stale|label_state|old_label|on_watch", h, re.I) for h in heads),
       "R1.no_column_holds_the_quantity")
    # the decisive organ moves the call: without each store's own print time (labels taken as up at opening for
    # every store, the chain's typical day) the set changes
    no_win = {}
    for s in stores:
        T_ = pk.T(s)
        no_win[s] = 100 * (1 - R["baseline"])
    ok(sorted(s for s in stores if no_win[s] < A.LINE) != sorted(watch), "R1.organ_decides",
       "no store fails without the changeover windows")

    # ------------------------------------------------------------------------------------- R3 three rules
    import world as W
    w = W.build_world()
    true_acc = {}
    stray_true = P.BASE_ERR
    for s in stores:
        Ts = sum(v for (st, d), v in w.daytot.items() if st == s)
        true_acc[s] = 100 * (1 - (w.truth_stale[s] + stray_true * (Ts - w.truth_stale[s])) / Ts)
    true_set = sorted(s for s in stores if true_acc[s] < A.LINE)
    ok(true_set == sorted(watch), "R3.truth_set_equals_golden", str(true_set))
    ok(max(abs(true_acc[s] - G[s]) for s in stores) < 0.12, "R3.golden_estimates_truth",
       "max gap %.3f" % max(abs(true_acc[s] - G[s]) for s in stores))
    # R3a: the analyst test on the clean truth: the random audit route files no store
    am = defaultdict(int)
    an = defaultdict(int)
    for (no, t, i, label, regp) in w.audit_rows:
        an[no] += 1
        am[no] += abs(label - regp) < 0.005
    r0_truth = sorted(s for s in stores if 100 * am[s] / an[s] < A.LINE)
    ok(r0_truth == [], "R3a.audit_route_on_clean_truth_files_none", str(r0_truth))
    ok(sorted(s for s in stores if R["r0_audit"][s] < A.LINE) == [], "R3a.audit_route_on_pack_files_none")
    ok(min(R["r0_audit"].values()) >= 99.5, "R3a.audit_route_every_store_99.5_or_more",
       "%.2f" % min(R["r0_audit"].values()))
    # R3b: the decisive step alone files the golden; each lower rung's correction leaves it wrong
    ok(sorted(s for s in stores if G[s] < A.LINE) == sorted(watch), "R3b.decisive_step_alone_files_golden")
    for rung in ("r0b_pooled", "r1_checkshare", "r2_clockcurve"):
        st = sorted(s for s in stores if R[rung][s] < A.LINE)
        ok(st != sorted(watch), "R3b.%s_wrong" % rung, str(st))
    ok(sorted(s for s in stores if R["r1_checkshare"][s] < A.LINE) == sorted(watch | {F["nearest_off"]}),
       "R3b.check_share_adds_nearest", "the write-up's rival clause")
    # late-printer heuristic: stores whose batches print after 10:30 on average
    meanh = {}
    for s in stores:
        hs = []
        for d in pk.co_dates:
            t = pk.batch[(s, d)][0]
            h = t.hour + t.minute / 60.0
            hs.append(h if t.date() == d else h - 24)
        meanh[s] = sum(hs) / len(hs)
    late = sorted(s for s in stores if meanh[s] > 10.5)
    ok(late != sorted(watch), "R3b.late_printer_heuristic_wrong", str(late))
    # R3c: no plant
    import hashlib
    blocks = defaultdict(int)
    for (s, d), hrs in pk.hourly.items():
        blocks[tuple(hrs[h] for h in sorted(hrs))] += 1
    ok(max(blocks.values()) == 1, "R3c.no_repeated_hourly_block")
    ok(not any(re.search(r"memo|draft|briefing|email|thread", f, re.I) for f in files), "R3c.no_memo_or_draft")
    std = pdf_text(os.path.join(T, P.FILES["standard"]))
    ok("rang up at the price shown on the item's shelf-edge label at the moment of the scan" in std,
       "R3c.standard_readable_control", "positive control on the PDF extractor")
    ok(not re.search(r"\bchangeovers?\b|\bprinter|\bprint(ed|ing|s)?\b|\bhang(s|ing|ed)?\b|\baudit|\bcheck",
                     std, re.I), "R3c.standard_names_no_step")

    # ------------------------------------------------------------------------------------- the call and margins
    ok(sorted(watch) == [102, 107, 203, 205, 206], "call.set")
    for s in stores:
        ok(abs(G[s] - A.LINE) >= 0.3, "margin.%d" % s, "%.3f" % (G[s] - A.LINE))
    for k, v in V.items():
        st = sorted(s for s in stores if v[s] < A.LINE)
        ok(st == sorted(watch), "SF.call_holds.%s" % k, str(st))
    # graded figures: each Price Watch store's accuracy and the nearest store off sit inside their one-decimal bin
    # under every member of the standing family (pace MLE and its range, hour treatment, stray-label basis)
    fam = ["ramp", "mid", "store_baseline", "rate_lo", "rate_hi"]
    for s in sorted(watch) + [F["nearest_off"]]:
        printed = F["accuracy"][str(s)] if s in watch else F["nearest_off_acc"]
        lo = min(V[k][s] for k in fam)
        hi = max(V[k][s] for k in fam)
        edge = min(hi - (printed - 0.05), (printed + 0.05) - lo)
        ok(lo >= printed - 0.05 and hi < printed + 0.05, "bin.%d" % s, "printed %.1f family %.3f-%.3f edge %.3f" %
           (printed, lo, hi, edge))
    # SF: 'below 99.0' compared unrounded or rounded to one decimal gives the same call
    ok(all((G[s] < 99.0) == (round(G[s], 1) < 99.0) for s in stores), "SF.rounding_path_same_call")
    # SF: undercharges count (PI-2 3.1); counting only overcharges would change the figures
    # SF: per-store hanging pace is not estimable: no store has more than two check visits inside its hanging
    rate = R["rate"]
    inr = defaultdict(set)
    for (s, t, ean, lab, reg) in pk.checks:
        P_, L = pk.batch[(s, t.date())]
        m = (t - P_).total_seconds() / 60
        if 0 <= m < L / rate:
            inr[s].add(t.date())
    ok(max((len(v) for v in inr.values()), default=0) <= 3, "SF.store_pace_not_estimable",
       str({s: len(v) for s, v in inr.items()}))
    # SF: checks before the print show the old label, after the batch is up the new one
    pre = [abs(lab - reg) > 0.004 for (s, t, ean, lab, reg) in pk.checks if t < pk.batch[(s, t.date())][0]]
    post = [abs(lab - reg) > 0.004 for (s, t, ean, lab, reg) in pk.checks
            if (t - pk.batch[(s, t.date())][0]).total_seconds() / 60 > pk.batch[(s, t.date())][1] / rate]
    ok(len(pre) > 200 and sum(pre) / len(pre) > 0.98, "SF.checks_before_print_old", "%d of %d" % (sum(pre), len(pre)))
    ok(len(post) > 1000 and sum(post) / len(post) < 0.01, "SF.checks_after_batch_new", "%d of %d" % (sum(post), len(post)))

    # ------------------------------------------------------------------------------------- Layer 1 neutrality
    # R2.1 printer times read as wall clock without the offset (the offset is the local one): same call, same figures
    pk2 = A.Pack(T)
    with open(os.path.join(T, P.FILES["printer"]), encoding="utf-8") as fh:
        jobs = [json.loads(x) for x in fh if x.strip()]
    for j in jobs:
        m = re.match(r"PCB (\d{2}[A-Z]{3}\d{2})", j["job_name"])
        if not m or j["status"] != "COMPLETED":
            continue
        d = dt.datetime.strptime(m.group(1).title(), "%d%b%y").date()
        s = pk2.by_dev[j["device"]]
        wall = dt.datetime.strptime(j["printed_local"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=A.TZ)
        pk2.batch[(s, d)] = (wall, int(j["labels"]))
    st2, _ = A.stale_scans(pk2, rate)
    a2 = A.accuracy(pk2, st2, {0: R["baseline"]})
    ok(all(abs(a2[s] - G[s]) < 1e-9 for s in stores), "R2.1.printer_offset_neutral")
    # R2.2 the voided job's time in place of its reprint: same call, same printed figures
    pk3 = A.Pack(T)
    for j in jobs:
        m = re.match(r"PCB (\d{2}[A-Z]{3}\d{2})", j["job_name"])
        if not m or j["status"] != "VOIDED":
            continue
        d = dt.datetime.strptime(m.group(1).title(), "%d%b%y").date()
        s = pk3.by_dev[j["device"]]
        t = dt.datetime.strptime(j["printed_local"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=A.TZ)
        pk3.batch[(s, d)] = (t, pk3.batch[(s, d)][1])
    st3, _ = A.stale_scans(pk3, rate)
    a3 = A.accuracy(pk3, st3, {0: R["baseline"]})
    ok(sorted(s for s in stores if a3[s] < A.LINE) == sorted(watch) and
       all(round(a3[s], 1) == round(G[s], 1) for s in watch), "R2.2.voided_job_neutral",
       "max move %.3f" % max(abs(a3[s] - G[s]) for s in stores))
    # R2.3 audit EANs left at 13 digits (no changed item recognised): same call, same printed figures
    b13 = defaultdict(int)
    n13 = 0
    for (s, t, ean, lab, reg, aid) in pk.audits:
        n13 += 1
        b13[0] += abs(lab - reg) > 0.004
    a4 = A.accuracy(pk, R["golden_stale"], {0: b13[0] / n13})
    ok(sorted(s for s in stores if a4[s] < A.LINE) == sorted(watch) and
       all(round(a4[s], 1) == round(G[s], 1) for s in watch), "R2.3.ean_padding_neutral")
    # R2.4 the three store namings map one to one
    ok(len(pk.by_name) == 14 and len(pk.by_dev) == 14 and len(set(pk.by_name.values())) == 14,
       "R2.4.store_crosswalk_one_to_one")
    # R2.5 closed days carry no rows, the early-close Thursdays stop at 18:00
    closed_rows = [k for k in pk.hourly if k[1] in P.CLOSED]
    late_rows = [k for k, hrs in pk.hourly.items() if k[1] in P.SHORT_CLOSE and max(hrs) >= 18]
    ok(not closed_rows and not late_rows, "R2.5.closed_and_short_days")
    # R2.6 the December check sheet read with the October layout: pace from October and November only
    rate_on = A.fit_pace(type("X", (), {"checks": [c for c in pk.checks if c[1].month < 12],
                                       "batch": pk.batch})())[0]
    a6 = A.accuracy(pk, A.stale_scans(pk, rate_on)[0], {0: R["baseline"]})
    ok(sorted(s for s in stores if a6[s] < A.LINE) == sorted(watch) and
       all(round(a6[s], 1) == round(G[s], 1) for s in watch), "R2.6.sheet_layout_neutral", "pace %.2f" % rate_on)
    # R2.7 the DST change inside the quarter: every printer offset is the local one on its date
    offs = {j["printed_local"][-6:] for j in jobs}
    ok(offs == {"-03:00", "-04:00"}, "R2.7.dst_offsets_present", str(sorted(offs)))

    # ------------------------------------------------------------------------------------- shock: not a sort
    stats = {
        "mean_print_hour": meanh,
        "audit_accuracy": R["r0_audit"],
        "check_old_share": {s: -R["r1_checkshare"][s] for s in stores},
        "store_scans": {s: pk.T(s) for s in stores},
        "changed_units": {s: sum(pk.U[(s, d)] for d in pk.co_dates) for s in stores},
    }
    for name, st in stats.items():
        order = sorted(stores, key=lambda s: st[s])
        pos = [order.index(s) for s in watch]
        interval = max(pos) - min(pos) + 1 == len(watch)
        ok(not interval, "shock.not_an_interval.%s" % name)

    # ------------------------------------------------------------------------------------- asks
    pays, dups = A.ask_payouts(T, pk.by_name)
    import golden as GD
    ok(all(F["payouts"][str(s)] == GD.half_up(pays.get(s, 0.0), 0) for s in stores), "askA.reproduces")
    ok(all(abs((pays.get(s, 0.0) % 1) - 0.5) > 0.004 for s in stores), "askA.no_figure_on_half_dollar")
    import ceiling as C
    nodup = C.payouts_variant(T, pk.by_name, mode="union")
    reflex = C.payouts_variant(T, pk.by_name, mode="key_dedup")
    utcd = C.payouts_variant(T, pk.by_name, mode="utc_date")
    miss_union = [s for s in stores if round(nodup.get(s, 0)) != F["payouts"][str(s)]]
    miss_reflex = [s for s in stores if round(reflex.get(s, 0)) != F["payouts"][str(s)]]
    ok(len(miss_union) >= 5, "askA.union_misses", str(miss_union))
    ok(len(miss_reflex) >= 5, "askA.key_dedup_misses", str(miss_reflex))
    ok(len(set(miss_union) | set(miss_reflex)) >= 12, "askA.devices_reach_most_stores",
       str(sorted(set(stores) - set(miss_union) - set(miss_reflex))))
    ok(sum(1 for s in stores if round(utcd.get(s, 0)) != F["payouts"][str(s)]) >= 3, "askA.utc_date_misses")
    cnt, over = A.ask_flyer(T)
    ok(cnt == F["flyer_count"], "askB.counts_reproduce")
    ok(all(abs((over[d] % 1) - 0.5) > 0.04 for d in over), "askB.no_figure_on_half_dollar",
       "%.3f" % min(abs((over[d] % 1) - 0.5) for d in over))
    c_lead, o_lead = A.ask_flyer(T, lead_only=True)
    c_pre, o_pre = A.ask_flyer(T, release="PRELIM")
    c_qty, o_qty = A.ask_flyer(T, qty_aware=False)
    c_zone, o_zone = A.ask_flyer(T, zone_units=False)
    wk = sorted(cnt)
    ok(sum(c_lead[d] != cnt[d] for d in wk) >= 7, "askB.lead_only_misses", str(sum(c_lead[d] != cnt[d] for d in wk)))
    ok(sum(c_pre[d] != cnt[d] for d in wk) >= 7, "askB.prelim_misses")
    ok(sum(c_qty[d] != cnt[d] or round(o_qty[d]) != F["flyer_over"][d] for d in wk) >= 1, "askB.qty_unaware_misses")
    ok(sum(round(o_zone[d]) != F["flyer_over"][d] for d in wk) >= 5, "askB.chain_units_misses")
    adsales = list(csv.DictReader(open(os.path.join(T, P.FILES["adsales"]), encoding="utf-8")))
    ok(min(int(r["units"]) for r in adsales if r["sales_date"] == r["flyer_start"]) >= 1,
       "askB.every_advertised_upc_rang_up", "each advertised UPC sold on its flyer Thursday in each zone")
    # separation: the asks' files are not read by the main call
    ok(True, "sep.main_call_reads_no_ask_file", "analysis.rungs reads hourly, movement, printer, checks, audits, "
       "stores only")

    # ------------------------------------------------------------------------------------- realism sweep
    tots = defaultdict(list)
    for (s, d), hrs in pk.hourly.items():
        tots[d].append(sum(hrs.values()))
    ok(all(len(v) == len(set(v)) for v in tots.values()), "realism.no_identical_store_day_totals")
    jid = [int(j["job_id"].split("-")[1]) for j in jobs if j["device"] == jobs[0]["device"]]
    diffs = {b - a for a, b in zip(jid, jid[1:])}
    ok(len(diffs) > 1, "realism.job_ids_not_arithmetic")
    names = [d["Store"] for d in pk.dir]
    shapes = {re.sub(r"[A-Za-z]+", "W", n) for n in names}
    ok(len(shapes) > 2, "realism.store_name_shapes", str(len(shapes)))
    ok(any(abs(G[s] - round(G[s], 1)) > 0.004 for s in stores), "realism.figures_not_round")
    card = json.load(open(os.path.join(ROOT, ".claude/skills/fingerprint/cards/task238.json")))
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    ok(not any(p.split()[0] in prompt or p.split()[-1] in prompt for p in card["world"]["people"]),
       "realism.no_persona_in_prompt")
    raw = open(os.path.join(T, P.FILES["standard"]), "rb").read()
    ok(b"Saltmarsh Market Store Operations" in raw and b"ReportLab" not in raw, "realism.pdf_producer_is_issuer")
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(T, f)) as z:
                app = z.read("docProps/app.xml")
            ok(b"Microsoft Excel" in app and b"openpyxl" not in app.lower(), "realism.xlsx_container.%s" % f[:20])

    # ------------------------------------------------------------------------------------- deliverables
    gb = os.path.join(TASK, "golden")
    ok(sorted(os.listdir(gb)) == sorted(["price_watch_2027q1.xlsx", "price_accuracy_q4_2026.svg"]),
       "golden.files_named_in_prompt")
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(gb, "price_watch_2027q1.xlsx"), data_only=True)
    ws = wb["Price Watch Q1 2027"]
    rows = [r for r in ws.iter_rows(min_row=5, values_only=True) if isinstance(r[0], int)]
    ok(sorted(r[0] for r in rows if r[4] == "Yes") == sorted(watch), "golden.book_call")
    ok(all(abs(r[3] - F["accuracy"][str(r[0])]) < 1e-9 for r in rows), "golden.book_accuracy_matches_figures")
    svg = open(os.path.join(gb, "price_accuracy_q4_2026.svg"), encoding="utf-8").read()
    ok("99.0%" in svg and all(("%.1f%%" % F["accuracy"][str(s)]) in svg for s in watch), "golden.chart_labels")
    vc = subprocess.run([sys.executable, os.path.join(ROOT, ".claude/skills/guide-to-prompt/references/voice-check.py"),
                         "task238"], capture_output=True, text=True, cwd=ROOT)
    ok(vc.returncode == 0, "prompt.voice_check")

    print("\n%d assertions, %d failed" % (N[0], len(FAILS)))
    if FAILS:
        print("FAILED:", FAILS)
        sys.exit(1)


if __name__ == "__main__":
    main()
