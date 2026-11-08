"""task197 architecture 2: names and fixed facts of the world (all invented organisations, products and people)."""
import datetime as dt

NETWORK = "Midcontinent Poison Data Network"
NETWORK_SHORT = "MPDN"
OFFICE = "Child Packaging Safety Office"
OFFICE_SHORT = "the Office"
PROVIDER = "Halcyon Retail Measurement"
PEOPLE = {"secretary": "Timothy Moran", "lead": "Gary Richards"}

# member poison centers: code, name, states served, the zone their call log is kept in, share of the network's calls
CENTERS = [
    ("C01", "Tallgrass Poison Center", "KS, NE", "America/Chicago", 0.12),
    ("C02", "Northland Poison Center", "ND, SD, MN", "America/Chicago", 0.10),
    ("C03", "Lakeshore Poison and Drug Information Center", "MI", "America/Detroit", 0.15),
    ("C04", "Ohio Valley Regional Poison Center", "OH, KY", "America/New_York", 0.18),
    ("C05", "Ozark Poison Information Service", "MO, AR", "America/Chicago", 0.11),
    ("C06", "Loess Hills Poison Control", "IA", "America/Chicago", 0.06),
    ("C07", "North Woods Poison Center", "WI", "America/Chicago", 0.08),
    ("C08", "Wabash Poison Center", "IN, IL", "America/Indiana/Indianapolis", 0.15),
    ("C09", "Front Range Poison and Drug Center", "CO", "America/Denver", 0.05),
]

# product metadata. UPC packs: (upc, description as the scan provider writes it, pack, share of the product's units)
META = {
    "FKJ": dict(name="Feverkind Junior Strength Acetaminophen Oral Suspension", maker="Laurentide Consumer Health",
                ingredient="Acetaminophen", strength="160 mg/5 mL", form="Oral suspension",
                packs=[("0 41763 21140 5", "FEVERKIND JR STR ACETAMIN SUSP GRAPE 4OZ", "4 fl oz (118 mL)", 0.71),
                       ("0 41763 21142 9", "FEVERKIND JR STR ACETAMIN SUSP CHRY 4OZ", "4 fl oz (118 mL)", 0.29)],
                closure_old="Child-resistant push-and-turn cap", closure_new="Squeeze-and-turn flow cap with dosing-syringe port",
                text=["Feverkind Junior", "FEVERKIND JR", "feverkind junior strength", "Feverkind Jr Strength grape",
                      "Feverkind children's acetaminophen", "Feverkind jr 160mg/5ml"]),
    "DOZ": dict(name="Dozinox Nighttime Sleep-Aid Doxylamine Succinate Tablets", maker="Corvan Health Brands",
                ingredient="Doxylamine succinate", strength="25 mg", form="Tablet",
                packs=[("3 08217 44032 6", "DOZINOX SLEEP AID TAB 32CT", "32 tablets", 0.64),
                       ("3 08217 44048 7", "DOZINOX SLEEP AID TAB 48CT", "48 tablets", 0.36)],
                closure_old="Bottle with child-resistant cap", closure_new="Child-resistant foil blister in carton",
                text=["Dozinox", "DOZINOX", "dozinox sleep aid", "Dozinox doxylamine", "doxylamine (Dozinox)"]),
    "GUM": dict(name="Sunnybear Kids Multivitamin with Iron Gummies", maker="Bright Meadow Nutrition",
                ingredient="Multivitamin with iron", strength="2 mg iron per gummy", form="Gummy",
                packs=[("8 51296 10070 2", "SUNNYBEAR KIDS MULTI+IRON GUMMY 70CT", "70 gummies", 0.58),
                       ("8 51296 10120 4", "SUNNYBEAR KIDS MULTI+IRON GUMMY 120CT", "120 gummies", 0.42)],
                closure_old="Child-resistant bottle", closure_new="Child-resistant wide-mouth jar",
                text=["Sunnybear gummies", "SUNNYBEAR KIDS GUMMIES", "sunnybear multivitamin", "Sunnybear multi + iron",
                      "sunny bear gummy vitamins"]),
    "EYE": dict(name="Clearview Redness Relief Tetrahydrozoline Eye Drops", maker="Corvan Health Brands",
                ingredient="Tetrahydrozoline hydrochloride", strength="0.05%", form="Ophthalmic solution",
                packs=[("3 08217 51015 0", "CLEARVIEW REDNESS RELIEF DROPS .5OZ", "0.5 fl oz (15 mL)", 1.0)],
                closure_old="Child-resistant dropper bottle", closure_new="Child-resistant dropper bottle, new tamper band",
                text=["Clearview eye drops", "CLEARVIEW", "clearview redness relief", "Clearview drops (tetrahydrozoline)"]),
    "NIC": dict(name="Embercalm Nicotine Polacrilex Lozenge Mint", maker="Holbrook Pharma",
                ingredient="Nicotine polacrilex", strength="4 mg", form="Lozenge",
                packs=[("6 12773 30072 1", "EMBERCALM LOZENGE MINT 4MG 72CT", "72 lozenges", 0.55),
                       ("6 12773 30020 2", "EMBERCALM LOZENGE MINT 4MG 20CT POCKET", "20 lozenges", 0.45)],
                closure_old="Child-resistant bottle", closure_new="Child-resistant pocket blister pack",
                text=["Embercalm lozenge", "EMBERCALM", "embercalm 4 mg", "Embercalm mint lozenges", "nicotine lozenge (Embercalm)"]),
    "IBC": dict(name="Ibucalm Children's Ibuprofen Oral Suspension", maker="Laurentide Consumer Health",
                ingredient="Ibuprofen", strength="100 mg/5 mL", form="Oral suspension",
                packs=[("0 41763 33041 0", "IBUCALM CHLD IBUPROF SUSP BERRY 4OZ", "4 fl oz (118 mL)", 1.0)],
                closure_old="Child-resistant cap, dosing cup", closure_new="Child-resistant cap, dosing syringe",
                text=["Ibucalm children's", "IBUCALM", "ibucalm childrens ibuprofen", "Ibucalm berry"]),
    "VAP": dict(name="Vapocare Medicated Chest Rub", maker="Holbrook Pharma",
                ingredient="Camphor, menthol, eucalyptus oil", strength="4.8% camphor", form="Ointment",
                packs=[("6 12773 41100 9", "VAPOCARE CHEST RUB 3.53OZ", "3.53 oz (100 g) jar", 0.77),
                       ("6 12773 41050 7", "VAPOCARE CHEST RUB 1.76OZ", "1.76 oz (50 g) jar", 0.23)],
                closure_old="Child-resistant jar lid", closure_new="Child-resistant jar lid, recessed grip",
                text=["Vapocare", "VAPOCARE RUB", "vapocare chest rub", "Vapocare camphor rub"]),
    "CGH": dict(name="Coughex Children's Dextromethorphan Cough Syrup", maker="Laurentide Consumer Health",
                ingredient="Dextromethorphan hydrobromide", strength="7.5 mg/5 mL", form="Syrup",
                packs=[("0 41763 52044 4", "COUGHEX CHLD COUGH DM SYRUP 4OZ", "4 fl oz (118 mL)", 1.0)],
                closure_old="Child-resistant cap", closure_new="Child-resistant cap, PET bottle",
                text=["Coughex children's", "COUGHEX", "coughex dm syrup", "Coughex cough syrup"]),
    "FKI": dict(name="Feverkind Infants' Acetaminophen Oral Suspension", maker="Laurentide Consumer Health",
                ingredient="Acetaminophen", strength="160 mg/5 mL", form="Oral suspension",
                packs=[("0 41763 21101 6", "FEVERKIND INFANTS ACETAMIN SUSP 1OZ", "1 fl oz (30 mL)", 1.0)],
                closure_old="Child-resistant cap with flow restrictor", closure_new="",
                text=["Feverkind infants", "FEVERKIND INF", "feverkind infant drops", "Feverkind infants acetaminophen"]),
    "ALC": dict(name="Wrenfield Children's Cetirizine Oral Solution", maker="Corvan Health Brands",
                ingredient="Cetirizine hydrochloride", strength="1 mg/mL", form="Oral solution",
                packs=[("3 08217 60004 1", "WRENFIELD CHLD CETIRIZINE SOL 4OZ", "4 fl oz (118 mL)", 1.0)],
                closure_old="Child-resistant cap", closure_new="",
                text=["Wrenfield children's", "WRENFIELD", "wrenfield cetirizine", "Wrenfield syrup"]),
    "IBT": dict(name="Ibucalm Ibuprofen Tablets", maker="Laurentide Consumer Health",
                ingredient="Ibuprofen", strength="200 mg", form="Coated tablet",
                packs=[("0 41763 33100 4", "IBUCALM IBUPROFEN TAB 200MG 100CT", "100 tablets", 0.62),
                       ("0 41763 33050 2", "IBUCALM IBUPROFEN TAB 200MG 50CT", "50 tablets", 0.38)],
                closure_old="Bottle with child-resistant cap", closure_new="",
                text=["Ibucalm tablets", "IBUCALM 200", "ibucalm ibuprofen 200mg", "Ibucalm tabs"]),
    "FER": dict(name="Ferrocare Ferrous Sulfate Tablets", maker="Bright Meadow Nutrition",
                ingredient="Ferrous sulfate", strength="325 mg (65 mg iron)", form="Tablet",
                packs=[("8 51296 20100 0", "FERROCARE FERROUS SULF 325MG 100CT", "100 tablets", 1.0)],
                closure_old="Bottle with child-resistant cap", closure_new="",
                text=["Ferrocare iron tablets", "FERROCARE", "ferrocare ferrous sulfate", "iron tablets (Ferrocare)"]),
}
# network product codes for the watched products
PRODUCT_CODE = {"FKJ": "MP-40211", "DOZ": "MP-40375", "GUM": "MP-40598", "EYE": "MP-40712", "NIC": "MP-40864",
                "IBC": "MP-40933", "VAP": "MP-41087", "CGH": "MP-41126", "FKI": "MP-40209", "ALC": "MP-41340",
                "IBT": "MP-40936", "FER": "MP-41452"}
NOTIFIED = {"FKJ": dt.date(2024, 8, 22), "DOZ": dt.date(2024, 2, 5), "GUM": dt.date(2025, 1, 14),
            "EYE": dt.date(2024, 10, 9), "NIC": dt.date(2025, 3, 3), "IBC": dt.date(2025, 5, 28),
            "VAP": dt.date(2024, 5, 16), "CGH": dt.date(2025, 8, 4)}

# the network's paediatric hospitals that return antidote preparation records
HOSPITALS = [
    ("H11", "Tallgrass Children's Hospital", "Wichita", "KS", "C01"),
    ("H23", "Lakeshore Children's Medical Center", "Grand Rapids", "MI", "C03"),
    ("H34", "Riverbend Children's Hospital", "Cincinnati", "OH", "C04"),
    ("H52", "Ozark Children's Hospital", "Springfield", "MO", "C05"),
]

DOC_DATES = {"procedure": dt.date(2026, 3, 9), "call": dt.date(2026, 9, 21), "register": dt.date(2026, 10, 30)}
