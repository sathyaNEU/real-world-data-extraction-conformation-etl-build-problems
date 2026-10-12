"""The records the district holds: the complaint system's rows (phone, web form, app; resends, two people in one
household, the January carry-over from the retired system, the app's UTC noticed times until 30 April, the
calls routed from the neighbouring district's line) and the station's 5-minute records (held-vane audits,
the June sensor outage, missing records)."""
import datetime as dt
import math

import numpy as np

import core
import world as WD

APP_FIX = dt.datetime(2026, 4, 30, 14, 0)          # local: the app release that wrote noticed times in local time
IMPORT_AT = dt.datetime(2026, 1, 6, 9, 12)          # local: the carry-over from the retired system
ROUTED = (dt.date(2026, 1, 12), dt.date(2026, 3, 27))
OUTAGE = (dt.datetime(2026, 6, 9, 14, 15), dt.datetime(2026, 6, 11, 16, 5))   # PST
EDGE_GAPS = [(dt.datetime(2026, 4, 30, 18, 0), dt.datetime(2026, 5, 1, 6, 0)),
             (dt.datetime(2026, 9, 30, 18, 0), dt.datetime(2026, 10, 1, 6, 0))]

DESC = {
    "compost": ["Rotten garbage smell, very strong outside", "Sour smell like rotting food", "Smells like a garbage truck",
                "Strong vinegar and rot smell", "Garbage smell came in through the windows", "Sour rotten odor all evening",
                "Smells like spoiled food, can't sit outside", "Rotting garbage odor again tonight",
                "Strong sour smell, like the compost place", "Sweet rotten smell, gagging"],
    "landfill": ["Garbage smell from the dump", "The dump again, strong garbage odor", "Trash smell, landfill?",
                 "Garbage odor at night", "Smells like the landfill"],
    "wwtp": ["Sewage smell", "Rotten eggs", "Sewer odor near the creek", "Smells like sewage again",
             "Rotten egg smell from the sewer plant"],
    "render": ["Dead animal smell", "Smells like the rendering plant", "Burnt meat and dead animal odor",
               "Awful dead animal smell"],
    "mush": ["Manure smell", "Strong manure odor", "Smells like the mushroom farm", "Ammonia and manure smell"],
    "frequent": ["Garbage smell from the dump again", "Same smell as every night, the dump", "Odor again, garbage",
                 "Dump smell, please do something", "Bad smell again tonight", "Sewage or garbage, can't tell",
                 "Smell is back", "Garbage odor, third night this week"],
    "background": ["Bad smell outside", "Strange odor", "Smells like garbage", "Sewage smell", "Rotten smell",
                   "Chemical smell", "Smoky and sour", "Something smells awful", "Garbage odor", "Manure smell"],
}
DESC["compost_calm"] = DESC["compost"]
DESC["wwtp_calm"] = DESC["wwtp"]
DESC["moderate"] = DESC["background"]
DURATION = ["Less than 15 minutes", "15 minutes to 1 hour", "More than 1 hour", "Still going"]
FINDING = ["No odor on arrival", "No odor on arrival", "No odor on arrival", "Faint odor, source not determined",
           "Odor confirmed at the address, source not determined"]
STAFF = ["JR", "AW", "JR"]                         # Jerome Reed, Alyssa White

# what people write (DESC above keeps the draw each complaint has always made; the words come from TEXT)
TEXT = {
    "compost": (["Rotten garbage smell", "Sour smell like rotting food", "Smells like a garbage truck",
                 "Strong vinegar and rot smell", "Sweet rotten smell", "Smells like spoiled food", "Rotting vegetable smell",
                 "Sour rotten odor", "Smell like rotting fruit and vinegar", "Strong sour smell like the compost place",
                 "Rotten food smell", "Sour garbage smell", "Smells like old food scraps", "Hot rotten garbage smell"],
                ["very strong outside", "coming in through the windows", "can't sit outside", "all evening",
                 "since about 7", "had to close all the windows", "worse than last night", "on the back patio",
                 "whole street smells like it", "gagging", "kids had to come inside", "again tonight",
                 "started after dinner", "it's in the house now", "with the breeze from the west", "strongest by the fence"]),
    "landfill": (["Garbage smell from the dump", "The dump again, strong garbage odor", "Trash smell", "Garbage odor",
                  "Smells like the landfill", "Dump smell", "Strong garbage smell", "Landfill odor"],
                 ["landfill?", "coming down the valley", "late at night", "woke us up", "every night this week",
                  "in the bedroom", "very strong", "again"]),
    "wwtp": (["Sewage smell", "Rotten eggs", "Sewer odor", "Smells like sewage", "Rotten egg smell", "Sulfur smell"],
             ["near the creek", "by the bridge", "strong at the corner", "on the walking path", "in the backyard",
              "from the treatment plant?"]),
    "render": (["Dead animal smell", "Smells like the rendering plant", "Burnt meat and dead animal odor",
                "Awful dead animal smell", "Cooked meat and rot smell", "Smells like burnt bones"],
               ["really bad tonight", "coming from the north", "around midnight", "made me sick", "in the whole house",
                "woke me up"]),
    "mush": (["Manure smell", "Strong manure odor", "Smells like the mushroom farm", "Ammonia and manure smell",
              "Barnyard smell"],
             ["from the east", "early morning", "strong ammonia", "all night", "in the car on the way to work"]),
    "background": (["Bad smell outside", "Strange odor", "Smells like garbage", "Sewage smell", "Rotten smell",
                    "Chemical smell", "Smoky and sour smell", "Something smells awful", "Garbage odor", "Manure smell",
                    "Musty sour smell", "Odor in the neighborhood"],
                   ["not sure where from", "for the last hour", "comes and goes", "pretty strong",
                    "noticed walking the dog", "in the backyard", "first time I've noticed it", "lasted a while"]),
    "moderate": (["Garbage smell again", "Sewage smell again", "Bad odor tonight", "The smell is back",
                  "Rotten smell in the neighborhood", "Strong odor again", "Smells like the dump", "Sour smell again"],
                 ["same as last week", "closed the windows", "comes and goes", "worse than usual", "late",
                  "please look into it"]),
    "routed": (["Smoke and burning smell", "Smell of manure from the fields", "Bad smell, burning",
                "Odor from a burn pile"],
               ["out by the fields", "neighbor burning?", "all evening", "strong"]),
}
TEXT["compost_calm"] = TEXT["compost"]
TEXT["wwtp_calm"] = TEXT["wwtp"]
EXTRA = ["Please send someone.", "When will this stop?", "This is the third time this week.",
         "Can't open the windows in this heat.", "Please call me back.", "It's been like this for weeks."]
# the four residents who report most nights, each in their own words
FREQ_TEXT = [
    ["Dump smell again", "Dump smell, please do something", "Same smell as every night, the dump",
     "Garbage smell from the dump again, woke me up", "Dump smell again tonight", "the dump again",
     "Dump smell. Please do something about this"],
    ["garbage odor again, same as last night", "garbage smell from the dump", "dump odor, third night this week",
     "strong garbage smell at the residence", "same garbage odor as every night"],
    ["Odor again, garbage", "Sewage or garbage, can't tell", "Bad smell again tonight", "Smell is back",
     "Bad smell again, garbage or sewage", "Same bad smell tonight", "Odor is back again"],
    ["Garbage odor, third night this week", "Smell is back, garbage", "Garbage odor again", "Garbage smell all night",
     "Garbage odor again tonight, please fix this"],
]


def compose(cause, channel, rng, freq_i=None):
    """A complainant's description: their words on the web form and in the app, the intake staff's on the phone."""
    if freq_i is not None:
        txt = FREQ_TEXT[freq_i][int(rng.integers(len(FREQ_TEXT[freq_i])))]
        if rng.random() < 0.25:
            txt += ", " + ["11 pm", "after midnight", "around 2", "early this morning", "all night"][int(rng.integers(5))]
    else:
        head, tail = TEXT[cause]
        txt = head[int(rng.integers(len(head)))]
        if rng.random() < 0.72 or len(txt.split()) < 3:
            txt += ", " + tail[int(rng.integers(len(tail)))]
        if rng.random() < 0.16:
            txt += ". " + EXTRA[int(rng.integers(len(EXTRA)))]
    if channel == "Phone" and rng.random() < 0.85:
        txt = ["Caller reports ", "Caller states ", "Reports "][int(rng.integers(3))] + txt[0].lower() + txt[1:]
    elif rng.random() < 0.12:
        txt = txt.lower()
    return txt


def address_of(h, style):
    """The service address as a person or the system writes it."""
    st = h["street"]
    if style == 1:
        st = st.replace(" St", " Street").replace(" Ave", " Avenue").replace(" Dr", " Drive").replace(" Rd", " Road")
    if style == 2:
        st = st.upper()
    s = "%d %s" % (h["num"], st)
    if h["unit"]:
        s += [" Apt %s", " #%s", " Unit %s"][style % 3] % h["unit"]
    return s


def channel_for(d, rng):
    m = d.month
    p_app = min(0.47, 0.12 + 0.045 * (m - 1))
    r = rng.random()
    return "App" if r < p_app else ("Web form" if r < p_app + 0.36 else "Phone")


def received_for(ch, noticed, rng):
    if ch == "App":
        return noticed + dt.timedelta(minutes=int(rng.integers(1, 13)))
    if ch == "Phone":
        if 7 <= noticed.hour < 22:
            return noticed + dt.timedelta(minutes=int(rng.integers(3, 31)))
        nxt = noticed.date() + dt.timedelta(1) if noticed.hour >= 22 else noticed.date()
        return dt.datetime(nxt.year, nxt.month, nxt.day, 7, 30) + dt.timedelta(minutes=int(rng.integers(0, 150)))
    lag = float(rng.exponential(2.2))
    t = noticed + dt.timedelta(minutes=int(10 + 60 * lag))
    return t


def in_gap(t):
    return any(a <= t < b for a, b in EDGE_GAPS)


def near_fix(t):
    return APP_FIX - dt.timedelta(hours=10) <= t < APP_FIX + dt.timedelta(hours=16)


def own_words(r, partner, cause, rng, freq_i=None):
    """A second person's own description: never one the first person's words contain, or the reverse."""
    for _ in range(40):
        txt = compose(cause, r["channel"], rng, freq_i)
        a, b = txt.strip().lower(), partner.strip().lower()
        if a not in b and b not in a:
            return txt
    raise AssertionError("no distinct description")


def complaints(W):
    """Every complaint row the system exports, before formatting; plus the retired system's open complaints."""
    H = W["H"]
    rng = WD.rng_for("complaints")
    # the draws below keep the order they have always had (contact ids are given out at the end, by received time)
    contacts = {}
    second = {}
    nxt = [10233]

    def contact(hid, k=0):
        tab = contacts if k == 0 else second
        if hid not in tab:
            tab[hid] = "C-%05d" % nxt[0]
            nxt[0] += int(rng.integers(1, 9))
        return tab[hid]

    freq_i = {W["freq"][i]: i for i in range(4)}
    freq_channel = {W["freq"][0]: "App", W["freq"][1]: "Phone", W["freq"][2]: "Web form", W["freq"][3]: "App"}
    rows = []
    seeds = sorted(set(W["seeds"]), key=lambda s: (s[1], s[2], s[0], s[3]))
    for hid, d, hl, cause in seeds:
        rng = WD.rng_for("c", hid, d.isoformat(), hl, cause)      # each complaint draws its own attributes
        words = WD.rng_for("w", hid, d.isoformat(), hl, cause)    # and its own words
        t = dt.datetime(d.year, d.month, d.day, hl, int(rng.integers(0, 60)))
        if in_gap(t):
            continue
        ch = freq_channel.get(hid) or channel_for(d, rng)
        if ch == "App" and near_fix(t):
            ch = "Web form"
        h = H[hid]
        style = int(rng.integers(0, 3)) if h["unit"] else (0 if rng.random() < 0.8 else int(rng.integers(1, 3)))
        r = dict(hid=hid, cause=cause, noticed=t, channel=ch, received=received_for(ch, t, rng),
                 contact=contact(hid) if cause != "moderate" else None, person=0,
                 address=address_of(h, style), desc=DESC[cause][int(rng.integers(len(DESC[cause])))],
                 intensity=int(min(5, max(1, round(rng.normal(3.4 if cause in ("compost", "compost_calm") else 2.9, 0.9))))),
                 duration=DURATION[int(rng.choice(4, p=[0.25, 0.4, 0.25, 0.1]))], kind="complaint")
        r["desc"] = compose(cause, ch, words, freq_i.get(hid))
        rows.append(r)
        # a second person in the household reports the same odor
        if cause not in ("frequent",) and rng.random() < 0.05:
            t2 = t + dt.timedelta(minutes=int(rng.choice([-9, -7, -5, -4, -3, -2, 2, 3, 4, 6, 8, 11, 12])))
            ch2 = channel_for(d, rng)
            if ch2 == "App" and near_fix(t2):
                ch2 = "Phone"
            p = dict(r, noticed=t2, channel=ch2, received=received_for(ch2, t2, rng),
                     contact=contact(hid, 1) if cause != "moderate" else None, person=1,
                     desc=DESC[cause][int(rng.integers(len(DESC[cause])))], kind="pair",
                     intensity=max(1, min(5, r["intensity"] + int(rng.integers(-1, 2)))))
            # they often give the same time: a later report takes the first one's minute (the event keeps its start)
            if t2 > t and words.random() < 0.45:
                p["noticed"] = t
            p["desc"] = own_words(p, r["desc"], cause, words)
            rows.append(p)
    # every month has a household whose two people gave the same time
    add = WD.rng_for("pairs-same-minute")
    clock = lambda r: r["channel"] == "App" and r["noticed"] < APP_FIX      # the app's UTC times until its release
    # April takes two: the app's report on the evening of March 31 reads into April on its UTC time
    need = {4: 2}
    for m in range(1, 10):
        while True:
            have = [p for p in rows if p["kind"] == "pair" and p["noticed"].month == m and
                    any(q is not p and q["hid"] == p["hid"] and q["noticed"] == p["noticed"] and clock(q) == clock(p)
                        for q in rows)]
            if len(have) >= need.get(m, 1):
                break
            cand = [r for r in rows if r["kind"] == "complaint" and r["noticed"].month == m and r["cause"] != "frequent"
                    and not near_fix(r["noticed"]) and not any(q["kind"] == "pair" and q["hid"] == r["hid"] and
                                                               q["noticed"].date() == r["noticed"].date() for q in rows)]
            r = cand[int(add.integers(len(cand)))]
            ch2 = ["Phone", "Web form", "App"][int(add.integers(3))]
            if r["noticed"] < APP_FIX:
                ch2 = "App" if r["channel"] == "App" else ("Phone" if ch2 == "App" else ch2)
            p = dict(r, channel=ch2, received=received_for(ch2, r["noticed"], add), contact=None, person=1, kind="pair",
                     intensity=max(1, min(5, r["intensity"] + int(add.integers(-1, 2)))),
                     duration=DURATION[int(add.integers(0, 3))])
            p["desc"] = own_words(p, r["desc"], r["cause"], add)
            rows.append(p)
    rng = WD.rng_for("complaints-late")
    words = WD.rng_for("complaints-late-words")
    # app reports on the last evening of January, February and March, which the app's UTC times carry into the
    # next month
    for day, hl in ((dt.date(2026, 1, 31), 20), (dt.date(2026, 2, 28), 19), (dt.date(2026, 3, 31), 21)):
        hid = int(rng.integers(len(H)))
        t = dt.datetime(day.year, day.month, day.day, hl, int(rng.integers(0, 60)))
        rows.append(dict(hid=hid, cause="background", noticed=t, channel="App", received=received_for("App", t, rng),
                         contact=contact(hid), person=0, address=address_of(H[hid], 0),
                         desc=DESC["background"][int(rng.integers(len(DESC["background"])))],
                         intensity=int(rng.integers(2, 5)), duration=DURATION[int(rng.integers(0, 3))], kind="complaint"))
        rows[-1]["desc"] = compose("background", "App", words)
    # app resends: the offline queue sends the saved draft of a delivered report again under a new number
    resends = []
    by_month = {}
    for r in rows:
        if r["channel"] == "App" and r["kind"] in ("complaint", "pair"):
            by_month.setdefault(r["noticed"].month, []).append(r)
    for m in sorted(by_month):
        cand = by_month[m]
        pick = [r for r in cand if rng.random() < 0.06]
        while len(pick) < 2 and len(pick) < len(cand):
            r = cand[int(rng.integers(len(cand)))]
            if r not in pick:
                pick.append(r)
        for j, r in enumerate(pick):
            ws = r["desc"].split()
            k = max(2, min(len(ws) - 1, int(rng.integers(2, 6))))
            draft = " ".join(ws[:k])
            new_reg = j == 0 or rng.random() < 0.45     # the app re-registered after an update: a new contact record
            if new_reg:
                rng.integers(0, 10000)
            resends.append(dict(r, received=r["received"] + dt.timedelta(minutes=int(rng.integers(35, 14 * 60))),
                                desc=draft, kind="resend", new_reg=new_reg))
    rows += resends
    # calls routed from the neighbouring district's line, January to March
    routed = []
    d = ROUTED[0]
    while d <= ROUTED[1]:
        if rng.random() < 0.16:
            x, y = -3.6 - rng.uniform(0, 1.4), -1.2 + rng.uniform(-1.0, 1.4)
            lat, lon = core.to_latlon(x, y)
            num = int(4000 + 10 * int(rng.integers(1, 300)))
            st = ["Lone Pine Rd", "Wheatland Rd", "Cordova Ln", "Stagecoach Rd"][int(rng.integers(4))]
            t = dt.datetime(d.year, d.month, d.day, int(rng.choice([7, 8, 18, 19, 20, 21])), int(rng.integers(0, 60)))
            routed.append(dict(hid=None, cause="routed", noticed=t, channel="Phone",
                               received=t + dt.timedelta(minutes=int(rng.integers(3, 30))),
                               contact=None, person=0, address="%d %s" % (num, st), lat=lat, lon=lon,
                               desc=compose("routed", "Phone", words),
                               intensity=int(rng.integers(2, 5)), duration=DURATION[int(rng.integers(0, 3))],
                               kind="routed", geocode="Street segment"))
            rng.integers(4)
        d += dt.timedelta(1)
    rows += routed
    # the retired system's open complaints, carried over on 6 January
    legacy = []
    for i in range(38):
        hid = int(rng.integers(len(H)))
        day = dt.date(2025, 11, 10) + dt.timedelta(int(rng.integers(0, 51)))
        t = dt.datetime(day.year, day.month, day.day, int(rng.choice([6, 7, 19, 20, 21, 22])), int(rng.integers(0, 60)))
        cause = ["background", "landfill", "wwtp", "background", "render"][int(rng.integers(5))]
        ch = ["Phone", "Web form"][int(rng.integers(2))]
        legacy.append(dict(hid=hid, cause=cause, noticed=t, channel=ch,
                           received=received_for("Phone", t, rng), contact=contact(hid), person=0,
                           address=address_of(H[hid], 0),
                           desc=DESC[cause][int(rng.integers(len(DESC[cause])))], intensity=int(rng.integers(2, 5)),
                           duration=DURATION[int(rng.integers(0, 3))], kind="legacy",
                           ocs_no="OCS-25-%04d" % (1100 + 3 * i + int(rng.integers(0, 3)))))
        legacy[-1]["desc"] = compose(cause, ch, words)
    legacy.sort(key=lambda r: r["noticed"])
    imported = []
    for i, r in enumerate(legacy):
        t = IMPORT_AT + dt.timedelta(seconds=int(25 * i + rng.integers(0, 20)))
        imported.append(dict(r, received=t.replace(second=0, microsecond=0), noticed_export=t.replace(second=0),
                             kind="imported"))
    rows += imported
    # five complaints from the first two days of October, outside every window
    late = WD.rng_for("october")
    for k in range(5):
        hid = int(late.integers(len(H)))
        t = dt.datetime(2026, 10, 1, 7, 0) + dt.timedelta(minutes=int(late.integers(0, 24 * 60)))
        rows.append(dict(hid=hid, cause="background", noticed=t, channel="Web form",
                         received=t + dt.timedelta(minutes=int(late.integers(12, 95))), contact=None, person=0,
                         address=address_of(H[hid], 0), desc=compose("background", "Web form", late),
                         intensity=int(late.integers(2, 5)), duration=DURATION[int(late.integers(0, 3))],
                         kind="complaint", cause_late=True))
    # follow-ups and export fields
    for r in rows:
        r.setdefault("lat", None)
        r["follow"] = ""
        r["finding"] = ""
        r["staff"] = ""
    for r in rows:
        if r["kind"] in ("complaint", "pair") and rng.random() < 0.24:
            r["follow"] = "Call back" if rng.random() < 0.7 else "Site visit"
            r["staff"] = STAFF[int(rng.integers(len(STAFF)))]
            if r["follow"] == "Site visit":
                r["finding"] = FINDING[int(rng.integers(len(FINDING)))]
    assign_contacts(rows)
    # the same household within one night writes its address the way it did earlier that night
    last = {}
    for r in sorted(rows, key=lambda r: (r["noticed"], r["received"], r["kind"], r["desc"])):
        if r["hid"] is None or r["kind"] == "imported":
            continue
        prev = last.get(r["hid"])
        if prev is not None and r["noticed"] - prev["noticed"] <= dt.timedelta(hours=3):
            r["address"] = prev["address"]
        last[r["hid"]] = r
    return rows, legacy, contacts, second


def assign_contacts(rows):
    """Contact records as the system creates them: one per phone number, e-mail address or app registration, in
    the order they first bring in a complaint; an app that re-registers after an update is a new registration
    from then on."""
    rng = WD.rng_for("contact-ids")
    regs = {}
    for r in rows:
        if r["kind"] == "resend" and r.get("new_reg"):
            regs.setdefault((r["hid"], r["person"]), []).append(r["received"])
    ids = {}
    nxt = 10233
    for r in sorted(rows, key=lambda r: (r["received"], r["noticed"], r["kind"], str(r["hid"]), r["desc"])):
        if r["kind"] == "routed":
            key = ("phone", r["address"])
        elif r["channel"] == "App":
            gen = sum(1 for t in regs.get((r["hid"], r["person"]), []) if t <= r["received"])
            key = ("app", r["hid"], r["person"], gen)
        else:
            key = ("phone" if r["channel"] == "Phone" else "email", r["hid"], r["person"])
        if key not in ids:
            ids[key] = "C-%05d" % nxt
            nxt += int(rng.integers(1, 6))
        r["contact"] = ids[key]


def exported_noticed(r):
    """The noticed time as the export carries it: the app wrote UTC with no offset before its 30 April fix, and
    the carry-over took the import time."""
    if r["kind"] == "imported":
        return r["noticed_export"]
    if r["channel"] == "App" and r["noticed"] < APP_FIX:
        return r["noticed"].replace(tzinfo=core.LOCAL).astimezone(core.UTC).replace(tzinfo=None)
    return r["noticed"]


# ----------------------------------------------------------------------------------------------------------------
# the station's records

def audits():
    """One monthly audit a month on a weekday morning (PST): the technician holds the vane."""
    rng = WD.rng_for("audits")
    out = []
    for m in range(1, 10):
        d = dt.date(2026, m, 8) + dt.timedelta(int(rng.integers(0, 10)))
        while d.weekday() >= 5:
            d += dt.timedelta(1)
        if OUTAGE[0].date() - dt.timedelta(1) <= d <= OUTAGE[1].date() + dt.timedelta(1):
            d = OUTAGE[1].date() + dt.timedelta(5)          # June's audit waited for the new monitor
        t0 = dt.datetime(d.year, d.month, d.day, 9, 0) + dt.timedelta(minutes=5 * int(rng.integers(2, 10)))
        t1 = t0 + dt.timedelta(minutes=5 * int(rng.integers(8, 31)))
        out.append((t0, t1))
    return out


OTHER_WORK = ["PM2.5 monitor filter tape changed", "PM2.5 flow audit, within limits",
              "Temperature probe comparison, within 0.2 C", "Shelter air conditioner serviced", "Pyranometer dome cleaned"]


def other_work():
    """The station's other work by month: (date, start time, text)."""
    rng = WD.rng_for("maint")
    out = []
    for m in range(1, 10):
        d = dt.date(2026, m, 2) + dt.timedelta(int(rng.integers(0, 20)))
        while d.weekday() >= 5:
            d += dt.timedelta(1)
        t = dt.datetime(d.year, d.month, d.day, int(rng.integers(8, 14)), 5 * int(rng.integers(0, 12)))
        out.append((t, OTHER_WORK[int(rng.integers(5))]))
    return out


def station_records(W):
    """{date: [(minute, ws, wd, sigma, t2, t10, solar, qc)]} in PST with sentinels and missing records."""
    rng = WD.rng_for("station")
    held = audits() + [OUTAGE]
    out = {}
    for d in core.DAYS:
        plan = W["plans"][d]
        recs = []
        for (mi, sp, dr, sig) in W["recs"][d]:
            t = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=mi)
            hr = mi / 60.0
            doy = (d - dt.date(2026, 1, 1)).days
            tbase = 8.0 + 14.0 * max(0.0, math.sin(math.pi * (doy - 20) / 330.0)) ** 1.3
            diurnal = 7.5 * math.sin(math.pi * (hr - 8.0) / 14.0) if 8.0 <= hr <= 22.0 else -2.5
            t2 = tbase + diurnal + rng.normal(0, 0.4)
            inv = (1.8 if plan["reg"][int(hr)] in ("drain", "calm", "nslope", "ecanyon", "transition") else -0.6)
            t10 = t2 + inv + rng.normal(0, 0.2)
            sol = max(0.0, 980.0 * math.sin(math.pi * (hr - 5.6) / 13.6)) if 5.6 < hr < 19.2 else 0.0
            if plan["kind"] == "storm":
                sol *= 0.3
            sol = max(0.0, sol * rng.uniform(0.85, 1.02))
            qc = "V"
            if any(a <= t < b for a, b in held):
                sp, dr, sig = 0.0, 0.0, 0.0
            recs.append([mi, sp, dr, sig, t2, t10, sol, qc])
        out[d] = recs
    # missing records: logger comms drops, a few longer gaps (never in the hours that open a local month)
    for d in core.DAYS:
        for r in out[d]:
            if rng.random() < 0.0035:
                r[7] = "M"
        if rng.random() < 0.035:
            s = int(rng.integers(0, 288 - 18))
            for r in out[d][s:s + int(rng.integers(5, 18))]:
                r[7] = "M"
        for r in out[d]:
            if (d, r[0] // 60) in WD.FORCED:
                r[7] = "V"
    return out, held
