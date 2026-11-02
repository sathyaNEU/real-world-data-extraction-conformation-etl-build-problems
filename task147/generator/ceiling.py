"""task147 ask layer against the careful solver's routes, on the cut pack.

    python3 task147/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The ask gives 25
figures: for each of the 2026 season's five roster weeks, the departure cleans and stayover services done by the crew
and by Brennock's temps, and the overtime hours the crew worked. Every route below is a complete pipeline over the cut
pack, scored figure by figure against figures.json; a count is kept only when it is exact, hours within an eighth of an
hour (half the prompt's quarter).

The cracker lands the call (each past season's later bookings replayed whole against the 2027 book, the closing week
about 400, the concert week next at about 200) and is the careful solver on the ask, never a narrowed one:
- it runs the hygiene battery: exact duplicate rows dropped in every ask file; every login, note and timesheet name
  joined across the app, HR and Brennock's timesheets, with the anti-joins both ways; day badges joined on the date and
  the holder; each door reader's clock found from its hour profile against the other readers;
- it reads every field by its plain meaning: a task's login is the attendant whose tablet closed it, a supervisor's
  task note names who did the room, a person is Brennock's on a day Brennock's own timesheet carries them, an HR start
  date after a service means the person was not yet the hotel's, a payroll overtime line's reference carries the date
  the hours were worked, the user list and the HR list stand at their export dates;
- it executes every filed rule as worded: HK-04 2.4 (completed departure cleans and stayover services by the day done,
  do-not-disturb and refused rooms not serviced, a re-clean part of the service it repeats) and 2.5 (the crew are the
  hotel's own room attendants).
The device it misses: on nine days a Brennock regular's loan tablet dropped out mid-morning and she finished her rooms on
the tablet of a crew attendant who was off that day, still signed in to her; that attendant has no door record that
day (no staff-badge event, no day badge from reception), and the app's late-finish claims on two of those tablets a
week were paid to her. No battery item joins a login-day to the door record, so the cracker credits the rooms to the
crew and counts the claims. Its over-cleaning half: crew attendants who came in on a day badge from reception, with no
staff-badge event, worked the whole day on their own logins; reading the doors on staff badges alone counts them out.
The mirror stops at the default path on the call (each night's own past pickup, the concert week first at about 600)
and is scored twice on the ask: on the cracker's own ask path (the ask does not depend on the call, so a top response
off the call runs it as carefully), and on the natural read without the battery (the user list's group as it stands,
notes unread, overtime by the pay period it was paid in). The full includer is the golden's route and has to give back
figures.json exactly, or the script exits 1.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the 25
figures, a method credit of 8 per cent on every figure not kept, a response off the call keeping 5 of the 38. Pair
ceiling is the worst of the pair on either mirror reading and the cracker finding the device alone.
The script modifies nothing and never runs inside the build."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import statistics
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C     # noqa: E402  (the pack readers and the call's routes)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
REC, INS, ASK, OFF, CREDIT = 38.0, 7.0, 55.0, 5.0, 0.08
WEEKS26 = K.roster_weeks(2026)
KEYS = ("crew_dep", "crew_stay", "brn_dep", "brn_stay")


# ---------------------------------------------------------------------------------------------------- the pack
def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling147-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target") if os.path.isdir(os.path.join(tmp, "target")) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return inner, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(inner)), md5)


def rows(folder, name):
    """A CSV as dicts, exact duplicate rows dropped (the battery's first step), with the count dropped."""
    with open(os.path.join(folder, name), encoding="utf-8", newline="") as fh:
        rd = list(csv.DictReader(fh))
    seen, out = set(), []
    for r in rd:
        k = tuple(r.items())
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out, len(rd) - len(out)


def hr_list(folder):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(folder, C.HR_F), read_only=True, data_only=True).worksheets[0]
    out = {}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0]:
            out["%s %s" % (r[2], r[1])] = dict(emp=r[0], title=r[3], contract=r[5], start=r[6].date())
    return out


def week_of(d):
    for w, (m, s) in enumerate(WEEKS26):
        if m <= d <= s:
            return w
    return None


# ---------------------------------------------------------------------------------------------------- Ask A
def ask_a_route(folder, how):
    """Ask A's 25 figures on a route. how: careful (the cracker), natural (no battery), golden (the full includer:
    calc's own route), doors (the cracker with the device found: calc's golden reached from the door record)."""
    if how in ("golden", "doors"):
        return C.ask_a(folder)
    tasks, dup_t = rows(folder, C.TASKS_F)
    users = {r["login"]: r for r in rows(folder, C.USERS_F)[0]}
    ts = C.timesheets(folder)
    hr = hr_list(folder)
    on_ts = {(r["name"], r["date"]) for r in ts}
    names = {u["display_name"] for u in users.values() if not u["login"].startswith("block")} | {r["name"] for r in ts}
    by_first = {}
    for n in names:
        by_first.setdefault(n.split(" ")[0], set()).add(n)
    out = {w: dict(crew_dep=0, crew_stay=0, brn_dep=0, brn_stay=0, ot=0.0) for w in range(5)}
    for r in tasks:
        if r["task_type"] not in ("Departure", "Stayover") or r["status"] != "Completed":
            continue                      # HK-04 2.4: re-cleans part of their service, DND and refused not serviced
        d = dt.date.fromisoformat(r["service_date"])
        w = week_of(d)
        if w is None:
            continue
        u = users[r["user_login"]]
        person = u["display_name"]
        if how == "careful" and r["note"] and u["user_group"] == "Housekeeping Supervisors":
            hit = [f for f in by_first if re.search(r"\b%s\b" % re.escape(f), r["note"])]
            if len(hit) == 1 and len(by_first[hit[0]]) == 1:
                person = next(iter(by_first[hit[0]]))      # the note names who did the room
        if how == "careful":
            started = hr.get(person, {}).get("start")
            brn = (person, d) in on_ts or u["user_group"] == "Agency - Brennock" or \
                (started is not None and started > d and (person, d) in on_ts)
        else:
            brn = u["user_group"] == "Agency - Brennock"
        out[w]["%s_%s" % ("brn" if brn else "crew", "dep" if r["task_type"] == "Departure" else "stay")] += 1
    pay = rows(folder, C.PAY_F)[0]
    for r in pay:
        if how == "careful":
            m = re.match(r"OT (\d\d)/(\d\d)/(\d\d) ", r["reference"])
            d = dt.date(2000 + int(m.group(3)), int(m.group(2)), int(m.group(1)))     # the date worked
        else:
            d = dt.date.fromisoformat(r["period_end"])                                  # the period paid in
        w = week_of(d)
        if w is not None:
            out[w]["ot"] += float(r["hours"])
    return out


def a_battery(folder):
    """The careful solver's checks on Ask A's files, each (check, finding)."""
    tasks, dup_t = rows(folder, C.TASKS_F)
    users = {r["login"]: r for r in rows(folder, C.USERS_F)[0]}
    ts = C.timesheets(folder)
    hr = hr_list(folder)
    out = [("exact duplicate task rows", "%d dropped" % dup_t)]
    used = {r["user_login"] for r in tasks}
    out.append(("every task login in the user list (anti-join)", "%d of %d" % (len(used & set(users)), len(used))))
    tsn = {r["name"] for r in ts}
    disp = {u["display_name"] for u in users.values()}
    out.append(("Brennock's timesheet names without an app login (day temps, logged by a supervisor's note)",
                ", ".join(sorted(tsn - disp)) or "none"))
    both = sorted(n for n in tsn & disp if users[[k for k, v in users.items() if v["display_name"] == n][0]][
        "user_group"] != "Agency - Brennock")
    out.append(("people on Brennock's 2026 timesheets whose login stands in a hotel group now",
                "%s (HR start dates %s)" % (", ".join(both), ", ".join(str(hr[n]["start"]) for n in both if n in hr))))
    sup = [r for r in tasks if users[r["user_login"]]["user_group"] == "Housekeeping Supervisors"]
    out.append(("tasks closed under a supervisor's login, each with a note naming the attendant",
                "%d tasks, %d with a note" % (len(sup), sum(1 for r in sup if r["note"]))))
    pay = rows(folder, C.PAY_F)[0]
    late = sum(1 for r in pay if dt.date(2000 + int(r["reference"][9:11]), int(r["reference"][6:8]),
                                         int(r["reference"][3:5])) < dt.date.fromisoformat(r["period_start"]))
    out.append(("overtime lines paid in a period after the date worked (the reference's date)",
                "%d of %d" % (late, len(pay))))
    return out


def reader_offsets(folder):
    """Each door reader's clock against the staff entrance's, from the hour profile of the same people's exits: the
    median afternoon exit of the day badges through each reader. A reader a whole hour early is read as UTC."""
    acc = rows(folder, C.ACCESS_F)[0]
    ex = {}
    for r in acc:
        t = dt.datetime.fromisoformat(r["event_time"])
        if r["direction"] == "OUT" and r["badge"].startswith("V-") and t.hour >= 13:
            ex.setdefault(r["reader"], []).append(t.hour * 60 + t.minute)
    base = statistics.median(ex["SE-02"])
    return {k: round((base - statistics.median(v)) / 60.0) for k, v in ex.items()}, \
        {k: "%02d:%02d" % divmod(int(statistics.median(v)), 60) for k, v in ex.items()}


# ---------------------------------------------------------------------------------------------------- scoring
def golden_figures():
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    num = lambda s: float(str(s).replace(",", ""))
    a = {w: {k: num(F["ask_a_2026_services_and_overtime"][w][src]) for k, src in
             (("crew_dep", "crew_departure_cleans"), ("crew_stay", "crew_stayover_services"),
              ("brn_dep", "brennock_departure_cleans"), ("brn_stay", "brennock_stayover_services"),
              ("ot", "crew_overtime_hours"))} for w in range(5)}
    return a, F


def kept_a(fig, gold):
    k = {key: sum(fig[w][key] == gold[w][key] for w in range(5)) for key in KEYS}
    k["ot"] = sum(abs(fig[w]["ot"] - gold[w]["ot"]) <= 0.125 for w in range(5))
    return k


def pair(kc, km, n):
    pts = lambda k: ASK * (k + CREDIT * (n - k)) / n
    c, s = REC + INS + pts(kc), OFF + INS + pts(km)
    return c, s, (c + s) / 2.0


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    gold_a, F = golden_figures()
    n = 25

    # the calls
    V = C.from_pack(folder)
    L = C.ladder(V)
    gw = L["gw"]
    p, r_, _ = C.top(gw)
    on_call = (p, r_) == (4, 2) and K.round_to(gw[4], 100) == 400 and K.round_to(gw[2], 100) == 200
    dflt = L["rivals"]["R1 book plus average pickup (default)"]
    pm, rm, _ = C.top(dflt)
    off_call = pm != 4
    print("cracker's call: %s, %.0f room-nights above capacity (%d), next %s at %.0f (%d) (%s)" % (
        C.WEEK_NAMES[p], gw[p], K.round_to(gw[p], 100), C.WEEK_NAMES[r_], gw[r_], K.round_to(gw[r_], 100),
        "lands the golden" if on_call else "MISSES"))
    print("mirror's call (the default path, each night's own pickup): %s at %.0f (%d), next %s (%s)" % (
        C.WEEK_NAMES[pm], dflt[pm], K.round_to(dflt[pm], 100), C.WEEK_NAMES[rm],
        "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    # the control
    kfa = kept_a(ask_a_route(folder, "golden"), gold_a)
    if sum(kfa.values()) != n:
        print("CONTROL FAILED: the full includer gives %d of %d, the route code does not reproduce figures.json"
              % (sum(kfa.values()), n))
        return 1

    # the battery, as the cracker runs it
    print("\nthe cracker's hygiene battery, the ask's files:")
    for chk, finding in a_battery(folder):
        print("  %-92s %s" % (chk, finding))
    offs, med = reader_offsets(folder)
    print("  %-92s %s" % ("each door reader's clock from its hour profile (the day badges' afternoon exits, median)",
                          "%s; an hour off the entrance: %s" % (", ".join("%s %s" % kv for kv in sorted(med.items())),
                                                               ", ".join(k for k, v in sorted(offs.items()) if v == 1)
                                                               or "none")))

    routes = {}
    for who, how in (("cracker", "careful"), ("mirror, no battery", "natural"), ("cracker, the device found", "doors")):
        a = ask_a_route(folder, how)
        routes[who] = (kept_a(a, gold_a), a)
    routes["mirror, the cracker's ask path"] = routes["cracker"]
    print("\nthe cracker's figures by week (golden in brackets): crew departures, crew stayovers, Brennock "
          "departures, Brennock stayovers, overtime hours the crew worked")
    a = routes["cracker"][1]
    for w in range(5):
        print("  %-24s %s" % ("%s to %s" % (WEEKS26[w][0].strftime("%d %b"), WEEKS26[w][1].strftime("%d %b 2026")),
                              "; ".join("%s (%s)" % (("%.2f" % a[w][k]) if k == "ot" else "%d" % a[w][k],
                                                     ("%.2f" % gold_a[w][k]) if k == "ot" else "%d" % gold_a[w][k])
                                        for k in KEYS + ("ot",))))
    print("\nper route, figures kept of %d:" % n)
    print("  %-46s %-14s %-12s %-12s %-12s %-10s %s" % ("", "crew dep (5)", "crew stay", "brn dep", "brn stay",
                                                     "ot hours", "all"))
    for who in ("cracker", "mirror, the cracker's ask path", "mirror, no battery", "cracker, the device found"):
        ka = routes[who][0]
        print("  %-46s %-14d %-12d %-12d %-12d %-10d %d" % (who, ka["crew_dep"], ka["crew_stay"], ka["brn_dep"],
                                                         ka["brn_stay"], ka["ot"], sum(ka.values())))
    print("  %-46s %-14d %-12d %-12d %-12d %-10d %d  (control, figures.json reproduced)" % (
        "full includer", kfa["crew_dep"], kfa["crew_stay"], kfa["brn_dep"], kfa["brn_stay"], kfa["ot"],
        sum(kfa.values())))
    for mode, lab in (("staffbadge", "stop: the doors on staff and temp badges only (the over-clean)"),
                      ("current_group", "stop: the user list's group as it stands"),
                      ("login", "stop: the notes unread"), ("paid", "stop: overtime by the pay period"),
                      ("recleans", "stop: re-cleans counted")):
        print("  %-46s %d" % (lab, sum(kept_a(C.ask_a(folder, mode), gold_a).values())))

    kc = sum(routes["cracker"][0].values())
    km_nat = sum(routes["mirror, no battery"][0].values())
    kd = sum(routes["cracker, the device found"][0].values())
    worst = []
    print("\nthe sheet's formula (38, 7, 55 over the %d figures, 8 per cent method credit on a figure not kept, r = 5):"
          % n)
    for lab, kcc, km in (("the mirror on the cracker's ask path", kc, kc), ("the mirror without the battery", kc, km_nat),
                         ("the cracker finding the device alone", kd, kc)):
        c, s_, pp = pair(kcc, km, n)
        worst.append(pp)
        print("  %s: cracker %.1f, mirror %.1f, pair %.1f" % (lab, c, s_, pp))
    both = pair(kc, kc, n)[0]
    print("  both top responses on the call (two careful responses): %.1f and %.1f, pair %.1f" % (both, both, both))
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight on the cracker's ask path (%.1f without the battery)" % (
        100.0 * (kc + CREDIT * (n - kc)) / n, 100.0 * (km_nat + CREDIT * (n - km_nat)) / n))
    print("Pair ceiling: %.1f (the worst of the pair on either mirror reading and the device found alone)" % max(worst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
