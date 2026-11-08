"""The ask figures computed from the shipped antidote preparation rows: the golden reconstruction and the careful
solver's routes. Used by build.py, checks.py and ceiling.py (verify.py has its own code path)."""
import csv, os, datetime as dt
from collections import defaultdict

FILE = "hospitals/antidote_preparations_2024-07_2026-10.csv"
HALVES = [("2025 H1", dt.date(2025, 1, 1), dt.date(2025, 6, 30)),
          ("2025 H2", dt.date(2025, 7, 1), dt.date(2025, 12, 31)),
          ("2026 H1", dt.date(2026, 1, 1), dt.date(2026, 6, 30))]
LOADING = (150, 200)               # mg/kg of a first bag: three-bag and two-bag regimens
FOLLOW = {150: [(50, 0.3, 1.6), (100, 0.3, 6.0), (100, 18.5, 22.5)],     # (mg/kg, earliest h, latest h after start)
          200: [(100, 3.0, 5.0), (100, 18.5, 21.5)]}


def load(tgt):
    out = []
    with open(os.path.join(tgt, FILE), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append(dict(h=r["hospital_code"], t=dt.datetime.strptime(r["prepared_local"], "%Y-%m-%d %H:%M"),
                            drug="NAC" if r["product"].startswith("Acetylcysteine") else "DFO", dose=int(r["dose_mg"])))
    return out


def half_of(d):
    for lab, a, b in HALVES:
        if a <= d <= b:
            return lab
    return None


def nac_courses_golden(bags):
    """Each bag either joins an open course whose regimen and weight it fits, or opens a course as a first bag."""
    courses = []
    ambiguous = 0
    by_h = defaultdict(list)
    for b in bags:
        if b["drug"] == "NAC":
            by_h[b["h"]].append(b)
    for h, lst in by_h.items():
        open_ = []
        for b in sorted(lst, key=lambda x: x["t"]):
            fits = []
            for c in open_:
                hrs = (b["t"] - c["start"]).total_seconds() / 3600.0
                for mgkg, lo, hi in FOLLOW[c["load"]]:
                    w = b["dose"] / mgkg
                    if lo <= hrs <= hi and abs(w - c["w"]) <= 0.15 and (mgkg, lo) not in c["used"]:
                        fits.append((c, (mgkg, lo)))
                        break
            if len(fits) > 1:
                ambiguous += 1
            if fits:
                c, role = fits[0]
                c["used"].add(role)
                c["bags"].append(b)
            else:
                # opens a course; its regimen is read from its own followers below
                c = dict(h=h, start=b["t"], first=b, bags=[b], used=set())
                c["load"], c["w"] = None, None
                open_.append(c)
                courses.append(c)
            # resolve regimen of fresh courses: a 200 mg/kg first bag has a 100 mg/kg follower 3-5 h later
            for c2 in open_:
                if c2["load"] is None:
                    c2["load"], c2["w"] = 150, c2["first"]["dose"] / 150.0
            open_ = [c for c in open_ if (b["t"] - c["start"]).total_seconds() < 23 * 3600]
    return courses, ambiguous


def nac_resolve(bags):
    """Golden: try both regimens for every first bag and keep the reading under which every bag is accounted for."""
    by_h = defaultdict(list)
    for b in bags:
        if b["drug"] == "NAC":
            by_h[b["h"]].append(b)
    starts = []
    unexplained = 0
    for h, lst in by_h.items():
        lst = sorted(lst, key=lambda x: x["t"])
        used = [False] * len(lst)
        for i, b in enumerate(lst):
            if used[i]:
                continue
            best = None
            for load in LOADING:
                w = b["dose"] / load
                took = []
                for mgkg, lo, hi in FOLLOW[load]:
                    for j in range(i + 1, len(lst)):
                        if used[j] or j in took:
                            continue
                        hrs = (lst[j]["t"] - b["t"]).total_seconds() / 3600.0
                        if hrs > hi:
                            break
                        if hrs >= lo and abs(lst[j]["dose"] / mgkg - w) <= 0.15:
                            took.append(j)
                            break
                score = len(took)
                if best is None or score > best[0]:
                    best = (score, load, took)
            used[i] = True
            for j in best[2]:
                used[j] = True
            starts.append((h, b["t"]))
        unexplained += used.count(False)
    return starts, unexplained


def dfo_split(bags):
    """Golden: deferoxamine bags of an acute course run on eight-hour bags of one dose; bags for transfusion
    admissions recur on consecutive evenings at one dose and return weeks later."""
    by_h = defaultdict(list)
    for b in bags:
        if b["drug"] == "DFO":
            by_h[b["h"]].append(b)
    acute_courses, chronic_bags = [], []
    acute_bags = []
    for h, lst in by_h.items():
        lst = sorted(lst, key=lambda x: x["t"])
        dose_times = defaultdict(list)
        for b in lst:
            dose_times[b["dose"]].append(b["t"])
        for b in lst:
            # the same dose again 20 to 30 hours later or earlier, or 18 to 40 days apart, is a transfusion night
            ts = dose_times[b["dose"]]
            nightly = any(18 <= abs((t - b["t"]).total_seconds()) / 3600 <= 30 for t in ts if t != b["t"])
            if nightly:
                chronic_bags.append(b)
            else:
                acute_bags.append(b)
        open_ = []
        for b in [x for x in acute_bags if x["h"] == h]:
            hit = None
            for c in open_:
                gap = (b["t"] - c["last"]).total_seconds() / 3600
                if c["dose"] == b["dose"] and 6.5 <= gap <= 9.5:
                    hit = c
                    break
            if hit:
                hit["last"] = b["t"]
                hit["bags"].append(b)
            else:
                c = dict(h=h, start=b["t"], last=b["t"], dose=b["dose"], bags=[b])
                open_.append(c)
                acute_courses.append(c)
    return acute_courses, acute_bags, chronic_bags


def figures_golden(bags):
    starts, unexplained = nac_resolve(bags)
    acute_courses, acute_bags, chronic = dfo_split(bags)
    out = {}
    for lab, a, b in HALVES:
        for h in sorted({x["h"] for x in bags}):
            out[(h, lab)] = dict(
                nac=sum(1 for hh, t in starts if hh == h and a <= t.date() <= b),
                dfo=sum(1 for c in acute_courses if c["h"] == h and a <= c["start"].date() <= b),
                dfo_g=round(sum(x["dose"] for x in acute_bags if x["h"] == h and a <= x["t"].date() <= b) / 1000.0, 2))
    return out, unexplained


# the careful solver's routes ------------------------------------------------------------------------------

def route_rows_over_three(bags):
    out = {}
    for lab, a, b in HALVES:
        for h in sorted({x["h"] for x in bags}):
            n = sum(1 for x in bags if x["drug"] == "NAC" and x["h"] == h and a <= x["t"].date() <= b)
            out[(h, lab)] = int(round(n / 3.0))
    return out


def route_time_clusters(bags, drug, window_h):
    """Bags at one hospital within window_h of a cluster's first bag are one course (the reflex grouping)."""
    out = defaultdict(int)
    by_h = defaultdict(list)
    for b in bags:
        if b["drug"] == drug:
            by_h[b["h"]].append(b)
    for h, lst in by_h.items():
        start = None
        for b in sorted(lst, key=lambda x: x["t"]):
            if start is None or (b["t"] - start).total_seconds() / 3600 > window_h:
                start = b["t"]
                lab = half_of(b["t"].date())
                if lab:
                    out[(h, lab)] += 1
    return out


def route_dose_chains(bags, drug, gap_h):
    """Bags of one dose at one hospital no more than gap_h after the previous one are one course."""
    out = defaultdict(int)
    by_hd = defaultdict(list)
    for b in bags:
        if b["drug"] == drug:
            by_hd[(b["h"], b["dose"])].append(b)
    for (h, dose), lst in by_hd.items():
        last = None
        for b in sorted(lst, key=lambda x: x["t"]):
            if last is None or (b["t"] - last).total_seconds() / 3600 > gap_h:
                lab = half_of(b["t"].date())
                if lab:
                    out[(h, lab)] += 1
            last = b["t"]
    return out


def route_dfo_grams_all(bags):
    out = defaultdict(float)
    for b in bags:
        if b["drug"] == "DFO":
            lab = half_of(b["t"].date())
            if lab:
                out[(b["h"], lab)] += b["dose"] / 1000.0
    return out

