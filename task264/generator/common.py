"""Constants for task264: a grocery market-data firm's weekly price index built from its partner chains' scanner
feeds, the index committee choosing which food categories the 2027 index publishes on their own, and the files the
firm's price index team keeps beside the feeds."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

SEED = 2641017


def rng(*keys):
    """One independent stream per named purpose, so a change in one part of the world moves no other part."""
    h = hashlib.sha256(("%d/" % SEED + "/".join(str(k) for k in keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


# ---------------------------------------------------------------------------------------------- the firm
FIRM = "Delvett Retail Data"
FIRM_SHORT = "Delvett"
INDEX = "Delvett Grocery Price Index"
PEOPLE = dict(head="Christy Chambers", feeds="Manuel Zamora")

# ---------------------------------------------------------------------------------------------- the calendar
W = 52
WEEK1 = dt.date(2025, 12, 6)                 # retail year 2026 week 1 ends Saturday 6 December 2025
WEEKS = [WEEK1 + dt.timedelta(days=7 * t) for t in range(W)]
LAST = WEEKS[-1]                             # Saturday 28 November 2026
assert LAST == dt.date(2026, 11, 28)
PULL = dt.date(2026, 12, 4)                  # the movement and totals tables as loaded
EXPORT = dt.date(2026, 12, 7)                # the files the team keeps, as sent
MEETING = dt.date(2026, 12, 9)               # the index committee adopts the 2027 structure
JULY_T = 30                                  # the July chain's first week (ends 4 July 2026)
UPGRADE_T = 35                               # a convenience chain's till upgrade, from the week ending 8 August 2026
assert WEEKS[JULY_T] == dt.date(2026, 7, 4) and WEEKS[UPGRADE_T] == dt.date(2026, 8, 8)

FORMATS = ["supermarket", "neighbourhood", "convenience", "online"]
FORMAT_LABEL = {"supermarket": "Supermarket", "neighbourhood": "Neighbourhood", "convenience": "Convenience",
                "online": "Online"}
# the committee's 2026 format weights (shares of household grocery spending by format, per cent)
FORMAT_WEIGHTS = {"supermarket": 59.6, "neighbourhood": 16.3, "convenience": 7.1, "online": 17.0}
assert abs(sum(FORMAT_WEIGHTS.values()) - 100.0) < 1e-9
TOLERANCE = 1.5                              # points, each format's change against the national change

# ---------------------------------------------------------------------------------------------- the chains
# code, banner, format, price level, panel stores, store size range, first week, traffic trend over the window,
# promotion rate a week, own promotion code, markdown code (None: no store markdowns)
CHAINS = [
    ("S1", "Haskard Fresh", "supermarket", 1.12, 4, (0.85, 1.30), 0, -0.22, 0.085, "SPECIAL", None),
    ("S2", "Brevane Supermarkets", "supermarket", 1.00, 4, (0.80, 1.25), 0, 0.00, 0.095, "PROMO", None),
    ("S3", "Fremett Foods", "supermarket", 0.99, 3, (0.75, 1.10), 0, 0.00, 0.080, "TPR", None),
    ("S4", "Pravard Discount", "supermarket", 0.92, 4, (0.85, 1.30), 0, 0.22, 0.070, "SALE", None),
    ("S5", "Gorvery Warehouse", "supermarket", 0.87, 3, (0.95, 1.30), JULY_T, 0.00, 0.050, "OFFER", None),
    ("N1", "Lumbane Local", "neighbourhood", 1.04, 4, (0.30, 0.45), 0, 0.00, 0.080, "P", "RC"),
    ("N2", "Ruskett Grocers", "neighbourhood", 0.99, 3, (0.30, 0.45), 0, 0.00, 0.075, "PROMO", "MD"),
    ("N3", "Skovard Local", "neighbourhood", 1.01, 4, (0.30, 0.45), 0, 0.00, 0.080, "SPC", "RC"),
    ("C1", "Quorrix", "convenience", 1.18, 14, (0.050, 0.080), 0, 0.00, 0.060, "PR", "RC"),
    ("C2", "Treskola", "convenience", 1.15, 16, (0.050, 0.080), 0, 0.00, 0.085, "PC", "RC"),
    ("C3", "Jorvery Stop", "convenience", 1.21, 13, (0.050, 0.080), 0, 0.00, 0.055, "DEAL", "CLR"),
    ("O1", "Wiskane Online", "online", 1.12, 2, (1.00, 1.40), 0, 0.00, 0.090, "SALE", None),
    ("O2", "Pembard Direct", "online", 1.00, 3, (1.00, 1.40), 0, 0.00, 0.100, "PROMO", None),
    ("O3", "Keskary", "online", 0.92, 2, (1.00, 1.40), 0, 0.00, 0.080, "SPECIAL", None),
]
CH = {c[0]: dict(code=c[0], banner=c[1], fmt=c[2], lvl=c[3], n=c[4], size=c[5], start=c[6], trend=c[7],
                 promo_rate=c[8], promo_code=c[9], md_code=c[10]) for c in CHAINS}
CHAIN_CODES = [c[0] for c in CHAINS]
UPGRADE_CHAIN = "C2"        # its till upgrade: price cuts coded TPR from the upgrade week, PC kept for price checks
SUNDAY_CHAIN = "C1"         # its trading week runs Monday to Sunday
ZERO_DROP_CHAIN = "N1"      # its tills send item codes without the GTIN-14 leading zero
RESUB_CHAIN, RESUB_WEEKS = "N2", (17, 18, 19, 20)          # a movement block resubmitted (weeks ending 4 to 25 April)
RESEND_CHAIN, RESEND_WEEKS = "S1", (13, 14, 15, 16, 17, 18)  # a totals resend the firm's validation rejected
VENDOR_CHAINS = ("S3", "N2", "C3", "O3")                    # one till vendor's weekly store sales export
BACKFILL_FROM = 4           # the July chain's onboarding totals start at the week ending 3 January 2026

# ---------------------------------------------------------------------------------------------- categories and lines
# per category: fast-line price range, slow-line price range, purchase weight in kg for lines sold by weight, and
# sixteen lines (description, sold by weight). The first three lines are the category's big sellers.
CATS = ["Bread and bakery", "Breakfast cereals", "Milk", "Cheese", "Yoghurt and desserts", "Butter and spreads",
        "Eggs", "Fresh meat and poultry", "Deli and cooked meats", "Seafood", "Fresh fruit", "Fresh vegetables",
        "Frozen foods", "Biscuits", "Confectionery", "Chips and snacks", "Soft drinks", "Coffee and tea"]
CAT_CODE = {c: "F%02d" % (i + 1) for i, c in enumerate(CATS)}
KG = True
LINES = {
    "Bread and bakery": ((2.6, 4.2), (5.4, 9.0), 0.0, [
        ("White sandwich loaf 650g", 0), ("Wholemeal sandwich loaf 650g", 0), ("Soft white rolls 6 pack", 0),
        ("Sourdough loaf 750g", 0), ("Gluten free white loaf 500g", 0), ("Light rye loaf 680g", 0),
        ("Spelt and honey loaf 600g", 0), ("Butter croissants 4 pack", 0), ("Brioche loaf 500g", 0),
        ("Raisin toast loaf 520g", 0), ("English muffins 6 pack", 0), ("Crumpets 6 pack", 0),
        ("Plain bagels 4 pack", 0), ("Wholegrain wraps 8 pack", 0), ("Lebanese bread 5 pack", 0),
        ("Apple danishes 4 pack", 0)]),
    "Breakfast cereals": ((3.6, 6.0), (6.5, 11.5), 0.0, [
        ("Wheat biscuit cereal 750g", 0), ("Corn flakes 500g", 0), ("Rolled oats 900g", 0),
        ("Toasted muesli 750g", 0), ("Bircher muesli 500g", 0), ("Granola clusters 450g", 0),
        ("Protein granola 400g", 0), ("Bran flakes 500g", 0), ("Puffed rice cereal 410g", 0),
        ("Honey puffs 450g", 0), ("Fruit and nut muesli 1kg", 0), ("Quick oats sachets 10 pack", 0),
        ("Steel cut oats 750g", 0), ("Coconut granola 500g", 0), ("Multigrain flakes 620g", 0),
        ("Ancient grain porridge 500g", 0)]),
    "Milk": ((1.9, 3.6), (3.8, 6.6), 0.0, [
        ("Full cream milk 2L", 0), ("Light milk 2L", 0), ("Full cream milk 1L", 0),
        ("Lactose free milk 2L", 0), ("Organic full cream milk 1.5L", 0), ("Unhomogenised milk 2L", 0),
        ("Skim milk 2L", 0), ("Barista milk 2L", 0), ("Almond milk 1L", 0), ("Oat milk 1L", 0),
        ("Soy milk 1L", 0), ("Long life full cream milk 1L", 0), ("Chocolate milk 600mL", 0),
        ("Iced coffee milk 600mL", 0), ("Jersey milk 1.5L", 0), ("Goat milk 1L", 0)]),
    "Cheese": ((7.5, 11.0), (6.5, 13.0), 0.0, [
        ("Tasty cheddar block 500g", 0), ("Tasty cheddar slices 500g", 0), ("Grated mozzarella 500g", 0),
        ("Brie 200g", 0), ("Camembert 125g", 0), ("Vintage cheddar 250g", 0), ("Parmesan wedge 250g", 0),
        ("Fetta 200g", 0), ("Haloumi 180g", 0), ("Blue vein 150g", 0), ("Cream cheese block 250g", 0),
        ("Ricotta 375g", 0), ("Shaved parmesan 125g", 0), ("Gouda wedge 200g", 0), ("Smoked cheddar 200g", 0),
        ("Swiss style slices 200g", 0)]),
    "Yoghurt and desserts": ((4.5, 7.0), (4.6, 9.0), 0.0, [
        ("Greek style yoghurt 1kg", 0), ("Natural yoghurt 1kg", 0), ("Vanilla yoghurt 1kg", 0),
        ("Strawberry yoghurt 4 pack", 0), ("Kids yoghurt pouches 6 pack", 0), ("Coconut yoghurt 500g", 0),
        ("Skyr natural 450g", 0), ("Chocolate custard 1kg", 0), ("Vanilla custard 1kg", 0),
        ("Creamed rice 4 pack", 0), ("Chocolate mousse 4 pack", 0), ("Creme caramel 2 pack", 0),
        ("Protein yoghurt 4 pack", 0), ("Lactose free yoghurt 500g", 0), ("Organic natural yoghurt 500g", 0),
        ("Fruit jelly cups 4 pack", 0)]),
    "Butter and spreads": ((3.8, 6.5), (5.0, 11.0), 0.0, [
        ("Salted butter 250g", 0), ("Spreadable butter 375g", 0), ("Margarine spread 500g", 0),
        ("Unsalted butter 250g", 0), ("Cultured butter 200g", 0), ("Organic butter 250g", 0),
        ("Olive oil spread 500g", 0), ("Dairy free spread 500g", 0), ("Peanut butter smooth 375g", 0),
        ("Peanut butter crunchy 375g", 0), ("Almond spread 250g", 0), ("Hazelnut spread 400g", 0),
        ("Strawberry jam 500g", 0), ("Honey 500g", 0), ("Yeast extract spread 380g", 0), ("Marmalade 500g", 0)]),
    "Eggs": ((5.5, 8.0), (6.5, 14.0), 0.0, [
        ("Cage eggs 12 pack 700g", 0), ("Free range eggs 12 pack 700g", 0), ("Barn laid eggs 12 pack 700g", 0),
        ("Free range eggs 6 pack", 0), ("Organic eggs 12 pack 700g", 0), ("Pasture raised eggs 12 pack", 0),
        ("Jumbo free range eggs 12 pack 800g", 0), ("Free range eggs 18 pack", 0), ("Omega-3 eggs 12 pack", 0),
        ("Duck eggs 6 pack", 0), ("Quail eggs 12 pack", 0), ("Liquid egg whites 500mL", 0),
        ("Free range eggs 30 tray", 0), ("Cage eggs 30 tray", 0), ("Organic eggs 6 pack", 0),
        ("Pullet eggs 12 pack", 0)]),
    "Fresh meat and poultry": ((9.0, 16.0), (14.0, 44.0), 0.7, [
        ("Beef mince 500g", 0), ("Chicken breast fillets per kg", KG), ("Chicken thigh fillets per kg", KG),
        ("Scotch fillet steak per kg", KG), ("Lamb loin chops per kg", KG), ("Pork belly per kg", KG),
        ("Lamb leg roast per kg", KG), ("Beef rump steak per kg", KG), ("Whole chicken per kg", KG),
        ("Pork sausages 500g", 0), ("Beef sausages 500g", 0), ("Lamb mince 500g", 0),
        ("Chicken drumsticks per kg", KG), ("Beef chuck steak per kg", KG), ("Pork loin chops per kg", KG),
        ("Veal schnitzel per kg", KG)]),
    "Deli and cooked meats": ((6.0, 22.0), (14.0, 64.0), 0.25, [
        ("Middle bacon 250g", 0), ("Shaved leg ham per kg", KG), ("Sliced chicken breast per kg", KG),
        ("Prosciutto per kg", KG), ("Hot salami per kg", KG), ("Mild salami per kg", KG), ("Pastrami per kg", KG),
        ("Smoked turkey per kg", KG), ("Mortadella per kg", KG), ("Kabana 250g", 0), ("Roast chicken each", 0),
        ("Leg ham off the bone per kg", KG), ("Silverside per kg", KG), ("Chorizo 250g", 0),
        ("Pancetta per kg", KG), ("Shaved beef per kg", KG)]),
    "Seafood": ((2.2, 34.0), (9.0, 52.0), 0.5, [
        ("Canned tuna 95g", 0), ("Barramundi fillets per kg", KG), ("Atlantic salmon fillets per kg", KG),
        ("Cooked king prawns per kg", KG), ("Raw prawns per kg", KG), ("Smoked salmon 100g", 0),
        ("Oysters dozen", 0), ("Snapper fillets per kg", KG), ("Flathead fillets per kg", KG),
        ("Calamari rings per kg", KG), ("Mussels 1kg pot", 0), ("Canned salmon 210g", 0), ("Scallops per kg", KG),
        ("Ling fillets per kg", KG), ("Blue swimmer crab per kg", KG), ("Tuna steaks per kg", KG)]),
    "Fresh fruit": ((3.0, 5.6), (3.6, 13.0), 0.9, [
        ("Bananas per kg", KG), ("Royal Gala apples 1kg bag", 0), ("Navel oranges 3kg bag", 0),
        ("Strawberries 250g punnet", 0), ("Blueberries 125g punnet", 0), ("Raspberries 125g punnet", 0),
        ("Cherries per kg", KG), ("Mangoes each", 0), ("Avocados each", 0), ("Kiwifruit per kg", KG),
        ("Pink Lady apples per kg", KG), ("Red grapes per kg", KG), ("Mandarins per kg", KG),
        ("Nectarines per kg", KG), ("Packham pears per kg", KG), ("Pineapple each", 0)]),
    "Fresh vegetables": ((2.0, 4.6), (2.6, 10.0), 0.8, [
        ("Brushed potatoes 2kg bag", 0), ("Carrots 1kg bag", 0), ("Brown onions 1kg bag", 0),
        ("Broccoli per kg", KG), ("Truss tomatoes per kg", KG), ("Continental cucumber each", 0),
        ("Iceberg lettuce each", 0), ("Baby spinach 120g", 0), ("Cup mushrooms per kg", KG),
        ("Red capsicum per kg", KG), ("Sweet potato per kg", KG), ("Zucchini per kg", KG),
        ("Asparagus bunch", 0), ("Green beans per kg", KG), ("Cauliflower each", 0), ("Baby cos lettuce 2 pack", 0)]),
    "Frozen foods": ((2.8, 5.0), (5.0, 12.0), 0.0, [
        ("Frozen peas 1kg", 0), ("Frozen chips 1kg", 0), ("Frozen mixed vegetables 1kg", 0),
        ("Frozen pizza 400g", 0), ("Fish fingers 425g", 0), ("Vanilla ice cream 2L", 0),
        ("Premium ice cream tub 1L", 0), ("Frozen dumplings 600g", 0), ("Frozen meat pies 4 pack", 0),
        ("Frozen lasagne 1kg", 0), ("Frozen mixed berries 500g", 0), ("Hash browns 1kg", 0),
        ("Frozen spring rolls 12 pack", 0), ("Chicken nuggets 1kg", 0), ("Frozen sweet corn 500g", 0),
        ("Ice blocks 8 pack", 0)]),
    "Biscuits": ((1.6, 3.5), (3.0, 7.6), 0.0, [
        ("Plain sweet biscuits 250g", 0), ("Cream filled biscuits 200g", 0), ("Water crackers 125g", 0),
        ("Chocolate coated biscuits 200g", 0), ("Shortbread 250g", 0), ("Rice crackers 100g", 0),
        ("Wholegrain crackers 200g", 0), ("Gluten free cookies 160g", 0), ("Choc chip cookies 300g", 0),
        ("Oat and golden syrup biscuits 300g", 0), ("Wafers 200g", 0), ("Ginger nut biscuits 250g", 0),
        ("Oatmeal biscuits 300g", 0), ("Cheese crackers 160g", 0), ("Butter biscuits 150g", 0),
        ("Animal biscuits 200g", 0)]),
    "Confectionery": ((2.5, 5.0), (3.5, 12.0), 0.0, [
        ("Milk chocolate block 180g", 0), ("Jelly lollies 200g", 0), ("Chocolate bar 50g", 0),
        ("Dark chocolate block 100g", 0), ("Boxed chocolates 250g", 0), ("Chocolate coated almonds 150g", 0),
        ("Licorice 300g", 0), ("Peppermints 50g", 0), ("Marshmallows 280g", 0), ("Chocolate eggs bag 150g", 0),
        ("Chewing gum 10 pack", 0), ("Caramel chocolate block 180g", 0), ("Sour lollies 180g", 0),
        ("Honeycomb 200g", 0), ("Fruit chews 200g", 0), ("Rocky road 150g", 0)]),
    "Chips and snacks": ((3.0, 6.5), (4.0, 12.0), 0.0, [
        ("Potato chips original 170g", 0), ("Corn chips 170g", 0), ("Salted peanuts 375g", 0),
        ("Kettle cooked chips 165g", 0), ("Cheese snacks 90g", 0), ("Microwave popcorn 3 pack", 0),
        ("Pretzels 200g", 0), ("Mixed nuts 375g", 0), ("Cashews 300g", 0), ("Vegetable crisps 100g", 0),
        ("Rice snacks 100g", 0), ("Seaweed snacks 5 pack", 0), ("Trail mix 400g", 0), ("Beef jerky 50g", 0),
        ("Protein bars 4 pack", 0), ("Muesli bars 6 pack", 0)]),
    "Soft drinks": ((1.6, 3.5), (3.0, 12.0), 0.0, [
        ("Cola 1.25L", 0), ("Lemonade 1.25L", 0), ("Sparkling mineral water 1.25L", 0),
        ("Cola cans 10 pack", 0), ("Diet cola 1.25L", 0), ("Ginger beer 4 pack", 0), ("Energy drink 250mL", 0),
        ("Sports drink 600mL", 0), ("Iced tea 1.5L", 0), ("Tonic water 1.25L", 0), ("Orange juice 2L", 0),
        ("Kombucha 330mL", 0), ("Flavoured mineral water 10 pack", 0), ("Fruit cordial 1L", 0),
        ("Coconut water 1L", 0), ("Lemon squash 1.25L", 0)]),
    "Coffee and tea": ((6.0, 12.0), (7.0, 28.0), 0.0, [
        ("Instant coffee 150g", 0), ("Black tea bags 100 pack", 0), ("Coffee capsules 10 pack", 0),
        ("Ground coffee 200g", 0), ("Coffee beans 1kg", 0), ("Freeze dried coffee 100g", 0),
        ("Decaf instant coffee 100g", 0), ("Green tea bags 50 pack", 0), ("Herbal tea bags 20 pack", 0),
        ("Chai latte sachets 10 pack", 0), ("Cold brew coffee 1L", 0), ("Loose leaf tea 250g", 0),
        ("Drinking chocolate 400g", 0), ("Coffee bags 18 pack", 0), ("Organic coffee beans 500g", 0),
        ("Matcha powder 100g", 0)]),
}
assert all(len(v[3]) == 16 for v in LINES.values()) and list(LINES) == CATS
N_FAST = 3

# ---------------------------------------------------------------------------------------------- files
FILES = {
    "movement": "gpi_movement_ry2026.csv",
    "totals": "store_weekly_sales_ry2026.csv",
    "register": "panel_store_register.csv",
    "partners": "partner_chains.xlsx",
    "items": "gpi_item_master_2026.csv",
    "log": "feed_delivery_log_ry2026.csv",
    "calendar": "retail_calendar_2025-2027.csv",
    "method": "gpi_methodology_statement_2026.pdf",
    "terms": "index_committee_terms_2027_structure.pdf",
    "dictionary": "gpi_feed_dictionary.xlsx",
    "manifest": "export_manifest.csv",
    "household": "household_panel_category_spend_2026.xlsx",
    "audit": "shelf_price_audit_2025.csv",
}
DISTRACTORS = ("household", "audit")
DELIVERABLES = ("gpi_2027_structure.xlsx", "gpi_2027_structure_paper.docx")
