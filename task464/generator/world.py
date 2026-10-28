"""task464 architecture 6: the world.

A combined authority commissions adult skills places from six delivery partners. Places are funded before the
learner decides; a refused place can be passed down the ballot only until the intake's enrolment census date.
The decision is which partner's model to scale for the 2027 funded place allocation.

Nothing in this module states a fill rate, a yield or a ranking. Those are computed in sim.py and answers.py.
"""

AUTHORITY = "Thornmere Combined Authority"
PROGRAMME = "Adult Skills Place Ballot"
QUALIFICATION = "Level 2 Certificate in Workplace Numeracy"
CURRENCY = "GBP"
ASOF = "2026-11-20"             # the commissioning decision is taken after this date
DECISION_YEAR = "2027"          # the allocation not yet committed

# People, drawn with guard.py names --geo england --seed 464. Never typed.
PEOPLE = {
    "commissioning_manager": "Glenn Taylor",     # adult skills team, prepares the slate
    "data_officer": "Gail Dobson",               # management information returns
}

# The two intakes the evidence covers. The census date is the hard stop on the waitlist cascade: a place not
# taken up by a learner enrolled on that date cannot be claimed and cannot be re-offered.
INTAKES = [
    {"code": "AUT25", "label": "autumn 2025", "term_start": "2025-09-15", "census": "2025-10-15",
     "release_prelim": "2026-06-30", "release_revised": "2026-07-28", "share": 0.56},
    {"code": "SPR26", "label": "spring 2026", "term_start": "2026-01-12", "census": "2026-02-04",
     "release_prelim": "2026-09-29", "release_revised": "2026-10-27", "share": 0.44},
]

# One row per delivery partner.
#   apps      total applications across both intakes
#   places    places funded across both intakes (the commissioning schedule)
#   takeup    share of applicants who would enrol if offered a place (the learner's own choice)
#   cascade   share of refused places the partner refills from its waitlist before the census date
#   effect    the effect on achievement among learners who enrol (the per-participant effect)
#   base      achievement rate for a learner who does not enrol on the programme
#   ballot_weeks   weeks between the partner's ballot and the census date, which is why cascade differs
PARTNERS = [
    {"key": "ASH", "name": "Ashcombe Adult Learning",      "town": "Ashcombe",
     "apps": 10958, "places": 3388, "takeup": 0.50, "cascade": 0.13, "effect": 0.150, "base": 0.318,
     "ballot_weeks": 3, "reserve_list": False},
    {"key": "BRN", "name": "Brenlow Skills Trust",         "town": "Brenlow",
     "apps": 9300,  "places": 3175, "takeup": 0.60, "cascade": 0.17, "effect": 0.240, "base": 0.281,
     "ballot_weeks": 4, "reserve_list": False},
    {"key": "CAL", "name": "Calderwick College",           "town": "Calderwick",
     "apps": 9499,  "places": 3066, "takeup": 0.48, "cascade": 0.08, "effect": 0.260, "base": 0.247,
     "ballot_weeks": 2, "reserve_list": False},
    {"key": "DUN", "name": "Dunthorpe Learning Partnership","town": "Dunthorpe",
     "apps": 8756,  "places": 3364, "takeup": 0.60, "cascade": 0.95, "effect": 0.200, "base": 0.262,
     "ballot_weeks": 10, "reserve_list": True},
    {"key": "ELM", "name": "Elmsgate Institute",           "town": "Elmsgate",
     "apps": 8648,  "places": 2778, "takeup": 0.45, "cascade": 0.09, "effect": 0.120, "base": 0.236,
     "ballot_weeks": 2, "reserve_list": False},
    {"key": "FAI", "name": "Fairholt Training",            "town": "Fairholt",
     "apps": 8201,  "places": 2723, "takeup": 0.36, "cascade": 0.05, "effect": 0.280, "base": 0.273,
     "ballot_weeks": 1, "reserve_list": False},
]
BY_KEY = {p["key"]: p for p in PARTNERS}

# Achievement is driven partly by a latent readiness that also drives take-up. This is the selection that makes
# an attendance-based comparison wrong, and it is why the ballot is the only honest contrast.
SELECTION = 0.045               # achievement points per standard deviation of readiness

SEED = 46835                    # fixed; build.py asserts two byte-identical rebuilds

def intake(code):
    for i in INTAKES:
        if i["code"] == code:
            return i
    raise KeyError(code)

def places_for(partner, intake_code):
    """Places funded for one partner in one intake. Integer, and the two intakes sum to the partner's total."""
    first = int(round(partner["places"] * INTAKES[0]["share"]))
    return first if intake_code == INTAKES[0]["code"] else partner["places"] - first

def apps_for(partner, intake_code):
    first = int(round(partner["apps"] * INTAKES[0]["share"]))
    return first if intake_code == INTAKES[0]["code"] else partner["apps"] - first
