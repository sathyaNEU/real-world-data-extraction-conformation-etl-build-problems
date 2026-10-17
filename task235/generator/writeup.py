"""Answers, figures.json and submission.md for task235, drafted from the analysis so no figure is typed."""
import json
import os

import estim as E
import params as P

NAME = {"ios": "iOS", "android": "Android"}
FILES = dict(val="purchase_service_validations_2026-10-05_to_2026-11-09.csv",
             evt="warehouse_purchase_completed_2026-10-05_to_2026-11-09.csv",
             ses="session_service_starts_2026-10-05_to_2026-11-09.csv",
             links="account_service_links_2026-10-05_to_2026-11-09.csv",
             rates="ecb_euro_reference_rates_2026-09-28_to_2026-11-06.csv", reg="build_register.xlsx",
             sdk="tern_sdk_release_notes.md")


def lab(b):
    return "%s %s" % (NAME[b[0]], b[1])


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _versions(builds):
    """builds named the way a release note does: iOS 7.38.2, 7.39.1 and 7.40.0"""
    out = []
    for plat in ("android", "ios"):
        vs = [b[1] for b in E.ORDER if b in builds and b[0] == plat]
        if vs:
            out.append("%s %s" % (NAME[plat], _and(vs)))
    return _and(out)


def answers(X):
    num = {b[1]: b[2] for b in P.BUILDS if b[0] == "ios"}, {b[1]: b[2] for b in P.BUILDS if b[0] == "android"}
    bn = lambda b: (num[0] if b[0] == "ios" else num[1])[b[1]]
    C, G = X["counts"], X["gold"]
    builds = []
    for b in E.ORDER:
        c = C[b]
        builds.append(dict(platform=b[0], version=b[1], build_number=bn(b), label=lab(b), n=c["n"], due=c["due"],
                           lost=c["lost"], held=c["held"], pending=c["pending"], q=E.resolved_share(c),
                           loss_pct=round(100 * G[b], 2), loss_pct_raw=100 * G[b], alert=b in X["esc"],
                           lo_pct=round(100 * X["lo"][b], 2), hi_pct=round(100 * X["hi"][b], 2),
                           lost_pct=round(100 * c["lost"] / c["n"], 2),
                           flip=E.flip_share(c), players=int(X["players"]["golden"][b]),
                           eur=float(X["bookings"]["golden"][b]), per_player=float(X["per_player"]["golden"][b])))
    rest = [r for r in builds if not r["alert"]]
    top_lost = max(rest, key=lambda r: r["lost"] / r["n"])
    R = X["routes"]
    gold = X["esc"]
    al = lambda name: E.alerted(R[name])
    s7 = al("settle7")
    tot = {k: sum(c[k] for c in C.values()) for k in ("n", "due", "lost", "held", "pending")}
    tot["missing"] = tot["lost"] + tot["pending"]
    tot["matched"] = tot["n"] - tot["missing"]
    old = [r for r in rest if r["pending"] and (r["platform"], r["version"]) in s7]
    new_a = [r for r in rest if (r["platform"], r["version"]) == ("android", "7.42.0")][0]
    return dict(builds=builds, by={(r["platform"], r["version"]): r for r in builds}, esc=gold, top_lost=top_lost,
                tot=tot, s7=s7, s7_false=sorted(s7 - gold, key=E.ORDER.index), s11=al("settle11"), curve=al("curve"),
                account=al("account"), account_false=sorted(al("account") - gold, key=E.ORDER.index),
                upper=al("upper"), short=X["short"], matched_age=X["matched_age"], old=old, new_a=new_a,
                old_flip=min(r["flip"] for r in old), old_q=max(r["q"] for r in old),
                players=X["players"], bookings=X["bookings"], routes=R, corridor=X["corridor"])


def figures(A):
    a41, i42, tl, na = A["by"][("android", "7.41.0")], A["by"][("ios", "7.42.0")], A["top_lost"], A["new_a"]
    pmin = min(A["builds"], key=lambda r: r["players"]); pmax = max(A["builds"], key=lambda r: r["players"])
    emin = min(A["builds"], key=lambda r: r["per_player"]); emax = max(A["builds"], key=lambda r: r["per_player"])
    fig = {
        "call": [lab(b) for b in E.ORDER if b in A["esc"]],
        "components": {
            "Android 7.41.0": {"lost": a41["lost"], "purchases": a41["n"], "open": a41["pending"],
                               "tracking_loss_pct": "%.2f" % a41["loss_pct"]},
            "iOS 7.42.0": {"lost": i42["lost"], "open": i42["pending"], "purchases": i42["n"],
                           "if_every_open_event_arrives": "%.2f" % i42["lo_pct"],
                           "if_no_open_event_arrives": "%.2f" % i42["hi_pct"]},
            "highest_other_lost": {"build": tl["label"], "lost": tl["lost"], "purchases": tl["n"], "open": tl["pending"],
                                   "lost_pct": "%.2f" % tl["lost_pct"]},
        },
        "rivals": {"old_builds_open_share_to_cross_pct": int(100 * A["old_flip"]),
                   "old_builds_resolved_share_lost_pct_at_most": int(round(100 * A["old_q"] + 0.5)),
                   "android_7_42_0": {"open": na["pending"], "resolved": na["lost"] + na["held"], "resolved_lost": na["lost"]}},
        "steps": {"purchases": A["tot"]["n"], "matched": A["tot"]["matched"], "missing_at_run": A["tot"]["missing"],
                  "phone_opened_since": A["tot"]["due"], "lost": A["tot"]["lost"], "open": A["tot"]["pending"],
                  "players_range": {pmin["label"]: pmin["players"], pmax["label"]: pmax["players"]},
                  "per_player_range": {emin["label"]: "%.2f" % emin["per_player"], emax["label"]: "%.2f" % emax["per_player"]}},
        "builds": {r["label"]: {"build_number": r["build_number"], "alert": r["alert"], "paying_players": r["players"],
                                "gross_bookings_per_paying_player_eur": "%.2f" % r["per_player"],
                                "chart_tracking_loss_pct": "%.2f" % r["loss_pct"]}
                   for r in A["builds"]},
        "line_per_cent": 2,
        "default_path": {"alerted": [lab(b) for b in E.ORDER if b in A["s7"]], "window_days": 7},
        "versions": sorted({b[1] for b in E.ORDER}),
        "run": "Monday 9 November 2026", "sdk_versions": ["4.6.0", "5.0.1"],
    }
    return fig


def submission(A):
    by = A["by"]
    a41, i42, tl, na = by[("android", "7.41.0")], by[("ios", "7.42.0")], A["top_lost"], A["new_a"]
    t = A["tot"]
    s7f, accf = A["s7_false"], A["account_false"]
    assert A["s11"] == {("android", "7.41.0")} and ("ios", "7.42.0") not in A["s7"] | A["curve"]
    assert all(v[("android", "7.42.0")][0] > E.LINE for w, v in A["short"].items() if w <= 2.5)
    ma = A["matched_age"]
    assert ma[("android", "7.42.0")][0] > ma[("android", "7.42.0")][1] and ma[("ios", "7.42.0")][0] < ma[("ios", "7.42.0")][1]
    assert na["lost"] == 0 and na["flip"] > 0.2 and A["old_flip"] >= 0.33 and A["old_q"] <= 0.02
    assert all(E.alerted(v) == A["esc"] for v in A["corridor"].values())
    pmin = min(A["builds"], key=lambda r: r["players"]); pmax = max(A["builds"], key=lambda r: r["players"])
    emin = min(A["builds"], key=lambda r: r["per_player"]); emax = max(A["builds"], key=lambda r: r["per_player"])
    out = ["# task235 submission\n", "## Tags\n",
           "**Domain:** Product Analytics (metric definition and measurement science: a mobile game's purchase tracking, "
           "the analytics SDK's client events reconciled against the store-verified purchases build by build).",
           "**Analytical objective:** Data Quality Monitoring & Alerting (which production builds of Kittiwake Cove get a "
           "purchase-tracking alert in the KC-DQ-04 run of Monday 9 November 2026).\n",
           "## 1. Final Recommendation\n",
           "**Alert Android 7.41.0 and iOS 7.42.0 in the run of Monday 9 November, and no other build.**\n"]
    out.append("Judged against the next session of the phone that made each purchase, Android 7.41.0 loses %.2f per cent of "
               "its purchase events with none still on a phone, and iOS 7.42.0 at least %.2f per cent even if every event "
               "still on a phone arrives. Not %s, which a seven-day settle window alerts: their missing events sit on phones "
               "that have not opened the game since, and each would cross the line only if %d per cent or more of those "
               "were lost, where of its events still on a phone when the game next opened at most %d per cent never "
               "arrived. Not Android 7.42.0, which short windows and same-age comparisons alert: its new uploads leave "
               "events on the phone until the game next starts, and all %d of its events still on a phone when the game "
               "next opened have arrived. Not the account's next "
               "session, which alerts %s, whose players open the game on another device while the one that bought still "
               "holds the event.\n"
               % (a41["loss_pct"], i42["lo_pct"], _versions(s7f), int(100 * A["old_flip"]), int(round(100 * A["old_q"] + 0.5)),
                  na["lost"] + na["held"], _versions(accf)))
    out.append("## 2. Critical Components\n")
    out.append("1. Android 7.41.0: **%d** of its **%s** purchases have a missing event though their phone has opened the "
               "game since, and none is still open: tracking loss **%.2f** per cent"
               % (a41["lost"], format(a41["n"], ","), a41["loss_pct"]))
    out.append("2. iOS 7.42.0: **%d** such purchases of **%d**, and **%d** whose event is still on a phone that has not "
               "opened the game since: tracking loss at least **%.2f** per cent, **%.2f** if none of those arrives"
               % (i42["lost"], i42["n"], i42["pending"], i42["lo_pct"], i42["hi_pct"]))
    out.append("3. No other build has more than **%.2f** per cent of its purchases missing an event after their phone opened "
               "the game again (%s, %d of %s, none open)\n"
               % (tl["lost_pct"], tl["label"], tl["lost"], format(tl["n"], ",")))
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Took the purchases under KC-DQ-04 section 2 from %s (transaction kind purchase, Production, standard, "
               "the Irish date of purchased_at from 12 October to 8 November) with their builds from %s: %s purchases."
               % (FILES["val"], FILES["reg"], format(t["n"], ",")))
    out.append("2. Matched each to its purchase_completed event in %s by store transaction id, the warehouse's several rows "
               "for one transaction being one event (section 3): %s matched, %d missing at the run."
               % (FILES["evt"], format(t["matched"], ","), t["missing"]))
    out.append("3. Found each purchase's next session start of the same device in %s; as the SDK uploads its queue when the "
               "game starts (%s, 4.6.0), a missing event whose phone has opened the game since will never arrive: %d lost, "
               "%d still on phones that have not opened the game since (section 4)."
               % (FILES["ses"], FILES["sdk"], t["lost"], t["pending"]))
    out.append("4. Android 7.41.0 has none open: %d of %s lost, %.2f per cent, above the 2 per cent line (section 5); iOS "
               "7.42.0 has %d lost and %d open of %d, %.2f per cent even if all %d arrive."
               % (a41["lost"], format(a41["n"], ","), a41["loss_pct"], i42["lost"], i42["pending"], i42["n"], i42["lo_pct"],
                  i42["pending"]))
    out.append("5. Every other build has at most %.2f per cent lost (%s) and crosses the line only if far more of its "
               "open purchases were lost than of its events still on a phone when the game next opened (at most %d per "
               "cent of those never arrived on the old builds, none on Android 7.42.0): no alert."
               % (tl["lost_pct"], tl["label"], int(round(100 * A["old_q"] + 0.5))))
    out.append("6. Charted each build's tracking loss against the 2 per cent line, its open purchases counted lost at the "
               "share of its events still on a phone when the game next opened that never arrived.")
    out.append("7. Counted paying players (section 6) with accounts joined through %s and each guest account joined to the "
               "account its phone shows next in %s, the links file being no full register of a player's accounts: from %d "
               "(%s) to %s (%s)." % (FILES["links"], FILES["ses"], pmin["players"], pmin["label"],
                                     format(pmax["players"], ","), pmax["label"]))
    out.append("8. Converted each purchase's price_minor at its currency's minor unit (none for JPY and KRW) at the ECB rate "
               "in force on its Irish date in %s, rounded to the cent line by line, and divided each build's total by its "
               "paying players (section 6): from %.2f euro (%s) to %.2f (%s) per paying player.\n"
               % (FILES["rates"], emin["per_player"], emin["label"], emax["per_player"], emax["label"]))
    out.append("## 4. Deliverable Answers\n")
    out.append("### tracking_loss_alerts_2026-11-09.csv\n")
    out.append("1. One row per build in the file's order, gross bookings per paying player in euro to the cent:")
    for r in A["builds"]:
        out.append("   - %s, build %s: %s, %s paying players, gross bookings per paying player %.2f"
                   % (r["label"], r["build_number"], "alert" if r["alert"] else "no alert", format(r["players"], ","),
                      r["per_player"]))
    out.append("\n### tracking_loss_by_build_2026-11-09.png\n")
    out.append("2. Horizontal bar chart of the twelve builds' tracking loss against the 2 per cent alert line, grouped by "
               "platform: Android 7.41.0 and iOS 7.42.0 in red above the line, every other bar below it.")
    return "\n".join(out) + "\n"


def write(task_dir, gen_dir, A):
    fig = figures(A)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
