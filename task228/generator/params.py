"""task228 architecture 5: Avisly Medier's experiment platform, the data-health check its scorecard service holds
experiments on from January 2027. Every quantity the generator draws from is set here."""
from datetime import date

SEED = 228501
Z = 2.5758293035489          # two-sided 1 per cent level
ALLOW = 0.02                  # at most one experiment in fifty without a confirmed incident may be held
BAND = 0.22                   # every valid method keeps every case at least this far from the line
STD_N = 10000                 # installs in each arm of a standard experiment's export
RUN_DAYS = 14

FIRST_START = date(2026, 1, 5)            # Mondays from here
LAST_START = date(2026, 9, 14)
MIGRATION = date(2026, 4, 13)             # scorecard service 2 writes the exports from this Monday
EXTRACT = date(2026, 10, 12)              # registry, exports, register and review log pulled
HOLD_LIVE = date(2027, 1, 4)              # the scorecard service holds on one check from this Monday

N_CLEAN = 64
INCIDENTS = ["loss"] * 10 + ["dup"] * 3 + ["late"] * 2 + ["consent"] * 3
N_ENGAGE = 9                              # experiments without an incident whose change moved reading itself
SPLITS = [0.5] * 70 + [0.2] * 8 + [0.1] * 4   # design treatment share
INSTALLS = (5200, 10400)                  # exported installs per experiment (both arms)
CONSENT = 0.86                            # share of assigned installs that allow analytics

PLATFORMS = ["ios", "android", "web"]
PLATFORM_P = [0.45, 0.40, 0.15]
FLAKY = {"ios": 0.028, "android": 0.050, "web": 0.030}     # installs whose uploader keeps failing
GAP_FLAKY, GAP_OK = (2.0, 7.0), (1.0, 60.0)
DUP_FLAKY_P = 0.010
DUP_FLAKY, DUP_OK = (1.2, 8.0), (0.4, 400.0)
OFFLINE_P = 0.15
LATE_OFFLINE, LATE_OK = (6.0, 45.0), (6.0, 170.0)
SESS_K, SESS_MEAN = 1.3, 11.0             # negative binomial sessions over a 14-day run, plus one
EVENTS_K, EVENTS_SCALE = 4.0, 9.0 / 4.0   # events per session

LOSS_BUMP = (0.014, 0.030)                # extra gap probability in heavy readers' sessions
LOSS_TOP = (0.10, 0.16)                   # share of installs (heaviest readers) the loss reaches
LOSS_BUMP_BROAD = (0.020, 0.034)          # the loss incidents that reached a broader slice of readers
LOSS_TOP_BROAD = (0.30, 0.45)
LOSS_LATE_SMALL = (0.0025, 0.0045)
LOSS_LATE = (0.004, 0.009)                # late sessions in three loss incidents (resumed uploads)
DUP_BUMP = (0.012, 0.022)                 # android duplicate-delivery incidents
LATE_BUMP = (0.008, 0.014)
CONSENT_LOST = (0.05, 0.09)
ENGAGE = (0.04, 0.08)

STD_SPLIT = 0.5
