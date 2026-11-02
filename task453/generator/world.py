"""task453 world: a fictional Canadian province's crematoria, the Crematoria Mercury Fund, its regulation and the
national adult oral health survey. Every constant the generator, the goldens and the checks share lives here."""
import datetime as dt

YEAR = 2026
SEED = 4532026
TZ_NAME = "America/Toronto"   # the province keeps Eastern time (DST)
EXTRACT = dt.date(2027, 2, 26)          # the Vital Statistics extract and the operators' ledger pulls
MEETING = dt.date(2027, 2, 24)

SHARE_REQUIRED = 55.0                   # per cent of the year's cremation mercury released in abated cremators
HG_PER_TOOTH_G = 0.55                   # grams of mercury per tooth restored with amalgam (regulation, schedule)
LEVY_UNABATED = 0.045                   # scheme rules: levy on cremation fee income
LEVY_ABATED = 0.015

PEOPLE = {"secretary": "Heidi Bond", "chair": "Casey Hodges", "vitals": "Alison Pena"}
FUND = "Crematoria Mercury Fund"
AGENCY = "Vital Statistics Agency"
SURVEY_BODY = "Dental Public Health Monitoring Unit"
SURVEY = "National Adult Dentition Survey"

# (fund code, agency facility no., name, operator, cremators, cremations 2026, median-ish age, sd, status, commissioned)
CREMATORIA = [
 ("CM-0417", "F2311", "Halbrook Memorial Crematorium", "City of Halbrook", 3, 3700, 88.1, 8.0, "A", "2021-05-17"),
 ("CM-1182", "F2087", "Fenwick Harbour Crematorium", "Shoreline Memorial Group", 3, 3200, 87.6, 8.0, "A", "2019-11-04"),
 ("CM-0659", "F2440", "Larchmere Cemetery Crematorium", "City of Larchmere", 2, 2800, 88.6, 7.5, "A", "2022-03-28"),
 ("CM-2034", "F2156", "Stannard Bay Crematorium & Chapel", "Shoreline Memorial Group", 2, 2500, 87.6, 8.0, "A", "2020-09-21"),
 ("CM-0738", "F2319", "Ostrander Hill Crematorium", "City of Halbrook", 2, 2200, 87.1, 8.5, "A", "2023-06-12"),
 ("CM-1590", "F2672", "Wexley Regional Crematorium", "Regional District of Wexley", 2, 1600, 86.6, 8.5, "M", "2026-07-03"),
 ("CM-2251", "F2728", "Hollinsbrook Funeral Home Crematory", "Hollinsbrook Funeral Home Ltd.", 1, 1400, 87.6, 8.0, "M", "2026-09-14"),
 ("CM-0896", "F2193", "Corbett Narrows Crematorium", "Corbett Narrows Memorial Society", 3, 2452, 89.0, 7.0, "U", None),
 ("CM-1347", "F2505", "Ashgrove Cremation Centre", "Ashgrove Funeral Co-operative", 2, 1557, 79.0, 7.5, "U", None),
 ("CM-0372", "F2268", "Tallis Creek Crematorium", "Orrinsford Memorial Services", 2, 1339, 72.4, 9.4, "U", None),
 ("CM-1925", "F2581", "Dunmore Falls Memorial Gardens", "Dunmore Falls Cemetery Board", 2, 1120, 69.5, 8.5, "U", None),
 ("CM-2163", "F2702", "Bellhaven Crematorium", "Orrinsford Memorial Services", 1, 855, 81.0, 7.3, "U", None),
 ("CM-0514", "F2134", "Kestrel Lake Crematory", "Lakeland Cremation Ltd.", 1, 950, 82.0, 8.5, "U", None),
 ("CM-1768", "F2397", "Port Alder Crematorium", "Shoreline Memorial Group", 1, 850, 81.0, 8.5, "U", None),
 ("CM-2409", "F2045", "Sorrel Bay Crematorium", "Shoreline Memorial Group", 1, 750, 83.0, 8.5, "U", None),
 ("CM-0283", "F2621", "Wynford Crematorium", "Township of Wynford", 1, 650, 82.0, 8.5, "U", None),
 ("CM-1471", "F2476", "Brackenridge Cremation Services", "Brackenridge Cremation Services Inc.", 1, 550, 84.0, 8.0, "U", None),
 ("CM-2087", "F2358", "Ravensmoor Crematorium", "Lakeland Cremation Ltd.", 1, 450, 82.0, 8.5, "U", None),
 ("CM-0941", "F2219", "Elderton Memorial Crematorium", "Elderton Cemetery Company", 1, 410, 83.0, 8.5, "U", None),
 ("CM-1633", "F2554", "Glenmora Crematorium", "Glenmora Cremation Society", 1, 350, 82.0, 8.5, "U", None),
]
WEXLEY_OLD_FACILITY = "F1984"            # the agency's number for Wexley until the district took it over
WEXLEY_RENUMBERED = dt.date(2026, 3, 2)

# which accounts-receivable export each crematorium's fees sit in
LEDGER_OF = {"City of Halbrook": "halbrook", "Shoreline Memorial Group": "shoreline"}

FILES = {
 "permits": "cremation_permits_returned_2025-12-01_2027-01-31.csv",
 "register": "cmf_member_crematoria_register_2026.xlsx",
 "s1996": "nads_1996_report_tables.pdf",
 "s2006": "nads_2006_report_tables.pdf",
 "s2016": "nads_2016_report_tables.pdf",
 "reg": "crematoria_mercury_regulation_2023_consolidated.pdf",
 "rules": "cmf_scheme_rules_2026.pdf",
 "ar_halbrook": "halbrook_bereavement_ar_2025-12_2027-02.csv",
 "ar_shoreline": "shoreline_memorial_receivables_2025-12_2027-02.xlsx",
 "ar_members": "cmf_fee_returns_independent_crematoria_2025-12_2027-02.csv",
 "cycles": "cremator_controller_cycles_2026.csv",
 "plant": "abatement_plant_logs_2026.parquet",
 "stack": "crematoria_stack_tests_2019-2025.pdf",
 "deaths": "deaths_registered_2026_by_region_age_sex.xlsx",
}
DISTRACTORS = ["stack", "deaths"]
GOLDEN = {"cert": "designation_certificate_2026.pdf", "book": "levy_and_bypass_2026.xlsx"}

# fees (scheme rules: cremation fee income includes these item kinds; urns, keepsakes and disbursements are out)
FEE_ITEMS = [("CREM", "Cremation fee", True), ("CHAP", "Chapel service (40 min)", True), ("XTND", "Extended chapel time",
             True), ("ORGN", "Organist", True), ("WEBC", "Webcast and recording", True), ("MEMB", "Book of remembrance entry",
             True), ("SCAT", "Scattering in the garden", True), ("URN", "Urn", False), ("KEEP", "Keepsake", False),
             ("MREF", "Medical referee fee (disbursement)", False), ("CERT", "Certificate copies", True)]
