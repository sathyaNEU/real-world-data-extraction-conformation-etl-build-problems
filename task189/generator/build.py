"""Cut the bundle, compute the goldens, write figures.json."""
import json
import os
import shutil
import sys

import checks as CK
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
    rows = PK.build_rows()
    PK.write_export(target, rows)
    PK.write_register(target)
    PK.write_crosswalk(target, rows)
    PK.write_abstractions(target)
    PK.write_manifest(target, rows)
    PK.write_flow(target)
    PK.write_sales(target)
    PK.write_batches(target, rows)
    PK.write_programme(target, rows)
    docs.regulations(target)
    docs.method_schedule(target)
    docs.dictionary(target)
    qr = G.report_rows(rows)
    for lab in ("TAS", "KGL"):
        docs.quarterly_report(target, lab, qr)
    # the containers carry their own issue stamps, not the build clock
    PP.normalize_pdf(os.path.join(target, "surface_water_quality_regulations_2019.pdf"),
                     b"D:20240314101500+00'00'", b"D:20240314101500+00'00'")
    PP.normalize_pdf(os.path.join(target, "laboratory_method_schedule.pdf"),
                     b"D:20261116084210+00'00'", b"D:20261116084210+00'00'")
    PP.normalize_pdf(os.path.join(target, "lims_field_dictionary.pdf"),
                     b"D:20260908143355+00'00'", b"D:20260908143355+00'00'")
    PP.normalize_pdf(os.path.join(target, "tirneevin_quarterly_report_2025q3.pdf"),
                     b"D:20260120110744+00'00'", b"D:20260120110744+00'00'")
    PP.normalize_pdf(os.path.join(target, "kilgarron_quarterly_report_2025q3.pdf"),
                     b"D:20260120153012+00'00'", b"D:20260120153012+00'00'")
    PP.normalize_ooxml(os.path.join(target, "monitoring_programme_2025_26.xlsx"),
                       "Emmet McQuillen", "Emmet McQuillen",
                       "2025-03-19T11:04:00Z", "2025-10-02T09:26:00Z",
                       title="Surface water monitoring programme 2025/26", excel=True)
    return rows


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "target")
    rows = cut(tgt)
    g = G.compute(tgt)
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gold = os.path.join(task, "golden")
    os.makedirs(gold, exist_ok=True)
    DL.workbook(os.path.join(gold, "annual_compliance_return_2025_26.xlsx"), g, None)
    DL.chart(os.path.join(gold, "mcpa_compliance_overview.png"), g)
    PP.normalize_ooxml(os.path.join(gold, "annual_compliance_return_2025_26.xlsx"),
                       "Emmet McQuillen", "Katie Enright",
                       "2026-11-17T15:38:00Z", "2026-11-19T10:12:00Z",
                       title="Annual compliance return 2025/26, MCPA", excel=True)
    MD.write(task, g)
    FG.write(os.path.dirname(os.path.abspath(__file__)), g)
    n = CK.run(tgt)
    import verify as VF
    k = VF.run(tgt, os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("files", len(os.listdir(tgt)), "export rows", len(rows))
    print("count", g["count"], g["non_compliant"])
    print("rungs", g["rungs"])
    print("a3", g["a3"])
