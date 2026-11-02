"""task467, architecture 2: the world's constants. Wrenfield & Holt (an online fashion and homeware retailer), its
Cotterby returns centre, Calvermoor Trading Standards and Tarnwell are invented; the 14-day refund period follows
the Consumer Contracts (Information, Cancellation and Additional Charges) Regulations 2013, regulation 34."""
import datetime as dt

SEED = 467
TZ_NAME = "Europe/London"
AS_OF = "2026-10-30"                 # the day the extracts were pulled
RETURN_DUE = dt.date(2026, 11, 30)   # the written assurance's return date
ASSURANCE_SIGNED = dt.date(2026, 10, 9)

RETAILER = "Wrenfield & Holt"
RETAILER_LTD = "Wrenfield & Holt Ltd"
CENTRE = "Cotterby returns centre"
TS = "Calvermoor Trading Standards"
COUNCIL = "Calvermoor County Council"
FUND = "the Meridale Consumer Trust"
LABEL_CARRIER = "Tarnwell"

PEOPLE = {"compliance": "Howard Jones", "centre": "Steven Jennings", "officer": "Neil Fisher"}
ROLES = {"compliance": "Head of Regulatory Compliance", "centre": "Returns Centre Operations Manager",
         "officer": "Senior Trading Standards Officer"}

# the window the return covers and the payment it carries
WINDOW_MONTHS = [(2026, m) for m in range(1, 7)]
LATE_DAY = 15            # a refund made on day 15 or later (the delivery day is day 0) is made late
PAYMENT_PER_LATE = 15    # pounds into the goodwill fund for each refund made late
COMMIT_SHARE = 0.95      # at least 95 per cent of each month's refunds made by day 14
EUR_RATE = 0.86          # the finance team's 2026 budget rate, pounds per euro
USD_RATE = 0.79

# the record: goods-in from 1 December 2024 (the hall's content on 1 January 2025 is on file), processing and refunds
# from then, everything to the day before the extracts were pulled
START = dt.date(2024, 12, 2)
END = dt.date(2026, 10, 28)
LABELS_END = dt.date(2025, 12, 31)   # the last day a prepaid label was issued

BANK_HOLIDAYS = {dt.date(*d) for d in [
    (2024, 12, 25), (2024, 12, 26), (2025, 1, 1), (2025, 4, 18), (2025, 4, 21), (2025, 5, 5), (2025, 5, 26),
    (2025, 8, 25), (2025, 12, 25), (2025, 12, 26), (2026, 1, 1), (2026, 4, 3), (2026, 4, 6), (2026, 5, 4),
    (2026, 5, 25), (2026, 8, 31)]}

CARRIERS_2026 = [("Ambrell Post", 0.58), ("Tarnwell", 0.17), ("Kestrix", 0.16), ("Vellum Parcels", 0.09)]

FILES = {
    "goods2025": "cotterby_goods_in_2025.csv",
    "goods2026": "cotterby_goods_in_2026.parquet",
    "processing": "cotterby_returns_processing_2025_2026.csv",
    "refunds": "wh_refund_ledger_2025_2026.parquet",
    "orders": "wh_orders_returning_customers.parquet",
    "assurance": "calvermoor_written_assurance_oct2026.pdf",
    "review": "cotterby_returns_review_2025.pdf",
    "vouchers": "wh_goodwill_vouchers_2026.csv",
    "redemptions": "wh_voucher_redemptions_2026.csv",
    "cases": "wh_customer_cases_2026.csv",
    "dailyops": "cotterby_daily_operations_2025_2026.xlsx",
    "rota": "cotterby_shift_rota_2026.csv",
}
DISTRACTORS = ["dailyops", "rota", "review"]
GOLDEN = {"return": "goodwill_fund_return_h1_2026.csv", "note": "refund_timeliness_note.pdf"}


def local_tz():
    from zoneinfo import ZoneInfo
    return ZoneInfo(TZ_NAME)


def days():
    d, out = START, []
    while d <= END:
        out.append(d)
        d += dt.timedelta(days=1)
    return out
