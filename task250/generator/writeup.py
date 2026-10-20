"""figures.json and submission.md, both emitted from the golden computed on the shipped pack."""
import json
import os

import numpy as np

import params as P
import routes as RT
import solve as S


def figures(target, F):
    g = S.solve(target)
    reg = S.register(target)
    c = g["call"]
    per = c["per_year"]
    whole = {k: int(round(v)) for k, v in per.items()}
    keep = reg["baja_prevista"].isna()
    r = RT.all_routes(target, reg)
    rerun = {k: int(round(v)) for k, v in r["rerun_2028_network"].items()}
    runner = max(k for k in P.SETTINGS if k < c["setting"])
    names = [nm for _, nm in P.DISTRICTS]
    cut = {k: c["parts"][k][1] for k in P.SETTINGS}
    return {
        "call": {"setting": c["setting"], "alerts_a_year": whole[c["setting"]],
                 "runner_up": runner, "runner_up_alerts_a_year": whole[runner],
                 "per_setting_alerts_a_year": {"%.1f" % k: whole[k] for k in P.SETTINGS}},
        "components": {"stations_kept": int(keep.sum()), "stations_closing": int((~keep).sum()),
                       "rerun_at_runner_up": rerun[runner],
                       "rerun_alerts_a_year": {"%.1f" % k: rerun[k] for k in P.SETTINGS},
                       "drift_alert_adjustments_kept": c["repairs_kept"],
                       "drifts_cut_short": {"%.1f" % k: cut[k] for k in P.SETTINGS}},
        "steps": {"drift_alert_visits_in_plan": c["budget"], "settings": list(P.SETTINGS), "radius_km": int(P.RADIUS_KM),
                  "neighbours": P.N_NEIGHBOURS, "window_days": P.WINDOW, "min_in_window": P.MIN_IN_WINDOW,
                  "hold_days": P.HOLD_DAYS, "stations_registered": len(reg), "lookback_days": 14,
                  "alert_window_days": 10, "opening_window_days": 3, "years": 3},
        "asks": {"drift_alert_visits_2027": {nm: g["ask_a"][nm]["visits"] for nm in names},
                 "days_alerts_waited_2027": {nm: g["ask_a"][nm]["days_waited"] for nm in names},
                 "breakdown_visits_2027_stations_kept": {nm: g["ask_b"][nm] for nm in names}},
        "_golden": {"per_year": per, "alerts_year_whole": whole, "rerun": rerun, "cut": cut, "budget": c["budget"],
                    "setting": c["setting"], "alerts_at_setting": whole[c["setting"]], "runner_up": runner,
                    "n_keep": int(keep.sum()), "n_close": int((~keep).sum()), "repairs_kept": c["repairs_kept"],
                    "ask_a": g["ask_a"], "ask_b": g["ask_b"]},
    }


def golden_content(fig):
    return fig["_golden"]


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def submission(fig):
    c, comp, st, a = fig["call"], fig["components"], fig["steps"], fig["asks"]
    ps = c["per_setting_alerts_a_year"]
    rr = comp["rerun_alerts_a_year"]
    cut = comp["drifts_cut_short"]
    ru = "%.1f" % c["runner_up"]
    names = [nm for _, nm in P.DISTRICTS]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: the daily "
             "spatial-consistency check of an agro-climatic station network's air temperature).  ")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Run the %.1f setting from the January 2028 configuration: it raises %d drift alerts a year, within the "
             "%d visits the field plan leaves for them.** At %.1f the quality control would raise %d a year: the record "
             "re-run with the 2028 network raises %d, and %d drifts the record's own alerts repaired at kept stations "
             "never reached the %.1f limit before their repair and would have kept growing until they did. Not %.1f on "
             "the re-run alone, which counts those drifts only as far as the 3.0 alerts let them run.\n"
             % (c["setting"], c["alerts_a_year"], st["drift_alert_visits_in_plan"], c["runner_up"],
                c["runner_up_alerts_a_year"], rr[ru], cut[ru], c["runner_up"], c["runner_up"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The 2028 network is **%d stations**: the register's %d less the **%d** closing on 31 December 2027."
             % (comp["stations_kept"], st["stations_registered"], comp["stations_closing"]))
    L.append("2. Re-run on the 2025 to 2027 record with that network and the limits set from the recorded statistic, "
             "the quality control raises **%d, %d, %d and %d** drift alerts a year at 3.0, 3.5, 4.0 and 4.5."
             % (rr["3.0"], rr["3.5"], rr["4.0"], rr["4.5"]))
    L.append("3. The sensor history holds **%d** adjustments or replacements at drift-alert visits to kept stations; the "
             "re-run never reaches **%d, %d, %d and %d** of them before their repair at 3.0, 3.5, 4.0 and 4.5."
             % (comp["drift_alert_adjustments_kept"], cut["3.0"], cut["3.5"], cut["4.0"], cut["4.5"]))
    L.append("4. Each setting's drift alerts a year in 2028: **%d, %d, %d and %d** at 3.0, 3.5, 4.0 and 4.5; the most "
             "sensitive within the **%d** visits is **%.1f**.\n"
             % (ps["3.0"], ps["3.5"], ps["4.0"], ps["4.5"], st["drift_alert_visits_in_plan"], c["setting"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took the 2028 network from registro_estaciones.xlsx (sheet Estaciones): the %d stations less the %d with "
             "a baja_prevista of 31/12/2027, %d stations." % (st["stations_registered"], comp["stations_closing"],
                                                              comp["stations_kept"]))
    L.append("2. Re-ran QC-02 sections 4, 5 and 8 on the anomalies in control_calidad_2025-2027.parquet with the %d kept "
             "stations as the network (the %d nearest with an anomaly that day within %d km, inverse-square weights, the "
             "%d-day mean where at least %d residuals exist, so from 10 January 2025 as in the export, no alert within %d "
             "days of the last), against each station's "
             "limit by section 6 (the setting times the standard deviation, n - 1, of its estadistico_14d over 2025 to "
             "2027), counting the kept stations' alerts: %d, %d, %d and %d a year at 3.0, 3.5, 4.0 and 4.5."
             % (comp["stations_kept"], st["neighbours"], st["radius_km"], st["window_days"], st["min_in_window"],
                st["hold_days"], rr["3.0"], rr["3.5"], rr["4.0"], rr["4.5"]))
    L.append("3. Took the drifts the record's alerts cut short from the sheet Historial sensor T: every row with motivo "
             "Alerta de deriva (an adjustment or a replacement, as-found error recorded) at a kept station, %d, each "
             "answering the station's latest alert in the export on or before its day, within %d days."
             % (comp["drift_alert_adjustments_kept"], st["alert_window_days"]))
    L.append("4. A drift goes on growing until a check sets it right (QC-02 section 9), so a drift the re-run's alerts "
             "at a setting never reached, from %d days before the alert its visit answered to the adjustment, would "
             "have raised one alert at that setting later, each two months or more before its station's next spring "
             "round: %d, %d, %d and %d drifts at 3.0, 3.5, 4.0 and 4.5, added to the re-run's count and the three years "
             "divided by %d: %d, %d, %d and %d a year."
             % (st["lookback_days"], cut["3.0"], cut["3.5"], cut["4.0"], cut["4.5"], st["years"],
                ps["3.0"], ps["3.5"], ps["4.0"], ps["4.5"]))
    L.append("5. Chose the most sensitive setting within the %d drift-alert visits in plan_campo_2028.pdf: %.1f."
             % (st["drift_alert_visits_in_plan"], c["setting"]))
    L.append("6. Took the 2027 drift-alert visits from ordenes_trabajo_2025-2027.xlsx: on the old contractor's sheet every "
             "Alerta deriva order closed with a Visita, on that day; on the new contractor's sheet each station of a "
             "closed Corrective opened within %d days of an alert there, on the first day from its opening to its "
             "visit_date with readings at the station in comprobaciones_patron_2025-2027.csv (under whatever order), "
             "leaving out a day with a reading outside the station's tmin to tmax in estaciones_diario_2025-2027.csv (a "
             "sensor read in a bath, not the check in place in the station's air that every visit includes, "
             "plan_campo_2028.pdf), and no visit where no such day exists. Days waited run from the alert's day in the "
             "quality-control export." % st["opening_window_days"])
    L.append("7. Took the 2027 breakdown visits at kept stations as the old contractor's Avería orders closed with a "
             "Visita and, by the same reading test, the stations of the new contractor's closed Correctives that "
             "answered no alert.")
    L.append("8. Run the %.1f setting in 2028.\n" % c["setting"])
    L.append("## 4. Deliverable Answers\n")
    L.append("### drift_alert_setting_2028.xlsx\n")
    L.append("1. Drift alerts a year in 2028, by setting:")
    for k in P.SETTINGS:
        L.append("   - %.1f: %d" % (k, ps["%.1f" % k]))
    L.append("2. The setting: %.1f, %d drift alerts a year." % (c["setting"], c["alerts_a_year"]))
    L.append("3. Drift-alert visits made in 2027 and the days their alerts waited for them in total, by district:")
    for nm in names:
        n = a["drift_alert_visits_2027"][nm]
        L.append("   - %s: %d visit%s, %d days" % (nm, n, "" if n == 1 else "s", a["days_alerts_waited_2027"][nm]))
    L.append("4. Breakdown visits made in 2027 at the stations kept in 2028, by district:")
    for nm in names:
        L.append("   - %s: %d" % (nm, a["breakdown_visits_2027_stations_kept"][nm]))
    L.append("\n### alerts_by_setting_2028.png\n")
    L.append("5. Bar chart of each setting's drift alerts a year in 2028 against a line at the field plan's %d visits, "
             "each bar split into the network re-run's alerts and the drifts the record's alerts cut short, the %.1f bar "
             "marked as the setting." % (st["drift_alert_visits_in_plan"], c["setting"]))
    return "\n".join(L) + "\n"
