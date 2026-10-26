"""Drumcondra Provisions Group: the twelve trading units, the fiscal calendar and the posting interfaces.

Nothing here knows about the analysis. The one quantity the analysis cares about, the per-posting rate at
which a unit's postings trip the monitoring ruleset, is set per unit in `ledger.py`, where it is tuned so
each unit's recovered figure lands near the centre of its graded bin.
"""
import datetime as dt

GROUP = "Drumcondra Provisions Group"
TRADE = "cash and carry and delivered wholesale"
CURRENCY = "EUR"
EXTRACT_DATE = dt.date(2026, 7, 3)      # FY26 P9 closed 2026-06-28; P10 to P12 still to run
FY26_LABEL = "FY26"
FY25_LABEL = "FY25"

# The group's financial year runs October to September on a 4-4-5 period calendar.
FY26_START = dt.date(2025, 9, 29)       # FY26 P1 week 1 Monday
FY25_START = dt.date(2024, 9, 30)
PERIOD_WEEKS = (4, 4, 5, 4, 4, 5, 4, 4, 5, 4, 4, 5)
GRADED_PERIODS = 9                      # FY26 P1 to P9 closed before the extract

# code_from is the pre-renumbering code the exception register still carries for part of the window.
# The renumbering took effect at the FY26 half year.
RENUMBER_DATE = dt.date(2026, 3, 30)

UNITS = (
    # code_to, code_from, name, kind, county
    ("DPG-110", "41", "Drumcondra Central Cash and Carry", "branch", "Dublin"),
    ("DPG-120", "42", "Finglas Cash and Carry", "branch", "Dublin"),
    ("DPG-130", "43", "Naas Road Cash and Carry", "branch", "Dublin"),
    ("DPG-210", "51", "Cork Kinsale Road Cash and Carry", "branch", "Cork"),
    ("DPG-220", "52", "Mallow Cash and Carry", "branch", "Cork"),
    ("DPG-310", "61", "Galway Oranmore Cash and Carry", "branch", "Galway"),
    ("DPG-320", "62", "Castlebar Cash and Carry", "branch", "Mayo"),
    ("DPG-410", "71", "Limerick Raheen Cash and Carry", "branch", "Limerick"),
    ("DPG-420", "72", "Waterford Belview Cash and Carry", "branch", "Waterford"),
    ("DPG-510", "81", "National Contracts", "contracts", "Dublin"),
    ("DPG-610", "91", "Drumcondra Bakery", "bakery", "Dublin"),
    ("DPG-900", "99", "Group Services", "services", "Dublin"),
)
BRANCHES = tuple(u[0] for u in UNITS if u[3] == "branch")

# The five routes a posting reaches the ledger by. `voucher` says how the interface groups postings into
# journal entries, which is what the monitoring platform writes its verdict against. Two of the five post
# at the document and three consolidate, which is why one entry can carry 1 posting or 3,200.
INTERFACES = {
    "EPOS": dict(name="Branch counter EPOS", system="Kerridge EPOS",
                 voucher="one voucher per branch per trading day to 2026-03-29, "
                         "one per till per trading day from 2026-03-30"),
    "ROUTE": dict(name="Route accounting", system="Transpoint RA 7",
                  voucher="one voucher per delivery docket on migrated branches, "
                          "one per van per day on the rest"),
    "AP": dict(name="Purchase ledger", system="Drumcondra AP",
               voucher="one voucher per supplier invoice, or one per invoice batch where the supplier "
                       "is on consolidated billing"),
    "PAYROLL": dict(name="Payroll", system="Megabyte Payroll",
                    voucher="one voucher per payroll run"),
    "MANUAL": dict(name="Manual journal", system="Drumcondra GL", voucher="one voucher per journal"),
}

PEOPLE = {
    "audit": ("Ruairi Barnett", "Group Head of Internal Audit"),
    "monitoring": ("Alana Marnan", "Continuous Monitoring Lead"),
    "controller": ("Fergus Rynne", "Group Financial Controller"),
    "route": ("Myles Connaughton", "Route Accounting Manager"),
}

ACCOUNTS = (
    ("4100", "Sales, foodservice", "revenue"),
    ("4120", "Sales, counter", "revenue"),
    ("4900", "Sales control", "control"),
    ("5100", "Cost of sales, ambient", "cost"),
    ("5120", "Cost of sales, chilled", "cost"),
    ("6100", "Distribution, fuel", "cost"),
    ("6110", "Distribution, agency drivers", "cost"),
    ("6300", "Depot overheads", "cost"),
    ("7200", "Supplier accruals", "control"),
    ("7210", "Purchase ledger control", "control"),
    ("8100", "Intercompany, group services", "control"),
    ("9900", "Suspense", "control"),
)


def periods(fy_start, n=12):
    """(period_no, start_date, end_date) on the 4-4-5 calendar."""
    out = []
    d = fy_start
    for i, weeks in enumerate(PERIOD_WEEKS[:n], start=1):
        end = d + dt.timedelta(days=7 * weeks - 1)
        out.append((i, d, end))
        d = end + dt.timedelta(days=1)
    return out


FY26_PERIODS = periods(FY26_START)
FY25_PERIODS = periods(FY25_START)


def period_of(day, fy_periods):
    for n, a, b in fy_periods:
        if a <= day <= b:
            return n
    return None


def unit_code_at(code_to, day):
    """The code the ledger carried for this unit on that day."""
    row = next(u for u in UNITS if u[0] == code_to)
    return code_to if day >= RENUMBER_DATE else row[1]


def unit_name(code_to):
    return next(u[2] for u in UNITS if u[0] == code_to)


def unit_kind(code_to):
    return next(u[3] for u in UNITS if u[0] == code_to)


_BY_CODE = {u[0]: u[0] for u in UNITS}
_BY_CODE.update({u[1]: u[0] for u in UNITS})


def resolve_unit(code):
    """The current unit code, whether given the current code or the one in force before the renumbering."""
    return _BY_CODE[str(code).strip()]
