---
layout: paper
title: "Explainable Data-Driven Multi-filter Framework for Bot Detection in Incentivized Online Surveys"
image: /images/papers/2026-06-13-ruger-explainable-datadriven-multifilter.png
authors: Andrew Ruger, Mohammed Abdalazeem, Eleni Christofa, Jimi Oke
year: 2026
ref: Ruger et al. 2026. Data Science for Transportation
journal: "Data Science for Transportation 8(2):21."
volume: 8
pdf: /pdfs/papers/2026-ruger-explainable-datadriven-multifilter.pdf
supplement:
doi: 10.1007/s42421-026-00158-4
github:
---

# Abstract

Online surveys have become increasingly popular for academic research due to their cost-effectiveness and ability to reach large populations. However, the use of monetary incentives to encourage participation has led to widespread infiltration by automated bots designed to complete surveys fraudulently. This study presents a transparent, multi-filter framework to detect and remove bot responses, using an incentivized online transportation survey on cycling preferences as a case study. The survey received 12,020 responses over 94 days, with clear evidence of bot activity including 3951 submissions (32.9%) concentrated on a single day. To secure the dataset, we developed an 11-filter pipeline spanning four categories: platform risk scores, duplicate identity detection, behavioral interaction patterns, and device consistency. The multi-filter pipeline removed 94.8% of the submissions. Sensitivity analyses reveal that while platform risk scores (reCAPTCHA, fraud score) screen the bulk of automated traffic, behavioral timing and device checks are essential for catching sophisticated bots. To establish ground-truth performance, we conducted a blind expert review on a data subsample, achieving an 88.9% agreement rate between the automated pipeline and independent human judgment. Finally, to audit the internal coherence of the rules, we trained an explainable XGBoost classifier. The model independently recovered the filter decisions with an F1 score of 0.94 for the human class (precision 0.90, recall 0.98), proving the pipeline captures statistically separable behavioral clusters rather than arbitrary noise. This open-source framework provides researchers with a generalizable, evidence-based template for ensuring data integrity in online surveys.
