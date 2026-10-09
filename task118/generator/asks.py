"""The ask layer: the web CMS revision export (headline corrections) and the audience panel (readers)."""
import datetime as dt
import hashlib

import numpy as np

import params as P
import spine as SP
from archive import rng_for

ALPH = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def doc_id(*key):
    h = hashlib.sha1(("|".join(str(k) for k in key)).encode()).digest()
    return "".join(ALPH[b % 32] for b in h[:10])


def hsha(*key):
    return hashlib.sha1(("|".join(str(k) for k in key)).encode()).hexdigest()[:12]


HEAD_NOTES = [
    "Correction: an earlier headline on this article misstated {x}.",
    "Correction: the headline on this story has been amended. It previously misstated {x}.",
    "This article's title was changed to correct {x}.",
    "Amended: the title of this story originally misstated {x}.",
    "Correction: an earlier version of this story gave {x} incorrectly in its headline.",
    "Correction: we have changed the heading on this story, which misstated {x}.",
]
BODY_NOTES = [
    "Correction: an earlier version of this article misstated {x}.",
    "This article was amended to correct {x}.",
    "Correction: {x} was given incorrectly in an earlier version of this story.",
    "Correction: this story previously misstated {x}.",
    "An earlier version of this article incorrectly reported {x}.",
]
SUBJECTS = {
    "POL-N": ["the date of the Senate vote", "the minister's portfolio", "the size of the funding package",
              "the number of crossbench votes", "the year the scheme began", "the name of the electorate",
              "the cost of the program", "the timing of the inquiry's report"],
    "BUS-N": ["the company's annual profit", "the size of the rate rise", "the movement in the share price",
              "the value of the takeover offer", "the date of the annual meeting", "the name of the fund",
              "the number of jobs affected", "the inflation figure"],
    "SPT-N": ["the final score", "the venue of the match", "the player's age", "the length of the suspension",
              "the round of the competition", "the number of goals kicked", "the margin of the win",
              "the club's finishing position"],
    "CUL-N": ["the title of the exhibition", "the author's previous novel", "the festival's opening date",
              "the name of the venue", "the award category", "the running time of the film"],
    "POL-M": ["the date of the state budget", "the number of new hospital beds", "the electorate",
              "the cost of the rail project", "the minister's title"],
    "SPT-M": ["the final score", "the player's age", "the venue", "the length of the suspension",
              "the club's ladder position", "the crowd figure"],
    "LOC-M": ["the suburb where the crash happened", "the council's budget figure", "the road closure dates",
              "the name of the school", "the time of the storm warning", "the number of homes without power",
              "the location of the fire", "the cost of the upgrade"],
}


def fmt(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


class Doc:
    __slots__ = ("id", "desk", "type", "parent", "restored_from", "revs", "art", "live_at")

    def __init__(self, id_, desk, type_, parent="", restored_from="", art=-1):
        self.id, self.desk, self.type, self.parent, self.restored_from = id_, desk, type_, parent, restored_from
        self.revs = []      # (saved_at, status, headline_sha, note)
        self.art = art
        self.live_at = None


def build_cms(W):
    """Every saved revision of every web-desk document first saved in the base year."""
    docs = []
    W.cms_truth = {}
    restore = P.RESTORE_AT
    lookback = restore - dt.timedelta(days=P.RESTORE_LOOKBACK_DAYS)
    end_utc = dt.datetime(P.WINDOW_END.year, P.WINDOW_END.month, P.WINDOW_END.day, 23, 59) - P.AEST
    for d in P.WEB:
        k = P.WEB.index(d)
        rng = rng_for(600 + k)
        A = W.art[d]
        n = len(A.pub)
        go = [SP.to_dt(m) - P.AEST for m in A.pub]          # UTC go-live
        rank = np.argsort(np.argsort(-A.w)) / n
        is_lb = rng.random(n) < P.LIVEBLOG_SHARE[d] * np.where(rank < 0.25, 2.6, 0.47)
        subjects = SUBJECTS[d]
        # corrections: which articles, when
        total, second = P.HEADLINE_CORR[d]
        n_art_corr = total - second
        can = np.array([go[i] < end_utc - dt.timedelta(days=2) for i in range(n)])
        metro_restorable = np.array([(d in P.METRO) and (lookback <= go[i] < restore - dt.timedelta(hours=3))
                                     for i in range(n)])
        forced = []
        if d in ("SPT-M", "LOC-M", "POL-M"):
            pool = np.where(metro_restorable & can)[0]
            n_force = {"SPT-M": 2, "LOC-M": 2, "POL-M": 1}[d]
            forced = list(rng.choice(pool, size=n_force, replace=False))
        rest = [i for i in np.where(can)[0] if i not in forced]
        chosen = forced + list(rng.choice(rest, size=n_art_corr - len(forced), replace=False))
        med = P.MEDIAN_MIN_GUIDE[d]
        hc_first = {}
        for i in chosen:
            if i in forced:
                gap = (restore - go[i]).total_seconds() / 60
                m = int(min(max(4, rng.lognormal(np.log(med), 0.6)), gap - 30))
            else:
                m = int(max(3, round(rng.lognormal(np.log(med), 0.75))))
            hc_first[i] = m
        if d == "LOC-M":
            # one restored article whose headline is corrected after the restore, on its new document
            pool = [i for i in np.where(metro_restorable & can)[0] if i not in chosen]
            late = int(rng.choice(pool))
            chosen.append(late)
            gap = (restore - go[late]).total_seconds() / 60
            hc_first[late] = int(gap + rng.integers(40, 160))
            # keep the desk total: drop one ordinary corrected article
            drop = [i for i in chosen if i not in forced and i != late][0]
            chosen.remove(drop)
            del hc_first[drop]
        sec_set = set(rng.choice([i for i in chosen if i not in forced], size=second, replace=False))
        hc_second = {i: hc_first[i] + int(rng.integers(45, 900)) for i in sec_set}
        n_body = int(round(P.BODY_PER_HEADLINE * total))
        body_idx = list(rng.choice(np.where(can)[0], size=n_body, replace=False))
        # a body note on each forced restorable article, before the restore, so the restored copy carries notes
        body_at = {}
        for i in body_idx:
            body_at.setdefault(i, []).append(int(max(5, round(rng.lognormal(np.log(260), 0.9)))))
        W.cms_truth[d] = dict(chosen=list(chosen), hc_first=dict(hc_first), hc_second=dict(hc_second))
        # documents
        for i in range(n):
            g = go[i]
            dtyp = "liveblog" if is_lb[i] else "story"
            D = Doc(doc_id("doc", d, i), d, dtyp, art=i)
            created = g - dt.timedelta(minutes=int(rng.integers(20, 240)))
            ev = [(created, "draft", None, None)]
            for _ in range(int(rng.random() < 0.25)):
                ev.append((created + dt.timedelta(minutes=int(rng.integers(5, 15))), "draft", None, None))
            if rng.random() < 0.3:
                ev.append((g - dt.timedelta(minutes=int(rng.integers(2, 12))), "scheduled", None, None))
            ev.append((g, "live", None, None))
            span = (rng.integers(180, 840) if dtyp == "liveblog" else rng.integers(30, 2160))
            nupd = rng.poisson(16 if dtyp == "liveblog" else 1.1)
            for _ in range(nupd):
                t = g + dt.timedelta(minutes=int(rng.integers(2, span + 1)))
                ch = rng.random() < (0.40 if dtyp == "liveblog" else 0.12)
                ev.append((t, "upd", ch, None))
            if i in hc_first:
                ev.append((g + dt.timedelta(minutes=hc_first[i]), "hc", True, None))
            if i in hc_second:
                ev.append((g + dt.timedelta(minutes=hc_second[i]), "hc", True, None))
            for m in body_at.get(i, []):
                ev.append((g + dt.timedelta(minutes=m), "bc", False, None))
            if (i in hc_first or i in body_at) and rng.random() < 0.08:
                ev.append((g + dt.timedelta(days=int(rng.integers(2, 20)), minutes=int(rng.integers(0, 600))), "clear", False, None))
            # later saves after a correction carry the note forward
            corr_times = [e[0] for e in ev if e[1] in ("hc", "bc")]
            if corr_times:
                for _ in range(int(rng.integers(2, 6))):
                    t = min(corr_times) + dt.timedelta(minutes=int(rng.integers(3, 2880)))
                    ev.append((t, "upd", rng.random() < 0.05, None))
            ev = [e for e in ev if e[0] <= end_utc]
            ev.sort(key=lambda e: (e[0], {"draft": 0, "scheduled": 1, "live": 2, "upd": 3, "hc": 4, "bc": 5, "clear": 6}[e[1]]))
            hv, note, status = 0, "", "draft"
            restored = (d in P.METRO) and (lookback <= g < restore)
            copy = None
            for (t, kind, ch, _) in ev:
                if restored and copy is None and t >= restore:
                    copy = Doc(doc_id("restored", d, i), d, dtyp, restored_from=D.id, art=i)
                    rt = restore + dt.timedelta(minutes=int(rng.integers(5, 55)))
                    copy.revs.append((rt, "live", hsha(D.id, hv), note))
                    if t < rt:
                        t = rt + dt.timedelta(minutes=1)
                target = copy if copy is not None else D
                if kind in ("draft", "scheduled", "live"):
                    status = kind
                elif kind == "upd":
                    if ch:
                        hv += 1
                elif kind == "hc":
                    hv += 1
                    x = subjects[int(rng.integers(len(subjects)))]
                    new = HEAD_NOTES[int(rng.integers(len(HEAD_NOTES)))].format(x=x)
                    note = new if not note else new + " " + note
                elif kind == "bc":
                    x = subjects[int(rng.integers(len(subjects)))]
                    new = BODY_NOTES[int(rng.integers(len(BODY_NOTES)))].format(x=x)
                    note = new if not note else new + " " + note
                elif kind == "clear":
                    note = ""
                target.revs.append((t, status, hsha(D.id, hv), note))
                if status == "live" and target.live_at is None:
                    target.live_at = t
            if restored and copy is None:
                copy = Doc(doc_id("restored", d, i), d, dtyp, restored_from=D.id, art=i)
                rt = restore + dt.timedelta(minutes=int(rng.integers(5, 55)))
                copy.revs.append((rt, "live", hsha(D.id, hv), note))
                copy.live_at = rt
            if copy is not None and copy.live_at is None:
                copy.live_at = copy.revs[0][0]
            docs.append(D)
            if copy is not None:
                docs.append(copy)
            # posts of a live blog
            if dtyp == "liveblog":
                npost = rng.poisson(P.POSTS_PER_LIVEBLOG[d])
                for j in range(npost):
                    t = g + dt.timedelta(minutes=int(rng.integers(3, int(span) + 30)))
                    if t > end_utc:
                        continue
                    parent = D.id
                    if restored and t >= restore and copy is not None:
                        parent = copy.id
                    Pd = Doc(doc_id("post", d, i, j), d, "post", parent=parent)
                    Pd.revs.append((t - dt.timedelta(minutes=int(rng.integers(1, 6))), "draft", hsha(Pd.id, 0), ""))
                    Pd.revs.append((t, "live", hsha(Pd.id, 0), ""))
                    Pd.live_at = t
                    if rng.random() < 0.3:
                        Pd.revs.append((t + dt.timedelta(minutes=int(rng.integers(2, 40))), "live",
                                        hsha(Pd.id, int(rng.random() < 0.5)), ""))
                    if restored and t < restore:
                        Cp = Doc(doc_id("restored-post", d, i, j), d, "post", parent=copy.id if copy else parent,
                                 restored_from=Pd.id)
                        rt = restore + dt.timedelta(minutes=int(rng.integers(5, 55)))
                        Cp.revs.append((rt, "live", Pd.revs[-1][2], ""))
                        Cp.live_at = rt
                        docs.append(Cp)
                    docs.append(Pd)
        # scheduled and pulled documents that never went live
        n_pull = int(round(P.PULLED_SHARE * n))
        for j in range(n_pull):
            day = P.WINDOW_START + dt.timedelta(days=int(rng.integers(1, 360)))
            t = dt.datetime(day.year, day.month, day.day, int(rng.integers(0, 12)), int(rng.integers(0, 60)))
            Dd = Doc(doc_id("pulled", d, j), d, "story")
            Dd.revs.append((t, "draft", hsha(Dd.id, 0), ""))
            Dd.revs.append((t + dt.timedelta(minutes=int(rng.integers(20, 300))), "scheduled", hsha(Dd.id, 0), ""))
            Dd.revs.append((t + dt.timedelta(minutes=int(rng.integers(320, 900))), "withdrawn", hsha(Dd.id, int(rng.random() < 0.3)), ""))
            docs.append(Dd)
    for D in docs:
        D.revs.sort(key=lambda r: r[0])
    W.cms_docs = docs
    return docs


def cms_rows(docs):
    rows = []
    for D in docs:
        for k, (t, status, hs, note) in enumerate(D.revs, start=1):
            rows.append((D.id, D.desk, D.type, D.parent, k, fmt(t), status, hs, note, D.restored_from))
    rows.sort(key=lambda r: (r[5], r[0], r[4]))
    return rows


# ---------------------------------------------------------------------------------- panel

SITES = {"BLN": "Bightline News", "BLB": "Bightline Brisbane"}
SECTION_OLD = [("BLN", 101, "Home and other", ""), ("BLN", 102, "Politics", "POL-N"), ("BLN", 103, "Business", "BUS-N"),
               ("BLN", 104, "Sport", "SPT-N"), ("BLN", 105, "Culture", "CUL-N"),
               ("BLB", 201, "Local", "LOC-M"), ("BLB", 202, "Sport", "SPT-M"), ("BLB", 203, "Politics", "POL-M"),
               ("BLB", 204, "Home and other", "")]
SECTION_NEW = [("BLN", 101, "Business", "BUS-N"), ("BLN", 102, "Culture", "CUL-N"), ("BLN", 103, "Home and other", ""),
               ("BLN", 104, "Politics", "POL-N"), ("BLN", 105, "Sport", "SPT-N"),
               ("BLB", 201, "Home and other", ""), ("BLB", 202, "Local", "LOC-M"), ("BLB", 203, "Politics", "POL-M"),
               ("BLB", 204, "Sport", "SPT-M")]
PERIODS = ["%d-%02d" % ym for ym in P.MONTHS]
CUTOVER = "2026-03"
SEASON_PANEL = {"SPT-N": [0.93, 0.97, 1.04, 1.02, 0.95, 0.92, 1.0, 1.04, 1.03, 1.05, 1.03, 1.02],
                "SPT-M": [0.92, 0.95, 1.0, 0.97, 0.9, 0.95, 1.03, 1.06, 1.05, 1.08, 1.05, 1.04],
                "POL-N": [1.0, 1.02, 0.86, 0.9, 1.02, 1.0, 1.0, 1.12, 1.06, 1.0, 1.03, 0.99],
                "POL-M": [1.0, 1.0, 0.85, 0.9, 1.0, 1.02, 1.0, 1.04, 1.18, 0.98, 1.02, 1.01]}


def build_panel(W):
    rng = rng_for(700)
    keyed = {}
    for site, code, name, desk in SECTION_NEW:
        key = desk or (site + "-HOME")
        tgt = P.PANEL_TARGET[key if desk else ("BLN-HOME" if site == "BLN" else "BLB-HOME")]
        rem = P.PANEL_REMAINDER[key if desk else ("BLN-HOME" if site == "BLN" else "BLB-HOME")]
        season = np.array(SEASON_PANEL.get(desk, [1.0] * 12))
        vals = tgt * season / season.mean() * (1 + rng.normal(0, 0.025, 12))
        vals = np.round(vals).astype(np.int64)
        want = (tgt // 1000) * 1000 + rem
        vals[-1] += want * 12 - vals.sum()
        keyed[(site, name)] = vals
    W.panel_true = {}
    for (site, name), vals in keyed.items():
        desk = [s[3] for s in SECTION_NEW if s[0] == site and s[2] == name][0]
        if desk:
            W.panel_true[desk] = vals
    rows = []
    rel_pub = {}
    for k, per in enumerate(PERIODS):
        y, m = map(int, per.split("-"))
        ny, nm = (y, m + 1) if m < 12 else (y + 1, 1)
        rel = "R%02d-%02d" % (ny % 100, nm)
        rel_pub[rel] = dt.date(ny, nm, 9 + int(rng.integers(0, 6)))
        sec = SECTION_OLD if per < CUTOVER else SECTION_NEW
        for site, code, name, desk in sec:
            ua = int(keyed[(site, name)][k])
            if per in P.RESTATED_PERIODS:
                ua_pub = int(round(ua * P.RESTATE_FACTOR * (1 + rng.normal(0, 0.004))))
            else:
                ua_pub = ua
            visits = int(round(ua_pub * rng.uniform(2.6, 4.4)))
            rows.append((rel, per, site, code, ua_pub, visits))
    rel_b = "R26-07B"
    rel_pub[rel_b] = dt.date(2026, 7, 30)
    for k, per in enumerate(PERIODS):
        if per not in P.RESTATED_PERIODS:
            continue
        for site, code, name, desk in SECTION_NEW:
            ua = int(keyed[(site, name)][k])
            visits = int(round(ua * rng.uniform(2.6, 4.4)))
            rows.append((rel_b, per, site, code, ua, visits))
    rows.sort(key=lambda r: (r[1], r[0], r[2], r[3]))
    W.panel_rows = rows
    W.panel_rel_pub = rel_pub
    return rows
