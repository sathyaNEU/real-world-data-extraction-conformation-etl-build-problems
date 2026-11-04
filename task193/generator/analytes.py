"""The analyte lists each event runs and how each laboratory names and reports them. The indicators are three of
the inorganic list; everything else is the routine program's other parameters, reported the way each laboratory's
system writes them."""

# name, cas, method_A, method_B, unit (mg/L unless stated), rl, typical natural level at a well
INORGANIC = [
    ("Alkalinity, Total (as CaCO3)", "ALK", "SM 2320B", "SM 2320 B-2011", "mg/L", 5.0, 285.0),
    ("Ammonia as N", "7664-41-7", "EPA 350.1", "EPA 350.1", "mg/L", 0.10, 0.05),
    ("Calcium", "7440-70-2", "EPA 200.7", "EPA 200.7", "mg/L", 1.0, 72.0),
    ("Magnesium", "7439-95-4", "EPA 200.7", "EPA 200.7", "mg/L", 1.0, 31.0),
    ("Potassium", "7440-09-7", "EPA 200.7", "EPA 200.7", "mg/L", 0.50, 1.6),
    ("Sulfate", "14808-79-8", "EPA 300.0", "EPA 300.0", "mg/L", 2.0, 24.0),
    ("Nitrate + Nitrite as N", "NO3NO2", "EPA 353.2", "EPA 353.2", "mg/L", 0.10, 1.9),
    ("Total Dissolved Solids", "TDS", "SM 2540C", "SM 2540 C-2015", "mg/L", 10.0, 360.0),
    ("Iron", "7439-89-6", "EPA 200.7", "EPA 200.7", "mg/L", 0.05, 0.08),
    ("Manganese", "7439-96-5", "EPA 200.7", "EPA 200.7", "mg/L", 0.005, 0.03),
    ("Chloride", "16887-00-6", "EPA 300.0", "EPA 300.0", "mg/L", 1.0, None),
    ("Sodium", "7440-23-5", "EPA 200.7", "EPA 200.7", "mg/L", 0.50, None),
    ("Boron", "7440-42-8", "EPA 200.7", "EPA 200.7", "ug/L", 10.0, None),
]
DISSOLVED = {"Calcium", "Magnesium", "Potassium", "Iron", "Manganese", "Sodium", "Boron"}
METALS = [
    ("Arsenic", "7440-38-2", 1.0, 0.6), ("Barium", "7440-39-3", 5.0, 48.0), ("Cadmium", "7440-43-9", 0.5, None),
    ("Chromium", "7440-47-3", 2.0, None), ("Cobalt", "7440-48-4", 1.0, None), ("Copper", "7440-50-8", 2.0, 1.1),
    ("Lead", "7439-92-1", 1.0, None), ("Nickel", "7440-02-0", 2.0, 1.4), ("Selenium", "7782-49-2", 2.0, None),
    ("Vanadium", "7440-62-2", 2.0, 0.9), ("Zinc", "7440-66-6", 10.0, 6.0),
]
VOCS = [
    ("Acetone", "67-64-1", 10.0), ("Acrylonitrile", "107-13-1", 5.0), ("Benzene", "71-43-2", 0.5),
    ("Bromochloromethane", "74-97-5", 1.0), ("Bromodichloromethane", "75-27-4", 0.5), ("Bromoform", "75-25-2", 1.0),
    ("Bromomethane", "74-83-9", 2.0), ("2-Butanone (MEK)", "78-93-3", 10.0), ("Carbon disulfide", "75-15-0", 1.0),
    ("Carbon tetrachloride", "56-23-5", 0.5), ("Chlorobenzene", "108-90-7", 0.5), ("Chloroethane", "75-00-3", 1.0),
    ("Chloroform", "67-66-3", 0.5), ("Chloromethane", "74-87-3", 1.0), ("Dibromochloromethane", "124-48-1", 0.5),
    ("1,2-Dibromo-3-chloropropane", "96-12-8", 2.0), ("1,2-Dibromoethane", "106-93-4", 0.5),
    ("1,2-Dichlorobenzene", "95-50-1", 0.5), ("1,4-Dichlorobenzene", "106-46-7", 0.5),
    ("trans-1,4-Dichloro-2-butene", "110-57-6", 2.0), ("1,1-Dichloroethane", "75-34-3", 0.5),
    ("1,2-Dichloroethane", "107-06-2", 0.5), ("1,1-Dichloroethene", "75-35-4", 0.5),
    ("cis-1,2-Dichloroethene", "156-59-2", 0.5), ("trans-1,2-Dichloroethene", "156-60-5", 0.5),
    ("1,2-Dichloropropane", "78-87-5", 0.5), ("cis-1,3-Dichloropropene", "10061-01-5", 0.5),
    ("trans-1,3-Dichloropropene", "10061-02-6", 0.5), ("Ethylbenzene", "100-41-4", 0.5), ("2-Hexanone", "591-78-6", 5.0),
    ("Methyl iodide", "74-88-4", 2.0), ("Methylene chloride", "75-09-2", 2.0),
    ("4-Methyl-2-pentanone (MIBK)", "108-10-1", 5.0), ("Styrene", "100-42-5", 0.5),
    ("1,1,1,2-Tetrachloroethane", "630-20-6", 0.5), ("1,1,2,2-Tetrachloroethane", "79-34-5", 0.5),
    ("Tetrachloroethene", "127-18-4", 0.5), ("Toluene", "108-88-3", 0.5), ("1,1,1-Trichloroethane", "71-55-6", 0.5),
    ("1,1,2-Trichloroethane", "79-00-5", 0.5), ("Trichloroethene", "79-01-6", 0.5),
    ("Trichlorofluoromethane", "75-69-4", 1.0), ("1,2,3-Trichloropropane", "96-18-4", 1.0),
    ("Vinyl acetate", "108-05-4", 5.0), ("Vinyl chloride", "75-01-4", 0.2), ("Xylenes, Total", "1330-20-7", 1.0),
    ("Tetrahydrofuran", "109-99-9", 5.0),
]
SVOCS = [
    ("Acenaphthene", "83-32-9"), ("Acenaphthylene", "208-96-8"), ("Anthracene", "120-12-7"),
    ("Benzo(a)anthracene", "56-55-3"), ("Benzo(a)pyrene", "50-32-8"), ("Benzo(b)fluoranthene", "205-99-2"),
    ("Benzo(g,h,i)perylene", "191-24-2"), ("Benzo(k)fluoranthene", "207-08-9"), ("Benzyl alcohol", "100-51-6"),
    ("Bis(2-chloroethoxy)methane", "111-91-1"), ("Bis(2-chloroethyl)ether", "111-44-4"),
    ("Bis(2-ethylhexyl)phthalate", "117-81-7"), ("4-Bromophenyl phenyl ether", "101-55-3"),
    ("Butyl benzyl phthalate", "85-68-7"), ("4-Chloro-3-methylphenol", "59-50-7"), ("4-Chloroaniline", "106-47-8"),
    ("2-Chloronaphthalene", "91-58-7"), ("2-Chlorophenol", "95-57-8"), ("4-Chlorophenyl phenyl ether", "7005-72-3"),
    ("Chrysene", "218-01-9"), ("Dibenz(a,h)anthracene", "53-70-3"), ("Dibenzofuran", "132-64-9"),
    ("3,3'-Dichlorobenzidine", "91-94-1"), ("2,4-Dichlorophenol", "120-83-2"), ("Diethyl phthalate", "84-66-2"),
    ("2,4-Dimethylphenol", "105-67-9"), ("Dimethyl phthalate", "131-11-3"), ("Di-n-butyl phthalate", "84-74-2"),
    ("4,6-Dinitro-2-methylphenol", "534-52-1"), ("2,4-Dinitrophenol", "51-28-5"), ("2,4-Dinitrotoluene", "121-14-2"),
    ("2,6-Dinitrotoluene", "606-20-2"), ("Di-n-octyl phthalate", "117-84-0"), ("Fluoranthene", "206-44-0"),
    ("Fluorene", "86-73-7"), ("Hexachlorobenzene", "118-74-1"), ("Hexachlorobutadiene", "87-68-3"),
    ("Hexachlorocyclopentadiene", "77-47-4"), ("Hexachloroethane", "67-72-1"), ("Indeno(1,2,3-cd)pyrene", "193-39-5"),
    ("Isophorone", "78-59-1"), ("2-Methylnaphthalene", "91-57-6"), ("2-Methylphenol", "95-48-7"),
    ("3&4-Methylphenol", "65794-96-9"), ("Naphthalene", "91-20-3"), ("2-Nitroaniline", "88-74-4"),
    ("Nitrobenzene", "98-95-3"), ("2-Nitrophenol", "88-75-5"), ("4-Nitrophenol", "100-02-7"),
    ("N-Nitrosodi-n-propylamine", "621-64-7"), ("N-Nitrosodiphenylamine", "86-30-6"), ("Pentachlorophenol", "87-86-5"),
    ("Phenanthrene", "85-01-8"), ("Phenol", "108-95-2"), ("Pyrene", "129-00-0"), ("1,4-Dioxane", "123-91-1"),
]
PFAS = [
    ("Perfluorobutanoic acid (PFBA)", "375-22-4"), ("Perfluoropentanoic acid (PFPeA)", "2706-90-3"),
    ("Perfluorohexanoic acid (PFHxA)", "307-24-4"), ("Perfluoroheptanoic acid (PFHpA)", "375-85-9"),
    ("Perfluorooctanoic acid (PFOA)", "335-67-1"), ("Perfluorononanoic acid (PFNA)", "375-95-1"),
    ("Perfluorodecanoic acid (PFDA)", "335-76-2"), ("Perfluoroundecanoic acid (PFUnA)", "2058-94-8"),
    ("Perfluorododecanoic acid (PFDoA)", "307-55-1"), ("Perfluorobutanesulfonic acid (PFBS)", "375-73-5"),
    ("Perfluoropentanesulfonic acid (PFPeS)", "2706-91-4"), ("Perfluorohexanesulfonic acid (PFHxS)", "355-46-4"),
    ("Perfluoroheptanesulfonic acid (PFHpS)", "375-92-8"), ("Perfluorooctanesulfonic acid (PFOS)", "1763-23-1"),
    ("Perfluorooctanesulfonamide (PFOSA)", "754-91-6"), ("6:2 Fluorotelomer sulfonic acid", "27619-97-2"),
    ("8:2 Fluorotelomer sulfonic acid", "39108-34-4"), ("N-MeFOSAA", "2355-31-9"), ("N-EtFOSAA", "2991-50-6"),
    ("HFPO-DA (GenX)", "13252-13-6"),
]
SURROGATES = [("Dibromofluoromethane (surr)", "1868-53-7"), ("1,2-Dichloroethane-d4 (surr)", "17060-07-0"),
              ("Toluene-d8 (surr)", "2037-26-5"), ("4-Bromofluorobenzene (surr)", "460-00-4")]
SVOC_SURROGATES = [("2-Fluorophenol (surr)", "367-12-4"), ("Phenol-d5 (surr)", "4165-62-2"),
                   ("Nitrobenzene-d5 (surr)", "4165-60-0"), ("2-Fluorobiphenyl (surr)", "321-60-8"),
                   ("2,4,6-Tribromophenol (surr)", "118-79-6"), ("Terphenyl-d14 (surr)", "1718-51-0")]
# the program added PFAS from the October 2024 event
PFAS_FROM = "2024-OCT"
