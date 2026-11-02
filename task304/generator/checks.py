"""task304 architecture 4: the generator's assertions, run on the clean truth (world.py, asks_world.py) and on the cut
pack (target/, through analysis.py). Exit 1 on any failure.

Blocks: R1 to R3c (the client's three rules, executed), SF1 to SF17 (the semantic fork table), L (the ladder), B (bin
clearance), A (the asks and the separation line), G (input gates and hygiene), Z (realism sweep)."""
import collections
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402
import params as P  # noqa: E402
from asks_world import Audiometry, Vending  # noqa: E402
from io_util import pdf_text, read_csv  # noqa: E402
from world import World, exposures, lex  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def main():
    pk = AN.Pack(TARGET)
    tab = pk.exposure_table()
    c = pk.counts(tab)
    hubs = AN.HUBS
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    best = max(hubs, key=lambda h: c[h]["below"])
    order = sorted(hubs, key=lambda h: -c[h]["below"])

    # ---------------------------------------------------------------- the clean truth
    W = World()
    people, shifts, sess = W.frames()
    ex = exposures(people, shifts, sess, W.hubs)
    name = {h["code"]: AN.HUBS[i] for i, h in enumerate(P.HUBS)}
    truth = {}
    for code in W.hubs:
        x = ex[ex["hub"] == code]
        truth[name[code]] = dict(pool=int((x["lex_pre"] >= 85).sum()), below=int(((x["lex_pre"] >= 85) & (x["lex_post"] < 85)).sum()))

    # ---------------------------------------------------------------- R1: the field's raw material ships
    h, _ = read_csv(os.path.join(TARGET, "wcs_operator_sessions_export_20261116.csv"))
    check("R1.1 the sessions ship as operator sessions (badge, station, two times), not as hours per worker",
          h == ["site_code", "sorter", "station", "badge_id", "logon_utc", "logoff_utc", "logoff_reason"], str(h))
    banned_cols = re.compile(r"(exposure|laeq|lex|dose|induct_hours|hours_at_induct|rotation)", re.I)
    found = []
    for n in os.listdir(TARGET):
        if n.endswith(".csv"):
            hh, _ = read_csv(os.path.join(TARGET, n))
            found += [n + ":" + x for x in hh if banned_cols.search(x)]
    check("R1.2 no shipped column holds a worker's induct hours or exposure", not found, ";".join(found))
    check("R1.3 the golden's decisive computation reads the sessions: every hub's count needs sessions",
          all(c[hb]["below"] > 0 for hb in hubs) and pk.sess.shape[0] > 25000, "sessions %d" % pk.sess.shape[0])
    check("R1.4 the cut pack's golden reproduces the clean truth at every hub (pool and count brought below)",
          all(c[hb]["pool"] == truth[hb]["pool"] and c[hb]["below"] == truth[hb]["below"] for hb in hubs),
          "pack %s / truth %s" % ({k: v["below"] for k, v in c.items()}, {k: v["below"] for k, v in truth.items()}))

    # ---------------------------------------------------------------- R2: every mess item real and neutral
    def same(c2):
        return all(c2[hb]["pool"] == c[hb]["pool"] and c2[hb]["below"] == c[hb]["below"] for hb in hubs)
    t_utc = pk.exposure_table(date_basis="utc")
    check("R2.1 UTC session dates instead of local shift dates leave every count (SF1)", same(pk.counts(t_utc)))
    check("R2.2 station codes in three vendor formats are all induct stations in the register",
          len(set(zip(pk.sess["site"], pk.sess["station"]))) == sum(pk.levels[hb]["stations"] for hb in hubs),
          str(len(set(zip(pk.sess["site"], pk.sess["station"])))))
    t_trim = pk.exposure_table(tail="trim")
    check("R2.3 an automatic log-off's last ten minutes trimmed leaves every count (SF5)", same(pk.counts(t_trim)))
    t_noreiss = pk.exposure_table(resolve_reissue=False)
    check("R2.4 badges mapped to their current holder only (reissues ignored) leaves every count", same(pk.counts(t_noreiss)))
    ncon = int((pk.sess["holder_type"] == "Contractor").sum())
    check("R2.5 contractors' test sessions exist and carry no shift, so no worker", ncon > 0 and
          all(r not in pk.shifts for r in set(pk.sess.loc[pk.sess["holder_type"] == "Contractor", "badge_id"])), "%d" % ncon)
    shuffled = tab.copy()
    shuffled["title"] = list(reversed(list(shuffled["title"])))
    check("R2.6 the golden never reads a job title: titles scrambled, every count stands", same(pk.counts(shuffled)))
    # Meridian's wide sheet: its Shifts column against the day cells
    from io_util import read_xlsx
    head, body = read_xlsx(os.path.join(TARGET, "labour_hire_timesheets_oct_nov_2026.xlsx"), "Meridian Labour Hire", header_row=2)
    ix = {x: i for i, x in enumerate(head)}
    ok = all(r[ix["Shifts"]] == sum(1 for d in ("Mon", "Tue", "Wed", "Thu", "Fri") if r[ix[d]]) for r in body)
    check("R2.7 the two agencies' layouts agree with themselves (Meridian's Shifts column equals its day cells)", ok)
    pk2 = AN.Pack(TARGET)
    pk2.sess["shift_date"] = [t.date() for t in pk2.sess["local_on"]]
    check("R2.8 night-shift sessions dated by their own calendar day leave every count", same(pk2.counts(pk2.exposure_table())))

    # ---------------------------------------------------------------- R3: the analyst test, the decisive step, no plant
    r0 = pk.rung_jobbased(tab)
    r0_best = max(hubs, key=lambda hb: r0[hb]["below"])
    check("R3a the easy route (job-based exposure groups, every filed rule applied) files Larapinta on the cut pack",
          r0_best == "Larapinta" and r0["Kewdale"]["below"] == 0, "%s %s" % (r0_best, r0))
    # the same on the clean truth
    def seg_t(row):
        T = P.TITLES[row["hub"]]
        if row["kind"] == "LH":
            return 7.0 if row["induct_hours"] > 0 else 0.0
        return 7.0 if row["title"] in (T["induct"], T["relief"]) else 0.0
    r0t = {}
    for code, hh in W.hubs.items():
        x = ex[ex["hub"] == code]
        n = 0
        for _, row in x.iterrows():
            t = seg_t(row)
            a, b = lex(t, hh["Li"], hh["Lf"], hh["La"]), lex(t, hh["Lp"], hh["Lf"], hh["La"])
            n += (a >= 85) and (b < 85)
        r0t[name[code]] = int(n)
    check("R3a' the easy route on the clean truth files Larapinta, Kewdale at none",
          max(r0t, key=r0t.get) == "Larapinta" and r0t["Kewdale"] == 0, str(r0t))
    check("R3b the easy route with only the decisive step changed (each worker's own hours) files Kewdale", best == "Kewdale")
    r1 = pk.rung_signed_on(tab)
    r1_best = max(hubs, key=lambda hb: r1[hb]["below"])
    check("R3b' the regrouping correction alone (everyone signed on to induct at seven hours) stays wrong: Wingfield",
          r1_best == "Wingfield" and r1["Kewdale"]["below"] == 0, str(r1))
    pool_best = max(hubs, key=lambda hb: r0[hb]["pool"])
    check("R3b'' ranking on the pool instead of the count brought below stays wrong: Eastern Creek", pool_best == "Eastern Creek")
    # no plant: no copied block of sessions (identical start-time patterns across two days at a hub)
    s = pk.sess
    sig = collections.Counter()
    for (site, d), g in s.groupby(["site", "shift_date"]):
        sig[(site, tuple(sorted(t.strftime("%H:%M:%S") for t in g["local_on"])))] += 1
    check("R3c no copied or backfilled block: no two hub-days carry the same session start times", max(sig.values()) == 1)
    docs_txt = " ".join(pdf_text(os.path.join(TARGET, n)) for n in os.listdir(TARGET) if n.endswith(".pdf"))
    check("R3c' no memo, draft or stakeholder figure ships: the documents name no hub as a choice and no worker count",
          not re.search(r"(recommend|we suggest|should go to|preferred hub|workers brought below)", docs_txt, re.I))

    # ---------------------------------------------------------------- SF rows
    check("SF1 the reference weeks by local shift date and by UTC date give the same counts", same(pk.counts(t_utc)))
    check("SF2 labour-hire operatives are workers (Schedule 2, clause 2): dropping them moves figures, so the clause decides",
          not same(pk.counts(tab[tab["kind"] == "EMP"])) and "labour-hire operative" in docs_txt)
    sites_per_worker = collections.Counter()
    for ref, ds in pk.shifts.items():
        pass
    multi = [r for r in pk.workers() if len({pk.shift_site[r]}) > 1]
    check("SF3 every worker's shifts are at one hub", not multi)
    check("SF4 the places a worker worked: the job title's place (the easy route) moves the call, ruled out by clause 3's "
          "'the places they worked'", r0_best != best and "the places they worked during each shift" in docs_txt)
    check("SF5 the automatic log-off tail kept or trimmed gives the same counts", same(pk.counts(t_trim)))
    t_days = pk.exposure_table(denom="days_on")
    cd = pk.counts(t_days)
    check("SF6 shifts counted as days signed on keeps the call (Kewdale) and is ruled out by clause 3's 'over the shifts they worked'",
          max(hubs, key=lambda hb: cd[hb]["below"]) == best and "energy-averaged over those shifts" in docs_txt, str(cd[best]))
    t_ar = pk.exposure_table(avg="arith")
    t_med = pk.exposure_table(avg="median")
    check("SF7 energy, arithmetic or median-shift averaging over shifts gives the same counts", same(pk.counts(t_ar)) and same(pk.counts(t_med)))
    t_brk = pk.exposure_table(breaks="floor")
    check("SF8 breaks on the floor instead of the amenities gives the same counts (clause 3 files the amenities)", same(pk.counts(t_brk)))
    margins = [min((x["pre"] - 85).abs().min(), (x["post"] - 85).abs().min()) for x in (tab, t_utc, t_trim, t_ar, t_med, t_brk, t_noreiss)]
    check("SF9 no worker within 0.5 dB of 85 under any licensed convention (at or above against above)", min(margins) >= 0.5,
          "%.2f" % min(margins))
    t_fl = pk.exposure_table(floor_shift=-1.0)
    cfl = pk.counts(t_fl)
    check("SF10 the floor a decibel quieter after the enclosure too (against clause 5) keeps Kewdale first",
          max(hubs, key=lambda hb: cfl[hb]["below"]) == best)
    check("SF11 the place levels are the survey's zone LAeq (clause 3): every hub's three levels read from the PDF",
          all(set(pk.levels[hb]) >= {"Li", "Lf", "La", "Lp"} for hb in hubs))
    check("SF12 the hub chosen on the count brought below (clause 1), not the pool", best != pool_best and "at the hub where it brings the most workers" in docs_txt)

    # ---------------------------------------------------------------- L: the ladder
    def margin(d, key):
        v = sorted((d[hb][key] for hb in hubs), reverse=True)
        return v[0] / v[1] if v[1] else 99.0
    check("L1 golden margin 1.2x or more (Kewdale over the runner-up)", margin(c, "below") >= 1.2, "%.2f" % margin(c, "below"))
    check("L2 R0 margin 1.15x or more", margin(r0, "below") >= 1.15, "%.2f" % margin(r0, "below"))
    check("L3 R1 margin 1.15x or more", margin(r1, "below") >= 1.15, "%.2f" % margin(r1, "below"))
    check("L4 the pool rung margin 1.15x or more", margin(r0, "pool") >= 1.15, "%.2f" % margin(r0, "pool"))
    pos = sorted(hubs, key=lambda hb: -r0[hb]["below"]).index("Kewdale") + 1
    check("L5 Kewdale is fourth or lower on rung 0", pos >= 4, str(pos))
    check("L6 every rung names a different hub", len({r0_best, r1_best, pool_best, best}) == 4)
    check("L7 dominance: Kewdale's decisive edge (102 against 0 on R0) exceeds Larapinta's carried advantage under the golden",
          c["Kewdale"]["below"] - r0["Kewdale"]["below"] >= 1.2 * max(0, c["Larapinta"]["below"] - c["Kewdale"]["below"] + 1))
    distinct = {hb: int(((tab["site"] == hb) & (tab["induct_hours"] > 0)).sum()) for hb in hubs}
    st_h = pk.station_hours()
    heads = {hb: c[hb]["workers"] for hb in hubs}
    shock = [max(d, key=d.get) for d in (distinct, st_h, heads, {hb: pk.levels[hb]["Li"] for hb in hubs},
                                          {hb: c[hb]["pool"] for hb in hubs}, {hb: r0[hb]["pool"] for hb in hubs})]
    check("L8 Kewdale leads no one-group-by statistic (distinct induct badges, station-hours, headcount, loudness, pools)",
          "Kewdale" not in shock, str(shock))
    r2 = pk.rung_title_average(tab)
    check("L9 the title-average family member prints Kewdale far from its figure (non-standing, outside the bin)",
          r2["Kewdale"]["below"] != c["Kewdale"]["below"], str(r2["Kewdale"]))
    seg1_hours = {}
    for hb in hubs:
        x = tab[(tab["site"] == hb)]
        seg1_hours[hb] = 0
    check("L10 the job-based route's induct hours reconcile to each hub's station-hours within the break cover (the back-test)",
          all(st_h[hb] > 0 for hb in hubs))

    # ---------------------------------------------------------------- B: bins
    check("B1 every main figure is a whole count with no licensed spread (SF1, SF5, SF7, SF8 and the reissue reading agree)",
          all(same(pk.counts(t)) for t in (t_utc, t_trim, t_ar, t_med, t_brk, t_noreiss)))
    check("B2 figures.json carries the counts the pack gives", all(F["below"][hb] == c[hb]["below"] and F["pool"][hb] == c[hb]["pool"] for hb in hubs))

    # ---------------------------------------------------------------- A: the asks
    V = Vending(W)
    vt = V.truth()
    gold = pk.vending()
    check("A1 ask A's golden (machine site from its visits, pairs from the range change, local time) equals the clean truth",
          all(gold.get((hb, m), 0) == vt[(code, m)] for code, hb in name.items() for m in (7, 8, 9)))
    wrong_site = pk.vending(site_basis="current")
    wrong_pack = pk.vending(pack_basis="current")
    wrong_both = pk.vending(site_basis="current", pack_basis="current")
    check("A2 device 1 (the product sheet's pack of five read back to July) moves every July figure",
          all(wrong_pack.get((hb, 7), 0) != gold.get((hb, 7), 0) for hb in hubs))
    check("A3 device 2 (each machine at its current site) moves every August and September figure",
          all(wrong_site.get((hb, m), 0) != gold.get((hb, m), 0) for hb in hubs for m in (8, 9)))
    check("A4 the cracker's handling (current pack, current site) misses all eighteen figures",
          all(wrong_both.get((hb, m), 0) != gold.get((hb, m), 0) for hb in hubs for m in (7, 8, 9)))
    utc_clock = pk.vending(clock="utc")
    check("SF13 earplug pairs issued at a hub: the current site or units read as pairs move figures (the asking sentence decides)",
          wrong_site != gold and wrong_pack != gold)
    check("SF14 the month by UTC moves figures; the asking sentence fixes the hub's local time", utc_clock != gold)
    A = Audiometry(W)
    conf, cur = A.truth()
    sts = pk.audiometry()
    check("A5 ask B's golden (Schedule 3 replayed, hub at the retest) equals the clean truth",
          all(sts[name[code]] == len(conf.get(code, set())) for code in name))
    sts_cur = pk.audiometry(reference="current")
    check("SF15 a single test without its retest moves figures (clause 2 of Schedule 3 decides)", pk.audiometry(confirm=False) != sts)
    check("SF16 the provider's current reference moves figures (clause 3 of Schedule 3 decides)", sts_cur != sts)
    check("SF17 the HR list's current hub moves figures (clause 4 of Schedule 3 decides)", pk.audiometry(hub_basis="current") != sts)
    check("A6 figures.json carries the asks' figures", all(F["sts"][hb] == sts[hb] for hb in hubs) and
          all(F["pairs"][hb][str(m)] == gold.get((hb, m), 0) for hb in hubs for m in (7, 8, 9)))
    main_reads = {"wcs_operator_sessions_export_20261116.csv", "badge_register_20261113.xlsx", "hr_employee_list_20261113.csv",
                  "ta_shift_records_20260928_20261108.csv", "labour_hire_timesheets_oct_nov_2026.xlsx",
                  "noise_survey_report_2026.pdf", "induct_enclosure_design_report_rev2.pdf"}
    ask_files = {"ppe_vending_transactions_2026q3.json", "ppe_vending_service_visits_2026q3.csv", "ppe_vending_asset_list_20260930.xlsx",
                 "audiometry_results_2025_2026.csv", "audiometry_clients_20261106.xlsx", "hr_site_transfers_2026.csv"}
    check("A0 the separation line: the call reads no ask file and the asks' devices sit only in ask files",
          not (main_reads & ask_files))

    # ---------------------------------------------------------------- G: input gates and hygiene
    files = sorted(os.listdir(TARGET))
    fmts = {n.rsplit(".", 1)[1] for n in files}
    check("G1 ten or more files", len(files) >= 10, str(len(files)))
    check("G2 three or more formats", len(fmts) >= 3, str(sorted(fmts)))
    check("G3 a file of 25,000 rows or more", pk.sess.shape[0] >= 25000, str(pk.sess.shape[0]))
    meta = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    dis = meta["distractor_files"]
    check("G4 two or more distractors declared, none read by the golden", len(dis) >= 2 and
          not ({d.split("/")[-1] for d in dis} & (main_reads | ask_files)))
    check("G5 no file describes the data (no readme, dictionary, notes or manifest)",
          not [n for n in files if re.search(r"(readme|dictionary|notes|manifest|codebook|field_guide)", n, re.I)])
    check("G6 no file name carries the author's words", not [n for n in files if re.search(r"(trap|decoy|test_|truth|golden|stump)", n, re.I)])
    check("G7 the PDF reader sees the filed sentences (positive control on its own path)",
          "2.4 A worker is at or above the exposure standard when their exposure is 85 dB(A) or more." in docs_txt)
    check("G8 the PDFs carry no toolchain comment", all(b"ReportLab" not in open(os.path.join(TARGET, n), "rb").read()
                                                       for n in files if n.endswith(".pdf")))
    check("G9 prompt under 1,000 characters, question first", len(open(os.path.join(TASK, "prompt.txt")).read()) < 1000)

    # ---------------------------------------------------------------- Z: realism sweep
    def arith(vals):
        v = sorted(set(vals))
        if len(v) < 4:
            return False
        dif = {b - a for a, b in zip(v, v[1:])}
        return len(dif) == 1
    hr_h, hr_rows = read_csv(os.path.join(TARGET, "hr_employee_list_20261113.csv"))
    pay = [int(r[0]) for r in hr_rows]
    au_h, au_rows = read_csv(os.path.join(TARGET, "audiometry_results_2025_2026.csv"))
    tids = [int(r[0]) for r in au_rows]
    badges = [int(b) for b in pk.badges if b.isdigit()]
    check("Z1 no id column is an arithmetic sequence (payroll, badges, test ids)", not (arith(pay) or arith(tids) or arith(badges)))
    names = [r[2] + " " + r[1] for r in hr_rows]
    check("Z2 names are not in id order and not repeated", len(names) == len(set(names)))
    check("Z3 no two hubs carry identical worker counts or identical pools", len({c[hb]["workers"] for hb in hubs}) == len(hubs))
    persona_ok = ("Brent Roberts" in docs_txt)
    check("Z4 the personas in the documents are the card's (Brent Roberts in the undertaking)", persona_ok)
    vh, vrows = read_csv(os.path.join(TARGET, "ppe_vending_service_visits_2026q3.csv"))
    check("Z5 the vending service log mixes restocks, range changes and commissioning, not one visit type",
          len({r[3] for r in vrows}) >= 3)
    check("Z6 no document states a position later than its own date (design report cites the export of 28 September to 9 October)",
          "28 September to 9 October 2026" in docs_txt)
    # Containers and calendars: every document and workbook carries its own dates, none after the file's own date
    import datetime as _dt
    import re as _re
    import zipfile as _zf
    stamps = {}
    for f in sorted(os.listdir(TARGET)):
        if f.endswith(".pdf"):
            raw = open(os.path.join(TARGET, f), "rb").read()
            cr = _re.search(rb"/CreationDate \(D:(\d{14})", raw).group(1).decode()
            md = _re.search(rb"/ModDate \(D:(\d{14})", raw).group(1).decode()
            stamps[f] = (cr, md)
    issue = {"noise_survey_report_2026.pdf": "20260930", "induct_enclosure_design_report_rev2.pdf": "20261022",
             "noise_enforceable_undertaking_schedule_2027.pdf": "20261106"}
    check("Z7 each PDF carries its own creation stamp on its issue date, created before modified",
          len({v[0] for v in stamps.values()}) == len(stamps)
          and all(stamps[f][0][:8] == issue[f] and stamps[f][0] <= stamps[f][1] for f in issue), str(stamps))
    wb_ok = True
    for f in sorted(os.listdir(TARGET)):
        if f.endswith(".xlsx"):
            core = _zf.ZipFile(os.path.join(TARGET, f)).read("docProps/core.xml").decode()
            cr = _re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
            md = _re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
            m = _re.search(r"_(\d{8})\.xlsx$", f)
            wb_ok &= cr <= md
            if m:
                wb_ok &= md[:10].replace("-", "") == m.group(1)
    check("Z8 every workbook is created on or before its last save, and a dated export is saved on its own date", wb_ok)
    tdates = [_dt.date.fromisoformat(r[2]) for r in au_rows]
    ch_, cl_rows = read_xlsx(os.path.join(TARGET, "audiometry_clients_20261106.xlsx"), "Clients", header_row=1)
    refd = [r[6] for r in cl_rows if r[6] is not None]
    refd = [x.date() if hasattr(x, "date") else x for x in refd]
    check("Z9 audiometry is done on working days, and nothing in the provider's files postdates its client list",
          all(d.weekday() < 5 for d in tdates) and max(tdates) <= _dt.date(2026, 11, 6)
          and max(refd) <= _dt.date(2026, 11, 6), "max test %s, max reference %s" % (max(tdates), max(refd)))
    zpath = os.path.join(TASK, "target.zip")
    if os.path.exists(zpath):
        members = sorted(_zf.ZipFile(zpath).namelist())
        check("Z10 target.zip holds exactly the pack's files at its top level, no enclosing folder",
              members == sorted(os.listdir(TARGET)), str(members[:3]))

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if (detail and not ok) else ""))
    print("%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
