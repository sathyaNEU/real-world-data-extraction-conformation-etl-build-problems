# Kelvale groundwater monitoring network: notes on the October 2026 extract

Environment, Kelvale Mine. Erika Martin, 9 October 2026.

These notes go with the network extract taken on Friday 9 October 2026 for the MG-02 assessments. Water levels run
to 30 September 2026; the loggers were downloaded between 1 and 6 October.

## The network

27 bores: the 18 landholder bores in the register, three state reference bores outside the EIS predicted drawdown
(read by our field team under an arrangement with the department) and six mine monitoring bores on the pit
perimeter. The consultant read the network for the EIS baseline every quarter from March 2012 to June 2014. The field
team has read it monthly since July 2014, and the landholder bores every fortnight since 10 August 2026. Ten bores
have had pressure loggers since May 2015.

Pit dewatering began on 4 July 2022 from the pit sumps; the advance dewatering bores AD01 to AD04 came on from March
2023.

## Bores and their names

Every bore has the company's code (KV-LB for landholder bores, KV-RF for the reference bores, KV-MB for the mine's
bores) and its state registered number. The field sheets use the code; the consultant's EIS sheets used the
registered number. Landholders use their own names for their bores. The register (`landholder_bore_register.xlsx`) holds all three, with
each bore's aquifer, construction and baseline assessment, the measuring point history and the other network bores.

## Manual dips (`water_level_dips_2012-2026.csv`)

One row per entry keyed from the field sheets, in the order keyed.

| Field | Meaning |
|---|---|
| `entry_no` | Database entry number. |
| `reading_date`, `reading_time` | Date and time of the reading, Queensland time (AEST, no daylight saving). |
| `site` | The bore as written on the field sheet. |
| `dtw` | Depth to water below the measuring point. |
| `units` | `m`; `ft` for the consultant's EIS rounds (March 2012 to June 2014), which were read in feet. |
| `remarks` | The officer's notes from the field sheet (access, headworks, pump, weather), as written. |
| `officer` | Initials of the officer who read the bore (IVH is the EIS consultant). |

A dip is measured from the measuring point in force on the day. Two bores have had their headworks rebuilt since the
baseline assessments and the new measuring point surveyed; the register's measuring point sheet has the dates.

## Loggers

`logger_pressure_2015-2026.parquet` holds the hourly records of every logger: `logger_serial`, `timestamp_utc` (UTC), `pressure_kpa` (absolute
pressure at the sensor, kPa) and `temperature_c`. The loggers are unvented, so each reading includes air pressure.
`barometric_logger_2015-2026.csv` is the site barometric logger, hourly, also in UTC. `logger_installations.csv` gives each logger's bore, the times it went
in and came out (Queensland time) and its sensor depth below the measuring point.

The water column above the sensor is the logger pressure less the barometric pressure for the same hour, divided by
9.80665 kPa per metre of water. The level (m AHD) is the measuring point elevation less the sensor depth plus the
water column. Each logger is checked against a manual dip when it is downloaded; the check dips are in the dips file.

## Other files

- `daily_climate_1990-2026.csv`: gridded climate data for the point nearest the pit: daily rainfall (24 hours to 9 am on the date) and
  Morton's areal potential evapotranspiration (mm), with maximum and minimum temperature, from 1 January 1990 to 30
  September 2026.
- `pit_dewatering_2022-2026.csv`: the daily metered volume from each dewatering source (ML).
- `groundwater_quality_2012-2026.csv`: field and laboratory water quality results by sampling round.
- `landholder_contact_log_2026.xlsx`: the environment team's log of contacts with neighbours in 2026.
