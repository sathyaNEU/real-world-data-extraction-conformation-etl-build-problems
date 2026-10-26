"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P

F = P.FILES
NETS = ["Central", "University", "Riverside", "Old Town", "Hillcrest"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def c(x):
    return "{:,}".format(int(x))


def usd(x):
    return "USD {:,}".format(int(x))


def write(path, fig):
    best = fig["recommended_network"]
    nr, ta, pl = fig["net_revenue"], fig["turned_away"], fig["pilot"]
    rp = fig["recorded_route_pick"]
    order = sorted(NETS, key=lambda n: -fig["net_revenue_exact"][n])
    t = ["## Tags\n",
         "**Domain:** Product analytics (churn propensity and uplift modelling).",
         "**Analytical objective:** Opportunity sizing and decision support.\n",
         "## 1. Final Recommendation\n",
         "**Put the %d e-bikes on the %s network: at 2025 demand they add %s a year in net fare revenue there.**"
         % (fig["constants"]["ebikes"], best, usd(nr[best])),
         "A ride exists only when a rider finds a bike, and %s's residence-hall hubs run empty at the class changes: its "
         "stations turned away about %s requests in 2025, %.1f per cent of its demand, and with e-bikes at every station "
         "those riders ride and pay a full fare. %s, which leads on the rides its stations served (%s on that view), "
         "adds %s, because most of its e-bike rides would only replace a classic ride.\n"
         % (best, c(ta[best]), fig["turned_away_share"][best], rp, usd(fig["recorded_route"][rp]), usd(nr[rp])),
         "## 2. Critical Components\n",
         "1. Rebuilt from the 03:00 audit, every undock and dock and every van move, %s's stations stood empty while "
         "riders came for bikes: about **%s** requests turned away in 2025 (**%.1f** per cent of its demand of about "
         "**%s**), against about **%s** (**%.1f** per cent) on %s."
         % (best, c(ta[best]), fig["turned_away_share"][best], c(fig["requests"][best]), c(ta[rp]),
            fig["turned_away_share"][rp], rp),
         "2. The Harbour pilot measures what e-bikes do where every request finds a bike: **%.1f** per cent of rides at "
         "pilot stations went on an e-bike, pilot stations drew **%.1f** per cent more rides than comparison stations, "
         "and an e-bike ride paid **USD %.2f** more than a classic ride." % (pl["ebike_share"], pl["uplift"], pl["premium"]),
         "3. Net fare revenue a year at 2025 demand: %s. On the rides the stations served alone, %s would lead at **%s**."
         % ("; ".join("%s **%s**" % (n, usd(nr[n])) for n in order), rp, usd(fig["recorded_route"][rp])),
         "",
         "## 3. Step-by-Step Solution\n",
         "1. Put the four trip exports on one footing: %s and %s (old trip system: station names, bike_no, account_no, "
         "fares in USD) and %s and %s (new platform: station codes, vehicle_id, account_id, fares in cents), every time "
         "as Central Time, stations through %s and %s; an undock of under %d seconds that ends where it started is a false "
         "start, kept as an undock and a dock but not counted as a ride or a request."
         % (F["q1"], F["q2"], F["q3"], F["q4"], F["stations"], F["regions"], fig["constants"]["false_start_seconds"]),
         "2. Rebuilt each station's classic bikes second by second: the count in %s at 03:00 each day, less each classic "
         "undock, plus each classic dock, plus and minus the classic moves in %s (UTC), an undock taken before a dock in "
         "the same second." % (F["audit"], F["moves"]),
         "3. For each station, month, weekday or weekend and local hour: requests per stocked second (undocks over the "
         "seconds it held a bike), times the seconds it stood empty, is the requests it turned away; summed by network.",
         "4. The pilot, from %s's station table: the e-bike share of the rides from pilot stations, the rides a pilot "
         "station drew over the rides a comparison station drew, less 1, and the mean e-bike fare less the mean classic "
         "fare at pilot stations." % F["pilot"],
         "5. Each network's net fare revenue: the requests turned away plus the uplift on demand, at the network's mean "
         "classic fare, plus the e-bike share of demand grown by the uplift, at the e-bike premium; demand is the classic "
         "rides plus the requests turned away. That is what riders would pay with the e-bikes less what they paid in "
         "2025, at 2025 demand (%s, section 2), rounded to the nearest %s." % (F["board"], usd(fig["constants"]["rounding_usd"])),
         "6. People: the accounts in %s with a ride in 2025 (January to June through legacy_account_no), one person per "
         "account except that accounts on one card_fingerprint are one person where the later account was opened after "
         "the earlier account's last ride; counted by home_area with case and spaces set aside." % F["accounts"],
         "7. Energy: the sessions in %s by the local month of plug_out_utc, each session once: a session whose station, "
         "point and meter_start_wh and meter_stop_wh repeat a session received earlier is a controller re-send; "
         "energy_kwh summed." % F["charging"],
         "8. Workshop: the jobs in %s by the local quarter of opened_utc and asset class, leaving out a job opened on a "
         "bike with no ride since its previous job closed (the repair's road test failing), over the rides of that class "
         "in that quarter (false starts out), per %s rides." % (F["workshop"], c(fig["constants"]["per_rides"])),
         "",
         "## 4. Deliverable Answers\n",
         "### ebike_deployment_2027.docx\n",
         "1. The network for the e-bikes: %s." % best,
         "2. The net fare revenue they add there a year: %s." % usd(nr[best]),
         "3. Every network's net fare revenue a year, to the nearest %s:" % usd(fig["constants"]["rounding_usd"])]
    t += ["   - %s: %s" % (n, usd(nr[n])) for n in NETS]
    t += ["", "### ebike_deployment_2027.xlsx\n", "4. People who rode with us in 2025, by the network they live in:"]
    t += ["   - %s: %s" % (n, c(fig["people"][n])) for n in NETS]
    t += ["5. Energy the Harbour pilot's charging points delivered in 2025, kWh:"]
    t += ["   - %s: %s" % (m, c(fig["energy_kwh"][m])) for m in MONTHS]
    t += ["6. Workshop jobs per %s rides in 2025:" % c(fig["constants"]["per_rides"])]
    t += ["   - E-bikes, Q%d: %.1f" % (q, fig["workshop_per_10000"]["E-bike Q%d" % q]) for q in range(1, 5)]
    t += ["   - Classic bikes, Q%d: %.1f" % (q, fig["workshop_per_10000"]["Classic Q%d" % q]) for q in range(1, 5)]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
