#!/usr/bin/env python3
"""task201 independent verifier. Reads only target/ and generator/figures.json.

    python3 generator/verify.py

No generator state, its own code path: it rebuilds the population from the two dispatch exports, the
device register, the telemetry archive and the notification log, walks the filed drill, recomputes
every graded figure and every ask answer, and reads back every format the pack ships with a positive
control on the same extractor the absence checks use.
"""
import os, sys, json, re, glob, zipfile
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
FAIL, N = [], [0]
WIN_FROM, WIN_TO = "2026-10-01", "2026-11-15"
ASOF = pd.Timestamp("2026-11-16 06:00")


def ok(c, label, detail=""):
    N[0] += 1
    if not c:
        FAIL.append("%s %s" % (label, detail)); print("FAIL %-32s %s" % (label, detail))
    else:
        print("ok   %-32s %s" % (label, detail))


def pdf_text(path):
    """The one extractor every pdf check in this file uses."""
    import pdfplumber
    with pdfplumber.open(path) as doc:
        return "\n".join((p.extract_text() or "") for p in doc.pages)


def norm_key(k):
    m = re.fullmatch(r"([A-Z]{3})-(\d+)-(\d+)/([A-Z])/(\d+)", str(k))
    if not m:
        return str(k)
    return "%s-%02d-%02d/%s/%02d" % (m.group(1), int(m.group(2)), int(m.group(3)),
                                     m.group(4), int(m.group(5)))


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    call, a1, a2, a3 = figs["call"], figs["a1"], figs["a2"], figs["a3"]

    # ---------------------------------------------------------------- read the bundle
    leg = pd.read_csv(os.path.join(TGT, "awarie_oms_2026-10-01_2026-11-07.csv"), comment="#")
    cur = pd.read_csv(os.path.join(TGT, "awarie_oms_2026-11-01_2026-11-15.csv"), comment="#")
    leg = leg.rename(columns=dict(zdarzenie_id="id", linia_sn="linia", urzadzenie="dev",
                                  rodzaj="rodzaj", ts_poczatek="start", ts_zalaczenie="end",
                                  epizod="epizod"))
    cur = cur.rename(columns=dict(id_zdarzenia="id", id_linii="linia", id_urzadzenia="dev",
                                  rodzaj_wylaczenia="rodzaj", poczatek_lokalny="start",
                                  zalaczenie_lokalne="end", epizod_pogodowy="epizod"))
    cols = ["id", "oddzial", "rejon", "linia", "dev", "rodzaj", "start", "end", "przyczyna", "epizod"]
    ev = pd.concat([leg[cols], cur[cols]], ignore_index=True).drop_duplicates("id")
    ev["start"] = pd.to_datetime(ev.start); ev["end"] = pd.to_datetime(ev.end)
    ev["key"] = ev.dev.map(norm_key)

    reg = pd.read_excel(os.path.join(TGT, "rejestr_urzadzen_sn_nn.xlsx"), sheet_name="urzadzenia")
    ev = ev.merge(reg[["id_urzadzenia", "klasa_odcinka", "odbiorcy_za_urzadzeniem",
                       "telemetria_linii"]], left_on="key", right_on="id_urzadzenia", how="left")
    ok(ev.odbiorcy_za_urzadzeniem.notna().all(), "join.register",
       "every export row joins the register on the normalised key")

    pop = ev[(ev.rodzaj == "awaryjne") & ev.end.notna() & (ev.end <= ASOF) &
             (ev.start >= pd.Timestamp(WIN_FROM)) &
             (ev.start <= pd.Timestamp(WIN_TO) + pd.Timedelta(days=1))].copy()
    ok(len(pop) == call["n_events"], "population",
       "%d unplanned restored interruptions in the window (figures.json %d)"
       % (len(pop), call["n_events"]))
    pop["telem"] = (pop.klasa_odcinka == "SN-magistrala") | (pop.telemetria_linii == True)
    ok(int(pop.telem.sum()) == call["n_telemetered"], "telemetered",
       "%d device-timed interruptions" % int(pop.telem.sum()))

    # the telemetry archive is UTC: converted at the offset that applied on each stamp it reproduces
    # the dispatch record's own start for the device-timed interruptions, and a flat hour does not
    sc = pd.read_csv(os.path.join(TGT, "telemetria_operacje_lacznikow_utc.csv"), comment="#")
    sct = pd.to_datetime(sc.ts_utc.str.replace("Z", "", regex=False))
    DST_UTC = pd.Timestamp("2026-10-25 01:00")
    sc["loc"] = (sct + pd.to_timedelta(np.where(sct < DST_UTC, 2, 1), unit="h")).dt.floor("min")
    sc["flat"] = (sct + pd.Timedelta(hours=1)).dt.floor("min")
    sc["key"] = sc.id_urzadzenia.map(norm_key)
    tel = pop[pop.telem][["key", "start"]]
    hit = len(tel.merge(sc[["key", "loc"]], left_on=["key", "start"], right_on=["key", "loc"]))
    hitf = len(tel.merge(sc[["key", "flat"]], left_on=["key", "start"], right_on=["key", "flat"]))
    ok(hit >= len(tel) * 0.99, "archive.offset",
       "%d of %d device-timed starts reproduce from the archive at +02:00 before 25 October and "
       "+01:00 after" % (hit, len(tel)))
    n_pre = int((tel.start < pd.Timestamp("2026-10-25 03:00")).sum())
    ok(hit - hitf == n_pre and n_pre > 90, "archive.flat_offset_fails",
       "a flat +01:00 reproduces only %d of them: it misses every one of the %d device-timed starts "
       "that fall while summer time still ran" % (hitf, n_pre))

    nl = pd.read_csv(os.path.join(TGT, "zgloszenia_klientow_2026.csv"), comment="#")
    nl["ts"] = pd.to_datetime(nl.ts_przyjecia)
    first = nl.dropna(subset=["id_zdarzenia"]).groupby("id_zdarzenia").ts.min()
    pop["first_call"] = pop.id.map(first)
    pop["godziny_rec"] = pop.odbiorcy_za_urzadzeniem * (pop.end - pop.start).dt.total_seconds() / 3600.0

    # the pre-notification interval, observable only where a device timed the interruption
    d = pop[pop.telem].copy()
    d["zwloka"] = (d.first_call - d.start).dt.total_seconds() / 60.0
    d = d[d.zwloka.notna() & (d.zwloka >= 0)]
    by_cls = d.groupby("klasa_odcinka").zwloka.mean()
    pooled = d.zwloka.mean()
    ok(abs(pooled - call["pooled_delay"]) < 0.6, "delay.pooled",
       "%.1f minutes (figures.json %.1f)" % (pooled, call["pooled_delay"]))
    for k, v in call["delay_by_class"].items():
        ok(abs(by_cls[k] - v) < 0.6, "delay.%s" % k, "%.1f minutes" % by_cls[k])

    need = ~pop.telem
    pop["r1"] = pop.godziny_rec
    pop["r2"] = pop.godziny_rec + np.where(need, pop.odbiorcy_za_urzadzeniem * pooled / 60.0, 0.0)
    pop["r3"] = pop.godziny_rec + np.where(
        need, pop.odbiorcy_za_urzadzeniem * pop.klasa_odcinka.map(by_cls).values / 60.0, 0.0)

    # ---------------------------------------------------------------- the filed drill
    def walk(col):
        path, scope, boxes = [], pop, []
        for lv in ["oddzial", "rejon", "klasa_odcinka"]:
            s = scope.groupby(lv)[col].sum().sort_values(ascending=False)
            boxes.append(scope.groupby(lv).agg(p=("id", "size"),
                                               o=("odbiorcy_za_urzadzeniem", "sum")).reindex(s.index))
            path.append(s.index[0]); scope = scope[scope[lv] == s.index[0]]
        return path, boxes
    p3, b3 = walk("r3"); p1, _ = walk("r1"); p2, _ = walk("r2")
    ok(p3 == call["path"], "drill.golden", "/".join(p3))
    ok(p1 == call["naive_path"], "drill.naive", "/".join(p1))
    ok(p2[0] == "PUS", "drill.pooled_rung", "the pooled interval files %s at level one" % p2[0])
    for r, nm in [("r1", "rung1"), ("r2", "rung2"), ("r3", "rung3")]:
        s = pop.groupby("oddzial")[r].sum().sort_values(ascending=False)
        ok(s.iloc[0] / s.iloc[1] >= 1.15, "margin.%s" % nm,
           "%s leads by %.3fx" % (s.index[0], s.iloc[0] / s.iloc[1]))
    for i, lvl in enumerate(call["levels"]):
        for box in lvl["boxes"]:
            got_p = int(b3[i].p[box["name"]]); got_o = int(b3[i].o[box["name"]])
            ok(got_p == box["przerwy"] and got_o == box["odbiorcoprzerwy"],
               "box.%s" % box["name"][:22],
               "%d interruptions, %d customer-interruptions" % (got_p, got_o))
    ok(int(b3[2].o[call["klass"]]) == call["leaf_odbiorcoprzerwy"], "call.figure",
       "%d customer-interruptions on the named class" % call["leaf_odbiorcoprzerwy"])

    # ---------------------------------------------------------------- A1
    sch = pd.read_excel(os.path.join(TGT, "harmonogram_wylaczen_planowanych.xlsx"), sheet_name=None)
    nov = sch["listopad_wydanie_2"]; okt = sch["pazdziernik_wydanie_1"]
    jobs = pd.concat([okt, nov], ignore_index=True)
    jobs["okno_do"] = pd.to_datetime(jobs.okno_do); jobs["okno_od"] = pd.to_datetime(jobs.okno_od)
    plan = ev[(ev.rodzaj == "planowane")].copy()
    plan["godziny"] = plan.odbiorcy_za_urzadzeniem * (plan.end - plan.start).dt.total_seconds() / 3600.0
    # match each planned interruption to the job whose window and feeder it sits in
    plan = plan.sort_values("start")
    jobs = jobs.sort_values("okno_od")
    plan = pd.merge_asof(plan, jobs[["okno_od", "okno_do", "id_pracy", "id_linii"]],
                         left_on="start", right_on="okno_od", left_by="linia", right_by="id_linii",
                         direction="backward", tolerance=pd.Timedelta(hours=26))
    ok(plan.id_pracy.notna().mean() > 0.95, "a1.match",
       "%.1f per cent of planned interruptions match a scheduled job" % (100 * plan.id_pracy.notna().mean()))
    jg = plan.dropna(subset=["id_pracy"]).groupby("id_pracy").agg(
        oddzial=("oddzial", "first"), end=("end", "max"), godziny=("godziny", "sum"),
        okno_do=("okno_do", "max"))
    over = jg[jg.end > jg.okno_do]
    ok(len(over) == a1["prac_przekroczonych_total"], "a1.jobs_over_total",
       "%d scheduled jobs ran past their published window" % len(over))
    tot = round(float((over.end - over.okno_do).dt.total_seconds().sum() / 3600.0), 1)
    ok(abs(tot - a1["przekroczenie_godz_total"]) <= 0.6, "a1.hours_over", "%.1f hours" % tot)
    for b, v in a1["godziny_prac_przekroczonych"].items():
        got = round(float(over[over.oddzial == b].godziny.sum()), 1)
        ok(abs(got - v) <= 1.5, "a1.cust_hours.%s" % b, "%.1f customer-hours" % got)

    # ---------------------------------------------------------------- A2
    ppe = pd.read_csv(os.path.join(TGT, "odbiorcy_ppe.csv"), comment="#")
    dup_key = ["nr_ppe", "ts_przyjecia", "opis", "kanal"]
    nld = nl.drop_duplicates(dup_key)
    ok(len(nl) - len(nld) > 1000, "a2.resaves",
       "%d notification rows repeat a row on the same customer, minute and wording" % (len(nl) - len(nld)))
    orph = nld[nld.id_zdarzenia.isna()].copy()
    dev_br = dict(zip(reg.id_urzadzenia, reg.oddzial))
    dev_cu = dict(zip(reg.id_urzadzenia, reg.odbiorcy_za_urzadzeniem))
    ppe_dev = dict(zip(ppe.nr_ppe, ppe.id_urzadzenia))
    orph["dev"] = orph.id_urzadzenia.fillna(orph.nr_ppe.map(ppe_dev))
    orph["br"] = orph.dev.map(dev_br)
    ok(orph.br.notna().all(), "a2.resolved",
       "every unmatched notification resolves to a branch through the device or the customer register")
    g = orph.groupby(["br", "kanal"]).size()
    for k, v in a2["bez_zdarzenia"].items():
        b, ch = k.split("|")
        ok(int(g.get((b, ch), 0)) == v, "a2.%s" % k, "%d" % int(g.get((b, ch), 0)))
    ok(len(orph) == a2["bez_zdarzenia_total"], "a2.total", "%d unmatched notifications" % len(orph))
    cu = orph.dev.map(dev_cu).groupby(orph.br).sum()
    for b, v in a2["odbiorcy_za_urzadzeniami"].items():
        ok(int(cu.get(b, 0)) == v, "a2.customers.%s" % b, "%d" % int(cu.get(b, 0)))

    # ---------------------------------------------------------------- A3
    xl = pd.read_excel(os.path.join(TGT, "sprawozdanie_URE_2026_wstepne_i_korekta.xlsx"),
                       sheet_name=None)
    pre, rev = xl["wstepne_2026"], xl["korekta_1_2026"]
    m = rev.miesiac != "2026-10"
    ratio = float(pre[m].saidi_planowane_min_na_odb.sum() / rev[m].saidi_planowane_min_na_odb.sum())
    ok(abs(ratio - a3["korekta_pazdziernik"]["denominator_ratio"]) < 0.002, "a3.ratio",
       "the untouched months differ by one constant ratio of %.5f" % ratio)
    for v in ["SN", "nN"]:
        a = float(rev[(rev.miesiac == "2026-10") & (rev.poziom == v)].saidi_awaryjne_min_na_odb.iloc[0])
        b = float(pre[(pre.miesiac == "2026-10") & (pre.poziom == v)].saidi_awaryjne_min_na_odb.iloc[0]) / ratio
        ok(abs(round(a - b, 1) - a3["korekta_pazdziernik"]["%s|min" % v]) <= 0.1,
           "a3.min.%s" % v, "%.1f minutes" % (a - b))
        ok(abs(round((a - b) / b * 100, 1) - a3["korekta_pazdziernik"]["%s|pct" % v]) <= 0.2,
           "a3.pct.%s" % v, "%.1f per cent" % ((a - b) / b * 100))

    # ---------------------------------------------------------------- formats read back
    print("\n-- every format read back, each with its positive control")
    pr = pdf_text(os.path.join(TGT, "procedura_PR-07_plan_remediacji.pdf"))
    ok(len(pr) > 800, "fmt.pdf_procedure", "%d characters extracted" % len(pr))
    ok("odbiorco-godziny" in pr.lower(), "fmt.pdf_control",
       "the procedure's own unit sentence is found by this extractor")
    ok("15 listopada 2026" in pr, "fmt.pdf_window", "the window's close is in the procedure")
    ok("awaryjn" in pr.lower() and "planowan" in pr.lower(), "fmt.pdf_population",
       "the procedure states the population")
    ret_pdf = pdf_text(os.path.join(TGT, "sprawozdanie_niezawodnosc_2024_2025.pdf"))
    ok("godzinach" in ret_pdf.lower() and "minutach" in ret_pdf.lower(), "fmt.pdf_return_units",
       "each prior-year table states its own unit")
    ok(not any(c in ret_pdf for c in ["ZAN", "PUS", "GRB", "NIE"]), "fmt.pdf_return_no_branch",
       "the prior-year return carries no branch split")
    ok(len(pd.read_excel(os.path.join(TGT, "program_telemetrii_linii.xlsx"))) > 50, "fmt.xlsx", "read")
    dic = open(os.path.join(TGT, "slownik_danych.md"), encoding="utf-8").read()
    ok("pierwszego zgloszenia" in dic, "fmt.md_control",
       "the dictionary's own definition of the recorded start is found")
    prov = open(os.path.join(TGT, "provenance.md"), encoding="utf-8").read()
    ok(len(prov) > 1200, "fmt.md_provenance", "provenance reads")
    mm = re.search(r"\|\s*(\d+) prac planowanych w oknie", prov)
    ok(mm is not None and int(mm.group(1)) == len(jobs), "doc.provenance_planned",
       "provenance states %s planned works and the schedule holds %d"
       % (mm.group(1) if mm else "no", len(jobs)))
    bl = nl[(nl.kanal == "IVR") & (nl.oddzial.isna())].copy()
    MON = {10: "pazdziernika", 11: "listopada"}
    d0, d1 = bl.ts.min(), bl.ts.max()
    want = "od %d %s do %d %s 2026" % (d0.day, MON[d0.month], d1.day, MON[d1.month])
    ok(want in dic, "doc.ivr_window",
       "the dictionary dates the IVR gap '%s' and the blank rows run %s to %s"
       % (want, d0.date(), d1.date()))
    ok(all(("na_odb" in c) for c in rev.columns if c not in ("miesiac", "poziom")),
       "doc.returns_units", "the return names the unit in every value column")
    pr25 = [float(x) for x in re.findall(r"\n?(\d+\.\d)\s", ret_pdf)]
    ok(any(60.0 < x < 140.0 for x in pr25), "doc.prior_year_level",
       "the prior-year table's annual unplanned minutes per customer sit in the order the window's "
       "own daily rate implies")

    # ---------------------------------------------------------------- gates
    print("\n-- input gates from the bundle alone")
    files = sorted(glob.glob(os.path.join(TGT, "*")))
    ok(len(files) >= 10, "gate.files", "%d files" % len(files))
    ok(len({os.path.splitext(f)[1] for f in files}) >= 3, "gate.formats",
       ",".join(sorted({os.path.splitext(f)[1] for f in files})))
    big = max(sum(1 for _ in open(f, encoding="utf-8", errors="replace")) - 2
              for f in files if f.endswith(".csv"))
    ok(big >= 25000, "gate.big_file", "%d rows" % big)

    print("\n%d assertions, %d failed" % (N[0], len(FAIL)))
    if FAIL:
        print("\n".join(FAIL)); sys.exit(1)


if __name__ == "__main__":
    main()
