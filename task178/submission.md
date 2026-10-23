## Tags

**Domain:** Quantitative Finance (volatility and derivatives pricing).  
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Price the 2027 one-year dollar options at 12 per cent.** The closing rate's volatility over the 2024 to 2026 sessions without the Banco Central's spot operations is between 11 and 12 per cent, so 12 is the lowest whole-per-cent setting that covers it and 11 falls short. Not the recorded 6.9 per cent (a setting of 7), which the Bank's operations held down. Not 8 or 9, which put the Bank's trades back at an impact read from the hour's move on the market's net flow (7.4 per cent) or on customer flow alone (8.9 per cent): the Bank traded against each hour's own move, so both regressions read the market's depth too low.

## 2. Critical Components

1. The market's price impact of net dollar flow, with customer flow as the instrument, is **between 0.5 and 0.6 per cent** of the rate per 100 million dollars.
2. The 2024 to 2026 closing-rate volatility without the Bank's operations is **between 11 and 12 per cent**.
3. The settings of 8 to 11 per cent fall short of it; 12 and 13 per cent cover it.

## 3. Step-by-Step Solution

1. Summed the reports of record in dealer_customer_flows_hourly_2024-2026.csv (the last report received for each dealer and hour, Financiera Tres Valles' reports after 30 June 2025 left out per bct_reporting_dealers.csv) into the customers' net dollar purchases each hour.
2. Dropped the ANULADA rows of bct_spot_operations_2024-2026.csv and netted VENTA less COMPRA into the Bank's net dollar sales each hour.
3. Took each hour's log change of the mid in platform_hourly_mid_2024-2026.csv, joining an hour to the next where its closing mark is missing.
4. Regressed the hour's change on the market's net flow (customers less the Bank) with customer flow as the instrument, because the Bank traded against each hour's own move: between 0.5 and 0.6 per cent per 100 million dollars.
5. Added each session's Bank net sales times that impact to the closing rate's daily log change and took the root mean square at 252 sessions (cordillera_fx_options_pricing_policy_2027.pdf, section 2): between 11 and 12 per cent, rounded up to 12.
6. Hedging cost: grouped the CONFIRMED executions in platform_confirmations_cordillera_2026.csv into orders by trader, side and millisecond time stamp (an order that takes several resting quotes shows one execution per quote), banded each order by its total size, and dollar-weighted each execution's price less the arrival mid, signed by side, by 2026 quarter.
7. Forwards due: in cordillera_fx_forward_deals_2025-2026.xlsx, dropped ANULADA, EUR/TQP and Treasury-desk deals, netted each WINDOW deal by the outrights booked against it (same client, side and forward rate, maturing inside the window), and summed the 2027 maturities by quarter and segment from cordillera_corporate_client_register.csv.
8. Priced the 2027 one-year options at 12 per cent, the lowest setting at or above the expected volatility.

## 4. Deliverable Answers

### usd_options_vol_2027.xlsx

1. Pricing volatility for 2027 one-year options: 12 per cent.
2. Grid settings against the expected 2027 volatility:
   - 8 per cent: falls short
   - 9 per cent: falls short
   - 10 per cent: falls short
   - 11 per cent: falls short
   - 12 per cent: covers
   - 13 per cent: covers
3. 2026 hedging cost per dollar against the arrival mid, dollar-weighted, in pesos:
   - Q1 2026: under 1 million 1.3; 1 to 3 million 1.5; 3 to 10 million 2.1; 10 million and over 3.5
   - Q2 2026: under 1 million 1.0; 1 to 3 million 1.5; 3 to 10 million 2.7; 10 million and over 8.2
   - Q3 2026: under 1 million 0.8; 1 to 3 million 0.9; 3 to 10 million 1.3; 10 million and over 3.9
   - Q4 2026: under 1 million 1.0; 1 to 3 million 1.4; 3 to 10 million 2.6; 10 million and over 10.1
4. Client dollar forwards falling due in 2027, in millions of dollars:
   - Q1 2027: exporters sell 69.2; importers buy 97.5
   - Q2 2027: exporters sell 39.4; importers buy 49.1
   - Q3 2027: exporters sell 42.3; importers buy 29.1
   - Q4 2027: exporters sell 22.4; importers buy 28.4

### free_float_vol_2027.png

5. Bars for the grid settings of 8 to 13 per cent with 12 per cent highlighted, against a band for the expected 2027 volatility between 11 and 12 per cent and a dashed line at the recorded 6.9 per cent.
