"""task184 pack: the files under target/, written from sim.py's truth, each in its producing system's own form."""
import csv
import datetime as dt
import hashlib
import io
import json

import world as W
import sim as S

DAY = dt.timedelta(days=1)

FILES = {
    "app": "grower_app_returns_2025-06_2027-02.csv",
    "paper": "paper_record_sheets_2024-11_2025-08.csv",
    "flocks": "flock_register_2024-11_2027-02.csv",
    "kh": "kirton_holme_despatches_2024-11_2027-02.csv",
    "lw": "lindewaard_leveringen_2026-12.csv",
    "catch": "wash_catching_sheets_2025-01_2027-02.csv",
    "intake": "riverside_intake_2026-12_2027-01.csv",
    "line2": "riverside_line2_loads_2027-01.json",
    "farms": "farm_register.xlsx",
    "protocol": "FP-AI-03_avian_influenza_surveillance_protocol.pdf",
    "aipz": "aipz_housing_measures_2026-11.pdf",
    "wild": "apha_wild_bird_findings_2026-10_2027-02.csv",
    "weather": "met_daily_weather_2025-01_2027-02.csv",
}


def h8(*keys):
    return int(hashlib.sha256("|".join(str(k) for k in keys).encode()).hexdigest()[:10], 16)


def _csv(path, header, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


# ---------------------------------------------------------------- identities shared by several files
def farm_meta():
    """Per farm: CPH, the plant's grower number, the hatchery's site code, the catcher's site name."""
    out = {}
    used_g, used_k = set(), set()
    for f in S.farms():
        r = S.R("meta", f.code)
        cph = "30/%03d/%04d" % (int(r.integers(101, 399)), int(r.integers(1000, 9999)))
        g = int(r.integers(1100, 4900))
        while g in used_g:
            g += 37
        used_g.add(g)
        k = int(r.integers(2000, 7999))
        while k in used_k:
            k += 13
        used_k.add(k)
        surname = f.grower.replace("&", "and").split()[-1].replace("Ltd", "").replace("LLP", "").strip()
        style = int(r.integers(0, 3))
        if style == 0:
            cname = "%s (%s)" % (f.parish, f.grower.split()[-1] if "Ltd" not in f.grower and "LLP" not in f.grower else f.grower.split()[0])
        elif style == 1:
            cname = f.name.replace(" Farm", "").replace(" Poultry Unit", " PU").replace(" Broiler Site", " BS")
        else:
            cname = "%s - %s" % (f.grower.split()[0] if f.grower[1] != "." else f.grower.split()[-1], f.parish)
        out[f.code] = dict(cph=cph, grower_no=g, kh_site="KH-%04d" % k, catcher=cname)
    return out


def flock_ref(c):
    return c.ref


# ---------------------------------------------------------------- returns
def _water(hc, a, alive):
    r = S.R("w", hc.house.farm.code, hc.house.code, (hc.place + dt.timedelta(days=a)).isoformat())
    per = (0.024 + 0.0071 * a) * float(r.normal(1.0, 0.035))
    return alive * per


def _app_from(f):
    r = S.R("appfrom", f.code)
    span = (W.APP_TO - W.APP_FROM).days
    return W.APP_FROM + dt.timedelta(days=int(r.integers(0, span + 1)))


def _submitted(f, h, d):
    """The app stamps a return when it is submitted, in UTC. Most go in mid-morning; a share are entered late,
    some after midnight."""
    r = S.R("sub", f.code, h.code, d.isoformat())
    u = r.random()
    if u < 0.82:
        t = dt.datetime.combine(d, dt.time(7, 0)) + dt.timedelta(minutes=int(r.integers(0, 260)))
    elif u < 0.95:
        t = dt.datetime.combine(d, dt.time(16, 0)) + dt.timedelta(minutes=int(r.integers(0, 420)))
    else:
        t = dt.datetime.combine(d + DAY, dt.time(0, 5)) + dt.timedelta(minutes=int(r.integers(0, 150)))
    # British Summer Time: the app stamps UTC
    bst = dt.date(t.year, 3, 31 - (dt.date(t.year, 3, 31).weekday() + 1) % 7) <= t.date() < dt.date(t.year, 10, 31 - (dt.date(t.year, 10, 31).weekday() + 1) % 7)
    if bst:
        t -= dt.timedelta(hours=1)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def returns_rows():
    app, paper = [], []
    overlap = {"FP155", "FP223", "FP298"}
    for f in S.build_world():
        start = _app_from(f)
        for c in f.crops:
            if c.place < W.FIRST_PLACEMENT:
                continue
            for hc in c.houses.values():
                for (d, a, alive, deaths, culls, post) in hc.days:
                    water = _water(hc, a, alive - deaths / 2.0)
                    on_app = d >= start
                    dup = (f.code in overlap and start <= d < start + dt.timedelta(days=7))
                    if on_app and d <= W.WINDOW[-1]:
                        rid = "R%09d" % (h8("ret", f.code, hc.house.code, d.isoformat()) % 10 ** 9)
                        build = "3.4.%d" % (2 if d < dt.date(2026, 3, 9) else (7 if d < dt.date(2026, 10, 12) else 9))
                        app.append([rid, f.code, hc.house.code, d.isoformat(), deaths, culls, int(round(water)),
                                    _submitted(f, hc.house, d), build])
                    if (not on_app or dup) and d <= W.WINDOW[-1]:
                        # keyed on the Monday after the sheet's week by the area manager
                        keyed = d + dt.timedelta(days=(7 - d.weekday()) % 7 or 7)
                        paper.append([f.name, hc.house.grower_name, d.strftime("%d/%m/%Y"), deaths, culls,
                                      "%.2f" % (water / 1000.0), keyed.strftime("%d/%m/%Y"), "EP"])
    # the January app outage: returns for the three days entered once more when the app came back
    extra = []
    for row in app:
        d = dt.date.fromisoformat(row[3])
        if d in W.APP_OUTAGE and (h8("outdup", row[1], row[2], row[3]) % 3 == 0):
            dup = list(row)
            dup[0] = "R%09d" % (h8("ret2", row[1], row[2], row[3]) % 10 ** 9)
            dup[7] = "2027-01-21T%02d:%02d:%02dZ" % (9 + h8("h", row[0]) % 3, h8("m", row[0]) % 60, h8("s", row[0]) % 60)
            extra.append(dup)
    for row in app:
        d = dt.date.fromisoformat(row[3])
        if d in W.APP_OUTAGE:
            row[7] = "2027-01-21T%02d:%02d:%02dZ" % (8 + h8("h0", row[0]) % 2, h8("m0", row[0]) % 60, h8("s0", row[0]) % 60)
    app += extra
    app.sort(key=lambda r: (r[3], r[1], r[2], r[7]))
    paper.sort(key=lambda r: (dt.datetime.strptime(r[2], "%d/%m/%Y"), r[0], r[1]))
    return app, paper


APP_HEADER = ["return_id", "farm_code", "house", "record_date", "found_dead", "culled", "water_litres",
              "submitted_at_utc", "app_build"]
PAPER_HEADER = ["Farm", "Shed", "Date", "Mort", "Culls", "Water m3", "Keyed on", "Keyed by"]


# ---------------------------------------------------------------- flock register and hatcheries
def flock_rows():
    rows = []
    for f in S.build_world():
        for c in f.crops:
            if c.place < W.FIRST_PLACEMENT:
                continue
            for hc in c.houses.values():
                if hc.place > W.WINDOW[-1]:
                    continue
                ordered = int(round(hc.chicks / 1000.0 + float(S.R("ord", c.ref, hc.house.code).normal(0, 0.4)))) * 1000
                rows.append([c.ref, f.code, hc.house.code, hc.place.isoformat(), ordered, "Ross 308"])
    rows.sort(key=lambda r: (r[3], r[1], r[2]))
    return rows


FLOCK_HEADER = ["crop_ref", "farm_code", "house", "placed_on", "chicks_ordered", "breed"]


def hatchery_rows():
    meta = farm_meta()
    kh, lw = [], []
    for f in S.build_world():
        for c in f.crops:
            if c.place < W.FIRST_PLACEMENT:
                continue
            for hc in c.houses.values():
                if hc.place > W.WINDOW[-1]:
                    continue
                for j, (d, boxes, src) in enumerate(hc.deliveries):
                    if src == "company":
                        hatch = d - DAY
                        kh.append([None, hatch.isoformat(), d.isoformat(), meta[f.code]["kh_site"], hc.house.code,
                                   boxes, 100, boxes * 100, boxes, "KH%02d" % (1 + h8("lorry", c.ref, hc.house.code, j) % 7)])
                    else:
                        incl = (h8("lwconv", c.ref, hc.house.code, j) % 4) != 0
                        per = 101 if incl else 100
                        loc = "Venray" if incl else "Ermelo"
                        lw.append([None, d.strftime("%d-%m-%Y"), loc, f.name, hc.house.grower_name, boxes, per,
                                   boxes * per, boxes])
    kh.sort(key=lambda r: (r[2], r[3], r[4]))
    n = 418230
    for r in kh:
        n += 1 + h8("dn", r[2], r[3], r[4]) % 4
        r[0] = "KH%d" % n
    lw.sort(key=lambda r: (dt.datetime.strptime(r[1], "%d-%m-%Y"), r[3], r[4]))
    m = 2611904
    for r in lw:
        m += 3 + h8("lb", r[1], r[3], r[4]) % 9
        r[0] = "LB%d" % m
    return kh, lw


KH_HEADER = ["despatch_no", "hatch_date", "delivered_on", "customer_site", "house", "boxes", "chicks_per_box",
             "chicks", "free_chicks", "lorry"]
LW_HEADER = ["leverbon", "afleverdatum", "broederij_locatie", "bedrijf", "stal", "dozen", "kuikens_per_doos",
             "kuikens", "gratis_kuikens"]


# ---------------------------------------------------------------- catching contractor
def _modules(hc, night, birds):
    age = (night - hc.place).days
    per = int(round(10 * (24 - 0.29 * age)))            # birds a module takes falls as the birds grow
    per = max(120, per)
    mods = int(-(-birds // per))
    return mods, per


def catch_rows():
    meta = farm_meta()
    rows = []
    for f in S.build_world():
        for c in f.crops:
            if c.place < W.FIRST_PLACEMENT:
                continue
            for hc in c.houses.values():
                for kind, night, birds in (("thin", hc.thin_night, hc.thinned_birds),
                                           ("clear", hc.clear_night, hc.cleared_birds)):
                    if night is None or night > W.WINDOW[-1] or birds <= 0:
                        continue
                    mods, per = _modules(hc, night, birds)
                    r = S.R("cs", c.ref, hc.house.code, kind)
                    caught = mods * per - int(r.integers(0, per))       # the last module goes part full
                    team = ["Team %s" % x for x in ("A", "B", "C", "D", "E")][h8("team", night.isoformat(), f.code) % 5]
                    start = dt.datetime.combine(night, dt.time(19, 30)) + dt.timedelta(minutes=int(r.integers(0, 150)))
                    dur = dt.timedelta(minutes=int(mods * float(r.uniform(5.5, 7.5))))
                    rows.append([None, night.isoformat(), meta[f.code]["catcher"], hc.house.code[1:], mods, per,
                                 caught, team, start.strftime("%H:%M"), (start + dur).strftime("%H:%M")])
    rows.sort(key=lambda r: (r[1], r[2], r[3]))
    n = 30417
    for r in rows:
        n += 1 + h8("ws", r[1], r[2], r[3]) % 3
        r[0] = "WCS%d" % n
    return rows


CATCH_HEADER = ["sheet_no", "catch_night", "site", "shed", "modules", "birds_per_module", "birds_caught", "team",
                "start", "finish"]


# ---------------------------------------------------------------- the plant (close-out records)
def loads():
    """Every load the plant took in December 2026 and January 2027, with its truth (tipped, dead on arrival)."""
    meta = farm_meta()
    out = []
    for f in S.build_world():
        for c in f.crops:
            for hc in c.houses.values():
                for kind, night, birds in (("thin", hc.thin_night, hc.thinned_birds),
                                           ("clear", hc.clear_night, hc.cleared_birds)):
                    if night is None or not (dt.date(2026, 12, 1) <= night <= dt.date(2027, 1, 31)) or birds <= 0:
                        continue
                    mods, per = _modules(hc, night, birds)
                    r = S.R("ld", c.ref, hc.house.code, kind)
                    left = birds
                    nload = int(-(-mods // 13))
                    for k in range(nload):
                        share = left if k == nload - 1 else int(round(birds / nload + float(r.normal(0, 60))))
                        share = min(share, left)
                        left -= share
                        p = float(r.uniform(0.0022, 0.0046))
                        doa = int(r.binomial(share, p))
                        out.append(dict(farm=f.code, crop=c.ref, house=hc.house.code, kind=kind, night=night,
                                        tipped=share, doa=doa, hung=share - doa, k=k, mods=-(-share // per),
                                        grower_no=meta[f.code]["grower_no"], cph=meta[f.code]["cph"]))
    # weigh-in times: the night's loads arrive through the night, in catch order
    out.sort(key=lambda x: (x["night"], x["farm"], x["house"], x["kind"], x["k"]))
    for x in out:
        r = S.R("wt", x["crop"], x["house"], x["kind"], x["k"])
        base = dt.datetime.combine(x["night"], dt.time(21, 10))
        x["weighed"] = base + dt.timedelta(minutes=int(55 * x["k"] + r.integers(0, 50) + 15 * (h8("fo", x["farm"]) % 4)))
        x["trailer"] = "T%03d" % (101 + h8("tr", x["crop"], x["house"], x["kind"], x["k"]) % 14)
        x["tare"] = int(r.integers(15200, 16400))
    return out


_PLACED = {}


def _placed():
    if not _PLACED:
        for f in S.build_world():
            for c in f.crops:
                for hc in c.houses.values():
                    _PLACED[(c.ref, hc.house.code)] = hc.place
    return _PLACED


def bird_weight(age):
    return 0.042 + 0.0011 * age ** 2 + 0.014 * age


def intake_rows(lds=None):
    lds = lds if lds is not None else loads()
    rows = []
    t = 506311
    for x in sorted(lds, key=lambda z: z["weighed"]):
        t += 1 + h8("tk", x["crop"], x["house"], x["kind"], x["k"]) % 3
        x["ticket"] = t
        # the intake software upgrade of 18 January: birds is then every bird tipped from the modules
        birds = x["tipped"] if x["night"] >= W.INTAKE_SWITCH else x["hung"]
        age = (x["night"] - _placed()[(x["crop"], x["house"])]).days
        kg = int(round(x["tipped"] * bird_weight(age) * float(S.R("kg", x["ticket"]).normal(1.0, 0.012))))
        gross = x["tare"] + kg + 38 * x["mods"] * 10
        weighed_utc = x["weighed"]
        rows.append([t, weighed_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), x["grower_no"], x["crop"], x["cph"],
                     x["trailer"], x["mods"], birds, x["doa"], gross, x["tare"] + 38 * x["mods"] * 10])
    return rows


INTAKE_HEADER = ["ticket", "weighed_in_utc", "grower_no", "flock_ref", "cph", "trailer", "modules", "birds", "doa",
                 "gross_kg", "tare_kg"]


def line2_rows(lds):
    out = []
    for x in sorted(lds, key=lambda z: z["weighed"]):
        if x["night"] < W.INTAKE_SWITCH:
            continue
        if h8("line", x["ticket"]) % 100 >= 46:
            continue
        r = S.R("l2", x["ticket"])
        start = x["weighed"] + dt.timedelta(minutes=int(r.integers(35, 160)))
        dur = dt.timedelta(seconds=int(x["hung"] / 172.0 * 60))
        out.append(dict(ticket=x["ticket"], line=2, hang_start=start.strftime("%Y-%m-%dT%H:%M"),
                        hang_end=(start + dur).strftime("%Y-%m-%dT%H:%M"), birds_hung=x["hung"],
                        rejected_carcasses=int(r.binomial(x["hung"], 0.009))))
    return out


# ---------------------------------------------------------------- distractors
def wild_rows():
    rows = []
    sp = ["Mute swan", "Greylag goose", "Pink-footed goose", "Black-headed gull", "Herring gull", "Mallard",
          "Wigeon", "Barnacle goose", "Common buzzard", "Great black-backed gull"]
    fs = S.farms()
    d = dt.date(2026, 10, 9)
    i = 0
    while d <= dt.date(2027, 2, 12):
        r = S.R("wb", d.isoformat())
        if r.random() < 0.38:
            f = fs[int(r.integers(0, len(fs)))]
            n = int(r.integers(1, 4))
            rows.append([d.isoformat(), sp[int(r.integers(0, len(sp)))], n, "%s, Lincolnshire" % f.parish,
                         "TF%04d%04d" % (int(r.integers(2000, 5800)), int(r.integers(1500, 4800))), "HPAI H5N1",
                         "APHA Weybridge"])
            i += 1
        d += DAY
    return rows


WILD_HEADER = ["date_found", "species", "number", "location", "grid_reference", "result", "laboratory"]


def weather_rows():
    import math
    rows = []
    d = dt.date(2025, 1, 1)
    while d <= dt.date(2027, 2, 14):
        for st in ("Boston", "Holbeach"):
            r = S.R("met", st, d.isoformat())
            doy = d.timetuple().tm_yday
            mean = 10.6 - 6.4 * math.cos(2 * math.pi * (doy - 18) / 365.25)
            tmax = mean + 4.2 + float(r.normal(0, 2.3))
            tmin = mean - 4.1 + float(r.normal(0, 2.4))
            rain = max(0.0, float(r.gamma(0.55, 3.4)) - 0.4)
            rows.append([d.isoformat(), st, "%.1f" % tmax, "%.1f" % min(tmin, tmax - 0.8), "%.1f" % rain])
        d += DAY
    return rows


WEATHER_HEADER = ["date", "station", "max_temp_c", "min_temp_c", "rain_mm"]


def farm_register_rows():
    meta = farm_meta()
    rows = []
    for f in S.farms():
        m = meta[f.code]
        for h in f.houses:
            rows.append([f.code, f.name, f.grower, f.parish, m["cph"], m["grower_no"], m["kh_site"], m["catcher"],
                         h.code, h.grower_name, h.area])
    return rows


FARM_HEADER = ["Farm code", "Farm", "Grower", "Parish", "CPH", "Plant grower no", "Hatchery site", "Catcher site",
               "House", "Grower's name for house", "Floor area m2"]
