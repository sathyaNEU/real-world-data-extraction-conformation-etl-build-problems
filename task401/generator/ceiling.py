"""The ask sheet as code on the cut pack: the cracker, the full includer, the no-repair reader and the mirror, each scored
figure by figure against the golden (a hit rounds to the same stated unit: admissions to 10, fees to GBP 100).

    python3 ceiling.py      prints the sheet and the pair ceiling; exit 1 if the ceiling is over 60

The cracker landed the call and runs the hygiene battery: returned and voided lines out, pence to pounds, every line read
as one admission or as the fees of its own date and payer. The full includer also reads family tickets by their price,
counts a Swim and Gym ticket's two lines once, dates bureau A by the day after processing, sends re-presentations and a
bureau's own returned collections to their months, splits a household's collection by its members' fees and leaves the
administration charge out; it nets every refund and keeps an amount no return of the same reference explains in the month
it came in. The mirror is the best response off the call, handling the asks as the cracker does (they do not turn on the
call)."""
import os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks


def score():
    gt, gd = asks.till_count('golden'), asks.dd_count('golden')
    rows = {}
    for route in ('cracker', 'full', 'norepair'):
        t, d = asks.till_count(route), asks.dd_count(route)
        rows[route] = (sum(round(t[k] / 10) == round(gt[k] / 10) for k in gt), sum(round(d[k] / 100) == round(gd[k] / 100) for k in gd))
    rows['mirror'] = rows['cracker']
    return rows, len(gt), len(gd)


def main():
    rows, na, nb = score()
    z = os.path.join(os.path.dirname(HERE), 'target.zip')
    digest = hashlib.sha256(open(z, 'rb').read()).hexdigest()[:12] if os.path.exists(z) else 'no zip'
    print('pack digest %s' % digest)
    print('%-10s %14s %12s %8s' % ('route', 'admissions', 'fees', 'share'))
    for r, (a, b) in rows.items():
        print('%-10s %10d/%-3d %8d/%-3d %7.1f%%' % (r, a, na, b, nb, 100.0 * (a + b) / (na + nb)))
    L = lambda r: (rows[r][0] + rows[r][1]) / (na + nb)
    C = 38 + 7 + 55 * L('cracker'); S = 5 + 7 + 55 * L('mirror')
    Cf = 38 + 7 + 55 * L('full'); Sf = 5 + 7 + 55 * L('full')
    pair = (C + S) / 2; pair_full = (Cf + Sf) / 2
    print('cracker on the call %.1f, mirror off it %.1f: pair %.1f' % (C, S, pair))
    print('two full includers, one on the call and one off it: pair %.1f' % pair_full)
    print('mirror leakage %.1f%%' % (100 * L('mirror')))
    worst = max(pair, pair_full)
    print('pair ceiling %.1f' % worst)
    return 1 if worst > 60 else 0


if __name__ == '__main__':
    raise SystemExit(main())
