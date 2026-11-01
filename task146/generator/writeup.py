"""task146 architecture 3: submission.md and metadata.json, every figure from figures.json."""
import json

import golden as GD
import pack as PK

ARM = GD.ARM_NAME


def submission(fig, path):
    e, s, p2 = fig["phase3_expected"], fig["phase3_side"], fig["phase2b_arm_pasi75"]
    mw = fig["mean_weight_kg"]
    ap, ai = fig["ask_pasi"], fig["ask_itch"]
    L = ["## Tags", "",
         "**Domain:** Biomedical & Clinical Research (dose-response and PK/PD modelling: a phase 3 dose for a "
         "monoclonal antibody in plaque psoriasis).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "",
         "## 1. Final Recommendation", "",
         "**Take HB-231 200 mg into phase 3: it is the lowest candidate dose whose expected week-16 PASI 75 response "
         "in the phase 3 population is at least 70 per cent.**",
         "Not 100 mg, whose VELA-2 arm reached %.1f per cent: the VELA-3 candidates weigh more (%.1f kg against "
         "%.1f kg), HB-231's troughs fall with body weight and response follows the trough, so 100 mg falls under "
         "the bar in the phase 3 population. Not 50 mg, under the bar in both." % (p2["100"], mw["phase3"],
                                                                                    mw["phase2b"]), "",
         "## 2. Critical Components", "",
         "1. Expected week-16 PASI 75 response in the phase 3 population against the 70 per cent bar: 50 mg "
         "**%s it**, 100 mg **%s it**, 200 mg **%s it**." % (s["50"], s["100"], s["200"]),
         "2. HB-231's week-16 trough concentration falls with body weight: clearance rises about in proportion to "
         "weight (exponent **%.1f** in the population PK model of the VELA-2 troughs)." % fig["weight_exponent"],
         "3. Mean body weight: VELA-2 patients **%.1f kg**, VELA-3 feasibility candidates **%.1f kg** (US weights "
         "converted from pounds)." % (mw["phase2b"], mw["phase3"]), "",
         "## 3. Step-by-Step Solution", "",
         "1. Study day 1 is each patient's first dose in the dosing log; PASI baseline is the last assessment on or "
         "before it (the Finnish sites' \"Day 1\" record, not their \"Baseline\" screening record).",
         "2. Week-16 PASI 75 and PASI 90 under the SAP's composite: rescue (ATC D07AC or D07AD, or phototherapy) "
         "started after the first dose and on or before the week-16 assessment, or no week-16 PASI, is "
         "non-response.",
         "3. Troughs: the Lund laboratory's ng/mL divided by 1,000, below-limit samples dropped; log concentration "
         "per mg regressed on visit and log(weight/85).",
         "4. Each active-arm patient's typical week-16 trough from dose and weight; logistic regression of the "
         "composite PASI 75 on its log.",
         "5. Each feasibility candidate's typical trough at 50, 100 and 200 mg (pounds times 0.45359237); the "
         "fitted response averaged over the candidates gives the expected response per dose.",
         "6. The lowest dose at or above 70 per cent is 200 mg.",
         "7. Itch: entries placed on the local diary day (after midnight and before 03:00 to the evening before); "
         "weekly means over study days -7 to -1, 78 to 84 and 106 to 112 with at least four entries; responders "
         "at least 4 points down from a baseline of at least 4 with no rescue by the week's last day.", "",
         "## 4. Deliverable Answers", "", "### %s" % GD.DELIV[0], "",
         "1. Phase 3 dose: HB-231 200 mg every four weeks.",
         "2. Expected week-16 PASI 75 in the phase 3 population against the 70 per cent bar: 50 mg %s, 100 mg %s, "
         "200 mg %s." % (s["50"], s["100"], s["200"]),
         "3. Chart of each candidate dose's expected response against the bar.", "",
         "### %s" % GD.DELIV[1], ""]
    k = 1
    for m in ("PASI 75", "PASI 90"):
        L.append("%d. %s at week 16 (per cent): %s." % (k, m, ", ".join("%s %.1f" % (ARM[a], ap["%s|%s" % (m, a)])
                                                                       for a in GD.A.ARMS)))
        k += 1
    for wk in ("Week 12", "Week 16"):
        L.append("%d. Itch NRS responders at %s (per cent of patients with a baseline weekly score of at least 4): "
                 "%s." % (k, wk.lower(), ", ".join("%s %.1f" % (ARM[a], ai["%s|%s" % (wk, a)]) for a in GD.A.ARMS)))
        k += 1
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


SOURCES = {
    "subjects": "the trial database's subject listing at lock", "dosing": "the IRT and pharmacy dosing log",
    "pasi": "the eCRF's PASI assessment pages", "pk": "the bioanalytical laboratories' trough concentration transfer",
    "cm": "the eCRF's concomitant medication pages", "epro": "the ePRO vendor's evening diary export",
    "ae": "the eCRF's adverse event pages", "dlqi": "the eCRF's DLQI pages", "sites": "the trial's site register",
    "feas": "Clinical Operations' VELA-3 site feasibility survey", "sap": "the VELA-2 statistical analysis plan",
    "cdp": "the HB-231 clinical development plan, section 7", "email": "the programme lead's request"}
DATES = {"sap": "2026-08-12", "cdp": "2026-06-04", "email": "2026-11-16", "feas": "2026-10-31", "sites": "2025-08-20"}
WHY = {"ae": "the adverse event pages decide nothing on the dose rule, which is set on efficacy",
       "dlqi": "quality of life is not the plan's endpoint; the dose rule is set on PASI 75"}


def metadata(n, path):
    meta = {"task": "task146", "architecture": 3, "as_of": "2026-11-16",
            "files": {PK.FILES[k]: {"source": SOURCES[k], "date": DATES.get(k, "2026-09-18"),
                                    "license": "synthetic, CC0",
                                    "role": "distractor" if k in PK.DISTRACTORS else "evidence"} for k in PK.FILES},
            "distractors": {PK.FILES[k]: WHY[k] for k in PK.DISTRACTORS},
            "largest_file": {"name": PK.FILES["epro"], "rows": n["epro"]},
            "deliverables": list(GD.DELIV)}
    json.dump(meta, open(path, "w"), indent=1, sort_keys=True)
