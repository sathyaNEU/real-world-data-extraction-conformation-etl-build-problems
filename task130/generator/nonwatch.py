"""Large holders' dwellings outside the watch list: the bulk of every return, simulated forwards from
1 July 2024. Nothing here can reach a watch-list section; it carries volume, the holders' regional
totals (every registered holder stays at ten or more), agreements for the back-test and a few of the
agency's commitments to large holders elsewhere in the region.
"""
import datetime as dt
import random

from common import D, SEED, CLOCK, full_ref
from history import blackout, rand_day, price, FREEZE, CARRIED
from world import MUNIS

T0 = D(2024, 6, 30)


def size_of(h, rng):
    if h[0] in "GN" and h[1:2].isdigit():
        return rng.randrange(170, 520)
    if h in ("X1", "X2", "X3", "X4", "X5", "Y1", "Y2", "Z1", "Z2", "OPH"):
        return rng.randrange(45, 150)
    if h.startswith("CAR"):
        return rng.randrange(18, 75)
    if h.startswith("nw"):
        return rng.randrange(14, 120)
    return rng.randrange(7, 40)


def build(holders, stock, people, book, used_parcels):
    rng = random.Random(SEED * 17 + 9)
    sections, buildings, dwellings = stock
    munis = sorted(MUNIS)
    nw_sections = []
    for m in munis:
        for dist in range(1, 8 if m in ("46250", "03014", "12040") else 5):
            for sec in rng.sample(range(1, 40), 6 if m in ("46250", "03014") else 4):
                code = f"{m}{dist:02d}{sec:03d}"
                if code in sections:
                    continue
                nw_sections.append(code)
    nw_sections.sort()
    own0 = {}
    spare = []   # (parcel, unit) never on any return until bought
    ids = [h for h in sorted(holders) if not h.startswith("old")]

    def new_building(size):
        code = rng.choice(nw_sections)
        sheet = MUNIS[code[:5]][2]
        while True:
            parcel = f"{rng.randrange(1000000, 9999999):07d}{sheet}{rng.randrange(10, 99)}{'ABCDEFGHJKLNPRSTUV'[rng.randrange(18)]}"
            if parcel not in used_parcels:
                used_parcels.add(parcel)
                break
        year = rng.choice([1955, 1964, 1969, 1973, 1977, 1982, 1989, 1996, 2003, 2006, 2008, 2017, 2021])
        buildings[parcel] = {"parcel": parcel, "section": code, "units": [], "street": None,
                             "num": rng.randrange(1, 180), "year": year, "size": size}
        sections.setdefault(code, {"code": code, "muni": code[:5], "dist": code[5:7], "N": None,
                                   "role": None, "parcels": []})["parcels"].append(parcel)
        return parcel

    def make(parcel, u):
        ref = full_ref(parcel, u)
        floors = max(1, (buildings[parcel]["size"] + 3) // 4)
        per = -(-buildings[parcel]["size"] // floors)
        f, dpos = divmod(u - 1, per)
        dwellings[ref] = {"ref": ref, "parcel": parcel, "unit": u, "section": buildings[parcel]["section"],
                          "floor": f"{f + 1:02d}", "door": f"{dpos + 1:02d}", "area": rng.randrange(45, 125),
                          "year": buildings[parcel]["year"]}
        buildings[parcel]["units"].append(ref)
        return ref

    for h in ids:
        n = size_of(h, rng)
        while n > 0:
            size = rng.choice([8, 10, 12, 14, 16, 20, 24, 30, 36])
            parcel = new_building(size)
            whole = rng.random() < 0.55
            k = size if whole else max(2, size // rng.choice([2, 3, 4]))
            k = min(k, n) if n >= 4 else n
            for u in range(1, k + 1):
                own0[make(parcel, u)] = h
            for u in range(k + 1, size + 1):
                spare.append((parcel, u))
            n -= k
    rng.shuffle(spare)
    # forward events, 8 July 2024 to 26 June 2026, then July to September 2026
    cur = dict(own0)
    by_holder = {}
    for r, h in cur.items():
        by_holder.setdefault(h, set()).add(r)
    plans = []
    for h in ids:
        k = max(1, len(by_holder.get(h, ())) // 55)
        for _ in range(k + rng.randrange(0, 3)):
            plans.append((rand_day(rng, D(2024, 7, 8), D(2026, 6, 26)), h, rng.choice(["sale", "sale", "buy", "buy", "swap"])))
    plans.sort()
    pending = set()
    acq = {}
    late_plans = []
    for h in ids:
        if rng.random() < 0.35:
            late_plans.append((rand_day(rng, D(2026, 7, 6), D(2026, 9, 18)), h, rng.choice(["sale", "buy", "swap"])))
    late_plans.sort()

    def run(plans):
      for t, h, kind in plans:
          frozen = h in CARRIED or h in ("Y1", "Y2")
          if frozen and t > FREEZE - dt.timedelta(days=170):
              continue
          mine = sorted(r for r in by_holder.get(h, ()) if r not in pending)
          if kind == "buy":
              m = rng.choice([1, 2, 3, 4, 6])
              refs = []
              for _ in range(m):
                  if not spare:
                      break
                  parcel, u = spare.pop()
                  refs.append(make(parcel, u))
              p = people.new()
              for r in refs:
                  own0[r] = p
              ev = book.event(t, {r: p for r in refs}, {r: h for r in refs}, price(rng, None))
              for r in refs:
                  cur[r] = h
                  acq[r] = t
                  by_holder.setdefault(h, set()).add(r)
              continue
          if len(mine) < 16:
              continue
          m = rng.choice([1, 2, 3, 4]) if kind == "sale" else rng.choice([2, 4, 6, 8])
          refs = sorted(rng.sample(mine, m))
          if kind == "sale":
              buyers = [people.new() for _ in refs]
              buyer = "private"
          else:
              others = [x for x in ids if x != h and not (x in CARRIED or x in ("Y1", "Y2"))]
              b = rng.choice(others)
              buyers, buyer = [b] * m, b
          lo = max(D(2024, 4, 1), t - dt.timedelta(days=160))
          hi = t - dt.timedelta(days=10)
          made = lo + dt.timedelta(days=rng.randrange(max(1, (hi - lo).days)))
          made = max([made] + [acq.get(r, made) + dt.timedelta(days=1) for r in refs])
          made = min(made, t)
          if frozen:
              made = min(made, t - dt.timedelta(days=12))
          pr = price(rng, None)
          agr = book.agreement(seller=h, buyer=buyer, buyers=buyers, refs=sorted(refs), made=made, agreed=t,
                               price=pr, takeover=None, section=None)
          book.event(t, {r: h for r in refs}, dict(zip(refs, buyers)), pr, agr)
          for r, b in zip(refs, buyers):
              by_holder[h].discard(r)
              cur[r] = b
              if not b.startswith("p:"):
                  by_holder.setdefault(b, set()).add(r)
                  acq[r] = t

    run(plans)

    # agreements in force on 30 June 2026 completing after 30 September, a few taken over by the agency
    later = [h for h in ids if not (h in CARRIED or h in ("Y1", "Y2")) and len(by_holder.get(h, ())) >= 40]
    rng.shuffle(later)
    tk_specs = [("c2", D(2026, 7, 16), D(2026, 12, 3)), ("c5", D(2026, 8, 13), D(2027, 2, 18)),
                ("c4", D(2026, 9, 17), D(2026, 11, 26)), ("c1", D(2026, 7, 29), D(2026, 10, 29)),
                ("c6", D(2026, 8, 20), D(2027, 4, 14)), ("c7", D(2026, 9, 24), D(2027, 3, 4))]
    for i, h in enumerate(later[:22]):
        mine = sorted(by_holder[h])
        refs = rng.sample(mine, rng.choice([1, 2, 3, 5]))
        for r in refs:
            by_holder[h].discard(r)
        tk = tk_specs[i] if i < len(tk_specs) else None
        if tk:
            case, commit, agreed = tk
        else:
            agreed = rand_day(rng, D(2026, 10, 5), D(2027, 5, 28))
        if tk:
            lh_buyer = case in ("c1", "c3", "c5")
        else:
            lh_buyer = rng.random() < 0.4
        buyer = rng.choice([x for x in later if x != h]) if lh_buyer else "private"
        made = rand_day(rng, D(2026, 3, 9), D(2026, 6, 24))
        pr = price(rng, None)
        pending.update(refs)
        for r in refs:
            b = people.new() if buyer == "private" else buyer
            a = book.agreement(seller=h, buyer=buyer, buyers=[b], refs=[r], made=made, agreed=agreed, price=pr,
                               section=None,
                               takeover=({"commit": commit, "case": case,
                                          "completion": commit + dt.timedelta(days=CLOCK)} if tk else None))
            if tk:
                book.commitments.append({"ref": r, "commit": commit, "notified": agreed, "price": pr,
                                         "seller": h, "lh": True, "agreement": a["id"]})
    run(late_plans)
    return own0, nw_sections
