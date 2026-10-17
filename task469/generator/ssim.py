"""The schedule files in the IATA SSIM Chapter 7 layout the authority keeps (fixed 200-character records): a header,
then for each carrier a carrier record, its flight leg records (type 3) with their segment data records (type 4), and a
trailer. Each carrier's records keep the time mode it filed in: local to each station with the station's UTC
variation, or UTC. One leg record covers a period of operation and the days of the week it flies.

The positions written here are the ones the pack's layout note (kdy_schedule_file_layout.pdf) describes."""
import datetime as dt

import world as W

MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def ddmmmyy(d):
    return "%02d%s%02d" % (d.day, MON[d.month - 1], d.year % 100)


def hhmm(m):
    m = int(m) % 1440
    return "%02d%02d" % (m // 60, m % 60)


def utcvar(hours):
    return "%s%02d00" % ("-" if hours < 0 else "+", abs(hours))


def put(buf, pos, text):
    """Write text into buf (a list of 200 chars) starting at 1-based position pos."""
    for i, ch in enumerate(text):
        buf[pos - 1 + i] = ch


def record3(leg, serial):
    b = [" "] * 200
    put(b, 1, "3")
    put(b, 3, "%-3s" % leg["airline"])
    put(b, 6, "%04d" % leg["flight"])
    put(b, 10, "%02d" % leg.get("ivi", 1))
    put(b, 12, "%02d" % leg.get("leg", 1))
    put(b, 14, "J")
    put(b, 15, ddmmmyy(leg["frm"]))
    put(b, 22, ddmmmyy(leg["to"]))
    put(b, 29, leg["dow"])
    put(b, 37, leg["dep"])
    put(b, 40, hhmm(leg["std"]))
    put(b, 44, hhmm(leg["std"]))
    put(b, 48, utcvar(leg["dep_var"]))
    put(b, 55, leg["arr"])
    put(b, 58, hhmm(leg["sta"]))
    put(b, 62, hhmm(leg["sta"]))
    put(b, 66, utcvar(leg["arr_var"]))
    put(b, 73, leg["eqp"])
    put(b, 76, "Y")
    put(b, 173, "Y%d" % W.SEATS[leg["eqp"]])
    if leg.get("onward"):
        oa, of, lay = leg["onward"]
        put(b, 138, "%-3s" % oa)
        put(b, 141, "%04d" % of)
        put(b, 145, str(lay))
    put(b, 193, "0")
    put(b, 194, str(leg.get("arr_dayvar", 0)))
    put(b, 195, "%06d" % serial)
    return "".join(b)


def record4(leg, dei, data, serial):
    b = [" "] * 200
    put(b, 1, "4")
    put(b, 3, "%-3s" % leg["airline"])
    put(b, 6, "%04d" % leg["flight"])
    put(b, 10, "%02d" % leg.get("ivi", 1))
    put(b, 12, "%02d" % leg.get("leg", 1))
    put(b, 14, "J")
    k = leg.get("leg", 1)
    put(b, 29, "ABCDEF"[k - 1])
    put(b, 30, "ABCDEF"[k])
    put(b, 31, "%03d" % dei)
    put(b, 34, leg["dep"])
    put(b, 37, leg["arr"])
    put(b, 40, data)
    put(b, 195, "%06d" % serial)
    return "".join(b)


def header(serial):
    b = [" "] * 200
    put(b, 1, "1AIRLINE STANDARD SCHEDULE DATA SET")
    put(b, 192, "001")
    put(b, 195, "%06d" % serial)
    return "".join(b)


def carrier(airline, season, frm, to, created, serial, utc=False):
    b = [" "] * 200
    put(b, 1, "2")
    put(b, 2, "U" if utc else "L")
    put(b, 3, "%-3s" % airline)
    put(b, 11, season)
    put(b, 15, ddmmmyy(frm))
    put(b, 22, ddmmmyy(to))
    put(b, 29, ddmmmyy(created))
    put(b, 36, ("%s SCHEDULE AT KDY" % W.BRANDS[airline].upper())[:29])
    put(b, 195, "%06d" % serial)
    return "".join(b)


def trailer(airline, serial):
    b = [" "] * 200
    put(b, 1, "5 ")
    put(b, 3, "%-3s" % airline)
    put(b, 188, "%06d" % (serial - 1))
    put(b, 194, "E")
    put(b, 195, "%06d" % serial)
    return "".join(b)


def write(path, carriers, season, frm, to):
    """carriers: list of (airline, legs, refs, created, utc, extra) where legs are dicts for record3, refs maps a
    leg's (airline, flight, leg) to the operating flight it is sold on (a DEI 050 segment data record) and extra maps
    a leg's key to other segment data records (dei, data) the carrier files."""
    lines, serial = [], 1
    lines.append(header(serial))
    serial += 1
    for airline, legs, refs, created, utc, extra in carriers:
        lines.append(carrier(airline, season, frm, to, created, serial, utc=utc))
        serial += 1
        for lg in legs:
            lines.append(record3(lg, serial))
            serial += 1
            key = (lg["airline"], lg["flight"], lg.get("leg", 1))
            recs = list(extra.get(key, []))
            if key in refs:
                recs.append((50, "%-3s%04d" % refs[key]))
            for dei, data in sorted(recs):
                lines.append(record4(lg, dei, data, serial))
                serial += 1
        lines.append(trailer(airline, serial))
        serial += 1
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    return len(lines)


def parse(path):
    """Read the type 3 and type 4 records back (the bundle's own reader)."""
    legs, refs = [], {}
    mode = "L"
    for raw in open(path, encoding="ascii"):
        s = raw.rstrip("\r\n")
        if not s:
            continue
        if s[0] == "3":
            onward = None
            if s[137:140].strip():
                onward = (s[137:140].strip(), int(s[140:144]), int(s[144]))
            legs.append(dict(airline=s[2:5].strip(), flight=int(s[5:9]), ivi=int(s[9:11]), leg=int(s[11:13]),
                             frm=s[14:21], to=s[21:28], dow=s[28:35], freq=s[35], dep=s[36:39], std=s[39:43],
                             dep_var=s[47:52], arr=s[54:57], sta=s[57:61], arr_var=s[65:70], eqp=s[72:75],
                             onward=onward, arr_dayvar=int(s[193]), serial=int(s[194:200]), mode=mode))
        elif s[0] == "4" and s[30:33] == "050":
            refs[(s[2:5].strip(), int(s[5:9]), int(s[11:13]))] = (s[39:42].strip(), int(s[42:46]))
        elif s[0] == "2":
            mode = s[1]
    return legs, refs


def to_date(s):
    return dt.date(2000 + int(s[5:7]), MON.index(s[2:5]) + 1, int(s[0:2]))
