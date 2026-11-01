"""Writes submission.md from figures.json, so every figure in blocks 1 to 4 is one the generator computed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["Brackenfield", "Hollinmoor", "Kestle Road", "Orrin Falls", "Pellsbury", "Quarry Hill", "Rookwood",
         "Sallow Creek", "Thistlebrook", "Veldane", "Wendmere", "Yarrowby"]


def c(n):
    return "{:,}".format(n)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    pts, ref, sens, grid = f["points"], f["referrals_by_clinic"], f["sensitivity_at_point_pct"], f["grid_pct"]
    nr40, vm = f["nr40_share_pct"], f["validation_by_model_pct"]
    by = {p: sorted(k for k, v in pts.items() if v == p) for p in ("Standard", "Enhanced", "High", "Maximum")}
    assert by["Standard"] == ["Orrin Falls", "Pellsbury", "Quarry Hill", "Sallow Creek", "Thistlebrook", "Wendmere",
                              "Yarrowby"], by
    assert by["High"] == ["Brackenfield", "Hollinmoor", "Kestle Road", "Rookwood", "Veldane"] and not by["Enhanced"]
    std = ", ".join(by["Standard"][:-1]) + " and " + by["Standard"][-1]
    vc = f["validation_by_model_counts"]
    L = []
    a = L.append
    a("## Tags\n")
    a("**Domain:** General Statistics & Data Science (robustness analysis: whether an autonomous diabetic retinopathy "
      "screening AI's validated sensitivity holds at each clinic of a community health center network).")
    a("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    a("## 1. Final Recommendation\n")
    a("**In 2027 run RetinaCheck at Standard at %s, and at High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and "
      "Veldane; on the 2025-26 screenings these points imply %s referrals, within Pellam's capacity of %s.** Not "
      "Standard everywhere: the validation study pooled images from two camera models, and at Standard the AI referred "
      "%d of %d referable patients imaged on the NR-40 against %d of %d on the NR-70, while five clinics screened "
      "%d%% or more of their year on an NR-40. Not Standard at Kestle Road and Veldane, where the register now shows "
      "their NR-70s back: %d%% and %d%% of their year ran on NR-40 loaners."
      % (std, c(f["referrals_total"]), c(f["capacity"]), vc["NR-40"]["Standard"]["referred"],
         vc["NR-40"]["Standard"]["referable"], vc["NR-70"]["Standard"]["referred"], vc["NR-70"]["Standard"]["referable"],
         min(nr40[k] for k in by["High"]), nr40["Kestle Road"], nr40["Veldane"]))
    a("")
    a("## 2. Critical Components\n")
    a("1. Validation study, referable patients the AI referred at Standard, Enhanced, High and Maximum: NR-40 **%d, "
      "%d, %d and %d of %d**; NR-70 **%d, %d, %d and %d of %d**." % tuple(
          [vc["NR-40"][k]["referred"] for k in ("Standard", "Enhanced", "High", "Maximum")] +
          [vc["NR-40"]["Standard"]["referable"]] +
          [vc["NR-70"][k]["referred"] for k in ("Standard", "Enhanced", "High", "Maximum")] +
          [vc["NR-70"]["Standard"]["referable"]]))
    a("2. Share of each clinic's 2025-26 screenings captured on an NR-40: **%d%%** at Brackenfield, Hollinmoor and "
      "Rookwood, **%d%%** Veldane, **%d%%** Kestle Road, **%d%%** Sallow Creek, **%d%%** Pellsbury, **%d%%** Orrin "
      "Falls, **%d%%** Yarrowby, **%d%%** at Quarry Hill, Thistlebrook and Wendmere."
      % (nr40["Rookwood"], nr40["Veldane"], nr40["Kestle Road"], nr40["Sallow Creek"], nr40["Pellsbury"],
         nr40["Orrin Falls"], nr40["Yarrowby"], nr40["Wendmere"]))
    a("3. Weighted by those shares, the five clinics stay under 85% at Enhanced and clear it at High; the other seven "
      "clear it at Standard.")
    a("4. The points chosen for 2027 imply **%s** referrals on the 2025-26 screenings against Pellam's **%s**; High at "
      "every clinic would imply %s.\n" % (c(f["referrals_total"]), c(f["capacity"]), c(f["referrals_high_everywhere"])))
    a("## 3. Step-by-Step Solution\n")
    a("1. Placed every image on its camera: validation images by the protocol's site letters (validation_study_"
      "protocol_2025.pdf) and capture_date, 2025-26 screenings by Site (clinic_directory.csv) and Captured (UTC) moved "
      "to Pacific local date; the camera is the serial the Location History sheet of biomed_asset_register_2026-09-30."
      "xlsx places at the clinic's location that day, its model from the Assets sheet.")
    a("2. From local_validation_study_2025.csv, counted as referable a final_level of moderate NPDR or worse or a "
      "final_dme of Y, and as referred an Ungradable result or a dr_score at or above the point's threshold "
      "(the CAI-03 definitions of referable disease and sensitivity, retinacheck_operating_points.pdf), referred over "
      "referable cases by camera model: NR-40 %d of %d and NR-70 %d of %d at Standard."
      % (vc["NR-40"]["Standard"]["referred"], vc["NR-40"]["Standard"]["referable"],
         vc["NR-70"]["Standard"]["referred"], vc["NR-70"]["Standard"]["referable"]))
    a("3. Weighted each model's proportion at every point by its share of the clinic's screenings in retina_ai_"
      "results_2025-10_2026-09.csv (a screening belongs to the clinic where it was captured): Brackenfield, "
      "Hollinmoor, Kestle Road, Rookwood and Veldane fall short of 85% at Enhanced and clear it at High; the other "
      "seven clear it at Standard.")
    a("4. Took each clinic's least sensitive point at or above 85%% (CAI-03 section 3) and counted the screenings it "
      "would have referred, an Ungradable result or a DR Score at or above its threshold: %s, within the %s in "
      "pellam_reading_agreement_2027.pdf." % (c(f["referrals_total"]), c(f["capacity"])))
    a("5. For the reading center figures, kept the cases in pellam_overread_log_2025-26.csv whose Referral Order is "
      "a REF7734 referral in ehr_retinal_screening_orders_2025-26.csv (the IMG92250 teleretinal reads are not AI "
      "referrals), took each referral order as one referral closed by its last Referable or Not referable grade, "
      "and counted days from its first case's Image Date to the closing grade's Graded (UTC) on the Pacific "
      "calendar, as CAI-03 section 4 states the measure.")
    a("6. For the camera faults, took the retinal camera tickets in biomed_service_tickets_2025-26.csv, ended each "
      "outage when the Location History moved the next camera into the clinic (not at the ticket's Closed date), "
      "and counted the weekdays after the fault day with no screening in the result export (the fault day itself "
      "had screenings before the camera failed).")
    a("7. Recommended Standard at seven clinics and High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and "
      "Veldane.\n")
    a("## 4. Deliverable Answers\n")
    a("### ai_operating_points_2027.xlsx\n")
    a("1. 2027 operating point by clinic:")
    for k in ORDER:
        a("   - %s: %s" % (k, pts[k]))
    a("2. Referrals each clinic's point implies on the 2025-26 screenings, whole counts:")
    for k in ORDER:
        a("   - %s: %s" % (k, c(ref[k])))
    a("3. Network: %s referrals against Pellam's 2027 capacity of %s, within capacity." %
      (c(f["referrals_total"]), c(f["capacity"])))
    a("4. AI referrals Pellam read from the 2025-26 screenings, whole counts, and the share whose closing grade is "
      "Referable, whole per cent:")
    for k in ORDER:
        a("   - %s: %s read, %d%%" % (k, c(f["reads_by_clinic"][k]), f["confirmed_pct_by_clinic"][k]))
    a("5. Average days from screening to Pellam's closing grade by quarter of screening, one decimal:")
    for q in ("Oct-Dec 2025", "Jan-Mar 2026", "Apr-Jun 2026", "Jul-Sep 2026"):
        a("   - %s: %.1f" % (q, f["days_by_quarter"][q]))
    a("6. Clinic days with no AI screening after each camera fault in the reference year, whole days:")
    for k, v in sorted(f["downtime"].items(), key=lambda kv: kv[0].split()[-1]):
        a("   - %s: %d" % (k, v))
    a("")
    a("### operating_points_2027_leadership.pptx\n")
    a("1. Heatmap on the slide with one row per clinic and one column per vendor point (Standard, Enhanced, High, Maximum), each "
      "cell the clinic's estimated sensitivity and each clinic's point for 2027 outlined: Standard at seven clinics, "
      "High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and Veldane.")
    text = "\n".join(L) + "\n"
    assert "—" not in text and "–" not in text
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()
