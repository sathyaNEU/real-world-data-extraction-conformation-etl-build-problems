"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import build as B
import golden as GD
import solve as S


def c(x):
    return "{:,}".format(int(x))


def write(path, F):
    FL = B.FILES
    win = F["call_region"]
    L = F["listed"]
    p = F["pilot"]
    q = F["quit_rate_pct"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Epidemiology and public health (health burden and impact modelling).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Place the 2027 quit outreach team in %s: it will help about %d patients there to quit.**"
             % (win, F["call_quits"]))
    t.append("About %d per cent of %s's %s recorded smokers will still smoke when the team calls. Not Coastal "
             "Hinterland, which lists the most (%s) but whose records are older and whose smokers stop more than twice "
             "as fast, so only about half its list still smokes in 2027. Not Western Plains, whose list is at least as "
             "current but smaller (%s). Not Northern Corridor, with a smaller list (%s) whose smokers stop faster.\n"
             % (F["call_still_pct"], win, c(L[win]), c(L["Coastal Hinterland"]), c(L["Western Plains"]),
                c(L["Northern Corridor"])))
    t.append("## 2. Critical Components\n")
    t.append("1. %s's practices record **%s** active patients as current smokers in the 30 September 2026 extract."
             % (win, c(L[win])))
    t.append("2. About **%d** per cent of them will still smoke when called in 2027, read from %s's own consecutive "
             "status recordings." % (F["call_still_pct"], win))
    t.append("3. The 2025 team helped about **%d** per cent of the listed patients who still smoked when it called to "
             "quit." % F["quits_per100_still"])
    t.append("\n## 3. Step-by-Step Solution\n")
    t.append("1. Counted each candidate's active patients whose status in %s is daily, weekly or irregular smoker or "
             "smoker (%s): Coastal Hinterland %s, Inner South %s, Northern Corridor %s, Western Plains %s."
             % (FL["extract"], FL["dictionary"], c(L["Coastal Hinterland"]), c(L["Inner South"]),
                c(L["Northern Corridor"]), c(L["Western Plains"])))
    t.append("2. Kept the last entry of each day in %s, paired every smoker or ex-smoker entry with the patient's next "
             "entry (never smoked read as not smoking) and fitted each sub-region's yearly rates of stopping and of "
             "relapse to its own pairs as a two-state Markov process by maximum likelihood: stopping about %d per cent "
             "a year in Coastal Hinterland, %d in Inner South, %d in Northern Corridor and %d in Western Plains, "
             "relapse about %.1f per cent."
             % (FL["history"], q["Coastal Hinterland"], q["Inner South"], q["Northern Corridor"], q["Western Plains"],
                F["relapse_pct"]))
    t.append("3. Averaged each listed patient's chance of still smoking over calls spread evenly through 2027 from the "
             "date of their status: about %d per cent of %s's list, about half of Coastal Hinterland's."
             % (F["call_still_pct"], win))
    t.append("4. In %s the team reached %s of its %s patients (%.1f per cent) and %s told it they had stopped; %s of "
             "the %s smokers it reached (%.1f per cent) were not smoking four weeks after their quit date, lost to "
             "follow-up counted as smoking per %s: about %d per cent of the listed patients still smoking when called."
             % (FL["log"], c(p["reached"]), c(p["listed"]), F["pilot_reach_pct"], c(p["stopped"]), c(p["quits"]),
                c(p["smokers_reached"]), F["pilot_quit_per_smoker_reached_pct"], FL["plan"],
                F["quits_per100_still"]))
    t.append("5. Multiplied each list's expected smokers at the call by that rate: %s about %d quits, the most of the "
             "four." % (win, F["call_quits"]))
    t.append("6. Matched %s's practice names to %s (case, Pty Ltd, Med Centre and GP spellings aside) and summed 2025's "
             "referrals by the register's sub-region, Quitline's phn_sub_region column placing four "
             "practices in other sub-regions than the register does." % (FL["quitline"], FL["practices"]))
    t.append("7. In %s started each leg its duration_s before its date_time, the dialler writing a leg's record when its "
             "line is released (each of the %s Transferred legs shares its patient's answered leg's date_time to the "
             "second, and read this way no team member's legs overlap); counted the calls to patients from 5 pm, the "
             "Transferred legs to Quitline aside, and the answered ones by weekday; and for each login and month took "
             "its answered legs' minutes less its Transferred legs', the coach leaving at the transfer while the "
             "patient's leg stays open to the end, per patient it reached." % (FL["dialler"], c(F["transfer_legs"])))
    t.append("\n## 4. Deliverable Answers\n")
    t.append("### %s\n" % GD.DOCX)
    t.append("1. Place the team in %s for 2027: about %d quits." % (win, F["call_quits"]))
    t.append("2. Horizontal bar chart of the four candidate sub-regions' expected 2027 quits, %s highlighted and "
             "labelled about %d." % (win, F["call_quits"]))
    t.append("\n### %s\n" % GD.XLSX)
    t.append("1. Quitline referrals from each candidate sub-region's practices in 2025:")
    for g in S.CANDS:
        t.append("   - %s: %s" % (g, c(F["ask_referrals"][g])))
    t.append("2. Calls the 2025 team made to patients from 5 pm, and patients reached in them, by weekday:")
    for d in S.WEEKDAYS:
        v = F["ask_evening"][d]
        t.append("   - %s: %s calls, %s patients reached" % (d, c(v["calls"]), c(v["reached"])))
    t.append("3. Minutes each team member spent on answered calls per patient they reached, by dialler login and month "
             "of 2025 (February to November):")
    for ag, months in F["ask_talk_min"].items():
        t.append("   - %s: %s" % (ag, ", ".join("%.1f" % v for v in months.values())))
    open(path, "w").write("\n".join(t) + "\n")
