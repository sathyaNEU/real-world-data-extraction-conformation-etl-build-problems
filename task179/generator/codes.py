"""The Merrow criminal code before and after the 1 July 2024 recodification, and Directive 26-07's Category V.

Each row: former section, new section, the new section's title, the generator's offence family, the felony or
misdemeanour level. The former code is Title 21 of the Merrow Statutes (21-3401 style, subsections in brackets);
the recodified Criminal Code numbers sections by chapter (302.10 style). A former section that the recodification
split carries one row per new section, each with its subsection."""

ROWS = [
    # former, new, title, family, level
    ("21-3401", "301.01", "Murder in the first degree", "VIOLENT", "F1"),
    ("21-3402", "301.02", "Murder in the second degree", "VIOLENT", "F1"),
    ("21-3403", "301.04", "Voluntary manslaughter", "VIOLENT", "F2"),
    ("21-3301/3402", "301.05", "Attempted murder", "VIOLENT", "F2"),
    ("21-3414", "302.10", "Aggravated assault causing bodily harm", "VIOLENT", "F3"),
    ("21-3410", "302.11", "Aggravated assault with a deadly weapon", "VIOLENT", "F3"),
    ("21-3414b", "302.12", "Aggravated domestic assault", "VIOLENT", "F4"),
    ("21-3408", "302.01", "Assault", "OTHER", "M2"),
    ("21-3412", "302.02", "Battery", "OTHER", "M1"),
    ("21-3412a", "302.05", "Domestic battery", "OTHER", "M1"),
    ("21-3433", "302.20", "Criminal threat", "OTHER", "F5"),
    ("21-3843", "302.40", "Violation of a protection order", "OTHER", "M1"),
    ("21-3426", "303.01", "Robbery", "VIOLENT", "F3"),
    ("21-3427(a)", "303.02", "Armed robbery", "VIOLENT", "F2"),
    ("21-3427(b)", "303.04", "Carjacking", "VIOLENT", "F2"),
    ("21-3420", "304.01", "Kidnapping", "VIOLENT", "F2"),
    ("21-3421", "304.02", "Aggravated kidnapping", "VIOLENT", "F1"),
    ("21-3502", "305.01", "Sexual assault in the first degree", "VIOLENT", "F1"),
    ("21-3503", "305.04", "Indecent liberties", "OTHER", "F4"),
    ("21-3608", "306.02", "Endangering a child", "OTHER", "M1"),
    ("21-3609", "306.03", "Aggravated endangering of a child", "OTHER", "F5"),
    ("21-3715", "401.01", "Burglary", "PROPERTY", "F4"),
    ("21-3716", "401.02", "Burglary of an occupied dwelling", "VIOLENT", "F3"),
    ("21-3701", "402.01", "Theft", "PROPERTY", "F5"),
    ("21-3705", "402.05", "Unauthorized use of a vehicle", "PROPERTY", "F6"),
    ("21-3720", "403.01", "Criminal damage to property", "PROPERTY", "M1"),
    ("21-4105", "403.05", "Criminal trespass", "OTHER", "M3"),
    ("21-3718", "404.01", "Arson", "PROPERTY", "F3"),
    ("21-3710", "405.02", "Forgery", "PROPERTY", "F6"),
    ("21-3707", "405.06", "Worthless check", "PROPERTY", "M2"),
    ("21-3734", "405.10", "Identity theft", "PROPERTY", "F5"),
    ("21-4204", "501.02", "Possession of a firearm by a prohibited person", "WEAPON", "F4"),
    ("21-4201(a)(4)", "501.04", "Carrying a concealed firearm without a licence", "WEAPON", "F5"),
    ("21-4219", "501.10", "Discharge of a firearm into an occupied structure", "WEAPON", "F3"),
    ("21-4203", "501.06", "Reckless discharge of a firearm", "WEAPON", "F5"),
    ("21-4220", "501.08", "Receiving a stolen firearm", "WEAPON", "F4"),
    ("21-4201(a)(1)", "501.12", "Carrying a dangerous knife", "OTHER", "M1"),
    ("21-5705", "601.03", "Distribution of a controlled substance", "DRUG", "F3"),
    ("21-5703", "601.05", "Manufacture of a controlled substance", "DRUG", "F2"),
    ("21-5706", "601.01", "Possession of a controlled substance", "DRUG", "F5"),
    ("21-5709", "601.08", "Possession of drug paraphernalia", "DRUG", "M2"),
    ("8-1567", "701.01", "Driving under the influence", "DUI", "M1"),
    ("8-1567(g)", "701.02", "Felony driving under the influence", "DUI", "F6"),
    ("8-262", "701.05", "Driving while suspended", "OTHER", "M2"),
    ("8-1568", "701.09", "Fleeing or eluding a police officer", "OTHER", "F6"),
    ("21-3808", "801.03", "Obstructing an officer", "OTHER", "M1"),
    ("21-3809", "801.07", "Escape from custody", "OTHER", "F5"),
    ("21-3824", "803.04", "Failure to register as an offender", "OTHER", "F5"),
    ("21-3813", "804.01", "Failure to appear", "OTHER", "M1"),
    ("21-4101", "802.01", "Disorderly conduct", "OTHER", "M3"),
]

# the rest of the Revisor's table: former sections of Title 21 and Title 8 that no record in the pack cites, each to its
# own new section; the generator never draws a charge from these, and none is a Category V section
EXTRA_ROWS = [
    ("21-3404", "301.06", "Involuntary manslaughter"),
    ("21-3405", "301.08", "Vehicular homicide"),
    ("21-3406", "301.09", "Assisting suicide"),
    ("21-3409", "302.06", "Assault of a law enforcement officer"),
    ("21-3413", "302.07", "Battery against a law enforcement officer"),
    ("21-3415", "302.15", "Mistreatment of a dependent adult"),
    ("21-3418", "302.25", "Stalking"),
    ("21-3419", "302.30", "Criminal restraint"),
    ("21-3424", "304.05", "Interference with parental custody"),
    ("21-3508", "305.08", "Lewd and lascivious behaviour"),
    ("21-3513", "305.10", "Promoting prostitution"),
    ("21-3517", "305.12", "Sexual battery"),
    ("21-3604", "306.01", "Abandonment of a child"),
    ("21-3610", "306.05", "Contributing to a child's misconduct"),
    ("21-3612", "306.07", "Furnishing alcohol to a minor"),
    ("21-3717", "401.05", "Burglary of a motor vehicle"),
    ("21-3702", "402.03", "Theft of services"),
    ("21-3703", "402.06", "Theft of lost or mislaid property"),
    ("21-3704", "402.07", "Theft of a motor vehicle"),
    ("21-3741", "402.10", "Receiving stolen property"),
    ("21-3742", "402.12", "Retail theft"),
    ("21-3721", "403.03", "Criminal desecration"),
    ("21-3722", "403.04", "Damage to a cemetery or burial ground"),
    ("21-3719", "404.03", "Reckless burning"),
    ("21-3709", "405.03", "Possession of forgery devices"),
    ("21-3711", "405.04", "Making a false information"),
    ("21-3708", "405.07", "Making a false writing"),
    ("21-3735", "405.11", "Identity fraud"),
    ("21-3712", "405.12", "Fraudulent insurance act"),
    ("21-3730", "405.14", "Unlawful computer access"),
    ("21-5701", "601.10", "Possession of a controlled substance precursor"),
    ("21-5707", "601.11", "Unlawful acts with a prescription"),
    ("21-5710", "601.12", "Use of a communication facility in a drug transaction"),
    ("21-5711", "601.14", "Possession of marijuana"),
    ("8-1566", "701.04", "Reckless driving"),
    ("8-235", "701.10", "Driving without a licence"),
    ("8-1602", "701.12", "Leaving the scene of an accident"),
    ("8-1606", "701.13", "Failure to report an accident"),
    ("8-1599", "701.15", "Transporting an open container"),
    ("8-142", "701.20", "Operating an unregistered vehicle"),
    ("21-3805", "801.01", "Perjury"),
    ("21-3806", "801.05", "Bribery"),
    ("21-3810", "801.09", "Aiding escape"),
    ("21-3812", "801.12", "Interference with the judicial process"),
    ("21-3820", "801.15", "False report of a crime"),
    ("21-4102", "802.02", "Riot"),
    ("21-4103", "802.03", "Unlawful assembly"),
    ("21-4108", "802.04", "Disturbing the peace"),
    ("21-4106", "802.06", "Public intoxication"),
    ("21-4107", "802.07", "Harassment by telecommunication"),
    ("21-4110", "802.10", "Cruelty to animals"),
    ("21-3825", "803.06", "Offender registration: failure to report a change of address"),
    ("21-3826", "803.08", "Offender residency restriction violation"),
    ("21-3814", "804.05", "Contempt of court"),
    ("21-3830", "804.06", "Violation of bond conditions"),
]

# Directive 26-07, Appendix: the recodified sections a Category V charge is laid under
SCHEDULE_B = ["301.01", "301.02", "301.04", "301.05", "302.10", "302.11", "302.12", "303.01", "303.02", "303.04",
              "304.01", "304.02", "305.01", "401.02", "501.02", "501.04", "501.06", "501.08", "501.10"]

OLD_TO_NEW = {r[0]: r[1] for r in ROWS}
NEW = {r[1]: r for r in ROWS}
TITLE = {r[1]: r[2] for r in ROWS}
FAMILY = {r[1]: r[3] for r in ROWS}
LEVEL = {r[1]: r[4] for r in ROWS}

# the new sections the generator draws a booking's charges from, by family
BY_FAMILY = {}
for _r in ROWS:
    BY_FAMILY.setdefault(_r[3], []).append(_r[1])

assert len(set(OLD_TO_NEW.values())) == len(ROWS) and all(s in NEW for s in SCHEDULE_B)
assert not set(r[0] for r in EXTRA_ROWS) & set(OLD_TO_NEW) and not set(r[1] for r in EXTRA_ROWS) & set(NEW)
assert len(set(r[0] for r in EXTRA_ROWS)) == len(set(r[1] for r in EXTRA_ROWS)) == len(EXTRA_ROWS)
assert not set(r[1] for r in EXTRA_ROWS) & set(SCHEDULE_B)
assert all(FAMILY[s] in ("VIOLENT", "WEAPON") for s in SCHEDULE_B)
assert all(s in SCHEDULE_B for s in NEW if FAMILY[s] in ("VIOLENT", "WEAPON"))
