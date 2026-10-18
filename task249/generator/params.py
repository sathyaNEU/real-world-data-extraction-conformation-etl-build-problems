"""task249 constants: the comarca's geometry, the clock, the regional ozone field and each node's head."""
import datetime as dt

SEED = 268
UTC = dt.timezone.utc
START = dt.datetime(2025, 12, 31, 23, tzinfo=UTC)       # first hour of the analysers' record (hour starting, UTC)
END = dt.datetime(2028, 5, 31, 23, tzinfo=UTC)           # last hour of every export (hour starting, UTC)
PPB_TO_UG = 1.996                                        # ozone, 20 degrees C and 101.3 kPa (the regional network)
PPB_TO_UG_25 = 1.962                                     # ozone, 25 degrees C (the slip the call must survive)
BAND = (0.85, 1.15)                                      # the quality plan's span band
WINDOW_LOCAL = (dt.datetime(2028, 4, 6), dt.datetime(2028, 6, 1))     # eight weeks before the list, Europe/Madrid
CAPTURE_LOCAL = (dt.datetime(2027, 11, 1), dt.datetime(2028, 2, 1))   # ask A's period, Europe/Madrid
LIST_DATE = dt.date(2028, 6, 1)
ROUND_DATE = dt.date(2028, 6, 12)
SYN_TAU_H = 72.0
RESID = [            # the residual's components: (sd ppb, e-folding km, hourly persistence)
    (4.0, 18.0, 0.95),   # slow: a sea of cloud or an inversion over part of the comarca
    (5.0, 5.0, 0.30),    # fast: plumes, showers and eddies passing one site and not the next
]
NODE_NOISE = 1.5     # ppb, a head's own hourly noise

# the regional network's four ozone analysers: code, name, km east, km north, lat, lon
ANALYSERS = [
    ("ES4101A", "Alcorna - Parque de la Dehesa", 0.0, 0.0),
    ("ES4102A", "Alcorna - Campus", 2.6, 1.8),
    ("ES4103A", "Torralba del Campo", 19.0, 9.0),
    ("ES4104A", "Villarejo de Mencia", -17.0, -12.0),
]
LAT0, LON0 = 39.62, -3.48     # the comarca's centre (an empty stretch of the plateau)

CENTRE = "Centro de Estudios del Aire de Alcorna"
CENTRE_SHORT = "CEAA"
DOMAIN = "ceaa-alcorna.es"
NETWORK = "Red Regional de Vigilancia de la Calidad del Aire"
NETWORK_DOMAIN = "rrvca-datos.es"
CONTRACTOR = "Servicios Ambientales Mencia S.L."
CONTRACTOR_DOMAIN = "sam-mencia.es"
VENDOR = "Ozonet Sensing"
COORDINATOR = ("Matilde Criado", "mcriado")
TECHNICIAN = ("Adan Ruano", "aruano")
NETWORK_OFFICER = ("Edelmira Urrutia", "eurrutia")
SCIENTIST = ("Paulino Cardona", "pcardona")
