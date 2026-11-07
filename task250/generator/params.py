"""task250 architecture 4: the fixed inputs of the world. Every figure the pack, the goldens and the write-up carry
is computed forward from these; nothing downstream types a number of its own."""
import datetime as dt

SEED = 250
YEAR = 2026
LINE = 0.85                      # QS-HS section 6: at least 85 in 100 responding households of two or more adults
ASOF = dt.date(2027, 1, 15)      # case management extract
COMMITTEE = dt.date(2027, 1, 21)
PRINT_ORDER = dt.date(2027, 1, 25)
FIRST_2027_MAILING = dt.date(2027, 2, 15)
STAMP = dt.datetime(2027, 1, 15, 9, 41, 0)   # export time of the extracts (local, Lisbon, WET in January)

INSTITUTE = "Instituto de Estudos e Inquéritos às Famílias"
INSTITUTE_SHORT = "IEIF"

# Adults' birthdays by day of the year (0 = 1 January). A spring peak in the cohorts the programme interviews.
BDAY_A1, BDAY_P1 = 0.215, 95.0
BDAY_A2, BDAY_P2 = 0.070, 95.0

# Seven fieldwork regions (code, name, share of the frame's addresses)
REGIONS = [
    ("NOR", "Norte", 0.335),
    ("CEN", "Centro", 0.215),
    ("LVT", "Lisboa e Vale do Tejo", 0.318),
    ("ALE", "Alentejo", 0.057),
    ("ALG", "Algarve", 0.040),
    ("ACO", "Açores", 0.016),
    ("MAD", "Madeira", 0.019),
]
REGION_RESP = {"NOR": 1.03, "CEN": 1.08, "LVT": 0.90, "ALE": 1.10, "ALG": 0.86, "ACO": 1.05, "MAD": 0.97}

# The six surveys of the 2026 programme: code, English name, Portuguese name, first letter, reserve release
# (date, addresses) or None, main sample addresses, base response propensity, substitution profile.
SURVEYS = [
    ("ISBE", "Health and Wellbeing Survey", "Inquérito à Saúde e Bem-Estar",
     dt.date(2026, 1, 12), None, 68400, 0.334, "oldest_woman"),
    ("IVD", "Digital Life Survey", "Inquérito à Vida Digital",
     dt.date(2026, 3, 16), (dt.date(2026, 4, 6), 4200), 66900, 0.318, "youngest"),
    ("ISV", "Safety and Victimisation Survey", "Inquérito à Segurança e Vitimação",
     dt.date(2026, 5, 18), None, 69100, 0.326, "oldest"),
    ("IPC", "Cultural Participation Survey", "Inquérito à Participação Cultural",
     dt.date(2026, 7, 20), (dt.date(2026, 8, 10), 5300), 65800, 0.301, "random"),
    ("IUT", "Time Use Survey", "Inquérito aos Usos do Tempo",
     dt.date(2026, 9, 21), None, 68700, 0.312, "woman"),
    ("IVP", "Working Life Survey", "Inquérito à Vida Profissional",
     dt.date(2026, 11, 23), None, 67600, 0.329, "man"),
]
SURVEY_CODES = [s[0] for s in SURVEYS]
MODES = ("web", "paper")

# Target share of responding households of two or more adults whose respondent is the next-birthday adult, per
# survey and mode. The share a stream reaches is c + (1 - c) * E[1/k]: a household that substitutes picks its
# substitute without regard to birthdays, so the substitute is the next-birthday adult one time in k.
TARGET_S = {
    ("ISBE", "web"): 0.905, ("ISBE", "paper"): 0.808,
    ("IVD", "web"): 0.784, ("IVD", "paper"): 0.776,
    ("ISV", "web"): 0.791, ("ISV", "paper"): 0.906,
    ("IPC", "web"): 0.892, ("IPC", "paper"): 0.789,
    ("IUT", "web"): 0.796, ("IUT", "paper"): 0.918,
    ("IVP", "web"): 0.781, ("IVP", "paper"): 0.903,
}
E_INV_K = 0.424    # E[1/k] over responding households of two or more adults (asserted against the world)
COMPLIANCE = {k: (s - E_INV_K) / (1 - E_INV_K) for k, s in TARGET_S.items()}

# How a substituting household picks its respondent, by survey topic: the profiled adult with this probability,
# otherwise whoever opened the letter (an adult unrelated to sex, age or birthday).
PROFILE_STRENGTH = {"oldest_woman": 0.66, "youngest": 0.64, "oldest": 0.66, "random": 0.0, "woman": 0.72,
                    "man": 0.70}

# Addresses as the frame lists them: status shares among sampled addresses
ADDRESS_STATUS = [("occupied", 0.8085), ("vacant", 0.1290), ("nonresidential", 0.0390), ("communal", 0.0085),
                  ("nonexistent", 0.0150)]

# Fieldwork rhythm (days after a household's first letter)
REMINDER_DAYS = 7
PAPER_MAILING_DAYS = 21
CLOSE_DAYS = 49
SYSTEM_UPGRADE = dt.date(2026, 7, 27)   # the case management system's new disposition list

# Responding households' adults (aged 16 or over): k = 1..5
K_PROBS = [0.338, 0.421, 0.152, 0.068, 0.021]
