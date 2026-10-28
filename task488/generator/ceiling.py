"""The pair ceiling on the cut pack (supplemental-stumping Part 0), on the rubric weights 38 / 7 / 55.

The cracker lands the call, runs the hygiene battery and executes every filed rule: it loads each authored item once
under its active version's key (specification section 1), takes the active version row as the item's record when the
bank's key fans out across the catalog's versions, reports the domain from that row's 2026 framework code or else the
crosswalk with its skill-tag condition, and builds the enemy sets from the active rows by authoring id, one grade at a
time, two or more to a set (section 4). The mirror stops at the default path (it misses the call, keeping about 5 of
the 38) and builds the asks from the bank export alone: every operational row, its 2010 standard through the
crosswalk, and the enemy groups of the catalog rows its keys match. Each ask figure is a hit when it equals the
golden."""
from __future__ import annotations

import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import params as P  # noqa: E402

W_CALL, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0


def xw_domain(xw, code, skill):
    c = xw[xw.standard_code_2010 == code]
    if len(c) > 1:
        hit = c[c.condition == "skill tag: %s" % skill]
        c = hit if len(hit) else c[c.condition == "other skill tags"]
    return c.framework_domain_2026.iloc[0]


def sets_of(pairs, grade_of):
    mem = {}
    for who, eg in pairs:
        if eg and who in grade_of:
            mem.setdefault((eg, grade_of[who]), set()).add(who)
    return {g: (sum(1 for (e, gg), m in mem.items() if gg == g and len(m) >= 2),
                sum(len(m) for (e, gg), m in mem.items() if gg == g and len(m) >= 2)) for g in P.GRADES}


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bank = pd.read_csv(os.path.join(T, "tessaline_item_bank_export_20270331.csv"))
    cat = pd.read_excel(os.path.join(T, "qrac_item_authoring_catalog_20270315.xlsx")).fillna("")
    xw = pd.read_csv(os.path.join(T, "qrac_framework_crosswalk_2010_to_2026.csv")).fillna("")
    op = bank[bank.status == "operational"]
    std = dict(zip(bank.item_key, bank.standard_code))
    # the cracker
    act = cat[(cat.status == "active") & cat.item_key.isin(set(op.item_key))]
    c_dom = {}
    for r in act.itertuples():
        d = r.framework_code_2026.split(".")[0] if r.framework_code_2026 else xw_domain(xw, std[r.item_key], r.skill_tag)
        c_dom[(int(r.grade), d)] = c_dom.get((int(r.grade), d), 0) + 1
    c_en = sets_of(zip(act.authoring_id, act.enemy_group), dict(zip(act.authoring_id, act.grade.astype(int))))
    # the mirror
    m_dom = {}
    for b in op.itertuples():
        d = xw_domain(xw, b.standard_code, "")
        m_dom[(int(b.grade), d)] = m_dom.get((int(b.grade), d), 0) + 1
    eg_by_key = cat[cat.status == "active"].groupby("item_key").enemy_group.last()
    m_en = sets_of(((k, eg_by_key.get(k, "")) for k in op.item_key), dict(zip(op.item_key, op.grade.astype(int))))
    keep = {}
    for who, dm, en in (("cracker", c_dom, c_en), ("mirror", m_dom, m_en)):
        hits = []
        for g in P.GRADES:
            for k in sorted(k for k in fig if k.startswith("dom_%d_" % g)):
                d = k.split("_")[2]
                hits.append(("dom %d %s" % (g, d), dm.get((g, d), 0) == fig[k]))
            hits.append(("sets %d" % g, en[g][0] == fig["enemy_sets_%d" % g]))
            hits.append(("set items %d" % g, en[g][1] == fig["enemy_items_%d" % g]))
        kept = [k for k, h in hits if h]
        keep[who] = len(kept) / len(hits)
        print("%-8s keeps %d of %d ask figures: %s" % (who, len(kept), len(hits), ", ".join(kept) or "none"))
    C = W_CALL + W_IF + W_ASK * keep["cracker"]
    S = R_MISS + W_IF + W_ASK * keep["mirror"]
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight"
          % (C, S, (C + S) / 2, 100 * keep["mirror"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
