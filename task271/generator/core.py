"""The world's fixed parameters: each class's chance that a call in each window reaches the member, the chance a
member reached declines, the age and sex structure of work, and the design and seed the search chose (each region's
level, the member services centre's share of first calls, the share of its unreached cases passed to the vendor, the
vendor calls a passed case received and the share of the region's sample in the last two releases)."""
import numpy as np

P0 = np.array([0.38, 0.36, 0.32])      # not working 80 hours: weekday day, weekday evening, Saturday
P1 = np.array([0.06, 0.27, 0.24])      # worked 80 hours or more in March
RHO = 0.10                              # a member reached declines, either class
KEYQ = 0.80                             # a declining member answers the key question (worked 80 hours in March)
AGE = [(0.34, -0.20), (0.36, 0.25), (0.30, -0.05)]   # share and log-odds shift: 19-29, 30-44, 45-64
SEX = [(0.53, -0.18), (0.47, 0.20)]                   # female, male

# Region order follows common.REGIONS: Great Rivers, Greater Columbia, King, North Central, North Sound, Pierce, Salish,
# Southwest, Spokane, Thurston-Mason. Design 3331 of the search, world seed 5342319.
DESIGN = {
    "pi": [0.5887120860827806, 0.4851698907173701, 0.4668197607375446, 0.5352545938256597, 0.5148384097917245, 0.4518555382995249, 0.611480425508045, 0.6128493715551904, 0.45587539247536146, 0.45922603946419494],
    "msc": [0.843025729228498, 0.38747853523602993, 0.44412904374199247, 0.10797230628680365, 0.5849148763162461, 0.3451150695474544, 0.7412514519456921, 0.432403611133906, 0.14021266008817712, 0.5598650479522623],
    "transfer": [0.24673618010845272, 0.388880812662202, 0.9428012638277632, 0.9310851640691864, 0.31404813274060006, 0.507679344986683, 0.3709780649719785, 0.3542939359760281, 0.37579953999425925, 0.7944453676596994],
    "vcalls": [3, 3, 1, 1, 2, 3, 4, 2, 3, 4],
    "late": [0.25395552995694576, 0.1796147784187512, 0.582407802180416, 0.3917682135701069, 0.312081374312788, 0.20034696424752685, 0.1301286749060147, 0.5406817030628183, 0.07241196004605795, 0.1634827821963424],
}
SEED = 5342319
ASK_SEED = 271003                       # the enrollment files' own stream, apart from the survey's world
