"""The offence codes the county's charges carry, the draft's Appendix B, and the Pretrial Assessment Scale (version 2):
its items, points and the two six-point scores. The world draws charges from this table; the crosswalk, the draft's
appendix and the scoring guide are written from it."""
from __future__ import annotations

# kind: M eligible misdemeanor, MX misdemeanor in Appendix B, FH felony class H or I, FX felony class A to G
# (new code, legacy codes, statute, description, class, kind, violent, weight within its kind)
OFFENCES = [
    ("25120", ["2512"], "14-72(a)", "LARCENY (MISDEMEANOR)", "1", "M", False, 15),
    ("25130", ["2513"], "14-72.1(a)", "CONCEALMENT OF MERCHANDISE", "3", "M", False, 9),
    ("25140", ["2514"], "14-72(a)", "POSSESS STOLEN GOODS (MISDEMEANOR)", "1", "M", False, 4),
    ("26410", ["2641"], "14-160(a)", "INJURY TO PERSONAL PROPERTY", "2", "M", False, 5),
    ("26420", ["2642"], "14-127", "INJURY TO REAL PROPERTY", "1", "M", False, 2),
    ("57120", ["5712"], "14-159.13", "SECOND DEGREE TRESPASS", "3", "M", False, 9),
    ("57110", ["5711"], "14-159.12", "FIRST DEGREE TRESPASS", "2", "M", False, 3),
    ("35110", ["3511", "3512"], "90-95(d)(4)", "SIMPLE POSSESS SCH VI CS (MARIJUANA)", "1", "M", False, 9),
    ("35610", ["3561"], "90-113.22", "POSSESS DRUG PARAPHERNALIA", "1", "M", False, 11),
    ("35620", ["3562"], "90-113.22A", "POSSESS MARIJUANA PARAPHERNALIA", "3", "M", False, 4),
    ("35140", ["3514"], "90-95(d)(3)", "SIMPLE POSSESS SCH IV CS", "1", "M", False, 2),
    ("54210", ["5421"], "20-28(a)", "DRIVING WHILE LICENSE REVOKED", "3", "M", False, 11),
    ("48010", ["4801"], "14-223", "RESIST, DELAY, OBSTRUCT PUBLIC OFFICER", "2", "M", False, 8),
    ("13110", ["1311"], "14-33(a)", "SIMPLE ASSAULT", "2", "M", True, 6),
    ("53110", ["5311"], "14-288.4(a)", "DISORDERLY CONDUCT", "2", "M", False, 4),
    ("26230", ["2623"], "14-107(d)(1)", "WORTHLESS CHECK", "2", "M", False, 1),
    ("22110", ["2211"], "14-54(b)", "BREAKING OR ENTERING (MISDEMEANOR)", "1", "M", False, 2),
    ("24110", ["2411"], "14-72.2", "UNAUTHORIZED USE OF MOTOR VEHICLE", "1", "M", False, 2),
    ("53210", ["5321"], "14-444", "INTOXICATED AND DISRUPTIVE", "3", "M", False, 3),
    ("48020", ["4802"], "20-29", "GIVE FALSE INFORMATION TO OFFICER", "2", "M", False, 2),
    ("13130", ["1313"], "14-33(c)(2)", "ASSAULT ON A FEMALE", "A1", "MX", True, 10),
    ("13120", ["1312"], "14-33(c)(1)", "ASSAULT WITH A DEADLY WEAPON", "A1", "MX", True, 4),
    ("16010", ["1601"], "14-277.1", "COMMUNICATING THREATS", "1", "MX", False, 5),
    ("13910", ["1391"], "50B-4.1(a)", "VIOLATION OF DV PROTECTIVE ORDER", "A1", "MX", False, 4),
    ("16110", ["1611"], "14-277.3A(c)", "STALKING", "A1", "MX", False, 1),
    ("54110", ["5411"], "20-138.1", "DRIVING WHILE IMPAIRED", "DWI", "MX", False, 10),
    ("52110", ["5211"], "14-269(a1)", "CARRYING CONCEALED GUN", "2", "MX", False, 2),
    ("13140", ["1314"], "14-33(c)(4)", "ASSAULT ON A GOVERNMENT OFFICIAL", "A1", "MX", True, 2),
    ("23120", ["2312"], "14-72(a)", "LARCENY (FELONY)", "H", "FH", False, 8),
    ("22010", ["2201"], "14-54(a)", "BREAKING AND OR ENTERING (FELONY)", "H", "FH", False, 7),
    ("24010", ["2401"], "20-106", "POSSESS STOLEN MOTOR VEHICLE", "H", "FH", False, 3),
    ("26010", ["2601"], "14-100", "OBTAIN PROPERTY FALSE PRETENSE", "H", "FH", False, 4),
    ("35210", ["3521"], "90-95(d)(2)", "POSSESS SCH II CS", "I", "FH", False, 10),
    ("35310", ["3531"], "90-95(a)(1)", "PWISD MARIJUANA", "I", "FH", False, 4),
    ("48110", ["4811"], "20-141.5(b)", "FELONY FLEE ELUDE ARREST", "H", "FH", False, 3),
    ("23130", ["2313"], "14-72(b)(1)", "LARCENY FROM THE PERSON", "H", "FH", False, 2),
    ("22210", ["2221"], "14-56", "BREAK OR ENTER A MOTOR VEHICLE", "I", "FH", False, 4),
    ("52010", ["5201"], "14-415.1", "POSSESS FIREARM BY FELON", "G", "FX", False, 5),
    ("13010", ["1301"], "14-32(b)", "AWDW INFLICTING SERIOUS INJURY", "E", "FX", True, 3),
    ("12010", ["1201"], "14-87", "ROBBERY WITH DANGEROUS WEAPON", "D", "FX", True, 2),
    ("35410", ["3541"], "90-95(h)(4)", "TRAFFICKING OPIUM OR HEROIN", "E", "FX", False, 2),
    ("13020", ["1302"], "14-32(c)", "AWDW INFLICTING SERIOUS INJURY (C)", "F", "FX", True, 1),
]

BY_CODE = {o[0]: o for o in OFFENCES}
LEGACY_TO_NEW = {lc: o[0] for o in OFFENCES for lc in o[1]}
KIND_CODES = {k: [o for o in OFFENCES if o[5] == k] for k in ("M", "MX", "FH", "FX")}
MISD_CLASSES = ("A1", "1", "2", "3")

# Appendix B of the draft: offences that take a defendant out of the presumptive tier, by statute; "any subsection"
# entries match every subsection of the section
APPENDIX_B = [
    ("14-33(c)(1)", "Assault with a deadly weapon", False),
    ("14-33(c)(2)", "Assault on a female", False),
    ("14-33(c)(4)", "Assault on a government officer or employee", False),
    ("14-269", "Carrying a concealed weapon (any subsection)", True),
    ("14-277.1", "Communicating threats", False),
    ("14-277.3A", "Stalking (any subsection)", True),
    ("20-138.1", "Impaired driving", False),
    ("50B-4.1", "Violation of a domestic violence protective order (any subsection)", True),
]


def in_appendix_b(statute):
    for s, _, anysub in APPENDIX_B:
        if statute == s or (anysub and statute.startswith(s + "(")):
            return True
    return False


def eligible_charge(code):
    o = BY_CODE[code]
    return o[4] in MISD_CLASSES and not in_appendix_b(o[2])


# ---------------------------------------------------------------------------------------------------- the scale
# new-criminal-activity items (points)
NCA_ITEMS = [
    ("age_22_or_under", "Age 22 or younger at the current arrest", {0: 0, 1: 2}),
    ("pending_charge", "Charge pending at the time of the current arrest", {0: 0, 1: 3}),
    ("prior_misd_conviction", "Prior misdemeanor conviction", {0: 0, 1: 1}),
    ("prior_felony_conviction", "Prior felony conviction", {0: 0, 1: 1}),
    ("prior_violent_conviction", "Prior violent conviction (one or two: 1; three or more: 2)", {0: 0, 1: 1, 2: 2}),
    ("prior_incarceration", "Prior sentence to incarceration of more than 30 days", {0: 0, 1: 1}),
]
# raw new-criminal-activity points (0 to 10) to the score
NCA_BANDS = [(0, 0, 1), (1, 2, 2), (3, 4, 3), (5, 6, 4), (7, 7, 5), (8, 10, 6)]
# failure-to-appear items
FTA_ITEMS = [
    ("pending_charge", "Charge pending at the time of the current arrest", {0: 0, 1: 1}),
    ("prior_conviction", "Prior conviction (misdemeanor or felony)", {0: 0, 1: 1}),
    ("fta_past_2_years", "Failures to appear in the past two years (one: 2; two or more: 4)", {0: 0, 1: 2, 2: 4}),
    ("fta_older", "Failure to appear more than two years ago", {0: 0, 1: 1}),
]
FTA_BANDS = [(0, 0, 1), (1, 1, 2), (2, 2, 3), (3, 4, 4), (5, 6, 5), (7, 7, 6)]


def band(raw, bands):
    for lo, hi, s in bands:
        if lo <= raw <= hi:
            return s
    raise ValueError(raw)
