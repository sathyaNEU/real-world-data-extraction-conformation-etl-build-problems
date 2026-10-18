"""task162 world: the browser's installs by platform, its adoption of every release (each install takes an update at
its next browser restart; on Windows most installs restart in the two days after Patch Tuesday), the reports users file
(a baseline that follows active installs, and first-use reports that follow the installs reaching a new version), the
duplicates among them, and the record's weekly truth. The parallel run on the new tracker is built in parallel.py.

Everything here is the clean truth: the files are cut from it in records.py, docs.py and parallel.py, and the golden is
computed from the shipped files in calc.py, never from these variables."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

PLATFORMS = ("Windows", "macOS", "Linux")
# install base (installs active in a typical week) at the 1 March 2027 trend level, before seasonality
BASE_INSTALLS = {"Windows": 5.10e6, "macOS": 1.30e6, "Linux": 0.46e6}
GROWTH = 0.04                      # a year
SEASON_AMP, SEASON_PEAK = 0.07, 75  # day of year
ACTIVITY = (1.0, 1.0, 1.0, 1.0, 1.0, 0.80, 0.77)   # weekday shares of the base active on a day
ORGANIC = {"Windows": 0.120, "macOS": 0.110, "Linux": 0.100}   # share of pending installs restarting into the update, a full weekday
BURST = (0.55, 0.42)               # Windows: share of pending installs updating on the Wednesday and Thursday after Patch Tuesday
KERNEL = (0.62, 0.22, 0.09, 0.04, 0.02, 0.01)   # first-use reports by days since the install reached the version
FIRST_USE = 747.0                  # first-use reports if the whole 1 March 2027 base reached one release
RHO_CV = 0.05
BASELINE_WEEK = 333.0              # baseline reports in the week of 8 March 2027
PROPENSITY = {"Windows": 1.00, "macOS": 1.15, "Linux": 2.10}   # baseline reports per active install, relative
SECURITY_SHARE = 0.031
HOUR_W = np.array([2.0, 1.4, 1.0, 0.8, 0.8, 1.0, 1.4, 2.0, 2.8, 3.4, 3.8, 4.0, 4.1, 4.2, 4.3, 4.4, 4.6, 4.9, 5.3, 5.6,
                   5.6, 5.0, 4.0, 2.9])
HOUR_W = HOUR_W / HOUR_W.sum()

DAYS = [K.SIM_START + dt.timedelta(days=i) for i in range((K.SIM_END - K.SIM_START).days + 1)]
IDX = {d: i for i, d in enumerate(DAYS)}


def season(d):
    doy = d.timetuple().tm_yday
    s = 1 + SEASON_AMP * math.cos(2 * math.pi * (doy - SEASON_PEAK) / 365.25)
    return s


def trend(d):
    return (1 + GROWTH) ** ((d - dt.date(2027, 3, 1)).days / 365.25)


def base(d, p):
    return BASE_INSTALLS[p] * trend(d) * season(d)


def activity(d):
    a = ACTIVITY[d.weekday()]
    if K.year_end(d):
        a *= 0.66
    elif K.easter(d):
        a *= 0.86
    return a


def dai(d, p):
    return base(d, p) * activity(d)


def restart_factor(d):
    f = 0.8 if d.weekday() >= 5 else 1.0
    if K.year_end(d):
        f *= 0.6
    return f


def burst_today(d):
    for pt in K.PATCH_TUESDAYS:
        k = (d - pt).days
        if k in (1, 2):
            return BURST[k - 1]
    return 0.0


def version_events():
    """(date, major, dot) for every release and dot release, in order."""
    ev = [(d, m, 0) for m, d in K.RELEASES]
    for m, dots in K.DOTS.items():
        ev += [(d, m, n) for n, d in dots]
    return sorted(ev)


def vstr(m, n):
    return "%d.0" % m if n == 0 else "%d.0.%d" % (m, n)


class Adoption:
    """Per platform and day: the share of the base on each version at the end of the day, and the share that reached
    each major that day (installs moving from an older major; a dot update inside a major is not a new major)."""

    def __init__(self):
        ev = version_events()
        self.share = {p: [] for p in PLATFORMS}        # list of dicts version -> share at end of day
        self.reach = {p: {m: np.zeros(len(DAYS)) for m, _ in K.RELEASES} for p in PLATFORMS}
        self.reach_hours = {}
        for p in PLATFORMS:
            state = {"30.0.2": 0.62, "30.0.1": 0.21, "29.0.1": 0.11, "28.0.1": 0.06}
            newest = (30, 2)
            for i, d in enumerate(DAYS):
                todays = [(m, n) for (dd, m, n) in ev if dd == d]
                half = False
                for m, n in todays:
                    newest = (m, n)
                    half = True
                nv = vstr(*newest)
                pend = {v: s for v, s in state.items() if v != nv}
                h = ORGANIC[p] * restart_factor(d) * (0.5 if half else 1.0)
                keep = 1 - h
                if p == "Windows":
                    b = burst_today(d)
                    if b:
                        keep *= (1 - b)
                conv = 1 - keep
                moved_major = 0.0
                for v, s in pend.items():
                    a = s * conv
                    state[v] = s - a
                    state[nv] = state.get(nv, 0.0) + a
                    if int(v.split(".")[0]) < newest[0]:
                        moved_major += a
                if newest[0] in self.reach[p]:
                    self.reach[p][newest[0]][i] += moved_major
                state = {v: s for v, s in state.items() if s > 1e-9}
                self.share[p].append(dict(state))


class Truth:
    pass


def simulate():
    T = Truth()
    T.adopt = Adoption()
    r = K.rng("rho")
    T.rho = {m: FIRST_USE / sum(BASE_INSTALLS.values()) * math.exp(r.normal(0, RHO_CV) - RHO_CV ** 2 / 2)
             for m, _ in K.RELEASES}
    # expected first-use reports per day and platform, by major
    n = len(DAYS)
    T.first_use = {p: {m: np.zeros(n) for m, _ in K.RELEASES} for p in PLATFORMS}
    for p in PLATFORMS:
        for m, _ in K.RELEASES:
            reach = T.adopt.reach[p][m]
            for i in np.nonzero(reach)[0]:
                installs = reach[i] * base(DAYS[i], p)
                for k, kv in enumerate(KERNEL):
                    if i + k < n:
                        T.first_use[p][m][i + k] += installs * T.rho[m] * kv
    # baseline: scaled so the week of 8 March 2027 carries BASELINE_WEEK
    wk = [dt.date(2027, 3, 8) + dt.timedelta(days=j) for j in range(7)]
    raw = sum(dai(d, p) * PROPENSITY[p] for d in wk for p in PLATFORMS)
    T.base_rate = BASELINE_WEEK / raw
    T.baseline = {p: np.array([dai(d, p) * PROPENSITY[p] * T.base_rate for d in DAYS]) for p in PLATFORMS}
    return T


def weekly_expected(T, monday):
    """Expected reports (security reports included) in the Monday-to-Sunday week."""
    tot = 0.0
    for j in range(7):
        i = IDX[monday + dt.timedelta(days=j)]
        for p in PLATFORMS:
            tot += T.baseline[p][i] + sum(T.first_use[p][m][i] for m in T.first_use[p])
    return tot


if __name__ == "__main__":
    T = simulate()
    for wkday in [dt.date(2026, 1, 12), dt.date(2026, 3, 9), dt.date(2026, 11, 9), dt.date(2027, 1, 11),
                  dt.date(2027, 2, 8), dt.date(2027, 3, 8)]:
        print(wkday, round(weekly_expected(T, wkday) * (1 - SECURITY_SHARE), 1))


# ------------------------------------------------------------------------------------------------- the old tracker
# products and components as the old tracker files them, with the area the dashboard groups them in, the weight of
# baseline reports landing there, and the weight of a release's regressions landing there
COMPONENTS = [
    # product, component, baseline weight, regression weight
    ("Engine", "Layout", 9.0, 9.0), ("Engine", "CSS", 5.0, 5.0), ("Engine", "Fonts and Text", 3.0, 2.5),
    ("Engine", "Graphics", 5.5, 7.0), ("Engine", "Images", 2.0, 1.5), ("Engine", "Audio and Video", 5.0, 5.5),
    ("Engine", "WebRTC", 2.0, 2.0), ("Engine", "Networking", 5.0, 4.5), ("Engine", "DNS and Proxy", 1.5, 1.0),
    ("Engine", "TLS and Certificates", 1.5, 1.0), ("Engine", "JavaScript", 4.5, 4.0), ("Engine", "WebAssembly", 1.0, 0.8),
    ("Engine", "DOM", 4.0, 3.5),
    ("Shell", "Tabs and Windows", 7.0, 8.0), ("Shell", "Address Bar", 6.0, 7.0), ("Shell", "Settings", 3.5, 3.5),
    ("Shell", "Downloads", 2.5, 2.0), ("Shell", "Bookmarks and History", 3.0, 2.5), ("Shell", "Passwords", 2.0, 2.0),
    ("Shell", "Privacy Protections", 3.0, 3.0), ("Shell", "Sync", 2.0, 1.5),
    ("Extensions", "Extension API", 3.5, 4.0), ("Extensions", "Extension Store", 1.5, 1.0),
    ("DevTools", "Inspector", 1.8, 1.5), ("DevTools", "Console and Debugger", 1.6, 1.2), ("DevTools", "Network Monitor", 0.9, 0.7),
    ("Install and Update", "Installer", 1.2, 1.5), ("Install and Update", "Updater", 1.2, 2.0),
    ("Install and Update", "Crash Reporter", 1.0, 1.2),
]
WEBCOMPAT_PRODUCT = ("Web Compatibility", "Site Reports")
# share of reports in each component that the team moves to the web-compatibility team's product (site problems)
MOVE_SHARE = {("Engine", "Layout"): 0.20, ("Engine", "CSS"): 0.22, ("Engine", "Fonts and Text"): 0.12,
              ("Engine", "Graphics"): 0.06, ("Engine", "Images"): 0.10, ("Engine", "Audio and Video"): 0.11,
              ("Engine", "WebRTC"): 0.07, ("Engine", "Networking"): 0.08, ("Engine", "DNS and Proxy"): 0.02,
              ("Engine", "TLS and Certificates"): 0.06, ("Engine", "JavaScript"): 0.16, ("Engine", "WebAssembly"): 0.08,
              ("Engine", "DOM"): 0.21, ("Shell", "Tabs and Windows"): 0.02, ("Shell", "Address Bar"): 0.03,
              ("Shell", "Settings"): 0.01, ("Shell", "Downloads"): 0.05, ("Shell", "Bookmarks and History"): 0.01,
              ("Shell", "Passwords"): 0.07, ("Shell", "Privacy Protections"): 0.10, ("Shell", "Sync"): 0.0,
              ("Extensions", "Extension API"): 0.04, ("Extensions", "Extension Store"): 0.01,
              ("DevTools", "Inspector"): 0.02, ("DevTools", "Console and Debugger"): 0.02,
              ("DevTools", "Network Monitor"): 0.02, ("Install and Update", "Installer"): 0.0,
              ("Install and Update", "Updater"): 0.0, ("Install and Update", "Crash Reporter"): 0.0}
CLUSTER_SHARE = 0.56             # share of first-use reports that report one of the release's regressions
BASE_DUP_SHARE = 0.13            # share of baseline reports duplicating a long-standing bug
LONG_STANDING = 260              # long-standing open bugs filed before the record, drawing duplicates
SPAM_SHARE = 0.03                # spam filed through the form, moved to the hidden product (not exported)
WEBC_OWN_WEEK = 70.0             # reports filed directly into the web-compatibility product (its own intake; not exported)
FIRST_ID = 1904117               # the old tracker's first bug id on 1 October 2025
OS_MIX = {"Windows": (("Windows 11", 0.68), ("Windows 10", 0.32)),
          "macOS": (("macOS 15", 0.55), ("macOS 14", 0.30), ("macOS 13", 0.15)),
          "Linux": (("Linux", 1.0),)}
SEVERITY = (("S1", 0.02), ("S2", 0.09), ("S3", 0.48), ("S4", 0.16), ("--", 0.25))


def _pick(r, pairs):
    names = [p[0] for p in pairs]
    w = np.array([p[1] for p in pairs], dtype=float)
    return names[int(r.choice(len(names), p=w / w.sum()))]


def _time_on(r, d):
    h = int(r.choice(24, p=HOUR_W))
    s = int(r.integers(0, 3600))
    return dt.datetime.combine(d, dt.time(h, s // 60, s % 60))


def regressions(m):
    """A release's regressions: component and reach weight."""
    r = K.rng("regressions", m)
    n = int(r.poisson(18))
    comps = [(c[0], c[1]) for c in COMPONENTS]
    w = np.array([c[3] for c in COMPONENTS])
    out = []
    for j in range(max(n, 6)):
        k = int(r.choice(len(comps), p=w / w.sum()))
        out.append(dict(m=m, j=j, product=comps[k][0], component=comps[k][1], reach=float(r.lognormal(0, 1.0))))
    return out


def realize(T):
    """Every report filed on the old tracker from SIM_START to SIM_END (truth), with the attributes its export
    carries; non-exported reports (spam, the web-compatibility product's own intake) are kept for the id sequence
    and the parallel run."""
    reps = []
    comps = [(c[0], c[1]) for c in COMPONENTS]
    wbase = np.array([c[2] for c in COMPONENTS])
    regs = {m: regressions(m) for m, _ in K.RELEASES}
    for i, d in enumerate(DAYS):
        r = K.rng("reports", d.isoformat())
        for p in PLATFORMS:
            nb = int(r.poisson(T.baseline[p][i]))
            for _ in range(nb):
                reps.append(dict(kind="baseline", platform=p, opened=_time_on(r, d)))
            for m, _ in K.RELEASES:
                lam = T.first_use[p][m][i]
                if lam <= 0:
                    continue
                nf = int(r.poisson(lam))
                for _ in range(nf):
                    reps.append(dict(kind="first_use", platform=p, major=m, opened=_time_on(r, d)))
        # spam and the web-compatibility product's own intake: in the id sequence, never in the export
        ns = int(r.poisson(SPAM_SHARE * sum(T.baseline[p][i] for p in PLATFORMS)))
        for _ in range(ns):
            reps.append(dict(kind="spam", platform=_pick(r, (("Windows", 0.8), ("macOS", 0.15), ("Linux", 0.05))),
                             opened=_time_on(r, d)))
        nw = int(r.poisson(WEBC_OWN_WEEK / 7 * activity(d) / 0.937))
        for _ in range(nw):
            reps.append(dict(kind="webcompat_own", platform=_pick(r, (("Windows", 0.7), ("macOS", 0.22), ("Linux", 0.08))),
                             opened=_time_on(r, d)))
    reps.sort(key=lambda x: (x["opened"], x["kind"], x["platform"], x.get("major", 0)))
    # ids in filing order from the first id at the record start (earlier reports get earlier ids)
    first = next(k for k, x in enumerate(reps) if x["opened"].date() >= K.RECORD_START)
    for k, x in enumerate(reps):
        x["bug_id"] = FIRST_ID + (k - first)
    # attributes
    ra = K.rng("attributes")
    long_ids = sorted(set(int(v) for v in ra.integers(1612000, FIRST_ID - 4000, size=LONG_STANDING)))
    long_w = ra.lognormal(0, 1.1, size=len(long_ids))
    cluster_first = {}
    for x in reps:
        p = x["platform"]
        d = x["opened"].date()
        x["op_sys"] = _pick(ra, OS_MIX[p])
        x["severity"] = _pick(ra, SEVERITY)
        x["security"] = bool(ra.random() < SECURITY_SHARE) if x["kind"] in ("baseline", "first_use") else False
        x["dupe_of"] = None
        x["regression_key"] = None
        if x["kind"] == "first_use":
            m = x["major"]
            # the version the install runs: the major's newest dot release at the filing time
            n = 0
            for dn, dd in K.DOTS.get(m, []):
                if dt.datetime.combine(dd, dt.time(K.RELEASE_HOUR)) <= x["opened"]:
                    n = dn
            x["version"] = vstr(m, n)
            if ra.random() < CLUSTER_SHARE:
                rg = regs[m]
                w = np.array([g["reach"] for g in rg])
                g = rg[int(ra.choice(len(rg), p=w / w.sum()))]
                x["product"], x["component"] = g["product"], g["component"]
                key = (m, g["j"])
                x["regression_key"] = key
                if key in cluster_first:
                    x["dupe_of"] = cluster_first[key]
                else:
                    cluster_first[key] = x["bug_id"]
            else:
                k = int(ra.choice(len(comps), p=wbase / wbase.sum()))
                x["product"], x["component"] = comps[k]
        elif x["kind"] == "baseline":
            k = int(ra.choice(len(comps), p=wbase / wbase.sum()))
            x["product"], x["component"] = comps[k]
            x["version"] = baseline_version(T, ra, p, x["opened"])
            if ra.random() < BASE_DUP_SHARE:
                x["dupe_of"] = int(long_ids[int(ra.choice(len(long_ids), p=long_w / long_w.sum()))])
        elif x["kind"] == "webcompat_own":
            x["product"], x["component"] = WEBCOMPAT_PRODUCT
            x["version"] = baseline_version(T, ra, p, x["opened"])
        else:
            x["product"], x["component"] = "Invalid Bugs", "Spam"
            x["version"] = baseline_version(T, ra, p, x["opened"])
        # the team moves some reports to the web-compatibility team's product during triage: site problems, most of
        # them reported against page layout, scripts and media
        x["moved_webcompat"] = (x["kind"] in ("baseline", "first_use") and not x["security"]
                                and ra.random() < MOVE_SHARE.get((x["product"], x["component"]), 0.0))
    T.long_ids = long_ids
    T.long_w = long_w
    T.regs = regs
    return reps


def baseline_version(T, r, p, t):
    """The version a reporter not on a first-use visit runs: the release channel's mix that day (88 per cent), the
    beta (8) or the nightly (4)."""
    d = t.date()
    u = r.random()
    newest = max([30] + [m for m, dd in K.RELEASES if dt.datetime.combine(dd, dt.time(K.RELEASE_HOUR)) <= t])
    if u < 0.08:
        age = (d - K.MAJOR_DATE.get(newest, dt.date(2025, 6, 17))).days
        return "%d.0b%d" % (newest + 1, 1 + min(9, age // 3))
    if u < 0.12:
        return "%d.0a1" % (newest + 2)
    mix = T.adopt.share[p][IDX[d]]
    vs = sorted(mix)
    w = np.array([mix[v] for v in vs])
    return vs[int(r.choice(len(vs), p=w / w.sum()))]
