---
layout: paper
title: "Enhanced Seasonal Typology-Informed Transit Trip Chaining via Mobile Boarding and Survey Data"
authors: Abdalazeem, Mohammed, Oke, Jimi
year: 2024
ref: Abdalazeem et al. 2024. Data Science for Transportation
journal: "Data Science for Transportation 6(3):NA."
volume: 6
pdf:
doi: 10.1007/s42421-024-00108-y
github:
---
# Abstract
Trip chaining is essential in estimating transit demand models based on big data sources, which hold advantages over traditional data collection methods in terms of both accuracy and cost-effectiveness. However, regional transit systems, accounting for 60% of transit systems in the United States, are often not equipped with smart card systems that are typically needed for trip chaining due to the high costs involved. This study introduces an innovative trip chaining framework that leverages boarding-only mobile ticketing automated fare collection (AFC) data. Our approach incorporates spatiotemporal passenger types obtained via typology analysis. This is followed by calibrating type-specific and season-aware parameters using survey data supplied by the network operators. We then trained a gradient boosting machine to learn the error structure of the initial trip chaining flow estimates and augment final trip frequency predictions. Our findings demonstrate that incorporating spatial error correction significantly improves the trip chaining results. However, the best performance is achieved when season-awareness and typology information are integrated with spatial error correction, reducing the mean absolute error (MAE) by approximately 70% and the symmetric mean absolute percentage error (SMAPE) by 85%. Furthermore, the typology, which we validate with a classification model, provides a deeper understanding of passenger travel characteristics which can facilitate further planning efforts. The spatial error correction model also provides insights into portions of the network that can be better targeted for survey data collection and mobile ticketing adoption to improve future models. Overall, this research will enable regional transit planners to efficiently utilize limited resources and generate valuable insights that would otherwise remain inaccessible.
