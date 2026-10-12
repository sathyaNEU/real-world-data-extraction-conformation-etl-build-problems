"""Every graded figure and every rung, from the generator's own state: the 2027 design days run through the planning
standard on the lanes that will be open with the unit posted (the host's own lanes less what its duty managers stood
down last summer, by interval, plus the unit's three), the ladder's wrong runs, the flip, last summer's realised
effect, and the three measures for every airport. Writes generator/figures.json for figures_check.py."""
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


def release_seen(world):
    """The host's own lanes open on its posted days against the summer roster plan, by interval, over 05:00 to 21:00:
    the lanes stood down (the same on every posted day)."""
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


def compute(world=None):
    import sim as S
    world = world or S.simulate_all()
    design, plans, phase = PR.design27()
    sc = {h: M.scenario(design, plans, h) for h in ("gross", "average", "interval", "average18", "shift", "allday",
                                                     "uniform2")}
    tot = {h: M.totals(s) for h, s in sc.items()}
    rank = {h: M.ranking(s) for h, s in sc.items()}
    gold = sc["interval"]
    pick = rank["interval"][0]
    runner = rank["interval"][1]
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
            "release_seen": release_seen(world), "no_team": no_team}


def figures(F):
    """The figures submission.md states, as it states them."""
    g, t = F["gold"], F["tot"]["interval"]
    pick, runner = F["pick"], F["runner"]
    out = {
        "call": W.NAME[pick],
        "pick_total": rnd100(t[pick]),
        "runner_up": W.NAME[runner],
        "runner_total": rnd100(t[runner]),
        "gross_leader": W.NAME[F["rank"]["gross"][0]],
        "average_leader": W.NAME[F["rank"]["average"][0]],
        "flip_pct": F["flip"],
        "lanes_stood_down_all_day": int(W.RELEASE["CUL"][0]),
        "unit_lanes": W.TEAM_LANES,
        "unit_lanes_added_at_banks": {W.NAME[c]: W.TEAM_LANES - int(W.RELEASE[c][0]) for c in W.CODES},
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
