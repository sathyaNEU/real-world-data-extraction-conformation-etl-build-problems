"""The records each system holds: the ICB warehouse's acute discharge spells (with the resubmissions a pathway
correction leaves) and the trusts' ward stays, the community equipment service's order lines, the council
brokerage's referrals, the council's spot-purchase invoice lines, the national weekly return, the daily bed
census and the reablement outcomes."""
import datetime as dt

import core
import world as W

DEST = {0: "Usual place of residence, no new support", 1: "Usual place of residence, with care support",
        2: "Rehabilitation or reablement bed", 3: "Care home"}
P1_CARE = {"New": "New package", "Restart": "Restart of existing package"}
EQUIP_ITEMS = ["Profiling bed", "Pressure-relieving mattress", "Mobile hoist", "Commode", "Bath lift",
               "Perching stool", "Walking frame", "Toilet frame", "Riser-recliner chair", "Bed lever", "Shower chair",
               "Raised toilet seat"]
# wards: code, name, specialty, beds; the first ward at each site is its assessment unit
WARDS = {
    "RMC01": [("RMH-AMU", "Acute Medical Unit", "Acute medicine", 56),
              ("RMH-W10", "Wren Ward", "Care of the elderly", 30), ("RMH-W11", "Kestrel Ward", "Care of the elderly", 30),
              ("RMH-W12", "Plover Ward", "Care of the elderly", 28), ("RMH-W13", "Curlew Ward", "Care of the elderly", 28),
              ("RMH-W14", "Rowan Ward", "General medicine", 28), ("RMH-W15", "Sparrow Ward", "General medicine", 28),
              ("RMH-W16", "Merlin Ward", "General medicine", 26), ("RMH-W17", "Linnet Ward", "Respiratory medicine", 26),
              ("RMH-W18", "Hawthorn Ward", "Respiratory medicine", 26), ("RMH-W19", "Willow Ward", "Cardiology", 24),
              ("RMH-W20", "Alder Ward", "Gastroenterology", 24), ("RMH-W21", "Ash Ward", "Trauma and orthopaedics", 28),
              ("RMH-W23", "Beech Ward", "Trauma and orthopaedics", 26), ("RMH-W22", "Elm Ward", "General surgery", 28)],
    "RMC02": [("WBH-AMU", "Medical Assessment Unit", "Acute medicine", 34),
              ("WBH-W2", "Teal Ward", "Care of the elderly", 28), ("WBH-W3", "Heron Ward", "General medicine", 26),
              ("WBH-W4", "Swift Ward", "Care of the elderly", 28), ("WBH-W5", "Larch Ward", "Rehabilitation", 24),
              ("WBH-W6", "Holly Ward", "Trauma and orthopaedics", 22), ("WBH-W7", "Lapwing Ward", "General medicine", 26),
              ("WBH-W8", "Oak Ward", "Care of the elderly", 26), ("WBH-W9", "Poplar Ward", "Respiratory medicine", 24),
              ("WBH-W10", "Finch Ward", "General surgery", 24), ("WBH-W11", "Robin Ward", "General medicine", 24)],
    "RSM01": [("AVH-MAU", "Medical Assessment Unit", "Acute medicine", 28),
              ("AVH-W3", "Bramble Ward", "Care of the elderly", 28), ("AVH-W4", "Clover Ward", "General medicine", 26),
              ("AVH-W5", "Primrose Ward", "Care of the elderly", 28), ("AVH-W6", "Bluebell Ward", "General medicine", 26),
              ("AVH-W7", "Fern Ward", "General surgery", 24), ("AVH-W8", "Hazel Ward", "Trauma and orthopaedics", 22),
              ("AVH-W9", "Foxglove Ward", "Respiratory medicine", 24), ("AVH-W10", "Heather Ward", "Care of the elderly", 26),
              ("AVH-W11", "Iris Ward", "Cardiology", 20)],
    "RSM02": [("CPH-MAU", "Medical Assessment Unit", "Acute medicine", 26),
              ("CPH-W1", "Juniper Ward", "Care of the elderly", 26), ("CPH-W2", "Laurel Ward", "General medicine", 24),
              ("CPH-W3", "Cedar Ward", "Care of the elderly", 26), ("CPH-W4", "Maple Ward", "General surgery", 20),
              ("CPH-W5", "Aspen Ward", "General medicine", 24), ("CPH-W6", "Sycamore Ward", "Respiratory medicine", 22),
              ("CPH-W7", "Hornbeam Ward", "Trauma and orthopaedics", 20), ("CPH-W9", "Meadow Ward", "Step-down", 24)],
    "RSM03": [("HIF-MAU", "Medical Assessment Unit", "Acute medicine", 28),
              ("HIF-W5", "Sorrel Ward", "Care of the elderly", 26), ("HIF-W6", "Thistle Ward", "General medicine", 24),
              ("HIF-W7", "Tansy Ward", "Care of the elderly", 26), ("HIF-W8", "Yarrow Ward", "General surgery", 22),
              ("HIF-W9", "Comfrey Ward", "General medicine", 24), ("HIF-W10", "Campion Ward", "Respiratory medicine", 22),
              ("HIF-W11", "Teasel Ward", "Trauma and orthopaedics", 20), ("HIF-W12", "Vetch Ward", "Care of the elderly", 24)],
}
RECEIVING_WARD = {"RMC02": "WBH-W5", "RSM02": "CPH-W9"}
# the share of a ward's beds patients aged 65 and over take on a full night, by specialty; younger patients hold the
# rest, and the share moves week to week with the ward's case mix
SHARE_65 = {"Care of the elderly": 0.93, "Rehabilitation": 0.88, "Step-down": 0.9, "General medicine": 0.82,
            "Respiratory medicine": 0.79, "Trauma and orthopaedics": 0.74, "Cardiology": 0.68, "Gastroenterology": 0.65,
            "General surgery": 0.57, "Acute medicine": 0.72}
# the most escalation beds each site opens on a winter night
ESCALATION = {"RMC01": 17, "RMC02": 8, "RSM01": 13, "RSM02": 9, "RSM03": 5}
FRAMEWORK = {"Marchford": ["Marchford Home Support", "Bluebell Care", "Carewell Homecare"],
             "Ashby": ["Vale Homecare", "Ashby Community Care", "Bluebell Care"],
             "Teme Valley": ["Teme Valley Care", "Riverside Homecare", "Carewell Homecare"]}
SPOT = ["Hillcrest Nursing Agency", "Maple Leaf Care Ltd", "Brightside Support Services", "Severn Vale Care Agency"]
SOURCES = ["GP practice", "District nursing", "Family or carer", "Self-referral", "Adult social care team"]


def dtime(d, h0, h1, rng):
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(rng.integers(h0 * 60, h1 * 60)))


def build():
    stays = W.stays()
    persons, pool, eligible_seen, busy = {}, {}, set(), {}
    spells, lates = [], []
    for s in stays:
        rr2 = W.rng_for("times", *s["key"])
        R = s["mofd"]
        adm_t = dtime(R - dt.timedelta(s["los_pre"]), 0, 24, rr2)
        if s["pathway"] == 1:
            care_start = R + dt.timedelta(s["care_wait"])
            equip = R + dt.timedelta(s["equip_lag"]) if s["equip_lag"] is not None else None
            dis_d = max([R, care_start] + ([equip] if equip else []))
            p1 = "New" if s["care_wait"] > 0 else "Restart"
        else:
            care_start, equip, p1 = None, None, None
            dis_d = R + dt.timedelta(s["delay"])
        dis_t = dtime(dis_d, 10, 19, rr2)
        if dis_d < core.REC0:
            continue
        late = dis_d > core.REC1          # still in hospital at the extract's end: on the bed census only
        rr = W.rng_for("person", *s["key"])
        site = s["site"]
        if "home" not in s:
            homes = W.HOME[site]
            s["home"] = list(homes)[int(rr.choice(len(homes), p=list(homes.values())))]
        home = s["home"]
        covered = (s["pathway"] == 1 and core.in_winter(s["mofd"]) and home != "Severnside" and s["care_wait"] > 0)
        win = (adm_t.date() - dt.timedelta(35), dis_d + dt.timedelta(35))
        nhs = None
        if pool.get(home) and rr.random() < 0.18:
            cand = pool[home][int(rr.integers(len(pool[home])))]
            clash = any(not (win[1] < a or b < win[0]) for a, b in busy.get(cand, []))
            if not (covered and cand in eligible_seen) and not clash:
                nhs = cand
        if nhs is None:
            nhs = W.nhs_number(rr)
            while nhs in persons:
                nhs = W.nhs_number(rr)
            pcs = W.POSTCODES[home]
            persons[nhs] = dict(nhs=nhs, home=home, practice=W.practice_for(home, rr),
                                postcode=pcs[int(rr.integers(len(pcs)))],
                                person_id="MC%07d" % int(rr.integers(1000000, 9999999)),
                                age0=s["age"], year0=s["mofd"].year)
            pool.setdefault(home, []).append(nhs)
        busy.setdefault(nhs, []).append((adm_t.date(), dis_d))
        if covered:
            eligible_seen.add(nhs)
        p = persons[nhs]
        age = p["age0"] + (s["mofd"].year - p["year0"])
        sp = dict(key=s["key"], nhs=nhs, site=site, adm_t=adm_t, ready=R, dis_t=dis_t, pathway=s["pathway"],
                  p1=p1, care_start=care_start, equip=equip, age=age, home=home, delay=(dis_d - R).days)
        # delayed patients waiting for a rehabilitation bed or a care home are moved to the trust's sister site;
        # the spell continues and ends at the site that discharges them
        if (s["pathway"] in (2, 3) and site in core.TRANSFER_TO and sp["delay"] >= 4
                and rr2.random() < (0.30 if site == "RSM03" else 0.22)):
            t = R + dt.timedelta(int(rr2.integers(1, sp["delay"])))
            sp["transfer_from"], sp["site"] = site, core.TRANSFER_TO[site]
            sp["transfer_t"] = dtime(t, 9, 16, rr2)
        (lates if late else spells).append(sp)
    spells.sort(key=lambda x: (x["dis_t"], x["key"]))
    nums = {"RMC": 6100000, "RSM": 7300000}
    for sp in spells:
        tr = core.HOSPITALS[sp["site"]]["trust"]
        nums[tr] += 1 + int(W.rng_for("spn", *sp["key"]).integers(0, 4))
        sp["spell"] = "%s%07d" % ("1" if tr == "RMC" else "2", nums[tr] % 10000000)
        sp["trust"] = tr
    for i, sp in enumerate(sorted(lates, key=lambda x: x["key"])):
        sp["spell"], sp["trust"] = "L%06d" % i, core.HOSPITALS[sp["site"]]["trust"]
    return dict(stays=stays, spells=spells, persons=persons, lates=lates)


def nudge(R, site, n):
    """Bring forward by a day the equipment delivery of the first n covered patients at the site whose equipment
    came after their discharge ready date and before their discharge (each adds one night to the site's total)."""
    done = 0
    for sp in sorted(R["spells"], key=lambda x: x["key"]):
        if done == n:
            break
        if (sp["site"] == site and sp["pathway"] == 1 and sp["p1"] == "New" and core.in_winter(sp["ready"])
                and sp["home"] != "Severnside" and sp["equip"] is not None
                and sp["ready"] < sp["equip"] < sp["dis_t"].date()):
            sp["equip"] -= dt.timedelta(1)
            done += 1
    assert done == n
    return done


def submissions(spells):
    """The warehouse rows: one per spell, and a second, later row for each spell whose pathway the trust corrected
    (a patient recorded for a rehabilitation bed who went to a care home, or the reverse)."""
    rows = []
    for sp in spells:
        rows.append(dict(sp, pw_sub=sp["pathway"], sub_d=(sp["dis_t"] + dt.timedelta(days=3)).date()))
        if sp["pathway"] in (2, 3):
            r = W.rng_for("corr", sp["spell"])
            if r.random() < 0.07 and sp["dis_t"].date() <= core.REC1 - dt.timedelta(40):
                # the first submission carried the pathway the patient was waiting for and the day the bed was
                # booked for; the correction carries where they went and when
                rows[-1]["pw_sub"] = 5 - sp["pathway"]
                early = min(int(r.integers(1, 5)), (sp["dis_t"].date() - sp["ready"]).days)
                rows[-1]["dis_sub"] = sp["dis_t"] - dt.timedelta(days=early)
                rows.append(dict(sp, pw_sub=sp["pathway"],
                                 sub_d=(sp["dis_t"] + dt.timedelta(days=int(r.integers(9, 40)))).date()))
    rows.sort(key=lambda x: (x["sub_d"], x["spell"], x["pw_sub"] == x["pathway"]))
    for i, row in enumerate(rows):
        row["sub_id"] = 880000 + 3 * i + int(W.rng_for("sub", row["spell"], i).integers(0, 3))
    return rows


def _midnights(a, b):
    """The dates of the nights (the evening each begins) a stay from a to b spans at midnight."""
    d = a.date()
    out = []
    while True:
        mid = dt.datetime(d.year, d.month, d.day) + dt.timedelta(1)
        if mid > b:
            return out
        if mid > a:
            out.append(d)
        d += dt.timedelta(1)


def _arrive(left, gap_min):
    """When the patient reaches the next ward: a gap of gap_min minutes, closed up when it would hold a midnight
    (running past one, or starting on one)."""
    t = left + dt.timedelta(minutes=gap_min)
    if t.date() != left.date() or (left.hour == 0 and left.minute == 0):
        return left
    return t


def ward_stays(spells):
    """Each spell's ward stays: the assessment unit, a base ward with a bed free (the bed manager places patients
    where the ward has room), any move inside the site, and for a moved patient the receiving site's ward."""
    beds = {w[0]: w[3] for ws in WARDS.values() for w in ws}
    spec = {w[0]: w[2] for ws in WARDS.values() for w in ws}
    load = {}                                   # (ward, night) -> patients aged 65 and over in a bed
    caps = {}

    off = {w: -0.10 + 0.17 * W.rng_for("woff", w).random() for w in beds}

    def cap(ward, n):
        k = (ward, n.toordinal() // 7)
        if k not in caps:
            r = W.rng_for("wcap", *k)
            caps[k] = int(beds[ward] * min(0.97, SHARE_65[spec[ward]] + off[ward] + 0.06 * (r.random() - 0.5)))
        return caps[k]

    def room(ward, a, b):
        return all(load.get((ward, n), 0) < cap(ward, n) for n in _midnights(a, b))

    def take(ward, a, b):
        for n in _midnights(a, b):
            load[(ward, n)] = load.get((ward, n), 0) + 1

    def place(cands, a, b, r):
        w = [beds[c] for c in cands]
        order = list(r.choice(len(cands), size=len(cands), replace=False, p=[x / sum(w) for x in w]))
        for i in order:
            if room(cands[i], a, b):
                return cands[i]
        return min(cands, key=lambda c: max([load.get((c, n), 0) for n in _midnights(a, b)] or [0]) / beds[c])

    out = []
    for sp in sorted(spells, key=lambda x: (x["adm_t"], x["spell"])):
        r = W.rng_for("ward", sp["spell"])
        site0 = sp.get("transfer_from", sp["site"])
        wards = WARDS[site0]
        end0 = sp.get("transfer_t", sp["dis_t"])
        t = sp["adm_t"]
        amu_h = int(r.integers(5, 40))
        seq = []
        gap = int(r.integers(10, 90))
        amu_end = t + dt.timedelta(hours=amu_h)
        # a full assessment unit sends the patient straight to a base ward
        amu_free = all(load.get((wards[0][0], n), 0) < beds[wards[0][0]] for n in _midnights(t, amu_end))
        if (end0 - t).total_seconds() / 3600 > amu_h + 6 and amu_free:
            seq.append((wards[0][0], t, amu_end))
            t = _arrive(amu_end, gap)
        hours_left = (end0 - t).total_seconds() / 3600
        cands = [w[0] for w in wards[1:]]
        if hours_left >= 96 and r.random() < 0.25:
            mid = t + dt.timedelta(hours=int(r.integers(24, int(hours_left) - 24)))
            t2 = _arrive(mid, int(r.integers(15, 120)))
            first = place(cands, t, mid, r)
            seq.append((first, t, mid))
            seq.append((place([c for c in cands if c != first], t2, end0, r), t2, end0))
        else:
            seq.append((place(cands, t, end0, r), t, end0))
        if sp.get("transfer_from"):
            t3 = end0 + dt.timedelta(minutes=int(r.integers(30, 150)))
            seq.append((RECEIVING_WARD[sp["site"]], t3, sp["dis_t"]))
        for w, a, b in seq:
            assert b > a, (sp["spell"], w, a, b)
            take(w, a, b)
            out.append(dict(spell=sp["spell"], trust=sp["trust"], ward=w, start=a, end=b))
    return out


def hospital_numbers(spells):
    """Each trust's own patient number for each NHS number."""
    out = {}
    for sp in spells:
        k = (sp["trust"], sp["nhs"])
        if k not in out:
            r = W.rng_for("hn", *k)
            out[k] = ("M" if sp["trust"] == "RMC" else "S") + "%07d" % int(r.integers(1000000, 9999999))
    return out


def in_hospital(spells):
    """Per NHS number, the windows around each stay when no community order or referral is placed."""
    win = {}
    for sp in spells:
        win.setdefault(sp["nhs"], []).append((sp["adm_t"].date() - dt.timedelta(14), sp["dis_t"].date() + dt.timedelta(7)))
    return win


def free(win, nhs, d):
    return all(not (a <= d <= b) for a, b in win.get(nhs, []))


def equipment(R):
    """Order lines: one order for each pathway-1 discharge of a Marchshire resident that needed equipment, every
    line delivered on one van; a few discharge orders cancelled; and the community's orders and collections."""
    rows = []
    win = in_hospital(R["spells"] + R["lates"])
    for sp in R["spells"]:
        if sp["pathway"] != 1 or sp["home"] == "Severnside":
            continue
        r = W.rng_for("eq", sp["spell"])
        depot = core.HOSPITALS[sp["site"]]["depot"]
        if sp["equip"] is None:
            if r.random() < 0.03:
                ordered = max(sp["ready"] - dt.timedelta(int(r.integers(0, 3))), sp["adm_t"].date())
                rows.append(dict(nhs=sp["nhs"], item=EQUIP_ITEMS[int(r.integers(4))], ordered=ordered,
                                 required=sp["ready"], delivered=None, collected=None, depot=depot,
                                 route="Hospital discharge", status="Cancelled", key=("d", sp["spell"])))
            continue
        ordered = max(min(sp["ready"] - dt.timedelta(int(r.integers(0, 3))), sp["equip"]), sp["adm_t"].date())
        n = 1 + int(r.random() < 0.55) + int(r.random() < 0.25)
        pick = EQUIP_ITEMS[:7] if depot == "South" else EQUIP_ITEMS[:9]
        for k in sorted(r.choice(len(pick), size=n, replace=False)):
            rows.append(dict(nhs=sp["nhs"], item=pick[int(k)], ordered=ordered, required=sp["ready"],
                             delivered=sp["equip"], collected=None, depot=depot, route="Hospital discharge",
                             status="Delivered", key=("d", sp["spell"])))
    pool = sorted(nhs for nhs, p in R["persons"].items() if p["home"] != "Severnside")
    d = core.REC0
    while d <= core.REC1:
        r = W.rng_for("ceq", d.isoformat())
        n = int(r.poisson(38.0 if d.weekday() < 5 else 1.0))
        for k in range(n):
            nhs = pool[int(r.integers(len(pool)))]
            if not free(win, nhs, d):
                continue
            p = R["persons"][nhs]
            depot = "North" if p["home"] == "Marchford" else "South"
            u = r.random()
            lag = int(r.integers(1, 6)) + (int(r.integers(0, 5)) if depot == "South" and d.month in (12, 1, 2) else 0)
            status = "Delivered" if u < 0.80 else ("Cancelled" if u < 0.88 else "Collected")
            if status != "Cancelled":
                extra = depot == "South" and d.month in (12, 1, 2)
                lag = W.rebook(d, lag, lambda g: int(g.integers(1, 6)) + (int(g.integers(0, 5)) if extra else 0),
                               W.DEPOT_WEEKEND, W.rng_for("ceqweek", d.isoformat(), k))
            dl = None if status == "Cancelled" else d + dt.timedelta(lag)
            col = dl + dt.timedelta(int(r.integers(20, 200))) if status == "Collected" else None
            if col is not None and col > core.REC1:
                col, status = None, "Delivered"
            route = ["Community nursing", "Occupational therapy", "Reablement", "Physiotherapy"][int(r.integers(4))]
            for j in range(1 + int(r.random() < 0.3)):
                rows.append(dict(nhs=nhs, item=EQUIP_ITEMS[int(r.integers(len(EQUIP_ITEMS)))], ordered=d,
                                 required=d + dt.timedelta(int(r.integers(2, 8))), delivered=dl, collected=col,
                                 depot=depot, route=route, status=status, key=("c", d.isoformat(), k)))
        d += dt.timedelta(1)
    for row in rows:
        if row["delivered"] is not None and row["delivered"] > core.SEEN:
            row["delivered"], row["collected"], row["status"] = None, None, "Ordered"
    rows.sort(key=lambda x: (x["ordered"], x["nhs"], x["key"], x["item"]))
    order_no, i = {}, 0
    for row in rows:
        if row["key"] not in order_no:
            i += 1
            order_no[row["key"]] = "EQ%06d" % (310000 + 3 * i + int(W.rng_for("eqn", i).integers(0, 3)))
        row["order_no"] = order_no[row["key"]]
        row["postcode"] = R["persons"][row["nhs"]]["postcode"]
    return rows


def referrals(R):
    """The brokerage's referrals for home care: one from the ward for each pathway-1 patient of Marchshire who needs
    a new package, and the community's. Care starts on the day a ward's patient goes home. A referral the brokerage
    cannot place with a framework provider is closed and passed to the council's commissioners, who buy the care
    from a spot provider."""
    rows = []
    persons = R["persons"]
    for sp in R["spells"]:
        if sp["pathway"] != 1 or sp["p1"] != "New" or sp["home"] == "Severnside":
            continue
        r = W.rng_for("ref", sp["spell"])
        ref_d = sp["ready"] - dt.timedelta(int(r.random() < 0.35))
        base = dict(person=persons[sp["nhs"]], source="Hospital discharge", site=sp["site"],
                    ref_t=dtime(ref_d, 8, 18, r), pc_style=0, nhs_shown=True)
        if r.random() < 0.10:
            # no framework provider could take it: commissioning bought the care from a spot provider, who started
            # on the day the patient went home
            rows.append(dict(base, start=None, status="Closed", spot=sp["dis_t"].date()))
        else:
            rows.append(dict(base, start=sp["dis_t"].date(), status="Started", spot=None))
    win = in_hospital(R["spells"] + R["lates"])
    pool = sorted(nhs for nhs, p in persons.items() if p["home"] != "Severnside")
    d = core.REC0
    while d <= core.REC1:
        r = W.rng_for("cref", d.isoformat())
        n = int(r.poisson(9.0 if d.weekday() < 5 else 1.5))
        for k in range(n):
            nhs = pool[int(r.integers(len(pool)))]
            if not free(win, nhs, d):
                continue
            p = persons[nhs]
            ref_t = dtime(d, 8, 18, r) if d.weekday() < 5 else dtime(d, 9, 13, r)
            wf = W.winter_factor(d)
            u = r.random()
            wait = max(1, int(round(W.skewed(r.random(), 6.8, 0.55) * (0.6 + 0.4 * wf))))
            spot_wait = max(2, int(round(W.skewed(r.random(), 6.0, 0.45) * (0.75 + 0.25 * wf))))
            rw = W.rng_for("cweek", d.isoformat(), k)
            fw, fs = 0.6 + 0.4 * wf, 0.75 + 0.25 * wf
            wait = W.rebook(d, wait, lambda g: max(1, int(round(W.skewed(g.random(), 6.8, 0.55) * fw))),
                            W.CARE_WEEKEND, rw)
            spot_wait = W.rebook(d, spot_wait, lambda g: max(2, int(round(W.skewed(g.random(), 6.0, 0.45) * fs))),
                                 W.CARE_WEEKEND, rw)
            style = 0 if r.random() < 0.94 else 1 + int(r.integers(3))
            shown = r.random() < 0.7
            src = SOURCES[int(r.integers(len(SOURCES)))]
            base = dict(person=p, source=src, site=None, ref_t=ref_t, pc_style=style, nhs_shown=shown)
            if u < 0.08:
                rows.append(dict(base, start=None, status="Cancelled", spot=None))
            elif u < 0.16:
                rows.append(dict(base, start=None, status="Closed", spot=None))
            elif u < 0.30:
                rows.append(dict(base, start=None, status="Closed", spot=d + dt.timedelta(spot_wait)))
            else:
                rows.append(dict(base, start=d + dt.timedelta(wait), status="Started", spot=None))
        d += dt.timedelta(1)
    for row in rows:
        if row["start"] is not None and row["start"] > core.SEEN:
            row["start"], row["status"] = None, "Open"          # care not yet started when the extract ran
    rows.sort(key=lambda x: (x["ref_t"], x["person"]["person_id"]))
    for i, row in enumerate(rows):
        r = W.rng_for("prov", i)
        row["ref_no"] = "BR%06d" % (240000 + 3 * i + int(r.integers(0, 3)))
        fw = FRAMEWORK[row["person"]["home"]]
        row["provider"] = fw[int(r.integers(len(fw)))] if row["status"] in ("Started", "Open") else ""
        if row["spot"] is not None:
            row["spot_provider"] = SPOT[int(r.integers(len(SPOT)))]
    return rows


def spot_invoices(refs):
    """Weekly invoice lines for spot-purchased care in 2025-26, each carrying the service's start date as the
    provider gives it."""
    out = []
    for row in refs:
        if row["spot"] is None:
            continue
        start = row["spot"]
        if not (dt.date(2025, 4, 1) <= start <= dt.date(2026, 3, 31)):
            continue
        r = W.rng_for("spot", row["ref_no"])
        weeks = int(r.integers(2, 9))
        wk_end = start + dt.timedelta((6 - start.weekday()) % 7)
        rate = [24.10, 24.85, 25.40, 26.20][SPOT.index(row["spot_provider"])]
        brk = 1 + int(r.integers(1, max(2, weeks - 1))) if weeks >= 4 and r.random() < 0.12 else None
        restart = None
        for w in range(weeks + (1 if brk else 0)):
            we = wk_end + dt.timedelta(7 * w)
            if brk is not None and w == brk:
                # care suspended for a week and restarted under the same purchase
                restart = we + dt.timedelta(1 + int(r.integers(0, 4)))
                continue
            days = 7 if w else (we - start).days + 1
            if days < 7:
                hours = max(1.0, round(float(r.integers(5, 16)) * days / 7.0 * 2) / 2)
            else:
                hours = float(r.integers(8, 22)) + 0.5 * int(r.integers(0, 2))
            if restart is not None:
                if we < restart:
                    continue
                if (we - restart).days < 7:
                    hours = max(1.0, round(float(r.integers(5, 16)) * ((we - restart).days + 1) / 7.0 * 2) / 2)
            if we > dt.date(2026, 3, 31):
                break                                   # the finance extract is the 2025-26 financial year
            out.append(dict(provider=row["spot_provider"], ref_no=row["ref_no"], person=row["person"],
                            start=restart or start, week_end=we, hours=hours, rate=rate))
    out.sort(key=lambda x: (x["week_end"], x["provider"], x["ref_no"]))
    inv = {}
    for x in out:
        k = (x["provider"], x["week_end"])
        if k not in inv:
            inv[k] = "SI%06d" % (40000 + 7 * len(inv) + int(W.rng_for("inv", *map(str, k)).integers(0, 7)))
        x["invoice"] = inv[k]
    return out


def weekly_return(spells):
    """The national weekly return, by trust and week ending Sunday: patients discharged on each pathway and the
    nights they spent in hospital after their discharge ready date, counted in the week of discharge."""
    out = {}
    for sp in spells:
        dd = sp["dis_t"].date()
        we = dd + dt.timedelta((6 - dd.weekday()) % 7)
        o = out.setdefault((sp["trust"], we), [0] * 8)
        o[2 * sp["pathway"]] += 1
        o[2 * sp["pathway"] + 1] += (dd - sp["ready"]).days
    return out


def census(wstays):
    """Patients aged 65 and over in a bed at midnight, by site and the date the night begins."""
    site_of = {w[0]: s for s, ws in WARDS.items() for w in ws}
    occ = {}
    for w in wstays:
        d = w["start"].date()
        while True:
            mid = dt.datetime(d.year, d.month, d.day) + dt.timedelta(1)
            if mid > w["end"]:
                break
            if mid > w["start"]:
                k = (site_of[w["ward"]], d)
                occ[k] = occ.get(k, 0) + 1
            d += dt.timedelta(1)
    return occ


def occupancy(wstays):
    """The daily general and acute bed census by site (a distractor): beds open and beds occupied at midnight,
    every age, with escalation beds opened in winter."""
    occ = census(wstays)
    beds = {s: sum(w[3] for w in ws) for s, ws in WARDS.items()}
    out = []
    d = core.REC0
    while d <= core.REC1:
        for site in core.SITES:
            r = W.rng_for("occ", site, d.isoformat())
            top = ESCALATION[site]
            esc = (int(r.integers(top // 4, top + 1)) if d.month in (12, 1, 2)
                   else (int(r.integers(0, top // 3 + 1)) if d.month in (11, 3) else 0))
            under65 = int(beds[site] * (0.33 + 0.05 * r.random()))
            open_ = beds[site] + esc
            out.append((d, site, open_, esc, min(open_, occ.get((site, d), 0) + under65)))
        d += dt.timedelta(1)
    return out


def reablement():
    """People discharged from hospital into the council's reablement service and still at home 91 days later, by
    district and quarter of discharge (a distractor)."""
    out = []
    qs = [(2024, 4), (2025, 1), (2025, 2), (2025, 3), (2025, 4), (2026, 1)]
    for y, q in qs:
        for dist in core.DISTRICTS:
            r = W.rng_for("reab", dist, y, q)
            n = int({"Marchford": 210, "Ashby": 120, "Teme Valley": 105}[dist] * (1.1 if q in (4, 1) else 1.0)
                    + r.integers(-18, 19))
            home = int(round(n * (0.80 + 0.06 * r.random())))
            out.append(dict(year=y, quarter=q, district=dist, discharged=n, at_home_91=home))
    return out
