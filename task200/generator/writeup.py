"""The answers the task owes, figures.json, and submission.md, all from solve.py's output (no typed figure)."""
import json
import os

TEAMS = ["Arden", "Brook", "Cleve", "Dene", "Esk", "Fell"]


def pct(x):
    return int(round(100 * x))


def answers(S):
    M = S["main"]
    t = M["t"]
    first = {k: {"n": int(M["first"].loc[k, "size"]), "hits": int(M["first"].loc[k, "sum"]),
                 "rate": float(M["first"].loc[k, "mean"])} for k in TEAMS}
    allr = {}
    for k in TEAMS:
        g = t[t.team == k]
        allr[k] = {"n": int(len(g)), "hits": int(g.hit.sum()), "rate": float(g.hit.mean())}
    met = {k: float(M["met"].loc[k, "mean"]) for k in TEAMS}
    met_n = {k: int(M["met"].loc[k, "size"]) for k in TEAMS}
    rep = {k: 1.0 - float(M["share_first"][k]) for k in TEAMS}
    hours = {k: round(float(S["A"]["golden"][k]) + 1e-9, 1) for k in TEAMS}
    return dict(order=list(M["golden_order"]), raw_order=list(M["raw_order"]), first=first, all=allr, met_rate=met,
                met_n=met_n,
                repeat_share=rep, hours=hours, hours_exact={k: float(S["A"]["golden"][k]) for k in TEAMS},
                clear={k: int(S["B"]["golden"][k]) for k in TEAMS}, certs={k: int(S["C"]["golden"][k]) for k in TEAMS},
                dprime_first=[x for x in S["rungs"]["R1 dprime"].sort_values(kind="mergesort").index][0])


WORDS = {5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}


def central_share(A):
    """the share of the Central teams' 2026 projections that showed an image already met, pooled"""
    cen = [k for k in TEAMS if k != A["order"][0]]
    return sum(A["met_n"][k] for k in cen) / float(sum(A["all"][k]["n"] for k in cen))


def one_in(A):
    return WORDS[int(round(1.0 / central_share(A)))]


def _fmt_h(v):
    return "{:,.1f}".format(v)


def _fmt_i(v):
    return "{:,}".format(v)


def write(task_dir, gen_dir, A):
    o = A["order"]
    f, al = A["first"], A["all"]
    figs = {
        "order": o,
        "first_rate_pct": {k: pct(f[k]["rate"]) for k in TEAMS},
        "first_n": {k: f[k]["n"] for k in TEAMS},
        "first_hits": {k: f[k]["hits"] for k in TEAMS},
        "all_rate_pct": {k: pct(al[k]["rate"]) for k in TEAMS},
        "met_n": A["met_n"], "all_n": {k: al[k]["n"] for k in TEAMS},
        "met_rate_pct": {k: pct(A["met_rate"][k]) for k in TEAMS},
        "hours": A["hours"], "clear": A["clear"], "certs": A["certs"],
        "cutoff": "1 July 2027", "sps_clause": "4.2",
    }
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(figs, fh, indent=1, sort_keys=True)
        fh.write("\n")
    a, b = o[0], o[1]
    L = []
    L += ["## Tags", "",
          "**Domain:** Human Factors & Ergonomics (safety incident and error analysis).",
          "**Analytical objective:** Anomaly Detection & Diagnostics.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Run the 2027 remedial image interpretation course in the order %s, %s, %s, %s, %s, %s, with %s first.**" % (
              tuple(o) + (a,)),
          "On the threat images its operators met for the first time in 2026 %s found %d per cent (%s of %s), against "
          "%d per cent for %s, the next lowest. Not %s first on the overall projection score (%d per cent against %s's "
          "%d), because most of %s's Pier B projections were images its operators had already met. Not %s first on "
          "d-prime against its clear searches, which measures how well a team separates threats from clutter, not "
          "how often it finds one." % (
              a, pct(f[a]["rate"]), _fmt_i(f[a]["hits"]), _fmt_i(f[a]["n"]), pct(f[b]["rate"]), b, b,
              pct(al[b]["rate"]), a, pct(al[a]["rate"]), a, A["dprime_first"]), ""]
    L += ["## 2. Critical Components", "",
          "1. %s's operators found **%d%%** of the threat images they met for the first time in 2026 (%s of %s), the "
          "lowest of the teams." % (a, pct(f[a]["rate"]), _fmt_i(f[a]["hits"]), _fmt_i(f[a]["n"])),
          "2. **%s of %s's %s** projections in 2026 showed an image its operators had already met, against about "
          "one in %s for the Central teams, and on those images %s found **%d%%**." % (
              _fmt_i(A["met_n"][a]), a, _fmt_i(al[a]["n"]), one_in(A), a, pct(A["met_rate"][a])),
          "3. On first meetings %s is next at **%d%%**, then %s %d%%, %s %d%%, %s %d%% and %s %d%%." % (
              b, pct(f[b]["rate"]), o[2], pct(f[o[2]]["rate"]), o[3], pct(f[o[3]]["rate"]), o[4],
              pct(f[o[4]]["rate"]), o[5], pct(f[o[5]]["rate"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Read ct_tip_events_2024.csv to ct_tip_events_2026.csv (each first-of-month repeat row dropped) and "
          "pierb_tip_log_2023-09_2026-12.csv, mapped every CT login and Pier B TIP operator to its staff number and team "
          "through screening_roster_2026-12-31.xlsx, and left out cancelled projections (SPS-04 section 3).",
          "2. Put each screener's projections in time order from the start of each export and marked one a first meeting where that "
          "screener had not been shown that image before.",
          "3. On 2026 projections each team's share found on first meetings is %s." % ", ".join(
              "%s %d%%" % (k, pct(f[k]["rate"])) for k in o),
          "4. On all 2026 projections %s finds %d%% and %s %d%%, the gap being %s's %s projections of images "
          "already met, found %d%% of the time." % (b, pct(al[b]["rate"]), a, pct(al[a]["rate"]), a,
                                                    _fmt_i(A["met_n"][a]), pct(A["met_rate"][a])),
          "5. Screen time: merged each CT login's overlapping rows in ct_workstation_sessions_2026.csv into one span, "
          "and ended each Pier B log-on in pierb_screen_events_2026.csv at the operator's own log-off, the next log-on "
          "at that screen or the screen's shutdown, whichever came first, each badge read to its holder on the day "
          "through id_centre_badge_register.csv.",
          "6. Clear searches: split search_log_2026.csv records that carry two trays, matched each tray to its latest "
          "reject before the search was taken (ct_tray_rejects_2026.csv, or the Pier B REJECT events) and charged it "
          "to the screener logged on at that screen then.",
          "7. Certificates: took each rostered screener's latest certification, from the passed IIC rows in the LMS "
          "export and from every certificate in assessment_centre_certificates.csv by candidate staff number on its "
          "assessment date (an EXT-IIC row in the LMS carries the date it was keyed, and the centre's list also holds "
          "certificates not yet keyed), and counted three-year expiries before 1 July 2027.",
          "8. Ordered the teams from least to most likely to find a prohibited article (SPS-04 4.2): %s." % ", ".join(o),
          ""]
    L += ["## 4. Deliverable Answers", "", "### remedial_course_2027.xlsx", "",
          "1. Course order:"]
    for i, k in enumerate(o, 1):
        L.append("   - %d. %s" % (i, k))
    L.append("2. Screen time in 2026, hours:")
    for k in TEAMS:
        L.append("   - %s: %s" % (k, _fmt_h(A["hours"][k])))
    L.append("3. Clear searches in 2026:")
    for k in TEAMS:
        L.append("   - %s: %s" % (k, _fmt_i(A["clear"][k])))
    L.append("4. Screeners whose image interpretation certificate runs out before 1 July 2027:")
    for k in TEAMS:
        L.append("   - %s: %d" % (k, A["certs"][k]))
    L += ["", "### remedial_course_2027_note.docx", "",
          "1. One page giving the order with %s first and %s second, the first-meeting figures it rests on, and why the "
          "overall projection score and d-prime would put another team first." % (a, b), ""]
    text = "\n".join(L)
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(text)
    return figs
