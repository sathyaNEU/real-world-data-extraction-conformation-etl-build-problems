# task500 · Fiscal 2026 lodging tax: the change the variance statement names

## Tags

**Domain:** Economics (public finance: a state lodging tax's fiscal 2026 shortfall against the adopted forecast, put on one of the year's changes in the revenue variance statement).
**Analytical objective:** Root-Cause Analysis (naming the change that drove the shortfall, with the rival changes measured and ruled out on the office's standing procedure).

## 1. Final Recommendation

**The fiscal 2026 variance statement should name the long-stay exemption, which reduced fiscal 2026 lodging tax by $3,235 thousand.**

The convention center closure is next at $2,108 thousand. Not the closure: downtown hotels fell furthest, but under the standing procedure their reference hotels fell nearly as far over the same months. Not the county option cut, measured at the old and new rates. Not facilitator collection: host returns stopped because the facilitators began filing for them, and the two together rose.

## 2. Critical Components

1. The standing procedure reproduces **78 of 78** reference figures in Appendix B of the fiscal 2024 and 2025 certified statements
2. Long-stay exemption effect on fiscal 2026 tax: **-3,235 thousand**
3. Convention center closure effect on fiscal 2026 tax: **-2,108 thousand**
4. Shortfall against the adopted forecast: **22,001 thousand**

## 3. Step-by-Step Solution

1. Built monthly taxable receipts and tax by filer from lodging_tax_returns_fy2023-fy2026.csv with class, region and county from lodging_filer_register_2026-08.csv: fiscal 2026 tax due is 223,571 thousand against 245,572 thousand in adopted_forecast_lodging_fy2026.csv, a shortfall of 22,001 thousand.
2. Recovered the reference group that revenue_variance_procedure_rev2023.pdf section 3 leaves open by reproducing variance_statements_appendix_b_fy2024_fy2025.xlsx: filers no change touched, outside the touched filer's region, with a return in each of the 24 months to June, the five closest on the 12 months before the effective month (each month standardised by the filer's own mean and spread), none serving more than two touched filers, larger touched filers matched first, each month grown at the reference median; it reproduces 78 of 78 figures to the dollar.
3. Applied the procedure to the touched filers of the closure, the exemption and the airline cut: -2,108, -3,235 and -586 thousand.
4. Measured the county option cut at the old and new rates (-862 thousand) and facilitator collection on hosts and facilitators together (+123 thousand), per sections 3.4 and 3.5.
5. The part of the shortfall no change accounts for is -15,333 thousand.
6. Walked the statement's total to treasury collections in treasury_lodging_deposits_fy2025-fy2026.csv on deposit dates, penalty and interest out, each return's latest amendment only, refunds netted: 225,148 thousand.
7. Recommendation: the statement names the long-stay exemption at -3,235 thousand.

## 4. Deliverable Answers

### fy2026_lodging_tax_variance.pptx
1. Change the statement names: the long-stay exemption (stays of 30 nights or more), effective January 2026
2. Its effect on fiscal 2026 tax: -3,235 thousand
3. Each change's effect on fiscal 2026 tax, thousands of dollars:
   - Long-stay exemption: -3,235
   - Convention center closure: -2,108
   - County option rate cut in Prairie and Bluff counties: -862
   - Airline hub reduction: -586
   - Marketplace facilitator collection for short-term rentals: +123
4. Part of the shortfall no change accounts for: -15,333 thousand
5. Shortfall against the adopted forecast: 22,001 thousand (adopted forecast 245,572 thousand, tax due on fiscal 2026 returns 223,571 thousand)
6. Reference figures in the last two certified statements reproduced: 78 of 78
7. Waterfall on slide 2 from the adopted forecast (245,572) to the actual (223,571), one bar per change and one for the part no change explains, every bar labelled in thousands, titled that the long-stay exemption cost the most
8. Walk from the statement's total to treasury collections on slide 4, thousands of dollars:
   - Tax due on fiscal 2026 returns: 223,571
   - Less fiscal 2026 periods not deposited by June 30: -21,938
   - Plus earlier periods deposited in fiscal 2026: +23,830
   - Plus amended returns booked in fiscal 2026: +84
   - Less refunds booked in fiscal 2026: -400
   - Treasury collections, fiscal 2026: 225,148

### fy2026_lodging_reference_matches.csv
1. 140 rows, every filer measured one by one (long-stay exemption 60, convention center closure 42, airline hub reduction 38), dollars and cents:
   - LT101184, LX ES, 2026-01 to 2026-06: actual 1,118,968.14, reference 1,847,963.39, tax effect -58,319.63, reference filers LT279228, LT925248, LT883401, LT829307, LT624364
   - LT111174, LX ES, 2026-01 to 2026-06: actual 1,234,207.57, reference 2,103,441.06, tax effect -69,538.68, reference filers LT130192, LT257990, LT727446, LT285222, LT785351
   - LT116724, LX ES, 2026-01 to 2026-06: actual 852,505.18, reference 1,575,000.16, tax effect -57,799.61, reference filers LT764261, LT883401, LT183879, LT568161, LT785092
   - LT119832, LX ES, 2026-01 to 2026-06: actual 777,493.77, reference 1,394,622.62, tax effect -49,370.31, reference filers LT712461, LT895796, LT586809, LT682639, LT613560
   - LT132560, LX ES, 2026-01 to 2026-06: actual 984,168.92, reference 1,741,532.72, tax effect -60,589.11, reference filers LT311233, LT353006, LT799818, LT420642, LT396555
   - LT139960, LX ES, 2026-01 to 2026-06: actual 1,200,216.21, reference 1,916,990.95, tax effect -57,341.98, reference filers LT518544, LT308643, LT873078, LT977825, LT391079
   - LT141292, LX ES, 2026-01 to 2026-06: actual 846,227.00, reference 1,549,805.51, tax effect -56,286.29, reference filers LT528164, LT174555, LT706504, LT261320, LT235790
   - LT149432, LX ES, 2026-01 to 2026-06: actual 799,046.10, reference 1,418,403.49, tax effect -49,548.59, reference filers LT568161, LT847844, LT581222, LT633651, LT117575
   - LT151467, LX ES, 2026-01 to 2026-06: actual 687,516.25, reference 1,183,954.83, tax effect -39,715.09, reference filers LT610748, LT182991, LT321223, LT125382, LT996658
   - LT169745, LX ES, 2026-01 to 2026-06: actual 658,226.98, reference 1,146,102.60, tax effect -39,030.05, reference filers LT743504, LT564017, LT693739, LT510034, LT240896
   - LT181881, LX ES, 2026-01 to 2026-06: actual 1,255,739.65, reference 2,093,484.85, tax effect -67,019.61, reference filers LT671946, LT443619, LT810659, LT128971, LT711388
   - LT184286, LX ES, 2026-01 to 2026-06: actual 1,290,077.32, reference 2,226,887.73, tax effect -74,944.83, reference filers LT552029, LT117242, LT229204, LT120054, LT907599
   - LT189429, LX ES, 2026-01 to 2026-06: actual 1,130,724.90, reference 1,833,611.42, tax effect -56,230.92, reference filers LT119425, LT993143, LT128971, LT552029, LT849953
   - LT189762, LX ES, 2026-01 to 2026-06: actual 1,034,311.56, reference 1,732,085.12, tax effect -55,821.88, reference filers LT785351, LT643900, LT350083, LT631024, LT924545
   - LT202046, LX ES, 2026-01 to 2026-06: actual 897,238.56, reference 1,546,335.72, tax effect -51,927.77, reference filers LT960953, LT850471, LT350083, LT343386, LT672316
   - LT207004, LX ES, 2026-01 to 2026-06: actual 1,302,531.61, reference 2,091,634.07, tax effect -63,128.20, reference filers LT702915, LT285222, LT791900, LT807440, LT913038
   - LT215847, LX ES, 2026-01 to 2026-06: actual 1,302,945.62, reference 2,281,899.05, tax effect -78,316.27, reference filers LT729703, LT162456, LT402179, LT925248, LT204414
   - LT227650, LX ES, 2026-01 to 2026-06: actual 597,665.07, reference 1,071,597.42, tax effect -37,914.60, reference filers LT323628, LT419532, LT579187, LT189466, LT451352
   - LT237936, LX ES, 2026-01 to 2026-06: actual 1,079,492.36, reference 1,806,862.89, tax effect -58,189.64, reference filers LT830084, LT557542, LT824682, LT785092, LT921548
   - LT253476, LX ES, 2026-01 to 2026-06: actual 1,142,915.40, reference 1,841,879.28, tax effect -55,917.11, reference filers LT431853, LT388304, LT261320, LT703322, LT799818
   - LT256103, LX ES, 2026-01 to 2026-06: actual 1,301,593.18, reference 2,225,495.88, tax effect -73,912.21, reference filers LT979194, LT557542, LT977825, LT921548, LT886472
   - LT293362, LX ES, 2026-01 to 2026-06: actual 743,452.62, reference 1,288,438.94, tax effect -43,598.90, reference filers LT509146, LT766148, LT525278, LT850471, LT848769
   - LT296988, LX ES, 2026-01 to 2026-06: actual 1,045,286.07, reference 1,796,585.21, tax effect -60,103.93, reference filers LT119425, LT229204, LT624364, LT111248, LT459270
   - LT323961, LX ES, 2026-01 to 2026-06: actual 874,872.70, reference 1,512,327.31, tax effect -50,996.36, reference filers LT639645, LT830084, LT473959, LT668505, LT183879
   - LT358408, LX ES, 2026-01 to 2026-06: actual 917,469.89, reference 1,497,380.15, tax effect -46,392.82, reference filers LT101850, LT617556, LT351711, LT386232, LT300873
   - LT367325, LX ES, 2026-01 to 2026-06: actual 1,393,502.73, reference 2,378,058.97, tax effect -78,764.50, reference filers LT117242, LT483912, LT130192, LT671946, LT570566
   - LT369286, LX ES, 2026-01 to 2026-06: actual 530,820.51, reference 942,443.11, tax effect -32,929.80, reference filers LT564017, LT226984, LT477955, LT990812, LT436256
   - LT373948, LX ES, 2026-01 to 2026-06: actual 663,772.60, reference 1,203,195.32, tax effect -43,153.82, reference filers LT682639, LT321223, LT115355, LT633170, LT424823
   - LT399034, LX ES, 2026-01 to 2026-06: actual 718,055.29, reference 1,309,801.77, tax effect -47,339.72, reference filers LT586809, LT703248, LT380349, LT424823, LT633170
   - LT412502, LX ES, 2026-01 to 2026-06: actual 989,922.92, reference 1,630,231.27, tax effect -51,224.67, reference filers LT472849, LT641421, LT311233, LT939271, LT711388
   - LT425415, LX ES, 2026-01 to 2026-06: actual 904,193.67, reference 1,560,519.80, tax effect -52,506.09, reference filers LT101850, LT478584, LT117575, LT174555, LT729703
   - LT427080, LX ES, 2026-01 to 2026-06: actual 715,750.41, reference 1,171,924.71, tax effect -36,493.95, reference filers LT379905, LT976345, LT834191, LT389895, LT960953
   - LT455755, LX ES, 2026-01 to 2026-06: actual 779,187.97, reference 1,230,840.22, tax effect -36,132.18, reference filers LT766148, LT991441, LT348307, LT404436, LT626214
   - LT487982, LX ES, 2026-01 to 2026-06: actual 1,120,859.22, reference 1,774,586.97, tax effect -52,298.22, reference filers LT333877, LT924545, LT443619, LT257990, LT810659
   - LT515769, LX ES, 2026-01 to 2026-06: actual 1,171,333.91, reference 1,907,045.71, tax effect -58,856.94, reference filers LT391079, LT703322, LT204414, LT849953, LT220805
   - LT526684, LX ES, 2026-01 to 2026-06: actual 1,231,364.19, reference 1,984,420.41, tax effect -60,244.50, reference filers LT702915, LT145917, LT967428, LT573415, LT423491
   - LT546701, LX ES, 2026-01 to 2026-06: actual 1,045,477.01, reference 1,907,289.94, tax effect -68,945.03, reference filers LT459270, LT308643, LT120054, LT388304, LT886472
   - LT557505, LX ES, 2026-01 to 2026-06: actual 905,192.71, reference 1,514,513.93, tax effect -48,745.70, reference filers LT847844, LT876593, LT380349, LT875113, LT613560
   - LT620812, LX ES, 2026-01 to 2026-06: actual 777,208.30, reference 1,351,382.58, tax effect -45,933.94, reference filers LT361516, LT848769, LT590620, LT624771, LT819835
   - LT621959, LX ES, 2026-01 to 2026-06: actual 781,301.85, reference 1,378,183.77, tax effect -47,750.55, reference filers LT478584, LT996658, LT895796, LT384382, LT300873
   - LT636315, LX ES, 2026-01 to 2026-06: actual 779,472.81, reference 1,408,570.85, tax effect -50,327.85, reference filers LT581222, LT633651, LT628582, LT875113, LT624771
   - LT669985, LX ES, 2026-01 to 2026-06: actual 790,734.67, reference 1,372,331.78, tax effect -46,527.77, reference filers LT712461, LT742246, LT279228, LT824682, LT546257
   - LT695922, LX ES, 2026-01 to 2026-06: actual 1,279,547.25, reference 2,047,625.47, tax effect -61,446.26, reference filers LT643641, LT309235, LT727446, LT517101, LT420642
   - LT698438, LX ES, 2026-01 to 2026-06: actual 707,063.78, reference 1,195,436.18, tax effect -39,069.78, reference filers LT311936, LT115355, LT876593, LT868934, LT473959
   - LT725004, LX ES, 2026-01 to 2026-06: actual 964,221.98, reference 1,764,839.29, tax effect -64,049.39, reference filers LT668505, LT764261, LT979194, LT111248, LT639645
   - LT734291, LX ES, 2026-01 to 2026-06: actual 1,005,043.70, reference 1,726,801.94, tax effect -57,740.65, reference filers LT707207, LT309235, LT509146, LT431853, LT472849
   - LT739619, LX ES, 2026-01 to 2026-06: actual 703,891.14, reference 1,257,359.93, tax effect -44,277.51, reference filers LT743504, LT829307, LT240896, LT510034, LT351711
   - LT779505, LX ES, 2026-01 to 2026-06: actual 1,109,847.02, reference 1,820,927.63, tax effect -56,886.45, reference filers LT162456, LT220805, LT343386, LT517101, LT617556
   - LT785721, LX ES, 2026-01 to 2026-06: actual 836,004.46, reference 1,463,146.18, tax effect -50,171.34, reference filers LT235790, LT643900, LT580334, LT672316, LT628582
   - LT831527, LX ES, 2026-01 to 2026-06: actual 1,090,232.46, reference 1,900,189.18, tax effect -64,796.54, reference filers LT967428, LT145917, LT573415, LT423491, LT807440
   - LT857649, LX ES, 2026-01 to 2026-06: actual 717,685.30, reference 1,273,579.50, tax effect -44,471.53, reference filers LT557468, LT610748, LT742246, LT137777, LT703248
   - LT865419, LX ES, 2026-01 to 2026-06: actual 696,524.18, reference 1,261,739.84, tax effect -45,217.27, reference filers LT976345, LT834191, LT546257, LT557468, LT137777
   - LT916072, LX ES, 2026-01 to 2026-06: actual 760,366.10, reference 1,252,606.42, tax effect -39,379.22, reference filers LT404436, LT631024, LT348307, LT991441, LT379905
   - LT926802, LX ES, 2026-01 to 2026-06: actual 900,678.81, reference 1,471,760.39, tax effect -45,686.53, reference filers LT525278, LT641421, LT304314, LT389340, LT626214
   - LT935497, LX ES, 2026-01 to 2026-06: actual 940,539.01, reference 1,641,693.48, tax effect -56,092.36, reference filers LT590620, LT706504, LT361516, LT389895, LT580334
   - LT940122, LX ES, 2026-01 to 2026-06: actual 1,059,584.30, reference 1,795,269.65, tax effect -58,854.82, reference filers LT389340, LT643641, LT304314, LT939271, LT333877
   - LT962877, LX ES, 2026-01 to 2026-06: actual 1,010,340.53, reference 1,635,448.30, tax effect -50,008.63, reference filers LT483912, LT707207, LT353006, LT819835, LT528164
   - LT975198, LX ES, 2026-01 to 2026-06: actual 684,287.89, reference 1,253,796.59, tax effect -45,560.69, reference filers LT311936, LT652077, LT568457, LT125382, LT419532
   - LT993106, LX ES, 2026-01 to 2026-06: actual 1,290,955.11, reference 2,200,871.10, tax effect -72,793.29, reference filers LT993143, LT975457, LT570566, LT873078, LT907599
   - LT993772, LX ES, 2026-01 to 2026-06: actual 1,256,194.40, reference 2,106,500.03, tax effect -68,024.46, reference filers LT913038, LT975457, LT518544, LT791900, LT396555
   - LT102405, CC LS, 2025-09 to 2026-06: actual 5,002,264.44, reference 5,785,054.41, tax effect -62,623.20, reference filers LT552029, LT568161, LT483912, LT849953, LT119425
   - LT108584, CC FS, 2025-09 to 2026-06: actual 11,326,664.08, reference 12,632,275.95, tax effect -104,448.95, reference filers LT353006, LT643900, LT850471, LT993143, LT711388
   - LT122052, CC FS, 2025-09 to 2026-06: actual 21,670,115.80, reference 22,207,161.70, tax effect -42,963.67, reference filers LT766148, LT333877, LT472849, LT626214, LT348307
   - LT137629, CC FS, 2025-09 to 2026-06: actual 24,651,349.28, reference 25,688,909.64, tax effect -83,004.83, reference filers LT145917, LT285222, LT967428, LT631024, LT641421
   - LT138998, CC LS, 2025-09 to 2026-06: actual 3,251,919.03, reference 3,647,916.66, tax effect -31,679.81, reference filers LT848769, LT819835, LT528164, LT672316, LT652077
   - LT204673, CC FS, 2025-09 to 2026-06: actual 20,538,228.23, reference 15,902,053.12, tax effect 370,894.01, reference filers LT886472, LT764261, LT261320, LT712461, LT361516
   - LT233385, CC FS, 2025-09 to 2026-06: actual 11,055,778.91, reference 12,491,548.44, tax effect -114,861.56, reference filers LT711388, LT807440, LT128971, LT120054, LT518544
   - LT325441, CC FS, 2025-09 to 2026-06: actual 19,597,961.33, reference 20,081,613.86, tax effect -38,692.20, reference filers LT810659, LT626214, LT525278, LT671946, LT130192
   - LT343534, CC FS, 2025-09 to 2026-06: actual 9,494,924.02, reference 10,919,227.74, tax effect -113,944.30, reference filers LT850471, LT807440, LT993143, LT117242, LT570566
   - LT352895, CC FS, 2025-09 to 2026-06: actual 33,403,128.95, reference 33,404,952.48, tax effect -145.88, reference filers LT967428, LT631024, LT509146, LT348307, LT924545
   - LT399552, CC LS, 2025-09 to 2026-06: actual 3,008,673.75, reference 3,223,930.77, tax effect -17,220.56, reference filers LT639645, LT111248, LT117575, LT580334, LT162456
   - LT407803, CC FS, 2025-09 to 2026-06: actual 16,863,791.89, reference 18,180,094.18, tax effect -105,304.19, reference filers LT643641, LT791900, LT472849, LT976345, LT834191
   - LT440289, CC FS, 2025-09 to 2026-06: actual 21,437,616.92, reference 21,663,602.37, tax effect -18,078.84, reference filers LT379905, LT976345, LT834191, LT991441, LT404436
   - LT461231, CC FS, 2025-09 to 2026-06: actual 23,755,196.12, reference 24,899,722.18, tax effect -91,562.09, reference filers LT702915, LT333877, LT924545, LT350083, LT285222
   - LT464783, CC FS, 2025-09 to 2026-06: actual 23,491,349.02, reference 23,586,600.20, tax effect -7,620.09, reference filers LT509146, LT145917, LT257990, LT785351, LT766148
   - LT475994, CC FS, 2025-09 to 2026-06: actual 14,528,371.76, reference 16,652,682.18, tax effect -169,944.84, reference filers LT459270, LT396555, LT939271, LT420642, LT443619
   - LT476882, CC LS, 2025-09 to 2026-06: actual 2,436,199.68, reference 2,864,333.92, tax effect -34,250.74, reference filers LT617556, LT799818, LT979194, LT391079, LT883401
   - LT478177, CC LS, 2025-09 to 2026-06: actual 1,911,344.51, reference 2,250,930.88, tax effect -27,166.91, reference filers LT613560, LT883401, LT557468, LT668505, LT988370
   - LT484097, CC FS, 2025-09 to 2026-06: actual 16,235,714.16, reference 17,828,465.26, tax effect -127,420.09, reference filers LT727446, LT913038, LT643900, LT353006, LT707207
   - LT486280, CC FS, 2025-09 to 2026-06: actual 15,680,150.35, reference 16,764,528.71, tax effect -86,750.27, reference filers LT311233, LT643641, LT913038, LT975457, LT525278
   - LT501894, CC LS, 2025-09 to 2026-06: actual 2,476,964.57, reference 2,749,530.88, tax effect -21,805.30, reference filers LT220805, LT174555, LT343386, LT162456, LT389895
   - LT510219, CC FS, 2025-09 to 2026-06: actual 15,792,915.95, reference 16,644,902.41, tax effect -68,158.92, reference filers LT707207, LT304314, LT443619, LT309235, LT423491
   - LT561612, CC LS, 2025-09 to 2026-06: actual 4,616,882.34, reference 5,126,716.71, tax effect -40,786.75, reference filers LT624364, LT119425, LT706504, LT308643, LT517101
   - LT595171, CC FS, 2025-09 to 2026-06: actual 15,071,375.11, reference 15,918,134.40, tax effect -67,740.74, reference filers LT311233, LT309235, LT727446, LT388304, LT420642
   - LT616039, CC FS, 2025-09 to 2026-06: actual 9,171,274.06, reference 10,367,336.64, tax effect -95,685.01, reference filers LT117242, LT849953, LT703322, LT431853, LT518544
   - LT621182, CC LS, 2025-09 to 2026-06: actual 1,881,148.14, reference 2,214,161.59, tax effect -26,641.07, reference filers LT617667, LT581222, LT847363, LT435294, LT204044
   - LT622477, CC LS, 2025-09 to 2026-06: actual 4,163,258.28, reference 4,417,266.25, tax effect -20,320.64, reference filers LT568161, LT672316, LT819835, LT873078, LT204414
   - LT688411, CC FS, 2025-09 to 2026-06: actual 14,453,879.21, reference 15,898,082.05, tax effect -115,536.23, reference filers LT128971, LT120054, LT939271, LT388304, LT396555
   - LT731109, CC LS, 2025-09 to 2026-06: actual 2,340,912.18, reference 2,625,241.15, tax effect -22,746.32, reference filers LT652077, LT343386, LT220805, LT261320, LT668505
   - LT741173, CC LS, 2025-09 to 2026-06: actual 5,611,259.39, reference 6,036,640.17, tax effect -34,030.46, reference filers LT517101, LT308643, LT483912, LT703322, LT873078
   - LT783131, CC LS, 2025-09 to 2026-06: actual 2,702,499.12, reference 3,078,078.90, tax effect -30,046.38, reference filers LT799818, LT229204, LT111248, LT580334, LT174555
   - LT789754, CC LS, 2025-09 to 2026-06: actual 2,157,268.06, reference 2,572,121.97, tax effect -33,188.31, reference filers LT478584, LT101850, LT988370, LT613560, LT557468
   - LT808106, CC LS, 2025-09 to 2026-06: actual 3,161,314.96, reference 3,621,798.44, tax effect -36,838.68, reference filers LT977825, LT235790, LT639645, LT907599, LT391079
   - LT808180, CC LS, 2025-09 to 2026-06: actual 3,394,198.20, reference 3,899,462.71, tax effect -40,421.16, reference filers LT590620, LT907599, LT235790, LT552029, LT977825
   - LT823646, CC FS, 2025-09 to 2026-06: actual 16,058,731.82, reference 17,818,429.74, tax effect -140,775.83, reference filers LT459270, LT975457, LT304314, LT389340, LT423491
   - LT851248, CC FS, 2025-09 to 2026-06: actual 7,658,050.36, reference 8,791,486.46, tax effect -90,674.89, reference filers LT590620, LT624364, LT431853, LT706504, LT570566
   - LT855984, CC FS, 2025-09 to 2026-06: actual 16,478,843.72, reference 17,746,793.40, tax effect -101,435.97, reference filers LT573415, LT389340, LT810659, LT791900, LT671946
   - LT857760, CC FS, 2025-09 to 2026-06: actual 23,078,195.84, reference 24,279,834.48, tax effect -96,131.09, reference filers LT641421, LT702915, LT257990, LT350083, LT130192
   - LT901457, CC LS, 2025-09 to 2026-06: actual 3,758,666.14, reference 3,998,310.38, tax effect -19,171.54, reference filers LT528164, LT848769, LT204414, LT979194, LT960953
   - LT956143, CC FS, 2025-09 to 2026-06: actual 17,181,874.10, reference 17,959,442.37, tax effect -62,205.46, reference filers LT404436, LT573415, LT785351, LT991441, LT379905
   - LT972830, CC LS, 2025-09 to 2026-06: actual 3,063,863.15, reference 3,267,694.64, tax effect -16,306.52, reference filers LT886472, LT117575, LT960953, LT764261, LT229204
   - LT999877, CC LS, 2025-09 to 2026-06: actual 2,428,446.82, reference 2,679,543.15, tax effect -20,087.71, reference filers LT361516, LT101850, LT617556, LT389895, LT478584
   - LT107881, AH LS, 2025-11 to 2026-06: actual 3,178,789.80, reference 3,317,126.83, tax effect -11,066.96, reference filers LT785351, LT257990, LT702915, LT643900, LT727446
   - LT136667, AH LS, 2025-11 to 2026-06: actual 2,968,889.73, reference 3,273,022.59, tax effect -24,330.63, reference filers LT431853, LT907599, LT873078, LT590620, LT557468
   - LT148396, AH LS, 2025-11 to 2026-06: actual 2,405,254.36, reference 2,558,523.97, tax effect -12,261.57, reference filers LT285222, LT641421, LT573415, LT404436, LT702915
   - LT192130, AH FS, 2025-11 to 2026-06: actual 4,888,610.12, reference 5,156,819.12, tax effect -21,456.72, reference filers LT145917, LT631024, LT350083, LT991441, LT379905
   - LT212036, AH LS, 2025-11 to 2026-06: actual 1,801,273.09, reference 2,033,504.81, tax effect -18,578.54, reference filers LT235790, LT848769, LT988370, LT742246, LT546257
   - LT317560, AH LS, 2025-11 to 2026-06: actual 1,991,423.35, reference 2,172,826.79, tax effect -14,512.27, reference filers LT361516, LT580334, LT235790, LT586809, LT389895
   - LT340648, AH LS, 2025-11 to 2026-06: actual 1,982,321.37, reference 2,049,945.00, tax effect -5,409.89, reference filers LT443619, LT766148, LT389340, LT573415, LT706504
   - LT355263, AH LS, 2025-11 to 2026-06: actual 1,646,546.11, reference 1,810,538.69, tax effect -13,119.41, reference filers LT610748, LT824682, LT137777, LT279228, LT115355
   - LT396888, AH FS, 2025-11 to 2026-06: actual 7,273,107.15, reference 7,760,080.63, tax effect -38,957.88, reference filers LT849953, LT975457, LT431853, LT570566, LT518544
   - LT449206, AH LS, 2025-11 to 2026-06: actual 2,476,743.10, reference 2,530,598.28, tax effect -4,308.41, reference filers LT396555, LT388304, LT517101, LT309235, LT785351
   - LT472738, AH LS, 2025-11 to 2026-06: actual 2,242,875.30, reference 2,406,129.89, tax effect -13,060.37, reference filers LT261320, LT517101, LT819835, LT162456, LT672316
   - LT483542, AH LS, 2025-11 to 2026-06: actual 3,163,237.58, reference 3,310,514.29, tax effect -11,782.14, reference filers LT308643, LT483912, LT643641, LT311233, LT128971
   - LT488759, AH LS, 2025-11 to 2026-06: actual 2,187,087.92, reference 2,372,178.25, tax effect -14,807.23, reference filers LT229204, LT174555, LT391079, LT850471, LT580334
   - LT497639, AH LS, 2025-11 to 2026-06: actual 2,826,770.54, reference 3,178,079.22, tax effect -28,104.69, reference filers LT624364, LT711388, LT799818, LT119425, LT204414
   - LT497750, AH LS, 2025-11 to 2026-06: actual 4,001,560.40, reference 4,107,559.22, tax effect -8,479.91, reference filers LT472849, LT707207, LT671946, LT939271, LT509146
   - LT519913, AH LS, 2025-11 to 2026-06: actual 1,533,279.45, reference 1,691,990.28, tax effect -12,696.87, reference filers LT848769, LT590620, LT568161, LT459270, LT712461
   - LT534121, AH FS, 2025-11 to 2026-06: actual 4,081,344.99, reference 4,418,868.31, tax effect -27,001.87, reference filers LT333877, LT991441, LT348307, LT404436, LT350083
   - LT575413, AH LS, 2025-11 to 2026-06: actual 2,023,055.22, reference 2,235,700.14, tax effect -17,011.59, reference filers LT396555, LT343386, LT389895, LT907599, LT672316
   - LT581037, AH FS, 2025-11 to 2026-06: actual 5,998,988.10, reference 6,161,044.41, tax effect -12,964.51, reference filers LT913038, LT924545, LT671946, LT525278, LT117242
   - LT615965, AH LS, 2025-11 to 2026-06: actual 2,472,033.56, reference 2,707,227.55, tax effect -18,815.52, reference filers LT204414, LT960953, LT353006, LT639645, LT391079
   - LT662918, AH FS, 2025-11 to 2026-06: actual 8,110,982.95, reference 8,208,518.56, tax effect -7,802.85, reference filers LT145917, LT379905, LT976345, LT631024, LT348307
   - LT679161, AH LS, 2025-11 to 2026-06: actual 2,162,836.98, reference 2,454,449.58, tax effect -23,329.01, reference filers LT824682, LT343386, LT162456, LT979194, LT174555
   - LT790013, AH FS, 2025-11 to 2026-06: actual 7,886,340.10, reference 8,391,515.74, tax effect -40,414.05, reference filers LT626214, LT791900, LT810659, LT924545, LT525278
   - LT798042, AH LS, 2025-11 to 2026-06: actual 2,918,016.97, reference 3,083,957.05, tax effect -13,275.21, reference filers LT727446, LT886472, LT308643, LT353006, LT552029
   - LT802815, AH LS, 2025-11 to 2026-06: actual 3,081,486.18, reference 3,244,126.36, tax effect -13,011.21, reference filers LT420642, LT311233, LT423491, LT641421, LT509146
   - LT814174, AH LS, 2025-11 to 2026-06: actual 2,444,327.77, reference 2,640,828.46, tax effect -15,720.06, reference filers LT304314, LT993143, LT939271, LT420642, LT703322
   - LT819539, AH LS, 2025-11 to 2026-06: actual 2,456,163.86, reference 2,459,779.18, tax effect -289.23, reference filers LT639645, LT960953, LT552029, LT261320, LT979194
   - LT831416, AH FS, 2025-11 to 2026-06: actual 5,934,270.39, reference 6,202,968.98, tax effect -21,495.89, reference filers LT570566, LT117242, LT849953, LT304314, LT913038
   - LT861830, AH LS, 2025-11 to 2026-06: actual 2,414,611.97, reference 2,547,447.71, tax effect -10,626.86, reference filers LT528164, LT706504, LT388304, LT309235, LT791900
   - LT864938, AH LS, 2025-11 to 2026-06: actual 3,764,973.96, reference 3,942,275.69, tax effect -14,184.14, reference filers LT423491, LT975457, LT120054, LT807440, LT472849
   - LT898534, AH LS, 2025-11 to 2026-06: actual 1,450,789.02, reference 1,631,970.98, tax effect -14,494.56, reference filers LT568161, LT528164, LT617556, LT668505, LT921548
   - LT910263, AH LS, 2025-11 to 2026-06: actual 2,660,386.12, reference 2,822,569.42, tax effect -12,974.66, reference filers LT993143, LT703322, LT873078, LT711388, LT518544
   - LT935312, AH LS, 2025-11 to 2026-06: actual 3,143,421.13, reference 3,345,937.98, tax effect -16,201.35, reference filers LT128971, LT120054, LT643641, LT483912, LT130192
   - LT946301, AH LS, 2025-11 to 2026-06: actual 2,120,747.90, reference 2,234,340.86, tax effect -9,087.44, reference filers LT443619, LT389340, LT834191, LT967428, LT707207
   - LT964283, AH LS, 2025-11 to 2026-06: actual 1,529,257.51, reference 1,693,048.38, tax effect -13,103.27, reference filers LT976345, LT834191, LT850471, LT459270, LT819835
   - LT972793, AH LS, 2025-11 to 2026-06: actual 3,059,889.47, reference 3,124,740.78, tax effect -5,188.10, reference filers LT624364, LT229204, LT119425, LT799818, LT886472
   - LT977529, AH LS, 2025-11 to 2026-06: actual 2,468,925.23, reference 2,605,095.67, tax effect -10,893.64, reference filers LT967428, LT766148, LT333877, LT285222, LT626214
   - LT981747, AH FS, 2025-11 to 2026-06: actual 3,801,555.41, reference 3,996,558.32, tax effect -15,600.23, reference filers LT130192, LT643900, LT257990, LT810659, LT807440
