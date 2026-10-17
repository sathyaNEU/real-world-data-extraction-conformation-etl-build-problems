"""Build task264: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch folder
inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task264/generator/build.py              everything
    python3 task264/generator/build.py --out DIR    the pack only, into DIR
    python3 task264/generator/build.py --golden     the pack and the goldens, no checks"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import argparse      # noqa: E402
import calendar      # noqa: E402
import datetime as dt  # noqa: E402
import hashlib       # noqa: E402
import shutil        # noqa: E402
import sys           # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K         # noqa: E402
import docs as D           # noqa: E402
import ops as O            # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
EXPORT = dt.datetime(2027, 1, 8, 9, 12)                 # the finance team's export for the levy papers, GMT
MTIME = calendar.timegm(EXPORT.timetuple())


def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, K.FILES[k])
    T = W.world()
    recs = R.interviews(T)
    m = R.weights_table(T, recs)
    n = {}
    n["wave1"] = R.write_wave1(p("wave1"), recs)
    n["wave2"] = R.write_wave2(p("wave2"), recs)
    n["weights"] = R.write_weights(p("weights"), recs)
    D.write_codebook(p("codebook"))
    n["gazetteer"] = D.write_gazetteer(p("gazetteer"))
    D.write_fieldnote(p("fieldnote"), recs, m)
    D.write_levypapers(p("levypapers"))
    C = T["C"]
    mrows = O.machine_rows(C)
    n["machines"] = O.write_transactions(p("machines"), mrows)
    lines = O.app_lines(C)
    n["app"] = O.write_app(p("app"), lines)
    O.write_tariffs(p("tariffs"))
    crow, ent, ext = O.counts(C)
    n["counts"] = O.write_counts(p("counts"), crow)
    n["assets"] = O.write_assets(p("assets"))
    inv = O.invoices()
    pays = O.payments(inv)
    n["invoices"] = O.write_invoices(p("invoices"), inv)
    others = O.other_receipts(T, mrows, lines)
    n["receipts"] = O.write_receipts(p("receipts"), pays, others)
    n["remittances"] = O.write_remittances(p("remittances"), pays, inv)
    n["payments"] = O.write_supplier_payments(p("payments"), inv)
    n["permits"] = O.write_permits(p("permits"))
    O.write_population(p("population"))
    D.write_manifest(p("manifest"), manifest(n))
    PP.COMPANY = K.AUTH
    PP.normalize_ooxml(p("wave1"), K.PEOPLE["contractor"], K.PEOPLE["contractor"], "2025-10-13T15:42:10Z",
                       "2025-10-14T08:57:31Z", excel=True)
    PP.normalize_ooxml(p("codebook"), K.PEOPLE["contractor"], K.PEOPLE["contractor"], "2025-03-26T10:04:52Z",
                       "2026-04-08T16:20:07Z", excel=True)
    PP.normalize_ooxml(p("app"), "Client Accounts", "Client Accounts", "2026-04-08T07:31:44Z",
                       "2026-04-08T07:33:02Z", excel=True)
    PP.normalize_ooxml(p("tariffs"), K.PEOPLE["finance"], K.PEOPLE["finance"], "2025-01-27T14:10:36Z",
                       "2025-03-19T11:48:23Z", excel=True)
    PP.normalize_ooxml(p("population"), "Research and Intelligence", "Research and Intelligence",
                       "2026-07-01T13:22:05Z", "2026-07-02T09:05:41Z", excel=True)
    PP.normalize_pdf(p("fieldnote"), b"D:20260408171302+01'00'", b"D:20260409092518+01'00'")
    PP.normalize_pdf(p("levypapers"), b"D:20270107154411+00'00'", b"D:20270108090236+00'00'")
    for f in sorted(os.listdir(out)):
        os.utime(os.path.join(out, f), (MTIME, MTIME))
    T.update(recs=recs, m=m, mrows=mrows, lines=lines, counts=crow, ent=ent, ext=ext, inv=inv, pays=pays, n=n)
    return T


def manifest(n):
    F = K.FILES
    return [
        (F["levypapers"], "Item 7 for the meeting of 21 January 2027: the 2027-28 levy requirement, resolution 14/2026, "
                          "the 2026-27 levy", "Finance", "8 January 2027", "3 pages"),
        (F["wave1"], "Visitor survey 2025-26, wave 1 (April to September 2025), one row per interview", K.CONTRACTOR,
         "14 October 2025", n["wave1"]),
        (F["wave2"], "Visitor survey 2025-26, wave 2 (October 2025 to March 2026), one row per interview", K.CONTRACTOR,
         "9 April 2026", n["wave2"]),
        (F["weights"], "Expansion weights for every interview of both waves", K.CONTRACTOR, "9 April 2026", n["weights"]),
        (F["fieldnote"], "How the 2025-26 survey was drawn and weighted", K.CONTRACTOR, "9 April 2026", "2 pages"),
        (F["codebook"], "Field names and codes for both waves", K.CONTRACTOR, "8 April 2026", "3 sheets"),
        (F["gazetteer"], "Settlements in the member councils and the council each lies in", "Parks and GIS",
         "4 March 2025", n["gazetteer"]),
        (F["machines"], "Pay-machine payments, by upload, April 2025 to March 2026 parking", "Car parks back office",
         "6 January 2027", n["machines"]),
        (F["app"], "Parking app statement lines, April 2025 to March 2026", O.APP_PROVIDER, "8 April 2026", n["app"]),
        (F["tariffs"], "Car park charges from 1 April 2025", "Finance", "19 March 2025", "2 sheets"),
        (F["assets"], "Pay machines and vehicle counters, current register", "Parks and GIS", "6 January 2027",
         n["assets"]),
        (F["counts"], "Hourly counts from the car-park vehicle counters, survey year", "Parks and GIS", "6 January 2027",
         n["counts"]),
        (F["invoices"], "Levy invoices issued for 2025-26", "Finance", "6 January 2027", n["invoices"]),
        (F["receipts"], "Credits to the Authority's main account, 1 April 2025 to 7 April 2026 by Date: Date is the day "
                        "the finance system posted the line from the bank's morning statement, Value date the day the "
                        "bank credited the funds", "Finance (cash book export)", "6 January 2027", n["receipts"]),
        (F["remittances"], "Remittance advices received with 2025-26 levy payments", "Finance", "6 January 2027",
         n["remittances"]),
        (F["payments"], "Supplier payment runs, 1 April 2025 to 7 April 2026", "Finance", "6 January 2027",
         n["payments"]),
        (F["permits"], "Annual parking permits sold for 2025-26", "Visitor services", "6 January 2027", n["permits"]),
        (F["population"], "Population estimates for the county's districts, mid-2023 to mid-2025",
         "County council research and intelligence team", "2 July 2026", "3 sheets"),
    ]


def tree_digest(d):
    h = hashlib.sha256()
    for f in sorted(os.listdir(d)):
        h.update(f.encode())
        h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--golden", action="store_true")
    a = ap.parse_args()
    if a.out:
        build(a.out)
        return
    target = os.path.join(TASK, "target")
    T = build(target)
    print("pack:", T["n"])
    import deliver
    deliver.write(target, os.path.join(TASK, "golden"), T)
    if a.golden:
        return
    import checks
    checks.run(target, T)
    r = os.system("python3 %s %s" % (os.path.join(HERE, "verify.py"), target))
    assert r == 0, "verify failed"
    scratch = os.path.join(TASK, ".rebuild")
    build(scratch)
    same = tree_digest(scratch) == tree_digest(target)
    shutil.rmtree(scratch)
    assert same, "second build differs"
    print("rebuild byte-identical")
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp):
        os.remove(zp)
    import zipfile
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(target)):
            zi = zipfile.ZipInfo("target/" + f, date_time=EXPORT.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(target, f), "rb").read())
    print("target.zip cut")


if __name__ == "__main__":
    main()
