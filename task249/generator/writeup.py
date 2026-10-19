"""figures.json and submission.md for task249, both from the solver's results on the built target."""
import json
import numpy as np
import params as P
import solve as S

NAMES = {e["code"]: e["name"] for e in P.EDITIONS}


def figures(target, files):
    L = S.load(target, files)
    res = S.main_call(L)
    A = L["A"]
    noted = [c for c in P.CODES if res.loc[c, "note"]]
    kept = [c for c in P.CODES if not res.loc[c, "note"]]
    rep = S.report_average(L)
    G = dict(res=res, noted=noted, kept=kept, n_noted=len(noted), reported={c: int(round(rep[c])) for c in P.CODES})
    fam = res[["golden", "g_q", "g_nodev", "g_vis", "g_vis2", "g_pv"]]
    G["min_noted"] = float(fam.loc[noted].min().min())
    G["max_kept"] = float(fam.loc[kept].max().max())
    G["sets"] = {k: S.golden_set(res, k) for k in ("r3a", "r4", "r4p", "r2d", "r2", "r1a", "r1c", "r1b", "r6")}
    G["drop_signin"] = sorted(set(noted) - set(G["sets"]["r3a"]))
    G["drop_print"] = sorted(set(noted) - set(G["sets"]["r2d"]))
    G["drop_ratio"] = sorted(set(noted) - set(G["sets"]["r1a"]))
    # print subscribers on Apple devices, from the register: devices of print accounts and of others, by engine
    dv = A[A["signed"]].drop_duplicates("device_id")
    G["print_wk_pct"] = round(100 * dv.loc[dv["printed"], "wk"].mean())
    G["other_signed_wk_pct"] = round(100 * dv.loc[~dv["printed"], "wk"].mean())
    G["newsletter"] = {c: int(v) for c, v in S.newsletter(target, files).items()}
    sc = S.sold_copies(target, files)
    G["copies"] = {c: int(round(sc[c])) for c in P.CODES}
    import os
    import pandas as pd
    E = pd.read_csv(os.path.join(target, files["nl_log"]), keep_default_na=False)
    adds = E[E["link"].str.contains(S.ADD_PATH, regex=False)]
    G["link_adds_after"] = int((adds["at_utc"] >= str(S.YEAR_END_UTC)).sum())
    G["link_adds_before"] = int((adds["at_utc"] < str(S.YEAR_END_UTC)).sum())
    subs = pd.read_csv(os.path.join(target, files["subs"]), parse_dates=["start_date", "end_date"])
    G["moved_subs"] = S.restore_starts(subs)[1]
    return L, G


def write_figures(path, G):
    out = {
        "filed": {"tolerance_pct": 25, "cap_days": 7, "free_metered_articles": 5, "months": ["2028-10", "2028-11", "2028-12"],
                  "public_holidays_day_of_month": [3, 25, 26, 1], "newsletter_cutoff_utc_hour": 23},
        "call": {"noted": G["noted"], "n_noted": G["n_noted"], "not_noted": G["kept"], "n_not_noted": len(G["kept"]),
                 "noted_names": [NAMES[c] for c in G["noted"]], "not_noted_names": [NAMES[c] for c in G["kept"]]},
        "components": {"noted_floor_pct": int(np.floor(G["min_noted"])), "kept_ceiling_pct": int(np.ceil(G["max_kept"])),
                       "print_devices_webkit_pct": G["print_wk_pct"], "other_signed_devices_webkit_pct": G["other_signed_wk_pct"],
                       "sign_in_split_drops": G["drop_signin"], "device_only_drops": G["drop_print"],
                       "signed_in_ratio_drops": G["drop_ratio"], "link_additions_after_midnight": G["link_adds_after"],
                       "link_additions_before_midnight": G["link_adds_before"], "subscriptions_started_before_quarter": G["moved_subs"]},
        "reported": G["reported"],
        "asks": {"newsletter_subscribers_2028_12_31": G["newsletter"], "sold_copies_per_publication_day_q4": G["copies"]},
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)


def _names(codes):
    n = [NAMES[c] for c in codes]
    return ", ".join(n[:-1]) + " and " + n[-1] if len(n) > 1 else n[0]


def submission(G):
    f = lambda v: "{:,}".format(v)
    noted, kept = G["noted"], G["kept"]
    lo, hi = int(np.floor(G["min_noted"])), int(np.ceil(G["max_kept"]))
    s = []
    s.append("# task249 submission\n")
    s.append("## Tags\n")
    s.append("**Domain:** Product Analytics (metric definition and measurement science: a regional newspaper group's "
             "monthly unique browsers per local edition, counted by an analytics identifier that WebKit drops after seven "
             "days without a visit).")
    s.append("**Analytical objective:** Data Quality Monitoring & Alerting (which editions' published audience figure "
             "fails the 2029 policy's tolerance and carries the measurement note).\n")
    s.append("## 1. Final Recommendation\n")
    s.append("**%s of the twelve editions carry the measurement note in the 2029 media kit: %s; %s print their figures "
             "without it.**\n" % (["Eight", "Seven", "Nine", "Six"][[8, 7, 9, 6].index(len(noted))] if len(noted) in (6, 7, 8, 9) else str(len(noted)),
                                 _names(noted), _names(kept)))
    s.append("Each of the %d reports more than %d per cent above the browsers that read it in October to December 2028, "
             "the other four less than %d per cent, against the policy's 25. Not the sign-in split (signed-in browsers "
             "from the register, signed-out identifiers on signed-out readers of other browsers), which leaves %s under "
             "the line: the meter sits in the same capped storage, so on WebKit it restarts with the identifier and keeps "
             "weekly and occasional readers signed out who on other browsers met the wall and registered (signed-in "
             "WebKit devices carry fewer identifiers a month than the replay gives signed-in readers of other browsers, "
             "while print subscribers' WebKit devices carry as many as the replay gives their other browsers). Not the "
             "device-only replay, which drops %s by pooling print subscribers, who read weekly on Apple devices. Not the "
             "signed-in identifiers per device, which are frequent readers' and drop %s."
             % (len(noted), lo, hi, _names(G["drop_signin"]), _names(G["drop_print"]), _names(G["drop_ratio"])))
    s.append("\n## 2. Critical Components\n")
    s.append("1. On other browsers an identifier is a browser; the seven-day rule replayed on their site-wide session "
             "histories, within edition, month and device class, gives the identifiers a WebKit browser carries.")
    s.append("2. Print subscribers are held apart and counted from the sign-in register: their access does not depend on "
             "the meter, and **%d per cent** of their signed-in devices are WebKit against **%d per cent** of other "
             "signed-in devices." % (G["print_wk_pct"], G["other_signed_wk_pct"]))
    s.append("3. Every other reader is pooled whether signed in or not: registration is a consequence of the cap, so the "
             "comparison is matched only on what the cap cannot change.")
    s.append("4. The %d noted editions overstate by more than **%d per cent**, the other four by less than **%d per cent**."
             % (len(noted), lo, hi))
    s.append("\n## 3. Step-by-Step Solution\n")
    s.append("1. Took the quarter's sessions from web_sessions_2028q4.parquet without is_bot rows, the newsroom's "
             "addresses and the re-sent duplicate rows, HKR read as HOL, months in Berlin time, and WebKit as every iOS "
             "browser and Safari on the Mac (analytics_tag_notes.pdf).")
    s.append("2. Reported figure: each edition's distinct client_ids per month averaged over October to December, the same "
             "as platform_users_by_month_2028.xlsx with HKR and HOL joined.")
    s.append("3. Print subscribers' browsers: client_ids in signin_device_register_2028q4.csv whose account's origin in "
             "reader_accounts.csv is print subscription, counted by device_id.")
    s.append("4. For each edition, month and device class: non-WebKit browsers as client_ids; WebKit print devices "
             "counted; WebKit non-print client_ids divided by the mean number of runs (a new run after more than seven "
             "days between one session's end and the next start, across all editions) that touch the edition and month "
             "among non-WebKit non-print client_ids; summed over device classes and averaged over the three months.")
    s.append("5. Overstatement: reported over estimated browsers less one; %s exceed 25 per cent (%d of 12)."
             % (", ".join(noted), len(noted)))
    s.append("6. Newsletter: status at 2028-12-31 23:00 UTC (midnight in Berlin) from newsletter_contacts_2029-01-15.csv "
             "with each contact's first status event after that moment in newsletter_activity_log.csv (a click is not a "
             "status event). Groups at that moment by undoing every change after it, newest first: the preference "
             "centre's changes in newsletter_group_changes.csv (the groups before) and the editions the newsletters' "
             "one-click links added, the clicked links to /newsletter/ausgabe-hinzufuegen in the activity log, which the "
             "preference centre's log does not hold (%s after midnight; the %s clicked before it stand). Confirmed "
             "subscribers counted in each of their groups." % (f(G["link_adds_after"]), f(G["link_adds_before"])))
    s.append("7. Sold copies: subscription numbers are issued in order as subscriptions are entered (DATA_DICTIONARY.md), "
             "so a start date later than that of a subscription numbered after it is not a first day of delivery: those "
             "%s subscriptions, each shown starting between November and mid-December 2028 (the COMBI ones beside Digital "
             "Plus accesses that started years before), were delivered from before the quarter. Then for each "
             "publication day (Monday to Saturday less 3 October, 25 and 26 December, and 1 November in "
             "Rhineland-Palatinate) the DAILY and COMBI copies and SATURDAY copies on Saturdays, less pauses, plus "
             "e-paper accesses except the Digital Plus accesses (each the e-paper of a COMBI subscription, order_ref "
             "Kombi and its sub_no) and trials, plus delivered less returned single copies, averaged over the edition's "
             "publication days." % f(G["moved_subs"]))
    s.append("8. The %d editions above carry the note in media_kit_2029_edition_figures.xlsx and measurement_note_2029.pdf."
             % len(noted))
    s.append("\n## 4. Deliverable Answers\n")
    s.append("### media_kit_2029_edition_figures.xlsx and measurement_note_2029.pdf\n")
    s.append("1. Editions carrying the measurement note (%d): %s." % (len(noted), ", ".join("%s (%s)" % (c, NAMES[c]) for c in noted)))
    s.append("2. Editions printed without the note (%d): %s." % (len(kept), ", ".join("%s (%s)" % (c, NAMES[c]) for c in kept)))
    s.append("3. Average sold copies per publication day, fourth quarter 2028:")
    for c in P.CODES:
        s.append("   - %s: %s" % (c, f(G["copies"][c])))
    s.append("4. Newsletter subscribers at the end of 31 December 2028:")
    for c in P.CODES:
        s.append("   - %s: %s" % (c, f(G["newsletter"][c])))
    s.append("5. Chart on page 1 of measurement_note_2029.pdf: each edition's reported users against its estimated "
             "browsers, the 25 per cent line drawn and the noted editions marked.")
    return "\n".join(s) + "\n"
