"""The world before any record is written: the candidates of the four 2024 and 2025 entry examinations, their five
component scores as the vendors and the boards produced them, the appointments the 2023 rules made, the academy
grades of those appointed, and (for screening only, never shipped) the academy grade every candidate would have
earned. The people who applied and the two tracking systems' records of them, the officers' examination duty and the
examinations' costs on the city's ledger are built here too."""
import datetime as dt
import zoneinfo

import numpy as np

import common as K

SEED = 270116
ATS_DRAW = 11          # the applicant tracking draw: every administration keeps three or more pairs of each link kind
LEDGER_DRAW = 17       # the ledger draw: every cost per candidate sits a quarter cent or more from a rounding edge
EASTERN = zoneinfo.ZoneInfo("America/New_York")

# the latent correlation of the five components and the academy final average (written, oral, pat, sjt, inventory)
R5 = np.array([[1.0, 0.238, 0.367, 0.174, 0.115],
               [0.238, 1.0, 0.081, 0.267, 0.225],
               [0.367, 0.081, 1.0, 0.191, -0.03],
               [0.174, 0.267, 0.191, 1.0, 0.286],
               [0.115, 0.225, -0.03, 0.286, 1.0]])
VALIDITY = [0.468, 0.383, 0.235, 0.263, 0.284]
N_SAT = (884, 931, 906, 947)          # candidates who completed all five components, by administration
N_PARTIAL = (97, 104, 89, 111)        # sat the written test but not every other component
CLASS_SIZE = {"24-2": 101, "24-3": 96, "25-1": 104, "25-2": 99, "25-3": 97, "25-4": 103, "26-1": 106, "26-2": 98}
VETERAN_SHARE = 0.083


def _clip(x, lo, hi):
    return np.minimum(np.maximum(x, lo), hi)


def candidates(seed=SEED):
    """Every candidate who sat the written test in the four administrations: latent standing on the five components
    and the academy, the observed scores, the appointment rule's outcome and the academy grade."""
    rng = np.random.default_rng([seed, 1])
    Rf = np.eye(6)
    Rf[:5, :5] = R5
    Rf[:5, 5] = Rf[5, :5] = VALIDITY
    L = np.linalg.cholesky(Rf)
    rows = []
    cand_no = 24001
    for k, adm in enumerate(K.ADMIN):
        n_full, n_part = N_SAT[k], N_PARTIAL[k]
        n = n_full + n_part
        Z = rng.standard_normal((n, 6)) @ L.T
        full = np.zeros(n, bool)
        full[rng.permutation(n)[:n_full]] = True
        vet = rng.random(n) < VETERAN_SHARE
        # the written test: two forms, form B three points harder on the raw scale; the scaled score counts
        form = np.where(rng.random(n) < 0.5, "A", "B")
        scaled = _clip(np.round(72 + 9.0 * Z[:, 0] + rng.normal(0, 1.2, n)), 34, 100)
        raw = scaled - np.where(form == "B", 3, 0)
        # the oral board: three members each rating six dimensions 1 to 5
        board_eff = rng.normal(0, 0.18, (n, 3))
        ratings = _clip(np.round(3.05 + 0.82 * Z[:, 1:2, None] + board_eff[:, :, None]
                                 + rng.normal(0, 0.55, (n, 3, 6))), 1, 5)
        absent = rng.random(n) < 0.05
        present = np.ones((n, 3), bool)
        present[absent, rng.integers(0, 3, absent.sum())] = False
        oral = np.array([ratings[i][present[i]].mean() * 20 for i in range(n)])
        # the physical ability test: obstacle course time, a retest for a first failure, the better time counts
        t1 = np.round(221 - 24.0 * Z[:, 2] + rng.normal(0, 7, n), 1)
        retest = t1 > K.PAT_LIMIT
        t2 = np.where(retest, np.round(t1 - 6 + rng.normal(0, 6, n), 1), np.nan)
        best = np.where(retest, np.fmin(t1, t2), t1)
        pat_pts = _clip(np.round(100 - (best - 160) * 0.62), 0, 100)
        # the trial components
        sjt = _clip(np.round(500 + 84 * Z[:, 3] + rng.normal(0, 6, n)), 200, 800)
        dep = _clip(np.round(50 + 10 * Z[:, 4] + rng.normal(0, 0.8, n)), 20, 80)
        # the academy grade every candidate would earn (only the appointed ever earn it)
        acad_all = np.round(_clip(76.5 + 6.8 * Z[:, 5], 41, 99), 1)
        for i in range(n):
            rows.append(dict(adm=adm["code"], k=k, cand=cand_no, full=bool(full[i]), vet=bool(vet[i]),
                             form=form[i], raw=int(raw[i]), written=int(scaled[i]), ratings=ratings[i],
                             present=present[i], oral=float(oral[i]), t1=float(t1[i]),
                             t2=(None if np.isnan(t2[i]) else float(t2[i])), pat_time=float(best[i]),
                             pat=int(pat_pts[i]), pat_pass=bool(best[i] <= K.PAT_LIMIT), sjt=int(sjt[i]),
                             inventory=int(dep[i]), z=Z[i], acad_all=float(acad_all[i])))
            cand_no += 1
        cand_no = (cand_no // 1000 + 1) * 1000 + 1
    sat_flags(rows, seed)
    appoint(rows, seed)
    return rows


def appoint(rows, seed=SEED):
    """The 2023 rules: the final score is 60 per cent of the written test's scaled score and 40 per cent of the oral
    board score, plus five points for a veteran; candidates who passed the physical ability test are listed in
    order of the final score (the written test breaks a tie) and appointed in list order, those failing the
    background or medical review or declining passed over, until the administration's two academy classes are full."""
    rng = np.random.default_rng([seed, 2])
    for adm in K.ADMIN:
        own = [r for r in rows if r["adm"] == adm["code"]]
        for r in own:
            r["final"] = round(K.WEIGHT["written"] * r["written"] + K.WEIGHT["oral"] * r["oral"]
                               + (K.VETERAN_POINTS if r["vet"] else 0.0), 2)
            r["status"] = None
            r["rank"] = None
            r["klass"] = None
        listed = [r for r in own if r["sat"]["oral"] and r["sat"]["pat"] and r["pat_pass"]]
        listed.sort(key=lambda r: (-r["final"], -r["written"], r["cand"]))
        for i, r in enumerate(listed, 1):
            r["rank"] = i
        need = [(c, CLASS_SIZE[c]) for c in adm["classes"]]
        ci, filled = 0, 0
        for r in listed:
            if ci >= len(need):
                r["status"] = "Not reached"
                continue
            u = rng.random()
            if u < 0.072:
                r["status"] = "Passed over - background"
                continue
            if u < 0.096:
                r["status"] = "Declined offer"
                continue
            r["status"] = "Appointed"
            r["klass"] = need[ci][0]
            filled += 1
            if filled == need[ci][1]:
                ci, filled = ci + 1, 0
        for r in own:
            if r["status"] is None:
                if not (r["sat"]["oral"] and r["sat"]["pat"]):
                    r["status"] = "Withdrew"
                else:
                    r["status"] = "Failed physical ability test"
    # the academy: the grade at graduation, or the average at separation for a recruit who left
    rng2 = np.random.default_rng([seed, 3])
    eff = {c: float(rng2.normal(0, 0.6)) for c in K.CLASS_START}
    for r in rows:
        r["acad"] = None
        r["separated"] = None
        if r["status"] == "Appointed":
            g = r["acad_all"] + eff[r["klass"]]
            p_sep = 1 / (1 + np.exp(3.2 + 1.3 * r["z"][5]))
            if rng2.random() < p_sep:
                r["separated"] = int(rng2.integers(3, K.ACADEMY_WEEKS - 2))
                g = g + float(rng2.normal(-1.0, 1.5))
            r["acad"] = round(float(min(max(g, 40.0), 99.0)), 1)


# ---------------------------------------------------------------------------------------------------------------
# who sat which component: a candidate who did not complete the battery sat the written test and some of the rest

def sat_flags(rows, seed=SEED):
    rng = np.random.default_rng([seed, 4])
    p = {"oral": 0.71, "pat": 0.42, "sjt": 0.57, "inventory": 0.55}
    for r in rows:
        if r["full"]:
            r["sat"] = {c: True for c in K.COMPONENTS}
        else:
            s = {"written": True}
            for c in ("oral", "pat", "sjt", "inventory"):
                s[c] = bool(rng.random() < p[c])
            # a partial candidate always missed at least one later component
            if all(s[c] for c in ("oral", "pat", "sjt", "inventory")):
                s[["oral", "pat", "sjt", "inventory"][int(rng.integers(0, 4))]] = False
            r["sat"] = s
    # the two online trial components: who of the partial candidates logged in to each (drawn on their own, so the
    # boards' and the course's attendance above is untouched)
    rng2 = np.random.default_rng([seed, 4, 1])
    for r in rows:
        if r["full"]:
            continue
        s = r["sat"]
        s["sjt"] = bool(rng2.random() < p["sjt"])
        s["inventory"] = bool(rng2.random() < p["inventory"])
        if all(s[c] for c in ("oral", "pat", "sjt", "inventory")):
            s[["sjt", "inventory"][int(rng2.integers(0, 2))]] = False
    return rows


def sat_counts(rows):
    """Candidates who sat each component in each administration."""
    out = {}
    for adm in K.ADMIN:
        own = [r for r in rows if r["adm"] == adm["code"]]
        out[adm["code"]] = {c: sum(1 for r in own if r["sat"][c]) for c in K.COMPONENTS}
    return out


# ---------------------------------------------------------------------------------------------------------------
# names

FIRST_M = """James Michael Robert John David William Richard Joseph Thomas Christopher Daniel Matthew Anthony Mark
Andrew Joshua Kevin Brian Tyler Jacob Nicholas Brandon Justin Ryan Eric Kyle Aaron Adam Nathan Zachary Steven Timothy
Jason Jeffrey Gregory Benjamin Samuel Patrick Alexander Jonathan Jordan Austin Dylan Cody Travis Derek Corey Shane
Seth Logan Caleb Ethan Noah Mason Hunter Cameron Connor Garrett Trevor Blake Dustin Jared Bradley Wesley Grant Chad
Marcus Andre Jamal Darnell Terrence Malik DeShawn Tyrone Cedric Isaiah Elijah Xavier Carlos Luis Jose Miguel Hector
Diego Juan Ricardo Javier Omar Ahmed Abdi Mohamed Hassan Yusuf Minh Duc Hieu Raj Arjun Vikram Sean Kenneth Scott
Jeremy Joel Lucas Evan Gavin Colin Spencer Mitchell Dalton Brett Neil Ross Keith Craig Todd Randy Curtis Lance
Vincent Victor Dominic Anton Nikolai Mateo Gabriel Rafael Damian Devin Darius Quentin Reginald Lamar""".split()
FIRST_F = """Mary Jennifer Jessica Ashley Sarah Emily Amanda Megan Rachel Lauren Brittany Samantha Stephanie Nicole Kayla
Hannah Taylor Alexis Morgan Danielle Courtney Kelsey Amber Heather Melissa Rebecca Chelsea Katherine Elizabeth Allison
Brooke Jordan Kristen Erin Shelby Haley Paige Madison Olivia Abigail Natalie Victoria Alyssa Jasmine Tiana Destiny
Aaliyah Imani Keisha Tamika Monique Maria Ana Gabriela Sofia Daniela Valeria Fatima Amina Hodan Mei Linh Priya
Anjali Leah Caitlin Mackenzie Sydney Jenna Kara Tara Holly Vanessa Andrea Erica Crystal Tiffany Bianca""".split()
LAST = """Smith Johnson Williams Brown Jones Miller Davis Wilson Anderson Taylor Thomas Moore Martin Jackson Thompson
White Harris Clark Lewis Robinson Walker Young Allen King Wright Scott Hill Green Adams Baker Nelson Carter Mitchell
Roberts Turner Phillips Campbell Parker Evans Edwards Collins Stewart Morris Murphy Cook Rogers Morgan Cooper Peterson
Reed Bailey Kelly Howell Ward Cox Richardson Wood Watson Brooks Bennett Gray Hughes Price Sanders Myers Long Ross
Foster Powell Jenkins Perry Russell Sullivan Fisher Hayes Graham Wallace Butler Barnes Coleman Henderson Simmons
Patterson Jordan Reynolds Hamilton Ellis Gibson Marshall Owens Harrison Fox Cole West Hunt Black Stone Palmer Wells
Webb Tucker Porter Hunter Hicks Crawford Henry Boyd Mason Kennedy Warren Dixon Burns Gordon Shaw Holmes Rice Robertson
Freeman Hudson Hart Daniels Knight Ferguson Rose Stephens Weaver Lane Payne Pierce Berry Arnold Wagner Willis Ray
Watkins Olson Carroll Duncan Snyder Hart Cunningham Bradley Lane Andrews Ruiz Harper Fowler Larson Stevens Grant
Spencer Dunn Burke Elliott Chapman Lawrence Hoffman Schmidt Schneider Meyer Weber Becker Schultz Zimmerman Krause
Hartman Lehman Fischer Kaiser Bauer Kuhn Vogel Koch Hahn Keller Wolfe Frank Kramer Sauer Lang Huber Stahl Zeller
Kowalski Nowak Wisniewski Kaminski Lewandowski Zielinski Szymanski Wozniak Dabrowski Kozlowski Mazur Kowalczyk
Novak Horvath Kovacs Toth Szabo Varga Nagy Molnar Balogh Farkas Russo Romano Ricci Marino Greco Bruno Gallo Conti
DeLuca Esposito Costa Mancini Lombardi Moretti Barbieri Fontana Rinaldi Caruso Ferrari Rizzo O'Brien O'Connor
O'Neill Ryan Walsh Byrne Doyle Gallagher Kennedy Lynch McCarthy Quinn Brennan Donovan Fitzgerald Gorman Kearney
Flanagan Garcia Martinez Rodriguez Hernandez Lopez Gonzalez Perez Sanchez Ramirez Torres Flores Rivera Gomez Diaz
Reyes Morales Ortiz Gutierrez Chavez Ramos Mendoza Castillo Vargas Romero Herrera Medina Aguilar Vega Castro
Nguyen Tran Le Pham Hoang Phan Vu Dang Bui Do Patel Shah Desai Mehta Joshi Kim Lee Park Choi Chen Wang Liu Zhang
Okafor Mensah Adeyemi Owusu Abdi Yusuf Ali Hassan Warsame Farah Haddad Khoury Saleh Nasser Washington Jefferson
Banks Gaines Mack Bryant Dawson Stokes Glover Hairston Peoples Merriweather Battle Langston Tolliver Rucker Gilliam
Pruitt Beasley Haynes Barrett Benson Blair Bowman Carlson Chandler Cross Curry Daugherty Dorsey Doss Emerson Ewing
Faulkner Fleming Frazier Fuller Gentry Gill Goodwin Griffin Hale Hampton Hardin Hatfield Hendricks Hensley Hester
Hodge Hogan Holt Hood Horton Houston Ingram Jarvis Kemp Kirby Lowe Lucas Lynn Malone Mann McCoy McDaniel McKinney
Meadows Mercer Moody Morrow Nash Nichols Noble Norris Oakley Osborne Page Parsons Patton Pollard Preston Pugh Ratliff
Reese Rhodes Riggs Riley Rowe Rowland Sampson Sexton Shelton Shepherd Short Sims Slone Spears Sparks Sprague Steele
Strickland Summers Sutton Swanson Tate Terrell Thornton Tipton Todd Townsend Underwood Vance Vaughn Wade Walton
Ware Waters Weeks Wheeler Whitaker Whitfield Wilkins Winters Wyatt Yates Yoder Zook Hershberger Troyer Miller
Stoltzfus Hostetler Gingerich Kauffman
Abbott Acevedo Acosta Akers Albright Alder Alvarado Ambrose Amos Archer Armstrong Ashby Atkins Austin Ayers Babcock
Bachman Bader Baird Baldwin Ball Ballard Barber Barker Barlow Barnett Barr Barron Bartley Barton Bass Bates Baxter Beal
Beck Beckett Bell Bender Bentley Bergman Bishop Blackburn Blackwell Blake Blanton Bolton Bond Booth Bowen Bowers Boyle
Brady Bragg Brandt Bray Brewer Briggs Britt Brock Brooks Browning Buck Buckley Bullock Burch Burgess Burnett Burton
Bush Byers Cain Caldwell Calhoun Callahan Cameron Cannon Cantrell Carey Carney Carr Carver Case Cash Chambers Chaney
Childers Christensen Church Clay Clayton Clements Cline Cobb Cochran Coffey Combs Compton Conley Conner Conrad Cope
Copeland Corbett Cotton Covington Craft Crane Crowley Culver Cummings Dalton Darby Davidson Dean Decker Delaney Denton
Dickerson Dickson Dillon Dodson Donnelly Dougherty Downey Drake Driscoll Duffy Dugan Durham Dyer Eaton Eckert Eldridge
Ellison England English Erickson Estep Everett Farley Farmer Feltner Fields Finch Finley Fitch Fletcher Flynn Forbes
Ford Foreman Foust Francis Franklin Fry Fulton Gaither Gallo Gamble Gardner Garner Garrett Gates Geiger Gibbs Gilbert
Gilmore Givens Goff Golden Goode Gough Graves Greer Gregg Grimes Gross Grove Hager Haines Hall Hammond Hancock Hanna
Hansen Hardy Harmon Hawkins Hayden Heath Helms Hendrix Herman Hess Hickman Hinton Hobbs Hoover Hopkins Horn Howard
Huff Hull Humphrey Hurst Hutchinson Irwin Jacobs James Jennings Joyner Justice Kane Keene Keith Kendall Kerr Kidd
Kincaid Kinney Kirk Kline Knapp Knox Lamb Lambert Landis Larkin Lawson Leach Leonard Lester Lindsey Little Livingston
Lloyd Logan Love Lucero Lutz Lyons Maddox Manning Marsh Massey Mathews Maxwell May Maynard McBride McClain McCormick
McCullough McGee McGuire McIntyre McKay McKee McLean McMahon McNeil Mead Means Middleton Miles Miner Monroe Montgomery
Moon Morton Moss Mueller Mullins Munoz Murray Nance Neal Newman Newton Nolan Norman Norton Oliver Orr Osborn Pace Pack
Parks Parrish Peck Pennington Perkins Pickett Pitts Poole Pope Potter Pratt Pruett Quinlan Raines Randall Rankin
Ransom Reid Rich Richards Ritchie Roach Robbins Rodgers Rollins Roth Rush Salyer Sargent Saunders Savage Schaefer
Schroeder Sears Sharp Shepard Sherman Shields Shipley Shirley Simon Simpson Skaggs Slater Small Solomon Sowers Stanley
Stark Steiner Stephenson Stout Strong Stroud Stuart Sweeney Talley Tanner Thacker Tillman Trent Trimble Tyler Vincent
Wall Walter Ward Warner Waller Watts Weiss Welch Whitehead Whitley Wiggins Wilcox Wiley Wilder Williamson Witt Wolf
Woodard Woods Workman Wright Wynn Yost Young Zimmer""".split()
LAST = list(dict.fromkeys(LAST))
DOMAINS = (["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "aol.com", "att.net"],
           [0.55, 0.14, 0.09, 0.07, 0.09, 0.04, 0.02])
AREA = (["937", "513", "614", "740", "419", "330"], [0.70, 0.10, 0.08, 0.06, 0.03, 0.03])


def _zipf(n, s):
    w = 1.0 / np.arange(1, n + 1) ** s
    return w / w.sum()


P_FM, P_FF, P_L = _zipf(len(FIRST_M), 0.35), _zipf(len(FIRST_F), 0.35), _zipf(len(LAST), 0.2)


def _phone(rng):
    a = rng.choice(AREA[0], p=AREA[1])
    ex = int(rng.integers(200, 1000))
    while ex == 555 or ex % 100 == 11:
        ex = int(rng.integers(200, 1000))
    return "%s%03d%04d" % (a, ex, int(rng.integers(0, 10000)))


def _email(rng, first, last, dob):
    f, l = first.lower(), last.lower().replace("'", "").replace(" ", "")
    pat = int(rng.integers(0, 6))
    if pat == 0:
        user = "%s.%s%d" % (f, l, int(rng.integers(1, 100)))
    elif pat == 1:
        user = "%s%s%d" % (f[0], l, int(rng.integers(10, 1000)))
    elif pat == 2:
        user = "%s%s%02d" % (f, l, dob.year % 100)
    elif pat == 3:
        user = "%s_%s%d" % (l, f, int(rng.integers(1, 100)))
    elif pat == 4:
        user = "%s.%s.%d" % (f, l, int(rng.integers(100, 10000)))
    else:
        user = "%s%s%d" % (f[:3], l, int(rng.integers(1, 1000)))
    return "%s@%s" % (user, rng.choice(DOMAINS[0], p=DOMAINS[1]))


def _new_email(rng, email, first, last, dob):
    user, dom = email.split("@")
    if rng.random() < 0.5:
        return "%s%d@%s" % (user.rstrip("0123456789"), int(rng.integers(1, 100)), dom)
    other = [d for d in DOMAINS[0] if d != dom]
    return "%s@%s" % (user, other[int(rng.integers(0, len(other)))])


def _swap(d):
    """A date of birth read month first when it was entered day first (both 12 or under, so it parsed)."""
    if d.day <= 12 and d.day != d.month:
        return dt.date(d.year, d.day, d.month)
    return d


# ---------------------------------------------------------------------------------------------------------------
# the people who applied and the tracking systems' records

N_PEOPLE = (2141, 2263, 2058, 2307)       # distinct people with an entry application in the window, by administration
LATERAL_N = (34, 41, 37, 83)              # people on the lateral entry postings, by administration
LEGACY_SOURCES = (["Web", "Mobile", "Career fair kiosk"], [0.58, 0.27, 0.15])
NEW_SOURCES = (["Web", "Mobile app", "Career fair batch"], [0.60, 0.25, 0.15])
SWAPPING = {"Mobile", "Career fair batch"}
LEGACY_POSTING = {"2024-1": ("PO-24-0116", "PO-24-0117"), "2024-2": ("PO-24-0715", "PO-24-0716"),
                  "2025-1": ("PO-25-0121", "PO-25-0122")}
NEW_REQ = {"2025-1": ("REQ-2025-0121", "REQ-2025-0122"), "2025-2": ("REQ-2025-0714", "REQ-2025-0715")}
LATERAL_MERGE = dt.datetime(2025, 8, 4, 9, 0)      # the autumn lateral requisition folded into the entry requisition
AUTUMN_CLOSED = dt.datetime(2025, 8, 18, 9, 0)     # the autumn requisition was taken down on the Monday morning


def people(seed=SEED):
    """The people who applied in each administration: entry applicants (N_PEOPLE), lateral applicants, and people who
    only left a draft or applied after the closing time. A person who applies again in a later administration keeps
    their name and date of birth and may have a new email address or phone number."""
    rng = np.random.default_rng([seed, 5, ATS_DRAW])
    P = {}

    def new(kind):
        pid = len(P) + 1
        male = rng.random() < 0.76
        first = rng.choice(FIRST_M, p=P_FM) if male else rng.choice(FIRST_F, p=P_FF)
        last = rng.choice(LAST, p=P_L)
        if kind == "lateral":
            dob = dt.date(1975, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365 * 24)))
        else:
            dob = dt.date(1980, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365 * 24 + 180)))
        P[pid] = dict(pid=pid, first=str(first), last=str(last), dob=dob, male=bool(male),
                      email=_email(rng, str(first), str(last), dob), phone=_phone(rng))
        return pid

    by_adm = {}
    pool = []
    for k, adm in enumerate(K.ADMIN):
        code = adm["code"]
        n = N_PEOPLE[k]
        n_back = int(round(n * 0.13)) if pool else 0
        back = [int(x) for x in rng.choice(pool, size=n_back, replace=False)] if n_back else []
        for pid in back:
            # a returning applicant: a new address or number for some
            if rng.random() < 0.35:
                p = P[pid]
                P[pid] = dict(p, email=_new_email(rng, p["email"], p["first"], p["last"], p["dob"]))
            if rng.random() < 0.20:
                P[pid] = dict(P[pid], phone=_phone(rng))
        fresh = [new("entry") for _ in range(n - n_back)]
        entry = back + fresh
        pool.extend(fresh)
        # emails and phones as they stood for this administration
        snap = {pid: (P[pid]["email"], P[pid]["phone"]) for pid in entry}
        lateral = [new("lateral") for _ in range(LATERAL_N[k])]
        drafts_only = [new("entry") for _ in range(int(round(n * 0.032)))]
        late = [new("entry") for _ in range(26)] if code == "2025-2" else []
        for pid in lateral + drafts_only + late:
            snap[pid] = (P[pid]["email"], P[pid]["phone"])
        by_adm[code] = dict(entry=entry, lateral=lateral, drafts_only=drafts_only, late=late, snap=snap)
    return P, by_adm


def _local_time(rng, adm, day=None, late=False):
    """A submission time in the posting window (Eastern), heavier in the evenings and in the last two days."""
    if late:
        start = dt.datetime.combine(adm["close"] + dt.timedelta(days=1), dt.time(0, 4))
        span = (AUTUMN_CLOSED - start).total_seconds()
        return start + dt.timedelta(seconds=int(rng.integers(0, int(span))))
    span = (adm["close"] - adm["open"]).days
    if day is None:
        day = adm["open"] + dt.timedelta(days=(span - int(rng.integers(0, 2))) if rng.random() < 0.15
                                         else int(rng.integers(0, span + 1)))
    hour = int(rng.choice(np.arange(24), p=_HOURS))
    if day == adm["open"] and hour < 8:
        hour = 8 + int(rng.integers(0, 10))
    return dt.datetime.combine(day, dt.time(hour, int(rng.integers(0, 60)), int(rng.integers(0, 60))))


_H = np.array([1, 1, 0.5, 0.3, 0.3, 0.5, 1.5, 3, 4, 4.5, 4.5, 4.5, 5, 5, 4.5, 4.5, 5, 6, 7, 8, 8.5, 8, 6, 3], float)
_HOURS = _H / _H.sum()


def _utc(local):
    return local.replace(tzinfo=EASTERN).astimezone(dt.timezone.utc).replace(tzinfo=None)


def applications(P, by_adm, seed=SEED):
    """Every application record the two tracking systems hold. Returns (legacy records, new-system records); each record
    carries its true person (pid) and administration, which the writers never ship."""
    rng = np.random.default_rng([seed, 6, ATS_DRAW])
    recs = []

    def record(pid, code, track, t, source, email, phone, status, title=None):
        p = P[pid]
        dob = _swap(p["dob"]) if source in SWAPPING else p["dob"]
        return dict(pid=pid, adm=code, track=track, t=t, source=source, email=email, phone=phone, status=status,
                    first=p["first"], last=p["last"], dob=dob, title=title)

    for k, adm in enumerate(K.ADMIN):
        code = adm["code"]
        g = by_adm[code]
        for track, pids in (("entry", g["entry"]), ("lateral", g["lateral"])):
            for pid in pids:
                email, phone = g["snap"][pid]
                n_rec = 2 if rng.random() < 0.046 else 1
                kind = "resubmitted" if rng.random() < 0.6 else "twice"
                times = sorted(_local_time(rng, adm) for _ in range(n_rec))
                srcs = []
                for j in range(n_rec):
                    system = "legacy" if (code in ("2024-1", "2024-2") or
                                          (code == "2025-1" and times[j].date() < K.ATS_CUTOVER)) else "new"
                    S = LEGACY_SOURCES if system == "legacy" else NEW_SOURCES
                    srcs.append(str(rng.choice(S[0], p=S[1])))
                emails, phones = [email], [phone]
                if n_rec == 2:
                    e2 = _new_email(rng, email, P[pid]["first"], P[pid]["last"], P[pid]["dob"]) \
                        if rng.random() < 0.45 else email
                    cross = (srcs[0] in SWAPPING) != (srcs[1] in SWAPPING)
                    p2 = _phone(rng) if rng.random() < (0.50 if cross else 0.25) else phone
                    d1 = _swap(P[pid]["dob"]) if srcs[0] in SWAPPING else P[pid]["dob"]
                    d2 = _swap(P[pid]["dob"]) if srcs[1] in SWAPPING else P[pid]["dob"]
                    if d1 != d2 and e2 != email and p2 != phone:
                        # the second form was filled from the same phone: nothing links the records otherwise
                        p2 = phone
                    emails.append(e2)
                    phones.append(p2)
                for j in range(n_rec):
                    if n_rec == 1:
                        status = "Withdrawn" if rng.random() < 0.035 else "Submitted"
                    elif kind == "resubmitted":
                        status = "Withdrawn" if j == 0 else "Submitted"
                    else:
                        status = "Submitted"
                    recs.append(record(pid, code, track, times[j], srcs[j], emails[j], phones[j], status))
        # drafts nobody submitted: by applicants who submitted another form, and by people who never submitted
        n_dr = int(round(N_PEOPLE[k] * 0.048))
        for pid in [int(x) for x in rng.choice(g["entry"], size=n_dr, replace=False)] + g["drafts_only"]:
            email, phone = g["snap"][pid]
            t = _local_time(rng, adm)
            system = "legacy" if (code in ("2024-1", "2024-2") or (code == "2025-1" and t.date() < K.ATS_CUTOVER)) \
                else "new"
            S = LEGACY_SOURCES if system == "legacy" else NEW_SOURCES
            recs.append(record(pid, code, "entry", t, str(rng.choice(S[0], p=[0.75, 0.25, 0.0])), email, phone,
                               "Incomplete"))
        for pid in g["late"]:
            email, phone = g["snap"][pid]
            recs.append(record(pid, code, "entry", _local_time(rng, adm, late=True), str(rng.choice(NEW_SOURCES[0][:2])),
                               email, phone, "Submitted"))
    # where each record sits: the legacy system before the cutover, the new system after, the spring 2025
    # legacy records copied into the new system at go-live
    legacy, new = [], []
    cand_ids = {}
    nxt = [118204]

    def cand_id(email, key):
        k2 = email.lower() if email else key
        if k2 not in cand_ids:
            nxt[0] += int(rng.integers(1, 9))
            cand_ids[k2] = "C%07d" % nxt[0]
        return cand_ids[k2]

    recs.sort(key=lambda r: (r["t"], r["pid"]))
    app_no = {}
    app_id = [5204417]
    for r in recs:
        code = r["adm"]
        if code in LEGACY_POSTING and (code != "2025-1" or r["t"].date() < K.ATS_CUTOVER):
            posting = LEGACY_POSTING[code][0 if r["track"] == "entry" else 1]
            app_no[posting] = app_no.get(posting, 0) + 1
            lr = dict(r, system="legacy", posting=posting, app_no=app_no[posting])
            legacy.append(lr)
            if code == "2025-1" and r["status"] != "Incomplete":
                m = dict(r, system="new", migrated=True)
                m["email"] = "" if rng.random() < 0.18 else r["email"]
                m["req"] = NEW_REQ[code][0 if r["track"] == "entry" else 1]
                m["title"] = "Police Officer" if r["track"] == "entry" else "Police Officer - Lateral Entry"
                m["officer"] = ""
                new.append(m)
        else:
            m = dict(r, system="new", migrated=False)
            if code == "2025-1":
                m["req"] = NEW_REQ[code][0 if r["track"] == "entry" else 1]
                m["title"] = "Police Officer" if r["track"] == "entry" else "Police Officer - Lateral Entry"
            else:
                # autumn 2025: the lateral requisition ran until 4 August, then its applications were moved into the
                # entry requisition (keeping the job title they were made under) and laterals applied there
                m["req"] = NEW_REQ[code][0]
                if r["track"] == "lateral" and r["t"] < LATERAL_MERGE:
                    m["title"] = "Police Officer - Lateral Entry"
                else:
                    m["title"] = "Police Officer"
            m["officer"] = "Yes" if r["track"] == "lateral" else "No"
            new.append(m)
    for m in new:
        app_id[0] += int(rng.integers(1, 30))
        m["app_id"] = "A%07d" % app_id[0]
        m["cand_id"] = cand_id(m["email"], "blank-%s" % m["app_id"])
        m["utc"] = _utc(m["t"])
    return legacy, new


def applicant_truth(by_adm):
    """Ask B's answer: the people who submitted an entry application in each administration's window."""
    return {code: len(set(g["entry"])) for code, g in by_adm.items()}


def assign_people(rows, P, by_adm, legacy, new, seed=SEED):
    """The candidates who sat the written test are entry applicants of their administration whose application was still
    standing (not withdrawn); a returning applicant may sit again."""
    rng = np.random.default_rng([seed, 8])
    standing = {}
    entry = {code: set(g["entry"]) for code, g in by_adm.items()}
    for r in legacy + new:
        if r["track"] == "entry" and r["status"] == "Submitted" and not r.get("migrated") and r["pid"] in entry[r["adm"]]:
            standing.setdefault(r["adm"], set()).add(r["pid"])
    for adm in K.ADMIN:
        code = adm["code"]
        own = [r for r in rows if r["adm"] == code]
        pool = sorted(standing[code])
        pick = [int(x) for x in rng.choice(pool, size=len(own), replace=False)]
        for r, pid in zip(own, pick):
            p = P[pid]
            r.update(pid=pid, first=p["first"], last=p["last"], dob=p["dob"])
    return rows


# ---------------------------------------------------------------------------------------------------------------
# the officers' examination duty: oral boards, the physical ability test's course and the written test's security

OUT_OF_SCOPE = [
    dict(code="2023-2", name="Autumn 2023", written=dt.date(2023, 9, 23), boards=(dt.date(2023, 10, 9), dt.date(2023, 10, 20)),
         pat=(dt.date(2023, 10, 28), dt.date(2023, 10, 29)), certified=dt.date(2023, 11, 21), n=948),
    dict(code="2026-1", name="Spring 2026", written=dt.date(2026, 3, 14), boards=(dt.date(2026, 4, 6), dt.date(2026, 4, 17)),
         pat=(dt.date(2026, 4, 25), dt.date(2026, 4, 26)), certified=dt.date(2026, 5, 12), n=1012),
]
PPE0 = dt.date(2023, 7, 8)             # a pay period end (biweekly, Saturdays)
RAISE_FROM = dt.date(2025, 3, 30)      # the FOP agreement's rates paid from this pay period
RETRO = (0.035, 0.0609)                # increases due on 2024 work and on January to March 2025 work
WKD = 1.25                             # weekend differential, an hour


def ppe(day):
    n = (day - PPE0).days
    return PPE0 + dt.timedelta(days=((n + 13) // 14) * 14)


def board_days(adm):
    d, out = adm["boards"][0], []
    while d <= adm["boards"][1]:
        if d.weekday() < 6:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def duty(rows, seed=SEED):
    """Every examination shift: the oral board panels (two sworn officers and a community panelist, fourteen interviews
    a weekday, ten on a Saturday), the course officers at the physical ability test and the written test's security,
    for the four trial administrations and the two either side. Returns (shifts, the oral board panel of each
    candidate who sat it)."""
    rng = np.random.default_rng([seed, 9])
    badges = sorted(int(x) for x in rng.choice(np.arange(1104, 2470), size=58, replace=False))
    base = {b: round(float(rng.uniform(33.40, 46.10)), 2) for b in badges}
    cps = ["CP-%02d" % i for i in range(1, 17)]
    shifts, panel_of = [], {}
    adms = [dict(a, n=None) for a in K.ADMIN] + OUT_OF_SCOPE
    for adm in adms:
        days = board_days(adm)
        own = [r for r in rows if r["adm"] == adm["code"] and r["sat"]["oral"]] if adm.get("n") is None else None
        n = len(own) if own is not None else int(round(adm["n"] * 0.95))
        cap = {d: (10 if d.weekday() == 5 else 14) for d in days}
        npan = int(np.ceil(n / sum(cap.values())))
        slots = [(d, chr(65 + j)) for d in days for j in range(npan)]
        tot = sum(cap[d] for d, _ in slots)
        load = [int(np.floor(n * cap[d] / tot)) for d, _ in slots]
        for i in range(n - sum(load)):
            load[i % len(load)] += 1
        order = list(rng.permutation(own)) if own is not None else [None] * n
        pos = 0
        for (d, pan), m in zip(slots, load):
            offs = [int(x) for x in rng.choice(badges, size=2, replace=False)]
            cp = cps[int(rng.integers(0, len(cps)))]
            for b in offs:
                shifts.append(dict(adm=adm["code"], cc="4412", day=d, badge=b, hours=7.0 if d.weekday() == 5 else 8.5,
                                   rate=base[b], duty="Oral board"))
            shifts.append(dict(adm=adm["code"], cc="4412", day=d, badge=cp, hours=0.0, rate=0.0, duty="Panelist"))
            for r in order[pos:pos + m]:
                if r is not None:
                    panel_of[r["cand"]] = dict(day=d, panel=pan, members=[offs[0], offs[1], cp])
            pos += m
        for d in (adm["pat"][0], adm["pat"][1]):
            for b in rng.choice(badges, size=6, replace=False):
                shifts.append(dict(adm=adm["code"], cc="4413", day=d, badge=int(b), hours=9.5, rate=base[int(b)],
                                   duty="Physical ability test"))
        for b in rng.choice(badges, size=4, replace=False):
            shifts.append(dict(adm=adm["code"], cc="4411", day=adm["written"], badge=int(b), hours=6.0,
                               rate=base[int(b)], duty="Written test security"))
    for s in shifts:
        if s["duty"] == "Panelist":
            continue
        r = s["rate"] * ((1 + RETRO[0]) * (1.03) if s["day"] >= RAISE_FROM else 1.0)
        s["ot"] = round(s["hours"] * 1.5 * r, 2)
        s["wkd"] = round(s["hours"] * WKD, 2) if s["day"].weekday() >= 5 else 0.0
        due = RETRO[0] if dt.date(2024, 1, 1) <= s["day"] <= dt.date(2024, 12, 31) else \
            (RETRO[1] if dt.date(2025, 1, 1) <= s["day"] < RAISE_FROM else 0.0)
        s["retro"] = round(s["hours"] * 1.5 * s["rate"] * due, 2)
    return shifts, panel_of


# ---------------------------------------------------------------------------------------------------------------
# the examinations' costs on the general ledger, July 2023 to September 2026

def fy_period(d):
    fy = d.year + 1 if d.month >= 7 else d.year
    return "FY%02d-P%02d" % (fy % 100, (d.month - 7) % 12 + 1)


SPRING_ACCRUED = {dt.date(2024, 6, 30): "2024-1", dt.date(2025, 6, 30): "2025-1", dt.date(2026, 6, 30): "2026-1"}


def ledger(rows, shifts, seed=SEED):
    """Every line on cost centres 4410 to 4415 from July 2023 to September 2026. The city's financial system was
    replaced on 1 July 2024: the old system's year-end accruals at 30 June 2024 were carried over as a balance and
    reversed by Finance in one line on the section's administration cost centre; from FY2025 the new system relieves
    an accrual when the invoice is matched to it, so the invoice posts only its difference from the accrual."""
    rng = np.random.default_rng([seed, 7, LEDGER_DRAW])
    counts = sat_counts(rows)
    L = []
    doc = {"old": 318, "new": 4417}

    def add(day, cc, account, vendor, amount, narration, source, ref=None, adm=None, kind="cost", po=""):
        L.append(dict(date=day, cc=cc, account=account, vendor=vendor, amount=round(float(amount), 2),
                      narration=narration, source=source, ref=ref, adm=adm, kind=kind, po=po))

    po_seq = [24100]

    def po():
        po_seq[0] += int(rng.integers(3, 40))
        return "PO-%d" % po_seq[0]

    def accrued_invoice(code, service_day, cc, account, vendor, amount, narration, inv_ref):
        """A spring invoice: on time, or still to come at 30 June and accrued."""
        ye = dt.date(service_day.year, 6, 30)
        p = po()
        if ye in SPRING_ACCRUED and SPRING_ACCRUED[ye] == code:
            est = round(amount * float(rng.uniform(0.93, 1.08)), -2)
            add(ye, cc, account, vendor, est, "YE accrual - %s" % narration, "GJ", adm=code, kind="accrual", po=p)
            inv_day = ye + dt.timedelta(days=int(rng.integers(9, 48)))
            if ye.year == 2024:
                add(inv_day, cc, account, vendor, amount, narration, "AP", inv_ref, adm=code, po=p)
            else:
                add(inv_day, cc, account, vendor, round(amount - est, 2), narration, "AP", inv_ref, adm=code,
                    kind="relief", po=p)
            return est
        add(service_day, cc, account, vendor, amount, narration, "AP", inv_ref, adm=code, po=p)
        return 0.0

    adms = [dict(a, trial=True, n_w=counts[a["code"]]["written"]) for a in K.ADMIN] + \
           [dict(a, trial=False, n_w=a["n"]) for a in OUT_OF_SCOPE]
    reversal = 0.0
    for adm in adms:
        code, name = adm["code"], adm["name"]
        yr = adm["written"].year
        rate_w = {2023: 33.75, 2024: 34.50, 2025: 35.40, 2026: 36.20}[yr]
        fee_w = {2023: 1200.0, 2024: 1250.0, 2025: 1300.0, 2026: 1300.0}[yr]
        spring = adm["written"].month < 6
        hss = adm["n_w"] * rate_w + fee_w
        inv_day = adm["written"] + dt.timedelta(days=int(rng.integers(30, 44)))
        a = accrued_invoice(code, inv_day if not spring else adm["written"] + dt.timedelta(days=150), "4411",
                            "5320 Testing services", "Halvorsen Selection Systems", hss,
                            "HSS written test administration and scoring, %s" % name,
                            "HSS")
        if code == "2024-1":
            reversal += a
        add(adm["written"] - dt.timedelta(days=int(rng.integers(20, 45))), "4411", "5410 Facility rental",
            "Kessling Convention Center", float(rng.uniform(6200, 7400)), "Written test hall, %s" % name, "AP", adm=code)
        n_pan = sum(1 for s in shifts if s["adm"] == code and s["duty"] == "Panelist")
        a = accrued_invoice(code, adm["boards"][1] + dt.timedelta(days=int(rng.integers(18, 30))) if not spring
                            else adm["boards"][1] + dt.timedelta(days=120), "4412", "5330 Professional services",
                            "Various - community panelists", 150.0 * n_pan,
                            "Community panelist honoraria, %s oral boards" % name, "HON-%s" % code.replace("-", ""))
        if code == "2024-1":
            reversal += a
        rent = float(rng.uniform(4300, 5200))
        a = accrued_invoice(code, adm["pat"][1] + dt.timedelta(days=int(rng.integers(14, 28))) if not spring
                            else adm["pat"][1] + dt.timedelta(days=110), "4413", "5420 Equipment rental",
                            "Kessling State College Athletics", rent,
                            "Agility course and timing equipment, %s physical ability test" % name,
                            "KSC")
        if code == "2024-1":
            reversal += a
        add(adm["pat"][1] + dt.timedelta(days=int(rng.integers(30, 40))), "4413", "5610 Interdepartmental charges",
            "Division of Fire", 2 * 2 * 10 * float(rng.choice([56.0, 57.5, 59.0])),
            "EMS standby %s-%s" % (adm["pat"][0].strftime("%m/%d"), adm["pat"][1].strftime("%m/%d/%Y")), "ID", adm=code)
        if adm["trial"]:
            n = counts[code]
            nap = n["sjt"] * 18.75 + 2500.0
            a = accrued_invoice(code, adm["online"][1] + dt.timedelta(days=int(rng.integers(30, 45))) if not spring
                                else adm["online"][1] + dt.timedelta(days=135), "4414", "5320 Testing services",
                                "Pellwyn Assessment Partners", nap,
                                "Pellwyn SJT trial administration and scoring, %s" % name,
                                "PAP")
            if code == "2024-1":
                reversal += a
            hinv = n["inventory"] * (11.40 if yr == 2024 else 11.70)
            a = accrued_invoice(code, adm["online"][1] + dt.timedelta(days=int(rng.integers(28, 40))) if not spring
                                else adm["online"][1] + dt.timedelta(days=125), "4415", "5320 Testing services",
                                "Halvorsen Selection Systems", hinv, "HSS work style inventory scoring, %s" % name,
                                "HSS")
            if code == "2024-1":
                reversal += a
        # the administration's own costs, shared under the cost rule
        add(adm["written"] + dt.timedelta(days=int(rng.integers(5, 20))), "4410", "5350 Temporary staffing",
            "Kessling Temporary Services", float(rng.uniform(8800, 11900)), "Exam proctors, %s" % name, "AP", adm=code)
        add(adm["written"] - dt.timedelta(days=int(rng.integers(8, 20))), "4410", "5510 Printing and postage", "",
            float(rng.uniform(2100, 3200)), "Candidate notices and admission letters, %s" % name, "AP", adm=code)
        add(adm["certified"] + dt.timedelta(days=int(rng.integers(3, 12))), "4410", "5510 Printing and postage", "",
            float(rng.uniform(900, 1500)), "Eligibility list notices, %s" % name, "AP", adm=code)
    # payroll: sworn overtime and the weekend differential, one line a cost centre a pay period, on the pay date
    pr = {}
    for s in shifts:
        if s["duty"] == "Panelist":
            continue
        key = (ppe(s["day"]), s["cc"])
        pr.setdefault(key, [0.0, set()])
        pr[key][0] += s["ot"] + s["wkd"]
        pr[key][1].add(s["adm"])
    for (pe, cc), (amt, codes) in sorted(pr.items()):
        assert len(codes) == 1
        add(pe + dt.timedelta(days=6), cc, "5110 Overtime - sworn", "", amt,
            "Payroll PPE %s, sworn overtime" % pe.strftime("%m/%d/%Y"), "PR", adm=codes.pop())
    # the FOP agreement's retroactive pay, April 2025, one line a cost centre
    for cc in ("4411", "4412", "4413"):
        amt = sum(s["retro"] for s in shifts if s["cc"] == cc and s["duty"] != "Panelist")
        add(dt.date(2025, 4, 25), cc, "5110 Overtime - sworn", "", amt,
            "Retroactive pay, FOP agreement 2024-2026", "PR", adm="retro")
    # the old system's accrued balance at 30 June 2024, reversed in one line on the administration cost centre
    add(dt.date(2024, 7, 1), "4410", "5320 Testing services", "", -round(reversal, 2),
        "Reversal of FY2024 accrued expenses carried over at conversion", "GJ", adm="2024-1", kind="reversal")
    # a scoring re-run credited by Pellwyn for autumn 2024, and a payment made twice and recovered
    add(dt.date(2025, 1, 23), "4414", "5320 Testing services", "Pellwyn Assessment Partners", -1140.0,
        "Pellwyn credit memo, SJT re-scoring, Autumn 2024", "AP", "PAP-CM-0217", adm="2024-2")
    dup = [l for l in L if l["cc"] == "4410" and l["adm"] == "2025-2" and l["vendor"] == "Kessling Temporary Services"][0]
    add(dup["date"] + dt.timedelta(days=4), "4410", dup["account"], dup["vendor"], dup["amount"], dup["narration"],
        "AP", adm="2025-2")
    add(dup["date"] + dt.timedelta(days=33), "4410", dup["account"], dup["vendor"], -dup["amount"],
        "Duplicate payment recovered, exam proctors Autumn 2025", "AP", adm="2025-2")
    # document numbers in posting order: each system's vouchers and journals, each vendor's own invoice series; the
    # year-end accruals of one 30 June are one journal
    L.sort(key=lambda l: (l["date"], l["cc"], l["narration"], l["amount"]))
    seq = {"V": 312, "INV": 4410, "JV": 207, "JE": 104388, "HSS": 21840, "PAP": 1306, "KSC": 3121}
    journal = {}
    for i, l in enumerate(L):
        old = l["date"] < dt.date(2024, 7, 1)
        r = l["ref"]
        if r in ("HSS", "PAP", "KSC"):
            seq[r] += int(rng.integers(40, 160)) if r == "HSS" else int(rng.integers(3, 30))
            l["ref"] = "%s-%d" % (r, seq[r])
        elif r is None and l["source"] == "GJ":
            key = ("YE", l["date"]) if l["kind"] == "accrual" else i
            if key not in journal:
                k = "JV" if old else "JE"
                seq[k] += int(rng.integers(2, 9))
                journal[key] = ("JV%s-%04d" % (l["date"].strftime("%y"), seq[k])) if old else "JE-%06d" % seq[k]
            l["ref"] = journal[key]
        elif r is None and l["source"] == "PR":
            l["ref"] = "PR%s" % l["date"].strftime("%y%m%d")
        elif r is None and l["source"] == "ID":
            l["ref"] = "IDC-%s" % l["date"].strftime("%y%m")
        elif r is None:
            k = "V" if old else "INV"
            seq[k] += int(rng.integers(2, 19))
            l["ref"] = ("V%s-%05d" % (l["date"].strftime("%y"), seq[k])) if old else "INV-%06d" % seq[k]
        l["period"] = fy_period(l["date"])
    return L


TRIAL = [a["code"] for a in K.ADMIN]


def cost_truth(rows, L):
    """Ask A's answer: each component's cost per candidate who sat it over the four administrations. A component's cost
    is what its work cost: every line on its cost centre for the four administrations, the FY2025 accruals with the
    invoices' differences, the retroactive pay and the credits, but not the FY2024 accruals, which were charged again by
    their invoices and reversed on cost centre 4410; plus 4410's lines for the four administrations (not the
    reversal), shared by testing minutes."""
    own = {c: 0.0 for c in K.COMPONENTS}
    shared = 0.0
    for l in L:
        if l["adm"] not in TRIAL and l["adm"] != "retro":
            continue
        if l["kind"] == "reversal" or (l["kind"] == "accrual" and l["date"].year == 2024):
            continue
        if l["cc"] == "4410":
            shared += l["amount"]
        else:
            c = [k for k, v in K.CC_OF.items() if v == l["cc"]][0]
            own[c] += l["amount"]
    tot_min = sum(K.MINUTES.values())
    counts = sat_counts(rows)
    n = {c: sum(counts[a][c] for a in counts) for c in K.COMPONENTS}
    total = {c: own[c] + shared * K.MINUTES[c] / tot_min for c in K.COMPONENTS}
    return {c: total[c] / n[c] for c in K.COMPONENTS}, total, n, own, shared


def world(seed=SEED):
    rows = candidates(seed)
    P, by_adm = people(seed)
    legacy, new = applications(P, by_adm, seed)
    assign_people(rows, P, by_adm, legacy, new, seed)
    shifts, panel_of = duty(rows, seed)
    L = ledger(rows, shifts, seed)
    return dict(rows=rows, P=P, by_adm=by_adm, legacy=legacy, new=new, shifts=shifts, panel_of=panel_of, L=L)
