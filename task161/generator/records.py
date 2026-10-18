"""task161 records: the operating layer built from the simulated truth.

Equipment for every receipt (ocean boxes, transload trailers, domestic transfers), the site split of
each account's stock, the pallet-level snapshot at the close of 6 December, the yard check, the
transload partner's manifests, the December booking notices and the ports' monthly statistics.
Nothing here decides the main call; the call reads only account totals by day.
"""
import datetime as dt
from zoneinfo import ZoneInfo
import numpy as np
import world as W
import sim

ONE = dt.timedelta(days=1)

# ----------------------------------------------------------------------------------- identifiers

def iso6346_check(code10):
    """Check digit of an ISO 6346 container number (owner code, category U, six-digit serial)."""
    vals = {}
    v = 10
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if v % 11 == 0:
            v += 1
        vals[ch] = v
        v += 1
    total = 0
    for i, ch in enumerate(code10):
        n = vals[ch] if ch.isalpha() else int(ch)
        total += n * (2 ** i)
    return (total % 11) % 10


OWNERS = ["MSCU", "MEDU", "MAEU", "MSKU", "CMAU", "CGMU", "COSU", "CSNU", "OOLU", "OOCU", "EGLV", "EMCU",
          "HLXU", "HLBU", "ONEU", "YMLU", "ZIMU", "HDMU", "TGHU", "TCLU", "CAIU", "SEGU", "FCIU", "BMOU",
          "TEMU", "GESU", "TRHU", "BEAU"]
OWNER_W = np.array([10, 8, 9, 7, 8, 6, 9, 7, 8, 6, 8, 5, 7, 5, 8, 5, 4, 4, 6, 5, 5, 4, 4, 3, 4, 3, 3, 2], float)
OWNER_W = OWNER_W / OWNER_W.sum()


def container_number(rng):
    owner = OWNERS[rng.choice(len(OWNERS), p=OWNER_W)]
    serial = "%06d" % rng.integers(0, 1000000)
    base = owner + serial
    return base + str(iso6346_check(base))


ISO_TYPE = {"20": "22G1", "40": "42G1", "40HC": "45G1", "45": "L5G1"}
TEU = {"22G1": 1.0, "42G1": 2.0, "45G1": 2.0, "L5G1": 2.25}
LEGACY_SIZE = {"20": "20", "40": "40", "40HC": "4H", "45": "45"}


def trailer_number(rng, prefix):
    return "%s%06d" % (prefix, rng.integers(100000, 999999))


# ----------------------------------------------------------------------------------- receipts

SOC = {"A01": ("QFGU", 150, 0.36), "A08": ("CPGU", 70, 0.32)}   # shipper-owned boxes: owner code, pool, share


def build_receipts(truth):
    """Every receipt as equipment: ocean boxes received direct, 53ft transload trailers carrying the
    contents of one or two ocean boxes received the same day, and 53ft domestic transfers from an
    account's own DCs. Two accounts ship part of their freight in their own boxes, which come back
    to us every few months; about one box in twenty is devanned across two shifts and confirmed as
    two receipts. The truth's daily receipts and on-hand are moved to match where a second shift
    falls on the next day."""
    out = []
    manifests = []
    rng = np.random.default_rng([W.SEED, 7001])
    seen = set()
    tl_start = dt.date(2024, 3, 4)          # the transload programme's first deliveries
    soc_pool = {}
    for c, (owner, n, _) in SOC.items():
        pool = []
        while len(pool) < n:
            base = owner + "%06d" % rng.integers(100000, 999999)
            cn = base + str(iso6346_check(base))
            if cn not in pool:
                pool.append(cn)
        soc_pool[c] = {"boxes": pool, "free": {cn: dt.date(2019, 1, 1) for cn in pool}}

    def fresh(fn):
        x = fn()
        while x in seen:
            x = fn()
        seen.add(x)
        return x

    def ocean_box(code, d):
        if code in SOC and rng.random() < SOC[code][2]:
            pool = soc_pool[code]
            ready = [cn for cn in pool["boxes"] if pool["free"][cn] <= d]
            if ready:
                cn = ready[int(rng.integers(0, len(ready)))]
                pool["free"][cn] = d + dt.timedelta(days=int(rng.integers(75, 140)))
                return cn
        return fresh(lambda: container_number(rng))

    for code, rec in truth.items():
        tshare = W.TRANSLOAD_SHARE.get(code, 0.0)
        dshare = W.DOMESTIC_SHARE.get(code, 0.0)
        byday = {}
        for (i, size, p) in rec["boxes"]:
            d = sim.ALL_DAYS[i]
            if d <= W.LAST_CLOSE:
                byday.setdefault(d, []).append((size, p))
        for d in sorted(byday):
            pending = []
            for (size, p) in byday[d]:
                u = rng.random()
                if d >= tl_start and u < tshare and size in ("40HC", "40", "20"):
                    pending.append((size, p))
                    if len(pending) == 2 or (size != "20" and rng.random() < 0.70):
                        tr = fresh(lambda: trailer_number(rng, "AVTL"))
                        srcs = [(fresh(lambda: container_number(rng)), ISO_TYPE[ss], sp) for ss, sp in pending]
                        out.append({"day": d, "account": code, "kind": "transload", "equipment": tr, "type": "53DV",
                                    "pallets": sum(x[2] for x in srcs), "sources": srcs})
                        for cn, it, sp in srcs:
                            manifests.append({"trailer": tr, "container": cn, "iso": it, "pallets": sp,
                                              "account": code, "delivered": d})
                        pending = []
                    continue
                if u > 1.0 - dshare:
                    tr = fresh(lambda: trailer_number(rng, "DC%s" % code[1:]))
                    out.append({"day": d, "account": code, "kind": "domestic", "equipment": tr, "type": "53DV",
                                "pallets": p, "sources": []})
                    continue
                cn = ocean_box(code, d)
                if rng.random() < 0.052 and p >= 8:
                    p1 = int(round(p * rng.uniform(0.35, 0.65)))
                    p2 = p - p1
                    nd = d + ONE
                    while not sim.open_day(nd):
                        nd += ONE
                    second = nd if (rng.random() < 0.7 and nd <= W.LAST_CLOSE) else d
                    out.append({"day": d, "account": code, "kind": "ocean", "equipment": cn, "type": ISO_TYPE[size],
                                "size": size, "pallets": p1, "sources": [], "part": 1})
                    out.append({"day": second, "account": code, "kind": "ocean", "equipment": cn,
                                "type": ISO_TYPE[size], "size": size, "pallets": p2, "sources": [], "part": 2})
                    if second != d:
                        i, j = sim.DIDX[d], sim.DIDX[second]
                        rec["R"][i] -= p2
                        rec["R"][j] += p2
                        rec["OH"][i:j] -= p2
                    continue
                out.append({"day": d, "account": code, "kind": "ocean", "equipment": cn, "type": ISO_TYPE[size],
                            "size": size, "pallets": p, "sources": []})
            if pending:
                tr = fresh(lambda: trailer_number(rng, "AVTL"))
                srcs = [(fresh(lambda: container_number(rng)), ISO_TYPE[ss], sp) for ss, sp in pending]
                out.append({"day": d, "account": code, "kind": "transload", "equipment": tr, "type": "53DV",
                            "pallets": sum(x[2] for x in srcs), "sources": srcs})
                for cn, it, sp in srcs:
                    manifests.append({"trailer": tr, "container": cn, "iso": it, "pallets": sp, "account": code,
                                      "delivered": d})
    out.sort(key=lambda r: (r["day"], r["account"], r["equipment"], r.get("part", 0)))
    return out, manifests


def daily_receipts_from_equipment(receipts, codes):
    """Pallets received per account per day, as the equipment records carry them."""
    acc = {c: {} for c in codes}
    for r in receipts:
        acc[r["account"]][r["day"]] = acc[r["account"]].get(r["day"], 0) + r["pallets"]
    return acc


# ----------------------------------------------------------------------------------- where stock sits

SITES = [b[0] for b in W.BUILDINGS]
CAP = {b[0]: b[4] for b in W.BUILDINGS}
RACK_FILL = 0.9935            # racks run at most this full (honeycombing)
DHS_CAP = 6000
SUBLEASE_STINTS = [(dt.date(2025, 7, 14), dt.date(2025, 10, 31)), (dt.date(2026, 10, 5), dt.date(2026, 12, 31))]
TRAILER_CAP = 25              # pallets in one storage trailer
MAX_TRAILERS = 118


def sublease_open(d):
    return any(a <= d <= b for a, b in SUBLEASE_STINTS)


def _ipf(seed, rows, cols, it=60):
    M = seed.copy()
    for _ in range(it):
        rs = M.sum(1)
        M *= np.where(rs > 0, rows / np.maximum(rs, 1e-9), 0)[:, None]
        cs = M.sum(0)
        M *= np.where(cs > 0, cols / np.maximum(cs, 1e-9), 0)[None, :]
    return M


def _round_rows(M, rows):
    """Integerise each row to its integer total by largest remainder."""
    out = np.floor(M).astype(int)
    for i in range(M.shape[0]):
        need = int(rows[i]) - out[i].sum()
        if need > 0:
            frac = M[i] - np.floor(M[i])
            for j in np.argsort(-frac)[:need]:
                out[i, j] += 1
        elif need < 0:
            for j in np.argsort(-out[i])[: -need]:
                out[i, j] -= 1
    return out


def site_split(truth, day):
    """Split each account's on-hand at a close into racked stock by building, floor and staging by
    building, storage trailers by yard (the yard's building) and the sublease. Off-rack stock is the
    bought-ahead stock first, then each account's share of the rest."""
    i = sim.DIDX[day]
    codes = [c for c in truth if truth[c]["OH"][i] > 0]
    oh = np.array([truth[c]["OH"][i] for c in codes], float)
    exc = np.array([max(0.0, truth[c]["E"][i]) for c in codes], float)
    total = oh.sum()
    rack_room = RACK_FILL * sum(CAP.values())
    over = max(0.0, total - rack_room)
    dhs = min(DHS_CAP * 0.985, over * 0.58) if sublease_open(day) else 0.0
    for a, b in SUBLEASE_STINTS:
        if a <= day <= b:
            dhs *= min(1.0, (b - day).days / 10.0)       # the sublease is emptied over its last ten days
    trl = min(MAX_TRAILERS * TRAILER_CAP * 0.93, (over - dhs) * 0.62)
    flr = over - dhs - trl
    w = exc + 0.15 * oh
    w = w / w.sum() if w.sum() > 0 else oh / oh.sum()
    off = np.minimum(oh, over * w)
    racked = oh - off
    # racked across buildings: home bias, columns to each building's share of the racked total
    seed = np.ones((len(codes), len(SITES)))
    for r, c in enumerate(codes):
        seed[r, SITES.index(W.HOME[c])] = 6.0
    cap = np.array([CAP[s] for s in SITES], float)
    cols = racked.sum() * cap / cap.sum()
    R = _ipf(seed, racked, cols)
    # off-rack: sublease, trailers by yard and floor/staging by building, each in proportion
    split = {}
    for r, c in enumerate(codes):
        o = off[r]
        parts = {"DHS1": o * (dhs / over) if over > 0 else 0.0}
        for s in SITES:
            share = cap[SITES.index(s)] / cap.sum()
            home = 1.6 if s == W.HOME[c] else 1.0
            parts["TRL:" + s] = o * (trl / over if over > 0 else 0.0) * share * home
            parts["FLR:" + s] = o * (flr / over if over > 0 else 0.0) * share * home * 0.68
            parts["STG:" + s] = o * (flr / over if over > 0 else 0.0) * share * home * 0.32
        tot = sum(parts.values())
        if tot > 0:
            for k in parts:
                parts[k] *= o / tot
        for j, s in enumerate(SITES):
            parts["RACK:" + s] = R[r, j]
        split[c] = parts
    # integerise each account's parts to its on-hand
    keys = ["RACK:" + s for s in SITES] + ["FLR:" + s for s in SITES] + ["STG:" + s for s in SITES] + \
           ["TRL:" + s for s in SITES] + ["DHS1"]
    M = np.array([[split[c][k] for k in keys] for c in codes])
    Mi = _round_rows(M, oh)
    return {c: {k: int(Mi[r, j]) for j, k in enumerate(keys)} for r, c in enumerate(codes)}


def site_totals(parts):
    """The WMS's site view of one account's parts: a trailer's pallets count at its yard's building."""
    out = {}
    for k, v in parts.items():
        site = k.split(":")[1] if ":" in k else k
        out[site] = out.get(site, 0) + v
    return out


# ----------------------------------------------------------------------------------- pallet snapshot

GS1_PREFIX = "0861347"          # the 3PL's own GS1 company prefix for the pallet labels it prints


def sscc(serial, ext):
    body = "%d%s%09d" % (ext, GS1_PREFIX, serial)
    s = 0
    for i, ch in enumerate(reversed(body)):
        s += int(ch) * (3 if i % 2 == 0 else 1)
    return body + str((10 - s % 10) % 10)


def rack_locations(site, n, rng):
    """Rack location codes for a building: aisle, bay, level and position."""
    out = []
    aisle = 1
    while len(out) < n:
        for bay in range(1, 61):
            for lvl in "ABCDE":
                for pos in (1, 2):
                    out.append("%s-%02d-%03d-%s%d" % (site, aisle, bay, lvl, pos))
        aisle += 1
    return out[:n]


def lpn_snapshot(truth, receipts, parts_by_acc, rng):
    """One row per pallet in a warehouse location (racks, floor lanes, dock staging, the sublease's
    racks) at the close of 6 December. Yard trailers are yard locations and are not in this export."""
    rows = []
    serial = 412000000
    # each account's newest receipts first: on-hand pallets are the latest received
    recv_days = {}
    for r in receipts:
        recv_days.setdefault(r["account"], []).append((r["day"], r["pallets"]))
    for c in recv_days:
        recv_days[c].sort(reverse=True)
    racks = {s: rack_locations(s, CAP[s], rng) for s in SITES}
    for s in SITES:
        rng.shuffle(racks[s])
    dhs_racks = rack_locations("DHS1", DHS_CAP, rng)
    rng.shuffle(dhs_racks)
    used = {s: 0 for s in SITES + ["DHS1"]}
    lane = {s: 1 for s in SITES}
    lane_fill = {s: 0 for s in SITES}
    door = {s: 1 for s in SITES}
    door_fill = {s: 0 for s in SITES}
    item_ct = {}
    for c in sorted(parts_by_acc):
        parts = parts_by_acc[c]
        # receipt dates for this account's pallets, newest first: off-rack pallets are the newest
        dates = []
        for d, p in recv_days.get(c, []):
            dates += [d] * p
        order = ["DHS1"] + ["TRL:" + s for s in SITES] + ["FLR:" + s for s in SITES] + \
                ["STG:" + s for s in SITES] + ["RACK:" + s for s in SITES]
        k = 0
        for key in order:
            n = parts.get(key, 0)
            for _ in range(n):
                d = dates[k] if k < len(dates) else dates[-1]
                k += 1
                if key.startswith("TRL:"):
                    continue
                serial += int(rng.integers(1, 4))
                code = W.ACCOUNT_NAMES[c][1]
                if code not in item_ct:
                    item_ct[code] = int(rng.integers(40, 220))
                item = "%s-%05d" % (code[2:], int(rng.integers(10001, 10001 + item_ct[code])))
                qty = int(rng.integers(18, 96))
                if key == "DHS1":
                    site, loc, typ = "DHS1", dhs_racks[used["DHS1"]], "RACK"
                    used["DHS1"] += 1
                else:
                    typ0, site = key.split(":")
                    if typ0 == "RACK":
                        loc, typ = racks[site][used[site]], "RACK"
                        used[site] += 1
                    elif typ0 == "FLR":
                        if lane_fill[site] >= 12:
                            lane[site] += 1
                            lane_fill[site] = 0
                        loc, typ = "%s-FL-%03d" % (site, lane[site]), "FLOOR"
                        lane_fill[site] += 1
                    else:
                        if door_fill[site] >= 18:
                            door[site] += 1
                            door_fill[site] = 0
                        loc, typ = "%s-STG-D%02d" % (site, door[site]), "STAGE"
                        door_fill[site] += 1
                rows.append({"site": site, "location": loc, "location_type": typ, "account": code,
                             "lpn": sscc(serial, 0), "item": item, "qty_cases": qty, "received": d})
    return rows


# ----------------------------------------------------------------------------------- booking notices

VESSELS = ["MSC ALINA", "CMA CMG BOUGAINVILLE", "COSCO SHIPPING ARIES", "OOCL HONG KONG", "EVER GLORY",
           "ONE MINATO", "YM WITNESS", "HMM GARNET", "MAERSK EMDEN", "APL CHANGI", "ZIM SAMMY OFER",
           "MSC MATTEA", "CMA CMG JACQUES SAADE", "EVER ACE", "ONE HAMBURG", "COSCO PRIDE"]
CARRIERS = {"MSC": "MSC", "CMA": "CMA CGM", "COS": "COSCO", "OOC": "OOCL", "EVE": "Evergreen", "ONE": "ONE",
            "YM ": "Yang Ming", "HMM": "HMM", "MAE": "Maersk", "APL": "APL", "ZIM": "ZIM"}
TERMINALS = ["APM Pier 400", "TraPac", "Fenix Marine", "Yusen Terminals", "Everport", "LBCT Middle Harbor",
             "TTI Pier T", "ITS Pier G", "SSA Pier A", "Pacific Container Terminal"]


def notices(truth, rng):
    """The December booking notices still to arrive after the close of 6 December: one row per booking
    (one vessel call), the boxes by size and the customer's pallet count where its notice gave one."""
    out = []
    i6 = sim.DIDX[W.LAST_CLOSE]
    i31 = sim.DIDX[dt.date(2026, 12, 31)]
    gives_pallets = {"A01": True, "A02": True, "A03": True, "A04": True, "A05": True, "A06": True,
                     "A07": False, "A08": True, "A09": False, "A10": False, "A11": True, "A12": True,
                     "A13": True, "A14": True}
    for c in W.CURRENT:
        rec = truth[c]
        byday = {}
        for (i, size, p) in rec["boxes"]:
            if i6 < i <= i31:
                byday.setdefault(sim.ALL_DAYS[i], []).append((size, p))
        for d in sorted(byday):
            boxes = byday[d]
            ves = VESSELS[int(rng.integers(0, len(VESSELS)))]
            carrier = CARRIERS.get(ves[:3], ves.split()[0].title())
            # the vessel arrives two to five days before the boxes are received
            eta = d - dt.timedelta(days=int(rng.integers(2, 6)))
            cnt = {"20": 0, "40": 0, "40HC": 0, "45": 0}
            for size, p in boxes:
                cnt[size] += 1
            out.append({"account": c, "eta": eta, "receive_by": d, "vessel": ves, "carrier": carrier,
                        "terminal": TERMINALS[int(rng.integers(0, len(TERMINALS)))],
                        "booking": "%s%08d" % (carrier[:3].upper().replace(" ", ""), int(rng.integers(10 ** 7, 10 ** 8))),
                        "boxes": cnt, "pallets": sum(p for _, p in boxes) if gives_pallets[c] else None})
    return out


# ----------------------------------------------------------------------------------- port statistics

def port_statistics(book_teu, rng):
    """Monthly TEU for the two ports, January to October 2026, in each port's own release layout.
    The book's TEU is fixed first; the ports' figures are drawn around a seasonal path with the
    autumn front-loading in them."""
    la_base = [452000, 398000, 447000, 451000, 470000, 482000, 514000, 506000, 521000, 538000]
    lb_base = [405000, 352000, 398000, 403000, 421000, 431000, 457000, 452000, 469000, 487000]
    la, lb = [], []
    for m in range(10):
        la_li = int(la_base[m] * float(np.exp(rng.normal(0, 0.012))))
        lb_li = int(lb_base[m] * float(np.exp(rng.normal(0, 0.012))))
        la.append(la_li)
        lb.append(lb_li)
    return la, lb


# ----------------------------------------------------------------------------------- clocks

PACIFIC = ZoneInfo("America/Los_Angeles")


def to_utc(d, hour, minute):
    """A Pacific wall-clock time on day d as a naive UTC datetime."""
    local = dt.datetime(d.year, d.month, d.day, hour, minute, tzinfo=PACIFIC)
    return local.astimezone(dt.timezone.utc).replace(tzinfo=None)


def utc_to_pacific_date(ts):
    """The Pacific calendar date of a naive UTC timestamp."""
    return ts.replace(tzinfo=dt.timezone.utc).astimezone(PACIFIC).date()


def run_stamp(close_day):
    """The nightly inventory run for the close of close_day starts at midnight Pacific that night."""
    return to_utc(close_day + ONE, 0, 0)


def receipt_times(receipts, rng):
    """A confirmation time for every receipt: two receiving shifts, 06:00 to 22:30 local."""
    for r in receipts:
        shift = rng.random()
        if shift < 0.62:
            h = int(rng.integers(6, 14))
        else:
            h = int(rng.integers(14, 22))
        mi = int(rng.integers(0, 60))
        if h == 21 and mi > 30:
            mi = 30
        r["received_at"] = to_utc(r["day"], h, mi)
    return receipts
