"""Write the evidence pack under target/ from a simulated World."""
import csv
import datetime as dt
import io
import os

import numpy as np

import world as W
import docs as D

SUB_COLS = ["ACCESSION_NUMBER", "FILING_DATE", "SUBMISSIONTYPE", "CIK", "PERIODOFREPORT"]
COV_COLS = ["ACCESSION_NUMBER", "REPORTCALENDARORQUARTER", "ISAMENDMENT", "AMENDMENTNO", "AMENDMENTTYPE",
            "CONFDENIEDEXPIRED", "DATEDENIEDEXPIRED", "DATEREPORTED", "REASONFORNONCONFIDENTIALITY",
            "FILINGMANAGER_NAME", "FILINGMANAGER_STREET1", "FILINGMANAGER_STREET2", "FILINGMANAGER_CITY",
            "FILINGMANAGER_STATEORCOUNTRY", "FILINGMANAGER_ZIPCODE", "REPORTTYPE", "FORM13FFILENUMBER",
            "CRDNUMBER", "SECFILENUMBER", "PROVIDEINFOFORINSTRUCTION5", "ADDITIONALINFORMATION"]
INF_COLS = ["ACCESSION_NUMBER", "INFOTABLE_SK", "NAMEOFISSUER", "TITLEOFCLASS", "CUSIP", "VALUE", "SSHPRNAMT",
            "SSHPRNAMTTYPE", "PUTCALL", "INVESTMENTDISCRETION", "OTHERMANAGER", "VOTING_AUTH_SOLE",
            "VOTING_AUTH_SHARED", "VOTING_AUTH_NONE"]


def _w_tsv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join("" if r.get(c) is None else str(r.get(c)) for c in cols) + "\n")


def write_drops(wd, target):
    M = wd.M
    rz = W.rng("pack-zip")
    zips = {m["mid"]: f"{int(rz.integers(10001, 99950)):05d}" for m in wd.mgrs}
    streets = {m["mid"]: f"{int(rz.integers(1, 2400))} {rz.choice(['MAIN ST', 'PARK AVENUE', 'BROAD ST', 'MARKET ST', 'STATE ST', 'WASHINGTON BLVD', 'ELM ST', 'LEXINGTON AVE', 'COMMERCE DR'])}" for m in wd.mgrs}
    crd = {m["mid"]: ("" if m["type"] in ("banktrust", "instit") else str(int(rz.integers(100000, 330000)))) for m in wd.mgrs}
    out = {}
    for folder, d0, d1 in W.DROPS:
        os.makedirs(os.path.join(target, folder), exist_ok=True)
        fl = [f for f in wd.filings if d0 <= f.date <= d1]
        fl.sort(key=lambda f: (f.date, f.acc))
        sub, cov, inf = [], [], []
        sk = int(rz.integers(40_000_000, 60_000_000))
        for f in fl:
            m = M[f.mid]
            sub.append(dict(ACCESSION_NUMBER=f.acc, FILING_DATE=W.sec_date(f.date), SUBMISSIONTYPE=f.form,
                            CIK=m["cik"], PERIODOFREPORT=W.sec_date(W.PERIODS[f.q])))
            cov.append(dict(ACCESSION_NUMBER=f.acc, REPORTCALENDARORQUARTER=W.sec_date(W.PERIODS[f.q]),
                            ISAMENDMENT="Y" if f.amend_no else "N",
                            AMENDMENTNO=f.amend_no if f.amend_no else "",
                            AMENDMENTTYPE=f.amend_type,
                            CONFDENIEDEXPIRED="", DATEDENIEDEXPIRED="", DATEREPORTED="",
                            REASONFORNONCONFIDENTIALITY="",
                            FILINGMANAGER_NAME=m["name"], FILINGMANAGER_STREET1=streets[f.mid],
                            FILINGMANAGER_STREET2="SUITE " + str(100 + int(rz.integers(0, 40)) * 10) if rz.random() < 0.4 else "",
                            FILINGMANAGER_CITY=m["city"], FILINGMANAGER_STATEORCOUNTRY=m["state"],
                            FILINGMANAGER_ZIPCODE=zips[f.mid], REPORTTYPE=f.reporttype,
                            FORM13FFILENUMBER=m["fileno"], CRDNUMBER=crd[f.mid], SECFILENUMBER="",
                            PROVIDEINFOFORINSTRUCTION5="N",
                            ADDITIONALINFORMATION=_addl(f)))
            for ln in f.lines:
                sk += 1
                sole = ln["shares"] if ln["disc"] == "SOLE" else 0
                none = 0
                shared = ln["shares"] - sole
                if m["type"] in ("ria", "banktrust") and ln["disc"] == "SOLE" and not ln["putcall"]:
                    none = int(ln["shares"] * 0.3) if rz.random() < 0.3 else 0
                    sole -= none
                if ln["putcall"]:
                    sole = shared = none = 0
                inf.append(dict(ACCESSION_NUMBER=f.acc, INFOTABLE_SK=sk, NAMEOFISSUER=ln["name"],
                                TITLEOFCLASS=ln["title"], CUSIP=ln["cusip"], VALUE=ln["value"],
                                SSHPRNAMT=ln["shares"], SSHPRNAMTTYPE=ln["sht"], PUTCALL=ln["putcall"],
                                INVESTMENTDISCRETION=ln["disc"], OTHERMANAGER=ln["othmgr"],
                                VOTING_AUTH_SOLE=sole, VOTING_AUTH_SHARED=shared, VOTING_AUTH_NONE=none))
        _w_tsv(os.path.join(target, folder, "SUBMISSION.tsv"), SUB_COLS, sub)
        _w_tsv(os.path.join(target, folder, "COVERPAGE.tsv"), COV_COLS, cov)
        _w_tsv(os.path.join(target, folder, "INFOTABLE.tsv"), INF_COLS, inf)
        out[folder] = dict(sub=len(sub), cov=len(cov), inf=len(inf))
    return out


def _addl(f):
    if f.amend_type == "NEW HOLDINGS":
        return "This amendment reports holdings for which confidential treatment was previously requested and has expired."
    if f.amend_type == "RESTATEMENT":
        return "Amendment restates the report in its entirety to correct share amounts."
    return ""


def write_fsds(wd, target):
    """Cover-page share counts in the FSDS sub/num layout, for the 10-Q and 10-K filings our
    security master pulls (issuers on the watchlist and the wider coverage list)."""
    folder = os.path.join(target, "fsds_cover_extract")
    os.makedirs(folder, exist_ok=True)
    rs = W.rng("fsds")
    sub, num = [], []
    for i in wd.iss:
        cik = i["issuer_cik"]
        # Q2 10-Q, Q3 10-Q, FY 10-K (only those accepted by the extract)
        docs = [("10-Q", dt.date(2022, 6, 30), "Q2", 2022, rs.integers(28, 44), i["S_jul"], 0),
                ("10-Q", dt.date(2022, 9, 30), "Q3", 2022, rs.integers(27, 43), i["S_oct"], 0)]
        kd = int(rs.integers(26, 62))
        if dt.date(2022, 12, 31) + dt.timedelta(days=kd) <= W.EXTRACT_DATE:
            docs.append(("10-K", dt.date(2022, 12, 31), "FY", 2022, kd, i["S_jan"], 1))
        for form, per, fp, fy, lag, shares, _ in docs:
            filed = W.business_day_on_or_after(per + dt.timedelta(days=int(lag)))
            asof = filed - dt.timedelta(days=int(rs.integers(3, 12)))
            seq = int(rs.integers(100, 99000))
            adsh = f"{int(rs.integers(1000000, 1999999)):010d}-{filed.year % 100:02d}-{seq:06d}"
            accepted = f"{filed.isoformat()} {int(rs.integers(6, 21)):02d}:{int(rs.integers(0, 60)):02d}:00.0"
            sub.append(dict(adsh=adsh, cik=cik, name=i["name"], sic=i["sic"], countryba="US", stprba=i["state"],
                            cityba=i["city"], form=form, period=per.strftime("%Y%m%d"), fy=fy, fp=fp,
                            filed=filed.strftime("%Y%m%d"), accepted=accepted, prevrpt=0, nciks=1,
                            afs=i["afs"], wksi=1 if i["afs"] == "1-LAF" else 0, fye="1231"))
            num.append(dict(adsh=adsh, tag="EntityCommonStockSharesOutstanding", version="dei/2022",
                            ddate=asof.strftime("%Y%m%d"), qtrs=0, uom="shares", coreg="", value=f"{shares}.0000", footnote=""))
            if form == "10-K":
                num.append(dict(adsh=adsh, tag="EntityPublicFloat", version="dei/2022", ddate="20220630", qtrs=0,
                                uom="USD", coreg="", value=f"{int(i['S_jul'] * i['P2'] * rs.uniform(0.55, 0.9))}.0000", footnote=""))
    sub_cols = ["adsh", "cik", "name", "sic", "countryba", "stprba", "cityba", "form", "period", "fy", "fp", "filed",
                "accepted", "prevrpt", "nciks", "afs", "wksi", "fye"]
    num_cols = ["adsh", "tag", "version", "ddate", "qtrs", "uom", "coreg", "value", "footnote"]
    sub.sort(key=lambda r: (r["filed"], r["adsh"]))
    num.sort(key=lambda r: (r["adsh"], r["tag"]))
    _w_tsv(os.path.join(folder, "sub.txt"), sub_cols, sub)
    _w_tsv(os.path.join(folder, "num.txt"), num_cols, num)
    return dict(sub=len(sub), num=len(num))


def write_register(wd, target):
    rows = []
    rr = W.rng("register")
    for m in sorted(wd.mgrs, key=lambda m: m["cik"]):
        since = ["2009Q4", "2012Q2", "2014Q1", "2016Q3", "2018Q1", "2019Q4", "2020Q2", "2021Q1"][int(rr.integers(8))]
        if m["mid"] in wd.newq4:
            since = "2022Q4"
        rows.append({"cik": m["cik"], "manager_name": m["disp"], "family": m["family"],
                     "manager_type": m["type_label"], "form13f_file_number": m["fileno"],
                     "hq_state": m["state"], "covered_since": since,
                     "status": "inactive" if m["mid"] in wd.attrit else "active"})
    path = os.path.join(target, "manager_register.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return len(rows)


def write_all(wd, target):
    os.makedirs(target, exist_ok=True)
    counts = {}
    counts["drops"] = write_drops(wd, target)
    counts["fsds"] = write_fsds(wd, target)
    counts["register"] = write_register(wd, target)
    D.write_docs(wd, target)
    return counts
