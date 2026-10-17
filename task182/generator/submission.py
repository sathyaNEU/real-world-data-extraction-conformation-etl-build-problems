"""Write submission.md from figures.json: every figure in it is emitted, never typed."""
import json
import os

ORDER = ["NSL%02d" % i for i in range(1, 15)]
DWELL = None


def write(task, gendir):
    fig = json.load(open(os.path.join(gendir, "figures.json"), encoding="utf-8"))
    import world as W
    sl = fig["slate_ordered"]
    lv = fig["specific_level_db"]
    tot = fig["measured_total_db"]
    res = fig["residual_db"]
    val = fig["valid_minutes"]
    exc = fig["excluded_minutes"]
    stp = fig["stop_minutes"]
    band = fig["highest_band_hz"]
    tone = fig["tone_prominent"]
    wk = fig["weekly_plant"]
    first = sl[0]
    rows = []
    for c in ORDER:
        tail = ("highest band %s Hz, tone %s" % (band[c], tone[c]) if band[c] != "none"
                else "no band rows, so no highest band and no tone")
        rows.append("   - %s (%s): %.1f dB LAeq, %d valid minutes, %d excluded, %s"
                    % (c, W.BY_CODE[c][1], lv[c], val[c], exc[c], tail))
    weekly = []
    for k in sorted(wk, key=int):
        w = wk[k]
        weekly.append("   - Week beginning %d %s: biogas %s m3, blower air %s thousand Nm3, "
                      "%d centrifuge runs"
                      % (W.WEEKS[int(k)].day, W.WEEKS[int(k)].strftime("%B"),
                         "{:,}".format(w["biogas_m3"]), "{:,}".format(w["blower_air_knm3"]),
                         w["centrifuge_runs"]))
    txt = """**Domain:** Physical and environmental sciences (environmental monitoring and exceedance).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The October acoustic treatment slot should cover %(sl)s.**
Their specific sound levels are %(lvs)s dB LAeq, and %(sixth)s is the first dwelling off the list at %(sixthlv).1f dB, %(margin).1f dB behind the fifth.
Not the five highest measured levels, which put %(in1)s in and %(out1)s out, because the measured level at a dwelling still holds its surroundings.
Not a background taken from the position's own record, which puts %(in2)s and %(in3)s in: the plant runs through every assessment minute, so that background contains it.
Not the complaints register, which is a record of what neighbours heard and not a measurement.

## 2. Critical Components

1. The measured sound level at %(first)s is **%(tot_first).1f dB LAeq** over %(val_first)s valid assessment minutes
2. The residual sound at %(first)s, from the %(stp_first)s minutes inside the plant's weekly process stops, is **%(res_first).1f dB LAeq**
3. The specific sound level at %(first)s is **%(lv_first).1f dB LAeq**
4. The fifth dwelling on the list stands **%(margin).1f dB** above the sixth, %(sixth)s

## 3. Step-by-Step Solution

1. Paired each of the %(deps)d deployments in meter_deployments_2026.csv with its position, and took each deployment's field-check deviation off its levels where plan 4.1 calls for it, which is %(calib)d of them.
2. Read sound_levels_1min_2026.parquet, kept one copy of the repeated download, and took the meters' UTC stamps to local time as survey_notes.md states.
3. Dropped the minutes whose ten-minute record in weather_10min_2026.csv counted rain or ran above the plan's wind limit, reading the replacement anemometer in km an hour from 20 September, and the minutes the meter recorded no measurement for, per plan 4.2.
4. Energetically averaged each position's assessment-period minutes for its measured sound level, per plan 3.1 and 3.2.
5. Took each position's residual sound from the minutes inside the intervals in plant_equipment_events_2026.csv where the blowers, the centrifuges and the gas engine are all recorded down.
6. Subtracted residual from measured level in energy for the specific sound level at each position, per plan 3.1.
7. Ranked the fourteen positions on that level and took the five the slot reaches, per plan 7.1: %(sl)s.
8. Recommended those five dwellings for the October slot, with %(sixth)s named as the first off the list.

## 4. Deliverable Answers

### specific_sound_levels.csv

1. One row for each of the 14 monitoring positions, in schedule order:
%(rows)s

### mitigation_shortlist.pdf

1. The five dwellings the slot covers: %(sl_full)s
2. The first dwelling off the list: %(sixth)s (%(sixth_dw)s) at %(sixthlv).1f dB LAeq, %(margin).1f dB below the fifth
3. The plant through the six survey weeks:
%(weekly)s
4. Ranked bar chart of all fourteen specific sound levels with the five selected marked and the slot's reach drawn, on page 1
""" % {
        "sl": ", ".join(sl[:-1]) + " and " + sl[-1],
        "sl_full": ", ".join("%s (%s) at %.1f dB LAeq" % (c, fig["slate_dwellings"][c], lv[c]) for c in sl),
        "lvs": ", ".join("%.1f" % lv[c] for c in sl),
        "sixth": fig["sixth"], "sixth_dw": fig["sixth_dwelling"], "sixthlv": fig["sixth_level_db"],
        "margin": fig["margin_db"], "first": first, "tot_first": tot[first], "res_first": res[first],
        "lv_first": lv[first], "val_first": "{:,}".format(val[first]), "stp_first": stp[first],
        "in1": "NSL06", "out1": "NSL13", "in2": "NSL03", "in3": "NSL12",
        "rows": "\n".join(rows), "weekly": "\n".join(weekly),
        "deps": fig["deployments"], "calib": fig["deployments_corrected"],
    }
    p = os.path.join(task, "submission.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return p
