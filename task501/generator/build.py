"""task501 build: simulate, observe, write the pack and its documents, scrub the containers, stamp the times.
Run from anywhere: python3 task501/generator/build.py. Then checks.py, golden.py and verify.py."""
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim
import observe as O
import pack as PK
import docs
import solve

REPO = os.path.dirname(os.path.dirname(HERE))
SCRUB = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")


DISTRACTORS = [PK.AUDITED, PK.NAVREG, PK.HOLDINGS]
FILE_DATES = {PK.LEDGER: "2027-01-05", PK.REGISTER: "2026-12-31", PK.FXFILE: "2026-12-31", PK.CUSTODY: "2027-01-04",
              PK.AUDITED: "2026-06-18", PK.NAVREG: "2027-01-04", PK.HOLDINGS: "2027-01-05", docs.DIRECTIVE: "2026-09-24",
              docs.TERMSHEET: "2026-12-09", docs.MINUTES: "2026-09-24", docs.MAIL: "2027-01-06", docs.NOTES: "2027-01-05",
              docs.MANIFEST: "2027-01-05", docs.REPORT: "2025-09-25"}
WHAT = {PK.LEDGER: "notice ledger, one row per line of each capital call and distribution notice (2015 to 2026)",
        PK.REGISTER: "fund register at 31 December 2026 with contract dates and terms",
        PK.FXFILE: "custodian end-of-day reference rates against the Swiss franc",
        PK.CUSTODY: "custodian statement of the programme account, 2025 and 2026",
        PK.AUDITED: "capital accounts from the funds' audited financial statements, FY2021 to FY2025",
        PK.NAVREG: "NAV register of manager statements received",
        PK.HOLDINGS: "look-through holdings from the managers' quarterly schedules of investments",
        docs.DIRECTIVE: "liquidity directive for the private-markets programme, version 5 (working translation)",
        docs.TERMSHEET: "lender's indicative term sheet for the 2027 standby facility",
        docs.MINUTES: "extract from the minutes of the board of trustees, 24 September 2026",
        docs.MAIL: "mail export: the year-end extract and the facility election",
        docs.NOTES: "field notes to the year-end extract",
        docs.MANIFEST: "extract log (manifest) of the year-end extract",
        docs.REPORT: "semi-annual programme report, first half of 2025"}


def write_metadata(counts):
    rows = {PK.LEDGER: counts["ledger"], PK.FXFILE: counts["fx"], PK.CUSTODY: counts["custody"], PK.AUDITED: counts["audited"],
            PK.NAVREG: counts["nav"], PK.HOLDINGS: counts["holdings"]}
    files = sorted(os.listdir(PK.T))
    used_big = max((f for f in rows if f not in DISTRACTORS), key=lambda f: rows[f])
    meta = {
        "task": "task501",
        "title": "The standby facility a Swiss pension foundation should elect for its private-markets programme's 2027 capital calls, "
                 "with the fees at the two nearest amounts and the 2026 distributions received by strategy and quarter",
        "domain": "Quantitative Finance",
        "subdomain": "liquidity, funding and balance-sheet risk (a private-markets programme's capital-call forecast against a standby facility)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "07 (a dial setting): the facility amount from the menu, with the fees at it and at the next amount down, and every "
                        "strategy's 2026 distributions received in each quarter and for the year",
        "as_of": "2027-01-06",
        "deliverables": ["facility_election_2027.docx", "distributions_received_2026.xlsx"],
        "stated_inputs": ["35"] + [str(a) for a in W.MENU] + ["0.30", "0.15"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({f.rsplit(".", 1)[-1] for f in files}),
                        "largest_file": used_big, "largest_file_rows": rows[used_big]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task501/generator/build.py (seeded, deterministic) around a fictional Swiss "
                               "pension foundation (Pensionskasse Werdinsel), its private-markets programme, fund managers, funds, "
                               "portfolio companies and lender (Privatbank Lindenhof AG). No real person, fund, company or record is "
                               "depicted; exchange-rate paths are synthetic.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task501/generator/build.py",
        "files": [{"path": f, "format": f.rsplit(".", 1)[-1], "bytes": os.path.getsize(os.path.join(PK.T, f)), "rows": rows.get(f),
                   "what": WHAT[f], "source": "Constructed for this task (fictional organisation; no third-party data)",
                   "date": FILE_DATES[f], "license": "CC0-1.0 (original work, constructed for this task)"} for f in files],
    }
    with open(os.path.join(os.path.dirname(HERE), "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def main():
    t0 = time.time()
    if os.path.isdir(PK.T):
        shutil.rmtree(PK.T)
    os.makedirs(PK.T)
    funds, fx_rows = sim.simulate()
    fx = sim.FX(fx_rows)
    obs = O.observe(funds, fx)
    cust = O.custodian_postings(funds, fx, obs["events"])
    counts = dict(ledger=PK.write_ledger(obs), fx=PK.write_fx(fx_rows), custody=PK.write_custody(cust),
                  audited=PK.write_audited(funds, PK.audited_cells(funds)), nav=PK.write_nav_register(funds, fx),
                  holdings=PK.write_holdings(funds))
    PK.write_register(funds)
    pk = solve.Pack()
    import pandas as pd
    nav = pd.read_csv(os.path.join(PK.T, PK.NAVREG))
    q2 = set(nav[nav["period_end"] == "2026-06-30"]["fund_id"])
    q3 = set(nav[nav["period_end"] == "2026-09-30"]["fund_id"])
    info = dict(q3_missing=len(q2 - q3), n_funds=len(funds))
    docs.write_directive()
    docs.write_term_sheet()
    docs.write_minutes(solve.september_event(pk))
    docs.write_mail(info)
    docs.write_report(solve.h1_2025_bridge(pk), solve.half_years_net_out(pk))
    docs.write_field_notes(counts)
    subprocess.run([sys.executable, SCRUB, PK.T, "--apply", "--producer", W.ORG, "--stamp", "2027-01-05", "--floor", "2025-01-01",
                    "--ceiling", "2027-01-05"], check=True, capture_output=True)
    for f in (PK.REGISTER, PK.AUDITED, docs.DIRECTIVE):
        PK.fix_zip_times(os.path.join(PK.T, f), core=PK.CORE_TIMES[f])
    for f, (cr, md, prod) in PK.PDF_INFO.items():
        PK.fix_pdf_info(os.path.join(PK.T, f), cr, md, prod)
    docs.write_manifest(counts, info)
    stamp = time.mktime((2027, 1, 6, 15, 10, 0, 0, 0, -1))   # the pack as assembled after the last message of 6 January
    for f in os.listdir(PK.T):
        os.utime(os.path.join(PK.T, f), (stamp, stamp))
    write_metadata(counts)
    record = dict(counts=counts, info=info, boundary=obs["boundary"], withdrawn_calls=obs["withdrawn_calls"],
                  withdrawn_dist=obs["withdrawn_dist"], in_specie=obs["in_specie"], world_2027=sim.world_calls_2027(funds, fx))
    with open(os.path.join(HERE, "build_record.json"), "w") as fh:
        json.dump(record, fh, indent=1, default=str)
    print("built %d files in %.1fs: %s" % (len(os.listdir(PK.T)), time.time() - t0, counts))


if __name__ == "__main__":
    main()
