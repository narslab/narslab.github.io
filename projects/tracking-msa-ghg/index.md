---
layout: project
title: tracking-msa-ghg/
project: tracking-msa-ghg
repo: narslab/tracking-msa-ghg
permalink: /:path/:basename:output_ext
---

# tracking-msa-ghg
This repository contains the code and data used in this research. We present a comprehensive accounting and scenario discovery framework for sector-specific regional greenhouse gas emissions. We expect that this framework will be easily deployable to other regions, serving as a useful tool to identify key areas of focus for equitable and effective emissions mitigation planning efforts.

## Overview
In this reasearch, we developed a comprehensive framework for estimating regional GHG inventories from seven sectors (Mobile Combustion, Electricity Consumption, Solid Waste, Stationary Combustion, Agriculture, Wastewater Treatment, and Forestry), forecasting multi-sectoral regional emissions, as well as scenario discovery for effective decarbonization pathways. The following steps were undertaken to complete the research:

1. **Data Collection**
- Obtained relevant activity data and emissions factors, as well as direct emissions estimates from various sources for three planning regions in Connecticut:  Bridgeport (Bridgeport-Stamford-Norwalk metropolitan statistical area and the towns of Bridgewater and New Milford), Hartford (Hartford-east Hartford-Middletown metropolitan statistical area and the towns of Colchester, Lyme, and Old Lyme), New Haven region (New Haven-Milford metropolitan statistical area).

2. **Inventory Estimation**
- Estimated regional inventories using a combination of bottom-up approaches (Mobile Combustion, Electricity Consumption, and Residential subsector), top-down approach of downscaling statewide estimates (Commercial subsector, Agriculture, Forestry and Wastewater Treatment sectors) and available regional estimates (Solid Waste and Industrial subsector).

3. **Emissions Projection**
- Applied the Autoregressive Integrated Moving Average (ARIMA) modeling approach to forecast sector-specific emissions, analyze near-term dynamics (2035) and inter-regional trends.

- 3. **Scenario Discovery**
- Applied the Latin Hypercube sampling method to generate 1,953,125 different states.
- Evaluated each state in the emissions model to obtain emissions futures.
- Used Patient Rule Induction Method to search for the optimal combination of strategies for emissions reductions

4. **Results and visualization**
- Generated comprehensive analysis and visualizations for emissions inventory and prediction, scenario discovery results


<p align="center">
  <img src="https://github.com/user-attachments/assets/6a8848b0-ae77-40b5-b266-558457264d30" alt="scenario-box" width="700"/>
  <img src="https://github.com/user-attachments/assets/b8613354-3da4-43f8-b304-1ad94686278a" alt="msa" width="400"/>
</p>



*PRIM trade-off curves are shown for three decarbonization targets across
different regions, with selected scenarios in each region outlined in red. Map of town boundaries and planning region areas in Connecticut.
.
*

## Repository Structure

| Directory                    | Description                                                                               |
| ---------------              | ----------------------------------------------------------------------------------------- |
| `bin/jupyter`                | Jupyter notebooks for data cleaning, model developing and analyzing.                      |
| `bin/dashboard`              | Jupyter notebooks for dashboard developing.                                               |
| `bin/quality-assurance`      | Jupyter notebooks for quality assurance of inventory methods.                             |
| `data/`                      | Contains raw and cleaned data.                                                            |
| `docs/`                      | Contains report created for the inventory and prediction study.                           |
| `figures/`                   | Visualizations and plots generated from the analysis, such as heatmaps and boxplot.       |
| `results/`                   | Output matrices, model validation results, and analysis outcomes.                         |

## Usage

 1. **Emissions accounting:**  
   Use the models provided to estimate emissions for different MSAs

 2. **Scenario discovery:**  
   Use the models provided to discover the optimal decarbonization pathways

 3. **Interactive dashboard:**  
   Use the models provided to establish the interactive dashboard


## Data Sources
- Obtained daily vehicle miles traveled (DVMT) for each of the relevant counties from the Connecticut Department of Transportation (CTDOT), and vehicle-type distributions from the Federal Transit Administration. Vehicle fuel economy data were obtained from the EPA’s Local Government Greenhouse Gas Inventory Tool (LGGIT).
- County-level electricity consumption data were obtained from EnergizeCT.
- Industrial emissions and Solid Waste emissions, including those from solid waste combustion and landfill methane emissions, were directly acquired from the EPA Facility Level Information on GreenHouse gases Tool (FLIGHT) database.
- Data collected for the Residential subsector included household fuel consumption distributions from the American Community Surveys (ACS) and statewide fuel consumption from the Energy Information Association (EIA).
- Commercial building footprints were obtained via a Python package, OSMnx.
- Agriculture land area, wastewater facility counts, and forestry data were obtained from the United States Department of Agriculture (USDA), EPA National Pollutant Discharge Elimination System (NPDES) permit dataset, and the Connecticut Land Cover database, respectively.
- Corresponding GHG-specific emissions factors (EFs) for each activity obtained from United States EPA Emissions Hub.

## Key Results
The study reveals that there is significant regional variability in emissions patterns and dynamics, highlighting the need for region-specific mitigation strategies. Specifically, our scenario discovery process finds that truck VMT, E-Grid emissions factor, residential fuel oil consumption, and commercial emissions are important influencing features. In addition, multi-sector approach should be taken to achieve a deeper and effective reductions, especially for moderate and deep decarbonization targets. Reducing Truck VMT highlights the need for reduced road transportation by truck and cleaner freight. Targeted building electrification and heating retrofits should be prioritized, given the high E-grid emissions factors and substantial commercial emissions—especially since commercial buildings in Connecticut heavily rely on natural gas and oil for heating. A deep emissions reduction outcome demands synchronized efforts in transportation, electricity grid reform, as well as building electrification, which highlights the need for building or freight energy efficiency upgrades, clean energy procurement, and heating system transitions. 

## Acknowledgments
We acknowledge funding from the South Central Regional Council of Governments (SCRCOG), the Naugutuck Valley Council of Governments (NVCOG) through an Environmental Protection Agency (EPA) Climate Pollution Reduction Grant (CPRG). We also acknowledge partial support from the NSF (Award Number 2325956).
