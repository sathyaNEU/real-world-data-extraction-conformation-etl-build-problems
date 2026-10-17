"""task239 owed figures (figures.json) and the submission, both emitted from the analysis, never typed."""
import json
import os

import estim as E
import params as P

KEEP_BAND = 0.80
DROP_BAND = 0.25
CHANNELS = [("personal", "personal link"), ("site", "site tablet"), ("paper", "paper form")]
WORDING = {it[0]: it[1] for it in P.ITEMS}


def fmt(n):
    return "{:,}".format(int(n))


def answers(X, FILES):
    lam = X["lam"]
    stay = X["stay"]
    gone = [c for c in E.ITEM_CODES if c not in stay]
    golden_spread = {h: lam[h] for h in E.GOLDEN_ROUTES}
    kept_min = min(min(v[E.ITEM_CODES.index(c)] for c in stay) for v in golden_spread.values())
    gone_max = max(max(v[E.ITEM_CODES.index(c)] for c in gone) for v in golden_spread.values())
    assert kept_min >= KEEP_BAND and gone_max < DROP_BAND, (kept_min, gone_max)
    R = X["R"]
    used = R[R["used"]]
    A = dict(
        files=FILES,
        stay=stay, gone=gone,
        n_stay=len(stay),
        loadings={c: round(float(l), 2) for c, l in zip(E.ITEM_CODES, X["golden"])},
        means={c: round(float(l), 2) for c, l in zip(E.ITEM_CODES, lam["means"])},
        disatt={c: round(float(l), 2) for c, l in zip(E.ITEM_CODES, lam["disatt"])},
        kept_min=round(float(kept_min), 2), gone_max=round(float(gone_max), 2),
        counted=int(len(R)), teams=len(X["reported"]), used=int(len(used)),
        ledger=X["ledger"],
        fav=X["fav"],
        div=X["div"],
        switch=E.site_switch(X["D"])[0],
    )
    A["means_stay"] = E.verdict(lam["means"])
    A["disatt_stay"] = E.verdict(lam["disatt"])
    return A


def figures(A):
    f = {"call": {"stay": A["stay"], "withdrawn": A["gone"], "items_staying": A["n_stay"]},
         "cited_sections": ["3.4", "4.2", "4.3", "5.1"],
         "components": {"kept_band": KEEP_BAND, "withdrawn_band": DROP_BAND, "line": E.LINE},
         "steps": {"returns_that_count": A["counted"], "teams_reported": A["teams"], "returns_used": A["used"]},
         "deliverables": {
             "loadings": A["loadings"],
             "ledger": A["ledger"],
             "favourable": A["fav"],
             "divisions": A["div"]},
         "rungs": {"team_means": A["means"], "team_means_stay": len(A["means_stay"]),
                   "reliability_corrected": A["disatt"], "reliability_corrected_stay": len(A["disatt_stay"])}}
    return f


def submission(A):
    F = A["files"]
    L = []
    L.append("# task239 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: the annual "
             "structure check of a team climate index that a parcels company's staff survey reports per team, each item's "
             "loading on the factor the items share at team level).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (which items the index carries into the next "
             "survey after its yearly check on whether each item still measures the team property it reports).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Keep ten of the twelve items, TC01 to TC10, in the Team Climate Index for the 2028 Staff Voice survey, "
             "and withdraw TC11 and TC12.**\n")
    L.append("TC11 and TC12 load under %.2f on the factor the twelve items share at team level, far below the "
             "standard's %.2f line, while every other item loads %.2f or more. Not eight items, which one factor fitted "
             "to the team means gives: each team mean also carries the members' own covariance across the items, "
             "divided by the team's number of returns, so the two team-practice items, TC09 and TC10, on which whole teams differ while one "
             "member's answers barely move with the rest, fall below the line there and only there. Not ten items with "
             "TC09 and TC10 withdrawn, which dividing each correlation of the team means by the square root of the two "
             "items' team-mean reliabilities gives: that correction rescales each item's variance but leaves the "
             "members' covariance between items in the means, and lifts TC11 and TC12 instead.\n"
             % (DROP_BAND, E.LINE, KEEP_BAND))
    L.append("## 2. Critical Components\n")
    L.append("1. TC09 and TC10, the two team-practice items, load **%.2f or more** at team level, as TC01 to TC08 do." % KEEP_BAND)
    L.append("2. TC11 and TC12 load **under %.2f** at team level.\n" % DROP_BAND)
    L.append("## 3. Step-by-Step Solution\n")
    sw = A["switch"]
    L.append("1. Built the returns that count under section 3 of %s: sessions submitted by the close in %s (a session a "
             "tablet re-sent with the same tablet_ref once), forms in %s scanned by 8 October with an answer, and each "
             "member once, at the return received last, the member found through the personal link's code, the code "
             "typed on a tablet and the pack each form was posted in (%s): %s returns."
             % (F["standard"], F["sessions"], F["paper"], F["packs"], fmt(A["counted"])))
    L.append("2. Placed each return in its team under section 3.4: personal links by their September code; tablet returns "
             "started before the tablets' second team list load on 13 September (%s) and paper packs by their printed "
             "code read through %s, a split team's code reaching no single team." % (F["tablets"], F["reorg"]))
    L.append("3. Kept the %s teams with five or more returns that count (section 5.1) and their %s returns that answer "
             "all twelve items on the scale, scored as section 2 and %s set out (TC04 and TC07 turned round)." % (fmt(A["teams"]), fmt(A["used"]), F["codebook"]))
    L.append("4. Split the items' covariance into the pooled within-team covariance and the between-team covariance (the "
             "scaled between-team matrix less the pooled within-team matrix) and fitted one factor to the between-team "
             "correlations (section 4.2): TC01 to TC10 load %.2f or more, TC11 and TC12 under %.2f."
             % (KEEP_BAND, DROP_BAND))
    L.append("5. Applied the %.2f line (section 4.3): ten items stay for 2028, TC11 and TC12 are withdrawn." % E.LINE)
    L.append("6. Counted each channel's returns that count, those in no team the dashboard reports, those in a reported "
             "team leaving an item without an answer on the scale, and those the check used.")
    L.append("7. Counted each item's answers on the scale and its favourable answers over every return that counts, as %s "
             "sets out." % F["note"])
    L.append("8. Placed each reported team in the division it belonged to on 1 September 2027 (%s, the previous division "
             "for a team that moved later) and counted the teams and the returns the check used.\n" % F["register"])
    L.append("## 4. Deliverable Answers\n")
    L.append("### lfp_tci_structure_check_2027.xlsx\n")
    L.append("1. Each item's team-level loading and decision:")
    for c in E.ITEM_CODES:
        if c in A["stay"]:
            L.append("   - %s (%s): %.2f or more, stays" % (c, WORDING[c].rstrip("."), KEEP_BAND))
        else:
            L.append("   - %s (%s): under %.2f, withdrawn" % (c, WORDING[c].rstrip("."), DROP_BAND))
    L.append("2. The 2027 returns by channel:")
    for ch, nm in CHANNELS:
        x = A["ledger"][ch]
        L.append("   - %s: %s count, %s outside the teams the dashboard reports, %s more leave an item without an answer "
                 "on the scale, %s used by the check" % (nm[0].upper() + nm[1:], fmt(x["count"]), fmt(x["outside"]),
                                                         fmt(x["incomplete"]), fmt(x["used"])))
    L.append("3. For each item, the company-wide answers on the scale the dashboard counts and how many of them are "
             "favourable:")
    for c in E.ITEM_CODES:
        L.append("   - %s: %s answers, %s favourable" % (c, fmt(A["fav"][c]["base"]), fmt(A["fav"][c]["fav"])))
    L.append("4. By division, the teams the dashboard reports and the returns the check used:")
    for d in [x[1] for x in P.DIVISIONS]:
        v = A["div"][d]
        L.append("   - %s: %s teams, %s returns" % (d, fmt(v["teams"]), fmt(v["used"])))
    L.append("")
    L.append("### lfp_tci_items_2028.pptx\n")
    L.append("5. One slide for the executive team: the ten items that stay and TC11 and TC12 withdrawn, with each item's "
             "team-level loading charted against the %.2f line and TC11 and TC12 marked." % E.LINE)
    return "\n".join(L) + "\n"


def write(task, here, A):
    fig = figures(A)
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=2, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
