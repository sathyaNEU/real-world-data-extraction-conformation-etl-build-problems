"""Emits submission.md and generator/figures.json from target/ (every figure computed, none typed)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402

f = R.fmt


def emit(tdir, task_dir):
    res = R.compute(tdir)
    g = res["raw"]["call"]
    rg = res["raw"]["rungs"]
    info = res["raw"]["info"]
    nat = g["nat"]
    V = g["V"]
    record = sum(V[n] for n in A.REACH_NAMES) + sum(V[b] for b in A.BERTH_NAMES)
    kvals = sorted(info["k"].values())
    figs = {}

    def put(key, text):
        figs[key] = text
        return text

    total = put("call.total_m3", f(res["total"]))
    unr = put("call.total_unrounded_m3", f(round(g["total"])))
    r0 = put("rung.R0_carry", f(R.nearest(rg["R0 carry"], 50000)))
    r1 = put("rung.R1_depth_ratio", f(R.nearest(rg["R1 depth ratio"], 50000)))
    r2 = put("rung.R2_trapping_efficiency", f(R.nearest(rg["R2 trapping efficiency"], 50000)))
    rec = put("component.record_mean_m3", f(round(record)))
    nb = {n: put("component.natural_bed.%s" % n, "%.2f" % nat[n]) for n in A.REACH_NAMES}
    k0 = put("step.k_low", "%.3f" % kvals[0])
    k1 = put("step.k_high", "%.3f" % kvals[-1])
    put("constant.depth_now", "12.3")
    put("constant.depth_new", "14.3")
    put("constant.odn", "%.2f" % P.CD_BELOW_ODN)
    parts = {p: put("answer.part.%s" % p, f(res["parts"][p])) for p in R.PARTS}
    a = {(s, q): put("answer.placed.%s.Q%d" % (s, q), f(res["a"][(s, q)])) for s in R.SITES for q in (1, 2, 3, 4)}
    b = {(n, m): put("answer.metal.%s.%s" % (n, m), "%.2f" % res["b"][(n, m)]) for n in A.REACH_NAMES for m in R.METALS}

    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences, hydrology and flood frequency (sedimentation of a maintained estuary channel).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Year 1 of the 2027-30 maintenance contract should be tendered at %s m3 in situ.** Each reach and the turning basin "
             "gather sediment in proportion to how far their bed is held below the natural bed beside them, so holding them two "
             "metres deeper raises each one's 2016-17 to 2025-26 infill by two metres over that depth. Not %s m3, the record "
             "carried at 12.3 m. Not %s m3 from scaling by the held depths, 14.3 over 12.3, nor %s m3 from a trench trapping "
             "efficiency: in the record each part's infill per square metre follows its depth below the natural bed, which "
             "neither reproduces." % (total, r0, r1, r2))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Natural bed beside each part, below chart datum: Outer Channel **%s m**, Fend Roads **%s m**, Middle Reach **%s m**, "
             "Inner Reach **%s m**, Turning Basin **%s m**." % tuple(nb[n] for n in A.REACH_NAMES))
    L.append("2. Mean in situ maintenance over the licence years 2016-17 to 2025-26: **%s m3** a year." % rec)
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read deepening_2027_maintenance_planning_basis.docx and notice_to_mariners_03-2026.pdf: from 1 October 2027 the four "
             "reaches and the turning basin are held at 14.3 m below chart datum (12.3 m now), the berth pockets keep their depths and "
             "North Quay Berth 2 stays out of maintenance.")
    L.append("2. Averaged maintenance_dredging_certificates_2016-2026.xlsx by area over October 2016 to September 2026, the 2021 codes "
             "read through its Area codes sheet and the re-issued October 2024 Middle Reach certificate in place of the original: "
             "%s m3 a year." % rec)
    L.append("3. Converted seaward_channel_surveys_2023-2026.csv to depth below chart datum (chart datum 2.90 m below ODN), placed "
             "every cell of both survey files against the notice's centreline, and took the mean of the cells 50 to 300 m outside each "
             "maintained width (the basin's open south side): the natural beds of component 1.")
    L.append("4. Divided each part's yearly infill per square metre by its depth below the natural bed: %s to %s a year per metre, "
             "one coefficient, while the held depth is 12.3 m in every part." % (k0, k1))
    L.append("5. Raised each reach and the basin by two metres over its depth below the natural bed, mean times (14.3 less bed) over "
             "(12.3 less bed), and added the berth pockets at their means: %s m3, %s to the nearest 50,000." % (unr, total))
    L.append("6. Placed each 2025-26 load in dunmarsh_load_log_2023-2026.csv at the site whose corners in "
             "marine_licence_L2021-00317_v2.pdf hold its dump position, took the Fend Endeavour's January to March dry solids from "
             "FE_dry_solids_revision_20260330.csv by trip reference (vessel, local date, trip of the day), the Maasbank's from the "
             "licence formula, divided by the loading area's dry-solids fraction from the latest campaign completed before the month "
             "(sediment_sampling_2025-2026.xlsx) and summed by local quarter: the placements in block 4.")
    L.append("7. Put each 2026 sample in aldern_results_FEN26.csv in the area where the field log places it, averaged each QA "
             "duplicate with the primary at its position and time, converted the second batch's mercury from micrograms, and "
             "averaged by area: the means in block 4.")
    L.append("8. Recommended tendering year 1 at %s m3 in situ." % total)
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### fendmouth_maintenance_2027-28.xlsx")
    L.append("")
    L.append("1. Year 1 quantity, 1 October 2027 to 30 September 2028: %s m3 in situ." % total)
    L.append("2. Each part's year 1 volume, nearest 20,000 m3:")
    for p in R.PARTS:
        label = p if p != "Berth pockets" else "Berth pockets (North Quay Berths 1 and 3, Container Terminal Berth 5)"
        L.append("   - %s: %s m3" % (label, parts[p]))
    L.append("3. Wet tonnes placed in the licence year to 30 September 2026, nearest 1,000 t:")
    for s in R.SITES:
        for q in (1, 2, 3, 4):
            L.append("   - %s, %s: %s t" % (s, R.QUARTERS[q], a[(s, q)]))
    L.append("4. Mean concentration in the 2026 samples, mg/kg dry weight:")
    for n in A.REACH_NAMES:
        L.append("   - %s: cadmium %s, mercury %s, lead %s, copper %s" % ((n,) + tuple(b[(n, m)] for m in R.METALS)))
    L.append("")
    L.append("### placements_2025-26.svg")
    L.append("")
    L.append("5. One stacked bar for each month from October 2025 to September 2026, split into Fend Spit and Wenning Deep, each "
             "month's total in thousand wet tonnes above its bar.")
    L.append("")
    text = "\n".join(L)
    assert "—" not in text and "–" not in text
    with open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(figs, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return res, figs


if __name__ == "__main__":
    emit(sys.argv[1], sys.argv[2])
