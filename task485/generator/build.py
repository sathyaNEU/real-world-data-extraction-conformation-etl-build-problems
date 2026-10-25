"""Builds task485's pack into target/ and the golden deliverables into golden/, writes generator/figures.json, and
cuts target.zip; two runs are byte-identical.

    python3 task485/generator/build.py          # the whole build
    python3 task485/generator/build.py pack     # the pack only
"""
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import ash as A            # noqa: E402
import coal                # noqa: E402
import golden as G         # noqa: E402
import reagent             # noqa: E402
import returns             # noqa: E402
import tests               # noqa: E402
import world as W          # noqa: E402

NAMES = dict(
    note="so2_order_2027_schedule_note.pdf", guidance="so2_inventory_guidance_2026.pdf",
    permits="permitted_boilers_register_2026.xlsx", guarantees="scrubber_guarantee_schedules.pdf",
    coal="coal_deliveries_2026.csv", sup_cust="coal_supplier_customers.csv", returns="boiler_returns_2026.xlsx",
    tickets="limestone_tickets_2026.csv", certs="limestone_certificates_2026.xlsx",
    northfield="scrubber_tests_2026_iverstow.pdf", ashgrove="scrubber_tests_2026_jarrness.pdf",
    moorside="whinmoss_invoice_lines_2026.xlsx", tolland="carnhope_jobs_2026.csv", greave="pellrigg_dockets_2026.xlsx",
    xref="ash_contractor_customers.csv", ambient="npa_ambient_so2_2026.csv",
    national="national_coal_consumption_2025.json")
GOLD = dict(workbook="sulphur_dioxide_order_schedule_2027.xlsx", chart="boiler_sulphur_dioxide_2026.png")
MIN = "Ministry of the Environment"
OWNERS = {
    "permits": dict(creator="Permitting Team", last_by="Permitting Team", created="2019-05-13T08:52:00Z",
                    modified="2027-01-06T10:37:00Z", company=MIN),
    "returns": dict(creator="AQD Returns", last_by="AQD Returns", created="2026-04-30T14:05:00Z",
                    modified="2027-02-02T16:21:00Z", company=MIN),
    "certs": dict(creator="AQD Returns", last_by="AQD Returns", created="2026-01-19T09:12:00Z",
                  modified="2027-01-14T11:48:00Z", company=MIN),
    "moorside": dict(creator="Whinmoss Waste Haulage", last_by="Accounts", created="2027-01-11T13:02:00Z",
                     modified="2027-01-11T13:09:00Z", company="Whinmoss Waste Haulage Ltd"),
    "greave": dict(creator="Pellrigg and Sons", last_by="Office", created="2026-01-05T07:58:00Z",
                   modified="2027-01-08T17:26:00Z", company="Pellrigg and Sons Haulage"),
}
STAMPS = {"note": b"D:20270208101500+00'00'", "guidance": b"D:20261102093000+00'00'",
          "guarantees": b"D:20240314112000+00'00'"}


def t(k):
    return os.path.join(TARGET, NAMES[k])


def truth():
    """the clean truth: the world day by day, every record cut from it, and every route computed from the records"""
    import pack as PK
    w = W.build()
    coal.deliveries(w)
    W.flows(w)
    reagent.silos(w)
    tests.run(w)
    returns.build(w)
    returns.permits(w)
    prod = A.produce(w, w.lots)
    jobs = A.collections(w, prod)
    A.exports(w, jobs)
    PK.customer_codes(w)
    rt = G.routes(w, w.returns, w.tickets, w.tests, w.permits)
    return dict(w=w, rt=rt, jobs=jobs, ash=A.golden(jobs))


def pack(tr=None):
    import docs as DOC
    import pack as PK
    import postprocess as PP
    for d in (TARGET, GOLDEN):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    tr = tr or truth()
    w = tr["w"]
    n = {}
    n["permits"] = PK.permits_xlsx(t("permits"), w)
    n["coal"] = PK.coal_csv(t("coal"), w)
    n["sup_cust"] = PK.supplier_customers_csv(t("sup_cust"), w)
    n["returns"] = PK.returns_xlsx(t("returns"), w)
    n["tickets"] = PK.tickets_csv(t("tickets"), w)
    n["certs"] = PK.certificates_xlsx(t("certs"), w)
    n["moorside"], n["tolland"], n["greave"] = PK.ash_files(
        dict(moorside=t("moorside"), tolland=t("tolland"), greave=t("greave"), xref=t("xref")), w)
    n["ambient"] = PK.ambient_csv(t("ambient"))
    n["national"] = PK.national_coal_json(t("national"))
    DOC.order_note(t("note"))
    DOC.guidance(t("guidance"))
    DOC.guarantees(t("guarantees"), w)
    issued = {k: DOC.test_report(t(k), w, lab) for k, lab in
              (("northfield", "Iverstow Emission Testing"), ("ashgrove", "Jarrness Stack Testing"))}
    for k in OWNERS:
        PP.normalize_ooxml(t(k), excel=True, **OWNERS[k])
    stamps = dict(STAMPS)
    for k, d in issued.items():
        stamps[k] = ("D:%s143000+00'00'" % d.strftime("%Y%m%d")).encode()
    for k, stamp in stamps.items():
        PP.normalize_pdf(t(k), stamp, stamp)
    tr["issued"] = issued
    return tr, n


def gpath(k):
    return os.path.join(GOLDEN, GOLD[k])


def main():
    tr, n = pack()
    import goldfiles as GF
    import postprocess as PP
    figs = GF.write(gpath, tr)
    PP.normalize_ooxml(gpath("workbook"), "Maria Burgess", "Maria Burgess", "2027-02-09T09:14:00Z",
                       "2027-02-17T15:52:00Z", title="Sulphur Dioxide Order 2027: schedule of listed boilers",
                       excel=True, company=MIN)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    import writeup
    writeup.main()
    import metadata
    metadata.main()
    cut_zip()
    print("built: %d files in target/, %d in golden/" % (len(os.listdir(TARGET)), len(os.listdir(GOLDEN))))
    print(json.dumps(n))
    return tr


def cut_zip():
    """Each file keeps the date its source produced it (metadata.SOURCES) and a working-hours time of its own."""
    import hashlib
    import metadata
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for nm in sorted(os.listdir(TARGET)):
            y, mo, d = (int(x) for x in metadata.SOURCES[nm][1].split("-"))
            h = int(hashlib.md5(nm.encode()).hexdigest(), 16)
            zi = zipfile.ZipInfo(nm, date_time=(y, mo, d, 7 + h % 11, (h // 11) % 60, ((h // 660) % 30) * 2))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, nm), "rb").read())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        tr, n = pack()
        print(json.dumps(n, indent=1))
    else:
        main()
