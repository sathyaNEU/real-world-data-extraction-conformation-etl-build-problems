"""figures.json: every number the write-up states, as the write-up states it, emitted from the golden."""
import golden as G
import world as W


def r0(x):
    return int(round(x))


def figures(g, info):
    k = g["call_code"]
    t = g["tightest"]
    f = {}
    f["call"] = g["cons"][k]["discharge"]
    f["call_permit"] = g["cons"][k]["permit"]
    f["condition_ref"] = "condition 2.3.1"
    f["hours_in_year"] = int(round(G.YEAR_S / 3600))
    f["call_pff_ls"] = r0(g["pff"][k])
    f["call_delivered_ls"] = r0(g["delivered"][k])
    f["call_rated_ls"] = round(g["stations"][k]["rated"][1], 1)
    f["call_share_of_pff_pct"] = r0(100 * g["delivered"][k] / g["pff"][k])
    f["call_spills_12_24"] = g["lines"][k]["spills"]
    f["call_hours"] = "%.1f" % g["lines"][k]["hours"]
    f["tightest_station"] = g["stations"][t]["name"]
    f["tightest_delivered_ls"] = r0(g["delivered"][t])
    f["tightest_pff_ls"] = r0(g["pff"][t])
    f["dry_day_station"] = g["stations"]["SPS0415"]["name"]
    f["dry_day_station_delivered_ls"] = r0(g["delivered"]["SPS0415"])
    f["dry_day_station_pff_ls"] = r0(g["pff"]["SPS0415"])
    f["high_spiller"] = g["stations"]["SPS0419"]["name"]
    f["high_spiller_spills"] = g["lines"]["SPS0419"]["spills"]
    f["dry_day_spills_hagworth"] = g["routes"]["dry_day"]["SPS0415"]
    f["retired_serials"] = len(g["evidence"])
    rows = {}
    for code in sorted(g["stations"], key=lambda c: g["cons"][c]["permit"]):
        L = g["lines"][code]
        rows[g["cons"][code]["permit"]] = dict(
            overflow=g["cons"][code]["discharge"], pff=r0(g["pff"][code]), delivered=r0(g["delivered"][code]),
            met="No" if code in g["breach"] else "Yes", spills=L["spills"], hours="%.1f" % L["hours"],
            operational="%.1f" % L["operational"])
    f["lines"] = rows
    top = max(g["stations"], key=lambda c: g["lines"][c]["hours"])
    f["chart_top_overflow"] = g["cons"][top]["discharge"]
    f["chart_top_hours"] = "%.1f" % g["lines"][top]["hours"]
    f["counts"] = dict(telemetry_events=info["telemetry_events"], telemetry_levels=info["telemetry_levels"],
                       rain_rows=info["rain_rows"], meter_rows=info["meter_rows"], edm_log_rows=info["edm_log_rows"])
    return f
