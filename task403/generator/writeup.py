"""task403 write-up: submission.md emitted from generator/figures.json, so no figure is typed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MONTHS = [('2025-02', 'February'), ('2025-03', 'March'), ('2025-04', 'April'), ('2025-05', 'May'), ('2025-06', 'June'),
          ('2025-07', 'July'), ('2025-08', 'August'), ('2025-09', 'September'), ('2025-10', 'October')]


def c(n):
    return '{:,}'.format(n)


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    L = []
    L += ['## Tags', '',
          '**Domain:** Product Analytics, funnel and journey analysis (a Canadian subscription streaming service\'s free-trial '
          'conversion and the one programme its subscriber growth budget funds for the 2026-27 winter).  ',
          '**Analytical objective:** Root-Cause Analysis (which cause of the 2025-26 winter\'s fall in trial-to-paid conversion '
          'the funded programme fixes).', '']
    L += ['## 1. Final Recommendation', '',
          '**Fund (C), the winter release slate.** Its cause cost about %s of the 2025-26 winter\'s paid conversions, %s more '
          'than the runner-up. Not (A) the first-month price hold (about %s): the fall holds in every segment and lands on the '
          'price date only because the autumn finales closed October the same week, and trialists with no season still to '
          'come converted almost as they did a year earlier. Not (B) first-charge recovery or (D) the paid acquisition mix '
          '(about %s each).' % (c(F['conv_slate']), c(F['conv_gap']), F['conv_price'], F['conv_recovery']), '']
    L += ['## 2. Critical Components', '',
          '1. The slate\'s cost, last winter\'s conversion less that of last winter\'s trialists with no season still to come, '
          'at this winter\'s trials (none of which had one): **%s** paid conversions.' % c(F['conv_slate']),
          '2. The price\'s cost, the rest of the fall less first-charge recovery and the channel mix: **%s**.' % F['conv_price'],
          '3. First-charge recovery **%s** and the paid acquisition mix **%s**; the slate leads the price by **%s**.'
          % (F['conv_recovery'], F['conv_channel'], c(F['conv_gap'])), '']
    L += ['## 3. Step-by-Step Solution', '',
          '1. Read trial_register.csv as one row per trial: the old platform\'s rows from 9 June 2025 carry Toronto time '
          'stamped Z, and its copies of web and phone sign-ups, which match a new-platform row field for field once re-timed, '
          'were dropped; trials counted by start date in Toronto time (conversion_standard_v3.pdf, section 2): %s and %s in '
          'the two winters.' % (c(F['stage_trials_w24']), c(F['stage_trials_w25'])),
          '2. Linked each trial to its first-charge attempts in charges_processor_a_2024-11_2025-09.csv and '
          'charges_processor_b_2025-09_2026-02.csv through the subscription it ended on (plan_changes.csv; section 4): '
          'conversion %.1f per cent last winter and %.1f per cent this winter, about %s paid conversions at this winter\'s '
          'trials.' % (F['paid_rate_w24'], F['paid_rate_w25'], c(F['conv_fall'])),
          '3. Set each trial\'s plays in trial_viewing_2024-11_2026-02.parquet (legacy numbers through account_crosswalk.csv and '
          'content_crosswalk.csv) against release_calendar.xlsx: last winter %.1f per cent of trials had played a season whose '
          'last episode came out after their trial ended and paid at %.1f per cent, against %.1f per cent for the rest; this '
          'winter none had.' % (F['runway_share_w24'], F['paid_rate_w24_runway'], F['paid_rate_w24_norunway']),
          '4. The slate: last winter\'s %.1f per cent less %.1f per cent, at this winter\'s trials: %s; first-charge recovery: '
          'declined first charges recovered fell from %.1f to %.1f per cent, on this winter\'s declined first charges: %s; the '
          'channel mix: last winter\'s channel shares at this winter\'s paid rate by channel: %s; the price takes the rest: %s.'
          % (F['paid_rate_w24'], F['paid_rate_w24_norunway'], c(F['conv_slate']), F['recovered_w24'], F['recovered_w25'],
             F['conv_recovery'], F['conv_channel'], F['conv_price']),
          '5. Paid, trials started February to October 2025: a plan change made on the old platform before 9 June '
          'or in the apps before 14 October opened a subscription that no file links to its trial; each such first charge was '
          'matched to the trial without a charge whose end most closely precedes its first attempt, in the provinces its tax '
          'rate names: the shares in block 4.',
          '6. Episodes, the same trials: the smart TV app\'s rows from 8 February to 27 October 2025 each cover an autoplay run, the '
          'episode named and the season\'s following episodes as far as the minutes reach on the calendar\'s runtimes; episodes '
          'counted once a trial (section 5) and averaged over every trial, including those that played nothing: the averages in block 4.',
          '7. Ranked the four causes: the slate at %s against %s for the price takes the budget.'
          % (c(F['conv_slate']), F['conv_price']), '']
    L += ['## 4. Deliverable Answers', '', '### trial_conversion_review.xlsx', '',
          '1. Share of each winter\'s November to January trials that played an episode: %.1f per cent in 2024-25, %.1f per '
          'cent in 2025-26.' % (F['stage_played_w24'], F['stage_played_w25']),
          '2. Share still subscribed when the trial ended: %.1f per cent and %.1f per cent.'
          % (F['stage_subscribed_w24'], F['stage_subscribed_w25']),
          '3. Share of their first charges collected: %.1f per cent and %.1f per cent.'
          % (F['stage_collected_w24'], F['stage_collected_w25']),
          '4. Paid conversions each programme\'s cause cost this winter\'s trials, to the nearest hundred:',
          '   - (A) First-month price hold: %s' % c(F['conv_price']),
          '   - (B) First-charge payment recovery: %s' % c(F['conv_recovery']),
          '   - (C) Winter release slate: %s' % c(F['conv_slate']),
          '   - (D) Paid acquisition mix: %s' % c(F['conv_channel']),
          '5. Programme to fund: (C) the winter release slate.',
          '6. Runner-up: (A) the first-month price hold.',
          '7. Gap: %s paid conversions.' % c(F['conv_gap']),
          '8. Trials started in each month of 2025, share that paid and average number of episodes played during the trial:']
    for k, nm in MONTHS:
        L.append('   - %s: %.1f per cent, %.1f episodes' % (nm, F['ask_paid_share_%s' % k], F['ask_episodes_%s' % k]))
    L += ['', '### winter_conversion_note.pdf', '',
          '1. Waterfall from last winter\'s conversion rate at this winter\'s trials, %s paid conversions, to this winter\'s %s, '
          'one bar per programme\'s cause: the slate %s, the price %s, first-charge recovery %s, the paid acquisition mix %s.'
          % (c(F['waterfall_start']), c(F['waterfall_end']), c(F['conv_slate']), F['conv_price'], F['conv_recovery'],
             F['conv_channel']), '']
    with open(os.path.join(TASK, 'submission.md'), 'w') as f:
        f.write('\n'.join(L))


if __name__ == '__main__':
    main()
