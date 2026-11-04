"""task401: submission.md from generator/figures.json (every figure emitted, never typed).

    python3 writeup.py            writes <task>/submission.md
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
F = json.load(open(os.path.join(HERE, 'figures.json')))
NAMES = {'01': 'January', '02': 'February', '03': 'March', '10': 'October', '11': 'November', '12': 'December',
         '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September'}


def ml(m):
    return '%s %s' % (NAMES[m[5:]], m[:4])


def main():
    n, p, reach, none = F['exc_window'], F['exc_prior'], F['dairy_reach'], F['upgrade_reach']
    L = []
    L += ['## Tags', '',
          '**Domain:** Physical & Environmental Sciences, pollution source attribution (a river\'s ammonia failures below a '
          'sewage works, and the nitrification upgrade in a water company\'s environment programme submission).  ',
          '**Analytical objective:** Root-Cause Analysis (what drove the River Allery\'s exceedance days below Coldmere this '
          'winter, and whether the upgrade would stop them).', '']
    L += ['## 1. Final Recommendation', '',
          '**Thornlea Dairy\'s evening acid whey discharges drive the Allery\'s ammonia failures, and the GBP %.1f million '
          'nitrification upgrade would not stop them, so it does not belong in the submission as the answer.** All %d '
          'exceedance days from November 2025 to March 2026 fell on the first or second day after an evening on which the '
          'dairy ran whey to its drain, and none fell on load and cold alone. Not the aeration control, which went live a '
          'week before the dairy\'s new line and reaches %d of the %d days. Not the works\' capacity in the cold, which met '
          'the river standard on every day without a whey evening before it.' % (F['upgrade_cost_m'], n, none, n), '']
    L += ['## 2. Critical Components', '',
          '1. Exceedance days at the downstream monitor, November 2025 to March 2026: **%d**, against **%d** in the same '
          'months a year earlier.' % (n, p),
          '2. Exceedance days on the first or second day after a Thornlea whey evening in its chamber record: **%d of %d**.'
          % (reach, n),
          '3. Exceedance days with no whey evening on the two evenings before, all the aeration control or the upgrade '
          'could reach: **%d**.' % none, '']
    L += ['## 3. Step-by-Step Solution', '',
          '1. Formed UK days from the downstream monitor\'s valid fifteen-minute readings and counted the days above %.1f '
          'mg/l as the investigation terms define them: %d from November 2025 to March 2026, %d a year earlier.'
          % (F['standard_mg_l'], n, p),
          '2. Joined the historian\'s final-effluent ammonia across the October 2025 tag rename: the works\' effluent fails '
          'on each exceedance day and runs normally between them.',
          '3. Picked out of thornlea_dairy_discharge_monitor_15min.csv the evenings with low pH at production flow after '
          '20:00 (the whey), apart from the dairy\'s night-time acid rinses.',
          '4. Marked the first and second day after each whey evening: all %d exceedance days fall on them and none off '
          'them, and every recovery window from one to five days gives the same %d.' % (n, reach),
          '5. Checked the other options against the same days: no exceedance day lacks a whey evening before it, so the '
          'aeration control and the upgrade reach %d of %d.' % (none, n),
          '6. Took each discharger\'s chargeable volume from the 00:00 1 April reads at its consent\'s meter point, split '
          'at the exchange reads for the brewery and the meat plant, times the consent\'s multiplier and allowance.',
          '7. Took each composite collected in 2025-26 as the bottles one round collected at the consented point (the round '
          'sheet\'s bottle number against te_sampler_downloads_2025-01_2026-04.csv), at the volume-weighted strength of the '
          'effluent the bottles hold, and averaged the composites\' settled COD and suspended solids.',
          '8. Recommendation: the upgrade reaches %d of the %d days; review Thornlea\'s consent so whey no longer reaches '
          'the drain.' % (none, n), '']
    L += ['## 4. Deliverable Answers', '', '### coldmere_ammonia_briefing.pptx', '',
          '1. The call: Thornlea Dairy\'s evening whey discharges drive the failures; the aeration control and the upgrade '
          'reach %d of the %d exceedance days and stopping the discharges reaches all %d.' % (none, n, reach),
          '2. Slide 3 carries the drill-down chart on one daily axis, November 2025 to March 2026: the river\'s day means '
          'with the %.1f mg/l standard and the exceedance days marked, the works\' final effluent ammonia with the same days '
          'marked, and the dairy\'s whey evenings.' % F['standard_mg_l'],
          '3. Slides 4 and 5 carry the case against the upgrade (no exceedance day without a whey evening before it, the '
          'standard met on every other day) and the recommendation.', '',
          '### coldmere_evidence.xlsx', '']
    win = ', '.join('%s %d' % (NAMES[m[5:]], v) for m, v in F['exc_by_month_window'].items())
    prv = ', '.join('%s %d' % (NAMES[m[5:]], v) for m, v in F['exc_by_month_prior'].items())
    L += ['1. Exceedance days by month, November 2025 to March 2026: %s.' % win,
          '2. Exceedance days by month a year earlier, November 2024 to March 2025: %s.' % prv,
          '3. Trade dischargers, 2025-26: chargeable volume in m3, settled COD strength and suspended solids strength in '
          'mg/l:']
    for name in sorted(F['ask_a']):
        v = F['ask_a'][name]
        L.append('   - %s: %s m3, settled COD %s mg/l, suspended solids %s mg/l' % (
            name, format(v['volume'], ','), format(v['ot'], ','), format(v['st'], ',')))
    L.append('')
    open(os.path.join(TASK, 'submission.md'), 'w').write('\n'.join(L))


if __name__ == '__main__':
    main()
