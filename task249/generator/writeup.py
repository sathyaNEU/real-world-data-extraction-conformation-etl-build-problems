"""figures.json and submission.md for task249, both from the solver's results on the built target."""
import json
import params as P
import solve as S

WEEKS = ["3 July", "10 July", "17 July", "24 July"]
WK_KEY = ["week_of_3_july", "week_of_10_july", "week_of_17_july", "week_of_24_july"]


def figures(target, files):
    L = S.load(target, files)
    df, rt, st = S.main_call(L)
    acc = df.to_dict("records")
    G = dict(accounts=acc, n_flag=int(df["flag"].sum()), flagged=[a["code"] for a in acc if a["flag"]],
             kept=[a["code"] for a in acc if not a["flag"]], study_short=st["study_short"], study_long=st["study_long"],
             gain_c=rt["c"], gain_a=rt["a"], gain_tau=rt["tau"],
             gain_2=float(rt["c"] + rt["a"] * __import__("math").exp(-2 / rt["tau"])),
             exposure=S.ask_exposure(target, files), impersonation=S.ask_impersonation(target, files),
             interrupted=S.ask_interrupted(target, files))
    G["shrink"] = S.shrinkage_check(rt)
    G["kelley_adds"] = sorted(set(df.loc[df["kelley_reported"] > P.CAP, "code"]) - set(G["flagged"]))
    G["no_gain_adds"] = sorted(set(df.loc[df["no_gain"] > P.CAP, "code"]) - set(G["flagged"]))
    G["const_se_drops"] = sorted(set(G["flagged"]) - set(df.loc[df["const_se"] > P.CAP, "code"]))
    G["rested"] = G["exposure"][0]["rested_2029"]
    G["min_flag"] = float(min(a["gold"] for a in acc if a["flag"]))
    G["max_keep"] = float(max(a["gold"] for a in acc if not a["flag"]))
    e_depth = [a["depth"] for a in acc if a["code"] in ("KSP", "VRD", "ANV", "PRM", "SQR", "ABH", "MTL", "TJM")]
    G["elite_depth_lo"], G["elite_depth_hi"] = float(min(e_depth)), float(max(e_depth))
    return L, G


def write_figures(path, G):
    out = {
        "filed": {"standard_cap_section": 3.3, "conditional_error_table": 4.3, "band_multiple": 1.96,
                  "exposure_ceiling_pct": 12, "restart_reference_release": "5.3.2"},
        "call": {"flagged": sorted(G["flagged"]), "n_flagged": G["n_flag"], "kept": sorted(G["kept"]), "n_kept": len(G["kept"]),
                 "min_flagged_share_pct_floor": int(100 * G["min_flag"] // 5 * 5)},
        "components": {"study_rate_within_3_days_pct": round(100 * G["study_short"], 1),
                       "study_rate_6_weeks_or_more_pct": round(100 * G["study_long"], 1),
                       "retest_gain_c": round(G["gain_c"], 2), "retest_gain_a": round(G["gain_a"], 2),
                       "retest_gain_tau_days": round(G["gain_tau"], 1), "retest_gain_at_2_days": round(G["gain_2"], 2),
                       "elite_depth_lo_pct": round(100 * G["elite_depth_lo"], 1),
                       "elite_depth_hi_pct": round(100 * G["elite_depth_hi"], 1), "cap_pct": 15,
                       "study_top_tenth_n": G["shrink"]["n"],
                       "study_top_tenth_mat_v_scored": round(G["shrink"]["scored"], 3),
                       "study_top_tenth_mat_v_at_ability": round(G["shrink"]["at_ability"], 3),
                       "study_top_tenth_mat_v_at_reported_error": round(G["shrink"]["at_reported"], 3),
                       "kelley_reported_error_adds": G["kelley_adds"], "no_gain_adds": G["no_gain_adds"],
                       "constant_error_drops": G["const_se_drops"]},
        "asks": {
            "items_over_ceiling": {WK_KEY[e["week"]]: e["over"] for e in G["exposure"]},
            "items_rested_for_2029": G["rested"],
            "impersonations_confirmed": {t["tier"]: t["confirmed"] for t in G["impersonation"]},
            "impersonations_per_thousand_shortlisted": {t["tier"]: round(t["per_thousand"], 1) for t in G["impersonation"]},
            "interrupted_share_pct": {d["device"]: round(d["share"], 2) for d in G["interrupted"]},
            "interrupted_finished_on_another_device": {d["device"]: d["moved"] for d in G["interrupted"]},
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    return out


def submission(G):
    names = {a["code"]: a["client"] for a in G["accounts"]}
    fl = G["flagged"]
    lines = []
    lines.append("# task249 submission\n")
    lines.append("## Tags\n")
    lines.append("**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: an assessment "
                 "firm's unproctored adaptive aptitude test, MAT-R, checked by a proctored verification test, MAT-V, at "
                 "client employers' selection days).")
    lines.append("**Analytical objective:** Data Quality Monitoring & Alerting (how often the new verification check would "
                 "refer genuine candidates at each client account in 2029, and so which accounts move to the extended "
                 "verification before the season).\n")
    lines.append("## 1. Final Recommendation\n")
    lines.append("**Move %d accounts to MAT-V Extended for 2029: %s; the other %d stay on the 12-item MAT-V.**\n"
                 % (G["n_flag"], ", ".join(fl), len(G["kept"])))
    lines.append("On their 2029 plans each of the %d would see its check refer at least %d per cent of its genuine "
                 "shortlisted candidates, against the 15 per cent cap of MAL-IS-04 section 3.3, while the other %d stay "
                 "under the cap. The equivalence study's own rates (%.1f per cent within three days, %.1f per cent at six "
                 "weeks or more) keep every account under the cap, because its volunteers were not shortlisted on MAT-R.\n"
                 % (G["n_flag"], int(100 * G["min_flag"] // 5 * 5), len(G["kept"]), 100 * G["study_short"], 100 * G["study_long"]))
    lines.append("## 2. Critical Components\n")
    lines.append("1. An account shortlists on MAT-R, so the candidates it invites are those whose MAT-R estimate ran above "
                 "their ability, by more the smaller the share it shortlists (the eight finance, consulting and analytics accounts take %.1f to "
                 "%.1f per cent of their applicants) and where MAT-R's standard error widens above +1 logit (Table 4.3); "
                 "their MAT-V falls short of MAT-R by that much and s.3.2 reads the shortfall."
                 % (100 * G["elite_depth_lo"], 100 * G["elite_depth_hi"]))
    lines.append("2. MAT-V sat soon after MAT-R runs higher (the study's retest gain, fitted %.2f + %.2f exp(-days/%.1f) "
                 "logit, %.2f at two days): it keeps the mid-sized day-one accounts %s under the cap, not the day-one "
                 "accounts that shortlist most selectively, %s, whose shortlisted candidates sit where MAT-R's error is "
                 "widest."
                 % (G["gain_c"], G["gain_a"], G["gain_tau"], G["gain_2"], ", ".join(G["no_gain_adds"]),
                    ", ".join(G["const_se_drops"])))
    lines.append("3. The shortfall is read with MAT-R's error at the candidate's ability, not at the estimate. On the "
                 "study's own top tenth of MAT-R scorers (%d volunteers), true-score shrinkage with Table 4.3's error at "
                 "the shrunken ability predicts their mean MAT-V within a fiftieth of a logit of what they scored; with each "
                 "volunteer's reported error (the error at the estimate, manual s.4.2) it predicts about a tenth of a logit "
                 "too low, and the same shortcut on the accounts' pools moves %s over the cap."
                 % (G["shrink"]["n"], ", ".join(G["kelley_adds"])))
    lines.append("4. Carrying the study's own rates (%.1f per cent within three days, %.1f per cent at six weeks or more) "
                 "moves no account; one MAT-R error for every ability leaves %s under the cap; leaving out the retest gain "
                 "moves %s over it.\n"
                 % (100 * G["study_short"], 100 * G["study_long"], ", ".join(G["const_se_drops"]), ", ".join(G["no_gain_adds"])))
    lines.append("## 3. Step-by-Step Solution\n")
    lines.append("1. Pool per account: candidates whose 2028 result was shared with it (results_shared_2028.csv, PGL folded "
                 "into NVK per client_accounts.csv, each candidate once), at their completed MAT-R attempt among registered "
                 "candidates (mat_r_attempts_2028.parquet, candidate_register_2028.csv).")
    lines.append("2. Depth: the 2029 plan's shortlist over its expected applicants (client_plans_2029.xlsx).")
    lines.append("3. Interval from MAT-R to MAT-V: two days at day-one and first-company drives (Calendar sheet: sitting on "
                 "day 1, selection day on day 3); otherwise the plan's selection days against the July 2029 test weeks.")
    lines.append("4. Retest gain: equivalence study pairs, MAT-V minus MAT-R by interval in days (dates in the file), fitted "
                 "by least squares weighted by pairs to c + a exp(-days/tau).")
    lines.append("5. For each account: abilities drawn normal with the pool's mean and the pool's variance less its mean "
                 "squared standard error; MAT-R = ability + error at Table 4.3's MAT-R value; the top share by depth "
                 "shortlisted; MAT-V = ability + retest gain at the interval + error at Table 4.3's MAT-V value; referred "
                 "when MAT-R exceeds MAT-V + 1.96 x MAT-V's standard error at its estimate; the referred share of the "
                 "shortlisted.")
    lines.append("6. Over 15 per cent: MAT-V Extended.")
    lines.append("7. Exposure (MAL-IS-04 s.4): every attempt by a candidate in the register (interrupted attempts included; "
                 "identities outside the register are not candidates, s.2), test weeks Monday to Sunday in IST, the distinct "
                 "candidates shown each item over the week's distinct candidates; an item over 12 per cent in any week is "
                 "rested for 2029.")
    lines.append("8. Impersonations (s.5): one sitting per candidate a season, so a sitting's standing is the latest decision "
                 "on any of the candidate's cases, the desk's appeal cases included (confirmed impersonation or confirmed on "
                 "appeal stands; overturned on appeal or cleared does not); tier through the candidate register and the "
                 "college register; per thousand distinct candidates on any 2028 shortlist.")
    lines.append("9. Interruptions (s.6): a candidate's attempts in time order make up the season's booking, linked by "
                 "candidate (from release 5.3.2 a restart carries a fresh booking reference); the booking's device is its "
                 "first attempt's; interrupted when any attempt was interrupted; finished on another device when the last "
                 "attempt ran on a different device.\n")
    lines.append("## 4. Deliverable Answers\n")
    lines.append("### verification_bands_2029.xlsx and account_referral_note_2029.pdf\n")
    lines.append("**MAT-V Extended (%d):** %s." % (G["n_flag"], ", ".join("%s (%s)" % (c, names[c]) for c in fl)))
    lines.append("**Standard MAT-V (%d):** %s.\n" % (len(G["kept"]), ", ".join(G["kept"])))
    lines.append("### Item exposure, July 2028 test weeks (ceiling 12 per cent)\n")
    lines.append("| Test week beginning | Items over 12 per cent |")
    lines.append("|---|---|")
    for e in G["exposure"]:
        lines.append("| %s | %d |" % (WEEKS[e["week"]], e["over"]))
    lines.append("\nItems to be rested before the 2029 season (over 12 per cent in any test week): %d.\n" % G["rested"])
    lines.append("### Impersonations standing confirmed, 2028\n")
    lines.append("| College tier | Sittings confirmed | Per thousand candidates shortlisted |")
    lines.append("|---|---|---|")
    for t in G["impersonation"]:
        lines.append("| %s | %d | %.1f |" % (t["tier"], t["confirmed"], t["per_thousand"]))
    lines.append("\n### Interrupted bookings, 2028\n")
    lines.append("| Device | Share of bookings started on it interrupted | Interrupted bookings finished on another device |")
    lines.append("|---|---|---|")
    for d in G["interrupted"]:
        lines.append("| %s | %.2f per cent | %d |" % (d["device"], d["share"], d["moved"]))
    return "\n".join(lines) + "\n"
