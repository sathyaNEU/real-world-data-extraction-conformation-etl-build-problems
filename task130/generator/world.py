"""Identities and the physical stock: holders, groups and their links, sections, buildings and
dwellings. Ownership over time is built in history.py on top of this.
"""
import random

from common import D, SEED, cif, dni, full_ref
from plan import SECTIONS

GROUP_WORD = {"G1": "Barana", "G2": "Xamfrà", "G3": "Finestral", "G4": "Terrat", "G5": "Mitgera",
              "G6": "Cantonera", "G7": "Rajola", "G8": "Escaire", "G9": "Ràfec", "G10": "Andana",
              "G12": "Porxo", "G13": "Arcada", "K1": "Ampit", "K2": "Golfa", "G14": "Trespol",
              "G15": "Cornisa", "G16": "Baluard"}
GROUP_CODE = {"G1": "GT0112", "G2": "GT0127", "G3": "GT0133", "G4": "GT0109", "G5": "GT0150",
              "G6": "GT0162", "G7": "GT0171", "G8": "GT0118", "G9": "GT0141", "G10": "GT0158",
              "G12": "GT0183", "G13": "GT0196", "K1": "GT0141", "K2": "GT0158", "G14": "GT0204",
              "G15": "GT0211", "G16": "GT0225"}
# group -> (formed, dissolved); G9 and G10 took the codes freed by K1 and K2
GROUP_LIFE = {"K1": (D(2019, 3, 4), D(2026, 2, 13)), "K2": (D(2020, 6, 15), D(2026, 2, 20)),
              "G9": (D(2026, 5, 11), None), "G10": (D(2026, 5, 18), None)}
for _g in GROUP_CODE:
    GROUP_LIFE.setdefault(_g, (D(2018, 1, 1) if _g not in ("G14", "G15", "G16") else D(2021, 9, 1), None))
GROUP_LIFE["G3"] = (D(2019, 11, 25), None)
GROUP_LIFE["G7"] = (D(2020, 2, 10), None)
GROUP_LIFE["G13"] = (D(2022, 4, 4), None)

# membership spells: holder -> list of (group, start, end) ; end None = open
MEMBER = {
    "G1a": [("G1", D(2018, 1, 1), None)], "G1b": [("G1", D(2018, 1, 1), None)],
    "G1c": [("G1", D(2021, 6, 1), None)], "X1": [("G1", D(2026, 10, 1), None)],
    "G2a": [("G2", D(2018, 1, 1), None)], "G2b": [("G2", D(2019, 9, 2), None)],
    "G3a": [("G3", D(2019, 11, 25), None)], "G3b": [("G3", D(2019, 11, 25), None)],
    "X2": [("G4", D(2018, 1, 1), D(2026, 11, 15)), ("G3", D(2026, 11, 16), None)],
    "G4a": [("G4", D(2018, 1, 1), None)], "G4b": [("G4", D(2018, 1, 1), None)],
    "G4c": [("G4", D(2023, 3, 1), None)],
    "G5a": [("G5", D(2018, 1, 1), None)], "G5b": [("G5", D(2018, 1, 1), None)],
    "G6a": [("G6", D(2018, 1, 1), None)], "X3": [("G6", D(2018, 1, 1), D(2026, 7, 31))],
    "G7a": [("G7", D(2020, 2, 10), None)],
    "G8a": [("G8", D(2018, 1, 1), None)], "G8b": [("G8", D(2018, 1, 1), None)],
    "G9a": [("G9", D(2026, 5, 11), None)], "G9b": [("G9", D(2026, 5, 11), None)],
    "X5": [("G9", D(2027, 3, 1), None)],
    "G10a": [("G10", D(2026, 5, 18), None)], "G10b": [("G10", D(2026, 5, 18), None)],
    "G10c": [("G10", D(2026, 5, 18), None)],
    "G12a": [("G12", D(2018, 1, 1), None)], "X4": [("G12", D(2018, 1, 1), D(2026, 12, 13))],
    "G13a": [("G13", D(2022, 4, 4), None)],
    "Y1": [("K1", D(2019, 3, 4), D(2026, 2, 13))], "Z1": [("K1", D(2019, 3, 4), D(2026, 2, 13))],
    "Y2": [("K2", D(2020, 6, 15), D(2026, 2, 20))], "Z2": [("K2", D(2020, 6, 15), D(2026, 2, 20))],
    "N14a": [("G14", D(2021, 9, 1), None)], "N14b": [("G14", D(2021, 9, 1), None)],
    "N15a": [("G15", D(2021, 9, 1), None)], "N15b": [("G15", D(2022, 1, 17), None)],
    "N16a": [("G16", D(2021, 9, 1), None)], "N16b": [("G16", D(2021, 9, 1), None)],
}
# when each link change was entered in the register (the switches were filed in September 2026)
LINK_ENTERED = {("X1", "G1"): D(2026, 9, 8), ("X2", "G3"): D(2026, 9, 22), ("X2", "G4"): D(2026, 9, 22),
                ("X3", "G6"): D(2026, 9, 2), ("X4", "G12"): D(2026, 9, 29), ("X5", "G9"): D(2026, 9, 29),
                ("Y1", "K1"): D(2026, 2, 27), ("Z1", "K1"): D(2026, 2, 27), ("Y2", "K2"): D(2026, 3, 4),
                ("Z2", "K2"): D(2026, 3, 4), ("G9a", "G9"): D(2026, 5, 13), ("G9b", "G9"): D(2026, 5, 13),
                ("G10a", "G10"): D(2026, 5, 20), ("G10b", "G10"): D(2026, 5, 20),
                ("G10c", "G10"): D(2026, 5, 20)}

SPECIAL_NAMES = {
    "G1a": "Barana Lloguers SL", "G1b": "Barana Patrimonial SL", "G1c": "Barana Llevant SL",
    "X1": "Habitatges Pilastra SL", "G2a": "Xamfrà Residencial SA", "G2b": "Xamfrà Gestió d'Actius SL",
    "G3a": "Finestral Habitatges SLU", "G3b": "Finestral Lloguer Social SL",
    "X2": "Inversions Llucana SL", "G4a": "Terrat Inversions Immobiliàries SA",
    "G4b": "Terrat Lloguers SL", "G4c": "Terrat Patrimoni Urbà SL", "G5a": "Mitgera Residencial SOCIMI SA",
    "G5b": "Mitgera Habitatges SL", "G6a": "Cantonera Patrimonial SL", "X3": "Gestió Ribot SL",
    "G7a": "Rajola Inversions SA", "G8a": "Escaire Lloguers SL", "G8b": "Escaire Actius SL",
    "G9a": "Ràfec Habitatge SL", "G9b": "Ràfec Gestió SL", "X5": "Pati Interior Lloguers SL",
    "G10a": "Andana Residencial SL", "G10b": "Andana Lloguers SL", "G10c": "Andana Sud SL",
    "G12a": "Porxo Habitatges SL", "X4": "Trespol Castelló SL", "G13a": "Arcada Lloguers SA",
    "Y1": "Ampit Lloguers SL", "Z1": "Ampit Promocions SL", "Y2": "Golfa Patrimonial SL",
    "Z2": "Golfa Residencial SL", "OPH": "Persiana Desenvolupaments SL",
    "N14a": "Trespol Habitatge SA", "N14b": "Trespol Gestió SL", "N15a": "Cornisa Patrimonial SL",
    "N15b": "Cornisa Rentals SL", "N16a": "Baluard Residencial SOCIMI SA", "N16b": "Baluard Lloguer SL",
}
WORDS = ["Aljub", "Arcó", "Biga", "Celler", "Cobert", "Escaleta", "Llinda", "Llosa", "Mirall",
         "Sostre", "Teula", "Volta", "Graonet", "Balconet", "Llucerna", "Fanal", "Portalet", "Replà",
         "Envà", "Bigam", "Carreró", "Pou", "Safareig", "Cisterna", "Lluerna", "Rellotge", "Brocal",
         "Corral", "Estudi", "Terrassa", "Bardissa", "Barrera", "Calaix", "Esglaó", "Llindar",
         "Morter", "Palau", "Pilar", "Sòcol", "Tàpia", "Pedrís", "Pujada", "Rampa", "Revolt",
         "Ronda", "Cercle", "Nucli", "Paret", "Solar", "Taulell", "Vidriera", "Trencadís", "Encaix",
         "Alcova", "Rebost", "Golfeta", "Torreta", "Marquesina", "Cancell", "Barbacana"]
FORMS = ["{w} Lloguers SL", "{w} Patrimonial SL", "Inversions {w} SL", "{w} Habitatges SLU",
         "Gestió {w} SL", "{w} Actius Residencials SL", "Promocions {w} SL", "Residencial {w} SL"]
# private large holders, drawn with guard.py names --geo "Spain, Valencian Community" --seed 130
PERSONS = ["Alfredo Palma", "Fátima Valera", "Cecilio Arteaga", "Brígida Cañellas", "Octavio Sancho",
           "Modesta Boix", "Pía Conesa", "Samuel Calderón", "Domingo Jerez", "Isaac Clemente",
           "Milagros Cobo", "Abril Bosch"]

MUNIS = {"46250": ("València", "46", "YJ27"), "03014": ("Alacant", "03", "YH15"),
         "12040": ("Castelló de la Plana", "12", "YK53"), "46131": ("Gandia", "46", "YJ42"),
         "46244": ("Torrent", "46", "YJ26"), "03065": ("Elx", "03", "YH03"),
         "46220": ("Sagunt", "46", "YJ39"), "46190": ("Paterna", "46", "YJ17"),
         "03031": ("Benidorm", "03", "YH57"), "12135": ("Vila-real", "12", "YK42")}
STREETS = {
    "4625001005": ["C/ de Cavallers", "C/ dels Serrans", "C/ de Roteros", "C/ del Salvador"],
    "4625001012": ["C/ de la Bosseria", "C/ de Quart", "C/ de la Corona", "C/ de Baix"],
    "4625002007": ["C/ de Russafa", "C/ de Cadis", "C/ de Sueca", "C/ de Cuba"],
    "4625002019": ["C/ de Dénia", "C/ de Puerto Rico", "C/ de Sevilla", "C/ de Literat Azorín"],
    "4625011004": ["C/ de la Reina", "C/ de Josep Benlliure", "C/ del Rosari", "C/ de la Barraca"],
    "4625011016": ["C/ de Pescadors", "C/ del Progrés", "C/ de Martí Grajales", "C/ de la Mare de Déu del Sufragi"],
    "4625012009": ["C/ de Pere Aleixandre", "C/ de Bilbao", "C/ de Cristòfol Colom", "C/ de Sant Josep de Calassanç"],
    "4625005013": ["C/ de Sagunt", "C/ de Sant Pau", "C/ de Maximilià Thous", "C/ de Visitació"],
    "4625013021": ["C/ del Doctor Vicent Zaragozá", "C/ de Sant Josep de Pignatelli", "C/ de Ramón Llull", "C/ de Músic Ginés"],
    "0301401008": ["C/ de San Fernando", "C/ de Castaños", "C/ de San Vicente", "C/ de las Navas"],
    "0301402014": ["C/ de Pintor Agrassot", "C/ de García Andreu", "C/ del Músico Tordera", "C/ de Pintor Velázquez"],
    "0301405003": ["C/ de Pintor Murillo", "C/ de Doctor Ramón y Cajal", "C/ de Marqués de Molins", "C/ de Pardo Gimeno"],
    "1204001006": ["C/ d'Enmig", "C/ de Colón", "C/ de Sant Vicent", "C/ dels Cavallers"],
    "1204003011": ["C/ de Sant Roc", "C/ de Herrero", "C/ de la Trinitat", "C/ de Maestrat"],
}


def _company_nif(rng, prov, used, letter="B"):
    while True:
        body = int(prov) * 100000 + rng.randrange(10000, 99999)
        n = cif(letter, body)
        if n not in used:
            used.add(n)
            return n


def _person_nif(rng, used):
    while True:
        n = dni(rng.randrange(18000000, 54999999))
        if n not in used:
            used.add(n)
            return n


def holder_ids():
    """Every holder id the watch plan uses, plus the holders seen only outside the watch list."""
    ids = []
    for s in SECTIONS:
        for h in s["hold"]:
            if h not in ids:
                ids.append(h)
    for h in ["Z1", "Z2", "N14a", "N14b", "N15a", "N15b", "N16a", "N16b"]:
        ids.append(h)
    for i in range(1, 19):
        ids.append(f"nw{i:02d}")
    return ids


def build_holders():
    rng = random.Random(SEED * 7 + 1)
    used = set()
    ids = holder_ids()
    smalls = [h for h in ids if h not in SPECIAL_NAMES]
    rng.shuffle(smalls)
    person_ids = set(sorted(smalls)[::7][:len(PERSONS)])
    words = list(WORDS)
    rng.shuffle(words)
    out = {}
    wi = pi = 0
    for h in ids:
        prov = rng.choice(["46", "46", "46", "03", "03", "12", "28", "08"])
        if h in SPECIAL_NAMES:
            name = SPECIAL_NAMES[h]
            letter = "A" if (" SA" in name or "SOCIMI" in name) else "B"
            nif, kind = _company_nif(rng, prov, used, letter), "J"
        elif h in person_ids:
            name, nif, kind = PERSONS[pi], _person_nif(rng, used), "F"
            pi += 1
        else:
            name = FORMS[wi % len(FORMS)].format(w=words[wi % len(words)])
            wi += 1
            nif, kind = _company_nif(rng, prov, used), "J"
        reg = D(2018, 4, 3) if rng.random() < 0.6 else D(2018 + rng.randrange(0, 6), rng.randrange(1, 13), rng.randrange(1, 28))
        out[h] = {"id": h, "nif": nif, "name": name, "kind": kind, "registered": reg}
    # two holders that left the register before the window (sold below ten in 2023)
    for k, nm in (("old1", "Promocions Sòtera SL"), ("old2", "Isaac Clemente")):
        if nm in [o["name"] for o in out.values()]:
            nm = "Lloguers Barbacana Vella SL"
        out[k] = {"id": k, "nif": _company_nif(rng, "46", used), "name": nm, "kind": "J",
                  "registered": D(2018, 4, 3), "left": D(2023, 6, 30)}
    return out, used


def group_of(h, day):
    """Group key of holder h on a day (None when standalone)."""
    for g, a, b in MEMBER.get(h, []):
        if a <= day and (b is None or day <= b):
            return g
    return None


def build_stock(rng_seed=SEED * 11 + 3):
    """Sections, buildings and dwellings for the watch list. Returns (sections, buildings, dwellings)."""
    rng = random.Random(rng_seed)
    sections, buildings, dwellings = {}, {}, {}
    used_parcels = set()
    for s in SECTIONS:
        code = s["code"]
        muni = code[:5]
        sheet = MUNIS[muni][2]
        sections[code] = {"code": code, "muni": muni, "dist": code[5:7], "N": s["N"], "role": s["role"],
                          "parcels": []}
        left = s["N"]
        streets = STREETS[code]
        while left > 0:
            size = min(left, rng.choice([6, 8, 9, 10, 12, 12, 14, 15, 16, 18, 20, 22, 24, 28, 32]))
            if 0 < left - size < 6:
                size = left
            while True:
                parcel = f"{rng.randrange(1000000, 9999999):07d}{sheet}{rng.randrange(10, 99)}{'ABCDEFGHJKLNPRSTUV'[rng.randrange(18)]}"
                if parcel not in used_parcels:
                    used_parcels.add(parcel)
                    break
            street = streets[len(sections[code]["parcels"]) % len(streets)]
            num = rng.randrange(1, 140)
            year = rng.choice([1902, 1915, 1928, 1934, 1950, 1958, 1962, 1965, 1968, 1971, 1974, 1978,
                               1983, 1990, 1998, 2004, 2007, 2019])
            buildings[parcel] = {"parcel": parcel, "section": code, "units": [], "street": street,
                                 "num": num, "year": year}
            sections[code]["parcels"].append(parcel)
            floors = max(1, (size + 3) // 4)
            per = -(-size // floors)
            u = 0
            for f in range(floors):
                for dpos in range(per):
                    if u == size:
                        break
                    u += 1
                    ref = full_ref(parcel, u)
                    floor = "BJ" if f == 0 and floors > 3 else f"{f + (0 if floors > 3 else 1):02d}"
                    dwellings[ref] = {"ref": ref, "parcel": parcel, "unit": u, "section": code,
                                      "floor": floor, "door": f"{dpos + 1:02d}",
                                      "area": rng.choice(range(42, 131)), "year": year}
                    buildings[parcel]["units"].append(ref)
            left -= size
    return sections, buildings, dwellings, used_parcels
