"""World constants for task229 architecture 2: Corderoy Logistics' eight centres running Thornacre's pick
faces, the count programme, the dates, and the seeds. Every parameter the build tunes lives here."""
import datetime as dt

TASK = "task229"
LINE = 97.0                      # Thornacre 5.1
CYCLE = {"A": 28, "B": 56, "C": 91}
VMEAN = {"A": 60.0, "B": 12.0, "C": 2.5}   # picks a day at the slotting review, before the centre's scale

START = dt.date(2026, 6, 1)      # trading day 0 of the export
F = 189                          # trading days 1 June .. 6 December; the stand-down is the start of day F
BURN = 260                       # burn-in trading days before 1 June
STANDDOWN = dt.datetime(2026, 12, 7, 6, 0)
CLOCKS_BACK = dt.date(2026, 10, 25)   # BST ends at 02:00 local (01:00 UTC)
FREEZE_DAYS = [dt.date(2026, 12, 7) + dt.timedelta(days=i) for i in range(28)]   # 7 Dec .. 3 Jan


def day_date(d):
    return START + dt.timedelta(days=int(d))


# Centre register. Silent, loud and false rates are per 10,000 handlings; cls_vel scales a class's picks a day.
CENTRES = [
    dict(code="HNK", name="Hinckley", country="England", regime="Ambient", depot="T104", n=3580,
         mix=[0.18, 0.27, 0.55], vel=1.05, vsd=0.35, cls_vel={"A": 1.7, "B": 1.0, "C": 1.0},
         silent=0.31, loud=0.8, false=0.4, slip=0.25, seed=4007),
    dict(code="DAV", name="Daventry", country="England", regime="Chilled", depot="T231", n=4030,
         mix=[0.28, 0.40, 0.32], vel=1.10, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=0.46, loud=1.2, false=0.4, slip=0.25, seed=4204),
    dict(code="BEL", name="Bellshill", country="Scotland", regime="Ambient", depot="T118", n=2910,
         mix=[0.22, 0.36, 0.42], vel=1.25, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=0.50, loud=0.6, false=0.4, slip=0.25, seed=4301),
    dict(code="THU", name="Thurrock", country="England", regime="Ambient", depot="T109", n=3360,
         mix=[0.15, 0.30, 0.55], vel=0.95, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=1.60, loud=0.8, false=0.4, slip=0.25, seed=4401),
    dict(code="MAG", name="Magor", country="Wales", regime="Frozen", depot="T352", n=2690,
         mix=[0.10, 0.25, 0.65], vel=0.75, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=0.46, loud=0.35, false=0.4, slip=0.25, seed=4105),
    dict(code="WAR", name="Warrington", country="England", regime="Chilled", depot="T236", n=3810,
         mix=[0.30, 0.42, 0.28], vel=1.10, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=0.52, loud=1.0, false=0.4, slip=0.25, seed=4504),
    dict(code="AVO", name="Avonmouth", country="England", regime="Ambient", depot="T121", n=3140,
         mix=[0.24, 0.34, 0.42], vel=1.05, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=0.60, loud=1.5, false=0.4, slip=0.25, seed=4605),
    dict(code="DON", name="Doncaster", country="England", regime="Frozen", depot="T357", n=3360,
         mix=[0.18, 0.32, 0.50], vel=1.15, vsd=0.35, cls_vel={"A": 1.0, "B": 1.0, "C": 1.0},
         silent=1.35, loud=0.7, false=0.4, slip=0.25, seed=4704),
]
NAMES = [c["name"] for c in CENTRES]
BY_NAME = {c["name"]: c for c in CENTRES}

# Out-of-scope pick faces carried in the count history: held at the stand-down, or released earlier.
HELD_SHARE = 0.009
RELEASED_SHARE = 0.018

PEOPLE = {
    "standard_owner": "Stacey Sykes",      # Thornacre head of replenishment
    "programme_owner": "Arthur Mason",     # Corderoy inventory control manager
    "analyst": "Leonard Finch",            # Corderoy BI analyst, the extract notes
    "account_director": "Rhys Flynn",      # Corderoy account director
}

ASK_SEED = 7229
QTY_SEED = 5229
