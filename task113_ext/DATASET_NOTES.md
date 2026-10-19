# task113_ext dataset notes

An input dataset only, built at the author's request: no question, draw, ladder, stump, golden, submission or
fingerprint card, and nothing planted. It replaces the earlier task113_ext (a pull of New York Fed and Treasury
publications) with a complete refresh for the domain, fully synthetic.

- **Domain:** Quantitative Finance. Anchored on `strategy-backtesting-evaluation` (Forecasting); the same store
  carries what `event-study`, `factor-return-attribution`, `market-microstructure-execution-cost` and
  `portfolio-construction-risk` work needs. The objective is fixed at the draw.
- **World:** Pellbrook Capital's systematic equity research store for US small and mid cap common stock, January
  2018 to September 2026: 142 securities (120 listed before the store begins, 20 IPOs, 2 spin-offs), on the real
  NYSE calendar (holidays, the closures of 5 December 2018 and 9 January 2025, early closes). Vendors: Merriden
  Market Data (prices, security master, corporate actions, delistings), Ledgerpoint Financial Data (point-in-time
  fundamentals, earnings calendar), Northcote Indices (the benchmark), the exchanges' short interest files, the
  custodian Harrowgate Trust (sweep rate), the firm's OMS and its broker Kelloway Securities (the live book since
  July 2023). Every company, vendor, index, broker and custodian is fictional, and no file names a person.
- **Spine:** Merriden's legacy end-of-day file, 186,430 rows; the current platform's Parquet adds 91,128, of which
  7,742 fall in the overlap quarter both files hold. 19 files in 8 formats (csv, parquet, json, jsonl, xlsx, txt,
  pdf, md); row counts and as-of dates in `metadata.json` and the bundle's README. `target.zip` sha256
  5c73f284435870a3, 11.6 MB.

## Layer 1, the systems' own mess

- Two price deliveries: the legacy CSV ends 29 December 2023; the current Parquet starts 2 October 2023, so a
  quarter overlaps, with the late close and volume corrections only in the current file. Shares in thousands
  against units, numeric exchange codes against MICs, price factors anchored at different dates.
- Identifiers: Merriden's security_id is permanent; tickers change and two are reused by later listings; CUSIPs
  change on reverse splits and rebrands. Ledgerpoint keys on its own lp_id, Northcote on CUSIP, short interest on
  symbol alone, the OMS on symbol and CUSIP, the broker on symbol.
- Corporate actions as a revision log (NEW, AMEND, CANCEL, COMPLETE): dividends declared and withdrawn in March
  2020, amended pay dates, raised and terminated deals, dividends declared for ex-dates after the store's last day,
  record dates moving with the one-day settlement cycle from 28 May 2024.
- Fundamentals point in time: a press release, a filing and sometimes an amendment for each period; a fourth
  quarter's own figures only in its press release, the 10-K carrying the fiscal year; cash flows year to date;
  thousands or millions by company; per-share figures as reported before later splits; June, September and March
  fiscal years, and 52-53 week retailers named for the year they begin.
- Clocks: the earnings calendar and the OMS in UTC, the broker in New York time, the sweep on calendar days,
  settlement on business days that skip bank holidays.
- Short interest stacked as published, with revisions; the broker's busts and corrections; partial fills; OTC prices
  missing for some delistings.

## What the data's own structure offers a draw

Delisted names with their delisting returns, knowledge dates against period ends, release timing before the open
and after the close, splits under two factor anchors, the benchmark's reconstitutions and caps, short interest's
publication lag, the live book against the store's prices and the commission change of March 2025. None of these
is placed to be caught; the draw takes its pitfall from whichever the question it files turns on.

## Checks

`generator/checks.py` reads only `target/` and proves the files agree: every total and price return recomputes
from the closes and the corporate actions feed, every price factor steps by its split's ratio, the overlap quarter
reconciles, every price row's ticker and exchange is the master's spell that day, delisting returns recompute,
diluted EPS ties to net income and shares in each row's units, every press release matches its confirmed calendar
event, the benchmark's daily levels recompute from its constituents, and the short interest, sweep and executions
tie out (44 checks). `generator/build_pack.py` runs them, builds twice byte for byte and cuts `target.zip`.

## Tried and rejected

- 2026-10-19: the earlier task113_ext's pull of New York Fed and Treasury publications: the four hosts are denied
  by this environment's network policy, and the author asked for a complete refresh with no government dataset.
- 2026-10-19: a money-market anomaly world like the earlier bundle's: the client taxonomy has no anomaly detection
  task type in Quantitative Finance.
- 2026-10-19: first calibration: the benchmark rose about fourfold over the window (idiosyncratic drift compounded
  by cap weighting and reconstitution) and fell 58 per cent in one year (a few runaway names); idiosyncratic
  returns centred on zero, sector factors demeaned, the market's yearly totals set so the benchmark reads like the
  period, and the index banded at $300 million to $7.5 billion and capped at 4 per cent.
- 2026-10-19: the live book traded names on days the vendor shows no trade in them; such orders now wait for the
  next rebalance.
