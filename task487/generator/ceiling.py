"""The ask layer measured on the cut pack: Schedule B's 24 figures (each route's fugitive methane in January to June and
in July to December, from the batteries the route ran in that half) under the golden's handling and under the
handlings a response is likely to take, scored figure by figure against the golden (a hit is the figure at one
decimal), and the pair ceiling those keeps imply.

    python3 task487/generator/ceiling.py

The cracker lands the call, executes every filed rule and the hygiene battery, and works Schedule B the way both round 3
readers did: each half's runs from the two apps, each repair from the last work order naming its tag, every session in
the survey log as a survey and each work order's Completed day as its repair. The mirror stops at the same rung and also
counts every tag as a leak of its own."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G      # noqa: E402
import pack_read as PR  # noqa: E402

ROUTES = ["R%02d" % i for i in range(1, 13)]
HANDLINGS = {
    "cracker": dict(fg_sessions="all", fg_repair="completed"),
    "mirror": dict(fg_sessions="all", fg_repair="completed", fg_chain="none"),
    "naive": dict(fg_sessions="all", fg_repair="tracker", fg_route="register"),
    "sessions_right_completed_days": dict(fg_repair="completed"),
    "tickets_right_every_session": dict(fg_sessions="all"),
    "tagged_sessions_only": dict(fg_sessions="tagged"),
    "reference_dates_everywhere": dict(fg_repair="refdate"),
    "tracker_closure_only": dict(fg_repair="tracker"),
    "register_runs_only": dict(fg_route="register"),
    "route_app_runs_both_halves": dict(fg_route="routeapp"),
    "checkin_runs_both_halves": dict(fg_route="checkin"),
    "register_runs_second_half": dict(fg_route="registerH2"),
    "tags_as_leaks_only": dict(fg_chain="none"),
    "received_as_survey_day": dict(fg_survey="tag"),
    "one_leak_a_component": dict(fg_chain="component"),
    "one_leak_a_work_order": dict(fg_chain="workorder"),
    "earlier_open_tag_dropped": dict(fg_chain="dropold"),
    "latest_rate": dict(fg_rate="latest"),
    "previous_tag_not_survey": dict(fg_prev="tracker"),
    "not_clipped_to_2026": dict(fg_clip=False),
    "old_code_not_carried": dict(rename=False),
}


def figures(sched):
    f = {}
    for r in ROUTES:
        for h in ("h1", "h2"):
            f["%s.%s_t" % (r, h)] = round(sched[r][h], 1)
    return f


def measure(p=None):
    p = p or PR.read()
    gold = figures(G.compute(p)["sched"])
    keeps = {}
    for name, kw in HANDLINGS.items():
        f = figures(G.compute(p, **kw)["sched"])
        hit = [k for k in gold if f[k] == gold[k]]
        keeps[name] = (len(hit), {a: sum(1 for k in hit if k.endswith(a)) for a in ("h1_t", "h2_t")}, hit)
    return gold, keeps


def pair(keep_c, keep_m, total, call=45.0, miss=12.0):
    """the pair ceiling: the cracker on the call, the mirror off it, each keeping its share of 55 ask points"""
    return ((call + 55.0 * keep_c / total) + (miss + 55.0 * keep_m / total)) / 2


if __name__ == "__main__":
    gold, keeps = measure()
    n = len(gold)
    print("graded ask figures:", n)
    for k, (v, by, hit) in keeps.items():
        print("  %-34s keeps %2d of %d  %s" % (k, v, n, {a: x for a, x in by.items() if x}))
    kc, km = keeps["cracker"][0], keeps["mirror"][0]
    print("cracker keeps %.1f per cent of ask weight, mirror %.1f per cent; pair ceiling %.1f" % (
        100.0 * kc / n, 100.0 * km / n, pair(kc, km, n)))
    worst = max(v for k, (v, by, hit) in keeps.items())
    print("the best non-golden handling keeps %d of %d (%.1f per cent)" % (worst, n, 100.0 * worst / n))
