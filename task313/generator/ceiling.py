"""The ask sheet's numbers, measured on the cut pack: the cracker (on the call, every filed rule and the hygiene
battery executed, the devices unhandled), the mirror (the default path's call, the same careful asks) and the
partial includers, each scored figure by figure against figures.json on 38 / 7 / 55.

    python3 task313/generator/ceiling.py [target_dir]
"""
import hashlib
import json
import os
import sys
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0


def digest(tgt):
    h = hashlib.sha256()
    for n in sorted(os.listdir(tgt)):
        with open(os.path.join(tgt, n), 'rb') as f:
            h.update(n.encode() + f.read())
    return h.hexdigest()[:16]


def score_call(posts, total, F):
    hits = sum(1 for u, p in posts.items() if F['call']['posts'][u] == p) + (1 if total == F['call']['readmissions_avoided_2027_28'] else 0)
    return hits, 6


def score_asks(a, b, F):
    rows = []
    for r, g in F['ask_a'].items():
        rows.append(('A %s usual-care rate' % r, g['usual_care_rate_pct'], a[r]['usual_care_rate_pct'],
                     abs(a[r]['usual_care_rate_pct'] - g['usual_care_rate_pct']) < 0.05 - 1e-9))
        rows.append(('A %s risk ratio' % r, g['risk_ratio'], a[r]['risk_ratio'], abs(a[r]['risk_ratio'] - g['risk_ratio']) < 0.005 - 1e-9))
    for r, g in F['ask_b'].items():
        for kk in ('home_visits', 'calls'):
            rows.append(('B %s %s' % (r, kk), g[kk], b[r][kk], abs(b[r][kk] - g[kk]) < 0.005 - 1e-9))
    return rows


def row_score(call_hits, ask_rows):
    kept = sum(1 for r in ask_rows if r[3])
    return W_CALL * call_hits / 6 + W_IF + W_ASK * kept / len(ask_rows), kept


def main():
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, 'target')
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    # the cracker: the call landed; final list, discharge-record reasons, NHS number or index, unplanned methods,
    # 28 days, contact ids once, NA and TNA dropped; rows under a mother's number and the failed attempts filed
    # before the new codes are not seen
    a_cr = V.ask_a(tgt, mother_map=False)
    b_cr = V.ask_b(tgt, call_mother_map=False, split_pre_update=False)
    cr_rows = score_asks(a_cr, b_cr, F)
    c_hits = score_call(F['call']['posts'], F['call']['readmissions_avoided_2027_28'], F)[0]
    C, c_kept = row_score(c_hits, cr_rows)
    # the mirror: the default path's call (the trial ratio carried to every readmission), the same asks
    m = V.call(tgt, reached_only=False)
    m_total = F['default_path']['readmissions_avoided']
    m_hits = score_call(m['posts'], m_total, F)[0]
    S, m_kept = row_score(m_hits, cr_rows)
    # partial includers: one device handled at a time
    parts = {}
    for name, a, b in (('mother rows mapped (admissions and calls)', V.ask_a(tgt), V.ask_b(tgt, split_pre_update=False)),
                       ('pre-update attempts split, mothers unmapped', V.ask_a(tgt, mother_map=False), V.ask_b(tgt, call_mother_map=False)),
                       ('calls under the mother mapped, admissions not', V.ask_a(tgt, mother_map=False), V.ask_b(tgt, split_pre_update=False)),
                       ('admissions under the mother mapped, calls not', V.ask_a(tgt), V.ask_b(tgt, call_mother_map=False, split_pre_update=False))):
        rows = score_asks(a, b, F)
        parts[name] = sum(1 for r in rows if r[3])
    pair = (C + S) / 2
    print('pack digest %s' % digest(tgt))
    print('cracker: call %d of 6, asks kept %d of %d, score %.1f' % (c_hits, c_kept, len(cr_rows), C))
    print('mirror: call %d of 6 (posts %s, total %d), asks kept %d of %d, score %.1f' % (m_hits, m['posts'], m_total, m_kept, len(cr_rows), S))
    print('Pair ceiling: %.1f' % pair)
    print('Mirror leakage: %.1f per cent of ask weight' % (100.0 * m_kept / len(cr_rows)))
    for k, v in parts.items():
        print('includer, %s: asks kept %d of %d' % (k, v, len(cr_rows)))
    print('| Ask figure | Cracker | Golden | Cracker |')
    for name, g, x, hit in cr_rows:
        print('| %s | %s | %s | %s |' % (name, x, g, 'keeps' if hit else 'miss'))
    return dict(C=C, S=S, pair=pair, c_kept=c_kept, m_kept=m_kept, parts=parts, rows=cr_rows)


if __name__ == '__main__':
    main()
