"""Cut the bundle, compute the goldens, write figures.json."""
import os
import shutil
import sys

import asks
import docs
import golden as G
import pack as PK
import panel
import postprocess as PP
import sim
import world as W


def cut(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    qs = sim.calibrate(W.WORST_WINDOW)
    minutes, rollup = panel.build(qs)
    kept, dropped = PK.write_panel(target, minutes)
    PK.write_rollup(target, rollup + PK.rollup_from_panel(kept))
    PK.write_register(target)
    PK.write_maintenance(target)
    PK.write_health(target, dropped)
    asks.write_edge(target)
    asks.write_commitments(target)
    asks.write_sessions(target)
    asks.write_incidents(target)
    asks.write_distractors(target)
    PK.write_plan(target)
    docs.framework(target)
    docs.standard(target)
    docs.dictionary(target)
    docs.bulletin(target, [["2025Q1", "5,980", "41.2", "0.91"], ["2025Q2", "6,040", "39.8", "0.88"],
                           ["2025Q3", "6,015", "38.9", "0.90"], ["2025Q4", "6,105", "43.1", "0.94"],
                           ["2026Q1", "6,120", "44.6", "0.97"], ["2026Q2", "6,190", "42.0", "0.89"],
                           ["2026Q3", "6,165", "41.3", "0.87"], ["2026Q4", "6,240", "45.8", "0.93"],
                           ["2027Q1", "6,275", "46.9", "0.92"]])
    PP.normalize_pdf(os.path.join(target, "network_capacity_framework.pdf"),
                     b"D:20261014101500+00'00'", b"D:20261014101500+00'00'")
    PP.normalize_pdf(os.path.join(target, "delivered_quality_standard.pdf"),
                     b"D:20260622143000+00'00'", b"D:20260622143000+00'00'")
    PP.normalize_pdf(os.path.join(target, "telemetry_dictionary.pdf"),
                     b"D:20270412090000+00'00'", b"D:20270412090000+00'00'")
    PP.normalize_pdf(os.path.join(target, "published_quarterly_quality_report.pdf"),
                     b"D:20270409113000+00'00'", b"D:20270409113000+00'00'")
    PP.normalize_ooxml(os.path.join(target, PK.FILES["plan"]), "Amelia Jekel", "Amelia Jekel",
                       "2027-01-06T09:10:00Z", "2027-04-02T16:20:00Z",
                       title="Interconnect capacity plan", excel=True)
    PK.write_manifest(target)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    cut(tgt)
    g = G.compute(tgt)
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gold = os.path.join(task, "golden")
    os.makedirs(gold, exist_ok=True)
    import deliver as DL
    import figures as FG
    import metadata as MD
    DL.workbook(os.path.join(gold, "augment_decision_2027Q1.xlsx"), g)
    DL.chart(os.path.join(gold, "shortfall_overview.png"), g)
    PP.normalize_ooxml(os.path.join(gold, "augment_decision_2027Q1.xlsx"),
                       "Amelia Jekel", "Rick Claassen",
                       "2027-04-08T11:05:00Z", "2027-04-10T15:40:00Z",
                       title="Interconnect augment decision 2027Q1", excel=True)
    MD.write(task, g)
    FG.write(os.path.dirname(os.path.abspath(__file__)), g)
    import checks as CK
    import verify as VF
    n = CK.run(tgt)
    k = VF.run(tgt, os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("decided : %s %s %s  %.0f kbps" % (g["decided_port"], g["decided_evening"],
                                             g["decided_window"], g["decided_shortfall"]))
    print("record  : %.0f kbps in %s; rank %d of 9" % (g["record_shortfall"], g["record_quarter"],
                                                       g["rank_of_nine"]))
    print("call    : fund %s" % g["fund"])
    print("rung 0  : %s %.0f kbps (maintenance kept)" % (g["rung0_port"], g["rung0_shortfall"]))
    print("rung 2  : %s mean %.1f kbps, next %.1f" % (g["rung2_port"], g["rung2_mean"],
                                                      g["rung2_next"]))
    print("closest : %s at %d kbps" % (g["closest_port"], g["closest_shortfall"]))
    print("quarters:", g["quarterly_worst"])
    print("a1      :", {k: (v["percentile_mbps"], v["commitment_mbps"], v["overage_eur"])
                        for k, v in g["a1_peers"].items()})
    print("a2      :", {k: (v["sessions"], v["rebuffered_pct"]) for k, v in g["a2_builds"].items()})
    print("a3      :", g["a3_incidents"])
