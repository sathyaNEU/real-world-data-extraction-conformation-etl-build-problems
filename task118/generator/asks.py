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
ENTRY_NOTES = [
    "Correction: an earlier entry in this blog misstated {x}.",
    "Correction: an entry below gave {x} incorrectly. It has been amended.",
    "Correction: we have amended an entry that misstated {x}.",
]
ENTRY_HEAD_NOTE = "Correction: an entry in this live blog misstated {x} in its headline."
# the note an editor adds on the save after the one that published the corrected headline: it always says so
LAG_NOTES = [
    "Correction: an earlier headline on this article misstated {x}.",
    "Correction: the headline on this story has been amended. It previously misstated {x}.",
    "Correction: an earlier version of this story gave {x} incorrectly in its headline.",
]
HEAD_GENERIC_SHARE = 0.45       # headline corrections written with a general note that does not name the headline
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
# order of events saved in the same minute
ORDER = {"draft": 0, "scheduled": 1, "live": 2, "auto": 3, "upd": 4, "drop": 4, "readd": 4, "hc": 5, "hf": 5, "hn": 5,
         "ln": 5, "lf": 5, "bc": 6, "ec": 7, "eb": 8, "clear": 9}


def fmt(t):
    return t.strftime("%Y-%m-%dT%H:%MZ")


def fmt_local(t):
    """A scheduled publish time as the editor set it in the CMS: Brisbane wall-clock time."""
    return (t + P.AEST).strftime("%Y-%m-%dT%H:%M")


class Doc:
    __slots__ = ("id", "desk", "type", "parent", "restored_from", "migrated_from", "revs", "art", "live_at")

    def __init__(self, id_, desk, type_, parent="", restored_from="", art=-1, migrated_from=""):
        self.id, self.desk, self.type, self.parent, self.restored_from = id_, desk, type_, parent, restored_from
        self.migrated_from = migrated_from
        self.revs = []      # (saved_at, status, headline_sha, note, publish_at)
        self.art = art
        self.live_at = None


class Ev:
    __slots__ = ("t", "kind", "ch", "note", "variant", "publish_at", "tag")

    def __init__(self, t, kind, ch=False, note="", variant="", publish_at=None, tag=""):
        self.t, self.kind, self.ch, self.note, self.variant, self.publish_at, self.tag = \
            t, kind, ch, note, variant, publish_at, tag


def mins(x):
    return dt.timedelta(minutes=int(x))


def clear(m):
    """Minutes to a first headline correction, kept off the hour and the three-hour mark: a value within two minutes of
    60 or 180 moves three minutes to the side it already sits on (the mark itself moves inside), so "within an hour"
    and "more than three hours" read the same whether the mark itself is in or out."""
    for mark in (60, 180):
        if mark - 2 <= m <= mark + 2:
            return mark - 3 if m <= mark else mark + 3
    return m


def build_cms(W, desks=None):
    """Every saved revision of every web-desk document first live in the base year (and never-live ones)."""
    docs = []
    W.cms_truth = {}
    restore = P.RESTORE_AT
    lookback = restore - dt.timedelta(days=P.RESTORE_LOOKBACK_DAYS)
    start_utc = dt.datetime(2025, 10, 1) - P.AEST
    end_utc = dt.datetime(P.WINDOW_END.year, P.WINDOW_END.month, P.WINDOW_END.day, 23, 59) - P.AEST
    quiet_lo = dt.datetime(*P.QUIET_FROM) - P.AEST
    quiet_hi = dt.datetime(*P.QUIET_TO) - P.AEST

    def quiet(t):
        return quiet_lo <= t < quiet_hi

    for d in (desks or P.WEB):
        k = P.WEB.index(d)
        rng = rng_for(600 + k)
        rng_m = rng_for(650 + k, P.CMS_SUBSEED[d])        # the minutes to each correction
        rng_l = rng_for(670 + k, P.LAG_SUBSEED[d])        # which story corrections arrive as a fix then a note
        rng_e = rng_for(680 + k)                          # which entry notes arrive minutes after the entry's fix
        rng_ld = rng_for(690 + k, P.LEAD_SUBSEED[d])      # which story corrections are saved note first
        rng_re = rng_for(695 + k, P.READD_SUBSEED[d])     # which text-corrected stories drop and restore their note
        guard = mins(P.PAIR_GUARD)
        A = W.art[d]
        n = len(A.pub)
        go = [SP.to_dt(m) - P.AEST for m in A.pub]          # UTC go-live
        rank = np.argsort(np.argsort(-A.w)) / n
        is_lb = rng.random(n) < P.LIVEBLOG_SHARE[d] * np.where(rank < 0.25, 2.6, 0.47)
        subjects = SUBJECTS[d]

        def subj():
            return subjects[int(rng.integers(len(subjects)))]

        def head_note():
            if rng.random() < HEAD_GENERIC_SHARE:
                return BODY_NOTES[int(rng.integers(len(BODY_NOTES)))].format(x=subj())
            return HEAD_NOTES[int(rng.integers(len(HEAD_NOTES)))].format(x=subj())

        def body_note():
            return BODY_NOTES[int(rng.integers(len(BODY_NOTES)))].format(x=subj())

        def entry_note(head):
            k = int(rng.integers(len(ENTRY_NOTES) + (1 if head else 0)))
            return (ENTRY_NOTES + [ENTRY_HEAD_NOTE])[k].format(x=subj())

        # ------------------------------------------------------------ which articles carry corrections
        total, second = P.HEADLINE_CORR[d]
        n_art_corr = total - second
        bounds = [dt.datetime(2026, 3, 1) - P.AEST, dt.datetime(2026, 4, 1) - P.AEST]
        near = np.array([any(b - dt.timedelta(days=3) <= go[i] <= b + dt.timedelta(hours=12) for b in bounds)
                         for i in range(n)])
        can = np.array([go[i] < end_utc - dt.timedelta(days=2) for i in range(n)]) & ~near
        restored_flag = np.array([(d in P.METRO) and (lookback <= go[i] < restore) for i in range(n)])
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
                m = int(min(max(4, rng_m.lognormal(np.log(med), 0.6)), gap - 30))
                m = clear(m) if clear(m) <= gap - 30 else clear(m) - 6
            else:
                m = int(max(3, round(rng_m.lognormal(np.log(med), 0.75))))
            hc_first[i] = clear(m)
        if d == "LOC-M":
            # one restored article whose headline is corrected after the restore, on its new document
            pool = [i for i in np.where(metro_restorable & can)[0] if i not in chosen]
            late = int(rng.choice(pool))
            chosen.append(late)
            gap = (restore - go[late]).total_seconds() / 60
            hc_first[late] = clear(int(gap + rng.integers(40, 160)))
            drop = [i for i in chosen if i not in forced and i != late][0]
            chosen.remove(drop)
            del hc_first[drop]
        sec_set = set(rng.choice([i for i in chosen if i not in forced], size=second, replace=False))
        hc_second = {i: hc_first[i] + int(rng_m.integers(45, 900)) for i in sec_set}
        n_body = int(round(P.BODY_PER_HEADLINE * total))
        body_idx = list(rng.choice(np.where(can)[0], size=n_body, replace=False))
        body_at = {}
        for i in body_idx:
            body_at.setdefault(i, []).append(int(max(5, round(rng.lognormal(np.log(260), 0.9)))))
        # live blogs whose entries carry a correction: no other correction, not restored, clear of the quiet span
        far = np.array([not (quiet_lo - dt.timedelta(days=3) <= go[i] < quiet_hi + dt.timedelta(days=1))
                        for i in range(n)])
        lb_pool = [i for i in np.where(is_lb & can & far & ~restored_flag)[0]
                   if i not in hc_first and i not in body_at]
        entry_lbs = set(int(x) for x in rng.choice(lb_pool, size=P.ENTRY_CORR[d], replace=False))
        lb_pool2 = [i for i in lb_pool if i not in entry_lbs]
        entry_body_lbs = set(int(x) for x in rng.choice(lb_pool2, size=P.ENTRY_BODY[d], replace=False))
        lagged_lbs = set(int(x) for x in rng_e.choice(sorted(entry_lbs), size=P.ENTRY_LAG[d], replace=False))
        lagged_lbs |= {i for i in sorted(entry_body_lbs) if rng_e.random() < P.ENTRY_BODY_LAG}
        # scheduling
        sched_type = [""] * n
        for i in range(n):
            u, v = rng.random(), rng.random()
            if restored_flag[i] or go[i] < start_utc + dt.timedelta(days=1) or go[i] > end_utc - dt.timedelta(hours=8):
                continue
            if u < P.SCHED_SHARE:
                sched_type[i] = "early" if v < P.EARLY_SHARE else "sched"
        # text-corrected stories (no headline correction) that will drop their note on one save and restore it on a later one
        text_only = [int(i) for i in sorted(body_at) if i not in hc_first and not is_lb[i] and not restored_flag[i]]
        readd_pool = [int(x) for x in rng_re.choice(text_only, size=min(4 * P.READD_N[d], len(text_only)), replace=False)]
        readd_order = {i: r for r, i in enumerate(readd_pool)}
        readd_done = [0]
        truth = dict(chosen=list(chosen), hc_first=dict(hc_first), hc_second=dict(hc_second),
                     entry=set(), entry_body=set(), sched={}, variants={}, lag={}, entry_lag={}, lead={}, readd={},
                     cancel={}, resched={}, moved={})
        W.cms_truth[d] = truth
        # schedules an editor set back to draft before their time, the article published by hand later the same
        # Brisbane day (aimed on two corrected stories a desk: one first corrected within the hour, one between the
        # hour and three hours, each old scheduled time far enough back that timing from it puts the correction past
        # three hours), and on stories never corrected at a base rate; and schedules set back to draft and set again,
        # which the CMS published at the time set second (one corrected story a desk, and a base rate)
        rng_c = rng_for(710 + k, P.CANCEL_SUBSEED[d])
        cancel, resched = {}, set()
        day_min = [int(((go[i] + P.AEST) - dt.datetime.combine((go[i] + P.AEST).date(), dt.time())).total_seconds() // 60)
                   for i in range(n)]
        room = [m_ - P.CANCEL_EARLIEST for m_ in day_min]     # how far back an old scheduled time can sit that day
        open_ = [not is_lb[i] and not restored_flag[i] and i not in forced and not sched_type[i]
                 and start_utc + dt.timedelta(days=2) <= go[i] <= end_utc - dt.timedelta(days=2) for i in range(n)]
        mid = float(np.median(list(hc_first.values())))
        for lo_, hi_, top in ((3, 55, 260), (64, 176, 330)):
            pool_ = [i for i in sorted(hc_first) if open_[i] and i not in cancel and lo_ <= hc_first[i] <= hi_
                     and room[i] >= max(30, 186 - hc_first[i])]
            if lo_ > 60 and any(hc_first[i] < mid for i in pool_):
                pool_ = [i for i in pool_ if hc_first[i] < mid]
            if not pool_:
                continue
            i = int(rng_c.choice(pool_))
            cancel[i] = int(rng_c.integers(max(30, 186 - hc_first[i]), min(room[i], top - hc_first[i]) + 1))
        for i in range(n):
            u = rng_c.random()
            if open_[i] and i not in hc_first and room[i] >= 40 and u < P.CANCEL_BASE:
                cancel[i] = int(rng_c.integers(20, min(room[i], 240) + 1))
        twin = [i for i in sorted(hc_first) if sched_type[i] == "sched" and not is_lb[i] and not restored_flag[i]
                and i not in forced]
        if twin:
            resched.add(int(rng_c.choice(twin)))
        for i in range(n):
            u = rng_c.random()
            if sched_type[i] == "sched" and i not in hc_first and not is_lb[i] and u < P.RESCHED_BASE:
                resched.add(i)
        # schedules moved to a later time before the first time came, and saved again after it while still scheduled
        # (aimed on two corrected stories a desk: one first corrected within the hour, one between the hour and three
        # hours below the desk's middle, each moved far enough that timing from the first time puts the correction past
        # three hours), and on stories never corrected at a base rate; the CMS published each at the later time
        rng_v = rng_for(730 + k, P.MOVED_SUBSEED[d])
        rng_w = rng_for(735 + k, P.MOVED_SUBSEED[d])
        moved = {}
        ok_m = [sched_type[i] == "sched" and not is_lb[i] and not restored_flag[i] and i not in forced
                and i not in resched and i not in cancel for i in range(n)]
        for lo_, hi_, top in ((6, 55, 330), (64, 176, 360)):
            pool_ = [i for i in sorted(hc_first) if ok_m[i] and i not in moved and lo_ <= hc_first[i] <= hi_]
            if lo_ > 60 and any(hc_first[i] < mid for i in pool_):
                pool_ = [i for i in pool_ if hc_first[i] < mid]
            if not pool_:
                continue
            i = int(rng_v.choice(pool_))
            moved[i] = int(rng_v.integers(max(45, 188 - hc_first[i]), top - hc_first[i] + 1))
        for i in range(n):
            u = rng_v.random()
            if ok_m[i] and i not in hc_first and u < P.MOVED_BASE:
                moved[i] = int(rng_v.integers(20, 241))
        # a desk with no scheduled story first corrected within the hour: one story an editor published by hand is cut
        # as a moved schedule instead (the CMS published it at the time it went live, its first live save a later edit)
        moved_hand, hand_done = {}, [False]
        if not any(6 <= hc_first[i] <= 55 for i in moved if i in hc_first):
            cands = [i for i in sorted(hc_first) if not sched_type[i] and not is_lb[i] and not restored_flag[i]
                     and i not in forced and i not in cancel and 6 <= hc_first[i] <= 55 and hc_first[i] < mid
                     and start_utc + dt.timedelta(days=2) <= go[i] <= end_utc - dt.timedelta(days=2)]
            for i in (rng_v.permutation(cands) if cands else []):
                moved_hand[int(i)] = int(rng_v.integers(max(45, 188 - hc_first[int(i)]), 330 - hc_first[int(i)] + 1))

        # ------------------------------------------------------------ documents carried across at the migration
        n_mig = int(round(n * P.MIGRATION_LOOKBACK_DAYS / 365))
        prefix = "B-" if d in P.METRO else "N-"
        mig_ids = sorted(rng.choice(np.arange(410000, 990000), size=n_mig, replace=False))
        p_head, p_body = 0.006, 0.010
        for j in range(n_mig):
            dtyp = "liveblog" if rng.random() < P.LIVEBLOG_SHARE[d] else "story"
            Dm = Doc(doc_id("migrated", d, j), d, dtyp, migrated_from="%s%07d" % (prefix, mig_ids[j]))
            note = ""
            hv = int(rng.integers(0, 3))
            u = rng.random()
            if j == 0 or u < p_head:
                note = HEAD_NOTES[int(rng.integers(len(HEAD_NOTES)))].format(x=subj())
                hv += 1
            elif j == 1 or u < p_head + p_body:
                note = BODY_NOTES[int(rng.integers(len(BODY_NOTES)))].format(x=subj())
            t0 = P.MIGRATION_AT + mins(rng.integers(0, 85))
            Dm.revs.append((t0, "live", hsha(Dm.id, hv), note, None))
            Dm.live_at = t0
            for _ in range(rng.poisson(0.7 if dtyp == "story" else 3.0)):
                t = t0 + mins(rng.integers(30, 10 * 1440))
                if rng.random() < 0.08:
                    hv += 1
                Dm.revs.append((t, "live", hsha(Dm.id, hv), note, None))
            docs.append(Dm)

        # ------------------------------------------------------------ articles
        for i in range(n):
            g = go[i]
            dtyp = "liveblog" if is_lb[i] else "story"
            D = Doc(doc_id("doc", d, i), d, dtyp, art=i)
            st = sched_type[i]
            created = g - mins(rng.integers(90, 960) if st else rng.integers(20, 240))
            created = max(created, start_utc + mins(1))
            if created >= g:
                created = g - mins(1)
            ev = [Ev(created, "draft")]
            if rng.random() < 0.25:
                t2 = created + mins(rng.integers(5, 15))
                if t2 < g - mins(1):
                    ev.append(Ev(t2, "draft"))
            last_pre = max(e.t for e in ev)
            if st:
                s_t = g - mins(rng.integers(15, 600))
                if s_t <= last_pre:
                    s_t = last_pre + mins(1)
                if s_t >= g:
                    st = ""
                else:
                    pub = g if st == "sched" else g + mins(rng.integers(10, 121))
                    ev.append(Ev(s_t, "scheduled", publish_at=pub))
            if st != "sched":
                ev.append(Ev(g, "live"))
            span = int(rng.integers(180, 840) if dtyp == "liveblog" else rng.integers(30, 2160))
            nupd = rng.poisson(16 if dtyp == "liveblog" else 1.1)
            for _ in range(nupd):
                t = g + mins(rng.integers(2, span + 1))
                ev.append(Ev(t, "upd", ch=rng.random() < (0.40 if dtyp == "liveblog" else 0.12)))
            if i in hc_first:
                ev.append(Ev(g + mins(hc_first[i]), "hc", note=head_note(), tag="first"))
            if i in hc_second:
                ev.append(Ev(g + mins(hc_second[i]), "hc", note=head_note(), tag="second"))
            for m in body_at.get(i, []):
                ev.append(Ev(g + mins(m), "bc", note=body_note()))
            if (i in hc_first or i in body_at) and rng.random() < 0.08:
                ev.append(Ev(g + dt.timedelta(days=int(rng.integers(2, 20)), minutes=int(rng.integers(0, 600))), "clear"))
            corr_times = [e.t for e in ev if e.kind in ("hc", "bc")]
            if corr_times:
                for _ in range(int(rng.integers(2, 6))):
                    ev.append(Ev(min(corr_times) + mins(rng.integers(3, 2880)), "upd", ch=rng.random() < 0.05))

            # live-blog entries, planned before the blog's own revisions so entry fixes line up with its notes
            posts = []
            if dtyp == "liveblog":
                npost = rng.poisson(P.POSTS_PER_LIVEBLOG[d])
                for j in range(npost):
                    tp = g + mins(rng.integers(1, 6) if j == 0 else rng.integers(3, span + 30))   # a blog opens on an entry
                    upd = None
                    if rng.random() < 0.3:
                        upd = (tp + mins(rng.integers(2, 40)), bool(rng.random() < 0.5))
                    posts.append(dict(j=j, t=tp, d0=int(rng.integers(1, 6)), upd=upd, fix=None))
                posts = [p for p in posts if p["t"] <= end_utc]
                for kind_set, kind in ((entry_lbs, "ec"), (entry_body_lbs, "eb")):
                    if i not in kind_set:
                        continue
                    cands = [p for p in posts if p["t"] + mins(100) < min(end_utc, g + mins(span + 120))]
                    if not cands:
                        continue
                    p = cands[int(rng.integers(len(cands)))]
                    t_post = p["t"] + mins(rng.integers(8, 91))
                    if kind == "ec":        # the entry's fix is the blog's first headline correction
                        dur = int((t_post - g).total_seconds() // 60)
                        t_post += mins(max(clear(dur) - dur, 0) + (6 if clear(dur) < dur else 0))
                    # the entry is saved first; the blog's note goes on in the same minute or a few minutes later
                    t_note = t_post + (mins(rng_e.integers(P.ENTRY_LAG_MINUTES[0], P.ENTRY_LAG_MINUTES[1] + 1))
                                       if i in lagged_lbs else dt.timedelta(0))
                    p["fix"] = (t_post, kind == "ec")
                    p["note_t"] = t_note
                    ev.append(Ev(t_note, kind, note=entry_note(kind == "ec"), tag=p["j"]))
                    (truth["entry"] if kind == "ec" else truth["entry_body"]).add(i)
                    truth["entry_lag"][i] = (t_post, t_note)

            ev = [e for e in ev if e.t <= end_utc]
            ev.sort(key=lambda e: (e.t, ORDER[e.kind]))

            # a scheduled article goes live at publish_at with no save; its first live save is a later edit
            if st == "sched":
                t_c = min([e.t for e in ev if e.t > g and e.kind in ("hc", "hf", "hn", "bc", "ec", "eb", "clear")],
                          default=None)
                t_u = min([e.t for e in ev if e.t > g and e.kind == "upd"], default=None)
                if t_c is None and t_u is None:
                    ev.append(Ev(min(g + mins(rng.integers(10, 241)), end_utc), "upd"))
                elif t_c is not None and (t_u is None or t_u >= t_c):
                    gap = (t_c - g).total_seconds() / 60
                    if gap < 5:
                        ev = [e for e in ev if e.kind != "scheduled"] + [Ev(g, "live")]
                        st = ""
                    else:
                        ev.append(Ev(g + mins(max(1, int(gap * rng.uniform(0.2, 0.7)))), "upd"))
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
            if st:
                truth["sched"][i] = st

            # a schedule set back to draft before its time: drafted, scheduled, set back to draft, worked on after the
            # time first set, published by hand at g; the article was a draft when that time came
            if i in cancel and not st:
                was = g - mins(cancel[i])
                s_t = was - mins(rng_c.integers(30, 601))
                c0 = s_t - mins(rng_c.integers(10, 121))
                gap = int((was - s_t).total_seconds() // 60)
                c_t = s_t + mins(rng_c.integers(3, gap - 2))
                r_t = was + mins(rng_c.integers(3, cancel[i] - 2))
                pre = [Ev(c0, "draft"), Ev(s_t, "scheduled", publish_at=was), Ev(c_t, "draft"), Ev(r_t, "draft")]
                if int((g - r_t).total_seconds() // 60) > 8 and rng_c.random() < 0.4:
                    pre.append(Ev(r_t + mins(rng_c.integers(2, int((g - r_t).total_seconds() // 60) - 3)), "draft"))
                ev = [e for e in ev if not (e.kind == "draft" and e.t < g)] + pre
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
                truth["cancel"][i] = (was, c_t, r_t)
            # a schedule set back to draft and set again: the CMS published the article at the time set second
            if i in resched and st == "sched":
                s2 = [e for e in ev if e.kind == "scheduled"][0].t
                s1 = s2 - mins(rng_c.integers(60, 601))
                c_t = s1 + mins(rng_c.integers(3, int((s2 - s1).total_seconds() // 120)))
                was = c_t + mins(rng_c.integers(3, int((s2 - c_t).total_seconds() // 60) - 2))
                c0 = s1 - mins(rng_c.integers(10, 121))
                ev = [e for e in ev if not (e.kind == "draft" and e.t < g)] + \
                    [Ev(c0, "draft"), Ev(s1, "scheduled", publish_at=was), Ev(c_t, "draft")]
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
                truth["resched"][i] = (was, c_t)
            # a schedule moved to a later time: drafted, scheduled for a time that never came, moved to g before it,
            # saved again after that time while still scheduled; the CMS published the article at g
            if i in moved and st == "sched" and i not in truth["resched"]:
                p1 = g - mins(moved[i])
                s1 = p1 - mins(rng_w.integers(30, 601))
                s2 = s1 + mins(rng_w.integers(3, int((p1 - s1).total_seconds() // 60) - 2))
                s3 = p1 + mins(rng_w.integers(2, max(3, moved[i] - 2)))
                c0 = s1 - mins(rng_w.integers(10, 121))
                ev = [e for e in ev if not (e.kind in ("draft", "scheduled") and e.t < g)] + \
                    [Ev(c0, "draft"), Ev(s1, "scheduled", publish_at=p1), Ev(s2, "scheduled", publish_at=g),
                     Ev(s3, "scheduled", publish_at=g)]
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
                truth["moved"][i] = (p1, s2, s3)

            # a story's headline correction saved in two steps: the corrected headline published on one live save
            # and the note, which says the headline was corrected, added on the next save a few minutes later
            if dtyp == "story" and not restored_flag[i] and i not in forced:
                split = []
                for e in sorted([e for e in ev if e.kind == "hc"], key=lambda e: e.t):
                    u = rng_l.random()
                    lag_m = int(rng_l.integers(P.LAG_MINUTES[0], P.LAG_MINUTES[1] + 1))
                    form = LAG_NOTES[int(rng_l.integers(len(LAG_NOTES)))]
                    x = subjects[int(rng_l.integers(len(subjects)))]
                    t_n = e.t + mins(lag_m)
                    clear_of = all(not (e.t - mins(1) <= o.t <= t_n + mins(1)) for o in ev if o is not e)
                    if (u < P.LAG_SHARE[d] and clear_of and not quiet(e.t - mins(P.PAIR_GUARD))
                            and not quiet(t_n + mins(P.PAIR_GUARD)) and t_n <= end_utc):
                        split.append((e, Ev(e.t, "hf", tag=e.tag), Ev(t_n, "hn", note=form.format(x=x), tag=e.tag)))
                for e, hf, hn in split:
                    ev.remove(e)
                    ev += [hf, hn]
                    truth["lag"][(i, e.tag)] = (hf.t, hn.t)
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
            # the note before its fix: a story's headline correction saved in two steps the other way round, the note
            # (which says the headline was corrected) on one live save and the corrected headline on the next save
            if dtyp == "story" and not restored_flag[i] and i not in forced:
                conv = []
                for e in sorted([e for e in ev if e.kind == "hc"], key=lambda e: e.t):
                    u = rng_ld.random()
                    lead_m = int(rng_ld.integers(P.LEAD_MINUTES[0], P.LEAD_MINUTES[1] + 1))
                    form = LAG_NOTES[int(rng_ld.integers(len(LAG_NOTES)))]
                    x = subjects[int(rng_ld.integers(len(subjects)))]
                    t_n = e.t - mins(lead_m)
                    clear_of = all(not (t_n - mins(1) <= o.t <= e.t + mins(1)) for o in ev if o is not e)
                    if (u < P.LEAD_SHARE[d] and clear_of and t_n > g + mins(1) and not quiet(t_n - mins(P.PAIR_GUARD))
                            and not quiet(e.t + mins(P.NOTE_GUARD_AFTER))):
                        conv.append((e, Ev(t_n, "ln", note=form.format(x=x), tag=e.tag), Ev(e.t, "lf", tag=e.tag)))
                for e, ln, lf in conv:
                    ev.remove(e)
                    ev += [ln, lf]
                    truth["lead"][(i, e.tag)] = (ln.t, lf.t)
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
            # no ordinary headline change in the hour before a note that leaves the headline as it was, so a note is
            # read against the one fix it records whatever pairing window a reader uses
            note_on_same = [e.t for e in ev if e.kind in ("bc", "hn", "ln", "ec", "eb")]
            guard_after = mins(P.NOTE_GUARD_AFTER)
            for e in ev:
                if e.kind == "upd" and e.ch and any(tn - guard <= e.t <= tn + guard_after for tn in note_on_same):
                    e.ch = False

            # autosaves of an editor's unpublished changes while the article is live
            restored = bool(restored_flag[i])
            if not restored:
                golive = g
                prev_t = None
                added = []
                for e in ev:
                    if e.t > golive and e.kind in ("upd", "hc", "hf", "lf", "bc"):
                        lo = max(prev_t if prev_t is not None else golive, golive) + mins(1)
                        a_t = e.t - mins(rng.integers(1, 7))
                        variant = ""
                        if e.kind in ("hc", "hf", "lf"):
                            u = rng.random()
                            if quiet(e.t):
                                variant = "B" if u < P.AUTO_B_QUIET else ""
                            else:
                                variant = "A" if u < P.AUTO_A else ("B" if u < P.AUTO_A + P.AUTO_B else "")
                            if e.kind in ("hf", "lf") and variant == "B":
                                variant = ""        # the note and the fix go on different saves
                        elif e.kind == "bc":
                            variant = "Bb" if rng.random() < P.AUTO_BODY else ""
                        else:
                            p_u = P.AUTO_UPD_LB if dtyp == "liveblog" else P.AUTO_UPD
                            variant = "U" if rng.random() < p_u else ""
                        if variant and a_t > lo:
                            added.append(Ev(a_t, "auto", ch=e.ch, note=e.note, variant=variant))
                            if e.kind in ("hc", "hf", "lf"):
                                truth["variants"][(i, e.tag)] = variant
                    prev_t = e.t
                ev += added
                ev.sort(key=lambda e: (e.t, ORDER[e.kind]))

            # a note dropped and restored: a live save leaves the correction note off and a later save, which updates the
            # headline, puts the same note back
            if i in readd_order and readd_done[0] < P.READD_N[d] and not restored \
                    and not any(e.kind == "clear" for e in ev):
                bcs = [e.t for e in ev if e.kind == "bc"]
                last_note = max(bcs) if bcs else end_utc
                for _try in range(16 if bcs else 0):
                    t1 = last_note + mins(rng_re.integers(180, 8 * 1440))
                    t2 = t1 + mins(rng_re.integers(P.READD_GAP[0], P.READD_GAP[1] + 1))
                    if t2 > end_utc - mins(60) or (quiet_lo - dt.timedelta(days=1) <= t2
                                                     and t1 <= quiet_hi + dt.timedelta(days=1)):
                        continue
                    if all(not (t1 - mins(60) <= o.t <= t2 + mins(60)) for o in ev):
                        ev += [Ev(t1, "drop"), Ev(t2, "readd")]
                        ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
                        truth["readd"][i] = (t1, t2)
                        readd_done[0] += 1
                        break

            # entries: an ordinary headline change never falls in the hour before a note on the blog
            if posts:
                note_ts = [e.t for e in ev if e.kind in ("hc", "hn", "bc", "ec", "eb")]
                for p in posts:
                    if p["upd"] is not None and p["upd"][1]:
                        tu = p["upd"][0]
                        if any(tn - guard <= tu <= tn for tn in note_ts):
                            p["upd"] = (tu, False)
                    if p["fix"] is not None:
                        tf = p["fix"][0]
                        own = [tn for tn in note_ts if tn == p["note_t"]]
                        other = [tn for tn in note_ts if tn != p["note_t"] and tn - guard <= tf <= tn]
                        assert own and not other, (d, i)

            # a story published by hand, cut as a moved schedule (above): drafted, scheduled for a time that never came,
            # moved to g before it, saved again after it while still scheduled; the CMS published it at g and its first
            # live save is an edit before anything else saved after g
            if i in moved_hand and not hand_done[0]:
                after_g = sorted(e.t for e in ev if e.t > g)
                gap0 = int((after_g[0] - g).total_seconds() // 60) if after_g else 99
                if gap0 >= 4 and sum(e.kind == "live" and e.t == g for e in ev) == 1:
                    p1 = g - mins(moved_hand[i])
                    s1 = p1 - mins(rng_w.integers(30, 601))
                    s2 = s1 + mins(rng_w.integers(3, int((p1 - s1).total_seconds() // 60) - 2))
                    s3 = p1 + mins(rng_w.integers(2, moved_hand[i] - 2))
                    c0 = s1 - mins(rng_w.integers(10, 121))
                    first_edit = g + mins(max(1, int(gap0 * rng_w.uniform(0.2, 0.5))))
                    ev = [e for e in ev if not (e.kind in ("draft", "scheduled") and e.t < g)
                          and not (e.kind == "live" and e.t == g)] + \
                        [Ev(c0, "draft"), Ev(s1, "scheduled", publish_at=p1), Ev(s2, "scheduled", publish_at=g),
                         Ev(s3, "scheduled", publish_at=g), Ev(first_edit, "upd")]
                    ev.sort(key=lambda e: (e.t, ORDER[e.kind]))
                    truth["moved"][i] = (p1, s2, s3)
                    truth["sched"][i] = "sched"
                    hand_done[0] = True

            # the article's revisions
            hv, note, dropped = 0, "", ""
            copy = None
            for e in ev:
                t = e.t
                if restored and copy is None and t >= restore:
                    copy = Doc(doc_id("restored", d, i), d, dtyp, restored_from=D.id, art=i)
                    rt = restore + mins(rng.integers(5, 55))
                    copy.revs.append((rt, "live", hsha(D.id, hv), note, None))
                    if t < rt:
                        t = rt + mins(1)
                target = copy if copy is not None else D
                pub = None
                if e.kind == "draft":
                    status = "draft"
                elif e.kind == "scheduled":
                    status, pub = "scheduled", e.publish_at
                elif e.kind == "live":
                    status = "live"
                elif e.kind == "upd":
                    status = "live"
                    if e.ch:
                        hv += 1
                elif e.kind == "hc":
                    status = "live"
                    hv += 1
                    note = e.note if not note else e.note + " " + note
                elif e.kind in ("hf", "lf"):
                    status = "live"
                    hv += 1
                elif e.kind == "drop":
                    status = "live"
                    dropped, note = note, ""
                elif e.kind == "readd":
                    status = "live"
                    hv += 1
                    note = dropped
                elif e.kind in ("bc", "hn", "ln", "ec", "eb"):
                    status = "live"
                    note = e.note if not note else e.note + " " + note
                elif e.kind == "clear":
                    status = "live"
                    note = ""
                elif e.kind == "auto":
                    status = "autosave"     # exported as the live document's status, save type autosave
                    if e.variant == "A":
                        target.revs.append((t, status, hsha(D.id, hv + 1), note, None))
                    elif e.variant == "B":
                        target.revs.append((t, status, hsha(D.id, hv + 1), e.note if not note else e.note + " " + note, None))
                    elif e.variant == "Bb":
                        target.revs.append((t, status, hsha(D.id, hv), e.note if not note else e.note + " " + note, None))
                    else:
                        target.revs.append((t, status, hsha(D.id, hv + (1 if e.ch else 0)), note, None))
                    continue
                target.revs.append((t, status, hsha(D.id, hv), note, pub))
                if status == "live" and target.live_at is None:
                    target.live_at = t
            if restored and copy is None:
                copy = Doc(doc_id("restored", d, i), d, dtyp, restored_from=D.id, art=i)
                rt = restore + mins(rng.integers(5, 55))
                copy.revs.append((rt, "live", hsha(D.id, hv), note, None))
                copy.live_at = rt
            if copy is not None and copy.live_at is None:
                copy.live_at = copy.revs[0][0]
            docs.append(D)
            if copy is not None:
                docs.append(copy)

            # the blog's entries
            for p in posts:
                j, t = p["j"], p["t"]
                parent = D.id
                if restored and t >= restore and copy is not None:
                    parent = copy.id
                Pd = Doc(doc_id("post", d, i, j), d, "post", parent=parent)
                pv = 0
                Pd.revs.append((t - mins(p["d0"]), "draft", hsha(Pd.id, pv), "", None))
                Pd.revs.append((t, "live", hsha(Pd.id, pv), "", None))
                Pd.live_at = t
                later = []
                if p["upd"] is not None:
                    later.append((p["upd"][0], "upd", p["upd"][1]))
                if p["fix"] is not None:
                    later.append((p["fix"][0], "fix", p["fix"][1]))
                for tt, kind, ch in sorted(later):
                    if tt > end_utc:
                        continue
                    if ch:
                        pv += 1
                    Pd.revs.append((tt, "live", hsha(Pd.id, pv), "", None))
                if restored and t < restore:
                    Cp = Doc(doc_id("restored-post", d, i, j), d, "post", parent=copy.id if copy else parent,
                             restored_from=Pd.id)
                    rt = restore + mins(rng.integers(5, 55))
                    Cp.revs.append((rt, "live", Pd.revs[-1][2], "", None))
                    Cp.live_at = rt
                    docs.append(Cp)
                docs.append(Pd)

        # ------------------------------------------------------------ scheduled and pulled documents that never went live
        n_pull = int(round(P.PULLED_SHARE * n))
        for j in range(n_pull):
            day = P.WINDOW_START + dt.timedelta(days=int(rng.integers(1, 360)))
            t = dt.datetime(day.year, day.month, day.day, int(rng.integers(0, 12)), int(rng.integers(0, 60)))
            Dd = Doc(doc_id("pulled", d, j), d, "story")
            s_t = t + mins(rng.integers(20, 300))
            pub = s_t + mins(rng.integers(300, 2000))
            w_t = s_t + mins(rng.integers(20, max(21, int((pub - s_t).total_seconds() // 60) - 30)))
            Dd.revs.append((t, "draft", hsha(Dd.id, 0), "", None))
            Dd.revs.append((s_t, "scheduled", hsha(Dd.id, 0), "", pub))
            Dd.revs.append((w_t, "withdrawn", hsha(Dd.id, int(rng.random() < 0.3)), "", None))
            docs.append(Dd)
    for D in docs:
        D.revs.sort(key=lambda r: r[0])
    W.cms_docs = docs
    return docs


def cms_rows(docs):
    """One row per saved revision. status is the document's status when the revision was saved; an autosave of a live
    document's working copy is saved while the document is live, with save type autosave."""
    rows = []
    for D in docs:
        for k, (t, status, hs, note, pub) in enumerate(D.revs, start=1):
            auto = status == "autosave"
            rows.append((D.id, D.desk, D.type, D.parent, k, fmt(t), "live" if auto else status,
                         "autosave" if auto else "save", fmt_local(pub) if pub else "", hs, note,
                         D.restored_from, D.migrated_from))
    rows.sort(key=lambda r: (r[5], r[0], r[4]))
    return rows


def read_corrections(rows, published=True, scheduled=True, entries=True, merge=True, migrated=False, posts=False,
                     never_live=False, blank_start=False, s1=True, s2=True, entry_any=False, entry_tol=None,
                     by_text=None, scheduled_always=False, lag=True, lag_struct=None, entry_from_entry=False,
                     lead=True, readd=True, readd_desk=False, after_first=False, entry_after=0, clock="AEST",
                     autosaves=False, sched_blind=False, sched_min=False, sched_drafted=False, sched_status=False,
                     sched_first=False):
    """Headline and text corrections per article document from cms_rows tuples.

    The golden reading (every flag at its default): a correction is a new note on a revision that publishes the
    article (live saves, and a scheduled revision the CMS published at publish_at), compared with the previously
    published state. It is a headline correction when that revision publishes a changed headline; when the note
    says the headline was corrected and the headline it records was published, with no note, on a save up to
    LAG_WINDOW minutes before (logged on that save); or when one of a live blog's entries published a changed
    headline in the ENTRY_WINDOW minutes up to the note (logged on the entry's revision). The article went live
    when it was first published. Flags switch one handling off at a time: published=False compares every saved
    revision with the one before it (drafts included), scheduled=False takes the first live save as going live,
    entries=False ignores entries, entry_tol sets the entry window in minutes (0 pairs the same minute only),
    lag=False reads a note on an unchanged headline as a text correction whatever it says, lag_struct=N pairs any
    such note with a headline published without a note in the N minutes before it whatever the note says,
    merge=False keeps restored copies as separate documents, migrated/posts/never_live=True keep those documents
    as articles, blank_start=True reads a document's first revision against an empty one, s1=False counts a note
    on every revision that carries one, s2=False counts every new note as a headline correction, entry_any=True
    pairs a blog's note with any entry save in the window, by_text (a tuple of words) classes a new note as a
    headline correction when its new text names one of them, scheduled_always=True takes publish_at as going
    live whenever a scheduled revision precedes the first live save, and entry_from_entry=True times an
    article's first headline correction from the entry's own going live when that correction is an entry's.
    A note the document already carried on an earlier published state, put back after a save that left it off, is
    not a new note (readd=False reads it as new; readd_desk=True also treats as carried any note text an earlier
    saved revision of any document on the desk showed). A note that names the headline on a save that leaves the
    headline unchanged records the headline published without a new note on a save within LAG_WINDOW minutes
    before it or, failing that, after it (lead=False looks before it only; after_first=True tries the save after it
    first); lag_struct pairs the same way. entry_after=N also pairs a blog's note with an entry whose headline changed
    up to N minutes after it (the field notes' pairing line read symmetrically). clock is the zone publish_at is read
    in: AEST (the editor's Brisbane wall clock, the golden), UTC (the saves' clock), or Sydney (AEDT in daylight
    saving, 5 October 2025 to 5 April 2026). autosaves=True takes every revision saved while the document was live as a
    published state, the autosaves of its working copy included (the status column read alone).
    A scheduled time is when the article went live only if the schedule was still in force when it came: the last save
    at or before it is that scheduled revision (a schedule set back to draft before its time never fired, and the
    article went live at its first live save). sched_blind=True takes the last scheduled revision's time whenever it
    precedes the first live save, whatever came after it; sched_min=True takes the earliest scheduled time set;
    sched_drafted=True reads any draft save after the first scheduled revision as a schedule that never fired.
    sched_status=True takes the earliest scheduled time at which the article's last save still read scheduled, whatever
    time that save had set (a schedule moved to a later time read as fired at the time first set); sched_first=True
    takes the first scheduled revision's time when the last save at or before it read scheduled, and otherwise the
    first live save."""
    from collections import defaultdict
    if entry_tol is None:
        entry_tol = P.ENTRY_WINDOW
    by_doc, info = defaultdict(list), {}
    for r in rows:
        did, desk, typ, parent, rev, saved, status, stype, pub, sha, note, rest, mig = r
        if stype == "autosave" and not autosaves:
            status = "autosave"     # a working copy, never published
        by_doc[did].append((int(rev), saved, status, pub, sha, note))
        info[did] = (desk, typ, parent, rest, mig)
    copy_of = {v[3]: k for k, v in info.items() if v[3]}
    t = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%MZ")     # noqa: E731

    def t_set(s):
        x = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M")
        if clock == "UTC":
            return x
        if clock == "Sydney" and dt.datetime(2025, 10, 5, 2) <= x < dt.datetime(2026, 4, 5, 3):
            return x - dt.timedelta(hours=11)
        return x - P.AEST
    first_shown = {}
    if readd_desk:
        for did, revs in by_doc.items():
            dk = info[did][0]
            for r in revs:
                if r[5]:
                    k_ = (dk, r[5])
                    first_shown[k_] = min(first_shown.get(k_, r[1]), r[1])
    fixes = defaultdict(list)       # live blog (original id) -> (time an entry published a changed headline, entry live)
    for did, (desk, typ, parent, rest, mig) in info.items():
        if typ != "post" or rest:
            continue
        chain = sorted(by_doc[did])
        if did in copy_of:
            chain += sorted(by_doc[copy_of[did]])
        pub_states = [r for r in chain if r[2] == "live"]
        if not pub_states:
            continue
        blog = info[parent][3] or parent
        for prev, cur in zip(pub_states, pub_states[1:]):
            if cur[4] != prev[4] or entry_any:
                fixes[blog].append((t(cur[1]), t(pub_states[0][1])))
    out = {}
    for did, (desk, typ, parent, rest, mig) in info.items():
        if (typ == "post" and not posts) or (mig and not migrated) or (rest and merge):
            continue
        chain = sorted(by_doc[did])
        if merge and did in copy_of:
            chain += sorted(by_doc[copy_of[did]])
        live = [r for r in chain if r[2] == "live"]
        if not live:
            if never_live and any(r[2] != "draft" for r in chain):
                out[did] = dict(desk=desk, type=typ, go=t(chain[0][1]), go_first=t(chain[0][1]), heads=[], texts=[])
            continue
        go = t(live[0][1])
        states = live
        if scheduled:
            sch = [r for r in chain if r[2] == "scheduled" and r[0] < live[0][0] and r[3]]
            if sch and sched_status:
                for r in sorted(sch, key=lambda r: t_set(r[3])):
                    p_t = t_set(r[3])
                    before = [x for x in chain if x[0] < live[0][0] and t(x[1]) <= p_t]
                    if p_t < go and before and before[-1][2] == "scheduled":
                        go, states = p_t, [r] + live
                        break
            elif sch and sched_first:
                p_t = t_set(sch[0][3])
                before = [x for x in chain if x[0] < live[0][0] and t(x[1]) <= p_t]
                if p_t < go and before and before[-1][2] == "scheduled":
                    go, states = p_t, [sch[0]] + live
            elif sch:
                pick = min(sch, key=lambda r: t_set(r[3])) if sched_min else sch[-1]
                p_t = t_set(pick[3])
                before = [r for r in chain if r[0] < live[0][0] and t(r[1]) <= p_t]
                fired = bool(before) and before[-1][2] == "scheduled" and before[-1][3] == pick[3]
                if sched_blind or sched_min:
                    fired = True
                elif sched_drafted:
                    fired = not any(r[2] == "draft" and sch[0][0] < r[0] < live[0][0] for r in chain)
                if (p_t < go and fired) or scheduled_always:
                    go = p_t
                    states = [pick] + live
        seq = states if published else chain
        if blank_start:
            seq = [(0, seq[0][1], "", "", "", "")] + list(seq)
        heads, texts, entry_go = [], [], {}
        last_h = None       # a headline published with no new note, since the last change of note
        seen = {seq[0][5]} if seq[0][5] else set()      # notes the document carried on earlier states
        consumed = set()    # later saves whose headline change a note before them has been paired with
        for idx in range(1, len(seq)):
            prev, cur = seq[idx - 1], seq[idx]
            tc = t(cur[1])
            carried = bool(cur[5]) and cur[5] != prev[5] and (
                (readd and cur[5] in seen) or (readd_desk and first_shown.get((desk, cur[5]), cur[1]) < cur[1]))
            if cur[5]:
                seen.add(cur[5])
            if carried or not (cur[5] and (cur[5] != prev[5] or not s1)):
                if cur[5] != prev[5]:
                    last_h = None
                elif cur[4] != prev[4] and idx not in consumed:
                    last_h = tc
                continue
            new_text = cur[5][:len(cur[5]) - len(prev[5])] if prev[5] and cur[5].endswith(prev[5]) else cur[5]
            if by_text is not None:
                (heads if any(w in new_text.lower() for w in by_text) else texts).append(tc)
                last_h = None
                continue
            if cur[4] != prev[4] or not s2:
                heads.append(tc)
                last_h = None
                continue
            if lag_struct is not None:
                cand, win = True, dt.timedelta(minutes=lag_struct)
            else:
                cand, win = lag and "headline" in new_text.lower(), dt.timedelta(minutes=P.LAG_WINDOW)
            paired = None
            if cand:
                if after_first:
                    for j in range(idx + 1, len(seq)):
                        nx, pv = seq[j], seq[j - 1]
                        if t(nx[1]) - tc > win or nx[5] != pv[5]:
                            break
                        if nx[4] != pv[4]:
                            paired = t(nx[1])
                            consumed.add(j)
                            break
                    if paired is None and last_h is not None and tc - last_h <= win:
                        paired = last_h
                elif last_h is not None and tc - last_h <= win:
                    paired = last_h
                elif lead:
                    for j in range(idx + 1, len(seq)):
                        nx, pv = seq[j], seq[j - 1]
                        if t(nx[1]) - tc > win or nx[5] != pv[5]:
                            break
                        if nx[4] != pv[4]:
                            paired = t(nx[1])
                            consumed.add(j)
                            break
            if paired is not None:
                heads.append(paired)
                last_h = None
                continue
            hit = [f for f in fixes.get(did, []) if tc - dt.timedelta(minutes=entry_tol) <= f[0]
                   <= tc + dt.timedelta(minutes=entry_after)] if entries else []
            if hit:
                f = min(hit)
                heads.append(f[0])
                entry_go[f[0]] = f[1]
            else:
                texts.append(tc)
            last_h = None
        heads, texts = sorted(heads), sorted(texts)
        go_first = entry_go.get(heads[0], go) if (heads and entry_from_entry) else go
        out[did] = dict(desk=desk, type=typ, go=go, go_first=go_first, heads=heads, texts=texts)
    return out


# ---------------------------------------------------------------------------------- panel

SITES = {"BLN": "Bightline News", "BLB": "Bightline Brisbane"}
SECTION_OLD = [("BLN", 101, "Home and other", ""), ("BLN", 102, "Politics", "POL-N"), ("BLN", 103, "Sport", "SPT-N"),
               ("BLN", 104, "Culture", "CUL-N"), ("BLN", 105, "Business", "BUS-N"),
               ("BLB", 201, "Home and other", ""), ("BLB", 202, "Politics", "POL-M"), ("BLB", 203, "Local", "LOC-M"),
               ("BLB", 204, "Sport", "SPT-M")]
SECTION_NEW = [("BLN", 101, "Politics", "POL-N"), ("BLN", 102, "Culture", "CUL-N"), ("BLN", 103, "Business", "BUS-N"),
               ("BLN", 104, "Sport", "SPT-N"), ("BLN", 105, "Home and other", ""),
               ("BLB", 201, "Local", "LOC-M"), ("BLB", 202, "Sport", "SPT-M"), ("BLB", 203, "Politics", "POL-M"),
               ("BLB", 204, "Home and other", "")]
PERIODS = ["%d-%02d" % ym for ym in P.MONTHS]
CUTOVER = "2026-03"
HISTORY_RELEASE = "R26-04H"
SEASON_PANEL = {"SPT-N": [0.93, 0.9, 0.95, 0.94, 0.89, 1.0, 1.05, 1.07, 1.06, 1.07, 1.08, 1.08],
                "SPT-M": [0.92, 0.95, 1.0, 0.97, 0.9, 0.95, 1.03, 1.06, 1.05, 1.08, 1.05, 1.04],
                "POL-N": [1.0, 1.02, 0.86, 0.9, 1.02, 1.0, 1.0, 1.12, 1.06, 1.0, 1.03, 0.99],
                "POL-M": [1.0, 1.0, 0.85, 0.9, 1.0, 1.02, 1.0, 1.04, 1.18, 0.98, 1.02, 1.01],
                "BUS-N": [1.02, 1.03, 0.86, 0.91, 1.04, 1.02, 0.99, 1.08, 1.09, 1.0, 0.99, 0.98],
                "CUL-N": [1.0, 0.98, 0.94, 0.91, 1.03, 1.06, 0.97, 1.03, 1.09, 1.0, 1.01, 0.98],
                "LOC-M": [1.03, 0.93, 0.78, 0.8, 0.94, 1.06, 1.05, 1.06, 1.07, 1.08, 1.06, 1.06]}


def build_panel(W):
    """Monthly section audiences in every release. The version of record for a section's month is the latest
    release that published that month (the release log's periods) carrying the section; a release's section codes
    are those of the taxonomy it was issued on. The history release reruns only the national sections whose content
    moved in 2026; the restated release carries both sites; the July release's file also carries April to June as
    first published, rows the warehouse loaded under the July release, which published July only."""
    rng = rng_for(700)
    rng_v = rng_for(701)   # visits: each section's own visits per reader, steady month to month
    freq = {}
    base = {}          # audience on the 2026 taxonomy, every month
    oct_old = {}       # October 2025 as first published, on the 2024 taxonomy (never rerun)
    for site, code, name, desk in SECTION_NEW:
        key = desk or (site + "-HOME")
        tgt = P.PANEL_TARGET[key if desk else ("BLN-HOME" if site == "BLN" else "BLB-HOME")]
        rem = P.PANEL_REMAINDER[key if desk else ("BLN-HOME" if site == "BLN" else "BLB-HOME")]
        season = np.array(SEASON_PANEL.get(desk, [1.0] * 12))
        vals = tgt * season / season.mean() * (1 + rng.normal(0, 0.025, 12))
        vals = np.round(vals).astype(np.int64)
        o = int(round(vals[0] * P.OLD_BASIS[(site, name)])) if (site, name) in P.HISTORY_SECTIONS else int(vals[0])
        want = (tgt // 1000) * 1000 + rem
        vals[-1] += want * 12 - (o + vals[1:].sum())
        base[(site, name)] = vals
        oct_old[(site, name)] = o
        freq[(site, name)] = (2.6 + 1.8 * rng_v.random()) * (1 + rng_v.normal(0, 0.02, 12))
    W.panel_true = {}
    for site, code, name, desk in SECTION_NEW:
        if desk:
            v = base[(site, name)].copy()
            v[0] = oct_old[(site, name)]
            W.panel_true[desk] = v
    rows = []
    rel_pub, rel_per = {}, {}
    first_pub = {}     # (period, site, code) -> (unique_audience, visits) as first published
    for k, per in enumerate(PERIODS):
        y, m = map(int, per.split("-"))
        ny, nm = (y, m + 1) if m < 12 else (y + 1, 1)
        rel = "R%02d-%02d" % (ny % 100, nm)
        rel_pub[rel] = dt.date(ny, nm, 9 + int(rng.integers(0, 6)))
        rel_per[rel] = [per]
        sec = SECTION_OLD if per < CUTOVER else SECTION_NEW
        for site, code, name, desk in sec:
            if per < CUTOVER and k == 0:
                ua = oct_old[(site, name)]
            elif per < CUTOVER and (site, name) in P.HISTORY_SECTIONS:
                ua = int(round(base[(site, name)][k] * P.OLD_BASIS[(site, name)] * (1 + rng.normal(0, 0.003))))
            else:
                ua = int(base[(site, name)][k])
            restated = per in P.RESTATED_PERIODS and site in P.RESTATED_SITES
            ua_pub = int(round(ua * P.RESTATE_FACTOR * (1 + rng.normal(0, 0.004)))) if restated else ua
            rng.uniform(2.6, 4.4)          # the audience stream keeps its draws
            v_true = ua * freq[(site, name)][k]
            visits = int(round(v_true * P.VISITS_RESTATE_FACTOR * (1 + rng_v.normal(0, 0.006)))) if restated \
                else int(round(v_true))
            rows.append((rel, per, site, code, ua_pub, visits))
            first_pub[(per, site, code)] = (ua_pub, visits)
    rel_pub[HISTORY_RELEASE] = dt.date(*P.HISTORY_PUBLISHED)
    rel_per[HISTORY_RELEASE] = list(P.HISTORY_PERIODS)
    for k, per in enumerate(PERIODS):
        if per not in P.HISTORY_PERIODS:
            continue
        for site, code, name, desk in SECTION_NEW:
            if (site, name) not in P.HISTORY_SECTIONS:
                continue
            ua = int(base[(site, name)][k])
            rng.uniform(2.6, 4.4)
            rows.append((HISTORY_RELEASE, per, site, code, ua, int(round(ua * freq[(site, name)][k]))))
    rel_b = "R26-07B"
    rel_pub[rel_b] = dt.date(2026, 7, 30)
    rel_per[rel_b] = list(P.RESTATED_PERIODS)
    for k, per in enumerate(PERIODS):
        if per not in P.RESTATED_PERIODS:
            continue
        for site, code, name, desk in SECTION_NEW:
            if site not in P.RESTATED_SITES:
                continue
            ua = int(base[(site, name)][k])
            rng.uniform(2.6, 4.4)
            rows.append((rel_b, per, site, code, ua, int(round(ua * freq[(site, name)][k]))))
    # each desk section's twelve-month average visits, on the record of each month, lands where VISITS_REMAINDER puts
    # it inside its thousand: the September release, which nothing restates, takes up the difference
    for site, code, name, desk in SECTION_NEW:
        if not desk:
            continue
        rec = []
        for per in PERIODS:
            y, m = map(int, per.split("-"))
            rel = "R%02d-%02d" % ((y + (m == 12)) % 100, m % 12 + 1)
            if per in P.RESTATED_PERIODS:
                rel = rel_b
            elif per in P.HISTORY_PERIODS and (site, name) in P.HISTORY_SECTIONS:
                rel = HISTORY_RELEASE
            sec = SECTION_OLD if (per < CUTOVER and rel != HISTORY_RELEASE) else SECTION_NEW
            c_ = [c for s_, c, nm, _ in sec if s_ == site and nm == name][0]
            idx = [i for i, r in enumerate(rows) if r[:4] == (rel, per, site, c_)]
            assert len(idx) == 1, (rel, per, site, c_)
            rec.append(idx[0])
        total = sum(rows[i][5] for i in rec)
        want = P.VISITS_REMAINDER[desk]
        target = int(round((total / 12 - want) / 1000)) * 1000 + want
        i_sep = rec[-1]
        r_ = rows[i_sep]
        assert r_[1] == "2026-09"
        rows[i_sep] = r_[:5] + (r_[5] + 12 * target - total,)
    # the July release's file also carried April to June for both sites as first published; the warehouse loaded those
    # rows under the July release, which published July only
    for per in P.RESTATED_PERIODS:
        for site, code, name, desk in SECTION_NEW:
            ua_pub, visits = first_pub[(per, site, code)]
            rows.append((P.ECHO_RELEASE, per, site, code, ua_pub, visits))
    rows.sort(key=lambda r: (r[1], r[0], r[2], r[3]))
    W.panel_rows = rows
    W.panel_rel_pub = rel_pub
    W.panel_rel_per = rel_per
    return rows
