"""task210 architecture 1: the fixed world of Lindmarsh Water's Marsh and Wolds wastewater network in 2026.

Every constant the simulation, the pack, the golden and the checks share lives here, so a change is made once.
Fourteen sewage pumping stations each have a storm overflow with an event duration monitor; every station runs
two identical pumps duty and standby, alternating duty at each start, so one pump runs at a time. At Gallowfen
the rising main is part-blocked and either pump delivers well under its rated duty; nothing records that."""
import datetime as dt

SEED = 210301
MON_VARIANT = 35                 # the event duration monitors' own draw
COMPANY = "Lindmarsh Water plc"
COMPANY_SHORT = "Lindmarsh Water"
AREA = "Marsh and Wolds"
WRC = "Fleetmouth WRC"
REGULATOR = "Environment Agency"
PEOPLE = {"compliance": "Harriet Kirk", "network": "Maurice Russell"}
YEAR = 2026
EXPORT_DATE = dt.date(2027, 1, 15)           # the compliance team's export for the 2026 return
RETURN_DUE = dt.date(2027, 3, 31)
# UK clock changes in 2026 (01:00 UTC on the last Sunday of March and of October)
BST_START_UTC = dt.datetime(2026, 3, 29, 1, 0, 0)
BST_END_UTC = dt.datetime(2026, 10, 25, 1, 0, 0)

# ---------------------------------------------------------------- stations
# code, name, telemetry label, RTU id, radar zone, role,
# wet well (shape, dims m), floor mAOD, duty stop and start above floor (m), weir above floor (m),
# pump model, rated duty l/s, duty head m, unit the register holds it in, delivered fraction of rated,
# DWF l/s, impervious ha, groundwater infiltration (late-winter rise and year-round base, fractions of delivered),
# permit PFF l/s, flow meter tag
STATIONS = [
    # code       name               telemetry label          rtu      zone role
    dict(code="SPS0407", name="Scarrow Leas", tlabel="SCARROW LEAS SPS", rtu="RTU 30407", zone="R2", role="normal",
         well=("circular", 3.4), floor=-1.42, stop=0.55, start=1.70, weir=2.35,
         model="Flygt NP 3127 HT", rated=41.6, head=11.8, unit="l/s", d=0.98400, dwf=2.9, imperv=5.4, gw=0.0,
         pff=35, meter=None),
    dict(code="SPS0412", name="Gallowfen", tlabel="GALLOWFEN SPS", rtu="RTU 30412", zone="R1", role="K",
         well=("circular", 4.1), floor=-2.18, stop=0.60, start=1.81, weir=2.56,
         model="Flygt NP 3171 MT", rated=85.3, head=15.6, unit="m3/h", d=0.56182, dwf=7.4, imperv=4.3, gw=0.0,
         pff=72, meter=None),
    dict(code="SPS0415", name="Hagworth Wold", tlabel="HAGWORTH WOLD PS", rtu="RTU 30415", zone="R4", role="G",
         well=("rectangular", 3.7, 3.0), floor=18.65, stop=0.50, start=1.65, weir=2.30,
         model="Grundfos SE1.110.200.40", rated=36.8, head=9.4, unit="l/s", d=0.97670, dwf=5.2, imperv=1.0, gw=0.20, gw_base=0.64,
         pff=31, meter=None),
    dict(code="SPS0419", name="Marram End", tlabel="MARRAM END SPS", rtu="RTU 30419", zone="R1", role="F",
         well=("circular", 2.8), floor=-0.96, stop=0.50, start=1.44, weir=2.09,
         model="Flygt NP 3102 MT", rated=19.7, head=8.1, unit="l/s", d=0.96292, dwf=3.3, imperv=10.6, gw=0.0,
         pff=16, meter=None),
    dict(code="SPS0421", name="Cressfleet", tlabel="CRESSFLEET SPS", rtu="RTU 30421", zone="R2", role="normal",
         well=("circular", 3.4), floor=-1.73, stop=0.55, start=1.76, weir=2.46,
         model="Flygt NP 3127 HT", rated=47.2, head=12.4, unit="l/s", d=0.95186, dwf=3.75, imperv=4.7, gw=0.0,
         pff=39, meter=None),
    dict(code="SPS0426", name="Sallowholme", tlabel="SALLOWHOLME SPS", rtu="RTU 30426", zone="R3", role="normal",
         well=("rectangular", 4.0, 3.4), floor=-0.51, stop=0.60, start=1.75, weir=2.50,
         model="KSB Amarex KRT D 150", rated=58.9, head=13.3, unit="m3/h", d=0.96619, dwf=4.4, imperv=5.7, gw=0.0,
         pff=50, meter=None),
    dict(code="SPS0428", name="Northwade Bank", tlabel="NORTHWADE BANK SPS", rtu="RTU 30428", zone="R3", role="metered",
         well=("rectangular", 4.8, 3.9), floor=-2.94, stop=0.65, start=1.93, weir=2.73,
         model="Flygt NP 3202 MT", rated=118.5, head=17.2, unit="l/s", d=0.99419, dwf=12.4, imperv=11.1, gw=0.0,
         pff=101, meter="FT-0428-01"),
    dict(code="SPS0433", name="Brackenings", tlabel="BRACKENINGS SPS", rtu="RTU 30433", zone="R5", role="normal",
         well=("circular", 3.1), floor=-0.22, stop=0.50, start=1.58, weir=2.23,
         model="Grundfos SE1.80.100.75", rated=28.4, head=10.2, unit="l/s", d=1.01949, dwf=4.6, imperv=3.9, gw=0.0,
         pff=23, meter=None),
    dict(code="SPS0437", name="Thornmarsh", tlabel="THORNMARSH SPS", rtu="RTU 30437", zone="R1", role="metered",
         well=("circular", 4.6), floor=-2.47, stop=0.60, start=1.88, weir=2.63,
         model="Flygt NP 3171 MT", rated=86.3, head=14.9, unit="m3/h", d=0.97090, dwf=6.7, imperv=7.8, gw=0.0,
         pff=73, meter="FT-0437-01"),
    dict(code="SPS0440", name="Kettlewade", tlabel="KETTLEWADE SPS", rtu="RTU 30440", zone="R4", role="normal",
         well=("rectangular", 3.4, 2.8), floor=12.08, stop=0.50, start=1.65, weir=2.35,
         model="Xylem Flygt NP 3127 MT", rated=33.5, head=10.7, unit="l/s", d=0.95370, dwf=2.45, imperv=3.6, gw=0.0,
         pff=28, meter=None),
    dict(code="SPS0444", name="Saltwade", tlabel="SALTWADE SPS", rtu="RTU 30444", zone="R5", role="normal",
         well=("circular", 3.8), floor=-1.15, stop=0.55, start=1.76, weir=2.41,
         model="KSB Amarex KRT D 100", rated=52.7, head=12.9, unit="l/s", d=0.98514, dwf=3.6, imperv=5.1, gw=0.0,
         pff=44, meter=None),
    dict(code="SPS0449", name="Reedhaven", tlabel="REEDHAVEN SPS", rtu="RTU 30449", zone="R2", role="normal",
         well=("circular", 2.8), floor=-0.37, stop=0.45, start=1.40, weir=2.05,
         model="Grundfos SE1.80.80.40", rated=22.6, head=8.8, unit="m3/h", d=0.97189, dwf=2.1, imperv=3.0, gw=0.0,
         pff=19, meter=None),
    dict(code="SPS0452", name="Sedgefleet", tlabel="SEDGEFLEET SPS", rtu="RTU 30452", zone="R3", role="metered",
         well=("rectangular", 4.4, 3.7), floor=-2.06, stop=0.60, start=1.88, weir=2.63,
         model="Flygt NP 3153 MT", rated=67.1, head=13.8, unit="l/s", d=0.99523, dwf=4.45, imperv=6.1, gw=0.0,
         pff=56, meter="FT-0452-01"),
    dict(code="SPS0458", name="Swathe Drove", tlabel="SWATHE DROVE SPS", rtu="RTU 30458", zone="R5", role="normal",
         well=("circular", 3.4), floor=-0.88, stop=0.55, start=1.70, weir=2.35,
         model="Flygt NP 3127 HT", rated=44.9, head=11.6, unit="l/s", d=0.95615, dwf=3.9, imperv=4.5, gw=0.0,
         pff=37, meter=None),
]
BY_CODE = {s["code"]: s for s in STATIONS}

# ---------------------------------------------------------------- event duration monitors
# Each overflow's monitor in service at the export is the one the asset register lists. Eleven were replaced
# in 2026 by the HX-40 fleet upgrade, in three crew batches; the old units ran on beside the new ones until the
# crew came back to remove them, and their history stays in the monitoring platform under the old serial.
EDM_CURRENT = {
    "SPS0407": "HX40-26-0318", "SPS0412": "AQ7-18-0609", "SPS0415": "AQ7-18-0614", "SPS0419": "AQ7-17-2228",
    "SPS0421": "HX40-26-0331", "SPS0426": "HX40-26-0335", "SPS0428": "HX40-26-0351", "SPS0433": "HX40-26-0325",
    "SPS0437": "HX40-26-0354", "SPS0440": "HX40-26-0322", "SPS0444": "HX40-26-0340", "SPS0449": "HX40-26-0353",
    "SPS0452": "HX40-26-0320", "SPS0458": "HX40-26-0356",
}
# replaced station -> (old serial, new installed (local date), old removed (local date)); each crew batch took one
# station from each radar zone it worked in
EDM_REPLACED = {
    "SPS0407": ("AQ7-17-2213", dt.date(2026, 3, 3), dt.date(2026, 3, 10)),
    "SPS0440": ("AQ7-19-1150", dt.date(2026, 3, 3), dt.date(2026, 3, 10)),
    "SPS0452": ("AQ7-17-2244", dt.date(2026, 3, 4), dt.date(2026, 3, 10)),
    "SPS0433": ("AQ7-19-1162", dt.date(2026, 3, 4), dt.date(2026, 3, 10)),
    "SPS0421": ("AQ7-17-2236", dt.date(2026, 9, 15), dt.date(2026, 9, 22)),
    "SPS0426": ("AQ7-18-0571", dt.date(2026, 9, 15), dt.date(2026, 9, 22)),
    "SPS0444": ("AQ7-17-2250", dt.date(2026, 9, 16), dt.date(2026, 9, 22)),
    "SPS0428": ("AQ7-17-2261", dt.date(2026, 11, 4), dt.date(2026, 11, 12)),
    "SPS0449": ("AQ7-19-1137", dt.date(2026, 11, 4), dt.date(2026, 11, 12)),
    "SPS0437": ("AQ7-18-0587", dt.date(2026, 11, 5), dt.date(2026, 11, 12)),
    "SPS0458": ("AQ7-18-0593", dt.date(2026, 11, 5), dt.date(2026, 11, 12)),
}



def aq7_commissioned(serial):
    """The AQ-7 fleet went in by crews working through a delivery in serial order (the platform's commissioning
    date for an AQ-7 unit)."""
    return dt.date(2000 + int(serial[4:6]), int(serial[-4:-2]) % 12 + 1, int(serial[-2:]) % 27 + 1)


# ---------------------------------------------------------------- permits
PERMIT = {
    "SPS0407": "EPRWW4407AX", "SPS0412": "EPRWW4412BK", "SPS0415": "EPRWW4415CG", "SPS0419": "EPRWW4419AD",
    "SPS0421": "EPRWW4421BN", "SPS0426": "EPRWW4426CF", "SPS0428": "EPRWW4428AT", "SPS0433": "EPRWW4433BW",
    "SPS0437": "EPRWW4437CQ", "SPS0440": "EPRWW4440AH", "SPS0444": "EPRWW4444BR", "SPS0449": "EPRWW4449CJ",
    "SPS0452": "EPRWW4452AM", "SPS0458": "EPRWW4458BE",
}
RECEIVING = {
    "SPS0407": "Scarrow Drain", "SPS0412": "Gallow Fen Drain", "SPS0415": "Hagworth Beck", "SPS0419": "Marram Haven",
    "SPS0421": "Cress Fleet", "SPS0426": "Sallow Dike", "SPS0428": "North Wade", "SPS0433": "Bracken Drain",
    "SPS0437": "Thorn Fleet", "SPS0440": "Kettle Beck", "SPS0444": "Salt Wade", "SPS0449": "Reed Dike",
    "SPS0452": "Sedge Fleet", "SPS0458": "Swathe Drain",
}
ZONES = ["R1", "R2", "R3", "R4", "R5"]
