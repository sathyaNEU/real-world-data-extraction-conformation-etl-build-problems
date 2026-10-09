"""Fixed parameters of the task121 world: calendar, organisation, segment volumes and rates.

Every graded figure is computed forward from the records the world module writes; nothing here is a
graded figure. The rates are the mechanism, the tuning module moves records, never these numbers."""
import datetime as dt

SEED = 121

STORE = "Ventania Merch"
STORE_LEGAL = "Ventania Merch, Lda."
STORE_DOMAIN = "loja.ventania.pt"
CLUB = "Clube Desportivo Monteralto"
CLUB_SHORT = "CD Monteralto"
ISSUER_X = "Bankora"      # decoupled app authentication (outcome D)
ISSUER_Y = "Finvo"
OTHER_ISSUERS = ["Caixa Atlântida", "Banco Ponte", "Millenial Crédito", "Novacaixa", "Banco Serrano",
                 "Crédito Ribeirinho"]
PSP = "Tagus Payments"

PEOPLE = {
    "julia": "Júlia Machado", "duarte": "Duarte Cunha", "luciana": "Luciana Castro", "lia": "Lia Neto",
    "cristiano": "Cristiano Soares", "jaime": "Jaime Jesus", "noah": "Noah Coelho", "raquel": "Raquel Pires",
}

# Monday-to-Sunday weeks, Lisbon local. B0 exists only for the five-week baseline reading.
WEEK_STARTS = [dt.datetime(2026, 7, 27), dt.datetime(2026, 8, 3), dt.datetime(2026, 8, 10),
               dt.datetime(2026, 8, 17), dt.datetime(2026, 8, 24), dt.datetime(2026, 8, 31),
               dt.datetime(2026, 9, 7), dt.datetime(2026, 9, 14), dt.datetime(2026, 9, 21)]
WEEK_NAMES = ["B0", "B1", "B2", "B3", "B4", "W1", "W2", "W3", "W4"]
BASE = ["B1", "B2", "B3", "B4"]
REVIEW = ["W1", "W2", "W3", "W4"]
END = dt.datetime(2026, 9, 28)
EXTRACT_DATE = dt.date(2026, 9, 28)

CLUB_LAUNCH = dt.datetime(2026, 8, 31, 9, 0)
COHORT_LIVE = {**{c: dt.datetime(2026, 9, 1, 10, 0) for c in (1, 2, 3, 4)},
               **{c: dt.datetime(2026, 9, 3, 10, 0) for c in (5, 6, 7, 8)},
               **{c: dt.datetime(2026, 9, 8, 10, 0) for c in (9, 10, 11, 12)}}
REBALANCE_AT = dt.datetime(2026, 9, 14, 6, 0)
ISSUER_STOP = {ISSUER_Y: dt.datetime(2026, 9, 3, 0, 0), ISSUER_X: dt.datetime(2026, 9, 7, 0, 0)}
THIRD_KIT_IN_STOCK = dt.datetime(2026, 9, 21, 8, 0)
FINANCE_NET_FROM = dt.datetime(2026, 8, 10, 0, 0)      # rows exported from this release are net of VAT
REEXPORT_AT = dt.datetime(2026, 8, 17, 5, 40)
VAT = 0.23

# basket sessions per week, before the seasonal dip and before tuning
SI_WEEKLY = {"MEMBER": 1600, "CP4": 4000, "XY": 1800, "OTHER": 8600}
NV_WEEKLY = 5600
RG_WEEKLY = 2400
WEEK_VOL = {"B0": 1.012, "B1": 1.031, "B2": 0.987, "B3": 1.018, "B4": 0.964,
            "W1": 0.951, "W2": 0.938, "W3": 0.944, "W4": 0.929}
CLUB_WEEKLY = {"W1": 1290, "W2": 1985, "W3": 2380, "W4": 2600}
CLUB_ACCOUNT_SHARE = {"W1": 0.585, "W2": 0.592, "W3": 0.602, "W4": 0.618}
MEMBER_APP_SHARE = {"W1": 0.47, "W2": 0.735, "W3": 0.885, "W4": 0.992}

MIXED_SHARE = 0.09
MIXED_SHARE_MEMBER = 0.03
MIXED_FACTOR = 0.5
R_SI = 0.046
R_NV = 0.014
R_RG = 0.022
R_P4 = 0.0130
R_P2 = 0.0110
R_P3 = 0.0337

# continuation probabilities: start checkout, pass contact, pass address, pass delivery, pass payment
# the last one is solved from the class's conversion rate
STEPS = ["basket", "contact", "address", "delivery", "payment", "confirmation"]
PROFILE = {
    "SI": (0.21, 0.97, 0.66, 0.74),
    "NV": (0.12, 0.62, 0.58, 0.72),
    "RG": (0.15, 0.75, 0.62, 0.72),
    "P4": (0.21, 0.95, 0.296, 0.74),
    "P2": (0.125, 0.80, 0.50, 0.72),
    "P3": (0.21, 0.97, 0.66, 0.74),
}

N_COHORTS = 12
BOT_SCRAPE_TOKENS = 14
BOT_SCRAPE_SESSIONS = 304
BOT_STUFF_ACCOUNTS = 380
