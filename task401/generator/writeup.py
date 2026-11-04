"""task401: submission.md from generator/figures.json (every figure emitted, never typed)."""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MON = [('2025-10', 'October 2025'), ('2025-11', 'November 2025'), ('2025-12', 'December 2025'), ('2026-01', 'January 2026'), ('2026-02', 'February 2026')]


def n(x): return '{:,}'.format(int(x))
def s(x): return ('%+d' % x).replace('-', '−') if False else ('{:+,}'.format(int(x)))


def run(R=None):
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    c, sf, ex, cv = F['cost'], F['so_far'], F['excess_idle'], F['conv_pct']
    L = []
    L += ['## Tags', '',
          '**Domain:** Psychology & Behavioral Science, mediation, moderation and process modelling (a charitable leisure trust\'s '
          'membership after its January and February 2026 changes, read through the members who stop coming before they cancel).  ',
          '**Analytical objective:** Root-Cause Analysis (which of the changes will cost the trust the most members over the 2026-27 '
          'membership year).', '']
    L += ['## 1. Final Recommendation', '',
          '**Reverse the Rewards closure.** It will cost about %s members over the 2026-27 membership year (2 February 2026 to 31 January '
          '2027), %.2f times the legacy terms letters at about %s, whose cancellations made February\'s spike. Not the letters: most of the '
          'members they prompted had stopped coming long before and would have cancelled within the year anyway. Not the daytime timetable '
          '(about %s), the shorter hours at Northgate and Westcroft (about %s) or the member care calls, which bring members back.'
          % (n(c['A']), F['lead'], n(c['D']), n(c['C']), n(c['E'])), '']
    L += ['## 2. Critical Components', '',
          '1. The closure: %s cancellations against the same weeks of 2025 by 16 March, and **%s** more Rewards holders with no visit in the '
          '28 days to 16 March than a year earlier; last year **%.1f per cent** of holders in that position cancelled before the membership '
          'year ended, so the year\'s cost is about **%s**.' % (s(sf['A']), n(ex['A']), cv['A'], n(c['A'])),
          '2. The letters: **%s** more legacy cancellations by 16 March than in the same weeks of 2025, but %s fewer legacy members not '
          'visiting than a year earlier, who on last year\'s %.1f per cent would have cancelled within the year: about **%s**.'
          % (n(sf['D']), n(-ex['D']), cv['D'], n(c['D'])),
          '3. The rest: the timetable about %s, the hours cut about %s, and the care calls lower cancellations.' % (n(c['C']), n(c['E'])), '']
    L += ['## 3. Step-by-Step Solution', '',
          '1. Took each change\'s members from savings_programme_2025-26.docx: Rewards holders on 31 January 2026 (rewards_account_opened in '
          'membership_register_2026-03-16.csv), legacy tariffs (codes L-) on 2 February, weekday class bookings starting before 5pm from '
          '13 October 2025 to 11 January 2026 (class_bookings_2024-10-07_to_2026-03-15.parquet), home centre Northgate or Westcroft; and '
          'the members in the same position 364 days earlier, the same weeks of 2025-26 (Schedule 4, 4.3).',
          '2. Counted each membership once at its first request (Schedule 4, 4.1) in cancellation_requests_2024-01-01_to_2026-03-15.csv; '
          'for each change, the cancellations from its date to 16 March among its members not already leaving, less the same weeks of '
          '2025 at that year\'s rate: closure %s, letters %s, timetable %s, hours %s.' % (s(sf['A']), s(sf['D']), s(sf['C']), s(sf['E'])),
          '3. From access_weekly_usage_2024-01-01_to_2026-03-15.parquet, members on the books with no visit in the 28 days before 16 March '
          '2026 and before 17 March 2025, as a share of each change\'s members, the difference times its members now: closure %s, letters '
          '%s, timetable %s, hours %s.' % (s(ex['A']), s(ex['D']), s(ex['C']), s(ex['E'])),
          '4. Of last year\'s members of each change in that position on 17 March 2025, the share whose first request came before 2 February '
          '2026, the end of that membership year: %.1f, %.1f, %.1f and %.1f per cent.' % (cv['A'], cv['D'], cv['C'], cv['E']),
          '5. Each change\'s year is step 2 plus step 3 times step 4: the closure about %s, the letters about %s, the timetable about %s, '
          'the hours about %s; the closure is the largest.' % (n(c['A']), n(c['D']), n(c['C']), n(c['E'])),
          '6. Admissions: old till lines with a Family Swim read as its party from the price list\'s pay-as-you-go sheet; EPOS lines by '
          'transaction, a Swim and Gym ticket\'s two 4.70 lines one person; voids netted in both; EPOS refunds made inside a closure in '
          'pool_closures_2025-10-01_to_2026-03-15.csv kept, those swimmers were admitted; month of sale, site codes from the EPOS notice.',
          '7. Fees: bureau A dated the working day after its processing date and re-presentations to their first month; bureau B by mandate '
          '(dd_mandates_2026-03-16.csv) over the household (paid_by_membership_no); a returned collection\'s fees counted when a later '
          'collection clears, including a bureau A collection refused twice and taken in December by bureau B; the administration charge '
          'out; each fee in the month its household\'s collection day falls in.', '']
    L += ['## 4. Deliverable Answers', '', '### change_review.pdf', '',
          '1. Change to reverse: the Rewards closure (1 February 2026), about %s members over the 2026-27 membership year.' % n(c['A']),
          '2. Why each of the others costs fewer: the legacy terms letters about %s (cancellations brought forward from later in the year), '
          'the daytime timetable about %s, the shorter hours at Northgate and Westcroft about %s, the member care calls fewer cancellations.'
          % (n(c['D']), n(c['C']), n(c['E'])),
          '3. Chart: one bar per change of its membership-year cost, split into the cancellations so far and the part still to come or '
          'already brought forward, the closure\'s largest.', '', '### monthly_return.xlsx', '',
          '1. Pay-as-you-go admissions, each person once, nearest 10:']
    for m, lab in MON:
        L.append('   - %s: Northgate and Westcroft %s, other centres %s' % (lab, n(F['admissions']['%s NW' % m]), n(F['admissions']['%s other' % m])))
    L.append('2. Membership fees for the month they pay for, nearest GBP 100:')
    for m, lab in MON[1:]:
        L.append('   - %s: legacy tariffs GBP %s, 2023 tariffs GBP %s' % (lab, n(F['fees']['%s legacy' % m]), n(F['fees']['%s 2023' % m])))
    open(os.path.join(TASK, 'submission.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    run()
