"""The goldens: the assignment paper (performance_squad_q1_2027.md) and its chart (lcp_reach_q1_2027.png), drawn
from figures computed on the pack as shipped."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

import analysis as AN   # noqa: E402
import common as K      # noqa: E402

NAMES = AN.NAMES


def compute(target):
    nov = AN.page_loads(target)
    e = AN.engagement_frame(target)
    eff = AN.effect(e)
    R = AN.rungs(nov, eff)
    eg = AN.egress(target)
    imgs = AN.hero_images(target)
    moved = {n: AN.round_to(R.loc[n, "golden"], 1e5) for n in NAMES}
    order = sorted(NAMES, key=lambda n: -R.loc[n, "golden"])
    call, second = order[0], order[1]
    m = lambda x: round(x / 1e6, 1)
    by_after = {k: v["after"]["load_delay_ms"] for k, v in eff["by"].items()}
    by_before = {k: v["before"]["load_delay_ms"] for k, v in eff["by"].items()}
    fig = {
        "call_property": call,
        "call_loads_moved_m": m(moved[call]),
        "runner_up": second,
        "runner_up_loads_moved_m": m(moved[second]),
        "level_ms": int(round(eff["level"])),
        "load_time_ratio": round(eff["r_load"], 2),
        "engagements": len(eff["by"]),
        "loads_moved_m": {n: m(moved[n]) for n in NAMES},
        "egress_gb": {n: AN.round_to(eg[n]["gb"], 1) for n in NAMES},
        "egress_aud": {n: AN.round_to(eg[n]["aud"], 1) for n in NAMES},
        "hero_images": {n: imgs[n] for n in NAMES},
        "rung_slow_all": [AN.winner(R.slow_all)[0], m(R.slow_all.max())],
        "rung_own_slow": [AN.winner(R.R1_reach)[0], m(R.R1_reach.max())],
        "rung_ratios_parts": [AN.winner(R.R2_parts)[0], m(R.R2_parts.max())],
        "rung_ratio_whole": [AN.winner(R.R2_whole)[0], m(R.R2_whole.max())],
        "rung_zero_delay": [AN.winner(R.R3_zero)[0], m(R.R3_zero.max())],
        "rung_level_held": [AN.winner(R.R4_held)[0], m(R.R4_held.max())],
        "gated_engagements": list(K.GATED_ENGAGEMENTS),
        "gated_render_before_ms": [int(round(eff["by"][k]["before"]["render_delay_ms"])) for k in K.GATED_ENGAGEMENTS],
        "gated_render_after_ms": [int(round(eff["by"][k]["after"]["render_delay_ms"])) for k in K.GATED_ENGAGEMENTS],
        "engagement_after_delay_min_ms": int(round(min(by_after.values()))),
        "engagement_after_delay_max_ms": int(round(max(by_after.values()))),
        "engagement_before_delay_min_ms": int(round(min(by_before.values()))),
        "engagement_before_delay_max_ms": int(round(max(by_before.values()))),
        "call_margin_x": round(R.loc[call, "golden"] / R.loc[second, "golden"], 2),
        "good_ms": K.GOOD_MS,
        "cdn_rate_aud_per_gb": K.CDN_RATE_AUD_PER_GB,
        "gb_bytes": 1_000_000_000,
    }
    return dict(figures=fig, rungs=R, effect=eff, egress=eg, images=imgs, order=order, nov=nov)


def _m(x):
    return "%.1f million" % x


def write_note(path, res):
    f = res["figures"]
    order = res["order"]
    call = f["call_property"]
    L = []
    L.append("# Performance squad, quarter from 5 January 2027: %s" % call)
    L.append("")
    L.append("To: %s, Head of Web Platform  " % K.PEOPLE["head"])
    L.append("From: %s, performance squad lead  " % K.PEOPLE["lead"])
    L.append("For the December planning, 8 December 2026")
    L.append("")
    L.append("**Send the squad to %s.** The hero-image playbook would move %s of %s's page loads a month into the "
             "good LCP band (2,500 ms or less), the most of our six properties; %s is next at %s."
             % (call, _m(f["call_loads_moved_m"]), call, f["runner_up"], _m(f["runner_up_loads_moved_m"])))
    L.append("")
    L.append("## What the playbook would do at each property")
    L.append("")
    L.append("| Property | Page loads moved into the good band, a month | Hero-image egress on the image CDN, GB a "
             "month | At the contract rate, AUD a month | Live hero images to convert to AVIF |")
    L.append("|---|---:|---:|---:|---:|")
    for n in order:
        L.append("| %s%s | %s | %s | %s | %s |" % (n, " (squad)" if n == call else "", _m(f["loads_moved_m"][n]),
                                                  "{:,}".format(f["egress_gb"][n]), "${:,}".format(f["egress_aud"][n]),
                                                  "{:,}".format(f["hero_images"][n])))
    L.append("")
    L.append("Page loads are November 2026's in Sydney time on our RUM, each beacon standing for 1 / the sampling "
             "rate in force when its page load started. Egress is costed on November's hero-image requests; the "
             "hero images are those live on the 2 December crawl. The chart is lcp_reach_q1_2027.png.")
    L.append("")
    L.append("## How the counts were built")
    L.append("")
    L.append("The playbook can only move a page load slower than 2,500 ms whose LCP element is the property's own "
             "hero image (charter 2.4). Each of those loads was rebuilt part by part the way the squad's %d past "
             "engagements landed. Time to first byte stays as it is. The image's load time falls to %.2f of what it "
             "was (AVIF at the slot size). The image's load delay goes to %d ms, whatever it was before: on every "
             "engagement the after-window median sat between %d and %d ms, from before-window medians of a little "
             "over 100 ms to nearly 3,000 ms, because a preloaded hero waits only on the connection to the image CDN."
             % (f["engagements"], f["load_time_ratio"], f["level_ms"], f["engagement_after_delay_min_ms"],
                f["engagement_after_delay_max_ms"]))
    L.append("")
    site = {e[0]: e[1] for e in K.ENGAGEMENTS}
    g0, g1 = f["gated_engagements"]
    L.append("The rebuilt paint then comes no sooner than the page's own first contentful paint, which the playbook "
             "leaves where it is: the squad does no work on scripts, fonts or the render path (charter 3.2). At %s "
             "(%s) and %s (%s) the render delay's median went from %s and %s ms to %s and %s ms once the hero arrived "
             "early, and the paint landed on the page's first paint, about three seconds after its first byte. On "
             "the other %s engagements the pages first painted soon after their first byte and the render delay held."
             % (site[g0], g0, site[g1], g1, "{:,}".format(f["gated_render_before_ms"][0]),
                "{:,}".format(f["gated_render_before_ms"][1]), "{:,}".format(f["gated_render_after_ms"][0]),
                "{:,}".format(f["gated_render_after_ms"][1]),
                {9: "nine"}.get(f["engagements"] - len(f["gated_engagements"]),
                                str(f["engagements"] - len(f["gated_engagements"])))))
    L.append("")
    L.append("That floor decides the quarter. With the render delay held as it is today, Pantry comes first (%s), "
             "because its hero images wait longest of all to start loading. But most of Pantry's slow loads are on "
             "its recipes, dinner, quick-meals and healthy pages, which first paint about three seconds after their "
             "first byte, and no faster image brings those under the line: Pantry moves %s. Most of %s's pages "
             "first paint soon after their first byte, so most of its gain stands."
             % (_m(f["rung_level_held"][1]), _m(f["loads_moved_m"]["Pantry"]), call))
    L.append("")
    L.append("Carried as a ratio of medians, or as a preload that removes the delay, the engagements put Ledger first "
             "(%s and %s), because they shrink Ledger's already short delays further. On the image CDN those delays "
             "rise to the connection time, and Ledger moves %s."
             % (_m(f["rung_ratios_parts"][1]), _m(f["rung_zero_delay"][1]), _m(f["loads_moved_m"]["Ledger"])))
    L.append("")
    L.append("Hearth has the most slow page loads on its own images (%s), but its paint is held by time to first "
             "byte, which is the Hearth team's work, not the squad's."
             % _m(f["rung_own_slow"][1]))
    L.append("")
    L.append("## Notes")
    L.append("")
    L.append("- Egress counts November's hero-slot requests answered with the image (revalidations answered 304 "
             "carry none) on each property's image host and image CDN path, and on the legacy aliases from the old "
             "media server's own log, at the mean AVIF size of the property's hero slot and AUD %.3f per GB."
             % K.CDN_RATE_AUD_PER_GB)
    L.append("- Hero images are the DAM's hero assets on the 2 December crawl, counted once each (renditions "
             "together, and a migrated asset's library record together with its DAM record) under the property "
             "whose page carried it: the heroes of the three sections moved in March 2025 are their new "
             "property's own, though the DAM still files them under the collection they were uploaded to.")
    L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def write_chart(path, res):
    f = res["figures"]
    call = f["call_property"]
    order = res["order"][::-1]
    vals = [f["loads_moved_m"][n] for n in order]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    figr, ax = plt.subplots(figsize=(8.4, 4.6), dpi=150)
    colors = ["#0f6b70" if n == call else "#b9c2c9" for n in order]
    bars = ax.barh(order, vals, color=colors, height=0.62)
    for b, v, n in zip(bars, vals, order):
        ax.text(v + 0.08, b.get_y() + b.get_height() / 2, "%.1f million" % v, va="center", fontsize=9.5,
                color="#1d2226", fontweight="bold" if n == call else "normal")
    i = order.index(call)
    ax.text(vals[i] - 0.12, i, "Squad, Q1 2027", ha="right", va="center", fontsize=9.5, color="white",
            fontweight="bold")
    ax.set_xlim(0, max(vals) * 1.22)
    ax.set_xlabel("Page loads a month moved into the good LCP band (millions)")
    ax.set_title("%s gains the most from the hero-image playbook" % call, loc="left", fontsize=12.5,
                 fontweight="bold", color="#1d2226", pad=24)
    ax.text(0, 1.025, "November 2026 page loads, Sydney time; good band: LCP 2,500 ms or less after the playbook",
            transform=ax.transAxes, fontsize=8.6, color="#5b6268")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color="#e3e7ea", lw=0.8)
    ax.set_axisbelow(True)
    figr.text(0.01, 0.01, "Source: group RUM beacons and the squad's engagement reviews, 2024 to 2026", fontsize=7.5,
              color="#5b6268")
    figr.tight_layout(rect=(0, 0.03, 1, 1))
    figr.savefig(path, metadata={"Software": None}, pil_kwargs={"optimize": False})
    plt.close(figr)
