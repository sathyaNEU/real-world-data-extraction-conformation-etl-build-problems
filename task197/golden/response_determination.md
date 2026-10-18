# Reserve withdrawal determination, November 2026 delivery month

Reserve portfolio desk, 2026-10-13. Notification to Rijksnet due 2026-10-23.

## Determination

Kampvliet (VKF-KPV) comes out of the reserve portfolio for November 2026 and takes the month's re-prequalification slot. Over the review window it delivered **72 per cent** of the response its contracted characteristic requires, against a tolerance of 90 per cent.

The runner-up is Reiderland (VKF-RDL) at 83 per cent, 11 percentage points above Kampvliet, so the choice of site is not close enough to turn on any single episode.

## Scorecard

| Site | Contracted FCR (MW) | Realised gain (%) | Qualifying episodes | Under tolerance |
|---|---|---|---|---|
| VKF-KPV Kampvliet | 5.00 | 72 | 137 | yes |
| VKF-RDL Reiderland | 2.50 | 83 | 156 | yes |
| VKF-HGZ Hoogezand | 3.00 | 88 | 157 | yes |
| VKF-NWV Nieuwveen | 6.00 | 91 | 113 | no |
| VKF-DLK Dollardkust | 10.00 | 93 | 145 | no |
| VKF-OOS Oosterhout | 6.00 | 95 | 40 | no |
| VKF-MPD Meppelerdiep | 2.00 | 97 | 33 | no |
| VKF-ZWT Zwartewater | 8.00 | 99 | 77 | no |
| VKF-TRB Terborgh | 3.00 | 101 | 77 | no |

Two further sites sit under tolerance: Reiderland at 83 per cent, Hoogezand at 88 per cent. None of them is close to Kampvliet, and under the technical conditions they carry at contracted capacity until a further test slot is offered.

## How the figure is built

Each qualifying episode is read at its extreme second on the published one-second frequency. The response credited to a site is its recorded power at that second less the power its own programme was taking it to at that second, and the programme is moving: every site traverses between settlement period setpoints over a span its controller fixes, which the archive shows at the boundaries where no episode ran. Taking the undisturbed level before the episode instead of the moving programme credits each site with whatever its programme did during the episode, which is why Zwartewater reads 77 per cent on that basis against 99 per cent here.

## Down regulation, availability and imbalance

Down-regulation gains are on the same characteristic and are reported in the workbook; Kampvliet is the lowest there too at 73 per cent, and Meppelerdiep had no qualifying over-frequency episode in the window. Reserve capacity held available and the shortfall against commitment are per block in the workbook; the withdrawn hours are taken from the platform's own log timestamps, which sit ninety seconds after each window opens throughout the file; the start field agrees with that on the rows the alarm handler wrote and reads two hours early on the rest. Outside the blocks they were committed to, the sites delivered 113.7 MWh above programme and 247.8 MWh below it, which is the imbalance position the desk carried and is dominated by the traverse lag rather than by any site missing dispatch.

## Next steps

1. Notify Rijksnet of the withdrawal of VKF-KPV before 2026-10-23 and carry it at zero contracted capacity from 2026-11-01.
2. Book the witnessed step test and pull the droop settings the controller is running, against the settings declared after the firmware change of 15 September.
3. Keep the two sites remaining under tolerance on the watch list and re-measure at the next determination.
