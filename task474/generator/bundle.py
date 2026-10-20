"""The pack read back from its files the way an analyst reads it: the State Data Center's releases (PDF tables and the
2024 workbook), the Bureau's B17001 extract, DSS's monthly SNAP counts (its town names matched to the codes file), the
codes file, the allocation rule's total, and the grants data system's exports with the closeout. The golden is computed
from this, never from the generator's copies."""
import csv
import os
import re
import subprocess

import openpyxl

import world as W


def pdf_lines(path):
    out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
    return out.splitlines()


ROW = re.compile(r"^\s*(52\d{0,3})\s+([A-Z][A-Za-z .']*?)\s{2,}([\d,]+)\s+(?:([\d,]+)\s+([\d,]+)\s+)?(\S+)"
                 r"(?:\s+([+-]\d+))?\s*$")


def release_tables(path):
    """Table 1 (first estimates) and Table 2 (revised estimates) of one PDF release: {area: value}."""
    t, cur, year = {1: {}, 2: {}}, None, {}
    for line in pdf_lines(path):
        m = re.match(r"^\s*Table ([12])\. Residents in poverty, (\d{4})", line)
        if m:
            cur = int(m.group(1))
            year[cur] = int(m.group(2))
            continue
        m = ROW.match(line)
        if cur and m and m.group(2).strip() != "State":
            t[cur][m.group(2).strip()] = int(m.group(3).replace(",", ""))
    return t, year


class Pack:
    def __init__(self, target):
        self.target = target
        self.path = lambda k: os.path.join(target, W.FILES[k])
        self._read_codes()
        self._read_sdc()
        self._read_acs()
        self._read_snap()

    # ----------------------------------------------------------------------------------- the main path's files
    def _read_codes(self):
        with open(self.path("codes"), encoding="utf-8") as f:
            self.codes = list(csv.DictReader(f))
        self.towns = [r["town"] for r in self.codes]
        self.county_of = {r["town"]: r["former_county"] for r in self.codes}
        self.region_of = {r["town"]: r["planning_region"] for r in self.codes}
        self.council_of = {r["planning_region"]: r["council_of_governments"] for r in self.codes}
        self.geoid = {r["town_geoid_region_basis"]: r["town"] for r in self.codes}
        self.regions = []
        for r in sorted(self.codes, key=lambda r: r["region_fips"]):
            if r["planning_region"] not in self.regions:
                self.regions.append(r["planning_region"])
        self.counties = []
        for r in sorted(self.codes, key=lambda r: r["county_fips"]):
            if r["former_county"] not in self.counties:
                self.counties.append(r["former_county"])

    def _read_sdc(self):
        """Each year's estimate as last published: the latest release that carries the year."""
        est, first = {}, {}
        for k in ("rel2021", "rel2022", "rel2023", "rel2024"):
            t, year = release_tables(self.path(k))
            for area, v in t[1].items():
                first[(area, year[1])] = v
                est[(area, year[1])] = v
            for area, v in t[2].items():
                est[(area, year[2])] = v
        wb = openpyxl.load_workbook(self.path("rel2025"), data_only=True)
        for row in wb["Table 1"].iter_rows(min_row=5, values_only=True):
            if row[1] and row[1] != "State":
                first[(row[1], 2024)] = int(row[2])
                est[(row[1], 2024)] = int(row[2])
        for row in wb["Table 2"].iter_rows(min_row=5, values_only=True):
            if row[1] and row[1] != "State":
                est[(row[1], 2023)] = int(row[2])
                first[(row[1], 2023)] = int(row[5])
        self.sdc, self.sdc_first = est, first

    def _read_acs(self):
        self.below = {}
        with open(self.path("acs"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["summary_level"] == "060" and r["table_line"] == "B17001_002":
                    self.below[self.geoid[r["geo_id"].replace("0600000US", "")]] = int(r["estimate"])

    @staticmethod
    def dss_key(name):
        s = name.upper()
        for a, b in (("EAST ", "E "), ("NORTH ", "N "), ("WEST ", "W "), ("LOWER ", "LWR "), ("UPPER ", "UPR "),
                     (" CENTER", " CTR"), (" HILL", "-HILL")):
            s = s.replace(a, b)
        return s

    def _read_snap(self):
        key = {self.dss_key(t): t for t in self.towns}
        self.snap = {}
        with open(self.path("snap"), encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="|"):
                t = key.get(r["TOWN"])
                if t is None:
                    continue
                y, m = int(r["BENEFIT_MONTH"][:4]), int(r["BENEFIT_MONTH"][4:])
                self.snap[(t, y, m)] = (int(r["HOUSEHOLDS"]), int(r["RECIPIENTS"]))
        self.snap_unmatched = sorted(set(self.towns) - {k[0] for k in self.snap})

    def snap_year(self, town, y, field=1):
        return sum(self.snap[(town, y, m)][field] for m in range(1, 13)) / 12.0

    # ----------------------------------------------------------------------------------- the asks' files
    def asks_inputs(self):
        def rows(k):
            with open(self.path(k), encoding="utf-8", newline="") as f:
                rd = csv.reader(f)
                next(rd)
                return [r for r in rd]
        ext, aud, conv = rows("extract"), rows("audit"), rows("conversion")
        wb = openpyxl.load_workbook(self.path("closeout"), data_only=True)
        bal = {}
        for row in wb["FY2026 closeout"].iter_rows(min_row=5, values_only=True):
            if row[2]:
                award = int(round(row[3] * 1000))
                bal[row[2]] = dict(award=award, spent=int(row[4]), unspent=int(row[5]))
        return ext, aud, conv, bal
