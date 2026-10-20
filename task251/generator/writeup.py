"""figures.json and submission.md, both emitted from the golden computed on the shipped pack."""
import datetime as dt
import json

import numpy as np

import routes as RT
import sim
import solve as S

STATIONS = [s[0] for s in sim.STATIONS]
NAMES = {s[0]: s[1] for s in sim.STATIONS}
TYPES = {"T": "traffic", "U": "urban background", "S": "suburban", "I": "industrial", "R": "rural"}
SEPARATION = 140.0                   # ppm-hours: every check below 96.5 per cent above it, every one at 97.5 or more below
LOW, HIGH = 0.965, 0.975


def _pct(x, nd=1):
    return round(100 * x, nd)


def _d(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def figures(target, F):
    g = S.solve(target, F)
    c = g["call"]
    T = c["table"].set_index("station")
    a = g["asks"]
    D = g["D"]
    r, TR = RT.all_routes(D)
    P = c["points"]
    st = P[P["kind"] != "post-sostituzione"]
    cur = set(T["serial"])
    last = st[st["serial"].isin(cur)].sort_values("start").groupby("serial").tail(1).set_index("serial")
    low = last["eta"].idxmin()
    low_station = T.index[T["serial"] == low][0]
    below97 = P[P["eta"] < LOW]
    above985 = P[P["eta"] >= HIGH]
    ch = S.changes(D)

    def age(p):
        inst = [x for x in ch[p.serial] if S.change_time(x) <= p.start]
        return (p.start - S.change_time(inst[-1])).total_seconds() / 86400

    ages_low = [age(p) for p in below97.itertuples()]
    goes = c["goes"]
    fig = {
        "call": {"bench": goes, "count": len(goes), "stays": len(T) - len(goes),
                 "verdict": {s: ("book" if T.loc[s, "goes"] else "stays") for s in STATIONS},
                 "serial": {s: T.loc[s, "serial"] for s in STATIONS}},
        "components": {"latest_check_lowest_pct": _pct(last.loc[low, "eta"]), "latest_check_lowest_station": low_station,
                       "latest_check_lowest_date": str(last.loc[low, "start"].date()),
                       "latest_checks_below_95": int((last["eta"] < 0.95).sum()),
                       "checks_below_97": int(len(below97)), "separation_ppm_h": SEPARATION,
                       "checks_below_97_age_months": [int(min(ages_low) // 30.4), int(round(max(ages_low) / 30.4))],
                       "bp08_service": str(T.loc["BP08", "service"]), "bp08_converter_since": str(T.loc["BP08", "installed"]),
                       "thresholds_pct": [round(100 * LOW, 1), round(100 * HIGH, 1)],
                       "date_days": {"latest_check": last.loc[low, "start"].day, "bp08_service": T.loc["BP08", "service"].day,
                                     "bp08_since": T.loc["BP08", "installed"].day}},
        "steps": {"titrations": int(len(P)), "titrations_tecnoaria": int((P["who"] == "A").sum()),
                  "titrations_delta": int((P["who"] == "B").sum()), "analyzers_titrated": int(P["serial"].nunique()),
                  "age_route_books": r["pooled_age_quadratic"], "own_trend_books": r["own_trend_in_time"],
                  "threshold_pct": 95, "bench_ceiling": 10, "minutes_rule": 45, "logger_factor": [1.91, 2.05],
                  "standard": "UNI EN 14211", "standard_number": 14211, "minutes_taken": 15,
                  "spare_stint": ["2027-02-08", "2027-03-01"]},
        "asks": {"valid_hours_2027": {s: int(a[s]["valid"]) for s in STATIONS},
                 "mean_2027_ugm3": {s: round(float(a[s]["mean"]), 1) for s in STATIONS},
                 "p19_2027_ugm3": {s: int(round(float(a[s]["p19"]))) for s in STATIONS}},
    }
    # separation asserted where it is stated
    assert below97["D"].min() > SEPARATION + 1 and above985["D"].max() < SEPARATION - 1
    fig["_golden"] = {"table": T, "points": P, "curve": c["curve"], "asks": a, "routes": r, "route_table": TR,
                      "fig": {k: v for k, v in fig.items() if not k.startswith("_")}, "t_end": c["t_end"]}
    return fig


def golden_content(fig):
    return fig["_golden"]


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def submission(fig):
    G = fig["_golden"]
    T = G["table"]
    c, comp, st, a = fig["call"], fig["components"], fig["steps"], fig["asks"]
    go = c["bench"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: the converter "
             "efficiency of a network's chemiluminescence NOx analyzers, checked by gas-phase titration).  ")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Book %d of the 16 station analyzers on the 17 to 21 January 2028 converter bench: %s; the other %d "
             "stay to their scheduled service.** A molybdenum converter is spent by the NO2 it reduces, and carried on "
             "its station's own load to the analyzer's 2028 service each of the seven converters is below 95 per cent "
             "by then. Not none on the latest titrations, every one at %.1f per cent or more. Not BP08 alone on a curve "
             "against converter age, which brings every other converter to its service at about a year old and above "
             "95 per cent.\n" % (c["count"], ", ".join(go), c["stays"], comp["latest_check_lowest_pct"]))
    L.append("## 2. Critical Components\n")
    L.append("1. No converter in service reads below 95 per cent at its latest titration; the lowest is %s's at "
             "**%.1f per cent** on %s." % (comp["latest_check_lowest_station"], comp["latest_check_lowest_pct"],
                                         _d(dt.date.fromisoformat(comp["latest_check_lowest_date"]))))
    L.append("2. The titrations separate on the NO2 the converter had reduced, not on its age: all **%d** below 96.5 "
             "per cent came after more than **%d ppm-hours**, at %d to %d months, and every titration at 97.5 per cent "
             "or more came before %d." % (comp["checks_below_97"], comp["separation_ppm_h"],
                                       comp["checks_below_97_age_months"][0], comp["checks_below_97_age_months"][1],
                                       comp["separation_ppm_h"]))
    L.append("3. BP08's converter, in since %s, stays in to the analyzer's service on **%s**, its 2027 service put "
             "back.\n" % (_d(dt.date.fromisoformat(comp["bp08_converter_since"])),
                         _d(dt.date.fromisoformat(comp["bp08_service"]))))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Put the %d titrations on one scale: Tecnoaria's NO2 misurato over NO2 generato "
             "(titolazioni_Tecnoaria_2025-2026.xlsx) and Delta's rise in NOx less NO over the NO consumed "
             "(titolazioni_Delta_2026-2027.csv), the ratio UNI EN 14211 defines (AQBP-QA-07 section 3)." % st["titrations"])
    L.append("2. Summed each analyzer's hourly no2_ppb in archivio_analizzatori_NOx_2024-2027.csv, each hour once, from "
             "its converter change in registro_interventi_2024-2027.xlsx to each titration: the titrations below 96.5 "
             "per cent all lie past %d ppm-hours." % comp["separation_ppm_h"])
    L.append("3. Fitted one curve to every titration's efficiency against that NO2, linear to a knee and falling "
             "faster past it, and read each converter in service at its NO2 to 31 December 2027.")
    L.append("4. Carried each converter forward on its station's own NO2 from 1 January to its service in "
             "piano_manutenzione_2028.xlsx, the mean of the same days of 2025, 2026 and 2027: %d station analyzers are "
             "below 95 per cent by their service (AQBP-QA-07 section 7)." % c["count"])
    L.append("5. Read no2_orari_validati_2027.csv, each row once, and took as valid the hours coded V or R, less every "
             "hour of which a Delta titration took more than 15 minutes (its ora_inizio and ora_fine, Italian civil "
             "time, put on the database's solar clock), so that the analyzer measured the station's air for under 45 "
             "minutes (AQBP-QA-07 section 5).")
    L.append("6. Gave BP07 the hours filed under MAG from 8 February to 1 March 2027, when the store spare stood in "
             "for its analyzer (the service log), and multiplied the six LGX-300 loggers' values between their "
             "installation and the visit that set them to 20 °C by 1.91 / 2.05 (their factory 0 °C setting).")
    L.append("7. Counted each station's valid hours, their mean NO2 and their 19th highest value (AQBP-QA-07 section 6).")
    L.append("8. Book the %d analyzers on the bench; the other %d stay to their scheduled service.\n"
             % (c["count"], c["stays"]))
    L.append("## 4. Deliverable Answers\n")
    L.append("### turno_banco_convertitori_2028.xlsx\n")
    L.append("1. Each station analyzer's verdict:")
    for s in STATIONS:
        L.append("   - %s, %s (%s): %s" % (s, NAMES[s], c["serial"][s],
                                          "book on the bench" if c["verdict"][s] == "book" else "stays"))
    L.append("2. The bench list: %s, %d analyzers." % (", ".join(go), c["count"]))
    L.append("3. Each station's 2027 NO2 record (valid hours; annual mean, µg/m³; 19th highest hourly value, µg/m³):")
    for s in STATIONS:
        L.append("   - %s: %d valid hours, mean %.1f µg/m³, 19th highest %d µg/m³" % (
            s, a["valid_hours_2027"][s], a["mean_2027_ugm3"][s], a["p19_2027_ugm3"][s]))
    L.append("\n### rendimento_convertitori_2028.png\n")
    L.append("4. Each of the 16 converters' efficiency at its scheduled 2028 service against the 95 per cent line, "
             "with its efficiency at 31 December 2027, the %d analyzers on the bench list marked." % c["count"])
    return "\n".join(L) + "\n"
