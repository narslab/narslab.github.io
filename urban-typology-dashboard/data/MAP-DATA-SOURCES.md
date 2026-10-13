# Map data verification

The previous map copied the dashboard's older `City_Typologies.csv`: six factors and ten clusters. Those IDs cannot be renamed into the final twelve typologies. That legacy CSV is preserved unchanged.

The replacement map is extracted from Jimi Oke's final published study data at pinned commit `039aeb018f95b7cc4073344d30fbe556ccef99e2`:

- Explicit city ID, cluster ID, typology name, country, population: [FINAL-COMBINED-DATASET.xlsx](https://github.com/jimioke/mitei-urban-typologies/blob/039aeb018f95b7cc4073344d30fbe556ccef99e2/FINAL-COMBINED-DATASET.xlsx), sheet `data`.
- Coordinates, independently matching cluster IDs: [published map CSV](https://github.com/jimioke/mitei-urban-typologies/blob/039aeb018f95b7cc4073344d30fbe556ccef99e2/map/12-clusters-9-factors-ward-scaled-sorted-cityID-lat-lon.csv).
- Names and marker colors: [original map script](https://github.com/jimioke/mitei-urban-typologies/blob/039aeb018f95b7cc4073344d30fbe556ccef99e2/map/clustermap.py). The name mapping also agrees with the workbook's `Sheet2` and `scripts/typology-profiles.r`.

All 331 cities are joined by unique `cityID`, with no fuzzy matching, guessing, or conversion from the old cluster IDs. Every final-workbook cluster ID agrees with its same-ID map record. All twelve explicit names agree with the Home/Profile labels. The map CSV's clean spelling for Xi'an is used for the workbook's damaged apostrophe; its city ID and cluster are unchanged. Other city names match exactly.

The audit snapshot `final-city-typologies.csv` contains exactly the records rendered by `map.html`. The intermediate `output/12-clusters-9-factors-ward-scaled.csv` is deliberately not used: it differs from the final workbook (for example, Cordoba).

| Final cluster ID | Explicit final typology | Cities |
| --- | --- | --- |
| 1 | Congested Emerging | 59 |
| 2 | BusTransit Sprawl | 47 |
| 3 | Congested Boomer | 17 |
| 4 | BusTransit Dense | 16 |
| 5 | Hybrid Moderate | 20 |
| 6 | Hybrid Giant | 26 |
| 7 | Auto Sprawl | 51 |
| 8 | Auto Innovative | 14 |
| 9 | MassTransit Heavyweight | 19 |
| 10 | MassTransit Moderate | 30 |
| 11 | MetroBike Giant | 5 |
| 12 | MetroBike Emerging | 27 |

Source SHA-256 checksums:

- `FINAL-COMBINED-DATASET.xlsx`: `be2aaa4290a31e935c7b3745bcd8baf811424351a11b07825e3b570f4ff24ce2`
- `12-clusters-9-factors-ward-scaled-sorted-cityID-lat-lon.csv`: `efe60fcac06bab30d88f6ae4d17df3e7e050db33dabfe91e29ebc40ba3dce2e1`
- `clustermap.py`: `5256076c2de06e5a54030061d8aac44f5f4b015263a8560fbf6a31f2a24007f9`
