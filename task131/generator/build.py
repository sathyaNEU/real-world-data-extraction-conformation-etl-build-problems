"""Build task131's evidence pack into <out>/ (default: task131/target)."""
import argparse
import datetime as dt
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim as S
import extracts as X
import docs as D
import distract as Q
import estimators as E
import postprocess as P

TASK = os.path.dirname(HERE)

FILES = {
    "facts": "card_week_sales_2026w15_w34.parquet",
    "alloc": "st26_offer_allocation.csv",
    "cards": "member_cards.csv",
    "memb": "memberships.csv",
    "branches": "branches_2026-01.csv",
    "notice": "network_changes_2026-07-01.docx",
    "standard": "MP-3_measuring_offers_rev3.pdf",
    "catalogue": "st26_offer_catalogue.json",
    "plan": "programme_plan_2027.xlsx",
    "notes": "crm_extract_field_notes.md",
    "log": "extract_log_2026-09-14.txt",
    "footfall": "branch_footfall_2026w15_w34.csv",
    "panel": "member_panel_2026-06.xlsx",
    "competitors": "competitor_price_checks_2026.csv",
}
DISTRACTORS = ["footfall", "panel", "competitors"]


def plan_numbers(sim, chain):
    """2026 average active cards and the 2027 plan by region, with the plan total placed so every
    offer's 2027 value sits inside its CHF-thousand bin, clear of the edges and of round figures."""
    reg_c = sim["reg"][sim["m_idx"]]
    drift = {"SGS": 1.006, "FUE": 0.991, "RHT": 1.003, "TGO": 0.996, "TOG": 0.988, "APZ": 1.009}
    active = {r: int(round((reg_c == r).sum() * drift[r])) for r, _ in W.REGIONS}
    growth = {"SGS": 1.021, "FUE": 1.014, "RHT": 1.018, "TGO": 1.011, "TOG": 1.006, "APZ": 1.016}
    planned = {r: int(round(active[r] * growth[r] / 10.0) * 10) for r, _ in W.REGIONS}
    order = [r for r, _ in W.REGIONS]
    edge = lambda v: 0.5 - abs(v / 1000 - round(v / 1000))      # distance to the bin edge, in thousands
    base = dict(planned)
    for k in [0] + [s * i for i in range(1, 300) for s in (1, -1)]:
        trial = dict(base)
        for i in range(abs(k)):
            trial[order[i % 6]] += 10 if k > 0 else -10
        tot = sum(trial.values())
        vals = [chain[x] * 52 * tot for x in W.OFFERS]
        if all(edge(v) >= 0.2 for v in vals) and all(abs(v - round(v, -4)) > 1500 for v in vals):
            return active, trial
    raise SystemExit("no plan total clears every bin")


def build(out, quiet=False):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    s = S.simulate()
    s = S.force_cells(s)
    s = S.round_cents(s)

    facts = X.facts_frame(s)
    alloc = X.allocation_frame(s)
    cards = X.cards_frame(s)
    memb = X.memberships_frame(s)
    br = X.branches_frame()

    p = lambda k: os.path.join(out, FILES[k])
    facts.to_parquet(p("facts"), index=False, compression="snappy")
    alloc.to_csv(p("alloc"), index=False)
    cards.to_csv(p("cards"), index=False)
    memb.to_csv(p("memb"), index=False)
    br.to_csv(p("branches"), index=False)

    chain = E.answer_net_same_cell(facts, alloc[["card_no", "cell"]], cards)
    active, planned = plan_numbers(s, chain)
    D.plan_xlsx(p("plan"), planned, active)
    D.standard_pdf(p("standard"))
    D.network_notice_docx(p("notice"))
    D.catalogue_json(p("catalogue"))
    D.field_notes_md(p("notes"))
    n_foot = Q.footfall_csv(p("footfall"), s)
    Q.panel_survey_xlsx(p("panel"))
    Q.competitor_checks_csv(p("competitors"))
    counts = {FILES["facts"]: len(facts), FILES["alloc"]: len(alloc), FILES["cards"]: len(cards),
              FILES["memb"]: len(memb), FILES["branches"]: len(br), FILES["footfall"]: n_foot}
    D.extract_log_txt(p("log"), counts)

    for k in ("notice", "plan"):
        P.normalize_zip(p(k))
    P.normalize_zip(p("panel"))
    P.normalize_pdf(p("standard"))
    # one coherent export date for the pack
    ts = dt.datetime(2026, 9, 14, 9, 30).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (ts, ts))
    if not quiet:
        print("built", out, len(os.listdir(out)), "files;", len(facts), "card-week rows")
    return s, dict(facts=facts, alloc=alloc, cards=cards, memb=memb, branches=br, planned=planned,
                   active=active)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    a = ap.parse_args()
    build(a.out)
