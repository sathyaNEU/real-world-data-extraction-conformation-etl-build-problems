"""Every graded figure and every rung, from the generator's own state: the 2027 design days run through the planning
standard on the lanes each checkpoint actually opens, without the unit and with it, the ladder's wrong runs, the flip,
last summer's realised effect, and the three measures for every airport. Writes generator/figures.json for
figures_check.py."""
import collections
import json

import numpy as np

import asks as A
import models as M
import profiles as PR
import records as R
import world as W


def rnd100(x):
    return int(round(x / 100.0)) * 100


def realised_2026(world, posts):
    """Last summer's effect per posted week, as the shipped sensor and lane files measure it: passengers screened in
    intervals whose queue time ran over 20 minutes, the airport's other days in the same months against its posted
    days, over seven days."""
    waits = {(c, d, i): v for (c, d, i, v) in world["waits"]}
    out = {}
    for c in W.CODES:
        staff = set(R.S.staff_ids(c))
        over = collections.defaultdict(int)
        for (_, lane, d, i, n) in world["airports"][c]["lanes"]:
            if lane in staff:
                continue
            if waits.get((c, d, i), 0.0) > W.STANDARD_MIN:
                over[d] += n
        posted = [d for d in world["days"] if W.host_on(d) == c]
        months = {d.month for d in posted}
        other = [d for d in world["days"] if W.host_on(d) != c and d.month in months]
        out[c] = 7 * (np.mean([over[d] for d in other]) - np.mean([over[d] for d in posted]))
    return out


def gap_seen(world):
    """What a posted day shows against the summer roster pattern, by interval: the host's own lanes open on its posted
    days subtracted from the pattern. It holds the lanes the pattern never opens and the lanes the duty managers stand
    down, together, and the pattern cannot tell them apart."""
    out = {}
    for c in W.CODES:
        plan = PR.plan(c)
        diffs = []
        for x in world["airports"][c]["daily"]:
            if not x["posted"]:
                continue
            opened = np.array(x["open"], float) - M.team()
            diffs.append(plan - opened)
        diffs = np.array(diffs)
        out[c] = {"min": diffs.min(axis=0), "max": diffs.max(axis=0)}
    return out


def shortfall_seen(world):
    """What the checkpoint's own days show against the pattern: on a day with no unit and no lane fault the lanes open
    are the pattern less the lanes it never opens, so the most any ordinary day opens in an interval is that figure."""
    out = {}
    for c in W.CODES:
        plan = PR.plan(c)
        opened = np.array([x["open"] for x in world["airports"][c]["daily"] if not x["posted"]], float)
        out[c] = plan - opened.max(axis=0)
    return out


def compute(world=None):
    import sim as S
    world = world or S.simulate_all()
    design, plans, phase = PR.design27()
    sc = {h: M.scenario(design, plans, h) for h in ("gross", "average", "interval", "actual", "double", "standonly",
                                                    "shift", "average18", "uniform")}
    tot = {h: M.totals(s) for h, s in sc.items()}
    rank = {h: M.ranking(s) for h, s in sc.items()}
    gold = sc["actual"]
    pick = rank["actual"][0]
    runner = rank["actual"][1]
    flips = {m: M.flip(design, plans, pick, m) for m in ("none", "round", "floor")}
    posts = R.postings()
    lines, stays = R.invoices(posts)
    export = R.export_claims(R.claims(posts))
    asks = {
        "passengers": A.passengers_2026(world),
        "hotel": A.hotel_per_night(lines, posts),
        "claims": A.claims_per_week(export, posts),
    }
    stops = {
        "passengers": {h: A.passengers_2026(world, h) for h in ("every lane", "no unit")},
        "hotel": {h: A.hotel_per_night(lines, posts, h) for h in ("every line", "no credit")},
        "claims": {h: A.claims_per_week(export, posts, h) for h in ("every row by date", "dedup by date",
                                                                   "dedup on officer")},
    }
    real = realised_2026(world, posts)
    no_team = {c: {n: M.queue(design[c][n], plans[c][n])[0] for n, _, _ in W.PERIODS} for c in W.CODES}
    return {"world": world, "design": design, "plans": plans, "phase": phase, "sc": sc, "tot": tot, "rank": rank,
            "gold": gold, "pick": pick, "runner": runner, "flip": flips["none"], "flips": flips, "posts": posts,
            "lines": lines, "stays": stays, "export": export, "asks": asks, "stops": stops, "realised": real,
            "gap_seen": gap_seen(world), "shortfall_seen": shortfall_seen(world), "no_team": no_team}


def figures(F):
    """The figures submission.md states, as it states them."""
    g, t = F["gold"], F["tot"]["actual"]
    pick, runner = F["pick"], F["runner"]
    out = {
        "call": W.NAME[pick],
        "pick_total": rnd100(t[pick]),
        "runner_up": W.NAME[runner],
        "runner_total": rnd100(t[runner]),
        "gross_leader": W.NAME[F["rank"]["gross"][0]],
        "interval_leader": W.NAME[F["rank"]["interval"][0]],
        "interval_leader_total": rnd100(F["tot"]["interval"][F["rank"]["interval"][0]]),
        "flip_pct": F["flip"],
        "unit_lanes": W.TEAM_LANES,
        "bank_lanes_unopened": {W.NAME[c]: int(W.SHORT[c][0]) for c in W.CODES},
        "bank_lanes_stood_down_morning": {W.NAME[c]: int(W.RELEASE[c][0]) for c in W.CODES},
        "bank_lanes_stood_down_evening": {W.NAME[c]: int(W.RELEASE[c][1]) for c in W.CODES},
        "period_days": [W.DAYS[n] for n, _, _ in W.PERIODS],
        "gap_to_runner": rnd100(t[pick] - t[runner]),
        "moved": {W.NAME[c]: {n: rnd100(g[c][n]) for n, _, _ in W.PERIODS} for c in W.CODES},
        "moved_total": {W.NAME[c]: rnd100(t[c]) for c in W.CODES},
        "passengers_2026": {W.NAME[c]: rnd100(F["asks"]["passengers"][c]) for c in W.CODES},
        "hotel_per_night": {W.NAME[c]: round(F["asks"]["hotel"][c], 2) for c in W.CODES},
        "claims_per_week": {W.NAME[c]: round(F["asks"]["claims"][c], 2) for c in W.CODES},
    }
    return out


def write_figures(F, path):
    with open(path, "w") as fh:
        json.dump(figures(F), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
