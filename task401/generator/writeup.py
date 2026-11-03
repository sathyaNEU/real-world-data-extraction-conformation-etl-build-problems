"""task401: submission.md from generator/figures.json (every figure emitted, none typed).
    python3 writeup.py
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); TASK = os.path.dirname(HERE)
F = json.load(open(os.path.join(HERE, 'figures.json')))
WEEKS = ['1 September', '8 September', '15 September', '22 September', '29 September', '6 October', '13 October',
         '20 October', '27 October']
MONTHS = [(7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
CH = ['Direct web', 'Comparison site', 'Phone', 'Broker']
s0, s1, fall = F['share_h1_2025'], F['share_h1_2026'], F['fall_points']
e, g = F['ask_a']['elec_gwh'], F['ask_a']['gas_gwh']
n = lambda v: '{:,}'.format(v)

L = []
L += ['## Tags', '',
      '**Domain:** Marketing & Consumer Research, customer satisfaction driver analysis (a GB domestic energy supplier\'s '
      'six-month new-customer satisfaction tracker).  ',
      '**Analytical objective:** Root-Cause Analysis (what pulled six-month satisfaction down between the first halves of '
      '2025 and 2026, and whether any of the fall belongs to the new billing platform before phase 2 cuts over).', '']
L += ['## 1. Final Recommendation', '',
      '**The fall in six-month satisfaction from %.1f to %.1f per cent belongs to the quote journey relaunched in May 2025, '
      'which stopped pre-filling each meter point\'s industry annual quantity, not to the billing platform, so phase 2 can '
      'cut over on 1 February 2027.**' % (s0, s1), '',
      'More than half of the %.1f-point fall sits with customers whose meter points\' annual quantities cost more than '
      'their quote, while customers whose quote covered that cost held their H1 2025 level on the new platform. Not the '
      'billing platform, which the billing ratings point at only because those bills ran above the quote. Not the October '
      '2025 tariff rise or the November 2025 contact centre move, each a point or two at most. Not the survey vendor '
      'change, across which the covered customers held their level.' % fall, '']
L += ['## 2. Critical Components', '',
      '1. Share satisfied (4 or 5 on the overall question, first answered response per account): **%.1f per cent** in H1 '
      '2025 and **%.1f per cent** in H1 2026, a fall of **%.1f points**.' % (s0, s1, fall),
      '2. The quote journey\'s quotes, costed against the annual quantities each customer\'s meter points then carried, '
      'carry **more than half** of the fall.',
      '3. Customers whose quote covered that cost were as satisfied in H1 2026 on the new platform as in H1 2025 on the '
      'legacy one.', '']
L += ['## 3. Step-by-Step Solution', '',
      '1. Read six_month_survey_2025H1.csv and survey_export_6m_2026-01-01_2026-06-30.csv per the measurement framework '
      '(labels by its scale table, 2026 times in UK time, the first answered response per account): %.1f and %.1f per cent '
      'satisfied, a fall of %.1f points.' % (s0, s1, fall),
      '2. Linked each respondent to the accepted quote its registration names in supply_registrations_2024-05_2025-12.csv '
      '(2026 platform numbers back to legacy numbers through phase1_migration_loads.jsonl) and costed, at that quote\'s '
      'rates in tariff_rates_2024-04_2026-06.xlsx, the annual quantities in force on the response date in '
      'meter_point_annual_quantities.parquet.',
      '3. Fitted satisfaction on the metered cost against the quote (kinked at zero) with the tariff rise, the contact '
      'centre and the 2026 term, and split the fall over the four causes in every order: the quote\'s part is more than '
      'half, and customers whose quote covered the cost held their level.',
      '4. Phase 2 scope: replayed switching_flows_2026-05-01_2026-11-05.csv to 1 November 2026 per the cutover plan (a meter '
      'point returned after an erroneous transfer is ours), gave each meter point to the account in '
      'legacy_accounts_extract_2026-10-31.csv that took it on last (a leaving occupier\'s account waiting for its final '
      'bill no longer counts), and summed each meter point\'s registers on its latest revision on or before that day: the '
      'regional counts, and %.1f GWh of electricity and %.1f GWh of gas for phase 2 as a whole.' % (e, g),
      '5. Phase 1 moves: walked each load in phase1_migration_loads.jsonl back through the platform number it was sourced '
      'from, took each account\'s last load in UK time with that load\'s fuels, and per the cutover plan left out the '
      'accounts legacy_accounts_extract_2026-10-31.csv shows live on the legacy platform again by the end of 2 November '
      '2025 (an account it shows taken back on a later date was moved): the weekly counts below.',
      '6. Switches: one per accepted quote in the registrations, no withdrawn registration counted, in the month its first '
      'supply started, credited to the channel of the prospect\'s quote in quote_log_2024-05_2025-12.csv dated on or before '
      'the registration (a later phone re-quote does not move it): the monthly counts below.',
      '7. The platform is not the cause of the fall; phase 2 can cut over on 1 February 2027 and the fix is the quote '
      'journey.', '']
L += ['## 4. Deliverable Answers', '', '### six_month_satisfaction_review.pdf', '',
      '1. The fall belongs to the quote journey\'s quotes since the May 2025 relaunch, not to the billing platform; phase 2 '
      'can cut over.',
      '2. Share satisfied %.1f per cent in H1 2025 and %.1f per cent in H1 2026, a fall of %.1f points, more than half of it '
      'the quote journey\'s.' % (s0, s1, fall),
      '3. Bridge chart on page 1 from %.1f to %.1f per cent, the quote journey\'s quotes the largest step.' % (s0, s1), '',
      '### phase2_readiness.xlsx', '',
      '1. Accounts phase 2 will move, by region, whole numbers:']
L += ['   - %s: %s' % (r, n(F['ask_a']['counts'][r])) for r in sorted(F['ask_a']['counts'])]
L += ['2. Total annual quantity of all the meter points phase 2 will move, GWh to one decimal: electricity %.1f, gas %.1f.' % (e, g),
      '3. Accounts phase 1 moved each week, whole numbers:']
L += ['   - Week commencing %s 2025: electricity-only %s, dual fuel %s' % (w, n(F['ask_b']['%d|ELEC' % k]), n(F['ask_b']['%d|DUAL' % k]))
      for k, w in enumerate(WEEKS, 1)]
L += ['4. Switches each sales channel brought in, by the month first supply started, whole numbers:']
L += ['   - %s 2025: %s' % (name, ', '.join('%s %s' % (c, n(F['ask_c']['%s|%d' % (c, m)])) for c in CH)) for m, name in MONTHS]
open(os.path.join(TASK, 'submission.md'), 'w').write('\n'.join(L) + '\n')
print('submission.md written')
