"""The governing documents of the pack: the concentration-QTc analysis plan and the DDI study synopsis."""
import params as P
from io_util import write_pdf


def analysis_plan(path):
    b = [
        ("t", "VLT-317 concentration-QTc analysis plan"),
        ("s", "Valtenna Therapeutics NV, Clinical Pharmacology. Version 2.0, 10 September 2026. Author: Hilde Lemmens "
              "(pharmacometrics). Approved: Micha&euml;l Tanghe (head of clinical pharmacology). Supersedes version 1.0 "
              "(QTcF, written before the single ascending dose study)."),
        ("h", "1. Purpose"),
        ("p", "This plan sets out how the QT effect of VLT-317 is assessed from the first-in-human studies VLT-317-101 "
              "(single ascending doses of 25 to 400 mg) and VLT-317-102 (multiple ascending doses of 25, 50 and 100 mg once "
              "daily for 10 days), both run at the Ekerstede Clinical Pharmacology Unit, so that the doses carried into "
              "study VLT-317-201 can be chosen and the QT assessment strategy agreed with the regulators. Study VLT-317-201 "
              "(phase 2b, start planned for the first quarter of 2027) will test 25, 50 and 100 mg once daily."),
        ("h", "2. ECG and concentration data"),
        ("p", "Triplicate 12-lead ECGs were extracted by the core laboratory from continuous Holter recordings at the "
              "nominal times 0.5, 1, 2, 3, 4, 6, 8, 12 and 24 hours after dosing on Day 1 (both studies) and Day 10 "
              "(study 102), and at the same clock times on Day -1. A plasma sample was drawn immediately after each "
              "extraction. Each time point's interval is the mean of its readable replicates."),
        ("h", "3. Heart-rate correction"),
        ("p", "VLT-317 raised heart rate in the single ascending dose study, so the analysis uses an individual "
              "correction. QTcI is each subject's QT interval corrected to an RR interval of 1,000 ms with his own "
              "heart-rate exponent: QTcI = QT / RR<super>b</super>, with RR in seconds, where b is the power with which "
              "that subject's QT interval follows his RR interval, the change in QT that a change in heart rate alone "
              "produces, taken from his own drug-free Holter recording before the first dose."),
        ("h", "4. Endpoint and model"),
        ("p", "The endpoint is the change in QTcI from the same nominal time on Day -1 (&Delta;QTcI) at every post-dose "
              "time point of both studies. &Delta;QTcI is analysed with a linear mixed-effects model with fixed effects "
              "for intercept, treatment (VLT-317 or placebo), plasma concentration, nominal time (categorical) and "
              "baseline QTcI (the subject's mean Day -1 QTcI over the nominal times, centred on the mean over all "
              "subjects), and with a random intercept and a random slope on concentration for each subject "
              "(unstructured covariance), fitted by restricted maximum likelihood. Placebo subjects enter with a "
              "concentration of zero; concentrations below the limit of quantification are set to zero."),
        ("h", "5. Prediction and criterion"),
        ("p", "The high clinical exposure for each phase 2b dose is the geometric mean of the observed Day 10 Cmax "
              "of the study 102 subjects who received VLT-317 at that dose, multiplied by the geometric mean ratio of "
              "Cmax with itraconazole from study VLT-317-103. The predicted placebo-corrected &Delta;QTcI at a "
              "concentration is the treatment effect plus the concentration slope times that concentration. A dose can be "
              "taken forward without a dedicated QT study if the upper bound of the two-sided 90% confidence interval "
              "of the predicted placebo-corrected &Delta;QTcI at its high clinical exposure is below 10 ms."),
        ("h", "6. Exposure parameters reported alongside"),
        ("p", "Non-compartmental parameters use actual sampling times. AUC is computed with the linear-up/log-down "
              "trapezoidal rule to the last quantifiable concentration and extrapolated to infinity with the terminal "
              "rate constant, estimated by log-linear regression on the terminal phase (best fit by adjusted "
              "R<super>2</super>, at least three points after Cmax). Concentrations below the limit of quantification "
              "before the first quantifiable one are set to zero; later ones are not used."),
        ("h", "7. Software and records"),
        ("p", "Analyses are run in validated R or SAS environments. Data transfers: core laboratory ECG transfer 3 (study "
              "101) and transfer 2 (study 102); bioanalytical results as issued by the unit's laboratory; dosing and "
              "randomisation records from the unit's clinical database after unblinding."),
    ]
    write_pdf(path, "VLT-317 concentration-QTc analysis plan v2.0", "Hilde Lemmens", "Microsoft Word", b,
              "Valtenna Therapeutics NV | VLT-317 C-QTc analysis plan v2.0 | Confidential",
              "D:20260910111840+02'00'", "D:20260910112205+02'00'", subject="VLT-317 clinical pharmacology")


def ddi_synopsis(path):
    rows = [["Parameter", "VLT-317 alone", "VLT-317 + itraconazole", "Geometric mean ratio (90% CI)"],
            ["Cmax (ng/mL), geometric mean", "35.6", "92.9", "%.2f (%.2f to %.2f)" % (P.DDI_CMAX_GMR, *P.DDI_CMAX_CI)],
            ["AUC0-inf (ng.h/mL), geometric mean", "518", "1,746", "%.2f (%.2f to %.2f)" % (P.DDI_AUC_GMR, *P.DDI_AUC_CI)],
            ["tmax (h), median", "2.0", "2.5", "not applicable"]]
    b = [
        ("t", "Clinical study report synopsis: VLT-317-103"),
        ("s", "Valtenna Therapeutics NV. Synopsis issued 9 October 2026. Principal investigator: Kim Huysmans, "
              "Ekerstede Clinical Pharmacology Unit, Antwerp."),
        ("h", "Title"),
        ("p", "An open-label, fixed-sequence study of the effect of multiple doses of itraconazole, a strong CYP3A "
              "inhibitor, on the pharmacokinetics of a single oral dose of VLT-317 in healthy subjects."),
        ("h", "Design"),
        ("p", "Period 1: VLT-317 10 mg single dose on Day 1. Period 2: itraconazole 200 mg once daily from Day 15 to "
              "Day 26 with VLT-317 10 mg on Day 18. Serial plasma samples to 144 hours after each VLT-317 dose. "
              "Sixteen subjects enrolled; fourteen completed both periods and form the pharmacokinetic population."),
        ("h", "Pharmacokinetic results"),
        ("table", rows),
        ("h", "Safety"),
        ("p", "VLT-317 alone and with itraconazole was well tolerated. The most frequent adverse events were dry mouth "
              "(5 subjects) and headache (3). No subject had a QTcF above 450 ms on the safety ECGs. One subject "
              "withdrew in period 2 for a reason unrelated to study drug."),
        ("h", "Conclusion"),
        ("p", "Itraconazole increased VLT-317 Cmax 2.6-fold and AUC 3.4-fold. Strong CYP3A inhibitors will be "
              "excluded in phase 2b; the exposure under strong inhibition defines the high clinical exposure for the "
              "QT assessment."),
    ]
    import reportlab.lib.units as u
    write_pdf(path, "VLT-317-103 CSR synopsis", "Kim Huysmans", "Microsoft Word", b,
              "Valtenna Therapeutics NV | VLT-317-103 synopsis | Confidential",
              "D:20261009093112+02'00'", "D:20261009094650+02'00'",
              widths={4: [52 * u.mm, 30 * u.mm, 40 * u.mm, 48 * u.mm]}, subject="VLT-317-103")
