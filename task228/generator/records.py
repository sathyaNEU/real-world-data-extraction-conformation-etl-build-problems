"""Records around the corpus: the registry, the install exports, the incident register (experiment and app-wide
rows), the reconciliation's findings, the weekly review log and the distractor files."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import numpy as np

import params as P
import world as W

CPH = ZoneInfo("Europe/Copenhagen")
UTC = ZoneInfo("UTC")


def local(d, h=0, m=0, s=0):
    return datetime(d.year, d.month, d.day, h, m, s, tzinfo=CPH)


def iso_local(dt):
    return dt.isoformat()


# ------------------------------------------------------------------ the registry
def registry(exps, rng):
    out = []
    for e in exps:
        cons_c = float(np.clip(rng.normal(P.CONSENT, 0.01), 0.82, 0.90))
        cons_t = cons_c if e["kind"] != "consent" else cons_c * (1 - e["par"]["lost"])
        n_c = int(round(e["n_c"] / cons_c))
        n_t = int(round(e["n_t"] / (cons_t if e["kind"] == "consent" else float(np.clip(cons_c + rng.normal(0, 0.004), 0.8, 0.92)))))
        e["assigned_c"], e["assigned_t"] = n_c, n_t
        out.append(dict(key=e["key"], title=e["title"], team=e["team"],
                        start=iso_local(local(e["start"])), end=iso_local(local(e["end"], 23, 59, 59)),
                        design={"control": round(1 - e["split"], 2), "treatment": round(e["split"], 2)},
                        assigned={"control": n_c, "treatment": n_t}, status="completed",
                        scorecard_service="v1" if e["start"] < P.MIGRATION - timedelta(days=7) else "v2"))
    return out


def export_of(e):
    s = e["start"]
    if s <= date(2026, 3, 30):
        return "q1"
    if s <= date(2026, 6, 29):
        return "q2"
    return "q3"


def install_ids(rng, n):
    v = rng.integers(0, 2 ** 40, n, dtype=np.int64)
    return ["%010x" % x for x in v]


# ------------------------------------------------------------------ the incident register
def _drift(title, k):
    """titles as typed by hand in the register"""
    forms = [title, title.lower(), title.replace(" ", "  ", 1), title + " ", title.capitalize()]
    return forms[k % len(forms)]


REDIAG = {  # (established kind, flagged by the review) -> first call logged at opening, by position in that group
    ("loss", True): ["late delivery", "duplicate delivery"],
    ("dup", False): ["consent loss"],
    ("late", False): ["telemetry loss", "consent loss"],
    ("consent", True): ["late delivery"],
    ("consent", False): ["telemetry loss"],
}
FLAGGED = {"loss": 5, "dup": 1, "late": 0, "consent": 1}


def incidents(exps, rng):
    """the review's flags and the first calls, set per established type"""
    by = {}
    for e in exps:
        if e["kind"] != "clean":
            by.setdefault(e["kind"], []).append(e)
    for k, es in by.items():
        order = [es[i] for i in rng.permutation(len(es))]
        for j, e in enumerate(order):
            e["flagged"] = j < FLAGGED[k]
        for fl in (True, False):
            grp = [e for e in order if e["flagged"] == fl]
            calls = REDIAG.get((k, fl), [])
            for j, e in enumerate(grp):
                e["first_call"] = calls[j] if j < len(calls) else W.KIND_TYPE[k]
    return by


def register_rows(exps, rng, app_wide):
    rows = []
    n = 0
    inc = [e for e in exps if e["kind"] != "clean"]
    clean = [e for e in exps if e["kind"] == "clean"]
    # suspicions the reconciliation withdrew: three of the engagement experiments and three others
    eng = [e for e in clean if e["eng"] < 0]
    others = [e for e in clean if not e["eng"]]
    withdrawn = eng[:3] + [others[i] for i in rng.choice(len(others), 3, replace=False)]
    for e in withdrawn:
        e["suspected"] = True
    events = []
    for e in inc:
        opened = local(e["start"] + timedelta(days=int(rng.integers(2, 9))), int(rng.integers(8, 17)), int(rng.integers(0, 60)))
        rec = recon_date(e)
        prelim = rng.random() < 0.45
        events.append((opened, e, "confirmed", rec, prelim))
    for e in withdrawn:
        opened = local(e["start"] + timedelta(days=int(rng.integers(2, 9))), int(rng.integers(8, 17)), int(rng.integers(0, 60)))
        events.append((opened, e, "withdrawn", recon_date(e), True))
    events.sort(key=lambda x: (x[0], x[1]["key"]))
    ids = {}
    for opened, e, final, rec, prelim in events:
        n += 1
        iid = "DI-26-%03d" % n
        ids[e["key"]] = iid
        e["incident_id"] = iid
        call = e.get("first_call") or ("telemetry loss" if e.get("eng") else str(rng.choice(W.TYPES)))
        e["first_call"] = call
        title = _drift(e["title"], n)
        base = dict(incident_id=iid, opened=opened.strftime("%Y-%m-%d %H:%M"), closed="", scope="experiment",
                    experiment=title, platform="", incident_type=call, sessions_in_window=None, gap_sessions=None)
        if prelim:
            rows.append(dict(base, status="preliminary", status_date=(opened + timedelta(days=1)).strftime("%Y-%m-%d"),
                             notes="raised at the weekly review" if e.get("flagged") else "raised by the experiment owner"))
        rows.append(dict(base, status=final, status_date=rec.strftime("%Y-%m-%d"),
                         notes="%s reconciliation" % rec.strftime("%B")))
    for a in app_wide:
        n += 1
        a["incident_id"] = "DI-26-%03d" % n
    return rows, ids


def recon_date(e):
    """the monthly reconciliation covering the month the run ended, run on the ninth working day after"""
    end = e["end"]
    m = date(end.year + (end.month == 12), end.month % 12 + 1, 1)
    d, k = m, 0
    while True:
        if d.weekday() < 5:
            k += 1
            if k == 7:
                return d
        d += timedelta(days=1)


# ------------------------------------------------------------------ app-wide incidents
HOURLY = np.array([0.18, 0.12, 0.09, 0.08, 0.10, 0.22, 0.62, 1.30, 1.55, 1.25, 1.05, 1.00, 1.12, 1.02, 0.96, 0.98,
                   1.08, 1.30, 1.45, 1.52, 1.58, 1.40, 0.95, 0.45])
HOURLY = HOURLY / HOURLY.mean()
DAY_SESSIONS = 342000
SHARE = {"ios": 0.45, "android": 0.40, "web": 0.15}


def window_sessions(t0, t1, plat, rng):
    """sessions started on a platform between two local times, from the hourly profile"""
    tot, t = 0.0, t0
    while t < t1:
        nxt = min(t1, (t + timedelta(hours=1)).replace(minute=0, second=0))
        frac = (nxt - t).total_seconds() / 3600.0
        tot += DAY_SESSIONS / 24.0 * HOURLY[t.hour] * SHARE[plat] * frac
        t = nxt
    return int(round(tot * float(np.exp(rng.normal(0, 0.03)))))


def app_wide(rng):
    out = []
    for a in W.APP_WIDE:
        t0 = datetime.strptime(a["opened"], "%Y-%m-%d %H:%M")
        t1 = datetime.strptime(a["closed"], "%Y-%m-%d %H:%M")
        lines = []
        for p in a["platforms"]:
            lines.append(dict(platform=p, sessions=window_sessions(t0, t1, p, rng)))
        tot = sum(x["sessions"] for x in lines)
        frac = a["frac"] + float(rng.uniform(-0.008, 0.008))
        gap = int(round(tot * frac))
        # the share sits mid-bin at two decimals of a per cent
        for d in sorted(range(-200, 201), key=abs):
            v = 100.0 * (gap + d) / tot
            if abs(v - round(v, 2)) <= 0.0018:
                gap += d
                break
        out.append(dict(a, lines=lines, gap=gap, sessions=tot))
    return out


# ------------------------------------------------------------------ the weekly review log
FLAG_TXT = ["telemetry looked off in the scorecard; readout held for a check", "event counts dropped mid-run, holding the readout",
            "panel shows more gaps than last week; held until the owner checks", "holding: sessions per install look wrong",
            "late batches piling up on Android, readout held", "held pending a look at the collector logs"]
CLEAR_TXT = ["owner confirmed the change moves reading; hold lifted", "checked with the squad, release lifted",
             "volume explained by the feature itself; cleared", "nothing wrong in the raw events, hold lifted"]
NOTE_TXT = ["no change in the data-health panel", "looked at the session counts; nothing to hold", "fine this week",
            "small dip on web, within the usual range", "owner asked us to keep an eye on it", "rechecked after the release, ok",
            "numbers in line with the control"]
def review_log(exps, rng):
    rows = []
    reviewers = W.PEOPLE["reviewers"]
    mondays = []
    d = date(2026, 1, 12)
    while d <= date(2026, 10, 5):
        mondays.append(d)
        d += timedelta(days=7)

    def stamp(day):
        t = local(day, 9, int(rng.integers(5, 55)), int(rng.integers(0, 60)))
        return t.astimezone(UTC)

    def review_days(e):
        return [m for m in mondays if e["start"] < m <= e["end"] + timedelta(days=7)]

    flags = []
    for e in exps:
        days = review_days(e)
        if e["kind"] != "clean" and e.get("flagged"):
            day = days[0]
            flags.append((day, e, "flag", FLAG_TXT[int(rng.integers(0, len(FLAG_TXT)))]))
        elif e["kind"] != "clean":
            if rng.random() < 0.4:
                flags.append((days[0], e, "note", NOTE_TXT[int(rng.integers(0, len(NOTE_TXT)))]))
    clean = [e for e in exps if e["kind"] == "clean"]
    for j in rng.choice(len(clean), 9, replace=False):
        e = clean[j]
        days = review_days(e)
        day = days[int(rng.integers(0, len(days)))]
        flags.append((day, e, "flag", FLAG_TXT[int(rng.integers(0, len(FLAG_TXT)))]))
        d2 = [x for x in days if x > day]
        if d2:
            flags.append((d2[0], e, "clear", CLEAR_TXT[int(rng.integers(0, len(CLEAR_TXT)))]))
    flagged_days = {(f[0], f[1]["key"]) for f in flags if f[2] == "flag"}
    for j in rng.choice(len(clean), 14, replace=False):
        e = clean[j]
        days = review_days(e)
        day = days[int(rng.integers(0, len(days)))]
        if (day, e["key"]) not in flagged_days:
            flags.append((day, e, "note", NOTE_TXT[int(rng.integers(0, len(NOTE_TXT)))]))
    # experiments of 2025 still running into January
    for k, (key, day) in enumerate([("AV-25-187", date(2026, 1, 12)), ("AV-25-190", date(2026, 1, 12)),
                                    ("AV-25-191", date(2026, 1, 19))]):
        flags.append((day, dict(key=key), "flag" if k == 1 else "note", "carried over from December"))
    flags.sort(key=lambda x: (x[0], x[1]["key"], x[2]))
    used = set()
    for day, e, act, com in flags:
        t = stamp(day)
        while t in used:
            t = t + timedelta(seconds=int(rng.integers(20, 200)))
        used.add(t)
        rows.append(dict(review_week="%d-W%02d" % day.isocalendar()[:2], logged_at_utc=t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                         experiment_key=e["key"], action=act, reviewer=reviewers[int(rng.integers(0, len(reviewers)))],
                         comment=com))
    return rows


# ------------------------------------------------------------------ distractors
def collector_daily(rng):
    rows = []
    d = date(2026, 1, 1)
    while d <= date(2026, 10, 11):
        for p in P.PLATFORMS:
            s = DAY_SESSIONS * SHARE[p] * float(np.exp(rng.normal(0, 0.05))) * (1.08 if d.weekday() >= 5 else 1.0)
            g = s * float(rng.normal(0.028, 0.002))
            rows.append(dict(date=d.isoformat(), platform=p, sessions=int(s), gap_sessions=int(g),
                             duplicate_sessions=int(s * float(rng.normal(0.003, 0.0004))),
                             late_sessions=int(s * float(rng.normal(0.047, 0.003))),
                             events_received=int(s * float(rng.normal(9.0, 0.3)))))
        d += timedelta(days=1)
    return rows


def app_releases(rng):
    rows = []
    vers = {"ios": [9, 1], "android": [9, 1], "web": [9, 1]}
    d = date(2026, 1, 8)
    while d <= date(2026, 10, 1):
        for p in ("ios", "android"):
            v = vers[p]
            v[1] += 1
            if v[1] > 6:
                v[0] += 1
                v[1] = 0
            if d < date(2026, 4, 1):
                sdk = "9.1.%d" % int(rng.integers(0, 3))
            elif d < date(2026, 7, 1):
                sdk = "9.2.%d" % int(rng.integers(0, 3))
            elif d < date(2026, 8, 3):
                sdk = "9.3.%d" % int(rng.integers(0, 2))
            elif d < date(2026, 8, 6):
                sdk = "9.4.1"
            else:
                sdk = "9.4.%d" % int(rng.integers(2, 4))
            rows.append(dict(released=d.isoformat(), platform=p, app_version="%d.%d.0" % (v[0], v[1]),
                             sdk_version=sdk,
                             rollout_complete=(d + timedelta(days=int(rng.integers(3, 8)))).isoformat()))
        d += timedelta(days=14)
    return rows


def booking_queue(rng):
    rows = []
    teams = W.TEAMS
    titles = ["Lead story video", "Audio player queue", "Paywall trial copy", "Breaking alert timing", "Search filters v2",
              "Live blog layout", "Podcast recommendations", "Student pricing page", "Topic follow onboarding",
              "Front page personalisation", "Article font", "Offline downloads limit", "Push digest time",
              "Comment ranking", "Election night page", "Weather module", "Checkout one page", "Sports hub"]
    d0 = date(2027, 1, 4)
    for j, t in enumerate(titles):
        st = d0 + timedelta(days=7 * int(rng.integers(0, 12)))
        share = float(rng.choice([0.5, 0.5, 0.5, 0.2]))
        rows.append(dict(booking_id="BK-27-%03d" % (j + 1), title=t, team=teams[int(rng.integers(0, len(teams)))],
                         planned_start=st.isoformat(), duration_days=14, design_treatment_share=share,
                         planned_installs=int(rng.choice([12000, 16000, 20000, 24000, 30000])), status="booked"))
    rows.sort(key=lambda r: (r["planned_start"], r["booking_id"]))
    return rows
