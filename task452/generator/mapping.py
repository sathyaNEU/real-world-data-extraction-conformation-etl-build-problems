"""The final change map as the remote sensing team delivers it: deforestation patches (connected areas of change on
the national mosaic, each at least the 0.5 ha minimum mapping unit, areas by pixel counting on the 30 m grid) by 2025
district, vectorised by 10 km delivery tile and by quarter of first detection, so a patch cleared over several
quarters or crossing a tile edge is delivered as several polygons, each carrying its own area and the area of the
patch it belongs to; and the map's class areas by district."""
import datetime as dt
import math

import numpy as np

import landscape as L
import world as W

TILE = 10_000            # metres
MMU_PIX = 6              # the 0.5 ha minimum mapping unit, in 30 m pixels (0.54 ha)
MAX_PIX = 4_444          # about 400 ha
QSTART = [dt.date(2024 + q // 4, 3 * (q % 4) + 1, 1) for q in range(8)] + [dt.date(2026, 1, 1)]


def quarter(day):
    return (day.year - 2024) * 4 + (day.month - 1) // 3


def pixels(ha):
    return int(round(ha / W.PIXEL_HA))


def fd_pixels_by_district2025():
    """the final map's deforestation by 2025 district in 30 m pixels: the program's districts from the class areas,
    the highland districts outside the accounting area as mapped"""
    return {d: v["FD"] for d, v in class_pixels_2025().items()}


def district2025_boxes():
    import interp as I
    b = I.district_boxes()
    out = {}
    for code in W.DCODE:
        x0, y0, w, h = b[code]
        if code == "05":
            out[W.D2025[code]] = (x0, y0, w * 0.62, h)
            out[W.SPLIT_NEW[0]] = (x0 + w * 0.62, y0, w * 0.38, h)
        else:
            out[W.D2025[code]] = b[code]
    for i, (code, _, _) in enumerate(W.HIGHLANDS):
        out[W.D2025[code]] = (420_000 + i * 125_000, 580_000, 100_000, 100_000)
    return out


def patches():
    """deforestation patches by 2025 district, sizes in pixels summing to the district's mapped deforestation"""
    rng = np.random.default_rng(W.SEED + 21)
    boxes = district2025_boxes()
    out = []
    for d, pix in sorted(fd_pixels_by_district2025().items()):
        sizes = []
        while sum(sizes) < pix:
            s = max(MMU_PIX, pixels(math.exp(rng.normal(math.log(1.35), 1.05))))
            sizes.append(min(s, MAX_PIX))
        excess = sum(sizes) - pix
        while excess > 0:                          # trim the largest patches so the sizes sum to the mapped area
            j = int(np.argmax(sizes))
            cut = min(excess, sizes[j] - MMU_PIX)
            sizes[j] -= cut
            excess -= cut
        x0, y0, w, h = boxes[d]
        for s in sizes:
            day = dt.date(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 731)))
            out.append(dict(district=d, pix=s, x=x0 + rng.random() * w, y=y0 + rng.random() * h, detected=day))
    return out


def _split(total, shares):
    """whole pixels in proportion to the shares, every part at least one pixel, summing to the total"""
    raw = [total * f for f in shares]
    out = [max(1, int(math.floor(v))) for v in raw]
    while sum(out) < total:
        k = max(range(len(raw)), key=lambda i: raw[i] - out[i])
        out[k] += 1
    while sum(out) > total:
        k = max(range(len(out)), key=lambda i: out[i])
        out[k] -= 1
    return out


def polygons():
    """the delivered polygons: each patch cut by the quarters in which its clearing was first detected and by the
    tile edges it crosses; a polygon's first detection is the earliest observation of change among its own pixels"""
    rng = np.random.default_rng(W.SEED + 23)
    rows = []
    for pt in patches():
        ha = pt["pix"] * W.PIXEL_HA
        r = math.sqrt(ha * 10_000 / math.pi)                    # radius of a disc of the patch's area, metres
        tx, ty = int(pt["x"] // TILE), int(pt["y"] // TILE)
        dx, dy = pt["x"] - tx * TILE, pt["y"] - ty * TILE
        cuts_x = [c for c in (dx, TILE - dx) if c < 0.8 * r]
        cuts_y = [c for c in (dy, TILE - dy) if c < 0.8 * r]
        tiles = [(tx, ty, 1.0)]
        nx = ny = None
        if cuts_x:
            f = 0.5 - min(cuts_x) / (2 * r)                      # share beyond the vertical edge
            nx = tx - 1 if dx < TILE - dx else tx + 1
            tiles = [(tx, ty, 1 - f), (nx, ty, f)]
        if cuts_y:
            g = 0.5 - min(cuts_y) / (2 * r)
            ny = ty - 1 if dy < TILE - dy else ty + 1
            tiles = [(a, b, s * (1 - g)) for a, b, s in tiles] + [(a, ny, s * g) for a, b, s in tiles]

        def centre(a, b, jit):
            """a polygon's centroid: the patch's centre in its own tile, beyond an edge the centroid of the part
            of the patch lying past it"""
            x, y = pt["x"] + jit[0], pt["y"] + jit[1]
            if a != tx:
                edge = (tx if nx < tx else tx + 1) * TILE
                x = edge + (1 if nx > tx else -1) * (5 + 0.4 * max(0.0, r - min(cuts_x))) + 0.3 * jit[0]
            if b != ty:
                edge = (ty if ny < ty else ty + 1) * TILE
                y = edge + (1 if ny > ty else -1) * (5 + 0.4 * max(0.0, r - min(cuts_y))) + 0.3 * jit[1]
            return (int(min(max(x, a * TILE + 3), a * TILE + TILE - 3)),
                    int(min(max(y, b * TILE + 3), b * TILE + TILE - 3)))
        q0 = quarter(pt["detected"])
        k = min(1 + int(rng.poisson(0.35 * ha ** 0.45)), 8 - q0, pt["pix"])   # quarters over which it was cleared
        fr = rng.dirichlet([2.0] + [1.0] * (k - 1)) if k > 1 else np.array([1.0])
        for qi, qpix in enumerate(_split(pt["pix"], list(fr))):
            q = q0 + qi
            qday = pt["detected"] if qi == 0 else QSTART[q] + dt.timedelta(
                days=int(rng.integers(0, (QSTART[q + 1] - QSTART[q]).days)))
            tp = rng.multinomial(qpix, np.array([s for _, _, s in tiles]) / sum(s for _, _, s in tiles))
            for (a, b, _), c in zip(tiles, tp):
                if c == 0:
                    continue
                day = qday if (a, b) == (tx, ty) else min(qday + dt.timedelta(days=int(rng.integers(0, 21))),
                                                          QSTART[q + 1] - dt.timedelta(days=1))
                cx, cy = centre(a, b, rng.normal(0, 0.15 * r, 2))
                rows.append(dict(district=pt["district"], tile="T%03d-%03d" % (a, b), area_pix=int(c),
                                 patch_pix=pt["pix"], detected=day, x=cx, y=cy))
    order = sorted(range(len(rows)), key=lambda i: (rows[i]["tile"], rows[i]["detected"], rows[i]["x"]))
    out = []
    for k, i in enumerate(order, 1):
        r = rows[i]
        r["polygon_id"] = "P%06d" % (100_000 + k * 7 + int(rng.integers(0, 7)))
        out.append(r)
    return out


def class_pixels_2025():
    """the final map's three classes by 2025 district, in 30 m pixels"""
    FA = L.final_areas()
    out = {}
    for code in W.DCODE:
        vals = {f: FA[(code, f)] for f in ("FD", "FF", "FN")}
        if code == "05":
            out[W.SPLIT_NEW[0]] = {f: pixels(v * W.SPLIT_SHARE) for f, v in vals.items()}
            out[W.D2025[code]] = {f: pixels(v * (1 - W.SPLIT_SHARE)) for f, v in vals.items()}
        else:
            out[W.D2025[code]] = {f: pixels(v) for f, v in vals.items()}
    hl_area = {"13": 820_000, "14": 1_140_000, "15": 610_000, "16": 990_000, "17": 760_000, "18": 1_050_000}
    hl_forest = {"13": 410_000, "14": 520_000, "15": 180_000, "16": 470_000, "17": 300_000, "18": 560_000}
    for code, _, ha in W.HIGHLANDS:
        out[W.D2025[code]] = {"FD": pixels(ha), "FF": pixels(hl_forest[code] - ha),
                              "FN": pixels(hl_area[code] - hl_forest[code])}
    return out


def class_areas_2025():
    """the final map's three classes by 2025 district (hectares, by pixel counting), for the map statistics"""
    return {d: {f: round(v * W.PIXEL_HA, 2) for f, v in c.items()} for d, c in class_pixels_2025().items()}
