"""Constants of the Quarrystone world. Every figure the pack, the goldens and the write-up carry is computed from
these and the seeds; nothing downstream is typed."""
import datetime as dt

SEED = 488
SEED_BANK = 488_101
SEED_STUDENTS = 488_202
SEED_CAT = 488_303
SEED_PACK = 488_404

GRADES = [3, 4, 5, 6, 7, 8]
STUDENTS = {3: 5_830, 4: 5_710, 5: 5_960, 6: 5_590, 7: 5_440, 8: 5_360}   # enrolled in grade in 2025-26
TEST_LENGTH = 40
EXPOSURE_K = 7                     # the engine picks at random among the seven items nearest its running estimate
SCALE_A, SCALE_B = 500.0, 40.0     # Quarrystone scale score = 500 + 40 x theta, one scale per grade (2021 launch)
LOSS, HOSS = 340, 660
# Approaching cut on each grade's scale (the 2021 standard setting)
CUT_QSS = {3: 481.0, 4: 482.0, 5: 482.0, 6: 483.0, 7: 481.0, 8: 482.0}
FLOOR = 150                        # Corvane's blueprint: items below the Approaching cut, per grade

WINDOWS = [("fall", dt.date(2025, 9, 15), dt.date(2025, 10, 24), -0.46),
           ("winter", dt.date(2026, 1, 12), dt.date(2026, 2, 20), -0.17),
           ("spring", dt.date(2026, 4, 13), dt.date(2026, 5, 22), 0.04)]
ABSENT_SHARE = 0.031               # a student misses a window
INVALIDATED_SHARE = 0.008
INCOMPLETE_SHARE = 0.009
RESUMED_SHARE = 0.021

EXPORT = dt.datetime(2027, 3, 31, 16, 40)      # Tessaline's close-out export, Central time
CUTOVER = dt.date(2027, 7, 1)
DECIDED = dt.date(2027, 4, 22)                  # the board meeting that funds the workshop

# provisional item groups, per grade counts drawn in world.py
#   right: computation and one-step word problems the panel rated about right
#   low_mis: multi-step word problems the panel rated far too easy, still truly below the cut
#   high_mis: multi-step word problems the panel rated far too easy, truly above the cut
#   mid_ok: multi-step word problems the panel rated about right, above the cut
