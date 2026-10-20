"""task251 constants: the seed, the organisation, the people and the pack's fixed facts."""
import datetime as dt

SEED = 11
ORG = "ASST Pianura Orientale"
LAB = "SC Medicina di Laboratorio, Presidio di Castelmarne"
POCT_OFFICE = "Ufficio POCT, SC Medicina di Laboratorio"
VENDOR = "Corvenza Medical Italia S.r.l."
METER = "Glyvera GX2"
DMS = "GlyLink"
ANALYZER_A, ANALYZER_B = "Kelvar C600", "Kelvar C900"
HOSPITALS = {"CM": "Presidio di Castelmarne", "RB": "Presidio di Rivobello", "VD": "Presidio di Valdarena"}
SIM_HOSP = {"CM": "CM", "RV": "RB", "VD": "VD"}
PEOPLE = dict(poct="Lorenzo Carfagna", director="Silvestro Fittipaldi", vendor="Adelmo Gori")
VISIT_2028 = (dt.date(2028, 1, 17), dt.date(2028, 1, 21))
LIST_DUE = dt.date(2028, 1, 10)
TOLERANCE = 5.0
