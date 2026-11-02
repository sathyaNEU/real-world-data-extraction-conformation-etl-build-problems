"""Emits figures.json and submission.md from the analysis of the cut pack."""
import json, os

ORDER = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6"]


def figures(E):
    C = E["call"]
    K = E["D"]["K"]
    des = [k for k in ORDER if k in C["designated"]]
    F = {
        "designated": des,
        "share_pct": {k: int(round(C["risers"][k]["share"])) for k in des},
        "nearest": C["nearest"],
        "nearest_share_pct": int(round(C["risers"][C["nearest"]]["share"])) if C["nearest"] else None,
        "all_share_pct": {k: int(round(C["risers"][k]["share"])) for k in ORDER},
        "july_mwh": {k: float("%.2f" % E["july_mwh"][k]) for k in ORDER},
        "requests": {k: int(E["requests"][k]) for k in ORDER},
        "voltage_pct": {k: float("%.2f" % E["voltage_pct"][k]) for k in ORDER},
        "rung_balanced": E["rung_sets"]["balanced"],
        "rung_rotation": [k for k in ORDER if k in E["rung_sets"]["rotation"]],
        "rung_simulated": [k for k in ORDER if k in E["rung_sets"]["simulated"]],
        "constants": {"charger_kw": K["ev"], "cooktop_kw": K["cook"], "limit_pct": int(round(K["limit"] * 100)),
                      "volts": int(K["volt"]), "window": "17:00 to 20:30", "days": "13 to 17 July 2026",
                      "voltage_limits": "216 V to 253 V", "week": "13 to 19 July", "hours_in_week": 168,
                      "years": [2019, 2025, 2026, 2027], "pq_window": "12 to 19 July", "remarking": "March 2025",
                      "exchange_month": "July", "read_date": "1 August", "dates": ["13 July 00:00", "20 July 00:00", "19 July"]},
        "counts": {"risers": len(ORDER)},
    }
    return F


def words_list(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def submission(F, path):
    des = F["designated"]
    sh = F["share_pct"]
    K = F["constants"]
    rot = F["rung_rotation"]
    rot_miss = [k for k in des if k not in rot]
    rot_add = [k for k in rot if k not in des]
    sim = F["rung_simulated"]
    sim_miss = [k for k in des if k not in sim]
    sim_add = [k for k in sim if k not in des]
    lo, hi = min(sh.values()), max(sh.values())
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution.")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    rot_txt = "leaves out %s" % words_list(rot_miss) + (" and adds %s" % words_list(rot_add) if rot_add else "")
    sim_txt = ("leaves out %s" % words_list(sim_miss) if sim_miss else "") + \
              ((" and adds %s" % words_list(sim_add)) if sim_add and sim_miss else ("adds %s" % words_list(sim_add) if sim_add else ""))
    L.append("**Rising mains %s need re-phasing or a larger main before the 2027 chargers and cooktop conversions are connected.** "
             "With each apartment's demand on the phase its supply is wired to, their busiest phases reach %d%% to %d%% of rating against the %d%% line. "
             "Not the balanced allocation, which spreads every single-phase apartment over three phases and puts no main over the line. "
             "Not the installer's rotation by apartment position, which %s. "
             "Not the expected busiest phase over random phasing, which %s." % (words_list(des), lo, hi, K["limit_pct"], rot_txt, sim_txt))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Busiest-phase demand, existing and added, as a share of rating: %s" % ", ".join("%s **%d%%**" % (k, sh[k]) for k in des))
    if F["nearest"]:
        L.append("2. Undesignated main nearest the line: %s at **%d%%**" % (F["nearest"], F["nearest_share_pct"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Mapped each child NMI to its lot (QES_child_meter_register_20261031.xlsx), unit (OC1_register_extract_lots_20260930.xlsx) and rising main by tower and level (MSB_upgrade_2019_rising_main_schedule.pdf), and took each apartment's demand as twice its NEM12 kWh, every register, in the half-hours beginning %s market time on %s (standard section 3)." % (K["window"], K["days"]))
    L.append("2. Sorted each main's single-phase apartments into three groups by how their hourly voltages in QES_PQ_hourly_V_20260712T0000Z-20260720T0000Z.csv move together once the main's own average is taken out, since apartments on one phase sag together whenever any of them draws; the groups separate on every main.")
    L.append("3. Added each charger in OC1_2027_electrification_works_schedule.xlsx at %.1f kW and each cooktop conversion at %.1f kW to its apartment's phase, three-phase supplies split equally (sections 2 and 4)." % (K["charger_kw"], K["cooktop_kw"]))
    L.append("4. Took each phase's highest summed half-hour plus its additions against %d%% of the main's rating at %d V (sections 1 and 5): %s over the line, %s nearest under at %d%%." % (K["limit_pct"], K["volts"], ", ".join("%s %d%%" % (k, sh[k]) for k in des), F["nearest"], F["nearest_share_pct"]))
    L.append("5. July use: each meter's register movement over July in QES_register_reads_2026-07.csv on every register, through QES_meter_exchanges_2026.csv for the meters changed in July and from the meter's own July intervals where its %s read is an estimate (section 7)." % K["read_date"])
    L.append("6. Requests: one per car space in EV_charger_applications_2024-2026.xlsx, B2 and B3 numbers carried through basement_remarking_schedule_March2025.xlsx where written before the re-marking or where the written number is not one of the applicant's own spaces and the re-marked one is, on the main of the apartment the space belongs to (section 8); the visitor bays belong to no apartment.")
    L.append("7. Time outside the limits: each apartment's records in QES_PQ_events_2026-07.json joined into spans across its elements and repeats, clipped to %s to %s market time, over %d hours an apartment (section 6)." % (K["dates"][0], K["dates"][1], K["hours_in_week"]))
    L.append("8. %s need works before connection; every other main stays under the %d%% line." % (words_list(des), K["limit_pct"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### riser_capacity_2027.xlsx")
    L.append("")
    L.append("1. Rising mains needing works, busiest-phase share of rating in whole per cents:")
    for k in des:
        L.append("   - %s: %d%%" % (k, sh[k]))
    L.append("2. Undesignated main nearest the line: %s at %d%%" % (F["nearest"], F["nearest_share_pct"]))
    L.append("3. Apartments' electricity use in July 2026, MWh to two decimals:")
    for k in ORDER:
        L.append("   - %s: %.2f" % (k, F["july_mwh"][k]))
    L.append("4. Charger requests lodged by the apartments' owners:")
    for k in ORDER:
        L.append("   - %s: %d" % (k, F["requests"][k]))
    L.append("5. Share of the apartments' time in the week of 13 to 19 July outside 216 V to 253 V, per cent to two decimals:")
    for k in ORDER:
        L.append("   - %s: %.2f%%" % (k, F["voltage_pct"][k]))
    L.append("")
    L.append("### riser_phase_loading_2027.svg")
    L.append("")
    L.append("1. One bar per rising main of its busiest-phase share of rating, the mains over the line in red with their shares, the %d%% limit dashed across." % K["limit_pct"])
    with open(path, "w") as f:
        f.write("\n".join(L) + "\n")


def write(E, task_dir):
    F = figures(E)
    with open(os.path.join(task_dir, "generator", "figures.json"), "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    submission(F, os.path.join(task_dir, "submission.md"))
    return F
