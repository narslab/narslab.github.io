---
layout: project
title: project-groundwork/
project: project-groundwork
repo: narslab/project-groundwork
permalink: /:path/:basename:output_ext
---

# **Project Groundwork: Cost-Benefit Analysis of Undergrounding Utility Lines**

This repository contains the data and code used in the research article [Benefits of aggressively co-undergrounding electric and broadband lines outweigh costs](https://www.cell.com/action/showPdf?pii=S2949-7906%2825%2900030-8) (*Cell Reports Sustainability*, 2025). The study introduces a novel data-driven cost-benefit framework and evaluates undergrounding strategies through a detailed case study in Shrewsbury, Massachusetts. The findings indicate that aggressively co-undergrounding electricity and broadband networks provides the highest net benefit when undergrounding is justified.

## **Overview**
This research investigates the economic feasibility and policy implications of undergrounding electricity and broadband networks. The key objectives are:
- Developing a **segment-specific cost model** incorporating local factors such as soil type, density, and infrastructure conditions.
- Simulating **nine undergrounding strategies** varying in **co-undergrounding policy (independent vs. co-undergrounding)** and **aggressiveness (moderate vs. aggressive conversion).**
- Evaluating **cost-benefit trade-offs** across multiple scenarios using sensitivity analyses.
- Providing **actionable insights** for utility planners and policymakers in assessing infrastructure resilience.

### **Key Findings**
- **Aggressive co-undergrounding (CAA strategy) yields the highest net benefit** in scenarios where undergrounding is justified.
- **Independent undergrounding strategies are less cost-effective**, as co-undergrounding reduces trenching costs.
- **The discount rate and undergrounding effectiveness (λ) are critical parameters** affecting the viability of undergrounding.
- **Segment-specific cost models provide more precise cost estimates** than traditional averaging methods.
- **Policy support is essential** as the costs are typically borne by municipalities while the benefits are widely distributed.

## **Methodology**
The research follows a **data-driven approach** integrating multiple data sources, including:
- **Geospatial network data** from Shrewsbury Electric and Cable Operations (SELCO).
- **Historical undergrounding cost data** from Concord, MA.
- **Outage statistics** and economic loss models to evaluate reliability improvements.

The methodology involves:
1. **Cost Modeling:** Life-cycle infrastructure, environmental, and safety cost estimation using regression models.
2. **Benefit Modeling:** Avoided economic loss, property value increase, and enhanced service reliability assessment.
3. **Simulation of Strategies:** Evaluating nine undergrounding strategies over a 40-year period.
4. **Sensitivity Analysis:** Assessing the robustness of undergrounding effectiveness, discount rates, and conversion costs.

## **Repository Structure**
| Directory       | Description                                                                               |
| --------------- | ----------------------------------------------------------------------------------------- |
| `bin/python/`   | Python scripts for cost modeling, benefit analysis, and optimization.
| `bin/jupyter/`  | Jupyter notebooks for analyzing model results and visualization.                          |
| `data/`         | Contains raw and processed data including geospatial, outage, and property value datasets.                 |
| `figures/`      | Visualizations and plots generated from the analysis, such as heatmaps and scatterplots.  |
| `results/`      | Output matrices, model validation results, and analysis outcomes.                         |

## **Contact**
For inquiries and collaborations, contact Mahsa Arabi at marabi@umass.edu.
