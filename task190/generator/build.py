"""Cut the bundle, compute the goldens, write figures.json."""
import json
import os
import shutil
import sys

import asks as A
import deliver
import docs
import golden as G
import pack as PK
import sim
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def cut(target, golden_dir):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    if os.path.isdir(golden_dir):
        shutil.rmtree(golden_dir)
    os.makedirs(golden_dir)

    custs, bycust, rows, truth = sim.build()
    deposits, acct = PK.enrich(custs, rows)

    stats = PK.write_feeds(target, deposits)
    # a reversed deposit and its reversing row are both outside the count (SF11), so the
    # figures are computed on the same rows the bundle leaves standing
    drop = set(stats["reversed_keys"])
    rows = [r for r in rows if (r["cust"], r["date"], round(r["amount"], 2)) not in drop]
    deposits = [d for d in deposits if (d["cust"], d["day"], round(d["amount"], 2)) not in drop]
    _, register_rows = PK.write_register(target, custs, acct)
    PK.write_crosswalk(target, custs, acct)
    PK.write_branches(target)
    PK.write_machine_register(target)
    PK.write_summary(target, deposits)
    npre, nrev, nover = PK.write_ptr(target, deposits)
    PK.write_card(target, custs)
    PK.write_dictionary(target)
    PK.write_manifest(target, stats)
    PK.write_provenance(target, stats)

    till = A.till_log(target)
    A.tolerance_register(target)
    events, ncorr = A.rating_history(target, custs)
    svc = A.service_log(target)
    vrows = A.vendor_rows(svc)

    docs.handbook(target)
    cash_prior = sum(d["amount"] for d in deposits
                     if d["instrument"] == "cash" and d["year"] == "2026")
    ptr_prior = sum(1 for d in deposits if d["instrument"] == "cash" and d["year"] == "2026"
                    and d["amount"] >= W.THRESHOLD)
    docs.prior_report(target, ptr_prior,
                      "$%s million" % ("%.1f" % (cash_prior / 1000000.0)))
    docs.vendor_report(target, vrows)

    # the figures are computed on exactly the rows the bundle ships, cash only
    shipped = [dict(cust=d["cust"], date=d["day"], amount=d["amount"], year=d["year"],
                    planted=d["planted"]) for d in deposits if d["instrument"] == "cash"]
    g = G.compute(custs, bycust, shipped)
    g["largest"] = max(W.SEG_KEYS, key=lambda k: (g["per_seg"][k], -W.SEG_KEYS.index(k)))
    g["a1"] = A.a1_golden(till)
    g["a1_stops"] = A.a1_stops(till)
    g["a2"] = A.a2_golden(events)
    g["a2_all"] = A.a2_golden(events, mode="all")
    g["a2_events"] = A.a2_golden(events, mode="events")
    g["a3"] = A.a3_golden(svc, vrows)
    g["stats"] = stats
    g["ptr"] = dict(preliminary=npre, revised=nrev, at_or_over=nover)
    g["ncorr"] = ncorr
    g["truth"] = {k: truth[("2027", k)] for k in W.SEG_KEYS}
    g["truth_prior"] = {k: truth[("2026", k)] for k in W.SEG_KEYS}
    g["custs"] = custs
    g["register_rows"] = register_rows
    g["deposits_rows"] = deposits
    g["events"] = events
    g["svc"] = svc
    g["vrows"] = vrows
    g["till"] = till
    _out, _tots, _labels = G.convergence(g)
    g["sweep_n"] = len(_labels)
    g["sweep_lo"], g["sweep_hi"] = min(_tots), max(_tots)

    deliver.workbook(os.path.join(golden_dir, "structured_cash_deposits_2027.xlsx"), g)
    deliver.chart(os.path.join(golden_dir, "structured_deposits_by_segment.png"), g)
    return g


PDF_STAMPS = {
    "aml_programme_handbook.pdf": b"D:20260514161000+00'00'",
    "annual_report_extract_2026.pdf": b"D:20260928094500+00'00'",
    "vendor_service_report_2027.pdf": b"D:20270709133000+00'00'",
}
XLSX_STAMPS = {
    "business_customer_register.xlsx": (W.ASSURANCE, W.ASSURANCE, "2027-07-19T07:41:00Z",
                                        "2027-07-19T07:41:00Z",
                                        "Business banking customer register"),
    "cash_tolerance_register.xlsx": ("Brian Simonsen", "Brian Simonsen", "2026-11-18T10:05:00Z",
                                     "2026-12-09T14:22:00Z", "Cash count variance tolerances"),
    "structured_cash_deposits_2027.xlsx": (W.ASSURANCE, W.MLRO, "2027-08-11T09:20:00Z",
                                           "2027-08-14T16:05:00Z",
                                           "Cash deposits split below the threshold 2026/27"),
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
    metadata.write(g, os.path.join(TASK, "metadata.json"))
    if "--no-checks" not in sys.argv:
        import checks
        checks.run(g, target)
    print("cut %d files into target/" % len(os.listdir(target)))
    return g


if __name__ == "__main__":
    main()
