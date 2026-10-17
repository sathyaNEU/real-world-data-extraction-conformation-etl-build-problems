"""Cut the bundle, compute the goldens, write figures.json."""
import json
import os
import shutil
import sys

import asks as A
import deliver
import docs
import golden as G
import mus
import pack as PK
import sim
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def realise(start=None, scale=1.0):
    """The population the authority tests, and the selection run on it.

    The two reversed lines and the credit notes that reverse them are chosen before the selection
    runs, because the authority tests the population after reversals are taken out.
    """
    allrows, runs = PK.enrich(sim.population(scale=scale))
    rng = sim.Rng(991117)
    extra, reversed_refs = PK.credit_notes(allrows, rng)
    dup, dup_run, dup_n = PK.redelivered(allrows, rng)
    rows = [r for r in allrows if r["status"] != "reversed"]
    for i, r in enumerate(rows):
        r["idx"] = i
    lines = [[r["code"], r["amount"], r["cls"], r["taint"]] for r in rows]
    hits, total, nsel = sim.select(lines, W.INTERVAL,
                                  W.RANDOM_START if start is None else start)
    return (allrows, rows, lines, hits, nsel, extra, dup, dup_run, dup_n, reversed_refs, runs)


def cut(target, golden_dir):
    for d in (target, golden_dir):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)

    allrows, rows, lines, hits, nsel, extra, dup, dup_run, dup_n, reversed_refs, runs = realise()
    shipped = allrows + extra + dup

    prows, pruns = PK.enrich(sim.population(year="2025"), year="2025")
    prior = [[r["code"], r["amount"], r["cls"], r["taint"]] for r in prows]
    phits, ptotal, pnsel = sim.select(prior, W.INTERVAL, W.RANDOM_START + 611)

    PK.write_lines(target, shipped, W.YEAR)
    PK.write_lines(target, prows, "2025")
    PK.write_programme_register(target)
    cwpath, cross = PK.write_crosswalk(target, rows + prows)

    # the tested lines, as the schedule records them
    byidx = {r["idx"]: r for r in rows}
    tested = []
    for i, m in hits:
        r = byidx[i]
        payable = round(r["amount"] * (1.0 - r["taint"]), 2)
        tested.append(dict(r, payable=payable,
                           schedule_ref="%s/%s" % (cross[r["sup"]], r["line"]),
                           finding=("rate applied not the rate in the schedule of rates"
                                    if r["taint"] > 0 else "no exception")))
    # one line was queried and re-tested, so the schedule carries it twice. It carries no
    # exception, so counting it twice changes no figure the report states.
    clean = [t for t in tested if t["taint"] == 0]
    clean.sort(key=lambda t: t["schedule_ref"])
    again = dict(clean[len(clean) // 2], finding="re-tested after query, no exception")
    tested.append(again)
    tested.sort(key=lambda t: (t["day"], t["schedule_ref"], t["finding"]))
    cert_n = len([x for x in lines if x[1] >= W.INTERVAL])
    docs.schedule(target, tested, nsel=nsel, ntested=len(set(i for i, _ in hits)),
                  ncert=cert_n)
    # the two-year extract the schedule was pulled from
    ptested = []
    pbyidx = {r["idx"]: r for r in prows}
    for i, m in phits:
        r = pbyidx[i]
        ptested.append(dict(r, payable=round(r["amount"] * (1.0 - r["taint"]), 2),
                            schedule_ref="%s/%s" % (cross[r["sup"]], r["line"])))
    ext = []
    for t in sorted(ptested + tested, key=lambda t: (t["day"], t["schedule_ref"])):
        ext.append([t["day"].isoformat()[:4], t["schedule_ref"], t["code"],
                    t["day"].isoformat(), "%.2f" % t["amount"], "%.2f" % t["payable"]])
    PK.write_csv(target, "testing_schedule_extract_2025_2026.csv",
                 ["testing_year", "schedule_ref", "programme_code", "paid_date",
                  "amount_recorded", "amount_properly_payable"], ext)

    run_truth = A.run_log(target, shipped, runs)
    A.cutoff_register(target)
    events, ncorr = A.risk_history(target, cross)
    cats = {}
    for e in sorted(events, key=lambda e: (e["eff"], e["eid"])):
        if e["status"] == "accepted":
            cats[e["sup"]] = W.RISK_NEW[e["after"]]
    PK.write_supplier_master(target, cross, cats)
    docs.plan(target)
    docs.manual(target)

    # distractors: the funder's claim on a different window, and revenue expenditure
    rng2 = sim.Rng(70213)
    claim = []
    for code, name, value, certs in W.PROGRAMMES:
        claim.append([code, "2025-04-01 to 2026-03-31",
                      "%.2f" % round(value * (0.58 + rng2.u() * 0.2), 2),
                      "%.2f" % round(value * 0.41, 2), "submitted"])
    PK.write_csv(target, "grant_claim_2026.csv",
                 ["programme_code", "claim_period", "eligible_expenditure_eur",
                  "grant_claimed_eur", "claim_status"], claim)
    rev = []
    for m in range(1, 13):
        rev.append(["2026-%02d" % m, "%.2f" % round(1_850_000 + rng2.u() * 420_000, 2),
                    "%.2f" % round(96_000 + rng2.u() * 31_000, 2), 1240 + rng2.below(260)])
    PK.write_csv(target, "revenue_expenditure_summary_2026.csv",
                 ["month", "revenue_expenditure_eur", "of_which_maintenance_eur",
                  "invoices_paid"], rev)

    PK.write_dictionary(target)
    stats = dict(lines=sum(1 for r in shipped if r["delivery"] == 1 and r["status"] != "credit_note"))
    PK.write_manifest(target, stats)
    PK.write_provenance(target, stats)

    # ---- the goldens, computed on exactly the lines the bundle ships -------------
    g = G.compute(lines, hits)
    g["a1"] = A.a1_golden(run_truth)
    g["a1_stops"] = A.a1_stops(run_truth)
    g["a2"] = A.a2_golden(events)
    g["a2_all"] = A.a2_golden(events, "all")
    g["a2_events"] = A.a2_golden(events, "events")
    g["a3"] = A.a3_golden(tested, [r for r in shipped if r["delivery"] == 1])
    g["lines"] = lines
    g["hits"] = hits
    g["shipped"] = shipped
    g["tested"] = tested
    g["events"] = events
    g["ncorr"] = ncorr
    g["run_truth"] = run_truth
    g["nsel"] = nsel
    g["dup_run"], g["dup_n"] = dup_run, dup_n
    g["reversed_refs"] = reversed_refs
    g["cross"] = cross
    g["prior_total_raw"] = mus.projection(prior, phits)
    g["stats"] = stats

    deliver.table(os.path.join(golden_dir, "projected_misstatement_2026.csv"), g)
    deliver.chart(os.path.join(golden_dir, "misstatement_by_population_2026.png"), g)
    return g


PDF_STAMPS = {
    "audit_plan_2026.pdf": b"D:20260204143000+00'00'",
    "audit_manual_part9.pdf": b"D:20251118101500+00'00'",
    "internal_audit_testing_schedule_2026.pdf": b"D:20270226163000+00'00'",
}
XLSX_STAMPS = {
    "supplier_master.xlsx": (W.FINANCE, W.FINANCE, "2027-01-14T08:12:00Z",
                             "2027-01-14T08:12:00Z", "Supplier master"),
    "payment_release_cutoff_register.xlsx": (W.FINANCE, W.FINANCE, "2026-06-24T11:40:00Z",
                                             "2026-06-26T09:05:00Z",
                                             "Payment release cut-off"),
}


def normalise(target, golden_dir):
    import postprocess as PP
    for d in (target, golden_dir):
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if name.endswith(".pdf"):
                s = PDF_STAMPS[name]
                PP.normalize_pdf(p, s, s)
            elif name.endswith(".xlsx"):
                creator, last, created, modified, title = XLSX_STAMPS[name]
                PP.normalize_ooxml(p, creator, last, created, modified, title=title, excel=True)
    stamp = 1500000000
    for d in (target, golden_dir):
        for name in sorted(os.listdir(d)):
            os.utime(os.path.join(d, name), (stamp, stamp))


def main():
    target = os.path.join(TASK, "target")
    golden_dir = os.path.join(TASK, "golden")
    g = cut(target, golden_dir)
    normalise(target, golden_dir)
    import figures
    figures.write(g, os.path.join(HERE, "figures.json"))
    import metadata
    metadata.write(g, os.path.join(TASK, "metadata.json"), target)
    import checks
    checks.run(g, target)
    print("cut %d files into target/" % len(os.listdir(target)))
    return g


if __name__ == "__main__":
    main()
