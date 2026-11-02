"""The clean truth of the world, before any file is written: the candidates and their standing, the May 2026 sitting
(choices, part marks, the committee's moves, the borderline re-marks, the results as issued, the reviews and their
fees), and the November 2026 sitting (entries, portal accounts, requests, withdrawals, absences, choices and part
marks). pack.py writes the files; nothing here is shipped as it stands."""
import datetime as dt

import numpy as np

import estimators as E
import params as P

D = dt.date
TD = dt.timedelta

# ---------------------------------------------------------------------------------------------------------------
# name pools (Australian candidate mix)
ANGLO_FAMILY = ["Smith", "Jones", "Williams", "Wilson", "Taylor", "Johnson", "White", "Martin", "Anderson",
                "Thompson", "Walker", "Harris", "Ryan", "Robinson", "Kelly", "King", "Davis", "Wright", "Evans",
                "Roberts", "Green", "Hall", "Wood", "Jackson", "Clarke", "Lewis", "Hill", "Mitchell", "Young",
                "Morris", "Cooper", "Ward", "Turner", "Campbell", "Murphy", "Stewart", "Edwards", "Baker", "Allen",
                "Bell", "Scott", "Hughes", "Morgan", "Collins", "Price", "Bennett", "Gray", "Watson", "Kennedy",
                "Russell", "Walsh", "Doyle", "O'Brien", "O'Connor", "McDonald", "McKenzie", "Fraser", "Henderson",
                "Graham", "Reid", "Sullivan", "Burke", "Fitzpatrick", "Gallagher", "Hayes", "Lynch", "Quinn", "Riley",
                "Ross", "Shaw", "Stone", "Webb", "Foster", "Hunt", "Holmes", "Matthews", "Chapman", "Pearce",
                "Lawson", "Marsh", "Fleming", "Dixon", "Crawford", "Hart", "Barnes", "Lambert", "Spencer", "Duffy",
                "Brennan", "Kerr", "Byrne", "Nolan", "Power", "Moloney", "Carroll", "Daly", "Harvey", "Simpson"]
ANGLO_M = ["James", "William", "Jack", "Thomas", "Lachlan", "Daniel", "Matthew", "Benjamin", "Samuel", "Liam",
           "Nicholas", "Ryan", "Michael", "David", "Andrew", "Christopher", "Luke", "Jacob", "Nathan", "Mitchell",
           "Adam", "Scott", "Brendan", "Callum", "Hamish", "Angus", "Riley", "Cooper", "Ethan", "Patrick", "Sean",
           "Timothy", "Craig", "Shane", "Dylan", "Jordan", "Bradley", "Aaron", "Jarrod", "Kieran"]
ANGLO_F = ["Emily", "Chloe", "Jessica", "Sarah", "Hannah", "Olivia", "Sophie", "Emma", "Grace", "Lauren", "Rebecca",
           "Amy", "Kate", "Megan", "Georgia", "Lucy", "Ella", "Isabella", "Charlotte", "Holly", "Rachel", "Natalie",
           "Zoe", "Bianca", "Tahlia", "Jasmine", "Brooke", "Kirsten", "Alison", "Melissa", "Danielle", "Kristy"]
MIDDLE = ["James", "John", "Robert", "Michael", "Peter", "Anne", "Louise", "Marie", "Jane", "Elizabeth", "Rose",
          "Lee", "Alexander", "Edward", "Grace", "Claire"]
GROUPS = {
    "viet": (["Nguyen", "Tran", "Le", "Pham", "Hoang", "Phan", "Vu", "Dang", "Bui", "Do", "Ho", "Ngo", "Duong", "Ly"],
             ["Minh Anh", "Van Duc", "Quang Huy", "Hoang Nam", "Duc Anh", "Thanh Tung", "Van Long", "Minh Tri"],
             ["Thi Hoa", "Ngoc Lan", "Thi Mai", "Bao Chau", "Thanh Tam", "Thu Trang", "Kim Ngan", "Thi Hang"]),
    "chinese": (["Chen", "Wang", "Li", "Zhang", "Liu", "Huang", "Zhou", "Wu", "Lin", "Yang", "Zhao", "Xu", "Sun",
                 "Lam", "Wong", "Chan", "Ng", "Cheung", "Leung", "Tan", "Lim"],
                ["Wei", "Jun", "Hao", "Lei", "Ming", "Kevin", "Jason", "Eric", "Alan", "Tony", "Zhi Hao"],
                ["Mei", "Yan", "Jing", "Michelle", "Vivian", "Jia Hui", "Xin Yi", "Ling", "Cindy", "Amy"]),
    "south_asian": (["Patel", "Singh", "Sharma", "Kumar", "Gupta", "Reddy", "Nair", "Iyer", "Rao", "Shah", "Mehta",
                     "Khan", "Desai", "Joshi", "Perera", "Fernando", "De Silva", "Jayasinghe"],
                    ["Rahul", "Arjun", "Vikram", "Aditya", "Rohan", "Sanjay", "Amit", "Harpreet", "Gurpreet", "Kasun"],
                    ["Priya", "Ananya", "Neha", "Pooja", "Kavya", "Deepa", "Harpreet", "Nimali", "Shreya"]),
    "med": (["Papadopoulos", "Nikolaidis", "Georgiou", "Konstantinidis", "Rossi", "Russo", "Romano", "Esposito",
             "Bianchi", "Ricci", "Marino", "Costa", "Haddad", "Khoury", "Nasser", "Saleh", "Hanna", "Karam"],
            ["Nick", "George", "Con", "Peter", "Anthony", "Marco", "Luca", "Elias", "Rami", "Joseph", "Steven"],
            ["Maria", "Helen", "Daniela", "Sophia", "Nadia", "Christina", "Elena", "Rita", "Joanne"]),
    "filipino": (["Santos", "Reyes", "Cruz", "Bautista", "Garcia", "Mendoza", "Torres", "Ramos", "Villanueva",
                  "Aquino"],
                 ["Mark", "John Paul", "Angelo", "Jerome", "Paolo", "Ramon"],
                 ["Mary Grace", "Kristine", "Rachelle", "Jennifer", "Maricel", "Joy"]),
    "other": (["Kowalski", "Novak", "van der Berg", "de Jong", "Muller", "Schmidt", "Jansen", "Okafor", "Mensah",
               "Ahmadi", "Hosseini", "Yilmaz"],
              ["Tomasz", "Jan", "Pieter", "Lukas", "Chidi", "Kwame", "Ali", "Reza", "Emre"],
              ["Anna", "Katarzyna", "Eva", "Sanne", "Ngozi", "Leila", "Sara", "Elif"]),
}
GROUP_P = [("anglo", 0.62), ("viet", 0.06), ("chinese", 0.10), ("south_asian", 0.09), ("med", 0.07),
           ("filipino", 0.03), ("other", 0.03)]
FIRMS = [
    ("ACC-1042", "Harbourline Building Surveyors Pty Ltd", "harbourline.com.au", 10.0),
    ("ACC-1067", "Certis Approvals Group", "certisapprovals.com.au", 12.5),
    ("ACC-1103", "Westgate Certification Services", "westgatecert.com.au", 10.0),
    ("ACC-1118", "Southern Cross Building Consultants", "scbc.com.au", 0.0),
    ("ACC-1150", "Bayside Private Certifiers", "baysidepc.com.au", 15.0),
    ("ACC-1176", "Gidgee Building Approvals", "gidgeeba.com.au", 10.0),
    ("ACC-1191", "Riverina Compliance Partners", "rivcomply.com.au", 12.5),
    ("ACC-1224", "Kestrel Building Certification", "kestrelbc.com.au", 10.0),
    ("ACC-1240", "Metro Surveying and Certification", "metrosc.com.au", 0.0),
    ("ACC-1263", "Pinnacle Certifiers", "pinnaclecert.com.au", 15.0),
]
MAILS = ["gmail.com", "outlook.com", "bigpond.com", "hotmail.com", "icloud.com", "yahoo.com.au"]


def pick(rng, seq, p=None):
    return seq[int(rng.choice(len(seq), p=p))]


def make_people(n=2600):
    rng = np.random.default_rng(P.SEED_PEOPLE)
    people, seen = [], set()
    groups, probs = [g for g, _ in GROUP_P], np.array([p for _, p in GROUP_P])
    reserved = {("BROWN", "TERRI"), ("NGUYEN", "STEPHANIE"), ("FITZGERALD", "JOSHUA")}
    while len(people) < n:
        g = pick(rng, groups, probs / probs.sum())
        female = rng.random() < 0.34
        if g == "anglo":
            fam = pick(rng, ANGLO_FAMILY)
            if rng.random() < 0.02:
                fam = fam.replace("'", "") + "-" + pick(rng, ANGLO_FAMILY).replace("'", "")
            first = pick(rng, ANGLO_F if female else ANGLO_M)
            given = first + (" " + pick(rng, MIDDLE) if rng.random() < 0.55 else "")
        else:
            fams, ms, fs = GROUPS[g]
            fam = pick(rng, fams)
            given = pick(rng, fs if female else ms)
            if g in ("med", "other", "filipino") and rng.random() < 0.3 and " " not in given:
                given += " " + pick(rng, MIDDLE)
        dob = D(1966, 1, 1) + TD(days=int(rng.integers(0, 365 * 35)))
        key = (norm(fam), norm(given.split()[0]), dob)
        if key in seen or (norm(fam), norm(given.split()[0])) in reserved:
            continue
        seen.add(key)
        people.append({"pid": len(people), "family": fam, "given": given, "female": female, "dob": dob,
                       "theta": float(rng.normal(0, 1)), "group": g})
    # membership: about half the candidates are individual members of the institute
    nums = rng.choice(np.arange(104_000, 189_999), size=n, replace=False)
    for p, num in zip(people, nums):
        p["member_no"] = str(int(num)) if rng.random() < 0.5 else ""
        p["firm"] = pick(rng, FIRMS)[0] if rng.random() < 0.3 else ""
    return people


def norm(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())


# ---------------------------------------------------------------------------------------------------------------
# one sitting's choices and part marks
def sit(rng, thetas, questions, mu, alpha, gamma, b=3.4, sig=2.0, p_four=0.03, part_sd=0.6):
    n, q = len(thetas), len(questions)
    chosen = np.zeros((n, q), bool)
    for i, th in enumerate(thetas):
        u = alpha + gamma * th + rng.gumbel(0, 1, q)
        k = 4 if rng.random() < p_four else 5
        chosen[i, np.argsort(-u)[:k]] = True
    parts = {}
    for j, (_t, mx) in enumerate(questions):
        mx = np.array(mx)
        share = mx / mx.sum()
        lat = mu[j] + b * np.asarray(thetas) + rng.normal(0, sig, n)
        for i in np.where(chosen[:, j])[0]:
            pe = lat[i] * share + rng.normal(0, part_sd, len(mx))
            pm = np.clip(np.rint(pe), 0, mx).astype(int)
            if pm.sum() == 0:
                pm[int(np.argmax(mx))] = 1
            parts[(int(i), j)] = pm
    return chosen, parts


def matrix(parts, n, q):
    m = np.full((n, q), np.nan)
    for (i, j), pm in parts.items():
        m[i, j] = pm.sum()
    return m


# ---------------------------------------------------------------------------------------------------------------
def business_days_after(d, k):
    while k > 0:
        d += TD(days=1)
        if d.weekday() < 5:
            k -= 1
    return d


def stamp_in(rng, day, h0=8.5, h1=17.5):
    mins = int(rng.integers(int(h0 * 60), int(h1 * 60)))
    return dt.datetime(day.year, day.month, day.day) + TD(minutes=mins)


def fee_for(day, kind):
    fy = "2025-26" if day < P.FEE_CHANGE else "2026-27"
    return P.FEES[fy][kind]


class World:
    pass


def build(seed_may=None, seed_nov=None, seed_ops=None):
    w = World()
    w.people = make_people()
    build_may(w, seed_may if seed_may is not None else P.SEED_MAY)
    build_nov_entries(w, seed_ops if seed_ops is not None else P.SEED_OPS)
    build_nov_marks(w, seed_nov if seed_nov is not None else P.SEED_NOV)
    return w


# ---------------------------------------------------------------------------------------------------------------
# May 2026
MAY_MOVES_TRUE = np.array([0, -1, 1, 0, 1, 0, -1, 0], float)
MAY_ALPHA = np.array([0.2, 0.3, 0.1, 0.35, 0.25, 0.3, 0.2, 0.3])
MAY_GAMMA = np.array([0.15, -0.1, 0.1, 0.0, -0.15, 0.1, 0.0, -0.1])


def build_may(w, seed):
    rng = np.random.default_rng(seed)
    people = w.people
    order = rng.permutation(len(people))
    # Paper 2 entrants and Paper 1-only entrants
    n2, n1 = 744, 92
    p2 = [people[i] for i in order[:n2]]
    p1only = [people[i] for i in order[n2:n2 + n1]]
    w.may_pool_used = set(int(i) for i in order[:n2 + n1])
    shares = np.array([c[3] for c in P.CENTRES])
    entries = []
    for p in p2 + p1only:
        c = P.CODES[int(rng.choice(len(P.CODES), p=shares / shares.sum()))]
        first_timer = rng.random() < 0.72
        if p in p1only:
            papers = "1"
        else:
            papers = "1 & 2" if first_timer else "2"
        late = rng.random() < 0.04
        ed = (D(2026, 3, 28) + TD(days=int(rng.integers(0, 13)))) if late else (
            D(2026, 2, 2) + TD(days=int(rng.integers(0, 54))))
        entries.append({"pid": p["pid"], "centre": c, "papers": papers, "entered": ed})
    # withdrawals before the day, then absence on the day (Paper 2 entrants)
    for e in entries:
        e["withdrawn"] = None
        e["sat2"] = False
        if "2" in e["papers"]:
            if rng.random() < 0.046:
                e["withdrawn"] = e["entered"] + TD(days=int(rng.integers(5, max(6, (P.MAY_SITTING - e["entered"]).days - 1))))
            elif rng.random() < 0.033:
                e["sat2"] = False
            else:
                e["sat2"] = True
        if "1" in e["papers"]:
            e["p1_pass"] = bool(rng.random() < 0.68)
    # candidate numbers: per centre block, in entry order
    for c, _n, blk, *_ in P.CENTRES:
        es = sorted([e for e in entries if e["centre"] == c], key=lambda e: (e["entered"], e["pid"]))
        for k, e in enumerate(es):
            e["cand"] = str(blk * 1000 + 1 + k)
    w.may_entries = entries
    sitters = [e for e in entries if e["sat2"]]
    w.may_sitters = sitters
    th = np.array([people[e["pid"]]["theta"] for e in sitters])
    mu = 11.1 - MAY_MOVES_TRUE
    chosen, parts = sit(rng, th, P.MAY_QUESTIONS, mu, MAY_ALPHA, MAY_GAMMA)
    w.may_chosen, w.may_parts0 = chosen, parts
    m0 = matrix(parts, len(sitters), 8)
    # one script delayed in transit: marked after the results were issued
    late_i = int(rng.choice([i for i, e in enumerate(sitters) if e["centre"] == "MEL"]))
    w.may_late = late_i
    m_comm = m0.copy()
    m_comm[late_i] = np.nan
    w.may_moves_raw = E.fe(m_comm)
    w.may_moves = np.rint(w.may_moves_raw).astype(int)
    w.may_fac_raw = E.facility(m_comm)
    w.may_m0 = m0
    # committee: totals on the original marks with the moves
    tot0 = np.nansum(E.apply_moves(m_comm, w.may_moves), axis=1)
    w.may_pass_committee = int((tot0 >= P.PASS_MARK).sum())
    w.may_sat_committee = len(sitters) - 1
    # borderline re-marks (48 and 49 after the moves), whole script, senior examiners, 19 to 26 June
    parts1 = {k: v.copy() for k, v in parts.items()}
    border = [i for i in range(len(sitters)) if i != late_i and tot0[i] in (48, 49)]
    w.may_border = border
    events = []
    for i in border:
        day = D(2026, 6, 19) + TD(days=int(rng.integers(0, 8)))
        while day.weekday() >= 5:
            day += TD(days=1)
        for j in np.where(chosen[i])[0]:
            mx = np.array(P.MAY_QUESTIONS[j][1])
            new = parts1[(i, int(j))].copy()
            for k in range(len(mx)):
                r = rng.random()
                if r < 0.06:
                    new[k] = max(0, new[k] - 1)
                elif r < 0.14:
                    new[k] = min(mx[k], new[k] + 1)
            parts1[(i, int(j))] = new
            events.append(("border", i, int(j), day))
    w.may_parts1 = parts1
    m1 = matrix(parts1, len(sitters), 8)
    m1_issue = m1.copy()
    m1_issue[late_i] = np.nan
    tot1 = np.nansum(E.apply_moves(m1_issue, w.may_moves), axis=1)
    w.may_tot_issue = tot1
    w.may_pass_issue = int((tot1 >= P.PASS_MARK).sum())
    # reviews: failers as issued, more often the nearer they came
    reqs = []
    for i in range(len(sitters)):
        if i == late_i or tot1[i] >= P.PASS_MARK:
            continue
        p_req = min(0.7, max(0.0, 0.02 + 0.07 * (tot1[i] - 38)))
        if rng.random() >= p_req:
            continue
        answered = list(np.where(chosen[i])[0])
        u = rng.random()
        if u < 0.26:
            service, qs = "clerical", []
        else:
            k = 2 if u > 0.80 else 1
            marks_i = np.array([m1[i, j] for j in answered])
            pw = np.exp(-0.25 * (marks_i - marks_i.min()))
            qs = sorted(int(x) for x in rng.choice(answered, size=k, replace=False, p=pw / pw.sum()))
            service = "remark"
        r = rng.random()
        if r < 0.5:
            rd = P.MAY_RELEASE + TD(days=int(rng.integers(0, 4)))
        elif r < 0.94:
            rd = P.MAY_RELEASE + TD(days=int(rng.integers(4, 22)))
        else:
            rd = P.REVIEW_CLOSE + TD(days=int(rng.integers(1, 4)))
        rt = stamp_in(rng, rd, 7.0, 22.5)
        if rd == P.MAY_RELEASE and rt.hour < 10:
            rt = rt.replace(hour=10 + int(rng.integers(0, 6)))
        reqs.append({"i": i, "service": service, "qs": qs, "received": rt})
    reqs.sort(key=lambda r: (r["received"], r["i"]))
    parts2 = {k: v.copy() for k, v in parts1.items()}
    for r in reqs:
        r["declined"] = r["received"].date() > P.REVIEW_CLOSE
        r["rows"] = []
        if r["declined"]:
            r["completed"] = r["received"].date() + TD(days=2)
            continue
        done = business_days_after(r["received"].date(), int(rng.integers(5, 22)))
        r["completed"] = done
        i = r["i"]
        if r["service"] == "remark":
            for j in r["qs"]:
                mx = np.array(P.MAY_QUESTIONS[j][1])
                new = parts2[(i, j)].copy()
                for k in range(len(mx)):
                    x = rng.random()
                    delta = -1 if x < 0.08 else (0 if x < 0.55 else (1 if x < 0.86 else 2))
                    new[k] = int(np.clip(new[k] + delta, 0, mx[k]))
                parts2[(i, j)] = new
                r["rows"].append((j, list(range(len(mx)))))
        else:
            if rng.random() < 0.24:
                answered = list(np.where(chosen[i])[0])
                j = int(rng.choice(answered))
                mx = np.array(P.MAY_QUESTIONS[j][1])
                k = int(rng.integers(0, len(mx)))
                new = parts2[(i, j)].copy()
                new[k] = int(min(mx[k], new[k] + int(rng.integers(2, 4))))
                parts2[(i, j)] = new
                r["rows"].append((j, [k]))
    w.may_parts2 = parts2
    m2 = matrix(parts2, len(sitters), 8)
    m2[late_i] = m0[late_i]
    w.may_m2 = m2
    tot2 = np.nansum(E.apply_moves(m2, w.may_moves), axis=1)
    w.may_tot_final = tot2
    for r in reqs:
        r["changed"] = (not r["declined"]) and tot1[r["i"]] < P.PASS_MARK <= tot2[r["i"]]
    w.may_reviews = reqs
    w.may_events = events
    # payment: an employer account where the candidate's firm holds one, otherwise a card
    firms = {f[0]: f for f in FIRMS}
    for r in reqs:
        p = people[sitters[r["i"]]["pid"]]
        r["account"] = p["firm"] if (p["firm"] and rng.random() < 0.7) else ""
        kind = "remark" if r["service"] == "remark" else "clerical"
        n_units = len(r["qs"]) if kind == "remark" else 1
        r["fee"] = round(fee_for(r["received"].date(), kind) * n_units, 2)
        disc = firms[r["account"]][3] if r["account"] else 0.0
        r["paid"] = round(r["fee"] * (1 - disc / 100.0), 2)
    # web-form typing: the candidate keys the number; a few are transposed
    for r in reqs:
        cand = sitters[r["i"]]["cand"]
        r["typed"] = cand
        if rng.random() < 0.05:
            s = list(cand)
            k = int(rng.integers(1, len(s) - 1))
            s[k], s[k + 1] = s[k + 1], s[k]
            if "".join(s) != cand:
                r["typed"] = "".join(s)
    # May results final (pass after reviews) by person
    w.may_final_pass = {sitters[i]["pid"]: bool(tot2[i] >= P.PASS_MARK) for i in range(len(sitters)) if i != late_i}
    w.may_final_pass[sitters[late_i]["pid"]] = bool(tot2[late_i] >= P.PASS_MARK)


# ---------------------------------------------------------------------------------------------------------------
# November 2026 entries, accounts, requests
def build_nov_entries(w, seed):
    rng = np.random.default_rng(seed)
    people = w.people
    byp = {e["pid"]: e for e in w.may_entries}
    sit_pid = {e["pid"] for e in w.may_sitters}
    changed_pid = {w.may_sitters[r["i"]]["pid"]: r for r in w.may_reviews if r["changed"]}
    nov = []

    def add(pid, centre, papers, entered):
        nov.append({"pid": pid, "centre": centre, "papers": papers, "entered": entered})

    for e in w.may_entries:
        pid, c = e["pid"], e["centre"]
        if rng.random() < 0.08:
            c = P.CODES[int(rng.integers(0, len(P.CODES)))]
        ed = P.NOV_OPEN + TD(days=int(rng.integers(0, 50)))
        p1_need = ("1" in e["papers"]) and not e.get("p1_pass", True)
        if "2" in e["papers"]:
            if pid in sit_pid:
                if not w.may_final_pass[pid]:
                    if rng.random() < 0.68:
                        add(pid, c, "P1,P2" if p1_need else "P2", ed)
                elif pid in changed_pid:
                    r = changed_pid[pid]
                    if rng.random() < 0.55:
                        ed = P.NOV_OPEN + TD(days=int(rng.integers(0, max(1, (r["completed"] - P.NOV_OPEN).days))))
                        add(pid, c, "P1,P2" if p1_need else "P2", ed)
                        nov[-1]["review_pass"] = r["completed"]
                elif p1_need and rng.random() < 0.6:
                    add(pid, c, "P1", ed)
            else:
                if rng.random() < (0.45 if e["withdrawn"] is None else 0.4):
                    add(pid, c, "P1,P2" if p1_need or "1" in e["papers"] else "P2", ed)
        elif p1_need and rng.random() < 0.62:
            add(pid, c, "P1", ed)
    used = set(w.may_pool_used)
    fresh = [p for p in people if p["pid"] not in used]
    rng.shuffle(fresh)
    shares = np.array([c[3] for c in P.CENTRES])
    k = 0
    while sum(1 for x in nov if "P2" in x["papers"]) < 806:
        p = fresh[k]
        k += 1
        c = P.CODES[int(rng.choice(len(P.CODES), p=shares / shares.sum()))]
        late = rng.random() < 0.045
        ed = (P.NOV_CLOSE + TD(days=int(rng.integers(1, 15)))) if late else (
            P.NOV_OPEN + TD(days=int(rng.integers(0, 54))))
        add(p["pid"], c, "P1,P2" if rng.random() < 0.7 else "P2", ed)
    for k2 in range(70):
        p = fresh[k + k2]
        c = P.CODES[int(rng.choice(len(P.CODES), p=shares / shares.sum()))]
        add(p["pid"], c, "P1", P.NOV_OPEN + TD(days=int(rng.integers(0, 54))))
    # portal accounts, membership and names as each candidate types them
    acct_ids = rng.choice(np.arange(10_000, 99_999), size=len(nov) + 40, replace=False)
    w.nov_people = {}
    firms = {f[0]: f for f in FIRMS}
    for x, aid in zip(nov, acct_ids):
        p = people[x["pid"]]
        x["applicant"] = "A26%05d" % int(aid)
        if x["pid"] in w.nov_people:
            continue
        mem = p["member_no"]
        if not mem and x["pid"] in byp and rng.random() < 0.14:
            mem = str(int(rng.integers(190_000, 199_999)))
        elif not mem and x["pid"] not in byp and rng.random() < 0.05:
            mem = str(int(rng.integers(190_000, 199_999)))
        fam = p["family"]
        changed = False
        if p["member_no"] and p["female"] and x["pid"] in byp and rng.random() < 0.06:
            fam = pick(rng, ANGLO_FAMILY)
            changed = True
        given = p["given"]
        if " " in given and p["group"] in ("anglo", "med", "other") and rng.random() < 0.4:
            given = given.split()[0]
        if rng.random() < 0.04:
            fam = fam.upper()
        if "-" in fam and rng.random() < 0.5:
            fam = fam.replace("-", " ")
        first = norm(given.split()[0])
        if p["firm"] and rng.random() < 0.55:
            email = "%s.%s@%s" % (first.lower(), norm(fam).lower(), firms[p["firm"]][2])
        else:
            email = "%s%s%d@%s" % (first.lower()[:1], norm(fam).lower(), int(rng.integers(1, 99)), pick(rng, MAILS))
        w.nov_people[x["pid"]] = {"family": fam, "given": given, "member_no": mem, "email": email,
                                  "surname_changed": changed}
    # a few candidates open a second portal account and enter twice; the office closes the second entry
    dups = []
    singles = [x for x in nov if "P2" in x["papers"] and x["entered"] < D(2026, 10, 2)]
    for x in rng.choice(len(singles), size=8, replace=False):
        o = singles[int(x)]
        d = dict(o)
        d["applicant"] = "A26%05d" % int(acct_ids[len(nov) + len(dups)])
        d["entered"] = o["entered"] + TD(days=int(rng.integers(1, 9)))
        d["duplicate_of"] = o["applicant"]
        d["closed"] = business_days_after(d["entered"], int(rng.integers(2, 12)))
        np_ = dict(w.nov_people[o["pid"]])
        first = norm(np_["given"].split()[0])
        np_["email"] = "%s%s%d@%s" % (first.lower(), norm(np_["family"]).lower()[:3], int(rng.integers(1, 99)),
                                       pick(rng, MAILS))
        d["person_override"] = np_
        dups.append(d)
    nov += dups
    # requests: withdrawals (whole entry or one paper), transfers, adjustments, other service requests
    reqs = []
    for x in nov:
        x["withdrawn_at"] = None
        x["status_changed"] = None
        x["withdraw_paper"] = None
    for x in nov:
        if "duplicate_of" in x:
            continue
        if "review_pass" in x:
            t = stamp_in(rng, x["review_pass"] + TD(days=int(rng.integers(1, 9))), 7, 22)
            reqs.append(withdraw(rng, x, t, x["papers"]))
            continue
        if "P2" in x["papers"]:
            u = rng.random()
            if u < 0.052:
                lo = x["entered"] + TD(days=1)
                span = (D(2026, 11, 6) - lo).days
                if rng.random() < 0.3:
                    day = D(2026, 11, 2) + TD(days=int(rng.integers(0, 5)))
                else:
                    day = lo + TD(days=int(rng.integers(0, max(1, span))))
                t = stamp_in(rng, max(day, lo), 6.5, 23.5)
                reqs.append(withdraw(rng, x, t, x["papers"]))
            elif u < 0.060:
                t = dt.datetime(2026, 11, 7, 5, 40) + TD(minutes=int(rng.integers(0, 190)))
                reqs.append(withdraw(rng, x, t, x["papers"]))
            elif "P1" in x["papers"] and u < 0.080:
                t = stamp_in(rng, x["entered"] + TD(days=int(rng.integers(3, 40))), 7, 22)
                reqs.append(withdraw(rng, x, t, "P1"))
    for x in nov:
        if "duplicate_of" in x or x.get("review_pass"):
            continue
        u = rng.random()
        if u < 0.03:
            new = P.CODES[int(rng.integers(0, len(P.CODES)))]
            if new != x["centre"]:
                t = stamp_in(rng, x["entered"] + TD(days=int(rng.integers(2, 30))), 7, 22)
                reqs.append({"type": "Centre transfer", "x": x, "created": t, "paper": x["papers"],
                             "detail": "%s to %s" % (x["centre"], new), "from": x["centre"], "to": new})
                x["centre"] = new
        elif u < 0.065:
            t = stamp_in(rng, x["entered"] + TD(days=int(rng.integers(1, 25))), 7, 22)
            reqs.append({"type": "Reasonable adjustment", "x": x, "created": t, "paper": x["papers"],
                         "detail": pick(rng, ["25% additional writing time", "rest breaks", "separate room",
                                              "25% additional writing time and rest breaks", "enlarged paper (A3)"])})
        elif u < 0.08:
            t = stamp_in(rng, x["entered"] + TD(days=int(rng.integers(1, 40))), 7, 22)
            reqs.append({"type": pick(rng, ["Tax invoice reissue", "Address change", "Entry confirmation resend"]),
                         "x": x, "created": t, "paper": x["papers"], "detail": ""})
    # processing: the office actions requests on business days; withdrawals sent in the week before the sitting
    # are actioned on the Monday after it
    for r in reqs:
        cd = r["created"].date()
        if r["type"] == "Withdrawal" and D(2026, 11, 2) <= cd <= D(2026, 11, 7):
            r["closed"] = D(2026, 11, 9) + TD(days=int(rng.integers(0, 2)))
        else:
            r["closed"] = business_days_after(cd, int(rng.integers(0, 3))) if cd.weekday() < 5 else \
                business_days_after(cd, 1)
        r["state"] = "Actioned"
        x = r["x"]
        if r["type"] == "Withdrawal":
            if r["paper"] == x["papers"]:
                x["withdrawn_at"] = r["created"]
                x["status_changed"] = r["closed"]
            x["withdraw_paper"] = r["paper"]
    for x in nov:
        if "duplicate_of" in x:
            x["status_changed"] = x["closed"]
    w.nov_requests = reqs
    # attendance: an entry live on the day (not withdrawn before 7 November, Sydney time) sits or is absent
    for x in nov:
        x["sat2"] = False
        if "P2" not in x["papers"] or "duplicate_of" in x:
            continue
        if x["withdrawn_at"] is not None and x["withdrawn_at"].date() < P.NOV_SITTING:
            continue
        if x["withdrawn_at"] is not None:
            continue
        x["sat2"] = rng.random() >= 0.031
    # candidate numbers at the close, per centre in entry order, late entries after
    for c, _n, blk, *_ in P.CENTRES:
        live = [x for x in nov if x["centre"] == c and not (
            x["status_changed"] is not None and x["status_changed"] <= P.NOV_CLOSE)]
        on_time = sorted([x for x in live if x["entered"] <= P.NOV_CLOSE], key=lambda x: (x["entered"], x["applicant"]))
        late = sorted([x for x in live if x["entered"] > P.NOV_CLOSE], key=lambda x: (x["entered"], x["applicant"]))
        seq = blk * 1000 + 1
        for x in on_time + late:
            x["cand"] = str(seq)
            seq += 1
    for x in nov:
        x.setdefault("cand", "")
    w.nov_entries = nov


def withdraw(rng, x, t, paper):
    return {"type": "Withdrawal", "x": x, "created": t, "paper": paper, "detail": ""}


# ---------------------------------------------------------------------------------------------------------------
# November 2026 marks
NOV_MOVES_TRUE = np.array([-1, 1, 0, 1, 0, 3.15, -1, -3.0])
NOV_BASE = 11.3
NOV_ALPHA = np.array([0.35, 0.2, 0.3, 0.1, 0.25, -0.2, 0.3, 0.45])
NOV_GAMMA = np.array([0, 0, 0, 0, 0, 1.6, 0, -1.5])


def build_nov_marks(w, seed):
    rng = np.random.default_rng(seed)
    sitters = sorted([x for x in w.nov_entries if x["sat2"]], key=lambda x: int(x["cand"]))
    w.nov_sitters = sitters
    th = np.array([w.people[x["pid"]]["theta"] for x in sitters])
    mu = NOV_BASE - NOV_MOVES_TRUE
    chosen, parts = sit(rng, th, P.NOV_QUESTIONS, mu, NOV_ALPHA, NOV_GAMMA)
    w.nov_chosen, w.nov_parts = chosen, parts
    w.nov_m = matrix(parts, len(sitters), 8)
    w.nov_seed = seed
