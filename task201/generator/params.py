"""task201 world parameters. One place, read by build.py, checks.py and ceiling.py."""
SEED = 20261154
ASOF = "2026-11-16"              # extract date, in fiction
WIN_FROM, WIN_TO = "2026-10-01", "2026-11-15"

CLS = ["SN-magistrala", "SN/nN-stacja", "SN-odgalezienie", "nN-obwod"]
CLS_PL = {"SN-magistrala": "ciag magistralny SN", "SN/nN-stacja": "stacja transformatorowa SN/nN",
          "SN-odgalezienie": "odgalezienie SN na bezpieczniku", "nN-obwod": "obwod nN"}
# Mean minutes from loss of supply to the first customer notification, by section class.
# A trunk de-energises a town centre and the switchboard rings at once; a village station is
# noticed within the half hour; a fused rural spur serving scattered holdings can stand for hours.
DELAY_MIN = {"SN-magistrala": 9.0, "SN/nN-stacja": 18.0, "SN-odgalezienie": 245.0, "nN-obwod": 165.0}
WEIBULL_SHAPE = 3.6             # near-symmetric: mean/median = 0.9996

BRANCH = {
  "ZAN": dict(name="Zanowiec", feeders=230, n_ev=301, inst=0.94,
              mix=[0.26, 0.64, 0.06, 0.04],
              cust=[(1150, 4200), (95, 430), (11, 62), (14, 92)],
              fix=[0.50, 1.55, 2.20, 1.80]),
  "PUS": dict(name="Pustrzyca", feeders=150, n_ev=560, inst=0.07,
              mix=[0.07, 0.84, 0.06, 0.03],
              cust=[(700, 2400), (78, 360), (8, 46), (10, 70)],
              fix=[0.70, 1.25, 2.60, 2.20]),
  "GRB": dict(name="Grabownik", feeders=150, n_ev=4700, inst=0.09,
              mix=[0.004, 0.012, 0.745, 0.239],
              cust=[(190, 720), (22, 110), (2, 19), (4, 27)],
              fix=[1.80, 4.60, 3.15, 2.70]),
  "NIE": dict(name="Nierzyca", feeders=130, n_ev=450, inst=0.58,
              mix=[0.17, 0.65, 0.12, 0.06],
              cust=[(520, 1850), (46, 205), (5, 29), (7, 42)],
              fix=[0.60, 1.90, 3.10, 2.50]),
}
DISTRICTS = {
  "ZAN": ["Zanowiec Miasto", "Zanowiec Polnoc", "Lipowka", "Trzebienie"],
  "PUS": ["Pustrzyca", "Dolna Wierzba", "Kamionki", "Sloneczne"],
  "GRB": ["Grabownik", "Borowa Puszcza", "Zalesie Stare", "Mokrzyce"],
  "NIE": ["Nierzyca", "Osowa Gora", "Przelewy", "Rudno"],
}

# District structure inside each branch: weight of the branch's events, its own telemetry share and
# its own class mix multiplier. The telemetry programme reached the town districts first.
DISTRICT_PROFILE = {
  "ZAN": [("Zanowiec Miasto", 0.42, 1.00, [1.3, 1.1, 0.4, 0.5], 1.00),
          ("Zanowiec Polnoc", 0.26, 0.97, [1.0, 1.1, 0.7, 0.8], 0.95),
          ("Lipowka",         0.19, 0.88, [0.7, 0.9, 1.8, 1.6], 1.10),
          ("Trzebienie",      0.13, 0.84, [0.6, 0.9, 2.1, 1.9], 1.15)],
  "PUS": [("Pustrzyca",       0.31, 0.19, [1.4, 1.1, 0.5, 0.6], 0.90),
          ("Dolna Wierzba",   0.27, 0.05, [0.8, 1.0, 1.3, 1.2], 1.05),
          ("Kamionki",        0.24, 0.03, [0.7, 1.0, 1.4, 1.3], 1.10),
          ("Sloneczne",       0.18, 0.04, [0.9, 1.0, 1.1, 1.1], 0.95)],
  # Borowa Puszcza is forest: the crews reach a fault there in hours, not in minutes, and the
  # dispatch note records the forest roads impassable until midday on 12 November. Mokrzyce sits
  # on the depot's own road, so its many fuse operations are cleared the same hour.
  "GRB": [("Borowa Puszcza",  0.24, 0.02, [0.5, 0.7, 1.18, 0.85], 2.10),
          ("Mokrzyce",        0.40, 0.05, [0.7, 0.9, 1.02, 1.05], 0.25),
          ("Zalesie Stare",   0.22, 0.08, [0.8, 1.0, 0.95, 1.10], 0.70),
          ("Grabownik",       0.14, 0.36, [2.6, 2.4, 0.70, 1.00], 0.55)],
  "NIE": [("Nierzyca",        0.34, 0.80, [1.3, 1.1, 0.5, 0.6], 0.95),
          ("Osowa Gora",      0.26, 0.62, [1.0, 1.0, 0.9, 1.0], 1.00),
          ("Przelewy",        0.22, 0.42, [0.8, 0.9, 1.4, 1.3], 1.10),
          ("Rudno",           0.18, 0.38, [0.7, 0.9, 1.6, 1.5], 1.15)],
}
# Storm episodes: (name, start, end, share of the window's events, branch weights)
EPISODES = [
  ("wichura 11-13.11",  "2026-11-11T09:00", "2026-11-13T22:00", 0.57, {"ZAN":0.7,"PUS":1.0,"GRB":1.35,"NIE":0.8}),
  ("front 02.11",      "2026-11-02T04:00", "2026-11-03T20:00", 0.17, {"ZAN":0.8,"PUS":0.9,"GRB":0.8,"NIE":2.6}),
]
OVERLAP_FROM, OVERLAP_TO = "2026-11-01", "2026-11-07"   # the week both OMS exports carry

# Planned work: the autumn maintenance programme de-energises whole sections to a published
# schedule. Separate `rodzaj` in the dispatch export; the procedure's population is unplanned only.
PLANNED_SHARE = {"ZAN": 0.09, "PUS": 0.14, "GRB": 0.11, "NIE": 0.66}
PLANNED_JOBS = 260
# What the autumn programme actually does at a station, as the work order names it and as the
# dispatcher types it into the outage record. The pool is SN/nN stations, so the scopes are the
# station trades; the weights are the programme's own mix.
PLANNED_SCOPE = [
  ("przeglad stacji SN/nN", "prace planowane - przeglad stacji"),
  ("wymiana odlacznika w stacji SN/nN", "prace planowane - wymiana odlacznika"),
  ("remont rozdzielni nN", "prace planowane - remont rozdzielni nN"),
  ("wymiana przekladnikow i zabezpieczen", "prace planowane - wymiana zabezpieczen"),
  ("wymiana izolatorow na odcinku zasilajacym", "prace planowane - wymiana izolatorow"),
  ("pomiary ochrony przeciwporazeniowej", "prace planowane - pomiary eksploatacyjne"),
  ("przelaczenie zasilania stacji", "przelaczenia ruchowe"),
]
PLANNED_SCOPE_W = [0.34, 0.17, 0.12, 0.11, 0.10, 0.09, 0.07]
# The indices the concession filed for 2024 and 2025, one copy read by the prior-year report and by
# the golden's annexe. 2024 was filed in hours per customer, 2025 in minutes per customer (each
# table says so in its own header). The level is the window's own: a 46-day storm-season stretch
# carrying one major windstorm runs at about two and a half times the annual daily rate.
RET24 = {("SN", "awaryjne"): 1.19, ("SN", "planowane"): 0.49,
         ("nN", "awaryjne"): 0.68, ("nN", "planowane"): 0.26}
SAIFI24 = {("SN", "awaryjne"): 0.98, ("SN", "planowane"): 0.17,
           ("nN", "awaryjne"): 0.66, ("nN", "planowane"): 0.10}
RET25 = {("SN", "awaryjne"): 78.3, ("SN", "planowane"): 31.6,
         ("nN", "awaryjne"): 45.9, ("nN", "planowane"): 17.8}
SAIFI25 = {("SN", "awaryjne"): 1.05, ("SN", "planowane"): 0.19,
           ("nN", "awaryjne"): 0.72, ("nN", "planowane"): 0.11}
PLANNED_MIN = (55, 185)   # a planned switching window is a working morning, not a day
ORPHAN_N = 3400          # notifications tied to no interruption: a neighbour, an own fuse, a query
IVR_GAP = ("2026-10-09", "2026-11-03")   # the IVR prompt change
# Zero padding in device identifiers arrived with the 2024 dispatch upgrade; records whose device
# was commissioned earlier still carry the unpadded form in the export.
UNPADDED_SHARE = {"ZAN": 0.11, "PUS": 0.22, "GRB": 0.52, "NIE": 0.31}
