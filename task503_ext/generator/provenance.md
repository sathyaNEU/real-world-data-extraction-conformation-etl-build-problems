# Provenance

Inbound crossings at every US land port of entry on the Canadian and Mexican borders, month by
month since January 1996, with the national transportation series they roll up into, the Federal
Register notices that restricted land-border travel from March 2020 to May 2023, and the
Canadian count of trucks crossing the other way. Every file was downloaded on 2026-10-13.

| File | Rows | What it is | Source |
|---|---|---|---|
| Border_Crossing_Entry_Data.csv | 276,749 | One row per port, measure and month, January 1996 to August 2026: trucks, trains, buses, personal vehicles, and the passengers and pedestrians entering the United States, as counted by US Customs and Border Protection at 118 ports | Bureau of Transportation Statistics, data.bts.gov dataset keg4-3bc2, full CSV export |
| Border_Crossing_Entry_Data_metadata.json | | The dataset's catalogue record: description, column definitions, update frequency, contact, licence | data.bts.gov `api/views/keg4-3bc2.json`, pretty-printed |
| Monthly_Transportation_Statistics.csv | 959 | BTS national monthly series from 1947, 136 columns, including incoming truck and person crossings by border, the value of US freight trade with Canada and Mexico (from 2006), the truck tonnage index, rail carloads and intermodal units, and diesel prices | data.bts.gov dataset crem-w557, full CSV export |
| federal_register_land_port_restrictions_2020-2023.json | 48 | Every Department of Homeland Security notice restricting travel at land ports of entry on either border, from the first notice (effective March 20, 2020) to the termination (May 12, 2023): document number, citation, dates, effective date, abstract and links | Federal Register API, documents search |
| 2020-06217.pdf | | 85 FR 16548, restrictions at the Canadian border as first imposed, with the definition of essential travel | govinfo.gov, as published |
| 2020-06253.pdf | | 85 FR 16547, the same for the Mexican border | govinfo.gov, as published |
| 2021-28063.pdf | | 86 FR 72842, the November 2021 lifting of the Canadian-border restrictions for fully vaccinated travellers | govinfo.gov, as published |
| 2022-01402.pdf | | 87 FR 3429, from January 22, 2022, noncitizens who are not permanent residents may enter at the Canadian border only if fully vaccinated, with no exception for truck drivers | govinfo.gov, as published |
| 2023-09948.pdf | | 88 FR 30033, termination of the Canadian-border restrictions | govinfo.gov, as published |
| 24100002_trucks_1996-2021.csv | 88,080 | Trucks entering Canada from the United States, by Canadian port, province and country of registration (US vehicles entering, Canadian vehicles returning), January 1996 to December 2021 | Statistics Canada table 24-10-0002-01, full-table CSV, rows for trucks from 1996-01 kept as served |
| 24100002_MetaData.csv | | The table's own metadata: title, archive status, dimensions and members, footnotes | Statistics Canada, inside the same download |

## How the files were handled

- No value has been edited. The Statistics Canada table is the only file cut down: the full table
  runs from 1972 for every vehicle type and length of stay (839,880 rows), and only the truck rows
  from January 1996 are kept, each line exactly as served.
- In the crossings file, `Value` is blank for nine port-months and zero where a port reported no
  crossings of that kind. Chief Mountain (port 3315) has no state or coordinates. Port names are not
  unique: Eastport is both port 103 (Maine) and port 3302 (Idaho). `Date` is the month as `Mon YYYY`.
- The national series is assembled by BTS from its own and other agencies' sources and is not
  revised on the same schedule as the port file, so a border total built from the port file does
  not always equal the national figure for the same month. The series labelled "Incoming Person
  Crossings" follows the pedestrian count rather than all persons. April 2023 appears twice, with
  different highway fatality figures.
- Statistics Canada stopped updating table 24-10-0002-01 after December 2021. Cells suppressed for
  confidentiality are blank with status `x`. The national rows equal the sum of the provinces, and
  in every province but Ontario the listed ports add up to the province. Ontario's rows include
  crossings the table does not publish port by port, so its listed ports fall short of the total.

## Licence and required notices

**BTS and Federal Register files** are works of the US federal government and in the public domain
(17 U.S.C. 105). The crossings data carry the US public domain label
(usa.gov/publicdomain/label/1.0) and are attributed to U.S. Customs and Border Protection.

**Statistics Canada** data are used under the Statistics Canada Open Licence
(statcan.gc.ca/en/reference/licence):

> Source: Statistics Canada. Table 24-10-0002-01 Number of vehicles travelling between Canada and
> the United States. DOI: https://doi.org/10.25318/2410000201-eng
>
> Adapted from Statistics Canada, Table 24-10-0002-01 (truck rows from January 1996). This does not
> constitute an endorsement by Statistics Canada of this product.
