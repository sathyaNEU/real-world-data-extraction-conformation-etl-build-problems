"""The register's reference catalog: the aircraft models and engines the four counties' registrations carry, with the
weights and years that place each airframe on a model of its own class. The simulation flies a small set of base
models (fleet.MODELS); each airframe is registered as a catalog model with the same aircraft type, engine type,
engine count, build certification and emitter category, built in a year the model was built, so nothing the
inventory prices moves."""
import numpy as np

# engines: code, manufacturer, model, type (1 reciprocating, 2 turbo-prop, 3 turbo-shaft, 5 turbo-fan), hp, thrust
ENGINES = [
    ("17003", "CONT MOTOR", "A-65-8", 1, 65, 0), ("17005", "CONT MOTOR", "C-85-12", 1, 85, 0),
    ("17006", "CONT MOTOR", "C-90-12F", 1, 90, 0), ("17007", "CONT MOTOR", "C-125-2", 1, 125, 0),
    ("17008", "CONT MOTOR", "O-200-A", 1, 100, 0), ("17009", "CONT MOTOR", "O-300-A", 1, 145, 0),
    ("17010", "CONT MOTOR", "C-145-2", 1, 145, 0), ("17011", "CONT MOTOR", "O-470-K", 1, 230, 0),
    ("17012", "CONT MOTOR", "O-470-U", 1, 230, 0), ("17013", "CONT MOTOR", "O-470-R", 1, 230, 0),
    ("17014", "CONT MOTOR", "IO-470-L", 1, 260, 0), ("17015", "CONT MOTOR", "IO-240-B", 1, 125, 0),
    ("17016", "CONT MOTOR", "IO-470-VO", 1, 260, 0), ("17018", "CONT MOTOR", "IO-360-ES", 1, 200, 0),
    ("17019", "CONT MOTOR", "IO-360-GB", 1, 210, 0), ("17020", "CONT MOTOR", "IO-520-BB", 1, 285, 0),
    ("17021", "CONT MOTOR", "IO-520-D", 1, 300, 0), ("17022", "CONT MOTOR", "IO-520-F", 1, 300, 0),
    ("17023", "CONT MOTOR", "IO-520-L", 1, 300, 0), ("17024", "CONT MOTOR", "IO-520-M", 1, 285, 0),
    ("17026", "CONT MOTOR", "IO-550-N", 1, 310, 0), ("17030", "CONT MOTOR", "IO-550-C", 1, 300, 0),
    ("17031", "CONT MOTOR", "TSIO-520-R", 1, 310, 0), ("17032", "CONT MOTOR", "TSIO-520-P", 1, 310, 0),
    ("17033", "CONT MOTOR", "TSIO-520-BE", 1, 310, 0), ("17034", "CONT MOTOR", "TSIO-520-NB", 1, 325, 0),
    ("17035", "CONT MOTOR", "GTSIO-520-L", 1, 375, 0), ("17036", "CONT MOTOR", "TSIO-360-E", 1, 200, 0),
    ("17037", "CONT MOTOR", "TSIO-360-RB", 1, 220, 0), ("17038", "CONT MOTOR", "TSIO-360-MB", 1, 210, 0),
    ("17040", "CONT MOTOR", "IO-550-B", 1, 300, 0), ("17041", "CONT MOTOR", "IO-550-G", 1, 280, 0),
    ("17042", "CONT MOTOR", "TSIO-550-K", 1, 315, 0), ("17043", "CONT MOTOR", "TSIO-550-G", 1, 280, 0),
    ("17045", "CONT MOTOR", "E-185-3", 1, 205, 0),
    ("41500", "LYCOMING", "O-145-B2", 1, 65, 0), ("41501", "LYCOMING", "O-235-C1", 1, 115, 0),
    ("41502", "LYCOMING", "O-235-C2C", 1, 108, 0), ("41503", "LYCOMING", "O-235-L2C", 1, 110, 0),
    ("41504", "LYCOMING", "O-235-K2C", 1, 115, 0), ("41544", "LYCOMING", "O-290-D2", 1, 135, 0),
    ("41510", "LYCOMING", "O-320-A2B", 1, 150, 0), ("41511", "LYCOMING", "O-320-E2A", 1, 150, 0),
    ("41512", "LYCOMING", "O-320-E2D", 1, 150, 0), ("41513", "LYCOMING", "O-320-E3D", 1, 150, 0),
    ("41514", "LYCOMING", "O-320-D2J", 1, 160, 0), ("41515", "LYCOMING", "O-320-H2AD", 1, 160, 0),
    ("41516", "LYCOMING", "O-320-D3G", 1, 160, 0), ("41517", "LYCOMING", "O-320-E2G", 1, 150, 0),
    ("41518", "LYCOMING", "O-320-D1A", 1, 160, 0), ("41519", "LYCOMING", "O-320-D2A", 1, 160, 0),
    ("41520", "LYCOMING", "O-360-A4M", 1, 180, 0), ("41521", "LYCOMING", "O-360-A1F6D", 1, 180, 0),
    ("41522", "LYCOMING", "AEIO-320-E2B", 1, 150, 0), ("41523", "LYCOMING", "IO-320-B1A", 1, 160, 0),
    ("41524", "LYCOMING", "O-360-A1A", 1, 180, 0), ("41525", "LYCOMING", "IO-360-L2A", 1, 180, 0),
    ("41526", "LYCOMING", "O-360-A1D", 1, 180, 0), ("41527", "LYCOMING", "O-360-A3A", 1, 180, 0),
    ("41528", "LYCOMING", "O-360-A4K", 1, 180, 0), ("41529", "LYCOMING", "O-360-C1G", 1, 180, 0),
    ("41530", "LYCOMING", "O-360-A1P", 1, 180, 0), ("41531", "LYCOMING", "IO-540-K1G5", 1, 300, 0),
    ("41532", "LYCOMING", "O-360-A1G6D", 1, 180, 0), ("41533", "LYCOMING", "O-360-E1A6D", 1, 180, 0),
    ("41534", "LYCOMING", "IO-360-A1A", 1, 200, 0), ("41535", "LYCOMING", "IO-360-A3B6D", 1, 200, 0),
    ("41536", "LYCOMING", "TIO-540-A2C", 1, 310, 0), ("41537", "LYCOMING", "IO-360-C1C", 1, 200, 0),
    ("41538", "LYCOMING", "IO-360-C1C6", 1, 200, 0), ("41539", "LYCOMING", "IO-360-A1B6D", 1, 200, 0),
    ("41540", "LYCOMING", "IO-360-A1B6", 1, 200, 0), ("41541", "LYCOMING", "O-360-A1H6", 1, 180, 0),
    ("41542", "LYCOMING", "IO-360-M1A", 1, 180, 0), ("41548", "LYCOMING", "IO-390-A3A6", 1, 210, 0),
    ("41549", "LYCOMING", "O-540-A1D5", 1, 250, 0), ("41550", "LYCOMING", "O-540-B2B5", 1, 235, 0),
    ("41551", "LYCOMING", "O-540-J3A5D", 1, 235, 0), ("41552", "LYCOMING", "O-540-J1A5D", 1, 235, 0),
    ("41553", "LYCOMING", "IO-540-K1A5", 1, 300, 0), ("41554", "LYCOMING", "IO-540-C4B5", 1, 250, 0),
    ("41555", "LYCOMING", "IO-540-AB1A5", 1, 230, 0), ("41556", "LYCOMING", "IO-540-AC1A5", 1, 300, 0),
    ("41557", "LYCOMING", "IO-540-W1A5", 1, 235, 0), ("41558", "LYCOMING", "IO-540-D4A5", 1, 260, 0),
    ("41559", "LYCOMING", "TIO-540-AK1A", 1, 235, 0), ("41560", "LYCOMING", "TIO-540-AE2A", 1, 350, 0),
    ("41561", "LYCOMING", "TIO-540-J2BD", 1, 350, 0),
    ("33101", "FRANKLIN", "6A4-150-B3", 1, 150, 0), ("33102", "FRANKLIN", "6A4-165-B3", 1, 165, 0),
    ("71106", "ROTAX", "912 ULS", 1, 100, 0),
    ("52005", "P&W CANADA", "PT6A-21", 2, 550, 0), ("52008", "P&W CANADA", "PT6A-28", 2, 620, 0),
    ("52010", "P&W CANADA", "PT6A-34", 2, 750, 0), ("52012", "P&W CANADA", "PT6A-42", 2, 850, 0),
    ("52013", "P&W CANADA", "PT6A-42A", 2, 1000, 0), ("52015", "P&W CANADA", "PT6A-60A", 2, 1050, 0),
    ("52017", "P&W CANADA", "PT6A-64", 2, 700, 0), ("52018", "P&W CANADA", "PT6A-66D", 2, 850, 0),
    ("52019", "P&W CANADA", "PT6A-67B", 2, 1200, 0), ("52020", "P&W CANADA", "PT6A-67P", 2, 1200, 0),
    ("52030", "P&W CANADA", "PT6A-114", 2, 600, 0), ("52031", "P&W CANADA", "PT6A-114A", 2, 675, 0),
    ("52033", "P&W CANADA", "PT6A-135A", 2, 550, 0), ("52045", "P&W CANADA", "PW535E", 5, 0, 3360),
    ("52046", "P&W CANADA", "PW545C", 5, 0, 4119), ("52047", "P&W CANADA", "PW615F", 5, 0, 1460),
    ("52048", "P&W CANADA", "PW617F-E", 5, 0, 1695),
    ("78001", "WILLIAMS", "FJ44-1A", 5, 0, 1965), ("78003", "WILLIAMS", "FJ44-2C", 5, 0, 2400),
    ("78005", "WILLIAMS", "FJ44-3A", 5, 0, 2820), ("78007", "WILLIAMS", "FJ44-4A", 5, 0, 3621),
    ("78008", "WILLIAMS", "FJ44-4A-QPM", 5, 0, 3435), ("39010", "GE HONDA", "HF120", 5, 0, 2095),
    ("62010", "ROLLS-ROYC", "250-C20B", 3, 420, 0), ("62012", "ROLLS-ROYC", "250-C20J", 3, 420, 0),
    ("62030", "ROLLS-ROYC", "250-C30P", 3, 650, 0), ("62040", "ROLLS-ROYC", "250-C47B", 3, 650, 0),
    ("29501", "TURBOMECA", "ARRIEL 2B1", 3, 847, 0),
]
ENGINE_BY_CODE = {e[0]: e for e in ENGINES}


def M(code, mfr, model, ta, te, ne, seats, bc, eng, wt, spd, years, pop, groups, names, kit=None):
    return dict(code=code, mfr=mfr, model=model, ta=ta, te=te, ne=ne, seats=seats, bc=bc, eng=eng, wt=wt, spd=spd,
                years=years, pop=pop, groups=groups, names=names, kit=kit)


S, B, V, X, C = "school", "bush", "vintage", "complex", "general"
CATALOG = [
    # single-engine piston, type certificated
    M("2070402", "CESSNA", "150", 4, 1, 1, 2, 0, ["17008"], 1600, 100, (1959, 1966), 2, [S, C], ["Cessna 150"]),
    M("2070434", "CESSNA", "150L", 4, 1, 1, 2, 0, ["17008"], 1600, 105, (1971, 1974), 3, [S, C], ["Cessna 150L", "C150L"]),
    M("2070436", "CESSNA", "150M", 4, 1, 1, 2, 0, ["17008"], 1600, 105, (1975, 1977), 4, [S, C], ["Cessna 150M", "C-150M"]),
    M("2071206", "CESSNA", "152", 4, 1, 1, 2, 0, ["41503"], 1670, 110, (1978, 1985), 8, [S, C], ["Cessna 152", "C152", "Cessna 152 II"]),
    M("2070201", "CESSNA", "170B", 4, 1, 1, 4, 0, ["17010"], 2200, 120, (1952, 1956), 2, [B, V], ["Cessna 170B", "C170B"]),
    M("2072001", "CESSNA", "172", 4, 1, 1, 4, 0, ["17009"], 2200, 120, (1956, 1960), 2, [C, V], ["Cessna 172", "C172"]),
    M("2072318", "CESSNA", "172M", 4, 1, 1, 4, 0, ["41512", "41520"], 2300, 125, (1973, 1976), 8, [S, C], ["Cessna 172M Skyhawk", "C172M", "Cessna 172M"]),
    M("2072706", "CESSNA", "172N", 4, 1, 1, 4, 0, ["41515", "41520"], 2300, 125, (1977, 1980), 10, [S, C], ["Cessna 172N Skyhawk", "C172N", "Cessna 172N"]),
    M("2072710", "CESSNA", "172P", 4, 1, 1, 4, 0, ["41514"], 2400, 125, (1981, 1986), 6, [S, C], ["Cessna 172P", "C172P Skyhawk"]),
    M("2072735", "CESSNA", "172R", 4, 1, 1, 4, 0, ["41525"], 2450, 140, (1996, 2009), 6, [S, C], ["Cessna 172R", "C172R", "Cessna 172R Skyhawk"]),
    M("2072738", "CESSNA", "172S", 4, 1, 1, 4, 0, ["41525"], 2550, 145, (1998, 2023), 9, [S, C], ["Cessna 172S", "Cessna 172 Skyhawk SP", "C172S"]),
    M("2072810", "CESSNA", "177B", 4, 1, 1, 4, 0, ["41521"], 2500, 145, (1971, 1978), 2, [C], ["Cessna Cardinal 177B", "C177B"]),
    M("2072815", "CESSNA", "177RG", 4, 1, 1, 4, 0, ["41539"], 2800, 165, (1971, 1978), 1, [X], ["Cessna 177RG Cardinal RG"]),
    M("2072921", "CESSNA", "180", 4, 1, 1, 4, 0, ["17011", "17013"], 2800, 155, (1953, 1981), 3, [B, C], ["Cessna 180", "C180 Skywagon"]),
    M("2073001", "CESSNA", "182P", 4, 1, 1, 4, 0, ["17013"], 2950, 150, (1972, 1976), 5, [C, X], ["Cessna 182P Skylane", "C182P"]),
    M("2073002", "CESSNA", "182Q", 4, 1, 1, 4, 0, ["17012"], 2950, 150, (1977, 1980), 5, [C, X], ["Cessna 182Q", "C182Q Skylane"]),
    M("2073003", "CESSNA", "182R", 4, 1, 1, 4, 0, ["17012"], 3100, 150, (1981, 1986), 2, [C, X], ["Cessna 182R"]),
    M("2073005", "CESSNA", "182S", 4, 1, 1, 4, 0, ["41555"], 3100, 165, (1997, 2000), 2, [C, X], ["Cessna 182S Skylane"]),
    M("2073006", "CESSNA", "182T", 4, 1, 1, 4, 0, ["41555"], 3100, 165, (2001, 2023), 6, [C, X], ["Cessna 182T", "C182T Skylane", "Cessna 182T Skylane"]),
    M("2073009", "CESSNA", "T182T", 4, 1, 1, 4, 0, ["41559"], 3100, 180, (2001, 2013), 1, [X], ["Cessna T182T Turbo Skylane"]),
    M("2073106", "CESSNA", "A185F", 4, 1, 1, 6, 0, ["17021"], 3350, 165, (1973, 1985), 2, [B], ["Cessna A185F Skywagon", "C185"]),
    M("2073201", "CESSNA", "U206G", 4, 1, 1, 6, 0, ["17022"], 3600, 160, (1977, 1986), 2, [B, C], ["Cessna U206G Stationair"]),
    M("2073208", "CESSNA", "206H", 4, 1, 1, 6, 0, ["41556"], 3600, 160, (1998, 2023), 2, [C, X], ["Cessna 206H Stationair", "C206H"]),
    M("2073504", "CESSNA", "210N", 4, 1, 1, 6, 0, ["17023"], 3800, 190, (1979, 1985), 2, [X], ["Cessna 210N Centurion"]),
    M("2073505", "CESSNA", "T210N", 4, 1, 1, 6, 0, ["17031"], 4000, 195, (1979, 1985), 2, [X], ["Cessna T210N Turbo Centurion", "C T210N"]),
    M("2073508", "CESSNA", "P210N", 4, 1, 1, 6, 0, ["17032"], 4000, 210, (1978, 1986), 1, [X], ["Cessna P210N"]),
    M("7100210", "PIPER", "J3C-65", 4, 1, 1, 2, 0, ["17003"], 1220, 75, (1938, 1947), 6, [V, B], ["Piper J-3 Cub", "J3C-65 Cub", "Piper J3C"]),
    M("7100410", "PIPER", "PA-11", 4, 1, 1, 2, 0, ["17006"], 1220, 85, (1947, 1949), 2, [V, B], ["Piper PA-11 Cub Special"]),
    M("7100512", "PIPER", "PA-12", 4, 1, 1, 3, 0, ["41501"], 1750, 95, (1946, 1948), 3, [V, B], ["Piper PA-12 Super Cruiser"]),
    M("7100801", "PIPER", "PA-15", 4, 1, 1, 2, 0, ["41500"], 1100, 85, (1948, 1949), 1, [V], ["Piper Vagabond PA-15"]),
    M("7101822", "PIPER", "PA-18-150", 4, 1, 1, 2, 0, ["41510"], 1750, 115, (1955, 1994), 2, [B, V], ["Piper PA-18-150 Super Cub", "PA18 Super Cub"]),
    M("7102001", "PIPER", "PA-20-135", 4, 1, 1, 4, 0, ["41544"], 1800, 120, (1950, 1954), 2, [V], ["Piper Pacer PA-20"]),
    M("7102205", "PIPER", "PA-22-150", 4, 1, 1, 4, 0, ["41510"], 2000, 125, (1955, 1960), 4, [V, C], ["Piper PA-22-150 Tri-Pacer", "Piper Tri-Pacer"]),
    M("7102212", "PIPER", "PA-22-108", 4, 1, 1, 2, 0, ["41501"], 1650, 105, (1961, 1963), 2, [V], ["Piper Colt PA-22-108"]),
    M("7102415", "PIPER", "PA-24-250", 4, 1, 1, 4, 0, ["41549"], 2900, 175, (1958, 1964), 2, [X], ["Piper Comanche 250", "PA-24-250 Comanche"]),
    M("7102701", "PIPER", "PA-28-140", 4, 1, 1, 4, 0, ["41511"], 2150, 120, (1964, 1977), 6, [S, C], ["Piper Cherokee 140", "PA-28-140"]),
    M("7102703", "PIPER", "PA-28-151", 4, 1, 1, 4, 0, ["41513"], 2325, 120, (1974, 1977), 3, [S, C], ["Piper Warrior PA-28-151"]),
    M("7102805", "PIPER", "PA-28-161", 4, 1, 1, 4, 0, ["41516"], 2440, 125, (1977, 2012), 8, [S, C], ["Piper PA-28-161 Warrior II", "Piper Warrior", "PA28-161"]),
    M("7102806", "PIPER", "PA-28-180", 4, 1, 1, 4, 0, ["41527"], 2400, 130, (1963, 1975), 4, [C], ["Piper Cherokee 180", "PA-28-180"]),
    M("7102810", "PIPER", "PA-28-181", 4, 1, 1, 4, 0, ["41520"], 2550, 135, (1976, 2023), 8, [S, C], ["Piper PA-28-181 Archer", "Piper Archer II", "PA28-181"]),
    M("7102820", "PIPER", "PA-28-236", 4, 1, 1, 4, 0, ["41551"], 3000, 150, (1979, 1994), 1, [C, X], ["Piper Dakota PA-28-236"]),
    M("7102860", "PIPER", "PA-28R-200", 4, 1, 1, 4, 0, ["41537"], 2650, 150, (1971, 1976), 2, [X, S], ["Piper Arrow II PA-28R-200"]),
    M("7102866", "PIPER", "PA-28R-201", 4, 1, 1, 4, 0, ["41538"], 2750, 150, (1977, 2016), 2, [X, S], ["Piper Arrow III", "PA-28R-201 Arrow"]),
    M("7103201", "PIPER", "PA-32-300", 4, 1, 1, 6, 0, ["41553"], 3400, 155, (1966, 1979), 3, [C, X], ["Piper Cherokee Six PA-32-300"]),
    M("7103215", "PIPER", "PA-32R-301", 4, 1, 1, 6, 0, ["41531"], 3600, 165, (1980, 2007), 3, [X], ["Piper Saratoga PA-32R-301", "PA-32R-301 Saratoga SP"]),
    M("7104610", "PIPER", "PA-46-310P", 4, 1, 1, 6, 0, ["17033"], 4100, 215, (1984, 1988), 1, [X], ["Piper Malibu PA-46-310P"]),
    M("7104615", "PIPER", "PA-46-350P", 4, 1, 1, 6, 0, ["41560"], 4340, 220, (1989, 2023), 1.2, [X], ["Piper Malibu Mirage", "PA-46-350P"]),
    M("0560108", "BEECH", "V35B", 4, 1, 1, 6, 0, ["17020"], 3400, 185, (1968, 1982), 4, [X], ["Beech V35B Bonanza", "Bonanza V35B"]),
    M("0560201", "BEECH", "F33A", 4, 1, 1, 5, 0, ["17020"], 3400, 180, (1970, 1994), 2, [X], ["Beech F33A Bonanza"]),
    M("0560416", "BEECH", "A36", 4, 1, 1, 6, 0, ["17040"], 3650, 185, (1970, 2005), 4, [X], ["Beech A36 Bonanza", "Bonanza A36"]),
    M("0560420", "BEECH", "G36", 4, 1, 1, 6, 0, ["17040"], 3650, 185, (2006, 2023), 1, [X], ["Beech G36 Bonanza"]),
    M("0560503", "BEECH", "C23", 4, 1, 1, 4, 0, ["41528"], 2450, 120, (1972, 1983), 2, [C, S], ["Beech Sundowner C23"]),
    M("0560610", "BEECH", "C24R", 4, 1, 1, 4, 0, ["41540"], 2750, 145, (1970, 1983), 1, [X], ["Beech Sierra C24R"]),
    M("0560701", "BEECH", "77", 4, 1, 1, 2, 0, ["41503"], 1675, 105, (1979, 1981), 1, [S], ["Beech Skipper 77"]),
    M("6070102", "MOONEY", "M20C", 4, 1, 1, 4, 0, ["41526"], 2575, 160, (1962, 1978), 4, [X, C], ["Mooney M20C Ranger", "Mooney M20C"]),
    M("6070104", "MOONEY", "M20E", 4, 1, 1, 4, 0, ["41534"], 2575, 170, (1964, 1975), 2, [X], ["Mooney M20E Chaparral"]),
    M("6070103", "MOONEY", "M20F", 4, 1, 1, 4, 0, ["41534"], 2740, 165, (1966, 1977), 3, [X], ["Mooney M20F Executive"]),
    M("6070105", "MOONEY", "M20J", 4, 1, 1, 4, 0, ["41535"], 2740, 175, (1977, 1998), 3, [X], ["Mooney M20J 201", "Mooney M20J"]),
    M("6070106", "MOONEY", "M20K", 4, 1, 1, 4, 0, ["17038"], 2900, 190, (1979, 1996), 1, [X], ["Mooney M20K 231"]),
    M("6070110", "MOONEY", "M20R", 4, 1, 1, 4, 0, ["17041"], 3368, 190, (1994, 2008), 1, [X], ["Mooney M20R Ovation"]),
    M("6070112", "MOONEY", "M20TN", 4, 1, 1, 4, 0, ["17043"], 3368, 220, (2006, 2019), 1, [X], ["Mooney Acclaim M20TN"]),
    M("1150120", "CIRRUS DESIGN CORP", "SR20", 4, 1, 1, 4, 0, ["17018"], 3050, 175, (2001, 2023), 4, [S, X], ["Cirrus SR20", "SR-20"]),
    M("1150122", "CIRRUS DESIGN CORP", "SR22", 4, 1, 1, 4, 0, ["17026"], 3600, 205, (2001, 2023), 5, [X], ["Cirrus SR22", "Cirrus SR-22", "SR22 G3"]),
    M("1150125", "CIRRUS DESIGN CORP", "SR22T", 4, 1, 1, 4, 0, ["17042"], 3600, 215, (2010, 2023), 2, [X], ["Cirrus SR22T", "SR22T G6"]),
    M("1351402", "DIAMOND", "DA20-C1", 4, 1, 1, 2, 0, ["17015"], 1764, 135, (1998, 2011), 3, [S], ["Diamond DA20-C1 Eclipse", "DA-20"]),
    M("1351408", "DIAMOND", "DA 40", 4, 1, 1, 4, 0, ["41542"], 2646, 155, (2002, 2021), 3, [S, X], ["Diamond DA40 Diamond Star", "DA-40"]),
    M("0410105", "GRUMMAN AMERICAN AVN. CORP", "AA-1B", 4, 1, 1, 2, 0, ["41502"], 1560, 115, (1971, 1976), 1, [S, C], ["Grumman AA-1B Trainer"]),
    M("0410202", "GRUMMAN AMERICAN AVN. CORP", "AA-5A", 4, 1, 1, 4, 0, ["41517"], 2200, 130, (1976, 1979), 2, [C], ["Grumman Cheetah AA-5A"]),
    M("0410204", "GRUMMAN AMERICAN AVN. CORP", "AA-5B", 4, 1, 1, 4, 0, ["41528"], 2400, 150, (1975, 1993), 2, [C], ["Grumman Tiger AA-5B", "AA5B Tiger"]),
    M("5800515", "MAULE", "M-5-235C", 4, 1, 1, 4, 0, ["41552"], 2300, 145, (1975, 1990), 0.4, [B], ["Maule M-5-235C Lunar Rocket"]),
    M("5800721", "MAULE", "M-7-235B", 4, 1, 1, 4, 0, ["41557"], 2500, 150, (1990, 2023), 0.6, [B], ["Maule M-7-235B", "Maule M7"]),
    M("0761601", "AMERICAN CHAMPION AIRCRAFT", "7ECA", 4, 1, 1, 2, 0, ["41504"], 1650, 110, (1965, 2023), 1.2, [B, S], ["Citabria 7ECA", "American Champion Citabria"]),
    M("0761605", "AMERICAN CHAMPION AIRCRAFT", "7GCAA", 4, 1, 1, 2, 0, ["41510"], 1800, 115, (1965, 2023), 0.5, [B], ["Citabria 7GCAA Adventure"]),
    M("0761610", "AMERICAN CHAMPION AIRCRAFT", "8KCAB", 4, 1, 1, 2, 0, ["41522"], 1950, 130, (1970, 2023), 0.6, [B, S], ["Decathlon 8KCAB", "Super Decathlon"]),
    M("0910103", "AVIAT AIRCRAFT INC", "A-1B", 4, 1, 1, 2, 0, ["41529"], 2000, 120, (1998, 2007), 0.3, [B], ["Aviat Husky A-1B"]),
    M("0910105", "AVIAT AIRCRAFT INC", "A-1C-180", 4, 1, 1, 2, 0, ["41530"], 2200, 125, (2007, 2023), 0.5, [B], ["Aviat Husky A-1C-180", "Husky A1C"]),
    M("3770102", "ERCO", "415-C", 4, 1, 1, 2, 0, ["17005"], 1260, 105, (1946, 1948), 3, [V], ["Ercoupe 415-C", "Erco 415C"]),
    M("3770104", "ERCO", "415-D", 4, 1, 1, 2, 0, ["17005"], 1400, 105, (1947, 1949), 1, [V], ["Ercoupe 415-D"]),
    M("0182001", "AERONCA", "7AC", 4, 1, 1, 2, 0, ["17003"], 1220, 85, (1946, 1948), 5, [V, B], ["Aeronca Champ 7AC", "Aeronca 7AC Champion"]),
    M("0182201", "AERONCA", "11AC", 4, 1, 1, 2, 0, ["17003"], 1250, 90, (1946, 1949), 2, [V], ["Aeronca Chief 11AC"]),
    M("8640011", "TAYLORCRAFT", "BC12-D", 4, 1, 1, 2, 0, ["17003"], 1200, 90, (1941, 1947), 4, [V], ["Taylorcraft BC12-D", "Taylorcraft BC-12D"]),
    M("5320006", "LUSCOMBE", "8A", 4, 1, 1, 2, 0, ["17003"], 1260, 95, (1946, 1949), 4, [V], ["Luscombe 8A Silvaire", "Luscombe 8A"]),
    M("5320008", "LUSCOMBE", "8E", 4, 1, 1, 2, 0, ["17005"], 1400, 105, (1946, 1949), 2, [V], ["Luscombe 8E"]),
    M("8310102", "STINSON", "108-1", 4, 1, 1, 4, 0, ["33101"], 2230, 120, (1946, 1947), 2, [V], ["Stinson 108-1 Voyager"]),
    M("8310106", "STINSON", "108-2", 4, 1, 1, 4, 0, ["33102"], 2230, 120, (1947, 1948), 2, [V], ["Stinson 108-2 Voyager"]),
    M("8310108", "STINSON", "108-3", 4, 1, 1, 4, 0, ["33102"], 2400, 120, (1947, 1949), 3, [V], ["Stinson 108-3 Station Wagon", "Stinson 108-3"]),
    M("2070102", "CESSNA", "120", 4, 1, 1, 2, 0, ["17005"], 1450, 100, (1946, 1949), 3, [V], ["Cessna 120"]),
    M("2070104", "CESSNA", "140", 4, 1, 1, 2, 0, ["17005"], 1450, 105, (1946, 1950), 4, [V, B], ["Cessna 140", "C-140"]),
    M("2070182", "CESSNA", "170A", 4, 1, 1, 4, 0, ["17010"], 2200, 115, (1949, 1952), 2, [V, B], ["Cessna 170A"]),
    M("3900105", "GLOBE", "GC-1B", 4, 1, 1, 2, 0, ["17007"], 1710, 140, (1946, 1947), 1, [V], ["Globe Swift GC-1B"]),
    M("6201002", "NORTH AMERICAN", "NAVION", 4, 1, 1, 4, 0, ["17045"], 2750, 140, (1946, 1951), 2, [V], ["Navion", "North American Navion"]),
    # single-engine piston, amateur built
    M("05628K4", "VANS", "RV-4", 4, 1, 1, 2, 1, ["41518"], 1500, 180, (1985, 2012), 3, [B, X], ["Vans RV-4", "RV4"], ("VANS AIRCRAFT INC", "RV-4")),
    M("05628K6", "VANS", "RV-6A", 4, 1, 1, 2, 1, ["41518", "41524"], 1600, 180, (1988, 2012), 3, [C, X], ["Vans RV-6A", "RV-6A"], ("VANS AIRCRAFT INC", "RV-6A")),
    M("05628KW", "VANS", "RV-7A", 4, 1, 1, 2, 1, ["41524"], 1800, 190, (2000, 2023), 4, [C, X], ["Vans RV-7A", "RV-7A", "RV7A"], ("VANS AIRCRAFT INC", "RV-7A")),
    M("05628K8", "VANS", "RV-8", 4, 1, 1, 2, 1, ["41524"], 1800, 195, (1996, 2023), 2, [B, X], ["Vans RV-8", "RV-8"], ("VANS AIRCRAFT INC", "RV-8")),
    M("05628K9", "VANS", "RV-9A", 4, 1, 1, 2, 1, ["41519"], 1750, 175, (2002, 2023), 3, [C], ["Vans RV-9A"], ("VANS AIRCRAFT INC", "RV-9A")),
    M("05628KT", "VANS", "RV-10", 4, 1, 1, 4, 1, ["41558"], 2700, 190, (2004, 2023), 3, [X], ["Vans RV-10", "RV10"], ("VANS AIRCRAFT INC", "RV-10")),
    M("05628KC", "VANS", "RV-12", 4, 1, 1, 2, 1, ["71106"], 1320, 130, (2009, 2023), 1, [C, B], ["Vans RV-12"], ("VANS AIRCRAFT INC", "RV-12")),
    M("4710305", "KITFOX", "SERIES 7", 4, 1, 1, 2, 1, ["71106"], 1550, 110, (2001, 2023), 0.8, [B], ["Kitfox Series 7", "Kitfox"], ("KITFOX AIRCRAFT LLC", "SERIES 7")),
    M("9820750", "ZENITH", "CH 750", 4, 1, 1, 2, 1, ["17008"], 1440, 95, (2008, 2023), 0.5, [B], ["Zenith CH 750 STOL"], ("ZENITH AIRCRAFT CO", "CH 750")),
    M("5103601", "LANCAIR", "360", 4, 1, 1, 2, 1, ["41534"], 1685, 220, (1990, 2008), 1, [X], ["Lancair 360"], ("LANCAIR", "360")),
    # multi-engine piston
    M("0566005", "BEECH", "95-B55", 5, 1, 2, 5, 0, ["17014"], 5100, 195, (1964, 1982), 3, [C, X], ["Beech Baron 95-B55", "Baron B55"]),
    M("0566012", "BEECH", "58", 5, 1, 2, 6, 0, ["17030"], 5500, 210, (1970, 2023), 4, [C, X], ["Beech Baron 58", "Baron 58"]),
    M("0567601", "BEECH", "76", 5, 1, 2, 4, 0, ["41532"], 3900, 165, (1978, 1982), 2, [S], ["Beech Duchess 76"]),
    M("7102303", "PIPER", "PA-23-250", 5, 1, 2, 6, 0, ["41554"], 5200, 185, (1960, 1981), 3, [C], ["Piper Aztec PA-23-250", "Piper Aztec"]),
    M("7103001", "PIPER", "PA-30", 5, 1, 2, 4, 0, ["41523"], 3600, 175, (1963, 1969), 1, [C], ["Piper Twin Comanche PA-30"]),
    M("7103405", "PIPER", "PA-34-200T", 5, 1, 2, 6, 0, ["17036"], 4750, 190, (1975, 1981), 3, [C, S], ["Piper Seneca II PA-34-200T", "Seneca II"]),
    M("7103410", "PIPER", "PA-34-220T", 5, 1, 2, 6, 0, ["17037"], 4750, 195, (1981, 2001), 3, [C, S], ["Piper Seneca III", "PA-34-220T"]),
    M("7104402", "PIPER", "PA-44-180", 5, 1, 2, 4, 0, ["41533"], 3800, 165, (1979, 2015), 3, [S], ["Piper Seminole PA-44-180", "PA44 Seminole"]),
    M("7103101", "PIPER", "PA-31", 5, 1, 2, 7, 0, ["41536"], 6500, 220, (1967, 1983), 1, [C], ["Piper Navajo PA-31"]),
    M("7103106", "PIPER", "PA-31-350", 5, 1, 2, 8, 0, ["41561"], 7000, 230, (1973, 1984), 1, [C], ["Piper Navajo Chieftain PA-31-350"]),
    M("2073804", "CESSNA", "310Q", 5, 1, 2, 6, 0, ["17016"], 5300, 205, (1970, 1974), 2, [C], ["Cessna 310Q"]),
    M("2073905", "CESSNA", "310R", 5, 1, 2, 6, 0, ["17024"], 5500, 210, (1975, 1981), 2, [C], ["Cessna 310R", "C310R"]),
    M("2074003", "CESSNA", "340A", 5, 1, 2, 6, 0, ["17034"], 5990, 230, (1976, 1984), 1, [X], ["Cessna 340A"]),
    M("2074103", "CESSNA", "414A", 5, 1, 2, 7, 0, ["17034"], 6750, 225, (1978, 1985), 1, [X], ["Cessna 414A Chancellor"]),
    M("2074205", "CESSNA", "421C", 5, 1, 2, 8, 0, ["17035"], 7450, 240, (1976, 1985), 1, [X], ["Cessna 421C Golden Eagle"]),
    M("2073712", "CESSNA", "337G", 5, 1, 2, 6, 0, ["17019"], 4630, 180, (1973, 1980), 1, [C], ["Cessna 337G Skymaster"]),
    # turbine
    M("6440008", "PILATUS", "PC-12/45", 4, 2, 1, 9, 0, ["52019"], 9921, 300, (1996, 2007), 2, [C], ["Pilatus PC-12/45"]),
    M("6440012", "PILATUS", "PC-12/47E", 4, 2, 1, 9, 0, ["52020"], 10450, 310, (2008, 2023), 3, [C], ["Pilatus PC-12 NG", "PC-12/47E"]),
    M("8960701", "SOCATA", "TBM 700", 4, 2, 1, 6, 0, ["52017"], 6578, 300, (1990, 2005), 1, [C], ["Socata TBM 700"]),
    M("8960850", "SOCATA", "TBM 850", 4, 2, 1, 6, 0, ["52018"], 7394, 320, (2006, 2014), 1, [C], ["TBM 850"]),
    M("2460940", "DAHER", "TBM 940", 4, 2, 1, 6, 0, ["52018"], 7394, 330, (2019, 2023), 1, [C], ["Daher TBM 940"]),
    M("7104650", "PIPER", "PA-46-500TP", 4, 2, 1, 6, 0, ["52013"], 5092, 260, (2000, 2020), 1, [C], ["Piper Meridian PA-46-500TP"]),
    M("2074501", "CESSNA", "208", 4, 2, 1, 9, 0, ["52030"], 8000, 200, (1985, 2010), 1, [C], ["Cessna 208 Caravan"]),
    M("2074520", "CESSNA", "208B", 4, 2, 1, 11, 0, ["52031"], 8750, 210, (1986, 2023), 2, [C], ["Cessna 208B Grand Caravan", "C208B"]),
    M("7300110", "QUEST AIRCRAFT", "KODIAK 100", 4, 2, 1, 9, 0, ["52010"], 7255, 200, (2007, 2023), 0.5, [C], ["Quest Kodiak 100"]),
    M("0569001", "BEECH", "C90A", 5, 2, 2, 7, 0, ["52005"], 10100, 280, (1984, 2005), 2, [C], ["King Air C90A"]),
    M("0569010", "BEECH", "C90GTI", 5, 2, 2, 7, 0, ["52033"], 10485, 300, (2008, 2023), 1, [C], ["King Air C90GTi"]),
    M("0569020", "BEECH", "B200", 5, 2, 2, 9, 0, ["52012"], 12500, 310, (1981, 2023), 3, [C], ["King Air B200", "Beech King Air 200"]),
    M("0569035", "BEECH", "B300", 5, 2, 2, 11, 0, ["52015"], 15000, 340, (1990, 2023), 1, [C], ["King Air 350"]),
    M("7103120", "PIPER", "PA-31T", 5, 2, 2, 7, 0, ["52008"], 9000, 280, (1974, 1983), 1, [C], ["Piper Cheyenne II PA-31T"]),
    M("2075301", "CESSNA", "525", 5, 5, 2, 7, 0, ["78001"], 10400, 440, (1993, 2000), 1, [C], ["Cessna CitationJet 525"]),
    M("2075320", "CESSNA", "525A", 5, 5, 2, 8, 0, ["78003"], 12375, 470, (2000, 2006), 1, [C], ["Citation CJ2 525A"]),
    M("2075340", "CESSNA", "525B", 5, 5, 2, 8, 0, ["78005"], 13870, 480, (2004, 2023), 2, [C], ["Citation CJ3 525B", "Cessna Citation CJ3"]),
    M("2075101", "CESSNA", "510", 5, 5, 2, 5, 0, ["52047"], 8645, 390, (2006, 2017), 1, [C], ["Citation Mustang 510"]),
    M("1370501", "EMBRAER", "EMB-500", 5, 5, 2, 6, 0, ["52048"], 10472, 450, (2008, 2023), 1, [C], ["Embraer Phenom 100"]),
    M("4100420", "HONDA AIRCRAFT CO", "HA-420", 5, 5, 2, 6, 0, ["39010"], 10700, 480, (2015, 2023), 1, [C], ["HondaJet HA-420"]),
    M("1370512", "EMBRAER", "EMB-505", 5, 5, 2, 9, 0, ["52045"], 17968, 520, (2009, 2023), 3, [C], ["Embraer Phenom 300", "EMB-505"]),
    M("2075360", "CESSNA", "525C", 5, 5, 2, 9, 0, ["78007"], 17110, 520, (2010, 2023), 2, [C], ["Citation CJ4 525C"]),
    M("6440024", "PILATUS", "PC-24", 5, 5, 2, 10, 0, ["78008"], 18300, 500, (2018, 2023), 1, [C], ["Pilatus PC-24"]),
    M("2075680", "CESSNA", "560XL", 5, 5, 2, 9, 0, ["52046"], 20200, 500, (1998, 2023), 1, [C], ["Citation Excel 560XL"]),
    # rotorcraft (turbine)
    M("0313004", "AIRBUS HELICOPTERS", "AS350B3", 6, 3, 1, 6, 0, ["29501"], 4961, 155, (2000, 2023), 3, [C], ["Airbus AS350 B3", "AStar AS350B3"]),
    M("0313130", "AIRBUS HELICOPTERS", "EC130B4", 6, 3, 1, 7, 0, ["29501"], 5291, 150, (2001, 2017), 1, [C], ["EC130 B4"]),
    M("1182010", "BELL", "407", 6, 3, 1, 7, 0, ["62040"], 5250, 150, (1996, 2023), 2, [C], ["Bell 407"]),
    M("1180614", "BELL", "206L-4", 6, 3, 1, 7, 0, ["62030"], 4450, 130, (1992, 2017), 2, [C], ["Bell 206L-4 LongRanger"]),
    M("1180605", "BELL", "206B", 6, 3, 1, 5, 0, ["62012"], 3200, 120, (1971, 2010), 1, [C], ["Bell 206B JetRanger III"]),
    M("6000369", "MD HELICOPTER INC", "369E", 6, 3, 1, 5, 0, ["62010"], 3000, 135, (1982, 2023), 1, [C], ["MD 500E 369E"]),
    # the glider club's gliders and tow plane
    M("0670038", "SCHWEIZER", "SGS 2-33A", 1, 0, 0, 2, 0, [""], 1040, 55, (1967, 1980), 1, [C], ["Schweizer 2-33A"]),
    M("7102508", "PIPER", "PA-25-235", 4, 1, 1, 1, 0, ["41550"], 2900, 115, (1965, 1978), 1, [B], ["Piper Pawnee PA-25-235"]),
]
BY_CODE = {m["code"]: m for m in CATALOG}
assert len(BY_CODE) == len(CATALOG)


def emitter_of(wt, ta):
    if ta == 6:
        return "A7"
    if ta == 1:
        return "B1"
    return "A1" if wt < 15500 else "A2"


def klass(m):
    """The class an airframe keeps when it is registered as another model."""
    return (m["ta"], m["te"], m["ne"], m["bc"], emitter_of(m["wt"], m["ta"]))


def weight_class(w):
    return "CLASS 1" if w < 12500 else ("CLASS 2" if w < 20000 else "CLASS 3")


CESSNA_SERIAL = {"T182T": ("T182", 5), "182T": ("182", 5), "182S": ("182", 5), "172S": ("172S", 5),
                 "U206G": ("U206", 5), "P210N": ("P210", 5), "A185F": ("185", 5), "310Q": ("310Q", 4),
                 "310R": ("310R", 4), "340A": ("340A", 4), "414A": ("414A", 4), "421C": ("421C", 4),
                 "208": ("208", 5), "208B": ("208B", 4), "525": ("525-", 4), "525A": ("525A", 4), "525B": ("525B", 4),
                 "525C": ("525C", 4), "510": ("510-", 4), "560XL": ("560-", 4)}


def serial(rng, m):
    """A serial number in the manufacturer's style."""
    mfr, model = m["mfr"], m["model"]
    if mfr == "CESSNA":
        pre, k = CESSNA_SERIAL.get(model, ("".join(c for c in model if c.isdigit())[:3], 5))
        return pre + ("%0" + str(k) + "d") % rng.integers(1, 10 ** k - 1 if k == 4 else 82000)
    if mfr == "PIPER":
        if model.startswith("PA-"):
            return "%s-%d%05d" % (model[3:5], rng.integers(7, 9), rng.integers(1000, 99999))
        return "%d" % rng.integers(1000, 22000)
    if mfr == "BEECH":
        pre = {"V35B": "D-", "F33A": "CE-", "A36": "E-", "G36": "E-", "C23": "M-", "C24R": "MC-", "77": "WA-",
               "95-B55": "TC-", "58": "TH-", "76": "ME-", "C90A": "LJ-", "C90GTI": "LJ-", "B200": "BB-",
               "B300": "FL-"}[model]
        return "%s%d" % (pre, rng.integers(100, 2400))
    if mfr == "MOONEY":
        return "%d-%04d" % ({"M20C": 22, "M20E": 21, "M20F": 22, "M20J": 24, "M20K": 25, "M20R": 29,
                             "M20TN": 31}[model], rng.integers(1, 3400))
    if mfr == "DIAMOND":
        return "%s.%03d" % ("40" if "40" in model else "C0", rng.integers(1, 999))
    if mfr in ("VANS", "KITFOX", "ZENITH", "LANCAIR"):
        return "%d" % rng.integers(100, 99999)
    return "%d" % rng.integers(100, 99999)


def relabel(aircraft, dereg, keep):
    """Each airframe's registered model, engine and serial: a catalog model of the airframe's class built in its
    year, weighted by how common the model is in the region and by where and how the airframe is used. Airframes in
    `keep` stay on their simulated model. Deterministic."""
    import fleet as FL
    rng = np.random.default_rng(4767)
    taken = set()

    def pick(a, base, home_kind, role):
        bm = BY_CODE[base]
        k = klass(bm)
        cands = [m for m in CATALOG if klass(m) == k and m["years"][0] <= a["year"] <= m["years"][1]]
        if not cands:
            return bm
        want = []
        if role == "school":
            want = ["school"]
        elif role == "strip" or home_kind == "strip":
            want = ["bush", "vintage"]
        elif home_kind == "vint" or FL.MODEL_BY_CODE[base][9] == "vintage":
            want = ["vintage", "bush"]
        elif home_kind == "tower":
            want = ["complex", "general"]
        w = np.array([m["pop"] * (3.0 if any(g in m["groups"] for g in want) else (1.0 if not want else 0.35))
                      for m in cands], float)
        return cands[int(rng.choice(len(cands), p=w / w.sum()))]

    import world as W
    for a in aircraft:
        if a["id"] in keep:
            m = BY_CODE[a["model"]]
            a["reg_model"], a["reg_serial"] = m["code"], a["serial"]
        else:
            home = a["home"]
            if home in W.TOWERED:
                kind = "tower"
            elif home in W.BY_LID:
                kind = W.BY_LID[home]["kind"]
            elif home is not None:
                kind = "strip"
            else:
                kind = None
            m = pick(a, a["model"], kind, a["role"])
            a["reg_model"] = m["code"]
            s = serial(rng, m)
            while (s, m["code"]) in taken:
                s = serial(rng, m)
            a["reg_serial"] = s
        taken.add((a["reg_serial"], a["reg_model"]))
        engs = BY_CODE[a["reg_model"]]["eng"]
        a["reg_engine"] = engs[int(rng.integers(0, len(engs)))] if len(engs) > 1 else engs[0]
    for r in dereg:
        o = r["a"]
        if o.get("id") is not None or "reg_model" in o:
            continue
        m = pick(o, o["model"], None, "filler")
        o["reg_model"] = m["code"]
        s = serial(rng, m)
        while (s, m["code"]) in taken:
            s = serial(rng, m)
        o["reg_serial"] = s
        taken.add((s, m["code"]))
        engs = m["eng"]
        o["reg_engine"] = engs[int(rng.integers(0, len(engs)))] if len(engs) > 1 else engs[0]
