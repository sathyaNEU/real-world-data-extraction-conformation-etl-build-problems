"""Reads the shipped pack (target/) and nothing else: the cards and their verbatims, the handout log, the revenue
control system's four quarterly extracts, the service-area ZIP list, the city-market table, the 2027 schedule and the
pitch standard's shortlist. Everything the golden and the rungs compute starts here."""
import csv
import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np

FILES = {
    "cards": "brennick_parking_survey_2026_cards.csv",
    "verbatims": "brennick_parking_survey_2026_verbatims.csv",
    "handout": "brennick_parking_survey_2026_handout_log.pdf",
    "methods": "brennick_parking_survey_2026_methods_report.pdf",
    "q1": "brennick_parcs_daily_entries_2026q1.csv",
    "q2": "brennick_parcs_daily_entries_2026q2.csv",
    "q3": "brennick_parcs_daily_entries_2026q3.csv",
    "q4": "brennick_parcs_daily_entries_2026q4.csv",
    "zips": "kvr_service_area_zip_codes.csv",
    "markets": "bureau_city_markets.csv",
    "schedule": "kvr_nonstop_schedule_2027.pdf",
    "standard": "bureau_air_service_pitch_standard_2027.pdf",
    "rates": "brennick_public_parking_rates_2026.pdf",
}
MONTH = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                         "Dec"])}
MONTHS_LONG = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                               "August", "September", "October", "November", "December"])}
LONG_STAY = {"ECONOMY C": "Economy C", "ECONOMY D": "Economy D", "LONG TERM": "Long-Term", "EC": "Economy C",
             "ED": "Economy D", "LT": "Long-Term"}
PLAZA_LOT = {"Plaza C": "Economy C", "Plaza D": "Economy D", "Plaza L": "Long-Term"}
LOTS = ["Economy C", "Economy D", "Long-Term"]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def zip5(z):
    d = re.sub(r"\D", "", z or "")
    return d[:5] if len(d) >= 5 else None


def party_written(s):
    """The people in the party as the traveller wrote them: a number standing alone, or before a word on who they are
    ("2 (me and my wife)", "3 incl. me"), is the party; parts written as a sum ("2+2", "2 adults 1 kid") are added, and
    "me + 2" is the traveller and two more."""
    s = s.strip()
    m = re.fullmatch(r"(\d+)(?:\s*\(.*\)|\s+incl(?:\.|uding) me)?", s)
    if m:
        return int(m.group(1))
    m = re.fullmatch(r"me \+ (\d+)", s)
    if m:
        return 1 + int(m.group(1))
    m = re.fullmatch(r"(\d+) ?\+ ?(\d+)", s) or re.fullmatch(r"(\d+) adults? (\d+) kids?", s)
    if m:
        return int(m.group(1)) + int(m.group(2))
    raise ValueError("party as written not read: %r" % s)


def party_summed(s):
    """Every number written added, 'me' one: a reading of the write-ins that counts a party twice where its number
    comes with a word on who it is."""
    n = sum(int(v) for v in re.findall(r"\d+", s))
    if re.search(r"\bme\b", s, re.I):
        n += 1
    return n


def pdf_tables(path):
    import pdfplumber
    out = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            out.append((page.extract_text() or "", page.extract_tables()))
    return out


def pdf_text(path):
    return "\n".join(t for t, _ in pdf_tables(path))


class Pack:
    def __init__(self, target):
        self.target = target
        f = lambda k: os.path.join(target, FILES[k])
        # the cards: the batch the export carries twice is the same rows again
        raw = read_csv(f("cards"))
        seen = {}
        self.dup_rows = 0
        self.dup_identical = True
        self.repeats = []
        for r in raw:
            key = r["card_no"]
            if key in seen:
                self.dup_identical &= seen[key] == r
                self.dup_rows += 1
                self.repeats.append(key)
                continue
            seen[key] = r
        self.cards = list(seen.values())
        self.raw_rows = len(raw)
        self.dup_batch = ",".join(sorted({seen[k]["keying_batch"] for k in self.repeats}))
        verb = defaultdict(dict)
        for r in read_csv(f("verbatims")):
            verb[r["card_no"]][r["question"]] = r["as_written"]
        self.verb = verb
        # the handout log: each day's card ranges by plaza
        self.handout = []        # (wave, date, lot, first serial, last serial, handed)
        for text, tables in pdf_tables(f("handout")):
            m = re.search(r"Wave (\d): .*? (\d{4})", text)
            year = int(m.group(2)) if m else 2026
            for t in tables:
                for row in t[1:]:
                    if not row[0] or row[0].startswith("Wave"):
                        continue
                    mm, dd, yy = row[0].split()[1].split("/")
                    d = dt.date(int(yy), int(mm), int(dd))
                    a, b = row[2], row[3]
                    self.handout.append((int(a[0]), d, PLAZA_LOT[row[1]], int(a[1:]), int(b[1:]),
                                         int(row[4].replace(",", ""))))
        # the methods report: each wave's last box collection
        txt = pdf_text(f("methods"))
        self.close = {}
        for m in re.finditer(r"\n(\d) (\d+) (\w+) to (\d+) (\w+) 2026 Night of (\d+) (\w+) 2026", txt):
            self.close[int(m.group(1))] = dt.date(2026, MONTHS_LONG[m.group(7)], int(m.group(6)))
        self.methods_text = txt
        # the register: transient entries by day and long-stay lot
        self.entries = defaultdict(int)          # (date, lot) -> transient entries
        self.permits = defaultdict(int)
        self.garage = defaultdict(int)
        self.by_file = defaultdict(int)          # quarter file -> long-stay transient entries
        for q in (1, 2, 3, 4):
            for r in read_csv(f("q%d" % q)):
                if "Date" in r:
                    d = dt.datetime.strptime(r["Date"], "%m/%d/%Y").date()
                    lot, n, p = r["Lot"], int(r["Transient Entries"]), 0
                else:
                    d = dt.date.fromisoformat(r["business_date"])
                    lot, n, p = r["facility"], int(r["transient_entries"]), int(r["permit_entries"])
                if lot in LONG_STAY:
                    self.entries[(d, LONG_STAY[lot])] += n
                    self.permits[(d, LONG_STAY[lot])] += p
                    self.by_file[q] += n
                else:
                    self.garage[d] += n
        self.zip_rows = read_csv(f("zips"))
        self.sa_zips = {r["zip_code"] for r in self.zip_rows}
        self.market_rows = read_csv(f("markets"))
        self.market_of = {r["code"]: r["market_code"] for r in self.market_rows}
        self.market_name = {r["market_code"]: r["city_market"] for r in self.market_rows}
        # the 2027 schedule: the airports Kessick Valley serves nonstop
        self.served_airports = []
        for text, tables in pdf_tables(f("schedule")):
            for t in tables:
                for row in t[1:]:
                    m = re.search(r"\((\w{3})\)", row[2] or "")
                    if m:
                        self.served_airports.append(m.group(1))
        self.served = sorted({self.market_of[a] for a in self.served_airports})
        # the standard's shortlist (Appendix A)
        self.shortlist = []
        for text, tables in pdf_tables(f("standard")):
            for t in tables:
                if t and t[0][:2] == ["Market", "Code"]:
                    self.shortlist += [row[1] for row in t[1:]]
        self.candidates = [m for m in self.shortlist if m not in self.served]
        self.standard_text = pdf_text(f("standard"))
        self.rates_text = pdf_text(f("rates"))
        self._arrays()

    def _arrays(self):
        """One row per card: wave, handout day index, lot, nights, service area, market, parties."""
        starts = {}
        rng = {}
        for w, d, lot, a, b, n in self.handout:
            starts[w] = min(starts.get(w, d), d)
            rng.setdefault(w, []).append((a, b, d, lot))
        for w in rng:
            rng[w].sort()
        self.wave_start = starts
        self.close_day = {w: (self.close[w] - starts[w]).days + 1 for w in starts}
        n = len(self.cards)
        self.wave = np.zeros(n, dtype=int)
        self.t = np.zeros(n, dtype=int)
        self.lot = np.zeros(n, dtype=int)
        self.L = np.zeros(n, dtype=int)
        self.sa = np.zeros(n, dtype=bool)
        self.mkt = np.empty(n, dtype=object)
        self.dest = np.empty(n, dtype=object)
        self.party = np.zeros(n)
        self.party_coded = np.zeros(n)
        self.party_summed = np.zeros(n)
        self.t_box = np.zeros(n, dtype=int)
        import bisect
        self.zip_raw = np.empty(n, dtype=object)
        self.zip5 = np.empty(n, dtype=object)
        self.coding_consistent = True
        for i, c in enumerate(self.cards):
            w = int(c["wave"])
            s = int(c["card_no"][1:])
            k = bisect.bisect_right([a for a, b, d, lot in rng[w]], s) - 1
            a, b, d, lot = rng[w][k]
            assert a <= s <= b
            self.wave[i] = w
            self.t[i] = (d - starts[w]).days + 1
            self.lot[i] = LOTS.index(lot)
            self.L[i] = int(c["nights"])
            box = dt.date.fromisoformat(c["box_collected"])
            self.t_box[i] = (box - starts[w]).days + 1 - self.L[i]
            z = zip5(c["home_zip"])
            self.zip_raw[i] = c["home_zip"]
            self.zip5[i] = z
            self.sa[i] = z in self.sa_zips
            self.mkt[i] = self.market_of.get(c["destination_code"])
            self.dest[i] = c["destination_code"]
            self.party_coded[i] = int(c["party"])
            q4 = self.verb[c["card_no"]]["Q4"]
            self.party[i] = party_written(q4)
            self.party_summed[i] = party_summed(q4)
            self.coding_consistent &= int(re.search(r"\d+", q4).group()) == self.party_coded[i]
        self.zip_forms = int(sum(1 for i in range(n) if self.zip_raw[i] != self.zip5[i]))

    def variant(self, sa=None, extra=()):
        """A copy reading the same files another way: a different service-area flag per card, or some cards' rows
        counted again."""
        import copy
        V = copy.copy(self)
        names = ("wave", "t", "lot", "L", "sa", "mkt", "dest", "party", "party_coded", "party_summed", "t_box",
                 "zip_raw", "zip5")
        if sa is not None:
            V.sa = sa
        if len(extra):
            idx = np.array(list(extra), dtype=int)
            for k in names:
                setattr(V, k, np.concatenate([getattr(V, k), getattr(V, k)[idx]]))
            V.cards = self.cards + [self.cards[i] for i in idx]
        return V

    def _with_repeats(self):
        pos = {c["card_no"]: i for i, c in enumerate(self.cards)}
        return self.variant(extra=[pos[k] for k in self.repeats])

    def _zips_as_keyed(self):
        return self.variant(sa=np.array([z in self.sa_zips for z in self.zip_raw]))

    def _zip_fanout(self):
        twice = {r["zip_code"] for r in self.zip_rows if sum(1 for q in self.zip_rows if q["zip_code"] == r["zip_code"])
                 > 1}
        return self.variant(extra=[i for i in range(len(self.cards)) if self.sa[i] and self.zip5[i] in twice])

    # ------------------------------------------------------------------------------------------ the register
    def quarter_entries(self, garage=False, permits=False):
        """Each quarter's transient entries in the three long-stay lots (with the garage's or the permit lanes' entries
        added only where asked)."""
        out = defaultdict(int)
        for (d, lot), n in self.entries.items():
            out[(d.month - 1) // 3 + 1] += n + (self.permits[(d, lot)] if permits else 0)
        if garage:
            for d, n in self.garage.items():
                out[(d.month - 1) // 3 + 1] += n
        return dict(out)

    def lot_quarter_entries(self):
        out = defaultdict(int)
        for (d, lot), n in self.entries.items():
            out[((d.month - 1) // 3 + 1, lot)] += n
        return dict(out)

    def handed_by_day(self, wave, lot=None):
        h = defaultdict(int)
        for w, d, l, a, b, n in self.handout:
            if w == wave and (lot is None or l == lot):
                h[(d - self.wave_start[w]).days + 1] += n
        return h


def r100(v):
    return int(round(v / 100.0)) * 100
