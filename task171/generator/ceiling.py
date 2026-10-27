"""The ask sheet's cracker and mirror, run on the cut pack.

The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out) and
executes every filed rule (SAP 6.2 to 6.10); the mirror stops at the call's most attractive wrong rung and takes each
ask's natural read. Each keeps an ask figure when its handling lands within half a unit of the figure's rounding.

    python3 task171/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks as AK          # noqa: E402
import common as K         # noqa: E402
import pack_read as PR     # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
WEIGHT = {"A": 6, "B": 6, "C": 6}


def figures(a, b, c):
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        out[('A', arm, 'si')] = a[arm]['pts_si']
        out[('A', arm, 'irr')] = a[arm]['pts_irr']
        out[('A', arm, 'rate')] = round(a[arm]['rate_si'], 1)
        for v in ('Week 4', 'Week 8', 'Week 12'):
            out[('B', arm, v)] = round(b[arm][v]['pct'], 1)
        for w, _ in K.DIARY_WEEKS:
            out[('C', arm, w)] = c[arm][w]['rem']
    return out


def run():
    P = PR.read(TARGET)
    gold = figures(AK.ask_a(P, TARGET), AK.ask_b(P, TARGET), AK.ask_c(P, TARGET))
    # the cracker runs the hygiene battery and every filed rule: adverse event episodes keyed by patient, term and
    # onset as recorded (SAP 6.2 and 6.5 executed on them); immunogenicity per patient and visit on the manifest,
    # rejected runs dropped, each tier's latest accepted result; the diary on the dispensing log's effective dates,
    # entries whose holder the trial database does not know set aside
    crack = figures(AK.ask_a(P, TARGET, 'onset_key'), AK.ask_b(P, TARGET, 'by_visit'), AK.ask_c(P, TARGET, 'drop_unmatched'))
    # the mirror: every adverse event record an event, the reaction preferred term alone; each sample's latest result
    # as delivered; diary entries to the handset's current holder
    mirror = figures(AK.ask_a(P, TARGET, 'records'), AK.ask_b(P, TARGET, 'latest'), AK.ask_c(P, TARGET, 'current_holder'))
    m_irr = AK.ask_a(P, TARGET, 'irr_term_only')
    for arm in ('dovikizumab', 'placebo'):
        mirror[('A', arm, 'irr')] = m_irr[arm]['pts_irr']
    def keep(sheet):
        k = {a: 0 for a in WEIGHT}
        for key, v in sheet.items():
            g = gold[key]
            tol = 0.05 if isinstance(g, float) else 0.5
            if abs(v - g) <= tol:
                k[key[0]] += 1
        return k
    kc, km = keep(crack), keep(mirror)
    tot = sum(WEIGHT.values())
    lc = sum(kc.values()) / tot
    ls = sum(km.values()) / tot
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * ls
    return dict(cracker=kc, mirror=km, Lc=lc, Ls=ls, pair=(C + S) / 2, mirror_leak=100 * ls)


if __name__ == "__main__":
    print(json.dumps(run(), indent=1))
