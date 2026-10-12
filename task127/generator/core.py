"""The world's fixed facts: the five hospitals and their trusts, the council's districts and the neighbouring county,
the equipment service's depots, the winter windows, and the fund's terms."""
import datetime as dt

TASK = "task127"
ICB = "NHS Marchshire Integrated Care Board"
COUNCIL = "Marchshire County Council"
FUND_PACKAGES = 1200
AS_OF = dt.date(2026, 10, 12)
EXPORT = dt.datetime(2026, 10, 5, 7, 40)            # the warehouse, equipment and council extracts
SEEN = dt.date(2026, 10, 4)                          # the last day an extract run on 5 October records
REC0, REC1 = dt.date(2024, 12, 1), dt.date(2026, 9, 30)
WINTER0, WINTER1 = dt.date(2025, 12, 1), dt.date(2026, 2, 28)     # last winter, by the date medically optimised
PRIOR0, PRIOR1 = dt.date(2024, 12, 1), dt.date(2025, 2, 28)

TRUSTS = {"RMC": "Marchshire Hospitals NHS Trust", "RSM": "South Marches Healthcare NHS Foundation Trust"}
HOSPITALS = {  # site code: name, short, trust, equipment depot
    "RMC01": dict(name="Royal Marchford Hospital", short="Royal Marchford", trust="RMC", depot="North"),
    "RMC02": dict(name="Wendlebury Hospital", short="Wendlebury", trust="RMC", depot="North"),
    "RSM01": dict(name="Ashby Vale Hospital", short="Ashby Vale", trust="RSM", depot="South"),
    "RSM02": dict(name="Cleeve Park Hospital", short="Cleeve Park", trust="RSM", depot="South"),
    "RSM03": dict(name="Holmford Infirmary", short="Holmford", trust="RSM", depot="South"),
}
SITES = list(HOSPITALS)
DISTRICTS = ["Marchford", "Ashby", "Teme Valley"]      # the council's three districts
NEIGHBOUR = "Severnside"


def in_winter(d):
    return WINTER0 <= d <= WINTER1


def month_name(d):
    return d.strftime("%B")


# delayed patients waiting for a rehabilitation bed or a care home are moved to a sister site of the same trust
TRANSFER_TO = {"RMC01": "RMC02", "RSM01": "RSM02", "RSM03": "RSM02"}
ASK_MONTHS = [(2025, 12), (2026, 1), (2026, 2)]
MONTH_LABEL = {(2025, 12): "December 2025", (2026, 1): "January 2026", (2026, 2): "February 2026"}
