"""The fixed world: Ridgeline Power Cooperative, a generation and transmission cooperative in an unnamed inland U.S.
state, its combined-cycle units (each a gas turbine with a heat-recovery steam generator and selective catalytic
reduction), its simple-cycle peakers and its one coal unit, the 2026 ozone season, the continuous emissions monitors
whose analyzers drop out mostly in the hours after a start, and the plants' control-system load logs. Every other
module reads its parameters from here."""
import datetime as dt

COOP = "Ridgeline Power Cooperative"
DEPT = "Environmental Services"
PEOPLE = {"engineer": ("Tamara Gill", "Senior Environmental Compliance Engineer"),
          "manager": ("Martin Estrada", "Manager, Generation Engineering")}
SEED = 474
YEAR = 2026
SEASON = (dt.date(2026, 5, 1), dt.date(2026, 9, 30))       # the ozone season, both days included
TARGET = 0.170                 # lb of NOx per gross MWh over the ozone season; at or above designates
GUIDELINE_DATE = "12 January 2026"
MEMO_DATE = "9 November 2026"
BOARD_DATE = "17 December 2026"

PLANTS = {"Cutler Bend": ("CB", "America/Chicago"), "Ashfork": ("AF", "America/Chicago"),
          "Dunmore Flats": ("DF", "America/Chicago"), "Sable Ridge": ("SR", "America/Chicago")}

# combined-cycle units: plant, unit, capacity MW, starts a week in season, steady NOx lb per MWh at full load, NOx in
# the first hours after a start (lb, spread over hours 1 to 3), chance the analyzer is out in hours 1 to 3 after a
# start, chance it is out in any other operating hour, typical run length (hours)
CC = {
    "CB-1": ("Cutler Bend", 1, 238, 5.6, .031, 520, .66, .020, 16),
    "CB-2": ("Cutler Bend", 2, 241, 2.1, .034, 505, .09, .024, 40),
    "AF-1": ("Ashfork", 1, 226, 4.4, .038, 560, .62, .018, 20),
    "AF-2": ("Ashfork", 2, 229, 4.9, .033, 470, .08, .022, 18),
    "DF-1": ("Dunmore Flats", 1, 262, 3.1, .029, 610, .68, .019, 28),
    "DF-2": ("Dunmore Flats", 2, 258, 1.4, .036, 540, .12, .026, 70),
    "DF-3": ("Dunmore Flats", 3, 255, 5.2, .032, 495, .67, .021, 17),
    "SR-1": ("Sable Ridge", 1, 247, 3.6, .035, 530, .06, .020, 24),
    "SR-2": ("Sable Ridge", 2, 251, 4.0, .030, 575, .64, .023, 22),
}
# each unit's uncontrolled NOx (lb per MMBtu, SCR out of service), set by its combustors
UNC = {"CB-1": .118, "CB-2": .121, "AF-1": .112, "AF-2": .109, "DF-1": .036, "DF-2": .035, "DF-3": .034, "SR-1": .037,
       "SR-2": .036}
# plant instrument air losses in the 2026 ozone season: (number, typical hours)
AIR = {"Cutler Bend": (12, 9.0), "Ashfork": (16, 10.0), "Dunmore Flats": (2, 4.0), "Sable Ridge": (1, 4.0)}
# each delivery point's transporter, whose fuel retention (a share of the Daily Index, reset monthly by its tariff)
# every point on it pays, and the point's transportation rate ($/Dth)
PIPELINE = {"Cutler Bend": "A", "Dunmore Flats": "A", "Sable Ridge": "A", "Ashfork": "B", "Holt Creek": "B"}
FUEL_RETENTION = {"A": {5: .011, 6: .013, 7: .016, 8: .018, 9: .014},
                  "B": {5: .024, 6: .028, 7: .032, 8: .035, 9: .029}}
TRANSPORT = {"Cutler Bend": .2186, "Ashfork": .1539, "Dunmore Flats": .2248, "Sable Ridge": .1929, "Holt Creek": .1386}
# other monitored units, outside the program: simple-cycle peakers and the coal unit
OTHER = {
    "AF-CT3": ("Ashfork", "simple cycle", 88), "AF-CT4": ("Ashfork", "simple cycle", 86),
    "SR-CT3": ("Sable Ridge", "simple cycle", 92), "HC-4": ("Holt Creek", "coal steam", 412),
}
# the golden's 2026 ozone-season NOx per MWh (tune.py scales each unit's start NOx until the cut pack lands here)
DESIRED = {"CB-1": .268, "CB-2": .186, "AF-1": .187, "AF-2": .251, "DF-1": .186, "DF-2": .099, "DF-3": .189,
           "SR-1": .187, "SR-2": .151}
ADJ = {'AF-1': 0.47015, 'AF-2': 0.87903, 'CB-1': 0.7154, 'CB-2': 1.21965, 'DF-1': 1.37014, 'DF-2': 0.98317, 'DF-3': 0.85185, 'SR-1': 1.04345, 'SR-2': 0.80133}

FILES = {
    "dahs": "dahs_hourly_export_2026.csv",
    "notes": "dahs_export_field_notes.txt",
    "units": "generating_unit_register_2026.xlsx",
    "tickets": "cems_maintenance_tickets_2026.csv",
    "guidelines": "scr_upgrade_program_rules_2027.pdf",
    "invoices": "gas_supply_daily_invoices_2026.csv",
    "terms": "gas_supply_agreement_excerpt.pdf",
    "events": "gads_event_report_2026.csv",
    "ozone": "ambient_ozone_daily_2026.csv",
    "allowances": "nox_allowance_holdings_2026.xlsx",
}
GOLDEN = {"workbook": "cc_unit_nox_inventory_2026.xlsx", "memo": "scr_upgrade_designations_2027.pdf"}
