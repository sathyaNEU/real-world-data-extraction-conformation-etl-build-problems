"""The quarter's geography as the city records it: the five-location register the force codes offences to, the city
gazetteer (two of the streets are spelt two ways, as the street naming authority has them), the beat map, and the
licensed premises register the partnership keeps for its own purposes."""
import world as W

REGISTER = "harbourgate_location_register.csv"
GAZETTEER = "kelverstoke_street_gazetteer.csv"
BEATS = "kelverstoke_beat_map.csv"
PREMISES = "harbourgate_licensed_premises.csv"

# location_code, name, street as the register spells it, the street numbers the quarter runs to, beat
REG = [
    ("HG-L01", "Harbourgate Street", "Harbourgate Street", "2", "178", "KC-04"),
    ("HG-L02", "Quayside Multi-Storey", "Quayside", "1", "1", "KC-04"),
    ("HG-L03", "Lamphouse Lane", "Lamphouse Lane", "1", "63", "KC-04"),
    ("HG-L04", "Fishmarket Square", "Fishmarket Square", "1", "28", "KC-05"),
    ("HG-L05", "Netherbow Car Park", "Netherbow Wynd", "14", "14", "KC-05"),
]
CODE = {r[1]: r[0] for r in REG}

# the neighbouring quarter's own registered locations, which the extract catches because it was pulled on the
# street name. The pack ships the Harbourgate page of the register, which is what the tasking agreement names.
CRANSTOUN = ["CR-L02", "CR-L05", "CR-L09"]

# the gazetteer: street_ref, name, locality, status. Two streets carry both spellings the authority has on file.
GAZ = [
    ("USRN-20411", "Harbourgate Street", "Harbourgate", "primary"),
    ("USRN-20411", "Harbour Gate Street", "Harbourgate", "alternative"),
    ("USRN-20417", "Quayside", "Harbourgate", "primary"),
    ("USRN-20423", "Lamphouse Lane", "Harbourgate", "primary"),
    ("USRN-20423", "Lamp House Lane", "Harbourgate", "alternative"),
    ("USRN-20431", "Fishmarket Square", "Harbourgate", "primary"),
    ("USRN-20437", "Netherbow Wynd", "Harbourgate", "primary"),
    ("USRN-20442", "Harbourgate Street", "Cranstoun", "primary"),
    ("USRN-20448", "Trinity Vennel", "Cranstoun", "primary"),
    ("USRN-20455", "Ropework Row", "Cranstoun", "primary"),
    ("USRN-20461", "Baltic Close", "Seabraes", "primary"),
    ("USRN-20468", "Marchmont Pend", "Seabraes", "primary"),
]

BEAT = [
    ("KC-04", "Harbourgate North", "the ferry end of Harbourgate Street, Quayside and Lamphouse Lane"),
    ("KC-05", "Harbourgate South", "Fishmarket Square, Netherbow Wynd and the market colonnade"),
    ("KC-06", "Cranstoun", "Harbourgate Street above 178, Trinity Vennel and Ropework Row"),
    ("KC-11", "Seabraes", "Baltic Close and Marchmont Pend"),
]

PUBS = [
    ("LP-0114", "The Lamphouse", "41 Lamphouse Lane", "02:00", "180"),
    ("LP-0119", "Harbourgate Tap", "88 Harbourgate Street", "01:00", "120"),
    ("LP-0127", "The Fishmarket Bar", "6 Fishmarket Square", "02:00", "240"),
    ("LP-0131", "Netherbow Social Club", "14 Netherbow Wynd", "00:30", "90"),
    ("LP-0138", "Quayside Grill", "2 Quayside", "23:30", "60"),
    ("LP-0144", "The Trinity Vaults", "9 Trinity Vennel", "01:00", "110"),
]


def register_rows():
    return [("location_code", "location_name", "street_name", "number_from", "number_to", "beat_code")] + \
           [list(r) for r in REG]


def gazetteer_rows():
    return [("street_ref", "street_name", "locality", "name_status")] + [list(r) for r in GAZ]


def beat_rows():
    return [("beat_code", "beat_name", "covers")] + [list(r) for r in BEAT]


def premises_rows():
    return [("premises_ref", "premises_name", "address", "terminal_hour", "capacity")] + [list(r) for r in PUBS]
