---
layout: paper
title: "Artificial Intelligence Framework for Crosswalk Detection Across Massachusetts"
image: /images/papers/2024-02-01-apostolov-artificial-intelligence-framework.jpg
authors: Atanas Apostolov, Yuanchang Xie, Chengbo Ai, Francis Tainter, Jimi Oke
year: 2024
ref: Apostolov et al. 2024. Massachusetts Department of Transportation
journal: "Massachusetts Department of Transportation 20-024."
volume:
pdf: /pdfs/papers/2024-apostolov-artificial-intelligence-framework.pdf
supplement:
doi:
github:
website: https://rosap.ntl.bts.gov/view/dot/75247
---

# Abstract

The goal of this project was to develop an artificial intelligence (AI) framework to detect crosswalk locations across the state of Massachusetts, as well as their type classification (continental, parallel lines, or solid) and location category (intersection, midblock, or driveway). Aerial images downloaded from MassGIS were annotated, and these were used to train the AI model, which was then used to detect crosswalks across the entire state using images from both 2019 and 2021. About 88,000 crosswalks were detected in 2021. In terms of location category, 89% of these were intersection crosswalks, 8% were midblock, and 3% were at driveways. In terms of type, just under 65% were continental (zebra-style) crosswalks, about 35% were parallel lines, and less than 1% were solid/painted crosswalks. A python script was developed to perform the post-processing. The model and the post-processing script will be available to MassDOT to perform further analyses, and results will be expected to inform maintenance and safety initiatives.
