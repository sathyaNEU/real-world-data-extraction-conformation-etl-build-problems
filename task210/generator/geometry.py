"""A haul road's passage exposure at MP1 as a solver can take it from the survey and the working scheme.

Three families of measure, each a sum over the road of length over squared distance (or its BS 5228 equivalent):
  level60   the stretch at road level 60 m AOD or higher (the original ground), with its length;
  los       the stretch with a line of sight to the microphone past the pit crest, the bench crest and the bund, for a
            source 1, 2 and 3.5 m above the road;
  bs5228    BS 5228-1 Annex F haul-road method: per straight segment the angle of view over 180 degrees divided by the
            distance (perpendicular to the road line, to the segment's midpoint, or to its nearest point), less 10 dB
            where a barrier hides the source and 5 dB where it is just visible over it.
screens.py applies them to the world's coordinates, checks.py to the shipped survey and scheme."""
import math

MIC = 59.5   # MP1 microphone level, m AOD


def _hit(p, q, a, b):
    d1 = (q[0] - p[0], q[1] - p[1]); d2 = (b[0] - a[0], b[1] - a[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return None
    w = (a[0] - p[0], a[1] - p[1])
    t = (w[0] * d2[1] - w[1] * d2[0]) / den
    u = (w[0] * d1[1] - w[1] * d1[0]) / den
    if 1e-9 < t < 1 - 1e-9 and 0.0 <= u <= 1.0:
        return t, u
    return None


def blocked(pt, hs, barriers):
    """True when the line from a source hs above pt to the microphone passes below a barrier's crest."""
    src = (pt[0], pt[1], pt[2] + hs)
    for poly in barriers:
        for i in range(len(poly) - 1):
            h = _hit(src, (0.0, 0.0), poly[i], poly[i + 1])
            if h:
                t, u = h
                if poly[i][2] + u * (poly[i + 1][2] - poly[i][2]) > src[2] + t * (MIC - src[2]):
                    return True
    return False


def _samples(pts, step=1.0):
    out = []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.dist(a[:2], b[:2]); n = max(1, int(round(L / step)))
        for k in range(n):
            f = (k + 0.5) / n
            out.append((a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]), a[2] + f * (b[2] - a[2]), L / n))
    return out


def _r3(s):
    return math.sqrt(s[0] ** 2 + s[1] ** 2 + (s[2] + 1.5 - MIC) ** 2)


def _bearing(x, y):
    return math.degrees(math.atan2(y, x)) % 360.0


def measures(pts, barriers):
    """Every measure for one polyline of (x, y, level) in metres about MP1."""
    S = _samples(pts)
    m = {}
    up = [s for s in S if s[2] >= 60.0]
    m['level60_int'] = sum(s[3] / _r3(s) ** 2 for s in up)
    m['level60_len'] = sum(s[3] for s in up)
    mean_r = sum(s[3] * _r3(s) for s in up) / max(m['level60_len'], 1e-9)
    m['level60_len_at_mean_r'] = m['level60_len'] / mean_r ** 2
    for hs in (1.0, 2.0, 3.5):
        vis = [s for s in S if not blocked(s, hs, barriers)]
        m['los_h%.1f_int' % hs] = sum(s[3] / _r3(s) ** 2 for s in vis)
        m['los_h%.1f_len' % hs] = sum(s[3] for s in vis)
    for kind in ('perp', 'mid', 'near'):
        tot = 0.0
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            th = abs((_bearing(b[0], b[1]) - _bearing(a[0], a[1]) + 180.0) % 360.0 - 180.0)
            L = math.dist(a[:2], b[:2])
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
            if kind == 'perp':
                d = abs(a[0] * b[1] - a[1] * b[0]) / L
            elif kind == 'mid':
                d = math.hypot(mid[0], mid[1])
            else:
                f = max(0.0, min(1.0, -(a[0] * (b[0] - a[0]) + a[1] * (b[1] - a[1])) / L ** 2))
                d = math.hypot(a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))
            hid = blocked(mid, 3.5, barriers)
            just = (not hid) and blocked(mid, 1.0, barriers)
            tot += 10 ** (-(10.0 if hid else 5.0 if just else 0.0) / 10.0) * (th / 180.0) / max(d, 1e-6)
        m['bs5228_%s' % kind] = tot
    return m


def compare(a_pts, b_pts, barriers):
    """dB of road b over road a under every measure."""
    ma, mb = measures(a_pts, barriers), measures(b_pts, barriers)
    return {k: 10 * math.log10(mb[k] / ma[k]) for k in ma}


def world_geometry(W):
    """Haul road 2 and the Phase 4 road (each alone and with its ramp) and the barriers, from the world's coordinates."""
    bars = [W.pit_crest(), W.bench_crest(), W.BUND]
    road2 = W.ROADS['north']['pts']; road4 = W.ROADS['ext']['pts']
    route2 = W.ROADS['north_up']['pts'] + road2[1:]
    route4 = W.ROADS['ext_up']['pts'] + road4[1:]
    return dict(road2=road2, road4=road4, route2=route2, route4=route4, barriers=bars)


def scalings(G):
    """Phase 4 over Haul road 2, as an energy ratio, under every measure on the roads and on the routes."""
    out = {}
    for lev in ('road', 'route'):
        for k, v in compare(G[lev + '2'], G[lev + '4'], G['barriers']).items():
            out['%s_%s' % (lev, k)] = 10 ** (v / 10.0)
    return out


def pack_geometry(tgt):
    """The same roads and barriers read back from the shipped survey (geojson) and working scheme (docx tables)."""
    import json
    import os
    import zipfile
    import xml.etree.ElementTree as ET
    f = [x for x in sorted(os.listdir(tgt)) if x.startswith('ravensby_topographic_survey')][0]
    fc = json.load(open(os.path.join(tgt, f)))
    feats = {(ft['properties']['layer'], ft['properties']['name']): ft['geometry'] for ft in fc['features']}
    mp1 = feats[('MONITORING', 'MP1 Ulverthorpe Lane')]['coordinates']
    lat0, lon0 = mp1[1], mp1[0]

    def xy(lon, lat, z=0.0):
        return ((lon - lon0) * 111320.0 * math.cos(math.radians(lat0)), (lat - lat0) * 111132.0, z)

    def line(layer, name):
        return [xy(*c) for c in feats[(layer, name)]['coordinates']]
    crest = [g for (ly, _n), g in feats.items() if ly == 'CREST'][0]['coordinates']
    bund = [g for (ly, _n), g in feats.items() if ly == 'BUND'][0]['coordinates']
    s = [x for x in sorted(os.listdir(tgt)) if x.startswith('phase4_working_scheme')][0]
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    root = ET.fromstring(zipfile.ZipFile(os.path.join(tgt, s)).read('word/document.xml'))
    pts = {}
    for tr in root.iter(w + 'tr'):
        cells = [''.join(t.text or '' for t in tc.iter(w + 't')) for tc in tr.iter(w + 'tc')]
        if len(cells) == 4 and cells[0][:2] in ('C-', 'R-', 'P4'):
            pts[cells[0]] = xy(float(cells[2]), float(cells[1]), float(cells[3]))

    def order(pre):
        return [pts[k] for k in sorted((k for k in pts if k.startswith(pre)), key=lambda k: int(k.split('-')[1]))]
    bench, ramp, road4 = order('C-'), order('R-'), order('P4-')
    road2 = line('HAUL_ROAD', 'Haul road 2')
    route2 = line('HAUL_ROAD', 'North face ramp') + road2[1:]
    route4 = ramp + road4
    bars = [[xy(*c) for c in crest], bench, [xy(*c) for c in bund]]
    return dict(road2=road2, road4=road4, route2=route2, route4=route4, barriers=bars,
                road4_survey=line('PROPOSED', 'Phase 4 haul road'), n_scheme_points=len(pts))
