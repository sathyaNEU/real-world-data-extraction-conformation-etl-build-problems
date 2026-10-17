"""task237 parameters: the Community Connections Survey's wave 6 translations of the twelve-item Belonging and
Connection Scale (BCS-12), their pilots with two fieldwork vendors, and the translation and adaptation standard's
release gate. Dates are Eastern Time unless a name says UTC."""
import datetime as dt

SEED = 237
WORLD_SEED = 57                      # respondents and their answers (sim.World)
RECORD_SEED = SEED * 7 + 5           # ids, timestamps, vendor files, distractors (records.Records)

PEOPLE = {"quality": "Tara Bauer", "coordinator": "Rodney Fernandez", "pilot": "Cindy Stein"}
CENTRE = "Survey Research Centre, Marlowe University"
SURVEY = "Community Connections Survey"
SCALE = "Belonging and Connection Scale (BCS-12)"
WAVE = 6

AS_OF = dt.date(2027, 3, 1)                     # the decisions are signed off on Monday 1 March 2027
LAUNCH = dt.date(2027, 3, 22)                   # wave 6 fieldwork launches
EXPORT_UTC = dt.datetime(2027, 2, 26, 21, 30)  # the vendors' final pilot files, Friday 26 February (UTC)
UTC_OFFSET = dt.timedelta(hours=-5)             # Eastern Standard Time

RELEASE, HOLD = 0.80, 0.70                      # the standard's bands

# the scale: item code, wording, keying (+1 positively worded, -1 negatively worded, reverse-scored)
ITEMS = [
    ("BCS01", "I feel close to the people around me.", 1),
    ("BCS02", "I often feel left out.", -1),
    ("BCS03", "There are people I can count on when things go wrong.", 1),
    ("BCS04", "There is no one I can talk to about personal matters.", -1),
    ("BCS05", "I feel part of my neighbourhood.", 1),
    ("BCS06", "I feel cut off from the people around me.", -1),
    ("BCS07", "People in my life care about how I am doing.", 1),
    ("BCS08", "I do not have anyone to share my interests with.", -1),
    ("BCS09", "I feel welcome in my community.", 1),
    ("BCS10", "I feel like an outsider where I live.", -1),
    ("BCS11", "I have people I can turn to for advice.", 1),
    ("BCS12", "I feel alone even when I am with others.", -1),
]
POS = [0, 2, 4, 6, 8, 10]
NEG = [1, 3, 5, 7, 9, 11]
LABELS = {1: "Strongly disagree", 2: "Disagree", 3: "Neither agree nor disagree", 4: "Agree", 5: "Strongly agree"}

VENDORS = {"NCP": ("Nesscroft Panels", "online panel"), "FLR": ("Fernlow Research", "interviewer-administered (CAPI)")}

# versions: code, language, vendor, valid completes, trait loadings of the positively and the negatively worded items,
# the wording factor's loading on the negatively worded items (0 where the translation carries none)
VERSIONS = [
    ("pa",      "Punjabi",                         "FLR", 512, [.62, .60, .63, .59, .61, .60], [.58, .57, .60, .56, .59, .57], 0.00),
    ("zh-Hans", "Chinese, Simplified (Mandarin)",  "NCP", 588, [.68, .66, .67, .65, .69, .66], [.48, .50, .47, .49, .46, .48], 0.45),
    ("yue",     "Cantonese",                       "FLR", 466, [.51, .49, .50, .48, .51, .47], [.33, .35, .31, .34, .32, .33], 0.52),
    ("tl",      "Tagalog",                         "NCP", 437, [.67, .65, .68, .64, .66, .65], [.46, .44, .47, .45, .43, .46], 0.50),
    ("ar",      "Arabic",                          "FLR", 538, [.63, .61, .65, .59, .64, .60], [.51, .50, .53, .49, .52, .50], 0.40),
    ("es",      "Spanish",                         "NCP", 604, [.70, .68, .66, .69, .67, .65], [.64, .62, .65, .61, .63, .60], 0.00),
    ("ur",      "Urdu",                            "FLR", 452, [.37, .35, .39, .34, .38, .36], [.33, .32, .35, .31, .34, .32], 0.00),
    ("vi",      "Vietnamese",                      "NCP", 497, [.72, .70, .71, .73, .69, .71], [.26, .24, .27, .25, .23, .26], 0.76),
    ("fa",      "Persian (Farsi)",                 "NCP", 476, [.73, .71, .70, .72, .69, .71], [.66, .64, .67, .63, .65, .62], 0.00),
    ("ko",      "Korean",                          "NCP", 556, [.69, .67, .66, .68, .65, .67], [.50, .52, .49, .51, .53, .50], 0.44),
]
ENGLISH = ([.72, .70, .71, .69, .72, .70], [.66, .65, .67, .64, .66, .65])   # the source version's loadings

# the five-point scale's thresholds (keyed direction), and each version's overall shift in how readily its items are
# endorsed (a translation's wording makes agreement a little easier or harder throughout)
CUTS = (-1.7, -0.8, 0.15, 1.1)
LEVEL = {"pa": -0.10, "zh-Hans": 0.06, "yue": 0.10, "tl": 0.05, "ar": -0.04, "es": -0.16, "ur": 0.08, "vi": 0.04,
         "fa": -0.06, "ko": 0.14}
NUDGE = {"vi": 0.001, "fa": 0.002, "ko": -0.002}

# respondents' ages: 18 plus a beta-distributed span (online panels run younger than interviewer-administered samples)
AGE_BETA = {"NCP": (1.7, 2.6, 71), "FLR": (1.9, 2.3, 74)}

# pilot fieldwork windows (Eastern dates) and the CAPI vendor's pretest of the draft translations before them
PILOT = {"NCP": (dt.date(2027, 1, 18), dt.date(2027, 2, 12)), "FLR": (dt.date(2027, 1, 25), dt.date(2027, 2, 19))}
PRETEST = (dt.date(2027, 1, 6), dt.date(2027, 1, 15))

# what each vendor's file carries besides valid completes
SCREENOUT = 0.035        # online: under-18 respondents screened out (no answers)
PARTIAL = 0.045          # online: broke off before the end of the module
RETAKE = 0.03            # online: a panel member's second completion of the version, under a fresh respondent id
SWITCH = 0.022           # online: switched the questionnaire to English before finishing
PRETEST_N = (32, 46)     # CAPI: pretest interviews of the draft translation, per version
BACKCHECKED = 0.24       # CAPI: interviews selected for the vendor's back-check
NOT_CONFIRMED = 0.035    # CAPI: share of all interviews the back-check could not confirm
NOT_REACHED = 0.30       # CAPI: share of back-checked respondents the vendor could not reach
ITEM_MISSING = 0.009     # an item left unanswered (prefer not to say, don't know, refused), per item
MISSING_SLOPE = 0.55     # unanswered items are commoner among the less connected

# the background questions after the BCS-12 module, and respondents who left the interview there
PAST_MODULE = {"NCP": 0.030, "FLR": 0.015}   # reached the end of the module, left in the background questions
INSIDE_FLR = 0.020       # CAPI: broken off inside the module
REVISIT = 0.60           # CAPI: share of those cases revisited by another interviewer for a full interview
MERGED = 0.008           # online: a second completion from a second account of the same member, merged afterwards
BENIGN_MERGES = 0.010    # online: merged second accounts whose entry was a screen-out or a partial
SOFT = 0.025             # online: entries on the soft-launch evening before the pilot's first day
SOFT_OPEN = 18           # the soft launch opened the links at 18:00 Eastern on the day before the pilot
REISSUE = 0.80           # CAPI: share of unconfirmed cases reissued to another interviewer within the pilot dates
