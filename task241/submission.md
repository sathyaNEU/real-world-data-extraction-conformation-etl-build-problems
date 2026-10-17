# task241 submission

## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: delayed-mode calibration of profiling-float salinity against ship CTD reference data).
**Analytical objective:** Data Quality Monitoring & Alerting (which floats of an observing array have their year's salinity record adjusted in the delayed-mode release, with the reference coverage and the real-time delivery record the release report carries).

## 1. Final Recommendation

**Adjust the 2027 salinity of six of the 24 floats in the delayed-mode release: 1990001, 1990004, 1990005 and 1990008, which read fresh (offsets -0.022, -0.020, -0.027, -0.030), and 1990007 and 1990012, which read salty (+0.021, +0.020). The other 18 floats' 2027 salinity goes out as measured.**

Each adjusted float reads 0.020 or more from the water it sampled, and the largest offset among the other floats is 0.003, against the tolerance of 0.010. Below the Mediterranean water the deep layer's temperature identifies the water, but in 2027 the layer sat deeper than in the reference years and heaved with eddies, and on a given potential-temperature level the water freshens westward across the basin. So each float's salinity is compared with the reference water of the same potential temperature at the profile's own position. Differencing at fixed pressure, against the reference casts' mean or the nearest casts, adjusts 13 to 17 floats depending on the levels and casts used, at least seven of them floats whose sensors read true, because water at a fixed pressure in 2027 was not the water the casts sampled there. Comparing on potential-temperature levels against the basin's pooled reference adjusts 10 to 14, at least four of them clean floats on the basin's eastern and western sides. Measuring each float against its own first profiles finds only the four floats that drifted during the year and misses 1990007 and 1990012, whose sensors were off from deployment.

## 2. Critical Components

1. The four floats reading fresh: 1990001 **-0.022**; 1990004 **-0.020**; 1990005 **-0.027**; 1990008 **-0.030**.
2. The two floats reading salty: 1990007 **+0.021**; 1990012 **+0.020**.
3. The largest offset among the other 18 floats is **-0.003** (1990016).

Offsets are in practical salinity and are accepted within 0.003 of these values: any mapping of the reference water to the profile's position on potential-temperature levels (nearest casts, casts within a few degrees, a fit in position) reproduces each offset to within 0.003, the third decimal moving with the mapping, and every such mapping adjusts the same six floats.

## 3. Step-by-Step Solution

1. Took the array's 24 floats from ibfa_float_register.csv and their 2027 ascending profiles from ibfa_profiles_2027.csv: 878 profiles, 44 of them received twice (file_version 1 broke off part way; file_version 2 carries every level, and is the one used). The partner float 1990731, decoded beside the array, and the descending profiles of floats 1990010, 1990013, 1990015, 1990018 are left out (ioa_dmqc_2027_release_thread.eml).
2. Joined the levels in ibfa_profile_levels_2027.csv and kept the good values, flag 1 or 2 in pressure, temperature and salinity, between 1,400 and 1,900 dbar: 8,794 values in 878 profiles.
3. Built the reference water from both sources named in ioa_reference_data_note.docx: the institute's archive (ioa_ctd_archive_stations.csv and ioa_ctd_archive_levels.csv, 183 casts; the 35 casts of the 2015 and 2016 cruises in IPTS-68, divided by 1.00024 for ITS-90) and the RHD extract (rhd_extract_iberian_basin_stations.csv and rhd_extract_iberian_basin_levels.csv, 190 stations; depths taken to pressure by Saunders 1981).
4. Computed potential temperature referred to the surface (EOS-80) for every float level and every reference level.
5. Fitted the reference salinity between 1,300 and 2,050 dbar on potential temperature theta and position: S = a + b theta + c theta^2 + (theta - 3.5)(d longitude + e latitude), least squares. The reference levels' potential temperatures (4.03 to 8.29) span every float level's used (4.32 to 7.53), so the fit is read only inside its own range.
6. For each profile, the mean over its good layer values of the float's salinity less the fitted reference salinity at the value's potential temperature and the profile's position; for each float, the mean over its 2027 ascending profiles (ioa_dmqc_2027_release_thread.eml).
7. Applied the tolerance in ioa_dmqc_2027_release_thread.eml, an offset more than 0.010 in magnitude: six floats are adjusted.
8. Reference casts reaching 2,000 dbar: an archive cast counts when its max_pres is 2,000 or more; an RHD station when its deepest depth, taken to pressure, is 2,000 dbar or more. 119 RHD stations are the institute's own casts under RHD ids (time within 15 minutes and position within 0.02 degree of an archive cast) and count once; casts the archive holds twice at one station a few hours apart are two casts. Counted by the year of the cast.
9. Delivery record: each of the array's ascending profiles, by the month the float surfaced, the end of the ascent (ascent_end in ibfa_cycle_technical_2027.csv; the model K floats' juld is the start of the ascent, about six hours earlier). Its time of arrival is the receipt of the file carrying every level in ioa_dac_receipt_log_2027.csv, the server's Lisbon time taken to UTC. Counted when that is within 24 hours of surfacing: 781 of 878 profiles in 2027.

## 4. Deliverable Answers

### ioa_dmqc_salinity_2027.xlsx

1. Each float's 2027 offset (practical salinity, three decimals; accepted within 0.003, the third decimal moving with the mapping of the reference to the profile's position) and decision:
   - 1990001: -0.022, adjust
   - 1990002: 0.000, release as measured
   - 1990003: -0.001, release as measured
   - 1990004: -0.020, adjust
   - 1990005: -0.027, adjust
   - 1990006: -0.001, release as measured
   - 1990007: +0.021, adjust
   - 1990008: -0.030, adjust
   - 1990009: 0.000, release as measured
   - 1990010: +0.001, release as measured
   - 1990011: 0.000, release as measured
   - 1990012: +0.020, adjust
   - 1990013: 0.000, release as measured
   - 1990014: -0.001, release as measured
   - 1990015: +0.001, release as measured
   - 1990016: -0.003, release as measured
   - 1990017: +0.001, release as measured
   - 1990018: 0.000, release as measured
   - 1990019: -0.001, release as measured
   - 1990020: 0.000, release as measured
   - 1990021: +0.001, release as measured
   - 1990022: -0.001, release as measured
   - 1990023: +0.002, release as measured
   - 1990024: 0.000, release as measured
2. Reference casts reaching 2,000 dbar, by year: 2015 21; 2016 17; 2017 19; 2018 24; 2019 19; 2020 13; 2021 21; 2022 17; 2023 22; 2024 23; 2025 17.
3. The array's ascending profiles that reached the data centre in full within 24 hours of the float surfacing, by the month the float surfaced: January 69; February 58; March 62; April 67; May 65; June 67; July 63; August 66; September 63; October 69; November 67; December 65.

### ioa_dmqc_offsets_2027.png

4. One bar per float with its 2027 offset, the tolerance band from -0.010 to +0.010 shaded, and the six adjusted floats (1990001, 1990004, 1990005, 1990007, 1990008, 1990012) marked.
