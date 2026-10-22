"""Constants for task273: Mirrendale Payroll's year-end readiness review. Every name, date and parameter the world, the
records, the documents and the analysis share lives here."""
import datetime as dt

SEED = 3152
SLA_MS = 800.0                      # the readiness standard's 99th-percentile response time
PCT = 99.0
WARMUP_S = 180.0                    # the test plan's warm-up, excluded from the run of record
MEASURE_S = 600.0                   # the measured ten minutes after it
RUN_S = WARMUP_S + MEASURE_S
TIMEOUT_S = 30.0                    # the test clients' request timeout
FREEZE = dt.date(2026, 12, 4)
ASSEMBLED = dt.datetime(2026, 11, 20, 16, 40, 0)

COMPANY = "Mirrendale Payroll"
REQUESTER = "Theresa Meyers"        # capacity planner
OWNER = "Zachary Mendoza"           # vice president, platform engineering

# service: (garbage collector, pods)
SERVICES = {
    "payroll-core":     ("parallel", 4),
    "tax-forms":        ("parallel", 3),
    "filings":          ("parallel", 5),
    "reports":          ("g1", 4),
    "employees":        ("g1", 4),
    "time-entries":     ("g1", 3),
    "pay-stubs":        ("g1", 5),
    "deductions":       ("g1", 3),
    "banking":          ("parallel", 2),
    "companies":        ("zgc", 3),
    "auth":             ("zgc", 4),
    "search":           ("g1", 3),
    "documents":        ("g1", 4),
    "webhooks":         ("g1", 2),
    "accounting-sync":  ("parallel", 3),
    "state-local":      ("g1", 3),
}

# endpoint id: (method and path, service, kind) ; kind sets the service-time tail
ENDPOINTS = [
    ("EP01", "POST /v2/payroll-runs", "payroll-core", "plain"),
    ("EP02", "GET /v2/payroll-runs/{id}/preview", "payroll-core", "plain"),
    ("EP03", "GET /v2/tax-forms/w2", "tax-forms", "plain"),
    ("EP04", "GET /v2/tax-forms/1099-nec", "tax-forms", "plain"),
    ("EP05", "POST /v2/filings", "filings", "plain"),
    ("EP06", "GET /v2/filings/{id}/status", "filings", "plain"),
    ("EP07", "GET /v2/reports/payroll-register", "reports", "heavy"),
    ("EP08", "GET /v2/reports/tax-liability", "reports", "heavy"),
    ("EP09", "GET /v2/employees", "employees", "plain"),
    ("EP10", "GET /v2/employees/{id}", "employees", "plain"),
    ("EP11", "POST /v2/approvals", "employees", "plain"),
    ("EP12", "POST /v2/time-entries", "time-entries", "plain"),
    ("EP13", "GET /v2/pay-stubs", "pay-stubs", "plain"),
    ("EP14", "GET /v2/deductions", "deductions", "plain"),
    ("EP15", "POST /v2/garnishments", "deductions", "plain"),
    ("EP16", "POST /v2/direct-deposits", "banking", "plain"),
    ("EP17", "GET /v2/companies/{id}", "companies", "plain"),
    ("EP18", "POST /v2/auth/token", "auth", "plain"),
    ("EP19", "GET /v2/search", "search", "heavy"),
    ("EP20", "POST /v2/documents", "documents", "heavy"),
    ("EP21", "POST /v2/webhooks", "webhooks", "plain"),
    ("EP22", "POST /v2/accounting-sync/exports", "accounting-sync", "plain"),
    ("EP23", "POST /v2/state-filings", "state-local", "plain"),
    ("EP24", "GET /v2/local-taxes", "state-local", "plain"),
]
CODES = [e[0] for e in ENDPOINTS]
PATH = {e[0]: e[1] for e in ENDPOINTS}
SERVICE = {e[0]: e[2] for e in ENDPOINTS}
KIND = {e[0]: e[3] for e in ENDPOINTS}

# the pack, as the platform's systems and teams name their exports
FILES = {
    "contents": "contents.txt",
    "standard": "yearend_readiness_standard_2026.pdf",
    "plan": "yearend_peak_loadtest_plan_2026.docx",
    "register": "public_api_endpoint_register.xlsx",
    "jmeter": "loadtest_jmeter_results_2026-11-10_to_12.jtl",
    "k6": "loadtest_k6_results_2026-11-16_to_19.csv",
    "gc": "perf_gc_log_export_2026-11-10_to_19.log",
    "events": "perf_cluster_pod_events_2026-11.csv",
    "edge": "edge_requests_hourly_2026-01.csv",
    "synthetic": "edge_uptime_monitors.yaml",
    "changelog": "developer_portal_changelog_2026.html",
    "employers": "crm_employer_accounts_2026-11-01.csv",
    "subs": "billing_subscription_events_2026.csv",
    "legacy": "legacy_billing_credits_2026-01_to_04.csv",
    "credits": "billing_credits_2026-05-01_to_11-19.json",
    "incidents": "status_page_incidents_2025-12_to_2026-11.xlsx",
    "apm": "apm_traces_perf_2026-11-18.json",
    "slowq": "payroll_db_slow_queries_2026-11.csv",
}
DISTRACTORS = ("apm", "slowq")
DELIVERABLES = ("yearend_readiness_2027.xlsx", "yearend_readiness_2027.png")
EDGE_HOST = "api.mirrendale.com"
PERF_EDGE = "perf-api.mirrendale.internal"
BUILD = "2026.11.2"
REVIEW_YEAR = 2026
WINDOW_FROM = dt.date(2026, 1, 1)          # Ask B: breaches from (Eastern date the incident began)
WINDOW_TO = dt.date(2026, 10, 31)          # to, inclusive
MIGRATION = dt.date(2026, 5, 1)            # billing moved to the new system
CREDITS_TO = dt.date(2026, 11, 19)         # the new system's export runs to this day
