"""Build task193's pack, goldens and figures, then check and verify them."""
import collections
import json
import os
import shutil

import world as W
import sim
import pack
import asks
import docs
import golden as G
import deliver
import figures as FG
import metadata as MD
import postprocess as PP

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")


def main():
    for d in (TGT, GOLD):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)

    cases = sim.draw()
    subs = pack.submissions(cases)
    exc = asks.exceptions(cases)

    counts = {}
    counts["spontaneous_reports_extract.csv"] = pack.write_extract(TGT, subs)
    counts["report_master.csv"] = pack.write_master(TGT, subs)
    counts["product_register.csv"] = pack.write_register(TGT)
    counts["reaction_dictionary.csv"] = pack.write_dictionary(TGT)
    counts["product_information_listed.csv"] = pack.write_listed(TGT)
    counts["closed_assessments_register.csv"] = pack.write_closed(TGT, cases)
    counts["campaign_vaccination_log.csv"] = pack.write_campaign(TGT)
    counts["coding_exceptions.csv"] = asks.write_exceptions(TGT, exc)
    counts["channel_totals.csv"] = asks.write_channel_totals(TGT, subs, exc)
    counts["holder_submissions.csv"] = asks.write_holder_submissions(TGT, subs, exc)
    n1, n2 = asks.write_distractors(TGT)
    counts["literature_screening_log.csv"] = n1
    counts["enquiry_log.csv"] = n2
    asks.write_agreements(TGT)
    docs.standard(TGT)

    cs, listed = G.load(TGT)
    npr, a = G.tally(cs)
    crude = G.run(npr, a, listed)
    corr = G.run(npr, a, listed, drop=(W.DOMINANT,))
    sc = set((x["code"], x["reaction"]) for x in crude)
    su = set((x["code"], x["reaction"]) for x in corr)
    docs.capacity(TGT, len(crude) + 3)
    counts["run_inventory.json"] = pack.write_manifest(TGT, counts)

    masked = sorted(su - sc)
    crude_of = {}
    for code, reaction in masked:
        crude_of[(code, reaction)] = G.measure(npr, a, code, reaction)[0]
    g = {
        "taken_forward": len(corr),
        "crude_count": len(crude),
        "rung0_count": len(G.rung0(TGT, listed)),
        "ror_count": len(G.run(npr, a, listed, stat="ror")),
        "slots_left": W.CAPACITY - len(corr),
        "capacity": W.CAPACITY,
        "cases": len(cs),
        "dominant_share": round(100.0 * npr[W.DOMINANT] / len(cs), 1),
        "nearest_to_threshold": round(min(abs(x["prr"] - W.PRR_MIN) for x in corr), 2),
        "masked_pairs": [list(p) for p in masked],
        "campaign_share": {r: round(100.0 * a[(W.DOMINANT, r)] /
                                    sum(v for (c, rr), v in a.items() if rr == r), 1)
                           for r in sorted(W.CAMPAIGN)},
        "signals": [{"code": x["code"], "reaction": x["reaction"], "reports": x["reports"],
                     "prr": round(x["prr"], 2), "chi": round(x["chi"], 1),
                     "prr_crude": round(crude_of.get((x["code"], x["reaction"]),
                                                     G.measure(npr, a, x["code"], x["reaction"])[0]), 2)}
                    for x in corr],
        "standard_paragraphs": ["2.1", "2.2", "2.3", "2.4", "3.1", "3.2", "3.3", "3.4",
                                "4.1", "4.2"],
        "age_bands": W.AGE_BANDS + ["not stated"],
        "a1_channels": G.ask_channels(TGT),
        "a2_holders": G.ask_holders(TGT),
        "a3_cells": G.ask_cells(TGT, cs),
    }

    deliver.workbook(os.path.join(GOLD, "signal_list_2026Q3.xlsx"), g)
    deliver.chart(os.path.join(GOLD, "signal_overview.png"), g)
    PP.normalize_ooxml(os.path.join(TGT, "data_agreement_schedule.xlsx"),
                       "Malthe Danielsen", "Malthe Danielsen",
                       "2026-09-11T08:40:00Z", "2026-09-11T08:40:00Z",
                       title="Data agreement schedule", excel=True)
    PP.normalize_ooxml(os.path.join(GOLD, "signal_list_2026Q3.xlsx"),
                       "Cirkeline Gregersen", "Cirkeline Gregersen",
                       "2026-10-08T15:20:00Z", "2026-10-09T09:05:00Z",
                       title="Signals of disproportionate reporting, 2026 Q3", excel=True)
    PP.normalize_pdf(os.path.join(TGT, "signal_standard.pdf"),
                     b"D:20251218103000+01'00'", b"D:20251218103000+01'00'")
    PP.normalize_pdf(os.path.join(TGT, "assessment_capacity_report.pdf"),
                     b"D:20260918091500+02'00'", b"D:20260918091500+02'00'")

    g["submissions"] = len(subs)
    MD.write(TGT, counts)
    import writeup as WU
    WU.write(TASK, g)
    FG.write(HERE, g)

    import checks as CK
    import verify as VF
    n = CK.run(TGT, g)
    k = VF.run(TGT, os.path.join(HERE, "figures.json"))
    print("generator assertions", n, "independent checks", k)
    print("answer  : %d pairs taken forward, %d slots left of %d"
          % (g["taken_forward"], g["slots_left"], W.CAPACITY))
    print("rungs   : raw %d, whole database %d, odds ratio %d, answer %d"
          % (g["rung0_count"], g["crude_count"], g["ror_count"], g["taken_forward"]))
    print("masked  : %s" % ", ".join("%s %s" % (c, r) for c, r in masked))
    print("dominant: %.1f per cent of the quarter's reports" % g["dominant_share"])
    print("campaign: %s" % g["campaign_share"])


if __name__ == "__main__":
    main()
