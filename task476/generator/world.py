"""The fixed world: the City of Carrow (Hollis County, an unnamed Midwestern state), its Neighborhood Stabilization
Fund's 2027 round, the five candidate neighbourhoods, the 2010 tracts and block groups under them and how the 2020
census redrew them. Every other module reads its parameters from here."""

STATE_FIPS = "59"          # an unassigned code: the state is not named and no real county is meant
COUNTY_FIPS = "601"
COUNTY = "Hollis County"
STATE = "the state"
CITY = "Carrow"
DEPT = "Community Development Department"
FUND = "Neighborhood Stabilization Fund"
PEOPLE = {"analyst": ("Tamara Larson", "Housing Data Analyst"),
          "manager": ("Brandon Freeman", "Neighborhood Stabilization Fund Program Manager")}
GUIDELINE_DATE = "4 January 2027"
AS_OF = "2027-03-15"
MEMO_DATE = "12 April 2027"
VOTE_DATE = "26 April 2027"
THRESHOLD = 0.200          # 2019 to 2023 poverty rate, 20.0 per cent or more
Z90 = 1.645
MIN_TRACTS = 3

NEIGHBOURHOODS = ["Calloway Flats", "Dunmore Heights", "Kestrel Park", "Linden Row", "Sorrel Bend"]

# Each 2010 tract under a candidate neighbourhood: (2010 tract code, its block groups' (universe 2014-18,
# true poverty rate 2014-18, true rate 2019-23, universe growth to 2019-23)), and, when the 2020 census split it,
# the 2020 children as (2020 tract code, the block-group numbers they are made of).
CANDIDATES = {
    "Dunmore Heights": [
        ("0201.00", [(1310, .171, .296), (1255, .182, .301), (1398, .176, .292)], None),
        ("0202.00", [(1206, .152, .262), (1342, .163, .271), (1297, .171, .275)], None),
        ("0203.00", [(1405, .214, .262), (1288, .221, .255)], None),
        ("0204.00", [(1251, .181, .287), (1306, .193, .296), (1214, .176, .283)], None),
        ("0205.00", [(1512, .121, .142), (1388, .128, .147), (1356, .112, .121), (1447, .119, .128)],
         [("0205.01", [1, 2]), ("0205.02", [3, 4])]),
    ],
    "Linden Row": [
        ("0301.00", [(1302, .158, .281), (1247, .171, .274), (1351, .152, .266)], None),
        ("0302.00", [(1198, .176, .286), (1311, .169, .292), (1246, .188, .287)], None),
        ("0303.00", [(1352, .301, .318), (1296, .292, .311), (1411, .078, .081), (1503, .071, .079)],
         [("0303.01", [1, 2]), ("0303.02", [3, 4])]),
        ("0304.00", [(1309, .121, .133), (1252, .132, .124)], None),
        ("0305.00", [(1404, .213, .209), (1302, .221, .226), (1348, .204, .212)], None),
    ],
    "Kestrel Park": [
        ("0401.00", [(1297, .151, .263), (1254, .162, .271), (1352, .141, .255)], None),
        ("0402.00", [(1203, .168, .281), (1306, .177, .276), (1249, .158, .283)], None),
        ("0403.00", [(1448, .352, .158), (1402, .361, .163), (1452, .094, .212), (1497, .101, .208), (1405, .092, .215)],
         [("0403.01", [1, 2]), ("0403.02", [3, 4, 5])]),
        ("0404.00", [(1304, .222, .231), (1249, .231, .222)], None),
        ("0405.00", [(1398, .111, .121), (1303, .102, .118), (1352, .121, .112)], None),
    ],
    "Calloway Flats": [
        ("0501.00", [(1304, .162, .262), (1249, .171, .271), (1351, .153, .254)], None),
        ("0502.00", [(1302, .242, .251), (1248, .251, .243)], None),
        ("0503.00", [(1404, .102, .112), (1302, .121, .108), (1351, .112, .121), (1448, .101, .102)],
         [("0503.01", [1, 2]), ("0503.02", [3, 4])]),
        ("0504.00", [(1306, .141, .152), (1251, .132, .161)], None),
    ],
    "Sorrel Bend": [
        ("0601.00", [(1303, .081, .092), (1252, .092, .101), (1354, .073, .082)], None),
        ("0602.00", [(1302, .232, .212), (1249, .221, .206), (1402, .201, .332), (1353, .212, .329)],
         [("0602.01", [1, 2]), ("0602.02", [3, 4])]),
        ("0603.00", [(1302, .121, .141), (1251, .112, .132)], None),
        ("0604.00", [(1306, .251, .262), (1249, .262, .251), (1302, .243, .261)], None),
    ],
}
GROWTH = 1.031             # each block group's poverty universe from 2014-18 to 2019-23

# The rest of Hollis County: tracts the round does not consider (their codes and sizes); a few merged or split in 2020.
OTHER_TRACTS = 56
SAMPLE_FRACTION = 0.105    # the five-year sample's effective fraction of persons
DESIGN_EFFECT = 2.0
CANDIDATE_NOISE = 0.30     # how far a candidate block group's published estimate sits from its true count, in SEs
SEED = 476

FILES = {
    "guidelines": "nsf_2027_program_guidelines.pdf",
    "neighbourhoods": "carrow_nsf_2027_candidate_neighborhoods.xlsx",
    "tract18": "ACSDT5Y2018.B17001-Data-hollis-tracts.csv",
    "tract23": "ACSDT5Y2023.B17001-Data-hollis-tracts.csv",
    "bg18": "ACSDT5Y2018.B17021-Data-hollis-blockgroups.csv",
    "bg23": "ACSDT5Y2023.B17021-Data-hollis-blockgroups.csv",
    "tractrel": "tab20_tract20_tract10_st59_hollis.txt",
    "blockrel": "tab2010_tab2020_st59_hollis.txt",
    "parcels": "carrow_parcels_2027-03.csv",
    "cases": "carrow_code_cases_2019_2027.csv",
    "events": "carrow_code_case_events_2019_2027.csv",
    "payments": "nsf_rehab_payment_register_fy2023_fy2027.xlsx",
    "pl2010": "DECENNIALPL2010.P1-Data-hollis-blocks.csv",
}
GOLDEN = {"workbook": "nsf_2027_tract_poverty_change.xlsx", "memo": "nsf_2027_designation_memo.pdf"}
FILES["notes"] = "carrow_open_data_extract_notes.txt"
DEPT_SHORT = "CDD"
