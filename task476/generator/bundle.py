"""Read the pack under target/ the way a solver must: every figure the golden, the checks and the ceiling use comes
from these parsers, never from the simulation."""
import csv
import datetime as dt
import math
import os
import re
from zoneinfo import ZoneInfo

import pdfplumber
from openpyxl import load_workbook

LA = ZoneInfo("America/Los_Angeles")
UTC = dt.timezone.utc
PST = dt.timezone(dt.timedelta(hours=-8))
WY0 = dt.datetime(2025, 10, 1, tzinfo=LA)
WY1 = dt.datetime(2026, 10, 1, tzinfo=LA)


def _p(target, *parts):
    return os.path.join(target, *parts)


def find(target, sub, pat):
    d = _p(target, sub)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if re.search(pat, f))


def register(target):
    wb = load_workbook(find(target, "ranch", r"well_register")[0], read_only=True)
    ws = wb["Wells"]
    rows = list(ws.iter_rows(values_only=True))
    head = [str(h) for h in rows[0]]
    out = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        out[d["Well"]] = d
    return out


def power(target, reg):
    """Every interval as (well, start in UTC, minutes, kWh); the old export's clock-face local times resolved with the
    fall-back hour's two rows taken in file order."""
    sa_old = {str(d["Electric SA (to Mar 31, 2026)"]): w for w, d in reg.items()}
    sa_new = {str(d["Electric SA (from Apr 1, 2026)"]): w for w, d in reg.items()}
    out = {w: [] for w in reg}
    f_old = find(target, "power", r"usage_export")[0]
    with open(f_old, newline="", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith("SERVICE AGREEMENT"))
    seen = {}
    for r in csv.reader(lines[i0 + 1:]):
        if not r:
            continue
        sa, _, day, start = r[0], r[1], r[2], r[3]
        y, m, d_ = map(int, day.split("-"))
        hh, mm = map(int, start.split(":"))
        key = (sa, day, start)
        fold = seen.get(key, 0)
        seen[key] = fold + 1
        t = dt.datetime(y, m, d_, hh, mm, tzinfo=LA, fold=fold).astimezone(UTC)
        out[sa_old[sa]].append((t, 60, float(r[5])))
    f_new = find(target, "power", r"interval_data")[0]
    with open(f_new, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        for r in rd:
            t = dt.datetime.strptime(r["interval_start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            out[sa_new[r["service_agreement_id"]]].append((t, int(r["interval_seconds"]) // 60,
                                                          int(r["energy_wh"]) / 1000.0))
    for w in out:
        out[w].sort(key=lambda z: z[0])
    return out


def loggers(target):
    """serial -> {PST hour: value}; vented files give depth below the tube top, absolute files total pressure head."""
    out = {}
    for f in find(target, "levels", r"^\d+\.csv$") + find(target, "levels", r"barologger"):
        lines = open(f, encoding="utf-8").read().splitlines()
        serial = re.search(r"(\d+)", os.path.basename(f)).group(1)
        if lines[0].startswith("Serial_number"):
            i0 = next(i for i, l in enumerate(lines) if l.startswith("Date,Time,ms,LEVEL"))
            baro = "barologger" in os.path.basename(f)
            vals = {}
            for r in csv.reader(lines[i0 + 1:]):
                t = dt.datetime.strptime(r[0] + " " + r[1], "%Y/%m/%d %H:%M:%S")
                t = t.replace(tzinfo=UTC if baro else PST)
                vals[t.astimezone(PST)] = float(r[3])
            out[serial] = ("baro" if baro else "absolute", vals)
        else:
            i0 = next(i for i, l in enumerate(lines) if l.startswith("Date Time"))
            vals = {}
            for r in csv.reader(lines[i0 + 1:]):
                t = dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=PST)
                vals[t] = float(r[1])
            out[serial] = ("vented", vals)
    return out


def download_log(target):
    rows = list(csv.DictReader(open(find(target, "levels", r"download_log")[0], encoding="utf-8")))
    return rows


def site_history(target, reg):
    """well -> sorted [(local time, serial logging there from that time)], from the technician's visits: each row's
    logger is the one read out at that site, and a move puts the installed serial there after the visit."""
    name = {str(d["Ranch name"]).split(" (")[0]: w for w, d in reg.items()}
    hist = {w: [] for w in reg}
    for r in download_log(target):
        if r["site"] not in name:
            continue
        w = name[r["site"]]
        t = dt.datetime.strptime(r["visit_local"], "%Y-%m-%d %H:%M").replace(tzinfo=LA)
        if not hist[w] or hist[w][-1][1] != r["logger_sn"]:
            hist[w].append((t, r["logger_sn"]))
        m = re.search(r"; (\d+) installed from", r["action"])
        if m:
            hist[w].append((t + dt.timedelta(minutes=1), m.group(1)))
    return hist


def serial_at(hist, well, t):
    moves = hist[well]
    cur = moves[0][1]
    for t0, s in moves:
        if t >= t0:
            cur = s
    return cur


def _num(pat, text):
    m = re.search(pat, text)
    return float(m.group(1).replace(",", "")) if m else None


def tests(target, reg):
    """Each report's job, date, account and printed figures; the well found through its account or state well no."""
    sa_old = {str(d["Electric SA (to Mar 31, 2026)"]): w for w, d in reg.items()}
    swn = {str(d["State well no."]): w for w, d in reg.items()}
    out = []
    for f in find(target, "pump_tests", r"\.pdf$"):
        with pdfplumber.open(f) as pdf:
            text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
        if "GUTIERREZ" in text:
            job = re.search(r"Job (GPT-\d\d-\d+)", text).group(1)
            date = dt.datetime.strptime(re.search(r"Test date ([A-Za-z]+ \d+, \d{4})", text).group(1), "%B %d, %Y").date()
            sa = re.search(r"Electric account (\d{10})", text).group(1)
            well = sa_old.get(sa)
            if well is None:
                pump = re.search(r"Pump (Pump \d+|Deep \d+)", text)
                well = {str(d["Ranch name"]).split(" (")[0]: w for w, d in reg.items()}.get(pump.group(1)) if pump else None
            rec = dict(job=job, date=date, sa=sa, well=well,
                       swl=_num(r"Standing water level \(ft\) ([\d.]+)", text),
                       pwl=_num(r"Pumping water level \(ft\) ([\d.]+)", text),
                       th=_num(r"Total head \(ft\) ([\d.]+)", text),
                       ope=_num(r"Overall plant efficiency \(%\) ([\d.]+)", text),
                       kwh_af=_num(r"kWh per acre-foot ([\d,]+)", text),
                       gpm=_num(r"Flow rate \(gpm\) ([\d,]+)", text),
                       kw=_num(r"Input kW ([\d.]+)", text), superseded="Bowl assembly" in text)
        else:
            job = re.search(r"ref (BHS-\d+)", text).group(1)
            date = dt.datetime.strptime(re.search(r"Date / time (\d\d/\d\d/\d{4})", text).group(1), "%m/%d/%Y").date()
            sa = re.search(r"Utility SA (\d{10})", text).group(1)
            s = re.search(r"State well no\. ([0-9A-Z/-]+)", text).group(1)
            rec = dict(job=job, date=date, sa=sa, well=swn.get(s) or sa_old.get(sa),
                       swl=_num(r"SWL, ft bgs ([\d.]+)", text), pwl=_num(r"PWL, ft bgs ([\d.]+)", text),
                       th=_num(r"TDH, ft ([\d.]+)", text), ope=_num(r"OPE, % ([\d.]+)", text),
                       kwh_af=_num(r"Energy, kWh/AF ([\d.]+)", text), gpm=_num(r"Capacity, gpm ([\d,]+)", text),
                       kw=_num(r"Motor input, kW ([\d.]+)", text), superseded="Note:" in text)
        out.append(rec)
    return out


def current_tests(target, reg):
    """Each pump's test: the latest report dated after the pump's installation."""
    best = {}
    for r in tests(target, reg):
        inst = dt.datetime.strptime(str(reg[r["well"]]["Pump installed"])[:10], "%Y-%m-%d").date()
        if r["date"] < inst:
            continue
        if r["well"] not in best or r["date"] > best[r["well"]]["date"]:
            best[r["well"]] = r
    return best


def meter_reads(target):
    wb = load_workbook(find(target, "ranch", r"totalizer_reads")[0], read_only=True)
    rows = list(wb["Reads"].iter_rows(values_only=True))
    head = rows[0]
    return [dict(zip(head, r)) for r in rows[1:]]


def notice(target):
    with pdfplumber.open(find(target, "agency", r"allocation_notice")[0]) as pdf:
        text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    alloc = 0.0
    for m in re.finditer(r"^(\d{3}-\d{3}-\d{2}) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)$", text, re.M):
        alloc += float(m.group(5))
    carry = float(re.search(r"carryover, as confirmed .*? is (\d+) acre-feet", text.replace("\n", " ")).group(1))
    block = int(re.search(r"in whole blocks of (\d+) acre-feet", text.replace("\n", " ")).group(1))
    return dict(text=text, allocation=round(alloc, 1), carryover=carry, available=round(alloc + carry, 1), block=block)


def tariff_text(target):
    with pdfplumber.open(find(target, "power", r"tou_schedules")[0]) as pdf:
        return "\n".join(pg.extract_text() or "" for pg in pdf.pages)


def tariff(target):
    with pdfplumber.open(find(target, "power", r"tou_schedules")[0]) as pdf:
        text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    rates = {}
    for line in text.splitlines():
        tok = line.split()
        if len(tok) >= 4 and tok[0] in ("AG-2T", "AG-3T") and tok[1] in ("Summer", "Winter"):
            nums = [float(v) for v in tok[2:]]
            if tok[1] == "Summer" and len(nums) == 3:
                rates.setdefault(tok[0], {})["summer"] = {"peak": nums[0], "part": nums[1], "off": nums[2]}
            elif tok[1] == "Winter" and len(nums) == 2:
                rates.setdefault(tok[0], {})["winter"] = {"part": nums[0], "off": nums[1]}
    return rates


def rate_letter(target):
    with pdfplumber.open(find(target, "power", r"rate_change")[0]) as pdf:
        text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    sas = re.findall(r"^(SA-\d{7}) .*? AG-2T AG-3T June 1, 2026$", text, re.M)
    return dict(sas=sas, effective=dt.datetime(2026, 6, 1, tzinfo=LA))


HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7),
            dt.date(2026, 11, 11), dt.date(2026, 11, 26), dt.date(2026, 12, 25)}


def period(local):
    season = "summer" if 6 <= local.month <= 9 else "winter"
    wk = local.weekday() < 5 and local.date() not in HOLIDAYS
    m = local.hour * 60 + local.minute
    if season == "summer":
        if wk and 720 <= m < 1080:
            return season, "peak"
        if wk and (510 <= m < 720 or 1080 <= m < 1290):
            return season, "part"
        return season, "off"
    return season, ("part" if wk and 510 <= m < 1290 else "off")


def hour_key(t):
    """The Pacific standard hour holding an instant."""
    p = t.astimezone(PST)
    return p.replace(minute=0, second=0, microsecond=0)


def quarter_key(t):
    """The logger instant (every 15 minutes, Pacific standard time) at or before an instant."""
    p = t.astimezone(PST)
    return p.replace(minute=15 * (p.minute // 15), second=0, microsecond=0)
