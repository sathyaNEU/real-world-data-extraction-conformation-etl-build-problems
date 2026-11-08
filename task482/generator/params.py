"""task482 architecture 17: the Corlinn Schools Assessment Trust's Year 10 Science Benchmark. Every constant the
generator, the golden and the checks share."""
import datetime as dt

SEED = 482025            # the shipped draw: students, sittings, responses, entries, make-up scripts
POOL_SEED = 48217        # the item pool and the drafts (held fixed across the screens' redraws)
TRUST = "Corlinn Schools Assessment Trust"
NZST = dt.timezone(dt.timedelta(hours=12))      # August and November 2026 sit before daylight saving on 27 Sep

REGIONS = ["Northern", "Central", "Capital", "Southern"]
SCHOOLS_PER_REGION = [16, 12, 9, 11]
SIZE_LO, SIZE_HI = 60, 160          # Year 10 entries per school
CLASS_SIZE = 26

# The August 2026 sitting: weeks 3 to 5 of the national Term 3 calendar, weekdays only.
WINDOW_START = dt.date(2026, 8, 3)
WINDOW = [WINDOW_START + dt.timedelta(days=d) for d in range(19) if (WINDOW_START + dt.timedelta(days=d)).weekday() < 5]
MAKEUP_DAYS = [dt.date(2026, 8, 25), dt.date(2026, 8, 26), dt.date(2026, 8, 27)]
PRELIM_CUTOFF = dt.date(2026, 8, 19)     # the preliminary calibration ran on sessions to 19 August (NZ)
TERM_STARTS = [(dt.date(2026, 7, 13), 0.15), (dt.date(2026, 7, 20), 0.55), (dt.date(2026, 7, 21), 0.10),
               (dt.date(2026, 7, 27), 0.20)]
TERM3_END = {dt.date(2026, 7, 13): dt.date(2026, 9, 18), dt.date(2026, 7, 20): dt.date(2026, 9, 25),
             dt.date(2026, 7, 21): dt.date(2026, 9, 25), dt.date(2026, 7, 27): dt.date(2026, 10, 2)}
SPAN_LO, SPAN_HI = 6, 9              # school days over which a school sits
END_LO, END_HI = 1, 7                # first Term 3 unit ends this many school days after the school's first sitting day
WEEK_LO, WEEK_HI = 4, 8              # ...in week 4 to 8 of the school's own term
PERIODS = [(8, 50), (9, 50), (11, 20), (12, 20), (14, 0)]   # local period starts a class sits in

# The course: six core units over Terms 1 to 3; Term 4 is the school's own.
UNITS = [("U1", "Matter and reactions", "Material World", 1),
         ("U2", "Cells and body systems", "Living World", 1),
         ("U3", "Electricity and magnetism", "Physical World", 2),
         ("U4", "Space and the solar system", "Planet Earth and Beyond", 2),
         ("U5", "Forces and motion", "Physical World", 3),
         ("U6", "Earth's systems", "Planet Earth and Beyond", 3)]
STRAND_RANGE = {"Material World": (10, 14), "Living World": (10, 14), "Physical World": (12, 16),
                "Planet Earth and Beyond": (10, 14)}

# The 2026 forms: a 20-item anchor block (five from each Term 1 and 2 unit) on every form, then 30 form items:
# 22 from Terms 1 and 2 and 8 from Term 3 (four from each Term 3 unit).
N_FORMS = 4
ANCHORS_PER_UNIT = 5
FORM_T12 = [[6, 5, 6, 5], [5, 6, 5, 6], [6, 5, 6, 5], [5, 6, 5, 6]]     # per unit (U1..U4), per form
FORM_T3 = [4, 4]            # U5, U6 per form

# Response model (the truth): Rasch, with a unit not yet taught at the sitting making its items harder.
THETA_SD_SCHOOL, THETA_SD = 0.45, 1.0
THETA_MEAN = 0.10
B_T12_SD = 0.9
B_T3_MEAN, B_T3_SD = -0.85, 0.8
DELTA_MEAN, DELTA_SD, DELTA_LO, DELTA_HI = 1.0, 0.15, 0.6, 1.3

THETA_ACHIEVED = 0.35        # the standard-setting record, bank scale
THETA_MERIT, THETA_EXCELLENCE = 1.20, 2.05
TARGET = 25.0
PAPER_LEN = 50
DRAFT_T3 = {"A": (3, 3), "B": (6, 5), "C": (9, 8)}       # Term 3 items per draft (U5, U6)
DRAFT_GOLD = {"A": 26.0, "B": 23.0, "C": 25.0}           # the golden marks the drafts are composed to

# Layer 1 rates
RECONNECT_RATE = 0.032       # sessions that dropped and resumed (a second session row; items re-answered)
REANSWER_MAX = 3
ABSENT_RATE = 0.055          # entered candidates with no online session
MAKEUP_TAKE = 0.62           # of those, booked into a make-up session
NOSHOW_RATE = 0.12           # of those booked, did not attend
WITHDRAW_RATE = 0.02
TRANSFERS_PER_REGION = (3, 8)
TWINS_PER_REGION = (2, 5)
WALKINS_PER_REGION = (2, 5)
ASK_SEED_OFFSET = 6          # the ask records (entries, make-up sitting) draw on their own stream
CENTRAL_TO_NORTH = (1, 2, 3, 4)   # Central schools (by order in the region) whose absentees sit at the Northern host
CAPITAL_TO_CENTRAL = 4           # the first Capital schools sit at the Central host, the rest at the Southern host
MARK_SEED_OFFSET = 111           # make-up marks drawn per script, independent of the room
