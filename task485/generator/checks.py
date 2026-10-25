"""task485's assertions on the cut pack and on the generator's clean truth: the input gates, the three rules (R1 the
raw material, R2 every Layer 1 item mishandled, R3a the analyst test, R3b the decisive step alone, R3c no plant), the
ladder and its margins, every semantic fork row (SF1 to SF15), rounding robustness, the ask, the documents' positive
controls and the realism sweep.

    python3 task485/generator/checks.py          (after build.py)
"""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import ash as A           # noqa: E402
import build as B         # noqa: E402
import ceiling as C       # noqa: E402
import golden as G        # noqa: E402
import pack as PK         # noqa: E402
import pack_ash_read      # noqa: E402
import world as W         # noqa: E402

N, FAILS = [0], []
GOLD = ["S01-2", "S03-1", "S12-1", "S13-1", "S14-1", "S15-1"]


def check(label, ok, detail=""):
    N[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def ten(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def hundred(x):
    return int(math.floor(x / 100.0 + 0.5) * 100)


def comps(bal):
    return (hundred(sum(v["formed"] for v in bal.values())), hundred(sum(v["removed"] for v in bal.values())))


def pdf_text(name):
    import pdfplumber
    with pdfplumber.open(os.path.join(T, name)) as p:
        return "\n".join(pg.extract_text() or "" for pg in p.pages)


def rows_csv(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    tr = B.truth()
    w, rt = tr["w"], tr["rt"]
    bal = G.balance(w, w.returns, w.tickets, w.permits)
    gold = G.listed_of(bal)
    base_c = comps(bal)
    names = {b["id"]: b["firm"] if b["site"] not in PK.UNIT_NAME else None for b in w.B}

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(T))
    check("G1 ten or more files in the pack", len(files) >= 10, "%d" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    coal_rows = rows_csv("coal_deliveries_2026.csv")
    check("G3 a file of 25,000 rows or more", len(coal_rows) >= 25000, "coal_deliveries_2026.csv %d" % len(coal_rows))
    check("G4 two or more distractors named in metadata.json, none named for its role",
          len(meta["distractor_files"]) >= 2 and not any("distract" in f for f in files))
    check("G5 every file carries a source, a date and a licence",
          all(x["source"] and x["date"] and x["license"] for x in meta["files"]) and len(meta["files"]) == len(files))
    check("G6 the call and the ask read neither distractor (no golden input names the ambient network or the "
          "statistics office)", all(n not in open(os.path.join(HERE, m)).read() for m in ("golden.py", "pack_ash_read.py")
                                    for n in ("ambient", "national_coal")))

    # ------------------------------------------------------------ R1: the field's raw material
    certs = {(r["Supplier"], r["Certificate No"]) for r in coal_rows}
    check("R1a the spine carries each delivery's laboratory analysis and net tonnes",
          all(r["Total Sulphur % (ar)"] and r["Net Tonnes"] for r in coal_rows) and len(certs) > 5000,
          "%d rows under %d certificates" % (len(coal_rows), len(certs)))
    per_b = collections.Counter(x["boiler"] for x in w.tickets)
    check("R1b every scrubber's quarry tickets, the weekly certificates, each quarter's silo stocks and each "
          "guarantee's stoichiometry ship", min(per_b.values()) >= 10 and len(per_b) == 18 and
          all(len(w.purity[q]) >= 54 for q in w.purity) and len(w.returns) == 72,
          "tickets per scrubber %d to %d" % (min(per_b.values()), max(per_b.values())))
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += list(rows_csv(f)[0].keys())
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(os.path.join(T, f), read_only=True)
            for ws in wb.worksheets:
                first = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
                heads += [str(x) for x in first if x]
    check("R1c no shipped column holds a boiler's sulphur dioxide over a period (the tests carry concentrations "
          "only)", not [h for h in heads if re.search(r"(?i)(sulphur dioxide|so2).*(tonne|\(t\))", h)])
    rem = {b: v["caco3"] / W.MCACO3 / next(p["ratio"] for p in w.permits if p["boiler"] == b) * W.MSO2
           for b, v in bal.items()}
    check("R1d the golden's removal is the calcium carbonate each scrubber consumed over its moles per mole removed",
          all(abs(rem[b] - bal[b]["removed"]) < 1e-6 for b in bal))

    # ------------------------------------------------------------ the call
    check("call: the balance lists the golden six", gold == GOLD, ", ".join(gold))
    check("call: figures.json carries the same six", sorted(figs["call"]["listed"]) == sorted(
        figs["order"][i] for i, b in enumerate(sorted(rt, key=lambda b: PK.PERMIT[b])) if b in GOLD))
    lo = min(bal[b]["so2"] for b in GOLD) / W.LINE
    hi = W.LINE / max(bal[b]["so2"] for b in bal if b not in GOLD)
    check("call: every listed boiler 1.2 times the line or more and every other one 1.2 times under it or more",
          lo >= 1.2 and hi >= 1.2, "%.3f over, %.3f under" % (lo, hi))

    # ------------------------------------------------------------ R2: every Layer 1 item mishandled
    def same(label, **o):
        v = G.balance(w, w.returns, w.tickets, w.permits, **o)
        check("R2 %s: the call and the two components" % label, G.listed_of(v) == GOLD and comps(v) == base_c,
              "%s; %s" % (", ".join(G.listed_of(v)), comps(v)))
    same("the collation's December 2025 and January 2027 receipts kept", window="all")
    same("receipts dated by dispatch", window="dispatched")
    same("re-issued certificates' deliveries set aside",
         skip={x["lot"] for x in w.lots if x["reissued"]})
    same("the 2026 template's gas oil added to its coal fired", gas_oil=True)
    same("ISO weeks counted from 1 January", purity_mode="jan1")
    v = G.balance(w, w.returns, w.tickets, w.permits, coal="receipts")
    check("R2 the yard reported once on the first boiler's row, coal burned rebuilt as receipts less the surveyed "
          "stock change shared by the returns' coal (SF3, guidance 4.1 files the returns): the call",
          G.listed_of(v) == GOLD)
    year_ok = True
    for r in coal_rows:
        if r["Supplier"] != "Ostmouth Coal Imports":
            continue
        d, m, y = (int(x) for x in r["Received"].split("/"))
        if d <= 12 and int(y) != dt.date(y, d, m).year:
            year_ok = False
    check("R2 Ostmouth's day-first dates read month first: no delivery changes year", year_ok)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, "limestone_certificates_2026.xlsx"), read_only=True)
    dp = collections.defaultdict(set)
    for r in wb["Delivery points"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            dp[(r[0], r[1], r[3])].add(r[4])
    tk = rows_csv("limestone_tickets_2026.csv")
    check("R2 every quarry ticket resolves to exactly one permit through the Delivery points sheet",
          all(len(dp[(t_["Quarry"], t_["Account"], t_["Delivery Point"])]) == 1 for t_ in tk), "%d tickets" % len(tk))
    sc = collections.defaultdict(set)
    for r in rows_csv("coal_supplier_customers.csv"):
        sc[(r["Supplier"], r["Customer Code"])].add(r["Customer"])
    check("R2 every coal row's customer code resolves to exactly one site",
          all(len(sc[(r["Supplier"], r["Customer Code"])]) == 1 for r in coal_rows))
    E = pack_ash_read.read(T)
    check("R2 every ash row resolves to one site through the contractors' cross-reference",
          all(r["site"] in w.sites for k in E for r in E[k]), "%d rows" % sum(len(v) for v in E.values()))
    check("R2 the two laboratories' reference oxygen: the golden opens no test report, and the test-rate route at "
          "each report's own reference lists Pridwold Starch and Candrigg Soda Works",
          G.listed(rt, "test_rate") == ["S10-1", "S12-1"])

    # ------------------------------------------------------------ R3
    check("R3a the analyst test: each scrubber's 2026 test removal carried across the year lists Candrigg Soda Works "
          "alone", G.listed(rt, "tested") == ["S12-1"], "%.0f t" % rt["S12-1"]["tested"])
    check("R3b the decisive step alone: the default path with only its removal taken from the reagent balance files "
          "the golden", G.listed(rt, "golden") == GOLD)
    for k, want in (("design", ["S01-1", "S12-1"]), ("test_rate", ["S10-1", "S12-1"]),
                    ("golden_ratio_one", ["S01-2", "S03-1", "S13-1", "S14-1", "S15-1"]),
                    ("golden_limestone_as_caco3", ["S01-2", "S03-1", "S13-1", "S14-1", "S15-1"]),
                    ("none", sorted(rt))):
        check("R3b the lower rung %s stays off the golden" % k, G.listed(rt, k) == want and want != GOLD,
              ", ".join(G.listed(rt, k)) if len(want) < 10 else "all eighteen")
    sig = collections.Counter((x["s"], x["tm"], x["ash"], x["c"], x["gcv"]) for x in
                              {v["lot"]: v for v in w.lots}.values())
    check("R3c no copied block: no two coal lots share an analysis", max(sig.values()) == 1)
    seqs = collections.Counter(tuple(round(x["t"], 2) for x in w.tickets if x["boiler"] == b) for b in rt)
    check("R3c no copied block: no two scrubbers share a ticket sequence", max(seqs.values()) == 1)
    txt = {f: pdf_text(f) for f in files if f.endswith(".pdf")}
    tonnes = [(f, m.group(0)) for f, s in txt.items() for m in re.finditer(r"\b(\d{2,3}(?:\.\d+)?) tonnes", s)
              if float(m.group(1)) not in (250.0, 64.066, 32.065)]
    check("R3c no shipped document states or ranks a boiler's tonnage", not tonnes, str(tonnes[:3]))

    # ------------------------------------------------------------ ladder and margins
    for k, floor in (("design", 1.15), ("tested", 1.15), ("test_rate", 1.15), ("golden_ratio_one", 1.15)):
        on = [rt[b][k] for b in rt if rt[b][k] >= W.LINE]
        off = [rt[b][k] for b in rt if rt[b][k] < W.LINE]
        m = min(min(on) / W.LINE, W.LINE / max(off))
        check("ladder: %s's set-defining cells 1.15 times from the line or more" % k, m >= floor, "%.3f" % m)
    ratios = [rt[b]["golden"] / rt[b]["tested"] for b in GOLD if b != "S12-1"]
    check("ladder: the five bypassed boilers run three times their tested figures or more", min(ratios) >= 3.0,
          "%.1f to %.1f" % (min(ratios), max(ratios)))

    # ------------------------------------------------------------ semantic forks
    check("SF1 calendar 2026: the four returns are the calendar quarters 1 January to 31 December",
          [W.day(a).isoformat() + "/" + W.day(z).isoformat() for a, z in __import__("returns").QDAYS] ==
          ["2026-01-01/2026-03-31", "2026-04-01/2026-06-30", "2026-07-01/2026-09-30", "2026-10-01/2026-12-31"])
    check("SF2 sulphur dioxide formed in place of leaving the stack lists all eighteen (another set; guidance 3.1)",
          G.listed(rt, "none") == sorted(rt))
    v = G.balance(w, w.returns, w.tickets, w.permits, weighted=False)
    check("SF4 a plain mean over delivery rows adds Pridwold Starch (another set; guidance 4.2 weights by tonnes)",
          G.listed_of(v) == sorted(GOLD + ["S10-1"]) and "each weighted by the tonnes" in txt[
              "so2_inventory_guidance_2026.pdf"].replace("\n", " "))
    v = G.balance(w, w.returns, w.tickets, w.permits, window="dispatched")
    check("SF5 a 2026 receipt dated by dispatch in place of receipt: the call (guidance 4.2 dates it by receipt)",
          G.listed_of(v) == GOLD and "received at the site" in txt["so2_inventory_guidance_2026.pdf"].replace("\n", " "))
    import openpyxl as _ox
    reg = [r for r in _ox.load_workbook(os.path.join(T, "permitted_boilers_register_2026.xlsx"), read_only=True)[
        "Register"].iter_rows(min_row=2, values_only=True) if r[0]]
    check("SF6 the ash's share is the permit register's figure for each boiler, 2 per cent pulverised and 5 per cent "
          "stoker, as the golden applies it", all(abs(r[11] - (2.0 if r[4] == "Pulverised coal" else 5.0)) < 1e-9 for r in reg)
          and all(abs(p["ash_ret"] - (0.02 if p["type"] == "PF" else 0.05)) < 1e-12 for p in w.permits))
    check("SF13 every boiler's records resolve across the files by permit number: the coal customer codes, the quarry "
          "delivery points, the laboratories' permit columns and the contractors' names (R2 above)",
          len({r[0] for r in reg}) == 18 and all(PK.PERMIT[b] in txt["scrubber_guarantee_schedules.pdf"] for b in rt)
          and all(PK.PERMIT[x["boiler"]] in txt["scrubber_tests_2026_iverstow.pdf"] + txt["scrubber_tests_2026_jarrness.pdf"]
                  for x in w.tests))
    v = G.balance(w, w.returns, w.tickets, w.permits, mratio=2.0)
    check("SF7 sulphur to sulphur dioxide at 2: the call and every boiler's tonnes",
          G.listed_of(v) == GOLD and all(ten(v[b]["so2"]) == ten(bal[b]["so2"]) for b in bal))
    check("SF8 the line on rounded tonnes: the call", sorted(b for b in bal if ten(bal[b]["so2"]) >= 250) == GOLD)
    site_tot = collections.Counter()
    for b in bal:
        site_tot[b.split("-")[0]] += bal[b]["so2"]
    by_site = sorted(s for s, x in site_tot.items() if x >= W.LINE)
    check("SF9 each site in place of each boiler names Quarholt Board Mills as a site (another set; the Order's "
          "note makes each boiler a unit)", "S01" in by_site and "each boiler is a unit" in txt[
              "so2_order_2027_schedule_note.pdf"].replace("\n", " "))
    v = G.balance(w, w.returns, w.tickets, w.permits, stock_change=False)
    check("SF10 the tickets alone in place of tickets less the silo's change: the call", G.listed_of(v) == GOLD)
    v = G.balance(w, w.returns, w.tickets, w.permits, purity_mode="mean")
    spread = max(abs(v[b]["so2"] / bal[b]["so2"] - 1) for b in bal)
    check("SF11 each quarry's mean certificate in place of each week's: the call", G.listed_of(v) == GOLD,
          "widest %.1f per cent" % (100 * spread))
    check("SF12 the stoichiometry is per mole removed in both schedules",
          txt["scrubber_guarantee_schedules.pdf"].replace("\n", " ").count("mole of sulphur dioxide removed") >= 2)
    moist = {}
    for q, sh in (("Bromscar Quarry", "Bromscar weekly"), ("Molhope Lime and Stone", "Molhope weekly")):
        moist[q] = {r[0]: r[4] for r in wb[sh].iter_rows(min_row=2, values_only=True) if r[0]}
    v = G.balance(w, w.returns, w.tickets, w.permits, moisture=moist)
    notes = " ".join(str(r[0]) for r in wb["Notes"].iter_rows(values_only=True) if r[0])
    check("SF14 the certificate's carbonate read as dry with the moisture taken off adds Quarholt Board Mills "
          "boiler 1 (another set; the certificates state it as delivered, moisture included)",
          G.listed_of(v) == sorted(GOLD + ["S01-1"]) and "as delivered, its moisture included" in notes)
    for mm in (100.09, 100.1):
        v = G.balance(w, w.returns, w.tickets, w.permits, mcaco3=mm)
        check("SF15 calcium carbonate at %s g a mole: the call and every boiler's tonnes" % mm,
              G.listed_of(v) == GOLD and all(ten(v[b]["so2"]) == ten(bal[b]["so2"]) for b in bal))

    # ------------------------------------------------------------ rounding
    edge = min(abs(bal[b]["so2"] % 10 - 5) for b in bal)
    check("rounding: every boiler's tonnes 1 tonne or more from a rounding boundary", edge >= 1.0, "%.2f" % edge)
    tots = [sum(x["formed"] for x in bal.values()), sum(x["removed"] for x in bal.values())]
    e2 = min(abs(t % 100 - 50) for t in tots)
    check("rounding: the two components 15 tonnes or more from a rounding boundary", e2 >= 15, "%.1f" % e2)

    # ------------------------------------------------------------ the ask
    g_cut = C.route(E, keep_moorside_sub=False)
    check("ask A: the cut pack's golden equals the clean truth's, every site at its rounding",
          all(ten(g_cut[s][0]) == ten(tr["ash"][s]["t"]) and round(g_cut[s][1], 1) == round(tr["ash"][s]["rec_pct"], 1)
              for s in tr["ash"]))
    check("ask A: figures.json carries the cut pack's golden",
          all(figs["ash"][w.sites[s]["firm"]]["t"] == ten(g_cut[s][0]) and
              abs(figs["ash"][w.sites[s]["firm"]]["rec"] - round(g_cut[s][1], 1)) < 1e-9 for s in g_cut))
    crack = C.score(g_cut, C.route(E))
    check("ask A: every ash line once as exported keeps under a tenth of the 32 figures", crack <= 3, "%d" % crack)
    subs = collections.Counter(r["site"] for r in E["moorside"] if r["kind"] != "other" and not r["ref"].startswith("WM-"))
    check("ask A: Whinmoss bills a local contractor's collection at every site", len(subs) == 16,
          "%d lines" % sum(subs.values()))
    loc = {(r["site"], r["day"]) for k in ("tolland", "greave") for r in E[k] if r["kind"] != "other"}
    own_same = sum(1 for r in E["moorside"] if r["ref"].startswith("WM-") and r["kind"] != "other"
                   and (r["site"], r["day"]) in loc)
    check("ask A: Whinmoss's own collections beside a local's on the same day exist (genuine pairs)", own_same >= 50,
          "%d" % own_same)
    lags = [r["day"] - next(j["day"] for k in ("tolland", "greave") for j in E[k] if j["job"] == r["ref"])
            for r in E["moorside"][:4000] if not r["ref"].startswith("WM-") and r["kind"] != "other"][:200]
    check("ask A: a subcontracted line is dated 3 to 10 days after the local's collection", min(lags) >= 3 and
          max(lags) <= 10)
    check("ask A: the call's population holds no ash row (no ash file is a golden input of the call)",
          all(n not in open(os.path.join(HERE, "golden.py")).read() for n in ("moorside", "tolland", "greave")))

    # ------------------------------------------------------------ documents
    g = txt["so2_inventory_guidance_2026.pdf"].replace("\n", " ")
    check("docs: the guidance files the year, the measure, 64.066 over 32.065, the returns' coal, the receipts by "
          "received date weighted by tonnes, the permit's ash retention and the unrounded line",
          all(s in g for s in ("calendar 2026", "leaving its stack", "64.066", "32.065", "four quarterly returns",
                               "received at the site", "permit register's figure", "unrounded")))
    check("docs: the guidance never names limestone, a test or a removal rate",
          not re.search(r"(?i)limestone|performance test|removal effic|tested", g))
    allt = " ".join(txt.values())
    for f in files:
        if f.endswith((".csv", ".json")):
            allt += open(os.path.join(T, f), encoding="utf-8").read(200000)
    hits = re.findall(r"(?i)\bby-?pass\w*|outage|availability|downtime|\bidle\b|stood down", allt)
    check("docs: no shipped text names the decisive relation's vocabulary (bypass, outage, availability, downtime)",
          not hits, str(hits[:5]))

    # ------------------------------------------------------------ realism sweep
    def dd(s):
        return dt.date.fromisoformat(s) if "-" in s else dt.datetime.strptime(s, "%d/%m/%Y").date()
    check("realism: every delivery received on or after its dispatch, and its certificate issued after dispatch",
          all(dd(r["Received"]) >= dd(r["Dispatched"]) and dd(r["Issued"]) > dd(r["Dispatched"]) for r in coal_rows))
    road = [dd(r["Received"]).weekday() for r in coal_rows if r["Transport"] == "Road"]
    rail = [dd(r["Received"]).weekday() for r in coal_rows if r["Transport"] == "Rail" and r["Received"][-4:] == "2026"]
    check("realism: no road delivery on a Sunday", 6 not in road)
    check("realism: trains received across the week (rail transit)", len(set(rail)) >= 5)
    days = [x["day"] for x in w.ash_jobs if x["day"] <= 364]
    check("realism: no ash collection on a Sunday or a holiday",
          all(W.day(d).weekday() != 6 and d not in A.CLOSED for d in days))
    tn = collections.defaultdict(list)
    for t_ in tk:
        tn[t_["Quarry"]].append((t_["Date"], t_["Time"], t_["Ticket"]))
    check("realism: each quarry's ticket numbers run in date and time order",
          all([x[2] for x in sorted(v)] == sorted(x[2] for x in v) for v in tn.values()))
    tdays = [W.day(x["day"]) for x in w.tests]
    check("realism: every test on a weekday between April and October, each report issued after its last test",
          all(d.weekday() < 5 and 4 <= d.month <= 10 for d in tdays) and
          all(dt.datetime.strptime(re.search(r"Issued (\d+ \w+ \d{4})", txt[f].replace("\n", " ")).group(1),
                                     "%d %B %Y").date() > max(W.day(x["day"]) for x in w.tests if x["lab"] == lab)
              for f, lab in (("scrubber_tests_2026_iverstow.pdf", "Iverstow Emission Testing"),
                             ("scrubber_tests_2026_jarrness.pdf", "Jarrness Stack Testing"))))
    cnt = [per_b[b] for b in rt]
    check("realism: the scrubbers' ticket counts are not alike", len(set(cnt)) >= 14, "%d distinct" % len(set(cnt)))
    coal_tot = sum(r["coal_burned"] for r in w.returns)
    check("realism: no round headline total", coal_tot % 1000 and len(tk) % 100 and len(coal_rows) % 100)
    lots_per_site = collections.Counter(x["site"] for x in w.lots)
    check("realism: no identical delivery counts across sites", len(set(lots_per_site.values())) == 16)
    people = ["Maria Burgess", "Timothy Peterson", "Brenda Cook"]
    found = {p for p in people if p in allt}
    check("realism: the personas in the pack are the card's", found <= set(people) and "Brenda Cook" in found and
          "Timothy Peterson" in found and "Maria Burgess" in found, ", ".join(sorted(found)))
    feeder = [abs(G.coal_from_receipts(w.lots, w.returns)[b] / G.coal_burned(w.returns)[b] - 1) for b in rt]
    check("realism: the yard balance and the weigh feeders differ, as stockpile surveys and belt weighers do",
          0.0005 < max(feeder) < 0.03, "widest %.2f per cent" % (100 * max(feeder)))

    print("\n%d checks, %d FAIL" % (N[0], len(FAILS)))
    if FAILS:
        print("FAILED: " + "; ".join(FAILS))
        sys.exit(1)


if __name__ == "__main__":
    main()
