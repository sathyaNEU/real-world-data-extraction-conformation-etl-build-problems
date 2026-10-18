"""task162 parallel run: the November 2026 rehearsal on the new tracker. Reporters kept filing on the old tracker's
form; a bridge (service account tracker-bridge) copied every report into the new tracker (form reports into the Browser
intake project BRW, the Report a site issue tool's reports into the web-compatibility project WEBC); the triage team
worked the run's reports on the new tracker under its working agreement. Built from the old tracker's truth in
world.realize(); the export is cut in records.py."""
from __future__ import annotations

import datetime as dt
import math

import common as K

RUN_FROM = dt.datetime(2026, 11, 2, 0, 0)      # Helsinki: the bridge copies reports filed from here
RUN_TO = dt.datetime(2026, 11, 30, 0, 0)       # ... to here (the run's last second is 23:59:59 on Sunday 29 November)
END = dt.datetime(2026, 11, 29, 23, 59, 59)
EXPORT_AT = K.RUN_EXPORT
BRIDGE = "tracker-bridge"
# the bridge stops for the new tracker's weekly maintenance on Sunday evenings and catches up at 02:00 on Monday; for
# the run's close-out it was stopped at 14:00 on Saturday 28 November and restarted at 07:00 on Monday 30 November to
# copy the rest of the run's reports
PAUSES = [(dt.datetime(2026, 11, 8, 18, 0), dt.datetime(2026, 11, 9, 2, 0)),
          (dt.datetime(2026, 11, 15, 18, 0), dt.datetime(2026, 11, 16, 2, 0)),
          (dt.datetime(2026, 11, 22, 18, 0), dt.datetime(2026, 11, 23, 2, 0)),
          (dt.datetime(2026, 11, 28, 14, 0), dt.datetime(2026, 11, 30, 7, 0))]
# stops: the old tracker's database maintenance overran and the bridge could not read it (5 November); the bridge's API
# token expired (10 November); a checkpoint fault (18 November: restarted from the checkpoint of 09:00 on Monday
# 16 November, so everything copied since then was written again); the new tracker's maintenance overran (25 November)
OUTAGES = [(dt.datetime(2026, 11, 5, 1, 5), dt.datetime(2026, 11, 5, 17, 40)),
           (dt.datetime(2026, 11, 10, 1, 12), dt.datetime(2026, 11, 10, 21, 37)),
           (dt.datetime(2026, 11, 18, 1, 50), dt.datetime(2026, 11, 18, 17, 5)),
           (dt.datetime(2026, 11, 25, 2, 41), dt.datetime(2026, 11, 25, 19, 52))]
RESEND_FROM = dt.datetime(2026, 11, 16, 9, 0)
RESEND_AT = dt.datetime(2026, 11, 18, 17, 5)
COPY_CLEANUP = dt.datetime(2026, 11, 18, 17, 52)   # the migration lead's script closes the copies as duplicates

ROTA = {  # Monday of the week -> weekday duty triagers, Saturday cover (10:00 to 14:00)
    dt.date(2026, 11, 2): (["Linnea Kärki", "Johannes Laukkanen", "Saara Väisänen", "Tapio Kallio", "Arja Turunen"], "Sakari Puhakka"),
    dt.date(2026, 11, 9): (["Linnea Kärki", "Johannes Laukkanen", "Tapio Kallio", "Sakari Puhakka", "Arja Turunen"], "Saara Väisänen"),
    dt.date(2026, 11, 16): (["Linnea Kärki", "Saara Väisänen", "Tapio Kallio", "Arja Turunen", "Sakari Puhakka"], "Johannes Laukkanen"),
    dt.date(2026, 11, 23): (["Johannes Laukkanen", "Saara Väisänen", "Arja Turunen", "Sakari Puhakka", "Linnea Kärki"], "Tapio Kallio"),
    dt.date(2026, 11, 30): (["Linnea Kärki", "Johannes Laukkanen", "Saara Väisänen", "Tapio Kallio", "Sakari Puhakka"], None),
}
CLOSE_TRANSITION_USER = "Linnea Kärki"   # closes through the workflow's Close transition (no resolution) most of the time
CLOSE_TRANSITION_SHARE = 0.6
SECOND_COMPONENT_SHARE = 0.065           # a report that spans two areas gets a second component at triage

# the new tracker's components, by the old tracker's product and component
NEW_COMPONENT = {
    ("Engine", "Layout"): "Rendering › Layout", ("Engine", "CSS"): "Rendering › Style",
    ("Engine", "Fonts and Text"): "Rendering › Text", ("Engine", "Graphics"): "Graphics › Compositing",
    ("Engine", "Images"): "Graphics › Images", ("Engine", "Audio and Video"): "Media › Playback",
    ("Engine", "WebRTC"): "Media › Real-time", ("Engine", "Networking"): "Networking › HTTP and Cache",
    ("Engine", "DNS and Proxy"): "Networking › DNS and Proxy", ("Engine", "TLS and Certificates"): "Networking › TLS",
    ("Engine", "JavaScript"): "Script › JavaScript Engine", ("Engine", "WebAssembly"): "Script › WebAssembly",
    ("Engine", "DOM"): "Script › DOM and Web APIs",
    ("Shell", "Tabs and Windows"): "Interface › Tabs and Windows", ("Shell", "Address Bar"): "Interface › Address Bar",
    ("Shell", "Settings"): "Interface › Settings", ("Shell", "Downloads"): "Interface › Downloads",
    ("Shell", "Bookmarks and History"): "Interface › Bookmarks and History", ("Shell", "Passwords"): "Interface › Passwords",
    ("Shell", "Privacy Protections"): "Interface › Privacy Protections", ("Shell", "Sync"): "Interface › Sync",
    ("Extensions", "Extension API"): "Extensions › WebExtensions API", ("Extensions", "Extension Store"): "Extensions › Store",
    ("DevTools", "Inspector"): "Developer Tools › Inspector", ("DevTools", "Console and Debugger"): "Developer Tools › Console and Debugger",
    ("DevTools", "Network Monitor"): "Developer Tools › Network Monitor",
    ("Install and Update", "Installer"): "Platform › Installer", ("Install and Update", "Updater"): "Platform › Updater",
    ("Install and Update", "Crash Reporter"): "Platform › Crash Reporting",
}
GROUPS = ["Rendering and Layout", "Graphics and Media", "Networking", "Script and Web APIs", "Browser Interface",
          "Extensions", "Developer Tools", "Platform and Updates"]
GROUP_OF_PREFIX = {"Rendering": "Rendering and Layout", "Graphics": "Graphics and Media", "Media": "Graphics and Media",
                   "Networking": "Networking", "Script": "Script and Web APIs", "Interface": "Browser Interface",
                   "Extensions": "Extensions", "Developer Tools": "Developer Tools", "Platform": "Platform and Updates"}
HOUSEKEEPING = "Triage › Housekeeping"
# the report form's areas: the component a report lands in when the reporter picks the area
FORM_DEFAULT = {"Engine": {"Layout": ("Engine", "Layout"), "CSS": ("Engine", "Layout"), "Fonts and Text": ("Engine", "Layout"),
                           "Graphics": ("Engine", "Layout"), "Images": ("Engine", "Layout"), "DOM": ("Engine", "DOM"),
                           "JavaScript": ("Engine", "DOM"), "WebAssembly": ("Engine", "DOM"),
                           "Audio and Video": ("Engine", "Audio and Video"), "WebRTC": ("Engine", "Audio and Video"),
                           "Networking": ("Engine", "Networking"), "DNS and Proxy": ("Engine", "Networking"),
                           "TLS and Certificates": ("Engine", "Networking")},
                "Shell": None, "Extensions": ("Extensions", "Extension API"), "DevTools": ("DevTools", "Inspector"),
                "Install and Update": ("Install and Update", "Installer")}
WEBC_COMPONENT = "Site reports › Desktop"
# the second area a report spanning two areas is filed under
SECOND_AREA = {"Media › Playback": "Graphics › Compositing", "Graphics › Compositing": "Media › Playback",
               "Rendering › Layout": "Script › DOM and Web APIs", "Script › DOM and Web APIs": "Rendering › Layout",
               "Rendering › Style": "Interface › Settings", "Rendering › Text": "Graphics › Compositing",
               "Networking › HTTP and Cache": "Interface › Downloads", "Interface › Downloads": "Networking › HTTP and Cache",
               "Extensions › WebExtensions API": "Interface › Tabs and Windows",
               "Interface › Tabs and Windows": "Extensions › WebExtensions API",
               "Interface › Address Bar": "Networking › DNS and Proxy", "Networking › TLS": "Interface › Address Bar",
               "Platform › Updater": "Interface › Settings", "Platform › Crash Reporting": "Graphics › Compositing",
               "Interface › Passwords": "Interface › Sync", "Interface › Sync": "Interface › Passwords",
               "Script › JavaScript Engine": "Developer Tools › Console and Debugger",
               "Developer Tools › Inspector": "Rendering › Style", "Media › Real-time": "Networking › HTTP and Cache",
               "Graphics › Images": "Rendering › Layout", "Interface › Privacy Protections": "Networking › HTTP and Cache",
               "Interface › Settings": "Platform › Updater", "Interface › Bookmarks and History": "Interface › Sync",
               "Developer Tools › Network Monitor": "Networking › HTTP and Cache",
               "Developer Tools › Console and Debugger": "Script › JavaScript Engine",
               "Networking › DNS and Proxy": "Interface › Settings", "Script › WebAssembly": "Script › JavaScript Engine",
               "Extensions › Store": "Interface › Settings", "Platform › Installer": "Platform › Updater"}


def group_of(path):
    return GROUP_OF_PREFIX.get(path.split(" › ")[0])


def form_default(product, component):
    f = FORM_DEFAULT[product]
    if f is None:
        return ("Shell", "Tabs and Windows")
    if isinstance(f, dict):
        return f[component]
    return f


def created_from_filed(t):
    """When the bridge wrote a report filed at t (Helsinki): seconds later, or at the end of a pause or a stop."""
    for a, b in PAUSES + OUTAGES:
        if a <= t < b:
            return b
    return None


def in_working(t):
    m = t.hour * 60 + t.minute
    if t.weekday() < 5:
        return 8 * 60 <= m < 16 * 60 + 30
    if t.weekday() == 5:
        return 10 * 60 <= m < 14 * 60
    return False


class Issue(dict):
    pass


def build(T, reps):
    r = K.rng("parallel")
    run = [x for x in reps if x["kind"] in ("baseline", "first_use", "webcompat_own") and RUN_FROM <= x["opened"] < RUN_TO]
    run.sort(key=lambda x: (x["opened"], x["bug_id"]))
    issues = []
    catch = {}
    for x in run:
        b = created_from_filed(x["opened"])
        if b is None:
            c = x["opened"] + dt.timedelta(seconds=int(r.integers(2, 41)))
        else:
            k = catch.get(b, 0)
            catch[b] = k + 1
            c = b + dt.timedelta(seconds=7 + 3 * k + int(r.integers(0, 3)))
        # a catch-up after a stop goes through the bulk-create endpoint, which takes standard fields only: the old
        # number goes in a label and the bridge's follow-up update (Legacy bug, Affects Version/s) is skipped
        issues.append(Issue(src=x, created=c, legacy=x["bug_id"], filed=x["opened"], copy=False,
                            project="WEBC" if x["kind"] == "webcompat_own" else "BRW", issuetype="Bug",
                            restricted=bool(x["security"]), bulk=b is not None))
    # the re-send: after the checkpoint fault the bridge wrote again every report it had copied since 09:00 on 16 November
    src = sorted((it for it in issues if RESEND_FROM <= it["created"] < OUTAGES[2][0]), key=lambda it: it["created"])
    t = RESEND_AT
    for it in src:
        t = t + dt.timedelta(seconds=int(r.integers(9, 15)))
        issues.append(Issue(src=it["src"], created=t, legacy=it["legacy"], filed=it["filed"], copy=True, original=it,
                            project=it["project"], issuetype="Bug", restricted=it["restricted"], bulk=True))
    # the reports filed while the bridge was stopped on 18 November come after the re-send
    for it in sorted((it for it in issues if not it["copy"] and OUTAGES[2][0] <= it["filed"] < OUTAGES[2][1]),
                     key=lambda it: it["filed"]):
        t = t + dt.timedelta(seconds=int(r.integers(8, 14)))
        it["created"] = t
        it["bulk"] = True
    # the team's own tasks
    for k in range(19):
        day = dt.date(2026, 11, 2) + dt.timedelta(days=int(r.integers(0, 26)))
        while day.weekday() >= 5:
            day += dt.timedelta(days=1)
        ct = dt.datetime.combine(day, dt.time(int(r.integers(8, 16)), int(r.integers(0, 60)), int(r.integers(0, 60))))
        who = ROTA[K.monday(day)][0][int(r.integers(0, 5))]
        issues.append(Issue(src=None, created=ct, legacy=None, filed=None, copy=False, project="BRW", issuetype="Task",
                            restricted=False, task_by=who, bulk=False))
    issues.sort(key=lambda it: (it["created"], it["legacy"] or 0, it["copy"]))
    nb = 23461
    for it in issues:
        if it["project"] == "BRW":
            it["key0"] = "BRW-%d" % nb
            nb += 1 + (1 if r.random() < 0.012 else 0)    # a deleted test issue now and then leaves a gap
    for it in issues:
        x = it["src"]
        if it["issuetype"] == "Task":
            it["comp0"] = HOUSEKEEPING
            continue
        if it["project"] == "WEBC":
            it["comp0"] = WEBC_COMPONENT
            continue
        it["comp0"] = NEW_COMPONENT[form_default(x["product"], x["component"])]
        it["comp_final"] = NEW_COMPONENT[(x["product"], x["component"])]
    triage(issues, r)
    assign_webc_keys(issues)
    return issues


def assign_webc_keys(issues):
    """WEBC keys in the order issues arrived in the project: the bridge's own WEBC reports at creation, the triage
    team's moves at the move."""
    ev = []
    for it in issues:
        if it["project"] == "WEBC":
            ev.append((it["created"], 0, it["legacy"] or 0, it))
        elif it.get("moved_at"):
            ev.append((it["moved_at"], 1, it["legacy"] or 0, it))
    ev.sort(key=lambda e: (e[0], e[1], e[2]))
    n = 5088
    for _, kind, _, it in ev:
        if kind == 0:
            it["key0"] = "WEBC-%d" % n
        else:
            it["key_moved"] = "WEBC-%d" % n
        n += 1


def key_at(it, t):
    if it.get("moved_at") and t >= it["moved_at"]:
        return it["key_moved"]
    return it["key0"]


def current_key(it):
    return it["key_moved"] if it.get("moved_at") else it["key0"]


def triage(issues, r):
    """The team works the run's reports in creation order during duty hours; about one in twelve needs another look
    and waits a day or more. Fills each issue's history."""
    for it in issues:
        it["hist"] = []
        if it["legacy"] is not None and not it["bulk"]:
            # BRW carries the old number in Legacy bug; WEBC, on the new tracker since the spring pilot, in its own
            # Old tracker ID
            field = "Legacy bug" if it["project"] == "BRW" else "Old tracker ID"
            it["hist"].append(dict(author=BRIDGE, at=it["created"] + dt.timedelta(seconds=int(r.integers(1, 4))),
                                   items=[(field, None, str(it["legacy"])),
                                          ("Affects Version/s", None, it["src"]["version"])]))
    # the security team's restricted reports and the web-compatibility team's own reports
    for it in issues:
        if it["copy"] or it["legacy"] is None:
            continue
        if it["restricted"]:
            at = next_working(it["created"] + dt.timedelta(hours=float(r.uniform(1, 30))), rota=False)
            if at is not None:
                it["hist"].append(dict(author=K.PEOPLE["security"], at=at,
                                       items=[("status", "New", "Triaged"),
                                              ("priority", "Unprioritised", "P%d" % int(r.choice([1, 2, 2, 3])))]))
        elif it["project"] == "WEBC":
            if r.random() < 0.83:
                at = next_working(it["created"] + dt.timedelta(hours=float(r.exponential(30))), rota=False)
                if at is not None:
                    who = K.WEBCOMPAT[int(r.integers(0, 2))]
                    it["hist"].append(dict(author=who, at=at, items=[("status", "Needs diagnosis", "Diagnosed")]))
    work = [it for it in issues if it["project"] == "BRW" and it["issuetype"] == "Bug" and not it["restricted"]
            and not it["copy"]]
    copies = sorted((it for it in issues if it["copy"]), key=lambda it: it["created"])
    cleaned = False
    deferred = set()
    for it in work:
        if r.random() < 0.085:
            deferred.add(id(it))
            it["defer_until"] = it["created"] + dt.timedelta(hours=float(r.uniform(20, 70)))
    queue = sorted(work, key=lambda it: it["created"])
    by_legacy = {it["legacy"]: it for it in work}
    minute = dt.datetime(2026, 11, 2, 0, 0)
    stop = dt.datetime(2026, 12, 1, 16, 30)
    busy = {}
    qi = 0
    waiting = []
    while minute < stop:
        while qi < len(queue) and queue[qi]["created"] <= minute:
            waiting.append(queue[qi])
            qi += 1
        if not cleaned and minute >= COPY_CLEANUP:
            cleaned = True
            cleanup_copies(copies, waiting, r)
        wkm = K.monday(minute.date())
        if wkm in ROTA and in_working(minute):
            names, sat = ROTA[wkm]
            on = names if minute.weekday() < 5 else ([sat] if sat else [])
            for who in on:
                if busy.get(who, minute) > minute:
                    continue
                pick = None
                for j, it in enumerate(waiting):
                    if id(it) in deferred and it["defer_until"] > minute:
                        continue
                    pick = j
                    break
                if pick is None:
                    break
                it = waiting.pop(pick)
                svc = float(r.lognormal(math.log(6.5), 0.45))
                at = minute + dt.timedelta(minutes=svc, seconds=int(r.integers(0, 60)))
                busy[who] = at
                first_action(it, who, at, r, by_legacy)
        minute += dt.timedelta(minutes=1)
    for it in waiting:
        it["untouched"] = True
    # later events of triaged reports, in duty hours, up to the export
    for it in work:
        lt = it.get("later")
        if not lt or it.get("closed_at"):
            continue
        at = next_working(lt[1])
        if at is None or at > EXPORT_AT:
            continue
        if lt[0] == "dup":
            close(it, lt[2], at, r, dup=dup_target(it, by_legacy))
        else:
            close(it, lt[2], at, r, resolution=lt[3])
    # the web-compatibility team works the reports moved to it
    for it in work:
        if it.get("moved_at") and r.random() < 0.8:
            at = next_working(it["moved_at"] + dt.timedelta(hours=float(r.exponential(40))), rota=False)
            if at is not None and at <= EXPORT_AT:
                who = K.WEBCOMPAT[int(r.integers(0, 2))]
                it["hist"].append(dict(author=who, at=at, items=[("status", "Needs diagnosis", "Diagnosed")]))
    # the open bugs a duplicate links to when its original is not in the run: loaded by the October trial migration
    pre = sorted({it["dup_link"][1] for it in issues if it.get("dup_link") and it["dup_link"][0] == "legacy"})
    preload = {lid: "BRW-%d" % (17204 + 7 * k + (lid % 5)) for k, lid in enumerate(pre)}
    for it in issues:
        dl = it.get("dup_link")
        it["preload_key"] = preload.get(dl[1]) if dl and dl[0] == "legacy" else None
        it["hist"].sort(key=lambda h: h["at"])
    T_PRELOAD = preload
    return T_PRELOAD


def cleanup_copies(copies, waiting, r):
    """The migration lead's script closes each copy (old number in its label) as a duplicate of the issue holding the
    same old number in Legacy bug, Old tracker ID or a label. An original the team had moved to WEBC no longer holds
    Legacy bug, so its copy is left open in BRW and the team meets it in the queue."""
    t = COPY_CLEANUP
    for it in copies:
        o = it["original"]
        if o["project"] == "BRW" and not o["bulk"] and o.get("moved_at") and o["moved_at"] <= COPY_CLEANUP:
            it["stray"] = True
            waiting.append(it)
            continue
        t = t + dt.timedelta(seconds=int(r.integers(2, 5)))
        it["hist"].append(dict(author=K.PEOPLE["migration"], at=t,
                               items=[("status", "New", "Resolved"), ("resolution", None, "Duplicate"),
                                      ("Link", None, ("dup", ("issue", o)))]))
        it["closed_at"] = t
        it["closed_via"] = "resolve"
        it["dup_link"] = ("issue", o)
    waiting.sort(key=lambda x: x["created"])


def dup_target(it, by_legacy):
    lid = it["src"]["dupe_of"]
    o = by_legacy.get(lid)
    if o is not None and o is not it and o["created"] < it["created"]:
        return ("issue", o)
    return ("legacy", lid)


def next_working(at, rota=True):
    """The first duty minute at or after at, up to the export (the security and web-compatibility teams keep office
    hours on weekdays)."""
    t = at.replace(second=0, microsecond=0)
    for _ in range(60 * 24 * 10):
        if rota:
            wkm = K.monday(t.date())
            ok = wkm in ROTA and in_working(t) and (t.weekday() < 5 or ROTA[wkm][1])
        else:
            ok = t.weekday() < 5 and 8 * 60 + 30 <= t.hour * 60 + t.minute < 16 * 60
        if ok:
            return t + dt.timedelta(seconds=at.second)
        t += dt.timedelta(minutes=1)
        if t > EXPORT_AT:
            return None
    return None


def first_action(it, who, at, r, by_legacy):
    x = it["src"]
    if it.get("stray"):
        # the triager finds the report already moved: closes the copy as a duplicate of it, or moves it there too
        if r.random() < 0.6:
            close(it, who, at, r, dup=("issue", it["original"]))
        else:
            move(it, who, at)
        return
    if x["dupe_of"] is not None and r.random() < 0.86:
        close(it, who, at, r, dup=dup_target(it, by_legacy))
        return
    if x["moved_webcompat"]:
        move(it, who, at)
        return
    items = []
    if it["comp_final"] != it["comp0"]:
        items += [("Component", it["comp0"], None), ("Component", None, it["comp_final"])]
    if r.random() < SECOND_COMPONENT_SHARE:
        second = SECOND_AREA[it["comp_final"]]
        items.append(("Component", None, second))
        it["comp_second"] = second
    items += [("status", "New", "Triaged"), ("priority", "Unprioritised", "P%d" % int(r.choice([2, 3, 3, 3, 4, 4])))]
    it["hist"].append(dict(author=who, at=at, items=items))
    it["triaged_at"] = at
    u = r.random()
    if x["dupe_of"] is not None:
        it["later"] = ("dup", at + dt.timedelta(hours=float(r.exponential(60))), who)
    elif u < 0.38:
        res = str(r.choice(["Incomplete", "Cannot Reproduce", "Won't Fix", "Invalid", "Fixed"], p=[0.32, 0.26, 0.17, 0.15, 0.10]))
        it["later"] = ("close", at + dt.timedelta(hours=float(r.exponential(110))), who, res)


def move(it, who, at):
    """A move to WEBC: Jira drops the Legacy bug value, which WEBC's field configuration does not carry."""
    items = [("project", "Browser intake", "Web compatibility"), ("Key", "MOVE", None)]
    if not it["bulk"]:
        items.append(("Legacy bug", str(it["legacy"]), None))
    items += [("Component", it["comp0"], None), ("Component", None, WEBC_COMPONENT), ("status", "New", "Needs diagnosis")]
    it["hist"].append(dict(author=who, at=at, items=items))
    it["moved_at"] = at


def close(it, who, at, r, dup=None, resolution="Duplicate"):
    frm = "Triaged" if it.get("triaged_at") else "New"
    via_close = (who == CLOSE_TRANSITION_USER and r.random() < CLOSE_TRANSITION_SHARE)
    if via_close:
        items = [("status", frm, "Closed")]
    else:
        items = [("status", frm, "Resolved"), ("resolution", None, resolution)]
    if dup is not None:
        items.append(("Link", None, ("dup", dup)))
    it["hist"].append(dict(author=who, at=at, items=items))
    it["closed_at"] = at
    it["closed_via"] = "close" if via_close else "resolve"
    it["dup_link"] = dup
