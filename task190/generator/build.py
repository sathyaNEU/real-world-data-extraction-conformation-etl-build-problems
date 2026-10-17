"""Cut the bundle, compute the goldens, write figures.json."""
import os
import shutil
import sys

import deliver as DL
import docs
import figures as FG
import golden as G
import metadata as MD
import pack as PK
import postprocess as PP


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    cs = PK.all_cases()
    case_rows = PK.write_cases(target, cs)
    alert_rows = PK.write_alerts(target, case_rows)
    PK.write_lines(target)
    PK.write_crosswalk(target, case_rows, alert_rows)
    PK.write_backlog(target)
    PK.write_ledger(target)
    versions = PK.write_lists(target)
    PK.write_matches(target, versions)
    PK.write_branches(target)
    PK.write_training(target)
    PK.write_closed_days(target)
    PK.write_base(target)
    PK.write_manifest(target, case_rows, alert_rows)
    docs.framework(target)
    docs.handbook(target)
    docs.dictionary(target)
    docs.contract(target)
    PP.normalize_pdf(os.path.join(target, "financial_crime_framework.pdf"),
                     b"D:20261119164500+00'00'", b"D:20261119164500+00'00'")
    PP.normalize_pdf(os.path.join(target, "investigation_handbook.pdf"),
                     b"D:20260803112000+00'00'", b"D:20260803112000+00'00'")
    PP.normalize_pdf(os.path.join(target, "extract_dictionary.pdf"),
                     b"D:20270118091500+00'00'", b"D:20270118091500+00'00'")
    PP.normalize_pdf(os.path.join(target, "contract_register.pdf"),
                     b"D:20260614150000+00'00'", b"D:20260614150000+00'00'")
    PP.normalize_ooxml(os.path.join(target, PK.FILES["base"]), "Bruce Wheeler", "Bruce Wheeler",
                       "2027-01-12T08:40:00Z", "2027-01-18T07:55:00Z",
                       title="Customers by business line", excel=True)
    return case_rows, alert_rows


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    cut(tgt)
    g = G.compute(tgt)
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gold = os.path.join(task, "golden")
    os.makedirs(gold, exist_ok=True)
    DL.workbook(os.path.join(gold, "review_placement_2027.xlsx"), g)
    DL.chart(os.path.join(gold, "placement_overview.png"), g)
    PP.normalize_ooxml(os.path.join(gold, "review_placement_2027.xlsx"), "Bruce Wheeler", "Kayla Burr",
                       "2027-01-21T16:05:00Z", "2027-01-23T09:30:00Z",
                       title="Specialist review placement 2027", excel=True)
    MD.write(task, g)
    FG.write(os.path.dirname(os.path.abspath(__file__)), g)
    import checks as CK
    import verify as VF
    n = CK.run(tgt)
    k = VF.run(tgt, os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("covered:", g["covered"], "| just misses:", g["just_misses"])
    for k, v in g["rungs"].items():
        print("  %-30s %s" % (k, v))
    print()
    for n, o in g["assess"].items():
        print("  %-24s closed=%4d lam=%5.2f W=%5.1f exp=%6.1f cohort=%6.1f conf2q=%4d"
              % (n, o["closed_cases"], o["arrivals_a_month"], o["months_unseen"],
                 o["expected_carrying"], o["cohort_estimate"], o["confirmed_two_quarters"]))
