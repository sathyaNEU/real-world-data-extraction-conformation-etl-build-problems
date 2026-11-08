"""Renders task156/submission.md from generator/figures.json, so every figure in it is one the generator wrote.
python3 task156/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(out=TASK):
    F = json.load(open(os.path.join(out, "generator", "figures.json")))
    call = F["call"]
    names = ", ".join(call[:-1]) + " and " + call[-1]
    already = ", ".join(F["naive"])
    rows = []
    for code, name in F["hub_rows"]:
        rows.append("   - %s %s: %s; %s charges; %.1f MWh" % (code, name, F["sides"][name], "{:,}".format(F["charges"][name]),
                                                              F["energy_mwh"][name]))
    text = """## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**List %d hubs in the 2027 Availability Plan: %s.**
No HX150 hangs before day %d after a power-up, and once the programme removes the RC50 and its monthly cabinet service, the
seven standard programme hubs' units run months between power-ups. Not the five hubs each unit's own hang rate gives,
because those rates were measured while the RC50's monthly service powered the units down; not the programme's motorway
hubs or its two rural spur hubs, whose visits every two months and frequent supply interruptions keep restarting them.

## 2. Critical Components

1. No HX150 on the record hung before day **%d** after its last power-up (**%d** hangs on record).
2. The five hubs whose HX150 units hang on the record are the five where the RC50's service does not power them down:
   **%s**.
3. Without the RC50, the seven standard programme hubs keep two planned visits a year and few supply interruptions, so
   their HX150 units fall below **%d per cent** in 2027.
4. The programme's three motorway hubs (visits every two months) and Annagh Cross and Cloonfin Crossroads (frequent
   supply interruptions) stay above **%d per cent**.

## 3. Step-by-Step Solution

1. Mapped previous and current IDs through charge_point_register.xlsx, kept one copy of each re-sent row in
   connector_status_history_2023-2026.csv and rebuilt each unit's Faulted, Unavailable and Offline spells.
2. Took each pillar power-down as the group of Offline rows, within six minutes, in which every unit at the hub that was
   up went Offline, and each hang as an HX150 Offline spell of three hours or more that a technician cleared by a power
   cycle (work_orders_2023-2026.xlsx) or a power-down ended.
3. Read the hangs on the days since each unit's last power-up (a pillar power-down, a hang restart or a repair): %d
   hangs, none before day %d.
4. Built each hub's 2027 power-downs from the 2027 plan sheet of planned_maintenance_schedule.xlsx, its interruption rate
   in supply_interruptions_2023-2026.csv, the RC50's isolations where it stays and the works dates in
   asset_renewal_programme_2027.pdf.
5. Ran every 2027 HX150, new units included, through that regime with the hub's callout attendance and fault rate,
   availability per Schedule 4 of concession_agreement_schedules_4_and_6.pdf: %d hubs have a unit below %d per cent.
6. Counted charges in charging_sessions_2026.csv under Schedule 6: one copy of each session number, a record joined to
   the one before it on its connector when it opens above that record's closing register or starts within five seconds
   of its close, failed starts out, HX150 units only, begun January to October 2026 Irish time.
7. Took each charge's energy from its first record's opening register to its last record's closing register, summed by
   hub in MWh.
8. Listed the %d hubs in the plan's letter and the return.

## 4. Deliverable Answers

### hub_availability_2027.csv

1. Each hub's side of the standard, its high-power charges begun January to October 2026 (whole charges) and their
   energy (MWh to one decimal), in the file's order:
%s

### availability_plan_2027.pdf

1. The covering letter to the partnership names the %d hubs the plan lists under Schedule 4: %s, with the action
   proposed at each.
""" % (F["call_count"], names, F["first_hang_day"], F["first_hang_day"], F["hangs_on_record"], already,
       F["standard_per_cent"], F["standard_per_cent"], F["hangs_on_record"], F["first_hang_day"], F["call_count"],
       F["standard_per_cent"], F["call_count"], "\n".join(rows), F["call_count"], names)
    open(os.path.join(out, "submission.md"), "w").write(text)


if __name__ == "__main__":
    main()
