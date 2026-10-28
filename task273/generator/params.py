"""task273 architecture 4: every constant the world, the pack and the goldens share.

The Ardvenny and Isles Health Board resets its Couples Carrier Screening Programme's panel each year from its own
population genome study. The Study sequenced its members in two phases on two capture kits and two calling
pipelines; the call is which of the 30 conditions under review go on the 2027/28 panel."""
from datetime import date

SEED = 2907

# ---------------------------------------------------------------------------------------------- the fiction
BOARD = "Ardvenny and Isles Health Board"
BOARD_SHORT = "the Board"
STUDY = "Ardvenny Genome Study"
LAB = "Kilvenny Genomics Laboratory"
PROGRAMME = "Couples Carrier Screening Programme"
PEOPLE = {"chair": "Abbie North", "lab_head": "Malcolm Lloyd"}
ROLES = {"chair": "Consultant Clinical Geneticist, Chair of the Panel Review Group",
         "lab_head": "Head of the Kilvenny Genomics Laboratory"}

CENSUS = date(2026, 11, 1)        # the policy's census date for the 2027/28 review
EXTRACT = date(2026, 11, 3)       # the Study and laboratory extracts
ASSEMBLED = date(2026, 11, 18)    # the pack assembled for the review
PAPER = date(2026, 12, 8)         # the executive team meeting
LIVE = date(2027, 4, 1)           # the 2027/28 panel starts
PROG_YEAR = (date(2025, 4, 1), date(2026, 3, 31))   # the programme's 2025/26 screening year
LIMS_UPGRADE = date(2025, 8, 4)   # from here the results export writes each finding's current class

# ---------------------------------------------------------------------------------------------- the Study
# (area, phase, members enrolled); phase 1 recruited in the islands and the glen, phase 2 on the mainland
AREAS = [("Morvaig Isles", 1, 3187), ("Glenhaskel", 1, 4846),
         ("Kilvenny", 2, 11338), ("Quarrendale", 2, 3419), ("Strathvenny", 2, 3207)]
FOUNDER_AREAS = ("Morvaig Isles", "Glenhaskel")
PHASE_DATES = {1: (date(2019, 8, 5), date(2021, 11, 26)), 2: (date(2022, 3, 7), date(2025, 10, 31))}
WITHDRAWN_SHARE = 0.0075          # consent withdrawn before the census
WITHDRAWN_LATE = 0.0012           # withdrawn after the census (still in the 2027/28 cohort)
QC_FAIL_SHARE = 0.0046            # no genotype released

# calling rules (the laboratory's methods report): a heterozygote needs at least K reads carrying the alternate
# allele making up at least F of the reads at the site; homozygous alternate at an allele fraction of 0.85 or more
CALLER = {1: dict(k=5, f=0.25, name="GermlineCall 2.3", kit="Exome capture panel v5 (2018 design)", build="GRCh37",
                  floor=8, transcript="legacy"),
          2: dict(k=3, f=0.20, name="GermlineCall 4.1", kit="Exome capture panel v8 (2021 design)", build="GRCh38",
                  floor=20, transcript="current")}
HOM_FRACTION = 0.85

# depth at a register site: floor + negative binomial excess; profiles by site class and phase
DEPTH = {("normal", 1): (13.0, 30), ("gc", 1): (1.4, 40), ("normal", 2): (58.0, 25), ("gc", 2): (44.0, 25)}

# ---------------------------------------------------------------------------------------------- conditions
# gene, condition, on the 2026/27 panel, carrier frequency per 1,000 (mainland, founder areas), variants:
# (hgvs_c, hgvs_p, legacy_c, share of the gene's carriers, site class, chrom, GRCh38 position, ref, alt)
# A legacy_c of None means the 2019 transcript names the variant the same way.
CONDITIONS = [
    ("CFTR", "Cystic fibrosis", True, (40.0, 40.0), [
        ("c.1521_1523del", "p.(Phe508del)", "c.1521_1523delCTT", .74, "normal", "7", 117559590, "ATCT", "A"),
        ("c.1624G>T", "p.(Gly542Ter)", None, .08, "normal", "7", 117587738, "G", "T"),
        ("c.1652G>A", "p.(Gly551Asp)", None, .07, "normal", "7", 117587806, "G", "A"),
        ("c.3909C>G", "p.(Asn1303Lys)", None, .06, "normal", "7", 117652877, "C", "G"),
        ("c.489+1G>T", "p.?", "c.621+1G>T", .05, "normal", "7", 117536785, "G", "T")]),
    ("PAH", "Phenylketonuria", True, (18.0, 18.0), [
        ("c.1222C>T", "p.(Arg408Trp)", None, .38, "normal", "12", 102840507, "G", "A"),
        ("c.1066-11G>A", "p.?", "c.1066-11G>A", .24, "normal", "12", 102846952, "C", "T"),
        ("c.782G>A", "p.(Arg261Gln)", None, .22, "normal", "12", 102852858, "C", "T"),
        ("c.842C>T", "p.(Pro281Leu)", None, .16, "normal", "12", 102852798, "G", "A")]),
    ("GJB2", "GJB2-related hearing loss", True, (16.5, 16.5), [
        ("c.35del", "p.(Gly12ValfsTer2)", "c.35delG", .88, "normal", "13", 20189547, "AC", "A"),
        ("c.71G>A", "p.(Trp24Ter)", None, .12, "normal", "13", 20189511, "C", "T")]),
    ("ACADM", "Medium-chain acyl-CoA dehydrogenase deficiency", True, (14.0, 14.0), [
        ("c.985A>G", "p.(Lys329Glu)", None, .86, "normal", "1", 75761161, "A", "G"),
        ("c.199T>C", "p.(Tyr67His)", None, .14, "normal", "1", 75732724, "T", "C")]),
    ("DHCR7", "Smith-Lemli-Opitz syndrome", True, (12.2, 12.2), [
        ("c.964-1G>C", "p.?", "c.964-1G>C", .58, "normal", "11", 71435763, "C", "G"),
        ("c.452G>A", "p.(Trp151Ter)", None, .24, "normal", "11", 71439287, "C", "T"),
        ("c.1054C>T", "p.(Arg352Trp)", None, .18, "normal", "11", 71435053, "G", "A")]),
    ("GALT", "Classic galactosaemia", True, (8.8, 8.8), [
        ("c.563A>G", "p.(Gln188Arg)", None, .82, "normal", "9", 34648167, "A", "G"),
        ("c.855G>T", "p.(Lys285Asn)", None, .18, "normal", "9", 34649032, "G", "T")]),
    ("ATP7B", "Wilson disease", True, (10.4, 10.4), [
        ("c.3207C>A", "p.(His1069Gln)", None, .62, "normal", "13", 51949672, "G", "T"),
        ("c.2333G>T", "p.(Arg778Leu)", None, .38, "normal", "13", 51958362, "C", "A")]),
    ("PKHD1", "Autosomal recessive polycystic kidney disease", True, (11.2, 11.2), [
        ("c.107C>T", "p.(Thr36Met)", None, .64, "normal", "6", 52086353, "G", "A"),
        ("c.5895dup", "p.(Leu1966ThrfsTer4)", "c.5895insA", .36, "normal", "6", 51906118, "T", "TA")]),
    ("MMUT", "Methylmalonic acidaemia, MMUT type", True, (7.4, 7.4), [
        ("c.655A>T", "p.(Asn219Tyr)", None, .55, "normal", "6", 49436606, "T", "A"),
        ("c.322C>T", "p.(Arg108Cys)", None, .45, "normal", "6", 49441723, "G", "A")]),
    ("GAA", "Pompe disease", True, (8.2, 8.2), [
        ("c.-32-13T>G", "p.?", "IVS1-13T>G", .72, "gc", "17", 80104542, "T", "G"),
        ("c.2560C>T", "p.(Arg854Ter)", None, .28, "normal", "17", 80117075, "C", "T")]),
    ("USH2A", "Usher syndrome type 2A", True, (7.6, 7.6), [
        ("c.2299del", "p.(Glu767SerfsTer21)", "c.2299delG", .78, "gc", "1", 216247118, "TC", "T"),
        ("c.2276G>T", "p.(Cys759Phe)", None, .22, "normal", "1", 216247141, "C", "A")]),
    ("SACS", "ARSACS, spastic ataxia of Charlevoix-Saguenay", False, (0.25, 20.5), [
        ("c.8844del", "p.(Ile2949SerfsTer5)", "c.8844delT", .93, "gc", "13", 23333404, "CA", "C"),
        ("c.7504C>T", "p.(Arg2502Ter)", None, .07, "normal", "13", 23334744, "G", "A")]),
    ("TMEM216", "Joubert syndrome type 2", False, (0.25, 19.0), [
        ("c.218G>T", "p.(Arg73Leu)", None, .95, "gc", "11", 61397984, "G", "T"),
        ("c.253C>T", "p.(Arg85Ter)", None, .05, "normal", "11", 61398019, "C", "T")]),
    ("SLC26A2", "Diastrophic dysplasia", False, (0.25, 20.0), [
        ("c.-26+2T>C", "p.?", "IVS1+2T>C", .92, "gc", "5", 149960780, "T", "C"),
        ("c.835C>T", "p.(Arg279Trp)", None, .08, "normal", "5", 149979437, "C", "T")]),
    ("HEXA", "Tay-Sachs disease", False, (1.6, 9.5), [
        ("c.1274_1277dup", "p.(Tyr427IlefsTer5)", "c.1278insTATC", .6, "gc", "15", 72346580, "G", "GGATA"),
        ("c.1421+1G>C", "p.?", None, .4, "normal", "15", 72345521, "C", "G")]),
    ("ASPA", "Canavan disease", False, (0.9, 0.9), [
        ("c.854A>C", "p.(Glu285Ala)", None, 1.0, "normal", "17", 3499019, "A", "C")]),
    ("FANCC", "Fanconi anaemia type C", False, (1.4, 1.4), [
        ("c.456+4A>T", "p.?", "IVS4+4A>T", .55, "normal", "9", 95172033, "T", "A"),
        ("c.67del", "p.(Asp23IlefsTer23)", "c.67delG", .45, "normal", "9", 95249244, "AC", "A")]),
    ("SMPD1", "Acid sphingomyelinase deficiency", False, (2.0, 2.0), [
        ("c.911T>C", "p.(Leu304Pro)", None, 1.0, "normal", "11", 6394121, "T", "C")]),
    ("NPC1", "Niemann-Pick disease type C1", False, (1.5, 9.0), [
        ("c.3182T>C", "p.(Ile1061Thr)", None, 1.0, "gc", "18", 23535640, "A", "G")]),
    ("PEX1", "Zellweger spectrum disorder", False, (3.25, 3.25), [
        ("c.2528G>A", "p.(Gly843Asp)", None, .7, "normal", "7", 92502049, "C", "T"),
        ("c.2097dup", "p.(Ile700TyrfsTer42)", "c.2097insT", .3, "normal", "7", 92509137, "A", "AT")]),
    ("G6PC1", "Glycogen storage disease type Ia", False, (2.6, 2.6), [
        ("c.247C>T", "p.(Arg83Cys)", None, 1.0, "normal", "17", 42903950, "C", "T")]),
    ("IDUA", "Mucopolysaccharidosis type I", False, (1.4, 9.8), [
        ("c.1205G>A", "p.(Trp402Ter)", None, .7, "gc", "4", 1003596, "G", "A"),
        ("c.208C>T", "p.(Gln70Ter)", None, .3, "normal", "4", 995500, "C", "T")]),
    ("ARSA", "Metachromatic leukodystrophy", False, (2.9, 2.9), [
        ("c.465+1G>A", "p.?", "c.459+1G>A", .55, "normal", "22", 50627509, "C", "T"),
        ("c.1283C>T", "p.(Pro428Leu)", None, .45, "normal", "22", 50625050, "G", "A")]),
    ("NPHS1", "Congenital nephrotic syndrome, Finnish type", False, (0.7, 0.7), [
        ("c.121_122del", "p.(Leu41AspfsTer50)", None, 1.0, "normal", "19", 35851386, "CAG", "C")]),
    ("AGA", "Aspartylglucosaminuria", False, (0.6, 0.6), [
        ("c.488G>C", "p.(Cys163Ser)", None, 1.0, "normal", "4", 177437139, "C", "G")]),
    ("BLM", "Bloom syndrome", False, (0.5, 0.5), [
        ("c.2207_2212delinsTAGATTC", "p.(Tyr736LeufsTer5)", "blmAsh", 1.0, "normal", "15", 90766923, "ATCTGA",
         "TAGATTC")]),
    ("ELP1", "Familial dysautonomia", False, (0.4, 0.4), [
        ("c.2204+6T>C", "p.?", "IVS20+6T>C", 1.0, "normal", "9", 108888896, "A", "G")]),
    ("MCOLN1", "Mucolipidosis type IV", False, (0.5, 0.5), [
        ("c.406-2A>G", "p.?", "IVS3-2A>G", 1.0, "normal", "19", 7525780, "A", "G")]),
    ("BCKDHB", "Maple syrup urine disease type 1B", False, (1.1, 1.1), [
        ("c.548G>C", "p.(Arg183Pro)", None, 1.0, "normal", "6", 80167548, "G", "C")]),
    ("PMM2", "PMM2-congenital disorder of glycosylation", False, (1.5, 8.6), [
        ("c.422G>A", "p.(Arg141His)", None, 1.0, "gc", "16", 8811088, "G", "A")]),
]
PANEL_LINE = 1 / 200            # the policy's line: at least one person in 200
# GRCh37 = GRCh38 - offset, one offset per chromosome region (the register carries both)
BUILD_OFFSET = {"1": 225134, "4": 22417, "5": 640212, "6": 34511, "7": 359946, "9": -37612, "11": 220733,
                "12": -394226, "13": 576138, "15": 292455, "16": 49921, "17": 4370, "18": 4121, "19": 44107,
                "22": -387210}

# coding sequence length of each gene's current transcript (bases), which bounds the register's texture entries
CDS_LENGTH = {"CFTR": 4443, "PAH": 1359, "GJB2": 681, "ACADM": 1266, "DHCR7": 1428, "GALT": 1140, "ATP7B": 4398,
              "PKHD1": 12222, "MMUT": 2253, "GAA": 2859, "USH2A": 15609, "SACS": 13740, "TMEM216": 438,
              "SLC26A2": 2220, "HEXA": 1590, "ASPA": 942, "FANCC": 1677, "SMPD1": 1896, "NPC1": 3837, "PEX1": 3852,
              "G6PC1": 1074, "IDUA": 1962, "ARSA": 1524, "NPHS1": 3726, "AGA": 1041, "BLM": 4254, "ELP1": 3999,
              "MCOLN1": 1743, "BCKDHB": 1179, "PMM2": 741}

# register texture: variants of uncertain significance and benign entries per gene, and the 2026 history
VUS_PER_GENE = (1, 3)
RECLASSIFIED = [  # (gene, hgvs_c, from, to, date): changes during 2026 that the census date sees
    ("GJB2", "c.101T>C", "Likely pathogenic", "Uncertain significance", date(2026, 6, 15)),
    ("PEX1", "c.1952_1960dup", "Uncertain significance", "Likely pathogenic", date(2026, 9, 2)),
    ("ATP7B", "c.2972C>T", "Likely pathogenic", "Uncertain significance", date(2026, 1, 21)),
    ("PAH", "c.1139C>T", "Uncertain significance", "Likely pathogenic", date(2026, 3, 10)),
    ("CFTR", "c.3454G>C", "Likely pathogenic", "Uncertain significance", date(2026, 7, 8)),
    ("ACADM", "c.799G>A", "Uncertain significance", "Likely pathogenic", date(2026, 4, 28)),
    ("DHCR7", "c.1342G>A", "Likely pathogenic", "Uncertain significance", date(2026, 5, 20)),
    ("MMUT", "c.1106G>A", "Uncertain significance", "Likely pathogenic", date(2026, 2, 16)),
    ("PKHD1", "c.9689del", "Likely pathogenic", "Uncertain significance", date(2026, 8, 25)),
    ("GALT", "c.404C>T", "Uncertain significance", "Likely pathogenic", date(2026, 6, 3)),
    ("GAA", "c.1935C>A", "Likely pathogenic", "Uncertain significance", date(2026, 3, 30)),
    ("USH2A", "c.4338_4339del", "Uncertain significance", "Likely pathogenic", date(2026, 9, 14)),
]
# programme-only variants and how often a screened partner carries each (none in the Study)
PROGRAMME_ONLY = {("ATP7B", "c.2972C>T"): 0.0062, ("PAH", "c.1139C>T"): 0.0058, ("GJB2", "c.101T>C"): 0.0036,
                  ("CFTR", "c.3454G>C"): 0.0049, ("ACADM", "c.799G>A"): 0.0044, ("DHCR7", "c.1342G>A"): 0.0041,
                  ("MMUT", "c.1106G>A"): 0.0039, ("PKHD1", "c.9689del"): 0.0043, ("GALT", "c.404C>T"): 0.0041,
                  ("GAA", "c.1935C>A"): 0.0038, ("USH2A", "c.4338_4339del"): 0.0040}
