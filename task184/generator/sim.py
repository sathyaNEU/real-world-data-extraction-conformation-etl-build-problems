"""task184 clean truth: every farm's crops, every house's daily deaths and culls, every catch, every delivery.

Drawn forward from fixed seeds. Nothing here knows about the files; pack.py writes them from this truth."""
import datetime as dt
import functools

import numpy as np

import world as W

DAY = dt.timedelta(days=1)


def rng(*keys):
    h = abs(hash(("t184",) + tuple(str(k) for k in keys))) % (2 ** 32)
    return np.random.default_rng([W.SEED, h])


def _stable_seed(*keys):
    import hashlib
    s = "|".join(str(k) for k in keys).encode()
    return int(hashlib.sha256(s).hexdigest()[:12], 16)


def R(*keys):
    return np.random.default_rng([W.SEED, _stable_seed(*keys)])


class House:
    def __init__(self, farm, idx, grower_name, area):
        self.farm, self.idx, self.grower_name, self.area = farm, idx, grower_name, area
        self.code = "H%d" % (idx + 1)


class Crop:
    """One farm's crop: every house placed together (two days for the five- and six-house farms) and caught together."""
    def __init__(self, farm, seq, place, thin_age, clear_age, share):
        self.farm, self.seq, self.place, self.thin_age, self.clear_age, self.share = farm, seq, place, thin_age, clear_age, share
        base = 23 + _stable_seed("seqbase", farm.code) % 140      # crops the farm has grown for the company
        self.ref = "C%02d-%s-%03d" % (place.year % 100, farm.code[2:], base + seq)
        self.houses = {}          # house code -> HouseCrop


class HouseCrop:
    def __init__(self, crop, house, place):
        self.crop, self.house, self.place = crop, house, place
        self.days = []            # (date, age, alive_at_start, deaths, culls, thinned_flag) per recording day
        self.chicks = 0
        self.thinned_birds = 0
        self.cleared_birds = 0
        self.thin_night = None
        self.clear_night = None
        self.deliveries = []      # (date, boxes, source)
        self.infection = None


class Farm:
    def __init__(self, code, name, grower, parish, house_names):
        self.code, self.name, self.grower, self.parish = code, name, grower, parish
        r = R("farm", code)
        self.houses = [House(self, i, n, int(round(r.uniform(1580, 2620) / 5.0)) * 5) for i, n in enumerate(house_names)]
        self.crops = []


def _ok_catch(d):
    return d not in W.NO_CATCH


@functools.lru_cache(maxsize=1)
def farms():
    out = []
    for code, name, grower, parish, hn in W.FARMS:
        out.append(Farm(code, name, grower, parish, hn))
    return out


def _window_crop(farm):
    """Placement date and plan of the crop on site in week 7 (or a cleanout across it)."""
    if farm.code in W.DESIGN:
        d = W.DESIGN[farm.code]
        return d["place"], d["thin"], d.get("inf")
    r = R("window", farm.code)
    # a few farms are in cleanout through the window: their last crop cleared 3 to 8 February
    if farm.code in ("FP168", "FP241", "FP293", "FP317", "FP334"):
        place = W.WINDOW[0] - dt.timedelta(days=int(r.integers(44, 50)))
        return place, None, None
    age0 = int(r.integers(2, 36))
    place = W.WINDOW[0] - dt.timedelta(days=age0)
    if place.month == 12 and place.day >= 25:
        place = dt.date(2026, 12, 28)
    return place, None, None


@functools.lru_cache(maxsize=1)
def build_world():
    fs = farms()
    for f in fs:
        r = R("sched", f.code)
        place_w, thin_w, inf_w = _window_crop(f)
        # crops backward from the window crop
        places = [place_w]
        p = place_w
        while True:
            gap = int(r.integers(8, 14))
            clear_age = int(r.integers(38, 43))
            prev_clear = p - dt.timedelta(days=gap)
            prev_place = prev_clear - dt.timedelta(days=clear_age)
            # catch nights avoid the holiday shutdown and the close-out boundaries
            tries = 0
            while (not _ok_catch(prev_clear) or not _ok_catch(prev_clear + DAY)) and tries < 12:
                prev_clear -= DAY
                prev_place -= DAY
                tries += 1
            # no placements on 25 to 27 December (hatchery shutdown)
            while dt.date(2026, 12, 25) <= prev_place <= dt.date(2026, 12, 27):
                prev_place -= DAY
            if prev_place < W.FIRST_PLACEMENT - dt.timedelta(days=60):
                break
            places.append(prev_place)
            p = prev_place
        places = sorted(places)
        f.crops = []
        for i, pl in enumerate(places):
            cr = R("crop", f.code, pl.isoformat())
            is_window = (pl == place_w)
            nxt = places[i + 1] if i + 1 < len(places) else None
            if nxt is not None:
                # clearance night leaves a cleanout of 8 to 13 days before the next placement
                want = max(37, min(43, (nxt - pl).days - int(cr.integers(8, 14))))
                order = [want] + [x for k in range(1, 7) for x in (want - k, want + k)]
                ok = [x for x in order if 37 <= x <= 43 and (nxt - pl).days - x >= 7
                      and _ok_catch(pl + dt.timedelta(days=x)) and _ok_catch(pl + dt.timedelta(days=x + 1))]
                clear_age = ok[0] if ok else want
            else:
                clear_age = int(cr.integers(39, 43))
            if is_window and f.code in W.DESIGN:
                thin_age = thin_w
                if W.DESIGN[f.code]["role"] in ("U1", "U2", "T1", "T2", "T3"):
                    clear_age = max(clear_age, (W.WINDOW[-1] - pl).days + 1, 41)
            elif cr.random() < 0.55:
                thin_age = int(cr.integers(31, 35))
                while not (_ok_catch(pl + dt.timedelta(days=thin_age)) and _ok_catch(pl + dt.timedelta(days=thin_age + 1))) and thin_age > 29:
                    thin_age -= 1
            else:
                thin_age = None
            if is_window and f.code not in W.DESIGN:
                # crops on site in the window keep the window inside their life
                clear_age = max(clear_age, (W.WINDOW[-1] - pl).days + 1) if (W.WINDOW[-1] - pl).days < 44 else clear_age
            share = float(cr.uniform(0.25, 0.33))
            crop = Crop(f, i + 1, pl, thin_age, clear_age, share)
            f.crops.append(crop)
        _simulate_farm(f, inf_w)
    return fs


def _simulate_farm(f, inf_w):
    for crop in f.crops:
        late = len(f.houses) >= 5
        for h in f.houses:
            place = crop.place + (DAY if (late and h.idx >= 3) else dt.timedelta(0))
            hc = HouseCrop(crop, h, place)
            r = R("hc", f.code, h.code, crop.place.isoformat())
            density = float(r.normal(20.2, 0.35))
            boxes = int(round(h.area * density / 101.0))
            source = "contract" if W.CONTRACT_FROM <= place <= W.CONTRACT_TO else "company"
            hc.chicks = boxes * 101
            # deliveries: one lorry up to 300 boxes, otherwise two
            if boxes > 300:
                b1 = int(boxes * float(r.uniform(0.45, 0.6)))
                hc.deliveries = [(place, b1, source), (place, boxes - b1, source)]
            else:
                hc.deliveries = [(place, boxes, source)]
            thin_age = crop.thin_age
            clear_age = crop.clear_age
            # house-level stagger of an infection
            inf = None
            if inf_w is not None and crop.place <= W.WINDOW[0] <= crop.place + dt.timedelta(days=crop.clear_age):
                d0, e0, g = inf_w
                off = int(R("infoff", f.code, h.code).integers(0, 2))
                inf = (d0 + dt.timedelta(days=off), e0 * W.INF_TUNE.get((f.code, h.code), 1.0), g)
            hc.infection = inf
            hc.box_short = int(R("short", f.code, h.code, crop.place.isoformat()).binomial(hc.chicks, 0.0021))
            alive = hc.chicks - hc.box_short
            hc.catch_lost_thin = 0
            for a in range(1, clear_age + 1):
                d = place + dt.timedelta(days=a)
                post = thin_age is not None and a > thin_age
                hz = W.course(a) * (W.THINNED_FACTOR if post else 1.0)
                lam = alive * hz / 1000.0
                if inf is not None and d >= inf[0]:
                    lam += alive * inf[1] * (inf[2] ** (d - inf[0]).days) / 1000.0
                dr = R("day", f.code, h.code, d.isoformat())
                deaths = int(min(alive, dr.poisson(lam)))
                culls = int(min(alive - deaths, dr.poisson(alive * W.cull_rate(a) / 1000.0)))
                hc.days.append((d, a, alive, deaths, culls, post))
                alive -= deaths + culls
                if thin_age is not None and a == thin_age:
                    hc.thin_night = d
                    take = int(round(alive * crop.share))
                    hc.catch_lost_thin = int(R("clt", f.code, h.code, d.isoformat()).binomial(take, 0.0012))
                    hc.thinned_birds = take - hc.catch_lost_thin
                    alive -= take
            hc.clear_night = place + dt.timedelta(days=clear_age)
            hc.catch_lost_clear = int(R("clc", f.code, h.code, hc.clear_night.isoformat()).binomial(alive, 0.0024))
            hc.cleared_birds = alive - hc.catch_lost_clear
            crop.houses[h.code] = hc


def all_house_crops():
    for f in build_world():
        for c in f.crops:
            for hc in c.houses.values():
                yield f, c, hc


def window_crops():
    out = []
    for f in build_world():
        for c in f.crops:
            hcs = list(c.houses.values())
            if any(any(d == W.WINDOW[0] for d, *_ in hc.days) for hc in hcs):
                out.append((f, c))
    return out
