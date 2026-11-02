"""Fixed parameters of the VLT-317 phase 1 world (Valtenna Therapeutics, Ghent; Ekerstede CPU, Antwerp)."""

SEED = 13804

TZ = "Europe/Brussels"

SPONSOR = "Valtenna Therapeutics NV"
UNIT = "Ekerstede Clinical Pharmacology Unit"
COMPOUND = "VLT-317"

# study, design, cohorts as (dose mg, Day -1 local date), actives and placebos per cohort
STUDIES = [
    ("101", "SAD", [(25, "2026-02-02"), (50, "2026-02-16"), (100, "2026-03-02"), (200, "2026-03-28"),
                    (400, "2026-04-20")], 6, 2),
    ("102", "MAD", [(25, "2026-05-26"), (50, "2026-06-22"), (100, "2026-07-20")], 9, 3),
]
MAD_DAYS = 10

ECG_TIMES = [0.5, 1, 2, 3, 4, 6, 8, 12, 24]
PK_TIMES = [0, 0.5, 1, 2, 3, 4, 6, 8, 12, 24]
AMB_TIMES_SAD = [48, 72, 96, 144]
AMB_TIMES_MAD = [48, 72, 96]

PHASE2B_DOSES = [25, 50, 100]
DDI_CMAX_GMR = 2.61
DDI_CMAX_CI = (2.32, 2.94)
DDI_AUC_GMR = 3.37
DDI_AUC_CI = (3.01, 3.78)
QT_BOUND_MS = 10.0

LLOQ = 0.500
ULOQ = 1000.0

# physiology (ms, bpm, h)
PHYS = dict(
    beta_mu=0.420, beta_sd=0.030,
    qtc0_mu=401.0, qtc0_sd=12.0,
    hr0_mu=61.0, hr0_sd=6.0,
    amp_q_mu=11.5, amp_q_sd=2.0, phase_q_mu=4.2, phase_q_sd=0.7,
    amp_h=5.0, phase_h=4.0,
    sleep_drop=6.5, ambul_offset=5.0,
    act_scale=8.5, act_phi=0.72,
    seg_qtc_sd=2.4, seg_qt_sd=4.0, seg_hr_sd=1.6,
    tp_hr_sd=2.4, rep_hr_sd=0.8, tp_qtc_sd=2.0, rep_qt_sd=3.4,
    supine_circ_share=0.6,
)

# drug effects per ng/mL
DRUG = dict(s_qt=0.0100, s_hr=0.0180)

# two-compartment oral PK, typical values (L, L/h, 1/h)
PK = dict(cl=20.0, v1=243.0, q=10.5, v2=323.0, ka=1.0,
          cv_cl=0.25, cv_v1=0.20, cv_q=0.15, cv_v2=0.15, cv_ka=0.30, assay_cv=0.055)

AS_OF = "2026-10-28"
