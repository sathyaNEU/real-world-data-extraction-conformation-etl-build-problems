"""Builds the whole world in memory, in a fixed order, from the seed."""
import datetime as dt
import random

from common import D, SEED, cif
import world
import history
import nonwatch
import returns
from plan import SECTIONS

AGENCY_NIF = cif("Q", 4600731)
AGENCY_NAME = "Ens Públic de Patrimoni Residencial"
WATCH = [s["code"] for s in SECTIONS]


def make_world():
    holders, used = world.build_holders()
    sections, buildings, dwellings, used_parcels = world.build_stock()
    stock = (sections, buildings, dwellings)
    people = history.People(used, SEED * 29 + 1)
    book = history.Book()
    rng = random.Random(SEED * 31 + 7)
    state26, reserved = history.allocate_june26(stock, people)
    settled = history.settled_purchases(book, state26, stock, people, rng)
    own0 = history.backward_history(book, state26, stock, people, rng, settled)
    used_tk = history.forward_2026(book, state26, stock, people, reserved, settled, rng)
    own0_nw, nw_sections = nonwatch.build(holders, stock, people, book, used_parcels)
    own0.update(own0_nw)
    add_private_texture(book, own0, stock, people, random.Random(SEED * 37 + 3))
    add_nonresidential(stock, random.Random(SEED * 41 + 5))
    timeline = returns.Timeline(own0, book.events)

    def nif(o):
        if o in holders:
            return holders[o]["nif"]
        if o == "AG":
            return AGENCY_NIF
        return o[2:]

    lodgements, expo = returns.build(holders, stock, timeline, book, nif)
    return {"holders": holders, "stock": stock, "book": book, "own0": own0, "timeline": timeline,
            "lodgements": lodgements, "expo": expo, "nif": nif, "settled": settled, "state26": state26,
            "nw_sections": nw_sections, "reserved": reserved}


def add_private_texture(book, own0, stock, people, rng, n=72):
    sections, buildings, dwellings = stock
    watch = set(WATCH)
    evs = {}
    for e in book.events:
        for r in e["refs"]:
            evs.setdefault(r, []).append(e)
    committed = {c["ref"] for c in book.commitments}
    refs = sorted(r for r, d in dwellings.items() if d["section"] in watch and r not in committed)
    rng.shuffle(refs)
    made = 0
    for r in refs:
        if made == n:
            break
        t = history.rand_day(rng, D(2024, 7, 15), D(2026, 9, 11))
        hist = sorted(evs.get(r, []), key=lambda e: e["date"])
        if any(abs((e["date"] - t).days) < 90 for e in hist):
            continue
        o = own0[r]
        for e in hist:
            if e["date"] <= t:
                o = e["after"][r]
        if not o.startswith("p:"):
            continue
        # the owner after t must stay the seller of any later event: only allow when no later event
        if any(e["date"] > t for e in hist):
            continue
        new = people.new()
        title = "herència" if rng.random() < 0.3 else "compravenda"
        book.event(t, {r: o}, {r: new}, history.price(rng, dwellings[r]["section"]) if title == "compravenda" else 0,
                   title=title)
        made += 1


def add_nonresidential(stock, rng):
    """Shops and garages in the watch buildings: cadastre units that are not dwellings."""
    sections, buildings, dwellings = stock
    from common import full_ref
    for code in WATCH:
        for p in sections[code]["parcels"]:
            if rng.random() < 0.45:
                k = rng.choice([1, 1, 2, 3])
                base = len(buildings[p]["units"])
                buildings[p].setdefault("nonres", [])
                for j in range(1, k + 1):
                    ref = full_ref(p, base + j)
                    buildings[p]["nonres"].append({"ref": ref, "unit": base + j,
                                                   "us": rng.choice(["Comercial", "Comercial", "Aparcament"]),
                                                   "floor": "BJ" if j == 1 else "-1", "door": f"{j:02d}",
                                                   "area": rng.randrange(18, 160)})
