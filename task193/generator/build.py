"""Build task193's pack, goldens and figures, then check and verify them."""
import json
import os
import shutil

import numpy as np

import world as W
import pack
import asks
import docs
import golden as G
import deliver
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

    first = W.draw()
    lines, people = pack.dispensings(first)
    kept, rejected, switch_day, keys, new_keys = pack.apply_mess(lines, people)

    counts = {}
    a, b = pack.write_extracts(TGT, kept)
    counts["dispensings_2023_2025.csv"] = a
    counts["dispensings_2025_2026.csv"] = b
    counts["package_index.csv"] = pack.write_package_index(TGT)
    counts["product_register.csv"] = pack.write_product_register(TGT)
    counts["screen_annexes.csv"] = pack.write_annexes(TGT)
    counts["atc_text.csv"] = pack.write_atc_text(TGT)
    counts["register_variable_documentation.csv"] = pack.write_variable_documentation(TGT)
    counts["person_key_crosswalk.csv"] = pack.write_crosswalk(TGT, switch_day, keys, new_keys)
    counts["person_register.csv"] = pack.write_person_register(TGT, people, keys, new_keys,
                                                               switch_day, kept)
    counts["pharmacy_register.csv"] = pack.write_pharmacy_register(TGT, kept)
    counts["holder_register.csv"] = pack.write_holder_register(TGT)
    counts["signal_tracker_export.csv"] = pack.write_tracker(TGT, first)
    counts["submission_exceptions.csv"] = asks.write_exceptions(TGT, rejected)
    counts["pharmacy_submission_log.csv"] = asks.write_submission_log(TGT, kept, rejected)
    n1, n2 = pack.write_distractors(TGT, kept)
    counts["spontaneous_reports_summary.csv"] = n1
    counts["literature_screening_log.csv"] = n2
    docs.standard(TGT)
    docs.fee_schedule(TGT, W.PULL_DAY)
    counts["screen_standard_7_2024.pdf"] = 1
    counts["data_fee_schedule.xlsx"] = 3
    counts["register_release_notes.json"] = pack.write_release_notes(TGT)
    counts["extract_manifest.csv"] = pack.write_manifest(TGT, counts)

    # ---- the screen, from the shipped bundle alone
    rp = G.load(TGT)
    firsts = G.first_receipts(rp[0])
    referred, rows = G.screen(TGT, rp, "perm", firsts)
    crude, crude_rows = G.screen(TGT, rp, "half", firsts)
    routes = {}
    for route in ("perm", "incidence", "pairprod", "even", "half"):
        routes[route] = G.screen(TGT, rp, route, firsts)[0]
    r0, r0rows = G.rung0(TGT)

    # tenths of a defined daily dose per package, read from the shipped index as exact decimals
    ddd_of = {}
    import csv as _csv
    from decimal import Decimal as _D
    with open(os.path.join(TGT, "package_index.csv"), newline="", encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            ddd_of[r["vnr"]] = int(_D(r["ddd_per_pack"]) * 10) if r["ddd_per_pack"] else 0
    a1 = asks.a1_golden(kept, rejected)
    a2 = asks.a2_golden(kept, ddd_of)
    a3 = asks.a3_golden(TGT, firsts, rp[1])

    by_key = {r["key"]: r for r in rows}
    crude_by = {r["key"]: r for r in crude_rows}
    screen_rows = []
    for r in rows:
        pc, mc = r["product"], r["marker"]
        screen_rows.append({
            "product": pc, "brand": W.PNAME[pc], "marker": mc, "marker_treatment": W.MNAME[mc],
            "patients": r["n"], "after": r["after"], "before": r["before"],
            "share_pct": round(100.0 * r["after"] / r["n"], 1) if r["candidate"] else None,
            "expected": round(r["expected"], 1) if r["candidate"] else None,
            "multiple": round(r["ratio"], 2) if r["candidate"] else None,
            "referred": ("yes" if r["referred"] else "no") if r["candidate"] else "below minimum",
            "crude_multiple": round(crude_by[r["key"]]["ratio"], 2) if r["candidate"] else None,
        })
    cands = [r for r in screen_rows if r["multiple"] is not None]
    misses = [r for r in cands if r["referred"] == "no"]
    nearest = max(misses, key=lambda r: r["multiple"])
    g = {
        "referred_count": len(referred),
        "crude_count": len(crude),
        "rung0_count": len(r0),
        "rung2_count": 0,
        "candidate_count": len(cands),
        "screened_count": len(screen_rows),
        "patients_in_extract": len(set(k for k, c in firsts)),
        "referred": [{"product": W.PNAME[k.split("/")[0]], "marker": W.MNAME[k.split("/")[1]],
                      "patients": by_key[k]["n"], "after": by_key[k]["after"],
                      "multiple": round(by_key[k]["ratio"], 2),
                      "crude_multiple": round(crude_by[k]["ratio"], 2)} for k in referred],
        "crude_only": [{"product": W.PNAME[k.split("/")[0]], "marker": W.MNAME[k.split("/")[1]],
                        "multiple": round(by_key[k]["ratio"], 2),
                        "crude_multiple": round(crude_by[k]["ratio"], 2)}
                       for k in sorted(set(crude) - set(referred))],
        "window_only": [{"product": W.PNAME[k.split("/")[0]], "marker": W.MNAME[k.split("/")[1]],
                         "multiple": round(by_key[k]["ratio"], 2),
                         "crude_multiple": round(crude_by[k]["ratio"], 2)}
                        for k in sorted(set(referred) - set(crude))],
        "nearest_miss": {"label": "%s and %s" % (nearest["brand"], nearest["marker_treatment"]),
                         "multiple": nearest["multiple"]},
        "routes": {k: sorted(v) for k, v in routes.items()},
        "screen_rows": screen_rows,
        "a1": a1, "a2": a2, "a3": a3,
        "standard_sections": ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "3.3", "3.4",
                              "4.1", "4.2"],
    }
    rung2 = G.screen(TGT, rp, "half", firsts, edge=60)[0]
    g["rung2_count"] = len(rung2)
    g["rung2"] = rung2

    deliver.workbook(os.path.join(GOLD, "sequence_screen_2027Q1.xlsx"), g)
    deliver.chart(os.path.join(GOLD, "order_shares_by_pair.png"), g)
    PP.normalize_ooxml(os.path.join(TGT, "data_fee_schedule.xlsx"),
                       "Arne Mogensen", "Arne Mogensen",
                       "2026-10-20T07:55:00Z", "2026-10-20T07:55:00Z",
                       title="Statutory data fee schedule", excel=True)
    PP.normalize_ooxml(os.path.join(GOLD, "sequence_screen_2027Q1.xlsx"),
                       "Sine Jakobsen", "Sine Jakobsen",
                       "2026-10-22T09:20:00Z", "2026-10-23T16:05:00Z",
                       title="Prescription-sequence screen, run of October 2026", excel=True)
    PP.normalize_pdf(os.path.join(TGT, "screen_standard_7_2024.pdf"),
                     b"D:20250617114500+02'00'", b"D:20250617114500+02'00'")

    import metadata as MD
    MD.write(TASK, counts)
    import writeup as WU
    WU.write(TASK, g)
    import figures as FG
    FG.write(HERE, g)

    import checks as CK
    import verify as VF
    n = CK.run(TGT, g, first, lines, kept, rejected, people, keys, new_keys, switch_day)
    k = VF.run(TGT, os.path.join(HERE, "figures.json"))
    print("generator assertions %d, independent checks %d" % (n, k))
    print("answer : %d pairs referred of %d candidates (%d screened)"
          % (g["referred_count"], g["candidate_count"], g["screened_count"]))
    print("rungs  : rung0 %d, crude %d, answer %d" % (g["rung0_count"], g["crude_count"],
                                                      g["referred_count"]))
    print("rung2  : %d  %s" % (len(rung2), " ".join(rung2)))
    print("routes : %s" % {k2: len(v) for k2, v in g["routes"].items()})
    print("crude only: %s" % ", ".join("%s+%s" % (x["product"], x["marker"]) for x in g["crude_only"]))
    print("window only: %s" % ", ".join("%s+%s" % (x["product"], x["marker"]) for x in g["window_only"]))
    print("rows   : %s" % {k2: v for k2, v in sorted(counts.items()) if k2.endswith(".csv")})


if __name__ == "__main__":
    main()
