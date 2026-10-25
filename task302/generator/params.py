"""Ridgeway Foodmarkets: the parameters every module reads."""
import pandas as pd

SEED_WORLD = 30221
SEED_STOCK = 30222
SEED_ASK = 30223
SEED_DOCS = 30224

ORG = "Ridgeway Foodmarkets"
D0 = pd.Timestamp("2024-07-01")
D1 = pd.Timestamp("2026-06-30")
DAYS = pd.date_range(D0, D1, freq="D")
ND = len(DAYS)
BASE_LO = pd.Timestamp("2025-07-01")          # the twelve months to 30 June 2026
TILL_MIGRATION = pd.Timestamp("2025-03-03")   # the point-of-sale export moves from article numbers to GTINs
FORMULA_DAY_CHANGE = pd.Timestamp("2025-09-01")  # the formula supplier's weekly delivery moves from Tuesday to Wednesday
GO_LIVE = pd.Timestamp("2027-02-01")
NOTE_DATE = pd.Timestamp("2026-11-16")
AS_OF = NOTE_DATE.date()
CUT = 0.5                                     # the share of out-of-stock line-days the system removes

# (store id, town, region, size factor seed offset); two stores closed for refits
TOWNS = [("Palmerston North Central", "Manawatu-Whanganui"), ("Palmerston North Kelvin Grove", "Manawatu-Whanganui"),
         ("Feilding", "Manawatu-Whanganui"), ("Levin", "Horowhenua"), ("Whanganui Central", "Manawatu-Whanganui"),
         ("Whanganui Aramoho", "Manawatu-Whanganui"), ("Marton", "Manawatu-Whanganui"), ("Dannevirke", "Manawatu-Whanganui"),
         ("Masterton", "Wairarapa"), ("Carterton", "Wairarapa"), ("Martinborough", "Wairarapa"), ("Otaki", "Kapiti Coast"),
         ("Waikanae", "Kapiti Coast"), ("Paraparaumu", "Kapiti Coast"), ("Upper Hutt", "Wellington"),
         ("Porirua", "Wellington"), ("Nelson Central", "Nelson Tasman"), ("Nelson Stoke", "Nelson Tasman"),
         ("Richmond", "Nelson Tasman"), ("Motueka", "Nelson Tasman"), ("Blenheim Central", "Marlborough"),
         ("Blenheim Redwoodtown", "Marlborough"), ("Picton", "Marlborough"), ("Takaka", "Nelson Tasman")]
NS = len(TOWNS)
REFITS = {6: ("2025-08-11", "2025-08-15"), 18: ("2026-02-16", "2026-02-20")}   # store index: closed days

CATS = {
    #  units a store-day at a store of size 1, substitute share, defer share, return lag (days), out-of-stock spell
    #  starts a line-day, extra spell days (Poisson mean), seasonal amplitude
    "W": dict(name="Bottled water", base=266.0, r=0.70, f=0.20, lag=(1, 5), rho=0.0127, dur=1.6, seas=0.25,
              route="DC"),
    "F": dict(name="Infant formula", base=15.2, r=0.0, f=0.0, lag=(1, 3), rho=0.0, dur=0.0, seas=0.0, route="direct",
              whole=True, rho_whole=0.0060, whole_dur=(3, 7)),
    "P": dict(name="Dry pet food", base=54.0, r=0.05, f=0.75, lag=(3, 12), rho=0.0072, dur=1.7, seas=0.05,
              route="DC"),
    "G": dict(name="Gluten-free bakery", base=31.0, r=0.30, f=0.10, lag=(1, 3), rho=0.0112, dur=1.3, seas=0.0,
              route="DC"),
}

# (description, share of the category's first-choice demand, substitution group, shelf price FY2026 in NZD)
LINES = {
    "W": [("Kaimai Spring Still Water 1.5L", 0.16, "still", 1.99), ("Kaimai Spring Still Water 600ml 6 Pack", 0.12, "still", 5.49),
          ("Kaimai Spring Still Water 10L", 0.05, "still", 7.99), ("Ridgeway Spring Water 1.5L", 0.20, "still", 1.29),
          ("Ridgeway Spring Water 750ml 12 Pack", 0.07, "still", 8.49), ("Southern Alps Sparkling 1L", 0.10, "sparkling", 2.49),
          ("Southern Alps Sparkling Lemon 1L", 0.06, "sparkling", 2.69), ("Ruahine Artesian Water 1.5L", 0.09, "still", 2.99),
          ("Ruahine Artesian Sports 750ml", 0.06, "still", 2.29), ("Ridgeway Sparkling Water 1.25L", 0.09, "sparkling", 1.49)],
    "F": [("Arataki Infant Formula Stage 1 900g", 0.24, "f", 32.99), ("Arataki Follow-on Formula Stage 2 900g", 0.20, "f", 32.99),
          ("Arataki Toddler Milk Stage 3 900g", 0.16, "f", 27.99), ("Arataki Goat Infant Formula Stage 1 800g", 0.10, "f", 44.99),
          ("Arataki Goat Follow-on Stage 2 800g", 0.08, "f", 44.99), ("Arataki Comfort Formula 800g", 0.08, "f", 36.99),
          ("Arataki Anti-Reflux Formula 800g", 0.07, "f", 38.99), ("Arataki Lactose Free Formula 800g", 0.07, "f", 36.99)],
    "P": [("Huntaway Adult Dog Beef 3kg", 0.14, "dog", 19.99), ("Huntaway Adult Dog Chicken 8kg", 0.10, "dog", 42.99),
          ("Huntaway Puppy 3kg", 0.06, "dog", 24.99), ("Huntaway Senior Dog 3kg", 0.05, "dog", 22.99),
          ("Ridgeway Dog Biscuits 2kg", 0.12, "dog", 9.99), ("Blue Ridge Grain Free Dog 2.5kg", 0.05, "dog", 34.99),
          ("Feline Choice Indoor Cat 1.5kg", 0.13, "cat", 17.99), ("Feline Choice Kitten 1.5kg", 0.06, "cat", 18.99),
          ("Feline Choice Seafood Cat 3kg", 0.09, "cat", 29.99), ("Ridgeway Cat Biscuits 1kg", 0.11, "cat", 6.99),
          ("Blue Ridge Grain Free Cat 1.8kg", 0.04, "cat", 31.99), ("Feline Choice Senior Cat 1.5kg", 0.05, "cat", 18.99)],
    "G": [("Bakehouse GF White Toast Loaf", 0.20, "bread", 7.49), ("Bakehouse GF Seeded Loaf", 0.14, "bread", 7.99),
          ("Bakehouse GF Wraps 6 Pack", 0.10, "other", 6.99), ("Bakehouse GF Burger Buns 4 Pack", 0.09, "other", 6.49),
          ("Bakehouse GF Dinner Rolls 6 Pack", 0.05, "other", 6.99), ("Bakehouse GF Bagels 4 Pack", 0.08, "other", 6.99),
          ("Rangi Baking GF Sourdough", 0.16, "bread", 9.49), ("Rangi Baking GF Fruit Loaf", 0.10, "bread", 8.49),
          ("Rangi Baking GF Pizza Bases 2 Pack", 0.08, "other", 7.49)],
}
PRICE_FY2025 = 0.96       # last year's shelf prices, rounded to the cent ending in 9
DOW = [0.92, 0.88, 0.93, 1.0, 1.12, 1.18, 0.97]      # Monday first
